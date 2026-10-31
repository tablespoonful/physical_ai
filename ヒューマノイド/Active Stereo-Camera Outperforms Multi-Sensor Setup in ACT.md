---
title: "Active Stereo-Camera Outperforms Multi-Sensor Setup in ACT Imitation Learning for Humanoid Manipulation"
date: "2026-03-30"
authors: "Robin Kühn; Moritz Schappler; Thomas Seel; Dennis Bank"
url: https://arxiv.org/abs/2603.28422
pdf: https://arxiv.org/pdf/2603.28422
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.28422)** / [論文ページ](https://arxiv.org/abs/2603.28422)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Active Stereo-Camera Outperforms Multi-Sensor Setup in ACT Imitation Learning for Humanoid Manipulation** 

Robin K¨uhn<sup>1</sup> , Moritz Schappler<sup>1</sup> , Thomas Seel<sup>1</sup> and Dennis Bank<sup>1</sup> 

**_Abstract_ — The complexity of teaching humanoid robots new tasks is one of the major reasons hindering their widespread adoption in the industry. While Imitation Learning (IL), particularly Action Chunking with Transformers (ACT), enables rapid task acquisition, there is no consensus yet on the optimal sensory hardware required for manipulation tasks. This paper benchmarks 14 sensor combinations on the Unitree G1 humanoid robot equipped with three-finger hands for two manipulation tasks. We explicitly evaluate the integration of tactile and proprioceptive modalities alongside active vision. Our analysis demonstrates that strategic sensor selection can outperform complex configurations in data-limited regimes while reducing computational overhead. We develop an opensource** **_Unified Ablation Framework_ that utilizes sensor masking on a comprehensive master dataset. Results indicate that additional modalities often degrade performance for IL with limited data. A minimal active stereo-camera setup outperformed complex multi-sensor configurations, achieving 87.5% success in a spatial generalization task and 94.4% in a structured manipulation task. Conversely, adding pressure sensors to this setup reduced success to 67.3% in the latter task due to a low signal-to-noise ratio. We conclude that in data-limited regimes, active vision offers a superior trade-off between robustness and complexity. While tactile modalities may require larger datasets to be effective, our findings validate that strategic sensor selection is critical for designing an efficient learning process. Code is available at http://github.com/kuehnrobin/ UAF_unitree_g1.** 

## I. INTRODUCTION 

While classical robots lack the flexibility to operate in unstructured environments, humanoids operate in humancentric spaces without requiring infrastructure modifications [1]. However, programming complex manipulation remains challenging. Imitation Learning (IL) approaches like Action Chunking with Transformers (ACT) [2] address this hurdle by enabling robots to learn fine-grained manipulation from demonstrations [3]. 

Despite the success of recent IL frameworks [4], [5], there is no consensus on the optimal sensory hardware required. While works like Bi-ACT [3], [6] suggest the utility of joint torques, and OpenTelevision [7] advocates for active vision, these modalities are typically validated without rigorous comparison to alternative setups. Recent frameworks like ULTRA [8] highlight the ongoing, complex efforts to unify multimodal sensor streams for autonomous behavior, underscoring the need for a foundational understanding of which sensors actually benefit the learning process. 

> 1The authors are with the Institute of Mechatronic Systems, Leibniz University Hannover, 30167 Hannover, Germany. robin.kuehn@imes.uni-hannover.de, _{_ dennis.bank, moritz.schappler, thomas.seel _}_ @imes.uni-hannover.de 

Crucially, these modalities are evaluated across diverse robotic platforms with varying sensor fidelity. For instance, Mobile ALOHA utilizes ViperX/WidowX arms [4], OpenTelevision evaluates on full-size humanoids (Unitree H1, Fourier GR-1) [7], and Bi-ACT relies on the Dynamixelbased ALPHA- _α_ platform [6]. Consequently, it remains unclear whether reported performance gains stem from the inherent value of the added modalities or merely from specific hardware characteristics. Classically, evaluating different sensor setups requires recording separate datasets or comparing results across different research papers. Both approaches introduce varying operator skill and demonstration quality as hidden variables, which diminishes the validity of the comparison. 

To bridge this gap, a unified benchmark on a single platform is required. While an evaluation on a single platform cannot claim universal transferability to high-fidelity, custom-built robots, it is uniquely suited for a controlled ablation study to isolate the impact of sensor selection. We purposefully conduct this evaluation on the Unitree G1 (version Edu-U4) equipped with standard three-finger hands, as it is representative of the emerging class of cost-effective, commercially available humanoids. As the community increasingly adopts such platforms, integrating their inherently noisy, lower-fidelity sensors presents unique challenges for imitation learning. Identifying the minimal viable sensor set here not only improves robustness but also reduces required computational resources and hardware costs. 

To achieve this, we benchmark 14 distinct sensor configurations across two complementary manipulation tasks. Unlike prior studies, we explicitly investigate the integration of builtin finger-pressure sensors and torque-based proprioception alongside active and passive vision. To ensure strict comparability across these setups, we introduce an open-source _Unified Ablation Framework_ (UAF). This pipeline trains multiple policy variations from a single master dataset via sensor masking, effectively eliminating human demonstration variance as a confounding factor. By training all policies on identical human trajectories, our framework guarantees that performance differences are uniquely attributable to the chosen sensory input. 

The main contributions of this work are: 

- 1) **Unified Ablation Framework (UAF):** We introduce an open-source toolchain utilizing sensor masking on a shared master dataset, building upon the LeRobot Framework [9]. This allows for a comparison of sensor configurations by guaranteeing identical training episodes regarding the human demonstrations. The UAF is made publicly 

