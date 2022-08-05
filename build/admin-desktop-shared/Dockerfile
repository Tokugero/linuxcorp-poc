# https://docs.linuxserver.io/images/docker-rdesktop
ARG LDAP_PASSWORD=""
ARG LDAP_ROOT=""
ARG LDAP_HOST=""

FROM lscr.io/linuxserver/rdesktop:mate-focal

RUN password=$LDAP_PASSWORD && \
    dn=$LDAP_ROOT && \
    ldap_ip=$LDAP_HOST && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y libnss-ldap nscd nfs-common 

COPY ldap.conf /etc/ldap.conf
COPY access.conf /etc/security/access.conf
COPY common-auth /etc/pam.d/common-auth