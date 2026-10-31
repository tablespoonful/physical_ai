---
title: "Deep Reinforcement Learning for Bipedal Locomotion: A Brief Survey"
date: "2024-04-25"
authors: "Lingfan Bao; Joseph Humphreys; Tianhu Peng; Chengxu Zhou"
url: https://arxiv.org/abs/2404.17070
pdf: https://arxiv.org/pdf/2404.17070
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2404.17070)** / [論文ページ](https://arxiv.org/abs/2404.17070)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

1 

# Deep Reinforcement Learning for Robotic Bipedal Locomotion: A Brief Survey 

Lingfan Bao<sup>1</sup> , Joseph Humphreys<sup>12</sup> , Tianhu Peng<sup>1</sup> and Chengxu Zhou<sup>1</sup> 

**_Abstract_ —Bipedal robots are gaining global recognition due to their potential applications and the rapid advancements in artificial intelligence, particularly through Deep Reinforcement Learning (DRL). While DRL has significantly advanced bipedal locomotion, the development of a unified framework capable of handling a wide range of tasks remains an ongoing challenge. This survey systematically categorises, compares, and analyses existing DRL frameworks for bipedal locomotion, organising them into end-to-end and hierarchical control schemes. Endto-end frameworks are evaluated based on their learning approaches, whereas hierarchical frameworks are examined in terms of their layered structures that integrate learning-based and traditional model-based methods. We provide a detailed evaluation of the composition, strengths, limitations, and capabilities of each framework. Furthermore, this survey identifies key research gaps and proposes future directions aimed at creating a more integrated and efficient unified framework for bipedal locomotion, with broad applicability in real-world environments.** 

### **_Index Terms_ —Deep Reinforcement Learning, Humanoid Robots, Bipedal Locomotion, Legged Robots** 


Fig. 1: Representative bipedal and humanoid robots illustrating the diversity of platforms for locomotion research and development. (a) Cassie: a torque-controlled bipedal robot designed for agile locomotion. (b) Digit: a full-sized humanoid robot evolved from Cassie and actuated by torque control. (c) H1: a full-size, electric, torque-controlled humanoid robot developed by Unitree Robotics. (d) G1: a compact humanoid robot from Unitree featuring lightweight design and high joint backdrivability. (e) Atlas: a fully electric humanoid robot developed by Boston Dynamics. 

## I. INTRODUCTION 

Humans navigate complex environments and perform diverse locomotion tasks with remarkable efficiency using only two legs. Bipedal robots, which closely mimic the human form, possess distinct advantages over wheeled or tracked alternatives, particularly when traversing uneven and challenging terrains. Furthermore, bipedal humanoid robots are specifically designed to operate in human-centric environments, enabling seamless interaction with tools and infrastructure intended for human use. This makes them highly adaptable to a wide range of tasks in such settings. 

As a result, bipedal robots hold significant potential for realworld applications [1]. In manufacturing, they can perform tasks efficiently without requiring additional tools, thereby enhancing productivity and reducing labour demands [2], [3], [4]. Their agility is particularly advantageous in complex environments such as multi-level workplaces. Bipedal robots are also well suited to tasks that involve the use of humandesigned tools, making them valuable for assisting in daily activities, healthcare, and rehabilitation [5]. Moreover, they show considerable promise in search-and-rescue operations, where they can navigate hazardous and unpredictable terrains [6], [7], [8]. 

This work was partially supported by the Royal Society [grant number RG _\_ R2 _\_ 232409] and the Advanced Research and Invention Agency [grant number SMRB-SE01-P06]. 

> 1Department of Computer Science, University College London, UK. chengxu.zhou@ucl.ac.uk 

> 2 School of Mechanical Engineering, University of Leeds, UK. 

Traditional approaches to bipedal locomotion control, such as model-based methods, have been prevalent since the 1980s [9], [10], [11]. Early methods, such as the Linear Inverted Pendulum Model (LIPM) [12], provided simplified representations of the dynamics involved in bipedal motion, enabling easier analysis and control. As research progressed, full dynamic models were introduced to better capture the complexities of real-world locomotion. Advanced methods such as Model Predictive Control (MPC) [13], [14] and Trajectory Optimisation (TO) [15], [16], [9] exploit predefined dynamic models to solve constrained optimal-control problems that plan footsteps, centre-of-mass (CoM) motion, and contact forces. While model-based approaches offer rapid convergence and predictive capabilities, they often struggle in dynamically complex and uncertain environments where adaptability is essential. 

Reinforcement learning (RL)-based methods, particularly deep reinforcement learning (DRL), are effective in optimising robot control policies through direct interaction with the environment [17], which provides a distinct advantage. Unlike model-based approaches, which rely on predefined dynamics and may fail under unforeseen conditions, DRL enables robots to autonomously discover control strategies through trial and error, achieving greater adaptability and robustness in diverse environments. In addition, hybrid methods that combine model-based and learning-based techniques further enhance planning and control by leveraging the strengths of both paradigms. 

2 

Despite these advancements, research in DRL-based locomotion remains highly fragmented, with inconsistencies in training pipelines, reward formulations, observation spaces, and evaluation setups that hinder systematic benchmarking and slow progress towards generalisable locomotion capabilities. Moreover, many methods are tailored to specific morphologies or tasks, offering limited transferability across embodiments and environments. 

This fragmentation motivates the following central research questions: _To what extent has current research achieved generalisation and robustness across diverse morphologies, terrains, and locomotion tasks? If full generalisation has not yet been realised, how can existing DRL approaches be organised and extended towards a unified framework that enables such capability in bipedal robots?_ In this context, the present survey seeks to categorise emerging DRL frameworks for bipedal locomotion, identify their key limitations, and outline opportunities for integration and convergence towards unification. 

To address these aspects, we first clarify the ultimate goal of robot learning: to develop systems that exhibit generalisation, adaptability, and robustness across diverse morphologies, tasks, and environments. The unified framework is therefore not the final destination but a conceptual scaffold emerging from the consolidation of current DRL research efforts. Its role is to organise fragmented methodologies through shared interfaces, training conventions, and evaluation protocols, thereby promoting steady progress towards the broader goal of generalisable and adaptive robot-learning systems. 

Guided by these definitions, this survey examines recent advancements in DRL-based frameworks, categorising control schemes into two primary types: (i) end-to-end and (ii) hierarchical. End-to-end frameworks directly map robot states to joint-level control outputs, while hierarchical frameworks decompose decision-making into multiple layers. In hierarchical systems, a High-Level (HL) planner governs navigation and path planning, while a Low-Level (LL) controller handles fundamental locomotion tasks. The task-level decision-making tier interfaces directly with user commands or predefined tasks, forming a structured approach to robotic control. 

The evolution of RL in bipedal robotics has largely advanced through the end-to-end learning paradigm. Early studies in 2004 applied simple policy-gradient methods to 2D bipeds [18], [19], while later breakthroughs in DRL enabled policy training in high-fidelity physics simulators [20], [21], [22]. As robotic hardware matured, an increasing variety of bipedal and humanoid platforms emerged, supporting extensive evaluation of DRL-based locomotion across diverse morphologies, as illustrated in Fig. 1. This evolution marked the transition from purely simulation-based training to simulation-to-real (sim-to-real) transfer, where policies trained in simulators are deployed on physical robots. In 2020, the first successful sim-to-real transfer of an end-to-end DRL locomotion policy was achieved on the 3D torque-controlled bipedal robot Cassie [23]. Subsequent work explored two principal learning paradigms: reference-based learning, which leverages TO-generated data or motion-capture data to guide policy training [24], [25], [26], [27]; and reference-free learn- 

ing, where policies are trained entirely from scratch to autonomously discover control strategies [28]. These developments demonstrate that end-to-end frameworks can achieve robust and versatile locomotion skills across complex terrains and dynamic environments [29], [30], [31]. 

Similarly, hierarchical structures have garnered significant interest. Within this subset, the hybrid approach combines RLbased and model-based methods to enhance both planning and control strategies. Hybrid architectures often integrate learning-based and model-based modules to combine adaptability with physical consistency. One representative design couples a learned HL planner with an LL model-based controller, forming a cascade-structure or deep-planning hybrid scheme [16], [32], [33]. Alternatively, DRL feedback-control hybrids embed learned control policies within model-based feedback loops to enhance tracking precision and disturbance rejection [34], [35]. Learned hierarchical control schemes [36] decompose locomotion into multiple layers, each focusing on specific functions such as navigation and fundamental locomotion skills [20], [21], [37]. To provide a clearer overview of the current landscape, we categorise existing DRL frameworks as shown in Fig. 2. 

Current progress across both end-to-end and hierarchical paradigms indicates that a unified framework for DRL-based bipedal locomotion is still far from being realised. Establishing such a framework is essential for consolidating diverse learning pipelines, standardising evaluation metrics, and enabling transferable locomotion capabilities across different robot morphologies. As locomotion tasks become increasingly complex, ranging from basic stabilisation to dynamic parkour and locomanipulation, the need for consistent benchmarking has intensified.The DARPA Robotics Challenge exemplified this trend by introducing one of the first large-scale evaluation platforms for bipedal humanoids performing real-world locomotion and manipulation tasks [38], highlighting the importance of robustness and practical deployment. 

Although several reviews discuss RL for general robotics [17] and model-based methods for bipedal robots [9], [10], [11], none specifically focus on DRL-based frameworks for bipeds. To address this gap, this survey reviews relevant literature according to the following selection criteria: (1) studies that investigate DRL frameworks specifically for bipedal robots; (2) research involving both simulated and physical bipedal robots; (3) approaches that improve policy transfer from simulation to real-world environments; and (4) publications from the last five years (2018–April 2024) sourced from reputable databases and conferences, including Google Scholar, IEEE Xplore, Web of Science, arXiv, and major robotics venues such as CoRL, RSS, ICRA, IROS, and Humanoids. 

The search was conducted using the key terms “deep reinforcement learning” or “reinforcement learning” in combination with “bipedal locomotion”, “bipedal walking”, “biped robot”, “humanoid robot”, or “legged robot”. The most relevant and impactful works were manually selected for further review. This survey is intended for readers with a foundational background in robotics who are transitioning to DRL methods, providing an overview of a wide range of approaches with sim- 

3 


Fig. 2: Classification of DRL-based control schemes. The approaches are broadly categorised into two main paradigms: endto-end frameworks, which learn a single policy from sensory inputs to motor commands; and hierarchical frameworks, which decompose the control problem into multiple levels. Within the end-to-end paradigm, a key distinction is drawn between reference-free learning (learning from scratch) and reference-based learning (tracking a predefined motion). Hierarchical structures include hybrid control schemes, which synergistically combine learned components with traditional model-based controllers. 

plified explanations where appropriate. For clarity, throughout this paper the term “humanoid robot” refers specifically to anthropomorphic bipedal robots. 

The primary contributions of this survey are: 

- A comprehensive summary and cataloguing of DRLbased frameworks for bipedal locomotion. 

- A detailed comparison of each control scheme, highlighting their strengths, limitations, and distinctive characteristics. 

- The identification of current challenges and the provision of insightful future research directions. 

The survey is organised as follows: Section II discusses end-to-end frameworks, categorised by learning approaches; Section III presents hierarchical frameworks, classified into three main types; Section IV outlines key limitations and challenges, linking them to the preceding discussions; Section V explores potential pathways, opportunities, and two proposed conceptual models that extend the end-to-end and hierarchical paradigms; finally, Section VI concludes the survey. 

## II. END-TO-END FRAMEWORK 

The end-to-end DRL framework represents a holistic approach in which a single neural network (NN) policy, denoted _π_ ( _·_ ) : _X →U_ , directly maps sensory inputs _X_ , such as images, LiDAR data, or proprioceptive feedback [39], together with user commands [28] or pre-defined references [40], into joint-level control actions _U_ . Here, _X_ represents the sensory input space, _U_ refers to the space of control actions, and _π_ ( _·_ ) denotes the policy function. This framework obviates the need for manually decomposing the problem into sub-tasks, streamlining the control process. 

End-to-end strategies primarily simplify the design of LL tracking to basic elements, such as a proportional–derivative (PD) controller. These methods can be broadly categorised according to their reliance on prior knowledge into two types: reference-based and reference-free. The locomotion skills de- 

veloped through these diverse learning approaches exhibit considerable variation in performance and adaptability. 

The following sections delve into various representation frameworks, exploring their characteristics, limitations, and strengths in comprehensive detail. To facilitate an understanding of these distinctions, Table I provides a succinct overview of the frameworks discussed. 

## _A. Reference-based learning_ 

Reference-based learning leverages prior knowledge generated offline through methods such as TO or motion capture systems. This predefined reference typically includes data related to the robot’s joint movements or pre-planned trajectories, serving as a foundation for the policy to develop locomotion skills by following these established motion patterns. Generally, this approach can be divided into two primary methods: (i) residual learning and (ii) guided learning. 

_1)_ **_Residual learning_** _:_ The proposed framework utilises a policy that modifies motor commands by applying action offsets based on the current reference joint positions, allowing the biped robot to achieve dynamic locomotion through error compensation. The state space includes proprioceptive information such as trunk position, orientation, velocity, angular velocity, joint angles, and joint velocities, providing the necessary sensory data for real-time adjustments. Actions are defined by offsets, _δa_ , which represent deviations from the predefined desired joint positions, _a_ ˆ, with the final motor commands represented as _a_ = _a_ ˆ + _δa_ . The reward function encourages the policy to optimise locomotion performance by considering (a) how closely the robot’s active joint angles match the reference angles, (b) how effectively the robot responds to user commands, and (c) additional terms that further enhance the stability of the robot’s movements. This holistic approach enables the biped robot to adapt to various dynamic conditions while maintaining balance and control. 

