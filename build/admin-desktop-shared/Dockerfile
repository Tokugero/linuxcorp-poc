# https://docs.linuxserver.io/images/docker-rdesktop
ARG LDAP_PASSWORD=""
ARG LDAP_ROOT=""
ARG LDAP_HOST=""

FROM lscr.io/linuxserver/rdesktop:mate-focal

RUN password=$LDAP_PASSWORD && \
    dn=$LDAP_ROOT && \
    ldap_ip=$LDAP_HOST && \
    apt-get update -y && \
    apt-get install -y ldap-auth-config && \
    cat << EOF | sudo debconf-set-selections && \
    ldap-auth-config ldap-auth-config/dbrootlogin boolean false && \
    ldap-auth-config ldap-auth-config/pam_password select md5 && \
    ldap-auth-config ldap-auth-config/move-to-debconf boolean true && \
    ldap-auth-config ldap-auth-config/ldapns/ldap-server string ldap://$ldap_ip && \
    ldap-auth-config ldap-auth-config/ldapns/base-dn string ou=users,$dn && \
    ldap-auth-config ldap-auth-config/override boolean true && \
    ldap-auth-config ldap-auth-config/ldapns/ldap_version select 3 && \
    ldap-auth-config ldap-auth-config/dblogin boolean false && \
    EOF && \
    apt-get install -y libnss-ldap nscd nfs-common && \
    auth-client-config -t nss -p lac_ldap && \
    pam-auth-update && \
    sed -e's,use_authtok,,g' -i /etc/pam.d/common-password