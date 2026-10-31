import re
from pathlib import Path

index_path = Path(r"C:\Users\laksh\.gemini\antigravity\scratch\rag-speech-to-isl\frontend\public\index.html")
content = index_path.read_text(encoding="utf-8")

# 1. Update bone traversal in buildHumanoidAvatar to scale feminine hands and arms
bone_pattern = re.compile(r'          if \(child\.isBone\) \{[\s\S]*?child\.userData\.initialPosition = child\.position\.clone\(\);\s*\}')
new_bone_block = '''          if (child.isBone) {
            avatarRig.bones[child.name] = child;
            child.userData.initialRotation = child.rotation.clone();
            child.userData.initialQuaternion = child.quaternion.clone();
            child.userData.initialPosition = child.position.clone();

            // Feminine Proportion Refinement: slender, graceful hands, delicate wrists & forearms
            if (child.name === 'LeftHand' || child.name === 'RightHand') {
              child.scale.set(0.78, 0.84, 0.78); // Slender, petite feminine hands
            }
            if (child.name === 'LeftForeArm' || child.name === 'RightForeArm') {
              child.scale.set(0.84, 0.92, 0.84); // Smooth, slender feminine forearm
            }
            if (child.name === 'LeftArm' || child.name === 'RightArm') {
              child.scale.set(0.88, 0.96, 0.88); // Natural feminine shoulder & arm contour
            }
          }'''

content, c1 = bone_pattern.subn(new_bone_block, content)
print("Updated feminine bone scaling:", c1)

# 2. Update getRestingPose with poised, elegant clasped hands & calm, sweet facial demeanor
rest_pattern = re.compile(r'    function getRestingPose\(\) \{[\s\S]*?return \{[\s\S]*?\};\s*\}')
new_resting_pose = '''    function getRestingPose() {
      // Poised, calm & sweet professional posture (hands gently clasped over lower waist, warm friendly smile)
      return {
        head: [0, 0, 0],
        browY: 0,
        mouthOpen: 0,
        smile: 0.38,
        bodyShiftZ: 0,
        bodyLeanX: 0,
        leftArm: {
          shoulder: [1.207, -0.226, 1.280],
          elbow: [0.095, 0.596, 0.052],
          wrist: [0.026, -0.082, 0.374],
          fingerCurl: [0.25, 0.22, 0.22, 0.22, 0.22]
        },
        rightArm: {
          shoulder: [1.207, 0.226, -1.280],
          elbow: [0.095, -0.596, -0.052],
          wrist: [0.026, 0.082, -0.374],
          fingerCurl: [0.25, 0.22, 0.22, 0.22, 0.22]
        }
      };
    }'''

content, c2 = rest_pattern.subn(new_resting_pose, content)
print("Updated getRestingPose:", c2)

