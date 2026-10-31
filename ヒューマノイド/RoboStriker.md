---
title: "RoboStriker: Hierarchical Decision-Making for Autonomous Humanoid Boxing"
date: "2026-01-30"
authors: "Kangning Yin; Zhe Cao; Wentao Dong; Weishuai Zeng; Tianyi Zhang; Qiang Zhang"
url: https://arxiv.org/abs/2601.22517
pdf: https://arxiv.org/pdf/2601.22517
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.22517)** / [論文ページ](https://arxiv.org/abs/2601.22517)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**RoboStriker: Hierarchical Decision-Making for Autonomous Humanoid Boxing** 

**Kangning Yin**<sup>* 1 2 3</sup> **Zhe Cao**<sup>* 1 2</sup> **Wentao Dong**<sup>1 2</sup> **Weishuai Zeng**<sup>2 4</sup> **Tianyi Zhang**<sup>1</sup> **Qiang Zhang**<sup>5</sup> **Jingbo Wang**<sup>2</sup> **Jiangmiao Pang**<sup>2</sup> **Ming Zhou**<sup>2</sup> **Weinan Zhang**<sup>1 2 3</sup> 

# **Abstract** 

Achieving human-level competitive intelligence and physical agility in humanoid robots remains a major challenge, particularly in contact-rich and highly dynamic tasks such as boxing. While Multi-Agent Reinforcement Learning (MARL) offers a principled framework for strategic interaction, its direct application to humanoid control is hindered by high-dimensional contact dynamics and the absence of strong physical motion priors. We propose RoboStriker, a hierarchical threestage framework that enables fully autonomous humanoid boxing by decoupling high-level strategic reasoning from low-level physical execution. The framework first learns a comprehensive repertoire of boxing skills by training a single-agent motion tracker on human motion capture data. These skills are subsequently distilled into a structured latent manifold, regularized by projecting the Gaussian-parameterized distribution onto a unit hypersphere. This topological constraint effectively confines exploration to the subspace of physically plausible motions. In the final stage, we introduce Latent-Space Neural Fictitious SelfPlay (LS-NFSP), where competing agents learn competitive tactics by interacting within the latent action space rather than the raw motor space, significantly stabilizing multi-agent training. Experimental results demonstrate that RoboStriker achieves superior competitive performance in simulation and exhibits sim-to-real transfer. Our website is available at RoboStriker. 

> 1Shanghai Jiao Tong University 2Shanghai Artificial Intelligence Laboratory<sup>3</sup> Shanghai Innovation Institute<sup>4</sup> Peking University<sup>5</sup> The Hong Kong University of Science and Technology (Guangzhou),. Correspondence to: Ming Zhou <zhouming@pjlab.org.cn>, Weinan Zhang <wnzhang@sjtu.edu.cn>. 

_Preprint. February 2, 2026._ 


_Figure 1._ Real-world clips of humanoid boxing using RoboStriker, showcasing agile, contact-rich punches and defenses under physical constraints. 

# **1. Introduction** 

Humanoid robots serve as a critical frontier for embodied intelligence, with recent breakthroughs demonstrating exceptional capabilities in locomotion and agile maneuvers (Liao et al., 2025; Yin et al., 2025; Zeng et al., 2025; Zhang et al., 2025). These successes, however, have largely focused on single-agent execution, where the environment is passive and predefined. Once other agents are introduced, as in competitive physical interactions such as boxing, the problem fundamentally shifts from motion-generation to strategic co-adaptation under physical constraints. This shift naturally situates humanoid competition within the scope of Multi-Agent Reinforcement Learning (MARL). Yet, unlike symbolic or abstract domains where MARL has achieved grandmaster-level success (Silver et al., 2017; Vinyals et al., 2019), embodied humanoid competition requires reasoning through high-dimensional, contact-rich dynamics, where every strategic decision is physically bound by balance stability and actuation limits. At this frontier of multi-agent embodiment, we argue that there lie two intrinsic and domainagnostic contradictions that characterize the competitive humanoid systems. 

**Physical Feasibility vs. Non-stationary Learning.** Humanoid control operates in a high-dimensional continuous action space, which is subject to strict physical constraints, including contact stability, joint limits and underactuated dynamics. Effective strategy exploration, however, requires 

1 

**RoboStriker: Hierarchical Decision-Making for Autonomous Humanoid Boxing** 

diverse and sometimes aggressive behaviors. As a result, such unconstrained policy exploration often leads to physically invalid motions and fails to keep balance (Peng et al., 2018; 2021), while overly restrictive controllers collapse strategy learning. This further creates an embodied coldstart problem: agents cannot evolve competitive strategies without first maintaining a stable physical stance (Luo et al., 2023). 

**Strategy Evolution vs. System Stability.** MARL via selfplay (Samuel, 1959; Hernandez et al., 2019) relies on continuously evolving opponent policies, which introduces severe non-stationarity during training. While such dynamics are essential for discovering competitive strategies, humanoid systems are dynamically fragile: small distributional shifts in opponent behavior can destabilize balance and contact, leading to training collapse. This results in another tension between competitive strategy evolution and stable embodied interaction. 

Existing approaches address these challenges in an isolated manner. Game-theoretic MARL methods such as Neural Fictitious Self-Play (NFSP) (Heinrich & Silver, 2016) are designed for abstract or weakly grounded environments, lacking inductive biases for physical feasibility. Conversely, embodied control frameworks such as Adversarial Motion Priors (AMP) (Peng et al., 2021) and DeepMimic (Peng et al., 2018) excel at learning robust single-agent motor skills via imitation, but do not support strategic co-evolution or opponent-aware adaptation. As a result, neither line of work alone can resolve the dual contradictions inherent to embodied competitive tasks. 

In this work, we argue that resolving these challenges requires a structured decoupling of physical control and strategic reasoning, coupled with a training mechanism that stabilizes competitive evolution. To this end, we propose a hierarchical framework that decomposes embodied MARL into three coupled layers: (1) physically grounded motion library, (2) structured latent motion space for strategy representation and (3) multi-agent strategy evolution over this latent space. Concretely, in the first layer, we establish a DeepMimic-based tracking policy (Peng et al., 2018) to faithfully reproduce diverse human motion primitives, ensuring the agent masters a repertoire of physically feasible kinematic skills. In the second layer, we construct a bounded latent motion space that supports diverse motion generation and serves as the effective strategy space. In the third layer, we perform competitive strategy learning via NFSP, namely Latent Space NFSP (LS-NFSP), which enables latent multi-agent co-evolution within the bounded latent manifold. Crucially, the bounded latent motion space is not merely a representational choice, it defines a compact, physically safe strategy search space that allows LS-NFSP to operate without inducing motor-level instability. Meanwhile, AMP-based (Peng et al., 2021) curriculum warmup 

initializes the policy within this manifold, mitigating the competitive cold-start problem and substantially reducing the non-stationarity during fictitious self-play. Together, these mechanisms resolve the aforementioned contradictions of embodied MARL by reconciling physical stability with strategic diversity, and stabilizing strategy evolution under continuous competition. 

We evaluate our framework on a humanoid boxing task using Unitree G1 robots with 29 degrees of freedom (Unitree, 2024), demonstrating that the proposed method achieves substantially improved performance, robustness, and convergence stability compared to existing baselines. Beyond this specific task, our framework provides a general recipe for embodied multi-agent competition, offering a principled pathway to scale MARL from abstract games to physically grounded robotic systems. Our contributions are summarized as follows: 

- To the best of our knowledge, this work is the first to formally characterize the intrinsic contradictions in embodied MARL, specifically the trade-off between physical feasibility and non-stationary learning, and the conflict between strategy evolution and system stability, using humanoid competition as a prime instantiation. 

- We propose a hierarchical framework that decouples high-level strategic reasoning from low-level physical execution, providing a stable pathway for evolving dynamic combat behaviors. 

- We demonstrate the robustness of our framework through the emergence of tactical boxing in simulation and its zero-shot transfer to physical humanoid robots ( Figure 1). 

# **2. Related Work** 

**Humanoid Motion Synthesis and Control.** The generation of lifelike humanoid movement has evolved from purely kinematic trajectory synthesis to physics-aware control policies. Kinematic Motion Synthesis historically relied on Inverse Kinematics (IK) and space-time optimization to retarget motion capture data onto robotic morphologies while satisfying joint and geometric constraints (Gleicher, 1998; Yamane et al., 2004). While deep generative models have significantly improved the diversity of synthesized trajectories (Holden et al., 2016; Zhang et al., 2023; Petrovich et al., 2023; Yin et al., 2024), these purely kinematic approaches lack dynamical awareness, often resulting in physical violations like "foot sliding" when transferred to simulators. Physics-based control addresses the challenge of executing motions within a dynamical environment by accounting for gravity, inertia, and contact forces. Classical robot learning methods utilize Zero Moment Point (ZMP) stability 

2 

**RoboStriker: Hierarchical Decision-Making for Autonomous Humanoid Boxing** 


_Figure 2._ Overview of RoboStriker. **Stage I** pretrains a motion tracker to produce physically plausible humanoid behaviors; **Stage II** compresses these behaviors into a bounded latent space for high-level control; **Stage III(a)** runs warm-up training on top of Stage II, then followed with **Stage III(b)** , a NFSP over latent-space to solve the humanoid boxing task as a two-player zero-sum game. 

and Model Predictive Control (MPC) to ensure bipedal balance (Kajita et al., 2003; Kuindersma et al., 2016). Modern reinforcement learning (RL) (Sutton et al., 1998) has advanced this through tracking-based imitation (Peng et al., 2018) and adversarial stylistic regularization (Peng et al., 2021). Crucially, the development of universal motion trackers (Chen et al., 2025; Yin et al., 2025; Zhang et al., 2025) has enabled the learning of unified policies capable of tracking a diverse repertoire of human motions. While these universal trackers provide a robust foundation for executing a vast library of skills, they primarily focus on highfidelity imitation of pre-defined trajectories. In contrast, our work builds upon universal tracking but extends it to a reactive, multi-agent setting, where the controller must maintain physical stability while simultaneously adapting to the non-stationary perturbations of an opponent. 

**Skill-based Latent Representation Learning.** To manage the complexity of humanoid action spaces, recent research has shifted toward learning low-level skills in latent manifolds. PULSE (Luo et al., 2023) establishes that distilling vast motion capture datasets into latent embeddings allows high-level policies to invoke complex behaviors via a simplified behavioral interface. Further refinements like CALM (Tessler et al., 2023) have improved the semantic diversity and controllability of these latent spaces. However, these manifolds are typically treated as unbounded Euclidean spaces where unconstrained exploration can still 

lead to out-of-distribution actions that cause physical collapse. We depart from this by imposing topological regularization—projecting the latent space onto a unit hypersphere (Peng et al., 2022; Davidson et al., 2018). This geometric constraint ensures that the strategic search remains bounded within a manifold of physically plausible maneuvers, effectively isolating the high-level policy from the dynamical instabilities of the robot’s joints. In this work, we leverage this topologically constrained manifold to decouple strategic reasoning from dynamics control, enabling the efficient evolution of complex competitive behaviors that would be intractable in raw observation spaces 

**Multi-Agent RL and Fictitious Self-Play.** Self-play has emerged as a principled paradigm for learning robust policies in competitive settings by framing training as an implicit game-solving process. Classical fictitious play (Brown, 1951) iteratively best-responds to the empirical distribution of past opponents and is known to converge to a Nash equilibrium in certain classes of games. Modern adaptations of fictitious self-play (FSP) integrate reinforcement learning with historical policy averaging, achieving strong empirical performance in large-scale imperfectinformation games such as poker (Heinrich & Silver, 2016). Subsequent extensions have explored continuous control and function approximation, showing that approximate bestresponse dynamics can converge to approximate Nash equilibria under bounded strategy spaces and smoothness as- 

3 

**RoboStriker: Hierarchical Decision-Making for Autonomous Humanoid Boxing** 

sumptions (Mertikopoulos & Zhou, 2019). Despite these advances, applying self-play directly in high-dimensional MARL often leads to cyclic strategic oscillations and training instabilities, particularly when policies operate in unconstrained continuous action spaces (Lanctot et al., 2017). Recent works have highlighted that constraining the effective strategy space—through regularization, policy parameterization, or latent abstractions—can significantly improve convergence behavior and stability in competitive learning (Balduzzi & Racaniere, 2018). From a game-theoretic perspective, restricting policies to a compact, continuous strategy set ensures the existence of mixed-strategy Nash equilibria and supports convergence guarantees for no-regret and fictitious-play-style dynamics (Rosen, 1965; Ramazi & Cao, 2020). 

Our work builds on this line of research by situating fictitious self-play within a bounded latent strategy manifold. By conducting the competitive learning process in a compact hyperspherical latent space rather than the raw motor command space, we effectively limit the strategic degrees of freedom available to each agent. This design mitigates non-stationarity arising from unbounded policy updates and aligns the training dynamics with theoretical convergence results for approximate Nash equilibria in continuous games with compact strategy sets. 

# **3. Method** 

We propose a hierarchical competitive learning framework that enables fully autonomous humanoid boxing through structured decision making in a continuous latent strategy space. The interaction between two humanoid agents is formalized as a two-player zero-sum Markov game, where each agent selects high-level motion intents rather than direct motor commands. A shared expert motion decoder executes these intents while preserving physical feasibility and human-like behaviors. Training proceeds through a threestage pipeline: learning a robust low-level motion tracker from human demonstrations (Section 3.2), distilling motion primitives into a bounded continuous latent space that serves as the strategic action space (Section 3.3), and progressively introducing competition via behavioral warmup (Section 3.4) and Latent-Space Neural Fictitious Self-Play (LS-NFSP) (Section 3.5). This design decouples strategic reasoning from low-level control, stabilizes multi-agent learning and facilitates convergence toward approximate Nash equilibria in high-dimensional humanoid combat scenarios. 

## **3.1. Two-player Zero-sum Markov Games** 

We define a two-player zero-sum Markov Game as _M_ = _⟨I, S, {O}_<sup>_i∈I_</sup> _, {Z}_<sup>_i∈I_</sup> _, P, {U}_<sup>_i∈I_</sup> _, γ⟩_ . _I_ = _{_ 1 _,_ 2 _}_ the set of players, _S_ the state space, _{O}_<sup>_i∈I_</sup> the set of player ob- 

servation spaces. We assume the existence of a (possibly implicit) mapping _F_ : _O_<sup>1</sup> _×· · ·×O_<sup>_|I|_</sup> _→S_ that relates joint observations to the underlying environment state. _{Z}_<sup>_i∈I_</sup> the set of player action spaces where _Z_<sup>_i_</sup> _⊂_ R<sup>_d_</sup> and _d_ the dimension size, _P_ : _S × Z_<sup>1</sup> _× · · · × Z_<sup>_|I|_</sup> _→_ ∆( _S_ ) the transition function, _{U}_<sup>_i∈I_</sup> the set of player utility functions and _u_<sup>_i_</sup> _∈U_<sup>_i_</sup> : _S × Z_<sup>1</sup> _× · · · × Z_<sup>_|I|_</sup> _→_ R, _γ ∈_ [0 _,_ 1) the discounted factor. Let each player _i ∈I_ adopt a policy _πz_<sup>_i_:</sup><sup>_Oi→_∆(</sup><sup>_Zi_), and the joint policy by</sup><sup>**_π_**</sup><sup>_z_=(</sup><sup>_π_</sup> _z_<sup>1</sup><sup>_, π_</sup> _z_<sup>2).</sup> The expected return for player _i_ under joint policy **_π_** from state _s ∈S_ satisfies _V_ **_π_**<sup>_i_</sup> _z_<sup>(</sup><sup>_s_) = E</sup> _zt_<sup>_i∼π_</sup> _z_<sup>_i_(</sup><sup>_·|oi_</sup> _t_<sup>)</sup> � _γ_<sup>_t_</sup> _u_<sup>_i_</sup> ( _st, zt_<sup>_i, z_</sup> _t_<sup>_−i_)</sup> _,_ � _t∞_ =0 ���� _s_ 0 = _s_ � (1) 

where _−i_ indicates the players except for player _i_ . In the zero-sum setting _u_<sup>1</sup> = _−u_<sup>2</sup> , the learning objective for each player _i_ is to find an optimal policy _πz_<sup>_i,∗_</sup> that maximizes its expected return against the worst-case opponent policy _πz_<sup>_−i_,</sup> i.e., to solve the following max–min optimization: 


where _J_<sup>_i_</sup> ( **_π_** _z_ ) := E _s∼p_ ( _s_ ) � _V_ **_π_**<sup>_i_</sup> _z_<sup>(</sup><sup>_s_)</sup> �. When all players simultaneously solve the above optimization up to approximation error, the resulting joint policy corresponds to an _ϵ_ -Nash Equilibrium of the Markov game, as defined below. **Definition 3.1** ( _ϵ_ -Nash Equilibrium (Aumann, 1976)) **.** A joint policy **_π_**<sup>_⋆_</sup> _z_<sup>=(</sup><sup>_π_</sup> _z_<sup>_i,⋆, π_</sup> _z_<sup>_−i,⋆_</sup> ) is said to be an _ϵ-Nash Equilibrium_ of a two-player zero-sum Markov game _M_ if no player can unilaterally improve its expected return by deviating from its policy, given that the opponent adheres to **_π_**<sup>_⋆_</sup> _z_<sup>.Formally, for all players</sup><sup>_i∈I_and any alternative</sup> policy _πz_<sup>_i_, it holds that</sup> 


In this work, we frame the boxing task that involves two humanoid robots as a zero-sum Markov game, where a player represents a robot. Rather than acting directly in the high-dimensional motor command space, each player selects actions in a bounded continuous latent space _Z_<sup>_i_</sup> _⊂_ R<sup>_d_</sup> . An action _zt_<sup>_i∈Zi_represents a high-level motion latent dis-</sup> tilled from a large motion corpus. In practice, we constrain _Z_<sup>_i_</sup> to be compact (specifically, _Z_<sup>_i_</sup> = S<sup>_d−_1</sup> ), which restricts exploration to a physically plausible manifold and simplifies strategic interactions in continuous control settings. 

While the preceding content formulate the proposed framework, its practical implementation requires additional design considerations. In the following, we provide a detailed description of a three-stage training pipeline that realizes a hierarchical decision-making process. 

4 

**RoboStriker: Hierarchical Decision-Making for Autonomous Humanoid Boxing** 

## **3.2. Learning Expertise Motion Tracker** 

In the first stage, we learn a robust low-level controller that can faithfully track diverse humanoid boxing motions and provide a stable motor foundation for higher-level strategic learning. The tracker _π_ trk( _at | s_<sup>self</sup> _t , s_<sup>ref</sup> _t_<sup>) is trained using</sup> human motion capture data and shared across all robots, where _s_<sup>self</sup> _t_ = ( _s_<sup>prop</sup> _t , s_<sup>priv</sup> _t_ ). Here, _s_<sup>prop</sup> _t_ denotes a robot’s proprioceptive state at timestep _t_ and _s_<sup>priv</sup> _t_ represents privileged observations that are inaccessible to the robot’s onboard sensors. _s_<sup>ref</sup> _t_ specifies a reference motion goal derived from human motion capture data, which is represented as a time-indexed sequence of full-body humanoid poses and velocities extracted from motion capture dataset _D_ motion. Each _s_<sup>ref</sup> _t_ encodes the root position and orientation, joint angles, and corresponding joint velocities in a canonical humanoid kinematic tree. All motions are temporally aligned and retargeted to the simulated humanoid morphology, enabling consistent tracking across diverse boxing behaviors. The objective maximizes expected tracking rewards _r_ trk over reference trajectories _τ_<sup>ref</sup> , encouraging high-fidelity imitation while maintaining physical plausibility, 


The reward function _r_ trk quantifies the similarity between the simulated humanoid and the reference motion, comprising specific terms for pose alignment, velocity tracking, and control regularization. Details of reward design and data collection are provided in Appendix A. 

## **3.3. Encoding Motion via Topological Latent Distillation** 

To enable learnable strategic control, we project the motion space into a continuous latent space _Z_ . This is achieved via a teacher-student distillation framework (Ross et al., 2011) consisting of an encoder _Eϕ_ , a decoder _Dψ_ , and a stateconditioned latent prior _Pξ_ . The encoder maps observations _ot_ = ( _s_<sup>self</sup> _t , s_<sup>ref</sup> _t_<sup>) to a distribution of latent codes</sup><sup>_zt_, i.e.,</sup> 


In our implementation, we model _Eϕ_ ( _zt_ ) as diagonal Gaussian _N_ ( _zt | µ_<sup>_e_</sup> _t_<sup>_, σ_</sup> _t_<sup>_e_).Then the decoder is trained to recon-</sup> structs the teacher’s actions _at ∼ π_ trk( _· | ot_ ) conditioned on ( _s_<sup>prop</sup> _t , zt_ ) as 


where ˆ _at ∼ Dψ_ ( _· | st_<sup>prop</sup> _, zt_ ). Acknowledging the inherent state-dependency of motion generation, we explicitly learn a state-conditioned latent prior, denoted as _Pξ_ ( _zt | st_<sup>prop</sup> ) = _N_ ( _zt | µ_<sup>_p_</sup> _t_<sup>_, σ_</sup> _t_<sup>_p_).This prior serves to model valid transitions</sup> 

from the current proprioceptive state and constrains the encoder _Eϕ_ ( _zt | ot_ ) via KL-regularization (Hershey & Olsen, 2007), thereby preventing posterior collapse, i.e., 


A key design choice is to enforce the latent space _Z_ to be bounded and continuous. To this end, rather than allowing unconstrained latent representations, we normalize latent codes onto a compact manifold, which restricts motion commands to a physically plausible set and prevents out-of-distribution execution by the decoder. Under this formulation, each latent action _z ∈Z_ fully specifies an motion decision, and we therefore model _Z_ as the effective strategy space of the induced two-player game in Section 3.1. In implementation, we let _z_ satisfies the requirements with normalization as 


thereby constraining the latent representation of _z_ to lie on the unit hypersphere. The total training objective is detailed in Appendix B. 

## **3.4. Behavioral Warmup with Adversarial Priors** 

Considering direct competitive self-play from scratch is unstable due to the lack of basic tactical competence. We therefore introduce a behavioral warmup stage, where agents learn effective striking behaviors against a stationary opponent that strictly maintains a stable standing stance. A learnable residual policy _πθ_ ( _· | s_<sup>goal</sup> _t_ ) is defined as outputs residual latent commands ∆ _zt_ over a fixed behavioral prior _Pξ_<sup>_⊥_from the second stage, ensuring stable and human-like</sup> motions. Then, the complete form of _πz_ is 


To prevent degeneration of motion quality, we regularize the warmup training with AMP (Peng et al., 2021). Specifically, a discriminator _C_ is trained to distinguish motion transitions generated by the agent operating via the frozen decoder _Dψ_ from reference motion data, providing a style-consistency reward _r_ style. Thus, the learning objective is to maximize the expected hybrid return: 


5 

**RoboStriker: Hierarchical Decision-Making for Autonomous Humanoid Boxing** 

where _R_ ( _st, zt_ ) = _w_ task _·r_ task( _st_ )+ _w_ style _·r_ style( _st, st_ +1), _τ_ denotes the trajectory induced by the policy _πz_ and the frozen decoder _Dψ_ . _w_ task and _w_ style is the weighting coefficient. The detail of the task observation _s_<sup>goal</sup> _t_ , the task reward definition and the AMP practice is illustrated in the Appendix C. 

## **3.5. Latent-Space Neural Fictitious Self-Play** 

Building on the behavioral warmup stage, we adopt LatentSpace Neural Fictitious Self-Play (LS-NFSP) to enable competitive co-evolution. Our approach inherit the core principles of Neural Fictitious Self-Play (NFSP) (Heinrich & Silver, 2016), while implementing them over a structured latent action space _Z_ rather than the raw motor space. In LSNFSP, each player is controlled by an independent LS-NFSP agent that learns through simultaneous self-play interactions with its opponents. An LS-NFSP agent interacts with its opponents and records its experience into two buffers, a reinforcement learning dataset _DRL_ that stores transitions and a supervised learning dataset _DSL_ that stores its own best-response behaviors. These two datasets are treated distinctly, corresponding to reinforcement learning and supervised learning objectives, respectively. For each agent, we train an RL policy _πz_<sup>_RL_</sup> via PPO (Schulman et al., 2017) on samples from _DRL_ . In parallel, we train an average policy _π_ ¯ _z_ from _DSL_ with supervised learning, to imitate the agent’s historical best-response behaviors. Concretely, over learning iterations _k_ = 1 _, . . . , K_ , the supervised dataset is incrementally updated as 


Action selection over latent space _Z_ follows an mixture strategy with _η ∈_ [0 _,_ 1). Formally, the mixed strategy is defined as 


and latent actions are sampled as _zt ∼ σ_ ( _· | s_<sup>prop</sup> _t , s_<sup>goal</sup> _t_ ). Under this formulation, _πz_<sup>_RL_</sup> represents an approximate best response to the opponents’ mixed strategies _σ_<sup>_−i_</sup> , while _π_ ¯ _z_ approximates the agent’s long-run average strategy. We summarize the pseudo algorithm of LS-NFSP in Appendix D. 

## **3.6. Theoretical Analysis** 

To analyze learning dynamics in our induced latent game, we first explicitly state a set of modeling assumptions that reflect both our hierarchical motion abstraction and the mathematical requirements for grounding equilibrium analysis in continuous strategy domains. 

**Assumption 3.2** (Bounded Continuous Latent Space) **.** Each agent’s high-level policy _πz_ is built on latent space _Z_ , where _Z ⊂_ R<sup>_d_</sup> is a compact continuous set. In our implementation, _Z_ is the unit hypersphere S<sup>_d−_1</sup> , ensuring boundedness of the latent space. 

**Assumption 3.3** (Well-Defined and Bounded Payoffs) **.** The interaction between agents induces an effective two-player zero-sum game with payoff functions _ui_ ( _zi, z−i_ ) for arbitrary _s ∈S_ , where the expectation is taken over environment stochasticity and low-level policy execution. We assume the payoff functions are bounded and measurable over _S × Z × Z_ . 

**Assumption 3.4** (Approximate Best-Response Updates) **.** At each iteration, each agent updates its latent strategy by approximately best-responding to the empirical distribution of its opponent’s past strategies. The approximation error introduced by finite-horizon rollouts and stochastic optimization is assumed to be bounded. 

Assumption 3.2 and 3.3 are motivated by Glicksberg’s existence theorem (Glicksberg, 1952), which ensures that a mixed-strategy Nash equilibrium exists when each player’s strategy set is non-empty and compact, and the payoff functions are continuous. Beyond these structural conditions on the strategy space, the analysis of self-play dynamics further requires assumptions on the learning process itself. In our framework, high-level policies are optimized via NFSP, which alternates between computing approximate best responses and updating average strategies. We therefore abstract this optimization procedure as an approximate best-response dynamic in the induced latent game (Assumption 3.4). Together, these assumptions establish a coherent analytical setting in which the latent game admits an equilibrium and we can derive approximate convergence results presented below. 

**Proposition 3.5.** _Under Assumptions 3.2 to 3.4, the induced latent interaction admits the standard regularity conditions under which FSP dynamics in continuous zero-sum game are known to approach approximate Nash Equilibrium. Consequently, LS-NFSP will converge to an ϵ-Nash Equilibrium of the induced game, up to bounded approximation error._ 

_Proof._ See Appendix E. 

# **4. Experiment** 

Policy training is performed in Isaac Lab (NVIDIA et al., 2025) on the NVIDIA Omniverse platform, leveraging largescale parallel simulation for efficient data collection. The simulated platform is the Unitree G1 humanoid (Unitree, 2024), featuring 29 degrees of freedom. All experiments are trained on a single NVIDIA RTX 4090 GPU. To improve robustness and encourage the emergence of transferable tactical behaviors, we apply domain randomization (Tobin et al., 2017) to contact friction, link masses, and actuator gains. Our evaluation is designed to answer the following questions: _(i) does the proposed method achieve superior converged performance compared to relevant baselines?_ 

6 

**RoboStriker: Hierarchical Decision-Making for Autonomous Humanoid Boxing** 

_Table 1._ Win Rate (%) of Cross-Playing. Each item the win rate of the row agent against the column agent, averaged over 20 bouts. 

|**Agent \ Opp**|**(1)**|**(2)**|**(3)**|**(4)**|**(5)**|**(6)**|**(7)**|**(8)**|
|---|---|---|---|---|---|---|---|---|
|(1)**Ours LS-NFSP**|-|**68.52 **|**76.24 **|**82.41 **|**84.47 **|**95.38 **|**98.50 **|**100.0**|
|(2) Fictitious SP|-|-|62.35|71.84|75.16|92.11|96.18|99.42|
|(3) Naive SP|-|-|-|68.45|70.38|88.61|94.52|98.53|
|(4) LS-NFSP w/o AMP|-|-|-|-|62.12|82.14|88.37|95.18|
|(5) PPO-Only|-|-|-|-|-|45.24|77.86|82.11|
|(6) Static-Target Specialist|-|-|-|-|-|-|60.33|85.58|
|(7) Naive SP w/o Warmup|-|-|-|-|-|-|-|94.17|
|(8) 29Dof Action-Space SP|-|-|-|-|-|-|-|-|


_Table 2._ Comparison between Action-Space (29-DOF) vs. LatentSpace (Ours) on Tactical and Physical proficiency. 

|**Metric**|**29Dof Action-Space SP **|**Ours LS-NFSP**|
|---|---|---|
|**(a)Tactical Metrics**|||
|Offensive Landing Rate (_ηhit_)_↑_|0_._142_±_0_._05|**0**_._**685**_±_**0**_._**03**|
|Engagement Rate (_ER_)_↑_|0_._315_±_0_._08|**0**_._**824**_±_**0**_._**02**|
|**(b)Physical Metrics**|||
|Base Stability (_BOS_)_↑_|0_._418_±_0_._12|**0**_._**942**_±_**0**_._**01**|
|Torque Smoothness (_TSτ_)_↓_|7_._452_±_1_._211|**0**_._**930**_±_**0**_._**150**|


and _(ii) do the introduced components—including the behavioral warm-up, and AMP—contribute positively to overall performance?_ 

## **4.1. Evaluation Metrics** 

To answer the above question, we propose some metrics to quantify the evaluation of LS-NFSP and baselines from three primary dimensions, which is motivated by some principles in professional boxing training and robust robotics control, as listed as follows. 

**Tactical Proficiency.** The tactical proficiency concentrates on evaluating the offensive precision and active engagement capabilities. Thus, we introduces two metrics as _Offensive Landing Rate_ ( _η_ hit) and _Engagement Rate_ ( _ER_ ). _η_ hit is identified by the proportion of contacts exceeding the force threshold to the total number of offensive attempts. _ER_ acts as a rigorous measure of an agent’s ability to maintain a viable combat posture, effectively penalizing tactical avoidance or non-confrontational movement patterns, the higher the better, and it is calculated as the proportion of the episode duration in which the agent concurrently satisfies two spatial conditions: (1) keep a distance within an effective striking range and (2) ensuring a facing alignment that exceeds a predefined threshold. 

**Physical Stability.** Physical stability is assessed through _Base Orientation Stability_ ( _BOS_ ) and _Torque Smoothness_ ( _TSτ_ ). To ensure a positive correlation with control quality, _BOS_ is defined using an exponential kernels on the angular deviation: _BOS_ = E �exp( _−∥_ **g** base _−_ **g** world _∥_<sup>2</sup> )�, where **g** base and **g** world the gravity vector in the robot’s local frame and the global frame, respectively. A higher _BOS_ 

_Table 3._ Tactical performance comparison focusing on Offensive Landing Rate and Engagement Rate. All metrics are evaluated against the Naive Self-Play (Latent). LS-NFSP outperforms all the baselines. 

|**Methods**<br>**O**|**ffensive Landing Rate**_↑_|**Engagement Rate**_↑_|
|---|---|---|
|**(a) Comparison with Strategic Algorithms**|||
|PPO-Only|0_._231_±_0_._03|0_._495_±_0_._02|
|Naive SP|0_._350_±_0_._04|0_._580_±_0_._05|
|Fictitious SP|0_._420_±_0_._03|0_._650_±_0_._04|
|**Ours LS-NFSP**|**0**_._**685**_±_**0**_._**03**|**0**_._**824**_±_**0**_._**02**|
|**(b) Impact of Latent Space**|||
|29Dof Action-Space SP|0_._142_±_0_._05|0_._315_±_0_._08|
|**Ours LS-NFSP**|**0**_._**685**_±_**0**_._**03**|**0**_._**824**_±_**0**_._**02**|
|**(c) Impact of Curriculum Design**|||
|Static-Target Specialist|0_._210_±_0_._04|0_._450_±_0_._06|
|SP w/o Warmup|0_._050_±_0_._02|0_._120_±_0_._05|
|**Ours LS-NFSP**|**0**_._**685**_±_**0**_._**03**|**0**_._**824**_±_**0**_._**02**|
|**(d) Impact of Stylistic Constraints**|||
|LS-NFSP w/o AMP|0_._490_±_0_._03|0_._720_±_0_._05|
|**Ours LS-NFSP**|**0**_._**685**_±_**0**_._**03**|**0**_._**824**_±_**0**_._**02**|


indicates a superior ability to maintain an upright posture under competitive perturbations. _TSτ_ measures the magnitude of high-frequency oscillations in motor commands, calculated as the mean absolute change in joint torques across consecutive control steps: _TSτ_ = E [ _∥τt − τt−_ 1 _∥_ ]. A lower _TSτ_ value represents more hardware-friendly execution and reduced mechanical wear. 

**Stylistic Authenticity.** The Stylistic Authenticity of the emergent behaviors is evaluated via qualitative visual inspection. Instead of relying on a singular numerical score, we provide a comparative analysis of simulation snapshots to assess the human-likeness of the motions. This includes identifying key boxing maneuvers such as slips, counters, and rhythmic footwork, while ensuring the absence of unnatural joint configurations or physically unsustainable postures that often characterize non-constrained reinforcement learning policies. 

## **4.2. Cross-Playing Evaluation** 

We answer the first question by conducting cross-play between LS-NFSP and involved baselines described in Appendix F. Table 1 presents the win rates over all the involved methods, which shows that LS-NFSP outperforms all the baselines. The most critical insight is the superiority of performing competitive self-play within a structured latent manifold. We notice that the LS-NFSP agent dominates 29Dof Action-Space SP agent with a 100.00% win rate and also performs superior tactical and physical proficiency (Table 2), proving that decoupling balance maintenance from tactical exploration is a fundamental prerequisite for competitive learning in high-dimensional humanoid combat. And for the comparison between self-play methods with latent space, LS-NFSP also outperforms the other methods, in the result of Fictitious SP of 68.52% and Naive SP 

7 

**RoboStriker: Hierarchical Decision-Making for Autonomous Humanoid Boxing** 


_Figure 3._ t-SNE visualization of the 32-dimensional latent manifold, illustrating the structured semantic clustering of combat primitives and their topological relationships that facilitate stable, compositional behavioral transitions in the hierarchical LS-NFSP framework. 

of 76.24%, confirming that the integration of NFSP effectively mitigates policy cycling to produce a more robust best response. The necessity of each training stage is further validated by the substantial performance gaps against Direct-SP of 98.50% and Static-Target Specialist of 95.38%, which fail to respectively overcome reward sparsity and reactive dynamic opponents. Additionally, the No-AMP variant exhibits reduced tactical efficiency of 82.41% win rate against Ours due to its non-standardized movement patterns. Finally, the significant win rate against the PPO-Only baseline of 84.47% underscores that competitive interaction is the indispensable driver of emergent combat behaviors. 

## **4.3. Ablation Study** 

To answer the second question, we conduct ablation study from two perspectives, i.e., whether the strategy prior, warmup and AMP can benefit the policy training. 

**Strategy Priors.** Table 3 (a) underscores the necessity of both competitive strategy priors in achieving elite boxing proficiency. LS-NFSP demonstrates superior tactical performance by achieving _η_ hit = 0 _._ 685 and _ER_ = 0 _._ 824, which significantly outperforms baselines. 

**Warm-Up Training.** As shown in Table 3(c), the necessity of leveraging warm-up is further evidenced by the collapse of the Direct-SP variant. Despite competitive access, it achieves a negligible _η_ hit = 0 _._ 050, proving its inability to overcome the inefficiency due to reward sparsity settings. 

**Adversarial Motion Prior.** We further evaluate the impact of stylistic constraints rigorously as in Table 3(d). While the variant achieves _ER_ = 0 _._ 720, its _η_ hit drops 


_Figure 4._ Mujoco visualization of the LS-NFSP and the one without AMP. 

sharply to 0.490. This discrepancy reveals that, without AMP, the agent can approach the opponent but executes erratic strikes that difficult to contact opponent effectively, as Figure 4 demonstrates that the policy trained without AMP lacks physical authenticity. Ultimately, these results prove that the synergy of NFSP-driven exploration and AMPguided movement is essential for producing a controller that is both strategically dominant and physically authentic. 

## **4.4. Analysis of the Learned Latent Space** 

To investigate the underlying structure of the latent skills, we perform a joint t-SNE (Maaten & Hinton, 2008) analysis on the generated embeddings, as illustrated in Figure 3. The visualization reveals a highly structured manifold with a distinct topological arrangement: there is a clear separation between the pure _Move_ (purple) and pure _Strike_ (pink) clusters. This demarcation indicates that the latent space successfully disentangles stable locomotion dynamics from highmomentum offensive maneuvers. Crucially, _Move+Strike_ (blue) embeddings occupy the intermediate space, exhibiting significant overlap with both _Move_ and _Strike_ regions. This dual overlap suggests that the _Move+Strike_ mode functions as a topological bridge, seamlessly connecting the two distinct primitives. Such a structure provides empirical evidence of the latent space’s compositional nature, enabling the LS-NFSP framework to smoothly interpolate between navigation and combat. This allows the agent to initiate attacks dynamically while moving, without suffering from the discontinuity or instability typically associated with switching between disjoint control modes. 

# **5. Conclusion** 

We propose a hierarchical competitive framework for humanoid interaction that integrates latent-space control with Neural Fictitious Self-Play (LS-NFSP). By decoupling highlevel tactical strategy from low-level balance control via a pre-trained latent manifold, our approach ensures physical stability while enabling the emergence of sophisticated boxing maneuvers like slip-and-counter tactics. Experimental results from an 8 _×_ 8 cross-play tournament, supported by 

8 

**RoboStriker: Hierarchical Decision-Making for Autonomous Humanoid Boxing** 

qualitative snapshots and t-SNE analysis, demonstrate that LS-NFSP consistently outperforms baselines in both competitive win rate and stylistic authenticity. Ultimately, this work proves that the synergy of hierarchical latent representations and competitive self-play provides a robust and scalable solution for achieving tactical intelligence in highdimensional humanoid robotics. 

# **References** 

- Araujo, J. P., Ze, Y., Xu, P., Wu, J., and Liu, C. K. Retargeting matters: General motion retargeting for humanoid motion tracking, 2025. URL https://arxiv.org/ abs/2510.02252. 

- Aumann, R. J. Agreeing to disagree. _The Annals of Statistics_ , 4(6):1236–1239, 1976. 

- Balduzzi, D. and Racaniere, S. The mechanics of n-player differentiable games. In _ICML_ , 2018. 

- Brown, G. W. Iterative solution of games by fictitious play. _Act. Anal. Prod Allocation_ , 13(1):374, 1951. 

- Chen, Z., Ji, M., Cheng, X., Peng, X., Peng, X. B., and Wang, X. Gmt: General motion tracking for humanoid whole-body control. _arXiv preprint arXiv:2506.14770_ , 2025. 

- Davidson, T. R., Falorsi, L., De Cao, N., Kipf, T., and Tomczak, J. M. Hyperspherical variational auto-encoders. _arXiv preprint arXiv:1804.00891_ , 2018. 

- Gleicher, M. Retargetting motion to new characters. In _Proceedings of the 25th annual conference on Computer graphics and interactive techniques_ , pp. 33–42, 1998. 

- Glicksberg, I. L. A further generalization of the kakutani fixed point theorem, with application to nash equilibrium points. _Proceedings of the American Mathematical Society_ , 3(1):170–174, 1952. 

- Heinrich, J. and Silver, D. Deep reinforcement learning from self-play in imperfect-information games. _arXiv preprint arXiv:1603.01121_ , 2016. 

- Hernandez, D., Denamganaï, K., Gao, Y., York, P., Devlin, S., Samothrakis, S., and Walker, J. A. A generalized framework for self-play training. In _2019 IEEE Conference on Games (CoG)_ , pp. 1–8. IEEE, 2019. 

- Hershey, J. R. and Olsen, P. A. Approximating the kullback leibler divergence between gaussian mixture models. In _2007 IEEE International Conference on Acoustics, Speech and Signal Processing-ICASSP’07_ , volume 4, pp. IV–317. IEEE, 2007. 

- Holden, D., Saito, J., and Komura, T. A deep learning framework for character motion synthesis and editing. _ACM Transactions on Graphics (ToG)_ , 35(4):1–11, 2016. 

- Kajita, S., Kanehiro, F., Kaneko, K., Fujiwara, K., Harada, K., Yokoi, K., and Hirukawa, H. Biped walking pattern generation by using preview control of zero-moment point. In _2003 IEEE international conference on robotics and automation (Cat. No. 03CH37422)_ , volume 2, pp. 1620–1626. IEEE, 2003. 

- Kuindersma, S., Deits, R., Fallon, M., Valenzuela, A., Dai, H., Permenter, F., Koolen, T., Marion, P., and Tedrake, R. Optimization-based locomotion planning, estimation, and control design for the atlas humanoid robot. _Autonomous robots_ , 40(3):429–455, 2016. 

- Lanctot, M., Zambaldi, V., and Gruslys, A. A unified gametheoretic approach to multiagent reinforcement learning. In _NeurIPS_ , 2017. 

- Liao, Q., Truong, T. E., Huang, X., Gao, Y., Tevet, G., Sreenath, K., and Liu, C. K. Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion, 2025. URL https://arxiv.org/abs/ 2508.08241. 

- Luo, Z., Cao, J., Merel, J., Winkler, A., Huang, J., Kitani, K., and Xu, W. Universal humanoid motion representations for physics-based control. _arXiv preprint arXiv:2310.04582_ , 2023. 

- Maaten, L. v. d. and Hinton, G. Visualizing data using t-sne. _Journal of machine learning research_ , 9(Nov): 2579–2605, 2008. 

- Mertikopoulos, P. and Zhou, Z. Learning in games with continuous action sets and unknown payoff functions. _Mathematical Programming_ , 173(1):465–507, 2019. 

- NVIDIA, :, Mittal, M., Roth, P., Tigue, J., Richard, A., Zhang, O., Du, P., Serrano-Muñoz, A., Yao, X., Zurbrügg, R., Rudin, N., Wawrzyniak, L., Rakhsha, M., Denzler, A., Heiden, E., Borovicka, A., Ahmed, O., Akinola, I., Anwar, A., Carlson, M. T., Feng, J. Y., Garg, A., Gasoto, R., Gulich, L., Guo, Y., Gussert, M., Hansen, A., Kulkarni, M., Li, C., Liu, W., Makoviychuk, V., Malczyk, G., Mazhar, H., Moghani, M., Murali, A., Noseworthy, M., Poddubny, A., Ratliff, N., Rehberg, W., Schwarke, C., Singh, R., Smith, J. L., Tang, B., Thaker, R., Trepte, M., Wyk, K. V., Yu, F., Millane, A., Ramasamy, V., Steiner, R., Subramanian, S., Volk, C., Chen, C., Jawale, N., Kuruttukulam, A. V., Lin, M. A., Mandlekar, A., Patzwaldt, K., Welsh, J., Zhao, H., Anes, F., Lafleche, J.-F., MoënneLoccoz, N., Park, S., Stepinski, R., Gelder, D. V., Amevor, C., Carius, J., Chang, J., Chen, A. H., de Heras Ciechomski, P., Daviet, G., Mohajerani, M., von Muralt, J., Reutskyy, V., Sauter, M., Schirm, S., Shi, E. L., Terdiman, P., 

9 

**RoboStriker: Hierarchical Decision-Making for Autonomous Humanoid Boxing** 

- Vilella, K., Widmer, T., Yeoman, G., Chen, T., Grizan, S., Li, C., Li, L., Smith, C., Wiltz, R., Alexis, K., Chang, Y., Chu, D., Fan, L. J., Farshidian, F., Handa, A., Huang, S., Hutter, M., Narang, Y., Pouya, S., Sheng, S., Zhu, Y., Macklin, M., Moravanszky, A., Reist, P., Guo, Y., Hoeller, D., and State, G. Isaac lab: A gpu-accelerated simulation framework for multi-modal robot learning, 2025. URL https://arxiv.org/abs/2511.04831. 

- Peng, X. B., Abbeel, P., Levine, S., and Van de Panne, M. Deepmimic: Example-guided deep reinforcement learning of physics-based character skills. _ACM Transactions On Graphics (TOG)_ , 37(4):1–14, 2018. 

- Peng, X. B., Ma, Z., Abbeel, P., Levine, S., and Kanazawa, A. Amp: Adversarial motion priors for stylized physicsbased character control. _ACM Transactions on Graphics (ToG)_ , 40(4):1–20, 2021. 

- Peng, X. B., Guo, Y., Halper, L., Levine, S., and Fidler, S. Ase: Large-scale reusable adversarial skill embeddings for physically simulated characters. _ACM Transactions On Graphics (TOG)_ , 41(4):1–17, 2022. 

- Petrovich, M., Black, M. J., and Varol, G. Tmr: Textto-motion retrieval using contrastive 3d human motion synthesis. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pp. 9488–9497, 2023. 

- Ramazi, P. and Cao, M. Global convergence for replicator dynamics of repeated snowdrift games. _IEEE Transactions on Automatic Control_ , 66(1):291–298, 2020. 

- Rosen, J. B. Existence and uniqueness of equilibrium points for concave n-person games. _Econometrica_ , 1965. 

- Ross, S., Gordon, G. J., and Bagnell, J. A. A reduction of imitation learning and structured prediction to no-regret online learning, 2011. URL https://arxiv.org/ abs/1011.0686. 

- Samuel, A. L. Some studies in machine learning using the game of checkers. _IBM Journal of research and development_ , 3(3):210–229, 1959. 

- Schulman, J., Wolski, F., Dhariwal, P., Radford, A., and Klimov, O. Proximal policy optimization algorithms, 2017. URL https://arxiv.org/abs/ 1707.06347. 

- Silver, D., Schrittwieser, J., Simonyan, K., Antonoglou, I., Huang, A., Guez, A., Hubert, T., Baker, L., Lai, M., Bolton, A., et al. Mastering the game of go without human knowledge. _nature_ , 550(7676):354–359, 2017. 

- Sutton, R. S., Barto, A. G., et al. _Reinforcement learning: An introduction_ , volume 1. MIT press Cambridge, 1998. 

- Tessler, C., Kasten, Y., Guo, Y., Mannor, S., Chechik, G., and Peng, X. B. Calm: Conditional adversarial latent models for directable virtual characters. In _ACM SIGGRAPH 2023 Conference Proceedings_ , pp. 1–9, 2023. 

- Tobin, J., Fong, R., Ray, A., Schneider, J., Zaremba, W., and Abbeel, P. Domain randomization for transferring deep neural networks from simulation to the real world, 2017. URL https://arxiv.org/abs/1703.06907. 

- Unitree. Unitree g1 humanoid agent ai avatar, 2024. URL https://www.unitree.com/g1. 

- Vinyals, O., Babuschkin, I., Czarnecki, W. M., Mathieu, M., Dudzik, A., Chung, J., Choi, D. H., Powell, R., Ewalds, T., Georgiev, P., et al. Grandmaster level in starcraft ii using multi-agent reinforcement learning. _nature_ , 575 (7782):350–354, 2019. 

- Xsens Technologies. Xsens mvn: Inertial motion capture system, 2024. URL https://www.xsens.com/ motion-capture. Accessed: 2026-01-28. 

- Yamane, K., Kuffner, J. J., and Hodgins, J. K. Synthesizing animations of human manipulation tasks. In _ACM SIGGRAPH 2004 Papers_ , pp. 532–539. 2004. 

- Yin, K., Zou, S., Ge, Y., and Tian, Z. Tri-modal motion retrieval by learning a joint embedding space. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 1596–1605, 2024. 

- Yin, K., Zeng, W., Fan, K., Dai, M., Wang, Z., Zhang, Q., Tian, Z., Wang, J., Pang, J., and Zhang, W. Unitracker: Learning universal whole-body motion tracker for humanoid robots. _arXiv preprint arXiv:2507.07356_ , 2025. 

- Zeng, W., Lu, S., Yin, K., Niu, X., Dai, M., Wang, J., and Pang, J. Behavior foundation model for humanoid robots, 2025. URL https://arxiv.org/ abs/2509.13780. 

- Zhang, J., Zhang, Y., Cun, X., Zhang, Y., Zhao, H., Lu, H., Shen, X., and Shan, Y. Generating human motion from textual descriptions with discrete representations. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pp. 14730–14740, 2023. 

- Zhang, Z., Guo, J., Chen, C., Wang, J., Lin, C., Lian, Y., Xue, H., Wang, Z., Liu, M., Lyu, J., et al. Track any motions under any disturbances. _arXiv preprint arXiv:2509.13833_ , 2025. 

- Zinkevich, M., Johanson, M., Bowling, M., and Piccione, C. Regret minimization in games with incomplete information. _Advances in neural information processing systems_ , 20, 2007. 

10 

**RoboStriker: Hierarchical Decision-Making for Autonomous Humanoid Boxing** 

# **A. Learning an Expert Motion Tracker** 

This section supplements Section 3.2 with implementation details for learning an expert motion tracker, including motion dataset collection and processing, as well as the reinforcement learning setup used to train the tracking policy. 

## **A.1. Motion Dataset Collection and Processing** 

We collect a diverse set of human boxing motions recorded by professional boxers using an Xsens motion capture system (Xsens Technologies, 2024). The dataset consists of 46 original motion clips with a total duration of approximately 14 minutes, captured at a frequency of 50 Hz. These clips cover a wide range of boxing behaviors, including offensive strikes, defensive maneuvers, footwork, and transitional movements. To increase data diversity and improve generalization, we augment the dataset through left-right mirroring, effectively doubling the number of available motion sequences. 

The captured human motions are retargeted to the Unitree G1 humanoid (Unitree, 2024) morphology following the Generalized Motion Retargeting (GMR) framework (Araujo et al., 2025). Through this retargeting process, we obtain physically realizable reference trajectories dataset _D_ motion that preserve the stylistic characteristics and temporal structure of the original boxing motions. 

## **A.2. Reinforcement Learning Settings and Training Details** 

**State, Observation and Action Spaces.** The state of the tracking policy is defined as _s_<sup>self</sup> _t_ = ( _s_<sup>prop</sup> _t , s_<sup>priv</sup> _t_ ), where _s_<sup>prop</sup> _t_ denotes the proprioceptive state, including base angular velocities, relative joint positions, and joint velocities, and _s_<sup>priv</sup> _t_ denotes privileged information, including base linear velocities, global base position and orientation, body link poses, and contact states. The observation **o** trk _∈O_ consists of three components: (i) the proprioceptive state _s_<sup>prop</sup> _t_ ; (ii) the reference motion state _s_<sup>ref</sup> _t ∼ τ_<sup>ref</sup> , which provides target full-body poses and base velocities over the current and the next _K_ = 3 timesteps; and (iii) the previous action _at−_ 1 to promote temporal smoothness. The action _at ∈A_ corresponds to target joint positions for the 29-degree-of-freedom Unitree G1 humanoid (Unitree, 2024), which are tracked by a low-level PD controller. 

**Reward Function.** The tracking reward _r_ trk is designed to encourage accurate imitation of reference boxing motions and is defined as a weighted sum of exponential tracking terms: 


where _X_ = p _,_ o _,_ bp _,_ bo _,_ lv _,_ av and each term is defined as _rx_ = exp( _−∥_ err _x∥_<sup>2</sup> _/σx_<sup>2)</sup><sup>_._Here,</sup><sup>_r_pand</sup><sup>_r_omeasureglobal</sup> root position and orientation tracking errors, _r_ bp and _r_ bo measure relative body link pose errors, and _r_ lv and _r_ av penalize deviations in linear and angular velocities. The regularization term _r_ reg penalizes excessive action rate, joint limit violations, and undesired self-collisions or ground contacts. The weights _wx_ and scaling factors _σx_ are provided in Table 4. 

_Table 4._ Reward Terms, Weights and Scaling Factor for Motion Tracker. 

|**Reward Terms**|**Weights**_w_|**Scaling Factor**_σ_|
|---|---|---|
|Root Position_r_p|0_._5|0_._3|
|Root Orientation_r_o|0_._5|0_._4|
|Body Position_r_bp|1_._0|0_._3|
|Body Orientation_r_bo|1_._0|0_._4|
|Body Linear Velocity_r_lv|1_._0|1_._0|
|Body Angular Velocity_r_av|1_._0|3_._14|


**Early Termination.** To accelerate training and prevent the policy from exploring unstable or physically unfeasible states, we follow (Peng et al., 2018) to implement an early termination mechanism _T_ . An episode is terminated if any of the following conditions are met: 1). **Pose Collapse:** The vertical distance between the robot’s base and its reference height falls below a threshold of 0 _._ 25 m, or the base orientation deviation exceeds 0 _._ 8 rad. 2). **End-Effector Violation:** The vertical 

