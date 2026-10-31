---
title: "Towards Forceful Robotic Foundation Models: a Literature Survey"
date: "2025-04-16"
authors: "William Xie; Nikolaus Correll"
url: https://arxiv.org/abs/2504.11827
pdf: https://arxiv.org/pdf/2504.11827
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2504.11827)** / [論文ページ](https://arxiv.org/abs/2504.11827)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Towards Forceful Robotic Foundation Models: a Literature Survey** 

**William Xie and Nikolaus Correll**<sup>_∗_</sup> 

**Abstract:** This article reviews contemporary methods for integrating force, including both proprioception and tactile sensing, in robot manipulation policy learning. We conduct a comparative analysis on various approaches for sensing force, data collection, behavior cloning, tactile representation learning, and lowlevel robot control. From our analysis, we articulate when and why forces are needed, and highlight opportunities to improve learning of contact-rich, generalist robot policies on the path toward highly capable touch-based robot foundation models. We generally find that while there are few tasks such as pouring, peg-inhole insertion, and handling delicate objects, the performance of imitation learning models is not at a level of dynamics where force truly matters. Also, force and touch are abstract quantities that can be inferred through a wide range of modalities and are often measured and controlled implicitly. We hope that juxtaposing the different approaches currently in use will help the reader to gain a systemic understanding and help inspire the next generation of robot foundation models. 

## **1 Introduction** 

With the world population in the industrialized part of the world shrinking [1], the need for generalist robotic systems capable of caring for an aging population and filling in gaps in the working population is rapidly growing. Emerging rapidly in response is a new industrial sector that focuses on humanoid robots—robots that can seamlessly integrate into existing workflows due to their humanlike shape and sensor configuration. Concurrently, so-called “robot foundation models” [2, 3, 4, 5, 6] have demonstrated zero-shot autonomy for a series of dexterous manipulation tasks via combining imitation learning with the world knowledge provided by large language models [7]. 

Force and touch are critical modalities for robotic systems that interact in the real world. Being able to control not only the robot’s position, but also the force it exerts on its environment, is critical for manipulating delicate objects [8], human-robot interaction, and contact-rich manipulation for assembly [9]. However, current robot foundation models focus exclusively on visual input and position control. Relying on position alone might not be sufficient to achieve true dexterity, as small errors in position may lead to large errors in force in stiff systems. And because force, the second derivative of position (via Newton’s second law of motion _F_ = _mx_ ¨), represents a richer, higher-frequency representation of motion, focusing only on position may not be sample-efficient or capture high-frequency information during imitation learning. Yet, why and how forces should be employed during learning remains still unclear, in particular, as many of the benefits of force control can be gained using implicit techniques ranging from impedance control to mechanism design. 

In this paper, we review recent efforts to extend end-to-end robot learning to force and touch sensing while situating this work in the larger context of force control and tactile sensing in robotics. Here, we specifically focus on transformer [10] and diffusion-based [11] end-to-end learning methods, which, due to their favorable scaling properties, have the potential to integrate with generalist foundation models. We hypothesize that the next generation of robot foundation models will require force and torque input and output and hope that the synthesis of the existing literature in this survey will contribute to their design. 

> _∗_ 1All authors are with the University of Colorado at Boulder, Boulder, CO. Corresponding email: `wixi6454@colorado.edu` 

We begin this survey with a background on the human sensing apparatus, force control in robotics, and the field of policy learning (Section 2). After providing an overview of the reviewed works by force and timescale (Section 3), we discuss work in forceful end-to-end learning with regard to data collection (Section 4), ways of generating force trajectories (Section 5), and utilizing and scaling representation of force data (Section 6). We conclude with a discussion on the advantages of forceful policies and future directions. 

## **2 Background** 

In this section we provide context for force and touch sensing, the latter of which we use synonymously with tactile sensing, and robot policy learning. We also situate tactile robot policies in the broader field of robot learning and the rise of large scale datasets and robot foundation models. 

### **2.1 Human Tactile Sensing and Proprioception Apparatus** 

We precede this survey with a brief overview of the human tactile and force sensing apparatus. This is important for two reasons: (1) the differentiation of the human sensing system suggests that tactile-based dexterity relies on a data with a wide variety of spatial resolution, bandwidth, and signal dynamics; (2) the impact of specific sensory information on makespan and precision for a variety of manipulation is well understood in humans, thereby possibly informing the design of robotic systems. 

The human tactile sensing system relies on specialized _mechanoreceptors_ located within the skin, each adapted to detect specific types of mechanical stimuli. These mechanoreceptors are categorized into four primary types: Fast-Adapting Type I and II (FA-I and FA-II), and Slowly Adapting Type I and II (SA-I and SA-II). Each type exhibits distinct physiological and functional properties that contribute to the sense of touch. FA-I mechanoreceptors, associated with Meissner corpuscles, are predominantly found in the glabrous (hairless) skin of the fingertips. They respond to lowfrequency vibrations in order of 20–200Hz [12] and dynamic skin deformations, playing a crucial role in detecting textures and slip during object manipulation. Their receptive fields are small and well-defined, allowing for precise spatial resolution [13, 14]. FA-II mechanoreceptors, linked to Pacinian corpuscles, are distributed throughout the hand. These receptors are particularly sensitive to high-frequency vibrations up to 1500Hz [12] and sudden changes in pressure. They contribute to the perception of fine textures and tool use. Unlike FA-I mechanoreceptors, FA-II receptors have large and diffuse receptive fields, enabling them to detect distant vibrations [14, 15]. SA-I mechanoreceptors, associated with Merkel cell-neurite complexes, are concentrated in the fingertips and specialize in detecting sustained pressure and fine spatial details. They are essential for form and texture discrimination due to their small and well-defined receptive fields [13]. SA-II mechanoreceptors, connected to Ruffini endings, are evenly distributed across the glabrous skin of the hand. They are particularly sensitive to skin stretch and sustained pressure, contributing to the perception of hand shape and finger position. Their large and diffuse receptive fields aid in proprioceptive feedback [16]. 

_Proprioception_ refers to the body’s ability to sense its position, movement, and the forces exerted by its limbs and joints without relying on external sensory input (e.g., vision). This sensory feedback is crucial for maintaining posture and executing coordinated, precise movements, such as in dexterous manipulation. Key proprioceptive sensors involved in detecting joint torque and muscle activity are muscle spindles, Golgi tendon organs (GTOs), and joint receptors. Muscle spindles [17] are embedded within muscles and detect changes in muscle length and the rate of stretch. When a muscle is stretched, muscle spindles send signals to the brain to inform it of the muscle’s length and how fast it is changing. This helps the brain adjust muscle activity to prevent overstretching and maintain proper muscle force during movements. Golgi Tendon Organs (GTOs) [18] are found in the tendons. GTOs sense the tension or force exerted by muscles. When the tension exceeds a certain threshold, GTOs inhibit further contraction to prevent muscle damage. This feedback is essential for regulating joint torque during activities that require force precision. Joint Receptors 

2 

[19] are located in the joint capsules and ligaments and detect changes in joint position, movement, and stretch. They provide feedback to the brain about the angle and motion of joints, which is essential for maintaining stable postures and controlled movements. 

Researchers have also studied the impact of the absence of certain sensing modalities. For example, local anesthesia of tactile mechanoreceptors [20] show severe impairement of dexterity, but also demonstrates that the task can eventually be completed using visual feedback and proprioception alone. This is also impressively demonstrated in a video showing a women striking a match with and without local anesthesia numbing the fingers [21]. Regarding proprioception, [19] reports of a case of a young man who was able to relearn muscle control after a neurological disease disabling his proprioception system. 

In robotics, the term proprioception usually refers to joint encoders and torque sensors that are internal to the robot, whereas tactile sensors fall into the category of exteroception, i.e. external to the robot. We note that the transition between force/torque and tactile sensing is quite fluent as these quantities are mechanically linked and that while proprioception is well developed, robotic tactile sensing generally trails human capabilities in terms of information density and the ability to measure shear forces. Here, the main challenges are less the existence of appropriate measures, but integration and manufacturing [22]. 

### **2.2 Force Control** 

In order to better understand the relationship between position and force and its implications for robot policy learning, we briefly review robotic force control [23]. A robot linkage with a Jacobian matrix _J ∈R_<sup>6</sup><sup>_xn_</sup> , the partial derivatives of all of its _n_ joints _q ∈R_<sup>_n_</sup> to the end-effector pose _x ∈R_<sup>6</sup> , can control its end-effector velocity _x_ ˙ via its joint velocity _q_ ˙ using 


We can use the same Jacobian to compute the necessary joint torques _τ ∈R_<sup>_n_</sup> as 


where _F_ is a spatial wrench consisting of three translational forces and three torques around the principal axes [24]. 

If a robot does not provide the ability to control joint torques directly, we can employ impedance control [25] to command a relationship between position and force: 


Here, _x_ ˙ and _x_ ¨, the current velocity and acceleration, are inputs to a _virtual_ spring-mass-damper system computes the force that results from the difference between current pose _x_ and desired pose _xd_ . In other words, if the robot end effector had mass _M_ and was attached to pose _xd_ with a virtual spring and damper, moving it to _x_ would exert the wrench _F_ due to the spring coefficient _K_ (Hooke’s law). Letting the end-effector go would let it snap back in place, oscillating like a real spring given its damping coefficient _D_ . If we ignore mass and damping ( _M_ = 0 _, D_ = 0), we would control only stiffness, also known as _compliance control_ . 

Alternatively, we can solve (3) for _x_ ¨ and integrate the velocity and pose numerically to obtain the necessary displacement to exert force _F_ . This is known as _admittance control_ [26]. As force readings might not be available along all degrees of freedom, thereby preventing closed-loop control around actual force, there exist also hybrid control schemes that control force only along some principal axes and use position control for the other dimensions. 

In the context of policy learning, approaches that learn from poses and implement position or velocity control require implementing a solution to inverting (1) (also known as differential inverse kinematics), whereas controllers that aim at imitating end-effector wrenches will need to provide solutions to invert (2) (inverse dynamics), possibly via the detour of admittance control. With this in mind, some policy learning frameworks also directly record joint-space positions, velocities and 

3 

torques. While this sacrifices transferring policies between robots with different kinematics such as in the Open-X dataset [3] which explicitly records trajectories in relative end-effector coordinates, imitation in joint space is less prone to singularities and numerical problems that arise from inverse kinematics/dynamics and admittance control. 

Policies can also learn impedance control for a variety of contact-rich manipulation tasks in [27, 28, 29, 30], where they help position-based frameworks to generalize better. 

### **2.3 Policy Learning** 

Imitation learning (IL) is a subfield of machine learning where an agent learns to perform tasks by mimicking expert demonstrations. Unlike reinforcement learning (RL), which relies on trial-anderror with a reward signal, IL directly infers the desired behavior from demonstrations and trains a model to match the demonstrations in a least-squares manner. IL is particularly useful in robotics, autonomous driving, and interactive AI applications where defining a reward function is difficult or unsafe. The two primary types of IL are (1) behavior cloning (BC), supervised learning applied to mapping states to expert actions, and (2) inverse reinforcement learning (IRL), learning a reward function that explains expert behavior and then optimizing it using RL [31]. 

While reinforcement learning-based approaches suffer from the curse of dimensionality, which makes many real-world learning problems intractable, BC is effective with comparatively fewer and sparser demonstrations. However, BC is then very brittle during inference in situations that have not been part of the initial training set or are “out-of-distribution”. Techniques like DAgger (Dataset Aggregation) [32] and Guided Policy Search [33] attempt to bridge IL with RL, helping agents recover from errors and improve performance beyond expert capabilities. 

Recent advancements in transformer and diffusion model architectures have reshaped IL, reducing the reliance on RL-based optimization. Models like Decision Transformer (DT) [34] and Trajectory Transformer [35] represent policy learning as a sequence modeling problem that generates actions much like a canonical text-based transformer generates characters. Instead of explicitly optimizing a reward function, these models treat demonstrations as a language-like sequence and generate future actions in an auto-regressive fashion. Unlike the classical formulation of a Markov Decision Problem, in which each state depends only on the previous state, self-attention in transformers [10] enables conditioning upon a large number of previous states, thereby allowing learning agents to discover implicit recovery mechanisms instead of blindly mimicking the expert. 

Diffusion models, originally developed for image generation (e.g., DALL-E 2 [36], Stable Diffusion [37]), have been adapted for IL by learning to denoise suboptimal trajectories into expert-like behaviors. Diffusion [38] applies noise to expert demonstrations and learns to refine them, resulting in smooth, human-like control policies. Here, the diffusion process ensures consistency across the entire trajectory. Diffusion policy [11] outperformed behavior cloning and RL baselines in robotic manipulation tasks by capturing uncertainty in demonstrations. Diffusion policy is a special case of flow-matching [39], which learns a velocity field that transforms a zero mean, variance one normal distribution into a target distribution. In this context, transformers are used to encode sensory data and text commands, which can then guide the diffusion / flow-matching process using feature-wise linear modulation (FiLM) encoding [40]. 

At the same time, the transformer architecture has also revolutionized policy learning by using large language models for code generation. Based on Google’s PalmE model, [41] has demonstrated a new level of open-world reasoning for mobile manipulation by choosing from LLM-generated suggestions for the next best learned policy [42] using learned value functions [43]. In our own work, we have chosen a similar approach to combine the open-world knowledge of an LLM to tune a variety of hand-coded controllers to manipulate delicate objects [8]. While seemingly at odds with action-generating transformers, these two approaches are starting to fuse in Vision Language Action models (VLA) that combine large pre-trained VLMs with transformer- [44] or diffusionbased action heads [45], or even directly generate trajectory end-points from a VLM as in Gemini 

4 

Robotics [6]. VLMs can also be fine-tuned to explicitly reason about the properties of physical objects [8] or spatial concepts [6] to increase their utility during manipulation tasks. 

In this article, we primarily review works which leverage data-driven methods for learning robot motion generation, of which diffusion [11] and transformer [2, 46, 47] based architectures are most common. This area of robot policy learning is often described as _end-to-end robot learning_ , in contrast with approaches which compose modules responsible for planning, vision, and control, as it is a method for learning a direct mapping from raw inputs to robot actions [48], e.g. sensing-totorques. However, end-to-end is a nebulous and often uninformative term, especially as 1) there is a wide performance gap between end-to-end methods which leverage large pretrained models and those which train on limited demonstrations [49] and 2) such methods do not ever capture the full robotics spectrum (nor should they ever be expected to, many will argue), requiring first and last mile help to go from long-horizon planning to precise force control. 

