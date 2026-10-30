# ros2_kdl_package

## About

Tutorial code for ROS 2 C++ nodes using the Kinematics and Dynamics Library
(KDL). This package is intended to run together with
[ros2_iiwa](https://github.com/RoboticsLab2026/ros2_iiwa).

The combined launch file starts `iiwa_bringup/iiwa.launch.py` and
`ros2_kdl_package/ros2_kdl_node` with a matching command interface.
`ros2_iiwa` is the repository containing the `iiwa_bringup` package.

## Build

Place this package and the `ros2_iiwa` repository in the `src/` directory of your ROS 2 workspace. Run the following commands from the workspace root:

```bash
colcon build --packages-select ros2_kdl_package --symlink-install
source install/setup.bash
```

Source the workspace in each new terminal before running the commands below.

## Basic kinematics example

Run the original example node to calculate basic kinematic quantities:

```bash
ros2 run ros2_kdl_package ros2_kdl_node_example
```

## Launch the robot and KDL node together

### Position control

```bash
ros2 launch ros2_kdl_package iiwa_kdl.launch.py
```

Position control is the default. It can also be selected explicitly:

```bash
ros2 launch ros2_kdl_package iiwa_kdl.launch.py cmd_interface:=position
```

### Velocity control

```bash
ros2 launch ros2_kdl_package iiwa_kdl.launch.py cmd_interface:=velocity
```

### Effort control

```bash
ros2 launch ros2_kdl_package iiwa_kdl.launch.py cmd_interface:=effort
```

### Trajectory options

| Launch argument | Accepted values | Default in this launch file |
| --- | --- | --- |
| `cmd_interface` | `position`, `velocity`, `effort` | `position` |
| `traj_type` | `linear`, `circular` | `linear` |
| `s_type` | `trapezoidal`, `cubic` | `trapezoidal` |

The launch file explicitly passes all three parameters to the KDL node. These launch defaults do not depend on the defaults in the C++ source.

For example, run a circular trajectory with cubic polynomial time scaling in velocity mode:

```bash
ros2 launch ros2_kdl_package iiwa_kdl.launch.py \
  cmd_interface:=velocity traj_type:=circular s_type:=cubic
```

Inspect the available arguments with:

```bash
ros2 launch ros2_kdl_package iiwa_kdl.launch.py --show-args
```

The selected mode determines the arguments passed to iiwa bringup:

| `cmd_interface` | iiwa `command_interface` | iiwa `robot_controller` |
| --- | --- | --- |
| `position` | Uses the bringup default | Uses the bringup default |
| `velocity` | `velocity` | `velocity_controller` |
| `effort` | `effort` | `effort_controller` |

Position mode uses the unmodified bringup defaults, matching
`ros2 launch iiwa_bringup iiwa.launch.py`.

The combined launch starts both components in one session; it does not wait for controller readiness before starting the KDL node. If the KDL node requires an active controller at startup, use the separate-terminal workflow below and start the node after the controller is ready. Press `Ctrl+C` to stop the combined launch session.

## Run components separately

Use two terminals with the workspace sourced: run robot bringup in the first,
then start the KDL node in the second after bringup is ready.

### Position control

Terminal 1:

```bash
ros2 launch iiwa_bringup iiwa.launch.py
```

Terminal 2:

```bash
ros2 run ros2_kdl_package ros2_kdl_node
```

### Velocity control

Terminal 1:

```bash
ros2 launch iiwa_bringup iiwa.launch.py \
  command_interface:=velocity robot_controller:=velocity_controller
```

Terminal 2:

```bash
ros2 run ros2_kdl_package ros2_kdl_node --ros-args -p cmd_interface:=velocity
```

### Effort control

Terminal 1:

```bash
ros2 launch iiwa_bringup iiwa.launch.py \
  command_interface:=effort robot_controller:=effort_controller
```

Terminal 2:

```bash
ros2 run ros2_kdl_package ros2_kdl_node --ros-args -p cmd_interface:=effort
```

To select the trajectory directly when running the node:

```bash
ros2 run ros2_kdl_package ros2_kdl_node --ros-args \
  -p cmd_interface:=velocity -p traj_type:=circular -p s_type:=cubic
```

Use `argument:=value` with `ros2 launch`. Use `--ros-args -p parameter:=value`
with `ros2 run`.