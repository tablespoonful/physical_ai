> **[PDF を開く](<Product Manual Franka Research 3_R02210_1.4_EN.pdf>)**
>
> PDF から自動変換した本文です。図は含まず、表は崩れている場合があります。安全や仕様の確認には PDF を使ってください。

[Hier eingeben] 





# **FRANKA RESEARCH 3** 

### **Product Manual** 

April 2022 

Franka Robotics GmbH © 1 

TRANSLATION FROM ORIGINAL PRODUCT MANUAL 

© Copyright 2025 Franka Robotics GmbH Frei-Otto-Straße 20 80797 Munich Germany 

This document and extracts of it may only be reproduced or made available to third parties with the explicit authorization of Franka Robotics GmbH. 

The content of this document has been carefully checked against compliance with the hardware and software described. However, discrepancies cannot entirely be ruled out, which is why we assume no liability for complete compliance. 

In the interest of our customers, we reserve the right to undertake improvements and corrections to hardware, software, and documentation at any point in time without notice. 

We are always grateful for your feedback at documentation@franka.de. 

The German documentation is the ORIGINAL DOCUMENTATION. Other languages are translations of the original document. 

Complementary documents to this product manual are: 

- Datasheet Franka Research 3 (Document number: R02212) 

- Quick Guide for Installation FR3 (Document number: R02040) 

Document name:                Product Manual Franka Research 3 

Document number: R02210 Release Version: 1.4 (May 2025), valid for Franka Research 3 with system version 5.7.0 

Change Log: 

|**Release Version**|**Release Date**|**Changes**|
|---|---|---|
|1.0|March. 2024|First Release Franka Robotics branding|
|1.1|September 2024|Adjustments for system version 5.4.0|
|1.1.1|December 2024|Corrected safety functions|
|1.2|March 2025|Adjustments for system version 5.5.0 New feature Import/Export in Safety configuration|
|1.3|April 2025|Adjustments for system version 5.6.0 Updated images of Execution operating mode|
|1.4|May 2025|Adjustments for system version 5.7.0 Updated images of Network Settings UI and Rescue System|





Get your manual and additional supporting material in English and other languages at <u>www.franka.de/documents.</u> 

## **TABLE OF CONTENTS** 

|1<br>ABO|UT FRANKA ROBOTICS .......................................................................................................................................... 7|
|---|---|
|2<br>RIG|HTS OF USE AND PROPERTY RIGHTS.................................................................................................................. 8|
|2.1|General...................................................................................................................................................................... 8|
|2.2|Identification ............................................................................................................................................................ 8|
|3<br>DEC|LARATION OF INCORPORATION AND CERTIFICATES .................................................................................. 9|
|3.1|Declaration of Incorporation ................................................................................................................................ 9|
|3.2|Certificates ............................................................................................................................................................ 11|
|3.3|Further Statements ............................................................................................................................................. 11|
|3.3.1|RoHS / REACH / WEEE / Battery Directive .................................................................................................. 11|
|3.3.2|China RoHS 2 ....................................................................................................................................................... 12|
|3.4|Labeling on the Equipment ................................................................................................................................ 13|
|4<br>SAF|ETY ...............................................................................................................................................................................16|
|4.1|Safety Instructions and General Indications .................................................................................................. 16|
|4.2|Notice of Liability................................................................................................................................................. 17|
|4.3|Intended Use ........................................................................................................................................................ 17|
|4.4|Misuse .................................................................................................................................................................... 17|
|4.5|General Possible Dangers and Safety Measures when Working with Robots ........................................ 18|
|4.6|Application Related Possible Dangers and Safety Measures...................................................................... 20|
|4.7|Installation of Safety Peripherals ...................................................................................................................... 23|
|4.8|Fail-safe locking system ..................................................................................................................................... 24|
|4.9|Manually Moving the Arm ................................................................................................................................. 24|
|4.10|Safety Concept ..................................................................................................................................................... 26|
|4.11|Safety Functionalities ......................................................................................................................................... 29|
|4.12|Additional information for planning and initial installation of a robot system ........................................ 32|
|5<br>ROL|ES AND PERSONNEL ..............................................................................................................................................36|
|5.1|Personnel ............................................................................................................................................................... 36|
|5.2|User Roles ............................................................................................................................................................. 37|
|6<br>EQU|IPMENT OVERVIEW...............................................................................................................................................39|
|6.1|The Arm ................................................................................................................................................................. 40|
|6.2|Control ................................................................................................................................................................... 46|
|7<br>SCO|PE OF DELIVERY AND ADDITIONAL EQUIPMENT .......................................................................................48|
|7.1|Included in the box .............................................................................................................................................. 48|
|7.2|Not included in the box ...................................................................................................................................... 49|
|7.3|Available Spare Parts and Accessories ............................................................................................................ 49|
|8<br>TEC|HNICAL SPECIFICATIONS .....................................................................................................................................50|
|9<br>TRA|NSPORT AND HANDLING ....................................................................................................................................54|
|9.1|Ambient Conditions for Delivery and Transport ........................................................................................... 55|
|10<br>|MOUNTING AND INSTALLATION .......................................................................................................................56|
|10.1|Unpacking the Equipment.................................................................................................................................. 57|



R02210/1.4/EN 

Franka Robotics GmbH © 

3 

|10.2|Correct Installation Site ...................................................................................................................................... 61|
|---|---|
|10.2.1|Maximum-and safeguarded space .............................................................................................................. 61|
|10.2.2|Ambient conditions: Arm .............................................................................................................................. 62|
|10.2.3|Ambient conditions: Control ........................................................................................................................ 63|
|10.3|Preparing the Installation Site ........................................................................................................................... 65|
|10.3.1|Arm .................................................................................................................................................................... 65|
|10.3.2|Control .............................................................................................................................................................. 66|
|10.4|Mounting the Arm ............................................................................................................................................... 67|
|10.5|Positioning the Control....................................................................................................................................... 70|
|10.6|Wiring and Electrical Installation ...................................................................................................................... 71|
|10.6.1|Connection diagram ....................................................................................................................................... 72|
|10.6.2|Interfaces.......................................................................................................................................................... 72|
|10.6.3|Connecting the functional earth .................................................................................................................. 75|
|10.6.4|Wiring ............................................................................................................................................................... 76|
|10.7|Mounting End Effectors ..................................................................................................................................... 80|
|10.8|Practical Tips for Usage and Positioning of Franka Research 3 ................................................................. 82|
|10.8.1|Energy consumption ...................................................................................................................................... 82|
|10.8.2|ESD limits ......................................................................................................................................................... 83|
|10.8.3|Design of the workspace .............................................................................................................................. 83|
|10.8.4|Personal safety and ergonomics .................................................................................................................. 84|
|10.9|Re-packing the Arm ............................................................................................................................................. 87|
|11<br>|OPERATION ...............................................................................................................................................................90|
|11.1|Switching On ........................................................................................................................................................ 90|
|11.2|Safety Relevant Tests of Franka Research 3 .................................................................................................. 93|
|11.2.1|Self-test of the robotic system .................................................................................................................... 93|
|11.2.2|Regular testing of safety functions ............................................................................................................. 94|
|11.2.3|Testing the emergency stop ......................................................................................................................... 94|
|11.3|Initial configuration ............................................................................................................................................. 96|
|11.3.1|Connecting a User Interface Device ........................................................................................................... 96|
|11.3.2|Initial Configuration „First Start“ ................................................................................................................. 96|
|11.4|Setup of Franka Control Interface (FCI) ........................................................................................................ 101|
|11.4.1|Configuration of the network for control via FCI .................................................................................. 101|
|11.4.2|Setup of libfranka on a Linux workstation ............................................................................................... 103|
|11.4.3|Verification of communication .................................................................................................................. 108|
|11.5|Typical Usage...................................................................................................................................................... 110|
|11.6|Switching Off and Restarting .......................................................................................................................... 110|
|12<br>S|AFETY CONFIGURATION/WATCHMAN ...................................................................................................... 112|
|12.1|Watchman ........................................................................................................................................................... 112|
|12.2|Overview ............................................................................................................................................................. 112|
|12.3|Editing of the Safety Configuration ............................................................................................................... 114|
|12.4|Import/Export of Safety Settings ................................................................................................................... 116|



R02210/1.4/EN 

Franka Robotics GmbH © 

4 

|12.4.1|Import Procedure ......................................................................................................................................... 117|
|---|---|
|12.4.2|Export Procedure.......................................................................................................................................... 119|
|12.5|Safety Setup........................................................................................................................................................ 121|
|12.5.1|General Safety Settings ............................................................................................................................... 121|
|12.5.2|Safe Input Configuration ............................................................................................................................. 121|
|12.5.3|End Effector Configuration......................................................................................................................... 122|
|12.5.4|Creation of spheres for modelling an End Effector envelope ............................................................. 123|
|12.6|Creating and editing rules ................................................................................................................................ 125|
|12.6.1|Structure of a rule......................................................................................................................................... 125|
|12.7|Validate ................................................................................................................................................................ 128|
|13<br>W|ORKING WITH FRANKA RESEARCH 3 ........................................................................................................ 132|
|13.1|Robotic Basics .................................................................................................................................................... 132|
|13.2|Single Point of Control ..................................................................................................................................... 133|
|13.3|Operating Modes ............................................................................................................................................... 136|
|13.3.1|Programming ................................................................................................................................................. 137|
|13.3.2|Execution........................................................................................................................................................ 138|
|13.3.3|Overview of the status indicators ............................................................................................................. 139|
|13.3.4|Step-by-step overview of operating modes and corresponding status indicators ......................... 139|
|13.4|Work..................................................................................................................................................................... 141|
|13.5|Assist .................................................................................................................................................................... 143|
|13.6|Franka UI ............................................................................................................................................................. 145|
|13.6.1|Apps ................................................................................................................................................................ 151|
|13.6.2|Teach a Task .................................................................................................................................................. 151|
|13.6.3|Creating a Task.............................................................................................................................................. 151|
|13.6.4|Task settings .................................................................................................................................................. 152|
|13.6.5|Parameterization of Apps ........................................................................................................................... 152|
|13.6.6|Pose teaching ................................................................................................................................................ 153|
|13.6.7|Pose fine adjustment ................................................................................................................................... 154|
|13.6.8|Guiding configurations ................................................................................................................................ 155|
|13.6.9|Guiding............................................................................................................................................................ 158|
|13.6.10|Editing end effector settings ...................................................................................................................... 159|
|13.6.11|Test & Jog ...................................................................................................................................................... 159|
|13.7|Franka Control Interface (FCI) ........................................................................................................................ 161|
|13.7.1|Working in principle with the FCI interface ............................................................................................ 162|
|13.8|Troubleshooting ................................................................................................................................................. 165|
|13.8.1|General use .................................................................................................................................................... 165|
|13.8.2|Troubleshooting while using FCI ............................................................................................................... 173|
|14<br>M|ANAGING FRANKA RESEARCH 3.................................................................................................................. 174|
|14.1|Franka World ...................................................................................................................................................... 174|
|14.2|Managing Apps and Updates .......................................................................................................................... 174|
|14.3|Hub ....................................................................................................................................................................... 175|



R02210/1.4/EN 

Franka Robotics GmbH © 

5 

|14.4|Updates................................................................................................................................................................ 176|
|---|---|
|14.5|Backup ................................................................................................................................................................. 177|
|14.5.1|Safety Configuration .................................................................................................................................... 177|
|14.5.2|Network Setting ............................................................................................................................................ 178|
|14.5.3|Modbus Configuration................................................................................................................................. 178|
|14.5.4|End Effector Configuration......................................................................................................................... 178|
|14.5.5|Saving of the created Tasks ........................................................................................................................ 179|
|15<br>|MAINTENANCE AND DISPOSAL ....................................................................................................................... 180|
|15.1|Maintenance ....................................................................................................................................................... 180|
|15.2|Cleaning ............................................................................................................................................................... 180|
|15.3|Disposal ............................................................................................................................................................... 181|
|16<br>|SERVICE AND SUPPORT ..................................................................................................................................... 182|
|16.1|Rescue System ................................................................................................................................................... 182|
|16.2|Hardware Exchange .......................................................................................................................................... 185|
|16.2.1|Replacing the Control .................................................................................................................................. 186|
|17<br>|APPENDIX ............................................................................................................................................................... 190|
|17.1|Stopping Times and Distances ........................................................................................................................ 190|
|17.2|Stop Category 1 ................................................................................................................................................. 191|
|17.2.1|Joint 1 ............................................................................................................................................................. 191|
|17.2.2|Joint 2 ............................................................................................................................................................. 193|
|17.2.3|Joint 3 ............................................................................................................................................................. 195|
|17.2.4|Joint 4 ............................................................................................................................................................. 197|
|17.3|Stop Category 2 ................................................................................................................................................. 199|
|17.3.1|Joint 1 ............................................................................................................................................................. 199|
|17.3.2|Joint 2 ............................................................................................................................................................. 201|
|17.3.3|Joint 3 ............................................................................................................................................................. 203|
|17.3.4|Joint 4 ............................................................................................................................................................. 205|
|17.4|Response times .................................................................................................................................................. 207|
|17.5|Safe Position Accuracy ..................................................................................................................................... 207|
|18<br>|GLOSSARY ............................................................................................................................................................... 208|
|19<br>I|NDEX ....................................................................................................................................................................... 213|
|20<br>|TABLE OF FIGURES ............................................................................................................................................... 216|



R02210/1.4/EN 

Franka Robotics GmbH © 

6 

ABOUT FRANKA ROBOTICS 

## **1 ABOUT FRANKA ROBOTICS** 



##### **Enabling industrial automation** 

Founded in 2016, Franka is a robotics platform company based in Munich with manufacturing facilities in Bavaria. 

The Franka robot platform is extensively used in research and beyond, due to its unique control interface, humanlike sense of touch technology, and large community of robotics and AI researchers and disruptors. 

Since November 2023, Franka Robotics has been a part of Agile Robots AG, representing a powerful alliance of experts in the industry. Together, we strive to advance innovation in research and industrial automation shaping the future of robotics. 

Designed, developed, manufactured and serviced in Germany. 

##### **Introducing Franka World – a digital robotics platform** 

After redefining robotics and establishing a community, we launched a novel digital robotics platform to interconnect the digital world with the physical world. 

Franka World allows community interaction between researchers, partners, customers, developers, suppliers, and robots. In addition, all users can easily gain integrated access to products and services and manage their entire robot fleets, independent of their physical location. Franka World also allows for easy robot deployment and updating. 

We strive for a world where everyone can use a robot, and we can reach that by connecting the world. We treasure our community of robotics professionals, academics, and enthusiasts, from whom we learn every single day. 

As members of the community ourselves, we commit to supporting each other and thriving together. Franka Robotics – a certified robotics platform with tactile intelligence. 

R02210/1.4/EN 

Franka Robotics GmbH © 

7 

RIGHTS OF USE AND PROPERTY RIGHTS 

## **2 RIGHTS OF USE AND PROPERTY RIGHTS** 

#### **2.1 General** 

###### **Protected trademarks** 

This product manual refers to protected trademarks not explicitly designated in the continuing text. The absence of such indication may not imply that the corresponding product name is free of third-party rights. The following trademarks are protected trademarks: 

Franka and Franka Robotics are registered trademarks. 

Microsoft is a registered trademark, and Windows is an indication of the Microsoft Corporation in the United States and other countries. 

GOOGLE, Mozilla, Firefox, CHROME, ITEM are registered trademarks. 

###### **Trademark rights** 

The responsible person is not granted any rights or claims to the trademark, logo, or trade names of Franka Robotics. 

###### **Use of open-source code** 

A complete list of all open-source licenses used by Franka Research 3 can be accessed via the Settings menu of the Franka UI. 

#### **2.2 Identification** 

###### **Removal of identification** 

Copyright notices, serial numbers, and any other labeling that identifies the product or operating software may not be removed or modified. 

R02210/1.4/EN 

Franka Robotics GmbH © 

8 

DECLARATION OF INCORPORATION AND CERTIFICATES 

## **3 DECLARATION OF INCORPORATION AND CERTIFICATES** 

#### **3.1 Declaration of Incorporation** 



R02210/1.4/EN 

Franka Robotics GmbH © 

9 

DECLARATION OF INCORPORATION AND CERTIFICATES 



R02210/1.4/EN 

Franka Robotics GmbH © 

10 

DECLARATION OF INCORPORATION AND CERTIFICATES 

<u>www.franka.de/documents</u> 

#### **3.2 Certificates** 

Certificates by TÜV SÜD RAIL and TÜV SÜD PS can be found under the following link: 

#### **3.3 Further Statements** 

##### **3.3.1 RoHS / REACH / WEEE / Battery Directive** 

Further Information 

**status: 01.04.2022 Franka Research 3** 

**Restriction of Hazardous Substances (RoHS):** 

The  components _Control and Arm_ do not fall within the scope of EU RoHS Directive 2011/65/EU but still meet the requirements of the restricted substances and maximum concentration values that are allowed in homogenous materials: 

- Lead (0.1 %) 

- • Mercury (0.1 %) 

- Cadmium (0.01 %) 

- Hexavalent chromium (0.1 %) 

- Polybrominated biphenyls (PBB) (0.1 %) 

- Polybrominated diphenyl ethers (PBDE) (0.1 %) 

The following exceptions are also applied: 

6a: Lead as an alloying element in steel for machining purposes and in galvanized steel containing up to 0.35 % lead by weight 

6b: Lead as an alloying element in aluminum containing up to 0.4 % lead by weight 

6c: Copper alloy containing up to 4 % lead by weight 

7a: Lead in high melting temperature type solders (i.e., lead-based alloys containing 85 % by weight or more lead) 

7c-I: Electrical and electronic components containing lead in a glass or ceramic other than dielectric ceramic <u>in capacitors, e.g., piezo-electronic devices, or in a glass or ceramic matrix compound</u> **REACH:** 

_FRANKA ROBOTICS GmbH_ is a "downstream user" as defined in REACH. Our products are exclusively nonchemical products (manufactured items). In addition, no substances are released under normal conditions of use and conditions that can reasonably be predicted (Article 7, REACH). 

We confirm that our products do not contain more than 0.1 percent by mass of any of the listed substances on the published ECHA candidate list (SVHC) unless covered by RoHS exceptions (see above). Extensions published by the ECHA candidate list are matched with our products, and if it is known that one of these newly added substances is contained in our products, we will inform you immediately. <u>This confirmation was created based on currently available information from our suppliers.</u> **WEEE Directive:** 

The components _Control and Arm_ are not subject to the WEEE Directive 2002/96/EC for collection, recycling, and recovery for electrical goods. 

R02210/1.4/EN 

Franka Robotics GmbH © 

11 

###### DECLARATION OF INCORPORATION AND CERTIFICATES 

###### **Battery Directive:** 

The product Control contains a BIOS battery. 

###### Disposal of batteries: 

There is an obligation to return rechargeable and non-rechargeable batteries by Battery Directive 2006/66/EC; do not dispose of them with consumer waste. Dispose of them according to statutory orders and bring them to a recycler. Batteries will be recycled. The signs below the crossed-out trashcan indicate the substances lead (Pb), cadmium (Cd), or mercury (Hg). 



##### **3.3.2 China RoHS 2** 