Still, however imperfect, we use the term _robot policies_ to describe the resultant state-action mappings produced from end-to-end (synonymous with data-driven or implicit) learning methods [48]. 

### **2.4 Touch and Force Sensing** 

In robotics, the sense of touch has been incorporated across a spectrum of embodiments, scale, and applications. Within manipulation alone, touch is deployed for grasping, in-hand manipulation and localization, object pose estimation, and object reconstruction [50, 51, 52, 53, 54, 55]. 

The hardware space of tactile robot manipulation is quite heterogeneous, ranging from 1) normal and shear force sensing on end-effector finger-mounted force sensors, 2) force-torque sensing at the wrist joint preceding the end-effector, 3) extrapolation of end-effector external wrenches to joint motor torques, 4) finger-mounted optical sensors (synonymous with visuo-tactile finger sensors) that capture high-resolution contact deformation imaging, 5) finger-mounted magnetometer, piezoelectric, and capacitive sensors that capture similar information as 4) but with lower dimensionality and modality-specific accommodations, and 6) assorted novel sensing methods, such as robot skins [56, 57] and soft actuators [58]. Examples of such signals are shown in Figure 1. 

**Figure 1:** A: Differential tactile data during a sequence of grasping events. Gripper aperture (top row), pressure sensing in the left and right finger tip (2nd row), the derivative of the pressure signal (3rd row), and accelerometer at the wrist (4th row), from [59]. B: Force (top) and torque (bottom) data over time during a successful bearing insertion from [9]. C: High-resolution tactile information from a GelSight sensor from [60]. 

This diversity in sensing is captured by policy learning, with our reviewed works leveraging all mentioned forms of sensing, across different products and robots. These works all demonstrate an intuitive result, which is that conditioning robot policies on force sensing enables robot skills that are otherwise limited, inferior, and/or impossible without touch sensing, such as pouring precise 

5 

volumes from a cup [61, 62], inserting pegs into tight-tolerance holes [63, 64], or grasping fragile and deformable objects [65, 66, 67]. 

**Figure 2:** Touch sensing can be represented across fine-grained fingers to the whole robot arm as forces. 


**(a)** Free body diagram of gripper-object interaction 


**(b)** Common force or touch sensing methods on robot arms include joint torques, wrist force/torque (F/T) sensors, and end effector gripper sensors. Diagram from [68]. 

During grasping, a robot end effector applies an external force on the object, as expressed in Fig. 2a. Assuming sufficient friction, at least two points of contact are needed for to create sufficient constraints on the object. Note, that the drawing shows the end-result of grasping, but contact with the objects and the different fingers of the gripper or hand almost never happen at the same time (see also Figure 1), which creates a strong motivation for tactile sensing [59] to minimize disturbance of an object as individual fingers are placed. 

Once the robot moves, this external wrench propagates through the arm, generating internal wrenches that must be accounted for in the robot’s control. In this view, touch is represented as the forces and torques transmitted through the end effector to the robot, which can be interpreted either as a six-dimensional wrench at the wrist or, by solving the full inverse dynamics, as joint torques across the robot’s degrees of freedom, depicted in Fig. 2b. Beyond grasping, this representation also applies to pushing or pulling an object with the robot end-effector. 

### **2.5 Foundation Models** 

Large-scale robotic datasets [3, 69] have enabled the emergence of generalist, end-to-end robot foundation models [4, 2, 70, 71, 72, 73] which typically combine a vision-language model with a behavior cloning architecture [46, 47, 74, 11] to generate robot policies from a larger representation space. However, these robot foundation models are pre-trained on limited modalities: vision, language, and robot joint and/or end effector data. This includes the most recent Gemini Robotics [6], which has recorded 2000-5000 episodes per task across six tasks and over a time-span of 12 months, but does not include force. 

Recently, we have seen an glut of smaller robot policy models which do capture and condition on tactile feedback, positioned at varying levels of generality and task and problem coverage. Such works have inherited the combinatorial, heterogeneous nature of physical sensing, with each contribution often proposing a unique ensemble of solutions for tactile policy learning. In this review we examine select key questions in this space: 1) how should we collect touch data in robot motion, 2) how should we express robot actions conditioned on touch data, and 3) how do we represent this data in robot policy learning? 

6 

## **3 Review Overview** 

In this section, we describe the review structure of 25 works, which learn tactile robot policies using transformer or diffusion models: [75, 76, 65, 63, 77, 78, 79, 80, 81, 82, 83, 84, 66, 85, 86, 64, 87, 88, 89, 67, 90, 91, 92, 93, 61]. Unlike previous work on end-to-end learning of force-based policies [27, 28, 29, 30], transformer and diffusion-based methods inherit the favorable scaling properties of large language models, making them suitable for training foundation models. 

From these papers, we identify 64 manipulation experiments, corresponding to 59 distinct policies trained and 53 unique tasks (Figure 4). That is, there is neither a consistent challenge application, except perhaps “peg-in-hole” for which five papers provide benchmarks, nor a policy that is capable of dealing with more than a handful of tasks at once. 

We employ multiple lenses with which to analyze these works and their respective tasks, the first of which is to plot the approximate force magnitude from 0.1 to 10N against task length time from 0.1 to 20s (“makespan”), categorized by paper in Fig. 3 and by specific task in Fig. 4. Within these works, we specifically explore their data collection methods in Sec. 4, action spaces in Sec. 5, and representation learning methods in Sec. 6. 

As only seven of the reviewed works (28%) provide force magnitudes for their learned tasks, we have estimated the order of magnitude for the other works. We represent force magnitude in logarithmic bins between 0.1N and 1N (delicate force), 1N to 10N (typical operational force), and greater than 10N (high force). We do an additional rough categorization within these bins based on the specific task. Although some works do not provide measured task length times, we are able to estimate task length from videos provided on project websites or presentations in such cases. Separating tasks between short and long duration ( _≤_ or _>_ than five seconds), we find that 4 tasks (6%) are short ( _≤_ 5s) and apply high forces ( _≥_ 10N), 14 (22%) are short and apply typical forces (1N to 10N), 11 (17%) are short and apply delicate forces (0.1N to 1N), 6 are long ( _>_ 5s) and apply delicate forces, 25 (40%) are long and apply typical forces, and 4 (6%) are long and apply high forces. 

It is possible to construct similar taxonomies categorized by touch sensor type, data collection method, policy learning architecture, dataset size, or policy action space. However, due to the high visual density of such resulting plots, in future sections we narrow our focus on the distribution of unique papers across a single category (e.g. what is the distribution of touch sensor type across the 25 works). 

We provide a full reference table for the 25 works and corresponding 64 tasks containing information, when available, on approximate force magnitude, task length time, general touch sensor type, specific touch sensor, policy action frequency, dataset size (per-task), action space of policygenerated actions, data collection method, low-level robot controller, policy learning architecture, and miscellaneous notes (typically relating to data representation) via this online spreadsheet (link). 

## **4 Data Collection** 

A fundamental challenge in policy learning is data collection of high-quality robot trajectories, which is predominantly accomplished by a human “demonstrating” how to do a specific task. Training a robot foundation model, e.g. a very large robot policy capable of many tasks across diverse environments and configurations, requires a proportionally very large amount of this high-quality robot data, typically characterized as a scaling law in machine learning [7, 49]. Tactile robot policy learning particularly adds difficulty to this scaling law. In a field where sensing varies significantly across platforms, data collection methods necessarily also vary, and thus it is difficult to amass the requisite amount of robot data for a tactile robot foundation model. In this section we discuss this first problem of extracting touch sensing for robot motion data, examining how reviewed works design data collection methods to capture touch sensing for their specific tasks and reduce the human-robot embodiment gap in demonstrations. 

7 


**Figure 3:** We plot force magnitude against task length time for 64 tasks (of which 53 are unique) across 25 papers implementing tactile robot policies. 

### **4.1 Sensor modalities** 

The first single-category lens we look at is general touch sensor type, shown in Fig. 5. We categorize touch sensing across six categories: audio, force, or optical (visuotactile) sensing at the end effector “fingers”, joint torque sensing from the robot arm joints (“whole arm”), combined sensing from the end effector and joint torques, and wrist F/T sensing. Visuotactile sensors at the finger are entirely constituted of GelSight-type [94] sensors, accounting for the plurality of sensing (36% of papers). The GelSight-type sensors measure touch by observing the deformation of a flexible polymer using a camera. Sensing is otherwise diverse, with the other methods constituting two (finger audio and combined arm and finger sensing) to four (finger force, whole arm, and wrist F/T) papers each. 

