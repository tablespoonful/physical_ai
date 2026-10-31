---
title: "Scalable and General Whole-Body Control for Cross-Humanoid Locomotion"
date: "2026-02-05"
authors: "Yufei Xue; YunFeng Lin; Wentao Dong; Yang Tang; Jingbo Wang; Jiangmiao Pang"
url: https://arxiv.org/abs/2602.05791
pdf: https://arxiv.org/pdf/2602.05791
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.05791)** / [論文ページ](https://arxiv.org/abs/2602.05791)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**Scalable and General Whole-Body Control for Cross-Humanoid Locomotion** 

**Yufei Xue**<sup>* 1 2</sup> **Yunfeng Lin**<sup>* 1 2</sup> **Wentao Dong**<sup>1 2</sup> **Yang Tang**<sup>1 2</sup> **Jingbo Wang**<sup>2</sup> **Jiangmiao Pang**<sup>2</sup> **Ming Zhou**<sup>2</sup> **Minghuan Liu**<sup>1</sup> **Weinan Zhang**<sup>1 2</sup> 

https://xhugwbc.github.io 


_Figure 1._ **Zero-shot generalization and real-world humanoid capabilities enabled by XHugWBC’s generalist policy. First row:** Robust zero-shot generalization across seven humanoids with diverse DoFs, dynamic characteristics, and morphological structures. **Second row:** flexible teleoperation using XHugWBC enables long-horizon whole-body loco-manipulation tasks. 

# **Abstract** 

Learning-based whole-body controllers have become a key driver for humanoid robots, yet most existing approaches require robot-specific training. In this paper, we study the problem of crossembodiment humanoid control and show that a single policy can robustly generalize across a wide range of humanoid robot designs with one-time training. We introduce XHugWBC, a novel crossembodiment training framework that enables generalist humanoid control through: (1) physicsconsistent morphological randomization, (2) semantically aligned observation and action spaces across diverse humanoid robots, and (3) effective policy architectures modeling morphological 

> * Equal contributions: Yufei Xue and Yunfeng Lin. 

> 1Shanghai Jiao Tong University 2Shanghai AI Laboratory. Correspondence to: Weinan Zhang _<_ wnzhang@sjtu.edu.cn _>_ , Minghuan Liu _<_ minghuanliu@sjtu.edu.cn _>_ , Ming Zhou _<_ zhouming@pjlab.org.cn _>_ . 

_Proceedings of the 43_<sup>_rd_</sup> _International Conference on Machine Learning_ , Seoul, South Korea. PMLR 306, 2026. Copyright 2026 by the author(s). 

and dynamical properties. XHugWBC is not tied to any specific robot. Instead, it internalizes a broad distribution of morphological and dynamical characteristics during training. By learning motion priors from diverse randomized embodiments, the policy acquires a strong structural bias that supports zero-shot transfer to previously unseen robots. Experiments on twelve simulated humanoids and seven real-world robots demonstrate the strong generalization and robustness of the resulting universal controller. 

# **1. Introduction** 

Learning-based whole-body control (WBC) has become a dominant paradigm for legged robots, especially humanoids, enabling agile and robust behaviors beyond conventional model-based controllers (Cheng et al., 2024a; He et al., 2024; Liao et al., 2025; Xue et al., 2025; Yang et al., 2025a; Li et al., 2025). However, most existing controllers target a single embodiment (Pan et al., 2025; Chen et al., 2025b), requiring extensive retraining when transferred to new platforms. This limits scalability as each new robot differs in 

1 

**Scalable and General Whole-Body Control for Cross-Humanoid Locomotion** 

morphology, kinematics, and dynamics, making per-robot training costly and inefficient. A key open question therefore remains: **can a single learned controller generalize across diverse humanoid embodiments?** 

Achieving this is challenging due to highly dynamic contacts, strict stability requirements, and large morphological variations. Prior cross-embodiment efforts in animation (Gupta et al., 2022; Huang et al., 2020) and locomotion (Yang et al., 2025b; Liu et al., 2025a) rely on shared morphological priors, unified state-action representations, or similar dynamics. Such assumptions break down for humanoids, which diverge substantially in kinematic structure, degrees of freedom, joint ordering, and physical properties. Simplifications that have facilitated transfer in quadrupeds such as reduced dynamic models or relatively homogeneous body morphologies also break down for humanoids (Feng et al., 2023; Luo et al., 2024), whose morphological diversity and whole-body dynamics are intrinsically more complex. 

To address these challenges, we propose XHugWBC, a framework for learning a cross-humanoid whole-body controller. XHugWBC combines: 1) physically consistent morphological randomization, 2) a unified state-action representation that semantically aligns different embodiments, and 3) a policy architecture modeling embodiment-specific and graphbased representations derived from robot topologies. 

We evaluate XHugWBC across diverse humanoids in simulation and reality. A single generalist policy trained with our framework achieves robust zero-shot whole-body control across seven real-world humanoid robots. In simulation, it scales to twelve distinct embodiments, reaching about 85% of specialist performance, while generalist-initialized finetuning surpasses specialists by up to 10%. These results show that XHugWBC learns strong embodiment-agnostic motion priors and enables scalable, general-purpose humanoid control. Our main contributions are: 

- A physics-consistent morphological randomization that yields diverse and physically meaningful embodiments. 

- A universal embodiment representation with tailored training techniques for cross-humanoid whole-body control. 

- To the best of our knowledge, this is the first generalist controller demonstrating robust zero-shot whole-body control across seven real-world humanoid robots with substantial diversity. 

# **2. Related Work** 

## **2.1. Cross-Embodiment Learning for Legged Robots** 

Cross-embodiment learning aims to find control policies that generalize across robots with different morphologies 

and dynamics, reducing the need for embodiment-specific controllers. Most existing approaches train on a small set of embodiments and achieve limited transfer (Yang et al., 2025b; Lin et al., 2025; Peng et al., 2026; Doshi et al., 2024), or introduce diversity through simple morphological randomization (Yu et al., 2023; Luo et al., 2024; Liu et al., 2025a; Ai et al., 2025). These methods typically assume aligned state-action spaces and similar embodiment dynamics, restricting their applicability to narrower robot families. 

Humanoid robots, however, exhibit heterogeneous structures, physical properties and state representations, thus violating such assumptions. To address this, some efforts resort to biology-inspired trajectory generators (Shafiee et al., 2024), while others represent embodiments with joint-level descriptor sequences (Bohlinger et al., 2024; Ai et al., 2025). In contrast, XHugWBC generates physically consistent embodiment data and leverages a hybrid-mask Transformer to capture broad humanoid motion priors, enabling robust generalization with a single policy. 

## **2.2. Humanoid Whole-Body Control** 

Whole-body control is a critical yet challenging task for humanoid robot learning and real-world applications. Recent work has explored unified command spaces (Xue et al., 2025; Li et al., 2025; Sun et al., 2025; Zhang et al., 2026), typically using command sampling and reinforcement learning. Other studies focus on motion tracking and representation learning from individual demonstrations (Xie et al., 2025; He et al., 2025; Huang et al., 2025) or large-scale datasets (Yin et al., 2025; Zhang et al., 2025; Ze et al., 2025; Luo et al., 2025), but often assume fixed robot morphologies. Additional progress has been made in whole-body loco-manipulation within controlled environments (Wang et al., 2025b; Weng et al., 2025; Su et al., 2025; Chen et al., 2025a; Zhuang & Zhao, 2025). 

Our work follows Xue et al. (2025) and adopts a unified command space to enable expressive whole-body behaviors while explicitly targeting cross-humanoid generalization. 

# **3. Method** 

## **3.1. Physics-Consistent Morphological Randomization** 

With the success of domain randomization (Peng et al., 2018; Hwangbo et al., 2019; Miki et al., 2022; Wu et al., 2023) in training robust whole-body controllers (Xue et al., 2025; Zeng et al., 2025; Wang et al., 2025a), a straightforward approach for learning cross-humanoid policies is to randomize embodied data (Feng et al., 2023; Bohlinger et al., 2024) across kinematic, dynamic, and morphological dimensions. However, a robot’s inertial parameters must satisfy physical consistency (Traversaro et al., 2016) to represent plausible rigid bodies, making the feasible parame- 

2 

**Scalable and General Whole-Body Control for Cross-Humanoid Locomotion** 


_Figure 2._ **Training framework of XHugWBC.** ( **a** ) **Data generation** : physics-consistent morphological randomization produces diverse and physically meaningful embodiments. ( **b** ) **Universal embodiment representation** : robot-specific states are projected into a global joint space, upon which an embodiment graph is constructed. ( **c** ) **Policy learning** : the generalist policy uses a GCN- or Transformer-based encoder together with a state estimator. ( **d** ) **Deployment** : the learned policy generalizes to seven humanoid robots with different kinematic, dynamic, and morphological structures in zero-shot. 

ter space inherently non-convex and discontinuous. Prior work on physics-based simulation and legged locomotion often overlooks this requirement, either because experiments are conducted entirely in simulation or because robot links are approximated using simple geometric primitives whose dynamics are scaled in a linear and often physically invalid manner (Trabucco et al., 2022; Ai et al., 2025). For humanoid robots with highly complex and heterogeneous structures, perturbing inertial parameters without enforcing physical consistency can easily produce unrealizable models, destabilize simulation, drive policy optimization toward degeneracy, and ultimately cause catastrophic failures in sim-to-real transfer. We therefore introduce physicsconsistent morphological randomization to generate diverse and plausible embodied data. 

**Parameterizing a template robot.** We capture the shared structures of humanoid robots in a template model and define a parameter vector that encodes its kinematic layout, link geometries, inertial properties, and joint configurations. 


where **_κ_** link _∈_ R<sup>10</sup><sup>_nb_</sup> are parameters of robot links, **_κ_** joint _∈_ R<sup>13</sup><sup>_nd_</sup> are parameters of robot joints, _nb ∈_ N+ and _nd ∈_ N+ are the number of the rigid bodies and the number of degrees of freedom, respectively. In detail, **_κ_** link = � **_κ_**<sup>1</sup> l _⊤, . . . ,_ **_κ_** _n_ l _b ⊤_<sup>�</sup><sup>_⊤_</sup> represents the contributions from each rigid body, each **_κ_**<sup>i</sup> l<sup>correspondstotheinertial</sup> parameters of the _i_ -th rigid body and is composed of 

