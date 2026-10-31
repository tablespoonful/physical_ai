---
title: "Hiking in the Wild: A Scalable Perceptive Parkour Framework for Humanoids"
date: "2026-01-12"
authors: "Shaoting Zhu; Ziwen Zhuang; Mengjie Zhao; Kun-Ying Lee; Hang Zhao"
url: https://arxiv.org/abs/2601.07718
pdf: https://arxiv.org/pdf/2601.07718
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.07718)** / [論文ページ](https://arxiv.org/abs/2601.07718)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Hiking in the Wild: A Scalable Perceptive Legged Parkour Framework for Humanoid Robots** 

**Shaoting Zhu**<sup>1</sup><sup>_,_2</sup><sup>_,∗_</sup> **Ziwen Zhuang**<sup>1</sup><sup>_,_2</sup><sup>_,∗_</sup> **Mengjie Zhao**<sup>1</sup> **Kun-Ying Lee**<sup>3</sup> **Hang Zhao**<sup>1</sup><sup>_,_2</sup><sup>_,†_</sup> 1IIIS, Tsinghua University 2Shanghai Qi Zhi Institute 

3Department of Computer Science and Technology, Tsinghua University _∗_ Equal contribution _†_ Corresponding author 


Figure 1: **Hiking in the Wild.** Our framework enables a humanoid robot to traverse diverse terrains in the wild. The robot can run at a maximum speed of 2.5 m/s over complex terrain. It can also negotiate stairs, gaps, high platforms, and ramps. Relying on depth images for perception, our extensible end-to-end framework achieves robust performance across these scenarios. 

**Abstract:** Achieving robust humanoid locomotion in complex, unstructured environments requires transitioning from reactive proprioception to proactive perception. However, integrating exteroception remains a significant challenge: existing approaches often fail to achieve high-speed, stable locomotion across diverse, unstructured terrains. In this work, we present _Hiking in the Wild_ , an extensible, end-to-end perceptive legged parkour framework designed for robust humanoid hiking. Our approach maps depth inputs and proprioception directly to joint actions, without relying on external localization and mapping. To ensure safety and training stability, we introduce two key mechanisms: a foothold safety mechanism combining extensible _Terrain Edge Detection_ with _Foot Volume Points_ to reduce catastrophic slippage on edges, and a _Flat Patch Sampling_ strategy that mitigates reward hacking by generating feasible navigation targets. Extensive experiments on the Unitree G1 humanoid robot demon- 

10th Conference on Robot Learning (CoRL 2026), Austin, Texas, USA. 

strate that our policy enables robust traversal of complex terrains at speeds up to 2.5 m/s. Code and video demonstrations are available on the project page: `https://project-instinct.github.io/hiking-in-the-wild` . 

**Keywords:** Humanoid Locomotion, Perceptive Legged Parkour, Reinforcement Learning 

## **1 Introduction** 

Humanoid robots hold immense promise for traversing complex real-world environments and executing difficult tasks. Unlike their wheeled counterparts, humanoids can step over obstacles and cross discontinuous terrain. Recently, significant strides have been made in humanoid control, enabling robots to perform dynamic maneuvers such as dancing, backflips, and mimicking human motions [1, 2]. However, there is a fundamental distinction between tracking a predefined motion and hiking in the wild. While tracking resembles memorizing a routine, hiking requires the robot to actively perceive the terrain, adapt to irregularities, and handle the unknown. In this paper, we study _legged parkour_ : agile traversal over obstacles using only legged contacts, without relying on arms, torso contacts, or full-body maneuvers such as vaulting and climbing. 

Blind locomotion has established a robust baseline [3, 4, 5, 6], but its purely reactive nature is fundamentally limited: without perceiving ahead, the robot cannot safely handle deep gaps or high steps. Integrating exteroceptive perception remains challenging: LiDAR-based methods [7, 8, 9] depend on precise state estimation and suffer from motion distortion at high speed, while depth-based methods that reconstruct heightmaps [10, 11, 12] are limited to low-speed, structured environments and struggle to scale to unseen wild terrains. 

To address these challenges, we present _Hiking in the Wild_ , an extensible, end-to-end perceptive legged parkour framework designed for robust humanoid locomotion in unstructured environments. Unlike complex modular pipelines, our approach directly maps depth input and proprioception to joint actions. To handle the high dimensionality of visual data and the complexity of diverse terrain skills, we incorporate a Mixture-of-Experts (MoE) architecture [13, 14]. Our design allows the policy to capture depth inputs at high frequencies (up to 60 Hz). This high-bandwidth perception loop enables the robot to perform dynamic legged obstacle traversal and high-speed running (up to 2.5 m/s). Crucially, our system incorporates a realistic depth synthesis module that models sensor noise and artifacts during training, enabling zero-shot sim-to-real transfer without external mapping and localization of the environment. 

A critical yet overlooked issue in humanoid RL is foothold precision: stepping partially on an edge can cause catastrophic slippage. Prior approaches [15, 16] require manually designed constraints for specific terrain types, limiting extensibility. We instead propose a geometric **Terrain Edge Detector** coupled with foot-attached **Volume Points** that automatically detects edges on arbitrary meshes and penalizes foot penetration, implicitly teaching the policy to seek safe, flat surfaces. Training stability is further challenged by “reward hacking”, where random velocity commands lead the robot to spin rather than traverse obstacles [16]. We address this with a **Flat Patch Sampling** strategy that identifies reachable flat regions and derives speed-controlled commands toward them, ensuring the robot is always challenged with physically solvable tasks. 

We validate our framework on the Unitree G1 humanoid robot, demonstrating robust traversal of stairs, ramps, gaps, and platforms at speeds up to 2.5 m/s. The contributions of this work are: 

1. An extensible, end-to-end perceptive **framework** for training and deployment based on depth input, enabling zero-shot sim-to-real transfer without external localization and mapping. 

2. A novel **safety mechanism** using Terrain Edge Detection and Foot Volume Points, alleviating the precise foothold problem in learning-based control. 

2 

3. A **geometry-aware command generation** method that derives velocity commands by pointing toward reachable flat terrain patches, eliminating reward hacking and ensuring the robot actively traverses complex environments. 

4. Demonstration of robust wild hiking and legged parkour capabilities on a humanoid robot. The training and deployment code is **open-source and available to the community** , enabling deployment on real robots with minimal hardware modifications. 

## **2 Related Work** 

### **2.1 Learning-based Legged Locomotion** 

Legged locomotion control has shifted from model-based approaches, such as Model Predictive Control (MPC) [17, 18, 19], to data-driven reinforcement learning (RL) to better handle unmodeled dynamics. Early blind RL policies achieved impressive robustness on irregular terrains using only proprioception [4, 6, 3, 20]. However, these methods lack the exteroception required to navigate large obstacles quickly and safely. 

To enable greater agility, recent works have integrated exteroceptive perception into the control loop [16, 21, 22, 23]. One category of methods relies on LiDAR to build elevation maps (2.5D) [8, 7, 24, 25] or voxel grids [9]. Nevertheless, these approaches depend heavily on precise localization, which limits their update frequency and overall robustness. Furthermore, LiDAR often suffers from motion distortion during fast movement, restricting these methods to low-speed scenarios. Alternatively, depth-based methods have been proposed. Some of these operate at low frequency [15], while others employ intermediate modules to predict heightmaps [10, 11, 12] or learn end-to-end depth policies [26, 27], potentially compromising performance in high-speed or unseen wild environments. In contrast, our method directly utilizes high-frequency depth images as input to train an end-to-end policy, achieving highly dynamic behaviors across complex, unstructured terrains in the wild. 

### **2.2 Perceptive Foothold Control** 

Explicit foothold control typically decouples perception and planning, utilizing terrain representations like elevation maps to solve for optimal placements. Approaches range from heuristic search [28, 29, 30, 31, 32, 33, 34] and learned feasibility costs [35, 36, 37, 38] to rigorous nonlinear optimization [39, 40]. While hybrid frameworks that utilize probabilistic map uncertainty [30, 41] or combine pre-planned references with online tracking [42, 43, 44] have achieved impressive agility, they remain brittle to state-estimation drift and reconstruction artifacts. Recently, end-to-end policies [16] use edge penalization to learn safe footholds implicitly. However, it is not extensible to arbitrary meshes. Our method takes a triangular mesh as input and automatically detects the edges, retaining the robustness of the implicit paradigm while improving safety. 

## **3 Method** 

### **3.1 Problem Formulation** 

We formulate perceptive humanoid locomotion as a POMDP and train the policy with PPO [45]. The actor receives a history of _h_ proprioceptive states (angular velocity, projected gravity, velocity commands, joint positions/velocities, last action) concatenated with a strided depth history _Ht_ , with stochastic noise applied during training. During hardware deployment, velocity commands are provided by a human operator through a remote controller. An asymmetric critic additionally observes noise-free states and base linear velocity. The policy outputs target joint positions executed via PD control ( **_τ_** _t_ = _kp_ ( **a** _t −_ **q** _t_ ) _− kd_ ˙ **q** _t_ ) with gains from [1]. Episodes terminate on time-out, boundary violation, torso contact, or large base tilt (details in subsection A.2). The reward comprises task tracking, regularization, safety, and AMP-style terms; full specifications are in Table 5. 

3 


Figure 2: System overview. Our framework trains an end-to-end policy using simulated depth and proprioception. To ensure safety and agility on complex terrains, we incorporate Extensible Edge Penalization to avoid risky footholds and Position-Based Command Generation for precise tracking. The trained policy is directly deployed to the real robot (Zero-shot) using only a 60 Hz onboard depth camera as exteroception, achieving highly dynamic locomotion without explicit localization or map reconstruction. 


Figure 3: Depth processing: Top row shows _Fsim_ on synthetic data, and bottom row shows _Freal_ on real-world data. 

### **3.2 Ego-centric Depth Perception** 

We implement a GPU-accelerated ray-caster using NVIDIA Warp [46] to synthesize dense depth maps in real time. To bridge the sim-to-real gap, we define two alignment pipelines: _Fsim_ degrades simulated depth via sequential stochastic operations (range-dependent Gaussian noise, disparity artifact synthesis, blur, and OOD perturbation), while _Freal_ applies inpainting and blur to the physical sensor stream, harmonizing both distributions into a shared perception space (see Figure 3 and subsection A.4). The policy receives a depth history of _m_ frames with temporal stride _ℓ_ . During deployment, depth acquisition and preprocessing run asynchronously at 60 Hz, while the policy runs at 50 Hz using the latest available depth observations. History length and stride determine the lookback window without reducing the depth update rate. During training, a one-frame delay emulates sensor latency. 

### **3.3 Terrain Edge Contact Penalization** 

Driven by energy efficiency, RL agents naturally tend to minimize effort by taking shorter steps and often placing their feet on the nearest terrain edges [16]. While this strategy can yield high success rates in simulation due to simplified contact physics, it significantly increases the sim-to-real gap. In the real world, contact dynamics at structural edges are far more unpredictable than in simulation, and stepping partially on them frequently leads to catastrophic slippage and deployment failures. To mitigate this, we propose a soft-constraint mechanism that penalizes foot contacts near sharp geometric boundaries. First, we use a detector to find the sharp edges of the terrain mesh. Second, we attach a set of “volume points” to the robot’s feet. By penalizing these points when they penetrate edge regions, the policy learns to select more stable, centered foot positions rather than risky ones. 

4 


Figure 4: Terrain edge contact penalization. Left: automatically detected edges across diverse terrains. Right: volume points distributed within the foot manifold for penetration penalization. 

### **3.3.1 Terrain Edge Detector** 

First, we identify sharp terrain edges by comparing the dihedral angle between adjacent faces to a predefined threshold _τ_ . To enhance computational efficiency, the resulting raw edges are further processed to filter noise and concatenate short segments. The edge processing step employs a greedy concatenation strategy to merge fragmented segments and reduce the total number of primitives. More details can be found in subsection A.10. 

### **3.3.2 Volumetric Point Penetration Penalization** 

To accurately monitor the contact state relative to terrain edges, we distribute a set of volume points _P_ within each foot’s collision geometry, as illustrated in Figure 4. We leverage NVIDIA Warp [46] to perform massively parallel distance queries, computing the penetration depth of each point relative to the previously constructed spatial collision grid _S_ . 

To discourage unstable foot-ground interactions near terrain edges, we define a penalty term that considers both the geometric penetration and the foot velocity, following [47]. For each point _i ∈P_ , let **d** _i_ be its penetration offset and **v** _i_ be its linear velocity in the world frame. The penalty term _rvol_ is formulated as: 


where _ϵ_ = 10<sup>_−_3</sup> is a small constant for numerical stability. This formulation ensures that the policy is penalized more heavily for high-velocity impacts or scraping motions near terrain edges, thereby encouraging the robot to seek stable footholds. 

### **3.4 Position-based Velocity Command Generation** 

During training, uniformly sampled velocity commands may cause “reward hacking” where the robot spins in place rather than traversing obstacles [16]. Prior fixes via reward shaping [48] or goal-based commands [49, 50] either lack speed control or produce infeasible targets. We instead generate targets from reachable flat terrain patches and derive speed-controlled commands toward them. 

We identify reachable flat regions on the terrain mesh via ray-casting: a candidate location is accepted as a navigation target only if the height variation within radius _r_ stays below threshold _δ_ , ensuring targets lie on stable ground rather than slopes or unreachable areas (see algorithm 1 and Figure 9). After generating the flat patches, we periodically select one as the navigation goal. The robot’s velocity commands are then generated based on the relative position of this goal. Let **p**<sup>_B_</sup> _goal_<sup>=[</sup><sup>_xg, yg_]</sup><sup>_T_represent the goal position in the robot’s base frame.The desired linear velocity</sup> _vx_ and angular velocity _ωz_ are calculated as follows: 


where _kv_ and _kω_ are the linear and angular stiffness coefficients. Because we use the forward camera on the robot’s head link, we only focus on forward locomotion and heading alignment; therefore, the lateral velocity command _vy_ is set to zero. The velocity limits ( _vmax, ωmax_ ) are adaptively adjusted based on the terrain category. 

5 


Figure 5: Snapshots of the humanoid robot traversing diverse indoor and outdoor environments via zero-shot transfer: (a) running ascent onto a high platform; (b) running descent from a high platform; (c) running on a grassy slope; (d) stair ascent; (e) stair descent; (f) traversing a discrete gap. 

However, relying solely on these position-based commands can limit the robot’s ability to learn inplace turning, as the goal is usually far away. To address this, we assign pure turning commands to a small subset of agents on flat terrain. For these agents, we set _vx_ = 0 and provide a random _ωz_ , forcing the policy to learn effective in-place rotation maneuvers. This combination improves the overall maneuverability of the robot across different environments. 

### **3.5 Policy Training with Adversarial Motion Priors** 

We adopt the AMP framework [51] to shape natural locomotion style. Walking and running policies use distinct reference datasets drawn from MPC-generated motion, retargeted human mocap, and running clips from LAFAN [52]. We train the gaits separately because joint training produces fast walking with long strides rather than natural running. The discriminator operates on short state sequences rather than single transitions to better capture motion dynamics. Full dataset composition, discriminator formulation, and style-reward details are provided in subsection A.9. 

## **4 Experiments** 

For the simulation results in Figure 1 and Table 2, each method uses a single generalist walking policy across all evaluated terrains. Our HPL reimplementation is evaluated in the walking regime, and our running policy is excluded from this comparison because it does not cover all evaluated terrain types, including stairs. Hardware experiments use the deployment policies described in subsection 4.1 and subsection A.8. Our evaluation addresses three questions: 

- **Q1** : Does our framework enable efficient training and reliable zero-shot deployment on physical hardware? 

- **Q2** : Does the edge-aware penalization mechanism improve foothold safety and stability when traversing discrete terrain features? Is it extensible to new terrains without any extra design? 

- **Q3** : What are the individual contributions of the key design components (e.g., perception, AMP, and command generation) to the robot’s performance? 

### **4.1 Real-world Deployment** 

We deploy the trained policies onto the humanoid robot via zero-shot sim-to-real transfer. For hardware deployment, we use specialized policies for stair walking, platform walking, and running, while retaining the general walking policy for the remaining walking tasks (subsection A.8). To switch policies, the robot first stops, transitions to a standing policy, and then switches to the selected 

6 


Figure 6: Real-world success rates across terrains and gaits. 


||**Sim**|**SR**_↑_|**Landi**|**ng Area**_↑_|**Rea**|**l SR**_↑_|
|---|---|---|---|---|---|---|
|**Terrain Type**|**Ours**|**No Edge **|**Ours**|**No Edge**|**Ours **|**No Edge**|
|Stair Up|100.00%|100.00%|**0.77**|0.68|**10/10**|8/10|
|Stair Down|**99.95%**|99.82%|**0.67**|0.50|**10/10**|6/10|
|Deep Gap|**100.0%**|99.94%|**0.84**|0.21|**8/10**|3/10|
|Small Box|**99.09%**|93.17%|**0.81**|0.70|–|–|


Table 1: Edge penalization results in simulation and hardware. 


Figure 7: Left: the robot slips and falls after stepping on a stair edge. Right: edge detector visualizations on new and noisy terrains. 

locomotion policy. As illustrated in Figure 5, the robot successfully performs various locomotion primitives across challenging terrains. Notably, the robot achieves a maximum running speed of 2 _._ 5 m/s and successfully traverses difficult obstacles, including high platforms up to 32 cm and discrete gaps with a width of 50 cm. During these deployments, the policy uses depth observations acquired at 60 Hz to react to terrain changes. 

To quantify the system’s reliability, we conduct 10 trials for each evaluated terrain–gait combination. A trial is successful if the robot reaches the endpoint and stops stably; falling before completion is counted as a failure. Figure 6 reports the success rates for these combinations; absent bars indicate combinations that were not evaluated. 

Furthermore, we conduct a long-duration test to evaluate the stability of the system over a prolonged period. The robot is tasked with continuous locomotion across multiple staircases and flat surfaces. It successfully maintains its balance and walks for 4 minutes without falls or physical assistance. This sustained performance highlights the effectiveness of our control framework and its potential for deployment in complex, long-range real-world tasks. 

### **4.2 Edge-aware Penalization Mechanism** 

As introduced in subsection 3.3, we utilize the _Terrain Edge Detector_ and _Volumetric Point Penetration Penalization_ to improve foothold safety. As illustrated in Figure 8, with edge-aware penalization enabled, the robot tends to seek larger safety margins, effectively placing its feet away from terrain edges to maintain stable contact. 

To quantitatively evaluate this effect, we measure the **Success Rate** and **Mean Foot Landing Area Fraction** in simulation across various challenging terrains. The landing-area metric quantifies the fraction of the foot area supported by the terrain surface, reported on a scale from 0 to 1. To eliminate flat-ground dilution, it is computed exclusively when the robot’s base is within the interaction range of the obstacle. We test each policy for 10,000 timesteps with 1,000 robots. Figure 1 compares our full method ( _Ours_ ) against the variant without edge penalization ( _No Edge_ ). Our method matches or exceeds _No Edge_ in simulation success rate and achieves a higher landing-area fraction across all tested terrains. 


Figure 8: Visualization of foothold placement. 

7 

Table 2: <u>Quantitative results in simulation</u> 

||||||**Success Rate**|**(%)**_↑_|||||||**Mea**|**n Reaching**|**Time (s)**_↓_||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Method**|**Large Box**|**Ramp**<br>|**Small Box**|**Rough**|**Stair Down**|**Platform down**|<br>**Stair Up**|**Platform up**|**Gap**|**Large Box**|**Ramp**|**Small Box**|**Rough**|**Stair Down**|**Platform down**|<br>**Stair Up**|**Platform up**|<br>**Gap**|
|w/o depth history|100.0|100.0|1.66|100.0|99.88|100.0|100.0|100.0|100.0|6.20|6.72|11.68|5.78|5.33|5.81|6.54|5.89|5.79|
|w/o position-based|23.13|100.0|90.68|100.0|99.59|100.0|95.18|11.70|100.0|9.41|5.74|11.32|5.72|6.77|7.07|6.79|10.57|5.70|
|w/o AMP|13.75|99.94|0.00|100.0|98.39|99.47|0.00|0.00|99.94|9.81|**5.68**|–|6.50|6.89|7.40|–|–|6.07|
|10Hz height map|99.40|100.0|15.28|100.0|99.60|100.0|100.0|95.21|100.0|6.51|6.01|14.73|6.34|**4.40**|**5.63**|5.63|6.03|6.40|
|w/o depth|38.94|100.0|3.33|100.0|99.12|99.93|94.54|0.00|67.95|7.88|8.48|10.59|7.75|5.39|6.72|7.12|–|7.58|
|HPL [15]|43.65|99.71|51.01|100.0|99.90|100.0|92.07|97.84|99.95|8.30|6.16|9.65|8.22|6.10|6.13|6.34|5.99|7.44|
|Ours|**100.0**|**100.0**|**99.09**|**100.0**|**99.95**|**100.0**|**100.0**|**100.0**|**100.0**|**5.91**|5.84|**8.03**|**5.40**|5.15|**5.63**|**5.36**|**5.60**|**5.43**|


In the real world, stepping on edges sometimes causes slippage or unpredictable contact dynamics, driving the robot into out-of-distribution (OOD) states that lead to immediate falls, as shown in Figure 7. By incentivizing the policy to maximize the landing area and avoid edges, our method significantly reduces these real-world risks, ensuring greater robustness during physical deployment. As shown in Figure 5, our policy exhibits ample safety margins and maintains stable footholds throughout the traversal. 

To further demonstrate the extensibility of our framework, we evaluate the edge detector on new terrain types: _Stones_ , _Stakes_ , and _Noisy Scan_ terrain. As illustrated in Figure 7, the detector precisely identifies terrain edges without any manual feature engineering or parameter tuning. This robust zero-shot performance confirms that our edge-aware mechanism can scale to arbitrary terrain topologies. 

### **4.3 Comparison and Ablation** 

To evaluate both overall performance and the individual contributions of our proposed components, we compare our full framework against a reimplemented external baseline and several ablated variants: 

- **Single-frame Depth (w/o depth history)** : The policy receives only the current depth image instead of the strided temporal history. 

- **Uniform Command (w/o position-based)** : The policy is trained using standard uniform velocity sampling with heading commands. 

- **No Motion Prior (w/o AMP)** : The Adversarial Motion Prior is removed, training the policy solely through task-related rewards. 

- **Blind Policy (w/o depth)** : The policy relies exclusively on proprioceptive feedback. 

- **Height Map (10 Hz)** : We use a practical elevation-map update rate of 10 Hz [24], compared with 60 Hz raw depth acquisition in our system. 

- **HPL [15]** : We reimplement the _humanoid parkour learning_ baseline in our training environment for comparison, as the original code is not open-sourced and the original work targets the Unitree H1 robot trained in IsaacGym. 

We evaluate each policy with 1,000 robots in simulation and record their success rates and the mean reaching time. As shown in Table 2, our method achieves the highest success rates among both ablated variants and HPL, confirming the effectiveness of the complete framework on complex terrains. Our depth-based configuration outperforms the 10 Hz height-map baseline at their respective practical operating rates. AMP is an existing training component adopted in our framework. Removing it ( _w/o AMP_ ) reduces success rates to 0% on Small Box, Stair Up, and Platform Up, indicating its importance for terrains requiring large leg lifts in our setting. The _w/o position-based_ variant degrades severely on Large Box (23.1%) and Platform Up (11.7%), confirming that position-based command generation is essential for directing the robot toward challenging obstacles. The blind policy ( _w/o depth_ ) fails on small and elevated structures where foothold precision requires visual feedback. 

8 

## **5 Conclusion and Limitations** 

In this paper, we present an extensible end-to-end perceptive locomotion framework for humanoid robots. By integrating a novel volumetric edge-aware penalization mechanism with position-based velocity command generation, our approach achieves highly dynamic behaviors on complex terrains. Extensive experiments in simulation and real-world deployment demonstrate that our framework enables humanoid robots to perform agile running and stable walking across a variety of challenging environments. 

**Limitations.** A single forward-facing depth camera limits backward and lateral awareness. Hardware deployment uses specialized policies for stair walking, platform walking, and running; learning a unified policy remains challenging because joint training can cause mode collapse. Evaluation is limited to the Unitree G1 and static environments, with only 10 trials per evaluated terrain–gait combination. These results do not establish generalization across robot platforms or performance in dynamic environments. Failure-recovery capability is also limited. Future work includes broader perceptual coverage, unified policies, recovery behaviors, and more extensive hardware evaluation. 

9 

### **Acknowledgments** 

We thank Xiangting Meng, Baijun Ye, Siqiao Huang, and Yizhuo Gao for their assistance. This project is supported by Tsinghua University Initiative Scientific Research Program. 

## **References** 

- [1] Q. Liao, T. E. Truong, X. Huang, Y. Gao, G. Tevet, K. Sreenath, and C. K. Liu. Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion. _arXiv preprint arXiv:2508.08241_ , 2025. 

- [2] Z. Luo, Y. Yuan, T. Wang, C. Li, S. Chen, F. Casta˜neda, Z.-A. Cao, J. Li, D. Minor, Q. Ben, et al. Sonic: Supersizing motion tracking for natural humanoid whole-body control. _arXiv preprint arXiv:2511.07820_ , 2025. 

- [3] X. Gu, Y.-J. Wang, and J. Chen. Humanoid-gym: Reinforcement learning for humanoid robot with zero-shot sim2real transfer. _arXiv preprint arXiv:2404.05695_ , 2024. 

- [4] I. Radosavovic, T. Xiao, B. Zhang, T. Darrell, J. Malik, and K. Sreenath. Real-world humanoid locomotion with reinforcement learning. _Science Robotics_ , 9(89):eadi9579, 2024. 

- [5] I. Radosavovic, S. Kamat, T. Darrell, and J. Malik. Learning humanoid locomotion over challenging terrain. _arXiv preprint arXiv:2410.03654_ , 2024. 

- [6] J. Siekmann, K. Green, J. Warila, A. Fern, and J. Hurst. Blind bipedal stair traversal via simto-real reinforcement learning. In _Robotics: Science and Systems XVII_ , 2021. 

- [7] J. Long, J. Ren, M. Shi, Z. Wang, T. Huang, P. Luo, and J. Pang. Learning humanoid locomotion with perceptive internal model. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 9997–10003. IEEE, 2025. 

- [8] J. He, C. Zhang, F. Jenelten, R. Grandia, M. B¨acher, and M. Hutter. Attention-based map encoding for learning generalized legged locomotion. _Science Robotics_ , 10(105):eadv3604, 2025. 

- [9] Q. Ben, B. Xu, K. Li, F. Jia, W. Zhang, J. Wang, J. Wang, D. Lin, and J. Pang. Gallant: Voxel grid-based humanoid locomotion and local-navigation across 3d constrained terrains. _arXiv preprint arXiv:2511.14625_ , 2025. 

- [10] H. Duan, B. Pandit, M. S. Gadde, B. Van Marum, J. Dao, C. Kim, and A. Fern. Learning visionbased bipedal locomotion for challenging terrain. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 56–62. IEEE, 2024. 

- [11] J. Sun, G. Han, P. Sun, W. Zhao, J. Cao, J. Wang, Y. Guo, and Q. Zhang. Dpl: Depthonly perceptive humanoid locomotion via realistic depth synthesis and cross-attention terrain reconstruction. _arXiv preprint arXiv:2510.07152_ , 2025. 

- [12] H. Song, H. Zhu, T. Yu, Y. Liu, M. Yuan, W. Zhou, H. Chen, and H. Li. Gait-adaptive perceptive humanoid locomotion with real-time under-base terrain reconstruction. _IEEE Robotics and Automation Letters_ , 11(4):4969–4976, 2026. 

- [13] R. A. Jacobs, M. I. Jordan, S. J. Nowlan, and G. E. Hinton. Adaptive mixtures of local experts. _Neural computation_ , 3(1):79–87, 1991. 

- [14] R. Huang, S. Zhu, Y. Du, and H. Zhao. Moe-loco: Mixture of experts for multitask locomotion. In _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 14218–14225. IEEE, 2025. 

10 

- [15] Z. Zhuang, S. Yao, and H. Zhao. Humanoid parkour learning. In _Conference on Robot Learning (CoRL)_ , volume 270 of _Proceedings of Machine Learning Research_ , pages 1975–1991. PMLR, 2024. 

- [16] X. Cheng, K. Shi, A. Agarwal, and D. Pathak. Extreme parkour with legged robots. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 11443–11450. IEEE, 2024. 

- [17] M. Y. Galliker. Whole-body humanoid mpc: Realtime physics-based procedural locomanipulation planning and control. https://github.com/1x-technologies/wb ~~h~~ umanoid ~~m~~ pc, 2024. 

- [18] N. Scianca, D. De Simone, L. Lanari, and G. Oriolo. Mpc for humanoid gait generation: Stability and feasibility. _IEEE Transactions on Robotics_ , 36(4):1171–1188, 2020. 

- [19] S. Katayama, M. Murooka, and Y. Tazaki. Model predictive control of legged and humanoid robots: models and algorithms. _Advanced Robotics_ , 37(5):298–315, 2023. 

- [20] M. Yuan, T. Yu, H. Song, B. Li, X. Jin, H. Chen, and W. Zeng. Pvp: Data-efficient humanoid robot learning with proprioceptive-privileged contrastive representations. _arXiv preprint arXiv:2512.13093_ , 2025. 

- [21] N. Rudin, J. He, J. Aurand, and M. Hutter. Parkour in the wild: Learning a general and extensible agile locomotion policy using multi-expert distillation and rl fine-tuning. _arXiv preprint arXiv:2505.11164_ , 2025. 

- [22] Z. Wu, X. Huang, L. Yang, Y. Zhang, K. Sreenath, X. Chen, P. Abbeel, R. Duan, A. Kanazawa, C. Sferrazza, et al. Perceptive humanoid parkour: Chaining dynamic human skills via motion matching. _arXiv preprint arXiv:2602.15827_ , 2026. 

- [23] Y. Zhang, Y. Seo, J. Chen, Y. Yuan, K. Sreenath, P. Abbeel, C. Sferrazza, K. Liu, R. Duan, and G. Shi. Rpl: Learning robust humanoid perceptive locomotion on challenging terrains. _arXiv preprint arXiv:2602.03002_ , 2026. 

- [24] H. Wang, Z. Wang, J. Ren, Q. Ben, T. Huang, W. Zhang, and J. Pang. Beamdojo: Learning agile humanoid locomotion on sparse footholds. In _Robotics: Science and Systems XXI_ , 2025. 

- [25] W. Sun, B. Cao, L. Chen, Y. Su, Y. Liu, Z. Xie, and H. Liu. Learning perceptive humanoid locomotion over challenging terrain. In _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 6571–6578. IEEE, 2025. 

- [26] W. Sun, Y. Su, L. Huang, A. Zhang, D. Wei, M. San, D. Tian, E. Cao, B. Cao, Y. Liu, et al. Now you see that: Learning end-to-end humanoid locomotion from raw pixels. _arXiv preprint arXiv:2602.06382_ , 2026. 

- [27] Y. Hao, R. Yu, S. Luo, G. Zhang, J. Wu, and Q. Zhu. Cref: Cross-modal and recurrent fusion for depth-conditioned humanoid locomotion. _arXiv preprint arXiv:2603.29452_ , 2026. 

- [28] M. Wermelinger, P. Fankhauser, R. Diethelm, P. Kr¨usi, R. Siegwart, and M. Hutter. Navigation planning for legged robots in challenging terrain. In _2016 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 1184–1189. IEEE, 2016. 

- [29] P. Fankhauser, M. Bjelonic, C. D. Bellicoso, T. Miki, and M. Hutter. Robust rough-terrain locomotion with a quadrupedal robot. In _2018 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 5761–5768. IEEE, 2018. 

- [30] F. Jenelten, T. Miki, A. E. Vijayan, M. Bjelonic, and M. Hutter. Perceptive locomotion in rough terrain–online foothold optimization. _IEEE Robotics and Automation Letters_ , 5(4):5370–5376, 2020. 

11 

- [31] D. Kim, D. Carballo, J. Di Carlo, B. Katz, G. Bledt, B. Lim, and S. Kim. Vision aided dynamic exploration of unstructured terrain with a small-scale quadruped robot. In _2020 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 2464–2470. IEEE, 2020. 

- [32] A. Chilian and H. Hirschm¨uller. Stereo camera based navigation of mobile robots on rough terrain. In _2009 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pages 4571–4576. IEEE, 2009. 

- [33] C. Mastalli, I. Havoutis, A. W. Winkler, D. G. Caldwell, and C. Semini. On-line and on-board planning and perception for quadrupedal locomotion. In _2015 IEEE International Conference on Technologies for Practical Robot Applications (TePRA)_ , pages 1–7. IEEE, 2015. 

- [34] A. Agrawal, S. Chen, A. Rai, and K. Sreenath. Vision-aided dynamic quadrupedal locomotion on discrete terrain using motion libraries. In _2022 International Conference on Robotics and Automation (ICRA)_ , pages 4708–4714. IEEE, 2022. 

- [35] O. A. V. Magana, V. Barasuol, M. Camurri, L. Franceschi, M. Focchi, M. Pontil, D. G. Caldwell, and C. Semini. Fast and continuous foothold adaptation for dynamic locomotion through cnns. _IEEE Robotics and Automation Letters_ , 4(2):2140–2147, 2019. 

- [36] B. Yang, L. Wellhausen, T. Miki, M. Liu, and M. Hutter. Real-time optimal navigation planning using learned motion costs. In _2021 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 9283–9289. IEEE, 2021. 

- [37] C. Mastalli, M. Focchi, I. Havoutis, A. Radulescu, S. Calinon, J. Buchli, D. G. Caldwell, and C. Semini. Trajectory and foothold optimization using low-dimensional models for rough terrain locomotion. In _2017 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 1096–1103. IEEE, 2017. 

- [38] L. Wellhausen and M. Hutter. Rough terrain navigation for legged robots using reachability planning and template learning. In _2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 6914–6921. IEEE, 2021. 

- [39] R. Grandia, F. Jenelten, S. Yang, F. Farshidian, and M. Hutter. Perceptive locomotion through nonlinear model-predictive control. _IEEE Transactions on Robotics_ , 39(5):3402–3421, 2023. 

- [40] C. Mastalli, I. Havoutis, M. Focchi, D. G. Caldwell, and C. Semini. Motion planning for quadrupedal locomotion: Coupled planning, terrain mapping, and whole-body control. _IEEE Transactions on Robotics_ , 36(6):1635–1648, 2020. 

- [41] P. Fankhauser, M. Bloesch, and M. Hutter. Probabilistic terrain mapping for mobile robots with uncertain localization. _IEEE Robotics and Automation Letters_ , 3(4):3019–3026, 2018. 

- [42] F. Jenelten, J. He, F. Farshidian, and M. Hutter. Dtc: Deep tracking control. _Science Robotics_ , 9(86):eadh5401, 2024. 

- [43] S. Gangapurwala, M. Geisert, R. Orsolino, M. Fallon, and I. Havoutis. Real-time trajectory adaptation for quadrupedal locomotion using deep reinforcement learning. In _2021 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 5973–5979. IEEE, 2021. 

- [44] H. Kim, H. Oh, J. Park, Y. Kim, D. Youm, M. Jung, M. Lee, and J. Hwangbo. High-speed control and navigation for quadrupedal robots on complex and discrete terrain. _Science Robotics_ , 10(102):eads6192, 2025. 

- [45] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [46] M. Macklin. Warp: A high-performance python framework for gpu simulation and graphics. `https://github.com/nvidia/warp` , March 2022. NVIDIA GPU Technology Conference (GTC). 

12 

- [47] Z. Zhuang, Z. Fu, J. Wang, C. Atkeson, S. Schwertfeger, C. Finn, and H. Zhao. Robot parkour learning. In _Conference on Robot Learning (CoRL)_ , volume 229 of _Proceedings of Machine Learning Research_ , pages 73–92. PMLR, 2023. 

- [48] Y. Cheng, H. Liu, G. Pan, H. Liu, and L. Ye. Quadruped robot traversing 3d complex environments with limited perception. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 9074–9081. IEEE, 2024. 

- [49] C. Zhang, N. Rudin, D. Hoeller, and M. Hutter. Learning agile locomotion on risky terrains. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 11864–11871. IEEE, 2024. 

- [50] S. Zhu, R. Huang, L. Mou, and H. Zhao. Robust robot walker: Learning agile locomotion over tiny traps. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 15987–15993. IEEE, 2025. 

- [51] X. B. Peng, Z. Ma, P. Abbeel, S. Levine, and A. Kanazawa. Amp: Adversarial motion priors for stylized physics-based character control. _ACM Transactions on Graphics (ToG)_ , 40(4): 1–20, 2021. 

- [52] F. G. Harvey, M. Yurick, D. Nowrouzezahrai, and C. Pal. Robust motion in-betweening. _ACM Transactions on Graphics (TOG)_ , 39(4):60–1, 2020. 

- [53] J. P. Araujo, Y. Ze, P. Xu, J. Wu, and C. K. Liu. Retargeting matters: General motion retargeting for humanoid motion tracking. _arXiv preprint arXiv:2510.02252_ , 2025. 

- [54] M. Mittal, P. Roth, J. Tigue, A. Richard, O. Zhang, P. Du, A. Serrano-Mu˜noz, X. Yao, R. Zurbr¨ugg, N. Rudin, et al. Isaac lab: A gpu-accelerated simulation framework for multimodal robot learning. _arXiv preprint arXiv:2511.04831_ , 2025. 

13 

## **Appendix** 

### **Table of Contents** 

### **A. Policy Training Details** 

   - A.1 Policy Observation, Action, and Noise 

   - A.2 Termination Criteria 

   - A.3 Reward Function 

   - A.4 Ego-centric Depth Perception Details 

   - A.5 Flat Patch Sampling 

   - A.6 Terrain Configuration 

   - A.7 Policy Network 

   - A.8 Post-Training for Hardware Deployment 

   - A.9 AMP Training Details 

   - A.10 Terrain Edge Detector Algorithm 

- **B. Experiment Configurations** 

- **C. Simulation Evaluation Details** 

## **A Policy Training Details** 

### **A.1 Policy Observation, Action, and Noise** 

The actor and critic observations are summarized in Table 3. The policy uses an asymmetric actorcritic architecture: the actor receives noisy proprioceptive states and depth history; the critic additionally observes noise-free states and base linear velocity. All proprioceptive signals use a history of _h_ = 8 steps. Noise scales and distributions for each term are provided in Table 4. 

Table 3: Observation and action space specification. 

|**Space**|**Signal**|**Dim**|**Description**|
|---|---|---|---|
||Base Angular Velocity**_ω_**_t_|3|IMU gyroscope|
||Projected Gravity**g**_t_|3|Gravity direction in base frame|
||Velocity Commands**c**_t_|3|(_vx, vy, ωz_)|
|**Actor Obs**|Joint Positions**q**_t_|29|29-DoF joint angles|
||Joint Velocities ˙**q**_t_|29|29-DoF joint velocities|
||Last Action**a**_t−_1|29|Previous target joint positions|
||Depth History_Ht_|_m×H×W_|Strided depth frames (32_×_18each)|
|**Critic Obs**|+ Base Linear Velocity**v**_t_|3|Noise-free; critic only|
|**Action**|Target Joint Positions**a**_t_|29|Executed via PD control: **_τ_**_t_ =_kp_(**a**_t −_**q**_t_)_−kd_˙**q**_t_|


The detailed noise configuration for each proprioceptive term is summarized in Table 4. The detailed exteroceptive depth observation is illustrated in subsection 3.2. 

Table 4: Detailed policy <u>proprioceptive observation space, scaling factors, and noise models.</u> 

|**Observation Term**|**Scale**|**Noise Type**|**Noise Parameters**|
|---|---|---|---|
|Base Angular Velocity (_ωt_)|0_._25|Uniform|_U_(_−_0_._2_,_0_._2)rad/s|
|Projected Gravity (**g**_t_)|1_._0|Uniform|_U_(_−_0_._05_,_0_._05)|
|Velocity Commands (**c**_t_)|1_._0|None|N/A|
|Joint Positions (_qt_)|1_._0|Uniform|_U_(_−_0_._01_,_0_._01)rad|
|Joint Velocities (˙_qt_)|0_._05|Uniform|_U_(_−_0_._5_,_0_._5)rad/s|
|Last Action (_at−_1)|1_._0|None|N/A|


14 

### **A.2 Termination Criteria** 

To ensure stable and efficient training, the training episode terminates immediately if any of the following conditions are met. These criteria prevent the policy from exploring physically invalid states or dangerous configurations. The specific thresholds and parameters used in our MDP are detailed below: 

- **Time Out:** The episode terminates naturally if the maximum episode duration is reached. 

- **Terrain Out-of-Bounds:** The episode ends if the robot moves beyond the valid terrain boundaries. A distance buffer of 2 _._ 0 m is applied to allow for minor deviations at the boundaries. 

- **Illegal Contact:** To penalize falls, the episode terminates if the robot’s torso ( `torso` ~~`l`~~ `ink` ) experiences a contact force exceeding a threshold of 1 _._ 0 N. 

- **Bad Orientation:** To maintain stability, the episode ends if the tilt angle of the robot’s base exceeds 1 _._ 0 rad relative to the gravity vector. 

- **Insufficient Root Height:** The episode terminates if the robot’s root height drops below 0 _._ 5 m relative to the environment origin, indicating a fall or a failure to stand up. 

### **A.3 Reward Function** 

The reward function is designed to encourage velocity tracking while enforcing physical safety. It consists of four components: task reward, regularization reward, safety reward, and AMP-style reward. The detailed definition of each term, along with its corresponding weight and key parameters, is provided in Table 5. 

### **A.4 Ego-centric Depth Perception Details** 

### **A.4.1 Efficient Depth Simulation via Parallelized Ray-casting** 

To synthesize high-fidelity depth observations, we leverage the NVIDIA Warp framework [46] to implement a GPU-accelerated ray-caster. For each pixel ( _i, j_ ) in the image plane, a ray is emitted in direction **v** _i,j_ . The ray-caster computes the radial distance _di,j_ by identifying the first intersection with the scene geometry _G_ : 

|_di,j_ = min_{τ |_**p**_c_+_τ_**v**_i,j ∩G̸_ =_∅}._<br>(4)|
|---|


The orthogonal depth _zi,j_ is obtained by projecting onto the camera’s principal axis **n** _c_ : 


### **A.4.2 Bidirectional Depth Alignment and Noise Modeling** 

We define two transformation pipelines that map depth from each domain into a unified perception space _O_ , targeting _P_ ( _Fsim_ ( _dsim_ )) _≈ P_ ( _Freal_ ( _dreal_ )). 

**Simulation Pipeline** _Fsim_ Sequential stochastic operations applied to simulated depth: 

1. **Crop and Resize** : Rescaled to target resolution, focusing on the terrain-relevant bottomcenter region. 

2. **Range-dependent Gaussian Noise** : Additive noise _ϵ ∼N_ (0 _, σ_<sup>2</sup> ) injected within valid sensing range [ _dmin, dmax_ ]: _zi,j_<sup>_′_=</sup><sup>_zi,j_+</sup><sup>_ϵ ·_I[</sup><sup>_zi,j∈_[</sup><sup>_dmin, dmax_]].</sup> 

3. **Disparity Artifact Synthesis** : Contiguous pixels masked as invalid to simulate binocular matching failures. 

4. **Gaussian Blur** : Convolved with blur kernel **K** to simulate motion blur. 

5. **Clipping and Normalization** : Values clipped and normalized to [0 _,_ 1]. 

6. **Out-of-distribution (OOD) Perturbation** : With probability _Pood_ , the entire observation is replaced by Gaussian noise to handle transient perceptual failures. 

15 

Table 5: Detailed specifications of reward terms, weights, and mathematical formulations. 

|**Reward Term**|**Weight**|**Mathematical Formulation**|
|---|---|---|
|**_Task Reward_**|||
|Linear Vel Tracking (_vxy_)|2_._0|exp(_−∥_**v**<sup>_∗_</sup><br>_xy _<sup>_−_</sup><sup>**v**</sup>_xy_<sup>_∥_2</sup><sup>_/_0</sup><sup>_._52)</sup>|
|Angular Vel Tracking (_ωz_)|2_._0|exp(_−_(_ω_<sup>_∗_</sup><br>_z _<sup>_−ω_</sup>_z_<sup>)2</sup><sup>_/_0</sup><sup>_._52)</sup>|
|Heading Error|_−_1_._0|_|ω_<sup>_∗_</sup><br>_z_<sup>_|_</sup>|
|Don’t Wait|_−_0_._5|I(_v_<sup>_∗_</sup><br>_x _<sup>_>_ 0</sup><sup>_._3)</sup><sup>_·_ (I(</sup><sup>_v_</sup>_x _<sup>_<_ 0</sup><sup>_._15) + I(</sup><sup>_v_</sup>_x _<sup>_<_ 0) + I(</sup><sup>_v_</sup>_x _<sup>_< −_0</sup><sup>_._15))</sup>|
|Is Alive|3_._0|+1|
|Stand Still|_−_0_._3|(_∥_**q**_−_**q**_default∥_1_−_4_._0)_·_I(_∥_**v**<sup>_∗_</sup>_∥<_0_._15)_·_I(_|ω_<sup>_∗_</sup><br>_z_<sup>_| <_ 0</sup><sup>_._15)</sup>|
|**_Regularization Reward_**|||
|Edge Penetration|_−_4_._0|�_|P|_<br>_i_=1 <sup>_∥_</sup><sup>**d**</sup><sup>_i∥·_ (</sup><sup>_∥_</sup><sup>**v**</sup><sup>_i∥_+</sup><sup>_ϵ_)</sup>|
|Feet Air Time|0_._5|min_f_(_tphase,f_)_·_I(<sup>�</sup>_cf_ = 1)_·_I(_∥_**v**<sup>_∗_</sup>_∥>_0_._15)|
|Feet Slide|_−_0_._4|�<br>_f _<sup>_∥_</sup><sup>**v**</sup><sup>_xy,f∥·_ I(</sup><sup>_cf_)</sup>|
|Joint Deviation (Hip)|_−_0_._5|�<br>_j∈_hips<sup>(</sup><sup>_qj −qj,default_)2</sup>|
|Base Ang Vel (XY) (_L_2)|_−_0_._05|_∥ωxy∥_<sup>2</sup>|
|Joint Torques (_L_2)|_−_1_._5e-7|_∥_**_τ_**_legs∥_<sup>2</sup>|
|Joint Acc (_L_2)|_−_1_._25e-7|_∥_¨**q**_∥_<sup>2</sup>|
|Joint Vel (_L_2)|_−_1_._0e-4|_∥_˙**q**_∥_<sup>2</sup>|
|Action Rate (_L_2)|_−_0_._005|_∥_**a**_t −_**a**_t−_1_∥_<sup>2</sup>|
|Flat Orientation|_−_3_._0|_∥_**g**<sup>_proj_</sup><br>_xy_<br>_∥_<sup>2</sup>|
|Pelvis Orientation|_−_3_._0|_∥_**g**<sup>_proj,pelvis_</sup><br>_xy_<br>_∥_<sup>2</sup><br>|
|Feet Orientation|_−_0_._4|�<br>_f _<sup>_∥_</sup><sup>**g**</sup><sup>_proj_</sup><br>_xy,f_<sup>_∥·_ I(</sup><sup>_cf_)</sup>|
|Feet Height Error|_−_0_._1|�<br>_f_<br>�<br>_p_ <sup>clip(</sup><sup>_hf −hterr,p −_0</sup><sup>_._035</sup><sup>_,_ 0</sup><sup>_,_ 0</sup><sup>_._3)</sup><sup>_·_ I(</sup><sup>_cf_)</sup>|
|Feet Distance|0_._4|exp(_−_max(0_,_0_._12_−|y_<sup>_R_</sup><br>_L _<sup>_−yR_</sup><br>_R_<sup>_|_)</sup><sup>_/_0</sup><sup>_._05)</sup><sup>_−_1</sup>|
|Energy Consumption|_−_5_._0e-5|�<br>_j_<sup>(</sup><sup>_τj_ ˙</sup><sup>_qj/kj_)2</sup>|
|Freeze Upper Body|_−_0_._004|_∥_**q**_upper −_**q**<sup>_default_</sup><br>_upper _<sup>_∥_</sup>1|
|**_Safety Reward_**|||
|Joint Pos Limits|_−_1_._0|�<br>_j_<sup>(max(0</sup><sup>_, qj −qj,max_) + max(0</sup><sup>_, qj,min −qj_))</sup>|
|Joint Vel Limits|_−_1_._0|�<br>_j_ <sup>max(0</sup><sup>_, |_ ˙</sup><sup>_qj| −_0</sup><sup>_._9 ˙</sup><sup>_qj,max_)</sup>|
|Torque Limits|_−_0_._01|�<br>_j_ <sup>max(0</sup><sup>_, |τj| −_0</sup><sup>_._8</sup><sup>_τj,max_)2</sup>|
|Undesired Contacts|_−_1_._0|I(count(collision_body\feet_)_>_0)|
|**_AMP Reward_**|||
|AMP Style|0_._25|max<br>�<br>0_,_1_−_0_._25(_D_(**S**_t_)_−_1)<sup>2�</sup>|


**Real-world Pipeline** _Freal_ Applied to the physical depth stream during deployment: 

1. **Crop and Resize** : Aligned to simulation input geometry. 

2. **Depth Inpainting** : Recovers zero-valued pixels caused by occlusion or disparity shadows. 

3. **Gaussian Blur** : Suppresses high-frequency sensor jitter. 

16 

### **A.4.3 Temporal Depth Aggregation via Strided Sampling** 

The policy receives a history buffer of _m_ depth frames sampled at temporal stride _ℓ_ and delayed by one frame to emulate sensor latency: 


This representation spans ( _m −_ 1) _· ℓ_ steps using _m_ frames. The stride spaces the historical samples without reducing the update rate of the newest frame. 

### **A.5 Flat Patch Sampling** 

#### **Algorithm 1: Flat Patch Sampling** 

**Input :** Mesh _M_ , Patch radius _r_ , Max height difference _δ_ **Output:** Set of valid targets _P_ 

- **1 while** _|P| < Ntargets_ **do** 

- **2** Sample a random 2D position ( _x, y_ ) in the environment 

- **3** Ray-cast to get a set of heights _H_ within radius _r_ around ( _x, y_ ) 

- **4 if** max( _H_ ) _−_ min( _H_ ) _< δ_ **then** 

- **5** Add ( _x, y,_ avg( _H_ )) to _P_ 

- **6 return** _P_ 


Figure 9: Flat patches on different terrains. 

Unless otherwise specified, the command-generation and flat-patch parameters are _ϵ_ = 1 _×_ 10<sup>_−_6</sup> , _kv_ = 2 _._ 0, _kω_ = 2 _._ 0, target radius _r_ = 0 _._ 2, and flatness threshold _δ_ = 0 _._ 05. 

### **A.6 Terrain Configuration** 

To ensure the robot learns robust locomotion skills across diverse environments, we employ a curriculum-based terrain generation pipeline. The training environment consists of a grid of 10 _×_ 20 sub-terrains, each measuring 8 _._ 0 _×_ 8 _._ 0 meters. The height field resolution is set to 0 _._ 05 m horizontally and 0 _._ 005 m vertically. 

The detailed specifications for each terrain type, including their geometric parameters, curriculum proportions, and the associated velocity command ranges used for training, are summarized in Table 7. We randomly generate walls around the terrains to simulate an indoor environment with probability _P_ = 0 _._ 3. Note that we use Rough (Stand) to train the robot for in-place turning. 

### **A.7 Policy Network** 

The learning framework consists of three primary components: a CNN-based visual encoder, a Mixture-of-Experts (MoE) policy, and an Adversarial Motion Prior (AMP) discriminator. The visual encoder processes the strided depth history through a convolutional network, followed by a 

17 

projection MLP to extract a visual embedding. This embedding is concatenated with the proprioceptive observations and fed into the MoE-based actor-critic network, where a gating mechanism dynamically weights the contributions of multiple expert networks to generate robust actions. Additionally, the AMP discriminator distinguishes between the actor’s generated motions and the reference dataset. The detailed hyperparameters for these components are listed in Table 6. 

Table 6: Detailed hyperparameters for the network architecture. 

|**Parameter**|**Value**|
|---|---|
|CNN channels|[4]|
|CNN kernel sizes|[3]|
|CNN strides|[1]|
|CNN paddings|[1]|
|CNN pooling|MaxPool|
|Encoder projection units|[256_,_256]|
|Encoder embedding dim|128|
|Encoder activation|ReLU|
|Policy Type|MoE|
|Number of Experts|4|
|Gating hidden units|[256]|
|Expert hidden units|[256_,_128_,_64]|
|Policy activation|ELU|
|Discriminator hidden units|[1024_,_512]|
|Discriminator activation|ReLU|


Table 7: Detailed specifications of terrain types and their corresponding velocity command ranges for walking and running modes. Note that the lateral velocity command _vy_ is set to 0 for all terrain types. 

||**Terrain Settings**|**Com**|**mand Range**|**(walking)**|**Co**|**mmand Ran**|**ge (run)**|
|---|---|---|---|---|---|---|---|
|**Terrain Type**|**Geometric Parameters**|**Prop.**|**vx (m/s)**|_ω_**z (rad/s)**|**Prop.**|**vx (m/s)**|_ω_**z (rad/s)**|
|Rough|Perlin Noise Scale_∈_[0_._0_,_0_._1]m|5%|[0_._45_,_1_._0]|[_−_1_._0_,_1_._0]|20%|[1_._95_,_3_._05]|[_−_1_._0_,_1_._0]|
|Rough (Stand)|Perlin Noise Scale_∈_[0_._0_,_0_._1]m|5%|0_._0|[_−_1_._0_,_1_._0]|5%|0_._0|[_−_1_._0_,_1_._0]|
|Square Gaps|Gap Dist_∈_[0_._1_,_0_._7]m, Depth_∈_[0_._4_,_0_._6]m|10%|[0_._45_,_0_._8]|[_−_1_._0_,_1_._0]|_−_|_−_|_−_|
|Stairs Down|Step Height_∈_[0_._05_,_0_._23]m, Width0_._3m|15%|[0_._45_,_0_._8]|[_−_1_._0_,_1_._0]|_−_|_−_|_−_|
|Platform Down|Platform Height_∈_[0_._05_,_0_._45]m|10%|[0_._45_,_0_._8]|[_−_1_._0_,_1_._0]|25%|[1_._95_,_3_._05]|[_−_1_._0_,_1_._0]|
|Stairs Up|Step Height_∈_[0_._05_,_0_._23]m, Width0_._3m|15%|[0_._45_,_0_._8]|[_−_1_._0_,_1_._0]|_−_|_−_|_−_|
|Platform Up|Platform Height_∈_[0_._05_,_0_._45]m|10%|[0_._45_,_0_._8]|[_−_1_._0_,_1_._0]|25%|[1_._95_,_3_._05]|[_−_1_._0_,_1_._0]|
|Discrete Boxes|Height_∈_[0_._05_,_0_._45]m, Width_∈_[0_._8_,_1_._5]m|10%|[0_._45_,_0_._8]|[_−_1_._0_,_1_._0]|_−_|_−_|_−_|
|Mesh Boxes|Height Mean_∈_[0_._1_,_0_._4]m|10%|[0_._45_,_0_._8]|[_−_1_._0_,_1_._0]|_−_|_−_|_−_|
|Slopes|Slope_∈_[0_._0_,_0_._7]rad|10%|[0_._45_,_0_._8]|[_−_1_._0_,_1_._0]|25%|[1_._95_,_3_._05]|[_−_1_._0_,_1_._0]|


### **A.8 Post-Training for Hardware Deployment** 

The general walking policy is trained across multiple terrain categories and serves as the initialization for hardware post-training. To improve hardware stability, we fine-tune three specialized policies from this checkpoint: _stair walking_ , _platform walking_ , and _running_ . Each specialized policy is trained for an additional 40 _,_ 000 iterations. During hardware deployment, the specialized policies handle their respective tasks, while the general walking policy handles the remaining walking tasks. 

Post-training is conducted on flat ground combined with the relevant target terrain. To focus each policy on its intended operating regime, we narrow the velocity command range compared to general training: the walking policies use _vx ∈_ [0 _._ 45 _,_ 0 _._ 55] m/s and the running policy uses 

18 

_vx ∈_ [1 _._ 95 _,_ 3 _._ 05] m/s. The lateral command is fixed at _vy_ = 0 for all post-training runs. All other training hyperparameters remain identical to those used in the general policy. 

### **A.9 AMP Training Details** 

### **A.9.1 Reference Dataset Composition** 

The reference dataset _D_ is collected at 50 Hz from three sources: 

1. **Synthetic Data** : Walking motions from an MPC controller [17]. 

2. **Human Motion** : Mocap data captured via the NOKOV system, including stair and platform traversal, retargeted to the robot via GMR [53]. 

3. **Running Motion** : High-speed running clips from the LAFAN dataset [52]. 

To avoid mode collapse, walking and running policies use separate datasets: _D_ walk combines sources 1 and 2 ( _T_ = 379 _._ 62 s); _D_ run uses source 3 ( _T_ = 1 _._ 54 s, one gait cycle). Symmetric augmentation is applied to all datasets. Joint training produces fast walking with long strides rather than natural running. We attribute this to the lack of transition data between walking demonstrations (up to 1 m/s) and running demonstrations (above 2 m/s), together with the smaller amount of running data. The running policy is therefore initialized from the general walking checkpoint and trained separately using _D_ run, as described in subsection A.8. Despite the narrow running distribution, the policy naturally generalizes to turning and climbing at inference time. This suggests that AMP requires as little as a single complete gait cycle to effectively imitate a target motion style, making it practical to deploy with minimal reference data. 

### **A.9.2 Discriminator and Style Reward** 

The discriminator _D_ ( **S** ) receives short temporal sequences rather than single state pairs, enabling it to capture motion dynamics. It is trained with a least-squares (MSE) loss: 


where _M_ is the reference dataset and _P_ is the policy rollout. Gradient penalty and weight decay are applied for training stability. The style reward fed back to the policy is: 


Compared to binary cross-entropy and log-based rewards, this combination of an MSE loss and a quadratic reward yields smoother, non-saturating gradients, improving convergence toward the reference motion manifold. 

### **A.10 Terrain Edge Detector Algorithm** 

We first identify sharp terrain edges by comparing the dihedral angle between adjacent faces to a predefined threshold _τ_ , as shown in algorithm 2. 

19 

|**Algorithm 2: Terrain Edge Detection Algorithm**|
|---|
|**Input :** Triangular Mesh_M_= (_V, F_), Sharpness Threshold_τ_, Cylinder Radius_r_, Grid Resolution<br>_N_grid<br>**Output:**Spatial Collision Grid_S_|
|`/* 1.`<br>`Sharp Edge Detection`<br>`*/`|
|**1** Let_A_be the set of face adjacencies in_M_<br>**2** Initialize raw edge set_E_raw _←∅_<br>**3 foreach**_adjacency a ∈A_**do**|
|**4**<br>Let_αa_ be the dihedral angle of_a_|
|**5**<br>**if**_αa > τ_ **then**|
|**6**<br>Let(_vi, vj_)be the vertex indices shared by_a_<br>**7**<br>Add the segment coordinates(_V_[_vi_]_, V_[_vj_])to_E_raw|
|`/* 2.`<br>`Edge Processing`<br>`*/`|
|**8 if**_Eraw is empty_**then**<br>**9**<br>**return**_None_<br>**10 else**|
|**11**<br>_E_final _←_`ProcessEdges`(_E_raw)|
|`/* 3.`<br>`Spatial Structure Construction`<br>`*/`|
|**12** Initialize cylinder set_C ←∅_<br>**13 foreach**_segment e ∈Efinal_ **do**<br>**14**<br>Construct cylinder_c_from segment_e_with radius_r_<br>**15**<br>Add_c_to_C_<br>**16** _S ←_`CylinderSpatialGrid`(_C, N_grid)<br>**17 return**_S_|


Then, we employ a greedy edge concatenation process to refine raw edges, as shown in algorithm 3. By merging adjacent collinear segments into single extended edges, this approach significantly reduces storage requirements and reduces computation time. 

#### **Algorithm 3: Greedy Edge Concatenation Process** 

**Input :** Edge set _Eraw_ , Angle threshold _θ_ , Min points _k_ min, Tol _ϵ_ **Output:** Processed Edge _Efinal_ **1** _G ←_ BuildAdjacency( _Eraw_ ) **2** _Savail ←_ Vertices( _G_ ) **3** _τ ←_ cos( _θ_ ) **4** _E_ final _←∅_ **5 while** _Savail̸_ = _∅_ **do 6** _v ←_ PopArbitrary( _Savail_ ) **7** _P ←_ [ _v_ ] **8 if** _G_ [ _v_ ] _̸_ = _∅_ **then 9** Append neighbor of _v_ to _P_ and update _G_ **10 repeat 11 foreach** _end ∈{head, tail}_ **do 12** Let **d** be the direction vector at _end_ **13** Find neighbor _n ∈ G_ [ _P._ get( _end_ )] maximizing alignment with **d 14 if** _alignment > τ_ **then 15** _P._ extend( _n_ ) at _end_ **16** Remove edge to _n_ from _G_ and _Savail_ **17 until** _cannot extend_ **18 while** _|P | ≥ k_ min **do 19** Find smallest index _i_ such that Dist( _P_ [ _i . . ._ end] _,_ Line( _P_ [ _i_ ] _, P_ [end])) _< ϵ_ **20 if** _segment found_ **then 21** _Efinal._ append( _{P_ [ _i_ ] _, P_ [end] _}_ ) **22** _P ← P_ [0 _. . . i_ ] **23 else 24 break 25 return** _Efinal_ 

20 

## **B Experiment Configurations** 

**Training Environment:** We train our policies using NVIDIA Isaac Sim and Isaac Lab [54] on an NVIDIA RTX 4090 GPU, parallelized with 4096 humanoid robot agents. We use the 29-DoF Unitree G1 humanoid robot for both simulation and physical deployment. The proprioceptive history length is _h_ = 8 steps, and the depth history uses _m_ = 8 strided frames with stride _ℓ_ . 

**Hardware and Perception:** For real-world deployment, we use the factory-integrated Intel RealSense D435i depth camera (standard on Unitree G1, no hardware modification). Depth images are captured at 60 Hz at 480 _×_ 270, downsampled to 64 _×_ 36, and cropped to 32 _×_ 18 as policy input. 

**Onboard Deployment:** The policy runs at 50 Hz on the onboard NVIDIA Jetson Orin NX via `onnxruntime` . Depth acquisition and preprocessing run asynchronously at 60 Hz to minimize latency. 

**Operator Guidance:** During hardware deployment, a human operator provides velocity commands through a remote controller, while the policy generates joint position targets from onboard observations. The position-based command generation procedure is used during training. Hardware operation therefore consists of perceptive locomotion under operator guidance. Policy changes follow a stop–stand–switch procedure: the robot stops, transitions to a standing policy, and then switches to the selected locomotion policy. 

**Safety and Broader Impact:** Perceptive locomotion can extend humanoid operation to uneven outdoor terrain, but falls and unintended motion can endanger nearby people. Hardware testing should therefore remain under continuous human supervision, with an accessible emergency-stop mechanism. Tests in public spaces should use a clearly marked exclusion zone that keeps bystanders outside the robot’s operating and potential fall area. Given the limited failure-recovery capability, the reported results do not establish safety for unsupervised operation around people. 

## **C Simulation Evaluation Details** 

For the comparison and ablation study in subsection 4.3, we evaluate each method with 1,000 parallel humanoid agents in simulation and report the success rate and mean reaching time in Table 2. A trial is considered successful if the robot reaches within 0.25 m of the target position within 15 s without triggering termination. The reaching time is computed for successful trials; entries marked as “–” indicate cases where no trial succeeds within the 15 s time limit, and the reaching time is therefore not reported. 

All methods are tested on the same terrain categories in Table 2, including large box, ramp, small box, rough terrain, stair down, platform down, stair up, platform up, and gap. To make the commandgeneration ablation more discriminative, we use challenging evaluation terrains with the final geometry settings summarized in Table 8. These terrains expose the failure mode of the _w/o positionbased_ baseline, which often refuses to climb the obstacle or turns around instead of reaching the specified target. 

Table 8: Terrain geometry settings used for the simulation comparison and ablation study. 

|**Terrain Type**|**Evaluation Geometry**|
|---|---|
|Stair up/down|Step height0_._20m|
|Large box|Height0_._40m|
|Platform up/down|Platform height0_._40m|
|Ramp|Slope0_._40rad|
|Gap|Gap distance0_._60m|
|Rough terrain|Noise scale0_._05|
|Small box|Height [0_._25_,_0_._35] m;<br>width and length randomly sampled from<br>[0_._30_,_0_._50]m|


21 

Because related perceptive locomotion methods do not provide directly reusable implementations or a shared benchmark, we use a best-effort reimplementation of HPL [15] for the Unitree G1 in our training environment. The simulation comparison uses one generalist walking policy per method across all terrain categories. 

22 

