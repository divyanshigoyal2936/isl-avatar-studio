import numpy as np
import json
from scipy.optimize import minimize

def rot_x(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
def rot_y(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
def rot_z(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
def euler_xyz(rx, ry, rz):
    return rot_x(rx) @ rot_y(ry) @ rot_z(rz)

def solve_arm(sh_pos, wrist_target, finger_target_dir=None, palm_target_norm=None, elbow_pole=None, init=None):
    p_el_local = np.array([0, -0.28, 0])
    p_wr_local = np.array([0, -0.26, 0])
    
    def cost(x):
        R_sh = euler_xyz(x[0], x[1], x[2])
        R_el = euler_xyz(x[3], x[4], x[5])
        R_wr = euler_xyz(x[6], x[7], x[8])
        
        el_pos = sh_pos + R_sh @ p_el_local
        wr_pos = el_pos + R_sh @ R_el @ p_wr_local
        
        err = np.sum((wr_pos - wrist_target)**2) * 350.0
        
        R_total = R_sh @ R_el @ R_wr
        if finger_target_dir is not None:
            f_dir = R_total @ np.array([0, -1, 0])
            err += np.sum((f_dir - finger_target_dir)**2) * 90.0
            
        if palm_target_norm is not None:
            p_norm = R_total @ np.array([0, 0, 1])
            err += np.sum((p_norm - palm_target_norm)**2) * 90.0
            
        if elbow_pole is not None:
            err += np.sum((el_pos - elbow_pole)**2) * 35.0
            
        err += np.sum(x**2) * 0.05
        return err

    x0 = np.zeros(9) if init is None else np.array(init)
    res = minimize(cost, x0, method='BFGS')
    res2 = minimize(cost, res.x, method='Nelder-Mead', options={'maxiter': 6000})
    angles = [round(float(v), 3) for v in res2.x]
    
    return {
        "shoulder": angles[:3],
        "elbow": angles[3:6],
        "wrist": angles[6:]
    }

sh_R = np.array([0.22, 0.44, 0.0])
sh_L = np.array([-0.22, 0.44, 0.0])

# Pre-solve all needed poses for the 24 signs
poses = {}

# 1. HELLO / NAMASTE (Verified: elbows down, hands vertically joined at chest)
poses["HELLO"] = {
    "desc": "Namaste with both hands vertically joined at chest, elbows down",
    "leftArm": {
        "shoulder": [-0.356, 0.0, 0.576],
        "elbow": [-1.941, 0.522, 0.402],
        "wrist": [-1.464, 1.775, 0.570],
        "fingerCurl": [0.0, 0.0, 0.0, 0.0, 0.0]
    },
    "rightArm": {
        "shoulder": [-0.356, 0.0, -0.576],
        "elbow": [-1.941, -0.522, -0.402],
        "wrist": [-1.464, -1.775, -0.570],
        "fingerCurl": [0.0, 0.0, 0.0, 0.0, 0.0]
    }
}

# 2. YOU (Verified: index pointing forward at user, elbow down)
poses["YOU"] = {
    "desc": "Right index pointing forward at user",
    "rightArm": {
        "shoulder": [-0.994, -0.210, -0.626],
        "elbow": [-0.851, -0.296, 0.677],
        "wrist": [0.256, -0.244, -0.098],
        "fingerCurl": [0.95, 0.0, 0.95, 0.95, 0.95]
    }
}

# 3. HOW (Fixed: cupped palms rotating upward, elbows down)
how_r = solve_arm(sh_R, np.array([0.15, 0.28, 0.30]), np.array([0, 0.3, 0.95])/np.linalg.norm([0, 0.3, 0.95]), np.array([0, 1, 0]), np.array([0.20, 0.18, 0.08]))
how_l = solve_arm(sh_L, np.array([-0.15, 0.28, 0.30]), np.array([0, 0.3, 0.95])/np.linalg.norm([0, 0.3, 0.95]), np.array([0, 1, 0]), np.array([-0.20, 0.18, 0.08]))
poses["HOW"] = {
    "desc": "Both cupped hands rotating palms-upward",
    "leftArm": {**how_l, "fingerCurl": [0.35, 0.35, 0.35, 0.35, 0.35]},
    "rightArm": {**how_r, "fingerCurl": [0.35, 0.35, 0.35, 0.35, 0.35]}
}

# 4. THANK-YOU (Chin to forward sweep)
ty_start = solve_arm(sh_R, np.array([0.06, 0.44, 0.22]), np.array([0, 0.8, 0.6])/np.linalg.norm([0, 0.8, 0.6]), np.array([-0.2, 0.6, -0.7])/np.linalg.norm([-0.2, 0.6, -0.7]), np.array([0.18, 0.22, 0.08]))
ty_end = solve_arm(sh_R, np.array([0.12, 0.26, 0.35]), np.array([0, 0.2, 0.98])/np.linalg.norm([0, 0.2, 0.98]), np.array([0, 1, 0]), np.array([0.18, 0.18, 0.08]))
poses["THANK_YOU_START"] = ty_start
poses["THANK_YOU_END"] = ty_end

# 5. WELCOME (Both palms facing up, sweeping gently inward)
wel_r = solve_arm(sh_R, np.array([0.14, 0.26, 0.28]), np.array([0, 0.2, 0.98])/np.linalg.norm([0, 0.2, 0.98]), np.array([0, 1, 0]), np.array([0.20, 0.18, 0.08]))
wel_l = solve_arm(sh_L, np.array([-0.14, 0.26, 0.28]), np.array([0, 0.2, 0.98])/np.linalg.norm([0, 0.2, 0.98]), np.array([0, 1, 0]), np.array([-0.20, 0.18, 0.08]))
poses["WELCOME"] = {
    "leftArm": {**wel_l, "fingerCurl": [0.0, 0.0, 0.0, 0.0, 0.0]},
    "rightArm": {**wel_r, "fingerCurl": [0.0, 0.0, 0.0, 0.0, 0.0]}
}

# 6. PLEASE (Right open palm rubbing gently on chest center)
pls = solve_arm(sh_R, np.array([0.04, 0.34, 0.18]), np.array([0, 0.95, 0.3])/np.linalg.norm([0, 0.95, 0.3]), np.array([0, 0.2, -0.98])/np.linalg.norm([0, 0.2, -0.98]), np.array([0.18, 0.20, 0.06]))
poses["PLEASE"] = pls

# 7. NAME (Right H-hand tapping left extended fingers)
nm_r = solve_arm(sh_R, np.array([0.02, 0.30, 0.26]), np.array([-0.6, 0.0, 0.8])/np.linalg.norm([-0.6, 0.0, 0.8]), np.array([0, -1, 0]), np.array([0.18, 0.18, 0.08]))
nm_l = solve_arm(sh_L, np.array([-0.04, 0.28, 0.26]), np.array([0.6, 0.0, 0.8])/np.linalg.norm([0.6, 0.0, 0.8]), np.array([0, 1, 0]), np.array([-0.18, 0.18, 0.08]))
poses["NAME"] = {"right": nm_r, "left": nm_l}

# 8. WHAT (Both open palms up at waist/chest oscillating)
what_r = solve_arm(sh_R, np.array([0.18, 0.24, 0.26]), np.array([0, 0.3, 0.95])/np.linalg.norm([0, 0.3, 0.95]), np.array([0, 1, 0]), np.array([0.22, 0.18, 0.06]))
what_l = solve_arm(sh_L, np.array([-0.18, 0.24, 0.26]), np.array([0, 0.3, 0.95])/np.linalg.norm([0, 0.3, 0.95]), np.array([0, 1, 0]), np.array([-0.22, 0.18, 0.06]))
poses["WHAT"] = {"right": what_r, "left": what_l}

# 9. WHERE (Right index pointing up/forward, waving side to side)
whr = solve_arm(sh_R, np.array([0.16, 0.36, 0.30]), np.array([0, 0.8, 0.6])/np.linalg.norm([0, 0.8, 0.6]), np.array([0, 0.5, -0.86])/np.linalg.norm([0, 0.5, -0.86]), np.array([0.20, 0.20, 0.08]))
poses["WHERE"] = whr

# 10. ME (Right index pointing directly at signer's own chest)
me = solve_arm(sh_R, np.array([0.06, 0.32, 0.16]), np.array([0, -0.2, -0.98])/np.linalg.norm([0, -0.2, -0.98]), np.array([0, 1, 0]), np.array([0.18, 0.20, 0.05]))
poses["ME"] = me

# 11. HELP (Right fist resting on flat left palm, lifting)
hlp_l = solve_arm(sh_L, np.array([-0.02, 0.26, 0.26]), np.array([0.3, 0.2, 0.93])/np.linalg.norm([0.3, 0.2, 0.93]), np.array([0, 1, 0]), np.array([-0.18, 0.18, 0.08]))
hlp_r = solve_arm(sh_R, np.array([0.02, 0.30, 0.26]), np.array([-0.2, 0.2, 0.96])/np.linalg.norm([-0.2, 0.2, 0.96]), np.array([-1, 0, 0]), np.array([0.18, 0.20, 0.08]))
poses["HELP"] = {"right": hlp_r, "left": hlp_l}

# 12. WATER (Right W-hand tapping at mouth)
wtr = solve_arm(sh_R, np.array([0.05, 0.46, 0.20]), np.array([0, 0.8, 0.6])/np.linalg.norm([0, 0.8, 0.6]), np.array([-0.2, 0.5, -0.85])/np.linalg.norm([-0.2, 0.5, -0.85]), np.array([0.18, 0.24, 0.08]))
poses["WATER"] = wtr

# 13. FOOD (Right bunched fingers brought toward mouth)
fd = solve_arm(sh_R, np.array([0.05, 0.44, 0.20]), np.array([0, 0.7, 0.7])/np.linalg.norm([0, 0.7, 0.7]), np.array([0, 0.7, -0.7])/np.linalg.norm([0, 0.7, -0.7]), np.array([0.18, 0.24, 0.08]))
poses["FOOD"] = fd

# 14. HOSPITAL (Right index+middle draws cross on left shoulder)
hosp = solve_arm(sh_R, np.array([-0.16, 0.40, 0.10]), np.array([0, 0.6, 0.8])/np.linalg.norm([0, 0.6, 0.8]), np.array([0, 0.8, -0.6])/np.linalg.norm([0, 0.8, -0.6]), np.array([0.12, 0.24, 0.06]))
poses["HOSPITAL"] = hosp

# 15. DOCTOR (Right two fingers tapping left inner wrist)
doc_l = solve_arm(sh_L, np.array([-0.08, 0.26, 0.26]), np.array([0.5, 0.2, 0.84])/np.linalg.norm([0.5, 0.2, 0.84]), np.array([0, 1, 0]), np.array([-0.18, 0.18, 0.08]))
doc_r = solve_arm(sh_R, np.array([-0.06, 0.29, 0.26]), np.array([-0.4, -0.4, 0.82])/np.linalg.norm([-0.4, -0.4, 0.82]), np.array([0, -1, 0]), np.array([0.16, 0.20, 0.08]))
poses["DOCTOR"] = {"right": doc_r, "left": doc_l}

# 16. TIME (Right index tapping left wrist watch)
tim_l = solve_arm(sh_L, np.array([-0.08, 0.26, 0.26]), np.array([0.5, 0.2, 0.84])/np.linalg.norm([0.5, 0.2, 0.84]), np.array([0, -1, 0]), np.array([-0.18, 0.18, 0.08]))
tim_r = solve_arm(sh_R, np.array([-0.07, 0.29, 0.26]), np.array([-0.3, -0.5, 0.82])/np.linalg.norm([-0.3, -0.5, 0.82]), np.array([0, -1, 0]), np.array([0.16, 0.20, 0.08]))
poses["TIME"] = {"right": tim_r, "left": tim_l}

# 17. TODAY (Both open palms face up, abrupt double drop)
td_r = solve_arm(sh_R, np.array([0.14, 0.25, 0.26]), np.array([0, 0.2, 0.98])/np.linalg.norm([0, 0.2, 0.98]), np.array([0, 1, 0]), np.array([0.20, 0.18, 0.08]))
td_l = solve_arm(sh_L, np.array([-0.14, 0.25, 0.26]), np.array([0, 0.2, 0.98])/np.linalg.norm([0, 0.2, 0.98]), np.array([0, 1, 0]), np.array([-0.20, 0.18, 0.08]))
poses["TODAY"] = {"right": td_r, "left": td_l}

# 18. GOOD (Right thumbs-up held forward)
gd = solve_arm(sh_R, np.array([0.14, 0.30, 0.32]), np.array([0, 0.1, 0.99])/np.linalg.norm([0, 0.1, 0.99]), np.array([-1, 0, 0]), np.array([0.20, 0.20, 0.08]))
poses["GOOD"] = gd

# 19. MORNING (Left horizontal arm, right arm rising like the sun)
mrn_l = solve_arm(sh_L, np.array([-0.04, 0.26, 0.24]), np.array([0.95, 0.0, 0.3])/np.linalg.norm([0.95, 0.0, 0.3]), np.array([0, 0, 1]), np.array([-0.18, 0.18, 0.08]))
mrn_r_lo = solve_arm(sh_R, np.array([0.02, 0.24, 0.20]), np.array([0, 0.7, 0.7])/np.linalg.norm([0, 0.7, 0.7]), np.array([0, 0.7, -0.7])/np.linalg.norm([0, 0.7, -0.7]), np.array([0.18, 0.18, 0.06]))
mrn_r_hi = solve_arm(sh_R, np.array([0.04, 0.42, 0.22]), np.array([0, 0.9, 0.43])/np.linalg.norm([0, 0.9, 0.43]), np.array([0, 0.43, -0.9])/np.linalg.norm([0, 0.43, -0.9]), np.array([0.18, 0.26, 0.08]))
poses["MORNING"] = {"left": mrn_l, "right_lo": mrn_r_lo, "right_hi": mrn_r_hi}

# 20. YES (Right fist nodding up and down at wrist)
ys = solve_arm(sh_R, np.array([0.14, 0.32, 0.30]), np.array([0, 0.2, 0.98])/np.linalg.norm([0, 0.2, 0.98]), np.array([0, 0.98, -0.2])/np.linalg.norm([0, 0.98, -0.2]), np.array([0.20, 0.20, 0.08]))
poses["YES"] = ys

# 21. NO (Right index wagging side to side)
no_p = solve_arm(sh_R, np.array([0.14, 0.36, 0.32]), np.array([0, 0.8, 0.6])/np.linalg.norm([0, 0.8, 0.6]), np.array([0, 0.6, -0.8])/np.linalg.norm([0, 0.6, -0.8]), np.array([0.20, 0.20, 0.08]))
poses["NO"] = no_p

# 22. INDIA (Right thumb touches center of forehead)
ind = solve_arm(sh_R, np.array([0.03, 0.52, 0.18]), np.array([0, 0.6, 0.8])/np.linalg.norm([0, 0.6, 0.8]), np.array([0, 0.8, -0.6])/np.linalg.norm([0, 0.8, -0.6]), np.array([0.18, 0.30, 0.08]))
poses["INDIA"] = ind

# 23. NICE (Right flat palm glides smoothly forward across left palm)
nc_l = solve_arm(sh_L, np.array([-0.04, 0.26, 0.26]), np.array([0.6, 0.1, 0.79])/np.linalg.norm([0.6, 0.1, 0.79]), np.array([0, 1, 0]), np.array([-0.18, 0.18, 0.08]))
nc_r_start = solve_arm(sh_R, np.array([-0.04, 0.28, 0.22]), np.array([0.2, 0.0, 0.98])/np.linalg.norm([0.2, 0.0, 0.98]), np.array([0, -1, 0]), np.array([0.16, 0.20, 0.08]))
nc_r_end = solve_arm(sh_R, np.array([0.06, 0.28, 0.34]), np.array([0.1, 0.0, 0.99])/np.linalg.norm([0.1, 0.0, 0.99]), np.array([0, -1, 0]), np.array([0.18, 0.20, 0.10]))
poses["NICE"] = {"left": nc_l, "right_start": nc_r_start, "right_end": nc_r_end}

# 24. MEET (Both hands with index upright approaching each other until knuckles meet)
mt_r = solve_arm(sh_R, np.array([0.04, 0.32, 0.28]), np.array([-0.3, 0.8, 0.52])/np.linalg.norm([-0.3, 0.8, 0.52]), np.array([-1, 0, 0]), np.array([0.18, 0.20, 0.08]))
mt_l = solve_arm(sh_L, np.array([-0.04, 0.32, 0.28]), np.array([0.3, 0.8, 0.52])/np.linalg.norm([0.3, 0.8, 0.52]), np.array([1, 0, 0]), np.array([-0.18, 0.18, 0.08]))
poses["MEET"] = {"right": mt_r, "left": mt_l}

with open(r'C:\Users\laksh\.gemini\antigravity\scratch\rag-speech-to-isl\data\computed_isl_poses.json', 'w') as f:
    json.dump(poses, f, indent=2)

print("SUCCESS: 24 ISL Signs fully computed and saved to data/computed_isl_poses.json!")
