> **[PDF を開く](<Product Manual AI Companion_R82010_1.1_EN.pdf>)**
>
> PDF から自動変換した本文です。図は含まず、表は崩れている場合があります。安全や仕様の確認には PDF を使ってください。





# **AI COMPANION** 

**Product Manual** 

PRODUCT MANUAL 

© Copyright 2025 Franka Robotics GmbH Frei-Otto-Straße 20 80797 Munich Germany 

This document and excerpts from it may only be reproduced or made accessible to third parties with the express permission of Franka Robotics GmbH. 

This product manual is designed to provide comprehensive guidance for both Franka Research 3 and Franka Production 3 

The content of this document has been carefully checked for compliance with the described hardware and software. However, deviations cannot be completely ruled out, which is why we assume no liability for complete compliance. 

In the interest of our customers, we reserve the right to make improvements and corrections to hardware, software and documentation at any time and without prior notice. 

We are always grateful for your feedback at documentation@franka.de. 

The original document is in English. 

The following documents supplement this product manual for the Franka AI Companion: 

- Original operating instructions from the manufacturer (ForeCr – UM-DSBXORNX-LAN_01_R1.0_18/03/24) 

- Original operating instructions for the robot system used 

Document name: AI Companion Product Manual 

Document number: R82010 

Version: 1.1 (May 2025) 

Change log: 

|**Release**|**Release date**|**Changes**|
|---|---|---|
|**version**|||
|1.0|April 2025|First Release|
|1.1|May 2025|Added Digital IOs|





Get your manual and additional accompanying material in English and other languages. <u>www.franka.de/documents.</u> 

### **TABLE OF CONTENTS** 

|1<br>F|RANKA AI COMPANION ................................................................................................................................................. 5|
|---|---|
|_1.1_|_Overview ......................................................................................................................................................................... 5_|
|_1.2_|_Device overview ............................................................................................................................................................. 6_|
|2<br>R|IGHTS OF USE AND PROPERTY RIGHTS .................................................................................................................... 9|
|_2.1_|_Before you get started................................................................................................................................................... 9_|
|_2.2_|_Due diligence .................................................................................................................................................................. 9_|
|_2.3_|_Limited warranty............................................................................................................................................................ 9_|
|_2.4_|_Liability and warranty obligation ................................................................................................................................. 9_|
|_2.5_|_General information ...................................................................................................................................................... 9_|
|_2.6_|_Costs for copyright and licenses................................................................................................................................... 9_|
|_2.7_|_Registered trademarks ............................................................................................................................................... 10_|
|_2.8_|_Use of open-source codes (open source) .................................................................................................................. 10_|
|_2.9_|_Removal of identification ........................................................................................................................................... 10_|
|3<br>D|ECLARATION OF INCORPORATION AND CERTIFICATES ................................................................................. 11|
|4<br>S|AFETY ................................................................................................................................................................................ 12|
|_4.1_|_Safety Instructions and General Indications ............................................................................................................ 12_|
|_4.2_|_Disclaimer .................................................................................................................................................................... 13_|
|_4.3_|_Intended use ................................................................................................................................................................ 13_|
|_4.4_|_Improper use................................................................................................................................................................ 13_|
|_4.5_|_Safety guidelines ......................................................................................................................................................... 14_|
|5<br>G|ETTING STARTED WITH AI COMPANION .............................................................................................................. 16|
|_5.1_|_Assembly and Installation of AI Companion ............................................................................................................. 16_|
||5.1.1<br>Compatible Franka robot systems ........................................................................................................... 17|
||5.1.2<br>Ambient conditions ..................................................................................................................................... 17|
||5.1.3<br>Ambient temperature ................................................................................................................................. 17|
|_5.2_|_Assembly of the AI companion .................................................................................................................................. 18_|
|_5.3_|_Wiring to a Franka robot system .............................................................................................................................. 18_|
|_5.4_|_Grounding .................................................................................................................................................................... 19_|
|_5.5_|_Set up a development environment ........................................................................................................................... 16_|
||5.5.1<br>Visual Studio Code for AI companion ..................................................................................................... 16|
||5.5.2<br>Development with Visual Studio Code via Remote SSH .................................................................... 16|
|_5.6_|_COMMISSIONING ...................................................................................................................................................... 20_|
||5.6.1<br>Direct access ................................................................................................................................................ 20|
||5.6.2<br>Access data ................................................................................................................................................... 20|
||5.~~6.3~~<br>~~Remote access .............................................................................................................................................~~20|



Franka Robotics GmbH © 

R82010/1.0/EN 

3 

|_5.7_|_OPER_|_ATION ................................................................................................................................................................ 21_|
|---|---|---|
||5.7.1|Overview of the functional structure of the AI companion ............................................................... 21|
||5.7.2|Base OS layer ............................................................................................................................................... 21|
||5.7.3|Application layer .......................................................................................................................................... 21|
||5.7.4|User layer ...................................................................................................................................................... 21|
||5.7.5|Web UI .......................................................................................................................................................... 21|
||5.7.6|Network configuration ............................................................................................................................... 21|
||5.7.7|System update ............................................................................................................................................. 22|
||5.7.8|Docker container ......................................................................................................................................... 22|
||5.7.9|Desk forwarding .......................................................................................................................................... 22|
||5.7.10|Digital IOs ..................................................................................................................................................... 22|
||5.7.11|CAN bus interface ....................................................................................................................................... 23|
|_5.8_|_Benef_|_its of the development environment............................................................................................................... 23_|
|_5.9_|_Exten_|_ded configuration .............................................................................................................................................. 23_|
||5.9.1|Network configuration ............................................................................................................................... 23|
|6<br>T|ECHNICA|L SPECIFICATIONS ....................................................................................................................................... 25|
|7<br>S|COPE OF|DELIVERY AND ADDITIONAL EQUIPMENT ......................................................................................... 27|
|_7.1_|_Includ_|_ed in scope of delivery ..................................................................................................................................... 27_|
|_7.2_|_Not in_|_cluded in the scope of delivery ....................................................................................................................... 27_|
|8<br>S|ERVICE A|ND SUPPORT ................................................................................................................................................. 28|
|_8.1_|_Updat_<br>|_e ......................................................................................................................................................................... 28_<br>|
||8.1.1|Prerequisites ................................................................................................................................................ 28|
||8.1.2|Procedure ..................................................................................................................................................... 28|
|9<br>|MAINTEN|ANCE ................................................................................................................................................................. 29|
|_9.1_|_Cleani_|_ng ....................................................................................................................................................................... 29_|
|_9.2_|_Dispo_|_sal ....................................................................................................................................................................... 29_|
|_9.3_|_Retur_|_ning packaging waste ....................................................................................................................................... 29_|
|10|LIST OF|FIGURES .......................................................................................................................................................... 30|
|11|INDEX ..|............................................................................................................................................................................ 31|



