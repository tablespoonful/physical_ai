> **[PDF を開く](<Operating Manual Franka Research 3_5.10_R02216_1.3_EN.pdf>)**
>
> PDF から自動変換した本文です。図は含まず、表は崩れている場合があります。安全や仕様の確認には PDF を使ってください。



Operating Manual FRANKA RESEARCH 3 

TABLE OF CONTENTS 

© Copyright 2026 Franka Robotics GmbH Koppstraße 12 81379 Munich Germany 

The information in this document, including any extracts, may only be reproduced or shared with third parties with the explicit authorization of Franka Robotics GmbH. 

The content of this document has been carefully checked against compliance with the hardware and software described. However, discrepancies cannot entirely be ruled out, which is why we assume no liability for complete compliance. 

In the interest of our customers, we reserve the right to make improvements and corrections to hardware, software, and documentation at any point in time without notice. 

We are always grateful for your feedback at documentation@franka.de. 

The English documentation is the ORIGINAL DOCUMENTATION. Other languages are translations of the original document. 

Complementary documents for this operating manual are: 

- Datasheet Franka Research 3 (Document number: R02212) 

- ESD Measurements FR3 (Document number: R02015) 

- Quick Guide for Installation FR3 (Document number: R02040) 

- Hardware Manual Franka Research 3 (Document number: R02210) 

Document name:                Operating Manual Franka Research 3 

Document number:            R02216 

System image: System image version 5.10 

Change Log: 

|**Content Iteration**|**Release Date**|**Release notes / Changes**|
|---|---|---|
|1.3|June 2026|Release of the Operating Manual for system image version 5.10. Updated the sidebar with<br>zoom-in and zoom-out features and improved the menu settings.|





Get your manual and additional supporting material in English and other languages at www.franka.de/documents. 

R02216/1.3/EN 

Franka Robotics GmbH © 

2 

TABLE OF CONTENTS 

# **TABLE OF CONTENTS** 

|TABLE OF|CONTENTS .................................................................................................................................................................... 3|
|---|---|
|1<br>ABO|UT THE MANUAL ............................................................................................................................................................ 7|
|1.1|Software and hardware version ................................................................................................................................. 7|
|1.2|Applicable document .................................................................................................................................................... 7|
|2<br>SAFE|TY INSTRUCTIONS AND GENERAL INDICATIONS ............................................................................................... 8|
|3<br>GETT|ING STARTED ................................................................................................................................................................. 9|
|3.1|Initial setup ..................................................................................................................................................................... 9|
|3.1.1|Connecting a user interface device ...................................................................................................................... 9|
|3.1.2|Hardware recommendation ................................................................................................................................... 9|
|3.1.3|Procedure .................................................................................................................................................................. 9|
|3.1.4|Initial configuration – “First Start” ..................................................................................................................... 10|
|3.1.5|Initial Sync During First Start .............................................................................................................................. 13|
|3.2|Unexpected motions during guiding ...................................................................................................................... 14|
|3.3|Falling objects during installation ........................................................................................................................... 14|
|3.4|End effector configuration ....................................................................................................................................... 14|
|4<br>TYPIC|AL USAGES .................................................................................................................................................................. 15|
|5<br>WOR|KING WITH FRANKA RESEARCH 3........................................................................................................................ 16|
|5.1|Robotic basics ............................................................................................................................................................. 16|
|5.2|Single point of control (SPoC) .................................................................................................................................. 17|
|5.2.1|Take control ........................................................................................................................................................... 17|
|5.2.2|Request control ..................................................................................................................................................... 17|
|5.2.3|Enforce control ...................................................................................................................................................... 19|
|5.2.4|Release control ...................................................................................................................................................... 19|
|5.2.5|Fieldbus control ..................................................................................................................................................... 19|
|5.3|Operating modes ........................................................................................................................................................ 20|
|5.3.1|Programming ............................................................................................................................................................... 21|
|5.3.2|Jogging in joint space ................................................................................................................................................ 22|
|5.3.3|Execution ..................................................................................................................................................................... 24|
|5.4|Apps .............................................................................................................................................................................. 29|
|5.5|Creating a Task ........................................................................................................................................................... 29|
|5.6|Task settings ............................................................................................................................................................... 30|
|5.7|Parameterization of Apps ......................................................................................................................................... 30|
|5.8|Pose teaching .............................................................................................................................................................. 31|
|5.9|Pose fine adjustment ................................................................................................................................................. 32|
|5.10|Guiding configurations .............................................................................................................................................. 33|
|5.11|Necessary guiding components .............................................................................................................................. 34|
|5.12|Guiding ......................................................................................................................................................................... 35|
|5.13|Editing end effector settings.................................................................................................................................... 36|
|6<br>FRAN|KA UI.............................................................................................................................................................................. 38|



R02216/1.3/EN 

Franka Robotics GmbH © 

3 

##### TABLE OF CONTENTS 

|6.1|Login ............................................................................................................................................................................. 38|
|---|---|
|6.1.1|Elements ................................................................................................................................................................. 38|
|6.2|Desk .............................................................................................................................................................................. 39|
|6.2.1|Overview ................................................................................................................................................................ 39|
|6.2.2|Elements ................................................................................................................................................................. 40|
|6.3|Watchman ................................................................................................................................................................... 42|
|6.4|Settings Interface ....................................................................................................................................................... 43|
|6.4.1|Elements ................................................................................................................................................................. 43|
|7<br>ROLE|S AND PERSONNEL ................................................................................................................................................... 45|
|7.1|Personnel ..................................................................................................................................................................... 45|
|7.1.1|Responsible person ............................................................................................................................................... 45|
|7.1.2|User .......................................................................................................................................................................... 45|
|7.1.3|Integrator ................................................................................................................................................................ 45|
|7.2|User Roles .................................................................................................................................................................... 46|
|7.2.1|Operator ................................................................................................................................................................. 46|
|7.2.2|Administrator ......................................................................................................................................................... 46|
|7.2.3|Safety operator ...................................................................................................................................................... 46|
|7.2.4|Assigning user roles .............................................................................................................................................. 47|
|8<br>MAN|AGING FRANKA RESEARCH 3 ................................................................................................................................. 47|
|8.1|Franka World .............................................................................................................................................................. 47|
|8.2|Hub ............................................................................................................................................................................... 48|
|8.3|Managing Apps and Features .................................................................................................................................. 48|
|8.4|Updates ........................................................................................................................................................................ 48|
|8.5|Backup .......................................................................................................................................................................... 54|
|8.6|Backing up and exporting safety configuration ................................................................................................... 55|
|8.7|Network Setting ......................................................................................................................................................... 56|
|8.8|Modbus Configuration .............................................................................................................................................. 56|
|8.9|End Effector Configuration ...................................................................................................................................... 56|
|8.10|Saving the created Tasks .......................................................................................................................................... 57|
|9<br>TROU|BLESHOOTING ........................................................................................................................................................... 58|
|9.1|General use .................................................................................................................................................................. 58|
|9.1.1|Recoverable errors ................................................................................................................................................ 58|
|9.1.2|Arm pulls strongly in one direction during teaching ...................................................................................... 58|
|9.1.3|Loud clicking at switch-off .................................................................................................................................. 58|
|9.1.4|Joint limit error ...................................................................................................................................................... 59|
|9.1.5|Joint position error ............................................................................................................................................... 60|
|9.1.6|Failed to unlock joints .......................................................................................................................................... 65|
|9.1.7|Robot does not finish booting ............................................................................................................................ 65|
|9.1.8|Desk continuously displays “Shutting down the system” ............................................................................. 66|
|9.1.9|Robot does not boot after turning on the Control ......................................................................................... 66|
|9.1.1|0<br>Restarting after an unexpected stop ................................................................................................................. 66|



R02216/1.3/EN 

Franka Robotics GmbH © 

4 

##### TABLE OF CONTENTS 

|9.2<br>Troubleshooting while using FCI ............................................................................................................................ 66|
|---|
|10<br>ADVANCE CONTROL ................................................................................................................................................... 67|
|10.1<br>Franka Control Interface (FCI) ................................................................................................................................. 67|
|10.2<br>Working in principle with the FCI interface ......................................................................................................... 68|
|10.3<br>Setup of Franka Control Interface (FCI) ................................................................................................................ 71|
|10.3.1<br>Network Configuration for FCI .......................................................................................................................... 71|
|10.3.2<br>Static IP Configuration Example ........................................................................................................................ 72|
|10.3.3<br>Configuring Control’s Network .......................................................................................................................... 72|
|10.3.4<br>Configuring the Operating Device (Ubuntu 20.04)........................................................................................ 72|
|10.4<br>Setup of libfranka on a Linux workstation ............................................................................................................ 74|
|10.5<br>Verification of communication ................................................................................................................................ 78|
|11<br>Safety Concept ................................................................................................................................................................ 79|
|11.1<br>Safety Functions ......................................................................................................................................................... 80|
|11.2<br>Other safety-related recoveries (in case of safety errors) ................................................................................. 83|
|12<br>SAFETY RULES AND SCENARIOS/WATCHMAN................................................................................................... 84|
|12.1<br>Watchman ................................................................................................................................................................... 84|
|12.1.1<br>Overview ................................................................................................................................................................ 84|
|12.2<br>Safety Rules and Scenarios in Watchman ............................................................................................................. 86|
|12.2.1<br>Adjusting predefined scenarios and rules ........................................................................................................ 86|
|12.2.2<br>Safety Scenarios for states in Programming mode ........................................................................................ 87|
|12.2.3<br>Safety Scenarios for states in execution mode ............................................................................................... 87|
|12.2.4<br>Error/Violation states ........................................................................................................................................... 87|
|12.2.5<br>Editing of the Safety Configuration ................................................................................................................... 88|
|12.3<br>Import/Export of Safety Settings............................................................................................................................ 91|
|12.3.1<br>Import Procedure .................................................................................................................................................. 92|
|12.3.2<br>Export Procedure .................................................................................................................................................. 94|
|12.4<br>Safety Setup ................................................................................................................................................................ 95|
|12.5<br>General Safety Settings ............................................................................................................................................ 95|
|12.6<br>Safe Input Configuration .......................................................................................................................................... 96|
|12.7<br>End Effector Configuration ...................................................................................................................................... 96|
|12.8<br>Creation of spheres for modelling an End effector envelope ........................................................................... 97|
|12.9<br>Creating and editing rules ........................................................................................................................................ 99|
|12.10<br>Structure of a rule ...................................................................................................................................................... 99|
|12.11<br>Validate ...................................................................................................................................................................... 103|
|12.11.1<br>Validating safe inputs .................................................................................................................................... 104|
|12.11.2<br>Validating SLP-C ............................................................................................................................................. 104|
|12.11.3<br>Validating SLS-C ............................................................................................................................................. 104|
|12.11.4<br>Validating SEEPO ........................................................................................................................................... 104|
|12.11.5<br>Validating the entire rules, scenarios and overall configuration .......................................................... 104|
|13<br>ROBOT LED INDICATOR SYSTEM........................................................................................................................... 106|
|13.1<br>Overview of the status indicators......................................................................................................................... 106|



R02216/1.3/EN 

Franka Robotics GmbH © 

5 

##### TABLE OF CONTENTS 

|13.2|LED Activation Behavior ........................................................................................................................................ 106|
|---|---|
|13.3|Startup Checklist for Operators ............................................................................................................................ 107|
|13.4|Flashing Patterns ...................................................................................................................................................... 107|
|13.5|LED Priority Logic .................................................................................................................................................... 107|
|13.6|LED Color Reference Table .................................................................................................................................... 108|
|14<br>S|ERVICE AND SUPPORT ............................................................................................................................................ 111|
|14.1|Rescue System .......................................................................................................................................................... 111|
|14.1|.1<br>Using the Desk API: ............................................................................................................................................ 111|
|14.1|.2<br>Using Franka UI: .................................................................................................................................................. 111|
|14.2|Log download............................................................................................................................................................ 115|
|14.2.1|Available log files and how to download them ............................................................................................. 115|
|14.2.2|Downloading log data ........................................................................................................................................ 116|
|14.3|Torque calibration .................................................................................................................................................... 117|
|14.3.1|When to calibrate the torque sensors ............................................................................................................ 118|
|14.3.2|How to calibrate torque sensors ...................................................................................................................... 118|
|14.3.3|Reset to factory defaults ................................................................................................................................... 121|
|14.3.4|Error handling ...................................................................................................................................................... 121|
|14.4|Hardware Exchange................................................................................................................................................. 122|
|14.4.1|Replacing the Control ......................................................................................................................................... 122|
|14.5|Transportation pose of the Arm ............................................................................................................................ 123|
|15<br>I|NDEX .............................................................................................................................................................................. 128|
|16<br>T|ABLE OF FIGURES ..................................................................................................................................................... 130|



R02216/1.3/EN 

Franka Robotics GmbH © 

6 

ABOUT THE MANUAL 

# **1 ABOUT THE MANUAL** 

This operating manual gives the information that you need to operate and handle the **Franka Research 3 (FR3)** robot system in a safe and correct way. 

This manual includes: 

- Instructions for the initial setup 

- Information about hardware and software configuration 

- Descriptions of typical use cases 

- Instructions to use the Franka UI, apps, and the Franka Control Interface (FCI) 

- Safety instructions 

- Managing apps and updates 

- Troubleshooting steps 

- Advanced configuration procedures 

Use this manual during installation, operation, and maintenance of the FR3 robot system. 

## **1.1 Software and hardware version** 

This manual applies to system image version 5.10. This version is compatible with all versions of the FR3 robot. 

## **1.2 Applicable document** 

In addition to this manual, the following document also applies: 

- **Hardware Manual:** Franka Research 3 with Arm v2.1. 

- **Hardware Manual:** Franka Research 3 with Arm v2.0. 

- **Hardware Manual:** Franka Research 3 with Arm v1. 

- **Document Number:** R02210 

R02216/1.3/EN 

Franka Robotics GmbH © 

7 

SAFETY INSTRUCTIONS AND GENERAL INDICATIONS 

# **2 SAFETY INSTRUCTIONS AND GENERAL INDICATIONS** 



##### **IMPORTANT** 

Before installing, starting up, or operating the device, please read this manual thoroughly, including all supplementary documentation. It is essential to observe the safety instructions and general indications provided here. 

- This chapter contains critical **warning notices** , which are structured as follows: 

   - Type of hazard 

   - Potential consequences of hazard 

   - Evasive/avoidance actions to be taken 

- The following warning notices are used in this manual: 



##### **DANGER** 

DANGER indicates a hazardous situation that, if not avoided, will result in death or serious injury. 



##### **WARNING** 

WARNING indicates a hazardous situation that, if not avoided, could result in death or serious injury. 



##### **CAUTION** 

CAUTION indicates a hazardous situation that, if not avoided, could result in minor or moderate injury. 

##### **_NOTICE_** 

NOTICE indicates information considered important but not hazard related. 



SAFETY INSTRUCTION indicates processes that need to be strictly observed. 

##### **Indications** 



Indicates where further information can be obtained. 

Franka Research 3 is equipped with a comprehensive safety system designed to meet application-specific requirements and international safety standards. For an overview of the system architecture, safety functions, and configuration using the Watchman tool, **_<mark>please refer to the chapter 11 titled ‘’Safety Concept’’ in this Manual</mark>_** _<mark>.</mark>_ 

R02216/1.3/EN 

Franka Robotics GmbH © 

8 

GETTING STARTED 

For additional safety measures and potential hazards **_<mark>, refer to Chapter 4 ‘’Safety’’ in the respective Hardware Manual (i.e. Franka Research 3 Arm v1 or Franka Research 3 Arm v2).</mark>_** 

# **3 GETTING STARTED** 

## **3.1 Initial setup** 

### **3.1.1 Connecting a user interface device** 

An external operating device in the form of a PC, laptop, or tablet is required to operate and control the robot. 

### **3.1.2 Hardware recommendation** 

- Commercially available PC, laptop, or tablet 

- Ethernet interface 

- Resolution: minimum 1280x720px, recommended Full HD (1920x1080 px) 

- Multitouch function (if using a tablet) 

- Recommended browsers: Chrome, Edge, Safari, or Firefox 

##### **_NOTICE_** 

Recommended browsers include Chrome, Edge, Safari, or Firefox with recent updates installed. Using outdated browser versions may result in compatibility issues with the system interface. 

##### **_NOTICE_** 

For secure access, browsers must support the TLS protocols defined in Mozilla’s <u>https://wiki.mozilla.org/Security/Server_Side_TLS.</u> 

### **3.1.3 Procedure** 

1. Connect the interface device to the X5 connector on the Arm base via Ethernet cable to open the initial configuration interface. 

**_NOTICE_** 

**_For more information, please refer to chapter 7 section 7.6 Wiring and Electrical Installation in the respective Hardware Manual (i.e. Franka Research 3 Arm v1 or Franka Research 3 Arm v2)._** 

2. Ensure your interface device has DHCP client activated to automatically obtain the IP address. The IP address will be assigned once Franka Research 3 is powered on. 

3. Open your preferred web browser. 

4. Enter the following URL: `robot.franka.de` 

5. Press **Enter**. 

The website showing the Franka UI opens up. 

R02216/1.3/EN 

Franka Robotics GmbH © 

9 

GETTING STARTED 

### **3.1.4 Initial configuration – “First Start”** 

After starting the Control for the first time, basic system settings must be configured. 

This configuration is displayed in the web browser and also appears after resetting the Control to factory settings. 

1. Start Franka Research 3. 

2. Enter the following URL: robot.franka.de 

   - The "First Start" web interface of the Franka UI opens with the language selection of the system interface. 



Figure 1: language selection initial configuration 

3. Click on the area where the IP address of the robot is shown in the menu bar to download the manual. Be sure to read it carefully. 

4. Select the desired language for the Franka UI interface. Click on „NEXT“ 

   - The page for setting the network connection is opened. 



Figure 2: Network 

On this page, the network connections of the internal robot network and those of the Internet connection or connection to a company network can be configured. 

The subaddress of the robot network can be adjusted if required. The default setting is 192.168.0.1, the address range can be used from 100-150. 

R02216/1.3/EN 

Franka Robotics GmbH © 

10 

GETTING STARTED 

For access to the company network or the Internet, the use of the DHCP client can be selected or a manual configuration can be performed. 

The current connection status to Franka World is displayed graphically. 

5. Confirm the settings by clicking on **NEXT** 

   - The web interface for configuring / managing the robot with Franka World opens. 



Figure 3: Franka World registration 

This page is used to register the robot in Franka World and to manage updates and Apps. 

When the Control is connected to the Internet, the robot is automatically registered in Franka World and checked for the availability of the latest system updates or application software (Apps). 

The configuration of the robot is done in Franka World. You can open Franka World by clicking on the link. 

A Franka World account is required for installing system updates and Apps refer to Chapter 7.1, Managing apps and updates. 

6. Click on „Download“ to transfer any available changes. 

If an internet connection cannot be established, you can also update the device "offline <mark>".</mark> **_<mark>For more information, please refer to chapter 7 section 7.4 Updates in this Manual.</mark>_** After the data has been transferred, confirmation is required to complete the installation. To do this, click on "Apply". 

A restart will be initiated in case of system-relevant changes. The first-start procedure is then restarted, but your previous settings are stored. In this case, confirm all previous steps with "Next". 

After all available changes have been installed in the Franka World step, you can proceed to the next step by clicking "Next". 



**_For information about system updates und Apps, see chapter 8.3 “Managing Apps and “._** 

- The web interface for creating the administrator is opened. 

R02216/1.3/EN 

Franka Robotics GmbH © 

11 

GETTING STARTED 



Figure 4: Creating Administrator 

7. Create an initial user of type “Administrator” 

<mark>This user can continue the configuration later and create additional system users.</mark> **_<mark>For more information on roles, please refer to the section "Assigning an administrator" in Chapter 7.2.4.1 in this Manual.</mark>_** 

8. Confirm the input by clicking on „Next“. 

   - The web interface for configuring the end effector is opened. 



Figure 5: End effector settings 



##### **Unexpected motions during guiding due to incorrectly configured end effectors** 

Incorrectly configured end effector mass and inertia may lead to not entirely compensated gravitational forces. The resulting and unexpected behavior of the robot including end effector may lead to injuries such as crushing, tearing of the skin, and puncturing. 

- Always check the configuration of the end effector. 

R02216/1.3/EN 

Franka Robotics GmbH © 

12 

GETTING STARTED 

- When copying an already parametrized App or Task to another Franka Research 3 system, ensure that the end effector configuration remains identical to the original one. 



##### **CAUTION** 

**Falling objects from end effectors during initial installation** 

   - Objects falling from the gripper lead to injuries to hands, fingers, feet, and toes. 

   - Always wear personal protective equipment (e.g., safety shoes). 

   - Use the appropriate type of grippers to prevent objects from falling. 

   - Consider the shape, texture, and weight of the grasped objects in the risk assessment according to 10218-2. Using lightweight and/or round objects may reduce risks significantly. 

   - Do not place your hands between grasped and solid objects (e.g., table). 

   - Do not load the end effector before start-up, since depending on the installed end effector, the 'homing' motions may be executed automatically upon restoration of power. 

9. Configure which end effector is used on the robot. 

If you do not have an end effector mounted, select **None** from the drop-down menu. . 

If you have mounted Franka Hand as an end effector, select **Hand** from the drop-down menu. 

**_NOTICE_** 

Franka Hand is not part of the certified robot. 

If you want to use another end effector or adjust the configuration of the Hand, select “User Defined” from the dropdown and enter the corresponding values into the text fields. The appropriate values are usually found in the end effector’s manual. 

**_NOTICE_** You will be able to reedit the end effector settings later on. 

10. Confirm the entries by clicking on "Confirm". The initial configuration is thus completed and confirmed, and a final preparation step is performed. 

   - The programming interface DESK is displayed in the web browser and the status display on the Arm lights up permanently in blue. 

### **3.1.5 Initial Sync During First Start** 

##### **Preconditions** 

- The robot is powered on and in _First Start_ mode. 

- A network connection has been configured (online or offline). 

- The user has a valid _Franka World_ account and login credentials. 

R02216/1.3/EN 

Franka Robotics GmbH © 

13 

GETTING STARTED 

During the first start of the robot, it must perform an initial synchronization with Franka World to verify registration and account assignment. 

##### **Procedure** 

1. **Online Scenario** 

   - Ensure the robot has an active internet connection. 

   - The robot automatically performs synchronization through the _Desk_ interface. 

   - This works only if the robot has already been pre-registered and assigned to a Franka World account (handled by manufacturer/company). 

**_NOTICE_** 

If the robot cannot connect to the platform even though it’s online, the customer should contact Support. 

2. **Offline Scenario** 

   - If the robot operates without internet access, the customer needs to: 

      1. Open the link shown on the robot in _Desk_ . 

      2. Download the sync file from the Franka World platform. 

   - **Prerequisites:** 

      - The user must have a Franka World account. 

      - The user must be logged in. 

      - The user must be invited to the same account as the robot. 

