// Lumen Coffee Roasters — brand motion package, built with effectcraft's After Effects-style scripting.
// Comps: Logo Sting (5 s), Title Card Ember Ridge (4 s), Lower Third Mara (6 s), Lower Third Origin (6 s), End Card (4 s).
// 1920x1080, 30 fps. Colours are the vectorcraft palette (screen references).

var W = 1920, H = 1080, FPS = 30;
function rgb(h) { return [parseInt(h.slice(1, 3), 16) / 255, parseInt(h.slice(3, 5), 16) / 255, parseInt(h.slice(5, 7), 16) / 255]; }
var ROAST = rgb("#1d1410"), EMBER = rgb("#f2843a"), GOLD = rgb("#f9bb2b"), CREMA = rgb("#fdf2e0"), CLAY = rgb("#b06a45");

function comp(name, dur, bg) {
    var c = app.project.items.addComp(name, W, H, 1, dur, FPS);
    c.bgColor = bg || ROAST;
    return c;
}

// Ease every keyframe of a property (influence %, out/in)
function ease(prop, infl) {
    infl = infl || 75;
    var dims = prop.value instanceof Array ? prop.value.length : 1;
    if (prop.propertyValueType == PropertyValueType.TwoD_SPATIAL || prop.propertyValueType == PropertyValueType.ThreeD_SPATIAL) dims = 1;
    var e = [];
    for (var i = 0; i < dims; i++) e.push(new KeyframeEase(0, infl));
    for (var k = 1; k <= prop.numKeys; k++) prop.setTemporalEaseAtKey(k, e, e);
}
function keys(prop, list, infl) { // list: [[t, v], ...]
    for (var i = 0; i < list.length; i++) prop.setValueAtTime(list[i][0], list[i][1]);
    ease(prop, infl);
}
function tr(layer, name) { return layer.property("ADBE Transform Group").property(name); }

function text(c, s, opt) {
    var t = c.layers.addText(s);
    var sp = t.property("ADBE Text Properties").property("ADBE Text Document");
    var d = sp.value;
    d.font = opt.font || "Bahnschrift";
    if (opt.style) { try { d.fontStyle = opt.style; } catch (e) {} }
    d.fontSize = opt.size || 60;
    d.fillColor = opt.color || CREMA;
    d.tracking = opt.tracking || 0;
    // Bahnschrift is installed as one variable font; effectcraft exposes only Regular, so Bold is
    // built as a same-colour stroke (2.4% of the size), which matched the vectorcraft Bold wordmark weight.
    if (opt.bold) { d.applyStroke = true; d.strokeColor = opt.color || CREMA; d.strokeWidth = Math.round((opt.size || 60) * 0.024); d.strokeOverFill = false; }
    d.applyFill = true;
    d.justification = opt.left ? ParagraphJustification.LEFT_JUSTIFY : ParagraphJustification.CENTER_JUSTIFY;
    sp.setValue(d);
    t.name = opt.name || s;
    tr(t, "Position").setValue(opt.pos || [W / 2, H / 2]);
    return t;
}
function trackingAnimator(t, from, to, t0, t1) {
    var an = t.property("ADBE Text Properties").property("ADBE Text Animators").addProperty("ADBE Text Animator");
    an.name = "Tracking in";
    var p = an.property("ADBE Text Animator Properties").addProperty("ADBE Text Tracking Amount");
    keys(p, [[t0, from], [t1, to]], 85);
}
function fadeInOut(layer, tIn, dIn, tOut, dOut) {
    var o = tr(layer, "Opacity"), l = [[tIn, 0], [tIn + dIn, 100]];
    if (tOut != null) { l.push([tOut, 100]); l.push([tOut + dOut, 0]); }
    keys(o, l, 70);
}

