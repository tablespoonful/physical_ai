---
title: "Dynamic Properties and Motion Reproducibility of a Compact Pneumatically Actuated Humanoid Upper Body for Data-Driven Control"
date: "2026-03-16"
authors: "Hiroshi Atsuta; Hisashi Ishihara; Minoru Asada"
url: https://arxiv.org/abs/2603.14787
pdf: https://arxiv.org/pdf/2603.14787
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.14787)** / [論文ページ](https://arxiv.org/abs/2603.14787)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

## FULL PAPER 

# **Dynamic properties and motion reproducibility of a compact pneumatically actuated humanoid upper body for data-driven control** 

Hiroshi Atsuta<sup>a</sup> , Hisashi Ishihara<sup>a,b</sup> , and Minoru Asada<sup>a,c,d</sup> 

> aSymbiotic Intelligent Systems Research Center, Institute for Open and Transdisciplinary Research Initiatives, The University of Osaka, Suita, Osaka, Japan;<sup>b</sup> College of Arts and Design, Ritsumeikan University, Kyoto, Japan;<sup>c</sup> International Professional University of Technology in Osaka, Umeda, Kita-ku, Osaka, Japan;<sup>d</sup> Chubu University Academy of Emerging Sciences, Kasugai, Aichi, Japan 

#### **ARTICLE HISTORY** 

Compiled September 14, 2026 

#### **ABSTRACT** 

Pneumatically-actuated anthropomorphic robots with high degrees of freedom (DOF) offer significant potential for physical human-robot interaction. However, precise control of pneumatic actuators is challenging due to their inherent nonlinearities. This paper presents the development of a compact 13-DOF upper-body humanoid robot. To assess the feasibility of an effective controller, we first investigate its key dynamic properties, such as actuation time delays, and confirm that its behavior is reproducible across repeated trials. Leveraging this reproducibility, we implement a preliminary data-driven controller for a 4-DOF arm subsystem based on a multilayer perceptron with explicit time delay compensation. The network was trained on random movement data to generate pressure commands for tracking arbitrary trajectories. In comparative evaluations on this subsystem, the data-driven controller achieved lower tracking errors than a traditional PID controller. This result suggests that data-driven approaches are a promising option for controlling complex, high-DOF pneumatic robots. 

#### **KEYWORDS** 

pneumatic robot; data-driven control; time-delay compensation; trajectory tracking; inverse dynamics; human-robot interaction; humanoid; android 

### **1. Introduction** 

For a human-robot symbiotic society to be established, physical human-robot interaction (HRI) involving close contact is crucial. Pneumatic actuators are effective for safe physical interaction due to their inherent compliance [1], which stands in contrast to electrically-driven actuators that use high-transmission-ratio gears [2]. Pneumatic actuators generally fall into two categories: pneumatic artificial muscles (PAMs) and pneumatic cylinders. PAMs are lightweight and flexible, making them suitable for dynamic movements like jumping and walking in legged robots [3,4] and for direct interaction with humans [5,6]. However, they require sophisticated control systems to handle their 

CONTACT Hiroshi Atsuta. Email: hiroshi.atsuta@otri.osaka-u.ac.jp 

complex dynamics, and their relatively short fatigue life limits their durability [7,8]. On the other hand, pneumatic cylinders have more rigid structures and simpler dynamics than PAMs, resulting in longer lifespans, lower maintenance, and better controllability. They offer high force output and compliance but require sturdy metal housings and piston rods. 

Designing a compact, pneumatically-actuated robot that replicates the human musculoskeletal system is challenging but essential for effective physical HRI. Furthermore, compactness also facilitates emotional HRI [9,10], as smaller robots is often less intimidating and helps people feel more safe and comfortable. Ishihara _et al._ [11] addressed this by developing a compact upper-body robot with 22 degrees of freedom (DOF) driven by pneumatic semi-rotary actuators and cylinders, all within a small frame of approximately 30 cm from waist to shoulders, as part of the “Affetto” project [12]. They achieved this compactness by carefully selecting joint mechanisms that optimized the use of limited internal space while meeting power requirements. This previous work demonstrated the feasibility of a small, high-DOF upper body by strategically employing pneumatic semi-rotary actuators and cylinders with direct drive, slider-crank, and parallel linkage mechanisms to ensure both sufficient power and compactness. While multi-DOF robotic systems with pneumatic cylinders are less common than PAM-driven robots, several have been reported, including robotic arms [13–16], legged robots [17,18], and humanoids [19–22]. However, to the best of the authors’ knowledge, no other humanoid robot driven by pneumatic cylinders has achieved such compactness [11]. 

A fundamental HRI task is kinesthetic teaching, where a robot is physically guided through a motion that it must then reproduce. To achieve this, the ability to track an arbitrary recorded trajectory is essential. However, precisely controlling pneumatic actuators remains challenging due to their nonlinearities, including pressure dynamics, air compressibility, and friction [23,24]. Numerous control approaches have been proposed, ranging from linear methods augmented with schemes like fuzzy logic [25,26] and gain scheduling [27,28] to nonlinear methods employing more accurate models, such as sliding mode control [29–32] and adaptive backstepping control [33–35]. These studies, however, typically focus on single-DOF experimental setups and require extensive system modeling. A further challenge, specific to HRI contexts, is the need for long air transmission lines to situate the robot away from bulky valves and noisy compressors, which introduces significant time delays and mass flow attenuation [36–38]. As reported in a previous study [11], a simple linear controller could not achieve adequate tracking performance for such a system. 

This study explores the potential of a data-driven approach for controlling such a complex robot, motivated by the challenges of identifying a complete dynamic model. This approach requires both system reproducibility and a sufficient amount of data. The robot in the previous study [11] had insufficient actuator power and structural stiffness, leading to unreliable motion generation over long periods. Therefore, we improved the mechanical design of the robot to address these shortcomings in collaboration with A-Lab Co., Ltd. (Tokyo, Japan). Consequently, we investigate the robot’s dynamic characteristics, including transmission line time delays, minimum pressures to start movements, and motion characteristics under maximum pressure differences, and examine its reproducibility under specific conditions. Furthermore, we confirm the robot’s durability for collecting time-series sensor data over extended periods. Finally, after confirming reproducibility across the 13-DOF platform, we implement a preliminary data-driven controller for a representative 4-DOF arm subsystem as a feasibility study of explicit time-delay compensation, and compare its tracking performance against that of a traditional PID controller. 

2 


**Figure 1.** The 13-DOF pneumatically-actuated upper-body humanoid robot developed in this study. The main photo shows the front view while the inset on the lower left shows the robot’s front-right side with a different pose. 

This paper is structured as follows: Section 2 details the design of the compact upperbody structure shown in Figure 1. Section 3 investigates the robot’s dynamic properties, focusing on time delays, motion characteristics, and reproducibility. Section 4 describes the data collection process and demonstrates the data-driven controller with explicit time delay compensation. Section 5 discusses the robot’s potential for dynamic expression, the limitations of the present study, and future directions for data-driven control. Finally, Section 6 concludes the paper. 

### **2. Robot System** 

The design policy of this robot follows the “Affetto” concept discussed in the preceding work [11]. The robot was developed for close physical human-robot interaction with a child-sized upper body, and this led to three main design requirements. First, pneumatic actuation was adopted for physical interaction. Second, the mechanism had to remain compact while preserving a wide motion range for expressive upper-body movements. Third, the noisy pneumatic pump and related equipment were placed away from the robot so as not to disturb interaction, which required long transmission tubes. As discussed later, these long tubes also introduce delay and attenuation in pressure transmission, which directly shape the control challenges addressed in this paper. 

3 


**Figure 2.** Kinematic diagram of the 13-DOF upper body. Joints 2, 3, 8, and 9 in the chest and scapula are driven by air cylinders A2, A3, A8, and A9, while the others driven by rotary actuators. 

### **_2.1. Mechanical System_** 

Figure 2 illustrates the joint structure of the upper-body robot, which has a total of 13 active joints assembled with seven types of mounts. The rotary actuator for waist rotation (joint 1) is fixed to the waist mount and rotates the chest mount. Two air cylinders for scapula rotation (joints 2 and 8) are fixed to the chest mount to rotate the left and right scapula mounts, while two other air cylinders for shoulder abduction (joints 3 and 9) are fixed to the scapula mounts to rotate the shoulder mounts. These joints must lift or support the arm against gravity within the limited space available in the chest and scapula. For this reason, closed-loop slider-crank mechanisms were adopted so that the force of linear cylinders could be used efficiently while keeping the shoulder structure compact and maintaining the required range of motion. In the arms, the rotary actuators for shoulder flexion (joints 4 and 10) are fixed to the shoulder mounts to rotate the upper arm mounts, and the actuators for shoulder rotation (joints 5 and 11) are fixed to the upper arm mounts to rotate the elbow mounts. The actuators for elbow flexion (joints 6 and 12) are fixed to the elbow mounts to rotate the forearm mounts, which carry the final rotary actuators for forearm rotation (joints 7 and 13). For this robot, the positive direction for each joint is defined as a movement that extends the limbs or opens the body, while the negative direction corresponds to a movement of flexing or folding the limbs. 

Figures 3(a) and 3(b) show the vane-type rotary actuators and the air cylinders used in the robot, respectively. These actuators were customized by A-Lab Co., Ltd. from 

4 


**Figure 3.** Actuator mechanisms. (a) Assembly drawing of a vane-type rotary actuator. (b) Assembly drawing of an air cylinder. (c) Internal schematic of the rotary actuator. (d) Internal schematic of the air cylinder. 

commercial products, whose specific off-the-shelf type numbers of pneumatic actuators (both the air cylinders and vane-type rotary actuators) are industrial secrets of A-Lab. Both actuator types have rigid bodies with mounting holes for attachment. Each actuator has two air ports (A and B) for the pneumatic tubes. As shown in the schematics in Figures 3(c) and 3(d), each actuator contains two air chambers (A and B). Pressurized air in these chambers pushes a movable vane (rotary actuator) or a movable partition (air cylinder). The resulting torque (Figure 3(c)) or force (Figure 3(d)) is determined by both the pressure difference between these chambers and the pressure-receiving surface area of the vane or partition. Therefore, controlling the pressure in these two chambers is crucial for motion control. 

The assembled robot is shown from the front and rear in Figure 4, where key actuators and structural mounts are indicated. The rear view reveals a complex tubing system where each actuator is connected via two pneumatic tubes, approximately 2 _._ 5 m in length, which allows for remote placement of the control valves. These tubes have a primary internal diameter of 1 mm, expanding to 2 mm at the branch section used to connect a pressure sensor (Nihon Pisco Co., Ltd., PSE530) near each actuator’s air port. To measure joint angles, potentiometers (NIDEC COMPONENTS CORPORATION, JC10) are installed at each joint. The robot’s height from the waist mount is approximately 38 cm, and its mass is 5 _._ 12 kg. 

Table 1 summarizes the mechanical specifications of the actuators installed for the 13 active joints. The table lists the corresponding joint number, function, actuator type, rated output at 0 _._ 7 MPaG, and range of motion for each joint. Because the output forces of the air cylinders differ according to the movement direction of the piston rod, the rated outputs for the pulling movement are described in parentheses after those for the pushing movement. 

5 


**Figure 4.** Hardware overview of the developed robot: (a) front view and (b) rear view, with key components labeled. 

### **_2.2. Drive, Sensory, and Control Systems_** 

As illustrated in Figure 5, the robot is controlled by a host computer that communicates with the hardware via two main channels. First, the valve unit, containing a series of proportional pressure control valves, is connected via USB serial and regulated by an air compressor at 0 _._ 6 MPaG. Second, the sensor unit, containing a micro CPU with analog-to-digital (AD) converters, is linked to the robot’s 13 potentiometers and 26 pressure sensors, which sends sensor data to the host computer via Ethernet. Programs for valve control and sensor acquisition run as separate processes on the host computer, while a client computer can interface with the host computer over a local network via UDP to issue commands and log data. 

The distal end of each pneumatic tube is connected to a proportional pressure control valve, which discharges compressed air at a regulated pressure from approximately 0 _._ 003 to 0 _._ 6 MPaG with a low hysteresis of 0 _._ 25% and high precision of 0 _._ 75%. The pressure setpoint is operated by an input voltage from 0 to 10 V proportionally. For example, the valve discharges 0, 0 _._ 3, and 0 _._ 6 MPaG when the input voltage is set to 0, 5, and 10 V, respectively. 

The input voltage for each valve is controlled by a one-byte integer command value (0–255), which is converted to an actual voltage from 0 to 10 V by a digital-to-analog converter. Consequently, the control signal for the robot is a 26-dimensional vector of one-byte elements, since the robot has 13 actuators, each with two pneumatic tube systems. This control signal is updated in the host computer and sent to the robot at 30 Hz. 

6 

**Table 1.** Mechanical specifications of the actuators for the 13 active <u>joints.</u> 

|**Joint No.**|**Function**|**Type**|**Output**|**Range**|
|---|---|---|---|---|
|1|Waist rotation|Rotary|5.5 N_·_m|90 deg|
|2|Right scapula rotation|Cylinder|525 (420) N|30 mm|
|3|Right shoulder abduction|Cylinder|350 (260) N|15 mm|
|4|Right shoulder flexion|Rotary|3.0 N_·_m|90 deg|
|5|Right shoulder rotation|Rotary|3.0 N_·_m|90 deg|
|6|Right elbow flexion|Rotary|3.0 N_·_m|90 deg|
|7|Right forearm rotation|Rotary|3.0 N_·_m|90 deg|
|8|Left scapula rotation|Cylinder|525 (420) N|30 mm|
|9|Left shoulder abduction|Cylinder|350 (260) N|15 mm|
|10|Left shoulder flexion|Rotary|3.0 N_·_m|90 deg|
|11|Left shoulder rotation|Rotary|3.0 N_·_m|90 deg|
|12|Left elbow flexion|Rotary|3.0 N_·_m|90 deg|
|13|Left forearm rotation|Rotary|3.0 N_·_m|90 deg|


**Figure 5.** Overview of the experimental control system. A host computer manages valve commands and sensor data acquisition, allowing a client computer to interface with the robot over a local network. 

The robot has a total of 13 potentiometers and 26 pressure sensors to measure the angles of active joints and the air pressures near the actuator chambers. The reference voltage for these sensors is 5 V, and their output voltages from 0 to 5 V are read by a 16-bit AD converter (CONTEC CO., LTD., ADI16-4(FIT)GY). These sensory signals are acquired by the host computer at 30 Hz. 

### **_2.3. Posture Variation_** 

Figure 6 shows examples of postures that the robot can achieve, including (a) a neutral pose, in which every joint is relaxed; (b) an open-arm pose, in which both arms are spread out; (c) an akimbo pose, in which both hands are set to the waist; (d) a raisinghands pose, in which the hands are raised toward the expected head area; (e) a twisting pose, in which the arms are twisted in opposite directions; and (f) a raising-elbows pose, in which both elbows are raised with folded hands. 

### **3. Dynamic Properties and Motion Reproducibility** 

To design an effective controller for the robot’s complex pneumatic system, it is essential to first understand its fundamental dynamic characteristics. This section details a series of experiments conducted to probe these properties. The investigation is divided into two main parts: 

7 


**Figure 6.** Examples of the robot’s expressive postures. 

- **Experiment I** characterizes three key dynamic properties: transmission time delay, the minimum pressure command required for activation, and maximum joint velocity. These tests are designed to highlight the system’s nonlinearities and the challenges involved in developing an analytical model. 

- **Experiment II** assesses the trial-to-trial reproducibility of the robot’s movements. This test is crucial for validating the feasibility of a data-driven control approach, which relies on the system behaving deterministically under consistent conditions. 

### **_3.1. Experimental Setup_** 

### _3.1.1. Tested Joints and Postures_ 

Due to the symmetric design of the robot’s arms, experiments were performed on a representative set of 7 joints: the waist (joint 1) and the six joints of the left arm (scapula rotation, shoulder abduction, shoulder flexion, shoulder rotation, elbow flexion, and forearm rotation; joints 8-13). The robot’s dynamic response is highly dependent on its posture. Specifically, the gravitational and inertial loads on any single joint under test vary significantly based on the configuration of its distal links (e.g., the shoulder joint experiences a much higher load when the arm is fully extended compared to when it is folded). To systematically investigate the effect of the configuration on the movement, four specific initial postures were defined for each test, accounting for the movement direction (Positive or Negative). These postures were chosen as the extremes of the load range for a given joint: 

- For positive direction movements: 

   - **Pose EP (Easiest-to-move, Positive)** : The robot is configured to minimize the gravitational and inertial load resisting a given positive movement. 

   - **Pose HP (Hardest-to-move, Positive)** : The robot is configured to maximize the load resisting a given positive movement. 

8 


**Figure 7.** Example of test postures for the left scapula rotation joint (joint 8). The physical posture for the ’easiest’ and ’hardest’ conditions depends on the movement direction relative to gravity. For positive movement (left), the folded-arm posture is defined as Pose EP (easiest) and the extended-arm posture as Pose HP (hardest). For negative movement (right), where gravity assists the motion, the extended-arm posture becomes the ’easiest’ condition (Pose EN), while the folded-arm posture becomes the ’hardest’ (Pose HN). 

- For negative direction movements: 

   - **Pose EN (Easiest-to-move, Negative)** : The robot is configured to minimize the load resisting a given negative movement. 

   - **Pose HN (Hardest-to-move, Negative)** : The robot is configured to maximize the load resisting a given negative movement. 

Thus, these “easiest” and “hardest” postures are defined relative to the specific joint being tested. For example, to test the left scapula rotation in the positive direction (lifting the arm against gravity), Pose EP involves folding the arm (changing the posture of distal links) to minimize the moment arm, while Pose HP involves extending the arm to maximize the load, as shown in Figure 7. Conversely, for negative-direction movements where gravity assists the motion, these physical postures are reversed: Pose EN (easiest) is the extended-arm posture, and Pose HN (hardest) is the folded-arm posture. 

### _3.1.2. Notation_ 

In this paper, joint angles are expressed as normalized positions in percent of each joint’s range of motion, where 0 and 100 correspond to the two mechanical limits of the joint, and joint velocities are given in this normalized unit per second. Throughout this section, we use the following notation: **_u_**<sup>A</sup> ( _t_ ) and **_u_**<sup>B</sup> ( _t_ ) represent the vectors of commanded values for the A and B actuator chambers at time _t_ , respectively. Similarly, **_p_**<sup>A</sup> ( _t_ ) and **_p_**<sup>B</sup> ( _t_ ) are the measured pressure values near each chamber, **_q_** ( _t_ ) is the vector of measured joint angles, and **_v_** ( _t_ ) is the vector of joint velocities (numerical derivative of **_q_** ( _t_ )). All vectors are 7-dimensional (e.g., **_u_**<sup>A</sup> ( _t_ ) _∈_ R<sup>7</sup> ), corresponding to the 7 joints under test. The subscript _i_ indicates the value for the _i_ -th joint (e.g., _qi_ ( _t_ )). 

9 


**Figure 8.** Method for measuring time delay ( _t_ delay _,_ 8) for the left scapula rotation joint. The delay is the duration between the command step input at _t_ 0 and the detected initiation of movement at _t_ start. 

**Table 2.** Converged time delay values <u>[ms]</u> for each <u>joint</u> and condition. 

||Moving direc|tion: Positive|Moving direct|ion: Negative|
|---|---|---|---|---|
|Joint|Pose EP|Pose HP|Pose EN|Pose HN|
|#1 Waist|275_._56_±_21_._12|274_._44_±_18_._55|265_._56_±_20_._73|266_._67_±_19_._91|
|#8 L. Scapula|242_._22_±_21_._37|261_._48_±_20_._45|277_._14_±_15_._74|283_._81_±_18_._81|
|#9 L. Shoulder Abd.|227_._22_±_18_._92|245_._56_±_20_._10|293_._89_±_19_._68|294_._44_±_16_._32|
|#10 L. Shoulder Flex.|254_._67_±_19_._99|260_._33_±_18_._58|285_._42_±_20_._88|324_._44_±_17_._10|
|#11 L. Shoulder Rot.|235_._15_±_18_._97|240_._61_±_20_._35|228_._67_±_16_._90|247_._33_±_19_._27|
|#12 L. Elbow Flex.|243_._33_±_21_._41|237_._00_±_20_._97|244_._85_±_19_._22|256_._36_±_19_._01|
|#13 L. Forearm Rot.|236_._67_±_18_._16|_−_|231_._52_±_20_._79|_−_|


### **_3.2. Experiment I-A: Measuring Transmission Time Delay_** 

### _3.2.1. Method_ 

A significant time delay is expected between the onset of a valve command and the resulting pressure change in the actuator chamber due to the 2.5 m long pneumatic tubes. This experiment quantifies this delay. For each joint, direction, and posture, the following procedure was repeated 10 times: 

- (1) To ensure a consistent starting condition, the robot was set to its initial posture (Pose EP, HP, EN or HN) by driving the target joint to one of its mechanical limits. This position was held with an initial set of valve commands, **_u_**<sup>A</sup> (0) and **_u_**<sup>B</sup> (0). 

- (2) At time _t_ 0, a step input was applied to one chamber’s valve command (e.g., _u_<sup>A</sup> _i_<sup>(</sup><sup>_t_0))</sup> to induce movement, while the other command ( _u_<sup>B</sup> _i_<sup>(0))washeldconstant.</sup> 

- (3) The joint angle _qi_ ( _t_ ) and commanded pressures _u_<sup>A</sup> _i_<sup>(</sup><sup>_t_)and</sup><sup>_u_B</sup> _i_<sup>(</sup><sup>_t_)wererecorded.</sup> 

- (4) The time when movement was first detected, _t_ start, was identified from the joint angle data. 

- (5) The time delay was calculated as _t_ delay _,i_ = _t_ start _− t_ 0, as depicted in Figure 8. 

### _3.2.2. Results_ 

Figure 9 shows the measured time delay for the left scapula rotation joint (joint 8) as a function of the applied pressure command difference, where the pressure command difference is calculated as follows: 


10 


**Figure 9.** Estimated time delay versus applied pressure command difference for the left scapula rotation joint (joint 8). The delay converges to a stable value of approximately 280 ms for large command differences. Error bars represent standard deviation over 10 trials. 


**Figure 10.** Method for measuring the minimum pressure command difference (<sup>min</sup> _u_ diff _,_ 8) for the left scapula rotation joint. The command difference is recorded at the moment movement is detected. 

At low command differences, the time delay is long and shows significant inconsistency. However, as the command difference increases, the delay shortens and converges toward a specific value. This convergent behavior was observed across all tested joints. 

Table 2 summarizes these converged time delay values, in which mean and standard deviation over 10 measurements are shown. These values were calculated by averaging the last several data points for each condition where the delay had saturated. The results confirm a substantial and consistent baseline delay inherent to the air transmission lines, roughly ranging from 230 ms to 320 ms. The posture also has a minor but consistent influence, with the hardest-to-move postures (Poses HP and HN) often resulting in a slightly longer delay than their easiest-to-move counterparts (Poses EP and EN). The low standard deviation in all cases suggests this phenomenon is highly reproducible. 

### **_3.3. Experiment I-B: Measuring Minimum Pressure Command_** 

### _3.3.1. Method_ 

To initiate movement, pneumatic actuators must generate sufficient force to overcome internal static friction. This experiment measures the minimum pressure command difference (<sup>min</sup> _u_ diff _,i_ ) required to start movement. The procedure, illustrated in Figure 10, 

11 


**Figure 11.** Average minimum pressure command difference required to initiate movement for each tested joint. The plot compares the four initial postures: Pose EP and Pose HP for the easiest and hardest positive movements, and Pose EN and Pose HN for the easiest and hardest negative movements. Error bars represent the standard deviation over 10 trials. 

was repeated 10 times for each condition. 

- (1) The robot was set to an initial posture (Pose EP, HP, EN or HN) and held at a mechanical limit. 

- (2) The pressure in one chamber was gradually increased (or decreased) while the other was held constant. 

- (3) The command difference<sup>min</sup> _u_ diff _,i_ was recorded at the exact moment joint movement was detected, which was computed as follows: 


### _3.3.2. Results_ 

The average minimum command differences for all tested joints are shown in Figure 11. The results reveal that the activation threshold is affected by both intrinsic actuator properties and external loads. For joints where gravity has a negligible influence on the movement, such as waist rotation (Figure 11(a)) and forearm rotation (Figure 11(g)), the required command difference shows no significant variation between the easiest (Pose EP or EN) and hardest (Pose HP or HN) postures. For those joints, the activation threshold is primarily determined by the actuator’s internal static friction. In contrast, for joints working against gravity, such as scapula rotation (Figure 11(b)) and shoulder flexion (Figure 11(d)), the external load becomes a significant factor; for positive movements against gravity, the hardest posture (Pose HP) requires a substantially higher command difference than the easiest posture (Pose EP). Across all conditions, the low variance in the measurements indicates that the static friction for each joint is consistent. While this predictability is useful, it also highlights a challenge in pneumatic control, as this friction can lead to stick-slip effects, making extremely smooth, slow motions difficult to achieve. 

12 


(a) Positive direction 

(b) Negative direction 

**Figure 12.** Motion profiles for the waist joint (joint 1) under maximum pressure command for (a) positive and (b) negative movement directions. The top, middle, and bottom plots show the commanded pressure, measured pressure responses, and resulting joint trajectories, respectively. The trajectories for the easiest (Pose EP in (a), Pose EN in (b)) and hardest (Pose HP in (a), Pose HN in (b)) postures are compared, showing a clear difference in speed. 

### **_3.4. Experiment I-C: Evaluating Maximum Velocity Characteristics_** 

### _3.4.1. Method_ 

To understand the robot’s capacity for dynamic movement, this experiment measured the maximum joint velocity (<sup>max</sup> _vi_ ) under the maximum possible pressure difference. The procedure was repeated 10 times for each condition. 

- (1) The robot was set to an initial posture (Pose EP, HP, EN or HN) and held at a mechanical limit. 

- (2) At _t_ 0, a maximum step input was applied by setting _u_<sup>A</sup> _i_<sup>tomax.</sup> 

- (3) The resulting joint trajectory _qi_ ( _t_ ) was recorded, and the maximum velocity was calculated from its numerical time derivative. 

### _3.4.2. Results_ 

The resulting motion profiles for the waist and left elbow flexion joints are shown in Figures 12 and 13, and the maximum velocities for all joints are summarized in Table 3. For each joint, the figures display the commanded pressure step input (top plot), the measured pressure responses in each actuator chamber (middle plot), and the resulting 

13 


**Figure 13.** Motion profiles for the left elbow flexion joint (joint 12) under maximum pressure command for (a) positive and (b) negative movement directions. The plot layout is identical to that of Figure 12. The trajectories for the easiest (Pose EP in (a), Pose EN in (b)) and hardest (Pose HP in (a), Pose HN in (b)) postures are compared. For this distal joint, the influence of posture on the resulting trajectories is less significant compared to the waist joint. 

joint angle trajectories (bottom plot). The key finding is that the robot’s posture has a much larger impact on the dynamic performance of proximal joints (close to the torso) than distal joints. 

As seen in Figure 12, the motion profile of the waist joint differs significantly between the easiest (Pose EP or EN) and hardest (Pose HP or HN) postures, as its movement is affected by the inertia of the entire upper body. In contrast, for a distal joint like the elbow (Figure 13), the difference between these two postural conditions is much smaller. This configuration-dependent behavior underscores the difficulty of developing a single, simple dynamic model for the robot. 

### **_3.5. Experiment II: Assessing Motion Reproducibility_** 

### _3.5.1. Method_ 

The previous experiments suggest that while the robot’s dynamics are highly complex and nonlinear, they are also consistent. This final experiment aims to quantify this consistency, or reproducibility, which is a prerequisite for data-driven control. 

- (1) The robot was initialized to a consistent starting state by moving all joints to one of their mechanical limits. 

14 

**Table 3.** Maximum <u>joint</u> velocity <u>[0-100/s]</u> for each <u>joint</u> and condition. 

||Moving direc|tion: Positive|Moving direc|tion: Negative|
|---|---|---|---|---|
|Joint No.|Pose EP|Pose HP|Pose EN|Pose HN|
|#1 Waist|445_._47_±_8_._36|394_._42_±_8_._81|_−_451_._82_±_6_._85|_−_401_._07_±_7_._25|
|#8 L. Scapula|816_._20_±_98_._93|797_._04_±_51_._17|_−_442_._74_±_48_._88|_−_379_._94_±_32_._68|
|#9 L. Shoulder Abd.|395_._31_±_22_._32|439_._86_±_58_._97|_−_222_._81_±_28_._19|_−_182_._50_±_19_._40|
|#10 L. Shoulder Flex.|728_._07_±_52_._06|559_._97_±_17_._96|_−_415_._80_±_21_._10|_−_328_._21_±_7_._84|
|#11 L. Shoulder Rot.|641_._15_±_68_._60|615_._60_±_40_._99|_−_572_._96_±_40_._17|_−_638_._92_±_59_._21|
|#12 L. Elbow Flex.|626_._83_±_54_._45|564_._33_±_61_._26|_−_555_._74_±_48_._20|_−_588_._55_±_66_._67|
|#13 L. Forearm Rot.|613_._95_±_58_._85|_−_|_−_552_._82_±_25_._16|_−_|


(a) Waist joint (1) 


(b) Arm joints (2-7, 8-13) 

**Figure 14.** RMSE matrices evaluating the trial-to-trial reproducibility for (a) the waist joint and (b) the 12 arm joints. Each cell ( _j, k_ ) shows the RMSE between trial _j_ and trial _k_ . The light coloring indicates very high similarity across trials. 

- (2) A predetermined, random time series of pressure commands was sent to all 26 valves simultaneously for 60 seconds. 

- (3) The resulting joint angle trajectories **_q_** ( _t_ ) were recorded. 

- (4) The procedure was repeated 11 times. The first trial was discarded as a warm-up. (5) The similarity between any two trial trajectories ( _j_ and _k_ ) for a single joint _i_ was quantified by calculating the Root Mean Square Error (RMSE): 


### _3.5.2. Results_ 

The RMSE values for all pairs of trials were computed for each joint and are visualized as matrices in Figure 14. The color in each cell represents the RMSE between two trials; lighter colors indicate higher similarity (lower error). The matrices are overwhelmingly light, indicating a very low RMSE between trials for almost all joints. The largest errors were observed in the right elbow flexion joint (joint 6). Because joints 6 and 12 are structurally symmetric, the difference is unlikely to arise from the nominal joint design itself. One plausible explanation is actuator-to-actuator variability in internal friction between the two customized actuators. Since pneumatic joint motion is sensitive to such friction differences, even small variations can appear as minor differences in motion reproducibility. This explanation has not been tested experimentally, and confirming it would require friction measurements on the individual actuators. However, a closer look at Figure 15 reveals that while the middle plot shows some small trial-to-trial variations in the trajectories, the bottom plot confirms these are minor relative to the joint’s overall range of motion by illustrating the consistently low standard deviation. 

15 


**Figure 15.** Reproducibility results for the right elbow flexion joint (joint 6), which exhibited the highest error. Top: random input commands. Middle: 10 overlaid trajectories showing high consistency. Bottom: standard deviation over time, which remains small. 


**Figure 16.** Block diagram of the data collection framework. A PID controller drives the robot to follow a randomly generated trajectory, while a data logger records the resulting time-series data of commands and sensor values. 

The results indicate that the robot’s behavior is highly reproducible under the tested conditions. Given the same initial state and the same command sequence, the system follows a nearly identical trajectory. This deterministic nature, despite the underlying dynamic complexity, supports the feasibility of a data-driven approach for precise motion control. 

### **4. Data-Driven Trajectory Tracking Control** 

The experiments in Section 3 demonstrated that the robot, while exhibiting highly reproducible behavior, possesses complex, nonlinear dynamics and a significant actuation delay. These characteristics make it difficult to control accurately using traditional model-based controllers. This section presents a feasibility study on a data-driven controller designed to overcome these challenges. The approach involves two stages: (1) collecting a comprehensive dataset of the robot’s dynamic behavior, and (2) using this data to train an inverse dynamics model that explicitly compensates for the system’s time delay. 

### **_4.1. Motion Data Collection_** 

The first step is to create a rich dataset that captures the relationship between control inputs (valve commands) and system states (joint angles, velocities, and pressures) across a wide range of movements. Although the motion reproducibility experiment in Section 3.5 demonstrated reproducible behavior across all 13 joints, we focused on 

16 


**Figure 17.** An example of the collected time-series data for joint #9 (blue) and joint #10 (orange). The top plot shows the valve commands computed by the PID controller for Chamber A (solid lines) and Chamber B (dashed lines). These commands produce the measured chamber pressures shown in the middle plot. The bottom plot displays the randomly generated reference trajectories the controller was tasked to follow (dashed lines) and the robot’s actual tracked trajectories that resulted from the applied pressures (solid lines). 

an arm subsystem in this preliminary controller study to keep the learning problem tractable and to evaluate the time-delay compensation strategy under coupled multijoint motion. This subsystem was chosen for its functional significance and dynamic challenges. Functionally, the selected joints are the primary actuators responsible for positioning the arm in its workspace for representative tasks like reaching. Dynamically, they form a highly coupled system that includes joints heavily affected by gravity. Based on these criteria, we selected the 4-DOF subsystem comprising the left arm’s shoulder abduction (joint 9), shoulder flexion (joint 10), shoulder rotation (joint 11), and elbow flexion (joint 12). 

We identified the 4-DOF arm simultaneously so that the model could learn the dynamic coupling between joints directly from data. Even if single-DOF models were learned separately, coordinated 4-DOF motion would still require additional treatment of interaction effects among joints. These effects are not the rigid-body terms alone but load-dependent changes in the friction, delay, and stiffness of each actuator, as explained in Section 5.2. In addition, each joint has different actuator and transmission-tube characteristics. 

### _4.1.1. Data Generation Method_ 

To ensure the data contained sufficient dynamic richness for training, we used a simple PID controller to make the robot follow a randomly generated reference trajectory, as shown in the block diagram in Figure 16. It is important to note that the PID controller’s purpose was not to achieve perfect tracking, but merely to serve as a driver to generate smooth, continuous, and varied movements that explore the system’s state space. 

The random reference trajectory<sup>ref</sup> **_q_** ( _t_ ) was generated using a random walk, where the target angle for each joint was updated by a random increment at intervals chosen 

17 

steps sensor values valve commands 


**Figure 18.** Schematic of the data preprocessing to compensate for time delay. An input sample **_X_** _k_ is formed by concatenating current sensor values with desired future angles from _τ_ steps ahead, while the corresponding output **_y_** _k_ is the current valve command. All such samples are then stacked vertically as rows to create the final training matrices, **X** and **Y** . 

randomly between 0 _._ 1 and 1 _._ 0 s. The PID control law is given by: 


where **_K_** p _,_ d _,_ i are diagonal gain matrices and **_u_** 0 is a baseline pressure command vector that defines the joint’s passive stiffness. The manually tuned gains and baseline stiffness were set to **_K_** p = diag _{_ 5 _._ 48 _,_ 3 _._ 08 _,_ 3 _._ 64 _,_ 3 _._ 4 _}_ , **_K_** d = diag _{_ 0 _._ 044 _,_ 0 _._ 148 _,_ 0 _._ 016 _,_ 0 _._ 016 _}_ , **_K_** i = diag _{_ 0 _._ 0005 _,_ 0 _._ 0036 _,_ 0 _._ 001 _,_ 0 _._ 0009 _}_ , and **_u_** 0 = [400 _._ 0 _,_ 400 _._ 0 _,_ 400 _._ 0 _,_ 400 _._ 0]. Figure 17 shows a sample of the rich time-series data generated with this method. 

### _4.1.2. Collected Dataset_ 

The robot performed 100 trials, each lasting 60 seconds. During these trials, the valve commands ( **_u_**<sup>A</sup> , **_u_**<sup>B</sup> ), chamber pressures ( **_p_**<sup>A</sup> , **_p_**<sup>B</sup> ), joint angles ( **_q_** ), and joint velocities ( **_v_** ) were all recorded at 30 Hz. This process yielded a final dataset containing 180,000 time-stamped data points for the four selected joints. The robot operated continuously without malfunction, confirming its mechanical robustness for long-duration experiments of the developed robot. 

### **_4.2. Inverse Dynamics Model with Time-Delay Compensation_** 

### _4.2.1. Time-Delay Compensation via Data Preprocessing_ 

The goal of the controller is to find a function that maps a desired motion to the valve commands required to achieve that motion. We frame this as learning an inverse dynamics model, **_f_** : **_X_** _k →_ **_y_** _k_ , where **_X_** _k_ represents the robot’s current and desired future states and **_y_** _k_ is the corresponding actuation command vector needed to produce that outcome. As discussed in Section 5.2, the rigid-body gravitational and inertial loads are, in principle, computable, but accurate control of this robot requires the full mapping from desired motion to valve commands, which also includes actuator nonlinearities, transmission delay, friction, pressure dynamics, and the load-dependent coupling effects 

18 

among joints. In particular, this mapping is affected by actuator internal friction, which has been modeled for pneumatic actuators in prior studies [39,40], and by the attenuation and delay introduced by the long transmission tubes, which have also been studied in the literature [41,42]. However, identifying a sufficiently accurate control-oriented inverse model for the installed multi-DOF robot remains difficult in practice. Therefore, we employ a data-driven approach to learn this mapping directly from measured data in this preliminary study. 

A critical challenge is the actuation delay identified in Section 3.2. To compensate for this delay, we adopt a preview-inspired strategy in which future desired states are explicitly embedded in the input feature vector during data preprocessing. This idea is related to preview control [43,44], but it is implemented here in a data-driven framework rather than in a model-based controller. Recent data-driven studies on delay systems have mainly considered linear systems, including Smith-Predictor-based controller design for known delay and state-feedback design for linear systems with uncertain or unknown delay [45–47]. These studies derive controllers through explicit linear-system synthesis formulas, whereas our method learns a nonlinear inverse mapping with future reference information embedded directly in the input features. Previous studies on long-line pneumatic systems have mainly addressed delay using model-based methods on 1-DOF setups [36–38]. In contrast, our study examines this strategy on a coupled multi-DOF pneumatic subsystem of a compact humanoid robot. As illustrated in Figure 18, the input and output vectors for a single training sample at time _k_ are defined as: 


For the 4-DOF subsystem under study, the input vector **_X_** _k_ has a dimension of 20 (a concatenation of five 4-dimensional vectors), and the output vector **_y_** _k_ has a dimension of 8 (a concatenation of two 4-dimensional vectors). From a total of _K_ recorded time steps, we construct the full training dataset, consisting of an input matrix **X** _∈_ R<sup>(</sup><sup>_K−τ_)</sup><sup>_×_20</sup> and an output matrix **Y** _∈_ R<sup>(</sup><sup>_K−τ_)</sup><sup>_×_8</sup> . This formulation forces the model to learn the valve commands at the present time _k_ that will cause the robot to achieve the desired state at a future time _k_ + _τ_ . Based on our empirical results, the lookahead period _τ_ was set to 9 time steps (9 _×_ 33 _._ 3ms _≈_ 300ms). 

### _4.2.2. Model Architecture and Training_ 

A standard three-layer multilayer perceptron (MLP) was used as the function approximator for the inverse model. The network architecture included an input layer with a size of 20 to match the dimension of **_X_** _k_ , a hidden layer with 200 neurons using a hyperbolic tangent (tanh) activation function, and an output layer with a size of 8 to match the dimension of **_y_** _k_ . Before training, both the input feature matrix **X** and the output matrix **Y** were standardized by removing the mean of each column and scaling it to unit variance. 

19 


**Figure 19.** Control framework for trajectory tracking using the trained inverse dynamics model. The model acts as a feedback controller, taking current state and future desired angles to generate valve commands. 

### **_4.3. Evaluation of Tracking Performance_** 

### _4.3.1. Method_ 

To evaluate the trained model, we tasked it with tracking a new, unseen reference trajectory that was recorded by a human manually guiding the robot’s arm. This trajectory was not part of the training set. The control framework is shown in Figure 19. For any given recorded trajectory **_D_** _r_ , spline interpolation is used to generate a smooth, continuous desired trajectory<sup>ref</sup> **_q_** ( _t_ ). At each time step _k_ , the current sensor readings and the future desired angle<sup>ref</sup> **_q_** ( _k_ + _τ_ ) are fed into the trained MLP model, which outputs the valve commands **_y_** _k_ = [ **_u_**<sup>A</sup> ( _k_ ); **_u_**<sup>B</sup> ( _k_ )]. 

The performance of this data-driven controller was compared against the same PID controller used for data collection. Each controller attempted to track the same reference trajectory 10 times. 

### _4.3.2. Results_ 

The trajectory tracking results are shown in Figure 20, and the quantitative performance is summarized by the Root Mean Square Error (RMSE) in Figure 21. The results indicate that the data-driven controller outperforms the PID baseline on this task. The PID controller exhibits a consistent lag behind the reference trajectory, a direct consequence of the uncompensated system delay. Furthermore, it struggles to overcome gravity, noticeably undershooting the target angle when lifting the arm (e.g., the left shoulder flexion in Figure 20(b)). In addition, the PID controller produces jerky motion due to stick-slip phenomena, which is especially visible during slower movements (e.g., from 10–14 s in Figure 20(d)). 

In contrast, the trained model tracks the reference trajectory closely. It successfully compensates for both the time delay and gravitational effects, and it effectively smooths out the stick-slip behavior, producing a smoother trajectory by having learned the system’s nonlinear dynamics from the data. These visual findings are confirmed by RMSE values. For all four tested joints, the trained model achieves a lower tracking error than the PID controller. For the left shoulder flexion (joint 10), the data-driven controller reduced the RMSE from 8 _._ 79 to 1 _._ 17 in the normalized position unit defined in Section 3.1.2, a reduction of nearly 87%. 

These experiments support the potential of a data-driven approach. By explicitly structuring the training data to account for system delay, even a simple MLP can learn an effective inverse model for this coupled, nonlinear pneumatic subsystem and outperform a standard PID controller. Section 5.3 discusses what this evidence does and does not show. 

20 


**Figure 20.** Comparison of trajectory tracking performance for four left arm joints. The trained model (green) follows the reference trajectory (dashed blue) much more closely than the PID controller (orange), which exhibits significant lag and error. Shaded areas represent standard deviation over 10 trials. 

### **5. Discussion** 

The high reproducibility of the robot, confirmed in our experiments, suggests that it is a promising platform for human-robot interaction, although no interaction experiment with humans has yet been conducted. This section discusses the robot’s potential for expressive motion and then turns to the controller study: why the arm was identified as a whole, the limitations of the study, and the directions they suggest. 

### **_5.1. Implications for Expressive and Interactive Motion_** 

The robot’s capacity for high-speed motion, revealed in Section 3.4, is a foundation for creating dynamic behaviors. This capacity could allow for quick, reflexive motions, such as flinching from a sudden, painful stimulus. In the context of human-robot interaction, such reflexes could make the robot seem more alive, potentially leading to more natural and empathetic interactions. The inherent compliance of the pneumatic system is also a major advantage for creating intense, oscillatory movements, like shaking the hands and shoulders to express excitement. While traditional robots with rigid, high-gear-ratio electric motors risk mechanical failure, the compressed air in the actuators naturally absorbs these rapid, opposing forces, protecting the mechanism from damage. This allows for a unique class of dynamic, emotional expressions that are difficult to achieve safely with other actuation methods. 

Our experimental results from Section 3 also provide practical guidelines for designing effective movements. The performance difference between the easiest (Pose EP or EN) 

21 


**Figure 21.** Comparison of RMSE for the PID and the trained model controllers. The data-driven model achieves lower tracking error across all tested joints. 

and hardest (Pose HP or HN) conditions reveals a joint’s sensitivity to gravitational and inertial loads. For joints with high sensitivity, such as the shoulders, complex motions should be designed with consideration for the full arm’s posture; for instance, lifting the shoulder is more efficient if the elbow is first flexed to reduce the arm’s moment of inertia. The robot’s high motion reproducibility, a key feature achieved by its robust design featuring pneumatic rotary actuators and cylinders with rigid bodies, was validated by the results in Section 3.5. This property allows for identifying which joints are most consistent and therefore best suited for tasks requiring high precision. Conversely, joints with the highest maximum velocity are best for fast gestures. Finally, the minimum activation pressure results highlight the challenge of static friction, which must be considered when designing extremely slow and smooth movements to avoid jerky stick-slip motion. 

### **_5.2. Interaction Effects Among Joints_** 

As described in Section 4.1, the 4-DOF arm was identified simultaneously rather than joint by joint, and the interaction effects behind this choice should be clarified. The rigid-body coupling among the joints, that is, the inertial, Coriolis, centrifugal, and gravitational terms, can be computed from a dynamics model. However, the difficulty lies in the mapping from valve commands to joint torques, whose parameters change with the load imposed by the other joints. Experiments I-A and I-B in Sections 3.2 and 3.3 showed that both the transmission delay and the friction threshold depend on posture. In addition, the compressed air in the chambers should be treated as a configurationdependent elastic element. A single-DOF inverse model identified in isolation therefore does not transfer to coordinated motion. 

### **_5.3. Limitations of the Present Study_** 

This study has several limitations. All measurements come from one physical robot, the dynamic properties were measured on the waist and left arm on the assumption that the two arms behave alike, and the controller was trained and tested on the left arm only. The difference between joints 6 and 12 in Section 3.5 shows that their trial-to-trial errors differ, but we did not pursue this variability further. 

The controller is preliminary: a static three-layer MLP trained once on a fixed dataset, without a systematic hyperparameter search or an ablation of the lookahead period _τ_ , and with a constant delay assumed. It was compared only against a manually tuned 

22 

PID controller and not against other learning-based or model-based controllers, so the results demonstrate feasibility rather than state-of-the-art performance. It also controls only the 4-DOF arm subsystem rather than the whole 13-DOF body. 

The evaluation is also narrow. Tracking was tested on a single manually guided reference trajectory of moderate speed, with no payload change, external contact, or interaction with a human. 

### **_5.4. Performance and Future Directions for the Data-Driven Controller_** 

The successful trajectory tracking controller presented in Section 4 is a key contribution of this work. Its performance supports two premises. First, the robot system is sufficiently durable and reproducible for data-driven methods, as shown by its ability to collect 100 trials of continuous motion data without malfunction. Second, the proposed time-delay compensation strategy is effective. By training the MLP to look ahead by an interval _τ_ derived from our experiments, the controller mitigated the inherent time delay and outperformed the traditional PID controller. This result supports further study of data-driven controllers for similar pneumatic robots. 

Several directions for future work can be drawn from these results. The model was trained on moderately paced random motions, and its performance at the extremes of speed should be investigated. Tracking very fast movements is limited by the physical actuation delay, while tracking very slow movements is challenged by stick-slip effects. Furthermore, the controller’s reliance on a fixed future period for the reference trajectory may not be optimal for dynamically generated or reflexive movements. Since the MLP is a static mapping, a future direction is to explore models that consider the history of states and inputs, such as a recurrent neural network, to capture the delay that varies with the actuator state and external loads. Extending the data-driven controller to the full 13-DOF robot is another important next step. A more advanced challenge is enabling the controller to adapt to changes in dynamics, such as when picking up an object, which would require online learning or adaptive control techniques to adjust the model in real time. 

### **6. Conclusion** 

This paper presented the development and analysis of a compact, 13-DOF upper-body humanoid robot driven by pneumatic actuators. We conducted a series of experiments to systematically characterize its dynamic properties, which revealed a system that is complex and highly nonlinear, yet robust and reproducible within the tested conditions. A key challenge identified and quantified through these experiments was a significant time delay, primarily due to the long pneumatic transmission lines. 

To address these control challenges, we proposed and implemented a preliminary data-driven controller. The core of our approach was to train a multilayer perceptron as an inverse dynamics model, using a data structure specifically designed to compensate for the known system delay by incorporating future desired states into the model’s input. When evaluated on an unseen, manually guided trajectory, this controller achieved lower tracking errors than a standard PID controller, mitigating both the time delay and configuration-dependent gravitational effects. 

This work shows that a data-driven approach is a viable strategy for controlling a coupled 4-DOF pneumatic arm of this robot and a promising direction for the full 13DOF system. Within the tested conditions, it also establishes this robot as a durable and 

23 

reproducible platform for further work on adaptive control and on expressive motion for human-robot interaction. The limitations of the study, in particular that only one robot was tested and that the controller was compared only with a PID baseline, are discussed in Section 5.3. 

### **Funding** 

This work was supported in part by the project, JPNP16007, commissioned by the New Energy and Industrial Technology Development Organization (NEDO), and in part by JSPS KAKENHI Grant-in-Aid for Transformative Research Areas Grant Number JP 25H01236. 

### **References** 

- [1] Ikemoto S, Amor HB, Minato T, et al. Physical Human-Robot Interaction: Mutual Learning and Adaptation. IEEE Robotics & Automation Magazine. 2012 Dec;19(4):24–35. 

- [2] Ogenyi UE, Liu J, Yang C, et al. Physical Human–Robot Collaboration: Robotic Systems, Learning Methods, Collaborative Strategies, Sensors, and Actuators. IEEE Transactions on Cybernetics. 2021 Apr;51(4):1888–1901. 

- [3] Hosoda K, Sakaguchi Y, Takayama H, et al. Pneumatic-driven jumping robot with anthropomorphic muscular skeleton structure. Autonomous Robots. 2010 Apr;28(3):307–316. 

- [4] Vanderborght B, Van Ham R, Verrelst B, et al. Overview of the Lucy Project: Dynamic Stabilization of a Biped Powered by Pneumatic Artificial Muscles. Advanced Robotics. 2008 Jan;22(10):1027–1051. 

- [5] Shin D, Sardellitti I, Park YL, et al. Design and Control of a Bio-inspired Human-friendly Robot. The International Journal of Robotics Research. 2010 Apr;29(5):571–584. 

- [6] Niiyama R. Soft Actuation and Compliant Mechanisms in Humanoid Robots. Current Robotics Reports. 2022 Sep;3(3):111–117. 

- [7] Klute G, Hannaford B. Fatigue characteristics of McKibben artificial muscle actuators. In: Proceedings. 1998 IEEE/RSJ International Conference on Intelligent Robots and Systems. Innovations in Theory, Practice and Applications (Cat. No.98CH36190); Vol. 3; Oct.; 1998. p. 1776–1781 vol.3. 

- [8] Woods BK, Gentry MF, Kothera CS, et al. Fatigue life testing of swaged pneumatic artificial muscles as actuators for aerospace applications. Journal of Intelligent Material Systems and Structures. 2012 Feb;23(3):327–343. 

- [9] Billard A, Robins B, Nadel J, et al. Building Robota, a Mini-Humanoid Robot for the Rehabilitation of Children With Autism. Assistive Technology. 2007 Mar;19(1):37–49. 

- [10] Dautenhahn K, Nehaniv CL, Walters ML, et al. KASPAR – A Minimally Expressive Humanoid Robot for Human–Robot Interaction Research. Applied Bionics and Biomechanics. 2009;6(3-4):708594. 

- [11] Ishihara H, Asada M. Design of 22-DOF pneumatically actuated upper body for child android ‘Affetto’. Advanced Robotics. 2015 Sep;29(18):1151–1163. 

- [12] Ishihara H, Yoshikawa Y, Asada M. Realistic child robot “Affetto” for understanding the caregiver-child attachment relationship that guides the child development. In: 2011 IEEE International Conference on Development and Learning (ICDL); Vol. 2; Aug.; 2011. p. 1–5. 

- [13] Noritsugu T, Park JG. Improvement of Pneumatic Robot Control Using Disturbance Observer (in Japanese). Journal of the Robotics Society of Japan. 1994;12(4):590–595. 

- [14] Hoshino K. Control of Speed and Power in a Humanoid Robot Arm Using Pneumatic Actuators for Human-Robot Coexisting Environment. IEICE TRANSACTIONS on Information and Systems. 2008 Jun;E91-D(6):1693–1699. 

24 

- [15] Murayama E, Yogosawa Y, Kawakami Y, et al. Study on Control Performance with Consideration of Articulated Manipulators with Pneumatic Cylinders. International Journal of Automation Technology. 2014 Mar;8(2):159–168. 

- [16] Hoffmann K, M¨uller D, Simon R, et al. On trajectory tracking control of fluid-driven actuators. at - Automatisierungstechnik. 2021 Nov;69(11):970–980. 

- [17] Binnard MB. Design of a small pneumatic walking robot Thesis. Massachusetts Institute of Technology; 1995. 

- [18] Wait KW, Goldfarb M. A Pneumatically Actuated Quadrupedal Walking Robot. IEEE/ASME Transactions on Mechatronics. 2014 Feb;19(1):339–347. 

- [19] Minato T, Yoshikawa Y, Noda T, et al. CB2: A child robot with biomimetic body for cognitive developmental robotics. In: 2007 7th IEEE-RAS International Conference on Humanoid Robots; Nov.; 2007. p. 557–562. 

- [20] Todorov E, Hu C, Simpkins A, et al. Identification and control of a pneumatic robot. In: 2010 3rd IEEE RAS EMBS International Conference on Biomedical Robotics and Biomechatronics; Sep.; 2010. p. 373–380. 

- [21] Tassa Y, Wu T, Movellan J, et al. Modeling and identification of pneumatic actuators. In: 2013 IEEE International Conference on Mechatronics and Automation; Aug.; 2013. p. 437–443. 

- [22] Tanaka K, Nishikawa S, Niiyama R, et al. Immediate Generation of Jump-and-Hit Motions by a Pneumatic Humanoid Robot Using a Lookup Table of Learned Dynamics. IEEE Robotics and Automation Letters. 2021 Jul;6(3):5557–5564. 

- [23] Beater P. Pneumatic Drives: System Design, Modelling and Control. Berlin: Springer; 2007. 

- [24] Jamian S, Salim SNS, Kamarudin MN, et al. Review on controller design in pneumatic actuator drive system. TELKOMNIKA (Telecommunication Computing Electronics and Control). 2020 Feb;18(1):332–342. 

- [25] Parnichkun M, Ngaecharoenkul C. Kinematics control of a pneumatic system by hybrid fuzzy PID. Mechatronics. 2001 Dec;11(8):1001–1023. 

- [26] Hoˇsovsk´y A, Nov´ak-Marcinˇcin J, Pitel’ J, et al. Model-Based Evolution of a Fast Hybrid Fuzzy Adaptive Controller for a Pneumatic Muscle Actuator. International Journal of Advanced Robotic Systems. 2012 Aug;9(2):40. 

- [27] Hamiti K, Voda-Besan¸con A, Roux-Buisson H. Position control of a pneumatic actuator under the influence of stiction. Control Engineering Practice. 1996 Aug;4(8):1079–1088. 

- [28] Situm Z, Pavkovic D, Novakovic B. Servo Pneumatic Position Control Using Fuzzy PID Gain Scheduling. Journal of Dynamic Systems, Measurement, and Control. 2004 Aug; 126(2):376–387. 

- [29] Song J, Ishida Y. A robust sliding mode control for pneumatic servo systems. International Journal of Engineering Science. 1997 Jun;35(8):711–723. 

- [30] Bouri M, Thomasset D. Sliding control of an electropneumatic actuator using an integral switching surface. IEEE Transactions on Control Systems Technology. 2001 Mar;9(2):368– 375. 

- [31] Tsai YC, Huang AC. Multiple-surface sliding controller design for pneumatic servo systems. Mechatronics. 2008 Nov;18(9):506–512. 

- [32] Smaoui M, Brun X, Thomasset D. High-order sliding mode for an electropneumatic system: A robust differentiator–controller design. International Journal of Robust and Nonlinear Control. 2008;18(4-5):481–501. 

- [33] Rahman RA, He L, Sepehri N. Design and experimental study of a dynamical adaptive backstepping–sliding mode control scheme for position tracking and regulating of a lowcost pneumatic cylinder. International Journal of Robust and Nonlinear Control. 2016; 26(4):853–875. 

- [34] Ayadi A, Smaoui M, Aloui S, et al. Adaptive sliding mode control with moving surface: Experimental validation for electropneumatic system. Mechanical Systems and Signal Processing. 2018 Sep;109:27–44. 

- [35] Ren HP, Wang X, Fan JT, et al. Adaptive Backstepping Control of a Pneumatic System 

25 

- With Unknown Model Parameters and Control Direction. IEEE Access. 2019;7:64471– 64482. 

- [36] Yang B, Tan UX, McMillan AB, et al. Design and Control of a 1-DOF MRI-Compatible Pneumatically Actuated Robot With Long Transmission Lines. IEEE/ASME Transactions on Mechatronics. 2011 Dec;16(6):1040–1048. 

- [37] Turkseven M, Ueda J. Model-Based Force Control of Pneumatic Actuators With Long Transmission Lines. IEEE/ASME Transactions on Mechatronics. 2018 Jun;23(3):1292– 1302. 

- [38] Butt K, Sepehri N. A Nonlinear Integral Sliding Surface to Improve the Transient Response of a Force-Controlled Pneumatic Actuator With Long Transmission Lines. Journal of Dynamic Systems, Measurement, and Control. 2019 Sep;141(12). 

- [39] Khayati K, Bigras P, Dessaint LA. LuGre model-based friction compensation and positioning control for a pneumatic actuator using multi-objective output-feedback control via LMI optimization. Mechatronics. 2009 Jun;19(4):535–547. 

- [40] Schl¨uter MS, Perondi EA. Mathematical modeling of pneumatic semi-rotary actuator with friction. Journal of the Brazilian Society of Mechanical Sciences and Engineering. 2018 Oct;40(11):523. 

- [41] Krichel SV, Sawodny O. Non-linear friction modelling and simulation of long pneumatic transmission lines. Mathematical and Computer Modelling of Dynamical Systems. 2014 Jan;20(1):23–44. 

- [42] Kern R. Physical modelling of a long pneumatic transmission line: Models of successively decreasing complexity and their experimental validation. Mathematical and Computer Modelling of Dynamical Systems. 2017 Sep;23(5):536–553. 

- [43] Birla N, Swarup A. Optimal preview control: A review. Optimal Control Applications and Methods. 2015;36(2):241–268. 

- [44] Liao Y, Liao F. Design of Preview Controller for Linear Continuous-time Systems with Input Delay. International Journal of Control, Automation and Systems. 2018 Jun; 16(3):1080–1090. 

- [45] Formentin S, Corno M, Savaresi SM, et al. Direct data-driven control of linear time-delay systems. Asian Journal of Control. 2012;14(3):652–663. 

- [46] Rueda-Escobedo JG, Fridman E, Schiffer J. Data-Driven Control for Linear Discrete-Time Delay Systems. IEEE Transactions on Automatic Control. 2022 Jul;67(7):3321–3336. 

- [47] Portilla G, Seuret A, Mondi´e S. Robust data-driven control for linear discrete-time systems with unknown delay. IFAC-PapersOnLine. 2025 Jan;59(13):231–236. 

26 

