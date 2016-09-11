############################################################
# Dockerfile to build Nginx Installed Containers
# Based on Ubuntu
############################################################

# Set the base image to Ubuntu
FROM ubuntu

# File Author / Maintainer
MAINTAINER Aurelien Legrand 

# Update the repository
RUN apt-get update

# Download and Install Nginx
RUN apt-get install -y nginx  

# Copy nginx configuration
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/default.conf /etc/nginx/conf.d/default.conf


# Expose ports
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
