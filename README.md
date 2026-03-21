# IMC Prosperity 4 Dashboard
Dashboard for IMC Prosperity 4

## Quick Start
Install docker desktop from [here](https://docs.docker.com/desktop/) (or software to manage containers)

From the root of the repository run `docker compose up -d`

This will start to build the images and containers for the application (this may take a while to set up on your computer
for the first time). There may be delays for the data platform to set up as it needs to wait for the spark connect
server and then run pipelines. Therefore, the frontend won't work until this has completed.

User Interface Servers:
- Frontend - http://localhost:8501/
- Unity Catalog UI - http://localhost:3000/
