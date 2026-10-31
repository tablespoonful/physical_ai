---
title: "Design of an Energy-Aware Cartesian Impedance Controller for Collaborative Disassembly"
date: "2023-02-07"
authors: "Sebastian Hjorth; Edoardo Lamon; Dimitrios Chrysostomou; Arash Ajoudani"
url: https://arxiv.org/abs/2302.03587
pdf: https://arxiv.org/pdf/2302.03587
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2302.03587)** / [論文ページ](https://arxiv.org/abs/2302.03587)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Design of an Energy-Aware Cartesian Impedance Controller for Collaborative Disassembly** 

Sebastian Hjorth<sup>1</sup> , Edoardo Lamon<sup>2</sup> , Dimitrios Chrysostomou<sup>1</sup> , and Arash Ajoudani<sup>2</sup> 

**_Abstract_ — Human-robot collaborative disassembly is an emerging trend in the sustainable recycling process of electronic and mechanical products. It requires the use of advanced technologies to assist workers in repetitive physical tasks and deal with creaky and potentially damaged components. Nevertheless, when disassembling worn-out or damaged components, unexpected robot behaviors may emerge, so harmless and symbiotic physical interaction with humans and the environment becomes paramount. This work addresses this challenge at the control level by ensuring safe and passive behaviors in unplanned interactions and contact losses. The proposed algorithm capitalizes on an energy-aware Cartesian impedance controller, which features energy scaling and damping injection, and an augmented energy tank, which limits the power flow from the controller to the robot. The controller is evaluated in a real-world flawed unscrewing task with a Franka Emika Panda and is compared to a standard impedance controller and a hybrid force-impedance controller. The results demonstrate the high potential of the algorithm in human-robot collaborative disassembly tasks.** 

## I. INTRODUCTION 

In the last decade, the European Union has started to promote the implementation of circular economy business models (CEBMs) across different manufacturing areas [1], [2]. CEBMs envision the adoption of take-back programs, efficient disassembly, and requalification processes [3]. To make such business models financially, environmentally, and socially viable, companies must recover as many undamaged components as possible. However, various challenges, for example, high variability in the condition of post-use parts, poor information about returned products, high product complexity, increasing quality requirements on recovered materials and components, and pressure on costs and efficiency, strongly limit the wide exploitation of effective disassembly processes [4]. 

To face the variability and uncertainties of the products’ state [5], human-in-the-loop solutions such as human-robot collaborative disassembly (HRCD) cells, in which humans and robots support each other to complete a given nondestructive disassembly task, started to be conceived [6] (an example for an HRCD cell can be seen in Figure 1.). 

> 1Dept. of Materials and Production, Aalborg University, Aalborg, Denmark. sshj@mp.aau.dk 

> 2Human-Robot Interfaces and Interaction, Istituto Italiano di Tecnologia, Genoa, Italy. edoardo.lamon@iit.it 

This research was partly supported by EU’s SMART EUREKA programme S0218-chARmER, Innovation Fund Denmark (Grant no. 911800001B), by the EU’s H2020-WIDESPREAD project no. 857061 ”Networking for Research and Development of Human Interactive and Sensitive Robotics Taking Advantage of Additive Manufacturing – R2P2”, and by EU’s Horizon 2020 research and innovation programme under Grant Agreement No. 871237 (SOPHIA). 


Fig. 1. Experimental setup: a manipulator, equipped with a cordless drill unfastens screws on the screw plate placed on the same workbench. The robot controller can drive the drill through a microcontroller. 

Nonetheless, when it comes to physical human-robot interaction (pHRI), implementing such HRCD solutions demands high safety standards. Due to their design, collaborativeenabled robots can attain control strategies that regulate the level of compliance [7], enabling them to interact safely with unstructured environments [8]. These features are of great importance in HRCD, which presents a high risk of unpredictable events occurring due to the variability and uncertainties of the product’s state. In particular, when separating two sub-assemblies, the breakage of the fasting component could lead to a contact loss between the robot’s end-effector and the component, which, in turn, might result in damaged components, tools and, in the worst case, human harm. 

A common fastening method that does not require destructive disassembly is screwing. However, since the product has reached its end of life, the screw condition can significantly affect the disassembly process [9]. Several control strategies for HRCD have been proposed in the literature, but only a few could deal with the realistic flawed conditions mentioned above. The work done by [10] focuses on the unscrewing of components on lithium-ion car batteries and the mechanism for changing the tool bit autonomously. It concluded that complained control schemes (i.e. impedance controller) are necessary to enable safe and direct pHRI. The work presented in [11], [12] focuses on the unfastening of screws with an external hexagonal-shaped head utilizing a KUKA LBR iiwa. Unscrewing is achieved with the help of a standard Cartesian impedance control scheme in combination with a custom nut-runner, which encloses the hexagonal-shaped screw head. Another unscrewing strategy for screws with a hexagonal shaped screw head was proposed in [13], where 

screw location and orientation are detected and the unscrewing makes use of a standard Cartesian impedance controller and a conventional 2-fingers gripper. In [14], an unscrewing robotic system for the automatic disassembly of electronic devices was developed. The work investigated force and torque profiles used by humans when unscrewing Phillips and internal hex screws, to design a control strategy and tool that minimizes slippage. The proposed strategy was deployed on a position-controlled UR3 equipped with a force/torque sensor in combination with a purpose-built screwdriver with passive compliance along the tool _z_ -axis. The drawback of using a position-controlled robot is that in case of collision, the robot’s only safety mechanism is the emergency stop, which can result in a dangerous quasi-static contact scenario (e.g., clamping). Nevertheless, none of the above presented approaches considers the robot’s behavior when an unpredicted faulty situation occurs during the unscrewing due to either a broken screw or failed engagement during the unscrewing process. In this context, observing, monitoring, and limiting the amount of energy and power flow that the controller is allowed to inject into the manipulator is crucial to a successful interaction. Additionally, the energy exchange between the manipulator and its environment would result in a safer task execution [15], not only by ensuring a passive behavior, but also by reducing the controller’s action in potential faults. Different control schemes that could allow the limitation of the energy and power flow are presented in [15]–[17]. Therefore, the presented formalism will focus on an energy-aware control strategy with the aim to tackle the aforementioned challenges. The formalism is an extension of an energy-aware Cartesian impedance controller presented in [17], [18] in combination with a task-based energy tank and a power flow regulation mechanism proposed by [19]. Moreover, the controller’s performance is evaluated and compared with the controller proposed in the literature through a set of experiments. These experiments assess the controller’s ability to handle external disturbances and minimize the impact force and energy exchange with the environment. To summarize, the novel contributions of the manuscript are the following: 

- The design of an energy-aware Cartesian impedance controller that uses a global energy tank with power limitation. 

- An experimental comparison of the proposed energyaware Cartesian impedance controller with a hybrid force-impedance controller [19], and a standard Cartesian impedance controller [20], in a faulty unscrewing task with a stripped screw head. 

## II. PROBLEM STATEMENT 

In this paper, we examine an HRCD task with a redundant manipulator, focusing on the behavior in case of contact loss during the unscrewing. Such a scenario can occur due to a stripped screw head, corrosion, or screw damaged inside that is not detectable by external inspection (e.g., damaged threads or broken shaft) or due to a pHRI. The generalized approach for the unscrewing operation is to generate enough 


Fig. 2. Illustration of two different unscrewing scenarios. Left-hand side: a successful unscrewing operation. Right-hand side: a possible scenario for contact loss due to the screw shaft breakage during the unscrewing operation. 

momentum **m** z on the screw so that the screw rotates around its longitudinal axis, thus generating a vertical upward force **w** ext<sup>0</sup><sup>_,_EE.Inordertoensuretheengagementofthescrewdriver</sup> bit during the unscrewing process, it is crucial to apply a force **w** _K_<sup>0</sup><sup>_,_EE</sup> onto the screw throughout the entire unscrewing process. Common approaches to generate such force are standard Cartesian impedance and hybrid Cartesian forceimpedance controllers. In case of a contact loss during the unscrewing process due to one of the scenarios mentioned above, the force applied at the screwdriver might cause the bit to hit the screwed product, damage the two components of the screwed product or harm the operator. A graphical visualization of a successful and a failed unscrewing operation is depicted in Figure 2. 

## III. METHODOLOGY 

## _A. Energy Aware-Impedance Controller_ 

This control scheme presents a method that autonomously counteracts the possible non-linear behavior of the impedance model in contact scenarios [20], with the help of the energy shaping and damping injection techniques, firstly introduced in [21]. These concepts are utilized to monitor and limit the total energy of the system, as well as the power of the robot. In [17], [18], the same control strategy was successfully implemented on a kinematically redundant manipulator, whose control torques **_τ_**<sup>_⊤_</sup> Control<sup>_∈_R</sup><sup>_n_are defined</sup> in a quasi-static condition as 


where **_τ_**<sup>_⊤_</sup> Spring<sup>_∈_R</sup><sup>_n_and</sup><sup>**_τ_**</sup><sup>_⊤_</sup> Damp<sup>_∈_R</sup><sup>_n_arerespectively</sup> generated by Cartesian springs and dampers. For a more detailed explanation of the notation hereafter, please refer to [18]. The torques **_τ_**<sup>_⊤_</sup> Spring<sup>aregeneratedbytheelastic</sup> wrench **w** _K_<sup>EE</sup><sup>_,_EE</sup> _⊤ ∈ se∗_ (3), which can be expressed as 


where ∆ **_η_** _∈ se_ (3) describes the infinitesimal body twist displacement [16], the diagonal matrices **K** _r ∈_ R<sup>3</sup><sup>_×_3</sup> , **K** _t ∈_ R<sup>3</sup><sup>_×_3</sup> hold the stiffness values for the rotational, translation springs, and **K** _c ∈_ R<sup>3</sup><sup>_×_3</sup> describes the decoupling between these two terms. Force **f** _K_<sup>EE</sup><sup>_,_EE</sup> _∈_ R<sup>1</sup><sup>_×_3</sup> and momentum **m**<sup>EE</sup> _K_<sup>_,_EE</sup> _∈_ R<sup>1</sup><sup>_×_3</sup> can be formulated in terms of energy by 

basing their formulation on the end-effector’s current transformation **H**<sup>0</sup> EE<sup>_∈SE_(3)anditsdesiredgoaltransformation</sup> **H**<sup>0</sup> _d_<sup>_∈SE_(3)inthefollowingway:</sup> 


with **p**<sup>_d_</sup> EE<sup>_∈_R3,</sup><sup>**R**EE</sup> _d_<sup>_∈SO_(3)describethetranslationand</sup> rotation between the end-effector’s current and its desired configuration. **G** _r,t,c ∈_ R<sup>3</sup><sup>_×_3</sup> are co-stiffnesses of the rotational spring, translational spring and coupling term [17], [18], [22] and _as_ () represents the asymmetric part of the matrix. Safety is dealt with two different controller features: (i) monitoring the total amount of energy stored in the system with the help of energy scaling and (ii) limiting the power of the system with the damping injection method, if necessary. The energy scaling method enforces a limit on the total energy of the system based on an energy-based safety metric _E_ total. The total energy stored in the system can be expressed as _E_ total = _T_ total + _U_ total where _T_ total _∈_ R is the kinetic co-energy and _U_ total _∈_ R the potential energy due to spatial springs [22]. In the event of a pHRI that results in a displacement of the end-effector, such that the statement _E_ total _> E_ total becomes true, one computes the following scaling parameter: 


As seen in [17] _U_ total is proportional to the co-stiffness **G** _r,t,c_ . Therefore, by scaling **G** _r,t,c_ with _λ ∈_ R in the following way **G** _r,t,c_ **_←_** _λ_ **G** _r,t,c_ , the wrench generated by the springs **w** _K_<sup>0</sup><sup>_,_EE</sup> _⊤_ is directly affected. This results in the motion generating torques from the Cartesian springs **_τ_**<sup>_⊤_</sup> Spring<sup>=</sup><sup>**J**(</sup><sup>**q**)</sup><sup>**w**</sup> K<sup>0</sup><sup>_,_EE</sup> _⊤_ , where **w** _K_ 0 _,_ EE _⊤_ = _Ad ⊤_ **H**<sup>EE</sup> 0<sup>**w**</sup> _K_<sup>EE</sup><sup>_,_EE</sup> _⊤_ with _Ad_<sup>_⊤_</sup> **H**<sup>EE</sup> 0<sup>_∈_R6</sup><sup>_×_6beingtheadjointcoordinatetransfor-</sup> mation. However, as the energy of the robot is manipulated directly, it is vital to ensure the passivity of the system. The enforcement of the passivity will be discussed in Section IIIB. After limiting the total energy of the robot, the robot’s power must also be overseen, as the power describes the instantaneous energy transferred when the robot makes contact with its environment. For this purpose, the damping injection method monitors the power resulting from the manipulator’s motion _P_ motion _∈_ R: 


with **B** init _∈_ R<sup>_n×n_</sup> being the initial positive definite damping matrix. As soon as the robot starts moving towards a desired transformation **H**<sup>0</sup> _d_<sup>,</sup><sup>_P_motionismonitored.Intheeventof</sup> _P_ motion exceeding the chosen power limit _P_ motion _∈_ R, the scaling parameter _β ∈_ R is calculated: 


multiplying _β_ with the initial damping matrix **B** init, resulting in the damping term: 


Hence, in the scenario in which _P_ motion exceeds _P_ motion, the increase of _β_ has a direct effect on the damping term. 

## _B. Energy Tank Integration_ 

The previously described methods ensure the robot’s safety by manipulating the robot’s energy; however, manipulating the system’s energy can result in a passivity-violating behavior. Therefore, it is necessary to limit the amount of energy that the controller is allowed to inject into the system. Furthermore, to this aim, latest research, such as [19], [23]–[26] also highlights that one has to limit the rate of energy injected by the controller. The augmented energy tank described in [19] prevents the energy of the system from suddenly increasing within a single time step, thereby ensuring that the system stays stable. As mentioned in [27], the stored energy in an impedance-controlled robot can be expressed as a storage function _S_ = _S_ c + _S_ r _∈_ R, which is composed of the storage functions of the controller and the robot. _S_ r is passive as the robot’s energy is physically bounded from below [28]. This results in _S_ being passive if _S_ c is passive with respect to the possible violating ports. The power flow of the possible violating ports with respect to the energy storage function _S_ c can be expressed as: 


where _P_ dissipation _∈_ R is the power flow due to the dissipation, and _P_ task = _−_ **w** _K_<sup>0</sup><sup>_,_EE</sup> **x** ˙ _∈_ R describes the power demand of the task and **x** ˙ _∈_ R<sup>6</sup> denotes the spatial end-effector velocity. The passivity of the overall system can be achieved by augmenting the storage function _S_ c with an energy tank _E_ tank bounded by upper and lower bounds _E_ tank/ _<u>E</u>_ ~~t~~ ank<sup>.The</sup> power flow of the new storage function can be expressed as 


However, as pointed out in [19], a rapid increase of the system energy even with a bounding _E_ tank unstable behavior can occur. Therefore, the authors proposed to limit the positive power flow in the system through the following formalism: 


where _k_ and _j_ ensure that the upper and lower bounds of _E_ tank are not violated. They are defined in such a way that the control system neither injects or takes out energy from the tank if the respective bound is reached. 


Additionally, the rate at which the controller can inject energy into the system is limited by: 


Where _γ_ is defined as a ratio between the maximal allowed power flow _<u>P</u>_ ~~t~~ ank<sup>andtheoriginallycalculatedpowerflow</sup> _P_ task from the controller to the system. Integrating the abovedescribed energy tank dynamic for the previously presented energy-aware Cartesian impedance controller, the energy scaling variable can be reformulated as 


In case the energy tank is empty ( _k_ = 0), _λ_ is hindered from increasing again after an interaction occurs, thereby keeping the **G** _r,t,c_ constant, which results in a standard Cartesian impedance controller with constant gains. This will reduce the controller’s performance; however, it does not hinder _λ_ from being further scaled down in order to ensure the safety metric _E_ total is not violated. Additionally, to ensure that _λ_ does not increase when the energy tank is drained, it is important to ensure that _λ_ does not rise too fast and result in an unstable behavior of the manipulator. Therefore, as previously mentioned, it is necessary to limit the energy that can be drained from the tank ( _P_ task). Hence, applying the constraint _γ_ , the power flow from the tank to the system results in the following **_τ_**<sup>_⊤_</sup> Spring<sup>:</sup> 


After limiting the amount of energy that can be injected into the system through the energy scaling variable _λ_ , the damping injection terms must be modified as follows: 


As _γ_ restricts the power flow to the system, it also has a direct effect on _P_ motion resulting in the following control law: 


The energy-aware Cartesian impedance controller was tested in a proof-of-concept unscrewing experiment with a stripped screw by comparing its performance with state-of-art approaches, i.e., a standard Cartesian impedance controller [20] and a Cartesian hybrid force-impedance controller with power limitation [19]. The setup consists of a Franka Emika Panada manipulator equipped with a cordless drill, a screw 

TABLE I 

CONTROL PARAMETERS USED DURING THE DIFFERENT EXPERIMENTS. 

|**Cartesian Impedance controller**||
|---|---|
|Translational spring stiffness<br>**K**_t_|900_·_**I**3|
|Rotational spring stiffness<br>**K**_r_|40_·_**I**3|
|Coupling spring stiffness<br>**K**_c_|0_·_**I**3|
|**Hybrid Force-Impedance controller**||
|Translational spring stiffness<br>**K**_t_|100_·_**I**3|
|Rotational spring stiffness<br>**K**_r_|10_·_**I**3|
|Coupling spring stiffness<br>**K**_c_|0_·_**I**3|
|Desired force<br>**w**desired_,z_|_−_**f**engage,z|
|**Energy-Aware Impedance controller**||
|Translational spring stiffness<br>**K**_t_|900_·_**I**3|
|Rotational spring stiffness<br>**K**_r_|40_·_**I**3|
|Coupling spring stiffness<br>**K**_c_|0_·_**I**3|
|Max. allowed energy<br>_E_total|0_._7J|
|Max. allowed power<br>_P_motion|0_._5W|
|Initial damping<br>**B**|5_·_**I**7|
|**Energy Tank & Others**||
|Engagement force<br>**f**engage,z|15N|
|Max. allowed power to be extracted<br>_P_<br>~~t~~ank|_−_0_._175W|
|Max. Energy level in the tank<br>_E_tank|5J|
|Min. Energy level in the tank<br>_E_<br>~~t~~ank|0_._5J|
|Initial Energy level in the tank<br>_E_tank|3J|


head fixture (screw plate), and an M5 _×_ 25 Phillips head screw, as seen in Figure 1. The cordless drill is equipped with a microcontroller that communicates with the robot controller via ROS interface. The experiment can be divided into two different phases: 1) unscrewing, and 2) interaction with a human. For our use-case, it is assumed that the position of the screw is known a priori, similarly to the work of [11] who discusses an exploration method for successful tool insertion. The unscrewing phase starts with the tool-centerpoint (TCP) being already inserted in the screw head and begins to increase the force along the TCPs _z_ -axis until it reaches the engagement force **f** engage,z. For the standard and the presented energy-aware Cartesian impedance controller, **f** engage,z is achieved by moving the desired transformation **H** _d_<sup>0</sup> along the _z_ -axis in the negative direction, thereby preventing the screw bit from slipping. As soon as **f** engage,z is reached, the drill starts, and simultaneously, the desired TCP pose is translated along the _z_ -axis mentioned above in a positive direction to maintain **w** _ext,z_<sup>0</sup><sup>_,EE_approximatelyconstant.With</sup> the hybrid force-impedance controller, such mechanism is ensured by the force loop of the _z_ -axis. To systematically generate contact loss, we use a simulated broken shaft, i.e., a screw 10 mm shorter than expected by the robot motion planner. In this way, the controller still exerts some force while the shaft comes out from the plate. For this reason, due to **w** _K_<sup>0</sup><sup>_,_EE</sup> , the screw slips, hence losing the contact between the screw and the drill bit and the robot end-effector moves in _z_ direction towards its current **H**<sup>0</sup> _d_<sup>andeventuallyhitsthe</sup> table. To further evaluate the suitability of the controller in human-populated environments, after the unscrewing phase, the robot’s end-effector was disturbed by a human in the interaction phase. Snapshots of the experiment are available 


