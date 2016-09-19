import subprocess


def test_docker_install():
    res = subprocess.check_output(["sudo", "docker", "ps"])

    # First line, first word of sudo docker ps output should be "CONTAINER"
    output = res.splitlines()[0].split()[0]
    assert(output == "CONTAINER")
