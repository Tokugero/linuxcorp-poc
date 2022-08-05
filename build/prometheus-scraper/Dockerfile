# https://github.com/prometheus/snmp_exporter
# https://github.com/Tokugero/device-collector-poc/blob/main/prom-snmp-stack/snmp/Dockerfile
FROM debian

RUN cat /etc/apt/sources.list | grep -v \# | sed "s/main$/main contrib non-free/g" | xargs -I {} echo {} >> /etc/apt/sources.list.d/nonfree.list && \
    apt-get update && \
    apt-get install -y \
        snmp \
        snmpd \
        snmp-mibs-downloader && \
    download-mibs && \
    rm -rf /var/lib/apt/lists/*

CMD ["/usr/sbin/snmpd", "-f"]