Fig. 3. Visualizes the observable quantities of the Cartesian impedance controller. The difference between current **p**<sup>0</sup> EE<sup>anddesiredposition</sup><sup>**p**0</sup> d<sup>as</sup> well as the workbench position **p**<sup>0</sup> wb<sup>andthelinearz-componentofthe</sup> external force applied on the TCP **w** _ext,z_<sup>0</sup><sup>_,EE_.</sup> 

in Figure 5. The control parameters chosen for each control scheme are shown in Table I. The force value 15 N was chosen based on an initial investigation which has shown that a screw tightened with 3 Nm needs approximately 1520 N of force applied to avoid slippage. The maximum energy threshold _E_ total was selected according to ISO/TS 15066:2016 [29] that specified a range of 0 _._ 52 - 2 _._ 5 J, the value for _P_ motion and the threshold for the power limit on the energy tank _<u>P</u>_ ~~t~~ ank<sup>were picked according to earlier results</sup> in [17], [18] and in [24], respectively. 

## _A. Standard Cartesian Impedance Controller_ 

As mentioned above, to generate the force required to perform the unscrewing process, **p**<sup>0</sup> _d,z_<sup>was moved incrementally</sup> below the screw head until **w** _K,z_<sup>0</sup><sup>_,_EEreachesthedesiredforce</sup> (Table I). This change along the z-axis results in an increase in the external force applied, as seen in the time period 7 _−_ 12 _._ 5 s in Figure 3. The time period between 12 _._ 5 _−_ 28 s marks the unscrewing phase, where the incremental change along the z-axis is changed in a direction such that **w** _ext,z_<sup>0</sup><sup>_,EE_</sup> is kept within the acceptable working range. Focusing on the external force, one can see how force decreases due to the missing counter force by the screw, which drives the robot to hit the workbench with an impact force of 15 N before the equilibrium pose of the controller reaches the surface (highlighted with a green area). In the interaction phase, which starts immediately afterwards, the robot’s end effector is displaced by pHRI at 32 s where the spatial spring generated a force of 37 N to counteract the disturbance. Once the end effector has reached its maximal displacement of 0 _._ 34 m, it is released, and the robot moves back towards its desired configuration and hits the workbench a second time with 18 N. 