In total, 14 unique sensor products are used, including the single category of GelSight-family sensors [63, 80, 82, 87, 88, 90, 91, 92, 61]. Joint torque sensing across whole robot arms is accomplished via off-the-shelf sensing from the Franka Panda robot arm [75, 66, 86, 89] or Flexiv Rizon arm [84], or from motor current sensing on custom robot arms [81]. Wrist F/T sensing can be done also with the Franka Panda arm or with three other dedicated wrist sensors: the UR5E sensor [76], OptoForce sensor [77, 93], and the ATI Mini 45 sensor [78]. For finger audio sensing both surface microphones [83, 85] and normal microphones [80] are used. For finger force sensing, motor current corresponding to contact normal force [66, 67], CoinFT sensors [65], and uncalibrated force-like quantities like magnetic-field sensing [64], and pressure-sensing [79] are used. 

8 


**Figure 4:** On the same force-time axes, we describe the 64 tasks learned by the 25 papers, with 53 unique tasks. 


**Figure 5:** Across the reviewed papers, we categorize touch or tactile sensors across six categories: audio, force, or optical (visuotactile) sensing at the end effector “fingers,” joint torque sensing along the whole robot arm, combined sensing from the end effector and joint torques, and wrist F/T sensing. 

9 


**Figure 6:** We categorize data collection into five methods: 1) human video demonstration methods, 2) kinesthetic teaching, which entails directly teaching the physical, human forces to perform a task, 3) reinforcement learning methods which do not require demonstration data, 4) augmented methods of teleoperation including haptic feedback for the operator, handheld grippers detached from a robot arm, and force-matching leaderfollower arm systems, typically with ALOHA-like systems [47], and 5) teleoperation. 

### **4.2 Teleoperation** 

_Teleoperation_ , whereby an expert operator uses a joystick, potentially with a VR headset [76, 80, 85, 64, 88], keyboard and other miscellaneous computer devices [63, 61], or via a smaller robot arm in a leader-follower setup [79, 90], to control the robot, accounts for the plurality of works (36%), Figure 6. 

### **4.3 Kinesthetic Teaching** 

The embodiment gap between human operators and robotic systems arises because robots experience forces differently from humans, both in magnitude and in the way forces are applied and sensed. Kinesthetic teaching mitigates this discrepancy, allowing operators to directly impart forces onto the robot by physically guiding it through a task. Kinesthetic teaching entails directly teaching the physical, human forces to perform a task [75, 65, 78, 91, 92]. Hou et al. place two UR5E robots in free-drive mode with gravity compensation, allowing them to move freely while being guided by a human operator, a common approach in kinesthetic teaching [78]. The human demonstrator then grabs specially designed handles mounted on the robots’ wrists, reminiscent of bimanual exoskeleton control, and demonstrates two high force magnitude tasks: cleaning a vase with sponge end-effectors and pivoting an object about a rigid surface with a rod end-effector. Ablett et al., in comparison, demonstrate more typical forces and move a Franka Panda arm to open a cabinet door, recording external forces via the arm’s joint torques [75]. Finally, Zhao et al. use kinesthetic teaching to do precise, low-force capacitor insertion on a printed circuit board, recording forces indirectly with the GelSight Wedge sensor [92]. 

In these works, the operator directly perceives forces through the robot’s arm, and the robot’s sensors, ranging from finger, wrist, and whole arm sensing, capture the imparted human forces, ranging from low, typical, and high forces. This method provides rich force interaction data representative of the nuanced compliance strategies at play in tasks that involve external contact forces. Unlike teleoperation, which relies on indirect control interfaces, kinesthetic teaching enables the robot to record internal and external wrenches (i.e., forces and torques applied by the human through both the robot and the environment) in a manner more representative of real-world forceful interactions. 

Kinesthetic teaching can also be accomplished by recording forces from a human demonstrator using finger-mounted sensors. Two works explore directly attaching a GelSight Mini [91] or CoinFT (finger F/T sensor) [65] to a human demonstrator’s hand as they perform pinch grasps and singlefinger motions, effectively demonstrating the forces to be emulated on a parallel-jaw robot gripper. This design enables direct and intuitive demonstration of contact-rich manipulation skills, such as 

10 

precise peg insertion [91], object reorientation, articulated grasping of earphone cases and enclosed batteries, and non-prehensile sliding [65]. 

Several issues pervade kinesthetic teaching, however: it is physically demanding, potentially timeintensive, and risks damaging fragile robotic sensors or actuators if mishandled, thus requiring skilled human demonstrators, of which there is often scarce supply. 

### **4.4 Augmented, Bilateral Teleoperation** 

A middle ground between kinesthetic teaching and teleoperation is bilateral control, or augmented teleoperation, which incorporates haptic or force feedback from the robot in teleoperation. In these setups, forces sensed by the robot are mirrored back to the human operator, enabling closed-loop interaction, using force-matching leader-follower arm systems [81, 66], haptic feedback joystick devices [93, 87], or with hand-held robot grippers equipped with touch sensing intended to emulate a robot end-effector [83, 84]. Some works additionally mix robot demonstration data with human demonstration data [88, 91], or teleoperated robot data with handheld gripper data [83]. In total, these alternative methods for teleoperation account for 56% of the reviewed works, though they come at the cost of additional required expertise and system design. 

The magnitude of force feedback from bilateral teleoperation can be scaled to help operators develop an intuitive feel for the task dynamics without exerting the true, full forces required to complete the task. Compared to kinesthetic teaching, bilateral control reduces the physical burden on the human while maintaining some degree of force awareness. However, bilateral control systems are highly engineered and often task-specific. The feedback provided to the operator is not a direct measurement of either human-applied forces or robot-experienced forces, but rather a processed signal reflecting robot interaction forces. 

Designing effective feedback mechanisms is nontrivial. Researchers have explored a variety of techniques, ranging from vibration-based hand feedback [93] to leader-follower robotic arms that attempt joint torque transfer without unduly burdening the operator [66, 81]. Xue et al. propose force-field visualizations, mapping interaction forces into a graphical display rather than physical feedback [95]. In constructing such systems, these works often near the complexity of kinesthetic teaching, demanding substantial hardware equipment and expertise, making data collection still expensive and difficult to scale. 

Handheld robot grippers are promising alternatives that simplify the data collection process while preserving force fidelity. This method removes the robot arm from the touch-sensing feedback loop entirely, focusing on force interactions at the end-effector. The assumption undergirding these devices is that force sensing at the wrist and gripper is the relevant signal for many manipulation tasks. Given this, researchers have developed portable force-sensing grippers equipped with F/T sensors and wrist-mounted cameras for direct data collection by human demonstrators [84, 96, 97]. 

Handheld grippers offer several key advantages: 1) direct force measurement; unlike bilateral control, these devices capture human-applied forces at the end effector without additional signal processing, 2) reduced complexity and cost; they eliminate the need for full robotic systems, lowering the barrier to collecting high-quality force-interaction data, and directly related to the prior advantage, 3) improved scalability; these tools are easier to use, vastly more portable, and require less expertise than kinesthetic teaching or leader-follower methods. 

Recent work has also explored diverse designs for handheld force-sensing grippers. Liu et al. integrates contact microphones at the fingertips of the handheld UMI gripper [98] to approximate force feedback via audio signals [83]. This approach enables highly sensitive tactile tasks, such as distinguishing surface textures (e.g., hook and loop tape surface identification), by learning the acoustic properties of frictional contact. Though these compact, specialized touch-sensing devices present practical and scalable alternatives for data collection in tactile robot policy learning, by disregarding the robot arm in demonstrations, future work should take care in performing high-force magnitude 

11 

tasks. When learning to generate correspondingly forceful actions at the end-effector, dangerous joint space trajectories may be enacted by the robot. 


**Figure 7:** The large majority of papers (76%) of papers train their policies on under 200 demonstrations. The exceptions collect large amounts of data either in simulation (Drake) [88] or via high-manpower data collection efforts [80]. 

### **4.5 Data requirements for forceful policies** 

Of the reviewed papers, the overwhelming majority (76%) train on fewer than 200 demonstrations, shown in Fig. 7. This reflects the broader challenge of collecting large-scale, high-quality force interaction datasets across heterogeneous robot platforms and suggests that, as no clearly superior sensing or data collection method has emerged, it may be premature to scale data collection. However, two outlier works train policies on datasets exceeding 2,000 [80, 88] episodes. 

The first such work from Jones et al. trains a policy, FuSe, on 26,866 tactile trajectories collected enmasse via VR headset teleoperation on Widow X robots outfitted with GelSight DIGIT sensors and microphone audio sensing at the fingers, in addition to language instruction, wrist camera vision, and third person camera vision [80]. This dataset is by an order of magnitude the largest real-world robot dataset with touch sensing. The resulting trained policy is able to distinguish textural and auditory features, generalizing to grasping new objects with novel and varying touch properties. However, while the large dataset of multimodal data enabled the trained policy to semantically reason about and classify objects based on their tactile properties, the policy learned primarily to grasp objects and press buttons (two distinct tasks) conditioned on this knowledge. With teleoperation, scaling up to skillful and nuanced manipulation tasks presents significant challenges, requiring proportionally greater manpower, time, and expertise. 

Wang et al. propose an alternative approach to scaling data collection without human data collection altogether, instead training policies primarily on 50,000 contact-rich, continuous tool-usage skills obtained in simulation (Drake), leveraging simulated GelSight sensing [88, 99]. A policy trained on simulation data combined with 400 real robot demonstrations exhibits better generalization to novel objects, distractors, and configurations as a result of domain and configuration randomization deployed in simulation. However, the simulated tasks are significantly abstracted; for example, in the hammer usage task, the demonstrated dynamics are not representative of practical usage. Simulation remains an underexplored domain for learning high-quality tactile robot policies, but perhaps the underlying condition of a simulator capable of accurately modeling dynamic, frictional, and large-magnitude forces has not been met yet. 

12 

We argue that it is never premature to scale data collection, if provided ample means to do so. Such efforts yield insights into model training and data representation distinct from works which are devoted to data collection method design and train on smaller datasets. Also, even if additional modalities are required later, such data might still be relevant to initialize a model with curriculum learning. 


**Figure 8:** A large (64%) majority of learned policies output robot actions in Cartesian space position control. Outside of this method of control, low level control is split across joint space control and various forms of force control. 

## **5 Action Space** 

While in the previous section we described a wide array of data collection methods, due to the primary underlying method being teleoperation in Cartesian space, a similarly large majority of learned policies (64%) output robot actions in Cartesian position space for a low-level robot position controller. Low level control is otherwise split across joint space control and various forms of force control–admittance [78, 93], impedance [75, 65, 86, 89], compliance control [76], and other custom control schemes [81, 84]). In this section we discuss how low-level force control can be formulated from human demonstrations, what benefits it yields, and whether it is necessary at all. 

It is perhaps misleading to dichotomize policies by low-level control. After all, if a position-control policy learns robot motion conditioned on force feedback, then it itself is a model-free, implicit force-position controller, albeit highly specialized for the learned task [66, 77]. With the concrete disadvantages of requiring more complex control schemes and potentially processing demonstration data to force-controllable inputs, explicit low-level force control’s concrete advantages are then: 1) performance, as such controllers run at high frequencies that enable reactivity and consistency beyond human capability, which are often further gimped by wide embodiment gaps in demonstration, 2) interpretability, in that force controllers accept low-dimension motion objectives or parameters that can be explicitly commanded, anticipated, and intuitively understood (e.g. maintaining a commanded scalar compliance parameter), and 3) dimension reduction in policy learning, in that learning motion parameters rather than direct robot motion offloads the complexity of force control from the policy to the controller. 