Introduced in 2018, a residual learning framework for the bipedal robot Cassie marked a significant advancement [41]. 

4 

TABLE I: Summary and comparison of reference-based and reference-free learning approaches for the end-to-end framework. The dashed line in the implementation flow chart indicates optional steps. 

|**Methods**|**Works**|**Capabilities**|**Characteristic**|**Advantages and Disadvantages**|**Implem**|**entation Flow Chart**|
|---|---|---|---|---|---|---|
|Residual<br>learning|[41]<br>[23]|Forward walk<br>unidirectional walk|Adding a residual term<br>known motor positions<br>current time step.|to the<br>at the<br>**A:** Fast convergence speed<br>**D:** Requires high-quality predefined<br>reference, limits to specific motions,<br>and lacks robustness to complex ter-<br>rains.|**Reference**<br>**User**<br>**Commands**|Policy𝜋<br>**Robots**|
|Guided<br>learning|[42]<br>[40]<br>[43]<br>[31]|Forward walk<br>Versatile walk<br>Versatile jump<br>Versatile motions|Mimic the predefined <br>ence and directly spei<br>joint-level commands.|refer-<br>cifies<br>**A:** Accelerates the learning process<br>and is robust across terrains.<br>**D:** Limits to the predefined motions<br>and lacks adaptability to unforeseen<br>changes in environment.|**Reference**<br>**User**<br>**Commands**|Policy𝜋<br>**Robots**|
|Reference-free<br>learning|[28]<br>[44]<br>[29]<br>|Periodic motions<br>Stepping stones walk<br>Visual walk|Learn<br>locomotion<br>from scratch without<br>prior knowledge.|skills<br> any<br>**A:** High potential for gait explo-<br>ration, highly robust to complex ter-<br>rain<br>**D:** Requires intensive reward shap-<br>ing for gait patterns and is rela-<br>tively expensive in computational re-<br>sources|**User**<br>**Commands**|Policy𝜋<br>**Robots**|


**Forward Walk** involves bipeds walking straight ahead. **Unidirectional Walk** enables bipeds to move forward and backward within a range of desired velocities. Omnidirectional Walk grants bipeds the ability to walk in any direction. **Versatile Walk** allows the bipeds to walk forward, backward, turn, and move sideways, providing extensive movement capabilities. **Periodic Motions** entails the execution of various repeated gait patterns, such as walking, hopping, or galloping. **Versatile Jump** refers to jumping towards different desired targets. **Versatile Motions** cover performing a broad array of motions, both periodic and aperiodic such as jumping. 

This framework allowed the robot to walk forward by incorporating a policy trained via Proximal Policy Optimisation (PPO) algorithms, as detailed in Appendix A. The policy receives the robot’s states and reference inputs, outputting a residual term that augments the reference at the current timestep. These modified references are then processed by a PD controller to set the desired joint positions. Although this framework has improved the robot’s ability to perform tasks beyond standing [45], it has yet to be physically deployed on a bipedal robot. As a result, it remains impractical for managing walking at varying speeds and is constrained to movement in a single direction. 

To transition this framework to a real robot, a sim-to-real strategy based on the previous model was demonstrated, where the policy, trained through a residual learning approach, was subsequently applied to a physical bipedal robot [23]. Compared to model-based methods, this training policy achieves faster running speeds on the same platform, underlining the considerable potential of DRL-based frameworks. However, the robot’s movements remain constrained to merely walking forward or backward. 

A unique residual learning approach was introduced to enable omnidirectional walking, where the policy adds a residual term to the current joint positions, allowing gradual omnidirectional walking [46]. In this case, the desired reference is the robot’s current joint positions, which makes the approach distinctive. However, this also limits the policy’s ability to explore more diverse motions, restricting it to a single slow walking pattern. 

Residual learning enhances an existing control policy by taking current joint positions or states and applying a residual action to adjust reference actions for better performance. 

Compared to other learning approaches that directly output joint positions, it is highly sample efficient [32]. However, when predefined references are unstable or of low quality, residual learning may struggle, especially on complex terrains, as the action space is bounded by the reference, limiting the ability to handle unpredictable or uneven terrains. 

_2)_ **_Guided learning_** _:_ Guided learning trains policies to directly output the desired joint-level commands as actions _a_ , without relying on the addition of a residual term. The state space is the same as the residual-learning approach. In this approach, the reward structure is centred on accurately imitating predefined reference trajectories, ensuring precise alignment between the policy output and the reference motion. 

A sim-to-real framework that employs periodic references to initiate the training phase was proposed in [42]. In this framework, the action space directly maps to the joint angles, and desired joint positions are managed by joint PD controllers. The framework also incorporates a Long Short-Term Memory (LSTM) network, as detailed in the Appendix A, which is synchronised with periodic time inputs. However, this model is limited to a single locomotion goal: forward walking. A more diverse and robust walking DRL framework that includes a Hybrid Zero Dynamics (HZD) gait library was demonstrated [40], achieving a significant advancement by enabling a single end-to-end policy to facilitate walking, turning, and squatting. 

Despite these advancements, the parameterisation of reference motions introduces constraints that limit the flexibility of the learning process and the policy’s response to disturbances. To broaden the capabilities of guided learning policies, a framework capable of handling multiple targets, including jumping, was developed [43]. This approach introduced a novel policy structure that integrates long-term 

5 

input/output (I/O) encoding, complemented by a multi-stage training methodology that enables the execution of complex jumping manoeuvrers. An adversarial motion priors approach, employing a style reward mechanism, was also introduced to facilitate the acquisition of user-specified gait behaviours [27]. This method improves the training of high-dimensional simulated agents by replacing complex hand-designed reward functions with more intuitive controls. 

While previous works primarily focused on specific locomotion skills, a unified framework that accommodates both periodic and non-periodic motions was further developed [31] based on the foundational work in [43]. This framework enhances the learning process by incorporating a wide range of locomotion skills and introducing a dual I/O history approach, marking a significant breakthrough in creating a robust, versatile, and dynamic end-to-end framework. However, experimental results indicate that the precision of locomotion features, such as velocity tracking, remains suboptimal. 

Guided learning methods expedite the learning process by leveraging expert knowledge and demonstrating the capacity to achieve versatile and robust locomotion skills. Through the comprehensive evaluation [31], it is demonstrated that guided learning employs references without complete dependence on them. Conversely, residual learning exhibits failures or severe deviations when predicated on references of inferior quality. This shortfall stems from the framework’s dependency on adhering closely to the provided references, which narrows its learning capabilities. 

However, the benefits of reference-based learning come with inherent limitations. Reliance on predefined trajectories often confines the policy to specific gaits, restricting its capacity to explore a broader range of motion possibilities [40], [47]. Moreover, such methods exhibit reduced adaptability when confronted with novel environments or unforeseen perturbations. These limitations are further compounded by the difficulty of acquiring high-quality and task-relevant demonstrations. 

Common sources of prior knowledge include TO [16], [48], [40], [31], human motion capture [25], teleoperation [49], [50], and scripted controllers [21]. While informative, these demonstrations often require adaptation due to embodiment mismatch or limited generalisability. Motion retargeting [51], [26], [52], as one of promising direction, addresses this by converting human-centric motions into robot-feasible trajectories, yet it still struggles with preserving fidelity and adapting across morphologies. 

Ultimately, the success of guided learning relies not only on using references but on accessing high-quality, adaptable demonstrations that generalise across tasks and platforms—highlighting a key challenge in advancing robust policy learning. 

## _B. Reference-free learning_ 

In reference-free learning, the policy is trained using a carefully crafted reward function rather than relying on predefined trajectories. This approach allows the policy to explore a wider range of gait patterns and adapt to unforeseen terrains, thereby 

enhancing innovation and flexibility within the learning process. The action space and observation space in this approach are similar to the guided-learning method; however, the reward structure differs significantly from the reference-based method. Instead of focusing on imitating predefined motions, the reward emphasises learning efficient gait patterns by capturing the distinctive characteristics of bipedal locomotion [47]. 

The concept of reference-free learning was initially explored using simulated physics engines with somewhat unrealistic bipedal models. A pioneering framework, which focused on learning symmetric gaits from scratch without the use of motion capture data, was developed and validated within a simulated environment [22]. This framework introduced a novel term into the loss function and utilised a curriculum learning strategy to effectively shape gait patterns. Another significant advancement was made in developing a learning method that enabled a robot to navigate stepping stones using curriculum learning, focusing on a physical robot model (Cassie), though this has yet to be validated outside of simulation [53]. 

Considering the practical implementation of this approach, significant efforts have been made to develop sim-to-real reference-free frameworks, and their potential has been further explored on physical robots. A notable example of such a framework accommodates various periodic motions, including walking, hopping, and galloping [28]. This framework employs periodic rewards to facilitate initial training within simulations before successfully transitioning to a physical robot. It has been further refined to adapt to diverse terrains and scenarios. For instance, robust blind walking on stairs was demonstrated through terrain randomisation techniques in [44]. Additionally, the integration of a vision system has enhanced the framework’s ability to precisely determine foot locations [54], thus enabling the robot to effectively navigate stepping stones [29]. Subsequent developments include the incorporation of a vision system equipped with height maps, leading to an end-to-end framework that more effectively generalises terrain information [55]. 

This approach to learning enables the exploration of novel solutions and strategies that might not be achievable through mere imitation of existing behaviours. However, the absence of reference guidance can render the learning process costly, time-consuming, and potentially infeasible for certain tasks. Moreover, the success of this method hinges critically on the design of the reward function, which presents significant challenges in specifying tasks such as jumping. 

## III. HIERARCHY FRAMEWORK 

Unlike end-to-end policies that directly map sensor inputs to motor outputs, hierarchical control schemes deconstruct locomotion challenges into discrete, manageable layers or stages of decision-making. Each layer within this structure is tasked with specific objectives, ranging from navigation to fundamental locomotion skills. This division not only enhances the framework’s flexibility but also simplifies the problem-solving process for each policy. 

The architecture of a hierarchical framework typically comprises two principal modules: an HL planner and an LL 

6 


Fig. 3: **Hierarchical control scheme diagram.** This figure illustrates a hierarchical control framework for a bipedal robot, comprising a basic scheme and three variations. (1) Basic scheme: The framework begins with a task command, followed by an HL planner and a LL controller, which ultimately drives the robot. Each module can be replaced with a learned policy, introducing adaptability across different control layers. (2) Variations (from left to right): (a) a deep planning hybrid scheme, in which the HL planner is learned; (b) a feedback DRL control hybrid scheme, with a learned LL controller; and (c) a learned hierarchical control scheme, where both layers are learned. 

controller. This modular approach allows for the substitution of each component with either a model-based method or a learning-based policy, further enhancing adaptability and customisation to specific needs. 

Communication between the layers in a hierarchical framework is achieved through the transmission of commands. The HL planner sets abstract goals, which the LL controller translates into specific actions, such as calculating joint movements to follow a desired trajectory. In return, the robot sends sensor data back to the HL planner, enabling real-time adjustments. The tasks handled by different layers often operate on varying time scales, adding complexity to synchronising communication between the layers. 

Hierarchical frameworks can be classified into three distinct types based on the integration and function of their components: 

- 1) **Deep planning hybrid scheme:** This approach combines strategic, HL planning with dynamic LL execution, leveraging the strengths of both learning-based and traditional model-based methods. 

- 2) **Feedback DRL control hybrid scheme:** It focuses on integrating direct feedback control mechanisms with DRL, allowing for real-time adjustments and enhanced responsiveness. 

