#!/bin/bash
sudo systemctl daemon-reload
sudo systemctl restart ugc.service
sudo systemctl enable ugc.service
sudo systemctl restart ngrok.service
sudo systemctl enable ngrok.service
curl localhost:8000
curl localhost:4040/api/tunnels