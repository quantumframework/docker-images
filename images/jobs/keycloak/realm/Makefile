#!/usr/bin/env make -f
DOCKER_REGISTRY=docker.io
DOCKER_REPOSITORY=
DOCKER_IMAGE_NAME=keycloak:realm
ifneq ($(DOCKER_REPOSITORY),)
DOCKER_QUALNAME=$(DOCKER_REGISTRY)/$(DOCKER_REPOSITORY)/$(DOCKER_IMAGE_NAME)
endif
TF_VARS_FILE := variables/main.json
export TF_VARS_FILE



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


init: .terraform terraform.tfstate

all: .terraform terraform.tfstate apply

force-all: .terraform terraform.tfstate force-apply

plan: terraform.plan


apply:
	@terraform apply --var-file $(TF_VARS_FILE)


force-apply:
	@terraform apply --var-file $(TF_VARS_FILE) -auto-approve


terraform.plan:
	@terraform plan --var-file $(TF_VARS_FILE)\
		-out terraform.plan


terraform.tfstate:
ifneq ("$(wildcard ./sbin/terraform-import)","")
	@sh ./sbin/terraform-import
endif


.terraform:
	@terraform init


clean:
	@rm -rf .terraform
	@rm -rf terraform.tfstate
	@rm -rf terraform.plan


destroy:
	@terraform destroy --var-file $(TF_VARS_FILE)
