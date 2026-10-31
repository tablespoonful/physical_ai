> **[PDF を開く](<Datasheet Franka Research 3_R02212_1.4_EN_June 2026.pdf>)**
>
> PDF から自動変換した本文です。図は含まず、表は崩れている場合があります。安全や仕様の確認には PDF を使ってください。

# **<mark>FRANKA RESEARCH 3</mark>** 

**Datasheet** 



**Franka Research 3** 

Release Version: 1.4 (2026/06) Document number: R02212 

## **Datasheet**<sup>¹</sup> **Arm & Control** 

||A|RM||
|---|---|---|---|
|Degrees of freedom|7|Interfaces|•ethernet (TCP/IP) for visual intuitive|
|Payload|3 kg||programming with Desk|
|Maximum reach|855 mm||•safety-rated input for external enabling device<br>i|
|Force/Torque sensing|link-side torque sensor in all 7 axes||•2 configurable safety-rated inputs for<br>emergency stop devices, safeguards or other|
|Joint position limits|A1, A3: -166/166 deg||<br>protective devices (OSSD devices via external|
||A2: -105/105 deg||OSSD converter connectable)|
||A4: -176/-7 deg<br>A5: -165/165 deg||•hardware prepared for: 2x DI & 2x DO<br>(24V, isolated, EN 61131-2 type 3<br>characteristics, 100 Hz sampling rate)|
||A6: 25/265 deg||•Control connector|
||A7: -175/175 deg||•connector for end effector|
|Joint torque limits|A1-A4: ±87 Nm|||
||A5-A7: ±12 Nm|User Interfaces at the|•integrated safety-rated guiding enabling switch|
|Mounting flange|DIN ISO 9409-1-A50|Arm's Pilot Grip|•guiding button|
|Installation position|upright||•guiding mode selector|
|Weight|~ 17.8 kg|||
|Protection rating|IP40|User Interfaces at the|•status light|
|Ambient temperature ²|+5 °C to +45 °C|Arm's Pilot Disc|•Pilot mode selector|
|Air humidity|20 − 80 % non-condensing||•arrow keys, teach, confirm, delete|
|CON|TROL||PERFORMANCE|
|Controller size (19”)|355 x 483 x 89 mm (D x W x H)|Motion||
|Supply voltage|100 − 240 VAC|Joint velocity limits|A1-A4: 150 °/s|
|Mains frequency|50− 60 Hz||A5-A7: 301 °/s(at FCI use A6: 239 °/s)|
|Power consumption|~ 80 W|Cartesian velocity limits|<br>up to 2 m/s end effector speed|
|Active power factor correction (PFC)|yes|Pose repeatability³|<+/- 0.1 mm (ISO 9283)|
|Weight|~ 7 kg|||
|Protection rating|IP20|Interaction||
|Ambient temperature ²|+5 °C to +45 °C|Guiding force|~ 2.5 N|
|Air humidity|20 − 80 % non-condensing|Adjustable translational|stiffness<br>10 − 3000 N/m|
|Permitted mounting orientation|horizontal|Adjustable rotational sti|ffness<br>1 − 300 Nm/rad|
|Interfaces|•ethernet (TCP/IP) for internet|Monitored signals|joint position, velocity,|
||and/or shop-floor connection||torque cartesian position, force|
||•power connector<br>IEC 60320C14 (V-Lock)||ADD-ONS|
||•Arm connector|Fully integrated end effec|tors<br>•2-finger gripper|
|EXCL|USIVE||•Vacuum gripper|
|||Fieldbuses|•Modbus/TCP|
|Research interface|1kHz Franka Control Interface (FCI)||•OPC UA|



Copyright © Franka Robotics 

**Franka Research 3** 

Release Version: 1.4 (2026/06) Document number: R02212 

### SAFETY 

Certification EN ISO 13849-1:2015 safety of machinery - safety-related parts of control systems EN ISO 10218-1:2011 Robots and robotic devices - safety requirements for industrial robots Part1: Robots 

certified by TÜV SÜD RAIL 

certified by TÜV SÜD Product Service 

|Collaborative operation modes||
|---|---|
|Safety-rated monitored stop|fully integrated in PL d Cat. 3|
|Hand-guiding|fully integrated in PL d Cat. 3|
|Safety-rated speed and separation monitoring|realizable in combination with external protective devices up to PL d Cat. 3|
|Safety parametrization & validation||
|Watchman|user interface to set and validate safety-related parameters|
|User management|role based access management|
|Safety Functions||
|Emergency Stop (X3.1)|PL d / Cat. 3|
|External Enabling Device (X4)|PL d / Cat. 3|
|Enabling Button|PL d / Cat. 3|
|Two configurable safe inputs (X3.2 and X3.3)|PL d / Cat. 3|
|SLP-C: Safely limited Cartesian position<sup>**4**</sup>|PL d / Cat. 3|
|SLS-C: Safely limited Cartesian speed<sup>**5**</sup>|PL d / Cat. 3|
|SLS-J: Safely limited joint speed|PL d / Cat. 3|
|SLD: Safely limited distance|PL d / Cat. 3|
|SEEPO: Safe End Effector Power off|PL b / Cat. b|
|Stopping Functions||
|Category 0 stop|PL d / Cat. 3|
|Category 1 stop|PL d/Cat. 3|
|Category 2 stop|PL d / Cat. 3|
|Worst case safe Cartesian position accuracy<br>for stopping functions|50 mm|
|Safety values according to EN ISO 13849-1||
|PFH of PL d / Cat. 3 safety functions<br>(Probability of Failures per Hour)|< 1 × 10−7|
|PFH of PL b / Cat. b safety functions<br>(Probability of Failures per Hour)|< 1 × 10−7|



1. Technical data are subject to change. 

2. For more details see Product Manual Franka Production 3. 

3. Based on ISO 9283 (Annex A), specified values refer to a workspace of 0.4 x 0.4 x 0.4 m centered at [0.498, 0.0, 0.226] m, 

with the Z-Axis of the flange oriented parallel to earth-gravity and the elbow positioned upwards. 

4. For System Images < 5.10, FCI cannot control the robot while SLP-C is configured. 

5. For System Images < 5.10, FCI cannot control the robot while SLS-C is configured. 

Copyright © Franka Robotics 

**Franka Research 3** 

Release Version: 1.3 (2025/06) Document number: R02212 

### DIMENSIONS & WORKSPACE 



Copyright © Franka Robotics 