available at https://github.com/kuehnrobin/ UAF_lerobot. 

- 2) **Extensive Evaluation of Sensor Modalities:** We provide an extensive evaluation of the impact of different sensory combinations on the performance of ACT IL. This includes proprioception by utilizing the pressure sensors from the Unitree Dex3 hands [10]. The collected training data for both evaluated tasks is made open-source and represents typical _data-limited regimes_ (defined here as _≤_ 250 demonstrations). Specifically, the _sort cans_ task consists of 20 episodes (approx. 1 hour of demonstration data) [11], and the _place cubes in box_ task consists of 242 episodes (approx. 2 hours of demonstration data) [12]. 

- 3) **Minimalist Design Guidelines:** We validate that a single active stereo-camera is often sufficient for designing an efficient learning process for ACT-based IL for humanoid manipulation in such data-limited regimes. 

After introducing related work (Sec. II), methodology (Sec. III) and discussing results (Sec. IV), the latter point of practical design guidelines is elaborated in Sec. V. This is followed by a discussion of limitations in Sec. VI and concluded in Sec. VII. 

## II. RELATED WORK 

## _A. Imitation Learning for Humanoid Manipulation_ 

Imitation Learning (IL) has evolved from simple Behavior Cloning to sophisticated sequence modeling. Action Chunking with Transformers (ACT) [2] and Diffusion Policies [13], [14] have emerged as dominant architectures. Subsequent frameworks have scaled these methods to complex wholebody humanoid control [5] and bimanual mobile manipulation [4]. To facilitate data collection for these data-hungry models, recent works explore robot-free demonstration interfaces [15] or implicit kinodynamic motion retargeting [16]. However, while frameworks like OpenTelevision [7] compare different visual sensory modalities, the question of the minimal sufficient sensor set for stationary manipulation tasks on standard hardware remains unanswered. 

## _B. Active Perception in Imitation Learning_ 

Active vision has gained traction in IL through frameworks like OpenTelevision [7] and Vision-in-Action [17]. Unlike classical active perception, which often relies on heuristics, these approaches learn active perceptual strategies end-to-end from human demonstrations. The efficacy of pure vision-based pipelines on the Unitree G1 has also been demonstrated in highly dynamic tasks, such as perceptive parkour [18]. This decoupling of the camera view from the torso notably improves performance compared to static baselines. However, current research validates these learned active perception policies primarily in isolation. Our work extends this by exploring interference effects when combining active vision with static wide-angle views. 

## _C. Tactile and Proprioceptive Feedback in IL_ 

While visual inputs are standard in Transformer-based IL, the integration of haptics and proprioception has only 

