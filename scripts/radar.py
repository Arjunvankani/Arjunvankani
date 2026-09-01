#!/usr/bin/env python3
"""
radar.py — draw the self-rated skill radar chart from assets/skills.json
into assets/radar-dark.svg and assets/radar-light.svg.

Run manually:
    python scripts/radar.py

Run automatically by .github/workflows/radar.yml whenever
assets/skills.json changes.
"""
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "assets" / "skills.json").read_text())

THEMES = {
    "dark": dict(bg="none", fg="#c9d1d9", grid="#30363d", line="#39D353", fill="#39D35333"),
    "light": dict(bg="none", fg="#24292f", grid="#d0d7de", line="#6a11cb", fill="#6a11cb33"),
}


def draw(theme_name: str):
    t = THEMES[theme_name]
    labels = [a["label"] for a in DATA["axes"]]
    values = [a["value"] for a in DATA["axes"]]
    n = len(labels)

    angles = [i / n * 2 * math.pi for i in range(n)]
    angles += angles[:1]
    values_closed = values + values[:1]

    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    ax.set_theta_offset(math.pi / 2)
    ax.set_theta_direction(-1)

    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels([])
    ax.spines["polar"].set_color(t["grid"])
    ax.grid(color=t["grid"], linewidth=0.8)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, color=t["fg"], fontsize=9, fontfamily="monospace")

    ax.plot(angles, values_closed, color=t["line"], linewidth=2)
    ax.fill(angles, values_closed, color=t["fill"])

    ax.set_title(DATA.get("title", "Skills"), color=t["fg"], fontfamily="monospace", pad=20)

    out = ROOT / "assets" / f"radar-{theme_name}.svg"
    fig.savefig(out, transparent=True, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out}")


if __name__ == "__main__":
    for theme in THEMES:
        draw(theme)