Franka Robotics GmbH © 

R82010/1.0/EN 

4 

FRANKA AI COMPANION 

## **1 FRANKA AI COMPANION** 

##### **1.1 Overview** 

The AI Companion is a small computer that offers various functions to make working with Franka Research 3 much more intuitive and, above all, to provide easy access to tools in the field of artificial intelligence and machine learning. The user can develop software within a modular environment, exchange it with just a few clicks and also share it with other users over the internet. 

###### **1.1.1 AI Companion Architecture** 

The development environment of the AI Companion is based on a modern Docker infrastructure that enables flexible and efficient containerization. This architecture allows developers to run different containers in parallel and link them seamlessly without having to deal with the complexities of dependencies on the base operating system. 

The AI companion brings an interface to all aspects of the FR3 robot controller i.e.: 

- Directly control the real-time interface of the FR3 

- Run GPU-heavy applications 

- Easily develop multiple individual applications in parallel without dependency conflicts 

- Download individual applications and upload them to another AI Companion 

###### **1.1.2 Use cases** 

Possible use cases include: 

- Creating applications in a modular way using content from the community 

- Managing multiple (even incompatible) applications on one computer 

- Quickly switching between applications without restarting or calling up multiple, unclear scripts 

- Using computationally intensive ML models on a real-time capable computer 

- Using CUDA-based software on a real-time capable computer 

- Downloading user-defined applications and running them onto other AI Companions without further changes 

R82010/1.0/EN                            Franka Robotics GmbH © 

5 

FRANKA AI COMPANION 

##### **1.2 Device overview** 



Figure 1: AI Companion 

The following illustration indicates the controls and the available interfaces and connections. 







Figure 2: Device overview and connections 

R82010/1.0/EN                            Franka Robotics GmbH © 

6 

FRANKA AI COMPANION 

|**Item**|**Description**|**Item**|**Description**|
|---|---|---|---|
|1|Reset button|6|Operatingdisplay|
|2|Recovery button|7|Power supply9 to 28 VDC**_A3_**|
|3|USB C port 1 (Recovery)**_A6_**|8|Ethernet 2x**_A1 / A2_**|
|4|USB Cport 2**_A5_**|9|HDMIport**_A4_**|
|5|USB C port 2**_A5_**|10|IO port**_A7_**|



###### **Reset button (1)** 

To reset the AI COMPANION 

###### **Recovery button (2)** 

To reset, press and hold the reset and recovery buttons for 1 s. 

###### **USB ports A5 / A6 (3/ 4/ 5)** 

The AI COMPANION has three USB 3.0 type C interfaces. The A6 interface (item 3) is a special recovery port that can be used to reset the system. 

###### **Operating display (6)** 

Indicates operation of the AI COMPANION 

###### **Power supply A3 (7)** 

The AI COMPANION requires a power supply of 9 to 28 V DC. 

If the supplied mains adapter is not used, a plug of type 1708595 (DFMC 1.5/2-STF-3.5) from Phoenix Contact must be used. 



Figure 3:Power supply assignment (A3) 

|**Pin**|**Description**|**I/O type**|
|---|---|---|
|**1**|+9 V to 28 V DC|POWER|
|**2**|GROUND|POWER|
|**3**|+9 V to 28 V DC|POWER|
|**4**|GROUND|POWER|



R82010/1.0/EN                            Franka Robotics GmbH © 

7 

FRANKA AI COMPANION 

###### **Ethernet ports A1 / A2 (8)** 

The AI COMPANION provides two Gigabit Ethernet ports. 

###### **HDMI port A4 (9)** 

The AI COMPANION has an HDMI interface that supports DP++ signalling. This means that monitors with DP, DVI, HDMI and VGA inputs can be connected using appropriate cables and adapters. 

###### **IO port A7 (10)** 

The RS232, RS422 and CAN bus signals can be tapped via the AI Companion IO ports. A type 1790344 plug (DFMC 1,5/7-STF-3,5) from Phoenix Contact is required 



Figure 4: Assignment of IO interface (A7) 

|**Pin**|**Description**|**I/O type**|**Pin**|**Description**|**I/O type**|
|---|---|---|---|---|---|
|**1**|RS422 B|I/O|**8**|GROUND|POWER|
|**2**|RS422 Y / RS485 A|I/O|**9**|GROUND|POWER|
|**3**|RS232 RX / RS422A|I/O|**10**|GROUND|POWER|
|**4**|RS232 TX /RS422 Z / RS485 B|I/O|**11**|DIGITAL_OUT1<br>Note:Up to 24 V, low-side switch<br>mechanism|OUTPUT|
|**5**|CAN_H|I/O|**12**|DIGITAL_IN1<br>Note:High at 11–24 V|INPUT|
|**6**|GROUND|POWER|**13**|DIGITAL_OUT0<br>Note:Up to 24 V, low-side switch<br>mechanism|OUTPUT|
|**7**|CAN_L|I/O|**14**|DIGITAL_IN0<br>Note:High at 11–24 V|INPUT|