[ _m, hx, hy, hz, Ixx, Iyy, Izz, Ixy, Ixz, Iyz_ ]<sup>_⊤_</sup> _∈_ R<sup>10</sup> 

where _m_ denotes the mass, **h** = [ _hx, hy, hz_ ]<sup>_⊤_</sup> = _m_ **c** is the first mass moments, where **c** _∈_ R<sup>3</sup> denotes the center-of- 

mass (CoM) coordinates in the body frame, and 


is the rotational inertia w.r.t. the coordinate origin. Similarly, joint parameters **_κ_** joint represent the contributions from each joint and can be expressed as **_κ_** joint = � **_κ_**<sup>1</sup> j _⊤, . . . ,_ **_κ_** _n_ j _d ⊤_<sup>�</sup><sup>_⊤_</sup> , where each **_κ_**<sup>i</sup> j<sup>connects a parent link and a child link, and is</sup> defined by both spatial and dynamic parameters 


where the **p** = [ _px, py, pz_ ] specifies the joint position in the parent frame, **e** = [ _ϕ, θ, ψ_ ] represent its orientation, **a** = [ _ax, ay, az_ ] defines the motion axis, and _q_ min, _q_ max, _q_ ˙max and _τ_ max denote the range of motion, maximum velocity and torque, respectively. For randomizing morphologies, intuitively, we can apply perturbations within this morphological space of the template robot: 


where _D_ morph is noise distribution. Nevertheless, adding ∆ **_κ_** is non-trivial, as arbitrary noise can break physical consistency. To achieve reasonable morphology randomization, we reparameterize the morphological space into a form that we can easily add noise to. 

**Reparameterizing the link space.** We first derive a physics-consistent randomization solution for the link space, which mainly consists of inertial parameters. 

3 

**Scalable and General Whole-Body Control for Cross-Humanoid Locomotion** 

**Definition 3.1** (Physics-Consistent Inertial Parameters) **.** A rigid body’s inertial parameters _κ_ link are said to be physically consistent if its pseudo-inertia matrix 


is symmetric positive definite, where **Σ** =<sup><u>1</u></sup> 2<sup>Tr(¯</sup><sup>**I**)</sup><sup>**I**</sup><sup>_−_¯</sup><sup>**I**.</sup> 

Recall that the pseudo-inertia matrix admits the integral form (Traversaro et al., 2016) as 


and the positive definiteness constraint **J** _≻_ 0 can be enforced via linear matrix inequalities (Rucker et al., 2022). **Lemma 3.2** (Cholesky-Level Parameterization) **.** _If_ **J** _≻_ 0 _, then there exists a unique upper-triangular matrix_ **L** _with positive diagonal entries such that_ 


Lemma 3.2 implies that any physically consistent inertia matrix can be smoothly parameterized by its Cholesky factor **L** . Therefore, physics-consistent randomization can be implemented by perturbing **L** as 


where _D_ denotes a noise distribution. To provide geometric interpretability of such perturbations, we further examine how the pseudo-inertia transforms under affine deformations of the rigid body. 

**Lemma 3.3** (Affine Transformation of Pseudo-Inertia) **.** _Under an affine transformation of homogeneous body coordinates_ **q**<sup>_′_</sup> = **Eq** _and a mass density scaling ρ_<sup>_′_</sup> = _β_<sup>2</sup> _ρ, the pseudo-inertia matrix transforms as_ 


_where_ **U** = _β_ **E** _and_ **q** = [ **x** _,_ 1]<sup>_⊤_</sup> _._ 

Combining Lemma 3.2 and Lemma 3.3, any physically consistent inertia perturbation can be expressed as 


**Lemma 3.4** (R<sup>10</sup> Bijective Mapping of Inertia) **.** _The transformation matrix_ **U** _∈ GL_<sup>+</sup> (4) _admits a unique uppertriangular factorization with positive diagonal entries. Moreover, parameterizing the diagonal entries via exponential maps yields a bijection between such_ **U** _and a 10dimensional real vector_ 

_θinert_ = [ _α, d_ 1 _, d_ 2 _, d_ 3 _, s_ 12 _, s_ 23 _, s_ 13 _, t_ 1 _, t_ 2 _, t_ 3]<sup>_⊤_</sup> _∈_ R<sup>10</sup> _,_ (8) _where the explicit matrix form of_ **U** _is given in Appendix A.1._ 

**Proposition 3.5** (Smooth Physics-Consistent Randomization) **.** _Under Lemma 3.2–3.4, any physically consistent inertia perturbation_ **J**<sup>_′_</sup> _≻_ 0 _can be written as_ 


_where_ **U** _is uniquely determined by θinert ∈_ R<sup>10</sup> _._ 

Proof of proposition 3.5 is in Appendix A.1. Consequently, physics-consistent randomization of inertial parameters can be performed by unconstrained perturbations in R<sup>10</sup> , while preserving physical feasibility and smoothness of the parameter space. 

**Reparameterizing the joint space.** joint parameters are typically constrained by the overall physical and structural design of the robot. Therefore, we perform joint space randomization over _joint rotational axes_ , _joint position_ , and _joint actuation_ . In particular, 1) we randomize the orientation of the hip joint’s rotational axis **a** = [ _ax, ay, az_ ], which enables the synthesis of a wide range of kinematically distinct hip configurations. The remaining joints follow a similar arrangement sequence across platforms. 2) We randomize joint position **p** = [ _px, py, pz_ ] relative to the parent link’s frame, with magnitudes bounded within twice the distance to the link’s center of mass. For motor control, the proportional-derivative (PD) gains and torque limits _τ_ max are linearly scaled with the total mass of the robot as a heuristic approximation to maintain consistent actuation behavior across morphologies. 3) We randomize the actuation type by sampling selected joints as either _revolute_ or _fixed_ , where fixed joints are rigidly locked and excluded from control. Joints subject to this randomization include three waist joints (roll, yaw, and pitch), seven arm joints (shoulder roll, yaw, and pitch; elbow pitch; and wrist roll, yaw, and pitch), and three head joints (roll, yaw, and pitch). As a result, the controller can operate on robots with widely varying degrees of freedom, ranging from a minimum of 12 active joints, corresponding to a pure bipedal configuration with three hip joints (roll, yaw, pitch), one knee joint, and two ankle joints (pitch, roll) per leg, to a maximum of 32 active joints, which additionally include three waist joints, two arms with seven joints each, and three head joints. Detailed randomization ranges are provided in Appendix A.2. 

## **3.2. Universal Cross-Embodiment Representation** 

Our goal is to develop a unified control policy across various morphologically diverse humanoid robots, each characterized by unique kinematic morphologies and differing numbers of actuated joints. A key challenge lies in the significant heterogeneity in their respective state and action spaces. To address this, we map robot-specific joint states into a global joint space for semantic alignment, and construct an embodiment graph on top of this global space to explicitly encode morphological structure. 

4 

**Scalable and General Whole-Body Control for Cross-Humanoid Locomotion** 

**Joint space semantic alignment.** (Lin et al., 2025) proposes a hardware-agnostic joint space mapping that standardizes joint representations across embodiments, enabling a consistent robot control interface. Following this idea, we define a canonical joint dimension of _N_ max = 32, where each index corresponds to a semantically aligned joint in a globally defined ordering. For any humanoid robot, its joints are embedded into this canonical space according to their kinematic roles and semantic identities. Formally, for a robot instance with _Nr ≤ N_ max joints and their configuration **q** _r ∈_ R<sup>_Nr_</sup> , we define a mapping 


such that the canonical joint state **q** global is constructed as: 


The resulting **q** global _∈_ R<sup>_N_max</sup> is a zero-padded, canonical representation shared across all embodiments. By enforcing semantic alignment at the joint level, the control policy receives fixed-dimensional inputs regardless of morphological variations or differences in actuation. The global joint index definition is provided in Table 8. 

**Graph-based morphology description.** The unified representation above naturally supports constructing a graphbased description of each robot’s morphology. Each embodiment represented by **q** global can be converted to a directed kinematic graph: _G_ = ( _V, E_ ), where the vertex set _V_ = ( _v_ 1 _, v_ 2 _, . . . , vi_ ) corresponds to joints, and the edge set 


captures rigid-body connections, where each edge _eij_ encodes the linkage between joint _vi_ and _vj_ . The adjacency matrix **A** _∈{_ 0 _,_ 1 _}_<sup>_N_max</sup><sup>_×N_max</sup> is constructed from _E_ and encodes the overall connectivity of the embodiment: 


Humanoid robots often adopt parallel-linkage mechanisms, which complicate graph construction. To address this, we collapse all nodes involved in a parallel linkage and connect them directly to the preceding joint in the articulation. For instance, ankle joints are treated as immediate children of the knee joint in the resulting graph. The final graph _G_ for each robot is connected and acyclic, forming a kinematic tree whose vertices may represent either actuated or fixed joints. This structure is expressive enough to encode diverse kinematic and actuation patterns, as well as morphological information for general control. Figure 2 (b) illustrates the mapping from the joint-level description to its corresponding adjacency matrix. 

## **3.3. Cross-Humanoid Learning** 

With physics-consistent morphological randomization and universal representation of structurally distinct robots, we proceed to develop a training strategy for a cross-humanoid control policy. We formulate the problem as a reinforcement learning task defined over a family of morphologically diverse robots _k ∼K_ . Each robot instance _k_ is modeled as a Partially Observable Markov Decision Process (POMDP): 


where _Sk_ , _Ok_ and _Ak_ denote the state, observation, and action subspaces of robot _k_ , represented in a universal space. _Rk_ is the reward function, and _γ_ is the discount factor. The learning objective is to optimize a single policy that maximizes the expected return over all embodiments: 


**Observation.** Following (Xue et al., 2025), the policy observation _o_<sup>_π_</sup> _t_<sup>at timestep</sup><sup>_t_consists of a five-step history of</sup> proprioception _o_<sup>_P_</sup> _t−_ 4: _t_<sup>, a joint controllability indicator</sup><sup>_I_(</sup><sup>_t_),</sup> and a whole-body command vector _ct_ . The proprioception observation _o_<sup>_P_</sup> _t_<sup>is defined as:</sup> 


where _ωt ∈_ R<sup>3</sup> is base angular velocity, g _t ∈_ R<sup>3</sup> is base gravity direction, _qt ∈_ R<sup>32</sup> and _q_ ˙ _t ∈_ R<sup>32</sup> are joint positions and velocities respectively, and _at−_ 1 _∈_ R<sup>32</sup> is the previous action. The binary indicator _I_ ( _t_ ) specifies which joints are controllable. The command vector _ct_ is defined as: 


