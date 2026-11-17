import urllib.request, ssl, struct, json, os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Download avaturn.glb (more realistic)
url = 'https://cdn.jsdelivr.net/gh/met4citizen/TalkingHead@1.8/avatars/avaturn.glb'
out = r'C:\Users\laksh\.gemini\antigravity\scratch\rag-speech-to-isl\frontend\public\avaturn.glb'

print(f'Downloading avaturn.glb...')
try:
    urllib.request.urlretrieve(url, out)
    size = os.path.getsize(out)
    print(f'Downloaded: {size} bytes = {size/1024/1024:.1f} MB')
    
    # Inspect the GLB
    with open(out, 'rb') as f:
        magic = f.read(4)
        version = struct.unpack('<I', f.read(4))[0]
        length = struct.unpack('<I', f.read(4))[0]
        chunk0_len = struct.unpack('<I', f.read(4))[0]
        chunk0_type = f.read(4)
        json_data = f.read(chunk0_len)
    
    gltf = json.loads(json_data)
    print('GLB version:', version)
    print('Meshes:', len(gltf.get('meshes', [])))
    mesh_names = [m.get('name','?') for m in gltf.get('meshes',[])]
    print('Mesh names:', mesh_names)
    
    # Check morph targets / blendshapes
    for i, m in enumerate(gltf.get('meshes', [])):
        for prim in m.get('primitives', []):
            targets = prim.get('targets', [])
            if targets:
                extras = m.get('extras', {})
                target_names = extras.get('targetNames', [])
                print(f'  Mesh {m.get("name","?")}: {len(targets)} morph targets')
                if target_names:
                    print(f'    Sample names: {target_names[:10]}')
                break
    
    # Check bones
    nodes = gltf.get('nodes', [])
    bone_names = [n.get('name','?') for n in nodes if 'skin' not in str(n)]
    print('Total nodes:', len(nodes))
    finger_bones = [b for b in bone_names if 'Hand' in b or 'Finger' in b or 'Index' in b or 'Thumb' in b]
    print('Hand/finger bones:', finger_bones[:20])
    
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
