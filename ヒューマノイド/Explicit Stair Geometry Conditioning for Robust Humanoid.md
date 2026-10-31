---
title: "Explicit Stair Geometry Conditioning for Robust Humanoid Locomotion"
date: "2026-05-11"
authors: "Jianguo Zhang; Wentai Xu; Shusheng Ye; Yuxiang He; Weimin Qi; Qinbo Sun"
url: https://arxiv.org/abs/2605.09944
pdf: https://arxiv.org/pdf/2605.09944
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2605.09944)** / [論文ページ](https://arxiv.org/abs/2605.09944)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Explicit Stair Geometry Conditioning for Robust Humanoid Locomotion** 

Jianguo Zhang<sup>1,</sup><sup>_†_</sup> , Wentai Xu<sup>1,</sup><sup>_†_</sup> , Shusheng Ye<sup>1,</sup><sup>_∗_</sup> , Yuxiang He<sup>1</sup> , Weimin Qi<sup>3</sup> , Qinbo Sun<sup>3</sup> , Ning Ding<sup>1</sup> , Liguang Zhou<sup>1,2,</sup><sup>_∗_</sup> 

**_Abstract_ — Robust humanoid stair climbing remains challenging due to geometric discontinuities, sensitivity to step height variations, and perception uncertainty in real-world environments. Existing learning-based locomotion policies often rely on implicit terrain representations or blind proprioceptive feedback, limiting their ability to generalize across varying stair geometries and to anticipate required gait adjustments. This paper proposes an explicit stair geometry conditioning framework for robust humanoid stair climbing. Instead of encoding terrain as high-dimensional latent features, we extract a compact set of interpretable geometric parameters, including step height, step depth, and current yaw angle relative to the robot heading. These explicit stair parameters directly condition a Proximal Policy Optimization (PPO)-based locomotion policy, enabling proactive modulation of swing-foot clearance and stride characteristics according to stair structure. Simulation experiments demonstrate improved generalization across unseen stair heights beyond the training distribution. Real-world experiments on the Unitree G1 humanoid validate reliable indoor and outdoor stair traversal. In challenging outdoor scenarios, the robot successfully ascends 33 consecutive steps without failure, demonstrating robustness and practical deployability.** 

## I. INTRODUCTION 

Humanoid robots are expected to operate in humancentered environments where staircases are ubiquitous, including public buildings, transportation hubs, and outdoor infrastructures. Although recent reinforcement learning (RL) approaches have achieved robust velocity tracking on flat terrain, reliable stair climbing remains significantly more challenging due to geometric discontinuities and sensitivity to step height variations. 

Most learning-based locomotion policies fall into two categories. Blind locomotion approaches rely primarily on proprioceptive feedback and adapt reactively through contact information. While effective on mildly uneven terrain, such policies lack anticipatory capability and frequently fail on stairs where precise swing-foot clearance and stride modulation are required. Perception-aware methods incorporate exteroceptive inputs such as height maps or depth images. However, these approaches typically encode terrain implicitly as high-dimensional latent features, making them sensitive to perception noise and difficult to interpret. When stair geometry varies beyond the training distribution, performance often degrades substantially. 

> _†_ These authors contributed equally to this work. 

> _∗_ Corresponding authors: Liguang Zhou and Shusheng Ye. 

> 1 Shenzhen Institute of Artificial Intelligence and Robotics for Society. 

> 2 School of Science and Engineering, The Chinese University of Hong Kong, Shenzhen. 

> 3 Mohamed bin Zayed University of Artificial Intelligence (MBZUAI). 


Fig. 1: **Explicit stair geometry conditioning for robust humanoid locomotion.** The local stair structure is parameterized by step height _h_ step, step depth _d_ step, and current yaw angle _θ_ yaw<sup>current</sup> defined relative to the robot heading direction. These explicit geometric parameters directly condition the locomotion policy, enabling anticipatory and adaptive gait modulation across varying stair configurations. 

A key limitation of prior work is the absence of explicit geometric conditioning. In practice, stair traversal fundamentally depends on a small number of geometric quantities, such as step height and step depth, which directly determine required foot clearance and step placement. Policies that do not explicitly reason about these quantities must implicitly infer them through latent representations, resulting in limited generalization and reduced robustness. 

To address this limitation, we propose _explicit stair geometry conditioning_ for robust humanoid stair climbing. As illustrated in Fig. 1, the local stair structure is summarized by a compact set of interpretable parameters, including step height _h_ step, step depth _d_ step, and current yaw angle _θ_ yaw<sup>current</sup> defined relative to the robot heading direction. Instead of encoding terrain implicitly as latent visual features, these explicit geometric parameters directly condition the locomotion policy. 

Conditioned on this structured stair representation, a PPObased policy learns to proactively modulate swing-foot clearance and stride characteristics according to stair geometry. This explicit conditioning improves robustness across 

varying stair configurations and reduces reliance on fragile implicit terrain encoding. 

We validate the proposed approach in both simulation and real-world experiments. Simulation results demonstrate improved generalization across unseen stair heights beyond the training distribution. On the Unitree G1 humanoid platform, the controller achieves reliable indoor and outdoor stair traversal. In challenging outdoor environments, the robot successfully ascends 33 consecutive steps without failure, demonstrating robustness and practical deployability. 

The main contributions of this work are summarized as follows: 

- 1) We propose an explicit stair geometry conditioning framework that represents local stair structure using compact and interpretable geometric parameters for policy input. 

