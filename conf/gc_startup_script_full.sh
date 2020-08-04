#! /bin/bash
# Install Stackdriver logging agent
curl -sSO https://dl.google.com/cloudagents/install-logging-agent.sh
sudo bash install-logging-agent.sh

# Install or update needed software
apt-get update
apt-get install -yq git supervisor python python-pip
pip install --upgrade pip virtualenv

# Account to own server process
useradd -m -d /home/pythonapp pythonapp

# Fetch source code
export HOME=/root
git clone https://github.com/PsiAmp/GameOverBot.git /opt/gameoverbot
git -C /opt/gameoverbot pull

# Python environment setup
virtualenv -p python3 /opt/gameoverbot/env
source /opt/gameoverbot/env/bin/activate
/opt/gameoverbot/env/bin/pip install -r /opt/gameoverbot/requirements.txt

# Set ownership to newly created account
chown -R pythonapp:pythonapp /opt/gameoverbot

# Put supervisor configuration in proper place
cp /opt/gameoverbot/gameoverbot-app.conf /etc/supervisor/conf.d/gameoverbot-app.conf

# Start service via supervisorctl
supervisorctl reread
supervisorctl update
EOF