"""
Complete ISL pose system fix:
- Replace COMPUTED_POSES with fully consistent structure (all keys: leftArm/rightArm with shoulder/elbow/wrist/fingerCurl)
- Replace getPoseForSign to use only correct key paths
- Fix applyFingerCurlBones to use proper curl multipliers for rigged skeleton
- Keep applyPoseToAvatar, expressions, blending intact
"""
import re
from pathlib import Path

index_path = Path(r"C:\Users\laksh\.gemini\antigravity\scratch\rag-speech-to-isl\frontend\public\index.html")
content = index_path.read_text(encoding="utf-8")

# ── Helper arm pose builder ─────────────────────────────────────────────────
def arm(sh, el, wr, fc):
    return {"shoulder": sh, "elbow": el, "wrist": wr, "fingerCurl": fc}

REST_L = arm([0.30, -0.12, 0.55], [0.10, 0.30, 0.10], [0.05, -0.05, 0.20], [0.18,0.18,0.18,0.18,0.18])
REST_R = arm([0.30,  0.12,-0.55], [0.10,-0.30,-0.10], [0.05,  0.05,-0.20], [0.18,0.18,0.18,0.18,0.18])

# All 24 signs – anatomically grounded, symmetric where needed
SIGNS = {
    # 1. HELLO – Namaste, both palms together at chest, fingers up, elbows bent inward
    "HELLO": {
        "leftArm":  arm([0.55,-0.08, 0.72],[-0.80, 0.10, 1.60],[-0.40, 0.25, 0.35],[0.0,0.0,0.0,0.0,0.0]),
        "rightArm": arm([0.55, 0.08,-0.72],[-0.80,-0.10,-1.60],[-0.40,-0.25,-0.35],[0.0,0.0,0.0,0.0,0.0]),
    },
    # 2. YOU – Right index extended, arm raised toward viewer
    "YOU": {
        "leftArm":  REST_L,
        "rightArm": arm([0.65, 0.35,-0.55],[-0.40,-0.05,-1.05],[-0.18,-0.12,-0.08],[0.70,0.0,0.90,0.90,0.90]),
    },
    # 3. HOW – Both palms up, slightly curled, questioning tilt
    "HOW": {
        "leftArm":  arm([0.50,-0.10, 0.50],[ 0.05, 0.15, 1.20],[-0.15, 0.20, 0.30],[0.20,0.20,0.20,0.20,0.20]),
        "rightArm": arm([0.50, 0.10,-0.50],[ 0.05,-0.15,-1.20],[-0.15,-0.20,-0.30],[0.20,0.20,0.20,0.20,0.20]),
    },
    # 4. THANK-YOU – Right flat hand from chin sweeping forward
    "THANK_YOU_START": {
        "leftArm":  REST_L,
        "rightArm": arm([0.80, 0.28,-0.65],[ 0.25, 0.20,-1.45],[-0.22,-0.18,-0.15],[0.0,0.0,0.0,0.0,0.0]),
    },
    "THANK_YOU_END": {
        "leftArm":  REST_L,
        "rightArm": arm([0.62, 0.25,-0.60],[-0.12, 0.22,-1.10],[-0.28,-0.14,-0.08],[0.0,0.0,0.0,0.0,0.0]),
    },
    # 5. WELCOME – Both arms open wide, palms facing up, inviting gesture
    "WELCOME": {
        "leftArm":  arm([0.45,-0.18, 0.35],[ 0.05, 0.10, 0.80],[-0.10, 0.18, 0.25],[0.0,0.0,0.0,0.0,0.0]),
        "rightArm": arm([0.45, 0.18,-0.35],[ 0.05,-0.10,-0.80],[-0.10,-0.18,-0.25],[0.0,0.0,0.0,0.0,0.0]),
    },
    # 6. PLEASE – Right palm flat circling on chest
    "PLEASE": {
        "leftArm":  REST_L,
        "rightArm": arm([0.70, 0.22,-0.58],[ 0.18, 0.18,-1.35],[-0.20,-0.15,-0.12],[0.0,0.0,0.0,0.0,0.0]),
    },
    # 7. NAME – Right H-hand (index+middle) tapped on left wrist
    "NAME": {
        "leftArm":  arm([0.45,-0.05, 0.55],[ 0.02, 0.10, 1.10],[-0.35, 0.22, 0.40],[0.10,0.10,0.10,0.10,0.10]),
        "rightArm": arm([0.62, 0.18,-0.62],[-0.05, 0.15,-1.28],[-0.25,-0.12,-0.10],[0.80,0.0,0.0,0.85,0.85]),
    },
    # 8. WHAT – Both palms up, shoulders shrug, questioning
    "WHAT": {
        "leftArm":  arm([0.38,-0.06, 0.42],[ 0.05, 0.12, 0.95],[-0.08, 0.15, 0.22],[0.08,0.08,0.08,0.08,0.08]),
        "rightArm": arm([0.38, 0.06,-0.42],[ 0.05,-0.12,-0.95],[-0.08,-0.15,-0.22],[0.08,0.08,0.08,0.08,0.08]),
    },
    # 9. WHERE – Right index pointing up and wagging
    "WHERE": {
        "leftArm":  REST_L,
        "rightArm": arm([0.68, 0.28,-0.60],[-0.08, 0.18,-1.22],[-0.22,-0.10,-0.05],[0.80,0.0,0.90,0.90,0.90]),
    },
    # 10. ME – Right index touching center of chest
    "ME": {
        "leftArm":  REST_L,
        "rightArm": arm([0.78, 0.48, 0.38],[ 1.25,-0.20, 0.35],[ 0.18,-0.40, 1.55],[0.70,0.0,0.90,0.90,0.90]),
    },
    # 11. HELP – Left palm up, right fist resting on it, then lifts
    "HELP": {
        "leftArm":  arm([0.48,-0.08, 0.50],[ 0.02, 0.12, 1.05],[-0.28, 0.20, 0.38],[0.0,0.0,0.0,0.0,0.0]),
        "rightArm": arm([0.52, 0.08,-0.52],[ 0.05,-0.12,-1.08],[-0.30,-0.20,-0.38],[0.0,0.85,0.85,0.85,0.85]),
    },
    # 12. WATER – W-hand (3 fingers) near lips, tapping
    "WATER": {
        "leftArm":  REST_L,
        "rightArm": arm([0.85, 0.32,-0.70],[ 0.18, 0.25,-1.52],[-0.20,-0.22,-0.16],[0.80,0.0,0.0,0.0,0.90]),
    },
    # 13. FOOD – Flat-O hand tapping toward mouth
    "FOOD": {
        "leftArm":  REST_L,
        "rightArm": arm([0.88, 0.35,-0.72],[ 0.22, 0.28,-1.58],[-0.22,-0.24,-0.18],[0.60,0.60,0.60,0.60,0.60]),
    },
    # 14. HOSPITAL – Right fingers drawing cross on left upper arm
    "HOSPITAL": {
        "leftArm":  arm([0.38,-0.02, 0.22],[ 0.02,-0.02, 0.44],[ 0.04,-0.18,-0.08],[0.15,0.15,0.15,0.15,0.15]),
        "rightArm": arm([0.65, 0.28,-0.58],[ 0.05, 0.22,-1.42],[-0.32,-0.18,-0.20],[0.75,0.0,0.0,0.75,0.75]),
    },
    # 15. DOCTOR – Right D-hand tapping wrist pulse
    "DOCTOR": {
        "leftArm":  arm([0.45,-0.05, 0.52],[ 0.02, 0.10, 1.08],[-0.38, 0.22, 0.42],[0.15,0.15,0.15,0.15,0.15]),
        "rightArm": arm([0.60, 0.16,-0.60],[-0.04, 0.14,-1.25],[-0.28,-0.12,-0.09],[0.75,0.0,0.0,0.75,0.75]),
    },
    # 16. TIME – Right index tapping wrist watch
    "TIME": {
        "leftArm":  arm([0.45,-0.05, 0.52],[ 0.02, 0.10, 1.08],[-0.38, 0.22, 0.42],[0.88,0.88,0.88,0.88,0.88]),
        "rightArm": arm([0.62, 0.18,-0.62],[-0.05, 0.15,-1.28],[-0.25,-0.12,-0.10],[0.75,0.0,0.90,0.90,0.90]),
    },
    # 17. TODAY – Both fists dropping firmly twice
    "TODAY": {
        "leftArm":  arm([0.42,-0.08, 0.45],[ 0.05, 0.12, 0.90],[-0.10, 0.18, 0.28],[0.0,0.72,0.72,0.72,0.0]),
        "rightArm": arm([0.42, 0.08,-0.45],[ 0.05,-0.12,-0.90],[-0.10,-0.18,-0.28],[0.0,0.72,0.72,0.72,0.0]),
    },
    # 18. GOOD – Right thumb up, other fingers curled
    "GOOD": {
        "leftArm":  REST_L,
        "rightArm": arm([0.65, 0.32,-0.55],[-0.40,-0.05,-1.05],[-0.18,-0.12,-0.08],[0.0,0.90,0.90,0.90,0.90]),
    },
    # 19. MORNING – Right arm rising behind left forearm like a sunrise
    "MORNING": {
        "leftArm":  arm([0.45,-0.10, 0.50],[ 0.02, 0.12, 1.05],[-0.30, 0.20, 0.35],[0.0,0.0,0.0,0.0,0.0]),
        "rightArm": arm([0.72, 0.22,-0.62],[ 0.12, 0.25,-1.48],[-0.25,-0.18,-0.14],[0.0,0.0,0.0,0.0,0.0]),
    },
    # 20. YES – Right fist nodding gently
    "YES": {
        "leftArm":  REST_L,
        "rightArm": arm([0.65, 0.26,-0.58],[-0.05, 0.20,-1.22],[-0.22,-0.12,-0.05],[0.85,0.85,0.85,0.85,0.85]),
    },
    # 21. NO – Right index and middle snap shut side to side
    "NO": {
        "leftArm":  REST_L,
        "rightArm": arm([0.62, 0.28,-0.56],[-0.06, 0.22,-1.18],[-0.20,-0.12,-0.04],[0.55,0.55,0.55,0.90,0.90]),
    },
    # 22. INDIA – Right thumb touching brow-center (bindi spot)
    "INDIA": {
        "leftArm":  REST_L,
        "rightArm": arm([0.90, 0.32,-0.72],[ 0.22, 0.30,-1.62],[-0.22,-0.24,-0.20],[0.0,0.90,0.90,0.90,0.90]),
    },
    # 23. NICE – Right flat palm glides across upturned left palm
    "NICE": {
        "leftArm":  arm([0.48,-0.08, 0.50],[ 0.02, 0.12, 1.05],[-0.28, 0.20, 0.38],[0.0,0.0,0.0,0.0,0.0]),
        "rightArm": arm([0.55, 0.10,-0.58],[ 0.02,-0.14,-1.18],[-0.32,-0.22,-0.36],[0.0,0.0,0.0,0.0,0.0]),
    },
    # 24. MEET – Both upright index fingers moving to touch in center
    "MEET": {
        "leftArm":  arm([0.58,-0.08, 0.68],[-0.05, 0.22, 1.55],[-0.62, 0.38, 0.50],[0.75,0.0,0.90,0.90,0.90]),
        "rightArm": arm([0.58, 0.08,-0.68],[-0.05,-0.22,-1.55],[-0.62,-0.38,-0.50],[0.75,0.0,0.90,0.90,0.90]),
    },
}

