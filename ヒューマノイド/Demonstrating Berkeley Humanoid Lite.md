---
title: "Demonstrating Berkeley Humanoid Lite: An Open-source, Accessible, and Customizable 3D-printed Humanoid Robot"
date: "2025-04-24"
authors: "Yufeng Chi; Qiayuan Liao; Junfeng Long; Xiaoyu Huang; Sophia Shao; Borivoje Nikolic"
venue: "RSS 2025"
url: https://arxiv.org/abs/2504.17249
pdf: https://arxiv.org/pdf/2504.17249
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2504.17249)** / [論文ページ](https://arxiv.org/abs/2504.17249)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# Demonstrating Berkeley Humanoid Lite: An Open-source, Accessible, and Customizable 3D-printed Humanoid Robot 

Yufeng Chi, Qiayuan Liao, Junfeng Long, Xiaoyu Huang, Sophia Shao, Borivoje Nikolic, Zhongyu Li, Koushil Sreenath University of California, Berkeley 

**_Abstract_ —Despite significant interest and advancements in humanoid robotics, most existing commercially available hardware remains high-cost, closed-source, and non-transparent within the robotics community. This lack of accessibility and customization hinders the growth of the field and the broader development of humanoid technologies. To address these challenges and promote democratization in humanoid robotics, we demonstrate Berkeley Humanoid Lite, an open-source humanoid robot designed to be accessible, customizable, and beneficial for the entire community. The core of this design is a modular 3D-printed gearbox for the actuators and robot body. All components can be sourced from widely available e-commerce platforms and fabricated using standard desktop 3D printers, keeping the total hardware cost under $5,000 (based on U.S. market prices). The design emphasizes modularity and ease of fabrication. To address the inherent limitations of 3D-printed gearboxes, such as reduced strength and durability compared to metal alternatives, we adopted a cycloidal gear design, which provides an optimal form factor in this context. Extensive testing was conducted on the 3D-printed actuators to validate their durability and alleviate concerns about the reliability of plastic components. To demonstrate the capabilities of Berkeley Humanoid Lite, we conducted a series of experiments, including the development of a locomotion controller using reinforcement learning. These experiments successfully showcased zero-shot policy transfer from simulation to hardware, highlighting the platform’s suitability for research validation. By fully open-sourcing the hardware design, embedded code, and training and deployment frameworks, we aim for Berkeley Humanoid Lite to serve as a pivotal step toward democratizing the development of humanoid robotics. All resources are available at https://lite.berkeley-humanoid.org.** 

## I. INTRODUCTION 

Humanoid robotics has gained substantial attention in research and industry, yet its accessibility remains a significant challenge. Most existing humanoid platforms are either commercial products with closed-source designs, high costs, and limited customizability, or research prototypes that require specialized manufacturing processes, making them inaccessible to the broader robotics community. This restricts innovation, as researchers, educators, and hobbyists face barriers in developing, modifying, and testing new ideas. Without affordable and customizable platforms, progress in fields such as reinforcement learning for bipedal locomotion, human-robot interaction, and robotic manipulation is hindered. Therefore, addressing the lack of open-source, cost-effective, and easily 


Fig. 1. Berkeley Humanoid Lite. An open-source, accessible, and customizable bipedal humanoid robot platform. 

reproducible humanoid robot designs is crucial for democratizing robotics research and accelerating advancements in humanoid technologies. 

Developing an open-source, cost-effective, and fully functional humanoid robot presents several challenges. First, humanoid robots require complex actuation mechanisms to achieve smooth and stable locomotion. While highperformance actuators exist, they are often expensive and proprietary, limiting accessibility. Prior research has explored various actuator designs, including planetary gear systems, belt-driven actuators, and quasi-direct drives, each with tradeoffs in cost, efficiency, and complexity. However, few solutions provide both affordability and reliability while maintaining open-source availability. Second, fabrication and assembly constraints further complicate accessibility. Many researchoriented humanoid platforms rely on CNC machining, laser 

cutting, or custom-milled components, which demand specialized manufacturing facilities. Open-source alternatives attempt to lower this barrier by utilizing 3D printing. Finally, it remains difficult to ensure durable real-world performance. Humanoid robots must withstand continuous operational stresses while maintaining precise motion control. The use of 3D-printed components, while improving accessibility, introduces durability concerns due to material limitations such as reduced stiffness and wear over time. Thus, designing a humanoid platform that balances accessibility, modularity, and long-term reliability remains an open challenge in robotics research. 

To address these challenges, we introduce Berkeley Humanoid Lite, an open-source, mid-scale humanoid robot platform designed for accessibility, affordability, and customizability. Our approach leverages 3D-printed cycloidal gear actuators, which balance cost-effectiveness with sufficient mechanical robustness, reducing dependency on expensive, proprietary actuators. By optimizing the actuator design and employing widely available components, our platform ensures that researchers and hobbyists can build and modify the robot without requiring specialized manufacturing facilities. To enhance fabrication accessibility, we focus on modular and scalable design principles. All structural components can be 3D-printed using standard desktop printers, and all electronic and mechanical parts can be sourced from common online vendors. This approach significantly lowers the barriers to entry for constructing and maintaining a humanoid robot, making it feasible for a wider range of users. Furthermore, we demonstrate the real-world viability of our platform through experiments in locomotion and teleoperation. By implementing a reinforcement learning-based locomotion controller, we achieve zero-shot policy transfer from simulation to hardware, validating the effectiveness of our actuator design in dynamic tasks. Additionally, the teleoperation system enables real-time manipulation tasks, further showcasing the robot’s adaptability for research and education. By making the hardware design, embedded system code, and training frameworks fully opensource, we aim to democratize humanoid robotics research. Our contribution is to provide an accessible, customizable, and cost-effective platform, encouraging broader participation in humanoid development and innovation. 

The main contributions of this work are summarized as follows: (1) We introduce a humanoid robot platform that is accessible and customizable. (2) We demonstrate the platform’s capability for locomotion and whole-body control tasks. (3) We provide a fully open-source hardware and software stack with accompanying detailed instructions, enabling researchers and enthusiasts worldwide to replicate, customize, and improve upon our platform. 

## II. RELATED WORKS 

Our focus is on open-source, accessible, and customizable actuators for robotics applications, as well as robot platforms that can be easily adopted by academic labs and research groups. 

## _A. Actuators_ 

Actuators play a crucial role in robotic platforms, directly impacting performance, efficiency, and capabilities. Various design configurations have been explored to optimize robotic actuators. Katz [14] developed a fully open-source, highperformance, proprioceptive actuator, including a custom motor driver for quadrupedal robots. Their design utilizes an offthe-shelf motor and a planetary gear component set, requiring modifications to both the motor and gears, along with a custom aluminum housing. Gealy et al. [10] employed belt reduction systems as modular actuators for the arm. Similarly, Kau et al. [15] demonstrated promising results in quadrupedal robotics by utilizing belt drive and ODrive [25] as the motor controller, however, their design features a low gear ratio and lacks modularity. In addition, Grimminger et al. [12] and W¨uthrich et al. [39] presented a series of open-source works incorporating belt reduction and custom motor drivers for small-scale legged robots. Urs et al. [36] introduced a 3D-printed planetary gearbox combined with the Moteus [23] motor driver, though their approach requires a resin 3D printer. Azocar et al. [4] developed fully open-source actuators with planetary gearing for prosthetic applications, but their method necessitates CNC machining. Furthermore, Roozing and Roozing [30] investigated the design considerations for manufacturing cycloidal gearboxes using Fused Deposition Modeling (FDM) 3D printing. In a subsequent study, Roozing and Roozing [31] proposed a non-pinwheel design, optimizing the form for 3D-printed actuators. Their research highlights the feasibility of integrating 3D-printed cycloidal drives into actuators, paving the way for low-cost, accessible, and reliable robotic systems. 

## _B. Humanoids_ 

Existing humanoid robot platforms generally fall into three categories: commercial proprietary systems, research lab designs, and open-source community projects. 

Commercial platforms—such as Agility Robotics’ Digit [1], Fourier Intelligence’s GR1 [9], Westwood Robotics’ THEMIS [2], OpenLoong FXV2750 [26], and NAO H25 [24]—are engineered for robust execution. However, their substantial price tag renders them largely inaccessible to most research groups and the broader robotics community. Although lower-cost alternatives like Unitree’s H1 [35] and G1 [34] are available, their closed-source architecture restricts user modifications and complicates repairs, limiting customization for research applications. 

Research labs have also been developing in-house humanoid robots that offer high degrees of freedom (DoF) and substantial torque, serving as advanced platforms for investigating humanoid robot control [13, 22, 27]. More recently, smaller-scale robots—such as Berkeley Humanoid [20], MIT Humanoid [32], Wukong [38] and many others [18, 21, 33, 40, 41]—have been introduced with a focus on agile locomotion. Although these platforms achieve high performance and are well-suited for reinforcement learning applications, their limited production quantities typically confine their use 


Fig. 2. Main components and key dimensions of the limbs of the Berkeley Humanoid Lite. 

to a few institutions. Furthermore, these designs often depends on advanced manufacture techniques such as CNC machining and laser cutting, which are only available at select academic institutes. Expensive components are also used which restricts adaptability and broader adoption. As a result, the need for specialized manufacturing facilities and expertise significantly limits the accessibility of these platforms to the wider research community and hobbyists. 

Open-source community projects offers a more accessible alternative. However, many still depend on custom parts that requires CNC manufacturing [28]. Other projects, such as the Poppy Humanoid [16], OP3 [29], and NimbRo-OP2 [8], take advantage of 3D printing and utilize servo motors as the joints. This approach lowers the manufacturing barrier by enabling fabrication with desktop 3D printers. Nevertheless, servos typically lack backdrivability and exhibit high reflected inertia, making them slower and less suitable for scaling up to mid-scale or larger humanoid platforms. 

To address these challenges, we introduce Berkeley Humanoid Lite, a modular, mid-scale humanoid robot platform that emphasizes both accessibility and customization. Berkeley Humanoid Lite is designed to lower the barrier to entry, enabling a broader community of researchers and hobbyists to engage in humanoid robotics research and innovation. 

## III. SYSTEM DESIGN 

## _A. Overview_ 

The Berkeley Humanoid Lite is a mid-scale humanoid robot platform that is designed with accessibility and customizability in mind. The main components of the robot are shown in Figure 2. The robot weighs 16 kg and stands 0.8 m tall. Two sizes of actuators, each incorporating a 3D-printed cycloidal gearbox, directly drive the joints in the legs and arms. The torso is built with aluminum extrusions to support mounting additional components, and a cellphone-grade IMU is positioned near the center of the torso. 


Fig. 3. Comparison between existing robot platforms. Y-axis shows the performance factor _p_ ˆ defined in (1), representing the average peak torque normalized by the weight and height of the robot. A higher performance-perdollar _φ_ , defined in (2), indicates better cost-effectiveness, and open-source hardware and software platform enables customization towards specific user requirements. 

High-speed and low-latency communication between the actuators, the IMU, and the controller is crucial to achieve smooth motion. An Intel N95 mini PC located at the center of the torso serves as the low-level control computer. Each limb’s joint actuators are connected via a 1 Mbps CAN 2.0 bus and the four buses interface to the computer through USB-CAN adapters. The IMU is connected over USB through an Arduino microcontroller. The communication rate to both the actuators and IMU is configured to be 250 Hz. RL-based locomotion policies are also deployed on the same computer, with details provided in Section V-A. 

The robot is powered by an onboard 6S 4000 mAh Lithium Polymer (LiPo) battery that provides approximately 30 minutes of operation. Tethering to an external power supply is also supported for extended testing sessions. 

Apart from the non-standard structural parts, which are printed on a common desktop 3D printer, all components can be purchased from major online vendors in multiple countries. These design choices reflect the goal of creating an accessible and customizable humanoid platform. 

## _B. Performance Factor_ 

To be able to benchmark against other robots and illustrate our focus on accessibility and customizability while maintaining sufficient performance, we adopt the quantitative performance metric proposed by Shi et al. [33], with a minor modification. Specifically, we normalize the metric by the number of joints, and define the performance factor as the average peak torque of all actuated DoFs, normalized by the robot’s height and weight: 


where _N_ denotes the number of actuated DoFs, _h_ and _mg_ represent the height and weight of the robot, and _|τi_<sup>_max_</sup> _|_ represents the maximum torque of the i-th joint motor. To incorporate cost-effectiveness into consideration, the performance- 


Fig. 4. Exploded and cross-sectional views of the 6512 actuator. All of the components are either 3D-printed or sourced from online marketplaces. 

per-dollar is then defined as the performance factor divided by the cost or selling price of the robot: 


As shown in Fig. 3, our platform achieves a high performance factor with a cost lower than $5000. 

## _C. Design Towards Accessibility_ 

A key priority in developing Berkeley Humanoid Lite is to make the hardware platform accessible to a wide range of users. To realize this goal, the design process emphasizes widely available components, straightforward fabrication methods, and overall cost control. 

_1) Component Availability:_ Many open-source robot designs depend on specialized components, such as custom thrust bearings or high-performance motor drivers, which can be difficult to source. In contrast, Berkeley Humanoid Lite relies on parts from commonly used online marketplaces, notably Amazon and Taobao (AliExpress), for most offthe-shelf elements. Electronic components are obtained from reputable suppliers such as Digikey and Mouser. By selecting parts that are broadly available in multiple countries, Berkeley Humanoid Lite minimizes supply barriers and ensures that users can acquire necessary materials without extensive lead times or geographic restrictions. 

