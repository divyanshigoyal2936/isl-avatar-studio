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
        
        err = np.sum((wr_pos - wrist_target)**2) * 300.0
        
        R_total = R_sh @ R_el @ R_wr
        if finger_target_dir is not None:
            f_dir = R_total @ np.array([0, -1, 0])
            err += np.sum((f_dir - finger_target_dir)**2) * 80.0
            
        if palm_target_norm is not None:
            p_norm = R_total @ np.array([0, 0, 1])
            err += np.sum((p_norm - palm_target_norm)**2) * 80.0
            
        if elbow_pole is not None:
            err += np.sum((el_pos - elbow_pole)**2) * 30.0
            
        # Regularization
        err += np.sum(x**2) * 0.05
        return err

    x0 = np.zeros(9) if init is None else np.array(init)
    res = minimize(cost, x0, method='BFGS')
    res2 = minimize(cost, res.x, method='Nelder-Mead', options={'maxiter': 5000})
    angles = [round(float(v), 3) for v in res2.x]
    
    # Validation check
    R_sh = euler_xyz(*angles[:3])
    R_el = euler_xyz(*angles[3:6])
    R_wr = euler_xyz(*angles[6:])
    el = sh_pos + R_sh @ p_el_local
    wr = el + R_sh @ R_el @ p_wr_local
    
    return {
        "shoulder": angles[:3],
        "elbow": angles[3:6],
        "wrist": angles[6:],
        "wrist_pos": [round(float(v), 3) for v in wr],
        "elbow_pos": [round(float(v), 3) for v in el]
    }

sh_R = np.array([0.22, 0.44, 0.0])
sh_L = np.array([-0.22, 0.44, 0.0])

print("IK Library ready.")