### **5.1 Explicit Force Control** 

It is still possible to generate force controllable actions even if robot demonstrations operate in Cartesian space. When such demonstrations are collected with force data, one can formulate and reconstruct force-controllable actions to be trained on. Revisiting Hou et al. [78], their trained Adaptive Compliance Policy performs the vase-wiping task and quasistatic flipping task by mapping human-demonstrated forces to high-frequency (500 Hz) admittance controller inputs. To briefly 

13 

revisit 2.2, such a force control scheme governs robot motion as a mass-spring-damper system, taking control inputs of a virtual target pose and stiffness matrix in response to external forces. 

To achieve this, Hou et al. design a post-processing method to reshape wrist force sensing (ATI Mini F/T wrist sensor) and end-effector position data from kinesthetic teaching demonstrations to admittance controller inputs, in order to train a policy able to command variable compliance across different contact modes and disturbances. Hou et al. formulate a post-facto stiffness matrix control input with the heuristic of allowing low stiffness (high compliance) in the direction of the force feedback and high stiffness otherwise. This low stiffness value is scaled by sensed force magnitude. Then, they project a virtual target position from position data in demonstrations along the sensed wrist forces and scaled by the computed stiffness. Additionally, a 1-second moving average filter is applied to demonstrated wrist wrenches to generate future-contact-informed stiffness inputs, which subsequently produce smooth, contact-engaging virtual target trajectories. Finally, the tactile robot policy is trained to predict a virtual target and stiffness value, in addition to true end-effector pose. As a result, the policy maintains appropriate compliance throughout unseen perturbations (jostling) and geometries (vases and objects to pivot). Compared to ablated policies which do not learn variable compliance and use a uniformly high- or low-stiffness controller, closer to position control, absolute success rate drops by 81% for the same tasks. 

Other works follow a similar implementation of reconstructing force-informed trajectories postdemonstration. Chen et al. [65] use fingertip F/T sensing and Ablett et al. map low-dimension deformation signals from a pressure-based finger tactile sensor to forces [75]. These works utilize finger sensing rather than wrist F/T data in order to decouple wrist wrenches, which are inextricable from human-applied wrenches if demonstrated with kinesthetic teaching, from the precise forces experienced at the fingers, before generating virtual targets with tuned stiffness components for impedance control. These approaches require careful model design and tuning of forceful action representation, but enable large success rate improvements and robust compliant behaviors for tasks like reorienting objects, opening doors, and manipulating other kinds of articulated objects compared to ablated methods without force input and force-informed virtual targets. 

Zhou et al. also leverage admittance control but directly predict future contact forces while adjusting to real-time contact forces, rather than predicting stiffness control parameters to generate future force-informed virtual targets [93]. The trained tactile policy performs tasks such as grasping, cabinet and door opening, dry-erase board drawing and erasing and demonstrate improved success, a 17% reduction in task completion time over a policy trained without force feedback, and a 26% reduction in task completion time over teleoperated methods without force control. 

Control schemes such as dually tracking orthogonal pose and force targets [84], predicting real, non-virtual poses and stiffness parameters for an underlying compliance controller to resolve into target joint positions [76], or simply commanding to a grasping force, rather than gripper position or closure [67] are also employed. Trained policies from [84, 76] demonstrate task performance on mortar-and-pestle grinding and zucchini peeling close to human expert time efficiency (1.3x) and three times faster than teleoperated methods (4.5x). 

Noseworthy et al. [86] generate actions as Cartesian space virtual targets for low-level impedance control, but do not train on stiffness or force targets. Instead, the trained policy learns the inherent impedance control law from contact forces provided in the observation. In order to generalize across a range of contact forces, they simulate impedance control and Franka Panda robot dynamics with randomized scaling and damping parameters, spanning commandable forces between 6 and 20N. Ablated policies trained without force input and thus doing solely position control were less successful, took longer to complete, and exerted larger ground-truth forces on the same tasks. 

Wu et al. train a policy to directly output high-frequency target external wrenches between 50 to 500 Hz, which are initially collected from pre-programmed behavior-tree guided peg insertion demonstrations [89]. They additionally implement dynamic filtering to interpolate from the policy action generation frequency to a low-level impedance controller at 1000 Hz. These trained policies execute precise ( _<_ 0.5mm tolerance) peg insertion, on average, in under two seconds and above 90% 

14 

success rate, where similar tactile robot policies generating position control actions to do less-precise peg insertion require typically at least double the time [63, 82, 91]. 


**Figure 9:** Looking at the behavior or policy learning architectures utilized by the reviewed papers, the majority (52%) train their policies with a diffusion architecture backbone [11]. Five papers (20%) use transformer architectures, with three of those using the action-chunking transformer introduced by [47]. Multilayer perceptron architectures (16%) are still relevant for action generation due to low quantities of data. 

## **6 Policy Learning** 

As policy learning is the natural bottleneck between sensory inputs and robot actions, the reviewed works implement various approaches to reduce dimensionality in tactile robot policies. In this section we discuss selection of behavior cloning architecture in policy learning and the differences between representing force data and visuotactile data for policy learning. 

### **6.1 Behavior Cloning** 

The majority of reviewed works (52%) train their policies with a diffusion architecture backbone [11], shown in Fig. 9. Five papers (20%) use transformer architectures, with three of those using the action-chunking transformer (ACT) [47]. Multilayer perceptron architectures (MLP) are still leveraged by some works (16%) as they can learn behavior cloning with low quantities of data. 

Diffusion policies have gained traction primarily due to their ease of training and their ability to balance sample efficiency with the capacity to model complex, multimodal robot behaviors by capturing the stochastic nature of human demonstrations. Unlike transformers, which often require large datasets to generalize effectively, or small MLPs, which struggle with intricate tasks and mode collapse, diffusion policies offer a middle ground. Diffusion does suffer some drawbacks, such as overfitting to absolute robot states and reducing generalization to other spatial configurations. Removing robot states from the observation and instead leveraging relative, instead of absolute, position actions improves this issue [71, 80], allowing tactile diffusion policies to learn from more relevant sensing. 

ACT [47] address a different challenge in policy learning: long-horizon reasoning and efficient action execution. By structuring actions into temporally coherent chunks, ACT reduce the burden of high-frequency action prediction while maintaining smooth and stable control. This is especially useful in tactile robot tasks requiring extended, coordinated motion sequences. The chunking mechanism allows the transformer to learn meaningful action segments, effectively bridging the gap between low-level motor commands and high-level task objectives. 

15 

While behavior cloning architectures have converged toward effective paradigms, another challenging aspect of policy learning lies in tactile representation learning, as in capturing salient tactile features in learnable, lower-dimension features. 

### **6.2 Visuotactile Representation Learning** 

Of the 14 unique sensors employed in the reviewed works, tactile representation learning research largely focuses on one: GelSight-type sensors which capture high-resolution surface deformation images, making them powerful tools for visuotactile learning. 

For instance, Jones et al. [80] fine-tune a TVL encoder [100]. pretrained on 44,000 vision-touchlanguage samples, to represent visuotactile sensing from a GelSight DIGIT sensor. This encoder, built on a vision transformer (ViT) [101], integrates annotated vision, language, and touch data from various GelSight sensors, mapping visuotactile data to semantic features like texture, force, and object category. The TVL encoder leverages vision-language pretraining (VLP), where large-scale multimodal datasets enhance representation learning. By aligning visuotactile signals with semantic and visual concepts, the latent representations of tactile data enable a richer understanding of contact interactions. In comparison, Xu et al. design a representation which can learn from a single object and sensor to reconstruct visual deformation of novel objects and from other GelSight-type sensors [90]. Zhao et al. [92] propose a tactile encoder for directly learning downstream tasks such as classification, force estimation, and pose estimation from representations of visuotactile data from different GelSight-type sensors. 

Despite the inherent challenges of working with visuotactile data from GelSight-type sensing, such sensors are more accessible than force-sensing methods, which require specific robot arms such as the Franka Panda or comparatively expensive wrist F/T sensors. As a result, research ecosystem surrounding these sensors continues to grow, continually improving learning from visuotactile inputs. 

Pattabiraman et al. leverage a single magnometer-based finger sensor (AnySkin [102]), which provides neither optical deformation nor force data [64]. However, the measured sensor produces data similar in dimension to force data, as it is equipped with five 3-axis magnetometers, totalling a 15-dimensional sensor reading. This data allows easier representation learning, as low-dimensional signals across objects ease estimation of contact events and contact magnitude. As such, the sensor data is encoded with just two fully-connected layers. The sensor provides uncalibrated force-like quantities (magnetic force fields) that capture contact shear and normal forces more directly than visual deformation, which enables learning continuous, precise tasks such as credit card swiping, tipping over and grasping a book off a shelf, and plug insertion from the lightweight data representation. Huang et al. learn from pressure sensing at the finger, which also provides neither force nor optical data [79]. However, they take an alternative approach and project tactile sensing and depth camera vision to a shared 3D, point-cloud representation to improve bi-manual, in-hand manipulation. 

### **6.3 Force Representation Learning** 

Force representation learning is less explored and oftentimes more straightforward. Force data is low-dimensional and explicitly, causally linked to motion. Unlike image data, force measurements are interpretable in their raw forms, can be encoded often directly without modification [75, 76, 65, 86, 81, 89, 67], with minor gravity compensation [84], with a fast Fourier transform to encode highfrequency force data as a 2D spectrogram [78], or with an MLP [66, 77, 93] into the observation space, and still yield effective tactile robot policies that appropriately act on force inputs. 

When the objective is to map sensor data to physical sensations, force data fundamentally provides a more direct and interpretable signal than visuotactile sensing, presenting promise for long-horizon and physically intricate tasks. While current research primarily applies force data to relatively short tasks such as grasping or pouring, its compact representation may help reasoning about prolonged and complex contact interactions, where visuotactile data may prove unwieldy or obfuscating. 

16 

Some works already condition on force to either select or modulate modes of action. He et al. postprocess ground-truth future contact state from RGB images and whether contact force exceeds a manually-selected threshold value to train a contact predictor [77]. This predictor then supervises a weighted prediction loss summed with the behavior cloning loss, which enables the policy to attend to force appropriately during and outside of contact. They additionally implement a reactive positon controller that conditions again on force to set more aggressive goal positions if insufficient F/T is detected during contact. Both the contact-supervised loss and force-conditioned reactive control enable better coverage and consistency in tasks like dry-erase board wiping, cucumber peeling, and pepper chopping. 

Liu et al. [84] similarly learn to switch between free-space position control and force control conditioned on force feedback, and Noseworthy et al. [86] learn to terminate a skill at either a specified or learned threshold. Outside of force data, Liu et al. (audio) [83], Mejia et al. (audio) [85], Feng et al. (optical and audio) [63], and Li et al. (optical and audio) [61] utilize multisensory self-attention to learn cross-modality, cross-time, and cross-modality-time relationships. This self-attention mechanism enables learning of adaptive weights for features at different task stages for action generation, resulting in greater task success and interpretability. 

### **6.4 Scaling Multimodal Reasoning** 

