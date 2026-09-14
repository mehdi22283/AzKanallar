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
print(f"HTML ölçüsü: {len(html)} simvol")


# const videoSrc = "URL"
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
    print("XƏTA: const videoSrc tapılmadı.")

    # Debug üçün videoSrc olan sətirləri göstər
    for line in html.splitlines():
        if "videoSrc" in line:
            print("TAPILAN SƏTİR:")
            print(line[:1000])

    raise SystemExit(1)


print("videoSrc tapıldı:")
print(video_src)


if not video_src.startswith(("http://", "https://")):
    raise RuntimeError(
        "videoSrc HTTP/HTTPS URL deyil."
    )


m3u_content = f"""#EXTM3U
#EXTINF:-1,Euro Star
{video_src}
"""


Path(OUTPUT_FILE).write_text(
    m3u_content,
    encoding="utf-8"
)

print()
print("================================")
print("M3U8 uğurla yaradıldı!")
print("================================")
print(f"Fayl: {OUTPUT_FILE}")
