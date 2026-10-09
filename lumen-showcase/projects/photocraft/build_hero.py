"""Lumen 'Ember Ridge' product hero — layered composite built from scratch in photocraft.

Inputs: only the bag label, which vectorcraft renders here from the identity master (dieline hidden).
Run:  python -I -X utf8 build_hero.py <vectorcraft-cli.exe> <photocraft-cli.exe>
"""
import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from mcpclient import Craft  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # projects/
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
W, H = 3000, 2000
LABEL = os.path.join(OUT, "label-1400w.png")


def render_label(vec_exe):
    """vectorcraft: label artboard (index 7) without the dieline layer, 1400 px wide."""
    master = os.path.join(ROOT, "vectorcraft", "out", "lumen-identity.vectorcraft")
    with Craft([vec_exe, "mcp", "--headless"]) as v:
        rc = lambda cmd, p=None: v.call("run_command", {"command": cmd, "params": p or {}})
        rc("document.open", {"path": master})
        doc = v.call("inspect_document")
        die = [l["id"] for l in doc["layers"] if l["name"] == "Dieline"]
        rc("layer.setProps", {"ids": die, "visible": False})
        r = rc("document.exportForScreens", {"folder": OUT, "artboards": [7],
                                              "formats": [{"format": "png", "width": 1400, "suffix": "-1400w"}]})
        produced = r["files"][0]
        if os.path.abspath(produced) != os.path.abspath(LABEL):
            os.replace(produced, LABEL)
    print("label:", LABEL)


