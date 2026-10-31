> **[PDF を開く](<Quick Guide for Installation Franka GELLO DUO_0.5_R62040_1.2_EN.pdf>)**
>
> PDF から自動変換した本文です。図は含まず、表は崩れている場合があります。安全や仕様の確認には PDF を使ってください。



Quick Guide for Installation 

FRANKA GELLO DUO 

© Copyright 2026 Franka Robotics GmbH Koppstraße 12 81379 Munich Germany 

Document name:              Quick Guide for Installation Franka GELLO DUO Document number:          R62040 Version:                             Franka GELLO Duo 0.5 Document version Change Log: 

|**Content Iteration**|**Release Date**|**Release notes / Changes**|
|---|---|---|
|1.0|24.11.2025|Initial Release of installation guide for Franka GELLO DUO|
|1.1|18.12.2025|Updated information in Chapter 5 “Assembly instructions” and fixed errors|
|1.2|14.04.2026|Updated document number, and fixed errors|



Product Reference: 

|**Franka article number**|**Revision**|**Model number**|**Description**|
|---|---|---|---|
|313686|00-05|10074107|Franka GELLO Duo|
|313684|00-05|10074108|Franka GELLO Arm<br>(part of Franka GELLO Duo)|





Get your manual and additional supporting material in English and other languages at <u>www.franka.de/documents</u> 

Copyright © Franka Robotics 

**TABLE** OF CONTENTS 

# **TABLE OF CONTENTS** 

|TAB|LE OF CONTENTS ........................................................................................................................... 3|
|---|---|
|1|PURPOSE AND SCOPE ................................................................................................................. 4|
|2|LEGAL DISCLAIMER ..................................................................................................................... 4|
|3|ABOUT FRANKA GELLO DUO ....................................................................................................... 5|
|4|SCOPE OF DELIVERY / INCLUDED IN THE BOX .............................................................................. 6|
|5|ASSEMBLY INSTRUCTIONS........................................................................................................... 8|
|6|SOFTWARE ................................................................................................................................11|



Copyright © Franka Robotics 

**PURPOSE** AND SCOPE 

# **1 PURPOSE AND SCOPE** 

The quick guide for installation provides step-by-step instructions for assembling and connecting Franka GELLO Duo system. It is intended to help users quickly set up the hardware and prepare it for initial operation with Franka Research 3 Duo (FR3 Duo robot). 

The guide covers: 

- Components included in the package 

- Correct assembly procedures 

- Reference to further resources for teleoperation and programming 

### **Intended Audience** 

This guide is designed for: 

- **Researchers** working with robotic systems 

- **Technicians** responsible for hardware setup 

- **Developers** integrating Franka GELLO Duo into custom applications 

Basic familiarity with robotic hardware and safe handling of electronic components is recommended. 

# **2 LEGAL DISCLAIMER** 

Franka GELLO-Arms are experimental development tools that are provided solely for testing and evaluation purposes. They are not part of the certified product portfolio of Franka Robotics GmbH and are supplied 'as-is' without any express or implied warranties, including but not limited to warranties of merchantability, fitness for a particular purpose, or conformity. The Supplier does not provide any support, maintenance, or updates for these tools. Any liability for material or legal defects is excluded, except in cases of willful misconduct or gross negligence. This clause shall not affect mandatory liability under applicable product liability laws or for injury to life, body, or health. 

Copyright © Franka Robotics 

**ABOUT** FRANKA GELLO DUO 

# **3 ABOUT FRANKA GELLO DUO** 

Franka GELLO Duo is a teleoperation device for the Franka FR3 Duo robot. It is kinematically equivalent to the FR3 Duo robot system, but scaled down in dimensions, allowing users to control the FR3 Duo directly at joint level. The hardware is an upgraded version of the hardware used in the original GELLO paper by Philipp Wu et al.<sup>1</sup> 

It is especially useful for researchers who want to explore: 

- Intuitive joint-level teleoperation 

- Large-scale data recording for imitation Learning, e.g., training of Vision-Language-Action models 

Comparing GELLO with VR controllers and 3D SpaceMouses for teleoperation tasks, the authors of the paper have found that _“utilizing GELLO results in consistently faster completion times. This not only signifies that GELLO is easier to use with a higher success rate but also indicates its efficiency; faster completion times would enable users to achieve more successful operations in each time frame”._ 



