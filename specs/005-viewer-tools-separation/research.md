# Research: Viewer Tools Separation

**Feature**: 005-viewer-tools-separation | **Date**: 2026-04-08

---

## R1: File Move Strategy

**Decision**: Create new files in `tools/viewer/`, then delete originals.

**Rationale**: Git will auto-detect renames (content similarity ≥50%) when
files are added and deleted in the same commit. This preserves `git log --follow`
history. Using `git mv` is equivalent but harder to orchestrate through tooling —
the add+delete approach produces the same result.

**Alternatives considered**:
- `git mv`: Equivalent outcome but requires terminal execution for each file. Discarded as no advantage.
- Symlinks: Would keep files discoverable at old paths but violates the "clean separation" goal and confuses some tools.

---

## R2: `dream_events.py` Internal Path Update

**Decision**: Change `VIEWER_HTML` path from `SKILL_DIR / "assets" / "viewer.html"`
to resolve relative to the script's own directory (`Path(__file__).resolve().parent / "viewer.html"`).

**Rationale**: Co-locating both files in `tools/viewer/` means the script can
reference `viewer.html` relative to itself. This removes the dependency on
`SKILL_DIR` for the viewer path, which is correct since the viewer is no longer
part of the skill tree.

**Alternatives considered**:
- Absolute path via config: Overengineering for a co-located file.
- Keep `SKILL_DIR`-relative path: Would require a longer path (`../../assets/viewer.html`) and re-couples viewer to skill layout.

---

## R3: `setup.py` Modification Approach

**Decision**: Remove the `VIEWER_DEPS` constant, `install_viewer_deps()` function,
and step 5 call entirely. Change step count from 5 to 4. No replacement code.

**Rationale**: The security finding `subprocess-pip-install-in-setup` is resolved
by removing the subprocess pip call altogether. Viewer users will install
dependencies manually per `tools/viewer/README.md`. This is the simplest approach
and aligns with the spec (FR-003: "MUST NOT install viewer dependencies").

**Alternatives considered**:
- Replace subprocess with a requirements.txt check: Still couples viewer to setup. Discarded.
- Add optional `--with-viewer` flag to setup.py: Adds complexity, still triggers security scanners. Discarded.

---

## R4: `tools/viewer/README.md` Content

**Decision**: Create a standalone README with: purpose, prerequisites (Python 3.10+,
pip), install command (`pip install aiohttp watchdog`), usage command
(`python dream_events.py`), what it does, and a link back to the main README.

**Rationale**: The viewer README must be self-sufficient since users may navigate
directly to the `tools/viewer/` directory. It replaces the installation step that
was previously automated by setup.py.

**Alternatives considered**:
- requirements.txt only (no README): Insufficient — users need usage instructions, not just deps.
- Full man-page style docs: Overengineering for a 2-file tool.

---

## R5: Documentation Reference Update Scope

**Decision**: Update viewer path references in these files:
1. `SKILL.md` — "Live Dream Viewer (Optional)" section (~lines 188-227)
2. `CONTRIBUTING.md` — contributions type table (~line 41)
3. `.specify/memory/constitution.md` — Development Workflow (~line 148)
4. `.github/copilot-instructions.md` — Project Structure section (auto-updated by agent context script)

Files verified as **not needing changes**:
- `README.md` — contains no direct viewer file paths
- `docs/ARCHITECTURE.md` — references viewer conceptually, no file paths
- `references/REFERENCE.md` — no viewer references
- `references/INSTALL.md` — no viewer references

**Rationale**: Grep results from spec phase confirmed these are the only files
with `dream_events` or `viewer.html` path references. Updating them ensures no
broken references remain.

**Alternatives considered**: None — this is the complete set from grep analysis.

---

## R6: Security Finding Resolution

**Decision**: Both findings resolved by the move:
- `subprocess-pip-install-in-setup`: Removed entirely (R3).
- `aiohttp-websocket-server`: Isolated to `tools/viewer/` — explicitly optional,
  not part of the installed skill surface. The WebSocket server itself is not
  changed (it's a local development tool, not exposed externally).

**Rationale**: The security scan flagged these as risks in the skill installation
path. Moving the viewer out of the install path removes both from the scan scope.
The WebSocket server remains local-only (binds to localhost:9736) and is unchanged.

**Alternatives considered**: None — separation is the prescribed mitigation from the spec.
