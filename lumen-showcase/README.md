# Lumen Coffee Roasters — "Ember Ridge" launch, made with 7 craft apps

A production test: one fictional client, no input files, every artifact made by an open-source Artcraft "craft" app driven by Claude Code. The story of the build — design decisions, failures, fixes and what each craft can do — is in [`DEVELOPMENT-JOURNEY.html`](DEVELOPMENT-JOURNEY.html). The file index with verification notes is [`projects/DELIVERABLES.md`](projects/DELIVERABLES.md).

## Demos — play them

The animations below play right here (silent previews). Click one to play the full video with sound in your browser.

| :30 launch spot (filmcraft) | 9:16 :15 cutdown (filmcraft) |
|---|---|
| [![30-second spot](demo/spot-30s.gif)](https://az9713.github.io/artcraft-tutorial/lumen-showcase/projects/filmcraft/out/lumen-ember-ridge-30_1080p30_h264.mp4) | [![15-second vertical spot](demo/spot-15s-vertical.gif)](https://az9713.github.io/artcraft-tutorial/lumen-showcase/projects/filmcraft/out/lumen-ember-ridge-15_1080x1920_h264.mp4) |

| Logo sting (effectcraft) | Lower third, transparent background (effectcraft) |
|---|---|
| [![Logo sting](demo/logo-sting.gif)](https://az9713.github.io/artcraft-tutorial/lumen-showcase/projects/effectcraft/out/renders/lumen-logo-sting_1080p30.mp4) | [![Lower third](demo/lower-third.gif)](https://az9713.github.io/artcraft-tutorial/lumen-showcase/projects/effectcraft/out/renders/lower-third-mara_prores4444_alpha.mov) |

More to play in the browser:
- **All demos on one page** (spots, web sting, logos, press kit): https://az9713.github.io/artcraft-tutorial/lumen-showcase/projects/_qc/index.html
- **Web logo animation as Lottie** (live vectors, on a transparency checkerboard): https://az9713.github.io/artcraft-tutorial/lumen-showcase/projects/_qc/lottie.html
- **Development journey** (how each craft was used, with pictures): https://az9713.github.io/artcraft-tutorial/lumen-showcase/DEVELOPMENT-JOURNEY.html
- **Music only** (ElevenLabs jingle): https://az9713.github.io/artcraft-tutorial/lumen-showcase/projects/filmcraft/music/lumen-jingle-30s.mp3

The lower third is ProRes 4444 with alpha. Most browsers cannot play ProRes, so that link downloads the file.

## What differs from the local build

- **Not included:** the ProRes 422 HQ master (541 MB) and the ProRes 422 Proxy (158 MB) are over GitHub's 100 MB file limit. The H.264 MP4 shows the same edit. `filmcraft/build_spot.py` rebuilds both.
- **Compressed:** `photocraft/out/lumen-ember-ridge-hero.psd.7z` is the 195 MB layered PSD packed losslessly with 7-Zip (55 MB). The `.pcraft` file is the master.
- **Not included:** build logs, the lightcraft library and shoot folders, preview caches, and the filmcraft QC project (app working data).
- **Paths:** the filmcraft project and interchange files point to media under `C:\work\Downloads\artcraft_jay_E\projects\`. Relink the media when you open them.
- **Music:** `filmcraft/music/` holds an instrumental jingle made with ElevenLabs Music v2.5. It is the only artifact not made by a craft.
- **Rebuild:** `. projects/env.sh` finds the apps in `../apps/` (download the Windows portable builds from github.com/storytold). `pdfcraft/build_presskit.py` needs the environment variable `LUMEN_PDF_OWNER_PW`.

## Artifacts by craft

### vectorcraft (Illustrator equivalent)

Brand identity: logo, palette, bag label with dieline, business cards, PDF/X-4, EPS, SVG/PNG, app icons.

| File | Size |
|---|---|
| [`vectorcraft/build_identity.py`](projects/vectorcraft/build_identity.py) | 14 KB |
| [`vectorcraft/out/lumen-identity-presentation.pdf`](projects/vectorcraft/out/lumen-identity-presentation.pdf) | 356 KB |
| [`vectorcraft/out/lumen-identity.ai`](projects/vectorcraft/out/lumen-identity.ai) | 356 KB |
| [`vectorcraft/out/lumen-identity.vectorcraft`](projects/vectorcraft/out/lumen-identity.vectorcraft) | 2.0 MB |
| [`vectorcraft/out/lumen-print-label-cards-PDFX4.pdf`](projects/vectorcraft/out/lumen-print-label-cards-PDFX4.pdf) | 398 KB |
| [`vectorcraft/out/app-icon/04-App-Icon-1024.png`](projects/vectorcraft/out/app-icon/04-App-Icon-1024.png) | 48 KB |
| [`vectorcraft/out/app-icon/04-App-Icon-16.png`](projects/vectorcraft/out/app-icon/04-App-Icon-16.png) | 1 KB |
| [`vectorcraft/out/app-icon/04-App-Icon-180.png`](projects/vectorcraft/out/app-icon/04-App-Icon-180.png) | 7 KB |
| [`vectorcraft/out/app-icon/04-App-Icon-192.png`](projects/vectorcraft/out/app-icon/04-App-Icon-192.png) | 8 KB |
| [`vectorcraft/out/app-icon/04-App-Icon-32.png`](projects/vectorcraft/out/app-icon/04-App-Icon-32.png) | 1 KB |
| [`vectorcraft/out/app-icon/04-App-Icon-512.png`](projects/vectorcraft/out/app-icon/04-App-Icon-512.png) | 22 KB |
| [`vectorcraft/out/app-icon/04-App-Icon.svg`](projects/vectorcraft/out/app-icon/04-App-Icon.svg) | 118 KB |
| [`vectorcraft/out/eps/lumen-logo_01-Primary-Stacked.eps`](projects/vectorcraft/out/eps/lumen-logo_01-Primary-Stacked.eps) | 359 KB |
| [`vectorcraft/out/eps/lumen-logo_02-Horizontal.eps`](projects/vectorcraft/out/eps/lumen-logo_02-Horizontal.eps) | 328 KB |
| [`vectorcraft/out/eps/lumen-logo_03-Mark.eps`](projects/vectorcraft/out/eps/lumen-logo_03-Mark.eps) | 523 KB |
| [`vectorcraft/out/eps/lumen-logo_05-One-Colour-Black.eps`](projects/vectorcraft/out/eps/lumen-logo_05-One-Colour-Black.eps) | 360 KB |
| [`vectorcraft/out/eps/lumen-logo_06-Reversed.eps`](projects/vectorcraft/out/eps/lumen-logo_06-Reversed.eps) | 1.5 MB |
| [`vectorcraft/out/eps/lumen-logo_12-Reversed-No-Background.eps`](projects/vectorcraft/out/eps/lumen-logo_12-Reversed-No-Background.eps) | 360 KB |
| [`vectorcraft/out/screens/1x/01-Primary-Stacked.png`](projects/vectorcraft/out/screens/1x/01-Primary-Stacked.png) | 27 KB |
| [`vectorcraft/out/screens/1x/02-Horizontal.png`](projects/vectorcraft/out/screens/1x/02-Horizontal.png) | 26 KB |
| [`vectorcraft/out/screens/1x/03-Mark.png`](projects/vectorcraft/out/screens/1x/03-Mark.png) | 26 KB |
| [`vectorcraft/out/screens/1x/05-One-Colour-Black.png`](projects/vectorcraft/out/screens/1x/05-One-Colour-Black.png) | 27 KB |
| [`vectorcraft/out/screens/1x/06-Reversed.png`](projects/vectorcraft/out/screens/1x/06-Reversed.png) | 24 KB |
| [`vectorcraft/out/screens/1x/07-Clear-Space.png`](projects/vectorcraft/out/screens/1x/07-Clear-Space.png) | 51 KB |
| [`vectorcraft/out/screens/1x/08-Bag-Label-100x140mm.png`](projects/vectorcraft/out/screens/1x/08-Bag-Label-100x140mm.png) | 24 KB |
| [`vectorcraft/out/screens/1x/09-Business-Card-Front.png`](projects/vectorcraft/out/screens/1x/09-Business-Card-Front.png) | 4 KB |
| [`vectorcraft/out/screens/1x/10-Business-Card-Back.png`](projects/vectorcraft/out/screens/1x/10-Business-Card-Back.png) | 8 KB |
| [`vectorcraft/out/screens/1x/11-Colour-Palette.png`](projects/vectorcraft/out/screens/1x/11-Colour-Palette.png) | 32 KB |
| [`vectorcraft/out/screens/2x/01-Primary-Stacked@2x.png`](projects/vectorcraft/out/screens/2x/01-Primary-Stacked%402x.png) | 56 KB |
| [`vectorcraft/out/screens/2x/02-Horizontal@2x.png`](projects/vectorcraft/out/screens/2x/02-Horizontal%402x.png) | 54 KB |
| [`vectorcraft/out/screens/2x/03-Mark@2x.png`](projects/vectorcraft/out/screens/2x/03-Mark%402x.png) | 57 KB |
| [`vectorcraft/out/screens/2x/05-One-Colour-Black@2x.png`](projects/vectorcraft/out/screens/2x/05-One-Colour-Black%402x.png) | 58 KB |
| [`vectorcraft/out/screens/2x/06-Reversed@2x.png`](projects/vectorcraft/out/screens/2x/06-Reversed%402x.png) | 50 KB |
| [`vectorcraft/out/screens/2x/07-Clear-Space@2x.png`](projects/vectorcraft/out/screens/2x/07-Clear-Space%402x.png) | 110 KB |
| [`vectorcraft/out/screens/2x/08-Bag-Label-100x140mm@2x.png`](projects/vectorcraft/out/screens/2x/08-Bag-Label-100x140mm%402x.png) | 53 KB |
| [`vectorcraft/out/screens/2x/09-Business-Card-Front@2x.png`](projects/vectorcraft/out/screens/2x/09-Business-Card-Front%402x.png) | 9 KB |
| [`vectorcraft/out/screens/2x/10-Business-Card-Back@2x.png`](projects/vectorcraft/out/screens/2x/10-Business-Card-Back%402x.png) | 19 KB |
| [`vectorcraft/out/screens/2x/11-Colour-Palette@2x.png`](projects/vectorcraft/out/screens/2x/11-Colour-Palette%402x.png) | 77 KB |
| [`vectorcraft/out/screens/SVG/01-Primary-Stacked.svg`](projects/vectorcraft/out/screens/SVG/01-Primary-Stacked.svg) | 114 KB |
| [`vectorcraft/out/screens/SVG/02-Horizontal.svg`](projects/vectorcraft/out/screens/SVG/02-Horizontal.svg) | 115 KB |
| [`vectorcraft/out/screens/SVG/03-Mark.svg`](projects/vectorcraft/out/screens/SVG/03-Mark.svg) | 116 KB |
| [`vectorcraft/out/screens/SVG/05-One-Colour-Black.svg`](projects/vectorcraft/out/screens/SVG/05-One-Colour-Black.svg) | 113 KB |
| [`vectorcraft/out/screens/SVG/06-Reversed.svg`](projects/vectorcraft/out/screens/SVG/06-Reversed.svg) | 113 KB |
| [`vectorcraft/out/screens/SVG/07-Clear-Space.svg`](projects/vectorcraft/out/screens/SVG/07-Clear-Space.svg) | 114 KB |
| [`vectorcraft/out/screens/SVG/08-Bag-Label-100x140mm.svg`](projects/vectorcraft/out/screens/SVG/08-Bag-Label-100x140mm.svg) | 116 KB |
| [`vectorcraft/out/screens/SVG/09-Business-Card-Front.svg`](projects/vectorcraft/out/screens/SVG/09-Business-Card-Front.svg) | 117 KB |
| [`vectorcraft/out/screens/SVG/10-Business-Card-Back.svg`](projects/vectorcraft/out/screens/SVG/10-Business-Card-Back.svg) | 117 KB |
| [`vectorcraft/out/screens/SVG/11-Colour-Palette.svg`](projects/vectorcraft/out/screens/SVG/11-Colour-Palette.svg) | 118 KB |
| [`vectorcraft/proof/label-pdfx4-p1.png`](projects/vectorcraft/proof/label-pdfx4-p1.png) | 76 KB |

### photocraft (Photoshop equivalent)

Layered product hero built from nothing (67 layers, 16-bit), social crops, story post.

| File | Size |
|---|---|
| [`photocraft/build_hero.py`](projects/photocraft/build_hero.py) | 12 KB |
| [`photocraft/make_story_post.sh`](projects/photocraft/make_story_post.sh) | 1 KB |
| [`photocraft/actions/social-portrait.json`](projects/photocraft/actions/social-portrait.json) | 0 KB |
| [`photocraft/actions/social-square.json`](projects/photocraft/actions/social-square.json) | 0 KB |
| [`photocraft/actions/social-story.json`](projects/photocraft/actions/social-story.json) | 0 KB |
| [`photocraft/actions/web-2400.json`](projects/photocraft/actions/web-2400.json) | 0 KB |
| [`photocraft/out/label-1400w.png`](projects/photocraft/out/label-1400w.png) | 142 KB |
| [`photocraft/out/layer-tree.json`](projects/photocraft/out/layer-tree.json) | 37 KB |
| [`photocraft/out/lumen-ember-ridge-hero-master.png`](projects/photocraft/out/lumen-ember-ridge-hero-master.png) | 26.2 MB |
| [`photocraft/out/lumen-ember-ridge-hero-master.tif`](projects/photocraft/out/lumen-ember-ridge-hero-master.tif) | 25.1 MB |
| [`photocraft/out/lumen-ember-ridge-hero.pcraft`](projects/photocraft/out/lumen-ember-ridge-hero.pcraft) | 62.2 MB |
| [`photocraft/out/lumen-ember-ridge-hero.psd.7z`](projects/photocraft/out/lumen-ember-ridge-hero.psd.7z) | 54.6 MB |
| [`photocraft/out/master/ember-ridge-hero.png`](projects/photocraft/out/master/ember-ridge-hero.png) | 26.2 MB |
| [`photocraft/out/social/portrait/ember-ridge-hero.jpg`](projects/photocraft/out/social/portrait/ember-ridge-hero.jpg) | 127 KB |
| [`photocraft/out/social/square/ember-ridge-hero.jpg`](projects/photocraft/out/social/square/ember-ridge-hero.jpg) | 107 KB |
| [`photocraft/out/social/story/ember-ridge-hero.jpg`](projects/photocraft/out/social/story/ember-ridge-hero.jpg) | 177 KB |
| [`photocraft/out/social/story/ember-ridge-story-post.jpg`](projects/photocraft/out/social/story/ember-ridge-story-post.jpg) | 207 KB |
| [`photocraft/out/social/story/ember-ridge-story-post.psd`](projects/photocraft/out/social/story/ember-ridge-story-post.psd) | 4.9 MB |
| [`photocraft/out/web/ember-ridge-hero.jpg`](projects/photocraft/out/web/ember-ridge-hero.jpg) | 219 KB |
| [`photocraft/out/web/ember-ridge-hero.webp`](projects/photocraft/out/web/ember-ridge-hero.webp) | 59 KB |

### lightcraft (Lightroom equivalent)

A 4-frame "shoot" graded with one preset, exported in sRGB, Display P3 and Adobe RGB.

| File | Size |
|---|---|
| [`lightcraft/build_series.py`](projects/lightcraft/build_series.py) | 6 KB |
| [`lightcraft/make_shoot.sh`](projects/lightcraft/make_shoot.sh) | 0 KB |
| [`lightcraft/out/print-adobeRGB-16bit/LUM_0001_wide.tif`](projects/lightcraft/out/print-adobeRGB-16bit/LUM_0001_wide.tif) | 26.9 MB |
| [`lightcraft/out/print-adobeRGB-16bit/LUM_0002_label-detail.tif`](projects/lightcraft/out/print-adobeRGB-16bit/LUM_0002_label-detail.tif) | 6.5 MB |
| [`lightcraft/out/print-adobeRGB-16bit/LUM_0003_beans-right.tif`](projects/lightcraft/out/print-adobeRGB-16bit/LUM_0003_beans-right.tif) | 2.4 MB |
| [`lightcraft/out/print-adobeRGB-16bit/LUM_0004_beans-left.tif`](projects/lightcraft/out/print-adobeRGB-16bit/LUM_0004_beans-left.tif) | 2.4 MB |
| [`lightcraft/out/print-displayP3-16bit/LUM_0001_wide.tif`](projects/lightcraft/out/print-displayP3-16bit/LUM_0001_wide.tif) | 27.0 MB |
| [`lightcraft/out/print-displayP3-16bit/LUM_0002_label-detail.tif`](projects/lightcraft/out/print-displayP3-16bit/LUM_0002_label-detail.tif) | 6.5 MB |
| [`lightcraft/out/print-displayP3-16bit/LUM_0003_beans-right.tif`](projects/lightcraft/out/print-displayP3-16bit/LUM_0003_beans-right.tif) | 2.5 MB |
| [`lightcraft/out/print-displayP3-16bit/LUM_0004_beans-left.tif`](projects/lightcraft/out/print-displayP3-16bit/LUM_0004_beans-left.tif) | 2.4 MB |
| [`lightcraft/out/video-master-srgb-16bit-full/LUM_0001_wide.tif`](projects/lightcraft/out/video-master-srgb-16bit-full/LUM_0001_wide.tif) | 27.0 MB |
| [`lightcraft/out/video-master-srgb-16bit-full/LUM_0002_label-detail.tif`](projects/lightcraft/out/video-master-srgb-16bit-full/LUM_0002_label-detail.tif) | 6.5 MB |
| [`lightcraft/out/video-master-srgb-16bit-full/LUM_0003_beans-right.tif`](projects/lightcraft/out/video-master-srgb-16bit-full/LUM_0003_beans-right.tif) | 2.5 MB |
| [`lightcraft/out/video-master-srgb-16bit-full/LUM_0004_beans-left.tif`](projects/lightcraft/out/video-master-srgb-16bit-full/LUM_0004_beans-left.tif) | 2.4 MB |
| [`lightcraft/out/web-jpeg-srgb-2048/LUM_0001_wide.jpg`](projects/lightcraft/out/web-jpeg-srgb-2048/LUM_0001_wide.jpg) | 241 KB |
| [`lightcraft/out/web-jpeg-srgb-2048/LUM_0002_label-detail.jpg`](projects/lightcraft/out/web-jpeg-srgb-2048/LUM_0002_label-detail.jpg) | 145 KB |
| [`lightcraft/out/web-jpeg-srgb-2048/LUM_0003_beans-right.jpg`](projects/lightcraft/out/web-jpeg-srgb-2048/LUM_0003_beans-right.jpg) | 37 KB |
| [`lightcraft/out/web-jpeg-srgb-2048/LUM_0004_beans-left.jpg`](projects/lightcraft/out/web-jpeg-srgb-2048/LUM_0004_beans-left.jpg) | 34 KB |
| [`lightcraft/out/web-master-srgb-16bit-2048/LUM_0001_wide.tif`](projects/lightcraft/out/web-master-srgb-16bit-2048/LUM_0001_wide.tif) | 12.3 MB |
| [`lightcraft/out/web-master-srgb-16bit-2048/LUM_0002_label-detail.tif`](projects/lightcraft/out/web-master-srgb-16bit-2048/LUM_0002_label-detail.tif) | 6.5 MB |
| [`lightcraft/out/web-master-srgb-16bit-2048/LUM_0003_beans-right.tif`](projects/lightcraft/out/web-master-srgb-16bit-2048/LUM_0003_beans-right.tif) | 2.5 MB |
| [`lightcraft/out/web-master-srgb-16bit-2048/LUM_0004_beans-left.tif`](projects/lightcraft/out/web-master-srgb-16bit-2048/LUM_0004_beans-left.tif) | 2.4 MB |

### effectcraft (After Effects equivalent)

Logo sting, title card, lower thirds with alpha (ProRes 4444), end card, web sting (WebM alpha + Lottie).

| File | Size |
|---|---|
| [`effectcraft/build_motion.jsx`](projects/effectcraft/build_motion.jsx) | 12 KB |
| [`effectcraft/out/lumen-motion.ecproj`](projects/effectcraft/out/lumen-motion.ecproj) | 1.2 MB |
| [`effectcraft/out/renders/end-card_1080p30.mp4`](projects/effectcraft/out/renders/end-card_1080p30.mp4) | 1006 KB |
| [`effectcraft/out/renders/lower-third-mara_prores4444_alpha.mov`](projects/effectcraft/out/renders/lower-third-mara_prores4444_alpha.mov) | 21.4 MB |
| [`effectcraft/out/renders/lower-third-origin_prores4444_alpha.mov`](projects/effectcraft/out/renders/lower-third-origin_prores4444_alpha.mov) | 23.8 MB |
| [`effectcraft/out/renders/lumen-logo-sting-web.lottie.json`](projects/effectcraft/out/renders/lumen-logo-sting-web.lottie.json) | 25 KB |
| [`effectcraft/out/renders/lumen-logo-sting-web_alpha.webm`](projects/effectcraft/out/renders/lumen-logo-sting-web_alpha.webm) | 922 KB |
| [`effectcraft/out/renders/lumen-logo-sting_1080p30.mp4`](projects/effectcraft/out/renders/lumen-logo-sting_1080p30.mp4) | 5.7 MB |
| [`effectcraft/out/renders/lumen-logo-sting_1080p30_prores4444_alpha.mov`](projects/effectcraft/out/renders/lumen-logo-sting_1080p30_prores4444_alpha.mov) | 94.4 MB |
| [`effectcraft/out/renders/lumen-temp-score-30s.wav`](projects/effectcraft/out/renders/lumen-temp-score-30s.wav) | 5.5 MB |
| [`effectcraft/out/renders/title-card-ember-ridge_1080p30.mp4`](projects/effectcraft/out/renders/title-card-ember-ridge_1080p30.mp4) | 654 KB |
| [`effectcraft/out/review/End_Card_2.5.png`](projects/effectcraft/out/review/End_Card_2.5.png) | 32 KB |
| [`effectcraft/out/review/Logo_Sting_0.5.png`](projects/effectcraft/out/review/Logo_Sting_0.5.png) | 42 KB |
| [`effectcraft/out/review/Logo_Sting_1.3.png`](projects/effectcraft/out/review/Logo_Sting_1.3.png) | 44 KB |
| [`effectcraft/out/review/Logo_Sting_2.6.png`](projects/effectcraft/out/review/Logo_Sting_2.6.png) | 209 KB |
| [`effectcraft/out/review/Logo_Sting_3.8.png`](projects/effectcraft/out/review/Logo_Sting_3.8.png) | 49 KB |
| [`effectcraft/out/review/Logo_Sting_4.0.png`](projects/effectcraft/out/review/Logo_Sting_4.0.png) | 35 KB |
| [`effectcraft/out/review/Lower_Third_Mara_2.0.png`](projects/effectcraft/out/review/Lower_Third_Mara_2.0.png) | 22 KB |
| [`effectcraft/out/review/Title_Card_Ember_Ridge_2.2.png`](projects/effectcraft/out/review/Title_Card_Ember_Ridge_2.2.png) | 52 KB |

### filmcraft (Premiere Pro equivalent)

:30 spot and 9:16 :15, captions, EDL / FCP7 XML / FCPXML / OTIO, project file, music.

| File | Size |
|---|---|
| [`filmcraft/build_spot.py`](projects/filmcraft/build_spot.py) | 9 KB |
| [`filmcraft/temp-score-explained.html`](projects/filmcraft/temp-score-explained.html) | 10 KB |
| [`filmcraft/music/lumen-jingle-30s.mp3`](projects/filmcraft/music/lumen-jingle-30s.mp3) | 721 KB |
| [`filmcraft/music/takes/take-a.mp3`](projects/filmcraft/music/takes/take-a.mp3) | 721 KB |
| [`filmcraft/music/takes/take-b.mp3`](projects/filmcraft/music/takes/take-b.mp3) | 721 KB |
| [`filmcraft/music/takes/take-c.mp3`](projects/filmcraft/music/takes/take-c.mp3) | 721 KB |
| [`filmcraft/out/lumen-ember-ridge-15_1080x1920_h264.mp4`](projects/filmcraft/out/lumen-ember-ridge-15_1080x1920_h264.mp4) | 10.3 MB |
| [`filmcraft/out/lumen-ember-ridge-30.en.srt`](projects/filmcraft/out/lumen-ember-ridge-30.en.srt) | 0 KB |
| [`filmcraft/out/lumen-ember-ridge-30_1080p30_h264.mp4`](projects/filmcraft/out/lumen-ember-ridge-30_1080p30_h264.mp4) | 38.7 MB |
| [`filmcraft/out/lumen-ember-ridge-30_1080p30_h264.srt`](projects/filmcraft/out/lumen-ember-ridge-30_1080p30_h264.srt) | 0 KB |
| [`filmcraft/out/lumen-ember-ridge.fcproj`](projects/filmcraft/out/lumen-ember-ridge.fcproj) | 29 KB |
| [`filmcraft/out/project-tree.json`](projects/filmcraft/out/project-tree.json) | 2 KB |
| [`filmcraft/out/interchange/lumen-ember-ridge-30.edl`](projects/filmcraft/out/interchange/lumen-ember-ridge-30.edl) | 3 KB |
| [`filmcraft/out/interchange/lumen-ember-ridge-30.fcpxml`](projects/filmcraft/out/interchange/lumen-ember-ridge-30.fcpxml) | 6 KB |
| [`filmcraft/out/interchange/lumen-ember-ridge-30.otio`](projects/filmcraft/out/interchange/lumen-ember-ridge-30.otio) | 68 KB |
| [`filmcraft/out/interchange/lumen-ember-ridge-30.xml`](projects/filmcraft/out/interchange/lumen-ember-ridge-30.xml) | 37 KB |

### designcraft (InDesign equivalent)

12-page brand guidelines: tagged PDF, PDF/X-4, IDML, native file, page PNGs.

| File | Size |
|---|---|
| [`designcraft/build_guidelines.py`](projects/designcraft/build_guidelines.py) | 14 KB |
| [`designcraft/out/lumen-brand-guidelines-v1.0.idml`](projects/designcraft/out/lumen-brand-guidelines-v1.0.idml) | 58.4 MB |
| [`designcraft/out/lumen-brand-guidelines-v1.0.pdf`](projects/designcraft/out/lumen-brand-guidelines-v1.0.pdf) | 33.5 MB |
| [`designcraft/out/lumen-brand-guidelines-v1.0_print-x4.pdf`](projects/designcraft/out/lumen-brand-guidelines-v1.0_print-x4.pdf) | 33.7 MB |
| [`designcraft/out/lumen-brand-guidelines.designcraft`](projects/designcraft/out/lumen-brand-guidelines.designcraft) | 57.2 MB |
| [`designcraft/out/pages/page-01.png`](projects/designcraft/out/pages/page-01.png) | 108 KB |
| [`designcraft/out/pages/page-02.png`](projects/designcraft/out/pages/page-02.png) | 148 KB |
| [`designcraft/out/pages/page-03.png`](projects/designcraft/out/pages/page-03.png) | 826 KB |
| [`designcraft/out/pages/page-04.png`](projects/designcraft/out/pages/page-04.png) | 157 KB |
| [`designcraft/out/pages/page-05.png`](projects/designcraft/out/pages/page-05.png) | 156 KB |
| [`designcraft/out/pages/page-06.png`](projects/designcraft/out/pages/page-06.png) | 200 KB |
| [`designcraft/out/pages/page-07.png`](projects/designcraft/out/pages/page-07.png) | 161 KB |
| [`designcraft/out/pages/page-08.png`](projects/designcraft/out/pages/page-08.png) | 183 KB |
| [`designcraft/out/pages/page-09.png`](projects/designcraft/out/pages/page-09.png) | 1.1 MB |
| [`designcraft/out/pages/page-10.png`](projects/designcraft/out/pages/page-10.png) | 762 KB |
| [`designcraft/out/pages/page-11.png`](projects/designcraft/out/pages/page-11.png) | 284 KB |
| [`designcraft/out/pages/page-12.png`](projects/designcraft/out/pages/page-12.png) | 74 KB |

### pdfcraft (Acrobat equivalent)

19-page press kit with bookmarks and page labels, protected distribution copy, product sheet, sections.

| File | Size |
|---|---|
| [`pdfcraft/build_presskit.py`](projects/pdfcraft/build_presskit.py) | 8 KB |
| [`pdfcraft/out/ember-ridge-product-sheet.pdf`](projects/pdfcraft/out/ember-ridge-product-sheet.pdf) | 32.8 MB |
| [`pdfcraft/out/lumen-press-kit-2026-10.pdf`](projects/pdfcraft/out/lumen-press-kit-2026-10.pdf) | 33.9 MB |
| [`pdfcraft/out/lumen-press-kit-2026-10_distribution.pdf`](projects/pdfcraft/out/lumen-press-kit-2026-10_distribution.pdf) | 34.0 MB |
| [`pdfcraft/out/sections/lumen-press-kit-2026-10-Brand guidelines v1.0.pdf`](projects/pdfcraft/out/sections/lumen-press-kit-2026-10-Brand%20guidelines%20v1.0.pdf) | 33.5 MB |
| [`pdfcraft/out/sections/lumen-press-kit-2026-10-Logo artwork (vector, from the identity master).pdf`](projects/pdfcraft/out/sections/lumen-press-kit-2026-10-Logo%20artwork%20%28vector%2C%20from%20the%20identity%20master%29.pdf) | 25 KB |
| [`pdfcraft/out/sections/lumen-press-kit-2026-10-Press release_ Ember Ridge.pdf`](projects/pdfcraft/out/sections/lumen-press-kit-2026-10-Press%20release_%20Ember%20Ridge.pdf) | 374 KB |
| [`pdfcraft/proof/kit-p1.png`](projects/pdfcraft/proof/kit-p1.png) | 126 KB |
| [`pdfcraft/proof/kit-p15.png`](projects/pdfcraft/proof/kit-p15.png) | 22 KB |
