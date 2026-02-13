#!/usr/bin/env bash
set -e

# Check if running inside Docker
if [ ! -f "/.dockerenv" ]; then
  echo "❌ This script must be run inside the Docker container."
  exit 1
fi

echo "==> Setting up Crazyswarm2"

ROS2_WS=${HOME}/ros2_ws

# Import repositories
echo "==> Cloning repo"

mkdir -p ${ROS2_WS}/src

if [ ! -d "${ROS2_WS}/src/crazyswarm2/crazyflie" ]; then
  git -C ${ROS2_WS}/src \
    clone --recursive \
    https://github.com/IMRCLab/crazyswarm2
else
  echo "==> Crazyswarm2 directory already exists, skipping clone"
fi

# Building Crazyswarm2
echo "==> Building Crazyswarm2"
cd ${ROS2_WS}
colcon build \
  --symlink-install \
  --cmake-args -DCMAKE_BUILD_TYPE=Release

source ${ROS2_WS}/install/setup.bash
echo "source ${ROS2_WS}/install/setup.bash" >> ${HOME}/.bashrc 

echo "==> Setup completed successfully ✅"