_2) 3D Printing:_ Recent advances in desktop 3D printing technology have made Fused Deposition Modeling (FDM) more accessible and reliable. Accordingly, Berkeley Humanoid Lite employs FDM to fabricate all non-standard structural parts. Polylactic Acid (PLA) is selected as the filament material for its robust mechanical properties and favorable printing characteristics. Although 3D-printed plastic parts introduce challenges—such as lower material strength, manufacturing variances, and anisotropic properties—Berkeley Humanoid Lite mitigates these concerns by adopting cycloidal gearboxes in its actuators. Cycloidal gears distribute loads over multiple teeth and accommodate the limited resolution of desktop 3D printers more effectively than planetary gears, thus enhancing reliability [30]. As shown in Figure 4, additional reinforcements, such as through-screws and embedded brass hex stands, help prevent failures along layer boundaries and bolster overall load capacity. Certain subcomponents are merged into single 

TABLE I 

BILL-OF-MATERIALS (BOM) OF THE 6512 ACTUATOR 

|Item|Cost (US)|Cost (China)|
|---|---|---|
|M6C12 BLDC Drone Motor|$129|$124|
|B-G431B-ESC1 Motor Driver|$19|$23|
|AS5600 Position Encoder|$3|$1|
|Bearings|$23|$4|
|Fasteners|$5|$1|
|3D Printed Parts|$4|$1|
|Misc (Cables, Connectors)|$5|$3|
|Total|$188|$157|