11 

**RoboStriker: Hierarchical Decision-Making for Autonomous Humanoid Boxing** 

position of key end-effectors, specifically the ankles and wrists, deviates from the reference height by more than 0 _._ 25 m. 3). **Temporal Limit:** The maximum episode duration of 10 _._ 0 seconds is reached. 

By combining structured reward shaping, early termination, and massive-scale parallel simulation in Isaac Lab (NVIDIA et al., 2025), the low-level tracking policy _π_ trk learns robust and physically consistent motor skills, which form the foundation for subsequent latent skill distillation. 

# **B. Encoding Motion via Topological Latent Distillation** 

This section provides implementation details for the latent motion distillation framework introduced in Section 3.3 

**Distillation Architecture.** We adopt a student–teacher paradigm to distill the low-level tracking policy _π_ trk into a compact latent interface. During training, the teacher policy is fixed, and a student model consisting of an encoder _Eϕ_ , a decoder _Dψ_ , and a state-conditioned prior network _Pξ_ is jointly optimized. At each timestep, the encoder maps privileged observations _ot_ = ( _s_<sup>self</sup> _t , s_<sup>ref</sup> _t_<sup>) to a latent distribution</sup><sup>_qϕ_(</sup><sup>_zt| ot_).A latent code</sup><sup>_zt_is sampled and provided to the decoder, which predicts</sup> target joint actions conditioned on the proprioceptive state. 

