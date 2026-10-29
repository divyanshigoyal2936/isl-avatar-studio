import re

with open(r'C:\Users\laksh\.gemini\antigravity\scratch\rag-speech-to-isl\frontend\public\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update materials in buildHumanoidAvatar to match Asian female model with porcelain-warm skin, dark midnight-navy suit, white mandarin blouse & silver brooch
old_mats = """      // Realistic warm human skin tone (Rich warm Indian olive complexion)
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

new_mats = """      // Porcelain fair skin with natural soft peachy warmth (Exact match to reference model)
      const skinColor = 0xf5dfd2; 
      const skinMat = new THREE.MeshStandardMaterial({
        color: skinColor,
        roughness: 0.52,
        metalness: 0.01
      });
      avatarRig.skinMat = skinMat;

      // Natural soft rose coral lip tone
      const lipMat = new THREE.MeshStandardMaterial({
        color: 0xd97c76,
        roughness: 0.32,
        metalness: 0.02
      });

      // Tailored Deep Ink-Navy Suit Fabric (Two-piece blazer and knee-length pencil skirt)
      const outfitMat = new THREE.MeshStandardMaterial({
        color: 0x1d273d, // High-end deep navy suiting wool
        roughness: 0.72,
        metalness: 0.04
      });

      const lapelMat = new THREE.MeshStandardMaterial({
        color: 0x182033, // Structured blazer lapel
        roughness: 0.65,
        metalness: 0.06
      });

      // Crisp White Silk Blouse with Mandarin Collar & Pleats
      const blouseMat = new THREE.MeshStandardMaterial({
        color: 0xfafafa,
        roughness: 0.48,
        metalness: 0.01
      });

      // Sparkling Silver / Platinum Floral Brooch on left lapel
      const silverBroochMat = new THREE.MeshStandardMaterial({
        color: 0xe2e8f0,
        roughness: 0.20,
        metalness: 0.85
      });

      // Single Horn Center Button
      const buttonMat = new THREE.MeshStandardMaterial({
        color: 0x0f1522,
        roughness: 0.40,
        metalness: 0.20
      });

      // Jet Black Sleek Hair with Soft Gloss
      const hairMat = new THREE.MeshStandardMaterial({
        color: 0x121010,
        roughness: 0.55,
        metalness: 0.08
      });

      const hairStrandMat = new THREE.MeshStandardMaterial({
        color: 0x1a1615,
        roughness: 0.50,
        metalness: 0.09
      });

      // Pointed Stiletto Pumps (Black Patent Leather)
      const shoeMat = new THREE.MeshStandardMaterial({
        color: 0x08090b,
        roughness: 0.22,
        metalness: 0.35
      });

      const eyeIrisMat = new THREE.MeshBasicMaterial({ color: 0x1c120c }); // Natural dark brown almond eyes
      const scleraMat = new THREE.MeshBasicMaterial({ color: 0xfdfdfd });
      const browMat = new THREE.MeshStandardMaterial({ color: 0x14100e, roughness: 0.85 });"""

if old_mats in html:
    html = html.replace(old_mats, new_mats)
    print("Updated materials to reference model palette.")
else:
    print("Warning: old_mats not found, check snippet.")

# 2. Update Pelvis, Knee-Length Pencil Skirt, Legs & Pointed Pumps
old_legs = """      // 1. Lower Body & Pelvis
      const pelvis = new THREE.Group();
      pelvis.position.y = 0.85;
      avatarRoot.add(pelvis);
      avatarRig.pelvis = pelvis;

      const legL = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.055, 0.75, 18), outfitMat);
      legL.position.set(-0.10, -0.42, 0);
      pelvis.add(legL);

      const legR = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.055, 0.75, 18), outfitMat);
      legR.position.set(0.10, -0.42, 0);
      pelvis.add(legR);

      // Elegant Shoes
      const shoeGeo = new THREE.BoxGeometry(0.090, 0.060, 0.19);
      const shoeMat = new THREE.MeshStandardMaterial({ color: 0x0f131a, roughness: 0.4 });
      const shoeL = new THREE.Mesh(shoeGeo, shoeMat);
      shoeL.position.set(-0.10, -0.80, 0.035);
      pelvis.add(shoeL);
      const shoeR = new THREE.Mesh(shoeGeo, shoeMat);
      shoeR.position.set(0.10, -0.80, 0.035);
      pelvis.add(shoeR);"""

new_legs = """      // 1. Lower Body: Tailored Navy Pencil Skirt & Bare Legs with Pointed Pumps
      const pelvis = new THREE.Group();
      pelvis.position.y = 0.85;
      avatarRoot.add(pelvis);
      avatarRig.pelvis = pelvis;

      // High-Waisted Knee-Length Navy Pencil Skirt
      const skirt = new THREE.Mesh(new THREE.CylinderGeometry(0.165, 0.145, 0.44, 28), outfitMat);
      skirt.position.set(0, -0.16, 0.0);
      pelvis.add(skirt);

      // Slender Bare Calves / Legs (Fair Skin)
      const calfL = new THREE.Mesh(new THREE.CylinderGeometry(0.042, 0.028, 0.48, 20), skinMat);
      calfL.position.set(-0.048, -0.56, 0.0);
      pelvis.add(calfL);

      const calfR = new THREE.Mesh(new THREE.CylinderGeometry(0.042, 0.028, 0.48, 20), skinMat);
      calfR.position.set(0.048, -0.56, 0.0);
      pelvis.add(calfR);

      // Elegant Pointed-Toe Black Stiletto Pumps
      function createPump(isLeft) {
        const pumpGroup = new THREE.Group();
        const xPos = isLeft ? -0.052 : 0.052;
        pumpGroup.position.set(xPos, -0.80, 0.02);

        // Pointed front shoe body
        const vamp = new THREE.Mesh(new THREE.ConeGeometry(0.040, 0.14, 16), shoeMat);
        vamp.rotation.x = -Math.PI / 2.3;
        vamp.scale.set(0.9, 0.6, 1.3);
        vamp.position.set(0, 0.015, 0.05);
        pumpGroup.add(vamp);

        // Heel cup
        const heelCup = new THREE.Mesh(new THREE.SphereGeometry(0.035, 16, 14, 0, Math.PI * 2, 0, Math.PI / 2), shoeMat);
        heelCup.position.set(0, 0.03, -0.03);
        pumpGroup.add(heelCup);

        // Stiletto Heel
        const heelSpike = new THREE.Mesh(new THREE.CylinderGeometry(0.005, 0.003, 0.065, 10), shoeMat);
        heelSpike.position.set(0, -0.010, -0.042);
        pumpGroup.add(heelSpike);

        return pumpGroup;
      }
      pelvis.add(createPump(true));
      pelvis.add(createPump(false));"""

if old_legs in html:
    html = html.replace(old_legs, new_legs)
    print("Replaced legs with tailored pencil skirt and pointed-toe stiletto pumps.")
else:
    print("Warning: old_legs not found.")

# 3. Update Torso: Peplum-waist Blazer, Mandarin pleated blouse, single button & silver floral brooch
old_torso = """      // 2. Spine & Torso (Soft feminine curves, not blocky)
      const spine = new THREE.Group();
      spine.position.y = 0.0;
      pelvis.add(spine);
      avatarRig.spine = spine;

      // Waist & Hips
      const waist = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.165, 0.22, 24), outfitMat);
      waist.position.y = 0.11;
      spine.add(waist);

      // Upper Bust & Formal Blazer
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