where _vt_<sup>_x, v_</sup> _t_<sup>_y_and</sup><sup>_ω_</sup> _t_<sup>_z_are the target base velocity,</sup><sup>_ht_is the</sup> target base height, _pt_ is the target pelvis angle, _θt_<sup>_y_,</sup><sup>_θ_</sup> _t_<sup>_p_and</sup> _θt_<sup>_r_stand for the waist yaw, pitch and roll rotations, and the</sup> remaining terms control gait parameters. We further incorporate an upper-body intervention training scheme to control the arm joints for achieving whole-body loco-manipulation tasks. An intervention indicator function I( _t_ ) = _{_ 0 _,_ 1 _}_ is introduced to denote whether an external upper-body controller is active. When I( _t_ ) = 1, the upper body is driven by an external controller (e.g., teleoperation signals), while the policy still observes these states and adapts lower-body behavior for balance. When I( _t_ ) = 0, the upper body is controlled by our whole-body controller. This command space ensures flexible whole-body control for versatile locomotion (Xue et al., 2025). To incorporate the structural information encoded by the robot’s graph description, we explore two encoder architectures: Graph Convolutional 

5 

**Scalable and General Whole-Body Control for Cross-Humanoid Locomotion** 

_Table 1._ **Average command tracking errors and survival rates aggregated across all robots.** We compare XHugWBC with specialist <u>(HugWBC (Xue et al., 2025)) denoting the upper-bound performance, which is trained and evaluated on specific robots separately.</u> 

||_Survival_||_Task Comma_|_nds_|||_Behavior Comm_|_ands_||
|---|---|---|---|---|---|---|---|---|---|
||_E_surv(%)|_E_vx(m_/_s)|_E_vy(m_/_s)|_Eω_(rad_/_s)|_E_h(m)|_E_p(_rad_)|_Eθ_y(rad)|_Eθ_p(rad)|_Eθ_r(rad)|
|Specialists (Xue et al.(2025))|100|0.060 (_±_0_._04|3)<br>0.079 (_±_0_._03|9)<br>0.121 (_±_0_._057|)<br>0.044 (_±_0_._022|)<br>0.138 (_±_0_._0|89)<br>0.062 (_±_0_._04|1)<br>0.037 (_±_0_._02|6)<br>0.048 (_±_0_._025)|
|Generalist (XHugWBC)|100|0.084 (_±_0_._04|2)<br>0.116 (_±_0_._02|2)<br>0.160 (_±_0_._021|)<br>0.044 (_±_0_._023|)<br>0.097 (_±_0_._0|39)<br>0.043 (_±_0_._02|8)<br>0.052 (_±_0_._02|7)<br>0.049 (_±_0_._008)|


Networks (GCN) (Kipf & Welling, 2017) and Transformers (Vaswani et al., 2017). These encoders model kinematic neighborhoods and produce node features that capture the topology of embodied motion. 

**GCN policy encoder.** To model each robot’s structure, we employ a Graph Convolutional Network (GCN) (Kipf & Welling, 2017) as a relational encoder. It operates on the node features **X** of the robot’s connection graph (see Appendix A.3 for details). We stack multiple GCN layers to progressively aggregate information from local kinematic neighborhoods to higher-order relational contexts, producing structure-aware node features. 

**Transformer policy encoder.** Transformers provide an alternative means for modeling robot structure via sequencebased attention. The input consists of node embeddings augmented with positional encodings: 


where **W** pos _∈_ R<sup>_N_max</sup><sup>_×D_</sup> are the learned positional embeddings. To exploit kinematic structure, we adopt a topologyaware hybrid-mask strategy: the first layer applies masked attention according to the graph, while subsequent layers use unmasked self-attention for global information exchange. This produces topology-aware attention patterns, enabling integration of both local kinematic structure and global coordination. Additional details are provided in Appendix A.3. 

**Critic structure.** The critic network mirrors the actor but omits the state estimator. Its detokenizer outputs a value estimate for each joint node, and the final value is computed by averaging across node-wise estimates. During training, the critic additionally receives privileged observations that are unavailable on physical hardware, including pelvis and torso linear velocities, torso height, link-collision pairs, and the robot’s morphological parameters, to ensure stable and accurate value estimation. 

Further architectural details for both the policy and critic networks are provided in Appendix A.3. 

# **4. Experiments** 

We conduct comprehensive evaluations of XHugWBC in both simulation and the real-world environments, guided by the following research questions: 

- **RQ1.** How well does XHugWBC generalize to previously unseen embodiments? 

- **RQ2.** How well can the generalist policy serve as an initialization for fine-tuning on each robot? 

- **RQ3.** How does the proposed framework compare with cross-embodiment baselines? 

- **RQ4.** Which policy architecture is more effective for building a generalist humanoid controller? 

**State estimator.** To mitigate partial observability on real robots, we concurrently train a state estimator to reconstruct privileged information such as base linear velocity and base height. The estimator is optimized via supervised regression, and its outputs serve as the reconstructed privileged information used by the actor detokenizer. This supervised objective is jointly optimized with the RL loss. 

**Action prediction.** The node features produced by the = encoders are concatenated with a global vector _o_<sup>_g_</sup> _t_ [ _wt, gt, ct_ ] and the reconstructed privileged information from the learned state estimator. This fused representation is fed into linear layers to generate per-node joint actions. These node-wise actions are then aggregated into a global action vector and mapped back to the robot’s physical joints through an embodiment-specific inverse mapping function inv( _ϕr_ ) : R<sup>_N_max</sup> _→_ R<sup>_Nr_</sup> . 

- **RQ5.** How does robot performance differ between simulation and real-world deployment? 

## **4.1. Evaluation on Unseen Robots** 

For RQ1, we evaluate how the generalist policy learned by XHugWBC performs on unseen embodiments. Table 1 summarizes results across 12 robots excluded from training, compared with specialist policies trained on each robot. Table 7 provides detailed per-robot results. 

The generalist policy demonstrates strong zero-shot generalization across diverse humanoid robots with substantial variations in kinematics, dynamics, and morphology. All robots evaluated achieve a 100% survival rate and maintain consistently high command-tracking accuracy, without exhibiting bias toward any specific system. While specialist policies remain an upper bound for each individual robot, 

6 

**Scalable and General Whole-Body Control for Cross-Humanoid Locomotion** 


_Figure 3._ **Comparing training curves** of the fine-tuned policies with the generalist policy and specialist policies. 


_Figure 4._ **t-SNE visualization of transformer latent representation.** “-DoF” denotes the number of waist joints DoFs. The arrow ( _←_ ) indicates the direction of increasing robot mass. 

XHugWBC achieves comparable performances across embodiments, with expected trade-offs due to lack of systemspecific priors. Nevertheless, the generalist provides a powerful pretrained initialization, as discussed in Section 4.2. 

**Qualitative Analysis.** To gain insight into how XHugWBC works, we visualize the latent representations produced by the trained transformer before detokenization. Figure 4 shows the t-SNE visualization of the latent vectors. Here, we denote the ordering of the humanoid hip joints, such as **R** oll, **P** itch, and **Y** aw, as **R-P-Y** , with other configurations defined similarly. The results indicate that robot structure shapes the embedded latent distribution: robots with similar hip-joint arrangements cluster closely together. 

The number of waist DoFs further modulates the embedding. For example, among robots with the **R-P-Y** hip joint configuration, the robot in yellow (with text **0-DoF** ) has no actuated waist joints and appears near the center of the upper-right ring-shaped cluster. Robots with a single waist DoF (orange, with text **1-DoF** ) form an outer ring, with lighter robots positioned slightly inward (shown in _⋆_ ). In contrast, robots with three waist DoFs (red and purple, with text **3-DoF** ) lie along the outermost boundary. 


_Figure 5._ **Zero-shot survival rate comparison across multiple baselines** . All policies are trained under the same training protocol. Naive Random is trained on data generated by the naive morphological randomization method, whereas XHugWBC, MetaMorph, and MorAL are trained using randomization in Sec. 3.1. 

## **4.2. Fine-tuning the Generalist Policy** 

To investigate RQ2, we conduct per-robot fine-tuning experiments by reusing the learned weights. Figure 3 compares the training curves of i) generalist policy (XHugWBC), ii) embodiment-specific specialist policies ((Xue et al., 2025)), and iii) the fine-tuned generalist policies (Generalist-FT) across 12 embodiments. At convergence, the generalist policy reaches approximately 85% of the return achieved by the specialist. A temporary drop in performance is observed during training, which arises from the curriculum schedule that progressively increases task difficulty. 

On the other hand, fine-tuning the generalist policy yields significantly higher sample efficiency than training from scratch, and converges substantially faster than the other approaches, and fine-tuned generalist rollouts show an approximate 10% improvement in return compared to specialist ones. These results indicate that the learned representations of the generalist are highly adaptable, serving as a strong initialization for efficient specialization while retaining the potential for high-performance control across diverse robots. Table 7 reports the tracking errors for all three policies, showing consistent findings. 

## **4.3. Comparing Cross-Embodiment Baselines** 

For RQ3, Figure 5 also compares XHugWBC with two _crossembodiment training_ baselines, **MetaMorph** (Gupta et al., 

7 

**Scalable and General Whole-Body Control for Cross-Humanoid Locomotion** 

_Table 2._ **Quantitative evaluation of sim-to-real performance gaps.** We zero-shot deploy XHugWBC on seven robots and compare average forward tracking errors between simulation and real-world, additionally computing the relative gap to quantify the discrepancy. 

|_Metrics_|_Booster T1_|_Fourier N1_|_Unitree G1_<br>(23 DoF)|_Unitree G1_<br>(29 DoF)|_Agibot X2_|_Dobot Atom_|_Unitree H1-2_|
|---|---|---|---|---|---|---|---|
|Simulation (m/s)|0.052|0.064|0.051|0.047|0.061|0.063|0.065|
|Real-World (m/s)|0.069|0.093|0.065|0.062|0.098|0.131|0.117|
|Relative Gap (%)|32.69|45.31|27.45|31.91|60.61|107.93|80.00|


_Figure 6._ **Network architecture ablation.** Training curves comparing MLP-, GNN-, and Transformer-based policies, reporting mean episodic return and mean episode length. 

2022) and **MorAL** (Luo et al., 2024) (with the proposed morphology randomization); along with _naive morphology randomization_ (Feng et al., 2023; Ai et al., 2025)( **Naive Random** in short) that approximates the rigid body of the robot as a box-shaped primitive, on zero-shot embodiment generalization. Naive random is trained with the same Transformer architecture as XHugWBC. MetaMorph’s policy relies on explicitly provided morphological information as input, including link inertial properties and joint motion ranges, and it is hard to learn generalizable representations from the high-dimensional, heterogeneous morphological descriptors of humanoid robots. MorAL performs even worse, with a substantial drop in performance observed on most robots, due to the limitations of the simple policy architectures and proprioceptive inputs without informative morphological features. In addition, Naive Random generalizes only to a small subset of embodiments with similar mass distributions and kinematic features, while exhibiting significant performance degradation on the remaining robots. 