**Training Objective.** The student is trained to reconstruct the teacher’s actions while learning a structured latent distribution. The reconstruction loss is defined as 


where _at ∼ π_ trk( _· | ot_ ), _zt ∼ Eϕ_ ( _· | ot_ ), ˆ _at ∼ Dψ_ ( _st_<sup>prop</sup> _, zt_ ) . To regularize the latent space, we impose a KL divergence between the encoder posterior and the state-conditioned prior: 


The prior loss ensures that the prior network captures the semantic structure of the motion primitives. During the competitive stage in self-play, this learned prior provides a critical reference for the high-level policy, where a KL penalty is applied to prevent the strategy from deviating into physically unstable regions of the action space. The total loss is given by 


where _λprior_ = 0 _._ 001. This dual optimization ensures that the student not only recovers the motor control expertise of the teacher but also constructs a structured, prior-conditioned manifold ready for competitive co-evolution. 

# **C. Behavioral Warmup with Adversarial Priors** 

This section gives implementation details for the behavioral wamup training. We also describe how Adversarial Motion Priors (AMP) are incorporated to regularize behaviors toward the motion-capture distribution and preserve human-like boxing style. 

## **C.1. Goal-Oriented Observation for Autonomous Boxing** 

Different from previous tracking-based task settings, the observation of the autonomous boxing task does not contain any explicit motion commands. Instead, the residual policy _πθ_ relies on goal-oriented spatial information to guide decisionmaking. The task observation _s_<sup>goal</sup> consists of two complementary components: (1) offensive target information and (2) defensive threat information. 

