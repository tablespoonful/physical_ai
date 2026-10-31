> 変換元: `installation.rst.txt`

# Build / Installation

> [!NOTE]
> **libfranka** supports Ubuntu 20.04 (focal), 22.04 (jammy), and 24.04 (noble) LTS versions. Pre-built **amd64** Debian packages are available for all supported versions.

## Debian Package

**libfranka** releases are provided as pre-built Debian packages for multiple Ubuntu LTS versions. You can find the packaged artifacts on the [libfranka releases](https://github.com/frankarobotics/libfranka/releases/) page on GitHub.

### Installation Instructions

**Step 1: Check your Ubuntu version**

``` bash
lsb_release -a
```

**Step 2: Download and install the appropriate package**

For the supported ubuntu versions, use the following pattern:

``` bash
# Replace with your desired version and Ubuntu codename
VERSION=0.19.0
CODENAME=focal  # or jammy, noble

wget https://github.com/frankarobotics/libfranka/releases/download/${VERSION}/libfranka_${VERSION}_${CODENAME}_amd64.deb
sudo dpkg -i libfranka_${VERSION}_${CODENAME}_amd64.deb
```

> [!TIP]
> This is the recommended installation method for **libfranka** if you do not need to modify the source code.

### Verify Installation

After installation, verify that libfranka is correctly installed:

``` bash
dpkg -l | grep libfranka
```

## Inside docker container

If you prefer to build **libfranka** inside a Docker container, you can use the provided Docker setup.

## Plain CMake

Before you begin, check the system-requirements.

Afterwards, proceed to building-from-source.

Once the build is complete, you can optionally create and install a Debian package as described in libfranka_installation_debian_package.

## Python Package (pip)

**pylibfranka** is a Python binding for libfranka that enables control of Franka Robotics robots from Python. Pre-built wheels are available on PyPI and include all necessary dependencies.

### Installation

The easiest way to install pylibfranka is via pip:

``` bash
pip install pylibfranka
```

### Platform Compatibility

| Ubuntu Version | Supported Python Versions    |
|----------------|------------------------------|
| 20.04 (Focal)  | Python 3.9 only              |
| 22.04 (Jammy)  | Python 3.9, 3.10, 3.11, 3.12 |
| 24.04 (Noble)  | Python 3.9, 3.10, 3.11, 3.12 |

> [!NOTE]
> Ubuntu 20.04 users must use Python 3.9 due to glibc compatibility requirements.

### Verify Installation

After installation, verify that pylibfranka is correctly installed:

``` python
import pylibfranka
print(f"pylibfranka version: {pylibfranka.__version__}")

# Verify key classes are available
from pylibfranka import Robot, Gripper, Model, RobotState
print("All core classes imported successfully")
```

### Quick Start Example

``` python
import pylibfranka

# Connect to the robot
robot = pylibfranka.Robot("172.16.0.2")
state = robot.read_once()

# Print joint positions
print(f"Joint positions: {state.q}")
```

For more examples, see the [pylibfranka examples](https://github.com/frankarobotics/libfranka/tree/main/pylibfranka/examples) on GitHub.

## Building Python Bindings from Source

If you need to build from source (e.g., for development or unsupported platforms), follow these instructions.

### Prerequisites

- Python 3.9 or newer
- CMake 3.16 or newer
- C++ compiler with C++17 support
- Eigen3 development headers
- Poco development headers

> [!TIP]
> If you are using the provided devcontainer, you can skip the prerequisites installation as they are already included in the container.

### Installing Prerequisites on Ubuntu/Debian

``` bash
sudo apt-get update
sudo apt-get install -y build-essential cmake libeigen3-dev libpoco-dev python3-dev
```

### Build and Install

From the libfranka root folder, install pylibfranka using pip:

``` bash
pip install ./pylibfranka
```

This will build the C++ extension and install pylibfranka in your current Python environment.

For development (editable install):

``` bash
pip install -e ./pylibfranka
```

## Inside a ROS / ROS 2 workspace

If you want to use libfranka in a ROS or ROS 2 workspace, please head over to the franka_ros2_jazzy and franka_ros2_humble chapters for instructions on how to use libfranka in ROS 2, and to the franka_ros chapter for ROS 1 instructions.

## Use this Library in Other Projects

To get started with **libfranka** in your own CMake projects, you need a simple <span class="title-ref">CMakeLists.txt</span> and a corresponding <span class="title-ref">main.cpp</span> file.

At a minimum, your project must:

- Use `find_package(Franka REQUIRED)` to locate the library
- Link against `Franka::Franka` inside your `target_link_libraries(...)` command

Below is an example <span class="title-ref">CMakeLists.txt</span> file:

<div class="literalinclude" language="cmake">

assets/example_cmake_lists.txt

</div>

This example uses `find_package` to detect **libfranka** and sets up an executable target that links to the library.

A matching <span class="title-ref">example_main.cpp</span> file could look like this:

<div class="literalinclude" language="cpp">

assets/example_main.cpp

</div>

To build the project:

``` bash
mkdir build && cd build
cmake ..
cmake --build .
```

Once built, run your example:

``` bash
./example_main
```
