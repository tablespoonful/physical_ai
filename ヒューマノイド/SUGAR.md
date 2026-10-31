---
title: "SUGAR: A Scalable Human-Video-Driven Generalizable Humanoid Loco-Manipulation Learning Framework"
date: "2026-05-19"
authors: "Tianshu Wu; Xiangqi Kong; Yue Chen; Qize Yu; Hang Ye; Jia Li"
url: https://arxiv.org/abs/2605.20373
pdf: https://arxiv.org/pdf/2605.20373
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2605.20373)** / [論文ページ](https://arxiv.org/abs/2605.20373)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **SUGAR: A Scalable Human-Video-Driven** **<u>Generalizable Humanoid Loco-Manipulation</u> Learning Framework** 

**Tianshu Wu**<sup>**1***</sup> **Xiangqi Kong**<sup>**2***</sup> **Yue Chen**<sup>**1***</sup> Qize Yu<sup>1</sup> Hang Ye<sup>1</sup> Jia Li<sup>1</sup> Yizhou Wang<sup>1</sup> Hao Dong<sup>1</sup><sup>_†_</sup> 1CFCS, School of Computer Science, Peking University 2School of Computer Science and Engineering, Beihang University 

## **Abstract** 

Building humanoid robots that perform generalizable whole-body locomanipulation in the real world remains a fundamental challenge: existing approaches either rely on heavy task-specific reward engineering, rigidly replay reference motions that fail to generalize, or depend on costly teleoperation that limits scalability. While human videos capture diverse human behaviors, the motion priors inferred from them are inherently imperfect, suffering from occlusion, contact artifacts, and retargeting errors that render them unsuitable for direct policy learning. To this end, we present SUGAR, a data-driven framework that converts diverse human videos into deployable humanoid loco-manipulation skills, without any task-specific reward engineering or reference-motion conditioning at inference. SUGAR proceeds in three stages: First, a fully automated pipeline extracts kinematic interaction priors including human-object motion trajectories and contact labels from diverse human videos. Second, a privileged physics-based refiner utilizes a unified mimic-style reward and a progressive state pool to transform imperfect kinematic interaction priors into physically feasible, high-fidelity skills. Third, the refined skills are distilled into a deployable autonomous policy, which is implemented as a command generator paired with a command tracker. We evaluate our method on six representative loco-manipulation tasks in both simulation and real-world humanoid hardware. SUGAR substantially outperforms referencetracking baselines, and its performance scales clearly with the amount of human video data. It also achieves zero-shot real-world transfer with reliable closed-loop execution, autonomous failure recovery and stable long-horizon performance under external perturbations. Project Page: https://tianshuwu.github.io/sugar-humanoid/ 

## **1 Introduction** 

A general-purpose humanoid assistant must seamlessly coordinate locomotion, balance, and contactrich object manipulation in unstructured environments. Existing approaches each face a scalability bottleneck. Reinforcement learning from scratch achieves remarkable single-task results [Xue et al., 2025, He et al., 2025b, Liu et al., 2024, Wang et al., 2025c, Su et al., 2025] but relies on heavy task-specific reward engineering and environment design. Reference-motion tracking [Zhao et al., 2025, Weng et al., 2025] attains high-fidelity behavior but rigidly binds the policy to recorded trajectories, limiting generalization across object geometries and configurations. Teleoperation-based imitation learning [Luo et al., 2025, Ze et al., 2025, Li et al., 2025b, Ben et al., 2025, Li et al., 2025a] produces high-quality embodiment-consistent data but demands extensive human effort and specialized hardware. Across all three paradigms, the data and engineering costs grow steeply with task diversity, hindering progress toward general-purpose interaction. 

Preprint. 


Figure 1: **SUGAR enables generalizable real-world humanoid loco-manipulation from diverse human videos.** We deploy SUGAR on a Unitree G1 humanoid across six representative whole-body interaction tasks: (a) Push Box, (b) Pick Bottle, (c) Carry Box, (d) Sit Chair, (e) Kick Box, and (f1, f2) Pick Bottle under external human disturbances. 

Diverse human videos [Wang et al., 2026a, Mao et al., 2024, Yang et al., 2026a, Weng et al., 2025] offer a compelling escape from this bottleneck. However, while human-object interaction (HOI) videos are abundant, the kinematic data extracted from them is inherently imperfect. Severe occlusion, contact artifacts, and retargeting errors render this data physically implausible for direct imitation. Consequently, current methods either strictly focus on object-free locomotion [Zhao et al., 2025, He et al., 2024, Ji et al., 2025], or rigidly replay recorded HOI trajectories without generalizing to novel configurations [Weng et al., 2025, Zhao et al., 2025] or surviving the sim-to-real gap on physical hardware [Xu et al., 2026a, Tessler et al., 2024]. To date, no framework provides a pathway from scalable video to reference-free loco-manipulation on real hardware. 

We present SUGAR, a data-driven framework that bridges this gap. Our key insight is that imperfect video-extracted data, despite its noise and artifacts, captures coarse but complete task logic, the rough body trajectories, contact events, and object motions that together define what an interaction is trying to accomplish. While too noisy for direct imitation, this data can be progressively refined into physically grounded training signals through simulation, and distilled into an autonomous policy. 

As illustrated in Fig. 2, SUGAR proceeds in three tightly coupled stages. First, a fully automated pipeline reconstructs human motion, 6D object trajectories, and VLM-labeled contact events from unannotated videos to form scalable kinematic priors. Second, a privileged RL policy utilizes a unified mimic-style reward and a novel progressive state pool to transform these coarse kinematic interaction priors into physically feasible and high-fidelity skills. Finally, we distill these skills into a hierarchical policy: a high-level diffusion policy command generator synthesizes movement intent commands, while a low-level whole-body command tracker robustly tracks them. 

We evaluate SUGAR on six representative whole-body loco-manipulation tasks on a Unitree G1 humanoid. Across both training and unseen test configurations, SUGAR substantially outperforms reference-tracking baselines, exhibits favorable scaling with the amount of human video data, and successfully deploys on real hardware with robust closed-loop execution, autonomous failure recovery, and stable long-horizon interaction under external perturbations. In summary, our contributions are: 

- A fully automated pipeline that first extracts coarse kinematic interaction priors from unstructured human videos, and subsequently refines them into physically feasible, high-fidelity skill demonstrations via privileged reinforcement learning. 

- A systematic hierarchical policy training pipeline that converts refined skill demonstrations into a deployable, reference-free autonomous policy. 

- Extensive simulation and real-world experiments validating that our method outperforms strong baselines, generalizes to unseen object configurations, scales naturally with video data, and transfers zero-shot to real hardware with robust closed-loop recovery. 

2 

## **2 Related Work** 

### **2.1 Humanoid-Object Interaction** 

Humanoid-object interaction remains a challenging open problem. Task-specific RL in simulation produces impressive results on tasks such as soccer [Wang et al., 2025c, Su et al., 2025], tennis [Zhang et al., 2026], and door opening [Chen et al., 2024, Xue et al., 2025], but requires per-task reward engineering [Zhuang et al., 2026, Yin et al., 2025]. An alternative line of work collects robot demonstrations through teleoperation and trains autonomous policies from this data [Chen et al., 2026, Ze et al., 2025, Wei et al., 2026, Li et al., 2025b, Ben et al., 2025, Li et al., 2025a, Jiang et al., 2025]. However, it is bottlenecked by human effort and specialized hardware. In the character animation community, retargeting mocap data to humanoid robots and applying imitation-based rewards has enabled robots to acquire diverse locomotion and interaction skills [Xu et al., 2026b, 2025, 2026a, Wang et al., 2023, Tessler et al., 2024, Tevet et al., 2024, Wang et al., 2025b, Yu et al., 2025, Wang et al., 2026b, Mahmood et al., 2019, Lee et al., 2025]. However, deploying these methods on real-world humanoid robots faces substantial challenges [Nai et al., 2026, Weng et al., 2025, Wang et al., 2026a, Yang et al., 2025, Lin et al., 2026, He et al., 2026, Wang et al., 2025a, Fu et al., 2024]: kinematic differences between human and robot embodiments, maintaining physical plausibility during HOI retargeting, and the sim-to-real gap in contact-rich interactions all hinder direct transfer. In this work, SUGAR addresses these challenges by proposing a scalable pipeline for constructing physically grounded HOI data from human videos, combined with a hierarchical policy framework that enables generalizable object interaction on real humanoid hardware. 

### **2.2 Humanoid Learning from Human Videos** 

Recent advances in humanoid robot learning have increasingly turned to human videos as a scalable source of demonstration data. One line of work learns locomotion skills from video demonstrations [He et al., 2025a, Mao et al., 2024, Allshire et al., 2025, Yang et al., 2026a, Xie et al., 2025, Han et al., 2025], successfully transferring walking, running, and acrobatic behaviors to humanoid robots. However, these approaches fundamentally lack object interaction capabilities, as they do not explicitly model object dynamics during training. Another line of work focuses on learning manipulation skills from video [Shi et al., 2026, Gao et al., 2026, Lepert et al., 2025, Shah et al., 2025, Li et al., 2024, Zhu et al., 2025, Heng et al., 2026], but is typically constrained to upper-body or tabletop interactions, failing to exploit the large workspace achievable through whole-body coordination. Recent works [Weng et al., 2025, Zhao et al., 2025] take a step toward unifying locomotion and manipulation by learning whole-body interactions from monocular RGB videos, co-tracking human and object trajectories. Nevertheless, it remains a reference-based approach that replays recorded motions at inference, limiting generalization to novel objects and configurations. Concurrent work HumanX [Wang et al., 2026a] compiles human video into real-world interaction skills, but relies on kinematic motion synthesis with manually defined anchor points rather than learning from large-scale multi-trajectory HOI data. In contrast, our approach automatically extracts and refines HOI data from diverse human videos at scale, and learns generalizable, reference-free interaction policies through a hierarchical architecture. 

## **3 Method** 

### **3.1 Overview** 

We aim to learn an autonomous policy _π_ for humanoid locomanipulation tasks by leveraging human videos as a primary data source. Formally, given the robot proprioception _o_<sup>_R_</sup> _t_<sup>, object observation</sup><sup>_oO_</sup> _t_ (represented as the 6D pose relative to the robot’s root frame), and an optional task goal _g_ (represented as the target object state), the policy _π_ predicts the action _at_ to achieve the task: _at_ = _π_ ( _o_<sup>_R_</sup> _t_<sup>_, oO_</sup> _t_<sup>_, g_),</sup> which is then transformed into joint torques via a PD controller. 

As illustrated in Fig. 2, our approach consists of three core stages designed to bridge the gap between unannotated human videos and robust physical execution: (1) We propose a fully automated pipeline to extract human-object kinematic interaction priors, including motion trajectories and contact labels, from unstructured human videos.(Sec. 3.2) (2) We train a privileged RL policy, refiner, to transform these coarse kinematic interaction priors into physically feasible and high-fidelity skills.(Sec. 3.3) (3) We learn an autonomous policy from the refined demonstrations, distilling the expert knowledge into a robust system capable of both high-level task planning and low-level command tracking.(Sec. 3.4) 

3 


Figure 2: **Overview of SUGAR.** Our approach consists of three stages: (1) extracting kinematic interaction priors from unstructured human videos through a fully automated pipeline; (2) refining the priors into physically feasible skills with a privileged RL policy; and (3) training a hierarchical autonomous policy on the refined demonstrations for robust humanoid locomanipulation. 

### **3.2 Scalable Kinematic Interaction Priors from Human Videos** 

Human videos offer an abundant, low-cost data source for skill acquisition. However, existing methods face constraints in fully exploiting this potential. To address this, we propose a fully automated pipeline to extract kinematic interaction priors dataset _P_ consisting of trajectories and contact labels from raw video, eliminating manual annotation labor. 

**Human-Object Motion Reconstruction** We utilize SAMBody [Yang et al., 2026b, Gao et al., 2025] to extract human motion sequences _p_ ˆ<sup>_R_</sup> 1: _T_<sup>, which are further aligned with the depth observa-</sup> tions and optimized using Iterative Closest Point (ICP) [Besl and McKay, 1992] to ensure spatial accuracy. For objects, we first generate a mesh using SAMObj [Team et al., 2025] and determine its physical scale by aligning the mesh with the captured object point cloud. We then employ FoundationPose [Wen et al., 2024] to estimate the object’s 6D pose trajectories _p_ ˆ<sup>_O_</sup> 1: _T_<sup>.</sup> 

**Automated Interaction Synthesis** To bypass manual annotation when assigning contact labels ˆ _lt_ , we query a VLM [Bai et al., 2025] based on task-specific body parts (e.g., hands for carrying), the prompt will be shown in Appendix B. In tasks where visual cues are ambiguous due to severe occlusion (e.g., kicking box), preventing the VLM from providing reliable per-frame contact signals, we infer contact if the object’s velocity exceeds the threshold. 

Finally, we apply temporal filtering to smooth the trajectories, yielding a comprehensive dataset of kinematic interaction priors dataset _P_ , which serves as a structured reference for subsequent physics-based refinement: 


Each trajectory _τ_ ˆ represents a sequence of reconstructed human-object motions and contact labels extracted from a single video clip. The "hat" notation (ˆ _·_ ) signifies that these priors are derived from purely kinematic estimation and may contain physical inaccuracies. 

### **3.3 Refining Kinematic Interaction Priors into Physically Feasible Skills** 

To bridge the gap between kinematic priors and physical dynamics, we train a privileged referencetracking RL policy, refiner, _πr_ ( _a_<sup>_r_</sup> _t_<sup>_| oR_</sup> _t_<sup>_, oO_</sup> _t_<sup>_, o_</sup> _t_<sup>_priv_</sup> _,_ ˆ _τi_ ) that translates noisy _P_ into physically feasible expert trajectories while maintaining the original task intent, producing a physically feasible refined skill dataset _R_ : 


4 


Figure 3: The Training Pipeline of SUGAR. (Left) The Refiner _πr_ transforms noisy kinematic priors _τ_ ˆ _∈P_ into physically feasible expert demonstrations _τ ∈R_ using privileged RL. (Middle) The Tracker _πt_ distills motor skills from the Refiner via behavior cloning and reinforcement learning to achieve robust command-tracking. (Right) The Generator _πg_ is trained via imitation learning on the rollout dataset _D_ to predict high-level command sequences, enabling autonomous locomanipulation in a hierarchical manner. 

Here, _p_<sup>_R_</sup> _t_<sup>,</sup><sup>_pO_</sup> _t_<sup>, and</sup><sup>_lt_represent the physically consistent robot poses, object poses, and actual contact</sup> states, respectively. To provide a concrete learning target for the subsequent stage, dataset _R_ also includes the expert states _ct_ recorded during successful executions, defined as: 


Specifically, _qt_<sup>cmd</sup> denotes the actual joint positions executed by the refiner, while _v_ t<sup>cmd</sup> and _ω_ t<sup>cmd</sup> are the resulting root linear and angular velocities. These recorded states serve as the reference commands for training the autonomous policy in the next stage. 

**Unified Reward Design** To minimize task-specific engineering, we design a unified mimic reward _r_ = _rtrack_ + _rint_ + _rreg_ , with detailed formulations provided in Appendix A.1. The **tracking reward term** _rtrack_ encourages the robot and object to follow reference trajectories (ˆ _p_<sup>_R_</sup> _t_<sup>_,_ˆ</sup><sup>_pO_</sup> _t_<sup>).Notably, the</sup> robot tracks root-relative poses to isolate reconstruction errors and prevent noisy global drift from degrading motion naturalness. The **interaction reward term** _rint_ enforces physical consistency by utilizing contact labels<sup>ˆ</sup> _lt_ to prevent force-inconsistent motions and penalizing spatial decoupling between robot links and the object. Finally, **regularization term** _rreg_ facilitates sim-to-real transfer by penalizing torque and non-smooth behaviors. 

**Progressive State Pool for Initialization** Standard Reference State Initialization (RSI) often fails in HOI tasks due to kinematic reconstruction errors, such as penetrations and misalignments, which create physically infeasible starting points. To mitigate this, we propose the Progressive State Pool _B_ , which initializes agents from physically-validated states instead of unreliable references from _P_ . During training, _B_ is incrementally populated with successful intermediate states encountered by _πr_ , providing diverse, physically consistent milestones that stabilize learning of complex interactions while preventing overfitting. 

**Interaction Robustness Enhancement** We apply extensive randomizations and perturbations to broaden the state-dynamics coverage. By varying physical properties like mass and friction, and applying random impulses to both the robot and the object, we force the refiner to learn real physical rules instead of finding shortcuts in the simulator. This ensures the policy develops robust interaction habits that work under uncertain conditions. Consequently, the generated expert data is physically sound and stays stable under interference, providing a reliable basis for training. 

### **3.4 Policy Learning from Refined Demonstrations** 

Given the refined skill dataset _R_ , we aim to train a policy capable of autonomous real-world execution. We separate the autonomous policy into two functional components: a Command Generator for task-level intent and a Command Tracker for robust physical execution. 

**Command Tracker** The tracker _πt_ ( _a_<sup>_t_</sup> _t_<sup>_|oR_</sup> _t_<sup>_, oO_</sup> _t_<sup>_, ct_)isdesignedtofollowamovementintent</sup> command _ct_ by predicting joint targets _at_ . During the distillation phase, _ct_ is from the refined dataset _R_ as an expert reference, whereas during autonomous inference, it is actively produced by the command generator _πg_ , as illustrated in Fig. 3. These targets are subsequently converted into joint torques via a PD controller. 

5 

- **Distillation from Refiner.** To efficiently scale _πt_ ’s capability across diverse demonstrations, we distill the expertise from the refiner _πr_ combining Behavior Cloning (BC) and Reinforcement Learning (RL). Specifically, _πt_ first performs BC to rapidly mimic _πr_ ’s motion patterns, providing a structured initialization. This is followed by a transitional phase to warm up the critic and actor of _πt_ , eventually shifting to full RL optimization using the same rewards as in Sec. 3.3. 

- **Evolutionary Initialization.** Leveraging the physically consistent states provided by the _R_ , we first utilize Reference State Initialization (RSI) to ensure a stable start. As training progresses, we shift to sampling from the Progressive State Pool Initialization (PSPI), to broaden the state coverage and prevent over-fitting to single demonstrations. This allows _πt_ to reliably master complex, multi-stage interactions from a stable physical foundation. 

**Task-Guided Command Generator** With the low-level tracker _πt_ frozen, autonomous locomanipulation is reformulated as a conditional sequence generation problem. We implement the high-level task-guided command generator _πg_ ( _ct_ : _t_ +7 _| ot_<sup>_O, ct−_1</sup><sup>_, g_) using a state-based Diffusion</sup> Policy [Chi et al., 2025], which predicts a sequence of future commands to drive the tracker toward task completion. We defer more details into Appendix A.2. 

To bridge the gap between kinematic planning and dynamic execution, we collect a rollout dataset _D_ that reflects the actual performance of the integrated system. Specifically, for each refined trajectory _τ ∈R_ , we drive the frozen tracker _πt_ using the recorded expert states **c** _t_ as reference commands. We then record the actual object states ˜ _o_<sup>_O_</sup> _t_<sup>reached by the tracker during these closed-loop rollouts,</sup> forming the dataset: 


By training on these execution-based data rather than idealized references, the command generator learns to guide the tracker based on the states it encounters. This approach enables the generator to proactively correct execution errors and drift, ensuring reliable task completion over long horizons. 

## **4 Experiment** 

To evaluate the effectiveness of our method, we design a series of experiments to answer the following questions: (1) Performance and Generalization: How does our method perform compared to prior approaches in terms of performance and generalization to unseen initial and target states? (2) Data Scaling: How does the performance of our method improve as the amount of training data increases? (3) Component Analysis: How does each component contribute to our framework? (4) Sim-to-Real Transfer: Can the learned policy be robustly transferred from simulation to real-world deployment? 

### **4.1 Experiment Setup** 

**Tasks.** We evaluate our method on six challenging whole-body loco-manipulation tasks: (1) _Carry Box_ : lift and transport a box to the target location; (2) _Push Box_ : push a box to the target location; (3) _Kick Box_ : kick a box to the target location; (4) _Pick Bottle_ : walk to and lift a bottle from the ground; (5) _Stand Bottle_ : reorient a bottle from lying to upright pose; (6) _Sit Chair_ : move from varied initial positions and stably sit on a chair. 

**Dataset.** For each task, we collect 100 human video demonstrations for training and 30 for testing. By leveraging human videos rather than robot teleoperation, data collection remains efficient and low-cost. Our pipeline then automatically processes these videos into training-ready data. 

**Evaluation Metrics.** We use the following metrics: (1) _Success Rate_ : the percentage of successful trials. A trial is considered successful based on task-specific criteria. For _Carry Box_ , _Push Box_ , and _Kick Box_ , success is defined as the final object position being within a predefined threshold of the target location. For _Sit Chair_ , success requires the robot base to maintain stable contact with the chair for a certain duration. For _Stand Bottle_ , success is achieved when the bottle is stably placed in an upright position on the ground. For _Pick Bottle_ , success is defined as lifting the bottle above a predefined height. (2) _Final Object Position Error_ : the Euclidean distance between the final object position and the target location for tasks involving target placement. 

**Baselines.** We compare our method with two representative methods, _Resmimic_ [Zhao et al., 2025] and _HDMI_ [Weng et al., 2025]. These baselines represent strong prior methods based on reference trajectory replay. All methods are trained and evaluated under the same dataset. 

6 

Table 1: **Main results in simulation.** We evaluate two baselines, ablated variants, and SUGAR on six whole-body loco-manipulation tasks in simulation. The two baselines additionally require reference demonstration trajectory observations, whereas SUGAR takes only an optional goal object state _g_ as input . All methods are trained and evaluated on the same training and test datasets. 

|**Method**|**Kick**<br>|**Box**<br>|**Push**<br>|**Box**<br>|**Carr**<br>|**y Box**<br>|**Sit Chair**<br>|**Pick Bottle**<br>|**Stand Bottle**<br>|
|---|---|---|---|---|---|---|---|---|---|
||SR_↑_|Err_↓_|SR_↑_|Err_↓_|SR_↑_|Err_↓_|SR_↑_|SR_↑_|SR_↑_|
|||||**Tra**|**ining**|**Dataset**||||
|**Resmimic**|21.6|0.912|16.5|1.021|0.0|_−_|23.2|0.0|0.0|
|**HDMI**|82.4|0.263|**94.1**|**0.162**|0.0|_−_|31.9|0.0|0.0|
|w/o refiner|48.3|0.419|56.5|0.464|66.8|0.429|93.4|97.5|79.0|
|w/o PSPI (SSI)|80.9|0.251|78.5|0.272|81.3|0.303|95.0|98.2|89.6|
|w/o PSPI (RSI)|85.9|0.241|83.9|0.272|68.9|0.483|**96.7**|94.3|86.2|
|w/o IR|80.4|0.254|85.5|0.264|73.8|0.390|96.0|0.0|85.0|
|w/o IRE|86.4|0.237|72.4|0.328|67.7|0.388|92.8|97.0|59.4|
|**Ours**|**89.5**|**0.222**|83.6|0.261|**84.5**|**0.280**|94.8|**98.8**|**91.9**|
||||||**Test Da**|**taset**||||
|**Resmimic**|18.5|0.963|10.6|1.160|0.0|_−_|20.6|0.0|0.0|
|**HDMI**|17.3|0.938|54.6|0.377|0.0|_−_|8.2|0.0|0.0|
|w/o refiner|46.3|0.414|41.7|0.554|62.0|0.424|99.0|96.7|79.0|
|w/o PSPI (SSI)|61.7|0.316|71.0|0.328|63.3|0.337|98.0|94.9|84.3|
|w/o PSPI (RSI)|71.4|0.269|**73.0**|0.345|62.0|0.557|98.3|94.2|79.6|
|w/o IR|**76.3**|**0.260**|63.4|0.338|60.3|0.513|97.6|0.0|73.1|
|w/o IRE|72.0|0.298|47.2|0.421|57.5|0.436|98.9|98.0|63.4|
|**Ours**|76.0|0.265|70.0|**0.325**|**69.6**|**0.326**|**99.6**|**99.2**|**86.3**|


(a) 20 trajectories, 31.6% success rate (b) 50 trajectories, 66.0% success rate (c) 100 trajectories, 86.4% success rate 


Figure 4: **Performance with different training data sizes.** Success rates, evaluated on both the train and test datasets, consistently improve as the amount of training data increases. 

### **4.2 Comparison with Baselines** 

We compare our method with baseline methods on six whole-body loco-manipulation tasks. Table 1 shows our method outperforms the baselines on all tasks in both success rate and final object position error. The performance gap is most evident in high-precision tasks like _Carry Box_ , _Pick Bottle_ , and _Stand Bottle_ . While baseline methods fail to learn effective skills from coarse, noisy dataset, our approach consistently extracts reusable skills and achieves significantly higher success rates. 

### **4.3 Performance scaling with data size** 

To analyze performance scaling, we train our model using 20, 50, and 100 trajectories per task. As shown in Table 2 and Fig 4, our method exhibits a strong scaling trend, where success rates improve consistently as the data volume increases. The improvement with more data is primarily due to increased coverage of state-action space. This suggests that our architecture can inherently capture more robust and generalizable behaviors from larger datasets without requiring additional task-specific rewards or robustness engineering. Such scalability highlights the potential of our approach to benefit from large-scale noisy human data in complex scenarios. 

7 

Table 2: **Simulation results under different training data sizes.** We evaluate SUGAR on six whole-body loco-manipulation tasks using 20, 50, and 100 training trajectories per task. Success rates improve consistently as the amount of training data increases. 

|**Method**|**Kick**|**Box**|**Push**|**Box**|**Carr**|**y Box**|**Sit Chair**|**Pick Bottle**|**Stand Bottle**|
|---|---|---|---|---|---|---|---|---|---|
||SR_↑_|Err_↓_|SR_↑_|Err_↓_|SR_↑_|Err_↓_|SR_↑_|SR_↑_|SR_↑_|
||||||**Traini**|**ng Datase**|**t**|||
|20|31.3|0.518|37.1|0.634|38.5|0.675|74.9|95.6|76.4|
|50|66.9|0.330|30.1|0.504|72.3|0.367|89.6|97.7|78.9|
|100|**89.5**|**0.222**|**83.6**|**0.261**|**84.5**|**0.280**|**94.8**|**98.8**|**91.9**|
||||||**Test**|**Dataset**||||
|20|32.7|0.416|35.0|0.593|33.5|0.682|90.0|94.2|66.4|
|50|63.1|0.336|52.3|0.527|61.0|0.403|98.9|95.3|75.3|
|100|**76.0**|**0.265**|**70.0**|**0.325**|**69.6**|**0.326**|**99.6**|**99.2**|**86.3**|


Figure 5: **Qualitative results:** **_Carry Box_ .** (a) Our method stably lifts the box. (b) Without interaction rewards (w/o IR), the policy only imitates the bending motion and fails to lift the box (c) Without interaction robustness enhancement (w/o IRE), the interaction is less robust and causes failure. 

### **4.4 Component Analysis** 

We conduct ablation studies to evaluate the contribution of key components in our framework. 

**Refinement Policy (w/o Refiner):** Removing the Refiner leads to substantial performance degradation, as shown in Table 1, proving that physical consistency is crucial when learning from noisy video data. This result highlights that the Refiner transforms coarse motion priors into physically valid and dynamically consistent demonstrations, enables stable and effective learning. 

**Progressive State Pool (w/o PSPI):** We analyze the impact of the Progressive State Pool for Initialization by replacing it with two alternatives: (1) _Start State Initialization (SSI)_ , where training always initializes from start phase; and (2) _Reference State Initialization (RSI)_ , where initial states are sampled from raw kinematic trajectories. Both variants lead to noticeable performance degradation (Table 1). In contrast, the Progressive State Pool provides diverse and physically consistent initialization states, enabling stable training and effective skill acquisition across different stages. 

**Interaction Rewards (w/o IR):** Quantitative and qualitative results (Table. 1 and Fig. 5) show removing interaction rewards leads to failure in contact-rich tasks like _Carry Box_ and _Pick Bottle_ , as kinematic tracking alone fails to enforce essential physical constraints. 

**Interaction Robustness Enhancement (w/o IRE):** As also illustrated in Table. 1 and Fig. 5, removing Interaction Robustness Enhancement causes severe overfitting to idealized physics, incorporating it forces the model to learn physical compensation, significantly improving robustness against external disturbances and varying physical properties. 

### **4.5 Real-World Evaluation** 

We deploy our policy on a real humanoid robot using MoCap, transferring the purely simulationtrained model to the real world. We evaluate each task over 10 trials and summarize the success rates in Table 3. In real-world experiments, the learned policy demonstrates robust closed-loop execution under noisy perception and dynamical discrepancies, enabling the robot to continuously perform tasks over extended horizons while maintaining consistent task progress. 

8 

Table 3: **Real-world success rates.** We evaluate SUGAR on six whole-body loco-manipulation tasks in the real world. Success rates are reported as successful attempts out of 10 trials. 


Figure 8: **Zero-shot generalization to different objects in the real world.** 

A key observation is the policy’s robustness in real-world execution. As shown in Fig. 6, when execution is disrupted, such as by object displacement or partial task failure, the robot can autonomously resume the task rather than terminating, indicating the ability to handle out-of-distribution states. As illustrated in Fig. 7, the robot also remains stable under external disturbances and continues execution without losing control. Moreover, Fig. 8 shows that the learned policy generalizes zero-shot to objects with different shapes, sizes, and appearances without finetuning, suggesting that it captures transferable interaction strategies instead of overfitting to a specific object instance. 

## **5 Conclusion** 

In this work, we introduced SUGAR, a data-driven learning framework that successfully unlocks generalizable humanoid loco-manipulation skills from diverse, unconstrained human videos. To address the physical implausibility and artifacts inherent in video-derived motion priors, we implement a robust three-stage pipeline: automated kinematic interaction prior extraction, privileged physicsbased refinement via a unified reward, and hierarchical policy distillation. Our extensive evaluations on the Unitree G1 demonstrate that SUGAR scales robustly with data volume, successfully transfers to the real world, and maintains successful task completion under external disturbances, providing a scalable path for learning from human videos. 

9 

## **References** 

- Arthur Allshire, Hongsuk Choi, Junyi Zhang, David McAllister, Anthony Zhang, Chung Min Kim, Trevor Darrell, Pieter Abbeel, Jitendra Malik, and Angjoo Kanazawa. Visual imitation enables contextual humanoid control, 2025. URL `https://arxiv.org/abs/2505.03729` . 

- Shuai Bai, Yuxuan Cai, Ruizhe Chen, Keqin Chen, Xionghui Chen, Zesen Cheng, Lianghao Deng, Wei Ding, Chang Gao, Chunjiang Ge, Wenbin Ge, Zhifang Guo, Qidong Huang, Jie Huang, Fei Huang, Binyuan Hui, Shutong Jiang, Zhaohai Li, Mingsheng Li, Mei Li, Kaixin Li, Zicheng Lin, Junyang Lin, Xuejing Liu, Jiawei Liu, Chenglong Liu, Yang Liu, Dayiheng Liu, Shixuan Liu, Dunjie Lu, Ruilin Luo, Chenxu Lv, Rui Men, Lingchen Meng, Xuancheng Ren, Xingzhang Ren, Sibo Song, Yuchong Sun, Jun Tang, Jianhong Tu, Jianqiang Wan, Peng Wang, Pengfei Wang, Qiuyue Wang, Yuxuan Wang, Tianbao Xie, Yiheng Xu, Haiyang Xu, Jin Xu, Zhibo Yang, Mingkun Yang, Jianxin Yang, An Yang, Bowen Yu, Fei Zhang, Hang Zhang, Xi Zhang, Bo Zheng, Humen Zhong, Jingren Zhou, Fan Zhou, Jing Zhou, Yuanzhi Zhu, and Ke Zhu. Qwen3-vl technical report. _arXiv preprint arXiv:2511.21631_ , 2025. 

- Qingwei Ben, Feiyu Jia, Jia Zeng, Junting Dong, Dahua Lin, and Jiangmiao Pang. Homie: Humanoid loco-manipulation with isomorphic exoskeleton cockpit, 2025. URL `https://arxiv.org/abs/ 2502.13013` . 

- Paul J Besl and Neil D McKay. Method for registration of 3-d shapes. In _Sensor fusion IV: control paradigms and data structures_ , volume 1611, pages 586–606. Spie, 1992. 

- Yue Chen, Chenrui Tie, Ruihai Wu, and Hao Dong. Eqvafford: Se(3) equivariance for point-level affordance learning, 2024. URL `https://arxiv.org/abs/2408.01953` . 

- Yue Chen, Muqing Jiang, Kaifeng Zheng, Jiaqi Liang, Chenrui Tie, Haoran Lu, Ruihai Wu, and Hao Dong. Learning part-aware dense 3d feature field for generalizable articulated object manipulation, 2026. URL `https://arxiv.org/abs/2602.14193` . 

- Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , 44(10-11):1684–1704, 2025. 

- Zipeng Fu, Qingqing Zhao, Qi Wu, Gordon Wetzstein, and Chelsea Finn. Humanplus: Humanoid shadowing and imitation from humans, 2024. URL `https://arxiv.org/abs/2406.10454` . 

- Mingqi Gao, Yunqi Miao, and Jungong Han. Sam-body4d: Training-free 4d human body mesh recovery from videos. _arXiv preprint arXiv:2512.08406_ , 2025. URL `https://arxiv.org/abs/ 2512.08406` . 

- Shenyuan Gao, William Liang, Kaiyuan Zheng, Ayaan Malik, Seonghyeon Ye, Sihyun Yu, WeiCheng Tseng, Yuzhu Dong, Kaichun Mo, Chen-Hsuan Lin, Qianli Ma, Seungjun Nah, Loic Magne, Jiannan Xiang, Yuqi Xie, Ruijie Zheng, Dantong Niu, You Liang Tan, K. R. Zentner, George Kurian, Suneel Indupuru, Pooya Jannaty, Jinwei Gu, Jun Zhang, Jitendra Malik, Pieter Abbeel, Ming-Yu Liu, Yuke Zhu, Joel Jang, and Linxi "Jim" Fan. Dreamdojo: A generalist robot world model from large-scale human videos, 2026. URL `https://arxiv.org/abs/2602.06949` . 

- Jinrui Han, Weiji Xie, Jiakun Zheng, Jiyuan Shi, Weinan Zhang, Ting Xiao, and Chenjia Bai. Kungfubot2: Learning versatile motion skills for humanoid whole-body control. _arXiv preprint arXiv:2509.16638_ , 2025. 

- Tairan He, Zhengyi Luo, Wenli Xiao, Chong Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. Learning human-to-humanoid real-time whole-body teleoperation, 2024. URL `https://arxiv. org/abs/2403.04436` . 

- Tairan He, Jiawei Gao, Wenli Xiao, Yuanhang Zhang, Zi Wang, Jiashun Wang, Zhengyi Luo, Guanqi He, Nikhil Sobanbab, Chaoyi Pan, Zeji Yi, Guannan Qu, Kris Kitani, Jessica Hodgins, Linxi "Jim" Fan, Yuke Zhu, Changliu Liu, and Guanya Shi. Asap: Aligning simulation and real-world physics for learning agile humanoid whole-body skills, 2025a. URL `https://arxiv.org/abs/2502. 01143` . 

10 

- Tairan He, Zi Wang, Haoru Xue, Qingwei Ben, Zhengyi Luo, Wenli Xiao, Ye Yuan, Xingye Da, Fernando Castañeda, Shankar Sastry, Changliu Liu, Guanya Shi, Linxi Fan, and Yuke Zhu. Viral: Visual sim-to-real at scale for humanoid loco-manipulation, 2025b. URL `https://arxiv.org/ abs/2511.15200` . 

- Xialin He, Sirui Xu, Xinyao Li, Runpei Dong, Liuyu Bian, Yu-Xiong Wang, and Liang-Yan Gui. Ultra: Unified multimodal control for autonomous humanoid whole-body loco-manipulation. _arXiv preprint arXiv:2603.03279_ , 2026. 

- Liang Heng, Yihe Tang, Jiajun Xu, Henghui Bao, Di Huang, and Yue Wang. Humdex: Humanoid dexterous manipulation made easy, 2026. URL `https://arxiv.org/abs/2603.12260` . 

- Mazeyu Ji, Xuanbin Peng, Fangchen Liu, Jialong Li, Ge Yang, Xuxin Cheng, and Xiaolong Wang. Exbody2: Advanced expressive humanoid whole-body control, 2025. URL `https://arxiv. org/abs/2412.13196` . 

- Haoran Jiang, Jin Chen, Qingwen Bu, Li Chen, Modi Shi, Yanjie Zhang, Delong Li, Chuanzhe Suo, Chuang Wang, Zhihui Peng, and Hongyang Li. Wholebodyvla: Towards unified latent vla for whole-body loco-manipulation control. _arXiv preprint arXiv:2512.11047_ , 2025. 

- Kyungmin Lee, Sibeen Kim, Minho Park, Hyunseung Kim, Dongyoon Hwang, Hojoon Lee, and Jaegul Choo. Phuma: Physically-grounded humanoid locomotion dataset, 2025. URL `https: //arxiv.org/abs/2510.26236` . 

- Marion Lepert, Jiaying Fang, and Jeannette Bohg. Masquerade: Learning from in-the-wild human videos using data-editing, 2025. URL `https://arxiv.org/abs/2508.09976` . 

- Jialong Li, Xuxin Cheng, Tianshu Huang, Shiqi Yang, Ri-Zhao Qiu, and Xiaolong Wang. Amo: Adaptive motion optimization for hyper-dexterous humanoid whole-body control, 2025a. URL `https://arxiv.org/abs/2505.03738` . 

- Jinhan Li, Yifeng Zhu, Yuqi Xie, Zhenyu Jiang, Mingyo Seo, Georgios Pavlakos, and Yuke Zhu. Okami: Teaching humanoid robots manipulation skills through single video imitation, 2024. URL `https://arxiv.org/abs/2410.11792` . 

- Yixuan Li, Yutang Lin, Jieming Cui, Tengyu Liu, Wei Liang, Yixin Zhu, and Siyuan Huang. Clone: Closed-loop whole-body humanoid teleoperation for long-horizon tasks, 2025b. URL `https: //arxiv.org/abs/2506.08931` . 

- Yutang Lin, Jieming Cui, Yixuan Li, Baoxiong Jia, Yixin Zhu, and Siyuan Huang. Lessmimic: Long-horizon humanoid interaction with unified distance field representations. _arXiv preprint arXiv:2602.21723_ , 2026. 

- Minghuan Liu, Zixuan Chen, Xuxin Cheng, Yandong Ji, Ri-Zhao Qiu, Ruihan Yang, and Xiaolong Wang. Visual whole-body control for legged loco-manipulation, 2024. URL `https://arxiv. org/abs/2403.16967` . 

- Zhengyi Luo, Ye Yuan, Tingwu Wang, Chenran Li, Sirui Chen, Fernando Castañeda, Zi-Ang Cao, Jiefeng Li, David Minor, Qingwei Ben, Xingye Da, Runyu Ding, Cyrus Hogg, Lina Song, Edy Lim, Eugene Jeong, Tairan He, Haoru Xue, Wenli Xiao, Zi Wang, Simon Yuen, Jan Kautz, Yan Chang, Umar Iqbal, Linxi "Jim" Fan, and Yuke Zhu. Sonic: Supersizing motion tracking for natural humanoid whole-body control, 2025. URL `https://arxiv.org/abs/2511.07820` . 

- Naureen Mahmood, Nima Ghorbani, Nikolaus F. Troje, Gerard Pons-Moll, and Michael J. Black. Amass: Archive of motion capture as surface shapes, 2019. URL `https://arxiv.org/abs/ 1904.03278` . 

- Jiageng Mao, Siheng Zhao, Siqi Song, Tianheng Shi, Junjie Ye, Mingtong Zhang, Haoran Geng, Jitendra Malik, Vitor Guizilini, and Yue Wang. Learning from massive human videos for universal humanoid pose control, 2024. URL `https://arxiv.org/abs/2412.14172` . 

- Ruiqian Nai, Boyuan Zheng, Junming Zhao, Haodong Zhu, Sicong Dai, Zunhao Chen, Yihang Hu, Yingdong Hu, Tong Zhang, Chuan Wen, and Yang Gao. Humanoid manipulation interface: Humanoid whole-body manipulation from robot-free demonstrations, 2026. URL `https:// arxiv.org/abs/2602.06643` . 

11 

- John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- Rutav Shah, Shuijing Liu, Qi Wang, Zhenyu Jiang, Sateesh Kumar, Mingyo Seo, Roberto MartínMartín, and Yuke Zhu. Mimicdroid: In-context learning for humanoid robot manipulation from human play videos, 2025. URL `https://arxiv.org/abs/2509.09769` . 

- Modi Shi, Shijia Peng, Jin Chen, Haoran Jiang, Yinghui Li, Di Huang, Ping Luo, Hongyang Li, and Li Chen. Egohumanoid: Unlocking in-the-wild loco-manipulation with robot-free egocentric demonstration, 2026. URL `https://arxiv.org/abs/2602.10106` . 

- Zhi Su, Yuman Gao, Emily Lukas, Yunfei Li, Jiaze Cai, Faris Tulbah, Fei Gao, Chao Yu, Zhongyu Li, Yi Wu, and Koushil Sreenath. Toward real-world cooperative and competitive soccer with quadrupedal robot teams, 2025. URL `https://arxiv.org/abs/2505.13834` . 

- SAM 3D Team, Xingyu Chen, Fu-Jen Chu, Pierre Gleize, Kevin J Liang, Alexander Sax, Hao Tang, Weiyao Wang, Michelle Guo, Thibaut Hardin, Xiang Li, Aohan Lin, Jiawei Liu, Ziqi Ma, Anushka Sagar, Bowen Song, Xiaodong Wang, Jianing Yang, Bowen Zhang, Piotr Dollár, Georgia Gkioxari, Matt Feiszli, and Jitendra Malik. Sam 3d: 3dfy anything in images. _arXiv preprint arXiv:2511.16624_ , 2025. URL `https://arxiv.org/abs/2511.16624` . 

- Chen Tessler, Yunrong Guo, Ofir Nabati, Gal Chechik, and Xue Bin Peng. Maskedmimic: Unified physics-based character control through masked motion inpainting, 2024. URL `https://arxiv. org/abs/2409.14393` . 

- Guy Tevet, Sigal Raab, Setareh Cohan, Daniele Reda, Zhengyi Luo, Xue Bin Peng, Amit H. Bermano, and Michiel van de Panne. Closd: Closing the loop between simulation and diffusion for multi-task character control, 2024. URL `https://arxiv.org/abs/2410.03441` . 

- Huayi Wang, Wentao Zhang, Runyi Yu, Tao Huang, Junli Ren, Feiyu Jia, Zirui Wang, Xiaojie Niu, Xiao Chen, Jiahe Chen, Qifeng Chen, Jingbo Wang, and Jiangmiao Pang. Physhsi: Towards a real-world generalizable and natural humanoid-scene interaction system, 2025a. URL `https: //arxiv.org/abs/2510.11072` . 

- Yinhuai Wang, Jing Lin, Ailing Zeng, Zhengyi Luo, Jian Zhang, and Lei Zhang. Physhoi: Physicsbased imitation of dynamic human-object interaction, 2023. URL `https://arxiv.org/abs/ 2312.04393` . 

- Yinhuai Wang, Qihan Zhao, Runyi Yu, Hok Wai Tsui, Ailing Zeng, Jing Lin, Zhengyi Luo, Jiwen Yu, Xiu Li, Qifeng Chen, Jian Zhang, Lei Zhang, and Ping Tan. Skillmimic: Learning basketball interaction skills from demonstrations. In _Proceedings of the Computer Vision and Pattern Recognition Conference (CVPR)_ , pages 17540–17549, June 2025b. 

- Yinhuai Wang, Qihan Zhao, Yuen Fui Lau, Runyi Yu, Hok Wai Tsui, Qifeng Chen, Jingbo Wang, Jiangmiao Pang, and Ping Tan. Humanx: Toward agile and generalizable humanoid interaction skills from human videos, 2026a. URL `https://arxiv.org/abs/2602.02473` . 

- Yunshen Wang, Shaohang Zhu, Peiyuan Zhi, Yuhan Li, Jiaxin Li, Yong-Lu Li, Yuchen Xiao, Xingxing Wang, Baoxiong Jia, and Siyuan Huang. Omnixtreme: Breaking the generality barrier in highdynamic humanoid control, 2026b. URL `https://arxiv.org/abs/2602.23843` . 

- Yushi Wang, Changsheng Luo, Penghui Chen, Jianran Liu, Weijian Sun, Tong Guo, Kechang Yang, Biao Hu, Yangang Zhang, and Mingguo Zhao. Learning vision-driven reactive soccer skills for humanoid robots, 2025c. URL `https://arxiv.org/abs/2511.03996` . 

- Songlin Wei, Hongyi Jing, Boqian Li, Zhenyu Zhao, Jiageng Mao, Zhenhao Ni, Sicheng He, Jie Liu, Xiawei Liu, Kaidi Kang, Sheng Zang, Weiduo Yuan, Marco Pavone, Di Huang, and Yue Wang. _ψ_ 0: An open foundation model towards universal humanoid loco-manipulation, 2026. URL `https://arxiv.org/abs/2603.12263` . 

- Bowen Wen, Wei Yang, Jan Kautz, and Stan Birchfield. FoundationPose: Unified 6d pose estimation and tracking of novel objects. In _CVPR_ , 2024. 

12 

- Haoyang Weng, Yitang Li, Nikhil Sobanbabu, Zihan Wang, Zhengyi Luo, Tairan He, Deva Ramanan, and Guanya Shi. Hdmi: Learning interactive humanoid whole-body control from human videos, 2025. URL `https://arxiv.org/abs/2509.16757` . 

- Weiji Xie, Jinrui Han, Jiakun Zheng, Huanyu Li, Xinzhe Liu, Jiyuan Shi, Weinan Zhang, Chenjia Bai, and Xuelong Li. Kungfubot: Physics-based humanoid whole-body control for learning highly-dynamic skills. _Advances in Neural Information Processing Systems_ , 2025. 

- Sirui Xu, Dongting Li, Yucheng Zhang, Xiyan Xu, Qi Long, Ziyin Wang, Yunzhi Lu, Shuchang Dong, Hezi Jiang, Akshat Gupta, Yu-Xiong Wang, and Liang-Yan Gui. Interact: Advancing large-scale versatile 3d human-object interaction generation. In _CVPR_ , 2025. 

- Sirui Xu, Hung Yu Ling, Yu-Xiong Wang, and Liang-Yan Gui. Intermimic: Towards universal whole-body control for physics-based human-object interactions, 2026a. URL `https://arxiv. org/abs/2502.20390` . 

- Sirui Xu, Samuel Schulter, Morteza Ziyadi, Xialin He, Xiaohan Fei, Yu-Xiong Wang, and Liangyan Gui. Interprior: Scaling generative control for physics-based human-object interactions. _arXiv preprint arXiv:2602.06035_ , 2026b. 

- Haoru Xue, Tairan He, Zi Wang, Qingwei Ben, Wenli Xiao, Zhengyi Luo, Xingye Da, Fernando Castañeda, Guanya Shi, Shankar Sastry, Linxi "Jim" Fan, and Yuke Zhu. Opening the sim-to-real door for humanoid pixel-to-action policy transfer, 2025. URL `https://arxiv.org/abs/2512. 01061` . 

- Haoran Yang, Jiacheng Bao, Yucheng Xin, Haoming Song, Yuyang Tian, Bin Zhao, Dong Wang, and Xuelong Li. Zerowbc: Learning natural visuomotor humanoid control directly from human egocentric video, 2026a. URL `https://arxiv.org/abs/2603.09170` . 

- Lujie Yang, Xiaoyu Huang, Zhen Wu, Angjoo Kanazawa, Pieter Abbeel, Carmelo Sferrazza, C. Karen Liu, Rocky Duan, and Guanya Shi. Omniretarget: Interaction-preserving data generation for humanoid whole-body loco-manipulation and scene interaction, 2025. URL `https://arxiv. org/abs/2509.26633` . 

- Xitong Yang, Devansh Kukreja, Don Pinkus, Anushka Sagar, Taosha Fan, Jinhyung Park, Soyong Shin, Jinkun Cao, Jiawei Liu, Nicolas Ugrinovic, Matt Feiszli, Jitendra Malik, Piotr Dollar, and Kris Kitani. Sam 3d body: Robust full-body human mesh recovery. _arXiv preprint arXiv:2602.15989_ , 2026b. 

- Shaofeng Yin, Yanjie Ze, Hong-Xing Yu, C. Karen Liu, and Jiajun Wu. Visualmimic: Visual humanoid loco-manipulation via motion tracking and generation. _arXiv preprint arXiv:2509.20322_ , 2025. 

- Runyi Yu, Yinhuai Wang, Qihan Zhao, Hok Wai Tsui, Jingbo Wang, Ping Tan, and Qifeng Chen. Skillmimic-v2: Learning robust and generalizable interaction skills from sparse and noisy demonstrations, 2025. 

- Yanjie Ze, Siheng Zhao, Weizhuo Wang, Angjoo Kanazawa, Rocky Duan, Pieter Abbeel, Guanya Shi, Jiajun Wu, and C. Karen Liu. Twist2: Scalable, portable, and holistic humanoid data collection system, 2025. URL `https://arxiv.org/abs/2511.02832` . 

- Zhikai Zhang, Haofei Lu, Yunrui Lian, Ziqing Chen, Yun Liu, Chenghuai Lin, Han Xue, Zicheng Zeng, Zekun Qi, Shaolin Zheng, Qing Luan, Jingbo Wang, Junliang Xing, He Wang, and Li Yi. Learning athletic humanoid tennis skills from imperfect human motion data, 2026. URL `https: //arxiv.org/abs/2603.12686` . 

- Siheng Zhao, Yanjie Ze, Yue Wang, C. Karen Liu, Pieter Abbeel, Guanya Shi, and Rocky Duan. Resmimic: From general motion tracking to humanoid whole-body loco-manipulation via residual learning, 2025. URL `https://arxiv.org/abs/2510.05070` . 

- Yifan Zhong, Xuchuan Huang, Ruochong Li, Ceyao Zhang, Zhang Chen, Tianrui Guan, Fanlian Zeng, Ka Num Lui, Yuyao Ye, Yitao Liang, Yaodong Yang, and Yuanpei Chen. Dexgraspvla: A vision-language-action framework towards general dexterous grasping, 2025. URL `https: //arxiv.org/abs/2502.20900` . 

13 

- Yifeng Zhu, Arisrei Lim, Peter Stone, and Yuke Zhu. Vision-based manipulation from single human video with open-world object graphs, 2025. URL `https://arxiv.org/abs/2405.20321` . 

- Ziwen Zhuang, Shaoting Zhu, Mengjie Zhao, and Hang Zhao. Deep whole-body parkour, 2026. URL `https://arxiv.org/abs/2601.07701` . 

14 

## **A Algorithm Design** 

### **A.1 Implementation of RL-based Policies: Refiner and Tracker** 

**PPO Hyperparameters** Both the Refiner ( _πr_ ) and the Command Tracker ( _πt_ ) are implemented as a three-layer MLP, optimized by PPO [Schulman et al., 2017]. The detailed hyperparameters for the PPO algorithm, including network dimensions, learning rates, and clip parameters, are summarized in Table 4. 

Table 4: PPO Learning Hyperparameters 

|**Hyperparameter**|**Value**|
|---|---|
|Actor MLP network|[512, 256, 128]|
|Critic MLP network|[512, 256, 128]|
|Activation function|ELU|
|Initial noise std (Refiner)|1.0|
|Initial noise std (Tracker)|0.5|
|Training iterations|30,000|
|Number of envs|4096|
|Steps per env|24|
|Number of mini-batches|4|
|Number of learning epochs|5|
|Learning rate|1e-3|
|Desired KL divergence|0.01|
|Discount factor (_γ_)|0.99|
|GAE parameter (_λ_)|0.95|
|PPO clip parameter|0.2|
|Entropy coefficient|0.005|
|Value loss coefficient|1.0|
|Max gradient norm|1.0|


**Observation Spaces** We adopt an **asymmetric actor-critic** training scheme. The Refiner (both actor and critic) and the Tracker’s critic have access to **privileged observations** shown in Table 6. In contrast, the Tracker’s actor only utilizes **deployable observations** shown in Table 5 to ensure a seamless sim-to-real transition. Notably, all robot body poses and object poses are expressed in the robot’s root-relative coordinate frame to maintain translation invariance. 

Table 5: Deployable Observations (Used by Tracker’s Actor) 

|**Observation Item**|**Dim.**|
|---|---|
|History root angular velocity|3_×_5|
|History root joint position|29_×_5|
|History root joint velocity|29_×_5|
|History action|29_×_5|
|History root projected gravity|3_×_5|
|Object position|3|
|Object orientation|6|
|Command joint position|29|
|Command root linear velocity|3|
|Command root angular velocity|3|
|Command contact label|1|


**Reward Function** The reward function _r_ = _rtrack_ + _rint_ + _rreg_ balances imitation accuracy and physical feasibility. As detailed in Table 7: 

**Domain Randomization** To make the policies robust against environmental uncertainty, we apply extensive Domain Randomization, as shown in Table 8. By varying physical properties and applying 

15 

Table 6: Privileged Observations (Used by Refiner’s Actor/Critic and Tracker’s Critic) 

|**Observation Item**|**Dim.**|
|---|---|
|Body position|14_×_3|
|Body orientation|14_×_6|
|Root linear velocity|3|
|Root angular velocity|3|
|Joint position|29|
|Joint velocity|29|
|Last action|29|
|Object position|3|
|Object orientation|6|
|Object linear velocity|3|
|Object angular velocity|3|
|Future reference joint position|29_×_5|
|Future reference joint velocity|29_×_5|
|Future reference root position|3_×_5|
|Future reference root orientation|6_×_5|
|Future reference object position|3_×_5|
|Future reference object orientation|6_×_5|
|Future reference object linear velocity|3_×_5|
|Future reference object angular velocity|3_×_5|


random impulses to both the robot and the object, we force the policies to learn real physical rules instead of exploiting simulator shortcuts. Notably, impulses on the object are only applied when active contact between the robot and the object is detected, ensuring the policies learn to maintain stable manipulation under dynamic disturbances. 

**Early Termination** We define several early termination terms shown in Table 9 to reset the environment when the robot deviates excessively from the reference motion or the target task, preventing the policy from exploring unrecoverable states. 

### **A.2 Implementation of IL-based Policies: Command Generator** 

The Command Generator Φ _θ_ is implemented as a 12-block Diffusion Transformer (DiT) to model the trajectory distribution [Zhong et al., 2025, Chen et al., 2026]. The object state, previous command, and optional target pose are embedded via individual MLPs, which are then concatenated to form the global condition feature _Fcond_ . Then the DiT backbone processes the noisy input _xt_ at timestep _t_ conditioned on _Fcond_ to predict the noise residual ˆ _ϵ_ . 

During joint hierarchical inference, the Generator predicts a chunk of _H_ = 8 steps. To balance reactivity and smoothness, we only execute the first _Aa_ = 4 steps before re-planning. The outputs of the Generator are linearly interpolated to 50 Hz to align with the control frequency of the Tracker. 

## **B VLM-based Contact Detection Template** 

To ensure consistency across diverse scenarios, we use a unified prompt template for all tasks. The `[BODY_PART]` and `[OBJECT]` are specified by the task definition. This approach allows the VLM to focus on the essential physical contact required for each task type without manual intervention. 

_Task: Determine whether the_ _`[BODY_PART]` is in DIRECT PHYSICAL CONTACT with the_ _`[OBJECT]` ._ 

_Answer ’Yes’ ONLY if the_ _`[BODY_PART]` is actually contacting with the_ _`[OBJECT]` . Answer ’No’ if the_ _`[BODY_PART]` is moving toward but not touching, or if a visible gap exists._ 

_Important: Do NOT infer based on intention; Do NOT predict future contact; Only judge only on actual physical contact._ 

_Output: [Yes/No]_ 

16 

Table 7: Detailed Reward Terms and Hyperparameters. Here, _e_ denotes the error between the current state and the reference prior, _q_ represents joint positions, _τ_ is the motor torque, and _a_ is the policy action. I( _·_ ) is the indicator function. 

|**Category**|**Reward Term**|**Weight**|**Expression**|
|---|---|---|---|
|**Tracking**|Joint Position|0.125|exp(_−∥e∥_<sup>2</sup>_/_0_._6<sup>2</sup>)<br>|
||Global Root Position|0.25|exp(_−∥e∥_<sup>2</sup>_/_0_._3<sup>2</sup>)<br>|
||Global Root Orientation|0.25|exp(_−∥e∥_<sup>2</sup>_/_0_._4<sup>2</sup>)<br>|
||Relative Body Position|0.25|exp(_−∥e∥_<sup>2</sup>_/_0_._3<sup>2</sup>)<br>|
||Relative Body Orientation|0.25|exp(_−∥e∥_<sup>2</sup>_/_0_._4<sup>2</sup>)|
||Body Linear Velocity|0.25|exp(_−∥e∥_<sup>2</sup>_/_1_._0<sup>2</sup>)<br>|
||Body Angular Velocity|0.25|exp(_−∥e∥_<sup>2</sup>_/_3_._14<sup>2</sup>)|
||Global Object Position|0.5|exp(_−∥e∥_<sup>2</sup>_/_0_._3<sup>2</sup>)|
||Global Object Orientation|0.5|exp(_−∥e∥_<sup>2</sup>_/_0_._4<sup>2</sup>)<br>|
||Global Object Lin. Velocity|0.5|exp(_−∥e∥_<sup>2</sup>_/_1_._0<sup>2</sup>)<br>|
||Global Object Ang. Velocity|0.5|exp(_−∥e∥_<sup>2</sup>_/_3_._14<sup>2</sup>)|
|**Interaction**|Obj-to-Body Rel. Position|0.25|exp(_−∥e∥_<sup>2</sup>_/_0_._3<sup>2</sup>)<br>|
||Obj-to-Body Rel. Orientation|0.25|exp(_−∥e∥_<sup>2</sup>_/_0_._4<sup>2</sup>)<br>|
||Contact Consistency|1.0|I(_Fcontact >_1_._0N) ==<sup>ˆ</sup>_lt_|
|**Regularization**|Feet Air Time|5.0|�(_tair −_0_._5)|
||Feet Slip Penalty|-0.1|_∥v_<sup>_xy_</sup><br>_foot_<sup>_∥·_ I(</sup><sup>_Fcontact >_ 1</sup><sup>_._0N)</sup>|
||Undesired Contacts|-0.1|I(_Fothers >_1_._0N)|
||Joint Acceleration|_−_2_._5_×_10<sup>_−_7</sup>|_∥_¨_q∥_<sup>2</sup>|
||Joint Torque|_−_1_._0_×_10<sup>_−_5</sup>|_∥τ∥_<sup>2</sup>|
||Action Rate|-0.1|_∥at −at−_1_∥_<sup>2</sup>|
||Joint Position Limits|-10.0|I(_q /∈_[_qmin, qmax_])|


Table 8: Domain Randomization Parameters 

|**Parameter**|**Range / Details**|
|---|---|
|Robot static friction|[0.3, 1.6]|
|Robot dynamic friction|[0.3, 1.2]|
|Robot restitution|[0.0, 0.5]|
|Joint default position|_±_0_._01rad<br>|
|Base center of mass (x, y, z)|_±_(0_._025_,_0_._05_,_0_._05)m|
|Object static friction|[0.2, 0.8]|
|Object dynamic friction|[0.2, 0.8]|
|Object restitution|[0.0, 0.5]|
|Object mass scale|[0.5, 2.0]|
|Robot external push (lin, ang)|_±_0_._3m/s,_±_0_._5rad/s|
|Object external push (lin, ang)|_±_0_._5m/s,_±_1_._0rad/s|
|Push interval|[1.5, 3.0] s|


Table 9: Early Termination 

|**Termination Term**|**Threshold**|
|---|---|
|Root position error|0.3 m|
|Root orientation error|0.8 rad|
|Body position error|0.3 m|
|Object position error|0.3 m|
|Object orientation error|0.8 rad|


17 

## **C Limitations and Future Work** 

First, the current data-processing pipeline extracts relatively coarse priors, limiting the framework to coarse-grained interaction skills. How to acquire fine-grained skills remains an open question. Second, data utilization efficiency is relatively low. Exploring data augmentation and generative models to learn interaction skills from limited human videos represents a valuable direction. Finally, the state-based policy hinders deployment convenience. How to develop policies that can effectively process visual and language inputs remains an open challenge for future research. 

## **D Computation Resources** 

All simulation, RL policy training, and hierarchical policy inference are conducted within the IsaacSim on a single NVIDIA GeForce RTX 5090 GPU. For each individual task, training the Refiner and the Tracker takes approximately 20 GPU hours each, while training the Command Generator requires around 5 GPU hours. 

18 

