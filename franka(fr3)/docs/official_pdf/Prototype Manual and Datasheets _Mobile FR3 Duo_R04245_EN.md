> **[PDF を開く](<Prototype Manual and Datasheets _Mobile FR3 Duo_R04245_EN.pdf>)**
>
> PDF から自動変換した本文です。図は含まず、表は崩れている場合があります。安全や仕様の確認には PDF を使ってください。



Prototype Manual & Datasheets 

MOBILE FR3 DUO 



© Copyright 2026 Franka Robotics GmbH Koppstraße 12 81379 Munich Germany 

#### Document name:              Prototype Manual and Datasheets Document number:          R04245 Change log: 

|**Content**<br>**Iteration**|**Release Date**|**Release notes / Changes**|
|---|---|---|
|1.0|03.09.2026|Prototype manual and datasheets first draft release|
|1.1|01.04.2026|Added document number and change log.<br>Added and/or updated the following new Chapters:|
|||•<br>Chapter 4.2 Dual Arm Workspace: Reach and Manipulation<br>•<br>Chapter 5.3 Physical User Interfaces|
|||•<br>Chapter 5.4 Turning on the TMR|
|||•<br>Chapter 5.5 Shutting Down the TMR|
|||•<br>Chapter 7.3 Nominal Charging Sequence|
|||•<br>Chapter 7.4 Rescue Charging Sequence|
|||•<br>Chapter 8.2.1 Spine Back and Top Plate Mounting Holes<br>•<br>Chapter 12 FAQ|



Copyright © Franka Robotics GmbH 

2 



## TABLE OF CONTENTS 

|1<br>Intri|oduction ................................................................................................................................................................................5|
|---|---|
|1.1|Prototype Disclaimer .......................................................................................................................................................5|
|1.2|Document Purpose ...........................................................................................................................................................5|
|1.3|Document scope ...............................................................................................................................................................5|
|1.4|Product Prototypes ..........................................................................................................................................................5|
|1.5|Accessory Prototypes ......................................................................................................................................................5|
|2<br>Saf|ety Guidelines.......................................................................................................................................................................6|
|2.1|Electrical Safety .................................................................................................................................................................6|
|2.2|Operational Guidelines ....................................................................................................................................................6|
|3<br>Typ|e labels on the equipment ................................................................................................................................................7|
|3.1|Tactile Mobile Robot ........................................................................................................................................................7|
|3.2|Franka Spine ......................................................................................................................................................................7|
|3.3|TMR Charging Station ......................................................................................................................................................7|
|4<br>Mo|bile FR3 Duo ........................................................................................................................................................................8|
|4.1|Datasheet ...........................................................................................................................................................................8|
|4.2|Dual Arm Workspace: Reach and Manipulation.........................................................................................................8|
|4.3|Scope of Delivery ........................................................................................................................................................... 10|
|4.4|Other User Devices ....................................................................................................................................................... 11|
|4.5|Limitations, Constraints and Misuse .......................................................................................................................... 11|
|5<br>Taci|tile Mobile Robot ............................................................................................................................................................. 12|
|5.1|Datasheet ........................................................................................................................................................................ 12|
|5.2|Scope of Delivery ........................................................................................................................................................... 13|
|5.3|Physical User Interfaces ............................................................................................................................................... 13|
|5.3|.1<br>Power Switch and Rescue Charging Port ...................................................................................................... 13|
|5.3|.2<br>Emergency Stops ................................................................................................................................................ 13|
|5.3|.3<br>Configuration and pairing of the FORT wireless E-Stop ............................................................................ 14|
|5.3|.4<br>UI-Panel and Related Connections ................................................................................................................. 15|
|5.3|.5<br>Battery SoC Monitor on the UI Panel ............................................................................................................. 15|
|5.3|.6<br>Spine Connection Bays ...................................................................................................................................... 15|
|5.3|.7<br>Router WAN Port ............................................................................................................................................... 16|
|5.3|.8<br>TMR Top Plate Mounting Holes ...................................................................................................................... 16|
|5.3|.9<br>TMR Type Label .................................................................................................................................................. 19|
|5.4|Turning on the TMR ...................................................................................................................................................... 19|
|5.5|Shutting Down the TMR............................................................................................................................................... 19|
|5.6|Sensors ............................................................................................................................................................................. 19|
|5.6|.1<br>LIDARs .................................................................................................................................................................. 19|
|5.6|.2<br>IMU ........................................................................................................................................................................ 19|
|5.6|.3<br>Cameras ................................................................................................................................................................ 20|
|5.6|.4<br>Sensor Testing ..................................................................................................................................................... 20|
|5.7|Software UI TMR v0.2 .................................................................................................................................................. 20|



Copyright © Franka Robotics GmbH 

3 