R82010/1.0/EN                            Franka Robotics GmbH © 

8 

RIGHTS OF USE AND PROPERTY RIGHTS 

### **2 RIGHTS OF USE AND PROPERTY RIGHTS** 

##### **2.1 Before you get started** 

Please read this user manual carefully to ensure you fully understand it before working with the Franka AI Companion. This user manual contains information that is essential for proper operation of the Franka AI Companion. The general safety instructions must be observed, and only trained and authorised personnel may work with the Franka AI Companion. 

##### **2.2 Due diligence** 

It must be ensured that the Franka AI Companion is only used in environments that meet the specification of the Franka AI Companion. This user manual must be fully read and understood and personnel working with the Franka AI Companion must be trained in the standards, regulations and instructions. It must also be ensured that the Franka AI Companion is installed, operated and maintained in accordance with the instructions in this operating manual. All applicable national and international regulations and standards must be complied with. 

##### **2.3 Limited warranty** 

Parts that are subject to natural wear and tear are excluded from the warranty, considering the statutory provisions. 

##### **2.4 Liability and warranty obligation** 

Franka Robotics GmbH is exempt from statutory accident liability if the user does not observe the instructions in this operating manual or the warnings on the device. In the event of damage caused by non-compliance with the instructions in this operating manual or the warnings on the device, Franka Robotics GmbH is also exempt from the warranty and from statutory accident liability during the warranty period. 

##### **2.5 General information** 

To get the most out of the Franka AI Companion, follow the tips in this user guide. Failure to do so may result in inconvenience, injury, or failure of the Franka AI Companion. 

##### **2.6 Costs for copyright and licenses** 

Copyright © 2024 Franka Robotics GmbH. This user manual may not be copied, reproduced, translated, modified or disputed, in whole or in part, in electronic, machine-readable or other form without the written consent of Franka Robotics GmbH. The drivers and utilities for the components used as well as the BIOS are subject to the copyrights of the respective manufacturers. 

The license conditions of the respective manufacturer must be observed. 

Franka Robotics GmbH © 

R82010/1.0/EN 

9 

RIGHTS OF USE AND PROPERTY RIGHTS 

##### **2.7 Registered trademarks** 

Franka Robotics GmbH endeavours to respect the copyrights of graphics and texts used in all publications and endeavours to use original or licence-free graphics and texts. All brands and trademarks referred to in the manual and possibly owned by third parties are subject, unless otherwise stated, to the provisions of trademark law, and trademarks in force in each case are subject in each case without limitation to the provisions of trademark law and the ownership rights of the respective registered owner without limitation. It is not to be assumed that because a brand name is mentioned, it is not legally protected by a third party. 

##### **2.8 Use of open-source codes (open source)** 

This product contains software components licensed under the GNU General Public License (GPL) and the Lesser General Public License (LGPL). In accordance with these licenses, we provide the source code of these components. 

You can obtain the full corresponding source code from us for a period of three years after the last delivery of this product by sending a request to the following address: 

Franka Robotics GmbH Frei-Otto-Straße 20 80797 Munich <u>info@franka.de www.franka.de</u> 

A complete list of all open-source licenses used by Franka Robotics robots can be accessed via the settings menu on the AI Companion user interface. 

##### **2.9 Removal of identification** 

Copyright notices, serial numbers and any other type of marking that serve to identify the product or the operating software may not be removed or altered. 

Franka Robotics GmbH © 

R82010/1.0/EN 

10 

DECLARATION OF INCORPORATION AND CERTIFICATES 

#### **3 DECLARATION OF INCORPORATION AND CERTIFICATES** 

**EU Declaration of Conformity** 



Franka Robotics GmbH © 

R82010/1.0/EN 

11 

SAFETY 

## **4 SAFETY** 

##### **4.1 Safety Instructions and General Indications** 

Read this manual and all related additional documentation carefully before installing, commissioning and operating the device. Observe the safety instructions and general indications. 

Warnings are posted as follows: 



Franka Robotics GmbH © 

R82010/1.0/EN 

12 

SAFETY 

##### **4.2 Disclaimer** 

Franka Robotics GmbH assumes no liability for the topicality, correctness, completeness or quality of the information contained in this manual. 

Franka Robotics GmbH also assumes no liability for further use of the information contained therein. Any liability claims against Franka Robotics GmbH that relate to damage of a material or immaterial nature that have been caused by the use or non-use of the information provided or by the use of incorrect and/or incomplete information, are in principle excluded insofar as there is no proven wilful or negligent fault on the part of Franka Robotics GmbH. 

Franka Robotics GmbH expressly reserves the right to change or supplement the content of this user manual or parts thereof without special notice. 

##### **4.3 Intended use** 

Only use the Franka AI Companion together with compatible robot systems from Franka Robotics and only for the intended purpose. The Franka AI Companion is suitable for use in research. 

The Franka AI Companion may only be used under the ambient and operating conditions described in this document. 

The Franka AI Companion may only be used in perfect technical condition, for the intended purpose and within the technical specifications and operating conditions, considering safety and possible hazards. 

The current Franka AI Companion is only intended for the use described in this manual. 

The normal and extended working conditions under which the Franka AI Companion should work can be found in the technical specifications. 

##### **4.4 Improper use** 

Improper use of the Franka AI Companion voids the manufacturer’s warranty and liability. Any application that deviates from the intended purpose shall be considered improper use and is not permitted. 