recently gained traction. Methods like Bi-ACT [3] utilize joint velocities and estimated forces for force-sensitive tasks. To capture high-fidelity contact dynamics, recent systems propose specialized hardware. Choi et al. employ a custom 6-DoF force/torque sensor at the fingertips in UMI-FT [19], while TACT [20] extends ACT with advanced tactile sensor arrays across the robot’s body to stabilize whole-body manipulation. However, there is a noteworthy gap between these custom, high-end sensor suites and the standard hardware of emerging commercial humanoids, which typically rely on basic fingertip pressure sensors and direct motor torques. The utility of integrating these standard, built-in modalities into ACT policies remains largely unexplored. We address this gap by evaluating whether the inclusion of these accessible tactile and proprioceptive sensors provides a tangible performance benefit for manipulation tasks in data-limited regimes. 

## III. METHODOLOGY 

To isolate the influence of sensor selection on policy performance, we developed a standardized experimental framework using the Unitree G1 humanoid robot [21], [22]. 

## _A. Scope of the Data Regime_ 

Before detailing the system architecture, it is crucial to define the scope of our evaluation. Recent advancements in robotic manipulation span a wide spectrum of data regimes. While foundation models leverage massive datasets exceeding 100,000 episodes to learn generalized representations [23], single-task Imitation Learning typically relies on 50 to 250 demonstrations [2], [4], [13]. 

In this work, we explicitly target this _data-limited regime_ (defined as _≤_ 250 demonstrations), as it represents the most realistic scenario for rapid, on-the-fly skill acquisition without massive data collection infrastructure or the need for large-scale robot-free approximations [15]. 

## _B. Augmented ACT Architecture_ 

We utilize the Unitree wrapper [24] of the _LeRobot_ library [9] as the foundational codebase for our implementation of ACT [2]. The model operates as a Conditional Variational Autoencoder (CVAE) predicting action sequences _at_ : _t_ + _k_ based on current observations and a latent style variable _z_ . To ensure comparability with state-of-the-art baselines, we adopted the hyperparameter set from OpenTelevision [7] and utilized a ResNet18 visual backbone for all policies. 

**State-Space Augmentation:** We extended the standard LeRobot ACT implementation to obtain a configurable state vector (Fig. 1). Unlike the default implementation, which typically relies solely on joint positions, our modified proprioceptive encoder accepts an augmented vector _st_ . This vector concatenates joint positions _q ∈_ R<sup>_n_</sup> , velocities _q_ ˙ _∈_ R<sup>_n_</sup> , motor torques _τ ∈_ R<sup>_n_</sup> , and tactile pressure data _f_ pres _∈_ R<sup>_m_</sup> from the fingertips: 


These inputs are concatenated and projected via a learnable linear layer to match the transformer’s embedding dimension. 


Fig. 1: **Custom ACT Architecture:** Schematic representation integrating pressure sensors, joint velocities, and torques into the state observation vector. Building upon: [2], [7], [9]. 


Fig. 2: **Teleoperation Setup:** The operator controls the Unitree G1 (with three-finger hands) via VR. Head movements are synchronized, enabling the collection of active vision data. 

custom data loader applies a binary mask to the observation vector during training, dynamically omitting excluded sensor streams. This strictly enforces perfectly synchronized training episodes across all evaluated policies. 

**Policy Naming Convention:** We employ the following policy-naming scheme: Camera Setup <u>(</u> _<u>A</u>_ <u>ctive,</u> _<u>S</u>_ <u>tatic,</u> _<u>W</u>_ <u>rist)</u> and Proprioception <u>(</u> _<u>P</u>_ <u>ressure,</u> _<u>V</u>_ <u>elocity,</u> _<u>T</u>_ <u>orque).</u> When only one camera of a stereo-camera is used, it is denoted by an underscore _<u>Le</u> ft_ or _<u>Right</u>_ . For example, _WA − P_ denotes a policy using Wrist and Active cameras plus Pressure sensors. 

## _E. Experimental Tasks_ 

## _C. Teleoperation and Active Perception_ 

We implemented a VR-based teleoperation system building upon OpenTelevision and Unitree’s AVP ~~T~~ eleoperate [7], [25], using the Meta Quest 3 headset [26]. While recent systems like HumDex [27] expand the G1’s capabilities by integrating highly complex 20-DoF dexterous hands, we deliberately utilize the stock **7-DoF Dex3-1 hands** [10] to benchmark the baseline sensory requirements of commercially available humanoids. 

Our system retargets human hand motions using a modified DexPilot algorithm [28], [29]. Crucially, the operator views the environment directly through the robot’s active stereo-camera (Fig. 2). This creates a causal link between head movement and visual observation, enabling the ACT policy to learn _active perception_ strategies (e.g., visual search) from demonstrations. 