**Offensive Target Observation.** The offensive target observation encodes the relative positions of the ego agent’s left and right fists with respect to the opponent’s torso, represented in the ego-centric coordinate frame. Let **p**<sup>ego</sup> _l ,_ **p**<sup>ego</sup> _r ∈_ R<sup>3</sup> denote the world-frame positions of the ego agent’s wrists, **p**<sup>opp</sup> _t ∈_ R<sup>3</sup> the position of the opponent’s torso, and **q**<sup>ego</sup> the ego root orientation. The relative vectors are defined as 


**RoboStriker: Hierarchical Decision-Making for Autonomous Humanoid Boxing** 

which are further transformed into the ego-centric frame via 


where **R** ( _·_ ) denotes the rotation matrix induced by the quaternion. 

This transformation removes global orientation dependency and ensures rotational invariance of the observation. As a result, the offensive component provides direct and physically interpretable geometric information for guiding accurate, distance-aware striking behaviors. 

**Defensive Target Observation.** The defensive target observation characterizes the relative positions of the opponent’s left and right fists with respect to the ego agent’s torso, also expressed in the ego-centric frame. Let **p**<sup>opp</sup> _l ,_ **p**<sup>opp</sup> _r ∈_ R<sup>3</sup> denote the opponent’s wrist positions and **p**<sup>ego</sup> _t ∈_ R<sup>3</sup> the ego torso position. The defensive vectors are computed as 


