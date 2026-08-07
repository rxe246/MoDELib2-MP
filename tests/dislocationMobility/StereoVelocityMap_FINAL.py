import sys, os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from matplotlib.path import Path
from scipy.spatial import Delaunay
from scipy.stats import mode

# --- PATHS ---
sys.path.append("../../build/tools/pyMoDELib")
sys.path.append("../../python")
import pyMoDELib
from modlibUtils import *

# --- CONFIG ---
cfg = {
    'grouped': False,    # focus on specific slip systems
    'full': False,       # full projection cube
    'family': True       # group by families (<111>{110} vs <100>{110})
}

# MoDELib params
mat_file = "../../Library/Materials/W.txt"
T = 300
s0 = 0.01

# Projection corners (ignored if full mode)
v1 = [-1, -1, 2]
v2 = [1, 1, 1]
v3 = [-2, 1, 1]

# Resolution
n = 200000   # increase for high-quality, decrease for speed

# Plot customization
title = "Max-Velocity Slip System"
show_extra = True       # show extra cube edges/directions
highlight = {            # custom directions to highlight
    '[001]': [0, 0, 1],
    '[111]': [1, 1, 1],
    '[011]': [0, 1, 1],
    '[-1-12]': [-1, -1, 2],
    '[-211]': [-2, 1, 1],
    '[-101]': [-1, 0, 1],
    '[-111]': [-1, 1, 1]
}

trace_lines = {
    # '[0-10] to [010]':      ([0,-1,0], [0,1,0], 'k'),
    # '[-1-10] to [110]':     ([-1,-1,0], [1,1,0], 'k'),
    # '[1-10] to [-110]':     ([1,-1,0], [-1,1,0], 'k'),
    # '[100] to [-100]':      ([1,0,0], [-1,0,0], 'k'),
    # '[0-10] to [-100]':     ([0,-1,0], [-1,0,0], 'k'),
    # '[-100] to [010]':      ([-1,0,0], [0,1,0], 'k'),
    # '[010] to [100]':       ([0,1,0], [1,0,0], 'k'),
    # '[100] to [0-10]':      ([1,0,0], [0,-1,0], 'k'),
    # '[0-10] to [101]':      ([0,-1,0], [1,0,1], 'k'),
    # '[0-10] to [-101]':      ([0,-1,0], [-1,0,1], 'k'),
    # '[010] to [101]':      ([0,1,0], [1,0,1], 'k'),
    # '[010] to [-101]':      ([0,1,0], [-1,0,1], 'k'),
    # '[100] to [011]':      ([1,0,0], [0,1,1], 'k'),
    # '[-100] to [011]':      ([-1,0,0], [0,1,1], 'k'),
    # '[-100] to [0-11]':      ([-1,0,0], [0,-1,1], 'k'),
    # '[100] to [0-11]':      ([1,0,0], [0,-1,1], 'k'),
    '[-1-12] to [-211]': ([-1,-1,2], [-2,1,1], 'r:'),
    '[-1-12] to [111]': ([-1,-1,2], [1,1,1], 'r:'),
    '[111] to [-211]': ([1,1,1], [-2,1,1], 'r:'),
    '[111] to [-101]': ([1,1,1], [-1,0,1], 'k--'),
    '[001] to [011]': ([0,0,1], [0,1,1], 'k'),
    '[001] to [-111]': ([0,0,1], [-1,1,1], 'k'),
    '[001] to [-101]': ([0,0,1], [-1,0,1], 'k'),
    '[-101] to [011]': ([-1,0,1], [-1,1,1], 'k')
}

sel_idx = [5, 2, 10, 14, 22, 13, 21, 16, 8, 6, 0, 18]  # slip systems if grouped mode

# --- UTILS ---
def norm(v):
    v = np.array(v, dtype=float)
    return v / np.linalg.norm(v)

def proj(v):
    v = norm(v)
    if v[2] < 0: v = -v
    return np.array([v[0]/(1+v[2]), v[1]/(1+v[2])])

def slerp(v0, v1, m=200):
    v0, v1 = norm(v0), norm(v1)
    dot = np.clip(np.dot(v0, v1), -1, 1)
    th = np.arccos(dot)
    if np.isclose(th, 0):
        return np.tile(v0, (m, 1))
    s = np.sin(th)
    return np.array([(np.sin((1-t)*th)*v0 + np.sin(t*th)*v1)/s for t in np.linspace(0,1,m)])

