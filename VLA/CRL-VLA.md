---
title: "CRL-VLA: Continual Vision-Language-Action Learning"
date: "2026-02-03"
authors: "Qixin Zeng; Shuo Zhang; Hongyin Zhang; Renjie Wang; Han Zhao; Libang Zhao"
url: https://arxiv.org/abs/2602.03445
pdf: https://arxiv.org/pdf/2602.03445
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.03445)** / [論文ページ](https://arxiv.org/abs/2602.03445)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**CRL-VLA: Continual Vision–Language–Action Learning** 

**Qixin Zeng**<sup>1</sup> **Shuo Zhang**<sup>2</sup> **Hongyin Zhang**<sup>2</sup> **Renjie Wang**<sup>2</sup> **Han Zhao**<sup>2</sup> **Libang Zhao**<sup>2</sup> **Runze Li**<sup>2</sup> **Donglin Wang**<sup>2</sup><sup>_†_</sup> **Chao Huang**<sup>1</sup><sup>_†_</sup> 

# **Abstract** 

Lifelong learning is critical for embodied agents in open-world environments, where reinforcement learning fine-tuning has emerged as an important paradigm to enable Vision-Language-Action (VLA) models to master dexterous manipulation through environmental interaction. Thus, Continual Reinforcement Learning (CRL) is a promising pathway for deploying VLA models in lifelong robotic scenarios, yet balancing stability (retaining old skills) and plasticity (learning new ones) remains a formidable challenge for existing methods. We introduce CRL-VLA, a framework for continual post-training of VLA models with rigorous theoretical bounds. We derive a unified performance bound linking the stabilityplasticity trade-off to goal-conditioned advantage magnitude, scaled by policy divergence. CRLVLA resolves this dilemma via asymmetric regulation: constraining advantage magnitudes on prior tasks while enabling controlled growth on new tasks. This is realized through a simple but effective dual-critic architecture with novel GoalConditioned Value Formulation (GCVF), where a frozen critic anchors semantic consistency and a trainable estimator drives adaptation. Experiments on the LIBERO benchmark demonstrate that CRL-VLA effectively harmonizes these conflicting objectives, outperforming baselines in both anti-forgetting and forward adaptation. 

# **1. Introduction** 

Reinforcement Learning (RL) post-training has become a central paradigm for aligning Vision–Language–Action (VLA) models with complex embodied reasoning and robotic manipulation tasks (Black et al., 2024; Kim et al., 

> *Equal contribution 1University of Southampton, UK 

> 2Westlake University, China. Correspondence to: Donglin Wang _<_ wangdonglin@westlake.edu.cn _>_ , Chao Huang _<_ Chao.Huang@soton.ac.uk _>_ . 

2025). By optimizing policies through interaction, RL posttraining enables adaptive, goal-directed behaviors beyond what supervised learning can provide. Sustaining such adaptability requires lifelong learning across non-stationary task streams. However, in large-scale settings, Continual Reinforcement Learning (CRL) aims to equip agents with the ability to acquire new skills over time without catastrophic forgetting (Sutton, 2019). This problem fundamentally requires balancing scalability, stability, and plasticity under non-stationary task distributions (Pan et al., 2025). Despite its importance, CRL for VLA models remains underexplored, particularly in robotic manipulation scenarios involving multi-modal observations and long-horizon dynamics (Xu & Zhu, 2018; Pan et al., 2025). 

Most existing CRL methods enforce stability via parameteror function-space regularization, but they face severe limitations when applied to modern VLA architectures. Experience replay (Rolnick et al., 2019; Abbes et al., 2025) reuses outdated transitions whose gradients often conflict with those of new tasks, inducing off-policy errors that destabilize continual learning. Second-order regularization methods (Kutalev & Lapina, 2021) are computationally prohibitive due to the scale and dimensionality of multi-modal Transformers (Kim et al., 2025; Li et al., 2024). Recent approaches favor lightweight constraints such as KL regularization (Shenfeld et al., 2025), but such transition-level constraints enforce only short-horizon behavioral similarity and fail to preserve long-term task performance (Korbak et al., 2022). Backbone-freezing strategies (Hancock et al., 2025) hinge on the fragile assumption that pretrained multimodal representations remain aligned with language goals; under task shifts, value learning drifts without explicit language conditioning, degrading adaptation and collapsing plasticity (Jiang et al., 2025b; Guo et al., 2025). 

In this work, we show that forgetting in continual VLA learning is fundamentally driven by the goal-conditioned advantage magnitude, which directly links policy divergence to performance degradation on prior tasks. This perspective reframes the stability–plasticity dilemma as an asymmetric regulation problem: _suppressing advantage magnitudes on previous tasks to ensure stability, while permitting controlled growth on new tasks to enable plasticity._ 

_Preprint. February 4, 2026._ 

1 

**CRL-VLA: Continual Vision–Language–Action Learning** 

Based on this insight, we propose **CRL-VLA** , a continual learning framework that disentangles stable value semantics from adaptive policy learning via a novel **GoalConditioned Value Formulation (GCVF)** . Our method employs a dual-critic architecture in which a frozen critic anchors long-horizon, language-conditioned value semantics, while a trainable critic estimator drives adaptation. Stability is further enforced by combining trajectory-level value consistency with transition-level KL regularization, while Monte Carlo (MC) estimation and standard RL objectives support efficient learning on new tasks without catastrophic forgetting. Our contributions are summarized as follows: 

- We propose **CRL-VLA** , a principled continual posttraining framework for VLA models that identifies the goal-conditioned advantage magnitude as the key quantity governing the stability–plasticity trade-off. 

- CRL-VLA operationalizes this insight via a dual-critic architecture with a novel goal-conditioned value formulation, enabling asymmetric regulation that preserves prior skills while efficiently adapting to new tasks. 

- Extensive experiments show that CRL-VLA consistently outperforms strong baselines on continual VLA benchmarks, achieving superior knowledge transfer and resistance to catastrophic forgetting. 

# **2. Related work** 

## **2.1. Reinforcement Learning for VLA Models** 

VLA models have gained interest as unified robotic manipulation policies, with recent work exploring online RL to address SFT limitations and improve generalization and long-horizon reasoning. SimpleVLA-RL (Li et al., 2025) builds upon OpenVLA-OFT and GRPO, showing that online RL substantially improves long-horizon planning under demonstration scarcity. RIPT-VLA (Tan et al., 2025) applies the REINFORCE leave-one-out estimator to QueST and OpenVLA-OFT architectures. ARFM (Zhang et al., 2025a) enhances VLA action models via adaptive offline RL, balancing signal and variance to improve generalization and robustness. RLinf-VLA (Zang et al., 2025) implements a novel hybrid fine-grained pipeline allocation mode scalling up VLA model training with diverse RL algorithms and benchmarks. Recent work introduces IRLVLA, a closed-loop RL framework for VLA autonomous driving that achieved award-winning performance in benchmarks (Jiang et al., 2025a) . In contrast, our work aims to investigate the knowledge transfer of VLA models and their ability to learn new tasks stably and continuously. 

## **2.2. Continual Reinforcement Learning** 

Continual reinforcement learning generally falls into three paradigms. Regularization-based methods constrain updates to important parameters using Fisher information (Aich, 2021) or path integrals (Zenke et al., 2017), or enforce behavioral consistency via KL divergence (Shenfeld et al., 2025). Replay-based strategies (Rolnick et al., 2019) mitigate forgetting by interleaving past experience, though recent benchmarks (Wolczyk et al., 2021) highlight their scalability limits in high-dimensional robotics. Architecturebased approaches (Xu & Zhu, 2018) prevent interference by expanding network capacity, a strategy often impractical for large-scale pretrained models. While limited works explore value preservation via distillation (Schwarz et al., 2018; Rusu et al., 2016), they typically neglect the value drift inherent in non-stationary, language-conditioned tasks. Unlike these approaches, our work focuses on the continuous learning process of VLA models for general visual language manipulation tasks. 

## **2.3. Continual learning in VLA model** 

To date, there are no studies on continual learning specifically for VLA models, but similar research methods exist. Recent work (Yadav et al., 2025) improves policy stability under task variations, providing useful insights for subsequent lifelong learning approaches, although it is evaluated in a non-continual setting. Recently, several works have extended these paradigms to the VLA domain. VLM2VLA (Hancock et al., 2025) treats actions as a special language tokens and employs LoRA to align pre-trained VLMs with low-level robot control. Stellar-VLA (Wu et al., 2025) introduces a skill-centric knowledge space to evolve task representations continually across diverse robot manipulation scenarios. DMPEL (Lei et al., 2025) proposes a dynamic mixture of progressive parameter-efficient experts to achieve lifelong learning without high storage overhead. ChatVLA (Zhou et al., 2025) addresses spurious forgetting by decoupling multi-modal understanding from high-frequency action execution. Unlike these work, we aim to investigate a continuous post-training framework for VLA models and explicitly model the stability-plasticity trade-off between new and old tasks. 

# **3. Preliminaries** 

We study continual post-training of VLA policies in a goal-conditioned reinforcement learning setting. Each task is formulated as a goal-conditioned MDP _M_ = _⟨S, A, G, P, r, γ⟩_ , where _s ∈S_ is the state, _g ∈G_ is a language instruction, and _a ∈A_ is a robotic control command. For a given policy _π_ and goal _g_ , we define the state-value function as _V_<sup>_π_</sup> ( _s, g_ ) = E _τ ∼π,g_ [<sup>�</sup><sup>_∞_</sup> _t_ =0<sup>_γtr_(</sup><sup>_st, at, g_)</sup><sup>_|s_0=</sup> _s_ ], which represents the expected cumulative return start- 

2 

**CRL-VLA: Continual Vision–Language–Action Learning** 

ing from state _s_ . The action-value function is defined as _Q_<sup>_π_</sup> ( _s, a, g_ ) = E[<sup>�</sup><sup>_∞_</sup> _t_ =0<sup>_γtr_(</sup><sup>_st, at, g_)</sup><sup>_|s_0=</sup><sup>_s, a_0=</sup><sup>_a_].The</sup> advantage function _A_<sup>_π_</sup> ( _s, a, g_ ) = _Q_<sup>_π_</sup> ( _s, a, g_ ) _− V_<sup>_π_</sup> ( _s, g_ ) measures how much better an action is compared to the average action at that state. 

The state occupancy measure _d_<sup>_π_</sup> _g_<sup>(</sup><sup>_s_)</sup> = (1 _−_ = _γ_ )E[<sup>�</sup><sup>_∞_</sup> _t_ =0<sup>_γt_</sup><sup>**1**(</sup><sup>_st_</sup> _s_ )] describes the distribution of states visited by policy _π_ when executing goal _g_ . Different policies induce different state visitation distributions, which is fundamental to understanding how policy updates affect task performance. The goal-conditioned policy is _π_ ( _a | s, g_ ), with expected return for goal _g_ given by _Jg_ ( _π_ ) = E _τ ∼π,g t_ =0<sup>_γtr_(</sup><sup>_st, at, g_)</sup> . �� _∞_ � Performance on old tasks under distribution _p_ old( _g_ ) = is _J_ old( _π_ ) E _g∼p_ old[ _Jg_ ( _π_ )]. New policy’s performance _π_<sup>_′_</sup> on new tasks under distribution _p_ new( _g_ ) is _J_ new( _π_<sup>_′_</sup> ) = E _g∼p_ new [ _Jg_ ( _π_<sup>_′_</sup> )]. 

A pretrained VLA policy _πθ_ 0 is adapted sequentially to a task stream _T_ = _{T_ 1 _, . . . , TK}_ . At stage _k_ , the agent interacts only with _Tk_ and updates to _πk_<sup>_θ_viaon-policy</sup> RL, without access to interaction data, rewards, or gradients from previous tasks _{Ti}i<k_ . For a trajectory _τ_ = ( _s_ 0 _, a_ 0 _, . . . , sT_ ) with goal _g_ , the MC return at time _t_ is _Gt_ =<sup>�</sup><sup>_T_</sup> _k_ = _t_<sup>_γk−tr_(</sup><sup>_sk, ak, g_)</sup><sup>_,_which provides an unbiased</sup> estimate of _V_<sup>_π_</sup> ( _st, g_ ) for critic training. We evaluate using a transfer matrix **R** _∈_ R<sup>_K×K_</sup> , where _Rk,i_ is the success rate on task _Ti_ after training through stage _k_ . The objective is to learn a sequence of policies that jointly satisfy three criteria: Plasticity through high performance on the current task, Stability through preserved performance on prior tasks, and Scalability through efficient learning without large buffers or capacity expansion. 

# **4. Methodology** 

In this section, we first characterize the stability–plasticity dilemma in continual VLA through the advantage magnitude and policy divergence, and then demonstrate that _M_ old and _M_ new can be controlled in a decoupled manner. Furthermore, we introduce a dual goal-conditioned critic for continual VLA and then present the corresponding objectives, regularization, and training recipe. 

## **4.1. The Stability–Plasticity Dilemma in Continual VLA** 

At stage _k_ of continual VLA post-training, we update the policy _π_<sup>_k_</sup> with two coupled criteria. **Plasticity** means the maximization of new-goal return _Jgk_ ( _π_<sup>_k_</sup> ; _Tk_ ), while **stability** is the bounded degradation of old-goal return under the 

same update. Therefore, we solve 


Here, each task _Tk_ in the sequence _T_ = _{T_ 1 _, . . . , TK}_ specifies a goal _gk_ , and the agent iteratively updates its policy _πk_<sup>_θ_</sup> via reinforcement learning under a bound _δ_ on degradation over prior tasks. However, directly measuring the return impact of policy divergence during task transition is intractable. We therefore seek a bridge that links policy divergence to return change. In continual reinforcement learning for VLA model, we introduce the advantage magnitude _Mg_ . 

**Definition 4.1.** For any policy _π_<sup>_κ_</sup> and goal _g_ , we define the _Advantage Magnitude_ , denoted as _Mg_ ( _π_<sup>_κ_</sup> ), as the maximum absolute advantage of the anchored policy _π_ (typically set as the previous policy _π_<sup>old</sup> ) evaluated over the state-action pairs visited by _π_<sup>_κ_</sup> : 


Here, _Mg_ ( _π_<sup>_κ_</sup> ) close to 0 indicates that the policy aligns closely with the anchored policy on the evaluated distribution. Based on Definition 4.1, we evaluate a post-update policy _π_<sup>new</sup> under the old-goal distribution _p_ old of old task and the new-goal distribution _p_ new of new task. We then define two metrics to quantify the stability-plasticity tradeoff. The **Stability Metric** _M_ old measures the maximum advantage of the old policy over its own state distribution, capturing performance retention on old tasks. The **Plasticity Metric** _M_ new measures the maximum advantage achievable on new tasks under the new policy: 


**A Unified Perspective on Stability and Plasticity.** Theorem 4.1 establishes a unified perspective on the stabilityplasticity trade-off in goal-conditioned continual learning. Both performance degradation on old tasks and performance improvement on new tasks are governed by the coupling mechanism of advantage magnitude and policy divergence measured by KL divergence. 

This unified bound suggests that controlling continual learning reduces to balancing these two coupled quantities on old and new tasks. We next discuss how _M_ old and _D_ old govern stability, and how _M_ new and _D_ new govern plasticity. **1)** Old-task stability. _M_ old characterizes the sensitivity of old-task returns to policy changes, while _D_ old quantifies the policy change magnitude under the old-task state distribution; the (1 _− γ_ )<sup>_−_2</sup> scaling factor amplifies this coupling in long-horizon settings. **2)** New-task plasticity. _M_ new 

