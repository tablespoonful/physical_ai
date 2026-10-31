> **[PDF を開く](<Quick Installation Guide FR3 Duo_R04240_1.3_EN-1.pdf>)**
>
> PDF から自動変換した本文です。図は含まず、表は崩れている場合があります。安全や仕様の確認には PDF を使ってください。

Quick Guide for Installation 

Quick Guide for Installation 

# FR3 Duo 



© Copyright 2026 

Franka Robotics GmbH Koppstraße 12 81379 Munich Germany 

## **QUICK GUIDE FOR INSTALLATION** 

##### **This booklet will guide you through the steps to get your FR3 Duo up and running.** 

Document name:              Quick Guide for Installation FR3 Duo Document number:          R04240 Change log: 

|**Content Iteration**|**Release Date**|**Release notes / Changes**|
|---|---|---|
|1.0|03.09.2025|Quick guide for the installation of FR3 Duo|
|1.1|29.04.2026|Added assembly instruction for FR3 Duo on Franka Spine. See Chapter 6.2|
|1.2|21.05.2026|Added S2.1.4 and S2.1.5|
|||Corrected screws description of S2.2.5 and S2.2.6|
|1.3|07.07.2026|Added chapter 9 ‘’Setting the mounting orientation for regular Arm’’|





Get your manual and additional supporting material in English and other languages at <u>www.franka.de/documents.</u> 

Copyright © Franka Robotics GmbH 

2 



## **Table of Contents** 

|1<br>Introduction .................................................................................................................... 5|
|---|
|2<br>Legal Disclaimer ............................................................................................................. 5|
|3<br>Operational Guidelines.................................................................................................... 5|
|4<br>Safety Guidelines ............................................................................................................ 7|
|5<br>Scope of Delivery ............................................................................................................ 8|
|6<br>Optional Accessories ...................................................................................................... 9|
|6.1<br>Pedestal v0.1 .......................................................................................................... 9|
|6.1.1<br>Scope of Delivery ............................................................................................... 10|
|6.1.2<br>Assembly Instructions: FR3 Duo with Pedestal v0.1 ............................................. 11|
|6.2<br>Pedestal v0.2 ......................................................................................................... 15|
|6.2.1<br>Scope of Delivery ............................................................................................... 16|
|6.2.2<br>Assembly Instructions: FR3 Duo with Pedestal v0.1 ............................................. 17|
|6.3<br>Franka Spine .......................................................................................................... 21|
|6.3.1<br>Scope of Delivery ............................................................................................... 21|
|6.3.2<br>Assembly Instruction: FR3 Duo with Franka Spine ............................................... 21|
|6.4<br>FR3 Duo Vision & Manipulation Kit .......................................................................... 23|
|6.4.1<br>Scope of Delivery ............................................................................................... 23|
|6.4.2<br>Assembly Instructions: Head Camera Bundle ..................................................... 25|
|6.4.3<br>Assembly Instructions: Gripper and Wrist Camera Bundle ................................... 26|
|7<br>Interface Drawings ......................................................................................................... 27|
|8<br>FR3 Duo Franka Reference Kinematics ............................................................................ 28|
|9<br>Setting the Mounting Orientation for Regular Arms ........................................................... 30|
|10<br>Table of Figures ......................................................................................................... 31|



Copyright © Franka Robotics GmbH 

3 



##### **NOTICE** 

This Quick Guide for Installation is not the manual of your Franka Research 3 robot and does not replace it. 



Before operating robots from Franka Robotics, all people working with them must read the corresponding manual carefully. Read or download the manual (translations available) here: www.franka.de/documents. 



Don’t hesitate to contact your sales partner or integrator if you need more detailed information. Alternatively, you can get in touch with us directly by sending an email to: <u>support@franka.de.</u> 

##### **NOTICE** 

