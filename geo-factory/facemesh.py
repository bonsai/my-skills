import math
from pathlib import Path
from PIL import Image, ImageDraw

W, H = 1080, 1920
FPS = 30
DURATION = 10
TOTAL_FRAMES = FPS * DURATION

CX, CY = W // 2, H // 2 - 100

FACE_R = 280
EYE_R = 35
MOUTH_W = 120
NOSE_H = 60

def lerp(a, b, t):
    return a + (b - a) * t

def ease(t):
    return t * t * (3 - 2 * t)

def rotate_z(pts, angle, cx=0, cy=0):
    cos_a, sin_a = math.cos(angle), math.sin(angle)
    return [
        (cx + (x - cx) * cos_a - (y - cy) * sin_a,
         cy + (x - cx) * sin_a + (y - cy) * cos_a,
         z)
        for x, y, z in pts
    ]

def rotate_y(pts, angle, cx=0, cy=0, cz=0):
    cos_a, sin_a = math.cos(angle), math.sin(angle)
    return [
        (cx + (x - cx) * cos_a - (z - cz) * sin_a, y,
         cz + (x - cx) * sin_a + (z - cz) * cos_a)
        for x, y, z in pts
    ]

def project(pts_3d, fov=600):
    return [
        (int(CX + x * fov / (fov + z)), int(CY + y * fov / (fov + z)))
        for x, y, z in pts_3d
    ]

def generate_face_points():
    pts = []
    for i in range(468):
        angle = i * 2.399963
        r = FACE_R * (0.3 + 0.7 * (i % 7) / 6)
        layer = i // 7
        z = -50 + 100 * (layer / 66)
        x = r * math.cos(angle) * (1 - abs(z) / 200)
        y = r * math.sin(angle) * (1.3 - abs(z) / 300)
        pts.append((x, y, z))
    return pts

def eye_pts(cx, cy, t, expr):
    pts = []
    for i in range(36):
        angle = 2 * math.pi * i / 36
        ry = lerp(EYE_R, EYE_R * 0.3, expr.get("blink", 0))
        rx = lerp(EYE_R * 1.2, EYE_R * 0.8, expr.get("squint", 0))
        x = cx + rx * math.cos(angle)
        y = cy + ry * math.sin(angle) + 5 * math.sin(t * 3 + i * 0.5)
        z = 20
        pts.append((x, y, z))
    return pts

def mouth_pts(cx, cy, t, expr):
    pts = []
    open_amt = expr.get("mouth_open", 0)
    smile = expr.get("smile", 0)
    for i in range(40):
        angle = 2 * math.pi * i / 40
        w = MOUTH_W * (1 + 0.3 * smile)
        h = 25 + 40 * open_amt
        x = cx + w * math.cos(angle) * (1 + 0.2 * math.sin(angle * 3))
        y = cy + h * math.sin(angle) * (1 + 0.5 * smile * math.sin(angle))
        z = 30
        pts.append((x, y, z))
    return pts

def nose_pts(cx, cy, t):
    pts = []
    for i in range(12):
        angle = 2 * math.pi * i / 12
        r = 15 + 5 * math.sin(t * 2 + i)
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle) * 0.5 + NOSE_H * 0.3
        z = 40
        pts.append((x, y, z))
    for i in range(8):
        angle = 2 * math.pi * i / 8
        x = cx + 8 * math.cos(angle)
        y = cy + NOSE_H + 5 * math.sin(angle)
        z = 45
        pts.append((x, y, z))
    return pts

def eyebrow_pts(cx, cy, t, expr, side=1):
    pts = []
    raise_amt = expr.get("eyebrow_raise", 0)
    furrow = expr.get("furrow", 0)
    for i in range(16):
        frac = i / 15
        x = cx + side * lerp(40, 130, frac)
        y = cy - 50 - raise_amt * 20 + furrow * 10 * math.sin(frac * math.pi)
        y += 3 * math.sin(t * 2 + i * 0.4)
        z = 25
        pts.append((x, y, z))
    return pts

EXPRESSIONS = [
    {"blink": 0, "squint": 0, "mouth_open": 0, "smile": 0, "eyebrow_raise": 0, "furrow": 0},
    {"blink": 0, "squint": 0, "mouth_open": 0.8, "smile": 0, "eyebrow_raise": 0.8, "furrow": 0},
    {"blink": 0, "squint": 0.5, "mouth_open": 0, "smile": 1, "eyebrow_raise": 0, "furrow": 0},
    {"blink": 1, "squint": 0, "mouth_open": 0.3, "smile": 0, "eyebrow_raise": 0, "furrow": 1},
    {"blink": 0, "squint": 0, "mouth_open": 1, "smile": 0.5, "eyebrow_raise": 1, "furrow": 0},
    {"blink": 0, "squint": 1, "mouth_open": 0, "smile": 0, "eyebrow_raise": 0, "furrow": 1},
    {"blink": 0, "squint": 0, "mouth_open": 0.5, "smile": 1, "eyebrow_raise": 0.5, "furrow": 0},
]

def lerp_expr(e1, e2, t):
    return {k: lerp(e1.get(k, 0), e2.get(k, 0), t) for k in e1}

