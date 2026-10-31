> **[PDF を開く](<Hardware Manual Franka Research 3_Arm v2.1_R02210_1.3_EN.pdf>)**
>
> PDF から自動変換した本文です。図は含まず、表は崩れている場合があります。安全や仕様の確認には PDF を使ってください。

Hardware Manual 

FRANKA RESEARCH 3 

© Copyright 2026 Franka Robotics GmbH Koppstraße 20 81379 Munich Germany 

The information in this document, including any extracts, may only be reproduced or shared with third parties with the explicit authorization of Franka Robotics GmbH. 

The content of this document has been carefully checked against compliance with the hardware and software described. However, discrepancies cannot entirely be ruled out, which is why we assume no liability for complete compliance. 

In the interest of our customers, we reserve the right to undertake improvements and corrections to hardware, software, and documentation at any point in time without notice. 

We are always grateful for your feedback at documentation@franka.de. 

English documentation is the ORIGINAL DOCUMENTATION. Other languages are translations of the original document. 

Complementary documents to this hardware manual are: 

- Datasheet Franka Research 3 with Arm v2.1 (Document number: R02212) 

- ESD Measurements FR3 Arm v2 (Document number: R02015) 

- Quick Guide for Installation FR3 (Document number: R02040) 

- Operating Manual Franka Research 3 (Document number: R02216) 

Document name:               Hardware Manual Franka Research 3 

Document number:           R02210 

Hardware Version:            Franka Research 3 with Arm v2.1 

Article number:                  Arm (309969) 

Change Log: 

|**Content Iteration**|**Release Date**|**Release notes / Changes**|
|---|---|---|
|1.0|November 2025|Franka Research 3 with Arm v2.1 featuring updated weight, revised labelling, and refined<br>stopping time and distance specifications.|
|1.1|November 2025|Updated information in chapter 4.7 ‘’Installation of safety peripherals’’|
|1.2|December 2025|Corrected LED color reference table in chapter 9.5|
|1.3|June 2026|Converted notices into safety instructions, removed SPL-C warnings in the "Monitoring Functions"<br>chapter, corrected references, and made a minor update to the Robot LED Indicator System.|





Get your manual and additional supporting material in English and other languages at www.franka.de/documents. 

R02210/1.3/EN 

Franka Robotics GmbH © 

2 

# **TABLE OF CONTENTS** 

|1<br>ABO|UT HARDWARE MANUAL ........................................................................................................................................... 6|
|---|---|
|1.1|Software and hardware version.................................................................................................................................. 6|
|1.2 Ap|plicable document.............................................................................................................................................................. 6|
|1.3 Be|fore you begin ..................................................................................................................................................................... 6|
|2<br>RIG|HTS OF USE AND PROPERTY RIGHTS ....................................................................................................................... 7|
|2.1|General ............................................................................................................................................................................ 7|
|2.2|Identification................................................................................................................................................................... 7|
|3<br>DEC|LARATION OF INCORPORATION AND CERTIFICATES ........................................................................................ 8|
|3.1|Declaration of Incorporation ....................................................................................................................................... 8|
|3.2|Further Statements ..................................................................................................................................................... 10|
|3.2.1|RoHS / REACH / WEEE / Battery Directive.......................................................................................................... 10|
|3.2.2|China RoHS 2 ............................................................................................................................................................... 11|
|3.3|Labeling on the equipment ........................................................................................................................................ 12|
|3.3.1|Arm ................................................................................................................................................................................. 12|
|3.3.2|External Enabling Device ........................................................................................................................................... 13|
|3.3.3|Emergency Stop Device ............................................................................................................................................. 14|
|4<br>SAF|ETY ..................................................................................................................................................................................... 14|
|4.1|Safety instructions and general instructions .......................................................................................................... 14|
|4.2|Notice of Liability ........................................................................................................................................................ 15|
|4.3|Intended use ................................................................................................................................................................. 15|
|4.4|Misuse ............................................................................................................................................................................ 15|
|4.5|General possible dangers and safety measures when working with robots ................................................... 16|
|4.6|Application related to possible dangers and safety measures ........................................................................... 19|
|4.7|Installation of safety peripherals .............................................................................................................................. 21|
|4.8|Fail-safe locking system ............................................................................................................................................. 22|
|4.9|Manually Moving the Arm ......................................................................................................................................... 23|
|4.10|Safety Functions .......................................................................................................................................................... 25|
|4.11|Additional information for planning and initial installation of a robot system ................................................ 29|
|5<br>EQU|IPMENT OVERVIEW .................................................................................................................................................... 33|
|5.1|The Arm ......................................................................................................................................................................... 34|
|5.2|Control ........................................................................................................................................................................... 42|
|6<br>SCO|PE OF DELIVERY AND ADDITIONAL EQUIPMENT ............................................................................................. 43|
|6.1|Included in the box ...................................................................................................................................................... 43|
|6.2|Not included in the box .............................................................................................................................................. 45|
|6.3|Available spare parts and accessories ..................................................................................................................... 45|
|7<br>MO|UNTING AND INSTALLATION .................................................................................................................................... 46|



R02210/1.3/EN 

Franka Robotics GmbH © 

3 

|7.1|Unpacking the equipment .......................................................................................................................................... 47|
|---|---|
|7.2|Correct installation site .............................................................................................................................................. 52|
|7.2.1|Maximum-and safeguarded space ........................................................................................................................... 52|
|7.2.2|Ambient conditions: Arm ........................................................................................................................................... 53|
|7.2.3|Ambient conditions: Control ..................................................................................................................................... 55|
|7.3|Preparing the Installation site ................................................................................................................................... 56|
|7.3.1|Arm ................................................................................................................................................................................. 56|
|7.3.2|Control ........................................................................................................................................................................... 58|
|7.4|Mounting the Arm ....................................................................................................................................................... 59|
|7.5|Positioning the Control .............................................................................................................................................. 61|
|7.6|Wiring and Electrical installation .............................................................................................................................. 62|
|7.7|Connecting to the robot interface ........................................................................................................................... 63|
|7.7.1|Connection diagram .................................................................................................................................................... 63|
|7.7.2|Interfaces....................................................................................................................................................................... 63|
|7.7.3|Wiring ............................................................................................................................................................................ 66|
|7.8|Mounting End Effectors ............................................................................................................................................. 71|
|7.9|Practical Tips for Usage and Positioning of Franka Research 3 ......................................................................... 73|
|7.9.1|Energy consumption ................................................................................................................................................... 73|
|7.9.2|ESD limits ...................................................................................................................................................................... 73|
|7.9.3|Design of the workspace ........................................................................................................................................... 75|
|7.9.4|Personal safety and ergonomics ............................................................................................................................... 76|
|8<br>US|AGE ...................................................................................................................................................................................... 78|
|8.1|Switching On ................................................................................................................................................................ 78|
|8.2|Safety Relevant Tests of Franka Research 3.......................................................................................................... 80|
|8.2.1|Self-test of the robotic system ................................................................................................................................. 80|
|8.2.2|Regular testing of safety functions .......................................................................................................................... 81|
|8.2.3|Testing the emergency stop ...................................................................................................................................... 81|
|8.3|Switching off and restarting ...................................................................................................................................... 83|
|9<br>RO|BOT LED INDICATOR SYSTEM .................................................................................................................................... 84|
|9.1|Overview of the status indicators ............................................................................................................................ 84|
|9.2|LED Activation Behavior ............................................................................................................................................ 85|
|9.3|Flashing Patterns ......................................................................................................................................................... 85|
|9.4|LED Priority Logic ........................................................................................................................................................ 86|
|9.5|LED Color Reference Table ....................................................................................................................................... 86|
|10|MAINTENANCE AND DISPOSAL ................................................................................................................................ 88|
|10.1|Maintenance ................................................................................................................................................................. 88|
|10.2|Cleaning ......................................................................................................................................................................... 89|
|10.3|Disposal ......................................................................................................................................................................... 90|



R02210/1.3/EN 

Franka Robotics GmbH © 

4 

|10.4|Mechanical exchange of Control .............................................................................................................................. 90|
|---|---|
|11<br>|TROUBLESHOOTING .................................................................................................................................................... 90|
|12<br>|TECHNICAL DATA .......................................................................................................................................................... 91|
|12.1|Technical specifications.............................................................................................................................................. 91|
|12.1.1|Ambient conditions for delivery and transport ................................................................................................ 92|
|13<br>|TRANSPORTATION AND HANDLING ...................................................................................................................... 92|
|13.1|Procedure ...................................................................................................................................................................... 92|
|13.1.1|Step 1. Transportation pose of the Arm ............................................................................................................ 93|
|13.1.2|Step 2. Handling and lifting .................................................................................................................................. 93|
|13.1.3|Step 3. Re-packing the Arm .................................................................................................................................. 95|
|14<br>|APPENDIX ........................................................................................................................................................................ 97|
|14.1|Stopping Times and Distances .................................................................................................................................. 97|
|14.2|Stop Category 1 ........................................................................................................................................................... 98|
|14.2.1|Joint 1 .....................................................................................................................................................................100|
|14.2.2|Joint 2 .....................................................................................................................................................................101|
|14.2.3|Joint 3 .....................................................................................................................................................................102|
|14.2.4|Joint 4 .....................................................................................................................................................................103|
|14.3|Stop Category 2 .........................................................................................................................................................103|
|14.3.1|Joint 1 .....................................................................................................................................................................104|
|14.3.2|Joint 2 .....................................................................................................................................................................105|
|14.3.1|Joint 3 .....................................................................................................................................................................106|
|14.3.2|Time Joint 4 ...........................................................................................................................................................107|
|14.4|Response times ..........................................................................................................................................................108|
|14.5|Safe Position Accuracy .............................................................................................................................................108|
|15<br>|GLOSSARY ..................................................................................................................................................................... 109|
|16<br>I|NDEX ............................................................................................................................................................................. 114|
|17<br>|TABLE OF FIGURES ..................................................................................................................................................... 116|



R02210/1.3/EN 

Franka Robotics GmbH © 

5 

**ABOUT HARDWARE MANUAL** 

# **1 ABOUT HARDWARE MANUAL** 

This hardware manual provides essential information to ensure the safe and correct use of the Franka robot. It includes detailed guidance on identifying the robot’s components, performing general maintenance, understanding built-in safety functions, and following step-by-step instructions for initial setup and usage. 

All personnel must read and fully understand this manual before beginning any work with the robot. Safe operation requires strict adherence to all safety guidelines and handling instructions provided in this manual. 

## **1.1 Software and hardware version** 

This hardware manual applies to Franka Research 3 with Arm version v2.1 This Arm version is compatible with system image version 5.8 and above. 

## **1.2 Applicable document** 

In addition to this manual, the following document also applies: 

- **Operating Manual:** Franka Research 3 with system image version 5.8 

- **Document number:** R02216 

#### **_NOTICE_** 

Hardware Manual Arm v2.1 is released with system image 5.8. Starting with system image version 5.9, Arm v2.1 is also supported. Full functionality without degradation is available from system image version 5.9.1 onward. 

## **1.3 Before you begin** 

### **1.3.1 Intended audience and training requirements** 

This manual is intended for qualified technical personnel responsible for installation, operation, and maintenance of the Franka Research 3 system. Users must: 

- Be trained in handling industrial robots and familiar with applicable safety regulations (e.g. EN ISO 102182). 

- Understand basic mechanical and electrical safety principles. 

- Be authorized by their employer to perform the described tasks. 

Untrained or unauthorized people are not permitted to install, operate, or service this product. 

R02210/1.3/EN 

Franka Robotics GmbH © 

6 

**RIGHTS** OF USE AND PROPERTY RIGHTS 

# **2 RIGHTS OF USE AND PROPERTY RIGHTS** 

## **2.1 General** 

#### **Protected trademarks** 

This manual refers to protected trademarks not explicitly designated in the continuing text. The absence of such indication may not imply that the corresponding product name is free of third-party rights. The following trademarks are protected trademarks: 

Franka and Franka Robotics are registered trademarks. 

Microsoft is a registered trademark, and Windows is an indication of the Microsoft Corporation in the United States and other countries. 

GOOGLE, Mozilla, Firefox, CHROME, ITEM are registered trademarks. 

#### **Trademark rights** 

The responsible person is not granted any rights or claims to the trademark, logo, or trade names of Franka Robotics. 

## **2.2 Identification** 

#### **Removal of identification** 

Copyright notices, serial numbers, and any other labelling that identifies the product or operating software may not be removed or modified. 

R02210/1.3/EN 

Franka Robotics GmbH © 

7 

**DECLARATION** OF INCORPORATION AND CERTIFICATES 

# **3 DECLARATION OF INCORPORATION AND CERTIFICATES** 

## **3.1 Declaration of Incorporation** 



R02210/1.3/EN 

Franka Robotics GmbH © 

8 

**DECLARATION** OF INCORPORATION AND CERTIFICATES 



R02210/1.3/EN 

Franka Robotics GmbH © 

9 

**DECLARATION** OF INCORPORATION AND CERTIFICATES 

## **3.2 Further Statements** 

### **3.2.1 RoHS / REACH / WEEE / Battery Directive** 

Further Information 

#### **status: 01.04.2022 Franka Research 3** 

**Restriction of Hazardous Substances (RoHS):** 

The  components _Control and Arm_ do not fall within the scope of EU RoHS Directive 2011/65/EU but still meet the requirements of the restricted substances and maximum concentration values that are allowed in homogenous materials: 

- Lead (0.1 %) 

- Mercury (0.1 %) 

- Cadmium (0.01 %) 

- Hexavalent chromium (0.1 %) 

- Polybrominated biphenyls (PBB) (0.1 %) 

- Polybrominated diphenyl ethers (PBDE) (0.1 %) 

The following exceptions are also applied: 6a: Lead as an alloying element in steel for machining purposes and in galvanized steel containing up to 0.35 % lead by weight 6b: Lead as an alloying element in aluminum containing up to 0.4 % lead by weight 6c: Copper alloy containing up to 4 % lead by weight 7a: Lead in high melting temperature type solders (i.e., lead-based alloys containing 85 % by weight or more lead) 7c-I: Electrical and electronic components containing lead in a glass or ceramic other than dielectric ceramic <u>in capacitors, e.g., piezo-electronic devices, or in a glass or ceramic matrix compound</u> **REACH:** 

_FRANKA ROBOTICS GmbH_ is a "downstream user" as defined in REACH. Our products are exclusively nonchemical products (manufactured items). In addition, no substances are released under normal conditions of use and conditions that can reasonably be predicted (Article 7, REACH). 

We confirm that our products do not contain more than 0.1 percent by mass of any of the listed substances on the published ECHA candidate list (SVHC) unless covered by RoHS exceptions (see above). Extensions published by the ECHA candidate list are matched with our products, and if it is known that one of these newly added substances is contained in our products, we will inform you immediately. <u>This confirmation was created based on currently available information from our suppliers.</u> **WEEE Directive:** 

The components _Control and Arm_ are not subject to the WEEE Directive 2002/96/EC for collection, recycling, and recovery for electrical goods. 

R02210/1.3/EN 

Franka Robotics GmbH © 

10 

**DECLARATION** OF INCORPORATION AND CERTIFICATES 

#### **Battery Directive:** 

The product Control contains a BIOS battery. 

Disposal of batteries: There is an obligation to return rechargeable and non-rechargeable batteries by Battery Directive 2006/66/EC; do not dispose of them with consumer waste. Dispose of them according to statutory orders and bring them to a recycler. Batteries will be recycled. The signs below the crossed-out trashcan indicate the substances lead (Pb), cadmium (Cd), or mercury (Hg). 



### **3.2.2 China RoHS 2** 