While the trained FuSe policy in Jones et al. [80] is largely limited to grasping, as discussed in 2.5, it is also the only tactile robot policy thus far which finetunes a pretrained “robot foundation model” backbone (Octo [71]). It is the pairing of the large, multimodal collected data and this pretrained Octo policy which enable complex, generalizable reasoning about tactile properties, which we expand upon here. 

As Octo is pretrained on a comparatively much larger dataset (OXE data [3]), Jones et al. identify that fine-tuning such a large pretrained model on novel tactile modalities with a “naive” meansquared error (MSE) behavior cloning loss results in over-reliance on pre-training modalities such as camera vision and robot position data. Thus, Jones et al. design two multimodal losses which address this issue, using language, e.g. a task instruction such as “pick up the squishy object”, as the “glue” across modalities. Each collected trajectory can have multiple task instructions: picking up a button can potentially alternate as one of picking up a (hard, metallic, red, circular) object. 

The first loss term is a contrastive loss to maximize mutual information between different modalities and semantics of the same scene. First, they construct an observation embedding from passing all modalities through the pre-trained Octo transformer and a multi-head attention layer. They compute a contrastive loss between each possible task instruction with this embedding and obtain an average _Lcontrast_ . 

The second loss term is a generative loss to learn high-level semantics for each possible combination of modalities, for which they build an embedding via the same process as above. Then, the embedding is passed through a generative head and a generative loss _Lgen_ is computed between the head output and ground truth language. During training, these auxiliary terms are summed to the MSE loss. Jones et al. show these multimodal losses enable compositional reasoning about tasks such as “pick the object that has the same color as the button that plays piano.” 

The trained FuSe policy leverages tactile sensing and multimodal reasoning for discrete tasks like the given example, centered around classifying perceived objects or selecting objects whose predicted tactile properties correspond to a task instruction. Future works which incorporate force sensing, in addition to the visuotactile and audio finger sensing leveraged here, may be able to train tactile robot policies capable of both discrete and continuous tasks. The original Octo policy was also adapted for precise peg-insertion via fine-tuning on a small dataset of 100 demonstrations with wrist F/T sensing, showing downstream adaptability of their foundation model [71], but no work has fully explored first-class large force pretraining for a tactile robot foundation model which can perform high-level (semantic reasoning) and low-level (reactive control) decision making for contact-rich, forceful tasks. 

17 

## **7 Discussion: Towards Tactile Robot Foundation Models** 

In this article we reviewed 25 state-of-the-art works which train tactile robot policies mapping tactile sensing to robot actions in order to complete various contact-rich, forceful tasks. First, we explored the large space of data collection methods, highlighting methods which reduced the human-robot embodiment gap in sensing touch and issues related to scaling collection, human demonstrations, and system design (Sec. 4). Then, we described the action space of tactile robot policies, drawing a line between position control and various force control methods, highlighting that low-level force control helped to bridge the human-robot embodiment gap and enabled fundamental physical skills (Sec. 5). Finally, we discussed representation learning methods for force and visuotactile data, as well as methods for multimodal reasoning about touch in complex, multi-part tasks, highlighting opportunities to leverage force in large scale pretraining for discrete and continuous decision-making (Sec. 6). These research areas each present highly relevant problems to overcome in order to build tactile robot foundation models and domestic robots which are suitably capable, safe, and versatile for human care. 

_On whether explicit force representations are needed:_ The elephant in the room is whether explicit representations for force are actually needed or not. From a physiology perspective, there is evidence that neither tactile sensing or proprioception are strictly needed to implement dexterity and controlled motion. We argue that this kind of functional replacement simply demonstrates the large degree of redundancy that supports the human sensory-motor system, but should not be used to construe an argument that vision alone is sufficient for reliably functioning at high performance. 

From a controls perspective, impedance control does provide a pathway in which force can be actively controlled, yet does not need to be implicitly presented as an input to a foundation model. Impedance control is a low-level functionality of many robotic arms, and many contact-rich tasks might be solved by simply inferring appropriate mass, spring and damping parameters from task context and otherwise rely on position control. Here, impedance control is not limited to joint-torque sensors, but can include tactile sensing at the finger tips. Yet, impedance control might only be a subset of the various ways that end-effectors, including individual fingers, should react to external forces, and explicit representations of force might still be necessary for state representation. 

From a mechanical design perspective, sensing touch is not necessary for complex in-hand manipulation [103]. Yet, sensing and impedance control is often implicit in soft mechanisms, and geometry and material choice are all critical in the open loop policies of [103] to succeed. In [104], basic impedance control is used to perform a variety of complex in-hand manipulation tasks, forgoing exact position control, a principle the authors refer to as implicit touch sensing. However, this method is not fully versatile, particularly for fine-grained manipulation tasks, and the authors propose future work to include actual touch sensing. 

_On compositional vs. end-to-end policies:_ Throughout this article, we have implicitly presumed that improving tactile robot policies learned end-to-end will eventually progress to generalist humanoid robots, while conceding and showing that for many of the reviewed works, the bounds of either “end” varied. One could potentially argue that policies which produce force controller parameters, rather than exact robot motions, are not fully end-to-end and rather compositional methods. Commercially, Physical Intelligence’s _π_ 0 [5], Figure AI’s Helix [105], and Google DeepMind’s Gemini Robotics [6] robot foundation models all leverage compositional control, in which a low-frequency model perceives the world and decomposes high-level task instructions into atomic skills for a highfrequency model to ingest and generate low-level control for. Other works explore even greater decomposition, leveraging large pretrained models to do step-by-step reasoning about object detection, picking appropriate grasp locations, judging the physical feasibility of actions, and determining appropriate modes of control [72, 106, 107]. These compositional approaches, though complementary with tactile robot policies, suggest that robot foundation models can be functionally equivalent to several smaller and specialized policies. 

By each focusing only on a few distinct tasks, tactile policies lag behind recent large robot models in generalizability across tasks, scenes, embodiments, and objects. This in part due to the nature of 

18 

contact-rich manipulation which necessitate tactile sensing and often simply cannot be captured by the action vocabulary of such models. Additionally, the relative paucity and heterogeneity of tactile robot data currently precludes traditional large model pretraining techniques. Such issues are not mere engineering obstacles. They are representative of the fundamental phenomenon of physical sensing, which is combinatorial in input, processing, and output. 

The large variety of forces and task completion times spanning two orders of magnitude and resulting diversity in sensing modalities make it tempting to treat examples at the extreme ends of the spectrum as distinct problems. This is misleading, however, as reliable and efficient execution of these tasks might indeed require operation across the full spectrum. For example, dispensing accurate quantities from a jug of liquid will require precise force measurement across a large spectrum. Similarly, manipulation of delicate objects requires both high-level planning (in the orders of seconds) and high-frequency feedback control. Furthermore, in the interest of generalist platforms such as humanoids, foundation models will likely need to cover the entire spectrum of bandwidth in sensing, actuation, and control. 

_On scaling data collection:_ There is no superlative method to collect forceful robot interaction data. Yet with contact-rich, tactile tasks being difficult to simulate with high fidelity, real-world data collection remains essential. Kinesthetic teaching, bilateral control, and handheld grippers improve upon teleoperation and each offer distinct trade-offs in terms of data fidelity, scalability, and human effort. Data collection of tactile robot data is an active research problem, and the research community remains in an exploratory phase where developing new, practical data collection methods is as important as refining existing methods. 

While the current paradigm of data collection leans heavily on human demonstrations, history suggests that major breakthroughs in learning arise when we eliminate human bottlenecks, such as unsupervised learning of next-token prediction from large text corpora in natural language processing (NLP) [7]. As research progresses, the next leap may come not from refining human-driven data collection, but from unlocking scalable, automated methods that reduce dependency on human effort altogether. 

TacDiffusion learns precise peg insertion from pre-designed behavior tree controlled trajectories which do require expert design [89]. Xie et al. [67] learn delicate grasp policies also from a predesigned adaptive grasp controller, but leverages LLM-supervision to parameterize the force controller, enabling automated versatility and generalizability across objects [8], which follows a new proposed paradigm of distilling large (vision) language model guided robot trajectories into smaller robot policy models [108]. 

Regardless of which method one chooses, the priority should be producing as much high-quality data as possible. This data leads to richer learning signals, better performing models, and ultimately, convergence toward effective tactile policy learning paradigms. 

## **8 Conclusion** 

Imbuing transformer and diffusion-based end-to-end learning models with the ability to sense and generate forces is a recent trend, which builds up on a long history of force control in robotics. Adding force either as an input, an output, or both shows consistent improvements in makespan and robustness. While consistent with human physiology where tactile sensing and proprioception greatly improves dexterity, this also demonstrates that neither sense is critical and can be compensated by other modalities. The latter fact is motivation enough for pursuing force-less policies, particularly in development of minimalist, affordable robots which may be adequate for a subset of applications. 

An intermediate solution between actively employing force sensing is the use of impedance control. Here, force control is only implicitly represented in a higher level controller, thereby reducing the data requirements during training. As impedance control is the computational equivalent of a mechanical spring and damper, it can also implemented as such, for example using soft, compliant 

19 

actuators, also known as “soft robotics”, or combinations of computational and mechanical compliance. Impressively demonstrated by biological systems, this mixed approach occupies a niche in robotics [109] and is little explored in the context of robot learning. 

Only few of the works emphasize the saliency of tactile information, which can provide lowdimensional and even binary information on critical events such as contact. With even contactrich tasks like in-hand manipulation being achieved via open-loop control or double-digit absolute improvements on benchmark tasks such as cloth-folding being achieved by model architecture improvements, we believe that the community has not really begun exploring highly dynamic tasks that cannot be solved without tactile sensing. We posit that tackling these tasks will require improving our understanding on representing forces and lead to models that are more data-efficient, cognizant of the physical world, and thus scalable and suitable for widespread adoption. 

## **References** 

- [1] United Nations, Department of Economic and Social Affairs, Population Division. World population prospects: Probabilistic projections - total population, 2024. URL `https://population.un.org/wpp/graphs?loc=906&type=Probabilistic% 20Projections&category=Population&subcategory=1_Total%20Population` . Accessed: 2025-02-22. 

- [2] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, J. Dabis, C. Finn, K. Gopalakrishnan, K. Hausman, A. Herzog, J. Hsu, J. Ibarz, B. Ichter, A. Irpan, T. Jackson, S. Jesmonth, N. J. Joshi, R. Julian, D. Kalashnikov, Y. Kuang, I. Leal, K.-H. Lee, S. Levine, Y. Lu, U. Malla, D. Manjunath, I. Mordatch, O. Nachum, C. Parada, J. Peralta, E. Perez, K. Pertsch, J. Quiambao, K. Rao, M. Ryoo, G. Salazar, P. Sanketi, K. Sayed, J. Singh, S. Sontakke, A. Stone, C. Tan, H. Tran, V. Vanhoucke, S. Vega, Q. Vuong, F. Xia, T. Xiao, P. Xu, S. Xu, T. Yu, and B. Zitkovich. Rt-1: Robotics transformer for real-world control at scale, 2023. URL `https://arxiv.org/abs/2212.06817` . 

