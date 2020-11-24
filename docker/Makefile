##
# Make animation
#
# @file
# @version 0.1
SHELL := /bin/bash

anim:
	INPUT_PATH=. \
	OUTPUT_PATH=. \
	docker-compose run manim scripts/example.py SquareToCircle -l | tee anim.log

play:
	xdg-open videos/example_scene/480p15/SquareToCircle.mp4

# end