After successful synchronization, the robot is linked to its assigned _Franka World_ account and can access available updates and applications as described in **_<mark>Chapter 8  Managing Apps and Updates in this Manual.</mark>_** 

## **3.2 Unexpected motions during guiding** 

Incorrectly configured end effector mass/inertia may lead to unexpected robot behavior and injuries. 

- Always check end effector configuration. 

- Ensure configuration consistency when copying Apps/Tasks between systems. 

## **3.3 Falling objects during installation** 

Objects falling from the gripper may cause injuries. 

- Wear personal protective equipment (e.g., safety shoes). 

- Use appropriate grippers. 

- Consider object shape, texture, and weight in risk assessment. 

- Avoid placing hands between grasped and solid objects. 

- Do not load the end effector before start-up. 

## **3.4 End effector configuration** 

- If no end effector is mounted, select **None**. 

- If Franka Hand is mounted, select **Hand**. 

- For other end effectors, select **User Defined** and enter values from the manual. 

R02216/1.3/EN 

Franka Robotics GmbH © 

14 

TYPICAL USAGES 

##### **_NOTICE_** 

- Franka Hand is not part of the certified robot. 

- • You can re-edit end effector settings later. 

# **4 TYPICAL USAGES** 

After switching on the robot, the **Franka UI** must be accessed via: 

- The previously assigned IP address, or 

- robot.franka.de (if the operating device is connected to the **X5 – Robot network** on the robot base) 

Franka Research 3 can be controlled in two different ways: 

##### **1. Control via Apps in Franka UI** 

You can control and program the robot using **Apps** directly in the open **Franka UI** . 

**_<mark>For further explanations and operating instructions, please refer to Chapter 6 “Franka UI” in this Manual.</mark>_** 

##### **2. Control via Franka Control Interface (FCI)** 

To control the robot using the **Franka Control Interface (FCI)** : 

1. Open **Desk** in the Franka UI. 

2. Expand the **System** menu in the header. 

3. Change the operation mode to **Execution** . 

4. Press the **Activate FCI** button to enable the FCI interface. 

Once activated, you can control the robot via: 

- Linux terminal using **libfranka** 

- **ROS** , **ROS 2** , or **MATLAB** interfaces 

##### **_NOTICE_** 

Network Requirements for FCI Mode 

- The robot must be connected to the operating device via the **C2 – Shop Floor network** on the front of the Control unit. 

- A **stable and fast network connection** is required. 

- **FCI mode cannot be used** when the robot is connected via the **X5 – Robot network** on the robot foot. 

R02216/1.3/EN 

Franka Robotics GmbH © 

15 

WORKING WITH FRANKA RESEARCH 3 

# **5 WORKING WITH FRANKA RESEARCH 3** 

## **5.1 Robotic basics** 

##### **Joint space** 

In joint space, a robot pose is described using the rotation angles of each of the robot's joints. In contrast to most industrial robots, which have six joints, Franka Research 3 has seven joints. This allows for extremely high flexibility. A linear movement of the end effector on the robot through space results from the superimposed interaction of the rotation of several joints. 

##### **Cartesian space** 

In Cartesian space, a robot pose is not described by the rotation angles of the individual robot joints but is specified with relation to the reference coordinate system (world coordinate system of the robot or tool coordinate system). Here, the position and orientation of the end effector are the focus. The three-dimensional space representation of a Cartesian pose usually consists of three values of lengths (in meters) for determining the position and three values (in degrees) for the orientation of the end effector. 

Movements in Cartesian space allow the precise tracking of predefined paths in space, such as straight lines. The changing of position is called translation, while the changing of orientation is called rotation. The Cartesian motion of a robot always depends on the reference coordinate system, which can be configured for Franka Research 3 via the configuration of the end effector in the administration’s settings of Franka UI. 

##### **Redundancy** 

As Franka Research 3 has seven joints, the Arm can reach a certain Cartesian pose with various joint configurations. This capability is called redundancy. The part of the robot that can still be moved while keeping the end effector pose the same is often called 'elbow' because it matches the motion capability of the elbow in a human arm. The redundancy of the Arm allows for greater flexibility when teaching or executing tasks, e.g., using it to circumnavigate an obstacle to grip an object located behind it. The behaviour of the robot’s elbow can be changed and adapted to each situation. It can be set to freely movable or immovable. 

##### **Sensitivity** 

The Arm has torque sensors in all seven joints. The torque sensors enable, among other things, to recognize and react to even the smallest forces acting on the Arm. This sensitivity facilitates numerous functionalities and capabilities, such as impedance or sensitive collision detection. For achieving maximum sensitivity, the robot system must be adapted in the best possible way to the additional masses attached to and picked up by the robot. For this reason, the end effector must be configured as precisely as possible in the Franka UI settings. 

##### **Impedance** 

Impedance is a robot's behaviour that imitates the ability of a mechanical spring. An impedance-controlled robot can interact gently with the environment, e.g., to not damage fragile objects. The ability to change impedance can be seen as similar to that of a human arm, which tenses the muscles to change rigidity and can adapt depending on the situation to increase robustness when executing a task. 

##### **Collision detection and reaction** 

Torque sensors have been incorporated into all seven axes. These provide information on the currently applied torques per axis at any given time. In combination with our model-based Control of Franka Research 3, contact forces and torques of the joints can be precisely determined. Then, the Arm can respond. For example, if the Arm touches an unexpected object while moving, this contact is detected in real time by one or more torque sensors and classified as a collision. This can then be used, for example, to stop the movement of the robot. 

R02216/1.3/EN 

Franka Robotics GmbH © 

16 

WORKING WITH FRANKA RESEARCH 3 

**_NOTICE_** 

The robot’s reaction to collisions depends on the users programming and is not a safety feature. 

##### **Generating forces** 

The Arm is in intended contact with its surroundings. With the help of the torque sensor signals, a defined force on the point of contact can be generated by the motors. To achieve this, suitable apps or programming are required. 

**_NOTICE_** External wiring adds additional loads and torques to the Arm which may influence the Franka Research 3‘s control performance. 

## **5.2 Single point of control (SPoC)** 

Franka Research 3 provides ****Single Point of Control (SPoC)**** functionality to comply with safety and regulatory standards. 

This ensures that only one user at a time can trigger critical actions such as: 

- Editing system settings and tasks 

- Unlocking joints 

- Running tasks 

The user in control is assigned the ****SPoC software token**** . 

- SPoC also applies to ****Fieldbus interfaces*** 

**_NOTICE_** 

Even without the SPoC token, it is still possible to trigger uncritical actions like stopping a running Task or locking the robot brakes. 

### **5.2.1 Take control** 

When connecting to the robot with an available token, take control by accepting the dialog displayed after login. The token is now assigned to you. Other users cannot control the robot without your consent. 

### **5.2.2 Request control** 

When connecting to the robot with a token already taken by another user, request control by accepting the dialog displayed after login. The controlling user will be shown a control request dialog on the screen. The token is reassigned to the requesting user if the controlling user grants access. If the controlling user denies access, the token will remain with the controlling user. 

##### **_NOTICE_** 

For improved traceability, it is recommended to set up named profiles for each user in the system settings. That way, the system is able to inform newly connected users about who is currently controlling the robot. 

A user requests control: 

R02216/1.3/EN 

Franka Robotics GmbH © 

17 

WORKING WITH FRANKA RESEARCH 3 





Figure 7: User management waiting for approval 

The user who has the SPoC token receives the control request: 



Figure 8: User request 

R02216/1.3/EN 

Franka Robotics GmbH © 

18 

WORKING WITH FRANKA RESEARCH 3 

### **5.2.3 Enforce control** 

It is possible to enforce control if the user has physical access to the robot. Instead of requesting control, the user chooses to enforce control in the dialog displayed after login. After choosing enforced control, the requesting user has a time window in which he can press the blue circle on the robot’s Pilot to take control. The controlling user is notified about the enforcement attempt during this time frame. The controlling user is then able to confirm or deny control. 

**_NOTICE_** 

Adjust the time window for control enforcement in the system settings. By default, the time window is set to 30 seconds. 

New user enforces control: 



Figure 9: Enforce control 

### **5.2.4 Release control** 

After the controlling user has finished working with the robot, the controlling user can release control in the robot menu. This will lock access to the controlling user and release the token. Other users can now connect to the robot and take control directly. Control is also released if the controlling user logs out. 

### **5.2.5 Fieldbus control** 

It is also possible to control the robot through Fieldbus interfaces. Single-Point-of-Control also applies to Fieldbus interfaces. The required functionalities are provided for the supported Fieldbus protocols but must be considered during connection implementation. Data access and uncritical actions are possible via Fieldbuses regardless of the token status. 

Franka Research 3 implements OPC UA server functionality. 

**_NOTICE_** 

All Fieldbuses have the same rights as the operator role. 

R02216/1.3/EN 

Franka Robotics GmbH © 

19 

WORKING WITH FRANKA RESEARCH 3 

##### **_NOTICE_** 

If the robot is controlled via a Fieldbus protocol, there is no request procedure for other users trying to take control via Franka UI. When a Franka UI user takes control, the token is automatically reassigned from the Fieldbus protocol towards the user. 



For more information on how to use Modbus and OPC UA, see the respective manual at Franka World. 

## **5.3 Operating modes** 



Figure 10: Overview operating modes 

Franka Research 3 offers the following operating modes: 

1. Programming 

   - Idle (default) 

   - Teach a Task (Enabling Button, Guiding Button) 

   - Test & Jog (External Enabling Device, Hold-to-run button in Desk) 

2. Execution 

   - Work (default) 

R02216/1.3/EN 

Franka Robotics GmbH © 

20 

WORKING WITH FRANKA RESEARCH 3 

- Monitored stop 

- Assist (Enabling Button, Guiding Button) 

##### **Switching** 

Switch between the general "Programming" and "Execution" modes using the toggle button in the Desk sidebar. Certain user interactions select all other modes implicitly within the general modes, e.g., pressing the External Enabling Device in "Programming." 

The general operating modes can also be switched via Fieldbus control. 

### **5.3.1 Programming** 

Programming mode is an operating mode in which the robot can be programmed to execute certain Tasks. 

Controlling the robot via FCI is not possible in "Programming" mode. 

#### **Teach a task (guiding enabling device** ) 

The administrator teaches the robot by parameterizing the Task and its Apps. This is done by hand-guiding the robot with the Enabling and Guiding Buttons at the Pilot-Grip. 

#### **Test & jog (external enabling device)** 

The administrator tests and monitors the execution while standing back from the robot. The External Enabling Device connected to the robot via the dedicated X4 port is used. 

#### **Typical procedure for programming** 

Proceed as follows when programming with the Franka Research 3: 



Figure 11: Procedure 

|1|Teach a Task|3|Run a Task|
|---|---|---|---|
|2|Test & Jog|||



#### **Teach a Task (1)** 

Teach Franka Research 3 a Task. 

#### **Test & Jog (2)** 

Step out of the maximum workspace and check whether the taught Task is correctly executed. For this, the velocity can be limited, and the execution can be stopped at any time. 

R02216/1.3/EN 

Franka Robotics GmbH © 

21 

WORKING WITH FRANKA RESEARCH 3 

#### **Run a Task (3)** 

Once the Task has been taught, Franka Research 3 executes the Task automatically. 

### **5.3.2 Jogging in joint space** 

Jogging is available in the sidebar. You can move each axis one by one individually. To utilize jogging, the system requires an attached X4 – enabling device. 

1. Select “Prog” in the mode selector switch on the far-right side in sidebar 

2. Select the jogging workflow by clicking on “Jog” 

The jogging workflow is now open and will guide you through the following steps. 

3. If not already done, unlock the joints by switching the Joints Lock toggle to Unlocked and confirming the modal dialog. 

4. Press and hold the X4 – enabling device 

5. While holding X4 – enabling device pressed, you can jog the robot by clicking on the + and – buttons. 



##### **WARNING** 

With this functionality you can move the robot into self-collisions and joint limits. Only use the functionality when you have a clear view of the robot. 

#### **Jogging in ‘’Test and Jog’’** 

Jogging is enabled when the system is in Test and Jog. Use jogging to: 

- Move the robot joint wise when you want to change the robot's position without using Apps or FCI 

- Move the robot out of soft joint limits 



Figure 12: Jogging 

R02216/1.3/EN 

Franka Robotics GmbH © 

22 

WORKING WITH FRANKA RESEARCH 3 



##### **WARNING** 

With this functionality you can move the robot into self-collisions and joint limits. Only use the functionality when you have a clear view of the robot. 

#### **Using the jogging preview** 

The jogging workflow also allows us to see which joint will be moved with a preview. 

1. Select “Prog” in the mode selector switch on the far-right side in sidebar 

2. Select the jogging workflow by clicking on “Jog” 

The jogging workflow is now open and will guide you through the following steps. 

3. You can drag the dots on each axis to see how the robot will move 

4. The 3d visualization will update accordingly, moving the joint and highlighting it. 

5. When releasing the dot, it will jump back to its current position. 



Figure 13: Jogging preview 

R02216/1.3/EN 

Franka Robotics GmbH © 

23 

WORKING WITH FRANKA RESEARCH 3 



Figure 14:Test view 

### **5.3.3 Execution** 

Execution mode is an operating mode in which the robot executes the tasks previously taught via the Franka UI or can be moved via the Franka Control Interface. 

##### **5.3.3.1 Work** 

In Work mode, automatic execution of Tasks without the requirement of safe External Enabling Devices is activated. 

In Work mode, the robot executes its task autonomously. Compared to Test & Jog, there is no External Enabling Device as a safeguard, i.e., the operator needs to be safely separated from dangers presented by the Arm (acc. to EN ISO 10218-1:2011 and ISO 10218-2). 



Figure 15: Area assignment 

|1|Maximum workspace|3<br>Perimeter safeguarding|
|---|---|---|
|2|Safeguarded space||



Precondition 

R02216/1.3/EN 

Franka Robotics GmbH © 

24 

WORKING WITH FRANKA RESEARCH 3 

- A Task has been created in Teach a Task 

- The Task has been successfully tested in Test & Jog. 

- The safety system is running without violations and errors. 

##### **_NOTICE_** 

Always evaluate the remote start of the execution and realize the safety concept within the safety design (e.g., external safety means) and the safety settings of the robotic system. 



Figure 16: Work operation 

##### **_NOTICE_** 

Noise levels during operation < 70 dB (A) 

##### **Procedure** 

   1. Switch to the “Execution” operating mode 

   2. Press the Play Button in Desk. 

- _A confirmation dialog is shown._ 

   3. Confirm the dialog. 

- _The robot executes the learned task._ 

##### **_NOTICE_** 

If a collision occurs, the execution is stopped. The failed App is highlighted, and an error description is displayed. In this mode, the Arm can be moved using guiding and any causes of error can be eliminated. 

R02216/1.3/EN 

Franka Robotics GmbH © 

25 

WORKING WITH FRANKA RESEARCH 3 

##### **_NOTICE_** 

Any error message is displayed in the sidebar. There, information on the error and how to eliminate it can be viewed. 

1. To continue with the execution, press the Play button for one of the Apps. 

2. To end the Task, press the Stop button. 

##### **_NOTICE_** 

The remote execution start must be evaluated during the realization of the specific cell safety concept. 

**Requirements for using the Franka Control Interface (FCI)** 

- FCI-Mode is activated **_<mark>(Please refer to Chapter 4 Typical Usages in this Manual.)</mark>_** 

- A network connection exists <mark>with the Linux workstation.</mark> 

- The safety system operates without violations and errors. 

- Brakes are open. 

- The control system is in Execution mode. 

##### **_NOTICE_** 

In the event of an error during control via FCI, the current operation is aborted and the resulting error is transmitted via the FCI. In Franka UI an error message is shown. 

The user's program must now be designed so that the errors are automatically transmitted as output. 

##### **5.3.3.2 Monitored stop** 

The robot is at a supervised standstill. This mode is present in the following cases: 

A safety sensor connected to a safe input configured in a dedicated safety rule using the SMSS safety function detects the presence of a human. 

A transition mode to offer Assist mode to the user. 

##### **5.3.3.3 Assist** 

This mode can be used during execution if hand-guiding is part of the application. This mode is only permitted within the collaboration space defined. 

R02216/1.3/EN 

Franka Robotics GmbH © 

26 

WORKING WITH FRANKA RESEARCH 3 



Figure 17: Assist operation 



##### **Hot Surfaces and Guiding** 

At ambient temperatures above 30 °C the robot surface can become too hot to touch. Therefore, using the Assist feature in Execution mode is not permitted above 30 °C 

The Assist mode is a state of the Execution operating mode. This mode enables collaborative operation with manual guidance in accordance with ISO 10218-1. In order for it to be usable, this mode must be explicitly enabled by a safety operator in Watchman. 

If the robot is placed in Save Monitored Standstill (SMSS) during the execution of a task, the robot automatically switches to Assist Mode when the Enable and Manual Guidance buttons are pressed. This state is displayed in the robot's status message in DESK. 



Figure 18: Indication of Assist Mode 

In this mode, the operator can move the robot in manual control by pressing the Enabling Button on the robot's Pilot-Grip. 

R02216/1.3/EN 

Franka Robotics GmbH © 

27 

WORKING WITH FRANKA RESEARCH 3 



Figure 19: Conditions for motion enabling in Assist Mode 



##### **WARNING** 

##### **Hot Surfaces and Guiding** 

At ambient temperatures above 30 °C the robot surface can become too hot to touch. Therefore, using the assist feature in automatic mode is not permitted above 30 °C. 

If the Safely Monitored StandStill condition (SMSS) is removed again, the robot resumes execution of the stopped task and moves to the next pose. 

When using the Franka Control Interface (FCI), an error message is issued by the SMSS and the execution of the robot movement is stopped. The cancellation of the SMSS does not automatically lead to a restart of the robot. This must be restarted via the command input. 

##### **Condition for initiating Assist Mode:** 

- Activated Assist-Mode in the Safety Settings in Watchman. This activation can only be done by a safety operator. 

- The robot must be in Safe Monitored StandStill (SMSS). For this purpose, a rule must be created in the Work Scenario in Watchman that brings the robot into the safe monitored state (Safe Monitored Stand Still). The trigger for this rule can be the processing of a safe input signal (X3.2 or X3.3) or the entry into a defined safe space. It is recommended to initiate the triggering of the safe monitored standstill by a safe input signal. 

- Press the Enabling Button and the Guiding Button. 

**Options for movements in Assist Mode:** 

- By pressing the Enabling and Guiding Buttons on the Pilot Grip, the robot can be moved freely in Hand Guiding mode. 

- Movements of the mounted end effector are not enabled in Assist mode. 

##### **Exiting the Assist Mode:** 

The Assist mode automatically stopped when the Enabling Button or the Guiding Button is released. 

R02216/1.3/EN 

Franka Robotics GmbH © 

28 

WORKING WITH FRANKA RESEARCH 3 



##### **CAUTION** 

If the Safe Monitored StandStill (SMSS) is triggered by a monitored space, the robot immediately moves to the next pose when the Enabling or the Guiding Button is released outside the monitored space. Therefore, plan a safe input (X3.2 or X3.3) for the use of the Assist Mode to initiate the Safe Monitored StandStill (SMSS). 

## **5.4 Apps** 

Apps incorporate the entire complexity of the Franka Research 3 system and represent modular building blocks of a process such as grasping, plugging, insertion, and screwing. Using Desk, Apps can be arranged to create entire Tasks in no time. The created Tasks can quickly be adapted, reused, or deployed on multiple robots to reduce set-up costs remarkably. Individual Apps and Tasks can be parameterized by teaching Franka Research 3 poses by demonstration or adding context-relevant parameters such as speed, duration, forces, and triggering actions. 



Visit our Store on <u>https://franka.world to browse our continuously growing portfolio of Apps and solutions.</u> 

## **5.5 Creating a Task** 



##### **WARNING** 

**Risk of injuries during guiding** 

Risk of tearing the skin or puncturing during guiding. 

- Do not have sharp edges in the maximum workspace. 

- Do not keep any pointed objects in the maximum workspace. 

- **_For more information, refer to Chapter 7.9 “Practical Tips for Usage and Positioning of Franka Research 3” in the respective Hardware Manual i.e. Franka Research 3 Arm v1 or Franka Research 3 Arm v2)._** 

##### **_NOTICE_** 

Before executing any Task with Franka Research 3, **_make sure to read chapter ‘’3.1” in this Manual._** 

##### **Procedure** 

1. To create and select a new Task, click on the “+”-symbol in Tasks and assign a name. 

A new Task is created with an empty Timeline. 

2. Drag and drop the respective Apps from Apps to Timeline to program an individual Task. Alternatively, double click on the respective Apps to add it to the timeline. 

3. Arrange them in the desired sequence by dragging and dropping the Apps. The programmed Tasks are executed from left to right. 

4. To remove Apps from a Task, drag and drop the respective Apps from Timeline to Apps. 

R02216/1.3/EN 

Franka Robotics GmbH © 

29 

WORKING WITH FRANKA RESEARCH 3 

Alternatively, right-click on the App to open a drop-down menu from which you can activate, deactivate, or delete individual Apps. 

5. To change Task-level settings, e.g., the execution speed, click on the Task name in Timeline. 

## **5.6 Task settings** 

##### **Procedure** 

1. Click on the Task’s name in the top left corner of Desk. 

2. Set the parameters for robot speed, compliance/stiffness, and sensitivity thresholds. 

**_NOTICE_** 

Navigation and parameterization can also be done via buttons on the Pilot. 

## **5.7 Parameterization of Apps** 



**WARNING** 

**Falling objects from end effectors during initial installation** 

- Objects falling from the gripper lead to injuries to hands, fingers, feet, and toes. 

- Always wear personal protective equipment (e.g., safety shoes). 

- Use the appropriate type of grippers to prevent objects from falling. 

- Consider the shape, texture, and weight of the grasped objects in the risk assessment according to 102182. Using lightweight and/or round objects may reduce risks significantly. 

- Do not place your hands between grasped objects and solid objects (e.g., table). 

- Do not load the end effector before start-up, as “homing” might happen after each time brakes are unlocked upon power-up. 

After the administrator creates a Task and adds at least one App, the App parameters can be configured. 

##### **Precondition** 

- A Task has been created and selected to be shown in the Timeline. 

- An App has been added to the Task. 

##### **Procedure** 

_1._ To open an App in the created Task, click on it. 

   - _A corresponding context menu appears to set the parameters._ 

2. Follow the instructions in the App context menu to teach or parameterize poses. 

3. Hand-guide the robot to the desired pose. 

4. Press the Teach button on the Pilot-Disc to confirm the pose. 

For further information on guiding, **_<mark>see section Guiding configuration in chapter 5.10 later in this Chapter</mark>_** <mark>.</mark> The context menus of the Apps vary and contain one or more steps for entering parameters, e.g., teaching poses or entering execution speed. 

R02216/1.3/EN 

Franka Robotics GmbH © 

30 

WORKING WITH FRANKA RESEARCH 3 

Only activated Apps are executed and need to be taught. 



Figure 20: App parameterization 

**_NOTICE_** 