## _B. Hybrid Force-Impedance Controller_ 

In the case of the hybrid controller, the force that is necessary to enable the the screw to be unscrewed is generated by the force control part. Therefore, it is not necessary to manipulate the desired pose **H**<sup>0</sup> _d_<sup>,asseeninFigure4.</sup> After 5 s, the desired force of 20 N is reached and the unscrewing phase 


Fig. 4. Visualizes the observable quantities of the hybrid force impedance controller. The difference between current **p**<sup>0</sup> EE<sup>anddesiredposition</sup><sup>**p**0</sup> d<sup>as</sup> well as the workbench position **p**<sup>0</sup> wb<sup>,thelinearz-componentoftheexternal</sup> force applied on the TCP **w** _ext,z_<sup>0</sup><sup>_,EE_andtheenergytank</sup><sup>_E_tankanditspower</sup> flow _P_ task. 

begins, which lasts until 21 s. After the contact loss, the robot gets accelerated by the force controller in order to maintain the desired force. Even though the restrictions on the implemented energy tank already reduce the rate by which the controller can inject energy into the system (see Figure 4), the resulting force is still significant (approx. 26 N). In the interaction phase, which begins immediately afterwards, the robot end-effector is displaced by pHRI at 24 _._ 5 s. During the displacement of the robot, one can see how the force response tries to adapt to the applied force. When the end effector is released, the tank’s power limit takes effect, thereby reducing the force response; however, even though the robot makes contact with the work surface with a significant impact force (approx. 34 N). 