and rotated into the local frame in the same manner: 


This component enables the policy to perceive incoming attack trajectories independently of global pose, facilitating anticipatory defense, evasive maneuvers, and counter-attacking strategies. 

= Together, the offensive and defensive observations form a compact yet expressive goal representation _s_<sup>goal</sup> (˜ **v** _l_<sup>off</sup><sup>_,_˜</sup><sup>**v**</sup> _r_<sup>off</sup><sup>_,_˜</sup><sup>**v**</sup> _l_<sup>def</sup> _,_ ˜ **v** _r_<sup>def) that supports coordinated attack–defense behaviors in autonomous humanoid boxing.</sup> 

## **C.2. Adversarial Motion Prior** 

To preserve human-like motion quality, we follow (Peng et al., 2018) to use a discriminator _C_ to distinguish whether the state originates from mocap dataset _D_ motion or the agent formed by the policy _πz_ and the frozen decoder _Dψ_ . Specifically, we first construct the AMP observation _ot_<sup>disc</sup> to better capture the style of the mocap data. The observation _ot_<sup>disc</sup> includes the local rotation and velocity of each joint, along with the angular velocities of the base. Observation transitions from the agent and those sampled from the mocap data are fed separately to the discriminator. We label the transitions from the mocap data as _real_ and those from the agent as _fake_ . The goal of the discriminator is to classify these inputs correctly: when mocap transitions are provided, the output should approach 1, whereas transitions from the agent should produce outputs closer to -1. As a result, the objective function can be formulated as follows: 


