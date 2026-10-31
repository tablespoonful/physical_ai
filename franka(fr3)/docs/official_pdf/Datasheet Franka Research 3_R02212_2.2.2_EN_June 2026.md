> **[PDF を開く](<Datasheet Franka Research 3_R02212_2.2.2_EN_June 2026.pdf>)**
>
> PDF から自動変換した本文です。図は含まず、表は崩れている場合があります。安全や仕様の確認には PDF を使ってください。

# **Datasheet** 

FRANKA RESEARCH 3 

Copyright © Franka Robotics 

## **Datasheet1 Franka Research 3** 

Arm (Art. No. 309969) & Control (Art. No. 295341) 

Document number: R02212 

Document release version: 2.2.2 (June 2026) 

||ARM|(v2.0)||
|---|---|---|---|
|Degrees of freedom|7|Interfaces|•Ethernet (TCP/IP) for programming|
|Rated payload|3 kg||and administration via Desk|
|Maximum reach|855 mm||•safety-rated input for external enabling device|
|Force/Torque sensing|link-side torque sensor in all 7 axes||•safety-rated input for emergency stop<br>i|
|Joint position limits|A1: -166/166 deg||•2 configurable safety-rated inputs for e.g.,<br>t di fd|
||A2: -105/105 deg<br>A3: -166/166 deg||emergency sop evces, saeguars or<br>other protective devices (OSSD devices via<br>external OSSD converter connectable)|
||A4: -176/-7 deg<br>A5: -165/165 deg<br>A6: 25/265 deg<br>A7: -175/175 deg||•Control connector<br>•connector for end effector|
|Joint torque limits|A1-A4: ±87 Nm<br>A5-A7: ±12 Nm|||
|Mechanical interface to<br>end effector|DIN ISO 9409-1-A50|||
|Installation position|upright|||
|Weight|~ 17.8 kg|||
|Ingress protection|IP40|||
|Ambient temperature ²|+5 °C to +45 °C|||
|Air humidity|20 − 80 %, non-condensing|||
|CONTR|OL (v5.1)||PERFORMANCE|
|Rackmount form factor|19'', 355 x 483 x 89 mm (D x W x H)|Motion||
|Supply voltage|100 − 240 VAC|Joint velocity limits|A1-A4: 150 deg/s|
|Mains frequency|50− 60 Hz||A5-A7: 301 deg/s (FCI use, A6: 239 deg/s)|
|Power consumption|~ 80 W|Cartesian velocity limits|up to 2 m/s  at TCP|
|Active power factor correction (PFC)|yes|Position repeatability³|<+/- 0.1 mm (ISO 9283)|
|Weight|~ 7 kg|||
|Ingress Protection|IP20|Interaction||
|Ambient temperature ²|+5 °C to +45 °C|Guiding force|~ 2.5 N|
|Air humidity|20 − 80 %, non-condensing|Adjustable translational st|iffness<br>10 − 3000 N/m|
|Permitted mounting orientation|horizontal|Adjustable rotational stiff|ness<br>1 − 300 Nm/rad|
|Interfaces|•ethernet (TCP/IP) for internet,|Monitored signals|joint position, velocity,|
||shop-floor connection, fieldbuses<br>and 1 kHz Franka Control||torque cartesian position, force|
||Interface (FCI)||ADD-ONS|
||•power connector<br>IEC 60320C14 (V-Lock)<br>•Arm connector|Fully integrated end effect|ors<br>•2-finger gripper<br>•Vacuum gripper|
|||Fieldbuses|•Modbus/TCP<br>•OPC UA|



> 1. Technical data are subject to change. 

> 2. For more details see Product Manual Franka Research 3. 

> 3. Based on ISO 9283 (Annex A), specified values refer to a workspace of 0.4 x 0.4 x 0.4 m centered at [0.498, 0.0, 0.226] m, with the Z-Axis of the flange oriented parallel to earth-gravity and the elbow positioned upwards. 

> 4. For System Images < 5.10, FCI cannot control the robot while SLP-C is configured. 

> 5. For System Images < 5.10, FCI cannot control the robot while SLS-C is configured. 

**Datasheet1 Franka Research 3** 

Document number: R02212 

Arm (Art. No. 309969) & Control (Art. No. 295341) 

Document release version: 2.2.2 (June 2026) 

### SAFETY 

|Certification process ongoing||
|---|---|
|EN ISO 13849-1:2015 safety of machinery -<br>safety-related parts of control systems||
|EN ISO 10218-1:2011 Robots and robotic devices -<br>safety requirements for industrial robots Part1: Robots||
|Collaborative operation modes||
|Monitored stop|fully integrated in PL d, Cat 3|
|Hand-guiding|fully integrated in PL d, Cat 3|
|Speed and separation monitoring|realizable in combination with external protective devices up to PL d, Cat 3|
|Safety Functions||
|Emergency Stop (X3.1)|PL d, Cat 3|
|External Enabling Device (X4)|PL d, Cat 3|
|Enabling Button|PL d, Cat 3|
|Two configurable safe inputs (X3.2 and X3.3)|PL d, Cat 3|
|SLP-C: Safely limited Cartesian position<sup>**4**</sup>|PL d, Cat 3|
|SLS-C: Safely limited Cartesian speed<sup>**5**</sup>|PL d, Cat 3|
|SLS-J: Safely limited joint speed|PL d, Cat 3|
|SLD: Safely limited distance|PL d, Cat 3|
|SEEPO: Safe End Effector Power off|PL b, Cat b|
|Stopping Functions||
|Category 0 stop|PL d, Cat 3|
|Category 1 stop|PL d, Cat 3|
|Category 2 stop|PL d, Cat 3|
|Worst case safe Cartesian position accuracy|50 mm|
|for stopping functions||
|Safety values according to EN ISO 13849-1||
|PFH of PL d, Cat 3 safety functions|< 1 × 10<sup>−7</sup>|
|(Probability of Failures per Hour)||
|PFH of PL b, Cat b safety functions<br>(Probability of Failures per Hour)|< 1 × 10<sup>−7</sup>|



Copyright © Franka Robotics 

**Datasheet1 Franka Research 3** 

Document number: R02212 

Document release version: 2.2.2 (June 2026) 

Arm (Art. No. 309969) & Control (Art. No. 295341) 

### DIMENSIONS & WORKSPACE 