// ---- The mark as native shape layers: sun ring (star minus circle) + bean (ellipse minus S-crease)
function sunLayer(c, cx, cy, R, color, evenOdd) {
    var L = c.layers.addShape(); L.name = "Sun ring";
    var g = L.property("ADBE Root Vectors Group").addProperty("ADBE Vector Group"); g.name = "Ring";
    var v = g.property("ADBE Vectors Group");
    var st = v.addProperty("ADBE Vector Shape - Star");
    st.property("Type").setValue(1); st.property("Points").setValue(16);
    st.property("Outer Radius").setValue(R); st.property("Inner Radius").setValue(R * 0.773);
    var el = v.addProperty("ADBE Vector Shape - Ellipse"); el.property("Size").setValue([2 * R * 0.606, 2 * R * 0.606]);
    // Lottie players (lottie-web) ignore Merge Paths, so the web version cuts holes with an even-odd fill instead
    if (!evenOdd) { var mg = v.addProperty("ADBE Vector Filter - Merge"); mg.property("Mode").setValue(3); }
    var f = v.addProperty("ADBE Vector Graphic - Fill"); f.property("Color").setValue(color);
    if (evenOdd) f.property("Fill Rule").setValue(2);
    tr(L, "Position").setValue([cx, cy]);
    return L;
}
function beanLayer(c, cx, cy, R, color, evenOdd) {
    var L = c.layers.addShape(); L.name = "Bean";
    var g = L.property("ADBE Root Vectors Group").addProperty("ADBE Vector Group"); g.name = "Bean";
    var v = g.property("ADBE Vectors Group");
    var el = v.addProperty("ADBE Vector Shape - Ellipse"); el.property("Size").setValue([R * 0.655, R * 0.8]);
    var k = R / 330, sh = new Shape();
    sh.vertices = [[0, -128 * k], [0, 128 * k]];
    sh.inTangents = [[-36 * k, 82 * k], [74 * k, -82 * k]];
    sh.outTangents = [[-74 * k, 82 * k], [36 * k, -82 * k]];
    sh.closed = true;
    var pg = v.addProperty("ADBE Vector Shape - Group"); pg.property("ADBE Vector Shape").setValue(sh);
    if (!evenOdd) { var mg = v.addProperty("ADBE Vector Filter - Merge"); mg.property("Mode").setValue(3); }
    var f = v.addProperty("ADBE Vector Graphic - Fill"); f.property("Color").setValue(color);
    if (evenOdd) f.property("Fill Rule").setValue(2);
    tr(L, "Position").setValue([cx, cy]);
    return L;
}
function rectLayer(c, name, w, h, color, pos, anchorLeft) {
    var L = c.layers.addShape(); L.name = name;
    var g = L.property("ADBE Root Vectors Group").addProperty("ADBE Vector Group");
    var v = g.property("ADBE Vectors Group");
    var r = v.addProperty("ADBE Vector Shape - Rect"); r.property("Size").setValue([w, h]);
    if (anchorLeft) r.property("Position").setValue([w / 2, 0]);
    var f = v.addProperty("ADBE Vector Graphic - Fill"); f.property("Color").setValue(color);
    tr(L, "Position").setValue(pos);
    return L;
}

// ================= 1. Logo Sting (5 s) =================
var S = comp("Logo Sting", 5);
var R = 230, MX = W / 2, MY = 420;
var sun = sunLayer(S, MX, MY, R, GOLD);
keys(tr(sun, "Scale"), [[0, [0, 0]], [0.5, [112, 112]], [0.8, [100, 100]]], 80);
keys(tr(sun, "Rotation"), [[0, -120], [0.9, 0], [5, 10]], 60);
var bean = beanLayer(S, MX, MY, R, EMBER);
keys(tr(bean, "Scale"), [[0.35, [0, 0]], [0.8, [108, 108]], [1.0, [100, 100]]], 80);
keys(tr(bean, "Rotation"), [[0.35, -35], [1.0, 0]], 75);
var word = text(S, "LUMEN", { size: 150, tracking: 160, bold: true, color: ROAST == null ? CREMA : CREMA, pos: [W / 2, 800], name: "Wordmark" });
trackingAnimator(word, 700, 0, 0.9, 1.9);
fadeInOut(word, 0.9, 0.5, 4.4, 0.6);
var tag = text(S, "COFFEE ROASTERS", { size: 40, tracking: 520, color: GOLD, pos: [W / 2, 880], name: "Tagline" });
keys(tr(tag, "Position"), [[1.5, [W / 2, 905]], [2.1, [W / 2, 880]]], 80);
fadeInOut(tag, 1.5, 0.6, 4.4, 0.6);
fadeInOut(sun, 0, 0.2, 4.4, 0.6);
fadeInOut(bean, 0.35, 0.1, 4.4, 0.6);
var flare = S.layers.addSolid([0, 0, 0], "Flare sweep", W, H, 1); flare.adjustmentLayer = true;
var lf = flare.property("ADBE Effect Parade").addProperty("Lens Flare");
keys(lf.property(1), [[2.0, [MX - 620, MY - 250]], [3.3, [MX + 620, MY - 230]]], 50);
keys(lf.property(2), [[2.0, 0], [2.65, 70], [3.3, 0]], 60);
flare.inPoint = 2.0; flare.outPoint = 3.4;