The Pilot (buttons) can also be used for navigation and parameterization. 

## **5.8 Pose teaching** 



##### **CAUTION** 

**Unexpected movement of Arm** 

Incorrect set mass and center of gravity values may lead to injuries, such as crushing. 

- Check the mass and center of gravity for any end effector and the objects grasped by it. 

- Correct the values if necessary. 

##### **Precondition** 

An App with pose parameters has been added to the Task. 

Procedure 

1. Open App by clicking on it. 

R02216/1.3/EN 

Franka Robotics GmbH © 

31 

WORKING WITH FRANKA RESEARCH 3 



Figure 21: App interface 

2. Click on necessary Step in the App 

##### **_<mark>Guide to the Arm as described later in chapter 5.12 Guiding.</mark>_** 

3. Stop guiding the Arm. 

4. Release the buttons when the correct pose is reached. 

5. Confirm the pose by pressing the Teach button. 

Teaching a pose in the App is now finalized. 

## **5.9 Pose fine adjustment** 

##### **Procedure** 

_1._ Click the App in which you want to adjust the pose. The context menu appears. 

_2._ Right-click on the pose you want to adjust in the context menu. 

3. Adjust the Cartesian pose of the end effector translationally and/or rotationally via the plus/minus keys (2) in single steps. When you have adjusted the pose, you can move the Arm to the readjusted pose via the "HOLD TO MOVE" (3) button. 

The "TAKE LIVE POS" (4) button can be used to adopt the pose previously achieved by manual guidance and the "TAKE STORED POSE" (5) button can be used to adopt the pose currently stored in the Control as the current configuration. 

4. To save the pose, click on „SAVE“ (1). 

_The pose is adjusted._ 

R02216/1.3/EN 

Franka Robotics GmbH © 

32 

WORKING WITH FRANKA RESEARCH 3 



Figure 22: Pose fine adjustment 

## **5.10 Guiding configurations** 

In Guiding mode, the motion of the Arm follows the corresponding guiding configuration, which is displayed in the sidebar. The guiding configuration can be changed by pressing the Guiding-Mode Button on top of the Pilot-Grip. The desired configuration can also be selected from the sidebar. The following configurations can be selected: 

- **Translation** 

The Arm can only be moved to change the Cartesian position of the end effector. Its orientation remains as it was before entering the Guiding mode. 

- **Rotation** 

The Arm can only be moved to change the Cartesian orientation of the end effector. Its position remains as it was before entering the Guiding mode. The reference coordinate system for this rotation is the predefined coordinate system of the end effector. 

- **Free** 

The Arm can be moved freely. All seven joints can be moved. 

- **User** 

The user can define the guiding behavior for each Cartesian translation and rotation axis. The elbow can be movable or fixed. 

R02216/1.3/EN 

Franka Robotics GmbH © 

33 

WORKING WITH FRANKA RESEARCH 3 



Figure 23: Overview of switching between Hand-Guiding-Modes 



Figure 24: Illustration of Hand Guiding 

If “User mode” is selected, the user can select constraints for guiding: 



Figure 25: Settings, if “User mode” is selected 

## **5.11 Necessary guiding components** 

To guide the Arm, use the Pilot. 

**_NOTICE_** Operate Desk directly via the touchscreen or using your mouse/keyboard. 

R02216/1.3/EN 

Franka Robotics GmbH © 

34 

WORKING WITH FRANKA RESEARCH 3 

##### **_NOTICE_** 

The motion speed in Teach or Hand Guiding-Mode is pre-set. In the settings of Watchman, the speed can be reduced according to the risk evaluation of the Arm within its application. 

##### **Safety instruction** 

##### **Precondition** 

1. The Control must be switched on and booted up. 

2. All external devices connected to X3 must be allowed to move. 

3. Emergency stop is released. 

##### **Procedure** 

- Leave the maximum workspace and make sure that no other people are within the maximum workspace. 

- On Desk, click on “Unlock joints”. 

_Each of the seven axes makes a small movement and seven clicking noises can be heard._ 

_The Arm is now in idle mode or monitored stop._ 

Step back into the maximum workspace to start the guiding. 



**_For more information on the Pilot, refer to Chapter 5.1 the Arm in the respective Hardware Manual (i.e. Franka Research 3 Arm v1 or Franka Research 3 Arm v2)._** 

## **5.12 Guiding** 



##### **CAUTION** 

**Unexpected movement of Arm** 

- Incorrect set mass and center of gravity values may lead to injuries, such as crushing. 

- Check the mass and center of gravity for any end effector and the objects grasped by it. 

- Correct the values if necessary. 

##### **Procedure** 

1. Press the Guiding Button and half-press the Enabling Button. 

##### _Guiding is now enabled._ 

_The status indicator on the base of the robot turns white._ 

2. Guide the Arm by hand. 

3. Stopp the Hand-Guiding of the Arm. 

4. Release the keys when the correct pose is reached. 

5. Confirm the Pose by pressing the Teach Button. 

Teaching a pose in the app is now completed _._ 

R02216/1.3/EN 

Franka Robotics GmbH © 

35 

WORKING WITH FRANKA RESEARCH 3 



Figure 26: Hand guide approval 



Do not use the external Enabling Button to guide the robot as it will lead to an error. 



Do not guide the Arm when locked. 

**_NOTICE_** 

The vibration transmitted during hand-guiding is below 2.5 m/s². It was tested according to the test methods defined in DIN EN 1032:2009-02. 

## **5.13 Editing end effector settings** 

A correct configuration is essential for operating Franka Research 3. When configuration is incorrectly, gravitational forces are not entirely compensated, and the Arm controls to the wrong target values. 

##### **Procedure** 

1. Go to Franka UI. 

2. Click on Settings. 

_3._ Select the end effector sub-menu. 

_The input mask opens._ 

4. Enter the respective technical data, e.g., mass or mass inertia matrix. 

In case of incorrect configuration, the following behavior might occur: 

- The Arm may pull in certain directions in guiding mode. 

- The control in operating mode may be affected so that the expected sensitivity of the Arm for collision detection is reduced. 

- The tracking behavior may be affected. 

R02216/1.3/EN 

Franka Robotics GmbH © 

36 

WORKING WITH FRANKA RESEARCH 3 

As soon as the Task is taught and the correct end effector settings are set, switch to Test & Jog to test the Task at a reasonable execution speed. Make sure that there are no collisions and that everything works fine while being able to stop at any time by releasing the External Enabling Device. 

##### **Initiating motion** 

An optional countdown for Task execution can be configured and edited in Settings. 

When starting a Task in either Test & Jog or Work mode, the countdown is displayed before executing the Task. During the countdown, the LEDs on the robot base will indicate the started Task by fast-flashing in green. 

##### **_NOTICE_** 

After a system reboot, the control token is being reset. 

**_NOTICE_** 

Adjust the waiting time in the system settings. By default, the waiting time is set to 0 seconds. 



Figure 27: Test & Jog 

##### **Testing** 

##### **Precondition** 

- The robot has learned a Task. 

- The External Enabling Device must be connected to X4. 

- The operator must have left the maximum workspace. 

- The operator must check that all other persons have left the safety zone. 

- The operator must direct his full attention to the pending robotic motion. 

##### **Procedure** 

To enable the robot, press the button on the External Enabling Device.Optional: Select an appropriate execution speed in the “Operation” section of the sidebar. _Default speed is 0.25m/s_ 

Press and hold the Test&Jog play button in the “Operation” section of the sidebar. 

Task execution will be terminated if either the Play button or the External Enabling Device is released. 

R02216/1.3/EN 

Franka Robotics GmbH © 

37 

FRANKA UI 

If a countdown for Task execution has been configured, a confirmation dialog is shown as well. During the countdown, the execution can still be cancelled. Robot lights are flashing green quickly during the countdown. 

If the robot executes the task as intended, **_<mark>go back to Section 5.6 Task settings in this Manual.</mark>_** 

If adjustments need to be made, **_<mark>go back to Section 5.3.2.1 Work in this Manual</mark>_** <mark>.</mark> 

**_NOTICE_** 

The system monitors the connection of the Franka UI hold-to-run control with a maximum timeout of 1 s. If a connection loss is detected while a hold-to-run control is pressed, the system is stopped. 

# **6 FRANKA UI** 

Franka UI is the user interface of the robots from Franka Robotics. 

- It can be used to program and operate the robot in Desk. 

- General settings can be made via Settings and the necessary safety adjustments are configured via Watchman. 

- Franka UI is always reachable via the URL https://robot.franka.de if the user terminal is connected to X5 - robot network at the robot base and the DHCP client is activated. 

## **6.1 Login** 

After entering the URL https://robot.franka.de the login to the user interface appears. 



Figure 28: Franka UI 

### **6.1.1 Elements** 

##### **1. Language selection** 

Click to select the languages available for the user interface. 

R02216/1.3/EN 

Franka Robotics GmbH © 

38 

FRANKA UI 

##### **2. System menu** 

Display of the current IP address of the robot and the registered name of the robot in Franka World. 

Clicking opens a menu with the following selection: 

- Link to Franka World, with indication whether the robot is connected to Franka World (green or red dot). 

- Reboot, reboot the robot. 

- Shut Down Button, to shut down the robot. 

- Reboot into Rescue System 

- Manuals Button, clicking on it opens a download page of the Control with the possibility to open the user manual in all available languages. 



Figure 29: Download User Manual 

##### **3. Login** 

Input field for login; after a user log in, the view of DESK appears. 

**4. Watchman** 

Direct access to the Watchman user interface in viewing mode. 

**5. Download log** 

Button for downloading the log files of the Robot. 

## **6.2 Desk** 

### **6.2.1 Overview** 

Desk is the user interface in Franka UI for programming, configuring and operating the robot. To open Desk, enter the following URL in the browser: https://robot.franka.de and log in. 

In Desk, you can create Tasks. Tasks are chronological sequences of Apps. Apps, in turn, are the building blocks of a Task and outline the basic abilities of Franka Research 3, e.g. "Grasp", "Put down" or "Press button". 

R02216/1.3/EN 

Franka Robotics GmbH © 

39 

FRANKA UI 



Figure 30:Desk 

### **6.2.2 Elements** 

|1|Quick Navigation|5<br>Timeline|
|---|---|---|
|2|Language selection|6<br>Tasks|
|3|System Menu|7<br>Apps|
|4|User Menu|8<br>Sidebar|



- 1 **Quick Navigation** 

To switch quickly between the displays of Desk, Watchman and Settings. 

- 2 **Language Selection** 

Click to select the languages available for the user interface. 

- 3 **System Menu** 

Display of the current IP address of the robot and the registered name of the robot in Franka World. 

Clicking opens the system menu with the following selection: 

- <u>Link to Franka World; with indication whether the robot is connected to Franka World (green or red dot).</u> 

- <u>Reboot Button; to reboot the Robot.</u> 

- <u>Shut Down Button, to shut down the robot.</u> 

- <u>Reboot into Rescue System: to boot into the Rescue system</u> 

- <u>Activate FCI Button, click on the activate button and confirm.</u> 

- <u>Manuals Button: Clicking on it opens a download page of the Control with the possibility to open the user</u> manual in all available languages. 

R02216/1.3/EN 

Franka Robotics GmbH © 

40 

FRANKA UI 

##### 4 **User Menu** 

The login information displays the currently logged in user and their role. Clicking this button opens the User menu with the following selection: 

- <u>Release Control; Handing over control of the robot.</u> 

- <u>Log Out, Logout of the current user from the user interface.</u> 

- 5 **Timeline** 

Arrange your apps in the timeline to program your task. The timeline represents the chronological sequence of a task. 

##### 6 **Tasks** 

All configured tasks of the robot are listed in the "Tasks" area. Here you can access existing tasks and manage the tasks. You can also create, download, clone, rename, or delete tasks. Import a Task by dragging and dropping a Task file downloaded from the current or another robot into the Tasks area. 

Tasks from an older generation of robot systems from Franka Robotics are not supported by Franka Research 3. 

**_NOTICE_** 

Make sure you always back up system logs, security logs, and created tasks. 

##### 7 **Apps** 

All installed apps from Franka World can be viewed here. The apps from this section of Desk can be used directly in the Tasks section. Drag and drop the desired apps into the timeline to use and configure them. 

##### 8 **Sidebar** 

The sidebar provides controls for certain workflows including a general toggle for the operation mode. For programming workflows select Mode “PROG”. Then you can choose between Teach, Test and Jog. ‘’Teach’’ allows you to teach the robot and change the hand guiding modes. ‘’Test’’ is for testing your tasks and Jog allows jogging in joint space ( **_See chapter 5 section 5.3.2)._** 

By selecting Mode “EXEC”, you activate execution mode, which enables the start of Tasks. 

When an Arm is attached, the 3D visualization at the top always shows the live robot in real time. The visualization can also be enlarged using the zoom in/out button in the top-right corner of the view, allowing for a larger and 

R02216/1.3/EN 

Franka Robotics GmbH © 

41 

FRANKA UI 

more detailed display of the robot system next to the sidebar. 



Figure 31: Sidebar 

## **6.3 Watchman** 

With the Watchman web application, only a “Safety Operator” user can edit, validate, and integrate safety settings. However, any user is authorized to view the current safety settings in Watchman. 

To view the current safety settings in Watchman, click "WATCHMAN" in the top menu bar or go to https://robot.franka.de/watchman in the browser. 



Figure 32: Watchman 

The detailed description of the interface as well as the procedure for configuring the safety settings of the robot can be found in Chapter Safety Functions. 

R02216/1.3/EN 

Franka Robotics GmbH © 

42 

FRANKA UI 

## **6.4 Settings Interface** 

Various functions for configuring the robot are available to administrators in the Settings interface. 



Figure 33: Menu Settings 

### **6.4.1 Elements** 

|1|System Overview (Dashboard)|6|Modbus TCP|
|---|---|---|---|
|2|Network Settings|7|System|
|3|User Management|8|Franka World|
|4|End Effector|9|Safety|
|5|Calibration|||



- **1 Dashboard (Overview of the system status)** 

   - System information about the control 

   - System information about the Arm 

   - Network information of the connected networks 

- **2 Management of network configurations** 

   - Address configuration of the X5 robot network 

   - Configuration of the company network C2 

- **3 User management** 

   - Creating, editing and removing users 

- **4 Configuration of the end effectors** 

   - Activating the power supply of the end effector 

R02216/1.3/EN 

Franka Robotics GmbH © 

43 

FRANKA UI 

- Selection of the end effector 

- Configuration of the end effector parameters 

##### **5 Calibration** 

   - Execute calibration routine 

   - Joint torque calibration 

- **6 Modbus Configuration** 

      - Download Modbus Manual 

      - Activating the Modbus function 

      - Upload and download the Modbus configuration 

- **7 System** 

      - Downloading of System-logs 

      - Reset to factory settings 

      - Move to pack pose 

- **8 Franka World Synchronisation** 

      - Installation of Apps und Features 

      - Software-Updates with Franka World 

- **9 Safety** 

      - Downloading of Safety logs 

      - Configuration the delay for movement initiation 

      - Configuration of SPoC-Token-forced timeout 

##### **_NOTICE_** 

The only change in this version is the sidebar UI in Settings (updated to version 5.9). All other interfaces, including Settings pages, Dashboard, and workflows, remain the same as in version 5.8. Images and instructions from 5.8 can still be used, except where the sidebar is shown. 

R02216/1.3/EN 

Franka Robotics GmbH © 

44 

ROLES AND PERSONNEL 

# **7 ROLES AND PERSONNEL** 

## **7.1 Personnel** 

### **7.1.1 Responsible person** 

The responsible person is responsible for compliance with occupational health regulations and the operational safety ordinance. The responsible person for Franka Research 3 can be in particular the entrepreneur, the director of the institute, the employer, or a delegate responsible for the use of Franka Research 3. 

The responsible person is responsible for the following: 

- The responsible person must fulfil the monitoring obligations. 

- The responsible person must ensure that all staff members working with Franka Research 3 are suitably qualified to do so and have been informed about the possible dangers Franka Research 3 may present. 

- The responsible person must provide training and instructions in given intervals to create and consolidate risk awareness. 

### **7.1.2 User** 

Users of the system are the people who are directly involved in the operation of the system. The operation of the system is divided into different tasks that cover the different operating phases of the system: 

- Administrative tasks 

- Safety related tasks 

- Operation of the system 

According to the assigned tasks, users must have qualified knowledge of the subject area of the task, safety instructions and training on the robot system. The required qualifications are described below in the description of the user roles. 

### **7.1.3 Integrator** 

The integrator is responsible for assembling the partly completed machinery into the final machinery by combining the robot with other equipment or another machine, including other robots, to form a machine system. 

The integrator also conducts an appropriate risk assessment to identify residual risks and eliminate or minimize them. 

The integrator is responsible for the safety of the final application. 

**_<mark>For more information, please refer to chapter 4 section 4.2 Notice of liability in the respective Hardware Manual (i.e.</mark> Franka Research 3 Arm v1 or Franka Research 3 Arm v2)._** 

##### **_NOTICE_** 

Only qualified or sufficiently trained personnel that possess adequate technical skills are permitted to operate the robot. The qualification of said personnel includes but is not limited to professional technical education, a university degree in engineering, or professional experience in the field of robotics or automation. Franka Robotics suggests a product specific training performed by Franka Robotics, partners, and affiliates. 

R02216/1.3/EN 

Franka Robotics GmbH © 

45 

ROLES AND PERSONNEL 

## **7.2 User Roles** 

### **7.2.1 Operator** 

An operator can access Franka Research 3 and utilize Franka UI to use Franka Research 3 within the limits defined by the responsible person, the administrator, and the safety operator. The operator can utilize the user interface Franka UI as follows: 

- Start, monitor, and stop the intended operation of Franka Research 3 

- Download and select Tasks 

- View Tasks and App settings 

- View status of the system (network, robot, end effector) 

- View safety settings 

- Lock/unlock joints 

- Start/stop a task 

- Guiding (no saving of poses possible) 

- Switchover Pilot-Mode 

- Move to transport pose for packing 

- Download log files from the system 

- Shutdown and reboot the system 

The operator only has limited access to Franka UI. 

### **7.2.2 Administrator** 

The administrator has all the rights that the operator has. An administrator is a person authorized by the responsible person to set up and access the robotic system and to utilize the user interface Franka UI as follows: 

- User management (create, update and delete users; assign roles and modify passwords) 

- Set and change non-safety-related parameters of the system (e.g., change end effector settings) 

- Program and teach the robot system 

- Install system updates, features, and apps 

- Edit system configuration 

- Create, edit, and set parameters for tasks 

### **7.2.3 Safety operator** 

The safety operator has the same rights as the operator, plus the rights to set up and validate safety settings. The safety operator can utilize Franka UI as follows: 

- Edit safety configurations 

- Program and teach the robot system 

- Create, edit, and set parameters for tasks 

- Recovering of specific Safety errors 

R02216/1.3/EN 

Franka Robotics GmbH © 

46 

MANAGING FRANKA RESEARCH 3 

##### **_NOTICE_** 

User roles should only be assumed by qualified or sufficiently trained personnel. They should be instructed on the conduct in emergency or abnormal situations. The Responsible Person must choose the personnel based on experience, training, or similar existing duties in robotics, automation, Industrial safety and occupational health. 

### **7.2.4 Assigning user roles** 

##### **7.2.4.1 Assign an administrator** 

When logging in for the first time, creating an administrator user is compulsory. 

1. Enter a username. 

2. Enter a password. 

3. Confirm the password. 

Administrator login information should be kept safely and securely. The only way to access the role as administrator without a password is to perform a factory reset that deletes all prior information. 

**_NOTICE_** 

Always use secure passwords to prevent unauthorized persons from accessing the system. 

##### **7.2.4.2 Creating and editing users** 

There must always be at least one user with the Administrator role defined. This means that the last administrator cannot be deleted. Every user must be assigned a role, and several users can have the same role. Franka Research 3 supports the roles described above. 

##### **Procedure** 

**_1._** Log into the Franka UI **_._** **_<mark>For information on Franka UI, see chapter 6 FRANKA UI.</mark>_** 

2. Go to Settings. 

3. Click on the Users tab. 

4. Add new users or edit existing ones. 

# **8 MANAGING FRANKA RESEARCH 3** 

## **8.1 Franka World** 

Franka World is an online platform that interconnects customers, partners, and software and hardware developers, whose activity revolves around Franka Robotics’s products and services. Franka World provides tools for managing Franka Research 3, access to an online store that features a continuously growing portfolio of software and hardware products, and the possibility of becoming part of an active and passionate community. 

Visit https://franka.world/ to make use of all the benefits. 

R02216/1.3/EN 

Franka Robotics GmbH © 

47 

MANAGING FRANKA RESEARCH 3 



Access the Franka World User Manual to get an overview of all Franka World features and how to benefit from them: https://download.franka.de/franka-world-manual/ 

## **8.2 Hub** 

Hub is the central knowledge section within Franka World. It provides access to documentation, tutorials, codes, and updates about our robot of Franka Robotics and its interfaces. Find more information on https://franka.world/. 

## **8.3 Managing Apps and Features** 

Apps and features purchased through the Franka World Store can be accessed and installed on the robot via the "Software Updates’’ tab in the Settings interface. When the robot is online, synchronization between the robot and the Franka World account is simple and fast. However, the operator can also perform the synchronization manually on the same interface, should the robot be offline. Depending on whether the robot is online or offline, the view adjusts automatically. 



Figure 34: Managing Apps and Features via Franka World 

##### **_NOTICE_** 

If required, the operating system will update when new Apps or features need to be installed from Franka World. 

## **8.4 Updates** 

##### **Software updates** 

Updates for the operating system can be downloaded conveniently via the "Software Updates" tab in the Settings view. To do this, the robot must have online access to Franka World. 

The Control regularly checks for available updates to the operating system and displays them in the "Software Updates" tab of the Settings interface. 

If your robot does not have online access to Franka World, you can also start an update manually (offline synchronization). 

R02216/1.3/EN 

Franka Robotics GmbH © 

48 

MANAGING FRANKA RESEARCH 3 



##### **WARNING** 

Downgrading to a version older than the one currently installed on the system will result in a factory reset. 

##### **_NOTICE_** 

If required, the operating system will update when new Apps or features need to be installed from Franka World. 

##### **_NOTICE_** 

- Do not confuse this process with the Initial Sync During First Start described in Chapter 3.1.5. 

   - The Initial Sync links the robot to _Franka World_ (ownership and registration step). 

   - • The Online/Offline Synchronization described here installs software updates after registration is complete. 

##### **Online synchronization** 

1. The software updates page indicates that an update is available. 



Figure 35: Software update 

2. Press "fetch update automatically (recommended)" to download the changes. 

R02216/1.3/EN 

Franka Robotics GmbH © 

49 

MANAGING FRANKA RESEARCH 3 



Figure 36: Fetch update automatically (recommended) 

3. The "APPLY" button becomes available after the changes are downloaded. 



Figure 37: Apply button 

4. A confirmation dialogue appears to apply the changes. 

R02216/1.3/EN 

Franka Robotics GmbH © 

