---
title: "SynAgent: Generalizable Cooperative Humanoid Manipulation via Solo-to-Cooperative Agent Synergy"
date: "2026-04-20"
authors: "Wei Yao; Haohan Ma; Hongwen Zhang; Liangjun Xing; Zhile Yang; Yuanjun Guo"
url: https://arxiv.org/abs/2604.18557
pdf: https://arxiv.org/pdf/2604.18557
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2604.18557)** / [論文ページ](https://arxiv.org/abs/2604.18557)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **SynAgent: Generalizable Cooperative Humanoid Manipulation via Solo-to-Cooperative Agent Synergy** 

## **Wei Yao**<sup>∗1</sup> **, Haohan Ma**<sup>∗2</sup> **, Hongwen Zhang**<sup>3</sup> **, Liangjun Xing**<sup>4</sup> **, Zhile Yang**<sup>2</sup> **, Yuanjun Guo**<sup>2</sup> **, Yunlian Sun**<sup>†1</sup> **, Yebin Liu**<sup>4</sup> 

1School of Computer Science and Engineering, Nanjing University of Science and Technology, Nanjing 210094, China 

- 2Shenzhen Institutes of Advanced Technology, Chinese Academy of Sciences, Shenzhen 518055, China 

3School of Artificial Intelligence, Beijing Normal University, Beijing 100875, China 

- 4Department of Automation, Tsinghua University, Beijing 100084, China 

{wei.yao, yunlian.sun}@njust.edu.cn, {hh.ma2, zl.yang, yj.guo}@siat.ac.cn, zhanghongwen@bnu.edu.cn, {xlj24@mails, liuyebin@mail}.tsinghua.edu.cn 


Figure 1: **Features of SynAgent.** As the first model to address trajectory-following object manipulation with multiple humanoid agents, SynAgent generalizes across diverse object geometries and supports cooperative manipulation. 

#### **Abstract** 

Controllable cooperative humanoid manipulation is a fundamental yet challenging problem for embodied intelligence, due to severe data scarcity, complexities in multi-agent coordination, and limited generalization across objects. In this paper, we present **SynAgent** , a unified framework that enables scalable and physically plausible cooperative manipulation by leveraging **Solo-to-Cooperative Agent Synergy** to transfer skills from single-agent human-object interaction to multi-agent human-object-human scenarios. To maintain semantic integrity during motion transfer, we introduce an interaction-preserving retargeting method based on an Interact Mesh constructed via Delaunay tetrahedralization, which faithfully maintains spatial relationships among humans and objects. Building upon this refined data, we propose a singleagent pretraining and adaptation paradigm that distills synergistic collaborative behaviors from abundant single-human data through decentralized training and multi-agent PPO. Finally, we develop a trajectory-conditioned generative policy 

- ∗These authors contributed equally. 

- †Corresponding author. 

using a conditional VAE, trained via multi-teacher distillation from motion imitation priors to achieve stable and controllable object-level trajectory execution. Extensive experiments demonstrate that SynAgent significantly outperforms existing baselines in both cooperative imitation and trajectoryconditioned control, while generalizing across diverse object geometries. Codes and data will be available after publication. Project Page: https://yw0208.github.io/synagent/. 

## **Introduction** 

Embodied intelligence has emerged as a key research frontier due to its substantial potentiality. Most existing work focuses on single-robot locomotion (Luo et al. 2023a,b) and isolated object manipulation (Luo et al. 2024a; Tessler et al. 2024). But future large-scale deployments will require robots to operate synergistically. In such settings, two capabilities are crucial: **cooperative manipulation** for multi-robot collaboration and **precise control** for reliable motion execution. Developing these capabilities is essential for advancing from isolated robotic skills to synergistic multi-agent systems. 

Despite their importance, robust cooperative manipulation 

and precise control remain challenging. A key limitation lies in the scarcity of high-quality large-scale datasets that capture human–object–human interactions (HOHI). Most existing datasets focus on single-person motion (Mahmood et al. 2019), dual-human interaction (Liang et al. 2024; Xu et al. 2024), and human–object interaction (HOI) (Taheri et al. 2020; Jiang et al. 2024a,b), while available HOHI data (Liu et al. 2025) is limited in scale and often ill-suited for learning physically grounded control policies. In addition, cooperative manipulation is much more complex than single-agent manipulation. The joint action space grows exponentially with the number of agents, leading to pronounced difficulties in optimization, convergence, and training stability. As a result, even SOTA methods often struggle to generalize to diverse interaction patterns, novel object geometries, and unseen coordination scenarios. 

To overcome these hurdles, as shown in Figure. 1, we present **SynAgent** , a unified framework designed to bridge the chasm between single-agent motor proficiency and multiagent collaborative synergy. Our first contribution addresses the fundamental data bottleneck through an **interactionpreserving retargeting** strategy. Direct motion transfer often suffers from severe skeletal discrepancies, so we utilize a differentiable SMPL-X proxy to bridge the morphology gap between human performers and humanoid agents. We then construct an _Interact Mesh_ via Delaunay tetrahedralization, which effectively encapsulates the local spatial structure between agent joints and object vertices. By minimizing the Laplacian deformation energy of interact meshes during the retargeting process, our method explicitly maintains motion semantics and contact relationships. 

Second, we introduce a **Solo-to-Cooperative Agent Synergy** paradigm. We observe that cooperative manipulation can be conceptually reformulated as a single-agent control problem subject to external force disturbances. This insight allows us to leverage abundant, high-quality single-human HOI data to distill robust motion imitation priors. These individual skills are subsequently evolved into multi-agent synergy through a decentralized training scheme with shared weights, optimized via Multi-Agent Proximal Policy Optimization (MAPPO) to foster emerging collaborative behaviors. As for achieving precise execution, we develop a **trajectory-conditioned policy** as a conditional VAE, which integrates agent states, object trajectories, and geometryaware interaction graphs. To mitigate the ill-posed trajectoryfollowing, we employ a **Multi-Teacher Distillation** framework. By distilling the collective expertise of specialized imitation teachers into a unified student model through a progressive DAgger-style schedule, our framework produces stable, coherent, and highly generalizable multi-agent manipulation motions across diverse object geometries. 

In summary, our primary contributions include: 

- A novel interaction-preserving retargeting method utilizing an Interact Mesh representation to explicitly maintain the semantic integrity and spatial relationships of HOHI data during motion transfer. 

- A Solo-to-Cooperative Agent Synergy paradigm that distills scalable multi-agent cooperative behaviors from 

abundant single-human interaction priors via distilling and decentralized learning. 

- A multi-teacher distillation framework that consolidates diverse motion priors into a unified trajectory-conditioned policy, enabling robust generalization across varying object geometries and trajectories. 

## **Related Work** 

### **Motion Imitation and Retargeting** 

Physics-based motion imitation learns control policies to track reference motions in simulation, as demonstrated by prior work such as DeepMimic (Peng et al. 2018)and Mimickit (Peng 2025), which commonly adopts policy optimization methods like PPO (Schulman et al. 2017). Owing to motion imitation, robotic tasks are decomposed into two subtasks: generation and imitation. Prior work demonstrated compelling results in specialized scenarios, such as human interaction generation (Yao et al. 2025; Jiao et al. 2026), sport interactions (Luo et al. 2024b; Wang et al. 2024; Haarnoja et al. 2024) and object transportation (Bae et al. 2023). (Zhang et al. 2023) achieved handless HOHI motion imitation, but we go further and use the knowledge learned from imitation to achieve more complex trajectory controlling. 

Motion retargeting aims to adapt existing motion data to new embodiments or actors. Recent works (Kim et al. 2016; Zhang et al. 2024b) have achieved impressive progress in this domain, but most of them are not directly designed for scalable multi-human interaction scenarios. For instance, Tairan et al. (He et al. 2024) primarily focus on retargeting motions to robotic, without addressing human–object interaction. Meanwhile, methods such as OmniRetarget (Yang et al. 2025) and SPIDER (Pan et al. 2025) extend retargeting to human-object and are capable of handling interactive motions. But we use interaction-preserving retargeting to refine and enhance **HOHI** data, enabling effective optimization of multi-character interactions. 

### **Human-Object Interaction Generation** 

HOI generation gained increasing attention as a means to synthesize realistic interactions between humans and objects. Existing HOI datasets provided a strong foundation for learning interaction behaviors. Extensive research has explored a wide spectrum, ranging from hand–object (Cha et al. 2024; Christen et al. 2024; Li et al. 2024; Ma et al. 2024; Zhang et al. 2024a, 2025) and static HOI generation (Hou, Yu, and Tao 2023; Kim, Saito, and Joo 2023; Xie, Lenssen, and Pons-Moll 2025) to full-body and dynamic interaction synthesis (Ghosh et al. 2023; Krebs et al. 2021; Lee and Joo 2023; Li, Wu, and Liu 2023; Razali and Demiris 2023; Taheri et al. 2022; Wan et al. 2022; Wu et al. 2022; Xu et al. 2021; Zhang et al. 2022; Yao et al. 2026). 

Compared to HOI, high-quality datasets capturing HOHI remain scarce (Loi, Zacharaki, and Moustakas 2023). CORE4D (Liu et al. 2025) focuses on two-person interaction synthesis. So, its interactions are constrained at a kinematic level, with limited physical fidelity. Scarce data is not the only problem, although progress in multi-agent RL has been 

made (Vaillant, Bouyarmane, and Kheddar 2016). For example, CooHOI (Gao et al. 2024) achieves collaborative multihuman interaction with objects by simplifing all objects into unified box-like proxies. Furthermore, CooHOI constructs an overly engineered reward system that is specifically tailored for box manipulation. On the contrary, our SynAgent adopts a scalable data-driven approach, which uses HOI data cleverly to compensate for the shortage of HOHI data. 

## **Method** 

**Notation.** We use **_p_** and **_q_** to denote position and rotation, respectively, ˙ denotes the relative velocity, e.g., **_p_** ˙ and **_q_** ˙ , and ˆ _._ represents ground truth. 

### **Interaction-Preserving Motion Retargeting** 

The data processing workflow consists of four steps. We first fit a Bridge SMPL-X model to address the non-differentiable forward kinematics of the simulated agent. We then retarget by optimizing the Interact Mesh objective in Equation 2, smooth retargeting results and filter low-quality data. 

**Shape Fitting** Due to skeletal discrepancies between MoCap actors and simulated agents, transferring MoCap data directly often results in incorrect interaction, as highlighted by the red circles in Figure 2. These artifacts hinder training because agents may fail to manipulate objects even when following the reference motion. A central challenge is that the simulated agent’s native forward kinematics pipeline is nondifferentiable, which prevents gradients from propagating through losses defined on joint positions. We therefore perform shape fitting and get a SMPL-X (Pavlakos et al. 2019) template as a differentiable proxy. By matching a SMPL-X template to the target agent’s proportions, we reformulate retargeting as differentiable alignment between two SMPL-X instances and bypass the non-differentiable agent kinematics. The shape fitting objective is defined as 


Here, **_β_** _b ∈_ R<sup>10</sup> denotes the SMPL-X shape parameters; _J_ and **_p_**<sup>target</sup> output the SMPL-X and agent joint positions respectively; and **_θ_** 0 and **_q_** 0 are their T-pose rotations. Iterative optimization yields the agent-matched shape **_β_**<sup>_∗_</sup> _b_<sup>,shownas</sup> the _Bridge SMPL-X_ in Figure 2. 

**Retargeting** To preserve interaction semantics in complex human-object and human-object-human scenarios, we introduce an _Interact Mesh_ constructed via Delaunay tetrahedralization. For each interaction frame, two joints **_p_** 1 _,_ **_p_** 2 from one human, one object mesh vertex **_p_** 3, and one joint **_p_** 4 from the other human form a tetrahedron that captures the local interaction structure. Each tetrahedron _τ_ composed of 4 points _{_ **_p_** 1 _,_ **_p_** 2 _,_ **_p_** 3 _,_ **_p_** 4 _}_ is represented by the 4 _×_ 3 Laplacian matrix **_L_** ( _τ_ ) = _{_ **_p_** _i −_ **_p_** _j | i, j ∈{_ 1 _,_ 2 _,_ 3 _,_ 4 _}, i̸_ = _j}_ . Enforcing its invariance during retargeting preserves the relative spatial relationships among agents and objects. The 


Figure 2: **Interaction-Preserving Retargeting** . (1) The upper part shows the difference between the MoCap actor and the actual agent’s skeletons. (2) In the lower part, the red shows the result of directly retargeting MoCap joints onto the agent, leading to incorrect interaction relationships. The brown area shows how we construct tetrahedrons to describe the interaction relationships, making the interaction relationships unchanged after retargeting. 

retargeting objective at time step _t_ is formulated as 


where the first term enforces Laplacian consistency of the Interact Mesh _τt_<sup>source</sup> and _τt_<sup>target</sup> , and the remaining terms impose temporal smoothness, joint position and velocity limits. The final term penalizes foot sliding by enforcing a stationary foot-joint position **_p_**<sup>_F_</sup> whenever its horizontal velocity **_p_** ˙<sup>_F_</sup> horizontal<sup>fallsbelow0.01m/s.Together,theseconstraints</sup> yield retargeted motions that are physically plausible and faithful to the original interactions. Due to the low quality of the data and the disruption caused by retargeting, we perform additional smoothing on the retargeting data. Please refer to supplementary materials for more details. 

**Filter** Some HOHI motions remain noisy after retargeting and can destabilize training. We therefore use a performancedriven _train-to-filter_ strategy. The policy is trained on the current dataset, and clips whose inference episode lengths fall below the mean _σ_ are removed before retraining. This process repeats until _σ_ converges, allowing the model to focus on reliable demonstrations. Note the evaluation set remains fixed, so there is no bias on evaluation. 


Figure 3: **Overview of SynAgent Training Pipeline.** (1) Stage I pre-trains imitation policies _{_ **_π_**<sup>_s_</sup> _i_<sup>_}N_</sup> _i_ =1<sup>onsingle-humanHOI</sup> data, then adapts them to multi-agent scenarios with MAPPO algorithm. (2) After distilling _{_ **_π_**<sup>_s_</sup> _i_<sup>_}N_</sup> _i_ =1<sup>into a unified Base Model,</sup> Stage II adapts the Base Model to multi-human HOHI data and get policies _{_ **_π_**<sup>_m_</sup> _i_<sup>_}M_</sup> _i_ =1<sup>. (3) Stage III learns a trajectory-conditioned</sup> cVAE policy. Motion imitation policies _{_ **_π_**<sup>_s_</sup> _i_<sup>_}N_</sup> _i_ =1<sup>and</sup><sup>_{_</sup><sup>**_π_**</sup><sup>_m_</sup> _i_<sup>_}M_</sup> _i_ =1<sup>are used to provide physical states as refined training data, and</sup> actions for supervised learning, which stabilize and boost the model training. 

### **Single-Agent Pretraining for Cooperation** 

**Reinforcement Learning Formulation** Our policy follows a single-agent paradigm: at each control step, it observes the state of one agent and outputs only that agent’s action. During deployment, multiple agents are independently controlled by identical copies of this shared policy, enabling decentralized cooperation. 

**State** To capture motion dynamics, the state is represented by two consecutive observations ( **_o_** _t,_ **_o_** _t_ +∆ _t_ ). Each observation contains an **a** gent– **o** bject **o** bservation **_o_**<sup>ao</sup> , an **i** nteraction **g** raph **_ig_** , and a delta interaction graph ∆ **_ig_** = **_ig_** _−_ **_ig_** ref . The interaction graph represents vectors from agent joints to their nearest object-mesh vertices and thus provides geometric contact cues. The agent–object observation **_o_**<sup>ao</sup> is further divided into agent observations **_o_**<sup>a</sup> and object observations **_o_**<sup>o</sup> . For each agent, **_o_**<sup>a</sup> contains joint positions **_p_** , rotations **_q_** , linear and angular velocities **_p_** ˙ and **_q_** ˙ , contact indicators **_c_** , and deviations from the reference motion. The object observation **_o_**<sup>o</sup> contains position **_p_** o, orientation **_q_** o, linear and angular velocities **_p_** ˙ o and **_q_** ˙ o, and deviations from the reference object trajectory. 

**Reward** The reward function is designed to encourage accurate motion imitation while maintaining physical realism during cooperative manipulation. It can be summarized as _R_ = _e_<sup>_−λ_∆(</sup><sup>**∆**</sup><sup>_·_</sup><sup>**_ω_**)</sup> _· e_<sup>_−λc_</sup> � _∥_ **_c_** ˆ _−_ **_c_** _∥⊙_ **_c_** ˆ _· e−λv_ � _∥_ **_v_** _∥−λf_ max _∥_ **_f_** _∥,_ (3) The first term penalizes deviations **∆** between simulated states and reference motions. Contact labels are defined by joint-to-mesh distance: distances below 0 _._ 07 m encourage contact, those from 0 _._ 07 m to 0 _._ 2 m are ignored, and those above 0 _._ 2 m penalize undesired contact. The contact term aligns simulated contacts **_c_** with reference contacts ˆ **_c_** , while the energy-efficiency term suppresses high-frequency joint motion **_v_** = _{_ **_p_** ˙ _,_ **_q_** ˙ _}_ and excessive contact forces **_f_** . In Eq. 3, **_λ_** and **_ω_** denote groups of hyper-parameters for different state components. For showing our method is generalizable, we use the same hyper-parameters across all objects, motions, and tasks without task-specific tuning. 

**Policy & Action** We parameterize the policy with a standard actor–critic MLP. It receives the concatenated observation ( **_o_** _t,_ **_o_** _t_ +∆ _t_ ) and predicts one agent’s joint PD targets **_a_** _t ∈_ R<sup>51</sup><sup>_×_3</sup> in exponential-map form. These targets are con- 

#### verted into torques for the whole-body humanoid. 

**Training Stages of Imitation Policies** Our core idea is to learn fundamental skills from simple tasks and progressively transfer them to more complex scenarios involving two agents. Throughout this process, we keep the network architecture, hyper-parameters, and reward function unchanged. 

**Stage I** In the first step of Stage I, we partition the singlehuman data into _N_ subsets and train a separate policy on each subset, corresponding to the blue networks in Stage I of Figure 3. Subsequently, we perform three operations. First, we augment the single-human data by duplicating the original human. The duplicate is either placed identically to the original or randomly positioned nearby. On this augmented data, we proceed to train a multi-agent policy. For the two agents in the scene (the red and green agents in Figure 3), we employ two networks with shared weights, initialized with the previously trained single-agent policy. A key design is the joint training of this policy using MAPPO algorithm, whose core objective is given by 


where _V_ **_ϕ_** is the critic network, _|_ agent _|_ is the number of agents in a simulated scene _S_ , and _R_<sup>ˆ</sup> _t_ is the real reward, i.e., _R_ in Equation 3. This function aims to integrate information from all agents to jointly optimize the value function model, thereby helping the policy learn collaborative skills. At last, as illustrated at the bottom of Stage I in Figure 3, both agents are trained simultaneously in a shared environment. We disable collisions between agents but enable collisions between each agent and the object. This design allows us to directly leverage single-human data to train multi-agent cooperative skills without forgetting the single-agent abilities, and the agents can perceive each other’s presence through the object’s dynamics. Inter-agent collisions are disabled only in Stage I because the duplicated agents may overlap; all collisions are enabled during subsequent training and inference. 

**Stage II** We distill the _N_ single-human policies _{_ **_π_**<sup>_s_</sup> _i_<sup>_}N_</sup> _i_ =1 into an architecture-matched _Base Model_ using the similar procedure in the next section. This Base Model initializes subsequent training on _M_ subsets of HOHI data. Table 4 shows that the distilled prior substantially stabilizes and accelerates cooperation learning compared with training from scratch. The resulting policies _{_ **_π_**<sup>_s_</sup> _i_<sup>_}N_</sup> _i_ =1<sup>and</sup><sup>_{_</sup><sup>**_π_**</sup><sup>_m_</sup> _i_<sup>_}M_</sup> _i_ =1<sup>con-</sup> stitute the Stage III _Motion Imitation Policies_ and provide state–action supervision for final training. 

### **Generalizable Trajectory-Conditioned Policy** 

As shown in Stage III of Figure 3, our final model, **SynAgent** , is essentially a conditional Variational Autoencoder (VAE). Unlike the imitation policy described earlier, SynAgent removes all observations related to the reference state of the agent from its input. The encoder receives three streams of information: the current _agent states_ **_o_**<sup>a</sup> , the _interaction graph_ **_ig_** , and the _object states_ **_o_**<sup>o</sup> —where the object states **_o_**<sup>o</sup> still include the reference object state as a control signal. 

**Algorithm 1** Learning from Motion Imitation Prior 

**Require:** Motion imitation policies **_π_**<sup>imit</sup> composed of _{_ **_π_**<sup>_s_</sup> _i_<sup>_}_</sup> _i_<sup>_N_</sup> =1<sup>and</sup><sup>_{_</sup><sup>**_π_**</sup> _i_<sup>_m}_</sup> _i_<sup>_M_</sup> =1<sup>, SynAgent policy parameters</sup><sup>**_ψ_**,</sup> SynAgent value function parameters **_ϕ_** , DAgger hyperparameter _ϵ_ and _κ_ , horizon length _H_ , max episode rounds _L_ of imitation training 1: **for** episode _l_ = 0 _,_ 1 _,_ 2 _, . . ._ **do** 2: **for** _t_ = 1 **to** _H_ **do** 3: Sample a variable _u ∼_ Uniform(0 _,_ 1) 4: Obtain **_a_**<sup>_e_</sup> _t_<sup>from</sup><sup>**_π_**imit(</sup><sup>**_a_**</sup><sup>_|_</sup><sup>**_s_**</sup><sup>_e_</sup> _t_<sup>)</sup> 5: Obtain **_a_** _t_ from **_πψ_** ( **_a_** _|_ **_s_** _t_<sup>_e_)</sup> 6: **if** _u ≤_ max �1 _−_ max � _<u>l−ϵκ</u>_<sup>_,_0</sup> � _,_ 0� **then** 7: Given **_s_**<sup>_e_</sup> _t_<sup>, execute</sup><sup>**_a_**</sup><sup>_e_</sup> _t_<sup>, observe</sup><sup>**_s_**</sup><sup>_e_</sup> _t_ +1 8: **else** 9: Given **_s_**<sup>_e_</sup> _t_<sup>, execute</sup><sup>**_a_**</sup><sup>_t_, observe</sup><sup>**_s_**</sup><sup>_e_</sup> _t_ +1 10: **end if** 11: Store the transition ( **_s_**<sup>_e_</sup> _t_<sup>_,_</sup><sup>**_s_**</sup><sup>_e_</sup> _t_ +1<sup>_,_</sup><sup>**_a_**</sup><sup>_t,_</sup><sup>**_a_**</sup> _t_<sup>_e_)</sup> 12: **end for** 13: Update **_ϕ_** according to Eq. 4 14: Compute _J_ ( **_ψ_** ) = _∥_ **_a_** _−_ **_a_**<sup>_e_</sup> _∥_ 15: Compute _w_ = min�max�1 _−_ max� _<u>l−ϵκ</u>_<sup>_,_0</sup> � _,_ 0� _,_ 1� 16: **if** _l < L_ **then** 17: Compute imitation PPO objective: _L_ imit( **_ψ_** ) 18: Update **_ψ_** by _∇_ **_ψ_** ( _wL_ imit( **_ψ_** ) + (1 _− w_ ) _J_ ( **_ψ_** )) 19: **else** 20: Compute trajectory PPO objective: _L_ traj( **_ψ_** ) 21: Update **_ψ_** by _∇_ **_ψ_** ( _wL_ traj( **_ψ_** ) + (1 _− w_ ) _J_ ( **_ψ_** )) 22: **end if** 23: **end for** 

The condition for our final model is defined as a _T ×_ 3 sequence of translations, representing the 3D position of the object across _T_ timesteps. The encoder outputs a latent vector **_z_** , which is then concatenated with [ **_o_**<sup>o</sup> _,_ **_p_** _,_ **_q_** _,_ **_p_ ˙** _,_ **_q_ ˙** _,_ **_ig_** ], and passed to the decoder to generate the corresponding actions **_a_** . In the following, we introduce two core designs of our training algorithm that enable effective learning of this trajectory-conditioned generative policy, which are illustrated in Algorithm 1. 

**Distill from Imitation to Generation** Unlike motion imitation, trajectory-conditioned control is an ill-posed problem. There exist infinitely many possible action sequences that can move an object along a given trajectory, which often leads to training instability and convergence difficulties. To address this, we propose to learn action generation from motion imitation priors. As illustrated in Stage III of Figure 3, we first process the original reference data using our pre-trained imitation policies **_π_**<sup>imit</sup> to produce physically consistent state– action pairs: physical states **_s_**<sup>_e_</sup> and corresponding actions **_a_**<sup>_e_</sup> . The physical states **_s_**<sup>_e_</sup> enhance the raw motion capture data by ensuring full physical plausibility, while the actions **_a_**<sup>_e_</sup> provide direct supervision for the generative model. This strong pairing effectively reduces the under-constrained nature of trajectory control, transforming an open-ended problem into a well-defined one with a unique solution per demonstration. 

**Progressive Skill Acquisition** The complete algorithm flow is shown in Algorithm 1. To ensure stable training and 

|M|ethod|box|bucket|chair|clothes stand|table|floor lamp|monitor|suitcase|tripod|all|
|---|---|---|---|---|---|---|---|---|---|---|---|
|CHOI|Dist._↓_|1.1801|1.382|1.4404|1.3825|1.2835|1.3837|1.1688|1.3088|1.3212|1.3074|
|oo|Succ. Rate_↑_|**14.14%**|2.95%|4.26%|0.00%|10.66%|6.56%|1.64%|3.28%|0.00%|7.28%|
|SAt|Dist._↓_|**0.9985**|**0.3871**|**0.4099**|**0.6524**|**0.7488**|**0.4271**|**0.6009**|**1.1005**|**0.8179**|**0.7939**|
|yngen|Succ. Rate _↑_|11.88%|**51.79%**|**39.33%**|**16.39%**|**12.94%**|**37.23%**|**25.00%**|**5.65%**|**15.48%**|**19.16%**|


Table 1: Comparison for Control. Note that each major category of objects also has various subcategories. See the supplementary materials for detailed experimental results. 

enable a gradual transition from pure imitation of **_π_**<sup>imit</sup> to autonomous action generation, we introduce three key hyperparameters to control the learning schedule. The first two, _ϵ_ and _κ_ , are adopted from the DAgger algorithm. When _l ≤ κ_ , only teacher actions **_a_**<sup>_e_</sup> are executed because the untrained policy **_ψ_** would cause early termination. During _κ < l < ϵ_ + _κ_ , we linearly reduce both the probability of sampling **_π_**<sup>imit</sup> actions and the weight of the action-imitation loss _J_ ( **_ψ_** ). After _κ_ + _ϵ_ episodes, SynAgent executes only its own actions and _J_ ( **_ψ_** ) is removed. The third hyperparameter, _L_ , governs the reward composition. As outlined in Algorithm 1, for the first _L_ episode rounds, we employ the full imitation reward used in Stages I and II to ground the policy. Beyond _L_ , we switch to a sparse reward that depends only on the object’s trajectory tracking error. This shift encourages the policy to explore its own action sequences to achieve the goal, rather than slavishly mimicking the teacher’s motions, thereby significantly improving generalization to novel trajectories and interaction scenarios. 

## **Experiments** 

### **Implementation Details** 

Our experiments are conducted on the OMOMO and CORE4D datasets. OMOMO provides HOI sequences, while CORE4D contains HOHI data. After automatic filtering to remove low-quality samples, we obtain 2,960 motion sequences covering 9 object categories and 25 distinct objects. Based on these data, we train 20 motion imitation models in total, including _N_ = 17 on OMOMO and _M_ = 3 on CORE4D. Each imitation model is trained on a single NVIDIA RTX 3090 GPU, while the final distillation stage for learning the generalizable trajectory-conditioned policy is performed on an NVIDIA A800 GPU. 

**Comparison** Since no prior method is explicitly designed for HOHI imitation or trajectory-controlled cooperative humanoid manipulation, we adopt representative alternatives for comparison. For motion imitation, we use InterMimic (Xu et al. 2025), a state-of-the-art HOI imitation method, applied independently to each agent to generate actions. For trajectory-conditioned control, we compare against CooHOI (Gao et al. 2024), which supports goal-conditioned object manipulation but does not track trajectories. Both methods are evaluated on their ability to cooperatively move an object to a target position, enabling a fair comparison at the object-control level. Qualitative comparison is shown in supplementary materials. Please refer to the demo in the Supp. Mat. for more qualitative results. Meanwhile, besides the results presented in the main paper, the Supp. Mat. contains a wealth of more detailed evaluation results for reference. 

**Ablation Studies** We perform ablation studies to examine key design choices in our framework. These include comparing centralized and decentralized policy structures for dualagent manipulation, evaluating different architectural variants of the VAE-based trajectory-conditioned policy, and assessing the transferability of knowledge learned from singlehuman data to multi-human cooperation. We also ablate the proposed data refinement strategies, including interactionpreserving retargeting and automatic filtering, to quantify their effects on training stability and performance. 

**Metrics** We use task-specific metrics to evaluate both imitation and control. For motion imitation, we report the success rate (Succ. Rate), episode length (Ep. Len.), and accumulated reward (Reward). We further measure accuracy using the success-rate-weighted mean human joint error _Eh_ and object trajectory error _Eo_ , where lower values indicate more accurate imitation. For trajectory-conditioned control, we report the success rate based on a final-position threshold and the average final-position error across all trials, with smaller errors indicating more precise goal-directed manipulation. Please refer to the Supp. Mat. for more details. 

### **Imitation and Control** 

**Comparison of Imitation.** Table 2 compares InterMimic and our method under the imitation setting. Both methods are trained on the same augmented OMOMO dataset using identical data splits, where we train 17 imitation policies _{_ **_π_**<sup>_s_</sup> _i_<sup>_}N_</sup> _i_ =1<sup>for our approach and 17 corresponding models for</sup> InterMimic. By the way, single-human data augmentation strategy is described in Stage I. As shown in the Table 2, although InterMimic achieves strong performance in singlehuman HOI imitation, its performance degrades significantly when an additional agent is introduced as a source of physical interference, indicating limited adaptability to multi-human settings without targeted training. In contrast, our method substantially improves the imitation success rate and consistently outperforms InterMimic across all metrics. Notably, these gains are achieved without modifying the model architecture or tuning hyper-parameters, demonstrating that MAPPO-based joint training is critical for enabling robust multi-agent imitation and highlighting the superiority of our approach in cooperative scenarios. 

|Method|Succ. Rate _↑_|Ep. Len. _↑_|Reward _↑_|_Eh ↓_|_Eo ↓_|
|---|---|---|---|---|---|
|InterMimic|7.26%|51.9151|20.1757|1.7352|1.4329|
|_{_**_π_**<sup>_s_</sup><br>_i_<sup>_}N_</sup><br>_i_=1|**45.00%**|**78.7416**|**25.5555**|**0.2376**|**0.2387**|


Table 2: Comparison for Imitation in OMOMO. More detailed results are on supplementary materials. 

**Comparison of Control.** The closest existing baseline to our task is CooHOI, as both methods are able to cooperatively transport an object to a specified target position. As reported in Table 1, except for box-shaped objects, our method consistently outperforms CooHOI across nearly all object categories. CooHOI is target-conditioned, so we provided it with the final 2D positions of test trajectories. And for fairness, only the distance on 2D plane is calculated when calculating the metrics. Moreover, CooHOI is an AMP-like method, meaning no training set bias existed. CooHOI’s drastic performance degradation stems from its inherent design: it abstracts objects into simple 8-keypoint bounding boxes and lacks dexterous hand modeling. Its performance relies on an over-engineered reward function specifically tailored for picking up the box, which inevitably limits its generalization to other objects. Consequently, it suffers from severe generalization failures when faced with non-box-like (even non-square boxes), complex geometries. 

Moreover, CooHOI does not model dexterous hands, which severely limits its ability to manipulate objects that require stable grasping, such as clothes stands, monitors, and tripods, where its success rate is nearly 0.00%. In contrast, our method demonstrates substantially stronger generalization. The VAE-based policy enables fine-grained trajectoryconditioned control rather than pure goal-conditioned behavior, while the interaction graph provides a more expressive and geometry-aware object representation. Although incorporating dexterous hands significantly increases learning difficulty, our framework successfully overcomes this challenge, allowing a single model to handle a broader range of objects that require precise and coordinated manipulation. 

### **Ablation and Analysis** 

**Centralized or Decentralized** Before training the imitation policies on CORE4D in Stage II, we need to determine which policy architecture can better facilitate dual-agent cooperation. We therefore conduct an architectural ablation study at the Base Model stage. A straightforward approach is a centralized policy, where a single model observes both agents and directly outputs actions for both of them. In principle, such a design allows more explicit information sharing and could simplify coordination between agents. In practice, however, doubling the action space significantly increases the learning difficulty, leading to slower convergence and degraded performance. As a result in Table 3, we observe inferior results compared to alternative designs. We therefore adopt a decentralized policy structure, where each agent is controlled by a shared-weight policy that outputs its own actions. This design not only yields better empirical performance but also offers superior scalability, as it naturally extends to scenarios involving varying numbers of agents. 

**Solo-to-Cooperative Skill Transition** As a core contribution of our work, we need to explicitly validate its effectiveness in facilitating multi-agent skill learning. As shown by the results of _w/o init_ in Table 4, training the multi-human imitation policies _{_ **_π_**<sup>_m_</sup> _i_<sup>_}M_</sup> _i_ =1<sup>without initializing from the Base</sup> Model distilled from single-human policies _{_ **_π_**<sup>_s_</sup> _i_<sup>_}N_</sup> _i_ =1<sup>leads</sup> to a sharp performance degradation. Without a strong skill prior acquired from abundant single-human data, learning 

|Method|Succ. Rate _↑_|Ep. Len. _↑_|Reward _↑_|_Eh ↓_|_Eo ↓_|
|---|---|---|---|---|---|
|Centralized|12.61%|77.0029|17.9975|0.8170|0.8184|
|Decentralized|**19.92%**|**84.0158**|**19.0685**|**0.5404**|**0.5568**|


Table 3: Ablation studies of Centralized vs Decentralized Base Model in OMOMO. **Centralized** means one policy outputs two agents’ actions, and **Decentralized** means two share-weight policies output two agents’ actions separately. 

complex cooperative behaviors from scratch becomes extremely difficult, and the training process often fails to converge. These results demonstrate that transiting single-agent skills is crucial for stable and effective learning in multi-agent cooperative manipulation tasks. 

|C|ompone|nts||M|etrics||
|---|---|---|---|---|---|---|
|Init|Retarget|Filter|Succ. Rate|_↑_Ep. Len._↑_|Reward_↑_|_Eh ↓_<br>_Eo ↓_|
|–|✓|✓|3.33%|79.3216|16.3713|4.8528 4.4174|
|✓|–|✓|2.42%|98.4375|20.2552|6.6776 6.0785|
|✓|✓|–|1.43%|69.7496|13.7437|12.6062 7.9756|
|✓|✓|✓|**21.82%**|**108.4463 **|**20.7419 **|**0.7406 0.6741**|


Table 4: Ablation Studies in CORE4D. We analyze the contribution of each component: initialization with Base Model (Init), Interaction-preserving retargeting (Retarget), and train-to-filter strategy (Filter). ✓indicates the component is used. 

**Data Refinement** Another major contribution is a comprehensive data refinement pipeline for HOHI motion data, whose effectiveness is reflected in the model performance. As shown by the results of _w/o retarget_ in Table 4, interactionpreserving retargeting significantly improves learning by correcting motion artifacts caused by shape discrepancies between human performers and humanoid agents. However, retargeting alone is insufficient. The poor performance of the _w/o filter_ variant highlights that MoCap data contains a substantial number of erroneous and low-quality sequences that cannot be remedied through retargeting alone. Our automatic filtering strategy effectively removes such problematic samples, allowing the model to focus on reliable demonstrations. Together, retargeting and filtering address the fundamental data quality issues in HOHI learning, enabling stable training and substantially improved performance. 

**Limitation** Despite its effectiveness, our work is still an initial step toward cooperative humanoid manipulation. The primary limitation lies in the scarcity of high-quality HOHI data, which prevents our model from scaling to achieve performance leaps. As a result, learning more diverse and complex interaction behaviors remains challenging. 

## **Conclusion** 

We presented SynAgent, a framework for generalizable cooperative humanoid manipulation that addresses the core challenges of data scarcity, coordination complexity, and trajectory control in multi-agent settings. By introducing an interaction-preserving retargeting strategy, we substantially improved the quality and usability of scarce HOHI 

data. Our single-agent pretraining paradigm demonstrates that cooperative manipulation can be effectively distilled from abundant single-human experience, enabling robust decentralized coordination without specialized multi-agent supervision. Furthermore, by distilling motion imitation priors into a trajectory-conditioned generative policy, SynAgent achieves precise and stable object-level control while maintaining strong generalization across object geometries and agent counts. Together, these components establish a scalable pathway from individual manipulation skills to coordinated multi-humanoid behaviors, offering a practical foundation for future research in embodied intelligence, physics-based animation, and multi-agent robotic interaction. 

## **References** 

Bae, J.; Won, J.; Lim, D.; Min, C.-H.; and Kim, Y. M. 2023. Pmp: Learning to physically interact with environments using part-wise motion priors. In _ACM SIGGRAPH 2023 Conference Proceedings_ , 1–10. 

Cha, J.; Kim, J.; Yoon, J. S.; and Baek, S. 2024. Text2hoi: Text-guided 3d motion generation for hand-object interaction. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 1577–1585. 

Christen, S.; Hampali, S.; Sener, F.; Remelli, E.; Hodan, T.; Sauser, E.; Ma, S.; and Tekin, B. 2024. Diffh2o: Diffusionbased synthesis of hand-object interactions from textual descriptions. In _SIGGRAPH Asia 2024 Conference Papers_ , 1–11. 

Gao, J.; Wang, Z.; Xiao, Z.; Wang, J.; Wang, T.; Cao, J.; Hu, X.; Liu, S.; Dai, J.; and Pang, J. 2024. Coohoi: Learning cooperative human-object interaction with manipulated object dynamics. _Advances in Neural Information Processing Systems_ , 37: 79741–79763. 

Ghosh, A.; Dabral, R.; Golyanik, V.; Theobalt, C.; and Slusallek, P. 2023. IMoS: Intent-Driven Full-Body Motion Synthesis for Human-Object Interactions. In _Computer Graphics Forum_ , volume 42, 1–12. Wiley Online Library. Haarnoja, T.; Moran, B.; Lever, G.; Huang, S. H.; Tirumala, D.; Humplik, J.; Wulfmeier, M.; Tunyasuvunakool, S.; Siegel, N. Y.; Hafner, R.; et al. 2024. Learning agile soccer skills for a bipedal robot with deep reinforcement learning. _Science Robotics_ , 9(89): eadi8022. 

He, T.; Luo, Z.; Xiao, W.; Zhang, C.; Kitani, K.; Liu, C.; and Shi, G. 2024. Learning human-to-humanoid real-time whole-body teleoperation. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 8944– 8951. IEEE. 

Hou, Z.; Yu, B.; and Tao, D. 2023. Compositional 3d humanobject neural animation. _arXiv preprint arXiv:2304.14070_ . Jiang, N.; He, Z.; Wang, Z.; Li, H.; Chen, Y.; Huang, S.; and Zhu, Y. 2024a. Autonomous character-scene interaction synthesis from text instruction. In _SIGGRAPH Asia 2024 Conference Papers_ , 1–11. 

Jiang, N.; Zhang, Z.; Li, H.; Ma, X.; Wang, Z.; Chen, Y.; Liu, T.; Zhu, Y.; and Huang, S. 2024b. Scaling up dynamic human-scene interaction modeling. In _Proceedings_ 

_of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 1737–1747. 

Jiao, Z.; Sun, Y.; Zhang, H.; Tang, J.; and Tistarelli, M. 2026. HiTMM: Generative Temporal Masked Modeling of Human Interactive Motions. _IEEE Transactions on Visualization and Computer Graphics_ . 

Kim, T.; Saito, S.; and Joo, H. 2023. Ncho: Unsupervised learning for neural 3d composition of humans and objects. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , 14817–14828. 

Kim, Y.; Park, H.; Bang, S.; and Lee, S.-H. 2016. Retargeting human-object interaction to virtual avatars. _IEEE transactions on visualization and computer graphics_ , 22(11): 2405– 2412. 

Krebs, F.; Meixner, A.; Patzer, I.; and Asfour, T. 2021. The kit bimanual manipulation dataset. In _2020 IEEE-RAS 20th International Conference on Humanoid Robots (Humanoids)_ , 499–506. IEEE. 

Lee, J.; and Joo, H. 2023. Locomotion-action-manipulation: Synthesizing human-scene interactions in complex 3d environments. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , 9663–9674. 

Li, J.; Wu, J.; and Liu, C. K. 2023. Object motion guided human motion synthesis. _ACM Transactions on Graphics (TOG)_ , 42(6): 1–11. 

Li, Q.; Wang, J.; Loy, C. C.; and Dai, B. 2024. Task-oriented human-object interactions generation with implicit neural representations. In _Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision_ , 3035–3044. 

Liang, H.; Zhang, W.; Li, W.; Yu, J.; and Xu, L. 2024. Intergen: Diffusion-based multi-human motion generation under complex interactions. _International Journal of Computer Vision_ , 1–21. 

Liu, Y.; Zhang, C.; Xing, R.; Tang, B.; Yang, B.; and Yi, L. 2025. Core4d: A 4d human-object-human interaction dataset for collaborative object rearrangement. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 1769–1782. 

Loi, I.; Zacharaki, E. I.; and Moustakas, K. 2023. Machine learning approaches for 3d motion synthesis and musculoskeletal dynamics estimation: a survey. _IEEE transactions on visualization and computer graphics_ , 30(8): 5810–5829. 

Luo, Z.; Cao, J.; Christen, S.; Winkler, A.; Kitani, K.; and Xu, W. 2024a. Omnigrasp: Grasping diverse objects with simulated humanoids. _Advances in Neural Information Processing Systems_ , 37: 2161–2184. 

Luo, Z.; Cao, J.; Kitani, K.; Xu, W.; et al. 2023a. Perpetual humanoid control for real-time simulated avatars. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , 10895–10904. 

Luo, Z.; Cao, J.; Merel, J.; Winkler, A.; Huang, J.; Kitani, K.; and Xu, W. 2023b. Universal humanoid motion representations for physics-based control. _arXiv preprint arXiv:2310.04582_ . 

Luo, Z.; Wang, J.; Liu, K.; Zhang, H.; Tessler, C.; Wang, J.; Yuan, Y.; Cao, J.; Lin, Z.; Wang, F.; et al. 2024b. Smplolympics: Sports environments for physically simulated humanoids. _arXiv preprint arXiv:2407.00187_ . 

Ma, J.; Xu, J.; Chen, X.; and Wang, H. 2024. Diff-IP2D: Diffusion-based hand-object interaction prediction on egocentric videos. _arXiv preprint arXiv:2405.04370_ . 

Mahmood, N.; Ghorbani, N.; Troje, N. F.; Pons-Moll, G.; and Black, M. J. 2019. AMASS: Archive of motion capture as surface shapes. In _Proceedings of the IEEE/CVF international conference on computer vision_ , 5442–5451. Pan, C.; Wang, C.; Qi, H.; Liu, Z.; Bharadhwaj, H.; Sharma, A.; Wu, T.; Shi, G.; Malik, J.; and Hogan, F. 2025. SPIDER: Scalable Physics-Informed Dexterous Retargeting. _arXiv preprint arXiv:2511.09484_ . 

Pavlakos, G.; Choutas, V.; Ghorbani, N.; Bolkart, T.; Osman, A. A.; Tzionas, D.; and Black, M. J. 2019. Expressive body capture: 3d hands, face, and body from a single image. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 10975–10985. 

Peng, X. B. 2025. MimicKit: A Reinforcement Learning Framework for Motion Imitation and Control. _arXiv preprint arXiv:2510.13794_ . 

Peng, X. B.; Abbeel, P.; Levine, S.; and Van de Panne, M. 2018. Deepmimic: Example-guided deep reinforcement learning of physics-based character skills. _ACM Transactions On Graphics (TOG)_ , 37(4): 1–14. 

Razali, H.; and Demiris, Y. 2023. Action-conditioned generation of bimanual object manipulation sequences. In _Proceedings of the AAAI conference on artificial intelligence_ , volume 37, 2146–2154. 

Schulman, J.; Wolski, F.; Dhariwal, P.; Radford, A.; and Klimov, O. 2017. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ . 

Taheri, O.; Choutas, V.; Black, M. J.; and Tzionas, D. 2022. GOAL: Generating 4D whole-body motion for hand-object grasping. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 13263–13273. 

Taheri, O.; Ghorbani, N.; Black, M. J.; and Tzionas, D. 2020. GRAB: A dataset of whole-body human grasping of objects. In _European conference on computer vision_ , 581–600. Springer. 

Tessler, C.; Guo, Y.; Nabati, O.; Chechik, G.; and Peng, X. B. 2024. Maskedmimic: Unified physics-based character control through masked motion inpainting. _ACM Transactions on Graphics (TOG)_ , 43(6): 1–21. 

Vaillant, J.; Bouyarmane, K.; and Kheddar, A. 2016. Multicharacter physical and behavioral interactions controller. _IEEE transactions on visualization and computer graphics_ , 23(6): 1650–1662. 

Wan, W.; Yang, L.; Liu, L.; Zhang, Z.; Jia, R.; Choi, Y.-K.; Pan, J.; Theobalt, C.; Komura, T.; and Wang, W. 2022. Learn to predict how humans manipulate large-sized objects from interactive motions. _IEEE Robotics and Automation Letters_ , 7(2): 4702–4709. 

Wang, Y.; Zhao, Q.; Yu, R.; Zeng, A.; Lin, J.; Luo, Z.; Tsui, H. W.; Yu, J.; Li, X.; Chen, Q.; et al. 2024. Skillmimic: Learning reusable basketball skills from demonstrations. _arXiv e-prints_ , arXiv–2408. 

Wu, Y.; Wang, J.; Zhang, Y.; Zhang, S.; Hilliges, O.; Yu, F.; and Tang, S. 2022. Saga: Stochastic whole-body grasping with contact. In _European Conference on Computer Vision_ , 257–274. Springer. 

Xie, X.; Lenssen, J. E.; and Pons-Moll, G. 2025. Intertrack: Tracking human object interaction without object templates. In _2025 International Conference on 3D Vision (3DV)_ , 1427– 1439. IEEE. 

Xu, L.; Lv, X.; Yan, Y.; Jin, X.; Wu, S.; Xu, C.; Liu, Y.; Zhou, Y.; Rao, F.; Sheng, X.; et al. 2024. Inter-x: Towards versatile human-human interaction analysis. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 22260–22271. 

Xu, S.; Ling, H. Y.; Wang, Y.-X.; and Gui, L.-Y. 2025. Intermimic: Towards universal whole-body control for physicsbased human-object interactions. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 12266– 12277. 

Xu, X.; Joo, H.; Mori, G.; and Savva, M. 2021. D3d-hoi: Dynamic 3d human-object interactions from videos. _arXiv preprint arXiv:2108.08420_ . 

Yang, L.; Huang, X.; Wu, Z.; Kanazawa, A.; Abbeel, P.; Sferrazza, C.; Liu, C. K.; Duan, R.; and Shi, G. 2025. Omniretarget: Interaction-preserving data generation for humanoid whole-body loco-manipulation and scene interaction. _arXiv preprint arXiv:2509.26633_ . 

Yao,W.;Sun, Y.;Liu,C.;Zhang,H.; andTang,J.2025. PhysiInter: Integrating Physical Mapping for High-Fidelity Human Interaction Generation. _arXiv preprint arXiv:2506.07456_ . 

Yao, W.; Sun, Y.; Zhang, H.; Liu, Y.; and Tang, J. 2026. Hosig: Full-body human-object-scene interaction generation with hierarchical scene perception. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 40, 11901–11909. 

Zeng, A.; Yang, L.; Ju, X.; Li, J.; Wang, J.; and Xu, Q. 2021. SmoothNet: A Plug-and-Play Network for Refining Human Poses in Videos. _ArXiv_ , abs/2112.13715. 

Zhang, H.; Christen, S.; Fan, Z.; Zheng, L.; Hwangbo, J.; Song, J.; and Hilliges, O. 2024a. Artigrasp: Physically plausible synthesis of bi-manual dexterous grasping and articulation. In _2024 International Conference on 3D Vision (3DV)_ , 235–246. IEEE. 

Zhang, J.; Zhang, Y.; An, L.; Li, M.; Zhang, H.; Hu, Z.; and Liu, Y. 2025. Manidext: Hand-object manipulation synthesis via continuous correspondence embeddings and residualguided diffusion. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ . 

Zhang, J.-Q.; Wang, M.; Zhang, F.-C.; and Zhang, F.-L. 2024b. Skinned motion retargeting with preservation of body part relationships. _IEEE Transactions on Visualization and Computer Graphics_ . 

Zhang, X.; Bhatnagar, B. L.; Starke, S.; Guzov, V.; and PonsMoll, G. 2022. Couch: Towards controllable human-chair interactions. In _European Conference on Computer Vision_ , 518–535. Springer. 

Zhang, Y.; Gopinath, D.; Ye, Y.; Hodgins, J.; Turk, G.; and Won, J. 2023. Simulation and retargeting of complex multicharacter interactions. In _ACM SIGGRAPH 2023 Conference Proceedings_ , 1–11. 

## **Supplementary Material** 

### **Data Preprocessing** 

**Smooth** Although we incorporate smoothness terms in the retargeting objective, the optimized motion sequence may still exhibit jitter. To address this, we apply a post-processing step to the root translation and joint rotations. For the root trajectory **_ρ_** , we employ Sobolev norm regularization. By solving linear equations ( **_I_** + _α_ ( **_D_**<sup>2</sup> )<sup>_T_</sup> **_D_**<sup>2</sup> ) **_ρ_**<sup>_∗_</sup> = **_ρ_** , we get smoothed root trajectory **_ρ_**<sup>_∗_</sup> , where _α_ is regularization parameter and **_D_**<sup>2</sup> is second-order difference operator matrix. For joint rotations, we leverage the pre-trained SmoothNet(Zeng et al. 2021) filter, a lightweight temporal network designed specifically for motion de-jittering. It processes the rotation sequence in a sliding-window manner, effectively suppressing jitter while preserving the essential kinematic posture. This decoupled approach ensures both positional and orientational smoothness in the final retargeted motion. 

**Filter** We initially organized the real-world motion capture data into 7 distinct subsets based on object categories to facilitate specialized training. However, as noted above, our HOHI imitation policies incorporate only 3 policies _{_ **_π_**<sup>_m_</sup> _i_<sup>_}_3</sup> _i_ =1<sup>. This reduction is necessitated by the critically low</sup> quality of the raw CORE4D data, which frequently exhibit severe artifacts such as abrupt trajectory discontinuities, skeletal distortions, and physically implausible contacts. These fundamental defects rendered training non-convergent for several categories, including boards and sticks, and could not be rectified through retargeting or post-optimization. Consequently, we were forced to discard the compromised subsets entirely. 

### **Final Dataset** 

Ultimately, these sequences from both the HOI and HOHI datasets undergo refinement via our imitation policies to generate the physically consistent state-action pairs for training the final Trajectory-Conditioned Policy. By aggregating these resources, we construct a comprehensive training corpus consisting of 20 distinct subsets, comprising 17 derived from single-human data and 3 from multi-human interactions, yielding a total of 2,960 physically validated motion sequences. This diverse dataset encompasses 9 major object categories and 25 unique object geometries, the full variety of which is visualized in Figure 4. To promote reproducibility and facilitate further research in the community, we will release both the curated training dataset and our complete source code upon the acceptance of this paper. 

### **Training Split** 

**Training on OMOMO** The OMOMO dataset serves as our primary source of single-human motion capture data, comprising approximately 10 hours of human-object interactions. To accommodate morphological variations, we partitioned the raw data into 17 distinct subsets based on the body shapes of the actors, yielding a total of 6,435 motion sequences. We initially trained separate imitation policies on these subsets and subsequently extended the training to dual-agent scenarios through data augmentation, resulting in a collection of expert policies denoted as _{_ **_π_**<sup>_s_</sup> _i_<sup>_}_17</sup> _i_ =1<sup>. A critical component of</sup> 


Figure 4: **Overview of 25 Objects.** Our model can ultimately cover these 25 objects. 

our pipeline is the refinement of this data using the trained policies. Since the original OMOMO dataset lacks dexterous hand articulation and contains physically inconsistent artifacts, we employed a physics-based re-tracking procedure to validate the motions. By retaining only the sequences where _{_ **_π_**<sup>_s_</sup> _i_<sup>_}_17</sup> _i_ =1<sup>successfully completed the imitation, we curated a</sup> high-quality dataset of 2,888 physically plausible motions. Finally, this refined dataset was utilized to distill _{_ **_π_**<sup>_s_</sup> _i_<sup>_}_17</sup> _i_ =1 into a unified Base Model, providing a robust initialization for subsequent multi-agent learning. 

**Training on CORE4D** In the second stage, we leverage the CORE4D dataset, a large-scale benchmark for humanobject-human interaction (HOHI) that nominally comprises 11,000 collaboration sequences spanning 3,000 real and virtual object shapes. However, upon closer inspection, we observed that the synthetically generated portion of the dataset exhibits low physical fidelity and contains significant artifacts, rendering it unsuitable for training robust physicsbased control policies. Consequently, we excluded these synthetic samples entirely and restricted our training set exclusively to the real-world motion capture segment. Following a data processing, we distilled the dataset down to 961 sequences, which serve as the initial training data for our multiagent cooperative policies. 

### **More Experiment Results** 

**Metrics** We design task-specific evaluation metrics for imitation and control, respectively. For motion imitation, we report five metrics. The inference success rate (Succ. Rate) measures the probability that a policy can successfully com- 

||Percent. <br>|Succ. Rate _↑_<br>|Ep. Len. _↑_<br>|Reward _↑_<br>|_Eh ↓_<br>|_Eo ↓_<br>|
|---|---|---|---|---|---|---|
|sub1|14.03%|1.40%|52.5902|9.5020|9.2286|7.83576|
|sub2|1.31%|10.34%|65.5994|22.4952|0.9107|0.9204|
|sub3|3.03%|0.50%|41.7012|7.2260|32.5400|22.1000|
|sub4|3.80%|0.40%|51.5622|9.8790|21.3250|17.2000|
|sub5|4.21%|8.24%|81.7084|18.1700|1.4256|0.4110|
|sub6|5.93%|3.31%|56.7799|11.7300|3.0333|1.3909|
|sub7<br>|5.89%<br>|11.03%<br>|66.1516<br>|15.7531<br>|1.2155|1.0591<br>|
|sub8|5.16%|9.06%|56.6106|14.5854|1.4330|1.5615|
|sub9|6.79%|0.00%|33.8088|3.8940|_∞_|_∞_|
|sub10|9.41%|15.06%|53.3284|7.4360|0.9364|0.8907|
|sub11 <br>|2.03%<br>|37.78%<br>|68.4531<br>|21.4116<br>|0.2622<br>|0.0593<br>|
|sub12|4.48%|2.02%|46.4172|10.3300|6.8750|5.7850|
|sub13|6.33%|8.81%|42.7553|6.8939|1.4352|1.4159|
|sub14|7.02%|4.73%|52.1470|8.9440|2.6340|2.3915|
|sub15|8.87%|16.50%|46.0051|7.6330|0.7909|0.6952|
|sub16|5.39%|5.04%|53.3982|12.9800|3.0120|2.2680|
|sub17|6.29%|5.28%|43.2625<br>|6.3382<br>|2.2377<br>|3.0623|
|all|100%|7.26%|51.9151|20.1757|1.7352|1.4329|


Table 5: Evaluation Results of InterMimic in OMOMO. Note that these are evaluation results for OMOMO in a two-agent scenario after it has been expanded to two-agent mode. 

plete an entire motion sequence when evaluated over _N_ demonstrations, where higher values indicate better robustness. Episode length (Ep. Len.) reports the average duration for which imitation remains successful before termination, with longer episode lengths reflecting more stable tracking. The accumulated reward (Reward) evaluates imitation quality, where higher rewards correspond to closer adherence to the reference motion. 

To directly quantify geometric accuracy, we further compute the mean human joint error _Eh_ over only successful episodes, weighted by the inference success rate, such that lower values indicate more accurate human motion reproduction. Similarly, the object error _Eo_ is defined as the weighted mean trajectory error between the manipulated object and the reference object motion, where smaller values correspond to more precise object-level imitation. For trajectoryconditioned control, we adopt two complementary metrics. The success rate (Succ. Rate) is defined by a minimum distance threshold, where a trial is considered successful if the final object position lies within this threshold of the target. In addition, we report the average distance between the final object position and the target position across all trials, with smaller distances indicating more accurate goal-directed manipulation. 

**Imitation on OMOMO** A comparative analysis of Table 5 and Table 6 highlights a critical finding: proficiency in singleagent HOI imitation is insufficient for direct application to multi-agent collaborative tasks. As evidenced in Table 5, although the baseline method (InterMimic) achieves strong results on standard single-human OMOMO sequences, its performance degrades precipitously when applied to our augmented dual-agent scenarios. This decline is primarily attributed to the inability of the policies to accommodate the dynamic perturbations introduced by a second interacting agent. In contrast, Table 6 demonstrates the superior robustness of our approach. By leveraging MAPPO-based joint training, our imitation policies effectively learn to mitigate 

||Percent.|Succ. Rate _↑_|Ep. Len. _↑_|Reward _↑_|_Eh ↓_|_Eo ↓_|
|---|---|---|---|---|---|---|
|sub1|14.03%|29.57%|82.4458|24.7642|0.3771|0.3923|
|sub2|1.31%|79.31%|116.6124|41.7244|0.1111|0.1265|
|sub3|3.03%|59.20%|84.7115|18.8653|0.2049|0.1995|
|sub4|3.80%|44.44%|83.0679|23.3746|0.2664|0.2459|
|sub5|4.21%|34.41%|93.8277|30.4317|0.3173|0.2647|
|sub6|5.93%|11.45%|76.9975|20.1347|0.8044|0.7205|
|sub7|5.89%|50.77%|93.6577|32.2836|0.2017|0.224|
|sub8|5.16%|60.82%|103.3444|34.2238|0.1771|0.1771|
|sub9|6.79%|40.00%|48.7679|9.0562|0.2483|0.2633|
|sub10|9.41%|60.58%|70.589|24.7642|0.2212|0.2136|
|sub11|2.03%|80.00%|95.9667|41.7244|0.1070|0.0616|
|sub12|4.48%|56.57%|87.9563|18.8653|0.1792|0.1944|
|sub13|6.33%|43.81%|68.8254|23.3746|0.2627|0.3186|
|sub14|7.02%|57.85%|95.0348|30.4317|0.1758|0.1801|
|sub15|8.87%|44.05%|59.5867|20.1347|0.2556|0.2427|
|sub16|5.39%|40.06%|79.4779|32.2836|0.2569|0.2683|
|sub17|6.29%|41.01%|65.4814|34.2238|0.2772|0.3299|
|all|100%|45.00%|78.7416|25.5555|0.2376|0.2387|


Table 6: Evaluation Results of _{_ **_π_**<sup>_s_</sup> _i_<sup>_}N_</sup> _i_ =1<sup>inOMOMO.The</sup> same data as Table 5 is used, and the results are compared with those in Table 4. "Ours" refers to imitation policies _{_ **_π_**<sup>_s_</sup> _i_<sup>_}N_</sup> _i_ =1<sup>.</sup> 

||Succ. Rate _↑_|Ep. Len. _↑_|Reward _↑_|_Eh ↓_|_Eo ↓_|
|---|---|---|---|---|---|
|box|4/272=1.47%|62.7061|12.8191|9.6054|2.7551|
|bucket|5/250=2.00%|78.3046|14.3882|8.9950|6.8500|
|chair|2/248=0.81%|68.8705|14.1121|19.5432|14.8395|
|all|11/770=1.43%|69.7496|13.7437|12.6062|7.9756|
|box|9/165=5.45%|109.9828|**22.3496**|2.7302|1.9137|
|bucket|28/250=11.20%|118.1502|20.5744|1.4232|1.2500|
|chair|6/162=3.70%|82.0555|16.9745|4.3027|4.7432|
|all|43/577=7.45%|102.7352|19.9511|2.0912|1.8778|
|box|29/102=28.43%|**110.9783**|21.8224|**0.5388**|**0.4618**|
|bucket|28/84=33.33%|**141.04**|**23.8459**|**0.4875**|**0.4347**|
|chair|15/144=10.42%|**87.6451**|**18.1666**|**1.6218**|**1.5854**|
|all|72/330=21.82%|**108.4463**|**20.7419**|**0.7406**|**0.6741**|


Table 7: Ablation Study of Train-to-Filter in CORE4D. From top to bottom, these are: no filter, first filter and second filter (i.e., _{_ **_π_**<sup>_m_</sup> _i_<sup>_}M_</sup> _i_ =1<sup>).</sup> 

external disturbances, resulting in substantially improved resistance to physical interference. Consequently, our method achieves comprehensive improvements across nearly all evaluated subsets, reaffirming the effectiveness of our framework in bridging the gap between isolated skill acquisition and resilient collaborative execution. 

**Imitation on CORE4D** As demonstrated in Table 7, we validated the effectiveness of our data refinement pipeline by applying the Train-to-Filter strategy over two iterations. A consistent trend is observed across these iterations, where all performance metrics improve following each filtration pass. Crucially, the Succ. Rate metric reveals a dual improvement: not only does the percentage of successful episodes increase, but the number of successfully learned motions also rises. This phenomenon indicates that low-quality data acts as a source of interference during training. By purging these physically inconsistent samples, the model gains the capacity to master complex motions that were previously unlearnable, 

||Succ. Rate _↑_|Ep. Len. _↑_|Reward _↑_|_Eh ↓_|_Eo ↓_|
|---|---|---|---|---|---|
|box|2/102=1.96%|84.2532|17.9991|7.8163|6.6989|
|bucket|7/84=8.33%|91.0018|18.2712|1.9507|1.7394|
|chair|2/144=1.39%|69.0171|14.1104|12.1582|11.8848|
|all|11/330=3.33%|79.3216|16.3713|4.8528|4.4174|
|box|2/102=1.96%|109.8439|**23.9613**|7.9336|2.5408|
|bucket|6/84=7.14%|105.8384|20.0035|2.6526|1.7450|
|chair|0/144=0.00%|86.0424|17.7771|_∞_|_∞_|
|all|8/330=2.42%|98.4375|20.2552|6.6776|6.0785|
|box|29/102=28.43%|**110.9783**|21.8224|**0.5388**|**0.4618**|
|bucket|28/84=33.33%|**141.04**|**23.8459**|**0.4875**|**0.4347**|
|chair|15/144=10.42%|**87.6451**|**18.1666**|**1.6218**|**1.5854**|
|all|72/330=21.82%|**108.4463**|**20.7419**|**0.7406**|**0.6741**|


Table 8: Ablation Study in CORE4D. From top to bottom, these are: no initilization with Base Model, no interactionpreserving retargeting and Ours (i.e., _{_ **_π_**<sup>_m_</sup> _i_<sup>_}M_</sup> _i_ =1<sup>).</sup> 

thereby underscoring the value of our filtering approach. Furthermore, Table 8 provides a more granular breakdown of our ablation studies, where the performance trends across subsets align with the aggregated results, confirming the consistency and robustness of our findings. 

**Motion Control** Complementing the aggregated results presented in the main paper, Table 9 provides a granular performance breakdown for each of the 25 individual object geometries. Consistent with the trends observed in Table 1, our framework demonstrates superior control capabilities and robust geometric generalization, significantly outperforming the CooHOI baseline, even on the box-transport tasks for which CooHOI was specifically optimized. 

|Object|Co<br>|oHOI<br>|Syn<br>|Agent<br>|
|---|---|---|---|---|
||Dist.|Succ. Rate|Dist.|Succ. Rate|
|box001|1.3959|22.95%|**0.3753**|**40.00%**|
|box021<br>|0.9676<br>|16.39%<br>|**0.411**<br>|**55.56%**<br>|
|box023|1.1619|1.64%|**0.2019**|**100.00%**|
|box024|1.1487|26.23%|**0.2965**|**71.43%**<br>|
|box025|0.968|37.70%|**0.3851**|**42.86%**|
|bucket007|1.2274|6.56%|**0.2817**|**85.71%**|
|bucket008|1.2214|3.28%|**0.2373**|**100.00%**|
|bucket009|**1.2589**|**1.64%**|1.3359|0.00%|
|bucket010|1.9481|1.64%|**0.5097**|**40.00%**|
|chair006|1.0154|6.56%|**0.6434**|**25.00%**|
|chair020|1.2553|1.64%|**0.2614**|**66.67%**|
|chair022|1.1807|3.28%|**0.2591**|**100.00%**|
|clothesstand|1.3825|0.00%|**0.6524**|**16.39%**|
|floorlamp|1.3837|6.56%|**0.4271**|**37.23%**|
|largebox|1.1982|4.92%|**1.0594**|**11.64%**|
|largetable|1.3339|**18.03%**|**0.7253**|13.60%|
|monitor|1.1688|1.64%|**0.6009**|**25.00%**|
|plasticbox|1.3409|1.64%|**0.8669**|**7.79%**|
|smallbox|1.2598|1.64%|**1.0379**|**10.16%**|
|smalltable|1.2330|3.28%|**0.7812**|**12.05%**|
|suitcase|1.3088|3.28%|**1.1005**|**5.65%**|
|trashcan|1.2545|1.64%|**0.3783**|**50.33%**|
|tripod|1.3212|0.00%|**0.8179**|**15.48%**|
|whitechair|2.5922|0.00%|**0.3356**|**54.20%**|
|woodchair|1.1585|9.84%|**0.4447**|**28.07%**|
|all|1.3074|7.28%|**0.7939**|**19.16%**|


Table 9: Comparison for Control in OMOMO and CORE4D. A more detailed version of Table 1, categorizes objects in a more specific way. 


Figure 5: **Qualitative Results.** In the comparison between Ours and existing comparable baselines, the blue and green agents are the test results from Ours. In _Comparison of Control_ , the green ball represents the trajectory control signal. In _Performance of Retargeting_ , “direct" indicates that MoCap data is directly transferred to the agent, “orig" represents the raw MoCap data, and “retarget" represents the effect of using our Interaction-preserving retargeting. 

