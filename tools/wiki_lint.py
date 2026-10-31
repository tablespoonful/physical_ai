"""wiki/ の OKF v0.2 形式、リンク、出典と、_catalog.csv の整合を検査する。

実行: uv run --no-project --with pyyaml python tools/wiki_lint.py
wiki の問題は ERROR (終了コード 1)、既存カタログの問題は WARN とする。
"""
import csv
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote

import yaml

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
DOMAINS = ("VLA", "worldmodel", "ヒューマノイド", "franka(fr3)", "franka_ROS2")
RESERVED = ("index.md", "log.md")
STATUS = ("draft", "stable", "deprecated")
FM = re.compile(r"\A---\n(.*?)\n---\n", re.S)
LINK = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)\)")
FOOTREF = re.compile(r"\[\^([^\]]+)\](?!:)")
FOOTDEF = re.compile(r"^\[\^([^\]]+)\]:", re.M)
errors, warnings = [], []


def rel(p):
    return p.relative_to(ROOT).as_posix()


def exact_exists(p):
    """大文字小文字まで一致するか調べる。Windows でも Linux の失敗を検出するため。"""
    # Path.resolve() は Windows で実際の表記へ直すので、ここでは使わない
    try:
        parts = Path(os.path.normpath(p)).relative_to(ROOT).parts
    except ValueError:
        return False
    cur = ROOT
    for part in parts:
        if not cur.is_dir() or part not in {c.name for c in cur.iterdir()}:
            return False
        cur = cur / part
    return True


def check_target(src, target):
    if re.match(r"[a-z][a-z0-9+.-]*:", target) or target.startswith("#"):
        return
    path = unquote(target.split("#")[0])
    full = WIKI / path[1:] if path.startswith("/") else src.parent / path
    if not exact_exists(full):
        errors.append(f"{rel(src)}: 参照先がない: {target}")


def check_concept(p, text):
    m = FM.match(text)
    if not m:
        errors.append(f"{rel(p)}: frontmatter がない")
        return
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        errors.append(f"{rel(p)}: frontmatter を解析できない: {e}")
        return
    if not fm.get("type"):
        errors.append(f"{rel(p)}: type がない")
    if fm.get("status", "stable") not in STATUS:
        errors.append(f"{rel(p)}: status が不正: {fm['status']}")
    if "resource" in fm:
        check_target(p, str(fm["resource"]))
    ids = set()
    for s in fm.get("sources") or []:
        if "resource" not in s:
            errors.append(f"{rel(p)}: resource のない sources がある")
            continue
        check_target(p, str(s["resource"]))
        if "id" in s:
            ids.add(s["id"])
    body = text[m.end():]
    refs, defs = set(FOOTREF.findall(body)), set(FOOTDEF.findall(body))
    for label in sorted(refs - ids):
        errors.append(f"{rel(p)}: sources にない脚注: {label}")
    for label in sorted(refs ^ defs):
        errors.append(f"{rel(p)}: 脚注の参照と定義が対応しない: {label}")
    for label in sorted(ids - refs):
        errors.append(f"{rel(p)}: 本文で使っていない sources: {label}")
    if "not_checked_with" not in fm:
        errors.append(f"{rel(p)}: not_checked_with がない")
    return body


def check_wiki():
    concepts = []
    for p in sorted(WIKI.rglob("*.md")):
        text = p.read_text(encoding="utf-8")
        if p.name == "index.md":
            body = FM.sub("", text, 1)
            if p.parent != WIKI and FM.match(text):
                errors.append(f"{rel(p)}: index.md の frontmatter はルートだけ")
        elif p.name == "log.md":
            body = text
            for h in re.findall(r"^## (.+)$", text, re.M):
                if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", h):
                    errors.append(f"{rel(p)}: 日付見出しが ISO 8601 でない: {h}")
        else:
            body = check_concept(p, text)
            concepts.append(p)
        for target in LINK.findall(body or ""):
            check_target(p, target)
    index = (WIKI / "index.md").read_text(encoding="utf-8")
    listed = {(WIKI / t).resolve() for t in LINK.findall(index)}
    for p in concepts:
        if p.resolve() not in listed:
            errors.append(f"{rel(p)}: index.md に載っていない")
    return len(concepts)


def check_catalogs():
    for d in DOMAINS:
        with open(ROOT / d / "_catalog.csv", encoding="utf-8-sig", newline="") as f:
            names = {r["local_file"] for r in csv.DictReader(f) if r["local_file"]}
        for n in sorted(names):
            if not (ROOT / d / n).exists():
                warnings.append(f"{d}: カタログの本文がない: {n}")
        for p in sorted((ROOT / d).glob("*.md")):
            if p.name not in ("README.md", "_catalog.md") and p.name not in names:
                warnings.append(f"{d}: カタログにない本文: {p.name}")


n = check_wiki()
check_catalogs()
for w in warnings:
    print("WARN ", w)
for e in errors:
    print("ERROR", e)
print(f"概念 {n} 件、ERROR {len(errors)} 件、WARN {len(warnings)} 件")
sys.exit(1 if errors else 0)