All values are rounded to the nearest dollar. 

TABLE II BILL-OF-MATERIALS (BOM) OF THE 5010 ACTUATOR 

|Item|Cost (US)|Cost (China)|
|---|---|---|
|5010 BLDC Drone Motor|$84|$62|
|B-G431B-ESC1 Motor Driver|$19|$23|
|AS5600 Position Encoder|$3|$1|
|Bearings|$18|$3|
|Fasteners|$4|$1|
|3D Printed Parts|$3|$1|
|Misc (Cables, Connectors)|$5|$3|
|Total|$136|$94|


All values are rounded to the nearest dollar. 

3D prints to reduce weight and avoid potential stress concentrations around fasteners. To maintain compatibility with standard desktop machines, every part is designed to fit within a 200 mm × 200 mm × 200 mm build volume. 

_3) Low Cost:_ We detail the component costs in the United States and China to illustrate the affordability of Berkeley Humanoid Lite. Tables I and II summarize the expenses for the two actuator designs, while Table III presents the total cost for the assembled robot. Beyond raw materials, the time for building and repairing the robot also factors into overall expense. For Berkeley Humanoid Lite, most off-the-shelf parts ship within a week in both the United States and China, custom parts can be printed within a week, and the entire robot can be assembled in about three days. Broken actuators can also be easily swapped out and repaired. These considerations minimize repair downtime and lower the barrier to entry for constructing and maintaining a mid-scale humanoid robot. 

