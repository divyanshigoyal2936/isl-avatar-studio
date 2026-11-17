import struct, json

out = r'C:\Users\laksh\.gemini\antigravity\scratch\rag-speech-to-isl\frontend\public\avaturn.glb'

with open(out, 'rb') as f:
    f.read(4)  # magic
    f.read(4)  # version
    f.read(4)  # length
    chunk0_len = struct.unpack('<I', f.read(4))[0]
    f.read(4)  # type
    json_data = f.read(chunk0_len)

gltf = json.loads(json_data)
nodes = gltf.get('nodes', [])
node_names = [n.get('name','?') for n in nodes]
print('ALL NODES:')
for name in node_names:
    print(' ', name)

print('\n\nALL MORPH TARGET NAMES:')
for m in gltf.get('meshes', []):
    extras = m.get('extras', {})
    target_names = extras.get('targetNames', [])
    if target_names:
        print(f'\n  [{m.get("name","?")}]:')
        for tn in target_names:
            print(f'    {tn}')