Figure 3 further reports the fine-tuned results for MetaMorph and MorAL. While fine-tuning both baselines benefit from improved initialization, their convergence is slower than Generalist-FT. In addition, their peak performance is comparable to that of specialist policies, but consistently lower than that achieved by the fine-tuned generalist. 


_Figure 7._ **Loco-manipulation sequence: plush toy picking, door opening, and traversal.** The robot first walks toward the box on the right and bends to grasp the plush toy. Next, it opens the door with the other hand, walks through, stops in front of the basket, squats, and places the toy inside, then neatly arranges the toys outside the basket. 

formance gain stems from the ability to exploit the robot’s embodied kinematic topology and dependency structure encoded in the embodiment adjacency matrix, leading to more sample-efficient learning. 

In contrast, even when provided with explicit morphological information (Luo et al., 2024), the MLP struggles to capture inter-joint dependencies. This is because a flattened state discards most of the underlying kinematic structure, making it difficult for the policy to infer meaningful relationships among joints. Based on these results, all subsequent experiments adopt the Transformer architecture. 

## **4.4. Network Ablation for the Generalist Controller** 

To answer RQ4, we systematically evaluate different policy network architectures on training convergence and generalization to unseen robots. Figure 6 presents the training curves for MLP-, GNN-, and Transformer-based policies, where **(a)** reports mean episodic return and **(b)** reports mean episode length. Both the GNN and Transformer architectures significantly outperform the MLP baseline. Their per- 

## **4.5. Sim to Real Performance Gap** 

We evaluated XHugWBC on 7 distinct humanoid robot platforms in real-world environments to test its zero-shot generalization and sim to real performance, as shown in Fig. 1. Hardware specifications of each platform are listed in Table 5. Despite large variations in hardware design, physical properties, and kinematic topology, XHugWBC transfers reliably to all platforms and achieves a 100% task success rate. 

8 

**Scalable and General Whole-Body Control for Cross-Humanoid Locomotion** 

These results are consistent with simulation. 

Due to the lack of external ground-truth systems (e.g., motion capture systems). We introduce a simplified evaluation protocol to quantify the embodiment sim-to-real gap. Specifically, we fix the commanded forward velocity to _vx_ = 0 _._ 6 ( _m/s_ ) over a duration of 10 seconds, and measure the average forward velocity tracking error _E_ error in both simulation and the real-world settings. To ensure a consistent evaluation protocol across both domains, the average velocity is computed from the traveled distance over time in both simulation and real-world experiments, and the tracking error is defined accordingly. Each experiment is repeated five times, and the reported results are averaged across all trials. This protocol enables a fair and direct comparison between the two domains. 

The results (shown in the Tab. 2) reveal that while all platforms exhibit performance degradation in the real world, - the magnitude of the relative gap-defined as<sup>_<u>|E</u>_real</sup> _E_<sup>_−_</sup> sim<sup>_E_sim</sup><sup>_<u>|</u>_</sup> varies significantly. Notably, the Booster T1 and Unitree G1 demonstrate superior transferability with relatively small gaps. In contrast, full-size humanoid platforms such as Dobot Atom and Unitree H1-2 show more pronounced discrepancies, which we attribute to hardware factors such as larger gear reduction ratios and increased joint clearances. Interestingly, Fourier N1 and Agibot X2 also exhibit relatively large gaps despite having sizes comparable to Unitree G1, indicating that sim-to-real performance is influenced not only by robot scale but also by platform-specific actuation and mechanical characteristics. 

## **4.6. Loco-Manipulation Real World Experiment** 

Beyond basic locomotion, we further evaluate our method in whole-body control scenarios. Our generalist policy on all robot platforms can robustly and accurately follow fullbody commands issued from real-time teleoperation (Cheng et al., 2024b), producing coordinated whole-body behaviors across diverse embodiments, as illustrated in Fig. 1. 

We also assess the policy on several long-horizon locomanipulation tasks using different robots, including Unitree G1 and H1-2 (shown in Fig. 7). In these tasks, each robot is required to approach the box, bend down to pick up the plush toy, open a door, and finally squat down to place the toy into the basket. These tasks demand precise arm control as well as efficient whole-body posture coordination. Despite these challenges, the policy achieves near-perfect success rates across all tasks. 

# **5. Conclusion** 

We present XHugWBC, a scalable cross-humanoid wholebody controller and training framework that enables zeroshot embodiment generalization. Extensive simulation and 

real-world experiments show that generalist policy transfers robustly across diverse humanoid robots, despite substantial differences in degrees of freedom, dynamics, and kinematic topologies. The learned policy further supports precise and stable control for long-horizon whole-body tasks. 

While effective, XHugWBC relies on a unified command interface in which all robots are driven by control signals with shared semantics. This simplifies the learning process but limits applicability to more expressive control settings. For example, motion tracking requires embodiment-specific retargeting, leading to a mismatch between motion representation and robot morphology. Extending cross-embodiment learning to support expressive, morphology-aware control remains an important direction for future work. 

# **Acknowledgments** 

This work was supported by the Shanghai Municipal Special Program for Basic Research on General AI Foundation Models (Grant No. 2025SHZDZX025D08), in collaboration with Shanghai Artificial Intelligence Laboratory. The SJTU team is partially supported by National Natural Science Foundation of China (62322603). This work was also supported by the Shanghai Artificial Intelligence Laboratory. 

# **Impact Statement** 

This paper presents a policy framework for cross-humanoid whole-body control that enables a single generalist policy to transfer zero-shot across diverse humanoid platforms. Our goal is to improve the scalability of future methods and facilitate rapid transfer and iteration across new embodiments. Notably, the proposed physics-consistent randomization requires embodiment-specific parameter ranges, since different humanoids exhibit distinct physical properties and therefore demand different randomization settings. 

# **References** 

- Ai, B., Dai, L., Bohlinger, N., Li, D., Mu, T., Wu, Z., Fay, K., Christensen, H. I., Peters, J., and Su, H. Towards embodiment scaling laws in robot locomotion. In _Proceedings of The 9th Conference on Robot Learning_ . PMLR, 2025. 

- Bohlinger, N., Czechmanowski, G., Krupka, M., Kicki, P., Walas, K., Peters, J., and Tateo, D. One policy to run them all: an end-to-end learning approach to multiembodiment locomotion. In _Proceedings of The 8th Conference on Robot Learning_ . PMLR, 2024. 

- Caron, S., De Mont-Marin, Y., Budhiraja, R., Bang, S. H., Domrachev, I., Nedelchev, S., Du, P., Escande, A., Vaillant, J., and Wingo, B. Pink: Python inverse kinematics 

9 

**Scalable and General Whole-Body Control for Cross-Humanoid Locomotion** 

- based on Pinocchio, 2025. URL https://github. com/stephane-caron/pink. 

- Carpentier, J., Saurel, G., Buondonno, G., Mirabel, J., Lamiraux, F., Stasse, O., and Mansard, N. The pinocchio c++ library – a fast and flexible implementation of rigid body dynamics algorithms and their analytical derivatives. In _IEEE International Symposium on System Integrations (SII)_ , 2019. 

- Chen, J., Li, X., and Cao, J. Rhino: Learning real-time humanoid-human-object interaction from human demonstrations. _arXiv preprint arXiv:2502.13134_ , 2025a. 

- Chen, Z., Ji, M., Cheng, X., Peng, X., Peng, X. B., and Wang, X. Gmt: General motion tracking for humanoid whole-body control. _arXiv preprint arXiv:2506.14770_ , 2025b. 

- Cheng, X., Ji, Y., Chen, J., Yang, R., Yang, G., and Wang, X. Expressive whole-body control for humanoid robots. In _Proceedings of Robotics: Science and Systems_ , 2024a. 

- Cheng, X., Li, J., Yang, S., Yang, G., and Wang, X. Opentelevision: Teleoperation with immersive active visual feedback. In _Proceedings of The 8th Conference on Robot Learning_ . PMLR, 2024b. 

- Developers, U. R. Xr teleoperate. https://github. com/unitreerobotics/xr_teleoperate, 2026. Accessed: January 26, 2026. 

- Doshi, R., Walke, H., Mees, O., Dasari, S., and Levine, S. Scaling cross-embodied learning: One policy for manipulation, navigation, locomotion and aviation. In _Proceedings of The 8th Conference on Robot Learning_ . PMLR, 2024. 

- Feng, G., Zhang, H., Li, Z., Peng, X. B., Basireddy, B., Yue, L., Song, Z., Yang, L., Liu, Y., Sreenath, K., et al. Genloco: Generalized locomotion controllers for quadrupedal robots. In _Proceedings of The 7th Conference on Robot Learning_ . PMLR, 2023. 

- Gupta, A., Fan, L., Ganguli, S., and Fei-Fei, L. Metamorph: Learning universal controllers with transformers. In _International Conference on Learning Representations_ , 2022. 

- He, T., Luo, Z., He, X., Xiao, W., Zhang, C., Zhang, W., Kitani, K., Liu, C., and Shi, G. Omnih2o: Universal and dexterous human-to-humanoid whole-body teleoperation and learning. In _Proceedings of The 8th Conference on Robot Learning_ . PMLR, 2024. 

- He, T., Gao, J., Xiao, W., Zhang, Y., Wang, Z., and Wang, J. Asap: Aligning simulation and real-world physics for learning agile humanoid whole-body skills. In _Proceedings of Robotics: Science and Systems_ , 2025. 

- Huang, T., Wang, H., Ren, J., and Yin, K. Towards adaptable humanoid control via adaptive motion tracking. _arXiv preprint arXiv:2510.14454_ , 2025. 