As a concrete example, for the 6512 actuator, we chose the widely available 6811ZZ ball bearing to define the overall actuator size. The M6C12 150KV BLDC drone motor from MAD Components is used to drive the actuator, which strikes a good balance between availability, performance, and cost. We then opted for the B-G431B-ESC1 as the motor driver, favoring its affordability and ready availability at Mouser and Digikey. Although alternatives like the Moteus Controller [23], ODrive [25], or VESC [37] can also be used, we prioritized cost-effectiveness and consistent supply. The housing, cycloidal gear, input shaft, and output shaft are all 3D printed, with a brass hex stand embedded in the input shaft to boost stiffness and improve torque transfer from the motor to the cycloidal disks. 

TABLE III 

BILL-OF-MATERIALS (BOM) OF A HUMANOID ROBOT 

|Item|Cost (US)|Cost (China)|
|---|---|---|
|Mini PC|$129|$223|
|USB-CAN Adapters (4x)|$68|$43|
|USB Hubs (2x)|$36|$11|
|BNO085 IMU|$13|$12|
|6S LiPo Battery|$70|$81|
|6512 Actuators (10x)|$1,880|$1,563|
|5010 Actuators (12x)|$1,632|$1,130|
|Grippers (2x)|$72|$44|
|Aluminum Extrusions|$39|$3|
|3D Printed Components|$200|$84|
|Misc. Structural Components|$50|$14|
|Misc. Electronic Components|$123|$28|
|Total|$4,312|$3,236|


All values are rounded to the nearest dollar. 


Fig. 5. An alternative adult-sized robot configuration with 7 degrees-offreedom leg and dexterous hand. Carbon fiber tubes that are also available from online vendors are used to increase the length of the legs to match an average adult. Colors are used to show joint orientation (green: thigh pitch; red: abduction; blue: thigh rotation). _D. Design Towards Customization_ In addition to accessibility, Berkeley Humanoid Lite is designed to be highly customizable. Different research objectives and tasks may require variations in robot dimensions and joint configurations, and the flexibility of 3D printing makes it straightforward to adapt the robot’s morphology to suit specific needs. 

_1) Flexible Configurations:_ Since each joint in Berkeley Humanoid Lite is driven by a self-contained actuator with no additional linkages, adjusting the link length between adjacent joints is straightforward. As illustrated in Figure 5, extending the leg links with carbon fiber tubes transforms Berkeley Humanoid Lite into an adult-scale platform. Joint orders are also easily interchangeable: while most humanoid robots use three consecutive revolute joints at the hip to approximate a ball joint, variations in joint arrangement and orientation can significantly influence range of motion, power consumption, and efficiency [42, 43]. Figure 5 also illustrates an alternative hip configuration that is commonly employed in other humanoids. By streamlining these modifications, Berkeley 


Fig. 6. With minimal modifications, the modular joint actuators can be arranged to form different robot morphologies. Example forms include quadruped (top-left), biped (top right), Centaur-like (bottom-left), and mobile base (bottom-right). 

Humanoid Lite enables rapid prototyping and comparative evaluation of different hip designs on real hardware. 

_2) Different Morphologies:_ Berkeley Humanoid Lite’s actuators require only power and CAN communication, which allows each CAN bus to support up to 64 devices. This benefit makes it easy to reconfigure the robot into a variety of morphologies. Figure 6 highlights examples of a quadruped, a biped, a Centaur-like arrangement, and a mobile base platform, illustrating how the 3D-printed structure and self-contained actuators can be adapted for diverse robotic designs with minimal changes. 

## IV. ACTUATOR EVALUATION 

A reliable actuator is fundamental to the robot’s overall performance. To assess the capabilities of our proposed design, we conducted a set of experiments under conditions identical to those on the robot, including a 24 V power supply, identical position PD gains, and matching position, torque, and current bandwidth configurations. For further verification, we cross-validated the outcomes obtained with our custom motor controller and firmware against those produced by an off-theshelf Moteus Controller. 

## _A. Power Efficiency_ 

To evaluate the actuator’s power efficiency, we employed a custom dynamometer stand (Figure 7). The actuator under test was operated in torque-control mode, while a secondary damping actuator—run in velocity-control mode—held the system at a constant rotational speed. Torque produced by the primary actuator was measured with two load cells. An electrical-power measurement board logged the supply voltage and current, from which electrical input power was calculated. Mechanical output power was obtained by multiplying the measured torque by the measured rotational velocity. Mechanical efficiency is defined as the ratio of the measured 


Fig. 7. Power efficiency test setup. Two load cells are used to directly measure the torque of the actuator under test, while another actuator acts as a damper, absorbing the mechanical energy produced by the actuator under test. 

mechanical power to the absolute value of the product of the commanded torque and velocity, which represents the efficiency of the cycloidal gear reducer. Total efficiency was defined as the ratio of the measured mechanical power to the electrical input power, thereby reflecting the overall actuator efficiency, which includes motor copper losses, driver electrical losses, and mechanical losses. 

We tested the actuator across three different speeds that correspond to its typical operating range on the robot. Each torque and speed command was maintained for one second prior to measurement to minimize transient effects. As shown in Figure 8, the measured efficiency trends align with previous findings [17, 36], demonstrating a decline in efficiency at higher torque and speed settings. The gearbox exhibits a mechanical efficiency of approximately 90% across most operating conditions. However, at high torque and velocity, efficiency decreases due to heat generation. 

## _B. Transmission Stiffness_ 