- 3) **Learned hierarchy scheme:** Entirely learning-driven, this scheme develops a layered decision-making hierarchy where each level is trained to optimise specific aspects of locomotion. 

These frameworks are illustrated in Fig. 3. Each type offers unique capabilities and exhibits distinct characteristics, albeit with limitations primarily due to the complexities involved in integrating diverse modules and their interactions. 

For a concise overview, Table II summarises the various frameworks, detailing their respective strengths, limitations, and primary characteristics. The subsequent sections will delve 

deeper into each of these frameworks, providing a thorough analysis of their operational mechanics and their application in real-world scenarios. 

## _A. Deep planning hybrid scheme_ 

In this scheme, robots are pre-equipped with the ability to execute basic locomotion skills such as walking, typically managed through model-based feedback controllers or interpretable methods. The addition of an HL learned layer focuses on strategic goals or the task space, enhancing locomotion capabilities and equipping the robot with advanced navigation abilities to effectively explore its environment. 

Several studies have demonstrated the integration of an HL planner policy with a model-based controller to achieve tasks in world space. A notable framework optimises task space level performance, eschewing direct joint-level and balancing considerations [32]. This system combines a residual learning planner with an inverse dynamics controller, enabling precise control over task-space commands to joint-level actions, thereby improving velocity tracking, foot touchdown location, and height control. Further advancements include a hybrid framework that merges HZD-based residual deep planning with model-based regulators to correct errors in learned trajectories, showcasing robustness, training efficiency, and effective velocity tracking [33]. These frameworks have been successfully transferred from simulation to reality and validated on robots such as Cassie. 

However, the limitations imposed by residual learning constrained the agents’ capacity to explore a broader array of possibilities. Building on previous work [33], a more efficient hybrid framework was developed, which learns from scratch without reliance on prior knowledge [56]. In this approach, a purely learning-based HL planner interacts with an LL controller using an Inverse Dynamics with Quadratic Programming formulation (ID-QP). This policy adeptly captures 

7 

TABLE II: Summary and comparison of hierarchical frameworks. 

|**Control Scheme**|**Works**|**Module**|**Characteristics**|**Advantages and Disadvantages**|
|---|---|---|---|---|
|Deep Planning<br>Hybrid Scheme|[32]<br>[56]<br>[57]|Deep planning + ID<br>Deep planning + ID-QP<br>Deep planning + WPG|HL policy is learned to guide<br>the LL controller to com-<br>plete locomotion and naviga-<br>tion tasks.|**A:** Enhanced command tracking capa-<br>bilities, generalised across different plat-<br>forms, sampling-efficient, and robust.<br>**D:** Complicated system and communica-<br>tion between layers, requires a precise<br>model, and lacks generalisation across<br>different tasks.|
|Feedback DRL Control<br>Hybrid Scheme|[48]<br>[34]<br>[35]|Gait library + feedback policy<br>Footstep planner + feedback policy<br>Model-based planner + feedback policy|LL feedback policy receives<br>non-learned HL planner as<br>input to achieve locomotion<br>skills.|**A:** Short inference time, robust, nav-<br>igation<br>locomotion<br>capabilities,<br>inter-<br>pretability.<br>**D:**<br>Complicated system and commu-<br>nication between layers, which reduces<br>sampling efficiency.|
|Learned Hierarchy<br>Fk|[20]<br>[37]|HL policy + LL policy<br>HL policy + LL policy|Both HL planner and LL<br>feedback<br>controller<br>are<br>learned. LL policy focuses<br>onbasiclocomotionskills|**A:** Provides layer flexibility, where each<br>layer can be independently retrained and<br>reused; alleviates the challenges associ-<br>ated with training an end-to-end policy.|
|ramewor|[50]|HL policy + LL policy|;<br>on the other side, HL policy<br>learns navigation skills.|**D:** Inefficient sim-to-real transfer, com-<br>plicated interface between layers, and an<br>expensive training process.|


dynamic walking gaits through the use of reduced-order states and simplifies the learning trajectory. Demonstrating robustness and training efficiency, this framework has outperformed other models and was successfully generalised across various bipedal platforms, including Digit, Cassie, and RABBIT. 

In parallel, several research teams have focused on developing navigation and locomotion planners for humanoid robots, leveraging onboard visual perception and learned control strategies. Recent work [57] explored complex dynamic motion tasks such as playing soccer by integrating a learned policy with an online footstep planner that utilises weight positioning generation (WPG) to create a CoM trajectory. This configuration, coupled with a whole-body controller, enables dynamic activities like soccer shooting. Although these systems demonstrate promising coordination between perception, planning, and control, they remain limited in dynamic movement capability compared to full-sized humanoid robots, and thus primarily address navigation and task-level execution. 

Regarding generalisation, these frameworks have shown potential for adaptation across different types of bipedal robots with minimal adjustments, demonstrating advanced user command tracking [56] and sophisticated navigation capabilities [57]. However, limitations are evident, notably the absence of capabilities for executing more complex and dynamic motions, such as jumping. Furthermore, while these systems adeptly navigate complex terrains with obstacles, footstep planning alone is insufficient without concurrent enhancements to the robot’s overall locomotion capabilities. Moreover, the requisite communication between the two distinct layers of the hierarchical framework may introduce system complexities. Enhancing both navigation and dynamic locomotion capabilities within the HL planner remains a significant challenge. 

## _B. Feedback DRL control hybrid scheme_ 

In contrast to the comprehensive approach of end-to-end policies discussed in Section II, which excels in handling 

versatile locomotion skills and complex terrains with minimal inference time, the Feedback DRL Control Hybrid Scheme integrates DRL policies as LL controllers. These LL controllers, replacing traditional model-based feedback mechanisms, work in conjunction with HL planners that process terrain information, plan future walking paths, and maintain robust locomotion stability. 

For instance, gait libraries, which provide predefined movement references based on user commands, have been integrated into such frameworks [48]. Despite the structured approach of using gait libraries, their static nature offers limited adaptability to changing terrains, diminishing their effectiveness. A more dynamic approach involves online planning, which has shown greater adaptability and efficiency. One notable framework combines a conventional foot planner with an LL DRL policy [34], delivering targeted footsteps and directional guidance to the robot, thereby enabling responsive and varied walking commands. Moreover, HL controllers can provide additional feedback to LL policies, incorporating CoM or endfeet information, either from model-based methods or other conventional control strategies. However, this work has not yet been transferred from simulation to real-world applications. Later, a similar structure featuring an HL foot planner and an LL DRL-based policy was proposed [35]. This strategy not only achieved a successful sim-to-real transfer but also enabled the robot to navigate omnidirectionally and avoid obstacles. 

A recent development has shown that focusing solely on foot placement might restrict the stability and adaptability of locomotion, particularly in complex maneuvers. A new framework integrates a model-based planner with a DRL feedback policy to enhance bipedal locomotion’s agility and versatility, displaying improved performance [58]. This system employs a residual learning architecture, where the DRL policy’s outputs are merged with the planner’s directives before being relayed to the PD controller. This integrated approach not only concerns itself with foot placement but also generates 

8 

comprehensive trajectories for trunk position, orientation, and ankle yaw angle, enabling the robot to perform a wide array of locomotion skills including walking, squatting, turning, and stair climbing. 

Compared to traditional model-based controllers, learned DRL policies provide a comprehensive closed-loop control strategy that does not rely on assumptions about terrain or robotic capabilities. These policies have demonstrated high efficiency in locomotion and accurate reference tracking [59]. Despite their extensive capabilities, such policies generally require short inference time, making DRL a preferred approach in scenarios where robustness is paramount or computational resources on the robot are limited. Nonetheless, these learning algorithms often face challenges in environments characterised by sparse rewards, where suitable footholds like gaps or stepping stones are infrequent [59]. 

Additionally, an HL planner can process critical data such as terrain variations or obstacles and generate precise target locations for feet or desired walking paths, instead of detailed terrain data, which can significantly expedite the training process [35]. This capability effectively addresses the navigational limitations observed in end-to-end frameworks. Moreover, unlike the deep planning hybrid scheme where modifications post-policy establishment can be cumbersome, this hybrid scheme offers enhanced flexibility for on-the-fly adjustments. 

Despite the significant potential demonstrated by previous studies, integrating DRL-based controllers with sophisticated and complex HL planners still presents limitations compared to more integrated frameworks such as end-to-end and deep planning models. Specifically, complex HL model-based planners often require substantial computational resources to resolve problems, rely heavily on model assumptions, necessitate extensive training periods, demand large datasets for optimisation, and hinder rapid deployment and iterative enhancements [59]. 

## _C. Learned hierarchy framework_ 

The Learned Hierarchy Framework merges a learned HL planner with an LL controller, focusing initially on refining LL policies to ensure balance and basic locomotion capabilities. Subsequently, an HL policy is developed to direct the robot towards specific targets, encapsulating a structured approach to robotic autonomy. 

The genesis of this framework was within a physics engine, aimed at validating its efficiency through simulation [20]. In this setup, LL policies, informed by human motions or trajectories generated via TO, strive to track these trajectories as dictated by the HL planner while maintaining balance. An HL policy is then introduced, pre-trained with longterm task goals, to navigate the environment and identify optimal paths. This structure enabled sophisticated interactions such as guiding a biped to dribble a soccer ball towards a goal. The framework was later enhanced to include imitation learning (IL), facilitating the replication of dynamic humanlike movements within the simulation environment [21]. 

However, despite its structured and layered approach, which allows for the reuse of learned behaviours to achieve long- 

term objectives, these frameworks has been validated only in simulations. The interface designed manually between the HL planner and the LL controller sometimes leads to suboptimal behaviours, including stability issues like falling. 

Expanding the application of this framework, a sim-to-real strategy for a wheeled bipedal robot was proposed, focusing the LL policy on balance and position tracking, while the HL policy enhances safety by aiding in collision avoidance and making strategic decisions based on the orientation of subgoals [37]. 

To fully leverage its potential, HumanPlus has been developed as a versatile framework for humanoid robots, integrating hierarchical learning, multimodal perception, and real-world imitation [50]. It employs a two-layer structure, where HIT learns from human demonstrations, trained on AMASS, and HST acts as an LL tracking controller. Additionally, binocular RGB vision input enhances perception, enabling precise locomanipulation and dynamic locomotion tasks such as jumping, walking, folding clothes, and rearranging objects. This shadowing-based IL approach improves adaptability, making it a promising framework for transferring human-like skills to robots. 

Learning complex locomotion skills, particularly when incorporating navigation elements, presents a significant challenge in robotics. Decomposing these tasks into distinct locomotion and navigation components allows robots to tackle more intricate activities, such as dribbling a soccer ball [20]. As discussed in the previous section, the benefits of integrating RL-based planners with RL-based controllers have been effectively demonstrated. This combination enables the framework to adeptly manage a diverse array of environments and tasks. 

Within such a framework, the HL policy is optimised for strategic planning and achieving specific goals. This optimisation allows for targeted enhancements depending on the tasks at hand. Moreover, the potential for continuous improvement and adaptation through further training ensures that the system can evolve over time, improving its efficiency and effectiveness in response to changing conditions or new objectives. Despite the theoretical advantages, the practical implementation of this type of sim-to-real application for bipedal robots remains largely unexplored. 

Additionally, the training process for each policy within the hierarchy demands considerable computational resources [37]. The intensive nature of this training can lead to a reliance on the simulation environment, potentially causing the system to overfit to specific scenarios and thereby fail to generalise to real-world conditions. This limitation highlights a significant hurdle that must be addressed to enhance the viability of learned hierarchy frameworks in practical applications. 

Besides, for the general hierarchical framework, the transition from simulation to real-world scenarios is challenging, particularly due to the complexities involved in coordinating two layers within the control hierarchy. Ensuring seamless communication and cooperation between the HL planner and LL controller is essential to avoid operational discrepancies. The primary challenges include: (1) Task division complexity—while the HL planner handles strategy and provides abstract goals, the LL Controller manages precise execution, 

9 

necessitating careful coordination to avoid functional overlap and conflicts. (2) Effective communication—the HL’s abstract goals must be accurately interpreted and converted by the LL into real-time actions, especially in dynamic environments. (3) Task allocation—clear division of responsibilities between layers is crucial to prevent redundancy and ensure smooth system performance. 

## IV. LIMITATIONS AND CHALLENGES 

The end-to-end and hierarchical frameworks detailed in Sections II and III represent the state of the art in DRL-based bipedal locomotion, demonstrating remarkable capabilities on specific tasks. However, a substantial gap remains between these task-oriented successes and the broader goal of achieving generalisation and adaptability across diverse morphologies, tasks, and environments. Bridging this gap requires more than incremental improvements—it demands the establishment of a unified framework that consolidates interfaces, training conventions, and evaluation protocols to systematically address the underlying limitations of current DRL pipelines. 