# 3. Update COMPUTED_POSES with calibrated coordinates (HELLO Namaste palms touching face-to-face)
poses_pattern = re.compile(r'    const COMPUTED_POSES = \{[\s\S]*?(?=    function getRestingPose)')
new_computed_poses = '''    const COMPUTED_POSES = {
      "HELLO": {
        "desc": "Namaste with both palms flush together at mid-chest, fingers straight up",
        "leftArm": {
          "shoulder": [1.154, 0.099, 0.901],
          "elbow": [-0.057, 0.255, 1.732],
          "wrist": [-0.828, 0.437, 0.572],
          "fingerCurl": [0.0, 0.0, 0.0, 0.0, 0.0]
        },
        "rightArm": {
          "shoulder": [1.154, -0.099, -0.901],
          "elbow": [-0.057, -0.255, -1.732],
          "wrist": [-0.828, -0.437, -0.572],
          "fingerCurl": [0.0, 0.0, 0.0, 0.0, 0.0]
        }
      },
      "YOU": {
        "desc": "Right index pointing smoothly forward at viewer",
        "rightArm": {
          "shoulder": [1.072, 0.335, -0.776],
          "elbow": [-0.106, 0.253, -1.157],
          "wrist": [-0.299, -0.140, -0.029],
          "fingerCurl": [0.70, 0.0, 0.85, 0.85, 0.85]
        }
      },
      "HOW": {
        "desc": "Both curved palms meeting in center and rotating open into inquiry",
        "leftArm": {
          "shoulder": [1.100, 0.080, 0.750],
          "elbow": [-0.040, 0.220, 1.450],
          "wrist": [-0.500, 0.350, 0.400],
          "fingerCurl": [0.20, 0.20, 0.20, 0.20, 0.20]
        },
        "rightArm": {
          "shoulder": [1.100, -0.080, -0.750],
          "elbow": [-0.040, -0.220, -1.450],
          "wrist": [-0.500, -0.350, -0.400],
          "fingerCurl": [0.20, 0.20, 0.20, 0.20, 0.20]
        }
      },
      "THANK_YOU_START": {
        "shoulder": [1.250, 0.434, -0.897],
        "elbow": [0.152, 0.336, -1.601],
        "wrist": [-0.341, -0.251, -0.204],
        "fingerCurl": [0.0, 0.0, 0.0, 0.0, 0.0]
      },
      "THANK_YOU_END": {
        "shoulder": [1.002, 0.314, -0.812],
        "elbow": [-0.072, 0.292, -1.182],
        "wrist": [-0.360, -0.152, -0.092],
        "fingerCurl": [0.0, 0.0, 0.0, 0.0, 0.0]
      },
      "WELCOME": {
        "desc": "Both open palms facing up and inviting forward",
        "leftArm": {
          "shoulder": [1.020, -0.150, 0.650],
          "elbow": [0.050, 0.180, 0.950],
          "wrist": [-0.150, 0.250, 0.350],
          "fingerCurl": [0.0, 0.0, 0.0, 0.0, 0.0]
        },
        "rightArm": {
          "shoulder": [1.020, 0.150, -0.650],
          "elbow": [0.050, -0.180, -0.950],
          "wrist": [-0.150, -0.250, -0.350],
          "fingerCurl": [0.0, 0.0, 0.0, 0.0, 0.0]
        }
      },
      "PLEASE": {
        "desc": "Both hands joined gently at chest in respectful appeal",
        "leftArm": {
          "shoulder": [1.154, 0.099, 0.901],
          "elbow": [-0.057, 0.255, 1.732],
          "wrist": [-0.828, 0.437, 0.572],
          "fingerCurl": [0.0, 0.0, 0.0, 0.0, 0.0]
        },
        "rightArm": {
          "shoulder": [1.154, -0.099, -0.901],
          "elbow": [-0.057, -0.255, -1.732],
          "wrist": [-0.828, -0.437, -0.572],
          "fingerCurl": [0.0, 0.0, 0.0, 0.0, 0.0]
        }
      },
      "NAME": {
        "desc": "H-handshape tapped respectfully",
        "rightArm": {
          "shoulder": [1.100, 0.280, -0.760],
          "elbow": [-0.050, 0.220, -1.250],
          "wrist": [-0.280, -0.120, -0.050],
          "fingerCurl": [0.70, 0.0, 0.0, 0.85, 0.85]
        }
      },
      "WHAT": {
        "desc": "Open palms facing up, questioning motion",
        "leftArm": {
          "shoulder": [0.950, -0.120, 0.580],
          "elbow": [0.020, 0.150, 0.880],
          "wrist": [-0.100, 0.200, 0.300],
          "fingerCurl": [0.0, 0.0, 0.0, 0.0, 0.0]
        },
        "rightArm": {
          "shoulder": [0.950, 0.120, -0.580],
          "elbow": [0.020, -0.150, -0.880],
          "wrist": [-0.100, -0.200, -0.300],
          "fingerCurl": [0.0, 0.0, 0.0, 0.0, 0.0]
        }
      },
      "WHERE": {
        "desc": "Right index upright in inquiry",
        "rightArm": {
          "shoulder": [1.150, 0.300, -0.750],
          "elbow": [-0.080, 0.220, -1.250],
          "wrist": [-0.250, -0.120, -0.050],
          "fingerCurl": [0.80, 0.0, 0.85, 0.85, 0.85]
        }
      },
      "ME": {
        "desc": "Right index finger pointing at center of chest",
        "rightArm": {
          "shoulder": [1.207, 0.679, 0.483],
          "elbow": [2.049, -0.314, 0.441],
          "wrist": [0.276, -0.518, 1.708],
          "fingerCurl": [0.70, 0.0, 0.85, 0.85, 0.85]
        }
      },
      "HELP": {
        "desc": "Left palm supports right fist as both lift gently",
        "leftArm": {
          "shoulder": [1.050, 0.050, 0.650],
          "elbow": [0.000, 0.150, 1.150],
          "wrist": [-0.350, 0.250, 0.400],
          "fingerCurl": [0.0, 0.0, 0.0, 0.0, 0.0]
        },
        "rightArm": {
          "shoulder": [1.080, -0.050, -0.680],
          "elbow": [0.020, -0.150, -1.180],
          "wrist": [-0.350, -0.250, -0.400],
          "fingerCurl": [0.0, 0.85, 0.85, 0.85, 0.85]
        }
      },
      "WATER": {
        "desc": "W-handshape gently near lips",
        "rightArm": {
          "shoulder": [1.220, 0.400, -0.850],
          "elbow": [0.120, 0.300, -1.550],
          "wrist": [-0.300, -0.220, -0.180],
          "fingerCurl": [0.80, 0.0, 0.0, 0.0, 0.85]
        }
      },
      "FOOD": {
        "desc": "Gathered fingertips tapping towards mouth",
        "rightArm": {
          "shoulder": [1.240, 0.420, -0.880],
          "elbow": [0.140, 0.320, -1.580],
          "wrist": [-0.320, -0.240, -0.200],
          "fingerCurl": [0.55, 0.55, 0.55, 0.55, 0.55]
        }
      },
      "HOSPITAL": {
        "desc": "Right fingers tracing cross on left upper arm",
        "leftArm": {
          "shoulder": [0.850, 0.080, 0.250],
          "elbow": [0.020, -0.020, 0.450],
          "wrist": [0.040, -0.200, -0.080],
          "fingerCurl": [0.20, 0.20, 0.20, 0.20, 0.20]
        },
        "rightArm": {
          "shoulder": [1.150, 0.350, -0.700],
          "elbow": [0.050, 0.250, -1.450],
          "wrist": [-0.400, -0.200, -0.250],
          "fingerCurl": [0.70, 0.0, 0.0, 0.70, 0.70]
        }
      },
      "DOCTOR": {
        "desc": "Right fingers tapping pulse on left wrist",
        "leftArm": {
          "shoulder": [1.100, 0.100, 0.800],
          "elbow": [-0.050, 0.200, 1.400],
          "wrist": [-0.600, 0.300, 0.450],
          "fingerCurl": [0.20, 0.20, 0.20, 0.20, 0.20]
        },
        "rightArm": {
          "shoulder": [1.120, -0.080, -0.780],
          "elbow": [-0.040, -0.180, -1.350],
          "wrist": [-0.550, -0.280, -0.420],
          "fingerCurl": [0.70, 0.0, 0.0, 0.70, 0.70]
        }
      },
      "TIME": {
        "desc": "Right index tapping wristwatch on left wrist",
        "leftArm": {
          "shoulder": [1.100, 0.100, 0.800],
          "elbow": [-0.050, 0.200, 1.400],
          "wrist": [-0.600, 0.300, 0.450],
          "fingerCurl": [0.20, 0.20, 0.20, 0.20, 0.20]
        },
        "rightArm": {
          "shoulder": [1.120, -0.080, -0.780],
          "elbow": [-0.040, -0.180, -1.350],
          "wrist": [-0.550, -0.280, -0.420],
          "fingerCurl": [0.70, 0.0, 0.85, 0.85, 0.85]
        }
      },
      "TODAY": {
        "desc": "Both hands moving downward firmly in front of body",
        "leftArm": {
          "shoulder": [0.980, -0.100, 0.600],
          "elbow": [0.020, 0.150, 0.900],
          "wrist": [-0.100, 0.200, 0.300],
          "fingerCurl": [0.0, 0.70, 0.70, 0.70, 0.0]
        },
        "rightArm": {
          "shoulder": [0.980, 0.100, -0.600],
          "elbow": [0.020, -0.150, -0.900],
          "wrist": [-0.100, -0.200, -0.300],
          "fingerCurl": [0.0, 0.70, 0.70, 0.70, 0.0]
        }
      },
      "GOOD": {
        "desc": "Right thumb upright in friendly approval",
        "rightArm": {
          "shoulder": [1.072, 0.335, -0.776],
          "elbow": [-0.106, 0.253, -1.157],
          "wrist": [-0.299, -0.140, -0.029],
          "fingerCurl": [0.0, 0.90, 0.90, 0.90, 0.90]
        }
      },
      "MORNING": {
        "desc": "Right arm rising like sun behind left horizon arm",
        "leftArm": {
          "shoulder": [1.050, 0.080, 0.700],
          "elbow": [-0.020, 0.180, 1.250],
          "wrist": [-0.400, 0.250, 0.350],
          "fingerCurl": [0.0, 0.0, 0.0, 0.0, 0.0]
        },
        "rightArm": {
          "shoulder": [1.180, 0.250, -0.750],
          "elbow": [0.100, 0.280, -1.500],
          "wrist": [-0.300, -0.200, -0.150],
          "fingerCurl": [0.0, 0.0, 0.0, 0.0, 0.0]
        }
      },
      "YES": {
        "desc": "Right fist nodding up and down affirmatively",
        "rightArm": {
          "shoulder": [1.120, 0.280, -0.780],
          "elbow": [-0.050, 0.220, -1.250],
          "wrist": [-0.280, -0.120, -0.050],
          "fingerCurl": [0.85, 0.85, 0.85, 0.85, 0.85]
        }
      },
      "NO": {
        "desc": "Right fingers snapping closed in polite refusal",
        "rightArm": {
          "shoulder": [1.100, 0.300, -0.760],
          "elbow": [-0.060, 0.240, -1.220],
          "wrist": [-0.260, -0.140, -0.040],
          "fingerCurl": [0.50, 0.50, 0.50, 0.85, 0.85]
        }
      },
      "INDIA": {
        "desc": "Right thumb touching forehead center bindi spot",
        "rightArm": {
          "shoulder": [1.280, 0.380, -0.850],
          "elbow": [0.180, 0.350, -1.650],
          "wrist": [-0.280, -0.250, -0.220],
          "fingerCurl": [0.0, 0.85, 0.85, 0.85, 0.85]
        }
      },
      "NICE": {
        "desc": "Right flat palm smoothly gliding across left palm",
        "leftArm": {
          "shoulder": [1.050, 0.080, 0.700],
          "elbow": [-0.020, 0.180, 1.250],
          "wrist": [-0.400, 0.250, 0.350],
          "fingerCurl": [0.0, 0.0, 0.0, 0.0, 0.0]
        },
        "rightArm": {
          "shoulder": [1.080, -0.060, -0.720],
          "elbow": [0.000, -0.160, -1.220],
          "wrist": [-0.380, -0.240, -0.380],
          "fingerCurl": [0.0, 0.0, 0.0, 0.0, 0.0]
        }
      },
      "MEET": {
        "desc": "Both upright index fingers moving together until they meet in center",
        "leftArm": {
          "shoulder": [1.140, 0.100, 0.850],
          "elbow": [-0.050, 0.240, 1.600],
          "wrist": [-0.750, 0.400, 0.520],
          "fingerCurl": [0.70, 0.0, 0.85, 0.85, 0.85]
        },
        "rightArm": {
          "shoulder": [1.140, -0.100, -0.850],
          "elbow": [-0.050, -0.240, -1.600],
          "wrist": [-0.750, -0.400, -0.520],
          "fingerCurl": [0.70, 0.0, 0.85, 0.85, 0.85]
        }
      }
    };\n\n'''

