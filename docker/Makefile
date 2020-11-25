##
# Make animation
#
# @file
# @version 0.1
SHELL := /bin/bash

anim:
	INPUT_PATH=. \
	OUTPUT_PATH=. \
	docker-compose run manim scripts/latex_scenes.py RigorousApproach -l | tee anim.log
	sed  's/\r$$//' anim.log > anim.log2

hq:

	INPUT_PATH=. \
	OUTPUT_PATH=. \
	docker-compose run manim scripts/latex_scenes.py RigorousApproach -qm -c=#1f303e  | tee anim.log
	sed  's/\r$$//' anim.log > anim.log2

play:
	xdg-open $$(grep "File ready at" anim.log2 | cut -d'/' -f4- | sed 's/ *$$//g')


mpv:
	mpv $$(grep "File ready at"  anim.log2 | cut -d'/' -f4- | sed 's/ *$$//g')

# end
