.RECIPEPREFIX := >
IMAGE ?= {{ foundry.service_name }}:dev

.PHONY: run test docker-build docker-run

run:
> PORT={{ foundry.port }} python3 app/main.py

test:
> python3 -m compileall -q app

docker-build:
> docker build -t $(IMAGE) .

docker-run: docker-build
> docker run --rm -p {{ foundry.port }}:{{ foundry.port }} $(IMAGE)