3 

**CRL-VLA: Continual Vision–Language–Action Learning** 

reflects the policy improvement potential, while _D_ new measures the policy modification degree under the new-task state distribution. Plasticity requires large policy modifications ( _D_ new) combined with learning potential ( _M_ new); conversely, constraining _D_ new to preserve old-task performance limits achievable improvement on new tasks. 

However, the coupling challenge remains stability and plasticity are fundamentally coupled through policy divergence under different state distributions. Common continual learning methods impose global constraints on policy updates via trust-region or KL penalties, restricting policy changes across all state space regions (Kessler et al., 2022). Reducing _D_ old to tighten the old-task stability bound also reduces _D_ new, thereby limiting plasticity on new tasks. Therefore, an effective trade-off requires minimizing _M_ old while constraining policy divergence under both old-task and new-task distributions with controllable _M_ new. 

## **Theoretical Result** 

**Theorem 4.1** (Unified Stability-Plasticity Bounds) **.** _Let π_<sup>new</sup> _and π_<sup>old</sup> _be the new and old policies. J_ old( _π_ ) _and J_ new( _π_ ) _denote the expected returns of policy π on the old and new tasks, respectively. The policy divergence parameters D_ old _and D_ new _directly use the expected KL divergence:_ 


_Proof._ Using Performance Difference Lemma (Kakade & Langford, 2002) and discounted occupancy bounds (Achiam et al., 2017), we derive performance difference bounds between old and new policies under goal-conditioned task transitions. Full derivations are in Appendix A.2. 

_Remark_ 4.1 _._ An effective stability-plasticity trade-off requires minimizing _M_ old while constraining _D_ old and _D_ new with controllable _M_ new. 

## **4.2. Decouple control for Stability and Plasticity Metrics** 

The central question becomes: can we control stability metrics _M_ old and plasticity metrics _M_ new separately? The answer depends on understanding the fundamental differences 

between these two quantities. Corollaries 4.1-4.2 reveal theses two metrics are bounded by independent factors with concrete derivations in Appendix A.4. _M_ old is constrained by critic approximation error _εV_ on _D_ old, while _M_ new is limited by environment return range [ _G_ min _, G_ max]. Since _εV_ operates on replay data and environment return range is task-intrinsic, a single constraint cannot regulate both. This necessitates dual mechanisms: minimizing _εV_ via constrained updates on _D_ old controls _M_ old, while MC-based estimation on new tasks exploits natural boundedness to control _M_ new. The orthogonality of these mechanisms enables simultaneous stability and plasticity without trade-offs: we control _M_ old by minimizing _εV_ on old task data, while _M_ new remains naturally bounded by the environment’s return range during new task learning. 

## **Corollary [V-only Path Bound]** 

**Corollary 4.1** (Controllability of Stability) **.** _Let Vθ denote the parameterized approximation and V_ old _the true anchor value. Under bounded rewards |r_ ( _s, a, g_ old) _| ≤ R_ max _and error εV_ ≜ sup _s,g_ old _|Vθ − V_ old _|, the advantage magnitude on old tasks satisfies: M_ old _≤ R_ max + (1 + _γ_ ) _εV_ + (1 + _γ_ ) _∥V_ old _∥∞._ 

