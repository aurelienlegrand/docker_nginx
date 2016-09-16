docker_nginx
============

Testing docker and nginx.

## Usage

# Nginx

First build the docker image based on the dockerfile: `docker build -t nginx_img .`

Then launch a new container based on this image: `docker run -d nginx_img`

You can also use this syntax to forward all traffic on port 8080 to your container on port 80: `docker run -d -p 8080:80 nginx_img`

Check that your container is running: `docker ps -a`

Test your webpage: `curl <container_IP>` (use the script docker_get_ip.sh to get the container IP with your container ID)

# Haproxy

Create haproxy container with configuration attached with a volume :
`docker run -d -p 8080:80 -v $PWD/haproxy/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro haproxy`

Reload the haproxy configuration: `docker kill -s HUP <container_d>`

## Done

    * First version of a working nginx instance

## TODO

    * Handle user for nginx (currently using root)
    * Copy static web content to change the landing page
    * Spawn ha-proxy instances and load balance to these nginx instances
    * ha-proxy high availability configuration
    * Auto scale nginx instances creation based on requests seen by ha-proxy
