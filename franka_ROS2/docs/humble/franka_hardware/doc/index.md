> 変換元: `index.rst.txt`

# franka_hardware

> [!IMPORTANT]
> Breaking changes as of 0.1.14 release: `franka_hardware` robot_state and robot_model will be prefixed by the `robot_type`.
>
> - `panda/robot_model  -> ${robot_type}/robot_model`
> - `panda/robot_state  -> ${robot_type}/robot_state`
>
> There is no change with the state and command interfaces naming. They are prefixed with the joint names in the URDF.

## Package Overview

This package contains the `franka_hardware` plugin needed for [ros2_control](https://control.ros.org/jazzy/index.html). The plugin is loaded from the URDF of the robot and passed to the controller manager via the robot description.

## Hardware Interfaces

The hardware plugin provides for each joint:

- a `position state interface` that contains the measured joint position.
- a `velocity state interface` that contains the measured joint velocity.
- an `effort state interface` that contains the measured link-side joint torques.
- an `initial_position state interface` that contains the initial joint position of the robot.
- an `effort command interface` that contains the desired joint torques without gravity.
- a `position command interface` that contains the desired joint position.
- a `velocity command interface` that contains the desired joint velocity.

## Additional State Interfaces

In addition to joint interfaces, the hardware plugin provides:

- a `franka_robot_state` that contains the robot state information, [franka_robot_state](https://github.com/frankarobotics/franka_ros2/blob/jazzy/franka_msgs/msg/FrankaRobotState.msg).
- a `franka_robot_model_interface` that contains the pointer to the model object.
- a `ForceTorqueSensor` (`<arm_prefix><robot_type>_tcp`) that exposes the estimated external wrench in the stiffness frame (`K_F_ext_hat_K` from libfranka) as six state interfaces: `force.x`, `force.y`, `force.z`, `torque.x`, `torque.y`, `torque.z`.

> [!IMPORTANT]
> `franka_robot_state` and `franka_robot_model_interface` state interfaces should not be used directly from hardware state interface. Rather, they should be utilized by the franka_semantic_components interface.
>
> The `ForceTorqueSensor` interfaces follow the standard `ros2_control` sensor convention and can be consumed directly via the `semantic_components::ForceTorqueSensor` component in any controller (e.g. the admittance controller) without requiring a topic bridge. See the gravity compensation example controller for usage.

## ros2_control Macro Library

This package owns the `ros2_control` xacro macro library used to declare hardware interfaces for all Franka robot configurations. The macros live in `franka_hardware/ros2_control/`:

- `franka_ros2_control_macros.xacro` — shared building blocks (`configure_arm_joints`, `configure_finger_joint`, `configure_steering_joint`, `configure_driving_joint`, `configure_mobile_drive_joints`, `configure_passive_mobile_base_joints`, `general_purpose_io`, `cartesian_velocity_io`, `cartesian_pose_loop`, `configure_arm_interfaces`, etc.)
- `franka_arm.ros2_control.xacro` — single-arm configuration
- `tmrv0_2.ros2_control.xacro` — standalone TMR base

These are composed with `franka_description` robot models via thin wrappers in `franka_bringup/urdf/` to produce complete robot descriptions with hardware interfaces.

## Configuration

The IP of the robot is read over a parameter from the URDF.

## Error Recovery

Previously, FCI errors caused the entire launch process to exit. Now, from versions v2.4.0+ and v3.3.0+, the hardware interface remains running and only deactivates itself and its controllers, allowing in-place recovery without restarting.

### Behavior on Error

When a Franka Control Interface (FCI) error occurs (e.g. a reflex triggered by a collision or a violated joint limit), the hardware plugin:

1.  Logs the error.
2.  Stops the active control loop on the robot.
3.  Returns `hardware_interface::return_type::ERROR` to the `controller_manager`.

The `controller_manager` then:

4.  Transitions the hardware component to the **unconfigured** state.

The `ros2_control_node` process **stays alive** — no restart is needed.

> [!WARNING]
> **Humble users:** Due to a limitation in `ros2_control` on Humble ([ros-controls/ros2_control#2318](https://github.com/ros-controls/ros2_control/issues/2318)), controllers are **not** automatically deactivated when the hardware component enters the error state. They remain in the *active* state even though the underlying hardware is no longer functional. **You must manually deactivate your controllers** before you can recover. See the recovery steps below.

### Recovery Steps

After an FCI error the following steps must be performed **in order**:

**Step 0 — (Humble only) Deactivate your controllers**

On Humble, controllers are not automatically deactivated on hardware error. You must stop them manually first:

``` bash
ros2 control switch_controllers --deactivate <controller_name>
```

> [!NOTE]
> On Jazzy this step is not needed — controllers are deactivated automatically.

**Step 1 — Clear the robot error**

Call the error recovery action exposed by the `franka_hardware` action server. This invokes `libfranka`'s `automaticErrorRecovery()` to reset the robot's error state.

``` bash
# Single-arm (no arm prefix):
ros2 action send_goal /action_server/error_recovery franka_msgs/action/ErrorRecovery {}

# Dual-arm (example for left arm with prefix "left_"):
ros2 action send_goal /left/action_server/error_recovery franka_msgs/action/ErrorRecovery {}
```

**Step 2 — Re-activate the hardware component**

Transition the hardware component back to the *active* state so it reconnects the control loop.

``` bash
# Single-arm:
ros2 control set_hardware_component_state FrankaHardwareInterface active

# Dual-arm (left arm):
ros2 control set_hardware_component_state left_FrankaHardwareInterface active
```

> [!TIP]
> You can discover the hardware component name at runtime with:
>
> ``` bash
> ros2 control list_hardware_components
> ```

**Step 3 — Re-activate your controllers**

``` bash
ros2 control switch_controllers --activate <controller_name>
```

> [!WARNING]
> The order matters. On Humble you must first deactivate controllers (Step 0), then clear the robot error (Step 1), re-activate the hardware (Step 2), and finally re-activate controllers (Step 3). On Jazzy, start from Step 1.

### Action Server Topics

The error recovery action topic follows the arm prefix configured in the URDF:

<table style="width:99%;">
<colgroup>
<col style="width: 38%" />
<col style="width: 58%" />
<col style="width: 1%" />
</colgroup>
<thead>
<tr>
<th>Configuration</th>
<th>Action topic</th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td>Single-arm (no prefix)</td>
<td colspan="2"><code>/action_server/error_recovery</code></td>
</tr>
<tr>
<td>Dual-arm, left (<code>left_</code>)</td>
<td colspan="2"><code>/left/action_server/error_recovery</code></td>
</tr>
<tr>
<td>Dual-arm, right (<code>right_</code>)</td>
<td colspan="2"><code>/right/action_server/error_recovery</code></td>
</tr>
</tbody>
</table>

## Usage with Controllers

Controllers can access these interfaces through the standard ros2_control framework. For examples of how to use these interfaces in practice, see the franka_example_controllers package.