As outlined in the following sections, the core challenges underlying this gap can be grouped into three interrelated aspects. At a foundational level, a primary difficulty involves the limitations and challenges in achieving both generalisation and precision (Section IV-A). This is further complicated by the practical barrier of the sim-to-real gap in transferring policies from simulation to physical robots (Section IV-B). Ultimately, these issues culminate in the critical challenges of ensuring safety and interpretability for robust deployment in real-world, safety-critical situations (Section IV-C). 

## _A. Generalisation and precision_ 

A central challenge in applying DRL to bipedal locomotion is the need to simultaneously achieve high generalisation across diverse skills and traverse to all kinds of terrains, and high precision in specific tasks. This remains a fundamental obstacle to realising truly unified and capable frameworks. 

This capability gap is evident in the current literature. Many approaches excel at generalisation, demonstrating policies that enable versatile skills such as walking and jumping [40], [31] and can transfer to different terrains [44], [29], [60]. However, these generalised policies often lack the fidelity required for high-precision tasks such as exact foot placement [34], [29], [54] or maintaining a specific velocity with minimal error [47]. Conversely, controllers specialised for narrow domains can achieve exceptional precision, as seen in jumping to a precise target [43], yet they cannot generalise these capabilities to a broader range of tasks. Thus, the development of a single unified framework that concurrently exhibits both broad competency and high fidelity remains largely unresolved. 

This difficulty in uniting generalisation and precision is not arbitrary but stems from several key limitations inherent in current DRL paradigms, whether related to framework design, task formulation, or the training process itself: 

- **Limited terrain and gait patterns:** The failure to generalise is often a direct result of training on insufficiently diverse environments or with a restricted set of behaviours. 

Models trained on limited terrain are brittle when faced with novel surfaces, while a limited gait pattern library prevents adaptation to tasks requiring new motor skills. 

- **Poor command tracking:** The learning signals for generalisation and precision are often in direct conflict. Generalisation requires permissive signals that allow the robot to adapt to varied terrains or recover from perturbations, whereas precision demands restrictive signals that minimise command-tracking error. Faced with these opposing objectives, a single policy is forced to compromise, which often leads to poor command tracking and the sacrifice of adaptability in favour of rigid, high-fidelity execution [30], [31]. 

- **Inefficient sampling:** Underpinning the difficulty of solving both problems simultaneously is the inefficient sampling of most DRL algorithms [36], [61], [62]. This problem is severely exacerbated in tasks that depend on sparse rewards, where feedback is infrequent and often only supports the success of the final task. Consequently, the immense amount of data required for an agent to explore, discover a successful strategy, and then refine it for both a diverse skill set for generalisation and the fine-grained control needed for precision is often computationally prohibitive, motivating massive parallel simulation merely to make training tractable [63], [64], [20], [21]. 

- **High-quality data scarcity:** As highlighted in Section II-A2, the scarcity of high-quality demonstrations is a key bottleneck. Such data provide essential guidance for DRL, enabling policies to learn physically feasible and natural-looking gaits while avoiding unsafe exploration [21], [20], [65]. This scarcity stems from the difficulty of transferring scalable human data due to embodiment mismatch [52], [51], [50], while generating feasible synthetic data via trajectory optimisation is often computationally expensive [15], [16]. 

These fundamental limitations give rise to common algorithmic challenges, such as the need for complex reward engineering, and are directly reflected in the design of the field’s dominant control architectures. End-to-end frameworks attempt a holistic solution, learning a single monolithic policy that must implicitly resolve all challenges simultaneously. While this approach can yield highly versatile and dynamic behaviours [60], it directly confronts the immense difficulty of exploration from sparse rewards and the struggle of reconciling conflicting training objectives within unstable system dynamics. This often results in a lack of the fidelity and precision that hierarchical systems can enforce [31]. Conversely, hierarchical frameworks are a direct architectural response to the lack of skill compositionality. By employing a “divide and conquer” strategy, they use an HL policy to sequence a library of LL, often model-based, controllers. This structure enforces precision and manages complex dynamics at a lower level [16], [54], [35]. However, this results in a brittle system, imposing a strong prior that constrains the policy’s freedom and limits its ability to generalise to situations not anticipated by the handcrafted controller [34]. 

10 

## _B. Challenges in transferring from simulation to reality_ 

Another challenge hindering the deployment of DRL policies on bipedal robots is the sim-to-real gap. This refers to the significant discrepancy between a policy’s performance in a physics simulator and its performance on actual hardware. This gap is a critical obstacle because training directly on physical robots is often impractical. The millions of environmental interactions required for DRL would lead to accelerated mechanical wear, a risk of catastrophic failure, and require constant human supervision. While simulation offers a safe and efficient alternative, the ultimate goal of “zero-shot” transfer, where a policy works perfectly without any real-world fine-tuning, is rarely achieved. 

A large body of research validates impressive locomotion skills purely within simulation, without attempting transfer to a physical system [20], [21], [66], [67], [30]. Even when transfer is successful, it often comes with compromises. Many successful transfers are not truly “zero-shot” and rely on a subsequent phase of extensive real-world fine-tuning or manual parameter tuning [68], [23]. In cases where policies do transfer without fine-tuning, they often exhibit a noticeable degradation in performance, where the robustness and agility seen in simulation are significantly lower in the real world [44], [29], [69]. 

This gap is caused by unavoidable differences between the virtual and physical worlds, which are especially problematic for dynamically unstable bipedal robots. 

- **Robot dynamics modelling and actuation:** Simulators struggle to replicate the complex dynamics of a physical bipedal robot, whose inherent instability makes it particularly sensitive to modelling errors. Factors such as motor friction, gear backlash, and precise link inertia are often simplified. 

- **Contact and terrain modelling:** Accurately simulating intermittent foot–ground contact is extremely difficult. A mismatch between simulated and real-world friction or surface properties can cause unexpected slips or bounces, leading to loss of balance. 

- **Sensing and state estimation:** A simulated robot has access to perfect, noise-free state information. In the real world, these states must be estimated from noisy sensors such as IMUs and joint encoders [23], [68]. For a bipedal robot, precise state estimation is critical for maintaining balance. 

Simulators such as Isaac Gym [63], RoboCup3D [70], OpenAI Gym [71], and MuJoCo [72], detailed in Appendix B, are widely used to train policies that closely mimic real-world physical conditions. These platforms use full-order dynamics to better represent the complex interactions robots face, and numerous sim-to-real frameworks [23], [73], [74] have demonstrated efficient and high-performance results. Despite these advancements, a significant gap persists between simulation and reality, exacerbated by the approximations made in simulation and the unpredictability of physical environments. 

## _C. Safety-critical locomotion_ 

Beyond performance metrics such as agility and robustness, the practical deployment of bipedal robots in human-centric environments is fundamentally contingent upon safety [1], [10], [11]. This includes ensuring the robot’s own integrity to prevent costly damage, as well as guaranteeing the safety of the surrounding environment and any humans within it. While many existing frameworks have demonstrated impressive locomotion skills, they often prioritise performance over these safety considerations. This creates a critical barrier that separates success in controlled laboratory settings from reliable operation in the unpredictable real world. 

- **Blind locomotion policies:** Many current frameworks rely solely on internal sensors (proprioception) such as joint angles and IMU data [42], [44], [28], creating a major safety risk. Lacking external perception, these robots cannot anticipate obstacles, slopes, or slippery surfaces, making them purely reactive and highly prone to failure. Despite these significant safety drawbacks, this approach is often adopted for several reasons: omitting vision simplifies the control problem to pure motor skills and avoids the computational cost of real-time visual processing. Moreover, since robust blind locomotion has already been demonstrated, vision is often treated as a supplementary component used to enhance task-specific precision [55] or path planning [75], rather than a core requirement for basic stability. 

- **Lack of physical constraint satisfaction:** Many DRL frameworks lack built-in mechanisms to guarantee physical constraint satisfaction. This gap has motivated constrained or safety-aware DRL that enforces limits via the learning objective or auxiliary safety modules—for example, Safe-RL on humanoids [76], hybrid DRL with identified low-dimensional safety models [77], footstepconstrained DRL policies [54], and reactive DRL steppers operating under feasibility constraints on uneven terrain [66]. This limitation makes it difficult to prevent the robot from exceeding joint limits, applying excessive torques, or causing self-collisions, particularly when reacting to unexpected events. This is a key area where constrained RL could be applied. 

In summary, the pursuit of performance in DRL has often sidelined critical safety issues. The prevalence of blind policies that cannot anticipate environmental hazards, combined with the lack of inherent mechanisms to enforce physical constraints, creates significant risk and hinders real-world deployment. While these challenges are considerable, they also define a clear path forward. The following section on Future Directions and Opportunities explores specific research avenues, such as vision-based learning and safe reinforcement learning, aimed at overcoming these safety barriers and enabling the development of truly robust and reliable bipedal robots. 

## V. FUTURE DIRECTIONS AND OPPORTUNITIES 

Following the analysis of the surveyed frameworks and their limitations, this section outlines a path forward for DRL- 

11 


Fig. 4: Towards a Unified Framework: This figure illustrates the logical progression from current DRL frameworks to future unified systems. It identifies the current limitations of existing end-to-end and hierarchical approaches, which motivate the exploration of specific Future Pathways. These pathways inform the design of two proposed conceptual models (i) MultiLayered Adaptive Model (MLAM) and (ii) Bipedal Foundation Model (BFM) which represent potential blueprints for achieving a generalist, unified framework. 

based bipedal locomotion by exploring both direct research avenues and emerging opportunities. We begin in Section V-A by detailing research directions that directly respond to the challenges identified in Section IV. Building on this foundation, Section V-B broadens the scope to explore synergistic opportunities from related fields, such as loco-manipulation and the application of foundation models. These discussions culminate in Section V-C, where we propose two conceptual models for a unified framework that represent the future evolution of the end-to-end and hierarchical paradigms. 

## _A. Pathways for bipedal locomotion_ 

In relation to the research question introduced in Section I, progress in DRL-based bipedal locomotion should be assessed not only through conventional metrics such as reward and success rate but also by broader system-level measures. These include generalisation breadth (across skills, terrains, and morphologies), precision in fidelity-critical tasks (e.g., command-tracking error and foot-placement accuracy), safety and constraint compliance (joint, torque, and contact feasibility), and efficiency or deployability (sample efficiency and on-robot inference latency). 

These dimensions build directly upon the challenges outlined in Section IV and together define the key pathways for advancing bipedal locomotion. The following subsections elaborate on these pathways, each addressing one or more of the above aspects to guide progress towards more generalisable and robust control systems. 

_1) Multi-skill learning:_ A fundamental goal for the next generation of bipedal robots is to move beyond the paradigm of single-task specialisation and towards versatile skill learning [60], [78], [31]. This research direction focuses on enabling robots to acquire, adapt, and deploy a broad and varied repertoire of motor skills, allowing them to handle unforeseen situations and operate effectively in unstructured environments. 

To achieve such versatility, researchers are pursuing several HL pathways, which can be broadly categorised into structured and holistic approaches. The structured approach focuses on explicit decomposition. A prominent example is hierarchical learning, where success depends on appropriately dividing responsibilities; for instance, an HL planner generates reference trajectories, while an LL DRL controller executes them robustly [50], [56], as shown in Section III. Similarly, skill composition employs a supervisor policy to select and sequence LL experts to solve complex tasks [21]. A related technique, knowledge distillation, leverages experts by first training them and then distilling their capabilities into a single, compact generalist policy [79]. 

_2) Traversing challenging environments:_ The goal of versatile skill learning is to enable bipedal robots to traverse challenging, human-centric environments where their unique form offers an advantage. Validating capabilities on such terrains serves a crucial dual purpose. It tests a policy’s generalisation across diverse settings, including stairs and uneven ground, which is essential for real-world integration [44], [47], [60]. More critically, it benchmarks precision on treacherous paths such as stepping stones, which demand exact foot placement 

12 

[29], [14], [66]. These environments are the ultimate test of both a robot’s skill repertoire and its control fidelity. 

_3) Efficient learning and reward shaping:_ As detailed in Section IV, while DRL has unlocked impressive capabilities in bipedal locomotion, its reliance on training from scratch leads to significant sample inefficiency [36], [28]. Addressing this bottleneck is a crucial research frontier that calls for both more efficient algorithms and more robust reward designs. 