- Huang, W., Mordatch, I., and Pathak, D. One policy to control them all: Shared modular policies for agent-agnostic control. In _International Conference on Learning Representations_ , 2020. 

- Hwangbo, J., Lee, J., Dosovitskiy, A., Bellicoso, D., Tsounis, V., Koltun, V., and Hutter, M. Learning agile and dynamic motor skills for legged robots. _Science Robotics_ , 4(26):eaau5872, 2019. 

- Ji, G., Mun, J., Kim, H., and Hwangbo, J. Concurrent training of a control policy and a state estimator for dynamic and robust legged locomotion. _IEEE Robotics and Automation Letters_ , 7(2):4630–4637, 2022. 

- Kipf, T. N. and Welling, M. Semi-supervised classification with graph convolutional networks. In _International Conference on Learning Representations_ , 2017. 

- Li, J., Cheng, X., Huang, T., Yang, S., Qiu, R., and Wang, X. Amo: Adaptive motion optimization for hyperdexterous humanoid whole-body control. In _Proceedings of Robotics: Science and Systems_ , 2025. 

- Liao, Q., Truong, T. E., Huang, X., Gao, Y., Tevet, G., Sreenath, K., and Liu, C. K. Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion. _arXiv preprint arXiv:2508.08241_ , 2025. 

- Lin, Y., Liu, M., Xue, Y., Zhou, M., Yu, Y., Pang, J., and Zhang, W. H-zero: Cross-humanoid locomotion pretraining enables few-shot novel embodiment transfer. _arXiv preprint arXiv:2512.00971_ , 2025. 

- Lin, Y., Xu, L., Yu, Y., Pang, J., and Zhang, W. Unicon: A unified system for efficient robot learning transfers, 2026. URL https://arxiv.org/abs/2601.14617. 

- Liu, M., Pathak, D., and Agarwal, A. Locoformer: Generalist locomotion via long-context adaptation. In _Proceedings of The 9th Conference on Robot Learning_ . PMLR, 2025a. 

- Liu, X., Wu, J., Xue, Y., Qi, C., Xin, G., and Gao, F. Skill latent space based multigait learning for a legged robot. _IEEE Transactions on Industrial Electronics_ , 72(2):1743– 1752, 2025b. 

- Luo, Z., Dong, Y., Li, X., Huang, R., Shu, Z., Xiao, E., and Lu, P. Moral: Learning morphologically adaptive locomotion controller for quadrupedal robots on challenging terrains. _IEEE Robotics and Automation Letters_ , 9(5): 4019–4026, 2024. 

10 

**Scalable and General Whole-Body Control for Cross-Humanoid Locomotion** 

- Luo, Z., Yuan, Y., Wang, T., Li, C., Chen, S., Castaneda, F., Cao, Z.-A., Li, J., Minor, D., Ben, Q., et al. Sonic: Supersizing motion tracking for natural humanoid wholebody control. _arXiv preprint arXiv:2511.07820_ , 2025. 

- Makoviychuk, V., Wawrzyniak, L., Guo, Y., Lu, M., Storey, K., Macklin, M., Hoeller, D., Rudin, N., Allshire, A., Handa, A., and State, G. Isaac gym: High performance gpu-based physics simulation for robot learning. In _Advances in Neural Information Processing Systems, Datasets and Benchmarks Track_ , 2021. 

- Miki, T., Lee, J., Hwangbo, J., Wellhausen, L., Koltun, V., and Hutter, M. Learning robust perceptive locomotion for quadrupedal robots in the wild. _Science Robotics_ , 7 (62):eabk2822, 2022. doi: 10.1126/scirobotics.abk2822. 

- Pan, Y., Qiao, R., Chen, L., Chitta, K., Pan, L., Mai, H., Bu, Q., Zhao, H., Zheng, C., Luo, P., et al. Agility meets stability: Versatile humanoid control with heterogeneous data. _arXiv preprint arXiv:2511.17373_ , 2025. 

- Peng, Q., Lin, Y., Xue, Y., Pang, J., and Zhang, W. Embodiment-aware generalist specialist distillation for unified humanoid whole-body control. _arXiv preprint arXiv:2602.02960_ , 2026. 

- Peng, X. B., Andrychowicz, M., Zaremba, W., and Abbeel, P. Sim-to-real transfer of robotic control with dynamics randomization. In _2018 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 1–8, May 2018. 

- Rucker, Caleb, and Wensing, P. M. Smooth parameterization of rigid-body inertia. _IEEE Robotics and Automation Letters_ , 7(2):2771–2778, 2022. 

- Sferrazza, C., Huang, D.-M., Liu, F., Lee, J., and Abbeel, P. Body transformer: Leveraging robot embodiment for policy learning. In _Proceedings of The 8th Conference on Robot Learning_ . PMLR, 2024. 

- Shafiee, M., Bellegarda, G., and Ijspeert, A. Manyquadrupeds: Learning a single locomotion policy for diverse quadruped robots. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 3471–3477, 2024. 

- Su, Z., Zhang, B., Rahmanian, N., Gao, Y., Liao, Q., Regan, C., Sreenath, K., and Sastry, S. S. Hitter: A humanoid table tennis robot via hierarchical planning and learning. _arXiv preprint arXiv:2508.21043_ , 2025. 

- Sun, W., Feng, L., Cao, B., Liu, Y., Jin, Y., and Xie, Z. Ulc: A unified and fine-grained controller for humanoid locomanipulation. _arXiv preprint arXiv:2507.06905_ , 2025. 

- Trabucco, B., Phielipp, M., and Berseth, G. Anymorph: Learning transferable polices by inferring agent morphology. In _International conference on Machine learning_ , pp. 21677–21691. PMLR, 2022. 

- Traversaro, S., Brossette, S., Escande, A., and Nori, F. Identification of fully physical consistent inertial parameters using optimization on manifolds. In _2016 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pp. 5446–5451, 2016. 

- Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., and Polosukhin, I. Attention is all you need. _Advances in neural information processing systems_ , 30, 2017. 

- Wang, D., Wang, X., Liu, X., Shi, J., Zhao, Y., Bai, C., and Li, X. More: Mixture of residual experts for humanoid lifelike gaits learning on complex terrains. _arXiv preprint arXiv:2506.08840_ , 2025a. 

- Wang, H., Zhang, W., Yu, R., and Huang, T. Physhsi: Towards a real-world generalizable and natural humanoid-scene interaction system. _arXiv preprint arXiv:2510.11072_ , 2025b. 

- Weng, H., Li, Y., Sobanbabu, N., Wang, Z., Luo, Z., He, T., Ramanan, D., and Shi, G. Hdmi: Learning interactive humanoid whole-body control from human videos. _arXiv preprint arXiv:2509.16757_ , 2025. 

- Wensing, P. M., Kim, S., and Slotine, J.-J. E. Linear matrix inequalities for physically consistent inertial parameter identification: A statistical perspective on the mass distribution. _IEEE Robotics and Automation Letters_ , 3(1): 60–67, 2018. 

- Wu, J., Xin, G., Qi, C., and Xue, Y. Learning robust and agile legged locomotion using adversarial motion priors. _IEEE Robotics and Automation Letters_ , 8(8):4975–4982, 2023. 

- Xie, W., Han, J., Zheng, J., Li, H., Liu, X., Shi, J., Zhang, W., Bai, C., and Li, X. Kungfubot: Physics-based humanoid whole-body control for learning highly-dynamic skills. _Advances in Neural Information Processing Systems_ , 2025. 

- Xue, Y., Dong, W., Liu, M., Zhang, W., and Pang, J. Hugwbc: A unified and general humanoid whole-body controller for versatile locomotion. In _Proceedings of Robotics: Science and Systems_ , 2025. 

- Yang, L., Huang, X., Wu, Z., Kanazawa, A., Abbeel, P., Sferrazza, C., Liu, C. K., Duan, R., and Shi, G. Omniretarget: Interaction-preserving data generation for humanoid whole-body loco-manipulation and scene interaction. _arXiv preprint arXiv:2509.26633_ , 2025a. 

11 

**Scalable and General Whole-Body Control for Cross-Humanoid Locomotion** 

- Yang, S., Fu, Z., Cao, Z., Guo, J., Wensing, P., Zhang, W., and Chen, H. Multi-loco: Unifying multi-embodiment legged locomotion via reinforcement learning augmented diffusion. In _Proceedings of The 9th Conference on Robot Learning_ . PMLR, 2025b. 

- Yin, K., Zeng, W., Fan, K., and Dai, M. Unitracker: Learning universal whole-body motion tracker for humanoid robots. _arXiv preprint arXiv:2507.07356_ , 2025. 

- Yu, C., Zhang, W., Lai, H., Tian, Z., Kneip, L., and Wang, J. Multi-embodiment legged robot control as a sequence modeling problem. In _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 7250–7257. IEEE, 2023. 

- Ze, Y., Zhao, S., Wang, W., Kanazawa, A., Duan, R., Abbeel, P., Shi, G., Wu, J., and Liu, C. K. Twist2: Scalable, portable, and holistic humanoid data collection system. _arXiv preprint arXiv:2511.02832_ , 2025. 

- Zeng, W., Lu, S., Yin, K., Niu, X., Dai, M., Wang, J., and Pang, J. Behavior foundation model for humanoid robots. _arXiv preprint arXiv:2509.13780_ , 2025. 

- Zhang, Z., Guo, J., Chen, C., Wang, J., Lin, C., Lian, Y., Xue, H., Wang, Z., Liu, M., Lyu, J., et al. Track any motions under any disturbances. _arXiv preprint arXiv:2509.13833_ , 2025. 

- Zhang, Z., Chen, C., Xue, H., Wang, J., Liang, S., Liu, Y., Zhang, Z., Wang, H., and Yi, L. Unleashing humanoid reaching potential via real-world-ready skill space. _IEEE Robotics and Automation Letters_ , 11(2): 2082–2089, 2026. 

- Zhuang, Z. and Zhao, H. Embrace collisions: Humanoid shadowing for deployable contact-agnostics motions. _arXiv preprint arXiv:2502.01465_ , 2025. 

12 

**Scalable and General Whole-Body Control for Cross-Humanoid Locomotion** 

# **A. Implementation Details** 

## **A.1. Proof Skeleton of Proposition 3.5** 

