"""Lumen 'Ember Ridge' :30 launch spot + 9:16 :15 cutdown + broadcast master, edited in filmcraft.

Media: effectcraft renders, lightcraft graded stills, photocraft story post (craft-made); music/lumen-jingle-30s.mp3 (ElevenLabs).
Run:  python -I -X utf8 build_spot.py <filmcraft-cli.exe>
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from mcpclient import Craft  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.dirname(HERE)
OUT = os.path.join(HERE, "out")
TPS = 254016000000  # ticks per second
FX = os.path.join(P, "effectcraft", "out", "renders")
LC = os.path.join(P, "lightcraft", "out", "web-jpeg-srgb-2048")
MEDIA = {
    "sting": os.path.join(FX, "lumen-logo-sting_1080p30.mp4"),
    "title": os.path.join(FX, "title-card-ember-ridge_1080p30.mp4"),
    "end": os.path.join(FX, "end-card_1080p30.mp4"),
    "lt_origin": os.path.join(FX, "lower-third-origin_prores4444_alpha.mov"),
    "lt_mara": os.path.join(FX, "lower-third-mara_prores4444_alpha.mov"),
    # 30 s instrumental jingle (ElevenLabs Music v2.5); replaced the effectcraft sine-chord temp score
    "score": os.path.join(HERE, "music", "lumen-jingle-30s.mp3"),
    # lightcraft full-size 16-bit sRGB master (3000x2000): the bean shots are 1:1 crops of it, no upscaling
    "wide": os.path.join(P, "lightcraft", "out", "video-master-srgb-16bit-full", "LUM_0001_wide.tif"),
    "label": os.path.join(LC, "LUM_0002_label-detail.jpg"),
    "story": os.path.join(P, "photocraft", "out", "social", "story", "ember-ridge-story-post.jpg"),
}

c = None


def run(cid, p=None):
    return c.call("command_run", {"id": cid, "params": p or {}})


def T(s):
    return int(round(s * TPS))


def items_by_path():
    tree = c.call("project_inspect")
    names = {}

    def walk(node):
        if isinstance(node, dict):
            if "item" in node and "name" in node:
                names[node["name"]] = node["item"]
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)
    walk(tree)
    return {k: names.get(os.path.basename(v)) for k, v in MEDIA.items()}, tree


def new_item(r):
    """Item id from a command result (generators return the new project item)."""
    if isinstance(r, dict):
        for k in ("item", "id", "items"):
            if k in r:
                return r[k][0] if isinstance(r[k], list) else r[k]
    return r


def clip_id(r):
    if isinstance(r, dict):
        for k in ("clip", "id", "clips"):
            if k in r:
                return r[k][0] if isinstance(r[k], list) else r[k]
    return r


def place(item, track, start, dur, src_in=0.0):
    r = run("timeline.place", {"item": item, "track": track, "seconds": start, "insert": False,
                               "duration": T(dur), "sourceIn": T(src_in)})
    cid = clip_id(r)
    if not isinstance(cid, int):
        print("place result:", json.dumps(r)[:300])
    return cid


def motion(clip, param, kfs):
    """kfs: [(clip-relative seconds, value)]; one pair sets a static value."""
    if len(kfs) == 1:
        run("effects.setParam", {"clip": clip, "effect": "motion", "param": param, "value": kfs[0][1]})
        return
    for t, v in kfs:
        run("effects.setParam", {"clip": clip, "effect": "motion", "param": param, "value": v, "time": T(t)})


def main(exe):
    global c
    os.makedirs(OUT, exist_ok=True)
    c = Craft([exe, "mcp"])
    log = {}

    # ---------- :30 spot ----------
    run("file.newSequence", {"name": "Lumen Ember Ridge 30 - 1080p30", "width": 1920, "height": 1080, "fps": 30,
                             "video": 3, "audio": 2})
    log["import"] = run("file.import", {"paths": list(MEDIA.values())})
    ids, tree = items_by_path()
    json.dump(tree, open(os.path.join(OUT, "project-tree.json"), "w"), indent=1)
    print("items:", ids)
    matte = run("file.newColorMatte", {"color": "#1d1410", "seconds": 30})
    matte_id = new_item(matte)
    print("matte:", matte)

    v1 = []
    v1.append(place(ids["sting"], "V1", 0, 5))
    v1.append(place(ids["title"], "V1", 5, 4))
    wide = place(ids["wide"], "V1", 9, 6)
    v1.append(wide)
    motion(wide, "scale", [(0, 64), (6, 70)])
    # label detail is 4:5: fitted to height over a Roast colour matte
    place(matte_id, "V1", 15, 4)
    lab = place(ids["label"], "V2", 15, 4)
    motion(lab, "scale", [(0, 80), (4, 86)])
    # bean close-ups: the 3000 px master at 100 %, framed on each cluster (anchor = image centre 1500,1000)
    br = place(ids["wide"], "V1", 19, 4)
    v1.append(br)
    motion(br, "scale", [(0, 100), (4, 104)])
    motion(br, "position", [(0, [420, 80]), (4, [400, 70])])
    bl = place(ids["wide"], "V1", 23, 3)
    v1.append(bl)
    motion(bl, "scale", [(0, 100)])
    motion(bl, "position", [(0, [1500, 80]), (3, [1440, 80])])
    v1.append(place(ids["end"], "V1", 26, 4))
    # lower thirds (ProRes 4444 with alpha) on V3
    place(ids["lt_origin"], "V3", 9.5, 5.5)
    place(ids["lt_mara"], "V3", 18.6, 6)
    # dissolves between picture cuts
    for clip in v1[1:]:
        try:
            run("sequence.applyVideoTransition", {"clip": clip, "effect": "cross_dissolve", "frames": 12, "edge": "in"})
        except RuntimeError as e:
            print("transition:", str(e)[-200:])
    # jingle on A1, -6 dB under picture
    score = place(ids["score"], "A1", 0, 30)
    run("clip.audioGain", {"clips": [score], "mode": "set", "db": -6})
    # captions for accessibility
    run("captions.newTrack", {"format": "Subtitle", "name": "English", "language": "en"})
    for t, d, s in ((1.0, 3.5, "Lumen Coffee Roasters"), (5.3, 3.4, "New single origin: Ember Ridge."),
                    (9.6, 5.0, "Grown at 2,100 m in Guji, Ethiopia. Washed."),
                    (15.2, 3.6, "Bergamot, ripe apricot, cacao nib."),
                    (19.2, 3.6, "Roasted light-medium by Mara Okafor, Head Roaster."),
                    (23.1, 2.7, "Whole bean, 340 g."), (26.3, 3.4, "Available now at lumen-coffee.example")):
        run("captions.add", {"track": "C1", "text": s, "seconds": t, "durationSeconds": d})
    log["sequence_30"] = c.call("sequence_inspect")
    for sec in (2.5, 7, 12, 17, 21, 24.5, 28):
        img = c.call("render_frame", {"seconds": sec})
        log.setdefault("frames", []).append(sec)

    # exports of the :30
    ex = {
        "lumen-ember-ridge-30_1080p30_h264.mp4": {"format": "h264", "bitrateKbps": 16000, "bitrateMode": "vbr2Pass",
                                                  "loudnessLufs": -16, "captionSidecar": "srt"},
        "lumen-ember-ridge-30_1080p30_prores-hq.mov": {"format": "prores", "proresProfile": "hq"},
        # smaller ProRes for the public repo (the HQ master is over GitHub's 100 MB file limit)
        "lumen-ember-ridge-30_1080p30_prores-proxy.mov": {"format": "prores", "proresProfile": "proxy"},
    }
    for name, opts in ex.items():
        log["export:" + name] = run("file.exportMedia", dict(opts, path=os.path.join(OUT, name), wait=True))
        print(name, json.dumps(log["export:" + name])[:240])
    for fmt, ext in (("edl", "edl"), ("xml", "xml"), ("fcpxml", "fcpxml"), ("otio", "otio")):
        log["interchange:" + fmt] = run("file.exportInterchange",
                                        {"format": fmt, "path": os.path.join(OUT, "interchange", "lumen-ember-ridge-30." + ext)})
    log["captions"] = run("captions.export", {"path": os.path.join(OUT, "lumen-ember-ridge-30.en.srt"), "track": "C1"})

    # ---------- 9:16 :15 cutdown ----------
    run("file.newSequence", {"name": "Lumen Ember Ridge 15 - 9x16", "width": 1080, "height": 1920, "fps": 30,
                             "video": 2, "audio": 1})
    m2 = run("file.newColorMatte", {"color": "#1d1410", "seconds": 15})
    m2_id = new_item(m2)
    st = place(ids["story"], "V1", 0, 6)
    motion(st, "scale", [(0, 100), (6, 106)])
    place(m2_id, "V1", 6, 9)
    lb2 = place(ids["label"], "V2", 6, 4.5)
    motion(lb2, "scale", [(0, 100), (4.5, 108)])
    ec = place(ids["end"], "V2", 10.5, 4.5)
    motion(ec, "scale", [(0, 100)])
    for clip in (lb2, ec):
        try:
            run("sequence.applyVideoTransition", {"clip": clip, "effect": "cross_dissolve", "frames": 10, "edge": "in"})
        except RuntimeError as e:
            print("transition:", str(e)[-200:])
    # last 15 s of the jingle, so the cutdown ends on its final chord with the end card
    sc2 = place(ids["score"], "A1", 0, 15, src_in=15)
    run("clip.audioGain", {"clips": [sc2], "mode": "set", "db": -6})
    try:
        run("sequence.applyAudioTransition", {"clip": sc2, "frames": 45})
    except RuntimeError as e:
        print("audio transition:", str(e)[-200:])
    log["sequence_15"] = c.call("sequence_inspect")
    log["export:916"] = run("file.exportMedia", {"path": os.path.join(OUT, "lumen-ember-ridge-15_1080x1920_h264.mp4"),
                                                 "format": "h264", "bitrateKbps": 12000, "loudnessLufs": -14, "wait": True})
    print("916", json.dumps(log["export:916"])[:240])

    run("file.saveAs", {"path": os.path.join(OUT, "lumen-ember-ridge.fcproj")}) if True else None
    json.dump(log, open(os.path.join(OUT, "build-log.json"), "w"), indent=1, default=str)
    c.close()


if __name__ == "__main__":
    main(sys.argv[1])
