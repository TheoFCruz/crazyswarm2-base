#!/usr/bin/env bash
set -e

echo "==> Setting up Crazyswarm2"

ROOT_DIR=/root
ROS2_WS=${ROOT_DIR}/ros2_ws

# Import repositories
echo "==> Cloning repo"

mkdir -p ${ROS2_WS}/src
git -C ${ROS2_WS}/src \
  clone --recursive \
  https://github.com/IMRCLab/crazyswarm2

# Building Crazyswarm2
echo "==> Building Crazyswarm2"
cd ${ROS2_WS}
colcon build \
  --symlink-install \
  --cmake-args -DCMAKE_BUILD_TYPE=Release

echo "==> Setup completed successfully ✅"