To mitigate sample inefficiency for complex skills, several research pathways are being actively explored. A primary strategy is to leverage prior data rather than learning entirely from scratch. Leveraging prior knowledge provides strong guidance and reduces unsafe exploration by anchoring policies to feasible motion patterns [21], [41], [50]. Curriculum learning further organises training from simple to progressively harder tasks, for example standing and balancing before walking and running, which improves stability and convergence [53], [46], [35]. 

Complementing advances in algorithms is the design of effective and robust rewards. Manual reward engineering remains a significant obstacle, since small choices can induce reward hacking and lengthy tuning cycles [64], [21]. Phaseaware objectives are well established for cyclic gaits such as walking [28], whereas reward design for non-periodic skills such as jumping is less standardised and often task specific [43]. Promising directions reduce manual effort by adding higher-level guidance, including event-based terms, goal-conditioned objectives, and kinematic reference tracking [54], [24], [45]. Alternatively, learning rewards from data through inverse methods and related approaches aims to replace hand-crafted objectives with implicit ones inferred from demonstrations [80]. Together, these directions seek to minimise skill-specific tuning and improve the transferability and reliability of learned locomotion policies. 

_4) Motion retargeting:_ As human-like agents, bipedal robots—especially humanoids—have the unique advantage of a morphology that is similar to our own. This presents a significant opportunity: the potential to learn from vast libraries of human motion data. While large-scale datasets such as AMASS [81] and Motion-X [82] provide a wealth of such data, they are inherently human-centric and cannot be used directly, requiring substantial retargeting effort [25]. Therefore, motion retargeting emerges as a critical component to bridge this gap. The challenge of this pathway is not merely to transfer human movements to the robot, but to generate trajectories that are both high in stylistic fidelity and physically feasible, adhering to the robot’s unique dynamics and constraints. Successfully developing these retargeting methods provides a scalable solution for accessing the data needed to train the natural and versatile generalist policies of the future. 

_5) Bridging the gap from simulation to reality:_ Strategies to bridge the sim-to-real gap generally follow two main philosophies. The first aims to train policies robust enough to tolerate the inevitable mismatch between simulation and reality, while the second focuses on minimising the gap itself by making the simulator a more faithful replica of the physical world. 

The first approach seeks to reduce the discrepancy by improving the simulation’s fidelity. This is often achieved through system identification (SI), where real-world robot data are used to fine-tune the simulator’s parameters to create a more accurate “digital twin” [68], [83]. This can include explicitly learning complex actuator dynamics to model the motors’ behaviour [68], [84]. Other methods, such as designing specialised feedback controllers [85], also contribute by making the system less sensitive to residual modelling errors. 

In contrast, the second philosophy accepts that simulations will always be imperfect and instead focuses on creating highly adaptive, robust policies. The primary method here is DR, which forces a policy to generalize by training it across a wide range of simulated physical variations. Other various ways, such as through end-to-end training that uses measurement histories to adapt online like in RMA [73], or via policy distillation, where a privileged “teacher” guides a “student” policy [47] to have a knowledge of unknown information like friction . Additionally, techniques like adversarial motion priors [27], [26] are used to ensure the learned behaviours are not just robust but also physically plausible. 

Looking ahead, the ultimate goal remains achieving reliable zero-shot transfer, where no real-world fine-tuning is needed. Progress will depend on the co-development of higher-fidelity simulations, improved hardware, and more robust control policies inherently capable of handling real-world unpredictability. The synergy of these advancements will be crucial in finally closing the sim-to-real gap. 

_6) Perception-conditioned locomotion:_ Integrating exteroceptive sensors such as cameras and LiDAR enables bipedal robots to proactively plan footsteps, avoid obstacles, and adapt to upcoming terrain. This shift from reactive to anticipatory control is essential for navigating unstructured real-world environments. 

The vision-based pathway is a human-inspired approach using RGB and depth cameras to capture rich data on colour, texture, and object appearance [29], [55], [35]. In contrast, LiDAR is an active sensing method that generates precise 3D point clouds of the terrain. While vision provides richer data but is sensitive to lighting, LiDAR offers robust geometric measurements without visual detail. 

Based on this sensory data, current research is exploring two primary pathways for processing perceptual information for control. The first involves creating an intermediate geometric representation, such as a height map from scanners [55]. This provides the policy with structured topographical data for effective footstep planning. The second is a more end-to-end approach, which utilises direct vision inputs such as RGB or depth images as inputs to the RL policy for real-time decisionmaking [75], [86]. The former offers interpretability, while the latter promises more nuanced, reactive behaviours learned directly from raw perception. 

Future progress requires advancing both pathways: building richer, semantic world representations and improving the efficiency of direct perception-to-action policies. Solving the underlying challenges of real-time processing and the perceptual sim-to-real gap will be crucial for enabling truly adaptive locomotion in complex, real-world scenarios. 

13 

_7) Constrained learning:_ While the previously discussed pathways focus on enhancing a robot’s capabilities, a parallel and equally critical frontier is ensuring that these capabilities are exercised safely and reliably. To formally integrate safety, modern approaches can be grouped by how they handle constraints: soft constraints that guide the policy through costs and hard constraints that strictly limit actions [76], [77]. 

Soft constraints encourage desirable behaviour and penalise undesirable behaviour without forbidding it. They are well suited to preferences or efficiency goals, for example minimising energy use, limiting peak torques, or promoting smooth motion [76]. Hard constraints are inviolable rules that prevent catastrophic failures. They are essential for enforcing physical limits and protecting the robot and its environment, for example footstep feasibility, contact timing, joint and torque bounds, and collision avoidance [54], [85]. A practical way to enforce hard constraints is to use safety filters or shields grounded in control theory, such as control barrier functions and related template model checks [87]. 

In practice, a robust and trustworthy bipedal robot will likely combine both ideas. Soft constraints help a policy learn efficient and natural gaits, while hard constraints guarantee that it will not take catastrophic actions. This combination supports the transition from systems that are merely capable in laboratory settings to agents that are reliable, predictable, and safe for real-world deployment. 

## _B. Opportunities_ 

_1) Leveraging foundation models for locomotion learning:_ The recent rise of Foundation Models (FMs), such as Large Language Models (LLMs) and Vision–Language Models (VLMs), presents a transformative opportunity for bipedal locomotion. Their powerful reasoning capabilities are unlocking new approaches that go beyond traditional control methods, primarily by enabling sophisticated HL task planning and by providing novel solutions to shape the learning process itself, particularly in automated reward design. 

As HL planners, FMs provide a reasoning engine that can bridge the gap between abstract human goals and LL motor execution. They can interpret complex linguistic commands or visual scenes and decompose them into a sequence of simpler, actionable commands for an LL policy to follow. This has been demonstrated effectively in legged robotics, where VLMs process raw sensory data to pass structured commands to motor controllers [88], creating a seamless link between strategic planning and physical action. 

Furthermore, FMs create a significant opportunity to overcome one of the most persistent bottlenecks in DRL: reward design. Instead of tedious manual tuning, LLMs can dynamically generate or refine reward functions based on linguistic descriptions of task success. Research has shown that LLMs can translate human feedback into reward adjustments [89] or even autonomously adjust rewards and control strategies to self-optimise for diverse terrains [90], drastically reducing human intervention. 

The foremost opportunity lies in the deeper synergy between these roles. The integration of the HL symbolic reasoning 

of FMs with the LL, real-time control of DRL could create a new class of highly adaptive and flexible robots. As this rapidly evolving field progresses, as reviewed in [91], we may see a paradigm shift towards more autonomous, self-learning humanoid robots that can understand, reason about, and adapt to the world with minimal human intervention. 

_2) Loco-manipulation tasks:_ While achieving stable locomotion is a foundational challenge, a bipedal robot with only a lower body has limited practical utility, as it cannot physically interact with its environment. The evolution of modern humanoids to include complex upper bodies is a critical advancement that has unlocked the opportunity for loco-manipulation—the dynamic integration of movement and object interaction. Achieving such full-body coordination is now a key benchmark for creating truly adaptable systems, with tasks ranging from climbing and using tools to carrying objects while navigating, as highlighted by initiatives like the DARPA Robotics Challenge [38]. 

However, realising this opportunity is a significant challenge. Early studies, such as a ‘box transportation’ framework [92], often rely on inefficient, multi-policy solutions that lack visual perception. Furthermore, dynamically interacting with mobile objects like scooters or balls introduces even greater complexity [93], [94]. 

These difficulties create significant research opportunities. One such opportunity lies in exploring hierarchical control approaches. By decomposing tasks into multiple layers, this method allows for precise, modular control over different components, which can enhance stability and adaptability to environmental variations [56]. 

Alternatively, a further research opportunity is the development of end-to-end learning frameworks, which offer a more scalable solution. Using techniques like curriculum learning and imitation from human motion-capture data [46], [35], [31], [49], [27], [25], a single, unified policy can be trained to handle diverse loco-manipulation tasks, representing a promising avenue of research for creating truly versatile agents. 

_3) Insights from quadruped robots:_ While DRL remains an emerging technology in bipedal robotics, it has firmly established its presence in the realm of quadruped robots, another category of legged systems. The diversity of frameworks developed for quadrupeds ranges from end-to-end, modelbased RL designed for training in real-world scenarios, where unpredictable dynamics often prevail [95], [96], to systems that include the modelling of deformable terrain to enhance locomotion over compliant surfaces [97]. Furthermore, dynamic quadruped models facilitate highly adaptable policies [98], [99], and sophisticated acrobatic motions are achieved through IL [100]. 

The domain of quadruped DRL has also seen significant advancements in complex hierarchical frameworks that integrate vision-based systems. To date, two primary versions of such hierarchical frameworks have been developed: one where a deep-planning module is paired with model-based control [101] within a deep-planning hybrid scheme, and another that combines model-based planning with LL DRL control [59], [102] within a feedback DRL control hybrid scheme. The latter has shown substantial efficacy; it employs an MPC 

14 

to generate reference motions, which are then followed by an LL feedback DRL policy. Additionally, the Terrain-aware Motion Generation for Legged Robots module [103] enhances the MPC and DRL policy by providing terrain height maps for effective foothold placements across diverse environments, including those not encountered during training. However, similar hierarchical hybrid control schemes have not been thoroughly investigated within the field of bipedal locomotion. 

Quadruped DRL frameworks are predominantly designed to navigate complex terrains, but efforts to extend their capabilities to other tasks are under way. These include mimicking real animals through motion-capture data and IL [104], [105], as well as augmenting quadrupeds with manipulation abilities. This is achieved either by adding a manipulator [106], [107] or by using the robots’ legs [108]. Notably, the research presented in [107] demonstrates that loco-manipulation tasks can be effectively managed using a single, unified, end-to-end framework. 

Despite the progress in quadruped DRL, similar advancements have been limited for bipedal robots, particularly in loco-manipulation tasks and vision-based DRL frameworks; a combination of their inherent instability, lack of accessibility to researchers, and high mechanical complexity can be attributed to this disparity between quadruped and bipedal robots. Establishing a unified framework could bridge this gap—an essential step, given the integral role of bipedal robots with upper bodies in developing fully functional humanoid systems. Moreover, the potential of hybrid frameworks that combine model-based and DRL-based methods in bipedal robots remains largely untapped. 

## _C. Conceptual models for unified frameworks_ 

Motivated by our survey and the current state of the art, we propose two conceptual models, intended as reference designs, towards a unified locomotion framework. They build on endto-end and hierarchical paradigms and offer complementary routes to scalable, generalisable architectures, rather than fully realised systems. 

- **Bipedal Foundation Models (BFMs):** large-scale, pretrained models that map perception directly to action through representation learning. Trained on diverse data across tasks and embodiments, BFMs aim to enable generalist locomotion control by supporting rapid adaptation via fine-tuning. 

- **Multi-Layer Adaptive Models (MLAMs):** modular, hierarchical architectures that span from HL planning to LL control, with each layer producing interpretable intermediate outputs. MLAMs are designed to integrate, substitute, and coordinate diverse policies, enabling flexible and adaptive responses across tasks and embodiments. 

- In the following sections, we will analyse each of these con- 

- ceptual models in detail, evaluating their respective strengths and challenges in the pursuit of a unified framework. 

_1) Bipedal foundation models:_ Inspired by Robot Foundation Models (RFMs) [91], [109], we propose the concept of BFMs as large-scale, general-purpose models tailored for bipedal locomotion. A BFM would be a large-scale model 

pre-trained specifically to learn the shared motion priors of dynamic balance and movement across a vast range of bipedal tasks and physical embodiments. Unlike traditional policies trained from scratch, a BFM would provide a foundational understanding of stable locomotion, directly tackling the core difficulties that make bipeds distinct from other robots. Architecturally, we envision such a model comprising a multi-modal embedding module, a shared backbone like a transformer, and an action decoder, drawing inspiration from models like RT2 [110]. 

