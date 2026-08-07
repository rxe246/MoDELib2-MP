import sys, os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from scipy.spatial import Delaunay
from scipy.stats import mode
sys.path.append("../../build/tools/pyMoDELib")
import pyMoDELib
sys.path.append("../../python")
from modlibUtils import *

plt.rcParams['text.usetex'] = False

def normalize(v):
    return np.array(v) / np.linalg.norm(v)

def stereographic_projection(v):
    v = normalize(v)
    if v[2] < 0:
        v = -v
    return np.array([v[0] / (1 + v[2]), v[1] / (1 + v[2])])

grouped_mode = True

# Final 12 slip systems specified by user (indices into the 24 total list)
selected_indices = [5, 2, 10, 14, 22, 13, 23, 16, 8, 6, 0, 18]
slip_systems_full = [
    ([1, 1, -1], [1, 0, 1]), ([-1, -1, 1], [1, 0, 1]),
    ([-1, 1, 1], [1, 0, 1]), ([1, -1, -1], [1, 0, 1]),
    ([-1, -1, -1], [-1, 0, 1]), ([1, 1, 1], [-1, 0, 1]),
    ([1, -1, 1], [-1, 0, 1]), ([-1, 1, -1], [-1, 0, 1]),
    ([1, -1, 1], [0, 1, 1]), ([-1, 1, -1], [0, 1, 1]),
    ([1, 1, -1], [0, 1, 1]), ([-1, -1, 1], [0, 1, 1]),
    ([-1, -1, -1], [0, 1, -1]), ([1, 1, 1], [0, 1, -1]),
    ([-1, 1, 1], [0, 1, -1]), ([1, -1, -1], [0, 1, -1]),
    ([-1, 1, 1], [1, 1, 0]), ([1, -1, -1], [1, 1, 0]),
    ([1, -1, 1], [1, 1, 0]), ([-1, 1, -1], [1, 1, 0]),
    ([-1, -1, -1], [1, -1, 0]), ([1, 1, 1], [1, -1, 0]),
    ([1, 1, -1], [1, -1, 0]), ([-1, -1, 1], [1, -1, 0])
]
if grouped_mode:
    selected_indices = [5, 2, 10, 14, 22, 13, 23, 16, 8, 6, 0, 18]
    slip_systems = [slip_systems_full[i] for i in selected_indices]
    group_map = np.arange(12)
else:
    slip_systems = slip_systems_full

slip_systems = [(normalize(np.array(b)), normalize(np.array(n))) for b, n in slip_systems]

corner_vectors = np.array([
    normalize([-1, -1, 2]),
    normalize([1, 1, 1]),
    normalize([-2, 1, 1])
])

num_points = 500
bary_coords = []
for i in range(num_points + 1):
    for j in range(num_points + 1 - i):
        k = num_points - i - j
        b = np.array([i, j, k]) / num_points
        bary_coords.append(b)
bary_coords = np.array(bary_coords)
orientations = np.dot(bary_coords, corner_vectors)
projected_points = np.array([stereographic_projection(v) for v in orientations])
R = np.array([[0, 1], [-1, 0]])  # rotate -90°
projected_points = projected_points @ R.T

materialFile = "../../Library/Materials/W.txt"
T = 300
s0 = 0.01
mat = pyMoDELib.PolycrystallineMaterialBase(materialFile, T)
mob = pyMoDELib.DislocationMobilityBCC(mat)

max_slip_indices = []
for m in orientations:
    m = normalize(m)
    S = np.outer(m, m) * s0
    v_all = [mob.velocity(S, b, b, n, T) for b, n in slip_systems]
    max_slip_indices.append(np.argmax(v_all))
max_slip_indices = np.array(max_slip_indices)

