#!/usr/bin/env make -f
DOCKER_REGISTRY=docker.io
DOCKER_REPOSITORY=
DOCKER_IMAGE_NAME=slave:k8s
ifneq ($(DOCKER_REPOSITORY),)
DOCKER_QUALNAME=$(DOCKER_REGISTRY)/$(DOCKER_REPOSITORY)/$(DOCKER_IMAGE_NAME)
endif


docker-image:
	@docker build -t $(DOCKER_IMAGE_NAME) .
ifdef DOCKER_QUALNAME
	@docker tag $(DOCKER_IMAGE_NAME) $(DOCKER_QUALNAME)
else
	@echo "Use the DOCKER_REPOSITORY variable to specify a repository."
endif


docker-publish:
	make docker-image DOCKER_REGISTRY=$(DOCKER_REGISTRY)\
		DOCKER_REPOSITORY=$(DOCKER_REPOSITORY)
	docker push $(DOCKER_QUALNAME)
