FROM fedora:41

RUN dnf -y install python3-specfile \
                   redhat-rpm-config \
    && dnf clean all
