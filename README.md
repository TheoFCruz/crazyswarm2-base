# crazyswarm2-base

This repository contains the necessary files for building and launching a base docker container for development of [Crazyswarm2](https://github.com/IMRCLab/crazyswarm2) packages using ROS2 Jazzy. It provides the following:
- `Dockerfile` and `docker-compose.yaml` for building the image with it's requirements.
- A `setup.sh` script for cloning crazyswarm's repo and building the workspace.
- An example package with it's own launch and config files, to avoid altering crazyswarm2's folder.
- Installation and setup of the [crazyflie-firmware](https://github.com/bitcraze/crazyflie-firmware) for SITL simulations.

## Requirements

Make sure the following tools are installed:
- Docker
- Docker Compose
- Git

## Setup

First, clone the repository
```
$ git clone https://github.com/TheoFCruz/crazyswarm2-base.git
```

Build the docker image. This step may take some time.
```
$ docker compose build
```

Launch the container.
```
$ docker compose up -d
```

Enter the container and run the `setup.sh` provided script.
```
$ docker exec -it crazyswarm2-base bash
$ bash ./setup.sh
```

## Basic Usage

After configuring crazsywarm through the `crazyswarm_package/config/` files, run the launch command.
```
ros2 launch crazyswarm_package launch.py
```

To change the package name, rename the folder `crazyswarm_package` and modify the following files accordingly:
- `setup.cfg`
- `setup.py`
- `package.xml`


