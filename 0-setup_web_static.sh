#!/usr/bin/env bash
# Preparing my web server

# Install Nginx if not already installed
if ! command -v nginx >/dev/null 2>&1; then
    apt-get update
    apt-get -y install nginx
fi

# Create necessary directories if they don't exist
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create a fake HTML file
echo "Hello, world!" > /data/web_static/releases/test/index.html

# Create or recreate symbolic link
if [ -L /data/web_static/current ]; then
    rm /data/web_static/current
fi
ln -s /data/web_static/releases/test/ /data/web_static/current

# Set ownership of the /data/ folder recursively
chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
config_file="/etc/nginx/sites-available/default"
config_block=$(cat <<EOF
        location /hbnb_static {
            alias /data/web_static/current/;
            index index.html;
        }
EOF
)

# Add or update the location block in the Nginx configuration file
if grep -q "location /hbnb_static" "$config_file"; then
    sed -i '/location \/hbnb_static/,$d' "$config_file"
fi
sed -i "/^}/i $config_block" "$config_file"

# Restart Nginx
service nginx restart