- 2) We develop a PPO-based humanoid locomotion policy directly conditioned on step height, step depth, and current yaw, enabling anticipatory gait modulation during stair climbing. 

- 3) We demonstrate improved generalization across unseen stair geometries in simulation and validate robust indoor and outdoor deployment, including successful traversal of 33 consecutive outdoor steps. 

## II. RELATED WORK 

Learning-based legged locomotion has progressed from early agile control to fast, generalizable training pipelines. Reinforcement learning enabled dynamic skills on real robots and sample-efficient real-world learning [7], [6], [5], while experience transfer and multi-expert or multi-behavior policies improved adaptability [26], [29], [15]. Large-scale training with curricula and parallel simulation accelerated learning and broadened generalization [16], [23], supported by sim-to-real techniques such as dynamics and domain randomization [21], [27]. Standard policy optimization backbones (e.g., PPO) remain dominant [25], often paired with high-throughput simulators [14]. Model-based and compliant control approaches further complement learned policies for stable bipedal walking [22]. Perception-driven locomotion extends these advances to complex terrain. Visionconditioned walking and egocentric perception enable stepping over obstacles and irregular ground [32], [2], while cross-modal transformers and volumetric memory improve temporal terrain understanding [31], [30]. Implicit terrain imagination and slope-conditioned linear policies demonstrate robust adaptation under limited sensing [19], [20], and terrain robustness is also pursued via proprioceptive controllers and slip-aware strategies [10], [8]. Recent work broadens the task scope to risky footholds, legged manipulation, and parkour-style behaviors [33], [3], [4], including transferring bipedal motion skills across morphologies [11]. Robustness under disturbances and uncertainty has been addressed by internal estimation and robust control formulations. The Hybrid Internal Model infers external effects from proprioception to improve generalization [12], while constraint-augmented RL reduces reward engineering and 

improves stability [9]. Robust RL and _H∞_ -style methods provide theoretical grounding for worst-case disturbance handling, complemented by passivity-preserving synthesis and safe RL with explicit constraints [18], [1]. Beyond singleagent locomotion, multi-agent learning frameworks such as MADDPG and counterfactual credit assignment, as well as emergent communication, provide general tools for complex coordination [13]. 

In contrast to prior perceptive locomotion methods that rely on implicit terrain embeddings, our approach explicitly estimates compact stair geometric parameters and directly conditions a PPO-based locomotion policy on this interpretable representation. By explicitly encoding step height, step depth, and heading alignment, the proposed method improves generalization across varying stair configurations and enhances robustness during real-world stair climbing. 

## III. METHOD 

We focus on stair environments as a representative class of structured terrains. Instead of implicitly learning terrain adaptation from raw perception, we propose an explicit stair geometry representation that exposes control-relevant geometric parameters. 

The framework consists of: (i) a BEV-based terrain perception network, (ii) a privileged terrain teacher used only in simulation, and (iii) a PPO-based actor–critic locomotion policy. 

The perception network predicts a compact terrain token containing step height, step depth, and heading information, which directly conditions the locomotion policy. During deployment, only onboard sensing and the learned perceptionpolicy pipeline are retained. 

## _A. Problem Formulation_ 

Humanoid locomotion over complex terrain is modeled as a Markov Decision Process (MDP). At timestep _t_ , the robot receives observation 


where _o_<sup>prop</sup> _t_ denotes proprioceptive sensing (base pose and velocity, joint states, contact indicators, and etc), and _zt_ is the predicted explicit stair geometry representation. 

The policy outputs action _at ∈A_ executed by a wholebody PD controller. The policy _πθ_ ( _at|ot_ ) is optimized with PPO to maximize the expected discounted return: 


where _rt_ follows the default IsaacLab rough-locomotion weighted reward [17]. 

## _B. Explicit Stair Geometry Representation_ 

_1) Point Cloud Input:_ The raw perception input consists of local point cloud _P_ = _{pi}_<sup>_N_</sup> _i_ =1<sup>,where</sup><sup>_pi∈_R3contains</sup> ( _x, y, z_ ) coordinates expressed in the robot-centric frame. 