## _C. Energy-Aware Controller_ 

The unscrewing task here follows the same procedure as the standard Cartesian impedance controller, where the equilibrium’s pose has to be incrementally moved along the screw’s longitudinal axis. The desired force is reached after 10 s (Figure 6), and the equilibrium pose is again translated in an upward direction during the unscrewing phase. At 


Fig. 5. Snapshots of the experiment with the energy-aware impedance controller. A video of the experiments is available in the multimedia extension and at https://www.youtube-nocookie.com/embed/SgYFHMlEl0k. From left to right: (i) unscrewing, (ii) contact loss, (iii) impact with table, (iv) pHRI, (v) end of the pHRI, (vi) second impact with table. 

the point of contact loss (26 s), the end effector starts to move towards its equilibrium pose thereby making contact with the workbench at 29 s without a significant impact force (approx. 1 _._ 2 N). A similar behavior can be observed during the interaction phase, where the end effector hits the workbench after the end of the disturbance without resulting in a significant impact force (approx. 2 _._ 6 N). This can be attributed to the effect of the spring energy scaling and the power flow regulation based on the power limit in the energy tank. When _λ_ decreases, the stiffness of the spring also decreases and thereby reduces the energy in the system; however, when _λ_ increases again, energy is injected back into the system; if this injection is not kept in check, it can result in unstable and non-passive behavior. Therefore, the rate at which energy can be injected must be monitored and limited. When comparing the response of _λ_ and _γ_ , one can see that at every instant when _λ_ increases, _γ_ decreases. As in (15), _γ_ directly affects the rate at which energy can be injected into the system, that is, it regulates how fast _λ_ can increase at each time step. Additionally, the energy tank also ensures that _λ_ can only be increased if there is energy in the tank ( _E_ tank _>_ _<u>E</u>_ ~~t~~ ank<sup>).Iftheenergytankisdepleted,</sup><sup>_λ_remains</sup> constant. 