_Remark_ 4.2 _._ The bound reveals that _M_ old can be directly controlled by constraining the value approximation error _εV_ on old tasks. 

## **Corollary [V-only Path Bound]** 

**Corollary 4.2** (Natural Boundedness of Plasticity) **.** _Let G_<sup>_g_</sup> _t_<sup>_betheground-truthMCreturnforgoalg,_</sup> _with G_<sup>_g_</sup> _t_<sup>_∈_[</sup><sup>_G_min</sup><sup>_, G_max]</sup><sup>_,atanytimet.Then,for_</sup> _the V-only advantage estimator A_<sup>ˆ</sup> _g_ new ( _s, a_ ) _, the advantage magnitude M_ new _satisfies: M_ new _≤_ 2(1 + _γ_ ) max _{|G_ min _|, |G_ max _|}._ 

_Remark_ 4.3 _._ The bound reveals that _M_ new can be directly controlled by bounding by reward of MC estimator. 

## **4.3. Dual Goal-Conditioned Critic for continual VLA** 

Given that _D_ old and _D_ new in Theorem 4.1 are realized via KL divergence, we develop value functions that make advantage magnitudes _Mg_ controllable, serving as a surrogate for direct advantage-based optimization. Furthermore, we enhance language-following capacity by conditioning the value network directly on language embeddings. Inspired by Corollaries 4.1 and 4.2, we propose a simple yet effective dual-critic framework. 

## **Infeasibility of Direct Advantage Optimization in VLA** 

Obtaining accurate advantage estimates in VLA settings 

4 

**CRL-VLA: Continual Vision–Language–Action Learning** 


_Figure 1._ The proposed CRL-VLA method. CRL-VLA is a continuous learning framework for VLA models that treats the goal-conditioned advantage magnitude as a key factor determining the trade-off between stability and plasticity. CRL-VLA achieves this insight through a dual critic architecture and a PPO loss with several regularization terms, enabling asymmetric tuning that efficiently adapts to new tasks while preserving prior knowledge. 

requires expensive multi-step rollouts and bootstrapping, which is hard to scale (Chen et al., 2023). Concretely, for large VLA policies deployed on real robots or high-fidelity simulators, each additional rollout entails a full forward pass of a vision–language backbone plus action decoding, making per-update advantage estimation extremely costly (Wen et al., 2024). Therefore, in continual VLA settings, MC estimation is preferred the TD bootstrapping due to prohibitive computational costs in scaling models and the bias inherent in value estimation. 

**Goal-Conditioned Value Formulation** To condition the value function on language goal _g_ , we leverage the shared Vision-Language Model’s embedding as the global state representation. Specifically, we concatenate language embedding with global state representations before the MLP (Figure 1), which outputs the scalar value _V_ ( _s, g_ ). This joint encoding addresses the poor language-goal following capacity in VLA value heads (Intelligence et al., 2025). 

**Dual-Critic Architecture for Independent Dimension Management** To operationalize indirect control of _Mg_ , we design a dual-critic architecture as follows. 

**Indirect Control via Value Functions** Corollaries 4.1 and 4.2 demonstrate that the theoretical upper bounds on the performance gap can be expressed through value functions. Guided by this insight, we control _Mg_ indirectly via value estimation rather than imposing direct constraints on the advantage network. While value estimation can be realized through either state-value functions or action-value functions, we focus on the state-value function _V_ ( _s, g_ ) in the main text for conciseness; the extension to action-value functions is detailed in Appendix B.2. Specifically, for a given VLA policy _π_ and language goal _g_ , we approximate the advantage function _A_<sup>ˆ</sup> _g_ ( _s, a_ ) as: _A_ ˆ _g_ ( _s, a_ ) = _r_ ( _s, a, g_ )+ _γVπ_ ( _s_<sup>_′_</sup> _, g_ ) _−Vπ_ ( _s, g_ ), where _s ∼ d_<sup>_π_</sup> _g_ is a state sampled from the goal-conditioned state distribution, _s_<sup>_′_</sup> _∼P_ ( _·|s, a_ ) is the successor state, _Vπ_ ( _·, g_ ) is the state-value function for goal _g_ under policy _π_ , and _γ ∈_ (0 _,_ 1) is the discount factor. 

1. Frozen Goal-Conditioned Value (GCV) Critic _θ_ GCV. Initialized from the old task’s value network and frozen during new task training, it provides the reference value _V_ old( _s, g_ ) for Corollary 4.1, enabling regularization of value accuracy differences on old data while maintaining predictable bounds via value drift prevention. 

2. Trainable MC critic _θ_ MC. Updated on new task MC returns to implement Corollary 4.2, allowing natural emergence of _M_ new bounds. 

Overall, the shared backbone _ϕ_ serves as a unified feature extractor, while head decoupling enables targeted optimization. Specifically, the frozen GCV critic _θ_ GCV. preserves value consistency and constrains value approximation error, guiding the action head _ω_ to favor high-return actions in old task states. While the trainable MC critic _θ_ MC bounds growth while maintaining plasticity for continual learning. 

5 

**CRL-VLA: Continual Vision–Language–Action Learning** 

## **4.4. Regularization and Training Recipe** 

We instantiate Theorem 4.1 with Corollaries 4.1 and 4.2 through three mechanisms that balance stability and plasticity by controlling _M_ old, _M_ new, _D_ new, and _D_ old. This unified algorithm applies to both state and action value functions, with the latter detailed in Appendix B.2. 

First, we control _M_ old through Goal-Conditioned Value (GCV) consistency. At task transition, the converged MC critic is copied to _θ_ GCV and frozen. During new task training, backbone updates _ϕ_ are penalized when _Vϕ,θ_ GCV deviates from _V_ old. At task transition, we freeze the converged MC critic as _θ_ GCV anchored to reference values _V_ old( _s, g_ ) from _B_ old to minimize _εV_ on the old task distribution, as required by Corollary 4.1. We constrain _M_ old by ensuring the new policy generates trajectory-level action distributions consistent with the old policy when evaluated on sampled states ( _s, g_ ) _∈B_ old from previous tasks. This is achieved through the following loss: 


Second, we realize bounded _M_ new via MC Critic learning. Since the Corollary 4.2 directly shows controllable _M_ new is bounded by MC return _G_<sup>_g_</sup> _t_<sup>new</sup> during roll-out. Combined with dense reward shaping (Zhang et al., 2025b), this achieves accurate advantage estimation without constraining backbone plasticity. Thus, we train a learnable MC Critic critic _θ_ MC on new task trajectories: 


Our third mechanism constrains policy divergence _D_ new and _D_ old to control distribution shift. PPO’s trust region constraint (Eq. 15, Appendix B.1) limits the _π_ updates in the distribution of new task, thereby bounding _D_ new drift. To maintain _D_ old (Theorem 4.1), we propose 


where _π_ old is the old policy that generated _B_ old. The total training loss integrates these constraints: 


This Lagrangian relaxation of Eq. (1) instantiates Theorem 4.1’s dual constraints, with concrete derivations in appendix A.5. _L_ PPO and _L_ KL bound _D_ new and _D_ old (policy divergence), while _L_<sup>_V_</sup> GCV<sup>and</sup><sup>_LV_</sup> MC<sup>bound</sup><sup>_M_oldand enable</sup> _M_ new exploitation (value accuracy and plasticity). Hyperparameters _α, βV , η_ act as Lagrange multipliers controlling the stability-plasticity tradeoff. Overall, the CRL-VLA pipeline has been summarized in Alg. 1. 

**Algorithm 1** CRL-VLA: VLA Policy Continuous Learning 

|**Re**|**quire:** Pretrained VLA policy_πθ_0, tasks_{Tk}_<sup>_K_</sup><br>_k_=1<sup>.</sup>|
|---|---|
|1:|**for**_k_ = 1to_K_:|
|2:|**if** _k_ = 1:|
|3:|Train_πθ_1 on_T_1using standard RL|
|4:|Freeze_πθ_1 and its value function as_π_<sup>old</sup>,_V_old|
|5:|Store replay buffer_B_old|
|6:|**else**:|
|7:|**for**each training iteration:|
|8:|Collect new task trajectories_τ ∼πθ_ on_Tk_|
|9:|Sample batch_B_new _∼τ_,_B_old _∼D_old|
|10:|Compute losses_L_total by Eq. 13|
|11:|Update_θ_via gradient descent on_L_total|
|12:|Continually adapted VLA policies_{πθk}_<sup>_K_</sup><br>_k_=1|


# **5. Experiments** 

In this section, we explore how the CRL-VLA effectively achieves a balance between stability and plasticity, thereby enhancing the robot’s continuous learning ability for visual language manipulation tasks. To this end, our experiments aim to investigate the following questions: **1)** Compared to baseline algorithms, does CRL-VLA exhibit better adaptability and resistance to forgetting when performing a single long-horizon task? **2)** Compared to baseline algorithms, does CRL-VLA exhibit superior cross-task knowledge sharing and transfer performance when performing multiple long-horizon tasks? **3)** How important are the core components of the proposed method to the overall learning performance of the CRL-VLA framework? 

## **5.1. Setup** 