|5.8|Software Integration Interfaces TMR v0.2 ............................................................................................................... 21|
|---|---|
|5.9|Internal network setup ................................................................................................................................................. 21|
|5.9|.1<br>IP Address Allocation ......................................................................................................................................... 21|
|5.9|.2<br>Wireless Configuration ...................................................................................................................................... 22|
|5.9|.3<br>Internet Access for internal components for Software Updates. ............................................................. 22|
|5.10|Working with User PC of TMR v0.2 ..................................................................................................................... 22|
|5.1|0.1<br>System specifications ......................................................................................................................................... 22|
|5.1|0.2<br>Access methods .................................................................................................................................................. 23|
|5.1|0.3<br>ROS 2 workspace setup .................................................................................................................................... 23|
|5.1|0.4<br>Available Demos ................................................................................................................................................. 23|
|5.1|0.5<br>Repositories ......................................................................................................................................................... 23|
|5.1|0.6<br>Gamepad Demo .................................................................................................................................................. 23|
|5.1|0.7<br>Steps ...................................................................................................................................................................... 23|
|5.1|0.8<br>Controls ................................................................................................................................................................ 23|
|5.1|0.9<br>ROS 2 Sensors Demo ......................................................................................................................................... 24|
|6<br>FR|3 Duo ................................................................................................................................................................................... 25|
|6.1|Datasheet ........................................................................................................................................................................ 25|
|6.2|Scope of Delivery ........................................................................................................................................................... 25|
|7<br>TM  i|R Charging Station ........................................................................................................................................................... 27|
|7.1|Datasheet ........................................................................................................................................................................ 27|
|7.2|Scope of Delivery ........................................................................................................................................................... 27|
|7.3|Nominal Charging Sequence ....................................................................................................................................... 27|
|7.4|Rescue charging sequence. .......................................................................................................................................... 28|
|7.5|Software-Interfaces ....................................................................................................................................................... 29|
|8<br>Fra|nka Spine ............................................................................................................................................................................ 30|
|8.1|Datasheet ........................................................................................................................................................................ 30|
|8.2|Physical User Interfaces ............................................................................................................................................... 31|
|8.2|.1<br>Spine Back and Top Plate Mounting Holes ................................................................................................... 31|
|8.3|Software Interfaces ....................................................................................................................................................... 31|
|9<br>FR  i|3 Duo Mounting Kit v0.3 ................................................................................................................................................. 32|
|9.1|Datasheet ........................................................................................................................................................................ 32|
|10|Franka Head Bracket v0.2 ............................................................................................................................................ 33|
|10.1|Datasheet ................................................................................................................................................................... 33|
|11|Handling, Transport & Maintenance .......................................................................................................................... 34|
|11.1|Areas for Manual Handling without Special Equipment .................................................................................. 35|
|11.2|Areas for Handling with Special Equipment ....................................................................................................... 35|
|12|FAQ................................................................................................................................................................................... 36|
|12.1|Desk Shows 500 Internal Server Error ................................................................................................................ 36|
|13|Table of figures ............................................................................................................................................................... 37|



Copyright © Franka Robotics GmbH 

4 



# **1 INTRODUCTION** 

### **1.1 Prototype Disclaimer** 

This document is for the internal use of Franka Robotics GmbH only. Specifications and features described herein are preliminary and may change without prior notice. Not for commercial distribution. 

###### **NOTICE** 

This manual applies to prototype hardware and is not certified according to IEC 60204 or other safety standards. Use only in controlled environments by qualified personnel. 

### **1.2 Document Purpose** 

This manual provides technical specifications, operational guidelines, and accessory details for the Mobile FR3 Duo prototype. It is intended for internal use during prototype evaluation and testing. 

### **1.3 Document scope** 

This document covers: 

- Safety guidelines 

- Operational guidelines 

- Datasheets 

### **1.4 Product Prototypes** 

- Mobile FR3 Duo – v0.2 

- Tactile Mobile Robot (TMR) – v0.2 

### **1.5 Accessory Prototypes** 

- Franka Spine – v0.1 

- Franka Head Bracket – v0.2 

- FR3 Duo Mounting Kit – v0.3 

- Charging Station – v0.1 

Copyright © Franka Robotics GmbH 

5 



# **2 SAFETY GUIDELINES** 

The following guidelines are essential for safe operation and handling of prototype hardware. These instructions apply to the Mobile FR3 Duo, Tactile Mobile Robot (TMR), and all associated accessories. 

The following notices are used throughout this manual to indicate the level of risk and importance of information: 

###### **DANGER** 

Indicates a hazardous situation that, if not avoided, will result in death or serious injury. 

###### **WARNING** 

Indicates a hazardous situation that, if not avoided, could result in death or serious injury. 

###### **CAUTION** 

Indicates a hazardous situation that, if not avoided, could result in minor or moderate injury. 

###### **NOTICE** 

Indicates important information not related to personal safety, but essential for proper operation. 

###### **SAFTEY-INSTRUCTIONS** 

Indicates processes or steps that must be strictly observed to ensure safe operation. 

### **2.1 Electrical Safety** 

###### **WARNING** 

- All E-stops are designed with redundancy. Still, the current design does not claim compliance with IEC 60204-1 or ISO 13849-1. Additionally, no diagnostic functionality is currently implemented. 

- The operator should perform a daily test to ensure E-Stops are operational. 

### **2.2 Operational Guidelines** 

- **Qualified Personnel Only:** Operate and maintain prototypes only by trained individuals familiar with robotic systems. 

- **Controlled Environment:** Use prototypes exclusively in supervised, indoor environments with stable surfaces. 

- **Personal Protective Equipment (PPE):** Wear safety gloves and protective eyewear during assembly, adjustment, or maintenance. 

- **Keep Clear of Moving Parts:** Never place hands or objects near active joints, drives, or robotic arms during operation. 

- **Disconnect Power Before Maintenance:** Always power down and unplug the system before performing any adjustments or repairs. 

- **Wireless E-Stop:** Always use the wireless E-Stop during operation of the prototype. 

Copyright © Franka Robotics GmbH 

6 



# **3 TYPE LABELS ON THE EQUIPMENT** 

### **3.1 Tactile Mobile Robot** 



_Figure 1: TMR Type Label_ 

### **3.2 Franka Spine** 



_Figure 2: Franka Spine Type Label_ 

- **3.3 TMR Charging Station** 



_Figure 3: TMR Charging Station_ 

Copyright © Franka Robotics GmbH 

7 



# **4 MOBILE FR3 DUO** 

###### _(Type: Product Prototype)_ 

The Mobile FR3 Duo is a prototype mobile manipulator optimized for research in the areas of teleoperation, mobile manipulation, and embodied AI. This system is intended to be used exclusively for use in research and development within industrial laboratory environments and/or for training and educational purposes related to industrial applications. It is not designed or approved for production use, or safety-critical applications. 



_Figure 4: Mobile FR3 Duo_ 

### **4.1 Datasheet** 

||**Mobile FR3**|**Duo**||
|---|---|---|---|
||**Platform**|**Onb**|**oard devices**|
|**Drive System**|Holonomic / Omnidirectional|**Mobile Platform**|Tactile Mobile Robot|
|**Degrees of freedom**|18|**Vertical Lift**|Franka Spine|
|**Dimensions**|800 x 583 x 1461 mm|**Robot Arms**|Franka Research 3|
|**Max. payload**|TMR: 125 kg<br>Franka Spine: 50 kg<br>FR3: 3 kg|||
|**Weight**|225 kg|||
|**Max. speed**|1.5 m/s|||



### **4.2 Dual Arm Workspace: Reach and Manipulation** 

