FROM docker.io/jenkins/jnlp-slave:3.29-1
  ARG JENKINS_UID=1000
  ARG JENKINS_GID=1000
  ARG JENKINS_USR=jenkins
  ARG JENKINS_GRP=jenkins
  ARG JENKINS_HOME=/home/jenkins
  ARG JENKINS_SHELL=/bin/bash
  ENV JENKINS_UID $JENKINS_UID
  ENV JENKINS_GID $JENKINS_GID
  ENV JENKINS_USR $JENKINS_USR
  ENV JENKINS_GRP $JENKINS_GRP
  ENV JENKINS_HOME $JENKINS_HOME
  ENV JENKINS_SHELL $JENKINS_SHELL

  USER root
  RUN mkdir -p /container/init.d
  RUN mkdir -p /usr/share/man/man1/
  RUN apt update && apt install -y\
    bash\
    openssh-client\
    gnupg\
    git\
    tig\
    subversion\
    mercurial\
    curl\
    lsb-release
  RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.14.0/bin/linux/amd64/kubectl &&\
    chmod +x ./kubectl &&\
    mv ./kubectl /usr/local/bin/kubectl
  RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg]\
    http://packages.cloud.google.com/apt cloud-sdk main" |\
    tee -a /etc/apt/sources.list.d/google-cloud-sdk.list &&\
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg |\
    apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - && \
    apt-get update -y &&\
    apt-get install google-cloud-sdk -y

  RUN mkdir -p $JENKINS_HOME
  RUN chown $JENKINS_UID:$JENKINS_GID $JENKINS_HOME

  RUN apt clean -y
  RUN apt autoremove gcc g++ --purge

  # Copy all executables, and explicitely copy the docker-entrypoint
  # since this executable is required to be present.
  COPY bin/ /usr/local/bin/
  COPY bin/docker-entrypoint /usr/local/bin/docker-entrypoint
  COPY container.init.d/ /container/init.d/
  RUN find /usr/local/bin -type f -exec chmod +x {} \;
  RUN find /container/init.d -type f -exec chmod +x {} \;
  RUN chmod +x /usr/local/bin/docker-entrypoint

  USER jenkins
  WORKDIR /home/jenkins

ENTRYPOINT ["/usr/local/bin/docker-entrypoint", "/usr/local/bin/jenkins-slave"]