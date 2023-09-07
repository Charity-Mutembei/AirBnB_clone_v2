#!/usr/bin/env bash
#update the system if there is need
apt-get update -y
apt-get upgrade -y
#command to install nginx
apt-get install nginx -y
#creation of the folders data and web_static
mkdir -p /data/web_static
#creation of folder - releases
mkdir -p /data/web_static/releases
#creation of folder- shared
mkdir -p /data/web_static/shared
#creation of the folder- tests
mkdir -p /data/web_static/releases/test
# Create the HTML content and store it in a variable
html_content="<html>
<head>
</head>
<body>
  Holberton School
</body>
</html>"

# Write the HTML content to the index.html file
echo "$html_content" > /data/web_static/releases/test/index.html
#create a symbolic link of the current and tests folders 
ln -fs /data/web_static/releases/test /data/web_static/current
chown -R ubuntu:ubuntu /data
#update the ngix configuration to server the content of the  current folder to hb#nb_static
nginx_config="\
server {
    location /hbnb_static/ {
        alias /data/web_static/current/;
    }
}"
# Use echo to append the new location block to the Nginx default configuration
echo "$nginx_config" > /etc/nginx/sites-available/default
#Restart for the configuration changes
service nginx restart
