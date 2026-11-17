"""
Complete fix: 
1. Copy avaturn.glb to avatar.glb (keep same URL, just replace the file)
2. Update index.html to fix mesh material names for avaturn model
3. Update blink morph names
4. Remove bone scale distortions (avaturn is already realistic female)
5. Fix the CDN fallback URL
"""
import shutil, re

PROJECT = r'C:\Users\laksh\.gemini\antigravity\scratch\rag-speech-to-isl'

# Step 1: Copy avaturn.glb -> avatar.glb (replace the old brunette)
src = PROJECT + r'\frontend\public\avaturn.glb'
dst = PROJECT + r'\frontend\public\avatar.glb'
print(f'Copying avaturn.glb -> avatar.glb ...')
shutil.copy2(src, dst)
import os
print(f'Done. Size: {os.path.getsize(dst)/1024/1024:.1f} MB')

# Step 2: Update index.html
with open(PROJECT + r'\frontend\public\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print(f'Original HTML length: {len(html)} chars, {len(html.splitlines())} lines')

# Fix 1: Update CDN fallback URL to avaturn (more realistic)
OLD_CDN = "const cdnFallbackUrl = 'https://cdn.jsdelivr.net/gh/met4citizen/TalkingHead@main/avatars/brunette.glb';"
NEW_CDN = "const cdnFallbackUrl = 'https://cdn.jsdelivr.net/gh/met4citizen/TalkingHead@1.8/avatars/avaturn.glb';"
count = html.count(OLD_CDN)
html = html.replace(OLD_CDN, NEW_CDN)
print(f'Fix1 CDN fallback: replaced {count} occurrences')

# Fix 2: Replace Wolf3D mesh styling with avaturn mesh names
OLD_MESH_BLOCK = """            // Hide glasses to match user reference image
            if (child.name === 'Wolf3D_Glasses') {
              child.visible = false;
            }

            // High-grade professional attire styling matching reference image:
            // Tailored dark navy blazer and skirt suit
            if (child.name === 'Wolf3D_Outfit_Top') {
              if (child.material) {
                child.material.color = new THREE.Color(0x192238);
                child.material.roughness = 0.82;
                child.material.metalness = 0.04;
              }
            }
            if (child.name === 'Wolf3D_Outfit_Bottom') {
              if (child.material) {
                child.material.color = new THREE.Color(0x192238);
                child.material.roughness = 0.82;
                child.material.metalness = 0.04;
              }
            }
            if (child.name === 'Wolf3D_Outfit_Footwear') {
              if (child.material) {
                child.material.color = new THREE.Color(0x101014);
                child.material.roughness = 0.35;
              }
            }
            if (child.name === 'Wolf3D_Hair') {
              if (child.material) {
                child.material.color = new THREE.Color(0x1a1512);
                child.material.roughness = 0.78;
              }
            }
            if (child.name === 'Wolf3D_Skin' || child.name === 'Wolf3D_Head' || child.name === 'Wolf3D_Body') {
              if (child.material) {
                child.material.roughness = 0.55;
                child.material.metalness = 0.01;
              }
            }"""

NEW_MESH_BLOCK = """            // Avaturn model mesh adjustments for professional female look
            // Hair: natural dark updo color
            if (child.name === 'avaturn_hair_0' || child.name === 'avaturn_hair_1') {
              if (child.material) {
                child.material.color = new THREE.Color(0x120e0c);
                child.material.roughness = 0.72;
                child.material.metalness = 0.00;
              }
            }
            // Outfit: dark navy professional blazer / look
            if (child.name === 'avaturn_look_0') {
              if (child.material) {
                child.material.color = new THREE.Color(0x1a2540);
                child.material.roughness = 0.80;
                child.material.metalness = 0.03;
              }
            }
            // Shoes: sleek black heels
            if (child.name === 'avaturn_shoes_0') {
              if (child.material) {
                child.material.color = new THREE.Color(0x0a0a0c);
                child.material.roughness = 0.28;
                child.material.metalness = 0.05;
              }
            }
            // Skin and head: natural realistic finish
            if (child.name === 'Head_Mesh' || child.name === 'Body_Mesh') {
              if (child.material) {
                child.material.roughness = 0.50;
                child.material.metalness = 0.00;
              }
            }"""

count = html.count(OLD_MESH_BLOCK)
html = html.replace(OLD_MESH_BLOCK, NEW_MESH_BLOCK)
print(f'Fix2 Mesh block: replaced {count} occurrences')

# Fix 3: Remove bone scale distortions (avaturn female is already correctly proportioned)
OLD_BONE_SCALE = """            // Feminine Proportion Refinement: slender, graceful hands, delicate wrists & forearms
            if (child.name === 'LeftHand' || child.name === 'RightHand') {
              child.scale.set(0.78, 0.84, 0.78); // Slender, petite feminine hands
            }
            if (child.name === 'LeftForeArm' || child.name === 'RightForeArm') {
              child.scale.set(0.84, 0.92, 0.84); // Smooth, slender feminine forearm
            }
            if (child.name === 'LeftArm' || child.name === 'RightArm') {
              child.scale.set(0.88, 0.96, 0.88); // Natural feminine shoulder & arm contour
            }"""

NEW_BONE_SCALE = """            // Avaturn female proportions are already natural & correct
            // No artificial bone scaling needed"""

count = html.count(OLD_BONE_SCALE)
html = html.replace(OLD_BONE_SCALE, NEW_BONE_SCALE)
print(f'Fix3 Bone scale: replaced {count} occurrences')

# Fix 4: Update blink morph - avaturn uses 'eyeBlinkLeft'/'eyeBlinkRight' AND 'eyesClosed'
# The current code already uses eyeBlinkLeft/eyeBlinkRight — avaturn has these! Good.
# But let's also add eyesClosed for smoother blink
OLD_BLINK = """      setMorph('eyeBlinkLeft', blinkWeight);
      setMorph('eyeBlinkRight', blinkWeight);"""

NEW_BLINK = """      setMorph('eyeBlinkLeft', blinkWeight);
      setMorph('eyeBlinkRight', blinkWeight);
      setMorph('eyesClosed', blinkWeight * 0.85);"""

count = html.count(OLD_BLINK)
html = html.replace(OLD_BLINK, NEW_BLINK)
print(f'Fix4 Blink morph: replaced {count} occurrences')

# Fix 5: Improve camera to show full body properly for the taller realistic avatar
# avaturn model is taller (standard ~1.7m humanoid)
OLD_CAMERA = """      camera.position.set(0, 1.35, 2.3);"""
NEW_CAMERA = """      camera.position.set(0, 1.20, 2.8);"""
count = html.count(OLD_CAMERA)
html = html.replace(OLD_CAMERA, NEW_CAMERA)
print(f'Fix5 Camera position: replaced {count} occurrences')

OLD_TARGET = """      controls.target.set(0, 1.25, 0);"""
NEW_TARGET = """      controls.target.set(0, 1.10, 0);"""
count = html.count(OLD_TARGET)
html = html.replace(OLD_TARGET, NEW_TARGET)
print(f'Fix5b Camera target: replaced {count} occurrences')

# Write back
with open(PROJECT + r'\frontend\public\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'\nDone! Updated HTML: {len(html)} chars, {len(html.splitlines())} lines')
print('avatar.glb is now the realistic Avaturn female model')
