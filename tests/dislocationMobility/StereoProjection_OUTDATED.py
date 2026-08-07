import numpy as np
import matplotlib.pyplot as plt

def normalize(v):
    return np.array(v) / np.linalg.norm(v)

def stereographic_projection(v):
    v = normalize(v)
    if v[2] < 0:
        v = -v
    return np.array([v[0] / (1 + v[2]), v[1] / (1 + v[2])])

def slerp(v0, v1, num_points=300):
    v0 = normalize(v0)
    v1 = normalize(v1)
    dot = np.clip(np.dot(v0, v1), -1.0, 1.0)
    theta = np.arccos(dot)
    if np.isclose(theta, 0):
        return np.array([v0] * num_points)
    sin_theta = np.sin(theta)
    return np.array([
        (np.sin((1 - t) * theta) * v0 + np.sin(t * theta) * v1) / sin_theta
        for t in np.linspace(0, 1, num_points)
    ])

def minor_circle_arc(v1, v2, num_points=300):
    v1 = normalize(v1)
    v2 = normalize(v2)
    axis = normalize(np.cross(v1, v2))
    if np.linalg.norm(axis) < 1e-8:
        return np.array([v1] * num_points)
    theta = np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0))
    return np.array([
        np.cos(t) * v1 + np.sin(t) * (np.cross(axis, v1))
        for t in np.linspace(0, theta, num_points)
    ])

def rotate_2d(points, angle_deg):
    theta = np.deg2rad(angle_deg)
    R = np.array([
        [np.cos(theta), np.sin(theta)],
        [-np.sin(theta), np.cos(theta)]
    ])
    return np.dot(points, R.T)

def plot_stereographic_triangle(corner_dict, rotation_deg=0,
                                addPoints=None,
                                chiLine=None,
                                addLines=None):
    proj_pts = {
        label: rotate_2d(stereographic_projection(vec).reshape(1, 2), rotation_deg)[0]
        for label, vec in corner_dict.items()
    }

    labels = list(corner_dict.keys())
    arcs = []
    for i in range(3):
        vi = corner_dict[labels[i]]
        vj = corner_dict[labels[(i + 1) % 3]]
        arc = slerp(vi, vj)
        arc_proj = np.array([stereographic_projection(p) for p in arc])
        arcs.append(rotate_2d(arc_proj, rotation_deg))

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect('equal')
    ax.axis('off')

    for arc in arcs:
        ax.plot(arc[:, 0], arc[:, 1], 'k', lw=4)

    for label, pt in proj_pts.items():
        ax.plot(*pt, 'ko')
        ax.text(pt[0] + 0.03, pt[1] + 0.01, label, fontsize=18)

    if addPoints:
        for label, vec in addPoints.items():
            pt = rotate_2d(stereographic_projection(vec).reshape(1, 2), rotation_deg)[0]
            ax.plot(*pt, 'ro', markersize=20)
            ax.text(pt[0] + 0.03, pt[1] + 0.01, label, fontsize=18, color='r')

    if chiLine:
        chi_arc = slerp(*chiLine)
        chi_arc_proj = np.array([stereographic_projection(p) for p in chi_arc])
        chi_arc_rot = rotate_2d(chi_arc_proj, rotation_deg)
        ax.plot(chi_arc_rot[:, 0], chi_arc_rot[:, 1], 'r--', lw=1.2, label=r'$\chi = 0$')

    if addLines:
        for v1, v2 in addLines:
            dot = np.dot(normalize(v1), normalize(v2))
            arc = minor_circle_arc(v1, v2) if dot >= 0.85 else slerp(v1, v2)
            arc_proj = np.array([stereographic_projection(p) for p in arc])
            arc_rot = rotate_2d(arc_proj, rotation_deg)
            ax.plot(arc_rot[:, 0], arc_rot[:, 1], 'k', lw=2)

    all_x = np.concatenate([arc[:, 0] for arc in arcs])
    all_y = np.concatenate([arc[:, 1] for arc in arcs])
    pad = 0.05
    ax.set_xlim(all_x.min() - pad, all_x.max() + pad)
    ax.set_ylim(all_y.min() - pad, all_y.max() + pad)

    fig.patch.set_alpha(0.7)  # Transparent figure background
    ax.patch.set_alpha(0.7)   # Transparent axes background


    #plt.legend()
    #plt.title("Stereographic Triangle", fontsize=12)
    plt.show()


# Input Block
triCorners = {
    #'[1̄1̄2]': [-1, -1, 2],
    #'[111]': [1, 1, 1],
    #'[2̄11]': [-2, 1, 1]
    #'[001]': [0,0,1],
    #'[1̄11]': [-1,1,1],
    #'[011]': [0,1,1],
    '[001]': [0,0,1],
    '[011]': [1,0,1],
    '[111]': [1,1,1],
}

points = {
    #'[001]': [0, 0, 1],
    '[111]': [1, 1, 1],
    #'[011]': [1, 0, 1],
    #'Crystal 3': [-5/6, 5/6, 1],
    #'Crystal 9': [-0.6, 0.75, 1]
}

chiZero = ([-1, 0, 1], [1, 1, 1])

addLines = [
    ([0, 0, 1], [0, 1, 1]),
    ([0, 0, 1], [-1, 1, 1]),
]

plot_stereographic_triangle(
    triCorners,
    addPoints=points,
    #chiLine=chiZero,
    #addLines=addLines
)