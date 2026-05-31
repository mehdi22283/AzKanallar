import os
import requests
import re

# Kanallar və onların linkləri (Prioritet sırası ilə)
CHANNELS = {
    "ARB_TV": [
        "http://185.32.44.154/arb/mono.m3u8",
        "http://185.118.50.218/arb/mono.m3u8",
        "http://149.255.154.194/arb/mono.m3u8",
        "https://raw.githubusercontent.com/UzunMuhalefet/streams/refs/heads/main/myvideo-az/arb.m3u8"
    ],
    "ARB_24": [
        "http://185.32.44.154/ARB24HD/mono.m3u8",
        "http://185.118.50.218/arb24/mono.m3u8",
        "http://149.255.154.194/arb24/tracks-v1a1/mono.m3u8",
        "https://raw.githubusercontent.com/UzunMuhalefet/streams/refs/heads/main/myvideo-az/arb-z4.m3u8"
    ],
    "ARB_Gunesh": [
        "http://185.32.44.154/arbgunesh/mono.m3u8",
        "http://185.118.50.218/arbgunesh/mono.m3u8",
        "http://149.255.154.194/arbgunesh/tracks-v1a1/mono.m3u8",
        "https://raw.githubusercontent.com/UzunMuhalefet/streams/refs/heads/main/myvideo-az/arb-gunes.m3u8"
    ],
    "ATV": [
        "http://185.32.44.154/azadazerbaycanhd/mono.m3u8",
        "http://185.118.50.218/azadazerbaycan/mono.m3u8",
        "http://149.255.154.194/atv/tracks-v1a1/mono.m3u8",
        "https://lives.atv.az:5443/ATV_TV_STREAM/streams/atvcanli.m3u8"
    ],
    "AzTV": [
        "http://185.32.44.154/AzTVHD/mono.m3u8",
        "http://185.118.50.218/aztv/mono.m3u8",
        "http://149.255.154.194/azertv/tracks-v1a1/mono.m3u8",
        "https://raw.githubusercontent.com/KarabagIsAzerbaijan/WEB-STREAM/6b9b59bc25103c5a1630b92d33bcf8c6a3dfd715/aztv.m3u8"
    ],
    "Baku_TV": [
        "http://149.255.154.194/bakutv/tracks-v1a1/mono.m3u8",
        "https://rtmp.baku.tv/hls/bakutv.m3u8",
        "https://raw.githubusercontent.com/UzunMuhalefet/streams/refs/heads/main/myvideo-az/baku-tv.m3u8"
    ],
    "Dunya_TV": [
        "http://185.32.44.154/dunyatv/mono.m3u8",
        "http://185.118.50.218/dunyatv/mono.m3u8",
        "https://stream.ftv.az/live/dunyatv.m3u8",
        "https://raw.githubusercontent.com/UzunMuhalefet/streams/refs/heads/main/myvideo-az/dunya-tv.m3u8"
    ],
    "El_TV": [
        "http://149.255.154.194/eltv/mono.m3u8",
        "https://live.eltv.az/live/eltv/playlist.m3u8"
    ],
    "Ictimai_TV": [
        "http://185.32.44.154/IctimaiHD/mono.m3u8",
        "http://185.118.50.218/ictimaitv/mono.m3u8",
        "http://149.255.154.194/ictimaitele/tracks-v1a1/mono.m3u8",
        "https://live.itv.az/itv.m3u8",
        "https://raw.githubusercontent.com/UzunMuhalefet/streams/refs/heads/main/myvideo-az/ictimai-tv.m3u8"
    ],
    "Idman_Azerbaycan": [
        "http://185.32.44.154/IdmanAzerbaycanHD/mono.m3u8",
        "http://185.118.50.218/idmanaz/mono.m3u8",
        "http://149.255.154.194/idmantele/tracks-v1a1/mono.m3u8"
    ],
    "Kanal_S": [
        "http://149.255.154.194/start/index.m3u8",
        "https://lives.atv.az:5443/KANAL-S/streams/kanals.m3u8",
        "https://raw.githubusercontent.com/UzunMuhalefet/streams/main/myvideo-az/kanal-s.m3u8"
    ],
    "Medeniyyet_TV": [
        "http://185.32.44.154/MedeniyyetHD/mono.m3u8",
        "http://185.118.50.218/medeniyyet/mono.m3u8",
        "http://149.255.154.194/medeniyyettele/tracks-v1a1/mono.m3u8",
        "https://raw.githubusercontent.com/UzunMuhalefet/streams/refs/heads/main/myvideo-az/medeniyet-tv.m3u8"
    ],
    "MTV_Azerbaycan": [
        "http://185.32.44.154/muztvaz/mono.m3u8",
        "http://185.118.50.218/muztvaz/mono.m3u8",
        "http://149.255.154.194/mtvaz/tracks-v1a1/mono.m3u8",
        "https://raw.githubusercontent.com/UzunMuhalefet/streams/refs/heads/main/myvideo-az/mtv-azerbaycan.m3u8"
    ],
    "Real_TV": [
        "http://185.32.44.154/RealTVHD/mono.m3u8",
        "http://185.118.50.218/realtv/mono.m3u8",
        "http://149.255.154.194/real/tracks-v1a1/mono.m3u8",
        "https://raw.githubusercontent.com/UzunMuhalefet/streams/refs/heads/main/myvideo-az/real-tv.m3u8"
    ],
    "Space_TV": [
        "http://185.32.44.154/spacetv/mono.m3u8",
        "http://185.118.50.218/spacetv/mono.m3u8",
        "http://149.255.154.194/space/tracks-v1a1/mono.m3u8",
        "https://raw.githubusercontent.com/UzunMuhalefet/streams/refs/heads/main/myvideo-az/space-tv.m3u8"
    ],
    "TMB": [
        "http://185.118.50.218/tmb/mono.m3u8",
        "http://149.255.154.194/tmb/tracks-v1a1/mono.m3u8",
        "https://raw.githubusercontent.com/UzunMuhalefet/streams/refs/heads/main/myvideo-az/tmb-tv.m3u8",
        "https://raw.githubusercontent.com/UzunMuhalefet/streams/refs/heads/main/myvideo-az/tmb-azerbaycan.m3u8"
    ],
    "Xezer_TV": [
        "http://185.32.44.154/XezerTVHD/mono.m3u8",
        "http://185.118.50.218/xezertv/mono.m3u8",
        "http://149.255.154.194/xazartv/tracks-v1a1/mono.m3u8",
        "http://135.125.235.54/11449/tracks-v1a1/mono.m3u8?token=1CCF01F2F16C",
        "https://raw.githubusercontent.com/UzunMuhalefet/streams/refs/heads/main/myvideo-az/xezer-tv.m3u8"
    ],
    "CBC_Sport": [
        "http://185.32.44.154/cbcsporthd/mono.m3u8",
        "http://185.118.50.218/cbcsporthd/mono.m3u8",
        "https://raw.githubusercontent.com/NewedaVIP/HK_PROVIP/main/CBC_SPORT_TV-restream.m3u8",
        "https://raw.githubusercontent.com/serxan13/VIP-PANEL/7106f7791fdd1cda07a3c9ad946b5a984404874f/Cbc_sport-tv-restream.m3u8",
        "https://cbcsports-live.lg.mncdn.com/cbcsports_live/cbcsports/playlist.m3u8"
    ]
}