_Figure 1: Franka GELLO Duo_ 

The hardware and software of Franka GELLO Duo are open source, so anyone in the community can access and use them freely. Franka Robotics has contributed a ROS 2 implementation of the GELLO software and 3D-printable parts compatible with the Franka FR3 Duo to the original author’s repositories: 

- <u>https://github.com/wuphilipp/gello_sofwaret</u> 

- <u>https://github.com/wuphilipp/gello_mechanical</u> 

## **_NOTICE_** 

Franka GELLO Duo is designed to match the kinematics of Franka FR3 Robot Arm v2.0 and later versions. Previous robot versions slightly differ. 

Copyright © Franka Robotics 

**SCOPE** OF DELIVERY / INCLUDED IN THE BOX 

# **4 SCOPE OF DELIVERY / INCLUDED IN THE BOX** 

|**Item No.**|**Components**|**Quantity**|
|---|---|---|
|1|Franka GELLO Arm|2 pcs.|
|2|Table Base Mount Duo|1 pc.|
|3|Screws M4x12|6 pcs.|
|4|OpenRB-150 Controller|2 pcs.|
|5|Screws C2x8 black|8 pcs.|
|6|Cable USB-A to USB-C 2m|2 pcs.|
|7|Reference to Assembly Guide|1 document|





<mark>See Figure 2 below for a visual reference</mark> 

Copyright © Franka Robotics 

**SCOPE** OF DELIVERY / INCLUDED IN THE BOX 



_Figure 2: Visualization of included items_ 

Copyright © Franka Robotics 

**ASSEMBLY** INSTRUCTIONS 

# **5 ASSEMBLY INSTRUCTIONS** 

**Step 1 – Install the Controllers** 

1. Position one **OpenRB-150 Controller** (4) on each side of the base (top corners). 

2. Check that the USB-C port faces outward for easy access. 

3. Fix each controller using **four screws C2×8 black** (5). 

**Step 2 – Mount Franka GELLO Arms** 

1. Place the **Table Base Mount Duo** (2) on a stable surface. 

2. Attach each **Franka GELLO Arm** (1) to either side bracket of the base. 

3. Use **three M4×12 screws** (3) per Arm to secure them firmly. 

4. Make sure both Arms are symmetrically aligned and stable. 

### **Step 3 – Connect the System** 

1. Plug **Franka GELLO Arm** (1) cable connector into any of the four white connectors on the controller (4). 

2. Repeat the same for the other **Franka GELLO Arm** (1). 

3. Ensure all connections are secure before continuing. 

4. Connect each **OpenRB-150 controller** (4) to your **PC** using the **USB-A to USB-C cable** (6). 



<mark>See Figure 3 below for a visual reference</mark> 

Copyright © Franka Robotics 

**ASSEMBLY** INSTRUCTIONS 



_Figure 3: Assembly_ 

Copyright © Franka Robotics 

**ASSEMBLY** INSTRUCTIONS 



_Figure 4: Installed Franka GELLO Duo_ 



_Figure 5: Resting pose_ 

Copyright © Franka Robotics 

**SOFTWARE** 

# **6 SOFTWARE** 

<mark>The ROS 2 integraton to control a Franka FR3 robot system using the Franka GELLO is available in the “ros2”</mark> i subfolder of the “gello_software” repository: <u>https://github.com/wuphilipp/gello_sofware/tree/main/ros2t .</u> 

**_Refer to the README of the “ros2” folder for instructions on launching ROS 2 nodes._** 

## **_NOTICE_** 

The ROS 2 package “franka_gello_state_publisher” requires a configuration file for each individual GELLO system which defines its hardware properties and settings. 

For Franka GELLO a suitable configuration file is provided: 

**_<mark>ros2/src/franka_gello_state_publisher/confg/franka_gello_duo.yaml</mark> i_** 

To use it: 

- Update the **com_port** entries so they match the ID of your controller. 

- Refer to the **README** for detailed instructions on how to identify this ID. 

Copyright © Franka Robotics 

**SOFTWARE** 

Franka Robotics GmbH Koppstraße 12 81379 Munich Germany Copyright © Franka Robotics 