Fig. 2: Overview of the proposed explicit stair geometry conditioning framework. During training, a teacher branch leverages privileged terrain and proprioceptive information in simulation to supervise a student encoder that predicts structured stair geometric parameters, including step height, step depth, and current yaw. These explicit parameters condition a PPO-based actor–critic policy for robust stair climbing. During deployment, only the student encoder and locomotion policy are used, enabling real-world execution without privileged information. 

_2) BEV Projection:_ We project the 3D point cloud into a fixed-size BEV grid centered at the robot. 

The projection region is defined as 3 m _×_ 3 m with a spatial resolution of 0 _._ 05 m, resulting in a grid size of _H_ = _W_ = 60. Grid size is _H_ = _W_ = 03 _.._ 050<sup>= 60. The resulting BEV feature</sup> map is: 


For each grid cell, we compute Z-axis statistics: 

- Channel 0: max( _z_ ) 

- Channel 1: min( _z_ ) 

- Channel 2: mean( _z_ ) 

- Channel 3: max( _z_ ) _−_ min( _z_ ) 

- Channel 4: std( _z_ ) 

- Channel 5: normalized point density 

These statistics capture local elevation discontinuities and surface roughness, which are informative for identifying stair structures, where empty cells are zero-filled. 

_3) BEV Terrain Encoder:_ The BEV feature map is processed by a convolutional neural network: 

- Multi-layer convolution 

- Batch Normalization 

- ReLU activation 

- Progressive downsampling 

The encoder outputs high-level spatial features: 


where _C_<sup>_′_</sup> , _H_<sup>_′_</sup> , and _W_<sup>_′_</sup> denote the channel and spatial dimensions of the encoded BEV feature map after the convolutional encoder. In our implementation, the encoder outputs _C_<sup>_′_</sup> = 128 channels with spatial resolution _H_<sup>_′_</sup> = _W_<sup>_′_</sup> = 8. 

_4) Explicit Stair Geometry Representation:_ To enable anticipatory locomotion over stairs, we propose an explicit stair geometry representation that exposes the physical parameters required for stair traversal. Instead of encoding terrain implicitly as high-dimensional visual features, the perception network estimates a compact set of interpretable geometric quantities that directly influence stepping behavior. From the encoded BEV features, the perception network predicts the terrain class 


together with the geometric stair parameters _hstep, dstep ∈_ R _,_ where _hstep_ denotes the step height and _dstep_ denotes the step depth. These quantities determine the minimum swing-foot clearance and feasible foot placement during stair traversal. To incorporate motion intent, the robot heading orientation is represented by 


which denotes the yaw angle of the robot relative to the terrain direction. The resulting structured terrain token is defined as 


For flat terrain, no discrete stair geometry exists. Therefore the geometric parameters are set to _hstep_ = 0 and _dstep_ = 0, while _θt_ remains the robot heading orientation. Conditioning the locomotion policy on this structured representation enables physically consistent adaptation, such as increasing swing-foot clearance for taller stairs and aligning the robot heading before stepping. 

## _C. Privileged Training and Joint Optimization_ 

During simulation training, a privileged teacher provides ground-truth terrain classes and geometric parameters. The terrain prediction loss is defined as 


where _L_ CE denotes cross-entropy loss for terrain classification, and the _L_ 1 terms correspond to SmoothL1 regression losses for step height and step depth. 

Training follows a three-stage strategy. First, the locomotion policy is pretrained using ground-truth terrain parameters to learn stable terrain-conditioned behaviors. Second, the perception network is trained independently under teacher supervision. We optimize the actor–critic policy using the standard clipped PPO objective with GAE [25], [24]. The joint training objective is: 


where _α_ balances reinforcement learning and terrain prediction objectives. 

We set _λ_ cls = 0 _._ 6, _λh_ = 1, and _λd_ = 1 to place higher emphasis on geometric parameter estimation, which directly affects locomotion control. The joint optimization weight is set to _α_ = 1 to balance reinforcement learning and perception supervision. 

## _D. Deployment_ 

At deployment, the privileged teacher is removed and the policy relies solely on fused onboard sensing and the predicted terrain token. The explicit stair geometry representation enables across flat segments and stairs, including indoor and irregular outdoor staircases, improving generalization to unseen terrain configurations and real-world perception noise. 

## IV. EXPERIMENTAL EVALUATION 

To comprehensively evaluate the proposed explicit stair geometry conditioning humanoid locomotion framework, we conduct both simulation-based experiments and real-world robot experiments. Simulation experiments are first performed to validate learning stability and stair generalization 