We selected two tasks to evaluate different policy attributes (Fig. 5, 6). To account for the variance introduced by randomization, we evaluated each policy over _N_ = 10 trials (Task 1, with six picked cans per trial) and _N_ = 15 trials (Task 2, with one cube per trial). 

_1) Sort Cans (Baseline Comparison):_ Adopted directly from OpenTelevision [7], this task serves as a standardized benchmark. It requires grasping and sorting beverage cans by color at predictable locations. 

_2) Grasp Cubes (Spatial Generalization):_ To test fine manipulation and spatial reasoning beyond the training distribution, we designed a task involving small (15 _×_ 15mm) cubes (Fig. 6). Unlike the structured can task, cube positions are randomized across the entire workspace during inference. This specifically challenges the policy’s depth perception and active search capabilities. 

## _F. Training Details_ 

## _D. Unified Ablation Framework_ 

To systematically evaluate the impact of sensor selection, we integrated a _Unified Ablation Framework_ directly into the LeRobot training pipeline (Fig. 3). 

**Master Dataset & Sensor Masking:** All demonstrations are recorded into a comprehensive dataset encompassing every available modality (Active Cam, Static Cam, Wrist Cams, _q,_ ˙ _q, τ, f_ pres). To emulate specific hardware setups, a 

To ensure full reproducibility and facilitate future research, the corresponding master datasets [11], [12] and the _Unified Ablation Framework_ (code at https://github. com/kuehnrobin/UAF_lerobot) are made publicly available. Model training was conducted on a workstation equipped with a single NVIDIA RTX 4090 (24 GB) GPU. Utilizing the LeRobot pipeline, each policy was trained with 80,000 optimization steps. The training took 7.3–20.6 h for 


Fig. 3: **Unified Ablation Framework:** To prevent human variance from influencing results, we record a master dataset with all sensors. During training, a masking module creates specific configurations (e.g., _A_ , _WA − P_ ) from identical demonstration data. 

the can-sorting ACT runs and 9.6–25.4 h for the cube-inbox ACT runs, depending on the selected sensor configuration. Since the training schedule in this work is stepbased, the equivalent number of epochs varies across sensor configurations (depending on dataset size and batch size). We empirically observed that both the validation loss and the physical behavioral performance stabilize well within this training budget. 

## IV. RESULTS AND DISCUSSION 

We evaluated 14 distinct sensor configurations across two manipulation tasks to identify the influence of sensor configuration on policy success for small datasets (Table I). The success rate represents the average completion score across five defined subtasks to capture partial progress. The optimal region in the result plots in Fig. 4 is the bottom-right corner, representing low execution time and high success rate. 

## _A. Task 1: Sort Cans (Structured Manipulation)_ 

The _Sort Cans_ task represents a structured environment with predictable object locations. Fig. 4 (a) illustrates the execution time and the success rate of the tested policies. 

**Competitive Performance of Active Vision Setup:** The _highest absolute performance_ was achieved by the complex configuration _WA − P ⃝_ 1 (Wrist + Active + Pressure) with a 

TABLE I: Performance Statistics per Policy and Task. All policies were trained for 80,000 optimization steps. Note: Evaluation counts (Trials) vary because failing policies (e.g., due to hovering) exceeded maximum trial durations, leading to truncated evaluations. 

|**Policy**|**Training**<br>**Time (h)**|**Trials**|**Execution**<br>**Time (min)**|**Success**<br>**Rate (%)**|
|---|---|---|---|---|
|**_Task 1: Can So_**|**_rting (20 E_**|**_pisodes)_**|||
|A|7.35|11|**3.9**|94.4|
|A-P|7.40|4|-|67.3|
|SW|-|6|4.2|76.4|
|_S_L_WA_|-|6|8.7|85.1|
|WA|20.58|11|5.8|93.6|
|WA-P|19.35|6|4.8|**97.6**|
|_WA_-_PV_A_T_A|15.35|7|5.6|94.5|
|_W_R_A_|10.32|5|5.9|94.8|
|**_Task 2: Cube i_**|**_n Box (242 _**|**_Episodes)_**|||
|A|11.51|15|**0.4**|**87.5**|
|S|9.56|6|-|10.0|
|_S_L_WA_-_P_|-|22|2.2|41.5|
|_S_L_WA_-_PV_A_T_A|32.07|15|2.4|56.7|
|WA|-|11|0.7|72.7|
|WA-P|13.58|20|0.7|68.1|
|_WA_-_PV_A_T_A|15.35|11|0.9|82.5|


mean **97.6%** success rate and a **4.8 min** mean execution time. This suggests that for structured tasks, the combination of close-up wrist views and tactile feedback can improve robustness. However, the minimal active stereocamera policy ( _A ⃝_ 2 ) remained _highly competitive_ with a mean **94.4%** success rate and the fastest mean execution time of **3.9 min** . This minimal setup operates with _a fraction of the state-vector complexity_ of multi-sensor configurations, directly translating to lower inference latency and reduced computational cost for training. 

**Comparison to State-of-the-Art:** To contextualize our performance, we compare our results against the OpenTelevision baseline [7], which utilized a similar ’Sort Cans’ task. Comparing against their ResNet18 baseline (to ensure backbone parity), they reported an 83% pick rate and a 50% place rate. While our policies _WA−P ⃝_ 1 and _A ⃝_ 2 achieved a higher overall success rate of 97.6% and 94.4%, we note that the OpenTelevision baseline was evaluated over only _N_ = 5 episodes and did use a slightly different method to determine the success rate [7]. The main reason for the performance increase is most likely the twofold amount of training data used by us. 

Moreover, we observed a frequent failure mode indicative of _mode averaging_ . The policy appeared to interpolate between the distinct trajectories targeting different drop zones, resulting in a path substantially lower than the training distribution and causing frequent collisions with the box rim or previously dropped cans (Fig. 7). 

**Low SNR in Tactile Modalities:** Crucially, adding pressure sensors to the active camera ( _A → A − P ⃝_ 3 ) caused a _substantial performance drop_ to **67.3%** . We hypothesize that without sufficient data to densely cover the tactile state-space, inference-time pressure signals deviate from the 


Fig. 4: **Execution time vs. success rate (Task 1):** The maximalist setup ( _WA − P_ ; marked with _⃝_ 1 in the plot) achieves the best combination of execution time and success. However, using only a single active stereo-camera ( _A ⃝_ 2 ) offers nearly identical results with a fraction of the statevector and thereby computational complexity. Notably, simply adding pressure sensors ( _A − P ⃝_ 3 ) causes a performance drop compared to the camera-only baseline. **Execution time vs. success rate (Task 2):** In generalization tasks, the minimal active setup ( _A ⃝_ 4 ) dominates with the combination of the highest success (mean **87.5%** ) and the fastest execution time with a mean of **0.4 min** . Conversely, setups involving static cameras (e.g., _S ⃝_ 5 , _S_ L _WA_ - _P ⃝_ 6 ) yield suboptimal performance and increased execution times. 

training distribution due to minor grasp variations. While the hardware sensor itself may possess a high signal fidelity, the policy interprets this out-of-distribution variance as informational noise. This drastically lowers the _effective, task-relevant signal-to-noise ratio_ for the learning process, destabilizing the grasp. Tactile data only aided performance when supported by wrist cameras ( _WA − P ⃝_ 1 ) to provide sufficient visual context to disambiguate the signals. 

## _B. Task 2: Grasp Cubes (Spatial Generalization)_ 

This task required the robot to locate and grasp small objects placed randomly within the workspace, testing the 


Fig. 5: Qualitative results of Fig. 6: Qualitative results of the _Sort Cans_ task ( _A_ policy). the _Grasp Cubes_ task ( _A_ polThe picture links to a video icy). The picture links to a of the autonomous task exevideo of the autonomous task cution. execution. 

policy’s ability to generalize to novel spatial configurations. Fig. 4 (b) shows the results. 

**Dominance of Active Vision:** Consistent with the findings in Task 1, the pure active vision setup ( _A ⃝_ 4 ) achieved the fastest execution times (mean **0.4 min** ) and the best success rate (mean **87.5%** ) with smaller state-vector and computational complexity than multi-sensor baselines. This dominance aligns with recent findings on active perception [17], stating that it can help to provide the IL policy with a focus on the most important object in the scene and thus improve the policy’s robustness. Our results indicate that _active perception is more critical for generalization_ than static multi-view redundancy. 

**Visual Interference and Hovering:** Policies using static cameras, either alone or combined with active vision, performed notably worse (e.g., _S_ , _S_ L _WA_ - _P ⃝_ 6 ). Qualitative analysis revealed a specific failure mode named _hovering behavior_ , where the robot freezes or oscillates during the approach phase. Crucially, this behavior was triggered specifically when combining the active stereo-camera with the static wide-angle head cameras. The inclusion of even a single static wide-angle feed alongside the active stream caused the policy to stall and greatly increased the execution time. This suggests a _feature conflict_ where the ResNet18based transformer architecture likely struggles to reconcile the dynamic, depth-resolved features of the active view with the conflicting spatial context of the static wide-angle view. Instead of adding information, the co-located static wideangle camera acts as a distractor, degrading the policy’s performance. It remains an open research question whether Vision Transformers (ViT) like DINOv3 [30], which are known for better feature separation, would exhibit the same sensitivity to this interference. 


Fig. 7: **Mode Averaging Failure in Task 1:** The policy fails to commit to a single drop-off target (e.g., green vs. red box) and instead generates a path that interpolates between the two distinct modes. This results in a trajectory that is notably lower than the demonstration data, causing the endeffector to collide with the box rim (2.1–2.3) or to collide with previously dropped cans (1.1–1.3). 

## V. SYNTHESIS AND PRACTICAL DESIGN GUIDELINES 

Combining the insights from both structured and unstructured tasks allows us to derive actionable design guidelines for ACT-based imitation learning on humanoid robots in data-limited regimes: 

- 1) **Active Vision is the Baseline:** A single active stereocamera ( _A_ ) proved to be the most robust single sensor, offering high generalization capabilities (Task 2) and competitive speed (Task 1). It should be the _default starting point_ for humanoid manipulation. 

