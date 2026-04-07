"""
electric_sheep.py  v5.0
───────────────────────
OpenDream — nightly dream skill for agents.

Triggered by system cron at 23:00. Reads context from disk.
Delegates all LLM generation to the agent CLI (OpenClaw or Hermes) —
uses the agent's configured model, not its own API clients.
Writes dream output to disk. Exits cleanly by ~04:50.

Usage:
    python3 electric_sheep.py
    python3 electric_sheep.py --config /path/to/skill.yaml
    python3 electric_sheep.py --dry-run        # context only, no LLM calls
    python3 electric_sheep.py --test-mode      # fast timing for testing
    python3 electric_sheep.py --agent openclaw # force agent CLI (default: auto)
    python3 electric_sheep.py --agent hermes

Requires: pyyaml pytz
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import signal
import subprocess
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

import yaml

logger = logging.getLogger("open-dream")

SKILL_ROOT   = Path(__file__).resolve().parent.parent
CONFIG_PATH  = SKILL_ROOT / "assets" / "skill.yaml"
PROMPTS_PATH = SKILL_ROOT / "references" / "prompts.yaml"


# ── Config ──────────────────────────────────────────────────────────────────────

def load_config(path: Path, test_mode: bool = False) -> dict:
    with open(path) as f:
        cfg = yaml.safe_load(f)
    if test_mode:
        tm = cfg.get("test_mode", {})
        cfg["sleep_cycles"]["nrem_duration_mins"] = tm.get("nrem_duration_mins", 0)
        cfg["sleep_cycles"]["rem_durations_mins"]  = tm.get("rem_durations_mins", [1,1,1,1,1])
        cfg["dream_interval_seconds"] = tm.get("dream_interval_seconds", 5)
        logger.info("Test mode active — timing overridden")
    return cfg


def load_prompts(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


# ── Agent CLI detection ─────────────────────────────────────────────────────────

def detect_agent() -> str:
    """Auto-detect which agent CLI is available. Returns 'openclaw' or 'hermes'."""
    for cmd in ("openclaw", "hermes"):
        result = subprocess.run(
            [cmd, "--version"],
            capture_output=True, timeout=5,
        )
        if result.returncode == 0:
            logger.info("Detected agent CLI: %s", cmd)
            return cmd
    raise RuntimeError(
        "No agent CLI found. Install OpenClaw or Hermes and ensure it is in PATH."
    )


class AgentBackend:
    """
    Delegates LLM generation to the agent's CLI.

    OpenClaw:  openclaw run --quiet --output json "<prompt>"
    Hermes:    hermes run --quiet --output json "<prompt>"

    Both CLIs accept a prompt, use the agent's configured model,
    and return the response. The skill never touches API keys directly.
    """

    def __init__(self, agent: str):
        self.agent = agent  # "openclaw" | "hermes"

    async def generate(self, system: str, prompt: str,
                       max_tokens: int = 80) -> str:
        """
        Shell out to the agent CLI with the combined system + user prompt.
        Returns the agent's response text.
        """
        # Combine system and user prompt for CLI invocation
        full_prompt = f"{system}\n\n---\n\n{prompt}"

        if self.agent == "openclaw":
            cmd = [
                "openclaw", "run",
                "--quiet",
                "--no-memory",       # don't pollute session with dream turns
                "--max-tokens", str(max_tokens),
                full_prompt,
            ]
        else:  # hermes
            cmd = [
                "hermes", "run",
                "--quiet",
                "--skip-memory",     # same — keep dream turns out of memory
                "--max-tokens", str(max_tokens),
                full_prompt,
            ]

        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(), timeout=120
            )
            if proc.returncode != 0:
                logger.warning(
                    "Agent CLI returned %d: %s",
                    proc.returncode,
                    stderr.decode().strip()[:200],
                )
                return ""
            return stdout.decode().strip()

        except asyncio.TimeoutError:
            logger.warning("Agent CLI timed out after 120s")
            proc.kill()
            return ""
        except FileNotFoundError:
            raise RuntimeError(
                f"Agent CLI '{self.agent}' not found in PATH. "
                "Is it installed and on your PATH?"
            )

    async def healthcheck(self) -> bool:
        """Verify the agent CLI is reachable."""
        try:
            result = subprocess.run(
                [self.agent, "--version"],
                capture_output=True, timeout=5,
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    @property
    def label(self) -> str:
        return self.agent


def build_backend(cfg: dict, agent_override: Optional[str] = None) -> AgentBackend:
    agent = agent_override or cfg.get("agent", "auto")
    if agent == "auto":
        agent = detect_agent()
    return AgentBackend(agent=agent)


# ── Context gathering ───────────────────────────────────────────────────────────

def _read_jsonl_session(agent_id: str, limit: int = 10) -> list[dict]:
    """Read recent user/assistant turns from the active session JSONL."""
    # OpenClaw session location
    sessions_dir = Path.home() / ".openclaw" / "agents" / agent_id / "sessions"
    if not sessions_dir.exists():
        # Hermes session location
        sessions_dir = Path.home() / ".hermes" / "sessions"
    if not sessions_dir.exists():
        return []

    jsonl_files = sorted(
        sessions_dir.glob("*.jsonl"),
        key=lambda f: f.stat().st_mtime,
        reverse=True,
    )
    if not jsonl_files:
        return []

    messages = []
    for line in jsonl_files[0].read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
            if msg.get("role") in ("user", "assistant"):
                content = msg.get("content", "")
                if isinstance(content, list):
                    content = " ".join(
                        b.get("text", "") for b in content
                        if isinstance(b, dict) and b.get("type") == "text"
                    )
                messages.append({
                    "role":    msg["role"],
                    "content": str(content)[:150],
                })
        except (json.JSONDecodeError, KeyError):
            continue

    return messages[-limit:]


def _read_json_file(path_str: str) -> list | dict | None:
    if not path_str:
        return None
    path = Path(path_str.replace("~", str(Path.home())))
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


@dataclass
class DreamContext:
    recent_interactions: list = field(default_factory=list)
    pending_reminders:   list = field(default_factory=list)
    calendar_today:      list = field(default_factory=list)
    calendar_tomorrow:   list = field(default_factory=list)
    tfl_status:  Optional[str] = None
    weather:     Optional[str] = None
    gathered_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_prompt_block(self) -> str:
        lines = ["## Agent context gathered at dream-start"]

        if self.recent_interactions:
            lines.append("\n### Recent interactions")
            for t in self.recent_interactions[-5:]:
                lines.append(f"  [{t['role']}] {t['content']}")

        if self.pending_reminders:
            lines.append("\n### Pending reminders")
            for r in self.pending_reminders:
                lines.append(f"  - {r}")

        if self.calendar_today:
            lines.append("\n### Today")
            for e in self.calendar_today:
                lines.append(f"  - {e}")

        if self.calendar_tomorrow:
            lines.append("\n### Tomorrow")
            for e in self.calendar_tomorrow:
                lines.append(f"  - {e}")

        if self.tfl_status:
            lines.append(f"\n### TfL  {self.tfl_status}")

        if self.weather:
            lines.append(f"\n### Weather  {self.weather}")

        if len(lines) == 1:
            lines.append("\n  (no context available — dreaming without memory)")

        return "\n".join(lines)

    def is_empty(self) -> bool:
        return not any([
            self.recent_interactions, self.pending_reminders,
            self.calendar_today, self.calendar_tomorrow,
            self.tfl_status, self.weather,
        ])


def gather_context(cfg: dict) -> DreamContext:
    """Gather all context from disk. All sources fail silently."""
    ctx_cfg  = cfg.get("context", {})
    agent_id = ctx_cfg.get("agent_id", "default")

    interactions = []
    try:
        interactions = _read_jsonl_session(agent_id, limit=10)
        logger.info("Context: %d recent interactions", len(interactions))
    except Exception as e:
        logger.debug("Context: interactions unavailable — %s", e)

    reminders = []
    try:
        data = _read_json_file(ctx_cfg.get("reminders", ""))
        if isinstance(data, list):
            reminders = [str(r) for r in data[:8]]
        logger.info("Context: %d reminders", len(reminders))
    except Exception as e:
        logger.debug("Context: reminders unavailable — %s", e)

    cal_today, cal_tomorrow = [], []
    try:
        data = _read_json_file(ctx_cfg.get("calendar", ""))
        if isinstance(data, dict):
            cal_today    = [str(e) for e in data.get("today",    [])[:8]]
            cal_tomorrow = [str(e) for e in data.get("tomorrow", [])[:8]]
        logger.info("Context: %d today, %d tomorrow", len(cal_today), len(cal_tomorrow))
    except Exception as e:
        logger.debug("Context: calendar unavailable — %s", e)

    tfl = None
    try:
        data = _read_json_file(ctx_cfg.get("tfl_cache", ""))
        if isinstance(data, dict):
            tfl = data.get("summary")
    except Exception as e:
        logger.debug("Context: TfL unavailable — %s", e)

    weather = None
    try:
        data = _read_json_file(ctx_cfg.get("weather_cache", ""))
        if isinstance(data, dict):
            weather = data.get("brief")
    except Exception as e:
        logger.debug("Context: weather unavailable — %s", e)

    return DreamContext(
        recent_interactions = interactions,
        pending_reminders   = reminders,
        calendar_today      = cal_today,
        calendar_tomorrow   = cal_tomorrow,
        tfl_status          = tfl,
        weather             = weather,
    )


# ── Prompt builder ──────────────────────────────────────────────────────────────

class PromptBuilder:
    THOUGHT_TEMPLATE = """\
{context}

