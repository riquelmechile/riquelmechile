#!/usr/bin/env python3
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
errors = []

banned_svg = (
    "<image", "data:image", "base64,", "<script", "javascript:",
    "<foreignobject", "onload=", "onclick=", "onerror="
)

svg_files = sorted(ROOT.glob("assets/**/*.svg"))
if not svg_files:
    errors.append("No SVG assets found.")

for path in svg_files:
    text = path.read_text(encoding="utf-8")
    low = text.lower()
    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid XML: {exc}")
        continue

    if not root.tag.endswith("svg"):
        errors.append(f"{path.relative_to(ROOT)}: root is not svg")
    for attr in ("viewBox", "role", "aria-labelledby"):
        if not root.attrib.get(attr):
            errors.append(f"{path.relative_to(ROOT)}: missing {attr}")
    if root.attrib.get("role") != "img":
        errors.append(f"{path.relative_to(ROOT)}: role must be img")

    title = next((el for el in root.iter() if el.tag.endswith("title")), None)
    desc = next((el for el in root.iter() if el.tag.endswith("desc")), None)
    if title is None or not (title.text or "").strip():
        errors.append(f"{path.relative_to(ROOT)}: missing non-empty title")
    if desc is None or not (desc.text or "").strip():
        errors.append(f"{path.relative_to(ROOT)}: missing non-empty desc")

    ids = [el.attrib["id"] for el in root.iter() if "id" in el.attrib]
    if len(ids) != len(set(ids)):
        errors.append(f"{path.relative_to(ROOT)}: duplicate id")
    for token in banned_svg:
        if token in low:
            errors.append(f"{path.relative_to(ROOT)}: banned SVG token {token}")
    for el in root.iter():
        for attr_name, attr_value in el.attrib.items():
            if attr_name.endswith("href") and str(attr_value).startswith(("http://", "https://")):
                errors.append(f"{path.relative_to(ROOT)}: external SVG dependency {attr_value}")

readme = (ROOT / "README.md").read_text(encoding="utf-8")

required = (
    "https://x.com/riquelme44127",
    "https://www.linkedin.com/in/sebastian-riquelme-vera-482778198",
    "https://github.com/riquelmechile/io",
    "https://github.com/riquelmechile/EAUTO-AI",
    "https://github.com/riquelmechile/msl-collab",
    "https://github.com/riquelmechile/zanaX",
    "https://github.com/riquelmechile/Skills-Chile",
    "3.609", "50 días activos", "21 días", "427",
)
for needle in required:
    if needle not in readme:
        errors.append(f"README missing required content: {needle}")

for bad in ("capsule-render", "readme-typing-svg", "github-profile-summary-cards", "komarev.com"):
    if bad in readme:
        errors.append(f"README depends on banned external profile service: {bad}")

asset_refs = set(re.findall(r'(?:src|srcset)="([^"]+\.svg)"', readme))
for ref in asset_refs:
    if ref.startswith(("http://", "https://")):
        errors.append(f"README SVG must be local: {ref}")
        continue
    if not (ROOT / ref).is_file():
        errors.append(f"README references missing asset: {ref}")

if len(svg_files) < 11:
    errors.append(f"Expected at least 11 SVG assets, found {len(svg_files)}")

if errors:
    print("PROFILE VALIDATION FAILED")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print(f"PROFILE VALIDATION OK · {len(svg_files)} SVG assets · {len(asset_refs)} referenced assets")