- 2) **Modality Balance is Critical:** Adding tactile sensors ( _P_ ) is not inherently beneficial in small-data regimes. As seen in Task 1, tactile data requires supporting visual context (like wrist cameras) to be interpretable; otherwise, it acts as a noise source due to distribution shifts. Our findings indicate that optimal sensor configurations are highly context-dependent. Consequently, _simply maximizing the number of sensors does not guarantee superior performance_ . Moreover, minimizing the sensor set lowers the computational cost. In some cases, benchmarking to identify the most synergistic sensor set could be beneficial. 

- 3) **Avoid Co-Located Visual Redundancy:** We observed that combining active and static cameras on the same kinematic link (the head) causes _destructive interference_ . Efficient system design should prioritize a single, highquality active view over redundant static streams that introduce conflicting feature maps. 

- 4) **High-Quality Demonstrations are Key:** We observed qualitatively that human demonstrations should incorporate a large enough clearance to obstacles to account for mode averaging. 

## VI. LIMITATIONS 

While this study offers an extensive comparison, several limitations exist: 

- **Algorithm Specificity:** These findings are evaluated using ACT. Other leading architectures, such as Diffusion Policy [13], handle multi-modal action distributions differently and might exhibit varying robustness to informational noise. 

- **Teleoperation Latency:** The VR setup introduced a motion-to-photon latency of 0.5–1.0 seconds. While operators learned to compensate, this may have introduced artifacts (e.g., pauses) in the training data. However, since this latency was constant across the entire master dataset, it cannot explain the variance in performance (e.g., hovering behavior) observed solely between different sensor configurations. 