def draw_frame(frame_idx):
    t = frame_idx / TOTAL_FRAMES
    img = Image.new("RGB", (W, H), (5, 5, 15))
    draw = ImageDraw.Draw(img)

    cycle = t * len(EXPRESSIONS)
    idx = int(cycle) % len(EXPRESSIONS)
    next_idx = (idx + 1) % len(EXPRESSIONS)
    morph = ease(cycle - int(cycle))
    expr = lerp_expr(EXPRESSIONS[idx], EXPRESSIONS[next_idx], morph)

    rot_y = math.sin(t * math.pi * 2) * 0.3
    rot_z = math.sin(t * math.pi * 1.5) * 0.1

    base = generate_face_points()
    rotated = rotate_y(base, rot_y, 0, 0, 0)
    rotated = rotate_z(rotated, rot_z, 0, 0)
    projected = project(rotated)

    for i, (px, py) in enumerate(projected):
        depth = rotated[i][2]
        brightness = int(80 + 175 * (1 - (depth + 100) / 250))
        pulse = 0.8 + 0.2 * math.sin(t * 6 + i * 0.1)
        g = int(brightness * 0.4 * pulse)
        b = int(brightness * pulse)
        r = int(brightness * 0.2 * pulse)
        size = max(1, int(2 + 1.5 * (1 - abs(depth) / 100)))
        draw.ellipse([px - size, py - size, px + size, py + size], fill=(r, g, b))

    left_eye = eye_pts(CX - 90, CY - 30, t, expr)
    right_eye = eye_pts(CX + 90, CY - 30, t, expr)
    mouth = mouth_pts(CX, CY + 100, t, expr)
    nose = nose_pts(CX, CY + 20, t)
    left_brow = eyebrow_pts(CX - 90, CY - 30, t, expr, side=-1)
    right_brow = eyebrow_pts(CX + 90, CY - 30, t, expr, side=1)

    contour = []
    for i in range(60):
        angle = 2 * math.pi * i / 60
        r = FACE_R * (1 + 0.05 * math.sin(angle * 5 + t * 2))
        x = r * math.cos(angle)
        y = r * 1.3 * math.sin(angle)
        z = -30 + 20 * math.sin(angle * 3)
        contour.append((x, y, z))

    contour_rot = rotate_y(contour, rot_y, 0, 0, 0)
    contour_rot = rotate_z(contour_rot, rot_z, 0, 0)
    contour_proj = project(contour_rot)

    for i in range(len(contour_proj)):
        j = (i + 1) % len(contour_proj)
        x1, y1 = contour_proj[i]
        x2, y2 = contour_proj[j]
        depth = contour_rot[i][2]
        c = int(40 + 60 * (1 - (depth + 100) / 250))
        draw.line([(x1, y1), (x2, y2)], fill=(0, c, c), width=1)

    for pts, color in [
        (left_eye, (0, 255, 200)),
        (right_eye, (0, 255, 200)),
        (mouth, (200, 50, 100)),
        (nose, (0, 180, 150)),
        (left_brow, (0, 200, 180)),
        (right_brow, (0, 200, 180)),
    ]:
        pts_rot = rotate_y(pts, rot_y, 0, 0, 0)
        pts_rot = rotate_z(pts_rot, rot_z, 0, 0)
        pts_proj = project(pts_rot)
        for i, (px, py) in enumerate(pts_proj):
            depth = pts_rot[i][2]
            fade = 0.5 + 0.5 * (1 - (depth + 100) / 200)
            r, g, b = color
            c = (int(r * fade), int(g * fade), int(b * fade))
            sz = max(2, int(3 + 1.5 * fade))
            draw.ellipse([px - sz, py - sz, px + sz, py + sz], fill=c)

    for ring in range(3):
        ring_r = 380 + ring * 30
        for i in range(20):
            angle = 2 * math.pi * i / 20 + t * (1 + ring * 0.3)
            x = CX + ring_r * math.cos(angle)
            y = CY + ring_r * 1.3 * math.sin(angle)
            sz = 1 + math.sin(t * 8 + i * 0.5)
            alpha = 0.3 + 0.2 * math.sin(t * 4 + ring)
            draw.ellipse([x - sz, y - sz, x + sz, y + sz],
                         fill=(int(30 * alpha), int(80 * alpha), int(100 * alpha)))

    return img


def generate(output="facemesh.mp4"):
    out = Path(output)
    print(f"generating {TOTAL_FRAMES} frames ({DURATION}s @ {FPS}fps)...")
    tmp_dir = Path("_face_frames")
    tmp_dir.mkdir(exist_ok=True)

    for i in range(TOTAL_FRAMES):
        img = draw_frame(i)
        img.save(tmp_dir / f"f{i:04d}.png")
        if i % FPS == 0:
            print(f"  {i}/{TOTAL_FRAMES}  ({i*100//TOTAL_FRAMES}%)")

    print("encoding mp4...")
    import subprocess
    subprocess.run([
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(tmp_dir / "f%04d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-preset", "fast",
        "-movflags", "faststart",
        str(out),
    ], check=True, capture_output=True)

    for f in tmp_dir.glob("*.png"):
        f.unlink()
    tmp_dir.rmdir()

    abs_path = str(out.resolve())
    print(f"\n{'='*60}")
    print(f"output: {abs_path}")
    print(f"{'='*60}")


if __name__ == "__main__":
    generate()