We characterized the actuator’s transmission stiffness by rigidly fixing the output shaft relative to the actuator housing and measuring motor displacement under a range of static torques. The torque command was gradually ramped from 0 Nm to 20 Nm and back in both directions. A linear fit was then applied to the data collected from 4 Nm to 10 Nm, and the inverse of the slope yielded a stiffness of approximately 319.49 Nm _/_ rad (Figure 9). This profile shape is consistent with previous measurements of 3D-printed cycloidal reducers reported by Roozing and Roozing [31], who measured a substantially higher stiffness of about 1468 Nm _/_ rad for a similar 3D-printed cycloidal reducer. The observed reduction in stiffness is likely attributable to the lower strength of PLA compared to the carbon fiber reinforced polyamide (PA-CF) material used in that study. 


Fig. 8. Efficiency of the 6512 actuator (top), and the 5010 actuator (bottom). Mechanical efficiency is calculated as the ratio between the measured mechanical power to the product of the commanded torque and velocity, whereas total efficiency is defined as the ratio of the measured mechanical power to the electrical input power. The results indicate that, under most operating conditions, the gearbox maintains high efficiency. 


Fig. 9. Transmission stiffness measurement. The output of a 6512 actuator was fixed while the motor’s command torque was gradually increased. The rotor position was recorded, yielding a mean stiffness of 319 N m. 

## _C. Durability_ 

A primary concern for any 3D-printed actuator is its operational lifespan. We conducted a 60-hour durability test in which the actuator repeatedly lifted a pendulum (0.5 kg, 0.5 m) through a range of -45 degrees to +90 degrees at a frequency of 0.5 Hz. At one-hour intervals for the first 12 hours—and every 12 hours thereafter—we paused the test to measure both efficiency (using the same dynamometer stand) and backlash. 

As shown in Figure 10, efficiency initially declined but later returned to near its original level, aligning with observations reported by Urs et al. [36]. Although backlash increased slightly as the 3D-printed parts experienced wear, it remained 


Fig. 10. Average total efficiency and backlash measured during the 60-hour durability test of the 6512 actuator. The efficiency remains stable throughout the test, while backlash progressively increases due to wear. 


Fig. 11. Average efficiency and torque tracking error at 1 rad s<sup>_−_1</sup> across six 6512 actuator samples printed on two different 3D printers (P1 and P2). 

within acceptable limits throughout the 60-hour test. 

## _D. Consistency Across Units_ 

The performance might vary across actuator parts printed under different environment conditions and with different printers. To demonstrate the consistency of our design, we performed the efficiency evaluation on six actuators printed on two different 3D printers. The efficiency and torque tracking error, shown in Figure 11, are consistent across units. The torque error remains within _±_ 0 _._ 5 N m throughout the operating range. This confirms low inter-sample variance and confirms that the actuator design is robust across different fabrication sources. 

## _E. Position Tracking Accuracy_ 

Gear-backlash is the dominant steady-state source of position error in our actuator stack. Therefore, we evaluate the position tracking accuracy of individual actuator modules by measuring backlash on six freshly printed 6512 actuators. The maximum observed backlash was 0 _._ 0229 rad with a standard deviation of 0 _._ 0042 rad. 

To evaluate the system-level performance, we assembled five actuators into a 5-DoF serial arm and commanded it to reach four spatial targets (Figure 12). Each target was repeated 100 times while the end-effector pose was captured by the SteamVR-based motion-tracking setup described in 


Fig. 12. (Left) The 5-DoF arm is commanded to reach four spatial position targets. (Right) End-effector position variance over 100 repetitions of the reaching task. 


Fig. 13. Teleoperation setup. Two SteamVR base stations are used to track the global position of the controller. The motion is then synchronized to the robot through our teleoperation software stack. 

section V-B. The results show consistent positioning with standard deviation of 3 _._ 433 mm. 

## V. EXPERIMENTS 

In this section, we evaluate Berkeley-Humanoid’s ability to perform standard tasks of interest in humanoid robotics research. To this end, we conduct experiments in two key domains: locomotion and manipulation. 

## _A. Legged Locomotion_ 

Our design serves as a robust platform for investigating humanoid robot locomotion. Notably, we achieve a direct simto-real transfer of an Isaac Gym-trained policy to the physical robot without relying on additional state estimation methods. We formulate the locomotion task as a Partially Observed Markov Decision Process (POMDP) and use a standard Proximal Policy Optimization (PPO) algorithm to learn a control 


Fig. 14. Snapshot of the robot in biped configuration walking forward with a trained RL policy. The robot is able to track a user commanded velocity. 


Fig. 15. Snapshot of teleoperated manipulation experiments, including four tasks: writing, unpacking and packing, picking and placing blocks, and solving Rubik’s Cube. 

policy. The policy receives proprioceptive observations from the robot hardware: (a) the base angular velocity, (b) the projected gravity vector, and (c) joint positions and velocities. Additional inputs include the commanded linear velocity provided by the user and the previous time-step action. The policy outputs desired joint positions to the joint actuators. During deployment, the multi-layer perception (MLP) policy runs onboard the robot at 25 Hz. Figure 14 shows snapshots of the robot walking in the bipedal configuration under the trained reinforcement learning policy that follows user-specified velocity commands. Notably, the experiment utilized only 30% of the actuator’s torque limit, suggesting that the actuators are 

operating well within their capacity. This observation implies that the same actuator design could support a larger humanoid robot—such as the example presented in the previous section—without compromising performance. 

## _B. Teleoperated Manipulation_ 