The parallel-axis theorem establishes a bijective mapping between the rotational inertia w.r.t body frame origin<sup>**¯**</sup> **I** and **¯I** C 


To obtain inertial parameters **_κ_** link that corresponds to a physically plausible system (Traversaro et al., 2016; Wensing et al., 2018), we should have constraints: 


where _m >_ 0, _D_ 1, _D_ 2 and _D_ 3 are principal moments of inertia, such that<sup>**¯**</sup> **I** C = **RDR**<sup>_⊤_</sup> with **D** = diag( _D_ 1 _, D_ 2 _, D_ 3) and **R** _∈_ **SO** (3). Note that the triangle-inequality component of the constraint can be reformulated as: 


where Tr( _·_ ) is the trace operator, _λ_ max( _·_ ) extracts the maximum eigenvalue. Since<sup>**¯**</sup> **I** C is a symmetric matrix, it must satisfy _λ_ max(<sup>**¯**</sup> **I** C) **I** _⪰_<sup>**¯**</sup> **I** C, then Ineq. (17) are equivalent to: 


According to the parallel-axis theorem of pseudoinertia (Wensing et al., 2018): 


according to Schur complement, we can further consolidate the inertial constraints (19) into a linear matrix inequality: 


where **J** _∈_ R<sup>4</sup><sup>_×_4</sup> is pseudo-inertia matrix of rigid body (Rucker et al., 2022), originally defined as the integral form: 


Therefore, obtaining a physically feasible set of inertial parameters only requires ensuring that the corresponding **J** is positive definite. A unique factorization by the Cholesky decomposition claims that a real symmetric matrix **J** is positive definite _iff_ there exists a unique real nonsingular matrix **L** such that 


where **L** is upper-triangular with a positive diagonal. Now we can physics-consistently randomize the link parameters, by perturbing the upper-triangular entries of **L** : 


where _D_ is the noise distribution. To achieve an interpretable randomization and provide geometric insight into the resulting link, instead of choosing a random distribution _D_ , we model the perturbations as an affine transformation on the rigid bodies’ geometry and scaling of the mass density: 


where **U** = _β_ **E** , **E** denotes the linear component of the affine transformation. Equation (23) can be rewritten as: 


from which it follows that **U** = **L** _′_ **L** _−_ **1** is a unique upper triangular matrix with positive diagonal entries, since both **L** and **L** _′_ are upper-triangular. Thus, **U** can be parameterized using exponential mapping on the diagonal entries: 


we finally obtain a bijective mapping from original inertia to 10-dimensional interpretable vector 

_θ_ inert = [ _α, d_ 1 _, d_ 2 _, d_ 3 _, s_ 12 _, s_ 23 _, s_ 13 _, t_ 1 _, t_ 2 _, t_ 3]<sup>_⊤_</sup> _∈_ R<sup>10</sup> _._ 

As a result, the random perturbation **_ϵ_** applied at the Cholesky-factor level can be equivalently expressed as a perturbation in _θ_ inert. The detailed ranges for _θ_ inert can be found in Table 3. 

## **A.2. Physical Interpretation of Morphological Randomization** 

Based on the interpretation of **U** as a combination of an affine transformation and a density scaling of reference rigid body, each parameter admits a clear physical meaning. 

The parameters _d_ 1 _, d_ 2 and _d_ 3 correspond to stretching or compression of the reference rigid body along _x, y_ and _z_ axes, respectively, where _di >_ 0 _⇒ e_<sup>_di_</sup> _>_ 1 implies the stretching, and _di <_ 0 _⇒ e_<sup>_di_</sup> _<_ 1 denotes the compression. Importantly, this exponential formulation guarantees that the body never degenerates to zero thickness. 

13 

**Scalable and General Whole-Body Control for Cross-Humanoid Locomotion** 

The shear parameters _s_ 12 _, s_ 13 and _s_ 23 induce shear deformations in the _xy, xz_ and _yz_ planes, respectively, without altering the volume of the object. The translation parameters _t_ 1 _, t_ 2 and _t_ 3 uniformly shift the center of mass of the reference rigid body along the _x, y_ and _z_ directions. Finally, the scalar parameter _α_ controls a global scaling of the mass density _ρ_ by the factor _e_<sup>2</sup><sup>_α_</sup> . 

In this work, we used the Unitree G1 (29 DoF) as the template and added three additional head joints. The corresponding link and joint randomization ranges are listed in Tables. 3 and 4. All noise is sampled from a uniform distribution except for the rotation axis and actuation type. Table 3 defines the randomization ranges for the side lengths of the nominal link bounding box, denoted as _lx_<sup>ref</sup><sup>_, l_</sup> _y_<sup>ref</sup><sup>_, l_</sup> _z_<sup>ref, expressed</sup> in the body frame. In the Tab. 4, we denote revolute joint actuation as **R** and fixed joint actuation as **F** . The rotation axes [ _ax, ay, az_ ] of the three hip joints are randomly permuted rather than independently sampled. The orientation offsets [ _ϕ, θ, ψ_ ] are randomly generated with the constraint that their sum across the joint group is zero, ensuring no net orientation bias. 

## **A.3. Policy Training** 

To achieve cross-embodiment learning, we employ either GCN or Transformer as representation-learning backbone. Joint-related observations in the policy input _o_<sup>_π_</sup> _t_<sup>, including</sup> joint position _qt_ , joint velocities _q_ ˙ _t_ , actions _at_ and _I_ ( _t_ ), are first mapped to canonical joint representation **q** global via mapping function defined in Equation 10. 

The resulting canonical representation is linearly projected, after which each joint node is processed by a node-specific learnable linear layer. This yields a sequence of _N_ max canonical node embeddings. The remaining policy observations are concatenated into vectors _o_<sup>_g_</sup> _t_<sup>, which is later used in de-</sup> coding stage to generate joint-level actions. 

Formally, the canonical node embedding **X** shared by both encoders. For the Transformer encoder, positional embeddings are added, while the GCN encoder operates directly on **X** . 


where the _ϕθ_ ( _·_ ) is learnable embedding function parameters by weights **W** _θ ∈_ R<sup>_N×D_</sup> . 

**Encoder.** We then apply a stack of GCN or transformer blocks as the encoder to selectively incorporate information beyond purely local kinematic neighborhood. For the GCN encoder, the input consists of the node embeddings **X** (without positional embedding) together with the structural mask **M** = **I** + **A** (with self-loops): 

_Table 3._ **Link space parameterization randomization ranges.** 

||_Shoulder_|_Torso_|_Pelvis_|_Hip_|_Knee_|_Foot_|
|---|---|---|---|---|---|---|
|_e_<sup>_α_</sup>|[0.8, 1.4]|[0.8, 1.5]|[0.8, 1.5]|[0.8, 1.5]|[0.8, 1.5]|[0.8, 1.4]|
|_e_<sup>_d_1</sup>|[0.8, 1.2]|[0.8, 1.5]|[0.8, 1.4]|[0.8, 1.2]|[0.8, 1.2]|[0.5, 1.5]|
|_e_<sup>_d_2</sup>|[0.8, 1.2]|[0.8, 1.4]|[0.8, 1.4]|[0.8, 1.2]|[0.8, 1.2]|[0.5, 1.2]|
|_e_<sup>_d_3</sup>|[0.8, 1.2]|[0.8, 1.2]|[0.8, 1.2]|[0.5, 1.5]|[0.5, 1.5]|[0.8, 1.2]|
|_s_12|[-0.1, 0.1]|[-0.1, 0.1]|[-0.1, 0.1]|[-0.1, 0.1]|[-0.1, 0.1]|[-0.1, 0.1]|
|_s_23|[-0.1, 0.1]|[-0.1, 0.1]|[-0.1, 0.1]|[-0.1, 0.1]|[-0.1, 0.1]|[-0.1, 0.1]|
|_s_13|[-0.1, 0.1]|[-0.1, 0.1]|[-0.1, 0.1]|[-0.1, 0.1]|[-0.1, 0.1]|[-0.1, 0.1]|
|_t_1|[_−_0_._2_,_0_._2]_× l_<sup>ref</sup><br>_x_|[_−_0_._2_,_0_._2]_× l_<sup>ref</sup><br>_x_|[_−_0_._2_,_0_._2]_× l_<sup>ref</sup><br>_x_|[_−_0_._2_,_0_._2]_× l_<sup>ref</sup><br>_x_|[_−_0_._2_,_0_._2]_× l_<sup>ref</sup><br>_x_|[_−_0_._2_,_0_._2]_× l_<sup>ref</sup><br>_x_|
|_t_2|[_−_0_._2_,_0_._2]_× l_<sup>ref</sup><br>_y_|[_−_0_._2_,_0_._2]_× l_<sup>ref</sup><br>_y_|[_−_0_._2_,_0_._2]_× l_<sup>ref</sup><br>_y_|[_−_0_._2_,_0_._2]_× l_<sup>ref</sup><br>_y_|[_−_0_._2_,_0_._2]_× l_<sup>ref</sup><br>_y_|[_−_0_._2_,_0_._2]_× l_<sup>ref</sup><br>_y_|
|_t_3|[_−_0_._3_,_0_._3]_× l_<sup>ref</sup><br>_z_|[_−_0_._3_,_0_._3]_× l_<sup>ref</sup><br>_z_|[_−_0_._3_,_0_._3]_× l_<sup>ref</sup><br>_z_|[_−_0_._3_,_0_._3]_× l_<sup>ref</sup><br>_z_|[_−_0_._3_,_0_._3]_× l_<sup>ref</sup><br>_z_|[_−_0_._2_,_0_._2]_× l_<sup>ref</sup><br>_z_|


_Table 4._ **Joint space parameterization randomization ranges.** 

||_Shoulder_|_Waist_|_Hip_|_Knee_|_Ankle_|
|---|---|---|---|---|---|
|[_px, py, pz_]|[0.8, 1.2]|[0.8, 1.2]|[0.8, 1.2]|[0.8, 1.2]|[0.8, 1.2]|
|[_ϕ, θ, ψ_]<br>[_q_min_, q_max_,_ ˙_q_max]|-<br>[0.8, 1.0]|-<br>[0.8, 1.0]|[-0.3,0.3] (rads)<br>�_δ_(_ϕ, θ, ψ_) = 0<br>[0.8, 1.0]|-<br>[0.8, 1.3]|-<br>[0.8, 1.0]|
|[_ax, ay, az_]|-|-|_Permuted_|-|-|
|_τ_max|[0.7, 1.0]|[0.7, 1.0]|[0.7, 1.0]|[0.7, 1.0]|[0.7, 1.0]|
|Actuation|R/F|R/F|R|R|R|