Please carefully follow all instructions, warnings, and other notes in this document and the official manual. Any deviation from the steps prescribed in these documents constitutes a misuse (as described in the paragraph “Misuse” of the corresponding manual). Franka Robotics does not assume any warranty and/or liability for any possible consequences. 

##### **DANGER** 

Safety-related aspects must be considered when planning and designing the application and performing the hazard & risk assessment for completed machinery. 

Copyright © Franka Robotics GmbH 

4 



## **1 Introduction** 

This Quick Guide for Installation provides step-by-step instructions for assembling and connecting FR3 Duo. It is intended to help users quickly set up the hardware and prepare it for initial operation. 

##### **NOTICE** 

This manual applies to prototype hardware and is not certified according to safety standards. Use only in controlled environments by qualified personnel. 

##### **NOTICE** 

FR3 Duo is compatible with Franka Robot Arm v2.0 and later versions. 

## **2 Legal Disclaimer** 

FR3 Duo is an experimental development tool provided solely for testing and evaluation. They are not part of the certified product portfolio of Franka Robotics GmbH and are supplied 'as-is' without any express or implied warranties, including but not limited to warranties of merchantability, fitness for a particular purpose, or conformity. The Supplier does not provide any support, maintenance, or updates for these tools. Any liability for material or legal defects (Material-legal defects) is excluded, except in cases of willful misconduct or gross negligence. This clause shall not affect mandatory liability under applicable product liability laws or for injury to life, body, or health. 

## **3 Operational Guidelines** 

- **Qualified Personnel Only:** Operate and maintain prototypes only by trained individuals familiar with robotic systems. 

- **Controlled Environment:** Use prototypes exclusively in supervised, indoor environments with stable surfaces. 

- **Personal Protective Equipment (PPE):** Wear safety gloves and protective eyewear during assembly, adjustment, or maintenance. 

- **Keep Clear of Moving Parts:** Never place hands or objects near active joints, drives, or robotic arms during operation. 

- **Disconnect Power Before Maintenance:** Always power down and unplug the system before performing any adjustments or repairs. 

- **Wireless E-Stop:** Always use the wireless E-Stop during operation of the prototype. 

##### **WARNING** 

Due to the heavy dead weight of the equipment and partly due to the geometric design, lifting and handling the equipment may cause physical injury. If the system or any of the components falls on a person, serious injury to fingers, hands, toes, and feet is possible. 

Copyright © Franka Robotics GmbH 

5 



- When transporting the equipment, always wear personal protective equipment (e.g., safety shoes, safety gloves). 

- Always lift the equipment with the help of a second person. 

- Follow the existing company regulations on lifting loads and personal protective equipment. 

##### **NOTICE** 

Always keep the original packaging in case of relocating the robot or its accessories. 

##### **Other User Devices** 

The risk assessment conducted does not cover additional interfaces/devices beyond those delivered with the system. Connecting additional user devices requires a renewed risk assessment to be performed by the user or system integrator. 

##### **Limitations, Constraints, and Misuse** 

Any application different from the intended use is a misuse and is not permitted. This includes, but is not limited to, the following uses: 

##### **Operational Misuse** 

- Transport of people or animals. 

- Transport without original packaging. 

- Use as climbing assistance. 

- Leaning against the TMR. 

- Handling of liquids. 

##### **Environmental Restrictions** 

- Use in potentially explosive areas. 

- Use below ground or in confined spaces. 

- Not designed for flammable/explosive environments. 

- Use for the handling of radioactive objects. 

- Use outdoors. 

- Use in private environments, e.g., real homes. 

- Use in the vicinity of children. 

##### **Safety And Compliance** 

- Use as a medical product. 

- Use outside of the specified operating limits. 

##### **Expected Environment** 

- Location: Dry, indoor lab or industrial setting. 

- Humidity: typically, non-condensing. 

- Floor conditions: Clear paths; avoid uneven surfaces. 

- Shared spaces: Allowed but require restricted access and monitoring. 

Copyright © Franka Robotics GmbH 

