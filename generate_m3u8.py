import re
import requests
from pathlib import Path

SOURCE_URL = "https://www.parsatv.com/m/name=Euro-Star"
OUTPUT_FILE = "euro-star.m3u8"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Linux; Android 10; K) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/140.0 Mobile Safari/537.36"
    )
}


def extract_video_src(html):
    # const videoSrc = "https://....m3u8";
    patterns = [
        r'const\s+videoSrc\s*=\s*["\']([^"\']+)["\']',
        r'let\s+videoSrc\s*=\s*["\']([^"\']+)["\']',
        r'var\s+videoSrc\s*=\s*["\']([^"\']+)["\']',
    ]

    for pattern in patterns:
        match = re.search(pattern, html, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return None


def main():
    print(f"Downloading: {SOURCE_URL}")

    response = requests.get(
        SOURCE_URL,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    html = response.text

    video_src = extract_video_src(html)

    if not video_src:
        raise RuntimeError(
            "HTML source daxilində const videoSrc tapılmadı."
        )

    print("Found videoSrc:")
    print(video_src)

    if not video_src.startswith(("http://", "https://")):
        raise RuntimeError(
            f"Tapılan videoSrc düzgün URL deyil: {video_src}"
        )

    content = f"""#EXTM3U
#EXTINF:-1,Euro Star
{video_src}
"""

    Path(OUTPUT_FILE).write_text(
        content,
        encoding="utf-8"
    )

    print(f"Created: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