# Brauzer bloklamasının qarşısını almaq üçün VLC/IPTV Player User-Agent başlığı
HEADERS = {
    "User-Agent": "VLC/3.0.18 LibVLC/3.0.18",
    "Accept": "*/*"
}

def check_link(url):
    """Linkin aktivliyini və daxilindəki bandwidth (keyfiyyət) dəyərini yoxlayır."""
    try:
        # İPTV pleyer kimi sorğu göndəririk (Həmçinin çox gözləməmək üçün 5 saniyə vaxt qoyuruq)
        response = requests.get(url, headers=HEADERS, timeout=5, verify=False)
        if response.status_code == 200:
            content = response.text
            # m3u8 daxilində BANDWIDTH dəyərini axtarırıq (Məsələn: BANDWIDTH=3000000)
            bandwidth_match = re.search(r"BANDWIDTH=(\d+)", content, re.IGNORECASE)
            if bandwidth_match:
                return True, int(bandwidth_match.group(1))
            return True, 0  # Əgər bandwidth tapılmasa amma link işləsə, 0 qayıdır
    except Exception:
        pass
    return False, -1

def process_channels():
    # Çıxış qovluğunu yaradırıq
    output_dir = "streams"
    os.makedirs(output_dir, exist_ok=True)

    for channel_name, urls in CHANNELS.items():
        alive_links = []
        dead_links = []

        for index, url in enumerate(urls):
            is_alive, bandwidth = check_link(url)
            
            # Link məlumatını saxlayırıq (orijinal sıra nömrəsi prioritet üçün lazımdır)
            link_info = {
                "url": url,
                "bandwidth": bandwidth,
                "original_index": index
            }

            if is_alive:
                alive_links.append(link_info)
            else:
                dead_links.append(link_info)

        # Sıralama qaydası: 
        # 1. Öncə ən yüksək BANDWIDTH (keyfiyyət) olanlar gəlsin.
        # 2. Keyfiyyət eynidirsə, sizin ilkin yazdığınız prioritet sırasına (original_index) baxsın.
        alive_links.sort(key=lambda x: (-x["bandwidth"], x["original_index"]))

        # İşlək linklər başda, ölü (ehtiyat) linklər isə aşağıda ardıcıllıqla düzülür
        final_sorted_urls = [item["url"] for item in alive_links] + [item["url"] for item in dead_links]

        # M3U8 faylının məzmununu formalaşdırırıq
        file_content = "#EXTM3U\n#EXT-X-VERSION:3\n"
        for url in final_sorted_urls:
            file_content += "#EXT-X-STREAM-INF:BANDWIDTH=3000000\n"
            file_content += f"{url}\n"

        # Faylı streams qovluğuna yazırıq (Məsələn: streams/ARB_TV.m3u8)
        file_path = os.path.join(output_dir, f"{channel_name}.m3u8")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(file_content)
        
        print(f"[UĞURLU] {channel_name}.m3u8 yeniləndi. Aktiv link sayı: {len(alive_links)}")

if __name__ == "__main__":
    # SSL xəbərdarlıqlarını gizlətmək üçün (Bəzi köhnə dövlət tv serverləri üçün)
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    process_channels()