6 



##### **Required Operator Skill Level** 

- Trained R&D or technical personnel only. 

- Must complete safety briefing and understand: 

   - Emergency stop procedures 

   - Shared-space safety rules 

## **4 Safety Guidelines** 

The following guidelines are essential for the safe operation and handling of prototype hardware. These instructions apply to FR3 Duo and all associated accessories. 

The following notices are used throughout this manual to indicate the level of risk and importance of information: 

##### **DANGER** 

Indicates a hazardous situation that, if not avoided, will result in death or serious injury. 

##### **WARNING** 

Indicates a hazardous situation that, if not avoided, could result in death or serious injury. 

##### **CAUTION** 

Indicates a hazardous situation that, if not avoided, could result in minor or moderate injury. 

##### **NOTICE** 

Indicates important information not related to personal safety, but essential for proper operation. 

##### **SAFTEY-INSTRUCTIONS** 

Indicates processes or steps that must be strictly observed to ensure safe operation. 

Copyright © Franka Robotics GmbH 

7 



## **5 Scope of Delivery** 

|**ID**|**Comp**|**onent**|**Preview**|**Qty**|
|---|---|---|---|---|
|**S1**|**Franka**|**Research 3**|||
||S1.1|Franka Research 3 Arm||2|
||S1.2|Control||2|
||S1.3|Emergency Stop Device||2|
||S1.4|External Enabling Device||2|
||S1.5|Connecting Cable||2|
|**S2**|**FR3 Du**|**o Mounting Kit v0.3**|||
||**S2.1**|**FR3 Duo Cover v0.3**||1|
|||S2.1.1<br>Arm Base Cover||1|
|||S2.1.2<br>Cables Lid||1|
|||S2.1.3<br>Cables Lid Screw|CSPPNSB-ST3W-TP4-5<br>(Self-tapping screw,⌀4 x 5)|1|
|||S2.1.4<br>Camera Bracket Lid Cover||1|
|||S2.1.5<br>ISO4762-M4x12|Hexagon socket cap screw|4|



Copyright © Franka Robotics GmbH 

8 





##### **Tools Needed** 

- Torque Wrench 

- 6 mm Hex Bit 

- 5 mm Hex Bit 

- 3 mm Hex Bit 

- Loctite 243 



The tools listed above are not included in the scope of delivery. 

## **6 Optional Accessories** 

### **6.1 Pedestal v0.1** 

A wheeled pedestal that enables the flexible placement of FR3 Duo. It provides mounting brackets for two Franka Controls and an interface for installing the FR3 Duo at the necessary height. 

Copyright © Franka Robotics GmbH 

9 





_Figure 1: Pedestal composition_ 

#### **6.1.1 Scope of Delivery** 



Copyright © Franka Robotics GmbH 

10 





###### **_NOTICE_** 

Installation height depends on the use case. The components provided in the scope of delivery are designed to position FR3 Duo at the _FR3 Duo Franka Reference Kinematics_ (Chapter 8). Adjusting height requires modifications for which the customer is responsible. In this case, the customer must procure an Item Profile of the required height to match their kinematics. 

**Tools Needed** 

- Torque Wrench 

- 6 mm Hex Bit 

- 5 mm Hex Bit 

- 10 mm wrench (spanner or socket) 

- Loctite 243 



The tools listed above are not included in the scope of delivery. 

#### **6.1.2 Assembly Instructions: FR3 Duo with Pedestal v0.1** 

**Step 1: Cut-out cover plate** – **Vention Base 790mm** 

Copyright © Franka Robotics GmbH 

11 





_Figure 2: Assemble the cut-out cover plate_ 

**Step 2: Remove screws from Vention Base 790mm** 



_Figure 3: Remove screws from Vention Base 790mm_ 

**Step 3: Brackets for Franka Control** – **Vention Wheeled Base 790** 



_Figure 4: Front-side installation of brackets P1.3 and P1.4 with screws left partially tightened for alignment_ 