###### **WARNING** 

Improper use can endanger life and limb and lead to impairment and damage to the robot and other property. The manufacturer accepts no liability for damage caused by improper use 

Improper use is any use that deviates from the warnings, information and instructions in this manual; in particular, but not exclusively, the following uses: 

- Transporting people and animals 

- Transport without original packaging 

- Use in a potentially explosive area 

- Use underground 

- Use in the handling of radioactive objects 

- Outdoor use 

- Use as a medical device 

- Use near children 

- Handling of liquids 

- Use outside the specified operating limits 

Franka Robotics GmbH © 

R82010/1.0/EN 

13 

SAFETY 

Modifications to the Franka AI Companion that have not been expressly permitted by Franka Robotics are inadmissible and lead to a loss of warranty and liability claims. Impermissible changes include, among others, the following: 

- Any adjustment of the mechanical structure 

- Paintwork 

- Modification of the pre-installed software 

It is not permitted to open the housing of the Franka AI Companion and other equipment. 

Franka Robotics is not liable for damage caused by assembled, gripped or lost equipment or by improper use. 

##### **4.5 Safety guidelines** 



###### **WARNING** 

Failure to observe the following safety instructions may result in injury to the operator and/or damage to the Franka AI Companion. 

- If the safety instructions are not observed, Franka Robotics GmbH is released from accident liability, even if the Franka AI Companion is still under warranty. 

- The Franka AI Companion must be used in accordance with the safety guidelines described in this manual relating to the Franka AI Companion and to the owner. 

- The installation location of the box must comply with the requirements of the standards and regulations in the respective country. If power cables are supplied with the Franka AI Companion, only these may be used. 

- Ensure adequate air circulation to cool the Franka AI Companion. Do not cover the Franka AI Companion or install it near heat sources or in damp places. 

###### **Disconnecting the Franka AI Companion:** 

**1. Power Cable Disconnection:** 

   - If you need to disconnect the Franka AI companion, ensure you first disconnect the power cable. 

   - Always keep the power cable easily accessible. 

**2. Handling Expansion Cards:** 

   - To insert or remove expansion cards, only open the MBox-Advanced after disconnecting all cables. 

   - This task should only be performed by qualified personnel. 

   - When installing expansion cards in the MBox-Advanced, comply with all applicable statutory provisions and technical data. 

   - Ensure the power consumption of the additional cards does not exceed the limits specified on the MBoxAdvanced label. 

Franka Robotics GmbH © 

R82010/1.0/EN 

14 

SAFETY 



###### **CAUTION** 

Safe operation is not possible if the Franka AI Companion is visibly damaged or is non-functional. In this case, the Franka AI Companion must be switched off and it must be ensured that the Franka AI Companion cannot be put back into operation. 

###### **Ensuring Safe Use of the Franka AI Companion:** 

1. **Power Cable Specifications:** 

   - Ensure that the power cables are adequately dimensioned according to the maximum electrical specifications of the Franka AI Companion. 

   - Comply with standards and regulations such as EN60950-1, VDE0100, EN60204, or UL508. 

**2. Safety Information:** 

   - Follow and retain all information provided with the Franka AI Companion. 

   - The information in this user manual does not alter the terms of your purchase contract or the limited warranty of Franka Robotics GmbH. 

**3. Safety Precautions:** 

   - Your safety is important to us. The Franka AI Companion is designed to be safe and effective. 

   - Power cables, power adapters, and other components can pose potential safety risks that may result in personal injury or property damage, especially if used improperly. 

   - To reduce these risks, follow the instructions in this user manual and observe all warnings on the Franka AI Companion and in this user manual. 

**4. Hazard Prevention:** 

   - By carefully following the information in this user manual and the information supplied with the Franka AI Companion, you can protect yourself from hazards and create a safer environment. 

   - Do not attempt to service the Franka AI Companion yourself unless instructed to do so by Franka Robotics GmbH or in this user manual. 

Franka Robotics GmbH © 

R82010/1.0/EN 

15 

GETTING STARTED WITH AI COMPANION 

## **5 GETTING STARTED WITH AI COMPANION** 

If this is your first time using AI Companion, please follow the Getting Started Guide. To begin, you need to complete the following setups: 

- Installation of AI Companion 

- Setting Up a Development Environment 

- Commissioning 

- Operation 

#### **5.1 Set up a development environment** 

###### **_5.1.1 Visual Studio Code for AI companion_** 

The AI companion is compatible with Visual Studio Code (VS Code), as well as other IDEs. 

###### **_5.1.2 Development with Visual Studio Code via Remote SSH_** 

**Visual Studio Code** offers an efficient and convenient way to access the development environment of the AI Companion. By using remote SSH and Docker functionality, you can develop directly within the AI Companion's containers. 

###### **Prerequisites** 

1. **Visual Studio Code** is installed on your local system. 

2. **Remote - SSH** extension installed in Visual Studio Code. 

###### **Steps to Connect** 

1. **Set Up SSH Connection** : 

   - Open the command palette in Visual Studio Code. 

   - Select **Remote SSH: Connect to Host** . 

   - Enter the connection data: ssh franka@<IP address of the AI Companion>. 

   - Authenticate with your access credentials. 

2. **Access Containers** : 

   - Use the Docker extension in the sidebar to manage containers. 

   - Start or stop containers as needed. 

   - Select the desired container and connect Visual Studio Code to it using the Attach Visual Studio Code option. 

**3. Development Environment** 

   - A new window will open, giving you direct access to all files and functions within the container. 

Franka Robotics GmbH © 

R82010/1.0/EN 

16 

GETTING STARTED WITH AI COMPANION 

- Develop, test, and debug your applications with changes saved directly in the container. 

- Use the integrated terminal for container-specific commands. 