- **Task Diversity:** Both tasks were tabletop manipulation. The optimal sensor set for dynamic tasks, such as locomotion or whole-body lifting, may differ. 

- **Data Regime:** We focused on data-limited regimes. The benefit of complex modalities like tactile sensing might only materialize with significantly larger datasets. 

- **Sensor Fidelity and Hardware Specificity:** Our findings regarding proprioceptive and tactile modalities are inherently tied to the sensor fidelity of the Unitree G1 (e.g., current-based torque estimation and binarytending pressure sensors). On high-fidelity robotic platforms with highly accurate joint-torque sensors (e.g., DLR TORO [31]), proprioceptive feedback might prove more beneficial. Our results emphasize that for cost-effective hardware, sensor inclusion must be carefully weighed against the introduced noise. 

## VII. CONCLUSION AND FUTURE WORK 

This extensive benchmark of 14 sensor configurations for humanoid imitation learning _challenges the assumption_ that richer sensory data inherently leads to better policy performance. By introducing a _Unified Ablation Framework_ , we isolated the impact of sensor selection from human demonstration variance. 

Our results hint that in data-limited regimes, the _signalto-noise ratio of sensory modalities_ is a critical determinant of success. We identified that a minimalistic **active stereovision setup** offers a superior trade-off between robustness and complexity, often outperforming extensive multi-sensor arrays. Conversely, additional modalities like tactile pressure were observed to act as distractors when not supported by sufficient visual context or dataset scale. 

