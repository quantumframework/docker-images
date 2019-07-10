FROM docker.io/library/python:3.7-slim-stretch
  ARG RUNTIME_UID=1000
  ARG RUNTIME_GID=1000
  ARG RUNTIME_USR=ansible
  ARG RUNTIME_GRP=ansible
  ARG RUNTIME_HOME=/home/ansible
  ARG RUNTIME_SHELL=/bin/bash
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
  RUN mkdir -p /usr/share/man/man1/
  RUN apt update && apt install -y curl
  RUN pip3 install paramiko==2.4.2
  RUN pip3 install ansible==2.8.1
  RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.14.0/bin/linux/amd64/kubectl &&\
    chmod +x ./kubectl &&\
    mv ./kubectl /usr/local/bin/kubectl
  RUN groupadd -g $RUNTIME_GID $RUNTIME_GRP
  RUN useradd -d "$RUNTIME_HOME" -u $RUNTIME_UID -g $RUNTIME_GID\
    -m -s /bin/bash $RUNTIME_USR
  RUN pip3 install lxml==4.3.4
  RUN pip3 install requests==2.22.0
  RUN pip3 install quantum-queen==1.0.0


  # Copy all executables, and explicitely copy the docker-entrypoint
  # since this executable is required to be present.
  COPY bin/ /usr/local/bin/
  COPY bin/docker-entrypoint /usr/local/bin/docker-entrypoint
  COPY container.init.d/ /container/init.d/
  RUN find /usr/local/bin -type f -exec chmod +x {} \;
  RUN find /container/init.d -type f -exec chmod +x {} \;
  RUN chmod +x /usr/local/bin/docker-entrypoint

  USER ansible
  WORKDIR /home/ansible
  COPY Makefile .
  ENV ANSIBLE_LIBRARY /home/ansible
  COPY main.yml main.yml
  RUN echo "noop ansible_connection=local" > hosts
  RUN mkdir -p vars
  RUN mkdir -p vault
  RUN echo "---\n{}" > vars/main.yml
  RUN echo "---\n{}" > vault/main.yml

  RUN mkdir /home/ansible/etc
  RUN echo '---\n{}' > /home/ansible/etc/organizations.yml
  RUN echo '---\n{}' > /home/ansible/etc/teams.yml
  COPY filter_plugins filter_plugins
  COPY generic.yml generic.yml
  COPY idp.yml idp.yml
  COPY saml.yml saml.yml

  USER root
  RUN apt autoremove -y python3-pip --purge
  RUN apt clean

USER ansible
ENTRYPOINT ["/usr/local/bin/docker-entrypoint"]
CMD ["ansible-playbook", "main.yml", "-i", "hosts", "-e", "@vars/main.yml", "-e", "@vault/main.yml"]