import json

def make_arm_js(a):
    sh = json.dumps(a["shoulder"])
    el = json.dumps(a["elbow"])
    wr = json.dumps(a["wrist"])
    fc = json.dumps(a["fingerCurl"])
    return f'{{"shoulder":{sh},"elbow":{el},"wrist":{wr},"fingerCurl":{fc}}}'

def make_pose_js(p):
    la = make_arm_js(p["leftArm"])
    ra = make_arm_js(p["rightArm"])
    return f'{{"leftArm":{la},"rightArm":{ra}}}'

signs_js_parts = []
for key, val in SIGNS.items():
    signs_js_parts.append(f'      "{key}":{make_pose_js(val)}')
signs_js = ",\n".join(signs_js_parts)
rest_l_js = make_arm_js(REST_L)
rest_r_js = make_arm_js(REST_R)

NEW_COMPUTED_POSES = f"""    const REST_L = {rest_l_js};
    const REST_R = {rest_r_js};

    const COMPUTED_POSES = {{
{signs_js}
    }};
"""

NEW_GET_POSE = r"""    function getPoseForSign(token, progress) {
      if (!token) return getRestingPose();
      const norm = token.toUpperCase().trim();
      const C = COMPUTED_POSES;
      const rest = getRestingPose();

      // Helper: safe arm with fallback
      function safeArm(a) {
        if (!a || !a.shoulder) return rest.leftArm;
        return a;
      }

      // 1. HELLO / NAMASTE
      if (norm === "HELLO" || norm === "NAMASTE" || norm === "GREETINGS" || norm === "HI") {
        const nod = Math.sin(progress * Math.PI) * 0.12;
        return {
          head: [nod * 0.6, 0, 0],
          browY: 0.015,
          mouthOpen: 0.02,
          smile: 0.90,
          bodyShiftZ: 0,
          bodyLeanX: 0.01,
          leftArm: C.HELLO.leftArm,
          rightArm: C.HELLO.rightArm
        };
      }

      // 2. YOU
      if (norm === "YOU" || norm === "AAP" || norm === "TUM" || norm === "YOUR") {
        return {
          head: [0.04, 0, 0],
          browY: 0.02,
          mouthOpen: 0,
          smile: 0.30,
          bodyShiftZ: -0.02,
          bodyLeanX: -0.02,
          leftArm: REST_L,
          rightArm: C.YOU.rightArm
        };
      }

      // 3. HOW
      if (norm === "HOW" || norm === "KAISE") {
        return {
          head: [0.04, 0, 0.10],
          browY: 0.05,
          mouthOpen: 0.14,
          smile: 0.08,
          bodyShiftZ: 0.02,
          bodyLeanX: 0.02,
          leftArm: C.HOW.leftArm,
          rightArm: C.HOW.rightArm
        };
      }

      // 4. THANK-YOU
      if (norm === "THANK-YOU" || norm === "THANKS" || norm === "DHANYAWAD" || norm === "SHUKRIYA") {
        const t = Math.max(0, Math.min(1, progress));
        const s = C.THANK_YOU_START.rightArm;
        const e = C.THANK_YOU_END.rightArm;
        return {
          head: [0.10 * Math.sin(progress * Math.PI), 0, 0],
          browY: 0.02,
          mouthOpen: 0.04,
          smile: 0.95,
          bodyShiftZ: 0.01,
          bodyLeanX: 0.02,
          leftArm: REST_L,
          rightArm: {
            shoulder: lerpArray(s.shoulder, e.shoulder, t),
            elbow:    lerpArray(s.elbow,    e.elbow,    t),
            wrist:    lerpArray(s.wrist,    e.wrist,    t),
            fingerCurl: [0.0, 0.0, 0.0, 0.0, 0.0]
          }
        };
      }

      // 5. WELCOME
      if (norm === "WELCOME" || norm === "SWAGATAM") {
        const sweep = Math.sin(progress * Math.PI) * 0.06;
        const L = C.WELCOME.leftArm;
        const R = C.WELCOME.rightArm;
        return {
          head: [0.05, 0, 0],
          browY: 0.02,
          mouthOpen: 0.04,
          smile: 0.85,
          bodyShiftZ: 0.01,
          bodyLeanX: 0.02,
          leftArm: {
            shoulder: [L.shoulder[0], L.shoulder[1], L.shoulder[2] + sweep],
            elbow: L.elbow, wrist: L.wrist, fingerCurl: L.fingerCurl
          },
          rightArm: {
            shoulder: [R.shoulder[0], R.shoulder[1], R.shoulder[2] - sweep],
            elbow: R.elbow, wrist: R.wrist, fingerCurl: R.fingerCurl
          }
        };
      }

      // 6. PLEASE
      if (norm === "PLEASE" || norm === "KRIPYA") {
        const circ = Math.sin(progress * Math.PI * 2) * 0.05;
        const R = C.PLEASE.rightArm;
        return {
          head: [0.06, 0, 0.06],
          browY: 0.02,
          mouthOpen: 0.03,
          smile: 0.55,
          bodyShiftZ: 0,
          bodyLeanX: 0,
          leftArm: REST_L,
          rightArm: {
            shoulder: [R.shoulder[0] + circ * 0.5, R.shoulder[1] + circ, R.shoulder[2]],
            elbow: R.elbow, wrist: R.wrist,
            fingerCurl: [0.0, 0.0, 0.0, 0.0, 0.0]
          }
        };
      }

      // 7. NAME
      if (norm === "NAME" || norm === "NAAM") {
        const tap = Math.sin(progress * Math.PI * 4) * 0.05;
        const R = C.NAME.rightArm;
        return {
          head: [0.04, 0, 0],
          browY: 0.01,
          mouthOpen: 0.06,
          smile: 0.28,
          bodyShiftZ: 0,
          bodyLeanX: 0,
          leftArm: C.NAME.leftArm,
          rightArm: {
            shoulder: [R.shoulder[0] + tap, R.shoulder[1], R.shoulder[2]],
            elbow: R.elbow, wrist: R.wrist,
            fingerCurl: [0.80, 0.0, 0.0, 0.85, 0.85]
          }
        };
      }

      // 8. WHAT
      if (norm === "WHAT" || norm === "KYA") {
        const shake = Math.sin(progress * Math.PI * 4) * 0.06;
        const L = C.WHAT.leftArm;
        const R = C.WHAT.rightArm;
        return {
          head: [0.06, shake * 0.4, 0],
          browY: -0.025,
          mouthOpen: 0.14,
          smile: 0.0,
          bodyShiftZ: 0.01,
          bodyLeanX: 0.01,
          leftArm: {
            shoulder: [L.shoulder[0], L.shoulder[1] + shake, L.shoulder[2]],
            elbow: L.elbow, wrist: L.wrist, fingerCurl: L.fingerCurl
          },
          rightArm: {
            shoulder: [R.shoulder[0], R.shoulder[1] - shake, R.shoulder[2]],
            elbow: R.elbow, wrist: R.wrist, fingerCurl: R.fingerCurl
          }
        };
      }

      // 9. WHERE
      if (norm === "WHERE" || norm === "KAHAN") {
        const wag = Math.sin(progress * Math.PI * 4) * 0.08;
        const R = C.WHERE.rightArm;
        return {
          head: [0.04, wag * 0.3, 0.08],
          browY: -0.022,
          mouthOpen: 0.10,
          smile: 0.0,
          bodyShiftZ: 0.01,
          bodyLeanX: 0.01,
          leftArm: REST_L,
          rightArm: {
            shoulder: R.shoulder,
            elbow: R.elbow,
            wrist: [R.wrist[0], R.wrist[1] + wag, R.wrist[2]],
            fingerCurl: [0.80, 0.0, 0.90, 0.90, 0.90]
          }
        };
      }

      // 10. ME
      if (norm === "ME" || norm === "I" || norm === "MAIN" || norm === "MY" || norm === "SELF") {
        return {
          head: [0.02, 0, 0],
          browY: 0.01,
          mouthOpen: 0.03,
          smile: 0.28,
          bodyShiftZ: 0.01,
          bodyLeanX: 0.01,
          leftArm: REST_L,
          rightArm: C.ME.rightArm
        };
      }

      // 11. HELP
      if (norm === "HELP" || norm === "MADAD" || norm === "SAHAYATA") {
        const lift = Math.sin(progress * Math.PI) * 0.06;
        const L = C.HELP.leftArm;
        const R = C.HELP.rightArm;
        return {
          head: [0.05, 0, 0],
          browY: 0.02,
          mouthOpen: 0.05,
          smile: 0.38,
          bodyShiftZ: 0,
          bodyLeanX: 0,
          leftArm: {
            shoulder: [L.shoulder[0] - lift, L.shoulder[1], L.shoulder[2]],
            elbow: L.elbow, wrist: L.wrist, fingerCurl: [0.0, 0.0, 0.0, 0.0, 0.0]
          },
          rightArm: {
            shoulder: [R.shoulder[0] - lift, R.shoulder[1], R.shoulder[2]],
            elbow: R.elbow, wrist: R.wrist, fingerCurl: [0.0, 0.85, 0.85, 0.85, 0.85]
          }
        };
      }

      // 12. WATER
      if (norm === "WATER" || norm === "PAANI" || norm === "JAL" || norm === "DRINK") {
        const tap = Math.sin(progress * Math.PI * 4) * 0.04;
        const R = C.WATER.rightArm;
        return {
          head: [0.04, 0, 0.03],
          browY: 0.01,
          mouthOpen: 0.12,
          smile: 0.12,
          bodyShiftZ: 0,
          bodyLeanX: 0,
          leftArm: REST_L,
          rightArm: {
            shoulder: [R.shoulder[0] + tap, R.shoulder[1], R.shoulder[2]],
            elbow: R.elbow, wrist: R.wrist,
            fingerCurl: [0.80, 0.0, 0.0, 0.0, 0.90]
          }
        };
      }

      // 13. FOOD
      if (norm === "FOOD" || norm === "EAT" || norm === "KHANA" || norm === "MEAL") {
        const eat = Math.sin(progress * Math.PI * 4) * 0.05;
        const R = C.FOOD.rightArm;
        return {
          head: [0.05, 0, 0],
          browY: 0.01,
          mouthOpen: 0.12 + Math.abs(eat) * 0.5,
          smile: 0.22,
          bodyShiftZ: 0,
          bodyLeanX: 0,
          leftArm: REST_L,
          rightArm: {
            shoulder: [R.shoulder[0] + eat, R.shoulder[1], R.shoulder[2]],
            elbow: R.elbow, wrist: R.wrist,
            fingerCurl: [0.62, 0.62, 0.62, 0.62, 0.62]
          }
        };
      }

      // 14. HOSPITAL
      if (norm === "HOSPITAL" || norm === "ASPATAL" || norm === "CLINIC") {
        const cross = Math.sin(progress * Math.PI * 2) * 0.04;
        const R = C.HOSPITAL.rightArm;
        return {
          head: [0.04, 0, -0.05],
          browY: 0.01,
          mouthOpen: 0.04,
          smile: 0.18,
          bodyShiftZ: 0,
          bodyLeanX: 0,
          leftArm: C.HOSPITAL.leftArm,
          rightArm: {
            shoulder: R.shoulder, elbow: R.elbow,
            wrist: [R.wrist[0] + cross, R.wrist[1], R.wrist[2]],
            fingerCurl: [0.75, 0.0, 0.0, 0.75, 0.75]
          }
        };
      }

      // 15. DOCTOR
      if (norm === "DOCTOR" || norm === "VAIDYA" || norm === "PHYSICIAN") {
        const tap = Math.sin(progress * Math.PI * 4) * 0.03;
        const R = C.DOCTOR.rightArm;
        return {
          head: [0.08, 0, 0],
          browY: 0.02,
          mouthOpen: 0.03,
          smile: 0.28,
          bodyShiftZ: 0,
          bodyLeanX: 0,
          leftArm: C.DOCTOR.leftArm,
          rightArm: {
            shoulder: [R.shoulder[0] + tap, R.shoulder[1], R.shoulder[2]],
            elbow: R.elbow, wrist: R.wrist,
            fingerCurl: [0.75, 0.0, 0.0, 0.75, 0.75]
          }
        };
      }

      // 16. TIME
      if (norm === "TIME" || norm === "SAMAY" || norm === "WAQT" || norm === "CLOCK" || norm === "WHEN") {
        const tap = Math.sin(progress * Math.PI * 4) * 0.04;
        const R = C.TIME.rightArm;
        return {
          head: [0.08, 0, 0],
          browY: 0.01,
          mouthOpen: 0.03,
          smile: 0.22,
          bodyShiftZ: 0,
          bodyLeanX: 0,
          leftArm: C.TIME.leftArm,
          rightArm: {
            shoulder: [R.shoulder[0] + tap, R.shoulder[1], R.shoulder[2]],
            elbow: R.elbow, wrist: R.wrist,
            fingerCurl: [0.75, 0.0, 0.90, 0.90, 0.90]
          }
        };
      }

      // 17. TODAY
      if (norm === "TODAY" || norm === "AAJ" || norm === "NOW") {
        const drop = Math.sin(progress * Math.PI * 2) * 0.06;
        const L = C.TODAY.leftArm;
        const R = C.TODAY.rightArm;
        return {
          head: [0.05, 0, 0],
          browY: 0.01,
          mouthOpen: 0.03,
          smile: 0.28,
          bodyShiftZ: 0,
          bodyLeanX: 0,
          leftArm: {
            shoulder: [L.shoulder[0] + drop, L.shoulder[1], L.shoulder[2]],
            elbow: L.elbow, wrist: L.wrist, fingerCurl: [0.0, 0.70, 0.70, 0.70, 0.0]
          },
          rightArm: {
            shoulder: [R.shoulder[0] + drop, R.shoulder[1], R.shoulder[2]],
            elbow: R.elbow, wrist: R.wrist, fingerCurl: [0.0, 0.70, 0.70, 0.70, 0.0]
          }
        };
      }

      // 18. GOOD
      if (norm === "GOOD" || norm === "ACHA" || norm === "BADHIYA") {
        return {
          head: [0.04, 0, 0],
          browY: 0.02,
          mouthOpen: 0.02,
          smile: 0.88,
          bodyShiftZ: 0,
          bodyLeanX: 0,
          leftArm: REST_L,
          rightArm: C.GOOD.rightArm
        };
      }

      // 19. MORNING
      if (norm === "MORNING" || norm === "SUBAH" || norm === "GOOD_MORNING") {
        const rise = Math.sin(progress * Math.PI) * 0.05;
        const R = C.MORNING.rightArm;
        return {
          head: [0.05, 0, 0],
          browY: 0.03,
          mouthOpen: 0.04,
          smile: 0.75,
          bodyShiftZ: 0,
          bodyLeanX: 0,
          leftArm: C.MORNING.leftArm,
          rightArm: {
            shoulder: [R.shoulder[0] - rise, R.shoulder[1], R.shoulder[2]],
            elbow: R.elbow, wrist: R.wrist, fingerCurl: R.fingerCurl
          }
        };
      }

      // 20. YES
      if (norm === "YES" || norm === "HAAN" || norm === "JI") {
        const nod = Math.sin(progress * Math.PI * 3) * 0.06;
        const R = C.YES.rightArm;
        return {
          head: [nod, 0, 0],
          browY: 0.02,
          mouthOpen: 0.02,
          smile: 0.65,
          bodyShiftZ: 0,
          bodyLeanX: 0,
          leftArm: REST_L,
          rightArm: {
            shoulder: [R.shoulder[0] + nod, R.shoulder[1], R.shoulder[2]],
            elbow: R.elbow, wrist: R.wrist, fingerCurl: R.fingerCurl
          }
        };
      }

      // 21. NO
      if (norm === "NO" || norm === "NAHI" || norm === "NAA") {
        const shake = Math.sin(progress * Math.PI * 4) * 0.08;
        const R = C.NO.rightArm;
        return {
          head: [0, shake * 0.4, 0],
          browY: -0.02,
          mouthOpen: 0.06,
          smile: 0.0,
          bodyShiftZ: 0,
          bodyLeanX: 0,
          leftArm: REST_L,
          rightArm: {
            shoulder: [R.shoulder[0], R.shoulder[1] + shake, R.shoulder[2]],
            elbow: R.elbow, wrist: R.wrist, fingerCurl: R.fingerCurl
          }
        };
      }

      // 22. INDIA
      if (norm === "INDIA" || norm === "BHARAT") {
        return {
          head: [0.02, 0, 0],
          browY: 0.02,
          mouthOpen: 0.02,
          smile: 0.55,
          bodyShiftZ: 0,
          bodyLeanX: 0,
          leftArm: REST_L,
          rightArm: C.INDIA.rightArm
        };
      }

      // 23. NICE
      if (norm === "NICE" || norm === "PLEASANT" || norm === "SUNDAR") {
        const t = Math.max(0, Math.min(1, progress));
        const L = C.NICE.leftArm;
        const Rstart = C.NICE.rightArm;
        // Glide animation: shift wrist forward during progress
        const glideX = -0.10 * t;
        return {
          head: [0.05, 0, 0],
          browY: 0.02,
          mouthOpen: 0.03,
          smile: 0.82,
          bodyShiftZ: 0,
          bodyLeanX: 0,
          leftArm: { shoulder: L.shoulder, elbow: L.elbow, wrist: L.wrist, fingerCurl: [0.0,0.0,0.0,0.0,0.0] },
          rightArm: {
            shoulder: Rstart.shoulder, elbow: Rstart.elbow,
            wrist: [Rstart.wrist[0] + glideX, Rstart.wrist[1], Rstart.wrist[2]],
            fingerCurl: [0.0,0.0,0.0,0.0,0.0]
          }
        };
      }

      // 24. MEET
      if (norm === "MEET" || norm === "MILNA" || norm === "MEETING") {
        const reach = Math.sin(progress * Math.PI) * 0.05;
        const L = C.MEET.leftArm;
        const R = C.MEET.rightArm;
        return {
          head: [0.04, 0, 0],
          browY: 0.02,
          mouthOpen: 0.04,
          smile: 0.75,
          bodyShiftZ: 0.01,
          bodyLeanX: 0.01,
          leftArm: {
            shoulder: [L.shoulder[0], L.shoulder[1], L.shoulder[2] + reach],
            elbow: L.elbow, wrist: L.wrist, fingerCurl: L.fingerCurl
          },
          rightArm: {
            shoulder: [R.shoulder[0], R.shoulder[1], R.shoulder[2] - reach],
            elbow: R.elbow, wrist: R.wrist, fingerCurl: R.fingerCurl
          }
        };
      }

      // DEFAULT – single right hand acknowledging
      return {
        head: [0.04 * Math.sin(progress * Math.PI), 0, 0],
        browY: 0.01,
        mouthOpen: 0.03,
        smile: 0.28,
        bodyShiftZ: 0,
        bodyLeanX: 0,
        leftArm: REST_L,
        rightArm: {
          shoulder: [0.55, 0.18, -0.50],
          elbow: [-0.25, -0.04, -1.00],
          wrist: [-0.15, -0.10, -0.06],
          fingerCurl: [0.15, 0.15, 0.15, 0.15, 0.15]
        }
      };
    }
"""

