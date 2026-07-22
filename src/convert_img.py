
import base64
import re
from pathlib import Path

# 项目根目录
ROOT = Path(__file__).parent.parent
HTML_PATH = ROOT / "index.html"
SRC_DIR = ROOT / "src"


def img_to_base64(img_path: Path) -> str:
    """将图片转换为 base64 字符串"""
    with open(img_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode("ascii")
        return f"data:image/png;base64,{b64}"


def update_html_img(html_path: Path, key: str, img_path: Path):
    """更新 HTML 中的 I_IMG 图片"""
    b64_data = img_to_base64(img_path)

    html = html_path.read_text(encoding="utf-8")

    # 匹配 I_IMG 中的 key: "..."
    # 模式：捕获 key: "value"，替换 value
    # 首先检查 key 是否存在
    pattern_exists = re.compile(rf'{key}\s*:\s*"[^"]*"')
    match = pattern_exists.search(html)

    if match:
        # key 已存在，替换
        new_html = pattern_exists.sub(f'{key}:"{b64_data}"', html)
    else:
        # key 不存在，在 dev 后面插入
        # 先找到 dev:"..."
        dev_pattern = re.compile(r'(dev\s*:\s*"[^"]+")')
        new_html = dev_pattern.sub(rf'\1, {key}:"{b64_data}"', html)

    html_path.write_text(new_html, encoding="utf-8")
    print(f"OK: updated {key} to {img_path.name}")


def main():
    # 更新后端立绘为 be.png
    be_img = SRC_DIR / "be.png"
    if be_img.exists():
        update_html_img(HTML_PATH, "be", be_img)
    else:
        print(f"WARN: cannot find {be_img}")

    # 把 test.png 也加上（可选，如果需要的话）
    test_img = SRC_DIR / "test.png"
    if test_img.exists():
        update_html_img(HTML_PATH, "test", test_img)
        print(f"OK: added test.png to I_IMG.test")


if __name__ == "__main__":
    main()