###### **Benefits** 

- **Efficiency** : Develop in an isolated, containerized environment. 

- **User-Friendly** : Leverage the familiar functions and interface of Visual Studio Code. 

##### **5.2 Assembly and Installation of AI Companion** 

###### **Suitable installation location** 

- **_5.2.1 Compatible Franka robot systems_** 

   - Franka Emika robot (discontinued) 

   - Franka Research 3 

###### **_5.2.2 Ambient conditions_** 

###### **Installation location** 

- Indoors, in enclosed buildings 

- Not exposed to direct sunlight 

- No vibrations 

- External magnetic fields are only permitted equivalent to the Earth’s magnetic field 

###### **Ambient medium** 

- Air 

- Free of flammable substances (dust, gas, liquid) 

- Free of aggressive media 

- Free of corrosive substances 

- Free of “flying parts” 

- Free of spray liquids 

- Free of pressurised air currents 

###### **_5.2.3 Ambient temperature_** 

- +15°C to 25°C (typical) 

- +5°C to 45°C (extended) 

- -10°C to 60°C (transport) 

- +5°C to 25°C (storage) 

- Relative humidity 20–80%, non-condensing 

Franka Robotics GmbH © 

R82010/1.0/EN 

17 

GETTING STARTED WITH AI COMPANION 

##### **5.3 Assembly of the AI companion** 

The AI Companion can be positioned as a desktop solution on a stable surface. Make sure that the AI Companion does not move uncontrollably during operation due to vibrations in the surface it is resting on. 

You can attach the AI Companion at various fastening points. The fastening points can be found in the technical drawing technical specifications of this manual. Further fastening options can be found in the original operating manual from the manufacturer. 

##### **5.4 Wiring to a Franka robot system** 

###### **_NOTE_** 

###### **Property damage to the AI Companion** 

Connecting or disconnecting live cables or plugs during operation may cause damage to the AI Companion or the robot system. 

- Never connect or disconnect the AI Companion until the AI Companion or a compatible Franka Robotics robot is safely disconnected from the mains. 



Fig. 8.1 Overview of wiring 

###### **Prerequisites** 

- Robot is up and running i.e. FR3 

- PC for remote access, alternatively screen and keyboard/mouse for direct access 

###### **Procedure** 

~~1. Connect the supplied mains adapter to the A3 power supply of the AI Companion.~~ 

Franka Robotics GmbH © 

R82010/1.0/EN 

18 

GETTING STARTED WITH AI COMPANION 

If you use an alternative power supply, you can find the assignment of the connection socket in section Chapter 1 section 1.2 Device overview. 

2. Connect the controller of the Franka Research 3 (C3) to the Ethernet port (A1) of the AI Companion. 

3. If necessary, connect the AI Companion to a network or the internet via the port (A2) 

4. Setup using direct access 

   - Connect a monitor to the HDMI port (A4) of the AI Companion 

   - Connect a keyboard to one of the USB ports (A5) 

   - Connect a mouse to one of the USB ports (A5) 

5. Remote access facility, direct 

   - Connect your PC to one of the USB ports (A5 / A6) using the AI Companion’s Ethernet port (A2) or a USB Ethernet adapter 

6. Remote access facility, network 

   - Connect the Ethernet port (A2) to your network and make sure that your PC is on the same network as the AI Companion 

7. Assign the IO interface 

An RS232 or RS422 interface or a CAN bus can be accessed via the IO interface (A7). 

You will find the assignment of the A7 interface in Chapter 1 section 1.2 Device overview. 

###### **_NOTE_** 

Please note that to achieve the best performance, no switch may be connected between the AI Companion and the robot. 

##### **5.5 Grounding** 

**1. Ground Your Workplace:** 

   - Use antistatic mats. 

   - Ground yourself with a wrist strap. 

2. **Use Conductive Tools** : 

   - Only use tools that are conductive when working on the Franka AI Companion. 

3. **Handle Components Properly** : 

   - Always touch electrostatically endangered components at the edges. 

   - Preferably wear conductive gloves. 

4. **Disconnect Power Cable** : 

   - Disconnect the power cable from the Franka AI Companion before connecting or removing cables or inserting or removing expansion cards. 

5. **Avoid Touching Contacts** : 

   - ~~Do not touch the contacts of plugs.~~ 

Franka Robotics GmbH © 

R82010/1.0/EN 

19 

GETTING STARTED WITH AI COMPANION 

6. **Maintain Clean Work Environment** : 

   - Keep your work environment clean and free of non-conductive materials. 

#### **5.6 COMMISSIONING** 

###### **Prerequisites** 

The AI Companion is connected to the power supply and connected in accordance with the connection diagram. For the following steps, the AI Companion can be accessed either via direct access or remote access. 

###### **_5.6.1 Direct access_** 

- For direct access, you need to connect an HDMI-enabled screen, a keyboard, and optionally a mouse. 

- Note that the AI Companion only has type C USB ports. 

- You can now perform all the functions of the AI Companion ... 

###### **_5.6.2 Access data_** 

- Username: franka 

- Password: franka123 

###### **_5.6.3 Remote access_** 

For remote access, you need a network-enabled PC. Remote access via the network is possible in two ways: 

- Access by SSH: to enable this, the corresponding software, i.e. an SSH client, must be installed on the PC. 

- Access via the web interface: to enable this, an up-to-date browser must be installed on your PC. 

###### **Procedure** 

1. First, all integrated devices must be switched on. In the case of direct access, the connected screen must also be switched on. In the case of remote access, the additional PC must be switched on. Wait for the robot, AI Companion and all other connected devices to power up and be ready. 

- In the case of remote access, the network of the additional PC must be configured as a DHCP client. In addition, a web browser must be opened. 