// ================= 2. Title Card — Ember Ridge (4 s) =================
var T = comp("Title Card Ember Ridge", 4);
var kick = text(T, "NEW SINGLE ORIGIN", { size: 34, tracking: 420, color: EMBER, pos: [W / 2, 380], name: "Kicker" });
keys(tr(kick, "Position"), [[0.2, [W / 2, 400]], [0.8, [W / 2, 380]]], 80);
fadeInOut(kick, 0.2, 0.5, 3.4, 0.5);
var head = text(T, "Ember Ridge", { font: "Georgia", style: "Italic", size: 170, color: CREMA, pos: [W / 2, 560], name: "Headline" });
trackingAnimator(head, 220, 0, 0.45, 1.5);
fadeInOut(head, 0.45, 0.6, 3.4, 0.5);
var rule = rectLayer(T, "Rule", 560, 3, EMBER, [W / 2, 625]);
keys(tr(rule, "Scale"), [[1.0, [0, 100]], [1.6, [100, 100]]], 85);
fadeInOut(rule, 1.0, 0.05, 3.4, 0.5);
var notes = text(T, "Bergamot  ·  Apricot  ·  Cacao nib", { font: "Georgia", size: 46, color: GOLD, pos: [W / 2, 710], name: "Tasting notes" });
fadeInOut(notes, 1.4, 0.6, 3.4, 0.5);
var orig = text(T, "ETHIOPIA  ·  GUJI  ·  WASHED  ·  2,100 M", { size: 26, tracking: 300, color: CLAY, pos: [W / 2, 780], name: "Origin" });
fadeInOut(orig, 1.7, 0.6, 3.4, 0.5);

// ================= 3/4. Lower thirds (6 s, transparent) =================
function lowerThird(name, line1, line2) {
    var C = comp(name, 6, [0, 0, 0]);
    var x0 = 140, y0 = 860;
    var bar = rectLayer(C, "Bar", 820, 150, ROAST, [x0, y0], true);
    tr(bar, "Opacity").setValue(92);
    keys(tr(bar, "Scale"), [[0.2, [0, 100]], [0.75, [100, 100]], [5.2, [100, 100]], [5.7, [0, 100]]], 85);
    var acc = rectLayer(C, "Accent", 12, 150, EMBER, [x0 - 12, y0], true);
    keys(tr(acc, "Scale"), [[0.0, [100, 0]], [0.35, [100, 100]], [5.6, [100, 100]], [5.9, [100, 0]]], 85);
    var a = text(C, line1, { size: 56, bold: true, color: CREMA, left: true, pos: [x0 + 40, y0 - 4], name: "Name" });
    keys(tr(a, "Position"), [[0.55, [x0 + 70, y0 - 4]], [1.05, [x0 + 40, y0 - 4]]], 80);
    fadeInOut(a, 0.55, 0.45, 5.0, 0.4);
    var b = text(C, line2, { font: "Georgia", style: "Italic", size: 36, color: GOLD, left: true, pos: [x0 + 42, y0 + 46], name: "Role" });
    keys(tr(b, "Position"), [[0.75, [x0 + 72, y0 + 46]], [1.25, [x0 + 42, y0 + 46]]], 80);
    fadeInOut(b, 0.75, 0.45, 5.0, 0.4);
    return C;
}
lowerThird("Lower Third Mara", "Mara Okafor", "Head Roaster, Lumen Coffee Roasters");
lowerThird("Lower Third Origin", "Ember Ridge, Lot 07", "Guji zone, Ethiopia · Washed · 2,100 m");