From investigations of the workspace of a single FR3 arm, there is a region right in front of the robot with good manipulability. This knowledge is used to define the so-called ISO-cube for performance experiments. 

**_<mark>See Datasheet Franka Research 3 (Document Number: R02212)</mark>_** 

Copyright © Franka Robotics GmbH 

8 





_Figure 5: Side and top views of the robot workspace, showing maximum reach and operating envelope dimensions._ 

In the case of FR3 Duo, overlapping the centers of the two ISO-cubes of the two FR3 arms ensures good manipulability for both the robots. 



_Figure 6: ISO cube for FR3 Duo_ 

The current positioning of the two FR3 arms with the shoulders (J2) further away from each other and the bases (J1) close to each other ensures a large workspace, reduces the likelihood of collisions, and ensures a small overall footprint. 

For visualizing the workspace, a simplified sphere with a 0.855m radius about the shoulder joint represents the reach, whereas a sphere with 0.7m radius about the shoulder joint represents manipulability. A voxelated Monte Carlo representation of reachability and a heatmap considering ideal the Yoshikawa’s Manipulability Index have not been provided in this manual. 

Copyright © Franka Robotics GmbH 

9 





_Figure 7: Dual arm workspace._ 

|**Dimension**||**Position of Spine**|
|---|---|---|
||**Lowest**|**Nominal**<br>**Highest**|
|A|- 142|451<br>609|
|B|13|606<br>764|
|C|713|1306<br>1464|
|D|1413|2006<br>2164|
|E|1568|2161<br>2319|



_Note: All dimensions in mm_ 

_Figure_ 8 _: Workspace relative to Franka Spine Position_ 

The only constraints for using the full extent of the workspace are joint limits and collisions. Self-collision checks with ROS2 is planned to be released soon. 

### **4.3 Scope of Delivery** 

The following items are included in the delivery of the Mobile FR3 Duo system. Optional accessories are listed separately. 

###### **System Components** 

- Tactile Mobile Robot – TMR (Mobile Platform) 

- FR3 Duo (dual-arm system) 

   - FR3 Duo Mounting Kit v0.3 

   - Franka Research 3 

###### **Optional Accessories** 

- Franka Spine (vertical lift) 

- TMR Charging Station (wireless and rescue charger) 

- FR3 Duo Vision and Manipulation * 

   - Head Camera Bundle: with ZED Mini 

   - Wrist Camera Bundle: with RealSense D405 

   - Grippers Bundle: with Robotiq 2F-85 kit 

- Franka Gello Duo<sup>§</sup> 

Copyright © Franka Robotics GmbH 

10 



###### **NOTICE** 

**_<mark>* Refer to Quick Guide for Installaton FR3 Duo (Document Number: R04240) on</mark> i_** **_<u><mark>Franka Product Documentat</mark></u> i_** **_<u><mark>on.</mark></u>_** 

**_<mark>§ Refer to Quick Guide for Installat</mark> i_** **_<mark>on Franka GELLO Duo (Document number: R62040) on</mark>_** **_<u><mark>Franka Product Documentaton</mark></u> i_** **_<mark>.</mark>_** 

### **4.4 Other User Devices** 

Connecting additional user devices (e.g., PC, router, sensors) is permitted at dedicated locations on the TMR Top Plate and the Franka Spine Back Plate, where a dedicated grid of mounting points is provided. 

The risk assessment conducted does not cover additional interfaces/devices beyond those delivered with the system. Connecting additional user devices requires a renewed risk assessment to be performed by the user or system integrator. 

### **4.5 Limitations, Constraints and Misuse** 

Any application different to the intended use is misuse and is not permitted. This includes, but is not limited to, the following uses: 

###### **Operational Misuse** 

- Transport of people or animals. 

- Transport without original packaging. 

- Use as climbing assistance. 

- Leaning against the TMR. 

- Handling of liquids. 

###### **Environmental Restrictions** 

- Use in potentially explosive areas. 

- Use below ground or in confined spaces. 

- Not designed for flammable/explosive environments. 

- Use for the handling of radioactive objects. 

- Use outdoors. 

- Use in private environments e.g. real homes. 

- Use in the vicinity of children. 

###### **Safety And Compliance** 

- Use as a medical product. 

- Use outside of the specified operating limits. 

###### **Expected Environment** 

- Location: Dry, indoor lab or industrial setting. 

- Humidity: typically, non-condensing 

- Floor conditions: Clear paths; avoid uneven surfaces. 

- Shared spaces: Allowed but require restricted access and monitoring. 

###### **Required Operator Skill Level** 

- Trained R&D or technical personnel only 

- Must complete safety briefing and understand: 

   - Emergency stop procedures. 

   - `o` Handling of charging station 

   - Shared-space safety rules. 

Copyright © Franka Robotics GmbH 

11 



# **5 TACTILE MOBILE ROBOT** 

###### _(Type: Product Prototype)_ 

Tactile Mobile Robot is a prototype mobile platform optimized for research in the areas of autonomous navigation, obstacle avoidance and embodied AI. A seamless integration with Franka Research 3 and Franka Spine allows the user to transform the mobile platform into a mobile manipulator seamlessly. 

Some of the key features of the platform are omnidirectional drive and wireless charging. 



_Figure 9: Tactile Mobile Robot (TMR)_ 

### **5.1 Datasheet** 

###### **Tactile Mobile Robot** 

||**Platform**|**On**|**board devices**|
|---|---|---|---|
|**Drive System**|Holonomic / Omnidirectional|**Lidars**|2 x Sick NanoScan3|
|**Degrees of freedom**|3|**Cameras**|4 x Realsense D455|
|**Suspension type**|Three-point suspension|**IMU**|olixSense™ X1 Pro|
|**Dimensions**|800 x 583 x 370 mm|**User PC**|NVIDIA Jetson AGX Orin<br>Developer Kit (64GB)|
|**Max. payload**|125 kg|**Network switch**|Unifi Flex 2.5G 8-Port|
|**Max. speed**|1.5 m/s|**Router**|Teltonika RUTX10|
|**Weight**|130 kg|**Emergency Stop**|FORT VSC / WES|
||**Power**||1x HDMI<br>2x USB-C|
|**Batteries**|4x MuRata-LFP-TypeB<br>24V/21Ah|**External Ports**<br>**Panel**|2x Ethernet (Switch)<br>1x Ethernet (User PC)|
|**Battery voltage**|48 V||1x External Power<br>1x Manual Charging|
|**Total capacity**|44 Ah|||
|**Charging Rate**|Up to 2C|||
|**Charging System**|Wiferion CW1000|||