- In the case of direct access, the web browser must be opened on the AI Companion. 

2. Open WebUI: 

   - On the connected PC, open a compatible web browser and enter the following in the address line: : localhost@<IP address of the AI Companion>. 

   - In the case of direct access, open a web browser on the AI Companion and enter the following in the address line: localhost@<IP address of the AI Companion>. 

3. On the WebUI, 

You can now navigate to the network configuration using the tabs in the upper part of the window. Here, the network connections of the AI Companion can be configured as desired. More detailed information can be found in 10.1.2. 

Franka Robotics GmbH © 

R82010/1.0/EN 

20 

GETTING STARTED WITH AI COMPANION 

#### **5.7 OPERATION** 

###### **_5.7.1 Overview of the functional structure of the AI companion_** 

###### **Software components** 

The software of the AI Companion consists of three separate areas, 

- Base OS layer 

- Application layer 

- User layer 

The functions and properties of the three areas are described below. 

###### **_5.7.2 Base OS layer_** 

The Base OS layer represents the Linux-based operating system of the AI Companion. It is a special Linux derivative (Linux for Tegra, L4T), which is distributed by NVIDIA. A PREEMPT real-time kernel is used to guarantee maximum compatibility with the FR3. The Base OS layer manages all hardware drivers for e.g. cameras and other devices, as well as an NVIDIA CUDA installation. The user has no administrative rights on the Base OS and can neither install nor remove programs. 

###### **_5.7.3 Application layer_** 

The Application layer comprises several applications provided directly by Franka Robotics that simplify the use of the AI Companion. These applications include: 

1. AI Companion Web UI: an intuitive web browser-based, graphical user interface that provides access to various functions. A detailed description can be found below. 

2. Desk Forwarding: if the AI Companion is connected to the master controller and thus blocks the only network connection, Desk can still be reached by navigating to <> in the browser. The prerequisite for this is that the device with the browser is on the same network as the AI Companion. 

3. DHCP server: the AI Companion has the option of configuring one of its network interfaces as a DHCP server. 

###### **_5.7.4 User layer_** 

The User layer represents the development environment for the user. The core of this is the applications. An application is an isolated environment in which the user can install and edit software at will in a dedicated Docker development container, if it does not conflict with the Base OS layer. Additional Docker containers can be added, which are then started, stopped etc. together as part of an application. 

###### **_5.7.5 Web UI_** 

The AI Companion’s Web UI offers various options for configuring and operating the system. Currently, it is possible to configure network connections, update the system, and start and stop Docker containers. 

###### **_5.7.6 Network configuration_** 

You can flexibly adjust the network configuration of your device via the Web UI. The following options are available: 

**Setting manual IP addresses:** fixed IP addresses can be configured for each available network interface. 

**Activating DHCP client mode:** have your device automatically obtain an IP address from a DHCP server on the network to simplify network setup. 

Franka Robotics GmbH © 

R82010/1.0/EN 

21 

GETTING STARTED WITH AI COMPANION 

**Starting a DHCP server for the network interface enP1p1s0** : set up a DHCP server on the network interface enP1p1s0 to automatically assign IP addresses to other devices on the network. This makes it easier to connect to other PCs or a robot in DHCP client mode. 

**_NOTE_** 

Please note that changes to the network settings may affect the connection to other devices. Make sure you understand the changes or consult a network administrator. 

###### **_5.7.7 System update_** 

Franka Robotics provides you with an update file that allows you to update your device to the latest version. On the “Settings” tab, you will find the “Update” option. Here you can upload the update file and execute the update. 

###### **_5.7.8 Docker container_** 

The dashboard tab is the central element for monitoring and managing the containers on the device. 

**Container overview** : the dashboard displays all available containers on the device, each represented by its own tile. 

**Container management** : in each tile you have the option of starting, stopping or deleting the respective container. These functions allow efficient and flexible management of your containers. 

###### **_5.7.9 Desk forwarding_** 

It is possible to access Desk directly via the AI Companion. To do this, enter the following in the address bar of the browser of a connected terminal: https://<ai-companion-url>/desk where you replace <ai-companion-url> with the IP of the AI Companion. 

###### **_5.7.10 Digital IOs_** 

The IO port A7 of the AI Companion features two digital inputs and two digital outputs: 

|**Pin name**|**Pin of IO**<br>**port A7**|**Linux sysfs**<br>**number**|**Linux GPIO**<br>**name**|**BCM pin**<br>**number**|**Note**|
|---|---|---|---|---|---|
|DIGITAL_IN1|12|470|PY.00|27|High at 11-24V, rated for 2.25mA|
|DIGITAL_IN0|14|471|PY.01|25|High at 11-24V, rated for 2.25mA|
|DIGITAL_OUT0|13|472|PY.02|26|max 24V, max 1A, low-side switch mechanism|
|DIGITAL_OUT1|11|473|PY.03|24|max 24V, max 1A, low-side switch mechanism|



Inside a Docker container, you can access and control these pins using the Linux GPIO character device interface or the deprecated Linux GPIO sysfs interface. The GPIO character device interface can used e.g. with the “libgpiod” package (C library, CLI tools, Python bindings) or the “Jetson.GPIO” Python library. Please refer to their respective documentation and the information in the pinout table above. 

Depending on which interface/library you want to use in your container, you need to run the container in privileged mode and/or pass it the “gpiochip0” device. One way to do this is to add the following entries to the `devcontainer.json` file of your Visual Studio Code Dev Container: 

```
"remoteUser": "root",
"runArgs": [
    "--privileged",
    "--device", "/dev/gpiochip0"
```

```
],
```

Franka Robotics GmbH © 

R82010/1.0/EN 

22 

GETTING STARTED WITH AI COMPANION 

###### **_5.7.11 CAN bus interface_** 