// ================= 5. End Card (4 s) =================
var E = comp("End Card", 4);
var es = sunLayer(E, W / 2, 380, 150, GOLD), eb = beanLayer(E, W / 2, 380, 150, EMBER);
keys(tr(es, "Rotation"), [[0, -20], [4, 0]], 40);
fadeInOut(es, 0, 0.5, null, 0); fadeInOut(eb, 0.1, 0.5, null, 0);
var ew = text(E, "LUMEN", { size: 120, tracking: 160, bold: true, color: CREMA, pos: [W / 2, 660], name: "Wordmark" });
fadeInOut(ew, 0.3, 0.6, null, 0);
var ec = text(E, "AVAILABLE NOW", { size: 30, tracking: 480, color: EMBER, pos: [W / 2, 760], name: "Kicker" });
fadeInOut(ec, 0.8, 0.5, null, 0);
var eu = text(E, "lumen-coffee.example", { size: 44, tracking: 120, color: GOLD, pos: [W / 2, 840], name: "URL" });
fadeInOut(eu, 1.1, 0.5, null, 0);


// ================= 6. Logo Sting Web (Lottie-safe: no text animators, no effects) =================
var LW = comp("Logo Sting Web", 4, [0, 0, 0]);
var wsun = sunLayer(LW, MX, MY, R, GOLD, true);
keys(tr(wsun, "Scale"), [[0, [0, 0]], [0.5, [112, 112]], [0.8, [100, 100]]], 80);
keys(tr(wsun, "Rotation"), [[0, -120], [0.9, 0]], 60);
var wbean = beanLayer(LW, MX, MY, R, EMBER, true);
keys(tr(wbean, "Scale"), [[0.35, [0, 0]], [0.8, [108, 108]], [1.0, [100, 100]]], 80);
keys(tr(wbean, "Rotation"), [[0.35, -35], [1.0, 0]], 75);
var wword = text(LW, "LUMEN", { size: 150, tracking: 160, bold: true, color: CREMA, pos: [W / 2, 800], name: "Wordmark" });
keys(tr(wword, "Position"), [[0.9, [W / 2, 830]], [1.5, [W / 2, 800]]], 80);
fadeInOut(wword, 0.9, 0.5, null, 0);
var wtag = text(LW, "COFFEE ROASTERS", { size: 40, tracking: 520, color: GOLD, pos: [W / 2, 880], name: "Tagline" });
keys(tr(wtag, "Position"), [[1.3, [W / 2, 905]], [1.9, [W / 2, 880]]], 80);
fadeInOut(wtag, 1.3, 0.6, null, 0);

// ================= 7. Music Bed (30 s temp score, synthesised with the Tone audio effect) =================
// Four sustained 5-voice chords, 7.5 s each, cross-faded: Dmaj9 - Bm11 - Gmaj9 - A6/9 (Hz).
var MB = comp("Music Bed 30s", 30, ROAST);
var CHORDS = [[146.83, 220.00, 277.18, 329.63, 369.99], [123.47, 185.00, 220.00, 293.66, 329.63],
              [98.00, 146.83, 220.00, 246.94, 369.99], [110.00, 164.81, 246.94, 277.18, 369.99]];
for (var ci = 0; ci < CHORDS.length; ci++) {
    var sl = MB.layers.addSolid(ROAST, "Chord " + (ci + 1), W, H, 1);
    var tone = sl.property("ADBE Effect Parade").addProperty("Tone");
    tone.property(1).setValue(1);
    for (var fi = 0; fi < 5; fi++) tone.property(2 + fi).setValue(CHORDS[ci][fi]);
    var t0 = ci * 7.5, t1 = t0 + 7.5;
    var lv = [[Math.max(0, t0 - 0.75), 0], [t0 + 0.75, 9], [t1 - 0.75, 9], [Math.min(30, t1 + 0.75), 0]];
    if (ci == 0) lv = [[0, 0], [2.0, 9], [t1 - 0.75, 9], [t1 + 0.75, 0]];
    if (ci == CHORDS.length - 1) lv = [[t0 - 0.75, 0], [t0 + 0.75, 9], [27.0, 9], [30, 0]];
    keys(tone.property(7), lv, 50);
    sl.inPoint = Math.max(0, t0 - 0.75); sl.outPoint = Math.min(30, t1 + 0.75);
}

writeLn("comps: " + app.project.numItems);
