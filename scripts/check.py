import os
import requests
import subprocess

# Kanallar və onların linkləri
channels = {
    "ARB": ["http://185.32.44.154/arb/mono.m3u8", "http://185.118.50.218/arb/mono.m3u8", "http://149.255.154.194/arb/mono.m3u8", "https://raw.githubusercontent.com/UzunMuhalefet/streams/refs/heads/main/myvideo-az/arb.m3u8"],
    # Digər kanalları da eyni qayda ilə bura əlavə edin
}

def is_link_alive(url):
    try:
        # IPTV pleyeri kimi davranmaq üçün User-Agent əlavə edirik
        cmd = ["curl", "-I", "-L", "--max-time", "10", "-H", "User-Agent: VLC/3.0.16", url]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return "200" in result.stdout or "302" in result.stdout
    except:
        return False

for name, urls in channels.items():
    working_links = []
    dead_links = []
    
    for url in urls:
        if is_link_alive(url):
            working_links.append(url)
        else:
            dead_links.append(url)
            
    # Siyahını yenilə: İşləyənlər başda
    final_list = working_links + dead_links
    
    with open(f"streams/{name}.m3u8", "w") as f:
        f.write("#EXTM3U\n#EXT-X-VERSION:3\n")
        for link in final_list:
            f.write(f"#EXT-X-STREAM-INF:BANDWIDTH=3000000\n{link}\n")
            
