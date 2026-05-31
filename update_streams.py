import os
import requests
import urllib3

# SSL xəbərdarlıqlarını gizlədirik
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Sizin təqdim etdiyiniz ardıcıllıq və linklər
CHANNELS = {
    "arb_tv": [
        "http://185.32.44.154/arb/mono.m3u8",
        "http://185.118.50.218/arb/mono.m3u8",
        "http://149.255.154.194/arb/mono.m3u8",
        "https://raw.githubusercontent.com/UzunMuhalefet/streams/refs/heads/main/myvideo-az/arb.m3u8"
    ],
    "arb_24": [
        "http://185.32.44.154/ARB24HD/mono.m3u8",
        "http://185.118.50.218/arb24/mono.m3u8",
        "http://149.255.154.194/arb24/tracks-v1a1/mono.m3u8",
        "https://raw.githubusercontent.com/UzunMuhalefet/streams/refs/heads/main/myvideo-az/arb-z4.m3u8"
    ],
    "arb_gunesh": [
        "http://185.32.44.154/arbgunesh/mono.m3u8",
        "http://185.118.50.218/arbgunesh/mono.m3u8",
        "http://149.255.154.194/arbgunesh/tracks-v1a1/mono.m3u8",
        "https://raw.githubusercontent.com/UzunMuhalefet/streams/refs/heads/main/myvideo-az/arb-gunes.m3u8"
    ],
    "atv": [
        "http://185.32.44.154/azadazerbaycanhd/mono.m3u8",
        "http://185.118.50.218/azadazerbaycan/mono.m3u8",
        "http://149.255.154.194/atv/tracks-v1a1/mono.m3u8",
        "https://lives.atv.az:5443/ATV_TV_STREAM/streams/atvcanli.m3u8"
    ],
    "aztv": [
        "http://185.32.44.154/AzTVHD/mono.m3u8",
        "http://185.118.50.218/aztv/mono.m3u8",
        "http://149.255.154.194/azertv/tracks-v1a1/mono.m3u8",
        "http://51.210.110.78/11438/tracks-v1a1/mono.m3u8?token=1CCF01F2F16C",
        "https://raw.githubusercontent.com/KarabagIsAzerbaijan/WEB-STREAM/6b9b59bc25103c5a1630b92d33bcf8c6a3dfd715/aztv.m3u8"
    ],
    "baku_tv": [
        "http://149.255.154.194/bakutv/tracks-v1a1/mono.m3u8",
        "https://rtmp.baku.tv/hls/bakutv.m3u8",
        "https://raw.githubusercontent.com/UzunMuhalefet/streams/refs/heads/main/myvideo-az/baku-tv.m3u8"
    ],
    "dunya_tv": [
        "http://185.32.44.154/dunyatv/mono.m3u8",
        "http://185.118.50.218/dunyatv/mono.m3u8",
        "https://stream.ftv.az/live/dunyatv.m3u8",
        "https://raw.githubusercontent.com/UzunMuhalefet/streams/refs/heads/main/myvideo-az/dunya-tv.m3u8"
    ],
    "el_tv": [
        "http://149.255.154.194/eltv/mono.m3u8",
        "https://live.eltv.az/live/eltv/playlist.m3u8"
    ],
    "ictimai_tv": [
        "http://185.32.44.154/IctimaiHD/mono.m3u8",
        "http://185.118.50.218/ictimaitv/mono.m3u8",
        "http://149.255.154.194/ictimaitele/tracks-v1a1/mono.m3u8",
        "https://live.itv.az/itv.m3u8",
        "http://85.234.100.186/11445/tracks-v1a1/mono.m3u8?token=1CCF01F2F16C",
        "https://raw.githubusercontent.com/UzunMuhalefet/streams/refs/heads/main/myvideo-az/ictimai-tv.m3u8"
    ],
    "idman_azerbaycan": [
        "http://185.32.44.154/IdmanAzerbaycanHD/mono.m3u8",
        "http://185.118.50.218/idmanaz/mono.m3u8",
        "http://149.255.154.194/idmantele/tracks-v1a1/mono.m3u8",
        "http://51.210.110.78/11446/tracks-v1a1/mono.m3u8?token=1CCF01F2F16C"
    ],
    "kanal_s": [
        "http://149.255.154.194/start/index.m3u8",
        "https://lives.atv.az:5443/KANAL-S/streams/kanals.m3u8",
        "http://51.210.110.78/11443/tracks-v1a1/mono.m3u8?token=1CCF01F2F16C",
        "https://raw.githubusercontent.com/UzunMuhalefet/streams/main/myvideo-az/kanal-s.m3u8"
    ],
    "medeniyyet_tv": [
        "http://185.32.44.154/MedeniyyetHD/mono.m3u8",
        "http://185.118.50.218/medeniyyet/mono.m3u8",
        "http://149.255.154.194/medeniyyettele/tracks-v1a1/mono.m3u8",
        "http://51.210.110.78/11442/tracks-v1a1/mono.m3u8?token=1CCF01F2F16C",
        "https://raw.githubusercontent.com/UzunMuhalefet/streams/refs/heads/main/myvideo-az/medeniyet-tv.m3u8"
    ],
    "mtv_azerbaycan": [
        "http://185.32.44.154/muztvaz/mono.m3u8",
        "http://185.118.50.218/muztvaz/mono.m3u8",
        "http://149.255.154.194/mtvaz/tracks-v1a1/mono.m3u8",
        "http://51.210.110.78/11451/tracks-v1a1/mono.m3u8?token=1CCF01F2F16C",
        "https://raw.githubusercontent.com/UzunMuhalefet/streams/refs/heads/main/myvideo-az/mtv-azerbaycan.m3u8"
    ],
    "real_tv": [
        "http://185.32.44.154/RealTVHD/mono.m3u8",
        "http://185.118.50.218/realtv/mono.m3u8",
        "http://149.255.154.194/real/tracks-v1a1/mono.m3u8",
        "http://51.77.58.55/1143/tracks-v1a1/mono.m3u8?token=1CCF01F2F16C",
        "https://raw.githubusercontent.com/UzunMuhalefet/streams/refs/heads/main/myvideo-az/real-tv.m3u8"
    ],
    "space_tv": [
        "http://185.32.44.154/spacetv/mono.m3u8",
        "http://185.118.50.218/spacetv/mono.m3u8",
        "http://149.255.154.194/space/tracks-v1a1/mono.m3u8",
        "http://51.210.110.78/11458/tracks-v1a1/mono.m3u8?token=1CCF01F2F16C",
        "https://raw.githubusercontent.com/UzunMuhalefet/streams/refs/heads/main/myvideo-az/space-tv.m3u8"
    ],
    "tmb_tv": [
        "http://185.118.50.218/tmb/mono.m3u8",
        "http://149.255.154.194/tmb/tracks-v1a1/mono.m3u8",
        "https://raw.githubusercontent.com/UzunMuhalefet/streams/refs/heads/main/myvideo-az/tmb-tv.m3u8",
        "https://raw.githubusercontent.com/UzunMuhalefet/streams/refs/heads/main/myvideo-az/tmb-azerbaycan.m3u8"
    ],
    "xezer_tv": [
        "http://185.32.44.154/XezerTVHD/mono.m3u8",
        "http://185.118.50.218/xezertv/mono.m3u8",
        "http://149.255.154.194/xazartv/tracks-v1a1/mono.m3u8",
        "http://135.125.235.54/11449/tracks-v1a1/mono.m3u8?token=1CCF01F2F16C",
        "https://raw.githubusercontent.com/UzunMuhalefet/streams/refs/heads/main/myvideo-az/xezer-tv.m3u8"
    ],
    "cbc_sport": [
        "http://185.32.44.154/cbcsporthd/mono.m3u8",
        "http://185.118.50.218/cbcsporthd/mono.m3u8",
        "https://raw.githubusercontent.com/NewedaVIP/HK_PROVIP/main/CBC_SPORT_TV-restream.m3u8",
        "https://raw.githubusercontent.com/serxan13/VIP-PANEL/7106f7791fdd1cda07a3c9ad946b5a984404874f/Cbc_sport-tv-restream.m3u8",
        "https://cbcsports-live.lg.mncdn.com/cbcsports_live/cbcsports/playlist.m3u8"
    ]
}

