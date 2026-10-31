import re
from pathlib import Path

index_path = Path(r"C:\Users\laksh\.gemini\antigravity\scratch\rag-speech-to-isl\frontend\public\index.html")
content = index_path.read_text(encoding="utf-8")

# 1. Add GLTFLoader.js to head
if "GLTFLoader.js" not in content:
    content = content.replace(
        '<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>',
        '<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>\n  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"></script>'
    )
    print("Added GLTFLoader.js to head")

# 2. Replace buildHumanoidAvatar
build_pattern = re.compile(r'    // --- PROCEDURAL CUTE FEMALE HUMANOID AVATAR[\s\S]*?(?=    // --- ANATOMICAL ISL POSE LIBRARY)')
new_build = '''    // --- 3D RIGGED REALISTIC HUMAN AVATAR ENGINE (GLTF / SKINNED MESH / BLENDSHAPES) ---
    function setMorph(name, val) {
      if (!avatarRig.morphMeshes) return;
      const clamped = Math.max(0, Math.min(1, val));
      for (let i = 0; i < avatarRig.morphMeshes.length; i++) {
        const m = avatarRig.morphMeshes[i];
        if (m.morphTargetDictionary && (name in m.morphTargetDictionary)) {
          const idx = m.morphTargetDictionary[name];
          m.morphTargetInfluences[idx] = clamped;
        }
      }
    }

    function buildHumanoidAvatar() {
      const avatarRoot = new THREE.Group();
      scene.add(avatarRoot);
      avatarRig.root = avatarRoot;
      avatarRig.bones = {};
      avatarRig.morphMeshes = [];
      avatarRig.isReady = false;

      const signLabel = document.getElementById('currentSignLabel');
      if (signLabel) signLabel.textContent = "INITIALIZING 3D AVATAR...";

      const loader = new THREE.GLTFLoader();
      const primaryUrl = '/avatar.glb';
      const cdnFallbackUrl = 'https://cdn.jsdelivr.net/gh/met4citizen/TalkingHead@main/avatars/brunette.glb';

      function onAvatarLoaded(gltf) {
        const model = gltf.scene;
        model.position.set(0, 0, 0);
        model.scale.set(1.0, 1.0, 1.0);
        avatarRoot.add(model);

        model.traverse((child) => {
          if (child.isMesh) {
            child.castShadow = true;
            child.receiveShadow = true;

            // Skinned mesh with facial blendshapes (ARKit morph targets)
            if (child.morphTargetDictionary) {
              avatarRig.morphMeshes.push(child);
            }

            // Hide glasses to match user reference image
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
            }
          }

          if (child.isBone) {
            avatarRig.bones[child.name] = child;
            child.userData.initialRotation = child.rotation.clone();
            child.userData.initialQuaternion = child.quaternion.clone();
            child.userData.initialPosition = child.position.clone();
          }
        });

        // Bone aliases for high-level controls
        avatarRig.head = avatarRig.bones['Head'];
        avatarRig.neck = avatarRig.bones['Neck'];
        avatarRig.spine = avatarRig.bones['Spine2'] || avatarRig.bones['Spine1'] || avatarRig.bones['Spine'];
        avatarRig.hips = avatarRig.bones['Hips'];

        avatarRig.isReady = true;
        if (signLabel) signLabel.textContent = "READY";

        // Apply natural resting pose immediately
        applyPoseToAvatar(getRestingPose());
      }

      loader.load(
        primaryUrl,
        onAvatarLoaded,
        undefined,
        (err) => {
          console.warn('Local avatar loading failed, falling back to CDN...', err);
          loader.load(cdnFallbackUrl, onAvatarLoaded, undefined, (cdnErr) => {
            console.error('All avatar loads failed:', cdnErr);
          });
        }
      );
    }

'''

content, count1 = build_pattern.subn(new_build, content)
print("Replaced buildHumanoidAvatar:", count1)

