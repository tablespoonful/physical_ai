---
title: "Characteristics, Management, and Utilization of Muscles in Musculoskeletal Humanoids: Empirical Study on Kengoro and Musashi"
date: "2026-02-09"
authors: "Kento Kawaharazuka; Kei Okada; Masayuki Inaba"
url: https://arxiv.org/abs/2602.08518
pdf: https://arxiv.org/pdf/2602.08518
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.08518)** / [論文ページ](https://arxiv.org/abs/2602.08518)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# Characteristics, Management, and Utilization of Muscles in Musculoskeletal Humanoids: Empirical Study on Kengoro and Musashi 

Kento Kawaharazuka<sup>_∗_1</sup> , Kei Okada<sup>1</sup> , and Masayuki Inaba<sup>1</sup> 

**_Abstract_ —Various musculoskeletal humanoids have been developed so far, and numerous studies on control mechanisms have been conducted to leverage the advantages of their biomimetic bodies. However, there has not been sufficient and unified discussion on the diverse properties inherent in these musculoskeletal structures, nor on how to manage and utilize them. Therefore, this study categorizes and analyzes the characteristics of muscles, as well as their management and utilization methods, based on the various research conducted on the musculoskeletal humanoids we have developed, Kengoro and Musashi. We classify the features of the musculoskeletal structure into five properties: Redundancy, Independency, Anisotropy, Variable Moment Arm, and Nonlinear Elasticity. We then organize the diverse advantages and disadvantages of musculoskeletal humanoids that arise from the combination of these properties. In particular, we discuss body schema learning and reflex control, along with muscle grouping and body schema adaptation. Also, we describe the implementation of movements through an integrated system and discuss future challenges and prospects.** 

**_Index Terms_ —Biomimetics, Musculoskeletal Humanoids, Tendon/Wire Mechanism, System Integration** 

## I. INTRODUCTION 

Various musculoskeletal humanoids have been developed so far [1]–[5]. These have been researched for diverse purposes, such as achieving a constructive understanding of the human body, validating the advantages of biomimetic structures, and transferring the benefits of imitating human anatomy to robotic technologies. 

The musculoskeletal structure includes bones, joints, ligaments, muscles, and skin, among which muscles play a particularly important role. Muscles possess diverse characteristics not found in general axis-driven robots [6], [7], creating not only advantages but also disadvantages for musculoskeletal humanoids. For example, redundant muscles and their nonlinear elasticity [8] enable variable stiffness control [9]. On the other hand, the redundancy introduced by numerous muscles makes modeling and control more challenging [10], increasing the risk of internal forces accumulating and causing damage due to modeling errors. Thus, the properties of muscles are highly diverse and complex, and the advantages and disadvantages that arise from their combinations are even more intricate. 

To date, numerous studies have explored the characteristics, advantages, and disadvantages of musculoskeletal systems. 

> _∗_ Corresponding Author: Kento Kawaharazuka 

> 1 The authors are with the Department of Mechano-Informatics, Graduate School of Information Science and Technology, The University of Tokyo, 7- 3-1 Hongo, Bunkyo-ku, Tokyo, 113-8656, Japan. [kawaharazuka, k-okada, inaba]@jsk.t.u-tokyo.ac.jp 


Fig. 1. The developed musculoskeletal humanoids: Kengoro and Musashi 

In particular, much attention has been given to redundancy. Research topics include variable stiffness utilizing redundancy and nonlinear elasticity [11], [12], the relationship between redundancy and muscle synergies [13], the impact of redundancy on contact force prediction [14], approaches to addressing muscle rupture using redundancy [15], as well as studies that view redundancy as a drawback and explore control methods to reduce it [16]. Additionally, studies cover a wide range of topics, such as the contribution of biarticular muscles to balance control and energy efficiency [17], [18], and learning the complex relationships between muscles and joints that are difficult to model [19], [20]. However, most of these studies are conducted in simulations or on simplified 2D models, with very few focusing on actual full-body musculoskeletal robots. Furthermore, there is still a lack of unified discussion on the characteristics of muscles in robots, how these characteristics should be managed, and how they can be effectively utilized. Most existing discussions remain fragmented and isolated. 

In this study, we empirically categorize and analyze the characteristics of muscles, as well as their management and utilization methods based on the various research conducted on the musculoskeletal humanoids we have developed, Kengoro [4] and Musashi [5] shown in Fig. 1. We classify the characteristics of the musculoskeletal structure into five properties: Redundancy, Independency, Anisotropy, Variable Moment Arm, and Nonlinear Elasticity, organizing the diverse advantages and disadvantages of musculoskeletal humanoids that arise from these combinations. In particular, we describe how to manage and utilize muscle characteristics concerning body schema learning, reflex control, muscle grouping, and 


Fig. 2. The basic musculoskeletal structure: the components include bones, joints, muscle actuators, wires, and nonlinear elastic elements. Muscle length _l_ , muscle tension _f_ , muscle temperature _c_ , and joint angle _θ_ (directly or indirectly depending on the robot) can be measured. 

body schema adaptation. Additionally, we discuss the implementation of movements through an integrated whole-body system, summarizing future challenges and perspectives. 

This study focuses on musculoskeletal humanoids that do not use pulleys at the joints, where the moment arm from the joints to the muscles and the muscle Jacobian are not constant, creating a more human-like musculoskeletal structure. Therefore, wire-driven robots that use pulleys at the joints to maintain constant moment arm [21], [22] are not directly addressed. However, these are simpler systems than musculoskeletal humanoids, so similar theories can be applied. Also, instead of musculoskeletal humanoids operated by pneumatic artificial muscles [23], [24], this study focuses on those that use electric motors to wind wires. Most properties are the same for pneumatic types and similar theories can be applied, but for the sake of unified explanation, we focus on the structure where wires are wound by electric motors. Additionally, note that the hardware is fixed and this study focuses on the software. 

The structure of this study is as follows. In Section II, we provide an overview of the characteristics of musculoskeletal humanoids and their advantages and disadvantages. In Section III, we describe how to address these advantages and disadvantages through body schema learning, reflex control, muscle grouping, and body schema adaptation in the musculoskeletal humanoids Kengoro and Musashi. In Section IV, we describe several motion experiments conducted by integrating these software systems. Finally, in Section V, we discuss future challenges and perspectives based on the research so far. 

## II. OVERVIEW OF CHARACTERISTICS, MANAGEMENT, AND UTILIZATION OF MUSCLES IN MUSCULOSKELETAL HUMANOIDS 

## _A. Basic Musculoskeletal Structure_ 

First, the basic structure of the musculoskeletal humanoid handled in this study is described. As shown in Fig. 2, the musculoskeletal structure consists of bones, joints, muscle actuators, wires, and nonlinear elastic elements. The muscle actuator drives the joint by winding the wire using a pulley attached to the motor. A nonlinear elastic element is attached to the end of the wire to mimic the nonlinear elasticity 

of muscles. Wires are often made of chemical fibers like Dyneema, which are resistant to friction. The muscle actuators are equipped with incremental encoders, tension measurement units, and temperature sensors, allowing the measurement of muscle length _l_ , muscle tension _f_ , and muscle temperature _c_ . Here, the robot’s joint angles are first returned to their initial position, where the muscle lengths are set to zero, and the encoder values are initialized. Some robots (e.g. Musashi [5]) have encoders attached to the joints, allowing for the measurement of the joint angle _θ_ . However, when imitating complex joints such as human ball joints and the scapula (e.g. Kengoro [4]), joint angle sensors cannot be used. In such cases, if the position of the end-effector can be measured using vision sensors, the joint angle _θ_ can be estimated from the relationship between the change in muscle length _l_ and the position of the end-effector [10]. Muscles are redundantly arranged around the joints, and there are muscles that span not only a single joint but also multiple joints. 

Next, the fundamental equations that describe the relationship between joints and muscles in musculoskeletal humanoids are presented. Let the number of muscles be _M_ , the number of joints be _N_ , muscle tension be **_f_** , joint torque be **_τ_** , endeffector force be **_F_** , muscle length be **_l_** , joint angle be **_θ_** , and end-effector position be **_x_** . The following equations generally hold, 


where **_g_** _m_ represents the mapping from **_θ_** to **_l_** , **_g_** _j_ represents the mapping from **_θ_** to **_x_** , **_G_** denotes the muscle Jacobian, and **_J_** denotes the joint Jacobian. Additionally, frequently used values include the minimum and maximum muscle tensions **_f_**<sup>_{min,max}_</sup> and the minimum and maximum muscle velocities **_l_** ˙<sup>_{min,max}_</sup> . 

Next, we discuss joint angle estimation in musculoskeletal humanoids. As mentioned earlier, due to the complex joint structure of musculoskeletal humanoids, they often lack joint angle sensors. Therefore, it is necessary to estimate the joint angle from changes in muscle length. Here, we discuss a method that uses the Extended Kalman Filter (EKF) to estimate the joint angle from changes in muscle length [25]. The prediction and update equations of EKF are as follows, 

## Predict: 


## Update: 


where _t_ is the time step, **_G_**<sup>+</sup> is the pseudoinverse of the muscle Jacobian, ∆ **_l_** is the change in the actual muscle length, **_P_** is the covariance matrix of the estimation error of the joint angle, **_Q_** is the covariance matrix of the error in the time transition, **_e_** is the observation residual, **_R_** is the covariance matrix in the observation space, **_S_** is the covariance matrix of the observation residual, and **_K_** is the Kalman gain. By repeating these predictions and updates, the obtained **_θ_** _t_<sup>_est_</sup> _|t_<sup>becomesthe</sup> current estimated joint angle **_θ_**<sup>_est_</sup> . However, **_θ_**<sup>_est_</sup> obtained here is greatly affected by factors that cannot be modeled, such as muscle stretch and friction, resulting in an error from the actual joint angle. Therefore, the estimated value is corrected using the recognition of AR markers through vision to estimate a joint angle closer to the actual one [10]. For example, when measuring the joint angle of the arm, an AR marker is attached to the end of the hand, and its position is denoted as **_p_** _marker_ . The previously estimated joint angle **_θ_**<sup>_est_</sup> is used as the initial value **_θ_**<sup>_init_</sup> , and the inverse kinematics is solved as follows concerning the target coordinate **_p_**<sup>_re f_</sup> = **_p_** _marker_ , 


where IK denotes the inverse kinematics, and **_θ_**<sup>_est′_</sup> represents the estimated joint angle corrected by vision. The **_θ_**<sup>_est′_</sup> obtained here can be used as the joint angle measured on the actual robot for learning and other purposes. 

Finally, the method to find the muscle tension **_f_** that can realize a given joint torque **_τ_** is described. The muscle tension **_f_** that satisfies the desired joint torque **_τ_** at **_θ_** can be calculated by solving the following quadratic programming, 


where **_W_** 1 is the weight matrix. However, there may be cases where a muscle tension **_f_** that perfectly realizes **_τ_** does not exist. In such cases, the formulation is modified to allow for error as follows [26], 


Fig. 3. The relationship between the characteristics of muscles and the advantages/disadvantages of the musculoskeletal structure. 

_B. Characteristics of Muscles in Musculoskeletal Humanoids_ 

In this study, the characteristics of muscles in musculoskeletal humanoids were classified into the following five categories. 

- Redundancy 

- Independency 

- Anisotropy 

- Variable Moment Arm 

- Nonlinear Elasticity 

Redundancy is the most important characteristic of muscles, indicating that multiple muscles can act on a single joint. Independency refers to the ability to arrange joints and muscles independently, unlike the axis-driven robots where actuators and joints are coupled. Anisotropy describes the nature of muscles that can exert force only in the contraction direction and can loosen in the opposite direction. Variable Moment Arm indicates that, due to its mimicry of the human body, the moment arm of the muscles to the joint varies depending on the joint angle. Nonlinear Elasticity refers to the presence of nonlinear elastic elements attached to the muscles, which is unique to the musculoskeletal structure. 

Note that Redundancy refers to both the property where muscles act antagonistically on a single joint and the property where multiple agonist and antagonist muscles can coexist for the same joint. 

## _C. Advantages/Disadvantages of the Musculoskeletal Structure_ 

The five muscle characteristics described in Section II-B mainly result in the following eight advantages and disadvantages. 

- Modeling Difficulty 

- High Internal Force 

- High Computational Cost 

- Easy Muscle Arrangement 

where **_W_** 2 is the weight matrix. Note that the robots handled in this study basically operate under muscle length control, so this method is not used for muscle tension control. 

- Variable Stiffness Control 

- Muscle Rupture Handling 

- Nonlinearity Utilization 

TABLE I 

THE RELATIONSHIP BETWEEN THE CONTROL RESEARCH ON KENGORO/MUSASHI AND ADVANTAGES/DISADVANTAGES OF THE MUSCULOSKELETAL 

STRUCTURE. 

|Research|Modeling<br>Difficulty|High<br>Internal Force|High<br>Computational Cost|Easy Muscle<br>Arrangement|Variable<br>Stiffness Control|Muscle Rupture<br>Handling|Nonlinearity<br>Utilization|Free Joint<br>Utilization|
|---|---|---|---|---|---|---|---|---|
|Antagonist Inhibition [27]|✓|✓|||||||
|Thermal Control [28]||✓|||||||
|Relaxation Control [29]||✓|||||||
|Stretch Reflex [30]|✓||||||||
|Joint-muscle Mapping [31]|✓|✓|||||||
|Predictive Model [32]|✓||||||||
|Muscle Grouping [33]|||✓||||||
|Muscle Addition [34]||||✓|||||
|Variable Stiffness [35]|||||✓||||
|Muscle Rupture [36]||||||✓|||
|Design Optimization [37]||||✓||✓|||
|Nonlinear Estimation [38]|||||||✓||
|Maximum Speed [39]||||||||✓|


## _•_ Free Joint Utilization 

The top three are disadvantages, and the bottom five are advantages. The relationships between muscle characteristics and their advantages and disadvantages are shown in Fig. 3. 

First, Modeling Difficulty arises from various muscle characteristics such as Redundancy, Anisotropy, Variable Moment Arm, and Nonlinear Elasticity. While axis-driven robots and wire-driven systems with constant moment arms are relatively easy to model, the nonlinear, anisotropic, and redundant nature of muscles makes modeling more challenging. On the other hand, humans are able to skillfully move their complex bodies, so the understanding of this body structure and its control principles is an important research topic. Next, High Internal Force is caused by Redundancy. When muscles are redundantly arranged around a joint, agonist and antagonist muscles can be created, potentially generating high internal forces when they oppose each other. High Computational Cost also results from Redundancy. Due to redundancy, the relationship between joints and muscles becomes complex. For example, calculating the muscle Jacobian or estimating the relationship between joint angle and muscle length requires significant computational resources. Easy Muscle Arrangement is derived from Independency. The ability to arrange muscles independently of the joints allows for the free adjustment of muscle placement and the moment arm. It is not difficult to add new muscles as needed though this is a feature not present in humans. Variable Stiffness Control arises from Redundancy and Nonlinear Elasticity. This is one of the most important characteristics of musculoskeletal structures, allowing for the immediate adaptation to various environments by changing body stiffness at the hardware level rather than through software. Muscle Rupture Handling is also a result of Redundancy. With muscles redundantly arranged around the joints, if one muscle is damaged, other muscles can compensate for its function, allowing the task to continue. While studies have shown that robustness to muscle rupture is not very high in humans [40], it is possible to freely design muscle configurations in musculoskeletal humanoids to ensure robustness against muscle rupture. Nonlinearity Utilization results from Variable Moment Arm. By leveraging the variation in the moment arm of muscles according to the joint angle, nonlinear changes in muscle length can be utilized for control and state 

estimation. When referring to Nonlinearity, one might think of nonlinear elastic elements; however, here it specifically refers to the nonlinearity of the muscle moment arms. Finally, Free Joint Utilization arises from Independency and Anisotropy. By relaxing the muscles to free the joint, it is possible to move the joint flexibly, ignoring the backdrivability of the actuator. 

_D. Management and Utilization of the Musculoskeletal Structure on Kengoro and Musashi_ 

As examples of research conducted with the musculoskeletal humanoids Kengoro and Musashi, we illustrate how to manage these various disadvantages and how to utilize the advantages. 

First, let’s briefly describe the body structures of Kengoro and Musashi. As shown in Fig. 1, Kengoro and Musashi are robots with human-like musculoskeletal structures. Kengoro currently has 124 muscles, while Musashi has 74 muscles in its body. Kengoro was developed to closely mimic human anatomy, featuring a structure very similar to the human skeleton, including the spine, ribs, scapula, radius, and ulna. Therefore, joint angle sensors are not installed, and as described in Section II-A, it is necessary to estimate the current joint angle from muscle length changes and vision sensors. On the other hand, Musashi is a robot designed for ease of design modification by modularizing joints and muscles without aiming for a detailed human mimicry. Encoders are installed within its joint modules, allowing direct measurement of joint angle, making it a platform for research on learning control. In addition to numerous contact sensors on the hands and feet, Musashi is equipped with movable eyeballs, a highprecision camera, and an auditory system, enabling control by integrating various sensor information. 

A table that correlates the control research conducted on Kengoro and Musashi with the advantages and disadvantages of muscles is shown in Table I. For Modeling Difficulty, lowlevel reflex controls (antagonist inhibition control [27] and stretch reflex control [30]) and high-level learning controls (learning of joint-muscle mapping [31] and deep predictive model [32]) can be effectively employed. Note that the lowlevel reflex controller is a controller that accesses a limited number of sensor values and responds quickly at a high frequency (greater than 100 Hz). In contrast, the high-level learning controller is a controller that accesses a wider range 


Fig. 4. The overview of the system which manages and utilizes advantages/disadvantages of the musculoskeletal structure. The components include reflex control (Section III-A), body schema learning (Section III-B), muscle grouping for body schema (Section III-C), and body schema adaptation (Section III-D). 

of modalities and operates at a slower frequency (around 10 Hz is sufficient). High Internal Force can also be managed by combining low-level reflex controls (antagonist inhibition control [27], muscle thermal control [28], and muscle relaxation control [29]) and high-level learning control (learning of joint-muscle mapping [31]). These reflex controls can address modeling errors and internal forces in the short term, while learning control can correct modeling errors and internal forces in the long term. To address High Computational Cost, the computational load of joint-muscle mapping can be reduced by appropriately grouping muscles and joints [33]. Easy Muscle Arrangement allows for the addition of muscles depending on the task, requiring the body schema to be relearned depending on the body change [34]. It is also possible to design muscle placements according to the task [37]. Variable Stiffness Control enables the robot to perform tasks while changing body stiffness according to various environments [35]. Muscle Rupture Handling makes it possible to respond to muscle rupture, allowing for continuous task execution while sequentially updating the body schema [36]. It is also possible to select muscle arrangements that are easier to handle in case of muscle rupture [37]. Nonlinearity Utilization allows for the use of nonlinear muscle length changes corresponding to joint angle changes, specifically the nonlinear changes in muscle Jacobian, enabling absolute joint angle estimation using only relative muscle length changes [38]. Normally, relative changes in muscle length only provide information about changes in joint angle, requiring initialization by setting the muscle length to zero relative to the initial joint angle. However, with this approach, such initialization is no longer necessary. Free Joint Utilization reduces the influence of backdrivability by freeing the joints, allowing for rapid movements that ignore the maximum speed of actuators [39]. 

In the following sections, we organize these studies in a more generalized form and present the integrated overall system. Please refer to each study for details, as we will summarize the outline of each component to maintain coherence. 

III. EMPIRICAL STUDY ON KENGORO AND MUSASHI 

Fig. 4 shows an overview of the software system for musculoskeletal humanoids, summarizing various research. This 

system mainly comprises low-level reflex control and highlevel body schema learning. Surrounding the body schema are components for data collection and its training, state estimation, anomaly detection, and body control using the body schema. At the same time, there are components for muscle grouping for the body schema aimed at reducing computational costs and body schema adaptation that incrementally responds to bodily changes. 

Section III-A discusses low-level reflex control, Section III-B covers body schema learning and control, Section III-C describes muscle grouping in the body schema, and Section III-D explains body schema adaptation. 

## _A. Reflex Control for Musculoskeletal Humanoids_ 

In musculoskeletal humanoids, it is difficult to control all the muscles from the upper layer. Therefore, controlling the muscle length and stiffness through low-level reflex control can enhance the robot’s adaptability. Since musculoskeletal humanoids closely mimic the human body, it is also possible to directly implement reflex controls similar to those in humans. Fig. 5 shows an integrated reflex control system that includes stretch reflex control, antagonist inhibition control, muscle thermal control, maximum speed control, and muscle relaxation control. 

First, the lowest-level control of the musculoskeletal humanoids Kengoro and Musashi is called Muscle Stiffness Control (MSC) and can be expressed for each muscle _i_ as follows [41], 


where **_·_** _i_ represents the value of the _i_ -th muscle, **_f_**<sup>_ref_</sup> is the target muscle tension, **_f_**<sup>_bias_</sup> is the bias term of muscle stiffness control, **_k_** _msc_ is the muscle stiffness coefficient, and **_l_**<sup>_ref_</sup> is the target muscle length. In the following various reflex controls, the robot’s behavior is modified by changing **_k_** _msc_ and **_l_**<sup>_ref_</sup> in this muscle stiffness control. 

Let’s briefly discuss human reflexes. In humans, muscle spindles are spindle-shaped organs attached in parallel to muscle fibers and serve as receptors that detect muscle length _l_ and velocity _l_<sup>˙</sup> . Group Ia fibers from the muscle spindles are 


Fig. 5. The overview of the reflex control system. Muscle relaxation control, maximum speed control, muscle thermal control, antagonist inhibition control, and stretch reflex control alter the muscle length and the muscle stiffness in muscle stiffness control. 

excitatory to the spinal cord’s _α_ motor neurons. When the muscle is suddenly stretched, the frequency of impulses from the muscle spindle increases, exciting the _α_ motor neurons and causing the stretched muscle to contract. This forms a reflex loop known as the stretch reflex, a negative feedback system with muscle length as its output. In contrast, tendon organs are located at the ends of muscles. Unlike muscle spindles, which are arranged in parallel to muscle fibers, tendon organs are connected in series with muscle fibers. Group Ib fibers from tendon organs connect to the spinal cord’s _α_ motor neurons via inhibitory interneurons. When the muscle contracts and muscle tension increases, the frequency of impulses from the tendon organs rises, inhibiting the excitatory action on the _α_ motor neurons. This forms a reflex loop known as the tendon reflex system, a negative feedback system with muscle tension as its output. Additionally, the Ia afferent fibers from the muscle spindles not only excite the motor neurons of the agonist muscle but also inhibit the motor neurons of the antagonist muscle via inhibitory neurons. This interaction between motor neurons of antagonist and agonist muscles is called reciprocal innervation. The stretch reflex control discussed below mimics the human stretch reflex, and the antagonist inhibition control mimics the human reciprocal innervation. 

_1) Stretch Reflex Control (SRC):_ Stretch Reflex Control (SRC) is a control that mimics the human stretch reflex, as mentioned earlier. It contracts each muscle _i_ when its muscle length _li_ is suddenly stretched. In other words, the stretch reflex occurs when the change in muscle length ∆ _li_ = _li,t_ +1 _−li,t_ ( _li,t_ represents the muscle length at time _t_ ) exceeds a threshold _Csrc_ (where _Csrc_ is a constant). However, as described in Section II-A, musculoskeletal humanoids often include nonlinear elastic elements. In this case, even if the muscle is suddenly stretched due to an impact, the deformation of the nonlinear elastic elements, which are more flexible than the motor and can absorb the shock, becomes dominant. The relationship between the muscle tension _fi_ acting on the nonlinear elastic element and its extension ∆ _ni_ can be expressed as an exponential function _fi_ = _e_<sup>_kn_∆</sup><sup>_ni_</sup> (where _kn_ is a constant) [5]. Therefore, it is possible to determine whether 

