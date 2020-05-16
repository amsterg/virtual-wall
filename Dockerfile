# This is an auto generated Dockerfile for ros:perception
# generated from docker_images/create_ros_image.Dockerfile.em
FROM ros:kinetic-ros-base-xenial

# install ros packages
RUN apt-get update && apt-get install -y \
    ros-kinetic-perception=1.3.2-0* \
    && rm -rf /var/lib/apt/lists/*
    



CMD cd home/ && git clone https://github.com/slightech/MYNT-EYE-S-SDK.git \
    && cd MYNT-EYE-S-SDK && git checkout c79808e7d8b4e2c593df3de347de30e7fccfedfd \
    && sed -i "/disparity_computing_method: 1/c\disparity_computing_method: 0" wrappers/ros/src/mynt_eye_ros_wrapper/config/process/process_config.yaml \
    && make ros \
    && cd wrappers/ros && ls && . devel/setup.sh \
    && export ROS_IP=`hostname -I` \
    # && python src/mynt_eye_ros_wrapper/scripts/*.py \
    && roslaunch src/mynt_eye_ros_wrapper/launch/mynteye.launch \