# 3. Replace getRestingPose
rest_pattern = re.compile(r'    function getRestingPose\(\) \{[\s\S]*?return \{[\s\S]*?\};\s*\}')
new_rest = '''    function getRestingPose() {
      return {
        head: [0, 0, 0],
        browY: 0,
        mouthOpen: 0,
        smile: 0.18,
        bodyShiftZ: 0,
        bodyLeanX: 0,
        leftArm: {
          shoulder: [0, 0, 0],
          elbow: [0, 0, 0],
          wrist: [0, 0, 0],
          fingerCurl: [0.15, 0.15, 0.15, 0.15, 0.15]
        },
        rightArm: {
          shoulder: [0, 0, 0],
          elbow: [0, 0, 0],
          wrist: [0, 0, 0],
          fingerCurl: [0.15, 0.15, 0.15, 0.15, 0.15]
        }
      };
    }'''

content, count2 = rest_pattern.subn(new_rest, content)
print("Replaced getRestingPose:", count2)

# 4. Replace applyPoseToAvatar and applyFingerCurls
apply_pattern = re.compile(r'    // Apply calculated joint rotations and finger curls to Three\.js avatar bones[\s\S]*?(?=    // --- CONTINUOUS TIMELINE & ANIMATION LOOP ---)')
new_apply = '''    // Full Rigged Human Skeleton & Blendshape Pose Controller
    function applyFingerCurlBones(prefix, curls, isLeft) {
      if (!avatarRig.bones) return;
      const bones = avatarRig.bones;
      const fingerNames = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky'];
      const curlScale = 1.25;

      fingerNames.forEach((fname, i) => {
        const curl = curls[i] || 0;
        const total = curl * curlScale;

        const b1 = bones[prefix + 'Hand' + fname + '1'];
        const b2 = bones[prefix + 'Hand' + fname + '2'];
        const b3 = bones[prefix + 'Hand' + fname + '3'];

        if (fname === 'Thumb') {
          if (b1 && b1.userData && b1.userData.initialRotation) {
            b1.rotation.x = b1.userData.initialRotation.x + curl * 0.35;
            b1.rotation.z = b1.userData.initialRotation.z + (isLeft ? 1 : -1) * curl * 0.30;
          }
          if (b2 && b2.userData && b2.userData.initialRotation) b2.rotation.x = b2.userData.initialRotation.x + curl * 0.45;
          if (b3 && b3.userData && b3.userData.initialRotation) b3.rotation.x = b3.userData.initialRotation.x + curl * 0.40;
        } else {
          if (b1 && b1.userData && b1.userData.initialRotation) b1.rotation.x = b1.userData.initialRotation.x + total * 0.45;
          if (b2 && b2.userData && b2.userData.initialRotation) b2.rotation.x = b2.userData.initialRotation.x + total * 0.35;
          if (b3 && b3.userData && b3.userData.initialRotation) b3.rotation.x = b3.userData.initialRotation.x + total * 0.20;
        }
      });
    }

    function applyArmRotations(isLeft, armPose) {
      if (!avatarRig.bones || !armPose) return;
      const bones = avatarRig.bones;
      const prefix = isLeft ? 'Left' : 'Right';
      const armBone = bones[prefix + 'Arm'];
      const foreArmBone = bones[prefix + 'ForeArm'];
      const handBone = bones[prefix + 'Hand'];

      if (armBone && armBone.userData && armBone.userData.initialRotation) {
        const init = armBone.userData.initialRotation;
        armBone.rotation.set(
          init.x + (armPose.shoulder ? armPose.shoulder[0] : 0),
          init.y + (armPose.shoulder ? armPose.shoulder[1] : 0),
          init.z + (armPose.shoulder ? armPose.shoulder[2] : 0)
        );
      }
      if (foreArmBone && foreArmBone.userData && foreArmBone.userData.initialRotation) {
        const init = foreArmBone.userData.initialRotation;
        foreArmBone.rotation.set(
          init.x + (armPose.elbow ? armPose.elbow[0] : 0),
          init.y + (armPose.elbow ? armPose.elbow[1] : 0),
          init.z + (armPose.elbow ? armPose.elbow[2] : 0)
        );
      }
      if (handBone && handBone.userData && handBone.userData.initialRotation) {
        const init = handBone.userData.initialRotation;
        handBone.rotation.set(
          init.x + (armPose.wrist ? armPose.wrist[0] : 0),
          init.y + (armPose.wrist ? armPose.wrist[1] : 0),
          init.z + (armPose.wrist ? armPose.wrist[2] : 0)
        );
      }

      if (armPose.fingerCurl) {
        applyFingerCurlBones(prefix, armPose.fingerCurl, isLeft);
      }
    }

    function applyPoseToAvatar(pose) {
      if (!avatarRig.isReady || !avatarRig.bones) return;
      const bones = avatarRig.bones;

      // Natural Human Body Weight Shift & Leaning
      const spineBone = bones.Spine2 || bones.Spine1 || bones.Spine;
      if (spineBone && spineBone.userData && spineBone.userData.initialPosition) {
        spineBone.position.z = spineBone.userData.initialPosition.z + (pose.bodyShiftZ || 0);
        spineBone.rotation.x = spineBone.userData.initialRotation.x + (pose.bodyLeanX || 0);
      }

      // Head & Neck Tilt / Gaze
      if (bones.Head && bones.Head.userData && bones.Head.userData.initialRotation) {
        const hInit = bones.Head.userData.initialRotation;
        bones.Head.rotation.set(
          hInit.x + (pose.head ? pose.head[0] : 0),
          hInit.y + (pose.head ? pose.head[1] : 0),
          hInit.z + (pose.head ? pose.head[2] : 0)
        );
      }

      // Dynamic blendshape expressions (Smile / mouthing / brows)
      const smileVal = pose.smile !== undefined ? pose.smile : 0.18;
      setMorph('mouthSmile', smileVal);
      setMorph('mouthSmileLeft', smileVal * 0.9);
      setMorph('mouthSmileRight', smileVal * 0.9);

      const mouthOpenVal = pose.mouthOpen || 0.0;
      setMorph('jawOpen', mouthOpenVal);
      setMorph('mouthOpen', mouthOpenVal * 0.7);

      const browVal = pose.browY || 0.0;
      if (browVal > 0) {
        setMorph('browInnerUp', Math.min(1.0, browVal * 12));
        setMorph('browOuterUpLeft', Math.min(1.0, browVal * 8));
        setMorph('browOuterUpRight', Math.min(1.0, browVal * 8));
        setMorph('browDownLeft', 0);
        setMorph('browDownRight', 0);
      } else if (browVal < 0) {
        setMorph('browDownLeft', Math.min(1.0, -browVal * 14));
        setMorph('browDownRight', Math.min(1.0, -browVal * 14));
        setMorph('browInnerUp', 0);
        setMorph('browOuterUpLeft', 0);
        setMorph('browOuterUpRight', 0);
      } else {
        setMorph('browInnerUp', 0);
        setMorph('browDownLeft', 0);
        setMorph('browDownRight', 0);
      }

      // Left & Right Arm Articulations
      applyArmRotations(true, pose.leftArm);
      applyArmRotations(false, pose.rightArm);
    }

'''