the muscle has been stretched as follows, 


where _Csrc_<sup>_′_=</sup><sup>_eknCsrc−_1.Inotherwords,thestretchreflex</sup> should occur when the difference in muscle tension between the previous time step ∆ _fi_ = _fi,t_ +1 _− fi,t_ becomes larger than _Csrc_<sup>_′fi,t_. At this point, the target muscle length</sup><sup>_l_</sup> _i_<sup>_ref_</sup> is contracted by a fixed amount ∆ _lsrc,i_ . Afterward, over a time period ∆ _tsrc_ , the contracted length ∆ _lsrc,i_ is gradually returned to its original state. This control not only offers the advantage of risk avoidance and posture stabilization to address Modeling Difficulty, but can also be actively applied to movements such as weightlifting. 

_2) Antagonist Inhibition Control (AIC):_ Antagonist Inhibition Control (AIC) is a control method that mimics human reciprocal innervation, as mentioned earlier. It controls the suppression of the antagonist muscle relative to the agonist muscle. The muscle Jacobian **_G_** ( **_θ_** ) is an _M × N_ matrix that represents how much the muscles contract when the joint at angle **_θ_** moves in a certain direction. In other words, **_G_** ( **_θ_** )( **_θ_**<sup>_ref_</sup> _−_ **_θ_** ) indicates whether each muscle acts as an agonist or an antagonist. In this method, the muscle stiffness **_k_** _msc_ of muscle stiffness control is modified depending on whether the muscle acts as an agonist or antagonist. For the _i_ -th muscle, if _kmsc,i_ is 0, the muscle tension remains constant at _fi_<sup>_bias_</sup> , and if _kmsc,i_ is positive, it generates force in the direction that follows the target muscle length _li_<sup>_ref_</sup> . The antagonist inhibition control is formulated as follows, 