The IO port A7 of the AI Companion features pins to connect CAN High (pin 5) and CAN Low (pin 7), see Section 1.2 Device overview. 

You can bring the interface up inside a Docker container by running the following command (adapt the bitrate according to your application): 

```
ip link set can0 up type can bitrate 1000000
```

##### **5.8 Benefits of the development environment** 

The development environment of the AI Companion is based on a modern Docker infrastructure that enables flexible and efficient containerisation. This architecture allows developers to run different containers in parallel and link them seamlessly without having to deal with the complexities of dependencies on the base operating system. 

###### **Robot operation with FCI (Franka Control Interface)** 

Operating the robot using the Franka Control Interface (FCI) first requires activation in the Desk environment. After successful activation, you can control the robot via both the Libfranka library and via ROS (Robot Operating System). These interfaces allow precise control and flexible programming of the robot system. Special attention and care are needed when using the FCI. Unlike standard Desk operation, FCI allows for more direct control of the robot, which can create additional safety risks. 



###### **CAUTION** 

Make sure you are aware of the responsibility and have taken all necessary safety precautions before operating the robot via FCI. 

###### **_NOTE_** 

If you have any questions about safe use of the FCI, please consult the appropriate safety documentation or contact our technical support. 

###### **_NOTE_** 

Always observe the applicable safety guidelines and carry out a thorough risk assessment before each commissioning. 

##### **5.9 Extended configuration** 

###### **_5.9.1 Network configuration_** 

The AI Service Box is equipped with two Ethernet interfaces: 

**enP8p1s0 (left Ethernet port, next to HDMI)** 

- This is the primary interface to the left of the two Ethernet ports. 

- It is used to connect the AI Companion with your company or laboratory network. 

- This interface is configured as a **DHCP client** by default, which means that it automatically receives an IP address from your network. 

**enP1p1s0 (right Ethernet port, next to the power supply)** 

- This interface on the right side is intended for direct connection with the main control unit of your robot. 

- `o` It is set up as a **DHCP server** by default and uses the IP address **192.168.19.1/24** . `o` Any robot or PC configured as a DHCP client and connected to this interface will automatically receive 

Franka Robotics GmbH © 

R82010/1.0/EN 

23 

GETTING STARTED WITH AI COMPANION 

the IP address **192.168.19.2/24** . 

###### **Connection options during initial setup** 

There are three possible scenarios for the connection: 

###### **_NOTE_** 

When setting up for the first time, make sure that your PC is either connected to the same network as the AI Companion or connected directly via an Ethernet cable 

1. **Connection over a network** : If the AI Companion is connected to a network via the enP8p1s0 interface in DHCP client mode, it automatically receives an IP address from the network’s DHCP server. Check with your IT department whether you need to register the AI Companion in the local firewall or on the network to gain full access. 

2. **Direct connection to the AI Companion** : connects your PC directly to the enP1p1s0 interface of the AI Companion. Make sure that your PC is configured as a DHCP client. Since the AI Companion acts as a DHCP server on this interface, your PC automatically receives an IP address. This allows direct communication between your PC and the AI Companion without additional configuration. 

3. **Manual IP address configuration** : if manual network setup is required, perform the following steps: 

   - **Connecting the monitor and input devices** : connect a monitor, keyboard, and mouse to the AI Companion to access the Ubuntu desktop interface. 

   - **Access network settings** : 

      - Log in to the Ubuntu desktop with the username franka and the password franka123. 

      - Click the network icon in the system tray and select “Network Settings”. 

         **1. Selecting the network interface:** 

            - Select the enP8p1s0 interface from the list of available network interfaces for manual configuration. 

         **2. Entering network information:** 

            - Configure the IP address, subnet mask, gateway and DNS server according to your network requirements. 

            - Make sure that the entered data is correct and matches your network environment. 

         **3. Applying the settings:** 

            - Save the changes and close the network settings. 

            - Check whether the AI Companion is now available on the network with the desired IP address. 

These steps allow you to manually configure the AI Companion’s network settings from the Ubuntu desktop interface and customise it to your specific network requirements. 

###### **_NOTE_** 

Changes to the network settings may affect the connection to other devices. Please back up important data in advance and consult your IT department or a network administrator if necessary to ensure that the configuration is carried out correctly. 

Franka Robotics GmbH © 

R82010/1.0/EN 

24 

TECHNICAL SPECIFICATIONS 

## **6 TECHNICAL SPECIFICATIONS** 

|**Description**|**Values**|
|---|---|
|**System equipment**||
|System|Jetson Orin NX Module|
|Memory|16 GB 128-bit LPDDR5|
|Memory capacity|500 GB SSD|
|Connections|2x Gigabit Ethernet|
||2x USB 3.1 Type A|
||1x CAN BUS|
||1x RS232 & 1x RS422|
||1x Micro-USB 2.0 (Recovery)|
||2x Digital Input|
||2x Digital Output|
||1x HDMI 2.0 (max. resolution 3840x2169)|
|Operating system|Ubuntu Linux 20.04|
|<br>**Power supply**||
|Operating voltage|9 to 28 V DC|
|Current consumption|1.6 A|
|**Ambient conditions**||
|Temperature|5°C to +45°C|
|Humidity|20–80%, non-condensing|
|**Physical data**||
|Dimensions [mm]|L: 110 / W: 130 / H: 60|
|Weight|760 g|



Franka Robotics GmbH © 

R82010/1.0/EN 

25 

TECHNICAL SPECIFICATIONS 



Figure 5:Dimensions 

Franka Robotics GmbH © 

R82010/1.0/EN 

26 

SCOPE OF DELIVERY AND ADDITIONAL EQUIPMENT 

## **7 SCOPE OF DELIVERY AND ADDITIONAL EQUIPMENT** 