|||**Toxic and Hazard**|**ous Substances an**|**d Elements /**有毒|和有害的物质和|元素|
|---|---|---|---|---|---|---|
|**Part Name**<br>`部件名称`|**Lead**<br>铅<br>**(Pb)**|**Mercury**<br>汞<br>**(Hg)**|**Cadmium**<br>镉<br>**(Cd)**|**Hexavalent**<br>**Chromium**<br>六价铬<br>**(Cr (VI))**|**Polybrominate**<br>**d biphenyls**<br>多溴联苯<br>**(PBB)**|**Polybrominated**<br>**diphenyl ethers**<br>多溴二苯醚<br>**(PBDE)**|
|Control<br>`控制器`|X|O|O|O|O|O|
|Arm FP3<br>`臂架 FP3`|X|O|O|O|O|O|
|Robot Connecting<br>Cable<br>连接线<br>2,5m/5m/10m|O|O|O|O|O|O|
|Emergency Stop<br>Device<br>紧`急停止装置`|O|O|O|O|O|O|
|External Enabling<br>Device<br>`外部支持`设备|O|O|O|O|O|O|



<u>This Table is prepared in accordance with the provisions of SJ/T 11364-2006.</u> <u>`本表根据` SJ/T 11364-2006</u> <u>`的` 规定编制。</u> 

**O** : Indicates that said hazardous substance contained in all of the homogeneous materials for this part is below the limit requirement of GB/T 26572-2011. 

O: `表示` 该部分所有均质材料中的所述有害物质低于 GB/T 26572-2011 `的限量要求。` 

**X:** indicates that said hazardous substance contained in at least one of the homogenous materials used for this part is above the limit requirement of GB/T 26572-2011 

X: `表示本` 试验用同质材料中至少有一种所含的有害物质高于 GB/T 26572-2011 `的限量要求。` 

(Enterprises may further provide in this box technical explanation for marking “X” based on their actual circumstances) ( `企` 业可根据自己的实际情况，在此框中进一步提供标示 "X " `的技` 术解释) 

R02210/1.4/EN 

Franka Robotics GmbH © 

12 

###### DECLARATION OF INCORPORATION AND CERTIFICATES 

#### **3.4 Labeling on the Equipment** 

##### **Arm** 

###### **Type label** 



Fig. 3.1: Type label 

###### **Emergency unlock label** 

Three Emergency Unlock Labels on the Arm point to the insertion points where the Emergency Unlocking Tool needs to be inserted to manually unlock the fail-safe locking system in case of an emergency. 



Fig. 3.2: Emergency unlock label 



###### **WARNING** 

**Falling heavy Arm when using Emergency Unlocking Tool** 

- Risk of being trapped by the Arm when unlocking joints 

- Do support the Arm before and during unlocking it. 

- Do not place your head or other body parts between or underneath links of the Arm. 

- Do not place body parts (especially hands, fingers) between links of the Arm, the end effector, or stationary objects. 

- Do not use the Emergency Unlocking Tool while the Arm is powered. 

- Only use the supplied Emergency Unlocking Tool. 

- Store Emergency Unlocking Tool near the Arm. 

R02210/1.4/EN 

Franka Robotics GmbH © 

13 

DECLARATION OF INCORPORATION AND CERTIFICATES **Hot Surfaces label** 



Fig. 3.3: Hot Surface label 



###### **WARNING** 

###### **Hot Surfaces and Guiding** 

At ambient temperatures above 30 °C the robot surface can become too hot to touch. Therefore, using the Assist feature in Execution mode is not permitted above 30 °C. 

###### **Functional earth label** 

The functional earth label points to the location where functional earth can be connected to the Arm. 



Fig. 3.4: Functional earth label 

###### **Lifting position label** 

The lifting position label indicates the points at which the Arm may be lifted. 



Fig. 3.5: Lifting position label 

##### **Control** 

###### **Type label** 



Fig. 3.6: Type label control 

R02210/1.4/EN 

Franka Robotics GmbH © 

14 

DECLARATION OF INCORPORATION AND CERTIFICATES **External Enabling Device** 

###### **Type label** 



Fig. 3.7: Type label external device 

##### **Emergency Stop Device** 

###### **Type label** 



Fig. 3.8: Type label emergency stop device 

R02210/1.4/EN 

Franka Robotics GmbH © 

15 

###### SAFETY 

## **4 SAFETY** 

#### **4.1 Safety Instructions and General Indications** 

###### **Warning notices** 

Before installing, starting up, and operating the device, carefully read this manual and any additional documentation. Take NOTICE of the safety instructions as well as general indications. 

Warning notices are posted as follows: 

**CAUTION** Type of hazard Potential consequences of hazard Evasive/avoidance actions to be taken 

The following warning notices are used in this manual: 



**DANGER** 

DANGER indicates a hazardous situation that, if not avoided, will result in death or serious injury. 



|**WARNING**|
|---|



WARNING indicates a hazardous situation that, if not avoided, could result in death or serious injury. 



**CAUTION** 

CAUTION indicates a hazardous situation that, if not avoided, could result in minor or moderate injury. 

**_NOTICE_** 

NOTICE indicates information considered important but not hazard related. 

**SAFETYINSTRUCTION** 

SAFETY INSTRUCTION indicates processes that need to be strictly observed. 

###### **Indications** 



Indicates where further information can be obtained. 

R02210/1.4/EN 

Franka Robotics GmbH © 

16 

###### SAFETY 

#### **4.2 Notice of Liability** 

Franka Research 3 has been developed according to the relevant quality standards. A hazard and risk assessment according to EN ISO 12100 has been carried out through the course of development and is the basis for Franka Research 3 and this manual. 

The Arm is equipped with an ISO end effector flange according to DIN ISO 9409-1-A50. 

The present document includes assembly instructions for Franka Research 3 as a partly completed machinery. It contains descriptions of the conditions that must be met to correct incorporation in the final machinery not to compromise safety and health (e.g., Annex I of Machinery Directive 2006/42/EC). 

#### **4.3 Intended Use** 

Franka Research 3 is exclusively intended for use in research and development in academic and industrial environments. The system may only be used in sound technical condition, for its intended purpose, and within the technical specifications and operating conditions, with awareness of safety and possible dangers. 

The present Franka Research 3 system is intended exclusively for use as described in this manual. 

For the normal and extended working conditions under which the robot should operate, see chapter 8 “TECHNICAL SPECIFICATIONS“ and Chapter 10.2 “Correct Installation Site”. 

#### **4.4 Misuse** 



###### **DANGER** 

**Misuse of Franka Research 3** 

- Danger to life and risk of injury, as well as risk of impairments, damage to the robot, and other material assets. 

- Only use Franka Research 3 in sound technical condition. 

- Only use Franka Research 3 in the ambient and operating conditions described in this document. 

The misuse of Franka Research 3 voids the manufacturer's warranty and liability. Any usage different from the intended use is considered misuse and is not permissible. 

Misuse is any use that deviates from the warnings, notices, and instructions in this manual and the Getting Started guide, in particular, but not limited to, the following uses: 

- Transport of people or animals 

- Transport without packing pose and original packaging 

- Use as climbing assistance 

- Leaning against the Arm 

- Use in potentially explosive areas 

- Use below ground 

- Use for the handling of radioactive objects 

- Use outdoors 

- Use as a medical product 

- Use as a service Arm, e.g., for the care of the elderly 

- Use in the vicinity of children 

- Handling of liquids 

- Use in any mounting position other than upright 

- Use outside of the specified operating limits 

R02210/1.4/EN 

Franka Robotics GmbH © 

17 

###### SAFETY 

Modifications to Franka Research 3 that Franka Robotics does not explicitly permit are not allowed and will lead to loss of warranty and liability claims. Not permitted modifications include but are not limited to the following: 

- Any adaptation of the mechanical structure 

- Varnishing 

- Wrapping the robotic structure unless using FE certified equipment 

Franka Robotics grants only the following modifications to Franka Research 3: 

- Installation of an external cable guiding system (can impact the motion and control behavior of the system) 

- Mounting equipment to the flange 

- Covering screw holes 

It is prohibited to open the Arm and the Control enclosure, and other equipment. 

The robot may only be used in places where sufficient space and safe use can be ensured. 

Franka Robotics is not liable for damage caused by mounted equipment or damage caused by misuse. 

#### **4.5 General Possible Dangers and Safety Measures when Working with Robots** 

**Abstract of possible dangers** 

An extensive but not definitive list of dangers that generally may be presented by a robot system can be found under EN ISO 10218-1:2011 ANNEX A. 

Special attention is drawn here to the following dangers that the Franka Research 3 may present: 



###### **DANGER** 

###### **Electrical or fire hazards and dangerous fumes** 

Fire and fumes may cause breathing difficulties, eye irritation, lung damage, poisoning, and may lead to death. 

- Do not use the Franka Research 3 outside of its indicated specifications. 



###### **DANGER** 

###### **Damaged wires or inadequate electrical installation** 

Risk of personal injury by electric shock, as well as material damage. 

- Only use Franka Research 3 in sound technical condition. 

- Only install the emergency stop system with qualified personnel. 

- Check cables and electrical installations. 

R02210/1.4/EN 

Franka Robotics GmbH © 

18 

###### SAFETY 



###### **DANGER** 

**Risk of smoldering fires** 

Too many devices connected to the power supply system may lead to an overload of the electrical installation and may result in smoldering fires, which may cause death or severe damage to persons. 

- Connect the Franka Research 3 accordingly to avoid an overload of the electrical installation. 

- Install the overload protection devices accordingly. 



###### **WARNING** 

**Objects falling from end effectors due to a power supply cut off** Objects falling from the gripper can lead to injuries to hands, fingers, feet, and toes. 

- Always wear personal protective equipment (e.g., safety shoes). 

- Use the appropriate type of grippers to prevent objects from falling. 



###### **WARNING** 

**Falling and unexpected motions of the robot, especially in earthquake-prone areas** 

Risk of severe injuries such as crushing, tearing of the skin, and puncturing. 

- Level the platform. 

- Only install the Arm on even, unmoving, and stable platforms. Accelerations and vibrations are not permissible. 

- Do not install the Arm on hanging, tilted, or uneven platforms. 

- Level the platform in an upright position. 

- Ensure a correctly laid out and tight screw connection. 

- Tighten the screws after 100 hours of operation with the correct tightening torque. 

- If operated in an earthquake-prone area, take the respective hazard and risk assessments into consideration. 



###### **WARNING** 

**Dangerous and uncontrolled motions of the Arm** 

Risk of severe injury, such as crushing, tearing of the skin, and puncturing from the Arm and end effectors. 

- Ensure that the end effector and/or the gripped object mass and the Center of Mass (CoM) are parameterized correctly. 

- Keep out of the workspace during operation. 



###### **CAUTION** 

**Damaged cables, plugs, mechanical housing, or oil leaks** 

Contact with leaking oil may cause eye or skin irritation. Electrical risks may lead to severe injury. 

R02210/1.4/EN 

Franka Robotics GmbH © 

19 

###### SAFETY 

- Only use Franka Research 3 in sound technical condition. 

- Do not use damaged cables, plugs, and mechanical housing for operation. In cases of doubt, contact Franka Robotics. 

###### **Sound condition** 



###### **CAUTION** 

**Leaking grease or oil through voids of structural elements of the robot** Irritation of skin and eyes. 

- Stop operating the machine. 

- Contact manufacturer. 

- Use gloves. 

- Seek medical attention after contact with eyes or skin. 

###### **Disruptions** 

###### **_NOTICE_** 

The operator will be informed about possible malfunctions through Desk. Malfunctions need to be rectified before continuing the operation. 

- To rectify the possible malfunctions, follow the instructions in the Franka UI. A reboot of the system may be required. 

###### **Overload of joints** 

###### **_NOTICE_** 

An offline overload in all the robot's joints may lead to material damage to the robot. 

- Perform a risk assessment with foreseeable misuse in mind. 

- Adhere to the system’s warning to take the robot out of operation if necessary. 

#### **4.6 Application Related Possible Dangers and Safety Measures** 

The following possibly safety-related aspects are to be considered when planning and designing the application and performing the hazard & risk assessment for completed machinery. The integrator is obligated to perform a risk analysis. 

###### **Functionalities and features of various safety levels** 

Franka Research 3 offers functionalities and features of various safety levels. All safety functions and their corresponding safety ratings are described in section Safety Functions in chapter 4.11 “Safety Functionalities“. All other functionality described throughout this chapter is not classified as safety-rated according to EN ISO 13849-1 or EN 62061. You may, therefore, not rely on the availability of these functionalities. 

Please NOTICE that the integrator is obligated to perform a risk analysis. 

R02210/1.4/EN 

Franka Robotics GmbH © 

20 

###### SAFETY 

###### **Unexpected motion** 



###### **CAUTION** 

###### **Unexpected movement of Arm** 

The use of various applications, handled end effectors and surrounding objects, may cause crushing between arm segments and impact and collision. 

- Ensure that the end effector and/or the object mass and the Center of Mass (CoM) are parameterized correctly. 

- Keep out of the maximum workspace during operation. 

###### **Trapping within a completed machinery** 



###### **WARNING** 

**Risk of trapping body parts or person** 

Risk of severe injury, such as crushing, tearing of the skin, and puncturing from the Arm and end effectors. 

- Do not place body parts between Arm segments. 

- In case of acute mortal danger: 

   1. Press the Emergency Stop Device to stop the robot from operating. 

   2. Pull or push the Arm out of the dangerous position manually. 

Please see section Emergency unlock in chapter 4.9 “Manually Moving the Arm” for more information. 

###### **Wiring of end effectors** 

###### **_NOTICE_** 

If an end effector is used with Franka Research 3, the maximum attachable payload is reduced by the weight of the end effector and its external wiring. 

###### **_NOTICE_** 

External wiring adds additional loads and torques to the Arm which may influence Franka Research 3‘s control performance. 

###### **Initiation of motion of externally wired end effectors, associated equipment** 

###### **_NOTICE_** 

Because of different configurations, installed apps and services, Franka Research 3 is able to send protocols to possibly connected machines (incl. starting motion), externally wired end effectors, and other associated equipment. Please be aware of possible related risks of using external equipment. 

Please see section Initiating Motion in chapter 13.6.11 “Test & Jog” for more information. 

###### **Single Point of Control** 

Franka Research 3 can be controlled via a single Franka UI connection or field bus. Single Point of Control (SPoC) mechanisms ensure control by one source only. Field buses are covered by SPoC as well. For more information about SPoC, refer to chapter 13.2 “Single Point of Control”. 

R02210/1.4/EN 

Franka Robotics GmbH © 

21 

###### SAFETY 



###### **WARNING** 

**Unexpected movement of Arm** 

- Risk of severe injury, such as crushing, tearing of the skin, and puncturing from the Arm and end effectors. 

- Ensure that the end effector and/or the object mass and the Center of Mass (CoM) are parameterized correctly. 

- Keep out of the workspace during operation. 

- In case of acute mortal danger: 

   1. Press the Emergency Stop Device to stop the robot from operating. 

   2. Pull or push the Arm out of the dangerous position manually. 

- In case of non-life-threatening danger: 

   1. Use the Emergency Unlocking Tool to move the Arm. 

###### **Surface temperature of the Arm (from base until axis 7, excluding flange)** 



###### **WARNING** 

###### **Hot Surfaces** 

Handling of the Arm's metal or plastic segments for a prolonged time after intense task execution may cause thermal burns. 

- Do not touch the Arm’s segments for more than 60 seconds after stopping the Franka Research 3 after an intense task execution at maximum payload and extended temperature. 



###### **WARNING** 

**Hot Surfaces and Guiding** 

At ambient temperatures above 30 °C the robot surface can become too hot to touch. Therefore, using the Assist feature in Execution mode is not permitted above 30 °C. 

Effects depending on the task and environment. 

The required safety instruction depends on risk assessment (regarding hot surfaces). 

###### **SAFETYINSTRUCTION** 

At extended ambient temperatures between 25 °C and 45 °C (after intense task execution and once Franka Research 3 is set to “monitored stop” state), the integrator needs to implement measures and evaluate the risks of touching the Arm for a prolonged time (< 60 s) without being subjected to thermal burns (EN ISO 13732-1:2006). Measures include but are not limited to the following: 

- Cool-down time for the robot. 

- Switching off the robot for a certain amount of time. 

- Notifying the operator. 

- Marking the spots that are most likely to be hot. 

- Prohibiting access to the robot. 

R02210/1.4/EN 

Franka Robotics GmbH © 

22 

###### SAFETY 

###### **SAFETYINSTRUCTION** 

The integrator needs to implement measures for touching the surfaces of the Arm, the end effector, and the end effector’s flange regarding possible heating which may lead to thermal burns (EN ISO 13732-1:2006). Measures include but are not limited to the following: 

- Cool-down time for the robot. 

- Switching off the robot for a certain amount of time. 

- Notifying the operator. 

- Marking the spots that are most likely to be hot. 

- Prohibiting access to the robot. 

#### **4.7 Installation of Safety Peripherals** 

###### **Emergency stop installation** 

The Emergency Stop Device needs to be installed according to the generally valid and accepted engineering standards, e.g., European standards EN 60204 and related. 

The Emergency Stop Device provided by Franka Robotics needs to be connected to the X3.1 port. Other devices than the Emergency Stop Device provided by Franka Robotics may also be connected to the X3 port. 

The devices connected to the emergency stop signal must follow EN 60947-5-5 or EN 62061. 

Store detached devices that no longer fulfill a safety function away from the device to prevent them from mistakenly being activated. 

###### **_NOTICE_** 

Place the connected Emergency Stop Device such that it is always reachable in case of an emergency but that an accidental use can be prevented. 



Fig. 4.1: Connection Emergency Stop Device 



R02210/1.4/EN 

Franka Robotics GmbH © 

23 

###### SAFETY 

###### **Stopping time and distance** 

Stopping time (i.e., the time that passes between the request of an emergency stop and the complete stop of the Arm) and stopping distance (i.e., the distance covered by the Arm after activation of the emergency stop until it comes to a complete stop) were measured per EN ISO 10218-1, Annex B. Stopping time and distance can be found in the appendix of this document. 

#### **4.8 Fail-safe locking system** 

###### **Fail-safe locking system** 

When the Arm is disconnected from the power supply, the locking bolts automatically lock all seven joints. The locking bolts mechanically lock any motion regarding the joints so that the Arm stays in position even when it is not supplied with power. 

Due to the technology of these locking bolts, the exact position cannot be maintained when the power is cut off. The locking bolts lock with an audible click and the arm lower a few centimetres. Especially in the joints, which are particularly influenced by gravity due to their alignment and position. 

###### **Unlocking the safety locking system** 

Each axis will move slightly as soon as the safety locking system unlocks. 

#### **4.9 Manually Moving the Arm** 

###### **Moving the Arm without electrical power** 



###### **CAUTION** 

###### **Moving Arm** 

- Risk of severe injury, such as crushing, tearing of the skin, and puncturing 

- Always wear personal protective equipment (e.g., safety goggles). 

- The integrator needs to perform a risk analysis for any attached end effectors. 

- Do not stand in the maximum workspace during operation. 

###### **_NOTICE_** 

The integrator must assess the risk that a person may become trapped. 

If a person is trapped by the Arm, follow one of the three release options below to free them even when the power supply is cut off. 

- Use the Emergency Unlocking Tool at the corresponding openings of the joint to be unlocked to unlock the robot and move it by hand. 

- Unscrew the Arm base from its mounting place. 

- Manually move the Arm. 

In case of non-acute danger and jamming of the Arm, use the Emergency Unlocking Tool. 

R02210/1.4/EN 

Franka Robotics GmbH © 

24 

###### SAFETY 



###### **WARNING** 

**Falling heavy Arm when using Emergency Unlocking Tool** 

- Risk of being trapped by the Arm when unlocking joints 

- Do support the Arm before and during unlocking it. 

- Do not place your head or other body parts between or underneath links of the Arm. 

- Do not place body parts (especially hands, fingers) between links of the Arm, the end effector, or stationary objects. 

- Do not use the Emergency Unlocking Tool while the Arm is powered. 

- Only use the supplied Emergency Unlocking Tool. 

- Store Emergency Unlocking Tool near the Arm. 

###### **Action: Emergency unlock** 

###### **SAFETYINSTRUCTION** 

1. Press the Emergency Stop Device to stop the robot from operating. 

2. Take the unlocking tool from the Pilot’s base. 

3. Hold the Arm’s segments. 

4. Insert the unlocking tool in the respective trapezoidal openings and unlock one or more joints one after another. 

   - The openings are marked with the “Emergency Unlock” label. 

- The Arm segment can now be moved manually. 



Fig. 4.2: Emergency unlock 

###### **_NOTICE_** 

Be aware that as soon as the unlocking tool is inserted, the Arm segment towards the wrist of the Arm can fall down with gravity. 

R02210/1.4/EN 

Franka Robotics GmbH © 

25 

###### SAFETY 

**_NOTICE_** 

- The integrator needs to make sure that the unlocking tool is stored in a holder at the base of the robot. 

- Do not remove the unlocking tool unless in an emergency. 

- The unlocking tool must always be within reach. 

- Only use the original unlocking tool. 

- The unlocking tool should only be used in case of emergency. 

###### **Action: Pushing away manually** 



Fig. 4.3: Pushing away manually 

###### **SAFETYINSTRUCTION** 

- In case of acute mortal danger: 

1. Press the emergency stop device to stop the robot from operating. 

2. Pull or push the Arm out of the dangerous position manually. 

3. Secure the robot arm from falling down. 

###### **_NOTICE_** 

Manually pulling or pushing the Arm will damage the Arm as the joints will be overloaded. 

- The Arm should only be manually pulled or pushed away in safety-critical situations. 

#### **4.10 Safety Concept** 

The safety concept of Franka Research 3 provides a simple approach to making the robotic system safe within its target application. The system provides a set of safety functions compliant with EN ISO 13849-1. For more information on safety functions, see chapter 4.11”Safety Functionalities“. 

With the Franka UI tool Watchman, the safety operator can use those safety functions in so-called safety rules and scenarios to cover the risks identified in the risk analysis carried out for the robot cell and application. 

The configuration of the safety system through Watchman is split into two parts: 

- General safety-relevant settings are configured in the safety setup (e.g., defining the behavior of safe inputs). 

- Safety scenarios allow covering different situations with suitable safety measures. 

Each safety scenario can define one or more safety rules to cover a certain situation/state the robot can be in. 

Each safety rule consists of a safety function, optional selectable conditions (defining when the rule is active), and a reaction triggered when the safety function is violated. 

R02210/1.4/EN 

Franka Robotics GmbH © 

26 

###### SAFETY 

With the safety setup and the safety scenarios, the safety operator can set up the safety system according to the needs revealed by the risk analysis. Franka Research 3 comes with a predefined and prevalidated set of scenarios. If they are suitable to cover the needs revealed by the risk analysis, this setup can be used out-of-thebox. 

If specific safety rules and scenarios are required, the safety operator can adjust predefined scenarios and rules using Watchman. Some safety scenarios are read-only or contain fixed rules to ensure a minimum set of safety measures common to most applications. In general, these presets are defined by ISO 10218-1. 

The safety operator must validate all customized safety settings and scenarios before confirming and activating them on the robot. 

The predefined safety scenarios cover the possible operation states of the system. 

###### **_NOTICE_** 

During recovery of violated safety functions, the system switches to the predefined recovery scenario to provide a safe recovery. The original scenario (e.g., Work), in which the violation happened, its rules, and especially the violated safety function, are not active during recovery. The system switches back to the original scenario as soon as the recovery has been completed. The integrator must consider the predefined recovery scenarios when performing the application-specific hazard & risk assessment for completed machinery. 

##### **Scenarios for states in Programming mode** 

###### **Idle (read-only)** 

- The user might be close to the robot but not interact with it. The robot is at a safely monitored standstill. 

- • This is the default state in Programming mode if no other mode is active or if conflicting inputs are present. 

###### **Teach (customizable)** 

- The user can hand-guide the robot. 

- Safe activation signal: Pressing the Enabling Button located on the Pilot-Grip. 

- The safety operator can customize the pre-defined velocity limit. 

###### **Test & Jog (customizable)** 

- The user watches and verifies the execution of a created task and inches the robot via Franka UI. 

- Safe activation signal: External Enabling Device (X4). 

- The safety operator can customize the pre-defined velocity limit. 

###### **Opening/closing brakes (read-only)** 

- Active while the brakes are opened or closed. 

- Extend of motion and speed is safely limited. 

##### **Scenarios for states in execution mode** 

###### **Work (customizable)** 

- The robot works independently by executing a task. 

- This scenario is pre-filled with rules activating the safely monitored standstill (SMSS) safety function stopping the robot when the inputs X3.2 or X3.3 are opened. A rule to trigger the “Safely Monitored Standstill” within “Work” to allow a switch to the “Assist” mode must be set. 

- The safety operator can customize all rules within this scenario. 

R02210/1.4/EN 

Franka Robotics GmbH © 

27 

###### SAFETY 

###### **Assist (customizable)** 

- Collaborative operation “hand-guiding” as defined by ISO 10218-1 while in execution mode. 

- Safe activation signal: Pressing the Enabling Button located on the Pilot-Grip while the robot is in Safely Monitored Standstill. 

- The safety operator can customize the velocity limit for this mode and/or add custom rules. 

###### **Opening/closing brakes (read-only)** 

- Active while the brakes are opened or closed. 

- Extend of motion and speed is safely limited. 

##### **Error/Violation states** 

The following states are not active in the normal operation of the robot. They only become active when safety functions in the other states are violated, or safety-relevant errors occur. 

###### **Work invalid (read-only)** 

If there is no valid safety scenario available for the Work mode, the “Work invalid” scenario is activated as a backup to prevent the robot from moving. 

###### **Violation idle (read-only)** 

This state is active after any safety function is violated and the respective reaction has been carried out. 

###### **Recovery (position error, joint limit violation, or space violation) (read-only)** 

This state is active while the robot is recovering from a violated safety function or an error. 

Safe activation signal: Depending on the type of violation or error. 



Fig. 4.4: States during normal operation 

R02210/1.4/EN 

Franka Robotics GmbH © 

28 

###### SAFETY 

#### **4.11 Safety Functionalities** 



###### **WARNING** 

###### **Hot Surfaces and Guiding during Recovery** 

At ambient temperatures above 30 °C the robot surface can become too hot to touch. Therefore, in case of occurence of a safety function violation which requires hand-guiding during recovery, the following must be observed: 

- Recovery may be performed only by personnel specifically trained for this situation. 

- Before recovery, surface temperatures must be evaluated to be within touchable limits. Cooldown times depend on previous operation and ambient temperatures. 

- Wearing heat resistant safety gloves for this procedure is advised. 

###### **_NOTICE_** 

Franka Research 3 distinguishes between two kinds of safety functions: monitoring functions and stopping functions. 

Monitoring functions guarantee that limits are not breached, e.g. speed (SLS-J), position (SLP-C)… 

Stopping functions are triggered upon a monitoring violation or a safety input. It is the Safety Operator’s obligation to consider stopping times and stopping distances when configuring the limits. 

###### **_NOTICE_** 

Connecting external devices with a separate power supply may jeopardize the system’s safety function if the electrical ratings are not complied with. 

In addition, the voltages in the connected devices must either be SELV or suitably isolated from systemconnected signals. 

###### **Safe inputs** 

|**Name**|**Description**|**Safety Rating**|**Stop Reaction**|
|---|---|---|---|
|X3.1 - Emergency stop|The X3 connector in the robot<br>base provides one safe input to<br>connect an emergency stop.|PL d / Cat.3|Category 1 stop|
|X4 - External Enabling|The X4 connector at the robot<br>base provides one safe input<br>dedicated to a 3-position External<br>Enabling Device.|PL d / Cat.3|Releasing or fully pressing the Enabling Button<br>activates the SMSS safety function. The<br>reaction in case of a violation of SMSS<br>depends on the active safety scenario.|
|Enabling Button|A 3-position Enabling Button is<br>provided near the flange on the<br>Pilot-Grip of the robot.|PL d / Cat.3|Operating mode “Programming”: Category 1<br>stop (see predefined scenario “Idle”)<br>Operating mode “Execution”: Reaction<br>depending on SMSS configuration in scenario<br>“Work.”<br>During safety function violation or error<br>recoveries, fully pressing or releasing the<br>Enabling Button triggers a Category 1 stop.|
|X3.2 - Safe input 1<br>X3.3 - Safe input 2|The X3 connector on the robot<br>base provides two additional safe<br>inputs. The behavior of those two<br>inputs can be configured in the<br>safety setup.|PL d / Cat.3|Depends on the configuration in safety<br>scenarios.|



R02210/1.4/EN 

Franka Robotics GmbH © 

29 

SAFETY 

**Monitoring functions** 

|**Name**|**Abbreviation**|<br>**Description**|**Safety**<br>**Rating**|**Recovery in case of violation**<br>**NOTICE: The operator can recover all**<br>**violations.**|
|---|---|---|---|---|
|When SLP-|C is activate|d, the robot cannot be controlled|by FCI!||
|Safely Limited Cartesian<br>Position<br>When SLS-|SLP-C<br>C is activate|Monitoring of the Cartesian position<br>of certain points on the Arm. The<br>position is checked against user-<br>defined Cartesian area.<br>The following points are monitored:<br>• Flange<br>• Elbow<br>• Wrist<br>• Customer defined tool spheres<br>The monitoring can be configured to<br>signal violation either when one or<br>more points are inside the defined<br>space or when one or more points<br>are outside the defined limits.<br>Parameterization:<br>• End Effector model (up to five<br>spheres)<br>`o`<br>Radius of each sphere<br>`o`<br>Position of each sphere<br>center relative to the flange<br>Hint: This is a general setting and<br>will affect all safety functions using<br>this tool model.<br>• Monitored Cartesian space (box)<br>• Violation if inside/outside<br>d, the robot cannot be controlled|PL d /<br>Cat.3<br>by FCI!|Violated position or orientation limits<br>will be shown in Desk of Franka UI.<br>• Unlock brakes of robot.<br>• Guide robot out of Cartesian<br>position limit. Franka UI shows if<br>position limits are not violated<br>anymore.<br>• Finish recovery by pressing Confirm<br>in Desk.|
|Safely Limited Cartesian<br>Speed|SLS-C|Monitoring of the Cartesian speed<br>of certain points on the Arm<br>structure. The following points are<br>monitored:<br>• Flange<br>• Elbow<br>• Wrist<br>• Centers of customer-defined tool<br>spheres<br>Parameterization:<br>• Limit for Cartesian speed|PL d /<br>Cat.3|A violation of the speed limit is shown<br>in a dialog in the Franka UI.<br>• Confirm violation by pressing the<br>button in Pop-up message.<br>No further recovery procedure is<br>necessary.|
|Safely Monitored Stand<br>Still|SMSS|Monitoring of the standstill in<br>Cartesian space of certain points on<br>the Arm structure. The following<br>points are monitored:<br>• Flange<br>• Elbow<br>• Wrist<br>• Centers of customer-defined tool<br>spheres<br>The user cannot change the<br>parameters of this safety function.|PL d /<br>Cat.3|A violation dialog is shown in the<br>Franka UI.<br>• Confirm violation by pressing the<br>button.<br>No further recovery procedure is<br>necessary.|
|Safe End Effector Power<br>Off|SEEPO|Safely switch off the power<br>provided to the end effector (48 V<br>power line). The behavior of SEEPO<br>can be configured in the safety<br>setup. E.g., it can be configured that<br>SEEPO switches off the power<br>when an emergency stop is<br>triggered.<br>Parameterization:<br>• General configuration, whether<br>SEEPO is active or not<br>• Switch-off triggers of SEEPO|PL b /<br>Cat. b|The power of the end effector can be<br>switched on again in Settings or the<br>sidebar of Desk.|



R02210/1.4/EN 

Franka Robotics GmbH © 

30 

SAFETY 

###### **Internal monitoring functions (not parametrizable and configurable in safety rules)** 

|**Name**<br>|**Abbreviation**<br>When SLP-J|**Description**<br>is activated, the robot c|**Safety**<br>**Rating**<br>annot be|**Reaction**<br>controlled|**Recovery in case of violation**<br>**NOTICE: The operator can recover all violations.**<br>by FCI!|
|---|---|---|---|---|---|
|Safely<br>Limited<br>Position<br>of Joint|SLP-J|Monitoring of the<br>position of each joint in<br>joint space.<br>This safety function is<br>only used internally to<br>protect the joint limits of<br>the Arm, prevent self-<br>collisions and local<br>clamping. It is not<br>available in user-defined<br>scenarios.<br>This is a limiting function.|PL d /<br>Cat.3|-|A dialog within Franka UI informs the user about<br>the violation and allows recovery.<br>• Unlock the joint that shall be moved by clicking<br>the unlock icon in the recovery dialog.<br>• To enable recovery motion, press the External<br>Enabling Device.<br>• Move the joint by pressing the +/- buttons in<br>the recovery dialog.<br>Hint: Joints in a violated state can only be moved<br>away from violated limit. All other joints can be<br>moved in both directions to move the robot into a<br>more convenient pose.|
|Safely<br>Limited<br>Speed of<br>Joint|SLS-J|Monitoring of the speed<br>of a single joint in joint<br>space.<br>This internal safety<br>function is used, e.g., to<br>prevent fast motions<br>during joint position<br>recovery.|PL d,<br>Cat. 3|Cat. 1<br>Stop|A violation dialog is shown in Franka UI.<br>1. Confirm violation by pressing the button.<br>No further recovery procedure is necessary.|
|Safely<br>Limited<br>Distance|SLD|SLD monitors a single<br>joint to stay within a<br>permitted position<br>window.<br>This internal safety<br>function is used, e.g., to<br>prevent excessive motion<br>during the brake opening<br>procedure.|PL d,<br>Cat. 3|Cat. 1<br>Stop|A safety error dialog is shown in the Franka UI.<br>1. Acknowledge error by pressing the button.<br>No further recovery procedure is necessary.|



###### **Stopping functions** 

|**Name**|**Description**|**Safety Rating**|
|---|---|---|
|Category 0 stop|The Arm is stopped immediately by removing power from the motors<br>and applying the brakes.|PL d / Cat.3|
|Category 1 stop|The Arm is stopped in a controlled manner using the normal control of<br>the motors until the standstill of each joint. The brakes are applied,<br>and the power is removed from the Motors upon standstill.<br>The Cartesian speed deceleration is monitored.|PL d / Cat.3|
|Category 2 stop|The Arm is stopped in a controlled manner using the normal control of<br>the motors until the standstill of each joint. Upon standstill, the<br>standstill is safely monitored.<br>The Cartesian speed deceleration is monitored.|PL d / Cat.3|



###### **Safe outputs** 

|**Name**|**Description**|**Safety Rating**|
|---|---|---|
|Safe End Effector|Switch the power provided to the end effector (48 V power line) off.|PL b / Cat.b|
|Power Off|||



###### **Further safety ratings** 

The 3-stage Enabling Button near the robot's flange is realized in compliance with IEC 60204-1:2016 and IEC 60947-5-8:2006. 

R02210/1.4/EN 

Franka Robotics GmbH © 

31 

###### SAFETY 

The 3-stage External Enabling Device provided by Franka Robotics is realized in compliance with IEC 602041:2016 and IEC 60947-5-8. 

The Emergency Stop provided by Franka Robotics complies with IEC 60204-1:2016 and EN ISO 13850:2015. 

##### **Other safety-related recoveries (in case of safety errors)** 

###### **Joint position error recovery** 

Only Safety Operators can recover joint position errors. 

A dialog in Franka UI informs the user about the error and allows recovery. 

Detailed instructions on how to correct the error can be found in chapter 13.8 “Troubleshooting”. 

###### **Safe input error recovery** 

Safe input errors are recoverable by confirming the respective dialog in Franka UI if confirmation for those inputs is configured in Watchman. 

###### **Other safety errors** 

Other safety errors are typically not recoverable. Please try to restart the system to recover from such errors. If the error persists, contact your vendor or Franka Robotics. 

###### **General info for all cases** 

In case of a safety violation, the robot does not allow motion until the recovery has been accomplished. 

In case of a safety violation, the base flashes slowly in red. 

If necessary, Franka UI will show a recovery wizard to perform the recovery procedure. 

Only the safety operator can recover joint position errors. 

The operator can perform all other recoveries. 

Further measures for possible troubleshooting are described in chapter 13.8 “Troubleshooting”. 

#### **4.12 Additional information for planning and initial installation of a robot system** 

According to the EN ISO 10218-2 and EN ISO 8373 standards, a robot system is understood to be a robot that is set up as a complete system with peripheral devices such as robot tools, workpieces, conveyor technology and all devices and protective equipment involved. Due to motion of the robot and the integrated applications, a robot system represents a potential hazard for those people involved with activities of operation, assembly or maintenance. The jobs of both the manufacturer and the installer of a robot system is to analyze and evaluate these hazards and to ensure appropriate protective measures. 

This specification is based on laws, regulations and guidelines that are country-specific and thus depend on the respective location (place of the operation) of the robot. 

In the European Economic Area (EEA), overarching regulations apply, which may be supplemented by respective country-specific legislation, industry-specific regulations and internal company regulations. 

When planning a robot system, it is therefore necessary to find out about the regulations at the installation site and to take these into account accordingly. 

The type of industry can also lead to different specifications. For example, will the robot system be used in industrial Research or in research? 

As mentioned above, the location of the robot system determines which various rules, regulations and laws must be observed. In the European Economic Area (EEA), the Machinery Directive and harmonized European standards apply across all countries. Furthermore, local legislation such as the Product Safety Act, the Product Liability Act and the Ordinance on Industrial Safety and Health in Germany must be considered. 

The most important rules and regulations for the build-up of a robot system are listed below. 

R02210/1.4/EN 

Franka Robotics GmbH © 

32 

###### SAFETY 

|Standards / Directives|Description|
|---|---|
|RL 2006/42/EG|Maschinenrichtline des Europäischen Parlaments und des Europäischen Rates|
|ISO 12100|Safety of machinery — General principles for design — Risk assessment and risk<br>reduction|
|ISO 10218-2|Robots and robotic devices — Safety requirements for industrial robots — Part 2:<br>Robot systems and integration|
|ISO/TS 15066|Robots and robotic devices — Collaborative robots|
|ISO 13854|Safety of machinery — Minimum gaps to avoid crushing of parts of the human body|
|ISO 13855|afety of machinery — Positioning of safeguards with respect to the approach<br>speeds of parts of the human body|
|ISO 13850|Safety of machinery — Emergency stop function — Principles for design|
|ISO 11161|Safety of machinery — Integrated manufacturing systems — Basic requirements|
|IEC 60204-1|Safety of machinery - Electrical equipment of machines - Part 1: General<br>requirements|
|ISO 13849-1|Safety of machinery — Safety-related parts of control systems — Part 1: General<br>principles for design|
|ISO 13849-2|Safety of machinery — Safety-related parts of control systems — Part 2: Validation|
|ISO 13482|Robots and robotic devices — Safety requirements for personal care robots|



Basically, the same objective always applies: =>reducing the risk of injury to people. 

Thus, the statement can be made that no robot system may be operated without appropriate protective measures. 

Protective measures can be, for example: 

- ➢ Safety protective device 

- ➢ Electro-sensitive protective equipment 

- ➢ Fencing and/or physical barriers 

- ➢ Marked areas 

- ➢ Signs 

- ➢ Emergency stop buttons 

- ➢ Indicating elements 

- ➢ Control system safety devices 

- ➢ Robot internal safety functionalities (see chapter 4.11 “Safety Functionalities”) 

Due to the different possible applications of a robot, Franka Robotics cannot provide a uniform guideline for determining the required protective devices when integrating a robot system. The responsibility for the safe realization of the robot system lies with the integrator / operator. 

A very good and detailed guide to the design of robot systems is also described on the DGUV (German Social Accident Insurance) website => DGUV Information 209-074. 

R02210/1.4/EN 

Franka Robotics GmbH © 

33 

###### SAFETY 

The following explanations describe measures that are an essential part of planning a robot system. These measures must then be supplemented by the necessary details from the regulations and specifications of the application. 

- I. Analysis: 

The analysis includes the description of the automation solution and at the same time a narrowing down of the function of the planned system. This part is called the intended use. The non-intended use, i.e. the conditions and activities that must not be performed with this system, must also be documented. A detailed description of the task is part of the subsequent risk assessment and simplifies the risk determination for the respective hazards in the further course of planning. 

Creating a concept layout facilitates the overview of the planned system. This should show all components including the associated peripherals. 

The next step is the analysis of the sources of the potential danger of the robot system. It brings clarity to the subsequent risk assessment if it is listed which component poses which hazard. If necessary, this also allows the effects of hazards to be grouped together. 

All components of the robot system to be integrated are to be considered as possible sources of danger. In addition to the robot, this includes all components to be integrated, such as tools, devices, conveyor systems, control cabinets and protective devices, but also the hazards that can result from the combination of the components with each other. 

- II. Risk assessment: 

The risk assessment is used to analyze and evaluate the sources of danger and the level of the resulting risks for personal injury, as well as to determine the necessary measures for risk reduction. 

The procedure of the required risk assessment according to the Machinery Directive is described in the standard DIN EN ISO 12100. There are various tables and tools that allow a structured implementation (see reference above these listings). The basic structure of a risk assessment consists of the following elements: 

- Data on the planned system (machine designation, serial number, etc.) 

- Limits of the robot system 

- Determination of the required regulations and standards 

- Layout of the robot system 

- Marking of the sources of danger in the layout 

- Assessment of the sources of danger with regard to the respective activities and operating modes. For this purpose, different evaluation procedures can be applied. The procedure is explained in detail in the standard. 

The procedure for determining the risk reduction measures is also described in the standard and in the guidelines and literature references. 

In principle, the following prioritization of measures applies to risk reduction: 

- Avoidance of the hazard 

- Reduction through inherently safe design 

- Reduction by mechanical protective devices 

- Reduction through control-related protective devices 

- Reduction through organizational measures 

When determining the measures, the specifications from the harmonized standards should always be met. This reduces the burden of proof due to the presumption of conformity according to the standard. 

R02210/1.4/EN 

Franka Robotics GmbH © 

34 

###### SAFETY 

- III. Layout: 

In the final layout of the robot system, all protective measures should be drawn to scale. There should be a clear assignment to the protective measures identified in the risk assessment. 

- IV. Realization phase: 

Set-up of the system and implementation of the defined protective measures. 

- V. Verification: 

After the system has been set up, including all protective measures, a verification of the protective measures must be performed in accordance with the respective standards. For example, the testing of the control technology protective measures is referred to as "functional safety verification" in standard 13849-2, and the requirements for validations are regulated therein. 

This protocol of verification is an essential component for the acceptance of a robot system. 

###### VI. Acceptance: 

The final acceptance of a robot system includes a detailed logging of all individual steps mentioned above. In industrial areas of application, a declaration of conformity (CE) is required from the distributor in accordance with the Machinery Directive. A declaration of conformity (CE) is also required if a robot system is set up for "own use" in in-house Research. For robot systems in research and in the laboratory, it is also necessary to design the operation of the robot to be safe for people and to implement appropriate protective measures. The Machinery Directive defines robot systems for research purposes as systems designed for a specific research purpose and built for temporary use only. Thus, the decisive factor is whether the system has a temporary use (e.g., a one-time experiment that will be dismantled afterwards - no CE - or a permanent use as equipment in the laboratory - CE required ). 

R02210/1.4/EN 

Franka Robotics GmbH © 

35 

ROLES AND PERSONNEL 

## **5 ROLES AND PERSONNEL** 



###### **WARNING** 

- **Insufficiently qualified personnel** 

- Insufficiently qualified personnel may cause severe injuries to themselves or others. 

- Read the manual thoroughly and resolve any questions. 

   - All persons entering the robot workspace must use their knowledge and experience, be aware of potential risks regarding the robot system, and be adequately prudent in their behavior. 

- The Responsible Person must explicitly inform the users about the limitations and restrictions of Franka Research 3. 



###### **WARNING** 

###### **Intoxicated personnel** 

Intoxicated personnel may cause severe injuries to themselves or others or may cause material damage to machinery and equipment. 

- Do not operate Franka Research 3 under the influence of drugs, alcohol, or medication impacting reactions. 

#### **5.1 Personnel** 

##### **Responsible person** 

The responsible person is responsible for compliance with occupational health regulations and the operational safety ordinance. The responsible person for Franka Research 3 can be in particular the entrepreneur, the director of the institute, the employer, or a delegate responsible for the use of Franka Research 3. 

The responsible person is responsible for the following: 

- The responsible person must fulfil the monitoring obligations. 

- The responsible person must ensure that all staff members working with Franka Research 3 are suitably qualified to do so and have been informed about the possible dangers Franka Research 3 may present. 

- The responsible person must provide training and instructions in given intervals to create and consolidate risk awareness. 

##### **User** 

Users of the system are the people who are directly involved in the operation of the system. The operation of the system is divided into different tasks that cover the different operating phases of the system: 

- Administrative tasks 

- Safety related tasks 

- Operation of the system 

According to the assigned tasks, users must have qualified knowledge of the subject area of the task, safety instructions and training on the robot system. The required qualifications are described below in the description of the user roles. 

R02210/1.4/EN 

Franka Robotics GmbH © 

36 

###### ROLES AND PERSONNEL 

##### **Integrator** 

The integrator is responsible for assembling the partly completed machinery into the final machinery by combining the robot with other equipment or another machine, including other robots, to form a machine system. 

The integrator also conducts an appropriate risk assessment to identify residual risks and eliminate or minimize them. 

The integrator is responsible for the safety of the final application. 

For further information on liability-related topics, see chapter 4.2 “Notice of Liability“. 

###### **_NOTICE_** 

Only qualified or sufficiently trained personnel that possess adequate technical skills are permitted to operate the robot. The qualification of said personnel includes but is not limited to professional technical education, a university degree in engineering, or professional experience in the field of robotics or automation. 

Franka Robotics suggests a product specific training performed by Franka Robotics, partners, and affiliates. 

#### **5.2 User Roles** 

##### **Operator** 

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

##### **Administrator** 

The administrator has all the rights that the operator has. An administrator is a person authorized by the responsible person to set up and access the robotic system and to utilize the user interface Franka UI as follows: 

- User management (create, update and delete users; assign roles and modify passwords) 

- Set and change non-safety-related parameters of the system (e.g., change end effector settings) 

- Program and teach the robot system 

- Install system updates, features, and apps 

R02210/1.4/EN 

Franka Robotics GmbH © 

37 

###### ROLES AND PERSONNEL 

- Edit system configuration 

- Create, edit, and set parameters for tasks 

##### **Safety operator** 

The safety operator has the same rights as the operator, plus the rights to set up and validate safety settings. The safety operator can utilize Franka UI as follows: 

- Edit safety configurations 

- Program and teach the robot system 

- Create, edit, and set parameters for tasks 

- Recovering of specific Safety errors 

###### **_NOTICE_** 

User roles should only be assumed by qualified or sufficiently trained personnel. They should be instructed on the conduct in emergency or abnormal situations. The Responsible Person must choose the personnel based on experience, training, or similar existing duties in robotics, automation, Industrial safety and occupational health. 

##### **Assigning user roles** 

###### **Assign an Administrator** 

When logging in for the first time, creating an administrator user is compulsory. 

1. Enter a username. 

2. Enter a password. 

3. Confirm the password. 

Administrator login information should be kept safely and securely. The only way to access the role as administrator without a password is to perform a factory reset that deletes all prior information. 

###### **_NOTICE_** 

Always use secure passwords to prevent unauthorized persons from accessing the system. 

###### **Creating and editing users** 

There must always be at least one user with the Administrator role defined. This means that the last administrator cannot be deleted. Every user must be assigned a role, and several users can have the same role. Franka Research 3 supports the roles described above. 

###### Procedure 

1. Log into the Franka UI. For information on the Franka UI, see chapter 13.6 ”Franka UI”. 

2. Go to Settings. 

3. Click on the Users tab. 

4. Add new users or edit existing ones. 

R02210/1.4/EN 

Franka Robotics GmbH © 

38 

EQUIPMENT OVERVIEW 

## **6 EQUIPMENT OVERVIEW** 

The following figure shows the minimum configuration of the system and exemplifies the cabling. 



Fig. 6.1: Equipment overview 

|1|Arm|7|Power cable|
|---|---|---|---|
|2|Emergency Stop Device|8|Mains power outlet|
|3|Connecting cable|9|Interface device (not included) with Franka UI|
|4|Control|10|External Enabling Device|
|5|Ethernet (Network)|11|Emergency Unlocking Tool|
|6|Power switch|12|Connection to functional earth|



R02210/1.4/EN 

Franka Robotics GmbH © 

39 

###### EQUIPMENT OVERVIEW 

#### **6.1 The Arm** 

The Arm has the following components: 



Fig. 6.2: Overview Arm 

|1|Pilot|7|Elbow|
|---|---|---|---|
|2|Pilot-Grip|8|Soft protector|
|3|Pilot-Disc|9|Shoulder|
|4|X6-End effector connector|10|Holder for Emergency Unlocking Tool|
|5|Flange for end effector|11|Status light|
|6|Wrist|12|Base|



R02210/1.4/EN 

Franka Robotics GmbH © 

40 

###### EQUIPMENT OVERVIEW 

###### **Pilot - top view** 

Parts of Desk and the integrated end effectors can be operated directly from the robotic Arm via the Pilot-Disc. 



Fig 6.3: Pilot 

|1|Pilot-Mode button|6<br>Status light|
|---|---|---|
|2|Confirm button|7<br>Enabling Button|
|3|Teach button|8<br>Guiding-Mode Button|
|4|Delete button|9<br>Guiding Button|
|5|Arrow keys||



###### **Pilot** 

The Pilot is the user interface integrated directly into the Arm for Guiding the robot and the easy interaction with end effectors and Desk. The Pilot consists of Pilot-Disc (1-6) and Pilot-Grip (7-9). 

For more information on Desk, see section Desk in chapter 13.2 “Single Point of Control”. 

###### **Pilot-Disc (1-6)** 

The Pilot-Disc is located on top of the Pilot and is used for interacting with the robot system. You can switch between the control of Arm or end effector by pressing the Pilot-Mode button (1) on the Pilot-Disc. Select individual Apps, parameterize them or enter poses by manually guiding the Arm to the desired pose and pressing the Teach button (3). 

###### **Pilot-Grip (7-9)** 

The Pilot-Grip is located near the robot's tip as part of the robot structure. The Pilot-Grip provides a Guiding Button, an Enabling Button, and a Guiding-Mode Button. 

###### **Pilot-Mode button (1)** 

By pressing the Pilot-Mode button (1), the user switches between using the arrow keys of the Pilot-Disc to navigate Desk or to control the integrated end effectors (e.g., Franka Hand). 

###### **Confirm button (2)** 

If Confirm button is illuminated, all changes made in a context menu will be confirmed and skips to the next section. The Confirm button saves any selections made. 

R02210/1.4/EN 

Franka Robotics GmbH © 

41 

###### EQUIPMENT OVERVIEW 

###### **Teach button (3)** 

Save an arm pose or an end effector pose by moving the arm or end effector to the desired configuration and pressing the Teach button. 

###### **Delete button (4)** 

If illuminated, pressing the Delete button deletes a selected pose or section. 

###### **Arrow keys (5)** 

The Arrow keys can either navigate Desk or control integrated end effectors depending on the Pilot-Mode. In end effector mode, the key assignment depends on the active end effector. 

###### **Enabling Button (7)** 

The Enabling Button is located on the left side of the Pilot-Grip and enables robot motions if pressed to the middle position. To move the robot, half-press the Enabling Button while pressing the Guiding Button simultaneously. The Enabling Button is safety rated per the requirements in EN ISO 10218-1. The three positions of the Enabling Button either stop, re-enable, or move the robot. To immediately stop the robot, release or fully press the Enabling Button. After stopping, release it first completely and then press it again to its middle position to re-enable the robot. 



Fig. 6.4: switching status Enabling Button 



Fig. 6.5: Enabling Button 

R02210/1.4/EN 

Franka Robotics GmbH © 

42 

EQUIPMENT OVERVIEW **Guiding-Mode Button (8)** 



Fig. 6.6: Guiding Mode Button 

The Guiding‑Mode Button is located on the top of the Pilot-Grip and allows the user to change between different Guiding modalities by pressing the Guiding-Mode Button. The possible Guiding-Modes are translation only, rotation only, free moves, and user-defined movement. 





###### **Guiding Button (9)** 



Fig. 6.8: Guiding Button 

The Guiding Button is located on the right of the Pilot-Grip. Press the Guiding Button while half-pressing the Enabling Button (7) simultaneously to move the robot. 

R02210/1.4/EN 

Franka Robotics GmbH © 

43 

###### EQUIPMENT OVERVIEW 





###### **Base of the Arm** 



Fig. 6.10: Connection ports at robot base 



The base of the robot has several ports to connect and support various equipment: 

- X1 - Connection to Control 

- X2 - Digital IO’s 

The connection carries two non-safe digital inputs and outputs. The inputs and outputs and the 24 V power supply are galvanically isolated from the robot system and other interfaces of the robot. The functionality of the physical ports depends on the particular software version. 

R02210/1.4/EN 

Franka Robotics GmbH © 

44 

###### EQUIPMENT OVERVIEW 

- 

- X3 - Safety Signals 

- X3.1 - Emergency stop: A category 1 stop command will be triggered to stop the robot and optionally cut the power to the end effector by pressing the Emergency Stop Device. This behavior can be configured in Watchman. 

- X3.2, X3.3 - Safe inputs: The X3 port allows two additional safe inputs. Their behavior can be configured in Watchman. For more information on Watchman, see section Watchman in Chapter **Error! Reference source not found.** “ **Error! Reference source not found.** ”. 

- X4 - External Enabling 

The 3-position External Enabling Device enable “Test & Jog” when the system is in Programming mode. It allows Franka Research 3 to move. Programs can be started via Desk. 

- X5 - Robot network 

The interface device running the browser-based Franka UI can be connected to the X5 Ethernet port. 

###### **_NOTICE_** 

A custom connector with the corresponding safety signals must be assembled to utilize the configurable Safe inputs (X3.2, X3.3). When doing so, the existing Emergency stop can no longer be used. Therefore, the Emergency stop functionality must be integrated for channel X3.1 in the custom connector. 

###### **_NOTICE_** 

By default, the Safe input channels X3.2 and X3.3 are assigned to the SMSS safety function in the "Work" scenario in Watchman. Suppose no external safety devices are connected to X3.2 and X3.3 (only Franka Robotics emergency stop is connected to X3.1). Those inputs will be considered “activated,” meaning it will not be possible to move the robot with the default "Work" scenario rules. Depending on the applicationspecific risk & hazard analysis, the default rules may be changed to allow robot movements regardless of X3.2 and X3.3. 

R02210/1.4/EN 

Franka Robotics GmbH © 

45 

###### EQUIPMENT OVERVIEW 

###### **End effector flange** 

End effectors, such as Franka Hand, can be connected via the end effector flange. The end effector flange has been developed according to the relevant quality standards of DIN ISO 9409-1-A50. For more information, see the chapter 10.7 “Mounting End Effectors“. 



Fig. 6.11: End effector flange 



Franka Hand is not part of the certified machinery. 

#### **6.2 Control** 



The operation of the Arm is only permitted with the Control provided by Franka Robotics. 

The Control is the main control unit and is part of Franka Research 3. The main control unit realizes monitoring and control of the mechanical structure of the robot. 



Fig. 6.12: Dimensions and connection ports of control 



R02210/1.4/EN 

Franka Robotics GmbH © 

46 

EQUIPMENT OVERVIEW 





###### **Installation** 

The Control fits in a 2RU 19” rack. 

R02210/1.4/EN 

Franka Robotics GmbH © 

47 

SCOPE OF DELIVERY AND ADDITIONAL EQUIPMENT 

## **7 SCOPE OF DELIVERY AND ADDITIONAL EQUIPMENT** 

#### **7.1 Included in the box** 

###### Arm 

- 1x Arm 

- 1x Emergency Unlocking Tool 

- 4x screw (ISO 4762, M8x20, ST 10.9 A2K) 

- 4x washer (ISO 7089, M8, ST HV300 A2K) 

- 1x screw (ISO 4762, M5x8, ST 8.8 A2K) 

- 1x tooth washer (DIN 6797-A, M5, ST A2K) 

- 1x Quick Guide for Installation FR3 (Document number: R02040) 



Fig. 7.1: scope of delivery Arm 

###### Control 

- 1x Control 

- 1x country-specific power cable 



Fig. 7.2: scope of delivery Control 

###### Devices 

- 1x External Enabling Device 

- 1x Emergency Stop Device 



Fig. 7.3: Scope of delivery devices 

R02210/1.4/EN 

Franka Robotics GmbH © 

48 

SCOPE OF DELIVERY AND ADDITIONAL EQUIPMENT Accessories 

- 1x Connecting cable 



Fig. 7.4: Scope of delivery Connecting cable 

#### **7.2 Not included in the box** 

For additional accessories, e.g., cobot pump, visit https://franka.world/. 

The following equipment is not included: 

- Interface device 

   - Tablet/NOTICEbook/PC 

      - The interface device should be equipped with a browser (Chrome, Chromium, or Firefox), an Ethernet port, and ideally with touch functionality. 

- Material 

   - Ethernet cable with RJ 45 connector for connecting the interface device to the Arm 

   - Ethernet cable with RJ 45 connector for optional connection of the Control to the company network or PC workstation 

   - Mounting accessories (recommended by Franka Robotics): 2x 6 mm h8 pins for precise mounting of the Arm, if applicable 

   - Baseplate to mount the Arm (depending on the baseplate, different screws and washers may be needed, see table in chapter 10.4“Mounting the Arm”) 

   - Functional earth cable with eye 

- Tools 

   - Hex key for mounting the Arm on the baseplate 

   - Screwdriver for connecting the functional earth cable 

   - Level for ensuring the horizontal installation of the Arm 

   - Torque spanners to tighten screws with 30 Nm 

#### **7.3 Available Spare Parts and Accessories** 

The spare parts for Franka Research 3 include but are not limited to: 

- Arm 

- Control incl. country-specific power cable 

- External Enabling Device 

- Emergency Stop Device 

- Connecting cable (2.5 m, 5 m, or 10 m) 

- Emergency Unlocking Tool 

- Franka Hand (Not part of the certified machinery) 

- Cobot pump (Not part of the certified machinery) 

R02210/1.4/EN 

Franka Robotics GmbH © 

49 

###### TECHNICAL SPECIFICATIONS 

## **8 TECHNICAL SPECIFICATIONS** 

|||**ARM**||
|---|---|---|---|
|Degrees of freedom|7|Interfaces|• Ethernet (TCP/IP) for visual<br>|
|Payload|3 kg||intuitive programming with Desk<br>• Safety-rated inputs for emergency|
|Maximum reach|855 mm||<br>stop and external enabling device|
|Force/Torque sensing|Link-side torque sensor in<br>all 7 axes||• 2 configurable safety-rated inputs<br>for safeguards or other protective<br>|
|Joint position limits|A1, A3<br>-166° / 166°||devices (OSSD devices via external<br>OSSD converter connectable)|
||A2<br>-105°/105°<br>A4<br>-176°/-7°<br>A5<br>-165°/165°||• Hardware prepared for: 2x DI & 2x<br>DO (24V, isolated, EN 61131-2<br>type 3  characteristics, 100 Hz<br>sampling rate)|
||A6<br>25°/265°||• Control connector|
||A7<br>-175°/175°||• Connector for end effector|
|Mounting flange|DIN ISO 9409-1-A50|||
|Installation position|Upright|User Interfaces at the|• Iintegrated safety-rated guiding<br>|
|Weight|~17,8 kg|Arm's Pilot Grip|enabling switch<br>•Guiding button|
|Protection rating|IP40||<br>• Guiding mode button|
|Ambieant temperature|+5°C to +45°C|User Interfaces at the|• Status light|
|Air humidity|20-80%,|Arm's Pilot Disc|• Pilot mode selector|
||non-condensing||• Arrow keys, teach, confirm, delete|
|**CO**|**NTROL**|**PERF**|**ORMANCE**|
|Control size (19“)|483 x 355 x 89 mm (L x W x H)|**Motion**||
|Supply voltage|100-240 VAC|Joint velocity limits|A1-A4: 150°/s|
|Mains frequency|50-60 Hz||A5-A7: 301°/s(with FCI use A6: 239°/s)|
|Power consumption|~ 80 W|Cartesian velocity limits|up to 2 m/s end effector speed|
|Active power factor<br>correction (PFC)|yes|Pose repeatability<sup>1</sup>|< ±0,1 mm (ISO9283)|
|Weight|~ 7 kg|**Interaction**||
|Protection rating|IP20|Guiding force|~ 2,5 N|
|Ambient temperature|+5 °C to +45 °C|Adjustable translational<br>stiffness|10-3000 N/m|
|Air humidity|20-80 %, non-condensing|Adjustable rotational stiffness|1-300 Nm/rad|
|Permittet mounting<br>orientation|horizontal|Monitored signals|joint position, velocity,<br>torque cartesian position, force|



1 The above values refer to a workspace of 0.4 x 0.4 x 0.4 m with [0.498/0.0/0.226]m measured as the center point, with the Z-axis of the flange oriented parallel to the earth's gravity and the elbow pointing upward (based on ISO 9283, Appendix A). 

R02210/1.4/EN 

Franka Robotics GmbH © 

50 

###### TECHNICAL SPECIFICATIONS 

|Interfaces<br>• Ethernet (TCP/IP) for<br>internet and/or shop-|**ADD**|**-ONS**|
|---|---|---|
|<br>floor connection<br>• power connector IEC<br>60320C14 (V-Lock)<br>• Arm connector|Fully integrated end effectors<br>Fieldbusses|• 2-finger gripper<br>• Vacuum gripper<br>• Modbus/TCP<br>|
|||• OPC UA|
|**EXCLU**|**SIVE**||
|Research interface<br>1kHz Franka Control Interface (|FCI)||
|**SAFE**<br>**Certification**|**TY**||
|EN ISO 13849-1:2015 safety of machinery -<br>safety-related parts of control systems|certified by TÜV SÜD Product S|ervice|
|**Collaborative operation modes**|||
|Safety-rated monitored stop|fully integrated in PLd / Cat. 3||
|Hand-guiding|fully integrated in PLd / Cat. 3||
|Safety-rated speed and separation monitoring|realizable in combination with e<br>PLd / Cat. 3|xternal protective devices up to|
|**Safety parametrization & validation**|||
|Watchman|user interface to set and validat|e safety-related parameters|
|User management|role based access management||
|**Safety Functions**|||
|Emergency Stop (x3.1)|PLd / Cat. 3||
|External Enabling Device (x4)|PLd / Cat. 3||
|Enabling Button|PLd / Cat. 3||
|Two configurable safe inputs (x3.2 und x3.3)|PLd / Cat. 3||
|SLP-C: Safely limited Cartesian position|PLd / Cat. 3NOTICE: FCI cannot|control the robot while SLP-C is active|
|SLS-C: Safely limited Cartesian speed|PLd / Cat. 3NOTICE: FCI canno|t control the robot while SLS-C is active|
|SLP-J: Safely limited joint angle|PLd / Cat. 3NOTICE: FCI canno|t control the robot while SLP-J is active|
|SLS-J: Safely limited joint speed|PLd / Cat. 3||
|SLD: Safely limited distance|PLd / Cat. 3||
|SEEPO: Safe End Effector Power off|PLb / Cat. b||
|**Stopping Functions**|||
|Category 0 stop|PLd / Cat. 3||
|Category 1 stop|PLd / Cat. 3||
|Category 2 stop|PLd / Cat. 3||
|Worst case safe Cartesian position accuracy for stopping functions|50 mm||
|**Safety values according to EN ISO 13849-1**|||
|PFH of PLd / Cat. 3 safety functions (Probability of Failures per Hour)|< 1 x 10<sup>-7</sup>||
|PFH of PLb / Cat. b safety functions (Probability of Failures per Hour)|< 1 x 10<sup>-7</sup>||



R02210/1.4/EN 

Franka Robotics GmbH © 

51 

TECHNICAL SPECIFICATIONS 



R02210/1.4/EN 

Franka Robotics GmbH © 

52 

TECHNICAL SPECIFICATIONS 

**_NOTICE_** The probability of failure per hour was evaluated at 40 °C. However, the safety rating holds for all functions within the temperature range, including the extended temperature range. If the system probability of failure per hour values are used for calculation, take the temperature into account. For more information on the probability of failure per hour, contact Franka Robotics at support@franka.de. 

R02210/1.4/EN 

Franka Robotics GmbH © 

53 

###### TRANSPORT AND HANDLING 

## **9 TRANSPORT AND HANDLING** 



###### **WARNING** 

###### **Heavy equipment** 

Due to the dead weight and geometric design, lifting and handling the equipment may cause back injury, and, if it falls, serious injury to fingers, hands, toes, and feet. 

- Always wear personal protective equipment (e.g., safety shoes) when transporting, mounting, or demounting the equipment. 

- The equipment must be placed on even surfaces to prevent it from tilting or sliding. 

- Follow the company regulations on lifting loads and personal protective equipment. 



###### **WARNING** 

**Damaged components** 

Electrical risks may lead to severe injury. 

- Check if the packaging is in sound condition and fulfils its protective function. 

- Check the cables, plugs, and mechanical housing for cracks and broken insulations. 

- Do not use damaged cables, plugs, and mechanical housing for operation. In cases of doubt, contact Franka Robotics. 

###### **_NOTICE_** 

**Material damage to Arm and Control** 

Mechanical shock may cause damage or loss of calibration of sensitive electromechanical components in the Arm and the Control. 

- Avoid shock. 

- Carefully set down the devices. 

- Always store and transport the devices in their original packing, even for short-distance transport. 

###### **_NOTICE_** 

**Material damage to Arm, end effectors, and objects in the maximum workspace** 

Sensitive electromechanical components in the Arm and end effectors may be damaged if end effectors are connected to the Arm while bringing it into transport position. 

- Dismount any end effector before bringing the Arm into transport position. 

- Do not leave loose objects in the maximum workspace. 

R02210/1.4/EN 

Franka Robotics GmbH © 

54 

###### TRANSPORT AND HANDLING 

#### **9.1 Ambient Conditions for Delivery and Transport** 

The system can be stored and transported within the temperature range of -25 °C to +70 °C. 

###### **Handling and lifting** 

Always lift the Arm in the positions intended for lifting (see graphic below) to not overstress the Arm joints during handling and lifting. In particular, the Arm may never be carried in the extended position with one person holding each end of the Arm. 



Fig. 9.1: Lifting positions 

###### **_NOTICE_** 

###### **Material damage to the Arm** 

Moving the Arm by force in a locked state will lead to a momentary slipping of internal parts which causes loss of calibration and damage to the Arm. 

- Handle, lift, and transport the Arm only at the points indicated in this manual to avoid overstressing the joints of the Arm. 

- The Arm is to be handled gently even when set-up and switched on or off. 

###### **_NOTICE_** 

Do not step or lean on the Arm. 

###### **_NOTICE_** 

Pay attention to the weight. 

The weight of the Arm is approx. 17,8 kg 

R02210/1.4/EN 

Franka Robotics GmbH © 

55 

MOUNTING AND INSTALLATION 

## **10 MOUNTING AND INSTALLATION** 



###### **WARNING** 

###### **Heavy equipment** 

Due to the dead weight and geometric design, lifting and handling the equipment may cause back injury, and, if it falls down, serious injury to fingers, hands, toes, and feet. 

- Always wear personal protective equipment (e.g., safety shoes) when transporting, mounting, or demounting the equipment. 

- Always lift the equipment with the help of a second person. 

- The equipment must be placed on even surfaces to prevent it from tilting or sliding. 

- Follow the company regulations on lifting loads and personal protective equipment. 

###### **_NOTICE_** 

Before mounting and installing the system, read chapter 4 “SAFETY” and chapter 9 “TRANSPORT AND HANDLING” carefully. 

###### **_NOTICE_** 

Arm does not stand stable without being screwed at the base. 

###### **Overview of interfaces provided by Control and Arm** 



Fig. 10.1: Overview of interfaces 

R02210/1.4/EN 

Franka Robotics GmbH © 

56 

###### MOUNTING AND INSTALLATION 

#### **10.1 Unpacking the Equipment** 





R02210/1.4/EN 

Franka Robotics GmbH © 

57 

###### MOUNTING AND INSTALLATION 

###### **Unboxing** 

###### Procedure 

1. Take off the top lid of the outer box. 



Fig. 10.3: Unpack main carton 

2. Lift the top inner boxes and put them aside. 



Fig. 10.4: Removal of individual cartons 

3. Pull the outer box apart to access the bottom inner box. 



Fig. 10.5: Inner cartons 

R02210/1.4/EN 

Franka Robotics GmbH © 

58 

###### MOUNTING AND INSTALLATION **Unpacking the Arm** 

Procedure 

1. Carefully open the box by removing the sealing adhesive strips on top of the cardboard box. 

2. Open the foil coating. 

3. Remove the top protective layer. 



Fig. 10.6: Open box from Arm 

4. Remove the middle protective layer. 



Fig. 10.7: Unpack arm 

5. Grasp the Arm at the indicated lifting positions carefully, lift it out of the bottom protective layer, and set it aside. 



Fig. 10.8: Lift out arm 

R02210/1.4/EN 

Franka Robotics GmbH © 

59 

###### MOUNTING AND INSTALLATION **Unpacking the Control** 

Procedure 

1. Carefully open the box by removing the sealing adhesive strips on top of the cardboard box. 

2. Open the foil coating. 

3. Remove the power cable and the top lid. 



Fig. 10.9: Open box of control 

4. Remove the top protective layer. 



Fig. 10.10: Removal packaging 

5. Grasp the Control at the indicated lifting positions, carefully lift it out of the bottom protective layer, and set it aside. 



Fig. 10.11: Lift out  control 

R02210/1.4/EN 

Franka Robotics GmbH © 

60 

###### MOUNTING AND INSTALLATION 

#### **10.2 Correct Installation Site** 

##### **10.2.1 Maximum-and safeguarded space** 

###### **Classification of spaces** 



Fig. 10.12: Classifcation of spaces 



- Maximum workspace 

   - Space that can be swept by the robot's moving parts plus the space which the end effector and the workpiece can sweep. 

- Safeguarded space 

Defined by the perimeter safeguarding (see graphic) 

###### **_NOTICE_** 

Utilize the provided safety functions to mitigate any risks of accidental collisions from an unexpectedly moving Arm. Monitoring functions are only triggered upon violation. The safety integrator must consider stopping times, distances, and tolerances. 

###### **_NOTICE_** 

Application-specific risk analysis may define a hazardous zone larger than the maximum workspace in some applications. 

R02210/1.4/EN 

Franka Robotics GmbH © 

61 

###### MOUNTING AND INSTALLATION 

##### **10.2.2 Ambient conditions: Arm** 

###### **Permissible conditions at the site of installation** 

###### Ambient temperature 

- +15 °C to +25 °C (normal) 

- +5 °C to +45 °C (extended) 

- IP 20 

- Normal operations (no-derating): +15°C to +25°C, 60% not condensing humidity 

- Extended operations (no de-rating of safety system, de-rating of performance possible) : +5°C to +45°C, 90% not condensing humidity 

- Storage and transport : -10°C to +60°C 

###### Relative air humidity 

- 20 % to 80 %, non-condensing 

###### Site of installation 

- Indoors, in enclosed buildings 

- Not exposed to direct sunlight 

- No vibrations, no accelerating fundaments 

- Magnetic fields are only permissible in the stated specification range. See chapter 4.2 “Notice of Liability”. 

###### Orientation of installation 

- Arm may only be installed vertically (base horizontal to the earth’s surface, no hanging Arm) 

###### Ambient medium 

- Air 

- Free from flammable substances (dust, gas, liquid) 

- Free from aggressive media 

- Free from corrosive substances 

- Free from flying objects 

- Free from spraying liquids 

- Free from pressurized air streams 

###### Pollution degree 

- Degree 2 (according to EN 60664) 

- Only dry, non-conductive pollution occurs; occasionally, temporary conductibility caused by condensation may occur 

###### Setup altitude 

- ≤ 2,000 m above sea level 

###### Electromagnetic compatibility 

- Environment conditions must adhere to general industrial equipment according to EN 61000-6-4 as the system is designed for respective emission tolerance according to EN 61000-6-2 

###### **_NOTICE_** 

In order not to endanger the safety functionality of the system, ensure pollution degree 2 according to EN 60664. 

R02210/1.4/EN 

Franka Robotics GmbH © 

62 

MOUNTING AND INSTALLATION 

###### **Adequate ventilation** 

###### **_NOTICE_** 

The heat produced by power electronic components and modules inside the Arm is dissipated via the Arm’s surface. 

- Install the Arm in an adequately ventilated place. 

- Do not expose the Arm to direct sunlight. 

- Do not repaint, paste up, or wrap up the Arm. 

###### **Ergonomic consideration** 

###### **_NOTICE_** 

To avoid overheating, the system will stop working when it exceeds the extended temperature range. The user will be informed through Franka UI. 

Follow further instructions in Franka UI. 

###### **_NOTICE_** 

To avoid overheating of the motors, the system will stop working, if the internal sensors detect excess temperatures in the windings. The user will be informed through Franka UI. 

Follow further instructions in Franka UI. 

###### **_NOTICE_** 

Install the Arm in an ergonomic teaching position. 

##### **10.2.3 Ambient conditions: Control** 

###### **Permissible conditions at site of installation** 

Ambient temperature 

   - +15 °C to +25 °C (normal) 

   - +5 °C to +45 °C (extended) 

- Relative air humidity 

   - 20 % to 80 %, non-condensing 

- Site of installation 

   - Indoors, in enclosed buildings 

   - Not exposed to direct sunlight 

   - No vibrations 

   - Magnetic fields are only permissible in the stated specification range. See chapter 4.2 “Notice of Liability” 

   - Enclosure needs a minimum degree of protection corresponding to IP4X or IPXXD if located in places open to all persons 

R02210/1.4/EN 

Franka Robotics GmbH © 

63 

###### MOUNTING AND INSTALLATION 

Orientation of installation 

- Device may only be installed horizontally on the earth’s surface 

- Mounting in angle brackets, e.g., under tables 

- Mounting in control cabinets (2U, 4HP) 

###### Power supply 

- In order to ensure stability and safety of the system, provide a stable power supply that maintains enough power to the control to shut down in a controlled fashion, when the power supply is shut off. 

###### Ambient medium 

- Air 

- Free from flammable substances (dust, gas, liquid) 

- Free from aggressive media 

- Free from corrosive substances 

- Free from flying objects 

- Free from spraying liquids 

- Free from pressurized air streams 

Pollution degree 

- Degree 2 (according to EN 60664) 

- Only dry, non-conductive pollution occurs; occasionally, temporary conductibility caused by condensation may occur 

Setup altitude: 

- ≤ 2,000 m above sea level 

###### **_NOTICE_** 

If it is not open to all persons, only pollution degree 2 is relevant and needs to be ensured. 

###### **_NOTICE_** 

In order not to endanger the safety functionality of the system, ensure pollution degree 2 according to EN 60664. 

The enclosure mentioned above is not suitable to protect from higher pollution degrees. Here, an even higher IP is needed. 

R02210/1.4/EN 

Franka Robotics GmbH © 

64 

MOUNTING AND INSTALLATION 

#### **10.3 Preparing the Installation Site** 

###### **Correct installation site** 

Before installation, prepare the installation site. See chapter 10.2 “Correct Installation Site“. 



###### **WARNING** 

**Malfunctions and unexpected motions due to improper installation** 

- Risk of severe injury, such as crushing of fingers, hands, upper body, head. 

- Only switch on the robot when the Arm is properly installed on the platform. 

- Only install the Arm on even, unmoving, and stable platforms. Accelerations and vibrations induced by the platform are not permissible. 

- Do not install the Arm hanging or on tilted or uneven platforms. 

- Level the platform and install the robot in an upright position. 

- Tighten the screws after 100 hours of operation with the correct tightening torque. 

##### **10.3.1 Arm** 

###### **Derating** 

When operating Franka Research 3 within the extended temperature range, the user may need to reduce the dynamic parameters (acceleration, maximum speed, etc.) to avoid overheating the system and its components. Otherwise, Franka Research 3 stops its operation. 

###### **Stable platform** 

The Arm is equipped with highly sensitive sensor technology and fine-tuned control algorithms. The control algorithm requires installation on a stable, leveled, non-moving, and non-vibrating platform in an upright position. The maximum permitted tilt angle is 0.1°. 

The following maximum forces must be supported during static and dynamic operation from mounting base: 

- tilting torque: 280 Nm 

- torque around axis: 190 Nm 

- horizontally force: 300 N 

- vertical force: 410 N 



Fig. 10.13: Preparing the baseplate 

|1<br>Tilting torque|4<br>Horizontal force|
|---|---|
|2<br>Torque around axis|5<br>Vertical force|



R02210/1.4/EN 

Franka Robotics GmbH © 

65 

MOUNTING AND INSTALLATION 

<u><mark>3</mark> Front</u> <u><mark>6</mark> Leveled surface</u> 

###### **Preparing the baseplate** 

Required material 

- Detailed mounting layout for baseplate 

###### Procedure 

- Use the technical drawing for positioning the holes. 

###### **_NOTICE_** 

NOTICE the position of the Arm in the technical drawing and align it on the baseplate accordingly. 

The hole spacing is designed to be compatible with flexible assembly parts by ITEM. Two holes (Ø 6 mm H7) for dowel pins in the mounting flange allow for accurate, repeatable assembly of the Arm using 2 x Ø6 h8 pins (see table in chapter 10.4 “Mounting the Arm”). 



Fig. 10.14: Drilling template 



##### **10.3.2 Control** 

###### **Installation site** 

Place the Control horizontally in its intended location. 

Alternative: 

Install the Control in a rack designed for 19-inch equipment. For further information, refer to chapter 10.2 “Correct Installation Site” 

R02210/1.4/EN 

Franka Robotics GmbH © 

66 

###### MOUNTING AND INSTALLATION 

**_NOTICE_** 

The power supply connection must be established via suitable equipment, e.g., by using the supplied countryspecific cable. 

Make sure that the main supply and main switch are easily accessible. 

###### **Adequate ventilation** 

###### **_NOTICE_** 

The heat produced by power electronic components and modules inside the Control is dissipated through an internal ventilation system. 

- Install the Control in an adequately ventilated place. 

- Do not expose the Control to direct sunlight. 

- Place the Control at a sufficient distance between the front/back fans and covering components (40 mm on both sides). 

- Make sure that the Control's fans are not covered with dirt. 



###### **WARNING** 

###### **Heavy equipment** 

Due to the dead weight and partly due to the geometric design, lifting and handling the equipment may cause back injury and, if it falls, serious injury to fingers, hands, toes, and feet. 

- Always wear personal protective equipment (e.g., safety shoes), when transporting, mounting, or demounting the equipment. 

- The equipment must be placed on even surfaces to prevent it from tilting or sliding. 

- Follow the company regulations on lifting loads and personal protective equipment. 

#### **10.4 Mounting the Arm** 

The Arm must be connected securely to the baseplate with four suitable-sized screws. For this purpose, four drill holes with a diameter of 9 mm are provided in the base flange of the Arm. 

Use only the designated lifting points to lift the Arm. 

Required tools and material 

- Washers and screws depend on the surface the robot is mounted on. Please check the table below for details. 

- 1x cylindrical head screw with hexagon socket M5x8 (strength class 8.8 A2K) 

- 1x tooth washer M5 (strength class A2K) 

- Torque spanners to tighten screws with 30 Nm 

||**Robot on aluminum table**|**Robot on steel table**|**Robot on ITEM aluminum profiles**|
|---|---|---|---|
|**Screws**|ISO 4762 - M8x25 - 10.9|ISO 4762 - M8x20 - 10.|9 (included in the scope of delivery)|
|**Washers**|ISO 7089-8,4-HV300 Washe|rs (included in the scope of|delivery)|
|**Minimal thread length**|16 mm|11 mm|Line 8 construction profiles|
|**Tightening torque**|30 Nm|||



R02210/1.4/EN 

Franka Robotics GmbH © 

67 

###### MOUNTING AND INSTALLATION 

**Other** Only use ITEM 0.0.420.83 Heavy Duty T-Slot M8 Nuts. 

###### **_NOTICE_** 

###### **Material damage to the Arm** 

- Moving the Arm by force in a locked state will lead to a momentary slipping of internal parts which causes loss of calibration and damage to the Arm. 

- Handle, lift, and transport the Arm only at the points indicated in this manual to avoid overstressing the joints of the Arm. 

- The Arm is to be handled gently even when set up and switched on or off. 

R02210/1.4/EN 

Franka Robotics GmbH © 

68 

###### MOUNTING AND INSTALLATION 

###### **_NOTICE_** 

Make sure that the maximum forces and torques are supported during static and dynamic operation. For more information, see section Stable platform in 10.3 “Preparing the Installation Site”. 

###### Precondition 

- Two people are required for mounting the Arm. 

- Prepared baseplate. See section Preparing the Baseplate in chapter 10.3 “Preparing the Installation Site”. 

###### Procedure 

1. Lift the Arm. 

2. Carry the Arm to its designated position. 

3. Align the Arm accordingly to the pre-fixed holes on the baseplate. 

4. Person 1: Hold the Arm. 

   - Person 2: Use the four screws to mount it to the baseplate with a tightening torque of 30 Nm. 



Fig. 10.15: Mounting of the arm 

   5. Connect the functional earth to the base of the Arm. 

- _The Arm is successfully mounted to the baseplate._ 

**_NOTICE_** 

The Arm should not be powered until correct mounting is validated again. 

R02210/1.4/EN 

Franka Robotics GmbH © 

69 

###### MOUNTING AND INSTALLATION 

#### **10.5 Positioning the Control** 



###### **WARNING** 

###### **Heavy equipment** 

Due to the dead weight and partly due to the geometric design, lifting and handling the equipment may cause back injury and, if it falls, serious injury to fingers, hands, toes, and feet. 

- Always wear personal protective equipment (e.g., safety shoes), when transporting, mounting, or demounting the equipment. 

- The Control must be placed on even surfaces to prevent it from tilting or sliding. 

- Follow the company regulations on lifting loads and personal protective equipment. 

###### **_NOTICE_** 

###### **Material damage to Arm and Control** 

Moving the Arm by force in a locked state will lead to a momentary slipping of internal parts which causes loss of calibration and damage to the Arm. 

- Avoid shocks. 

- Carefully set down the devices. 

- Always store and transport the devices in their original packing, even inside buildings. 

###### **Positioning** 

###### Procedure 

1. Person 1: Grasp the Control at the indicated lifting positions. 

2. Person 2: Remove the foam packaging from the Control. 

3. Place the Control horizontally in its designated position and ensure that proper ventilation is provided. Alternative option: 

Attach the Control in a rack designed for 19-inch units. For more information, see chapter 10.2 “Correct Installation Site”. 

R02210/1.4/EN 

Franka Robotics GmbH © 

70 

###### MOUNTING AND INSTALLATION 

#### **10.6 Wiring and Electrical Installation** 

###### **Sound condition** 



###### **DANGER** 

- **Damaged wires or inadequate electrical installation** 

- Risk of personal injury by electric shock, as well as material damage 

- Only use Franka Research 3 in sound technical condition. 

- Only install the emergency stop and safety peripherals system with qualified personnel. 

- Check cables and electrical installations. 

- **CAUTION** 

- **Exposed wires and cables** Operators may trip and fall due to exposed wires and cables in the maximum workspace. Therefore: • Always lay cables safely. 

**_NOTICE_** 

Only devices with galvanic isolation up to 60 V in the Ethernet port may be connected to the system. 

**_NOTICE_** 

Do not swap or unplug the connected Arm while the Control is powered on. 

R02210/1.4/EN 

Franka Robotics GmbH © 

71 

MOUNTING AND INSTALLATION 

##### **10.6.1 Connection diagram** 



Fig. 10.16: Overview connection diagram 

##### **10.6.2 Interfaces** 

###### **X2 - Digital IOs** 

The Interface X2 is located at the robot’s base. This provides a hardware interface for non-safe digital inputs and outputs. This interface is not enabled in all - especially older - software versions. 

The inputs and outputs and the 24 V power supply provided on X2 are galvanically isolated from the robot system and other interfaces at the robot. 

The connector is a female 8-pin M12 connector with A coding. 

The 24V power supply is driven by the robot. Feeding power into these pins is neither necessary nor permitted. The maximum total output current for the 24 V pins and the digital outputs is 500 mA. 

###### Input characteristics 

- 24 V input according to IEC 61131-2 type 3 

- 15 kHz low-pass input filter 

- Sampling frequency 1 kHz 

Output characteristics 

- Output high level 24 V DC; Output current per output max. 250 mA 

- Update frequency 1 kHz 

R02210/1.4/EN 

Franka Robotics GmbH © 

72 

###### MOUNTING AND INSTALLATION 



Fig. 10.17: X2 interface 

###### **X3 - Safe inputs** 

Safe inputs (X3.n) always have two separate channels, designated A and B. Each channel is implemented via its p- and n-pins which have to be connected via a floating switch. During regular operation, both channels must be in the same state (open/closed) and not be connected; any other state will trigger a failure in the safety system. 

The safe inputs are galvanically isolated from the robot system and other interfaces at the robot, although all safe inputs share a common electrical domain, regardless of their interface connector. 

Interface X3 is located at the base of the robot arm and carries three safe input signals. X3.1 provides the emergency stop integration of the robot, X3.2 and X3.3 provide two freely configurable safety inputs. The connector is a female 12-pin M12 connector with A coding. 

Safe Inputs electrical domain characteristics for X3: 

- signal voltage 24 V; signal current 30mA 



Fig. 10.18: X3 - Safe Inputs 

###### **X4 - External enabling** 

Interface X4 is located at the base of the robot arm and carries one safe input signal. The connector is a female 4-pin M12 connector with A coding. This connector is intended for the temporary connection of the External Enabling Device during operating phases when this is required. 

If possible, always use the external enabling device supplied. 

###### **_Notice_** 

If a separate external enabling device is to be used, the external enabling device must comply with IEC 60204 1 and DIN EN 60947 5 8. 

R02210/1.4/EN 

Franka Robotics GmbH © 

73 

###### MOUNTING AND INSTALLATION 

###### **X5 - Robot network** 

The X5 connector is located on the robot base and provides the internal robot network via an Ethernet socket. The robot network has an integrated DHCP server. The operating device can be connected to X5. By entering the URL robot.franka.de, you can access the Franka UI web interface of the robot. The IP address of the X5 interface can be configured in the settings. 

The default setting has the stored IP address 192.168.0/24. The robot can then be reached under the IP address 192.168.0.1. The DHCP server assigns addresses in the range 100 to 150 to the clients, i.e. with default settings 192.168.0.100 to 192.168.0.150. 

###### **X6 - End effector** 

Interface X6 is located at the wrist of the robot arm and carries signals from the robot connecting to the end effector. The connector is a Binder 8-pin female Snap-in IP67 Series 620. 



Fig. 10.19: X6 interface 

- Nominal voltage 48 ± 3 VDC. 

- Nominal hold current 0.5 A at 25°C. 

- Maximal capacitive load 220 µF. 

The End effector interface does not exchange any safety-related information. No discrete nor protocol-based means of safe data transfer is provided. No 48 V power supply is available on this interface if SEEPO is active. No earthing is provided in the end effector supply. 

If additional devices are connected, please test whether the intended function works as expected. 

###### **C2 Network connection** 

The C2 interface is located on the front of the control unit. It provides an Ethernet connection via which the control unit can be connected to a system/company network and also to the Internet. 

The network connection can be configured in the settings. The DHCP client is activated for this interface in the default settings. It is also possible to manually set the network connection for integration into an existing network. Please note that the robot network and the company network must not have an identical IP address range. 

R02210/1.4/EN 

Franka Robotics GmbH © 

74 

MOUNTING AND INSTALLATION 

##### **10.6.3 Connecting the functional earth** 

###### **_NOTICE_** 

It is required to connect the functional earth to meet the stated EMC levels. 

###### Required material 

- M5 screw thread 

- 1x tooth washer M5 

- Functional earth cable 

We recommend using a minimum 1.5 mm<sup>2</sup> section Cu cable, with a maximum length of 5 m. 





###### Procedure 

1. Connect the functional earth to the M5 thread of the Arm’s base at the indicated position on one side and to a nearby, well-grounded part (e.g., a solid metal grounding bar) on the other side. 

2. Position the tooth washer M5 at the indicated position at the Arm's base for the functional earth. 

3. Secure the cable lug of the functional earth cable with the M5 screw. 

4. Connect the other side of the cable to a nearby, well-grounded part (e.g., a solid metal grounding bar). 

###### **_NOTICE_** 

The electrical safety of the system does not depend on a functional earth connection. A functional earth connection is not suited to propagate protective bonding to attached equipment like end effectors. All equipment in the vicinity of the robot must be installed in accordance with their respective electrical requirements, including protective bonding, if applicable. 

R02210/1.4/EN 

Franka Robotics GmbH © 

75 

###### MOUNTING AND INSTALLATION 

##### **10.6.4 Wiring** 

###### **_NOTICE_** 

The Arm connection cable, emergency stop cable, External Enabling Device cable, and user specific cabling shall not be extraordinarily subjected to the following: 

- Mechanical handling and dragging across rough surfaces (abrasion) 

- Operation without guides (kinking) 

- Guide rollers and forced guiding, being wound and re-wound on cable drums (stress) 

- High tensile stress, small radii, bending into another plane and/or frequent duty cycles 

###### **Connecting Arm to Control** 

Required material: 

- Connecting cable 

###### **_NOTICE_** 

Only connecting cables provided by Franka Robotics shall be used for electrical connection between Arm and Control. 

###### **Procedure** 

1. Carefully place the connector port (female site) onto the connector X1 and ensure that the triangular marking points upward. 





Fig. 10.21: Connection of connecting cable  the arm 

2. The plug itself is pulled into the connector port by turning the movable front part of the connector. 

3. Turn hand-tight and test correct fit by slightly pulling the plug. 

4. Apply the same principle to connect the other end of the connecting cable (male site) with the connector C1 on the front of the Control. 

R02210/1.4/EN 

Franka Robotics GmbH © 

76 

###### MOUNTING AND INSTALLATION 



Fig. 10.22: connection of connecting cable to the control 

###### **Connecting External Enabling Device** 

Required material: 

- External Enabling Device supplied 

###### Procedure 

1. Make sure that the guide pin is pointing in the right direction. 

2. External Enabling Device to the X4 connector. 



Fig. 10.23: Connection of external Enabeling Device 

3. The plug itself is pulled into the connector port by turning the movable front part of the connector. 

4. Turn hand-tight. 

###### **Connecting your operating device (for operation via Franka UI)** 

Required material: 

- Interface device ( see chapter 11.3 “Initial configuration”) 

- Ethernet cable with RJ 45 connector (not included) 

###### Procedure 

- Connect your interface device and the connector X5 at the Arm base with the Ethernet cable. 

R02210/1.4/EN 

Franka Robotics GmbH © 

77 

###### MOUNTING AND INSTALLATION 



Fig. 10.24: Connection of operating device 

###### **Connecting the Control with the power supply** 

###### **_NOTICE_** 

Make sure to connect the mandatory locking mechanism to the C14 connector on the power supply cable. 

**_NOTICE_** Allowed supply frequency: 50 − 60 Hz Supply voltage: 100 - 240 VAC Earth leakage: < 10 mA 

Required material: 

- Country-specific power cable 

###### Procedure 

1. Connect the power cable to the Control. 

2. Connect the power cable to the power supply. 

###### **Connecting protective devices** 

If you want to connect external safety devices to slow down the arm and / or bring it to a standstill by means of category 1 or 2 stops (according to IEC 60204 1), please read chapter 4.7 “Installation of Safety Peripherals". 

R02210/1.4/EN 

Franka Robotics GmbH © 

78 

###### MOUNTING AND INSTALLATION 



###### **WARNING** 

###### **Risk of injuries** 

Connecting external devices with a separate power supply may jeopardize the system safety functionality. Risk of severe injury, such as crushing, tearing of the skin, and puncturing from the Arm and end effectors. 

- Ensure that the voltages in the connected devices are either SELV or suitably isolated to systemconnected signals. 

###### **_NOTICE_** 

###### **Material damage** 

Connecting external devices with a separate power supply may cause system damage if not adhering to electrical ratings. 

- Voltages in connected devices must either be SELV or suitably isolated to system-connected signals. 

###### **_NOTICE_** 

- **Material damage of cables** 

Improper handling of cables leads to damage to the cables. 

- Do not bend, fold, or roll the connection cable. 

- Lay the connection cable such that it will not be overstressed. 

###### **_NOTICE_** 

###### **Material damage of Arm or end effectors** 

Unsafe connection or disconnection of live cables or end effectors during operation leads to equipment damage. 

- Do not connect or disconnect cables when Franka Research 3 is connected to the power supply. 

- Do not connect or disconnect end effectors when Franka Research 3 is connected to the power supply. 

###### **Using the supplied emergency stop device** 

###### Required material 

- Supplied emergency stop device or customer-provided protective device (not included in scope of delivery) 

- When using a customer-provided protective device: an additional connecting cable (not included in scope of delivery) 

###### Procedure 

1. connect the supplied emergency stop device to the X3 terminal. or 

R02210/1.4/EN 

Franka Robotics GmbH © 

79 

###### MOUNTING AND INSTALLATION 

Connect the customer-specific configurated matching connector to the X3 connection and the protective devices to be connected (not included in the scope of delivery). Connect the protective device to the X3 connector. 



Fig. 10.25: Connection of the protective device (here emergency stop command device) 

2. The plug itself is pulled into the connector port by turning the movable front part of the connector. 

3. Turn hand-tight 

For more information on safe inputs, refer to the "Safe input" section of chapter 4.11 „Safety Functionalities“. For more information on the safety functions, refer to the chapter 4.11 „Safety Functionalities“. 

For more information on the security settings, refer to chapter **Error! Reference source not found.** ” **Error! Re ference source not found.** “. 

For more information on the devices, refer to chapter 4.7 „Installation of Safety Peripherals“. 

**_NOTICE_** 

Safety devices need to be checked for proper functioning before initial operation and at regular intervals. 

#### **10.7 Mounting End Effectors** 



###### **WARNING** 

**Falling and/or flying tools from the end effectors** Tools that remain inserted in the end effector may turn into projectiles during later motions of the Arm and lead to injuries. 

- Do not leave any tools inside the robot. 



###### **CAUTION** 

- **Sharp-edged, pointed designs and moving parts** 

Attached end effectors may cause injuries to hands, fingers, upper body, and head. 

- Always wear personal protective equipment (e.g., safety goggles). 

- The integrator needs to perform a risk assessment of any attached end effector. 

R02210/1.4/EN 

Franka Robotics GmbH © 

80 

MOUNTING AND INSTALLATION 

• Do not stand in the maximum workspace during operation. 

###### **_NOTICE_** 

Connecting external devices with a separate power supply may jeopardize the system’s safety function if it does not adhere to electrical ratings. 

In addition, the voltages in the connected devices must either be SELV or suitably isolated from systemconnected signals. 

The arm has a flange for the mechanical connection of an end effector. The information on the end effector flange can be found in chapter 10.3.1 “Arm”. 

NOTICE that the pilot grip has a 45° twist to the end effector flange. 

###### **Interface X6 - End effector** 

The X6 electrical connection on the end effector flange can be used to supply power to the end effector if required and to communicate with the controller via the can bus. NOTICE that the X6 connection has been configured specifically for Franka Hand and other devices may not be compatible with this connection. If an end effector is to be coupled that cannot be directly connected to such a port, external wiring for power supply and control of the end effector can be designed and implemented accordingly. 

For detailed description of the wiring of interface X6 see chapter 10.6 “Wiring and Electrical Installation”. 

The end effector interface does not exchange any safety-related information. No discrete nor protocol-based means of safe data transfer is provided. No 48 V power supply is available on this interface if SEEPO is active. 



###### **CAUTION** 

###### **Opening and closing end effectors** 

- Malfunctions of the Control may lead to an unexpected opening and closing of end effectors **.** 

- Always wear personal protective equipment (e.g., safety goggles). 

- The integrator must perform a risk assessment on any attached end effector. 

- Do not stand in the maximum workspace during operation. 



###### **CAUTION** 

###### **Moving Arm** 

- Risk of severe injury, such as crushing, tearing of the skin, and puncturing 

- Always wear personal protective equipment (e.g., safety goggles). 

- The integrator must perform a risk assessment on any attached end effector. 

- Do not stand in the maximum workspace during operation. 

###### **_NOTICE_** 

After connecting an end effector, a risk assessment needs to be performed. The risk assessment depends on the end effector and includes but is not limited to the following: 

- Sharp-edged or pointed end effectors 

- Movement or rotation of sharp rotating end effectors 

- Unexpectedly moving Arm leading to the end effector impacting or crushing a human 

R02210/1.4/EN 

Franka Robotics GmbH © 

81 

###### MOUNTING AND INSTALLATION 

An additional risk assessment is required for risks of a possible end effector failure. The failure risk assessment depends on the end effector and includes but is not limited to the following: 

- Malfunction of the protective stop signal leading to not stopping of the end effector opening/closing 

- Evaluation of power-loss of the end effector and its functions 

- Control failures leading to unexpectedly opening/closing of the end effector 



For information on mounting and de-mounting the end effector, please see the respective end effector manual. 

#### **10.8 Practical Tips for Usage and Positioning of Franka Research 3** 

##### **10.8.1 Energy consumption** 

For standard operation, Franka Research 3 requires an average electrical power of 140–350 W. Temporarily, electrical power of up to 600 W can be drawn from the power supply. 

###### **_NOTICE_** 

In case of an unexpected power loss, Franka Research 3 attempts a Cat. 1 Stop. If the stored energy does not suffice, a Cat. 0 Stop will be performed. 

After an emergency stop, the Arm could have lost calibration or been damaged. If malfunctions are detected at the next start-up, the user will be informed and should follow the instructions in Desk. 

R02210/1.4/EN 

Franka Robotics GmbH © 

82 

MOUNTING AND INSTALLATION 

##### **10.8.2 ESD limits** 

**_NOTICE_** 

It is required to connect functional earth to meet stated EMC levels. 



Fig. 10.26: Measuring points ESD measurement 

The values in the table were measured at a temperature of 24.2 °C and relative humidity of 44 %. 

||**Resistance to ground RG **<br>**[Ohm]**|**Surface voltage [V]**|**Distance to ESDS [mm]**|
|---|---|---|---|
|**Coating robot (1)**|15,5 x 10<sup>9</sup>|13|0|
|**Forearm bumper (2)**|20,3 x 10<sup>9</sup>|30|0|
|**Wrist shell incl. Bumper (3)**|24,3 x 10<sup>9</sup>|850|25|
|**Flange (4)**|50,0 x 10<sup>3</sup>|0|0|
|**Pilot-Grip (5)**|25,7 x 10<sup>9</sup>|279|25|
|**Franka Hand (without fingertip) (6)**|38,1 x 10<sup>9</sup>|615|25|



The specified distances correspond to the DIN EN 61340-5-1 standard. Above 125 V to 2.000 V require 25mm spacing. 

###### **_NOTICE_** 

It is recommended to check the distances according to the application requirement and the DIN EN 61340-5-1 standard. 

##### **10.8.3 Design of the workspace** 



###### **WARNING** 

**Unexpectedly moving Arm** 

Risk of severe injury, such as crushing of fingers, hands, upper body, head. 

- Do not have sharp edges in the maximum workspace. 

- Do not keep any pointed objects in the maximum workspace. 

- Install the Arm in an ergonomic teaching position. 

R02210/1.4/EN 

Franka Robotics GmbH © 

83 

###### MOUNTING AND INSTALLATION 



Fig. 10.27: Design of the workspace 

When planning the installation, ensure that there is sufficient free workspace around the robot. 

###### **_NOTICE_** 

For recovery procedures in the event of a failure, it may be necessary to move the joints to the reference positions of the arm. It is therefore recommended to consider the position shown below in the setup planning so that the robot can reach the reference position if needed. 



Fig. 10.28: Joint reference position of the arm 

##### **10.8.4 Personal safety and ergonomics** 

**Free space for retracting** 

**_NOTICE_** 

The following information on how to use and place the Arm are practical tips and may not be exhaustive when it comes to a specific application. They do not replace a hazard and risk assessment but may suggest layout options. 

Humans instinctively retract from unexpected motions. Therefore, the area where the operator or other persons stand should allow for sufficient space to retract or recoil. 

Furthermore, ensure that this space is free of obstacles (e.g., cables, objects) to prevent people from tripping over them and harming themselves. 

R02210/1.4/EN 

Franka Robotics GmbH © 

84 

###### MOUNTING AND INSTALLATION **Greatest possible distance to the Arm** 



###### **WARNING** 

###### **Moving Arm** 

- Risk of being trapped by the Arm. 

- Keep the Arm at the greatest possible distance at any given time to allow the operator to react and retract. 

- Do not operate the Arm while embracing it. 

- Do not place your head or other body parts between or underneath segments of the Arm. 

- Do not place body parts (especially hands, fingers) between the Arm, the end effector, or stationary objects. 

- In case of acute mortal danger: 

   1. Press the Emergency Stop Device to stop the robot from operating. 

   2. Pull or push the Arm out of the dangerous position manually. 



Fig. 10.29: Distance to arm bumping the head 





Fig. 10.31: Distance to arm Squeezing the hand 

R02210/1.4/EN 

Franka Robotics GmbH © 

85 

###### MOUNTING AND INSTALLATION **Eye protection** 



###### **WARNING** 

**Unexpected movement of Arm and leaking oil** 

Contact with leaking oil may cause eye or skin irritation. 

The use of various applications, the handled end effectors, and surrounding objects may lead to crushing, tearing of the skin, and puncturing. 

- Always wear protective goggles. 

###### **Clothing and jewelry** 



###### **CAUTION** 

- **Loose clothing or jewelry getting caught in Arm** 

- Caught clothing or jewelry may cause imbalance and the risk of falling personnel. 

- Do not wear loose clothing or clothing with ribbons 

- Do not wear loose jewelry, e.g., necklaces or bracelets. 





###### **Further information** 

Corrosion might appear on visible surfaces. This does not affect the functionality of the robot. 

###### **_NOTICE_** 

The following information is practical and may not be exhaustive when it comes to preventing rust. In the event of rust, Franka Robotics assumes no warranty or liability, since rust does not impair the function. 

- Ensure compliance with humidity and temperature ranges during use, transport, and storage. 

- Store the robot in moisture-reducing materials, for example with drybags. 

- Only work with clean and dry hands especially during handling, installation, and when teaching a task. 

R02210/1.4/EN 

Franka Robotics GmbH © 

86 

###### MOUNTING AND INSTALLATION 

#### **10.9 Re-packing the Arm** 



###### **WARNING** 

###### **Heavy equipment** 

Due to the dead weight and partly due to the geometric design, lifting and handling the equipment may cause back injury and, if it falls, serious injury to fingers, hands, toes, and feet. 

- Always wear personal protective equipment (e.g., safety shoes), when transporting, mounting, or demounting the equipment. 

- Always lift the equipment with the help of a second person. 

- The equipment must be placed on even surfaces to prevent it from tilting or sliding. 

- Follow the existing company regulations on lifting loads and personal protective equipment. 

###### **_NOTICE_** 

**Material damage to Arm, end effectors, and objects in the maximum workspace** 

Sensitive electromechanical components in the Arm and end effectors may be damaged if end effectors are connected to the Arm while bringing it into transport position. 

- Dismount any end effector and attachments before bringing the Arm into transport position. 

- Do not leave loose objects in the maximum workspace. 

###### **_NOTICE_** 

**Material damage to Arm and Control** 

Mechanical shock may cause damage or loss of calibration of sensitive electromechanical components in the Arm and Control. Avoid shock. 

- Do not set down the devices roughly. 

- Always store and transport the devices in their original packing, even inside buildings. 

###### **Transportation pose of the Arm** 

To bring Franka Research 3 into transport mode, use the Move to pack pose function in Settings in Franka UI. 

Precondition 

- The end effector and attachments must be removed from the Arm. 

- The robot needs to move freely without being encumbered by obstacles to adopt the transport pose. In case of obstacles in the robot cell, consider moving the robot closer to the transport pose via handguiding. 



To remove the end effectors from the Arm, see the instructions in the product manual of the end effector. 

R02210/1.4/EN 

Franka Robotics GmbH © 

87 

###### MOUNTING AND INSTALLATION 

###### Procedure 

1. Log onto at the user interface in Franka UI. 

2. Click on Settings. 

3. Navigate to System. 

4. Click and hold the “Move to pack pose” button. 

_The Arm will automatically move to the transport pose while the button is pressed. If the robot is in Programming mode, pressing the enabling device is also necessary to move the robot._ 

###### **_NOTICE_** 

The system monitors the connection of the Franka UI hold-to-run control with a maximum timeout of 1 s. If a connection loss is detected while a hold-to-run control is pressed, the system is stopped. 

###### **Re-packing the Arm** 

###### Precondition 

- The robot needs to be in the transport pose. 

Procedure 

1. Open the box. 

2. Grasp the Arm at the indicated lifting positions in twos and carefully put it inside the bottom protective layer. 



Fig. 10.33: Lifting the arm 

R02210/1.4/EN 

Franka Robotics GmbH © 

88 

###### MOUNTING AND INSTALLATION 

3. Insert the middle protective layer. 



4. Insert the top protective layer. 



5. Close the foil coating. 

6. Close the box by sealing it with adhesive strips 

R02210/1.4/EN 

Franka Robotics GmbH © 

89 

###### OPERATION 

## **11 OPERATION** 

#### **11.1 Switching On** 



###### **DANGER** 

**Short circuit due to developed condensation when the device is transported from colder to warmer and more humid surroundings** 

- Risk of life-threatening injuries due to electrical shock. 

- Leave devices to acclimatize after transport. 

- Do not switch on wet devices. 

###### Precondition 

- Cables need to be plugged in correctly. 

- The external power supply must be connected. 

- Leave the maximum workspace. 

###### Procedure 

1. Switch on Control. 



Fig. 11.1: Switching on Control 

_Control is now switched on._ 

R02210/1.4/EN 

Franka Robotics GmbH © 

90 

###### OPERATION 



Fig. 11.2: Blue status lights on Arm 

You can observe the following sequence: 

- The cooling system will be activated and is visible and audible. 

- Booting up may take approximately 1 minute. 

- The status lights on the Pilot and both sides of the base will start to flash. 

- After boot-up is complete, the status light will be continuously blue, indicating that the robot is in a stopped state in Execution mode. If the status light flashes red, there exists a safety error. Then check whether the emergency stop is enabled or whether the Emergency Stop device has been correctly connected to input X3. 

- The fail-safe locking system is active. The joints are still mechanically locked. For information on unlocking the fail-safe locking system, see section Pre-guiding in Chapter 0 “ 

- 

- Teach a Task 

- ”. 

- In the event of a malfunction, refer to chapters 15.1 “Maintenance", 16 “SERVICE AND SUPPORT" and 13.8 ”Troubleshooting". 

###### **Overview of the status indicators** 

The visual indicators indicate the current state of the robot. The base LEDs are always active, while the LEDs on the Pilot are only active during programming. 

When switching on the robot, always check the functionality of the indicators and their visibility from the operator’s perspective. The following colour schemes represent the following states: 

R02210/1.4/EN 

Franka Robotics GmbH © 

91 

###### OPERATION 

|**Colour**|**Category**|**Explanation**|**Approaching the robot***|
|---|---|---|---|
|White|Not active; ready<br>to start execution|Franka Research 3 is running but not in an active<br>state (either in TEACH or IDLE). It is ready to start<br>execution or interaction.|The robot is inactive and can be<br>approached.|
|White (slow<br>flashing)|Not active; booting<br>or shutting down|Franka Research 3 is booting or shutting down. Do<br>not interrupt the process.||
|White (fast<br>flashing)|Not active;<br>updating|Franka Research 3 is updating. Do not interrupt<br>the process or disconnect Franka Research 3 from<br>its power source.||
|Blue|Brakes engaged|Franka Research 3’s brakes are locked.|The robot is in a stopped state, but the<br>|
|Blue|Ready to execute<br>task|Operator can now start a task in Execution or Test<br>& Jog mode.|safety system allows to start motion at<br>any<br>time.<br>Approach with care.|
|Blue (slow<br>flashing)|Opening brakes|Franka Research 3 is opening its brakes. It might<br>move slowly while doing this.||
|Blue (slow<br>flashing)|Collaborative<br>operation (no task<br>active)|Franka Research 3 is in collaborative mode while<br>no task is active.||
|Green|Automatic<br>execution|Franka Research 3 is currently running an<br>automatic program and is moving independently.|The robot is executing a task. Do not<br>approach.|
|Green (slow<br>flashing)|Collaborative<br>operation (task<br>active)|Franka Research 3 is in collaborative mode while a<br>task is active (e.g., to hand-guide in Assist mode).|The robot is executing a task, but<br>ready for collaboration in Assist mode.<br>Approach with care and in accordance<br>with the application-specific safety<br>measures defined for Assist mode.|
|Green (fast<br>flashing)|Attention:<br>Automatic<br>execution starting|Franka Research 3 will start task execution after<br>“work execution wait time” countdown (if<br>configured) has elapsed.|The robot will soon be executing a<br>task. Do not approach.|
|Yellow|Warning|Franka Research 3 is in a warning state|The system is in a warning state. Do<br>|
|Yellow (slow<br>flashing)|Warning; user<br>interaction needed|Franka Research 3 is in a warning state that needs<br>to be acknowledged by the user.|not approach the robot.|
|Pink (slow<br>flashing)|Conflicting inputs|Franka Research 3 encountered conflicting input<br>signals.|Do not approach the robot.|
|Red|Error|An error has occurred (e.g., Safety Error, System<br>Error, or loss of communication).|Do not approach the robot.|
|Red (slow<br>flashing)|Safety Violation /<br>application error|A safety violation or application error is preventing<br>task execution.|The<br>robot<br>can<br>be<br>approached<br>depending on<br>the violation/error<br>shown in the Franka UI and the steps<br>required for recovering a safety<br>violation.<br>Approach<br>with<br>care<br>depending on the situation and actual<br>violation.|



(*) In general, it depends on the application specific risk & hazard analysis and on the specific configuration of the safety scenarios whether it is safe to approach the robot in a specific situation or state. The visual color indicators can help identify the situation or state the system is in. However, the visual indicators are not a safety function, so the user must always be careful when approaching the robot based on such information. If in doubt, use appropriate safety measures to prevent injuries before approaching the robot (e.g., press Emergency Stop or activate protective stop). 

Generally, slow flashing (0.6 Hz, twice per 3 seconds) signals that the system is in transition between states or is used to attract attention to get support. The fast-flashing scheme (2 Hz, twice per second) warns the user that motion is initiating, the robot is moving very slowly, or the system is updating. 

If a visual indicator or its controlling device detects a loss of communication, this is signaled as an error with a red light. 

The visual indicators will always signal the most important event or state. The color scheme with the higher significance is signaled. Within one significance level, only one color scheme is shown. 

R02210/1.4/EN 

Franka Robotics GmbH © 

92 

OPERATION 

#### **11.2 Safety Relevant Tests of Franka Research 3** 

##### **11.2.1 Self-test of the robotic system** 

The self-tests of Control are executed while the system is running. The Arm is power cycled once to execute the self-tests of the Arm. 



###### **WARNING** 

**Risk of injury due to falling objects** 

During the power cycle of the Arm, the power to the end effector is removed. Objects may fall from the end effector which could lead to injury. 

- Remove all objects from the end effector. 

- Move out of the hazard zone. 

###### **_NOTICE_** 

Every 24 hours, the user must initiate a safety diagnostic to detect potentially dangerous failures during operation. In the sidebar, the system will warn the user 2 hours before the time is exceeded. 

If the time is exceeded, the robot will stop all operations and request the user to initiate the self-test. For this purpose, a message appears from which you can start the self-test. 

You can also start the self-test manually at any time. To do this, proceed according to the following steps 

1. Start Franka UI on your Interface device. 

2. Go to “Settings”. 

3. Change to “Dashbord” 

4. Click on Button “EXECUTE” next to the display of the countdown to the self-test 



###### **WARNING** 

**Falling objects from end effectors due to a power supply cut off when SEEPO configuration is active** 

- Risk of severe injury, such as crushing, tearing of the skin, and puncturing from the Arm and end effectors. 

- Always wear personal protective equipment (e.g., safety shoes). 

- Use the appropriate type of end effector to prevent objects from falling. 

- Consider the shape, texture, and weight of the grasped objects in the risk assessment according to 102182. Using lightweight and/or round objects may reduce risks significantly. 

R02210/1.4/EN 

Franka Robotics GmbH © 

93 

###### OPERATION 

##### **11.2.2 Regular testing of safety functions** 

The function of some safety functions must be tested regularly. This applies to the following safety functions: 

|**Safety function**|**Test**|
|---|---|
|Emergency Stop Device|1. Press the Emergency Stop Device while the robot is not active.<br>2. Check whether the brakes are locked.|
|Guiding Enabling Device|1. Release the Pilot-Grip´s Enabling Button while guiding.<br>_The robot must stop._<br>2. Fully press the Pilot-Grip´s Enabling Button while guiding.<br>_The robot must stop._|
|External Enabling Device|1. Release the enabling button of the External Enabling Device while testing a task.<br>_The robot must stop._<br>2. Fully press the enabling button of the External Enabling Device while testing a task.<br>_The robot must stop._|
|Any switch connected to X3.2 or X3.3|1. Activate switch.<br>2. Check if configured safety function is triggered accordingly.|



###### **_NOTICE_** 

- Activate the emergency stop system during start-up every 12 months. 

- Reconnect the emergency stop system during start-up every 12 months. 

- Check all safety installations, e.g., emergency stop system, for function every 12 months. 

- Check any additional safety measures that have been taken to secure safe operation. 



For more information on the emergency stop system, see chapter 4.7 Installation of Safety Peripherals”. 

##### **11.2.3 Testing the emergency stop** 



###### **WARNING** 

###### **Risk of severe injury due to a non-operating Emergency Stop Device** 

Using a non-operational Emergency Stop Device to stop an operation in case of an emergency may lead to staying trapped which leads to severe injuries, such as crushing, tearing of the skin, and puncturing from the Arm and end effectors. 

- Store the Emergency Stop Device in a safe place. 

###### **_NOTICE_** 

###### **Material damage** 

The end effector, workpieces, or the surroundings can be damaged, when the device is stopped at an unfavorable point in the process. 

- Only use the emergency stop in safety-critical situations. 

R02210/1.4/EN 

Franka Robotics GmbH © 

94 

###### OPERATION 

###### **_NOTICE_** 

Any damage occurring to the Arm when the emergency stop is pressed will not cause harm to persons, as the Arm will safely stop regardless of damage. 

###### **_NOTICE_** 

After an emergency stop, the Arm could have lost calibration or been damaged. If malfunctions are detected at the next start-up, the user will be informed. 

###### **_NOTICE_** 

Take other installed devices apart from Franka Research 3 into account that will be switched off by the emergency stop as well. 

###### **SAFETYINSTRUCTION** 

###### Precondition 

- Franka Research 3 must be at standstill with no task running. 

- The locking bolts of the fail-safe locking system must be open. 

- The Arm may not move. 

- Procedure 

1. Clear the space around the Arm to avoid any damage to grasped objects or surroundings. 2. Use the guiding to bring the Arm into a position that is free from obstacles, e.g., 200 mm above stationary objects. 

3. Activate the emergency stop. The Arm will slightly lower with a clicking noise when falling into the mechanical locking bolts. 

R02210/1.4/EN 

Franka Robotics GmbH © 

95 

###### OPERATION 

#### **11.3 Initial configuration** 

##### **11.3.1 Connecting a User Interface Device** 

An external operating device in the form of a PC, laptop or tablet is required to operate and control the robot. 

Hardware recommendation: 

- Commercially available PC, laptop or tablet 

- Ethernet interface 

- Resolution min. 1280x720px, recommended Full HD (1920x1080 px) 

- Multitouch function, if using a tablet. 

- Recommended browsers: Chrome, Edge, Safari or Firefox 

Procedure: 

1. Connect the interface device to the X5 connector on the Arm base via Ethernet cable to open the initial configuration interface. 

For more information, see chapter 10.6 “Wiring and Electrical Installation”. 

2. To automatically obtain the IP address via DHCP,  make sure that your interface device has activated the DHCP client. 

The IP address will automatically be assigned once Franka Research 3 has been switched on. 

3. Go to your preferred web browser. 

4. Enter the following URL: robot.franka.de 

5. Press Enter. 

_The website showing the Franka UI opens up._ 

##### **11.3.2 Initial Configuration „First Start“** 

After starting the Control for the first time, it is necessary to set basic settings in the system. The initial configuration is displayed in the web browser. This initial configuration is also displayed after resetting the Control to the factory settings. 

To perform the initial configuration, first perform the procedure from Chapter 11.3 “Initial configuration 

Connecting a User Interface Device” and then proceed according to the following steps: 

1. Start Franka Research 3. 

2. Enter the following URL: robot.franka.de 

   - The "First Start" web interface of the Franka UI opens with the language selection of the system interface. 

R02210/1.4/EN 

Franka Robotics GmbH © 

96 

###### OPERATION 



Fig. 11.3: Language Selection Initial Configuration 

3. Click on the area where the IP address of the robot is shown in the menu bar to download the product manual. Be sure to read it carefully. 

4. Select the desired language for the Franka UI interface. Click on „NEXT“ 

   - The page for setting the network connection is opened. 



Fig. 11.4: Network Initial Configuration 

On this page, the network connections of the internal robot network and those of the Internet connection or connection to a company network can be configured. 

The subaddress of the robot network can be adjusted if required. The default setting is 192.168.0.1, the address range can be used from 100-150. 

For access to the company network or the Internet, the use of the DHCP client can be selected or a manual configuration can be performed. 

The current connection status to Franka World is displayed graphically. 

5. Confirm the settings by clicking on „NEXT“ 

   - The web interface for configuring / managing the robot with Franka World opens. 

R02210/1.4/EN 

Franka Robotics GmbH © 

97 

###### OPERATION 



Fig. 11.5: Franka World registration 

This page is used to register the robot in Franka World and to manage updates and Apps. 

When the Control is connected to the Internet, the robot is automatically registered in Franka World and checked for the availability of the latest system updates or application software (Apps). 

The configuration of the robot is done in Franka World. You can open Franka World by clicking on the link. 

A Franka World account is required for installing system updates and Apps (see Chapter 14.2 "Managing apps and features"). 



For more information about Franka World see Chapter 14.1 „Franka World“. 

6. Click on „Download“ to transfer any available changes. 

If an internet connection cannot be established, you can also update the device "offline". For this purpose, read chapter 14.4 „Updates“. 

7. After the data has been transferred, confirmation is required to complete the installation. To do this, click on "Apply". 

A restart will be initiated in case of system-relevant changes. The first-start procedure is then restarted, but your previous settings are stored. In this case, confirm all previous steps with "Next". 

After all available changes have been installed in the Franka World step, you can proceed to the next step by clicking "Next". 



For information about system updates und Apps, see chapter 14.2 “Managing Apps and Updates“. 

- The web interface for creating the administrator is opened. 

R02210/1.4/EN 

Franka Robotics GmbH © 

98 

###### OPERATION 



Fig. 11.6: Creating Administrator 

8. Create an initial user of type “Administrator” 

This user can continue the configuration later and create additional system users. For more information on roles, see the section "Creating an administrator" in Chapter 5 “ROLES AND PERSONNEL ". 

9. Confirm the input by clicking on „Next“. 

   - The web interface for configuring the end effector is opened. 



Fig. 11.7: End effector settings 



###### **WARNING** 

###### **Unexpected motions during guiding due to incorrectly configured end effectors** 

Incorrectly configured end effector mass and inertia may lead to not entirely compensated gravitational forces. The resulting and unexpected behavior of the robot including end effector may lead to injuries such as crushing, tearing of the skin, and puncturing. 

- Always check the configuration of the end effector. 

R02210/1.4/EN 

Franka Robotics GmbH © 

99 

###### OPERATION 

- When copying an already parametrized App or Task to another Franka Research 3 system, ensure that the end effector configuration remains identical to the original one. 



###### **CAUTION** 

###### **Falling objects from end effectors during initial installation** 

Objects falling from the gripper lead to injuries to hands, fingers, feet, and toes. 

   - Always wear personal protective equipment (e.g., safety shoes). 

   - Use the appropriate type of grippers to prevent objects from falling. 

   - Consider the shape, texture, and weight of the grasped objects in the risk assessment according to 10218-2. Using lightweight and/or round objects may reduce risks significantly. 

   - Do not place your hands between grasped and solid objects (e.g., table). 

   - Do not load the end effector before start-up, since depending on the installed end effector, the 'homing' motions may be executed automatically upon restoration of power. 

10. Configure which end effector is used on the robot. 

If you do not have an end effector mounted, select “None“ from the drop-down menu. . 

If you have mounted Franka Hand as an end effector, select “Hand“ from the drop-down menu. 

###### **_NOTICE_** 

Franka Hand is not part of the certified robot. 

If you want to use another end effector or adjust the configuration of the Hand, select “User Defined” from the dropdown and enter the corresponding values into the text fields. The appropriate values are usually found in the end effector’s manual. 

**_NOTICE_** 

You will be able to reedit the end effector settings later on. 

11. Confirm the entries by clicking on "Confirm". The initial configuration is thus completed and confirmed, and a final preparation step is performed. 

   - The programming interface DESK is displayed in the web browser and the status display on the arm lights up permanently in blue. 

R02210/1.4/EN 

Franka Robotics GmbH © 

100 

###### OPERATION 

#### **11.4 Setup of Franka Control Interface (FCI)** 

To operate the robot via the Franka Control Interface (FCI), the FCI-Feature must be installed on your device. If it is already installed on the controller, it will be listed under Franka UI -> Settings -> System -> Installed Features. By default, the FCI feature is automatically installed during initial configuration. If FCI is not already installed, you can install it on Control with your Franka World account. 

To control the robot via the Franka Control Interface (FCI), the operating device must be connected to the C2 – Shop floor network port on controller via an Ethernet cable. 

###### **_NOTICE_** 

Control via FCI is only possible via the C2 – Shop floor network port. The use of the X5 - Robot network port on the robot foot is not suitable for the use of the FCI function. 



Fig. 11.8 Network connection for FCI Usage 

##### **11.4.1 Configuration of the network for control via FCI** 

Good network performance is critical for controlling the robot via the FCI interface. It is therefore strongly recommended to use a direct connection between the workstation PC and Control. This section describes how to configure your network for this use case. 

To operate and control the robot via the FCI interface, an external operating device in the form of a PC or laptop with a Linux operating system (e.g. Ubuntu) is recommended. 

Hardware recommendation: 

- Commercially available PC, laptop with Linux 

- Ethernet interface 

- Resolution min. 1280x720px, recommended Full HD (1920x1080 px) 

- Recommended browsers: Chrome or Firefox 

<mark>Control and your workstation must be configured to appear on the same network. The simplest way to achieve that is to use static IP addresses. Any two addresses on the same network would work, but the following values will be used for the purpose of this example</mark> : 

||**Workstation PC**|**Control**|
|---|---|---|
|Address|172.16.0.1|172.16.0.2|
|Netmask|24|24|



<mark>The Control’s address (172.16.0.2) is called <fci-ip> in the following chapters.</mark> 

R02210/1.4/EN 

Franka Robotics GmbH © 

101 

###### OPERATION 

**_NOTICE_** 

With this network configuration, Franka UI can be accessed via https://<fci-ip>, although you will see a certificate warning in your browser. 

<mark>The Control’s network can be configured in the administrator’s settings. For the duration of this step, you can connect to the X5 – Robot network port in the robot’s base.</mark> 

Further information can be found in the chapter 11.3.1 “Connecting a User Interface Device“. 

To set up a static address, deactivate DHCP-Client in “C2-Shop Floor network” settings. 



Fig. 11.9 <mark>Network settings</mark> 

Now, you can enter the settings of the static IP for the LAN connection of the controller for the Shop floor-/ company- network. 

To confirm the settings, press "Apply". 

After the settings have been successfully applied, the settings of the network interface of the operating device in Linux still have to be adjusted. 

###### **Configuration of operating device** 

<mark>This section describes how to set up a static IP address on Ubuntu 20.04 using the GUI. Follow the official Ubuntu guide if you prefer to use the command line.</mark> 

**_NOTICE_** 

The following steps will modify your network settings. If in doubt, contact your network’s administrator. 

<mark>First, go to Network Connection widget. Select the wired connection you will be using and click edit.</mark> 

R02210/1.4/EN 

Franka Robotics GmbH © 

102 

###### OPERATION 



Fig. 11.10 <mark>Ubuntu – Ethernet configuration</mark> 

<mark>Next, click on the IPv4 settings tab, set the method to Manual, and enter the following values</mark> . 



Fig. 11.11 Ubuntu – <mark>setting a static IP</mark> 

###### **_NOTICE_** 

This step will disable DHCP, which means you will no longer obtain an address when connecting to a DHCP server, like the one in Arm’s base (X5 – Robot network). When you no longer use FCI, you can change the method back to _Automatic (DHCP)_ . 

<mark>Save the changes and close the Network Connection window. Click on the connection name from the drop-down menu. It should now be possible to connect to the robot from your workstation.</mark> 

To verify network quality, perform a communication test of network bandwidth, delay, and jitter after completing the FCI configuration of the system. 

<mark>From now on, you can also access Franka UI through this address <fci-ip> in your browser.</mark> 

##### **11.4.2 Setup of libfranka on a Linux workstation** 

Recommended for the setup is an Ubuntu 22.04 Pro version or newer. In this version, Ubuntu already provides the required RT kernel, but it may be chargeable depending on the usage. 

If you are using an Ubuntu version without a provided RT kernel, it must be installed before libfranka is patched. The real-time kernel is used to realize the real-time transmission with 1 kHz of the signals between Control and the operating device. 

R02210/1.4/EN 

Franka Robotics GmbH © 

103 

###### OPERATION 

The setup of libfranka then requires two steps, which must be performed one after the other. For the execution you need full "admin" rights on your Linux PC. 

Further information can also be found in <u>FCI-Documentation</u> via <u>Franka World.</u> 

###### **Installation PREEMPT_RT Kernel** 

In the first step, if an RT kernel has not yet been installed with the Ubuntu version, a PREEMPT Real-Time kernel must be installed. To do this, create a new folder in your Linux PC's drive and start the terminal from it. 

**_NOTICE_** 

NVIDIA binary drivers are not supported on PREEMPT_RT-kernels. 

To install, proceed now according to the following steps: 

**_NOTICE_** 

To avoid typing errors when entering commands, open the online FCI documentation and copy the command lines there, which you can then paste and execute in the terminal. 

###### • **Download** 

To install the dependencies, enter the following command in the Terminal: 

```
sudo apt-get install build-essential bc curl ca-certificates gnupg2 libssl-dev lsb-release libelf-dev bison flex
dwarves zstd libncurses-dev
```

Then you need to decide which kernel version you want to use. Use the following command to find out which version you are currently using. 

```
uname -r
```

<mark>Real-time patches are only available for select kernel versions, see https://www.kernel.org/pub/linux/kernel/projects/rt/. We recommend choosing the version closest to the one you currently use.</mark> 

The version tested by Franka Robotics is the 5.9.1 for Ubuntu 20.04, on which the following installation steps are based. 

Use the command lines below to download the source files. 

If you have chosen a different version, change the version number (5.9.1) in the command lines to match the version you have chosen. 

```
curl -SLO https://www.kernel.org/pub/linux/kernel/v5.x/linux-5.9.1.tar.xz
curl -SLO https://www.kernel.org/pub/linux/kernel/v5.x/linux-5.9.1.tar.sign
curl -SLO https://www.kernel.org/pub/linux/kernel/projects/rt/5.9/patch-5.9.1-rt20.patch.xz
curl -SLO https://www.kernel.org/pub/linux/kernel/projects/rt/5.9/patch-5.9.1-rt20.patch.sign
```

Then decompress the downloaded data with the command: 

```
xz -d *.xz
```

###### • **Verification** 

After downloading the dependencies, it is recommended that you check them to see if they have been corrupted or tampered with. The steps recommended for this are taken from the Linux Kernel Archive. 

Use the following commands to check: 

```
gpg2 --verify linux-*.tar.sign
gpg2 --verify patch-*.patch.sign
```

If all loaded packages are correct, you will receive a message corresponding to the following example for each command. 

R02210/1.4/EN 

Franka Robotics GmbH © 

104 

###### OPERATION 

```
$ gpg2 --verify linux-*.tar.sign
gpg: assuming signed data in 'linux-4.14.12.tar'
gpg: Signature made Fr 05 Jan 2018 06:49:11 PST using RSA key ID 6092693E
gpg: Good signature from "Greg Kroah-Hartman <gregkh@linuxfoundation.org>" [unknown]
gpg:                 aka "Greg Kroah-Hartman <gregkh@kernel.org>" [unknown]
gpg:                 aka "Greg Kroah-Hartman (Linux kernel stable release signing key)
<greg@kroah.com>" [unknown]
gpg: WARNING: This key is not certified with a trusted signature!
gpg:          There is no indication that the signature belongs to the owner.
Primary key fingerprint: 647F 2865 4894 E3BD 4571  99BE 38DB BDC8 6092 693E
```

<mark>See</mark> <u><mark>Linux Kernel Archive for more information about the warning.</mark></u> 

If the check returns an error, then you will receive a message corresponding to the example below. 

```
$ gpg2 --verify linux-*.tar.sign
gpg: assuming signed data in 'linux-4.14.12.tar'
gpg: Signature made Fr 05 Jan 2018 06:49:11 PST using RSA key ID 6092693E
gpg: Can't check signature: No public key
```

In this case, you must download the key from the key server. 

To do this, use the following command for both "*.tar" and "*.patch" and enter the ID specified in the respective error message in the command line. 

```
gpg2  --keyserver hkp://keyserver.ubuntu.com:80--recv-keys 6092693E
```

###### • **Compiling the kernel** 

<mark>Once you are sure the files were downloaded properly, you can extract the source code and apply the patch.</mark> 

To do this, enter the following commands one after the other: 

```
tar xf linux-*.tar
cd linux-*/
patch -p1 <../patch-*.patch
```

Get the current name of the patch with the command: 

```
uname -r
```

Als nächstes kopieren Sie mit der nachfolgenden Befehlszeile Ihre aktuell gebootete Kernelkonfiguration als Standardkonfiguration für den neuen Real-Time-Kernel. Über „uname -r“ wird automatisch der aktuelle Kernel ausgewählt. 

```
cp -v /boot/config-$(uname -r) .config
```

Now you can use this configuration as the default for configuring the build. To do this, eonter the following cmmands: 

```
make olddefconfig
make menuconfig
```

The second command opens a terminal interface (TUI) where you can configure the preemption model. 

R02210/1.4/EN 

Franka Robotics GmbH © 

105 

###### OPERATION 



Fig. 11.12 TUI-Interface 

- Navigate with the up/down keys to "General Setup" > **"Preemption Model"** and mark there > **"Fully Preemptible Kernel (Real-Time)"** By using the side arrow keys you can move the cursor to Select in the command line at the bottom of the screen. Now press <Enter> and the selection is chosen _._ 

- Set the cursor in the command line to <EXIT> and press <Enter> repeatedly until you return to the main menu. 

- Now navigate to **"Cryptographic API"** > **"Certificates for signature checking"** (at the very bottom of the list) > **"Provide system-wide ring of trusted keys"** . 

- There, select **"Additional X.509 keys for default system keyring"** and press Enter. An input window opens. Remove the entry **"debian/canonical-certs.pem"** from the prompt and press Ok. 

- Now navigate to " **Cryptographic API"** > **"Certificates for signature checking"** (at the very bottom of the list) > **"Provide system-wide ring of revocation certificates"** . 

- There select **"X.509 Certfifcates tob e preloaded into the system blacklist keyring"** and press Enter. An input window opens. There remove the entry **"debian/canonical-revoked-certs.pem"** from the prompt and press Ok. 

- Save this now the configuration in .config and exit the terminal interface (TUI). 

Now the installation is ready for the kernel to be compiled. Since this is a lengthy process, the "nproc" command automatically uses the multithreading option "-j" on the command line to use the maximum number of cores on your CPU. Nevertheless, this step takes longer time. 

```
make -j$(nproc) deb-pkg
```

Now you can install the newly created package with the following command. The exact names depend on your environment. The command searches for the header and images packages. 

```
sudo dpkg -i ../linux-headers-*.deb ../linux-image-*.deb
```

- **Verifing the new kernel** 

Restart your system. The grub boot menu should now allow you to choose your newly installed kernel. To see which kernel will be used after the boot, look at the output of the following command: 

```
uname -a
```

It should contain the string PREEMPT_RT and the version number you chose. Additionally, /sys/kernel/realtime should exist and contain the the number „1“. 

R02210/1.4/EN 

Franka Robotics GmbH © 

106 

###### OPERATION 

**_NOTICE_** 

   - If you encounter errors that you fail to boot the new kernel see „Cannot boot realtime kernel <u>because of Invalid Signature".</u> 

   - If you want to re-do the build, then delete all the unzipped data from your installation folder beforehand. 

- **Allow a user to set real-time permissions for this process** 

<mark>After the P</mark> REEMPT_RT-Kernel <mark>is installed and running, add a group named</mark> _<mark>realtime</mark>_ <mark>and add the user controlling your robot to this group.</mark> 

You can get your user name from the command line: 

```
whoami
```

```
sudo addgroup realtime
sudo usermod -a -G realtime $(whoami)
```

Then open the "limits.conf" file with the following command: 

```
sudo gedit /etc/security/limits.conf
```

Then add the following real-time group limits to the file and save them. 

```
@realtime soft rtprio 99
@realtime soft priority 99
@realtime soft memlock 102400
@realtime hard rtprio 99
@realtime hard priority 99
@realtime hard memlock 102400
```

<mark>The limits will be applied after you log out and in again.</mark> 

###### **Installation Libfranka** 

The next step describes how to install libfranka from source files. Alternatively, libfranka can be installed by ROSrepos (<Ubuntu 22.04) or ROS2-repos (Ubuntu 22.04 and later). 

You can also find further assistance in the FCI-Dokumentation on <u>Franka World.</u> 

###### **_NOTICE_** 

To avoid typing errors when entering commands, open the online FCI documentation and copy the command lines there, which you can then paste and execute in the terminal. 

<mark>Before building the new libfranka from source, please uninstall existing installations of</mark> libfranka <mark>and f</mark> ranka_ros <mark>to avoid conflicts.</mark> 

To do this, run the following command in the terminal: 

```
sudo apt remove "*libfranka*"
```

R02210/1.4/EN 

Franka Robotics GmbH © 

107 

###### OPERATION 

- **Download** 

To install libfranka, the dependencies must be downloaded. To do this, enter the following command line: 

```
sudo apt install build-essential cmake git libpoco-dev libeigen3-dev
```

Then download the source code by cloning libfranka from GitHub and then change to the directory. To do this, use the following commands: 

```
git clone --recursive https://github.com/frankaemika/libfranka --branch 0.10.0
cd libfranka
```

- **Install** 

Then, the following commands create a build folder in the current directory and run the "CMake" command to create the build / project files. 

```
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTS=OFF ..
cmake –-build .
```

It is recommended to install the optional libfranka Debian package. To do this, enter the following command in the same directory that creates the "libfranka-<version>-<architecture>.deb" package. 

```
cpack -G DEB
```

This is then installed by the following command. 

```
sudo dpkg -i libfranka*.deb
```

The libfranka is now installed on your PC and can be used to control the robot via FCI. 

##### **11.4.3 Verification of communication** 

After the successful compilation / installation of libfranka, a test of the communication of the interface is recommended. To do this, make sure that the robot is prepared for FCI use in Desk and run the example "echo_robot_state" from libfranka. 

Change to the build directory of libfranka and execute the following on Linux: 

```
./examples/echo_robot_state <fci-ip>
```

The program will display the current state of the robot on the console and will exit automatically after a few iterations. 

```
{
"O_T_EE":[0.998578,0.0328747,-0.0417381,0,0.0335224,-0.999317,0.0149157,0,-0.04122,
-0.016294,-0.999017,0,0.305468,-0.00814133,0.483198,1],
"O_T_EE_d": [0.998582,0.0329548,-0.041575,0,0.0336027,-0.999313,0.0149824,0,-0.0410535,
-0.0163585,-0.999023,0,0.305444,-0.00810967,0.483251,1],
"F_T_EE":[0.7071,-0.7071,0,0,0.7071,0.7071,0,0,0,0,1,0,0,0,0.1034,1],
"EE_T_K":[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],
"m_ee":0.73,"F_x_Cee":[-0.01,0,0.03],"I_ee":[0.001,0,0,0,0.0025,0,0,0,0.0017],
"m_load":0,"F_x_Cload":[0,0,0],"I_load":[0,0,0,0,0,0,0,0,0],
"m_total":0.73,"F_x_Ctotal":[-0.01,0,0.03],"I_total":[0.001,0,0,0,0.0025,0,0,0,0.0017],
"elbow":[-0.0207622,-1],"elbow_d":[-0.0206678,-1],
"tau_J":[-0.00359774,-5.08582,0.105732,21.8135,0.63253,2.18121,-0.0481953],
"tau_J_d":[0,0,0,0,0,0,0],
```

R02210/1.4/EN 

Franka Robotics GmbH © 

108 

OPERATION 

```
"dtau_J":[-54.0161,-18.9808,-64.6899,-64.2609,14.1561,28.5654,-11.1858],
"q":[0.0167305,-0.762614,-0.0207622,-2.34352,-0.0305686,1.53975,0.753872],
"dq":[0.00785939,0.00189343,0.00932415,0.0135431,-0.00220327,-0.00492024,0.00213604],
"q_d":[0.0167347,-0.762775,-0.0206678,-2.34352,-0.0305677,1.53975,0.753862],
"dq_d":[0,0,0,0,0,0,0],
"joint_contact":[0,0,0,0,0,0,0],"cartesian_contact":[0,0,0,0,0,0],
"joint_collision":[0,0,0,0,0,0,0],"cartesian_collision":[0,0,0,0,0,0],
"tau_ext_hat_filtered":[0.00187271,-0.700316,0.386035,0.0914781,-0.117258,-0.00667777,
-0.0252562],
"O_F_ext_hat_K":[-2.06065,0.45889,-0.150951,-0.482791,-1.39347,0.109695],
"K_F_ext_hat_K":[-2.03638,-0.529916,0.228266,-0.275938,0.434583,0.0317351],
"theta":[0.01673,-0.763341,-0.0207471,-2.34041,-0.0304783,1.54006,0.753865],
"dtheta":[0,0,0,0,0,0,0],
"current_errors":[],"last_motion_errors":[],
"control_command_success_rate":0,"robot_mode":"Idle","time":3781435
}
```

Abb.11.1 Example output of „echo robot state“ 

The respective fields are explained in the libfranka API documentation <u><mark>(https://frankaemika.github.io/libfranka.)</mark></u> 

**_NOTICE_** 

If an error occurs at this point, perform the ping test and verify that FCI is enabled and the robot's brakes are open. 

To perform the ping test, enter the following command line: 

```
ping <fci-ip>
```

If this command fails, the robot is not properly connected to the network or the IP address was not assigned correctly during the setup phase. Please set up the network again according to the steps described in section 11.4.211.4.1 “Configuration of the network for control via FCI”. 

R02210/1.4/EN 

Franka Robotics GmbH © 

109 

###### OPERATION 

#### **11.5 Typical Usage** 

After switching on the robot, Franka UI must be called up via the previously assigned IP address or, if the operating device is connected to the X5 – Robot network on the robot base, via <u>robot.franka.de. The Franka</u> Research 3 can now be controlled in two different ways. 

1. If you want to control and program the robot by using Apps, you can now do this in the open **_Franka UI_** . 

Further explanations and operating instructions can be found in Chapter 0 "Franka UI". 

2. If you want to control the robot via the **Franka Control Interface (FCI)** , you must activate the FCI mode in Control. 

To do this, open Desk in the Franka UI and expand the System menu in the header. Change the operation mode to “Execution” and activate the FCI interface here by pressing the "Activate FCI" button. 

From now on, you can control the robot by Linux-terminal with FCI commands via libfranka or by using ROS-, ROS 2- or Matlab-Interface. 

Further explanations and operating instructions can be found in Chapter 13.7 “Franka Control Interface (FCI)". 

**_NOTICE_** 

The robot must be connected to the operating device via the C2 – Shop Floor network on the front of Control using a stable and fast network connection in order to use FCI mode. Controlling the robot via the X5 – Robot network on the robot foot is not possible when using FCI. 

#### **11.6 Switching Off and Restarting** 



###### **WARNING** 

**Falling objects from end effectors due to a power supply cut off** 

- Objects falling from the gripper lead to injuries to hands, fingers, feet, and toes. 

- Always wear personal protective equipment (e.g., safety shoes). 

- Use the appropriate type of grippers to prevent objects from falling. 

- Consider the shape, texture, and weight of the grasped objects in the risk assessment according to 102182. Using lightweight and/or round objects may reduce risks significantly. 

###### **Shutting down** 

**_NOTICE_** 

The system is only completely shut down when the fans stopped running. Still running fans indicate that Franka Research 3 has not been completely shut down yet. Repeat the Safety Instructions of Shutting down Franka Research 3. 

R02210/1.4/EN 

Franka Robotics GmbH © 

110 

###### OPERATION 

**SAFETYINSTRUCTION** 

Procedure 

1. Move out of the hazard zone. 

2. In Franka UI, navigate in user menu to “Shut-down” and click on it. 

_The fail-safe locking system is activated. Franka Research 3 will shut down._ 

###### **Restarting** 

Turn off the system in Desk and wait for the fans to power down. Switch off the power switch on the Control. Wait one minute before restarting Franka Research 3 again. To restart Franka Research 3, switch on the power switch on the back of the Control. Franka Research 3 will start to reboot again. 

**_NOTICE_** 

To avoid unintentional repowering of the system, secure the connecting cable in a safe place. 

###### **Disconnecting Franka Research 3 from the power supply** 

###### Procedure 

1. Move out of the maximum workspace. 

2. Go to Franka UI. 

3. Select in User-Menu “Shut-down.” 

_The system shuts down._ 

4. Switch off the power switch on the backside of the Control. 

5. Pull the cable from the backside of the Control. 

**_NOTICE_** 

To avoid unintentional restarting of the system, stow the power cord in a safe place. 

_Franka Research 3 is disconnected from the power supply._ 

R02210/1.4/EN 

Franka Robotics GmbH © 

111 

SAFETY CONFIGURATION/WATCHMAN 

## **12 SAFETY CONFIGURATION/WATCHMAN** 

As already described in chapter 4.12 “Additional information for planning and initial installation of a robot system“, robots must always be surrounded by protective devices that prevent people from entering the hazardous area or, in the case of collaborative robots there are safe-zones that must be initiated and monitored when people are present in the hazardous area. 

After the risk assessment has been carried out, the safety scenarios of the robot must be adapted to the determined necessary safety functions of the worksite in which the robot system is installed. 

The Franka Research 3 is delivered with a predefined and pre-validated set of safety scenarios according to the requirements from the ISO 10218-1 standard. 

If the risk analysis shows that these are sufficient, the Franka Research 3 can be integrated and used in the planned working environment of the robot without further changes to the safety configuration after appropriate electrical integration. However, if the risk analysis shows that additional safety functions are required, these must be implemented in Watchman by means of rules that apply in specific robot states or scenarios. 

#### **12.1 Watchman** 

Watchman is a tool in the Franka Web User Interface (Franka WebUI) for displaying, creating and editing safety functions also on the Franka Research 3. Safety functions can be defined via rules. These rules can in turn adapt the behavior of the respective scenarios, such as "Teach" and "Work", to the required protective measures from the risk assessment for the two operating states of the robot ("Programming" and "Execution"). 

The safety configuration can only be done by a Safety Operator. The Safety Operator is one of three user roles available on the FRANKA RESEARCH 3. The other roles available are Administrator and Operator. See the chapter 5 “ROLES AND PERSONNEL ” for more information. A user in the Administrator role can create a Safety Operator role but cannot edit any safety functions himself. Only in the user role Safety Operator can modify settings in Watchman. The Safety Operator is responsible for the correct safety configuration and documentation of the safety functions and should only be performed by qualified personnel. 

#### **12.2 Overview** 

In Watchman, the security scenarios are displayed via an intuitive graphical interface. 

The structure of the interface is illustrated and described below. 



R02210/1.4/EN 

Franka Robotics GmbH © 

112 

Fig. 12.1: Watchman 

###### SAFETY CONFIGURATION/WATCHMAN 

In the header of the Watchman view, you can find the currently valid security configuration report on the right. The button with the three dots on the right allows you to reset the security configuration to factory settings. 

The current validation status of the safety configuration is displayed. Green means validated; orange indicates the need for validations 

Clicking the validation symbol next to the Draft tab displays the checksum of the currently validated safety configuration. 

In the left part of the view, a structural overview is visible, which displays the validation states of the basic safety settings as well as those of the different safety scenarios. 

In the editing area, the basic settings or the rules of the safety scenarios are displayed. 

The security scenarios are divided into editable and non-editable security scenarios. 

The detailed descriptions of the security scenarios can be found in the chapter 4.10 “Safety Concept” of the product manual. 

The editable scenarios are used for the possibility to adapt the robot control to the determined safety measures from the previous risk analysis. The following scenarios are available: 

- Work 

- Assist 

- Test & Jog 

- Teach 

For the "Work" and "Assist" scenarios, up to 16 user made safety rules can be created and configured. In the "Test & Jog" and "Teach" scenarios, only adjustments to the existing rules can be made. 

The factory settings of the Franka Research 3 have a predefined and prepared set of scenarios. If these are suitable for the requirements identified in doing the risk analysis, they can be used immediately. 

**_NOTICE_** 

By default, the “Work” scenario in Watchman does not contain any rules. To ensure a safe operation also considering the application-specific risk & hazard analysis the empty “Work” scenario is not pre-validated. A safety operator has to setup the system correctly and validate the safety settings. 

Non-editable safety scenarios (Read Only Scenarios) are safety functions permanently integrated in the robot Control that ensure safe and standard-compliant operation of the robot and cannot be changed. These are: 

- Idle 

- Opening/Closing Brakes 

- Position Error Recovery 

- Position Function Recovery IDLE 

- Position Function Recovery 

- Joint Limit Recovery 

- Work Invalid 

All recovery scenarios as well as the scenario "Work Invalid" are scenarios that are only activated in the robot state "error/violation". The robot state "error/violation" is caused by violations of the safety scenarios from the robot states "execution" and "programming" or in the presence of a fundamental safety-relevant error. 

The robot state "execution" includes the scenarios "Work", "Assist" and "Opening/Closing brakes". The robot state "programming" includes the scenarios "Idle", "Teach" and "Test&Jog". 

R02210/1.4/EN 

Franka Robotics GmbH © 

113 

SAFETY CONFIGURATION/WATCHMAN 

#### **12.3 Editing of the Safety Configuration** 

In order to complete the following steps, a "Safety Operator” user must be logged in. 

Open the Watchman interface via the menu on the sidebar in Franka UI. The active and confirmed rules as well as the validation states of the scenarios are now displayed on the Watchman interface. 



Fig. 12.2: Validated rules 

Switch to "Draft" mode and start editing. 



Fig. 12.3: Switch to “Draft” mode 

After opening a validated safety concept in "Draft" mode, all validation markers are shown in green. 

R02210/1.4/EN 

Franka Robotics GmbH © 

114 

SAFETY CONFIGURATION/WATCHMAN 



Fig. 12.4: Draft Mode 

If changes are now made, the validation markers of the changed safety function and all parameters, rules and scenarios dependent on the change, as well as the overall safety, are shown in orange. Parameters, rules and scenarios that are not affected remain validated and thus green. 



Fig. 12.5: Validation markers 

After completing the safety configuration, the overall concept must be validated. The procedure is described in the chapter 12.7 “Validate”. 

R02210/1.4/EN 

Franka Robotics GmbH © 

115 

SAFETY CONFIGURATION/WATCHMAN 

#### **12.4 Import/Export of Safety Settings** 

The import/export feature allows safety operators to transfer safety settings between systems or create backups.  It will allow user to avoids the need to configure settings from scratch, ensures uniform safety settings across multiple systems and provides a way to back up current safety settings for recovery purposes. 



Fig. 12.6: Import/Export settings 

###### **Scenarios for Using This Feature** 

**System Migration** : 

- When moving safety settings to a new system. 

**Backup and Recovery** : 

- For safeguarding settings against data loss. 

**Multiple Systems** : 

- Applying the same settings across different systems to maintain consistency. 

###### **Post-Import Actions** 

Safety operators can export the currently committed safety settings into a file that they can download onto their own device. Subsequently, this file can be imported on the same system or on a different system. In both cases, the currently existing drafts are overwritten with the contents of the imported file. 

After importing settings, safety operator should: 

- Check the new settings to ensure they are correct. 

- The safety operator still needs to commit these drafts before the imported safety settings become active. 

- In case the import was performed on a different system, additionally they also need to be validated before they can be committed. 

R02210/1.4/EN 

Franka Robotics GmbH © 

116 

SAFETY CONFIGURATION/WATCHMAN 

###### **_NOTICE_** 

It is crucial to ensure that any important drafts are committed or backed up before proceeding with the import. 

##### **12.4.1 Import Procedure** 

**1. Open Standard UI:** 

Start by opening the Standard UI Watchman. 



Fig. 12.7: Standard UI Watchman 

**2. Access Top Right Menu:** 

Click on the menu located at the top right corner of the interface. 

R02210/1.4/EN 

Franka Robotics GmbH © 

117 

SAFETY CONFIGURATION/WATCHMAN 



Fig. 12.8: Import settings as drafts 

**3. Select "Import Settings as Drafts":** 

In the top right menu, find and click on the "Import Settings as Drafts" tab. 

###### **4. File Selection for Import:** 

A prompt will appear asking you to select a file for import. Choose the appropriate file from your system. 



Fig. 12.9: File selection 

###### **5. Warning Dialog:** 

After selecting the file, a warning dialog will appear. It will inform you that your current drafts will be replaced with the safety settings from the import file. 

R02210/1.4/EN 

Franka Robotics GmbH © 

118 

SAFETY CONFIGURATION/WATCHMAN 



Fig. 12.10: Warning dialog 

**6. Confirm Import:** 

If you confirm the action, the safety settings will be successfully imported. 

##### **12.4.2 Export Procedure** 

To export current committed settings: 

**Steps** : 

1. Navigate to the ‘’Export committed settings’’ section in the Watchman UI. 

2. Select the settings to export. 

3. Download the file. 

**File Format** 



The only permitted file extension is .fesafety. Manual modification of these files is not allowed. 

R02210/1.4/EN 

Franka Robotics GmbH © 

119 

SAFETY CONFIGURATION/WATCHMAN 



Fig. 12.11: Safety settings imported 

###### **7. Error Handling:** 

If there is an error during the import, an error message will appear stating "Safety settings could not be imported." This error typically occurs if the safety rules file has been manipulated. 



Fig. 12.12: Error Message 

R02210/1.4/EN 

Franka Robotics GmbH © 

120 

SAFETY CONFIGURATION/WATCHMAN 

#### **12.5 Safety Setup** 

In the Safety Setup, the higher-level configurable basic settings of the robot are mapped. These include the areas "General Safety Settings", "Safe Input Configuration" and "End Effector Configuration". 



Fig. 12.7: Safety Setup 

##### **12.5.1 General Safety Settings** 

To be able to operate the robot in Assist Mode, the "Enable Assist Mode" checkbox must be set. The description of the Assist Mode can be found in the chapter 13.5 “Assist”. If this function is deactivated, the Assist function is not available in any other submenus of the robot Control. These function menus are then greyed out. 

This function is activated in the default settings of the robot. 

##### **12.5.2 Safe Input Configuration** 

The processing of the safety inputs X3.2 and X3.3 can be configured via the Safe Input Configuration. 

The assignment of inputs X3.2 and X3.3 can be found in the chapter 10.6 “Wiring and Electrical Installation”. 

With the setting "No confirmation required", the signal is processed directly. The control reacts immediately to the input. 

With the setting "Confirmation required", the signal is processed directly when the contact is opened, but a query message appears on DESK when the input is closed. This message must be confirmed in order to process the input signal internally. 

In the default settings of the robot, the setting "No confirmation required" is preselected. 

R02210/1.4/EN 

Franka Robotics GmbH © 

121 

SAFETY CONFIGURATION/WATCHMAN 

##### **12.5.3 End Effector Configuration** 

The safety behavior of the connected end effector is defined via the "End Effector Configuration". The following fields can be set: 

- **<u>Description:</u>** Free editable description of the end effector 

- **<u>SEEPO Behavior:</u>** Determination of when and for which safety shutdowns the end effector is to be switched off. 



Fig. 12.6: End Effector Configuration 

- Safety Error:  => Robot safety fault Safety Error /EM-Stop:=> Robot safety fault or Emergency Stop Safety Error/EM-Stop/Cat. 1 stop: Robot safety fault or Emergency Stop or Category 1 Stop 

- Safety Error/EM-Stop/Cat. 1&2 stop: Robot safety fault or Emergency Stop or Category 1 or 2 Stop 

In the default settings of the Robot is set “Safety Error/EM-Stop/Cat. 1 stop". 

**<u>Power ON Behavior:</u>** Setting when the end effector is to be switched on. 

- **Manual** =>with each switching on, the end effector must be activated manually in DESK. 

- **Automatic** => the end effector will be automatically activated when the joints are unlocking. 

In the default settings of the Robot „Automatic“is preselected. 

R02210/1.4/EN 

Franka Robotics GmbH © 

122 

SAFETY CONFIGURATION/WATCHMAN 

##### **12.5.4 Creation of spheres for modelling an End Effector envelope** 

When an end effector is mounted, the control system needs information on its dimensions in order to be able to monitor the end effector spatially and kinetically. For this purpose, up to five spheres can be created and placed in their size and position so that the totality of the spheres resembles the contour of the end effector. 

For spatial monitoring, the outer shells of the spheres are considered and for velocity monitoring, the centers of the spheres are considered. It should be noticed that spheres placed far from the end effector flange can be very sensitive to velocity monitoring due to the lever consideration. 

When positioning the spheres, ensure that the Franka hand is mounted at a 45° angle to the flange coordinate system. 



Fig. 12.7: Configuration of spheres 

R02210/1.4/EN 

Franka Robotics GmbH © 

123 

###### SAFETY CONFIGURATION/WATCHMAN 

Below, an example of the sphere configuration of the Franka Hand is shown. 



Fig. 12.8: Example of spheres for Franka Hand 

If your gripping situation is not covered by the spherical model shown above, it must be adapted. Make sure that contours that could lead to collisions are covered by the sphere model. If you are handling longer objects, the maximum speed of cantilevered objects must also be monitored. To do this, you can place the centers of the spheres at the ends of the object. The maximum speed is monitored in the centers. 



R02210/1.4/EN 

Franka Robotics GmbH © 

124 

SAFETY CONFIGURATION/WATCHMAN 

Fig. 12.9 Example of sphere configuration Franka hand with staff 

#### **12.6 Creating and editing rules** 

Up to 16 rules can be created in each of the "Work" and "Assist" scenarios. By clicking on "Create Rule" below the last rule displayed, a new rule is inserted. By clicking on the "Delete" symbol within a rule, it can be deleted. 



Fig. 12.10: Editing rules 

##### **12.6.1 Structure of a rule** 

A rule consists of the following components: 



Fig. 12.11: structur of a rule 

- **Name:** Freely editable name of the rule 

- **Activation Condition:** Condition for which the rule is activated. The following selection is possible: 

   - <u>Always</u> the rule is always active 

   - `o` <u>X3.2</u> the rule becomes active, when the two-channel X3.2-Input is opened. 

   - `o` <u>X3.3</u> the rule becomes active, when the two-channel X3.3-Input is opened. 

- **Activation Space:** Spatial area in or outside of which the rule gets active. The following selection is possible: 

   - <u>Everywhere</u> the rule is active in the whole working area of the robot. 

   - <u>Inside / Outside Area</u> the rule becomes active inside or outside a free definable cuboid space. When defining the space, it is determined whether the rule becomes active inside or outside the space. 

R02210/1.4/EN 

Franka Robotics GmbH © 

125 

SAFETY CONFIGURATION/WATCHMAN 

- **Safety Function:** Safety function to be executed when the rule is violated. The following selection is possible: 

- `o` <u>Always violated</u> no safety function is executed. If "Always violated" is selected, the rule is permanently violated if the rule becomes active. 

- `o` <u>Inside/Outside Area</u> a violation is triggered if the robot is inside or outside a defined space. When defining the space, it is determined whether the violation should take place inside or outside the space. 

- `o` <u>Maximum Speed</u> Within the applicable spatial area of the rule, the maximum speed is monitored. If the speed of the robot exceeds the permitted maximum speed, a monitored reduction to the permitted speed takes place. If the reduction of the speed does not occur as expected, the preselected reaction is executed (Cat. 1 Stop / Cat. 2 Stop). 

- `o` <u>Safe Monitored Stand Still In the applicable spatial area of the rule, the robot is</u> safely monitored for standstill. Any movement leads to violation of the rule. 

- **WARNING** 

NOTICE that control of the robot via FCI is not possible when the SLP-C, SLS-C or SLP-J functions are active. This affects the safety functions that include spatial position monitoring (Inside/Outside Area) and Cartesian speed monitoring (maximum speed). If these are integrated into rules in Watchman, control via FCI is not possible. 

- **Reaction:** Reaction of the robot that is executed when the rule is violated. 

|`o`<br>Cat. 1 Stop|Category 1 stop in accordance with EN ISO 13849-1|
|---|---|
||(controlled stop and shutoff of energy when standstill is reached)|
|`o`<br>Cat. 2 Stop|Category 2 stop according to EN ISO 13849-1<br>(controlled stop with maintenance of energy)|



The robot Control already takes the rules into account during the execution of the movement and thus always tries to avoid violations. If a violation cannot be prevented, the safety function initiates the safe reaction. 

Functions or parameters that need to be validated are shown in the rule window with the validation symbol. If the rule is validated, this symbol is green. If validation is required, this symbol is orange. 

If "Inside/Outside area" is selected in the "Activation Space" or "Safety Function" field of a rule, this area must be configured by clicking on the "Configure" button that appears. The following view opens. 



R02210/1.4/EN 

Franka Robotics GmbH © 

126 

###### SAFETY CONFIGURATION/WATCHMAN 

Fig. 12.12: Configuration of ”Activation Space” 

With the selection field "Type of area" you can determine whether the robot is not allowed to leave the cuboid area (stay inside area) or not allowed to enter the cuboid area (stay outside area). The tool, flange, wrist and elbow are monitored here. 



Fig. 12.13: monitoring 

To define the cuboid area, it’s reference corner must first be determined. To do this, you can guide the TCP of the robot to the reference corner and teach the position values by clicking on "Take from Robot" or enter the position values manually. In case of manual entry, the coordinates are entered in the coordinate system of the robot. 

The reference corner must be selected in such a way that the opposite corner is created with positive values only. Then the spatial extension must be defined by entering the XYZ values. For this purpose, the space can also be taught by guiding the robot TCP to the opposite corner point. 

With the help of "Orientation", the defined space can also be rotated around the three axes. The pivot point is the set reference corner. 



When the cuboid area has been defined, the settings must be saved. Then the validation button becomes active. After clicking on "Validate", the validation specifications and the entered values are compared. The robot must now be moved in all 3 directions in and out of the created space. Depending on whether "Stay inside area" or "Stay outside area" is selected, "Violated" appears with a red dot if the function is violated. This can be used to check whether the area boundaries correspond to your specifications. 

After the check has been done, the area is confirmed by clicking on "Confirm Validation". Next to the button, the validation is then confirmed in green and after returning to the rule, the validation symbol of the rule parameter appears in green. 

If "Maximum Speed" is selected in the "Safety Function" field of a rule, this area must be configured by clicking on the "Configure" button that appears. The following view opens. 

R02210/1.4/EN 

Franka Robotics GmbH © 

127 

SAFETY CONFIGURATION/WATCHMAN 



Fig. 12.15: Setting of speed 

The maximum permissible speed determined from the risk assessment must be set and confirmed by clicking on "Save". The entry must then be validated by clicking on "Validate". 

After validation of the set speed, the validation must be completed by clicking on "Confirm Validation". 

Next to the button, the validation is confirmed by a green symbol and after returning to the rule, the validation symbol of the rule parameter appears in green. 

#### **12.7 Validate** 

After changes have been made to the settings in Watchman, validation must take place. The structure of Watchman is such that rules only need to be validated if an included parameter has been changed and a scenario only if an included rule has been changed. 



Fig. 12.16: Validation structure 

R02210/1.4/EN 

Franka Robotics GmbH © 

128 

###### SAFETY CONFIGURATION/WATCHMAN 



Fig. 12.17: Validating 

Non-validated rules are indicated by the orange validation icon in the lower right corner. To validate a scenario, click on "Validate Rules" above the listed rules. 



Fig. 12.18: Validating of rules 

All rules of the scenario are now listed with the respective parameters. In the first step, the rule parameters and then the rule itself must be validated in the unconfirmed rules, as described previously. The procedure for validating the various safety functions is described below: 

###### **Validating safe inputs** 

- Check whether the activation condition matches the safety concept defined by the risk analysis. 

- Connect peripheral devices to the safe input. 

- Check whether the status displayed in the Watchman UI changes when the input is triggered. 

###### **Validating SLP-C** 

- Check whether the parameters of the safety functions correspond to the safety concept defined by the risk analysis. 

R02210/1.4/EN 

Franka Robotics GmbH © 

129 

###### SAFETY CONFIGURATION/WATCHMAN 

###### **Validating SLS-C** 

- Guide the robot in Programming mode so that the defined rules are violated. 

- Check that the violation state displayed next to the safety function in the Watchman UI changes when the rules are violated at the expected positions/orientations. 

###### **Validating SEEPO** 

- Check that the power supply to the end effector is switched off in all expected situations. 

###### **Validating the entire rules, scenarios and overall configuration** 

- Check whether the parameters of the safety functions correspond to the safety concept defined by the risk analysis. 

- Check at each level whether the combination of activation triggers, safety functions, reactions, rules and scenarios correspond to the safety concept defined by the risk analysis. 

To validate the rule, click on "Confirm Validation" or check the box next to the rules to be confirmed and then click on "Confirm Selected Rules" above the rules. 

All rules are now displayed as validated. 

The next step is to confirm the security scenario by clicking on "Confirm Whole Security Scenario". The Watchman overview is now displayed again and the security scenario that has just been confirmed is now shown as validated. 

All scenarios that have not been validated must be treated within the manner described above. 

After all scenarios have been validated, the "Report & Commit" button appears in the upper left corner. 



Fig. 12.19: Validating Watchman 

Click on "Report & Commit". The security report opens, which is generated from Watchman settings. 

This report contains all the relevant information for documenting the security functions, including the generated checksum. 

The report must now be printed and signed. 

R02210/1.4/EN 

Franka Robotics GmbH © 

130 

###### SAFETY CONFIGURATION/WATCHMAN 



Fig. 12.20 Safety Report 

By subsequently checking the box "I verify that I signed the report" and then clicking on "Commit", it is confirmed that the report has been printed and signed. 

The security configuration is now saved and accepted in the system. The validation symbol next to the slide switch is now displayed in green and shows the validated state. 

By clicking on the validation symbol next to the slide switch, the current checksum of the security configuration is displayed. 

R02210/1.4/EN 

Franka Robotics GmbH © 

131 

WORKING WITH FRANKA RESEARCH 3 

## **13 WORKING WITH FRANKA RESEARCH 3** 

#### **13.1 Robotic Basics** 

###### **Joint space** 

In joint space, a robot pose is described using the rotation angles of each of the robot's joints. In contrast to most industrial robots, which have six joints, Franka Research 3 has seven joints. This allows for extremely high flexibility. A linear movement of the end effector on the robot through space results from the superimposed interaction of the rotation of several joints. 

###### **Cartesian space** 

In Cartesian space, a robot pose is not described by the rotation angles of the individual robot joints, but is specified with relation to the reference coordinate system (world coordinate system of the robot or tool coordinate system). Here, the position and orientation of the end effector are the main focus. The threedimensional space representation of a Cartesian pose usually consists of three values of lengths (in meters) for determining the position and three values (in degrees) for the orientation of the end effector. 

For more information on robot poses, see section Redundancy in this chapter. 

Movements in Cartesian space allow the precise tracking of predefined paths in space, such as straight lines. The changing of position is called translation, while the changing of orientation is called rotation. The Cartesian motion of a robot always depends on the reference coordinate system, which can be configured for Franka Research 3 via the configuration of the end effector in the administration’s settings of Franka UI. 

###### **Redundancy** 

As Franka Research 3 has seven joints, the Arm can reach a certain Cartesian pose with various joint configurations. This capability is called redundancy. The part of the robot that can still be moved while keeping the end effector pose the same is often called 'elbow' because it matches the motion capability of the elbow in a human arm. The redundancy of the Arm allows for greater flexibility when teaching or executing tasks, e.g., using it to circumnavigate an obstacle to grip an object located behind it. The behaviour of the robot’s elbow can be changed and adapted to each situation. It can be set to freely movable or immovable. 

###### **Sensitivity** 

The Arm has torque sensors in all seven joints. The torque sensors enable, among other things, to recognize and react to even the smallest forces acting on the Arm. This sensitivity facilitates numerous functionalities and capabilities, such as impedance or sensitive collision detection. For achieving maximum sensitivity, the robot system must be adapted in the best possible way to the additional masses attached to and picked up by the robot. For this reason, the end effector must be configured as precisely as possible in the Franka UI settings. 

###### **Impedance** 

Impedance is a robot's behaviour that imitates the ability of a mechanical spring. An impedance-controlled robot can interact gently with the environment, e.g., to not damage fragile objects. The ability to change impedance can be seen as similar to that of a human arm, which tenses the muscles to change rigidity and can adapt depending on the situation to increase robustness when executing a task. 

###### **Collision detection and reaction** 

Torque sensors have been incorporated into all seven axes. These provide information on the currently applied torques per axis at any given time. In combination with our model-based Control of Franka Research 3, contact forces and torques of the joints can be precisely determined. Then, the Arm can respond. For example, if the Arm touches an unexpected object while moving, this contact is detected in real time by one or more torque sensors and classified as a collision. This can then be used, for example, to stop the movement of the robot. 

**_NOTICE_** 

The robot’s reaction to collisions depends on the users programming and is not a safety feature. 

R02210/1.4/EN 

Franka Robotics GmbH © 

132 

###### WORKING WITH FRANKA RESEARCH 3 

###### **Generating forces** 

The Arm is in intended contact with its surroundings. With the help of the torque sensor signals, a defined force on the point of contact can be generated by the motors. To achieve this, suitable apps or programming are required. 

**_NOTICE_** 

External wiring adds additional loads and torques to the Arm which may influence the Franka Research 3‘s control performance. 

#### **13.2 Single Point of Control** 

The system provides Single Point of Control (SPoC) functionality to comply with regulations. This means that only one user at a time can trigger critical actions, i.e., edit system settings and Tasks, or trigger active robot actions like unlocking joints and running Tasks. The user in control gets assigned the SPoC software token. 

SPoC also applies to Fieldbuses. See section Fieldbus control in this chapter. 

**_NOTICE_** 

Even without the SPoC token, it is still possible to trigger uncritical actions like stopping a running Task or locking the robot brakes. 

###### **Take control** 

When connecting to the robot with an available token, take control by accepting the dialog displayed after login. The token is now assigned to you. Other users cannot control the robot without your consent. 

###### **Request control** 

When connecting to the robot with a token already taken by another user, request control by accepting the dialog displayed after login. The controlling user will be shown a control request dialog on the screen. The token is reassigned to the requesting user if the controlling user grants access. If the controlling user denies access, the token will remain with the controlling user. 

###### **_NOTICE_** 

For improved traceability, it is recommended to set up named profiles for each user in the system settings. That way, the system is able to inform newly connected users about who is currently controlling the robot. 

R02210/1.4/EN 

Franka Robotics GmbH © 

133 

WORKING WITH FRANKA RESEARCH 3 

A user requests control: 





Fig. 13.2: User management waiting for approval 

The user who has the SPoC token receives the control request: 



Fig. 13.3: User request 

###### **Enforce control** 

It is possible to enforce control if the user has physical access to the robot. Instead of requesting control, the user chooses to enforce control in the dialog displayed after login. After choosing enforced control, the requesting user has a time window in which he can press the blue circle on the robot’s Pilot to take control. The controlling user is notified about the enforcement attempt during this time frame. The controlling user is then able to confirm or deny control. 

R02210/1.4/EN 

Franka Robotics GmbH © 

134 

###### WORKING WITH FRANKA RESEARCH 3 

###### **_NOTICE_** 

Adjust the time window for control enforcement in the system settings. By default, the time window is set to 30 seconds. 

New user enforces control: 



Fig. 13.4: Enforce control 

###### **Enforce control** 

After the controlling user has finished working with the robot, the controlling user can release control in the robot menu. This will lock access to the controlling user and release the token. Other users can now connect to the robot and take control directly. Control is also released if the controlling user logs out. 

###### **Fieldbus control** 

It is also possible to control the robot through Fieldbus interfaces. Single-Point-of-Control also applies to Fieldbus interfaces. The required functionalities are provided for the supported Fieldbus protocols but must be considered during connection implementation. Data access and uncritical actions are possible via Fieldbuses regardless of the token status. 

Franka Research 3 implements OPC UA server functionality. 

###### **_NOTICE_** 

All Fieldbuses have the same rights as the operator role. 

###### **_NOTICE_** 

If the robot is controlled via a Fieldbus protocol, there is no request procedure for other users trying to take control via Franka UI. When a Franka UI user takes control, the token is automatically reassigned from the Fieldbus protocol towards the user. 



For more information on how to use Modbus and OPC UA, see the respective manual at Franka World. 

R02210/1.4/EN 

Franka Robotics GmbH © 

135 

###### WORKING WITH FRANKA RESEARCH 3 

#### **13.3 Operating Modes** 



Fig. 13.5: Overview operating modes 

Franka Research 3 offers the following operating modes: 

1. Programming 

   - Idle (default) 

   - Teach a Task (Enabling Button, Guiding Button) 

   - Test & Jog (External Enabling Device, Hold-to-run button in Desk) 

2. Execution 

   - Work (default) 

   - Monitored stop 

   - Assist (Enabling Button, Guiding Button) 

###### **Switching** 

Switch between the general "Programming" and "Execution" modes using the toggle button in the Desk sidebar. Certain user interactions select all other modes implicitly within the general modes, e.g., pressing the External Enabling Device in "Programming." 

The general operating modes can also be switched via Fieldbus control. 

R02210/1.4/EN 

Franka Robotics GmbH © 

136 

###### WORKING WITH FRANKA RESEARCH 3 

##### **13.3.1 Programming** 

Programming mode is an operating mode in which the robot can be programmed to execute certain Tasks. 

Controlling the robot via FCI is not possible in "Programming" mode. 

###### **Teach a Task (Guiding Enabling Device)** 

The administrator teaches the robot by parameterizing the Task and its Apps. This is done by hand-guiding the robot with the Enabling and Guiding Buttons at the Pilot-Grip. See chapter 0 ” 

Teach a Task 

”. 

###### **Test & Jog (External Enabling Device)** 

The administrator tests and monitors the execution while standing back from the robot. The External Enabling Device connected to the robot via the dedicated X4 port is used. For more information, see chapter 13.6.11 “Test & Jog“. 

###### **Typical procedure for programming** 

Proceed as follows when programming with the Franka Research 3: 





###### **Teach a Task (1)** 

Teach Franka Research 3 a Task. 

###### **Test & Jog (2)** 

Step out of the maximum workspace and check whether the taught Task is correctly executed. For this, the velocity can be limited, and the execution can be stopped at any time. 

###### **Run a Task (3)** 

Once the Task has been taught, Franka Research 3 executes the Task automatically. 

R02210/1.4/EN 

Franka Robotics GmbH © 

137 

###### WORKING WITH FRANKA RESEARCH 3 

##### **13.3.2 Execution** 

Execution mode is an operating mode in which the robot executes the tasks previously taught via the Franka UI or can be moved via the Franka Control Interface. 

###### **Work** 

In Work mode, automatic execution of Tasks without the requirement of safe External Enabling Devices is activated. For more information, see chapter 13.4 “Work“. 

###### **Monitored stop** 

The robot is at a supervised standstill. This mode is present in the following cases: 

A safety sensor connected to a safe input configured in a dedicated safety rule using the SMSS safety function detects the presence of a human. 

A transition mode to offer Assist mode to the user. 

###### **Assist** 

This mode can be used during execution if hand-guiding is part of the application. This mode is only permitted within the collaboration space defined. 



Fig. 13.7: Assist operation 



###### **WARNING** 

###### **Hot Surfaces and Guiding** 

At ambient temperatures above 30 °C the robot surface can become too hot to touch. Therefore, using the Assist feature in Execution mode is not permitted above 30 °C 

R02210/1.4/EN 

Franka Robotics GmbH © 

138 

WORKING WITH FRANKA RESEARCH 3 

##### **13.3.3 Overview of the status indicators** 

Status lights on both sides of the base take on the corresponding color, similar to a traffic light. The status lights will flash slowly during boot-up, when Franka Research 3 requires attention, or when the user enters values. The lights are lit in the corresponding color of the Franka Research 3 status during other processes. A circular status light in the middle of the Pilot-Disc indicates Franka Research 3’s status as well. 

When the operator is interacting with the Arm, the status light on the Pilot-Disc is switched off. 

For more information on the color behavior, see chapter 11.1 “Switching On“. 



###### **WARNING** 

###### **Dangerous and uncontrolled motions of the Arm** 

Risk of severe injury, such as crushing, tearing of the skin, and puncturing from the Arm and end effectors. 

- Ensure that the end effector and/or the object mass and the Center of Mass (CoM) are parameterized correctly. 

- Keep out of the workspace during operation. 

###### **_NOTICE_** 

The motion speed in Teach or Hand-Guiding Mode is pre-set. The speed can be reduced according to the risk evaluation of the Arm within its application. 

##### **13.3.4 Step-by-step overview of operating modes and corresponding status indicators** 

1. Switch on the Control. 

_The fail-safe locking system is activated, and motions are locked mechanically._ 

_During boot up, the lights flash slowly white._ 

_When booted up, lights are lit blue continuously, indicating brakes are still engaged._ 

2. To open the fail-safe locking system, click “unlock joints” in the sidebar of Desk. _The display lights are lit_ _<u>white continuously.</u>_ 

_During unlocking, lights are slowly flashing blue. After unlocking, the lights are again blue continuously._ 

_The Desk sidebar shows “joints unlocked.”_ 

_Franka Research 3 is in Work mode._ 

3. Switch to “Programming” mode in Desk. 

_Franka Research 3 is in “idle” mode._ 

_The lights are lit_ _<u>white continuously.</u>_ 

R02210/1.4/EN 

Franka Robotics GmbH © 

139 

###### WORKING WITH FRANKA RESEARCH 3 

4. To guide the Arm manually for teaching, press the Guiding Button while half-pressing the Enabling Button at the same time. 

_The lights are lit_ _<u>white continuously.</u>_ 

5. Release the Buttons. 

_Franka Research 3 is in “idle.”_ 

_The light is lit white continuously._ 

6. Leave the maximum workspace and take the External Enabling Device and the Emergency Stop Device with you to perform Test & Jog. 

7. Press the External Enabling Device. 

_Franka Research 3 is in "Test & Jog" mode._ 

_The light is lit blue continuously._ 

8. Press the Play button in Desk. 

_If a countdown was configured (see section Initiating motion in chapter 13.6.11 “_ Test & Jog _”), the robot light lights up fast-flashing green until the countdown expires._ 

_Afterward, the Task starts execution._ 

_During execution, the robot light is lit green._ 

In case of error or safety violation, the light turns red. 

If conflicting safe inputs are present, the light turns pink (flashing slowly). 

9. Switch to “Execution” mode in Desk. 

_Franka Research 3 enters “Work“ mode._ 

_The light is lit blue._ 

_Tasks can be executed without External Enabling Device._ 

_During execution, the light is lit green._ 

By triggering a safely monitored standstill from the safety configuration (e.g., from safe input), Franka Research 3 enters “monitored stop mode.” 

10. Press the Guiding Button and the Enabling Button. 

_Franka Research 3 goes into “Assist” mode and can be guided as part of the Task._ 

R02210/1.4/EN 

Franka Robotics GmbH © 

140 

###### WORKING WITH FRANKA RESEARCH 3 

#### **13.4 Work** 

In Work mode, the robot executes its task autonomously. Compared to Test & Jog, there is no External Enabling Device as a safeguard, i.e., the operator needs to be safely separated from dangers presented by the Arm (acc. to EN ISO 10218-1:2011 and ISO 10218-2). 



Fig. 13.8: Area assignment 

<u><mark>1</mark> Maximum workspace</u> <u><mark>3</mark> Perimeter safeguarding</u> <u><mark>2</mark> Safeguarded space</u> 

Precondition 

- A Task has been created in Teach a Task 

- The Task has been successfully tested in Test & Jog. 

- The safety system is running without violations and errors. 

###### **_NOTICE_** 

Always evaluate the remote start of the execution and realize the safety concept within the safety design (e.g., external safety means) and the safety settings of the robotic system. 



Fig. 13.9: Work operation 

R02210/1.4/EN 

Franka Robotics GmbH © 

141 

###### WORKING WITH FRANKA RESEARCH 3 

**_NOTICE_** 

Noise levels during operation < 70 dB (A) 

Procedure 

   1. Switch to the “Execution” operating mode 

   2. Press the Play Button in Desk. 

- _A confirmation dialog is shown._ 

   3. Confirm the dialog. 

- _The robot executes the learned task._ 

###### **_NOTICE_** 

If a collision occurs, the execution is stopped. The failed App is highlighted, and an error description is displayed. In this mode, the Arm can be moved using guiding and any causes of error can be eliminated. 

###### **_NOTICE_** 

Any error message is displayed in the sidebar. There, information on the error and how to eliminate it can be viewed. 

1. To continue with the execution, press the Play button for one of the Apps. 

2. To end the Task, press the Stop button. 

###### **_NOTICE_** 

The remote execution start must be evaluated during the realization of the specific cell safety concept. 

###### **Requirements for using the Franka Control Interface (FCI)** 

- Der FCI-Mode is activated (see 11.5 “Typical Usage”). 

- A network connection exists with the Linux workstation. 

- The safety system operates without violations and errors. 

- Brakes are open. 

- The control system is in Execution mode. 

###### **_NOTICE_** 

In the event of an error during control via FCI, the current operation is aborted and the resulting error is transmitted via the FCI. In Franka UI an error message is shown. 

The user's program must now be designed so that the errors are automatically transmitted as output. 

R02210/1.4/EN 

Franka Robotics GmbH © 

142 

###### WORKING WITH FRANKA RESEARCH 3 

#### **13.5 Assist** 

The Assist mode is a state of the Execution operating mode. This mode enables collaborative operation with manual guidance in accordance with ISO 10218-1. In order for it to be usable, this mode must be explicitly enabled by a safety operator in Watchman. 

If the robot is placed in Save Monitored Standstill (SMSS) during the execution of a task, the robot automatically switches to Assist Mode when the Enable and Manual Guidance buttons are pressed. This state is displayed in the robot's status message in DESK. 



Fig. 13.10: Indication of Assist Mode 

In this mode, the operator can move the robot in manual control by pressing the Enabling Button on the robot's Pilot-Grip. 



Fig. 13.11: Conditions for motion enabling in Assist Mode 



###### **WARNING** 

###### **Hot Surfaces and Guiding** 

At ambient temperatures above 30 °C the robot surface can become too hot to touch. Therefore, using the assist feature in automatic mode is not permitted above 30 °C. 

If the **S** afely **M** onitored **S** tand **S** till condition (SMSS) is removed again, the robot resumes execution of the stopped task and moves to the next pose. 

R02210/1.4/EN 

Franka Robotics GmbH © 

143 

###### WORKING WITH FRANKA RESEARCH 3 

When using the Franka Control Interface (FCI), an error message is issued by the SMSS and the execution of the robot movement is stopped. The cancellation of the SMSS does not automatically lead to a restart of the robot. This must be restarted via the command input. 

###### **Condition for initiating Assist Mode:** 

- Activated Assist-Mode in the Safety Settings in Watchman. This activation can only be done by a safety operator. 

- The robot must be in **S** afe **M** onitored **S** tand **S** till (SMSS). For this purpose, a rule must be created in the Work Scenario in Watchman that brings the robot into the safe monitored state ( **S** afe **M** onitored **S** tand **S** till). The trigger for this rule can be the processing of a safe input signal (X3.2 or X3.3) or the entry into a defined safe space. It is recommended to initiate the triggering of the safe monitored standstill by a safe input signal. 

- Press the Enabling Button and the Guiding Button. 

###### **Options for movements in Assist Mode:** 

- By pressing the Enabling and Guiding Buttons on the Pilot Grip, the robot can be moved freely in Hand Guiding mode. 

- Movements of the mounted end effector are not enabled in Assist mode. 

###### **Exiting the Assist Mode:** 

The Assist mode is automatically stopped when the Enabling Button or the Guiding Button is released. 



###### **CAUTION** 

If the **S** afe **M** onitored **S** tand **S** till (SMSS) is triggered by a monitored space, the robot immediately moves to the next pose when the Enabling or the Guiding Button is released outside the monitored space. Therefore, plan a safe input (X3.2 or X3.3) for the use of the Assist Mode to initiate the **S** afe **M** onitored **S** tand **S** till (SMSS). 

R02210/1.4/EN 

Franka Robotics GmbH © 

144 

###### WORKING WITH FRANKA RESEARCH 3 

#### **13.6 Franka UI** 

Franka UI is the user interface of the robots from Franka Robotics. It can be used to program and operate the robot in Desk. General settings can be made via Settings and the necessary safety adjustments are configured via Watchman. 

Franka UI is always reachable via the URL https://robot.franka.de if the user terminal is connected to X5 -robot network at the robot base and the DHCP client is activated. 

##### **Login** 

After entering the URL https://robot.franka.de the login to the user interface appears. 



Fig. 13.12: Login Franka User interface 



- **1 Language selection** 

Click to select the available languages for the user interface. 

- **2 Network Status** 

Display of the current IP address of the robot and the registered name of the robot in Franka World. 

Clicking opens a menu with the following selection: 

- <u>Link to Franka World, with indication whether the robot is connected to Franka World (green or red</u> dot). 

- <u>Shut Down Button, to shut down the robot.</u> 

- <u>Manuals Button, Clicking on it opens a download page of the Control with the possibility to open the</u> user manual in all available languages. 

R02210/1.4/EN 

Franka Robotics GmbH © 

145 

###### WORKING WITH FRANKA RESEARCH 3 



Fig. 13.13: Download User Manual 

- **3 Login** 

   - Input field for login; after a user logs in, the view of DESK appears. 

- **4 Watchman** 

Direct access to the Watchman user interface in viewing mode. 

- **5 Download Log** 

Button for downloading the log files of the Robot. 

##### **Desk** 

###### **Overview** 

Desk is the user interface in Franka UI for programming, configuring and operating the robot. To open Desk, enter the following URL in the browser: https://robot.franka.de and log in. 

In Desk, you can create Tasks. Tasks are chronological sequences of Apps. Apps, in turn, are the building blocks of a Task and outline the basic abilities of Franka Research 3, e.g. "Grasp", "Put down" or "Press button". 



Fig. 13.14: Desk 

|1|Quick Navigation|5<br>Timeline|
|---|---|---|
|2|Language selection|6<br>Tasks|
|3|System Menu|7<br>Apps|
|4|User Menu|8<br>Sidebar|



R02210/1.4/EN 

Franka Robotics GmbH © 

146 

###### WORKING WITH FRANKA RESEARCH 3 

###### **1 Quick Navigation** 

To switch quickly between the displays of Desk, Watchman and Settings. 

- **2 Language Selection** 

Click to select the available languages for the user interface. 

###### **3 System Menu** 

Display of the current IP address of the robot and the registered name of the robot in Franka World. 

Clicking opens the system menu with the following selection: 

- <u>Link to Franka World; with indication whether the robot is connected to Franka World (green or red dot).</u> 

- <u>Reboot Button; to reboot the Robot.</u> 

- <u>Shut Down Button, to shut down the robot.</u> 

- <u>Activate FCI Button.</u> 

- <u>Manuals Button; Clicking on it opens a download page of the Control with the possibility to open the user</u> manual in all available languages. 

###### **4 User Menu** 

The login information displays the currently logged in user and their role. Clicking this button opens the User menu with the following selection: 

- <u>Release Control; Handing over control of the robot.</u> 

- <u>Log Out; Logout of the current user from the user interface.</u> 

- **5 Timeline** 

Arrange your apps in the timeline to program your task. The timeline represents the chronological sequence of a task. 

###### **6 Tasks** 

All configured tasks of the robot are listed in the "Tasks" area. Here you can access existing tasks and manage the tasks. You can also create, download, clone, rename, or delete tasks. Import a Task by dragging and dropping a Task file downloaded from the current or another robot into the Tasks area. 

Tasks from an older generation of robot systems from Franka Robotics are not supported by Franka Research 3. 

**_NOTICE_** 

Make sure you always back up system logs, security logs, and created tasks. 

###### **7 Apps** 

All installed apps from Franka World can be viewed here. The apps from this section of Desk can be used directly in the Tasks section. Drag and drop the desired apps into the timeline to use and configure them. 

###### **8 Sidebar** 

The sidebar allows the user to control the robot by selecting pilot mode (1), selecting a hand-guide mode (2), locking/unlocking the joints (3), or turning the end effector on and off (4). It displays the current status of the robot and important messages (5 & 6). It also allows changing the operating mode (7) and starting tasks (8) to execute or test them. 

Fig. 13.15: Desk Sidebar 

R02210/1.4/EN 

Franka Robotics GmbH © 

147 

###### WORKING WITH FRANKA RESEARCH 3 

###### **1. Pilot Mode:** 

_Switching between desk control and end effector control_ 



- _Translation_ 

   - _Rotation_ 

   - _Free_ 

   - _User define_ 

**3. Locking Joints:** 

   - _Lock_ 

   - _Unlock_ 

**4. Activate End Effector:** 

   - _Switch On_ 

   - _Switch Off_ 

**5. Status indication Robot** 

   - _Status and Messages_ 

**6. Status bar** 

_Colored display of the robot status, see color table in Chapter 11.1 "Switching On“_ 

**7. Operation mode** 

   - _Programming_ 

   - _Execution_ 

**8. Execution mode** 



- Start Execution 

Fig. 13.16: Desk Sidebar 

R02210/1.4/EN 

Franka Robotics GmbH © 

148 

WORKING WITH FRANKA RESEARCH 3 

##### **Watchman** 

With the Watchman web application, only a “Safety Operator” user can edit, validate, and integrate safety settings. However, any user is authorized to view the current safety settings in Watchman. 

To view the current safety settings in Watchman, click "WATCHMAN" in the top menu bar or go to https://robot.franka.de/watchman in the browser. 



Fig. 13.17: Watchman 

The detailed description of the interface as well as the procedure for configuring the safety settings of the robot can be found in Chapter **Error! Reference source not found.** “ **Error! Reference source not found.** “. 

##### **Settings Interface** 

Various functions for configuring the robot are available to administrators in the Settings interface. 



Fig. 13.18: Menu Settings 

R02210/1.4/EN 

Franka Robotics GmbH © 

149 

###### WORKING WITH FRANKA RESEARCH 3 

|1|System Overview|5|Modbus TCP Settings|
|---|---|---|---|
|2|Network Settings|6|System Settings|
|3|User Management|7|Franka World Synchronisation|
|4|End Effector configuration|8|Safety|



###### **1 Overview of the system status** 

   - System information about the control 

   - System information about the arm 

   - Network information of the connected networks 

- **2 Management of network configurations** 

   - Address configuration of the X5 robot network 

   - Configuration of the company network C2 

- **3** 

###### **User Management** 

   - Creating, editing and removing users 

- **4 Configuration of the end effectors** 

   - Activating the power supply of the end effector 

   - Selection of the end effector 

   - Configuration of the end effector parameters 

- **5 Modbus Configuration** 

   - Download Modbus Manual 

   - Activating the Modbus function 

   - Upload and Download the Modbus configuration 

- **6 System Settings** 

   - Downloading of System-logs 

   - Reset to factory settings 

   - Move to pack pose 

- **7 Franka World Synchronisation** 

   - Installation of Apps und Features 

   - Software-Updates with Franka World 

- **8** 

###### **Safety Settings** 

- Downloading of Safety logs 

- Configuration the delay for movement initiation 

- Configuration of SPoC-Token-forced timeout 

R02210/1.4/EN 

Franka Robotics GmbH © 

150 

###### WORKING WITH FRANKA RESEARCH 3 

##### **13.6.1 Apps** 

Apps incorporate the entire complexity of the Franka Research 3 system and represent modular building blocks of a process such as grasping, plugging, insertion, and screwing. Using Desk, Apps can be arranged to create entire Tasks in no time. The created Tasks can quickly be adapted, reused, or deployed on multiple robots to reduce set-up costs remarkably. Individual Apps and Tasks can be parameterized by teaching Franka Research 3 poses by demonstration or adding context-relevant parameters such as speed, duration, forces, and triggering actions. 



Visit our Store on <u>https://franka.world to browse our continuously growing portfolio of Apps and solutions.</u> 

##### **13.6.2 Teach a Task** 



###### **WARNING** 

**Risk of injuries during guiding** 

- Risk of tearing the skin or puncturing during guiding. 

- Do not have sharp edges in the maximum workspace. 

- Do not keep any pointed objects in the maximum workspace. 

- For more information, read chapter 0 “Practical Tips for Usage and Positioning of Franka Research 3”. 

**_NOTICE_** 

Before executing any Task with Franka Research 3, make sure to read chapter 11 “OPERATION” first. 

##### **13.6.3 Creating a Task** 

###### Procedure 

1. To create and select a new Task, click on the “+”-symbol in Tasks and assign a name. 

A new Task is created with an empty Timeline. 

2. Drag and drop the respective Apps from Apps to Timeline to program an individual Task. Alternatively, double click on the respective Apps to add it to the timeline. 

3. Arrange them in the desired sequence by dragging and dropping the Apps. The programmed Tasks are executed from left to right. 

4. To remove Apps from a Task, drag and drop the respective Apps from Timeline to Apps. Alternatively, right-click on the App to open a drop-down menu from which you can activate, deactivate, or delete individual Apps. 

5. To change Task-level settings, e.g., the execution speed, click on the Task name in Timeline. 

R02210/1.4/EN 

Franka Robotics GmbH © 

151 

###### WORKING WITH FRANKA RESEARCH 3 

##### **13.6.4 Task settings** 

Procedure 

1. Click on the Task’s name in the top left corner of Desk. 

2. Set the parameters for robot speed, compliance/stiffness, and sensitivity thresholds. 

**_NOTICE_** 

Navigation and parameterization can also be done via buttons on the Pilot. 

##### **13.6.5 Parameterization of Apps** 



###### **WARNING** 

**Falling objects from end effectors during initial installation** 

- Objects falling from the gripper lead to injuries to hands, fingers, feet, and toes. 

- Always wear personal protective equipment (e.g., safety shoes). 

- Use the appropriate type of grippers to prevent objects from falling. 

- Consider the shape, texture, and weight of the grasped objects in the risk assessment according to 102182. Using lightweight and/or round objects may reduce risks significantly. 

- Do not place your hands between grasped objects and solid objects (e.g., table). 

- Do not load the end effector before start-up, as “homing” might happen after each time brakes are unlocked upon power-up. 

After the administrator creates a Task and adds at least one App, the App parameters can be configured. 

###### Precondition 

- A Task has been created and selected to be shown in the Timeline. 

- An App has been added to the Task. 

###### Procedure 

_1._ To open an App in the created Task, click on it. 

   - _A corresponding context menu appears to set the parameters._ 

2. Follow the instructions in the App context menu to teach or parameterize poses. 

3. Hand-guide the robot to the desired pose. 

4. Press the Teach button on the Pilot-Disc to confirm the pose. 

For further information on the Pilot-Disc and its buttons, see chapter 6.1 “The Arm“. 

For further information on guiding, see section Guiding configuration in chapter 0 “ 

Teach a Task 

“. 

The context menus of the Apps vary and contain one or more steps for entering parameters, e.g., teaching poses or entering execution speed. 

Only activated Apps are executed and need to be taught. 

R02210/1.4/EN 

Franka Robotics GmbH © 

152 

WORKING WITH FRANKA RESEARCH 3 



Fig. 13.19: App parameterization 

**_NOTICE_** 

The Pilot (buttons) can also be used for navigation and parameterization. 

##### **13.6.6 Pose teaching** 



###### **CAUTION** 

- **Unexpected movement of Arm** Incorrect set mass and center of gravity values may lead to injuries, such as crushing. 

- Check the mass and center of gravity for any end effector and the objects grasped by it. 

- Correct the values if necessary. 

###### Precondition 

An App with pose parameters has been added to the Task. 

Procedure 

1. Open App by clicking on it. 

R02210/1.4/EN 

Franka Robotics GmbH © 

153 

###### WORKING WITH FRANKA RESEARCH 3 



Fig. 13.20: App interface 

2. Click on necessary Step in the App 

Guide the Arm as described in chapter 13.6.9 “Guiding” 

3. Stop guiding the Arm. 

4. Release the buttons when the correct pose is reached. 

5. Confirm the pose by pressing the Teach button. 

Teaching a pose in the App is now finalized. 

##### **13.6.7 Pose fine adjustment** 

###### Procedure 

_1._ Click the App in which you want to adjust the pose. 

_The context menu appears._ 

2. Right-click on the pose you want to adjust in the context menu. 

3. Adjust the Cartesian pose of the end effector translationally and/or rotationally via the plus/minus keys (2) in single steps. When you have adjusted the pose, you can move the arm to the readjusted pose via the "HOLD TO MOVE" (3) button. 

The "TAKE LIVE POS" (4) button can be used to adopt the pose previously achieved by manual guidance and the "TAKE STORED POSE" (5) button can be used to adopt the pose currently stored in the Control as the current configuration. 

4. To save the pose, click on „SAVE“ (1). 

_The pose is adjusted._ 

R02210/1.4/EN 

Franka Robotics GmbH © 

154 

WORKING WITH FRANKA RESEARCH 3 



Fig. 13.21: Pose fine adjustment 

##### **13.6.8 Guiding configurations** 

In Guiding mode, the motion of the Arm follows the corresponding guiding configuration, which is displayed in the sidebar. The guiding configuration can be changed by pressing the Guiding-Mode Button on top of the PilotGrip. The desired configuration can also be selected from the sidebar. The following configurations can be selected: 

- Translation 

The Arm can only be moved to change the Cartesian position of the end effector. Its orientation remains as it was before entering the Guiding mode. 

- Rotation 

The Arm can only be moved to change the Cartesian orientation of the end effector. Its position remains as it was before entering the Guiding mode. The reference coordinate system for this rotation is the predefined coordinate system of the end effector. 

- Free 

The Arm can be moved freely. All seven joints can be moved. 

- User 

The user can define the guiding behavior for each Cartesian translation and rotation axis. The elbow can be movable or fixed. 

R02210/1.4/EN 

Franka Robotics GmbH © 

155 

WORKING WITH FRANKA RESEARCH 3 



Fig. 13.22: Overview of switching between Hand-Guiding-Modes 



Fig. 13.23: Illustration of Hand Guiding 

If “User mode” is selected, the user can select constraints for guiding: 



Fig. 13.24: Settings, if “User mode” is selected 

###### **Necessary guiding components** 

To guide the Arm, use the Pilot. 



Operate Desk directly via the touchscreen or using your mouse/keyboard. 



The motion speed in Teach or Hand Guiding-Mode is pre-set. In the settings of Watchman, the speed can be reduced according to the risk evaluation of the Arm within its application. 

R02210/1.4/EN 

Franka Robotics GmbH © 

156 

###### WORKING WITH FRANKA RESEARCH 3 

###### **SAFETY-INSTRUCTION** 

###### Precondition 

1. The Control must be switched on and booted up. 

2. All external devices connected to X3 must be allowed to move. 

3. Emergency stop is released. 

###### Procedure 

- Leave the maximum workspace and make sure that no other persons are within the maximum workspace. 

- On Desk, click on “Unlock joints”. 

- _Each of the seven axes makes a small movement and seven clicking noises can be heard._ 

- _The Arm is now in idle mode or monitored stop._ 

- Step back into the maximum workspace to start the guiding. 



For more information on the Pilot, see chapter 6.1 ”The Arm”. 



For more information, see chapter 0 “ 

Practical Tips for Usage and Positioning of Franka Research 3”. 

R02210/1.4/EN 

Franka Robotics GmbH © 

157 

###### WORKING WITH FRANKA RESEARCH 3 

##### **13.6.9 Guiding** 



###### **CAUTION** 

**Unexpected movement of Arm** 

- Incorrect set mass and center of gravity values may lead to injuries, such as crushing. 

- Check the mass and center of gravity for any end effector and the objects grasped by it. 

- Correct the values if necessary. 

###### Procedure 

1. Press the Guiding Button and half-press the Enabling Button. 

_Guiding is now enabled._ 

_Thestatus indicator on the base of the robot turns white._ 

2. Guide the Arm by hand. 

3. Stopp the Hand-Guiding of the Arm. 

4. Release the keys when the correct pose is reached. 

5. Confirm the Pose by pressing the Teach Button. 

Teaching a pose in the app is now completed _._ 



Fig. 13.25: Hand guide approval 

###### **_NOTICE_** 

Do not use the external Enabling Button to guide the robot as it will lead to an error. 

###### **_NOTICE_** 

Do not guide the Arm when locked. 

###### **_NOTICE_** 

The vibration transmitted during hand-guiding is below 2.5 m/s². It was tested according to the test methods defined in DIN EN 1032:2009-02. 

R02210/1.4/EN 

Franka Robotics GmbH © 

158 

###### WORKING WITH FRANKA RESEARCH 3 

##### **13.6.10 Editing end effector settings** 

A correct configuration is essential for operating Franka Research 3. When configuration is incorrectly, gravitational forces are not entirely compensated, and the Arm controls to the wrong target values. 

Procedure 

1. Go to Franka UI. 

2. Click on Settings. 

_3._ Select the end effector sub-menu. 

_The input mask opens._ 

4. Enter the respective technical data, e.g., mass or mass inertia matrix. 

In case of incorrect configuration, the following behavior might occur: 

- The Arm may pull in certain directions in guiding mode. 

- The control in operating mode may be affected so that the expected sensitivity of the Arm for collision detection is reduced. 

- The tracking behavior may be affected. 

As soon as the Task is taught and the correct end effector settings are set, switch to Test & Jog to test the Task at a reasonable execution speed. Make sure that there are no collisions and that everything works fine while being able to stop at any time by releasing the External Enabling Device. 

##### **13.6.11 Test & Jog** 

###### **_NOTICE_** 

Before executing any Task with Franka Research 3, make sure to read chapter 11 “OPERATION” first. 

##### **Initiating motion** 

An optional countdown for Task execution can be configured and edited in Settings. 

When starting a Task in either Test & Jog or Work mode, the countdown is displayed before executing the Task. During the countdown, the LEDs on the robot base will indicate the started Task by fast-flashing in green. 

###### **_NOTICE_** 

After a system reboot, the control token is being reset. 

**_NOTICE_** 

Adjust the waiting time in the system settings. By default, the waiting time is set to 0 seconds. 

R02210/1.4/EN 

Franka Robotics GmbH © 

159 

###### WORKING WITH FRANKA RESEARCH 3 



Fig. 13.26: Test & Jog 

###### **Testing** 

###### **SAFETY-INSTRUCTION** 

Precondition 

- The robot has learned a Task. 

- The External Enabling Device must be connected to X4. 

- The operator must have left the maximum workspace. 

- The operator must check that all other persons have left the safety zone. 

- The operator must direct his full attention to the pending robotic motion. 

###### Procedure 

To enable the robot, press the button on the External Enabling Device.Optional: Select an appropriate execution speed in the “Operation” section of the sidebar. _Default speed is 0.25m/s_ 

Press and hold the Test&Jog play button in the “Operation” section of the sidebar. 

Task execution will be terminated if either the Play button or the External Enabling Device is released. 

If a countdown for Task execution has been configured, a confirmation dialog is shown as well. During the countdown, the execution can still be cancelled. Robot lights are flashing green quickly during the countdown. 

If the robot executes the task as intended, proceed to chapter 13.4 “Work“. 

If adjustments need to be made, go back to chapter 13.6.2 “Teach a Task “. 

###### **_NOTICE_** 

The system monitors the connection of the Franka UI hold-to-run control with a maximum timeout of 1 s. If a connection loss is detected while a hold-to-run control is pressed, the system is stopped. 

R02210/1.4/EN 

Franka Robotics GmbH © 

160 

###### WORKING WITH FRANKA RESEARCH 3 

#### **13.7 Franka Control Interface (FCI)** 

<mark>The Franka Control Interface (FCI) allows a fast and direct low-level bidirectional connection to the Arm, Franka Hand and Cobot Pump. It provides the current status of the robot and enables its direct control with an external workstation PC connected via Ethernet.</mark> 



Abb.13.1 Schematic overview FCI 

<mark>Using libfranka, our open source C++ FCI client, you can send real-time control values at 1 kHz with 5 different interfaces</mark> : 

- <mark>Gravity & friction compensated joint level torque commands.</mark> 

- Joint position commands 

- Joint velocity commands. 

- Cartesian pose commands. 

- Cartesian velocity commands. 

<mark>At the same time, you get access to 1 kHz measurements of:</mark> 

- Measured joint data, such as the position, velocity and link side torque sensor signals. 

- Estimation of externally applied torques and forces. 

- Various collision and contact information. 

<mark>You also get access to the robot model library which provides:</mark> 

- Forward kinematics of all robot joints. 

- Jacobian matrix of all robot joints. 

- Dynamics: inertia matrix, Coriolis and centrifugal vector and gravity vector. 

<mark>In addition, franka_ros and franka_ros2 connects Research robots of Franka Robotics with the entire ROS and ROS2 ecosystem. It integrates libfranka into</mark> <u><mark>ROS Control. Additionally, it includes URDF models and detailed 3D</mark></u> <mark>meshes of our robots and end effectors, which allows visualization (e.g. RViz) and kinematic simulations. MoveIt!</mark> <u><mark>/ Movelt!2 integration makes it easy to move the robot and control the gripper, and the provided examples in MoveIt! / Movelt!2</mark></u> <mark>show you how to control your robot using ROS.</mark> 

R02210/1.4/EN 

Franka Robotics GmbH © 

161 

WORKING WITH FRANKA RESEARCH 3 



###### **WARNING** 

NOTICE that control of the robot via FCI is not possible when the SLP-C, SLS-C or SLP-J functions are active. This affects the safety functions that include spatial position monitoring (Inside/Outside Area) and Cartesian velocity monitoring (maximum speed). If these are used in rules in Watchman, control via FCI is not possible. 

**_NOTICE_** 

Data is sent over the network with a frequency of 1 kHz. Therefore, a good network connection is required! 

###### **_NOTICE_** 

While the FCI is active you have full, exclusive control of the Arm and Franka Hand. This means that Arm control cannot be performed via Apps and FCI at the same time! 

##### **13.7.1 Working in principle with the FCI interface** 

Controlling the robot via the FCI interface can be realized by using libfranka in the C++ environment. A sound knowledge of Linux environment and C++ programming is recommended for this purpose. Alternatively, the robot can be controlled via the FCI interface by ROS, ROS 2. 

The following section describes the basic procedure for programming with the help of libfranka in the C++ environment. 

###### **Executables** 

Via the libfanka described before in chapter 13.7 "Franka Control Interface (FCI)" executable files (executables) can be created. 

In the "examples" subfolder of libfranka, examples of executables are listed. You can use these as a base to get started easily and create copies from them that are customized according to your requirements. 

Below you will find the source code of the example " _generate_joint_position_motion.cpp_ " from libfranka to explain the structure of a script. 

```
// Copyright (c) 2017 Franka Robotics GmbH
// Use of this source code is governed by the Apache-2.0 license, see LICENSE
#include <cmath>
#include <iostream>
#include <franka/exception.h>
#include <franka/robot.h>
#include "examples_common.h"
/**
 * @example generate_joint_position_motion.cpp
 * An example showing how to generate a joint position motion.
 *
 * @warning Before executing this example, make sure there is enough space in front of the robot.
 */
