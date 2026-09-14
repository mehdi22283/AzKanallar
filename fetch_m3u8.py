#!/usr/bin/env python3
"""
ATV Avrupa canli yayin sehifesindeki .m3u8 linkini tapib
atvavrupa.m3u8 faylina yazir.

Iki metod sinanilir:
  1) STATIK metod: sehifenin HTML/JS kodunu birbasa yuklayib icindeki
     .m3u8 linkini regex ile axtarir (suretli, brauzer teleb etmir).
  2) DINAMIK metod (fallback): Playwright ile hemin sehifeni hexiqi
     brauzerde acir ve sebeke (network) sorgularini izleyerek
     .m3u8 linkini tutur. Bu, oyun (player) JavaScript ile
     yuklendiyi ve statik metod ise yaramadigi hallar ucundur.

Istifade:
    python fetch_m3u8.py

Chixish faylı:
    atvavrupa.m3u8
"""

import re
import sys
import time
import urllib.request

PAGE_URL = "https://www.atvavrupa.tv/canli-yayin"
OUTPUT_FILE = "atvavrupa.m3u8"
CHANNEL_NAME = "ATV Avrupa"

# Bu siteler cox zaman Referer/Origin yoxlayir, ona gore normal
# brauzer kimi gorunmek ucun basliqlar elave edirik.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Referer": PAGE_URL,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

# Sehifenin HTML/JS kodunda .m3u8 linkini axtaran ana pattern.
M3U8_REGEX = re.compile(r"https?://[^\s\"'\\]+\.m3u8[^\s\"'\\]*")

# Player konfiqurasiyasi cox zaman iframe icinde olur, bu yuzden
# olasi iframe/embed linklerini de axtaririq.
IFRAME_REGEX = re.compile(
    r'<iframe[^>]+src=["\']([^"\']+)["\']', re.IGNORECASE
)


def fetch_url(url: str, timeout: int = 15) -> str:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def find_m3u8_in_text(html: str):
    matches = M3U8_REGEX.findall(html)
    # Bezen sonunda artiq HTML/JS simvollari qalir, temizleyek
    cleaned = []
    for m in matches:
        m = m.rstrip(');",')
        cleaned.append(m)
    return cleaned


def try_static_method() -> str | None:
    """1-ci metod: sadece HTTP GET + regex."""
    try:
        html = fetch_url(PAGE_URL)
    except Exception as e:
        print(f"[static] Ana sehife yuklenmedi: {e}", file=sys.stderr)
        return None

    found = find_m3u8_in_text(html)
    if found:
        print(f"[static] Ana sehifede tapildi: {found[0]}")
        return found[0]

    # Ana sehifede tapilmadisa, iframe-leri yoxla
    for iframe_src in IFRAME_REGEX.findall(html):
        if iframe_src.startswith("//"):
            iframe_src = "https:" + iframe_src
        elif iframe_src.startswith("/"):
            iframe_src = "https://www.atvavrupa.tv" + iframe_src
        try:
            iframe_html = fetch_url(iframe_src)
        except Exception as e:
            print(f"[static] Iframe yuklenmedi ({iframe_src}): {e}", file=sys.stderr)
            continue
        found = find_m3u8_in_text(iframe_html)
        if found:
            print(f"[static] Iframe icinde tapildi ({iframe_src}): {found[0]}")
            return found[0]

    return None


def try_dynamic_method() -> str | None:
    """
    2-ci metod (fallback): Playwright ile hexiqi brauzer acib
    network sorgularinda .m3u8 axtarir. Statik metod is vermediyi
    halda avtomatik cagirilir.

    Bunun ucun once bu paketleri qurmaq lazimdir:
        pip install playwright
        playwright install chromium
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "[dynamic] Playwright qurulu deyil, dinamik metod atlanildi. "
            "'pip install playwright && playwright install chromium' ile qura bilersiniz.",
            file=sys.stderr,
        )
        return None

    found_url = {"value": None}

    def handle_request(request):
        if ".m3u8" in request.url and found_url["value"] is None:
            found_url["value"] = request.url

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent=HEADERS["User-Agent"])
            page = context.new_page()
            page.on("request", handle_request)
            page.goto(PAGE_URL, wait_until="networkidle", timeout=30000)
            # Video oynadiciya birbasa cixmaq ucun bir az gozleyek,
            # bezi playerler avtomatik play olmur.
            page.wait_for_timeout(5000)
            browser.close()
    except Exception as e:
        print(f"[dynamic] Playwright xetasi: {e}", file=sys.stderr)
        return None

    if found_url["value"]:
        print(f"[dynamic] Sebeke sorgusunda tapildi: {found_url['value']}")
    return found_url["value"]


def write_m3u8(stream_url: str, path: str = OUTPUT_FILE) -> None:
    content = (
        "#EXTM3U\n"
        f'#EXTINF:-1 tvg-name="{CHANNEL_NAME}" group-title="Live",{CHANNEL_NAME}\n'
        f"{stream_url}\n"
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Yazildi -> {path}")


def main() -> int:
    stream_url = try_static_method()

    if not stream_url:
        print("[info] Statik metod is vermedi, dinamik metod (Playwright) sinanilir...")
        stream_url = try_dynamic_method()

    if not stream_url:
        print(
            "XETA: .m3u8 linki tapilmadi. Brauzerde F12 -> Network -> 'm3u8' "
            "filtri ile hexiqi linki tapib bu skriptdeki M3U8_REGEX-i "
            "veya iframe menbeyini dogrulayin.",
            file=sys.stderr,
        )
        return 1

    write_m3u8(stream_url)
    return 0


if __name__ == "__main__":
    sys.exit(main())