The two 5-DOF arms and integrated grippers enable the robot to serve as an effective platform for bimanual manipulation research. To demonstrate its capabilities, we implemented a teleoperation system that leverages a motion capture setup built with SteamVR base stations and controllers. This system provides real-time tracking of the global position and orientation of the operator’s hand. The SteamVR tracking system was 

chosen for its broad support within the OpenXR ecosystem and its cost-effectiveness. However, our open-source software stack is designed for flexibility and can be readily adapted to incorporate alternative tracking solutions, such as Apple Vision Pro, Meta Quest, OptiTrack, or Xsens, to suit a variety of research needs. Our setup is shown in Figure 13. 

Our teleoperation system offers two distinct operational modes: Headless Mode and VR Mode, providing flexibility for diverse user needs and environments. Both modes leverage a unified inverse kinematics (IK) pipeline based on the Pink and Pinocchio library [5, 6, 7]. Headless mode facilitates a “third-person” perspective, ideal for users without access to a VR display. In this configuration, the system interprets the position and orientation changes of controllers relative to the global coordinate frame. This allows the operator to intuitively control the robot by observing its actions from an external viewpoint, similar to controlling a character in a video game. In addition, the user can engage and disengage anytime, allowing for comfortable adjustment of their gesture. VR mode delivers an immersive, first-person control experience. It directly maps the position and orientation changes of controllers within the user’s local coordinate frame to the robot’s local coordinate frame. This “body-ownership” approach enables operators to perform manipulations as naturally as they would with their own hands in a real-world setting, fostering a strong sense of presence and control. Both modes utilize the same robust IK solver built upon the Pink and Pinocchio library [5, 6, 7]. This ensures consistent and reliable translation of the desired end-effector poses into corresponding robot joint configurations, regardless of the chosen operational mode. As shown in Figure 15, we are able to use this setup to (a) write with a marker (b) unpack and pack a box, (c) solve a Rubik’s Cube, and (d) pick and place blocks. 

## _C. Potential Applications_ 

We further discuss potential extensions of Berkeley Humanoid Lite’s components, particularly in engineering education and animatronics. Given its open-source and accessible modular design, we anticipate a broader range of applications emerging with contributions from the robotics community. 

_1) Education:_ The 3D-printed actuator is an effective teaching tool for engineering education. In mechatronics classrooms, its accessibility enables students to gain hands-on experience with motor actuator components, including gear reduction, the motor, and its driver board. Notably, the 6512 actuator is already utilized in the UC Berkeley MECENG 102B class to demonstrate the working principle of a cycloidal drive. Its open-source and easily fabricated design allows students to experiment with different gear types beyond cycloidal gears or use modular actuators to build their own robots. In control courses, students can develop their own FOC algorithms based on motor models or use the actuator to create an inverted pendulum testbed for controller evaluation. In robotics courses, they can conduct hands-on experiments with existing robots to implement class-taught algorithms, such as motion planning, reinforcement learning, or imitation learning. The system’s 


Fig. 16. An anime-style head is integrated into the robot, enabling it to embody expressive and visually appealing anime characters while enhancing its overall aesthetic and potential for engaging human-robot interaction. 

modular, accessible, and easily repairable design also benefits instructors, allowing for quick replacement of broken parts. Beyond higher education, this platform can also inspire and engage middle and high school students in robotics. 

_2) Animatronics:_ Due to its modularity and lightweight design, the Berkeley Humanoid Lite can also serve as an animatronics platform for entertainment, as demonstrated in Figure 16. By refining its form to enhance expressiveness—incorporating features such as cuteness and vividness [3]—the robot can achieve a more engaging and visually appealing presence. Moreover, employing body motion design techniques inspired by animation can generate expressive movements, which the physical robot can execute using the control methods detailed in [11, 19]. With its low cost, ease of fabrication and straightforward repairability, Berkeley Humanoid Lite presents a promising platform for entertainment applications, particularly in settings aimed at young audiences. 

## VI. LIMITATIONS 

One limitation of this work is the insufficient study of thermal effects on the 3D-printed structure during prolonged operation, which could impact both mechanical strength and 

overall system reliability. Future iterations will include more rigorous thermal testing and structural refinements to address these concerns. Beyond the robot morphologies presented in this work, there are more potential new morphologies that can be explored and made openly available. 

## VII. CONCLUSION 

In this work, we introduced an affordable, mid-scale humanoid robot platform that significantly lowers the barriers to entry for researchers, educators, and hobbyists alike. By leveraging 3D-printed cycloidal actuators, off-the-shelf components, and a fully open-source hardware and software stack, we demonstrated that effective humanoid systems need not rely on proprietary, high-cost solutions. We evaluated the reliability and versatility of the 3D-printed actuators and demonstrated the ability of the robot platform to perform locomotion and teleoperation tasks. By sharing all design files, control algorithms, and manufacturing details, we hope to democratize access to humanoid robot hardware, fostering broader participation in humanoid-robotics research and accelerating innovations in this critical domain. 

## VIII. ACKNOWLEDGMENT 

We would like to thank Lydia Liu, Widyadewi Soedarmadji, and Daniel Wong for the early-stage project explorations. We would also like to thank Alex Hao and Ted Zhang for providing help on supporting the experiments. We are grateful to Chengyi Lux Zhang for the generous assistance. Finally, we appreciate the helpful discussions from all members of Hybrid Robotics Group and SLICE lab. This work is supported in part by NSF 2303735 for POSE, in part by NSF 2238346 for CAREER, in part by the Robotics and AI Institute. K. Sreenath has financial interest in the Robotics and AI Institute. He and the company may benefit from the commercialization of the results of this research. 

## REFERENCES 

