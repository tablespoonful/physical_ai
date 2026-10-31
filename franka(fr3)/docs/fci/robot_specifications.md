> 変換元: `robot_specifications.rst.txt`。CSV 参照の表は省略しました。数値は変換元を確認してください。

# Control Interface Specification and Robot Limits<span id="control_parameters_specifications"></span><span id="control_interface_specifications"></span>

## Overview

Realtime control commands sent to the robot must satisfy a set of *recommended* and *necessary* conditions. Recommended conditions ensure optimal and stable behavior, while necessary conditions are strict safety and feasibility requirements. Violating any necessary condition results in an immediate motion abort.

The executed robot trajectory is based on the user-defined trajectory but adjusted to ensure that recommended conditions are respected. As long as all necessary conditions are satisfied, the robot will follow the commanded trajectory; however, it will only match it exactly if the recommended conditions are also fulfilled.

If a necessary condition is violated, the system raises an error and stops the motion. For example, if the first point of a user-provided joint trajectory differs too much from the robot's actual start configuration ($`q(t=0) \neq q_c(t=0)`$), a `start_pose_invalid` error is triggered.

All constants referenced in the equations below are provided in the [Limits for Franka Emika Robot (FER)](#limits-for-franka-emika-robot-fer) and [Limits for Franka Research 3 (FR3)](#limits-for-franka-research-3-fr3) sections.

## Control Modes

### Joint Space Control Requirements

#### Necessary Conditions

- $`q_{min} < q_c < q_{max}`$
- $`-\dot{q}_{max} < \dot{q}_c < \dot{q}_{max}`$
- $`-\ddot{q}_{max} < \ddot{q}_c < \ddot{q}_{max}`$
- $`-\dddot{q}_{max} < \dddot{q}_c < \dddot{q}_{max}`$

#### Recommended Conditions

- $`-{\tau_j}_{max} < {\tau_j}_d < {\tau_j}_{max}`$
- $`-\dot{\tau_j}_{max} < \dot{\tau_j}_d < \dot{\tau_j}_{max}`$

<div id="joint_space_initial">

Initial trajectory requirements:

</div>

- $`q = q_c`$
- $`\dot{q}_c = 0`$
- $`\ddot{q}_c = 0`$

<div id="joint_space_final">

Final trajectory requirements:

</div>

- $`\dot{q}_c = 0`$
- $`\ddot{q}_c = 0`$

#### Torque Control Requirements

##### Necessary Conditions

- $`-\dot{\tau_j}_{max} < \dot{{\tau_j}_d} < \dot{\tau_j}_{max}`$

##### Recommended Conditions

- $`-{\tau_j}_{max} < {\tau_j}_d < {\tau_j}_{max}`$

<div id="torque_initial">

Initial controller requirements:

</div>

- $`{\tau_j}_d = 0`$

### Cartesian Space Control Requirements

#### Necessary Conditions

- $`T`$ is a proper transformation matrix.
- $`-\dot{p}_{max} < \dot{p}_c < \dot{p}_{max}`$ (Cartesian velocity)
- $`-\ddot{p}_{max} < \ddot{p}_c < \ddot{p}_{max}`$ (Cartesian acceleration)
- $`-\dddot{p}_{max} < \dddot{p}_c < \dddot{p}_{max}`$ (Cartesian jerk)

Conditions derived from inverse kinematics:

- $`q_{min} < q_c < q_{max}`$
- $`-\dot{q}_{max} < \dot{q}_c < \dot{q}_{max}`$
- $`-\ddot{q}_{max} < \ddot{q}_c < \ddot{q}_{max}`$

#### Recommended Conditions

Conditions derived from inverse kinematics:

- $`-{\tau_j}_{max} < {\tau_j}_d < {\tau_j}_{max}`$
- $`-\dot{\tau_j}_{max} < \dot{{\tau_j}_d} < \dot{\tau_j}_{max}`$

<div id="cartesian_space_initial">

Initial trajectory requirements:

</div>

- $`{}^OT_{EE} = {{}^OT_{EE}}_c`$
- $`\dot{p}_c = 0`$
- $`\ddot{p}_c = 0`$

<div id="cartesian_space_final">

Final trajectory requirements:

</div>

- $`\dot{p}_c = 0`$
- $`\ddot{p}_c = 0`$

## System Limits for Supported Robot Models

### Limits for Franka Research 3 (FR3)

<div id="fr3_cartesian_limits">

Cartesian-space limits:

</div>

<table style="width:99%;">
<colgroup>
<col style="width: 14%" />
<col style="width: 28%" />
<col style="width: 28%" />
<col style="width: 26%" />
</colgroup>
<thead>
<tr>
<th><blockquote>
<p>Name</p>
</blockquote></th>
<th><blockquote>
<p>Translation</p>
</blockquote></th>
<th><blockquote>
<p>Rotation</p>
</blockquote></th>
<th><blockquote>
<p>Elbow</p>
</blockquote></th>
</tr>
</thead>
<tbody>
<tr>
<td><span class="math inline"><em>ṗ</em><sub><em>m</em><em>a</em><em>x</em></sub></span></td>
<td>3.0 <span class="math inline">$\frac{\text{m}}{\text{s}}$</span></td>
<td>2.5 <span class="math inline">$\frac{\text{rad}}{\text{s}}$</span></td>
<td>2.620 <span class="math inline">$\frac{rad}{\text{s}}$</span></td>
</tr>
<tr>
<td><span class="math inline">$\ddot{p}_{max}$</span></td>
<td>9.0 <span class="math inline">$\frac{\text{m}}{\text{s}^2}$</span></td>
<td>17.0 <span class="math inline">$\frac{\text{rad}}{\text{s}^2}$</span></td>
<td>10.0 <span class="math inline">$\frac{rad}{\text{s}^2}$</span></td>
</tr>
<tr>
<td><span class="math inline">$\dddot{p}_{max}$</span></td>
<td>4500.0 <span class="math inline">$\frac{\text{m}}{\text{s}^3}$</span></td>
<td>8500.0 <span class="math inline">$\frac{\text{rad}}{\text{s}^3}$</span></td>
<td>5000.0 <span class="math inline">$\frac{rad}{\text{s}^3}$</span></td>
</tr>
</tbody>
</table>

<div id="fr3_joint_limits">

Joint-space limits:

</div>

The arm reaches its maximum extension when joint 4 is at $`q_{elbow-flip} = -0.467002423653011\:rad`$.

#### Position-Based Velocity Limits

> [!IMPORTANT]
> The maximum joint velocity depends on both the joint position and the direction of motion. The position-dependent velocity limits can be queried via:
>
> ``` c++
> Robot::getUpperJointVelocityLimits(
>     const std::array<double, 7UL>& joint_positions
> );
> Robot::getLowerJointVelocityLimits(
>     const std::array<double, 7UL>& joint_positions
> );
> ```
>
> Position-based limits are computed as:
>
> ``` math
> \dot{q_i}(q_i)_{max} =
> \min(
>     \dot{q}_{max,i},
>     \max(
>         0,
>         -\dot{q}_{offset,i} +
>         \sqrt{\max(0, 2 \cdot \ddot{q}_{dec,i} (q_{max,i} - q_i))}
>     )
> )
> ```
>
> ``` math
> \dot{q_i}(q_i)_{min} =
> \max(
>     \dot{q}_{min,i},
>     \min(
>         0,
>         \dot{q}_{offset,i} -
>         \sqrt{\max(0, 2 \cdot \ddot{q}_{dec,i} (-q_{min,i} + q_i))}
>     )
> )
> ```
>
> These limits ensure safety and may be more restrictive than the nominal hardware capabilities.

Users may choose their own joint ranges and velocity limits depending on the requirements of their motion generator.

<figure class="align-center">
<img src="_static/pbv_limits_generic.svg" alt="Position-based velocity limits." />
<figcaption aria-hidden="true">Position-based velocity limits.</figcaption>
</figure>

Suggested rectangular position–velocity limits:

### Limits for Franka Emika Robot (FER)

<div id="fer_cartesian_limits">

Cartesian-space limits:

</div>

<table style="width:99%;">
<colgroup>
<col style="width: 14%" />
<col style="width: 28%" />
<col style="width: 28%" />
<col style="width: 26%" />
</colgroup>
<thead>
<tr>
<th><blockquote>
<p>Name</p>
</blockquote></th>
<th><blockquote>
<p>Translation</p>
</blockquote></th>
<th><blockquote>
<p>Rotation</p>
</blockquote></th>
<th><blockquote>
<p>Elbow</p>
</blockquote></th>
</tr>
</thead>
<tbody>
<tr>
<td><span class="math inline"><em>ṗ</em><sub><em>m</em><em>a</em><em>x</em></sub></span></td>
<td>1.7 <span class="math inline">$\frac{\text{m}}{\text{s}}$</span></td>
<td>2.5 <span class="math inline">$\frac{\text{rad}}{\text{s}}$</span></td>
<td>2.1750 <span class="math inline">$\frac{rad}{\text{s}}$</span></td>
</tr>
<tr>
<td><span class="math inline">$\ddot{p}_{max}$</span></td>
<td>13.0 <span class="math inline">$\frac{\text{m}}{\text{s}^2}$</span></td>
<td>25.0 <span class="math inline">$\frac{\text{rad}}{\text{s}^2}$</span></td>
<td>10.0 <span class="math inline">$\frac{rad}{\text{s}^2}$</span></td>
</tr>
<tr>
<td><span class="math inline">$\dddot{p}_{max}$</span></td>
<td>6500.0 <span class="math inline">$\frac{\text{m}}{\text{s}^3}$</span></td>
<td>12500.0 <span class="math inline">$\frac{\text{rad}}{\text{s}^3}$</span></td>
<td>5000.0 <span class="math inline">$\frac{rad}{\text{s}^3}$</span></td>
</tr>
</tbody>
</table>

<div id="fer_joint_limits">

Joint-space limits:

</div>

The arm reaches its maximum extension when joint 4 is at $`q_{elbow-flip} = -0.467002423653011\:rad`$. This parameter determines the elbow flip direction.

## Kinematic Configuration

### Denavit–Hartenberg Parameters

The Denavit–Hartenberg parameters for the Franka Research 3 kinematic chain (following Craig's convention) are shown below:

<figure class="align-center">
<img src="_static/dh-diagram-frankarobotics.png" alt="Franka Research 3 kinematic chain." />
<figcaption aria-hidden="true">Franka Research 3 kinematic chain.</figcaption>
</figure>

<div id="dh_table">

<table style="width:98%;">
<colgroup>
<col style="width: 11%" />
<col style="width: 18%" />
<col style="width: 18%" />
<col style="width: 24%" />
<col style="width: 24%" />
</colgroup>
<thead>
<tr>
<th><blockquote>
<p>Joint</p>
</blockquote></th>
<th><span class="math inline"><em>a</em> (m)</span></th>
<th><span class="math inline"><em>d</em> (m)</span></th>
<th><span class="math inline"><em>α</em> (rad)</span></th>
<th><span class="math inline"><em>θ</em> (rad)</span></th>
</tr>
</thead>
<tbody>
<tr>
<td>Joint 1</td>
<td>0</td>
<td>0.333</td>
<td>0</td>
<td><span class="math inline"><em>θ</em><sub>1</sub></span></td>
</tr>
<tr>
<td>Joint 2</td>
<td>0</td>
<td>0</td>
<td><span class="math inline">$-\frac{\pi}{2}$</span></td>
<td><span class="math inline"><em>θ</em><sub>2</sub></span></td>
</tr>
<tr>
<td>Joint 3</td>
<td>0</td>
<td>0.316</td>
<td><span class="math inline">$\frac{\pi}{2}$</span></td>
<td><span class="math inline"><em>θ</em><sub>3</sub></span></td>
</tr>
<tr>
<td>Joint 4</td>
<td>0.0825</td>
<td>0</td>
<td><span class="math inline">$\frac{\pi}{2}$</span></td>
<td><span class="math inline"><em>θ</em><sub>4</sub></span></td>
</tr>
<tr>
<td>Joint 5</td>
<td>-0.0825</td>
<td>0.384</td>
<td><span class="math inline">$-\frac{\pi}{2}$</span></td>
<td><span class="math inline"><em>θ</em><sub>5</sub></span></td>
</tr>
<tr>
<td>Joint 6</td>
<td>0</td>
<td>0</td>
<td><span class="math inline">$\frac{\pi}{2}$</span></td>
<td><span class="math inline"><em>θ</em><sub>6</sub></span></td>
</tr>
<tr>
<td>Joint 7</td>
<td>0.088</td>
<td>0</td>
<td><span class="math inline">$\frac{\pi}{2}$</span></td>
<td><span class="math inline"><em>θ</em><sub>7</sub></span></td>
</tr>
<tr>
<td>Flange</td>
<td>0</td>
<td>0.107</td>
<td>0</td>
<td>0</td>
</tr>
</tbody>
</table>

</div>

> [!NOTE]
> $`{}^0T_{1}`$ describes the pose of frame 1 in frame 0.
>
> The full kinematic chain is computed as:
>
> $`{}^0T_{2} = {}^0T_{1} \cdot {}^1T_{2} \cdot {}^2T_{n}`$