**Step 4: Mounting Plate** – **Item Profile** 

Copyright © Franka Robotics GmbH 

12 





_Figure 5: Mounting plate to Item Profile_ 

**Step 5: Item Profile and Mounting Plate** – **Pedestal** 



_Figure 6: Item Profile and Mounting Plate to Pedestal_ 

**Step 6: Base Block Duo** – **Item Profile** 



_Figure 7: Base Block Duo to Item Profile_ 

Copyright © Franka Robotics GmbH 

13 



**Step 7: FR3 Duo Cover Bracket** – **Base Block Duo** 



_Figure 8: FR3 Duo Cover Bracket to Base Block Duo_ 

**Step 8: Arm Adapter Plate** – **Base Block Duo** 



_Figure 9: Arm Adapter Plate to Base Block Duo_ 

**Step 9: FR3 Arms – FR3 Duo Mount** 



_Figure 10: FR3 Arms to FR3 Duo Mount_ 

- Mount two FR3 Arms on the Arm Adapter Plates and connect the necessary cables. 

- <mark>Refer to the Product Manual of Franka Research 3 for detailed instructions of arm assembly.</mark> 

##### **Step 10: Place FR3 Duo Cover** 

Copyright © Franka Robotics GmbH 

14 





_Figure 11: FR3 Duo Cover to FR3 Duo Mount_ 

##### **Step 11: (Optional) Assemble the Cables Lid** 



_Figure 12: Cables Lid to Arm Base Cover_ 

##### **Step 12: Franka Control – Brackets** 



_Figure 13: Alignment of brackets P1.6 and P1.7 before final tightening. Adjust brackets while P1.4 screws remain partially loosened; final torque: 15 Nm (M6)_ 

### **6.2 Pedestal v0.2** 

A wheeled pedestal that enables the flexible placement of FR3 Duo. It provides mounting brackets for two Franka Controls and an interface for installing the FR3 Duo at the necessary height. 

Copyright © Franka Robotics GmbH 

15 





_Figure 14: Pedestal composition_ 

#### **6.2.1 Scope of Delivery** 



Copyright © Franka Robotics GmbH 

16 





###### **_NOTICE_** 

Installation height depends on the use case. The components provided in the scope of delivery are designed to position FR3 Duo at the _FR3 Duo Franka Reference Kinematics_ (Chapter 8). Adjusting height requires modifications for which the customer is responsible. In this case, the customer must procure an Item Profile of the required height to match their kinematics. 

##### **Tools Needed** 

- Torque Wrench 

- 6 mm Hex Bit 

- 5 mm Hex Bit 

- 10 mm wrench (spanner or socket) 

- Loctite 243 



The tools listed above are not included in the scope of delivery. 

#### **6.2.2 Assembly Instructions: FR3 Duo with Pedestal v0.1** 

**Step 1: Remove screws from Vention Base 790mm** 



_Figure 15: Remove screws from Vention Base 790mm_ 

**Step 2: Brackets for Franka Control** – **Vention Wheeled Base 790** 

Copyright © Franka Robotics GmbH 

17 





_Figure 16: Front-side installation of brackets P1.3 and P1.4 with screws left partially tightened for alignment_ 

**Step 4: Mounting Plate** – **Item Profile** 



_Figure 17: Mounting plate to Item Profile_ 

**Step 5: Item Profile and Mounting Plate** – **Pedestal** 



_Figure 18: Item Profile and Mounting Plate to Pedestal_ 

Copyright © Franka Robotics GmbH 

18 



**Step 6: Base Block Duo** – **Item Profile** 



_Figure 19: Base Block Duo to Item Profile_ 

**Step 7: FR3 Duo Cover Bracket** – **Base Block Duo** 



_Figure 20: FR3 Duo Cover Bracket to Base Block Duo_ 

**Step 8: Arm Adapter Plate** – **Base Block Duo** 