Fig. 3: Simulation sequence of humanoid stair climbing under explicit stair geometry conditioning. From left to right, the robot ascends consecutive steps while adapting swing-foot clearance according to the estimated step height _h_ step. The policy maintains stable posture and consistent step placement across the staircase. 

under controlled conditions, followed by real-robot experiments to demonstrate practical feasibility and robustness in real environments. 

## _A. Experiment Settings_ 

We first evaluate the proposed explicit stair geometry conditioning in simulation to validate learning stability, stairheight generalization, and robustness under controlled conditions. 

All policies are trained with PPO and deployed with the same observation/action interfaces as in real-world experiments. 

_1) Training Setup:_ The locomotion policy is trained with PPO using an actor–critic architecture. The policy observation includes high-rate proprioception and low-rate visual perception. Unless otherwise stated, we use the same network architecture and control frequency as in real deployment. 

## _B. Simulation Experiments_ 

_1) Stairs Traversal:_ In simulation, the proposed method achieves reliable traversal across different stairs while maintaining stable command tracking. As depicted in Fig. 3, explicitly conditioning the PPO policy on stair geometric parameters reduces foot scuffing and improves stair-climbing stability, especially at terrain transitions where geometryonly perception is prone to ambiguity. 

_2) MuJoCo Simulation and Velocity Tracking.:_ We evaluate the proposed locomotion policy in MuJoCo simulation on a stair-climbing task with time-varying forward velocity commands. The top row shows representative snapshots of the humanoid robot ascending stairs under different commanded velocities, while the bottom plot reports the commanded forward velocity and the measured robot velocity over time. As illustrated in Fig. 4, the robot accurately tracks piecewise-constant velocity commands despite abrupt command transitions and changes in stair geometry. Transient tracking errors mainly occur during rapid acceleration and deceleration phases, whereas small steady-state errors are observed once the velocity stabilizes. Notably, during low-speed and near-stop intervals, the policy maintains balance without foot slippage, and at higher velocities it preserves smooth and consistent stepping patterns. These results demonstrate that the proposed explicit stair geometry conditioning enables robust and responsive velocity tracking for stair climbing in simulation. 


Fig. 4: MuJoCo simulation results of stair climbing with velocity tracking. Top: representative snapshots of the humanoid robot ascending stairs under different forward velocity commands. Bottom: commanded forward velocity (red dashed) and measured velocity (blue) over time. The policy achieves accurate velocity tracking and stable locomotion despite abrupt command changes. 


Fig. 5: Ablation study on stair perception representations for geometry-conditioned locomotion. We compare BlindPPO (proprioception only), HeightMap-PPO (local elevation map), and our explicit stair geometry representation. Our representation leads to faster learning and superior asymptotic performance. 

## _C. Ablation Study_ 

_1) Learning Curves Comparison:_ Fig. 5 compares the learning curves of three locomotion policies trained with different stair perception representations: _Ours_ , _Height MapPPO_ , and _Blind-PPO_ . The explicit stair geometry conditioning consistently achieves the fastest convergence and the highest final episode reward, indicating that explicit stair geometric parameters provide more structured and task-relevant information for policy learning. The heightmap based policy shows moderate performance, converging slower and reaching a lower reward plateau, suggesting that raw geometric 

TABLE I: Training performance comparison (mean _±_ std over 3 random seeds). Lower is better for tracking errors, higher is better for terrain difficulty, reward, and success rate. 

|Method|_E_vel _↓_|_E_ang _↓_|_M_terrain _↑_|_M_reward _↑_|Success (%)|
|---|---|---|---|---|---|
|Blind-PPO|0.29|0.36|2.54|17.61|52_±_5|
|HeightMap-PPO|0.20|0.30|4.16|32.23|88_±_3|
|**Ours**|**0.16**|**0.22**|**5.30**|**45.10**|96_±_2|


elevation alone is less effective in capturing traversabilityrelevant features. In contrast, the blind climbing policy exhibits the slowest learning progress and the lowest asymptotic performance, highlighting the difficulty of learning stable stair-climbing behaviors without explicit terrain perception. Overall, these results demonstrate that incorporating explicit stair geometry representation significantly improves both learning efficiency and locomotion performance. 

_2) Comparison experiment:_ We conduct a comprehensive baseline comparison to evaluate the effectiveness of different terrain perception modalities under a unified reinforcement learning framework. All methods are trained using Proximal Policy Optimization (PPO) with identical network architecture, reward formulation, and optimization settings. The only difference lies in the perceptual input representation. 

Stair configurations are procedurally randomized, including variations in step height, step depth, and yaw orientation, with occasional flat segments before and after the staircase. To verify cross-simulator consistency, trained policies are additionally evaluated in MuJoCo without fine-tuning. 

We compare the following four methods: 

- **Blind-PPO** : uses only proprioceptive observations without any exteroceptive perception. 

