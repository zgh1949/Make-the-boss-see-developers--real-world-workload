
import argparse
import base64
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
HTML_PATH = ROOT / "index.html"
SRC_DIR = ROOT / "src"

SPECIAL_MAP = {
    "note_mac": "ref",
}


def img_to_base64(img_path: Path) -> str:
    with open(img_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
        return f"data:image/png;base64,{b64}"


def read_html() -> str:
    return HTML_PATH.read_text(encoding="utf-8", newline="")


def write_html(html: str):
    HTML_PATH.write_text(html, encoding="utf-8", newline="")


def i_img_bounds(html: str):
    start = html.index("var I_IMG = {")
    end = html.index("};", start) + 2
    return start, end


def set_image(html: str, key: str, b64: str) -> str:
    start, end = i_img_bounds(html)
    block = html[start:end]
    pattern = re.compile(rf"{re.escape(key)}\s*:\s*\"[^\"]*\"")
    if pattern.search(block):
        block = pattern.sub(f'{key}:"{b64}"', block, count=1)
    else:
        brace = block.rfind("};")
        prefix = block[:brace].rstrip()
        block = prefix + ', ' + key + ':"' + b64 + '"' + block[brace:]
    return html[:start] + block + html[end:]


def sync_all() -> list:
    html = read_html()
    changed = []
    for p in sorted(SRC_DIR.glob("*.png")):
        key = SPECIAL_MAP.get(p.stem, p.stem)
        html = set_image(html, key, img_to_base64(p))
        changed.append(f"{p.name} -> {key}")
    write_html(html)
    return changed


def main():
    parser = argparse.ArgumentParser(description="把 PNG 素材嵌入 index.html 的 I_IMG")
    parser.add_argument("key", nargs="?", help="I_IMG 键名：boss / pm / ui / dev / be / test / ops / ref")
    parser.add_argument("image", nargs="?", help="PNG 图片路径")
    args = parser.parse_args()

    if not args.key:
        for item in sync_all():
            print("OK:", item)
        return

    if not args.image:
        print("用法: python src/convert_img.py <key> <图片.png>", file=sys.stderr)
        sys.exit(1)

    img = Path(args.image)
    if not img.exists():
        print(f"ERROR: 找不到图片 {img}", file=sys.stderr)
        sys.exit(1)

    html = set_image(read_html(), args.key, img_to_base64(img))
    write_html(html)
    print(f"OK: {args.key} <- {img}")


if __name__ == "__main__":
    main()