int main(int argc, char** argv) {
  if (argc != 2) {
    std::cerr << "Usage: " << argv[0] << " <robot-hostname>" << std::endl;
    return -1;
  }
```

R02210/1.4/EN 

Franka Robotics GmbH © 

162 

###### WORKING WITH FRANKA RESEARCH 3 

```
  try {
    franka::Robot robot(argv[1]);
    setDefaultBehavior(robot);
    // First move the robot to a suitable joint configuration
    std::array<double, 7> q_goal = {{0, -M_PI_4, 0, -3 * M_PI_4, 0, M_PI_2, M_PI_4}};
    MotionGenerator motion_generator(0.5, q_goal);
    std::cout << "WARNING: This example will move the robot! "
              << "Please make sure to have the user stop button at hand!" << std::endl
              << "Press Enter to continue..." << std::endl;
    std::cin.ignore();
    robot.control(motion_generator);
    std::cout << "Finished moving to initial joint configuration." << std::endl;
    // Set additional parameters always before the control loop, NEVER in the control loop!
    // Set collision behavior.
    robot.setCollisionBehavior(
        {{20.0, 20.0, 18.0, 18.0, 16.0, 14.0, 12.0}}, {{20.0, 20.0, 18.0, 18.0, 16.0, 14.0, 12.0}},
        {{20.0, 20.0, 18.0, 18.0, 16.0, 14.0, 12.0}}, {{20.0, 20.0, 18.0, 18.0, 16.0, 14.0, 12.0}},
        {{20.0, 20.0, 20.0, 25.0, 25.0, 25.0}}, {{20.0, 20.0, 20.0, 25.0, 25.0, 25.0}},
        {{20.0, 20.0, 20.0, 25.0, 25.0, 25.0}}, {{20.0, 20.0, 20.0, 25.0, 25.0, 25.0}});
    std::array<double, 7> initial_position;
    double time = 0.0;
    robot.control([&initial_position, &time](const franka::RobotState& robot_state,
                                            franka::Duration period) -> franka::JointPositions {
      time += period.toSec();
      if (time == 0.0) {
        initial_position = robot_state.q_d;
      }
      double delta_angle = M_PI / 8.0 * (1 - std::cos(M_PI / 2.5 * time));
      franka::JointPositions output = {{initial_position[0], initial_position[1],
                                        initial_position[2], initial_position[3] + delta_angle,
                                        initial_position[4] + delta_angle, initial_position[5],
                                        initial_position[6] + delta_angle}};
      if (time >= 5.0) {
        std::cout << std::endl << "Finished motion, shutting down example" << std::endl;
        return franka::MotionFinished(output);
      }
      return output;
    });
  } catch (const franka::Exception& e) {
    std::cout << e.what() << std::endl;
    return -1;
  }
  return 0;
}
```

In C++ texts are excluded via the character string "//". These serve e.g. as information of the programmer to the program structure. 

The include command "#include <path-spec>" at the beginning of the script instructs the processor to include the content from the in the path specification at the point where the -statement is displayed. For example, you can use this to access predefined functions from libfranka. 

The line "int main(int argc, char** argv) { }" contains the command line parameters inside the single brackets. Inside the curly braces is the actual main function of the script. The main function is terminated by a closing curly bracket. 

In the main function, various commands can now be executed or calls to included sub-functions can be made. 

R02210/1.4/EN 

Franka Robotics GmbH © 

163 

###### WORKING WITH FRANKA RESEARCH 3 

As mentioned before, the control of the robot requires a profound knowledge of C++ programming. 

**_NOTICE_** 

To intercept the immediate start of the robot's movement, Franka Robotics recommends to create a query procedure at the beginning of a script, which will execute the program only after active confirmation. Such queries can also be found in the sample scripts in libfranka. 

###### **Creating or modifying executables** 

If you want to create your own executables, we recommend that you create your own project. To do this, create your project folder. In this folder you have to create a "CMakeLists.txt". This file should be structured according to the following scheme. 

```
project(hello_world)
find_package(Franka REQUIRED)
add_executable(hello_worldhello_world.cpp)
target_link_libraries(hello_world Franka::Franka)
```

Store your source code files for your executables (xxxxx.cpp) in your project folder. Add your source codes to the "CMakelists.txt" file accordingly. 

Now create a build folder in your project. And from this folder, run the following command: 

```
cmake ..
```

Your build will now be created according to the CMakeLists.txt. 

Then, to compile, run the following command from your build folder: 

```
make
```

Your project is now successfully compiled. 

###### **Execution of Executables** 

To run executables, you must run them from the build you created for your project. 

An executable is executed by opening a terminal in the build folder of your project where it is stored and executing the following command: 

```
./name executable <ip roboter>
```

Enter the name of the executable and the IP address of the robot. 

The script will now be executed. 



###### **WARNING** 

The execution of an executable can directly initiate movements of the robot and thus lead to injuries. Before starting an executable, make sure that there are no persons in the danger zone of the robot! 

To stop / cancel the execution of an executable, you can press the key combination <CTRL>+<C>. 

R02210/1.4/EN 

Franka Robotics GmbH © 

164 

###### WORKING WITH FRANKA RESEARCH 3 

#### **13.8 Troubleshooting** 

##### **13.8.1 General use** 

###### **Recoverable errors** 

For a list of recoverable safety errors, see chapter 4.11 “Safety Functionalities“. 

|**Error**|**Solution**|
|---|---|
|Franka Research 3 indicator is lit white|Possibly one of the two buttons on the Pilot-Grip has not been pressed properly. Release<br>both buttons and half-press the Enabling Button while simultaneously pressing the<br>Guiding Button again.<br>Make sure that you do not completely press down the Enabling Button, otherwise the<br>Arm’s motion is stopped.|
|Franka Research 3 indicator changes to color<br>pink|The system is receiving conflicting enabling signals.<br>Close all inputs before moving the robot again. The opened inputs X3.1 (emergency stop)<br>and X4 (External Enabling Device) are highlighted inpinkin Desk.|
|Franka Research 3 indicator is lit or flashes<br>yellow|The system has identified a warning in the system.<br>The system might work with the active warning or not, depending on the type of warning.|
|Franka Research 3 indicatorflashesred|An application error or safety violation has occurred.<br>The error or violation must be fixed before the system fail-safe locking system can be<br>released again from Desk.|
|Franka Research 3 indicator is litred|There is a problem.<br>If this cannot be rectified by restarting the system, please contact a contact partner, a<br>service provider or us directly at: support@franka.de.|



###### **Arm pulls strongly in one direction during teaching** 

Immediately check the settings for the end effector and make sure that the correct end effector has been selected and configured. Make sure Franka Research 3 is mounted on a plain surface within the permitted tilt tolerance. 

If you connect to a third party or custom-made end effector, ensure that you have compensated it correctly by updating the transformation matrix. To set the correct tool center point, adjust the weight, set the center of mass relative to the flange. 

###### **_NOTICE_** 

If a third party or custom-made end effector has been installed, check the following: 

1. Update the transformation matrix to set the correct tool center point. 

2. Adjust the weight of the end effector. 

3. Set the center of mass relative to the flange. 

4. Update the inertia matrix. 

If the problem persists, please contact your service partner or customer support at support@franka.de. Do not operate the system until the issue is solved. 

In the case of heavy external cabling, a drift cannot be prevented as that cannot be compensated with Franka Research 3 settings for all poses. 

###### **Loud clicking at switch-off** 

The clicking results from the deployment of the fail-safe locking system and is normal. Locking pins are deployed in the joints to lock them mechanically. 

R02210/1.4/EN 

Franka Robotics GmbH © 

165 

###### WORKING WITH FRANKA RESEARCH 3 

###### **Joint limit error** 

In the event of a joint limit error, a joint of the robot was moved out of the permissible movement range. The following error message appears: 



Fig. 13.27: Message “A joint limit has been violated” 

This error can only be corrected by a safety operator. The "START RECOVERY" button appears for logged-in safety operators. 

Clicking on "START RECOVERY" starts the procedure for restoring the joint error. A dialog opens with the display of the affected joint. 



Fig. 13.28: Message with display of the faulty joint 

Now activate the External Enabling Device and click on "Move Joint Out Of Limit". Hold both until the following message appears: 

R02210/1.4/EN 

Franka Robotics GmbH © 

166 

WORKING WITH FRANKA RESEARCH 3 



Fig. 13.29: Confirmation joint is back in the limit 

The joint is now inside the movement limit again. Now click on "CONFIRM" and thereby complete the recovery. 

###### **Joint position error** 

In the presence of a joint position error, the position data of a joint has been lost in the control system. This can be caused, for example, by a power failure with the brakes open. To rectify this error, a procedure is required that enables the position assignment or joint calibration to be restored. This error is indicated by the following message in Desk. 



Fig. 13.30: Message “Joint position error detected” 

This error can only be corrected by a safety operator. The "START RECOVERY" button appears for logged-in safety users. 

After clicking on "START RECOVERY", a message is opened in which the failed joints are displayed. 

R02210/1.4/EN 

Franka Robotics GmbH © 

167 

###### WORKING WITH FRANKA RESEARCH 3 



Fig. 13.31:  Message with display of failed joints 

Click on any joint that has been reported failed. The view for restoring the joint is displayed. 



Fig. 13.32: Joint recovery locked 

Now activate the External Enabling Device and keep it pressed until the recovery of the joint is completed. Click on the unlock icon of the joint. 

R02210/1.4/EN 

Franka Robotics GmbH © 

168 

###### WORKING WITH FRANKA RESEARCH 3 

###### **_NOTICE_** 

When operating the External Enabling Device, make sure that you are outside the hazardous area to check the execution of the recovery from a safe distance. 

Now, the Robot is unlocking this joint. 



Fig. 13.33: Joint recovery ready for movement 

Then click on the "Move Joint To Ref. Position" button and keep it pressed until the reference position is reached on the robot. Alternatively, the "+ / -" keys can also be used to move the robot. 

When the joint has reached the correct position, the following message appears: 



Fig. 13.34: Conformation position reached 

Visually check whether the affected joint has moved to the reference position. If this is not the case, i.e. a joint has not moved to the correct reference position, contact Support. 

R02210/1.4/EN 

Franka Robotics GmbH © 

169 

###### WORKING WITH FRANKA RESEARCH 3 

When the joint position is in the reference position, you can release the external enabling device again. Now check the box to confirm the correct reference position of the joint and click on the "CONFIRM" button. Now, the joint position is referenced again. 



Fig. 13.35: Confirmed Joint recovery 

Now carry out the described procedure for all other joints that are still indicated as failed. 

If you do not hold the buttons to move, the following message appears: 



Fig. 13.36: Message Button not held 

If you end the procedure before reaching the reference position, the following message appears: 

R02210/1.4/EN 

Franka Robotics GmbH © 

170 

WORKING WITH FRANKA RESEARCH 3 



Fig. 13.37: Message if reference position not reached 

If you are unable to move to a joint position because it cannot be reached due to an interfering contour, you can move other joints of the robot first as required using the "+/-" keys and thus enable the reference positions of the joint to be referenced to be reached. 

When all incorrectly reported joints have been referenced, the restoration of the robot's reference position is complete. Confirm the recovery by clicking "CONFIRM". 



Fig. 13.38: Confirm the complete recovery 

The robot can now be used again. 

**_NOTICE_** 

R02210/1.4/EN 

Franka Robotics GmbH © 

171 

###### WORKING WITH FRANKA RESEARCH 3 

After restoring joint position errors, the system cannot guarantee that previously taught poses are still approached correctly. Therefore, check the poses of your tasks before you start them in Execute. 

If the recovery cannot be completed successfully, the robot hardware may have been damaged or there is a software error. In this case, shut down the system, take the robot out of operation and contact support. 

###### **Failed to unlock joints** 

If the joint unlocking process fails, follow the following steps: 

1. Shut down the robot, unplug it from its power source, and remove the connecting cable between the Arm and Control. For information on how to safely shut down Franka Research 3, see section Disconnecting Franka Research 3 from the power supply in chapter 11.6 “Switching Off and Restarting”. 

2. Check the pins for potential damage. 

   - If no damage can be observed, carefully but firmly reattach the cable and make sure it sits tight. Power up the robot and try to unlock the joints. 

3. If the issue should persist, contact your service partner or customer support at support@franka.de by providing the serial number of the Arm and the log files of the robot. You can find the log files in Desk – Settings – System – Download log files. 

###### **Robot does not finish booting** 

###### Procedure 

1. Turn off the Control. 

2. Unplug the system from its power source. 

   - For information on how to safely shut down Franka Research 3, see section Disconnecting Franka Research 3 from the power supply in chapter 10.3 “Preparing the Installation Site”. 

3. Remove the connecting cable between the Arm and Control. 

4. Check the pins for potential damage. 

5. If no damage can be observed, carefully but firmly reattach the cable and make sure it sits tight. 

6. Power up the robot. 

If the issue persists, contact your service partner or support@franka.de by providing the serial number of the Arm. 

###### **Desk continuously displays “Shutting down the system”** 

You have shut down the system. As soon as the front fans of the Control have stopped turning, the Control can be turned off using the switch on the rear side. Then the browser window of Desk can be closed. 

###### **Robot does not boot after turning on the Control** 

Occurs when the system has been turned off via Desk, but the Control power button was not turned off. Solution: Turn off the Control and wait for 1-2 minutes. Turn on again.  Control should now boot. 

###### **Restarting after an unexpected stop** 

For restarting after an unexpected stop, refer to subchapter Restarting in chapter 11.6 “Switching Off and Restarting”. 

R02210/1.4/EN 

Franka Robotics GmbH © 

172 

###### WORKING WITH FRANKA RESEARCH 3 

##### **13.8.2 Troubleshooting while using FCI** 

For errors related to the use of FCI, please refer to the online FCI documentation at https://franka.world/. 

There you will find detailed and updated information on how to fix various error scenarios that may occur. 

R02210/1.4/EN 

Franka Robotics GmbH © 

173 

MANAGING FRANKA RESEARCH 3 

## **14 MANAGING FRANKA RESEARCH 3** 

#### **14.1 Franka World** 



Franka World is an online platform that interconnects customers, partners, and software and hardware developers, whose activity revolves around Franka Robotics’s products and services. Franka World provides tools for managing Franka Research 3, access to an online store that features a continuously growing portfolio of software and hardware products, and the possibility of becoming part of an active and passionate community. 

Visit https://franka.world/ to make use of all the benefits. 



Access the Franka World User Manual to get an overview of all Franka World features and how to benefit from them: https://download.franka.de/franka-world-manual/ 

#### **14.2 Managing Apps and Updates** 

Apps and features purchased through the Franka World Store can be accessed and installed on the robot via the "Franka World" tab in the Settings interface. When the robot is online, synchronization between the robot and the Franka World account is simple and fast. However, the operator can also perform the synchronization manually on the same interface, should the robot be offline. Depending on whether the robot is online or offline, the view adjusts automatically. 



Fig. 14.1: Managing Apps and Features via Franka World 

R02210/1.4/EN 

Franka Robotics GmbH © 

174 

###### MANAGING FRANKA RESEARCH 3 

###### **_NOTICE_** 

If required, the operating system will update when new Apps or features need to be installed from Franka World. 

###### **Registering of Robot** 

###### Precondition 

- The robot must be online. 

- You must be logged in to Franka World. 





###### Procedure 

1. Navigate to Settings. 

2. Click on REGISTER DEVICE. 

_You will be redirected to a different site that states your robot’s serial number and other proof of ownership._ 

3. If required, enter your e-mail and password and log in. 

_You will be redirected to another site._ 

4. Choose an account for registering your robot. 

5. Click REGISTER. 

_The robot is now registered._ 

6. Navigate to Manage. 

7. To see all registered robots, click on Devices. 

#### **14.3 Hub** 

Hub is the central knowledge section within Franka World. It provides access to documentation, tutorials, codes, and updates about our robot of Franka Robotics and its interfaces. Find more information on <u>https://franka.world/.</u> 

R02210/1.4/EN 

Franka Robotics GmbH © 

175 

###### MANAGING FRANKA RESEARCH 3 

#### **14.4 Updates** 

###### **System updates** 

Updates for the operating system can be downloaded conveniently via the "Franka World" tab in the Settings view. To do this, the robot must have online access to Franka World. 

The Control regularly checks for available updates to the operating system and displays them in the "Franka World" tab of the Settings interface. 



Fig. 14.3: Managing of Updates via Franka World 

If you want to apply the updates, click on "DOWNLOAD". The update data will be downloaded. After the download is complete, the "Apply changes" display is highlighted. Now click on "NEXT" to perform the installation. 

After the update, the operating system will be restarted. The power supply to the robot must not be interrupted during this time. 

If your robot does not have online access to Franka World, you can also start an update manually. For this purpose, the update file can be downloaded from the Franka World page and uploaded to the robot via the operating device connected to the robot. To do this, click on "UPLOAD" in the "Franka World" tab of the Settings interface and select the previously downloaded download file. After manually uploading the update file to the robot, confirmation is required to install, analogous to the online procedure. 

After the manual installation of the update, a download button for the status file of the performed update will appear. Download the file and upload it again to your Franka World account. This status file synchronizes the update status of your robot with Franka World. 

###### **_NOTICE_** 

If required, the operating system will update when new Apps or features need to be installed from Franka World. 

R02210/1.4/EN 

Franka Robotics GmbH © 

176 

MANAGING FRANKA RESEARCH 3 

#### **14.5 Backup** 

A Backup of the Control consists of several relevant categories of Control data. These are usually: 

- Safety Configuration of the system, 

- Network Settings, 

- ModBus-Configuration, 

- End effector configuration, 

- User configuration, 

- created Tasks. 

With the actual available firmware or previous versions of the Control, a system backup must be performed manually in five individual steps. These steps are: 

- ✓ Saving of the Safety Configuration 

- ✓ Saving of the network Settings 

- ✓ Saving of the ModBus-configuration 

- ✓ Saving of the End effector configuration 

- ✓ Saving of the created Tasks 

A backup of the User administration is currently not possible. We recommend, to save the created users and their configured authorization as a screenshot and saving it as a file with the remaining backup data. With the current firmware, a restoring of the user administration can only be done by recreating the users. 

Create a backup directory for the backup files on a suitable storage medium connected to your user interface device. The steps required to create the backup data are explained below. 

##### **14.5.1 Safety Configuration** 

The safety configuration cannot be saved as a backup file in the current firmware. To perform a backup of the created configuration, the report must be opened in Watchman and saved as a PDF in the backup directory. To do this, proceed according to the following steps: 

- ✓ Select Watchman in the Desk menu 

- ✓ Click on „Report“ in the upper left corner of the Watchman user interface. 

- ✓ Save the report as a PDF and place it in the backup directory. 

There are two more parameters of the security configuration to be saved outside of the Watchman interface. To do this, proceed as follows: 

- ✓ Select „Settings“ in the DESK menu 

- ✓ Open the „Safety“ tab. 

- ✓ Take a screenshot of this view and save it in the backup directory. 

The relevant parameters in this section are: 

- Work Execution Wait Time 

- Token Force Timeout 

In case of a recovery, the parameters and rules must be entered and validated manually in Watchman or in the “Settings/Safety” tab. 

R02210/1.4/EN 

Franka Robotics GmbH © 

177 

###### MANAGING FRANKA RESEARCH 3 

##### **14.5.2 Network Setting** 

To save the network settings, proceed with the steps below: 

- ✓ Open the „Settings“ on Desk 

- ✓ Select „NETWORK“ tab 

- ✓ Take a screenshot of this view and save it in the created backup directory. 



Fig. 14.4: Network Settings 

In case of necessary configuration recovery, the parameters listed in the screenshot must be entered manually. 

##### **14.5.3 Modbus Configuration** 

To save the Modbus configuration, proceed with the steps below: 

- ✓ Open the „Settings“ on Desk 

- ✓ Select the „MODBUS TCP“ tab 

- ✓ Clicking on „DOWNLOAD“ saves the Modbus configuration with the following name on the connected user interface device: „ _modbus.json_ “ 

Save the downloaded file in the previously created backup directory. 

Via the "UPLOAD" button you can restore a backup file of the Modbus configuration to the system again. 

##### **14.5.4 End Effector Configuration** 

To save the End effector configuration, proceed with the steps below: 

- ✓ Open the „Settings“ on Desk 

- ✓ Select the „END_EFFECTOR“ tab 

- ✓ Click on the edit symbol next to „Mechanical Data“ 

- ✓ Clicking on „DOWNLOAD“ saves the Modbus configuration with the following name on the connected user interface device: „ _endeffector-config.json_ “ 

Save the downloaded file in the previously created backup directory. 

Via the "UPLOAD" button you can restore a backup file of the End effector configuration to the system again. 

R02210/1.4/EN 

Franka Robotics GmbH © 

178 

###### MANAGING FRANKA RESEARCH 3 

##### **14.5.5 Saving of the created Tasks** 

The created Tasks can be downloaded individually in the „DESK“-View. 

To download a Task, proceed with the steps below: 

- ✓ Open the „Settings“ on Desk 

- ✓ Select the desired Tasks 

- ✓ Clicking on the download symbol starts the download process. 

Save all downloaded Tasks to the backup directory. 



Fig. 14.5: Save Tasks 

To Restore a Task, move the downloaded task-file from file directory by dragging and dropping to the Task-List in DESK. 

R02210/1.4/EN 

Franka Robotics GmbH © 

179 

MAINTENANCE AND DISPOSAL 

## **15 MAINTENANCE AND DISPOSAL** 

#### **15.1 Maintenance** 

The Arm and Control of the Franka Research 3 are designed for maintenance-free operation of approx. 20,000 hours under normal operating conditions. The normal operating conditions used as a basis were derived from various representative applications of the robot system and verified by analyses and tests. If a customer application deviates greatly from these underlying operating conditions, the duration may be extended or shortened under certain circumstances. 

If the system approaches this operating duration, contacting Franka Robotics support (support@franke.de) is recommended. Evaluation of the system's log data by the support team will then indicate any necessary action. 

###### **_NOTICE_** 

If damage to the structure of the robot is detected during a visual inspection, the robot must be taken out of service regardless of the current operating time. 

###### **_NOTICE_** 

- Activate the emergency stop system during start-up every 12 months. 

- Reconnect the emergency stop system during start-up every 12 months. 

- Check all safety installations, e.g., emergency stop system, for function every 12 months. 

- Check any additional safety measures that have been taken to secure safe operation. 

#### **15.2 Cleaning** 



###### **DANGER** 

###### **Risk of electric shock** 

Improper use of liquid cleaning agents, as well as incorrectly disconnected devices from the power supply, can lead to fatal accidents. 

- Do not clean devices that have not been safely disconnected from the power supply. 

- Do not use liquid cleaning agents for cleaning the devices. 

- The following things need to be kept in mind while cleaning: 

   - Only qualified persons may carry out cleaning. 

   - Cleaning is only permissible when Franka Research 3 is safely stopped and disconnected from the power supply. 

   - Switching off and disconnecting the device must be carried out by qualified persons only. 

   - Do not use any liquids to clean the device. 

   - Do not use any cleaning chemicals. 

   - The components may only be cleaned with a dry cloth. 

   - Moisture must not enter the device. 

   - Do not apply great force to the Arm. The parts to be cleaned must be supported manually to not overload and possibly damage the Arm. 

R02210/1.4/EN 

Franka Robotics GmbH © 

180 

MAINTENANCE AND DISPOSAL 

**_NOTICE_** 

- **Material damage to the devices** 

- Do not use liquid cleaning agents for cleaning the devices. 

#### **15.3 Disposal** 

###### **Disposal** 

Disposal of Franka Research 3 must comply with the relevant country-specific laws, standards, and regulations. 

###### **Battery** 

The Control contains a coin cell battery. The cell battery must be disposed of separately according to the relevant country-specific laws, standards, and regulations. 

To remove the battery, open the Control. 

**_NOTICE_** 

Opening the Control is only allowed for the purpose of removing the coin cell battery when disposing of it. 

###### **Return of waste of packaging** 

Please contact Franka Robotics to return any used packaging. 

R02210/1.4/EN 

Franka Robotics GmbH © 

181 

SERVICE AND SUPPORT 

## **16 SERVICE AND SUPPORT** 

###### **_NOTICE_** 

If you have purchased your Franka Research 3 at one of our sales partners or if you have cooperated with a service provider, please get in contact with them first. Our partners can consolidate information and reach out to Franka Robotics for troubleshooting and further support. 

Please visit <u>www.franka.world</u> for supplemental material and additional information on our robot. 

For any other requests regarding service and support please contact us at support@franka.de. We will issue a ticket regarding your request in our service and support center and our experts will respond as soon as possible. 

When contacting our service, please have the following information available: 

- ✓ Customer no. 

- ✓ Serial no. of the control 

- ✓ Serial number of the arm 

- ✓ Log files of the system 

#### **16.1 Rescue System** 

In case the Control does not boot or an administrator login is not possible, a rescue system is implemented in the Control. 

Only basic functions for accessing the Control are supported in the rescue system. These functions can be: 

- the retrieval of system logs for further error analysis with the customer, 

- retrieving the configuration of the network setting of the Rescue System, 

- the reinstallation of the system version by synchronization with Franka World, 

- resetting the main system to factory settings. 

Robot movements or other interactions with the arm or end effector are not supported. 

To access the Rescue system user interface, connect an operator device with access to a browser to the X5 port on the arm base via an Ethernet cable. 

To manually boot the Control into the Rescue System, perform the following steps: 

- ✓ Shut down the Control, wait for the fans to switch off, then switch off the main switch. 

- ✓ Wait approx. 10 sec. before restarting the Control by switching on the main switch. 

- ✓ Wait at least 20 sec., but less than 40 sec. 

- ✓ Switch off the Control with the main switch. 

- ✓ Wait 10 sec. 

- ✓ Restart the Control by switching on the main switch. 

The Control should now boot into the rescue system. After calling up the robot.franka.de web interface on the connected user device, the following user interface is displayed in the browser. 

R02210/1.4/EN 

Franka Robotics GmbH © 

182 

###### SERVICE AND SUPPORT 



Fig. 16.1: Rescue System 

###### **Network** 

The Rescue System tries to use the stored network settings of the main system. If this does not succeed, the default settings are used. 

On this page you can temporarily adjust the network settings of the Control. The settings only apply temporarily within the Rescue System and are not adopted in the main system after a restart. 





On this page you can start a download of the log-file or initiate the factory reset. 

R02210/1.4/EN 

Franka Robotics GmbH © 

183 

###### SERVICE AND SUPPORT 



Fig. 16.3: Log Download and Factory Reset 

###### `o` **Log Download** 

When downloading logs, the Rescue System collects the log files of the main system. If the file system of the main system is corrupted, this operation may fail. 

- **Factory Reset** 

The factory reset function resets the main system. All configurations and created tasks as well as all installed apps and functions are deleted. This has no effect on the Rescue System itself. After the reset, the system must be restarted by the user. 

###### **Logging** 

###### **Franka World** 

This function allows you to reinstall or update the system software of the main system. Installing apps and features is not possible in the Rescue System. 

To ensure an error-free installation of the system software, all apps and features are deleted during this type of installation. 

After successful installation and booting of the main system, all apps and features can be reinstalled in the main system via the Franka World page. However, previously created tasks can only be restored if they have been saved or backed up separately before. 

R02210/1.4/EN 

Franka Robotics GmbH © 

184 

###### SERVICE AND SUPPORT 



Fig. 16.4: Franka World 

###### **Safety** 

This page allows to download the Safety Log. 

The Safety Log contains all safety relevant events that occurred since the first start of the robot. 



Fig. 16.5: Safety Log 

###### **Exiting the Rescue System** 

To exit the rescue system, the Control must be restarted. The Control then restarts in the regular system. 

#### **16.2 Hardware Exchange** 

In case of damage to the Control unit or the Arm, it may be necessary to carry out a replacement of the respective defective component. 

R02210/1.4/EN 

Franka Robotics GmbH © 

185 

###### SERVICE AND SUPPORT 

##### **16.2.1 Replacing the Control** 

In the case of a failed Control unit, two situations must be considered. 

1. the Control can still be started and can connect to the Franka World. 

2. the Control can no longer be started and/or synchronized with Franka World. 

For the situation that the Control still starts and can connect to Franka World, all installed features and apps can be detached from the defective Control via Franka World and made available in Franka World for transfer to the new Control. To do this, follow the steps below: 

1. Perform a backup of the Control as described in chapter 14.5 "BACKUP". 

2. Call up Franka World via the URL https://franka.world. 

3. Switch to the "MANAGE" view in the menu bar. All Control units registered to you or your company are now listed here. 

4. Select the Control unit of concern. All system information of the robot as well as the features installed on the Control are displayed. 



Fig. 16.6: Device detail view 

5. By removing the blue checkmarks, the respective features are marked for detaching from the Control. Before removing all blue check marks, take a screenshot or NOTICE which features were installed on the Control. 

6. After the blue check marks have been removed, the "Synchronized" button appears with a blue check mark. Clicking it initiates the detachment from the Control and executes it with the next synchronization of the Control. 

7. Now call up the URL https://franka.robot.de in the browser and select "Settings" in the Desk menu. 

8. Open the Franka World view. You will now see that changes are to be made to the robot. Click on "Download" to download the changes. It is also possible to manually import the update file into the system. 

R02210/1.4/EN 

Franka Robotics GmbH © 

186 

###### SERVICE AND SUPPORT 



Fig. 16.7: Sync-prompt 

9. After reading the update data, the "DISCARD" and "APPLY" buttons appear. To apply, click on "APPLY". 

10. Depending on the change, the system may reboot. After completion, "Everything up-to-Date" appears in the view. 



Fig. 16.8: Everything up-to-date 

The license affiliation of your features and apps are now detached from the old Control and are available for linking in Franka World. 

11. Now replace the old Control with the new one. To do this, follow the steps described in Section 16.2.1 "Replacing the Control". 

12. Switch on the new Control and open the Desk interface via the URL <u>https://franka.robot.de</u> after starting the system. 

13. Switch to the "Settings/Franka World" view and perform the registration by clicking the "REGISTER" button. Once registration is complete, you can configure your Control in Franka World. 

R02210/1.4/EN 

Franka Robotics GmbH © 

187 

###### SERVICE AND SUPPORT 



Fig. 16.9: Register Control 

14. Open the URL: https://franka.world in the browser and log in. 

15. switch to the MANAGE view and check whether the new Control is displayed. 

16. Select the new Control and open the view by clicking on it. 

17. You will now see the data of the new Control and all the features available in your account. 

18. According to the screenshot or your NOTICEs of the old Control, fill in all information fields and select the features by setting the respective checkmark. 

19. Click on the "SYNCHRONIZED" button to apply the data. 

20. Now switch to the Desk view of the robot in the browser by entering the URL https://franka.robot.de and call up the "Settings/Franka World" view there. 

21. The changes that you have activated in Franka World are now displayed. Click on "DOWNLOAD". 

22. After all data has been downloaded, you can accept the transfer by clicking on "APPLY". The Control now installs all changes and carries out a restart if necessary. 

23. To restore your Control to the status of the old Control, restore the system from the backup data of the old Control. Proceed as described in chapter 14.5 "BACKUP”. 

For the situation that the Control can no longer be started and thus synchronization with Franka World is no longer possible, the licenses of the old Control must be detached from the defective Control by the support of Franka Robotics GmbH. 

To do this, send an e-mail with the following information to Support at: support@franka.de: 

- Account name (Franka World) 

- Account-number (Franka World) 

- Serial number of the defective Control 

R02210/1.4/EN 

Franka Robotics GmbH © 

188 

###### SERVICE AND SUPPORT 

- serial number of the new Control (optional) 

- Type of Platform (FP3/FR3) 

After the licenses have been released by Support, they will be available again in Franka World for linking to a new Control. 

Now connect the new Control to the arm and then switch it on. To transfer the features and apps, proceed as described in steps 13 to 22. If you still have an update of the old Control, you can import the data into the new Control according to the procedure described in Chapter 14.4 “Updates”. 

###### **Mechanical exchange of the Control** 

To replace the Control mechanically, proceed according to the following steps: 

- ✓ Perform a backup, if the defective Control still allows it. 

- ✓ Shut down the robot. 

- ✓ Switch off the Control at the main switch 

- ✓ Disconnect the Control from the mains supply 

- ✓ Disconnect the plug connection C1 (connection cable to the robot) as well as the network connection C2 at the Control. 

- ✓ Replace the defective Control with the replacement Control. Observe the required environmental conditions for the Control (see Chapter 10 "Assembly & Installation"). 

- ✓ Connect the robot's connection cable to the C1 plug connection on the Control 

- ✓ Establish the network connection C2 

- ✓ Connect the Control to the mains supply 

- ✓ Connect your operating device to connector X5 on the robot base using an Ethernet cable 

- ✓ Switch on the Control with the main switch 

R02210/1.4/EN 

Franka Robotics GmbH © 

189 

###### APPENDIX 

## **17 APPENDIX** 

#### **17.1 Stopping Times and Distances** 

The following diagram shows the stopping times and stopping distances of axes 1 to 4 according to the requirement from EN ISO 10218-1. 

The following table illustrates the joint positions for the different extension states of the Franka Research 3. 



Fig. 17.1: Illustration of extension states 

R02210/1.4/EN 

Franka Robotics GmbH © 

190 

APPENDIX 

#### **17.2 Stop Category 1** 

The following table summarizes the maximum values of axes 1-4 for stop category 1. 

|Joint|max. stopping distance<br>[rad]|max. stopping time [s]|
|---|---|---|
|1|0,803|0,735|
|2|0,798|0,682|
|3|0,684|0,534|
|4|0,455|0,418|



##### **17.2.1 Joint 1** 



Fig. 17.2: Distance; Stopp Cat 1; Joint 1, 33% 



Fig. 17.3: Time; Stopp Cat 1; Joint 1 33% 

R02210/1.4/EN 

Franka Robotics GmbH © 

191 

APPENDIX 



Fig. 17.4: Distance; Stopp Cat 1; Joint 1 66% 





Fig. 17.6: Distance; Stopp Cat 1; Joint 1 100% 

R02210/1.4/EN 

Franka Robotics GmbH © 

192 

APPENDIX 



Fig. 17.7: Time; Stopp Cat 1; Joint 1 100% 

##### **17.2.2 Joint 2** 



Fig. 17.8: Distance; Stopp Cat 1; Joint 2 33% 



Fig. 17.9: Time; Stopp Cat 1; Joint 2 33% 

R02210/1.4/EN 

Franka Robotics GmbH © 

193 

APPENDIX 



Fig. 17.10: Distance; Stopp Cat 1; Joint 2 66% 





Fig. 17.12: Distance; Stopp Cat 1; Joint 2 100% 

R02210/1.4/EN 

Franka Robotics GmbH © 

194 

APPENDIX 



Fig. 17.13: Time; Stopp Cat 1; Joint 2 100% 

##### **17.2.3 Joint 3** 



Fig. 17.14: Distance; Stopp Cat 1; Joint 3 33% 



Fig. 17.15: Time; Stopp Cat 1; Joint 3 33% 

R02210/1.4/EN 

Franka Robotics GmbH © 

195 

APPENDIX 



Fig. 17.16: Distance; Stopp Cat 1; Joint 3 66% 





Fig. 17.18: Distance; Stopp Cat 1; Joint 3 100% 

R02210/1.4/EN 

Franka Robotics GmbH © 

196 

APPENDIX 



Fig. 17.19: Time; Stopp Cat 1; Joint 3 100% 

##### **17.2.4 Joint 4** 



Fig. 17.20: Distance; Stopp Cat 1; Joint 4 66% 



Fig. 17.21: Time; Stopp Cat 1; Joint 4 66% 

R02210/1.4/EN 

Franka Robotics GmbH © 

197 

APPENDIX 



Fig. 17.22: Distance; Stopp Cat 1; Joint 4 100% 



Fig. 17.23: Time; Stopp Cat 1; Joint 4 100% 

R02210/1.4/EN 

Franka Robotics GmbH © 

198 

APPENDIX 

#### **17.3 Stop Category 2** 

The following table summarizes the maximum values of axes 1-4 for stop category 2. 

|Joint|max. stopping distance<br>[rad]|max. stopping time [s]|
|---|---|---|
|1|0,806|0,743|
|2|0,805|0,684|
|3|0,695|0,542|
|4|0,455|0,417|



##### **17.3.1 Joint 1** 



Fig. 17.24: Distance; Stopp Cat 2; Joint 1 33% 



Fig. 17.25: Time; Stopp Cat 2; Joint 1 33% 

R02210/1.4/EN 

Franka Robotics GmbH © 

199 

APPENDIX 



Fig. 17.26: Distance; Stopp Cat 2; Joint 1 66% 





Fig. 17.28: Distance; Stopp Cat 2; Joint 1 100% 

R02210/1.4/EN 

Franka Robotics GmbH © 

200 

APPENDIX 



Fig. 17.29: Time; Stopp Cat 2; Joint 1 100% 

##### **17.3.2 Joint 2** 



Fig. 17.30: Distance; Stopp Cat 2; Joint 2 33% 



Fig. 17.31: Time; Stopp Cat 2; Joint 2 33% 

R02210/1.4/EN 

Franka Robotics GmbH © 

201 

APPENDIX 



Fig. 17.32: Distance; Stopp Cat 2; Joint 2 66% 





Fig. 17.34: Distance; Stopp Cat 2; Joint 2 100% 

R02210/1.4/EN 

Franka Robotics GmbH © 

202 

APPENDIX 



Fig. 17.35: Time; Stopp Cat 2; Joint 2 100% 

##### **17.3.3 Joint 3** 





Fig. 17.37: Time; Stopp Cat 2; Joint 3 41% 

R02210/1.4/EN 

Franka Robotics GmbH © 

203 

APPENDIX 



Fig. 17.38: Distance; Stopp Cat 2; Joint 3 66% 





Fig. 17.40: Distance; Stopp Cat 2; Joint 3 100% 

R02210/1.4/EN 

Franka Robotics GmbH © 

204 

APPENDIX 



Fig. 17.41: Time; Stopp Cat 2; Joint 3 100% 

##### **17.3.4 Joint 4** 



Fig. 17.42: Distance; Stopp Cat 2; Joint 4 66% 



Fig. 17.43: Time; Stopp Cat 2; Joint 4 66% 

R02210/1.4/EN 

Franka Robotics GmbH © 

205 

APPENDIX 



Fig. 17.44: Distance; Stopp Cat 2; Joint 4 100% 



Fig. 17.45: Zeit; Stopp Cat 2; Joint 4 100% 

R02210/1.4/EN 

Franka Robotics GmbH © 

206 

###### APPENDIX 

#### **17.4 Response times** 

|**Input**|**Reaction time motor**|**Reaction**<br>**time**<br>**Output grip**|**Safe**|
|---|---|---|---|
|User input|42 ms|48 ms||
|Safety function violation|36 ms|42 ms||
||42 ms|48 ms||
|Central reaction – joint error|42 ms|48 ms||
|Central reaction – subordinate error|10 ms|–||
|Local reaction – joint error|10 ms|–||
|Local reaction – subordinate error|30 ms|36 ms||
|Reaction – Master  Control  error||||



#### **17.5 Safe Position Accuracy** 

If any safety function, that is based on safe position measurement is used, a limited accuracy needs to be taken into account. 

Main contributing factors to be considered include, but are not limited to structural elasticity, mechanical tolerances, assembly tolerances, signal processing, sensor accuracy. 

The effect on the accuracy of these factors is strongly influenced by external forces, payload, dynamic state such as velocity and kinematic configuration (pose). 

Safe position accuracy needs to be considered while parameterizing the safety functions to be used in an application. How much of a margin needs to be used is highly dependent on the aforementioned factors, and therefore needs to be evaluated and validated individually. 

R02210/1.4/EN 

Franka Robotics GmbH © 

207 

GLOSSARY 

## **18 GLOSSARY** 

|**Naming**|**Description**|
|---|---|
|Administrator|An administrator is a person authorized by the responsible person to access the robotic<br>system and utilize the user interface Desk as follows:<br>The administrator sets and changes roles, access rights, and passwords.<br>The administrator sets and changes non-safety-related parameters of the system (e.g., when<br>changing the end effector settings).<br>The administrator programs and teaches the robot system.|
|App|Apps are modular robot programs, each representing a partial step of a robot Task. They<br>can be purchased in the Franka Store and be parametrized in Desk to form entire<br>automation tasks.|
|Arm|The Arm is a tactile robotic arm with seven axes. It is part of Franka Research 3.|
|Axes|The Arm consists of seven consecutive axes. The motion is created in the axes.|
|Cartesian|The Cartesian space is the three-dimensional space where all axes (X, Y, and Z) are<br>perpendicular.|
|Category 0<br>Stop|A Category 0 Stop is the stopping by immediate removal of power to the machine actuators<br>(acc. to EN 60204:2019).|
|Category 1<br>Stop|A Category 1 Stop is a controlled stop with power available to the machine actuators to<br>achieve the stop and then the removal of power when the stop is achieved (acc. to<br>EN 60204:2019).|
|Category 2<br>Stop|A Category 2 Stop is a controlled stop with power available to the machine actuators (acc.<br>to EN 60204:2019).|
|Center of Mass<br>(CoM)|The center of mass is the center of gravity of an object. At this point, the gravitational force<br>comes into effect.|
|Collaboration<br>space|Space accessible by both the operator and the robot during the execution of Tasks.|
|Connecting<br>cable|The connecting cable connects the Arm with the Control.|
|Control|The Control is the main control unit and is part of Franka Research 3. The main control unit<br>allows monitoring and control of the mechanical structure of the robot.|
|Desk|Desk is Franka Robotics web-based, intuitive, and graphical programming and user interface<br>to exchange information and issue commands. It is part of the Franka UI.|
|Emergency<br>Stop Device|The Emergency Stop Device must be connected to the system to stop Franka Research 3<br>and execute a Cat. 1 Stop in case of an emergency. This will cause Franka Research 3 to<br>brake at maximum capacity and the locking bolts to mechanically lock the Arm.<br>The Emergency Stop Device is connected to the X3 connector at the Arm’s base.|



R02210/1.4/EN 

Franka Robotics GmbH © 

208 

###### GLOSSARY 

|**Naming**|**Description**|
|---|---|
|Emergency<br>Unlock Labels|The Emergency Unlock Labels can be found in three different areas on the Arm. They show<br>where to use the Emergency Unlocking Tool to move the robot manually in case of an<br>emergency.|
|Emergency<br>unlocking|Using the Emergency Unlocking Tool to unlock the fail-safe locking system to move the<br>Arm manually is called emergency unlocking.|
|Emergency<br>Unlocking Tool|The Emergency Unlocking Tool is a tool to manually unlock the fail-safe locking system in<br>case of an emergency. Using the tool, the Arm can be moved even when the Arm has no<br>power.|
|EMI Directive<br>2014/30/EU|The EMI Directive (2014/30/EC), referred to as EMI Directive, regulates the<br>electromagnetic compatibility of devices within the European Economic Area, Switzerland,<br>and Turkey.|
|Enabling<br>Button|The Enabling Button is part of the Pilot-Grip and the Pilot. It allows the activation of the<br>Arm’s motion.|
|External<br>Enabling<br>Device|The External Enabling Device is connected to the X4 connector into the Arm‘s base. While<br>half-pressing the External Enabling Device, it is possible to test and run automatic robot<br>programs as long as the device remains half-pressed.|
|Fail-safe<br>locking system|The fail-safe locking system locks all seven axes of the Arm. The Arm maintains its position,<br>even when the power is turned off.|
|FCC rule 47<br>CFR part 15|FCC is the Federal Communications Commission. It is an independent US agency regulating<br>radio, satellite, and cable communications. It regulates issues regarding the electromagnetic<br>compatibility of devices.|
|Franka<br>Robotics<br>GmbH|Franka Robotics GmbH (abbreviated FR) is the company name. We have developed and now<br>produce Franka Research 3.|
|Franka<br>Research 3/<br>Franka<br>Research 3<br>System|The Arm and Control system components compose the Franka Research 3 System, simply<br>called Franka Research 3.|
|Franka Store|Franka Store is Franka Robotics online store, offering apps, bundles, and hardware for easy<br>online ordering. It is part of Franka World:https://franka.world/|
|Franka UI|The Franka UI is the software framework for the web browser accessible user interface for<br>Franka Research 3. It contains "Desk," "Watchman," and the “Settings” interface.|
|Franka World|Franka World is an online platform that interconnects customers, partners, and software<br>and hardware developers, whose activity revolves around Franka Robotics products and<br>services. Franka World provides tools for managing Franka Research 3, access to an online<br>store that features a continuously growing portfolio of software and hardware products,<br>and the possibility of becoming part of an active and passionate community.<br>Visithttps://franka.world/to make use of all the benefits.|
|Guiding /<br>Hand-guiding|Guiding describes moving the robot by haptic interaction, e.g., to teach a new pose.|



R02210/1.4/EN 

Franka Robotics GmbH © 

209 

###### GLOSSARY 

|**Naming**|**Description**|
|---|---|
|Guiding Button|The Guiding Button is located on the right of the Pilot-Grip. The Arm can be moved by<br>pressing the Guiding Button and half-pressing the Enabling Button.|
|Guiding Mode|Guiding modes ease guiding by locking or unlocking different directions or rotations in<br>space, e.g., moving the Arm in three directions. One can switch between guiding modes<br>using the Guiding-Mode Button on the Pilot-Grip or directly from Desk.|
|Hand/<br>Franka Hand|The Hand is an electrical two-finger parallel gripper and is optionally available. The Hand<br>can be used for Franka Production3, Franka Research 3, and mountings according to the<br>ISO flange design. The Hand is an end effector. It is not part of the certified machinery.|
|Integrator|The integrator is responsible for assembling the partly completed machinery into the final<br>machinery by combining the robot with other equipment or another machine, including<br>additional robots to form a machine system.<br>The integrator also conducts appropriate risk assessments to identify residual risks and to<br>eliminate and minimize them according to ISO 12100.<br>The integrator is responsible for the safety of the final application.|
|Interaction|Franka Research 3 is designed to be easily programmed and operated, and to learn and<br>relearn new Tasks quickly. When Franka Research 3 is in “monitored stop” mode or is being<br>guided (teaching mode), Franka Research 3’s base is white to indicate that the Arm is ready<br>for interaction.|
|Interface<br>device|The interface device, a commercially available PC, tablet, or NOTICEbook with a web<br>browser, is connected to the Arm base via an Ethernet cable. The Franka UI can be accessed<br>in a web browser via the interface device.|
|Low Voltage<br>Directive<br>2014/35/EC|The Low Voltage Directive (2014/35/EC), hereinafter referred to as Low Voltage Directive<br>(LVD), regulates the safety of electronically operated devices within the European<br>Economic Area, Switzerland, and Turkey.|
|Machinery<br>Directive<br>(2006/42/EU)|The Machinery Directive (2006/42/EG), hereinafter referred to as Machinery Directive or<br>MD, regulates a standardized level of protection to prevent accidents for machinery and<br>partly completed machinery within the European Economic Area, Switzerland, and Turkey.|
|Maximum<br>workspace|Space that can be swept by the robot's moving parts plus the space that the end effector<br>and the workpiece can sweep.<br>For further information, see section Maximum-and safeguarded space in chapter Correct<br>Installation.|
|Operator|An operator is authorized to access Franka Research 3 and utilize the user interface Desk<br>to use Franka Research 3 within the limits defined by the responsible person and the<br>administrator.The operator is allowed to start, monitor, and stop the intended operation of<br>Franka Research 3. Within Desk, the “operator” role can be assigned to users. Operators<br>only have limited access to Desk.|
|Pilot|The Pilot is the user interface on the Arm for guiding and operating the Arm and/or Desk.<br>It includes the Pilot-Grip and the Pilot-Disc.|
|Pilot-Disc|The Pilot-Disc is part of the Pilot and is used for interacting with the Arm and/or Desk.|
|Pilot-Grip|The Pilot-Grip is part of the Pilot and is used for manual guiding.|
|Pose|A pose is a combination of position and orientation in space.|



R02210/1.4/EN 

Franka Robotics GmbH © 

210 

###### GLOSSARY 

|**Naming**|**Description**|
|---|---|
|Protective<br>Measures|Protective measures achieve risk reduction according to 3.19 of ISO 12100. They are<br>implemented and assessed by the following persons:<br>Designer and/or Integrator (inherently safe design, safeguarding, and complementary<br>protective measures, information for use)<br>Responsible person/Integrator (organization: safe working procedures, supervision, permit-<br>to-work systems; provision and use of additional safeguards; use of personal protective<br>equipment; training)|
|Responsible<br>person|The responsible person is responsible for compliance with occupational health regulations<br>and the operational safety ordinance. The responsible person for Franka Research 3<br>includes but is not limited to the entrepreneur, the director of the institute, the employer,<br>or a delegate responsible for the use of Franka Research 3.|
|RoHS Directive<br>2011/65/EU|The RoHS Directive (2011/65/EU), hereinafter referred to as RoHS Directive, restricts the<br>use of certain dangerous substances in electrical and electronic equipment within the<br>European Economic Area, Switzerland, and Turkey.|
|Safeguarded<br>space|The perimeter safeguarding defines the safeguarded space.<br>For further information, see section Classification of spaces in chapter Correct Installation.|
|Safety rules|A safety rule consists of a parameterized safety function, optional activation conditions, and<br>a reaction to be carried out when the safety function is violated.|
|Safety<br>scenarios|A set of safety rules defined in Watchman covering a specific risk situation, e.g., the "Test &<br>Jog" scenario covering all rules for the Test & Jog mode.|
|Safety set-up|Definition of general safety-relevant settings such as safe input behavior or an end effector<br>collision model.|
|SEEPO|Safety function “Safe End Effector Power Off.” See chapter Safety functionalities for details.|
|Settings<br>interface|The Settings interface is a web browser accessible user interface to set non-safety-related<br>parameters of Franka Research 3, e.g., network settings, user roles, or passwords. It is part<br>of the software framework Franka UI.|
|Single Point of<br>Control (SPoC)|Single Point of Control (SPoC) is a functionality that allows only one user at a time to trigger<br>critical actions, i.e., edit system settings and Tasks or trigger active robot actions like<br>unlocking joints and running tasks.|
|SLD|Safety function “Safely limited distance.” See chapter Safety functionalities for details.|
|SLP-C|Safety function “Safely limited Cartesian Position.” See chapter Safety functionalities for<br>details.|
|SLP-J|Safety function “Safely limited joint angle.” See chapter Safety functionalities for details.|
|SLS-C|Safety function “Safely limited Cartesian speed.” See chapter Safety functionalities for<br>details.|
|SLS-J|Safety function “Safely limited joint speed.” See chapter Safety functionalities for details.|
|SMSS|Safety function “Safely monitored standstill.” See chapter Safety functionalities for details.|
|Stopping<br>Distance|The stopping distance is the distance the Arm covers after a stop demand is received until<br>the Arm comes to a full stop.|



R02210/1.4/EN 

Franka Robotics GmbH © 

211 

###### GLOSSARY 

|**Naming**|**Description**|
|---|---|
|Stopping Time|The stopping time is the time that passes after the stop demand is received, e.g., by the<br>emergency device, until the Arm comes to a full stop.|
|Task|A Task in Desk represents an entire automation routine. A Task consists of one or several<br>Apps.|
|Teaching|Teaching describes the process of parameterizing a Task and the contained Apps by<br>manually guiding the robot or end effector. This includes, among others, the teaching of<br>"poses" by guiding the robot to that poses.|
|Tracking Error|The actual motion of the Arm follows the target motion with a small deviation, a so-called<br>tracking error.|
|Watchman|Watchman is a web browser accessible user interface to set and visually validate safety-<br>related parameters of Franka Research 3, e.g., safety-related monitored speed or safety-<br>related monitored spaces. It is part of the Franka UI.|
|Web browser|A software application running on an interface device, serving as the Franka UI connection.<br>A web browser provides the environment for Desk, Watchman, and the Settings interface.<br>Examples include the following: Chrome, Edge, and Firefox.|



R02210/1.4/EN 

Franka Robotics GmbH © 

212 

###### INDEX 

## **19 INDEX** 

|Additionally Equipment ............................................ 48|
|---|
|Administrator .............................................................. 38|
|Apps .................................................. 98, 145, 146, 166|
|Arm ............................................. 13, 17, 40, 48, 56, 66|
|Manually Moving the Arm ................................... 24|
|Unpacking the Equipment .................................... 57|
|Axes ............................................................................ 126|
|Backup ........................................................................ 169|
|End Effector Configuration ................................ 170|
|Modbus Configuration ........................................ 170|
|Network Setting ................................................... 170|
|Safety Configuration ........................................... 169|
|Saving of the created Tasks ............................... 171|
|Cartesian ...................................................................... 30|
|Cartesian space ........................................................ 126|
|Center of Mass (CoM) ............................. 19, 133, 159|
|Certificates .................................................................. 11|
|Cleaning ..................................................................... 172|
|Collaboration space ................................................. 132|
|Connecting cable ................................................. 57, 76|
|Control ....................................... 14, 18, 39, 48, 56, 67|
|Desk .............................................................. 41, 77, 140|
|Disposal ...................................................... 12, 172, 173|
|Emergency ............................................................ 15, 18|
|Emergency Stop Device ....................................... 15|
|Emergency stop installation................................. 23|
|Emergency unlock label ........................................ 13|
|Emergency Unlocking ........................................... 13|
|Emergency Unlocking Tool .................................. 24|
|EMI Directive 2014/30/EU ................................... 200|
|Enabling Button ................................. 28, 94, 152, 159|
|End effector ................................ 46, 80, 87, 144, 159|
|External Enabling Device ...................... 15, 48, 73, 94|
|factory reset ................................................................ 38|
|Factory Reset............................................................. 176|
|Fail-safe Locking System ........................ 24, 133, 159|
|FCC rule 47 CFR part 15 ........................................ 200|
|Fieldbus ............................................................ 129, 130|



|Franka .................................................................... 8, 200|
|---|
|Franka Control Interface ..................... 110, 155, 156|
|FCI........................................................ 110, 155, 156|
|Franka Store .............................................................. 200|
|Franka UI ................................................. 8, 21, 27, 139|
|Franka World ......................................... 144, 166, 176|
|Managing Apps and Updates ............................ 166|
|Updates.................................................................. 168|
|Gelenk-Referenz-Position des Armes .................... 84|
|Glossary ..................................................................... 199|
|Guiding|
|Guiding / hand-guiding ......................................... 28|
|Guiding Button ..................................... 43, 130, 159|
|Guiding Mode ....................................................... 149|
|Guiding-Mode Button ........................................... 43|
|Hand ................................................................41, 46, 49|
|Handling ..........................................................54, 55, 87|
|Idle ................................................................ 27, 28, 130|
|Installation ............................................... 18, 47, 49, 56|
|Preparing the Installation Site ............................. 65|
|Wiring and Electrical Installation ........................ 71|
|Integrator .............................................................. 20, 37|
|Intended Use............................................................... 17|
|Interaction ............................................................ 41, 92|
|Interface Device ............................................39, 49, 96|
|Labeling on the Equipment ...................................... 13|
|Functional earth label ........................................... 14|
|Grasping position label ......................................... 14|
|Log Download ........................................................... 176|
|Login ........................................................................... 139|
|Low Voltage Directive 2014/35/EC .................... 201|
|Machinery Directive 2006/42/EC ......................... 17|
|Maintenance ............................................................. 172|
|Maximum space ..................................... 54, 61, 81, 90|
|Misuse ................................................................... 17, 20|
|Operating Modes ..................................................... 130|
|Operator .................................................. 26, 27, 30, 37|
|Pilot ........................................................................ 40, 41|



R02210/1.4/EN 

Franka Robotics GmbH © 

213 

|INDEX|
|---|



|Pilot-Disc ................................................................. 41|
|---|
|Pilot-Grip ................................................................. 41|
|Pilot-Mode .............................................................. 41|
|Ports.............................................................................. 72|
|C2 .............................................................................. 74|
|X1 .............................................................................. 44|
|X2 .............................................................................. 72|
|X3 .............................................................................. 73|
|X4 .............................................................................. 73|
|X5 .............................................................................. 74|
|X6 .............................................................................. 74|
|Pose ............................................................................ 126|
|Practical Tips for Usage and Positioning ...... 82, 151|
|Protective Measures ................................................. 18|
|Responsible person ......................................... 8, 36, 37|
|Restarting................................................................... 110|
|RoHS Directive 2011/65/EU .................................. 11|
|Roles and Personae|
|Administrator .......................................................... 38|
|Responsible Person ............................................... 36|
|Roles and Personae ................................................... 36|
|Roles and Personae|
|Responsible person ............................................... 36|
|Roles and Personae|
|Integrator ................................................................. 37|
|Roles and Personae|
|Operator .................................................................. 37|
|Roles and Personae|
|Administrator .......................................................... 37|
|Roles and Personae|
|Safety operator ...................................................... 38|
|Roles and Personae<br>Assigning user roles ............................................... 38|
|Safety............................................................................ 16|
|Installation of Safety Peripherals ........................ 23|
|Safe inputs ............................................................... 29|
|Safe outputs ............................................................ 31|
|Safeguarded space................................................. 61|
|Safety Concept ....................................................... 26|
|Safety Functionalities............................................ 29|
|Safety rules ............................................................. 26|



|Safety Log .................................................................. 177|
|---|
|SEEPO .......................................................................... 30|
|Self-test ........................................................................ 93|
|Service and Support .......................................159, 174|
|Hardware Exchange ............................................ 177|
|Settings-Schnittstelle .............................................. 143|
|Single Point of Control (SpoC) ............................... 127|
|Single Point of Control (SPoC) ....................... 21, 127|
|Site of installation ............................................... 62, 64|
|SLD................................................................................ 31|
|SLP-J ............................................................................. 31|
|SLS-C ............................................................................ 30|
|SLS-J ............................................................................. 31|
|SMSS ............................................................................ 30|
|Software-Einrichtung ................................................ 96|
|Stopping distance....................................................... 24|
|Stopping functions ..................................................... 31|
|Category 0 stop...................................................... 31|
|Category 1 stop...................................................... 31|
|Category 2 stop...................................................... 31|
|Stopping time .............................................................. 24|
|Stopping time and distances .........................181, 198|
|Switching Off ......................................... 110, 164, 165|
|Switching On............................................................... 90|
|Task ................................................... 94, 100, 126, 146|
|Teaching................ 91, 131, 133, 145, 146, 154, 159|
|Teaching a Task ..................... 91, 131, 145, 146, 154|
|Technical Specifications ........................................... 50|
|Tracking error ........................................................... 153|
|Transport ................................................. 54, 56, 87, 90|
|Re-packing the Arm ............................................... 87|
|Unpacking ............................................................... 58|
|Troubleshooting ....................................................... 159|
|User interface ...................................... 37, 41, 96, 102|
|Watchman ................................................. 26, 112, 143|
|Creating and editing rules .................................. 119|
|Creation of spheres for modelling an End Effector<br>envelope ............................................................ 117|
|Editing of the Safety Configuration ................. 114|
|End effector configuration ................................. 116|
|General Safety Settings ...................................... 116|



R02210/1.4/EN 

Franka Robotics GmbH © 

214 

###### INDEX 

|Safe Input Configuration .................................... 116|Structure of a rule ................................................ 119|
|---|---|
|Safety configuration ............................................ 112|Validate .................................................................. 122|
|Safety Setup .......................................................... 116||



R02210/1.4/EN 

Franka Robotics GmbH © 

215 

TABLE OF FIGURES 

## **20 TABLE OF FIGURES** 

|Fig. 3.1: Type label ..................................................... 13|
|---|
|Fig. 3.2: Emergency unlock label............................. 13|
|Fig. 3.3: Hot Surface label ........................................ 14|
|Fig. 3.4: Functional earth label ................................ 14|
|Fig. 3.5: Lifting position label ................................... 14|
|Fig. 3.6: Type label control ....................................... 14|
|Fig. 3.7: Type label external device ........................ 15|
|Fig. 3.8: Type label emergency stop device .......... 15|
|Fig. 4.1: Connection Emergency Stop Device ...... 23|
|Fig. 4.2: Emergency unlock ...................................... 25|
|Fig. 4.3: Pushing away manually ............................. 26|
|Fig. 4.4: States during normal operation ............... 28|
|Fig. 6.1: Equipment overview .................................. 39|
|Fig. 6.2: Overview Arm ............................................. 40|
|Fig 6.3: Pilot ................................................................ 41|
|Fig. 6.4: switching status Enabling Button ............ 42|
|Fig. 6.5: Enabling Button .......................................... 42|
|Fig. 6.6: Guiding Mode Button ................................ 43|
|Fig. 6.7: Guiding Mode Button ................................ 43|
|Fig. 6.8: Guiding Button ............................................ 43|
|Fig. 6.9: Guiding Button ............................................ 44|
|Fig. 6.10: Connection ports at robot base ............ 44|
|Fig. 6.11: End effector flange .................................. 46|
|Fig. 6.12: Dimensions and connection ports of|
|control .......................................................................... 46|
|Fig. 6:.13 ...................................................................... 47|
|Fig. 7.1: scope of delivery Arm ................................ 48|
|Fig. 7.2: scope of delivery Control .......................... 48|
|Fig. 7.3: Scope of delivery devices ......................... 48|
|Fig. 7.4: Scope of delivery Connecting cable ....... 49|
|Fig. 9.1: Lifting positions........................................... 55|
|Fig. 10.1: Overview of interfaces ........................... 56|
|Fig. 10.2: Packing ....................................................... 57|
|Fig. 10.3: Unpack main carton ................................. 58|
|Fig. 10.4: Removal of individual cartons ............... 58|
|Fig. 10.5: Inner cartons ............................................. 58|
|Fig. 10.6: Open box from Arm ................................. 59|
|Fig. 10.7: Unpack arm ............................................... 59|
|Fig. 10.8: Lift out arm ................................................ 59|



|Fig. 10.9: Open box of control ................................ 60|
|---|
|Fig. 10.10: Removal packaging ................................ 60|
|Fig. 10.11: Lift out  control ...................................... 60|
|Fig. 10.12: Classifcation of spaces.......................... 61|
|Fig. 10.13: Preparing the baseplate ........................ 65|
|Fig. 10.14: Drilling template .................................... 66|
|Fig. 10.15: Mounting of the arm ............................. 69|
|Fig. 10.16: Overview connection diagram ............ 72|
|Fig. 10.17: X2 interface ............................................ 73|
|Fig. 10.18: X3 - Safe Inputs...................................... 73|
|Fig. 10.19: X6 interface ............................................ 74|
|Fig. 10.20: Connection the functional earth......... 75|
|Fig. 10.21: Connection of connecting cable  the arm<br>....................................................................................... 76|
|Fig. 10.22: connection of connecting cable to the<br>control .......................................................................... 77|
|Fig. 10.23: Connection of external Enabeling Device<br>....................................................................................... 77|
|Fig. 10.24: Connection of operating device ......... 78|
|Fig. 10.25: Connection of the protective device|
|(here emergency stop command device)............... 80|
|Fig. 10.26: Measuring points ESD measurement 83|
|Fig. 10.27: Design of the workspace...................... 84|
|Fig. 10.28: Joint reference position of the arm ... 84|
|Fig. 10.29: Distance to arm bumping the head .... 85|
|Fig. 10.30: Distance to arm bumping ..................... 85|
|Fig. 10.31: Distance to arm Squeezing the hand . 85|
|Fig. 10.32: Protective equipment do not wear|
|jewelry .......................................................................... 86|
|Fig. 10.33: Lifting the arm ........................................ 88|
|Fig. 10.34: Packing the arm...................................... 89|
|Fig. 10.35: Closing the box....................................... 89|
|Fig. 11.1: Switching on Control ............................... 90|
|Fig. 11.2: Blue status lights on Arm ........................ 91|
|Fig. 11.3: Language Selection Initial Configuration<br>....................................................................................... 97|
|Fig. 11.4: Network Initial Configuration ................ 97|
|Fig. 11.5: Franka World registration ...................... 98|
|Fig. 11.6: Creating Administrator............................ 99|
|Fig. 11.7: End effector settings ............................... 99|



R02210/1.4/EN 

Franka Robotics GmbH © 

216 

|TABLE OF FIGURES|
|---|
|Fig. 11.8 Network connection for FCI Usage ..... 101|
|Fig. 11.9Network settings..................................... 102|
|Fig. 11.10Ubuntu – Ethernet configuration...... 103|
|Fig. 11.11 Ubuntu –setting a static IP................ 103|
|Fig. 11.12 TUI-Interface ......................................... 106|
|Fig. 12.1: Watchman ............................................... 113|
|Fig. 12.2: Validated rules ........................................ 114|
|Fig. 12.3: Switch to “Draft” mode ......................... 114|
|Fig. 12.4: Draft Mode .............................................. 115|
|Fig. 12.5: Validation markers ................................. 115|
|Fig. 12.7: End Effector Configuration .................. 122|
|Fig. 12.8: Configuration of spheres ...................... 123|
|Fig. 12.9: Example of spheres for Franka Hand . 124|
|Fig. 12.10 Example of sphere configuration Franka|
|hand with staff .......................................................... 125|
|Fig. 12.11: Editing rules .......................................... 125|
|Fig. 12.12: structur of a rule .................................. 125|
|Fig. 12.13: Configuration of ”Activation Space” 127|
|Fig. 12.14: monitoring ............................................. 127|
|Fig. 12.15: Creating cuboid area ........................... 127|
|Fig. 12.16: Setting of speed ................................... 128|
|Fig. 12.17: Validation structure ............................. 128|
|Fig. 12.18: Validating ............................................... 129|
|Fig. 12.19: Validating of rules ................................ 129|
|Fig. 12.20: Validating Watchman.......................... 130|
|Fig. 12.21 Safety Report ......................................... 131|
|Fig. 13.1: Control request....................................... 134|
|Fig. 13.2: User management waiting for approval<br>..................................................................................... 134|
|Fig. 13.3: User request ............................................ 134|
|Fig. 13.4: Enforce control ....................................... 135|
|Fig. 13.5: Overview operating modes .................. 136|
|Fig. 13.6: procedure................................................. 137|
|Fig. 13.7: Assist operation ...................................... 138|
|Fig. 13.8: Area assignment ..................................... 141|
|Fig. 13.9: Work operation ...................................... 141|
|Fig. 13.10: Indication of Assist Mode .................. 143|
|Fig. 13.11: Conditions for motion enabling in Assist|
|Mode .......................................................................... 143|
|Fig. 13.12: Login Franka User interface .............. 145|
|Fig. 13.13: Download User Manual ...................... 146|
|Fig. 13.14: Desk........................................................ 146|



|Fig. 13.15: Desk Sidebar ......................................... 147|
|---|
|Fig. 13.16: Watchman ............................................. 149|
|Fig. 13.17: Menu Settings ...................................... 149|
|Fig. 13.18: App parameterization ......................... 153|
|Fig. 13.19: App interface ........................................ 154|
|Fig. 13.20: Pose fine adjustment .......................... 155|
|Fig. 13.21: Overview of switching between Hand-<br>Guiding-Modes ......................................................... 156|
|Fig. 13.22: Illustration of Hand Guiding .............. 156|
|Fig. 13.23: Settings, if “User mode” is selected . 156|
|Fig. 13.24: Hand guide approval ........................... 158|
|Fig. 13.25: Test & Jog.............................................. 160|
|Fig. 13.26: Message “A joint limit has been violated”<br>..................................................................................... 166|
|Fig. 13.27: Message with display of the faulty joint<br>..................................................................................... 166|
|Fig. 13.28: Confirmation joint is back in the limit<br>..................................................................................... 167|
|Fig. 13.29: Message “Joint position error detected”<br>..................................................................................... 167|
|Fig. 13.30:  Message with display of failed joints<br>..................................................................................... 168|
|Fig. 13.31: Joint recovery locked .......................... 168|
|Fig. 13.32: Joint recovery ready for movement 169|
|Fig. 13.33: Conformation position reached ........ 169|
|Fig. 13.34: Confirmed Joint recovery .................. 170|
|Fig. 13.35: Message Button not held ................... 170|
|Fig. 13.36: Message if reference position not|
|reached....................................................................... 171|
|Fig. 13.37: Confirm the complete recovery ........ 171|
|Fig. 14.1: Managing Apps and Features via Franka<br>World .......................................................................... 174|
|Fig. 14.2: Network connection of control ........... 175|
|Fig. 14.3: Managing of Updates via Franka World<br>..................................................................................... 176|
|Fig. 14.4: Network Settings ................................... 178|
|Fig. 14.5: Save Tasks ............................................... 179|
|Fig. 16.1: Rescue System ........................................ 183|
|Fig. 16.2: Network ................................................... 183|
|Fig. 16.3: Log Download and Factory Reset....... 184|
|Fig. 16.4: Franka World .......................................... 185|
|Fig. 16.5: Safety Log ................................................ 185|
|Fig. 16.6: Device detail view .................................. 186|
|Fig. 16.7: Sync-prompt............................................ 187|



R02210/1.4/EN 

Franka Robotics GmbH © 

217 

###### TABLE OF FIGURES 

Fig. 16.8: Everything up-to-date ........................... 187 Fig. 16.9: Register Control ..................................... 188 Fig. 17.1: Illustration of extension states ............ 190 Fig. 17.2: Distance; Stopp Cat 1; Joint 1, 33% ... 191 Fig. 17.3: Time; Stopp Cat 1; Joint 1 33%........... 191 Fig. 17.4: Distance; Stopp Cat 1; Joint 1 66%.... 192 Fig. 17.5: Time; Stopp Cat 1; Joint 1 66%........... 192 Fig. 17.6: Distance; Stopp Cat 1; Joint 1 100% . 192 Fig. 17.7: Time; Stopp Cat 1; Joint 1 100% ........ 193 Fig. 17.8: Distance; Stopp Cat 1; Joint 2 33%.... 193 Fig. 17.9: Time; Stopp Cat 1; Joint 2 33%........... 193 Fig. 17.10: Distance; Stopp Cat 1; Joint 2 66% . 194 Fig. 17.11: Time; Stopp Cat 1; Joint 2 66% ........ 194 Fig. 17.12: Distance; Stopp Cat 1; Joint 2 100% ..................................................................................... 194 Fig. 17.13: Time; Stopp Cat 1; Joint 2 100% ...... 195 Fig. 17.14: Distance; Stopp Cat 1; Joint 3 33% . 195 Fig. 17.15: Time; Stopp Cat 1; Joint 3 33% ........ 195 Fig. 17.16: Distance; Stopp Cat 1; Joint 3 66% . 196 Fig. 17.17: Time; Stopp Cat 1; Joint 3 66% ........ 196 Fig. 17.18: Distance; Stopp Cat 1; Joint 3 100% ..................................................................................... 196 

Fig. 17.31: Time; Stopp Cat 2; Joint 2 33% ........ 201 Fig. 17.32: Distance; Stopp Cat 2; Joint 2 66% . 202 Fig. 17.33: Time; Stopp Cat 2; Joint 2 66% ........ 202 Fig. 17.34: Distance; Stopp Cat 2; Joint 2 100% ..................................................................................... 202 Fig. 17.35: Time; Stopp Cat 2; Joint 2 100% ...... 203 Fig. 17.36: Distance; Stopp Cat 2; Joint 3 41% . 203 Fig. 17.37: Time; Stopp Cat 2; Joint 3 41% ........ 203 Fig. 17.38: Distance; Stopp Cat 2; Joint 3 66% . 204 Fig. 17.39: Time; Stopp Cat 2; Joint 3 66% ........ 204 Fig. 17.40: Distance; Stopp Cat 2; Joint 3 100% ..................................................................................... 204 Fig. 17.41: Time; Stopp Cat 2; Joint 3 100% ...... 205 Fig. 17.42: Distance; Stopp Cat 2; Joint 4 66% . 205 Fig. 17.43: Time; Stopp Cat 2; Joint 4 66% ........ 205 Fig. 17.44: Distance; Stopp Cat 2; Joint 4 100% ..................................................................................... 206 Fig. 17.45: Zeit; Stopp Cat 2; Joint 4 100% ........ 206 

Fig. 17.19: Time; Stopp Cat 1; Joint 3 100% ...... 197 Fig. 17.20: Distance; Stopp Cat 1; Joint 4 66% . 197 Fig. 17.21: Time; Stopp Cat 1; Joint 4 66% ........ 197 Fig. 17.22: Distance; Stopp Cat 1; Joint 4 100% ..................................................................................... 198 Fig. 17.23: Time; Stopp Cat 1; Joint 4 100% ...... 198 Fig. 17.24: Distance; Stopp Cat 2; Joint 1 33% . 199 Fig. 17.25: Time; Stopp Cat 2; Joint 1 33% ........ 199 Fig. 17.26: Distance; Stopp Cat 2; Joint 1 66% . 200 Fig. 17.27: Time; Stopp Cat 2; Joint 1 66% ........ 200 Fig. 17.28: Distance; Stopp Cat 2; Joint 1 100% ..................................................................................... 200 Fig. 17.29: Time; Stopp Cat 2; Joint 1 100% ...... 201 Fig. 17.30: Distance; Stopp Cat 2; Joint 2 33% . 201 

R02210/1.4/EN 

Franka Robotics GmbH © 

218 

**Error! Use the Home tab to apply Überschrift 1;PM Überschrift 1 to the text that you want to appear here.** 

Franka Robotics GmbH Frei-Otto-Strasse 20 80797 Munich Germany 

R02210/1.4/EN 

Franka Robotics GmbH © 

219 

