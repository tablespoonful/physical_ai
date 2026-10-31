---
title: "SIMPLE: Simulation-Based Policy Learning and Evaluation for Humanoid Loco-manipulation"
date: "2026-06-06"
authors: "Songlin Wei; Zhenhao Ni; Jie Liu; Zhenyu Zhao; Junjie Ye; Hongyi Jing"
url: https://arxiv.org/abs/2606.08278
pdf: https://arxiv.org/pdf/2606.08278
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.08278)** / [論文ページ](https://arxiv.org/abs/2606.08278)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **SIMPLE: Simulation-Based Policy Learning and Evaluation for Humanoid Loco-manipulation** 

**Songlin Wei**<sup>_∗_</sup> **, Zhenhao Ni**<sup>_∗_</sup> **, Jie Liu**<sup>_∗_</sup> **, Zhenyu Zhao**<sup>_∗_</sup> **,** Junjie Ye, Hongyi Jing, Junkai Xia, Xiawei Liu, Michael Leong, 

Liang Heng, Di Huang, Yue Wang<sup>_†_</sup> 

USC Physical Superintelligence (PSI) Lab 

_∗_ equal contribution,<sup>_†_</sup> corresponding author `https://psi-lab.ai/SIMPLE` 


Figure 1: **Humanoid Loco-manipulation in SIMPLE.** We introduce a comprehensive simulation benchmark designed to standardize the evaluation and training of humanoid foundation models. The framework features 16 diverse whole-body tasks across 50 indoor scenes, utilizing over 1,000 object assets. By coupling MuJoCo’s robust contact physics with Isaac Sim’s photorealistic rendering, SIMPLE provides built-in data collection pipelines and natively benchmarks state-of-the-art VLAs and WAMs. 

**Abstract:** Humanoid foundation models are advancing faster than we can evaluate them. While real-world testing is expensive and difficult to reproduce, existing simulation benchmarks focus primarily on table-top or wheeled robots. A scalable and reproducible benchmark for whole-body humanoid loco-manipulation remains an open problem. To this end, we present SIMPLE, a unified simulation testbed for humanoid policy learning and evaluation. SIMPLE couples the accurate contact-rich dynamics of MuJoCo with the photorealistic rendering of IsaacSim. It provides a large-scale environment comprising 16 diverse wholebody tasks, 50 indoor scenes, and over 1,000 object assets. To facilitate scalable data collection, the framework integrates two data generation pipelines: automated trajectory generation via motion planning and a low-latency VR teleoperation interface. We further integrate and benchmark mainstream humanoid policies at scale in SIMPLE, including lightweight imitation networks, large visionlanguage-action (VLA) models, and recent world action models (WAMs). Our experiments demonstrate that policies trained on data collected in SIMPLE can be transferred zero-shot to physical humanoid robots under similar settings, providing a robust and reproducible foundation for humanoid robotics research. 

**Keywords:** Humanoid Loco-Manipulation, Simulation-based Evaluation, Wholebody Foundation Models 

## **1 Introduction** 

Robotic foundation models [1, 2, 3, 4] are advancing rapidly, demonstrating increasingly general behaviors. However, scaling these models is fundamentally constrained by evaluation. For tabletop and wheeled robots, standardized simulation benchmarks [5, 6, 7, 8] have greatly accelerated progress. Developing equivalent benchmarks for humanoid robots remains an open challenge. Humanoid loco-manipulation is inherently complex, requiring the tight coordination of dynamic locomotion, whole-body balancing, and fine-grained dexterous manipulation. 

Currently, most humanoid foundation models are evaluated directly in the real world. While authentic, real-world evaluation is expensive, time-consuming, and notoriously difficult to reproduce. Consequently, conducting fair, side-by-side comparisons across different policies is a major challenge. Recent efforts to automate real-world evaluation via crowd-sourced rankings [9] or VLM-based reset policies [10] face scalability limits and potential biases. Simulation offers a scalable alternative [11], but existing platforms are highly fragmented. They either focus exclusively on tabletop manipulation [5, 6], ignoring locomotion and whole-body balancing, or on pure locomotion [12, 13], lacking diverse object interactions. 

To address this fragmentation, we present **SIMPLE** , a comprehensive, full-stack simulation testbed designed for the extensive evaluation and fair comparison of humanoid policies. Instead of focusing on a narrow subset of skills, SIMPLE provides a large-scale environment dedicated to whole-body loco-manipulation. We design 16 diverse tasks, spanning rigid object pick-and-place, non-prehensile interaction, and articulated object manipulation. These tasks are set in 50 indoor scenes [14] utilizing over 1,000 object assets [15]. To support this scale with high fidelity, SIMPLE utilizes a hybrid architecture, coupling the accurate contact-rich dynamics of MuJoCo [16] with the photorealistic ray-traced rendering of Isaac Sim [17]. This dual-simulator approach ensures that policies trained in SIMPLE experience both the rigorous physical constraints of real-world locomotion and the complex visual diversity required for robust perception. 

A standardized testbed must also support the full lifecycle of policy development. Beyond evaluation, SIMPLE facilitates scalable data collection by providing two built-in pipelines: automated trajectory generation driven by motion planners [18, 19], and a low-latency VR teleoperation interface for collecting human demonstrations. By standardizing these pipelines, SIMPLE eliminates the engineering overhead typically required to gather high-quality, whole-body demonstration data. Furthermore, the testbed integrates state-of-the-art lower-body controllers [20, 21] and offers a unified interface with native compatibility for mainstream vision-language-action (VLA) architectures, such as Ψ0 [4], _π_ 0 _._ 5 [3], and GR00T-N1.6 [1], as well as World-Action-Models (WAMs) like DreamZero [2] and other recent models [22, 23]. Crucially, SIMPLE is designed to be fully portable. This modularity enables researchers to easily extend the framework with new tasks, objects, environments, and policies. 

We conduct extensive evaluations on SIMPLE to benchmark state-of-the-art policies at scale. Our experiments reveal a strong correlation between policy performance in simulation and in the real world. We further demonstrate that policies trained on data collected in SIMPLE can be transferred zero-shot to physical humanoid robots under similar settings. Our contributions are threefold: 

- We introduce SIMPLE, a hybrid full-stack simulation framework standardizing the evaluation of humanoid loco-manipulation. 

- We construct a large-scale loco-manipulation environment comprising 16 diverse tasks, over 1,000 objects, and 50 scenes, alongside built-in pipelines for automated and teleoperated data collection, yielding over 6,000 trajectories. 

- We conduct extensive benchmarking of mainstream VLA and WAM policies, demonstrating strong sim-to-real correlation and effective zero-shot policy transfer. 

2 

## **2 Related Work** 

### **2.1 Robot Policy Evaluation in the Real World** 

Evaluating generalist policies [3, 1, 24, 25, 4] directly in the real world is the current standard but presents significant scalability challenges. Fair and reproducible evaluation requires multiple rollouts with meticulous environment resets, which are difficult to standardize and prone to humanoperator bias. To address this, prior works have proposed using 3D-printable assets [26, 27] or centralized physical testbeds [28], though these still require substantial human supervision. While AutoEval [10] employs large language models (LLMs) to automate resets, the robustness of LLMbased physical interventions remains suboptimal. Alternatively, RoboArena [9] mitigates human bias via a decentralized, double-blind evaluation protocol. However, while effective for zero-shot testing on controlled tabletop setups with standardized datasets [29], this paradigm does not easily extend to humanoids. Because large-scale humanoid data is scarce, evaluating VLA models typically requires collecting in-domain demonstrations for policy fine-tuning prior to testing. Both collecting these demonstrations and conducting subsequent physical evaluations involve highly dynamic, fullbody motions with heavy hardware, significantly increasing operational complexity and safety risks. Consequently, while real-world evaluation remains the gold standard, relying on it for the rapid, iterative development of humanoid policies is highly impractical. 

### **2.2 Simulation-Based Benchmarks for Manipulation** 

Simulation provides a scalable, reproducible, and automated alternative to real-world testing [30]. Benchmarks such as RLBench [31] and LIBERO [7] have driven significant progress in tabletop single-arm manipulation, while platforms like RoboCasa [32], Behavior-1K [8], MolmoSpaces [33], and ManiSkill-HAB [34] have extended evaluation to mobile manipulation. Crucially, Simpler-Env [11] demonstrated that simulation can serve as a faithful proxy for real-world evaluation. By identifying and mitigating visual and control gaps, they showed that policy performance in simulation is highly correlated with real-world rankings. More recently, RoboTwin [5] introduced extensive domain randomization for bimanual tasks, and RoboVerse [6] unified multiple benchmarks within IsaacLab [35]. However, these platforms are typically built on physics engines or configurations optimized exclusively for fixed-base or wheeled robots [36]. Consequently, they lack the necessary physics support and integration for humanoid whole-body loco-manipulation. 

### **2.3 Simulation for Humanoid Loco-Manipulation** 

Simulation has long been the primary paradigm for training robust humanoid locomotion policies before real-world deployment. Recent frameworks like AMO [20] and SONIC [21] leverage massively parallel reinforcement learning in IsaacGym [37] and IsaacLab [35] to train highly stable lower-body and whole-body tracking networks. These locomotion-focused policies are frequently deployed and evaluated in MuJoCo [16] due to its superior contact fidelity. However, while these environments excel at locomotion, they lack the diverse object assets, complex indoor scenes, and photorealistic rendering required to train and evaluate generalist foundation models. Conversely, platforms capable of high-fidelity rendering (such as those built on PhysX) often struggle to provide the accurate, high-frequency contact dynamics necessary for stable humanoid locomotion and delicate hand-object interaction. SIMPLE bridges this divide by natively building upon MuJoCo [16] for superior contact fidelity, ensuring compatibility with state-of-the-art locomotion policies, while coupling it with Isaac Sim’s photorealistic rendering [17]. To the best of our knowledge, SIMPLE is the first comprehensive, full-stack simulation testbed dedicated to whole-body humanoid locomanipulation, seamlessly integrating data generation, policy learning, and standardized evaluation. 

## **3 Method** 

We present SIMPLE, a comprehensive simulation infrastructure designed for humanoid locomanipulation. The framework integrates dual-simulators for physics and rendering, large-scale asset curation, built-in data collection pipelines, and a standardized evaluation protocol. The overall system pipeline is illustrated in Fig. 2. 

3 


Figure 2: **System Pipeline.** Our pipeline consists of three stages: (1) data generation in MuJoCo via motion planning and teleoperation; (2) offline replay and rendering in Isaac Sim to obtain photorealistic visual observations; and (3) policy evaluation under diverse domain-randomized settings. 

### **3.1 System Architecture** 

SIMPLE employs a dual-simulator architecture that strictly decouples physical simulation from visual rendering. As shown in Fig. 3, MuJoCo [16] handles all rigid-body dynamics, contact resolution, and robot control. At each simulation step, the physical states of the robot and environment are synchronized to Isaac Sim [17], which performs photorealistic ray-traced rendering. This separation allows SIMPLE to harness both the superior contact fidelity and locomotion stability of MuJoCo and the high-quality visual diversity of Isaac Sim. 

To support generalist foundation models, SIMPLE implements a decoupled whole-body control scheme. The high-level policy ( _e.g._ , a VLA) predicts kinematic trajectories for the upper body and navigation commands for the base. These commands are subsequently passed to a state-of-the-art lower-body tracking controller [20, 21, 1], which operates at a higher frequency to main- 


Figure 3: **System Diagram.** MuJoCo simulates physical interactions, while Isaac Sim synchronizes states and renders photorealistic images for policy inference. 

tain balance and execute locomotion. To ensure seamless integration with existing reinforcement learning workflows, the entire simulation loop is wrapped in a standard OpenAI Gym interface [38], as detailed in Algorithm 1. 

|**Algorithm 1**Core PolicyEvaluation Workflow in SIMPLE<br>||
|---|---|
|1: import gymnasium as gym|_▷_Gym-style API|
|2: env = gym.make(_”_G1WholebodyXmovePickTeleop-v0_”_,||
|3:<br>render<br>~~m~~odel=_”_mujoco<br>~~i~~saacsim_”_)|_▷_Create Dual-Sim Env|
|4: agent = Psi0Agent(env.robot)|_▷_Instantiate VLA Agent|
|5: env = LerobotEnv(env)|_▷_Wrapper for trajectory recording|
|6: obs, info = env.reset()|_▷_Initialize environment|
|7: **while**not (terminated or truncated)**do**|_▷_50 Hz control loop|
|8:<br>action = agent.get<br>~~a~~ction(obs, info, instruction)|_▷_Policy inference|
|9:<br>obs, info, truncated, terminated = env.step(action)|_▷_Advance simulation|
|10: **end while**||


### **3.2 Large-Scale Asset Curation and Task Design** 

To ensure sufficient diversity for training robust vision-language-action models, we curated a massive library of objects and environments. We imported 53 objects from GraspNet-1B [26] and over 1,500 diverse objects from Objaverse [15]. To guarantee stable physics in MuJoCo, all object meshes underwent convex decomposition via CoACD [39] to generate accurate collision geometries. Simultaneously, all assets were converted into USD format with high-resolution textures for Isaac Sim 

4 


Figure 4: **Automated Motion Planning.** Based on task decomposition, scripted policies coordinate upper-body manipulation via motion planning and lower-body movement to generate automated demonstrations. 

rendering. To move beyond isolated tabletop setups, we integrated 50 complete indoor scenes from the HSSD dataset [14]. Using these assets, we designed 60 distinct whole-body loco-manipulation tasks, encompassing rigid object pick-and-place, non-prehensile interactions, and articulated object manipulation. Detailed illustrations of each task and other entities are included in the class diagrams provided in the Appendix. 

### **3.3 Scalable Data Collection Pipelines** 

A core feature of SIMPLE is its built-in infrastructure for generating the large-scale demonstration data required to fine-tune humanoid policies. We provide two distinct pipelines: automated motion planning and human teleoperation. 

**Automated Motion Planning.** For scalable trajectory generation, we implemented an automated pipeline driven by CuRobo [18], as illustrated in Fig. 4. To ensure physically plausible grasping, objects are first dropped in MuJoCo to determine their stable resting poses. These stable poses are then processed by BoDex [19] to synthesize feasible grasp configurations. During task execution, a scripted policy decomposes the high-level objective into atomic actions. CuRobo generates the kinematic trajectories for the dual arms to execute the grasp, while a scripted lower-body policy coordinates the necessary base movements to reach the target. We detail the grasp synthesis process and trajectory decomposition in the Appendix. 

**Low-Latency VR Teleoperation.** Because motion planning struggles with complex dexterous manipulation, we also integrated a human teleoperation pipeline. To minimize latency, Isaac Sim rendering is disabled during data collection. Instead, MuJoCo’s native renderer streams egocentric stereo video directly to a PICO XR headset. The operator’s hand movements are retargeted to the humanoid’s upper body via inverse kinematics, while a whole-body tracking policy [20, 21] autonomously manages the robot’s balance and locomotion based on the operator’s joystick inputs. This decoupled approach drastically reduces the operator’s cognitive load. Demonstrations are recorded at 50 Hz and automatically exported into the standardized LeRobot format [40]. 

### **3.4 Offline Rendering and Domain Randomization** 

To close the visual sim-to-real gap, trajectories collected via motion planning or teleoperation are replayed offline in Isaac Sim. During this replay phase, we apply extensive domain randomization. We randomize object instances, initial poses, tabletop textures, lighting conditions, camera viewpoints, and language instructions. Specifically, we utilize NVIDIA vMaterials [41] to inject high-quality, diverse surface properties into the scenes. This offline rendering pipeline enables the generation of high-quality RGB observations under diverse visual conditions for downstream policy learning and evaluation. 

### **3.5 Policy Integration and Evaluation Protocol** 

To standardize evaluation, SIMPLE defines a strict protocol with three progressively difficult levels. Level 1 introduces random distractor objects into the scene. Level 2 adds visual randomization, altering object materials and environmental lighting to test perceptual robustness. Level 3 introduces spatial randomization, varying the initial positions of both the target objects and the robot to evaluate layout generalization. 

5 

For policy integration, SIMPLE natively supports the Ψ0 [4] training stack. The standard wholebody representation consists of a 32-dimensional proprioceptive state (14 DoF hands, 14 DoF arms, waist roll-pitch-yaw, and base height). The action space is 36-dimensional, comprising the 32dimensional upper-body targets and 4-dimensional locomotion commands ( _vx, vy, vyaw, qyaw_ ). Using this unified interface, we rendered 6,000 episodes to facilitate the large-scale benchmarking of mainstream VLA and WAM architectures. 

## **4 Experiments** 

In this section, we evaluate the utility and scalability of the SIMPLE benchmark. We first present the results of our large-scale benchmarking, where state-of-the-art VLA models and WAMs are evaluated in a controlled environment across multiple tasks. We then assess the efficiency of our data generation pipelines. Next, we conduct ablation studies to analyze the impact of domain randomization, data scaling, and data sources on policy learning. Finally, we evaluate the feasibility of transferring policies trained entirely in SIMPLE to the real world in a zero-shot manner. 

### **4.1 Benchmarking of Humanoid Policies** 

To benchmark state-of-the-art humanoid models, we select six representative tasks and fine-tune each baseline using 100 demonstrations for each task, and then evaluate them across the three domain-randomization levels defined in Section 3.5. 

|**Baseline**|**XMovePick**|**BendPick**|**Handover**|**Mobile P&P**|**Grasp**|**XMoveBendPick**|
|---|---|---|---|---|---|---|
|Ψ0 [4]|10 / 10 / 6|**10 / 10 / 10**|**7 / 7 / 10**|**7 / 5 / 6**|**10 / 10 / 8**|10<br>/<br>9<br>/<br>9|
|GR00T N1.6 [1]|10<br>/<br>10<br>/<br>7|7 / 7 / 6|1 / 3 / 3|0 / 0 / 0|9 / 9 / 7|4 / 4 / 1|
|_π_0_._5 [3]|7 / 5 / 1|10<br>/<br>10<br>/<br>8|5 / 4 / 5|3 / 3 / 3|**10 / 10 / 8**|0 / 0 / 0|
|DreamZero [2]|**10 / 10 / 10**|9 / 9 / 8|7<br>/<br>8<br>/<br>9|5 / 3 / 3|9 / 10 / 7|0 / 0 / 1|
|Cosmos3 [42]|10 / 10 / 8|0 / 0 / 0|7 / 10 / 7|7 / 5 / 2|3 / 3 / 3|5 / 2 / 1|
|DP [43]|3 / 3 / 2|10 / 8 / 6|3 / 2 / 4|4 / 0 / 0|8 / 9 / 8|0 / 0 / 0|
|ACT [44]|10 / 10 / 5|10 / 9 / 9|**7 / 7 / 10**|5<br>/<br>5<br>/<br>5|**10 / 10 / 8**|**9 / 10 / 10**|


Table 1: **Single-Task Fine-Tuning Results.** Each entry reports performance under three domainrandomization levels ( _Level 0 / Level 1 / Level 2_ ). **Boldface** indicates the best performance, and <u>underlined</u> values indicate the second best. The six task labels are `XMovePickTeleop-v0` , `BendPickMP-v0` , `HandoverTeleop-v0` , `LocomotionPickBetweenTablesTeleop-v0` , `Table topGraspMP-v0` , and `XMoveBendPickTeleop-v0` , where the suffix _MP_ denotes motion planning and _Teleop_ denotes teleoperation. 

**Baselines.** The evaluated baseline models are categorized into four groups: **(1) VLA Models.** Ψ0 [4] is a 2.5B universal humanoid foundation model specialized for rapid adaptation through fine-tuning. We also evaluate _π_ 0 _._ 5 [3] and GR00T-N1.6 [1], two seminal VLA models for general robotics, carefully adapting their pre-trained weights to the humanoid embodiment. **(2) WorldAction Models.** DreamZero [2] extends video generation models to simultaneously predict future video frames and actions. By imagining future interactions during execution, the video prediction mechanism serves as planning in image space. We also include Cosmos3-Nano [42], a recent worldaction model that jointly generates video and actions. **(3) Imitation Learning Baselines.** Because our benchmark utilizes single-task fine-tuning, we also include two classic visual imitation learning baselines, Diffusion policy (DP) [43] and Action Chunk Transformers (ACT) [44]. 

**Experimental Results.** Additional details regarding the adaptation of each baseline are provided in the Appendix. As shown in Table 1, Ψ0 consistently performs well across most tasks and leads the benchmark. DreamZero and _π_ 0 _._ 5 demonstrate strong generalization performance on _level 2_ across most tasks, with the exception of Task 6, likely because it requires highly precise base movements. Interestingly, the relatively small ACT model achieves strong overall performance, which we attribute to its data efficiency on _single task overfitting_ of the SIMPLE dataset, whose demonstrations 

6 

||**T1: Whole-B**|**ody Pick-Place**|**T2: Stand-**|**Still Handover**|**T3: Mobi**|**le Pick-Place**|
|---|---|---|---|---|---|---|
|**Collection Method**|**Demos/hr**_↑_|**Avg. time (s)**_↓_|**Demos/hr**_↑_|**Avg. time (s)**_↓_|**Demos/hr**_↑_|**Avg. time (s)**_↓_|
|Motion Planning (Sim)|58.9|61.1|32.7|109.8|24.0|150.0|
|Teleoperation (Real)|206.8|17.4|130.9|`27.5`|87.2|41.3|
|Teleoperation (Sim)|**310.3**|**11.6**|**197.8**|**18.2**|**156.5**|**23.0**|


Table 2: **Data Collection Efficiency.** Each cell reports the number of demonstrations collected per hour and the mean episode duration in seconds. Motion planning runs without an operator; teleoperation figures reflect a single experienced operator per session. 

|**Task**|**Training data**|**Eval Set 0**|**Eval Set 1**|**Eval Set 2**|
|---|---|---|---|---|
|BendHandover|10_×_Level 0|**8/10 = 0.80**|**8/10 = 0.80**|5/10 = 0.50|
||5_×_Level 0 + 5_×_Level 1|**8/10 = 0.80**|7/10 = 0.70|**8/10 = 0.80**|
|XmoveBendPick|10 Trajectories (Teleop)|5/10 = 0.50|6/10 = 0.60|3/10 = 0.30|
||100 Trajectories (Teleop)|**10/10 = 1.00**|**9/10 = 0.90**|**9/10 = 0.90**|


Table 3: **Ablation Study on Domain Randomization.** Evaluation success rates of Ψ0 fine-tuned for 2,000 training steps under different training data compositions. Training with mixed domainrandomization levels improves generalization to harder evaluation settings. Scaling up teleoperation data further improves performance. 

are less noisy than real-world teleoperation data. To complement the single-task finetuning results, multi-task benchmarking results of the foundation models are provided in Appendix A.5. 

### **4.2 Data Collection Efficiency in the Simulator** 

A key motivation for building SIMPLE is to reduce the cost and effort of collecting high-quality robot demonstration data. We compare three data collection paradigms across three representative tasks: _whole-body pick-and-place_ (T1), _stand-still handover_ (T2), and _mobile pick-and-place_ (T3). The three paradigms are: (1) **Motion planning (MP)** in simulation, which generates demonstrations autonomously without a human operator; (2) **Real-robot teleoperation** , where an operator collects demonstrations directly on physical hardware; and (3) **Sim teleoperation** , where a human operator controls the robot inside SIMPLE via the VR interface; 

We measure collection throughput in demonstrations per hour (demos/hr) and average episode duration (seconds), as reported in Table 2. Motion planning achieves the lowest throughput due to the difficulty of optimization in high-dimensional spaces; however, it does not incur operator fatigue or hardware reset overhead. Real-robot teleoperation achieves higher efficiency and captures more natural whole-body motions than motion-planning-based scripted policies. Conversely, Sim teleoperation is substantially faster because it avoids physical reset overhead, safety constraints, and hardware maintenance. Beyond raw time efficiency, simulated data collection is fundamentally more scalable. It eliminates the need for physical humanoid hardware, requiring only a standard VR headset, and allows collected trajectories to be infinitely scaled across diverse environments, lighting conditions, and object instances via offline replay and rendering. 

### **4.3 Ablation Studies** 

**Domain Randomization and Data Scaling.** Domain randomization (DR) is central to bridging the visual sim-to-real gap. We ablate the effect of training data composition on cross-level generalization using Ψ0 fine-tuned for 2,000 steps. As reported in Table 3, training on Level 0 data alone yields a strong in-distribution success rate (0.80 at Eval Set 0) but generalizes poorly to harder visual conditions (0.50 at Eval Set 2). Mixing Level 0 and Level 1 training data maintains in-distribution performance while substantially improving out-of-distribution robustness (0.80 on Set 2). This confirms that exposure to diverse visual conditions during training is necessary for policies to transfer to challenging environments. The results motivate the mixed-DR evaluation strategy adopted in the main benchmark (Table 1). Furthermore, we found that increasing the amount of teleoperation data significantly improves performance across all three validation sets. 

7 

|**Variant **|**BendPick **|**Mobile P&P **|**XMoveBendPick **|**Avg.**|**Task**|**Sim Eval**|**Real Eval**|
|---|---|---|---|---|---|---|---|
|MP<br>Teleop|**10/10/10**<br>8/8/6|3/2/2<br>**7/5/6**|4/2/2<br>**10/9/9**|5.00<br>**7.56**|Pick & Place<br>Handover<br>XMoveBendCarryBox|9/10 = 0.90<br>10/10 = 1.00 <br>7/10 = 0.70|8/10 = 0.80<br> 8/10 = 0.80<br>5/10 = 0.50|


Table 4: **Ablation Study on Data Source.** We compare motion-planning-only and teleoperation-only training data across three task families. Teleoperation data leads to better performance. 

Table 5: **Zero-Shot Sim-to-Real Transfer.** Fine-tuned exclusively on simulation data, evaluated both in the simulator and directly in the real world. 

**Data Source Quality.** To study the impact of different data sources, we fine-tune Ψ0 [4] on three tasks using either motion-planning-only data or teleoperation-only data (Table 4). In general, human teleoperation data proves more suitable for learning complex tasks, which we attribute to its diverse and naturalistic motion profiles. 

### **4.4 Zero-Shot Sim-to-Real Transfer** 

While SIMPLE is primarily designed as a simulation benchmark, we investigate whether policies trained exclusively on SIMPLE data can transfer to the real world. Because real-world evaluation is highly constrained, we perform this evaluation on a subset of tasks under similar environmental settings, as illustrated in Figure 5. As shown in Table 5, we observe that the learned Ψ0 policy generalizes to the real world in a zero-shot fashion without requiring real-world data for downstream fine-tuning. This suggests that the high-fidelity physics and photorealistic rendering provided by SIMPLE are sufficient to cross the sim-to-real gap for certain loco-manipulation tasks. 


Figure 5: **Sim-to-Real Task Observations.** Each task is shown as an adjacent simulation–real pair, with the simulated egocentric view on the left and the corresponding real egocentric view on the right. The left pair shows the pick-and-place task, and the right pair shows the handover task. 

### **4.5 Whole-Body Task Coverage** 

Beyond tabletop manipulation, SIMPLE includes whole-body tasks that require coordinated arm– leg motion, such as _XMovePushBox_ , _KickBox_ , and _XMoveBendCarryBox_ . Figure 6 illustrates _XMoveBendCarryBox_ , where the robot kneels to lower its torso and then wraps both arms around the box to lift it onto the table. The same task is also included in our sim-to-real evaluation (Table 5). 


Figure 6: **Whole-Body Task Example.** Three frames of _XMoveBendCarryBox_ : the robot approaches the box, kneels to wrap both arms around it, and lifts it onto the table. 

### **4.6 Physics–Rendering Consistency** 

Because physics and rendering run in separate engines, we verify that the collision meshes simulated in MuJoCo stay aligned with the visual meshes rendered in Isaac Sim. Figure 7 compares the two from the robot’s egocentric view; they are closely aligned across frames, as evidenced by the consistent table surfaces, cuboid object edges, and humanoid torso. We also note that the _∼_ 4 fps rendering 

8 

throughput is bound by the _synchronized_ render mode of Isaac Sim. It can be mitigated by parallelizing environments during offline data generation or policy inference, in which case throughput is bottlenecked only by available compute. 


Figure 7: **Visual–Physics Mesh Alignment.** Two egocentric frames, each shown as a pair with the Isaac Sim visual rendering on the left and the corresponding MuJoCo physics rendering on the right. 

### **4.7 Simulation Parameters in MuJoCo** 

Table 6 lists the main tuned simulation parameters, covering actuator, solver, and contact settings, except for the control gains, which vary with the whole-body controller (AMO or SONIC). These were extensively tested to ensure stable and realistic simulation: (1) maximum force limits are enforced for all leg, arm, and finger joints; (2) joint friction introduces a dead zone that prevents small torques from inducing unintended motion; (3) viscous damping suppresses joint oscillations; and (4) joint armature adds rotational inertia to improve numerical stability. 

|**Parameter**|**Default**|**Type**|**Parameter**|**Default**|**Type**|
|---|---|---|---|---|---|
|`actuatorfrclimited`|true|Actuator|`impratio`|10|Solver|
|`frictionloss`|0.2|Actuator|`cone`|elliptic|Contact|
|`damping`|2|Actuator|`solref`|0.005 1|Contact|
|`armature`|0.05|Actuator|`solimp`|0.9 0.95 0.001|Contact|
|`integrator`|implicitfast|Solver|_Kp_/_Kd_|_varied_|Control|


Table 6: **Simulation Parameters in MuJoCo.** Main tuned physics and actuator parameters shared across all tasks. Control gains vary with the whole-body controller (AMO or SONIC). 

## **5 Conclusion** 

We presented SIMPLE, a full-stack simulation infrastructure designed to standardize the evaluation and training of humanoid policies. By coupling the robust contact physics of MuJoCo with the photorealistic rendering of Isaac Sim, SIMPLE provides a high-fidelity environment tailored for whole-body loco-manipulation. The framework features a large-scale benchmark comprising 16 diverse tasks, over 1,000 objects, and 50 indoor scenes. To facilitate scalable policy learning, SIMPLE integrates built-in data collection pipelines for both automated motion planning and low-latency VR teleoperation. Our extensive benchmarking of state-of-the-art VLA and WAM architectures demonstrates that performance in SIMPLE strongly correlates with real-world outcomes, and that data generated in SIMPLE empowers effective sim-to-real transfer. We hope SIMPLE will serve as a reproducible and scalable foundation to accelerate future research in humanoid robotics. 

**Limitations.** Despite these contributions, SIMPLE has several limitations that point toward future work. _(1) Rendering throughput._ The photorealistic ray-tracing pipeline in Isaac Sim is computationally expensive. A single GPU renders _∼_ 4 frames per second, making large-scale dataset generation time-intensive. _(2) Rigid-body assumption._ The current simulation pipeline models all objects as rigid bodies. Deformable and soft-body objects such as cloth, rope, or food items cannot be faithfully simulated within the current framework. 

9 

### **Acknowledgments** 

We thank Weiduo Yuan for assistance in setting up the multi-task fine-tuning of DreamZero, Jingxuan Wang and Junsoo Kim for support in integrating the SONIC whole-body controller, and Andrew Park for their help in testing SIMPLE. 

## **References** 

- [1] J. Bjorck, F. Casta˜neda, N. Cherniadev, X. Da, R. Ding, L. Fan, Y. Fang, D. Fox, F. Hu, S. Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- [2] S. Ye, Y. Ge, K. Zheng, S. Gao, S. Yu, G. Kurian, S. Indupuru, Y. L. Tan, C. Zhu, J. Xiang, et al. World action models are zero-shot policies. _arXiv preprint arXiv:2602.15922_ , 2026. 

- [3] P. Intelligence, K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, et al. _π_ 0 _._ 5: A vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 

- [4] S. Wei, H. Jing, B. Li, Z. Zhao, J. Mao, Z. Ni, S. He, J. Liu, X. Liu, K. Kang, et al. Ψ0: An open foundation model towards universal humanoid loco-manipulation. _arXiv preprint arXiv:2603.12263_ , 2026. 

- [5] T. Chen, Z. Chen, B. Chen, Z. Cai, Y. Liu, Z. Li, Q. Liang, X. Lin, Y. Ge, Z. Gu, et al. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. _arXiv preprint arXiv:2506.18088_ , 2025. 

- [6] H. Geng, F. Wang, S. Wei, Y. Li, B. Wang, B. An, C. T. Cheng, H. Lou, P. Li, Y.-J. Wang, et al. Roboverse: Towards a unified platform, dataset and benchmark for scalable and generalizable robot learning. _arXiv preprint arXiv:2504.18904_ , 2025. 

- [7] B. Liu, Y. Zhu, C. Gao, Y. Feng, Q. Liu, Y. Zhu, and P. Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791, 2023. 

- [8] C. Li, R. Zhang, J. Wong, C. Gokmen, S. Srivastava, R. Mart´ın-Mart´ın, C. Wang, G. Levine, M. Lingelbach, J. Sun, et al. Behavior-1k: A benchmark for embodied ai with 1,000 everyday activities and realistic simulation. In _Conference on Robot Learning_ , pages 80–93. PMLR, 2023. 

- [9] P. Atreya, K. Pertsch, T. Lee, M. J. Kim, A. Jain, A. Kuramshin, C. Eppner, C. Neary, E. Hu, F. Ramos, et al. Roboarena: Distributed real-world evaluation of generalist robot policies. In _Proceedings of the Conference on Robot Learning (CoRL 2025)_ , 2025. 

- [10] Z. Zhou, P. Atreya, Y. L. Tan, K. Pertsch, and S. Levine. Autoeval: Autonomous evaluation of generalist robot manipulation policies in the real world. _arXiv preprint arXiv:2503.24278_ , 2025. 

- [11] X. Li, K. Hsu, J. Gu, K. Pertsch, O. Mees, H. R. Walke, C. Fu, I. Lunawat, I. Sieh, S. Kirmani, et al. Evaluating real-world robot manipulation policies in simulation. _arXiv preprint arXiv:2405.05941_ , 2024. 

- [12] C. L. Lab. Humanoidverse: A multi-simulator framework for humanoid robot sim-to-real learning. `https://github.com/LeCAR-Lab/HumanoidVerse` , 2025. 

- [13] C. Sferrazza, D.-M. Huang, X. Lin, Y. Lee, and P. Abbeel. Humanoidbench: Simulated humanoid benchmark for whole-body locomotion and manipulation, 2024. 

10 

- [14] M. Khanna, Y. Mao, H. Jiang, S. Haresh, B. Shacklett, D. Batra, A. Clegg, E. Undersander, A. X. Chang, and M. Savva. Habitat synthetic scenes dataset (hssd-200): An analysis of 3d scene scale and realism tradeoffs for objectgoal navigation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 16384–16393, 2024. 

- [15] M. Deitke, D. Schwenk, J. Salvador, L. Weihs, O. Michel, E. VanderBilt, L. Schmidt, K. Ehsani, A. Kembhavi, and A. Farhadi. Objaverse: A universe of annotated 3d objects. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 13142–13153, 2023. 

- [16] E. Todorov, T. Erez, and Y. Tassa. Mujoco: A physics engine for model-based control. In _2012 IEEE/RSJ international conference on intelligent robots and systems_ , pages 5026–5033. IEEE, 2012. 

- [17] NVIDIA. Isaac Sim. URL `https://github.com/isaac-sim/IsaacSim` . 

- [18] B. Sundaralingam, A. Murali, and S. Birchfield. curobov2: Dynamics-aware motion generation with depth-fused distance fields for high-dof robots, 2026. 

- [19] J. Chen, Y. Ke, and H. Wang. Bodex: Scalable and efficient robotic dexterous grasp synthesis using bilevel optimization. _arXiv preprint arXiv:2412.16490_ , 2024. 

- [20] J. Li, X. Cheng, T. Huang, S. Yang, R. Qiu, and X. Wang. Amo: Adaptive motion optimization for hyper-dexterous humanoid whole-body control. _Robotics: Science and Systems 2025_ , 2025. 

- [21] Z. Luo, Y. Yuan, T. Wang, C. Li, S. Chen, F. Castaneda, Z.-A. Cao, J. Li, D. Minor, Q. Ben, et al. Sonic: Supersizing motion tracking for natural humanoid whole-body control. _arXiv preprint arXiv:2511.07820_ , 2025. 

- [22] R. Yang, Q. Yu, Y. Wu, R. Yan, B. Li, A.-C. Cheng, X. Zou, Y. Fang, X. Cheng, R.-Z. Qiu, et al. Egovla: Learning vision-language-action models from egocentric human videos. _arXiv preprint arXiv:2507.12440_ , 2025. 

- [23] H. Bi, L. Wu, T. Lin, H. Tan, Z. Su, H. Su, and J. Zhu. H-rdt: Human manipulation enhanced bimanual robotic manipulation. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 40, pages 18135–18143, 2026. 

- [24] S. Deng, M. Yan, S. Wei, H. Ma, Y. Yang, J. Chen, Z. Zhang, T. Yang, X. Zhang, W. Zhang, et al. Graspvla: a grasping foundation model pre-trained on billion-scale synthetic action data. _arXiv preprint arXiv:2505.03233_ , 2025. 

- [25] J. Zhang, K. Wang, S. Wang, M. Li, H. Liu, S. Wei, Z. Wang, Z. Zhang, and H. Wang. Uninavid: A video-based vision-language-action model for unifying embodied navigation tasks. _arXiv preprint arXiv:2412.06224_ , 2024. 

- [26] H.-S. Fang, C. Wang, M. Gou, and C. Lu. Graspnet-1billion: A large-scale benchmark for general object grasping. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 11444–11453, 2020. 

- [27] S. Wei, H. Geng, J. Chen, C. Deng, C. Wenbo, C. Zhao, X. Fang, L. Guibas, and H. Wang. D3roma: Disparity diffusion-based depth sensing for material-agnostic robotic manipulation. In _8th Annual Conference on Robot Learning_ , 2024. URL `https://openreview.net/ forum?id=7E3JAys1xO` . 

- [28] A. Yakefu, B. Xie, C. Xu, E. Zhang, E. Zhou, F. Jia, H. Yang, H. Fan, H. Zhang, H. Peng, et al. Robochallenge: Large-scale real-robot evaluation of embodied policies. _arXiv preprint arXiv:2510.17950_ , 2025. 

11 

- [29] A. Khazatsky, K. Pertsch, S. Nair, A. Balakrishna, and S. D. et al. DROID: A Large-Scale In-The-Wild Robot Manipulation Dataset. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2024. doi:10.15607/RSS.2024.XX.120. 

- [30] Y. R. Wang, C. Ung, G. Tannert, J. Duan, J. Li, A. Le, R. Oswal, M. Grotz, W. Pumacay, Y. Deng, et al. Roboeval: Where robotic manipulation meets structured and scalable evaluation. _arXiv preprint arXiv:2507.00435_ , 2025. 

- [31] S. James, Z. Ma, D. R. Arrojo, and A. J. Davison. Rlbench: The robot learning benchmark & learning environment. _IEEE Robotics and Automation Letters_ , 5(2):3019–3026, 2020. 

- [32] S. Nasiriany, S. Nasiriany, A. Maddukuri, and Y. Zhu. Robocasa365: A large-scale simulation framework for training and benchmarking generalist robots. In _International Conference on Learning Representations (ICLR)_ , 2026. 

- [33] Y. Kim, W. Pumacay, O. Rayyan, M. Argus, W. Han, E. VanderBilt, J. Salvador, A. Deshpande, R. Hendrix, S. Jauhri, S. Liu, N. M. M. Shafiullah, M. Guru, A. Guru, A. Eftekhar, K. Farley, D. Clay, J. Duan, P. Wolters, A. Herrasti, Y.-C. Lee, G. Chalvatzaki, Y. Cui, A. Farhadi, D. Fox, and R. Krishna. Molmospaces: A large-scale open ecosystem for robot navigation and manipulation, 2026. 

- [34] A. Shukla, S. Tao, and H. Su. Maniskill-hab: A benchmark for low-level manipulation in home rearrangement tasks. _arXiv preprint arXiv:2412.13211_ , 2024. 

- [35] M. Mittal, P. Roth, J. Tigue, A. Richard, O. Zhang, P. Du, A. Serrano-Munoz, X. Yao, R. Zurbr¨ugg, N. Rudin, et al. Isaac lab: A gpu-accelerated simulation framework for multimodal robot learning. _arXiv preprint arXiv:2511.04831_ , 2025. 

- [36] Y. Chen, S. Wei, B. Xiao, J. Lyu, J. Chen, F. Zhu, and H. Wang. Robohanger: Learning generalizable robotic hanger insertion for diverse garments. _IEEE Robotics and Automation Letters_ , 2025. 

- [37] V. Makoviychuk, L. Wawrzyniak, Y. Guo, M. Lu, K. Storey, M. Macklin, D. Hoeller, N. Rudin, A. Allshire, A. Handa, et al. Isaac gym: High performance gpu-based physics simulation for robot learning. _arXiv preprint arXiv:2108.10470_ , 2021. 

- [38] G. Brockman, V. Cheung, L. Pettersson, J. Schneider, J. Schulman, J. Tang, and W. Zaremba. Openai gym. _arXiv preprint arXiv:1606.01540_ , 2016. 

- [39] X. Wei, M. Liu, Z. Ling, and H. Su. Approximate convex decomposition for 3d meshes with collision-aware concavity and tree search. _ACM Transactions on Graphics (TOG)_ , 41(4):1–18, 2022. 

- [40] R. Cadene, S. Aliberts, F. Capuano, M. Aractingi, A. Zouitine, P. Kooijmans, J. Choghari, M. Russi, C. Pascal, S. Palma, et al. Lerobot: An open-source library for end-to-end robot learning. _arXiv preprint arXiv:2602.22818_ , 2026. 

- [41] NVIDIA. vmaterials. `https://developer.nvidia.com/vmaterials` , 2026. Accessed: 2026-05-24. 

- [42] NVIDIA. Cosmos 3: Omnimodal world models for physical AI. _arXiv preprint arXiv:2606.02800_ , 2026. 

- [43] C. Chi, Z. Xu, S. Feng, E. Cousineau, Y. Du, B. Burchfiel, R. Tedrake, and S. Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , 44(10-11):1684–1704, 2025. 

- [44] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn. Learning fine-grained bimanual manipulation with low-cost hardware. _arXiv preprint arXiv:2304.13705_ , 2023. 

12 


Figure 8: **Class Diagram of the SIMPLE Framework.** `BaseDualSimEnv` owns two `Simulator` instances and a `Task` , and exposes a standard Gym interface. `Task` composes a `DomainRandomizer` and a `Robot` and drives scene randomization at each reset. The `Agent` hierarchy (teleoperation, motion planning, remote inference) shares a unified `get` ~~`a`~~ `ction` interface, while whole-body controllers ( `AmoWBC` , `SonicWBC` , `SonicDecoupledWBC` ) translate high-level commands into low-level joint targets. Policy servers ( `Psi0Server` , `Pi05Server` , `GR00TServer` ) run as independent processes and are accessed over HTTP or WebSocket. 

## **Supplementary Material** 

This document provides five supplementary sections. §A.1 details the SIMPLE class hierarchy and the per-step message-passing sequence between MuJoCo and Isaac Sim. §A.2 describes the offline asset preprocessing pipeline for physics collision geometries, USD rendering assets, and grasp synthesis. §A.3 gives the fine-tuning hyperparameters and embodiment adaptations for each evaluated baseline. §A.4 describes the two whole-body locomotion controllers (AMO and SONIC) integrated in SIMPLE. §A.5 reports multi-task benchmarking results of the foundation models across all 16 tasks, followed by the complete task list. 

### **A.1 System Architecture Details** 

### **A.1.1 Main Class Entities** 

Figure 8 shows the class hierarchy of SIMPLE; we describe each component below. 

**BaseDualSimEnv.** `BaseDualSim` ( `envs/base` ~~`d`~~ `ual` ~~`e`~~ `nv.py` ) is the central `gymnasium.Env` that holds references to both a `MujocoSimulator` and an `IsaacSimSimulator` , along with the active `Task` . It initializes Isaac Sim lazily — the `SimulationApp` is created only when `"isaac"` appears in `sim` ~~`m`~~ `ode` — so MuJoCo-only workflows incur no rendering overhead. All concrete task environments ( _e.g._ , `LocoManipulationEnv` , `TabletopGraspEnv` ) inherit from `BaseDualSim` and add task-specific `reset()` and `step()` logic on top. 

**Simulator.** `Simulator` ( `core/simulator.py` ) is an abstract base class defining five operations: `update` ~~`l`~~ `ayout()` , `set` ~~`s`~~ `tates()` , `get` ~~`s`~~ `tates()` , `step()` , and `render()` . `MujocoSimulator` ( `engines/mujoco.py` ) implements the physics backend: it runs the rigid-body contact simulation at 500 Hz and manages robot actuation, collision geometries, and proprioceptive state readout. `IsaacSimSimulator` ( `engines/isaacsim.py` ) implements the rendering backend: it consumes synchronized joint and pose states from MuJoCo and produces photorealistic ray-traced RGB frames via NVIDIA Isaac Sim’s USD/Replicator pipeline. 

**Task.** `Task` ( `core/task.py` ) is an abstract class that bundles all task-specific configuration: the `DRManager` instance, the `Robot` descriptor, sensor configs, and Gym action/observation spaces. Its 

13 


Figure 9: **Sequential Diagram of a Single** `env.step()` **Call.** Each invocation of `env.step(action)` (line 8 of Algorithm 1) triggers the following sequence: `MujocoSimulator` advances the physics loop at 500 Hz and writes the updated robot and object states to a shared buffer; `IsaacSimSimulator` reads those states, renders photorealistic RGB frames at 50 Hz, and returns the visual observation; `BaseDualSim` then queries the `Task` for the reward and termination condition before surfacing the full step output to the agent. 

`reset()` method sequences through all registered randomizers — scene, target, container, distractor, spatial, lighting, camera, and material — building a `Layout` object that both simulators ingest to rebuild the scene. Concrete subclasses ( _e.g._ , `G1WholebodyXMovePickTaskTeleop` ) additionally implement `check` ~~`s`~~ `uccess()` , a natural-language `instruction` property, and `decompose()` for automated subtask generation. 

**Robot.** `Robot` ( `core/robot.py` ) is a configuration container that holds the MJCF physics model path, USD rendering model path, CuRobo kinematics config, sensor configurations, and controller config. Concrete implementations ( _e.g._ , `G1Wholebody` , `G1Sonic` ) extend `Robot` with mixin traits such as `HeadCamMountable` , `HasDexterousHand` , and `CuRoboMixin` , and declare robot-specific constants like joint names and default poses. The `Robot` class does not execute control directly; it passes its asset paths to the `Simulator` backends and its kinematics config to the whole-body controller modules. 

**DomainRandomizer.** `DRManager` ( `dr/manager.py` ) maintains a named registry of `Randomizer` instances and dispatches randomization calls at each `Task.reset()` . Its `set` ~~`l`~~ `evel()` method adjusts active configurations to one of three difficulty levels: Level 0 adds distractor objects and background variation, Level 1 additionally randomizes material shaders and lighting, and Level 2 further varies object and robot spatial poses. Four leaf randomizers each implement a ~~`c`~~ `all` ~~`(`~~ `)` interface: `MaterialDR` samples NVIDIA vMaterials surface shaders, `SpatialDR` varies object and robot initial poses, `LightingDR` randomizes light positions and intensities, and `DistractorDR` populates the scene with randomly chosen distractor objects. 

**Agent.** `BaseAgent` ( `agents/base` ~~`a`~~ `gent.py` ) is the abstract policy interface; all subclasses implement `get` ~~`a`~~ `ction(observation, instruction)` and manage an internal ~~`a`~~ `ction` ~~`q`~~ `ueue` that buffers predicted action chunks for step-by-step execution. `MotionPlanAgent` ( `agents/mp` ~~`a`~~ `gent.py` ) wraps a CuRobo planner: it converts the planned kinematic trajectory into a sequence of `ActionCmd` objects and replays them deterministically, enabling fully automated data collection without a human operator. `PicoDecoupledAgent` ( `agents/pico` ~~`d`~~ `ecoupled` ~~`a`~~ `gent.py` ) is the teleoperation agent: it streams egocentric stereo video to a PICO XR headset via `TCPVideoSender` , receives hand-pose commands retargeted through inverse kinematics, and routes the resulting upper-body targets through the decoupled WBC pipeline. 

14 

**RemoteAgent.** VLA and WAM policies run as independent server processes ( `Psi0Server` , `Pi05Server` , `GR00TServer` ), each exposing a `health()` readiness check and an `act()` inference endpoint over HTTP or WebSocket. The corresponding client-side agents ( `Psi0Agent` , `Pi05Agent` , `Gr00tN16Agent` ) package RGB observations and proprioceptive state into the server’s expected format, issue a blocking network call, and enqueue the returned action chunk into the shared ~~`a`~~ `ction` ~~`q`~~ `ueue` . This server–client split allows policies to run on separate GPUs or machines, decoupling inference throughput from the simulation host’s memory budget. 

**Whole-Body Controllers.** SIMPLE supports three whole-body controller (WBC) implementations, each following a common `setup` ~~`c`~~ `ontroller()` / `apply` ~~`a`~~ `ction()` interface. `AmoWBC` wraps the AMO controller [20], which decouples upper- and lower-body control and uses a learned velocity-tracking policy for the base while accepting end-effector targets for the arms. `SonicWBC` ( `agents/sonic` ~~`w`~~ `bc` ~~`a`~~ `gent.py` ) and `SonicDecoupledWBC` ( `agents/sonic` ~~`d`~~ `ecoupled` ~~`w`~~ `bc` ~~`a`~~ `gent.py` ) both build on the SONIC framework [21]: the former forwards raw whole-body motion-tracking commands via the Unitree SDK, while the latter instantiates the full `decoupled` ~~`w`~~ `bc` pipeline — including a G1 kinematic model and a WBC policy — to convert high-level joint targets into low-level position commands at 50 Hz. 

### **A.1.2 Sequential Diagram** 

Figure 9 expands `env.step(action)` (line 8 of Algorithm 1) into its internal message-passing sequence. Within each step, `MujocoSimulator` integrates physics at 500 Hz and writes updated states to a shared buffer; `IsaacSimSimulator` reads those states and renders RGB frames at 50 Hz; and `BaseDualSim` queries the `Task` for the reward and termination signal before returning the step output. This producer–consumer ordering ensures every inference step receives a physically consistent, photorealistic observation while allowing MuJoCo to sub-step ahead of the slower rendering pass. 

### **A.2 Offline Object Preprocessing Pipeline** 

Figure 10 shows the offline preprocessing pipeline that runs once per asset and produces all artifacts needed for physics, rendering, and grasp planning. 

Assets are drawn from Objaverse [15] (1,500+ objects) and GraspNet-1B [26] (75 objects). After normalization, each mesh is processed in two parallel tracks: the _physics track_ applies CoACD [39] convex decomposition to generate MuJoCo collision geometries and drops each object in simulation to enumerate stable resting poses; the _rendering track_ converts meshes to USD format with highresolution PBR textures for Isaac Sim. 

BoDex [19] synthesizes dexterous grasp configurations for each stable pose offline, caching quality scores and approach depths per asset. At task initialization, SIMPLE samples a stable pose via `SpatialDR` , retrieves the cached grasps, and passes the selected target to CuRobo [18] for trajectory generation — no online grasp synthesis is required at training or evaluation time. 

### **A.3 Baseline Implementation Details** 

Ψ0 [4] is a 2.5B humanoid foundation model with a Qwen3-VL-2B vision backbone and a flowmatching diffusion transformer action expert. We fine-tune the released pre-trained checkpoint for 40,000 steps on 8 NVIDIA A100 GPUs using DDP, with a per-device batch size of 16, a cosineannealed learning rate of 1 _×_ 10<sup>_−_4</sup> , 1,000 warmup steps, and bf16 mixed precision. The action head is configured with a 36-dimensional output and a chunk size of 30, matching the SIMPLE whole-body action space. 

**DreamZero** [2] extends the Wan2.1-I2V video generation model (14B parameters) to jointly predict future video frames and robot actions via a flow-matching DiT action head, enabling planning in image space during execution. We initialize from the _DreamZero-AgiBot_ pretrained checkpoint and apply LoRA fine-tuning (rank 4, _α_ 4, targeting `q,k,v,o,ffn.0,ffn.2` layers) for 40,000 steps on eight NVIDIA A100 GPUs using DeepSpeed ZeRO-2, with a per-device batch size of 1, a 

15 

### **Offline object preprocessing** 


Figure 10: **Offline Object Preprocessing Pipeline.** Raw mesh assets from Objaverse and GraspNet-1B are processed for two purposes: (1) _For Physics_ — CoACD convex decomposition generates MuJoCo collision geometries, and stable resting poses are determined by dropping each object in simulation; (2) _For Rendering_ — meshes are converted to USD format with high-resolution PBR textures for Isaac Sim. BoDex [19] synthesizes dexterous grasp poses on the stable-pose meshes; the results are cached alongside each asset for use at task initialization. 

cosine-annealed learning rate of 1 _×_ 10<sup>_−_4</sup> , and a 5% linear warmup. The action head outputs a 36dimensional action at a step horizon of 48; video observations are rendered at 320 _×_ 176 resolution and encoded by the Wan2.1 VAE, with the number of context frames set per task (17, 25, or 33 frames corresponding to chunk sizes of 2, 3, or 4, respectively). 

**Cosmos3** [42] is a 16B Mixture-of-Transformers world foundation model that couples a Qwen3VL-8B understanding branch with a generation expert and jointly denoises video latents and action tokens with a shared rectified-flow objective. We initialize from the public Cosmos3-Nano checkpoint, register the G1 embodiment as a new domain with a 36-dimensional action space, and fully fine-tune the generation expert, timestep embedder, VAE projections, and newly initialized action projections while keeping the understanding branch frozen. Training runs for 40,000 iterations on 32 NVIDIA H100 GPUs with a base learning rate of 2 _×_ 10<sup>_−_4</sup> under a linear-decay schedule, a 5 _×_ multiplier on the action projections, and 10 _×_ weights on the video and action flow-matching losses. Each sample is a 33-frame egocentric clip at 50 fps encoded by the Wan2.2 VAE and paired with a 32-step chunk of normalized actions conditioned on the proprioceptive state. 

_π_ 0 _._ 5 [3] shows strong generalization on mobile dual-arm platforms, but its released checkpoint supports only a 30-dimensional action space. We expand the action dimension to 36 with a chunk size of 16, padding the weights of the affected linear layers to accommodate the larger space. To bridge the embodiment gap between the original training distribution and humanoid morphologies, we raise the learning rate from 1 _×_ 10<sup>_−_5</sup> to 1 _×_ 10<sup>_−_4</sup> and the global batch size from 32 to 128, fine-tuning from the _Pi05_ _~~D~~ ROID_ checkpoint ported to PyTorch. 

**GR00T N1.6** [1] is a 3B VLA pretrained for general robot manipulation. We fine-tune from the released checkpoint for 20,000 steps on three NVIDIA A100 GPUs (global batch size 24, lr 1 _×_ 10<sup>_−_4</sup> cosine), using all default hyperparameters. As the RTC inference code is unavailable, we use a standard sequential scheme conditioning each prediction on the most recently executed observation. 

**Diffusion Policy (DP)** [43] uses a pre-trained ResNet-18 as the visual encoder, with a learning rate of 1 _×_ 10<sup>_−_4</sup> and a global batch size of 32. Training runs for 40,000 steps on two NVIDIA A100 GPUs, taking approximately 15 hours per task. Despite fitting the training data reasonably, DP fails on most evaluation tasks; we attribute this to the insufficient visual capacity of the UNetbased architecture for the diverse visual conditions in SIMPLE. At inference time, we perform 100 denoising steps to recover actionable trajectories from noise. 

**Action Chunking with Transformers (ACT)** [44] is reconfigured with a 36-dimensional action head and a chunk size of 100, using a transformer comprising 4 encoder layers and 1 decoder layer following the publicly released LeRobot configuration [40]. All other hyperparameters are kept identical to those used for DP. 

16 

Table 7: Representative tasks in our benchmark. 

|`Task Name`|**Category**|**Teleop**|**Success Criteria**|
|---|---|---|---|
|`BendPick`|Rigid|Yes|Lift the target object more than 5 cm<br>from the table.|
|`BendPickAndPlace`|Rigid|Yes|Place the target object into the con-<br>tainer.|
|`BendHandover`|Bimanual|Yes|Handover the object and place it into<br>the container.|
|`Handover`|Bimanual|Yes|Handover the object and place it into<br>the container.|
|`OpenTrashCan`|Articulated|Yes|Open the trash can lid beyond the tar-<br>get angle threshold.|
|`PushOfficeChair`|Non-prehensile|Yes|Push the office chair beyond the target<br>distance.|
|`OpenFaucet`|Articulated|Yes|Rotate the faucet handle beyond the<br>target angle.|
|`OpenOven`|Articulated|Yes|Open the oven door beyond the target<br>angle threshold.|
|`CloseDoor`|Articulated|Yes|Close the door to the target closed<br>state.|
|`XMovePick`|Mobile|Yes|Move laterally and lift the target ob-<br>ject.|
|`XMoveBendPick`|Mobile|Yes|Move laterally, bend down, and lift the<br>target object.|
|`LocomotionPickBetweenTables`|Whole-body|Yes|Transfer the object from one table to<br>another table container.|
|`PickAndPlaceAndHugContainer`|Whole-body|Yes|Place two objects into the container,<br>lift it, and move it onto another table.|
|`BendPickMP`|Rigid|No|Lift the target object more than 5 cm<br>from the table.|
|`TableTopGraspMp`|Rigid|No|Lift the target object more than 5 cm<br>from the table.|
|`LocoPickBetweenTablesMP`|Whole-body|No|Transfer the object from one table to<br>another table.|


### **A.4 Whole-Body Controller Details** 

SIMPLE integrates two whole-body locomotion controllers that share a common teleoperation interface but differ in their internal control architecture. Both controllers receive the same high-level inputs — upper-body joint targets from the teleoperation or policy layer and a 4-dimensional navigation command ( _vx, vy, v_ yaw _, q_ yaw) — and output low-level joint position commands to the Unitree G1 at 500 Hz via MuJoCo. 

**AMO** [20] adopts a decoupled architecture that treats upper-body and lower-body control as two independent problems. The lower body is governed by a learned RL locomotion policy ( `AMO` ~~`P`~~ `olicy` in `robots/policy/AMO` ~~`P`~~ `olicy.py` ) that takes IMU measurements and proprioceptive joint states as input and outputs 15 lower-body joint targets (hip, knee, ankle, and waist joints) at high frequency. The upper body is controlled separately by directly tracking the joint targets received from the highlevel policy or teleoperator, so arm and hand movements do not feed back into the locomotion policy, giving the operator more predictable upper-body control at the cost of tighter coupling between arm posture and balance. 

**SONIC** [21] takes an end-to-end whole-body motion tracking approach. SIMPLE provides two SONIC-based implementations: `SonicWbcAgent` ( `agents/sonic` ~~`w`~~ `bc` ~~`a`~~ `gent.py` ), which forwards whole-body commands directly through the Unitree SDK bridge ( `gear` ~~`s`~~ `onic` ), and `SonicDecoupledWbcAgent` ( `agents/sonic` ~~`d`~~ `ecoupled` ~~`w`~~ `bc` ~~`a`~~ `gent.py` ), which runs the full `decoupled` ~~`w`~~ `bc` pipeline internally — instantiating a G1 kinematic model and a WBC policy — to convert upper-body joint targets and navigation commands into full-body position commands at 

17 

50 Hz. Because SONIC tracks the operator’s whole-body motion as a unified trajectory rather than handling each segment independently, it tends to produce smoother and more natural whole-body demonstrations, particularly for tasks requiring coordinated arm–leg movements such as mobile pick-and-place. 

### **A.5 Extended Benchmark Results** 

Beyond the single-task fine-tuning results in Table 1 of the main paper, we benchmark the foundation models by jointly fine-tuning each on all 16 tasks and report per-task success rates under the three domain-randomization levels (Level 0 / Level 1 / Level 2) in Table 8. ACT and DP are excluded from this setting since they are designed for single-task training. Each task is evaluated with 20 trials per level to tighten the confidence intervals. 

|**Task**|Ψ0 **[4]**|_π_0_._5 **[3]**|**GR00T N1.6 [1]**|**Cosmos3-Nano [42]**|**DreamZero [2]**|
|---|---|---|---|---|---|
|`BendHandoverTeleop`|75/50/60|65/40/30|80/80/0|80/75/65|**70/80/90**|
|`BendPickAndPlaceTeleop`|10/20/0|15/10/5|20/10/0|**15/25/20**|**30/20/10**|
|`BendPickMP`|**100/100/100**|5/0/0|45/30/40|0/0/0|90/90/80|
|`BendPickTeleop`|100/50/50|75/75/70|**100/100/80**|70/65/35|80/80/60|
|`CloseDoorTeleop`|95/95/75|90/75/95|100/95/100|100/100/95|**100/100/100**|
|`HandoverTeleop`|**70/70/100**|55/35/45|65/65/0|65/100/70|70/50/30|
|`LocomotionPickBetweenTablesTeleop`|**70/50/60**|35/15/20|55/50/10|70/50/20|50/30/30|
|`OpenFaucetTeleop`|**10/10/35**|5/0/0|0/0/0|15/5/10|10/0/0|
|`OpenOvenTeleop`|65/25/10|55/25/50|85/60/90|65/60/75|**90/80/70**|
|`OpenTrashCanTeleop`|45/55/25|5/5/5|**65/50/75**|20/10/15|20/10/10|
|`PickAndBendPlaceMP`|20/55/40|60/45/20|**90/75/85**|85/75/75|80/70/50|
|`PickAndPlaceAndHugContainerTeleop`|25/25/10|35/15/35|**80/80/20**|40/50/30|50/50/10|
|`PushOfficeChairTeleop`|100/100/65|95/90/60|**100/100/100**|100/90/60|100/70/40|
|`TabletopGraspMP`|**100/100/80**|40/10/25|75/90/60|30/30/25|90/100/70|
|`TabletopHandoverMP`|45/50/10|0/5/5|0/5/15|**95/55/60**|0/0/0|
|`XMovePickTeleop`|100/100/60|15/15/25|0/0/0|95/95/75|**100/100/100**|
|**Average**|**64.4/59.7/48.8**|40.6/28.8/30.6|60.0/55.6/42.2|59.1/55.3/45.6|64.4/58.1/46.9|


Table 8: **Multi-Task Benchmarking Results.** Success rates (%) under three domain-randomization levels ( _Level 0 / Level 1 / Level 2_ ) of foundation models jointly fine-tuned on all 16 tasks. Each entry averages 20 trials per task and level (10 for DreamZero due to time constraints). 

Averaged over tasks, Ψ0 [4] leads the benchmark, followed closely by DreamZero, GR00T N1.6, and Cosmos3-Nano [42], whereas _π_ 0 _._ 5 lags behind; success rates generally decrease with the domain-randomization level for all models. Tasks with unambiguous geometric success signals ( `CloseDoor` , `PushOfficeChair` ) are solved by nearly all models, whereas fine-grained contact tasks ( `OpenFaucet` ) stay at or below 35% for every model, confirming a meaningful difficulty gradient. Every task is solved at a non-trivial rate by at least one model, establishing these results as reference baselines for future comparisons. 

18 