## V. DISCUSSION & CONCLUSIONS 

This work presents an energy-based control formalism in combination with an augmented energy tank to ensure the passivity of the system. To the best of the authors knowledge, such a formalism has not been applied to a disassembly task before. The capabilities of the formalism to handle contact loss and pHRI are evaluated on an unscrewing task. Additionally, its performance was compared to a standard Cartesian impedance controller as well as a hybrid forceimpedance controller. When it comes to applying and tracking a constant force onto the screw, the force-impedance control outperforms the standard Cartesian impedance controller and the energy-aware controller; however, in case of a contact loss, it generates the highest impact force among the compared controllers. On the other hand, the Cartesian impedance controller is intrinsically passive, but, due to the task requirements in terms of force and, thus, stiff behavior, a significant impact force is generated, which is not in compliance with pHRI. The presented formalism introduces an energy-aware scaling mechanism to the Cartesian impedance controller, as well as a power flow regulated energy tank, which ensures the passivity of the system. Therefore, to allow the manipulator to react in a compliant manner in the scenario of contact loss or pHRI, the manipulator stays within its predefined energy thresholds. Notably, during 


Fig. 6. Visualizes the observable quantities of the energy-aware impedance controller. The difference between current **p**<sup>0</sup> EE<sup>anddesiredposition</sup><sup>**p**0</sup> d<sup>,as</sup> well as the workbench position **p**<sup>0</sup> wb<sup>,thelinearz-componentoftheexternal</sup> force applied on the TCP **w** _ext,z_<sup>0</sup><sup>_,EE_, the energy tank</sup><sup>_E_tankand its power flow</sup> _P_ task as well as the energy scaling of the total energy _E_ total. 