where **_s_** represents the moment arm, _kmsc_<sup>_ref_istheconstant</sup> applied to the stiffness of the agonist muscle, and _Caic_ is the threshold that determines the antagonistic relationship. The default value of _Caic_ is 0, and muscle stiffness is adjusted based on the sign of the moment arm, indicating whether the muscle is an agonist or an antagonist. To ensure motion stability, it is also possible to set _Caic_ to a positive value, which prevents the suppression of antagonist muscles with small moment arms. This control alleviates movement inhibition by Modeling Difficulty and High Internal Force of the musculoskeletal body, allowing for smooth movements across a wide range of motions. 

_3) Muscle Thermal Control (MTC):_ Muscle Thermal Control (MTC) is a reflex mechanism where the activity of a muscle is suppressed as its temperature rises. Here, muscle tension is controlled according to the muscle temperature, which is represented here as the motor core temperature. This mechanism functions similarly to a tendon reflex. In this method, muscle length and muscle tension are not considered as vectors, and each muscle is treated individually. 

A two-resistor temperature model is adopted as the motor’s temperature model, letting _C_ 1 and _C_ 2 be thermal capacities for the motor core and housing respectively, and _R_ 1 and _R_ 2 be thermal resistances between the motor core and motor housing, and between the motor housing and ambient air, respectively. Under this model, the motor core temperature _c_ 1, motor housing temperature _c_ 2, ambient temperature _ca_ , and muscle tension _f_ have the following relationship: 


