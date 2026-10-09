# 9:16 story post: typography over the photocraft story crop. Needs $photo (see projects/env.sh).
"$photo" run out/social/story/ember-ridge-hero.jpg \
 --cmd type.create --params '{"x":540,"y":140,"text":"NEW SINGLE ORIGIN","align":"center","font":"Bahnschrift","fontStyle":"SemiBold","size":30,"color":"#1d1410","tracking":420,"name":"Kicker"}' \
 --cmd type.create --params '{"x":540,"y":250,"text":"Ember Ridge","align":"center","font":"Georgia","fontStyle":"Italic","italic":true,"size":96,"color":"#1d1410","name":"Headline"}' \
 --cmd type.create --params '{"x":540,"y":312,"text":"Bergamot · Apricot · Cacao nib","align":"center","font":"Georgia","fontStyle":"Regular","size":30,"color":"#6b3f24","name":"Tasting notes"}' \
 --cmd type.create --params '{"x":540,"y":1702,"text":"LUMEN-COFFEE.EXAMPLE","align":"center","font":"Bahnschrift","fontStyle":"SemiBold","size":24,"color":"#f9bb2b","tracking":300,"name":"URL"}' \
 --out out/social/story/ember-ridge-story-post.psd
"$photo" convert out/social/story/ember-ridge-story-post.psd out/social/story/ember-ridge-story-post.jpg --quality 90