the pHRI, a larger displacement could be achieved whilst reducing the impact force between the tool and the robot (up to 92%), given the same initial end-effector impedance values as the classic Cartesian impedance controller. Moreover, when facing comparable disturbances, such as in the contact loss scenario, the impact force is reduced by up to 91% and 95% for the Cartesian Impedance and the hybrid force impedance controller respectively. One drawback of the presented control formalism is the parameterization of the power flow limit, i.e. the size of the energy tank must be designed manually. In the direction, in [23] the power flow formulation depends on the remaining energy in the tank. 

## REFERENCES 

- [1] E. Commission, “Circular Economy Action Plan,” European Commission, Tech. Rep., 2015. 

- [2] European Environment Agency, “Recycling industry can boost the European economy,” p. 2020, 2020. [Online]. Available: https: //www.eea.europa.eu/highlights/recycling-industry-can-boost-the 

- [3] T. E. Graedel, J. Allwood, J.-P. Birat, B. K. Reck, S. F. Sibley, G. Sonnemann, M. Buchert, and C. Hagel¨uken, _UNEP (2011) Recycling Rates of Metals – A Status Report, A Report of the Working Group on the Global Metal Flows to the International Resource Panel._ International Resource Panel, 2011. 

- [4] T. Tolio, A. Bernard, M. Colledani, S. Kara, G. Seliger, J. Duflou, O. Battaia, and S. Takata, “Design, management and control of demanufacturing and remanufacturing systems,” _CIRP Ann. - Manuf. Technol._ , vol. 66, no. 2, pp. 585–609, 2017. 