where _K_ is a constant calculated from the motor’s torque constant, transmission efficiency, gear ratio, pulley radius, and winding resistance. By iterating the recurrence relations of Eq. 24 and Eq. 25 discretely, the motor core temperature _c_ 1 can be estimated. Conversely, the time series of muscle tension **_f_** _seq_<sup>_limit_</sup> that can bring the motor core temperature _c_ 1 to the set maximum value _c_<sup>_max_</sup> 1 as quickly as possible can be calculated similarly to model predictive control. During this process, constraints on the minimum and maximum muscle tension and the smoothness of the time-series transition of muscle tension are added. To prevent the current muscle tension from exceeding the current value _ft_<sup>_limit_</sup> of **_f_** _seq_<sup>_limit_,thetargetmuscle</sup> length _l_<sup>_ref_</sup> of muscle stiffness control is relaxed by ∆ _lmtc_ as follows, 


_else_ 


where _|·|_ denotes the absolute value, ∆ _lmtc,t_ is the relaxation degree at time _t_ , ∆ _l{minus,plus}_ are coefficients that determine the muscle length change amount per step in the negative or positive direction, and _Dgain_ is the coefficient that determines the maximum relaxation amount. In other words, by imposing limits with ∆ _lminusd_ and ∆ _lplusd_ , the muscle is relaxed or tightened to ensure the muscle tension does not exceed the maximum value. With this control, even if excessive muscle length is commanded or excessive force is applied, the muscles will automatically relax to ensure that the motor core temperature does not exceed _c_<sup>_max_</sup> 1 , thus addressing High Internal Force. _4) Maximum Speed Control:_ Maximum Speed Control is a method that adjusts the stiffness and length of muscles to enable rapid joint movements. Musculoskeletal humanoids have redundant muscles, each with different moment arms to the joints and varying maximum muscle length velocities. Muscles with larger moment arms can reach their maximum muscle length velocity more easily, even with the same joint angle velocity. This can impede movement and prevent the joint from achieving its intended angular velocity. Here, we describe two methods to solve this problem. 

The first method is Inhibition Control (IC), which suppresses antagonist muscles with large moment arms by setting the motor current to zero, thereby using backdrivability to 

rapidly release the muscles. This method is quite simple and sets the motor current of some muscles to zero based on the following equations, 


where **_o_** represents the motor current, and _Cic_ is a constant. If _Cic_ = 0, the motor current of only the antagonist muscles becomes zero. If _Cic >_ 0, the motor current of antagonist muscles with large moment arms becomes zero. If the muscle actuators have backdrivability, the muscles will naturally extend when pulled, eliminating the maximum muscle length velocity for these muscles. 

The second method is Elongation Control (EC), which involves pre-elongating the antagonist muscles with large moment arms to enable rapid joint movements. This begins by simulating how pre-elongating antagonist muscles affects movement duration, or joint velocity. Let the current joint angle be **_θ_**<sup>_start_</sup> and the target joint angle be **_θ_**<sup>_end_</sup> . A mask vector **_m_** is created, where muscles to be relaxed in advance are set to 0, and those not to be relaxed are set to 1. The following calculation is then performed, 


where ∆ **_θ_** represents the expected displacement from the current joint angle **_θ_** , _W_ 3 is the weight matrix, and ∆ _t_ is the simulation interval. This allows the calculation of ∆ **_θ_** , which indicates how close the joint can get to **_θ_**<sup>_end_</sup> within ∆ _t_ seconds starting from **_θ_** . The simulation starts at **_θ_** = **_θ_**<sup>_start_</sup> and is updated iteratively as **_θ_** _←_ **_θ_** + ∆ **_θ_** and _t ← t_ + ∆ _t_ until **_θ_**<sup>_end_</sup> is reached. The total time taken is denoted as ∆ _t_<sup>_cost_</sup> , and **_m_** is determined through exhaustive search to minimize ∆ _t_<sup>_cost_</sup> . Finally, based on the muscle length transitions computed by Eq. 29, the muscle length is pre-elongated to ensure that the muscles do not reach their maximum speed. This way, the antagonist muscles do not impede the agonist muscles, allowing for rapid movements through Free Joint Utilization. 

_5) Muscle Relaxation Control (MRC):_ Muscle Relaxation Control is a simple control method that gradually relaxes muscles without affecting the posture. First, the necessary joint torque **_τ_**<sup>_nec_</sup> at the current joint angle **_θ_** is calculated, and the muscle tension **_f_**<sup>_nec_</sup> required to maintain this torque is computed using Eq. 18. Next, the muscles are sorted in ascending order based on **_f_**<sup>_nec_</sup> . The muscles with the smallest **_f_**<sup>_nec_</sup> values, i.e., those not essential for maintaining posture, are examined sequentially. If the current muscle tension sensor value _fi_ for the muscle _i_ is less than _f_<sup>_min_</sup> , the control moves on to the next muscle _i_ + 1. If _fi > f_<sup>_min_</sup> , the value of ∆ _li_ is checked. If ∆ _li_ + ∆ _l_ + _>_ ∆ _l_<sup>_max_</sup> (∆ _l_ + represents the muscle relaxation amount per step), the control proceeds to the next muscle _i_ + 1. If ∆ _li_ + ∆ _l_ + _<_ ∆ _l_<sup>_max_</sup> , then ∆ _li_ is updated as ∆ _li ←_ min(∆ _li_ + ∆ _l_ + _,_ ∆ _l_<sup>_max_</sup> ). If the update of ∆ _li_ succeeds even once, the loop exits. If not, the process is repeated for all muscles. 

This describes the basic operation of muscle relaxation control, but several conditions apply to its activation. Firstly, 


Fig. 6. The overview of the body schema learning and control system. The system consists of the data collector, network trainer, online updater, controller, anomaly detector, state estimator, and simulator. 

muscle relaxation control operates only in a static state where the muscle length command **_l_**<sup>_re f_</sup> is not fluctuating. When **_l_**<sup>_re f_</sup> is fluctuating, i.e., during movement, the muscles with the highest **_f_**<sup>_nec_</sup> are targeted in descending order, and ∆ _li_ is reverted to 0 as ∆ _li ←_ max(∆ _li −_ ∆ _l−,_ 0) (∆ _l−_ represents the muscle contraction amount per step). Additionally, muscle relaxation control stops if the norm of the difference between the current joint angle **_θ_** and the joint angle **_θ_**<sup>_init_</sup> at the moment when **_l_**<sup>_re f_</sup> stopped is greater than a maximum allowable change ∆ _θ_<sup>_max_</sup> . This ensures that muscle relaxation does not significantly affect the posture. This control allows for the suppression of High Internal Force in antagonistic relationships, which enables continuous movement, internal force suppression due to contact with the environment, and actions such as using the environment to rest the body. 

_B. Body Schema Learning and Control for Musculoskeletal Humanoids_ 

We describe the body schema learning, the layer above the reflex control, as well as control and state estimation using this schema. In this study, we refer to a model that represents the relationships between sensory input and motor output, describing correlations such as how movements of the body affect vision, touch, sound, and temperature, as a body schema [42], [43]. The overall system including the body schema is shown in Fig. 6. The body schema in this study is represented as follows, 


where **_x_** _in_ is the network input, **_x_** _out_ is the network output, **_m_** is the mask variable, **_z_** is the latent variable, **_h_** _enc_ represents the encoder part of the neural network, **_h_** _dec_ represents the decoder part, and **_h_** represents the entire network. The mask variable is used to represent the correlation between the sensors included in **_x_** _{in,out}_ by masking some of the inputs to predict the outputs. The variables **_x_** _{in,out}_ are consolidated and generalized as **_x_** , which includes various sensor values and control inputs such as joint angle, muscle tension, muscle length, and contact force. Using this body schema as the core, the system can perform data collection, network training, and 

