FROM hashicorp/terraform:0.12.1
  ARG RUNTIME_UID=1000
  ARG RUNTIME_GID=1000
  ARG RUNTIME_USR=terraform
  ARG RUNTIME_GRP=terraform
  ARG RUNTIME_HOME=/home/terraform
  ARG RUNTIME_SHELL=/bin/ash
  ENV RUNTIME_UID $RUNTIME_UID
  ENV RUNTIME_GID $RUNTIME_GID
  ENV RUNTIME_USR $RUNTIME_USR
  ENV RUNTIME_GRP $RUNTIME_GRP
  ENV RUNTIME_HOME $RUNTIME_HOME
  ENV RUNTIME_SHELL $RUNTIME_SHELL
  ENV ANSIBLE_PLAYBOOK main

  USER root
  RUN mkdir -p /container/init.d
  RUN mkdir -p $RUNTIME_HOME
  RUN chown $RUNTIME_UID:$RUNTIME_GID $RUNTIME_HOME
  RUN apk add make

  RUN addgroup -g $RUNTIME_GID -S $RUNTIME_GRP
  RUN adduser -h $RUNTIME_HOME -u $RUNTIME_UID -G $RUNTIME_GRP\
    -H -D -s /bin/ash $RUNTIME_USR
  RUN apk add unzip jq


  # Copy all executables, and explicitely copy the docker-entrypoint
  # since this executable is required to be present.
  COPY bin/ /usr/local/bin/
  COPY bin/docker-entrypoint /usr/local/bin/docker-entrypoint
  COPY container.init.d/ /container/init.d/
  RUN find /usr/local/bin -type f -exec chmod +x {} \;
  RUN find /container/init.d -type f -exec chmod +x {} \;
  RUN chmod +x /usr/local/bin/docker-entrypoint

  USER terraform
  WORKDIR /home/terraform
  ENV SSL_CERT_DIR /usr/local/share/ca-certificates
  COPY Makefile .
  RUN mkdir -p ~/.terraform.d/plugins/linux_amd64
  RUN wget https://github.com/mrparkers/terraform-provider-keycloak/releases/download/1.9.0/terraform-provider-keycloak_v1.9.0_linux_amd64_static.zip
  RUN unzip -: terraform-provider-keycloak*.zip -d ~/.terraform.d/plugins/linux_amd64/
  RUN rm terraform-provider-keycloak*.zip
  COPY main.tf .
  COPY variables.tf .

ENTRYPOINT ["/usr/local/bin/docker-entrypoint"]

CMD ["make", "force-all"]