- [3] O. X.-E. Collaboration, A. O’Neill, A. Rehman, A. Gupta, A. Maddukuri, A. Gupta, A. Padalkar, A. Lee, A. Pooley, A. Gupta, A. Mandlekar, A. Jain, A. Tung, A. Bewley, A. Herzog, A. Irpan, A. Khazatsky, A. Rai, A. Gupta, A. Wang, A. Kolobov, A. Singh, A. Garg, A. Kembhavi, A. Xie, A. Brohan, A. Raffin, A. Sharma, A. Yavary, A. Jain, A. Balakrishna, A. Wahid, B. Burgess-Limerick, B. Kim, B. Sch¨olkopf, B. Wulfe, B. Ichter, C. Lu, C. Xu, C. Le, C. Finn, C. Wang, C. Xu, C. Chi, C. Huang, C. Chan, C. Agia, C. Pan, C. Fu, C. Devin, D. Xu, D. Morton, D. Driess, D. Chen, D. Pathak, D. Shah, D. B¨uchler, D. Jayaraman, D. Kalashnikov, D. Sadigh, E. Johns, E. Foster, F. Liu, F. Ceola, F. Xia, F. Zhao, F. V. Frujeri, F. Stulp, G. Zhou, G. S. Sukhatme, G. Salhotra, G. Yan, G. Feng, G. Schiavi, G. Berseth, G. Kahn, G. Yang, G. Wang, H. Su, H.-S. Fang, H. Shi, H. Bao, H. B. Amor, H. I. Christensen, H. Furuta, H. Bharadhwaj, H. Walke, H. Fang, H. Ha, I. Mordatch, I. Radosavovic, I. Leal, J. Liang, J. Abou-Chakra, J. Kim, J. Drake, J. Peters, J. Schneider, J. Hsu, J. Vakil, J. Bohg, J. Bingham, J. Wu, J. Gao, J. Hu, J. Wu, J. Wu, J. Sun, J. Luo, J. Gu, J. Tan, J. Oh, J. Wu, J. Lu, J. Yang, J. Malik, J. Silv´erio, J. Hejna, J. Booher, J. Tompson, J. Yang, J. Salvador, J. J. Lim, J. Han, K. Wang, K. Rao, K. Pertsch, K. Hausman, K. Go, K. Gopalakrishnan, K. Goldberg, K. Byrne, K. Oslund, K. Kawaharazuka, K. Black, K. Lin, K. Zhang, K. Ehsani, K. Lekkala, K. Ellis, K. Rana, K. Srinivasan, K. Fang, K. P. Singh, K.-H. Zeng, K. Hatch, K. Hsu, L. Itti, L. Y. Chen, L. Pinto, L. Fei-Fei, L. Tan, L. J. Fan, L. Ott, L. Lee, L. Weihs, M. Chen, M. Lepert, M. Memmel, M. Tomizuka, M. Itkina, M. G. Castro, M. Spero, M. Du, M. Ahn, M. C. Yip, M. Zhang, M. Ding, M. Heo, M. K. Srirama, M. Sharma, M. J. Kim, N. Kanazawa, N. Hansen, N. Heess, N. J. Joshi, N. Suenderhauf, N. Liu, N. D. Palo, N. M. M. Shafiullah, O. Mees, O. Kroemer, O. Bastani, P. R. Sanketi, P. T. Miller, P. Yin, P. Wohlhart, P. Xu, P. D. Fagan, P. Mitrano, P. Sermanet, P. Abbeel, P. Sundaresan, Q. Chen, Q. Vuong, R. Rafailov, R. Tian, R. Doshi, R. Mart’in-Mart’in, R. Baijal, R. Scalise, R. Hendrix, R. Lin, R. Qian, R. Zhang, R. Mendonca, R. Shah, R. Hoque, R. Julian, S. Bustamante, S. Kirmani, S. Levine, S. Lin, S. Moore, S. Bahl, S. Dass, S. Sonawani, 

20 

   - S. Tulsiani, S. Song, S. Xu, S. Haldar, S. Karamcheti, S. Adebola, S. Guist, S. Nasiriany, S. Schaal, S. Welker, S. Tian, S. Ramamoorthy, S. Dasari, S. Belkhale, S. Park, S. Nair, S. Mirchandani, T. Osa, T. Gupta, T. Harada, T. Matsushima, T. Xiao, T. Kollar, T. Yu, T. Ding, T. Davchev, T. Z. Zhao, T. Armstrong, T. Darrell, T. Chung, V. Jain, V. Kumar, V. Vanhoucke, W. Zhan, W. Zhou, W. Burgard, X. Chen, X. Chen, X. Wang, X. Zhu, X. Geng, X. Liu, X. Liangwei, X. Li, Y. Pang, Y. Lu, Y. J. Ma, Y. Kim, Y. Chebotar, Y. Zhou, Y. Zhu, Y. Wu, Y. Xu, Y. Wang, Y. Bisk, Y. Dou, Y. Cho, Y. Lee, Y. Cui, Y. Cao, Y.-H. Wu, Y. Tang, Y. Zhu, Y. Zhang, Y. Jiang, Y. Li, Y. Li, Y. Iwasawa, Y. Matsuo, Z. Ma, Z. Xu, Z. J. Cui, Z. Zhang, Z. Fu, and Z. Lin. Open X-Embodiment: Robotic learning datasets and RT-X models. `https://arxiv.org/abs/2310.08864` , 2023. 

- [4] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi, Q. Vuong, T. Kollar, B. Burchfiel, R. Tedrake, D. Sadigh, S. Levine, P. Liang, and C. Finn. Openvla: An open-source vision-language-action model, 2024. URL `https://arxiv.org/abs/2406.09246` . 

- [5] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter, S. Jakubczak, T. Jones, L. Ke, S. Levine, A. Li-Bell, M. Mothukuri, S. Nair, K. Pertsch, L. X. Shi, J. Tanner, Q. Vuong, A. Walling, H. Wang, and U. Zhilinsky. Pi0: Our first generalist policy. 

- [6] G. D. Gemini Robotics Team. Gemini robotics: Bringing ai into the physical world, 2025. URL `https://storage.googleapis.com/deepmind-media/ gemini-robotics/gemini_robotics_report.pdf` . 

- [7] T. Brown, B. Mann, N. Ryder, M. Subbiah, J. Kaplan, P. Dhariwal, A. Neelakantan, P. Shyam, G. Sastry, A. Askell, S. Agarwal, A. Herbert-Voss, G. Krueger, T. Henighan, R. Child, A. Ramesh, D. Ziegler, J. Wu, C. Winter, C. Hesse, M. Chen, E. Sigler, M. Litwin, S. Gray, B. Chess, J. Clark, C. Berner, S. McCandlish, A. Radford, I. Sutskever, and D. Amodei. Language models are few-shot learners. _Advances in Neural Information Processing Systems (NeurIPS)_ , 2020. URL `https://arxiv.org/abs/2005.14165` . 

- [8] W. Xie, M. Valentini, J. Lavering, and N. Correll. Deligrasp: Inferring object properties with llms for adaptive grasp policies. In _Proceedings of The 8th Conference on Robot Learning_ , pages 1290–1309. PMLR, 2024. URL `https://proceedings.mlr.press/v270/ xie25a.html` . 

- [9] J. Watson, A. Miller, and N. Correll. Autonomous industrial assembly using force, torque, and rgb-d sensing. _Advanced Robotics_ , 34(7-8):546–559, 2020. 

- [10] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser, and I. Polosukhin. Attention is all you need. _Advances in neural information processing systems_ , 30, 2017. 

- [11] C. Chi, S. Feng, Y. Du, Z. Xu, E. Cousineau, B. Burchfiel, and S. Song. Diffusion policy: Visuomotor policy learning via action diffusion. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2023. URL `https://arxiv.org/abs/2311.01248` . 

- [12] J. M. Wolfe and A. Iggo. Sensory receptors, cutaneous. _Sensory Systems: II: Senses Other than Vision_ , pages 109–110, 1988. 

- [13] R. S. Johansson and A. B. Vallbo.<sup>˚</sup> Tactile sensory coding in the glabrous skin of the human hand. _Trends in neurosciences_ , 6:27–32, 1983. 

- [14] K. O. Johnson. The roles and functions of cutaneous mechanoreceptors. _Current opinion in neurobiology_ , 11(4):455–461, 2001. 

- [15] V. B. Mountcastle. _The sensory hand: neural mechanisms of somatic sensation_ . Harvard University Press, 2005. 

21 

- [16] A. B. Vallbo, R. S. Johansson, et al. Properties of cutaneous mechanoreceptors in the human hand related to touch sensation. _Hum neurobiol_ , 3(1):3–14, 1984. 

- [17] R. W. Banks, P. H. Ellaway, A. Prochazka, and U. Proske. Secondary endings of muscle spindles: Structure, reflex action, role in motor control and proprioception. _Experimental Physiology_ , 106(12):2339–2366, 2021. 

- [18] L. Jami. Golgi tendon organs in mammalian skeletal muscle: functional properties and central actions. _Physiological reviews_ , 72(3):623–666, 1992. 

- [19] J. C. Tuthill and E. Azim. Proprioception. _Current Biology_ , 28(5):R194–R203, 2018. 

- [20] R. S. Johansson and G. Westling. Roles of glabrous skin receptors and sensorimotor memory in automatic control of precision grip when lifting rougher or more slippery objects. _Experimental brain research_ , 56(3):550–564, 1984. 

- [21] R. Johansson. Proprioception and motor control, 2025. URL `https://www.youtube.com/ watch?v=0LfJ3M3Kn80` . Accessed: 2025-03-26. 

- [22] M. A. McEvoy and N. Correll. Materials that couple sensing, actuation, computation, and communication. _Science_ , 347(6228):1261689, 2015. 

- [23] B. Siciliano and L. Villani. _Robot force control_ . Springer Science & Business Media, 1999. 

- [24] N. Correll, B. Hayes, C. Heckman, and A. Roncone. _Introduction to autonomous robots: mechanisms, sensors, actuators, and algorithms_ . MIT Press, 2022. 

- [25] N. Hogan. Impedance control: An approach to manipulation: Part ii—implementation. 1985. 

- [26] A. Q. Keemink, H. Van der Kooij, and A. H. Stienen. Admittance control for physical human– robot interaction. _The International Journal of Robotics Research_ , 37(11):1421–1444, 2018. 

- [27] J. Buchli, F. Stulp, E. Theodorou, and S. Schaal. Learning variable impedance control. _The International Journal of Robotics Research_ , 30(7):820–833, 2011. 

- [28] F. J. Abu-Dakka and M. Saveriano. Variable impedance control and learning—a review. _Frontiers in Robotics and AI_ , 7:590681, 2020. 

- [29] X. Zhang, L. Sun, Z. Kuang, and M. Tomizuka. Learning variable impedance control via inverse reinforcement learning for force-related tasks. _IEEE Robotics and Automation Letters_ , 6(2):2225–2232, 2021. 

- [30] S. Park, S. Jo, and S. Lee. Lstm-based imitation learning of robot manipulator using impedance control. _Journal of Institute of Control, Robotics and Systems_ , 29(2):107–112, 2023. 

- [31] A. Y. Ng, S. Russell, et al. Algorithms for inverse reinforcement learning. In _Icml_ , volume 1, page 2, 2000. 

- [32] S. Ross, G. Gordon, and D. Bagnell. A reduction of imitation learning and structured prediction to no-regret online learning. In _Proceedings of the fourteenth international conference on artificial intelligence and statistics_ , pages 627–635. JMLR Workshop and Conference Proceedings, 2011. 

- [33] S. Levine and V. Koltun. Guided policy search. In _International conference on machine learning_ , pages 1–9. PMLR, 2013. 