50 

MANAGING FRANKA RESEARCH 3 



Figure 38: Apply and reboot 

5. The system begins applying the changes. 



Figure 39: Applying changes 

6. The system shows "Applying Changes and Rebooting" after applying the changes. 

R02216/1.3/EN 

Franka Robotics GmbH © 

51 

MANAGING FRANKA RESEARCH 3 



Figure 40: Applying changes and rebooting 

7. The application of changes is now complete. 



Figure 41: Rebooting 

##### **Offline synchronization** 

Instructions are shown to synchronize the system after pressing "Synchronize manually". 

1. Press "Next" to proceed. 

R02216/1.3/EN 

Franka Robotics GmbH © 

52 

MANAGING FRANKA RESEARCH 3 



Figure 42: Synchronize manually 

2. Upload the update file. 



Figure 43: Upload update file 

3. Uploading update file. 

R02216/1.3/EN 

Franka Robotics GmbH © 

53 

MANAGING FRANKA RESEARCH 3 



Figure 44: Uploading update file 

4. The upload of the update file is successful. 



Figure 45: Dismiss 

5. Follow the same steps as the online process starting from the "APPLY" button available after downloading changes. 

6. 

##### **_NOTICE_** 

The only change in this version is the sidebar UI in Settings (updated to version 5.9). All other interfaces, including Settings pages, Dashboard, and workflows, remain the same as in version 5.8. Images and instructions from 5.8 can still be used, except where the sidebar is shown. 

## **8.5 Backup** 

A Backup of the Control consists of several relevant categories of Control data. These are usually: 

- Safety Configuration of the system, 

- Network Settings, 

- ModBus-Configuration, 

- End effector configuration, 

R02216/1.3/EN 

Franka Robotics GmbH © 

54 

MANAGING FRANKA RESEARCH 3 

- User configuration, 

- created Tasks. 

With the actual available firmware or previous versions of the Control, a system backup must be performed manually in five individual steps. These steps are: 

- Saving of the Safety Configuration 

- Saving of the network Settings 

- Saving of the ModBus-configuration 

- Saving of the End effector configuration 

- Saving of the created Tasks 

A backup of the User administration is currently not possible. We recommend saving the created users and their configured authorization as a screenshot and saving it as a file with the remaining backup data. With the current firmware, restoring the user administration can only be done by recreating the users. 

Create a backup directory for the backup files on a suitable storage medium connected to your user interface device. The steps required to create the backup data are explained below. 

## **8.6 Backing up and exporting safety configuration** 

The safety configuration can be saved as a backup file in the current firmware. To perform a backup of the created configuration, the report must be opened in Watchman and saved as a PDF in the backup directory or the user can export the safety configuration in Watchman. To do this, proceed according to the following steps: 

- Select Watchman in the Desk menu 

- Click on „Report“in the upper left corner of the Watchman user interface. 

- Save the report as a PDF and place it in the backup directory. 

For the export route in Watchman: 

- Navigate to Watchman 

- On the top right you find the the option to “Export committed settings” 

When those are exported you can re-import them from the same menu. The functions will be imported as drafts and need to be re-validated. 

There are two more parameters of the security configuration to be saved outside of the Watchman interface. To do this, proceed as follows: 

- Select „Settings“in the DESK menu 

- Open the „Safety“tab. 

- Take a screenshot of this view and save it in the backup directory. 

The relevant parameters in this section are: 

- Work Execution Wait Time 

- Token Force Timeout 

In case of a recovery, the parameters and rules must be entered and validated manually in Watchman or in the “Settings/Safety” tab. 

R02216/1.3/EN 

Franka Robotics GmbH © 

55 

MANAGING FRANKA RESEARCH 3 

## **8.7 Network Setting** 

To save the network settings, proceed with the steps below: 

- Open the „Settings“on Desk 

- Select „Network“tab 

- Take a screenshot of this view and save it in the created backup directory. 



Figure 46: Network Settings 

In case of necessary configuration recovery, the parameters listed in the screenshot must be entered manually. 

## **8.8 Modbus Configuration** 

To save the Modbus configuration, proceed with the steps below: 

- Open the „Settings“ on Desk 

- Select the „MODBUS TCP“ tab 

- Clicking on „DOWNLOAD“ saves the Modbus configuration with the following name on the connected user interface device: „ _modbus.json_ “ 

Save the downloaded file in the previously created backup directory. 

Via the "UPLOAD" button you can restore a backup file of the Modbus configuration to the system again. 

## **8.9 End Effector Configuration** 

To save the end effector configuration, proceed with the steps below: 

- Open the „Settings“ on Desk 

- Select the „END_EFFECTOR“ tab 

- Click on the edit symbol next to „Mechanical Data“ 

R02216/1.3/EN 

Franka Robotics GmbH © 

56 

MANAGING FRANKA RESEARCH 3 

- Clicking on „DOWNLOAD“ saves the Modbus configuration with the following name on the connected user interface device: „ _endeffector-config.json_ “ 

Save the downloaded file in the previously created backup directory. 

Via the "UPLOAD" button you can restore a backup file of the End effector configuration to the system again. 

## **8.10 Saving the created Tasks** 

The created Tasks can be downloaded individually in the „DESK“-View. 

To download a Task, proceed with the steps below: 

- Open the „Settings“ on Desk 

- Select the desired Tasks 

- Clicking on the download symbol starts the download process. 

Save all downloaded Tasks to the backup directory. 



Figure 47: Save Tasks 

To Restore a Task, move the downloaded task-file from file directory by dragging and dropping to the Task-List in DESK. 

R02216/1.3/EN 

Franka Robotics GmbH © 

57 

TROUBLESHOOTING 

# **9 TROUBLESHOOTING** 

## **9.1 General use** 

### **9.1.1 Recoverable errors** 

For a list of recoverable safety errors, see 

|**Error**|**Solution**|
|---|---|
|Franka Research 3 indicator is lit white|Possibly one of the two buttons on the Pilot-Grip has not been pressed properly. Release<br>both buttons and half-press the Enabling Button while simultaneously pressing the<br>Guiding Button again.<br>Make sure that you do not completely press down the Enabling Button, otherwise the<br>Arm’s motion is stopped.|
|Franka Research 3 indicator changes to color<br>pink|The system is receiving conflicting enabling signals.<br>Close all inputs before moving the robot again. The opened inputs X3.1 (emergency stop)<br>and X4 (External Enabling Device) are highlighted in pink in Desk.|
|Franka Research 3 indicator is lit or flashes<br>yellow|The system has identified a warning in the system.<br>The system might work with the active warning or not, depending on the type of warning.|
|Franka Research 3 indicator flashes red|An application error or safety violation has occurred.<br>The error or violation must be fixed before the system fail-safe locking system can be<br>released again from Desk.|
|Franka Research 3 indicator is lit red|There is a problem.<br>If this cannot be rectified by restarting the system, please contact a contact partner, a<br>service provider or us directly at: support@franka.de.|



### **9.1.2 Arms pull strongly in one direction during teaching** 

Immediately check the settings for the end effector and make sure that the correct end effector has been selected and configured. Make sure Franka Research 3 is mounted on a plain surface within the permitted tilt tolerance. 

If you connect to a third party or custom-made end effector, ensure that you have compensated it correctly by updating the transformation matrix. To set the correct tool center point, adjust the weight, set the center of mass relative to the flange. 

##### **_NOTICE_** 

- If a third party or custom-made end effector has been installed, check the following: 

1. Update the transformation matrix to set the correct tool center point. 

2. Adjust the weight of the end effector. 

3. Set the center of mass relative to the flange. 

4. Update the inertia matrix. 

If the problem persists, please contact your service partner or customer support at support@franka.de. Do not operate the system until the issue is solved. 

In the case of heavy external cabling, a drift cannot be prevented as that cannot be compensated with Franka Research 3 settings for all poses. 

### **9.1.3 Loud clicking at switch-off** 

The clicking results from the deployment of the fail-safe locking system and is normal. Locking pins are deployed in the joints to lock them mechanically. 

R02216/1.3/EN 

Franka Robotics GmbH © 

58 

TROUBLESHOOTING 

### **9.1.4 Joint limit error** 

In the event of a joint limit error, the joint of the robot was moved out of the permissible movement range. The following error message appears: 



Figure 48: Message “A joint limit has been violated” 

This error can only be corrected by a safety operator. The "START RECOVERY" button appears for logged-in safety operators. 

Clicking on "START RECOVERY" starts the procedure for restoring the joint error. A dialog opens with the display of the affected joint. 



Figure 49: Message with display of the faulty joint 

Now activate the External Enabling Device and click on "Move Joint Out Of Limit". Hold both until the following message appears: 

R02216/1.3/EN 

Franka Robotics GmbH © 

59 

TROUBLESHOOTING 



Figure 50: Confirmation joint is back in the limit 

The joint is now inside the movement limit again. Now click on "CONFIRM" and thereby complete the recovery. 

### **9.1.5 Joint position error** 

**_NOTICE_** 

Reference positions required for recovery using the DeskAPI are documented in the _Hardware M_ anual. These markings differ between Arm v1 and Arm v2, **_so please refer to_** **_<mark>the respective Hardware Manual (i.e. Franka Research 3 Arm v1 or Franka Research 3 Arm v2).</mark>_** 

**_NOTICE_** 

The images shown for the recovery process may differ depending on your installed system image version. Additionally, visuals may vary based on the Arm variant. 

In the presence of a joint position error, the position data of a joint has been lost in the control system. This can be caused, for example, by a power failure with the brakes open. To rectify this error, a procedure is required that enables the position assignment or joint calibration to be restored. This error is indicated by the following message in Desk. 

R02216/1.3/EN 

Franka Robotics GmbH © 

60 

TROUBLESHOOTING 



Figure 51: Message “Joint position error detected” 

This error can only be corrected by a safety operator. The "START RECOVERY" button appears for logged-in safety users. 

After clicking on "START RECOVERY", a message is opened in which the failed joints are displayed. 



Figure 52: Message with display of failed joints 

Click on any joint that has been reported failed. The view for restoring the joint is displayed. 

R02216/1.3/EN 

Franka Robotics GmbH © 

61 

TROUBLESHOOTING 



Figure 53: Joint recovery locked 

Now activate the External Enabling Device and keep it pressed until the recovery of the joint is completed. Click on the unlock icon of the joint. 



When operating the External Enabling Device, make sure that you are outside the hazardous area to check the execution of the recovery from a safe distance. 

Now, the Robot is unlocking this joint. 



Figure 54: Joint recovery ready for movement 

Then click on the "Move Joint To Ref. Position" button and keep it pressed until the reference position is reached on the robot. Alternatively, the "+ / -" keys can also be used to move the robot. 

When the joint has reached the correct position, the following message appears: 

R02216/1.3/EN 

Franka Robotics GmbH © 

62 

TROUBLESHOOTING 



Figure 55: Conformation position reached 

Visually check whether the affected joint has moved to the reference position. If this is not the case, i.e. a joint has not moved to the correct reference position, contact Support. 

When the joint position is in the reference position, you can release the external enabling device again. Now check the box to confirm the correct reference position of the joint and click on the "CONFIRM" button. Now, the joint position is referenced again. 



Figure 56: Confirmed Joint recovery 

Now carry out the procedure described for all other joints that are still indicated as failed. 

If you do not hold the buttons to move, the following message appears: 

R02216/1.3/EN 

Franka Robotics GmbH © 

63 

TROUBLESHOOTING 



Figure 57: Message Button not held 

If you end the procedure before reaching the reference position, the following message appears: 



Figure 58: Message if reference position not reached 

If you are unable to move to a joint position because it cannot be reached due to an interfering contour, you can move other joints of the robot first as required using the "+/-" keys and thus enable the reference positions of the joint to be referenced to be reached. 

When all incorrectly reported joints have been referenced, the restoration of the robot's reference position is complete. Confirm the recovery by clicking "CONFIRM". 

R02216/1.3/EN 

Franka Robotics GmbH © 

64 

TROUBLESHOOTING 



Figure 59: Confirm the complete recovery 

The robot can now be used again. 

##### **_NOTICE_** 

After restoring joint position errors, the system cannot guarantee that previously taught poses are still approached correctly. Therefore, check the poses of your tasks before you start them in Execute. 

If the recovery cannot be completed successfully, the robot hardware may have been damaged or there is a software error. In this case, shut down the system, take the robot out of operation and contact support. 

### **9.1.6 Failed to unlock joints** 

If the joint unlocking process fails, follow the following steps: 

1. Shut down the robot, unplug it from its power source, and remove the connecting cable between the Arm and Control. For information on how to safely shut down Franka Research 3, **_<mark>see section Disconnecting Franka Research 3 from the power chapter 8 ‘’switching off and restarting’’ in the respective Hardware Manual (i.e. Franka Research 3 Arm v1 or Franka Research 3 Arm v2).</mark>_** 

2. Check the pins for potential damage. 

   - If no damage can be observed, carefully but firmly reattach the cable and make sure it sits tight. Power up the robot and try to unlock the joints. 

3. If the issue should persist, contact your service partner or customer support at support@franka.de by providing the serial number of the Arm and the log files of the robot. You can find the log files in Desk – Settings – System – Download log files. 

### **9.1.7 Robot does not finish booting** 

##### **Procedure** 

1. Turn off the Control. 

2. Unplug the system from its power source. 

R02216/1.3/EN 

Franka Robotics GmbH © 

65 

TROUBLESHOOTING 

<mark>For information on how to safely shut down Franka Research 3,</mark> **_<mark>please refer to chapter 8.3 Switching off and restarting section ‘Disconnecting Franka Research 3 from the power supply’’ in the respective Hardware Manual (i.e. Franka Research 3 Arm v1 or Franka Research 3 Arm v2).</mark>_** 

3. Remove the connecting cable between the Arm and Control. 

4. Check the pins for potential damage. 

5. If no damage can be observed, carefully but firmly reattach the cable and make sure it sits tight. 

6. Power up the robot. 

If the issue persists, contact your service partner or support@franka.de by providing the serial number of the Arm. 

### **9.1.8 Desk continuously displays “Shutting down the system”** 

You have shut down the system. As soon as the front fans of the Control have stopped turning, the Control can be turned off using the switch on the rear side. Then the browser window of Desk can be closed. 

### **9.1.9 Robot does not boot after turning on the Control** 

Occurs when the system has been turned off via Desk, but the Control power button was not turned off. Solution: Turn off the Control and wait for 1-2 minutes. Turn on again. Control should now boot. 

### **9.1.10 Restarting after an unexpected stop** 

**_<mark>For restarting after an unexpected stop, refer to chapter 8.3 ‘’Switching off and Restarting’’ in the respective Hardware Manual (i.e. Franka Research 3 Arm v1 or Franka Research 3 Arm v2).</mark>_** 

## **9.2 Troubleshooting while using FCI** 

For errors related to the use of FCI, please refer to the online FCI documentation at https://franka.world/. 

There you will find detailed and updated information on how to fix various error scenarios that may occur. 

R02216/1.3/EN 

Franka Robotics GmbH © 

66 

ADVANCE CONTROL 

# **10 ADVANCE CONTROL** 

## **10.1 Franka Control Interface (FCI)** 

The Franka Control Interface (FCI) allows a fast and direct low-level bidirectional connection to the Arm, Franka Hand and Cobot Pump. It provides the current status of the robot and enables its direct control with an external workstation PC connected via Ethernet. 



Figure 60: Schematic overview FCI 

Using libfranka, our open source C++ FCI client, you can send real-time control values at 1 kHz with 5 different interfaces: 

- Gravity & friction compensated joint level torque commands. 

- Joint position commands 

- Joint velocity commands. 

- Cartesian pose commands. 

- Cartesian velocity commands. 

At the same time, you get access to 1 kHz measurements of: 

- Measured joint data, such as the position, velocity and link side torque sensor signals. 

- Estimation of externally applied torques and forces. 

- Various collision and contact information. 

You also get access to the robot model library which provides: 

- Forward kinematics of all robot joints. 

- Jacobian matrix of all robot joints. 

- Dynamics: inertia matrix, Coriolis and centrifugal vector and gravity vector. 

<mark>In addition, franka_ros and franka_ros2 connects Research robots of Franka Robotics with the entire ROS and ROS2 ecosystem. It integrates libfranka into</mark> <u><mark>ROS Control. Additionally, it includes URDF models and detailed 3D meshes</mark></u> <mark>of our robots and end effectors, which allows visualization (e.g. RViz) and kinematic simulations.</mark> <u><mark>MoveIt! / Movelt!2</mark></u> <mark>integration makes it easy to move the robot and control the gripper, and the provided examples in MoveIt!</mark> <u><mark>/ Movelt!2</mark></u> <mark>show you how to control your robot using ROS.</mark> 

R02216/1.3/EN 

Franka Robotics GmbH © 

67 

ADVANCE CONTROL 



##### **WARNING** 

For System Images <5.10, FCI cannot control the robot while SLP-C is configured. This affects the safety functions that include spatial position monitoring (Inside/Outside Area) and Cartesian velocity monitoring (maximum speed). If these are used in rules in Watchman, control via FCI is not possible. 

##### **_NOTICE_** 

Data is sent over the network with a frequency of 1 kHz. Therefore, a good network connection is required! 

##### **_NOTICE_** 

While the FCI is active you have full, exclusive control of the Arm and Franka Hand. This means that Arm control cannot be performed via Apps and FCI at the same time! 

## **10.2 Working in principle with the FCI interface** 

Controlling the robot via the FCI interface can be realized by using libfranka in the C++ environment. A sound knowledge of Linux environment and C++ programming is recommended for this purpose. Alternatively, the robot can be controlled via the FCI interface by ROS, ROS 2. 

The following section describes the basic procedure for programming with the help of libfranka in the C++ environment. 

##### **Executables** 

Via the libfanka described before in chapter 8.1. executable files (executables) can be created. 

In the "examples" subfolder of libfranka, examples of executables are listed. You can use these as a base to get started easily and create copies from them that are customized according to your requirements. 

Below you will find the source code of the example " _generate_joint_position_motion.cpp_ " from libfranka to explain the structure of a script. 

// Copyright (c) 2017 Franka Robotics GmbH // Use of this source code is governed by the Apache-2.0 license, see LICENSE #include <cmath> #include <iostream> #include <franka/exception.h> #include <franka/robot.h> #include "examples_common.h" /** * @example generate_joint_position_motion.cpp * An example showing how to generate a joint position motion. * * @warning Before executing this example, make sure there is enough space in front of the robot. */ int main(int argc, char** argv) { 

R02216/1.3/EN 

Franka Robotics GmbH © 

68 

ADVANCE CONTROL 