_Figure 21: Arm Adapter Plate to Base Block Duo_ 

**Step 9: FR3 Arms – FR3 Duo Mount** 

Copyright © Franka Robotics GmbH 

19 





_Figure 22: FR3 Arms to FR3 Duo Mount_ 

- Mount two FR3 Arms on the Arm Adapter Plates and connect the necessary cables. 

- Refer to the Product Manual of Franka Research 3 for detailed instructions of arm assembly. 

##### **Step 10: Place FR3 Duo Cover** 



_Figure 23: FR3 Duo Cover to FR3 Duo Mount_ 

##### **Step 11: (Optional) Assemble the Cables Lid** 



_Figure 24: Cables Lid to Arm Base Cover_ 

**Step 12: Franka Control – Brackets** 

Copyright © Franka Robotics GmbH 

20 





_Figure 25: Alignment of brackets P1.6 and P1.7 before final tightening. Adjust brackets while P1.4 screws remain partially loosened; final torque: 15 Nm (M6)_ 

### **6.3 Franka Spine** 

Franka Spine is vertical lift with 1 DOF that enables vertical actuation of FR3 Duo. The Franka Spine is currently only compatible with the Tactile Mobile Robot. 

#### **6.3.1 Scope of Delivery** 



#### **6.3.2 Assembly Instruction: FR3 Duo with Franka Spine** 

**Step 1: Ensure that the Franka Spine is securely mounted on the TMR** 

Copyright © Franka Robotics GmbH 

21 





**Step 2: Alignment Pins on Base Block Duo** 



**Step 3: Base Block Duo to Lever** 



##### **NOTICE** 

To complete the remaining assembly of FR3 Duo on the Franka Spine, follow Steps 7 to 11 from Chapter 6.1.2 Assembly Instructions: FR3 Duo with Pedestal 

Copyright © Franka Robotics GmbH 

22 



### **6.4 FR3 Duo Vision & Manipulation Kit** 

FR3 Duo Vision & Manipulation Kit is a collection of vision sensors and manipulation actuators curated by Franka Robotics. It reduces integration efforts and provides a reproducible setup that ensures comparable results across labs. 

#### **6.4.1 Scope of Delivery** 

|**ID**|**Compo**|**nents**||**Preview**|**Qty**|**Notes**|
|---|---|---|---|---|---|---|
|**M1**|**Grippe**|**rs Bundle**|||||
||M1.1|Robotiq 2|F-85 Kit||2x|2-finger gripper kit for UR CB-<br>Series, with RS485 – USB<br>convertor|
||M1.2|Power Su|pply||1x|120 W, 24 V, 5A DIN-rail-<br>mount power supply for 2x<br>Robotiq Grippers|
||M1.3|Cable fix|iation straps||4x|300mm and 650mm slip-<br>resistant Velcro tape|
|**V1**|**Head C**|**amera Bu**|**ndle**||||
||V1.1|ZED Mini|Stereo camera||1x|Ultra-depth<br>sensing<br>and<br>motion tracking camera with<br>1.5m and 4m USB-C to A<br>cable|
||V1.2|Franka H|ead Bracket v0.2||1x|Mounting bracket for ZED Mini<br>Camera|
|||V1.2.1|Head Bracket Base||1|Interfaces<br>with<br>FR3<br>Duo<br>Mount|
|||V1.2.2|Head Bracket<br>Mount||1|Compatible only with ZED<br>Mini Camera|
|||V1.2.3|ISO2338-4x10-h8||2|Alignment Pins|
|||V1.2.4|ISO 4762-M6x30||1|Hexagon socket cap screw|
|||V1.2.5|ISO 4762-M4x12||4|Hexagon socket cap screw|



Copyright © Franka Robotics GmbH 

23 



