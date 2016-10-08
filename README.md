docker_nginx
============

Testing docker and nginx.

# Usage

## Setup
Use the scripts in the setup folder to setup your environment (tested on Ubuntu 16.04LTS).

Use pip install -r requirements.txt to install python libraries.

## Nginx

First build the docker image based on the dockerfile: `docker build -t nginx_img .`

Then launch a new container based on this image: `docker run -d nginx_img`

You can also use this syntax to forward all traffic on port 8080 to your container on port 80: `docker run -d -p 8080:80 nginx_img`

Check that your container is running: `docker ps -a`

Test your webpage: `curl <container_IP>` (use the script docker_get_ip.sh to get the container IP with your container ID)

## Haproxy

Create haproxy container with configuration attached with a volume :
`docker run -d -p 8080:80 -v $PWD/haproxy/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro haproxy`

Reload the haproxy configuration: `docker kill -s HUP <container_d>`

## Docker remote API

Use the setup/setup_docker.sh script to set up your environment and the Docker Remote API.

After setup, use `docker -H tcp://127.0.0.1:2375 ps` or ` curl -X GET http://127.0.0.1:2375/images/json` to test the API. 

## Python API

The goal of the Python API is to help you provision easily webservers containers. Launch the api with `python api.py`

Documentation is still work in progress but accessible at `localhost:5000/api/spec.json` when the API is running.

## Tests

Install python, pip and the python requirements if you have not already done it.
Run `pytest tests/test.py`


# Done

    * First version of a working nginx instance
    * First version of a working haproxy instance
    * Simple Docker Remote API configuration (not secure)
    * First version of an API that communicate with Docker Remote API

# TODO

    * Handle user for nginx (currently using root)
    * Copy static web content to change the landing page
    * Spawn ha-proxy instances and load balance to these nginx instances
    * Secure Docker Remote API configuration with TLS
    * ha-proxy high availability configuration
    * Auto scale nginx instances creation based on requests seen by ha-proxy