- **HeightMap-PPO** : encodes a local 11 _×_ 17 elevation map as input to the PPO policy. 

- **Ours** : leverages an explicit stair geometry representation that models stair state (upstairs / downstairs / flat) and fitted geometric parameters (step height, step depth, and current yaw). 

Locomotion performance is evaluated using multiple complementary metrics: linear and angular velocity tracking errors ( _E_ vel, _E_ ang), the maximum traversable terrain difficulty ( _M_ terrain), the normalized cumulative episode reward ( _M_ reward), and overall task success rate. All results are reported as mean _±_ standard deviation over three random seeds. 

As shown in Table I, Blind-PPO exhibits large tracking errors and low success rate, indicating that purely proprioceptive control is insufficient for robust locomotion over structured stair environments. 

HeightMap-PPO substantially improves terrain adaptability and success rate; however, its performance remains sensitive to perception noise and discretization artifacts. 

In contrast, the proposed explicit stair geometry representation achieves the lowest velocity tracking errors and the highest terrain difficulty, reward, and success rate. By explicitly encoding interpretable terrain parameters, the policy can adapt its locomotion strategy according to underlying phys- 


Fig. 6: Time-sequence key frames from real humanoid robot experiments in an indoor environment (left to right). The robot maintains stable locomotion during continuous indoor walking and motion transitions, demonstrating reliable real-world deployment of the proposed explicit stair geometry representation. 


Fig. 7: Time-sequence key frames from real humanoid robot outdoor step-climbing experiments (1 s–8 s). The robot continuously ascends multiple steps with adaptive swing-foot clearance and coordinated body elevation, demonstrating robust real-world stair-climbing capability of the proposed explicit stair geometry representation. 

TABLE II: Accuracy of explicit stair geometry estimation in simulation and real-world environments. MAE denotes mean absolute error. 

|Setting|MAE(_h_step)|MAE(_d_step)|MAE(_θ_<sup>current</sup><br>yaw<br>)|State Acc (%)|
|---|---|---|---|---|
|Sim|0.6 cm|0.7 cm|1.8<sup>_◦_</sup>|99.1|
|Real|0.9 cm|1.1 cm|3.9<sup>_◦_</sup>|97.3|


ical structure, leading to more stable, robust, and sampleefficient learning across diverse stair geometries. 

_3) Stair Geometry Estimation Accuracy:_ To evaluate the robustness and reliability of the explicit stair geometry estimation module, we conduct quantitative analysis in both simulation and real-world environments. 

**Simulation Evaluation.** During training in simulation, Gaussian noise is injected into the depth input to mimic realistic sensor noise and perception uncertainty. For evaluation, we generate random stair configurations with varying step height, step depth, and yaw orientation. The trained perception module is evaluated over 1000 randomized episodes, and we compute the mean absolute error (MAE) for step height _h_ step, step depth _d_ step, and current yaw angle _θ_ yaw<sup>current</sup> , along with stair-state classification accuracy. 

**Real-World Evaluation.** In real-world experiments, we evaluate the perception module on two standard staircase configurations with known geometric parameters: (i) step 

TABLE III: Generalization performance across different stair heights. The first three heights are used during training, while higher stairs are unseen during testing. 

|**Stair Height**|**Vision-based (MoRE) [28]**|**Ours**|
|---|---|---|
|0.12m (Training)|97.2%|**99.7%**|
|0.14m (Training)|95.8%|**99.4%**|
|0.16m (Training)|90.3%|**97.5%**|
|0.18m (Testing)|88.5%|**92.3%**|
|0.20m (Testing)|78.8%|**87.6%**|
|0.22m (Testing)|69.4%|**82.7%**|


TABLE IV: Success rate on irregular outdoor stairs. 

|**Method**|**Success Rate**|
|---|---|
|BlindPPO|20%|
|HeightMapPPO|75%|
|Vision-based (MoRE)|72%|
|Ours|**93%**|


height 17 cm and depth 30 cm, and (ii) step height 15 cm and depth 28 cm. The humanoid robot collects approximately 200 depth observations under varying observation distances (0.5–2.0 m) and viewing angles. Predicted geometric parameters are compared against manually measured ground-truth values, and estimation errors are computed accordingly. 

The quantitative results are summarized in Table II. In 

simulation, the model achieves sub-centimeter accuracy for step height and depth estimation, and below 2<sup>_◦_</sup> error for yaw prediction. In real-world experiments, only moderate performance degradation is observed, maintaining centimeter-level geometric precision and over 97% stair-state classification accuracy. 

These results confirm that the explicit stair geometry representation provides stable and physically meaningful controlrelevant parameters, enabling reliable geometry-conditioned locomotion across both simulated and real environments. 