online update, as well as control, state estimation, anomaly detection, and simulation for the musculoskeletal humanoid. When the time at which **_x_** _out_ is obtained is the same as the time at which **_x_** _in_ is obtained, it is referred to as a static body schema. When they differ, i.e., **_x_** _out_ is at time _t_ + 1 and **_x_** _in_ is at time _t_ , it is called a dynamic body schema. The static body schema [44] represents the correlation between sensor values at the same time, while the dynamic body schema [32] represents the temporal state transitions of sensor values. We will summarize the system for musculoskeletal humanoids for each of these schemas. 

_1) Static Body Schema:_ The static body schema in the musculoskeletal structure represents the correlations among various sensors, particularly the joint angle **_θ_** , muscle tension **_f_** , and muscle length **_l_** , which are indispensable in musculoskeletal systems. This is also referred to as joint-muscle mapping. There are three relationships among these three sensors: it is possible to estimate **_l_** from **_θ_** and **_f_** , estimate **_θ_** from **_f_** and **_l_** , and estimate **_f_** from **_l_** and **_θ_** . The variables are set as follows. 


The input and output of the network are **_θ_** , **_f_** , and **_l_** , and the mask variable **_m_** represents their respective relationships. For example, when **_m_** is �1 1 0�, **_l_** is treated as **0** , and **_l_** is estimated from **_θ_** and **_f_** . In other words, all of **_θ_** , **_f_** , and **_l_** are estimated from **_θ_** and **_f_** . After collecting data **_x_** from the actual robot, a static body schema of the musculoskeletal structure can be learned by randomly varying **_m_** , masking **_x_** , and training the network accordingly. To cope with temporal changes in the body schema, online learning is also possible, in which the network weights **_W_** are updated in real time based on the data **_x_** . If we want to find the muscle length that minimizes muscle tension while bringing the joint angle closer to the target value **_θ_**<sup>_ref_</sup> , the network can be used to optimize **_z_** through forward and backward propagation to minimize _||_ **_θ_**<sup>_ref_</sup> _−_ **_θ_** _||_ 2 + _||_ **_f_** _||_ 2, ultimately obtaining **_l_** . In a similar manner, it is also possible to estimate joint angles from muscle length and muscle tension, simulate joint angle and muscle tension changes based on muscle length changes, and detect anomalies using the reconstruction error of network outputs for muscle length and muscle tension. The static body schema 

training can overcome Modeling Difficulty. Additionally, by using this static body schema to realize the desired muscle tensions, it becomes possible to achieve Variable Stiffness Control, allowing impacts to be either softly absorbed or rigidly resisted as needed. 

Note that the simpler the network structure, the easier it is to train the body schema. If the goal is simply to obtain muscle length from the target joint angle, **_x_** _in_ = **_θ_** and **_x_** _out_ = **_l_** can be set accordingly [10]. Furthermore, by setting **_x_**<sup>_T_</sup> _in_<sup>=</sup> � **_θ_**<sup>_T_</sup> **_f_**<sup>_T_�</sup> and **_x_**<sup>_T_</sup> _out_<sup>=</sup><sup>**_l_**</sup><sup>_T_,controlthattakesmuscletensionintoaccount</sup> becomes possible [35], [45]. 

_2) Dynamic Body Schema:_ The dynamic body schema in the musculoskeletal structure is a state equation that represents the time-series changes of various sensor values, including joint angle, muscle tension, muscle length, muscle temperature, and contact force. Here, we will explain object grasping with a musculoskeletal hand as an example of the dynamic body schema. 

The musculoskeletal hand of Musashi [46] is equipped with sensors that measure the wrist joint angle **_θ_** , muscle tension **_f_** , muscle length **_l_** , and contact force **_f_** _contact_ at the fingertips and palm. The dynamic body schema that expresses the timeseries changes in each sensor value when an object is grasped and the fingers are moved is represented as follows, 


where ∆ **_l_**<sup>_ref_</sup> is the control input, which is the difference in the muscle length command. The mask variable **_m_** indicates that the changes in sensor values at time _t_ + 1 can be inferred from the sensor values and control inputs at time _t_ . Moreover, if this network **_h_** is a recurrent neural network that can take time series information into account, it can predict the sensor values at the next time step using only the control inputs. By collecting time-series data **_x_** from the actual robot while randomly commanding ∆ **_l_**<sup>_re f_</sup> , and training the network while randomly varying **_m_** , it is possible to learn a dynamic body schema of the musculoskeletal hand. To cope with temporal changes in the body schema, online learning is also possible, in which the network weights **_W_** or learnable latent variables [47] are updated in real time based on the data **_x_** . If it is necessary to adjust the control inputs to maintain the initial contact force **_f_** _contact_<sup>_init_consistently throughout some movement,</sup> ∆ **_l_**<sup>_ref_</sup> can be optimized by iteratively performing forward and backward propagation to minimize _||_ **_f_** _contact_<sup>_init−_</sup><sup>**_f_**</sup><sup>_contact||_2in</sup> the same manner as model predictive control. As this is a state equation, not only contact simulation and estimation but also anomaly detection using reconstruction errors _danomaly_ are possible. Additionally, although not detailed here, by using Parametric Bias [47], which can represent the time-series changes of various sensor values when grasping different objects within a single network, it is even possible to recognize what object is currently being grasped. These methods are applicable not only to the musculoskeletal hand but also to various body parts and object manipulation scenarios [48]– [50]. 


Fig. 7. The grouping of muscles in body schema of musculoskeletal humanoids for reduction of high computational cost. 

## _C. Muscle Grouping for Musculoskeletal Humanoids_ 

Controlling all muscles simultaneously in a musculoskeletal humanoid is computationally intensive and impractical. To reduce this high computational cost, it is necessary to perform muscle grouping for the body schema. As shown in Fig. 7, multiple muscles are arranged around each joint in the musculoskeletal humanoid. By appropriately grouping these muscles, the static body schema can be divided, thereby reducing the computational cost. There are two methods for this: manual grouping [38] and automatic grouping [33], which are described below. 

Manual Grouping reduces computational cost by manually partitioning the static body schema into groups of joints and muscles. This method is straightforward: a small number of target joints for which the body schema is to be constructed are selected, and the muscle groups capable of moving those joints are identified. The joints that these muscles can move are then added to the target joint group, forming a single group. For example, to estimate joint angle of the 3 degrees of freedom of the shoulder joint, the muscle group capable of moving these 3 degrees of freedom is selected. This muscle group includes several multi-articular muscles such as the biceps brachii and pectoralis major, which also influence other joints. Consequently, joints like the elbow and scapula are included in the group. In the case of the shoulder of Kengoro, for instance, the static body schema corresponds to 10 muscles and 10 degrees of freedom. Similarly, constructing a static body schema for the neck requires a correspondence of 10 muscles and 16 degrees of freedom. Joint angle estimation is performed only on the initially targeted joints, while values estimated from other static body schemas are used for the remaining joints. Although various granularities can be considered for partition sizes, it is generally preferable, from a maintenance perspective, to have a small number of large static body schemas rather than many small ones. 

Automatic Grouping automates the manual grouping process to achieve more appropriate groupings. Two types of information aid in grouping the numerous redundant muscles spread throughout the body: functional connections and spatial connections. Functional connections indicate that muscles, 


Fig. 8. The adaptation for the change in body schema due to muscle addition and muscle rupture. 

due to their redundancy, are functionally related to each other, reflecting the strength of their correlations (e.g., the relationship between agonist and antagonist muscles is strong). Spatial connections represent the spatial proximity of muscles based on their neural connections (e.g., the spatial connection between leg muscles and arm muscles is weak). The former is derived from the network weights of the static body schema, while the latter is calculated from the geometric model and embedded into a graph structure. By performing graph partitioning, appropriate muscle grouping is achieved automatically. Through this method, the robot can identify functional connections from its random movements and combine these with spatial connections to achieve appropriate muscle grouping. This allows for the creation of interpretable and manageable controllers for each group, maintaining accuracy while reducing computational cost and complexity. 

## _D. Body Schema Adaptation for Musculoskeletal Humanoids_ 

In musculoskeletal humanoids, the body schema can change due to various factors. Due to Redundancy and Independency of muscles, musculoskeletal humanoids can adapt their body schema in response to bodily changes such as muscle addition [34] and muscle rupture [36], as shown in Fig. 8. 

In muscle addition, new muscles are added to the musculoskeletal humanoid according to the task, and the body schema is relearned. If a task requires more force, muscles can be added to modify the body to provide sufficient force. In this case, the static body schema will have an increased dimension for muscle tension and muscle length. Therefore, a new static body schema corresponding to the new number of muscles is constructed, and the weights of the original body schema are copied. Subsequently, the network’s weights for the new muscles are relearned using random movements while ensuring that the relationships between the original muscles and joints are preserved. 

In muscle rupture adaptation, if a muscle in the musculoskeletal humanoid ruptures for some reason, the body schema is updated to allow the remaining muscles to continue the task. In this case, the muscle rupture is detected 