- [1] Agility Robotics. Meet digit: The newest robot from agility robotics, 2024. URL https://agilityrobotics.com/ products/digit. Accessed: 2024-11-11. 

- [2] Min Sung Ahn. _Development and Real-Time Optimization-based Control of a Full-sized Humanoid for Dynamic Walking and Running_ . University of California, Los Angeles, 2023. 

- [3] Mohammed Al-Sada, Pin-Chu Yang, Chang Chieh Chiu, Tito Pradhono Tomo, Mhd Yamen Saraiji, Tetsuya Ogata, and Tatsuo Nakajima. From Anime To Reality: Embodying An Anime Character As A Humanoid Robot. In _Extended Abstracts of the 2021 CHI Conference on Human Factors in Computing Systems_ , pages 1–5, 2021. 

- [4] Alejandro F Azocar, Luke M Mooney, Levi J Hargrove, and Elliott J Rouse. Design and characterization of an open-source robotic leg prosthesis. In _2018 7th IEEE International Conference on Biomedical Robotics and Biomechatronics (Biorob)_ , pages 111–118. IEEE, 2018. 

- [5] St´ephane Caron, Yann De Mont-Marin, Rohan Budhiraja, Seung Hyeon Bang, Ivan Domrachev, and Simeon Nedelchev. Pink: Python inverse kinematics based on Pinocchio, 2024. URL https://github.com/ stephane-caron/pink. 

- [6] Justin Carpentier, Florian Valenza, Nicolas Mansard, et al. Pinocchio: fast forward and inverse dynamics for poly-articulated systems. https://stack-oftasks.github.io/pinocchio, 2015–2021. 

- [7] Justin Carpentier, Guilhem Saurel, Gabriele Buondonno, Joseph Mirabel, Florent Lamiraux, Olivier Stasse, and Nicolas Mansard. The Pinocchio C++ library – A fast and flexible implementation of rigid body dynamics algorithms and their analytical derivatives. In _IEEE International Symposium on System Integrations (SII)_ , 2019. 

- [8] Grzegorz Ficht, Philipp Allgeuer, Hafez Farazi, and Sven Behnke. NimbRo-OP2: Grown-up 3D printed open humanoid platform for research. In _2017 IEEE-RAS 17th International Conference on Humanoid Robotics (Humanoids)_ , pages 669–675. IEEE, 2017. 

- [9] Fourier. GR-1, 2024. URL https://www.fftai.com/ products-gr1. Accessed: 2024-11-11. 

- [10] David V Gealy, Stephen McKinley, Brent Yi, Philipp Wu, Phillip R Downey, Greg Balke, Allan Zhao, Menglong Guo, Rachel Thomasson, Anthony Sinclair, et al. Quasidirect drive for low-cost compliant robotic manipulation. In _2019 International Conference on Robotics and Automation (ICRA)_ , pages 437–443. IEEE, 2019. 

- [11] Ruben Grandia, Espen Knoop, Michael A Hopkins, Georg Wiedebach, Jared Bishop, Steven Pickles, David M¨uller, and Moritz B¨acher. Design and control of a bipedal robotic character. _arXiv preprint arXiv:2501.05204_ , 2025. 

- [12] Felix Grimminger, Avadesh Meduri, Majid Khadiv, Julian Viereck, Manuel W¨uthrich, Maximilien Naveau, Vincent Berenz, Steve Heim, Felix Widmaier, Thomas Flayols, et al. An open torque-controlled modular robot architecture for legged locomotion research. _IEEE Robotics and Automation Letters_ , 5(2):3650–3657, 2020. 

- [13] Kenji Kaneko, Hiroshi Kaminaga, Takeshi Sakaguchi, Shuuji Kajita, Mitsuharu Morisawa, Iori Kumagai, and Fumio Kanehiro. Humanoid robot HRP-5P: An electrically actuated humanoid robot with high-power and wide-range joints. _IEEE Robotics and Automation Letters_ , 4(2):1431–1438, 2019. 

- [14] Benjamin G Katz. _A low cost modular actuator for dynamic robots_ . PhD thesis, Massachusetts Institute of Technology, 2018. 

- [15] Nathan Kau, Aaron Schultz, Natalie Ferrante, and Patrick Slade. Stanford doggo: An open-source, quasi-directdrive quadruped. In _2019 International conference on robotics and automation (ICRA)_ , pages 6309–6315. IEEE, 2019. 

- [16] Matthieu Lapeyre, Steve N’Guyen, Alexandre Le Falher, and Pierre-Yves Oudeyer. Rapid morphological 

exploration with the Poppy humanoid platform. In _2014 IEEE-RAS International Conference on Humanoid Robots_ , pages 959–966. IEEE, 2014. 

- [17] Ung Hee Lee, Chen-Wen Pan, and Elliott J Rouse. Empirical characterization of a high-performance exteriorrotor type brushless DC motor and drive. In _2019 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 8018–8025. IEEE, 2019. 

- [18] Junheng Li, Junchao Ma, Omar Kolt, Manas Shah, and Quan Nguyen. Dynamic Loco-manipulation on HECTOR: Humanoid for Enhanced ConTrol and Open-source Research. _arXiv preprint arXiv:2312.11868_ , 2023. 

- [19] Zhongyu Li, Christine Cummings, and Koushil Sreenath. Animated cassie: A dynamic relatable robotic character. In _2020 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 3739–3746. IEEE, 2020. 

- [20] Qiayuan Liao, Bike Zhang, Xuanyu Huang, Xiaoyu Huang, Zhongyu Li, and Koushil Sreenath. Berkeley humanoid: A research platform for learning-based control. _arXiv preprint arXiv:2407.21781_ , 2024. 