Since discriminators often suffer from mode collapse, we follow AMP (Peng et al., 2018) by applying a gradient penalty to the mocap data transitions to ensure stability. This can be formulated as follows: 


The final objective function to train the discriminator is formulated as follows: 


13 

**RoboStriker: Hierarchical Decision-Making for Autonomous Humanoid Boxing** 

## **C.3. Reward Formulation** 

To encourage effective engagement, active striking, and robust defensive behaviors in humanoid combat, we design a hierarchical and compositional reward function. The overall reward integrates geometric alignment, locomotion, contactbased interaction, and terminal dominance, enabling stable learning under self-play settings. 

**Overall Objective.** The warm-up reward is defined as a weighted combination of task-oriented and style-oriented objectives: 


where _r_ style encourages motion naturalness, and _r_ task focuses on combat effectiveness. 

**Task-Level Decomposition.** The task reward is formulated as 


where each component captures a distinct aspect of humanoid combat behavior. 

**Hierarchical Design.** The reward structure follows a layered principle: (i) geometric alignment and distance shaping, (ii) velocity-oriented locomotion, and (iii) contact-based striking behaviors. This hierarchy stabilizes optimization and mitigates reward exploitation. 

**Facing Alignment Reward.** We encourage the agent to orient its torso toward the opponent target. Let **p** _e_ and **p** _t_ denote the ego root position and the opponent target position. The horizontal target direction in the world frame is defined as 