Copyright © Franka Robotics GmbH 

12 



### **5.2 Scope of Delivery** 

The following items are included in the delivery of the Tactile Mobile Robot system. Optional accessories are listed separately. 

###### **System Components** 

- Tactile Mobile Robot – TMR (Mobile Platform) 

###### **Accessories** 

###### **_<mark>See Chapter 5.3 Physical User Interfaces</mark>_** 

- FORT Robotics Wireless Emergency Stop 

- Microsoft X-Box Controller / Gamepad 

- External User Power Cable for the user power port on the UI Panel 

###### **Optional Accessories** 

- TMR Charging Station 

- Franka Spine 

### **5.3 Physical User Interfaces** 

#### **5.3.1 Power Switch and Rescue Charging Port** 

The power switch and charging port can be found on the front side of the TMR. 

**_<mark>Refer to Chapter 5.4 Turning on the TMR and Chapter 5.5 Shutng Down the TMR. For addit</mark> ti i_** **_<mark>onal informat</mark> i_** **_<mark>on on the Rescue Charging Port, see the chapter TMR Charging Stat</mark> i_** **_<mark>on.</mark>_** 



_Figure 10: Power Switch and Rescue Charging_ 

#### **5.3.2 Emergency Stops** 

The TMR is equipped with a redundant emergency stop (E-Stop) architecture designed to arrest all motion immediately upon activation. 

##### **_5.3.2.1 E-Stop Locations_** 

**Onboard:** Two physical E-Stop buttons are mounted on diagonally opposite corners of the TMR chassis for 360° accessibility. 

Copyright © Franka Robotics GmbH 

13 





_Figure 11: TMR onboard E-Stop_ 

**Wireless:** A handheld wireless E-Stop is provided for the safety operator. This must be maintained within line-ofsight of the robot during all autonomous or manual operations. 



_Figure 12: FORT Wireless E-Stop (WES-Tx)_ 

###### **NOTICE** 

If the wireless handheld E-Stop moves out of range of the TMR or loses battery power, the system will default to a Protective Stop. Always ensure the handheld unit is fully charged before beginning usage. 

##### **_5.3.2.2 System Protective Stops_** 

Activating any of the three E-Stops will lead to behaviors that vary by subsystem, as explained below: 

|**Subsystem**|**Stop**<br>**Category**|**Functional State**|**Mechanical Behavior**|
|---|---|---|---|
|TMR|Category 0|Safe Torque Off<br>(STO)|Power is cut immediately; mechanical brakes engage and<br>lock wheels.|
|Franka<br>Spine|Category 0|Power Removed|Power to the motor drive is severe; power to the motor<br>controller is still on; electromechanical holding brakes<br>engage.|
|FR3 Arms|Category 1|Controlled Stop|Joint motors execute a controlled deceleration to zero<br>velocity before the brakes engage.|
|**NOTICE**||||



The TMR drive units utilize mechanical braking during Category 0 events, and dynamic braking should be limited, i.e., stopping when the robot is in motion. Engaging the E-Stop while the TMR is at a standstill (e.g., when parked and during setup) does not utilize the friction budget and causes no significant wear to the braking system. 

#### **5.3.3 Configuration and pairing of the FORT wireless E-Stop** 

TMRv0.2 has a FORT Vehicle Safety Controller (VSC-Rx) that pairs with the portable FORT Wireless E-Stop (WESTx). To configure the VSC-Rx and access the FORT Configuration Tool, the USB-mini port is exposed on the VSCRx, as shown below. 



_Figure 13: FORT VSC-Rx Configuration Cable_ Copyright © Franka Robotics GmbH 

14 



###### **NOTICE** 

Detailed instructions for pairing and configuration of the VSC-WES will be described in the upcoming Quick Guide for Installation Mobile FR3 Duo (not yet released). If a need arises that the VSC and WES must be re-paired, contact the Franka team. 

**_<mark>Refer to the FORT Robot</mark> i_** **_<mark>cs products page for detailed informaton.</mark> i_** 

#### **5.3.4 UI-Panel and Related Connections** 

The UI Panel is located on the rear-top side of the TMR. The following ports are provided on the UI Panel: 



_Figure 14: UI Panel_ 

The User Power port on the UI panel consists of a 4-pin panel mount receptacle C016 20G003 100 12 from Amphenol. This accepts a C016 20H003 100 10 plug from Amphenol. 

#### **5.3.5 Battery SoC Monitor on the UI Panel** 

In the current prototype version of the TMR, a simple open-circuit voltage-based battery capacity read-out is integrated in the UI Panel. Given below is a table showing a mapping between SoC monitor voltage and the actual state of charge read from the battery BMS-SoC: 

|**SoC Monitor Voltage**|**State of Charge Approximation**|
|---|---|
|52.70 V|100%|
|52.15 V|70%|
|51.24 V|33%|
|50.87 V|25%|
|50.45 V|15%|



###### **NOTICE** 

In a system that experiences dynamic loading of the batteries, voltage-based estimations tend to be inaccurate. The user is advised to refer to the voltage read-out and not the percentage read-out on the monitor. 

For an accurate SoC of the system, the user should rely on the Battery Service functionality from the Franka Desk and Desk API. 

**_<mark>See Chapter 5.7 Sofware UI TMR v0.2</mark> t_** 

#### **5.3.6 Spine Connection Bays** 

The Spine Connection Bays Left/Right are located at the front-top side of the TMR: 

Copyright © Franka Robotics GmbH 

15 





_Figure 15: Spine Connection Bays_ 

#### **5.3.7 Router WAN Port** 

The WAN Port of the router can be accessed by removing the cover surrounding the UI Panel: 



_Figure 16: Exposed Router WAN Port_ 

#### **5.3.8 TMR Top Plate Mounting Holes** 

Mounting holes are provided to the user on the front and rear Top Plates of the TMR. 