To comprehensively evaluate the performance of the proposed CRL-VLA, we constructed a set of VLA model continuous learning task settings based on the LIBERO (Liu et al., 2023) benchmark. Specifically, we constructed benchmark subsets by randomly sampling tasks from the LIBERO shared task pool. These subsets contain tasks randomly sampled from the original dataset to cover different task scales. Each benchmark contains multiple sets of tasks defined by language instructions. See Appendix C for specific task settings. Furthermore, we used the same OpenVLA-oft model and PPO post-training configuration for all algorithms (Tan et al., 2025; Kim et al., 2025). To systematically answer the first and second questions, two types of experimental settings were primarily considered: **1)** Single-task learning scenarios: used to evaluate the adaptability of each algorithm to a specific task; **2)** Multi-task learning scenarios: used to evaluate the cross-task knowledge sharing and continuous learning performance of each algorithm. 

6 

**CRL-VLA: Continual Vision–Language–Action Learning** 

**Baselines.** To thoroughly compare the superiority of the CRL-VLA, we consider several classic CL algorithms. **1)** Sequence Learning (SL) (Liu et al., 2023): This is the most direct CL algorithm. The VLA model is only fine-tuned for new tasks, without any specific mechanism to prevent forgetting. **2)** Learning Without Forgetting (LWF) (Li & Hoiem, 2017): This baseline algorithm retrains the VLA model using only new task data while preserving the model’s original functionality. **3)** Experience Replay (ER) (Lopez-Paz & Ranzato, 2017): This baseline algorithm stores sample data from past tasks and converts them into gradient constraints, achieving gradient contextual memory. **4)** Multi-Task Learning (MTL) (Liu et al., 2023): This baseline algorithm learns from both new and old tasks simultaneously. Our method includes two versions: one using V-based goal-conditioned value ( **CRL-VLA (V)** ) and the other using Q-based goalconditioned value ( **CRL-VLA (Q)** ). 

**Evaluation Metrics.** To systematically evaluate the performance of each algorithm, we adopted three standard metrics widely used in CRL benchmarks (Wolczyk et al., 2021): **1) Final Performance** ; **2) Stability and Forgetting** ; **3) Plasticity and Forward Transfer** . Specifically, the **Final Performance** metric represents the overall task performance of the VLA model after continuous training, and is measured by the Final Average Return ( **FAR** ): FAR := _T_ <u>1</u> � _Ti_ =1<sup>_RT,i._Thismetricreflectstheaverage</sup> success rate of the VLA model across all tasks in the posttraining phase. **Stability and Forgetting** metrics are evaluated using Backward Transfer ( **BWT** ), which measures how learning a new task affects the performance of previously learned tasks: BWT := _T −_ <u>1</u> 1 � _Ti_ =1 _−_ 1<sup>(</sup><sup>_RT,i −Ri,i_)</sup><sup>_._</sup> A negative BWT indicates a catastrophic forgetting rate in the VLA model. To explicitly quantify forgetting, we further define the Forgetting ( **F** ) metric for the VLA model: _Fi_ := max _k≥i Rk,i − RT,i,_ F := _T −_ <u>1</u> 1 � _Ti_ =1 _−_ 1<sup>_Fi,_This</sup> metric measures the degree of degradation from peak performance to final performance for each task. **Plasticity and Forward Transfer** metrics are evaluated using Forward Transfer ( **FT** ), which reflects the extent to which prior knowledge facilitates the learning of new tasks. Let _bi_ represent the baseline success rate of task _Ti_ before learning previous tasks. We define: FT := _T −_ <u>1</u> 1 � _Ti_ =2<sup>(</sup><sup>_Ri−_1</sup><sup>_,i −bi_)</sup><sup>_,_</sup> where a positive value indicates a beneficial forward transition in the VLA model. 

## **5.2. Main Results** 

**Single-task learning scenario.** Tab. 1 compares the continuous learning performance of various algorithms in single-task learning scenarios. The results show that, compared to the baselines, the CRL-VLA (Q) has the highest FAR metric value (0 _._ 98), the second highest BWT metric value ( _−_ 0 _._ 02), and the lowest F metric value (0 _._ 03). Except 

_Table 1._ Performance comparison on the single-task learning scenario. Specific task settings in Appendix C.1. _↑_ denotes higher is better, _↓_ denotes lower is better. Best results are **bold** , and <u>second best</u> are underlined. 

|**Method**|**FAR**(_↑_)|**BWT**(_↑_)|**FT**(_↑_)|**F**(_↓_)|
|---|---|---|---|---|
|SL (Liu et al., 2023)|0.00|-0.62|-0.50|0.62|
|MTL (Liu et al., 2023)|0.96|**0.11**|**-0.06**|0.06|
|ER (Lopez-Paz & Ranzato, 2017)|0.60|-0.51|**-0.06**|0.53|
|LWF (Li & Hoiem, 2017)|0.67|-0.50|**-0.06**|0.50|
|CRL-VLA (V)|0.67|-0.49|**-0.06**|0.50|
|CRL-VLA (Q)|**0.98**|-0.02|**-0.06**|**0.03**|


for the SL baseline algorithm ( _−_ 0 _._ 5), the other methods exhibit similarly high FT metric values ( _−_ 0 _._ 06). Therefore, our method has better overall task success rate and resistance to forgetting old tasks, thus enabling more continuous and stable learning of new tasks. This also confirms that our method allows the VLA model to better balance task stability and plasticity during continuous learning. 

_Table 2._ Performance comparison on the multi-task learning scenario. Specific task settings in Appendix C.2. 

|**Method**|**FAR**(_↑_)|**BWT**(_↑_)|**FT**(_↑_)|
|---|---|---|---|
|SL (Liu et al., 2023)|0.62|0.07|**0.25**|
|MTL (Liu et al., 2023)|0.49|0.00|**0.25**|
|ER (Lopez-Paz & Ranzato, 2017)|0.62|0.05|0.00|
|LWF (Li & Hoiem, 2017)|0.63|0.10|0.00|
|CRL-VLA (V)|**0.74**|**0.17**|0.00|
|CRL-VLA (Q)|0.66|-0.03|0.00|


_Figure 2._ Performance comparison of various algorithms during continual learning. Specific task settings in Appendix C.2. 

**Multi-task learning scenario.** To further examine whether the proposed method CRL-VLA possesses better cross-task knowledge sharing and continuous learning capabilities in multi-task learning scenarios, we conducted a performance comparison experiment (Tab. 2). The experimental results show that, compared to the baseline algorithms, our method CRL-VLA (V) has the highest FAR metric value (0 _._ 74) and the highest BWT metric value (0 _._ 17). Furthermore, regarding the FT metric values, SL and MTL have the highest values (0 _._ 25), while other methods have the 

7 

**CRL-VLA: Continual Vision–Language–Action Learning** 


_Figure 4._ The impact of different values of the loss weights of _L_ mc<sup>_V_(left) and</sup><sup>_LQ_</sup> mc<sup>(middle) on the continuous learning performance of the</sup> VLA model, and an ablation comparison with and without GCV (right). Specific task settings in Appendix C.4. 

same value (0 _._ ). Therefore, in multi-task learning scenarios, compared to the baseline, our method possesses better crosstask knowledge sharing and anti-forgetting capabilities, thus exhibiting better continuous learning capabilities. Moreover, the experiment result also demonstrates that our method can significantly improve the overall task success rate of the VLA model, and the performance comparison of each algorithm during the continuous learning process in Fig. 2 further confirms this. For more performance comparisons in multi-task learning scenarios, see Appendix Tab. 3. 

Furthermore, experimental results (Tab. 1 and Tab. 2) also show that _L_<sup>_Q_</sup> GCV<sup>is more effective in single-task learning,</sup> while _L_<sup>_V_</sup> GCV<sup>performs better in multi-task continuous learn-</sup> ing environments. We believe the fundamental reason for this is that in multi-task continuous learning, the state-goal distribution becomes more diverse, and similar states may correspond to multiple effective action implementations in different tasks. _L_<sup>_Q_</sup> GCV<sup>constrains value consistency at the</sup> action-condition level, implicitly enforcing outdated action semantics sampled from previous tasks, which may conflict with the current learning objective. In contrast, _L_<sup>_V_</sup> GCV<sup>op-</sup> erates at the state-goal level and marginalizes actions, thus maintaining robustness to increased action diversity while preserving long-horizon value semantics. 

## **5.3. Ablation Study** 

We first conduct ablation experiments on the GCV loss weights and policy KL loss weights in the CRL-VLA to evaluate the contribution of the GCV and policy KL components to the continuous learning performance of VLA. The experimental results are shown in Fig. 3. For _L_<sup>_Q_</sup> GCV and _L_<sup>_V_</sup> GCV<sup>losses,moderatelossweights(approximately</sup> 

0.01 and 0.001 respectively) yield better FAR and BWT, as well as lower forgetting, achieving a better post-training stability-plasticity balance for the VLA model. Furthermore, excessively small weights fail to suppress _M_ old, while excessively large weights over-constrain updates and reduce forward adaptation. On the other hand, moderate policy KL term weights _α_ perform best (approximately 0.01). An excessively strong KL term narrows the feasible update region and indirectly inhibits the effective use of _M_ new, while an excessively weak KL term leads to policy drift, potentially increasing the actual _M_ old even with critic anchoring. 

We further conduct ablation experiments on the value loss MC weights (Fig. 4, left and middle). The results show that the VLA model exhibits the best sustained learning performance when the weights of _L_<sup>_V_</sup> MC<sup>and</sup><sup>_LQ_</sup> MC<sup>areap-</sup> proximately 1. When the value loss weight is too small, the judge error increases, leading to a larger actual advantage and consequently worsening the BWT and forgetting effects; conversely, the optimization process tends to be conservative, potentially reducing the final task performance. This trend confirms that the quality of the critic estimation is a direct means of adjusting _Mg_ , which directly affects the sustained learning performance of the VLA model. Furthermore, experiments comparing the effects of GCV ablation (Fig. 4, right) demonstrate that directly allowing the critic to perceive the language goal brings better success rates, resistance to forgetting, and plasticity to the VLA model. 