_4) Performance Trend Across Stair Heights:_ We evaluate continuous stair-height generalization from 0.12 m to 0.22 m, where stair height corresponds to the geometric parameter _h_ step estimated by our perception module. While both MoRE and our method perform well within the training distribution (0.12–0.16 m), performance degradation becomes evident in unseen heights. 

As shown in Table III, MoRE drops from 90.3% at 0.16 m to 69.4% at 0.22 m, whereas our method maintains a higher success rate of 82.7%. The performance gap increases monotonically as stair height deviates from the training distribution, reaching a +13.3% improvement at 0.22 m. 

This trend indicates that the proposed explicit stair geometry representation enables physically grounded adaptation (e.g., increasing swing-foot clearance with stair height), rather than memorizing visual patterns. 

_5) Generalization to Irregular Outdoor Stairs:_ We further evaluate robustness on irregular outdoor staircases. 

As summarized in Table IV, our method achieves a 93% success rate, significantly outperforming BlindPPO (20%), HeightMapPPO (75%), and MoRE (72%). 

Unlike heightmap-based methods that are sensitive to noise and vision-based policies affected by lighting variations, our explicit stair geometry conditioning provides robust structural cues, leading to improved deployment stability. 

## _D. Real-World Robot Experiments_ 

After training in simulation, the learned policy is directly deployed on a real humanoid robot platform without additional fine-tuning. Real-world experiments are conducted in both indoor and outdoor environments to evaluate robustness, generalization, and long-horizon performance. 

_1) Indoor Stair-Climbing Experiments:_ Indoor experiments are performed on a structured staircase consisting of five consecutive steps, representative of common indoor environments such as office buildings. The robot autonomously perceives the staircase, infers parameters and adjusts swingfoot clearance and body posture accordingly. As shown in Fig. 6, the robot successfully climbs all five steps in a continuous motion sequence without external support, demonstrating stable and smooth locomotion enabled by the proposed explicit stair geometry conditioning policy. 

_2) Outdoor Stair-Climbing Experiments:_ To further evaluate scalability and long-duration robustness, outdoor experiments are conducted on a large staircase consisting of 33 consecutive steps. This scenario introduces increased 

challenges due to prolonged execution time, accumulated state estimation errors, and environmental variability. Fig. 7 presents a time-sequence visualization extracted from 1 s to 8 s of the outdoor experiment, illustrating multiple step ascents with coordinated body elevation and adaptive swingfoot clearance. The robot successfully completes the entire staircase, highlighting the robustness and generalization capability of the proposed approach. 

## V. CONCLUSION 

This paper presented an explicit stair geometry conditioning framework for robust humanoid stair climbing. By estimating compact and interpretable geometric parameters, including step height, step depth, and current yaw, and directly conditioning a PPO-based locomotion policy on these quantities, the proposed method enables proactive gait modulation without relying on implicit terrain embeddings or privileged information at deployment. 

Simulation experiments demonstrated improved generalization across unseen stair heights compared to blind and heightmap-based baselines. The learned policy transferred directly to a real humanoid platform and achieved reliable indoor and outdoor stair traversal without additional finetuning. In challenging outdoor scenarios, the robot successfully ascended 33 consecutive steps, highlighting the robustness and practical deployability of explicit stair geometry conditioning. 

## REFERENCES 

- [1] Ali Aalipour and Alireza Khani. Data-driven h-infinity control with a real-time and efficient reinforcement learning algorithm: An application to autonomous mobility-on-demand systems. _arXiv preprint arXiv:2309.08880_ , 2023. 

- [2] Ananye Agarwal, Ashish Kumar, Jitendra Malik, and Deepak Pathak. Legged locomotion in challenging terrains using egocentric vision. In _Conference on robot learning_ , pages 403–415. PMLR, 2023. 

- [3] Xuxin Cheng, Ashish Kumar, and Deepak Pathak. Legs as manipulator: Pushing quadrupedal agility beyond locomotion. In _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , 2023. 

- [4] Xuxin Cheng, Kexin Shi, Ananye Agarwal, and Deepak Pathak. Extreme parkour with legged robots. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 11443–11450. IEEE, 2024. 

- [5] Sehoon Ha, Peng Xu, Zhenyu Tan, Sergey Levine, and Jie Tan. Learning to walk in the real world with minimal human effort. In Jens Kober, Fabio Ramos, and Claire Tomlin, editors, _Proceedings of the 2020 Conference on Robot Learning_ , volume 155 of _Proceedings of Machine Learning Research_ , pages 1110–1120. PMLR, 16–18 Nov 2021. 

- [6] Tuomas Haarnoja, Sehoon Ha, Aurick Zhou, Jie Tan, George Tucker, and Sergey Levine. Learning to walk via deep reinforcement learning. In _Proceedings of Robotics: Science and Systems_ , FreiburgimBreisgau, Germany, June 2019. 

