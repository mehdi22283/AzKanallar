import os
import requests

# VLC User-Agent brauzer kimi görünməmək və iptv linklərini düzgün yoxlamaq üçün
HEADERS = {
    'User-Agent': 'VLC/3.0.18 LibVLC/3.0.18'
}

# Sənin verdiyin kanallar və prioritet sırası ilə linklər
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
    "TMB_TV": [
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

def is_live(url):
    """Linkin aktiv olub-olmadığını yoxlayır (VLC headers ilə)"""
    try:
        # GET əvəzinə HEAD sorğusu göndəririk ki, vaxt aparmasın və trafiki yükləməsin
        response = requests.head(url, headers=HEADERS, timeout=5, allow_redirects=True)
        if response.status_code == 200:
            return True
        # Bəzi serverlər HEAD sorğusunu dəstəkləmir, ona görə GET ilə təkrar yoxlayırıq
        response = requests.get(url, headers=HEADERS, timeout=5, stream=True)
        return response.status_code == 200
    except Exception:
        return False

# Çıxış qovluğunu yarat
os.makedirs("streams", exist_ok=True)

for channel_name, urls in CHANNELS.items():
    working_urls = []
    dead_urls = []
    
    # Sıra ilə linkləri yoxla (Sənin yazdığın prioritet ardıcıllıq qorunur)
    for url in urls:
        if is_live(url):
            working_urls.append(url)
        else:
            dead_urls.append(url)
            
    # Hər iki halda linkləri birləşdir (Öncə işləklər, sonra digərləri)
    final_list = working_urls + dead_urls
    
    # Əgər heç bir link işləmirsə, köhnə prioritet siyahısını qoru (bütünlük üçün)
    if not final_list:
        final_list = urls

    # Faylın məzmununu sənin istədiyin kimi formatla
    m3u8_content = "#EXTM3U\n#EXT-X-VERSION:3\n#EXT-X-STREAM-INF:BANDWIDTH=3000000\n"
    m3u8_content += "\n".join(final_list) + "\n"
    
    # Faylı streams qovluğunda kanal adına uyğun m3u8 olaraq yadda saxla
    file_path = f"streams/{channel_name}.m3u8"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(m3u8_content)
        
    print(f"{channel_name}.m3u8 yeniləndi. Aktiv link sayı: {len(working_urls)}")