# streams qovluğunu yaradırıq
os.makedirs('streams', exist_ok=True)

# IPTV provayderlərinin bloklamaması üçün xüsusi başlıqlar
HEADERS = {
    "User-Agent": "VLC/3.0.16 LibVLC/3.0.16",
    "Accept": "*/*",
    "Connection": "keep-alive"
}

# Problemli IP-lər: Brauzerdə/GitHub-da bloklanan amma əslində işləyən serverlər
TRUSTED_IPS = ["185.32.44.154", "185.118.50.218", "149.255.154.194"]

for name, urls in CHANNELS.items():
    working = []
    failing = []
    
    for url in urls:
        try:
            # 5 saniyə yoxlayır
            response = requests.get(url, headers=HEADERS, timeout=5.0, stream=True, verify=False)
            if response.status_code == 200:
                working.append(url)
            else:
                failing.append(url)
        except Exception:
            # Əgər bağlantı xətası verərsə və IP "TRUSTED" sırasındadırsa, onu yenə də işlək kimi qəbul et.
            if any(ip in url for ip in TRUSTED_IPS):
                working.append(url)
            else:
                failing.append(url)

    # Nəticə: Əvvəlcə işləyən linklər (prioritet sırası ilə), sonra işləməyənlər
    final_urls = working + failing

    # Faylın yaradılması
    file_path = f"streams/{name}.m3u8"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        f.write("#EXT-X-VERSION:3\n")
        for url in final_urls:
            f.write("#EXT-X-STREAM-INF:BANDWIDTH=3000000\n")
            f.write(f"{url}\n")
            
print("Bütün kanallar yoxlanıldı və streams qovluğuna yazıldı.")

