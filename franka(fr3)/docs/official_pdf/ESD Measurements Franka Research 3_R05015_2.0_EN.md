> **[PDF を開く](<ESD Measurements Franka Research 3_R05015_2.0_EN.pdf>)**
>
> PDF から自動変換した本文です。図は含まず、表は崩れている場合があります。安全や仕様の確認には PDF を使ってください。

## **ESD Measurements** 

FRANKA RESEARCH 3 

# **Franka Research 3 v2.0** 

# **ESD Measurements** 

Release Version: 2.0 (June 2025) Document Number: R05015 

Copyright © Franka Robotics GmbH 

2 

### **Fundamentals of Testing** 

The Franka Production 3 robot was subjected to a test to determine the following parameters: 

- Measurement of resistance to ground RGP of the surfaces, contact surfaces and the flange surfaces (according to DIN IEC/TR 61340-5-1 and DIN EN 61340-5-2). 

- Measurements of existing electric fields / surface voltages after rubbing the surface as well as during operation (according to DIN EN 61340-5-1). 

Environmental conditions during measurement: 

- Temperature: 24,2 °C 

- Relative humidity: 44 % 

### **Definition of ESD Measuring Points** 





**Figure 1** : Measuring points 

Copyright © Franka Robotics GmbH 

3 

### **ESD Measurements** 

##### **Measured Values** 

||**Resistance to ground**<br>**RGP [Ohm]**|**Electrost**<br>**volta**|**atic surface**<br>**ge [V]**|**Electrostatic field [V/m]**|
|---|---|---|---|---|
|||after<br>friction|after 0,75 h<br>operation|after 0,75 h operation|
|Limits|< 1 G**Ω**|< 1|25 V|< 5000 V/m|
|M1|<50,0 x 10³|10,0|0,0|0,0|
|M2|27,7 x 10**⁹**|220,0|0,0|1500,0|
|M3|23,2 x 10**⁹**|0,0|0,0|0,0|
|M4|27,7 x 10**⁹**|258,0|6,0|0,0|
|M5|30,6 x 10**⁹**|0,0|0,0|0,0|
|M6|81,7 x 10**⁹**|150,0|0,0|0,0|
|M7|29,0 x 10**⁹**|350|0,0|0,0|
|M8|72,6 x 10**⁹**|0,0|0,0|0,0|
|M9|33,8 x 10**⁹**|990,0|0,0|0,0|
|M10|20,2 x 10**⁹**|0,0|9,0|0,0|
|M11|37,1 x 10**⁹**|0,0|7,0|0,0|
|M12|2,36 x 10**⁹**|0,0|0,0|0,0|



Copyright © Franka Robotics GmbH 

4 

#### **Considerations on ESD Measured Values** 

The measured values show that the robot complies with the requirements of DIN EN61340-5-1 (2017 edition) while maintaining the distances to ESD-sensitive electronics. 

When integrating the robot into an ESD-sensitive environment, there must be no contact with ESD sensitive electronics. EN61340-5-1 specifies a minimum distance of 25 mm for the values listed. 

The fingertips supplied with the Franka Hand must be replaced with a conductive material that is suitable for ESD. For creating new fingertips, you can use the fingertip-configurator at franka.world (https://franka.world/fingertipconfigurator). 

The real values of the integrated robot regarding the electrostatic surface voltage and the electrostatic field can deviate from the listed measured values due to different environmental conditions. 

Therefore, a verifying measurement is recommended after integration. 

Copyright © Franka Robotics GmbH 

5 

Franka Robotics GmbH Frei-Otto-Straße 20 80797 Munich Germany 

