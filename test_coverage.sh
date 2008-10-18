#!/bin/sh
nosetests \
    --with-coverage \
    --cover-package=tsp \
    --cover-package=optimise \
    --cover-package=ga \
    --cover-package=sa \
    --cover-package=hillclimb \
    --cover-erase