## Current dream cycle
{instruction}

---
Generate your next dream thought. One sentence only. No quotation marks.

Previous thoughts this session (do not repeat):
{previous}
"""

    MORNING_NOTE_TEMPLATE = """\
{context}

## The night is ending
You have completed 5 sleep cycles:
1. Emotional Review
2. Creative Association
3. Cognitive Processing
4. Memory Consolidation
5. Future Simulation

{instruction}

All thoughts from tonight:
{all_thoughts}
"""

    def __init__(self, prompts: dict):
        self.base    = prompts.get("system_base", "You are a dreaming agent. Dream.").strip()
        self.cycles  = prompts.get("cycles", {})
        self.morning = prompts.get("morning_note", {})

    def for_thought(self, cycle_number: int, ctx: DreamContext,
                    previous: list[str]) -> tuple[str, str]:
        cc = self.cycles.get(cycle_number, {})
        system = self.base + "\n\n" + cc.get("instruction", "Dream.").strip()
        previous_block = (
            "\n".join(f"  - {t}" for t in previous[-12:]) or "  (none yet)"
        )
        user = self.THOUGHT_TEMPLATE.format(
            context     = ctx.to_prompt_block(),
            instruction = cc.get("instruction", "Dream.").strip(),
            previous    = previous_block,
        )
        return system, user

    def for_morning_note(self, ctx: DreamContext,
                         all_thoughts: list[str]) -> tuple[str, str]:
        system = self.base
        thought_block = (
            "\n".join(f"  - {t}" for t in all_thoughts[-30:])
            or "  (no thoughts recorded)"
        )
        user = self.MORNING_NOTE_TEMPLATE.format(
            context      = ctx.to_prompt_block(),
            instruction  = self.morning.get("instruction", "Write a morning note.").strip(),
            all_thoughts = thought_block,
        )
        return system, user


# ── Sleep cycle data ────────────────────────────────────────────────────────────

@dataclass
class SleepCycle:
    number:    int
    name:      str
    purpose:   str
    style:     str
    nrem_mins: int
    rem_mins:  int

    @property
    def label(self) -> str:
        return f"cycle {self.number} — {self.name}"


def build_cycles(cfg: dict, prompts: dict) -> list[SleepCycle]:
    sc       = cfg.get("sleep_cycles", {})
    nrem     = sc.get("nrem_duration_mins", 50)
    rem_list = sc.get("rem_durations_mins", [10, 15, 20, 30, 45])
    p_cycles = prompts.get("cycles", {})

    return [
        SleepCycle(
            number    = i + 1,
            name      = p_cycles.get(i + 1, {}).get("name",    f"Cycle {i+1}"),
            purpose   = p_cycles.get(i + 1, {}).get("purpose", ""),
            style     = p_cycles.get(i + 1, {}).get("style",   "reflective"),
            nrem_mins = nrem,
            rem_mins  = rem_mins,
        )
        for i, rem_mins in enumerate(rem_list)
    ]


# ── Output ──────────────────────────────────────────────────────────────────────

def resolve_output_dir(cfg: dict) -> Path:
    env = os.environ.get("OPENDREAM_OUTPUT")
    if env:
        return Path(env).expanduser()
    raw = cfg.get("output", {}).get("path", "~/.openclaw/workspace/dreams")
    return Path(str(raw).replace("~", str(Path.home())))


def write_cycle(output_dir: Path, date_str: str, cycle: SleepCycle,
                thoughts: list[str], agent: str,
                started_at: str, finished_at: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    slug = cycle.name.lower().replace(" ", "_")
    path = output_dir / f"{date_str}_cycle{cycle.number}_{slug}.json"
    path.write_text(json.dumps({
        "cycle":       cycle.number,
        "name":        cycle.name,
        "purpose":     cycle.purpose,
        "thoughts":    thoughts,
        "agent":       agent,
        "started_at":  started_at,
        "finished_at": finished_at,
    }, indent=2, ensure_ascii=False))
    logger.info("Written: %s (%d thoughts)", path.name, len(thoughts))


def write_morning_note(output_dir: Path, date_str: str,
                       text: str, agent: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{date_str}_morning_note.json"
    path.write_text(json.dumps({
        "text":       text,
        "agent":      agent,
        "written_at": datetime.now().isoformat(),
    }, indent=2, ensure_ascii=False))
    logger.info("Morning note written: %s", path.name)


def write_lock(output_dir: Path, cycle_number: int, cycle_name: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / ".dream_active").write_text(json.dumps({
        "active":     True,
        "cycle":      cycle_number,
        "cycle_name": cycle_name,
        "since":      datetime.now().isoformat(),
    }))


def clear_lock(output_dir: Path) -> None:
    lock = output_dir / ".dream_active"
    if lock.exists():
        lock.unlink()


# ── REM dream burst ─────────────────────────────────────────────────────────────

async def rem_burst(
    backend: AgentBackend,
    cycle: SleepCycle,
    ctx: DreamContext,
    builder: PromptBuilder,
    all_thoughts: list[str],
    interval_secs: int,
    dry_run: bool = False,
) -> list[str]:
    deadline       = time.monotonic() + cycle.rem_mins * 60
    cycle_thoughts: list[str] = []

    logger.info(
        "REM %s — %d min [%s]",
        cycle.label, cycle.rem_mins, backend.label,
    )

    if dry_run:
        logger.info("DRY RUN — skipping generation for %s", cycle.label)
        await asyncio.sleep(min(cycle.rem_mins * 60, 3))
        return ["[dry run]"]

    while time.monotonic() < deadline:
        try:
            system, prompt = builder.for_thought(cycle.number, ctx, all_thoughts)
            raw  = await backend.generate(system, prompt)
            text = raw.strip('"\'').strip()

            if not text:
                await asyncio.sleep(interval_secs)
                continue

            all_thoughts.append(text)
            cycle_thoughts.append(text)
            logger.debug("[%s][%s] %s", backend.label, cycle.label, text)

            await asyncio.sleep(interval_secs)

        except asyncio.CancelledError:
            logger.info("REM interrupted — %s", cycle.label)
            break
        except Exception as exc:
            logger.warning("Generation error — %s", exc)
            await asyncio.sleep(interval_secs * 2)

    logger.info("REM complete — %s: %d thoughts", cycle.label, len(cycle_thoughts))
    return cycle_thoughts


# ── Night orchestrator ──────────────────────────────────────────────────────────

async def run_night(cfg: dict, backend: AgentBackend,
                    dry_run: bool = False) -> None:
    prompts    = load_prompts(PROMPTS_PATH)
    cycles     = build_cycles(cfg, prompts)
    builder    = PromptBuilder(prompts)
    output_dir = resolve_output_dir(cfg)
    interval   = cfg.get("dream_interval_seconds", 30)
    date_str   = datetime.now().strftime("%Y-%m-%d")
    all_thoughts: list[str] = []

    if not dry_run and not await backend.healthcheck():
        logger.error(
            "Agent CLI '%s' not available — aborting dream", backend.agent
        )
        return

    logger.info(
        "Night begins — %d cycles, agent=%s, output=%s",
        len(cycles), backend.label, output_dir,
    )

    ctx = gather_context(cfg)
    if ctx.is_empty():
        logger.warning("No context available — dreaming without memory")
    else:
        logger.info("Context gathered: %s", ctx.gathered_at)

    for cycle in cycles:
        # NREM — silence
        if cycle.nrem_mins > 0:
            logger.info("NREM %s — sleeping for %d min", cycle.label, cycle.nrem_mins)
            write_lock(output_dir, cycle.number, f"NREM — {cycle.name}")
            await asyncio.sleep(cycle.nrem_mins * 60)

        # REM — dream
        write_lock(output_dir, cycle.number, cycle.name)
        started_at = datetime.now().isoformat()

        thoughts = await rem_burst(
            backend       = backend,
            cycle         = cycle,
            ctx           = ctx,
            builder       = builder,
            all_thoughts  = all_thoughts,
            interval_secs = interval,
            dry_run       = dry_run,
        )

        write_cycle(
            output_dir  = output_dir,
            date_str    = date_str,
            cycle       = cycle,
            thoughts    = thoughts,
            agent       = backend.label,
            started_at  = started_at,
            finished_at = datetime.now().isoformat(),
        )

    # Morning note
    note_cfg = cfg.get("morning_note", {})
    if note_cfg.get("enabled", True) and not dry_run:
        try:
            logger.info("Writing morning note")
            system, prompt = builder.for_morning_note(ctx, all_thoughts)
            note = await backend.generate(system, prompt, note_cfg.get("max_tokens", 150))
            write_morning_note(output_dir, date_str, note, backend.label)
        except Exception as exc:
            logger.warning("Morning note failed — %s", exc)

    clear_lock(output_dir)
    logger.info(
        "Night complete — %d total thoughts across %d cycles",
        len(all_thoughts), len(cycles),
    )


# ── Entry point ─────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="OpenDream — nightly dream skill for agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 electric_sheep.py                          # auto-detect agent
  python3 electric_sheep.py --agent openclaw         # force OpenClaw
  python3 electric_sheep.py --agent hermes           # force Hermes
  python3 electric_sheep.py --dry-run                # context only, no generation
  python3 electric_sheep.py --test-mode              # fast timing for testing
  python3 electric_sheep.py --config /my/skill.yaml  # custom config
        """,
    )
    parser.add_argument(
        "--config", type=Path, default=CONFIG_PATH,
        help="Path to skill.yaml (default: assets/skill.yaml)",
    )
    parser.add_argument(
        "--agent", choices=["openclaw", "hermes", "auto"], default="auto",
        help="Agent CLI to use for generation (default: auto-detect)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Gather and print context only — no generation",
    )
    parser.add_argument(
        "--test-mode", action="store_true",
        help="Fast timing — 1 min per cycle, 5s intervals",
    )
    parser.add_argument(
        "--log-level", default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
    )
    args = parser.parse_args()

    logging.basicConfig(
        level   = getattr(logging, args.log_level),
        format  = "%(asctime)s [%(name)s] %(levelname)s %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S",
    )

    cfg     = load_config(args.config, test_mode=args.test_mode)
    backend = build_backend(cfg, agent_override=(
        None if args.agent == "auto" else args.agent
    ))

    if args.dry_run:
        ctx = gather_context(cfg)
        print("\n" + ctx.to_prompt_block() + "\n")
        return

    output_dir = resolve_output_dir(cfg)

    loop = asyncio.new_event_loop()
    task = loop.create_task(run_night(cfg, backend))

    def _shutdown(sig, _frame):
        logger.info("Signal %s — cancelling dream", sig)
        task.cancel()
        clear_lock(output_dir)

    signal.signal(signal.SIGTERM, _shutdown)
    signal.signal(signal.SIGINT,  _shutdown)

    try:
        loop.run_until_complete(task)
    except asyncio.CancelledError:
        logger.info("Dream cancelled")
    finally:
        loop.close()


if __name__ == "__main__":
    main()