content, c3 = poses_pattern.subn(new_computed_poses, content)
print("Updated COMPUTED_POSES:", c3)

# 4. Update applyArmRotations to apply absolute Euler rotations directly to bones
apply_arm_pattern = re.compile(r'    function applyArmRotations\(isLeft, armPose\) \{[\s\S]*?(?=    function applyPoseToAvatar)')
new_apply_arm = '''    function applyArmRotations(isLeft, armPose) {
      if (!avatarRig.bones || !armPose) return;
      const bones = avatarRig.bones;
      const prefix = isLeft ? 'Left' : 'Right';
      const armBone = bones[prefix + 'Arm'];
      const foreArmBone = bones[prefix + 'ForeArm'];
      const handBone = bones[prefix + 'Hand'];

      if (armBone && armPose.shoulder) {
        armBone.rotation.set(armPose.shoulder[0], armPose.shoulder[1], armPose.shoulder[2]);
      }
      if (foreArmBone && armPose.elbow) {
        foreArmBone.rotation.set(armPose.elbow[0], armPose.elbow[1], armPose.elbow[2]);
      }
      if (handBone && armPose.wrist) {
        handBone.rotation.set(armPose.wrist[0], armPose.wrist[1], armPose.wrist[2]);
      }

      if (armPose.fingerCurl) {
        applyFingerCurlBones(prefix, armPose.fingerCurl, isLeft);
      }
    }

'''

