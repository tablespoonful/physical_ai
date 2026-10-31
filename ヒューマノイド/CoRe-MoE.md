---
title: "CoRe-MoE: Contrastive Reweighted Mixture of Experts for Multi-Terrain Humanoid Locomotion with Gait Adaptation"
date: "2026-06-03"
authors: "Kailun Huang; Zikang Xie; Yanzhe Xie; Panpan Liao; Fanghai Zhang; Yanheng Mai"
url: https://arxiv.org/abs/2606.04718
pdf: https://arxiv.org/pdf/2606.04718
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.04718)** / [論文ページ](https://arxiv.org/abs/2606.04718)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **CoRe-MoE: Contrastive Reweighted Mixture of Experts for Multi-Terrain Humanoid Locomotion with Gait Adaptation** 

Kailun Huang<sup>1</sup><sup>_,∗_</sup> Zikang Xie<sup>1</sup><sup>_,∗_</sup> Yanzhe Xie<sup>1</sup><sup>_,∗_</sup> Panpan Liao<sup>4</sup><sup>_,∗_</sup> Fanghai Zhang<sup>1</sup> Yanheng Mai<sup>1</sup> Wenhao Xu<sup>3</sup> Yunheng Wang<sup>1</sup> Renjing Xu<sup>1</sup><sup>_,†_</sup> Haohui Huang<sup>4</sup><sup>_,†_</sup> Chenguang Yang<sup>2</sup><sup>_,†_</sup> _Fellow, IEEE_ 1Hong Kong University of Science and Technology (Guangzhou) 2Hong Kong Polytechnic University 3South China Agricultural University 4Guangdong University of Technology 

> _∗_ Equal contribution _†_ Corresponding authors 


Fig. 1: We propose **CoRe-MoE** enables smooth, natural, and continuous transitions between walking and running using a single unified policy, while maintaining stable adaptability to complex terrain. In contrast, **Hiking in the Wild** relies on separately trained walking and running policies that must be manually switched during execution, leading to abrupt transitions, reduced continuity, and noticeably unnatural motion, especially under terrain variations. **Project Page: https://core-moe.github.io/.** 

**_Abstract_ —Humans primarily rely on walking and running to traverse complex terrains. Similarly, humanoid robots should be able to smoothly transition between walking and running while maintaining natural and stable locomotion. However, unifying gait transition and multi-terrain adaptation within a single policy remains challenging due to gradient interference between tasks and the distribution shift caused by terrain variations. Although Mixture-of-Experts (MoE) architectures can mitigate multi-skill interference, direct joint training often fails to achieve clear expert specialization. To address these challenges, we propose CoRe-MoE, a two-stage reinforcement learning framework that decouples gait generation from terrain adaptation. In the first stage, a stable locomotion policy is learned to produce natural walking and running behaviors with smooth transitions. In the** 

**second stage, a terrain-aware MoE branch is introduced, and the gating network is trained with a contrastive objective to learn structured terrain representations and promote expert specialization. The final action is obtained through weighted fusion of the base gait policy and the terrain-aware branch, enabling the policy to preserve stable locomotion while adapting to complex terrains. Extensive simulation results demonstrate that the proposed method outperforms baseline approaches in terms of success rate, locomotion stability, and multi-terrain adaptability. Furthermore, zero-shot deployment on a Unitree G1 humanoid robot validates the effectiveness of our framework, achieving robust walking and running across stairs, slopes, steps, obstacles, and unstructured outdoor terrains while maintaining accurate foothold control and dynamic stability.** 

**_Index Terms_ —humanoid locomotion, gait adaptation, reinforcement learning, contrastive learning, mixture of experts.** 

## I. INTRODUCTION 

**H** UMANOIDtasks in real-worldrobots areenvironments,increasinglywhichrequiredoftento performcontain 

tasks in real-worldrobots environments,increasinglywhichrequiredoftentowhichrequiredoftentooftento contain abrupt terrain variations such as stairs, slopes, and steps. Compared with wheeled robots [1], [2], humanoids can step over obstacles and traverse discontinuous terrains, making them more suitable for deployment in human-centered environments [3], [4], [5], [6]. To achieve robust and human-like locomotion in such scenarios, robots must not only maintain basic stability but also proactively adjust their actions according to upcoming terrain changes [7], [8]. 

Humans rely primarily on two fundamental gaits: walking and running to adapt to complex terrains [9], [10], rarely employing additional complex or ineffective gaits to cross stairs, slopes, or gaps. This observation provides a design insight for humanoid robots: control strategies should focus on smooth switching between walking and running, rather than learning numerous artificial gait types[11], which contribute little to practical adaptability. 

Despite the significant progress in reinforcement learning–based humanoid locomotion, key challenges remain. Pure proprioception–based “blind locomotion” methods can resist moderate disturbances through contact feedback [12], [13], [14], [15], but their reactive nature makes it difficult for the robot to anticipate hazards such as high steps or deep gaps. On the one hand, this can lead to instability or falls on critical terrains; on the other hand, jointly achieving gait switching and multi-terrain adaptation within a single policy often induces gradient conflicts, while the visual and dynamic variations introduced by complex terrains further increase learning difficulty. 

In addition, Mixture-of-Experts (MoE) architectures [16] have shown promising potential in multi-skill learning and have been gradually applied to humanoid locomotion and multi-terrain adaptation [17], [11]. However, during direct training, the experts often fail to develop clear specialization: their activation patterns tend to be dispersed and highly overlapping across different terrains or gait conditions, preventing the policy from fully exploiting the advantages of the MoE structure and limiting its multi-terrain adaptability and gait control precision. 

To address these issues, we propose the Contrastive Reweighted Mixture of Experts (CoRe-MoE), a two-stage training framework that integrates adaptive gait policies, visual perception, and contrastive MoE learning. Depth images [3], [18] are incorporated to enable proactive, terrain-aware motion adjustment. In the first stage, the policy learns stable walking and running on flat terrains and acquires natural and smooth gait transition capabilities. In the second stage, we introduce a terrain-aware MoE branch guided by SwAV-style contrastive learning [19]. This encourages the network to learn structured terrain representations and promotes expert specialization. The final action is produced by a weighted fusion of the base gait 

policy and the terrain-aware branch, enabling robust multiterrain adaptability while preserving stable fundamental gait behaviors. 

As illustrated in Figure 1, CoRe-MoE achieves continuous, natural transitions between walking and running within a single policy while maintaining stable performance on complex terrain. In contrast, existing methods—such as Hiking in the Wild—train walking and running separately and require manual switching during execution, leading to abrupt transitions, poor continuity, and degraded stability when terrain conditions change. 

Simulation results demonstrate that CoRe-MoE outperforms baseline methods in terms of success rate, gait stability, and multi-terrain adaptability. Further zero-shot deployment experiments on the Unitree G1 robot show that the policy achieves robust locomotion across stairs, slopes, and outdoor natural terrains, while maintaining accurate foot placement and dynamic stability under external disturbances, highlighting its potential for real-world applications. 

The main contributions of this work are summarized as follows: 

- We propose CoRe-MoE, a two-stage end-to-end training framework that enables smooth switching between walking and running while achieving multi-terrain adaptability and robustness. 

- We design a terrain-aware MoE module based on contrastive learning that generates terrain-conditioned action adjustments and promotes clear expert specialization in different terrains. 

- We perform a zero-shot deployment on the Unitree G1 robot, and the results demonstrate robust locomotion and dynamic stability across stairs, slopes, and natural outdoor terrains. 

TABLE I: Comparison of locomotion capabilities across different methods. Unlike prior approaches that support limited gaits or require policy switching, CoRe-MoE is the first unified policy achieving walking, running, smooth transitions, and robust multi-terrain performance. 

|**Method**|**Walk **|**Run**<br>**Auto **|**Transition **|**Terrain Adapt**|
|---|---|---|---|---|
|Beamdojo [6]|✓|✗|✗|✓|
|Now You See That [20]|✓|✗|✗|✓|
|MoRE [11]|✓|✓|✗|✓|
|Hiking in the Wild [3]|✓|✓|✗|✓|
|**CoRe-MoE**|✓|✓|✓|✓|


II. RELATED WORK 

## _A. Learning-based Humanoid Robot Control_ 

Reinforcement learning (RL) has recently achieved substantial progress in humanoid locomotion. RL-based policies can learn stable walking and running behaviors directly from proprioceptive feedback and maintain robustness on moderately challenging terrains [21], [22], [12], [23]. Compared to traditional model-based controllers [24], [25], [26], these learning-based approaches are capable of handling unknown 


Fig. 2: Overview of our framework. In Stage 1, we learn a flat-terrain adaptive gait policy using MoE and AMP, enabling stable walking–running transitions. In Stage 2, we incorporate depth perception and employ MoE with contrastive learning to acquire terrainaware control. During inference, the flat-terrain policy provides a gait prior and the multi-terrain policy applies terrain adjustments; their weighted fusion produces the final action, achieving natural gait and multi-terrain adaptability. 

dynamics and unstructured environments, leading to significantly improved adaptability. 

Although prior works have explored multi-gait or multiterrain locomotion [11], [17], [27], their policies often rely on manually triggered gait switches and cannot autonomously adjust gait according to speed or terrain commands. Their generalization across fundamentally different terrain types such as stairs, gaps, and obstacles also remains limited, as shown in Table I. 

Human locomotion studies show that people primarily rely on only two fundamental gaits—walking and running—to traverse diverse terrains, without resorting to additional artificial or inefficient gait patterns. This observation suggests that practical humanoid locomotion should emphasize autonomous and smooth transitions between these two core gaits while simultaneously maintaining strong multi-terrain adaptability. 

## _B. Perception for Locomotion_ 

In recent years, researchers have incorporated exteroceptive perception into humanoid locomotion policies [20], [28], [1], [6], [29]to enhance proactive adaptation to complex terrains. Blind locomotion methods, which rely solely on proprioceptive signals, can maintain stability on limited terrains but cannot anticipate upcoming terrain features. Traditional LiDAR-based approaches can provide height information [30], [7], [31], but their limited field-of-view, especially under the robot’s feet, combined with state estimation drift, low update frequency, and motion distortion, restricts their effectiveness in high-speed or dynamic scenarios [32], [6]. In contrast, depth cameras provide high-frequency perception and can 

be integrated with policy networks for end-to-end control[3], [33], [18], enabling the robot to proactively adjust its actions to handle complex terrains, thereby improving safety and adaptability. 

## _C. Multi-terrain Adaptation and Mixture-of-Experts_ 

Mixture-of-Experts architectures [16], [34] offer an effective approach for multi-skill learning and multi-terrain adaptation. By dividing the policy into specialized experts, the robot can learn distinct skills such as walking, running, and gapcrossing[11], [17]. However, during direct training, expert activations are often dispersed and lack specialization, limiting the policy’s ability to adapt across different terrains. Contrastive learning methods, such as SwAV [19] and SimCLR [35], can guide experts to specialize according to terrain conditions, enhancing both policy robustness and multi-terrain adaptability. Our proposed CoRe-MoE framework combines weighted action correction with contrastive MoE learning, preserving gait stability while enabling proactive adaptation and flexible control over complex terrains. 

## III. METHOD 

To address the coupled challenges of terrain disturbances and gait transitions, we aim for humanoid robots to maintain stable dynamics while achieving natural and continuous gait switching in complex environments. We adopt a two-stage training pipeline: the first stage focuses on learning stable and controllable fundamental gaits such as walking and running; the second stage extends the objective to enable multi-terrain adaptation while preserving a consistent anthropomorphic motion style, as illustrated in Figure 2. This staged design 

improves training stability and allows the robot to perform smooth and coherent gait transitions across diverse terrains. 

## _A. Problem Description_ 

We formulate humanoid multi-terrain locomotion as a Partially Observable Markov Decision Process (POMDP) with a tuple _⟨S, A, P, R, γ⟩_ , where _S_ is the state space, _A_ is the action space, _P_ ( _|s, a_ ) is the transition function. The agent receives a reward from _R_ ( _s, a_ ). The discount factor _γ ∈_ [0 _,_ 1] balances immediate and future rewards. We use Proximal Policy Optimization (PPO) [36] to learn the optimal policy _π_<sup>_∗_</sup> that maximizes the expected discounted return: 


We adopt an asymmetric actor–critic architecture. The policy network relies solely on deployable, non-privileged proprioceptive observations, defined at time t as: 


including robot angular velocity _ωt_ , gravity direction _gt_ , velocity command _c_<sup>_t_</sup> _v_<sup>, joint angle</sup><sup>_θt_, velocity</sup><sup>_θ_˙</sup><sup>_t_, last action</sup><sup>_at−_1.</sup> In addition, the policy also receives the perception observation depth image _It_ . The critic receives the same observation as the actor but is additionally provided with privileged base linear velocity _vt_ . 

## _B. Adaptive Gait Locomotion Policy_ 

In the first training stage, we aim to learn a stable and controllable locomotion policy that enables the humanoid robot to adaptively switch between walking and running on flat terrain. We employ two separate Adversarial Motion Priors (AMP) [37] networks, one for walking and one for running. Additionally, the walking trajectories are augmented with gait samples such as stair climbing and obstacle crossing to further enhance gait diversity and adaptability. 

The policy adopts MoE architecture with historical frame inputs _Ot_<sup>_H_</sup> to capture temporal dependencies. It is important to note that the depth image _It_ is not used in this stage; locomotion control on flat terrain relies solely on proprioceptive observations to achieve gait switching. The MoE gating network takes the commanded velocity _c_<sup>_t_</sup> _v_<sup>asinputand</sup> dynamically activates different experts, enabling the walking AMP under low-speed commands and the running AMP under high-speed commands. The final action is computed as a weighted sum of expert outputs through softmax gating: 


where _zi_ means the _i_ -th expert outputs and _gi_ is the expert activation. 

The training reward consists of three terms, combined as 


where _ramp_ is provided by the activated AMP network to enforce realistic walking or running motions, _rtask_ ensures 

locomotion stability and that the commanded velocity is achieved, _rreg_ is a regularization term that penalizes large or abrupt joint motions to promote smooth and physically plausible actions. By optimizing this combined reward, the policy learns to smoothly transition between walking and running, achieving natural and continuous gait adaptation while maintaining dynamic stability on flat terrain. After completing Stage 1 training, the entire policy network is frozen. 

## _C. Adaptive Multi-Terrain Policy_ 

In the second training stage, we introduce a multi-terrain policy on top of the adaptive gait policy learned in Stage 1 to enhance locomotion performance on complex terrains. This policy is built using a MoE architecture, where each expert receives not only historical proprioceptive observations _Ot_<sup>_H_</sup> but also the corresponding historical depth image sequence _It_<sup>_H_, allowing the model to capture both temporal dynamics and</sup> external terrain geometry. During this stage, the Stage 1 policy network is frozen, and the actions generated by the Stage 2 policy are added to those from Stage 1, enabling terrainaware fine-grained adjustments while preserving the stable gait foundation learned previously. The reward function in this stage retains only the task reward _rtask_ and regularization reward _rreg_ , ensuring the policy focuses on terrain adaptation while maintaining smooth and physically consistent actions. 

To fully activate experts and encourage terrain-specific specialization, we adopt a SwAV-based contrastive learning objective that aligns the gating output with the encoded representation of the history of the depth image. Compared with single-frame information, the historical depth sequence provides more stable and structured cues about terrain geometry, enabling the gating network to form clearer terrain clusters. We align the gating embedding _gt_<sup>_z_withthedepth</sup> history representation _d_<sup>_z_</sup> _t−H_ : _t_ 


During each iteration, we collect batch trajectories from all environments. If a historical observation and its corresponding historical depth sequence belong to the same trajectory, they form a positive pair; otherwise, they are negative. The gate network output _gt_ serves as the source vector _I_ source<sup>_t_, while the</sup> encoded representation of the historical depth sequence _d_<sup>_z_</sup> _t−H_ : _t_ serves as the target vector _I_ target<sup>_z_.Bothvectorsarenormalized</sup> before computing the contrastive objective. 

To predict the cluster assignment probabilities, we first normalize the prototype matrix: 


and compute the source and target probabilities: 


Fig. 3: Sensitivity analysis of the action fusion coefficients _ϵlower_ and _ϵupper_ . Colors indicate the success rate under multi-terrain evaluation. 

where _τ_ is a temperature parameter. To avoid trivial solutions, the Sinkhorn-Knopp algorithm is applied to both source and target probabilities to obtain target distributions _q_ target<sup>_tq_</sup> source<sup>_t_.</sup> The final SwAV contrastive loss is: 


By aligning the embedding of the gating with the historical depth representation, the SwAV objective enables the gating network to better discriminate variations in terrain. As a result, different terrain types induce distinct cluster assignments, which in turn encourage the MoE experts to develop specialized behaviors. With more accurate expert activation, the policy is able to produce terrain-aware corrections rather than generic modifications. The MoE-weighted action: 


which reflects the specific adjustments required by the upcoming terrain. 

For action fusion, we apply different blending coefficients to different body parts to control the influence of terrain-aware corrections: _ϵupper_ = 0 _._ 1 for the upper body and _ϵlower_ = 0 _._ 5 for the lower body. The final action is defined as: 


where _ϵ_ is applied per body region accordingly. This design preserves the stable gait structure learned in Stage 1 while adding fine-grained, terrain-dependent refinements. 

To investigate the influence of the fusion coefficients, we further performed a sensitivity analysis on _ϵupper_ and _ϵlower_ , as shown in Fig. 3. The results indicate that the policy is more sensitive to _ϵlower_ , highlighting the dominant role of terrain-aware corrections of the lower-body in the adaptation 

of the foothold and the traversal of the terrain. When _ϵlower_ is too small, the policy cannot respond effectively to terrain variations, whereas excessively large values may introduce overly aggressive corrections that compromise gait stability. In contrast, _ϵupper_ has a relatively smaller impact on overall performance. The results show that the adopted configuration lies within a high-performance region, indicating that the proposed action fusion mechanism achieves a favorable balance between locomotion stability and terrain adaptability. 

Through this mechanism, the multi-terrain branch serves as a lightweight yet effective adaptation layer, driven by contrastively shaped gating behavior, enabling robust locomotion across diverse and uneven terrains. 

## IV. EXPERIMENT CONFIGURATIONS 

## _A. Training Parameters_ 

We train all policies in NVIDIA Isaac Sim and Isaac Lab [38] 4096 parallel environments to ensure stable gradient estimates and rapid throughput. Motion priors are constructed from selected AMASS [39] and LAFAN [40] sequences, retargeted to the Unitree G1 model and used to supervise the AMP discriminator. The first-stage adaptive gait policy is trained for 25k iterations on an RTX 4090 GPU with a 2-expert MoE, while the second-stage residual multi-terrain policy is trained for 20k iterations with the MoE capacity expanded to 8 experts. For the contrastive learning module, we set the number of prototypes at 16 and the temperature at 0.1. Depth image preprocessing, including downsampling and spatial cropping, follows the procedure referenced in [3], ensuring consistent perceptual inputs across simulation and real-world deployment. 

## _B. Reward Functions_ 

Our reward formulation is based on standard locomotion objectives while incorporating two essential safety considerations. The first focuses on preventing missteps in unsupported terrain regions [6], ensuring that the policy avoids foot placements that could lead to immediate loss of balance. The second integrates a scalable terrain-edge detection module with footvolume contact evaluation [3], encouraging the robot to land within a safe foothold margin and reducing the likelihood of edge-related slips. A complete description of all reward terms is provided in Table II. 

## _C. Domain Randomization_ 

To improve the real-world generalization of the learned policy, we introduce moderate domain randomization during training across dynamics, depth perception, and command inputs. This includes small perturbations to physical properties such as mass and friction, staged noise applied to ray-cast depth observations, and mild variations in velocity and heading commands. Periodic external forces are also applied to enhance disturbance robustness. Together, these randomizations strengthen the policy’s stability in real-world settings, with the detailed configurations summarized in Table III. 

TABLE II: Reward Functions for Humanoid Locomotion 

|**Term**|**Equation**|**Weight**|
|---|---|---|
|Velocity tracking|exp(_−∥_**v**_xy −_**v**<sup>_c_</sup><br>_xy_<sup>_∥_2</sup><br>2<sup>_/σ_2)</sup><br><br>|2_._0|
|Yaw tracking|exp(_−∥ωz −ω_<sup>_c_</sup><br>_z_<sup>_∥_2</sup><br>2<sup>_/σ_2)</sup><br>|2_._0|
|Heading error<br>|_∥ψ −ψ_<sup>_c_</sup>_∥_<sup>2</sup><br>2<br>|_−_1_._0<br>|
|Is alive|1<br>|3_._0|
|Stand still|I(_∥_**v**<sup>_c_</sup>_∥< ϵ_)_∥_**v**_∥_<sup>2</sup><br>2|_−_0_._3|
|Don’t wait|I(_∥_**v**<sup>_c_</sup>_∥> ϵ_)I(_∥_**v**_∥< δ_)|_−_0_._5|
|Orientation|_∥_**g**_xy∥_<sup>2</sup><br>2<br>|_−_3_._0|
|Pelvis orientation|_∥_**q**err,pelvis_∥_<sup>2</sup><br>2<br>|_−_3_._0|
|Angular velocity|_∥_**_ω_**_xy∥_<sup>2</sup><br>2<br><br>|_−_0_._05|
|Joint deviation hip|�<br>_i∈_hip<sup>(</sup><sup>_θi −θ_def</sup><br>_i_ <sup>)2</sup><br>|_−_0_._5|
|Freeze upper body|�<br>_i∈_upper <sup>_|θi −θ_def</sup><br>_i _<sup>_|_</sup><br>|_−_0_._004|
|Feet air time|�<br>_i _<sup>_t_air</sup><sup>_,i_</sup><br>|0_._5|
|Feet slide|�<br>_i _<sup>_∥_</sup><sup>**v**</sup><sup>_i,xy∥_2</sup><br>2 <sup>I(contact</sup><sup>_i_)</sup><br>|_−_0_._4|
|Feet at plane|�<br>_i_<sup>(</sup><sup>_zi −z_plane)2</sup><br>|_−_0_._1|
|Feet flat orientation|�<br>_i _<sup>_∥_</sup><sup>**q**</sup><sup>_i,_err</sup><sup>_∥_2</sup><br>2 <sup>I(contact</sup><sup>_i_)</sup><br><br>|_−_0_._4|
|Feet close|exp(_−d_<sup>2</sup><br>_xy_<sup>_/σ_2)</sup>|0_._4|
|Foothold penalty|�<br>_i∈{_L_,_R_}_ <sup>I(</sup><sup>_ci_ = 1)I(</sup><sup>_hi < h_thr)</sup><br>|_−_2_._0|
|Volume penetration|�max(0_, z_terrain_−z_point)<br><br>|_−_5_._0|
|Undesired contacts|�<br>_i_ <sup>I(</sup><sup>_∥_</sup><sup>**F**</sup><sup>_i∥_2</sup> <sup>_> F_thr)</sup><br>|_−_1_._0<br>|
|Joint torques|�<br>_i _<sup>_τ_ 2</sup><br>_i_<br><sup>¨</sup>|_−_1_._5_e_<sup>_−_7</sup><br>|
|Joint acceleration|�<br>_i_ <sup>_θ_2</sup><br>_i_<br><sup>˙</sup>|_−_1_._25_e_<sup>_−_7</sup>|
|Joint velocity|�<br>_i_ <sup>_θ_2</sup><br>_i_<br>|_−_1_._0_e_<sup>_−_4</sup>|
|Action rate|_∥_**a**_t −_**a**_t−_1_∥_<sup>2</sup><br>2<br>|_−_0_._005<br>|
|Energy|�<br>_i _<sup>_P_ 2</sup><br>_i_|_−_5_._0_e_<sup>_−_5</sup>|
|CoT penalty|<br><br>�<br>_i _<sup>_|τi_ ˙</sup><sup>_qi| /_ (</sup><sup>_mg∥_</sup><sup>**v**</sup><sup>_∥_)</sup>|_−_0_._05|
|Joint pos limits|<br>�<br>_i_ <sup>ReLU(</sup><sup>_θi −θ_max) +</sup><br>ReLU(_θ_min_−θi_)<br><sup>˙˙</sup>|_−_1_._0|
|Joint vel limits|�<br>_i_ <sup>ReLU(</sup><sup>_|_ </sup><sup>_θi| −θ_max)</sup><br><br>|_−_1_._0|
|Torque limits|�<br>_i_ <sup>ReLU(</sup><sup>_|τi|/τ_max</sup><sup>_−_0</sup><sup>_._8)</sup>|_−_0_._01|
|AMP reward|_−_log<br>�<br>1_−Dϕ_(**s**_t_)<br>�|0_._25|


## _D. Curriculum Learning_ 

To improve the policy’s adaptability to complex terrains, we adopt a curriculum learning strategy. During training, the environment is divided into 10 levels, and the curriculum level is dynamically increased based on the achieved velocity reward. Higher levels correspond to larger commanded target velocities and progressively more challenging terrains. This design guides the policy to learn robust locomotion behaviors in a gradual and structured manner. 

TABLE III: Parameters for Domain Randomization During Training 

|**Term**|**Randomization Range**|
|---|---|
|Static Friction|[0.1, 3.0]|
|Dynamic Friction|[0.1, 3.0]|
|Ground Restitution|[0.05, 0.5]|
|Base Mass Offset|[-5.0, 5.0]|
|_Kp_ Scale|[0.9, 1.1]|
|_Kd_ Scale|[0.9, 1.1]|
|Base Orientation Reset|[-0.1, 0.1]|
|Linear Velocity Reset|[-0.2, 0.2]|
|Angular Velocity Reset|[-0.2, 0.2]|
|Linear Velocity Perturbation|[-0.2, 0.2]|
|Initial Joint Positions|[-0.15, 0.15]|
|Initial Joint Velocities|[0.0, 0.1]|
|Crop & Resize|[18, 0, 16, 16]|
|Gaussian Noise|_σ_ = 0_._02, range [0.12, 1.2]|
|Disparity Artifact Synthesis|_P_mask = 0_._05%|
|Depth Gaussian Blur|kernel size = 3_×_3, _σ_ = 1_._0|
|Depth Range Normalization|[0.0, 2.5] _→_[0.0, 1.0]|
|OOD Perturbation Probability|_P_ood = 0_._02%|


## V. EXPERIMENTS 

In this section, we evaluate the robustness and performance of our two-stage adaptive locomotion framework through extensive experiments in both simulation and real-world environments. The policy is tested across flat and complex terrains, including stairs, platforms, slopes, and discrete gaps, summarized in Table IV, using both walking and running gaits. All quantitative results are reported as the mean and standard deviation (mean ± std) over multiple evaluation runs. Our evaluation aims to answer the following three questions: 

- **Q1** : In Stage 1, can the adaptive gait locomotion policy learn natural walking and running gaits on flat terrain, while enabling smooth transitions between them? 

- **Q2** : In Stage 2, can the depth perception policy branch with contrastive learning enable stable locomotion and terrain-aware motion adjustment on complex terrains through action fusion with the Stage 1 policy? 

- **Q3** : Can the trained policy be reliably deployed on physical hardware in a zero-shot manner, without additional fine-tuning? 

TABLE IV: Terrain Types and Corresponding Parameter Ranges 

|**Terrain Type**|**Terrain Feature**|**Range**|
|---|---|---|
|Flat Ground|Flat terrain with mild variations|0.0–0.1m|
|Up Slope|Upward inclined terrain|0.0–35.0<sup>_◦_</sup>|
|Down Slope|Downward inclined terrain|0.0–35.0<sup>_◦_</sup>|
|Up Stairs|Standard stair ascent terrain|0.0–0.2m|
|Down Stairs|Standard stair descent terrain|0.0–0.2m|
|High Up Stairs|Steep and tall stair ascent terrain|0.0–0.45m|
|High Down Stairs|Steep and tall stair descent terrain|0.0–0.45m|
|High Obstacle|Tall single-step obstacle terrain|0.1–0.4m|
|Random Obstacle|Randomly distributed obstacle terrain|0.1–0.3m|


## _A. Evaluation of the Adaptive Gait Locomotion Policy_ 

We compared the proposed Adaptive Gait Locomotion Policy with three baseline methods: **(1) Mixed AMP** : which merges walking and running datasets to train a single AMP network; **(2) Sel AMP** : which selects walking or running references based on the commanded velocity to train a single AMP network; **(3) w/o MoE** : a single actor-critic network without using the MoE architecture. 

To evaluate the performance of the Stage-1 adaptive gait policy on flat terrain, the robot receives distance-based velocity commands while navigating toward target points. When far from the target, the commanded velocity increases in the range of 1 to 2.5 m/s to induce a running gait, while near the target the velocity gradually decreases in the range of 0 to 1 m/s to produce a walking gait. This setup examines whether the policy can generate natural walking and running gaits and achieve smooth gait transitions on flat ground. 

Locomotion performance was evaluated using four metrics: (1) **Velocity Tracking Score (Vel. Score.)** : An averaged exponential kernel score computed from the squared error between the commanded and actual base linear velocities in the xyplane. (2) **Success Rate (Succ.)** : The percentage of trials in which the robot successfully reaches the specified target point; 


Fig. 4: Side-view gait sequence visualization results. CoRe-MoE exhibits the most natural gait. 

(3) **Average Traversal Ratio (Dist.)** : The fraction of the target distance completed before reaching the goal or termination; (4) **Side-view Gait Sequencess** : Visual inspection of the robot’s side-view motion sequences to assess the naturalness and smoothness of the walking and running gaits. 

As shown in Table V, CoRe-MoE achieves the highest velocity tracking score, success rate, and traversal ratio. Moreover, the relatively small standard deviations indicate that the proposed policy maintains consistent performance across different evaluations. 

The side-view gait sequences in Figure 4 further reveal the differences among the policies. For Mixed AMP, merging walking and running data into a single network causes it to learn an intermediate shuffling gait between walking and running, resulting in unnatural motion. Sel-AMP, although selecting the corresponding reference data based on the commanded velocity, often incorrectly increases stride length under high-speed commands, producing an unnatural over-stride behavior. This leads to unstable mixed gait characteristics and prevents the emergence of clear walking or running patterns. In addition, both baseline methods exhibit unnatural arm movements. 

In contrast, CoRe-MoE employs separate AMP experts for walking and running and dynamically selects them based on the commanded velocity, enabling the policy to learn distinct walking and running gaits at low and high speeds. Moreover, modeling each gait with its own expert results in more natural and coherent arm swings, yielding significantly better gait continuity and adaptability compared to the baselines. We strongly recommend watching the demonstration videos on our project homepage for a more intuitive understanding. 

TABLE V: Performance Comparison of Adaptive Gait Policy and Baseline Methods on Flat Ground 

|**Method**|**Vel. Score.**|**Succ.**|**Dist.**|
|---|---|---|---|
|Mixed AMP|0_._796_±_0_._008|96_._12_±_0_._37%|97_._60_±_0_._29%|
|Sel AMP|0_._812_±_0_._015|54_._20_±_1_._84%|54_._50_±_1_._67%|
|w/o MoE|0_._817_±_0_._007|97_._06_±_0_._31%|98_._41_±_0_._24%|
|**CoRe-MoE**|**0**_._**853**_±_**0**_._**004**|**99**_._**13**_±_**0**_._**15**%|**99**_._**85**_±_**0**_._**08**%|


## _B. Evaluation of the Adaptive Multi-Terrain Policy_ 

We compare the proposed Adaptive Multi-Terrain Policy with five baseline variants to analyze the contribution of each key component: **(1) w/o MoE** : removing the MoE architecture; **(2) Masked Expert** : zeroing out the outputs of activated experts; **(3) w/o Fusion** : removing the second-stage policy branch and directly fine-tuning the Stage 1 policy on multiterrain tasks; **(4) w/o SwAV** : removing SwAV-based contrastive learning; **(5) SimCLR** : using instance-level SimCLR contrastive learning instead of SwAV. 

To evaluate the policy under complex terrain conditions, the robot is deployed on diverse terrains including stairs, slopes and obstacle. We retain the same distance-dependent velocity setting used in Stage 1 to create mixed walking–running scenarios. The key distinction is that this stage focuses on assessing stability under terrain-induced disturbances and determining whether the policy can leverage the second-stage policy branch and the contrastively trained MoE gating mechanism to generate terrain-aware corrective actions for robust traversal over challenging terrains. 

Locomotion performance was quantified using multiple metrics: **(1) Success rate (Succ.)** : The percentage of trials in which the robot successfully reached the target point; **(2) Average Traversal Ratio (Dist.)** : The fraction of the target distance completed before reaching the goal or termination; **(3) Convergence time (Conv. Time)** : The number of training iterations required for the policy to reach stable performance; **(4) Discriminability of terrain features** : evaluated via t-SNE [41] visualization of MoE gating outputs to assess how well the embeddings differentiate between different terrain types. 

As shown in Table VI and Figure 5, (1) w/o MoE exhibits a significant drop in success rate and traversal ratio across most terrains, indicating that MoE plays a central role in expert decomposition and policy specialization; (2) Masked Expert severely degrades performance by zeroing out activated expert outputs, further validating the importance of correct expert selection for terrain-aware control; (3) w/o Fusion shows reduced stability in complex multi-terrain scenarios and 


Fig. 5: Evolution of Mean Reward and Terrain Curriculum Level Across Training Iterations 

TABLE VI: Ablation Study of CoRe-MoE with Multi-Terrain Locomotion Performance Analysis. All results are reported as mean values over evaluation episodes. Standard deviations are omitted for clarity. 

|**Method**|**Flat Ground**|**Up Slope**|**Down Slope**|**Up Stairs**<br>**Down**|**Stairs**|**High Up Stairs**|**High Down Stairs**<br>**High O**|**bstacle**|**Random Obstacle**|
|---|---|---|---|---|---|---|---|---|---|
||Succ. Dist.|Succ. Dist.|Succ. Dist.|Succ. Dist.<br>Succ.|Dist.|Succ. Dist.|Succ. Dist.<br>Succ.|Dist.|Succ. Dist.|
|w/o MoE|97.6% 99.5%|76.4% 82.6%|79.1% 86.1%|35.6% 54.7%<br>40.7%|63.2%|12.2% 30.1%|16.7% 38.9%<br>23.5%|41.3%|29.8% 46.2%|
|Masked Expert|19.2% 32.6%|4.9% 19.3%|15.6% 27.4%|2.1% 6.7%<br>9.4%|24.7%|0.2% 2.3%|4.3% 15.6%<br>7.6%|21.0%|3.5% 12.5%|
|w/o Fusion|98.7% 99.8%|81.2% 87.6%|86.3% 93.7%|36.3% 58.6%<br>51.8%|70.4%|9.4% 24.8%|17.5% 42.3%<br>26.1%|43.4%|35.4% 58.5%|
|w/o SwAV|99.5% 99.9%|96.4% 98.5%|98.2% 99.4%|84.6% 92.3%<br>86.3%|93.6%|72.3% 85.1%|79.5% 87.2%<br>90.2%|96.9%|81.5% 89.6%|
|SimCLR|99.7% 99.9%|97.3% 99.1%|98.6% 99.7%|87.6% 94.3%<br>89.4%|94.2%|76.8% 89.3%|81.6% 90.3%<br>93.4%|97.5%|83.6% 91.4%|
|**CoRe-MoE**|**99.9% 99.9%**|**98.7% 99.4%**|**98.9% 99.9%**|**94.3% 96.8%**<br>**96.5% **|**97.9%**|**86.4% 91.6%**|**87.1% 93.7%**<br>**97.6% **|**98.7%**|**89.3% 92.8%**|


Fig. 6: T-SNE visualization of MoE gating features across different terrains. The left figure (w/o SwAV) shows mixed and overlapping feature distributions, while the right figure (CoRe-MoE) presents more compact and clearly separated clusters. 

performs reasonably only on structurally simple terrains such as stairs, demonstrating that this fusion mechanism is essential for cross-terrain generalization; (4) w/o SwAV leads to lower success rate and slower convergence, suggesting that SwAV contrastive learning helps the MoE gating network better distinguish terrain features and accelerate policy optimization; (5) SimCLR performs better than w/o SwAV on most terrains but still underperforms CoRe-MoE overall, indicating that although instance-level contrastive learning improves representation quality, it lacks structured terrain semantic modeling capability and cannot form effective cluster-level alignment between terrains and experts, thereby limiting its effectiveness in MoE expert selection. 

In contrast, CoRe-MoE consistently achieves the highest success rates and traversal ratios across all evaluated terrains, demonstrating superior robustness and generalization capability. Nevertheless, a small number of failures still occur in the most challenging scenarios, particularly on High Up Stairs and Random Obstacle terrains. We attribute these failures primarily to the abrupt terrain height variations and limited foothold margins in highly irregular environments, where small perception or foot-placement errors can accumulate and eventually lead to loss of balance. 

Figure 6 presents t-SNE visualizations of MoE gating outputs across different terrain types. We specifically conducted this experiment to verify the effect of SwAV contrastive learning on terrain feature encoding. The embeddings with SwAV show clearly separated clusters for each terrain type, while embeddings without SwAV exhibit more overlap, indicating reduced discriminability. These results demonstrate that contrastive learning enables the gating network to more effectively distinguish terrain features and activate the corresponding 

experts for terrain-aware motion adjustments. 

Overall, the proposed CoRe-MoE demonstrates superior robustness and stability in multi-terrain locomotion tasks, and achieves more reliable locomotion performance under complex terrain conditions. 

## _C. Comparison with Prior Locomotion Methods_ 

To further evaluate the proposed method, we compared CoRe-MoE with representative humanoid locomotion frameworks, including Hiking in the Wild [3] and MoRE [11]. For concise presentation, the reported stair, slope, and obstacle success rates are averaged over the corresponding terrain variants, including both ascending and descending cases as well as different difficulty levels. 

As shown in Table VII, Hiking in the Wild trains separate walking and running policies and requires manual switching during deployment, while MoRE employs a single policy but still relies on manually specified gait motion modes. Such approaches struggle to continuously adapt locomotion behaviors according to motion demands, limiting both adaptability and energy efficiency across a wide range of velocities. For example, using only a walking policy becomes inefficient at high speeds, whereas relying solely on running introduces unnecessary energy expenditure at low speeds. Moreover, manually specified motion modes cannot always guarantee optimal gait selection under varying terrain and velocity conditions. 

In contrast, CoRe-MoE achieves unified walking and running control within a single policy and automatically performs gait transitions according to commanded velocities. In addition to the simplified policy structure, CoRe-MoE achieves the best overall locomotion performance, obtaining the highest velocity tracking score and success rates across multiple terrain categories. Furthermore, CoRe-MoE achieves the lowest Cost of Transport (CoT), indicating superior energy efficiency during locomotion. This advantage stems from the automatic walk run transition mechanism, which enables the policy to employ energy-efficient walking at low speeds, switch to more suitable running behaviors at high speeds, and smoothly transition between the two regimes in intermediate velocity ranges. As a result, CoRe-MoE avoids the efficiency loss associated with relying on a single locomotion mode across all velocities. These results demonstrate that the proposed framework effectively combines unified gait generation, automatic gait transition, energy-efficient locomotion, and robust multi-terrain traversal within a single policy architecture. 

TABLE VII: Comparison of Policy Structures and Multi-Terrain Locomotion Performance Across Methods. 

|**Method**|**Unified Policy**|**Transition Mode**|**Vel. Score.**|**Flat Succ.**|**Slope Succ.**|**Stairs Succ.**|**Obstacle Succ.**|**CoT**|
|---|---|---|---|---|---|---|---|---|
|Hiking in the Wild(Walk)|✗|Manual|0_._85_±_0_._02|99_._7_±_0_._2%|76_._8_±_0_._8%|82_._6_±_0_._7%|84_._9_±_0_._6%|0_._75_±_0_._02|
|Hiking in the Wild(Run)|✗|Manual|0_._62_±_0_._03|99_._4_±_0_._3%|67_._9_±_1_._1%|54_._7_±_1_._4%|78_._5_±_0_._9%|0_._67_±_0_._02|
|MoRE|✓|Manual|0_._79_±_0_._02|97_._6_±_0_._4%|93_._7_±_0_._5%|90_._3_±_0_._6%|91_._2_±_0_._5%|0_._82_±_0_._03|
|**CoRe-MoE**|✓|**Automatic**|**0**_._**89**_±_**0**_._**01**|**99**_._**9**_±_**0**_._**1**%|**98**_._**8**_±_**0**_._**3**%|**91**_._**1**_±_**0**_._**4**%|**93**_._**5**_±_**0**_._**3**%|**0**_._**61**_±_**0**_._**01**|


Fig. 7: The multi-terrain sequence demonstrates the robot’s continuous locomotion across six representative terrains, where A-F correspond to obstacle ascent, obstacle descent, slope ascent, flat ground, stair descent, and stair ascent. The robot smoothly transitions between different terrains while maintaining stable gait and reliable foothold control, demonstrating strong multi-terrain adaptability. 


Fig. 8: Side-view gait sequence of the humanoid robot in real world deployment, showing a continuous transition from walking to running and back to walking without any mode switching. 

## _D. Real-world Experiment_ 

To validate the generalization capability of the proposed method CoRe-MoE on real robotic hardware, we directly deployed the trained policy onto the Unitree G1 humanoid robot without any additional fine-tuning. The system uses the onboard Intel RealSense D435i depth camera to capture realtime depth images, which are processed through lightweight geometric operations and fed into the policy network, enabling zero-shot transfer from simulation to the real robot. 

All experiments are conducted in real outdoor environments, including uneven ground, natural steps, outdoor obstacles, natural slopes, and terrains with height discontinuities. Despite significant discrepancies in geometry, surface materials, and lighting conditions compared to simulation, the robot consistently maintains stable locomotion with accurate foothold placement. 

As shown in Figure 8, the robot executes a continuous sequence consisting of walking, running, and returning to 


Fig. 9: The robot is subjected to a sudden external impact while running, maintaining balance and quickly recovering stable locomotion. 

walking on flat ground. This experiment highlights the natural and coherent behavior of CoRe-MoE under varying velocity commands. Since the framework is trained as a single unified policy, the robot automatically adjusts its gait as speed increases or decreases, without relying on any manually triggered mode-switching mechanism. Even during highspeed motions, where the maximum outdoor forward velocity reaches 2.5 m/s, the robot exhibits stable and coordinated dynamics with no noticeable discontinuities. 

To further illustrate the advantage of unified gait control, we 

provide a comparison with the Hiking in the Wild baseline, as shown in Figure 1. The baseline trains walking and running policies separately, and switching between them must be performed manually during execution. Such manual switching often introduces brief discontinuities or posture inconsistencies at the transition points, resulting in a visibly fragmented motion sequence. In contrast, CoRe-MoE preserves natural, smooth, and dynamically consistent gait transitions throughout the entire sequence, including walking, running, returning to walking. The unified policy adaptively regulates stride length, center-of-mass motion, and whole-body coordination, demonstrating superior continuity compared with methods that depend on switching between multiple independent controllers. 

Furthermore, in multi-terrain traversal tasks, the robot exhibits strong adaptability across different terrain types. The temporal sequence in Figure 7 illustrates the robot traversing uneven ground, natural steps, and slopes in a continuous manner. Throughout the process, the policy dynamically adjusts step length, foothold placement, and body posture in response to terrain variations, while maintaining stability under height discontinuities and varying friction conditions. These results demonstrate that the proposed method enables robust and coherent locomotion across diverse and challenging terrain compositions. 

To further evaluate the system’s robustness in real-world conditions, we conducted an impact disturbance test. During level-ground locomotion, the robot was subjected to a sudden external impact while running, as shown in Figure 9. Despite the disturbance occurring under high-speed motion, the robot maintained balance and quickly recovered stable locomotion. This experiment demonstrates that the proposed method provides strong stability and recovery capability under external perturbations during dynamic gait execution. 

## VI. CONCLUSIONS 

In this work, we presented a humanoid locomotion framework CoRe-MoE that integrates visual perception, weighted action refinement, and contrastively enhanced mixture-ofexperts. The proposed method enables terrain-aware corrections and improves expert specialization through SwAV, allowing smooth and adaptive transitions between walking and running under varying velocity commands. Extensive simulations show that our approach outperforms baseline policies in success rate, travel distance, and multi-terrain adaptability. The trained policy is deployed onto a Unitree G1 robot without any fine-tuning, achieving stable zero-shot sim-to-real transfer using only the onboard depth camera. In both indoor and outdoor experiments, the robot demonstrates strong robustness, natural gait transitions, and resilience to external disturbances. Future work will extend this framework to whole-body coordination for more dynamic and human-like locomotion behaviors. 

## REFERENCES 

- [1] Shixin Luo, Songbo Li, Ruiqi Yu, Zhicheng Wang, Jun Wu, and Qiuguo Zhu. Pie: Parkour with implicit-explicit learning framework for legged robots. _IEEE Robotics and Automation Letters_ , 2024. 

- [2] I Made Aswin Nahrendra, Byeongho Yu, Minho Oh, Dongkyu Lee, Seunghyun Lee, Hyeonwoo Lee, Hyungtae Lim, and Hyun Myung. Dreamwaq++: Obstacle-aware quadrupedal locomotion with resilient multimodal reinforcement learning. _IEEE Transactions on Robotics_ , 42:819–836, 2026. 

- [3] Shaoting Zhu, Ziwen Zhuang, Mengjie Zhao, Kun-Ying Lee, and Hang Zhao. Hiking in the wild: A scalable perceptive parkour framework for humanoids. _arXiv preprint arXiv:2601.07718_ , 2026. 

- [4] Ilija Radosavovic, Tete Xiao, Bike Zhang, Trevor Darrell, Jitendra Malik, and Koushil Sreenath. Real-world humanoid locomotion with reinforcement learning. _Science Robotics_ , 9(89):eadi9579, 2024. 

- [5] Wenhao Cui, Shengtao Li, Huaxing Huang, Bangyu Qin, Tianchu Zhang, Liang Zheng, Ziyang Tang, Chenxu Hu, NING Yan, Jiahao Chen, et al. Adapting humanoid locomotion over challenging terrain via two-phase training. In _8th Annual Conference on Robot Learning_ , 2024. 

- [6] Huayi Wang, Zirui Wang, Junli Ren, Qingwei Ben, Tao Huang, Weinan Zhang, and Jiangmiao Pang. Beamdojo: Learning agile humanoid locomotion on sparse footholds. 2025. 

- [7] Junfeng Long, Junli Ren, Moji Shi, Zirui Wang, Tao Huang, Ping Luo, and Jiangmiao Pang. Learning humanoid locomotion with perceptive internal model, 2024. 

- [8] Junfeng Long, ZiRui Wang, Quanyi Li, Liu Cao, Jiawei Gao, and Jiangmiao Pang. Hybrid internal model: Learning agile legged locomotion with simulated robot response. In _The Twelfth International Conference on Learning Representations_ , 2024. 

- [9] Dimple Sethi, Sourabh Bharti, and Chandra Prakash. A comprehensive survey on gait analysis: History, parameters, approaches, pose estimation, and future work. _Artificial Intelligence in Medicine_ , 129:102314, 2022. 

- [10] E. Y. S. Chao. _Biomechanics of the Human Gait_ , pages 225–244. Springer New York, New York, NY, 1986. 

- [11] Dewei Wang, Xinmiao Wang, Xinzhe Liu, Jiyuan Shi, Yingnan Zhao, Chenjia Bai, and Xuelong Li. More: Mixture of residual experts for humanoid lifelike gaits learning on complex terrains, 2025. 

- [12] Xinyang Gu, Yen-Jen Wang, and Jianyu Chen. Humanoid-gym: Reinforcement learning for humanoid robot with zero-shot sim2real transfer. 2024. 

- [13] Jonah Siekmann, Kevin Green, John Warila, Alan Fern, and Jonathan Hurst. Blind bipedal stair traversal via sim-to-real reinforcement learning. 2021. 

- [14] Ilija Radosavovic, Tete Xiao, Bike Zhang, Trevor Darrell, Jitendra Malik, and Koushil Sreenath. Real-world humanoid locomotion with reinforcement learning. _Science Robotics_ , 9(89):eadi9579, 2024. 

- [15] Ilija Radosavovic, Sarthak Kamat, Trevor Darrell, and Jitendra Malik. Learning humanoid locomotion over challenging terrain. 2024. 

- [16] Robert A Jacobs, Michael I Jordan, Steven J Nowlan, and Geoffrey E Hinton. Adaptive mixtures of local experts. _Neural computation_ , 3(1):79–87, 1991. 

- [17] Runhan Huang, Shaoting Zhu, Yilun Du, and Hang Zhao. Moe-loco: Mixture of experts for multitask locomotion. 2025. 

- [18] Ziwen Zhuang, Shaoting Zhu, Mengjie Zhao, and Hang Zhao. Deep whole-body parkour, 2026. 

- [19] Mathilde Caron, Ishan Misra, Julien Mairal, Piotr Goyal, Piotr Bojanowski, and Armand Joulin. Swav: Unsupervised learning of visual features by contrasting cluster assignments. 2020. 

- [20] Wandong Sun, Yongbo Su, Leoric Huang, Alex Zhang, Dwyane Wei, Mu San, Daniel Tian, Ellie Cao, Finn Yan, Ethan Xie, and Zongwu Xie. Now you see that: Learning end-to-end humanoid locomotion from raw pixels, 2026. 

- [21] Ilija Radosavovic, Tete Xiao, Bike Zhang, Trevor Darrell, Jitendra Malik, and Koushil Sreenath. Real-world humanoid locomotion with reinforcement learning. _Science Robotics_ , 9(89):eadi9579, 2024. 

- [22] Jonah Siekmann, Kevin Green, John Warila, Alan Fern, and Jonathan Hurst. Blind bipedal stair traversal via sim-to-real reinforcement learning. _arXiv preprint arXiv:2105.08328_ , 2021. 

- [23] Mingqi Yuan, Tao Yu, Haolin Song, Bo Li, Xin Jin, Hua Chen, and Wenjun Zeng. Pvp: Data-efficient humanoid robot learning with proprioceptive-privileged contrastive representations. _arXiv preprint arXiv:2512.13093_ , 2025. 

- [24] Manuel Yves Galliker. Whole-body humanoid mpc: Realtime physics-based procedural loco-manipulation planning and control. https://github.com/1x-technologies/wb_humanoid_mpc, 2024. 

- [25] Nicola Scianca, Daniele De Simone, Leonardo Lanari, and Giuseppe Oriolo. Mpc for humanoid gait generation: Stability and feasibility. _IEEE Transactions on Robotics_ , 36(4):1171–1188, 2020. 

- [26] Sotaro Katayama, Masaki Murooka, and Yuichi Tazaki. Model predictive control of legged and humanoid robots: models and algorithms. _Advanced Robotics_ , 37(5):298–315, 2023. 

- [27] Haolin Song, Hongbo Zhu, Tao Yu, Yan Liu, Mingqi Yuan, Wengang Zhou, Hua Chen, and Houqiang Li. Gait-adaptive perceptive humanoid locomotion with real time under-base terrain reconstruction. 2025. 

- [28] Xuxin Cheng, Kexin Shi, Ananye Agarwal, and Deepak Pathak. Extreme parkour with legged robots. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 11443–11450. IEEE, 2024. 

- [29] Nikita Rudin, Junzhe He, Joshua Aurand, and Marco Hutter. Parkour in the wild: Learning a general and extensible agile locomotion policy using multi-expert distillation and rl fine-tuning. _arXiv preprint arXiv:2505.11164_ , 2025. 

- [30] Junzhe He, Chong Zhang, Fabian Jenelten, Ruben Grandia, Moritz Bächer, and Marco Hutter. Attention-based map encoding for learning generalized legged locomotion. _Science Robotics_ , 10(105):eadv3604, 2025. 

- [31] Qingwei Ben, Botian Xu, Kailin Li, Feiyu Jia, Wentao Zhang, Jingping Wang, Jingbo Wang, Dahua Lin, and Jiangmiao Pang. Gallant: Voxel grid-based humanoid locomotion and local-navigation across 3d constrained terrains. _arXiv preprint arXiv:2511.14625_ , 2025. 

- [32] Junfeng Long, Junli Ren, Moji Shi, Zirui Wang, Tao Huang, Ping Luo, and Jiangmiao Pang. Learning humanoid locomotion with perceptive internal model. 2025. 

- [33] Ziwen Zhuang, Shenzhe Yao, and Hang Zhao. Humanoid parkour learning. _arXiv preprint arXiv:2406.10759_ , 2024. 

- [34] Michael I. Jordan and Robert A. Jacobs. Hierarchical mixtures of experts and the em algorithm. _Neural Computation_ , 6(2):181–214, 1994. 

- [35] Ting Chen, Simon Kornblith, Mohammad Norouzi, and Geoffrey Hinton. A simple framework for contrastive learning of visual representations. _arXiv preprint arXiv:2002.05709_ , 2020. 

- [36] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [37] Xue Bin Peng, Ze Ma, Pieter Abbeel, Sergey Levine, and Angjoo Kanazawa. Amp: Adversarial motion priors for stylized physics-based character control. _ACM Transactions on Graphics (ToG)_ , 40(4):1–20, 2021. 

- [38] Mayank Mittal, Pascal Roth, James Tigue, et al. Isaac lab: A gpuaccelerated simulation framework for multi-modal robot learning. _arXiv preprint arXiv:2511.04831_ , 2025. 

- [39] Naureen Mahmood, Nima Ghorbani, Nikolaus F Troje, Gerard PonsMoll, and Michael J Black. Amass: Archive of motion capture as surface shapes. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 5442–5451, 2019. 

- [40] Félix G. Harvey, Mike Yurick, Derek Nowrouzezahrai, and Christopher Pal. Robust motion in-betweening. 39(4), 2020. 

- [41] Matthew C. Cieslak, Ann M. Castelfranco, Vittoria Roncalli, Petra H. Lenz, and Daniel K. Hartline. t-distributed stochastic neighbor embedding (t-sne): A tool for eco-physiological transcriptomic analysis. _Marine Genomics_ , 51:100723, 2020. 