- [34] L. Chen, K. Lu, A. Rajeswaran, K. Lee, A. Grover, M. Laskin, P. Abbeel, A. Srinivas, and I. Mordatch. Decision transformer: Reinforcement learning via sequence modeling. _Advances in neural information processing systems_ , 34:15084–15097, 2021. 

22 

- [35] M. Janner, Q. Li, and S. Levine. Offline reinforcement learning as one big sequence modeling problem. _Advances in neural information processing systems_ , 34:1273–1286, 2021. 

- [36] A. Ramesh, P. Dhariwal, A. Nichol, C. Chu, and M. Chen. Hierarchical text-conditional image generation with clip latents. _arXiv preprint arXiv:2204.06125_ , 1(2):3, 2022. 

- [37] R. Rombach, A. Blattmann, D. Lorenz, P. Esser, and B. Ommer. High-resolution image synthesis with latent diffusion models. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 10684–10695, 2022. 

- [38] M. Janner, Y. Du, J. B. Tenenbaum, and S. Levine. Planning with diffusion for flexible behavior synthesis. _arXiv preprint arXiv:2205.09991_ , 2022. 

- [39] Y. Lipman, R. T. Chen, H. Ben-Hamu, M. Nickel, and M. Le. Flow matching for generative modeling. _arXiv preprint arXiv:2210.02747_ , 2022. 

- [40] E. Perez, F. Strub, H. De Vries, V. Dumoulin, and A. Courville. Film: Visual reasoning with a general conditioning layer. In _Proceedings of the AAAI conference on artificial intelligence_ , volume 32, 2018. 

- [41] M. Ahn, A. Brohan, N. Brown, Y. Chebotar, O. Cortes, B. David, C. Finn, C. Fu, K. Gopalakrishnan, K. Hausman, et al. Do as i can, not as i say: Grounding language in robotic affordances. _arXiv preprint arXiv:2204.01691_ , 2022. 

- [42] E. Jang, A. Irpan, M. Khansari, D. Kappler, F. Ebert, C. Lynch, S. Levine, and C. Finn. Bc-z: Zero-shot task generalization with robotic imitation learning. In _Conference on Robot Learning_ , pages 991–1002. PMLR, 2022. 

- [43] D. Kalashnikov, J. Varley, Y. Chebotar, B. Swanson, R. Jonschkowski, C. Finn, S. Levine, and K. Hausman. Mt-opt: Continuous multi-task robotic reinforcement learning at scale. _arXiv preprint arXiv:2104.08212_ , 2021. 

- [44] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- [45] J. Wen, Y. Zhu, J. Li, M. Zhu, Z. Tang, K. Wu, Z. Xu, N. Liu, R. Cheng, C. Shen, et al. Tinyvla: Towards fast, data-efficient vision-language-action models for robotic manipulation. _IEEE Robotics and Automation Letters_ , 2025. 

- [46] N. M. M. Shafiullah, Z. J. Cui, A. Altanzaya, and L. Pinto. Behavior transformers: Cloning _k_ modes with one stone, 2022. URL `https://arxiv.org/abs/2206.11251` . 

- [47] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn. Learning fine-grained bimanual manipulation with low-cost hardware, 2023. URL `https://arxiv.org/abs/2304.13705` . 

- [48] K. E. Bekris, J. Doerr, P. Meng, and S. Tangirala. The State of Robot Motion Generation, Dec. 2024. URL `http://arxiv.org/abs/2410.12172` . arXiv:2410.12172 [cs]. 

- [49] F. Lin, Y. Hu, P. Sheng, C. Wen, J. You, and Y. Gao. Data scaling laws in imitation learning for robotic manipulation, 2025. URL `https://arxiv.org/abs/2410.18647` . 

- [50] R. D. Howe. Tactile sensing and control of robotic manipulation. _Advanced Robotics_ , 8 (3):245–261, 1993. doi:10.1163/156855394X00356. URL `https://doi.org/10.1163/ 156855394X00356` . 

- [51] R. S. Dahiya, G. Metta, M. Valle, and G. Sandini. Tactile Sensing—From Humans to Humanoids. _IEEE Transactions on Robotics_ , 26(1):1–20, Feb. 2010. ISSN 1941-0468. doi:10. 1109/TRO.2009.2033627. URL `https://ieeexplore.ieee.org/document/5339133/ ?arnumber=5339133&tag=1` . Conference Name: IEEE Transactions on Robotics. 

23 

- [52] A. Yamaguchi and C. G. Atkeson. Recent progress in tactile sensing and sensors for robotic manipulation: can we turn tactile sensing into vision? _Advanced Robotics_ , 33(14):661– 673, July 2019. ISSN 0169-1864, 1568-5535. doi:10.1080/01691864.2019.1632222. URL `https://www.tandfonline.com/doi/full/10.1080/01691864.2019.1632222` . 

- [53] M. Suomalainen, Y. Karayiannidis, and V. Kyrki. A Survey of Robot Manipulation in Contact. _Robotics and Autonomous Systems_ , 156:104224, Oct. 2022. ISSN 09218890. doi:10.1016/j. robot.2022.104224. URL `http://arxiv.org/abs/2112.01942` . arXiv:2112.01942 [cs]. 

- [54] R. M. Bhirangi. _Tactile sensing for Robot Learning: Development to Deployment_ . PhD Thesis, Carnegie Mellon University, 2024. URL `https://kilthub.cmu.edu/ndownloader/ files/49565013` . 

- [55] T. Li, Y. Yan, C. Yu, J. An, Y. Wang, and G. Chen. A comprehensive review of robot intelligent grasping based on tactile perception. _Robotics and Computer-Integrated Manufacturing_ , 90: 102792, Dec. 2024. ISSN 0736-5845. doi:10.1016/j.rcim.2024.102792. URL `https:// www.sciencedirect.com/science/article/pii/S0736584524000796` . 

- [56] D. Hughes and N. Correll. Texture recognition and localization in amorphous robotic skin. _Bioinspiration & biomimetics_ , 10(5):055002, 2015. 

- [57] D. Hughes, J. Lammie, and N. Correll. A robotic skin for collision avoidance and affective touch recognition. _IEEE Robotics and Automation Letters_ , 3(3):1386–1393, 2018. 

- [58] P. Polygerinos, N. Correll, S. A. Morin, B. Mosadegh, C. D. Onal, K. Petersen, M. Cianchetti, M. T. Tolley, and R. F. Shepherd. Soft robotics: Review of fluid-driven intrinsically soft devices; manufacturing, sensing, control, and applications in human-robot interaction. _Advanced engineering materials_ , 19(12):1700016, 2017. 

- [59] R. Patel, J. C. Alastuey, and N. Correll. Improving grasp performance using in-hand proximity and dynamic tactile sensing. In _2016 International Symposium on Experimental Robotics_ , pages 185–194. Springer, 2017. 

- [60] R. Calandra, A. Owens, M. Upadhyaya, W. Yuan, J. Lin, E. H. Adelson, and S. Levine. The feeling of success: Does touch sensing help predict grasp outcomes? _arXiv preprint arXiv:1710.05512_ , 2017. 

- [61] H. Li, Y. Zhang, J. Zhu, S. Wang, M. A. Lee, H. Xu, E. Adelson, L. Fei-Fei, R. Gao, and J. Wu. See, hear, and feel: Smart sensory fusion for robotic manipulation, 2022. URL `https://arxiv.org/abs/2212.03858` . 

- [62] M. A. Lee, Y. Zhu, K. Srinivasan, P. Shah, S. Savarese, L. Fei-Fei, A. Garg, and J. Bohg. Making Sense of Vision and Touch: Self-Supervised Learning of Multimodal Representations for Contact-Rich Tasks, Mar. 2019. URL `http://arxiv.org/abs/1810.10191` . arXiv:1810.10191 [cs]. 

- [63] R. Feng, D. Hu, W. Ma, and X. Li. Play to the Score: Stage-Guided Dynamic Multi-Sensory Fusion for Robotic Manipulation, Oct. 2024. URL `http://arxiv.org/abs/2408.01366` . arXiv:2408.01366 [cs]. 

- [64] V. Pattabiraman, Y. Cao, S. Haldar, L. Pinto, and R. Bhirangi. Learning Precise, ContactRich Manipulation through Uncalibrated Tactile Skins, Oct. 2024. URL `http://arxiv. org/abs/2410.17246` . arXiv:2410.17246. 

- [65] C. Chen, Z. Yu, H. Choi, M. Cutkosky, and J. Bohg. Dexforce: Extracting force-informed actions from kinesthetic demonstrations for dexterous manipulation, 2025. URL `https: //arxiv.org/abs/2501.10356` . 

24 

- [66] J. J. Liu, Y. Li, K. Shaw, T. Tao, R. Salakhutdinov, and D. Pathak. Factr: Force-attending curriculum training for contact-rich policy learning, 2025. URL `https://arxiv.org/abs/ 2502.17432` . 

- [67] W. Xie, S. Caldararu, and N. Correll. Just add force for delicate robot policies. In _CoRL 2024 Workshop on Mastering Robot Manipulation in a World of Abundant Data_ , 2024. URL `https://openreview.net/pdf?id=GSEs7MCnoi` . 

- [68] R. Robotics. Force and torque sensors – why are they of interest in robotics?, 2023. URL `https://reachrobotics.com/blog/ force-and-torque-ft-why-are-they-of-interest-in-robotics/` . 

- [69] A. Khazatsky, K. Pertsch, S. Nair, A. Balakrishna, S. Dasari, S. Karamcheti, S. Nasiriany, M. K. Srirama, L. Y. Chen, K. Ellis, P. D. Fagan, J. Hejna, M. Itkina, M. Lepert, Y. J. Ma, P. T. Miller, J. Wu, S. Belkhale, S. Dass, H. Ha, A. Jain, A. Lee, Y. Lee, M. Memmel, S. Park, I. Radosavovic, K. Wang, A. Zhan, K. Black, C. Chi, K. B. Hatch, S. Lin, J. Lu, J. Mercat, A. Rehman, P. R. Sanketi, A. Sharma, C. Simpson, Q. Vuong, H. R. Walke, B. Wulfe, T. Xiao, J. H. Yang, A. Yavary, T. Z. Zhao, C. Agia, R. Baijal, M. G. Castro, D. Chen, Q. Chen, T. Chung, J. Drake, E. P. Foster, J. Gao, D. A. Herrera, M. Heo, K. Hsu, J. Hu, D. Jackson, C. Le, Y. Li, K. Lin, R. Lin, Z. Ma, A. Maddukuri, S. Mirchandani, D. Morton, T. Nguyen, A. O’Neill, R. Scalise, D. Seale, V. Son, S. Tian, E. Tran, A. E. Wang, Y. Wu, A. Xie, J. Yang, P. Yin, Y. Zhang, O. Bastani, G. Berseth, J. Bohg, K. Goldberg, A. Gupta, A. Gupta, D. Jayaraman, J. J. Lim, J. Malik, R. Mart´ın-Mart´ın, S. Ramamoorthy, D. Sadigh, S. Song, J. Wu, M. C. Yip, Y. Zhu, T. Kollar, S. Levine, and C. Finn. Droid: A large-scale in-the-wild robot manipulation dataset. 2024. 

- [70] A. Majumdar, K. Yadav, S. Arnaud, Y. J. Ma, C. Chen, S. Silwal, A. Jain, V.-P. Berges, P. Abbeel, J. Malik, D. Batra, Y. Lin, O. Maksymets, A. Rajeswaran, and F. Meier. Where are we in the search for an artificial visual cortex for embodied intelligence?, 2024. URL `https://arxiv.org/abs/2303.18240` . 

