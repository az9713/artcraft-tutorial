# Render the 4-frame "shoot" from the photocraft 16-bit master. Needs $photo (projects/env.sh).
m=../photocraft/out/lumen-ember-ridge-hero-master.tif
mkdir -p shoot
"$photo" convert $m shoot/LUM_0001_wide.tif
i=2; for spec in "label-detail 960 450 1080 1440" "beans-right 1880 1400 900 600" "beans-left 190 1400 900 600"; do
  set -- $spec
  "$photo" run $m --cmd image.crop --params "{\"x\":$2,\"y\":$3,\"width\":$4,\"height\":$5}" --out shoot/LUM_000${i}_$1.tif >/dev/null
  i=$((i+1))
done