# **6. Conclusion and Future Work** 

In this work, we study continual learning for VLA models and identify the goal-conditioned advantage magnitude as the key factor governing the stability–plasticity trade-off. 

8 

**CRL-VLA: Continual Vision–Language–Action Learning** 

Building on this theoretical insight, we propose CRL-VLA, an asymmetric regularization framework realized through a dual-critic architecture with a novel goal-conditioned value formulation. Empirical results demonstrate that CRL-VLA effectively mitigates catastrophic forgetting while maintaining strong forward transfer, outperforming existing baselines. An important direction is extending CRL-VLA to more diverse and unstructured task streams, including partial observability and non-stationary language goals. 

# **References** 

- Abbes, I., Subbaraj, G., Riemer, M., Islah, N., Therien, B., Tabaru, T., Kingetsu, H., Chandar, S., and Rish, I. Revisiting replay and gradient alignment for continual pre-training of large language models. _ArXiv_ , abs/2508.01908, 2025. doi: 10.48550/arxiv.2508.01908. 

- Achiam, J., Held, D., Tamar, A., and Abbeel, P. Constrained policy optimization. In _International conference on machine learning_ , pp. 22–31. PMLR, 2017. 

- Aich, A. Elastic weight consolidation (EWC): nuts and bolts. _CoRR_ , abs/2105.04093, 2021. URL https:// arxiv.org/abs/2105.04093. 

- Black, K., Brown, T., et al. Pi-0.6: A generalist policy for robotic manipulation. _arXiv preprint arXiv:2410.24192_ , 2024. 

- Chen, Y., Zhang, F., and Liu, Z. Adaptive bias-variance trade-off in advantage estimator for actor-critic algorithms. _Neural networks : the official journal of the International Neural Network Society_ , 169:764–777, 2023. doi: 10.1016/j.neunet.2023.10.023. 

- Guo, Y., Zhang, J., Chen, X., Ji, X., Wang, Y.-J., Hu, Y., and Chen, J. Improving vision-language-action model with online reinforcement learning. _arXiv preprint arXiv:2501.16664_ , 2025. 

- Hancock, A. J., Wu, X., Zha, L., Russakovsky, O., and Majumdar, A. Actions as language: Fine-tuning vlms into vlas without catastrophic forgetting. _arXiv preprint arXiv:2509.22195_ , 2025. 

- Intelligence, P., Black, K., Brown, N., Darpinian, J., Dhabalia, K., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Galliker, M. Y., Ghosh, D., Groom, L., Hausman, K., Ichter, B., Jakubczak, S., Jones, T., Ke, L., LeBlanc, D., Levine, S., Li-Bell, A., Mothukuri, M., Nair, S., Pertsch, K., Ren, A. Z., Shi, L. X., Smith, L., Springenberg, J. T., Stachowicz, K., Tanner, J., Vuong, Q., Walke, H., Walling, A., Wang, H., Yu, L., and Zhilinsky, U. _π_ 0 _._ 5: a vision-language-action model with open-world generalization, 2025. URL https: //arxiv.org/abs/2504.16054. 

- Jiang, A., Gao, Y., Wang, Y., Sun, Z., Wang, S., Heng, Y., Sun, H., Tang, S., Zhu, L., Chai, J., et al. Irl-vla: Training an vision-language-action policy via reward world model. _arXiv preprint arXiv:2508.06571_ , 2025a. 

- Jiang, K., Huang, S., Chen, X., Shao, J., Zhang, H., and Li, X. Multimodal continual learning with mllms from multiscenario perspectives. _arXiv preprint arXiv:2511.18507_ , 2025b. 

- Kakade, S. and Langford, J. Approximately optimal approximate reinforcement learning. In _Proceedings of the nineteenth international conference on machine learning_ , pp. 267–274, 2002. 

- Kessler, S., Parker-Holder, J., Ball, P., Zohren, S., and Roberts, S. J. Same state, different task: Continual reinforcement learning without interference. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 36, pp. 7143–7151, 2022. 

- Kim, M. J., Finn, C., and Liang, P. Fine-tuning visionlanguage-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 

- Korbak, T., Perez, E., and Buckley, C. L. RL with KL penalties is better viewed as Bayesian inference. In _Proceedings of the 25th International Conference on Artificial Intelligence and Statistics (AISTATS)_ , volume 151 of _Proceedings of Machine Learning Research_ , pp. 1083–1091. PMLR, 2022. URL https://proceedings.mlr. press/v151/korbak22a.html. 

- Kutalev, A. and Lapina, A. Stabilizing elastic weight consolidation method in practical ml tasks and using weight importances for neural network pruning. _arXiv preprint arXiv:2109.10021_ , 2021. 

- Lei, Y., Mao, S., Zhou, S., Zhang, H., Li, X., and Luo, P. Dynamic mixture of progressive parameter-efficient expert library for lifelong robot learning. _arXiv preprint arXiv:2506.05985_ , 2025. 

- Li, H., Zuo, Y., Yu, J., Zhang, Y., Yang, Z., Zhang, K., Zhu, X., Zhang, Y., Chen, T., Cui, G., et al. Simplevla-rl: Scaling vla training via reinforcement learning. _arXiv preprint arXiv:2509.09674_ , 2025. 

- Li, X., Lu, F., Tao, M., and Ye, F. X.-F. Robust first and second-order differentiation for regularized optimal transport. _SIAM J. Sci. Comput._ , 47:630–, 2024. doi: 10.48550/arxiv.2407.02015. 

- Li, Z. and Hoiem, D. Learning without forgetting. _IEEE transactions on pattern analysis and machine intelligence_ , 40(12):2935–2947, 2017. 

9 

**CRL-VLA: Continual Vision–Language–Action Learning** 

- Liu, B., Zhu, Y., Gao, C., Feng, Y., Liu, Q., Zhu, Y., and Stone, P. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791, 2023. 

- Lopez-Paz, D. and Ranzato, M. Gradient episodic memory for continual learning. _Advances in neural information processing systems_ , 30, 2017. 

- Pan, C., Yang, X., Li, Y., Wei, W., Li, T., An, B., and Liang, J. A survey of continual reinforcement learning. _arXiv preprint arXiv:2506.21872_ , 2025. 

- Rolnick, D., Ahuja, A., Schwarz, J., Lillicrap, T., and Wayne, G. Experience replay for continual learning. In _Advances in Neural Information Processing Systems (NeurIPS)_ , volume 32, 2019. 

- Rusu, A. A., Colmenarejo, S. G., Gulcehre, C., Desjardins, G., Kirkpatrick, J., Kavukcuoglu, K., Pascanu, R., and Hadsell, R. Policy distillation. In _International Conference on Learning Representations_ , 2016. 

- Schulman, J., Wolski, F., Dhariwal, P., Radford, A., and Klimov, O. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- Schwarz, J. H., Luketina, J., Czarnecki, W. M., GrabskaBarwinska, A., Hessel, M., Kavukcuoglu, K., Kumaran, D., and Teh, Y. W. Progress & compress: A scalable framework for continual learning. In _International Conference on Machine Learning (ICML)_ , pp. 4528–4537, 2018. 

- Shenfeld, I., Pari, J., and Agrawal, P. Rl’s razor: Why online reinforcement learning forgets less. _arXiv preprint arXiv:2509.04259_ , 2025. 

- Sutton, R. S. The bitter lesson, March 2019. Available at http://www.incompleteideas.net/. 

- Tan, S., Dou, K., Zhao, Y., and Krahenb¨ uhl, P.¨ Interactive post-training for vision-language-action models, 2025. URL https://arxiv.org/abs/2505.17016. 

   - Wu, Y., Wang, G., Yang, Z., Yao, M., Sheil, B., and Wang, H. Continually evolving skill knowledge in vision language action model. _arXiv preprint arXiv:2511.18085_ , 2025. 

   - Xu, J. and Zhu, Z. Reinforced continual learning. In _Advances in Neural Information Processing Systems (NeurIPS)_ , volume 31, pp. 907– 916, 2018. URL https://proceedings. neurips.cc/paper/2018/hash/ 3229532386db9d77f8ec75591c28b556-Abstract. html. 

   - Yadav, Y., Zhou, Z., Wagenmaker, A., Pertsch, K., and Levine, S. Robust finetuning of vision-language-action robot policies via parameter merging. _arXiv preprint arXiv:2512.08333_ , 2025. 

   - Zang, H., Wei, M., Xu, S., Wu, Y., Guo, Z., Wang, Y., Lin, H., Shi, L., Xie, Y., Xu, Z., et al. Rlinf-vla: A unified and efficient framework for vla+ rl training. _arXiv preprint arXiv:2510.06710_ , 2025. 

   - Zenke, F., Poole, B., and Ganguli, S. Continual learning through synaptic intelligence. In _International Conference on Machine Learning (ICML)_ , pp. 3987–3995, 2017. 

   - Zhang, H., Zhang, S., Jin, J., Zeng, Q., Qiao, Y., Lu, H., and Wang, D. Balancing signal and variance: Adaptive offline rl post-training for vla flow models. _arXiv preprint arXiv:2509.04063_ , 2025a. 

   - Zhang, H., Zhuang, Z., Zhao, H., Ding, P., Lu, H., and Wang, D. Reinbot: Amplifying robot visual-language manipulation with reinforcement learning. _arXiv preprint arXiv:2505.07395_ , 2025b. 

   - Zhou, Z., Zhu, Y., Zhu, M., Wen, J., Liu, N., Xu, Z., Meng, W., Peng, Y., Shen, C., Feng, F., et al. Chatvla: Unified multimodal understanding and robot control with vision-language-action model. In _Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing_ , pp. 5377–5395, 2025. 

