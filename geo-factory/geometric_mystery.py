import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import random

W, H = 1080, 1920
FPS = 30
DURATION = 30
TOTAL_FRAMES = FPS * DURATION


def lerp(a, b, t):
    return a + (b - a) * t


def ease_in_out(t):
    return t * t * (3 - 2 * t)


def polygon_points(cx, cy, r, n, rotation=0):
    pts = []
    for i in range(n):
        angle = 2 * math.pi * i / n + rotation
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    return pts


def color_cycle(t, palette):
    n = len(palette)
    idx = t * n
    i = int(idx) % n
    j = (i + 1) % n
    frac = idx - int(idx)
    c1, c2 = palette[i], palette[j]
    return tuple(int(lerp(c1[k], c2[k], frac)) for k in range(3))


PALETTES = [
    [(8, 8, 24), (0, 200, 255), (200, 50, 255), (0, 255, 180)],
    [(12, 4, 20), (255, 50, 100), (255, 220, 50), (50, 255, 150)],
    [(4, 12, 20), (120, 80, 255), (30, 200, 255), (255, 120, 80)],
    [(8, 8, 16), (0, 255, 128), (255, 0, 128), (128, 128, 255)],
]

SHAPES = [3, 4, 5, 6, 8, 12, 7, 9]


def draw_frame(frame_idx):
    t = frame_idx / TOTAL_FRAMES
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    pal_idx = int(t * len(PALETTES)) % len(PALETTES)
    palette = PALETTES[pal_idx]
    bg = color_cycle(t * 0.2, palette)
    draw.rectangle([0, 0, W, H], fill=tuple(max(0, c - 40) for c in bg))

    cx, cy = W / 2, H / 2

    cycle = t * 6
    shape_idx = int(cycle) % len(SHAPES)
    next_idx = (shape_idx + 1) % len(SHAPES)
    morph = ease_in_out(cycle - int(cycle))

    pulse = 0.7 + 0.3 * math.sin(t * math.pi * 4)

    for layer in range(8, 0, -1):
        layer_t = (t * 0.8 + layer * 0.12) % 1.0
        radius = lerp(60, 380, layer / 8) * pulse
        rot_speed = (1.5 - layer * 0.15) * (1 if layer % 2 == 0 else -1)
        rot = t * math.pi * rot_speed

        n1 = SHAPES[shape_idx] + layer
        n2 = SHAPES[next_idx] + layer
        sides = n1 if morph < 0.5 else n2

        color = color_cycle(layer_t + t * 0.4, palette)
        fade = 1.0 - layer / 10

        pts = polygon_points(cx, cy, radius, sides, rot)
        r, g, b = color
        fill = (int(r * fade), int(g * fade), int(b * fade))
        outline = (min(255, r + 80), min(255, g + 80), min(255, b + 80))

        draw.polygon(pts, fill=fill, outline=outline)

        inner = polygon_points(cx, cy, radius * 0.7, sides, rot + math.pi / sides)
        inner_fill = (int(r * fade * 0.4), int(g * fade * 0.4), int(b * fade * 0.4))
        draw.polygon(inner, fill=inner_fill, outline=outline)

        for px, py in pts:
            dot_r = 3 + 2 * math.sin(t * math.pi * 6 + layer * 0.8)
            draw.ellipse(
                [px - dot_r, py - dot_r, px + dot_r, py + dot_r],
                fill=outline,
            )

    num_rings = 5
    for ring in range(num_rings):
        ring_r = 350 + ring * 40
        ring_n = 16 + ring * 4
        for i in range(ring_n):
            angle = 2 * math.pi * i / ring_n + t * math.pi * (0.5 + ring * 0.3)
            x = cx + ring_r * math.cos(angle)
            y = cy + ring_r * math.sin(angle)
            if 0 < x < W and 0 < y < H:
                size = max(1, 2 + 1.5 * math.sin(t * 8 + i * 0.5 + ring))
                c = color_cycle(t * 0.5 + i / ring_n + ring * 0.2, palette)
                draw.ellipse([x - size, y - size, x + size, y + size], fill=c)

    num_particles = 30
    for i in range(num_particles):
        seed = i * 137.508
        angle = t * (1 + (i % 5) * 0.3) + seed
        r = 100 + 200 * ((math.sin(seed) + 1) / 2)
        r *= 0.8 + 0.2 * math.sin(t * 3 + seed)
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        if 0 < x < W and 0 < y < H:
            size = max(1, 1 + 2 * math.sin(t * 10 + seed))
            c = color_cycle(t + i / num_particles, palette)
            draw.ellipse([x - size, y - size, x + size, y + size], fill=c)

    return img


def generate(output="geometric_mystery.mp4"):
    out = Path(output)
    print(f"generating {TOTAL_FRAMES} frames ({DURATION}s @ {FPS}fps)...")
    tmp_dir = Path("_geo_frames")
    tmp_dir.mkdir(exist_ok=True)

    for i in range(TOTAL_FRAMES):
        img = draw_frame(i)
        img.save(tmp_dir / f"f{i:04d}.png")
        if i % (FPS * 2) == 0:
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