Depending on the version of the TMR received, the user will find one of the following top plates on the front side of the TMR: 



_Figure 17: TMR Top Plate Front - variant A_ 

Copyright © Franka Robotics GmbH 

16 





_Figure 18: TMR Top Plate Front - variant B_ 

Copyright © Franka Robotics GmbH 

17 



Depending on the version of the TMR received, the user will find one of the following Top Plates on the rear side of the TMR: 





_Figure 20: Top Plate Rear - variant B_ 

Copyright © Franka Robotics GmbH 

18 



#### **5.3.9 TMR Type Label** 

To access the Type Label on the TMR, flip-open the enclosure on the right side of the TMR. 



_Figure 21: TMR Type Label_ 

### **5.4 Turning on the TMR** 

To turn on the TMR, simply twist the Power Switch to the ON position. 

###### **_<mark>See Chapter 5.3.1 Power Switch and Rescue Charging Port.</mark>_** 

### **5.5 Shutting Down the TMR** 

- Press and quickly release the soft shutdown button ( _short press of ~500ms_ ) to perform a soft shutdown of the robot controllers. 

###### **_<mark>See Figure 14: UI Panel</mark>_** 

- This is necessary to prevent data corruption on the controller disks. 

###### **_<mark>See Chapter 12.1 “Desk Shows 500 Internal Server Error”.</mark>_** 

- After the exhaust fans on the TMR top plate stop, twist the TMR’s Power Switch to fully turn off power from the rest of the system. 

###### **NOTICE** 

- For the soft shutdown to work for the TMR controller, the TMR needs to have the 5.9.2-tmr-os-0.3. 

- Holding the button ~4s will trigger a hard shutdown. 

### **5.6 Sensors** 

TMR integrates multiple sensors that interface with the User PC for environmental perception and navigation. 

#### **5.6.1 LIDARs** 

The TMR is equipped with two Sick NanoScan3 LIDARs that scan the environment using lasers to generate precise distance and outline data of surrounding objects. LIDARs are not pre-configured but can be set up using the Sick Safety Designer software **.** 

**<mark>Refer to the Sick documentaton</mark> i** **<mark>for conf</mark> i** **<mark>guraton instruct</mark> i** **<mark>ons.</mark> i** 

#### **5.6.2 IMU** 

The TMR features an Olive Robotics IMU providing precise orientation, acceleration, and angular rate measurements. The olixSense X1 Pro IMU is ROS 2 native and publishes sensor data to ROS 2 topics by default. 

Copyright © Franka Robotics GmbH 

19 



**Web interface access:** <u>http://192.168.7.100</u> 

###### **_<mark>Refer to the</mark>_** **_<u><mark>Olive Robot</mark></u> i_** **_<u><mark>cs documentat</mark></u> i_** **_<u><mark>on</mark></u>_** **_<mark>for detailed informaton.</mark> i_** 

###### **NOTICE** 

Modifying the IMU's IP address or topic names will break the provided ROS 2 demos. 

#### **5.6.3 Cameras** 

The TMR is equipped with four Intel RealSense D455 cameras for visual and depth data acquisition, positioned at the front, left, right, and rear of the platform. Additionally, a ZED Mini Stereo Camera is mounted on the Franka Head Bracket, and one RealSense D405 is mounted on each wrist of the FR3 Duo. 

#### **5.6.4 Sensor Testing** 

A comprehensive test suite is available to verify sensor functionality. Execute **test_sensors** in the terminal to run automated tests for IMU frequency and gravity detection, LIDAR frequency and range measurements, camera frequency and image quality, as well as position verification tests. Use **test_sensors --help** for all available options. 

### **5.7 Software UI TMR v0.2** 

The TMR user interface is based on the interface provided with Franka Research 3, featuring familiar pages under Settings: 



_Figure 22: User Interface_ 

###### **Dashboard** 

Displays the state of the robotic system, including: 

- **Drives** (enable/disable, recovery options) 

- **Spine** (enable/disable, recovery options) 

- **Battery status** (start/stop charging) 

###### **_NOTICE_** 

_Some features may be unavailable in early versions._ 

###### **Network** 

- Allows setting up the network interface for the TMR. T 

- Internal router configuration is pre-set. 

###### **System** 

- Allows you to download safety and other log files 

Copyright © Franka Robotics GmbH 

20 



###### **Software Updates** 

- Allow us to update the system image version when a new version is assigned in Franka World. 

### **5.8 Software Integration Interfaces TMR v0.2** 

The software interfaces for the TMR can be found under the following routes: 

- **<robot-ip>/deskapi** for the normal DeskAPI functionality that lets you set up your robot 

   - **<robot-ip>/spineapi** that allows the user to enable and recover the spine 

- **<robot-ip>/driveapi** that allows to enable and recover the drives. 

All three APIs mentioned above provide OpenAPI specifications, that allow direct interaction. 

### **5.9 Internal network setup** 