Ultimately, this study indicates that _hardware design for learning-based robots cannot be decoupled from the data regime_ . Future work will investigate the scaling laws of sensor fusion to determine the dataset thresholds required for tactile modalities to transition from noise sources to informative features, potentially leveraging novel synthetic data-generation pipelines like Real2Render2Real [32] to overcome physical data limitations. Moreover, we hypothesize that the observed trade-offs extend to broader classes 

of algorithms, including Diffusion Policies (e.g., utilizing 3D representations [14]) and Vision-Language-Action (VLA) models [23]. Determining whether the pre-trained representations in VLAs mitigate these noise sensitivities or if they exhibit similar failure modes in data-limited regimes constitutes an interesting potential for future cross-architecture research. 

- [13] C. Chi _et al._ Diffusion Policy: Visuomotor Policy Learning via Action Diffusion. [Online]. Available: http://arxiv.org/abs/2303.04137 

- [14] Y. Ze _et al._ Generalizable Humanoid Manipulation with 3D Diffusion Policies. [Online]. Available: http://arxiv.org/abs/2410.10803 

- [15] R. Nai _et al._ Humanoid Manipulation Interface: Humanoid WholeBody Manipulation from Robot-Free Demonstrations. [Online]. Available: http://arxiv.org/abs/2602.06643 

- [16] X. Chen, H. Wu, S. Wu, M. Zhou, D. Xiang, and H. Zhang. Implicit Kinodynamic Motion Retargeting for Human-to-humanoid Imitation Learning. [Online]. Available: http://arxiv.org/abs/2509.15443 

- [17] H. Xiong, X. Xu, J. Wu, Y. Hou, J. Bohg, and S. Song, “Vision in Action: Learning active perception from human demonstrations,” 2025. [Online]. Available: https://arxiv.org/abs/2506.15666 

## REFERENCES 

- [1] M. Shamsuddoha, T. Nasir, and M. S. Fawaaz, “Humanoid Robots like Tesla Optimus and the Future of Supply Chains: Enhancing Efficiency, Sustainability, and Workforce Dynamics,” _Automation_ , vol. 6, no. 1, 2025. [Online]. Available: https://www.mdpi.com/2673-4052/6/1/9 

- [2] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn, “Learning fine-grained bimanual manipulation with low-cost hardware,” 2023. [Online]. Available: https://arxiv.org/abs/2304.13705 

- [3] T. Buamanee, M. Kobayashi, Y. Uranishi, and H. Takemura, “Bi-ACT: Bilateral control-based imitation learning via action chunking with transformer,” 2024. [Online]. Available: https: //arxiv.org/abs/2401.17698 

- [4] Z. Fu, T. Z. Zhao, and C. Finn, “Mobile ALOHA: Learning bimanual mobile manipulation with low-cost whole-body teleoperation,” in _Conference on Robot Learning (CoRL)_ , 2024. [Online]. Available: https://mobile-aloha.github.io/ 

- [5] Z. Fu, Q. Zhao, Q. Wu, G. Wetzstein, and C. Finn, “Humanplus: Humanoid shadowing and imitation from humans,” in _Conference on Robot Learning (CoRL)_ , 2024. [Online]. Available: https: //humanoid-ai.github.io/ 

- [6] M. Kobayashi, T. Buamanee, and T. Kobayashi, “ALPHA- _α_ and Bi-ACT Are All You Need: Importance of Position and Force Information/ Control for Imitation Learning of Unimanual and Bimanual Robotic Manipulation With Low-Cost System,” _IEEE Access_ , vol. 13, pp. 29 886–29 899, 2025. [Online]. Available: https://ieeexplore.ieee.org/document/10883984 

