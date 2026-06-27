# LawnMower Simulation (ROS2 Jazzy + WSL2)

This repository provides a simple differential drive robot ("lawnmower") for testing in **RViz** and **Gazebo** with teleop keyboard control.

---

## 🖥️ Step 1: Clone Repository
Clone directly into your home directory (`~`):
```bash
cd ~
git clone https://github.com/ros-uthm/lawnmover.git
cd lawnmover
```

⚙️ Step 2: Install ROS 2 Dependencies
-------------------------------------
Make sure ROS 2 (Humble or Jazzy) is installed. Then run:
```bash
sudo apt update
sudo apt install ros-jazzy-rviz2\
                 ros-jazzy-ros-gz-sim\
                 ros-jazzy-ros-gz-bridge\
                 ros-jazzy-teleop-twist-keyboard\
                 ros-jazzy-xacro\
                 ros-jazzy-joint-state-publisher\
                 ros-jazzy-robot-state-publisher

```

> Replace `jazzy` with `humble` if using ROS 2 Humble.

📦 Step 3: Build the Package
----------------------------
```bash
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
source install/setup.bash

```

🚀 Step 4: Launch Options
-------------------------
Choose **one** of the following:
```bash
# RViz display only
ros2 launch lawnmover display.launch.py
```
```bash
# Gazebo simulation (without RViz)
ros2 launch lawnmover gazebo.launch.py rviz:=false
```
```bash
# Gazebo simulation (with RViz)
ros2 launch lawnmover gazebo.launch.py rviz:=true
```

🎮 Step 5: Teleop Keyboard Control
----------------------------------
Open a new terminal, then run:
```bash
source ~/lawnmover/install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p stamped:=true -r /cmd_vel:=/diff_drive_controller/cmd_vel
```