- Wen, J., Zhu, Y., Li, J., Zhu, M., Tang, Z., Wu, K., Xu, Z., Liu, N., Cheng, R., Shen, C., Peng, Y., Feng, F., and Tang, J. Tinyvla: Toward fast, data-efficient visionlanguage-action models for robotic manipulation. _IEEE Robotics and Automation Letters_ , 10:3988–3995, 2024. doi: 10.1109/lra.2025.3544909. 

- Wolczyk, M., Zajac, M., Pascanu, R., Kucinski, L., and Milos, P. Continual world: A robotic benchmark for continual reinforcement learning. In _Advances in Neural Information Processing Systems_ , volume 34, pp. 12398– 12411, 2021. 

10 

**CRL-VLA: Continual Vision–Language–Action Learning** 

# **A. Theoretical Analysis and Proofs** 

## **A.1. Preliminaries and Definitions** 

**Definition A.1** (Mixture Occupancy Measures) **.** Given a goal distribution _p_ ( _g_ ), we define the mixture occupancy measure as: 


where _d_<sup>_π_</sup> _g_<sup>(</sup><sup>_s_) = (1</sup><sup>_−γ_) �</sup> _t_<sup>_∞_</sup> =0<sup>_γt_Pr(</sup><sup>_st_=</sup><sup>_s | g, π_) is the discounted state visitation distribution.</sup> **Definition A.2** (Advantage Magnitude) **.** For any policy _π_<sup>_κ_</sup> and goal _g_ , we define the _Advantage Magnitude_ , denoted as _Mg_ ( _π_<sup>_κ_</sup> ), as the maximum absolute advantage of the anchored policy _π_ (typically set as the previous policy _π_<sup>old</sup> ) evaluated over the state-action pairs visited by _π_<sup>_κ_</sup> : 


Based on Definition A.2, we define the aggregate stability and plasticity metrics evaluated on the new policy’s distribution: 


## **A.2. Proof of Theorem 4.1** 

We employ the Goal-Conditioned Performance Difference Lemma (PDL) (Kakade & Langford, 2002): 

**Lemma A.1** (Goal-Conditioned PDL) **.** _For any policies π_<sup>new</sup> _, π_<sup>old</sup> _and goal g, the performance difference satisfies:_ 


A.2.1. PROOF OF STABILITY BOUND 

We aim to bound the performance degradation on old tasks: _|J_ old( _π_<sup>new</sup> ) _− J_ old( _π_<sup>old</sup> ) _|_ . Fix a goal _g ∼ p_ old. Let _fg_ ( _s_ ) ≜ E _a∼π_ new( _·|s,g_ )[ _A_<sup>_π_</sup> _g_<sup>old</sup> ( _s, a_ )]. Using Lemma A.1, we decompose the expectation over _d_<sup>_π_</sup> _g_<sup>new</sup> : 


**Bounding the Supremum Term:** Note that for any state _s ∈_ supp( _d_<sup>_π_</sup> _g_<sup>new</sup> ) and action _a ∼ π_<sup>new</sup> ( _·|s, g_ ), the pair ( _s, a_ ) falls within the support of the visiting policy. By Definition A.2: 


**Term (II) Occupancy Mismatch:** This term represents the drift in state distribution. Applying Holder’s inequality and the¨ discounted occupancy bound (Achiam et al., 2017): 


Substituting the bounds: 


Applying Pinsker’s inequality ( _D_ TV _≤_ ~~�~~ <u>12</u><sup>_D_KL) and substituting back into the PDL (multiplying by</sup> 1 _−_ <u>1</u> _γ_<sup>):</sup> 


11 

**CRL-VLA: Continual Vision–Language–Action Learning** 

Taking the expectation over _g ∼ p_ old, applying Jensen’s inequality E[ _~~√~~ X_ ] _≤_ ~~�~~ E[ _X_ ], and using the definition _D_ old ≜ ~~�~~ 2 E _s∼dπ_ oldold<sup>[</sup><sup>_D_KL]:</sup> 


A.2.2. PROOF OF PLASTICITY BOUND 

For new tasks, we consider the performance gain: _J_ new( _π_<sup>new</sup> ) _− J_ new( _π_<sup>old</sup> ). Using Lemma A.1 with _π_<sup>old</sup> as the anchor, for a goal _g ∼ p_ new: 


Since E _a∼π_ old[ _A_<sup>_π_</sup> _g_<sup>old</sup> ( _s, a_ )] = 0, we can rewrite the inner expectation: 


By H¨older’s inequality: 


For states _s_ visited by _π_<sup>new</sup> , the advantage is bounded by _Mg_ ( _π_<sup>new</sup> ). Applying Pinsker’s inequality: 


Substituting back into the PDL: 


Taking the expectation over _g ∼ p_ new, applying Jensen’s inequality, and using the definitions of _M_ new and _D_ new: 


## **A.3. Corollaries and Proofs** 

## A.3.1. BOUNDS ON ADVANTAGE MAGNITUDE 

The metric _Mg_ ( _π_<sup>new</sup> ) defined in Definition A.2 depends on the magnitude of the estimated advantage _A_<sup>ˆ</sup> . We show that this magnitude is naturally bounded by the critic’s approximation error (for old tasks) or the return range (for new tasks). **Corollary A.1** (Stability Control via Critic Error) **.** _For old goals g ∈ p_ old _, assume rewards are bounded by R_ max _and the critic approximates the true value with error ε. Then Mg_ ( _π_<sup>new</sup> ) _is bounded by:_ 


_where C_ 1 _, C_ 2 _are constants depending on γ._ 

_Proof._ (Proof omitted for brevity, follows from triangle inequality on _A_<sup>ˆ</sup> = _r_ + _γV − V_ and bound analysis in Section A.3.1). 

**Corollary A.2** (Plasticity Control via Return Range) **.** _For new goals g ∈ p_ new _, if critics are fitted to MC returns bounded in_ [ _G_ min _, G_ max] _, let G_ abs = max( _|G_ min _|, |G_ max _|_ ) _. Then:_ 


_Proof._ Since _A_<sup>ˆ</sup> is evaluated on trajectories collected by _π_<sup>new</sup> (the visiting policy), the values satisfy the MC bounds. The proof follows directly from the triangle inequality _|r_ + _γV_<sup>_′_</sup> _− V | ≤|r|_ + _γ|V_<sup>_′_</sup> _|_ + _|V |_ and substituting _|V | ≤ G_ abs. 

12 

**CRL-VLA: Continual Vision–Language–Action Learning** 

## **A.4. Corollaries and Proofs: Controlling Advantage Magnitude** 

In Theorem 4.1, the stability and plasticity bounds depend linearly on the advantage magnitude _Mg_ ( _π_<sup>new</sup> ). Here, we derive explicit bounds for _Mg_ based on the critic’s approximation error (for old tasks) and the MC return range (for new tasks). These corollaries theoretically justify why minimizing critic error preserves stability and why bounding MC returns ensures safe plasticity. 

## A.4.1. BOUNDS FOR OLD TASKS (STABILITY) 

For old tasks, the advantage _A_<sup>ˆ</sup> _g_ old is estimated using learned value functions. We denote the true value functions of the anchored policy as _V_ old and _Q_ old. 

**Corollary A.3** (V-only Path Bound) **.** _Assume the reward is bounded by |r_ ( _s, a, g_ ) _| ≤ R_ max _. Let the learned value function Vθ approximate the anchored policy’s value V_ old _with a uniform error bound_ sup _s |Vθ_ ( _s, g_ ) _−V_ old( _s, g_ ) _| ≤ εV . Let ∥V_ old _∥∞ denote the infinity norm of the true value function. Then:_ 


_Proof._ Under the V-only path, the advantage is estimated as _A_<sup>ˆ</sup> ( _s, a_ ) = _r_ ( _s, a_ ) + _γ_ E _s′_ [ _Vθ_ ( _s_<sup>_′_</sup> )] _− Vθ_ ( _s_ ). By the triangle inequality and Jensen’s inequality ( _|_ E[ _X_ ] _| ≤_ E[ _|X|_ ]): 


Using the approximation assumption, for any state _s_ , _|Vθ_ ( _s_ ) _| ≤|V_ old( _s_ ) _|_ + _εV ≤∥V_ old _∥∞_ + _εV_ . Substituting these bounds: 


Since this bound holds for all ( _s, a_ ), it holds for the supremum over the support of any visiting policy _π_<sup>new</sup> , thus proving the corollary. 

**Corollary A.4** (Q-only Path Bound) **.** _Assume the learned Q-function Qϕ approximates the anchored Q-function Q_ old _with error_ sup _s,a |Qϕ_ ( _s, a, g_ ) _− Q_ old( _s, a, g_ ) _| ≤ εQ. Let ∥Q_ old _∥∞ be the supremum of the true Q-values. Then:_ 


