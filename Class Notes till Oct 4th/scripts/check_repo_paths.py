#!/usr/bin/env python3
"""Fail if anything in this repo would break `git clone` / `git pull` on Windows, macOS or Linux.

Run locally before pushing:   python3 scripts/check_repo_paths.py
Also runs in CI (.github/workflows/path-audit.yml) on every push and pull request.

Checks tracked files for: illegal Windows characters, reserved device names, leading/trailing
spaces or dots, control/non-ASCII characters, case-only and Unicode-normalization collisions,
symlinks, submodule links, paths that are too long, oversized files, and committed junk
(.DS_Store, .venv, __pycache__). Also flags nested .git folders on disk, which make `git add`
silently skip a folder.
"""
import os
import subprocess
import sys
import unicodedata
from collections import defaultdict

ILLEGAL = set('<>:"|?*\\')
RESERVED = {"CON", "PRN", "AUX", "NUL"} | {f"COM{i}" for i in range(1, 10)} | {f"LPT{i}" for i in range(1, 10)}
MAX_PATH_ERROR = 200   # Windows limit is 260 for the WHOLE path, incl. the student's clone folder
MAX_PATH_WARN = 180
MAX_FILE_MB = 50       # GitHub hard-blocks at 100 MB
JUNK_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini"}
SKIP_DIRS = {".git", ".venv", "node_modules", "__pycache__"}


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, check=True).stdout


def main():
    root = git("rev-parse", "--show-toplevel").decode().strip()
    os.chdir(root)

    entries = []
    for rec in git("ls-files", "-z", "--stage").decode("utf-8", "replace").split("\0"):
        if rec:
            meta, path = rec.split("\t", 1)
            entries.append((meta.split()[0], path))

    errors, warnings = [], []
    lower, nfc = defaultdict(set), defaultdict(set)

    for mode, path in entries:
        if mode == "160000":
            errors.append(f"submodule/gitlink (a nested repo was committed): {path}")
        if mode == "120000":
            errors.append(f"symlink (breaks on Windows): {path}")
        if any(ord(c) < 32 for c in path):
            errors.append(f"control character in name: {path!r}")
        if not path.isascii():
            warnings.append(f"non-ASCII characters (unicode normalization differs on macOS): {path}")
        if len(path) > MAX_PATH_ERROR:
            errors.append(f"path is {len(path)} chars (> {MAX_PATH_ERROR}): {path}")
        elif len(path) > MAX_PATH_WARN:
            warnings.append(f"path is {len(path)} chars (> {MAX_PATH_WARN}): {path}")

        for part in path.split("/"):
            if part != part.strip():
                errors.append(f"leading/trailing space in '{part}': {path}")
            if part.endswith("."):
                errors.append(f"trailing dot in '{part}': {path}")
            if part.split(".")[0].upper() in RESERVED:
                errors.append(f"reserved Windows name '{part}': {path}")
            bad = ILLEGAL & set(part)
            if bad:
                errors.append(f"illegal Windows character(s) {''.join(sorted(bad))} in '{part}': {path}")
            if part in JUNK_NAMES or part in {".venv", "__pycache__"} or part.endswith(".pyc"):
                errors.append(f"junk file/folder committed: {path}")
            if part.lower() == ".git":
                errors.append(f"'.git' path component committed: {path}")

        lower[path.lower()].add(path)
        nfc[unicodedata.normalize("NFC", path).lower()].add(path)
        try:
            size = os.path.getsize(path)
            if size > MAX_FILE_MB * 1024 * 1024:
                errors.append(f"file is {size // 1024 // 1024} MB (> {MAX_FILE_MB} MB): {path}")
        except OSError:
            pass

    for group in list(lower.values()) + list(nfc.values()):
        if len(group) > 1:
            errors.append("case/unicode-only collision (breaks Windows/macOS): " + " | ".join(sorted(group)))

    for dirpath, dirnames, _ in os.walk("."):
        if ".git" in dirnames and os.path.abspath(dirpath) != os.path.abspath("."):
            errors.append(
                f"nested .git repo in '{dirpath}' - git will silently skip this folder; "
                f"delete '{dirpath}/.git' (or run `uv init --no-vcs`)"
            )
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

    for w in sorted(set(warnings)):
        print(f"WARNING: {w}")
    for e in sorted(set(errors)):
        print(f"ERROR:   {e}")
    longest = max((len(p) for _, p in entries), default=0)
    print(f"\nChecked {len(entries)} tracked paths (longest: {longest} chars): "
          f"{len(set(errors))} error(s), {len(set(warnings))} warning(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
