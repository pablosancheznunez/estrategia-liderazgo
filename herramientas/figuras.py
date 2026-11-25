"""Genera las figuras del libro (SVG) en figuras/.

Uso, desde la raíz del libro:   python3 herramientas/figuras.py [--png]
Paleta categórica validada (orden fijo): azul, naranja, aguamarina, amarillo, magenta.
"""
import pathlib, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch

RAIZ = pathlib.Path(__file__).resolve().parent.parent
OUT = RAIZ / "figuras"; OUT.mkdir(exist_ok=True)

S = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]
TINTA, TINTA2, GRIS, SUP = "#0b0b0b", "#52514e", "#d9d8d4", "#ffffff"
CAJA, CAJA2 = "#eef0f6", "#c9cfe0"

plt.rcParams.update({
    "font.family": ["Inter", "DejaVu Sans"], "font.size": 11,
    "svg.fonttype": "path", "figure.facecolor": SUP, "axes.facecolor": SUP,
})


def lienzo(w, h, xlim, ylim):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect("equal"); ax.axis("off")
    return fig, ax


def guardar(fig, nombre):
    fig.savefig(OUT / nombre, format="svg", bbox_inches="tight", pad_inches=0.15)
    if "--png" in sys.argv:
        pathlib.Path("/tmp/figpng").mkdir(exist_ok=True)
        fig.savefig(pathlib.Path("/tmp/figpng") / nombre.replace(".svg", ".png"), dpi=100, bbox_inches="tight")
    plt.close(fig); print("ok", nombre)


def caja(ax, x, y, w, h, texto, fc=CAJA, ec=CAJA2, tc=TINTA, fs=10, r=0.08, lw=1.2, peso="normal"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw))
    if texto:
        ax.text(x + w / 2, y + h / 2, texto, ha="center", va="center", fontsize=fs, color=tc,
                linespacing=1.2, fontweight=peso)


def flecha(ax, a, b, color=TINTA2, rad=0.0):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=12, color=color, lw=1.3,
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=2, shrinkB=2))


def pagina(ax, x, y, w, h, titulo):
    caja(ax, x, y, w, h, None, fc=SUP, ec=TINTA2, r=0.06)
    ax.add_patch(FancyBboxPatch((x, y + h - 0.35), w, 0.35, boxstyle="round,pad=0,rounding_size=0.06",
                                fc=CAJA, ec=TINTA2, lw=1.2))
    ax.text(x + 0.15, y + h - 0.175, titulo, ha="left", va="center", fontsize=9, color=TINTA2)
    for i in range(5):
        ax.plot([x + 0.2, x + w - 0.2 - (0.5 if i % 2 else 0)], [y + h - 0.7 - i * 0.32] * 2,
                color=GRIS, lw=3, solid_capstyle="round")





def e1_alon():
    fig, ax = lienzo(7.2, 5.0, (0, 10.5), (0, 7.4))
    cs = [((1, 3.7), "Lo mejor", "Viable y valioso", S[2]), ((5.6, 3.7), "Apuesta a largo plazo", "Para cuando hay experiencia", S[3]),
          ((1, 0.6), "Para aprender", "Buen comienzo", S[0]), ((5.6, 0.6), "Evitar", "Mucho esfuerzo, poca ganancia", "#a3a29e")]
    for (x, y), t, st, c in cs:
        ax.add_patch(FancyBboxPatch((x, y), 4.4, 2.9, boxstyle="round,pad=0,rounding_size=0.12", fc=c, ec="none", alpha=0.22))
        ax.text(x + 2.2, y + 1.75, t, ha="center", fontsize=12.5, fontweight="bold", color=TINTA)
        ax.text(x + 2.2, y + 1.05, st, ha="center", fontsize=10, color=TINTA2)
    flecha(ax, (1, 0.25), (10.1, 0.25)); ax.text(5.55, -0.25, "Dificultad", ha="center", fontsize=11, color=TINTA)
    flecha(ax, (0.6, 0.6), (0.6, 7.0)); ax.text(0.15, 3.8, "Ganancia de conocimiento", rotation=90, va="center", ha="center", fontsize=11, color=TINTA)
    guardar(fig, "e1_alon.svg")


def e3_desarrollo():
    fig, ax = lienzo(9.0, 4.0, (0, 13), (0, 5.6))
    for x, tit, sub, items, c in ((0.3, "Desarrollo del líder", "capital humano", ["Autoconocimiento", "Regulación emocional", "Competencias sociales", "Identidad como líder"], S[0]),
                                  (7.7, "Desarrollo del liderazgo", "capital social", ["Confianza", "Redes", "Compromiso mutuo", "Aprendizaje colectivo"], S[2])):
        ax.add_patch(FancyBboxPatch((x, 0.2), 5.0, 5.1, boxstyle="round,pad=0,rounding_size=0.15", fc=c, ec="none", alpha=0.15))
        ax.text(x + 2.5, 4.75, tit, ha="center", fontsize=12.5, fontweight="bold", color=TINTA)
        ax.text(x + 2.5, 4.25, sub, ha="center", fontsize=10, color=TINTA2, style="italic")
        for i, t in enumerate(items):
            caja(ax, x + 0.5, 3.15 - i * 0.9, 4.0, 0.7, t, fs=10.5)
    flecha(ax, (5.45, 2.75), (7.55, 2.75)); ax.text(6.5, 3.05, "sostiene", ha="center", fontsize=9.5, color=TINTA2)
    guardar(fig, "e3_desarrollo.svg")


def e5_gantt():
    fig, ax = plt.subplots(figsize=(9.5, 3.4))
    pts = [("PT1 · Revisión y diseño", 0, 6, S[0]), ("PT2 · Recogida de datos", 4, 12, S[1]), ("PT3 · Análisis", 10, 18, S[2]), ("PT4 · Difusión", 15, 22, S[4])]
    for i, (t, a, b, c) in enumerate(pts):
        y = 3 - i
        ax.add_patch(FancyBboxPatch((a + 0.05, y - 0.3), b - a - 0.1, 0.6, boxstyle="round,pad=0,rounding_size=0.15", fc=c, ec="none"))
        ax.text(-0.4, y, t, ha="right", va="center", fontsize=10.5, color=TINTA)
    ax.add_patch(plt.Rectangle((22, -0.5), 2, 4.0, fc="#a3a29e", alpha=0.25, ec="none")); ax.text(23, 3.62, "margen", ha="center", fontsize=9, color=TINTA2)
    for m, t in ((6, "Diseño\ncerrado"), (12, "Datos\ndepurados"), (18, "Resultados")):
        ax.plot([m], [-0.75], marker="D", ms=9, color=TINTA); ax.text(m, -1.35, t, ha="center", va="top", fontsize=8.8, color=TINTA2)
    ax.set_xlim(0, 24); ax.set_ylim(-2.2, 3.8)
    ax.set_xticks(range(0, 25, 3)); ax.set_xticklabels([f"M{m}" for m in range(0, 25, 3)], fontsize=9, color=TINTA2)
    ax.set_yticks([]); [ax.spines[s].set_visible(False) for s in ("top", "right", "left")]
    ax.spines["bottom"].set_color(GRIS); ax.tick_params(colors=GRIS, labelcolor=TINTA2)
    ax.grid(axis="x", color=GRIS, lw=0.6); ax.set_axisbelow(True)
    guardar(fig, "e5_gantt.svg")


if __name__ == "__main__":
    e1_alon(); e3_desarrollo(); e5_gantt()
