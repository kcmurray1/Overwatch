#!/bin/bash
# Currently this script must be manually run on the target machine to approve the sudo commands
USER=`whoami`
PROJECT_DIR="/home/$USER/overwatch-agent"
TAILSCALE_ADDR=`tailscale ip -4`
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

# install env + dependencies
sudo apt-get  install -y python3-venv python3-pip
if [ ! -d "env" ]; then
        python3 -m venv env
fi

# install requirements
./env/bin/pip install -r requirements.txt
# setup firewall rules
sudo ufw allow from 100.64.0.0/10 to any port 8001 proto tcp
# Create the service
cat <<EOF | sudo tee /etc/systemd/system/overwatch.service
[Unit]
Description=Overwatch Agent FastAPI Service
After=network.target tailscaled.service

[Service]
User=$USER
Group=$USER
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/env/bin/python -m uvicorn agent:app --host $TAILSCALE_ADDR --port 8001
Restart=always
RestartSec=5
StandardOutput=append:$PROJECT_DIR/agent.log
StandardError=append:$PROJECT_DIR/agent.log

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable overwatch.service
sudo systemctl restart overwatch.service