- [71] Octo Model Team, D. Ghosh, H. Walke, K. Pertsch, K. Black, O. Mees, S. Dasari, J. Hejna, C. Xu, J. Luo, T. Kreiman, Y. Tan, L. Y. Chen, P. Sanketi, Q. Vuong, T. Xiao, D. Sadigh, C. Finn, and S. Levine. Octo: An open-source generalist robot policy. In _Proceedings of Robotics: Science and Systems_ , Delft, Netherlands, 2024. 

- [72] M. Zawalski, W. Chen, K. Pertsch, O. Mees, C. Finn, and S. Levine. Robotic control via embodied chain-of-thought reasoning, 2024. URL `https://arxiv.org/abs/2407.08693` . 

- [73] J. Wen, Y. Zhu, J. Li, M. Zhu, K. Wu, Z. Xu, N. Liu, R. Cheng, C. Shen, Y. Peng, F. Feng, and J. Tang. Tinyvla: Towards fast, data-efficient vision-language-action models for robotic manipulation, 2024. URL `https://arxiv.org/abs/2409.12514` . 

- [74] S. Lee, Y. Wang, H. Etukuru, H. J. Kim, N. M. M. Shafiullah, and L. Pinto. Behavior generation with latent actions, 2024. URL `https://arxiv.org/abs/2403.03181` . 

- [75] T. Ablett, O. Limoyo, A. Sigal, A. Jilani, J. Kelly, K. Siddiqi, F. Hogan, and G. Dudek. Multimodal and Force-Matched Imitation Learning with a See-Through Visuotactile Sensor, Dec. 2024. URL `http://arxiv.org/abs/2311.01248` . arXiv:2311.01248 [cs]. 

- [76] M. Aburub, C. C. Beltran-Hernandez, T. Kamijo, and M. Hamaya. Learning Diffusion Policies from Demonstrations For Compliant Contact-rich Manipulation, Oct. 2024. URL `http://arxiv.org/abs/2410.19235` . arXiv:2410.19235 [cs]. 

- [77] Z. He, H. Fang, J. Chen, H.-S. Fang, and C. Lu. FoAR: Force-Aware Reactive Policy for Contact-Rich Robotic Manipulation, Nov. 2024. URL `http://arxiv.org/abs/2411. 15753` . arXiv:2411.15753 [cs] version: 1. 

25 

- [78] Y. Hou, Z. Liu, C. Chi, E. Cousineau, N. Kuppuswamy, S. Feng, B. Burchfiel, and S. Song. Adaptive compliance policy: Learning approximate compliance for diffusion guided control, 2024. URL `https://arxiv.org/abs/2410.09309` . 

- [79] B. Huang, Y. Wang, X. Yang, Y. Luo, and Y. Li. 3D-ViTac: Learning Fine-Grained Manipulation with Visuo-Tactile Sensing. Sept. 2024. URL `https://openreview.net/forum? id=bk28WlkqZn` . 

- [80] J. Jones, O. Mees, C. Sferrazza, K. Stachowicz, P. Abbeel, and S. Levine. Beyond Sight: Finetuning Generalist Robot Policies with Heterogeneous Sensors via Language Grounding, Jan. 2025. URL `http://arxiv.org/abs/2501.04693` . arXiv:2501.04693 [cs]. 

- [81] M. Kobayashi, T. Buamanee, and T. Kobayashi. ALPHA and Bi-ACT Are All You Need: Importance of Position and Force Information/Control for Imitation Learning of Unimanual and Bimanual Robotic Manipulation with Low-Cost System, Dec. 2024. URL `http:// arxiv.org/abs/2411.09942` . arXiv:2411.09942 [cs]. 

- [82] J. Lenz, T. Gruner, D. Palenicek, T. Schneider, and J. Peters. Analysing the Interplay of Vision and Touch for Dexterous Insertion Tasks, Oct. 2024. URL `http://arxiv.org/abs/2410. 23860` . arXiv:2410.23860 [cs]. 

- [83] Z. Liu, C. Chi, E. Cousineau, N. Kuppuswamy, B. Burchfiel, and S. Song. Maniwav: Learning robot manipulation from in-the-wild audio-visual data, 2024. URL `https://arxiv.org/ abs/2406.19464` . 

- [84] W. Liu, J. Wang, Y. Wang, W. Wang, and C. Lu. ForceMimic: Force-Centric Imitation Learning with Force-Motion Capture System for Contact-Rich Manipulation, Oct. 2024. URL `http://arxiv.org/abs/2410.07554` . arXiv:2410.07554 [cs]. 

- [85] J. Mejia, V. Dean, T. Hellebrekers, and A. Gupta. Hearing Touch: Audio-Visual Pretraining for Contact-Rich Manipulation, May 2024. URL `http://arxiv.org/abs/2405.08576` . arXiv:2405.08576 [cs]. 

- [86] M. Noseworthy, B. Tang, B. Wen, A. Handa, N. Roy, D. Fox, F. Ramos, Y. Narang, and I. Akinola. FORGE: Force-Guided Exploration for Robust Contact-Rich Manipulation under Uncertainty, Aug. 2024. URL `http://arxiv.org/abs/2408.04587` . arXiv:2408.04587 [cs]. 

- [87] B. Romero, H.-S. Fang, P. Agrawal, and E. Adelson. EyeSight Hand: Design of a FullyActuated Dexterous Robot Hand with Integrated Vision-Based Tactile Sensors and Compliant Actuation, Aug. 2024. URL `http://arxiv.org/abs/2408.06265` . arXiv:2408.06265 [cs]. 

- [88] L. Wang, J. Zhao, Y. Du, E. H. Adelson, and R. Tedrake. Poco: Policy composition from and for heterogeneous robot learning, 2024. URL `https://arxiv.org/abs/2402.02511` . 

- [89] Y. Wu, Z. Chen, F. Wu, L. Chen, L. Zhang, Z. Bing, A. Swikir, A. Knoll, and S. Haddadin. TacDiffusion: Force-domain Diffusion Policy for Precise Tactile Manipulation, Sept. 2024. URL `http://arxiv.org/abs/2409.11047` . arXiv:2409.11047 [cs]. 

- [90] Z. Xu, R. Uppuluri, X. Zhang, C. Fitch, P. G. Crandall, W. Shou, D. Wang, and Y. She. UniT: Unified Tactile Representation for Robot Learning, Aug. 2024. URL `http://arxiv.org/ abs/2408.06481` . arXiv:2408.06481 [cs]. 

- [91] K. Yu, Y. Han, Q. Wang, V. Saxena, D. Xu, and Y. Zhao. MimicTouch: Leveraging Multimodal Human Tactile Demonstrations for Contact-rich Manipulation, Sept. 2024. URL `http://arxiv.org/abs/2310.16917` . arXiv:2310.16917 [cs]. 

26 

- [92] J. Zhao, Y. Ma, L. Wang, and E. H. Adelson. Transferable Tactile Transformers for Representation Learning Across Diverse Sensors and Tasks, Oct. 2024. URL `http://arxiv.org/ abs/2406.13640` . arXiv:2406.13640. 

- [93] B. Zhou, R. Jiao, Y. Li, X. Yuan, F. Fang, and S. Li. Admittance Visuomotor Policy Learning for General-Purpose Contact-Rich Manipulations, Nov. 2024. URL `http://arxiv.org/ abs/2409.14440` . arXiv:2409.14440 [cs]. 

- [94] W. Yuan, S. Dong, and E. H. Adelson. Gelsight: High-resolution robot tactile sensors for estimating geometry and force. _Sensors_ , 17(12):2762, 2017. 

- [95] H. Xue, J. Ren, W. Chen, G. Zhang, Y. Fang, G. Gu, H. Xu, and C. Lu. Reactive diffusion policy: Slow-fast visual-tactile policy learning for contact-rich manipulation, 2025. URL `https://arxiv.org/abs/2503.02881` . 

- [96] Y. Zou, J. Huang, B. Liang, H. Guo, Z. Liu, X. Ma, J. Zhou, and M. Tomizuka. Few-shot sim2real based on high fidelity rendering with force feedback teleoperation, 2025. URL `https://arxiv.org/abs/2503.01301` . 

- [97] M. Hagenow, D. Kontogiorgos, Y. Wang, and J. Shah. Versatile Demonstration Interface: Toward More Flexible Robot Demonstration Collection, Oct. 2024. URL `http://arxiv. org/abs/2410.19141` . arXiv:2410.19141 [cs]. 

- [98] C. Chi, Z. Xu, C. Pan, E. Cousineau, B. Burchfiel, S. Feng, R. Tedrake, and S. Song. Universal manipulation interface: In-the-wild robot teaching without in-the-wild robots, 2024. URL `https://arxiv.org/abs/2402.10329` . 

- [99] L. Wang, K. Zhang, A. Zhou, M. Simchowitz, and R. Tedrake. Robot fleet learning via policy merging, 2024. URL `https://arxiv.org/abs/2310.01362` . 

- [100] L. Fu, G. Datta, H. Huang, W. C.-H. Panitch, J. Drake, J. Ortiz, M. Mukadam, M. Lambeta, R. Calandra, and K. Goldberg. A Touch, Vision, and Language Dataset for Multimodal Alignment. URL `https://tactile-vlm.github.io/` . 

- [101] A. Dosovitskiy, L. Beyer, A. Kolesnikov, D. Weissenborn, X. Zhai, T. Unterthiner, M. Dehghani, M. Minderer, G. Heigold, S. Gelly, J. Uszkoreit, and N. Houlsby. An image is worth 16x16 words: Transformers for image recognition at scale, 2021. URL `https: //arxiv.org/abs/2010.11929` . 

- [102] R. Bhirangi, V. Pattabiraman, E. Erciyes, Y. Cao, T. Hellebrekers, and L. Pinto. Anyskin: Plug-and-play skin sensing for robotic touch, 2024. URL `https://arxiv.org/abs/2409. 08276` . 

- [103] A. Bhatt, A. Sieler, S. Puhlmann, and O. Brock. Surprisingly robust in-hand manipulation: An empirical study. _arXiv preprint arXiv:2201.11503_ , 2022. 

- [104] Z.-H. Yin, C. Wang, L. Pineda, F. Hogan, K. Bodduluri, A. Sharma, P. Lancaster, I. Prasad, M. Kalakrishnan, J. Malik, et al. Dexteritygen: Foundation controller for unprecedented dexterity. _arXiv preprint arXiv:2502.04307_ , 2025. 

- [105] F. AI. Helix: A vision-language-action model for generalist humanoid control, 2025. URL `https://www.figure.ai/news/helix` . 

- [106] T. Wei, L. Ma, R. Chen, W. Zhao, and C. Liu. Meta-control: Automatic model-based control synthesis for heterogeneous robot skills. In _8th Annual Conference on Robot Learning_ , 2024. URL `https://openreview.net/forum?id=cvVEkS5yij` . 

- [107] J. Clark, S. Mirchandani, D. Sadigh, and S. Belkhale. Action-free reasoning for policy generalization. In _https://arxiv.org/abs/2403.01823_ , 2025. 

27 

- [108] H. Ha, P. Florence, and S. Song. Scaling up and distilling down: Language-guided robot skill acquisition, 2023. URL `https://arxiv.org/abs/2307.14535` . 

- [109] Y. Meng¨uc¸, N. Correll, R. Kramer, and J. Paik. Will robots be bodies with brains or brains with bodies? _Science robotics_ , 2(12):eaar4527, 2017. 

28 