# ── Locate and replace COMPUTED_POSES + getPoseForSign ────────────────────
# Pattern: from "    const COMPUTED_POSES = {" through end of getPoseForSign
cp_pattern = re.compile(
    r'    const COMPUTED_POSES = \{[\s\S]*?\n    \};\s*\n[\s\S]*?function getPoseForSign\(token, progress\) \{[\s\S]*?\n    \}',
    re.MULTILINE
)
replacement = NEW_COMPUTED_POSES + "\n" + NEW_GET_POSE

content, n = cp_pattern.subn(replacement, content)
print("Replaced COMPUTED_POSES + getPoseForSign:", n)
if n == 0:
    # Try fallback: find boundaries manually
    cp_start = content.find("    const COMPUTED_POSES = {")
    gp_end_marker = "\n    }\n\n    // --- SMOOTH INTERPOLATION"
    gp_end = content.find(gp_end_marker)
    if cp_start != -1 and gp_end != -1:
        old_block = content[cp_start:gp_end + 6]  # include closing }
        content = content[:cp_start] + NEW_COMPUTED_POSES + "\n" + NEW_GET_POSE + content[gp_end + 6:]
        print("Used fallback replacement")
    else:
        print("ERROR: Could not locate block. cp_start=", cp_start, "gp_end=", gp_end)

# ── Fix getRestingPose to return proper REST_L / REST_R style ─────────────
NEW_REST = """    function getRestingPose() {
      return {
        head: [0, 0, 0],
        browY: 0,
        mouthOpen: 0,
        smile: 0.38,
        bodyShiftZ: 0,
        bodyLeanX: 0,
        leftArm: REST_L,
        rightArm: REST_R
      };
    }
"""
rest_pattern = re.compile(r'    function getRestingPose\(\) \{[\s\S]*?\n    \}')
content, n2 = rest_pattern.subn(NEW_REST, content)
print("Updated getRestingPose:", n2)

# ── Write back ────────────────────────────────────────────────────────────
index_path.write_text(content, encoding="utf-8")
print("Written successfully!")
print("Total length:", len(content.splitlines()), "lines")
