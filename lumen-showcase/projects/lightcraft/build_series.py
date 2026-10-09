"""Lumen 'Ember Ridge' shoot — catalogue, develop one look, sync, rate, tag, deliver. Built in lightcraft.

The four frames in ./shoot were rendered by photocraft (16-bit TIFF). They are not camera RAW files.
Run:  python -I -X utf8 build_series.py <lightcraft-cli.exe>
"""
import json
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from mcpclient import Craft  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HERE, "library")
OUT = os.path.join(HERE, "out")

LOOK = {  # "Lumen Warm Matte"
    "wb.temp": 6900, "wb.tint": 4,
    "light.exposure": 0.12, "light.contrast": 12, "light.highlights": -18, "light.shadows": 10,
    "light.whites": 6, "light.blacks": 8,
    "curve.shadows": 10, "curve.darks": 4, "curve.lights": 4,
    "color.vibrance": 10, "color.saturation": -4,
    "mixer.orange.sat": -8, "mixer.orange.lum": 6, "mixer.yellow.hue": -6,
    "grading.shadows.hue": 30, "grading.shadows.sat": 10,
    "grading.highlights.hue": 45, "grading.highlights.sat": 8,
    "effects.texture": 4, "effects.clarity": 0,
    "vignette.amount": -14, "vignette.midpoint": 40,
    "grain.amount": 12, "grain.size": 20,
    "detail.sharpenAmount": 25, "detail.sharpenRadius": 1.0, "detail.sharpenDetail": 30, "detail.sharpenMasking": 20,
}

META = {
    "LUM_0001_wide": ("Ember Ridge — hero, wide", "Stand-up pouch of Ember Ridge single origin on a walnut table.", 5),
    "LUM_0002_label-detail": ("Ember Ridge — label detail", "Front label: origin, tasting notes, roast level.", 4),
    "LUM_0003_beans-right": ("Ember Ridge — roasted beans, right", "Light-medium roast beans, right cluster.", 3),
    "LUM_0004_beans-left": ("Ember Ridge — roasted beans, left", "Light-medium roast beans, left cluster.", 3),
}


def main(exe):
    shutil.rmtree(LIB, ignore_errors=True)
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(OUT)
    log = {}
    with Craft([exe, "mcp", "--library", LIB]) as c:
        rc = lambda cmd, p=None: c.call("run_command", {"command": cmd, "params": p or {}})
        log["import"] = rc("library.import", {"paths": [os.path.join(HERE, "shoot")], "mode": "copy",
                                              "organize": "flat"})
        photos = c.call("query_photos")
        photos = photos.get("photos", photos) if isinstance(photos, dict) else photos
        ids = {}
        for p in photos:
            stem = os.path.splitext(p.get("fileName") or p.get("name") or p.get("file", ""))[0]
            ids[stem] = p["id"]
        print("photos:", ids)
        all_ids = list(ids.values())
        hero = ids["LUM_0001_wide"]

        # 1 Develop the hero frame, save the look as a preset, sync it to the shoot
        c.call("select_photos", {"ids": [hero], "active": hero})
        log["develop"] = rc("develop.set", {"values": LOOK, "ids": [hero]})
        log["preset"] = rc("preset.create", {"name": "Lumen Warm Matte", "group": "Lumen"})
        c.call("select_photos", {"ids": all_ids, "active": hero})
        log["sync"] = rc("develop.sync", {})
        # per-frame finishing: tighter crop on the label detail (4:5), stronger clarity on bean frames
        c.call("select_photos", {"ids": [ids["LUM_0002_label-detail"]], "active": ids["LUM_0002_label-detail"]})
        rc("crop.aspect", {"aspect": "4x5"})
        for k in ("LUM_0003_beans-right", "LUM_0004_beans-left"):
            rc("develop.set", {"values": {"effects.clarity": 8, "effects.texture": 10}, "ids": [ids[k]]})

        # 2 Catalogue: ratings, pick, metadata, album
        for stem, (title, caption, stars) in META.items():
            rc("photo.rate", {"rating": stars, "ids": [ids[stem]]})
            rc("photo.setMeta", {"ids": [ids[stem]], "title": title, "caption": caption,
                                 "altText": caption,
                                 "copyright": "© 2026 Lumen Coffee Roasters (fictional brand)",
                                 "copyrightStatus": "copyrighted", "creator": "Lumen in-house studio",
                                 "city": "Portland", "state": "OR", "country": "USA",
                                 "keywords": ["Lumen", "Ember Ridge", "coffee", "packaging", "product"]})
        rc("photo.pick", {"ids": [hero]})
        c.call("select_photos", {"ids": all_ids, "active": hero})
        log["album"] = rc("album.create", {"name": "Ember Ridge launch — selects", "addSelected": True})

        log["settings_hero"] = rc("develop.get", {"id": hero})

    # 3 Deliver. Each export runs in its own lightcraft-cli process on the saved library.
    # lightcraft 0.4.0 crashes with "Illegal instruction" (exit 132) on this CPU (i5-12450H, no AVX-512)
    # for every 8-bit encode: JPEG, PNG, WebP, AVIF and 8-bit TIFF. 16-bit TIFF works, resized or not.
    # So lightcraft delivers 16-bit TIFF masters; photocraft makes the 8-bit web files from the sRGB master.
    exports = {
        "web-master-srgb-16bit-2048": ["format=tiff", "longEdge=2048", "colorSpace=sRGB", "bitDepth=16", "ppi=72"],
        "video-master-srgb-16bit-full": ["format=tiff", "longEdge=0", "colorSpace=sRGB", "bitDepth=16", "ppi=72"],
        "print-displayP3-16bit": ["format=tiff", "longEdge=0", "colorSpace=displayP3", "bitDepth=16", "ppi=300"],
        "print-adobeRGB-16bit": ["format=tiff", "longEdge=0", "colorSpace=adobeRGB", "bitDepth=16", "ppi=300"],
    }
    for name, opts in exports.items():
        d = os.path.join(OUT, name)
        os.makedirs(d, exist_ok=True)
        r = subprocess.run([exe, "run", "--library", LIB, "app.export", "dir=" + d,
                            "ids=" + json.dumps(all_ids), *opts], capture_output=True, text=True)
        log["export:" + name] = {"exit": r.returncode, "stdout": r.stdout[-600:]}
        print(name, "exit", r.returncode)
    json.dump(log, open(os.path.join(OUT, "build-log.json"), "w"), indent=1, default=str)


if __name__ == "__main__":
    main(sys.argv[1])
