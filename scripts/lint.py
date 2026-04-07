#!/usr/bin/env python3
"""Wiki lint helper — structural checks for the Research Wiki.

Checks performed:
  1. Broken wikilinks: [[slug]] target file does not exist
  2. Orphan pages: pages with zero incoming links
  3. Missing required YAML frontmatter fields
  4. Cross-reference asymmetry: forward link exists but reverse is missing

Usage:
    python scripts/lint.py                  # lint wiki/ in current dir
    python scripts/lint.py --wiki-dir wiki/ # specify wiki directory
"""

import argparse
import os
import re
import sys
from pathlib import Path

WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]*)?\]\]")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)

# Required fields per page type
REQUIRED_FIELDS = {
    "papers": ["title", "slug", "tags", "importance"],
    "concepts": ["title", "tags", "maturity", "key_papers"],
    "topics": ["title", "tags"],
    "people": ["name", "tags"],
    "Summary": ["title", "scope", "key_topics"],
}


class LintIssue:
    def __init__(self, level: str, category: str, file: str, message: str):
        self.level = level      # 🔴 🟡 🔵
        self.category = category
        self.file = file
        self.message = message

    def __str__(self):
        return f"{self.level} [{self.category}] {self.file}: {self.message}"


def find_all_pages(wiki_dir: Path) -> dict[str, Path]:
    """Map slug -> file path for all wiki pages."""
    pages = {}
    for subdir in ["papers", "concepts", "topics", "people", "Summary"]:
        dir_path = wiki_dir / subdir
        if not dir_path.exists():
            continue
        for f in dir_path.glob("*.md"):
            slug = f.stem
            pages[slug] = f
    return pages


def extract_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter as dict (basic parsing)."""
    m = FRONTMATTER_RE.match(content)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).split("\n"):
        if ":" in line:
            key = line.split(":")[0].strip()
            fm[key] = True  # Just check key existence
    return fm


def lint(wiki_dir: Path) -> list[LintIssue]:
    issues = []
    pages = find_all_pages(wiki_dir)

    # Track incoming links for orphan detection
    incoming: dict[str, set[str]] = {slug: set() for slug in pages}

    for slug, fpath in pages.items():
        content = fpath.read_text(encoding="utf-8")
        rel = fpath.relative_to(wiki_dir)

        # 1. Check frontmatter
        fm = extract_frontmatter(content)
        page_type = fpath.parent.name
        for field in REQUIRED_FIELDS.get(page_type, []):
            if field not in fm:
                issues.append(LintIssue("🔴", "missing-field", str(rel),
                                        f"Missing required field: {field}"))

        # 2. Check wikilinks
        for match in WIKILINK_RE.finditer(content):
            target = match.group(1).strip()
            if target in pages:
                incoming.setdefault(target, set()).add(slug)
            else:
                issues.append(LintIssue("🟡", "broken-link", str(rel),
                                        f"[[{target}}}] → file not found"))

    # 3. Orphan pages (no incoming links, exclude index-like files)
    for slug, fpath in pages.items():
        if not incoming.get(slug):
            rel = fpath.relative_to(wiki_dir)
            issues.append(LintIssue("🔵", "orphan", str(rel),
                                    "No incoming links"))

    # 4. Cross-reference asymmetry (check key_papers ↔ Related)
    for slug, fpath in pages.items():
        content = fpath.read_text(encoding="utf-8")
        if fpath.parent.name == "concepts":
            # Check key_papers field
            for match in re.finditer(r"key_papers:\s*\[(.*?)\]", content):
                for ref in re.findall(r"(\S+)", match.group(1)):
                    ref = ref.rstrip(",")
                    ref_path = wiki_dir / "papers" / f"{ref}.md"
                    if ref_path.exists():
                        ref_content = ref_path.read_text(encoding="utf-8")
                        if f"[[{slug}]]" not in ref_content and f"[[{slug}" not in ref_content:
                            issues.append(LintIssue("🟡", "xref-asymmetry", str(fpath.relative_to(wiki_dir)),
                                                    f"key_papers has {ref} but paper doesn't link back"))

    return issues


def main():
    parser = argparse.ArgumentParser(description="Research Wiki linter")
    parser.add_argument("--wiki-dir", default="wiki/", help="Path to wiki directory")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    wiki_dir = Path(args.wiki_dir)
    if not wiki_dir.exists():
        print(f"Error: {wiki_dir} does not exist", file=sys.stderr)
        sys.exit(1)

    issues = lint(wiki_dir)

    if args.json:
        import json
        print(json.dumps([{
            "level": i.level,
            "category": i.category,
            "file": i.file,
            "message": i.message,
        } for i in issues], indent=2, ensure_ascii=False))
    else:
        red = sum(1 for i in issues if i.level == "🔴")
        yellow = sum(1 for i in issues if i.level == "🟡")
        blue = sum(1 for i in issues if i.level == "🔵")
        print(f"Lint: {red} 🔴, {yellow} 🟡, {blue} 🔵\n")
        for issue in sorted(issues, key=lambda i: ("🔴🟡🔵".index(i.level), i.file)):
            print(issue)
        if not issues:
            print("No issues found.")


if __name__ == "__main__":
    main()