new_torso = """      // 2. Spine & Torso: Fitted Navy Peplum Blazer & Pleated Mandarin Blouse
      const spine = new THREE.Group();
      spine.position.y = 0.0;
      pelvis.add(spine);
      avatarRig.spine = spine;

      // Cinched Waist with Peplum Flare Hem
      const waist = new THREE.Mesh(new THREE.CylinderGeometry(0.138, 0.160, 0.20, 26), outfitMat);
      waist.position.y = 0.10;
      spine.add(waist);

      // Flared Peplum Hem of Blazer over Hips (Exactly like reference)
      const peplum = new THREE.Mesh(new THREE.ConeGeometry(0.180, 0.11, 28, 1, true), outfitMat);
      peplum.rotation.x = Math.PI;
      peplum.position.set(0, 0.04, 0.0);
      spine.add(peplum);

      // Upper Bust & Tailored Jacket
      const bust = new THREE.Mesh(new THREE.CylinderGeometry(0.188, 0.140, 0.28, 26), outfitMat);
      bust.position.y = 0.34;
      spine.add(bust);

      // White Silk Blouse Insert with Vertical Pleating
      const blouseInsert = new THREE.Mesh(new THREE.CylinderGeometry(0.095, 0.070, 0.20, 18), blouseMat);
      blouseInsert.position.set(0, 0.40, 0.088);
      spine.add(blouseInsert);

      // Mandarin Ruffled / Gathered High Collar (Standing collar around neck)
      const mandarinCollar = new THREE.Mesh(new THREE.CylinderGeometry(0.052, 0.056, 0.045, 20, 1, true), blouseMat);
      mandarinCollar.position.set(0, 0.49, 0.020);
      spine.add(mandarinCollar);

      // Sharp Notched Tailored Lapels (Deep V-cut)
      const lapelGeo = new THREE.BoxGeometry(0.038, 0.22, 0.012);
      const lapelL = new THREE.Mesh(lapelGeo, lapelMat);
      lapelL.position.set(-0.065, 0.35, 0.118);
      lapelL.rotation.z = 0.24;
      lapelL.rotation.y = -0.15;
      spine.add(lapelL);

      const lapelR = new THREE.Mesh(lapelGeo, lapelMat);
      lapelR.position.set(0.065, 0.35, 0.118);
      lapelR.rotation.z = -0.24;
      lapelR.rotation.y = 0.15;
      spine.add(lapelR);

      // Single Center Fastening Button at cinched waist
      const centerBtn = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 0.005, 16), buttonMat);
      centerBtn.rotation.x = Math.PI / 2;
      centerBtn.position.set(0, 0.24, 0.150);
      spine.add(centerBtn);

      // Silver Sparkling Floral Lapel Brooch (Pin on upper left lapel, exactly like image)
      const broochGroup = new THREE.Group();
      broochGroup.position.set(-0.075, 0.41, 0.132);
      broochGroup.rotation.y = -0.20;

      const broochCenter = new THREE.Mesh(new THREE.SphereGeometry(0.004, 12, 12), silverBroochMat);
      broochGroup.add(broochCenter);
      for (let i = 0; i < 5; i++) {
        const petal = new THREE.Mesh(new THREE.ConeGeometry(0.003, 0.010, 8), silverBroochMat);
        petal.position.set(Math.cos(i * Math.PI * 0.4) * 0.006, Math.sin(i * Math.PI * 0.4) * 0.006, 0);
        petal.rotation.z = i * Math.PI * 0.4 - Math.PI / 2;
        broochGroup.add(petal);
      }
      spine.add(broochGroup);

      // Smooth Anatomical Clavicle / Shoulder Bridge with Tailored Blazer Pads
      const clavicleYoke = new THREE.Mesh(new THREE.CylinderGeometry(0.040, 0.040, 0.44, 20), outfitMat);
      clavicleYoke.rotation.z = Math.PI / 2;
      clavicleYoke.position.set(0, 0.44, 0.0);
      spine.add(clavicleYoke);"""

