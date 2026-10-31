---
title: "Towards Shared Embodied Intelligence in Humanoid Robots through Optimization Development and Testing of the Human Aware ergoCub Robot"
date: "2026-05-26"
authors: "Carlotta Sartore; Mohamed Elobaid; Lorenzo Rapetti; Giulio Romualdi; Stefano Dafarra; Nicola A. Piga"
url: https://arxiv.org/abs/2605.26991
pdf: https://arxiv.org/pdf/2605.26991
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2605.26991)** / [論文ページ](https://arxiv.org/abs/2605.26991)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# Towards Shared Embodied Intelligence in Humanoid Robots through Optimization Development and Testing of the Human-Aware ergoCub Robot 

Carlotta Sartore<sup>1,2,3*</sup> , Mohamed Elobaid<sup>2</sup> , Lorenzo Rapetti<sup>1,2</sup> , Giulio Romuladi<sup>1,2</sup> , Stefano Dafarra<sup>1,2</sup> , Nicola A. Piga<sup>4</sup> , Ines Sorrentino<sup>1,2,3</sup> , Paolo Maria Viceconte<sup>1,2</sup> , Silvio Traversaro<sup>1,2</sup> , Ugo Pattacini<sup>5</sup> , Luca Fiorio<sup>1,5</sup> , Francesco Draicchio<sup>6</sup> , Giovanna Tranfo<sup>6</sup> , Lorenzo Natale<sup>4</sup> , Marco Maggiali<sup>1,5</sup> , Daniele Pucci<sup>1,2*</sup> 

1 GenerativeBionics, Genova, Italy. 

- 2Artificial and Mechanical Intelligence, Istituto Italiano di Tecnologia, Genova, Italy. 

3School of Computer Science, University of Manchester, Manchester, United Kingdom. 

- 4Humanoid Sensing and Perception, Istituto Italiano di Tecnologia, Genova, Italy. 

   - 5iCub Tech Facility, Istituto Italiano di Tecnologia, Genova, Italy. 

6DiMEILA, Istituto Nazionale Assicurazione Infortuni sul Lavoro (INAIL), Rome, Italy. 

- *Corresponding author(s). E-mail(s): carlotta.sartore@gbionics.ai; daniele.pucci@gbionics.ai; 

###### **Abstract** 

Collaboration is central to human behavior, enabling tasks beyond individual capability. This ability arises from coordinating actions through internal representations of others, a concept known as _shared intelligence_ . Additionally, humans are characterized by physical bodies and cognitive abilities that are optimized in response to their environment, a phenomenon referred to as _embodied cognition_ . Designing humanoid robots that collaborate safely and effectively with people requires unifying these principles. Here we propose an architecture that integrates _shared intelligence_ and _embodied cognition_ to enable robots to physically collaborate with humans, where robot hardware and control are optimized for human metrics, using representations of the human body and motion intelligence. The ultimate goal is to achieve a form of _shared embodied intelligence_ . Specifically, our architecture optimizes robot hardware and physical intelligence parameters with respect to human ergonomic metrics. This is accomplished by modeling human–robot interaction as a function of hardware configurations and embedding human models into the robot’s physical intelligence. As a concrete implementation, we present the humanoid robot ergoCub, whose morphology and control have been optimized for collaborative tasks with humans. Our approach provides a framework for designing humanoid robots that prioritize human ergonomics at both the hardware and physical intelligence levels, with applications in industrial and assistive robotics. 

**Keywords:** Humanoid robots, Physical human-robot interaction (pHRI) 

1 

## **1 Introduction** 

_Collaboration_ is a conducive condition for survival in the natural world, enabling groups to accomplish tasks unattainable by individuals. For instance, wolves leverage complex social dynamics to ensure both the pack’s and the individual’s survival [1]; ants coordinate to transport heavy loads; and human orchestras produce sounds impossible for individuals to create alone. Collaboration can even overcome species limitations, leading to interspecies partnerships such as the dog-human alliance, where dogs’ acute sense of smell complements humans’ strategic planning, resulting in highly effective rescue missions [2]. It becomes then clear how collaboration depends upon a degree of human _shared intelligence_ , namely, the capability to perform coordinated actions and maintain mutual awareness, thereby fostering intelligent behavior that surpasses individual capacities. An individual’s intelligence is also shaped by physical characteristics. This is evident in evolution, where physical traits develop alongside cognition, forming what is known as embodied cognition [3–5]. For example, consider the human ability to walk, which results from the synergy and coordination of muscle reflexes and neural circuits controlling gait [6]. Physical attributes have also evolved in response to the need for collaboration within and across species. An example is the oxpecker bird, whose beak has evolved to precisely remove parasites from its hosts without causing harm [7]. Inspired by the above observations, this paper lays the foundation for _shared embodied intelligence_ architectures for artificial agents, and more precisely for humanoid robots. By _shared embodied intelligence_ , we refer to the integration of _shared intelligence_ and _embodied cognition_ to equip an agent with both physical attributes and cognitive abilities optimized for collaboration with other beings. The proposed shared embodied intelligence architecture enables simultaneous optimization of the robot’s physical intelligence and hardware characteristics, taking into account not only the task and environment but also the physical intelligence and attributes of potential partners, whether human or robotic. We focus on humanoid robots as the target platform for our shared embodied intelligence architecture, since their human-like form enables more natural physical interaction and facilitates task execution in environments designed for humans [8]. The presented shared embodied intelligence principles are applied to design a humanoid robot: the ergoCub (Figure 1), developed at the Istituto Italiano di Tecnologia (IIT) in collaboration with the National Institute for Insurance against Accidents at Work (INAIL). 

### **1.1 Related works** 

In the literature, physical intelligence has been instantiated in various forms, including behavior models [9], imitation-learning policies [10], and foundation VLA models [11]. A widely adopted approach for humanoid robots is the cascade control architecture [12]. This architecture is structured into multiple layers - or control loops - each with a different role and degree of complexity. The outer layers provide references to achieve the desired goal while the inner layers of the control architecture receive inputs from the robot and from the environment, and they provide references to subsequent loops. The further down a control loop is within the hierarchical architecture, the more complex the robot models become and the shorter the prediction horizons are for generating outputs, which often enables each inner loop to run faster than the outer ones. Specifically, the standard _physical intelligence_ control architecture for humanoid robots comprises three fundamental layers: the _trajectory generation_ , the _trajectory adjustment_ , and the _trajectory control_ layer. The _trajectory generation_ layer translates high-level objectives into whole-body reference trajectories, typically using direct of indirect trajectory optimization or data-driven methods, often computed off-line without robot feedback [13–15]. The _trajectory adjustment_ layer refines these trajectories using simplified models and on-line feedback [16–18], which are then executed by the _trajectory control_ layer via inputs such as currents or voltages, commonly through Quadratic Programming (QP) [19–21]. This hierarchical control has also been applied to human–robot collaboration, with emphasis on safety, efficiency [22, 23], and _ergonomics_ [24, 25] to align with human physical and cognitive abilities. Despite the above efforts, shared actions remain elusive due to limited partner representation, leading to insufficient mutual partner awareness. When attempting energy efficiency or increasing robot performances, _physical intelligence_ may not be enough to achieve the desired requirements. _Robot hardware_ plays a pivotal role in these cases. However, the properties of the robot hardware are sometimes overlooked during the development of control architectures for 

2 

implementing robot _physical intelligence_ . Robot hardware is often treated as a given, immutable component. Conversely, during robot hardware design, the specific task the robot is intended to perform is sometimes disregarded, leading to suboptimal designs that do not align with the robot’s intended functions. To optimize robot hardware and control simultaneously, the principle of _co-design_ has been largely applied to the design process of robots. Co-design places a strong emphasis on optimizing parameters characterizing both the robot hardware and the control system to obtain optimal body-and-control robot concepts. For instance, the Alternating Direction Method of Multipliers (ADMM) has been used to identify quadruped hardware parameters optimized for walking on different terrains [26]. Additionally, reinforcement learning has been applied to the co-design problem considering the hardware as part of the policy showing evidence of how a task directly affects the design of the robot [27, 28]. Tackling the same problem, genetic algorithms have been used to identify optimum control and hardware able to ensure control robustness while minimizing energy consumption [29–31]. However, these studies focus on robots composed of a limited number of links, overlooking the inherent complexities of humanoid robots. Moreover, co-design principles are applied to individual robot subparts rather than considering the entire robot, missing the synergistic interplay among different robot components. Furthermore, co-design principles are yet to be applied to tailor robot designs addressing physical human-robot collaboration tasks. Our previous works [32, 33] presented the utilization of both classical optimization techniques and genetic algorithms to co-design humanoid robots for human-robot collaborative tasks still not considering human simulation and identifying hardware parameters under static conditions. Furthermore , they neither address the translation of the optimization output into real robot hardware, nor the integration of the optimal hardware with robot physical intelligence. 

### **1.2 Contribution** 

This paper proposes a methodology to optimize robot hardware and control parameters considering not only the robot body, environment, and task - as classically attempted when implementing instances of optimal _embodied cognition_ - but also possible partners possessing themselves a degree of _physical intelligence_ . We see this as a first step towards artificial agents owning a degree of _shared embodied intelligence_ , namely having humanoid robots designed considering the body and properties of surrounding individuals. More specifically, the contribution is two-fold: 

1. _Scientific_ : we present a _shared embodied intelligence_ architecture that can be employed to optimize both the hardware and control of humanoid robots interacting physically with humans to achieve specific tasks. The key ingredients of the architecture are: _i_ ) differentiable parametrized floating-base models representing humanoid robots and humans that exchange contact forces for achieving a physical collaboration task; the parameters of the models are robot limbs lengths and ensure physical consistency of the underlying mechanics (e.g. inertia) _ii_ ) a parametrized physical intelligence architecture for the humanoid robot that considers a representation of the physical intelligence of the human, which is implemented by modeling the policies that generate human movements, namely, signals that affect the human musculoskeletal system. The parameters of this architecture are those that characterize how the robot physical intelligence is implemented (e.g. gains of the low-level controllers, horizons of the high-level planners, etc.). The architecture, the controllers for the robot physical intelligence, and the differentiable models are publicly available in Python-based libraries (https://github.com/ami-iit/adam, https://github.com/ami-iit/shared-controllers). 

2. _Technological_ : we present the ergoCub humanoid robot, which is designed and controlled using the above architecture for shared embodied intelligence. The name of the humanoid robot is composed of two words: _ergo_ , which stands for _ergonomics_ , and _Cub_ , which references the _iCub_ humanoid robot that represented a starting point for the optimizations performed for the ergoCub. The emphasis on ergonomics is due to the fact that the robot was optimized with respect to two tasks: walking and collaborating with humans during payload lifting tasks. More precisely, the parameter optimization layer of the architecture considers quantitative human ergonomic indices, specifically human back stress, to identify parameters characterizing both the robot hardware and its physical intelligence, while simultaneously improving locomotion robustness and minimizing energy consumption. These metrics capture instantaneous biomechanical risk during 

3 

human–robot interaction and therefore quantify musculoskeletal loading. As such, they do not necessarily align with subjective human measures such as perceived comfort or fatigue. 

The ergoCub robot, coupled with its cognitive architecture, represents the inaugural embodiment of our methodology. 

## **2 Results** 

Shared embodied intelligence enables collaborative tasks by jointly optimizing robot hardware and control parameters with respect to ergonomic indexes. We designed a modular architecture based on human and robot representations to identify optimal hardware and physical intelligence parameters for human–robot collaboration. Here, _physical intelligence_ refers to the components that enable behaviors through movements, including trajectory blocks, sensors/sensory systems, and muscle/actuators (see Section 4.1). To design and control the ergoCub humanoid, we implemented two versions of this architecture. The first optimizes hardware by adjusting link lengths to improve walking performances and ergonomics during static collaborations (Figure 2a), assuming simplified link geometries to guide manufacturing. The second (Figure 2b) takes the optimized hardware as input and is aimed to improve human-robot coordination and robustness during task execution by optimizing the robot’s physical intelligence parameters, like gains and weights of the optimal control problems. Together, these two instances culminate in the ergoCub robot, which integrates optimized hardware and control. The following sections present and assess their results, validating our shared embodied intelligence approach. 

### **2.1 First architecture instance: ergoCub optimal hardware** 

The ergoCub robot is the outcome of a concatenation of manufacturing and optimization processes, as visually represented in Figure 2a. The hardware optimization employed non-linear techniques, which are highly sensitive to initial conditions. To address this, we used the iCub3 humanoid as a starting point, retaining its kinematic structure while optimizing link geometries for selected tasks. iCub3 is an open-source humanoid robot developed at IIT and widely adopted in applications from locomotion to telepresence [34], providing a solid baseline that ensured the optimization remained both effective and efficient. To maintain the iCub3 kinematic structure, electronics, and type of motors we imposed a constraint on the ergoCub maximum height to ensure manufacturability. In detail, we start by representing the iCub3 humanoid robot links using basic geometric shapes such as spheres, cylinders, and boxes to create a simplified model, depicted in Figure 2a. This approach allowed us to generalize the dynamic characteristics of the robot’s links based on their lengths. Subsequently, we analyze the influence of the robot hardware parameters on human-robot interaction by leveraging representations of the human body and physical intelligence. The key components of the human models are depicted in Figure 2a and they consist of policies that generate human motions, namely, signals that affect the human musculoskeletal system. Specifically, we modeled the human control system by decomposing it into two main components: a centralized processing unit representing the central nervous system’s role, and a local processing unit representing the output of the peripheral nervous system. The centralized processing unit models the high-level motion commands, and it includes whole-body control and trajectory blocks. The model of the peripheral nervous system concerns the joint control loop, and it includes blocks for gathering sensory information and stabilizing motion through localized muscle reflexes. Further details are provided in Section 4.1.3. Starting from the defined human and robot model, we formulated the human-robot coupled dynamics, parametrized with respect to the robot hardware parameters. Such a coupled human-robot parametrized dynamic is harnessed to define an optimization problem to find the robot optimum link lengths. In this optimization, our focus is on a scenario where a human and a robot collaborate to lift a load. More precisely, our objective is two-fold : enhancing walking capabilities and improving the ergonomics of human-robot physical interaction. In this way, we will design a humanoid robot able to collaborate with humans in lifting a load but we will also consider additional humanoid robot key abilities such as walking. More in detail, the optimization problem was defined with two main objectives. The first was to improve ergonomics during human–robot collaborative lifting by minimizing the energy expenditure of both agents, quantified as joint torques, across several static lifting configurations (see Section 4.2). The second objective was to enhance walking performance by raising the robot’s 

4 

center of mass, thereby increasing system bandwidth and robustness [35]. More detail about the formulation and mathematical background of the optimization problem defined can be found in Section 4.2. In Figure 3, we present the outputs of the hardware optimization process. Figure 3 (a) shows the simplified model of the iCub3 robot, depicted in red, serving as the initial configuration for our optimization. Figures 3 (b) and 3 (c) depict the robot designs obtained through the proposed optimization, considering load height ranges of 0 _._ 8 m to 1 _._ 2 m and 0 _._ 8 m to 1 _._ 5 m, respectively. We will refer to these models as the optimized blue model and the optimized green model respectively. Figure 3 (d) summarizes the output of the performed optimization by reporting the human joint torque computed for the original, optimized blue, and optimized green robot designs. These torque values are deterministic and directly tied to the cost function of the optimization problem (more detail can be found in Section 4.2). Real-world testing involving human-robot physical collaborations is presented separately in Section 2.2. Compared to the original design (Figure 3 a), the optimized blue model (Figure 3 (b)) reduces human back stress at all load heights, with the greatest relief observed at the lumbosacral joint (L5–S1), a region particularly vulnerable to high compressive forces during lifting [36]. The green model (Figure 3 (c)) further decreases back torque at nearly all heights, except at 0 _._ 8 m, and uniquely enables lifting tasks up to 1 _._ 5 m. For these reasons, we selected the green solution, as it provides the best compromise between extended task reach and improved ergonomics, outperforming both the original design (red in Figure 3 a) and the other optimized candidate (blue in Figure 3 (b)). The limb lengths of the selected solution are provided in Figure 3 (e). Starting with the identified optimal limb lengths, we built ergoCub and employed metal extenders to achieve the desired measurements. In the same Figure 3 (e), we report the main dimensions of ergoCub compared with iCub3, and in Figure 1a we illustrate additional features of ergoCub. Further analyses are provided in the supplementary material, including a comparison of collaborative payload lifting between ergoCub and iCub3 (Appendix B). To enhance human–robot coordination, ergoCub is equipped with a flexible LCD screen that displays simplified facial expressions, enabling feedback during task execution (see Section 2.2). The acceptability of the ergoCUb design was evaluated in a survey with 850 participants from industrial and healthcare domains. ergoCub was rated more positively than Baxter [37] and R1 [38], and its simplified facial expressions were consistently preferred (Appendix E) over the alternatives. 

### **2.2 Second architecture instance: ergoCub physical intelligence** 

In this section, we examine the ergoCub’s physical intelligence, namely its ability to generate movements that achieve the desired behavior. Building on the optimized hardware described in Section 2.1, we refined the control architecture shown in Figure 2b to address both collaboration and locomotion. For collaboration, the framework mirrors human and robot physical intelligence as hierarchical systems composed of trajectory blocks, sensors, and actuators. Such symmetry allows the robot to account for the human partner’s behavior and identify strategies that enhance collaboration. For locomotion, the human component is disregarded, and the framework focuses on walking performance. We present both collaboration and locomotion instances since the hardware optimization enhanced both tasks. Appendix A describes an additional validation scenario in which a human and ergoCub walk together while carrying a payload. 

#### **Human-robot collaboration tasks** 

We validated the optimized hardware and shared embodied intelligence architecture for physical intelligence (Figure 2b) on the real ergoCub robot. In the tested scenario (Figure 1b–d), the robot collaborates with a human partner to manipulate payloads of varying weights: empty, 1 kg, and 2 kg. During these collaborations, the robot follows the human’s upward and downward movements while the human’s stress is monitored. These experiments are conducted in a dynamic setting, with the human and robot jointly moving the load, thereby relaxing the static assumptions of the hardware optimization. In an initial offline phase, a human model is initialized by measuring the subject’s height and weight, following [39]. During collaboration, this model is continuously updated by an estimation algorithm using data from non-intrusive wearable sensors (Appendix E). More specifically, human kinematics are estimated with an inverse kinematics approach [40], while joint torques are computed using a 

5 

Maximum-A-Posteriori method [39, 41] and smoothed with a moving average filter (window size = 2). These estimates continuously update the internal human model of the shared embodied intelligence architecture. Thanks to this approach, the robot’s physical intelligence can adapt to different human partners, capturing individual physical characteristics through offline initialization of the human model, and online updates of the human kinematics and dynamics via sensor feedback. The robot’s reference trajectories are pre-planned to optimize the configuration during human interaction, while the robot’s movement velocity (in terms of both amplitude and direction) is governed by a variable that depends on the height difference between the robot’s and the human’s hands. The theoretical framework of this architecture is detailed in Section 4.3.1. During task execution, the robot continuously monitors the human’s ergonomic state by estimating the torque exerted on the lumbosacral joint (L5-S1), a critical indicator of ergonomic strain in lifting tasks. Based on the detected stress levels at the L5-S1 joint, the robot uses its head-mounted LCD screen to display expressive feedback, signaling whether the human is experiencing high or low stress. Moreover, the robot follows the human only within a predefined height range of 0 _._ 8 m to 1 _._ 2 m; if the human’s motion exceeds this range, the robot stops following. This range depends on the task and is fully configurable within the architecture. Crucially, it is not a limitation of the hardware or physical intelligence: if enlarged, ergonomic support is still guaranteed by the hardware design and the real-time adaptation of the physical intelligence. In Figure 4, we present the results of the human and robot collaborating to manipulate loads of different weights: empty, 1 kg, and 2 kg. In Figure 4 (a) we compare the human hands’ height with the robot one. It can be noticed how the robot correctly follows the human in all three cases but that there are some delays in the robot’s movements with respect to the human one, these are because there is no prediction of the human movements. Nevertheless, the robot consistently follows the human’s movements, with an average error of 0 _._ 0084 m and a mean maximum error of 0 _._ 0339 m across the three experiments. Figure 4 (b) shows the maximum L5-S1 joint torque experienced by the human when manipulating loads of 1 kg and 2 kg and empty, with and without the robot’s assistance. The stress on the lumbosacral joint is significantly reduced when the human collaborates with the robot. For instance, the peak torque decreases from 43 _._ 95 _Nm_ to 24 _._ 88 _Nm_ with the empty load, and a similar trend is observed for the 1 kg and 2 kg loads, where the peaks when collaborating with the robot drop from 50 _._ 66 _Nm_ to 25 _._ 77 _Nm_ and from 44 _._ 88 _Nm_ to 31 _._ 82 _Nm_ . 

#### **Locomotion tasks** 

The optimization process that determined the primary shape of ergoCub also specifically aimed to enhance the robot locomotion abilities. Let us recall, in fact, that the optimization problem has a task specifically aimed at increasing the system bandwidth to improve the walking robustness. The synergy of the robot design with the locomotion architecture results in robust walking performances (in the sense of the ability to adapt footsteps for small pushes). Because of this, and compared to its predecessor iCub3, the ergoCub robot is able to walk faster and smoother; the maximal step length achieved is 0 _._ 35 m compared to 0 _._ 28 m on the iCub3 with a minimal step duration being 0 _._ 5 s compared to 0 _._ 8 s on the iCub3 using the same walking command and control architecture. The detailed comparison of the locomotion capability can be seen in Appendix C with the robots walking side by side given the same commands. For optimizing the locomotion ability of the ergoCub robot, we employed the architecture instance represented in Figure 2b, disregarding the human model and focusing on the robot control architecture. The details of each component of the employed architecture, and the mathematics involved are deferred to Sections 4.3.2 for the interested reader. In the classical locomotion architectures, the trajectory adjustment layers uses “template” models (e.g. the Linear Inverted Pendulum LIPM, or more recently the centroidal dynamics model [42]) to compute the Center of Mass - CoM - and feet trajectories [43, 44], while the trajectory control layer provides individual position commands to the robot joints motors by solving an instantaneous inverse kinematics (or inverse dynamics) problem. The trajectory generation and adjustment blocks run at 50 Hz, generating kinematically feasible nominal trajectories for the CoM and feet contact locations and timings respectively, while the trajectory control, being an instantaneous controller, running at 500 Hz solves a stack-of-tasks QP, generating desired joint velocities which are integrated to the low-level motor control boards. The solution is obtained using an off-the-shelf optimization solver, running on a 2.4 GHz Intel©core i7 Ubuntu machine mounted inside 

6 

the robot torso to serve as the main computational resource. The robot locomotion capabilities in this context are tested in different scenarios, among which are the ones reported below 

- _Locomotion with persistent disturbances:_ in combination with the robot forearms and wrist hardware design, the detailed locomotion architecture allows for carrying the rated payload (6 kg) adjusting the nominal footsteps plan if necessary to counter the effect of this persistent disturbance. 

- _Locomotion with time-varying disturbances:_ as can be seen in Figure 5, and more precisely in multimedia video companion, the robot is subjected to increasing payload forces while a human is pushing on the robot right upper arm (impulsive pushes estimated using an Newton-Euler method [45] propagating FT measurements to be around 60 N _−_ 100 N). The robot can complete the task (walking in a straight line), adjusting the steps within a nominal error bound if necessary to prevent falling (see Figure 5 - (a)). 

## **3 Discussion** 

The work presented contributes to the state of the art by deriving a methodology for designing humanoid robots that explicitly account for human comfort and task requirements (e.g., walking stability) already at the hardware design stage, and not solely when implementing the robot behavior. In Section 2.1, we presented the ergoCub humanoid robot, which is the outcome of the proposed modular architecture instances depicted in Figure 2a and 2b, which implements the paper methodology. By integrating shared intelligence, coordinated action, and mutual awareness, with embodied cognition, namely the coupling between morphology and physical intelligence, the proposed methodology enables the joint design of robot morphology and control policies with respect to human-centered metrics. Within this perspective, the ergoCub robot represents a contribution in its own as a tangible realization of the methodology, demonstrating how human representations can be embedded into the robot’s body and physical intelligence to support ergonomic collaboration and robust locomotion. The reported results illustrate the effects of this design approach on representative collaborative and locomotion tasks, providing evidence of the feasibility and practical relevance of the proposed framework, as well as the advantages of embedding human representation within the robot’s physical intelligence for human–robot collaboration. Indeed, the experimental campaign is designed to validate the feasibility and internal consistency of the proposed methodology as well as evaluate how the hardware optimization can be translated into a real humanoid robot. The focus is on demonstrating that embeeding task related objective during hardware optimization results in improved task performance. Particularly, for human-robot interaction, this translates into embedding human representations at the hardware optimization stage and results in improved ergonomy interaction. Broader user studies assessing long-term interaction fluency, subjective comfort across diverse populations, or clinical ergonomic validation represent complementary research directions that are not covered by the results presented in this paper. Additionally, the proposed optimization targets biomechanical risk metrics, which do not necessarily align with subjective perceptions of fatigue or comfort, further motivating the use of objective biomechanical indicators in the experimental campaign. The remainder of this section is organized as follows. In Section 3.1, we further elaborate on the adopted human representations, while in Section 3.2 we discuss possible extensions incorporating predictive components. Section 3.3 addresses the generalizability of the hardware optimization framework and its potential extensions. In Section 3.4, we analyze how the hardware optimization was translated into a realized humanoid robot. Finally, Section 3.5 proposes strategies to mitigate the sim-to-real gap arising from manufacturing process. 

### **3.1 Human representations** 

The proposed modular architecture (Figure 2b) integrates both hardware optimization and robot physical intelligence to support locomotion and active human–robot collaboration through mutual partner awareness. This is achieved by explicitly incorporating human models into the hardware optimization process and by embedding models of human behavior within the robot’s control architecture. The human is represented as a multi-rigid-body system governed by a hierarchical control structure. This abstraction is embedded in both the hardware optimization and the robot’s physical intelligence. At the design stage, this level of abstraction enables the inclusion of human ergonomic metrics without overfitting to specific individual characteristics. The simplified morphology 

7 

allows the optimization to capture general human-centered properties while remaining computationally tractable. At the control level, we adopt a unified framework in which both agents operate with internal representations of each other’s behavior: the robot relies on its human model, while the human relies on natural intuition and cognitive abilities to coordinate with the robot. Indeed, in collaborative scenarios, representing a partner’s actions and planning accordingly is essential for intelligibility and acceptability [46]. Nevertheless, a fully detailed representation of human physical intelligence is unattainable due to the complexity of musculoskeletal and neuro-sensory processes. Simplifications are therefore necessary to enable real-time estimation from non-intrusive sensors and limited measurements. In our framework, the human physical intelligence is modeled using the same logical components as the robot, namely trajectory planning, adjustment, and control blocks. Although this symmetry is an abstraction, it captures the essential features required for ergonomic collaboration and enables seamless integration within the robot’s control architecture. As shown in Appendix A, the same modeling principles extend to more dynamic scenarios such as collaborative walking. Importantly, the results involve three distinct human subjects: one whose model informed hardware optimization, one performing collaborative payload lifting, and one engaged in collaborative walking. These subjects differ substantially in anthropometry and strength. Nevertheless, the ergonomic benefits are consistently preserved, demonstrating that the design-level optimization does not overfit a specific individual. Instead, inter-subject variability is accommodated through the robot’s physical intelligence, which integrates subject-specific modeling and real-time measurements. These choices are supported by both the present experimental validation and prior related work [39–41, 47, 48]. 

### **3.2 Human representation improvements** 

We have analyzed in detail the rationale behind the adopted human representation and its role within the proposed robot physical intelligence. While this representation captures key structural and ergonomic aspects of human–robot collaboration, it currently models interaction in a purely reactive manner. Specifically, anticipatory behavior is not yet explicitly incorporated into the framework. A conservative refinement could involve using the robot’s LCD interface to signal potentially unsafe postures, thereby encouraging proactive human correction without imposing explicit behavioral constraints; nevertheless, this would still rely on the real-time human measurement. A more comprehensive extension would integrate short-horizon human motion forecasting directly within the robot’s physical intelligence. Such forecasting could rely on data-driven models of human movement,for example, leveraging wearable sensing approaches as in [49], which are compatible with the sensing setup considered in this work. Anticipatory behavior could be incorporated into the robot’s physical intelligence trajectory planning module. Short-horizon forecasts would provide predicted future human states, from which corresponding ergonomic metrics could be estimated. The planning layer would then compute a robot trajectory that minimizes the expected ergonomic cost over the prediction horizon, effectively biasing behavior toward configurations that are most likely to reduce human musculoskeletal load in the near future. The resulting reference trajectory would be passed to the trajectory control layer, operating at a higher frequency to ensure accurate tracking while remaining responsive to real-time human measurements. Within this hierarchical structure, prediction informs planned behavior, while the robot trajectory control preserves robustness to modeling inaccuracies, sensing uncertainty, and unexpected human deviations by relying on real-time human measurements. Importantly, this extension affects only the physical intelligence layer and does not modify the hardware optimization stage, which embeds structural human representations at design time. The validity of the co-design methodology, therefore, remains independent of whether online interaction is purely reactive or augmented with predictive components. 

### **3.3 Generalizability across tasks and human partners** 

In this work, we focused on payload lifting and walking tasks, which represent constrained yet relevant scenarios in industrial and healthcare contexts. This choice enabled a clear analysis of how the proposed methodology translates from an abstract optimization framework into a realizable robotic platform, and allowed us to evaluate its effectiveness on concrete tasks. Nevertheless, the methodology can be extended to accommodate different 

8 

task requirements by encoding them through appropriate objective functions and constraints. It can also incorporate additional hardware and control related goals, such as power consumption, mass distribution, end-effector workspace specifications, and dynamic behaviors (e.g., running). Importantly, human-related ergonomic metrics and locomotion-related objectives were jointly included within a single optimization problem, already demonstrating the flexibility of the framework to address multiple task requirements simultaneously. A promising extension would be to encode collaborative scenarios involving multiple human partners and heterogeneous payloads. This could be achieved by extending the same optimization problem, specifically by replicating the coupled human–robot–load dynamics for each subject or load of interest. Since the optimization is performed offline to identify optimal hardware parameters, the resulting computational overhead would likely remain tractable. However, real-time human measurements and subject-specific models embedded in the robot’s physical intelligence would still be required to ensure smooth interaction and preserve the generalizability of the proposed approach. More generally, although the experimental validation focuses on structured collaborative tasks, the architecture itself is not restricted to predefined motion patterns. During interaction, the robot continuously estimates human kinematics and dynamics through real-time sensing and updates its internal human model accordingly. This enables the robot’s physical intelligence to react to variations in human motion and behavior during collaboration. Future extensions incorporating predictive models of human motion, as discussed in Section 3.2, could further enhance the system’s ability to anticipate evolving human strategies in more dynamic and less structured collaboration scenarios. 

### **3.4 From optimized models to a real robot hardware** 

The distinctiveness of the proposed hardware optimization lies in its explicit use of human–robot coupled dynamics and non-linear optimization, directly linking hardware characteristics to task performance. By incorporating ergonomic metrics, the human factor is addressed at the design stage rather than only during behavior implementation. A limitation of this approach is the sensitivity of non-linear methods to initial conditions and local minima, which we mitigated by initializing with iCub3, thereby starting from a proven design, ensuring manufacturability. To keep the problem tractable, we considered multiple static task configurations, leaving motion-related ergonomics to the physical intelligence component. Simplifications in modeling, however, led to some mismatches between the optimized design and the manufactured ergoCub. As shown in Figure 3 (e), ergoCub differs from the optimization output in height, weight, and slightly in limb lengths. These discrepancies arise from several factors for instance, the head is larger than in the optimized model, since an LCD screen was added to display emotions, increasing the overall height compared to the original iCub design. Regarding the robot weight, the optimization assumed the densities constant along the link, whereas during manufacturing, we reused iCub3 electronics and motors [34] and employed metal extenders to lengthen the limbs. This difference, combined with the manufacturing optimization process, resulted in lighter components and produced a robot approximately 0 _._ 25 m taller than iCub3, yet weighing only 56.70 kg, i.e., about 4 kg more than iCub3. Compared to the optimization output, which predicted a mass of 70 kg under simplified density assumptions, the final robot is substantially lighter thanks to a dedicated manufacturing optimization process. The legs and torso of ergoCub are 0 _._ 01 m shorter than the optimized design because the optimization simplified links into basic shapes and omitted assembly details such as covers, electronics, and wiring. The accumulated small mismatches in building the robot led to slight differences in proportions during construction. The simplifications introduced were necessary for tractability but do not undermine the generality of the method. In practice, assumptions such as simplified shapes or uniform densities are relaxed during manufacturing, where each link is refined at the sub-component level while preserving the wholebody properties identified by optimization. This enables attainment of the global link optimum, even if equivalent masses or volumes are achieved through adjustments in the smaller link components. Despite its challenges, the approach yielded tangible results, with the ergoCub robot successfully retaining the ergonomic enhancements from the optimization process. 

9 

### **3.5 Bridging the sim-to-real gap** 

Discrepancies between the optimization output and the manufactured robot primarily arise from three sources: (i) geometric simplifications adopted to ensure tractable nonlinear optimization, (ii) simplified inertial assumptions, such as uniform density distributions, and (iii) practical manufacturing constraints that prevent the physical hardware from exactly matching the optimized design (e.g., component reuse, wiring, protective covers, and mechanical tolerances). Several strategies could reduce the sim-to-real gap. Regarding geometric simplifications, the hardware optimization model could be refined by decomposing links into subcomponents (e.g., motors, electronics, structural elements, and covers), although this would increase problem complexity. Concerning inertial assumptions, material-dependent density distributions could be incorporated into the optimization and treated as design variables. While this would remain an approximation, since link density is not perfectly uniform, it would yield a more accurate representation of mass distribution and potentially improve optimization fidelity. With respect to manufacturing constraints, the sim-to-real gap can be further reduced through progressive model refinement. An initial optimization stage may rely on simplified link representations to identify globally consistent proportions, mass distributions, and dynamic properties. As the mechanical design evolves, subsequent optimization stages can incorporate increasingly detailed geometric and inertial descriptions, with the optimzation that follows the stages of the mechanical design. Another approach could involve calibration loops introduced after prototype realization: experimentally measured sub-component parameters, such as inertial parameters and joint-level actuation characteristics, can be fed back into the optimization model, enabling dynamic parameter reidentification and refinement of task-level objectives. Surrogate modeling techniques can also be used to improve physical accuracy while reducing computational burden. Nevertheless since hardware parameters constitute the decision variables of the nonlinear optimization, any surrogate model must be formulated explicitly as a function of those same variables. This ensures that detailed hardware characterization can be introduced without removing hardware parameters from the optimization search space. 

10 

## **Declarations** 

##### **_Data Availability:_** 

The data supporting the findings of this study are publicly available in the paper repository at https://github.com /ami-iit/paper ~~s~~ artore ~~2~~ 025 ~~e~~ rgocub ~~n~~ ature ~~m~~ achine ~~i~~ ntelligence [50]. For further inquiries regarding the data, please contact the corresponding authors at carlotta.sartore@gbionics.ai and daniele.pucci@gbionics.ai. 

##### **_Code Availability:_** 

The code developed to derive the results of the presented work is available at https://github.com/ami-iit/paper ~~s~~ ar tore ~~2~~ 025 ~~e~~ rgocub ~~n~~ ature ~~m~~ achine ~~i~~ ntelligence [50]. 

##### **_Acknowledgements:_** 

The authors acknowledge Mattia Salvi, Davide Gorbani, Camilla Gallina and Dario Maria Sortino for their technical support during the experimental phases of this work, and Francesca Bruzzone and Bruno Trombetta for their support in video production and material preparation. 

##### **_Author contributions Statement:_** 

- **Conceptualization** : C.S., L.R., M.E., L.F., F.D., G.T., L.N, M.M, D.P. 

- **Funding acquisition** : M.M., D.P. 

- **Investigation** : C.S., L.R., M.E.,G.R., S.D.,N.A.P., I.S., P.M.V., S.T., L.F. 

- **Methodology** : C.S., L.R., M.E., D.P. 

- **Project administration** : D.P. 

- **Software** : C.S., L.R.,M.E., G.R., S.D., S.T., U.P., 

- **Supervision** : L.R., L.N., M.M., D.P. 

- **Validation** : C.S., L.R., M.E., G.R., S.D., I.S., P.M.V. 

- **Visualization** : C.S., L.R., M.E., N.A.P. 

- **Writing** : C.S., L.R., M.E., D.P. 

##### **_Competing interests Statement:_** 

The authors declare that they have no competing interests. 

##### **_Funding:_** 

The paper was supported by the Italian National Institute for Insurance against Accidents at Work (INAIL) ergoCub Project. 

11 


**Fig. 1** : The ergoCub robot, a humanoid robot developed to minimize workers’ fatigue and risks in collaborative tasks for industry and healthcare, and endowed with a degree of shared embodied intelligence. In (a), the main characteristics of the ergoCub robot. In (b)–(d), The ergoCub robot collaborates with a human to perform a payload lifting task, adapting its motion to the human partner and monitoring the human’s ergonomic state to reduce physical stress. In (e)–(g), the ergoCub robot walks during a live demo on stage. 

12 


**Fig. 2** : The shared embodied intelligence architecture instances to optimize robot hardware and physical intelligence leveraging human-robot interaction models that are parametrized with respect to robot hardware parameters. Within this architecture, both human and robot physical intelligence are structured within a hierarchical control framework, establishing symmetry between the two agents. Figure (a) illustrates the architecture instance that identifies optimal robot hardware parameters for static collaborations with human and walking tasks. The output consists of optimal robot link lengths to enhance human ergonomics and robot walking capabilities. Such output has been used to manufacture the real ergoCub robot. In Figure (b), the architecture instance to optimize the ergoCub physical intelligence given the optimal hardware. The output enables the ergoCub robot to collaborate with humans and walk robustly. 

13 


**Fig. 3** : Comparison between iCub3, different humanoid robot models output of the presented optimization framework and ergoCub. In (a), the iCub3 simplified robot collaborates with a human. In (b) and (c), we present the humanoid robot outputs optimized for collaborative payload lifting, with load height ranges of 0 _._ 8 m to 1 _._ 2 m and 0 _._ 8 m to 1 _._ 5 m, respectively. In (d), we illustrate the human back torques when holding a box at different heights using the models depicted in Figures (a), (b), and (c) in green we highlight the model used to define the ergoCub robot link lengths. In (e) the main dimensions of ergoCub, iCub3, and the optimization output for Figure (c), used to define the ergoCub limb lengths. 

14 


**Fig. 4** : Comparison of hand trajectories and lumbosacral joint torques during human-robot collaborative payload lifting with ergoCub robot. In (a) Comparison of hand height trajectories between the human and the robot during the lifting task with three different payloads. In (b), the maximum estimated torque on the human’s lumbosacral joint (L5-S1) during the payload lifting task with three different weights, comparing collaboration with the robot versus performing the task alone. 

15 


**Fig. 5** : Figure showing the tracking performances of the ergoCub Controller while executing a walking-in-straightline task subject to pushes and carrying a heavy box. ( _a_ ) the reference and actual footsteps. The adaptation at the end of the sequence is due to push exerted by the human, with direction of walking given by the dashed arrow, ( _b_ ); the CoM trajectory tracking performance, with the big push corresponding to a larger _y_ component adjustment. 

16 


**Fig. 6** : Shared embodied intelligence framework. In (a), we depict the parametrization of humanoid robot dynamics based on hardware parameters. (b) Shows the human modeled as a multi-rigid body system. (c) Illustrates the coupled dynamics of human-robot-load, parametrized with respect to robot hardware parameters. In (c), we also display the physical intelligence architecture employed, consisting of trajectory blocks providing joint-level inputs to muscles/actuators using sensor/sensory system feedback. For the human, physical intelligence is divided into the peripheral and central nervous systems. 

17 

## **4 Methods** 

At the methodological level, our goal is to propose a shared embodied intelligence architecture to enable effective physical collaboration between robots and surrounding humans, namely, identify robot hardware and control parameters to optimize quantities of the human collaborator. A high-level sketch of the framework is depicted in Figure 6. We design the architecture to be modular, being composed of different blocks suitable for various robot tasks performed with or without a human collaborator. The first key element is the _agent design_ , hence human body properties and robot hardware characteristics. The second key element of the architecture is representations of both the human and the robot’s physical intelligence, thus the blocks that define the agent motion to achieve the desired behavior. For both the human and the robot, we employed a hierarchical control architecture to model the physical intelligence, establishing a symmetry between the two agents. The key blocks constituting both human and robot physical intelligence include: (i) _muscles/actuators_ , which model joint-level actuation in both the robot and the human; (ii) _sensors/sensory systems_ , which perceive information from the environment and the agent’s state; and (iii) _trajectory planning_ , _trajectory adjustment_ , and _trajectory control_ blocks, which respectively generate, refine, and execute trajectories to achieve the desired behavior. For what concerns the human, for the sake of simplicity, we associate the peripheral nervous system with the joint control loop and the central nervous system with whole-body control. Building upon this modular modeling, we developed a parametrized architecture incorporating environmental factors such as the interaction between different agents or the agents and the environment. We present two instances of this architecture, as illustrated in Figure 2, whose outputs culminate in the realization of the ergoCub robot, as presented in the previous Section 2. The implemented architecture instances are obtained by activating specific sub-modeling components, and each of these instances targets specific objectives and differs in terms of optimized parameters. The ultimate objective of each instance is to identify an architecture configuration that realizes the envisioned shared embodied intelligence. In the following sections, we delve into the different sub-blocks that compose the architecture and the instances defined. The rest of the sections are organized as follows: in Section 4.1, we detail the modeling employed to represent the human, the robot, and the human-robot interaction, as well as the models employed in the robot physical intelligence and the hardware optimization processes. Subsequently, in Section 4.2, we delve into the optimization process that crafted the ergoCub robot, as presented in Section 2.1. Moving on to Section 4.3, we explore the architecture instances that define the ergoCub physical intelligence, which confers upon the ergoCub robot the capability to engage in physical collaboration with humans and exhibit walking abilities, as shown in Section 2.2. 

### **4.1 Modeling** 

In the context of this work, we define physical collaboration as the ability of humanoid agents, whether they be humans or humanoid robots, to interact with the environment while jointly lifting objects. To achieve the shared embodied intelligence envisioned in this study, it is essential to examine the mutual influence each agent exerts on the other, as well as the impact of hardware and control parameters on this interaction. In these sections, we provide a detailed description of the humanoid robot dynamic parametrization with respect to robot hardware parameters, together with the exploited human model. Furthermore, we formulate the coupled dynamics, building upon the individual representations of both the robot and the human, that describe their reciprocal interaction and the interaction with the environment. These models are leveraged to identify the optimal hardware design and physical intelligence required to attain shared embodied intelligence. Before delving into the details properly, we define the following basic notations and nomenclature which will be used throughout the rest of this section. 

- For an element of a normed Euclidean 3D space, _x ∈_ R<sup>3</sup> , _x_<sup>_∧_</sup> = _S_ ( _x_ ) : R<sup>3</sup> _→_ so(3) returns the skew symmetric matrix form of _x_ . 

- Given an inertial frame, _I_ , and a frame attached to the rigid body (base frame) _B_ ,<sup>_I_</sup> _pB ∈_ R<sup>3</sup> and<sup>_I_</sup> _RB ∈ SO_ (3) denote the position and the orientation of the _base frame_ respectively. 

- Whenever the superscripts are dropped, quantities are referred to the inertial frame, e.g. _pCoM_ denotes the position of the CoM of the model referred to the inertial frame. 

- Denote by I3 _,_ 03 the identity and zero matrices of dimension 3 respectively. 

18 

#### **4.1.1 Humanoid robot parametrized dynamics** 

To parameterize the robot dynamics with respect to the robot hardware parameters, we establish the relationship between the hardware parameters, namely link lengths, and densities, and the inertial characteristics of the rigid body. For any given rigid body, its inertial properties are described by the density _ρ ∈_ R<sup>+</sup> , and _V_ = _V_ ( _l_ ) _⊂_ R<sup>3</sup> , representing a region in the 3D Euclidean space where _ρ̸_ = 0 and dependent on the body shape and a set of dimensional parameters _l ∈_ R<sup>_nl_</sup> . This parametrization allows us to express the rigid body mass _m_ , the inertia _I_ and the rigid body center of mass _c_ computed with respect to the rigid body frame _L_ as functions of _ρ_ and _l_ , as per Equation (1), where _r_ is expressed with respect to the rigid body frame _L_ 


We consider basic shapes such as spheres, cylinders, and boxes. We parametrize their geometry using _lm ∈_ R<sup>+</sup> as a multiplier that elongates the shape along its principal directions and we assumed _ρ_ to be uniform across all body points. With this established relationship, we then parameterize the rigid body dynamics with respect to _lm_ and _ρ_ as per Equation (2), following the notation of [51]: 


where 


to the inertial reference frame _I_ 

- _M ∈_ R<sup>6</sup><sup>_×_6</sup> is the 6D inertia matrix defined as: 


where _m_ and _I_ are computed as per Equation 1. 


The same approach as described in Equation (2) was applied to each link of the robot kinematic chain. This enables us to define _π_ as the set of hardware parameters associated with the robot links, encompassing the length multiplier _lm_ and density _ρ_ for each link. To formulate the robot’s dynamics, we apply the Euler-Poincar`e formalism [53] to the kinematic chain. This results in a comprehensive set of differential equations, accompanied by holonomic constraints that characterize the robot dynamical behavior parametrized with respect to the set of hardware parameters _π_ : 


where: 

19 

- _nR_ is the number of the robot _joints_ with one degree of freedom that connect _nR_ + 1 rigid bodies, i.e. _links_ that composes the robot. 

- _q_ = � _IpB,_<sup>_I_</sup> _RB, s_ � represents the system configuration, where _s ∈_ R<sup>_nR_</sup> is the joints configuration and _I_ is the reference inertial frame. 

- _ν ∈_ V is the model velocity and is defined as _ν_ = � _I_ v _B, s_ ˙� where<sup>_I_</sup> v _B_ = � _I_ ˙ _pB, IωB_ � _∈_ R<sup>6</sup> denotes the linear and angular velocity of the _base frame_ , and _s_ ˙ denotes the joint velocities. 

- _M ∈_ R<sup>(</sup><sup>_nR_+6)</sup><sup>_×_(</sup><sup>_nR_+6)</sup> is the mass matrix, 

- _h ∈_ R<sup>_nR_+6</sup> is the term accounting for Coriolis and gravity forces. 

- _B_ = �0 _nR×_ 6 _,_ I _n_ � _T_ is a selector matrix. 

- _τ ∈_ R<sup>_nR_</sup> is a vector representing the robot’s joint torques. 

- _f ∈_ R<sup>6</sup><sup>_nc_</sup> represents a vector containing _nc_ wrenches stacked. 

- _Jc ∈_ R<sup>_nR_+6</sup><sup>_×_6</sup><sup>_nc_</sup> is the Jacobian of the contact frames. 

In this work, we consider a robot composed solely of basic shapes — spheres, cylinders, and boxes. Therefore, starting with the iCub3 robot topology, we designed the model depicted in Figure 6a. 

#### **4.1.2 Human modeling** 

A comprehensive description of the human body and its physical intelligence is nearly impossible, even with vast amounts of data. Therefore, it is crucial to select models that effectively capture key aspects of the human body and behavior based on specific objectives. In this work, we utilize models of the musculoskeletal system, which governs body structure and movement, and the nervous system, which processes sensory information and generates motor commands [54]. **Musculoskeletal system** We begin by modeling the human skeleton as a floating-base multi-body system with _NH_ links connected through _nH_ joints. In the context of this work, _nH_ = 34 joints, 6 per arm, 9 in each leg, and 4 in the back. Each link corresponds to a segment of the human skeleton represented as a basic geometry, that prioritizes fast processing over fidelity, based on the model proposed in [39]. The mass is distributed on different body districts based on anthropometric tables [55, 56]. The resulting model is depicted in Figure 6b. The skeletal muscles act on the human skeleton by contracting and consequently transmitting the force through the tendons to the bones. Considering that there are more than 600 skeletal muscles [57], in the proposed model, the effect of muscle groups is synthesized by the resulting torques _τH ∈_ R<sup>_nH_</sup> applied to the system joints. The human dynamics is therefore described with the same set of equations presented in Equation 4 for the robot dynamics, but disregarding the dependency on the hardware parameters _π_ . The human torques are computed online with a Maximum a Posteriori (MaP) estimation as per [39], exploiting the contact wrench measurements given by the FT on the shoes and the output of the Inverse kinematic estimation that computes the joint configuration given the iFeel and tracker sensors output as per [40]. More in detail, the system dynamics is rearranged into a compact matrix form of Equation (5) 


where _Y_ and _D_ are matrices accounting for the sensor measurements and the system dynamics respectively, _bY_ and _bD_ are the associated bias term. _γ_ is a vector collecting the sensor measurements, in our case, it contains IMU and Force Torque (FT) measurements from the iFeel sensors. The vector _d_ includes the dynamic and kinematic quantities of the links and joints such as the proper sensor acceleration, the internal joint wrench, and the joint acceleration. The algorithm maximizes the probability of _d_ given the sensor measurements. which leads to : 


where _µ_ and Σ are respectively the mean and the covariance matrix, while _P_ � _d|γ_ � is the probability of _d_ conditioned on _γ_ . **Nervous system** The nervous system integrates sensory inputs and high-level goals, transforming them into motor commands through various pathways. These pathways can be either centralized—comprising the 

20 

ascending path to the brain and the descending path from the brain to the muscles—or local, involving the reflex arc path between the muscles and the spinal cord. Given the diverse operational pathways, the human nervous system can be conceptualized as a hierarchical control system, with multiple loops running in parallel [58] [48]. This conceptualization has led to the proposal of a hierarchical human motor control model, which mirrors the three-layer control architecture used in humanoid robots, as shown in Figure6c. In this model, human behavior results from multiple loops operating concurrently. The mathematical models that describe these phenomena can be simplified into motor control models. In the proposed representation, the hierarchical nature of motor control, analogous to that of humanoid robots, includes three key components: a trajectory planning layer responsible for translating objectives into whole-body trajectories, a trajectory adjustment layer that fine-tunes these trajectories based on sensory feedback and reduced models, and a trajectory control block that generates control inputs for the actuators/muscles. The model of the human central nervous system shares these key components with the humanoid robot’s physical intelligence while, the peripheral nervous system model manages local actions, such as muscle activity at the joints and sensory processing. This symmetry between human and robot physical intelligence enables seamless integration of the human model into the humanoid robot control architecture. 

#### **4.1.3 Parametrized human-robot coupled dynamics** 

The proposed framework requires a description of the dynamics of the whole system accounting for the interaction among multiple agents. For the sake of simplicity, and to guarantee the feasibility of experimental validation, we will restrict the discussion to the case where two agents manipulate a single rigid body object, as represented in Figure 6. In this section, we will use the subscript _R_ , _H_ , _o_ to refer, respectively, to the robot, human, and object quantities. The dynamics of each agent, considered in isolation, is described by dynamics description in Equation (4) and the holonomic constraints in Equation (4b), with or without the parametrization w.r.t. hardware parameters. During physical collaboration, multiple contact points are present, and forces are exchanged both with the environment and between the agents and the payload. For this reason, constraints on the contact point with the environment _J_<sup>_e_</sup> _ν_ = 0 and those of the agent-payload contact point for each agent _JR_<sup>_iνR_=</sup><sup>_J_</sup> _o_<sup>_iνo_,</sup><sup>_J_</sup> _H_<sup>_iνH_=</sup><sup>_J_</sup> _o_<sup>_iνo_</sup> must be taken into account as system constraint. In addition, the _action reaction_ property for internal forces must be considered, i.e. _fR_<sup>_i_=</sup><sup>_−f_</sup> _o_<sup>_if_</sup> _H_<sup>_i_=</sup><sup>_−f_</sup> _o_<sup>_i_. This leads to the definition of the following constraint dynamics:</sup> 


where **Q** is a coupling matrix combining contact point Jacobians, and **f** contains all the internal and external wrenches exchanged by the agents. By identifying with bold the composite matrices, we can write Equation (7), in its compact form as: 


21 

#### **4.1.4 Reduced models** 

When considering locomotion on flat terrain (i.e. assuming unilateral planar contacts with no slipping nor tilting), the full floating-base parametrized dynamics is not necessary for control design, and template models suffice. Typically, those models are derived using Newton-Euler balance of forces and moments equations. One such model is Orin’s centroidal dynamics; equations describing the evolution in time of the aggregate linear and angular momentum of all links referred to the robot center of mass - CoM, and oriented as the inertial frame due to contact forces and other external perturbations [42]. These equations read as: 


in which Equation (9a) describes the dynamics of the CoM position as a function of the robot mass _m_ and its aggregate momentum _Gh_ through a selector matrix _C_ = �I3 03�. Similarly, Equation (9b) describes the dynamics of the aggregate momentum _Gh_ as a function of the 6D gravity vector _g_ , and the balance of external contact forces _fi_ and perturbations _di_ , and their locations _pi, pdi_ respectively. In addition, to simulate whether a given contact force at the feet _fi_ is _active_ or not during stepping, and following [16], we considered the contact locations _pi_ as continuous variables with the following dynamics 


where _vi_ is the contact velocity. 

### **4.2 Optimization of humanoid robot design for ergonomic human-robot collaboration** 

In this section, we present details about the implementation of the architecture depicted in Figure 2a, which results in the ergoCub optimal hardware, as presented in Section 2.1. To identify the morphology of the ergoCub robot, we formulated the optimization problem as per Equation (11). 


The optimization problem search variables is defined as **_y_** = � **_q_** ˜ _π_ � _T_ where _π_ are the robot link lengths, and **_q_** ˜ are the human and robot configurations associated with different load heights. ˜ _·_ represents a set of variables. In this optimization problem, we leveraged the parametrized coupled dynamics of human-robot-load of Equation (8), but considering only the robot link lengths as hardware parameters, thus disregarding the link densities. Following the same convention of Section 4.1.3, we identify the agents configuration with **_q_** and the agents’ configuration velocity with **_ν_** . The interaction wrenches are identified with **_f_** and with **_Q_** we defined the coupling matrix that considers both the constraints of the contact with the environment and those exerted in between the agents. The human and robot internal joint torques **_τ_** are incorporated into the system dynamics via a constant selector matrix 

22 

**_B_** meanwhile with **M** we refer to the coupled mass matrix and **h** accounts for the Coriolis and gravity effects. In the formulation of the optimization problem, in addition to the coupled dynamics of Equation (11a), we integrated several constraints to ensure task feasibility. These encompass kinematic constraints (Equation (11c)) to maintain the correct load orientation and height, as well as to position the hands and feet appropriately for both agents during the task. Additionally, we impose contact constraints (Equation (11b)) and static conditions (Equation (11d). Our goal was to find the set of optimum robot link lengths _π_<sup>_∗_</sup> to improve collaborative and walking task performances. For this reason, we formulated three tasks weighted by _W_ 1 _, W_ 2 _, W_ 3 _∈_ R<sup>+</sup> . For the ergoCub optimization, the chosen values were _W_ 1 = 10<sup>5</sup> , _W_ 2 = 10<sup>10</sup> , and _W_ 3 = 1. To improve the walking performances we lifted 2 the robot center of mass by adding in the cost function the task _T_ 3 = <u>1</u> ��� _I pz_ 0 _,com_ ���2<sup>where</sup><sup>_Ipz_0</sup><sup>_,com_istherobot</sup> center of mass height computed at null configuration. To improve the human-robot collaboration, we improve the ergonomy of the interaction in the form of agents energy expenditure. A measure of the agents energy expenditure is the norm of both agent joint torque. For this reason, we add two tasks minimizing the agents joint torque, i.e. _T_ 1 = �� _SR_ **_τ_** ( **_q_** _, π_ )��22<sup>and</sup><sup>_T_2=</sup> �� _SH_ **_τ_** ( **_q_** _, π_ )��22<sup>,with</sup><sup>_SR, SH_areselectormatrixforrobotandhumantorque</sup> respectively. **_τ_** ( **_q_** _, π_ ) is computed by projecting the dynamics of Equation (8) into the holonomic constraints, thus obtaining Equation (12) with **_N_** _λ_ ( **_q_** _, π_ ) defined as Equation (13) (where the dependency on **_q_** and _π_ has been omitted for the sake of conciseness). 


Equation (12), is then used to express the relationship between the agents joint torques and the search variable _y_ = � **_q_** ˜ _π_ � _T_ at static configurations and considering a minimum norm solution, leading to the following relationship: **_τ_** ( _y_ ) = � **_N_** Λ( **_q_** _, π_ ) **_B_** � _†_ **_N_** Λ( **_q_** _, π_ ) **_g_** ( **_q_** _, π_ ), with **_g_** ( **_q_** _, π_ ) accounting for the gravity effects only. This computation enables to constraint the optimization problem to the parametrized couple dynamics without explicitly incorporating it into the optimization problem constraints, avoiding potential computational issues. This torque relationship is also used in the analysis of the optimization outcomes presented in Section 2.1. Specifically, the human joint torque values reported in Figure 3 (e) are computed using this formulation. 

### **4.3 Physical intelligence** 

In this section, we present details about the implementation of the control framework used in the architecture proposed in Section 2.2. In such an architecture instance, we developed trajectory control, adjustment, and planning blocks that consider the influence of a human companion while keeping the hardware parameters fixed to the optimal values obtained in the previous instance. The ultimate goal is to generate instances of the trajectory blocks that incorporate human representation and achieve partner awareness. Starting from the dynamics of Equation (8), it is possible to derive a set of control inputs _u_<sup>_∗_</sup> , i.e. joint torques **_τ_** and contact forces **f** , defining trajectory blocks, able to achieve the desired task while minimizing both human and robot metrics, and considering the optimum set of hardware parameters _π_<sup>_∗_</sup> . 


In addition, the same architecture can be used, disregarding the human, to achieve other behaviors, like walking robustly, as exemplified in the ergoCub robot physical intelligence, presented in Section 2.2. In the following section, we will delve into the definition of each block that composes the architecture physical intelligence, which 

23 

is organized as a cascade control architecture, hence composed of the _trajectory control_ , _adjustment_ , and _planning_ blocks. We will delve into both the collaborative and locomotion control architectures. The proposed architectures builds upon prior work conducted on the iCub[59] and iCub3[34] humanoid robots. Collaborative controllers developed for the iCub facilitated human-robot collaboration with the concept of assistance [60] and allowed for robot-robot collaborative lifting [61]. With the iCub3, we incorporated the modeling of the human balancing system into the collaborative controller [48]. Regarding locomotion controllers, the initial architecture designed for the iCub employed predictive control on the robot Zero Moment Point (ZMP) [62], which subsequently evolved with the application of Centroidal Model Predictive Control (MPC) on the iCub3 robot [16, 63]. With the introduction of the ergoCub robot, we have further refined and adapted these controllers to suit the ergoCub-specific features that arise from the performed hardware optimization. In the following section, we will see in detail the control architectures employed for performing human-robot collaboration (Section 4.3.1) and locomotion (Section 4.3.2) on the ergoCub humanoid robot. 

#### **4.3.1 Human-robot collaboration-payload lifting task** 

In this Section, we will hover over the main blocks that compose the human-robot collaboration architecture visually depicted in Figure 6(c). The description of the employed control framework can be decomposed into the description of _trajectory control_ , _trajectory adjustment_ , and _trajectory planning_ blocks. **Trajectory control** The trajectory control represents the inner loop of the control framework preceding the low-level control of the actuators. It demands both a high frequency and a comprehensive system model, consequently, predictive horizons need to be sacrificed while instantaneous control is employed. Given reference robot joints trajectory ( _s_<sup>_r_</sup> _R_<sup>_,s_˙</sup><sup>_r_</sup> _R_<sup>_,_¨</sup><sup>_sr_</sup> _R_<sup>)</sup> or task-space robot reference trajectories ( _x_<sup>_r_</sup> _R,n_<sup>_,x_˙</sup><sup>_r_</sup> _R,n_<sup>_,_¨</sup><sup>_xr_</sup> _R,n_<sup>),itisrequiredtodesignacontrollawthatdefines</sup> the actuation command based on the dynamics model of the system. In the human-robot collaboration task, the robot is actuated through joint torques _τR_ , in this way, it can be _compliant_ , as usually is the case for HumanRobot interaction [64]. We employed a task-space inverse dynamics approach [65], together with the coupled human-robot dynamics of Equation (8), thus considering the human-robot mutual influence, and we formulate the trajectory control as a linear constrained optimization problem: 


where _π_<sup>_∗_</sup> is the optimal set of hardware parameters, identified as explained in Section 4.2 and the subscript _R_ highlights that the quantities are robot-related. To achieve task-space tracking, we use the following: 


Similarly, for joint tracking, we use: 


These equations ensure the tracking of desired tasks when _Kd_ , _Kp_ , _KI_ , _kd_ , and _kp_ are diagonal positive definite matrices. The constrained optimization problem in Equation (15) involves both quadratic and linear functions, enabling efficient online solutions at high frequencies by exploting QP. **Trajectory adjustment** While tracking 

24 

a pre-computed trajectory can enable the achievement of simple tasks in controlled environments, the presence of collaborative agents necessitates the adjustment of the trajectory for dynamical adaptation to the surroundings. In this case, we are interested in adjusting the time evolution of the planned trajectory, while we are not modifying the trajectory _per se_ . We have previously explored the idea of parametrizing the trajectory for human-robot collaboration in [66] and [48]. Starting from the latter, we proposed an updated version of trajectory parametrization for collaborative lifting, which further promotes ergonomics collaboration. The reference robot configuration _s_<sup>_r_</sup> _R_<sup>(</sup><sup>_t_)</sup> for determining the motor control input of the trajectory control block, as per Equation (15), is computed using Equation (18). 


Therefore, _s_<sup>_r_</sup> _R_<sup>isdefinetomovefromajointconfiguration</sup><sup>_s_1to</sup><sup>_s_2anditisregulatedbyafreeparameter,</sup><sup>_ψ_=</sup> _ψ_ ( _t_ ) _∈_ [0 _,_ 1]. To regulate the evolution of the free-parameter, we need to define a task-specific quantity that acts as a master. In the case of collaborative lifting, this corresponds to the motion of the human hands which should be followed by the robot motion. In synthesis, we obtain a desired robot hands velocity and we use it to regulate the free parameter: 


where _zH_ and _zR_ are respectively the height of the human and the robot hand, _Js_<sup>_z_is the component of the robot</sup> hand jacobian associated with the velocity along the z-axis, and _kψ ∈_ R<sup>+</sup> is a gain that determines the robot reactivity in following human hand motion. The robot, therefore, will be governed by the human action as per Equation (19) only inside the range _s_ 1 _, s_ 2 meanwhile it will not move outside such a range. **Trajectory planning** In trajectory planning, starting from the desired height range the load should be manipulated, we computed two references initial _s_ 1 and final _s_ 2 joint configuration, solving an Inverse Kinematic problem. These reference joint positions, _s_ 1 and _s_ 2, are then employed in the trajectory adjustment block, as described in Equation (19) . 

#### **4.3.2 Locomotion** 

Also for the locomotion control, we employed a hierarchical control architecture defined by the trajectory control, adjustment and planning blocks. **Trajectory control** As is usual by now, this block is aimed at providing direct inputs to the low level actuators control. For the locomotion behavior, we have two different trajectory blocks, depending if the low level input are joint torques or positions. When the input is joint positions, as for the ergoCub robot locomotion instance, the reference joint positions _s_<sup>_r_</sup> _R_<sup>are evaluated through a QP-based inverse kinematics</sup> module and they are passed to the actuator low-level motor control boards [43]. In this instance, a _stack of tasks_ is employed in which tracking of the feet poses and the CoM position is treated as a _hard_ constraint, while the torso orientation is treated as a cost term. In this sense, at each time step one solves: 


where in this formulation, the optimization variable is the robot velocity _νR_ , and the feedback is obtained by integrating the desired quantities. The hessian matrix and gradient vector _H, g_ are obtained from the torso and joints regularization tasks respectively, while the constraint matrices _A, b_ and robot joint velocity lower and upper limits _s_ ˙ _R,ℓ, s_ ˙ _R.u_ are obtained from the jacobians associated with the velocity of the CoM and feet, together with actuator limits respectively. **Trajectory adjustment** Also in the locomotion case, a trajectory adjustment block is needed, since complex tasks — such as creating and removing contacts — necessitate the adjustment of the trajectory for 

25 

dynamical adaptation to the surroundings. To achieve this, simplified models with lower computational costs are employed, eventually allowing for the inclusion of a prediction horizon. In our case we utilized Model Predictive Control (MPC) which allows finding the system state **_x_** and control input **_u_** over a defined time horizon. In [16], it was proposed the centroidal MPC, which can adjust online the trajectory of a humanoid robot during locomotion, and further improved in [63] for locomotion with payloads. The tasks considered in the loss function are the position of the contact points, rate of change of the feet impact wrenches, angular momentum tracking, and symmetry in the feet impact wrenches. More in detail, and starting from the dynamical system (Equation (9)), we aim to adjust the feet contact locations and timings solving the following optimization problem via receding horizon [67] over _np ≥_ 1 future time steps; 


where at the current time step _k_ and with a sampling period ∆ _T_ we have; 

- Equation (21a) describes the function to be minimized, comprising: _TGh_ a term penalizing the _L_ 2-norm of the error between the desired and current CoM position _pCoM_ and aggregate momentum. Similarly _Tf , Tp_ regularizes the contact forces at the feet vertices ( _fi_ ) to be as similar as possible and minimizes the tracking error of the footsteps contact locations _pi_ respectively. _WGh, Wf , Wp ∈R_<sup>+</sup> are weights. 

- Equation (21b-21d) describes the Euler discretization of the centroidal dynamics and contact position dynamics described in (9)-(10) respectively. 

- Equation (21e - 21f) describe the constraints restricting the obtained optimal co-planar contact forces _fi_ to be _feasible_ [68], i.e. in the sense of lying in the interior of the friction cone, and the maximum allowable contact location tracking error within given bounds _ℓb, ub_ respectively. 

The outputs of the above are: adjusted (given feedback and estimates of the presence of disturbances) trajectories for the CoM, the footsteps locations, and their timings. This is then passed to the whole-body trajectory control layer. **Trajectory planning** For the walking task, the trajectory planning block generates nominal footstep and CoM trajectories for the centroidal MPC block. Such references are generated either starting from user inputs, given via a remote controller and employing an optimal control based trajectory planner (https://github.com/robotology/unicycle-footstep-planner). 

## **Appendix A Collaborative walking with payload** 

To further validate the ergoCub hardware design in human–robot collaboration, we performed an additional experiment in which a human and the robot walk together while carrying a payload, as illustrated in Figure A1 (a). The control architecture was the same as that used for locomotion in Section 2.2, with the addition of two constraints: 

26 

i) the robot was commanded to maintain a constant distance from the human, and ii) an inverse kinematics task was added to ensure that the robot’s hand maintained contact with the payload. It is important to note that in this setup, the robot’s physical intelligence does not incorporate human ergonomic metrics or an explicit representation of the human partner. The purpose of these experiments is instead to assess the suitability of the robot’s hardware design for collaborative interaction, given that the design was optimized with respect to both walking and human–robot collaboration tasks. In the experiments, the human and robot jointly carried a 2 kg payload in two trials lasting 130 and 160 seconds, respectively Which is 4 times longer than the collaborative payload lifting experiments. Additionally, these experiments were conducted with a different operator than in the collaborative lifting study. The human participant wore the iFeel suit to capture ergonomic data. Figure A1 (c) reports the measured torques at the human lower back (L5S1), computed using the same methodology described in Section 2.2. The signals were smoothed using a moving average filter with a window size of 20. Figure A1 (d) summarizes the mean and maximum torque values observed during the two tasks. The mean torque was consistent across both trials (approximately 14 Nm), while the maximum values differed slightly. These peaks are likely due to transient stress events (e.g., momentary misalignment of the payload), which is expected since the robot did not actively regulate ergonomics in this scenario, and the payload was grasped only through an additional task in the inverse kinematics. As expected, the maximum torque recorded in these experiments was higher than in the collaborative payload lifting of Section 2.2. However, it is important to account for inter-subject variability: in this experiment, the human participant was taller (180 cm vs. 173 cm) and heavier (80 kg vs. 65 kg) than the subject in the lifting experiments, which naturally shifts the threshold for critical back stress. Overall, these results indicate that collaborative walking with payload is feasible, and the recorded ergonomic metrics show good repeatability (comparable mean L5S1 torque across two trials) even in longer-duration interactions. This experiment complements the collaborative lifting study by validating that the ergoCub hardware design supports robust and repeatable human–robot collaboration across different tasks, durations, and human partners. 

## **Appendix B Comparison between iCub3 and ergoCub for human–robot collaboration** 

To further validate the proposed framework, we extend our analysis of the human–robot collaboration task by comparing the performance of the ergoCub robot with that of iCub3. Indeed, while both are humanoid robots, iCub3 was not optimized for collaborative payload lifting, although it has been used for such tasks, as reported in [48]. Unfortunately, detailed information on human ergonomic metrics, such as internal joint stress or torque, was not recorded during the iCub3 experiments; therefore, direct ergonomic comparisons are not possible. However, a clear distinction arises in terms of operational load height range: iCub3 was tested between 0 _._ 40 m to 0 _._ 75 m, whereas ergoCub has been validated across the range of 0 _._ 8 m to 1 _._ 2 m. To assess the ergonomic value of the load range, we computed the lower back stress across multiple human models holding loads at different heights. Specifically, we considered eight different human models, defined according to the methodology in [39], representing individuals of varying sex, height, and weight. The physical characteristics of these models are summarized in Figure B1 and are publicly available at: https://github.com/robotology/human-gazebo.git. To assess how load height influences human effort during static load holding, we sampled a range of heights from 0 _._ 4 m to 1 _._ 8 m with a step of 0 _._ 05 m. For each combination load height _i_ and human model _j ∈{_ Human1 _, · · ·_ Human8 _}_ we solved the optimisation problem of Equation (B1). This problem computes the optimal configuration _qj_ that minimizes joint torque _τ_ ( _qj_ ) under static conditions ((B1d), (B1e)), while satisfying system dynamics ((B1a)), holonomic constraints (B1b) and load placement constraint (B1c). 


27 

_Hi,j_ = _Hi,j_<sup>_∗,_</sup> (B1c) _ν_ ˙ _j_ = 0 _,_ (B1d) _νj_ = 0 _._ (B1e) 

As an ergonomic indicator, we extracted the average torque at the L5–S1 spinal joint, a commonly used metric for evaluating lumbar stress during lifting tasks. The results were then averaged across all eight human models to compute the mean and standard deviation at each height. Since the torque values are computed under static assumptions and serve as an indicative stress index rather than absolute measurements, we normalized all results by the maximum observed torque, producing a dimensionless stress profile across the tested height range This allows us to identify load height intervals that are more or less ergonomically favorable, as shown in Figure B1. The analysis reveals that maximum back stress occurs at the lowest tested height of 0 _._ 4 m. As the height increases, the stress decreases sharply, reaching a minimum around 0 _._ 8 m. Between 0 _._ 8 m and 1 _._ 1 m, the stress remains relatively low and stable, forming a plateau with low standard deviation. Beyond 1 _._ 1 m, the stress begins to rise again, accompanied by greater inter-subject variability up to approximately 1 _._ 7 m. At 1 _._ 8 m, the stress slightly decreases once more together with the standard deviation, as this height corresponds to full extension for shorter individuals, while remaining within a comfortable range for taller ones. The larger standard deviation observed in the 1 _._ 1 m to 1 _._ 7 m range reflects how ergonomic favorability in that region is highly dependent on individual anthropometrics. In contrast, the 0 _._ 8 m to 1 _._ 2 m range exhibits both low stress and low variance, indicating a robust ergonomic spot across diverse users. Notably, this height interval aligns precisely with the range in which ergoCub is able to collaborate effectively, as demonstrated in the main experimental results. Conversely, iCub3’s collaboration range is limited to the lower part of the spectrum (0 _._ 40 m to 0 _._ 75 m), which corresponds to the least ergonomically favorable region. It is important to note that these ranges of feasible load heights are not manually selected but are instead determined by the robot’s hardware, and in the case of ergoCub, by the outcome of the hardware optimization process. This dependence extends beyond the robot’s overall height and includes the robot’s morphological proportions, such as the relative lengths of the legs, torso, and arms. For example, a robot that is tall overall but has relatively short arms or torso may struggle in reaching loads placed at medium heights. This analysis shows that hardware optimization under shared embodied intelligence principles allows ergoCub to extend collaboration capabilities while better aligning with human ergonomics across diverse users. 

## **Appendix C Comparison between iCub3 and ergoCub for locomotion** 

We compare the capabilities of ergoCub with the iCub3 humanoid robot [34], a widely utilized platform in various applications including telexistence [34], walking [16], and collaborative tasks with humans [48], which was the starting point for the development of the ergoCub robot. The iCub3 and ergoCub robot are depicted together in Figure C1. We conducted experiments campain using real hardware where both iCub3 and ergoCub robots were tested in a locomotion task simultaneously, receiving identical user inputs and implementing the same control architecture as outlined in [34]. For each platform, the control feedback gains were hand-tuned separately to achieve the best locomotion performance, ensuring that the comparison focuses on morphological differences rather than being influenced by a single set of parameters shared across both robots. The goal was to assess and compare their performance in dynamic walking tasks. In Figure C1 (b), we present the trajectories of the Center of Mass (CoM) in the x and y directions during both forward and lateral walking tasks. The data reveals that, despite starting from the same initial position, ergoCub consistently outpaces iCub3 in both directions. In addition, by looking at Figure C1 (c), it can be noticed that, despite the higher velocity, the ergoCub robot requires lower currents. Indeed the mean of the norm of the current of ergoCub and the standard deviation is lower with respect to the one of iCub3. This difference in velocity can be attributed to ergoCub’s optimized design and shows evidence of the ergoCub’s improved capability. 

28 

## **Appendix D Acceptability of the ergoCub Robot** 

As introduced in Section 1, the ergoCub robot was conceived for close-proximity collaboration in industrial and healthcare domains, where ergonomics and safe physical interaction are critical. In this Appendix, we report a user study that provides complementary insight into the perceived acceptability of the resulting humanoid platform when deployed in contexts where humans and robots interact closely. In such scenarios, perceived trustworthiness and comfort can influence real-world adoption. It is worth noting that this study is not directly related to the primary focus of this work, which is the methodological framework for optimizing robot hardware and physical intelligence with respect to human-centered ergonomic metrics. Rather, it provides additional perspective on one of the tangible outcomes of the proposed framework, namely the ergoCub robot. We conducted a user study to assess the acceptability of ergoCub’s design and its simplified facial expressions, which provide ergonomic feedback during interaction (see Section 2.2). The study was run in collaboration with Ipsos (https://www.ipsos.com/en) and involved a total of 850 participants: 500 from the manufacturing sector and 350 from healthcare. Respondents were recruited via Computer-Assisted Personal Interviews (CAPI) and Computer-Assisted Web Interviews (CAWI). Each participant was asked to: 

- Rate the overall appeal of four robots: NAO[69], Baxter[37], R1[38], and ergoCub, on a 0–10 scale. 

- Report the emotions evoked by each of the four robot designs (positive: interest, pleasantness, joy; negative: discomfort). 

- Indicate preferences among four styles of robot facial expression: simplified, avatar, emoji, or abstract (Figure D3). 

Results in the manufacturing domain (Figure D1) showed that NAO received the highest average rating (7.0), followed by ergoCub (6.7), R1 (6.0), and Baxter (5.2). Importantly, ergoCub outperformed Baxter, a widely adopted collaborative robot, and R1, which lacks locomotion and humanoid proportions. NAO elicited slightly more positive emotions (25%) than ergoCub (23%), but both robots showed similarly low levels of negative affect (around 10%), suggesting broad neutrality or acceptance rather than rejection. Results in healthcare (Figure D2) followed the same trend: NAO again ranked first (6.5), followed by ergoCub (6.0), R1 (5.3), and Baxter (4.3). Absolute scores were lower across all robots, reflecting a more critical stance among healthcare professionals, but the relative ranking remained unchanged. Emotional responses mirrored the manufacturing domain, with ergoCub and NAO eliciting comparable levels of positive affect. From these findings, we conclude that although NAO was the most liked robot overall, its lack of suitability for physical collaboration means that ergoCub is the most accepted option among robots capable of direct physical interaction with humans. Baxter, despite being a benchmark collaborative platform, consistently ranked lowest, underscoring the importance of humanoid form and mobility for user acceptability. For what concern facial expression (Figure D3), simplified facial expressions, as implemented in ergoCub, were consistently preferred over more complex or abstract alternatives, thereby validating our design choice for ergonomic feedback. Taken together, these results indicate that ergoCub achieves a favorable balance between functional capability and user acceptability, reinforcing its potential for deployment in both industrial and healthcare settings. 

## **Appendix E Wearable technology** 

As depicted in Figure E1, wearable sensors are used to update human kinematics and estimate ergonomics during the human robot interaction of Section 2.2. The setup includes: a set of IMU-based iFeel Nodes [70], which estimate the relative orientation of the limbs; the iFeel Shoes [70], which embed Force/Torque (FT) sensors in the soles to measure ground reaction forces; and VIVE trackers (https://www.vive.com/eu/accessory/tracker3/), mounted on the feet, hands, and waist, providing absolute pose data. These sensor measurements are integrated online to estimate human kinematics and joint torques, updating the internal human representation within the robot’s physical intelligence for collaboration. 

29 


**Fig. A1** : Human–robot collaborative walking with payload. (a) The ergoCub robot walking together with a human while carrying a payload. (b) Avatar representation of the human companion. (c) Estimated L5S1 joint torques during collaborative walking for the two trials. (d) Mean and maximum torque values measured on the human participant during collaboration. 

30 


**Fig. B1** : Human model characteristics and normalized L5–S1 spinal torque demand as a function of load height. (a) Main characteristics of the human models used for the ergonomics analysis. (b) Relative L5–S1 torque demand (mean ± standard deviation across simulated human models) as a function of target load height. All values are normalized such that the maximum observed spinal torque corresponds to 1. The shaded area represents the standard deviation across the different human models. 

31 


**Fig. C1** : Comparison between the ergoCub robot and iCub3. The ergoCub and iCub3 robots walking together (a). Comparison of Center of Mass (CoM) trajectories for both robots (b). Mean and standard deviation of the current norm during the walking task for ergoCub and iCub3 (c). 

32 

|Emotion|1|2|3|4|5|Emotion|1|2|3|4|5|
|---|---|---|---|---|---|---|---|---|---|---|---|
|Interest|9%|10%|29%|29%|23%|Interest|7%|11%|26%|31%|25%|
|Pleasantness|13%|13%|33%|25%|16%|Pleasantness|9%|13%|30%|28%|20%|
|Joy|21%|18%|31%|18%|12%|Joy|17%|20%|30%|19%|14%|
|Sadness|45%|21%|16%|7%|11%|Sadness|46%|20%|13%|10%|11%|
|Anxiety|40%|20%|19%|11%|10%|Anxiety|43%|21%|16%|12%|8%|
|Fear|48%|21%|14%|7%|10%|Fear|52%|19%|12%|9%|8%|
||(a)|ergoCu|b.||||(|b) NAO.||||
|Emotion|1|2|3|4|5|Emotion|1|2|3|4|5|
|Interest|10%|15%|30%|26%|19%|Interest|10%|15%|30%|26%|19%|
|Pleasantness|14%|21%|28%|24%|13%|Pleasantness|14%|21%|28%|24%|13%|
|Joy|23%|20%|28%|19%|10%|Joy|23%|20%|28%|19%|10%|
|Sadness|40%|23%|16%|9%|12%|Sadness|40%|23%|16%|9%|12%|
|Anxiety|37%|22%|18%|13%|10%|Anxiety|37%|22%|18%|13%|10%|
|Fear|45%|24%|14%|9%|8%|Fear|45%|24%|14%|9%|8%|
|||(c) R1.|||||(d|) Baxter|.|||


|Robot|0–3|4–5|6|7|8–10|Average|
|---|---|---|---|---|---|---|
|Baxter|25%|22%|18%|11%|24%|5.3|
|R1|16%|19%|19%|17%|29%|6.0|
|ergoCub|10%|14%|16%|21%|39%|6.7|
|Nao|8%|11%|12%|19%|50%|7.0|


(e) Rate robot appeal. 

**Fig. D1** : Comparison of robot acceptability results in the manufacturing domain. Figures (a–d) report the percentage of responses to the question: _“On a scale from 1 (not at all) to 5 (completely), to what extent does the robot image evoke the following sensations?”_ . Figure (e) reports the responses to the question: _“On a scale from 1 (not at all) to 10 (completely), how much do you like the robot design?”_ . 

33 

|Emotion|1|2|3|4|5|Emotion|1|2|3|4|5|
|---|---|---|---|---|---|---|---|---|---|---|---|
|Interest|11%|19%|31%|23%|16%|Interest|8%|16%|29%|27%|20%|
|Pleasantness|20%|20%|30%|19%|11%|Pleasantness|14%|16%|28%|24%|18%|
|Joy|27%|26%|27%|12%|8%|Joy|27%|23%|24%|18%|8%|
|Sadness|39%|21%|16%|13%|11%|Sadness|44%|19%|17%|10%|10%|
|Anxiety|34%|24%|20%|15%|7%|Anxiety|41%|23%|18%|12%|6%|
|Fear|46%|21%|21%|7%|5%|Fear|52%|21%|17%|6%|4%|
||(a)|ergoCu|b.||||(|b) NAO.||||
|Emotion|1|2|3|4|5|Emotion|1|2|3|4|5|
|Interest|16%|18%|31%|23%|12%|Interest|23%|19%|24%|25%|9 %|
|Pleasantness|26%|23%|27%|17%|7%|Pleasantness|35%|25%|23%|13%|4%|
|Joy|33%|24%|26%|12%|5%|Joy|40%|23%|23%|10%|4%|
|Sadness|34%|24%|17%|16%|9%|Sadness|33%|21%|18%|14%|14%|
|Anxiety|31%|24%|20%|16%|9%|Anxiety|22%|19%|26%|19%|14%|
|Fear|41%|27%|16%|8%|8%|Fear|38%|21%|21%|13%|7%|
|||(c) R1.|||||(d|) Baxter|.|||


|Robot|0–3|4–5|6|7|8–10|Average|
|---|---|---|---|---|---|---|
|Baxter|45%|17%|12%|11%|24%|4.3|
|R1|29%|20%|13%|13%|29%|5.3|
|ergoCub|18%|22%|12%|16%|32%|6.0|
|Nao|15%|14%|12%|21%|38%|6.5|


(e) Rate robot appeal. 

**Fig. D2** : Comparison of robot acceptability results in the healthcare domain. Figures (a–d) report the percentage of responses to the question: _“On a scale from 1 (not at all) to 5 (completely), to what extent does the robot image evoke the following sensations?”_ . Figure (e) reports the responses to the question: _“On a scale from 1 (not at all) to 10 (completely), how much do you like the robot design?”_ . 

34 


(a) 

|**Expression**|**Manufacture (%)**|**Healthcare (%)**|
|---|---|---|
|Simplified|36%|41%|
|Avatar|30%|31%|
|Emoji|24%|24%|
|Abstract|10%|4%|


(b) 

**Fig. D3** : Acceptability of ergoCub facial expression. (a) The different facial expression considered. (b) Comparison of preferred facial expression styles in the manufacturing and healthcare domains. Participants answered the question “Which facial expression do you prefer?”. 

35 


**Fig. E1** : The human and the robot collaborate to move a load. The figure highlights the non-intrusive sensors worn by the human and the corresponding measurements they provide. The human wears several iFeel Node sensors (blue markers) placed on the arms and legs, which provide IMU measurements. VIVE trackers (green markers) are mounted on the feet (on top of the iFeel Shoes), wrists, and waists to capture the absolute pose of the human body segments. The iFeel Shoes (highlighted in orange) are equipped with force/torque (FT) sensors embedded in the soles to measure ground reaction forces. 

36 

## **References** 

- [1] Cordoni, G., Palagi, E.: Back to the future: A glance over wolf social behavior to understand dog–human relationship. Animals **9** (11), 991 (2019) 

- [2] Fenton, V.: The use of dogs in search, rescue and recovery. Journal of Wilderness Medicine **3** (3), 292–300 (1992) 

- [3] Morris, S.C.: Life’s solution: inevitable humans in a lonely universe (2003) 

- [4] Wilson, R.A., Foglia, L.: Embodied cognition. Stanford encyclopedia of philosophy (2011) 

- [5] Wilson, A.D., Golonka, S.: Embodied cognition is not what you think it is. Frontiers in psychology **4** , 58 (2013) 

- [6] Geyer, H., Herr, H.: A muscle-reflex model that encodes principles of legged mechanics produces human walking dynamics and muscle activities. IEEE Transactions on Neural Systems and Rehabilitation Engineering **18** (3), 263–273 (2010) https://doi.org/10.1109/TNSRE.2010.2047592 

- [7] Nunn, C.L., Ezenwa, V.O., Arnold, C., Koenig, W.D.: Mutualism or parasitism? using a phylogenetic approach to characterize the oxpecker-ungulate relationship. Evolution **65** (5), 1297–1304 (2011) 

- [8] Gu, Z., Li, J., Shen, W., Yu, W., Xie, Z., McCrory, S., Cheng, X., Shamsah, A., Griffin, R., Liu, C.K., et al.: Humanoid locomotion and manipulation: Current progress and challenges in control, planning, and learning. IEEEASME transactions on mechatronics (2025) 

- [9] Team, T.L., Barreiros, J., Beaulieu, A., Bhat, A., Cory, R., Cousineau, E., Dai, H., Fang, C.-H., Hashimoto, K., Irshad, M.Z., Itkina, M., Kuppuswamy, N., Lee, K.-H., Liu, K., McConachie, D., McMahon, I., Nishimura, H., Phillips-Grafflin, C., Richter, C., Shah, P., Srinivasan, K., Wulfe, B., Xu, C., Zhang, M., Alspach, A., Angeles, M., Arora, K., Guizilini, V.C., Castro, A., Chen, D., Chu, T.-S., Creasey, S., Curtis, S., Denitto, R., Dixon, E., Dusel, E., Ferreira, M., Goncalves, A., Gould, G., Guoy, D., Gupta, S., Han, X., Hatch, K., Hathaway, B., Henry, A., Hochsztein, H., Horgan, P., Iwase, S., Jackson, D., Karamcheti, S., Keh, S., Masterjohn, J., Mercat, J., Miller, P., Mitiguy, P., Nguyen, T., Nimmer, J., Noguchi, Y., Ong, R., Onol, A., Pfannenstiehl, O., Poyner, R., Rocha, L.P.M., Richardson, G., Rodriguez, C., Seale, D., Sherman, M., SmithJones, M., Tago, D., Tokmakov, P., Tran, M., Hoorick, B.V., Vasiljevic, I., Zakharov, S., Zolotas, M., Ambrus, R., Fetzer-Borelli, K., Burchfiel, B., Kress-Gazit, H., Feng, S., Ford, S., Tedrake, R.: A Careful Examination of Large Behavior Models for Multitask Dexterous Manipulation (2025). https://arxiv.org/abs/2507.05331 

- [10] Cardenas-Perez, C., Romualdi, G., Elobaid, M., Dafarra, S., L’Erario, G., Traversaro, S., Morerio, P., Del Bue, A., Pucci, D.: Xbg: End-to-end imitation learning for autonomous behaviour in human-robot interaction and collaboration. IEEE Robotics and Automation Letters (2024) 

- [11] NVIDIA, :, Bjorck, J., Casta˜neda, F., Cherniadev, N., Da, X., Ding, R., Fan, L.J., Fang, Y., Fox, D., Hu, F., Huang, S., Jang, J., Jiang, Z., Kautz, J., Kundalia, K., Lao, L., Li, Z., Lin, Z., Lin, K., Liu, G., Llontop, E., Magne, L., Mandlekar, A., Narayan, A., Nasiriany, S., Reed, S., Tan, Y.L., Wang, G., Wang, Z., Wang, J., Wang, Q., Xiang, J., Xie, Y., Xu, Y., Xu, Z., Ye, S., Yu, Z., Zhang, A., Zhang, H., Zhao, Y., Zheng, R., Zhu, Y.: GR00T N1: An Open Foundation Model for Generalist Humanoid Robots (2025). https://arxiv.org/abs/ 2503.14734 

- [12] Feng, S., Whitman, E., Xinjilefu, X., Atkeson, C.G.: Optimization-based full body control for the darpa robotics challenge. Journal of field robotics **32** (2), 293–312 (2015) 

37 

- [13] Viceconte, P.M., Camoriano, R., Romualdi, G., Ferigo, D., Dafarra, S., Traversaro, S., Oriolo, G., Rosasco, L., Pucci, D.: Adherent: Learning human-like trajectory generators for whole-body control of humanoid robots. IEEE Robotics and Automation Letters **7** (2), 2779–2786 (2022) https://doi.org/10.1109/LRA.2022.3 141658 

- [14] Dafarra, S., Romualdi, G., Pucci, D.: Dynamic complementarity conditions and whole-body trajectory optimization for humanoid robot locomotion. IEEE Transactions on Robotics **38** (6), 3414–3433 (2022) https://doi.org/10.1109/TRO.2022.3183785 

- [15] Herzog, A., Rotella, N., Schaal, S., Righetti, L.: Trajectory generation for multi-contact momentum control. In: 2015 IEEE-RAS 15th International Conference on Humanoid Robots (Humanoids), pp. 874–880 (2015). IEEE 

- [16] Romualdi, G., Dafarra, S., L’Erario, G., Sorrentino, I., Traversaro, S., Pucci, D.: Online non-linear centroidal mpc for humanoid robot locomotion with step adjustment. In: 2022 International Conference on Robotics and Automation (ICRA), pp. 10412–10419 (2022). https://doi.org/10.1109/ICRA46639.2022.9811670 

- [17] Griffin, R.J., Leonessa, A.: Model predictive control for dynamic footstep adjustment using the divergent component of motion. In: 2016 IEEE International Conference on Robotics and Automation (ICRA), pp. 1763–1768 (2016). IEEE 

- [18] Joe, H.-M., Oh, J.-H.: Balance recovery through model predictive control based on capture point dynamics for biped walking robot. Robotics and Autonomous Systems **105** , 1–10 (2018) 

- [19] Ott, C., Roa, M.A., Hirzinger, G.: Posture and balance control for biped robots based on contact force optimization. In: 2011 11th IEEE-RAS International Conference on Humanoid Robots, pp. 26–33 (2011). https://doi.org/10.1109/Humanoids.2011.6100882 

- [20] Wensing, P.M., Orin, D.E.: Generation of dynamic humanoid behaviors through task-space control with conic optimization. In: 2013 IEEE International Conference on Robotics and Automation, pp. 3103–3109 (2013). https://doi.org/10.1109/ICRA.2013.6631008 

- [21] Nava, G., Romano, F., Nori, F., Pucci, D.: Stability analysis and design of momentum-based controllers for humanoid robots. In: 2016 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pp. 680–687 (2016). https://doi.org/10.1109/IROS.2016.7759126 

- [22] Bauer, A., Wollherr, D., Buss, M.: Human-robot collaboration: a survey. International Journal of Humanoid Robotics **05** (01), 47–66 (2008) https://doi.org/10.1142/S0219843608001303 

- [23] Haddadin, S., Croft, E.: In: Siciliano, B., Khatib, O. (eds.) Physical human-robot interaction, 2nd edn., pp. 1835–1874. Springer, . (2016). https://doi.org/10.1007/978-3-319-32552-1 ~~6~~ 9 

- [24] Rasmussen, J., Damsgaard, M., Christensen, S.T., Surma, E.: Design optimization with respect to ergonomic properties. Structural and Multidisciplinary Optimization **24** (2), 89–97 (2002) 

- [25] Lagomarsino, M., Lorenzini, M., De Momi, E., Ajoudani, A.: Robot trajectory adaptation to optimise the trade-off between human cognitive ergonomics and workplace productivity in collaborative tasks. In: 2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pp. 663–669 (2022). https: //doi.org/10.1109/IROS47612.2022.9981424 

[26] Bravo-Palacios, G., Wensing, P.M.: Large-scale admm-based co-design of legged robots. In: 2022 IEEE/RSJ 

38 

International Conference on Intelligent Robots and Systems (IROS), pp. 8842–8849 (2022). IEEE 

- [27] Ha, D.: Reinforcement learning for improving agent design. Artificial life **25** (4), 352–365 (2019) 

- [28] Bjelonic, F., Lee, J., Arm, P., Sako, D., Tateo, D., Peters, J., Hutter, M.: Learning-based design and control for quadrupedal robots with parallel-elastic actuators. IEEE Robotics and Automation Letters **8** (3), 1611–1618 (2023) https://doi.org/10.1109/LRA.2023.3234809 

- [29] Fadini, G., Flayols, T., Del Prete, A., Sou`eres, P.: Simulation aided co-design for robust robot optimization. IEEE Robotics and Automation Letters **7** (4), 11306–11313 (2022) 

- [30] Gkikakis, A.E., Featherstone, R.: Realistic mechanism and behaviour co-design of a one legged hopping robot. In: 2021 International Conference on Computer, Control and Robotics (ICCCR), pp. 42–49 (2021). https://doi.org/10.1109/ICCCR49711.2021.9349280 

- [31] Bergonti, F., Nava, G., W¨uest, V., Paolino, A., L’Erario, G., Pucci, D., Floreano, D.: Co-design optimisation of morphing topology and control of winged drones. arXiv preprint arXiv:2309.13948 (2023) 

- [32] Sartore, C., Rapetti, L., Pucci, D.: Optimization of humanoid robot designs for human-robot ergonomic payload lifting. In: 2022 IEEE-RAS 21st International Conference on Humanoid Robots (Humanoids), pp. 722–729 (2022). https://doi.org/10.1109/Humanoids53995.2022.10000222 

- [33] Sartore, C., Rapetti, L., Bergonti, F., Dafarra, S., Traversaro, S., Pucci, D.: Codesign of humanoid robots for ergonomic collaboration with multiple humans via genetic algorithms and nonlinear optimization. In: 2023 IEEE-RAS 22nd International Conference on Humanoid Robots (Humanoids), pp. 1–8 (2023). IEEE 

- [34] Dafarra, S., Pattacini, U., Romualdi, G., Rapetti, L., Grieco, R., Darvish, K., Milani, G., Valli, E., Sorrentino, I., Viceconte, P.M., _et al._ : icub3 avatar system: Enabling remote fully immersive embodiment of humanoid robots. Science Robotics **9** (86), 3834 (2024) 

- [35] Choi, Y., Kim, D., You, B.-J.: On the walking control for humanoid robot based on the kinematic resolution of com jacobian with embedded motion. In: Proceedings 2006 IEEE International Conference on Robotics and Automation, 2006. ICRA 2006., pp. 2655–2660 (2006). https://doi.org/10.1109/ROBOT.2006.1642102 

- [36] Waters, T.R., Putz-Anderson, V., Garg, A., Fine, L.J.: Revised niosh equation for the design and evaluation of manual lifting tasks. Ergonomics **36** (7), 749–776 (1993) 

- [37] Fitzgerald, C.: Developing baxter. In: 2013 IEEE Conference on Technologies for Practical Robot Applications (TePRA), pp. 1–6 (2013). https://doi.org/10.1109/TePRA.2013.6556344 

- [38] Parmiggiani, A., Fiorio, L., Scalzo, A., Sureshbabu, A.V., Randazzo, M., Maggiali, M., Pattacini, U., Lehmann, H., Tikhanoff, V., Domenichelli, D., Cardellino, A., Congiu, P., Pagnin, A., Cingolani, R., Natale, L., Metta, G.: The design and validation of the r1 personal humanoid. In: 2017 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pp. 674–680 (2017). https://doi.org/10.1109/IROS.2017. 8202224 

- [39] Latella, C., Traversaro, S., Ferigo, D., Tirupachuri, Y., Rapetti, L., Andrade Chavez, F.J., Nori, F., Pucci, D.: Simultaneous floating-base estimation of human kinematics and joint torques. Sensors **19** (12), 2794 (2019) 

- [40] Rapetti, L., Tirupachuri, Y., Darvish, K., Dafarra, S., Nava, G., Latella, C., Pucci, D.: Model-based real-time motion tracking using dynamical inverse kinematics. Algorithms **13** (10), 266 (2020) 

39 

- [41] Tirupachuri, Y., Ramadoss, P., Rapetti, L., Latella, C., Darvish, K., Traversaro, S., Pucci, D.: Online noncollocated estimation of payload and articular stress for real-time human ergonomy assessment. IEEE Access **9** , 123260–123279 (2021) 

- [42] Orin, D.E., Goswami, A., Lee, S.-H.: Centroidal dynamics of a humanoid robot. Autonomous robots **35** , 161–176 (2013) 

- [43] Romualdi, G., Dafarra, S., Hu, Y., Pucci, D.: A benchmarking of dcm based architectures for position and velocity controlled walking of humanoid robots. In: 2018 IEEE-RAS 18th International Conference on Humanoid Robots (Humanoids), pp. 1–9 (2018). IEEE 

- [44] Elobaid, M., Turrisi, G., Rapetti, L., Romualdi, G., Dafarra, S., Kawakami, T., Chaki, T., Yoshiike, T., Semini, C., Pucci, D.: Adaptive non-linear centroidal mpc with stability guarantees for robust locomotion of legged robots. IEEE Robotics and Automation Letters **10** (3), 2806–2813 (2025) https://doi.org/10.1109/LRA.2025 .3536296 

- [45] Ivaldi, S., Fumagalli, M., Randazzo, M., Nori, F., Metta, G., Sandini, G.: Computing robot internal/external wrenches by means of inertial, tactile and f/t sensors: Theory and implementation on the icub. In: 2011 11th IEEE-RAS International Conference on Humanoid Robots, pp. 521–528 (2011). https://doi.org/10.1109/Hu manoids.2011.6100813 

- [46] De Santis, A., Siciliano, B., De Luca, A., Bicchi, A.: An atlas of physical human–robot interaction. Mechanism and Machine Theory **43** (3), 253–270 (2008) https://doi.org/10.1016/j.mechmachtheory.2007.03.0 03 

- [47] Latella, C., Tirupachuri, Y., Tagliapietra, L., Rapetti, L., Schirrmeister, B., Bornmann, J., Gorjan, D., ˇCamernik, J., Maurice, P., Fritzsche, L., Gonzalez-Vargas, J., Ivaldi, S., Babiˇc, J., Nori, F., Pucci, D.: Analysis of human whole-body joint torques during overhead work with a passive exoskeleton. IEEE Transactions on Human-Machine Systems **PP** (2021) https://doi.org/10.1109/THMS.2021.3128892 

- [48] Rapetti, L., Sartore, C., Elobaid, M., Tirupachuri, Y., Draicchio, F., Kawakami, T., Yoshiike, T., Pucci, D.: A control approach for human-robot ergonomic payload lifting. In: 2023 IEEE International Conference on Robotics and Automation (ICRA), pp. 7504–7510 (2023). IEEE 

- [49] Guo, C., Rapetti, L., Darvish, K., Grieco, R., Draicchio, F., Pucci, D.: Online action recognition for human risk prediction with anticipated haptic alert via wearables. In: 2023 IEEE-RAS 22nd International Conference on Humanoid Robots (humanoids), pp. 1–8 (2023). IEEE 

- [50] Sartore, C.: Ami-iit/paper ~~s~~ artore ~~2~~ 025 ~~e~~ rgocub ~~n~~ ature ~~m~~ achine ~~i~~ ntelligence: NatureRelease. https://doi.or g/10.5281/zenodo.17011716 . Version V1.0. https://doi.org/10.5281/zenodo.17011716 

- [51] Traversaro, S.: Modelling, Estimation and Identification of Humanoid Robots Dynamics. PhD thesis, University of Genoa (April 2017). https://doi.org/10.5281/zenodo.3564797 . https://doi.org/10.5281/zenodo.3 564797 

- [52] Featherstone, R.: Rigid body dynamics algorithms (2014) 

- [53] Marsden, J.E., Ratiu, T.S.: Introduction to mechanics and symmetry: A basic exposition of classical mechanical systems (2010) 

- [54] Ingram, J.N., Wolpert, D.M.: Chapter 1 - naturalistic approaches to sensorimotor control **191** , 3–29 (2011) 

40 

https://doi.org/10.1016/B978-0-444-53752-2.00016-3 

- [55] Hanavan, E.P., et al.: A mathematical model of the human body **32** (3) (1964) 

- [56] Herman, I.P.: Mechanical Properties of the Body. Springer, Cham (2016). https://doi.org/10.1007/978-3-319 -23932-3 ~~4~~ . https://doi.org/10.1007/978-3-319-23932-3 ~~4~~ 

- [57] Garza-Ulloa, J.: Chapter 2 - introduction to human neuromusculoskeletal systems. In: Garza-Ulloa, J. (ed.) Applied Biomechatronics Using Mathematical Models, pp. 53–118. Academic Press, . (2018). https://doi.or g/10.1016/B978-0-12-812594-6.00002-0 

- [58] Binder, M.D., Hirokawa, N., Windhorst, U. (eds.): Motor Control Hierarchy, pp. 2428–2428. Springer, Berlin, Heidelberg (2009). https://doi.org/10.1007/978-3-540-29678-2 ~~3~~ 583 

- [59] Natale, L., Bartolozzi, C., Pucci, D., Wykowska, A., Metta, G.: icub: The not-yet-finished story of building a robot child. Science Robotics **2** (13), 1026 (2017) https://doi.org/10.1126/scirobotics.aaq1026 https://www.science.org/doi/pdf/10.1126/scirobotics.aaq1026 

- [60] Tirupachuri, Y., Nava, G., Latella, C., Ferigo, D., Rapetti, L., Tagliapietra, L., Nori, F., Pucci, D.: Towards partner-aware humanoid robot control under physical interactions. In: Bi, Y., Bhatia, R., Kapoor, S. (eds.) Intelligent Systems and Applications, pp. 1073–1092. Springer, Cham (2020) 

- [61] Rapetti, L., Tirupachuri, Y., Ranavolo, A., Kawakami, T., Yoshiike, T., Pucci, D.: Shared control of robotrobot collaborative lifting with agent postural and force ergonomic optimization. In: 2021 IEEE International Conference on Robotics and Automation (ICRA), pp. 9840–9847 (2021). https://doi.org/10.1109/ICRA48 506.2021.9561623 

- [62] Dafarra, S., Nava, G., Charbonneau, M., Guedelha, N., Andrade, F., Traversaro, S., Fiorio, L., Romano, F., Nori, F., Metta, G., Pucci, D.: A control architecture with online predictive planning for position and torque controlled walking of humanoid robots. In: 2018 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pp. 1–9 (2018). https://doi.org/10.1109/IROS.2018.8594277 

- [63] Elobaid, M., Romualdi, G., Nava, G., Rapetti, L., Omer Mohamed, H.A., Pucci, D.: Online non-linear centroidal mpc for humanoid robots payload carrying with contact-stable force parametrization. In: 2023 IEEE International Conference on Robotics and Automation (ICRA), pp. 12233–12239 (2023). https: //doi.org/10.1109/ICRA48891.2023.10161086 

- [64] Hyon, S.-H., Hale, J.G., Cheng, G.: Full-body compliant human–humanoid interaction: balancing in the presence of unknown external forces. IEEE transactions on robotics **23** (5), 884–898 (2007) 

- [65] Del Prete, A., Nori, F., Metta, G., Natale, L.: Prioritized motion–force control of constrained fully-actuated robots: “task space inverse dynamics”. Robotics and Autonomous Systems **63** , 150–157 (2015) https://doi. org/10.1016/j.robot.2014.08.016 

- [66] Tirupachuri, Y., Nava, G., Rapetti, L., Latella, C., Pucci, D.: Trajectory advancement during human-robot collaboration. In: 2019 28th IEEE International Conference on Robot and Human Interactive Communication (RO-MAN), pp. 1–8 (2019). https://doi.org/10.1109/RO-MAN46459.2019.8956339 

- [67] Gr¨une, L., Pannek, J.: Nonlinear model predictive control (2017) 

- [68] Gazar, A., Nava, G., Chavez, F.J.A., Pucci, D.: Jerk control of floating base systems with contact-stable 

41 

parameterized force feedback. IEEE Transactions on Robotics **37** (1), 1–15 (2021) https://doi.org/10.1109/ TRO.2020.3005547 

- [69] Shamsuddin, S., Ismail, L.I., Yussof, H., Zahari, N.I., Bahari, S., Hashim, H., Jaffar, A.: Humanoid robot nao: Review of control and motion exploration. In: 2011 IEEE International Conference on Control System, Computing and Engineering, pp. 511–516 (2011). IEEE 

- [70] Sortino, D.M., Rapetti, L., Valli, E., Pucci, D.: Towards a real-world application of wearable sensors for musculoskeletal disorders prevention: the ifeel wired suit. In: 2023 IEEE-EMBS International Conference on Wearable and Implantable Body Sensor Networks (BSN) (2023) 

42 

