"""Lumen Coffee Roasters — brand identity system, built headless with vectorcraft-cli (MCP).

Run:  python -I -X utf8 build_identity.py <path-to-vectorcraft-cli.exe>
Writes everything into ./out next to this script.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from mcpclient import Craft  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(os.path.join(OUT, "eps"), exist_ok=True)
os.makedirs(OUT, exist_ok=True)

BLEED = 8.504  # 3 mm in pt
MM = 2.834645

# CMYK brand palette (print masters). Hex values are the screen references.
PALETTE = [
    # name, cmyk, hex, spot?, usage
    ("Lumen Roast", (60, 72, 75, 82), "#1d1410", False, "Primary dark. Backgrounds, body type."),
    ("Lumen Ember", (0, 58, 88, 0), "#f2843a", True, "Signature colour. Bean, accents. Spot plate."),
    ("Lumen Gold", (0, 27, 92, 0), "#f9bb2b", False, "Sun ring. Highlights, never body type."),
    ("Lumen Crema", (0, 5, 14, 0), "#fdf2e0", False, "Paper tone. Light backgrounds."),
    ("Lumen Clay", (22, 58, 72, 10), "#b06a45", False, "Secondary type, origin details."),
]

c = None


def rc(cmd, p=None):
    return c.call("run_command", {"command": cmd, "params": p or {}})


def sel(ids):
    rc("select.set", {"ids": list(ids)})


def bounds(ids):
    sel(ids)
    return c.call("inspect_document")["selectionBounds"]


def fill(ids, sw):
    rc("paint.setFill", {"swatch": sw, "ids": list(ids)})
    rc("paint.setStroke", {"none": True, "ids": list(ids)})


def rect(x, y, w, h, sw=None, radius=None):
    p = {"x": x, "y": y, "width": w, "height": h}
    if radius:
        p["radius"] = radius
    i = rc("shape.rectangle", p)["id"]
    if sw:
        fill([i], sw)
    return i


def ellipse(cx, cy, r, sw=None):
    i = rc("shape.ellipse", {"x": cx - r, "y": cy - r, "width": 2 * r, "height": 2 * r})["id"]
    if sw:
        fill([i], sw)
    return i


def stroke_only(ids, sw, weight, dash=None):
    rc("paint.setFill", {"none": True, "ids": list(ids)})
    rc("paint.setStroke", {"swatch": sw, "ids": list(ids)})
    p = {"weight": weight, "ids": list(ids)}
    if dash:
        p["dash"] = dash
    rc("stroke.set", p)


def text(x, y, s, size, sw, font="Bahnschrift", style="Regular", tracking=0):
    p = {"x": x, "y": y, "text": s, "size": size, "font": font, "style": style}
    t = rc("text.create", p)["id"]
    if tracking:
        rc("text.setStyle", {"id": t, "tracking": tracking})
    fill([t], sw)
    return t


def outline(ids):
    sel(ids)
    return rc("type.createOutlines")["ids"]


def move_center(ids, cx=None, cy=None):
    b = bounds(ids)
    dx = 0 if cx is None else cx - (b["x"] + b["width"] / 2)
    dy = 0 if cy is None else cy - (b["y"] + b["height"] / 2)
    rc("object.move", {"dx": dx, "dy": dy})


def group(ids):
    sel(ids)
    return rc("object.group")["id"]


def mark(cx, cy, R, sun, bean):
    """Sun ring (16-point star minus a circle) + coffee bean (ellipse minus an S-crease)."""
    s = rc("shape.star", {"cx": cx, "cy": cy, "radius1": R, "radius2": R * 0.773, "points": 16})["id"]
    hole = ellipse(cx, cy, R * 0.606)
    sel([s, hole])
    ring = rc("object.pathfinder.minusFront")["ids"]
    bw, bh = R * 0.655, R * 0.8
    b = rc("shape.ellipse", {"x": cx - bw / 2, "y": cy - bh / 2, "width": bw, "height": bh})["id"]
    k = R / 330.0
    P = lambda x, y: f"{cx + x * k:.3f} {cy + y * k:.3f}"
    d = (f"M {P(0, -128)} C {P(-74, -46)}, {P(74, 46)}, {P(0, 128)} "
         f"C {P(36, 46)}, {P(-36, -46)}, {P(0, -128)} Z")
    cr = rc("path.create", {"d": d, "closed": True})["id"]
    sel([b, cr])
    beanp = rc("object.pathfinder.minusFront")["ids"]
    fill(ring, sun)
    fill(beanp, bean)
    return group(ring + beanp)


def stacked(ox, oy, W, sun, bean, word, tag):
    cx = ox + W / 2
    R = W * 0.27
    m = mark(cx, oy + W * 0.36, R, sun, bean)
    w = outline([text(ox, oy + W * 0.82, "LUMEN", W * 0.17, word, style="Bold", tracking=160)])
    t = outline([text(ox, oy + W * 0.905, "COFFEE ROASTERS", W * 0.046, tag, style="SemiLight", tracking=520)])
    move_center(w, cx=cx)
    move_center(t, cx=cx)
    g = group([m] + w + t)
    move_center([g], cx=cx, cy=oy + W / 2)
    return g


def horizontal(ox, oy, W, H, sun, bean, word, tag):
    R = H * 0.37
    m = mark(ox + R + 10, oy + H / 2, R, sun, bean)
    x0 = ox + 2 * R + 50
    w = outline([text(x0, oy + H / 2 + H * 0.12, "LUMEN", H * 0.46, word, style="Bold", tracking=120)])
    t = outline([text(x0 + 4, oy + H / 2 + H * 0.29, "COFFEE ROASTERS", H * 0.105, tag, style="SemiLight", tracking=560)])
    g = group([m] + w + t)
    move_center([g], cx=ox + W / 2, cy=oy + H / 2)
    return g


def main(exe):
    global c
    c = Craft([exe, "mcp", "--headless"])
    log = []

    def note(k, v):
        log.append({k: v})
        print(k, json.dumps(v)[:300])

    # Document: CMYK, points, 3 mm bleed
    ab = [  # name, x, y, w, h
        ("01 Primary Stacked", 0, 0, 600, 600),
        ("02 Horizontal", 700, 0, 1000, 320),
        ("03 Mark", 1800, 0, 600, 600),
        ("04 App Icon", 2500, 0, 512, 512),
        ("05 One-Colour Black", 0, 700, 600, 600),
        ("06 Reversed", 700, 700, 600, 600),
        ("07 Clear Space", 1400, 700, 800, 800),
        ("08 Bag Label 100x140mm", 2300, 700, 100 * MM, 140 * MM),
        ("09 Business Card Front", 0, 1600, 252, 144),
        ("10 Business Card Back", 350, 1600, 252, 144),
        ("11 Colour Palette", 700, 1600, 1000, 440),
        ("12 Reversed No Background", 1800, 1600, 600, 600),
    ]
    rc("file.new", {"name": "lumen-identity", "width": ab[0][3], "height": ab[0][4],
                    "units": "Points", "colorMode": "cmyk", "backgroundContents": "transparent"})
    rc("artboard.setProps", {"index": 0, "name": ab[0][0], "x": 0, "y": 0})
    for name, x, y, w, h in ab[1:]:
        rc("artboard.new", {"x": x, "y": y, "width": w, "height": h, "name": name})
    rc("document.setup", {"bleed": BLEED})
    rc("select.none")
    rc("paint.setStroke", {"none": True})

    for name, (cc, mm, yy, kk), _hex, spot, _u in PALETTE:
        p = {"name": name, "color": {"c": cc, "m": mm, "y": yy, "k": kk}, "mode": "cmyk", "global": True}
        if spot:
            p["spot"] = True
        note("swatch", rc("swatch.new", p))
    rc("swatch.new", {"name": "Lumen Black", "color": {"c": 0, "m": 0, "y": 0, "k": 100}, "mode": "cmyk", "global": True})
    rc("swatch.new", {"name": "Dieline", "color": {"c": 0, "m": 100, "y": 0, "k": 0}, "mode": "cmyk", "spot": True})

    rc("layer.setProps", {"name": "Artwork"})
    art_layer = c.call("inspect_document")["currentLayer"]

    # 01 Primary stacked
    x, y, W = 0, 0, 600
    stacked(x, y, W, "Lumen Gold", "Lumen Ember", "Lumen Roast", "Lumen Clay")
    # 02 Horizontal
    horizontal(700, 0, 1000, 320, "Lumen Gold", "Lumen Ember", "Lumen Roast", "Lumen Clay")
    # 03 Mark only
    mark(2100, 300, 250, "Lumen Gold", "Lumen Ember")
    # 04 App icon (screen asset)
    rect(2500, 0, 512, 512, "Lumen Roast", radius=115)
    mark(2756, 256, 178, "Lumen Gold", "Lumen Ember")
    # 05 One-colour black
    stacked(0, 700, 600, "Lumen Black", "Lumen Black", "Lumen Black", "Lumen Black")
    # 06 Reversed on Roast (background runs into the bleed)
    rect(700 - BLEED, 700 - BLEED, 600 + 2 * BLEED, 600 + 2 * BLEED, "Lumen Roast")
    stacked(700, 700, 600, "Lumen Gold", "Lumen Ember", "Lumen Crema", "Lumen Gold")
    # 07 Clear space
    g = stacked(1550, 850, 500, "Lumen Gold", "Lumen Ember", "Lumen Roast", "Lumen Clay")
    b = bounds([g])
    X = 500 * 0.27 / 2  # half the sun radius
    rc("layer.new", {"name": "Annotations"})
    guide = rect(b["x"] - X, b["y"] - X, b["width"] + 2 * X, b["height"] + 2 * X)
    stroke_only([guide], "Lumen Ember", 1.25, dash=[8, 5])
    xm = rect(b["x"] - X, b["y"] - X, X, X)
    stroke_only([xm], "Lumen Ember", 1.25)
    text(b["x"] - X + 8, b["y"] - X - 10, "X = half the sun radius", 14, "Lumen Ember", style="SemiBold")
    text(1440, 1440, "Keep clear space of X on every side. Minimum size: 25 mm wide in print, 120 px on screen.",
         15, "Lumen Roast", style="Regular")
    text(1440, 1465, "Never stretch, recolour outside the palette, add effects, or place the mark on busy imagery.",
         15, "Lumen Clay", style="Regular")
    rc("layer.setCurrent", {"id": art_layer})

    # 08 Bag label 100 x 140 mm, 3 mm bleed, 5 mm safe area
    ox, oy, lw, lh = 2300, 700, 100 * MM, 140 * MM
    rect(ox - BLEED, oy - BLEED, lw + 2 * BLEED, lh + 2 * BLEED, "Lumen Crema")
    rect(ox - BLEED, oy - BLEED, lw + 2 * BLEED, 118 + BLEED, "Lumen Roast")
    hl = horizontal(ox + 10, oy + 14, lw - 20, 90, "Lumen Gold", "Lumen Ember", "Lumen Crema", "Lumen Gold")
    L = ox + 22
    text(L, oy + 152, "SINGLE ORIGIN  ·  LOT 07", 8, "Lumen Clay", style="SemiBold", tracking=380)
    text(L, oy + 188, "EMBER RIDGE", 32, "Lumen Roast", style="Bold", tracking=40)
    text(L, oy + 208, "Ethiopia · Guji · Washed · 2,100 m", 11.5, "Lumen Clay", font="Georgia", style="Italic")
    rect(L, oy + 222, lw - 44, 0.9, "Lumen Ember")
    text(L, oy + 244, "TASTES LIKE", 7.5, "Lumen Roast", style="SemiBold", tracking=380)
    text(L, oy + 262, "Bergamot, ripe apricot, cacao nib", 11.5, "Lumen Roast", font="Georgia")
    text(L, oy + 290, "ROAST", 7.5, "Lumen Roast", style="SemiBold", tracking=380)
    for i in range(5):
        d = ellipse(L + 6 + i * 20, oy + 306, 6)
        if i < 2:
            fill([d], "Lumen Ember")
        else:
            stroke_only([d], "Lumen Roast", 0.9)
    text(L, oy + 326, "LIGHT", 6, "Lumen Clay", style="SemiBold", tracking=200)
    text(L + 74, oy + 326, "DARK", 6, "Lumen Clay", style="SemiBold", tracking=200)
    text(L + 140, oy + 290, "BREW", 7.5, "Lumen Roast", style="SemiBold", tracking=380)
    text(L + 140, oy + 305, "Filter · Espresso", 9.5, "Lumen Roast", font="Georgia")
    text(L, oy + 352, "WHOLE BEAN  ·  340 g / 12 oz", 9, "Lumen Roast", style="Bold", tracking=120)
    text(L, oy + 370, "ROASTED ON  ______________", 7.5, "Lumen Roast", style="SemiBold", tracking=200)
    rc("layer.new", {"name": "Dieline"})
    die = rect(ox, oy, lw, lh, radius=5 * MM)
    stroke_only([die], "Dieline", 0.5)
    rc("object.setOverprint", {"stroke": True, "ids": [die]})
    rc("layer.setCurrent", {"id": art_layer})

    # 09/10 Business card 3.5 x 2 in
    ox, oy = 0, 1600
    rect(ox - BLEED, oy - BLEED, 252 + 2 * BLEED, 144 + 2 * BLEED, "Lumen Roast")
    mark(ox + 126, oy + 60, 38, "Lumen Gold", "Lumen Ember")
    w = outline([text(ox, oy + 122, "LUMEN", 15, "Lumen Crema", style="Bold", tracking=320)])
    move_center(w, cx=ox + 126)
    ox = 350
    rect(ox - BLEED, oy - BLEED, 252 + 2 * BLEED, 144 + 2 * BLEED, "Lumen Crema")
    text(ox + 20, oy + 40, "Mara Okafor", 14, "Lumen Roast", style="SemiBold")
    text(ox + 20, oy + 54, "Head Roaster", 9, "Lumen Clay", font="Georgia", style="Italic")
    rect(ox + 20, oy + 66, 36, 1.2, "Lumen Ember")
    text(ox + 20, oy + 92, "+1 (555) 014-2290", 7.5, "Lumen Roast")
    text(ox + 20, oy + 104, "mara@lumen-coffee.example", 7.5, "Lumen Roast")
    text(ox + 20, oy + 116, "214 Foundry Lane · Portland, OR 97209", 7.5, "Lumen Roast")
    mark(ox + 222, oy + 38, 17, "Lumen Gold", "Lumen Ember")

    # 11 Colour palette
    ox, oy = 700, 1600
    text(ox + 20, oy + 40, "Colour palette", 24, "Lumen Roast", style="SemiBold")
    for i, (name, (cc, mm, yy, kk), hx, spot, usage) in enumerate(PALETTE):
        tx = ox + 20 + i * 196
        sw = rect(tx, oy + 60, 180, 210, name)
        if name == "Lumen Crema":  # light tile needs a keyline
            rc("paint.setStroke", {"swatch": "Lumen Clay", "ids": [sw]})
            rc("stroke.set", {"weight": 0.75, "ids": [sw]})
        text(tx, oy + 296, name + (" (spot)" if spot else ""), 14, "Lumen Roast", style="SemiBold")
        text(tx, oy + 316, f"CMYK {cc} / {mm} / {yy} / {kk}", 10.5, "Lumen Roast")
        text(tx, oy + 332, f"Screen {hx}", 10.5, "Lumen Roast")
        words, line, yy2 = usage.split(), "", oy + 354
        for wd in words:  # simple wrap at ~28 chars
            if len(line) + len(wd) > 28:
                text(tx, yy2, line.strip(), 10, "Lumen Clay")
                line, yy2 = "", yy2 + 14
            line += wd + " "
        text(tx, yy2, line.strip(), 10, "Lumen Clay")

    # 12 Reversed lockup without a background, for placing on Roast in layouts
    stacked(1800, 1600, 600, "Lumen Gold", "Lumen Ember", "Lumen Crema", "Lumen Gold")

    # ---- Saves and exports ----
    note("save_native", rc("document.save", {"path": os.path.join(OUT, "lumen-identity.vectorcraft")}))
    note("save_ai", rc("document.save", {"path": os.path.join(OUT, "lumen-identity.ai"), "format": "ai"}))
    note("pdf_presentation", rc("document.exportPdf", {"path": os.path.join(OUT, "lumen-identity-presentation.pdf")}))
    note("pdf_print_x4", rc("document.exportPdf", {
        "path": os.path.join(OUT, "lumen-print-label-cards-PDFX4.pdf"), "artboards": [7, 8, 9],
        "standard": "pdfX4", "marks": {"trim": True, "registration": True, "colorBars": True, "pageInfo": True},
        "bleed": {"useDocument": True}}))
    note("eps_logos", rc("document.exportEps", {"path": os.path.join(OUT, "eps", "lumen-logo.eps"),
                                                 "useArtboards": True, "artboards": [0, 1, 2, 4, 5, 11]}))
    note("screens", rc("document.exportForScreens", {
        "folder": os.path.join(OUT, "screens"), "artboards": [0, 1, 2, 4, 5, 6, 7, 8, 9, 10],
        "subfolders": True, "formats": [{"format": "svg"}, {"format": "png", "scale": 1},
                                        {"format": "png", "scale": 2}]}))
    note("app_icon", rc("document.exportForScreens", {
        "folder": os.path.join(OUT, "app-icon"), "artboards": [3],
        "formats": [{"format": "png", "width": w, "suffix": f"-{w}"} for w in (1024, 512, 192, 180, 32, 16)]
                   + [{"format": "svg"}]}))
    json.dump(log, open(os.path.join(OUT, "build-log.json"), "w"), indent=1)
    c.close()


if __name__ == "__main__":
    main(sys.argv[1])
