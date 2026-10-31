---
title: "RPL: Learning Robust Humanoid Perceptive Locomotion on Challenging Terrains"
date: "2026-02-03"
authors: "Yuanhang Zhang; Younggyo Seo; Juyue Chen; Yifu Yuan; Koushil Sreenath; Pieter Abbeel"
url: https://arxiv.org/abs/2602.03002
pdf: https://arxiv.org/pdf/2602.03002
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.03002)** / [論文ページ](https://arxiv.org/abs/2602.03002)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **RPL: Learning Robust Humanoid Perceptive Locomotion on Challenging Terrains** 

**Yuanhang Zhang**<sup>1</sup><sup>_,_2</sup> **, Younggyo Seo**<sup>1</sup> **, Juyue Chen**<sup>1</sup> **, Yifu Yuan**<sup>2</sup> **, Koushil Sreenath**<sup>1</sup><sup>_,_4</sup> **, Pieter Abbeel**<sup>1</sup><sup>_,_4</sup><sup>_†_</sup> **, Carmelo Sferrazza**<sup>1</sup><sup>_†_</sup> **, Karen Liu**<sup>1</sup><sup>_,_3</sup><sup>_†_</sup> **, Rocky Duan**<sup>1</sup><sup>_†_</sup> **, Guanya Shi**<sup>1</sup><sup>_,_2</sup><sup>_†_</sup> 

- 1Amazon FAR, 2CMU, 3Stanford University, 4UC Berkeley, _†_ Amazon FAR Co-Lead Page: https://rpl-humanoid.github.io/ 


Figure 1: RPL enables long-horizon bidirectional locomotion and remains robust with payloads on Unitree G1 humanoid robot with a depth-based transformer policy. Terrains include 20<sup>_◦_</sup> slopes, staircases with different step lengths (22 cm, 25 cm, 30 cm), and 25 cm _×_ 25 cm stepping stones with 60 cm gaps. 

**Abstract:** Humanoid perceptive locomotion has made significant progress and shows great promise, yet achieving robust multi-directional locomotion on complex terrains remains underexplored. To tackle this challenge, we propose RPL, a two-stage training framework that enables multi-directional locomotion on challenging terrains, and remains robust with payloads. RPL first trains terrain-specific expert policies with privileged height map observations to master decoupled locomotion and manipulation skills across different terrains, and then distills them into a transformer policy that leverages multiple depth cameras to cover a wide range of views. During distillation, we introduce two techniques to robustify multidirectional locomotion, depth feature scaling based on velocity commands and random side masking, which are critical for asymmetric depth observations and unseen widths of terrains. For scalable depth distillation, we develop an efficient multi-depth system that ray-casts against both dynamic robot meshes and static terrain meshes in massively parallel environments, achieving a 5 _×_ speedup over the depth rendering pipelines in existing simulators while modeling realistic sensor latency, noise, and dropout. Extensive real-world experiments demonstrate robust multi-directional locomotion with payloads (2 kg) across challenging terrains, including 20<sup>_◦_</sup> slopes, staircases with different step lengths (22 cm, 25 cm, 30 cm), and 25 cm _×_ 25 cm stepping stones separated by 60 cm gaps. 

**Keywords:** Humanoid Perceptive Locomotion, RL, Imitation Learning 

## **1 Introduction** 

Humanoid robots hold great potential for daily human tasks. While recent work has demonstrated expressive whole-body motion tracking and loco-manipulation capabilities [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], a defining capability beyond wheeled mobile manipulators is leveraging legged mobility to robustly traverse diverse terrains, while performing meaningful tasks such as carrying payloads. Existing humanoid perceptive locomotion methods [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24] typically rely on a single forward camera and idealized upper-body conditions, becoming brittle under multi-directional locomotion or dynamic self-occlusions from upper-body motions. Mapping-based methods [25, 22, 17, 18, 14] can handle bidirectional locomotion on challenging terrains but rely on noisy state estimation that complicates system-level optimization. End-to-end perceptive control under asymmetric multi-view inputs (i.e., different cameras observing different terrain types) remains underexplored. 

We propose RPL, a two-stage framework for **R** obust humanoid **P** erceptive **L** ocomotion. RPL first trains terrain-specific expert policies with privileged height maps under end-effector force perturbations, acquiring decoupled locomotion and manipulation skills. These experts are then distilled into a unified transformer policy taking multi-view depth, enabling robust multi-directional locomotion. For scalable distillation, we develop an efficient multi-depth rendering system ray-casting against both dynamic robot meshes and static terrain meshes in massively parallel environments, modeling realistic latency, noise, and dropout. We further introduce two distillation techniques: (1) _Depth Feature Scaling based on Velocity commands_ (DFSV), which adaptively modulates perception features based on the velocity command to reduce distribution shift under asymmetric multi-view inputs; and (2) _Random Side Masking_ (RSM), which randomly masks lateral regions of depth images to improve generalization to unseen terrain widths. 

Our key contributions are: (1) RPL, a two-stage framework distilling terrain-specific experts into a unified depth policy for robust multi-directional humanoid locomotion; (2) an efficient multi-depth rendering system over dynamic robot and static terrain meshes, achieving a 5 _×_ speedup over existing simulators with realistic latency, noise, and dropout; (3) Depth Feature Scaling based on Velocity commands (DFSV) and Random Side Masking (RSM) during distillation to handle asymmetric multi-view inputs and unseen terrain widths; and (4) real-world validation of long-horizon bidirectional locomotion under whole-body motions and payload disturbances. 

## **2 Related Works** 

### **2.1 Perceptive Locomotion in Legged Robots** 

Perceptive locomotion for legged robots has progressed rapidly [25, 14, 15, 16, 17, 19, 20, 21, 22, 23, 24, 18, 26, 27]. Quadrupeds can sometimes traverse stairs and curbs blindly [28] thanks to inherently stable support polygons, whereas humanoids demand precise foot placement and are far more sensitive to perception errors. Two paradigms dominate: (1) LiDAR-based mapping [25, 14, 17, 18, 19, 24, 22] compresses terrain into elevation maps but relies on calibration and state estimation that introduce sim-to-real drift; (2) end-to-end depth-based methods [15, 20, 21, 27, 16, 26, 23] map raw depth directly to actions, removing explicit estimation. 

Most depth-based work uses a single forward camera and demonstrates only forward locomotion. [29] achieves omnidirectional traversal with a single downward camera but struggles with sparse footholds (e.g., stepping stones); [30] adds multiple cameras for wider coverage but evaluates only on stairs, not the general asymmetric multi-view setting where different cameras observe distinct terrain types. Depth rendering also remains expensive: recent Warp-based pipelines [26, 22, 20, 31] accelerate it but lack dynamic-mesh support or do not scale to multiple cameras. Existing policies also rarely evaluate robustness to unseen terrain widths or loco-manipulation disturbances such as transporting payloads. RPL targets this gap, combining scalable multi-depth rendering with distillation techniques that generalize across unseen terrain widths under payloads. 

2 

|**Method**|**Stairs**<br>**Up/Down**|**Stepping**<br>**stones**|**Multi-view**<br>**coverage**|**Real-world**<br>**Bidirectional**|**Manip. /**<br>**Active Payload**|**Sim Traversal**<br>slopes/stairs/stones|
|---|---|---|---|---|---|---|
|**RPL (ours)**|✓|✓|✓|✓|✓|✓/✓/✓|
|Hiking-in-the-Wild [26]|✓|_×_|_×_|_×_|✓|✓/_∼_/_×_|
|DPL [20]|✓|_×_|_×_|_×_|✓|N/A|
|Gait-adaptive [29]|✓|_×_|✓|✓|✓|N/A|
|No More Blind Spots [30]|✓|_×_|✓|✓|_×_|N/A|
|BeamDojo [14]|✓|✓|✓|✓|_×_|N/A|
|Humanoid Parkour [16]|✓|_×_|_×_|_×_|✓|N/A|


Table 1: CAPABILITY COMPARISON VS. RELATED METHODS. ✓ yes, _∼_ partial (only single-direction), _×_ no. _Multi-View_ : 360 deg LiDAR or multi-camera; _Sim Traversal_ : single-shot per-terrain success (slopes/stairs/stones); N/A marks without public code. 


Figure 2: **Overview of the Two-Stage Training Framework in RPL** . **Top (Stage 1)** : We train terrain-specific expert policies using privileged height-map observations to master decoupled locomotion and manipulation. **Bottom (Stage 2)** : We distill the expert policies into a single multi-view, depth-based transformer policy. Multi-camera depth inputs are encoded by CNN backbones with random side masking (Section 3.2.4) and depth feature scaling based on velocity commands (Section 3.2.3), fused into visual features, and combined with noisy proprioceptive observations and task goals to predict student actions. 

**Comparison with prior work.** Table 1 highlights RPL’s combination of onboard multi-view depth, real-world bidirectional traversal, and teleoperated active payload transport across stairs, slopes, and stepping stones. 

## **3 RPL: Two Stage – From Multiple Experts to One General Visual Policy** 

RPL is a two-stage framework (Figure 2). Stage 1 trains terrain-specialized experts with privileged height-map observations over slopes, stairs up, stairs down, and stepping stones (Figure 6a). Stage 2 distills them into a single unified visual policy taking front and back depth observations for bidirectional locomotion. We build on the dual-agent formulation of FALCON [1], which factorizes whole-body control into a lower-body locomotion policy and an upper-body manipulation policy on a shared proprioceptive history, outperforming single-agent whole-body control [1, 32, 33]. Both agents observe the proprioceptive history **s**<sup>_p_</sup> _t_<sup>= [</sup><sup>**q**</sup><sup>_t−_4:</sup><sup>_t,_</sup><sup>**q**˙</sup><sup>_t−_4:</sup><sup>_t,_</sup><sup>**_ω_**root</sup> _t−_ 4: _t_<sup>_,_</sup><sup>**g**</sup><sup>_t−_4:</sup><sup>_t,_</sup><sup>**a**</sup><sup>_t−_5:</sup><sup>_t−_1].The lower-</sup> body policy is conditioned on locomotion goals **G**<sup>_l_</sup> _t_<sup>= [</sup><sup>**v**</sup> _t_<sup>lin</sup><sup>_,_</sup><sup>**w**</sup> _t_<sup>yaw</sup> _,_ **_ϕ_**<sup>stance</sup> _t ,_ **h**<sup>root</sup> _t ,_ **o**<sup>torso</sup> _t_ ] (linear/angular velocity, stance/walking mode, root height, torso orientation; root height and torso are tracked only during stance), and the upper-body policy on **G**<sup>_u_</sup> _t_<sup>=</sup><sup>**q**upper</sup><sup>_,t_(upper-body joint targets).The percep-</sup> tual observation is **H** _t_ in Stage 1 (privileged height map) and **D** _t_ = _{_ **d**<sup>(</sup> _t_<sup>_i_)</sup><sup>_}N_</sup> _i_ =1<sup>camin Stage 2 (multi-view</sup> depth), fed only to the lower-body policy since terrain perception primarily governs legged locomotion. The policies are **_π_** _l_ : ( **s**<sup>_p_</sup> _t_<sup>_,_</sup><sup>**G**</sup><sup>_l_</sup> _t_<sup>_,_</sup><sup>**H**</sup><sup>_t_or</sup><sup>**D**</sup><sup>_t_)</sup><sup>_→_</sup><sup>**a**</sup><sup>_l_</sup> _t_<sup>and</sup><sup>**_π_**</sup><sup>_u_:(</sup><sup>**s**</sup> _t_<sup>_p,_</sup><sup>**G**</sup><sup>_u_</sup> _t_<sup>)</sup><sup>_→_</sup><sup>**a**</sup><sup>_u_</sup> _t_<sup>,withconcatenated</sup> actions **a** _t_ = [ **a**<sup>_l_</sup> _t_<sup>;</sup><sup>**a**</sup><sup>_u_</sup> _t_<sup>]trackedbyalow-levelPDcontroller.(SeeAppendixA.1forthenotation</sup> summary.) 

3 


Figure 3: w/o (left) and w/ (right) foot-edge penalty. Figure 4: w/o (left) and w/ (right) foothold penalty. 

### **3.1 Stage 1: Training Multiple Terrain Experts via Height Map** 

To provide high-quality teacher actions for distillation, we train one terrain-specialized expert per terrain family using a privileged height map represented as a local grid of size 1 _._ 6 m _×_ 1 _._ 0 m at 0 _._ 1 m resolution. The dual-agent policies are jointly trained with independent reward functions and optimized using PPO [34]. We adopt a force curriculum [1] with direction ratio **_γ_** = [ _γx, γy, γz_ ] = [0 _,_ 0 _,_ 1] to specifically address end-effector payloads for robust loco-manipulation. We further apply asymmetric actor–critic training [35], where the critics access privileged information including root linear velocity and end-effector force **_F_**<sup>_ee_</sup> _t_<sup>,andusesymmetrydataaugmentation[36]on</sup><sup>**s**</sup> _t_<sup>_p_,</sup><sup>**G**</sup><sup>_l_</sup> _t_<sup>,</sup> **G**<sup>_u_</sup> _t_<sup>, and</sup><sup>**H**</sup><sup>_l_</sup> _t_<sup>to encourage symmetric gait patterns.</sup> 

### **3.1.1 Terrain Settings** 

We train specialized experts for four terrain families illustrated in Figure 2: (1) **Slopes** : ramps with inclinations up to 37<sup>_◦_</sup> in pyramid form; (2) **Stairs Up / Down** : ascending and descending staircases with 0 _._ 25–0 _._ 30 m step length and 0 _._ 05–0 _._ 27 m height; (3) **Stepping Stones** : column-shaped discrete footholds with 0 _._ 25–0 _._ 40 m diameter, 0 _._ 05–0 _._ 70 m gaps, and up to 0 _._ 05 m height variation. Stairs and stepping stones are particularly challenging given the robot’s 0 _._ 21 m foot length, which is close to the minimum support size of 0 _._ 25 m, leaving little margin for foothold placement errors. 

### **3.1.2 Reward Design** 

We adopt the dual-agent rewards in [1] and add three terms for stable terrain traversal: (i) **Foot Edge Penalty** [15], which uses precomputed dilated edge masks to penalize contacts at terrain edges (Figure 3); (ii) **Foothold Penalty** [14], which samples a grid across the foot sole and penalizes invalid coverage (Figure 4); and (iii) **Torso Orientation Tracking** [37], _rtorso_ = exp( _−∥_ **g** proj _−_ **g** ref _∥_<sup>2</sup> _/σ_ ), coordinating waist and hip joints for a wide stance-mode tracking range. We use foothold penalty for stairs (edge dilation is too conservative on 0.25 m treads vs. 0.21 m feet) and foot-edge penalty for stepping stones (small isolated supports offer little tolerance to placement errors). 

### **3.2 Stage 2: Distillation into Unified Visuomotor Policy** 

As shown in Figure 2, after all the terrain experts based on height maps are obtained, we distill them into one unified visuomotor policy for multi-directional perceptive locomotion. 

### **3.2.1 Distillation Formulation** 

We use DAgger [38] style imitation learning to train the student policy. The perceptual observation **P**<sup>_l_</sup> _t_<sup>consists of depth inputs from multiple depth cameras.The student lower-body policy</sup><sup>**_π_**vis</sup> _l_ takes noisy proprioception ˆ **s**<sup>_p_</sup> _t_<sup>andmulti-viewdepthinputs</sup><sup>**D**</sup><sup>_t_=</sup><sup>_{_</sup><sup>**d**(</sup> _t_<sup>_i_)</sup><sup>_}N_</sup> _i_ =1<sup>cam,whiletheexpertpolicies</sup> **_π_**<sup>exp</sup> _l,k_<sup>are conditioned on noise-free proprioception</sup><sup>**s**</sup> _t_<sup>_p_and privileged height maps</sup><sup>**H**</sup><sup>_t_.We train the</sup> student by minimizing the action regression loss: 


The final deployed controller combines the distilled visual locomotion policy **_π_**<sup>vis</sup> _l_ with the blind upper-body policy **_π_** _u_ , producing the whole-body action for low-level PD tracking. We use DAgger 

4 


(a) Illustration of DFSV. 


(b) Illustration of RSM. 

Figure 5: (a) **DFSV.** CNN feature maps from four directional depth cameras under a zero command ( _vx_ =0 _, vy_ =0, left) and a diagonal command ( _vx_ =0 _._ 5 _, vy_ =0 _._ 5, right); heatmaps visualize each camera’s relevance to the commanded velocity direction. (b) **RSM.** The red dot on the top figure is where the front camera is placed; the bottom three figures show different masking modes. 

Only rather than a Hybrid DAgger + RL objective, which we find preserves cross-terrain gradient alignment and achieves higher terrain levels on every terrain family (See Appendix 4.5 for details). 

### **3.2.2 Efficient Multi-Depth System Simulation** 

We implement a GPU-efficient multi-depth camera simulation in NVIDIA Warp [39], performing massively parallel depth synthesis by ray-casting against both dynamic robot meshes and a shared static terrain mesh (Algorithm 1). For each environment _e_ , camera _c_ , and pixel ( _x, y_ ) with intrinsics **K** _e_ , we form a camera-frame ray **r** _c_ = **K**<sup>_−_</sup> _e_<sup>1[</sup><sup>_x, y,_1]</sup><sup>_⊤_, rotate it by the camera orientation</sup><sup>**q**</sup><sup>_e,c_</sup> _c_<sup>, and</sup> cast from the origin **o** = **p**<sup>_e,c_</sup> _c_ along direction **d** . The depth is the distance to the closest ray–mesh intersection, clipped by far-plane _d_ max. 

To avoid costly per-frame mesh refitting [40], we keep each body mesh _Mb_ canonical in its local frame and transform rays as **o** _b_ = **R**<sup>_⊤_</sup> _b_<sup>(</sup><sup>**o**</sup><sup>_−_</sup><sup>**t**</sup><sup>_b_),</sup><sup>**d**</sup><sup>_b_=</sup><sup>**R**</sup><sup>_⊤_</sup> _b_<sup>**d**,where(</sup><sup>**t**</sup><sup>_b,_</sup><sup>**R**</sup><sup>_b_)isthebodypose.</sup> For each ray, we first query all robot body meshes locally—tracking the closest hit _z_<sup>_⋆_</sup> as an earlytermination upper bound—and then the shared terrain mesh in the world frame, updating _z_<sup>_⋆_</sup> if a closer hit is found. All queries execute in a single fused Warp kernel parallelized over environments, cameras, and pixels, and the entire pipeline is captured into a CUDA graph for low-overhead replay; per-environment intrinsics randomization is supported by batching _{_ **K**<sup>_−_</sup> _e_<sup>1</sup><sup>_}_.The full kernel is</sup> summarized in Algorithm 1. 

### **Algorithm 1:** Multi-Depth Ray Casting Kernel 

**Input:** Static terrain mesh _M_ terrain; robot body meshes _{Mb}_<sup>_B_</sup> _b_ =1<sup>; camera poses</sup> _{_ ( **p**<sup>_e,c_</sup> _c_<sup>_,_</sup><sup>**q**</sup><sup>_e,c_</sup> _c_<sup>)</sup><sup>_}_; body poses</sup><sup>_{_(</sup><sup>**t**</sup><sup>_e_</sup> _b_<sup>_,_</sup><sup>**q**</sup><sup>_e_</sup> _b_<sup>)</sup><sup>_}_; batched inverse intrinsics</sup><sup>_{_</sup><sup>**K**</sup> _e_<sup>_−_1</sup><sup>_}_; far plane</sup> _d_ max; principal pixel ( _cx, cy_ ) **Output:** Depth image **D** _∈_ R<sup>_N×C×H×W_</sup> **1 foreach** <u>(</u> _<u>e, c, x, y</u>_ <u>)</u> _<u>∈</u>_ <u>[</u> _<u>N</u>_ <u>]</u> _<u>×</u>_ <u>[</u> _<u>C</u>_ <u>]</u> _<u>×</u>_ <u>[</u> _<u>W</u>_ <u>]</u> _<u>×</u>_ <u>[</u> _<u>H</u>_ <u>]</u> **do 2** ( **o** _,_ **d** _, m_ ) _←_ BUILDDEPTHRAY( **p**<sup>_e,c_</sup> _c_<sup>_,_</sup><sup>**q**</sup><sup>_e,c_</sup> _c_<sup>_,_</sup><sup>**K**</sup><sup>_−_</sup> _e_<sup>1</sup><sup>_, x, y, cx, cy_);</sup> **3** _z_<sup>_⋆_</sup> _← d_ max; _d_ bound _← d_ max; /* 1) Query dynamic robot bodies *<sup>/</sup> **4 for** _<u>b ←</u>_ <u>1</u> **<u>to</u>** _<u>B</u>_ **do 5** ( **o** _l,_ **d** _l_ ) _←_ WORLDTOBODYRAY( **o** _,_ **d** _,_ **t**<sup>_e_</sup> _b_<sup>_,_</sup><sup>**q**</sup> _b_<sup>_e_);</sup> **6 if** <u>MESHRAYQUERY(</u> _<u>Mb,</u>_ **<u>o</u>** _<u>l,</u>_ **<u>d</u>** _<u>l, d</u>_ <u>bound</u> _<u>/m</u>_ <u>)</u> _<u>→ t</u>_ **then 7** _z_<sup>_<u>⋆</u>_</sup> _←_ min( _z_<sup>_<u>⋆</u>_</sup> _, m t_ ); **8** _d_ bound _← z_<sup>_⋆_</sup> ; // early termination /* 2) Query static terrain *<sup>/</sup> **9 if** <u>MESHRAYQUERY(</u> _<u>M</u>_ <u>terrain</u> _<u>,</u>_ **<u>o</u>** _<u>,</u>_ **<u>d</u>** _<u>, d</u>_ <u>bound</u> _<u>/m</u>_ <u>)</u> _<u>→ t</u>_ **then 10** _z_<sup>_<u>⋆</u>_</sup> _← m t_ ; **11 D** [ _e, c, y, x_ ] _← z_<sup>_⋆_</sup> ; 

5 


(a) Real-world terrain course overview. 


(b) Robot setup. 

Figure 6: (a) Overview of the terrain course including slopes, stairs, and stepping stones; key geometric dimensions are annotated in white. (b) Real-world robot setup with front and rear depth cameras. 

### **3.2.3 Depth Feature Scaling Based on Velocity Commands** 

When the robot is equipped with multiple depth cameras facing different directions, the relevance of each camera depends on the locomotion direction. We thus introduce Depth Feature Scaling based on Velocity commands (DFSV, Figure 5a). Let **_n_ ˆ** _i ∈_ R<sup>2</sup> denote the normalized viewing direction of camera _i_ in the robot’s local frame. Given the planar velocity command **v** _l_<sup>_lin_</sup> = [ _vx, vy_ ]<sup>_⊤_</sup> , we compute per-camera attention scales _δi_ = 1 _−σ_ ( _−k_ ( _⟨_ **v** _l_<sup>_lin_</sup> _,_ **ˆ** **_n_** _i⟩−v_ th)) for _i_ = 1 _, . . . , N_ cam, where _k_ controls the transition sharpness and _v_ th is a velocity threshold. Cameras aligned with the commanded velocity are emphasized ( _δi ≈_ 1), while those facing away are suppressed ( _δi ≈_ 0). The scales are applied element-wise to the CNN feature vectors **f** _i_ before concatenation: **f** fused =<sup>�</sup><sup>_N_</sup> _i_ =1<sup>cam</sup><sup>_δi ·_</sup><sup>**f**</sup><sup>_i_,</sup> requiring no additional learned parameters. 

### **3.2.4 Random Side Masking for Unseen Terrain Widths** 

Real-world terrains often have widths different from the wide terrains seen during training. To generalize to narrower ones, we introduce Random Side Masking (RSM, Figure 5b): during training we stochastically occlude peripheral regions of the depth image with random noise, forcing the policy to rely on the central visible region. For each environment, we sample mode _∼_ Categorical( **p** _k_ ) over _{_ none _,_ small _,_ large _}_ , where **p** _k_ depends on the terrain type _k_ ; larger masks emulate narrower effective widths. Occluded pixels are filled with uniformly sampled values in [ _d_ near _, d_ far] to prevent exploitation of boundary artifacts. We use larger masks on continuous terrains (stairs, slopes), where traversability is governed by local geometry ahead, and smaller masks on stepping stones, where valid footholds may appear only peripherally. 

## **4 Experiments** 

In this section, we will present extensive experiments in both simulation and the real world to show the effectiveness and the robustness of our method RPL. We aim to answer four questions: (Q1) Does RPL enable scalable multi-depth rendering compared to existing simulation methods? (Q2) Do DFSV and RSM improve robustness under asymmetric visual inputs and unseen terrain widths? (Q3) Does our network architecture outperform alternatives in distillation? (Q4) Can RPL robustly perform long-horizon bidirectional locomotion across diverse, challenging terrains in the real world? 

### **4.1 Experiment Setup** 

**Training Configurations.** We use Unitree G1 29 DoF as the humanoid and train all policies in NVIDIA IsaacGym [41]. Stage 1 uses 4 NVIDIA L40S GPUs with 4096 _×_ 4 parallel envs for 12h for each expert policy; Stage 2 uses 8 GPUs with 1024 _×_ 8 envs for 12h. 

**Real-World Terrain Settings.** As shown in Figure 6, we evaluate on a customized terrain course and a long curvy staircase. The course consists of (i) a 20<sup>_◦_</sup> slope, (ii) 1.2 m-wide staircases with 20 cm step height and step lengths of 22 cm and 25 cm, and (iii) stepping stones (25 cm side length, 

6 

|**Method**|**Dyn. Mesh**|**Num. Envs**|_N_**cam** =|1|_N_**cam** =|2|_N_**cam**|= 4|
|---|---|---|---|---|---|---|---|---|
||||VRAM (GB)_↓_|Iter. (s)_↓_|VRAM (GB)_↓_|Iter. (s)_↓_|VRAM (GB)_↓_|Iter. (s)_↓_|
|IsaacGym PhysX|✓|1024|16.8|35.6_±_4.1|22.5|70.1_±_8.3|33.9|146.5_±_16.1|
|IsaacSim RTX|✓|1024|17.5|5.3_±_0.1|23.2|7.6_±_0.1|34.4|12.6_±_0.1|
|IsaacSim Warp|×|1024|**12.8**|3.5_±_0.1|15.1|5.9_±_0.1|20.7|9.1_±_0.1|
|IsaacLab Warp 2.3.2|✓|1024|15.0|6.6_±_0.1|17.8|8.5_±_0.1|23.5|14.7_±_0.1|
|**Ours (Alg. 1)**|✓|1024|13.3|**1.3**_±_0.0|**14.6**|**1.5**_±_0.1|**17.3**|**1.9**_±_0.1|


Table 2: Depth rendering scalability across different numbers of depth cameras with _N_ env = 1024. 

|**Task**|_N_**cam (Config.)**|**Slopes**|**Stairs Up**|**Stairs Down**|**Stepping Stones**|
|---|---|---|---|---|---|
||_Expert Level_|_6.0_|_6.0_|_6.0_|_6.0_|
|**Bidirectional**|1 (Down)<br>2 (F + B)<br>4 (F + B + L + R)|**6.0**_±_0.0<br>**6.0**_±_0.0<br>**6.0**_±_0.0|**6.0**_±_0.0<br>**6.0**_±_0.0<br>**6.0**_±_0.0|**5.9**_±_0.1<br>**6.0**_±_0.0<br>**6.0**_±_0.0|5.1_±_0.1<br>**6.0**_±_0.0<br>**6.0**_±_0.0|
||_Expert Level_|_6.0_|_6.0_|_6.0_|_5.6_|
|**Omnidirectional**|1 (Down)<br>2 (F + B)|**6.0**_±_0.0<br>**6.0**_±_0.0|**6.0**_±_0.0<br>**6.0**_±_0.0|**5.9**_±_0.1<br>**5.9**_±_0.1|3.0_±_0.2<br>**4.5**_±_0.1|
||4 (F + B + L + R)|**6.0**_±_0.0|**6.0**_±_0.1|**6.0**_±_0.0|**4.6**_±_0.0|


Table 3: **Terrain levels** _↑_ achieved under different _N_ cam for bidirectional and omnidirectional locomotion. 

60 cm gaps). With G1’s 21 cm foot, these leave little margin for footholds. The long curvy staircase is with 20 cm height and 30 cm step length, additionally requiring non-zero angular velocity. 

**Perception Settings.** During distillation, we render depth at 10 Hz with FOV 101<sup>_◦_</sup> _×_ 69<sup>_◦_</sup> , raw resolution 240 _×_ 135 downsampled to 48 _×_ 27. We support up to _N_ cam = 4 cameras (front/rear/left/right) for omni-directional locomotion in simulation. To minimize hardware modification on Unitree G1 (mounting holes only at front and rear), we deploy _N_ cam = 2 in a front–back configuration (Figure 6 (b)), which suffices for bidirectional locomotion. We use ZED 2i cameras at 15 Hz with _neural_ _~~l~~ ight_ mode, downsampled to 48 _×_ 27 before policy input. Realistic depth randomization (process delay, noise, dropout) is summarized in Appendix A.2. 

### **4.2 Scalable Multi-Depth Rendering Performance** 

To answer **Q1** , we benchmark depth rendering pipelines for RPL against IsaacGym PhysX, IsaacSim [42] RTX (TiledCamera), and IsaacSim Warp (RayCasterCamera). As shown in Table 2, on a single L40S GPU with _N_ cam = 1 _,_ 2 _,_ 4 over all terrains at 240 _×_ 135 resolution, RPL supports ray-casting against both dynamic and static Figure 7: Camera poses for _N_ cam = 1 _,_ 2 _,_ 4.. meshes and achieves a 5 _×_ speedup over the fastest baseline (IsaacSim Warp), which does not support dynamic meshes. IsaacLab 2.3.2’s dynamic-mesh MultiMeshRayCasterCamera is 5 _._ 1 _/_ 5 _._ 7 _/_ 7 _._ 7 _×_ slower at 1 _/_ 2 _/_ 4 cameras (Table 2). Iter. includes physics, rendering, and inference for all methods. Both use canonical-frame queries; RPL’s CUDA-graph replay and pre-allocated buffers avoid the baseline’s per-camera launches, blocking synchronization, and per-step allocation. 

Figure 7: Camera poses for _N_ cam = 1 _,_ 2 _,_ 4.. 

To show the necessity of multiple cameras, we compare achieved terrain levels for _N_ cam = 1 _,_ 2 _,_ 4 under bidirectional and omnidirectional locomotion (Table 3); camera configurations are in Figure 7 ( _N_ cam = 1 uses a downward-facing camera). Performance degrades sharply on stepping stones with fewer cameras, where 70 cm gaps demand a wide FOV aligned with the walking direction. Reliable multi-directional locomotion thus requires at least two cameras covering each walking direction. 

In single-shot per-terrain simulation tests, Hiking-in-the-Wild [26] traverses slopes bidirectionally and stairs forward but fails on stepping stones; RPL traverses all three. These outcomes are not aggregate success-rate estimates. 

7 


Figure 8: **Distillation Loss Comparison.** (a) compares among different network architectures. (b) compares among (1) RPL; (2) RPL w/o DFSV & RSM; (3) RPL w/o DFSV; and (4) RPL w/o RSM. 


Figure 9: **Bidirectional locomotion on unseen-width stairs with asymmetric depth observations** . (a) RPL w/o RSM; (c) RPL w/o DFSV; (b,d) RPL. 

|**Method**|**Forward **|**Backward**|
|---|---|---|
|RPL(CNN+Transformer)|**10/10**|**10/10**|
|w/o DFSV|0/10|2/10|
|w/o RSM|2/10|0/10|
|w/o DFSV & RSM|0/10|0/10|
|w/o force pert.|3/10|3/10|
|CNN+MLP|6/10|7/10|
|CNN+RNN|5/10|5/10|
|U-Net+Transformer|1/10|0/10|


Table 4: **Whole terrain course traversal success rate** . Top: DFSV/RSM ablations. Bottom: alternative network architectures, all with force perturbation, DFSV and RSM if applicable. 

### **4.3 Robustness to Asymmetric Depth Inputs, Unseen Terrain Widths and Payloads** 

To answer **Q2** , we ablate RSM, DFSV with four variants: RPL, RPL w/o RSM, RPL w/o DFSV, and RPL w/o DFSV & RSM. All four reach similar final distillation losses (Figure 8 (b)), indicating the masked inputs still preserve enough task-relevant information for action supervision. Despite comparable training losses, deployment behavior differs substantially. We visualize sim-to-sim rollouts in MuJoCo [43] on a terrain course consisting of (i) a 25<sup>_◦_</sup> slope, (ii) 1.2 m-wide staircases with 20 cm step height and step lengths of 25 cm, and (iii) stepping stones (25 cm side length, 60 cm gaps). The weight of the fake hand is changed to 2.5kg for the real world loco-manipulation setting in Figure 1 (b). During backward descent (a,b), RPL w/o RSM fails on the unseen narrow stairs while RPL remains stable. During forward descent (c,d), the front camera sees stairs while the rear still perceives stepping stones, creating asymmetric multi-view inputs; without DFSV, the policy is distracted by irrelevant rear-view cues and falls. The whole-course traversal success rates in Table 4 (top block) confirm this: removing DFSV, RSM, or both drops success from 10/10 to as low as 0/10, and removing the Stage-1 force perturbation drops it to 3/10 under the 2.5 kg payload. RSM, DFSV, and the force perturbation thus jointly enable robust bidirectional locomotion under OOD geometry, asymmetric perception, and end-effector payloads. 

### **4.4 Training Architecture and Distillation Ablations** 

To answer **Q3** , we compare four distillation backbones (Figure 8 (a)): (i) _CNN+MLP_ , (ii) _CNN+RNN_ , (iii) _CNN+Transformer_ ( **Ours** ), and (iv) _U-Net+Transformer_ that reconstructs a height map via _L_ rec = E _t_ [ _∥f_ rec( **D** _t_ ) _−_ **H** _t∥_ 2<sup>2] jointly with Equation (1).</sup> _CNN+Transformer_ achieves the lowest distillation loss <u>and</u> the highest deployment success (Table 4, bottom block) thanks to its attention-based multi-view fusion. While Section 3.2.4 shows similar losses do not guarantee similar robustness, with DFSV and RSM applied, 


Figure 10: Terrain course in simulation. 

higher loss here reliably indicates worse deployment—so the loss remains a useful coarse selection 

8 

signal. U-Net’s pixel-wise reconstruction is also incompatible with RSM, limiting deployment robustness under partial observations. 

### **4.5 Multi-Terrain Gradient Analysis – DAgger Only vs. Hybrid DAgger + RL** 


Figure 11: **Pairwise inter-terrain gradient cosine during training** for the �24� = 6 terrain pairs. DAgger Only (orange) preserves higher cosine throughout, while Hybrid DAgger + RL (red) collapses toward 0 within the first few hundred iterations. 


Figure 13: **Terrain-level curves under DAgger Only vs. Hybrid DAgger + RL.** DAgger Only (orange) reaches and sustains a higher terrain level on every terrain family, while Hybrid DAgger + RL (red) converges more slowly and plateaus at lower levels. 

We compare two distillation objectives: (i) <u>DAgger Only,</u> training the student only with the BC action regression loss in Equation (1); and (ii) <u>Hybrid DAgger + RL</u> as proposed by [44], which adds a PPO-style policy-gradient term so the student can both imitate the expert and refine itself with task rewards: 


9 

where _L_ distill is the BC term from Equation (1) and _L_ PPO is a standard PPO actor objective. We tune down _λ_ D gradually following a cosine scheduling scheme, which is capped at 0.1. The hybrid is appealing in principle—the policy-gradient term could let the student improve in regions where the height-map expert is suboptimal under the new depth-only observation. 

**Higher terrain levels.** On every terrain family, DAgger Only reaches a substantially higher terrain level and converges faster than Hybrid DAgger + RL (Figure 13). 

**Better gradient alignment.** Let _Bk_ denote the subset of a shared mini-batch belonging to terrain _k ∈{_ 1 _, . . . , K}_ ( _K_ =4 here). For each terrain we compute the per-terrain actor gradient 


and the pairwise cosine between any two terrains _i, j_ : 


A high _ρij_ ( _ρij →_ 1) means updating _θ_ to reduce loss on terrain _i_ also reduces loss on terrain _j_ , so the parameters move in a direction shared across terrains and one step improves multiple terrains at once; _ρij ≈_ 0 means the two updates are roughly orthogonal, so each step pulls _θ_ in its own direction and only improves one terrain at a time. We log _ρij_ for all � _K_ 2 � = 6 pairs (Figure 11). DAgger Only keeps _ρij_ well above zero during early training, so each step is shared across terrains and the policy quickly learns the common locomotion fundamentals (balance, gait timing, depth–proprio fusion). Hybrid DAgger + RL drives _ρij →_ 0 within the first few thousand iterations (the per-terrain norms _∥_ **g** _k∥_ stay non-zero in Figure 12, so the gradients are just mutually orthogonal): the four terrains compete for capacity, per-step progress per terrain is smaller, and convergence is slower with lower final terrain levels (Figure 13). This is not a flaw of hybrid itself: although we apply largely shared reward terms across the four terrains, the RL objective is value-driven and pushes the policy toward what is locally optimal <u>on each terrain, so the per-terrain gradients still pull</u> _θ_ in different directions—the multi-task RL gradient-interference phenomenon studied in prior work [45, 46, 47]. Resolving it would require either explicit gradient-surgery techniques or further reward co-design. Since DAgger Only already performs strongly, we adopt it in RPL without investing in such treatment. 

### **4.6 Robust Real-World Bidirectional Locomotion** 

To answer **Q4** , we deploy RPL on the Unitree G1 29 DoF humanoid for back-and-forth traversal across a 50 m terrain course and a curved building staircase (Section 4.1). The transformer policy runs at 50 Hz on an onboard Jetson Orin NX 16GB; depth capture, policy inference, and the Apple Vision Pro teleoperation pipeline communicate via shared-memory buffers to reduce system latency. We run 10 whole-course bidirectional traversals (5 without payload, 5 with a 2 kg payload), where a single misstep on any subterrain ends the trial. 

As shown in the **supplementary Failure Setting Suc. video** , Figure 1, and Table 5, RPL achieves (a) Stones (b) Stairs (c) Payload an overall 6/10 whole-course success rate w/o payload **3/5** 1 1 — (3/5 without payload, 3/5 with the 2 kg w/ 2 kg payload **3/5** 1 0 1 payload), each successful trial chaining a **Total 6/10** 2 1 1 20<sup>_◦_</sup> slope, staircases of two step lengths (22 / 25 cm), and 25 cm stepping stones Table 5: **Real-world whole-course traversal** (10 trials). with 60 cm gaps in either forward or backFailure modes (a)-(c) detailed in Section 4.7. ward direction for _∼_ 200 m and _∼_ 2 min of continuous traversal. The robot also bends down to pick up the 2 kg payload and transports it across the entire course, and generalizes zero-shot to an in-the-wild curved building staircase (30 cm step) with unseen curvature and lighting. The remaining failures concentrate in three categories—foot-edge contacts on stepping stones and on the lateral side edge of the staircase, and payload swing—analyzed in detail in Section 4.7. Overall, these results demonstrate robustness under long horizons, asymmetric observations, narrow terrains, and payloads on a real humanoid. 

10 

### **4.7 Real-World Study and Failure Mode Analysis** 


Figure 14: **Real-world failure modes of RPL.** Representative failure cases observed during real-world deployment: (a) foot landings near the perimeter of stepping stones; (b) foot landings near the lateral side edge of the staircase; (c) payload swing from the imperfect hook-style end-effector attachment. 

We further break down the failure modes of the 10 whole-course trials reported in Table 5 (6/10 overall). The remaining trials split across three categories (Figure 14): 

**(a,b) Foot landings near terrain edges.** The 21 cm foot leaves little margin against the 25 cm stones (a) and the 1.2 m-wide staircase (b); small noise or drift pushes landings to the boundary. The Stage-1 foot-edge penalty mitigates but does not eliminate this; a stricter edge-avoidance reward would help. 

**(c) Payload swing.** Our passive hook lets the payload swing, shifting the CoM beyond the Stage-1 force curriculum—the single payload-trial failure falls under this mode. Mitigations: a pinching gripper or an end-effector stabilization term [32]. 

## **5 Conclusion** 

We propose RPL, a two-stage learning framework for multi-directional humanoid perceptive locomotion over complex terrains and remain robust with payloads. RPL first trains terrain-specialized expert policies with privileged height-map observations to learn decoupled locomotion and manipulation, and then distills them into a single depth-based transformer policy that fuses multi-view depth inputs. Our parallel depth renderer efficiently ray-casts dynamic robot and static terrain meshes with realistic latency, noise, and dropout, achieving 5 _×_ speedup over existing simulation renderers. We further introduce DFSV and RSM to improve robustness under asymmetric multi-view observations and unseen terrain widths. Extensive simulation and real-world experiments on the Unitree G1 demonstrate robust and long-horizon back-and-forth locomotion across challenging terrains. 

## **6 Limitations** 

Despite its strong performance, RPL has two main limitations. First, we do not demonstrate realworld sideways locomotion in this paper, as achieving high-level sideways performance on discrete terrains such as stepping stones, remains non-trivial for both the expert training and the distillation. Second, while DFSV improves robustness with fixed cameras but does not explicitly learn active viewpoint selection for highly occluded or ambiguous loco-manipulation scenarios. 

11 

## **References** 

- [1] Y. Zhang, Y. Yuan, P. Gurunath, I. Gupta, S. Omidshafiei, A.-a. Agha-mohammadi, M. Vazquez-Chanlatte, L. Pedersen, T. He, and G. Shi. Falcon: Learning force-adaptive humanoid loco-manipulation. <u>arXiv preprint arXiv:2505.06776, 2025.</u> 

- [2] Q. Ben, F. Jia, J. Zeng, J. Dong, D. Lin, and J. Pang. HOMIE: humanoid loco-manipulation with isomorphic exoskeleton cockpit. <u>CoRR, abs/2502.13013, 2025.</u> doi:10.48550/ARXIV.2 502.13013. URL https://doi.org/10.48550/arXiv.2502.13013. 

- [3] M. Ji, X. Peng, F. Liu, J. Li, G. Yang, X. Cheng, and X. Wang. Exbody2: Advanced expressive humanoid whole-body control. <u>arXiv preprint arXiv:2412.13196, 2024.</u> 

- [4] X. Cheng, Y. Ji, J. Chen, R. Yang, G. Yang, and X. Wang. Expressive whole-body control for humanoid robots. <u>arXiv preprint arXiv:2402.16796, 2024.</u> 

- [5] M. Sombolestan and Q. Nguyen. Adaptive force-based control of dynamic legged locomotion over uneven terrain. <u>IEEE Transactions on Robotics, 2024.</u> 

- [6] N. Fey, G. B. Margolis, M. Peticco, and P. Agrawal. Bridging the sim-to-real gap for athletic loco-manipulation. <u>arXiv preprint arXiv:2502.10894, 2025.</u> 

- [7] T. He, Z. Luo, X. He, W. Xiao, C. Zhang, W. Zhang, K. Kitani, C. Liu, and G. Shi. Omnih2o: Universal and dexterous human-to-humanoid whole-body teleoperation and learning. <u>arXiv preprint arXiv:2406.08858, 2024.</u> 

- [8] T. He, J. Gao, W. Xiao, Y. Zhang, Z. Wang, J. Wang, Z. Luo, G. He, N. Sobanbab, C. Pan, et al. Asap: Aligning simulation and real-world physics for learning agile humanoid wholebody skills. <u>arXiv preprint arXiv:2502.01143, 2025.</u> 

- [9] J. Li, J. Ma, O. Kolt, M. Shah, and Q. Nguyen. Dynamic loco-manipulation on hector: Humanoid for enhanced control and open-source research. <u>arXiv preprint arXiv:2312.11868,</u> 2023. 

- [10] M. Murooka, K. Chappellet, A. Tanguy, M. Benallegue, I. Kumagai, M. Morisawa, F. Kanehiro, and A. Kheddar. Humanoid loco-manipulations pattern generation and stabilization control. <u>IEEE Robotics and Automation Letters, 6(3):5597–5604, 2021.</u> 

- [11] K. Bouyarmane, K. Chappellet, J. Vaillant, and A. Kheddar. Quadratic programming for multirobot and task-space force control. <u>IEEE Transactions on Robotics, 35(1):64–77, 2018.</u> 

- [12] Z. Fu, Q. Zhao, Q. Wu, G. Wetzstein, and C. Finn. Humanplus: Humanoid shadowing and imitation from humans. In <u>Conference on Robot Learning (CoRL), 2024.</u> 

- [13] L. Yang, X. Huang, Z. Wu, A. Kanazawa, P. Abbeel, C. Sferrazza, C. K. Liu, R. Duan, and G. Shi. Omniretarget: Interaction-preserving data generation for humanoid whole-body locomanipulation and scene interaction. <u>arXiv preprint arXiv:2509.26633, 2025.</u> 

- [14] H. Wang, Z. Wang, J. Ren, Q. Ben, T. Huang, W. Zhang, and J. Pang. Beamdojo: Learning agile humanoid locomotion on sparse footholds. <u>arXiv preprint arXiv:2502.10363, 2025.</u> 

- [15] X. Cheng, K. Shi, A. Agarwal, and D. Pathak. Extreme parkour with legged robots. In <u>2024 IEEE International Conference on Robotics and Automation (ICRA),</u> pages 11443–11450. IEEE, 2024. 

- [16] Z. Zhuang, S. Yao, and H. Zhao. Humanoid parkour learning. <u>arXiv preprint arXiv:2406.10759, 2024.</u> 

- [17] J. Long, J. Ren, M. Shi, Z. Wang, T. Huang, P. Luo, and J. Pang. Learning humanoid locomotion with perceptive internal model. In <u>2025 IEEE International Conference on Robotics and Automation (ICRA), pages 9997–10003. IEEE, 2025.</u> 

12 

- [18] Q. Ben, B. Xu, K. Li, F. Jia, W. Zhang, J. Wang, J. Wang, D. Lin, and J. Pang. Gallant: Voxel grid-based humanoid locomotion and local-navigation across 3d constrained terrains. <u>arXiv preprint arXiv:2511.14625, 2025.</u> 

- [19] D. Hoeller, N. Rudin, D. Sako, and M. Hutter. Anymal parkour: Learning agile navigation for quadrupedal robots. <u>Science Robotics, 9(88):eadi7566, 2024.</u> 

- [20] J. Sun, G. Han, P. Sun, W. Zhao, J. Cao, J. Wang, Y. Guo, and Q. Zhang. Dpl: Depthonly perceptive humanoid locomotion via realistic depth synthesis and cross-attention terrain reconstruction. <u>arXiv preprint arXiv:2510.07152, 2025.</u> 

- [21] W. Sun, B. Cao, L. Chen, Y. Su, Y. Liu, Z. Xie, and H. Liu. Learning perceptive humanoid locomotion over challenging terrain. <u>arXiv preprint arXiv:2503.00692, 2025.</u> 

- [22] Z. Wang, T. Ma, Y. Jia, X. Yang, J. Zhou, W. Ouyang, Q. Zhang, and J. Liang. Omniperception: Omnidirectional collision avoidance for legged locomotion in dynamic environments. <u>arXiv preprint arXiv:2505.19214, 2025.</u> 

- [23] R. Yang, M. Zhang, N. Hansen, H. Xu, and X. Wang. Learning vision-guided quadrupedal locomotion end-to-end with cross-modal transformers. <u>arXiv preprint arXiv:2107.03996, 2021.</u> 

- [24] J. He, C. Zhang, F. Jenelten, R. Grandia, M. B¨acher, and M. Hutter. Attention-based map encoding for learning generalized legged locomotion. <u>Science Robotics,</u> 10(105):eadv3604, 2025. 

- [25] T. Miki, J. Lee, J. Hwangbo, L. Wellhausen, V. Koltun, and M. Hutter. Learning robust perceptive locomotion for quadrupedal robots in the wild. <u>Science robotics, 7(62):eabk2822, 2022.</u> 

- [26] S. Zhu, Z. Zhuang, M. Zhao, K.-Y. Lee, and H. Zhao. Hiking in the wild: A scalable perceptive parkour framework for humanoids. <u>arXiv preprint arXiv:2601.07718, 2026.</u> 

- [27] A. Agarwal, A. Kumar, J. Malik, and D. Pathak. Legged locomotion in challenging terrains using egocentric vision. In <u>Conference on robot learning, pages 403–415. PMLR, 2023.</u> 

- [28] J. Lee, J. Hwangbo, L. Wellhausen, V. Koltun, and M. Hutter. Learning quadrupedal locomotion over challenging terrain. <u>Science robotics, 5(47):eabc5986, 2020.</u> 

- [29] H. Song, H. Zhu, T. Yu, Y. Liu, M. Yuan, W. Zhou, H. Chen, and H. Li. Gait-adaptive perceptive humanoid locomotion with real-time under-base terrain reconstruction. <u>arXiv preprint arXiv:2512.07464, 2025.</u> 

- [30] M. S. Gadde, P. Dugar, A. Malik, and A. Fern. No more blind spots: Learning vision-based omnidirectional bipedal locomotion for challenging terrain. In <u>2025 IEEE-RAS 24th International Conference on Humanoid Robots (Humanoids), pages 601–608. IEEE, 2025.</u> 

- [31] D. Wang, X. Wang, X. Liu, J. Shi, Y. Zhao, C. Bai, and X. Li. More: Mixture of residual experts for humanoid lifelike gaits learning on complex terrains. <u>arXiv preprint arXiv:2506.08840,</u> 2025. 

- [32] Y. Li, Y. Zhang, W. Xiao, C. Pan, H. Weng, G. He, T. He, and G. Shi. Hold my beer: Learning gentle humanoid locomotion and end-effector stabilization control. In <u>RSS 2025 Workshop on Whole-body Control and Bimanual Manipulation: Applications in Humanoids and Beyond,</u> 2025. 

- [33] Z. Ding, H. Jiang, Y. Wang, Z. Sun, Y. Zhang, X. Niu, M. Yang, W. Zeng, X. Xu, and Z. Lu. Jaeger: Dual-level humanoid whole-body controller. <u>arXiv preprint arXiv:2505.06584, 2025.</u> 

- [34] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov. Proximal policy optimization algorithms. <u>CoRR, abs/1707.06347, 2017.</u> URL http://arxiv.org/abs/1707.063 47. 

13 

- [35] L. Pinto, M. Andrychowicz, P. Welinder, W. Zaremba, and P. Abbeel. Asymmetric actor critic for image-based robot learning. <u>arXiv preprint arXiv:1710.06542, 2017.</u> 

- [36] M. Mittal, N. Rudin, V. Klemm, A. Allshire, and M. Hutter. Symmetry considerations for learning task symmetric robot policies. In <u>2024 IEEE International Conference on Robotics and Automation (ICRA), pages 7433–7439. IEEE, 2024.</u> 

- [37] J. Li, X. Cheng, T. Huang, S. Yang, R.-Z. Qiu, and X. Wang. Amo: Adaptive motion optimization for hyper-dexterous humanoid whole-body control. <u>arXiv preprint arXiv:2505.03738,</u> 2025. 

- [38] S. Ross, G. Gordon, and D. Bagnell. A reduction of imitation learning and structured prediction to no-regret online learning. In <u>Proceedings of the fourteenth international conference on artificial intelligence and statistics, pages 627–635. JMLR Workshop and Conference Proceed-</u> ings, 2011. 

- [39] M. Macklin. Warp: A high-performance python framework for gpu simulation and graphics. In <u>NVIDIA GPU Technology Conference (GTC), volume 3, 2022.</u> 

- [40] M. Kulkarni, W. Rehberg, and K. Alexis. Aerial gym simulator: A framework for highly parallelized simulation of aerial robots. <u>IEEE Robotics and Automation Letters, 2025.</u> 

- [41] V. Makoviychuk, L. Wawrzyniak, Y. Guo, M. Lu, K. Storey, M. Macklin, D. Hoeller, N. Rudin, A. Allshire, A. Handa, and G. State. Isaac gym: High performance GPU based physics simulation for robot learning. In J. Vanschoren and S. Yeung, editors, <u>Proceedings of the Neural Information Processing Systems Track on Datasets and Benchmarks 1, NeurIPS Datasets and Benchmarks 2021, December 2021, virtual, 2021.</u> URL https://datasets-benchma rks-proceedings.neurips.cc/paper/2021/hash/28dd2c7955ce926456 240b2ff0100bde-Abstract-round2.html. 

- [42] M. Mittal, C. Yu, Q. Yu, J. Liu, N. Rudin, D. Hoeller, J. L. Yuan, R. Singh, Y. Guo, H. Mazhar, et al. Orbit: A unified simulation framework for interactive robot learning environments. <u>IEEE Robotics and Automation Letters, 8(6):3740–3747, 2023.</u> 

- [43] E. Todorov, T. Erez, and Y. Tassa. Mujoco: A physics engine for model-based control. In <u>2012 IEEE/RSJ International Conference on Intelligent Robots and Systems, IROS 2012, Vilamoura, Algarve, Portugal, October 7-12, 2012, pages 5026–5033. IEEE, 2012.</u> doi:10.110 9/IROS.2012.6386109. URL https://doi.org/10.1109/IROS.2012.6386109. 

- [44] Z. Wu, X. Huang, L. Yang, Y. Zhang, X. Chen, P. Abbeel, R. Duan, A. Kanazawa, C. Sferrazza, G. Shi, and C. K. Liu. Perceptive humanoid parkour: Chaining dynamic human skills via motion matching. <u>arXiv preprint arXiv:2602.15827, 2026.</u> 

- [45] T. Yu, S. Kumar, A. Gupta, S. Levine, K. Hausman, and C. Finn. Gradient surgery for multitask learning. <u>Advances in Neural Information Processing Systems, 33:5824–5836, 2020.</u> 

- [46] Z. Chen, V. Badrinarayanan, C.-Y. Lee, and A. Rabinovich. Gradnorm: Gradient normalization for adaptive loss balancing in deep multitask networks. In <u>International Conference on Machine Learning, pages 794–803, 2018.</u> 

- [47] B. Liu, X. Liu, X. Jin, P. Stone, and Q. Liu. Conflict-averse gradient descent for multi-task learning. <u>Advances in Neural Information Processing Systems, 34:18878–18890, 2021.</u> 

14 

## **A Appendix** 

### **A.1 Notation Summary** 

Table 6: Notation summary. 

|Symbol|Meaning|
|---|---|
||**Proprioception**|
|**_s_**<sup>_p_</sup><br>_t_|Proprioceptive history|
|**_q_**_t−_4:_t_|Joint positions history|
|˙**_q_**_t−_4:_t_<br>**_ω_**<sup>root</sup><br>_t−_4:_t_|Joint velocities history<br>Root angular velocity history|
|**_g_**_t−_4:_t_|Gravity vector history|
|**_a_**_t−_5:_t−_1|Action history|
||**Goals**|
|**_G_**<sup>_l_</sup><br>_t_<br>**_v_**<sup>lin</sup><br>_t_|Lower-body locomotion goals<br>Linear velocity command|
|**_w_**<sup>yaw</sup><br>_t_<br>**_ϕ_**<sup>stance</sup><br>_t_|Angular velocity command<br>Stance/walking mode command|
|**_h_**<sup>root</sup><br>_t_|Root height command|
|**_o_**<sup>torso</sup><br>_t_|Torso orientation command|
|**_G_**<sup>_u_</sup><br>_t_|Upper-body manipulation goals|
|**_q_**upper_,t_|Upper-body joint target|
||**Perceptual Observation**|
|**_H_**_t_|Privileged height map|
|**_D_**_t_<br>|Multi-view depth observation|
|**_d_**<sup>(</sup><sup>_i_)</sup><br>_t_|Depth image from camera_i_at time_t_|
|_N_cam|Number of depth cameras|


### **A.2 Domain Randomization** 

Table 7: Domain randomization terms during distillation. 

|Term|Value|
|---|---|
|**Dynamics Ra**<br>|**ndomization**<br>|
|Friction|_U_(0_._5_,_1_._25)|
|Link mass|_U_(0_._9_,_1_._2)_×_default kg|
|Base mass|_U_(_−_1_._0_,_3_._0)kg|
|Base COM range|_x ∼U_(_−_0_._025_,_0_._025)m<br>_y ∼U_(_−_0_._05_,_0_._05)m<br>_z ∼U_(_−_0_._05_,_0_._05)m|
|Control delay|_U_(0_,_20)ms|
|**Perception Randomiza**|**tion(Depth Cameras)**|
|Depth cam translation|_x ∼U_(_−_0_._025_,_0_._025)m<br>_y ∼U_(_−_0_._025_,_0_._025)m|
||_z ∼U_(_−_0_._025_,_0_._025)m|
|Depth cam rotation (Euler)|_ϕ ∼U_(_−_2_._5_,_2_._5)<sup>_◦_</sup>|
||_θ ∼U_(_−_3_._0_,_3_._0)<sup>_◦_</sup><br>_ψ ∼U_(_−_2_._5_,_2_._5)<sup>_◦_</sup>|
|Depth cam FOV|∆FOV_∼U_(_−_2_._0_,_2_._0)<sup>_◦_</sup>|
|Pixel dropout|_p_drop = 0_._05|
|Depth noise|_σd_ = 0_._1_·_depth|


15 