|||V1.2.6<br>ISO 4762-M2x8|||2x<br>Hexagon socket cap screw|
|---|---|---|---|---|---|
|||V1.2.7<br>ISO 7092 M2x6x0.5|||6x<br>Washer|
|**Pos**|**Compo**|**nents**|**Preview**|**Qty**|**Notes**|
|**V2**|**Wrist C**|**ameras Bundle**||||
||V2.1|D405 RealSense camera||2x|Short-range stereo depth camera|
||V2.2|Wrist camera mount for Robotiq||2x|Wrist Camera Mount|
||V2.3|USB 3.0 to Micro B, Male-to-Male, 90<br>Degree, Up-Angled, 3m||2x|Camera data cable|
||V2.4|ISO 10642 – M3x6|-|2x|Fasteners D405 to Wrist Camera Mount|
||V2.5|ISO 4762 – M4x25|-|4x|Fasteners|
||V2.6|ISO 7089 – M4|-|4x|Washers|
||V2.7|Cable fixation straps||4x|300mm and 650mm slip-resistant<br>Velcro tape|



##### **Tools Needed** 

- Torque Wrench 

- T20 torx bit 

- 5 mm Hex Bit 

- 3 mm Hex Bit 

- <u>2 mm Hex Bit</u> 

- 1.5 mm Hex Bit 



The tools listed above are not included in the scope of delivery. 

Copyright © Franka Robotics GmbH 

24 



#### **6.4.2 Assembly Instructions: Head Camera Bundle** 

**Step 1: Head Bracket Mount – ZED Mini Camera** 



_Figure 26: Head Bracket Base to ZED Mini Camera_ 

**Step 2: Head Bracket Mount – Head Bracket Base** 



_Figure 27: Head Bracket Mount to Head Bracket Base_ 

**Step 5: Route the USB-C Cable** 



_Figure 28: Routing the USB-C cable of ZED Mini Camera_ 

Copyright © Franka Robotics GmbH 

25 



##### **Step 6: Franka Head Bracket – FR3 Duo Mounting Kit** 



_Figure 29: Franka head bracket to FR3 Duo Mounting Kit_ 

#### **6.4.3 Assembly Instructions: Gripper and Wrist Camera Bundle** 

**Step 1: D405 Camera – Wrist Camera Mount** 



_Figure 30: D405 Camera to Wrist Camera Mount_ 

**Step 2: Wrist Camera – Robotiq Gripper** 



_Figure 31: Assembly of components V2.1, V2.2, V2.5, and M1.1 on the gripper. Apply Loctite 243 and tighten M4 screws to 1 Nm._ 

Copyright © Franka Robotics GmbH 

26 



**Step 3: Robotiq Gripper – Franka Arm End-Effector Flange** 



_Figure 32: Robotic Coupling to Franka Arm EE Flange_ 

## **7 Interface Drawings** 



_Figure 33: Mounting Plate (P2.1) between pedestal and item profile_ 

Copyright © Franka Robotics GmbH 

27 





_Figure 34: Base Block Duo (S2.2.1) mounting holes_ 



_Figure 35: FR3 Duo Cover Bracket (S2.2.3) mounting holes_ 

## **8 FR3 Duo Franka Reference Kinematics** 

FR3 Duo kinematics are optimized for: 

- Ensuring elbow-to-elbow distance is small enough to traverse doors. 

- Overlapping the Yoshikawa manipulability space of both arms 

- Maximizing reachability on a table-top surface, considering FR3 Duo’s Origin at 200 mm above the worksurface. 

Copyright © Franka Robotics GmbH 

28 





_Figure 36: Difference between FR3 Arm’s Origin, FR3 Duo’s Origin, and FR3 Duo Mount’s Origin_ 



_Figure 37: Transformation from FR3 Duo origin to the individual arm origins_ 

As the origin of FR3 Duo is not easily accessible, a reference point is engraved at the bottom of FR3 Duo Mount that is easy to identify and measure from. 

Copyright © Franka Robotics GmbH 

29 