# --- PROJECTION PATH ---
R = np.array([[0,1],[-1,0]])

if not cfg['full']:
    a12, a23, a31 = slerp(v1,v2), slerp(v2,v3), slerp(v3,v1)
    p12 = np.array([proj(p) for p in a12]) @ R.T
    p23 = np.array([proj(p) for p in a23]) @ R.T
    p31 = np.array([proj(p) for p in a31]) @ R.T
    tri_path = Path(np.vstack([p12,p23,p31]))

# --- SLIP SYSTEMS ---
ss111 = [
    ([1,1,-1],[1,0,1]),([-1,-1,1],[1,0,1]),([-1,1,1],[1,0,1]),([1,-1,-1],[1,0,1]),
    ([-1,-1,-1],[-1,0,1]),([1,1,1],[-1,0,1]),([1,-1,1],[-1,0,1]),([-1,1,-1],[-1,0,1]),
    ([1,-1,1],[0,1,1]),([-1,1,-1],[0,1,1]),([1,1,-1],[0,1,1]),([-1,-1,1],[0,1,1]),
    ([-1,-1,-1],[0,1,-1]),([1,1,1],[0,1,-1]),([-1,1,1],[0,1,-1]),([1,-1,-1],[0,1,-1]),
    ([-1,1,1],[1,1,0]),([1,-1,-1],[1,1,0]),([1,-1,1],[1,1,0]),([-1,1,-1],[1,1,0]),
    ([-1,-1,-1],[1,-1,0]),([1,1,1],[1,-1,0]),([1,1,-1],[1,-1,0]),([-1,-1,1],[1,-1,0])
]
ss100 = [
    ([0,1,0],[1,0,1]),([0,-1,0],[1,0,1]),([0,-1,0],[-1,0,1]),([0,1,0],[-1,0,1]),
    ([1,0,0],[0,1,1]),([-1,0,0],[0,1,1]),([-1,0,0],[0,1,-1]),([1,0,0],[0,1,-1]),
    ([0,0,1],[1,1,0]),([0,0,-1],[1,1,0]),([0,0,-1],[1,-1,0]),([0,0,1],[1,-1,0])
]

if cfg['family']:
    ss = ss111 + ss100
    gmap = np.array([0]*24 + [1]*12)
elif cfg['grouped']:
    ss = [ss111[i] for i in sel_idx]
    gmap = np.arange(len(sel_idx))
else:
    ss = ss111
    gmap = np.arange(len(ss))

ss = [(norm(b), norm(n)) for b,n in ss]

# --- ORIENTATIONS ---
idx = np.arange(0,n)+0.5
phi = np.arccos(1-2*idx/n)
th = np.pi*(1+5**0.5)*idx
x,y,z = np.sin(phi)*np.cos(th), np.sin(phi)*np.sin(th), np.cos(phi)
ori = np.stack((x,y,z),1)

pts = np.array([proj(v) for v in ori]) @ R.T

# --- MoDELib ---
mat = pyMoDELib.PolycrystallineMaterialBase(mat_file,T)
if cfg['family']:
    mob111, mob100 = pyMoDELib.DislocationMobilityBCC(mat), pyMoDELib.DislocationMobilityBCC100(mat)
else:
    mob = pyMoDELib.DislocationMobilityBCC(mat)

