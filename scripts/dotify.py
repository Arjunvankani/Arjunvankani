#!/usr/bin/env python3
"""
dotify.py — convert a photo into a dot-matrix SVG "portrait".

Usage:
    python scripts/dotify.py assets/jacket.jpg -o assets/portrait \
        --cols 100 --equalize --detail 0.5 --color

Produces a single portrait.svg (colour mode) that looks good on both
light and dark GitHub themes, since dots are drawn with their own
sampled colour rather than a single foreground colour.
"""
import argparse
from PIL import Image, ImageOps


def build_svg(img: Image.Image, cols: int, detail: float, color: bool) -> str:
    w, h = img.size
    cell = w / cols
    rows = max(1, round(h / cell))
    cell_h = h / rows

    small = img.resize((cols, rows), Image.LANCZOS)
    gray = ImageOps.grayscale(small)

    out_w, out_h = 600, round(600 * rows / cols)
    dot_w = out_w / cols
    dot_h = out_h / rows
    max_r = min(dot_w, dot_h) / 2 * 0.92

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {out_w} {out_h}" '
        f'width="{out_w}" height="{out_h}">'
    ]
    parts.append(f'<rect width="{out_w}" height="{out_h}" fill="none"/>')

    px = small.convert("RGB").load()
    gpx = gray.load()

    for y in range(rows):
        for x in range(cols):
            brightness = gpx[x, y] / 255.0
            # darker pixel -> bigger dot (more "ink"), scaled by detail
            r = max_r * (1 - brightness) ** (1.0 / max(detail, 0.05))
            if r < 0.35:
                continue
            cx = x * dot_w + dot_w / 2
            cy = y * dot_h + dot_h / 2
            if color:
                cr, cg, cb = px[x, y]
                fill = f"rgb({cr},{cg},{cb})"
            else:
                fill = "var(--dot-color, #39D353)"
            parts.append(
                f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.2f}" fill="{fill}"/>'
            )

    parts.append("</svg>")
    return "\n".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("-o", "--out", default="assets/portrait")
    ap.add_argument("--cols", type=int, default=90)
    ap.add_argument("--detail", type=float, default=0.5)
    ap.add_argument("--equalize", action="store_true")
    ap.add_argument("--color", action="store_true")
    args = ap.parse_args()

    img = Image.open(args.image).convert("RGB")
    if args.equalize:
        img = ImageOps.equalize(img)

    svg = build_svg(img, args.cols, args.detail, args.color)
    out_path = f"{args.out}.svg"
    with open(out_path, "w") as f:
        f.write(svg)
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