if old_torso in html:
    html = html.replace(old_torso, new_torso)
    print("Replaced torso with fitted peplum blazer, mandarin blouse, center button & silver brooch.")
else:
    print("Warning: old_torso not found.")

# 4. Update Face & Updo Hair with loose tendril side strands
old_face = """      // Realistic Cranium & Head Base (Natural human proportions)
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

new_face = """      // Realistic Asian Female Head Profile (Refined jawline, porcelain-peachy tone)
      const headMesh = new THREE.Mesh(new THREE.SphereGeometry(0.124, 32, 32), skinMat);
      headMesh.scale.set(0.90, 1.16, 1.02);
      head.add(headMesh);

      // Delicate Soft Cheek Contours
      const cheekL = new THREE.Mesh(new THREE.SphereGeometry(0.038, 16, 16), skinMat);
      cheekL.position.set(-0.052, -0.012, 0.088);
      cheekL.scale.set(1.0, 0.85, 0.70);
      head.add(cheekL);

      const cheekR = new THREE.Mesh(new THREE.SphereGeometry(0.038, 16, 16), skinMat);
      cheekR.position.set(0.052, -0.012, 0.088);
      cheekR.scale.set(1.0, 0.85, 0.70);
      head.add(cheekR);

      // Slender Tapered Chin (V-Line Jaw Profile as in reference photo)
      const chinMesh = new THREE.Mesh(new THREE.CylinderGeometry(0.042, 0.024, 0.070, 20), skinMat);
      chinMesh.position.set(0, -0.084, 0.042);
      chinMesh.rotation.x = 0.22;
      head.add(chinMesh);

      // Slender Defined Nose with Petite Tip
      const noseBridge = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.012, 0.048, 16), skinMat);
      noseBridge.position.set(0, 0.012, 0.130);
      noseBridge.rotation.x = 0.26;
      head.add(noseBridge);

      const noseTip = new THREE.Mesh(new THREE.SphereGeometry(0.012, 16, 16), skinMat);
      noseTip.position.set(0, -0.014, 0.140);
      head.add(noseTip);

      // Natural Coral-Rose Lips (Subtle gentle smile)
      const lipsGroup = new THREE.Group();
      lipsGroup.position.set(0, -0.054, 0.128);
      head.add(lipsGroup);
      avatarRig.lips = lipsGroup;

      const upperLip = new THREE.Mesh(new THREE.CylinderGeometry(0.007, 0.007, 0.040, 16), lipMat);
      upperLip.rotation.z = Math.PI / 2;
      upperLip.position.set(0, 0.005, 0.003);
      upperLip.scale.set(0.60, 1.0, 0.85);
      lipsGroup.add(upperLip);

      const lowerLip = new THREE.Mesh(new THREE.CylinderGeometry(0.009, 0.009, 0.036, 16), lipMat);
      lowerLip.rotation.z = Math.PI / 2;
      lowerLip.position.set(0, -0.005, 0.002);
      lowerLip.scale.set(0.80, 1.0, 1.00);
      lipsGroup.add(lowerLip);

      // Delicate Ears with Dainty Pearl Drop Earrings
      function createEar(isLeft) {
        const earGroup = new THREE.Group();
        const xSign = isLeft ? -1 : 1;
        earGroup.position.set(xSign * 0.114, 0.005, -0.008);
        earGroup.rotation.y = xSign * 0.22;

        const earHelix = new THREE.Mesh(new THREE.TorusGeometry(0.022, 0.006, 12, 20, Math.PI * 1.3), skinMat);
        earHelix.rotation.z = isLeft ? -0.4 : 0.4;
        earGroup.add(earHelix);

        const earLobe = new THREE.Mesh(new THREE.SphereGeometry(0.010, 12, 12), skinMat);
        earLobe.position.set(0, -0.020, 0);
        earGroup.add(earLobe);

        // Elegant Petite Pearl Stud Earring
        const pearlStud = new THREE.Mesh(new THREE.SphereGeometry(0.0045, 16, 16), new THREE.MeshStandardMaterial({
          color: 0xffffff,
          roughness: 0.20,
          metalness: 0.15
        }));
        pearlStud.position.set(0, -0.020, 0.006);
        earGroup.add(pearlStud);

        return earGroup;
      }
      head.add(createEar(true));
      head.add(createEar(false));

      // Almond Eyes with Defined Lashline and Dual Specular Highlights
      function createEye(isLeft) {
        const eyeGroup = new THREE.Group();
        const xSign = isLeft ? -1 : 1;
        eyeGroup.position.set(xSign * 0.042, 0.022, 0.120);

        // Sclera
        const sclera = new THREE.Mesh(new THREE.SphereGeometry(0.019, 24, 24), scleraMat);
        sclera.scale.set(1.15, 0.85, 0.85);
        eyeGroup.add(sclera);

        // Deep warm brown iris
        const iris = new THREE.Mesh(new THREE.CircleGeometry(0.0105, 24), eyeIrisMat);
        iris.position.set(0, 0, 0.017);
        eyeGroup.add(iris);

        // Pupil
        const pupil = new THREE.Mesh(new THREE.CircleGeometry(0.0050, 16), new THREE.MeshBasicMaterial({ color: 0x050302 }));
        pupil.position.set(0, 0, 0.0175);
        eyeGroup.add(pupil);

        // Catchlights (Sparkling lively gaze)
        const glint1 = new THREE.Mesh(new THREE.CircleGeometry(0.0028, 12), new THREE.MeshBasicMaterial({ color: 0xffffff }));
        glint1.position.set(0.0028, 0.0028, 0.018);
        eyeGroup.add(glint1);

        const glint2 = new THREE.Mesh(new THREE.CircleGeometry(0.0014, 8), new THREE.MeshBasicMaterial({ color: 0xffffff }));
        glint2.position.set(-0.0028, -0.0028, 0.018);
        eyeGroup.add(glint2);

        // Upper Eyelash line contour
        const lashGeo = new THREE.CylinderGeometry(0.0018, 0.0018, 0.036, 12);
        const lash = new THREE.Mesh(lashGeo, new THREE.MeshBasicMaterial({ color: 0x100a06 }));
        lash.rotation.z = Math.PI / 2;
        lash.position.set(0, 0.014, 0.013);
        eyeGroup.add(lash);

        // Eyelid for Smooth Natural Blinking
        const lidGeo = new THREE.SphereGeometry(0.021, 24, 16, 0, Math.PI * 2, 0, Math.PI / 2);
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

      // Soft Arch Eyebrows (Dynamic ISL non-manual grammar)
      const browGeo = new THREE.CylinderGeometry(0.0030, 0.0020, 0.042, 16);
      const browL = new THREE.Mesh(browGeo, browMat);
      browL.rotation.z = Math.PI / 2 + 0.10;
      browL.position.set(-0.042, 0.050, 0.124);
      head.add(browL);
      avatarRig.browL = browL;

      const browR = new THREE.Mesh(browGeo, browMat);
      browR.rotation.z = -(Math.PI / 2 + 0.10);
      browR.position.set(0.042, 0.050, 0.124);
      head.add(browR);
      avatarRig.browR = browR;

      // Elegant Updo Hairstyle (Soft Center-Parting with Whispy Tendrils Framing Face, as in photo)
      const hairCrown = new THREE.Mesh(new THREE.SphereGeometry(0.134, 28, 28), hairMat);
      hairCrown.position.set(0, 0.038, -0.016);
      hairCrown.scale.set(1.02, 1.16, 1.06);
      head.add(hairCrown);

      // Whispy side face-framing tendrils (Left & Right soft curved strands)
      const tendrilL = new THREE.Mesh(new THREE.CylinderGeometry(0.010, 0.003, 0.16, 12), hairStrandMat);
      tendrilL.position.set(-0.082, -0.010, 0.065);
      tendrilL.rotation.set(0.20, 0.15, 0.28);
      head.add(tendrilL);

      const tendrilR = new THREE.Mesh(new THREE.CylinderGeometry(0.010, 0.003, 0.16, 12), hairStrandMat);
      tendrilR.position.set(0.082, -0.010, 0.065);
      tendrilR.rotation.set(0.20, -0.15, -0.28);
      head.add(tendrilR);

      // Soft Front Bangs / Curtain Parting Strands
      const bangL = new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.006, 0.09, 12), hairStrandMat);
      bangL.position.set(-0.045, 0.060, 0.114);
      bangL.rotation.set(-0.35, 0.30, 0.80);
      head.add(bangL);

      const bangR = new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.006, 0.09, 12), hairStrandMat);
      bangR.position.set(0.045, 0.060, 0.114);
      bangR.rotation.set(-0.35, -0.30, -0.80);
      head.add(bangR);

      // Chic Low Updo Chignon / Bun at back of head
      const bun = new THREE.Mesh(new THREE.SphereGeometry(0.052, 20, 20), hairMat);
      bun.position.set(0, -0.010, -0.140);
      bun.scale.set(1.18, 0.92, 0.85);
      head.add(bun);"""

if old_face in html:
    html = html.replace(old_face, new_face)
    print("Replaced head, face, eyes, and hairstyle with reference model.")
else:
    print("Warning: old_face not found.")

# 5. Update getRestingPose: Hands clasped gracefully in front of abdomen (exact match to photo!)
old_rest = """    function getRestingPose() {
      return {
        head: [0, 0, 0],
        browY: 0,
        mouthOpen: 0,
        smile: 0.15,
        bodyShiftZ: 0,
        bodyLeanX: 0,
        leftArm: {
          shoulder: [0.08, 0.0, 0.10],
          elbow: [0.0, 0.0, -0.12],
          wrist: [0.0, 0.0, 0.0],
          fingerCurl: [0.15, 0.15, 0.15, 0.15, 0.15]
        },
        rightArm: {
          shoulder: [0.08, 0.0, -0.10],
          elbow: [0.0, 0.0, 0.12],
          wrist: [0.0, 0.0, 0.0],
          fingerCurl: [0.15, 0.15, 0.15, 0.15, 0.15]
        }
      };
    }"""

new_rest = """    // Professional Idle Posture: Hands clasped elegantly over lower abdomen (Matching reference model)
    function getRestingPose() {
      return {
        head: [0, 0, 0],
        browY: 0,
        mouthOpen: 0,
        smile: 0.20,
        bodyShiftZ: 0,
        bodyLeanX: 0,
        leftArm: {
          shoulder: [-0.138, -0.021, -0.052],
          elbow: [-0.276, -0.349, 1.153],
          wrist: [0.454, -0.368, -0.321],
          fingerCurl: [0.35, 0.30, 0.30, 0.30, 0.30]
        },
        rightArm: {
          shoulder: [-0.170, -0.382, 0.089],
          elbow: [-0.912, 0.215, -0.810],
          wrist: [0.738, -2.084, 0.188],
          fingerCurl: [0.40, 0.35, 0.35, 0.35, 0.35]
        }
      };
    }"""

if old_rest in html:
    html = html.replace(old_rest, new_rest)
    print("Updated getRestingPose to elegant clasped-hands posture matching the reference image.")
else:
    print("Warning: old_rest not found.")

with open(r'C:\Users\laksh\.gemini\antigravity\scratch\rag-speech-to-isl\frontend\public\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("HTML updated successfully!")
