import re

with open(r'C:\Users\laksh\.gemini\antigravity\scratch\rag-speech-to-isl\frontend\public\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Enhance lighting setup in initThreeJS
old_lighting = """      // Studio Lighting for Real Human Skin & Hands
      const ambientLight = new THREE.AmbientLight(0xffffff, 0.65);
      scene.add(ambientLight);

      const keyLight = new THREE.DirectionalLight(0xfffaed, 0.95);
      keyLight.position.set(1.8, 2.5, 2.2);
      keyLight.castShadow = true;
      scene.add(keyLight);

      const fillLight = new THREE.DirectionalLight(0x90b4d4, 0.55);
      fillLight.position.set(-2.0, 1.8, 1.5);
      scene.add(fillLight);

      const rimLight = new THREE.DirectionalLight(0xffd29d, 0.6);
      rimLight.position.set(0, 2.8, -2.0);
      scene.add(rimLight);"""

new_lighting = """      // Studio Warm Cinematic 3-Point Lighting for Human Skin & Professional Attire
      const ambientLight = new THREE.AmbientLight(0xfff7ed, 0.72);
      scene.add(ambientLight);

      const keyLight = new THREE.DirectionalLight(0xfff5ea, 1.15);
      keyLight.position.set(1.6, 2.8, 2.2);
      keyLight.castShadow = true;
      scene.add(keyLight);

      const fillLight = new THREE.DirectionalLight(0xc7d2fe, 0.65);
      fillLight.position.set(-2.2, 1.9, 1.8);
      scene.add(fillLight);

      const rimLight = new THREE.DirectionalLight(0xfde68a, 0.75);
      rimLight.position.set(0, 2.9, -1.8);
      scene.add(rimLight);

      // Subtle under-chin bounce light to soften neck shadows
      const bounceLight = new THREE.DirectionalLight(0xffedd5, 0.35);
      bounceLight.position.set(0, 0.4, 1.5);
      scene.add(bounceLight);"""

if old_lighting in html:
    html = html.replace(old_lighting, new_lighting)
    print("Upgraded lighting to studio warm cinematic setup.")
else:
    print("Warning: old_lighting not found exactly, check regex.")

# 2. Enhance materials & head/hair/face construction
# Find from 'function buildHumanoidAvatar() {' down to 'function createArm(isLeft) {'
old_build_avatar_head = """    function buildHumanoidAvatar() {
      const avatarRoot = new THREE.Group();
      scene.add(avatarRoot);
      avatarRig.root = avatarRoot;

      // Realistic warm human skin tones (Cute female appearance)
      const skinColor = 0xdba178; // Warm soft Indian complexion
      const skinMat = new THREE.MeshStandardMaterial({
        color: skinColor,
        roughness: 0.58,
        metalness: 0.02
      });
      avatarRig.skinMat = skinMat;

      // Soft Blush / Lip shade
      const lipMat = new THREE.MeshStandardMaterial({
        color: 0xba5f58,
        roughness: 0.45,
        metalness: 0.0
      });

      // Elegant feminine attire (Chic pastel slate blazer & clean inner top)
      const outfitMat = new THREE.MeshStandardMaterial({
        color: 0x222a3d, // Deep indigo blazer
        roughness: 0.70,
        metalness: 0.08
      });

      const topMat = new THREE.MeshStandardMaterial({
        color: 0xf3f4f8, // Soft ivory inner top
        roughness: 0.60,
        metalness: 0.02
      });

      const accentMat = new THREE.MeshStandardMaterial({
        color: 0x1e293b,
        roughness: 0.70,
        metalness: 0.05
      });

      const hairMat = new THREE.MeshStandardMaterial({
        color: 0x16110e, // Rich dark brunette hair
        roughness: 0.82,
        metalness: 0.05
      });

      const eyeIrisMat = new THREE.MeshBasicMaterial({ color: 0x28180e });
      const scleraMat = new THREE.MeshBasicMaterial({ color: 0xfafafa });
      const browMat = new THREE.MeshStandardMaterial({ color: 0x16110e, roughness: 0.9 });"""

new_build_avatar_head = """    function buildHumanoidAvatar() {
      const avatarRoot = new THREE.Group();
      scene.add(avatarRoot);
      avatarRig.root = avatarRoot;

      // Realistic warm human skin tone (Rich warm Indian olive complexion)
      const skinColor = 0xce8f68; 
      const skinMat = new THREE.MeshStandardMaterial({
        color: skinColor,
        roughness: 0.62,
        metalness: 0.01
      });
      avatarRig.skinMat = skinMat;

      // Natural soft rose-terracotta lip tint
      const lipMat = new THREE.MeshStandardMaterial({
        color: 0xb55a52,
        roughness: 0.38,
        metalness: 0.02
      });

      // Professional Tailored Attire (Rich Navy Formal Blazer & Silk Collared Inner)
      const outfitMat = new THREE.MeshStandardMaterial({
        color: 0x1c2438, // Crisp Midnight Navy Formal Blazer
        roughness: 0.68,
        metalness: 0.06
      });

      const lapelMat = new THREE.MeshStandardMaterial({
        color: 0x141b2a, // Subtle darker navy peak lapel contrast
        roughness: 0.62,
        metalness: 0.08
      });

      const topMat = new THREE.MeshStandardMaterial({
        color: 0xf8fafc, // Pristine silk ivory inner top
        roughness: 0.55,
        metalness: 0.02
      });

      const collarMat = new THREE.MeshStandardMaterial({
        color: 0xeff2f7, // Sharp crisp collar
        roughness: 0.50,
        metalness: 0.02
      });

      const goldMat = new THREE.MeshStandardMaterial({
        color: 0xd4af37, // Elegant subtle warm gold blazer button & stud
        roughness: 0.30,
        metalness: 0.70
      });

      // Lustrous Natural Dark Hair with Silky Specular Highlights
      const hairMat = new THREE.MeshStandardMaterial({
        color: 0x1a1412, // Deep espresso / warm black
        roughness: 0.65,
        metalness: 0.08
      });

      const hairHighlightMat = new THREE.MeshStandardMaterial({
        color: 0x2e221d, // Soft natural hair highlight
        roughness: 0.58,
        metalness: 0.10
      });

      const eyeIrisMat = new THREE.MeshBasicMaterial({ color: 0x2b170c }); // Rich deep brown iris
      const scleraMat = new THREE.MeshBasicMaterial({ color: 0xfdfdfd });
      const browMat = new THREE.MeshStandardMaterial({ color: 0x17120f, roughness: 0.85 });"""

if old_build_avatar_head in html:
    html = html.replace(old_build_avatar_head, new_build_avatar_head)
    print("Upgraded materials to professional tailored look.")
else:
    print("Warning: old_build_avatar_head not found, checking...")

# 3. Upgrade Torso & Collar / Lapel
old_torso = """      // Upper Bust & Chest
      const bust = new THREE.Mesh(new THREE.CylinderGeometry(0.19, 0.15, 0.28, 24), outfitMat);
      bust.position.y = 0.35;
      spine.add(bust);

      // White inner top insert
      const topInsert = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.08, 0.16, 16), topMat);
      topInsert.position.set(0, 0.41, 0.085);
      spine.add(topInsert);

      // Natural subtle fabric button on blouse
      const button = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 0.004, 16), outfitMat);
      button.rotation.x = Math.PI / 2;
      button.position.set(0, 0.38, 0.155);
      spine.add(button);

      // Smooth Anatomical Clavicle / Shoulder Bridge
      const clavicleYoke = new THREE.Mesh(new THREE.CylinderGeometry(0.038, 0.038, 0.44, 20), outfitMat);
      clavicleYoke.rotation.z = Math.PI / 2;
      clavicleYoke.position.set(0, 0.44, 0.0);
      spine.add(clavicleYoke);"""

new_torso = """      // Upper Bust & Formal Blazer
      const bust = new THREE.Mesh(new THREE.CylinderGeometry(0.195, 0.155, 0.28, 24), outfitMat);
      bust.position.y = 0.35;
      spine.add(bust);

      // Crisp Collared V-Neck Blouse Insert
      const topInsert = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.08, 0.17, 16), topMat);
      topInsert.position.set(0, 0.41, 0.088);
      spine.add(topInsert);

      // Professional Tailored Blazer Lapels (Left & Right V-Flaps)
      const lapelGeo = new THREE.BoxGeometry(0.040, 0.20, 0.015);
      const lapelL = new THREE.Mesh(lapelGeo, lapelMat);
      lapelL.position.set(-0.065, 0.37, 0.125);
      lapelL.rotation.z = 0.20;
      lapelL.rotation.y = -0.15;
      spine.add(lapelL);

      const lapelR = new THREE.Mesh(lapelGeo, lapelMat);
      lapelR.position.set(0.065, 0.37, 0.125);
      lapelR.rotation.z = -0.20;
      lapelR.rotation.y = 0.15;
      spine.add(lapelR);

      // Crisp Blouse Shirt Collar
      const collarL = new THREE.Mesh(new THREE.BoxGeometry(0.030, 0.06, 0.010), collarMat);
      collarL.position.set(-0.045, 0.46, 0.095);
      collarL.rotation.set(0.1, -0.2, 0.35);
      spine.add(collarL);

      const collarR = new THREE.Mesh(new THREE.BoxGeometry(0.030, 0.06, 0.010), collarMat);
      collarR.position.set(0.045, 0.46, 0.095);
      collarR.rotation.set(0.1, 0.2, -0.35);
      spine.add(collarR);

      // Subtle Premium Gold Buttons
      const button1 = new THREE.Mesh(new THREE.CylinderGeometry(0.007, 0.007, 0.005, 16), goldMat);
      button1.rotation.x = Math.PI / 2;
      button1.position.set(0, 0.31, 0.165);
      spine.add(button1);

      const button2 = new THREE.Mesh(new THREE.CylinderGeometry(0.007, 0.007, 0.005, 16), goldMat);
      button2.rotation.x = Math.PI / 2;
      button2.position.set(0, 0.23, 0.160);
      spine.add(button2);

      // Smooth Anatomical Clavicle / Shoulder Bridge with Blazer Padding
      const clavicleYoke = new THREE.Mesh(new THREE.CylinderGeometry(0.040, 0.040, 0.44, 20), outfitMat);
      clavicleYoke.rotation.z = Math.PI / 2;
      clavicleYoke.position.set(0, 0.44, 0.0);
      spine.add(clavicleYoke);"""

if old_torso in html:
    html = html.replace(old_torso, new_torso)
    print("Upgraded torso with tailored lapels, shirt collar, and gold buttons.")
else:
    print("Warning: old_torso not found.")

# 4. Upgrade Face, Nose, Lips, and Hair
# Find head mesh down to ponytail
old_face_and_hair = """      // Soft Humanoid Face Mesh (Cute almond shape)
      const headMesh = new THREE.Mesh(new THREE.SphereGeometry(0.128, 28, 28), skinMat);
      headMesh.scale.set(0.94, 1.22, 1.05);
      head.add(headMesh);

      // Soft rounded feminine chin
      const chinMesh = new THREE.Mesh(new THREE.ConeGeometry(0.065, 0.09, 20), skinMat);
      chinMesh.position.set(0, -0.085, 0.035);
      chinMesh.rotation.x = Math.PI;
      head.add(chinMesh);

      // Soft sculpted nose
      const noseGeo = new THREE.ConeGeometry(0.018, 0.054, 16);
      const nose = new THREE.Mesh(noseGeo, skinMat);
      nose.position.set(0, -0.012, 0.138);
      nose.rotation.x = Math.PI / 10;
      head.add(nose);

      // Expressive Lips (Natural smile & mouthing)
      const lipGeo = new THREE.BoxGeometry(0.046, 0.014, 0.020);
      const lips = new THREE.Mesh(lipGeo, lipMat);
      lips.position.set(0, -0.058, 0.134);
      head.add(lips);
      avatarRig.lips = lips;

      // Big, Expressive Almond Eyes with Blinking Eyelids
      function createEye(isLeft) {
        const eyeGroup = new THREE.Group();
        const xSign = isLeft ? -1 : 1;
        eyeGroup.position.set(xSign * 0.045, 0.022, 0.126);

        // Sclera
        const sclera = new THREE.Mesh(new THREE.SphereGeometry(0.020, 20, 20), scleraMat);
        sclera.scale.set(1.22, 0.85, 0.80);
        eyeGroup.add(sclera);

        // Warm Brown Iris
        const iris = new THREE.Mesh(new THREE.CircleGeometry(0.011, 20), eyeIrisMat);
        iris.position.set(0, 0, 0.017);
        eyeGroup.add(iris);

        // Cute Sparkling Highlights
        const glint1 = new THREE.Mesh(new THREE.CircleGeometry(0.0035, 12), new THREE.MeshBasicMaterial({ color: 0xffffff }));
        glint1.position.set(0.003, 0.003, 0.018);
        eyeGroup.add(glint1);

        const glint2 = new THREE.Mesh(new THREE.CircleGeometry(0.0018, 8), new THREE.MeshBasicMaterial({ color: 0xffffff }));
        glint2.position.set(-0.003, -0.003, 0.018);
        eyeGroup.add(glint2);

        // Eyelid for Smooth Blinking
        const lidGeo = new THREE.SphereGeometry(0.022, 20, 14, 0, Math.PI * 2, 0, Math.PI / 2);
        const lid = new THREE.Mesh(lidGeo, skinMat);
        lid.rotation.x = -Math.PI / 2;
        lid.position.set(0, 0.006, 0.003);
        eyeGroup.add(lid);

        return { eyeGroup, lid };
      }

      const leftEyeObj = createEye(true);
      const rightEyeObj = createEye(false);
      head.add(leftEyeObj.eyeGroup);
      head.add(rightEyeObj.eyeGroup);
      avatarRig.leftLid = leftEyeObj.lid;
      avatarRig.rightLid = rightEyeObj.lid;

      // Cute Dynamic Eyebrows (Physical motion for ISL markers)
      const browGeo = new THREE.BoxGeometry(0.042, 0.008, 0.010);
      const browL = new THREE.Mesh(browGeo, browMat);
      browL.position.set(-0.045, 0.054, 0.130);
      browL.rotation.z = -0.05;
      head.add(browL);
      avatarRig.browL = browL;

      const browR = new THREE.Mesh(browGeo, browMat);
      browR.position.set(0.045, 0.054, 0.130);
      browR.rotation.z = 0.05;
      head.add(browR);
      avatarRig.browR = browR;

      // Stylish Hair (Brunette with cute ponytail & bangs)
      const hairBase = new THREE.Mesh(new THREE.SphereGeometry(0.136, 24, 24), hairMat);
      hairBase.position.set(0, 0.038, -0.015);
      hairBase.scale.set(1.02, 1.20, 1.08);
      head.add(hairBase);

      // Cute High Ponytail
      const ponytail = new THREE.Mesh(new THREE.CylinderGeometry(0.032, 0.018, 0.24, 16), hairMat);
      ponytail.rotation.x = -0.45;
      ponytail.position.set(0, 0.06, -0.16);
      head.add(ponytail);"""

new_face_and_hair = """      // Realistic Cranium & Head Base (Natural human proportions)
      const headMesh = new THREE.Mesh(new THREE.SphereGeometry(0.126, 32, 32), skinMat);
      headMesh.scale.set(0.92, 1.18, 1.04);
      head.add(headMesh);

      // Natural Human Cheekbones (Subtle cheek contours)
      const cheekL = new THREE.Mesh(new THREE.SphereGeometry(0.042, 16, 16), skinMat);
      cheekL.position.set(-0.055, -0.015, 0.090);
      cheekL.scale.set(1.0, 0.85, 0.70);
      head.add(cheekL);

      const cheekR = new THREE.Mesh(new THREE.SphereGeometry(0.042, 16, 16), skinMat);
      cheekR.position.set(0.055, -0.015, 0.090);
      cheekR.scale.set(1.0, 0.85, 0.70);
      head.add(cheekR);

      // Natural feminine jawline & rounded chin
      const chinMesh = new THREE.Mesh(new THREE.CylinderGeometry(0.048, 0.032, 0.075, 20), skinMat);
      chinMesh.position.set(0, -0.088, 0.045);
      chinMesh.rotation.x = 0.25;
      head.add(chinMesh);

      // Anatomically Sculpted Nose (Bridge, tip, and delicate nostrils)
      const noseBridge = new THREE.Mesh(new THREE.CylinderGeometry(0.010, 0.014, 0.050, 16), skinMat);
      noseBridge.position.set(0, 0.012, 0.134);
      noseBridge.rotation.x = 0.28;
      head.add(noseBridge);

      const noseTip = new THREE.Mesh(new THREE.SphereGeometry(0.014, 16, 16), skinMat);
      noseTip.position.set(0, -0.016, 0.144);
      head.add(noseTip);

      const nostrilL = new THREE.Mesh(new THREE.SphereGeometry(0.007, 12, 12), skinMat);
      nostrilL.position.set(-0.012, -0.020, 0.137);
      head.add(nostrilL);

      const nostrilR = new THREE.Mesh(new THREE.SphereGeometry(0.007, 12, 12), skinMat);
      nostrilR.position.set(0.012, -0.020, 0.137);
      head.add(nostrilR);

      // Expressive Natural Lips (Upper Cupid's Bow + Fuller Lower Lip)
      const lipsGroup = new THREE.Group();
      lipsGroup.position.set(0, -0.056, 0.132);
      head.add(lipsGroup);
      avatarRig.lips = lipsGroup;

      const upperLip = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 0.042, 16), lipMat);
      upperLip.rotation.z = Math.PI / 2;
      upperLip.position.set(0, 0.006, 0.003);
      upperLip.scale.set(0.65, 1.0, 0.90);
      lipsGroup.add(upperLip);

      const lowerLip = new THREE.Mesh(new THREE.CylinderGeometry(0.010, 0.010, 0.038, 16), lipMat);
      lowerLip.rotation.z = Math.PI / 2;
      lowerLip.position.set(0, -0.006, 0.002);
      lowerLip.scale.set(0.85, 1.0, 1.05);
      lipsGroup.add(lowerLip);

      // Delicate Human Ears & Professional Pearl Studs
      function createEar(isLeft) {
        const earGroup = new THREE.Group();
        const xSign = isLeft ? -1 : 1;
        earGroup.position.set(xSign * 0.118, 0.005, -0.010);
        earGroup.rotation.y = xSign * 0.25;

        const earHelix = new THREE.Mesh(new THREE.TorusGeometry(0.024, 0.007, 12, 20, Math.PI * 1.3), skinMat);
        earHelix.rotation.z = isLeft ? -0.4 : 0.4;
        earGroup.add(earHelix);

        const earLobe = new THREE.Mesh(new THREE.SphereGeometry(0.012, 12, 12), skinMat);
        earLobe.position.set(0, -0.022, 0);
        earGroup.add(earLobe);

        // Elegant Pearl Stud Earring
        const pearlStud = new THREE.Mesh(new THREE.SphereGeometry(0.005, 16, 16), new THREE.MeshStandardMaterial({
          color: 0xfffbf0,
          roughness: 0.25,
          metalness: 0.15
        }));
        pearlStud.position.set(0, -0.022, 0.007);
        earGroup.add(pearlStud);

        return earGroup;
      }
      head.add(createEar(true));
      head.add(createEar(false));

      // Realistic Almond Eyes with Smooth Blinking Eyelids
      function createEye(isLeft) {
        const eyeGroup = new THREE.Group();
        const xSign = isLeft ? -1 : 1;
        eyeGroup.position.set(xSign * 0.044, 0.022, 0.124);

        // Eyeball Sclera
        const sclera = new THREE.Mesh(new THREE.SphereGeometry(0.020, 24, 24), scleraMat);
        sclera.scale.set(1.15, 0.88, 0.85);
        eyeGroup.add(sclera);

        // Deep warm brown iris with subtle depth
        const iris = new THREE.Mesh(new THREE.CircleGeometry(0.011, 24), eyeIrisMat);
        iris.position.set(0, 0, 0.0175);
        eyeGroup.add(iris);

        // Pupil
        const pupil = new THREE.Mesh(new THREE.CircleGeometry(0.0055, 16), new THREE.MeshBasicMaterial({ color: 0x080402 }));
        pupil.position.set(0, 0, 0.018);
        eyeGroup.add(pupil);

        // Dual Catchlights for lively professional gaze
        const glint1 = new THREE.Mesh(new THREE.CircleGeometry(0.0030, 12), new THREE.MeshBasicMaterial({ color: 0xffffff }));
        glint1.position.set(0.003, 0.003, 0.0185);
        eyeGroup.add(glint1);

        const glint2 = new THREE.Mesh(new THREE.CircleGeometry(0.0016, 8), new THREE.MeshBasicMaterial({ color: 0xffffff }));
        glint2.position.set(-0.003, -0.003, 0.0185);
        eyeGroup.add(glint2);

        // Upper Eyelash line
        const lashGeo = new THREE.CylinderGeometry(0.002, 0.002, 0.038, 12);
        const lash = new THREE.Mesh(lashGeo, new THREE.MeshBasicMaterial({ color: 0x120c08 }));
        lash.rotation.z = Math.PI / 2;
        lash.position.set(0, 0.015, 0.014);
        eyeGroup.add(lash);

        // Eyelid for Smooth Natural Blinking
        const lidGeo = new THREE.SphereGeometry(0.022, 24, 16, 0, Math.PI * 2, 0, Math.PI / 2);
        const lid = new THREE.Mesh(lidGeo, skinMat);
        lid.rotation.x = -Math.PI / 2;
        lid.position.set(0, 0.006, 0.003);
        eyeGroup.add(lid);

        return { eyeGroup, lid };
      }

      const leftEyeObj = createEye(true);
      const rightEyeObj = createEye(false);
      head.add(leftEyeObj.eyeGroup);
      head.add(rightEyeObj.eyeGroup);
      avatarRig.leftLid = leftEyeObj.lid;
      avatarRig.rightLid = rightEyeObj.lid;

      // Sculpted Arch Eyebrows (Dynamic non-manual grammatical markers)
      const browGeo = new THREE.CylinderGeometry(0.0035, 0.0025, 0.044, 16);
      const browL = new THREE.Mesh(browGeo, browMat);
      browL.rotation.z = Math.PI / 2 + 0.12;
      browL.position.set(-0.045, 0.052, 0.128);
      head.add(browL);
      avatarRig.browL = browL;

      const browR = new THREE.Mesh(browGeo, browMat);
      browR.rotation.z = -(Math.PI / 2 + 0.12);
      browR.position.set(0.045, 0.052, 0.128);
      head.add(browR);
      avatarRig.browR = browR;

      // Professional Hairstyling (Elegant Side-Parted Hair with Sleek Professional Low Bun)
      const hairCrown = new THREE.Mesh(new THREE.SphereGeometry(0.138, 28, 28), hairMat);
      hairCrown.position.set(0, 0.038, -0.016);
      hairCrown.scale.set(1.02, 1.18, 1.08);
      head.add(hairCrown);

      // Sleek side fringe strands across forehead
      const fringeL = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.012, 0.12, 16), hairHighlightMat);
      fringeL.position.set(-0.058, 0.055, 0.110);
      fringeL.rotation.set(-0.35, 0.45, 0.85);
      head.add(fringeL);

      const fringeR = new THREE.Mesh(new THREE.CylinderGeometry(0.020, 0.010, 0.09, 16), hairMat);
      fringeR.position.set(0.065, 0.058, 0.105);
      fringeR.rotation.set(-0.35, -0.35, -0.75);
      head.add(fringeR);

      // Elegant Professional Low Chignon / Bun (Neat & Formal)
      const bun = new THREE.Mesh(new THREE.SphereGeometry(0.055, 20, 20), hairMat);
      bun.position.set(0, -0.015, -0.145);
      bun.scale.set(1.15, 0.95, 0.85);
      head.add(bun);

      // Sophisticated tortoiseshell hair pin accent
      const hairPin = new THREE.Mesh(new THREE.TorusGeometry(0.050, 0.005, 10, 24), goldMat);
      hairPin.position.set(0, -0.015, -0.142);
      head.add(hairPin);"""

if old_face_and_hair in html:
    html = html.replace(old_face_and_hair, new_face_and_hair)
    print("Upgraded face, ears, pearl studs, sculpted nose, lips, and sleek professional hair.")
else:
    print("Warning: old_face_and_hair not found, check snippet.")

with open(r'C:\Users\laksh\.gemini\antigravity\scratch\rag-speech-to-isl\frontend\public\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html successfully!")