through the prediction error of the body schema, and a mask variable **_r_** is introduced to mask the ruptured muscle in the body schema. For the original network training, joint angle estimation, posture control, etc., network inputs and outputs are partially masked by **_r_** to ignore the ruptured muscles. This enables control, state estimation, and training to continue without being affected by the ruptured muscles. 

## IV. REALIZATION OF VARIOUS TASKS 

We present examples that demonstrate the effectiveness of the characteristics of musculoskeletal humanoids and their management and utilization methods through several experiments [10], [36], [49], [51]. As this paper is a perspective review, we summarize representative experimental sequences here; detailed quantitative evaluations and method-by-method comparisons are provided in the original papers cited above. 

First, in Fig. 9 (a), we show an object-grasping experiment based on online learning for the musculoskeletal humanoid Kengoro. Here, an accurate body schema is gradually acquired through online learning of the static body schema, allowing object grasping through control based on this schema. Initially, in frame _⃝_ 2 , inverse kinematics on the can fails to achieve the intended grasp. However, through online learning in frames _⃝_ 4 – _⃝_ 5 and _⃝_ 8 – _⃝_ 9 , successful grasping is eventually achieved. Next, Fig. 9 (b) shows a muscle rupture adaptation experiment with the musculoskeletal humanoid Musashi. When a muscle rupture occurs, it is detected as an anomaly from the prediction error of the static body schema in frame _⃝_ 3 . The body schema is then relearned to account for the ruptured muscle through random movements in frames _⃝_ 4 – _⃝_ 5 , ultimately succeeding in the intended object manipulation. 

Then, Fig. 9 (c) illustrates a table-setting task involving flexible cloth manipulation using the musculoskeletal wheeled robot Musashi-W. Here, muscle relaxation control and muscle thermal control are employed as reflex controls. A static body schema is used for regular movements, and a dynamic body schema is used for dynamic flexible cloth manipulation to complete the series of tasks. In particular, during dynamic cloth manipulation, adaptively modulating the body stiffness through Variable Stiffness Control improves the maximum joint velocity by 12%, successfully enabling the cloth to be spread more widely. The robot successfully recognizes the tablecloth, grasps it, manipulates it using a dynamic body schema that takes cloth images as input and output, sets it on the table, and then places snacks on the table. 

Finally, Fig. 9 (d) presents an autonomous driving experiment with the musculoskeletal humanoid Musashi. Muscle relaxation control and muscle thermal control are used as reflex controls, with a static body schema employed for steering and a dynamic body schema used for pedal operation. The robot successfully recognized traffic signals, operated the pedals using a dynamic body schema with vehicle speed as input and output, and turned the steering wheel to navigate through intersections. 

## V. DISCUSSION 

In this study, we attempted an integrated explanation by organizing the characteristics of muscles in musculoskeletal 


Fig. 9. Experiments on Kengoro and Musashi: (a) shows the object grasping experiment on Kengoro with online learning of the static body schema, (b) shows the muscle rupture response experiment on Musashi, (c) shows the table setting operation experiment including deformable cloth manipulation by Musashi-W, and (d) shows the integrated autonomous driving experiment by Musashi. 

humanoids and the advantages and disadvantages arising from them. We built a comprehensive system to overcome and leverage these disadvantages and advantages, which includes reflex control, body schema learning, muscle grouping, and body schema adaptation. Reflex control encompasses stretch reflex control, antagonist inhibition control, muscle thermal control, maximum speed control, and muscle relaxation control. Body schema learning includes static body schemas that represent joint-muscle mapping and dynamic body schemas that represent state equations. Muscle grouping involves both manual and automatic grouping, while body schema adaptation includes muscle addition and muscle rupture adaptation. This integrated system can manage the shortcomings of musculoskeletal humanoids and make effective use of their advantages, enabling tasks such as object grasping, dynamic flexible object manipulation, and autonomous driving. 

Stretch reflex control, antagonistic inhibition control, and muscle relaxation control have proven useful in certain movements. However, when applied to precise manipulations, they can interfere with the accuracy of movements, and are therefore typically disabled. These reflexes reduce muscle load and function as a sort of safety mechanism, but as a result, posture may shift slightly. Humans also increase body stiffness and move cautiously during precise tasks [52], making reflex control that disrupts these antagonistic relationships unsuitable for precise movements. A mechanism to switch reflexes will likely become more important in the future. Additionally, muscle thermal control is always effective, while maximum speed control is only effective during rapid movements. 

Currently, the estimation of joint angle in Kengoro relies on muscle length changes and vision. However, since this is based on external sensory input, it is not highly reliable; for instance, joint angle cannot be estimated if vision is obstructed. In contrast, using static body schema learning gradually enables joint angle estimation from muscle length and muscle tension. Internal sensing encompasses not only muscle length and muscle tension but also various types of information, such as IMUs, joint capsule pressure, and skin stretch. In the future, we aim to implement these sensors and develop a more accurate and reliable method for estimating the state of the musculoskeletal system. 

This study does not address energy storage and release through redundancy and nonlinear elastic elements. Previous research has utilized muscle energy storage and release in exoskeletons [53] and jumping spider robots [54]. Naturally, this concept is also applicable to musculoskeletal humanoids, but the current challenge lies in nonlinear elastic elements. The nonlinear elastic elements used in Musashi [5] achieve nonlinear elasticity using rubber O-rings. However, the high viscosity of the rubber reduces the effectiveness of energy storage and release. On the other hand, nonlinear elastic elements constructed with springs [55] become too large to apply to robots like Musashi or Kengoro, which have numerous muscles. Future discussions must address the shapes, characteristics, and utilization of nonlinear elasticity. 

In this study, we have not deeply examined robustness against disturbances such as dynamic obstacles or forces exerted by the external environment. Control of musculoskeletal 

humanoids is still in its early stages of development, and current research has mainly focused on internal issues such as Modeling Difficulty, High Internal Force, and High Computational Cost, while stability in interaction with the external environment has not been extensively discussed. On the other hand, Variable Stiffness Control through body schema learning, as well as reflex-based controls such as stretch reflex control, muscle thermal control, and muscle relaxation control, are effective against dynamic obstacles and external forces from the environment. In future work, we plan to investigate the usefulness of control and learning from a broader perspective that includes not only the internal body dynamics but also interactions with the environment. 

This study does not focus deeply on the hardware aspects. The advantages of musculoskeletal humanoids go beyond control and are largely influenced by their physical structures. For example, complex joints like scapulae and passive elements like the spine can be created [56], or gear ratios can be adjusted according to the movement [57]. The flexibility to rearrange components allows for easy reconfiguration. On the other hand, this study deliberately avoids deep discussion on hardware, focusing primarily on software, aiming to present a clearer understanding of muscle management and utilization methods. Future research will examine hardware aspects in greater detail to achieve long-term, stable, and more humanlike movements in musculoskeletal humanoids. 

Currently, discussions from a developmental and cognitive perspective are not included. This is because operating a fullbody musculoskeletal humanoid requires a significant amount of engineering, making it a time-intensive process to reach a stage where cognitive development can be discussed. Body schema learning is highly beneficial from a cognitive development perspective as well. Future work will explore its internal states, comparisons with humans, muscle synergies, and related topics. 

## VI. CONCLUSION 

In this study, we organized the characteristics of muscles in musculoskeletal humanoids and the advantages and disadvantages that arise from them. Using the musculoskeletal humanoids Kengoro and Musashi as examples, we conducted an integrated discussion on how to empirically manage their disadvantages and leverage their advantages. The characteristics of muscles include Redundancy, Independency, Anisotropy, Variable Moment Arm, and Nonlinear Elasticity. From these characteristics arise advantages and disadvantages such as Modeling Difficulty, High Internal Force, High Computational Cost, Easy Muscle Arrangement, Variable Stiffness Control, Muscle Rupture Handling, Nonlinearity Utilization, and Free Joint Utilization. These can be managed and utilized through low-level reflex control, high-level learning control, muscle grouping, and body schema adaptation in musculoskeletal humanoids. Several experiments have shown that long-term and stable movements can be realized by musculoskeletal humanoids through these methods. We hope this study provides a unified discussion on the characteristics of musculoskeletal structures and their management and utilization methods, serving as a foundation for future research. 

## ACKNOWLEDGMENTS 

This work was partially supported by JST FOREST Grant Number JPMJFR232N, Japan. 

## REFERENCES 

- [1] M. J¨antsch, S. Wittmeier, K. Dalamagkidis, A. Panos, F. Volkart, and A. Knoll, “Anthrob - A Printed Anthropomimetic Robot,” in _2013 IEEERAS International Conference on Humanoid Robots_ , 2013, pp. 342–347. 

- [2] H. G. Marques, M. J¨antsh, S. Wittmeier, O. Holland, C. Alessandro, A. Diamond, M. Lungarella, and R. Knight, “ECCE1: the first of a series of anthropomimetic musculoskeletal upper torsos,” in _2010 IEEE-RAS International Conference on Humanoid Robots_ , 2010, pp. 391–396. 