The proposed BFM paradigm would operate in two stages. First, IL on diverse datasets would establish the generalisable foundation. Second, DRL would be repurposed as an efficient fine-tuning mechanism to adapt these general priors to the specific, and often unforgiving, dynamics of a physical robot. The potential of this approach is highlighted by recent works, with frameworks like FLaRe [111] enhancing generalisation for long-horizon tasks, MOTO [112] enabling effective offlineto-online adaptation from images, and AdA [113] demonstrating in-context adaptation to novel environments. Collectively, these approaches underscore DRL not only as a simple tuning tool but as a central mechanism for grounding abstract foundation model priors into executable, platform-specific control policies. 

However, realising the BFM concept for bipeds presents significant challenges. The DRL fine-tuning stage can be costly and risky on physical hardware, and policies may overfit to narrow dynamics or catastrophically forget the generalisable priors acquired during pre-training [111], [113]. Furthermore, as detailed in Sections IV-A and V-A4, the scarcity of highquality, large-scale data remains a fundamental bottleneck, as most existing datasets are human-centric and require significant adaptation before they can be used. 

_2) Multi-layered adaptive models:_ As a complementary path to BFMs, we propose the concept of MLAMs. Rather than relying on large-scale pre-training, this conceptual framework would adopt a modular, hierarchical approach. The idea is to extend conventional hierarchical frameworks (discussed in Section III) with explicitly adaptive layers, allowing for the dynamic composition of specialised policies. The core principle of this concept would be modularity, enabling each layer to be independently optimised or replaced and providing interpretable outputs at each stage. 

A key feature we envision for MLAMs is their capacity to dynamically compose adaptive modules for each control tier. Each layer processes context-specific inputs and outputs interpretable commands. The HL reasoning layer leverages large pre-trained models such as LLMs and VLMs [114], [115] to parse commands into sub-tasks. For instance, Vision–Language Model Predictive Control [88] has been effective in quadrupedal robots, integrating linguistic and visual inputs to optimise HL task planning. By leveraging LLMs, a unified framework could seamlessly bridge HL strategic planning with detailed task execution. 

The mid-level planner selects or synthesises motions via learned motion libraries [48], [40] or DRL-based planners [116]. The LL control layer comprises various modular controllers, dynamically selected and composed based on task- 

15 

specific demands. These include locomotion primitives like walking and climbing [117], adaptive tracking controllers for whole-body tracking [50], and imitation-based skills such as kicking and dancing [21], by utilising RL, IL, or model-based methods. This layered architecture is exemplified by recent work on quadrupedal robots, where LLMs are used to translate HL commands into robust and flexible real-world behaviours [117]. 

However, realising the MLAM concept would introduce challenges distinct from BFMs. Such a framework would depend heavily on real-time multi-modal perception, which complicates data alignment across layers with differing timescales and abstraction levels [103]. Additionally, the computational latency incurred by HL reasoning modules like LLMs [117] would pose limitations for tasks needing rapid reactions. 

## VI. CONCLUSION 

Despite significant progress in DRL for robotics, a substantial gap remains between current achievements and the development of a unified framework capable of efficiently handling a wide range of complex tasks. DRL research is generally divided into two main control schemes: end-toend and hierarchical frameworks. End-to-end frameworks have demonstrated success in handling diverse locomotion skills [31], climbing stairs [44], and navigating challenging terrains such as stepping stones [29]. Meanwhile, hierarchical frameworks provide enhanced capabilities, particularly in managing both locomotion and navigation tasks simultaneously. 

Each framework contributes unique strengths to the pursuit of a unified framework. End-to-end approaches simplify control by directly mapping inputs to outputs, while referencebased and reference-free learning methods provide the versatility required for robots to acquire diverse locomotion skills. In contrast, hierarchical frameworks improve flexibility by structuring control into layers, allowing modular task decomposition and hybrid strategies. 

While DRL has enabled remarkable progress, our survey concludes that current frameworks face key limitations, including the tension between multi-skill generalisation and taskspecific precision, the persistent sim-to-real gap, and critical safety concerns. To address these challenges, this survey synthesises specific pathways for future research and identifies key opportunities for cross-pollination from related fields, such as FMs, loco-manipulation, and quadrupedal robotics. These insights culminate in our proposal of two conceptual frameworks: the BFMs, extending the end-to-end paradigm, and the MLAMs, evolving from the hierarchical approach, which together offer distinct blueprints for the next generation of generalist bipedal controllers. 

## APPENDIX A 

## DEEP REINFORCEMENT LEARNING ALGORITHMS 

The advancement and development of RL are crucial for bipedal locomotion. Specifically, advances in deep learning provide deep NNs that serve as function approximators, enabling RL to handle tasks characterised by high-dimensional and continuous spaces by efficiently discovering condensed, 

low-dimensional representations of complex data. In comparison with other robots of different morphologies, such as wheeled robots, bipedal robots possess far higher DoFs and continuously interact with their environments, which results in greater demands on DRL algorithms. In particular, within legged locomotion, policy-gradient-based algorithms are prevalent in bipedal locomotion research. 

Designing an effective NN architecture is essential for tackling complex bipedal locomotion tasks. Multi-Layer Perceptrons (MLPs), a fundamental NN structure, excel in straightforward regression tasks with lower computational resource requirements. A comprehensive comparison between MLPs and the memory-based NN LSTM reveals that MLPs have an advantage in convergence speed for many tasks [74]. However, LSTMs, as variants of Recurrent Neural Networks (RNNs), are adept at processing time-associated data, effectively relating different states across time and modelling key physical properties vital for periodic gaits [28] and successful sim-to-real transfer in bipedal locomotion. Additionally, Convolutional Neural Networks (CNNs) specialise in spatial data processing, particularly for image-related tasks, making them highly suitable for environments where visual perception is crucial. This diversity of NN architectures highlights the importance of selecting an appropriate model based on the specific requirements of bipedal locomotion tasks. 

Considering DRL algorithms, recent bipedal locomotion studies have focused on model-free RL algorithms. Unlike model-based RL, which learns a model of the environment but may inherit biases from simulations that do not accurately reflect real-world conditions, model-free RL directly trains policies through environmental interaction without relying on an explicit environmental model. Although model-free RL requires more computational samples and resources, it can train more robust policies that allow robots to traverse challenging environments. 

Many sophisticated model-free RL algorithms exist, which can be broadly classified into two categories: policy-based (or policy optimisation) and value-based approaches. Value-based methods, e.g. Q-learning, State–Action–Reward–State–Action (SARSA), and Deep Q-learning (DQN) [66], excel only in discrete action spaces and often struggle with high-dimensional action spaces. Q-learning is an off-policy algorithm that directly learns the optimal Q-values, allowing it to derive the best possible actions irrespective of the current policy. SARSA, an on-policy variant, updates its Q-values based on 


Fig. 5: **Diagram for RL algorithms catalogue** 

16 

the actual actions taken, making it robust in environments where the policy evolves during learning. DQN extends Q- learning by using deep NNs to approximate Q-values, enabling the algorithm to tackle complex state spaces, though it still faces challenges with high-dimensional action spaces due to difficulties in accurate value estimation. In contrast, policybased methods, such as policy-gradient techniques, can handle complex tasks but are generally less sample-efficient than value-based methods. 

More advanced algorithms combine both policy-based and value-based methods. The Actor–Critic (AC) framework simultaneously learns both a policy (actor) and a value function (critic), combining the advantages of both approaches [118], [119]. Popular algorithms such as Trust Region Policy Optimisation (TRPO) [120] and PPO, based on policy-based methods, borrow ideas from AC. Moreover, other novel algorithms based on the AC framework include Deep Deterministic Policy Gradient (DDPG) [121], Twin Delayed Deep Deterministic Policy Gradients (TD3) [122], A2C (Advantage Actor–Critic), A3C (Asynchronous Advantage Actor–Critic) [123], and SAC (Soft Actor–Critic) [124]. Each algorithm has its strengths for different tasks in bipedal locomotion scenarios. Several key factors determine their performance, such as sample efficiency, robustness and generalisation, and implementation complexity. A comparative analysis [62] illustrates that SACbased algorithms excel in stability and achieve the highest scores, while their training efficiency significantly trails behind that of PPO, which attains relatively high scores. 

In [61], PPO demonstrates robustness and computational efficiency in complex scenarios such as bipedal locomotion, utilising fewer resources than TRPO. In terms of training time, PPO is much faster than SAC and DDPG [62]. Moreover, many studies [28], [48], [42] have demonstrated its robustness and ease of implementation. Combined with its flexibility to integrate with various NN architectures, this has made PPO the most popular choice in the field. Numerous studies have shown that PPO can enable the exploration of walking [28], jumping [43], stair climbing [44], and stepping-stone traversal [29], demonstrating its efficiency, robustness, and generalisation. 

Additionally, the DDPG algorithm integrates the Actor–Critic framework with DQN to facilitate off-policy training, further optimising sample efficiency. In certain scenarios, such as jumping, DDPG shows higher rewards and better learning performance than PPO [30], [125]. TD3, developed from DDPG, improves upon the performance of both DDPG and SAC [124]. 

SAC improves exploration through its stochastic policy and entropy-regularised objective, which encourages the agent to maintain randomness in its actions, balancing exploration and exploitation more effectively than DDPG and TD3. Unlike PPO, which is an on-policy algorithm, SAC’s off-policy nature allows it to leverage a replay buffer, reusing past experiences for training without requiring constant interaction with the environment. This, combined with entropy maximisation, enables SAC to achieve faster convergence in complex environments where exploration is essential. SAC is also known for its stability and strong performance across a wide range of tasks [124]. While A2C offers improved efficiency 

and stability compared with A3C, the asynchronous update mechanism of A3C provides better exploration capability and accelerates learning. Although these algorithms demonstrate clear advantages, they are more challenging to apply owing to their complexity compared with PPO. 

## APPENDIX B 

## TRAINING SIMULATION ENVIRONMENT 

The development of DRL algorithms and sim-to-real techniques highlights the requirement for high-quality simulators. Creating a reliable simulation environment and conducting RL training is challenging. The literature shows that several simulators are available, including Isaac Gym [63], RoboCup3D [70], OpenAI Gym [71], MuJoCo [72], Orbit [126], Brax [127], and Isaac Lab [128]. 

OpenAI developed Gym and Gymnasium to provide lightweight environments for rapid testing of RL algorithms, including simplified bipedal locomotion models. RoboCup also serves as a benchmark platform for RL research and development in multi-agent settings. 

For physics-based simulation, MuJoCo, developed by DeepMind, and Gazebo are widely used platforms that support a range of robotics research tasks. NVIDIA’s Isaac Gym, although now deprecated, played an important role as a highperformance GPU-based simulator for training agents in complex environments. Its successors, such as Isaac Lab and Orbit, continue to evolve as modern RL and robotics frameworks. 

One of the most crucial aspects is the parallelisation strategy and GPU simulation. For instance, Isaac Gym was developed to maximise the throughput of physics-based machine learning algorithms, with particular emphasis on simulations requiring large numbers of environment instances executing in parallel. Running the physics simulation on a GPU can result in significant speed-ups, especially for large scenes with thousands of individual actors. 

## REFERENCES 

- [1] Y. Tong, H. Liu, and Z. Zhang, “Advancements in humanoid robots: A comprehensive review and future prospects,” _IEEE/CAA Journal of Automatica Sinica_ , vol. 11, pp. 301–328, 2024. 

- [2] A. Dzedzickis, J. Subaˇci¯ut˙e-Zemaitien˙e<sup>ˇ</sup> _et al._ , “Advanced applications of industrial robotics: New trends and possibilities,” _Applied Sciences_ , vol. 12, p. 135, 2021. 

- [3] M. Yang, E. Yang _et al._ , “Collaborative mobile industrial manipulator: a review of system architecture and applications,” in _International conference on automation and computing_ , 2019, pp. 1–6. 

- [4] “6+ Hours Live Autonomous Robot Demo,” https://www.youtube.com/watch?v=Ke468Mv8ldM, Mar. 2024. 

- [5] G. Bingjing, H. Jianhai _et al._ , “Human–robot interactive control based on reinforcement learning for gait rehabilitation training robot,” _International Journal of Advanced Robotic Systems_ , vol. 16, p. 1729881419839584, 2019. 

- [6] R. Bogue, “Underwater robots: a review of technologies and applications,” _Industrial Robot: An International Journal_ , vol. 42, pp. 186– 191, 2015. 

- [7] N. Rudin, H. Kolvenbach _et al._ , “Cat-like jumping and landing of legged robots in low gravity using deep reinforcement learning,” _IEEE Transactions on Robotics_ , vol. 38, pp. 317–328, 2022. 