- [7] J. Hwangbo, J. Lee, A. Dosovitskiy, D. Bellicoso, V. Tsounis, V. Koltun, and M. Hutter. Learning agile and dynamic motor skills for legged robots. _Science Robotics_ , 2019. 

- [8] Fabian Jenelten, Jemin Hwangbo, Fabian Tresoldi, C Dario Bellicoso, and Marco Hutter. Dynamic locomotion on slippery ground. _IEEE Robotics and Automation Letters_ , 4(4):4170–4176, 2019. 

- [9] Yunho Kim, Hyunsik Oh, Jeonghyun Lee, Jinhyeok Choi, Gwanghyeon Ji, Moonkyu Jung, Donghoon Youm, and Jemin Hwangbo. Not only rewards but also constraints: Applications on legged robot locomotion. _IEEE Transactions on Robotics_ , 40:2984–3003, 2024. 

- [10] Joonho Lee, Jemin Hwangbo, Lorenz Wellhausen, Vladlen Koltun, and Marco Hutter. Learning quadrupedal locomotion over challenging terrain. _Science robotics_ , 5(47):eabc5986, 2020. 

- [11] Yunfei Li, Jinhan Li, Wei Fu, and Yi Wu. Learning agile bipedal motions on a quadrupedal robot. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 9735–9742. IEEE, 2024. 

- [12] Junfeng Long, ZiRui Wang, Quanyi Li, Liu Cao, Jiawei Gao, and Jiangmiao Pang. Hybrid internal model: Learning agile legged locomotion with simulated robot response. In _The Twelfth International Conference on Learning Representations_ , 2024. 

- [13] Ryan Lowe, Yi I Wu, Aviv Tamar, Jean Harb, OpenAI Pieter Abbeel, and Igor Mordatch. Multi-agent actor-critic for mixed cooperativecompetitive environments. _Advances in neural information processing systems_ , 30, 2017. 

- [14] Viktor Makoviychuk, Lukasz Wawrzyniak, Yunrong Guo, Michelle Lu, Kier Storey, Miles Macklin, David Hoeller, Nikita Rudin, Arthur Allshire, Ankur Handa, et al. Isaac gym: High performance gpu-based physics simulation for robot learning. _arXiv preprint arXiv:2108.10470_ , 2021. 

- [15] Gabriel B Margolis and Pulkit Agrawal. Walk these ways: Tuning robot control for generalization with multiplicity of behavior. In _Conference on Robot Learning_ , pages 22–31. PMLR, 2023. 

- [16] Gabriel B Margolis, Ge Yang, Kartik Paigwar, Tao Chen, and Pulkit Agrawal. Rapid locomotion via reinforcement learning. _The International Journal of Robotics Research_ , 43(4):572–587, 2024. 