- [5] K. Elo and E. Sundin, “Automatic dismantling challenges in the structural design of LCD TVs,” _Procedia CIRP_ , vol. 15, pp. 251–256, 2014. 

- [6] S. Hjorth and D. Chrysostomou, “Human–robot collaboration in industrial environments: A literature review on non-destructive disassembly,” _Robotics and Computer-Integrated Manufacturing_ , vol. 73, p. 102208, 2022. 

- [7] J. Zhao, A. Giammarino, E. Lamon, J. M. Gandarias, E. D. Momi, and A. Ajoudani, “A hybrid learning and optimization framework to achieve physically interactive tasks with mobile manipulators,” _IEEE Robotics and Automation Letters_ , vol. 7, no. 3, pp. 8036–8043, 2022. 

- [8] A. Pereira, M. Baumann, J. Gerstner, and M. Althoff, “Improving efficiency of human-robot coexistence while guaranteeing safety: Theory and user study,” _IEEE Transactions on Automation Science and Engineering_ , pp. 1–14, 2022. 

- [9] S. Vongbunyong and W. H. Chen, _Disassembly Automation: Automated Systems with Cognitive Abilities_ , ser. Sustainable production, life cycle engineering and management. Cham: Springer International Publishing AG, 2015. 

- [10] W. H. Chen, K. Wegener, and F. Dietrich, “A robot assistant for unscrewing in hybrid human-robot disassembly,” _2014 IEEE Int. Conf. Robot. Biomimetics, IEEE ROBIO 2014_ , pp. 536–541, 2014. 

- [11] R. Li, C. Ji, Q. Liu, Z. Zhou, D. T. Pham, J. Huang, Y. Tan, M. Qu, Y. Wang, M. Kerin, K. Jiang, and S. Su, “Unfastening of Hexagonal Headed Screws by a Collaborative Robot,” _IEEE Trans. Autom. Sci. Eng._ , pp. 1–14, 2020. 