_Proof._ The Q-only advantage is _A_<sup>ˆ</sup> ( _s, a_ ) = _Qϕ_ ( _s, a_ ) _−_ E _a′∼π_ [ _Qϕ_ ( _s, a_<sup>_′_</sup> )]. By the triangle inequality: 


Using the error bound _|Qϕ_ ( _s, a_ ) _| ≤∥Q_ old _∥∞_ + _εQ_ , we obtain: 


This completes the proof. 

## A.4.2. BOUNDS FOR NEW TASKS (PLASTICITY) 

For new tasks, where no pre-trained critic exists, the advantage is estimated using MC returns _Gt_ . 

**Corollary A.5** (MC Estimation Controls Plasticity) **.** _Assume the value functions are fitted to MC returns bounded within_ [ _G_ min _, G_ max] _. Let G_ abs ≜ max( _|G_ min _|, |G_ max _|_ ) _. Then the advantage magnitude Mg_ new _is bounded by:_ 


13 

**CRL-VLA: Continual Vision–Language–Action Learning** 

_Proof._ Since the critics are trained on bounded returns, we have _|V_ ( _s_ ) _| ≤ G_ abs and _|Q_ ( _s, a_ ) _| ≤ G_ abs for all states visited. **1. V-only path:** Recall that the realized return satisfies _Gt_ = _rt_ + _γGt_ +1. Rearranging for reward implies _rt_ = _Gt − γGt_ +1, thus _|rt| ≤|Gt|_ + _γ|Gt_ +1 _| ≤_ (1+ _γ_ ) _G_ abs. Substituting this reward bound and the value bound into the advantage definition: 


**2. Q-only path:** Directly applying the triangle inequality to _A_<sup>ˆ</sup> ( _s, a_ ) = _Q_ ( _s, a_ ) _−_ E[ _Q_ ( _s, ·_ )]: 


A.4.3. SUMMARY OF THEORETICAL IMPLICATIONS 

These corollaries provide the mechanism for the Unified Stability-Plasticity bounds in Theorem 4.1: 

- **Stability:** Corollaries A.3 and A.4 imply that stability on old tasks is governed by the quality of value function approximation ( _εV , εQ_ ). A well-optimized critic minimizes _M_ old, thereby tightening the trust region and preventing catastrophic forgetting. 

- **Plasticity:** Corollary A.5 ensures that even during the exploration of new tasks (where _π_<sup>new</sup> may diverge significantly from _π_<sup>old</sup> ), the advantage magnitude remains strictly bounded by the return range. This prevents destabilizing updates solely due to estimation variance, facilitating safe adaptation. 

## **A.5. Objectives and Total Training Loss** 

**Policy Divergence Constraint for** _D_ new **and** _D_ old The trust region in Eq. 14 bounds _D_ new. To constrain _D_ old per Theorem 4.1, we add goal-conditioned behavior cloning on _B_ old: 


**Total Training Loss: Lagrangian Relaxation** Recall our constrained continual learning objective: 


We convert this into an unconstrained optimization via Lagrangian relaxation. By Theorem 4.1, the constraint can be decomposed into bounds on policy divergence ( _D_ old _, D_ new) and value accuracy ( _M_ old _, M_ new). This yields the Lagrangian: 


where _α, βV , η ≥_ 0 are Lagrange multipliers enforcing the constraint. 

We instantiate this Lagrangian with practical loss terms: 


where: 

14 

**CRL-VLA: Continual Vision–Language–Action Learning** 

- _L_ PPO _≈−Jgk_ ( _π_<sup>_k_</sup> ): PPO objective maximizing new-task return with _D_ new trust region; 

- _L_ KL _∝ D_ old: behavior cloning loss bounding old-task policy divergence; 

- _L_<sup>_V_</sup> GCV<sup>_∝M_old:frozen critic loss constraining old-task value drift;</sup> 

- _L_<sup>_V_</sup> MC<sup>_∝M_new:trainable critic loss ensuring new-task value accuracy.</sup> 

Thus, Eq. (13) is a Lagrangian relaxation of Eq. (11), with hyperparameters _α, βV , η_ serving as Lagrange multipliers that balance stability (preserving old-task performance) and plasticity (learning new tasks). 

# **B. Implementation Details** 

## **B.1. Architecture and Value Function Design** 

**Goal-Conditioned Value Formulation** The value network is conditioned on language goal _g_ by concatenating language token embeddings with state representations (extracted from the VLA backbone) before feeding through an MLP. This design ensures sensitivity to language-conditioned goals, inheriting smoothness from the shared embedding geometry. After task transition, the value network’s sensitivity to state actions automatically adjusts through the goal-conditioned mechanism. 

**Dual-Critic Implementation.** The policy consists of three critics on shared backbone _ϕ_ : 

- Action critic _ω_ . 

- MC critic _θ_ MC: trained on new task returns, initialized randomly for task 1 

- GCV critic _θ_ GCV: copied from previous task’s MC critic at task transition, then frozen 

At task _k_ = 1, standard RL training optimizes _L_ PPO + _η L_<sup>_V_</sup> MC<sup>.Upon transition to task</sup><sup>_k>_1, we freeze the converged MC</sup> critic as the new GCV critic and initialize a fresh MC critic. 

**PPO Loss Implementation and KL Constraint** Following Schulman et al. (2017), we optimize the clipped surrogate objective for each task to ensure stable policy updates. Specifically, we constrain the policy update by enforcing a KL divergence penalty between the updated policy _πθ_ and the reference policy _π_<sup>_′_</sup> , thereby adhering to the trust region principle. Building upon this framework, the surrogate constraint for policy divergence constrains _D_ new. The overall PPO loss is then expressed as: 


where _ϵ_ is the **clipping hyperparameter** that restricts the probability ratio _rθ_ ( _s, a, g_ ) = _ππ_ old _<u>θ</u>_ <u>((</u> _aa|s|s,g,g_ <u>))</u><sup>.To strictly enforce the</sup> trust region, we implement an **early stopping criterion** based on the approximate KL divergence: 


where _d_ targ is the **target KL threshold** . The advantage _A_<sup>ˆ</sup> _θ_ is computed using Generalized Advantage Estimation (GAE) ( **?** ): 


where _γ ∈_ [0 _,_ 1] is the **discount factor** , _λ ∈_ [0 _,_ 1] is the **GAE smoothing parameter** , and _δt_<sup>_V_=</sup><sup>_rt_+</sup><sup>_γV_(</sup><sup>_st_+1)</sup><sup>_−V_(</sup><sup>_st_)</sup> denotes the TD error. 

15 

**CRL-VLA: Continual Vision–Language–Action Learning** 

## **B.2. Action-Value (Q-based) Implementation** 

We extend the Dual-Critic Architecture and Goal-Conditioned Value Formulation detailed in the methodology to action-value functions. This extension applies the same principles of independent dimension management to _Q_ ( _s, a, g_ ), enabling precise control over stability and plasticity in the action-value space. 

**Goal-Conditioned Action-Value Formulation** Consistent with the value function design, we leverage the shared VisionLanguage Model’s embedding as the global state representation _ϕ_ ( _s, g_ ). To parameterize the action-value function _Q_ ( _s, a, g_ ), we concatenate the continuous action vector _a_ with the language-grounded state embedding _ϕ_ ( _s, g_ ) before the Multi-Layer Perceptron processing. This joint encoding ensures that _Q_ -values inherit the metric smoothness and semantic understanding from the pretrained VLM embedding space, addressing language-goal tracking issues while incorporating action information. 

**Dual-Critic Architecture via Action State Value** To operationalize the control of _M_ old and _M_ new within the Q-learning framework, we employ the Dual-Critic Architecture with critic decoupling: **1) Frozen GCV Q-critic** _θ_ **GCV.** Initialized from the old task’s converged Q-network and frozen during new task training. It serves as the anchor for stability, providing reference values _Q_ old( _s, a, g_ ) to regularize backbone updates on historical data. **2) Trainable MC Q-critic** _θ_ **MC.** Updated on new task trajectories using MC returns. This critic remains plastic to capture the reward structure of the new task, naturally bounding _M_ new via the environment’s reward limits. 

**Q-based Goal-Conditioned Value Consistency (Q-GCV)** The Q-based GCV mechanism enforces consistency between the current backbone’s predictions (via the frozen GCV critic) and the historical Q-values stored in the replay buffer _B_ old. Unlike the value function which targets MC returns, the Q-function targets the specific state-action values _Q_ old recorded from previous interactions. The loss is formulated as the Mean Squared Error (MSE): 


This objective constrains the shared backbone _ϕ_ to maintain representations that, when passed through _θ_ GCV, reconstruct the historical action values, thereby minimizing performance degradation on old tasks ( _M_ old). 

**Q-based Monte Carlo Learning** To exploit the plasticity dimension ( _M_ new), the Trainable MC Q critic is optimized to fit the returns _G_<sup>_g_</sup> _t_<sup>new</sup> from the current policy on the new task: 


This allows the shared backbone to learn features necessary for the new task without being overly inhibited by the frozen GCV critic, as the optimization of _θ_ MC drives the embedding towards relevant new structures. 

## **B.3. Training Procedure and Hyperparameters** 

