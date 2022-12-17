import ruamel.yaml as yaml
from diagrams import Diagram, Cluster, Edge  # Types
from diagrams.onprem import client, compute, container, database, monitoring, network  # Pictures
from diagrams.generic import database as generic_database
from diagrams.aws import storage

import os


def parseFiles():
    with open("../docker-compose.yml", "r") as f:
        compose_data = yaml.safe_load(f)

    proxyConfs = "../data/swag-proxy/config/nginx/proxy-confs"
    for file in os.listdir(proxyConfs):
        if file.endswith(".conf"):
            with open(proxyConfs+"/" + file, "r") as f:
                if "deny all" in f.read():
                    compose_data["services"][file.split(
                        ".")[0]+"-ui"]["private"] = True

    return compose_data


def generateDiagram(compose_data):
    diagram = Diagram("LinuxCorp", show=False)

    # Sorted List Buckets
    privateServices = [
        service for service in compose_data["services"] if "private" in compose_data["services"][service]]
    edgeServices = ["swag-proxy", "wireguard", "authelia-sso"]
    dbs = [service for service in compose_data["services"] if "db" in service]
    nonPrivServices = [
        service for service in compose_data["services"] if service not in privateServices and service not in edgeServices and service not in dbs]
    desktops = [service for service in compose_data["services"]
                if "desktop" in service]

    # Holding Buckets
    volumes = {}
    nodes = {}

    # Diagram generation
    with diagram:
        for service in edgeServices:
            nodes[service] = determineNode(compose_data, service)

        adminCluster = Cluster("Admin")
        with adminCluster:
            for service in privateServices:
                nodes[service] = determineNode(compose_data, service, True)
            for service in dbs:
                nodes[service] = determineNode(compose_data, service, True)
            for volume in compose_data["volumes"]:
                volumes[volume] = determineVolume(compose_data, volume)

        corpCluster = Cluster("Corp")
        with corpCluster:
            for service in nonPrivServices:
                nodes[service] = determineNode(compose_data, service)

        cloud = Cluster("Cloud")
        with cloud:
            nodes["duplicati-ui"]["node"] >> storage.SimpleStorageServiceS3Bucket(
                "Backups")

        for node in nodes.keys():
            if "-ui" in node:
                if "private" in nodes[node]["data"]:
                    nodes["swag-proxy"]["node"] >> Edge(
                        color="red", label="Only Admins") >> nodes[node]["node"]
                else:
                    nodes["swag-proxy"]["node"] >> nodes[node]["node"]
            if "depends_on" in nodes[node]["data"]:
                for dependency in nodes[node]["data"]["depends_on"]:
                    nodes[dependency]["node"] << nodes[node]["node"]
            if "volumes" in nodes[node]["data"]:
                for volume in nodes[node]["data"]["volumes"]:
                    volume = volume.split(":")[0]
                    if volume in volumes:
                        nodes[node]["node"] << volumes[volume]["volume"]

        for desktop in desktops:
            if "links" in nodes[desktop]["data"]:
                nodes[desktop]["node"] << Edge(
                    color="red", label="Only Admins") << nodes["guacd"]["node"]
            else:
                nodes[desktop]["node"] << nodes["guacd"]["node"]

        # Edge cases
        user = client.User("User")
        admin = client.User("Admin")

        user >> nodes["swag-proxy"]["node"]
        admin >> nodes["wireguard"]["node"] >> Edge(
            color="red", label="Only Admins") >> nodes["admin-desktop-shared"]["node"] >> Edge(
            color="red", label="Only Admins") >> nodes["swag-proxy"]["node"]

        dockerEngine = container.Docker("DockerEngine")

        dockerEngine << nodes["yacht-ui"]["node"]


def determineNode(compose_data, service, private=False):
    if "grafana" in service:
        nodeType = monitoring.Grafana
    elif "prometheus" in service:
        nodeType = monitoring.Prometheus
    elif "swag" in service:
        nodeType = network.Nginx
    elif "mariadb" in compose_data["services"][service]["container_name"]:
        nodeType = database.MariaDB
    elif "desktop" in service:
        nodeType = container.Docker
    else:  # Default
        nodeType = compute.Server

    node = {"data": compose_data["services"][service],
            "node": nodeType(service),
            "private": private}

    return node


def determineVolume(compose_data, volume):
    volume = {"data": compose_data["volumes"][volume],
              "volume": storage.ElasticBlockStoreEBSVolume(volume)}
    return volume


def main():
    generateDiagram(parseFiles())


if __name__ == "__main__":
    main()