##### **7.1 Included in scope of delivery** 

- 1x AI Companion 

- 1x mains adapter 

- 1x connector for non-heating apparatus (country-specific) 

- 1x Ethernet cable (Cat 6a 1m) 

- 1x information sheet on online documentation 











Figure 6:Scope of delivery of AI Companion 

##### **7.2 Not included in the scope of delivery** 

The following components are not included: 

- Operating devices 

   - Notebook/PC (remote access) 

The operating device should be a network-enabled PC, equipped with an internet browser (Chrome, Edge, or Firefox) and preferably have VS Code installed. 

   - Monitor with HD resolution (optional for direct access) 

   - Keyboard (optional for direct access) 

   - Mouse (optional for direct access) 

- Material 

   - Ethernet cable with RJ45 connector for connecting the system to the internet / shop floor network 

   - Ethernet cable with RJ45 connector for optional connection of the controller to the company network or the workstation PC 

   - Fasteners 

   - Connector for assigning the interface A 

Franka Robotics GmbH © 

R82010/1.0/EN 

27 

SERVICE AND SUPPORT 

## **8 SERVICE AND SUPPORT** 

Please visit our website www.franka.de for the latest product documentation, drivers, utilities and technical support. You can register on our website franka.world to gain access to limited information and automatic updating services. 

For direct technical support, please contact our FAE team at support@franka.de. Our FAE team can also assist you with additional information not found on our website. 

**_NOTE_** 

For all other service and support inquiries, please contact us at support@franka.de. In our service and support centre, a ticket will be created for your request, and our experts will respond to you as soon as possible. Please visit https://franka.world for additional material and more information about our robots. 

##### **8.1 Update** 

###### **_8.1.1 Prerequisites_** 

- The AI Companion is switched on and connected to the internet. 

- You have access to the web interface of the AI Companion with one device. 

- A newer version is available for the Base OS of the AI Companion. 

###### **_8.1.2 Procedure_** 

To update your AI Companion to the latest version, we provide you with a special download link where you can obtain the current update file. First, download this file to your local system. Then open the WebUI of your AI Companion and navigate to the “Settings” area. There you will find the menu item “Update”. In this area, you can upload the previously downloaded update file via the upload function and start the update process. 

During the update, it is essential that the AI Companion is continuously supplied with power and that the process is not interrupted. We also recommend backing up important data before updating. Upon successful completion of the update, a reboot of the system may be required to enable all changes. If problems occur during the update process, our technical support is available to you. 

Franka Robotics GmbH © 

R82010/1.0/EN 

28 

MAINTENANCE 

## **9 MAINTENANCE** 

##### **9.1 Cleaning** 



###### **DANGER** 

###### **Risk of electric shock** 

Improper use of liquid cleaning agents and improper disconnection of the devices from the mains can lead to fatal accidents. 

- Do not clean devices that have not been safely disconnected from the mains. 

- Do not use liquid detergents to clean the equipment. 

- Do not switch on devices that have not yet completely dried. 

The following must be considered when cleaning: 

- Cleaning may only be carried out by qualified personnel. 

- Cleaning of components is only permitted if the AI Companion and the compatible robot from Franka Robotics are safely disconnected from the power supply (controller disconnected from the mains). 

- Do not spray liquids directly onto the device. 

- Do not use chemical cleaning agents. 

- The components may only be cleaned with a dry cloth. Make sure that no moisture gets into the devices. 

**_NOTE_** 

**Material damage to the AI Companion** 

Do not use liquid detergents to clean the AI Companion. 

##### **9.2 Disposal** 

The AI Companion may only be disposed of in accordance with the respective country-specific laws, regulations and regulations. 

##### **9.3 Returning packaging waste** 

Please contact Franka Robotics to return packaging waste. 

Franka Robotics GmbH © 

R82010/1.0/EN 

29 

## **10 LIST OF FIGURES** 

|Figure 1: AI Companion....................................................................................................................................................................................... 6|
|---|
|Figure 2: Device overview and connections................................................................................................................................................... 6|
|Figure 3: Power supply assignment (A3)........................................................................................................................................................ 7|
|Figure 4: Assignment of IO interface (A7)....................................................................................................................................................... 8|
|Figure 5: Dimensions........................................................................................................................................................................................ 26|
|Figure 6: Scope of delivery of AI Companion.............................................................................................................................................. 27|



Franka Robotics GmbH © 

R82010/1.0/EN 

30 

## **11 INDEX** 

|Additional equipment .......................................... 14|
|---|
|Ambient temperature .......................................... 15|
|Arm .......................................................................... 25|
|Assembly ................................................................ 16|
|Cleaning .................................................................. 23|
|Connecting cable .................................................. 25|
|Device overview ................................................... 13|
|Disposal .................................................................. 23|
|Franka Robotics GmbH ......................................... 2|
|Franka UI ........................................................... 6, 25|
|Guidance/manual guidance ................................ 25|
|Improper use ............................................................ 9|
|Installation .............................................................. 15|
|Ambient conditions ........................................... 15|
|Relative humidity ............................................... 15|



|Intended use............................................................. 9|
|---|
|Liability notes ........................................................... 9|
|Operating device .................................................. 14|
|Rights of use ............................................................. 6|
|Safety ......................................................................... 8|
|Improper use ......................................................... 9|
|Intended use ......................................................... 9|
|Liability notes........................................................ 9|
|Service ............................................................. 21, 23|
|Technical data ....................................................... 11|
|Troubleshooting ............................................ 21, 25|
|Effector settings ................................................ 25|
|Restart ................................................................. 25|



Franka Robotics GmbH © 

R82010/1.0/EN 

31 

Franka Robotics GmbH Frei-Otto-Strasse 20 80797 Munich Germany 