All experiments are conducted based on OpenVLA-OFT (Kim et al., 2025), where the official pretrained checkpoints are adopted as the base model and LoRA adapters are applied for efficient task adaptation. Our implementation is built upon the RIPT-VLA codebase (Tan et al., 2025), and all unspecified training configurations strictly follow the settings reported in prior work. Training is performed with a LoRA rank of 32, and the detailed hyperparameter configuration is summarized in Tab. 7. Unless otherwise stated, all hyperparameters are kept consistent across experiments to ensure fair comparison. All experiments are executed on the following hardware platform: **CPU:** Intel(R) Xeon(R) Platinum 8358 @ 2.60GHz; **GPU:** NVIDIA A100-SXM4-80GB. 

# **C. Task and Experiment Details** 

To systematically evaluate the robustness and scalability of our method, we construct multiple benchmarks by randomly sampling tasks from a shared task pool. Each benchmark contains a different number of object manipulation tasks, serving as controlled evaluation settings with varying task complexity and combinatorial difficulty. All benchmarks are fixed across methods and runs to ensure fair comparison. 

Specifically, we evaluate our method on a subset of the **LIBERO** benchmark suite, consisting of tasks randomly sampled from the original collection to encompass various task cardinalities. We denote these benchmarks as **Task-1** through **Task-4** . Each benchmark comprises multiple task sets defined by natural language directives, primarily focusing on robotic 

16 

**CRL-VLA: Continual Vision–Language–Action Learning** 

_Table 3._ More performance comparison on the multi-task learning scenario. Specific task settings in Appendix C.3. _↑_ denotes higher is better, while _↓_ denotes lower is better. The **best** and second best results are highlighted accordingly. 

|**Method**|**FAR**(_↑_)|**BWT**(_↑_)|**FT**(_↑_)|
|---|---|---|---|
|SL (Liu et al., 2023)|0.60|0.00|-0.70|
|MTL (Liu et al., 2023)|0.54|**0.17**|-0.70|
|ER (Lopez-Paz & Ranzato, 2017)|0.52|-0.05|**-0.65**|
|LWF (Li & Hoiem, 2017)|0.43|0.00|**-0.65**|
|CRL-VLA (V)|**0.63**|-0.10|-0.70|
|CRL-VLA (Q)|0.33|-0.45|-0.70|


_Table 4._ Comparison of continual learning metrics under different parameter settings (Only _L_<sup>_V_</sup> GCV<sup>, Only</sup><sup>_L_</sup> GCV<sup>_V_, and KL), where all</sup> experiments are conducted on the Task-4 benchmark (Appendix C.4). 

|PARAMETERVALUE|FAR(_↑_)|BWT(_↑_)|FORGETTING(_↓_)|FT(_↑_)|
|---|---|---|---|---|
|_L_<sup>_Q_</sup><br>GCV|||||
|0.00001|0.97|-0.02|0.02|-0.13|
|0.0001|0.94|-0.05|0.05|-0.09|
|0.001|0.93|-0.05|0.05|**-0.06**|
|0.01|**0.98**|**0.02**|**0.00**|-0.09|
|0.1|0.93|0.00|0.02|**-0.06**|
|_L_<sup>_V_</sup><br>GCV|||||
|0.00001|0.91|-0.05|0.06|-0.06|
|0.0001|0.91|**0.00**|**0.00**|-0.19|
|0.001|**0.98**|**0.00**|**0.00**|-0.06|
|0.01|0.94|-0.06|0.06|**-0.03**|
|0.1|0.93|-0.03|0.02|-0.06|
|**KL**|||||
|0|0.91|-0.03|0.03|**-0.03**|
|0.000001|0.95|-0.02|**0.02**|-0.09|
|0.00001|**0.98**|-0.02|**0.02**|-0.06|
|0.0001|0.95|-0.02|**0.02**|-0.11|
|0.001|0.91|-0.05|0.05|**-0.03**|
|0.01|0.96|**0.02**|**0.02**|-0.06|
|0.1|0.90|-0.02|0.06|-0.09|


pick-and-place behaviors. This setup allows us to rigorously assess the model’s instruction-following capabilities and its generalization across diverse task scales. we next detail the language instructions used for each benchmark. Each task consists of one or more natural language directives. 

## **C.1. Task-1 Benchmark** 

- _Task 0_ : “pick up the black bowl from table center and place it on the plate” 

- _Task 1_ : “pick up the black bowl next to the ramekin and place it on the plate” 

- _Task 2_ : “pick up the black bowl on the cookie box and place it on the plate” 

## **C.2. Task-2 Benchmark** 

- _Task 0_ : “pick up the orange juice and place it in the basket”, “pick up the chocolate pudding and place it in the basket”, “pick up the bbq sauce and place it in the basket” 

- _Task 1_ : “pick up the cream cheese and place it in the basket”, “pick up the milk and place it in the basket”, “pick up the tomato sauce and place it in the basket” 

17 

**CRL-VLA: Continual Vision–Language–Action Learning** 

_Table 5._ Ablation study on the effects of the _L_ MC<sup>_V_losscoefficientandthe</sup><sup>_LQ_</sup> MC<sup>losscoefficientonperformanceandstability.All</sup> experiments are conducted on the Task-4 benchmark (Appendix C.4). 

|PARAMETERCOEF|FAR(_↑_)|BWT(_↑_)|FORGETTING(_↓_)<br>FT(_↑_)|
|---|---|---|---|
|_L_<sup>_V_</sup><br>MC||||
|10|0.93|**0.00**|**0.02**<br>-0.06|
|1|**0.95**|-0.02|**0.02**<br>**-0.03**|
|0.1|0.93|-0.03|0.03<br>-0.06|
|0.01|0.90|-0.05|0.05<br>-0.13|
|0.001|0.85|-0.08|0.08<br>-0.13|
|_L_<sup>_Q_</sup><br>MC||||
|10|0.98|**0.05**|**0.00**<br>-0.06|
|1|**0.99**|**0.05**|**0.00**<br>**0.00**|
|0.1|0.94|0.03|**0.00**<br>-0.06|
|0.01|0.85|-0.06|0.09<br>-0.06|
|0.001|0.92|-0.03|0.08<br>-0.06|


_Table 6._ Ablation study of the Goal-Conditioned Value (GCV) network on model performance and stability. All experiments are conducted on the Task-4 benchmark (Appendix C.4). Enabling GCV leads to higher success rates (FAR) and significantly reduced forgetting. 

|USED GCV|FAR(_↑_)|BWT(_↑_)|FORGETTING(_↓_)|FORWARDTRANSFER(_↑_)|
|---|---|---|---|---|
|FALSE|0.29|-0.06|0.06|-0.72|
|TRUE|**0.31**|**-0.02**|**0.02**|**-0.70**|


## **C.3. Task-3 Benchmark** 

- _Task 0_ : “pick up the bbq sauce and place it in the basket”, “pick up the chocolate pudding and place it in the basket” 

- _Task 1_ : “pick up the ketchup and place it in the basket”, “pick up the salad dressing and place it in the basket” 

## **C.4. Task-4 Benchmark** 

- _Task 0_ : “put the wine bottle on the rack”, ”put the cream cheese in the bowl” 

- _Task 1_ : “push the plate to the front of the stove”, ”put the bowl on the stove.” 

- _Task 2_ : “put the wine bottle on top of the cabinet”, ”open the top drawer and put the bowl inside.” 

## **C.5. Baselines** 

**1)** Sequential Learning (SL) (Liu et al., 2023): This is the most straightforward continual learning method, where the VLA model is simply fine-tuned on new tasks without any specific mechanisms to prevent forgetting. **2)** Multi-Task Learing (MTL) (Liu et al., 2023): This baseline algorithm learns from both new and old tasks simultaneously. **3)** Learning Without Forgetting (LWF) (Li & Hoiem, 2017): This algorithm preserves existing knowledge without requiring the old data by having the new model _imitate_ the old model’s predictions on new data during training (knowledge distillation). **4)** Experience Replay (ER) (Lopez-Paz & Ranzato, 2017): It is a classic example of combining reinforcement learning and supervised learning, explicitly using episode memory to store samples from past tasks and converting them into gradient constraints to prevent the gradients of new tasks from degrading the performance on old tasks. 

18 

**CRL-VLA: Continual Vision–Language–Action Learning** 

_Table 7._ Training hyperparameter configuration. 

|**Parameter**|**Value**|
|---|---|
|_General_||
|LoRA Rank|32|
|Gradient Accumulation Steps|1|
|PPO Epochs|1|
|PPO Clip Range|0_._2|
|PPO Clip High|0_._2|
|Max Step Batch Size|2<br>|
|Learning Rate (LoRA modules)|1_._0_×_10<sup>_−_4</sup>|
|Learning Rate (Action head)|5_._0_×_10<sup>_−_5</sup>|
|Weight Decay|1_._0_×_10<sup>_−_4</sup>|
|Gradient Clip Norm (model)|1_._0|
|Gradient Clip Norm (header)|1_._0|
|Total Steps_M_|12|
|Eval Interval_Iinterval_|1|
|Update Times_N_|10|
|_CRL-VLA Weight_||
|Q-Network Constraint (_L_<sup>_Q_</sup><br>GCV<sup>)</sup>|0_._01|
|Value-Head Constraint (_L_<sup>_V_</sup><br>GCV<sup>)</sup>|0_._01|
|KL Divergence Scale (_λ_KL)<br>|1_._0_×_10<sup>_−_6</sup>|
|Q Loss Coef (_L_<sup>_Q_</sup><br>MC<sup>)</sup>|1_._0|
|Value Loss Coef (_L_<sup>_V_</sup><br>MC<sup>)</sup>|1_._0|
|Global Context Vector (GCV)|Enabled|


19 