def main(vec_exe, photo_exe):
    render_label(vec_exe)
    c = Craft([photo_exe, "mcp", "--automation-read-root", ROOT, "--automation-write-root", HERE])

    def run(cid, p=None):
        return c.call("command_run", {"id": cid, "params": p or {}})

    def active():
        return c.call("doc_inspect").get("activeLayer")

    def smart_blur(radius):
        run("layer.smartObjects.convertToSmartObject")
        run("filter.blur.gaussianBlur", {"radius": radius})

    def props(**kw):
        run("layer.setProps", kw)

    c.call("doc_new", {"width": W, "height": H, "mode": "rgb", "depth": 16, "background": "#e9d2b0",
                       "name": "lumen-ember-ridge-hero"})

    # 1 Backdrop: warm radial falloff
    run("layer.newFillLayer.gradient", {"from": "#f7e6cb", "to": "#9c6a44", "style": "radial", "angle": 90})
    props(name="Backdrop")
    # soft key-light bloom behind the bag
    run("shape.create", {"kind": "ellipse", "rect": [700, 80, 1600, 1400], "fill": "#fff4e0", "name": "Backdrop bloom"})
    smart_blur(260)
    props(blend="Screen", opacity=0.55)

    # 2 Tabletop with wood grain
    run("shape.create", {"kind": "rect", "rect": [0, 1380, W, H - 1380], "name": "Tabletop",
                         "fill": {"gradient": {"stops": [[0, "#6b4630"], [1, "#24160d"]], "angle": -90}}})
    run("layer.new.layer", {"name": "Wood grain"})
    run("edit.fill", {"contents": "gray"})
    run("filter.noise.addNoise", {"amount": 40, "distribution": "gaussian", "monochromatic": True, "seed": 7})
    run("filter.blur.motionBlur", {"angle": 0, "distance": 600})
    props(blend="Overlay", opacity=0.45, clipped=True)
    # table front edge highlight
    run("shape.create", {"kind": "rect", "rect": [0, 1380, W, 6], "fill": "#c8946a", "name": "Table edge light"})
    props(opacity=0.5)

    # 3 Contact shadows (tight + ambient)
    run("shape.create", {"kind": "ellipse", "rect": [820, 1540, 1360, 220], "fill": "#000000", "name": "Ambient shadow"})
    smart_blur(110)
    props(blend="Multiply", opacity=0.45)
    run("shape.create", {"kind": "ellipse", "rect": [960, 1585, 1080, 70], "fill": "#000000", "name": "Contact shadow"})
    smart_blur(22)
    props(blend="Multiply", opacity=0.8)

    # 4 The bag: matte roast-brown stand-up pouch
    bx, by, bw, bh = 1000, 360, 1000, 1260
    run("shape.create", {"kind": "roundedRect", "rect": [bx, by, bw, bh], "radii": [36, 36, 28, 28], "name": "Bag body",
                         "fill": {"gradient": {"stops": [[0, "#1d130d"], [0.18, "#3a281d"], [0.55, "#473224"],
                                                         [0.85, "#2e1f16"], [1, "#160e09"]], "angle": 0}}})
    run("layer.layerStyle.innerGlow", {"color": "#ffcf96", "opacity": 22, "blend": "screen", "technique": "softer",
                                        "source": "edge", "size": 70})
    run("layer.layerStyle.innerShadow", {"color": "#000000", "opacity": 45, "blend": "multiply", "angle": 120,
                                          "distance": 14, "size": 60, "add": True})
    # heat-seal band with crimp lines
    run("shape.create", {"kind": "roundedRect", "rect": [bx, by, bw, 120], "radii": [36, 36, 0, 0],
                         "fill": "#1a110b", "name": "Seal band"})
    for i in range(7):
        y = by + 22 + i * 13
        run("shape.create", {"kind": "line", "from": [bx + 30, y], "to": [bx + bw - 30, y], "weight": 3,
                             "fill": "#3b2a1f", "name": f"Crimp {i + 1}"})
    run("shape.create", {"kind": "rect", "rect": [bx + 30, by + 128, bw - 60, 4], "fill": "#5a4232", "name": "Tear notch line"})
    props(opacity=0.6)
    # side gussets: soft shading on both edges
    for name, x, stops in (("Gusset left", bx, [[0, "#000000"], [1, "#ffffff"]]),
                           ("Gusset right", bx + bw - 140, [[0, "#ffffff"], [1, "#000000"]])):
        run("shape.create", {"kind": "rect", "rect": [x, by + 120, 140, bh - 150], "name": name,
                             "fill": {"gradient": {"stops": stops, "angle": 0}}})
        props(blend="Multiply", opacity=0.55)

    # 5 Label from vectorcraft, with cylindrical shading
    lw = 700
    # (file.placeEmbedded is disabled over MCP, so open the label and paste it in)
    tx, ty = bx + bw / 2, by + 160 + 980 / 2 + 72
    lh = lw * 1960 / 1400
    # die-cut base: the label is clipped to a 5 mm-radius rounded rectangle, as the dieline specifies
    run("shape.create", {"kind": "roundedRect", "rect": [tx - lw / 2, ty - lh / 2, lw, lh],
                         "radii": lw * 5 / 100, "fill": "#ffffff", "name": "Label die-cut"})
    run("layer.layerStyle.dropShadow", {"color": "#000000", "opacity": 40, "blend": "multiply", "angle": 90,
                                         "distance": 3, "size": 7})
    hero_idx = c.call("session_list")["active"]
    lab = c.call("doc_open", {"path": "photocraft/out/label-1400w.png"})
    run("select.all")
    run("edit.copy")
    c.call("doc_close", {"index": lab["index"]} if isinstance(lab, dict) and "index" in lab else {})
    c.call("doc_select", {"index": hero_idx})
    run("edit.paste")
    run("layer.smartObjects.convertToSmartObject")
    props(name="Label (vectorcraft)")
    lb = next(l for l in c.call("doc_inspect")["layers"] if l.get("name") == "Label (vectorcraft)")
    print("pasted label bounds:", json.dumps({k: lb.get(k) for k in ("bounds", "rect", "x", "y", "width", "height")}))
    s = lw / 1400
    b0 = lb["bounds"]  # the paste lands at the layer's own bounds (top-left here)
    ccx, ccy = (b0[0] + b0[2]) / 2, (b0[1] + b0[3]) / 2
    run("edit.transform", {"matrix": [s, 0, 0, s, tx - s * ccx, ty - s * ccy]})
    props(clipped=True)
    run("layer.layerStyle.gradientOverlay", {"from": "#c9b49b", "to": "#ffffff", "style": "reflected", "angle": 0,
                                             "scale": 100, "opacity": 45, "blend": "multiply"})
    # degassing valve
    run("shape.create", {"kind": "ellipse", "rect": [bx + bw / 2 - 34, by + 146, 68, 68], "fill": "#120b07", "name": "Valve"})
    run("layer.layerStyle.bevelEmboss", {"style": "inner", "technique": "smooth", "depth": 120, "size": 8, "soften": 2,
                                         "angle": 120, "altitude": 35})
    run("shape.create", {"kind": "ellipse", "rect": [bx + bw / 2 - 14, by + 166, 28, 28], "fill": "#2a1d14", "name": "Valve core"})

    # 6 Scattered roasted beans (one master bean, duplicated with transforms)
    bean_w, bean_h = 74, 100
    cx0, cy0 = 200, 200  # master bean drawn off to the side, then moved into place
    run("shape.create", {"kind": "ellipse", "rect": [cx0 - bean_w / 2, cy0 - bean_h / 2, bean_w, bean_h], "name": "Bean",
                         "fill": {"gradient": {"stops": [[0, "#2a160b"], [0.5, "#5b331b"], [1, "#2a160b"]], "angle": 0}}})
    sid = active()
    run("shape.create", {"kind": "path", "addTo": sid, "op": "subtract", "path": {"subpaths": [{"closed": True, "knots": [
        {"anchor": [cx0, cy0 - 46], "out": [cx0 - 20, cy0 - 14]},
        {"anchor": [cx0, cy0 + 46], "in": [cx0 + 20, cy0 + 14], "out": [cx0 + 6, cy0 + 14]},
        {"anchor": [cx0, cy0 - 46], "in": [cx0 - 6, cy0 - 14]}]}]}})
    run("layer.smartObjects.convertToSmartObject")
    run("layer.layerStyle.bevelEmboss", {"style": "inner", "technique": "smooth", "depth": 180, "size": 18, "soften": 6,
                                         "angle": 120, "altitude": 40})
    run("layer.layerStyle.dropShadow", {"color": "#000000", "opacity": 70, "blend": "multiply", "angle": 110,
                                         "distance": 8, "size": 14, "add": True})
    master = active()
    rnd = random.Random(42)
    spots = []
    # two loose clusters on the tabletop, front-left and front-right of the bag, plus strays
    for cxs, cys, n, spread in ((640, 1700, 14, 230), (2330, 1740, 16, 260), (1500, 1840, 6, 520)):
        for _ in range(n):
            spots.append((cxs + rnd.gauss(0, spread * 0.5), cys + rnd.gauss(0, spread * 0.22)))
    bean_ids = []
    for i, (tx, ty) in enumerate(spots):
        run("layer.select", {"layer": master})
        run("layer.duplicate")
        ang = math.radians(rnd.uniform(0, 360))
        s = 0.8 + (ty - 1600) / 900 * 0.5  # nearer beans are larger
        a, b, cc, d = s * math.cos(ang), s * math.sin(ang), -s * math.sin(ang), s * math.cos(ang)
        e = tx - (a * cx0 + cc * cy0)
        f = ty - (b * cx0 + d * cy0)
        run("edit.transform", {"matrix": [a, b, cc, d, e, f]})
        props(name=f"Bean {i + 1:02d}")
        bean_ids.append(active())
    run("layer.select", {"layer": master})
    props(visible=False, name="Bean master (hidden)")
    run("layer.select", {"layer": bean_ids[0]})
    for i in bean_ids[1:]:
        run("layer.select", {"layer": i, "mode": "add"})
    run("layer.groupLayers", {"name": "Beans"})

    # 7 Light and finishing
    run("layer.newFillLayer.gradient", {"from": "#fff1d2", "to": "#1a0f08", "style": "radial", "angle": 45})
    props(name="Key light wrap", blend="Soft Light", opacity=0.35)
    run("layer.newAdjustmentLayer.curves", {"points": [[0, 8], [64, 52], [128, 128], [192, 206], [255, 250]]})
    props(name="Curves (contrast)")
    run("layer.newAdjustmentLayer.colorBalance", {"shadows": [0, 0, -6], "midtones": [6, 0, -8], "highlights": [4, 0, -10]})
    props(name="Colour balance (warm)")
    run("layer.newAdjustmentLayer.vibrance", {"vibrance": 12, "saturation": 0})
    props(name="Vibrance")
    run("layer.new.layer", {"name": "Film grain"})
    run("edit.fill", {"contents": "gray"})
    run("filter.noise.addNoise", {"amount": 6, "distribution": "gaussian", "monochromatic": True, "seed": 3})
    props(blend="Overlay", opacity=0.5)

    out = {}
    for rel in ("out/lumen-ember-ridge-hero.pcraft", "out/lumen-ember-ridge-hero.psd",
                "out/lumen-ember-ridge-hero-master.png", "out/lumen-ember-ridge-hero-master.tif"):
        out[rel] = c.call("doc_save", {"path": rel})
        print(rel, json.dumps(out[rel])[:200])
    tree = c.call("doc_inspect")
    json.dump(tree, open(os.path.join(OUT, "layer-tree.json"), "w"), indent=1)
    c.close()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