- [21] Yeting Liu, Junjie Shen, Jingwen Zhang, Xiaoguang Zhang, Taoyuanmin Zhu, and Dennis Hong. Design and control of a miniature bipedal robot with proprioceptive actuation for dynamic behaviors. In _2022 International Conference on Robotics and Automation (ICRA)_ , pages 8547–8553. IEEE, 2022. 

- [22] Sebastian Lohmeier, Thomas Buschmann, and Heinz Ulbrich. Humanoid robot LOLA. In _2009 IEEE International Conference on robotics and automation_ , pages 775–780. IEEE, 2009. 

- [23] mjbots. Moteus R4.11, 2025. URL https://mjbots.com/ products/moteus-r4-11. Accessed: 2025-01-31. 

- [24] NAO H25. NAO H25, 2024. URL http://doc. aldebaran.com/2-1/family/nao <u>h25/index h25.html.</u> Accessed: 2025-04-10. 

- [25] ODrive Robotics. ODrive Robotics: High Performance Motor Control, 2025. URL https://odriverobotics.com. Accessed: 2025-01-31. 

- [26] OPENLOONG. The universal humanoid robot FXV2750, 2024. URL https://www.openloong.org.cn/en/ developer/robot. Accessed: 2024-11-11. 

- [27] Ill-Woo Park, Jung-Yup Kim, Jungho Lee, and Jun-Ho Oh. Mechanical design of humanoid robot platform KHR-3 (KAIST humanoid robot 3: HUBO). In _5th IEEERAS International Conference on Humanoid Robots, 2005._ , pages 321–326. IEEE, 2005. 

- [28] Alberto Parmiggiani, Marco Maggiali, Lorenzo Natale, Francesco Nori, Alexander Schmitz, Nikos Tsagarakis, Jose Santos Victor, Francesco Becchi, Giulio Sandini, and Giorgio Metta. The design of the iCub humanoid robot. _International journal of humanoid robotics_ , 9(04): 1250027, 2012. 

- [29] ROBOTIS. OP3 E-Manual, 2018. URL https://emanual. robotis.com/docs/en/platform/op3/introduction/. Accessed: 2025-04-10. 

- [30] Wesley Roozing and Glenn Roozing. 3D-printable low-reduction cycloidal gearing for robotics. In _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 1929–1935. IEEE, 2022. 

- [31] Wesley Roozing and Glenn Roozing. Experimental comparison of pinwheel and non-pinwheel designs of 3D-printed cycloidal gearing for robotics. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 7091–7098. IEEE, 2024. 

- [32] Andrew SaLoutos, Elijah Stanger-Jones, Yanran Ding, Matthew Chignoli, and Sangbae Kim. Design and development of the mit humanoid: A dynamic and robust research platform. In _2023 IEEE-RAS 22nd International Conference on Humanoid Robots (Humanoids)_ , pages 1– 8. IEEE, 2023. 

- [33] Haochen Shi, Weizhuo Wang, Shuran Song, and C Karen Liu. Toddlerbot: Open-source ml-compatible humanoid platform for loco-manipulation. _arXiv preprint arXiv:2502.00893_ , 2025. 

- [34] Unitree Robotics. Unitree G1 - Humanoid Robot, 2024. URL https://www.unitree.com/g1. Accessed: 2024-1111. 

- [35] Unitree Robotics. Unitree H1 - Universal Humanoid Robot, 2024. URL https://www.unitree.com/h1. Accessed: 2024-11-11. 

- [36] Karthik Urs, Challen Enninful Adu, Elliott J Rouse, and Talia Y Moore. Design and characterization of 3d printed, open-source actuators for legged locomotion. In _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 1957–1964. IEEE, 2022. 

- [37] Benjamin Vedder and the VESC Project Community. VESC Project - Open Source ESC, 2025. URL https: //vesc-project.com. Accessed: 2025-01-31. 

- [38] Zhicheng Wang, Wandi Wei, Anhuan Xie, Yifeng Zhang, Jun Wu, and Qiuguo Zhu. Hybrid bipedal locomotion based on reinforcement learning and heuristics. _Micromachines_ , 13(10):1688, 2022. 

- [39] Manuel W¨uthrich, Felix Widmaier, Felix Grimminger, Joel Akpo, Shruti Joshi, Vaibhav Agrawal, Bilal Hammoud, Majid Khadiv, Miroslav Bogdanovic, Vincent Berenz, et al. Trifinger: An open-source robot for learning dexterity. _arXiv preprint arXiv:2008.03596_ , 2020. 

- [40] Boxi Xia, Bokuan Li, Jacob Lee, Michael Scutari, and Boyuan Chen. The duke humanoid: Design and control for energy efficient bipedal locomotion using passive dynamics. _arXiv preprint arXiv:2409.19795_ , 2024. 

- [41] Taoyuanmin Zhu. _Design of a highly dynamic humanoid robot_ . University of California, Los Angeles, 2023. 

- [42] Maja Zorjan, Vincent Hugel, and Pierre Blazevic. Influence of hip joint axes change of orientation on power distribution in humanoid motion. In _The 5th International Conference on Automation, Robotics and Applications_ , pages 271–276. IEEE, 2011. 

- [43] Maja Zorjan, Vincent Hugel, Pierre Blazevic, and 

_Robotics_ , 29(11):707–719, 2015. 

Branislav Borovac. Influence of rotation of humanoid hip joint axes on joint power during locomotion. _Advanced_ 

