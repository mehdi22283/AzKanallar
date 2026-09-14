import re
import urllib.request
from pathlib import Path

SOURCE_URL = "https://www.parsatv.com/m/name=Euro-Star"
OUTPUT_FILE = "euro-star.m3u8"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Linux; Android 10; K) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/140.0 Mobile Safari/537.36"
    )
}

request = urllib.request.Request(
    SOURCE_URL,
    headers=headers
)

print("Sayt yüklənir...")

with urllib.request.urlopen(request, timeout=30) as response:
    html = response.read().decode("utf-8", errors="ignore")

print("HTML alındı.")


patterns = [
    r'const\s+videoSrc\s*=\s*["\']([^"\']+)["\']',
    r'let\s+videoSrc\s*=\s*["\']([^"\']+)["\']',
    r'var\s+videoSrc\s*=\s*["\']([^"\']+)["\']',
]

video_src = None

for pattern in patterns:
    match = re.search(pattern, html, re.IGNORECASE)

    if match:
        video_src = match.group(1).strip()
        break


if not video_src:
    print("XƏTA: videoSrc tapılmadı.")

    for line in html.splitlines():
        if "videoSrc" in line:
            print(line[:1000])

    raise SystemExit(1)


print("videoSrc tapıldı:")
print(video_src)


if not video_src.startswith(("http://", "https://")):
    raise RuntimeError("videoSrc düzgün URL deyil.")


# İstənilən M3U8 formatı
m3u_content = f"""#EXTM3U
#EXTVLCOPT:http-user-agent=WINK/1.28.2 (AndroidTV/9) HlsWinkPlayer
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:BANDWIDTH=2096000
{video_src}
"""


Path(OUTPUT_FILE).write_text(
    m3u_content,
    encoding="utf-8"
)

print()
print("M3U8 uğurla yaradıldı:")
print(OUTPUT_FILE)
