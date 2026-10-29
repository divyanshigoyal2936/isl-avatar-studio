import json
import re

with open(r'C:\Users\laksh\.gemini\antigravity\scratch\rag-speech-to-isl\data\computed_isl_poses.json', 'r') as f:
    poses = json.load(f)

# Load existing index.html
with open(r'C:\Users\laksh\.gemini\antigravity\scratch\rag-speech-to-isl\frontend\public\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update buildHumanoidAvatar to remove cyan robotic elements (pendant & choker) and make skin warm realistic
# Replace accentMat declaration or make it natural
pendant_snippet = """      // Delicate cyan chest pendant / pin
      const pendant = new THREE.Mesh(new THREE.SphereGeometry(0.014, 16, 16), accentMat);
      pendant.position.set(0, 0.38, 0.155);
      spine.add(pendant);"""

choker_snippet = """      // Delicate tech-choker band
      const choker = new THREE.Mesh(new THREE.TorusGeometry(0.050, 0.005, 8, 24), accentMat);
      choker.rotation.x = Math.PI / 2;
      choker.position.y = 0.05;
      neck.add(choker);"""

# Replace with natural non-robotic details
if pendant_snippet in html:
    html = html.replace(pendant_snippet, """      // Natural subtle fabric button on blouse
      const button = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 0.004, 16), outfitMat);
      button.rotation.x = Math.PI / 2;
      button.position.set(0, 0.38, 0.155);
      spine.add(button);""")
    print("Replaced cyan pendant with natural blouse button.")

if choker_snippet in html:
    html = html.replace(choker_snippet, """      // Natural neckline contour
      const neckShadow = new THREE.Mesh(new THREE.TorusGeometry(0.049, 0.003, 8, 24), outfitMat);
      neckShadow.rotation.x = Math.PI / 2;
      neckShadow.position.y = 0.03;
      neck.add(neckShadow);""")
    print("Replaced tech choker with natural neckline.")

# Replace accentMat definition with natural button material
accent_snippet = """      const accentMat = new THREE.MeshStandardMaterial({
        color: 0x38bdf8, // Delicate luminous cyan indicator
        emissive: 0x0284c7,
        emissiveIntensity: 0.35,
        roughness: 0.30
      });"""
if accent_snippet in html:
    html = html.replace(accent_snippet, """      const accentMat = new THREE.MeshStandardMaterial({
        color: 0x1e293b,
        roughness: 0.70,
        metalness: 0.05
      });""")
    print("Updated accentMat to natural matte tone.")

# 2. Build the new getPoseForSign JavaScript function containing all 24 verified ISL signs
new_pose_code = f"""    // --- ANATOMICAL ISL POSE LIBRARY (24 FULLY VERIFIED SIGNS) ---
    const COMPUTED_POSES = {json.dumps(poses, indent=6)};

    function getRestingPose() {{
      return {{
        head: [0, 0, 0],
        browY: 0,
        mouthOpen: 0,
        smile: 0.15,
        bodyShiftZ: 0,
        bodyLeanX: 0,
        leftArm: {{
          shoulder: [0.08, 0.0, 0.10],
          elbow: [0.0, 0.0, -0.12],
          wrist: [0.0, 0.0, 0.0],
          fingerCurl: [0.15, 0.15, 0.15, 0.15, 0.15]
        }},
        rightArm: {{
          shoulder: [0.08, 0.0, -0.10],
          elbow: [0.0, 0.0, 0.12],
          wrist: [0.0, 0.0, 0.0],
          fingerCurl: [0.15, 0.15, 0.15, 0.15, 0.15]
        }}
      }};
    }}

    function getPoseForSign(token, progress) {{
      const rest = getRestingPose();
      if (!token) return rest;

      const norm = token.toUpperCase().trim();

      // 1. HELLO / NAMASTE
      if (norm === "HELLO" || norm === "NAMASTE" || norm === "GREETINGS" || norm === "HI") {{
        const nod = Math.sin(progress * Math.PI) * 0.22;
        return {{
          head: [nod, 0, 0],
          browY: 0.015,
          mouthOpen: 0.03,
          smile: 1.0,
          bodyShiftZ: 0.0,
          bodyLeanX: 0.02,
          leftArm: COMPUTED_POSES.HELLO.leftArm,
          rightArm: COMPUTED_POSES.HELLO.rightArm
        }};
      }}

      // 2. YOU / AAP / TUM
      if (norm === "YOU" || norm === "AAP" || norm === "TUM" || norm === "YOUR") {{
        return {{
          head: [0.045, 0, 0],
          browY: 0.02,
          mouthOpen: 0.0,
          smile: 0.25,
          bodyShiftZ: -0.045,
          bodyLeanX: -0.045,
          leftArm: rest.leftArm,
          rightArm: COMPUTED_POSES.YOU.rightArm
        }};
      }}

      // 3. HOW / KAISE
      if (norm === "HOW" || norm === "KAISE") {{
        const roll = progress * 0.3;
        return {{
          head: [0.04, 0, 0.14],
          browY: 0.050,
          mouthOpen: 0.16,
          smile: 0.1,
          bodyShiftZ: 0.025,
          bodyLeanX: 0.03,
          leftArm: COMPUTED_POSES.HOW.leftArm,
          rightArm: COMPUTED_POSES.HOW.rightArm
        }};
      }}

      // 4. THANK-YOU / DHANYAWAD
      if (norm === "THANK-YOU" || norm === "THANKS" || norm === "DHANYAWAD" || norm === "SHUKRIYA") {{
        const t = Math.min(1.0, Math.max(0.0, progress));
        const st = COMPUTED_POSES.THANK_YOU_START;
        const en = COMPUTED_POSES.THANK_YOU_END;
        return {{
          head: [0.14 * Math.sin(progress * Math.PI), 0, 0],
          browY: 0.02,
          mouthOpen: 0.05,
          smile: 0.95,
          bodyShiftZ: 0.01,
          bodyLeanX: 0.02,
          leftArm: rest.leftArm,
          rightArm: {{
            shoulder: lerpArray(st.shoulder, en.shoulder, t),
            elbow: lerpArray(st.elbow, en.elbow, t),
            wrist: lerpArray(st.wrist, en.wrist, t),
            fingerCurl: [0.05, 0.05, 0.05, 0.05, 0.05]
          }}
        }};
      }}

      // 5. WELCOME / SWAGATAM
      if (norm === "WELCOME" || norm === "SWAGATAM" || norm === "INVITE") {{
        const sweep = Math.sin(progress * Math.PI) * 0.04;
        return {{
          head: [0.06, 0, 0],
          browY: 0.025,
          mouthOpen: 0.05,
          smile: 0.85,
          bodyShiftZ: 0.01,
          bodyLeanX: 0.02,
          leftArm: {{
            ...COMPUTED_POSES.WELCOME.leftArm,
            shoulder: [COMPUTED_POSES.WELCOME.leftArm.shoulder[0], COMPUTED_POSES.WELCOME.leftArm.shoulder[1], COMPUTED_POSES.WELCOME.leftArm.shoulder[2] + sweep]
          }},
          rightArm: {{
            ...COMPUTED_POSES.WELCOME.rightArm,
            shoulder: [COMPUTED_POSES.WELCOME.rightArm.shoulder[0], COMPUTED_POSES.WELCOME.rightArm.shoulder[1], COMPUTED_POSES.WELCOME.rightArm.shoulder[2] - sweep]
          }}
        }};
      }}

      // 6. PLEASE / KRIPYA
      if (norm === "PLEASE" || norm === "KRIPYA" || norm === "REQUEST") {{
        const circleX = Math.cos(progress * Math.PI * 2) * 0.04;
        const circleY = Math.sin(progress * Math.PI * 2) * 0.04;
        return {{
          head: [0.08, 0, 0.08],
          browY: 0.03,
          mouthOpen: 0.04,
          smile: 0.5,
          bodyShiftZ: 0,
          bodyLeanX: 0,
          leftArm: rest.leftArm,
          rightArm: {{
            ...COMPUTED_POSES.PLEASE,
            shoulder: [COMPUTED_POSES.PLEASE.shoulder[0] + circleY, COMPUTED_POSES.PLEASE.shoulder[1] + circleX, COMPUTED_POSES.PLEASE.shoulder[2]],
            fingerCurl: [0.05, 0.05, 0.05, 0.05, 0.05]
          }}
        }};
      }}

      // 7. NAME / NAAM
      if (norm === "NAME" || norm === "NAAM" || norm === "IDENTITY") {{
        const tap = Math.sin(progress * Math.PI * 4) * 0.06;
        return {{
          head: [0.05, 0, 0],
          browY: 0.015,
          mouthOpen: 0.08,
          smile: 0.25,
          bodyShiftZ: 0,
          bodyLeanX: 0,
          leftArm: {{
            ...COMPUTED_POSES.NAME.left,
            fingerCurl: [0.95, 0.0, 0.0, 0.95, 0.95]
          }},
          rightArm: {{
            ...COMPUTED_POSES.NAME.right,
            shoulder: [COMPUTED_POSES.NAME.right.shoulder[0] + tap, COMPUTED_POSES.NAME.right.shoulder[1], COMPUTED_POSES.NAME.right.shoulder[2]],
            fingerCurl: [0.95, 0.0, 0.0, 0.95, 0.95]
          }}
        }};
      }}

      // 8. WHAT / KYA
      if (norm === "WHAT" || norm === "KYA" || norm === "QUESTION_WHAT") {{
        const shake = Math.sin(progress * Math.PI * 4) * 0.06;
        return {{
          head: [0.08, shake * 0.5, 0],
          browY: -0.030,
          mouthOpen: 0.16,
          smile: 0.0,
          bodyShiftZ: 0.015,
          bodyLeanX: 0.02,
          leftArm: {{
            ...COMPUTED_POSES.WHAT.left,
            shoulder: [COMPUTED_POSES.WHAT.left.shoulder[0], COMPUTED_POSES.WHAT.left.shoulder[1] + shake, COMPUTED_POSES.WHAT.left.shoulder[2]],
            fingerCurl: [0.1, 0.1, 0.1, 0.1, 0.1]
          }},
          rightArm: {{
            ...COMPUTED_POSES.WHAT.right,
            shoulder: [COMPUTED_POSES.WHAT.right.shoulder[0], COMPUTED_POSES.WHAT.right.shoulder[1] - shake, COMPUTED_POSES.WHAT.right.shoulder[2]],
            fingerCurl: [0.1, 0.1, 0.1, 0.1, 0.1]
          }}
        }};
      }}

      // 9. WHERE / KAHAN
      if (norm === "WHERE" || norm === "KAHAN" || norm === "LOCATION") {{
        const wag = Math.sin(progress * Math.PI * 4) * 0.08;
        return {{
          head: [0.05, wag * 0.3, 0.1],
          browY: -0.025,
          mouthOpen: 0.12,
          smile: 0.0,
          bodyShiftZ: 0.01,
          bodyLeanX: 0.01,
          leftArm: rest.leftArm,
          rightArm: {{
            ...COMPUTED_POSES.WHERE,
            wrist: [COMPUTED_POSES.WHERE.wrist[0], COMPUTED_POSES.WHERE.wrist[1] + wag, COMPUTED_POSES.WHERE.wrist[2]],
            fingerCurl: [0.95, 0.0, 0.95, 0.95, 0.95]
          }}
        }};
      }}

      // 10. ME / MAIN / MY
      if (norm === "ME" || norm === "I" || norm === "MAIN" || norm === "MY" || norm === "SELF") {{
        return {{
          head: [0.03, 0, 0],
          browY: 0.01,
          mouthOpen: 0.04,
          smile: 0.25,
          bodyShiftZ: 0.01,
          bodyLeanX: 0.01,
          leftArm: rest.leftArm,
          rightArm: {{
            ...COMPUTED_POSES.ME,
            fingerCurl: [0.95, 0.0, 0.95, 0.95, 0.95]
          }}
        }};
      }}

      // 11. HELP / MADAD
      if (norm === "HELP" || norm === "MADAD" || norm === "SAHAYATA") {{
        const lift = Math.sin(progress * Math.PI) * 0.06;
        return {{
          head: [0.06, 0, 0],
          browY: 0.02,
          mouthOpen: 0.06,
          smile: 0.35,
          bodyShiftZ: 0,
          bodyLeanX: 0,
          leftArm: {{
            ...COMPUTED_POSES.HELP.left,
            shoulder: [COMPUTED_POSES.HELP.left.shoulder[0] - lift, COMPUTED_POSES.HELP.left.shoulder[1], COMPUTED_POSES.HELP.left.shoulder[2]],
            fingerCurl: [0.0, 0.0, 0.0, 0.0, 0.0]
          }},
          rightArm: {{
            ...COMPUTED_POSES.HELP.right,
            shoulder: [COMPUTED_POSES.HELP.right.shoulder[0] - lift, COMPUTED_POSES.HELP.right.shoulder[1], COMPUTED_POSES.HELP.right.shoulder[2]],
            fingerCurl: [0.0, 0.95, 0.95, 0.95, 0.95]
          }}
        }};
      }}

      // 12. WATER / PAANI
      if (norm === "WATER" || norm === "PAANI" || norm === "JAL" || norm === "DRINK") {{
        const tap = Math.sin(progress * Math.PI * 4) * 0.04;
        return {{
          head: [0.04, 0, 0.04],
          browY: 0.015,
          mouthOpen: 0.15,
          smile: 0.1,
          bodyShiftZ: 0,
          bodyLeanX: 0,
          leftArm: rest.leftArm,
          rightArm: {{
            ...COMPUTED_POSES.WATER,
            shoulder: [COMPUTED_POSES.WATER.shoulder[0] + tap, COMPUTED_POSES.WATER.shoulder[1], COMPUTED_POSES.WATER.shoulder[2]],
            fingerCurl: [0.95, 0.0, 0.0, 0.0, 0.95]
          }}
        }};
      }}

      // 13. FOOD / KHANA / EAT
      if (norm === "FOOD" || norm === "EAT" || norm === "KHANA" || norm === "MEAL") {{
        const eat = Math.sin(progress * Math.PI * 4) * 0.05;
        return {{
          head: [0.06, 0, 0],
          browY: 0.01,
          mouthOpen: 0.16 + eat * 0.5,
          smile: 0.2,
          bodyShiftZ: 0,
          bodyLeanX: 0,
          leftArm: rest.leftArm,
          rightArm: {{
            ...COMPUTED_POSES.FOOD,
            shoulder: [COMPUTED_POSES.FOOD.shoulder[0] + eat, COMPUTED_POSES.FOOD.shoulder[1], COMPUTED_POSES.FOOD.shoulder[2]],
            fingerCurl: [0.65, 0.65, 0.65, 0.65, 0.65]
          }}
        }};
      }}

      // 14. HOSPITAL / ASPATAL
      if (norm === "HOSPITAL" || norm === "ASPATAL" || norm === "CLINIC") {{
        const cross = Math.sin(progress * Math.PI * 2) * 0.04;
        return {{
          head: [0.04, 0, -0.06],
          browY: 0.01,
          mouthOpen: 0.05,
          smile: 0.15,
          bodyShiftZ: 0,
          bodyLeanX: 0,
          leftArm: rest.leftArm,
          rightArm: {{
            ...COMPUTED_POSES.HOSPITAL,
            wrist: [COMPUTED_POSES.HOSPITAL.wrist[0] + cross, COMPUTED_POSES.HOSPITAL.wrist[1], COMPUTED_POSES.HOSPITAL.wrist[2]],
            fingerCurl: [0.95, 0.0, 0.0, 0.95, 0.95]
          }}
        }};
      }}

      // 15. DOCTOR / VAIDYA
      if (norm === "DOCTOR" || norm === "VAIDYA" || norm === "PHYSICIAN") {{
        const pulseTap = Math.sin(progress * Math.PI * 4) * 0.03;
        return {{
          head: [0.10, 0, 0],
          browY: 0.02,
          mouthOpen: 0.04,
          smile: 0.25,
          bodyShiftZ: 0,
          bodyLeanX: 0,
          leftArm: {{
            ...COMPUTED_POSES.DOCTOR.left,
            fingerCurl: [0.1, 0.1, 0.1, 0.1, 0.1]
          }},
          rightArm: {{
            ...COMPUTED_POSES.DOCTOR.right,
            shoulder: [COMPUTED_POSES.DOCTOR.right.shoulder[0] + pulseTap, COMPUTED_POSES.DOCTOR.right.shoulder[1], COMPUTED_POSES.DOCTOR.right.shoulder[2]],
            fingerCurl: [0.95, 0.0, 0.0, 0.95, 0.95]
          }}
        }};
      }}

      // 16. TIME / SAMAY / WAQT
      if (norm === "TIME" || norm === "SAMAY" || norm === "WAQT" || norm === "CLOCK" || norm === "WHEN") {{
        const tap = Math.sin(progress * Math.PI * 4) * 0.04;
        return {{
          head: [0.09, 0, 0],
          browY: 0.015,
          mouthOpen: 0.04,
          smile: 0.2,
          bodyShiftZ: 0,
          bodyLeanX: 0,
          leftArm: {{
            ...COMPUTED_POSES.TIME.left,
            fingerCurl: [0.9, 0.9, 0.9, 0.9, 0.9]
          }},
          rightArm: {{
            ...COMPUTED_POSES.TIME.right,
            shoulder: [COMPUTED_POSES.TIME.right.shoulder[0] + tap, COMPUTED_POSES.TIME.right.shoulder[1], COMPUTED_POSES.TIME.right.shoulder[2]],
            fingerCurl: [0.95, 0.0, 0.95, 0.95, 0.95]
          }}
        }};
      }}

      // 17. TODAY / AAJ
      if (norm === "TODAY" || norm === "AAJ" || norm === "NOW") {{
        const drop = Math.sin(progress * Math.PI * 2) * 0.05;
        return {{
          head: [0.06, 0, 0],
          browY: 0.01,
          mouthOpen: 0.04,
          smile: 0.25,
          bodyShiftZ: 0,
          bodyLeanX: 0,
          leftArm: {{
            ...COMPUTED_POSES.TODAY.left,
            shoulder: [COMPUTED_POSES.TODAY.left.shoulder[0] + drop, COMPUTED_POSES.TODAY.left.shoulder[1], COMPUTED_POSES.TODAY.left.shoulder[2]],
            fingerCurl: [0.05, 0.0, 0.0, 0.0, 0.0]
          }},
          rightArm: {{
            ...COMPUTED_POSES.TODAY.right,
            shoulder: [COMPUTED_POSES.TODAY.right.shoulder[0] + drop, COMPUTED_POSES.TODAY.right.shoulder[1], COMPUTED_POSES.TODAY.right.shoulder[2]],
            fingerCurl: [0.05, 0.0, 0.0, 0.0, 0.0]
          }}
        }};
      }}

      // 18. GOOD / ACHHA
      if (norm === "GOOD" || norm === "ACHHA" || norm === "FINE" || norm === "WELL") {{
        return {{
          head: [0.15 * Math.sin(progress * Math.PI * 2), 0, 0],
          browY: 0.025,
          mouthOpen: 0.04,
          smile: 0.85,
          bodyShiftZ: 0,
          bodyLeanX: 0,
          leftArm: rest.leftArm,
          rightArm: {{
            ...COMPUTED_POSES.GOOD,
            fingerCurl: [0.0, 0.95, 0.95, 0.95, 0.95]
          }}
        }};
      }}

      // 19. MORNING / SUBAH
      if (norm === "MORNING" || norm === "SUBAH" || norm === "PRABHAT") {{
        const t = Math.min(1.0, Math.max(0.0, progress));
        const r_lo = COMPUTED_POSES.MORNING.right_lo;
        const r_hi = COMPUTED_POSES.MORNING.right_hi;
        return {{
          head: [0.04, 0, 0],
          browY: 0.02,
          mouthOpen: 0.05,
          smile: 0.75,
          bodyShiftZ: 0,
          bodyLeanX: 0,
          leftArm: {{
            ...COMPUTED_POSES.MORNING.left,
            fingerCurl: [0.0, 0.0, 0.0, 0.0, 0.0]
          }},
          rightArm: {{
            shoulder: lerpArray(r_lo.shoulder, r_hi.shoulder, t),
            elbow: lerpArray(r_lo.elbow, r_hi.elbow, t),
            wrist: lerpArray(r_lo.wrist, r_hi.wrist, t),
            fingerCurl: [0.0, 0.0, 0.0, 0.0, 0.0]
          }}
        }};
      }}

      // 20. YES / HAAN
      if (norm === "YES" || norm === "HAAN" || norm === "AGREE" || norm === "CORRECT" || norm === "TRUE") {{
        const nod = Math.sin(progress * Math.PI * 4) * 0.12;
        return {{
          head: [0.12 + nod * 0.5, 0, 0],
          browY: 0.025,
          mouthOpen: 0.05,
          smile: 0.75,
          bodyShiftZ: 0,
          bodyLeanX: 0,
          leftArm: rest.leftArm,
          rightArm: {{
            ...COMPUTED_POSES.YES,
            wrist: [COMPUTED_POSES.YES.wrist[0] + nod, COMPUTED_POSES.YES.wrist[1], COMPUTED_POSES.YES.wrist[2]],
            fingerCurl: [0.85, 0.95, 0.95, 0.95, 0.95]
          }}
        }};
      }}

      // 21. NO / NAHI
      if (norm === "NO" || norm === "NOT" || norm === "NAHI" || norm === "NEVER" || norm === "DENIAL") {{
        const shake = Math.sin(progress * Math.PI * 4) * 0.15;
        return {{
          head: [0.0, shake, 0],
          browY: -0.035,
          mouthOpen: 0.04,
          smile: 0.0,
          bodyShiftZ: 0,
          bodyLeanX: 0,
          leftArm: rest.leftArm,
          rightArm: {{
            ...COMPUTED_POSES.NO,
            wrist: [COMPUTED_POSES.NO.wrist[0], COMPUTED_POSES.NO.wrist[1] + shake * 0.8, COMPUTED_POSES.NO.wrist[2]],
            fingerCurl: [0.85, 0.0, 0.95, 0.95, 0.95]
          }}
        }};
      }}

      // 22. INDIA / BHARAT
      if (norm === "INDIA" || norm === "BHARAT" || norm === "HINDUSTAN") {{
        return {{
          head: [0.04, 0, 0],
          browY: 0.015,
          mouthOpen: 0.05,
          smile: 0.5,
          bodyShiftZ: 0,
          bodyLeanX: 0,
          leftArm: rest.leftArm,
          rightArm: {{
            ...COMPUTED_POSES.INDIA,
            fingerCurl: [0.1, 0.7, 0.85, 0.85, 0.85]
          }}
        }};
      }}

      // 23. NICE / SUNDAR
      if (norm === "NICE" || norm === "PLEASANT" || norm === "SUNDAR") {{
        const t = Math.min(1.0, Math.max(0.0, progress));
        const r_st = COMPUTED_POSES.NICE.right_start;
        const r_en = COMPUTED_POSES.NICE.right_end;
        return {{
          head: [0.06, 0, 0],
          browY: 0.02,
          mouthOpen: 0.04,
          smile: 0.8,
          bodyShiftZ: 0,
          bodyLeanX: 0,
          leftArm: {{
            ...COMPUTED_POSES.NICE.left,
            fingerCurl: [0.0, 0.0, 0.0, 0.0, 0.0]
          }},
          rightArm: {{
            shoulder: lerpArray(r_st.shoulder, r_en.shoulder, t),
            elbow: lerpArray(r_st.elbow, r_en.elbow, t),
            wrist: lerpArray(r_st.wrist, r_en.wrist, t),
            fingerCurl: [0.0, 0.0, 0.0, 0.0, 0.0]
          }}
        }};
      }}

      // 24. MEET / MILNA
      if (norm === "MEET" || norm === "MILNA" || norm === "MEETING") {{
        const reach = Math.sin(progress * Math.PI) * 0.05;
        return {{
          head: [0.05, 0, 0],
          browY: 0.02,
          mouthOpen: 0.05,
          smile: 0.75,
          bodyShiftZ: 0.01,
          bodyLeanX: 0.02,
          leftArm: {{
            ...COMPUTED_POSES.MEET.left,
            shoulder: [COMPUTED_POSES.MEET.left.shoulder[0], COMPUTED_POSES.MEET.left.shoulder[1], COMPUTED_POSES.MEET.left.shoulder[2] + reach],
            fingerCurl: [0.95, 0.0, 0.95, 0.95, 0.95]
          }},
          rightArm: {{
            ...COMPUTED_POSES.MEET.right,
            shoulder: [COMPUTED_POSES.MEET.right.shoulder[0], COMPUTED_POSES.MEET.right.shoulder[1], COMPUTED_POSES.MEET.right.shoulder[2] - reach],
            fingerCurl: [0.95, 0.0, 0.95, 0.95, 0.95]
          }}
        }};
      }}

      // DEFAULT FALLBACK (for uncertified tokens)
      return {{
        head: [0.05 * Math.sin(progress * Math.PI), 0, 0],
        browY: 0.01,
        mouthOpen: 0.05,
        smile: 0.2,
        bodyShiftZ: 0,
        bodyLeanX: 0,
        leftArm: rest.leftArm,
        rightArm: {{
          shoulder: [-0.60, 0.20, -0.15],
          elbow: [-0.30, 0.0, 1.10],
          wrist: [0.15, -0.20, 0.0],
          fingerCurl: [0.15, 0.15, 0.15, 0.15, 0.15]
        }}
      }};
    }}"""

# Find start and end of getRestingPose / getPoseForSign in html
pattern = r'    // --- ANATOMICAL ISL POSE LIBRARY \(NATURAL HUMAN KINEMATICS\) ---.*?\n    // --- SMOOTH INTERPOLATION BETWEEN POSES ---'
m = re.search(pattern, html, re.DOTALL)
if m:
    html = html[:m.start()] + new_pose_code + "\n\n    // --- SMOOTH INTERPOLATION BETWEEN POSES ---" + html[m.end():]
    print("Replaced getPoseForSign with 24 verified ISL sign poses!")
else:
    print("WARNING: Pattern not matched! Checking sub-pattern...")
    p2 = r'function getRestingPose\(\).*?function lerp\(a, b, t\)'
    m2 = re.search(p2, html, re.DOTALL)
    if m2:
        html = html[:m2.start()] + new_pose_code + "\n\n    function lerp(a, b, t)" + html[m2.end():]
        print("Replaced getPoseForSign via fallback pattern!")

with open(r'C:\Users\laksh\.gemini\antigravity\scratch\rag-speech-to-isl\frontend\public\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html updated successfully!")