- [3] Y. Nakanishi, Y. Asano, T. Kozuki, H. Mizoguchi, Y. Motegi, M. Osada, T. Shirai, J. Urata, K. Okada, and M. Inaba, “Design concept of detail musculoskeletal humanoid “Kenshiro” - Toward a real human body musculoskeletal simulator,” in _2012 IEEE-RAS International Conference on Humanoid Robots_ , 2012, pp. 1–6. 

- [4] Y. Asano, T. Kozuki, S. Ookubo, M. Kawamura, S. Nakashima, T. Katayama, Y. Iori, H. Toshinori, K. Kawaharazuka, S. Makino, Y. Kakiuchi, K. Okada, and M. Inaba, “Human Mimetic Musculoskeletal Humanoid Kengoro toward Real World Physically Interactive Actions,” in _2016 IEEE-RAS International Conference on Humanoid Robots_ , 2016, pp. 876–883. 

- [5] K. Kawaharazuka, S. Makino, K. Tsuzuki, M. Onitsuka, Y. Nagamatsu, K. Shinjo, T. Makabe, Y. Asano, K. Okada, K. Kawasaki, and M. Inaba, “Component Modularized Design of Musculoskeletal Humanoid Platform Musashi to Investigate Learning Control Systems,” in _2019 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2019, pp. 7294–7301. 

- [6] K. Hirai, M. Hirose, Y. Haikawa, and T. Takenaka, “The Development of Honda Humanoid Robot,” in _1998 IEEE International Conference on Robotics and Automation_ , 1998, pp. 1321–1326. 

- [7] K. Kaneko, F. Kanehiro, S. Kajita, H. Hirukawa, T. Kawasaki, M. Hirata, K. Akachi, and T. Isozumi, “Humanoid robot HRP-2,” in _2004 IEEE International Conference on Robotics and Automation_ , 2004, pp. 1083– 1090. 

- [8] B. Calvo, A. Ram´ırez, A. Alonso, J. Grasa, F. Soteras, R. Osta, and M. Mu˜noz, “Passive nonlinear elastic behaviour of skeletal muscle: experimental results and model formulation,” _Journal of biomechanics_ , vol. 43, no. 2, pp. 318–325, 2010. 

- [9] H. Kobayashi, K. Hyodo, and D. Ogane, “On Tendon-Driven Robotic Mechanisms with Redundant Tendons,” _The International Journal of Robotics Research_ , vol. 17, no. 5, pp. 561–571, 1998. 

- [10] K. Kawaharazuka, S. Makino, M. Kawamura, Y. Asano, K. Okada, and M. Inaba, “Online Learning of Joint-Muscle Mapping using Vision in Tendon-driven Musculoskeletal Humanoids,” _IEEE Robotics and Automation Letters_ , vol. 3, no. 2, pp. 772–779, 2018. 

- [11] D. Stanev and K. Moustakas, “Stiffness modulation of redundant musculoskeletal systems,” _Journal of biomechanics_ , vol. 85, pp. 101–107, 2019. 

- [12] S. Tsuboi, H. Kino, and K. Tahara, “End-Point stiffness and joint viscosity control of musculoskeletal robotic arm using muscle redundancy,” in _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2022, pp. 4997–5002. 

- [13] R. S. Razavian, B. Ghannadi, and J. McPhee, “On the relationship between muscle synergies and redundant degrees of freedom in musculoskeletal systems,” _Frontiers in Computational Neuroscience_ , vol. 13, p. 23, 2019. 