max_idx = []
for m in ori:
    m = norm(m)
    S = np.outer(m,m)*s0
    v_all = []
    for b,n in ss:
        if cfg['family']:
            if np.allclose(np.abs(b),[1,0,0]) or np.allclose(np.abs(b),[0,1,0]) or np.allclose(np.abs(b),[0,0,1]):
                v_all.append(mob100.velocity(S,b,b,n,T))
            else:
                v_all.append(mob111.velocity(S,b,b,n,T))
        else:
            v_all = [mob.velocity(S,b,b,n,T) for b,n in ss]
    max_idx.append(np.argmax(v_all))

    """ target_pole = [-1, 0, 1]
    # Check if the current orientation 'm' is effectively the target pole
    if abs(np.dot(m, target_pole)) > 0.995: # Tolerance for "close enough"
        print(f"\n========== DEBUG ANALYSIS AT POLE {m} ==========")
        print(f"Applied Stress Axis: {m}")
        print(f"{'Idx':<4} {'Family':<6} {'b-vector':<20} {'n-vector':<20} {'Velocity':<15} {'Note'}")
        print("-" * 80)
        
        # Re-iterate to print details
        best_v = -1.0
        best_idx = -1
        
        for i, val in enumerate(v_all):
            b_tmp, n_tmp = ss[i]
            
            # Determine Family Label
            is_100 = np.allclose(np.abs(b_tmp),[1,0,0]) or np.allclose(np.abs(b_tmp),[0,1,0]) or np.allclose(np.abs(b_tmp),[0,0,1])
            fam = "<100>" if is_100 else "<111>"
            
            # Track max manually to verify
            if val > best_v:
                best_v = val
                best_idx = i
            
            # Filter: Print all <100> systems, and the winner
            # We want to see if <100> is 0.0 or 1e-35
            if is_100 or i == np.argmax(v_all) or val > 0.0:
                marker = "<< WINNER" if i == np.argmax(v_all) else ""
                # Format vectors nicely
                b_str = str(np.round(b_tmp, 2))
                n_str = str(np.round(n_tmp, 2))
                print(f"{i:<4} {fam:<6} {b_str:<20} {n_str:<20} {val:.6e}   {marker}")
                
        print("-" * 80)
        print(f"Script detected Max Index: {np.argmax(v_all)}")
        print("================================================\n") """
max_idx = np.array(max_idx)

idx_final = gmap[max_idx] if cfg['grouped'] else max_idx

# --- COLORS & LABELS ---
if cfg['family']:
    cmap = ListedColormap(["#ffaf03", "#039a00"])
    labels = ['<111>{110}','<100>{110}']
elif cfg['grouped']:
    cmap = ListedColormap([
        "#f5a400", "#802080", "#888888", "#0000ff",
        "#ff69b4", "#808000", "#00e5ff", "#ff0000",
        "#66f0e3", "#a0522d", "#000000", "#ffff00"
    ])
    labels = [f'SS {i+1}' for i in range(len(sel_idx))]
else:
    cmap = ListedColormap([
        '#e6194b','#3cb44b','#ffe119','#4363d8','#f58231','#911eb4','#46f0f0','#f032e6',
        '#bcf60c','#fabebe','#008080','#e6beff','#9a6324','#fffac8','#800000','#aaffc3',
        '#808000','#ffd8b1','#000075','#808080','#ffffff','#000000','#d2691e','#00ffff']
    )
    labels = [f'SS {i+1}' for i in range(len(ss))]

# --- PLOTTING ---
tri = Delaunay(pts)
fc = mode(idx_final[tri.simplices],axis=1).mode.flatten()
cent = pts[tri.simplices].mean(1)

if cfg['full']:
    alpha = np.ones_like(fc,float)
else:
    mask = tri_path.contains_points(cent)
    alpha = np.zeros_like(fc,float)
    alpha[mask] = 1.0

fig,ax = plt.subplots(figsize=(7,7))
tpc = ax.tripcolor(pts[:,0],pts[:,1],tri.simplices,facecolors=fc,cmap=cmap,edgecolors='none',shading='flat',alpha=alpha)

for label, (v_start, v_end, style) in trace_lines.items():
    # 1. Generate 3D points along the Great Circle arc
    # Increase 'm' in slerp if the curve looks jagged
    arc_points_3d = slerp(v_start, v_end, m=100)
    
    # 2. Project to 2D and Apply Rotation (R)
    # matches existing logic: pts = np.array([proj(v) for v in ori]) @ R.T
    line_2d = np.array([proj(p) for p in arc_points_3d]) @ R.T
    
    # 3. Plot
    ax.plot(line_2d[:, 0], line_2d[:, 1], style, lw=1.5, label=label)

if not cfg['full']:
    ax.plot(p12[:,0],p12[:,1],'k-',lw=1)
    ax.plot(p23[:,0],p23[:,1],'k-',lw=1)
    ax.plot(p31[:,0],p31[:,1],'k-',lw=1)

ax.set_aspect('equal')
ax.axis('off')
ax.set_title(title,fontsize=12)
patches = [Patch(color=cmap(i),label=labels[i]) for i in range(len(labels))]
ax.legend(handles=patches,loc='center left',bbox_to_anchor=(1.22,0.5),frameon=False)

# highlight points
for k,v in highlight.items():
    p = proj(v) @ R.T
    ax.plot(p[0],p[1],'ro')
    ax.text(p[0]+0.02,p[1]+0.02,k,fontsize=9)

plt.tight_layout()
plt.show()