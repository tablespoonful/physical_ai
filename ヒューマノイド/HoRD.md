---
title: "HoRD: Robust Humanoid Control via History-Conditioned Reinforcement Learning and Online Distillation"
date: "2026-02-04"
authors: "Puyue Wang; Jiawei Hu; Yan Gao; Junyan Wang; Yu Zhang; Gillian Dobbie"
url: https://arxiv.org/abs/2602.04412
pdf: https://arxiv.org/pdf/2602.04412
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.04412)** / [論文ページ](https://arxiv.org/abs/2602.04412)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **HoRD: Robust Humanoid Control via History-Conditioned Reinforcement Learning and Online Distillation** 

**Puyue Wang**<sup>_∗_1</sup> **Jiawei Hu**<sup>_∗_2</sup> **Yan Gao**<sup>3</sup> **Junyan Wang**<sup>4</sup> **Yu Zhang**<sup>5</sup> **Gillian Dobbie**<sup>1</sup> **Tao Gu**<sup>5</sup> **Wafa Johal**<sup>6</sup> **Ting Dang**<sup>6</sup> **Hong Jia**<sup>1</sup> 


tonywang-0517.github.io/hord/ 

## **Abstract** 

Humanoid robots can suffer significant performance drops under small changes in dynamics, task specifications, or environment setup. We propose HoRD, a two-stage learning framework for robust humanoid control under domain shift. First, we train a high-performance teacher policy via history-conditioned reinforcement learning, where the policy infers latent dynamics context from recent state–action trajectories to adapt online to diverse randomized dynamics. Second, we perform online distillation to transfer the teacher’s robust control capabilities into a transformer-based student policy that operates on sparse root-relative 3D joint keypoint trajectories. By combining history-conditioned adaptation with online distillation, HoRD enables a single policy to adapt zero-shot to unseen domains without per-domain retraining. Extensive experiments show HoRD outperforms strong baselines in robustness and transfer, especially under unseen domains and external perturbations. 

## **1. Introduction** 

Humanoid robots promise to unify locomotion, manipulation, and whole-body interaction in dynamic, human-centric environments. Recent advances in high-level planning and abstraction, ranging from vision–language–action (VLA) systems (Ahn et al., 2022; Driess et al., 2023; Brohan et al., 2023; Zhao et al., 2025; Kim et al., 2024) to learning-based planning and latent behavior modeling in reinforcement learning (Janner et al., 2022; Ghosh et al., 2023), have significantly improved semantic reasoning and task specification. Such high-level specifications are often formalized as 

> *Equal contribution 1University of Auckland 2University of New South Wales<sup>3</sup> University of Cambridge<sup>4</sup> University of Adelaide<sup>5</sup> Macquarie University<sup>6</sup> University of Melbourne. Correspondence to: Hong Jia _<_ hong.jia@auckland.ac.nz _>_ . 

_Preprint. March 17, 2026._ 

goal-conditioned or multi-task reinforcement learning (RL) problems (Schaul et al., 2015). However, learning policies that map these high-level commands to stable, torque-level humanoid control remains a fundamental challenge, particularly under distribution shift where test-time dynamics, contact properties, or physics engines differ from training conditions. 

Existing physics-based control policies are typically trained on dense motion-capture datasets (Peng et al., 2018; Mahmood et al., 2019) within a single simulator with fixed dynamics parameters. These methods suffer from two critical limitations. First, the training distribution is limited and sparse: motion datasets cover only a narrow range of skeleton definitions, frame rates, and input modalities, leading to incomplete motion-manifold coverage and hindering scalable learning and fair method comparison. Second, policies overfit to source-domain dynamics and exhibit catastrophic failure under domain shift (Cobbe et al., 2020), such as when operating with different motion patterns, on different terrains, or when evaluated in different simulation engines. Recent masked imitation method (i.e., MaskedMimic) (Tessler et al., 2024) addresses data fragmentation by reformulating control as masked motion inpainting, achieving visually plausible motions but lacking generalization robustness. When evaluated in a different physics engine, these policies fail to maintain stability, limiting their utility as reliable execution layers. 

Together, data fragmentation and domain shift expose a key gap: current methods lack a unified, robust representation from high-level motion specifications to torque-level control that generalizes across data sources and physical environments. This motivates a learning framework that (i) is able to track human-like motions from sparse motion commands, (ii) generalizes robustly under distribution shifts in physical dynamics or simulators, and (iii) is capable of _adapting online_ to unobserved dynamic changes (e.g., mass distribution, friction, actuator delay); otherwise, small model mismatches can compound into large tracking errors and destabilize torque control over long horizons. 

We propose HoRD, a learning framework that maps sparse 

1 

**HoRD: Robust Humanoid Control via History-Conditioned Reinforcement Learning and Online Distillation** 

motion commands (formalized as root-relative 3D joint keypoint trajectories) to torque-level humanoid control with strong cross-domain generalization. HoRD uses a two-stage pipeline in which we (i) train a high-performance teacher torque policy via RL on large-scale real world human motion data under diverse randomized dynamics, and (ii) distill it into a transformer-based student that executes sparse keypoint commands. Both teacher and student are conditioned by HCDR, a history-based module that infers a latent dynamics context from recent state–action trajectories for online compensation to handle domain shift, while the student additionally operates in SSJR, a standardized sparse-joint command representation that addresses data fragmentation by unifying fragmented datasets to process sparse keypoint commands from diverse motion sources. 

This work makes the following contributions: 

- We propose a two-stage learning framework that maps sparse root-relative 3D joint keypoint trajectories to torque-level humanoid control with strong cross-domain generalization. 

- We introduce a history-conditioned RL framework that infers latent dynamics parameters from recent state–action sequences, enabling online adaptation to distribution shift and significantly improving cross-domain generalization and zero-shot transfer. We also released a large-scale trajectory dataset of 7,000+ diverse humanoid motions (100+ hours), to help the community train and evaluate their specific humanoid robots. 

- Extensive evaluations show that HoRD consistently outperforms state-of-the-art baselines, achieving up to 14.2% higher success rates under domain shift and enabling reliable zero-shot transfer from IsaacLab to an unseen physics engine (Genesis), where prior methods degrade or fail catastrophically. 

## **2. Related Work** 

**Physics-guided policy learning for humanoid control.** Physics-based character control learns humanoid behaviors by optimizing torque-level policies under contact-rich dynamics in simulation. Early work focused on imitation and motion tracking of individual reference clips, producing realistic locomotion and agile behaviors from curated demonstrations (Peng et al., 2017; 2018). More recently, the increasing availability of large-scale motion capture datasets such as AMASS (Mahmood et al., 2019) has enabled methods to scale toward training over diverse and heterogeneous motion collections. Such policy learning across broad skill distributions has been extensively studied in the context of multi-task optimization and transfer, with challenges including gradient interference and negative transfer across behaviors (Sener & Koltun, 2018; Yu et al., 2020; Wang 

et al., 2025; Zhang et al., 2024). Along this scaling direction, some work has explored two complementary paradigms to support large-scale motion learning: expert-based decomposition with mixture-of-experts routing or distillation frameworks (Won et al., 2020; Shazeer et al., 2017; Zhou & et al., 2022; Fedus et al., 2022), such as Hover (He et al., 2025c) and ExBody2 (Ji et al., 2024); and unified-policy training strategies that acquire broad motion priors through adversarial imitation or masked objectives without explicit expert routing, as demonstrated in AMP (Peng et al., 2021) and OmniH2O (He et al., 2025b). However, a fundamental limitation persists: existing methods require dense reference trajectories (i.e., full joint-space motion target) during both training and deployment. This creates a critical deployment gap, as real-world motion planners, video-to-motion systems, and high-level controllers typically provide only _sparse keypoint commands_ (e.g., only the 3D positions of key body joints such as shoulders, hips, and knees extracted from video, rather than complete joint-space trajectories with all 20+ joint angles) rather than complete joint trajectories. Moreover, heterogeneous motion sources often use incompatible skeleton definitions and temporal resolutions, further complicating integration. 

HoRD addresses this limitation through SSJR, a standardized sparse-joint representation that unifies fragmented motion sources into a single training distribution, enabling policies to operate directly from sparse commands. By adopting a teacher–student framework, HoRD trains a robust and unified expert policy using dense references (which are available in simulation), then distills this expertise into a lightweight student policy that executes from sparse SSJR commands, bridging the gap between simulation training and real-world deployment. 

**Cross-domain generalization and dynamics adaptation.** Generalization across domains (e.g, different motions, terrains and environments) with varying dynamics is a longstanding challenge in reinforcement learning, particularly for contact-rich control problems (Cobbe et al., 2019). A common strategy is domain randomization, which exposes policies to a distribution of physical parameters during training to enable zero-shot transfer (Tobin et al., 2017; Campanaro et al., 2024), as demonstrated by recent humanoid controllers such as Hover (He et al., 2025c), ExBody2 (Ji et al., 2024), and OmniH2o (He et al., 2025b). An alternative line of work focuses on target-domain adaptation, such as residual or delta-action learning(He et al., 2025a), which leverages limited target-domain data to compensate for dynamics mismatch (Chebotar et al., 2019). However, both approaches have limitations. Domain randomization alone is insufficient. Even with extensive parameter coverage, policies cannot anticipate all possible dynamic variations, and the learned representations often fail to adapt when encoun- 

2 

**HoRD: Robust Humanoid Control via History-Conditioned Reinforcement Learning and Online Distillation** 


_Figure 1._ **Framework overview.** Two-stage teacher–student learning pipeline for robust humanoid control under partial observability. **Stage I:** an expert policy _π_<sup>_⋆_</sup> is trained with PPO in simulation using privileged full-state observations **s** _t_<sup>full, dense future motion intent</sup> **Y** _t_<sup>full, and episode-level domain randomization</sup><sup>**_ψ_**(</sup><sup>_e_).A shared HCDR module encodes the interaction history</sup><sup>_H_</sup> _t_<sup>into a temporal memory</sup> embedding **m** _t_ for online dynamics inference and adaptive modulation. **Stage II:** a deployable student policy _π_ receives only sparse proprioception **s**<sup>sparse</sup> _t_ , environment context **g** _t_ , and standardized motion commands **Y** _t_<sup>sparse</sup> via SSJR, and is trained by distillation to match the expert’s actions. SSJR maps a global planner command into a platform-agnostic sparse-joint command interface, enabling cross-platform transfer while HCDR provides in-context adaptation to latent dynamics during deployment. 

tering novel dynamics at test time. Recent humanoid control systems demonstrate strong performance under nominal training conditions, but exhibit noticeable degradation under distribution shifts, including changes in contact dynamics, actuator delays, or physics engines (He et al., 2025c;b; Ji et al., 2024). Moreover, aggressive randomization can make optimization more difficult and slow convergence for high-dimensional humanoid systems. Target-domain adaptation methods, while effective, require additional interaction and fine-tuning in the target domain, which is impractical for real-world deployment where collecting and labeling target-domain data may be costly or unsafe. HoRD resolves this through HCDR, a novel history-conditioned dynamics adaptation mechanism that learns to infer latent dynamics parameters from recent state–action sequences. 

Unlike prior adaptation methods that require target-domain data, HCDR enables _online adaptation_ at test time by encoding how the environment has recently responded to policy actions. This learned representation enables zero-shot transfer without any target-domain fine-tuning, addressing the fundamental limitation that static domain randomization cannot fully capture the dynamics variations encountered in deployment. Appendix A.3 provides a structured comparison of representative prior humanoid control frameworks and our method along three deployment-relevant capabilities: unified skill coverage, sparse-command generalization, and explicit online dynamics adaptation 

## **3. Method** 

We propose a framework for robust, anticipatory humanoid control that generalizes across domains. Our approach decomposes the control problem into three primary components: _SSJR_ for standardized motion representation, _Episode-Level Domain Randomization_ for distributional robustness, and _HCDR_ for history-conditioned dynamics representation. 

### **3.1. Problem Definition** 

We formalize the task of learning an adaptive, domainagnostic control policy as a _Contextual Partially Observable Markov Decision Process_ (C-POMDP) (Hallak et al., 2015). This formulation explicitly models both the robot’s partial observability and latent variations in environment dynamics. 

**Latent Environment Dynamics.** Each episode _e_ is associated with an unobserved, episode-specific physical parameter vector **_ψ_**<sup>(</sup><sup>_e_)</sup> _∼ P_ (Ψ) that encodes physical properties such as control delay, body mass scaling, and gravity magnitude. The robot state **s** _t_ evolves according to parameterized transitions that depend on **_ψ_**<sup>(</sup><sup>_e_)</sup> , where **s** _t_ represents the robot’s configuration and dynamics state at time _t_ . The control modulation signal **_α_** _t_ allows the robot to adapt its behavior to the specific latent dynamics of the current episode. 

**Observations and Anticipatory Input.** To enable anticipatory control, the robot receives future motion intentions **Y** _t_ over a short-horizon lookahead, which provide guidance for upcoming movements. The robot also maintains historical interactions _Ht_ (formally defined in §3.2), capturing recent state-action pairs that encode how the environment has responded to previous control commands. Additionally, the robot observes environmental context **g** _t_ , such as terrain geometry or obstacles, which informs its control decisions. 

**Policy Objective.** The goal is to learn a policy _π_ that generates adaptive proportional-derivative (PD) targets as the control modulation signal **_α_** _t_ based on both the observed history and future motion intent. The policy leverages a temporal memory embedding **m** _t_ (see §3.5) that captures latent dynamics information, enabling the policy to adapt its control strategy in real-time. The optimal policy maximizes performance across diverse physical and environmental conditions, where _t_ denotes discrete time steps, _T_ is the episode horizon (an episode starts from initialization and terminates 

3 

**HoRD: Robust Humanoid Control via History-Conditioned Reinforcement Learning and Online Distillation** 

when the tracking error exceeds a threshold), and _γ ∈_ [0 _,_ 1) is the discount factor. 

**_ψ_**<sup>(</sup><sup>_e_)</sup> using domain randomization (see §3.4), the expert policy learns to handle a wide range of latent dynamics and environment variations. 

### **3.2. Framework Overview** 

We propose a two-stage learning framework designed to bridge the gap between high-fidelity simulation and realworld deployment under partial observability as shown in Figure 1. The framework leverages a teacher-student distillation paradigm: a full-observation expert policy provides supervision to a deployable student policy that operates under realistic, sparse sensory inputs. 

Both the expert and student policies utilize a shared mechanism for processing historical interactions. They collect a history window 


containing recent state-action pairs, where _K_ is the history window length. This history is processed by the proposed HCDR module (see §3.5) to produce a temporal memory embedding **m** _t_ that captures latent dynamics information and serves as a key input to both policies, enabling adaptive control based on how the environment responds to previous actions. 

**Stage I: Full-Observation Expert Training.** In the first stage, we train an expert (teacher) policy _π_<sup>_⋆_</sup> in simulation with privileged access to the full state **s**<sup>full</sup> _t_<sup>, including</sup> link velocities, contact forces, and precise joint torques, as well as dense future motion intent **Y** _t_<sup>full</sup> derived from highfrequency motion capture data. The expert obtains temporal memory embedding **m** _t_ from historical interactions _Ht_ (as mentioned above). The expert then predicts the control modulation signal 


where **_α_**<sup>(1)</sup> _t_ is the expert policy output, _fθ_ 1 is the expert policy network parameterized by _θ_ 1, **s**<sup>full</sup> _t_ is the full state observation, **g** _t_ encodes environmental context, and **Y** _t_<sup>full</sup> is the dense future motion intent. 

The expert is trained using Proximal Policy Optimization (PPO) to maximize the expected discounted return across domain-randomized episodes: 


where _J_ ( _π_<sup>_⋆_</sup> ) is the expert policy objective function, _π_<sup>_⋆_</sup> denotes the expert policy, _τ_ = _{_ ( **s** _t,_ **_α_**<sup>(1)</sup> _t_<sup>)</sup><sup>_}T_</sup> _t_ =0<sup>is a trajectory</sup> generated by the expert policy under the latent dynamics **_ψ_**<sup>(</sup><sup>_e_)</sup> , and _r_ ( _·_ ) is a reward function that penalizes deviations from desired motion, loss of balance, excessive control effort, and falls. By training over a diverse distribution of 

**Stage II: Sparse-Observation Student.** The second stage distills the expert’s behavior into a student policy _πθ_ 2 that operates under realistic sensory constraints. The student receives sparse observations **s**<sup>sparse</sup> _t ⊂_ **s**<sup>full</sup> _t_ and sparse future motion cues **Y** _t_<sup>sparse</sup> , but uses the same temporal memory embedding **m** _t_ (obtained from _Ht_ as mentioned above) and the proposed SSJR representation (see §3.3) to leverage historical interactions and standardized motion commands. 

The student outputs the control modulation 


where **_α_**<sup>(2)</sup> _t_ is the student policy output, _fθ_ 2 is the student policy network parameterized by _θ_ 2, **s**<sup>sparse</sup> _t_ is the sparse state observation, and **Y** _t_<sup>sparse</sup> is the sparse future motion intent. The student is trained via supervised distillation to match the expert: 


where _L_ distill is the distillation loss, and _ℓ_ ( _·_ ) is the mean squared error (MSE). 

By sharing the temporal memory representation **m** _t_ and the SSJR motion interface across both stages, the student learns to recover the expert’s anticipatory behavior using only its own historical interactions and partial observations, resulting in a robust and domain-agnostic policy that enables reliable control across a wide range of physical and environmental conditions. 

### **3.3. SSJR: Standardized Sparse-Joint Representation** 

To decouple high-level motion specification from low-level torque control for humanoid robots, we introduce a standardized sparse-joint representation (SSJR). SSJR enables leveraging large-scale human motion data to train robot controllers without requiring platform-specific robots torque demonstrations, thereby improving scalability and crossplatform generalization. 

**Motion Abstraction.** SSJR represents future motion intentions **Y** _t_ using a sparse set of key joints _J_ defined in a canonical human skeletal model (e.g., SMPL-X). The motion commands over a short-horizon lookahead _H_ are expressed as: 


where **q**<sup>cmd</sup> denotes the relative joint configurations. By projecting human motion data from large-scale motion capture 

4 

**HoRD: Robust Humanoid Control via History-Conditioned Reinforcement Learning and Online Distillation** 

datasets (e.g., AMASS) onto this canonical sparse-joint representation, SSJR abstracts away platform-specific details while preserving task-relevant motion information. 

**Policy Integration.** At execution, the student policy _πθ_ 2 receives the SSJR commands **Y** _t_ along with robot proprioception and environmental context, and outputs torque modulation signals **_α_** _t_ . By standardizing the input across human datasets and humanoid platforms, SSJR ensures that the learned policy generalizes robustly to diverse robots and environmental conditions. 

SSJR offers several advantages. _Data scalability_ : The sparse-joint representation allows the use of widely available human motion datasets without costly torque supervision. _Cross-platform transfer_ : By abstracting away robot-specific actuation details, SSJR supports generalization across heterogeneous humanoid morphologies. _Anticipatory control_ : Coupled with temporal memory (HCDR, _cf_ . §3.5) and domain randomization, SSJR enables the policy to interpret future motion intentions and adapt its torque commands accordingly. 

### **3.4. Episode-Level Domain Randomization** 

To promote robust cross-domain generalization and prevent overfitting to simulator-specific artifacts, we adopt an _Episode-Level Domain Randomization_ strategy. Rather than applying uncorrelated noise at each timestep, we sample **_ψ_**<sup>(</sup><sup>_e_)</sup> (as defined in §3.1) at the start of each episode _e_ and hold it fixed for the duration of the episode. By maintaining temporally consistent dynamics shifts, the policy is encouraged to infer latent physical properties from its observations, rather than memorizing short-term fluctuations. 

The robot state evolves according to a family of parameterized transitions: 


where **s** _t_ is the state at time _t_ , **_α_** _t_ is a control modulation applied to the low-level actuators, and **_ω_** _t ∼N_ (0 _,_ Σ _ω_ ) captures unmodeled disturbances. 

We randomize **_ψ_**<sup>(</sup><sup>_e_)</sup> along four key dimensions: (1) inertial properties, including link masses, center-of-mass locations, and joint damping coefficients; (2) contact dynamics, such as ground friction coefficients _µ_ and contact stiffness; (3) probabilistic system latency delays _δ ∈{_ 1 _,_ 2 _}_ in executing control commands to emulate communication and actuator delays; and (4) periodic random external forces applied to the robot’s torso to simulate environmental disturbances and contact irregularities. 

By sampling coherent parameter vectors per episode, the agent experiences dynamics that are both diverse and temporally consistent. This exposes the policy to distributional 

shifts similar to those encountered when transferring between different physics engines (e.g., IsaacLab vs. Genesis) or during real-world deployment, enabling robust and adaptive control under previously unseen conditions. 

### **3.5. HCDR: History-Conditioned Dynamics Representation** 

To adapt to latent environment parameters **_ψ_**<sup>(</sup><sup>_e_)</sup> (defined in §3.1) in real-time, we introduce HCDR, a latent representation module that performs online dynamics inference from historical interactions. 

**Latent Dynamics Inference.** HCDR models historical interactions as evidence for latent dynamics using a QueryTransformer (Q-Former) architecture, rather than flattening them into a simple vector. We define a set of learnable latent tokens **m** 0 _∈_ R<sup>_dm×N_</sup> that encode a shared prior over dynamics configurations encountered during training, where _dm_ is the embedding dimension and _N_ is the number of tokens. The temporal memory embedding **m** _t_ is computed via cross-attention between the prior tokens and the history _Ht_ (defined in §3.2): 

**m** _t_ = QFormer( **m** 0 _, Ht_ ) _,_ (8) where **m** _t ∈_ R<sup>_dm_</sup> is the temporal memory embedding at time _t_ . 

This mechanism allows the module to selectively extract history components that are most informative for identifying the current latent dynamics regime. 

**Adaptive Modulation.** The resulting embedding **m** _t_ acts as a compact _dynamics fingerprint_ , capturing unobserved physical properties such as surface friction, unexpected mass distribution, or actuator delays. By conditioning the control modulation **_α_** _t_ on **m** _t_ , the policy can adapt its behavior “in context”, adjusting gait, balance, and torque outputs based on how the environment responds to previous actions. In essence, HCDR enables online system identification and adaptive control without direct access to the latent parameters **_ψ_**<sup>(</sup><sup>_e_)</sup> . 

## **4. Experiments** 

We evaluate HoRD on large-scale AMASS-based benchmarks and a suite of robustness scenarios. We design a transformer-based architecture with a 6-layer encoder using 8 attention heads. The actor head uses a 4-layer MLP and outputs the mean actions. Detailed model structures and RL settings are discussed in appendix C and D. 

### **4.1. Experimental Setup** 

_Robot and environment._ All experiments are conducted on a Unitree-style G1 humanoid with 29 actuated DoF, con- 

5 

**HoRD: Robust Humanoid Control via History-Conditioned Reinforcement Learning and Online Distillation** 

_Table 1._ **Overall performance** of HoRD on the test set across 4 environments. Genesis results are evaluated in a zero-shot manner without collecting test-domain data for retraining. Best results are bold; second-best are underlined. 

||**Is**|**aacLab (I**|**D)**|**Isaa**|**cLab + D**|**R (ID)**|**G**|**enesis (O**|**OD)**|**Gene**|**sis + DR**|**(OOD)**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Method**|**Succ.**<br>(%)_↑_|**E**g-mpjpe<br>(mm)_↓_|**E**mpjpe<br>(mm)_↓_|**Succ.**<br>(%)_↑_|**E**g-mpjpe<br>(mm)_↓_|**E**mpjpe<br>(mm)_↓_|**Succ.**<br>(%)_↑_|**E**g-mpjpe<br>(mm)_↓_|**E**mpjpe<br>(mm)_↓_|**Succ.**<br>(%)_↑_|**E**g-mpjpe<br>(mm)_↓_|**E**mpjpe<br>(mm)_↓_|
|MaskedMimic|32.1|376|182|_<_10|713|283|_<_10|742|322|_<_10|738|326|
|OmniH2O|85.2|266|132|83.2|282|168|72.3|312|165|70.2|335|191|
|ExBody2|86.6|247|108|85.9|237|128|73.1|305|157|69.4|342|202|
|Hover|71.2|278|138|67.9|375|196|16.2|722|258|15.5|746|282|
|**HoRD (Ours)**|**90.7**|**102**|**76**|**88.4**|**124**|**87**|**86.0**|**162**|**96**|**84.4**|**171**|**108**|


trolled at the PD level at 50 Hz. Training is performed in Isaac Lab (Mittal et al., 2025) with contact-rich rigid-body dynamics, while evaluation additionally includes zero-shot transfer to the Genesis physics engine (Zhou et al., 2024). Episodes follow the duration of each target motion clip and terminate early if the tracking error diverges or the robot falls. Detailed environment and deployment specifications, together with the full reward formulation and stability constraints, are provided in Appendix B and Appendix C.1. 

_Motion dataset and commands._ We use the AMASS motion corpus (Mahmood et al., 2019), covering locomotion, balance, manipulation-style poses, and recovery motions. Motion clips are segmented, retargeted to the humanoid, and converted into sparse key-joint trajectories using the proposed SSJR representation. Details of motion retargeting, filtering, SSJR and teacher/student observation specifications and input dimensions, are provided in Appendix A.6, B.1, and C.4. 

_Baselines._ We compare HoRD against strong physicsbased and masked-imitation baselines, including MaskedMimic (Tessler et al., 2024), OmniH2O (He et al., 2025b), ExBody2 (Ji et al., 2024), and Hover (He et al., 2025c). All methods are trained under the same environment configuration. Detailed baseline configurations and implementation notes are provided in Appendix A.5. 

_Evaluation metrics._ In evaluation, we report: (1) _success rate_ (Succ. ), defined as the percentage of episodes that complete without falling, (2) global pose error **E** g-mpjpe, and (3) local pose error **E** mpjpe. All results are averaged across multiple random seeds. Full experimental details, including environment configuration, metric definitions, and PPO training hyperparameters, in Appendix B and Appendix Table 7. 

### **4.2. In-Domain Performance** 

Table 1 reports the test performance of HoRD and representative baselines on a test set of around 800 motions from AMASS. All methods are trained in IsaacLab using identical training data, while evaluation is conducted under four 

settings: IsaacLab and Genesis, each with and without additional domain randomization (DR). Genesis represents an unseen physics engine, and no test-domain data are collected for retraining (zero-shot). 

Across all environments (w/o and w DR) and metrics, HoRD consistently achieves the best performance. In the in-domain environment (IsaacLab), HoRD attains a 90 _._ 7% success rate with substantially lower motion tracking errors, reducing **E** g-mpjpe and **E** mpjpe by more than 2 _×_ compared to strong physics-based baselines. This advantage persists under IsaacLab with DR, indicating that HoRD maintains stable execution even when additional observation noise and perturbations are introduced at test time. 

In contrast, MaskedMimic performs poorly even in the seen environment, achieving only 32 _._ 1% success and failing almost entirely ( _<_ 10%) under domain randomization. This behavior is consistent with its design focus on animationquality motion synthesis rather than torque-level execution on a complex humanoid platform such as Unitree G1. While other baselines achieve reasonable performance in the training environment, their success rates and tracking accuracy degrade notably once domain shifts are introduced. 

### **4.3. Cross-Domain Generalization** 

We further examine cross-domain generalization (w/o and w DR) by evaluating all methods in Genesis (Table 1 right), an unseen environment with different contact dynamics and numerical properties. (Detailed domain-shift factors are provided in Appendix 3.4). This setting tests whether a controller can generalize beyond the simulator used during training. As shown in Table 1, most baselines experience substantial performance degradation when transferred from IsaacLab to Genesis, even without additional domain randomization. Specifically, OmniH2O, ExBody2, and Hover suffer large drops in success rate and tracking accuracy, suggesting limited sim-to-sim robustness. MaskedMimic fails entirely in Genesis, reflecting its inability for sim-to-sim transfer. 

In contrast, HoRD exhibits strong zero-shot transfer to Gen- 

6 

**HoRD: Robust Humanoid Control via History-Conditioned Reinforcement Learning and Online Distillation** 


_Figure 2._ Results of HoRD on six representative motions, while red markers indicate ground-truth skeleton joints. Qualitative comparison results with baselines are shown in Appendix Fig. 5. With DR and HCDR, the robot is able to mimic a range of different human actions. 


_Figure 3._ Pose estimation errors comparing HoRD and ExBody2 across six representative motions. 

cases, HoRD produces temporally stable, human-like trajectories while maintaining balance and task completion. In particular, challenging motions such as high kick, which involve rapid center-of-mass shifts and intermittent ground contact, remain stable without collapse. 

Figure 3 reports pose errors comparing HoRD with the baselines. HoRD achieves lower errors on most motions in both **E** g-mpjpe and **E** mpjpe, with the clearest improvements on common walk, side walk, and martial. These cases emphasize sustained tracking under long-horizon coordination and asymmetric contacts, where small deviations can accumulate over time. Overall, the per-motion breakdown suggests that HoRD’s advantage is most pronounced on motions that require consistent whole-body coordination over longer horizons. 

esis, achieving an 86 _._ 0% success rate without retraining. When additional domain randomization is applied at test time, HoRD retains high performance (84 _._ 4% success), while all baselines collapse to near-failure regimes. We attribute this robustness to two factors. First, HoRD is trained under extensive domain randomization that covers a broad range of physical parameters. Second, the student policy additionally receives mild observation noise during training, encouraging adaptation to imperfect and shifted sensing conditions. Together with HCDR, which conditions control on recent state-action histories, HoRD is able to infer latent dynamics discrepancies online and adjust its execution accordingly. 

### **4.4. Representative Motion Case Studies** 

To better understand how HoRD behaves across diverse motion patterns beyond aggregate metrics, we conduct a motion-level analysis on six representative motions: common walk, side walk, get-up, punch, high kick, and martial. These motions vary substantially in contact patterns, balance requirements, and action aggressiveness. Figure 2 visualizes representative rollouts of HoRD on these motions in the unseen Genesis environment. Across all 

### **4.5. Ablation Studies** 

Ablation studies (Table 2) reveal complementary roles for domain randomization and HCDR. Removing domain randomization (HoRD w/o D) causes severe performance collapse under test-time perturbations or simulator changes, confirming its necessity for robust generalization beyond the training distribution. 

Removing HCDR (HoRD w/o H) maintains competitive performance on the training distribution but degrades sharply under distribution shift, with near-zero success in Genesis, highlighting its role as a learned dynamics adaptation mechanism that enables online adaptation to latent changes in simulator parameters and contact behavior. Further implementation details, diagnostic metrics, and training convergence analyses are provided in Appendix C.5, Appendix A.2, and Appendix C.7. 

### **4.6. Online Adaptation on Different Terrain Surface** 

We evaluate terrain robustness in the Genesis simulator under zero-shot transfer. We consider three terrain settings of increasing difficulty: flat ground, smooth slope, and rough slope. We visualize terrain rollouts in Appendix A.4. 

7 

**HoRD: Robust Humanoid Control via History-Conditioned Reinforcement Learning and Online Distillation** 

_Table 2._ Ablation study of HoRD across different environments. We analyze the contribution of domain randomization (D) and the HCDR module (H). Note that without SSJR (w/o S), there will be no conversion from motion to torque, and the **Succ.** will be _<_ 10 for all cases. 

||**Is**|**aacLab (**|**ID)**|**Isaac**|**Lab + DR**|**(ID)**|**G**|**enesis (OO**|**D)**|**Gene**|**sis + DR**|**(OOD)**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Method**|**Succ.**|**E**g-mpjpe|**E**mpjpe|**Succ.**|**E**g-mpjpe|**E**mpjpe|**Succ.**|**E**g-mpjpe|**E**mpjpe|**Succ.**|**E**g-mpjpe|**E**mpjpe|
||(%)_↑_|(mm)_↓_|(mm)_↓_|(%)_↑_|(mm)_↓_|(mm)_↓_|(%)_↑_|(mm)_↓_|(mm)_↓_|(%)_↑_|(mm)_↓_|(mm)_↓_|
|HoRD|90.7|102|76|88.4|124|87|86.0|162|96|84.4|171|108|
|HoRD w/o D|79.8|186|136|_<_10|832|286|_<_10|838|316|_<_10|838|287|
|HoRD w/o H|91.3|137|97|70.5|341|182|_<_10|846|324|_<_10|433|234|


_Table 3._ Online adaptation performance on different terrain surfaces. 

|**Terrain Method**|**Succ.** (%)_↑_|**E**g-mpjpe (mm)_↓_|**E**mpjpe(mm)_↓_|
|---|---|---|---|
|Flat ground|86.2|167|102|
|Smooth slope|85.8|171|106|
|Rough slope|84.2|180|112|


As shown in Table 3, HoRD maintains strong performance across all terrain conditions. On flat terrain, HoRD achieves an 86 _._ 2% success rate with low tracking error. As terrain difficulty increases, performance degrades gracefully, specifically, 85 _._ 8% on smooth slopes and 84 _._ 2% on rough slopes, closely matching its performance on flat terrian setting. 

Qualitative results (Appendix Fig. 6) further illustrate this trend. HoRD produces stable and continuous motions across all terrains, adapting foot placement and body posture to compensate for incline, whereas baselines frequently lose balance or exhibit oscillatory behavior. These results demonstrate that HoRD generalizes beyond flat-ground assumptions and provides robustness control under terrain-induced dynamics variations. 

### **4.7. Disturbance Recovery** 

To further evaluate robustness under unexpected physical disturbances, we test HoRD in the same zero-shot Genesis environment above, while injecting random external pushes during execution. These disturbances are applied intermittently at random time intervals, perturbing the humanoid’s root velocity in the world frame and simulating sudden external forces such as collisions or human interference. 

Figure 4 shows a representative recovery sequence, where a push is applied during walking motion execution. Despite the abrupt disturbance, HoRD quickly absorbs the impact, re-stabilizes the body, and resumes the intended motion without falling or task failure. This behavior is consistently observed across evaluation rollouts. HoRD recovers successfully in 85.2% of disturbed executions, outperforming strong baselines such as OmniH2O (71.8%) and ExBody2 (72.1%). These results show the robustness of HoRD under disturbance and indicate that HoRD performs closed-loop execution rather than open-loop motion replay. 


_Figure 4._ Online adaptation experiment shows that a lateral push is applied mid-execution (second frame), perturbing the humanoid’s motion. HoRD rapidly re-stabilizes and resumes the intended trajectory (red markers). 

## **5. Discussion and Future Works** 

**Data and behavior coverage.** Our experiments are based on AMASS-derived motions. Because the humanoid differs from humans in mass distribution and torque limits, some clips are effectively infeasible and, despite basic filtering, can introduce gradient interference with more plausible motions. Object-centric behaviors that rely on environmental props (e.g., chairs, external supports) are also largely outside our current scope. More careful feasibility-aware curation and extending HoRD to richer scenes with explicit object interactions are natural next steps. 

**Learning efficiency and optimization cost.** The expert policy is learned via on-policy RL in a broad domainrandomized setting, which remains computationally expensive and sensitive to reward design, observation noise, and randomization ranges. Learning policies that cover a wide dynamics distribution on AMASS-scale data requires days of training on a single high-end GPU, and overly aggressive randomization can create competing gradients across motions. Future work will explore more sample-efficient learning schemes and automated calibration of domain randomization to better balance performance on the training distribution and cross-domain generalization. 

**Long-horizon recovery and goal-aware control.** HoRD demonstrates strong robustness to perturbations and emergent fall-recovery behaviors, but its learned policy remains conditioned primarily on short-horizon sparse inputs. A natural extension is to explore lightweight goal or waypointconditioned variants. Such extensions can be incorporated into SSJR and learned within the HoRD framework, providing a principled path toward richer recovery and higher-level whole-body behaviors. 

8 

**HoRD: Robust Humanoid Control via History-Conditioned Reinforcement Learning and Online Distillation** 

## **6. Conclusion** 

We introduced HoRD, a framework mapping sparse motion commands to robust torque-level humanoid control. By combining standardized sparse-joint representation with history-conditioned dynamics adaptation, HoRD learns stable whole-body behaviors that generalize across substantial dynamics variation. HoRD significantly outperforms baselines in tracking fidelity, stability, and zero-shot transfer via data-efficient distillation from a domain-randomized expert. HoRD shows that lightweight learned policies with standardized representations can bridge high-level planners and deployment-ready control. 

## **Impact Statement** 

This work improves robustness in torque-level humanoid control by introducing a learning framework that (i) decouples high-level motion intent from low-level actuation via standardized representations, (ii) operates from sparse motion commands that can be produced from diverse sources such as vision–language-action models, video, or wearables, and (iii) generalizes under distribution shifts in physical dynamics or simulators through online adaptation from recent state–action history. Such capability may benefit embodied AI research and, in the longer term, assistive and service robotics by reducing the engineering and compute overhead of re-training or re-tuning controllers across robots and deployment conditions, while the released large-scale trajectory dataset and evaluation scripts support reproducible benchmarking. 

However, more capable and transferable humanoid control policies raise safety considerations if deployed without sufficient verification. In particular, real-world dynamics changes that are not directly observed (e.g., mass distribution, friction, actuator delay) can cause small model mismatches to compound into large tracking errors and destabilize torque control over long horizons. We therefore emphasize responsible deployment: systems built on this technique should undergo extensive validation beyond simulation, incorporate safety constraints and fail-safes (e.g., action limiting, emergency stops, and monitoring), and maintain clear usage boundaries with human oversight on physical platforms. Robustness may also vary across embodiments, sensing configurations, and operating conditions; future work should audit reliability across diverse settings and strengthen evaluation protocols for sim-to-real transfer and safety. 

- Brohan, A., Chebotar, Y., Finn, C., and et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. _arXiv preprint arXiv:2307.15818_ , 2023. 

- Campanaro, L., Gangapurwala, S., Merkt, W., and Havoutis, I. Learning and deploying robust locomotion policies with minimal dynamics randomization. In _6th Annual Learning for Dynamics & Control Conference_ , pp. 578– 590. PMLR, 2024. 

- Chebotar, Y., Handa, A., Makoviychuk, V., Macklin, M., Issac, J., Ratliff, N., and Fox, D. Closing the sim-toreal loop: Adapting simulation randomization with real world experience. In _2019 International Conference on Robotics and Automation (ICRA)_ , pp. 8973–8979. IEEE, 2019. 

- Cobbe, K., Klimov, O., Hesse, C., Kim, T., and Schulman, J. Quantifying generalization in reinforcement learning. In _International conference on machine learning_ , pp. 1282– 1289. PMLR, 2019. 

- Cobbe, K., Hesse, C., Hilton, J., and Schulman, J. Leveraging procedural generation to benchmark reinforcement learning. In _International conference on machine learning_ , pp. 2048–2056. PMLR, 2020. 

- Driess, D., Xia, F., Sajjadi, M. S., and et al. Palm-e: An embodied multimodal language model. _arXiv preprint arXiv:2303.03378_ , 2023. 

- Fedus, W., Zoph, B., and Shazeer, N. Switch transformers: Scaling to trillion parameter models with simple and efficient sparsity. _Journal of Machine Learning Research_ , 23(120):1–39, 2022. 

- Ghosh, D., Bhateja, C. A., and Levine, S. Reinforcement learning from passive data via latent intentions. In _International Conference on Machine Learning_ , pp. 11321– 11339. PMLR, 2023. 

- Hallak, A., Di Castro, D., and Mannor, S. Contextual markov decision processes. _arXiv preprint arXiv:1502.02259_ , 2015. 

- He, T., Gao, J., Xiao, W., Zhang, Y., Wang, Z., Wang, J., Luo, Z., He, G., Sobanbab, N., Pan, C., et al. Asap: Aligning simulation and real-world physics for learning agile humanoid whole-body skills. _arXiv preprint arXiv:2502.01143_ , 2025a. 

## **References** 

- Ahn, M., Brohan, A., Chebotar, Y., and et al. Do as i can, not as i say: Grounding language in robotic affordances. In _Conference on Robot Learning (CoRL)_ , 2022. 

- He, T., Luo, Z., He, X., Xiao, W., Zhang, C., Zhang, W., Kitani, K. M., Liu, C., and Shi, G. Omnih2o: Universal and dexterous human-to-humanoid whole-body teleoperation and learning. In _Conference on Robot Learning_ , pp. 1516–1540. PMLR, 2025b. 

9 

**HoRD: Robust Humanoid Control via History-Conditioned Reinforcement Learning and Online Distillation** 

- He, T., Xiao, W., Lin, T., Luo, Z., Xu, Z., Jiang, Z., Kautz, J., Liu, C., Shi, G., Wang, X., et al. Hover: Versatile neural whole-body controller for humanoid robots. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 9989–9996. IEEE, 2025c. 

- Janner, M., Du, Y., Tenenbaum, J., and Levine, S. Planning with diffusion for flexible behavior synthesis. In _International Conference on Machine Learning_ , pp. 9902–9915. PMLR, 2022. 

- Ji, M., Peng, X., Liu, F., Li, J., Yang, G., Cheng, X., and Wang, X. Exbody2: Advanced expressive humanoid whole-body control. _arXiv preprint arXiv:2412.13196_ , 2024. 

- Kim, M. J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E., Lam, G., Sanketi, P., et al. Openvla: An open-source vision-languageaction model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- Mahmood, N., Ghorbani, N., Troje, N. F., Pons-Moll, G., and Black, M. J. Amass: Archive of motion capture as surface shapes. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pp. 5442–5451, 2019. 

- Mittal, M., Roth, P., Tigue, J., Richard, A., Zhang, O., Du, P., Serrano-Munoz, A., Yao, X., Zurbr˜ ugg, R., Rudin, N.,¨ et al. Isaac lab: A gpu-accelerated simulation framework for multi-modal robot learning. _arXiv preprint arXiv:2511.04831_ , 2025. 

- Peng, X. B., Berseth, G., Yin, K., and Van De Panne, M. Deeploco: Dynamic locomotion skills using hierarchical deep reinforcement learning. _Acm transactions on graphics (tog)_ , 36(4):1–13, 2017. 

- Peng, X. B., Abbeel, P., Levine, S., and Van de Panne, M. Deepmimic: Example-guided deep reinforcement learning of physics-based character skills. _ACM Transactions On Graphics (TOG)_ , 37(4):1–14, 2018. 

- Peng, X. B., Ma, Z., Abbeel, P., Levine, S., and van de Panne, M. Amp: Adversarial motion priors for stylized physics-based character control. _ACM Transactions on Graphics (Proc. SIGGRAPH)_ , 40(4):85, 2021. 

networks: The sparsely-gated mixture-of-experts layer. _arXiv preprint arXiv:1701.06538_ , 2017. 

   - Tessler, C., Peng, X. B., Makadia, A., Kanazawa, A., Abbeel, P., and Levine, S. Maskedmimic: Unified physics-based character control through masked motion inpainting. _ACM Transactions on Graphics (Proc. SIGGRAPH Asia)_ , 43(6):245, 2024. 

   - Tobin, J., Fong, R., Ray, A., and et al. Domain randomization for transferring vision models from simulation to the real world. In _IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pp. 23–30, 2017. 

   - Wang, S., Wang, X., Zhang, C., Pang, S., Gui, H., Ji, W., and Liao, X. Soft conflict-resolution decision transformer for offline multi-task reinforcement learning. _arXiv preprint arXiv:2511.13133_ , 2025. 

   - Won, J., Gopinath, D., and Hodgins, J. A scalable approach to control diverse behaviors for physically simulated characters. _ACM Transactions on Graphics (TOG)_ , 39(4): 33–1, 2020. 

   - Yu, T., Kumar, S., Gupta, A., Levine, S., Hausman, K., and Finn, C. Gradient surgery for multi-task learning. _Advances in neural information processing systems_ , 33: 5824–5836, 2020. 

   - Zhang, Z., Shen, J., Cao, C., Dai, G., Zhou, S., Zhang, Q., Zhang, S., and Shutova, E. Proactive gradient conflict mitigation in multi-task learning: A sparse training perspective. _arXiv preprint arXiv:2411.18615_ , 2024. 

   - Zhao, Q., Lu, Y., Kim, M. J., Fu, Z., Zhang, Z., Wu, Y., Li, Z., Ma, Q., Han, S., Finn, C., et al. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 1702–1713, 2025. 

   - Zhou, X., Qiao, Y., Xu, Z., Wang, T., Chen, Z., Zheng, J., Xiong, Z., Wang, Y., Zhang, M., Ma, P., et al. Genesis: A generative and universal physics engine for robotics and beyond. _arXiv preprint arXiv:2401.01454_ , 2024. 

   - Zhou, Y. and et al. Mixture-of-experts with expert choice routing. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2022. 

- Schaul, T., Horgan, D., Gregor, K., and Silver, D. Universal value function approximators. In _International conference on machine learning_ , pp. 1312–1320. PMLR, 2015. 

- Sener, O. and Koltun, V. Multi-task learning as multiobjective optimization. _Advances in neural information processing systems_ , 31, 2018. 

- Shazeer, N., Mirhoseini, A., Maziarz, K., Davis, A., Le, Q., Hinton, G., and Dean, J. Outrageously large neural 

10 

**HoRD: Robust Humanoid Control via History-Conditioned Reinforcement Learning and Online Distillation** 

## **A. Additional Results** 

### **A.1. Qualitative Comparisons** 

Fig. 5 provides qualitative visualizations corresponding to the quantitative results (Figure 3) in the Section 4.4. Specifically, we visualize representative execution trajectories of HoRD together with the strongest competing baseline and the weakestperforming baseline identified, MaskedMimic and ExBody2. 


_Figure 5._ Qualitative comparisons across 6 different motions. 

11 

**HoRD: Robust Humanoid Control via History-Conditioned Reinforcement Learning and Online Distillation** 

The examples are intended to illustrate how differences in tracking errors reported by the quantitative metrics manifest in the resulting motion executions, and to provide additional visual context for the comparative results. In several cases, MaskedMimic exhibits early instability or tracking failure, while ExBody2 shows noticeable drift or delayed recovery. In contrast, HoRD maintains closer alignment with the reference motion throughout the execution. 

### **A.2. Test Set Evaluation Metrics** 

We present comprehensive evaluation metrics on the test set. These results are obtained from learned policies evaluated in IsaacLab with domain randomization (DR) settings on held-out test motions. Table 4 summarizes the performance comparison across different evaluation metrics for HoRD and its ablation variants. 

_Table 4._ Comprehensive evaluation metrics comparison across different methods on the test set. All policies are evaluated in IsaacLab with domain randomization. 

|**Metric**|**HoRD**|**HoRD w/o D**|**HoRD w/o M**|
|---|---|---|---|
|Cartesian Error_↓_|0.087|0.286|0.182|
|Global Rotation Error_↓_|0.369|1.594|1.011|
|Global Translation Error_↓_|0.124|0.832|0.341|
|DOF Velocity Reward_↑_|0.972|0.980|0.960|
|Key Body Reward_↑_|0.907|0.412|0.612|
|Local Rotation Reward_↑_|0.833|0.274|0.507|
|Root Angular Velocity Reward_↑_|0.480|0.722|0.412|
|Root Velocity Reward_↑_|0.954|0.878|0.904|


### **A.3. Discussion on Extra Baselines** 

We compare HoRD with existing methods across three deployment-relevant capabilities, as summarized in Table 5: unified skill coverage, sparse-command generalization, and explicit online dynamics adaptation. HoRD supports unified policy learning over heterogeneous skills while remaining robust when only sparse or partial keypoint-level commands are available. In addition, HoRD incorporates an explicit online dynamics adaptation mechanism through HCDR’s history-conditioned representation, enabling the policy to infer latent dynamics variations and adjust its strategy accordingly at test time. In contrast, prior approaches typically emphasize only a subset of these capabilities, for example focusing on unified motion priors or partial-constraint training without dedicated dynamics adaptation. 

### **A.4. Performance across different terrains** 


Figure 6 visualizes HoRD locomotion across three terrain types: flat ground, a smooth incline, and a rough incline. On flat ground, the robot maintains stable forward motion with a consistent posture. On the smooth slope, HoRD adapts its body pitch and foot placement to climb steadily without noticeable slipping. On the rough slope, it remains robust to uneven contacts, adjusting step timing and stance to preserve balance and traction while ascending. 

### **A.5. Baseline Training Details** 

To evaluate the effectiveness of our method, we compare it with four state-of-the-art (SOTA) methods: Maskedmimic, OmniH2O, Ex- _Figure 6._ Visualization of HoRD performance across Body2, and HOVER. For fair comparison, we either use the officially different terrains. released code or closely follow the official implementation when code is unavailable. We adapt each method to the Unitree G1 robot (instead of H1/H1-2). In addition, we keep the training dataset consistent with that used for HoRD. For HOVER, we use unmasked observations during the evaluation to ensure optimal performance. 

This section summarizes the training configurations of the baseline methods used for comparison. Whenever possible, we follow the training settings reported in the original papers or official implementations. For methods whose training pipelines 

12 

**HoRD: Robust Humanoid Control via History-Conditioned Reinforcement Learning and Online Distillation** 

_Table 5._ Comparison of representative humanoid control frameworks in terms of three deployment-relevant capabilities: (i) **Unified Skill Coverage** , indicating whether a single policy can cover diverse heterogeneous skills; (ii) **Sparse-Command Generalization** , reflecting robustness when only sparse or partial keypoint-level commands are available; and (iii) **Explicit Online Dynamics Adaptation** , denoting the presence of a dedicated mechanism for adapting to dynamics variations at test time. 

|Method|Unified Skill Coverage|Sparse-Command Generalization|Explicit Online Dynamics Adaptation|
|---|---|---|---|
|BumbleBee|_×_|_×_|_×_|
|HOVER|_×_|✓|_×_|
|MaskedMimic|✓|✓|_×_|
|ASAP|_×_|_×_|_×_|
|PHC|_×_|_×_|_×_|
|PULSE|_×_|_×_|_×_|
|ExBody2|_×_|_×_|_×_|
|OmniH2O|✓|_×_|_×_|
|HoRD (ours)|✓|✓|✓|


**Notation:** ✓ supported; _×_ not supported. 

are not fully specified or publicly available, we adopt reasonable approximations consistent with prior work and document the key differences explicitly. 

All baselines are evaluated under the same test environments and metrics as our method. 

### **A.6. SSJR Example** 

For reproducibility, we provide a minimal SSJR packet example. It specifies the sequence frame rate (30 fps), duration (10.0 s), number of frames (300), and number of joints (33). The packet stores time-indexed motion fields with fixed tensor dimensions, including global translation [300 _,_ 33 _,_ 3], global rotation matrices [300 _,_ 33 _,_ 3 _,_ 3], global rotations in quaternion form [300 _,_ 33 _,_ 4], global linear and angular velocities [300 _,_ 33 _,_ 3], local joint rotations [300 _,_ 29 _,_ 4], root linear and angular velocities [300 _,_ 3], and joint DoF positions and velocities [300 _,_ 29]. Finally, it optionally includes text tokens (e.g., a brief natural-language description of the motion) to support downstream conditioning. 

## **B. Environment Details** 

### **B.1. RL Settings** 

We provide a detailed training and test environment setting in this subsection. 

**Observation.** For privileged observation (teacher policy), we use proprioception including linear velocity, angular velocity, joint position, joint velocity, and last action, as well as task-relevant observation including target joint positions, target keypoint positions, target root translations, and target root rotations in global coordinates. 

Temporal context is provided by stacking observations over multiple timesteps. The teacher policy consumes observations from the past 5 timesteps, while the student policy uses a longer horizon of 10 timesteps (8-step history with 2-step lookahead). The resulting proprioceptive observation dimension is 493, and target poses include an 8-step future with 18 dimensions per joint. 

**Action and actuation model.** We operate a torque-actuated simulator of the Unitree G1 humanoid with 29 actuated degrees of freedom (DoFs). The policy outputs desired joint configurations **_α_** _t_ , which are converted into joint torques through a proportional–derivative (PD) controller and applied in simulation. Concretely, the applied torque at time _t_ is given by 


where **_α_** _t_ denotes the target joint positions predicted by the policy, and **q** _t_ , **q** ˙ _t_ are the current joint positions and velocities. Stiffness and damping gains are specified per joint group, with stiffness values of 100 for hips, 200 for knees, 400 for the waist, and 60–90 for shoulders, and damping coefficients ranging from 0.1 to 5.0. 

13 

**HoRD: Robust Humanoid Control via History-Conditioned Reinforcement Learning and Online Distillation** 

**Termination.** Each episode follows the duration of a target motion clip. An episode terminates early if the global tracking error exceeds a threshold of 0 _._ 5 m, indicating irreversible divergence. 

### **B.2. Deployment** 

The policy runs at 50 Hz, while the simulator operates at 200 Hz with a decimation factor of 4, corresponding to four simulation steps per control action. Policy inference and actuation are integrated through standard simulation interfaces in IsaacLab. 

### **B.3. Metrics** 

We evaluate learned policies using task-level success, trajectory tracking errors, and several reward-aligned kinematic terms. Unless otherwise stated, expectations are taken over time and over evaluation episodes. 

**Strict tracking success.** Our primary metric is the strict success rate. For an episode _i_ , let GTE<sup>(</sup> _t_<sup>_i_)</sup> denote the global translation error at time _t_ (defined below). The episode is counted as successful if the per-frame error never exceeds the threshold _ε_ GTE=0 _._ 5 m, 


and the strict success rate over _N_ episodes is 


**Cartesian position error (cartesian** **~~e~~ rr, MPJPE).** To measure local trajectory fidelity, we compute the mean per-joint position error (MPJPE) in the local frame, after subtracting the initial root translation: 


where _p_ ˆ _t_ and _p_ ˆ<sup>ref</sup> _t_<sup>are local-frame joint positions for the executed and reference motions, respectively.</sup> 

**Global translation error (gt** **~~e~~ rr, Global MPJPE).** Global alignment is quantified by the RMS error between reference and executed joint positions in world coordinates: 


and we write GTE _t_ = _∥p_<sup>ref</sup> _t_<sup>_−pt∥_2for the instantaneous error used in the strict success criterion.</sup> 

**Global rotation error (gr** **~~e~~ rr).** We also report the RMS angular error between reference and executed global orientations: 


where ∆ _q_ ( _·, ·_ ) denotes the angular distance between two unit quaternions. 

**Reward-aligned kinematic terms.** For completeness, we additionally report several exponentiated tracking rewards that HCDR components of the teacher’s RL objective, which are not used as primary evaluation metrics, including DoF velocity tracking, key-body Cartesian tracking, local joint rotation consistency, root linear velocity tracking, and root angular velocity tracking: 

14 

**HoRD: Robust Humanoid Control via History-Conditioned Reinforcement Learning and Online Distillation** 

_Table 6._ Domain randomization ranges used for both training and evaluation. 


Here _q_ ˙ _t_ denotes joint velocities, _bt_ key-body points (e.g., hands, feet, head), _lrt_ local joint rotations, and _vt_<sup>root</sup> , _ωt_<sup>root</sup> the root linear and angular velocities; _c_ dv _, c_ kb _, c_ lr _, c_ rv _, c_ rav are positive scaling constants shared across methods. 

**Legacy aggregate metrics.** For comparability to prior work, some tables additionally report legacy aggregate metrics used in MaskedMimic, namely trajectory error _E_ traj and torque smoothness _Sτ_ . 

## **C. Training Details** 

### **C.1. Reward Design** 

The reward design for our tracking policy includes task rewards, penalties, and regularization terms. The main reward components are: 

- **Task rewards:** Global translation (GT) weight=0.5, Global rotation (GR) weight=0.4, Global velocity (GV) weight=0.1, Global angular velocity (GAV) weight=0.1, Root height (RH) weight=0.2 

- **Penalties:** Global rotation constraint (GR _c_ )=-10, Global translation constraint (GT _c_ )=-100, Root tracking constraint (RT _c_ )=-120, Root height constraint (RH _c_ )=-100 

- **Regularization:** Power penalty = 5 _×_ 10<sup>_−_6</sup> 

The reward function encourages accurate motion tracking while maintaining physical feasibility and smooth control. 

### **C.2. Domain Randomization** 

To encourage cross-domain generalization and zero-shot transfer, we apply structured domain randomization at the beginning of each episode. The detailed domain randomization setup is summarized in Table 6. 

This randomization envelope is shared across HoRD and all baselines to ensure fair comparison. 

### **C.3. RL Hyperparameters** 

The RL training follows standard PPO. We provide the detailed training hyperparameters in Table 7. 

### **C.4. Motion Dataset Processing** 

Following prior work, we first retarget SMPL-format human motion sequences from the AMASS dataset into robot-specific representations, including global translations and joint axis-angle rotations. Given that AMASS contains a wide range of 

15 

**HoRD: Robust Humanoid Control via History-Conditioned Reinforcement Learning and Online Distillation** 

_Table 7._ Key training hyperparameters. 

|**Category**|**Values**|
|---|---|
|**Training setup**|Env count: 4,096; Max steps: 1_×_10<sup>10</sup>; Seed: 0<br>Simulator FPS: 200; Decimation: 4; Mixed terrains (7 levels)|
|**Optimization**|PPO_γ_=0_._99,_τ_=0_._95, clip_ϵ_=0_._2<br>Actor LR=2_×_10<sup>_−_5</sup>, Critic LR=1_×_10<sup>_−_4</sup><br>Batch size=16,384, Mini epochs=1, Grad clip=50.0|
|**Model**|Transformer: 6 layers, 8 heads, dim=512, FF=1,024<br>Actor log std = -2.9; Dropout = 0; Activation = ReLU<br>Critic: 4-layer MLP (1,024 hidden units each)|
|**Observation encoding**|Self obs dim = 493; Hist steps = 8<br>Target poses: 8-step future, 18 dims per joint<br>Terrain encoding: 256-256 MLP with normalization|
|**Reward shaping**|Weights: GT=0.5, GR=0.4, GV=0.1, GAV=0.1, RH=0.2<br>Penalties: GR_c_=_−_10, GT_c_=_−_100, RT_c_=_−_120, RH_c_=_−_100<br>Power penalty =5_×_10<sup>_−_6</sup>|
|**Control and robot**|Actions: 29 DoFs, Proportional PD control<br>Stiffness: hips=100, knees=200, waist=400, shoulders=60–90<br>Damping: 0.1–5.0 depending on joint group|
|**Terrain**|Terrain types: [smooth slope, rough slope, stairs up, stairs down, discrete, stepping, poles, flat]<br>Terrain proportions: [0.25, 0.25, 0., 0., 0., 0., 0., 0.5]|


motions, such as crawling and climbing, we perform an additional data cleaning step to ensure quality. We adopt the data filtering procedures described in PHC and MaskedMimic to clean the dataset, and split the dataset following MaskedMimic’s data splitting protocol. 

Motion sequences are segmented into clips of 2–10 seconds and retargeted to the humanoid morphology. Clips are discarded if retargeting violates joint limits or induces more than 5% persistent contact penetration. All remaining clips are downsampled to 30 Hz and converted into sparse key-joint trajectories using the proposed SSJR interface. 

### **C.5. Training and Distillation** 

The expert policy is learned via PPO with dense motion tracking rewards under domain randomization. The student policy is distilled from the expert using online DAgger-style imitation learning, where expert actions are queried during rollouts. Both the teacher and student policies share the same lightweight Transformer encoder backbone with 6 layers, 8 attention heads, model dimension 512, and a 3 _×_ feed-forward expansion. HCDR is implemented as a lightweight Q-Former, in which a set of learnable queries attends to a short window of past ( _s, a_ ) pairs to learn a compact latent summary of interaction history (Sec. 3.5). This learned history token is appended to the policy input sequence. 

The teacher is a goal-conditioned PPO agent learned on dense reference motion under extensive dynamics randomization. The student is distilled from this expert using online DAgger-style imitation learning as described in Sec. 3.2. Expert learning uses large-scale parallel simulation with thousands of humanoids and the same terrain configuration (including slopes, stairs, and uneven surfaces), and runs for a total of 10<sup>9</sup> control steps. 

### **C.6. Training Resources** 

All methods are trained on the same set of tasks, under the same randomization scheme and environment-step budgets, and all consume SSJR-formatted commands. Unless otherwise stated, experiments are run on a single NVIDIA A100 80 GB GPU with 32 GB host RAM using PyTorch 2.3. We evaluate learned policies at 50 Hz on held-out motions and terrains from the test split. Success rates and error metrics are averaged over multiple seeds, and significance is assessed using paired _t_ -tests with _p<_ 0 _._ 01. 

### **C.7. Training Convergence Curves** 

16 

**HoRD: Robust Humanoid Control via History-Conditioned Reinforcement Learning and Online Distillation** 


_Figure 7._ Reward components comparison across different methods. Full HoRD consistently achieves best performance across all reward metrics, demonstrating robust training stability and effectiveness of our approach. 


We provide additional learning convergence curves for ablation variants to analyze optimization dynamics during training, as shown in Fig. 8 and Fig. 7. Policies are trained in IsaacLab with domain randomization (DR) for 1,000M simulation steps. Success rate and intermediate metrics are periodically computed on the training distribution every 500 epochs, corresponding to approximately 65.54M simulation steps per evaluation. These curves illustrate learning stability, convergence behavior, and optimization dynamics under domain randomization. 

## **D. Model Details** 

_Figure 8._ Training convergence curves for different ablation variants, evaluated periodically on the training distribution. 

Both the teacher and student policies adopt a Transformer-based architecture with a 6-layer gence curves for different encoder using 8 attention heads, a model dimension of 512, and a feed-forward dimension ablation variants, evaluated of 1,536 (i.e., a 3 _×_ expansion). The actor head outputs mean actions and uses a fixed log periodically on the training standard deviation of _−_ 2 _._ 9 with ReLU activation, while the critic is a 4-layer MLP with 1,024 distribution. hidden units per layer. The policy takes as input a sequence of observations (5 timesteps for the teacher and 10 timesteps for the student), which is processed by the Transformer encoder. HCDR is implemented as a lightweight Q-Former-style history encoder in which a small set of learnable queries attends to a short window of recent state–action pairs to produce a history token that is appended to the policy input sequence. 

17 