- [12] J. Huang, D. T. Pham, R. Li, M. Qu, Y. Wang, M. Kerin, S. Su, C. Ji, O. Mahomed, R. Khalil, D. Stockton, W. Xu, Q. Liu, and Z. Zhou, “An experimental human-robot collaborative disassembly cell,” _Computers & Industrial Engineering_ , vol. 155, p. 107189, 2021. 

- [13] A. Rastegarpanah, R. Ner, R. Stolkin, and N. Marturi, “Nut unfastening by robotic surface exploration,” _Robotics_ , vol. 10, no. 3, 2021. 

- [14] D. Mironov, M. Altamirano, H. Zabihifar, A. Liviniuk, V. Liviniuk, and D. Tsetserukou, “Haptics of screwing and unscrewing for its application in smart factories for disassembly,” in _International Conference_ 

_on Human Haptic Sensing and Touch Enabled Computer Applications_ . Springer, 2018, pp. 428–439. 

- [15] J. Lachner, F. Allmendinger, E. Hobert, N. Hogan, and S. Stramigioli, “Energy budgets for coordinate invariant robot control in physical human–robot interaction,” _The International Journal of Robotics Research_ , vol. 40, no. 8-9, pp. 968–985, 2021. 

- [16] S. Stramigioli, _Modeling and IPC Control of Interactive Mechanical Systems - A Coordinate-Free Approach_ . Springer, 2001. 

- [17] G. Raiola, C. A. Cardenas, T. S. Tadele, T. de Vries, and S. Stramigioli, “Development of a safety- and energy-aware impedance controller for collaborative robots,” _IEEE Robotics and Automation Letters_ , vol. 3, no. 2, pp. 1237–1244, 2018. 

- [18] S. Hjorth, J. Lachner, S. Stramigioli, O. Madsen, and D. Chrysostomou, “An energy-based approach for the integration of collaborative redundant robots in restricted work environments,” in _2020 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2020, pp. 7152–7158. 

- [19] E. Shahriari, L. Johannsmeier, E. Jensen, and S. Haddadin, “Power flow regulation, adaptation, and learning for intrinsically robust virtual energy tanks,” _IEEE Robotics and Automation Letters_ , vol. 5, no. 1, pp. 211–218, 2019. 

- [20] C. Ott, _Cartesian Impedance Control of Redundant and Flexible-Joint Robots_ . Springer, Berlin, Heidelberg, 2008. 

- [21] S. Stramigioli, “From differential manifolds to interactive robot control,” Ph.D. dissertation, University of Twente, 12 1998. 

- [22] T. Tadele, “Human-friendly robotic manipulators: safety and performance issues in controller design,” Ph.D. dissertation, University of Twente, 11 2014. 

- [23] Y. Michel, C. Ott, and D. Lee, “Safety-aware hierarchical passivitybased variable compliance control for redundant manipulators,” _IEEE Transactions on Robotics_ , 2022. 

- [24] N. Ramuzat, S. Boria, and O. Stasse, “Passive inverse dynamics control using a global energy tank for torque-controlled humanoid robots in multi-contact,” _IEEE Robotics and Automation Letters_ , vol. 7, no. 2, pp. 2787–2794, 2022. 

- [25] B. Gerlagh, F. Califano, S. Stramigioli, and W. Roozing, “Energyaware adaptive impedance control using offline task-based optimization,” in _2021 20th International Conference on Advanced Robotics (ICAR)_ . IEEE, 2021, pp. 187–194. 

- [26] F. Califano, D. van Dijk, and W. Roozing, “A task-based post-impact safety protocol based on energy tanks,” _IEEE Robotics and Automation Letters_ , vol. 7, no. 4, pp. 8791–8798, 2022. 

- [27] J. Lachner, F. Allmendinger, S. Stramigioli, and N. Hogan, “Shaping impedances to comply with constrained task dynamics,” _IEEE Transactions on Robotics_ , 2022. 

- [28] S. Stramigioli, “Energy-aware robotics,” in _Mathematical Control Theory I_ , M. K. Camlibel, A. A. Julius, R. Pasumarthy, and J. M. Scherpen, Eds. Cham: Springer International Publishing, 2015, pp. 37–50. 

- [29] “ISO/TS 15066:2016 robots and robotic devices — collaborative robots,” 2016. [Online]. Available: https://www.iso.org/standard/ 62996.html 