- [14] F. Moissenet, L. Ch`eze, and R. Dumas, “Influence of the level of muscular redundancy on the validity of a musculoskeletal model,” _Journal of Biomechanical Engineering_ , vol. 138, no. 2, 2016. 

- [15] E. Almanzor, T. Sugiyama, A. Abdulali, M. Hayashibe, and F. Iida, “Utilising redundancy in musculoskeletal systems for adaptive stiffness and muscle failure compensation: a model-free inverse statics approach,” _Bioinspiration & Biomimetics_ , 2024. 

- [16] S. Zhong, J. Chen, X. Niu, H. Fu, and H. Qiao, “Reducing Redundancy of Musculoskeletal Robot with Convex Hull Vertexes Selection,” _IEEE Transactions on Cognitive and Developmental Systems_ , pp. 1–1, 2019. 

- [17] M. A. Sharbafi, C. Rode, S. Kurowski, D. Scholz, R. M¨ockel, K. Radkhah, G. Zhao, A. M. Rashty, O. V. Stryk, and A. Seyfarth, “A new biarticular actuator design facilitates control of leg function in BioBiped3,” _Bioinspiration & Biomimetics_ , vol. 11, no. 4, p. 046003, 2016. 

- [18] A. Nejadfard, K. Berns, and P. Vonwirth, “Technical advantages and disadvantages of biarticular actuators in bipedal robots,” _Robots Human Life_ , vol. 166, 2020. 

- [19] A. Marjaninejad, D. Urbina-Mel¨endez, B. A. Cohn, and F. J. ValeroCuevas, “Autonomous functional movements in a tendon-driven limb via limited experience,” _Nature Machine Intelligence_ , vol. 1, no. 3, pp. 144–154, 2019. 

- [20] D. A. Hagen, A. Marjaninejad, G. E. Loeb, and F. J. Valero-Cuevas, “insideOut: A Bio-Inspired Machine Learning Approach to Estimating Posture in Robots Driven by Compliant Tendons,” _Frontiers in Neurorobotics_ , vol. 15, 2021. 

- [21] G. Endo, A. Horigome, and A. Takata, “Super Dragon: A 10-m-LongCoupled Tendon-Driven Articulated Manipulator,” _IEEE Robotics and Automation Letters_ , vol. 4, no. 2, pp. 934–941, 2019. 

- [22] K. Koganezawa and M. Yamazaki, “Mechanical stiffness control of tendon-driven joints,” in _1999 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 1999, pp. 818–825. 

- [23] K. Ogawa, K. Narioka, and K. Hosoda, “Development of whole-body humanoid “pneumat-BS” with pneumatic musculoskeletal system,” in _2011 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2011, pp. 4838–4843. 

- [24] I. Mizuuchi, M. Kawamura, T. Asaoka, and S. Kumakura, “Design and development of a compressor-embedded pneumatic-driven musculoskeletal humanoid,” in _2012 IEEE-RAS International Conference on Humanoid Robots_ , 2012, pp. 811–816. 

- [25] S. Ookubo, Y. Asano, T. Kozuki, T. Shirai, K. Okada, and M. Inaba, “Learning Nonlinear Muscle-Joint State Mapping Toward Geometric Model-Free Tendon Driven Musculoskeletal Robots,” in _2015 IEEE-RAS International Conference on Humanoid Robots_ , 2015, pp. 765–770. 

- [26] M. Kawamura, S. Ookubo, Y. Asano, T. Kozuki, K. Okada, and M. Inaba, “A Joint-Space Controller Based on Redundant Muscle Tension for Multiple DOF Joints in Musculoskeletal Humanoids,” in _2016 IEEE-RAS International Conference on Humanoid Robots_ , 2016, pp. 814–819. 

- [27] K. Kawaharazuka, M. Kawamura, S. Makino, Y. Asano, K. Okada, and M. Inaba, “Antagonist Inhibition Control in Redundant Tendondriven Structures Based on Human Reciprocal Innervation for Wide Range Limb Motion of Musculoskeletal Humanoids,” _IEEE Robotics and Automation Letters_ , vol. 2, no. 4, pp. 2119–2126, 2017. 

- [28] K. Kawaharazuka, N. Hiraoka, K. Tsuzuki, M. Onitsuka, Y. Asano, K. Okada, K. Kawasaki, and M. Inaba, “Estimation and Control of Motor Core Temperature with Online Learning of Thermal Model Parameters: Application to Musculoskeletal Humanoids,” _IEEE Robotics and Automation Letters_ , vol. 5, no. 3, pp. 4273–4280, 2020. 

- [29] K. Kawaharazuka, K. Tsuzuki, M. Onitsuka, Y. Koga, Y. Omura, Y. Asano, K. Okada, K. Kawasaki, and M. Inaba, “Reflex-based Motion Strategy of Musculoskeletal Humanoids under Environmental Contact Using Muscle Relaxation Control,” in _2019 IEEE-RAS International Conference on Humanoid Robots_ , 2019, pp. 114–119. 

- [30] K. Kawaharazuka, Y. Koga, K. Tsuzuki, M. Onitsuka, Y. Asano, K. Okada, K. Kawasaki, and M. Inaba, “Applications of Stretch Reflex for the Upper Limb of Musculoskeletal Humanoids: Protective Behavior, Postural Stability, and Active Induction,” in _2020 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2020, pp. 3598– 3603. 

- [31] K. Kawaharazuka, K. Tsuzuki, M. Onitsuka, Y. Asano, K. Okada, K. Kawasaki, and M. Inaba, “Musculoskeletal AutoEncoder: A Unified Online Acquisition Method of Intersensory Networks for State Estimation, Control, and Simulation of Musculoskeletal Humanoids,” _IEEE Robotics and Automation Letters_ , vol. 5, no. 2, pp. 2411–2418, 2020. 

- [32] K. Kawaharazuka, K. Okada, and M. Inaba, “Deep Predictive Model Learning with Parametric Bias: Handling Modeling Difficulties and Temporal Model Changes,” _IEEE Robotics Automation Magazine_ , 2023. 

- [33] K. Kawaharazuka, M. Nishiura, Y. Koga, Y. Omura, Y. Toshimitsu, Y. Asano, K. Okada, K. Kawasaki, and M. Inaba, “Automatic Grouping of Redundant Sensors and Actuators Using Functional and Spatial Connections: Application to Muscle Grouping for Musculoskeletal Humanoids,” _IEEE Robotics and Automation Letters_ , vol. 6, no. 2, pp. 1981–1988, 2021. 

- [34] K. Kawaharazuka, A. Miki, Y. Toshimitsu, K. Okada, and M. Inaba, “Adaptive Body Schema Learning System Considering Additional Muscles for Musculoskeletal Humanoids,” _IEEE Robotics and Automation Letters_ , vol. 7, no. 2, pp. 3459–3466, 2022. 

- [35] K. Kawaharazuka, K. Tsuzuki, S. Makino, M. Onitsuka, Y. Asano, K. Okada, K. Kawasaki, and M. Inaba, “Long-time Self-body Image Acquisition and its Application to the Control of Musculoskeletal Structures,” _IEEE Robotics and Automation Letters_ , vol. 4, no. 3, pp. 2965–2972, 2019. 

- [36] K. Kawaharazuka, M. Nishiura, Y. Toshimitsu, Y. Omura, Y. Koga, Y. Asano, K. Okada, K. Kawasaki, and M. Inaba, “Robust Continuous Motion Strategy Against Muscle Rupture using Online Learning of Redundant Intersensory Networks for Musculoskeletal Humanoids,” _Robotics and Autonomous Systems_ , vol. 152, pp. 1–14, 2022. 

- [37] K. Kawaharazuka, Y. Toshimitsu, M. Nishiura, Y. Koga, Y. Omura, Y. Asano, K. Okada, K. Kawasaki, and M. Inaba, “Design Optimization of Musculoskeletal Humanoids with Maximization of Redundancy to Compensate for Muscle Rupture,” in _2021 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2021, pp. 3227–3233. 

- [38] K. Kawaharazuka, S. Makino, M. Kawamura, Y. Asano, K. Okada, and M. Inaba, “A Method of Joint Angle Estimation Using Only Relative Changes in Muscle Lengths for Tendon-driven Humanoids with Complex Musculoskeletal Structures,” in _2018 IEEE-RAS International Conference on Humanoid Robots_ , 2018, pp. 1128–1135. 

- [39] K. Kawaharazuka, Y. Koga, K. Tsuzuki, M. Onitsuka, Y. Asano, K. Okada, K. Kawasaki, and M. Inaba, “Exceeding the Maximum Speed Limit of the Joint Angle for the Redundant Tendon-driven Structures of Musculoskeletal Humanoids,” in _2020 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2020, pp. 3585–3590. 

   - [54] A. Spr¨owitz, C. G¨ottler, A. Sinha, C. Caer, M. U. Ooztekin, K. Petersen,<sup>¨</sup> and M. Sitti, “Scalable pneumatic and tendon driven robotic joint inspired by jumping spiders,” in _2017 IEEE International Conference on Robotics and Automation_ , 2017, pp. 64–70. 

   - [55] Y. Nakanishi, T. Izawa, M. Osada, N. Ito, S. Ohta, J. Urata, and M. Inaba, “Development of Musculoskeletal Humanoid Kenzoh with Mechanical Compliance Changeable Tendons by Nonlinear Spring Unit,” in _2011 IEEE International Conference on Robotics and Biomimetics_ , 2011, pp. 2384–2389. 

   - [56] M. Osada, T. Izawa, J. Urata, Y. Nakanishi, K. Okada, and M. Inaba, “Approach of “planar muscle” suitable for musculoskeletal humanoids, especially for their body trunk with spine having multiple vertebral,” in _2011 IEEE-RAS International Conference on Humanoid Robots_ , 2011, pp. 358–363. 

   - [57] B. Kim and A. D. Deshpande, “Design of nonlinear rotational stiffness using a noncircular pulley-spring mechanism,” _Journal of Mechanisms and Robotics_ , vol. 6, no. 4, 2014. 

- [40] J. J. Kutch and F. J. Valero-Cuevas, “Muscle redundancy does not imply robustness to muscle dysfunction,” _Journal of biomechanics_ , vol. 44, no. 7, pp. 1264–1270, 2011. 

- [41] T. Shirai, J. Urata, Y. Nakanishi, K. Okada, and M. Inaba, “Whole body adapting behavior with muscle level stiffness control of tendon-driven multijoint robot,” in _2011 IEEE International Conference on Robotics and Biomimetics_ , 2011, pp. 2229–2234. 

- [42] H. Head and G. Holmes, “Sensory disturbances from cerebral lesions,” _Brain_ , vol. 34, no. 2–3, pp. 102–254, 1911. 

- [43] M. Hoffmann, H. Marques, A. Arieta, H. Sumioka, M. Lungarella, and R. Pfeifer, “Body schema in robotics: a review,” _IEEE Transactions on Autonomous Mental Development_ , vol. 2, no. 4, pp. 304–324, 2010. 

- [44] K. Kawaharazuka, K. Okada, and M. Inaba, “GeMuCo: Generalized Multisensory Correlational Model for Body Schema Learning,” _IEEE Robotics Automation Magazine_ , vol. 32, no. 2, pp. 80–98, 2024. 

- [45] K. Kawaharazuka, S. Makino, M. Kawamura, A. Fujii, Y. Asano, K. Okada, and M. Inaba, “Online Self-body Image Acquisition Considering Changes in Muscle Routes Caused by Softness of Body Tissue for Tendon-driven Musculoskeletal Humanoids,” in _2018 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2018, pp. 1711–1717. 

- [46] S. Makino, K. Kawaharazuka, M. Kawamura, A. Fujii, T. Makabe, M. Onitsuka, Y. Asano, K. Okada, K. Kawasaki, and M. Inaba, “FiveFingered Hand with Wide Range of Thumb Using Combination of Machined Springs and Variable Stiffness Joints,” in _2018 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2018, pp. 4562–4567. 

- [47] J. Tani, “Self-organization of behavioral primitives as multiple attractor dynamics: a robot experiment,” in _2002 International Joint Conference on Neural Networks_ , 2002, pp. 489–494. 

- [48] K. Kawaharazuka, K. Tsuzuki, M. Onitsuka, Y. Asano, K. Okada, K. Kawasaki, and M. Inaba, “Object Recognition, Dynamic Contact Simulation, Detection, and Control of the Flexible Musculoskeletal Hand Using a Recurrent Neural Network With Parametric Bias,” _IEEE Robotics and Automation Letters_ , vol. 5, no. 3, pp. 4580–4587, 2020. 

- [49] K. Kawaharazuka, A. Miki, M. Bando, K. Okada, and M. Inaba, “Dynamic Cloth Manipulation Considering Variable Stiffness and Material Change Using Deep Predictive Model With Parametric Bias,” _Frontiers in Neurorobotics_ , vol. 16, pp. 1–16, 2022. 

- [50] K. Kawaharazuka, Y. Kawamura, K. Okada, and M. Inaba, “Imitation Learning with Additional Constraints on Motion Style using Parametric Bias,” _IEEE Robotics and Automation Letters_ , vol. 6, no. 3, pp. 5897– 5904, 2021. 

- [51] K. Kawaharazuka, K. Tsuzuki, Y. Koga, Y. Omura, T. Makabe, K. Shinjo, M. Onitsuka, Y. Nagamatsu, Y. Asano, K. Okada, K. Kawasaki, and M. Inaba, “Toward Autonomous Driving by Musculoskeletal Humanoids: Study of Developed Hardware and LearningBased Software,” _IEEE Robotics Automation Magazine_ , vol. 27, no. 3, pp. 84–96, 2020. 

- [52] P. L. Gribble, L. I. Mullin, N. Cothros, and A. Mattar, “Role of cocontraction in arm movement accuracy,” _Journal of neurophysiology_ , vol. 89, no. 5, pp. 2396–2405, 2003. 

- [53] M. B. Wiggin, G. S. Sawicki, and S. H. Collins, “An exoskeleton using controlled energy storage and release to aid ankle propulsion,” in _2011 IEEE International Conference on Rehabilitation Robotics_ , 2011, pp. 1–5. 