For the Transformer-based encoder, we adopt two types of attention blocks: self-attention blocks (SAB) and maskedattention block (MAB), defined respectively as: 


The hybrid-masking design is similar to prior work (Sferrazza et al., 2024), in which the first encoder layer employs a MAB to respect embodiment-specific structural constraints, while all subsequent layers use SABs to enable global information exchange. Formally, the Transformer encoder is defined as: 


**Action Decoder.** The encoded node features **Z** produced by either GCN or Transformer encoder are concatenated with the global context vector _o_<sup>_g_</sup> _t_<sup>and the reconstructed privileged</sup> information **P** obtained from the learned state-estimation module. 


where **Estimator** is state estimator trained by supervised learning (Ji et al., 2022; Liu et al., 2025b). Joint-level actions are then decoded independently for each node: 


14 

**Scalable and General Whole-Body Control for Cross-Humanoid Locomotion** 

_Table 5._ **Robot models used in our experiments** 

|_Robot type_|_Evaluation_||_DoFs_||_Mass_(kg)|_Height_(m)|
|---|---|---|---|---|---|---|
|||_Arm_|_Waist_|_Leg_|||
|_Booster K1_|_Sim_|4|0|5|18|0.95|
|_Booster T1_|_Sim / Real_|4|1|6|31|1.2|
|_Fourier N1_|_Sim / Real_|5|1|6|39|1.3|
|_Unitree G1 (23 DoF)_|_Sim / Real_|5|1|6|33|1.4|
|_Unitree G1 (29 DoF)_|_Sim / Real_|7|3|6|33|1.4|
|_Agibot X2_|_Sim / Real_|7|3|6|40|1.3|
|_EngineAI PM01_|_Sim_|5|1|6|40|1.4|
|_MagicLab Gen1_|_Sim_|7|2|6|66|1.7|
|_TianGong-1_|_Sim_|4|0|6|42|1.7|
|_TianGong-2_|_Sim_|4|0|6|61|1.7|
|_Dobot Atom_|_Sim / Real_|7|1|6|60|1.7|
|_Unitree H1-2_|_Sim / Real_|7|1|6|66|1.8|
|_LeJu Kuavo_|_Sim_|7|0|6|52|1.7|


exceed 80<sup>_◦_</sup> . 

**Average commands tracking error** _E_ cmd measures the average episodic tracking accuracy for a single command across 1000 environments. The metric is defined as the _L_ 1 distance between the actual robot states and the command states. All commands are uniformly sampled within a predefined range. 

Figure 8 presents a visualization of simulation evaluation. 

Figure 9 shows the embodiment data generated by physicsconsistent morphological randomization. 

## **B.2. Deployment Details** 

_Table 6._ **Reward definitions used in XHugWBC.** 

|Term|Definition|Weight|
|---|---|---|
||Task Reward<br><br>taret<br>2 <br>||
|Linear Velocity Tracking|exp<br>�<br>_−_<br>��_v_g<br>xy<br>_−v_xy<br>��_/_0_._2<br>�<br><br><br>|2.5|
|Angular Velocity Tracking|exp<br>�<br>_−_<br>��_ω_target<br>z<br>_−ω_z<br>��2_/_0_._2<br>�|2.0|
||Behavior Reward<br><sup>2</sup>||
|Body Height Tracking|_∥h_<sup>target</sup> _−h∥_<br>|-20|
|Torso Pitch Tracking<br>Waist Yaw Tracking|_∥p_<sup>target</sup> _−p∥_<sup>2</sup><br>��_θy_<br>target <sup>_−θy_��2</sup><br>|-10<br>-1|
|Waist Roll Tracking|��_θr_<br>target <sup>_−θr_��2</sup><br>|-1|
|Waist Pitch Tracking<br>Contact-Swing Tracking|��_θp_<br>target <sup>_−θp_��2</sup><br>_−_<sup>�</sup><br>_i_<sup>[1</sup><sup>_−C_(</sup><sup>_ϕi_)]</sup><br>�<br>1_−_exp(<br>��_f_foot_,i_��2_/_50)<br>�<br>_−C_(_ϕi_)<br>�<br>1_−_exp<br>�<br>_∥v_<sup>foot</sup><sup>_,i_</sup><br>_xy_<br>_∥_<sup>2</sup>_/_5<br>��|-2<br>-2|
||Regularization Reward||
|R-P Angular Velocity|_∥ω_xy_∥_<sup>2</sup><br>|-0.5|
|Vertical Body Movement|_∥v_z_∥_<sup>2</sup><br><br>|-0.1|
|Feet Slip|1_−_<sup>�</sup><br>_i_ <sup>exp</sup><br>�<br>_−_<br>��_v_foot,i<br>xy<br>��2<sup>�</sup><br>|-0.2|
|Action Rate|_∥at −at−_1_∥_<sup>2</sup><br>|-0.01|
|Action Smoothness|_∥at−_2_−_2_at−_1+_at∥_<sup>2</sup><br>|-0.01|
|Joint Torque|_∥τ/kp∥_<sup>2</sup><br>|-5e-6|
|Joint Acceleration|_∥_¨_q∥_<sup>2</sup><br>|-2.5e-7|
|Upper Joint Deviation|��_q_upper_−q_nominal<br>upper<br>��2<br>|-0.5|
|Head Joint Deviation|��_q_head_−q_nominal<br>head<br>��2<br><br><br>2|-0.5|
|Hip Joint Deviation|���_q_hip_,_xz_−q_nominal<br>hip_,_xz<br>���<br>|-1|
|Zero Actions|I(t)_∥a∥_<sup>2</sup>|-0.05|
|Termination|1[Early Terminate]|-40|


We employ a modular and reusable deployment framework to simplify our sim-to-sim and sim-to-real experiment workflows across diverse embodiments (Lin et al., 2026). During multi-robot experiments, locomotion and manipulation commands are issued from one centralized workstation and synchronized with all robot participants over ZMQ-based communication channels, while each robot executes an identical locomotion policy on its own on-board computing device. In addition, we combine the framework with existing IK solvers (Carpentier et al., 2019; Caron et al., 2025) and teleoperation pipelines (Cheng et al., 2024b; Developers, 2026) to enable whole-body, hardware-agnostic locomanipulation. 

## **A.4. Reward Details** 

The total rewards consist of three terms, including task rewards, behavior rewards and regularization rewards. Table 6 lists reward terms for XHugWBC. The Contact-Swing Tracking reward is adopted from (Xue et al., 2025). 

# **B. Extended Experiment** 

## **B.1. Metrics** 

We evaluate ablation methods in Isaac Gym (Makoviychuk et al., 2021), and the policy performance is measured by two distinct metrics: 

**Survival Rate** _E_ surv measures the trajectory survival rate over 1000 environments per episode. Non-termination is defined as the roll and pitch angle of the robot torso do not 

15 

**Scalable and General Whole-Body Control for Cross-Humanoid Locomotion** 


_Figure 8._ **Evaluation of 12 humanoid robots in simulation,** including Booster K1, Booster T1, Fourier N1, Unitree G1, Agibot X2, EngineAI PM01, MagicLab Gen1, TianGong-1, TianGong-2, Dobot Atom, Unitree H1-2, and LeJu Kuavo. The first six rows report per-robot evaluations, while the final rows show parallel evaluations across all robots. 

16 

**Scalable and General Whole-Body Control for Cross-Humanoid Locomotion** 


_Figure 9._ **Visualization of samples from procedurally generated embodiment data.** 

17 

**Scalable and General Whole-Body Control for Cross-Humanoid Locomotion** 

_Table 7._ **Command tracking errors and survival rates.** Zero-shot performance of XHugWBC, the specialist controller (HugWBC (Xue et al., 2025)) and generalist fine-tuned (Generalist-FT) controller on each of the twelve unseen robots, measured in terms of command tracking errors and survival rates. The symbol ”-” indicates that the corresponding robot does not have controllable joints in the specified command space. 