- [8] J. Qi, H. Gao _et al._ , “Reinforcement learning-based stable jump control method for asteroid-exploration quadruped robots,” _Aerospace Science and Technology_ , vol. 142, p. 108689, 2023. 

- [9] S. Gupta and A. Kumar, “A brief review of dynamics and control of underactuated biped robots,” _Advanced Robotics_ , vol. 31, pp. 607–623, 2017. 

17 

- [10] J. Reher and A. Ames, “Dynamic walking: Toward agile and efficient bipedal robots,” _Annual Review of Control, Robotics, and Autonomous Systems_ , vol. 4, 2021. 

- [11] J. Carpentier and P.-B. Wieber, “Recent progress in legged robots locomotion control,” _Current Robotics Reports_ , vol. 2, pp. 231–238, 2021. 

- [12] P. M. Wensing and D. E. Orin, “High-speed humanoid running through control with a 3d-slip model,” in _IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2013, pp. 5134–5140. 

- [13] L. Hou, B. Li _et al._ , “Deep reinforcement learning for model predictive controller based on disturbed single rigid body model of biped robots,” _Machines_ , vol. 10, p. 975, 2022. 

- [14] J. Li and Q. Nguyen, “Dynamic walking of bipedal robots on uneven stepping stones via adaptive-frequency mpc,” _IEEE Control Systems Letters_ , vol. 7, pp. 1279–1284, 2023. 

- [15] A. Herzog, S. Schaal, and L. Righetti, “Structured contact force optimization for kino-dynamic motion generation,” in _IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2016, pp. 2703–2710. 

- [16] T. Li, H. Geyer _et al._ , “Using deep reinforcement learning to learn high-level policies on the ATRIAS biped,” in _International Conference on Robotics and Automation_ , 2019, pp. 263–269. 

- [17] M. A.-M. Khan, M. R. J. Khan _et al._ , “A systematic review on reinforcement learning-based robotics within the last decade,” _IEEE Access_ , vol. 8, pp. 176 598–176 623, 2020. 

- [18] R. Tedrake, T. Zhang, and H. Seung, “Stochastic policy gradient reinforcement learning on a simple 3D biped,” in _IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2004, pp. 2849–2854. 

- [19] J. Morimoto, G. Cheng _et al._ , “A simple reinforcement learning algorithm for biped walking,” in _IEEE International Conference on Robotics and Automation_ , 2004, pp. 3030–3035 Vol.3. 

- [20] X. Peng, G. Berseth _et al._ , “DeepLoco: dynamic locomotion skills using hierarchical deep reinforcement learning,” _ACM Transactions on Graphics_ , vol. 36, pp. 1–13, 2017. 

- [21] X. Peng, P. Abbeel _et al._ , “DeepMimic: Example-guided deep reinforcement learning of physics-based character skills,” _ACM Transactions on Graphics_ , vol. 37, 2018. 

- [22] W. Yu, G. Turk, and C. K. Liu, “Learning symmetric and low-energy locomotion,” _ACM Transactions on Graphics_ , vol. 37, pp. 1–12, 2018. 

- [23] Z. Xie, P. Clary _et al._ , “Learning locomotion skills for cassie: Iterative design and sim-to-real,” in _Conference on Robot Learning_ , 2020, pp. 317–329. 

- [24] M. Taylor, S. Bashkirov _et al._ , “Learning bipedal robot locomotion from human movement,” in _IEEE International Conference on Robotics and Automation_ , 2021, pp. 2797–2803. 

- [25] X. Cheng, Y. Ji _et al._ , “Expressive whole-body control for humanoid robots,” _arXiv preprint arXiv:2402.16796_ , 2024. 

- [26] A. Tang, T. Hiraoka _et al._ , “HumanMimic: Learning natural locomotion and transitions for humanoid robot via wasserstein adversarial imitation,” _arXiv preprint arXiv:2309.14225_ , 2023. 

- [27] Q. Zhang, P. Cui _et al._ , “Whole-body humanoid robot locomotion with human reference,” _arXiv preprint arXiv:2402.18294_ , 2024. 

- [28] J. Siekmann, Y. Godse _et al._ , “Sim-to-real learning of all common bipedal gaits via periodic reward composition,” in _IEEE International Conference on Robotics and Automation_ , 2021, pp. 7309–7315. 

- [29] H. Duan, A. Malik _et al._ , “Learning dynamic bipedal walking across stepping stones,” in _IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2022, pp. 6746–6752. 

- [30] C. Tao, M. Li _et al._ , “A multiobjective collaborative deep reinforcement learning algorithm for jumping optimization of bipedal robot,” _Advanced Intelligent Systems_ , vol. 6, p. 2300352, 2023. 

- [31] Z. Li, X. B. Peng _et al._ , “Reinforcement learning for versatile, dynamic, and robust bipedal locomotion control,” _arXiv e-prints_ , pp. arXiv–2401, 2024. 

- [32] H. Duan, J. Dao _et al._ , “Learning task space actions for bipedal locomotion,” in _IEEE International Conference on Robotics and Automation_ , 2021, pp. 1276–1282. 

- [33] G. A. Castillo, B. Weng _et al._ , “Reinforcement learning-based cascade motion policy design for robust 3d bipedal locomotion,” _IEEE Access_ , vol. 10, pp. 20 135–20 148, 2022. 

- [34] R. P. Singh, M. Benallegue _et al._ , “Learning bipedal walking on planned footsteps for humanoid robots,” in _IEEE-RAS International Conference on Humanoid Robots_ , 2022, pp. 686–693. 

- [35] S. Wang, S. Piao _et al._ , “Learning 3D bipedal walking with planned footsteps and fourier series periodic gait planning,” _Sensors_ , vol. 23, p. 1873, 2023. 

- [36] K. Arulkumaran, M. P. Deisenroth _et al._ , “Deep reinforcement learning: A brief survey,” _IEEE Signal Processing Magazine_ , vol. 34, pp. 26–38, 2017. 

- [37] W. Zhu and M. Hayashibe, “A hierarchical deep reinforcement learning framework with high efficiency and generalization for fast and safe navigation,” _IEEE Transactions on Industrial Electronics_ , vol. 70, pp. 4962–4971, 2023. 

- [38] C. G. Atkeson, B. P. W. Babu _et al._ , “No falls, no resets: Reliable humanoid behavior in the darpa robotics challenge,” in _IEEE-RAS 15th International Conference on Humanoid Robot_ , 2015, pp. 623–630. 

- [39] X. B. Peng and M. van de Panne, “Learning locomotion skills using deeprl: Does the choice of action space matter?” in _ACM SIGGRAPH/Eurographics Symposium on Computer Animation_ , 2017, pp. 1–13. 

- [40] Z. Li, X. Cheng _et al._ , “Reinforcement learning for robust parameterized locomotion control of bipedal robots,” in _IEEE International Conference on Robotics and Automation_ , 2021, pp. 2811–2817. 

- [41] Z. Xie, G. Berseth _et al._ , “Feedback control for cassie with deep reinforcement learning,” in _IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2018, pp. 1241–1246. 

- [42] J. Siekmann, S. Valluri _et al._ , “Learning memory-based control for human-scale bipedal locomotion,” in _Robotics science and systems_ , 2020. 

- [43] Z. Li, X. B. Peng _et al._ , “Robust and versatile bipedal jumping control through multi-task reinforcement learning,” in _Robotics: Science and Systems_ , 2023. 

- [44] J. Siekmann, K. Green _et al._ , “Blind bipedal stair traversal via sim-toreal reinforcement learning,” in _Robotics: Science and Systems_ , 2021. 

- [45] C. Yang, K. Yuan _et al._ , “Learning whole-body motor skills for humanoids,” in _IEEE-RAS International Conference on Humanoid Robots_ , 2019, pp. 270–276. 

- [46] D. Rodriguez and S. Behnke, “Deepwalk: Omnidirectional bipedal gait by deep reinforcement learning,” in _IEEE International Conference on Robotics and Automation_ , 2021, pp. 3033–3039. 

- [47] B. van Marum, M. Sabatelli, and H. Kasaei, “Learning perceptive bipedal locomotion over irregular terrain,” _arXiv preprint arXiv:2304.07236_ , 2023. 

- [48] K. Green, Y. Godse _et al._ , “Learning spring mass locomotion: Guiding policies with a reduced-order model,” _IEEE Robotics and Automation Letters_ , vol. 6, pp. 3926–3932, 2021. 

- [49] M. Seo, S. Han _et al._ , “Deep imitation learning for humanoid locomanipulation through human teleoperation,” in _IEEE-RAS International Conference on Humanoid Robots_ , 2023, pp. 1–8. 

- [50] Z. Fu, Q. Zhao _et al._ , “Humanplus: Humanoid shadowing and imitation from humans,” _arXiv preprint arXiv:2406.10454_ , 2024. [Online]. Available: https://arxiv.org/abs/2406.10454 

- [51] L. Penco, B. Clement _et al._ , “Robust real-time whole-body motion retargeting from human to humanoid,” in _2018 IEEE-RAS 18th International Conference on Humanoid Robots (Humanoids)_ , 2018, pp. 425–432. 

- [52] K. Ayusawa and E. Yoshida, “Motion retargeting for humanoid robots based on simultaneous morphing parameter identification and motion optimization,” _IEEE Transactions on Robotics_ , vol. 33, no. 6, pp. 1343– 1357, 2017. 

- [53] Z. Xie, H. Ling _et al._ , “ALLSTEPS: Curriculum-driven learning of stepping stone skills,” _Computer Graphics Forum_ , vol. 39, pp. 213– 224, 2020. 

- [54] H. Duan, A. Malik _et al._ , “Sim-to-real learning of footstep-constrained bipedal dynamic walking,” in _International Conference on Robotics and Automation_ , 2022, pp. 10 428–10 434. 

- [55] B. Marum, M. Sabatelli, and H. Kasaei, “Learning vision-based bipedal locomotion for challenging terrain,” _arXiv preprint arXiv:2309.14594_ , 2023. 

- [56] G. A. Castillo, B. Weng _et al._ , “Template model inspired task space learning for robust bipedal locomotion,” in _IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2023, pp. 8582–8589. 

- [57] C. Gaspard, G. Passault _et al._ , “FootstepNet: an efficient actor-critic method for fast on-line bipedal footstep planning and forecasting,” _arXiv preprint arXiv:2403.12589_ , 2024. 

- [58] J. Li, L. Ye _et al._ , “Agile and versatile bipedal robot tracking control through reinforcement learning,” _arXiv preprint arXiv:2404.08246_ , 2024. 

- [59] F. Jenelten, J. He _et al._ , “DTC: Deep tracking control,” _Science Robotics_ , vol. 9, p. eadh5401, 2024. 

- [60] I. Radosavovic, T. Xiao _et al._ , “Real-world humanoid locomotion with reinforcement learning,” _Science Robotics_ , vol. 9, no. 89, p. eadi9579, 2024. 

18 

- [61] J. Schulman, F. Wolski _et al._ , “Proximal policy optimization algorithms,” _arXiv e-prints_ , pp. arXiv–1707, 2017. 

- [62] O. Aydogmus and M. Yilmaz, “Comparative analysis of reinforcement learning algorithms for bipedal robot locomotion,” _IEEE Access_ , pp. 7490–7499, 2023. 

- [63] N. Rudin, D. Hoeller _et al._ , “Learning to walk in minutes using massively parallel deep reinforcement learning,” in _Conference on Robot Learning_ , 2022, pp. 91–100. 

- [64] N. Heess, D. TB _et al._ , “Emergence of locomotion behaviours in rich environments,” _arXiv preprint arXiv:1707.02286_ , 2017. 

- [65] C. Yang, K. Yuan _et al._ , “Learning natural locomotion behaviors for humanoid robots using human bias,” _IEEE Robotics and Automation Letters_ , vol. 5, pp. 2610–2617, 2020. 

- [66] A. Meduri, M. Khadiv, and L. Righetti, “DeepQ stepper: A framework for reactive dynamic walking on uneven terrain,” in _IEEE International Conference on Robotics and Automation_ , 2021, pp. 2099–2105. 

- [67] J. Merel, Y. Tassa _et al._ , “Learning human behaviors from motion capture by adversarial imitation,” _arXiv e-prints_ , pp. arXiv–1707, 2017. 

- [68] W. Yu, V. C. V. Kumar _et al._ , “Sim-to-real transfer for biped locomotion,” in _IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2019, pp. 3503–3510. 

- [69] H. Park, R. Yu _et al._ , “Understanding the stability of deep control policies for biped locomotion,” _The Visual Computer_ , vol. 39, pp. 1– 15, 2020. 