- [7] X. Cheng, J. Li, S. Yang, G. Yang, and X. Wang, “Opentelevision: Teleoperation with immersive active visual feedback,” _arXiv preprint arXiv:2407.01512_ , 2024. [Online]. Available: https: //robot-tv.github.io/ 

- [8] X. He _et al._ ULTRA: Unified Multimodal Control for Autonomous Humanoid Whole-Body Loco-Manipulation. [Online]. Available: http://arxiv.org/abs/2603.03279 

- [9] R. Cadene _et al._ , “Lerobot: State-of-the-art machine learning for realworld robotics in pytorch,” https://github.com/huggingface/lerobot, 2024. 

- [10] Unitree Robotics, “Dex3-1,” 2025, accessed: 2026-03-18. [Online]. Available: https://www.unitree.com/Dex3-1 

- [11] R. K¨uhn, “Dataset G1 sort cans,” 2026, revision eefeb43. [Online]. Available: https://huggingface.co/datasets/kuehnrobin/uaf ~~g~~ 1 ~~s~~ ort ~~c~~ ans 

- [12] ——, “Dataset G1 cubes in box,” 2026, revision ba5d998. [Online]. Available: https://huggingface.co/datasets/kuehnrobin/uaf g1 ~~c~~ ubes ~~i~~ n ~~b~~ ox 

- [18] Z. Wu _et al._ Perceptive Humanoid Parkour: Chaining Dynamic Human Skills via Motion Matching. [Online]. Available: http: //arxiv.org/abs/2602.15827 

- [19] H. Choi _et al._ In-the-Wild Compliant Manipulation with UMI-FT. [Online]. Available: http://arxiv.org/abs/2601.09988 

- [20] M. Murooka _et al._ , “TACT: Humanoid Whole-body Contact Manipulation through Deep Imitation Learning with Tactile Modality,” _IEEE Robotics and Automation Letters_ , vol. 10, no. 8, pp. 7819–7826, 2025. [Online]. Available: http://arxiv.org/abs/2506.15146 

- [21] Unitree Robotics, “Unitree G1 Humanoid Robot,” 2025, accessed: 2026-03-18. [Online]. Available: https://www.unitree.com/g1 

- [22] U. Robotics, “Unitree G1 robot documentation,” https://www.docs. quadruped.de/projects/g1/html/index.html, 2024, accessed: 2026-0318. 

- [23] A. Brohan _et al._ RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control. [Online]. Available: http: //arxiv.org/abs/2307.15818 

- [24] Unitree Robotics, “Unitree IL LeRobot,” 2025. [Online]. Available: https://github.com/unitreerobotics/unitree ~~I~~ L ~~l~~ erobot 

- [25] ——, “avp ~~t~~ eleoperate,” https://github.com/unitreerobotics/ avp ~~t~~ eleoperate, 2023. 

- [26] Meta, “Quest 3,” 2023, accessed: 2026-03-18. [Online]. Available: https://www.meta.com/de/en/quest/quest-3/ 

- [27] L. Heng, Y. Tang, J. Xu, H. Bao, D. Huang, and Y. Wang. HumDex: Humanoid Dexterous Manipulation Made Easy. [Online]. Available: http://arxiv.org/abs/2603.12260 

- [28] A. Handa _et al._ , “Dexpilot: Vision-based teleoperation of dexterous robotic hand-arm system,” in _2020 IEEE International Conference on Robotics and Automation (ICRA)_ , 2020, pp. 9164–9170. 

- [29] Y. Qin, H. Su, and X. Wang, “From one hand to multiple hands: Imitation learning for dexterous manipulation from single-camera teleoperation,” 2023. [Online]. Available: https://arxiv.org/abs/2204. 12490 

- [30] O. Sim´eoni _et al._ DINOv3. [Online]. Available: http://arxiv.org/abs/ 2508.10104 

- [31] J. Englsberger _et al._ , “Overview of the torque-controlled humanoid robot TORO,” in _2014 IEEE-RAS International Conference on Humanoid Robots_ , 2014, pp. 916–923. [Online]. Available: https: //ieeexplore.ieee.org/document/7041473 

- [32] J. Yu _et al._ Real2Render2Real: Scaling Robot Data Without Dynamics Simulation or Robot Hardware. [Online]. Available: http://arxiv.org/abs/2505.09601 