where _πxy_ ( _·_ ) projects a vector onto the horizontal plane. Let _Re ∈ SO_ (3) be the rotation matrix corresponding to **q** _e_ . The direction expressed in the ego local frame is 


The facing reward is defined as 


where _dx_ represents the forward component of the target direction, and _σ_ face controls the sharpness. 

**Velocity Reward.** We reward locomotion along the line of sight to the opponent. Let **v** _e_ denote the ego root linear velocity and **d** 2 _D_ the normalized horizontal target direction: 


The projected velocity along the target direction is 


Given the desired approaching speed _v_ tar, we define the velocity error 


and the reward 


where _σ_ vel determines the scaler. 

14 

**RoboStriker: Hierarchical Decision-Making for Autonomous Humanoid Boxing** 

**Distance Reward.** To prevent passive exploitation, we introduce a velocity-gated distance reward term. Let **v** _wi_ be the velocity of wrist _i_ and 


be the unit vector from wrist _i_ to target torso link. The projected punching speed is 


A smooth gating function is defined as 


where _v_ th is the speed threshold and _α_ controls steepness. The active hitting reward is 


with _di_ represents the distance from wrist _i_ to the opponent torso. 

**Hit Reward.** In adversarial humanoid control, naive contact-based rewards often lead to degenerate behaviors such as body pushing, leaning, or passive collision, rather than deliberate punching actions. To address this issue, we design an offensive punch hit reward that jointly considers kinematic intent, geometric alignment, and physical contact. Let **v** _wi_ be the velocity of wrist _i_ and **v** _t_ be the velocity of the torso link. We define the relative punching velocities as: 


for _i_ = _l_ or _r_ . These quantities represent the local striking motion of each fist with respect to the robot’s body. When the agent only translates forward, the relative velocities turns to 0. The effective attack speed is obtained by projecting relative velocity onto the attack direction: 


Let **F**<sup>opp</sup> _t_ be the contact force on opponent’s torso link, **F**<sup>ego</sup> _i_ be the contact forces on left or right wrists. We define binary contact indicators: 


the valid hit signals for any wrist is: 


This hit reward is a high-level sparse reward granted for landing a clean, significant blow on the opponent, incentivizing decisive offensive actions beyond simple contact. 

**Style Reward.** The style reward _r_ style is derived from the discriminator’s output to anchor the agent’s behavior within the reference motion distribution: 


**Reward Scheduling.** To ensure a stable transition from imitation to task execution, we implement a dynamic weight schedule. During the initial warmup epochs, the agent is driven primarily by _r_ style to master stable bipedal locomotion and boxing postures. Subsequently, the task reward weight _w_ task is phased in, allowing the agent to optimize strike precision while adhering to the geometric and stylistic constraints imposed by the learned manifold and the AMP prior. 

# **D. Latent-Space Neural Fictitious Self-Play** 

This section includes the pseudo code in Algorithm 1 and the training details of LS-NFSP. 

15 

**RoboStriker: Hierarchical Decision-Making for Autonomous Humanoid Boxing** 

## **Algorithm 1** Latent-Space Neural Fictitious Self-Play (LS-NFSP) 

**Require:** Two-player zero-sum game environment _M_ , anticipatory parameter _η ∈_ [0 _,_ 1], horizon _T_ **Require:** Best-response (RL) policies _{πz,θ_<sup>RL</sup> _i_<sup>_}i∈{_1</sup><sup>_,_2</sup><sup>_}_, average policies</sup><sup>_{π_¯</sup><sup>_z,ϕ_</sup> _i_<sup>_}i∈{_1</sup><sup>_,_2</sup><sup>_}_</sup> **Require:** On-policy rollout buffers _{D_ RL<sup>_i}i∈{_1</sup><sup>_,_2</sup><sup>_}_, reservoir buffers</sup><sup>_{D_</sup> SL<sup>_i}i∈{_1</sup><sup>_,_2</sup><sup>_}_</sup> 1: **for** iteration _k_ = 1 _,_ 2 _, . . ._ **do** 2: Reset _M_ and observe _o_<sup>1</sup> 1<sup>_, o_2</sup> 1<sup>{</sup><sup>_oi_</sup> _t_<sup>can include (</sup><sup>_s_</sup> _t_<sup>prop</sup><sup>_,i_</sup> _, s_<sup>goal</sup> _t_<sup>_,i_</sup> )} 3: **for** _t_ = 1 _,_ 2 _, . . . , T_ **do** 4: **for all** players _i ∈{_ 1 _,_ 2 _}_ **do** 5: Sample mode _mi ∼_ Bernoulli( _η_ ) { _mi_ =1: best-response; _mi_ =0: average} 6: **if** _mi_ = 1 **then** 7: Sample latent action _zt_<sup>_i∼π_</sup> _z,θ_<sup>RL</sup> _i_<sup>(</sup><sup>_· | o_</sup> _t_<sup>_i_)</sup> 8: Insert ( _o_<sup>_i_</sup> _t_<sup>_, z_</sup> _t_<sup>_i_) into</sup><sup>_D_</sup> SL<sup>_i_via reservoir sampling</sup> 9: **else** 10: Sample latent action _zt_<sup>_i∼π_¯</sup><sup>_z,ϕ_</sup> _i_<sup>(</sup><sup>_· | o_</sup> _t_<sup>_i_)</sup> 11: **end if** 12: **end for** 13: Step environment with joint latent action ( _zt_<sup>1</sup><sup>_, z_</sup> _t_<sup>2); receive rewards (</sup><sup>_r_</sup> _t_<sup>1</sup><sup>_, r_</sup> _t_<sup>2) and next obs (</sup><sup>_o_1</sup> _t_ +1<sup>_, o_2</sup> _t_ +1<sup>)</sup> 14: **for all** players _i ∈{_ 1 _,_ 2 _}_ **do** 15: Append transition ( _o_<sup>_i_</sup> _t_<sup>_, z_</sup> _t_<sup>_i, r_</sup> _t_<sup>_i, oi_</sup> _t_ +1<sup>) to</sup><sup>_D_</sup> RL<sup>_i_</sup> 16: **end for** 17: **end for** 18: **for all** players _i ∈{_ 1 _,_ 2 _}_ **do** 19: Update _θi_ with PPO on _D_ RL<sup>_i_</sup> 20: Update _ϕi_ by minimizing _L_ SL = E( _o,z_ ) _∼D_ SL _i_ � _∥π_ ¯ _z,ϕi_ ( _o_ ) _− z∥_<sup>2�</sup> 21: **end for** 22: **end for** 23: **return** Average policies _{π_ ¯ _z,ϕi}i∈{_ 1 _,_ 2 _}_ 

## **D.1. Dual-Policy Architecture.** 

To implement fictitious play, each agent maintains a dual-policy system. This system includes a best response policy ( _πz_<sup>_RL_</sup> ) and a average policy ( _π_ ¯ _z_ ). The best response policy ( _πz_<sup>_RL_</sup> ) is an on-policy actor optimized via PPO (Schulman et al., 2017) to exploit the opponent’s current average strategy. The average policy ( _π_ ¯ _z_ ) is a supervised learning network that approximates the agent’s historical distribution of best-response behaviors, acting as a stable strategic anchor. 

## **D.2. Reservoir-Based Strategy Buffer.** 

To ensure that the average policy represents a uniform sampling of the agent’s behavioral history, we utilize a reservoir sampling mechanism. Each agent stores its latent-space trajectories ( _s_<sup>prop</sup> _t , s_<sup>goal</sup> _t , zt_ ) in a buffer _DSL_ of capacity _K_ . For every new experience _n > K_ , the sample replaces a random existing entry with probability _P_ = _K/n_ . This prevents the average strategy from being biased toward recent iterations and preserves tactical diversity. 

## **D.3. Reward Formulation.** 

Transitioning from the single-agent warmup to a zero-sum game requires an expanded task reward _r_ expand, which incorporates competitive outcome conditions and defensive necessity. In addition to the basic striking and facing rewards, we introduce the following competitive terms: 


**Strike Force Reward.** We encourage effective physical impacts using contact forces. Let **F**<sup>opp</sup> and **F**<sup>ego</sup> denote the net contact forces measured on the opponent and ego torso body, respectively. The reward is defined as 


16 

**RoboStriker: Hierarchical Decision-Making for Autonomous Humanoid Boxing** 

**Defensive Penalty.** To penalize being hit by high-velocity strikes, we define 


**Terminal Outcome Reward.** The terminal reward reflects episode outcomes: 


**Summary.** The total task reward in this competitive stage is: 


The detailed reward terms, weights and hyperparameters are shown in Table 5. 

_Table 5._ Summary of Boxing Reward Components in Competitive Stage. 

|**Term**|**Formula**|**Hyperparameters**|**Weight**|**Description**|
|---|---|---|---|---|
|_r_face|exp(_−_<sup>1</sup><sup>_−dx_</sup><br>_σ_face <sup>)</sup><br><sup>2</sup>|_σ_face = 0_._5|_w_face = 1_._2|Facing alignment|
|_r_vel|I[_v∥>_0] exp(_−_<sup>_e_</sup><br>_v_<br>_σ_vel <sup>)</sup><br><br>|_σ_vel = 0_._25,_v_tar = 1_._0|_w_vel = 0_._5|Velocity|
|_r_dist|1<br>_H_<br>�_e−di/σgi_|_σ_dist = 1_._0,_v_th = 0_._8,_α_= 10_._0|_w_dist = 1_._5|Velocity-gated approach|
|_r_hit|I[_Hl ∨Hr_]|_τf_ = 1_._0_, τv_ = 1_._0|_w_hit = 50|Offensive hit|
|_r_def|I[_δl ∨δr_]|_τf_ = 1_._0,_τv_ = 1_._0|_w_def = 8_._0|Defensive penalty|
|_r_str|_∥_**F**<sup>opp</sup>_∥−∥_**F**<sup>ego</sup>_∥_|–|_w_str = 0_._3|Delta striking force|
|_r_term|I[_h_opp _< h_min]_−_I[_h_ego _< h_min]|_h_min = 0_._4|_w_term = 0_._3|Terminal outcome|


