#!/usr/bin/env bash
#!/usr/bin/env bash

# Install Nginx if it's not already installed
if ! [ -x "$(command -v nginx)" ]; then
  sudo apt-get update
  sudo apt-get install -y nginx
fi

# Create the necessary directories
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create a fake HTML file for testing
echo "<html><head><title>Test Page</title></head><body><p>This is a test page.</p></body></html>" | sudo tee /data/web_static/releases/test/index.html

# Create symbolic link and give ownership
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
sudo sed -i '/^\s*server\s*{/ a \\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default
sudo service nginx restart

exit 0