group_map = np.arange(12)
if grouped_mode:
    colors = [
        "#f5a400", "#802080", "#888888", "#0000ff",
        "#ff69b4", "#808000", "#00e5ff", "#ff0000",
        "#66f0e3", "#a0522d", "#000000", "#ffff00"
    ]
    cmap = ListedColormap(colors)
    labels = [
        r'$\langle 111 \rangle\{\bar{1}01\}$', r'$\langle \bar{1}11 \rangle\{101\}$',
        r'$\langle 11\bar{1} \rangle\{011\}$', r'$\langle \bar{1}11 \rangle\{01\bar{1}\}$',
        r'$\langle 11\bar{1} \rangle\{1\bar{1}0\}$', r'$\langle 111 \rangle\{01\bar{1}\}$',
        r'$\langle 111 \rangle\{1\bar{1}0\}$', r'$\langle \bar{1}11 \rangle\{110\}$',
        r'$\langle 1\bar{1}1 \rangle\{011\}$', r'$\langle 1\bar{1}1 \rangle\{\bar{1}01\}$',
        r'$\langle 11\bar{1} \rangle\{101\}$', r'$\langle 1\bar{1}1 \rangle\{110\}$'
    ]
else:
    labels = [f'SS {i+1}' for i in range(24)]
    tab24 = [
        '#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4',
        '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff',
        '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1',
        '#000075', '#808080', '#ffffff', '#000000', '#d2691e', '#00ffff'
    ]
    cmap = ListedColormap(tab24)

indices = group_map[max_slip_indices] if grouped_mode else max_slip_indices

fig, ax = plt.subplots(figsize=(6, 6))
tri = Delaunay(projected_points)
facecolors = mode(indices[tri.simplices], axis=1).mode.flatten()
tpc = ax.tripcolor(projected_points[:, 0], projected_points[:, 1], tri.simplices,
                   facecolors=facecolors, cmap=cmap, edgecolors='none', shading='flat')
ax.set_aspect('equal')
ax.axis('off')
ax.set_title("Max-Velocity Slip System", fontsize=12)

patches = [Patch(color=cmap(i), label=labels[i]) for i in range(len(labels))]
ax.legend(handles=patches, loc='center left', bbox_to_anchor=(1.22, 0.5), frameon=False)

# --- Add key points and SLERP arcs on triangle ---
def slerp(v0, v1, num_points=200):
    v0, v1 = normalize(v0), normalize(v1)
    dot = np.clip(np.dot(v0, v1), -1.0, 1.0)
    theta = np.arccos(dot)
    sin_theta = np.sin(theta)
    return np.array([
        (np.sin((1 - t) * theta) * v0 + np.sin(t * theta) * v1) / sin_theta
        for t in np.linspace(0, 1, num_points)
    ])

# Special directions for point labels
special_dirs = {
    '[001]': normalize([0, 0, 1]),
    '[011]': normalize([0, 1, 1]),
    '[-111]': normalize([-1, 1, 1]),
    '[-101]': normalize([-1, 0, 1]),
    '[-1-12]': normalize([-1, -1, 2]),
    '[111]': normalize([1, 1, 1]),
    '[-211]': normalize([-2, 1, 1])
}

# Project and plot points
proj_pts = {k: stereographic_projection(v) @ R.T for k, v in special_dirs.items()}
for label, pt in proj_pts.items():
    ax.plot(pt[0], pt[1], 'ko', zorder=5)
    ax.text(pt[0] + 0.02, pt[1] + 0.02, label, fontsize=9, weight='bold', zorder=6)

# SLERP arcs
pairs = [('[001]', '[011]'), ('[011]', '[-111]'), ('[-111]', '[001]'),
         ('[-101]', '[001]'), ('[-101]', '[-111]'),
         ('[-211]', '[-1-12]'), ('[-211]', '[111]'), ('[-1-12]', '[111]')]
for a, b in pairs:
    arc = slerp(special_dirs[a], special_dirs[b])
    arc_proj = np.array([stereographic_projection(v) @ R.T for v in arc])
    ax.plot(arc_proj[:, 0], arc_proj[:, 1], 'k-', lw=1.5, zorder=4)

plt.tight_layout()
plt.show()