- [17] Mayank Mittal, Pascal Roth, James Tigue, Antoine Richard, Octi Zhang, Peter Du, Antonio Serrano-Mu˜noz, Xinjie Yao, Ren´e Zurbr¨ugg, Nikita Rudin, Lukasz Wawrzyniak, Milad Rakhsha, Alain Denzler, Eric Heiden, Ales Borovicka, Ossama Ahmed, Iretiayo Akinola, Abrar Anwar, Mark T. Carlson, Ji Yuan Feng, Animesh Garg, Renato Gasoto, Lionel Gulich, Yijie Guo, M. Gussert, Alex Hansen, Mihir Kulkarni, Chenran Li, Wei Liu, Viktor Makoviychuk, Grzegorz Malczyk, Hammad Mazhar, Masoud Moghani, Adithyavairavan Murali, Michael Noseworthy, Alexander Poddubny, Nathan Ratliff, Welf Rehberg, Clemens Schwarke, Ritvik Singh, James Latham Smith, Bingjie Tang, Ruchik Thaker, Matthew Trepte, Karl Van Wyk, Fangzhou Yu, Alex Millane, Vikram Ramasamy, Remo Steiner, Sangeeta Subramanian, Clemens Volk, CY Chen, Neel Jawale, Ashwin Varghese Kuruttukulam, Michael A. Lin, Ajay Mandlekar, Karsten Patzwaldt, John Welsh, Huihua Zhao, Fatima Anes, Jean-Francois Lafleche, Nicolas Mo¨enneLoccoz, Soowan Park, Rob Stepinski, Dirk Van Gelder, Chris Amevor, Jan Carius, Jumyung Chang, Anka He Chen, Pablo de Heras Ciechomski, Gilles Daviet, Mohammad Mohajerani, Julia von Muralt, Viktor Reutskyy, Michael Sauter, Simon Schirm, Eric L. Shi, Pierre Terdiman, Kenny Vilella, Tobias Widmer, Gordon Yeoman, Tiffany Chen, Sergey Grizan, Cathy Li, Lotus Li, Connor Smith, Rafael Wiltz, Kostas Alexis, Yan Chang, David Chu, Linxi ”Jim” Fan, Farbod Farshidian, Ankur Handa, Spencer Huang, Marco Hutter, Yashraj Narang, Soha Pouya, Shiwei Sheng, Yuke Zhu, Miles Macklin, Adam Moravanszky, Philipp Reist, Yunrong Guo, David Hoeller, and Gavriel State. Isaac lab: A gpu-accelerated simulation framework for multi-modal robot learning. _arXiv preprint arXiv:2511.04831_ , 2025. 

Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

   - [26] Laura M Smith, J. Chase Kew, Tianyu Li, Linda Luu, Xue Bin Peng, Sehoon Ha, Jie Tan, and Sergey Levine. Learning and Adapting Agile Locomotion Skills by Transferring Experience. In _Proceedings of Robotics: Science and Systems_ , Daegu, Republic of Korea, July 2023. 

   - [27] Josh Tobin, Rachel Fong, Alex Ray, Jonas Schneider, Wojciech Zaremba, and Pieter Abbeel. Domain randomization for transferring deep neural networks from simulation to the real world. In _2017 IEEE/RSJ international conference on intelligent robots and systems (IROS)_ , pages 23–30. IEEE, 2017. 

   - [28] Dewei Wang, Xinmiao Wang, Xinzhe Liu, Jiyuan Shi, Yingnan Zhao, Chenjia Bai, and Xuelong Li. More: Mixture of residual experts for humanoid lifelike gaits learning on complex terrains, 2025. 

   - [29] Chuanyu Yang, Kai Yuan, Qiuguo Zhu, Wanming Yu, and Zhibin Li. Multi-expert learning of adaptive legged locomotion. _Science Robotics_ , 5(49):eabb2174, 2020. 

   - [30] Ruihan Yang, Ge Yang, and Xiaolong Wang. Neural volumetric memory for visual locomotion control. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 1430– 1440, 2023. 

   - [31] Ruihan Yang, Minghao Zhang, Nicklas Hansen, Huazhe Xu, and Xiaolong Wang. Learning vision-guided quadrupedal locomotion endto-end with cross-modal transformers. In _International Conference on Learning Representations_ , 2022. 

   - [32] Wenhao Yu, Deepali Jain, Alejandro Escontrela, Atil Iscen, Peng Xu, Erwin Coumans, Sehoon Ha, Jie Tan, and Tingnan Zhang. Visuallocomotion: Learning to walk on complex terrains with vision. In _5th Annual Conference on Robot Learning_ , 2021. 

   - [33] Chong Zhang, Nikita Rudin, David Hoeller, and Marco Hutter. Learning agile locomotion on risky terrains. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 11864– 11871. IEEE, 2024. 

- [18] Jun Morimoto and Kenji Doya. Robust reinforcement learning. _Neural computation_ , 17(2):335–359, 2005. 

- [19] I Made Aswin Nahrendra, Byeongho Yu, and Hyun Myung. Dreamwaq: Learning robust quadrupedal locomotion with implicit terrain imagination via deep reinforcement learning. In _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 5078–5084. IEEE, 2023. 

- [20] Kartik Paigwar, Lokesh Krishna, Shalabh Bhatnagar, Ashitava Ghosal, Bharadwaj Amrutur, Shishir Kolathaya, et al. Robust quadrupedal locomotion on sloped terrains: A linear policy approach. In _Conference on Robot Learning_ , pages 2257–2267. PMLR, 2021. 

- [21] Xue Bin Peng, Marcin Andrychowicz, Wojciech Zaremba, and Pieter Abbeel. Sim-to-real transfer of robotic control with dynamics randomization. In _2018 IEEE international conference on robotics and automation (ICRA)_ , pages 3803–3810. IEEE, 2018. 

- [22] Jacob Reher, Wen-Loong Ma, and Aaron D Ames. Dynamic walking with compliance on a cassie bipedal robot. In _2019 18th European Control Conference (ECC)_ , pages 2589–2595. IEEE, 2019. 

- [23] Nikita Rudin, David Hoeller, Philipp Reist, and Marco Hutter. Learning to walk in minutes using massively parallel deep reinforcement learning. In _Conference on robot learning_ , pages 91–100. PMLR, 2022. 

- [24] John Schulman, Philipp Moritz, Sergey Levine, Michael Jordan, and Pieter Abbeel. High-dimensional continuous control using generalized advantage estimation. _arXiv preprint arXiv:1506.02438_ , 2015. 

- [25] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and 

