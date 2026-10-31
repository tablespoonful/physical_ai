> 変換元: `index.rst.txt`

# franka_mobile

## Package Overview

This package contains the controllers needed for franka tmr swerve drive robot, both in simulation and on real hardware.

## Controllers

The package provides:

- `franka_mobile/swerve_drive_controller`: this is the main drive controller for the tmr. Its main features are:  
  - subscribes to <span class="title-ref">geometry_msgs::msg::TwistStamped</span> messages on `~/cmd_vel`
  - publishes to <span class="title-ref">/tf</span> the odometry transformation between <span class="title-ref">world</span> and <span class="title-ref">base_link</span>. Frame names are configurable
  - publishes to <span class="title-ref">~/odom</span> the <span class="title-ref">nav_msgs::msg::Odometry</span> containing the twist coming from the robot's master controller or simulation.
  - writes to a loaned <span class="title-ref">franka_semantic_components::CartesianVelocity</span> command interface to send the desired twist to the robot (either real or simulated).
  - Both state and reference interfaces are configurable with prefixes for chaining purposes.

- `franka_mobile/swerve_ik_controller`: this controller is needed for simulation purposes, e.g. with gazebo. Its main features are:  
  - Reads/writes from/to <span class="title-ref">joint/position</span> and <span class="title-ref">joint/velocity</span> state/command interface exposes by <span class="title-ref">gz_ros2_control</span> plugins.
  - Performs the forward/inverse kinematics computation needed to replicated the master controller's behaviour.
  - Exports a <span class="title-ref">franka_semantic_components::CartesianVelocityInterface</span> as reference interface.
  - Exports a <span class="title-ref">franka_semantic_components::CartesianPoseInterface</span> as state interface.
  - Both state and reference interfaces are configurable with prefixes for chaining purposes.

Both these controllers are derived from `controller_interface::ChainableControllerInterface` and can be composed with other controllers that adhere to the same state/reference interfaces exposed. Please look the the ros2 control documentation for more informations about chaining controllers.

## Configuration

Please look into the <span class="title-ref">config/swerve_drive_controller_parameters.yaml</span> for available overrides in your yaml files.

## Battery service

ROS 2 interface for the Franka TMR Battery REST API (`https://<robot_ip>/battery/api`), using only standard message types.

### Launch

``` bash
ros2 launch franka_mobile battery.launch.py robot_ip:=172.16.0.1
```

### Topic

By default the node publishes `sensor_msgs/BatteryState` on `/franka_battery_node/battery_state` at 1 Hz (parameters `enable_battery_topic` and `publish_rate`).

### Services

Wireless charging control uses `std_srvs/Trigger`:

``` bash
ros2 service call /franka_battery_node/stop_wireless_charging std_srvs/srv/Trigger
ros2 service call /franka_battery_node/try_start_wireless_charging std_srvs/srv/Trigger
```
