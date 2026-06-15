#!/bin/bash
# Currently this script must be manually run on the target machine to approve the sudo commands
# Prerequsites: Tailscale must be installed and running, Python must be instaleld
# Usage ./setup to setup agent OR ./setup <any value> to perform teardown
#
USER=`whoami`
PROJECT_DIR="/home/$USER/overwatch-agent"
TAILSCALE_ADDR=`tailscale ip -4`

SERVICE_NAME="overwatch"

SERVICE_FILE_LOCATION="/etc/systemd/system/$SERVICE_NAME.service"


if [[ -n "$1" ]]; then
	
	# Teardown: remove service
	if systemctl list-unit-files | grep $SERVICE_NAME; then
		sudo systemctl stop $SERVICE_NAME.service
		sudo systemctl disable $SERVICE_NAME.service
		sudo rm /etc/systemd/system/$SERVICE_NAME.service
		sudo systemctl daemon-reload
	else
		echo "could not find service $SERVICE_NAME skipping step"
	fi

	# NOTE: rperform tailscale logout?

	# delete src code and this script
	if [[ -d $PROJECT_DIR ]]; then
		cd /home/$USER
		sudo rm -r $PROJECT_DIR
	else
		echo "could not find agent files at $PROJECT_DIR"
	fi

	echo "Teardown complete!"
	



else
	# Setup: Create agent folder
	mkdir -p $PROJECT_DIR
	cd $PROJECT_DIR

	# install env + dependencies
	sudo apt-get install -y python3-venv python3-pip
	if [ ! -d "env" ]; then
		python3 -m venv env
	fi

	# install requirements
	./env/bin/pip install -r requirements.txt
	# Create the service(to run even if system restarts)
cat <<EOF | sudo tee $SERVICE_FILE_LOCATION
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
	sudo systemctl enable $SERVICE_NAME.service
	sudo systemctl restart $SERVICE_NAME.service
fi