## **D.4. Training Details** 

**Latent Action Mixing.** During interaction, agents select their behavior based on an exploration parameter _η ∈_ [0 _,_ 1]. The latent action _z_ is sampled according to a mixture strategy _σ_ = _η ·_ ¯ _πz_ + (1 _− η_ ) _· πz_<sup>_RL_</sup> , i.e., 


**Optimization Objectives.** The best response policy is updated using the PPO objective to maximize the hybrid task and style reward. Simultaneously, the average policy _π_ ¯ _z_ is optimized by minimizing the mean squared error (MSE) relative to the stored best-response actions: 


Through this competitive co-evolution, the agents develop sophisticated boxing behaviors, while the latent-space constraints ensure that all maneuvers remain within the bounds of physical feasibility and stylistic authenticity. 

# **E. Proof Sketch of Proposition 3.5** 

_Proof._ Let _Z_ be a compact metric space and let _u_ : _Z × Z →_ R be the (induced) bounded payoff for player 1, with player 2 receiving _−u_ . Denote _|u_ ( _z_ 1 _, z_ 2) _| ≤ U_ for all ( _z_ 1 _, z_ 2) (Assumption 3.3). We consider mixed strategies as probability measures over _Z_ . For distributions _µ, ν ∈_ ∆( _Z_ ), define the bilinear extension 


Because _u_ is bounded and measurable, _u_ ( _µ, ν_ ) is well-defined. Moreover, since _Z_ is compact and _u_ is continuous, the zero-sum game admits a value 


17 

### **RoboStriker: Hierarchical Decision-Making for Autonomous Humanoid Boxing** 

and at least one Nash equilibrium ( _µ_<sup>_⋆_</sup> _, ν_<sup>_⋆_</sup> ) exists (standard minimax on compact domains). Let ( _z_ 1<sup>_t, z_</sup> 2<sup>_t_)</sup><sup>_T_</sup> _t_ =1<sup>be the sequence</sup> generated by the learning process. Define the empirical distributions (uniform averages) 


where _δz_ is a point mass at _z_ . Let _νt−_ 1 denote player 2’s empirical distribution up to time _t −_ 1: _νt−_ 1 = _t−_ <u>11</u> � _ts−_ =11<sup>_δz_</sup> 2<sup>_s_</sup> (similarly _µt−_ 1). Assumption 3.4 states that the updates are approximate best responses: for some error sequences ( _ϵ_ 1<sup>_t, ϵt_</sup> 2<sup>)</sup> with _ϵ_<sup>_t_</sup> _i_<sup>_≥_0,</sup> 


Equivalently, player 2 approximately best-responds to _minimize_ player 1’s payoff. 

Given the regrets against the realized opponent actions as 


Then, a standard zero-sum argument shows that for any sequences, the empirical distributions satisfy 


because _u_ ( _z_ 1 _,_ ¯ _νT_ ) = _T_<sup><u>1</u></sup> � _Tt_ =1<sup>_u_(</sup><sup>_z_1</sup><sup>_, z_</sup> 2<sup>_t_) and similarly for the other term.Thus, if both average regrets are small, (¯</sup><sup>_µT,_¯</sup><sup>_νT_) is</sup> an approximate Nash Equilibrium, i.e., 


The dynamics (21)–(22) correspond to a follow-the-leader / best-response-to-average procedure. In zero-sum games with bounded payoffs, this yields sublinear regret up to logarithmic factors; informally, best-responding to the running average prevents persistent exploitation. Concretely, one can show that there exists a constant _C_ depending only on the payoff range (e.g., _C_ = 2 _U_ suffices for a crude bound) (Brown, 1951; Zinkevich et al., 2007) such that 


Combining (23) and (25) gives 


and 


Therefore, letting 


we obtain that (¯ _µT ,_ ¯ _νT_ ) is an _ϵT_ -Nash equilibrium of the induced game. As _T →∞_ , if the average approximation errors vanish (or remain bounded), _ϵT →_ 0 (or to the average error floor), establishing the claimed convergence to an approximate Nash Equilibrium. 

18 

**RoboStriker: Hierarchical Decision-Making for Autonomous Humanoid Boxing** 

# **F. Experiment Details** 

**Training Setup.** We implement our framework using Isaac Lab (NVIDIA et al., 2025) on the NVIDIA Omniverse platform, leveraging massive parallelization with 4,096 environments for large-scale training. The simulated Unitree G1 humanoid (Unitree, 2024) utilizes 29 degrees of freedom, with the physics engine operating at 200 Hz and the control policy at 50 Hz. Strategic co-evolution is conducted over a 32-dimensional latent manifold. 

**Multi-agent Training.** In the final self-play stage, the LS-NFSP is configured with an exploration parameter _η_ = 0 _._ 1 and a strategy reservoir capacity of _K_ = 10<sup>6</sup> samples per agent. The reward function balances performance and style with a task reward weight _w_ task of 0 _._ 8 and an AMP style reward weight _w_ style of 0 _._ 2, while the prior loss coefficient _λ_ prior is set to 0 _._ 001. Training is executed on a single NVIDIA RTX 4090 GPU, incorporating domain randomization across friction, mass, and actuator gains to ensure robust tactical emergence. 

To evaluate the tactical progression and physical performance of the LS-NFSP framework, we define a comprehensive set of metrics across three primary dimensions: tactical proficiency, physical stability, and stylistic authenticity. Win Rate ( _WR_ ) is defined as the percentage of matches won over a series of 20 evaluation bouts, where a match is lost by the agent that first contacts the ground with any body part other than the feet, thereby triggering a fall-based termination. To quantify offensive precision, we define Hit Efficiency ( _ηhit_ ) as the ratio of successful strikes, which is identified by the proportion of contacts exceeding the force threshold _Fth_ = 10 _N_ to the total number of offensive attempts. Furthermore, the Engagement Rate ( _ER_ ) evaluates the strategic positioning and operational persistence of an agent. It is calculated as the proportion of the episode duration in which the agent concurrently satisfies two spatial conditions: maintaining a distance _dt_ within the effective striking range [0 _._ 5 _,_ 1 _._ 2] and ensuring a facing alignment cos( _θt_ ) that exceeds a predefined threshold _τface_ = 0 _._ 9. This metric provides a rigorous measure of an agent’s ability to maintain a viable combat posture, effectively penalizing tactical avoidance or non-confrontational movement patterns. 

Physical stability is assessed through Base Orientation Stability ( _Obase_ ) and Torque Smoothness ( _Sτ_ ). To ensure a positive correlation with control quality, _Obase_ is defined using an exponential kernels on the angular deviation: _Obase_ = E[exp( _−∥_ **g** _base −_ **g** _world∥_<sup>2</sup> )], where **g** _base_ and **g** _world_ represent the gravity vector in the robot’s local frame and the global frame, respectively. A higher _Obase_ score indicates a superior ability to maintain an upright posture under competitve perturbations. Torque Smoothness ( _Sτ_ ) measures the magnitude of high-frequency oscillations in motor commands, calculated as the mean absolute change in joint torques across consecutive control steps: _Sτ_ = E[ _∥τt − τt−_ 1 _∥_ ]. A lower _Sτ_ value represents more hardware-friendly execution and reduced mechanical wear. Finally, the Stylistic Authenticity of the emergent behaviors is evaluated via qualitative visual inspection. Instead of relying on a singular numerical score, we provide a comparative analysis of simulation snapshots to assess the human-likeness of the motions. This includes identifying key boxing maneuvers such as slips, counters, and rhythmic footwork, while ensuring the absence of unnatural joint configurations or physically unsustainable postures that often characterize non-constrained reinforcement learning policies. 

## **F.1. Baselines** 

We compare LS-NFSP against a set of baselines that isolate the contributions of (i) NFSP-style opponent averaging, (ii) the latent strategy manifold, (iii) curriculum warmup, and (iv) stylistic regularization. 

- **Naive Self-Play (Naive SP).** A standard self-play baseline (Samuel, 1959; Hernandez et al., 2019) trained in the same latent action space as ours, where each agent always plays against the opponent’s latest policy snapshot (no opponent averaging). 

- **Fictitious Self-Play (Fictitious SP).** A latent-space self-play baseline inspired by fictitious play (Brown, 1951), where agents are trained by sampling opponents uniformly from a population of historical policies. Unlike LS-NFSP, it does not maintain an explicit learned average policy network. 

- **LS-NFSP w/o AMP.** An ablation of our method where the Adversarial Motion Prior (AMP) style reward (Peng et al., 2021) is removed during training, testing the importance of motion-style regularization for physically plausible and effective strikes. 

- **PPO-Only.** A non-competitive baseline trained with PPO (Schulman et al., 2017) against a fixed opponent (no self-play). This tests whether competitive co-evolution is necessary to induce robust tactics. 

19 

**RoboStriker: Hierarchical Decision-Making for Autonomous Humanoid Boxing** 

- **Static-Target Specialist.** The policy after the warmup stage (trained to strike a passive sandbag) deployed without further competitive training. This measures how much performance comes from single-agent skill acquisition alone. 

- **Self-Play w/o Warmup (SP w/o Warmup).** A curriculum ablation where self-play starts from scratch without the sandbag warmup, testing learning stability under sparse and non-stationary competitive signals. 

- **29-DoF Action-Space Self-Play (29Dof Action-Space SP).** A baseline that performs self-play directly in the 29-DoF joint target space (i.e., without the learned latent manifold), highlighting the instability of competitive learning in raw motor command space. 

20 