- [70] A. Birk, S. Coradeschi, and S. Tadokoro, _RoboCup 2001: Robot Soccer World Cup V_ , 2003, vol. 2377. 

- [71] G. Brockman, V. Cheung _et al._ , “Openai gym,” _arXiv preprint arXiv:1606.01540_ , 2016. 

- [72] E. Todorov, T. Erez, and Y. Tassa, “MuJoCo: A physics engine for model-based control,” in _IEEE/RSJ International conference on intelligent robots and systems_ , 2012, pp. 5026–5033. 

- [73] A. Kumar, Z. Li _et al._ , “Adapting rapid motor adaptation for bipedal robots,” in _IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2022, pp. 1161–1168. 

- [74] R. P. singh, Z. Xie _et al._ , “Learning bipedal walking for humanoids with current feedback,” _IEEE Access_ , vol. 11, p. 82013–82023, 2023. 

- [75] K. Lobos-Tsunekawa, F. Leiva, and J. Ruiz-del Solar, “Visual navigation for biped humanoid robots using deep reinforcement learning,” _IEEE Robotics and Automation Letters_ , vol. 3, no. 4, pp. 3247–3254, 2018. 

- [76] J. Garc´ıa and D. Shafie, “Teaching a humanoid robot to walk faster through safe reinforcement learning,” _Engineering Applications of Artificial Intelligence_ , vol. 88, p. 103360, 2020. 

- [77] Z. Li, J. Zeng _et al._ , “Bridging Model-based Safety and Modelfree Reinforcement Learning through System Identification of Low Dimensional Linear Models,” in _Proceedings of Robotics: Science and Systems_ , 2022. 

- [78] I. Radosavovic, B. Zhang _et al._ , “Humanoid locomotion as next token prediction,” _arXiv preprint arXiv:2402.19469_ , 2024. [Online]. Available: https://arxiv.org/abs/2402.19469 

- [79] X. Huang, Y. Chi _et al._ , “Diffuseloco: Real-time legged locomotion control with diffusion from offline datasets,” _arXiv preprint arXiv:2404.19264_ , 2024. 

- [80] J. Ho and S. Ermon, “Generative adversarial imitation learning,” in _International Conference on Neural Information Processing Systems_ , 2016, pp. 4572–4580. 

- [81] N. Mahmood, N. Ghorbani _et al._ , “Amass: Archive of motion capture as surface shapes,” in _2019 IEEE/CVF International Conference on Computer Vision_ , 2019, pp. 5441–5450. 

- [82] J. Lin, A. Zeng _et al._ , “Motion-x: A large-scale 3d expressive wholebody human motion dataset,” _NeurIPS_ , 2024. 

- [83] S. Masuda and K. Takahashi, “Sim-to-real transfer of compliant bipedal locomotion on torque sensor-less gear-driven humanoid,” in _IEEE-RAS International Conference on Humanoid Robots_ , 2023, pp. 1–8. 

- [84] J. Hwangbo, J. Lee _et al._ , “Learning agile and dynamic motor skills for legged robots,” _Science Robotics_ , vol. 4, p. eaau5872, 2019. 

- [85] G. A. Castillo, B. Weng _et al._ , “Robust feedback motion policy design using reinforcement learning on a 3D digit bipedal robot,” in _IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2021, pp. 5136–5143. 

- [86] A. Byravan, J. Humplik _et al._ , “Nerf2real: Sim2real transfer of visionguided bipedal motion skills using neural radiance fields,” in _IEEE International Conference on Robotics and Automation_ , 2023, pp. 9362– 9369. 

- [87] Q. Nguyen, A. Hereid _et al._ , “3d dynamic walking on stepping stones with control barrier functions,” in _IEEE Conference on Decision and Control_ , 2016, pp. 827–834. 

- [88] A. S. Chen, A. M. Lessing _et al._ , “Commonsense reasoning for legged robot adaptation with vision-language models,” _arXiv preprint arXiv:2407.02666_ , 2024. 

- [89] K. N. Kumar, I. Essa, and S. Ha, “Words into action: Learning diverse humanoid robot behaviors using language guided iterative motion refinement,” in _Workshop on Language and Robot Learning: Language as Grounding_ , 2023. 

- [90] Y. Yao, W. He _et al._ , “Anybipe: An end-to-end framework for training and deploying bipedal robots guided by large language models,” 2024. [Online]. Available: https://arxiv.org/abs/2409.08904 

- [91] R. Firoozi, J. Tucker _et al._ , “Foundation models in robotics: Applications, challenges, and the future,” _The International Journal of Robotics Research_ , p. 02783649241281508, 2023. 

- [92] J. Dao, H. Duan, and A. Fern, “Sim-to-real learning for humanoid box loco-manipulation,” _arXiv preprint arXiv:2310.03191_ , 2023. 

- [93] J. Baltes, G. Christmann, and S. Saeedvand, “A deep reinforcement learning algorithm to control a two-wheeled scooter with a humanoid robot,” _Engineering Applications of Artificial Intelligence_ , vol. 126, p. 106941, 2023. 

- [94] T. Haarnoja, B. Moran _et al._ , “Learning agile soccer skills for a bipedal robot with deep reinforcement learning,” _Science Robotics_ , vol. 9, p. eadi8022, 2024. 

- [95] L. Smith, I. Kostrikov, and S. Levine, “Demonstrating a walk in the park: Learning to walk in 20 minutes with model-free reinforcement learning,” _Robotics: Science and Systems Demo_ , vol. 2, p. 4, 2023. 

- [96] P. Wu, A. Escontrela _et al._ , “DayDreamer: World models for physical robot learning,” in _Conference on Robot Learning_ , 2023, pp. 2226– 2240. 

- [97] S. Choi, G. Ji _et al._ , “Learning quadrupedal locomotion on deformable terrain,” _Science Robotics_ , vol. 8, p. eade2256, 2023. 

- [98] G. Feng, H. Zhang _et al._ , “Genloco: Generalized locomotion controllers for quadrupedal robots,” in _Conference on Robot Learning_ , vol. 205, 2023, pp. 1893–1903. 

- [99] J. Humphreys and C. Zhou, “Learning to adapt through bio-inspired gait strategies for versatile quadruped locomotion,” _arXiv preprint arXiv:2412.09440_ , 2024. 

- [100] Y. Fuchioka, Z. Xie, and M. van de Panne, “OPT-Mimic: Imitation of optimized trajectories for dynamic quadruped behaviors,” in _IEEE International Conference on Robotics and Automation_ , 2023, pp. 5092– 5098. 

- [101] S. Gangapurwala, M. Geisert _et al._ , “RLOC: Terrain-aware legged locomotion using reinforcement learning and optimal control,” _IEEE Transactions on Robotics_ , vol. 38, pp. 2908–2927, 2022. 

- [102] D. Kang, J. Cheng _et al._ , “RL + Model-Based Control: Using ondemand optimal control to learn versatile legged locomotion,” _IEEE Robotics and Automation Letters_ , vol. 8, pp. 6619–6626, 2023. 

- [103] F. Jenelten, R. Grandia _et al._ , “TAMOLS: Terrain-aware motion optimization for legged systems,” _IEEE Transactions on Robotics_ , vol. 38, pp. 3395–3413, 2022. 

- [104] X. B. Peng, E. Coumans _et al._ , “Learning agile robotic locomotion skills by imitating animals,” in _Robotics: Science and Systems_ , 2020. 

- [105] F. Yin, A. Tang _et al._ , “Run like a dog: Learning based whole-body control framework for quadruped gait style transfer,” in _IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2021, pp. 8508–8514. 

- [106] Y. Ma, F. Farshidian _et al._ , “Combining learning-based locomotion policy with model-based manipulation for legged mobile manipulators,” _IEEE Robotics and Automation Letters_ , vol. 7, pp. 2377–2384, 2022. 

- [107] Z. Fu, X. Cheng, and D. Pathak, “Deep whole-body control: Learning a unified policy for manipulation and locomotion,” in _Conference on Robot Learning_ , 2023, pp. 138–149. 

- [108] P. Arm, M. Mittal _et al._ , “Pedipulate: Enabling manipulation skills using a quadruped robot’s leg,” in _IEEE Conference on Robotics and Automation_ , 2024. 

- [109] Y. Hu, Q. Xie _et al._ , “Toward general-purpose robots via foundation models: A survey and meta-analysis,” _arXiv preprint arXiv:2312.08782_ , 2023. 

- [110] B. Zitkovich, T. Yu _et al._ , “Rt-2: Vision-language-action models transfer web knowledge to robotic control,” in _Proceedings of The 7th Conference on Robot Learning_ , J. Tan, M. Toussaint, and K. Darvish, Eds., 2023, pp. 2165–2183. [Online]. Available: https://proceedings.mlr.press/v229/zitkovich23a.html 

- [111] J. Hu, R. Hendrix _et al._ , “Flare: Achieving masterful and adaptive robot policies with large-scale reinforcement learning fine-tuning,” _arXiv_ , 2024. 

19 

- [112] R. Rafailov, K. B. Hatch _et al._ , “MOTO: Offline pre-training to online fine-tuning for model-based robot learning,” in _Proceedings of The 7th Conference on Robot Learning_ , ser. Proceedings of Machine Learning Research, vol. 229, 2023, pp. 3654–3671. 

- [113] J. Bauer, K. Baumli _et al._ , “Human-timescale adaptation in an openended task space,” in _Proceedings of the 40th International Conference on Machine Learning_ , 2023. 

- [114] A. Irpan, A. Herzog _et al._ , “Do as i can, not as i say: Grounding language in robotic affordances,” _arXiv preprint arXiv:2204.01691_ , 2022. 

- [115] J. Liang, W. Huang _et al._ , “Code as policies: Language model programs for embodied control,” in _arXiv preprint arXiv:2209.07753_ , 2022. 

- [116] M. Kasaei, M. Abreu _et al._ , “Robust biped locomotion using deep reinforcement learning on top of an analytical control approach,” _Robotics and Autonomous Systems_ , vol. 146, p. 103900, 2021. 

- [117] Y. Ouyang, J. Li _et al._ , “Long-horizon locomotion and manipulation on a quadrupedal robot with large language models,” _arXiv preprint arXiv:2404.05291_ , 2024. 

- [118] T. P. Lillicrap, J. J. Hunt _et al._ , “Continuous control with deep reinforcement learning,” in _International Conference on Learning Representations_ , 2016. 

- [119] L. Liu, M. van de Panne, and K. Yin, “Guided learning of control graphs for physics-based characters,” _ACM Transactions on Graphics_ , vol. 35, pp. 1–14, 2016. 

- [120] J. Schulman, S. Levine _et al._ , “Trust region policy optimization,” in _International Conference on Machine Learning_ , 2015, pp. 1889–1897. 

- [121] C. Huang, G. Wang _et al._ , “Reward-adaptive reinforcement learning: Dynamic policy gradient optimization for bipedal locomotion,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , vol. 45, pp. 7686–7695, 2023. 

- [122] S. Dankwa and W. Zheng, “Twin-delayed DDPG: A deep reinforcement learning technique to model a continuous movement of an intelligent robot agent,” in _International conference on vision, image and signal processing_ , 2019, pp. 1–5. 

- [123] J. Leng, S. Fan _et al._ , “M-A3C: A mean-asynchronous advantage actorcritic reinforcement learning method for real-time gait planning of biped robot,” _IEEE Access_ , vol. 10, pp. 76 523–76 536, 2022. 

- [124] C. Yu and A. Rosendo, “Multi-modal legged locomotion framework with automated residual reinforcement learning,” _IEEE Robotics and Automation Letters_ , vol. 7, pp. 10 312–10 319, 2022. 

- [125] C. Tao, J. Xue _et al._ , “Parallel deep reinforcement learning method for gait control of biped robot,” _IEEE Transactions on Circuits and Systems II: Express Briefs_ , vol. 69, pp. 2802–2806, 2022. 

- [126] M. Mittal, C. Yu _et al._ , “Orbit: A unified simulation framework for interactive robot learning environments,” _IEEE Robotics and Automation Letters_ , vol. 8, no. 6, pp. 3740–3747, 2023. 

- [127] C. D. Freeman, E. Frey _et al._ , “Brax – a differentiable physics engine for large scale rigid body simulation,” 2021. [Online]. Available: https://arxiv.org/abs/2106.13281 

- [128] M. Mittal, P. Roth _et al._ , “Isaac lab: A gpuaccelerated simulation framework for multi-modal robot learning,” _arXiv preprint arXiv:2511.04831_ , 2025. [Online]. Available: https://arxiv.org/abs/2511.04831 

