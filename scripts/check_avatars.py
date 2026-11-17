import urllib.request, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = [
    'https://cdn.jsdelivr.net/gh/met4citizen/TalkingHead@1.8/avatars/avaturn.glb',
    'https://cdn.jsdelivr.net/gh/met4citizen/TalkingHead@main/avatars/avaturn.glb',
    'https://cdn.jsdelivr.net/gh/met4citizen/TalkingHead@1.3/avatars/brunette.glb',
    'https://cdn.jsdelivr.net/gh/met4citizen/TalkingHead@main/avatars/brunette.glb',
]
for url in urls:
    try:
        req = urllib.request.Request(url, method='HEAD')
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            size = resp.headers.get('content-length', '?')
            print(f'OK {resp.status} size={size} {url}')
    except Exception as e:
        print(f'ERR {url}: {e}')