if (argc != 2) { std::cerr << "Usage: " << argv[0] << " <robot-hostname>" << std::endl; return -1; } try { franka::Robot robot(argv[1]); setDefaultBehavior(robot); // First move the robot to a suitable joint configuration std::array<double, 7> q_goal = {{0, -M_PI_4, 0, -3 * M_PI_4, 0, M_PI_2, M_PI_4}}; MotionGenerator motion_generator(0.5, q_goal); std::cout << "WARNING: This example will move the robot! " << "Please make sure to have the user stop button at hand!" << std::endl << "Press Enter to continue..." << std::endl; std::cin.ignore(); robot.control(motion_generator); std::cout << "Finished moving to initial joint configuration." << std::endl; // Set additional parameters always before the control loop, NEVER in the control loop! // Set collision behavior. robot.setCollisionBehavior( {{20.0, 20.0, 18.0, 18.0, 16.0, 14.0, 12.0}}, {{20.0, 20.0, 18.0, 18.0, 16.0, 14.0, 12.0}}, {{20.0, 20.0, 18.0, 18.0, 16.0, 14.0, 12.0}}, {{20.0, 20.0, 18.0, 18.0, 16.0, 14.0, 12.0}}, {{20.0, 20.0, 20.0, 25.0, 25.0, 25.0}}, {{20.0, 20.0, 20.0, 25.0, 25.0, 25.0}}, {{20.0, 20.0, 20.0, 25.0, 25.0, 25.0}}, {{20.0, 20.0, 20.0, 25.0, 25.0, 25.0}}); std::array<double, 7> initial_position; double time = 0.0; robot.control([&initial_position, &time](const franka::RobotState& robot_state, franka::Duration period) -> franka::JointPositions { time += period.toSec(); if (time == 0.0) { initial_position = robot_state.q_d; } double delta_angle = M_PI / 8.0 * (1 - std::cos(M_PI / 2.5 * time)); franka::JointPositions output = {{initial_position[0], initial_position[1], initial_position[2], initial_position[3] + delta_angle, initial_position[4] + delta_angle, initial_position[5], initial_position[6] + delta_angle}}; if (time >= 5.0) { std::cout << std::endl << "Finished motion, shutting down example" << std::endl; return franka::MotionFinished(output); } return output; }); } catch (const franka::Exception& e) { std::cout << e.what() << std::endl; return -1; } return 0; } 

R02216/1.3/EN 

Franka Robotics GmbH © 

69 

ADVANCE CONTROL 

In C++ texts are excluded via the character string "//". These serve e.g. as information of the programmer to the program structure. 

The include command "#include <path-spec>" at the beginning of the script instructs the processor to include the content from the in the path specification at the point where the -statement is displayed. For example, you can use this to access predefined functions from libfranka. 

The line "int main(int argc, char** argv) { }" contains the command line parameters inside the single brackets. Inside the curly braces is the actual main function of the script. The main function is terminated by a closing curly bracket. 

In the main function, various commands can now be executed or calls to included sub-functions can be made. 

As mentioned before, the control of the robot requires a profound knowledge of C++ programming. 

##### **_NOTICE_** 

To intercept the immediate start of the robot's movement, Franka Robotics recommends to create a query procedure at the beginning of a script, which will execute the program only after active confirmation. Such queries can also be found in the sample scripts in libfranka. 

##### **Creating or modifying executables** 

If you want to create your own executables, we recommend that you create your own project. To do this, create your project folder. In this folder you have to create a "CMakeLists.txt". This file should be structured according to the following scheme. 

project( _hello_world_ ) find_package(Franka REQUIRED) add_executable( _hello_world hello_world.cpp_ ) target_link_libraries( _hello_world_ Franka::Franka) 

Store your source code files for your executables (xxxxx.cpp) in your project folder. Add your source codes to the "CMakelists.txt" file accordingly. 

Now create a build folder in your project. And from this folder, run the following command: 

cmake .. 

Your build will now be created according to the CMakeLists.txt. 

Then, to compile, run the following command from your build folder: 

make 

Your project is now successfully compiled. 

##### **Execution of Executables** 

To run executables, you must run them from the build you created for your project. 

An executable is executed by opening a terminal in the build folder of your project where it is stored and executing the following command: 

./name executable <ip roboter> 

Enter the name of the executable and the IP address of the robot. 

R02216/1.3/EN 

Franka Robotics GmbH © 

70 

ADVANCE CONTROL 

The script will now be executed. 



**WARNING** 

The execution of an executable can directly initiate movements of the robot and thus lead to injuries. Before starting an executable, make sure that there are no people in the danger zone of the robot! 

To stop / cancel the execution of an executable, you can press the key combination <CTRL>+<C>. 

## **10.3 Setup of Franka Control Interface (FCI)** 

To operate the robot via the Franka Control Interface (FCI), the FCI-Feature must be installed on your device. If it is already installed on the controller, it will be listed under Franka UI -> Settings -> System -> Installed Features. By default, the FCI feature is automatically installed during initial configuration. If FCI is not already installed, you can install it on Control with your Franka World account. 

To control the robot via the Franka Control Interface (FCI), the operating device must be connected to the C2 – Shop floor network port on controller via an Ethernet cable. 

##### **_NOTICE_** 

Control via FCI is only possible via the C2 – Shop floor network port. The use of the X5 - Robot network port on the robot foot is not suitable for the use of the FCI function. 



Figure 61: Network connection for FCI Usage 

### **10.3.1 Network Configuration for FCI** 

Good network performance is critical for controlling the robot via the FCI interface. It is therefore strongly recommended to use a direct connection between the workstation PC and Control. This section describes how to configure your network for this use case. 

To operate and control the robot via the FCI interface, an external operating device in the form of a PC or laptop with a Linux operating system (e.g. Ubuntu) is recommended. 

Hardware recommendation: 

- Commercially available PC, laptop with Linux 

- Ethernet interface 

- Resolution min. 1280x720px, recommended Full HD (1920x1080 px) 

- Recommended browsers: Chrome or Firefox 

R02216/1.3/EN 

Franka Robotics GmbH © 

71 

ADVANCE CONTROL 

### **10.3.2 Static IP Configuration Example** 

Control and your workstation must be configured to appear on the same network. The simplest way to achieve that is to use static IP addresses. Any two addresses on the same network would work, but the following values will be used for the purpose of this example: 

||**Workstation PC**|**Control**|
|---|---|---|
|Address|172.16.0.1|172.16.0.2|
|Netmask|24|24|



The Control’s address (172.16.0.2) is called <fci-ip> in the following chapters. 

##### **_NOTICE_** 

With this network configuration, Franka UI can be accessed via https://<fci-ip>, although you will see a certificate warning in your browser. 

### **10.3.3 Configuring Control’s Network** 

1. Connect to the **X5 – Robot network port** on the robot base. 

2. Open **Administrator Settings** in Franka UI. 

3. Navigate to **C2 – Shop Floor network** settings. 

4. Deactivate **DHCP Client** . 

5. Enter static IP settings for LAN connection. 

6. Press **Apply** to confirm. 



Figure 62: <mark>Network settings</mark> 

### **10.3.4** **<mark>Configuring the Operating Device (Ubuntu 20.04)</mark>** 

<mark>This section describes how to set up a static IP address on Ubuntu 20.04 using GUI. Follow the official Ubuntu</mark> <u><mark>guide</mark></u> <mark>if you prefer to use the command line.</mark> 

R02216/1.3/EN 

Franka Robotics GmbH © 

72 

ADVANCE CONTROL 

<mark>These steps modify your network settings. Contact your network administrator if you are unsure.</mark> 

##### **<mark>Steps:</mark>** 

- Open the Network Connection widget. 

- Select the wired connection and click Edit. 

- Go to the IPv4 Settings tab. 

- Set the method to Manual. 

- Enter the following values: 



Figure 63: Values 

1. Save changes and close the window. 

2. Select the connection from the drop-down menu to activate it. 



Figure 64: Ubuntu – <mark>setting a static IP</mark> 

##### **_NOTICE_** 

This step will disable DHCP, which means you will no longer obtain an address when connecting to a DHCP server, like the one in Arm’s base (X5 – Robot network). When you no longer use FCI, you can change the method back to _Automatic (DHCP)_ . 

##### **Final Steps** 

- After configuration, you can access Franka UI via https://<fci-ip> in your browser. 

R02216/1.3/EN 

Franka Robotics GmbH © 

73 

ADVANCE CONTROL 

- To verify network quality, perform a communication test for bandwidth, delay, and jitter. 

## **10.4 Setup of libfranka on a Linux workstation** 

Recommended for the setup is an Ubuntu 22.04 Pro version or newer. In this version, Ubuntu already provides the required RT kernel, but it may be chargeable depending on the usage. 

If you are using an Ubuntu version without a provided RT kernel, it must be installed before libfranka is patched. The real-time kernel is used to realize the real-time transmission with 1 kHz of the signals between Control and the operating device. 

The setup of libfranka then requires two steps, which must be performed one after the other. For the execution you need full "admin" rights on your Linux PC. 

Further information can also be found in FCI-Documentation via <u>Franka World.</u> 

##### **Installation PREEMPT_RT Kernel** 

In the first step, if an RT kernel has not yet been installed with the Ubuntu version, a PREEMPT Real-Time kernel must be installed. To do this, create a new folder in your Linux PC's drive and start the terminal from it. 

**_NOTICE_** 

NVIDIA binary drivers are not supported by PREEMPT_RT-kernels. 

To install, proceed now according to the following steps: 

##### **_NOTICE_** 

To avoid typing errors when entering commands, open the online FCI documentation and copy the command lines there, which you can then paste and execute in the terminal. 

- **Download** 

To install the dependencies, enter the following command in the Terminal: 

sudo apt-get install build-essential bc curl ca-certificates gnupg2 libssl-dev lsb-release libelf-dev bison flex dwarves zstd libncurses-dev 

Then you need to decide which kernel version you want to use. Use the following command to find out which version you are currently using. 

uname -r 

<mark>Real-time patches are only available for select kernel versions, see</mark> <u><mark>https://www.kernel.org/pub/linux/kernel/projects/rt/. We recommend choosing the version closest to the</mark></u> <mark>one you currently use.</mark> 

The version tested by Franka Robotics is the 5.9.1 for Ubuntu 20.04, on which the following installation steps are based. 

Use the command lines below to download the source files. 

If you have chosen a different version, change the version number (5.9.1) in the command lines to match the version you have chosen. 

curl -SLO https://www.kernel.org/pub/linux/kernel/v5.x/linux-5.9.1.tar.xz curl -SLO https://www.kernel.org/pub/linux/kernel/v5.x/linux-5.9.1.tar.sign curl -SLO https://www.kernel.org/pub/linux/kernel/projects/rt/5.9/patch-5.9.1-rt20.patch.xz curl -SLO https://www.kernel.org/pub/linux/kernel/projects/rt/5.9/patch-5.9.1-rt20.patch.sign 

R02216/1.3/EN 

Franka Robotics GmbH © 

74 

ADVANCE CONTROL 

Then decompress the downloaded data with the command: 

xz -d *.xz 

##### • **Verification** 

After downloading the dependencies, it is recommended that you check them to see if they have been corrupted or tampered with. The steps recommended for this are taken from the Linux Kernel Archive. 

Use the following commands to check: 

gpg2 --verify linux-*.tar.sign gpg2 --verify patch-*.patch.sign 

If all loaded packages are correct, you will receive a message corresponding to the following example for each command. 

$ gpg2 --verify linux-*.tar.sign gpg: assuming signed data in 'linux-4.14.12.tar' gpg: Signature made Fr 05 Jan 2018 06:49:11 PST using RSA key ID 6092693E gpg: Good signature from "Greg Kroah-Hartman <gregkh@linuxfoundation.org>" [unknown] gpg:                 aka "Greg Kroah-Hartman <gregkh@kernel.org>" [unknown] gpg:                 aka "Greg Kroah-Hartman (Linux kernel stable release signing key) <greg@kroah.com>" [unknown] gpg: WARNING: This key is not certified with a trusted signature! gpg:          There is no indication that the signature belongs to the owner. Primary key fingerprint: 647F 2865 4894 E3BD 4571  99BE 38DB BDC8 6092 693E 

<mark>See</mark> <u><mark>Linux Kernel Archive</mark></u> <mark>for more information about the warning.</mark> 

If the check returns an error, then you will receive a message corresponding to the example below. 

$ gpg2 --verify linux-*.tar.sign gpg: assuming signed data in 'linux-4.14.12.tar' gpg: Signature made Fr 05 Jan 2018 06:49:11 PST using RSA key ID _6092693E_ gpg: Can't check signature: No public key 

In this case, you must download the key from the key server. 

To do this, use the following command for both "*.tar" and "*.patch" and enter the ID specified in the respective error message in the command line. 

gpg2  --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys _6092693E_ 

##### • **Compiling the kernel** 

<mark>Once you are sure the files were downloaded properly, you can extract the source code and apply the patch</mark> . To do this, enter the following commands one after the other: 

tar xf linux-*.tar cd linux-*/ patch -p1 < ../patch-*.patch 

Get the current name of the patch with the command: 

uname -r 

Als nächstes kopieren Sie mit der nachfolgenden Befehlszeile Ihre aktuell gebootete Kernelkonfiguration als Standardkonfiguration für den neuen Real-Time-Kernel. Über „uname -r“ wird automatisch der aktuelle Kernel ausgewählt. 

R02216/1.3/EN 

Franka Robotics GmbH © 

75 

ADVANCE CONTROL 

cp -v /boot/config-$(uname -r) .config 

Now you can use this configuration as the default for configuring the build. To do this, eonter the following cmmands: 

make olddefconfig <mark>make menuconfig</mark> 

The second command opens a terminal interface (TUI) where you can configure the preemption model. 



Figure 65: TUI-Interface 

- Navigate with the up/down keys to "General Setup" > **"Preemption Model"** and mark there > **"Fully Preemptible Kernel (Real-Time)"** By using the side arrow keys you can move the cursor to Select in the command line at the bottom of the screen. Now press <Enter> and the selection is chosen _._ 

- Set the cursor in the command line to <EXIT> and press <Enter> repeatedly until you return to the main menu. 

- Now navigate to **"Cryptographic API"** > **"Certificates for signature checking"** (at the very bottom of the list) > **"Provide system-wide ring of trusted keys"** . 

- There, select **"Additional X.509 keys for default system keyring"** and press Enter. An input window opens. Remove the entry **"debian/canonical-certs.pem"** from the prompt and press Ok. 

- Now navigate to " **Cryptographic API"** > **"Certificates for signature checking"** (at the very bottom of the list) > **"Provide system-wide ring of revocation certificates"** . 

- There select **"X.509 Certfifcates tob e preloaded into the system blacklist keyring"** and press Enter. An input window opens. There remove the entry **"debian/canonical-revoked-certs.pem"** from the prompt and press Ok. 

- Save this now the configuration in .config and exit the terminal interface (TUI). 

Now the installation is ready for the kernel to be compiled. Since this is a lengthy process, the "nproc" command automatically uses the multithreading option "-j" on the command line to use the maximum number of cores on your CPU. Nevertheless, this step takes longer time. 

make -j$(nproc) deb-pkg 

Now you can install the newly created package with the following command. The exact names depend on your environment. The command searches for the header and images packages. 

sudo dpkg -i ../linux-headers-*.deb ../linux-image-*.deb 

- **Verifing the new kernel** 

R02216/1.3/EN 

Franka Robotics GmbH © 

76 

ADVANCE CONTROL 

Restart your system. The grub boot menu should now allow you to choose your newly installed kernel. To see which kernel will be used after the boot, look at the output of the following command: 

uname -a 

It should contain the string PREEMPT_RT and the version number you chose. Additionally, /sys/kernel/realtime should exist and contain the the number „1“. 

**_NOTICE_** 

   - If you encounter errors that you fail to boot the new kernel see „Cannot boot realtime kernel <u>because of Invalid Signature".</u> 

   - If you want to re-do the build, then delete all the unzipped data from your installation folder beforehand. 

- **Allow a user to set real-time permissions for this process** 

<mark>After the</mark> PREEMPT_RT-Kernel <mark>is installed and running, add a group named</mark> _<mark>realtime</mark>_ <mark>and add the user controlling your robot to this group.</mark> 

You can get your user name from the command line: 

whoami sudo addgroup realtime sudo usermod -a -G realtime $(whoami) 

Then open the "limits.conf" file with the following command: 

sudo gedit /etc/security/limits.conf 

Then add the following real-time group limits to the file and save them. 

@realtime soft rtprio 99 @realtime soft priority 99 @realtime soft memlock 102400 @realtime hard rtprio 99 @realtime hard priority 99 @realtime hard memlock 102400 

<mark>The limits will be applied after you log out and in again</mark> . 

##### **Installation Libfranka** 

The next step describes how to install libfranka from source files. Alternatively, libfranka can be installed by ROSrepos (<Ubuntu 22.04) or ROS2-repos (Ubuntu 22.04 and later). 

You can also find further assistance in the FCI-Dokumentation on <u>Franka World.</u> 

**_NOTICE_** 

To avoid typing errors when entering commands, open the online FCI documentation and copy the command lines there, which you can then paste and execute in the terminal. 

R02216/1.3/EN 

Franka Robotics GmbH © 

77 

ADVANCE CONTROL 

<mark>Before building the new libfranka from source, please uninstall existing installations of l</mark> ibfranka <mark>and f</mark> ranka_ros <mark>to avoid conflicts.</mark> 

To do this, run the following command in the terminal: 

sudo apt remove "*libfranka*" 

- **Download** 

To install libfranka, the dependencies must be downloaded. To do this, enter the following command line: 

sudo apt install build-essential cmake git libpoco-dev libeigen3-dev 

Then download the source code by cloning libfranka from GitHub and then change to the directory. To do this, use the following commands: 

git clone --recursive https://github.com/frankarobotics/libfranka --branch 0.10.0 cd libfranka 

- **Install** 

Then, the following commands create a build folder in the current directory and run the "CMake" command to create the build / project files. 

mkdir build cd build cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTS=OFF .. cmake –-build . 

It is recommended to install the optional libfranka Debian package. To do this, enter the following command in the same directory that creates the "libfranka-<version>-<architecture>.deb" package. 

cpack -G DEB 

This is then installed by the following command. 

sudo dpkg -i libfranka*.deb 

The libfranka is now installed on your PC and can be used to control the robot via FCI. 

## **10.5 Verification of communication** 

After the successful compilation / installation of libfranka, a test of the communication of the interface is recommended. To do this, make sure that the robot is prepared for FCI use in Desk and run the example "echo_robot_state" from libfranka. 

Change to the build directory of libfranka and execute the following on Linux: 

_./examples/echo_robot_state <fci-ip>_ 

The program will display the current state of the robot on the console and will exit automatically after a few iterations. 

R02216/1.3/EN 

Franka Robotics GmbH © 

78 

Safety Concept 

{ **"O_T_EE"** : [0.998578,0.0328747,-0.0417381,0,0.0335224,-0.999317,0.0149157,0,-0.04122, -0.016294,             -0.999017,0,0.305468,-0.00814133,0.483198,1], **"O_T_EE_d"** : [0.998582,0.0329548,-0.041575,0,0.0336027,-0.999313,0.0149824,0,-0.0410535, -0.0163585,-0.999023,0,0.305444,-0.00810967,0.483251,1], **"F_T_EE"** : [0.7071,-0.7071,0,0,0.7071,0.7071,0,0,0,0,1,0,0,0,0.1034,1], **"EE_T_K"** : [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1], **"m_ee"** : 0.73, **"F_x_Cee"** : [-0.01,0,0.03], **"I_ee"** : [0.001,0,0,0,0.0025,0,0,0,0.0017], **"m_load"** : 0, **"F_x_Cload"** : [0,0,0], **"I_load"** : [0,0,0,0,0,0,0,0,0], **"m_total"** : 0.73, **"F_x_Ctotal"** : [-0.01,0,0.03], **"I_total"** : [0.001,0,0,0,0.0025,0,0,0,0.0017], **"elbow"** : [-0.0207622,-1], **"elbow_d"** : [-0.0206678,-1], **"tau_J"** : [-0.00359774,-5.08582,0.105732,21.8135,0.63253,2.18121,-0.0481953], **"tau_J_d"** : [0,0,0,0,0,0,0], **"dtau_J"** : [-54.0161,-18.9808,-64.6899,-64.2609,14.1561,28.5654,-11.1858], **"q"** : [0.0167305,-0.762614,-0.0207622,-2.34352,-0.0305686,1.53975,0.753872], **"dq"** : [0.00785939,0.00189343,0.00932415,0.0135431,-0.00220327,-0.00492024,0.00213604], **"q_d"** : [0.0167347,-0.762775,-0.0206678,-2.34352,-0.0305677,1.53975,0.753862], **"dq_d"** : [0,0,0,0,0,0,0], **"joint_contact"** : [0,0,0,0,0,0,0], **"cartesian_contact"** : [0,0,0,0,0,0], **"joint_collision"** : [0,0,0,0,0,0,0], **"cartesian_collision"** : [0,0,0,0,0,0], **"tau_ext_hat_filtered"** : [0.00187271,-0.700316,0.386035,0.0914781,-0.117258,-0.00667777, -0.0252562], **"O_F_ext_hat_K"** : [-2.06065,0.45889,-0.150951,-0.482791,-1.39347,0.109695], **"K_F_ext_hat_K"** : [-2.03638,-0.529916,0.228266,-0.275938,0.434583,0.0317351], **"theta"** : [0.01673,-0.763341,-0.0207471,-2.34041,-0.0304783,1.54006,0.753865], **"dtheta"** : [0,0,0,0,0,0,0], **"current_errors"** : [], **"last_motion_errors"** : [], **"control_command_success_rate"** : 0, **"robot_mode"** : "Idle", **"time"** : 3781435 } 

Fig. 10.3: Example output of „echo robot state“ 

The respective fields are explained in the libfranka API documentation ( <u><mark>https://frankarobotics.github.io/libfranka.)</mark></u> 

**_NOTICE_** 

If an error occurs at this point, perform the ping test and verify that FCI is enabled and the robot's brakes are open. 

To perform the ping test, enter the following command line: 

_ping <fci-ip>_ 

<mark>If this command fails, the robot is not properly connected to the network, or the IP address was not assigned correctly during the setup phase. Please set up the network again according to the steps described in</mark> **_<mark>chapter 10.3.1 Network configuration for FCI in this manual.</mark>_** 

# **11 SAFETY CONCEPT** 

The safety concept of Franka Research 3 provides a simple approach to making the robotic system safe within its target application. The system provides a set of safety functions compliant with EN ISO 13849-1. For more information on safety functions. 

With the Franka UI tool Watchman, the safety operator can use those safety functions in so-called safety rules and scenarios to cover the risks identified in the risk analysis carried out for the robot cell and application. 

The configuration of the safety system through Watchman is split into two parts: 

R02216/1.3/EN 

Franka Robotics GmbH © 

79 

Safety Concept 

- General safety-relevant settings are configured in the safety setup (e.g., defining the behavior of safe inputs). 

- Safety scenarios allow covering different situations with suitable safety measures. 

Each safety scenario can define one or more safety rules to cover a certain situation/state the robot can be in. 

Each safety rule consists of a safety function, optional selectable conditions (defining when the rule is active), and a reaction triggered when the safety function is violated. 

With the safety setup and the safety scenarios, the safety operator can set up the safety system according to the needs revealed by the risk analysis. Franka Research 3 comes with a predefined and pre-validated set of scenarios. If they are suitable to cover the needs revealed by the risk analysis, this setup can be used out-of-the-box. 

If specific safety rules and scenarios are required, the safety operator can adjust predefined scenarios and rules using Watchman. Some safety scenarios are read-only or contain fixed rules to ensure a minimum set of safety measures common to most applications. In general, these presets are defined by ISO 10218-1. 

The safety operator must validate all customized safety settings and scenarios before confirming and activating them on the robot. 

The predefined safety scenarios cover the possible operation states of the system. 

##### **_NOTICE_** 

During recovery of violated safety functions, the system switches to the predefined recovery scenario to provide a safe recovery. The original scenario (e.g., Work), in which the violation happened, its rules, and especially the violated safety function, are not active during recovery. The system switches back to the original scenario as soon as the recovery has been completed. The integrator must consider the predefined recovery scenarios when performing the application-specific hazard & risk assessment for completed machinery. 

## **11.1 Safety Functions** 



##### **WARNING** 

**Hot Surfaces and Guiding during Recovery** 

At ambient temperatures above 30 °C the robot surface can become too hot to touch. Therefore, in case of occurence of a safety function violation which requires hand-guiding during recovery, the following must be observed: 

- Recovery may be performed only by personnel specifically trained for this situation. 

- Before recovery, surface temperatures must be evaluated to be within touchable limits. Cooldown times depend on previous operation and ambient temperatures. 

- Wearing heat resistant safety gloves for this procedure is advised. 

##### **_NOTICE_** 

Franka Research 3 distinguishes between two kinds of safety functions: monitoring functions and stopping functions. 

Monitoring functions guarantee that limits are not breached, e.g. speed (SLS-J), position (SLP-C)… 

Stopping functions are triggered upon a monitoring violation or a safety input. It is the Safety Operator’s obligation to consider stopping times and stopping distances when configuring the limits. 

R02216/1.3/EN 

Franka Robotics GmbH © 

80 

Safety Concept 

##### **_NOTICE_** 

Connecting external devices with a separate power supply may jeopardize the system’s safety function if the electrical ratings are not complied with. 

In addition, the voltages in the connected devices must either be SELV or suitably isolated from systemconnected signals. 

##### **Safe inputs** 

|**Name**|**Description**|**Safety Rating**|**Stop Reaction**|
|---|---|---|---|
|X3.1 - Emergency stop|The X3 connector in the robot<br>base provides one safe input to<br>connect an emergency stop.|PL d / Cat.3|Category 1 stop|
|X4 - External Enabling|The X4 connector at the robot<br>base provides one safe input<br>dedicated to a 3-position External<br>Enabling Device.|PL d / Cat.3|Releasing or fully pressing the Enabling Button<br>activates the SMSS safety function. The<br>reaction in case of a violation of SMSS<br>depends on the active safety scenario.|
|Enabling Button|A 3-position Enabling Button is<br>provided near the flange on the<br>Pilot-Grip of the robot.|PL d / Cat.3|Operating mode “Programming”: Category 1<br>stop (see predefined scenario “Idle”)<br>Operating mode “Execution”: Reaction<br>depending on SMSS configuration in scenario<br>“Work.”<br>During safety function violation or error<br>recoveries, fully pressing or releasing the<br>Enabling Button triggers a Category 1 stop.|
|X3.2 - Safe input 1<br>X3.3 - Safe input 2|The X3 connector on the robot<br>base provides two additional safe<br>inputs. The behavior of those two<br>inputs can be configured in the<br>safety setup.|PL d / Cat.3|Depends on the configuration in safety<br>scenarios.|



##### **Monitoring functions** 

|**Name**|**Abbreviation**|**Description**|**Safety**<br>**Rating**|**Recovery in case of violation**<br>**NOTICE: The operator can recover all**<br>**violations.**|
|---|---|---|---|---|
|Safely Limited Cartesian<br>Position|SLP-C|Monitoring of the Cartesian position<br>of certain points on the Arm. The<br>position is checked against user-<br>defined Cartesian area.<br>The following points are monitored:<br>• Flange<br>• Elbow<br>• Wrist<br>• Customer defined tool spheres<br>The monitoring can be configured to<br>signal violation either when one or<br>more points are inside the defined<br>space or when one or more points<br>are outside the defined limits.<br>Parameterization:<br>• End Effector model (up to five<br>spheres)<br>`o`<br>Radius of each sphere<br>`o`<br>Position of each sphere<br>center relative to the flange|PL d /<br>Cat.3|Violated position or orientation limits<br>will be shown in Desk of Franka UI.<br>• Unlock brakes of robot.<br>• Guide robot out of Cartesian<br>position limit. Franka UI shows if<br>position limits are not violated<br>anymore.<br>• Finish recovery by pressing Confirm<br>in Desk.|



R02216/1.3/EN 

Franka Robotics GmbH © 

81 

Safety Concept 

|||Hint: This is a general setting and<br>will affect all safety functions using<br>this tool model.<br>• Monitored Cartesian space (box)<br>• Violation if inside/outside|||
|---|---|---|---|---|
|Safely Limited Cartesian<br>Speed|SLS-C|Monitoring of the Cartesian speed<br>of certain points on the Arm<br>structure. The following points are<br>monitored:<br>• Flange<br>• Elbow<br>• Wrist<br>• Centers of customer-defined tool<br>spheres<br>Parameterization:<br>• Limit for Cartesian speed|PL d /<br>Cat.3|A violation of the speed limit is shown<br>in a dialog in the Franka UI.<br>• Confirm violation by pressing the<br>button in Pop-up message.<br>No further recovery procedure is<br>necessary.|
|Safely Monitored Stand<br>Still|SMSS|Monitoring of the standstill in<br>Cartesian space of certain points on<br>the Arm structure. The following<br>points are monitored:<br>• Flange<br>• Elbow<br>• Wrist<br>• Centers of customer-defined tool<br>spheres<br>The user cannot change the<br>parameters of this safety function.|PL d /<br>Cat.3|A violation dialog is shown in the<br>Franka UI.<br>• Confirm violation by pressing the<br>button.<br>No further recovery procedure is<br>necessary.|
|Safe End Effector Power<br>Off|SEEPO|Safely switch off the power<br>provided to the end effector (48 V<br>power line). The behavior of SEEPO<br>can be configured in the safety<br>setup. E.g., it can be configured that<br>SEEPO switches off the power<br>when an emergency stop is<br>triggered.<br>Parameterization:<br>• General configuration, whether<br>SEEPO is active or not<br>• Switch-off triggers of SEEPO|PL b /<br>Cat. b|The power of the end effector can be<br>switched on again in Settings or the<br>sidebar of Desk.|



##### **Internal monitoring functions (not parametrizable and configurable in safety rules)** 

|**Name**|**Abbreviation**|**Description**|**Safety**<br>**Rating**|**Reaction**|**Recovery in case of violation**<br>**NOTICE: The operator can recover all violations.**|
|---|---|---|---|---|---|
|Safely<br>Limited<br>Position<br>of Joint|SLP-J|Monitoring of the<br>position of each joint in<br>joint space.<br>This safety function is<br>only used internally to<br>protect the joint limits of<br>the Arm, prevent self-<br>collisions and local<br>clamping. It is not<br>available in user-defined<br>scenarios.<br>This is a limiting function.|PL d /<br>Cat.3|-|A dialog within Franka UI informs the user about<br>the violation and allows recovery.<br>• Unlock the joint that shall be moved by clicking<br>the unlock icon in the recovery dialog.<br>• To enable recovery motion, press the External<br>Enabling Device.<br>• Move the joint by pressing the +/- buttons in<br>the recovery dialog.<br>Hint: Joints in a violated state can only be moved<br>away from violated limit. All other joints can be<br>moved in both directions to move the robot into a<br>more convenient pose.|
|Safely<br>Limited<br>Speed of<br>Joint|SLS-J|Monitoring of the speed<br>of a single joint in joint<br>space.<br>This internal safety<br>function is used, e.g., to|PL d,<br>Cat. 3|Cat. 1<br>Stop|A violation dialog is shown in Franka UI.<br>1. Confirm violation by pressing the button.<br>No further recovery procedure is necessary.|



R02216/1.3/EN 

Franka Robotics GmbH © 

82 

Safety Concept 

|||prevent fast motions<br>during joint position<br>recovery.||||
|---|---|---|---|---|---|
|Safely<br>Limited<br>Distance|SLD|SLD monitors a single<br>joint to stay within a<br>permitted position<br>window.<br>This internal safety<br>function is used, e.g., to<br>prevent excessive motion<br>during the brake opening<br>procedure.|PL d,<br>Cat. 3|Cat. 1<br>Stop|A safety error dialog is shown in the Franka UI.<br>1. Acknowledge error by pressing the button.<br>No further recovery procedure is necessary.|



##### **Stopping functions** 

|**Name**|**Description**|**Safety Rating**|
|---|---|---|
|Category 0 stop|The Arm is stopped immediately by removing power from the motors<br>and applying the brakes.|PL d / Cat.3|
|Category 1 stop|The Arm is stopped in a controlled manner using the normal control of<br>the motors until the standstill of each joint. The brakes are applied,<br>and the power is removed from the Motors upon standstill.<br>The Cartesian speed deceleration is monitored.|PL d / Cat.3|
|Category 2 stop|The Arm is stopped in a controlled manner using the normal control of<br>the motors until the standstill of each joint. Upon standstill, the<br>standstill is safely monitored.<br>The Cartesian speed deceleration is monitored.|PL d / Cat.3|



##### **Safe outputs** 

|**Name**|**Description**|**Safety Rating**|
|---|---|---|
|Safe End Effector<br>Power Off|Switch the power provided to the end effector (48 V power line) off.|PL b / Cat.b|



##### **Further safety ratings** 

- The 3-stage Enabling Button near the robot's flange is realized in compliance with IEC 60204-1:2016 and IEC 60947-5-8:2006. 

- The 3-stage External Enabling Device provided by Franka Robotics is realized in compliance with IEC 60204-1:2016 and IEC 60947-5-8. 

- The Emergency Stop provided by Franka Robotics complies with IEC 60204-1:2016 and EN ISO 13850:2015. 

## **11.2 Other safety-related recoveries (in case of safety errors)** 

##### **Joint position error recovery** 

- Only Safety Operators can recover joint position errors. 

- A dialog in Franka UI informs the user about the error and allows recovery. 

- Detailed instructions on how to correct the error can be found in **_<mark>Chapter 9 Troubleshooting in this Manual.</mark>_** 

##### **Safe input error recovery** 

Safe input errors are recoverable by confirming the respective dialog in Franka UI if confirmation for those inputs is configured in Watchman. 

R02216/1.3/EN 

Franka Robotics GmbH © 

83 

SAFETY RULES AND SCENARIOS/WATCHMAN 

##### **Other safety errors** 

Other safety errors are typically not recoverable. Please try to restart the system to recover from such errors. If the error persists, contact your vendor or Franka Robotics. 

**General info for all cases** 

- In case of a safety violation, the robot does not allow motion until the recovery has been accomplished. 

- In case of a safety violation, the base flashes slowly in red. 

- If necessary, Franka UI will show a recovery wizard to perform the recovery procedure. 

- Only the safety operator can recover joint position errors. 

- The operator can perform all other recoveries. 

**_NOTICE_** 

**Further measures for possible troubleshooting are described in chapter 11 please refe** **<mark>r</mark>** **_<mark>to the respective Hardware Manual (i.e. Franka Research 3 Arm v1 or Franka Research 3 Arm v2).</mark>_** 

# **12 SAFETY RULES AND SCENARIOS/WATCHMAN** 

## **12.1 Watchman** 

Watchman is a tool in the Franka Web User Interface (Franka Web UI) for displaying, creating and editing safety functions also on the Franka Research 3. Safety functions can be defined via rules. These rules can in turn adapt the behavior of the respective scenarios, such as "Teach" and "Work", to the required protective measures from the risk assessment for the two operating states of the robot ("Programming" and "Execution"). 

The safety configuration can only be done by a Safety Operator. The Safety Operator is one of three user roles available on FRANKA RESEARCH 3. The other roles available are Administrator and Operator **_<mark>. Please refer to Chapter 7 Roles and Personnel in this Manual” for more information</mark>_** . A user in the Administrator role can create a Safety Operator role but cannot edit any safety functions himself. Only in the user role Safety Operator can modify settings in Watchman. The Safety Operator is responsible for the correct safety configuration and documentation of the safety functions and should only be performed by qualified personnel. 

### **12.1.1 Overview** 

In Watchman, the security scenarios are displayed via an intuitive graphical interface. 

The structure of the interface is illustrated and described below. 

R02216/1.3/EN 

Franka Robotics GmbH © 

84 

SAFETY RULES AND SCENARIOS/WATCHMAN 



Figure 66: Watchman 

In the header of the Watchman view, you can find the currently valid security configuration report on the right. The button with the three dots on the right allows you to reset the security configuration to factory settings. 

The current validation status of the safety configuration is displayed. Green means validated; orange indicates the need for validations 

Clicking the validation symbol next to the Draft tab displays the checksum of the currently validated safety configuration. 

In the left part of the view, a structural overview is visible, which displays the validation states of the basic safety settings as well as those of the different safety scenarios. 

In the editing area, the basic settings or the rules of the safety scenarios are displayed. 

The security scenarios are divided into editable and non-editable security scenarios. 

<mark>Detailed descriptions of the security scenarios can be found in</mark> **_<mark>Chapter 11.1 Safety Concept in this Manual.</mark>_** 

The editable scenarios are used for the possibility to adapt robot control to the determined safety measures from the previous risk analysis. The following scenarios are available: 

- Work 

- Assist 

- Test & Jog 

- Teach 

For the "Work" and "Assist" scenarios, up to 16 user-made safety rules can be created and configured. In the "Test & Jog" and "Teach" scenarios, only adjustments to the existing rules can be made. 

The factory settings of Franka Research 3 have a predefined and prepared set of scenarios. If these are suitable for the requirements identified in doing the risk analysis, they can be used immediately. 

##### **_NOTICE_** 

By default, the “Work” scenario in Watchman does not contain any rules. To ensure a safe operation also considering the application-specific risk & hazard analysis the empty “Work” scenario is not pre-validated. A safety operator has to setup the system correctly and validate the safety settings. 

R02216/1.3/EN 

Franka Robotics GmbH © 

85 

SAFETY RULES AND SCENARIOS/WATCHMAN 

Non-editable safety scenarios (Read Only Scenarios) are safety functions permanently integrated in the robot Control that ensure safe and standard-compliant operation of the robot and cannot be changed. These are: 

- Idle 

- Opening/Closing Brakes 

- Position Error Recovery 

- Position Function Recovery IDLE 

- Position Function Recovery 

- Joint Limit Recovery 

- Work Invalid 

All recovery scenarios as well as the scenario "Work Invalid" are scenarios that are only activated in the robot state "error/violation". The robot states "error/violation" is caused by violations of the safety scenarios from the robot states "execution" and "programming" or in the presence of a fundamental safety-relevant error. 

The robot state "execution" includes the scenarios "Work", "Assist" and "Opening/Closing brakes". The robot states "programming" includes the scenarios "Idle", "Teach" and "Test and Jog". 

## **12.2 Safety Rules and Scenarios in Watchman** 

With the Franka UI tool Watchman, the safety operator can use those safety functions in so-called safety rules and scenarios to cover the risks identified in the risk analysis carried out for the robot cell and application. 

The configuration of the safety system through Watchman is split into two parts: 

- General safety-relevant settings are configured in the safety setup (e.g., defining the behavior of safe inputs). 

- Safety scenarios allow covering different situations with suitable safety measures. 

Each safety scenario can define one or more safety rules to cover a certain situation/state the robot can be in. 

Each safety rule consists of a safety function, optional selectable conditions (defining when the rule is active), and a reaction triggered when the safety function is violated. 

### **12.2.1 Adjusting predefined scenarios and rules** 

If specific safety rules and scenarios are required, the safety operator can adjust predefined scenarios and rules using Watchman. 

Some safety scenarios are read-only or contain fixed rules to ensure a minimum set of safety measures common to most applications. In general, these presets are defined by ISO 10218-1. 

The safety operator must validate all customized safety settings and scenarios before confirming and activating them on the robot. 

The predefined safety scenarios cover the possible operation states of the system. 

During recovery of violated safety functions, the system switches to the predefined recovery scenario to provide a safe recovery. 

The original scenario (e.g., Work), in which the violation happened, its rules, and especially the violated safety function, are not active during recovery. 

The system switches back to the original scenario as soon as the recovery has been completed. 

The integrator must consider the predefined recovery scenarios when performing the application-specific hazard and risk assessment for completed machinery. 

R02216/1.3/EN 

Franka Robotics GmbH © 

86 

SAFETY RULES AND SCENARIOS/WATCHMAN 

### **12.2.2 Safety Scenarios for states in Programming mode** 

##### **Idle (read-only)** 

- The user might be close to the robot but not interact with it. The robot is at a safely monitored standstill. 

- This is the default state in Programming mode if no other mode is active or if conflicting inputs are present. 

##### **Teach (customizable)** 

- The user can hand-guide the robot. 

- Safe activation signal: Pressing the Enabling Button located on the Pilot-Grip. 

- The safety operator can customize the pre-defined velocity limit. 

##### **Test & Jog (customizable)** 

- The user watches and verifies the execution of a created task and inches the robot via Franka UI. 

- Safe activation signal: External Enabling Device (X4). 

- The safety operator can customize the pre-defined velocity limit. 

##### **Opening/closing brakes (read-only)** 

- Active while the brakes are opened or closed. 

- Extend of motion and speed is safely limited. 

### **12.2.3 Safety Scenarios for states in execution mode** 

##### **Work (customizable)** 

- The robot works independently by executing a task. 

- This scenario is pre-filled with rules activating the safely monitored standstill (SMSS) safety function stopping the robot when the inputs X3.2 or X3.3 are opened. A rule to trigger the “Safely Monitored Standstill” within “Work” to allow a switch to the “Assist” mode must be set. 

- The safety operator can customize all rules within this scenario. 

##### **Assist (customizable)** 

- Collaborative operation “hand-guiding” as defined by ISO 10218-1 while in execution mode. 

- Safe activation signal: Pressing the Enabling Button located on the Pilot-Grip while the robot is in Safely Monitored Standstill. 

- The safety operator can customize the velocity limit for this mode and/or add custom rules. 

##### **Opening/closing brakes (read-only)** 

- Active while the brakes are opened or closed. 

- Extend of motion and speed is safely limited. 

### **12.2.4 Error/Violation states** 

The following states are not active in the normal operation of the robot. They only become active when safety functions in the other states are violated, or safety-relevant errors occur. 

##### **12.2.4.1 Work invalid (read-only)** 

If there is no valid safety scenario available for the Work mode, the “Work invalid” scenario is activated as a backup to prevent the robot from moving. 

R02216/1.3/EN 

Franka Robotics GmbH © 

87 

SAFETY RULES AND SCENARIOS/WATCHMAN 

##### **12.2.4.2 Violation idle (read-only)** 

This state is active after any safety function is violated and the respective reaction has been carried out. 

##### **12.2.4.2 Recovery (position error, joint limit violation, or space violation) (read-only)** 

This state is active while the robot is recovering from a violated safety function or an error. 

Safe activation signal: Depending on the type of violation or error. 



Figure 67: States during normal operation 

Robots must always be surrounded by protective devices that prevent people from entering the hazardous area or, in the case of collaborative robots there are safe-zones that must be initiated and monitored when people are present in the hazardous area. 

After the risk assessment has been carried out, the safety scenarios of the robot must be adapted to the determined necessary safety functions of the worksite in which the robot system is installed. 

The Franka Research 3 is delivered with a predefined and pre-validated set of safety scenarios according to the requirements from the ISO 10218-1 standard. 

If the risk analysis shows that these are sufficient, the Franka Research 3 can be integrated and used in the planned working environment of the robot without further changes to the safety configuration after appropriate electrical integration. However, if the risk analysis shows that additional safety functions are required, these must be implemented in Watchman by means of rules that apply in specific robot states or scenarios. 

### **12.2.5 Editing of the Safety Configuration** 

In order to complete the following steps, a "Safety Operator” user must be logged in. 

Open the Watchman interface via the menu on the sidebar in Franka UI. The active and confirmed rules as well as the validation states of the scenarios are now displayed on the Watchman interface. 

Depending on the kind of the parameter watchman now uses the following precisions for editable parameters: 

- Coordinates (in meters): 4 decimal places 

- Speed (in meters/second): 2 decimal places 

- Orientations (in degrees): 0 decimal places 

R02216/1.3/EN 

Franka Robotics GmbH © 

88 

SAFETY RULES AND SCENARIOS/WATCHMAN 

- Orientations (in radians): 2 decimal places 

- Joint speeds (in radians/second): 2 decimal places 

_For example:_ 



Figure 68: Editable parameters 



Figure 69: Validated rules 

Switch to "Draft" mode and start editing. 

R02216/1.3/EN 

Franka Robotics GmbH © 

89 

SAFETY RULES AND SCENARIOS/WATCHMAN 



Figure 70: Switch to “Draft” mode 

After opening a validated safety concept in "Draft" mode, all validation markers are shown in green. 



Figure 71: Draft Mode 

If changes are now made, the validation markers of the changed safety function and all parameters, rules and scenarios dependent on the change, as well as the overall safety, are shown in orange. Parameters, rules and scenarios that are not affected remain validated and thus green. 

R02216/1.3/EN 

Franka Robotics GmbH © 

90 

SAFETY RULES AND SCENARIOS/WATCHMAN 



Figure 72: Validation markers 

After completing the safety configuration, the overall concept must be validated. 

##### **_<mark>The procedure is described in section 12.11.</mark>_** 

## **12.3 Import/Export of Safety Settings** 

Safety configuration can be exported and imported. Alternatively, a complete backup can be created using the PDF export option. 

The import/export feature allows safety operators to transfer safety settings between systems or create backups. It will allow users to avoid the need to configure settings from scratch, ensures uniform safety settings across multiple systems and provides a way to back up current safety settings for recovery purposes. 



Figure 73: Import/Export settings 

##### **Scenarios for Using This Feature** 

**System Migration** : 

- When moving safety settings to a new system. 

**Backup and Recovery** : 

- For safeguarding settings against data loss. 

**Multiple Systems** : 

R02216/1.3/EN 

Franka Robotics GmbH © 

91 

SAFETY RULES AND SCENARIOS/WATCHMAN 

- Applying the same settings across different systems to maintain consistency. 

##### **Post-Import Actions** 

Safety operators can export the currently committed safety settings into a file that they can download onto their own device. Subsequently, this file can be imported on the same system or on a different system. In both cases, the currently existing drafts are overwritten with the contents of the imported file. 

After importing settings, the safety operator should: 

- Check the new settings to ensure they are correct. 

- The safety operator still needs to commit these drafts before the imported safety settings become active. 

- In case the import was performed on a different system, additionally they also need to be validated before they can be committed. 

##### **_NOTICE_** 

It is crucial to ensure that any important drafts are committed or backed up before proceeding with the import. 

### **12.3.1 Import Procedure** 

##### **1. Open Standard UI:** 

Start by opening the Standard UI Watchman. 



Figure 74: Standard UI Watchman 

##### **2. Access Top Right Menu:** 

Click on the menu located at the top right corner of the interface. 

R02216/1.3/EN 

Franka Robotics GmbH © 

92 

SAFETY RULES AND SCENARIOS/WATCHMAN 



Figure 75: Import settings as drafts 

**3. Select "Import Settings as Drafts":** 

In the top right menu, find and click on the "Import Settings as Drafts" tab. 

**4. File Selection for Import:** 

A prompt will appear asking you to select a file for import. Choose the appropriate file from your system. 



Figure 76: File selection 

**5. Warning Dialog:** 

After selecting the file, a warning dialog will appear. It will inform you that your current drafts will be replaced with the safety settings from the import file. 

R02216/1.3/EN 

Franka Robotics GmbH © 

93 

SAFETY RULES AND SCENARIOS/WATCHMAN 



Figure 77: Warning dialog 

**6. Confirm Import:** 

If you confirm the action, the safety settings will be successfully imported. 

### **12.3.2 Export Procedure** 

To export current committed settings: 

**Steps** : 

1. Navigate to the ‘’Export committed settings’’ section in the Watchman UI. 

2. Select the settings to export. 

3. Download the file. 

**File Format** 

##### **_NOTICE_** 

The only permitted file extension is. fesafety. Manual modification of these files is not allowed. 



Figure 78: Safety settings imported 

##### **7. Error Handling:** 

If there is an error during the import, an error message will appear stating "Safety settings could not be imported." This error typically occurs if the safety rules file has been manipulated. 

R02216/1.3/EN 

Franka Robotics GmbH © 

94 

SAFETY RULES AND SCENARIOS/WATCHMAN 



Figure 79: Error Message 

## **12.4 Safety Setup** 

In the Safety Setup, the higher-level configurable basic settings of the robot are mapped. These include the areas "General Safety Settings", "Safe Input Configuration" and "End Effector Configuration". 

With the safety setup and the safety scenarios, the safety operator can set up the safety system according to the needs revealed by the risk analysis. Franka Research 3 comes with a predefined and prevalidated set of scenarios. If they are suitable to cover the needs revealed by the risk analysis, this setup can be used out-of-the-box. 



Figure 80: Safety Setup 

## **12.5 General Safety Settings** 

To be able to operate the robot in Assist Mode, the "Enable Assist Mode" checkbox must be set. The description of the Assist Mode can be found in **_<mark>Chapter 5 Working with Franka Research 3 section ‘5.3.3.3’in this Manual</mark>_** <mark>.</mark> If this function is deactivated, the Assist function is not available in any other submenus of the robot Control. These function menus are then greyed out. 

This function is activated in the default settings of the robot. 

R02216/1.3/EN 

Franka Robotics GmbH © 

95 

SAFETY RULES AND SCENARIOS/WATCHMAN 

## **12.6 Safe Input Configuration** 

The processing of the safety inputs X3.2 and X3.3 can be configured via the Safe Input Configuration. 

Form information on the assignment of inputs X3.2 and X3.3 **_<mark>please refer to chapter 7 section 7.6 Wiring and Electrical Installation in the respective Hardware Manual (i.e. Franka Research 3 Arm v1 or Franka Research 3 Arm v2).</mark>_** 

With the setting "No confirmation required", the signal is processed directly. The control reacts immediately to the input. 

With the setting "Confirmation required", the signal is processed directly when the contact is opened, but a query message appears on DESK when the input is closed. This message must be confirmed in order to process the input signal internally. 

In the default settings of the robot, the setting "No confirmation required" is preselected. 

## **12.7 End Effector Configuration** 

The safety behavior of the connected end effector is defined via the "End Effector Configuration". The following fields can be set: 

- **<u>Description:</u>** Free editable description of the end effector 

- **<u>SEEPO Behavior:</u>** Determination of when and for which safety shutdowns the end effector is to be switched off. 



Figure 81: End Effector Configuration 

- Safety Error:  => Robot safety fault 

- Safety Error /EM-Stop:=> Robot safety fault or Emergency Stop 

- Safety Error/EM-Stop/Cat. 1 stop: Robot safety fault or Emergency Stop or Category 1 Stop 

- Safety Error/EM-Stop/Cat. 1&2 stop: Robot safety fault or Emergency Stop or Category 1 or 2 Stop 

In the default settings of the Robot is set “Safety Error/EM-Stop/Cat. 1 stop". 

**<u>Power ON Behavior:</u>** Setting when the end effector is to be switched on. 

- **Manual** =>with each switching on, the end effector must be activated manually in DESK. 

- **Automatic** => the end effector will be automatically activated when the joints are unlocking. 

In the default settings of the Robot „Automatic “is preselected. 

R02216/1.3/EN 

Franka Robotics GmbH © 

96 

SAFETY RULES AND SCENARIOS/WATCHMAN 

## **12.8 Creation of spheres for modelling an End effector envelope** 

When an end effector is mounted, the control system needs information on its dimensions in order to be able to monitor the end effector spatially and kinetically. For this purpose, up to five spheres can be created and placed in their size and position so that the totality of the spheres resembles the contour of the end effector. 

For spatial monitoring, the outer shells of the spheres are considered and for velocity monitoring, the centers of the spheres are considered. It should be noticed that spheres placed far from the end effector flange can be very sensitive to velocity monitoring due to the lever consideration. 

When positioning the spheres, ensure that the Franka hand is mounted at a 45° angle to the flange coordinate system. 



Figure 82: Configuration of spheres 

Below, an example of the sphere configuration of the Franka Hand is shown. 

R02216/1.3/EN 

Franka Robotics GmbH © 

97 

SAFETY RULES AND SCENARIOS/WATCHMAN 



Figure 83: Example of spheres for Franka Hand 

If your gripping situation is not covered by the spherical model shown above, it must be adapted. Make sure that contours that could lead to collisions are covered by the sphere model. If you are handling longer objects, the maximum speed of cantilevered objects must also be monitored. To do this, you can place the centers of the spheres at the ends of the object. The maximum speed is monitored in the centers. 



Figure 84: Example of sphere configuration Franka hand with staff 

R02216/1.3/EN 

Franka Robotics GmbH © 

98 

SAFETY RULES AND SCENARIOS/WATCHMAN 

## 12.9 **Creating and editing rules** 

Up to 16 rules can be created in each of the "Work" and "Assist" scenarios. By clicking on "Create Rule" below the last rule displayed, a new rule is inserted. By clicking on the "Delete" symbol within a rule, it can be deleted. 



Figure 85: Editing rules 

## **12.10 Structure of a rule** 

The rule consists of the following components: 



Figure 86: structur of a rule 

- **Name:** Freely editable name of the rule 

- **Activation Condition:** Condition for which the rule is activated. The following selection is possible: 

   - <u>Always</u> the rule is always active 

   - `o` <u>X3.2</u> the rule becomes active, when the two-channel X3.2-Input is opened. 

   - `o` <u>X3.3</u> the rule becomes active, when the two-channel X3.3-Input is opened. 

- **Activation Space:** Spatial area in or outside of which the rule gets active. The following selection is 

      - possible: 

   - <u>Everywhere</u> the rule is active in the whole working area of the robot. 

   - `o` <u>Inside / Outside Area</u> the rule becomes active inside or outside a free definable cuboid space. When defining the space, it is determined whether the rule becomes active inside or outside the space. 

- **Safety Function:** Safety function to be executed when the rule is violated. The following selection 

R02216/1.3/EN 

Franka Robotics GmbH © 

99 

SAFETY RULES AND SCENARIOS/WATCHMAN 

is possible: 

- <u>Always violated</u> no safety function is executed. If "Always violated" is selected, the rule is permanently violated if the rule becomes active. 

- `o` <u>Inside/Outside Area</u> a violation is triggered if the robot is inside or outside a defined space. When defining the space, it is determined whether the violation should take place inside or outside the space. 

- `o` <u>Maximum Speed</u> Within the applicable spatial area of the rule, the maximum speed is monitored. If the speed of the robot exceeds the permitted maximum speed, a monitored reduction to the permitted speed takes place. If the reduction of the speed does not occur as expected, the preselected reaction is executed (Cat. 1 Stop / Cat. 2 Stop). 

- <u>Safe Monitored Stand Still In the applicable spatial area of the rule, the robot is</u> safely monitored for standstill. Any movement leads to violation of the rule. 



##### **WARNING** 

For System Images <5.10, FCI cannot control the robot while SLP-C is configured. This affects the safety functions that include spatial position monitoring (Inside/Outside Area) and Cartesian speed monitoring (maximum speed). If these are integrated into rules in Watchman, control via FCI is not possible. 

- **Reaction:** Reaction of the robot that is executed when the rule is violated. 

   - <u>Cat. 1 Stop</u> Category 1 stop in accordance with EN ISO 13849-1 (controlled stop and shutoff of energy when standstill is reached) 

   - `o` <u>Cat. 2 Stop</u> Category 2 stop according to EN ISO 13849-1 (controlled stop with maintenance of energy) 

The robot Control already takes the rules into account during the execution of the movement and thus always tries to avoid violations. If a violation cannot be prevented, the safety function initiates the safe reaction. 

Functions or parameters that need to be validated are shown in the rule window with the validation symbol. If the rule is validated, this symbol is green. If validation is required, this symbol is orange. 

If "Inside/Outside area" is selected in the "Activation Space" or "Safety Function" field of a rule, this area must be configured by clicking on the "Configure" button that appears. The following view opens. 

R02216/1.3/EN 

Franka Robotics GmbH © 

100 

SAFETY RULES AND SCENARIOS/WATCHMAN 



Figure 87: Configuration of ”Activation Space” 

With the selection field "Type of area" you can determine whether the robot is not allowed to leave the cuboid area (stay inside area) or not allowed to enter the cuboid area (stay outside area). The tool, flange, wrist and elbow are monitored here. 



Figure 88: monitoring 

To define the cuboid area, it’s reference corner must first be determined. To do this, you can guide the TCP of the robot to the reference corner and teach the position values by clicking on "Take from Robot" or enter the position values manually. In case of manual entry, the coordinates are entered in the coordinate system of the robot. The reference corner must be selected in such a way that the opposite corner is created with positive values only. Then the spatial extension must be defined by entering the XYZ values. For this purpose, the space can also be taught by guiding the robot TCP to the opposite corner point. 

With the help of "Orientation", the defined space can also be rotated around the three axes. The pivot point is the set reference corner. 

R02216/1.3/EN 

Franka Robotics GmbH © 

101 

SAFETY RULES AND SCENARIOS/WATCHMAN 



Figure 89: Creating cuboid area 

When the cuboid area has been defined, the settings must be saved. Then the validation button becomes active. After clicking on "Validate", the validation specifications and the entered values are compared. The robot must now be moved in all 3 directions in and out of the created space. Depending on whether "Stay inside area" or "Stay outside area" is selected, "Violated" appears with a red dot if the function is violated. This can be used to check whether the area boundaries correspond to your specifications. 

After the check has been done, the area is confirmed by clicking on "Confirm Validation". Next to the button, the validation is then confirmed in green and after returning to the rule, the validation symbol of the rule parameter appears in green. 

If "Maximum Speed" is selected in the "Safety Function" field of a rule, this area must be configured by clicking on the "Configure" button that appears. The following view opens. 



Figure 90: Setting of speed 

The maximum permissible speed determined from the risk assessment must be set and confirmed by clicking on "Save". The entry must then be validated by clicking on "Validate". 

After validation of the set speed, the validation must be completed by clicking on "Confirm Validation". 

R02216/1.3/EN 

Franka Robotics GmbH © 

102 

SAFETY RULES AND SCENARIOS/WATCHMAN 

Next to the button, the validation is confirmed by a green symbol and after returning to the rule, the validation symbol of the rule parameter appears in green. 

## **12.11 Validate** 

After changes have been made to the settings in Watchman, validation must take place. The structure of Watchman is such that rules only need to be validated if an included parameter has been changed and a scenario only if an included rule has been changed. 



Figure 91: Validation structure 



Figure 92: Validating 

Non-validated rules are indicated by the orange validation icon in the lower right corner. To validate a scenario, click on "Validate Rules" above the listed rules. 

R02216/1.3/EN 

Franka Robotics GmbH © 

103 

SAFETY RULES AND SCENARIOS/WATCHMAN 



Figure 93: Validating of rules 

All rules of the scenario are now listed with the respective parameters. In the first step, the rule parameters and then the rule itself must be validated in the unconfirmed rules, as described previously. The procedure for validating the various safety functions is described below: 

### **12.11.1 Validating safe inputs** 

- Check whether the activation condition matches the safety concept defined by the risk analysis. 

- Connect peripheral devices to safe input. 

- Check whether the status displayed in the Watchman UI changes when the input is triggered. 

### **12.11.2 Validating SLP-C** 

- Check whether the parameters of the safety functions correspond to the safety concept defined by the risk analysis. 

### **12.11.3 Validating SLS-C** 

- Guide the robot in Programming mode so that the defined rules are violated. 

- Check that the violation state displayed next to the safety function in the Watchman UI changes when the rules are violated at the expected positions/orientations. 

### **12.11.4 Validating SEEPO** 

- Check that the power supply to the end effector is switched off in all expected situations. 

### **12.11.5 Validating the entire rules, scenarios and overall configuration** 

- Check whether the parameters of the safety functions correspond to the safety concept defined by the risk analysis. 

- Check at each level whether the combination of activation triggers, safety functions, reactions, rules and scenarios correspond to the safety concept defined by the risk analysis. 

To validate the rule, click on "Confirm Validation" or check the box next to the rules to be confirmed and then click on "Confirm Selected Rules" above the rules. 

R02216/1.3/EN 

Franka Robotics GmbH © 

104 

SAFETY RULES AND SCENARIOS/WATCHMAN 

All rules are now displayed as validated. 

The next step is to confirm the security scenario by clicking on "Confirm Whole Security Scenario". The Watchman overview is now displayed again and the security scenario that has just been confirmed is now shown as validated. 

All scenarios that have not been validated must be treated within the manner described above. 

After all scenarios have been validated, the " Sign report & commit" button appears in the upper left corner. 



Figure 94: Validating Watchman 

Click on "Sign report & commit". The safety report opens, which is generated from Watchman settings. 

This report contains all the relevant information for documenting the security functions, including the generated checksum. 

The report must now be printed and signed. 



Figure 95: Safety Report 

By subsequently checking the box "I verify that I signed the report" and then clicking on "Commit", it is confirmed that the report has been printed and signed. 

The security configuration is now saved and accepted in the system. The validation symbol next to the slide switch is now displayed in green and shows the validated state. 

By clicking on the validation symbol next to the slide switch, the current checksum of the security configuration is displayed. 

R02216/1.3/EN 

Franka Robotics GmbH © 

105 

ROBOT LED INDICATOR SYSTEM 

# **13 ROBOT LED INDICATOR SYSTEM** 

## **13.1 Overview of the status indicators** 

Status lights on both sides of the base take on the corresponding color, similar to a traffic light. The status lights will flash slowly during boot-up, when Franka Research 3 requires attention, or when the user enters values. The lights are lit in the corresponding color of the Franka Research 3 status during other processes. A circular status light in the middle of the Pilot-Disc indicates Franka Research 3’s status as well. 

When the operator is interacting with the Arm, the status light on the Pilot-Disc is switched off. 



##### **WARNING** 

**Dangerous and uncontrolled motions of the Arm** 

- Risk of severe injury, such as crushing, tearing of the skin, and puncturing from the Arm and end effectors. 

- Ensure that the end effector and/or the object mass and the Center of Mass (CoM) are parameterized correctly. 

- Keep out of the workspace during operation. 

##### **_NOTICE_** 

The motion speed in Teach or Hand-Guiding Mode is pre-set. The speed can be reduced according to the risk evaluation of the Arm within its application. 

The robot uses six distinct LED colors to communicate its operational status. These lights can appear in two patterns: 

- **Solid (Static)** – indicating a stable state 

- **Blinking (Flashing)** – indicating a transitional or attention-required state 

LED indicators are visible in three key locations: 

- Desk Interface 

- Base of the Robot 

- Pilot (Control Handle) 

Each color and pattern combination provides critical information about the robot’s current state and whether it is safe to interact with. These visual cues are designed to enhance operator awareness and safety. 

## **13.2 LED Activation Behavior** 

- **Base LEDs** : 

Always active. They continuously reflect the robot’s operational status and are the primary reference for system state. 

- **Pilot LEDs** : 

Only active during programming or manual guidance. They provide feedback specific to user interaction during these modes. 

R02216/1.3/EN 

Franka Robotics GmbH © 

106 

ROBOT LED INDICATOR SYSTEM 

## **13.3 Startup Checklist for Operators** 

When powering on the robot, always: 

1. Verify that all indicator lights are functioning properly. 

2. Ensure the LEDs are clearly visible from your working position. 

3. Interpret the lights correctly to determine whether the robot is: 

   - a. IDLE or in TEACH mode 

   - b. Executing a task 

   - c. In an error or warning state 

   - d. Awaiting user input 

##### **Important Safety Considerations** 

(*) Whether it is safe to approach the robot in each state depends on the application-specific risk and hazard analysis and the configured safety scenarios. While LED indicators help identify the robot’s state, they are not certified safety functions. 

If in doubt, always use appropriate safety measures before approaching the robot: 

- Press the Emergency Stop 

- Activate a Protective Stop 

- Confirm the robot is in a safe state via the user interface 

## **13.4 Flashing Patterns** 

|**Pattern**|**Frequency**|**Meaning**|
|---|---|---|
|**Slow**<br>**Flashing**|~0.6 Hz|Indicates a transition between states or a request for user attention|
|**Fast Flashing**|~2 Hz|Warns that motion is initiating, the robot is moving slowly, or the system is<br>updating|



##### **Error and Communication Loss** 

If the controller loses communication, this is treated as a critical error and is signaled with a solid red light. 

## **13.5 LED Priority Logic** 

- The LED system always displays the most critical state. 

- If multiple events occur simultaneously, the color with the highest significance is shown. 

- Within the same priority level, only a one-color scheme is displayed at a time to avoid confusion. 

R02216/1.3/EN 

Franka Robotics GmbH © 

107 

ROBOT LED INDICATOR SYSTEM 

## **13.6 LED Color Reference Table** 

|**Category**|**LED Color**|**LED**<br>**Pattern**|**Status Meaning**|**User Action**|
|---|---|---|---|---|
|**Robot**<br>**System**|White|Static|System idle or in TEACH mode.|Observe<br>standard<br>safety<br>precautions<br>before<br>approaching.|
|**Status**|White|Slow<br>Flashing|Booting or shutting down.|Do not<br>interrupt.<br>Wait until<br>complete.|
||White|Fast<br>Flashing|System updating.|Do not<br>unplug or<br>interrupt.<br>Wait until<br>complete.|
|**Brakes**|Yellow|Static|Brakes locked/unlocked.|Used<br>during brake<br>operations.|
||Yellow|Slow<br>Flashing|Waiting for the boot to finish.|Wait until<br>solid yellow or<br>next<br>instruction.|
|**Warnings**|Yellow|Static|Warning state.|Do not<br>approach.<br>Check UI.|
||Yellow|Slow<br>Flashing|Warning:<br>user<br>interaction<br>needed.|Check UI<br>and<br>acknowledge<br>warning.|



R02216/1.3/EN 

Franka Robotics GmbH © 

108 

ROBOT LED INDICATOR SYSTEM 

|**Category**|**LED Color**|**LED**<br>**Pattern**|**Status Meaning**|**User Action**|
|---|---|---|---|---|
||Red|Static|Severe<br>errors<br>(e.g.,<br>safety,<br>system, communication).|Do not<br>approach.<br>Investigate via<br>UI.|
|**Safety Errors**|Red|Slow<br>Flashing|Safety violation or application<br>error.|Check UI.<br>Approach<br>only if safe<br>and trained.|
||Red|Fast<br>Flashing|Error recovery in progress.|Wait or<br>reset via UI.|
||Red|Slow<br>Flashing|Input needed to recover from<br>error. Error recovery possible<br>with user input (e.g., joint limits<br>exceeded during hand-guiding)|Unlock<br>joint or reset<br>to resume<br>operation.|
|**Execution**|Green|Static|Task executing autonomously.|Do not<br>approach.<br>Robot is<br>moving.|
||Green|Fast<br>Flashing|Execution will begin shortly|Do not<br>approach.<br>Execution<br>imminent.|
|**Collaborative**|Green|Slow<br>Flashing|Task active in assist mode.|Approach<br>with care.<br>Follow safety<br>protocols.|
||Blue|Static|Execution phase ready. Brakes<br>engaged.|Approach<br>with care.<br>Robots may<br>start moving.|



R02216/1.3/EN 

Franka Robotics GmbH © 

109 

ROBOT LED INDICATOR SYSTEM 

|**Category**|**LED Color**|**LED**<br>**Pattern**|**Status Meaning**|**User Action**|
|---|---|---|---|---|
|**Execution**<br>**Mode**|Blue|Slow<br>Flashing|Brakes opening or collaborative<br>mode (no active task).|Robot<br>may move<br>slightly. Safe<br>to approach.|
||Blue|Slow<br>Flashing|Execution interrupted. Awaiting<br>feedback.|Provide<br>feedback to<br>resume.<br>Robot paused.|
|**Conflicts**|Magenta|Static|Conflicting input detected (e.g.,<br>manual guidance vs. automation).|Do not<br>approach.<br>Resolve input<br>conflict.|
||Magenta|Slow<br>Flashing|Input needed to resolve conflict.|Provide<br>input or<br>guidance to<br>continue.|



R02216/1.3/EN 

Franka Robotics GmbH © 

110 

SERVICE AND SUPPORT 

# **14 SERVICE AND SUPPORT** 

##### **_NOTICE_** 

If you have purchased your Franka Research 3 at one of our sales partners or if you have cooperated with a service provider, please get in contact with them first. Our partners can consolidate information and reach out to Franka Robotics for troubleshooting and further support. 

Please visit www.franka.world for supplemental material and additional information on our robot. 

For any other requests regarding service and support please contact us at support@franka.de. We will issue a ticket regarding your request in our service and support center, and our experts will respond as soon as possible. 

When contacting our service, please have the following information available: 

- Customer no. 

- Serial no. of the Control 

- Serial number of the Arm 

- Log files of the system 

## **14.1 Rescue System** 

In case the Control does not boot, or an administrator login is not possible, a rescue system is implemented in the Control. 

Only basic functions for accessing the Control are supported in the rescue system. These functions can be: 

- the retrieval of system logs for further error analysis with the customer, 

- retrieving the configuration of the network setting of the Rescue System, 

- the reinstallation of the system version by synchronization with Franka World, 

- resetting the main system to factory settings. 

Robot movements or other interactions with the Arm or end effector are not supported. 

To access the Rescue system user interface, connect an operator device with access to a browser to the X5 port on the Arm base via an Ethernet cable. 

There are multiple ways to boot the Control into the Rescue system: 

### **14.1.1 Using the Desk API:** 

Any authenticated user can boot into the Rescue System by sending a POST request to [URL TBD]. If user credentials are unavailable, this endpoint is accessible without authentication if the operator device is connected to the X5 port on the Arm base. 

### **14.1.2 Using Franka UI:** 

Any authenticated user can boot into the Rescue system by selecting the “Boot into Rescue System” option in the System menu in the header and confirming the action. If user credentials are unavailable, this option is available in the Login Screen if the operator device is connected to the X5 port on the Arm base. 

R02216/1.3/EN 

Franka Robotics GmbH © 

111 

SERVICE AND SUPPORT 



Figure 96: Booting 

##### **Manually:** 

Should the above steps fail, you can use the following manual sequence to boot into the Rescue System: 

- Shut down the Control, wait for the fans to switch off, then switch off the main switch. 

- Wait approx. 10 sec. before restarting the Control by switching on the main switch. 

- Wait at least 20 sec., but less than 40 sec. 

- Switch off the Control with the main switch. 

- Wait 10 sec. 

- Restart the Control by switching on the main switch. 

The Control should now boot into the rescue system. After calling up the robot.franka.de web interface on the connected user device, the following user interface is displayed in the browser. 

R02216/1.3/EN 

Franka Robotics GmbH © 

112 

SERVICE AND SUPPORT 



Figure 97: Rescue System 

##### **Network** 

The Rescue System tries to use the stored network settings of the main system. If this fails, the default settings are used. 

On this page you can temporarily adjust the network settings of the Control. The settings only apply temporarily within the Rescue System and are not adopted in the main system after a restart. 



Figure 98: Network 

##### **System** 

On this page you can start a download of the log-file or initiate the factory reset. 

R02216/1.3/EN 

Franka Robotics GmbH © 

113 

SERVICE AND SUPPORT 



Figure 99: Log Download and Factory Reset 

##### `o` **Log Download** 

When downloading logs, the Rescue System collects the log files of the main system. If the file system of the main system is corrupted, this operation may fail. 

- **Factory Reset** 

The factory reset function resets the main system. All configurations and created tasks as well as all installed apps and functions are deleted. This has no effect on the Rescue System itself. After the reset, the system must be restarted by the user. 

##### **Franka World** 

This function allows you to reinstall or update the system software of the main system. Installing apps and features is not possible in the Rescue System. 

To ensure an error-free installation of the system software, all apps and features are deleted during this type of installation. 

After successful installation and booting of the main system, all apps and features can be reinstalled in the main system via the Franka World page. However, previously created tasks can only be restored if they have been saved or backed up separately before. 

R02216/1.3/EN 

Franka Robotics GmbH © 

114 

SERVICE AND SUPPORT 



Figure 100: Franka World 

##### **Exiting the Rescue System** 

To exit the rescue system, the Control must be restarted. The Control then restarts in the regular system. 

## **14.2 Log download** 

The FR3 system collects information while it is running and forwards this data to the user through specific log files. Currently, there are four different log files where this information is gathered and provided. 

### **14.2.1 Available log files and how to download them** 

The four different log files include: 

|**Log file**|**Description**|**Specific to**|
|---|---|---|
|System log package|It contains all log files that are specific to the system, readable<br>only by Franka Robotics employees. These logs are used for<br>trouble shooting system issues. It is recommended to include<br>system logs when creating a support ticket.|Franka Robotics employees|
|Safety log|It contains all safety-related events of the system. This log is<br>human-readable and will never be deleted, even during a<br>factory reset.|Franka Robotics employees,<br>integrators, and end users|
|Cyclic log data|It contains data collected while the robot is active, such as<br>forces and velocities.|End<br>users,<br>and<br>Franka<br>Robotics employees|
|Event log data|It contains all event-based data, including restarts and system<br>updates.|End users|



R02216/1.3/EN 

Franka Robotics GmbH © 

115 

SERVICE AND SUPPORT 

### **14.2.2 Downloading log data** 

Log data can be downloaded in Settings for each of log files. 

- **System log package, cyclic log and event log:** These can be downloaded under Settings -> System. 



Figure 101: System 

- **Safety log:** This can be downloaded under Settings -> Safety. 



Figure 102: Safety 

R02216/1.3/EN 

Franka Robotics GmbH © 

116 

SERVICE AND SUPPORT 



Figure 103: Download 

- **Desk API:** All log files are also available via the Desk API. 

## **14.3 Torque calibration** 

FR3 comes with torque sensors on every joint. Out-of-limit efforts exerted on the arm, such as impacts or overloads, can deteriorate system performance in areas of hand-guiding or force application, and may require new calibration of the torque sensors. 

The torque sensors calibration in Settings allows a user with the admin role to re-calibrate the sensors to be able to use the robot again without the necessity to send it back to Franka Robotics GmbH. 



Figure 104: Calibration 

R02216/1.3/EN 

Franka Robotics GmbH © 

117 

SERVICE AND SUPPORT 

### **14.3.1 When to calibrate the torque sensors** 

The torque sensors should be calibrated in one of the following cases: 

- When hand-guiding the robot arm feels unbalanced, because one of the joints is either pushing or pulling. 

- When applying force triggers force or torque threshold violations. 

- When customer support instructs you to do so. 

### **14.3.2 How to calibrate torque sensors** 

The torque sensors can be calibrated in Settings. The torque sensors calibration routine will guide you through the following steps: 

##### **_NOTICE_** 

The torque sensors should be calibrated only with the robot arm mounted on a fixed horizontal flat surface. Any un-flat surface or vibrations during the calibration will significantly influence the results. 

##### **1. Preparation of the robot arm** 

- a. The user must confirm that the workspace is free of any obstacles and can move freely. The torque sensor calibration routine will move the robot in its full workspace. 

- b. The user must confirm that the robot arm is mounted upright and level. 



Figure 105: Prepare Arm 

2. **Preparation of the system** 

R02216/1.3/EN 

Franka Robotics GmbH © 

118 

SERVICE AND SUPPORT 

The user needs to be logged in with the admin role and have control over the robot arm. 

- a. The joints need to be unlocked. 

- b. The operation mode needs to be “Execution” 

- c. The end effector profile “no end-effector" needs to be set. 

- d. The user needs to confirm that no end effector is mounted to the robot arm. 

- e. The execution needs to be ready. The system checks internally that: 

   - i. The robot arm is not in collaborative operation mode. 

   - ii. No task is running. 

   - iii. The system configuration in Watchman is validated. 



Figure 106: Prepare system 

##### **3. Calibrate** 

The torque sensors calibration will be run. This can take up to five minutes. The robot will move to certain positions while measuring internal torques 

##### **_NOTICE_** 

The torque sensors should be calibrated only with the robot arm mounted on a fixed horizontal flat surface. Any un-flat surface or vibrations during the calibration will significantly influence the results. 



##### **WARNING** 

The robot arm may appear not to move but always confirm in the Calibration page if it is safe to approach the arm before doing so. 

During calibration, do not approach the robot arm. Do not cause any vibrations of the mounting surface. Do not obstruct the path of the Arm. 

- Do not cause any vibrations of the mounting surface. 

- Do not obstruct the path of the Arm. 

- The status LED may turn yellow while the robot arm moves in a singularity. This is expected behavior, and no user action is necessary. 

R02216/1.3/EN 

Franka Robotics GmbH © 

119 

SERVICE AND SUPPORT 

##### **_NOTICE_** 

The robot arm may appear not to move but always confirm in the Calibration page if it is safe to approach the arm before doing so. 



Figure 107: Run procedure 

4. **Confirm the values** 

The values will be presented to the user. 

- a. The user can apply the values to the system. 

   - i. If the values are applied the robot arm will restart. 

- b. The user can abort, the values will not be saved, a new calibration can be started. 

R02216/1.3/EN 

Franka Robotics GmbH © 

120 

SERVICE AND SUPPORT 



Figure 108: Confirm values 

### **14.3.3 Reset to factory defaults** 

After a torque offset calibration has been executed the Settings page will allow a user with Admin role to reset the torque offsets to its factory values. 



Figure 109: Joint torque offsets 

### **14.3.4 Error handling** 

In case the problems with the robot arm persist after the calibration, please contact customer support. There might be instances especially in case of collisions – that are beyond the possibilities of torque calibration. 

R02216/1.3/EN 

Franka Robotics GmbH © 

121 

SERVICE AND SUPPORT 

## **14.4 Hardware Exchange** 

In case of damage to the Control unit or the Arm, it may be necessary to carry out a replacement of the respective defective component. 

### **14.4.1 Replacing the Control** 

In the case of a failed Control unit, two situations must be considered: 

1. Control can still be started and can connect to Franka World 

2. Control can no longer be started and/or synchronized with Franka World 

##### **14.4.1.1 Control can still be started** 

All installed features and apps can be detached from the defective Control via Franka World and made available for transfer to the new Control. Follow these steps: 

##### **Step 1: Backup the old Control** 

- Perform a backup of the Control as **_<mark>described in Chapter 8.5 "Backup in this Manual".</mark>_** 

##### **Step 2: Detach features and apps via Franka World** 

1. Open Franka World in a browser and switch to the MANAGE view. 

2. Select the defective Control. The system information and installed features are displayed. 

3. Remove the blue checkmarks for all features you wish to detach. 

   - Take a screenshot or note which features were installed for reference. 

4. Click SYNCHRONIZED to apply detachment at the next synchronization. 

##### **_NOTICE_** 

This ensures that all licenses for features and apps are detached from the old Control and available for linking to the new Control. 

##### **Step 3: Replace the old Control physically** 

   - Remove the defective Control and install the new control. 

- **Step 4: Register the new Control** 

   1. Switch on the new Control and open the Desk interface via https://franka.robot.de. 

   2. Navigate to Settings ‘Software updates’ and click REGISTER. 

##### **_NOTICE_** 

This is not a first-time robot registration. It links the new Control to the existing Franka World account so that previously licensed features, apps, and updates can be synchronized 

##### **Step 5: Synchronize features and apps** 

1. Open Franka World in the browser and log in. 

2. Switch to the MANAGE view and select the new Control. 

3. Using the screenshot or notes from the old Control, reselect the features to link to the new Control. 

4. Click SYNCHRONIZED to apply the changes. 

5. Return to the Desk interface on the robot, navigate to Settings ‘Software updates’, and click DOWNLOAD, then APPLY. 

R02216/1.3/EN 

Franka Robotics GmbH © 

122 

SERVICE AND SUPPORT 

6. The Control will install all changes and may restart as needed. 

##### **_NOTICE_** 

Downloading updates or safety settings manually via the Standard UI (import procedure) does not transfer features, apps, or licenses. Always use backup and Franka World synchronization for a full setup transfer. 

##### **Step 6: Restore system settings** 

- Restore the system from the backup of the old Control, **_<mark>as described in Chapter 8.5 "Backup" in this Manual.</mark>_** This ensures that all system configurations and updates are preserved. 

##### **14.4.1.2 Control can no longer be started or synchronized** 

If the defective Control cannot start or connect to Franka World: 

Contact <u>support@franka.de</u> to release licenses from the old Control. Provide: 

   - Franka World account name and number 

   - Serial number of the defective Control 

   - Serial number of the new Control (optional) 

   - Platform type (FP3/FR3) 

2. Install and start the new Control. 

3. Transfer features and apps by following Step 5: Synchronize features and apps above. 

4. Optional: If you have updates from the old Control, import them according to ‘ <mark>’</mark> **_<mark>Chapter 8.4 “Updates in this Manual”</mark> ._** 

**_NOTICE_** 

Without contacting Support and releasing licenses, features and apps cannot be linked to the new Control. 

## **14.5 Transportation pose of the Arm** 

#### **Procedure** 

1. Log onto the user interface in Franka UI. 

2. Click on Settings. 

3. Navigate to System. 

4. Depending on the Execution mode 

   - a. In Programming: Click and hold-to-run the “Move to pack pose” button. 

   - b. In Execution: Click the “Move to pack pose button” and wait until the motion has finished. 

The Arm will automatically move to the transport pose while the button is pressed. If the robot is in Programming mode, pressing the enabling device is also necessary to move the robot. 

##### **_NOTICE_** 

The system monitors the connection of the Franka UI hold-to-run control with a maximum timeout of 1 s. If a connection loss is detected while hold-to-run control is pressed, the system is stopped. 

R02216/1.3/EN 

Franka Robotics GmbH © 

123 

SERVICE AND SUPPORT 

##### **Procedure** 

1. Navigate to Settings: 



Figure 110: Settings 

##### **_NOTICE_** 

The only change in this version is the sidebar UI in Settings (updated to version 5.9). All other interfaces, including Settings pages, Dashboard, and workflows, remain the same as in version 5.8. Images and instructions from 5.8 can still be used, except where the sidebar is shown. 

2. Navigate to System: 



Figure 111: System 

3. Need to unlock the brakes and hold down x4 to start moving the robot (Programming Mode): 

R02216/1.3/EN 

Franka Robotics GmbH © 

124 

SERVICE AND SUPPORT 



Figure 112: Brakes unlocked 

4. Need to hold down x4 to start moving the robot (Programming Mode): 



Figure 113: x4 external enabling device 

5. Need to unlock the brakes to start moving the robot (Execution): 



Figure 114: Brakes unlocked execution mode 

6. Moving to Pack Pose button enabled (Programming) 

R02216/1.3/EN 

Franka Robotics GmbH © 

125 

SERVICE AND SUPPORT 



Figure 115: Brakes unlocked execution mode 

7. Moving to Pack Pose button enabled (Execution) 



Figure 116: Pack pose button enabled in execution mode 

8. Release x4 before Robot reaches Pack Pose (Programming mode) 



Figure 117: Before robot reaches pack pose in programming mode 

9. Abort Move to Pack Pose button (Execution mode) 

R02216/1.3/EN 

Franka Robotics GmbH © 

126 

SERVICE AND SUPPORT 

##### **_NOTICE_** 

Aborting does not generate any additional dialogue. The screen simply returns to the state where the 'Move to Pack Pose' button is enabled (Execution mode) 



Figure 118: Abort move to pack pose button in execution mode 

10. Move to Pack Pose Completed 

##### **_NOTICE_** 

Programming – Execution does not trigger an additional pop-up. 



Figure 119: Move to pack pose completed 

R02216/1.3/EN 

Franka Robotics GmbH © 

127 

INDEX 

# **15 INDEX** 

|Administrator.................................................................. 47|
|---|
|Apps ............................................................. 10, 26, 28, 48|
|Axes .................................................................................. 16|
|Backup ............................................................................. 55|
|End Effector Configuration ..................................... 57|
|Modbus Configuration ............................................. 57|
|Network Setting ........................................................ 56|
|Safety Configuration .......................................... 56, 90|
|Saving of the created Tasks .................................... 58|
|Cartesian ......................................................................... 85|
|Cartesian space .............................................................. 15|
|Center of Mass (CoM) ......................................... 59, 111|
|Collaboration space ....................................................... 24|
|Enabling Button ................................................33, 59, 91|
|End effector ............................................................. 44, 59|
|factory reset ................................................................... 47|
|Factory Reset ................................................................ 118|
|Fail-safe Locking System .............................................. 59|
|Fieldbus .................................................................... 19, 21|
|Franka Control Interface .............................................. 68|
|FCI ................................................................................ 68|
|Franka UI ......................................................................... 91|
|Franka World .................................................. 44, 48, 118|
|Managing Apps and Updates .................................. 48|
|Updates ....................................................................... 49|
|Guiding|
|Guiding / hand-guiding ............................................ 91|
|Guiding Button .................................................... 20, 59|
|Guiding Mode............................................................. 31|
|Idle .......................................................................20, 90, 91|
|Integrator ........................................................................ 45|
|Log Download ............................................................... 118|
|Operating Modes ........................................................... 20|
|Operator ............................................... 46, 83, 85, 90, 91|
|Pose .................................................................................. 15|
|Responsible person ................................................ 45, 46|
|Roles and Personae|
|Administrator ............................................................. 47|



|Roles and Personae|
|---|
|Administrator ............................................................. 46|
|Assigning user roles .................................................. 47|
|Integrator .................................................................... 45|
|Operator ..................................................................... 46|
|Responsible person ................................................... 45|
|Safety operator .......................................................... 46|
|Safety|
|Safe inputs .................................................................. 84|
|Safe outputs ............................................................... 87|
|Safety Concept .......................................................... 83|
|Safety Functionalities ............................................... 84|
|Safety rules ........................................................... 83, 90|
|SEEPO.............................................................................. 86|
|Service and Support ............................................. 59, 116|
|Hardware Exchange ............................................... 126|
|Settings-Schnittstelle .................................................... 43|
|Single Point of Control (SpoC) .................................... 16|
|SLD ................................................................................... 86|
|SLP-J ................................................................................ 86|
|SLS-C ............................................................................... 85|
|SLS-J ................................................................................ 86|
|SMSS ................................................................................ 86|
|Stopping functions ........................................................ 87|
|Category 0 stop ......................................................... 87|
|Category 1 stop ......................................................... 87|
|Category 2 stop ......................................................... 87|
|Task ..................................................................... 12, 16, 27|
|Teaching .......................................................................... 59|
|Tracking error ................................................................. 35|
|Troubleshooting ............................................................ 59|
|User interface................................................................. 46|
|Watchman ......................................................... 42, 83, 90|
|Creating and editing rules ..................................... 103|
|Creation of spheres for modelling an End Effector<br>envelope ............................................................... 101|
|Editing of the Safety Configuration ....................... 92|
|End effector configuration .................................... 100|



R02216/1.3/EN 

Franka Robotics GmbH © 

128 

INDEX 

|General Safety Settings ............................................ 99|Structure of a rule ................................................... 103|
|---|---|
|Safe Input Configuration ........................................ 100|Validate ..................................................................... 107|
|Safety Setup ............................................................... 99||



R02216/1.3/EN 

Franka Robotics GmbH © 

129 

TABLE OF FIGURES 

# **16 TABLE OF FIGURES** 

|Figure 1: language selection initial configuration .................................................................................................................... 10|
|---|
|Figure 2: Network .......................................................................................................................................................................... 10|
|Figure 3: Franka World registration ........................................................................................................................................... 11|
|Figure 4: Creating Administrator ................................................................................................................................................. 12|
|Figure 5: End effector settings .................................................................................................................................................... 12|
|Figure 6: Control request .............................................................................................................................................................. 18|
|Figure 7: User management waiting for approval.................................................................................................................... 18|
|Figure 8: User request ................................................................................................................................................................... 18|
|Figure 9: Enforce control .............................................................................................................................................................. 19|
|Figure 10: Overview operating modes....................................................................................................................................... 20|
|Figure 11: Procedure ..................................................................................................................................................................... 21|
|Figure 12: Jogging .......................................................................................................................................................................... 22|
|Figure 13: Jogging preview .......................................................................................................................................................... 23|
|Figure 14:Test view........................................................................................................................................................................ 24|
|Figure 15: Area assignment .......................................................................................................................................................... 24|
|Figure 16: Work operation ........................................................................................................................................................... 25|
|Figure 12: Assist operation ........................................................................................................................................................... 27|
|Figure 18: Indication of Assist Mode.......................................................................................................................................... 27|
|Figure 19: Conditions for motion enabling in Assist Mode ................................................................................................... 28|
|Figure 20: App parameterization ................................................................................................................................................. 31|
|Figure 21: App interface ............................................................................................................................................................... 32|
|Figure 22: Pose fine adjustment .................................................................................................................................................. 33|
|Figure 23: Overview of switching between Hand-Guiding-Modes ..................................................................................... 34|
|Figure 24: Illustration of Hand Guiding ..................................................................................................................................... 34|
|Figure 25: Settings, if “User mode” is selected ......................................................................................................................... 34|
|Figure 26: Hand guide approval .................................................................................................................................................. 36|
|Figure 27: Test & Jog ..................................................................................................................................................................... 37|
|Figure 28: Franka UI ...................................................................................................................................................................... 38|
|Figure 29: Download User Manual ............................................................................................................................................. 39|
|Figure 30:Desk ...............................................................................................................................**Error! Bookmark not defined.**|
|Figure 31: Sidebar .......................................................................................................................................................................... 42|
|Figure 32: Watchman .................................................................................................................................................................... 42|
|Figure 33: Menu Settings .............................................................................................................................................................. 43|
|Figure 34: Managing Apps and Features via Franka World ................................................................................................... 48|
|Figure 35: Software update .......................................................................................................................................................... 49|
|Figure 36: Fetch update automatically (recommended) ......................................................................................................... 50|
|Figure 37: Apply button ................................................................................................................................................................ 50|
|Figure 38: Apply and reboot ........................................................................................................................................................ 51|
|Figure 39: Applying changes ........................................................................................................................................................ 51|



R02216/1.3/EN 

Franka Robotics GmbH © 

130 

##### TABLE OF FIGURES 

|Figure 40: Applying changes and rebooting ............................................................................................................................. 52|
|---|
|Figure 41: Rebooting ..................................................................................................................................................................... 52|
|Figure 42: Synchronize manually ................................................................................................................................................ 53|
|Figure 43: Upload update file ...................................................................................................................................................... 53|
|Figure 44: Uploading update file ................................................................................................................................................. 54|
|Figure 45: Dismiss .......................................................................................................................................................................... 54|
|Figure 46: Network Settings ........................................................................................................................................................ 56|
|Figure 47: Save Tasks .................................................................................................................................................................... 57|
|Figure 48: Message “A joint limit has been violated” .............................................................................................................. 59|
|Figure 49: Message with display of the faulty joint ................................................................................................................ 59|
|Figure 50: Confirmation joint is back in the limit ..................................................................................................................... 60|
|Figure 51: Message “Joint position error detected” ................................................................................................................ 61|
|Figure 52: Message with display of failed joints ...................................................................................................................... 61|
|Figure 53: Joint recovery locked ................................................................................................................................................. 62|
|Figure 54: Joint recovery ready for movement ........................................................................................................................ 62|
|Figure 55: Conformation position reached ............................................................................................................................... 63|
|Figure 56: Confirmed Joint recovery.......................................................................................................................................... 63|
|Figure 57: Message Button not held .......................................................................................................................................... 64|
|Figure 58: Message if reference position not reached ........................................................................................................... 64|
|Figure 59: Confirm the complete recovery ............................................................................................................................... 65|
|Figure 60: Schematic overview FCI ............................................................................................................................................ 67|
|Figure 61: Network connection for FCI Usage ........................................................................................................................ 71|
|Figure 62:Network settings......................................................................................................................................................... 72|
|Figure 63: Values ............................................................................................................................................................................ 73|
|Figure 64: Ubuntu –setting a static IP...................................................................................................................................... 73|
|Figure 66: TUI-Interface ............................................................................................................................................................... 76|
|Figure 67: Watchman .................................................................................................................................................................... 85|
|Figure 68: States during normal operation ................................................................................................................................ 88|
|Figure 69: Editable parameters .................................................................................................................................................... 89|
|Figure 70: Validated rules ............................................................................................................................................................. 89|
|Figure 71: Switch to “Draft” mode .............................................................................................................................................. 90|
|Figure 72: Draft Mode ................................................................................................................................................................... 90|
|Figure 73: Validation markers ...................................................................................................................................................... 91|
|Figure 74: Import/Export settings .............................................................................................................................................. 91|
|Figure 75: Standard UI Watchman ............................................................................................................................................. 92|
|Figure 76: Import settings as drafts ............................................................................................................................................ 93|
|Figure 77: File selection ................................................................................................................................................................ 93|
|Figure 78: Warning dialog ............................................................................................................................................................ 94|
|Figure 79: Safety settings imported ........................................................................................................................................... 94|
|Figure 80: Error Message .............................................................................................................................................................. 95|
|Figure 81: Safety Setup ................................................................................................................................................................. 95|



R02216/1.3/EN 

Franka Robotics GmbH © 

131 

##### TABLE OF FIGURES 

|Figure 82: End Effector Configuration ....................................................................................................................................... 96|
|---|
|Figure 83: Configuration of spheres ........................................................................................................................................... 97|
|Figure 84: Example of spheres for Franka Hand ...................................................................................................................... 98|
|Figure 85: Example of sphere configuration Franka hand with staff ................................................................................... 98|
|Figure 86: Editing rules.................................................................................................................................................................. 99|
|Figure 87: structur of a rule.......................................................................................................................................................... 99|
|Figure 88: Configuration of ”Activation Space” ..................................................................................................................... 101|
|Figure 89: monitoring .................................................................................................................................................................. 101|
|Figure 90: Creating cuboid area ................................................................................................................................................ 102|
|Figure 91: Setting of speed ........................................................................................................................................................ 102|
|Figure 92: Validation structure .................................................................................................................................................. 103|
|Figure 93: Validating .................................................................................................................................................................... 103|
|Figure 94: Validating of rules ..................................................................................................................................................... 104|
|Figure 95: Validating Watchman ............................................................................................................................................... 105|
|Figure 96: Safety Report ............................................................................................................................................................. 105|
|Figure 97: Booting ........................................................................................................................................................................ 112|
|Figure 98: Rescue System ........................................................................................................................................................... 113|
|Figure 99: Network ...................................................................................................................................................................... 113|
|Figure 100: Log Download and Factory Reset ....................................................................................................................... 114|
|Figure 101: Franka World ........................................................................................................................................................... 115|
|Figure 102: System ...................................................................................................................................................................... 116|
|Figure 103: Safety ........................................................................................................................................................................ 116|
|Figure 104: Download ................................................................................................................................................................. 117|
|Figure 105: Calibration ................................................................................................................................................................ 117|
|Figure 106: Prepare Arm............................................................................................................................................................. 118|
|Figure 107: Prepare system ....................................................................................................................................................... 119|
|Figure 108: Run procedure ......................................................................................................................................................... 120|
|Figure 109: Confirm values ........................................................................................................................................................ 121|
|Figure 110: Joint torque offsets ................................................................................................................................................ 121|
|Figure 111: Settings ..................................................................................................................................................................... 124|
|Figure 112: System ...................................................................................................................................................................... 124|
|Figure 113: Brakes unlocked ...................................................................................................................................................... 125|
|Figure 114: x4 external enabling device .................................................................................................................................. 125|
|Figure 115: Brakes unlocked execution mode ....................................................................................................................... 125|
|Figure 116: Brakes unlocked execution mode ....................................................................................................................... 126|
|Figure 117: Pack pose button enabled in execution mode.................................................................................................. 126|
|Figure 118: Before robot reaches pack pose in programming mode ................................................................................ 126|
|Figure 119: Abort move to pack pose button in execution mode ..................................................................................... 127|
|Figure 120: Move to pack pose completed ............................................................................................................................ 127|



R02216/1.3/EN 

Franka Robotics GmbH © 

132 

TABLE OF FIGURES 

© Copyright 2026 Franka Robotics GmbH Koppstraße 12 81379 Munich Germany 



R02216/1.3/EN 

Franka Robotics GmbH © 

133 