content, c4 = apply_arm_pattern.subn(new_apply_arm, content)
print("Updated applyArmRotations:", c4)

# 5. Update applyPoseToAvatar for sweet, calm, serene female expressions
apply_pose_pattern = re.compile(r'      // Dynamic blendshape expressions[\s\S]*?(?=      // Left & Right Arm Articulations)')
new_expressions = '''      // Dynamic calm, sweet, radiant female expressions (gentle smile, warm eyes, serene brows)
      const smileVal = pose.smile !== undefined ? Math.max(pose.smile, 0.35) : 0.38;
      setMorph('mouthSmile', smileVal);
      setMorph('mouthSmileLeft', smileVal);
      setMorph('mouthSmileRight', smileVal);
      setMorph('cheekSquintLeft', smileVal * 0.65);
      setMorph('cheekSquintRight', smileVal * 0.65);
      setMorph('eyeSquintLeft', smileVal * 0.22);
      setMorph('eyeSquintRight', smileVal * 0.22);

      const mouthOpenVal = pose.mouthOpen || 0.0;
      setMorph('jawOpen', mouthOpenVal);
      setMorph('mouthOpen', mouthOpenVal * 0.7);

      const browVal = pose.browY || 0.0;
      if (browVal > 0) {
        setMorph('browInnerUp', Math.min(1.0, 0.16 + browVal * 10));
        setMorph('browOuterUpLeft', Math.min(1.0, browVal * 8));
        setMorph('browOuterUpRight', Math.min(1.0, browVal * 8));
        setMorph('browDownLeft', 0);
        setMorph('browDownRight', 0);
      } else if (browVal < 0) {
        setMorph('browDownLeft', Math.min(1.0, -browVal * 14));
        setMorph('browDownRight', Math.min(1.0, -browVal * 14));
        setMorph('browInnerUp', 0);
      } else {
        // Serene, gentle welcoming resting eyebrows
        setMorph('browInnerUp', 0.14);
        setMorph('browOuterUpLeft', 0.05);
        setMorph('browOuterUpRight', 0.05);
        setMorph('browDownLeft', 0);
        setMorph('browDownRight', 0);
      }
'''

content, c5 = apply_pose_pattern.subn(new_expressions, content)
print("Updated sweet female expressions:", c5)

index_path.write_text(content, encoding="utf-8")
print("frontend/public/index.html updated successfully with all enhancements!")
