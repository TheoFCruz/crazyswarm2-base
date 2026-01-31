# ROS2 desktop full base image with additional linux utils
FROM osrf/ros:jazzy-desktop-full AS ros2-base
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt-get install -y \
    git \
    x11vnc \
    wget \
    unzip \
    xvfb \
    icewm \
    tree \
    dos2unix \
    vim \
    net-tools \
    iputils-ping \
    iproute2 \
    iptables \
    tcpdump \
    nano \
    tmux

# Crazyswarm2 ros2 image for development
FROM ros2-base AS crazyswarm-tests
RUN apt-get update && apt-get install -y \
    libboost-program-options-dev \
    swig \
    libusb-1.0-0-dev
RUN apt-get install -y \
    ros-${ROS_DISTRO}-tf-transformations \
    ros-${ROS_DISTRO}-motion-capture-tracking \
    python3-pip \
    python3-venv

WORKDIR /root
SHELL ["/bin/bash", "-c"]

# setup pythonvenv and install dependencies
RUN python3 -m venv /root/.ros_venv && \
   .ros_venv/bin/pip3 install \
   rowan \
   nicegui==1.4.2 \
   cflib \
   transforms3d \
   'empy<4' \
   catkin_pkg \
   lark-parser

# add source to bashrc
RUN echo "source /opt/ros/jazzy/setup.bash" >> /root/.bashrc && \
    echo "source /root/.ros_venv/bin/activate" >> /root/.bashrc

# build firmware python bindings
RUN git clone \
    --branch 2025.02 --single-branch --recursive \
    https://github.com/bitcraze/crazyflie-firmware.git 
RUN make -C /root/crazyflie-firmware cf2_defconfig && \
    make -C /root/crazyflie-firmware bindings_python && \
    /root/.ros_venv/bin/pip3 install -e /root/crazyflie-firmware/build

# copy setup script
COPY ./setup.sh /root

# colored prompt
RUN sed -i 's/#force_color_prompt=yes/force_color_prompt=yes/' /root/.bashrc

CMD tail -f /dev/null

