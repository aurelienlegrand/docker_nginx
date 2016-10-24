#!/usr/bin/env python3
import subprocess
import json
import requests

def test_docker_install():
    """Test if docker is installed and running"""
    res = subprocess.check_output(["sudo", "docker", "ps"])

    assert("CONTAINER" in res.decode("utf-8"))


def test_docker_api():
    """Test if docker api is running and can be requested"""
    # Creates a new container using the docker remote API

    docker_host = "127.0.0.1"
    payload = { 'Image' : 'nginx' }
    r_create = requests.post('http://' + docker_host + ':2375/containers/create', json=payload)

    data = json.loads(r_create.content.decode("utf-8"))
    assert("Id" in data)

    node_id = data["Id"][:12]

    # Tries to get info about the container we just created
    r_get = requests.get('http://' + docker_host + ':2375/containers/' + node_id + "/json")

    data = json.loads(r_get.content.decode("utf-8"))
    assert("State" in data)
    assert(data["State"]["Status"] == "created")

    # Deletes the container
    r_delete = requests.delete("http://" + docker_host + ":2375/containers/" + node_id)
    data = r_delete.content.decode("utf-8")
    assert(r_delete.status_code == 204)
