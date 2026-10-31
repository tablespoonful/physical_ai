---
title: "CMR: Contractive Mapping Embeddings for Robust Humanoid Locomotion on Unstructured Terrains"
date: "2026-02-03"
authors: "Qixin Zeng; Hongyin Zhang; Shangke Lyu; Junxi Jin; Donglin Wang; Chao Huang"
url: https://arxiv.org/abs/2602.03511
pdf: https://arxiv.org/pdf/2602.03511
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.03511)** / [論文ページ](https://arxiv.org/abs/2602.03511)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **CMR: Contractive Mapping Embeddings for Robust Humanoid Locomotion on Unstructured Terrains** 

Qixin Zeng<sup>1</sup> , Hongyin Zhang<sup>2</sup> , Shangke Lyu<sup>3</sup> , Junxi Jin<sup>1</sup> Donglin Wang<sup>2,*</sup> , Chao Huang<sup>1,*</sup> 

**_Abstract_ — Robust disturbance rejection remains a longstanding challenge in humanoid locomotion, particularly on unstructured terrains where sensing is unreliable and model mismatch is pronounced. While perception information, such as height map, enhances terrain awareness, sensor noise and sim-toreal gaps can destabilize policies in practice. In this work, we provide theoretical analysis that bounds the return gap under observation noise, when the induced latent dynamics are contractive. Furthermore, we present Contractive Mapping for Robustness (CMR) framework that maps high-dimensional, disturbance-prone observations into a latent space, where local perturbations are attenuated over time. Specifically, this approach couples contrastive representation learning with Lipschitz regularization to preserve task-relevant geometry while explicitly controlling sensitivity. Notably, the formulation can be incorporated into modern deep reinforcement learning pipelines as an auxiliary loss term with minimal additional technical effort required. Further, our extensive humanoid experiments show that CMR potently outperforms other locomotion algorithms under increased noise.** 


Fig. 1: The left panel illustrates diverse types of challenging terrains I–VI for humanoid locomotion tasks under **noisy** observations. While the radar plot on the right shows that CMR ( **Ours** ) consistently outperforms the baselines under Noise Case III. More results are further reported in Fig. 5. 

## I. INTRODUCTION 

Humanoid robots hold immense potential for operating in human environments [1], especially with the development of whole-body control, which has expanded feasible task sets [2], [3]. Alternatively, achieving stable locomotion remains challenging due to terrain irregularities, actuation perturbations and perception noise [4]. In addition, deployment in unstructured environments typically requires exteroceptive sensing using radar, cameras, or height map [5], [6], [7]. In these extreme scenes, sensing degradation and model mismatch make robustness more critical [8]. 

Approaches to robust humanoid locomotion broadly fall into two categories: model-based control and learning-based methods. On the one hand model-based approaches, such as the ZMP [9], LIP [10], SLIP [11], and SRBD controllers [12] offer interpretability but rely on restrictive assumptions, such as fixed CoM height and simplified centroidal dynamics, limiting their effectiveness on variable terrains [13], [14]. Moreover, model-based controllers solve deterministic optimal control and thus struggle with measurement uncertainty, which may lead to degraded performance under noisy perceptions and imprecise motor actuation [15]. In contrast, learning-based methods have emerged as powerful tools by leveraging large-scale parallel simulations [16]. Notably, modern policy optimization [17] can synthesize more complex behaviors, particularly in the context of Reinforcement Learning (RL) in humanoid robots. Previous work [18], 

> 1University of Southampton; 2Westlake University; 3Nanjing University. 

> *Corresponding author. 

[19] introduced proprioception-only internal embeddings via contrastive learning, enabling robust locomotion without exteroception. Since solely relying on proprioceptive observations is insufficient to achieve a robust sim-to-real transfer, Wang et al. [20] evaluated different types of explicit and implicit estimations incorporated in humanoid robot control. Even when augmenting environment estimation, maintaining robustness on more precise and challenging terrains such as stairs, stepping stones, and balance beams remains nontrivial. For these environments previous work has utilized cameras [18] and radar [5], [6], [15], yet these exteroception devices introduce additional noise [4]. 

Additionally, existing approaches that ensure robustness against observation noise have profound limitations. Traditional methods mitigate noise effects through low-pass filters [21], [22] or smoothness rewards. Since such techniques require tuning overhead to balance smooth behavior with task completion, and filters reduce exploration capacity, they impede controller’s transferability to diverse robotic systems. A recent study, LCP [23] applies Lipschitz constraints via differentiable gradient penalties but remains limited to basic walking behaviors on low-complexity terrains. Crucially, systematically addressing noise robustness in complex humanoid locomotion remains an open research problem. 

To this end, we propose a novel _Contractive Mapping for Robustness_ (CMR) approach, which maps states into a latent space where disturbances are systematically attenuated rather than amplified along trajectories. Our framework combines 

contrastive representation learning for semantic preservation with Lipschitz-constrained control for bounded sensitivity, yielding disturbance-resilient latent dynamics. Furthermore, experiments partially shown in Fig. 1 demonstrate that CMR significantly exceeds other baseline algorithms under elevated observation noise in diverse terrains. Ablation studies further validate the effectiveness of its components. In simto-sim experiments, CMR enables zero-shot deployment and remains performance, providing evidence of generalization. In summary, our contributions are three-fold: 

- We present CMR, a novel contractive-embedding framework that systematically attenuates observation perturbations while preserving task-relevant structure. 

- We are the first to present contraction mapping theorem into learning-based humanoid locomotion task, establishing rigorous bounds on noise-induced return gaps. 

- We introduce a simple but effective training system that integrates seamlessly with normal deep RL pipelines. All Together, these advances enable robust humanoid locomotion across diverse and challenging terrains. 

## II. RELATED WORK 

## _A. Reinforcement Learning for Humanoid Locomotion_ 

With large-scale parallel simulations [16] and modern policy optimization, deep RL can synthesize complex behaviors [17]. Early work in humanoid locomotion primarily relied on proprioceptive feedback to avoid the complexity of visual processing. Previous work [17] used observation and action history containing useful information about the world. Wang et al.[20] proved that learned state estimation is critical for enabling blind walking capability in real-world. While these approaches achieve impressive performance on relatively flat terrains. For more challenging settings including stairs and balancing beams, perception is so critical that humanoid robots can fully exploit the embodiment and perform tasks beyond locomotion on the plane [4]. Recent studies have incorporated visual perception to handle complex terrains. Long et. [5], who followed HIM [24] approach integrating internal models via contrastive learning to infer external states, used onboard elevation map to get ground-truth obstacle heights. BEAM DOJO [6] employs sampling-based foothold rewards with curriculum learning from flat to beams with robot-centric height map. Zhuang et al. [18] presented an end-to-end approach using camera for humanoid parkour without motion priors. These methods enable complex terrain traversal but often suffer from perception noise. While CMR provides rigorous robust bounds for humanoid locomotion policies under noisy observations. 

## _B. Observation Noise in Legged Locomotion_ 

In real-world scenarios, legged robots often lack access to external states such as elevation mapping or contact forces. Moreover, the available onboard observations are potentially corrupted by noise. To address these challenges, prior work has leveraged mimic learning to compensate 

for the missing environmental information. Existing mimiclearning approaches can be broadly grouped into two frameworks: _adaptation_ [25], [26] and _teacher-student_ [27], [28], [29], [30]. Adaptation methods fine-tune a policy online to match the deployment environment, whereas teacher-student methods distill knowledge from a privileged policy as the teacher to a deployable policy as the student under noisy and partial observations [31]. Although these techniques mitigate the sim-to-real gap, a substantial performance drop typically remains between the teacher policy and the final deployable policy [32]. Unlike the above mimic-learning frameworks, CMR purely learns a _contractive state embedding_ that provably limits noise propagation and integrates seamlessly with modern RL frameworks. 

## _C. Sensitivity Control and Robustness_ 

In control systems, ensuring solution existence and stability under constraints and perturbations is a fundamental robustness problem. Toward this goal, _Jacobian regularization_ and _Lipschitz constraints_ are widely used in system control [33], [34]. On the one side, Jacobian-based methods directly penalize input-output sensitivity through gradient penalties [35], [36], aiming to suppress rapid action fluctuations that could damage hardware. On the other side, Lipschitz constraints provide global continuity [37], [38], [39], ensuring that small input perturbations lead to proportionally bounded output changes. This is because Lipschitz constraints can be verified using convex programming and semidefinite programming relaxations [40]. Additionally, it is a critical property for maintaining stability in dynamic systems such as humanoid robots. For instance, practical implementation LCP [23] offers differentiable objectives compatible with deep learning frameworks. Different from these existing sensitivity control methods, CMR focuses on learning a contractive latent space where small disturbances are naturally attenuated over time. 

## PROBLEM FORMULATION 

We model humanoid locomotion as a Partially Observable Markov Decision Process (POMDP) _⟨S, A, f, r, γ, O⟩_ , with the long horizon _H_ . Here, _S_ encompasses the true states including joint angles, velocities, base pose, and exteroceptive features such as height map. _A_ includes continuous motor commands across multiple Degrees of Freedom (DOF). _f_ : _S × A →_ ∆( _S_ ) models the nonlinear, stochastic dynamics arising from contact uncertainties and sensor noise. The Lipschitz constant of the system dynamics _Lf_ reflects system stability [41]. _r_ : _S × A →_ R encodes rewards for stability, progress, and robustness. The Lipschitz constant of the reward function _Lr_ characterizes the robustness of the reward signal itself [42]. _γ ∈_ [0 _,_ 1) is the discount factor. _O_ is the observation space, consisting of noisy exteroceptive and proprioceptive observations. Specifically, given the true state _st ∈_ R<sup>_d_</sup> , the observed state _s_ ˜ _t_ = _st_ + _δs_<sup>_t∈O_,where</sup> _δs_<sup>_t∼U_([</sup><sup>_−ζ, ζ_]</sup><sup>_d_)iszero-meanuniformnoise[43].Ourgoal</sup> 


Fig. 2: **Overview of the CMR framework.** Noisy observations, including current and historical proprioception ( _o_<sup>proprio</sup> _t_ + _δt_<sup>1,</sup><sup>_o_proprio</sup> _t−h_ + _δt_<sup>2)andperception(</sup><sup>_o_</sup> _t_<sup>percept</sup> + _δt_<sup>3),are</sup> encoded into the contractive embedding _It_ . Training _It_ uses a Lipschitz regularization term and a contrastive objective. As a result, the trained contractive embedding _It_ is compatible with deep-RL pipelines as an additional input. 

is to derive a robust policy in noisy conditions: 


where transitions are _s_ ˜ _t_ +1 _∼ f_ (˜ _st, at_ ). Define the policygradient feature as _g_ ( _s, a_ ) := _∇_ log _π_ ( _a | s_ ). Policy value is _J_ ( _π_ ) = E _π_ [<sup>�</sup><sup>_∞_</sup> _t_ =0<sup>_γtr_(˜</sup><sup>_st, at_)].Robustnessisassessedvia</sup> the return gap _J_ ( _π_<sup>_∗_</sup> ) _− J_ ( _π_ ) [44], measuring performance degradation from perturbations. 

## III. METHODOLOGY 

This section details the proposed CMR framework. We begin by analyzing the performance degradation caused by observation noise. We then present the theoretical foundation for the contractive embedding space, followed by the formulation of optimization objectives. Finally, the specifics of training and implementation are presented. All detailed derivations are provided in the Appendix. 

## _A. Motivating Analysis_ 

**Theorem 1** (Return Gap under Observation Noise) **.** _Assume perturbed observations s_ ˜ _t_ = _st_ + _δs_<sup>_twith∥δ_</sup> _s_<sup>_t∥≤δmax,cur-_</sup> _rent policy π with a bounded policy Jacobian ∥∇sπ_ ( _s_ ) _∥≤ M [45], and optimized policy π_<sup>_∗_</sup> _. Then:_ 


Humanoid robots exhibit high DOF, strongly coupled, multimodal dynamics, making conventional low-dimensional representation learning methods inadequate for robustness and transient behavior modeling [19], [20]. In contrast, the embedding in **Theorem 1** bounds policy sensitivity by _M_ 

and ensures observation noise _δs_<sup>_t_degrades</sup><sup>_J_(</sup><sup>_π_) only propor-</sup> tionally, yielding a principled representation. Otherwise, for systems with _Lf ≥_ 1 [46], the _L_<sup>_H_</sup> _f_<sup>termcausesexponential</sup> error growth over horizon _H_ , so minor noise leads to severe degradation. This motivates a more geometric, contractive embedding space where noise is inherently attenuated without _L_<sup>_H_</sup> _f_<sup>amplification,therebyimprovingrobustness.</sup> _B. Analysis of Contractive Embedding Space_ **Theorem 2** (Return Gap in Contractive Embedding Space) **.** _To enhance robustness in humanoid locomotion, we map states into a contractive latent space via an embedding projection ϕ, where disturbances attenuate over time. Let ϕ be a contractive embedding with_ 0 _< κ <_ 1 _, at ∼ π_ ( _·|st_ ) _, a_<sup>_∗_</sup> _t_<sup>_∼π∗_(</sup><sup>_·|st_)</sup><sup>_,ϵt_=</sup><sup>_∥ϕ_(</sup><sup>_f_(</sup><sup>_st, at_))</sup><sup>_−ϕ_(</sup><sup>_f_(</sup><sup>_st, a∗_</sup> _t_<sup>))</sup><sup>_∥,current_</sup> _policy π, and optimized policy π_<sup>_∗_</sup> _satisfy_ E[ _∥at − a_<sup>_∗_</sup> _t_<sup>_∥_]</sup><sup>_≤η_</sup> _for all t [47] satisfying:_ 


_then,_ 


**Global stability through contraction.** In this contractive latent space, state transitions become more regular and predictable, as the contraction property ensures that differences between trajectories shrink over time at rate _κ_ . This regularity directly simplifies policy optimization by reducing the effective complexity of the underlying dynamics, enabling deep RL algorithms to learn stable and efficient policies. Moreover, **Theorem 2** quantifies this benefit: the return gap is bounded by _O_ <u>�</u> 1 _−η κ_ �, where _η_ bounds the expected action discrepancy and 1 _−_ <u>1</u> _κ_<sup>capturestheaccumulationoferrors</sup> under contraction. This analysis reveals how _κ_ precisely governs the trade-off between expressiveness (larger _κ_ ) and robustness (smaller _κ_ ), providing a principled way to limit performance degradation from observation noise. **Long-horizon robustness against error growth.** Contraction embeddings constrain similar states to remain close in the latent space, thereby suppressing the propagation of errors across time steps _H_ . It is worthwhile to note that, compared with **Theorem 1** , this expression is independent of horizon length _H_ , making it significantly more tractable for long-horizon control tasks. 

**Align high-dimensional observations with policy optimization.** The high-dimensional, nonlinear observation spaces (e.g., images, depth maps) in real-world humanoid locomotion, coupled with the robots’ strongly coupled dynamics and vast state spaces, fundamentally lack geometric regularities. Here contractive representation learning is crucial: it maps complex observations into a low-dimensional latent space with _κ <_ 1 dynamics, thereby preserving longhorizon robustness and enabling policy optimization with simplified and geometry-aware dynamics. 

Accordingly, let the noise be _δs_<sup>_t∼U_([</sup><sup>_−ζ, ζ_]</sup><sup>_d_).Thenthe</sup> bias and variance of the policy-gradient feature _g_ ( _s_ ) satisfy 


Var _δ_ � _g_ (˜ _s_ )� _≤_<sup>_<u>ζ</u>_</sup> 3<sup>2</sup><sup>_κ_2</sup><sup>_L_</sup> _π_<sup>2</sup><sup>_d._</sup> (2) joint velocities _θ_<sup>˙</sup> _t ∈_ R<sup>29</sup> ; perceptive observations _o_<sup>percept</sup> _t ∈_ R<sup>15</sup><sup>_×_15</sup> representing an egocentric elevation map centered establish that, under uniform noise, both the around the robot, covering a 1 _._ 5 m _×_ 1 _._ 5 m area with 0 _._ 1 m of _g_ ( _s_ ) are explicitly bounded, thereby resolution, and the previous time step’s action _at−_ 1 _∈_ R<sup>12</sup> or robustness. Nevertheless, we acknowledge _at−_ 1 _∈_ R<sup>29</sup> providing temporal continuity. In the lower-body may yield suboptimal performance comcontrol setting, only the 12 actuated lower-body joints re- **1** when the contraction strength _η_ is too ceive time-varying references from the policy; the remaining constrained by E[[ _|atatt − a_<sup>_∗_</sup> _t_<sup>_|_]</sup><sup>_≤η_,whichmay</sup> upper-body joints remain at their default setpoints. For comenvironment relevant information loss. pleteness, we also consider a whole-body variant in which the action space is expanded to _at ∈_ R<sup>29</sup> and consequently _Functions for Contractive Embeddings at−_ 1 _∈_ R<sup>29</sup> in the observation. The noise magnitude is the foregoing theory, our objectives jointly governed by a global noise level _α_ that uniformly scales **contraction** while preserving sufficient the predefined base noise across observation channels. To , yielding an ideal embedding space mitigate the sim-to-real gap, we inject noise exclusively into **2** . For dynamic contraction, we introthe perception observations during training following Beam regularization term explicitly constraining Dojo[6], with a moderate _α_ = 1. To stress-test robustness, all differences in the embedding space, noise configurations are further amplified in our experiments. 

These bounds establish that, under uniform noise, both the bias and variance of _g_ ( _s_ ) are explicitly bounded, thereby enhancing policy robustness. Nevertheless, we acknowledge that **Theorem 2** may yield suboptimal performance compared to **Theorem 1** when the contraction strength _η_ is too excessive, as constrained by E[[ _|atatt − a_<sup>_∗_</sup> _t_<sup>_|_]</sup><sup>_≤η_,whichmay</sup> lead to task and environment relevant information loss. 

## _C. Objective Functions for Contractive Embeddings_ 

Grounded in the foregoing theory, our objectives jointly promote **dynamic contraction** while preserving sufficient **semantic discrimination** , yielding an ideal embedding space satisfying **Theorem 2** . For dynamic contraction, we introduce a Lipschitz regularization term explicitly constraining the evolution of differences in the embedding space, 

The total training loss combined has detailed in Equ 5. We trained the policy using a double critic framework following the heuristic of Beam Dojo [6], on a single NVIDIA A100 GPU. Initially, ground-truth environmental data in _Isaac Gym_ simulator is employed to train for computational efficiency. To further validate its generalization, the policy trained is transferred into _MuJoCo_ under noisy disturbtions. Additionally, key hyperparameters used in the training process are listed in the appendix. 


where _St_ = _∥ϕ_ ( _st_ ) _− ϕ_ ( _s_<sup>_′_</sup> _t_<sup>)</sup><sup>_∥_2,[</sup><sup>_x_]+=max(</sup><sup>_x,_0)ensures</sup> the penalty applies only when the contraction condition is violated. _L_ Lipschitz aims to build the contractive mapping space _ϕ_ ( _s_ ) with 0 _< κ <_ 1. It also endows the policy with inherent self-stabilizing properties, enabling the robot to intrinsically maintain performance under external disturbances. Complementarily, semantic discrimination is attained by contrastive learning through the InfoNCE loss [48]: 

## IV. EXPERIMENTS 


This section presents complete evaluations. We aim to answer the following questions Is CMR more effective and robust than the baselines? (2) Does each component of CMR contribute to improving its performance? (3) How does CMR generalize in zero-shot transfer scenarios? 

where w _i,jσ_ = exp�sim� _ϕ_ ( _si_ ) _, ϕ_ ( _sjσ_ )� _/τ_ �, _σ ∈{_ + _, −}_ , _s_<sup>+</sup> _i_ and _s_<sup>_−_</sup> _j_ respectively represent a positive and negative sample from the trajectory as _si_ respectively, and _τ_ is the temperature parameter. This objective avoids excessive contraction that loses information in the contractive embedding space _ϕ_ ( _s_ ). We optimize the humanoid locomotion task’s policy _π_ with Proximal Policy Optimization (PPO) [49], leveraging its parallel training capability. In addition to PPO optimization objective _L_ PPO, we set _λ_ as a trade off between semantic discrimination and dynamic contraction. Thus the total training objective _L_ CMR: 

## _A. Evaluation Setups_ 

Baselines. We compare our approach against existing baselines in the context of humanoid locomotion. **HIM:** It uses a hybrid internal embedding representation [24]. Long et [5] integrate it into humanoid control. **LCP:** This method implements Lipschitz constraint with a gradient penalty [23]. **Naive PPO:** It is a plain PPO baseline. 

Disturbance Configurations. We consider two noise categories: proprioceptive and perceptual observation noise. Five disturbance scenarios are considered: **Noise Case I:** High-level noise with _α_ = 2 applied exclusively to the exteroceptive height map input. **Noise Case II:** Mild noise with _α_ = 0 _._ 01 applied to proprioceptive and perceptive observations. **Noise Case III-V:** Noise applied to both observational sources with increasing intensity: moderate _α_ = 1, high _α_ = 2, and extreme _α_ = 3 respectively. 


This formulation ensures that the embedding space _ϕ_ ( _s_ ) simultaneously preserves task-relevant information while guaranteeing the contraction properties necessary, making the CMR framework deployable in humanoid locomotion task. 

## _D. Training Settings and Sim-to-sim Transfer_ 

The full observation space at each time step _t_ is defined as _s_ ˜ _t_ = _ct, o_<sup>proprio</sup> _t , o_<sup>percept</sup> _t , at−_ 1 . The noisy observation � � space _s_ ˜ _t_ consists of four components: command inputs _ct ∈_ R<sup>3</sup> specifying desired velocity commands (longitudinal velocity _vx_ , lateral velocity _vy_ , and angular yaw velocity _ω_ yaw); proprioceptive observations _ot_<sup>proprio</sup> _∈_ R<sup>64</sup> comprising base angular velocity _ωt ∈_ R<sup>3</sup> , joint positions _θt ∈_ R<sup>29</sup> , and 

Dual robot configurations are conducted on the Unitree G1: (1) a constrained 12-DOF setup with the upper body locked, and (2) a full-body configuration with all DOF active. This configuration enables comprehensive assessments of algorithms’ robustness across different kinematic complexities. 

Experiment metrics. We employ diverse metrics for evaluations, including Joint Power, Action Rate (control effort 

TABLE I: Different algorithms’ performance comparison under Noise Cases I/II. 

|**Experiment Settings**||**Environment: U**<br>|**neven Terrain & Disturba**<br>|**nce Configuratio**<br>|**ns: Noise Case I**<br>||
|---|---|---|---|---|---|---|
||**Joint Power (**_↓_**)**|**Action Rate (**_↓_**)**|**Action Smoothness (**_↓_**)**|**Dof Vel (**_↓_**)**|**Dof Acc (**_↓_**)**|**Distance (**_↑_**)**|
|HIM|1971_._9 (_±_712_._2)|10_._6 (_±_4_._7)|10_._8 (_±_4_._8)|170_._4 (_±_66_._9)|430428_._8 (_±_170306_._7)|2_._3 (_±_0_._8)|
|LCP|1333_._3 (_±_1526_._7)|4_._1 (_±_2_._4)|164_._8 (_±_861_._3)|113_._1 (_±_126_._4)|282492_._8 (_±_242580_._8)|5_._8 (_±_1_._8)|
|Naive PPO|13618_._3 (_±_1105_._7)|27_._0 (_±_2_._2)|5431_._7 (_±_617_._4)|1203_._9 (_±_95_._5)|2128629_._0 (_±_151030_._2)|0_._1 (_±_0_._0)|
|**CMR (Ours)**|**1120**_._**7** (_±_277_._5)|**4**_._**1** (_±_1_._4)|**4**_._**5** (_±_1_._6)|**84**_._**5** (_±_24_._6)|**213465**_._**3** (_±_69684_._6)|**7**_._**0** (_±_1_._3)|
|**EitStti**||**Environment: U**|**neven Terrain & Disturba**|**nce Configuratio**|**n: Noise Case II**||
|**xermen ens**|||||||
||**Joint Power (**_↓_**)**|**Action Rate (**_↓_**)**|**Action Smoothness (**_↓_**)**|**Dof Vel (**_↓_**)**|**Dof Acc (**_↓_**)**|**Distance (**_↑_**)**|
|HIM|1486_._2 (_±_885_._4)|8_._1 (_±_5_._6)|8_._6 (_±_5_._9)|133_._9 (_±_84_._2)|372216_._0 (_±_235641_._8)|1_._3 (_±_0_._6)|
|LCP|**976**_._**3** (_±_795_._0)|3_._3 (_±_2_._6)|13_._3 (_±_248_._5)|83_._2 (_±_75_._0)|217245_._5 (_±_180823_._6)|4_._9 (_±_1_._7)|
|Naive PPO|13943_._9 (_±_383_._7)|23_._2 (_±_1_._3)|4103_._4 (_±_234_._1)|1135_._8 (_±_38_._3)|1874354_._3 (_±_80916_._9)|0_._2 (_±_0_._0)|
|**CMR (Ours)**|1012_._3 (_±_350_._3)|**3**_._**2** (_±_1_._5)|**3**_._**4** (_±_1_._6)|**77**_._**8** (_±_31_._3)|**184686**_._**9** (_±_82814_._0)|**7**_._**2** (_±_1_._4)|


TABLE II: Different algorithms’ performance comparison under dual command configurations. 

|**Experiment Settings**|**Enviro**<br>|**nment: Uneven Ter**<br>|**rain (Walking Random) **<br>|**& Disturbance Coi**<br>|**nfigurations: Noise Cas**<br>|**e I**<br>|
|---|---|---|---|---|---|---|
||**Joint Power (**_↓_**)**|**Action Rate (**_↓_**)**|**Action Smoothness (**_↓_**)**|**Dof Vel (**_↓_**)**|**Dof Acc (**_↓_**)**|**Distance (**_↑_**)**|
|HIM|3523_._4 (_±_950_._9)|9_._9 (_±_3_._3)|10_._1 (_±_3_._3)|162_._4 (_±_43_._4)|414386_._5 (_±_110425_._4)|2_._1 (_±_0_._8)|
|LCP|2451_._5 (_±_3230_._6)|**3**_._**8** (_±_1_._3)|213_._6 (_±_969_._4)|116_._6 (_±_134_._1)|282361_._0 (_±_230976_._4)|5_._6 (_±_1_._7)|
|Naive PPO|26832_._2 (_±_1408_._3)|27_._5 (_±_1_._7)|5608_._1 (_±_354_._8)|1230_._6 (_±_57_._9)|2167369_._3 (_±_104718_._8)|0_._08 (_±_0_._02)|
|**CMR (Ours)**|**1854**_._**7** (_±_345_._6)|3_._9 (_±_0_._8)|**4**_._**4** (_±_1_._0)|**81**_._**0** (_±_13_._8)|**206715**_._**1** (_±_39190_._9)|**6**_._**1** (_±_1_._5)|
|**ExerimentSettins**|**Environm**|**ent: Uneven Terrai**|**n (Walking Random OOD**|**) & Disturbance **|**Configurations: Noise C**|**ase II**|
|**p g**|**Joint Power (**_↓_**)**|**Action Rate (**_↓_**)**|**Action Smoothness (**_↓_**)**|**Dof Vel (**_↓_**)**|**Dof Acc (**_↓_**)**|**Distance (**_↑_**)**|
|HIM|2505_._0 (_±_558_._9)|12_._9 (_±_2_._9)|13_._3 (_±_2_._9)|208_._7 (_±_34_._9)|515972_._8 (_±_86794_._4)|2_._1 (_±_0_._6)|
|LCP|1771_._8 (_±_1544_._0)|**5**_._**6** (_±_1_._1)|182_._0 (_±_868_._4)|157_._4 (_±_112_._8)|390014_._1 (_±_190081_._3)|5_._0 (_±_1_._3)|
|Naive PPO|13936_._9 (_±_1752_._7)|26_._2 (_±_2_._9)|5212_._2 (_±_864_._7)|1168_._6 (_±_133_._5)|2074207_._0 (_±_203178_._2)|0_._09 (_±_0_._05)|
|**CMR (Ours)**|**1395**_._**6** (_±_283_._5)|5_._9 (_±_1_._1)|**6**_._**9** (_±_1_._5)|**123**_._**5** (_±_18_._5)|**316543**_._**9** (_±_53703_._2)|**6**_._**2** (_±_0_._8)|


magnitude), Action Smoothness, DoF Velocity, DoF Acceleration, Distance Traveled, and Command Tracking Error. 

## _B. Main Results in Simulation_ 

**Noise Rejection and Stability.** We evaluate the proposed method’s performance across multiple metrics under identical experimental settings (Table. I). Compared with the naive PPO baseline, incorporating the embedding components consistently improves overall performance. In the first scenario, under perceptual noise levels exceeding those in training configurations, controllers utilizing embedding components largely maintain stable and effective locomotion. In the second scenario, where mild noise affects all observations, most methods exhibit a noticeable drop in performance. Conversely, CMR consistently delivers superior performance and preserves locomotion quality across both scenarios. Although LCP demonstrates strength in joint power under Noise Case II, it underperforms in other metrics. Notably, proprioceptive noise has a greater impact on performance degradation than perceptual noise in comparison between Noise Case I and II. Thus experiment below will focus more on the combined effects of both noise sources. Overall, our approach maintains the lowest power consumption, smoothest control actions, and the most stable internal dynamics, showcasing exceptional noise-rejection capability and locomotion stability. 

**Random Velocity and Out-of-distribution Conditions.** 

To evaluate our algorithms’ performance under random velocity commands, we conduct an additional experiment (Table. II). Even in the OOD setting, CMR achieves the longest travel distance and the lowest Action Smoothness score, while operating with the lowest joint power. CMR demonstrates optimal generalization to OOD scenarios coupled with excellent noise immunity, among all algorithms. We hypothesize that the contractive embedding space _ϕ_ ( _s_ ), inherently instills a self-stability attribute in the robot, optimized by the CMR objective. Consequently, the humanoid robot is expected to exhibit superior robustness. Intriguingly, when subjected to amplified noise, the robot executes locomotion tasks more thoroughly, yielding unexpectedly greater walking distances, as corroborated by data presented in Table. I and Table. II. 

**Discriminative Embeddings via t-SNE Visualization.** To elucidate the mechanisms underlying CMR’s superiority, we employed t-SNE [50] to visualize latent embeddings from ours and HIM. In the presence of noise, CMR’s trajectories (Fig. 3) exhibit significantly less deviation, validating its effective maintenance of robot self-stability and resilience in the contractive space. Across diverse terrains under amplified noise, CMR also yields more distinctly separated clusters (Fig. 4), underscoring its retained expressive capacity and environmental identification even within such a contractive space. Collectively, we find that CMR strikes an effective 

balance between dynamic contraction and semantic expressiveness and prove the advantages of **Theorem 2** , intrinsically explaining our approach’s improved performance. 

; 


Fig. 3: Latent space visualizations of five trajectories from deployments of CMR ( **left** ) and HIM ( **right** ) under Noise Case I. 


Fig. 4: Latent space visualizations of trajectories across terrains from deployments of CMR ( **left** ) and HIM ( **right** ). 

**Adaptability Across Diverse Terrain Types.** To further evaluate the environmental adaptation and the locomotion capability in unstructured terrains, we conduct experiments on six challenging and diverse terrains, such as uneven terrains, stepping stones, and balance beam (Fig. 1). The results in Fig. 1 and Fig. 5 show that, across all terrain types and difficulty levels, the robot equipped with the proposed representation contractive embedding consistently covers markedly longer distances than all baseline approaches. 


Fig. 5: Locomotion Distances for deployment of CMR ( **Ours** ) and baselines across varing terrains under Noise Case IV/V. 


Fig. 6: Ablation studies on key hyperparameters in CMR. 

|**Metric**|**HIM**|**CMR (Ours)**|
|---|---|---|
|Command Tracking Error (_↓_)|2.51 (_±_0_._22)|**2.36** (_±_0_._63)|
|DoF Vel (_↓_)|81.09 (_±_18_._68)|**71.34** (_±_22_._25)|
|Action Rate (_↓_)|2.84 (_±_0_._39)|**2.67** (_±_0_._35)|
|Joint Power (_↓_)|1465.43 (_±_902_._67)|**1023.32** (_±_576_._21)|


TABLE III: Sim-to-sim transfer performance comparison between HIM and CMR ( **Ours** ) across four evaluation metrics. 

## _C. Ablation Studies_ 

An ablation study was conducted to evaluate the sensitivity of CMR to temperature _τ_ , Lipschitz parameter _λ_ , and contractive factor _κ_ , under the same simulation settings. As shown in Fig. 6, the results collectively demonstrate a consistent trade-off between trajectory accuracy (Distance) and energy consumption (Joint Power) across all parameters. Increasing _τ_ improves accuracy at the cost of higher energy use and reduced motion dynamics (DoF Vel, DoF Acc), while stronger Lipschitz regularization _λ_ enhances efficiency and smoothness but may limit responsiveness. Similarly, higher _κ_ values suppress oscillations and improve stability, albeit with increased energetic overhead. These inter dependencies validate our default configuration ( _τ_ = 0.04, _λ_ = 0 _._ 05, _κ_ = 0 _._ 1) as a balanced compromise for achieving robust and efficient robotic performance across diverse scenarios. 

## _D. Sim-to-sim Transfer_ 

To validate the generalization capability of CMR, we perform a sim-to-sim transfer by deploying the trained policies 

in the _MuJoCo_ simulation environment. Within _MuJoCo_ , we generate the command _ct_ at each time step by sampling from a uniform distribution under Noise Case I. As shown in Table III, not only dose CMR track command better than HIM, but it also consumes pronouncedly less joint power, suggesting more energy-efficient control. These results demonstrate CMR’s strong zero-shot transfer ability. 

## CONCLUSIONS 

In this paper, we propose a _Contraction Mapping Robustness framework_ (CMR) for robust humanoid locomotion in the presence of observation noise. CMR is the first framework to incorporate the contraction mapping theorem into learning-based robust humanoid locomotion. Its combination of contrastive representation learning and Lipschitz regularization enables explicit sensitivity control while remaining compatible with modern deep RL pipelines. Theoretical analysis further establish return-gap bounds under observation 

noise when latent dynamics are contractive. Comprehensive experiments indicate that CMR maintains a marked lead over alternative locomotion algorithms under amplified noise. Moreover, we are verifying transfer performance through real-robot experiments, thereby strengthening practical credibility. Moving forward, CMR will be augmented with more multi-modal perception such as depth cameras, to perform better in more precise and complex terrains. 

## APPENDIX 

## **(1) Proof of Theorem 1: Return Gap under Observation Noise** 

_Proof._ Setup. We consider _s_ ˜ _t_ = _st_ + _δs_<sup>_t_with</sup><sup>_||δ_</sup> _s_<sup>_t|| ≤δmax_,</sup> and _at_ = _πt_ (˜ _st_ ). The only error source is observation noise. The policy Jacobian satisfies _||∇sπt_ ( _s_ ) _|| ≤ M_ . Goal. Upper bound _J_ ( _π_<sup>_∗_</sup> ) _− J_ ( _π_ ). The action deviation is bounded as follows: _∥at − a_<sup>_∗_</sup> _t_<sup>_∥_=</sup><sup>_∥π_(˜</sup><sup>_st_)</sup><sup>_−π_(</sup><sup>_s∗_</sup> _t_<sup>)</sup><sup>_∥≤M∥s_˜</sup><sup>_t−s∗_</sup> _t_<sup>_∥≤_</sup> _M_ ( _∥st − s_<sup>_∗_</sup> _t_<sup>_∥_+</sup><sup>_∥δ_</sup> _s_<sup>_t∥_)</sup><sup>_≤M_(</sup><sup>_xt_+</sup><sup>_δmax_)</sup><sup>_._ByLipschitzconti-</sup> nuity of the dynamics _f_ : _xt_ +1 = _∥f_ ( _st, at_ ) _− f_ ( _s_<sup>_∗_</sup> _t_<sup>_, a∗_</sup> _t_<sup>)</sup><sup>_∥≤_</sup> _Lf_ ( _∥st − st_<sup>_∗∥_+</sup><sup>_∥at−a∗_</sup> _t_<sup>_∥_)</sup><sup>_≤Lf_(</sup><sup>_xt_+</sup><sup>_Mδmax_)</sup><sup>_._Bounding</sup> _dt_ via Unfolding. With _d_ 0 = 0: 


Return Gap Bound. For discrete reward functions in humanoid locomotion, we approximate them using Gaussian kernel functions [20] to ensure the Lipschitz continuity of the reward with a bounded constant _Lr_ . At each step, using the _Lr_ -Lipschitz continuity of the reward function _r_ : 

E[ _||ηt||_ ] _≤_<sup>_L_</sup> 1<sup>_<u>ϕ</u>_</sup> _−_<sup>_L_</sup> _κ_<sup>_<u>f η</u>_</sup> + _κ_<sup>_t_</sup> _||η_ 0 _||._ The per-step expected reward gap is bounded: 


Summing over the horizon and assuming _η_ 0 = 0, the total return gap is bounded independent of _H_ : 


## **(3) Proof of Bias and Variance Bounds under Contraction** 

The objective is to prove the following two inequalities for the policy feature _g_ under uniform observation noise _δ ∼U_ ([ _−ζ, ζ_ ]<sup>_d_</sup> ), given a contractive embedding _ϕ_ : 


Proof of the Bias Bound. We begin by bounding the norm of the expected difference. 


Summing over horizon _H_ gives the final bound: 


## **(2) Proof of Theorem 2: Return Gap in Contractive Embedding Space** 

Proof of the Variance Bound. The variance of the policy feature _g_ (˜ _s_ ) is defined as Var _δ_ [ _g_ (˜ _s_ )]. 


## **(4) Key hyperparameters in the training process** 

TABLE IV: Hyperparameters used for training. 

_Proof._ The proof analyzes the deviation between a trajectory from policy _π_ and one from the optimal policy _π_<sup>_∗_</sup> . Let _st ∼ P_<sup>_π_</sup> and _s_<sup>_′_</sup> _t_<sup>_∼P π∗_bethestates</sup> at timestep _t_ . We define the latent space deviation as _ηt_ := _ϕ_ ( _st_ ) _− ϕ_ ( _s_<sup>_′_</sup> _t_<sup>).Fromthetheorem’spremise,thelatent</sup> dynamics follow _||ϕ_ ( _st_ +1) _− ϕ_ ( _s_<sup>_′_</sup> _t_ +1<sup>)</sup><sup>_|| ≤κ||ηt||_+</sup><sup>_ϵt_,where</sup> _ϵt_ = _||ϕ_ ( _f_ ( _st, at_ )) _− ϕ_ ( _f_ ( _st, a_<sup>_∗_</sup> _t_<sup>))</sup><sup>_||_.Webound</sup><sup>_ϵt_usingthe</sup> Lipschitz continuity of _ϕ_ (constant _Lϕ_ ) and _f_ (constant _Lf_ ): _ϵt ≤ Lϕ||f_ ( _st, at_ ) _− f_ ( _st, a_<sup>_∗_</sup> _t_<sup>)</sup><sup>_|| ≤LϕLf||at−a_</sup> _t_<sup>_∗||._</sup> 

Substituting this back gives the single-step deviation bound: _||ηt_ +1 _|| ≤ κ||ηt||_ + _LϕLf ||at − at_<sup>_∗||._Takingthe</sup> expectation and unrolling with assumption E[ _||at −a_<sup>_∗_</sup> _t_<sup>_||_]</sup><sup>_≤η_:</sup> 

|**Category**<br>|**Hyperparameter**<br>|**Value**<br>|
|---|---|---|
|General|Number of environments<br>|1200<br>|
|Noise Scales|DOF position<br>DOF velocity<br>Linear velocity<br>Angular velocity<br>Gravity<br>|0.05<br>1.0<br>0.1<br>0.5<br>0.05<br>|
|Height Measurements|Extend probability<br>Vertical scale<br>Offset range<br>|0.6<br>0.02<br>[-0.05, 0.02]<br>|
|Policy Network|Actor hidden dimensions<br>Critic hidden dimensions<br>Activation function<br>|[512, 256, 128]<br>[512, 256, 128]<br>elu<br>|
|Contractive Encoder|Hidden dimensions<br>Activation function<br>|[256, 256, 128]<br>elu<br>|
|Loss Coefficients|Temperature (_τ_)<br>Kappa (_κ_)<br>Lambda (_λ_)|0.04<br>0.1<br>0.05|


ACKNOWLEDGMENT 

## REFERENCES 

- [1] Z. Gu, J. Li, W. Shen, W. Yu, Z. Xie, S. McCrory, X. Cheng, A. Shamsah, R. Griffin, C. K. Liu, _et al._ , “Humanoid locomotion and manipulation: Current progress and challenges in control, planning, and learning,” _arXiv preprint arXiv:2501.02116_ , 2025. 

- [2] T. He, Z. Luo, W. Xiao, C. Zhang, K. Kitani, C. Liu, and G. Shi, “Learning human-to-humanoid real-time whole-body teleoperation,” in _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2024, pp. 8944–8951. 

- [3] T. He, Z. Luo, X. He, W. Xiao, C. Zhang, W. Zhang, K. Kitani, C. Liu, and G. Shi, “Omnih2o: Universal and dexterous humanto-humanoid whole-body teleoperation and learning,” _arXiv preprint arXiv:2406.08858_ , 2024. 

- [4] T. Bin, H. Yan, N. Wang, M. N. Nikoli´c, J. Yao, and T. Zhang, “A survey on the visual perception of humanoid robot,” _Biomimetic Intelligence and Robotics_ , vol. 5, no. 1, p. 100197, 2025. 

- [5] J. Long, J. Ren, M. Shi, Z. Wang, T. Huang, P. Luo, and J. Pang, “Learning humanoid locomotion with perceptive internal model,” _arXiv preprint arXiv:2411.14386_ , 2024. 

- [6] H. Wang, Z. Wang, J. Ren, Q. Ben, T. Huang, W. Zhang, and J. Pang, “Beamdojo: Learning agile humanoid locomotion on sparse footholds,” _arXiv preprint arXiv:2502.10363_ , 2025. 

- [7] W. Xie, C. Bai, J. Shi, J. Yang, Y. Ge, W. Zhang, and X. Li, “Humanoid whole-body locomotion on narrow terrain via dynamic balance and reinforcement learning,” _arXiv preprint arXiv:2502.17219_ , 2025. 

- [8] T. Miki, J. Lee, L. Wellhausen, and M. Hutter, “Learning to walk in confined spaces using 3d representation,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 8649–8656. 

- [9] S. Nakaura, M. Sampei, _et al._ , “Balance control analysis of humanoid robot based on zmp feedback control,” in _IEEE/RSJ International Conference on Intelligent Robots and Systems_ , vol. 3. IEEE, 2002, pp. 2437–2442. 

- [10] Napoleon, S. Nakaura, and M. Sampei, “Balance control analysis of humanoid robot based on zmp feedback control,” in _IEEE/RSJ International Conference on Intelligent Robots and Systems_ , vol. 3, 2002, pp. 2437–2442 vol.3. 

- [11] J. H. Kim, J. Lee, and Y. Oh, “A theoretical framework for stability regions for standing balance of humanoids based on their lipm treatment,” _IEEE Transactions on Systems, Man, and Cybernetics: Systems_ , vol. 50, no. 11, pp. 4569–4586, 2020. 

- [12] J. Li, J. Ma, O. Kolt, M. Shah, and Q. Nguyen, “Dynamic locomanipulation on hector: Humanoid for enhanced control and opensource research,” _ArXiv_ , vol. abs/2312.11868, 2023. 

- [13] B. Pont´on, M. Khadiv, A. Meduri, and L. Righetti, “Efficient multicontact pattern generation with sequential convex approximations of the centroidal dynamics,” _IEEE Transactions on Robotics_ , vol. 37, pp. 1661–1679, 2020. 

- [14] A. W. Winkler, C. D. Bellicoso, M. Hutter, and J. Buchli, “Gait and trajectory optimization for legged systems through phase-based endeffector parameterization,” _IEEE Robotics and Automation Letters_ , vol. 3, pp. 1560–1567, 2018. 

- [15] J. He, C. Zhang, F. Jenelten, R. Grandia, M. B¨acher, and M. Hutter, “Attention-based map encoding for learning generalized legged locomotion,” _Science Robotics_ , vol. 10, no. 105, p. eadv3604, 2025. 

- [16] N. Rudin, D. Hoeller, P. Reist, and M. Hutter, “Learning to walk in minutes using massively parallel deep reinforcement learning,” in _Conference on robot learning_ . PMLR, 2022, pp. 91–100. 

- [17] I. Radosavovic, T. Xiao, B. Zhang, T. Darrell, J. Malik, and K. Sreenath, “Real-world humanoid locomotion with reinforcement learning,” _Science Robotics_ , vol. 9, no. 89, p. eadi9579, 2024. 

- [18] Z. Zhuang, S. Yao, and H. Zhao, “Humanoid parkour learning,” _arXiv preprint arXiv:2406.10759_ , 2024. 

- [19] I. Radosavovic, T. Xiao, B. Zhang, T. Darrell, J. Malik, and K. Sreenath, “Real-world humanoid locomotion with reinforcement learning,” _Science Robotics_ , vol. 9, 2023. 

- [20] Z. Wang, W. Wei, R. Yu, J. Wu, and Q. Zhu, “Toward understanding key estimation in learning robust humanoid locomotion,” in _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2024, pp. 11 232–11 239. 

- [21] Y. Ji, Z. Li, Y. Sun, X. B. Peng, S. Levine, G. Berseth, and K. Sreenath, “Hierarchical reinforcement learning for precise soccer shooting skills using a quadrupedal robot,” in _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2022, pp. 1479–1486. 

- [22] Z. Li, X. Cheng, X. B. Peng, P. Abbeel, S. Levine, G. Berseth, and K. Sreenath, “Reinforcement learning for robust parameterized locomotion control of bipedal robots,” in _2021 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2021, pp. 2811–2817. 

- [23] Z. Chen, X. He, Y.-J. Wang, Q. Liao, Y. Ze, Z. Li, S. S. Sastry, J. Wu, K. Sreenath, S. Gupta, _et al._ , “Learning smooth humanoid locomotion through lipschitz-constrained policies,” _arXiv preprint arXiv:2410.11825_ , 2024. 

- [24] J. Long, Z. Wang, Q. Li, J. Gao, L. Cao, and J. Pang, “Hybrid internal model: Learning agile legged locomotion with simulated robot response,” _arXiv preprint arXiv:2312.11460_ , 2023. 

- [25] G. B. Margolis and P. Agrawal, “Walk these ways: Tuning robot control for generalization with multiplicity of behavior,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 22–31. 

- [26] A. Kumar, Z. Fu, D. Pathak, and J. Malik, “Rma: Rapid motor adaptation for legged robots,” _arXiv preprint arXiv:2107.04034_ , 2021. 

- [27] J. Wu, G. Xin, C. Qi, and Y. Xue, “Learning robust and agile legged locomotion using adversarial motion priors,” _IEEE Robotics and Automation Letters_ , vol. 8, no. 8, pp. 4975–4982, 2023. 

- [28] G. B. Margolis, G. Yang, K. Paigwar, T. Chen, and P. Agrawal, “Rapid locomotion via reinforcement learning,” _The International Journal of Robotics Research_ , vol. 43, no. 4, pp. 572–587, 2024. 

- [29] D. Chen, B. Zhou, V. Koltun, and P. Kr¨ahenb¨uhl, “Learning by cheating,” in _Conference on robot learning_ . PMLR, 2020, pp. 66–75. 

- [30] J. Lee, J. Hwangbo, L. Wellhausen, V. Koltun, and M. Hutter, “Learning quadrupedal locomotion over challenging terrain,” _Science robotics_ , vol. 5, no. 47, p. eabc5986, 2020. 

- [31] M. Bogdanovic, M. Khadiv, and L. Righetti, “Model-free reinforcement learning for robust locomotion using demonstrations from trajectory optimization,” _Frontiers in Robotics and AI_ , vol. 9, p. 854212, 2022. 

- [32] J. Lee, M. Bjelonic, A. Reske, L. Wellhausen, T. Miki, and M. Hutter, “Learning robust autonomous navigation and locomotion for wheeledlegged robots,” _Science Robotics_ , vol. 9, 2024. 

- [33] S. Daudin, “Optimal control of the fokker-planck equation under state constraints in the wasserstein space,” _Journal de Math´ematiques Pures et Appliqu´ees_ , 2021. 

- [34] J. Kim, J. Shin, and I. Yang, “Hamilton-jacobi deep q-learning for deterministic continuous-time systems with lipschitz continuous controls,” _J. Mach. Learn. Res._ , vol. 22, pp. 206:1–206:34, 2020. 

- [35] D. Varga, A. Csisz´arik, and Z. Zombori, “Gradient regularization improves accuracy of discriminative models,” _arXiv preprint arXiv:1712.09936_ , 2017. 

- [36] R. Achtibat, S. M. V. Hatefi, M. Dreyer, A. Jain, T. Wiegand, S. Lapuschkin, and W. Samek, “Attnlrp: attention-aware layer-wise relevance propagation for transformers,” _arXiv preprint arXiv:2402.05602_ , 2024. 

- [37] S. Mysore, B. Mabsout, R. Mancuso, and K. Saenko, “Regularizing action policies for smooth control with reinforcement learning,” in _2021 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2021, pp. 1810–1816. 

- [38] T. Kobayashi, “L2c2: Locally lipschitz continuous constraint towards stable and smooth reinforcement learning,” in _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , Oct 2022, pp. 4032–4039. 

- [39] S. Pradhan and S. Y¨uksel, “Near optimality of lipschitz and smooth policies in controlled diffusions,” _Systems & Control Letters_ , vol. 193, p. 105943, 2024. 

- [40] M. Fazlyab, A. Robey, H. Hassani, M. Morari, and G. Pappas, “Efficient and accurate estimation of lipschitz constants for deep neural networks,” _Advances in neural information processing systems_ , vol. 32, 2019. 

- [41] M. Jin and J. Lavaei, “Stability-certified reinforcement learning: A control-theoretic perspective,” _IEEE Access_ , vol. 8, pp. 229 086– 229 100, 2020. 

- [42] F. De Lellis, M. Coraggio, G. Russo, M. Musolesi, and M. di Bernardo, “Guaranteeing control requirements via reward shaping in reinforcement learning,” _IEEE Transactions on Control Systems Technology_ , vol. 32, no. 6, pp. 2102–2113, 2024. 

- [43] S. Gu, L. Shi, M. Wen, M. Jin, E. Mazumdar, Y. Chi, A. Wierman, and C. Spanos, “Robust gymnasium: A unified modular benchmark for robust reinforcement learning,” _arXiv preprint arXiv:2502.19652_ , 2025. 

- [44] J. C. Kiemel and T. Kr¨oger, “Learning collision-free and torque-limited robot trajectories based on alternative safe behaviors,” _2022 IEEE-RAS 21st International Conference on Humanoid Robots (Humanoids)_ , pp. 223–230, 2021. 

- [45] O. Gannot, “A frequency-domain analysis of inexact gradient methods,” _Mathematical Programming_ , vol. 194, pp. 975–1016, 2019. 

- [46] S. Kajita, F. Kanehiro, K. Kaneko, K. Fujiwara, K. Harada, K. Yokoi, and H. Hirukawa, “Biped walking pattern generation by using preview control of zero-moment point,” in _2003 IEEE International Conference on Robotics and Automation (Cat. No.03CH37422)_ , vol. 2, 2003, pp. 1620–1626 vol.2. 

- [47] M. Liu, X. Wang, and Z. Li, “Robust bipartite consensus and tracking control of high-order multiagent systems with matching uncertainties and antagonistic interactions,” _IEEE Transactions on Systems, Man, and Cybernetics: Systems_ , vol. 50, no. 7, pp. 2541–2550, 2020. 

- [48] A. v. d. Oord, Y. Li, and O. Vinyals, “Representation learning with contrastive predictive coding,” _arXiv preprint arXiv:1807.03748_ , 2018. 

- [49] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 

- [50] L. v. d. Maaten and G. Hinton, “Visualizing data using t-sne,” _Journal of machine learning research_ , vol. 9, no. Nov, pp. 2579–2605, 2008. 

