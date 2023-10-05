#!/usr/bin/env bash
# sets up your web servers for the deployment of web_static

sudo apt-get -y upgrade
sudo apt-get -y install nginx
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
echo "Hello Yassine!" > /data/web_static/releases/test/index.html

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -Rh ubuntu:ubuntu /data/

sudo sed -i "47i\\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\\n" /etc/nginx/sites-available/default
sudo ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default
sudo service nginx restart