||_Survival_||_Task Command_|_s_||_Be_|_havior Comma_|_nds_||
|---|---|---|---|---|---|---|---|---|---|
||_E_surv|_E_vx(m_/_s)|_E_vy(m_/_s)|_Eω_(rad_/_s)|_E_h(m)|_E_p(_rad_)|_Eθ_y(rad)|_Eθ_p(rad)|_Eθ_r(rad)|
|**_Generalist (XHug_**|**_WBC)_**|||||||||
|_Booster K1_|100|0.125 (_±_0_._062)|0.203 (_±_0_._021)|0.159 (_±_0_._028)|0.046 (_±_0_._025)|0.134 (_±_0_._056)|-|-|-|
|_Booster T1_|100|0.094 (_±_0_._034)|0.142 (_±_0_._027)|0.281 (_±_0_._013)|0.075 (_±_0_._043)|0.090 (_±_0_._021)|0.039 (_±_0_._025)|-|-|
|_Fourier N1_|100|0.090 (_±_0_._040)|0.119 (_±_0_._031)|0.177 (_±_0_._011)|0.015 (_±_0_._006)|0.112 (_±_0_._034)|0.044 (_±_0_._026)|-|-|
|_Unitree G1_|100|0.047 (_±_0_._069)|0.079 (_±_0_._023)|0.145 (_±_0_._021)|0.067 (_±_0_._036)|0.094 (_±_0_._036)|0.041 (_±_0_._034)|0.042 (_±_0_._030)|0.038 (_±_0_._006)|
|_Agibot X2_|100|0.052 (_±_0_._016)|0.097 (_±_0_._026)|0.168 (_±_0_._014)|0.037 (_±_0_._018)|0.106 (_±_0_._032)|0.041 (_±_0_._035)|0.062 (_±_0_._024)|0.065 (_±_0_._016)|
|_EngineAI PM01_|100|0.075 (_±_0_._029)|0.107 (_±_0_._022)|0.150 (_±_0_._013)|0.039 (_±_0_._026)|0.142 (_±_0_._043)|0.044 (_±_0_._027)|-|-|
|_MagicLab Gen1_|100|0.106 (_±_0_._031)|0.086 (_±_0_._022)|0.151 (_±_0_._030)|0.031 (_±_0_._016)|0.076 (_±_0_._052)|0.054 (_±_0_._038)|-|0.044 (_±_0_._002)|
|_TianGong-1_|100|0.121 (_±_0_._107)|0.109 (_±_0_._026)|0.208 (_±_0_._046)|0.014 (_±_0_._028)|0.081 (_±_0_._099)|-|-|-|
|_TianGong-2_|100|0.094 (_±_0_._033)|0.155 (_±_0_._016)|0.146 (_±_0_._011)|0.038 (_±_0_._015)|0.119 (_±_0_._023)|-|-|-|
|_Dobot Atom_|100|0.063 (_±_0_._028)|0.111 (_±_0_._023)|0.147 (_±_0_._016)|0.026 (_±_0_._016)|0.060 (_±_0_._014)|0.037 (_±_0_._011)|-|-|
|_Unitree H1-2_|100|0.065 (_±_0_._031)|0.102 (_±_0_._009)|0.099 (_±_0_._030)|0.014 (_±_0_._007)|0.086 (_±_0_._038)|0.044 (_±_0_._031)|-|-|
|_LeJu Kuavo_|100|0.075 (_±_0_._025)|0.082 (_±_0_._026)|0.098 (_±_0_._024)|0.126 (_±_0_._040)|0.072 (_±_0_._027)|-|-|-|
|**_Specialist (HugW_**|**_BC)_**|||||||||
|_Booster K1_|100|0.088 (_±_0_._078)|0.125 (_±_0_._090)|0.214 (_±_0_._121)|0.065 (_±_0_._036)|0.142 (_±_0_._108)|-|-|-|
|_Booster T1_|100|0.029 (_±_0_._011)|0.091 (_±_0_._017)|0.191 (_±_0_._012)|0.057 (_±_0_._002)|0.101 (_±_0_._055)|0.059 (_±_0_._035)|-|-|
|_Fourier N1_|100|**0.057 (**_±_0_._050**)**|0.076 (_±_0_._046)|0.140 (_±_0_._101)|0.052 (_±_0_._039)|0.173 (_±_0_._098)|0.057 (_±_0_._032)|-|-|
|_Unitree G1_|100|0.054 (_±_0_._049)|0.061 (_±_0_._036)|0.110 (_±_0_._076)|0.054 (_±_0_._035)|0.121 (_±_0_._070)|0.050 (_±_0_._030)|0.045 (_±_0_._026)|**0.036 (**_±_0_._023**)**|
|_Agibot X2_|100|0.052 (_±_0_._016)|0.042 (_±_0_._014)|0.101 (_±_0_._012)|**0.007 (**_±_0_._001**)**|**0.074 (**_±_0_._035**)**|0.043 (_±_0_._028)|0.030 (_±_0_._027)|**0.011 (**_±_0_._005**)**|
|_EngineAI PM01_|100|**0.030 (**_±_0_._014**)**|0.074 (_±_0_._009)|0.109 (_±_0_._023)|0.061 (_±_0_._001)|0.096 (_±_0_._054)|0.072 (_±_0_._044)|-|-|
|_MagicLab Gen1_|100|0.090 (_±_0_._054)|0.080 (_±_0_._048)|0.130 (_±_0_._087)|**0.029 (**_±_0_._021**)**|0.179 (_±_0_._121)|0.059 (_±_0_._030)|0.097 (_±_0_._046)|0.097 (_±_0_._046)|
|_TianGong-1_|100|0.076 (_±_0_._062)|0.072 (_±_0_._042)|**0.063 (**_±_0_._043**)**|0.043 (_±_0_._030)|0.231 (_±_0_._163)|-|-|-|
|_TianGong-2_|100|**0.067 (**_±_0_._048**)**|0.095 (_±_0_._051)|0.084 (_±_0_._056)|0.023 (_±_0_._017)|0.121 (_±_0_._084)|-|-|-|
|_Dobot Atom_|100|0.061 (_±_0_._044)|0.065 (_±_0_._038)|0.145 (_±_0_._086)|0.034 (_±_0_._022)|0.126 (_±_0_._083)|0.118 (_±_0_._107)|-|-|
|_Unitree H1-2_|100|0.042 (_±_0_._019)|0.058 (_±_0_._017)|**0.101 (**_±_0_._025**)**|0.065 (_±_0_._021)|0.096 (_±_0_._061)|0.044 (_±_0_._027)|-|-|
|_LeJu Kuavo_|100|0.084 (_±_0_._077)|0.113 (_±_0_._058)|0.070 (_±_0_._037)|**0.042 (**_±_0_._035**)**|0.206 (_±_0_._139)|-|-|-|
|**_Generalist-FT_**||||||||||
|_Booster K1_|100|**0.061 (**_±_0_._049**)**|**0.088 (**_±_0_._047**)**|**0.090 (**_±_0_._062**)**|**0.055 (**_±_0_._035**)**|**0.114 (**_±_0_._082**)**|-|-|-|
|_Booster T1_|100|**0.027 (**_±_0_._009**)**|**0.088 (**_±_0_._016**)**|**0.181 (**_±_0_._002**)**|**0.033 (**_±_0_._021**)**|**0.084 (**_±_0_._011**)**|**0.029 (**_±_0_._015**)**|-|-|
|_Fourier N1_|100|0.061 (_±_0_._049)|**0.068 (**_±_0_._039**)**|**0.135 (**_±_0_._089**)**|**0.039 (**_±_0_._029**)**|**0.096 (**_±_0_._045**)**|**0.031 (**_±_0_._019**)**|-|-|
|_Unitree G1_|100|**0.039 (**_±_0_._021**)**|**0.058 (**_±_0_._031**)**|**0.091 (**_±_0_._055**)**|**0.051 (**_±_0_._036**)**|**0.102 (**_±_0_._051**)**|**0.026 (**_±_0_._014**)**|**0.033 (**_±_0_._017**)**|0.037 (_±_0_._022)|
|_Agibot X2_|100|**0.025 (**_±_0_._006**)**|**0.042 (**_±_0_._011**)**|**0.095 (**_±_0_._027**)**|0.057 (_±_0_._031)|0.078 (_±_0_._034)|**0.018 (**_±_0_._010**)**|**0.018 (**_±_0_._007**)**|0.041 (_±_0_._017)|
|_EngineAI PM01_|100|0.043 (_±_0_._005)|**0.051 (**_±_0_._006**)**|**0.091 (**_±_0_._018**)**|**0.016 (**_±_0_._013**)**|**0.082 (**_±_0_._038**)**|**0.035 (**_±_0_._012**)**|-|-|
|_MagicLab Gen1_|100|**0.064 (**_±_0_._051**)**|**0.068 (**_±_0_._035**)**|**0.103 (**_±_0_._064**)**|0.033 (_±_0_._023)|**0.121 (**_±_0_._063**)**|**0.024 (**_±_0_._014**)**|-|**0.073 (**_±_0_._036**)**|
|_TianGong-1_|100|**0.070 (**_±_0_._057**)**|**0.056 (**_±_0_._029**)**|0.066 (_±_0_._041)|**0.041 (**_±_0_._032**)**|**0.231 (**_±_0_._151**)**|-|-|-|
|_TianGong-2_|100|0.079 (_±_0_._049)|**0.091 (**_±_0_._051**)**|**0.075 (**_±_0_._087**)**|**0.018 (**_±_0_._026**)**|**0.080 (**_±_0_._055**)**|-|-|-|
|_Dobot Atom_|100|**0.055 (**_±_0_._036**)**|**0.057 (**_±_0_._034**)**|**0.133 (**_±_0_._068**)**|**0.031 (**_±_0_._020**)**|**0.106 (**_±_0_._053**)**|**0.102 (**_±_0_._051**)**|-|-|
|_Unitree H1-2_|100|**0.021 (**_±_0_._019**)**|**0.058 (**_±_0_._014**)**|0.106 (_±_0_._031)|**0.060 (**_±_0_._025**)**|**0.072 (**_±_0_._033**)**|**0.024 (**_±_0_._011**)**|-|-|
|_LeJu Kuavo_|100|**0.061 (**_±_0_._055**)**|**0.099 (**_±_0_._051**)**|**0.058 (**_±_0_._034**)**|0.048 (_±_0_._040)|**0.158 (**_±_0_._113**)**|-|-|-|


18 

**Scalable and General Whole-Body Control for Cross-Humanoid Locomotion** 

_Table 8._ **Joint index and joint motion direction defined in the global joint space. Each joint axis direction adopts the righthand rule.** 

|_Joint Name_|_Joint Index_|_Joint Axis_|
|---|---|---|
|_Left hip roll_|0|[1, 0, 0]|
|_Left hip pitch_|1|[0, 1, 0]|
|_Left hip yaw_|2|[0, 0, 1]|
|_Left knee pitch_|3|[0, 1, 0]|
|_Left ankle roll_|4|[1, 0, 0]|
|_Left ankle pitch_|5|[0, 1, 0]|
|_Right hip roll_|6|[1, 0, 0]|
|_Right hip pitch_|7|[0, 1, 0]|
|_Right hip yaw_|8|[0, 0, 1]|
|_Right knee pitch_|9|[0, 1, 0]|
|_Right ankle roll_|10|[1, 0, 0]|
|_Right ankle pitch_|11|[0, 1, 0]|
|_Waist pitch_|12|[0, 1, 0]|
|_Waist roll_|13|[1, 0, 0]|
|_Waist yaw_|14|[0, 0, 1]|
|_Head roll_|15|[1, 0, 0]|
|_Head pitch_|16|[0, 1, 0]|
|_Head yaw_|17|[0, 0, 1]|
|_Left shoulder roll_|18|[1, 0, 0]|
|_Left shoulder pitch_|19|[0, 1, 0]|
|_Left shoulder yaw_|20|[0, 0, 1]|
|_Left elbow pitch_|21|[0, 1, 0]|
|_Left wrist roll_|22|[1, 0, 0]|
|_Left wrist pitch_|23|[0, 1, 0]|
|_Left wrist yaw_|24|[0, 0, 1]|
|_Right shoulder roll_|25|[1, 0, 0]|
|_Right shoulder pitch_|26|[0, 1, 0]|
|_Right shoulder yaw_|27|[0, 0, 1]|
|_Right elbow pitch_|28|[0, 1, 0]|
|_Right wrist roll_|29|[1, 0, 0]|
|_Right wrist pitch_|30|[0, 1, 0]|
|_Right wrist yaw_|31|[0, 0, 1]|


19 