content, count3 = apply_pattern.subn(new_apply, content)
print("Replaced applyPoseToAvatar:", count3)

# 5. Update animate function for breathing & blinking
anim_pattern = re.compile(r'      // Natural Human Micro-movements \(breathing, eye blinking\)[\s\S]*?(?=      if \(isPlaying && scheduledClips\.length > 0\))')
new_anim = '''      // Natural Human Micro-movements (breathing, eye blinking)
      if (avatarRig.bones && avatarRig.bones.Spine && avatarRig.bones.Spine.userData && avatarRig.bones.Spine.userData.initialPosition) {
        const breath = Math.sin(timestamp * 0.002) * 0.004;
        avatarRig.bones.Spine.position.y = avatarRig.bones.Spine.userData.initialPosition.y + breath;
      }

      // Eye blinking every 3.5 seconds via blendshapes
      const blinkCycle = timestamp % 3600;
      const blinkClosed = (blinkCycle < 140);
      const blinkWeight = blinkClosed ? 1.0 : 0.0;
      setMorph('eyeBlinkLeft', blinkWeight);
      setMorph('eyeBlinkRight', blinkWeight);

'''

content, count4 = anim_pattern.subn(new_anim, content)
print("Replaced animate breathing/blinking:", count4)

index_path.write_text(content, encoding="utf-8")
print("Updated frontend/public/index.html successfully!")