|**Part Name**||**Toxic and Hazard**|**ous Substances and**|**Elements /**有毒<br>**Hexavalent**|和有害的物质和<br>**Polbrominate**|元素<br>**Polbrominated**|
|---|---|---|---|---|---|---|
|<br>`部件名称`|**Lead**<br>铅<br>**(Pb)**|**Mercury**<br>汞<br>**(Hg)**|**Cadmium**<br>镉<br>**(Cd)**|<br>**Chromium**<br>六价铬<br>**(Cr (VI))**|**y**<br>**d biphenyls**<br>多溴联苯<br>**(PBB)**|**y**<br>**diphenyl ethers**<br>多溴二苯醚<br>**(PBDE)**|
|Control<br>`控制器`|X|O|O|O|O|O|
|Arm FP3<br>`臂架 FP3`|X|O|O|O|O|O|
|Robot Connecting<br>Cable<br>连接线<br>2,5m/5m/10m|O|O|O|O|O|O|
|Emergency Stop<br>Device<br>紧`急停止装置`|O|O|O|O|O|O|
|External Enabling<br>Device<br>`外部支持`设备<br>This Table is prepared in<br>`本表根据`SJ/T 11364-20|O<br>accordance with<br>06`的`规定编制。|O<br>the provisions of|O<br>SJ/T 11364-2006.|O|O|O|



**O** : Indicates that said hazardous substance contained in all of the homogeneous materials for this part is below the limit requirement of GB/T 26572-2011. 

O: `表示` 该部分所有均质材料中的所述有害物质低于 GB/T 26572-2011 `的限量要求。` 

**X:** indicates that said hazardous substance contained in at least one of the homogenous materials used for this part is above the limit requirement of GB/T 26572-2011 

X: `表示本` 试验用同质材料中至少有一种所含的有害物质高于 GB/T 26572-2011 `的限量要求。` (Enterprises may further provide in this box technical explanation for marking “X” based on their actual circumstances) ( `企` 业可根据自己的实际情况，在此框中进一步提供标示 "X " `的技` 术解释) 

R02210/1.3/EN 

Franka Robotics GmbH © 

11 

**DECLARATION** OF INCORPORATION AND CERTIFICATES 

## **3.3 Labeling on the equipment** 

### **3.3.1 Arm** 

#### **Type label** 



Figure 3.1: Type label 

#### **Emergency unlock label** 

In case of emergency there are three emergency unlock labels on the Arm point to the insertion points where the Emergency Unlocking Tool needs to be inserted to manually unlock the fail-safe locking system. 



Figure 3.2: Emergency unlock label 



#### **WARNING** 

**Falling heavy Arm when using Emergency Unlocking Tool** Risk of being trapped by the Arm when unlocking joints 

- Do support the Arm before and during unlocking it. 

- Do not place your head or other body parts between or underneath links of the Arm. 

- Do not place body parts (especially hands, fingers) between links of the Arm, the end effector, or stationary objects. 

- Do not use the Emergency Unlocking Tool while the Arm is powered on. 

- Only use the supplied Emergency Unlocking Tool. 

- Store Emergency Unlocking Tool near the Arm. 

R02210/1.3/EN 

Franka Robotics GmbH © 

12 

**DECLARATION** OF INCORPORATION AND CERTIFICATES 

#### **Hot Surfaces label** 



Figure 3.3: Hot Surface label 

**WARNING Hot Surfaces and Guiding** At ambient temperatures above 30 °C the robot surface can become too hot to touch. Therefore, using the Assist feature in Execution mode is not permitted above 30 °C. 

#### **Functional earth label** 

The functional earth label points to the location where functional earth can be connected to the Arm. 



Figure 3.4: Functional earth label 

#### **Lifting position label** 

The lifting position label indicates the points at which the Arm may be lifted. 



Figure 3.5: Lifting position label 

### **3.3.2 External Enabling Device** 

#### **Type label** 



Figure 3.6: Type label external device 

R02210/1.3/EN 

Franka Robotics GmbH © 

13 

**SAFETY** 

### **3.3.3 Emergency Stop Device** 

#### **Type label** 



Figure 3.7: Type label emergency stop device 

# **4 SAFETY** 

## **4.1 Safety instructions and general instructions** 

#### **Warning notices** 

Before installing, starting up, and operating the device, carefully read this manual and any additional documentation. Take NOTICE of the safety instructions as well as general indications. 

Warning notices are posted as follows: 



R02210/1.3/EN 

Franka Robotics GmbH © 

14 

**SAFETY** 

**SAFETYINSTRUCTION** 

SAFETY INSTRUCTION indicates processes that need to be strictly observed. 

#### **Indications** 



Indicates where further information can be obtained. 

## **4.2 Notice of Liability** 

Franka Research 3 has been developed according to the relevant quality standards. A hazard and risk assessment according to EN ISO 12100 has been carried out through the course of development and is the basis for Franka Research 3 and this manual. 

The present document includes assembly instructions for Franka Research 3 as a partly completed machinery. It contains descriptions of the conditions that must be met to correct incorporation in the final machinery not to compromise safety and health (e.g., Annex I of Machinery Directive 2006/42/EC). 

## **4.3 Intended use** 

Franka Research 3 is exclusively intended for use in research and development in academic and industrial environments. The system may only be used in sound technical condition, for its intended purpose, and within the technical specifications and operating conditions, with awareness of safety and possible dangers. 

<mark>The present Franka Research 3 system is intended exclusively for use as described in this manual.</mark> **_<mark>For the normal and extended working conditions under which the robot should operate, see Chapter 12 “Technical Data” and Chapter 7.2 “Correct installation site”.</mark>_** 

## **4.4 Misuse** 



#### **DANGER** 

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

R02210/1.3/EN 

Franka Robotics GmbH © 

15 

**SAFETY** 

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

## **4.5 General possible dangers and safety measures when working with robots** 

#### **Abstract of possible dangers** 

An extensive but not definitive list of dangers that generally may be presented by a robot system can be found under EN ISO 10218-1:2011 ANNEX A. 

Special attention is drawn here to the following dangers that the Franka Research 3 may present: 



#### **DANGER** 

#### **Electrical or fire hazards and dangerous fumes** 

Fire and fumes may cause breathing difficulties, eye irritation, lung damage, poisoning, and may lead to death. 

- Do not use the Franka Research 3 outside of its indicated specifications. 

R02210/1.3/EN 

Franka Robotics GmbH © 

16 

**SAFETY** 



#### **DANGER** 

**Damaged wires or inadequate electrical installation** 

Risk of personal injury by electric shock, as well as material damage. 

- Only use Franka Research 3 in sound technical condition. 

- Only install the emergency stop system with qualified personnel. 

- Check cables and electrical installations. 



#### **DANGER** 

#### **Risk of smoldering fires** 

Too many devices connected to the power supply system may lead to an overload of the electrical installation and may result in smoldering fires, which may cause death or severe damage to persons. 

- Connect the Franka Research 3 accordingly to avoid an overload of the electrical installation. 

- Install the overload protection devices accordingly. 



#### **WARNING** 

**Objects falling from end effectors due to a power supply cut off** 

- Objects falling from the gripper can lead to injuries to hands, fingers, feet, and toes. 

- Always wear personal protective equipment (e.g., safety shoes). 

- Use the appropriate type of grippers to prevent objects from falling. 



#### **WARNING** 

**Falling and unexpected motions of the robot, especially in earthquake-prone areas** 

- Risk of severe injuries such as crushing, tearing of the skin, and puncturing. 

- Level the platform. 

- Only install the Arm on even, unmoving, and stable platforms. Accelerations and vibrations are not permissible. 

- Do not install the Arm on hanging, tilted, or uneven platforms. 

- Level the platform in an upright position. 

- Ensure a correctly laid out and tight screw connection. 

- Tighten the screws after 100 hours of operation with the correct tightening torque. 

- If operated in an earthquake-prone area, take the respective hazard and risk assessments into consideration. 

R02210/1.3/EN 

Franka Robotics GmbH © 

17 

**SAFETY** 



#### **WARNING** 

**Dangerous and uncontrolled motions of the Arm** 

- Risk of severe injury, such as crushing, tearing of the skin, and puncturing from the Arm and end effectors. 

- Ensure that the end effector and/or the gripped object mass and the Center of Mass (CoM) are parameterized correctly. 

- Keep out of the workspace during operation. 



#### **CAUTION** 

**Damaged cables, plugs, mechanical housing, or oil leaks** 

Contact with leaking oil may cause eye or skin irritation. Electrical risks may lead to severe injury. 

- Only use Franka Research 3 in sound technical condition. 

- Do not use damaged cables, plugs, and mechanical housing for operation. In cases of doubt, contact Franka Robotics. 

#### **Sound condition** 



#### **CAUTION** 

**Leaking grease or oil through voids of structural elements of the robot** 

- Irritation of skin and eyes. 

- Stop operating the machine. 

- Contact manufacturer. 

- Use gloves. 

- Seek medical attention after contact with eyes or skin. 

#### **Disruptions** 

#### **_NOTICE_** 

The operator will be informed about possible malfunctions through Desk. Malfunctions need to be rectified before continuing the operation. 

- To rectify the possible malfunctions, follow the instructions in the Franka UI. A reboot of the system may be required. 

#### **Overload of joints** 

#### **_NOTICE_** 

An offline overload in all the robot's joints may lead to material damage to the robot. 

- Perform a risk assessment with foreseeable misuse in mind. 

- Adhere to the system’s warning to take the robot out of operation if necessary. 

R02210/1.3/EN 

Franka Robotics GmbH © 

18 

**SAFETY** 

## **4.6 Application related to possible dangers and safety measures** 

The following possibly safety-related aspects are to be considered when planning and designing the application and performing the hazard & risk assessment for completed machinery. The integrator is obligated to perform a risk analysis. 

#### **Functionalities and features of various safety levels** 

Franka Research 3 offers functionalities and features of various safety levels. **_<mark>All safety functions and their corresponding safety ratings are described in section Safety Functions in Chapter 4.10 “Safety Functions “.</mark>_** All other functionalities described throughout this chapter is not classified as safety-rated according to EN ISO 13849-1. You may, therefore, not rely on the availability of these functionalities. 

Please NOTICE that the integrator is obligated to perform a risk analysis. 

#### **Unexpected motion** 



#### **CAUTION** 

#### **Unexpected movement of Arm** 

- The use of various applications, handled end effectors and surrounding objects, may cause crushing between Arm segments and impact and collision. 

- Ensure that the end effector and/or the object mass and the Center of Mass (CoM) are parameterized correctly. 

- Keep out of the maximum workspace during operation. 

#### **Trapping within a completed machinery** 



#### **WARNING** 

#### **Risk of trapping body parts or person** 

- Risk of severe injury, such as crushing, tearing of the skin, and puncturing from the Arm and end effectors. 

- Do not place body parts between Arm segments. 

- In case of acute mortal danger: 

   1. Press the Emergency Stop Device to stop the robot from operating. 

   2. Pull or push the Arm out of the dangerous position manually. 

**_<mark>Refer to the topic 4.9 “Manually Moving the Arm” for more information.</mark>_** 

#### **Wiring of end effectors** 

#### **_NOTICE_** 

If an end effector is used with Franka Research 3, the maximum attachable payload is reduced by the weight of the end effector and its external wiring. 

R02210/1.3/EN 

Franka Robotics GmbH © 

19 

**SAFETY** 

#### **_NOTICE_** 

External wiring adds additional loads and torques to the Arm which may influence Franka Research 3‘s control performance. 

#### **Initiation of motion of externally wired end effectors, associated equipment** 

#### **_NOTICE_** 

Because of different configurations, installed apps and services, Franka Research 3 is able to send protocols to possibly connected machines (incl. starting motion), externally wired end effectors, and other associated equipment. Please be aware of possible related risks of using external equipment. 

#### **Single Point of Control** 

<mark>Franka Research 3 can be controlled via a single Franka UI connection or field bus. Single Point of Control (SPoC) mechanisms ensure control by one source only. Field buses are covered by SPoC as well.</mark> **_<mark>For more information about SPoC, please refer to Chapter 4.2: Single Point of Control (SPoC) in the respective Operating Manual corresponding to your system version (e.g., 5.8.0).</mark>_** 



#### **WARNING** 

**Unexpected movement of Arm** 

Risk of severe injury, such as crushing, tearing of the skin, and puncturing from the Arm and end effectors. 

- Ensure that the end effector and/or the object mass and the Center of Mass (CoM) are parameterized correctly. 

- Keep out of the workspace during operation. 

- In case of acute mortal danger: 

   1. Press the Emergency Stop Device to stop the robot from operating. 

   2. Pull or push the Arm out of the dangerous position manually. 

- In case of non-life-threatening danger: 

   1. Use the Emergency Unlocking Tool to move the Arm. 

#### **Surface temperature of the Arm (from base until axis 7, excluding flange)** 



#### **WARNING** 

#### **Hot Surfaces** 

Handling of the Arm's metal or plastic segments for a prolonged time after intense task execution may cause thermal burns. 

- Do not touch the Arm’s segments for more than 60 seconds after stopping the Franka Research 3 after an intense task execution at maximum payload and extended temperature. 

R02210/1.3/EN 

Franka Robotics GmbH © 

20 

**SAFETY** 



#### **WARNING** 

#### **Hot Surfaces and Guiding** 

At ambient temperatures above 30 °C the robot surface can become too hot to touch. Therefore, using the Assist feature in Execution mode is not permitted above 30 °C. 

Effects depending on the task and environment. 

The required safety instruction depends on risk assessment (regarding hot surfaces) 

#### **SAFETY-** 

#### **INSTRUCTION** 

At extended ambient temperatures between 25 °C and 45 °C (after intense task execution and once Franka Research 3 is set to “monitored stop” state), the integrator needs to implement measures and evaluate the risks of touching the Arm for a prolonged time (< 60 s) without being subjected to thermal burns (EN ISO 13732-1:2006). Measures include but are not limited to the following: 

- Cool-down time for the robot. 

- Switching off the robot for a certain amount of time. 

- Notifying the operator. 

- Marking the spots that are most likely to be hot. 

- Prohibiting access to the robot. 

#### **SAFETYINSTRUCTION** 

The integrator needs to implement measures for touching the surfaces of the Arm, the end effector, and the end effector’s flange regarding possible heating which may lead to thermal burns (EN ISO 13732-1:2006). Measures include but are not limited to the following: 

- Cool-down time for the robot. 

- Switching off the robot for a certain amount of time. 

- Notifying the operator. 

- Marking the spots that are most likely to be hot. 

- Prohibiting access to the robot. 

## **4.7 Installation of safety peripherals** 

#### **Emergency stop installation** 

The Emergency Stop Device needs to be installed according to the generally valid and accepted engineering standards, e.g., European standards EN 60204 and related. 

The Emergency Stop Device provided by Franka Robotics needs to be connected to the X3.1 port. Other devices than the Emergency Stop Device provided by Franka Robotics may also be connected to the X3 port. 

The devices connected to the emergency stop signal must follow EN 60947-5-5 or equivalent. 

Store detached devices that no longer fulfill a safety function away from the device to prevent them from mistakenly being activated. 

R02210/1.3/EN 

Franka Robotics GmbH © 

21 

**SAFETY** 

#### **_NOTICE_** 

Place the connected Emergency Stop Device such that it is always reachable in case of an emergency but that an accidental use can be prevented. 



Figure 4.1: Connection Emergency Stop Device 

<mark>1</mark> X3 - Safe inputs connector <mark>2</mark> Emergency Stop Device 

#### **Stopping time and distance** 

Stopping time (i.e., the time that passes between the request of an emergency stop and the complete stop of the Arm) and stopping distance (i.e., the distance covered by the Arm after activation of the emergency stop until it comes to a complete stop) were measured per EN ISO 10218-1, Annex B. Stopping time and distance can be found in the appendix of this document. 

## **4.8 Fail-safe locking system** 

#### **Fail-safe locking system** 

When the Arm is disconnected from the power supply, the locking bolts automatically lock all seven joints. The locking bolts mechanically lock any motion regarding the joints so that the Arm stays in position even when it is not supplied with power. 

Due to the technology of these locking bolts, the exact position cannot be maintained when the power is cut off. The locking bolts lock with an audible click and the Arm lowers a few centimetres. Especially in the joints, which are particularly influenced by gravity due to their alignment and position. 

#### **Unlocking the safety locking system** 

Each axis will move slightly as soon as the safety locking system unlocks. 

R02210/1.3/EN 

Franka Robotics GmbH © 

22 

**SAFETY** 

## **4.9 Manually Moving the Arm** 

#### **Moving the Arm without electrical power** 



#### **CAUTION** 

#### **Moving Arm** 

- Risk of severe injury, such as crushing, tearing of the skin, and puncturing 

- Always wear personal protective equipment (e.g., safety goggles). 

- The integrator needs to perform a risk analysis for any attached end effectors. 

- Do not stand in the maximum workspace during operation 

#### **_NOTICE_** 

The integrator must assess the risk that a person may become trapped. 

If a person is trapped by the Arm, follow one of the three release options below to free them even when the power supply is cut off. 

- Use the Emergency Unlocking Tool at the corresponding openings of the joint to be unlocked to unlock the robot and move it by hand. 

- Unscrew the Arm base from its mounting place. 

- Manually move the Arm. 

In case of non-acute danger and jamming of the Arm, use the Emergency Unlocking Tool. 



#### **WARNING** 

**Falling heavy Arm when using Emergency Unlocking Tool** 

Risk of being trapped by the Arm when unlocking joints 

- Do support the Arm before and during unlocking it. 

- Do not place your head or other body parts between or underneath links of the Arm. 

- Do not place body parts (especially hands, fingers) between links of the Arm, the end effector, or stationary objects. 

- Do not use the Emergency Unlocking Tool while the Arm is powered. 

- Only use the supplied Emergency Unlocking Tool. 

- Store Emergency Unlocking Tool near the Arm. 

#### **Action: Emergency unlock** 

**SAFETYINSTRUCTION** 

1. Press the Emergency Stop Device to stop the robot from operating. 

2. Take the unlocking tool from the Pilot’s base. 

3. Hold the Arm’s segments. 

R02210/1.3/EN 

Franka Robotics GmbH © 

23 

**SAFETY** 

4. Insert the unlocking tool in the respective trapezoidal openings and unlock one or more joints one after another. 

The openings are marked with the “Emergency Unlock” label. 

The Arm segment can now be moved manually. If unlocking fails, the user should try again, ensuring that the emergency unlocking tool is inserted perpendicular to the opening. 



Figure 4.2: Emergency unlock 

#### **_NOTICE_** 

Be aware that as soon as the unlocking tool is inserted, the Arm segment towards the wrist of the Arm can fall down with gravity. 

#### **_NOTICE_** 

- The integrator needs to make sure that the unlocking tool is stored in a holder at the base of the robot. 

- Do not remove the unlocking tool unless in an emergency. 

- The unlocking tool must always be within reach. 

- Only use the original unlocking tool. 

- The unlocking tool should only be used in case of emergency. 

R02210/1.3/EN 

Franka Robotics GmbH © 

24 

**SAFETY** 

**Action: Pushing away manually** 



Figure 4.3: Pushing away manually 

#### **SAFETYINSTRUCTION** 

- In case of acute mortal danger: 

1. Press the emergency stop device to stop the robot from operating. 

2. Pull or push the Arm out of the dangerous position manually. 

3. Secure the robot arm from falling down. 

#### **_NOTICE_** 

Manually pulling or pushing the Arm will damage the Arm as the joints will be overloaded. 

- The Arm should only be manually pulled or pushed away in safety-critical situations. 

## **4.10 Safety Functions** 



#### **WARNING** 

**Hot Surfaces and Guiding during Recovery** 

At ambient temperatures above 30 °C the robot surface can become too hot to touch. Therefore, in case of occurence of a safety function violation which requires hand-guiding during recovery, the following must be observed: 

- Recovery may be performed only by personnel specifically trained for this situation. 

- Before recovery, surface temperatures must be evaluated to be within touchable limits. Cooldown times depend on previous operation and ambient temperatures. 

- Wearing heat resistant safety gloves for this procedure is advised. 

#### **_NOTICE_** 

Franka Research 3 distinguishes between two kinds of safety functions: monitoring functions and stopping functions. 

Monitoring functions guarantee that limits are not breached, e.g. speed (SLS-J), position (SLP-C)… 

R02210/1.3/EN 

Franka Robotics GmbH © 

25 

**SAFETY** 

Stopping functions are triggered upon a monitoring violation or a safety input. It is the Safety Operator’s obligation to consider stopping times and stopping distances when configuring the limits. 

#### **_NOTICE_** 

Connecting external devices with a separate power supply may jeopardize the system’s safety function if the electrical ratings are not complied with. 

In addition, the voltages in the connected devices must either be SELV or suitably isolated from systemconnected signals. 

The safety functions of the Franka Research 3 are rated PL d Category 3 (ISO 13849-1) with a PFH value of 4,8E-08. The only expectation as listed below is SEEPO which is rated PL b Category B (ISO 13849-1) with a PFH value of 6,2E-08. 

#### **Safe inputs** 

|**Name**|**Description**|**Safety Rating**|**Stop Reaction**|
|---|---|---|---|
|X3.1 - Emergency stop|The X3 connector in the robot<br>base provides one safe input to<br>connect an emergency stop.|PL d / Cat.3|Category 1 stop|
|X4 - External Enabling|The X4 connector at the robot<br>base provides one safe input<br>dedicated to a 3-position External<br>Enabling Device.|PL d / Cat.3|Releasing or fully pressing the Enabling Button<br>activates the SMSS safety function. The<br>reaction in case of a violation of SMSS<br>depends on the active safety scenario.|
|Enabling Button|A 3-position Enabling Button is<br>provided near the flange on the<br>Pilot-Grip of the robot.|PL d / Cat.3|Operating mode “Programming”: Category 1<br>stop (see predefined scenario “Idle”)<br>Operating mode “Execution”: Reaction<br>depending on SMSS configuration in scenario<br>“Work.”<br>During safety function violation or error<br>recoveries, fully pressing or releasing the<br>Enabling Button triggers a Category 1 stop.|
|X3.2 - Safe input 1<br>X3.3 - Safe input 2|The X3 connector on the robot<br>base provides two additional safe<br>inputs. The behavior of those two<br>inputs can be configured in the<br>safety setup.|PL d / Cat.3|Depends on the configuration in safety<br>scenarios.|



#### **Monitoring functions** 

|**Name**|**Abbreviation**|**Description**|**Safety**<br>**Rating**|**Recovery in case of violation**<br>**NOTICE: The operator can recover all**<br>**violations.**|
|---|---|---|---|---|
|Safely Limited Cartesian<br>Position|SLP-C|Monitoring of the Cartesian position<br>of certain points on the Arm. The<br>position is checked against user-<br>defined Cartesian area.<br>The following points are monitored:<br>• Flange<br>• Elbow<br>• Wrist<br>• Customer defined tool spheres<br>The monitoring can be configured to<br>signal violation either when one or<br>morepoints are inside the defined|PL d /<br>Cat.3|Violated position or orientation limits<br>will be shown in Desk of Franka UI.<br>• Unlock brakes of robot.<br>• Guide robot out of Cartesian<br>position limit. Franka UI shows if<br>position limits are not violated<br>anymore.<br>• Finish recovery by pressing Confirm<br>in Desk.|



R02210/1.3/EN 

Franka Robotics GmbH © 

26 

**SAFETY** 

|||space or when one or more points<br>are outside the defined limits.<br>Parameterization:<br>• End Effector model (up to five<br>spheres)<br>`o`<br>Radius of each sphere<br>`o`<br>Position of each sphere<br>center relative to the flange<br>Hint: This is a general setting and<br>will affect all safety functions using<br>this tool model.<br>• Monitored Cartesian space (box)<br>• Violation if inside/outside|||
|---|---|---|---|---|
|Safely Limited Cartesian<br>Speed|SLS-C|Monitoring of the Cartesian speed<br>of certain points on the Arm<br>structure. The following points are<br>monitored:<br>• Flange<br>• Elbow<br>• Wrist<br>• Centers of customer-defined tool<br>spheres<br>Parameterization:<br>• Limit for Cartesian speed|PL d /<br>Cat.3|A violation of the speed limit is shown<br>in a dialog in the Franka UI.<br>• Confirm violation by pressing the<br>button in Pop-up message.<br>No further recovery procedure is<br>necessary.|
|Safely Monitored Stand<br>Still|SMSS|Monitoring of the standstill in<br>Cartesian space of certain points on<br>the Arm structure. The following<br>points are monitored:<br>• Flange<br>• Elbow<br>• Wrist<br>• Centers of customer-defined tool<br>spheres<br>The user cannot change the<br>parameters of this safety function.|PL d /<br>Cat.3|A violation dialog is shown in the<br>Franka UI.<br>• Confirm violation by pressing the<br>button.<br>No further recovery procedure is<br>necessary.|
|Safe End Effector Power<br>Off|SEEPO|Safely switch off the power<br>provided to the end effector (48 V<br>power line). The behavior of SEEPO<br>can be configured in the safety<br>setup. E.g., it can be configured that<br>SEEPO switches off the power<br>when an emergency stop is<br>triggered.<br>Parameterization:<br>• General configuration, whether<br>SEEPO is active or not<br>• Switch-off triggers of SEEPO|PL b /<br>Cat. b|The power of the end effector can be<br>switched on again in Settings or the<br>sidebar of Desk.|



#### **Internal monitoring functions (not parametrizable and configurable in safety rules)** 

|**Name**|**Abbreviation**|**Description**|**Safety**<br>**Rating**|**Reaction**|**Recovery in case of violation**<br>**NOTICE: The operator can recover all violations.**|
|---|---|---|---|---|---|
|Safely<br>Limited<br>Position<br>of Joint|SLP-J|Monitoring of the<br>position of each joint in<br>joint space.<br>This safety function is<br>only used internally to<br>protect the joint limits of<br>the Arm, prevent self-<br>collisions and local<br>clamping. It is not<br>available in user-defined<br>scenarios.|PL d /<br>Cat.3|-|A dialog within Franka UI informs the user about<br>the violation and allows recovery.<br>• Unlock the joint that shall be moved by clicking<br>the unlock icon in the recovery dialog.<br>• To enable recovery motion, press the External<br>Enabling Device.<br>• Move the joint by pressing the +/- buttons in<br>the recovery dialog.<br>Hint: Joints in a violated state can only be moved<br>away from violated limit. All other joints can be|



R02210/1.3/EN 

Franka Robotics GmbH © 

27 

**SAFETY** 

|||This is a limiting function.|||moved in both directions to move the robot into a<br>more convenient pose.|
|---|---|---|---|---|---|
|Safely<br>Limited<br>Speed of<br>Joint|SLS-J|Monitoring of the speed<br>of a single joint in joint<br>space.<br>This internal safety<br>function is used, e.g., to<br>prevent fast motions<br>during joint position<br>recovery.|PL d,<br>Cat. 3|Cat. 1<br>Stop|A violation dialog is shown in Franka UI.<br>1. Confirm violation by pressing the button.<br>No further recovery procedure is necessary.|
|Safely<br>Limited<br>Distance|SLD|SLD monitors a single<br>joint to stay within a<br>permitted position<br>window.<br>This internal safety<br>function is used, e.g., to<br>prevent excessive motion<br>during the brake opening<br>procedure.|PL d,<br>Cat. 3|Cat. 1<br>Stop|A safety error dialog is shown in the Franka UI.<br>1. Acknowledge error by pressing the button.<br>No further recovery procedure is necessary.|



#### **Stopping functions** 

|**Name**|**Description**|**Safety Rating**|
|---|---|---|
|Category 0 stop|The Arm is stopped immediately by removing power from the motors<br>and applying the brakes.|PL d / Cat.3|
|Category 1 stop|The Arm is stopped in a controlled manner using the normal control of<br>the motors until the standstill of each joint. The brakes are applied,<br>and the power is removed from the Motors upon standstill.<br>The Cartesian speed deceleration is monitored.|PL d / Cat.3|
|Category 2 stop|The Arm is stopped in a controlled manner using the normal control of<br>the motors until the standstill of each joint. Upon standstill, the<br>standstill is safely monitored.<br>The Cartesian speed deceleration is monitored.|PL d / Cat.3|



#### **Safe outputs** 

|**Name**|**Description**|**Safety Rating**|
|---|---|---|
|Safe End Effector|Switch the power provided to the end effector (48 V power line) off.|PL b / Cat.b|
|Power Off|||



#### **Further safety ratings** 

The 3-stage Enabling Button near the robot's flange is realized in compliance with IEC 60204-1:2016 and IEC 609475-8:2006. 

The 3-stage External Enabling Device provided by Franka Robotics is realized in compliance with IEC 60204-1:2016 and IEC 60947-5-8. 

The Emergency Stop provided by Franka Robotics complies with IEC 60204-1:2016 and EN ISO 13850:2015. 

### **4.10.1 Other safety-related recoveries (in case of safety errors)** 

#### **Joint position error recovery** 

Only Safety Operators can recover joint position errors. 

A dialog in Franka UI informs the user about the error and allows recovery. 

**_<mark>Detailed instructions on how to correct the error can be found in Chapter 9 Troubleshooting in the respective Operating Manual corresponding to your system version (e.g.,5.8.0).</mark>_** 

R02210/1.3/EN 

Franka Robotics GmbH © 

28 

**SAFETY** 

#### **Safe input error recovery** 

Safe input errors are recoverable by confirming the respective dialog in Franka UI if confirmation for those inputs is configured in Watchman. 

#### **Other safety errors** 

Other safety errors are typically not recoverable. Please try to restart the system to recover from such errors. If the error persists, contact your vendor or Franka Robotics. 

#### **General info for all cases** 

- In case of a safety violation, the robot does not allow motion until the recovery has been accomplished. 

- In case of a safety violation, the base flashes slowly in red. 

- If necessary, Franka UI will show a recovery wizard to perform the recovery procedure. 

- Only the safety operator can recover joint position errors. 

- The operator can perform all other recoveries. 

**_<mark>Further measures for possible troubleshooting are described in chapter in Chapter 9 Troubleshooting in the respective Operating Manual corresponding to your system version (e.g.,5.8.0).</mark>_** 

## **4.11 Additional information for planning and initial installation of a robot system** 

According to the EN ISO 10218-2 and EN ISO 8373 standards, a robot system is understood to be a robot that is set up as a complete system with peripheral devices such as robot tools, workpieces, conveyor technology and all devices and protective equipment involved. Due to the motion of robots and the integrated applications, a robot system represents a potential hazard for those people involved with activities of operation, assembly or maintenance. The job of both the manufacturer and the installer of a robot system is to analyze and evaluate these hazards and to ensure appropriate protective measures. 

This specification is based on laws, regulations and guidelines that are country-specific and thus depend on the respective location (place of the operation) of the robot. 

In the European Economic Area (EEA), overarching regulations apply, which may be supplemented by respective country-specific legislation, industry-specific regulations and internal company regulations. 

When planning a robot system, it is therefore necessary to find out about the regulations at the installation site and to take these into account accordingly. 

This type of industry can also lead to different specifications. For example, will the robot system be used in industrial Research or in research? 

As mentioned above, the location of the robot system determines which various rules, regulations and laws must be observed. In the European Economic Area (EEA), the Machinery Directive and harmonized European standards apply across all countries. Furthermore, local legislation such as the Product Safety Act, the Product Liability Act and the Ordinance on Industrial Safety and Health in Germany must be considered. 

The most important rules and regulations for the build-up of a robot system are listed below. 

R02210/1.3/EN 

Franka Robotics GmbH © 

29 

**SAFETY** 

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

Thus, the statement can be made that no robot system may be operated without appropriate protective measures. Protective measures can be, for example: 

- ➢ Safety protective device 

- ➢ Electro-sensitive protective equipment 

- ➢ Fencing and/or physical barriers 

- ➢ Marked areas 

- ➢ Signs 

- ➢ Emergency stop buttons 

- ➢ Indicating elements 

- ➢ Control system safety devices 

- ➢ Robot internal safety functionalities <mark>(</mark> **_<mark>For the details please refer to above section 4.10 in this Manual</mark>_** ) 

Due to the different possible applications of a robot, Franka Robotics cannot provide a uniform guideline for determining the required protective devices when integrating a robot system. The responsibility for the safe realization of the robot system lies with the integrator / operator. 

R02210/1.3/EN 

Franka Robotics GmbH © 

30 

**SAFETY** 

A very good and detailed guide to the design of robot systems is also described on the DGUV (German Social Accident Insurance) website => DGUV Information 209-074. 

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

R02210/1.3/EN 

Franka Robotics GmbH © 

31 

**SAFETY** 

- III. Layout: 

In the final layout of the robot system, all protective measures should be drawn to scale. There should be a clear assignment to the protective measures identified in the risk assessment. 

- IV. Realization phase: 

Set-up of the system and implementation of the defined protective measures. 

- V. Verification: 

After the system has been set up, including all protective measures, a verification of the protective measures must be performed in accordance with the respective standards. For example, the testing of the control technology protective measures is referred to as "functional safety verification" in standard 13849-2, and the requirements for validations are regulated therein. 

This protocol of verification is an essential component for the acceptance of a robot system. 

- VI. Acceptance: 

The final acceptance of a robot system includes a detailed logging of all individual steps mentioned above. In industrial areas of application, a declaration of conformity (CE) is required by the distributor in accordance with the Machinery Directive. A declaration of conformity (CE) is also required if a robot system is set up for "own use" in in-house Research. For robot systems in research and in the laboratory, it is also necessary to design the operation of robots to be safe for people and to implement appropriate protective measures. The Machinery Directive defines robot systems for research purposes as systems designed for a specific research purpose and built for temporary use only. Thus, the decisive factor is whether the system has temporary use (e.g., a one-time experiment that will be dismantled afterwards - no CE - or permanent use as equipment in the laboratory - CE required). 

R02210/1.3/EN 

Franka Robotics GmbH © 

32 

**EQUIPMENT** OVERVIEW 

# **5 EQUIPMENT OVERVIEW** 

The following figure shows the minimum configuration of the system and exemplifies the cabling. 



Figure 5.1: Equipment overview 



R02210/1.3/EN 

Franka Robotics GmbH © 

33 

**EQUIPMENT** OVERVIEW 

## **5.1 The Arm** 

The Arm has the following components: 



Figure 5.2: Overview Arm 

|1|Pilot|7|Elbow|
|---|---|---|---|
|2|Pilot-Grip|8|Shoulder|
|3|Pilot-Disc|9|Holder for Emergency Unlocking Tool|
|4|X6-End effector connector|10|Status light|
|5|Flange for end effector|11|Base|
|6|Wrist|||



R02210/1.3/EN 

Franka Robotics GmbH © 

34 

**EQUIPMENT** OVERVIEW 

#### **Joint Indicators** 

Arrows are positioned on either side of the joints to indicate the recovery pose of the robot. The number of each joint is clearly labelled. Plus, and minus indicators illustrate the direction of positive and negative rotation of the joint. 



Figure 5.3: Reference Triangles 

#### **World Coordinate System Indicators** 

Indicators on the base provide information on the world coordinate system. The X and Y axis are clearly indicated, thereby implying the Z axis. 



Figure 5.4: World Coordinate System Indicators 

R02210/1.3/EN 

Franka Robotics GmbH © 

35 

**EQUIPMENT** OVERVIEW 

#### **Alignment Marks** 

To facilitate easy repositioning of the robot in situations where pins are not sufficient, alignment marks are included on the base. 



Figure 5.5: Base Alignment Marks 

#### **Pilot - top view** 

Parts of Desk and the integrated end effectors can be operated directly from the robotic Arm via the Pilot-Disc. 

R02210/1.3/EN 

Franka Robotics GmbH © 

36 

**EQUIPMENT** OVERVIEW 



Figure 5.6: Pilot 

|1|Pilot-Mode button|6<br>Status light|
|---|---|---|
|2|Confirmbutton|7<br>EnablingButton|
|3|Teach button|8<br>Guiding-Mode Button|
|4|Delete button|9<br>GuidingButton|
|5|Arrow keys||



#### **Pilot** 

The Pilot is the user interface integrated directly into the Arm for Guiding the robot and the easy interaction with end effectors and Desk. The Pilot consists of Pilot-Disc (1-6) and Pilot-Grip (7-9). 

**_<mark>For more information on Desk, please refer to Chapter 6.2 Desk in the respective Operating Manual corresponding to your system version (e.g., 5.6.0 or 5.8).</mark>_** 

#### **Pilot-Disc (1-6)** 

The Pilot-Disc is located on top of the Pilot and is used for interacting with the robot system. You can switch between the control of Arm or end effector by pressing the Pilot-Mode button (1) on the Pilot-Disc. Select individual Apps, parameterize them or enter poses by manually guiding the Arm to the desired pose and pressing the Teach button (3). 

#### **Pilot-Grip (7-9)** 

The Pilot-Grip is located near the robot's tip as part of the robot structure. The Pilot-Grip provides a Guiding Button, an Enabling Button, and a Guiding-Mode Button. 

#### **Pilot-Mode button (1)** 

By pressing the Pilot-Mode button (1), the user switches between using the arrow keys of the Pilot-Disc to navigate Desk or to control the integrated end effectors (e.g., Franka Hand). 

R02210/1.3/EN 

Franka Robotics GmbH © 

37 

**EQUIPMENT** OVERVIEW 

#### **Confirm button (2)** 

If Confirm button is illuminated, all changes made in a context menu will be confirmed and skips to the next section. The Confirm button saves any selections made. 

#### **Teach button (3)** 

Save an Arm pose, or an end effector pose by moving the Arm or end effector to the desired configuration and pressing the Teach button. 

#### **Delete button (4)** 

If illuminated, pressing the Delete button deletes a selected pose or section. 

#### **Arrow keys (5)** 

The Arrow keys can either navigate Desk or control integrated end effectors depending on the Pilot-Mode. In end effector mode, the key assignment depends on the active end effector. 

#### **Enabling Button (7)** 

The Enabling Button is located on the left side of the Pilot-Grip and enables robot motions if pressed to the middle position. To move the robot, half-press the Enabling Button while pressing the Guiding Button simultaneously. The Enabling Button is safety rated per the requirements in EN ISO 10218-1. The three positions of the Enabling Button either stop, re-enable, or move the robot. To immediately stop the robot, release or fully press the Enabling Button. After stopping, release it first completely and then press it again to its middle position to re-enable the robot. 



Figure 5.7: Switching status Enabling Button 



Figure 5.8: Enabling Button 

R02210/1.3/EN 

Franka Robotics GmbH © 

38 

**EQUIPMENT** OVERVIEW 

#### **Guiding-Mode Button (8)** 



Figure 5.9: Guiding Mode Button 

The Guiding‑Mode Button is located on the top of the Pilot-Grip and allows the user to change between different Guiding modalities by pressing the Guiding-Mode Button. The possible Guiding-Modes are translation only, rotation only, free moves, and user-defined movement. 



Figure 5.10: Guiding Mode Button 

#### **Guiding Button (9)** 



Figure 5.11: Guiding Button 

The Guiding Button is located on the right of the Pilot-Grip. Press the Guiding Button while half-pressing the Enabling Button (7) simultaneously to move the robot. 

R02210/1.3/EN 

Franka Robotics GmbH © 

39 

#### **EQUIPMENT** OVERVIEW 



Figure 5.12: Guiding Button 

#### **Base of the Arm** 



Figure 5.13: Connection ports at robot base 

- <mark>1</mark> X1 - Connection to Control connector 

- <mark>2</mark> X3 - Safe inputs connector 

- <mark>3</mark> Status light 

- <mark>4</mark> Insertion point for Emergency Unlocking Tool <mark>5</mark> X4 - External enabling connector <mark>6</mark> X5 - Robot network connector 

The base of the robot has several ports to connect and support various equipment: 

- X1 - Connection to Control 

R02210/1.3/EN 

Franka Robotics GmbH © 

40 

**EQUIPMENT** OVERVIEW 

- X3 - Safety Signals 

   - X3.1 - Emergency stop: A category 1 stop command will be triggered to stop the robot and optionally cut the power to the end effector by pressing the Emergency Stop Device. This behavior can be configured in Watchman. 

   - X3.2, X3.3 - Safe inputs: The X3 port allows two additional safe inputs. Their behavior can be configured in Watchman. For more information on Watchman, please refer to Operating Manual, chapter 5.3. 

   - X4 - External Enabling 

The 3-position External Enabling Device enable “Test & Jog” when the system is in Programming mode. It allows Franka Research 3 to move. Programs can be started via Desk. 

- X5 - Robot network 

The interface device running the browser-based Franka UI can be connected to the X5 Ethernet port. 

#### **SAFETYINSTRUCTION** 

A custom connector with the corresponding safety signals must be assembled to utilize the configurable Safe inputs (X3.2, X3.3). When doing so, the existing Emergency stop can no longer be used. Therefore, the Emergency stop functionality must be integrated for channel X3.1 in the custom connector. 

#### **_NOTICE_** 

By default, the Safe input channels X3.2 and X3.3 are assigned to the SMSS safety function in the "Work" scenario in Watchman. Suppose no external safety devices are connected to X3.2 and X3.3 (only Franka Robotics emergency stop is connected to X3.1). Those inputs will be considered “activated,” meaning it will not be possible to move the robot with the default "Work" scenario rules. Depending on the applicationspecific risk & hazard analysis, the default rules may be changed to allow robot movements regardless of X3.2 and X3.3. 

#### **End effector flange** 

End effectors, such as Franka Hand, can be connected via the end effector flange. The end effector flange has been developed according to the relevant quality standards of DIN ISO 9409-1-A50 **_. For more information, see the chapter 7.8 “Mounting End Effectors“ in this manual._** 

R02210/1.3/EN 

Franka Robotics GmbH © 

41 

**EQUIPMENT** OVERVIEW 



Figure 5.14: End effector flange 

**_NOTICE_** Franka Hand is not part of the certified machinery. 

## **5.2 Control** 



The operation of the Arm is only permitted with the Control provided by Franka Robotics. 

The Control is the main control unit and is part of Franka Research 3. The main control unit realizes monitoring and control of the mechanical structure of the robot. 



Figure 5.15: Dimensions and connection ports of control 

R02210/1.3/EN 

Franka Robotics GmbH © 

42 

**SCOPE** OF DELIVERY AND ADDITIONAL EQUIPMENT 

- <mark>1</mark> C2 - Shop floor network connector <mark>2</mark> C1 - Connection to Arm connector 



Figure 5.16: Connection ports 

- <mark>1</mark> C3 – Power connector <mark>2</mark> Power switch 

#### **Installation** 

The Control fits in a 2RU 19” rack. 

# **6 SCOPE OF DELIVERY AND ADDITIONAL EQUIPMENT** 

## **6.1 Included in the box** 

Arm 

- 1x Arm 

- 1x Emergency Unlocking Tool 

- 4x screw (ISO 4762, M8x20, ST 10.9 A2K) 

- 4x washer (ISO 7089, M8, ST HV300 A2K) 

- 1x screw (ISO 4762, M5x8, ST 8.8 A2K) 

- 1x tooth washer (DIN 6797-A, M5, ST A2K) 

- 1x Quick Guide for Installation FR3 (Document number: R02040) 

R02210/1.3/EN 

Franka Robotics GmbH © 

43 

**SCOPE** OF DELIVERY AND ADDITIONAL EQUIPMENT 



Figure 6.1: Scope of delivery Arm 

#### **Control** 

- 1x Control 

- 1x country-specific power cable 



Figure 6.2: Scope of delivery Control 

#### **Devices** 

- 1x External Enabling Device 

- 1x Emergency Stop Device 



Figure 6.3: Scope of delivery devices 

R02210/1.3/EN 

Franka Robotics GmbH © 

44 

**SCOPE** OF DELIVERY AND ADDITIONAL EQUIPMENT 

#### **Accessories** 

- 1x Connecting cable 



Figure 6.4: Scope of delivery Connecting cable 

## **6.2 Not included in the box** 

For additional accessories, e.g., cobot pump, visit https://franka.world/. 

The following equipment is not included: 

- Interface device 

   - Tablet/Notebook/PC 

The interface device should be equipped with a browser (Chrome, Chromium, or Firefox), an Ethernet port, and ideally with touch functionality. 

- Material 

   - Ethernet cable with RJ 45 connector for connecting the interface device to the Arm 

   - Ethernet cable with RJ 45 connector for optional connection of the Control to the company network or PC workstation 

   - Mounting accessories (recommended by Franka Robotics): 2x 6 mm h8 pins for precise mounting of the Arm, if applicable 

   - Baseplate to mount the Arm (depending on the baseplate, different screws and washers may be needed, **_<mark>see table in Chapter 7.4“Mounting the Arm</mark>_** <mark>”</mark> ) 

   - Functional earth cable with eye 

- Tools 

   - Hex key for mounting the Arm on the baseplate 

   - Screwdriver for connecting the functional earth cable 

   - Level for ensuring the horizontal installation of the Arm 

   - Torque spanners to tighten screws with 30 Nm 

## **6.3 Available spare parts and accessories** 

The spare parts for Franka Research 3 include but are not limited to: 

- Arm 

- Control incl. country-specific power cable 

- External Enabling Device 

- Emergency Stop Device 

- Connecting cable (2.5 m, 5 m, or 10 m) 

- Emergency Unlocking Tool 

- Franka Hand (Not part of the certified machinery) 

R02210/1.3/EN 

Franka Robotics GmbH © 

45 

**Mounting** and installation 

- Cobot pump (Not part of the certified machinery) 

# **7 MOUNTING AND INSTALLATION** 



#### **WARNING** 

#### **Heavy equipment** 

Due to the dead weight and geometric design, lifting and handling the equipment may cause back injury, and, if it falls down, serious injury to fingers, hands, toes, and feet. 

- Always wear personal protective equipment (e.g., safety shoes) when transporting, mounting, or demounting the equipment. 

- Always lift the equipment with the help of a second person. 

- The equipment must be placed on even surfaces to prevent it from tilting or sliding. 

- Follow the company regulations on lifting loads and personal protective equipment. 

#### **_NOTICE_** 

Arm does not stand stable without being screwed at the base. 

#### **Overview of interfaces provided by Control and Arm** 



Figure 7.1: Overview of interfaces 

R02210/1.3/EN 

Franka Robotics GmbH © 

46 

**Mounting** and installation 

## **7.1 Unpacking the equipment** 



Figure 7.2: Packing 



Always keep the original packaging in case of relocating the robot. 

#### **Unboxing** 

Procedure 

1. Take off the top lid of the outer box. 

R02210/1.3/EN 

Franka Robotics GmbH © 

47 

**Mounting** and installation 



Figure 7.3: Unpack main carton 

2. Lift the top inner boxes and put them aside. 



Figure 7.4: Removal of individual cartons 

3. Pull the outer box apart to access the bottom inner box. 

R02210/1.3/EN 

Franka Robotics GmbH © 

48 

**Mounting** and installation 



Figure 7.5: Inner cartons 

#### **Unpacking the Arm** 

Procedure 

1. Carefully open the box by removing the sealing adhesive strips on top of the cardboard box. 

2. Open the foil coating. 

3. Remove the top protective layer. 



Figure 7.6: Open box from Arm 

4. Remove the middle protective layer. 

R02210/1.3/EN 

Franka Robotics GmbH © 

49 

**Mounting** and installation 



Figure 7.7: Unpack Arm 

5. Grasp the Arm at the indicated lifting positions carefully, lift it out of the bottom protective layer, and set it aside. 



Figure 7.8: Lift out Arm 

#### **Unpacking the Control** 

Procedure 

1. Carefully open the box by removing the sealing adhesive strips on top of the cardboard box. 

2. Open the foil coating. 

R02210/1.3/EN 

Franka Robotics GmbH © 

50 

**Mounting** and installation 

3. Remove the power cable and the top lid. 



Figure 7.9: Open box of control 

4. Remove the top protective layer. 



Figure 7.10: Removal packaging 

5. Grasp the Control at the indicated lifting positions, carefully lift it out of the bottom protective layer, and set it aside. 

R02210/1.3/EN 

Franka Robotics GmbH © 

51 

**Mounting** and installation 



Figure 7.11: Lift out  control 

## **7.2 Correct installation site** 

### **7.2.1 Maximum-and safeguarded space** 

#### **Classification of spaces** 



Figure 7.12: Classifcation of spaces 



R02210/1.3/EN 

Franka Robotics GmbH © 

52 

**Mounting** and installation 

- Maximum workspace 

   - Space that can be swept by the robot's moving parts plus the space which the end effector and the workpiece can sweep. 

- Safeguarded space Defined by the perimeter safeguarding (see graphic) 

#### **_NOTICE_** 

Utilize the provided safety functions to mitigate any risks of accidental collisions from an unexpectedly moving Arm. Monitoring functions are only triggered upon violation. The safety integrator must consider stopping times, distances, and tolerances. 

#### **_NOTICE_** 

Application-specific risk analysis may define a hazardous zone larger than the maximum workspace in some applications. 

### **7.2.2 Ambient conditions: Arm** 

#### **Permissible conditions at the site of installation** 

Ambient temperature 

- +15 °C to +25 °C (normal) 

- +5 °C to +45 °C (extended) 

- IP 20 

- Normal operations (no-derating): +15°C to +25°C, 60% not condensing humidity 

- Extended operations (no de-rating of safety system, de-rating of performance possible) : +5°C to +45°C, 90% not condensing humidity 

- Storage and transport: -10°C to +60°C 

Relative air humidity 

- 20 % to 80 %, non-condensing 

Site of installation 

- Indoors, in enclosed buildings 

- Not exposed to direct sunlight 

- No vibrations, no accelerating fundaments 

- Magnetic fields are only permissible in the stated specification range. 

#### **_<mark>Please refer to topic 4.2 Notice of liability in this Manual.</mark>_** 

#### Orientation of installation 

- Arm may only be installed vertically (base horizontal to the earth’s surface, no hanging Arm) 

Ambient medium 

- Air 

- Free from flammable substances (dust, gas, liquid) 

- Free from aggressive media 

R02210/1.3/EN 

Franka Robotics GmbH © 

53 

**Mounting** and installation 

- Free from corrosive substances 

- Free from flying objects 

- Free from spraying liquids 

- Free from pressurized air streams 

#### Pollution degree 

- Degree 2 (according to EN 60664) 

- Only dry, non-conductive pollution occurs; occasionally, temporary conductibility caused by condensation may occur 

#### Setup altitude 

- ≤ 2,000 m above sea level 

#### Electromagnetic compatibility 

- Environment conditions must adhere to general industrial equipment according to EN 61000-6-4 as the system is designed for respective emission tolerance according to EN 61000-6-2 

#### **_NOTICE_** 

In order not to endanger the safety functionality of the system, ensure pollution degree 2 according to EN 60664. 

#### **Adequate ventilation** 

#### **_NOTICE_** 

The heat produced by power electronic components and modules inside the Arm is dissipated via the Arm’s surface. 

- Install the Arm in an adequately ventilated place. 

- Do not expose the Arm to direct sunlight. 

- Do not repaint, paste up, or wrap up the Arm. 

#### **Ergonomic consideration** 

#### **_NOTICE_** 

To avoid overheating, the system will stop working when it exceeds the extended temperature range. The user will be informed through Franka UI. 

Follow further instructions in Franka UI. 

#### **_NOTICE_** 

To avoid overheating of the motors, the system will stop working, if the internal sensors detect excess temperatures in the windings. The user will be informed through Franka UI. 

Follow further instructions in Franka UI. 

R02210/1.3/EN 

Franka Robotics GmbH © 

54 

**Mounting** and installation 

**_NOTICE_** 

Install the Arm in an ergonomic teaching position. 

### **7.2.3 Ambient conditions: Control** 

#### **Permissible conditions at site of installation** 

Ambient temperature 

- +15 °C to +25 °C (normal) 

- +5 °C to +45 °C (extended) 

Relative air humidity 

- 20 % to 80 %, non-condensing 

#### Site of installation 

- Indoors, in enclosed buildings 

- Not exposed to direct sunlight 

- No vibrations 

- Magnetic fields are only permissible in the stated specification range. 

#### **_<mark>Please refer to topic 4.2 Notice of liability in this Manual.</mark>_** 

• Enclosure needs a minimum degree of protection corresponding to IP4X or IPXXD if located in places open to all persons. 

#### Orientation of installation 

- Device may only be installed horizontally on the earth’s surface 

- Mounting in angle brackets, e.g., under tables 

- Mounting in control cabinets (2U, 4HP) 

#### Power supply 

• In order to ensure stability and safety of the system, provide a stable power supply that maintains enough power to the control to shut down in a controlled fashion, when the power supply is shut off. 

#### Ambient medium 

- Air 

- Free from flammable substances (dust, gas, liquid) 

- Free from aggressive media 

- Free from corrosive substances 

- Free from flying objects 

- Free from spraying liquids 

- Free from pressurized air streams 

#### Pollution degree 

- Degree 2 (according to EN 60664) 

- Only dry, non-conductive pollution occurs; occasionally, temporary conductibility caused by condensation may occur 

R02210/1.3/EN 

Franka Robotics GmbH © 

55 

**Mounting** and installation 

Setup altitude: 

• ≤ 2,000 m above sea level 

**_NOTICE_** 

If it is not open to all persons, only pollution degree 2 is relevant and needs to be ensured. 

#### **_NOTICE_** 

In order not to endanger the safety functionality of the system, ensure pollution degree 2 according to EN 60664. 

The enclosure mentioned above is not suitable to protect from higher pollution degrees. Here, an even higher IP is needed. 

## **7.3 Preparing the Installation site** 

#### **Correct installation site** 

Before installation, prepare the installation site. 



#### **WARNING** 

**Malfunctions and unexpected motions due to improper installation** 

Risk of severe injury, such as crushing of fingers, hands, upper body, head. 

- Only switch on the robot when the Arm is properly installed on the platform. 

- Only install the Arm on even, unmoving, and stable platforms. Accelerations and vibrations induced by the platform are not permissible. 

- Do not install the Arm hanging or on tilted or uneven platforms. 

- Level the platform and install the robot in an upright position. 

- Tighten the screws after 100 hours of operation with the correct tightening torque. 

### **7.3.1 Arm** 

#### **Derating** 

When operating Franka Research 3 within the extended temperature range, the user may need to reduce the dynamic parameters (acceleration, maximum speed, etc.) to avoid overheating the system and its components. Otherwise, Franka Research 3 stops its operation. 

#### **Stable platform** 

The Arm is equipped with highly sensitive sensor technology and fine-tuned control algorithms. The control algorithm requires installation on a stable, leveled, non-moving, and non-vibrating platform in an upright position. The maximum permitted tilt angle is 0.1°. 

The following maximum forces must be supported during static and dynamic operation from mounting base: 

- tilting torque: 280 Nm 

R02210/1.3/EN 

Franka Robotics GmbH © 

56 

**Mounting** and installation 

- torque around axis: 190 Nm 

- horizontally force: 300 N 

- vertical force: 410 N 



Figure 7.13: Preparing the baseplate 



#### **Preparing the baseplate** 

Required material 

- Detailed mounting layout for baseplate 

Procedure 

- Use the technical drawing for positioning the holes. 

**_NOTICE_** 

NOTICE the position of the Arm in the technical drawing and align it on the baseplate accordingly. 

The hole spacing is designed to be compatible with flexible assembly parts by ITEM. Two holes (Ø 6 mm H7) for dowel pins in the mounting flange allow for accurate, repeatable assembly of the Arm using 2 x Ø6 h8 pins (see table in chapter 7.4 “Mounting the Arm”). 

R02210/1.3/EN 

Franka Robotics GmbH © 

57 

**Mounting** and installation 



Figure 7.14: Drilling template 

<mark>1</mark> Front <mark>3</mark> Thread for functional earth M5 <mark>2</mark> Holes for M8 screws <mark>4</mark> Holes for alignment pins Ø6H7 

### **7.3.2 Control** 

#### **Installation site** 

Place the Control horizontally in its intended location. 

Alternative: 

Install the Control in a rack designed for 19-inch equipment. 

**_<mark>For further information, please refer to chapter 7.2 Correct installation site in this Manual.</mark>_** 

#### **_NOTICE_** 

The power supply connection must be established via suitable equipment, e.g., by using the supplied countryspecific cable. 

Make sure that the main supply and main switch are easily accessible. 

#### **Adequate ventilation** 

#### **_NOTICE_** 

The heat produced by power electronic components and modules inside the Control is dissipated through an internal ventilation system. 

- Install the Control in an adequately ventilated place. 

- Do not expose the Control to direct sunlight. 

- Place the Control at a sufficient distance between the front/back fans and covering components (40 mm on both sides). 

- Make sure that the Control's fans are not covered with dirt. 

R02210/1.3/EN 

Franka Robotics GmbH © 

58 

**Mounting** and installation 



#### **WARNING** 

#### **Heavy equipment** 

Due to the dead weight and partly due to the geometric design, lifting and handling the equipment may cause back injury and, if it falls, serious injury to fingers, hands, toes, and feet. 

- Always wear personal protective equipment (e.g., safety shoes), when transporting, mounting, or demounting the equipment. 

- The equipment must be placed on even surfaces to prevent it from tilting or sliding. 

- Follow the company regulations on lifting loads and personal protective equipment. 

## **7.4 Mounting the Arm** 

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
|**Other**|||Only use ITEM 0.0.420.83 Heavy<br>Duty T-Slot M8 Nuts.|



#### **_NOTICE_** 

#### **Material damage to the Arm** 

Moving the Arm by force in a locked state will lead to a momentary slipping of internal parts which causes loss of calibration and damage to the Arm. 

- Handle, lift, and transport the Arm only at the points indicated in this manual to avoid overstressing the joints of the Arm. 

- The Arm is to be handled gently even when set up and switched on or off. 

R02210/1.3/EN 

Franka Robotics GmbH © 

59 

**Mounting** and installation 

#### **_NOTICE_** 

Make sure that the maximum forces and torques are supported during static and dynamic operation. For more information. 

**_Please refer to chapter 7.3 Preparing the installation site in this Manual._** 

#### Precondition 

- Two people are required for mounting the Arm. 

- Prepared baseplate. See section Preparing the Baseplate in chapter 7.3 “Preparing the Installation site”. 

Procedure 

1. Lift the Arm. 

2. Carry the Arm to its designated position. 

3. Align the Arm accordingly to the pre-fixed holes on the baseplate. 

4. Person 1: Hold the Arm. 

   - Person 2: Use the four screws to mount it to the baseplate with a tightening torque of 30 Nm. 



Figure 7.15: Mounting of the Arm 

5. Connect the functional earth to the base of the Arm. 

_The Arm is successfully mounted to the baseplate._ 

|**_NOTICE_**|
|---|



The Arm should not be powered until correct mounting is validated again. 

R02210/1.3/EN 

Franka Robotics GmbH © 

60 

**Mounting** and installation 

## **7.5 Positioning the Control** 



#### **WARNING** 

#### **Heavy equipment** 

Due to the dead weight and partly due to the geometric design, lifting and handling the equipment may cause back injury and, if it falls, serious injury to fingers, hands, toes, and feet. 

- Always wear personal protective equipment (e.g., safety shoes), when transporting, mounting, or demounting the equipment. 

- The Control must be placed on even surfaces to prevent it from tilting or sliding. 

- Follow the company regulations on lifting loads and personal protective equipment. 

#### **_NOTICE_** 

**Material damage to Arm and Control** 

Moving the Arm by force in a locked state will lead to a momentary slipping of internal parts which causes loss of calibration and damage to the Arm. 

- Avoid shocks. 

- Carefully set down the devices. 

- Always store and transport the devices in their original packing, even inside buildings. 

#### **Positioning** 

#### Procedure 

1. Person 1: Grasp the Control at the indicated lifting positions. 

2. Person 2: Remove the foam packaging from the Control. 

3. Place the Control horizontally in its designated position and ensure that proper ventilation is provided. Alternative option: 

Attach the Control in a rack designed for 19-inch units. 

**_<mark>Please refer to topic 7.2 Correct installation site above in this chapter.</mark>_** 

R02210/1.3/EN 

Franka Robotics GmbH © 

61 

**Mounting** and installation 

## **7.6 Wiring and Electrical installation** 

#### **Sound condition** 



#### **DANGER** 

**Damaged wires or inadequate electrical installation** 

Risk of personal injury by electric shock, as well as material damage 

- Only use Franka Research 3 in sound technical condition. 

- Only install the emergency stop and safety peripherals system with qualified personnel. 

- Check cables and electrical installations. 



#### **CAUTION** 

- **Exposed wires and cables** 

- Operators may trip and fall due to exposed wires and cables in the maximum workspace. Therefore: • Always lay cables safely. 

**_NOTICE_** 

Only devices with galvanic isolation up to 60 V in the Ethernet port may be connected to the system. 

#### **_NOTICE_** 

Do not swap or unplug the connected Arm while the Control is powered on. 

R02210/1.3/EN 

Franka Robotics GmbH © 

62 

**Mounting** and installation 

## **7.7 Connecting to the robot interface** 

### **7.7.1 Connection diagram** 



Figure 7.16: Overview connection diagram 

### **7.7.2 Interfaces** 

#### **X3 - Safe inputs** 

Safe inputs (X3.n) always have two separate channels, designated A and B. Each channel is implemented via its p- and n-pins which have to be connected via a floating switch. During regular operation, both channels must be in the same state (open/closed) and not be connected; any other state will trigger a failure in the safety system. 

The safe inputs are galvanically isolated from the robot system and other interfaces at the robot, although all safe inputs share a common electrical domain, regardless of their interface connector. 

Interface X3 is located at the base of the robot arm and carries three safe input signals. X3.1 provides the emergency stop integration of the robot, X3.2 and X3.3 provide two freely configurable safety inputs. The connector is a female 12-pin M12 connector with A coding. 

Safe Inputs electrical domain characteristics for X3: 

- signal voltage 24 V; signal current 30mA 

R02210/1.3/EN 

Franka Robotics GmbH © 

63 

**Mounting** and installation 



Figure 7.17: X3 - Safe Inputs 

#### **X4 - External enabling** 

Interface X4 is located at the base of the robot arm and carries one safe input signal. The connector is a female 4-pin M12 connector with A coding. This connector is intended for the temporary connection of the External Enabling Device during operating phases when this is required. 

If possible, always use the external enabling device supplied. 

#### **_Notice_** 

If a separate external enabling device is to be used, the external enabling device must comply with IEC 60204 1 and DIN EN 60947 5 8. 

#### **X5 - Robot network** 

The X5 connector is located on the robot base and provides the internal robot network via an Ethernet socket. The robot network has an integrated DHCP server. The operating device can be connected to X5. By entering the URL robot.franka.de, you can access the Franka UI web interface of the robot. The IP address of the X5 interface can be configured in the settings. 

The default setting has the stored IP address 192.168.0/24. The robot can then be reached under the IP address 192.168.0.1. The DHCP server assigns addresses in the range 100 to 150 to the clients, i.e. with default settings 192.168.0.100 to 192.168.0.150. 

#### **X6 - End effector** 

Interface X6 is located at the wrist of the robot arm and carries signals from the robot connecting to the end effector. The connector is a Binder 8-pin female Snap-in IP67 Series 620. 

R02210/1.3/EN 

Franka Robotics GmbH © 

64 

**Mounting** and installation 



Figure 7.18: X6 interface 

- Nominal voltage 48 ± 3 VDC. 

- Nominal hold current 0.5 A at 25°C. 

- Maximal capacitive load 220 µF. 

The end-effector interface does not transmit any safety-related information. It provides neither discrete signals nor protocol-based safe data transfer. When SEEPO (Safe Electrical Power Off) is active, no 48 V power supply is available on this interface. Additionally, the end-effector supply does not include an earthing connection. 

If additional devices are connected, please test whether the intended function works as expected. 

#### **C2 Network connection** 

The C2 interface is located on the front of the control unit. It provides an Ethernet connection via which the control unit can be connected to a system/company network and also to the Internet. 

The network connection can be configured in the settings. The DHCP client is activated for this interface in the default settings. It is also possible to manually set the network connection for integration into an existing network. Please note that the robot network and the company network must not have an identical IP address range.Connecting the functional earth 

**_NOTICE_** 

It is required to connect the functional earth to meet the stated EMC levels. 

Required material 

- M5 screw thread 

- 1x tooth washer M5 

- Functional earth cable 

We recommend using a minimum 1.5 mm<sup>2</sup> section Cu cable, with a maximum length of 5 m. 

R02210/1.3/EN 

Franka Robotics GmbH © 

65 

**Mounting** and installation 



Figure 7.19: Connection the functional earth 

#### Procedure 

1. Connect the functional earth to the M5 thread of the Arm’s base at the indicated position on one side and to a nearby, well-grounded part (e.g., a solid metal grounding bar) on the other side. 

2. Position the tooth washer M5 at the indicated position at the Arm's base for the functional earth. 

3. Secure the cable lug of the functional earth cable with the M5 screw. 

4. Connect the other side of the cable to a nearby, well-grounded part (e.g., a solid metal grounding bar). 

#### **_NOTICE_** 

The electrical safety of the system does not depend on a functional earth connection. A functional earth connection is not suited to propagate protective bonding to attached equipment like end effectors. All equipment in the vicinity of the robot must be installed in accordance with their respective electrical requirements, including protective bonding, if applicable. 

### **7.7.3 Wiring** 

#### **_NOTICE_** 

The Arm connection cable, emergency stop cable, External Enabling Device cable, and user specific cabling shall not be extraordinarily subjected to the following: 

- Mechanical handling and dragging across rough surfaces (abrasion) 

- Operation without guides (kinking) 

- Guide rollers and forced guiding, being wound and re-wound on cable drums (stress) 

- High tensile stress, small radii, bending into another plane and/or frequent duty cycles 

#### **Connecting Arm to Control** 

Required material: 

- Connecting cable 

R02210/1.3/EN 

Franka Robotics GmbH © 

66 

**Mounting** and installation 

#### **_NOTICE_** 

Only connecting cables provided by Franka Robotics shall be used for electrical connection between Arm and Control. 

#### **Procedure** 

1. Carefully place the connector port (female site) onto the connector X1 and ensure that the triangular marking points upward. 



Figure 7.20: Connection of connecting cable  the Arm 

2. The plug itself is pulled into the connector port by turning the movable front part of the connector. 

3. Turn hand-tight and test correct fit by slightly pulling the plug. 

4. Apply the same principle to connect the other end of the connecting cable (male site) with the connector C1 on the front of the Control. 



Figure 7.21: Connection of connecting cable to the control 

#### **Connecting External Enabling Device** 

Required material: 

- External Enabling Device supplied 

Procedure 

1. Make sure that the guide pin is pointing in the right direction. 

2. External Enabling Device to the X4 connector. 

R02210/1.3/EN 

Franka Robotics GmbH © 

67 

**Mounting** and installation 



Figure 7.22: Connection of external Enabeling Device 

3. The plug itself is pulled into the connector port by turning the movable front part of the connector. 

4. Turn hand tight. 

#### **Connecting your operating device (for operation via Franka UI)** 

Required material: 

- Interface device 

- **_<mark>Please refer to the Chapter 3.1.1 Connecting a user interface device in the respective Operating Manual corresponding to your system version (e.g.,5.8.0).</mark>_** 

- Ethernet cable with RJ 45 connector (not included) 

#### Procedure 

- Connect your interface device and the connector X5 at the Arm base with the Ethernet cable. 



Figure 7.23: Connection of operating device 

R02210/1.3/EN 

Franka Robotics GmbH © 

68 

**Mounting** and installation 

#### **Connecting the Control with the power supply** 

#### **_NOTICE_** 

Make sure to connect the mandatory locking mechanism to the C14 connector on the power supply cable. 

**_NOTICE_** Allowed supply frequency: 50 − 60 Hz Supply voltage: 100 - 240 VAC Earth leakage: < 10 mA 

Required material: 

- Country-specific power cable 

Procedure 

1. Connect the power cable to the Control. 

2. Connect the power cable to the power supply. 

#### **Connecting protective devices** 

If you want to connect external safety devices to slow down the Arm and / or bring it to a standstill by means of category 1 or 2 stops (according to IEC 60204 1). 

**_<mark>Please refer to Chapter 4.7 Installation of safety peripherals above in this Manual.</mark>_** 



#### **WARNING** 

#### **Risk of injuries** 

Connecting external devices with a separate power supply may jeopardize the system safety functionality. Risk of severe injury, such as crushing, tearing of the skin, and puncturing from the Arm and end effectors. 

- Ensure that the voltages in the connected devices are either SELV or suitably isolated to systemconnected signals. 

#### **_NOTICE_** 

#### **Material damage** 

Connecting external devices with a separate power supply may cause system damage if not adhering to electrical ratings. 

- Voltages in connected devices must either be SELV or suitably isolated to system-connected signals. 

R02210/1.3/EN 

Franka Robotics GmbH © 

69 

**Mounting** and installation 

#### **_NOTICE_** 

**Material damage of cables** 

Improper handling of cables leads to damage to the cables. 

- Do not bend, fold, or roll the connection cable. 

- Lay the connection cable such that it will not be overstressed. 

#### **_NOTICE_** 

#### **Material damage of Arm or end effectors** 

Unsafe connection or disconnection of live cables or end effectors during operation leads to equipment damage. 

- Do not connect or disconnect cables when Franka Research 3 is connected to the power supply. 

- Do not connect or disconnect end effectors when Franka Research 3 is connected to the power supply. 

#### **Using the supplied emergency stop device** 

#### Required material 

- Supplied emergency stop device or customer-provided protective device (not included in scope of delivery) 

- When using a customer-provided protective device: an additional connecting cable (not included in scope of delivery) 

#### Procedure 

1. connect the supplied emergency stop device to the X3 terminal. 

or 

Connect the customer-specific configurated matching connector to the X3 connection and the protective devices to be connected (not included in the scope of delivery). Connect the protective device to the X3 connector. 



Figure 7.24: Connection of the protective device (here emergency stop command device 

2. The plug itself is pulled into the connector port by turning the movable front part of the connector. 

R02210/1.3/EN 

Franka Robotics GmbH © 

70 

**Mounting** and installation 

3. Turn hand-tight 

**_<mark>For more information on safe input, please refer to Chapter 4.10 Safety Functions section ‘Safe input’’ in this Manual.</mark>_** 

**_<mark>For more information, please refer to Chapter 4.7 Installation of safety peripherals in this Manual.</mark>_** 

**_NOTICE_** 

Safety devices need to be checked for proper functioning before initial operation and at regular intervals. 

## **7.8 Mounting End Effectors** 



**WARNING** 

**Falling and/or flying tools from the end effectors** Tools that remain inserted in the end effector may turn into projectiles during later motions of the Arm and lead to injuries. 

- Do not leave any tools inside the robot. 



#### **CAUTION** 

**Sharp-edged, pointed designs and moving parts** 

- Attached end effectors may cause injuries to hands, fingers, upper body, and head. 

- Always wear personal protective equipment (e.g., safety goggles). 

- The integrator needs to perform a risk assessment of any attached end effector. 

- Do not stand in the maximum workspace during operation. 

#### **_NOTICE_** 

Connecting external devices with a separate power supply may jeopardize the system’s safety function if it does not adhere to electrical ratings. 

In addition, the voltages in the connected devices must either be SELV or suitably isolated from systemconnected signals. 

**_<mark>The information on the end effector flange can be found in Chapter 7.3.1 ‘Arm’ in this Manual.</mark>_** 

**_NOTICE_** 

Note that the pilot grip has a 45° twist to the end effector flange. 

#### **Interface X6 - End effector** 

The X6 electrical connection on the end effector flange can be used to supply power to the end effector if required and to communicate with the controller via the can bus. NOTICE that the X6 connection has been configured 

R02210/1.3/EN 

Franka Robotics GmbH © 

71 

**Mounting** and installation 

specifically for Franka Hand and other devices may not be compatible with this connection. If an end effector is to be coupled that cannot be directly connected to such a port, external wiring for power supply and control of the end effector can be designed and implemented accordingly. 

**_<mark>For detailed description of the wiring of interface X6 please refer to Chapter 7.6 Wiring and electrical installation in this Manual.</mark>_** 



#### **CAUTION** 

**Opening and closing end effectors** 

- Malfunctions of the Control may lead to an unexpected opening and closing of end effectors **.** 

- Always wear personal protective equipment (e.g., safety goggles). 

- The integrator must perform a risk assessment on any attached end effector. 

- Do not stand in the maximum workspace during operation. 



#### **CAUTION** 

#### **Moving Arm** 

- Risk of severe injury, such as crushing, tearing of the skin, and puncturing 

- Always wear personal protective equipment (e.g., safety goggles). 

- The integrator must perform a risk assessment on any attached end effector. 

- Do not stand in the maximum workspace during operation. 

After connecting an end effector, a risk assessment needs to be performed. The risk assessment depends on the end effector and includes but is not limited to the following: 

- Sharp-edged or pointed end effectors 

- Movement or rotation of sharp rotating end effectors 

- Unexpectedly moving Arm leading to the end effector impacting or crushing a human 

#### **_NOTICE_** 

An additional risk assessment is required for risks of a possible end effector failure. The failure risk assessment depends on the end effector and includes but is not limited to the following: 

- Malfunction of the protective stop signal leading to not stopping of the end effector opening/closing 

- Evaluation of power-loss of the end effector and its functions 

- Control failures leading to unexpectedly opening/closing of the end effector 

R02210/1.3/EN 

Franka Robotics GmbH © 

72 

**Mounting** and installation 



For information on mounting and de-mounting the end effector, please see the respective end effector manual. 

## **7.9 Practical Tips for Usage and Positioning of Franka Research 3** 

### **7.9.1 Energy consumption** 

For standard operation, Franka Research 3 requires an average electrical power of 140–350 W. Temporarily, electrical power of up to 600 W can be drawn from the power supply. 

**_NOTICE_** 

In case of an unexpected power loss, Franka Research 3 attempts a Cat. 1 Stop. If the stored energy does not suffice, a Cat. 0 Stop will be performed. 

After an emergency stop, the Arm could have lost calibration or been damaged. If malfunctions are detected at the next start-up, the user will be informed and should follow the instructions in Desk. 

### **7.9.2 ESD limits** 

**_NOTICE_** 

It is required to connect functional earth to meet stated EMC levels. 

R02210/1.3/EN 

Franka Robotics GmbH © 

73 

**Mounting** and installation 



Figure 7.25: Measuring points ESD measurement 

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

|**_NOTICE_**|
|---|



It is recommended to check the distances according to the application requirement and the DIN EN 61340-5-1 standard. 

R02210/1.3/EN 

Franka Robotics GmbH © 

74 

**Mounting** and installation 

### **7.9.3 Design of the workspace** 



#### **WARNING** 

**Unexpectedly moving Arm** 

Risk of severe injury, such as crushing of fingers, hands, upper body, head. 

- Do not have sharp edges in the maximum workspace. 

- Do not keep any pointed objects in the maximum workspace. 

- Install the Arm in an ergonomic teaching position. 



Figure 7.26: Design of the workspace 

When planning the installation, ensure that there is sufficient free workspace around the robot. 

#### **_NOTICE_** 

For recovery procedures in the event of a failure, it may be necessary to move the joints to the reference positions of the Arm. It is therefore recommended to consider the position shown below in the setup planning so that the robot can reach the reference position if needed. 



Figure 7.27: Joint reference position of the Arm 

R02210/1.3/EN 

Franka Robotics GmbH © 

75 

**Mounting** and installation 

**_NOTICE_** 

**_In case of joint position errors please refer to Chapter Troubleshooting 8.1.4 and 8.1.5 in the appropriate version of the Operating Manual based on your installed system (e.g., v5.8)._** 

### **7.9.4 Personal safety and ergonomics** 

#### **Free space for retracting** 

#### **_NOTICE_** 

The following information on how to use and place the Arm are practical tips and may not be exhaustive when it comes to a specific application. They do not replace a hazard and risk assessment but may suggest layout options. 

Humans instinctively retract from unexpected motions. Therefore, the area where the operator or other persons stand should allow for sufficient space to retract or recoil. 

Furthermore, ensure that this space is free of obstacles (e.g., cables, objects) to prevent people from tripping over them and harming themselves. 

#### **Greatest possible distance to the Arm** 



#### **WARNING** 

#### **Moving Arm** 

- Risk of being trapped by the Arm. 

- Keep the Arm at the greatest possible distance at any given time to allow the operator to react and retract. 

- Do not operate the Arm while embracing it. 

- Do not place your head or other body parts between or underneath segments of the Arm. 

- Do not place body parts (especially hands, fingers) between the Arm, the end effector, or stationary objects. 

- In case of acute mortal danger: 

   1. Press the Emergency Stop Device to stop the robot from operating. 

   2. Pull or push the Arm out of the dangerous position manually. 



Figure 7.28: Distance to Arm bumping the head 

R02210/1.3/EN 

Franka Robotics GmbH © 

76 

**Mounting** and installation 



Figure 7.29: Distance to Arm bumping 



Figure 7.30: Distance to Arm squeezing the hand 

#### **Eye protection** 



#### **WARNING** 

#### **Unexpected movement of Arm and leaking oil** 

Contact with leaking oil may cause eye or skin irritation. 

The use of various applications, the handled end effectors, and surrounding objects may lead to crushing, tearing of the skin, and puncturing. 

- Always wear protective goggles. 

#### **Clothing and jewelry** 



#### **CAUTION** 

#### **Loose clothing or jewelry getting caught in Arm** 

Caught clothing or jewelry may cause imbalance and the risk of falling personnel. 

- Do not wear loose clothing or clothing with ribbons 

- Do not wear loose jewelry, e.g., necklaces or bracelets. 



Figure 7.31: Protective equipment (do not wear jewellery) 

#### **Further information** 

Corrosion might appear on visible surfaces. This does not affect the functionality of the robot. 

R02210/1.3/EN 

Franka Robotics GmbH © 

77 

**USAGE** 

#### **_NOTICE_** 

The following information is practical and may not be exhaustive when it comes to preventing rust. In the event of rust, Franka Robotics assumes no warranty or liability, since rust does not impair the function. 

- Ensure compliance with humidity and temperature ranges during use, transport, and storage. 

- Store the robot in moisture-reducing materials, for example with drybags. 

- Only work with clean and dry hands especially during handling, installation, and when teaching a task. 

- Sealing it with adhesive strips 

# **8 USAGE** 

## **8.1 Switching On** 



#### **DANGER** 

**Short circuit due to developed condensation when the device is transported from colder to warmer and more humid surroundings** 

- Risk of life-threatening injuries due to electrical shock. 

- Leave devices to acclimatize after transport. 

- Do not switch on wet devices. 

#### Precondition 

- Cables need to be plugged in correctly. 

- The external power supply must be connected. 

- Leave the maximum workspace. 

#### Procedure 

1. Switch on Control. 

R02210/1.3/EN 

Franka Robotics GmbH © 

78 

**USAGE** 



Figure 8.1: Switching on Control 

_Control is now switched on._ 



Figure 8.2: Blue status lights on Arm 

You can observe the following sequence: 

- The cooling system will be activated and is visible and audible. 

- Booting up may take approximately 1 minute. 

R02210/1.3/EN 

Franka Robotics GmbH © 

79 

**USAGE** 

- The status lights on the Pilot and both sides of the base will start to flash. 

- After boot-up is complete, the status light will be continuously blue, indicating that the robot is in a stopped state in Execution mode. 

   - If the status light flashes red, there exists a safety error. Then check whether the emergency stop is enabled or whether the Emergency Stop device has been correctly connected to input X3. 

- The fail-safe locking system is active. The joints are still mechanically locked. For information on unlocking the fail-safe locking system, see section Pre-guiding in the event of a malfunction, **_<mark>please refer to Chapter 10 Maintenance and Disposal in this Manual.</mark>_** 

## **8.2 Safety Relevant Tests of Franka Research 3** 

### **8.2.1 Self-test of the robotic system** 

The self-tests of Control are executed while the system is running. The Arm is power cycled once to execute the selftests of the Arm. 



#### **WARNING** 

**Risk of injury due to falling objects** 

During the power cycle of the Arm, the power to the end effector is removed. Objects may fall from the end effector which could lead to injury. 

- Remove all objects from the end effector. 

- Move out of the hazard zone. 

#### **_NOTICE_** 

Every 24 hours, the user must initiate a safety diagnostic to detect potentially dangerous failures during operation. In the sidebar, the system will warn the user 2 hours before the time is exceeded. 

If the time is exceeded, the robot will stop all operations and request the user to initiate the self-test. For this purpose, a message appears from which you can start the self-test. 

You can also start the self-test manually at any time. To do this, proceed according to the following steps 

1. Start Franka UI on your Interface device. 

2. Go to “Settings”. 

3. Change to “Dashbord” 

4. Click on Button “EXECUTE” next to the display of the countdown to the self-test 



#### **WARNING** 

**Falling objects from end effectors due to a power supply cut off when SEEPO configuration is active** 

Risk of severe injury, such as crushing, tearing of the skin, and puncturing from the Arm and end effectors. 

- Always wear personal protective equipment (e.g., safety shoes). 

R02210/1.3/EN 

Franka Robotics GmbH © 

80 

**USAGE** 

- Use the appropriate type of end effector to prevent objects from falling. 

- Consider the shape, texture, and weight of the grasped objects in the risk assessment according to 102182. Using lightweight and/or round objects may reduce risks significantly. 

### **8.2.2 Regular testing of safety functions** 

The function of some safety functions must be tested regularly. This applies to the following safety functions: 

|**Safety function**|**Test**|
|---|---|
|Emergency Stop Device|1. Press the Emergency Stop Device while the robot is not active.<br>2. Check whether the brakes are locked.|
|Guiding Enabling Device|1. Release the Pilot-Grip´s Enabling Button while guiding.<br>_The robot must stop._<br>2. Fully press the Pilot-Grip´s Enabling Button while guiding.<br>_The robot must stop._|
|External Enabling Device|1. Release the enabling button of the External Enabling Device while testing a task.<br>_The robot must stop._<br>2. Fully press the enabling button of the External Enabling Device while testing a task.<br>_The robot must stop._|
|Any switch connected to X3.2 or X3.3|1. Activate switch.<br>2. Check if configured safety function is triggered accordingly.|



#### **SAFETYINSTRUCTION** 

- Activate the emergency stop system during start-up every 12 months. 

- Reconnect the emergency stop system during start-up every 12 months. 

- Check all safety installations, e.g., emergency stop system, for function every 12 months. 

- Check any additional safety measures that have been taken to secure safe operation. 



For more information on the emergency stop system, **_<mark>please refer to Chapter 4.7 Installation of safety peripherals in this Manual.</mark>_** 

### **8.2.3 Testing the emergency stop** 



#### **WARNING** 

**Risk of severe injury due to a non-operating Emergency Stop Device** 

Using a non-operational Emergency Stop Device to stop an operation in case of an emergency may lead to staying trapped which leads to severe injuries, such as crushing, tearing of the skin, and puncturing from the Arm and end effectors. 

- Store the Emergency Stop Device in a safe place. 

R02210/1.3/EN 

Franka Robotics GmbH © 

81 

**USAGE** 

#### **_NOTICE_** 

#### **Material damage** 

The end effector, workpieces, or the surroundings can be damaged, when the device is stopped at an unfavorable point in the process. 

- Only use the emergency stop in safety-critical situations. 

#### **_NOTICE_** 

Any damage occurring to the Arm when the emergency stop is pressed will not cause harm to persons, as the Arm will safely stop regardless of damage. 

#### **_NOTICE_** 

After an emergency stop, the Arm could have lost calibration or been damaged. If malfunctions are detected at the next start-up, the user will be informed. 

#### **_NOTICE_** 

Take other installed devices apart from Franka Research 3 into account that will be switched off by the emergency stop as well. 

#### **Precondition** 

- Franka Research 3 must be at standstill with no task running. 

- The locking bolts of the fail-safe locking system must be open. 

- The Arm may not move. 

#### **Procedure** 

1. Clear the space around the Arm to avoid any damage to grasped objects or surroundings. 

2. Use the guiding to bring the Arm into a position that is free from obstacles, e.g., 200 mm above stationary objects. 

3. Activate the emergency stop. 

The Arm will slightly lower with a clicking noise when falling into the mechanical locking bolts. 

#### **_NOTICE_** 

**_For detailed instructions please refer to the Operating Manual, Chapter 2.1 Initial Connection in the respective Operating Manual corresponding to your system version (e.g., 5.8)._** 

R02210/1.3/EN 

Franka Robotics GmbH © 

82 

**USAGE** 

## **8.3 Switching off and restarting** 



#### **WARNING** 

**Falling objects from end effectors due to a power supply cut off** 

- Objects falling from the gripper lead to injuries to hands, fingers, feet, and toes. 

- Always wear personal protective equipment (e.g., safety shoes). 

- Use the appropriate type of grippers to prevent objects from falling. 

- Consider the shape, texture, and weight of the grasped objects in the risk assessment according to 102182. Using lightweight and/or round objects may reduce risks significantly. 

#### **Shutting down** 

#### **_NOTICE_** 

The system is only completely shut down when the fans stopped running. Still running fans indicate that Franka Research 3 has not been completely shut down yet. Repeat the Safety Instructions of Shutting down Franka Research 3. 

#### **SAFETYINSTRUCTION** 

Procedure 

1. Move out of the hazard zone. 

2. In Franka UI, navigate in user menu to “Shut-down” and click on it. _The fail-safe locking system is activated. Franka Research 3 will shut down._ 

#### **Restarting** 

Turn off the system in Desk and wait for the fans to power down. Switch off the power switch on the Control. Wait one minute before restarting Franka Research 3 again. To restart Franka Research 3, switch on the power switch on the back of the Control. Franka Research 3 will start to reboot again. 

**_NOTICE_** 

To avoid unintentional repowering of the system, secure the connecting cable in a safe place. 

#### **Disconnecting Franka Research 3 from the power supply** 

#### Procedure 

1. Move out of the maximum workspace. 

2. Go to Franka UI. 

3. Select in User-Menu “Shut-down.” 

_The system shuts down._ 

4. Switch off the power switch on the backside of the Control. 

R02210/1.3/EN 

Franka Robotics GmbH © 

83 

**ROBOT** LED INDICATOR SYSTEM 

5. Pull the cable from the backside of the Control. 

**_NOTICE_** 

To avoid unintentional restarting of the system, stow the power cord in a safe place. 

_Franka Research 3 is disconnected from the power supply._ 

# **9 ROBOT LED INDICATOR SYSTEM** 

## **9.1 Overview of the status indicators** 

Status lights on both sides of the base take on the corresponding color, like a traffic light. The status lights will flash slowly during boot-up, when Franka Research 3 requires attention, or when the user enters values. The lights are lit in the corresponding color of the Franka Research 3 status during other processes. A circular status light in the middle of the Pilot-Disc indicates Franka Research 3’s status as well. 

When the operator is interacting with the Arm, the status light on the Pilot-Disc is switched off. 

**_<mark>For more information on the color behavior, please refer to Chapter 8.1 Switching On in this Manual.</mark>_** 



#### **WARNING** 

**Dangerous and uncontrolled motions of the Arm** 

- Risk of severe injury, such as crushing, tearing of the skin, and puncturing from the Arm and end effectors. 

- Ensure that the end effector and/or the object mass and the Center of Mass (CoM) are parameterized correctly. 

- Keep out of the workspace during operation. 

#### **_NOTICE_** 

The motion speed in Teach or Hand-Guiding Mode is pre-set. The speed can be reduced according to the risk evaluation of the Arm within its application. 

The robot uses six distinct LED colors to communicate its operational status. These lights can appear in two patterns: 

- **Solid (Static)** – indicating a stable state 

- **Blinking (Flashing)** – indicating a transitional or attention-required state 

LED indicators are visible in three key locations: 

- Desk Interface 

- Base of the Robot 

- Pilot-Disk 

R02210/1.3/EN 

Franka Robotics GmbH © 

84 

**ROBOT** LED INDICATOR SYSTEM 

Each color and pattern combination provides critical information about the robot’s current state and whether it is safe to interact with. These visual cues are designed to enhance operator awareness and safety. 

## **9.2 LED Activation Behavior** 

- **Base LEDs** : 

Always active. They continuously reflect the robot’s operational status and are the primary reference for system state. 

- **Pilot LEDs** : 

   - Only active during programming or manual guidance. They provide feedback specific to user interaction during these modes. 

#### **Startup Checklist for Operators** 

When powering on the robot, always: 

1. Verify that all indicator lights are functioning properly. 

2. Ensure the LEDs are clearly visible from your working position. 

3. Interpret the lights correctly to determine whether the robot is: 

   - IDLE or in TEACH mode 

   - Executing a Task 

   - In an error or warning state 

   - Awaiting user input 

#### **Important Safety Considerations** 

Whether it is safe to approach the robot in each state depends on the application-specific risk and hazard analysis and the configured safety scenarios. While LED indicators help identify the robot’s state, they are not certified safety functions. 

If in doubt, always use appropriate safety measures before approaching the robot: 

- Press the Emergency Stop 

- Activate a Protective Stop 

- Confirm the robot is in a safe state via the user interface 

## **9.3 Flashing Patterns** 

|**Pattern**|**Frequency**|**Meaning**|
|---|---|---|
|**Slow**<br>**Flashing**|~0.6 Hz (approximately 2 flashes<br>every 3 seconds)|Indicates a transition between states or a request for<br>user attention|
|**Fast**|~2 Hz (approximately 2 flashes per|Warns that motion is initiating, the robot is moving|
|**Flashing**|second)|slowly, or the system is updating|



R02210/1.3/EN 

Franka Robotics GmbH © 

85 

**ROBOT** LED INDICATOR SYSTEM 

#### **Error and Communication Loss** 

If a visual indicator or its controlling device detects a loss of communication, this is signaled as an error with a solid red light. 

## **9.4 LED Priority Logic** 

- The LED system always displays the most critical state. 

- If multiple events occur simultaneously, the color with the highest significance is shown. 

- Within the same priority level, only a one-color scheme is displayed at a time to avoid confusion. 

## **9.5 LED Color Reference Table** 

|**Category**|**LED**<br>**Color**|**LED**<br>**Pattern**|**Status Meaning**|**User Action**|
|---|---|---|---|---|
||White|Static|System idle or in TEACH mode.|Observe<br>standard safety<br>precautions before<br>approaching.|
|**Robot System**|||||
|**Status**|White|Slow<br>Flashing|Booting or shutting down.|Do not<br>interrupt. Wait<br>until complete.|
||White|Fast<br>Flashing|System updating.|Do not unplug<br>or interrupt. Wait<br>until complete.|
||Yellow|Static|Brakes locked/unlocked.|Used during<br>brake operations.|
|**Brakes**|Yellow|Slow<br>Flashing|Waiting for the boot to finish.|Wait until solid<br>yellow or next<br>instruction.|
||Yellow|Static|Warning state.|Do not<br>approach. Check<br>UI.|



R02210/1.3/EN 

Franka Robotics GmbH © 

86 

**ROBOT** LED INDICATOR SYSTEM 

|**Category**|**LED**<br>**Color**|**LED**<br>**Pattern**|**Status Meaning**|**User Action**|
|---|---|---|---|---|
|**Warnings**|Yellow|Slow<br>Flashing|Warning:<br>user<br>interaction<br>needed.|Check UI and<br>acknowledge<br>warning.|
||Red|Static|Severe<br>errors<br>(e.g.,<br>safety,<br>system, communication).|Do not<br>approach.<br>Investigate via UI.|
|**Safety Errors**|Red|Slow<br>Flashing|Safety violation or application<br>error.|Check UI.<br>Approach only if<br>safe and trained.|
||Red|Fast<br>Flashing|Error recovery in progress.|Wait or reset<br>via UI.|
||Red|Slow<br>Flashing|Input needed to recover from<br>error. Error recovery possible<br>with user input (e.g., joint limits<br>exceeded during hand-guiding)|Unlock joint or<br>reset to resume<br>operation.|
||Green|Static|Task executing autonomously.|Do not<br>approach. Robot is<br>moving.|
|**Execution**|Green|Fast<br>Flashing|Execution will begin shortly.|Do not<br>approach.<br>Execution<br>imminent.|
|**Collaborative**|Green|Slow<br>Flashing|Task active in assist mode.|Approach with<br>care. Follow safety<br>protocols.|



R02210/1.3/EN 

Franka Robotics GmbH © 

87 

**MAINTENANCE** AND DISPOSAL 

|**Category**|**LED**<br>**Color**|**LED**<br>**Pattern**|**Status Meaning**|**User Action**|
|---|---|---|---|---|
||Blue|Static|Execution phase ready. Brakes<br>engaged.|Approach with<br>care. Robots may<br>start moving.|
|**Execution**<br>**Mode**|Blue|Slow<br>Flashing|Brakes opening or<br>collaborative mode (no active<br>task).|Robot may<br>move slightly. Safe<br>to approach.|
||Blue|Slow<br>Flashing|Execution interrupted.<br>Awaiting feedback.|Provide<br>feedback to<br>resume. Robot<br>paused.|
||Magenta|Static|Conflicting input detected (e.g.,<br>manual guidance vs.<br>automation).|Do not<br>approach. Resolve<br>input conflict.|
|**Conflicts**|Magenta|Slow<br>Flashing|Input<br>needed<br>to<br>resolve<br>conflict.|Provide input<br>or guidance to<br>continue.|



# **10 MAINTENANCE AND DISPOSAL** 

## **10.1 Maintenance** 

The Arm and Control of the Franka Research 3 are designed for maintenance-free operation of approx. 20,000 hours under normal operating conditions. The normal operating conditions used as a basis were derived from various representative applications of the robot system and verified by analyses and tests. If a customer application deviates greatly from these underlying operating conditions, the duration may be extended or shortened under certain circumstances. 

If the system approaches this operating duration, contacting Franka Robotics support (support@franke.de) is recommended. Evaluation of the system's log data by the support team will then indicate any necessary action. 

R02210/1.3/EN 

Franka Robotics GmbH © 

88 

**MAINTENANCE** AND DISPOSAL 

#### **SAFETYINSTRUCTION** 

If damage to the structure of the robot is detected during a visual inspection, the robot must be taken out of service regardless of the current operating time. 

#### **SAFETY-** 

#### **INSTRUCTION** 

- Activate the emergency stop system during start-up every 12 months. 

- Reconnect the emergency stop system during start-up every 12 months. 

- Check all safety installations, e.g., the emergency stop system, for function every 12 months. 

- Check any additional safety measures that have been taken to secure safe operation. 

## **10.2 Cleaning** 



#### **DANGER** 

#### **Risk of electric shock** 

Improper use of liquid cleaning agents, as well as incorrectly disconnected devices from the power supply, can lead to fatal accidents. 

- Do not clean devices that have not been safely disconnected from the power supply. 

- Do not use liquid cleaning agents for cleaning the devices. 

The following things need to be kept in mind while cleaning: 

- Only qualified people may carry out cleaning. 

- Cleaning is only permissible when Franka Research 3 is safely stopped and disconnected from the power supply. 

- Switching off and disconnecting the device must be carried out by qualified people only. 

- Do not use any liquids to clean the device. 

- Do not use any cleaning chemicals. 

- The components may only be cleaned with dry cloth. 

- Moisture must not enter the device. 

- Do not apply great force to the Arm. The parts to be cleaned must be supported manually to not overload and possibly damage the Arm. 

#### **_NOTICE_** 

**Material damage to the devices** 

- Do not use liquid cleaning agents for cleaning the devices. 

R02210/1.3/EN 

Franka Robotics GmbH © 

89 

**TROUBLESHOOTING** 

## **10.3 Disposal** 

#### **Disposal** 

Disposal of Franka Research 3 must comply with the relevant country-specific laws, standards, and regulations. 

#### **Battery** 

The Control contains a coin cell battery. The cell battery must be disposed of separately according to the relevant country-specific laws, standards, and regulations. 

To remove the battery, open the Control. 

**_NOTICE_** 

Opening the Control is only allowed for the purpose of removing the coin cell battery when disposing of it. 

#### **Return of waste of packaging** 

Please contact Franka Robotics to return any used packaging. 

## **10.4 Mechanical exchange of Control** 

To replace the Control mechanically, proceed according to the following steps: 

- Perform a backup, if the defective Control still allows it. 

- Shut down the robot. 

- Switch off the Control at the main switch. 

- Disconnect the Control from the mains supply. 

- Disconnect the plug connection C1 (connection cable to the robot) as well as the network connection C2 at the Control. 

- Replace the defective Control with the replacement Control. Observe the required environmental conditions for the Control (see Chapter 10 "Assembly & Installation"). 

- Connect the robot's connection cable to the C1 plug connection on the Control. 

- Establish the network connection C2. 

- Connect the Control to the mains supply. 

- Connect your operating device to connector X5 on the robot base using an Ethernet cable. 

- Switch on the Control with the main switch. 

# **11 TROUBLESHOOTING** 

#### **Troubleshooting and Safety Error Reference** 

For a list of recoverable safety errors, **_<mark>please refer to Chapter 4.10 – Safety Functions in this Manual.</mark>_** 

For troubleshooting the following issues, **_<mark>please refer to Chapter Troubleshooting in the respective Operating Manual corresponding to your system version (e.g.,5.8)."</mark>_** 

- Loud clicking sound during shutdown 

R02210/1.3/EN 

Franka Robotics GmbH © 

90 

**TECHNICAL** DATA 

   - Joint limit error. 

   - Joint position error. 

   - Failed to unlock joints. 

   - Robot does not complete booting. 

   - Desk continuously displays “Shutting down the system”. 

   - Robot does not boot after turning on the Control. 

   - Unexpected stop followed by restart. 

- If recovery is unsuccessful, the issue may be due to hardware damage or a software malfunction. In such cases: 

   1. Shut down the system immediately. 

   2. Take the robot out of operation. 

   3. Contact your service partner or Franka customer support Contact: support@franka.de. 

#### **_NOTICE_** 

When contacting support, please provide the serial number of the Arm and the robot log files. You can download the log files via: Desk For detailed instructions, **_see Chapter 14.2 – Log Download in the respective Operating Manual (i.e. 5.8 or 5.9)._** 

# **12 TECHNICAL DATA** 

## **12.1 Technical specifications** 

For the latest datasheet on Franka Research 3 (Document Number: **R02212** ), please visit: 

- Link <u>https://franka.de/documents</u> 

- You will find the datasheet titled: 

   - **“FR3 Arm v2.1”** available in both English and German 

#### **_NOTICE_** 

The probability of failure per hour was evaluated at 40 °C. However, the safety rating holds for all functions within the temperature range, including the extended temperature range. 

If the system probability of failure per hour values are used for calculation, take the temperature into account. 

For more information on the probability of failure per hour, contact Franka Robotics at support@franka.de. 

R02210/1.3/EN 

Franka Robotics GmbH © 

91 

**TRANSPORTATION** AND HANDLING 

### **12.1.1 Ambient conditions for delivery and transport** 

The system can be stored and transported within the temperature range of -25 °C to +70 °C. 

# **13 TRANSPORTATION AND HANDLING** 



#### **WARNING** 

#### **Heavy equipment** 

Due to the dead weight and partly due to the geometric design, lifting and handling the equipment may cause back injury and, if it falls, serious injury to fingers, hands, toes, and feet. 

- Always wear personal protective equipment (e.g., safety shoes), when transporting, mounting, or demounting the equipment. 

- Always lift the equipment with the help of a second person. 

- The equipment must be placed on even surfaces to prevent it from tilting or sliding. 

- Follow the existing company regulations on lifting loads and personal protective equipment. 

#### **_NOTICE_** 

#### **Material damage to Arm, end effectors, and objects in the maximum workspace** 

Sensitive electromechanical components in the Arm and end effectors may be damaged if end effectors are connected to the Arm while bringing it into transport position. 

- Dismount any end effector and attachments before bringing the Arm into transport position. 

Do not leave loose objects in the maximum workspace. 



#### **DANGER** 

**Material damage to Arm and Control** 

Mechanical shock may cause damage or loss of calibration of sensitive electromechanical components in the Arm and Control. Avoid shock. 

- Do not set down the devices roughly. 

- Always store and transport the devices in their original packing, even inside buildings. 

## **13.1 Procedure** 

To ensure the safe and secure movement of the Franka Research 3 robot, users must follow a three-step procedure. This process is critical to protect the robot from damage during handling, transport, or storage. 

#### **Precondition** 

- The end effector and attachments must be removed from the Arm. 

R02210/1.3/EN 

Franka Robotics GmbH © 

92 

**TRANSPORTATION** AND HANDLING 

- The robot needs to move freely without being encumbered by obstacles to adopt the transport pose. In case of obstacles in the robot cell, consider moving the robot closer to the transport pose via hand-guiding. 

The procedure consists of the following steps: 

### **13.1.1 Step 1. Transportation pose of the Arm** 

Before handling or transporting the robot, it must first be moved into a safe and compact configuration called the transport mode. 

To do this, use the “Move to pack pose” function found in the Settings menu of the Franka UI. This ensures that all joints are correctly positioned to minimize the risk of damage during lifting or packaging. 

<mark>For detailed instructions with images on how to prepare the robot for transport mode using the “Move to pack pose” function in Programming and Execution mode Settings in the Franka UI,</mark> **_<mark>please refer to Chapter 14.5 Transportation pose of the Arm in the respective Operating Manual corresponding to your system version (e.g., 5.8).</mark>_** 

After that, follow the handling and lifting and re-packing the Arm instructions described in the 13.1.2 and 13.1.3 of this manual. 

### **13.1.2 Step 2. Handling and lifting** 

Always lift the Arm in the positions intended for lifting (see graphic below) to not overstress the Arm joints during handling and lifting. In particular, the Arm may never be carried in the extended position with one person holding each end of the Arm. 



Figure 13.1: Lifting positions 

R02210/1.3/EN 

Franka Robotics GmbH © 

93 

**TRANSPORTATION** AND HANDLING 

#### **_NOTICE_** 

#### **Material damage to the Arm** 

- Moving the Arm by force in a locked state will lead to a momentary slipping of internal parts which causes loss of calibration and damage to the Arm. 

- Handle, lift, and transport the Arm only at the points indicated in this manual to avoid overstressing the joints of the Arm. 

- The Arm is to be handled gently even when set-up and switched on or off. 

#### **_NOTICE_** 

Do not step or lean on the Arm. 

#### **_NOTICE_** 

Pay attention to the weight. 

The weight of the Arm is approx. 18.2 kg 



#### **WARNING** 

#### **Heavy equipment** 

Due to the dead weight and geometric design, lifting and handling the equipment may cause back injury, and, if it falls, serious injury to fingers, hands, toes, and feet. 

- Always wear personal protective equipment (e.g., safety shoes) when transporting, mounting, or demounting the equipment. 

- The equipment must be placed on even surfaces to prevent it from tilting or sliding. 

- Follow the company regulations on lifting loads and personal protective equipment. 



#### **WARNING** 

**Damaged components** 

Electrical risks may lead to severe injury. 

- Check if the packaging is in sound condition and fulfils its protective function. 

- Check the cables, plugs, and mechanical housing for cracks and broken insulations. 

- Do not use damaged cables, plugs, and mechanical housing for operation. In cases of doubt, contact Franka Robotics. 

R02210/1.3/EN 

Franka Robotics GmbH © 

94 

**TRANSPORTATION** AND HANDLING 

#### **_NOTICE_** 

**Material damage to Arm and Control** 

Mechanical shock may cause damage or loss of calibration of sensitive electromechanical components in the Arm and the Control. 

- Avoid shock. 

- Carefully set down the devices. 

- Always store and transport the devices in their original packing, even for short-distance transport. 

#### **_NOTICE_** 

**Material damage to Arm, end effectors, and objects in the maximum workspace** Sensitive electromechanical components in the Arm and end effectors may be damaged if end effectors are connected to the Arm while bringing it into transport position. 

- Dismount any end effector before bringing the Arm into transport position. 

- Do not leave loose objects in the maximum workspace. 

### **13.1.3 Step 3. Re-packing the Arm** 

Precondition 

- The robot needs to be in the transport pose. 

Procedure 

1. Open the box. 

2. Grasp the Arm at the indicated lifting positions in twos and carefully put it inside the bottom protective layer. 



Figure 13.2: Lifting the Arm 

R02210/1.3/EN 

Franka Robotics GmbH © 

95 

**TRANSPORTATION** AND HANDLING 

3. Insert the middle protective layer. 



4. Insert the top protective layer. 



Figure 13.4: Closing the box 

5. Close the foil coating. 6. Close the box. 

R02210/1.3/EN 

Franka Robotics GmbH © 

96 

**APPENDIX** 

# **14 APPENDIX** 

## **14.1 Stopping Times and Distances** 

The following diagram shows the stopping times and stopping distances of axes 1 to 4 according to the requirement from EN ISO 10218-1. 

The following table illustrates the joint positions for the different extension states of the Franka Research 3. 



Figure 14.1: Illustration of extension states 

R02210/1.3/EN 

Franka Robotics GmbH © 

97 

**APPENDIX** 

## **14.2 Stop Category 0** 

The following table summarizes the maximum values of axes 1-4 for stop category 0. 

|Joint|max. stopping distance<br>[rad]|max. stopping time [s]|
|---|---|---|
|1|0.674|0.655|
|2|0.670|0.561|
|3|0.532|0.445|
|**4**|0.360|0.306|





Figure 14.2: Distance, Stopp Cat0 

R02210/1.3/EN 

Franka Robotics GmbH © 

98 

**APPENDIX** 



Figure 14.3: Time, Stop Cat0 

## **14.3 Stop Category 1** 

The following table summarizes the maximum values of axes 1-4 for stop category 1. 

|Joint|max. stopping distance<br>[rad]|max. stopping time [s]|
|---|---|---|
|1|0.675|0.625|
|2|0.667|0.561|
|3|0.538|0.794|
|**4**|0.354|0.313|



R02210/1.3/EN 

Franka Robotics GmbH © 

99 

**APPENDIX** 

### **14.3.1 Joint 1** 



Figure 14.4: Distance, Stopp Cat1, Joint 1 



Figure 14.5: Time, Stopp Cat1, Joint 1 

R02210/1.3/EN 

Franka Robotics GmbH © 

100 

**APPENDIX** 

### **14.3.2 Joint 2** 



Figure 14.6: Distance, Stopp Cat1, Joint 



Figure 14.7: Time, Stopp Cat1, Joint 2 

R02210/1.3/EN 

Franka Robotics GmbH © 

101 

**APPENDIX** 

### **14.3.3 Joint 3** 



Figure 14.8: Distance, Stopp Cat1, Joint 3 



Figure 14.9: Time, Stop Cat1, Joint 3 

R02210/1.3/EN 

Franka Robotics GmbH © 

102 

**APPENDIX** 

### **14.3.4 Joint 4** 



Figure 14.10: Distance, Stop Cat1, Joint 4 



Figure 14.11: Time, Stop Cat1, Joint 4 

## **14.4 Stop Category 2** 

The following table summarizes the maximum values of axes 1-4 for stop category 2. 

R02210/1.3/EN 

Franka Robotics GmbH © 

103 

**APPENDIX** 

|Joint|max. stopping distance<br>[rad]|max. stopping time [s]|
|---|---|---|
|1|0,674|0,655|
|2|0,670|0,561|
|3|0,532|0,445|
|4|0,360|0,306|



### **14.4.1 Joint 1** 



Figure 14.12: Distance, Stopp Cat2, Joint 1 



Figure 14.13: Time, Stopp Cat2, Joint 1 

R02210/1.3/EN 

Franka Robotics GmbH © 

104 

**APPENDIX** 

### **14.4.2 Joint 2** 



Figure 14.14: Distance, Stopp Cat2, Joint 2 



Figure 14.15: Time, Stopp Cat2, Joint 2 

R02210/1.3/EN 

Franka Robotics GmbH © 

105 

**APPENDIX** 

### **14.4.1 Joint 3** 



Figure 14.16: Distance, Stopp Cat2, Joint 3 



Figure 14.17: Time, Stopp Cat2, Joint 3 

R02210/1.3/EN 

Franka Robotics GmbH © 

106 

**APPENDIX** 

### **14.4.2 Time Joint 4** 



Figure 14.18: Distance, Stopp Cat2, Joint 4 



Figure 14.19: Time, Stopp Cat2, Joint 4 

R02210/1.3/EN 

Franka Robotics GmbH © 

107 

**APPENDIX** 

## **14.5 Response times** 

|**Input**|**Reaction time motor**|**Reaction time Safe**<br>**Output grip**|
|---|---|---|
|User input|42 ms|48 ms|
|Safety function violation|36 ms|42 ms|
||42 ms|48 ms|
|Central reaction – joint error|42 ms|48 ms|
|Central reaction – subordinate error|10 ms|–|
|Local reaction – joint error|10 ms|–|
|Local reaction – subordinate error|30 ms|36 ms|
|Reaction – Master  Control  error|||



## **14.6 Safe Position Accuracy** 

If any safety function, that is based on safe position measurement is used, a limited accuracy needs to be taken into account. 

Main contributing factors to be considered include, but are not limited to structural elasticity, mechanical tolerances, assembly tolerances, signal processing, sensor accuracy. 

The effect on the accuracy of these factors is strongly influenced by external forces, payload, dynamic state such as velocity and kinematic configuration (pose). 

Safe position accuracy needs to be considered while parameterizing the safety functions to be used in an application. How much of a margin needs to be used is highly dependent on the aforementioned factors, and therefore needs to be evaluated and validated individually. 

R02210/1.3/EN 

Franka Robotics GmbH © 

108 

**GLOSSARY** 

# **15 GLOSSARY** 

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



R02210/1.3/EN 

Franka Robotics GmbH © 

109 

**GLOSSARY** 

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



R02210/1.3/EN 

Franka Robotics GmbH © 

110 

**GLOSSARY** 

|**Naming**|**Description**|
|---|---|
|Guiding /<br>Hand-guiding|Guiding describes moving the robot by haptic interaction, e.g., to teach a new pose.|
|Guiding Button|The Guiding Button is located on the right of the Pilot-Grip. The Arm can be moved by<br>pressing the Guiding Button and half-pressing the Enabling Button.|
|Guiding Mode|Guiding modes ease guiding by locking or unlocking different directions or rotations in<br>space, e.g., moving the Arm in three directions. One can switch between guiding modes<br>using the Guiding-Mode Button on the Pilot-Grip or directly from Desk.|
|Hand/<br>Franka Hand|The Hand is an electrical two-finger parallel gripper and is optionally available. The Hand<br>can be used for Franka Production3, Franka Research 3, and mountings according to the<br>ISO flange design. The Hand is an end effector. It is not part of the certified machinery.|
|Integrator|The integrator is responsible for assembling the partly completed machinery into the final<br>machinery by combining the robot with other equipment or another machine, including<br>additional robots to form a machine system.<br>The integrator also conducts appropriate risk assessments to identify residual risks and to<br>eliminate and minimize them according to ISO 12100.<br>The integrator is responsible for the safety of the final application.|
|Interaction|Franka Research 3 is designed to be easily programmed and operated, and to learn and<br>relearn new Tasks quickly. When Franka Research 3 is in “monitored stop” mode or is being<br>guided (teaching mode), Franka Research 3’s base is white to indicate that the Arm is ready<br>for interaction.|
|Interface<br>device|The interface device, a commercially available PC, tablet, or NOTICEbook with a web<br>browser, is connected to the Arm base via an Ethernet cable. The Franka UI can be accessed<br>in a web browser via the interface device.|
|Low Voltage<br>Directive<br>2014/35/EC|The Low Voltage Directive (2014/35/EC), hereinafter referred to as Low Voltage Directive<br>(LVD), regulates the safety of electronically operated devices within the European<br>Economic Area, Switzerland, and Turkey.|
|Machinery<br>Directive<br>(2006/42/EU)|The Machinery Directive (2006/42/EG), hereinafter referred to as Machinery Directive or<br>MD, regulates a standardized level of protection to prevent accidents for machinery and<br>partly completed machinery within the European Economic Area, Switzerland, and Turkey.|
|Maximum<br>workspace|Space that can be swept by the robot's moving parts plus the space that the end effector<br>and the workpiece can sweep.<br>For further information, see section Maximum-and safeguarded space in chapter Correct<br>installation.|
|Operator|An operator is authorized to access Franka Research 3 and utilize the user interface Desk<br>to use Franka Research 3 within the limits defined by the responsible person and the<br>administrator.The operator is allowed to start, monitor, and stop the intended operation of<br>Franka Research 3. Within Desk, the “operator” role can be assigned to users. Operators<br>only have limited access to Desk.|
|Pilot|The Pilot is the user interface on the Arm for guiding and operating the Arm and/or Desk.<br>It includes the Pilot-Grip and the Pilot-Disc.|



R02210/1.3/EN 

Franka Robotics GmbH © 

111 

**GLOSSARY** 

|**Naming**<br>Pilot-Disc|**Description**<br>The Pilot-Disc is part of the Pilot and is used for interacting with the Arm and/or Desk.|
|---|---|
|Pilot-Grip|The Pilot-Grip is part of the Pilot and is used for manual guiding.|
|Pose|A pose is a combination of position and orientation in space.|
|Protective<br>Measures|Protective measures achieve risk reduction according to 3.19 of ISO 12100. They are<br>implemented and assessed by the following persons:<br>Designer and/or Integrator (inherently safe design, safeguarding, and complementary<br>protective measures, information for use)<br>Responsible person/Integrator (organization: safe working procedures, supervision, permit-<br>to-work systems; provision and use of additional safeguards; use of personal protective<br>equipment; training)|
|Responsible<br>person|The responsible person is responsible for compliance with occupational health regulations<br>and the operational safety ordinance. The responsible person for Franka Research 3<br>includes but is not limited to the entrepreneur, the director of the institute, the employer,<br>or a delegate responsible for the use of Franka Research 3.|
|RoHS Directive<br>2011/65/EU|The RoHS Directive (2011/65/EU), hereinafter referred to as RoHS Directive, restricts the<br>use of certain dangerous substances in electrical and electronic equipment within the<br>European Economic Area, Switzerland, and Turkey.|
|Safeguarded<br>space|The perimeter safeguarding defines the safeguarded space.<br>For further information, see section Classification of spaces in chapter Correct installation.|
|Safety rules|A safety rule consists of a parameterized safety function, optional activation conditions, and<br>a reaction to be carried out when the safety function is violated.|
|Safety<br>scenarios|A set of safety rules defined in Watchman covering a specific risk situation, e.g., the "Test &<br>Jog" scenario covering all rules for the Test & Jog mode.|
|Safety set-up|Definition of general safety-relevant settings such as safe input behavior or an end effector<br>collision model.|
|SEEPO|Safety function “Safe End Effector Power Off.” See chapter Safety functionalities for details.|
|Settings<br>interface|The Settings interface is a web browser accessible user interface to set non-safety-related<br>parameters of Franka Research 3, e.g., network settings, user roles, or passwords. It is part<br>of the software framework Franka UI.|
|Single Point of<br>Control (SPoC)|Single Point of Control (SPoC) is a functionality that allows only one user at a time to trigger<br>critical actions, i.e., edit system settings and Tasks or trigger active robot actions like<br>unlocking joints and running tasks.|
|SLD|Safety function “Safely limited distance.” See chapter Safety functionalities for details.|
|SLP-C|Safety function “Safely limited Cartesian Position.” See chapter Safety functionalities for<br>details.|
|SLP-J|Safety function “Safely limited joint angle.” See chapter Safety functionalities for details.|



R02210/1.3/EN 

Franka Robotics GmbH © 

112 

**GLOSSARY** 

|**Naming**|**Description**|
|---|---|
|SLS-C|Safety function “Safely limited Cartesian speed.” See chapter Safety functionalities for<br>details.|
|SLS-J|Safety function “Safely limited joint speed.” See chapter Safety functionalities for details.|
|SMSS|Safety function “Safely monitored standstill.” See chapter Safety functionalities for details.|
|Stopping<br>Distance|The stopping distance is the distance the Arm covers after a stop demand is received until<br>the Arm comes to a full stop.|
|Stopping Time|The stopping time is the time that passes after the stop demand is received, e.g., by the<br>emergency device, until the Arm comes to a full stop.|
|Task|A Task in Desk represents an entire automation routine. A Task consists of one or several<br>Apps.|
|Teaching|Teaching describes the process of parameterizing a Task and the contained Apps by<br>manually guiding the robot or end effector. This includes, among others, the teaching of<br>"poses" by guiding the robot to that poses.|
|Tracking Error|The actual motion of the Arm follows the target motion with a small deviation, a so-called<br>tracking error.|
|Watchman|Watchman is a web browser accessible user interface to set and visually validate safety-<br>related parameters of Franka Research 3, e.g., safety-related monitored speed or safety-<br>related monitored spaces. It is part of the Franka UI.|
|Web browser|A software application running on an interface device, serving as the Franka UI connection.<br>A web browser provides the environment for Desk, Watchman, and the Settings interface.<br>Examples include the following: Chrome, Edge, and Firefox.|



R02210/1.3/EN 

Franka Robotics GmbH © 

113 

**INDEX** 

# **16 INDEX** 

|Additionally Equipment ................................................ 46|
|---|
|Apps .................................................................................. 98|
|Arm ........................................................ 14, 36, 46, 51, 60|
|Manually Moving the Arm ....................................... 25|
|Unpacking the Equipment ........................................ 51|
|Cartesian .......................................................................... 29|
|Center of Mass (CoM) ................................... 20, 91, 102|
|Certificates ...................................................................... 11|
|Cleaning ......................................................................... 100|
|Connecting cable..................................................... 51, 70|
|Control ........................................... 15, 19, 35, 46, 50, 62|
|Desk ........................................................................... 38, 71|
|Disposal .......................................................... 12, 100, 101|
|Emergency ................................................................ 16, 19|
|Emergency Stop Device ........................................... 16|
|Emergency stop installation..................................... 24|
|Emergency unlock label ............................................ 14|
|Emergency Unlocking ............................................... 14|
|Emergency Unlocking Tool ...................................... 26|
|EMI Directive 2014/30/EU ....................................... 128|
|Enabling Button ..................................................... 88, 102|
|End effector ............................................. 44, 74, 81, 102|
|External Enabling Device ..........................16, 47, 67, 88|
|Fail-safe Locking System ..................................... 25, 102|
|FCC rule 47 CFR part 15 ............................................ 128|
|Franka ........................................................................ 7, 128|
|Franka Store .................................................................. 128|
|Franka UI ......................................................................... 23|
|Glossary ......................................................................... 127|
|Guiding<br>Guiding Button .................................................. 41, 102|
|Guiding-Mode Button ............................................... 41|
|Hand ................................................................... 39, 44, 48|
|Handling ......................................................... 81, 112, 113|
|Installation ...................................................19, 45, 48, 49|



|Preparing the Installation Site ................................. 60|
|---|
|Wiring and Electrical Installation ............................ 65|
|Integrator ......................................................................... 21|
|Intended Use ................................................................... 18|
|Interaction ....................................................................... 39|
|Interface Device ...................................................... 35, 47|
|Labeling on the Equipment .......................................... 14|
|Functional earth label................................................ 15|
|Grasping position label ............................................. 15|
|Low Voltage Directive 2014/35/EC ........................129|
|Machinery Directive 2006/42/EC.............................. 18|
|Maintenance .................................................................100|
|Maximum space ....................................... 57, 75, 85, 114|
|Misuse ....................................................................... 18, 21|
|Operator .......................................................................... 29|
|Pilot ............................................................................ 36, 39|
|Pilot-Disc ..................................................................... 39|
|Pilot-Grip ..................................................................... 39|
|Pilot-Mode .................................................................. 39|
|Ports .................................................................................. 66|
|C2 .................................................................................. 68|
|X1 .................................................................................. 42|
|X3 .................................................................................. 67|
|X4 .................................................................................. 67|
|X5 .................................................................................. 67|
|X6 .................................................................................. 68|
|Practical Tips for Usage and Positioning ................... 76|
|Protective Measures ..................................................... 19|
|Responsible person .......................................................... 7|
|Restarting ......................................................................... 90|
|RoHS Directive 2011/65/EU ...................................... 11|
|Safety ................................................................................ 17|
|Installation of Safety Peripherals ............................ 24|
|Safe inputs ................................................................... 29|
|Safe outputs ................................................................ 31|



R02210/1.3/EN 

Franka Robotics GmbH © 

114 

#### **INDEX** 

|Safeguarded space ..................................................... 56|
|---|
|Safety Functionalities................................................ 28|
|SEEPO .............................................................................. 30|
|Self-test ............................................................................ 86|
|Service and Support .................................................... 102|
|Single Point of Control (SPoC) .................................... 23|
|Site of installation ................................................... 57, 59|
|SLD .................................................................................... 31|
|SLP-J ................................................................................. 30|
|SLS-C ................................................................................ 29|
|SLS-J ................................................................................. 30|
|SMSS ................................................................................ 30|
|Stopping distance ........................................................... 25|
|Stopping functions ......................................................... 31|
|Category 0 stop .......................................................... 31|



|Category 1 stop .......................................................... 31|
|---|
|Category 2 stop .......................................................... 31|
|Stopping time .................................................................. 25|
|Stopping time and distances ............................ 114, 126|
|Switching Off ......................................................... 90, 108|
|Switching On ................................................................... 85|
|Task ............................................................................ 88, 99|
|Teaching .................................................................. 86, 102|
|Teaching a Task .............................................................. 86|
|Transport .................................................. 49, 82, 85, 112|
|Re-packing the Arm ................................................... 81|
|Unpacking .................................................................... 51|
|Troubleshooting ...........................................................102|
|User interface ................................................................. 39|



R02210/1.3/EN 

Franka Robotics GmbH © 

115 

**TABLE** OF FIGURES 

# **17 TABLE OF FIGURES** 

|Figure 3.1: Type label .................................................... 12|
|---|
|Figure 3.2: Emergency unlock label ........................... 12|
|Figure 3.3: Hot Surface label ....................................... 13|
|Figure 3.4: Functional earth label ............................... 13|
|Figure 3.5: Lifting position label .................................. 13|
|Figure 3.6: Type label external device ....................... 13|
|Figure 3.7: Type label emergency stop device......... 14|
|Figure 4.1: Connection Emergency Stop Device ..... 22|
|Figure 4.2: Emergency unlock ..................................... 24|
|Figure 4.3: Pushing away manually ............................ 25|
|Figure 5.1: Equipment overview ................................. 33|
|Figure 5.2: Overview Arm ............................................ 34|
|Figure 5.3: Reference Triangles .................................. 35|
|Figure 5.4: World Coordinate System Indicators .... 35|
|Figure 5.5: Base Alignment Marks.............................. 36|
|Figure 5.6: Pilot .............................................................. 37|
|Figure 5.7: Switching status Enabling Button .......... 38|
|Figure 5.8: Enabling Button ......................................... 38|
|Figure 5.9: Guiding Mode Button ............................... 39|
|Figure 5.10: Guiding Mode Button ............................ 39|
|Figure 5.11: Guiding Button ........................................ 39|
|Figure 5.12: Guiding Button ........................................ 40|
|Figure 5.13: Connection ports at robot base ........... 40|
|Figure 5.14: End effector flange ................................. 42|
|Figure 5.15: Dimensions and connection ports of<br>control .............................................................................. 42|
|Figure 5.16: Connection ports .................................... 43|
|Figure 6.1: Scope of delivery Arm .............................. 44|
|Figure 6.2: Scope of delivery Control ........................ 44|
|Figure 6.3: Scope of delivery devices ........................ 44|
|Figure 6.4: Scope of delivery Connecting cable ...... 45|
|Figure 7.1: Overview of interfaces ............................. 46|
|Figure 7.2: Packing ........................................................ 47|
|Figure 7.3: Unpack main carton .................................. 48|
|Figure 7.4: Removal of individual cartons ................. 48|
|Figure 7.5: Inner cartons .............................................. 49|



|Figure 7.6: Open box from Arm .................................. 49|
|---|
|Figure 7.7: Unpack Arm ................................................ 50|
|Figure 7.8: Lift out Arm ................................................. 50|
|Figure 7.9: Open box of control .................................. 51|
|Figure 7.10: Removal packaging ................................. 51|
|Figure 7.11: Lift out  control ........................................ 52|
|Figure 7.12: Classifcation of spaces ........................... 52|
|Figure 7.13: Preparing the baseplate ......................... 57|
|Figure 7.14: Drilling template ...................................... 58|
|Figure 7.15: Mounting of the Arm .............................. 60|
|Figure 7.16: Overview connection diagram ............. 63|
|Figure 7.17: X3 - Safe Inputs ....................................... 64|
|Figure 7.18: X6 interface .............................................. 65|
|Figure 7.19: Connection the functional earth .......... 66|
|Figure 7.20: Connection of connecting cable  the Arm<br>........................................................................................... 67|
|Figure 7.21: Connection of connecting cable to the<br>control .............................................................................. 67|
|Figure 7.22: Connection of external Enabeling Device<br>........................................................................................... 68|
|Figure 7.23: Connection of operating device ........... 68|
|Figure 7.24: Connection of the protective device<br>(here emergency stop command device .................... 70|
|Figure 7.25: Measuring points ESD measurement .. 74|
|Figure 7.26: Design of the workspace ....................... 75|
|Figure 7.27: Joint reference position of the Arm .... 75|
|Figure 7.28: Distance to Arm bumping the head..... 76|
|Figure 7.29: Distance to Arm bumping ...................... 77|
|Figure 7.30: Distance to Arm squeezing the hand .. 77|
|Figure 7.31: Protective equipment (do not wear<br>|
|jewellery) .......................................................................... 77|
|Figure 8.1: Switching on Control ................................ 79|
|Figure 8.2: Blue status lights on Arm ......................... 79|
|Figure 13.1: Lifting positions ....................................... 93|
|Figure 13.2: Lifting the Arm ......................................... 95|
|Figure 13.3: Packing the Arm ...................................... 96|
|Figure 13.4: Closing the box ........................................ 96|



R02210/1.3/EN 

Franka Robotics GmbH © 

116 

|**TABLE OF FIGURES**||
|---|---|
|Figure 14.1: Illustration of extension states ............. 97|Figure 14.19: Time, Stopp Cat2, Joint 4 ..................107|
|Figure 14.2: Distance, Stopp Cat0 ............................. 98||
|Figure 14.3: Time, Stop Cat0 ....................................... 99||
|Figure 14.4: Distance, Stopp Cat1, Joint 1 ............. 100||
|Figure 14.5: Time, Stopp Cat1, Joint 1 .................... 100||
|Figure 14.6: Distance, Stopp Cat1, Joint................. 101||
|Figure 14.7: Time, Stopp Cat1, Joint 2 .................... 101||
|Figure 14.8: Distance, Stopp Cat1, Joint 3 ............. 102||
|Figure 14.9: Time, Stop Cat1, Joint 3 ...................... 102||
|Figure 14.10: Distance, Stop Cat1, Joint 4 ............. 103||
|Figure 14.11: Time, Stop Cat1, Joint 4 .................... 103||
|Figure 14.12: Distance, Stopp Cat2, Joint 1 ........... 104||
|Figure 14.13: Time, Stopp Cat2, Joint 1 .................. 104||
|Figure 14.14: Distance, Stopp Cat2, Joint 2 ........... 105||
|Figure 14.15: Time, Stopp Cat2, Joint 2 .................. 105||
|Figure 14.16: Distance, Stopp Cat2, Joint 3 ........... 106||
|Figure 14.17: Time, Stopp Cat2, Joint 3 .................. 106||
|Figure 14.18: Distance, Stopp Cat2, Joint 4 ........... 107||



R02210/1.3/EN 

Franka Robotics GmbH © 

117 

**Error! Use the Home tab to apply Überschrift 1;PM Überschrift 1 to the text that you want to appear here.** 

Franka Robotics GmbH Koppstraße 20 81379 Munich Germany 

R02210/1.3/EN 

Franka Robotics GmbH © 

118 