The internal network comes pre-configured, with all components assigned IP addresses via DHCP from the WiFi router. This setup ensures IP address consistency, even after a factory reset. Furthermore, each device is accessible via a unique DNS hostname (e.g., Desk of the Right arm is available at <u>https://right/). All components connect</u> through a high-performance switch, and each TMR broadcasts a WiFi network with a unique SSID. Passwords are provided on the TMR labels. Please note that FCI over WiFi is not supported. 



_Figure 23: System Overview of FR3 DUO Setup_ 

#### **5.9.1 IP Address Allocation** 

**RUTX10 Router:** 

`o` IP: 172.16.16.1 `o` DNS: router `o` Web UI: https://router/ 

- TMR Base: 

`o` IP: 172.16.16.10 `o` DNS: tmr `o` DESK UI: https://tmr/ 

Copyright © Franka Robotics GmbH 

21 



• Right Arm: `o` IP: 172.16.16.11 `o` DNS: right `o` DESK UI: https://right/ • Left Arm: `o` IP: 172.16.16.12 `o` DNS: left `o` DESK UI: https://left/ • User PC: `o` IP: 172.16.16.50 `o` DNS: companion `o` SSH: ssh tmr-user@companion • Front LIDAR `o` IP: 172.16.16.60 `o` DNS: front-lidar • Rear LIDAR `o` IP: 172.16.16.61 `o` DNS: rear-lidar • DHCP Range (Dynamic Allocation) `o` Any devices not listed above will be assigned an IP address from the following pool: 172.16.16.100 - 172.16.16.249 

#### **5.9.2 Wireless Configuration** 

The wireless network names (SSIDs) are derived from the Serial Number (SN) of the TMR unit. 

- 2.4 GHz: 

   - SSID: TMR_<SN>_2G (e.g., `TMR_12345678_2G`) 

- 5 GHz: 

   - SSID: TMR_<SN>_5G (e.g., `TMR_12345678_5G`) 

#### **5.9.3 Internet Access for internal components for Software Updates.** 

To update the robot software, you can use either (1) offline sync or (2) online sync. 

##### **_5.9.3.1 (1) Offline Sync_** 

Please follow the instructions of the Franka Robot Manual. 

##### **_5.9.3.2 (2) Online Sync_** 

Online sync requires the router's WAN port to be connected to a network with internet access, or the configuration of a WiFi WAN bridge. To locate the WAN port in the TMR **_._** 

###### **_<mark>For more informaton, refer to Chapter 5.3 (Physical User Interfaces).</mark> i_** 

Alternatively, you can use a WiFi WAN bridge. This procedure is described in the Teltonika manual, see <u>https://wiki.teltonika-networks.com/view/WiFi_WAN_example.</u> 

Once the WAN connection is established, navigate to _Settings -> Software Update_ in DESK (e.g., accessed through <u>https://right/). If the configuration is correct, the Franka World status indicator will display</u> _‘connected’_ . You can also verify the WAN connection from the user's PC **.** Proceed by following the instructions in the Franka Robot manual to install the update. 

### **5.10 Working with User PC of TMR v0.2** 

The User PC serves as the interface for interacting with the TMR. It is an NVIDIA® Jetson AGX Orin™ Developer Kit with powerful onboard edge computation, combining GPU and CPU performance with CUDA cores for AI and vision algorithms. It features a real-time kernel. 

#### **5.10.1 System specifications** 

- Operating System: Ubuntu 22.04 

Copyright © Franka Robotics GmbH 

22 



- ROS Distribution: ROS 2 Humble 

- Docker and Docker Compose installed. 

- User: tmr-user (default password: user-TMR, sudo rights enabled) 

#### **5.10.2 Access methods** 

- Via Switch network (left/middle ethernet port on external ports panel or WiFi): 

- ssh tmr-user@172.16.16.50 or ssh tmr-user@companion 

- • Direct connection to User PC (right ethernet port on external ports panel): 

   - ssh tmr-user@172.16.1.9 

- Direct: Connect HDMI, mouse, and keyboard to the external ports on the top of the TMR 

#### **5.10.3 ROS 2 workspace setup** 

Create additional ROS 2 projects in /home/tmr-user/ros2_ws/src/. To build, navigate to /home/tmr-user/ros2_ws/ and execute colcon build. 

#### **5.10.4 Available Demos** 

Demo source code is located in /home/tmr-user/ros2_ws/src/. 

#### **5.10.5 Repositories** 

- <u>franka_descriptoni</u> (branch: humble) - URDF and meshes 

- <u>franka_ros2</u> (branch: humble) - ROS 2 packages 

Updates are pushed to these branches and can be pulled via `git pull`. For access credentials, contact <u>support@franka.de.</u> 

#### **5.10.6 Gamepad Demo** 

Control the TMR using ROS 2 Humble and the included Xbox controller that is integrated via the Xone firmware. 

**Prerequisites:** 

- Ensure the robot is not blocked by safety. 

#### **5.10.7 Steps** 

1. Open terminal: Direct access (screen/mouse/keyboard) or ssh tmr-user@172.16.16.50 

2. Run **screen** to create a detachable session 

**3.** Run the demo: 

Either directly executing **gamepad_demo** or running the following command from the ROS2 workspace: **ros2 launch franka_bringup mobile_teleop.launch.py** 

**controller_names:="mobile_cartesian_velocity_example_controller"** 

4. Power on Xbox controller (steady white light confirms pairing) 

5. Detach session: Press CTRL-A then d 

6. Reconnect to session if desired with screen –r 

###### **NOTICE** 

Ensure no other Xbox controllers or TMRs are powered to avoid connection disruption and potentially crashing the TMR. If connection or pairing issues persist, use a USB cable between the Xbox controller and the User PC USB-A port on the UI Panel. 

#### **5.10.8 Controls** 

- Hold RB button to enable control. 

- Left joystick: Command linear velocities in x and y (translation). 

Copyright © Franka Robotics GmbH 

23 



- Right joystick: Command angular velocity in z (rotation). This joystick can only be moved sideways. 

- 

- Hold LB button to increase the maximum speed. 

#### **5.10.9 ROS 2 Sensors Demo** 

Visualize sensors, cameras, and LIDARs in RViz. 

- Connect to User PC: Direct access (screen/mouse/keyboard) or **ssh -C -X** **<u>tmr-user@172.16.16.50</u>** 

- Execute either sensors_demo or ros2 launch franka_mobile_sensors franka_mobile_sensors.launch.py 

RViz displays the TMR model with LIDAR surroundings detection. Each camera output appears in a separate window. View all sensor topics with **ros2 topic list** . 

Copyright © Franka Robotics GmbH 

24 



# **6 FR3 DUO** 

_(Type: Product Prototype)_ 

The FR3 Duo is a prototype dual-arm system optimized for research in the areas of teleoperation, manipulation, and embodied AI. This system is intended to be used exclusively for use in research and development within industrial laboratory environments and/or for training and educational purposes related to industrial applications. It is not designed or approved for production use or safety-critical applications. 



_Figure 24: FR3 Duo_ 

### **6.1 Datasheet** 

||**FR3 Duo**|
|---|---|
|**Degrees of freedom**|14|
|**Max. payload**|Each FR3 Arm: 3 kg|
|**Weight**|45|



### **6.2 Scope of Delivery** 

The following items are included in the delivery of the FR3 Duo system. Optional accessories are listed separately. 

**System Components** 

- FR3 Duo Mounting Kit 

- Franka Research 3 

Currently, there are two options to mount and use the FR3 Duo system: using the Franka Spine or the Pedestal. 

Copyright © Franka Robotics GmbH 

25 



**Optional Components** 

- Franka Spine 

- Pedestal * 

- FR3 Duo Vision and Manipulation * 

   - Head Camera Bundle: with ZED Mini 

   - Wrist Camera Bundle: with RealSense D405 

   - Grippers Bundle: with Robotiq 2F-85 kit 

- Franka Gello Duo<sup>§</sup> 

**NOTICE** 

**_* Refer to Quick Guide for Installation FR3 Duo (Document Number: R04240) on Franka Product Documentation._** **_<mark>§ Refer to Quick Guide for Installat</mark> i_** **_<mark>on Franka GELLO Duo (Document number: R62040) on</mark>_** **_<u><mark>Franka Product Documentaton</mark></u> i_** **_<mark>.</mark>_** 

Copyright © Franka Robotics GmbH 

26 



# **7 TMR CHARGING STATION** 

_(Type: Accessory Prototype)_ 

The TMR Charging Station is the primary charging system intended for the TMR. The charging station consists of a wireless charger intended for nominal usage. The wired charger is intended to be used as a rescue charger to charge stranded TMRs with drained batteries. 



_Figure 25: TMR charging station_ 

### **7.1 Datasheet** 

||**TMR Charging Station**|
|---|---|
|**Dimensions**|420 x 390 x 1000 mm|
|**Weight**|27 kg|
|**Wireless Charger**|Wiferion Wallbox & Sending Pad (SEPA)|
|**Manual Charger**|HEP- 600C|



### **7.2 Scope of Delivery** 

The following items are included in the delivery of the Tactile Mobile Robot system. Optional accessories are listed separately. 

###### **System Components** 

- Tactile Mobile Robot – TMR (Mobile Platform) 

###### **Optional Accessories** 

- TMR Charging Station 

- Franka Spine 

### **7.3 Nominal Charging Sequence** 

During nominal use, the TMR is intended to be charged using the inductive wireless charger on the Charging Station. 

Copyright © Franka Robotics GmbH 

27 





_Figure 26: TMR nominal charging_ 

###### **SAFTEY-INSTRUCTIONS** 

Ensure that the Charging Station is connected to the mains supply and is turned off. 

###### **NOTICE** 

- Ensure that the TMR is enabled/powered on before wireless charging takes place. 

- Wireless charging is not possible when the TMR is powered off. 

**Steps for wireless charging:** 

1. Pull open the wireless charging pad (SEPA) and lay it flat on the floor. 

2. With the SEPA on the floor, move the Charging Station and position it approximately centered on the rearside of the TMR. The SEPA should slide underneath the TMR. 

3. The SEPA from must be aligned with the Mobile Charging Pad (MOCHA) underneath the TMR for the inductive charging to begin. The Wiferion inductive charging system allows a high positional tolerance between these charging pads. 

4. Once correct positioning is ensured, turn on the Charging Station. 

5. The SoC indicator on the UI Panel should show rising voltage to confirm that charging is taking place. 

### **7.4 Rescue charging sequence.** 

When the TMR runs out of battery, wireless charging is not possible. This rescue charging sequence is intended, as the name suggests, to rescue the TMR from such situations.  Once enough charge is provided, the user can revert to nominal charging sequence with the wireless charger. 

Copyright © Franka Robotics GmbH 

28 





_Figure 27: TMR rescue charging_ 

###### **SAFTEY-INSTRUCTIONS** 

1. Ensure that the Charging Station is connected to the mains supply and is turned off. 

2. Ensure that the TMR is powered off. 

**Steps for manual rescue charging:** 

1. Connect the cables (with SPK connectors on both ends) to the charging station and to the TMR. 

2. Turn on the Charging Station mains switch. 

3. Turn on the TMR Power Switch 

###### **WARNING** 

Do not use the Wiferion wireless charger for charging the system overnight. If there is a need for overnight charging, for example to rebalance the batteries, use the wired charging system. 

### **7.5 Software-Interfaces** 

The primary software interface for the TMR is libfranka, for operational tasks such as monitoring the battery status and managing charging (start/stop). The TMR User Interface (UI) offers dedicated controls within the Dashboard page. 

Copyright © Franka Robotics GmbH 

29 



# **8 FRANKA SPINE** 

_(Type: Accessory Prototype)_ 

The Franka Spine is a vertical lift design primarily to provide an additional degree of freedom during dual-arm manipulations. 

It is compatible with: 

- **TMR** – enabling integration with the Tactile Mobile Robot platform. 

- **Spine Pedestal** (not yet available for users). 



_Figure 28: Franka Spine_ 

### **8.1 Datasheet** 

||**Franka Spi**|**ne**||
|---|---|---|---|
|**Drive system**|linear guideway and ball-screw|**Back-drive resistance**|300W 10Ω|
|**Degrees of Freedom**|1|**Lead**|20 mm/rev|
|**Dimensions**|300 x 275 x 1111 mm|**Stroke**|827 mm|
|**Weight**|45 kg|**Max Input Torque**|2.37 Nm|
|**Max. Payload**|50 kg|**Max Holding Torque**|1.91 Nm|
|**Max. Speed**|0.3 m/s|||



Copyright © Franka Robotics GmbH 

30 



### **8.2 Physical User Interfaces** 

#### **8.2.1 Spine Back and Top Plate Mounting Holes** 



_Figure 29: Spine back plate_ 



_Figure 30: Spine top plate_ 

### **8.3 Software Interfaces** 

The primary software interface for the TMR is libfranka, the same library used for controlling Franka Research 3 robots. 

For operational tasks such as spine recovery and enabling/disabling the spine, the TMR user interface (UI) provides dedicated controls within the Dashboard page. 

Copyright © Franka Robotics GmbH 

31 



# **9 FR3 DUO MOUNTING KIT V0.3** 

_(Type: Accessory Prototype)_ 



_Figure 31: FR3 Duo Mounting Kit v0.3_ 

### **9.1 Datasheet** 

||**FR3 Duo Mounting Kit v0.3**|
|---|---|
|**Dimensions**|290mm x 210mm x 250mm|
|**Weight**|5 kg|
|**Maximum payload**|50 kg|
|**Degrees of freedom**|0|
|**Orientation of**<br>**Arm Adapter**|leftArm Adapter*:<br>[Roll, Pitch, Yaw] =<br>[-51.18507533, -10.00159382, -<br>26.54771649] °<br>right Arm Adapter*:<br>[Roll, Pitch, Yaw] =<br>[+51.18507533, -10.00159382,<br>+26.54771649] °|
||*As seen from the front view|
|**Installation**<br>**position**|upright|
|**Ambient**<br>**temperature**|+5 to +45 °C|



**_<mark>Refer to the Quick Guide for Installat</mark> i_** **_<mark>on FR3 Duo (R04240) for more details.</mark>_** 

Copyright © Franka Robotics GmbH 

32 



# **10 FRANKA HEAD BRACKET V0.2** 

_(Type: Accessory prototype)_ 

The Franka Head Bracket v0.2 has a camera holder compatible only with the ZED Mini camera. 

The bracket is compatible with being mounted on top of the FR3 Duo Mount v0.3. 



_Figure 32: Franka Head Bracket v0.2_ 

### **10.1 Datasheet** 

||**Franka Head Bracket v0.2**|
|---|---|
|**Dimensions**|250mm x 82mm x 80mm|
|**Weight**|~1 kg|



**_<mark>Refer to the “Quick Guide for Installaton FR3 Duo” (</mark> i_** **_<mark>R04240) for more details</mark>_** <mark>.</mark> 

Copyright © Franka Robotics GmbH 

33 



# **11 HANDLING, TRANSPORT & MAINTENANCE** 

This section provides guidelines for the safe handling, transportation, and maintenance of the Tactile Mobile Robot (TMR). Proper handling is essential to prevent damage to the robot and ensure the operator’s safety. The technical drawing below illustrates the dimensions and structural layout, which should be considered when planning lifting, transport, and maintenance activities. 



_Figure 33: Technical illustration_ 

Copyright © Franka Robotics GmbH 

34 



### **11.1 Areas for Manual Handling without Special Equipment** 

The designated area for safely lifting the TMR manually by a minimum of 4 people is as shown below: 



_Figure 34: Designated Manual Handling Zones for TMR_ 

###### **NOTICE** 

The rear part of the TMR has a rear-axle which swivels about its axis. Lifting the TMR in this area poses a risk of clamping of fingers or hands. 

### **11.2 Areas for Handling with Special Equipment** 

Still being defined. 

Copyright © Franka Robotics GmbH 

35 



# **12 FAQ** 

### **12.1 Desk Shows 500 Internal Server Error** 



_Figure 35: Server showing a 500 Internal Server Error_ 

This error indicates that the data on the disk of the TMR controller was corrupted during shutdown. It can be resolved by booting into the Rescue System and performing a Factory Reset. 

**NOTICE** Contact the Franka team for a clear description to troubleshoot this error. 

The process of fixing the above error will delete your configuration and all installed features. These will need to be reinstalled. 

Copyright © Franka Robotics GmbH 

36 



# **13 TABLE OF FIGURES** 

|Figure 1: TMR Type Label ................................................................................................................................................................7|
|---|
|Figure 2: Franka Spine Type Label .................................................................................................................................................7|
|Figure 3: TMR Charging Station .....................................................................................................................................................7|
|Figure 4: Mobile FR3 Duo................................................................................................................................................................8|
|Figure 5: Side and top views of the robot workspace, showing maximum reach and operating envelope dimensions.<br>9|
|...............................................................................................................................................................................................................<br>Figure 6: ISO cube for FR3 Duo .....................................................................................................................................................9|
|Figure 7: Dual arm workspace. .................................................................................................................................................... 10|
|_Figure_8_: Workspace relative to Franka Spine Position_............................................................................................................... 10|
|Figure 9: Tactile Mobile Robot (TMR) ........................................................................................................................................ 12|
|Figure 10: Power Switch and Rescue Charging........................................................................................................................ 13|
|Figure 11: TMR onboard E-Stop ................................................................................................................................................. 14|
|Figure 12: FORT Wireless E-Stop (WES-Tx) ............................................................................................................................. 14|
|Figure 13: FORT VSC-Rx Configuration Cable......................................................................................................................... 14|
|Figure 14: UI Panel ......................................................................................................................................................................... 15|
|Figure 15: Spine Connection Bays .............................................................................................................................................. 16|
|Figure 16: Exposed Router WAN Port ....................................................................................................................................... 16|
|Figure 17: TMR Top Plate Front - variant A ............................................................................................................................. 16|
|Figure 18: TMR Top Plate Front - variant B.............................................................................................................................. 17|
|Figure 19: Top Plate - variant A................................................................................................................................................... 18|
|Figure 20: Top Plate Rear - variant B ......................................................................................................................................... 18|
|Figure 21: TMR Type Label .......................................................................................................................................................... 19|
|Figure 22: User Interface .............................................................................................................................................................. 20|
|Figure 23: System Overview of FR3 DUO Setup .................................................................................................................... 21|
|Figure 24: FR3 Duo ........................................................................................................................................................................ 25|
|Figure 25: TMR charging station ................................................................................................................................................. 27|
|Figure 26: TMR nominal charging ............................................................................................................................................... 28|
|Figure 27: TMR rescue charging.................................................................................................................................................. 29|
|Figure 28: Franka Spine................................................................................................................................................................. 30|
|Figure 29: Spine back plate .......................................................................................................................................................... 31|
|Figure 30: Spine top plate ............................................................................................................................................................. 31|
|Figure 31: FR3 Duo Mounting Kit v0.3...................................................................................................................................... 32|
|Figure 32: Franka Head Bracket v0.2 ......................................................................................................................................... 33|
|Figure 33: Technical illustration .................................................................................................................................................. 34|
|Figure 34: Designated Manual Handling Zones for TMR ....................................................................................................... 35|
|Figure 35: Server showing a 500 Internal Server Error .......................................................................................................... 36|



Copyright © Franka Robotics GmbH 

37 



Franka Robotics GmbH Koppstraße 12 81379 Munich Germany 

Copyright © Franka Robotics GmbH 38 