For FR3 Duo Mount v0.3, this reference point is located 50 mm below (z) and 37 mm along the negative x-direction relative to FR3 Duo origin. 

From this reference point, visible at the bottom of FR3 Duo Mount v0.3: 

- Ensure the worksurface is 150 mm below 

- Ensure the camera is 400 mm above. 

- Ensure the camera is 53 mm forward. 



_Figure 38: FR3 Duo Mount geometry and vertical reference dimensions_ 

## **9 Setting the Mounting Orientation for Regular Arms** 

If you are using regular arms on a Duo Mount, you need to set the gravity vectors manually. To do this, use the Desk API, which provides an endpoint to configure the mounting orientation of your robot arm. You can set the orientation in roll, pitch, and yaw. For convenience, the Swagger UI also offers presets for the left and right arm mounting positions. 

Copyright © Franka Robotics GmbH 

30 



## **10 Table of Figures** 

|Figure 1: Pedestal composition .............................................................................................. 10|
|---|
|Figure 2: Assemble the cut-out cover plate ............................................................................. 12|
|Figure 3: Remove screws from Vention Base 790mm .............................................................. 12|
|Figure 4: Front-side installation of brackets P1.3 and P1.4 with screws left partially tightened for|
|alignment .............................................................................................................................. 12<br>i|
|Figure 5: Mounting plate to Item Profile .................................................................................. 13<br>i|
|Figure 6: Item Profile and Mounting Plate to Pedestal .............................................................. 13<br>i|
|Figure 7: Base Block Duo to Item Profile ................................................................................. 13|
|Figure 8: FR3 Duo Cover Bracket to Base Block Duo ................................................................ 14|
|Figure 9: Arm Adapter Plate to Base Block Duo ....................................................................... 14|
|Figure 10: FR3 Arms to FR3 Duo Mount ................................................................................... 14|
|Figure 11: FR3 Duo Cover to FR3 Duo Mount ........................................................................... 15|
|Figure 12: Cables Lid to Arm Base Cover ................................................................................ 15<br>i|
|Figure 13: Alignment of brackets P1.6 and P1.7 before final tightening. Adjust brackets while|
|P1.4 screws remain partially loosened; final torque: 15 Nm (M6) ............................................. 15|
|Figure 14: Head Bracket Base to ZED Mini Camera ................................................................. 25|
|Figure 15: Head Bracket Mount to Head Bracket Base ............................................................. 25|
|Figure 16: Routing USB-C cable of ZED Mini Camera ............................................................... 25|
|Figure 17: Franka head bracket to FR3 Duo Mounting Kit ......................................................... 26|
|Figure 18: D405 Camera to Wrist Camera Mount .................................................................... 26|
|Figure 19: Assembly of components V2.1, V2.2, V2.5, and M1.1 on the gripper. Apply Loctite 243<br>and tighten M4 screws to 1 Nm. ............................................................................................. 26|
|Figure 20: Robotiq Coupling to Franka Arm EE Flange ............................................................. 27<br>**i**|
|Figure 21: Franka Spine ..............................................................**Error! Bookmark not defined.**<br>i|
|Figure 22: Mounting Plate (P2.1) between pedestal and item profile ........................................ 27|
|Figure 23: Base Block Duo (S2.2.1) mounting holes ................................................................. 28|
|Figure 24: FR3 Duo Cover Bracket (S2.2.3) mounting holes ..................................................... 28|
|Figure 25: Difference between FR3 Arm’s Origin, FR3 Duo’s Origin, and FR3 Duo Mount’s Origin<br>............................................................................................................................................. 29|
|Figure 26: Transformation from FR3 Duo origin to the individual arm origins ............................ 29|
|Figure 27: FR3 Duo Mount geometry and vertical reference dimensions .................................. 30|



Copyright © Franka Robotics GmbH 

31 



Franka Robotics GmbH Koppstraße 12 81379 Munich 



Copyright © Franka Robotics GmbH 

32 

