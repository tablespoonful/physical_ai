---
title: "Domain-Adaptive Communication-Rate Optimization for Sim-to-Real Humanoid-Robot Wireless XR Teleoperation"
date: "2026-05-19"
authors: "Caolu Xu; Zhiyong Chen; Meixia Tao; Li Song; Feng Yang; Wenjun Zhang"
url: https://arxiv.org/abs/2605.19293
pdf: https://arxiv.org/pdf/2605.19293
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2605.19293)** / [論文ページ](https://arxiv.org/abs/2605.19293)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

1 

# Domain-Adaptive Communication-Rate Optimization for Sim-to-Real Humanoid-Robot Wireless XR Teleoperation Caolu Xu, Zhiyong Chen, _Senior Member, IEEE_ , Meixia Tao, _Fellow, IEEE_ , Li Song, _Senior Member, IEEE_ , Feng Yang, and Wenjun Zhang, _Fellow, IEEE_ 

**_Abstract_ —Wireless extended reality (XR) teleoperation provides embodied interaction capability for collecting humanoid robot demonstrations, but the large-scale adoption is restricted by the overhead of high-frequency motion transmission. This paper develops a system framework that integrates sampling, transmission, interpolation, and reconstruction and formulates a communication-rate optimization that aims to minimize the communication energy while maintaining the reconstruction accuracy of robot motion trajectories through dimension-wise samplingrate control. Since acquiring real-time feedback from physical robots is limited by hardware costs, it is necessary to solve the problem through simulator interaction with offline real-domain data correction. To guide sim-to-real adaptation, we provide a PAC-Bayes generalization characterization that reveals the effects of latent density-ratio estimation, finite-sample deviation, and encoder bias. Building on this analysis, we propose a proximal policy optimization (PPO) method with density-ratio weighting and trust-region regularization. Experiments on public humanoid teleoperation dataset show that the proposed method improves the tradeoff between reconstruction error and communication energy consumption under sim-to-real distribution shift. We further analyze the effectiveness of the proposed algorithm across various wireless channels and dynamic motion trajectories.** 

**_Index Terms_ —Wireless XR teleoperation, sim-to-real, domainadaptive, proximal policy optimization.** 

## I. INTRODUCTION 

Embodied intelligence has recently emerged as a highly promising direction in both industry and academia. Representative paradigms, such as vision-language-action (VLA) [1] and world models (WMs) [2], rely on large-scale demonstration data to train generalizable embodied policies. In this context, extended reality (XR) enables wireless teleoperation through immersive interaction and intuitive human interfaces [3], [4], making it particularly suitable for scalable collection of high-quality human demonstrations. 

Despite these advantages, wireless XR teleoperation still faces several critical challenges. From the communication perspective, accurate motion reconstruction requires highfrequency motion sampling and transmission. Such frequent updates impose non-negligible energy consumption on the battery-powered XR device. In addition, wireless channels are inherently time-varying due to user mobility, blockage, and interference, which further complicates reliable low-latency 

The authors are with the Cooperative Medianet Innovation Center, the School of Information Science and Electronic Engineering, Shanghai Jiao Tong University, Shanghai 200240, China (e-mail: _{_ 021034910015, zhiyongchen, mxtao, song <u>li,</u> yangfeng, zhangwenjun _}_ @sjtu.edu.cn). 

transmission. Different dimensions contribute unequally to robot-side reconstruction fidelity, implying that uniform fullrate transmission of all components can be energy-inefficient. 

From the learning perspective, the evaluation metric is the execution performance of physical robots in real-world environments. However, large-scale real-world interaction is often impractical for training communication-aware teleoperation policies due to safety constraints, high hardware costs, and limited data collection efficiency. As a result, policy training is typically conducted in simulation environments, where abundant rollouts can be generated efficiently. Nevertheless, the discrepancy between simulated and real-world environments introduces a sim-to-real distribution shift, which may degrade policy performance during real deployment. 

These challenges motivate the need to design a wireless XR teleoperation framework that jointly balances device resource consumption and motion reconstruction accuracy, while explicitly accounting for the sim-to-real gap. 

## _A. Related Work_ 

Recently, several works have investigated wireless XR systems. For XR video streaming, latency optimization of prediction, communication, and computing was studied in [5], while cross-frame resource allocation with proactive caching for 360<sup>_◦_</sup> video was investigated in [6]. For interactive XR, wireless multiplayer systems with edge computing were modeled in [7], and an edge-device collaborative framework leveraging foreground-background separation was developed in [8]. Beyond XR services, synchronization between physical devices and digital models in the metaverse has been studied to enable timely and accurate model updates [9], [10]. These studies demonstrate the importance of cross-layer resource management for wireless XR. However, most existing works focus on media transmission or system-level coordination, and few have investigated wireless transmission for robot motion reconstruction while explicitly considering the sim-to-real gap in XR teleoperation. 

In humanoid robot learning, sim-to-real transfer has become an important topic. Reinforcement learning (RL) algorithms have been widely used to train humanoid control policies for whole-body skills, motion imitation, and recovery behaviors. HoST [11] learns standing-up control for humanoids across diverse postures, demonstrating the potential of RL-based policies for real-world humanoid recovery tasks. ASAP [12] 

2 


Fig. 1: Overview of the proposed sim-to-real wireless XR teleoperation framework for humanoid robot. 

uses real-world data to mitigate dynamics mismatch and improve the transferability of humanoid skills learned in simulation, while Humanoid Policy [13] studies cross-embodiment learning from human and humanoid demonstrations. More recently, DoorMan [14] investigates humanoid pixel-to-action policy transfer and shows that vision-based loco-manipulation policies trained in simulation can be transferred to real humanoids for articulated-object interaction. These methods primarily aim to enhance the transferability of humanoid manipulation and locomotion skills. In contrast, our work focuses on communication-rate policy learning in wireless XR teleoperation. Specifically, the policy is trained mainly using simulator rollouts, while offline real-world teleoperation trajectories are used to characterize deployment bias and mitigate the sim-to-real distribution shift. 

Domain adaptation has shown promise in addressing distribution shifts in communication systems, such as mmWavebased human activity recognition [15], collaborative learning on mobile edge devices [16], and cross-domain wireless localization under non-line-of-sight conditions [17]. In general, domain adaptation aims to transfer knowledge from a source domain, where effective model training is feasible, to a target domain with a different distribution, by reducing sourcetarget discrepancy. Representative techniques include instance reweighting and density-ratio estimation [18], [19], as well as discrepancy-based feature alignment approaches such as maximum mean discrepancy (MMD) and correlation alignment [20]–[22]. In this paper, domain adaptation provides a principled way to correct simulator-induced bias using offline real-domain trajectories, preserving the effectiveness of communication rate decisions without requiring online interaction with the physical robot during policy training. Compared with existing methods developed for model adaptation under relatively fixed input-output mappings, wireless XR teleoperation involves sequential communication control, where current decisions affect subsequent system states and performance. This motivates domain-adaptive policy learning rather than direct application of conventional domain adaptation methods. 

- We propose a sim-to-real wireless XR teleoperation framework that considers dimension-wise motion sampling, energy-aware wireless communication, robot reconstruction, and platform execution. Based on this framework, we formulate a long-term communication rate optimization problem that balances the motionreconstruction accuracy and device communication energy under sim-to-real distribution shift. 

- We develop a PAC-Bayes [23] generalization characterization with latent density-ratio estimation and encoderinduced representation bias. This characterization decomposes the real-domain performance gap into the importance-weighted empirical risk, density-ratio approximation error, finite-sample deviation, and encoder representation bias. This analysis provides theoretical guidance for designing the representation learning and policy optimization procedure. 

- We introduce latent density-ratio correction into proximal policy optimization (PPO) [24] for communicationrate optimization and develop a domain-adaptive training framework. First, an encoder is initialized through a MMD-based warm-up on simulator samples and offline real-domain trajectories. The initialized encoder is then frozen to provide a stable latent space for densityratio estimation and importance-weighted PPO. Finally, with the policy network fixed, the encoder is finetuned using trust-region regularization [25] and weighted MMD, improving latent alignment while preventing uncontrolled representation drift. The experimental results demonstrate that the proposed algorithm achieves a better reconstruction-energy tradeoff than baseline methods under sim-to-real distribution shift. 

The rest of this paper is organized as follows. Section II presents the system model and formulates the sim-to-real communication-rate optimization problem. Section III provides the PAC-Bayes generalization analysis with latent density ratio and representation bias. Section IV develops the domain-adaptive policy optimization algorithm. Section V presents simulation results. Section VI concludes the paper. 

## _B. Contributions_ 

In this paper, we investigate sim-to-real communication-rate optimization in wireless XR teleoperation for humanoid robot. The main contributions are summarized as follows. 

## II. SYSTEM MODEL AND PROBLEM FORMULATION 

In this section, we present a framework for the simto-real wireless XR teleoperation system. As illustrated in 

3 

Fig. 1, the XR device first captures human motion trajectories through pose sensing, followed by dimension-wise sampling for communication-efficient transmission. The sampled human motion data are transmitted to the execution module, where interpolation and reconstruction are performed to recover robot motions. The system aims to achieve accurate, real-time motion reconstruction on the physical robot while reducing unnecessary device communication energy under time-varying wireless conditions and the sim-to-real distribution shift. 

## _A. Framework and Cross-System Architecture_ 

The timeline of the proposed framework is shown in Fig. 2. The teleoperation process is described on three time scales: continuous physical time _ν_ for the raw XR motion, decision slots _t_ for sampling-rate control, and execution indices _t†_ for simulation or robot updates, where _† ∈{_ sim _,_ real _}_ denotes the execution platform. 

The decision process is modeled in discrete slots indexed by _t_ , where each slot has duration _τs_ and corresponds to interval 


At the beginning of slot _t_ , sampling rates are selected and remain effective over _Tt_ . 

_XR and robot configuration spaces: ν ∈_ R+ denotes continuous physical time. The human motion trajectory captured by the XR device is denoted by 


where _J_ xr is the number of tracked XR sampling dimension. The humanoid robot configuration space is represented by 


where _J_ rb is the number of controllable robot joints. In general, _J_ xr _̸_ = _J_ rb, and the two spaces have different kinematic structures. 

_Execution time scales:_ The execution platform is indicated by _† ∈{_ sim _,_ real _}_ , with sim and real corresponding to the simulated and physical robot, respectively. For platform _†_ , the execution frequency is _f†_ , the execution period is _τ†_ = 1 _/f†_ , and the execution index is _t† ∈_ Z+. 

To satisfy the update requirements of platform _†_ , the XR motion trajectory is aligned to the execution grid. For the ideal reference trajectory, each sampling dimension is assumed to be transmitted over a lossless channel at its highest admissible rate. Let _fj_<sup>max</sup> denote the highest admissible rate of the _j_ - th sampling dimension, and let _Tj_<sup>max</sup> = 1 _/fj_<sup>max</sup> be the corresponding sampling period. The reference sampling-time set _Vj_<sup>max</sup> consists of equally spaced physical instants with interval _Tj_<sup>max</sup> . For each dimension _j_ , the ideal interpolated XR trajectory is defined as 


where _Ij,_<sup>ref</sup> _†_<sup>(</sup><sup>_·_)isthereferenceinterpolationoperatorthateval-</sup> uates the _j_ -th XR sampling dimension at execution instant _t†τ†_ from the reference samples. Stacking all dimensions gives **q**<sup>xr</sup> ( _t†_ ) = � _q_ 1<sup>xr(</sup><sup>_t†_)</sup><sup>_, . . . , q_</sup> _J_<sup>xr</sup> xr<sup>(</sup><sup>_t†_)</sup> � _⊤_ . 

_Retargeting operator:_ The mapping from the XR sample space to the robot joint space is denoted by 


Then the ideal robot joint trajectory on platform _†_ is 


The specific realization of _R_ , such as inverse kinematics, does not affect the subsequent analysis. 

## _B. Sampling, Transmission, Interpolation, and Reconstruction_ 

_Dimension-wise sampling rates:_ To account for different motion characteristics and transmission requirements across sampling dimensions, we allow the admissible sampling-rate set to depend on the dimension index. At the beginning of the slot _t_ , the sampling rate assigned to the _j_ -th sampling dimension is denoted by _fj_ ( _t_ ), where 


Here, _Fj_ is the admissible sampling-rate set of the _j_ -th XR sampling dimension, and _Fj_ is the number of nonzero rate levels. The nonzero rate levels are ordered as 0 _< fj_<sup>(1)</sup> _< · · · < fj_<sup>(</sup><sup>_Fj_)</sup> = _fj_<sup>max</sup> _._ In particular, _fj_ ( _t_ ) = 0 indicates that there is no transmission of dimension _j_ in slot _t_ . The dimension-wise sampling rate in slot _t_ is 


Given _fj_ ( _t_ ), let _Vj_ ( _t_ ) _⊆Tt_ denote the set of physical time stamps at which samples of the _j_ -th XR dimension are received within slot _t_ . If _fj_ ( _t_ ) = 0, no sample of dimension _j_ is transmitted and _Vj_ ( _t_ ) = ∅ _._ If _fj_ ( _t_ ) _>_ 0, _Vj_ ( _t_ ) is generated by the sampling clock associated with rate _fj_ ( _t_ ) over _Tt_ . Thus, _t_ indexes the decision slot, whereas _ν ∈Vj_ ( _t_ ) denotes a physical time stamp used for interpolation of the _j_ -th XR sampling dimension. 

_Wireless transmission and energy cost:_ We consider a orthogonal frequency division multiplexing (OFDM) wireless link with total bandwidth _B_ and use an equivalent-link rate model after subcarrier aggregation. Let _P_ ( _t_ ) denote the total transmit power of the XR device in slot _t_ . The equivalent channel gain _g_ ( _t_ ) captures the time-varying wireless conditions. We assume that _g_ ( _t_ ) is available at the beginning of slot _t_ . _N_ 0 denotes the spectral density of noise power. The transmission rate _C_ ( _t_ ) in slot _t_ is given by 


Let **d** = [ _d_ 1 _, . . . , dJ_ xr]<sup>_⊤_</sup> denote the payload-size vector for one update of the XR samples, where _dj_ is the number of bits transmitted for one update of dimension _j_ . Given the samplingrate vector **f** ( _t_ ) in slot _t_ , the transmission load over the slot is 


The transmission constraint in slot _t_ is given by 


4 


Fig. 2: Timeline of the proposed wireless XR teleoperation framework. 

Effective communication energy is not limited to the radio frequency (RF) transmit power. In addition to RF transmit power, packetization, protocol-related, and other communication pipeline overheads also contribute to the energy consumption of XR device. For tractability, these additional overheads are incorporated through an effective energy coefficient _ζ ≥_ 1. The effective communication energy in slot _t_ is defined as 


_Sample interpolation:_ For the _j_ -th XR sampling dimension, the sample received at the execution module at physical instant _ν ∈Vj_ ( _t_ ) is denoted by _q_ ˜ _j_<sup>xr(</sup><sup>_ν_).Tomatchthe</sup> execution time scale of platform _†_ , the received XR samples are interpolated on the execution grid. For each dimension _j_ , the reconstructed XR sample value at execution index _t†_ is obtained from the samples received no later than the execution instant _t†τ†_ 


where _Ij,†_ ( _·_ ) denotes the interpolation operator for dimension _j_ on platform _†_ . If no prior sample is available, an initial pose is used. Stacking all reconstructed dimensions gives the interpolated XR trajectory **q** ˆ<sup>xr</sup> ( _t†_ ) = � _q_ ˆ1<sup>xr(</sup><sup>_t†_)</sup><sup>_, . . . ,_ˆ</sup><sup>_q_</sup> _J_<sup>xr</sup> xr<sup>(</sup><sup>_t†_)</sup> � _⊤_ . 

_Reconstruction error:_ The reconstructed robot joint trajectory is obtained by applying the retargeting operator to the interpolated XR motion 


Since the reconstruction fidelity is evaluated on the execution time scale, the joint reconstruction error is defined as 


where **W** = diag( _w_ 1 _, . . . , wJ_ rb) with _wj ≥_ 0 is the jointimportance weighting matrix, and **q**<sup>rb</sup><sup>_⋆_</sup> ( _t†_ ) is the ideal robot joint trajectory defined in (6). 

To obtain a slot-level fidelity measure, the execution-level errors falling within slot _t_ are accumulated over the associated execution indices 


5 

The reconstruction cost on platform _†_ in slot _t_ is defined as 

and the corresponding minimum update energy cost is 


Substituting (20) and (21) into _P_ 0, an equivalent problem is obtained as 

## _C. Sim-to-Real Objective and Problem Formulation_ 


Let _M_ sim and _M_ real denote the simulated and real teleoperation systems, respectively. The objective is to determine the sequence _{_ **f** ( _t_ ) _}t≥_ 1 that minimizes the average teleoperation cost on the real system. With the reconstruction cost _E_ real( _t_ ) in (17) and the effective communication energy cost _E_ ( _t_ ) in (12), the real-system performance criterion is defined as 

## _D. Reinforcement Learning Reformulation_ 

The optimization problem _P_ 1 is a stochastic sequential decision problem over an infinite horizon. Due to the discrete sampling-rate decisions, the nonlinear communication energy model, and the coupled reconstruction cost induced by sampling, interpolation, and reconstruction, it is more suitably addressed through RL. Accordingly, _P_ 1 is reformulated as a Markov decision process (MDP). The policy _π_ is learned in simulation and deployed at the execution module for slot-wise decision making. 


where _λE >_ 0 is a weighting coefficient that balances teleoperation accuracy and energy consumption, and E _M_ real[ _·_ ] denotes the expectation with respect to the probability distribution induced by _M_ real. 

During policy training, the real teleoperation system _M_ real is not treated as an interactive environment. Instead, it provides offline real-domain trajectories, while the simulator _M_ sim can be queried repeatedly to generate rollouts under candidate communication rate policies. The discrepancy between the simulator-induced distribution and the offline real domain distribution is incorporated through a density-ratio correction. For each slot _t_ , let _χt_ denote the random variable induced by the teleoperation process. The probability distributions of _χt_ under _M_ real and _M_ sim are denoted by _P_ real _,t_ and _P_ sim _,t_ , respectively. Both domains share the same robot kinematic model, action space, and state representation, while their distributions may differ due to sensing noise, actuation uncertainty, and unmodeled physical effects. Assuming _P_ real _,t ≪ P_ sim _,t_ , the Radon–Nikodym derivative of _P_ real _,t_ with respect to _P_ sim _,t_ exists [26]. The density-ratio weight in slot _t_ is defined as 

_State:_ The latest available execution index before the beginning of slot _t_ on platform _†_ is denoted by 


Accordingly, the most recent reconstructed robot joint position available at slot _t_ is **q** ˆ<sup>rb</sup> ( _t_<sup>¯</sup> _†_ ( _t_ )). **v** ˆ<sup>rb</sup> ( _t_ ) and **a** ˆ<sup>rb</sup> ( _t_ ) denote the current reconstructed robot joint velocity and acceleration, respectively. The reconstructed robot joint velocity and acceleration are defined by 


For the first two execution instants, the missing historical terms are initialized using the initial robot state. 


To characterize the dimension-wise transmission load in the previous slot, define 

which gives the importance weight for converting the expectation under _M_ sim into that under _M_ real. 


Accordingly, the sim-to-real problem is formulated as 

where _⊙_ denotes the Hadamard product, and **f** ( _t −_ 1) is the sampling-rate vector selected in the previous slot. 


The state at slot _t_ is then defined as 


where _λ_ E _>_ 0 is a coefficient that calibrates the relative scale of the two terms in the unified objective, and E _M_ sim[ _·_ ] denotes the expectation with respect to the probability distribution induced by _M_ sim. 

_Action:_ The action at slot _t_ is the dimension-wise sampling-rate decision 


For any given **f** ( _t_ ), the effective communication energy _E_ ( _t_ ) in (12) is monotonically increasing in _P_ ( _t_ ). Therefore, the minimum energy required to support the transmission load _D_ ( _t_ ) is attained when (11) holds with equality, 

_Reward:_ In the simulator _M_ sim, the instantaneous reward is defined as the negative cost 


The density-ratio _ιt_ in _P_ 1 is incorporated as an importance weight in Section IV-B, rather than being absorbed into _rt_ . 


6 

III. PAC-BAYES GENERALIZATION ANALYSIS WITH LATENT DENSITY RATIO AND REPRESENTATION BIAS 

## _A. Setup and Notation_ 

We consider a sim-to-real RL problem induced by the MDP reformulation in Section II-D. A parameterized encoder Ω _θ_ maps the state _xt_ in (27) into a latent representation _zt_ = Ω _θ_ ( _xt_ ) _∈Z_ , and the policy operates in the latent space. For notational simplicity, we write _x ∈X_ and _a_ as generic realizations of the state _xt_ in (27) and the action _at_ in (28), respectively. The simulator and the real system induce state distributions over _X_ , denoted by _P_ sim and _P_ real, respectively. Since the encoder Ω _θ_ maps state samples from both simulator and real domain into a common latent space, it is trained on mixed-domain samples to construct a shared latent representation across the two domains. 

By construction, the real-domain risk can be rewritten as 


Since the policy operates in latent space, for a given encoder Ω _θ_ , we consider the latent distributions _P_ sim<sup>_θ_=</sup><sup>_P_sim</sup><sup>_◦_Ω</sup><sup>_−_</sup> _θ_<sup>1</sup> and _P_ real<sup>_θ_=</sup><sup>_P_real</sup><sup>_◦_Ω</sup><sup>_−_</sup> _θ_<sup>1.Thecorrespondinglatentdensityratiois</sup> denoted by 


In implementation, an estimator ˆ _ι_ ( _z_ ) is fitted in the latent space using kernel-based density-ratio estimation methods, e.g., uLSIF and KLIEP. For notational simplicity, we omit the dependence of ˆ _ι_ on the encoder parameter _θ_ when the encoder is clear from the context. 

Let _H_ be a hypothesis class, where each _h ∈H_ comprises 

the parameters of encoder Ω _θ_ , policy _πψ_ , value function _Vω_ , 


In the dataset _D†_ , _τi_<sup>_†_isthe</sup><sup>_i_-thtrajectory,</sup><sup>_N†_isthenumber</sup> of trajectories, and _Ti_<sup>_†_denotes the length of the</sup><sup>_i_-th trajectory.</sup> Define the simulator and real sample sets as 


To separate representation warm-up from density-ratio estimation, the simulator samples are divided into a warm-up set _Sh_ and a ratio-estimation set _Sι_ 


The encoder warm-up is performed on _Sh ∪X_ real, while density-ratio estimation uses _Sι_ and _X_ real. 

## _B. Population Risks on Real Domain_ 

The population risk of a hypothesis _h ∈H_ under distribution _P_ real is defined as 


where _L_ ( _h, x_ ) _∈_ [0 _,_ 1] is a bounded loss. 

The slot-level density-ratio weight _ιt_ in (19) is defined on _χt_ for the objective formulation. For the generalization analysis, we use the real-to-simulator density ratio over _X_ 


When _x_ = _xt_ , this ratio is evaluated at the state sample generated in decision slot _t_ . 

We assume that _P_ real is absolutely continuous with respect to _P_ sim, denoted by _P_ real _≪ P_ sim. This assumption means that any event in _X_ with zero probability under _P_ sim also has zero probability under _P_ real. It guarantees the existence of the Radon–Nikodym derivative in (35). 

## _C. Importance-Weighted PAC–Bayes Deviation Analysis_ 

After the density-ratio estimator ˆ _ι_ is fitted using _Sι_ and _X_ real in the frozen reference latent space, it is treated as fixed in the subsequent deviation analysis. If the raw estimator takes negative values, it is clipped to be nonnegative before normalization, and we still use ˆ _ι_ to denote the resulting nonnegative estimator in the deviation analysis. The analysis is interpreted for a fixed encoder used to construct the latent space at the corresponding training stage; the dependence on the encoder is captured by _ει_ ( _θ,_ ˆ _ι_ ) and _ε_ enc( _θ_ ). Let _B_ sim denote a simulator rollout batch collected after fitting ˆ _ι_ . The estimated weights are normalized to have unit mean over _B_ sim, and we reuse ˆ _ι_ to denote the normalized estimator. The realdomain risk (36) is approximated by 


Following standard importance-weighted analysis, we decompose 


The density-ratio estimation error is defined as 

_ει_ ( _θ,_ ˆ _ι_ ) = sup _|_ E _x∼P_ sim[( _ιX_<sup>_⋆_(</sup><sup>_x_)</sup><sup>_−_ˆ</sup><sup>_ι_(Ω</sup><sup>_θ_(</sup><sup>_x_)))</sup><sup>_L_(</sup><sup>_h, x_)]</sup><sup>_| ._(40)</sup> _h∈H_ 

For a data-dependent posterior _Q_ over _H_ , define 


Consider a prior _P_ that is chosen independently of the simulator samples used in the empirical risk estimate, and a data-dependent posterior _Q_ over _H_ . For any confidence parameter _δ ∈_ (0 _,_ 1), let _C >_ 0 be a universal constant appearing in PAC–Bayes inequalities [23]. The standard importanceweighted PAC-Bayes analysis gives the following deviation 


7 

Here, the effective sample size is computed from the normalized weights as 


Combining (38)–(43) and introducing a representation discrepancy associated with the learned encoder, we obtain the following real-domain generalization characterization 


where _ε_ enc( _θ_ ) denotes the representation discrepancy induced by using the learned encoder Ω _θ_ in place of an ideal encoder. 

## _D. Encoder Bias_ 

Let Ω<sup>_⋆_</sup> denote an ideal encoder under which the real-tosimulator density ratio is sufficiently smooth and well approximated in the latent space. Define the encoder discrepancy as 


Assume that the loss _L_ is _Lz_ –Lipschitz with respect to the latent representation. Then, by a standard Lipschitz argument, 


Substituting (45) into (44), we obtain the following instantiated real-domain generalization characterization 


This characterization identifies four contributing terms to the real-domain generalization error: 

(i) the importance-weighted risk of the real domain _R_<sup>�</sup> ( _Q_ ); (ii) density-ratio approximation error _ει_ ( _θ,_ ˆ _ι_ ), induced by approximating the target ratio _ι_<sup>_⋆_</sup> _X_<sup>withthelatent-spaceesti-</sup> mator ˆ _ι_ (Ω _θ_ ( _x_ )); 

(iii) the PAC–Bayes deviation term, which captures finitesample uncertainty through KL( _Q∥P_ ) and _n_ eff (ˆ _ι_ ); 

(iv) the encoder representation bias _Lzϵ_ Ω( _θ_ ) induced by the mismatch between Ω _θ_ and Ω<sup>_⋆_</sup> . 

## IV. SIM-TO-REAL DOMAIN-ADAPTIVE POLICY OPTIMIZATION 

Building upon the PAC-Bayes analysis, we design a structured training framework that addresses the density-ratio estimation error and the encoder representation term identified above. The overall procedure consists of three phases: an encoder warm-up phase followed by two training stages. 

- 1) Warm-up: The encoder is initialized on _Sh∪X_ real by minimizing an MMD based warm-up objective. This phase provides a shared latent representation for simulator and real-domain samples. 

- 2) Stage 1: With the encoder frozen at _θ_ 0, a latent realto-simulator density ratio ˆ _ι_ is estimated and used as 

   - the importance weight. The communication-rate policy is then optimized in the latent state space using PPO. 

- 3) Stage 2: The encoder is unfrozen and fine-tuned with a trust-region regularization centered at _θ_ 0 and a latent alignment objective based on weighted MMD. During this stage, the policy and value networks are kept fixed, and only the encoder parameter _θ_ is updated. After encoder fine-tuning, the reference encoder is updated by setting _θ_ 0 _← θ_ , and policy optimization continues in the next outer iteration. 

The illustration of algorithm architecture is shown in Fig. 3. The warm-up phase initializes a coherent latent space. Stage 1 fixes the encoder to enable stable density-ratio estimation and reliable policy optimization in the latent space. Stage 2 then allows controlled encoder refinement through trust-region regularization, aiming to improve cross-domain alignment while keeping the latent representation close to the Stage 1 reference space. Together, these stages separate representation learning into a stable initialization phase and a subsequent regulated adaptation phase. The following subsections detail each component of the training framework. 

## _A. Encoder Warm-up_ 

We employ a multi-layer perceptron (MLP) as the encoder Ω _θ_ . Given simulator and real-domain minibatches _{x_ ˇ<sup>sim</sup> _u_<sup>_}n_</sup> _u_ =1<sup>w</sup><sup>_,_s</sup> _⊂ Sh_ and _{x_ ˇ<sup>real</sup> _v }_<sup>_n_</sup> _v_ =1<sup>w</sup><sup>_,_r</sup> _⊂ X_ real, their latent representations are defined as 


We use an MMD loss to reduce the initial discrepancy between the simulator and real-domain latent distributions: 


where _ϖ_ ( _z, z_<sup>_′_</sup> ) is a Gaussian mixture kernel defined on the latent space, 


where _σℓ >_ 0 controls the kernel width and _αℓ >_ 0 denotes the mixture weight satisfying<sup>�</sup><sup>_L_</sup> _ℓ_ =1<sup>_αℓ_= 1.</sup> The warm-up objective is 


where _λ_<sup>0</sup> MMD<sup>_, λ_regarenonnegativecoefficientsand</sup><sup>_∥θ∥_</sup> 2<sup>2is</sup> a regularization term. The warm-up on _Sh ∪X_ real provides a coherent latent representation across the simulator and the real domains. After optimizing _L_ warm( _θ_ ) in the warm-up phase, we denote the encoder parameter by _θ_ 0, and the initialized encoder by Ω _θ_ 0. 

8 


Fig. 3: Illustration of proposed sim-to-real domain-adaptive policy optimization algorithm architecture. 

## _B. Latent-Space PPO_ 

In Stage 1, the general characterization in Section III is instantiated with the frozen encoder Ω _θ_ 0. All simulator and real samples are first mapped into the corresponding reference latent space. The simulator and real latent sample sets are defined as 


where _i_ indexes trajectories and _t_ denotes the decision slot within each trajectory. 

To optimize the sim-to-real control objective in _P_ 1, a latent density ratio ˆ _ι_ ( _z_ ) is estimated 


where _P_ sim<sup>_θ_0and</sup><sup>_P_</sup> real<sup>_θ_0arethelatentdistributionsinducedby</sup> the frozen encoder Ω _θ_ 0. The estimator ˆ _ι_ ( _z_ ) is fitted using latent samples by uLSIF or KLIEP [18], [19]. Detailed descriptions of uLSIF and KLIEP are provided in the Appendix. For each iteration, simulator trajectories are collected as ( _x_ 1 _, a_ 1 _, r_ 1 _, . . . , xT_ ), where the horizon _T_ may vary across trajectories. Each state is mapped to latent space _zt_ = Ω _θ_ 0( _xt_ ). Generalized advantage estimation (GAE) is computed along the trajectory: 


Following the convention in Section III-C, ˆ _ι_ denotes the nonnegative density-ratio estimator after clipping when neces- 

sary. The real-to-simulator density ratio provides the normalized importance weight 


where E _t_ [ _·_ ] denotes the average over the rollout batch. 

The policy and value networks are updated by minimizing the following weighted PPO loss: 

_L_ PPO( _ψ, ω_ ) = _L_ pol( _ψ_ ) _− µ_ ent _L_ ent( _ψ_ ) + _µ_ val _L_ val( _ω_ ) _,_ (57) where _µ_ ent and _µ_ val are positive constants; the clipped policy loss is 


with the importance sampling ratio 


the entropy regularization term is defined as 


the value function term is 


where _Gt_ = _At_ + _Vω_ old( _zt_ ) denotes the value target constructed from generalized advantage estimation (GAE) [27]. 

Since the encoder remains fixed at _θ_ 0, the representation bias term _Lzϵ_ Ω( _θ_ 0) is fixed, and the density-ratio estimation is performed in a fixed latent space. Thus, the learned posterior _Q_ stage1 follows the characterization in (47): 


9 

## _C. Trust-Region Encoder Fine-tuning_ 

In Stage 2, the encoder parameters are unfrozen. To prevent uncontrolled drift in the latent space, which would compromise both policy optimization and density-ratio estimation, we introduce an explicit trust-region regularization. Specifically, a quadratic penalty centered at _θ_ 0 is imposed, where the coefficient _β >_ 0 controls the strength of the trust region, 


Within each outer iteration, _θ_ 0 is kept fixed and serves as the trust-region anchor. Here, _L_ MMD( _θ_ ) measures the discrepancy between the weighted simulator latent samples and the real latent samples. 

To keep encoder fine-tuning data consistent with the latest policy, we refresh simulator-state minibatches by rolling out _M_ sim with the frozen policy _πψ_ ( _·|_ Ω _θ_ 0( _x_ )) obtained from Stage 1. Given minibatches _{x_<sup>sim</sup> _u_<sup>_}n_</sup> _u_ =1<sup>_t,s_and</sup><sup>_{x_</sup> _v_<sup>real</sup> _}_<sup>_n_</sup> _v_ =1<sup>_t,r_,the</sup> latent representations are 


For the simulator minibatch, the stabilized weight is computed in the reference latent space using the encoder Ω _θ_ 0, under which the density-ratio estimator was fitted 


where _ϵw >_ 0 is used only to avoid numerical degeneracy when all estimated weights are close to zero. The estimator ˆ _ι_ is fixed after Stage 1, while the kernel evaluations in _L_ MMD( _θ_ ) use the current encoder Ω _θ_ . Thus, _L_ MMD( _θ_ ) can update the encoder while the importance weights remain tied to the reference latent space. 


The policy and encoder optimization are intentionally decoupled to preserve training stability. In Stage 1, the weighted PPO objective in (57) updates ( _ψ, ω_ ), under the frozen reference encoder Ω _θ_ 0. In Stage 2, _πψ_ is a frozen policy with input Ω _θ_ 0( _x_ ) to refresh simulator-state minibatches. The objective in (63) is then optimized using the current encoder Ω _θ_ for the MMD kernel evaluations, while the importance weights remain computed in the reference latent space. Therefore, no PPO gradient is propagated into the encoder during Stage 2. This separation avoids mutual interference between policy optimization and latent-space alignment. 

We now establish a stability result showing that bounded encoder drift introduces a controlled perturbation to the realdomain risk. Since Stage 2 freezes the policy and value networks, the posterior variation in this stage is induced only by the encoder parameter _θ_ , while _ψ_ and _ω_ are treated as fixed components inherited from Stage 1. 

_Assumption 1 (Lipschitz continuity with respect to encoder parameters):_ For any two encoders Ω _θ_ and Ω _θ_ 0 satisfying _∥θ−_ 

_θ_ 0 _∥_ 2 _≤_ κ, and for any policy parameter _ψ_ and value parameter _ω_ , the loss function satisfies 


This condition holds, for instance, when the loss is Lipschitz continuous with respect to the latent representation and the encoder is Lipschitz continuous with respect to its parameters. 

_Proposition 1 (Stability under bounded encoder drift):_ Let _Q_ stage2 denote the posterior after Stage 2, and let _Q_<sup>0</sup> stage2 denote the posterior obtained from _Q_ stage2 by replacing the encoder parameter _θ_ with _θ_ 0 while keeping ( _ψ, ω_ ) unchanged. Suppose that Stage 2 satisfies _∥θ − θ_ 0 _∥_ 2 _≤_ κ almost surely under _Q_ stage2. Then, under Assumption 1, 


_Proof:_ For any _h_ = ( _θ, ψ, ω_ ) sampled from _Q_ stage2, define _h_ 0 = ( _θ_ 0 _, ψ, ω_ ) by replacing the encoder parameter _θ_ with _θ_ 0 while keeping ( _ψ, ω_ ) unchanged. By Assumption 1, 


Taking expectation over _x ∼ P_ real and _h ∼ Q_ stage2 gives (67). 

Proposition 1 justifies the trust-region design in (63). Stage 2 allows the encoder to adapt through the MMD objective, while the proximal penalty _β∥θ − θ_ 0 _∥_ 2<sup>2discourageslarge</sup> deviations from the Stage 1 encoder. This design limits abrupt latent-space drift that could invalidate the learned density-ratio estimator and destabilize policy optimization. In practice, _β_ is gradually decayed across outer iterations, enabling conservative encoder updates at the early stage and increased flexibility after the policy and density-ratio estimator have stabilized. 

After Stage 2, the reference encoder is updated by setting _θ_ 0 _← θ_ , and the next iteration re-estimates the latent density ratio and continues weighted PPO training under the updated reference encoder. The overall procedure of the proposed algorithm is presented in Algorithm 1. 

## V. SIMULATION RESULTS 

## _A. Environment Settings_ 

Since human motion states in XR teleoperation usually evolve continuously over a second-level time scale, we adopt a relatively low-frequency decision frequency to reduce the additional overhead induced by receiving dimension-wise control at the XR device and avoid undesirable control oscillations induced by frequently sampling-rate switching. Specifically, the decision frequency is 5 Hz, i.e., _τs_ = 200 ms. Motivated by high-rate XR tracking modes in commercial XR devices, _fj_<sup>max</sup> = 120 Hz and _Fj_ = _{_ 0 _,_ 30 _,_ 60 _,_ 120 _}_ Hz. The execution frequencies of the simulated and real platforms are set to _f_ sim = 120 Hz and _f_ real = 30 Hz, i.e., _τ_ sim = 8 _._ 3 ms, _τ_ real = 33 _._ 3 ms, _T_ = 2000. All experiments were performed on an NVIDIA RTX 3070 GPU and Ubuntu 22.04. 

10 

## **Algorithm 1** Sim-to-Real Domain-Adaptive Policy Optimiza- <u>tion</u> 

- 1: **Initialize:** Interactive simulator environment _M_ sim; datasets _D_ sim _, D_ real; simulator-sample split ( _Sh, Sι_ ); warm-up steps _K_ 0; global iterations _K_ 1; Stage 1 iterations _K_ 2; Stage 2 iterations _K_ 3; trust-region weight _β_ 0; decay factor _µ_ ; regularization coefficient _λ_ reg; MMD coefficient _λ_<sup>0</sup> MMD<sup>;weightedMMDcoefficient</sup><sup>_λ_MMD.</sup> 

- 2: **Warm-up:** 3: **for** _k_ 0 = 1 _· · · K_ 0 **do** 4: Sample warm-up minibatches from _Sh_ and _X_<sup>real</sup> . 5: Update encoder parameter _θ_ by minimizing (51). 6: **end for** 7: Set initial encoder parameter _θ_ 0 _← θ_ . 8: Initialize PPO policy and value parameters ( _ψ, ω_ ). 9: Set _β ← β_ 0. 

- 10: **for** _k_ 1 = 1 _· · · K_ 1 **do** 11: **Stage 1. Frozen encoder with latent density-ratio estimation and PPO:** 

- 12: Freeze encoder at _θ ← θ_ 0. 13: Estimate latent real-to-simulator density ratio ˆ _ι_ ( _·_ ) using uLSIF or KLIEP in the Appendix. 

- 14: **for** _k_ 2 = 1 _· · · K_ 2 **do** 15: Roll out simulator trajectories in _M_ sim using _πψ_ ( _· | z_ ) with _z_ = Ω _θ_ 0( _x_ ), and collect the batch _B_ sim. 

- 16: Compute GAE advantages _At_ and real-to-simulator importance weights _wt_ by (54)–(56). 

- 17: Update ( _ψ, ω_ ) by minimizing the weighted PPO objective (57) with density ratio (59). 

- 18: **end for** 19: **Stage 2. Encoder fine-tuning with trust region and weighted MMD:** 

- 20: Unfreeze encoder _θ_ , while keeping _θ_ 0, ˆ _ι_ , _ψ_ , and _ω_ fixed. 21: **for** _k_ 3 = 1 _· · · K_ 3 **do** 22: Roll out simulator trajectories in _M_ sim using the policy _πψ_ ( _· | z_ ), where _z_ = Ω _θ_ 0( _x_ ). Collect simulator minibatches _{x_<sup>sim</sup> _u_<sup>_}n_</sup> _u_ =1<sup>t</sup><sup>_,_s,andcollectreal-domain</sup> minibatches _{x_<sup>real</sup> _v }_<sup>_n_</sup> _v_ =1<sup>t</sup><sup>_,_rfrom</sup><sup>_X_real.</sup> 

- 23: Encode them using the current encoder as _zu_<sup>sim</sup> = Ω _θ_ ( _x_<sup>sim</sup> _u_<sup>),</sup><sup>_z_</sup> _v_<sup>real</sup> = Ω _θ_ ( _x_<sup>real</sup> _v_ ). 

- 24: Compute the stabilized weights _w_ ¯ _u_ using the frozen Ω _θ_ 0 and ˆ _ι_ according to (65). 

- 25: Compute the weighted MMD loss in (66). 

- 26: Update the encoder parameter _θ_ by minimizing (63). 27: **end for** 28: Set _θ_ 0 _← θ_ . 

- 29: Decay trust-region weight _β ← µβ_ . 30: **end for** 

31: **return** encoder Ω _θ_ and policy _πψ_ . 

_1) Communication parameter setup:_ Following the 3GPP TR 38.901 indoor-office channel model [28], the path-loss model supports both LOS and NLOS conditions, with the user mobility set to 3 km/h. For room-scale indoor XR teleoperation, we consider the distance in [3 _,_ 30] m and _fc_ = 7 GHz. To account for shadow fading and occasional 

human-body or device blockage, we generate the channel gain 10 lg _g_ ( _t_ ) _∈_ [ _−_ 105 _, −_ 55] dB. _N_ 0 is set to -174 dBm/Hz, _B_ = 100 MHz. _ζ_ = 3 _×_ 10<sup>4</sup> and _λ_ E = 5. 

_2) Real-world and simulator platform:_ The real-domain dataset _D_ real is constructed based on Humanoid Everyday, a comprehensive public dataset that contains motion data collected by Apple Vision Pro [4] and humanoid robot data recorded in real-world task scenarios [29]. For _D_ sim, we develop a customized simulation environment named wireless <u>xr teleoperate</u> based on the unitree <u>sim isaaclab</u> in the Unitree toolkit xr <u>teleoperate</u> [30]. The underlying simulator is built on NVIDIA Isaac Sim 4.5.0 and Isaac Lab. To ensure that the simulator in unitree <u>sim isaaclab</u> matches the robot embodiment, end-effector type, and task category of the Humanoid Everyday real-world dataset, we use the same Unitree G1-29DoF humanoid robot equipped with Dex3 dexterous hands [30] in both the real-world and simulation domains, and select similar tabletop manipulation tasks. The take <u>out the lid of the spray bottle g1</u> scenario in Humanoid Everyday is used to construct _D_ real. In the unitree <u>sim isaaclab</u> environment, the Isaac-PickPlace-CylinderG129-Dex3-Joint task is used to construct the interactive simulator _M_ sim and collect _D_ sim. 

In Humanoid Everyday, **q**<sup>xr</sup> includes the 9-dimensional operator head orientation, the 16-dimensional left and right wrist poses, and the 7-dimensional left and right Dex3 dexteroushand actions, i.e., total dimensions _J_ xr = 55. Since the type of each sampling-rate dimension is float64, _dj_ = 64 bits. The execution-side **q**<sup>rb</sup> is constructed from the G1-Dex3 joint states, including 7 joints for each arm, 7 joints for each hand, 6 joints for each leg, and 3 waist joints. Hence, the robotside has totally _J_ rb = 43 joints. Considering that tabletop manipulation task is mainly sensitive to arm and dexteroushand motions, we set _wj_ to 1.0 for arm joints, 1.5 for hand joints, 0.5 for leg joints, 0.75 for waist joints in **W** . Since all trajectories in Humanoid Everyday are recorded at 30 Hz, the motion data collected by Apple Vision Pro are also recorded at 30 Hz. In practice, Apple Vision Pro [4] can support a 90 Hz sampling rate, while Meta Quest 3 [3] also provides a 120 Hz high-rate mode. Therefore, we adopt an emulation method of sampling-rate levels. Specifically, four normalized raw-rate levels, i.e., _{_ 0 _,_ 10 _,_ 20 _,_ 30 _}_ Hz, are first constructed from the original 30 Hz motion records through temporal downsampling. These rate levels are then mapped to the target XR communication-rate set _Fj_ = _{_ 0 _,_ 30 _,_ 60 _,_ 120 _}_ Hz. Under this mapping, the resulting sampled data are further processed through the sampling, transmission, interpolation, and reconstruction pipelines defined in Section II. This design enables the public 30 Hz dataset to preserve the reconstructionerror differences among different sampling-rate levels, while matching the transmission load of high-rate XR teleoperation. 

_3) Algorithm design details: L_ = 5, _λ_<sup>0</sup> MMD<sup>=1,</sup><sup>_λ_reg=</sup> 10<sup>_−_5</sup> , _αℓ_ = 0 _._ 2, _σℓ_ = 2<sup>_ℓ−_3</sup> _σ_ 0, where _σ_ 0 is the pairwise distance median after merging simulator and real latent samples in Section IV-A. _γ_ = 0 _._ 99, _ϵ_ = 0 _._ 2, _λ_ GAE = 0 _._ 95 in Section IV-B. _ϵw_ = 10<sup>_−_8</sup> in Section IV-C. Iterations _K_ 0 = 500, _K_ 1 = 25, _K_ 2 = 40, _K_ 3 = 10, trust-region _β_ 0 = 1, _µ_ = 0 _._ 95. 

11 


Fig. 5: Performance comparison under different channel gains. 

## _B. Performance Evaluation_ 

The training convergence is shown in Fig. 4. The total reconstruction error and total effective communication energy are accumulated over _T_ slots within each episode. DR-PPOuLSIF and DR-PPO-KLIEP denote two weighted PPO algorithms using different density-ratio estimation methods. Both methods eventually reach similar performance. In comparison, DR-PPO-uLSIF converges faster and achieves slightly better performance, whereas DR-PPO-KLIEP exhibits larger fluctuations during training. The faster and smoother convergence of DR-PPO-uLSIF is mainly attributed to the more stable densityratio estimates produced by least-squares fitting, while KLIEP is more sensitive to sample variability. 

Three baselines are included in Fig. 5 for ablation. **PPOMMD** performs PPO training with MMD-based latent domain but without density-ratio reweighting. **Unweighted PPO** removes importance weighting and is trained without realworld data. **FT** directly adopts full-rate transmission without learning policy. The wireless channel condition in dB is given by 10 lg _g_ ( _t_ ). According to Fig. 5a, the proposed DR-PPOuLSIF and DR-PPO-KLIEP methods achieve significantly lower reconstruction errors than other policy methods. Unweighted PPO performs the worst due to sim-to-real distribution mismatch. Although FT attains the lowest reconstruction error under severely degraded channel conditions, its energy cost becomes prohibitive. As shown in Fig. 5b, when 10 lg _g_ ( _t_ ) = _−_ 105 dB, the energy consumption of 

FT is tens of times higher than that of the policy-learning methods. Moreover, Fig. 5b shows that DR-PPO-uLSIF and DR-PPO-KLIEP reduce the effective communication energy to approximately half of that required by Unweighted PPO and PPO-MMD when the channel deteriorates to _−_ 105 dB. As the channel improves, the proposed methods adaptively exploit the more favorable transmission condition by allocating higher sampling rates, thereby achieving a better tradeoff between reconstruction accuracy and long-term communication energy efficiency. 

Fig. 6 present the dimension-wise sampling-rate decisions obtained by the DR-PPO-uLSIF under the channel condition 10 lg _g_ ( _t_ ) = _−_ 80 dB. The two figures correspond to the same 10000 ms time segment. The associated motion trajectories are extracted from take <u>out the lid of the spray bottle g1,</u> which is held out for validation. By comparing two subfigures, it can be observed that the sampling rates in Fig. 6b are significantly higher than those in Fig. 6a. This is because the 10-th dimension, _q_ 10<sup>xr(</sup><sup>_ν_)inFig.6a,istheposevalueof</sup> the left-wrist in rotation matrix, whereas the 50-th dimension, _q_ 50<sup>xr(</sup><sup>_ν_) in Fig. 6b is an angle value of the right Dex3 dexterous</sup> hand. Compared with the wrist component, the dexterous-hand component contains higher frequency motion, and therefore requires a higher sampling rate to preserve reconstruction accuracy. In Fig. 6a, it can be observed that the sampling rate increases when the pose value exhibits larger temporal variations. These results demonstrate that the DR-PPO-uLSIF algorithm can learn motion-adaptive sampling-rate decisions 

12 


Fig. 6: Dimension-wise sampling-rate decisions generated by DR-PPO-uLSIF. 

and effectively respond to time-varying XR motion dynamics. 

## VI. CONCLUSION 

This paper investigated sim-to-real communication-rate optimization for humanoid-robot wireless XR teleoperation. We developed a unified framework integrating motion sampling, wireless transmission, and simulator-physical execution to address the coupled challenges of energy efficiency and simto-real mismatch. By establishing a PAC-Bayes generalization characterization based on latent density-ratio estimation and representation bias, we provided theoretical insights into robust policy transfer under distribution shift. Building on this analysis, we proposed a domain-adaptive RL framework with latent density-ratio corrected PPO and trust-region regularization. Experimental results demonstrated superior energy–reconstruction tradeoffs and enhanced robustness under diverse wireless environments and dynamic humanoid motion trajectories. These findings highlight the importance of integrating theoretical generalization analysis with domainadaptive communication intelligence for future wireless embodied AI systems. 

## APPENDIX: DENSITY RATIO ESTIMATION IN LATENT SPACE 

This appendix summarizes the density-ratio estimation procedures used in Stage 1. The goal is to estimate the realto-simulator density ratio in the latent space induced by the frozen encoder Ω _θ_ 0. Let _{x_ ˜ _u_<sup>sim</sup><sup>_}n_</sup> _u_ =1<sup>_ι,s_and</sup><sup>_{x_˜</sup> _v_<sup>real</sup> _}_<sup>_n_</sup> _v_ =1<sup>_ι,r_denote</sup> the simulator and real-domain samples used for density-ratio estimation, obtained from _Sι_ and _X_ real, respectively. Their latent representations under Ω _θ_ 0 are 


For _† ∈{_ sim _,_ real _}_ , the latent distribution induced by _z_ = Ω _θ_ 0( _x_ ) with _x ∼ P†_ is defined as 


Since _P_ real _≪ P_ sim, the pushforward distributions also satisfy _P_ real<sup>_θ_0</sup><sup>_≪P_</sup> sim<sup>_θ_0</sup><sup>_._The target real-to-simulator density ratio</sup> in the latent space is defined as 


To approximate the target ratio in (70), we use a kernel basis model with _M_ basis functions. Let _ξ_ = [ _ξ_ 1 _, . . . , ξM_ ]<sup>_⊤_</sup> denote the coefficient vector, where _ξm_ is the coefficient of the _m_ -th basis function. The parametric density-ratio model is 


where _{cm}_<sup>_M_</sup> _m_ =1<sup>arekernelcentersand</sup><sup>_ϖ_(</sup><sup>_·, ·_)isthekernel</sup> function. The feature vector is defined as 


Once the coefficient vector is estimated by uLSIF or KLIEP, denoted by _ξ_<sup>ˆ</sup> , the latent density-ratio estimator used in Section IV-B is given by ˆ _ι_ ( _z_ ) = _ιξ_ ˆ( _z_ ). This estimator is the raw density-ratio estimate. Its clipping and normalization are performed separately in Sections III-C, IV-B, and IV-C. 

_A.1 uLSIF: Unconstrained Least-Squares Importance Fitting_ 

uLSIF estimates _ι_<sup>_⋆_</sup> _θ_ 0<sup>(</sup><sup>_z_)bysolvingtheregularizedleast-</sup> squares objective 

1 min 2<sup>_,_</sup> (73) _ξ_ 2<sup>E</sup><sup>_z∼P_</sup> sim<sup>_θ_0[</sup><sup>_ιξ_(</sup><sup>_z_)2]</sup><sup>_−_E</sup><sup>_z∼P_</sup> real<sup>_θ_0[</sup><sup>_ιξ_(</sup><sup>_z_)] +</sup><sup>_λ_</sup> 2<sup>_ι∥ξ∥_2</sup> where _λι >_ 0 is the _ℓ_ 2 regularization weight. Using samples _{z_ ˜ _u_<sup>sim</sup> _}_<sup>_n_</sup> _u_ =1<sup>_ι,_sand</sup><sup>_{z_˜</sup> _v_<sup>real</sup> _}_<sup>_n_</sup> _v_ =1<sup>_ι,_r,weminimize</sup> 


Define the empirical matrices 


13 

Then, we have 


In implementation, we optionally clip _ιξ_ ˆ( _z_ ) to be nonnegative. _A.2 KLIEP: Kullback–Leibler Importance Estimation Procedure_ 

KLIEP estimates _ι_<sup>_⋆_</sup> _θ_ 0<sup>(</sup><sup>_z_)byminimizingKLdivergencebe-</sup> tween the target latent distribution and the reweighted simulator latent distribution. Up to constants independent of _ξ_ , 


Using samples _{z_ ˜ _u_<sup>sim</sup> _}_<sup>_n_</sup> _u_ =1<sup>_ι,s_and</sup><sup>_{z_˜</sup> _v_<sup>real</sup> _}_<sup>_n_</sup> _v_ =1<sup>_ι,r_,theobjectiveis</sup> denoted by 


where _ς >_ 0 controls the constraint penalty, and (82) is under the constraint _ξ ⪰_ 0. 

The gradient of (82) with respect to _ξm_ is given by 


In practice, (82) is optimized by a constrained quasi-Newton method (e.g., L-BFGS-B) to enforce _ξ ≥_ 0 [31]. 

## REFERENCES 

- [1] K. Black, M. Y. Galliker, and S. Levine, “Real-time execution of action chunking flow policies,” in _Proc. Adv. Neural Inf. Process. Syst. (NeurIPS)_ , 2026. 

- [2] L. Li, Q. Zhang, Y. Luo, S. Yang, R. Wang, F. Han, M. Yu, Z. Gao, N. Xue, X. Zhu _et al._ , “Causal world modeling for robot control,” _arXiv preprint arXiv:2601.21998_ , 2026. 

- [3] “Meta Quest 3”, (2025), https://www.meta.com/quest/quest-3/. 

- [4] “Apple Vision Pro”, https://www.apple.com/apple-vision-pro/. 

- [5] X. Wei, C. Yang, and S. Han, “Prediction, communication, and computing duration optimization for vr video streaming,” _IEEE Trans. Commun._ , vol. 69, no. 3, pp. 1947–1959, 2021. 

- [6] Q. Cheng, H. Shan, W. Zhuang, L. Yu, Z. Zhang, and T. Quek, “Design and analysis of mec- and proactive caching-based 360<sup>_◦_</sup> mobile vr video streaming,” _IEEE Trans. Multimedia_ , vol. 24, pp. 1529–1544, 2022. 

- [7] Z. Chen, H. Zhu, L. Song, D. He, and B. Xia, “Wireless multiplayer interactive virtual reality game systems with edge computing: Modeling and optimization,” _IEEE Trans. Wireless Commun._ , vol. 21, no. 11, pp. 9684–9699, 2022. 

- [8] C. Xu, Z. Chen, M. Tao, and W. Zhang, “Wireless multi-user interactive virtual reality in metaverse with edge-device collaborative computing,” _IEEE Trans. Wireless Commun._ , pp. 1–1, 2025. 

- [9] Z. Meng, K. Chen, Y. Diao, C. She, G. Zhao, M. A. Imran, and B. Vucetic, “Task-oriented cross-system design for timely and accurate modeling in the metaverse,” _IEEE J. Sel. Areas Commun._ , vol. 42, no. 3, pp. 752–766, 2024. 

- [10] Z. Meng, C. She, G. Zhao, and D. De Martini, “Sampling, communication, and prediction co-design for synchronizing the real-world device and digital model in metaverse,” _IEEE J. Sel. Areas Commun._ , vol. 41, no. 1, pp. 288–300, 2023. 

- [11] T. Huang, J. Ren, H. Wang, Z. Wang, Q. Ben, M. Wen, X. Chen, J. Li, and J. Pang, “Learning Humanoid Standing-up Control across Diverse Postures,” in _Proc. Robot. Sci. Syst. (RSS)_ , Los Angeles, CA, USA, June 2025. 

- [12] T. He, J. Gao, W. Xiao, Y. Zhang, Z. Wang, J. Wang, Z. Luo, G. He, N. Sobanbabu, C. Pan, Z. Yi, G. Qu, K. Kitani, J. Hodgins, L. J. Fan, Y. Zhu, C. Liu, and G. Shi, “Asap: Aligning simulation and real-world physics for learning agile humanoid whole-body skills,” in _Proc. Robot. Sci. Syst. (RSS)_ , 2025. 

- [13] R.-Z. Qiu, S. Yang, X. Cheng, C. Chawla, J. Li, T. He, G. Yan, L. Paulsen, G. Yang, S. Yi, G. Shi, and X. Wang, “Humanoid policy _∼_ human policy,” _Proc. Conf. Robot Learn. (CoRL)_ , 2025. 

- [14] H. Xue, T. He, Z. Wang, Q. Ben, W. Xiao, Z. Luo, X. Da, F. Casta˜neda, G. Shi, S. Sastry, L. J. Fan, and Y. Zhu, “Opening the sim-to-real door for humanoid pixel-to-action policy transfer,” 2026, accepted to Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR). 

- [15] C. Zhao, G. Fang, H. Ding, X. Liu, F. Wang, G. Wang, K. Zhao, Z. Wang, and W. Xi, “Federated multi-source domain adaptation for mmwave-based human activity recognition,” _IEEE Trans. Mobile Comput._ , vol. 24, no. 8, pp. 7283–7296, 2025. 

- [16] X. Zhou, Y. Tian, and X. Wang, “Mec-da: Memory-efficient collaborative domain adaptation for mobile edge devices,” _IEEE Trans. Mobile Comput._ , vol. 23, no. 5, pp. 3923–3937, 2024. 

- [17] P. Chen, K. Zhang, S. Gao, K. He, and J. Lv, “Achieving cross-domain NLOS localization via edge-assisted semi-supervised learning,” _IEEE Trans. Wireless Commun._ , vol. 24, no. 9, pp. 7424–7436, 2025. 

- [18] M. Sugiyama, S. Nakajima, H. Kashima, P. von B¨unau, and M. Kawanabe, “Direct importance estimation with model selection and its application to covariate shift adaptation,” _Ann. Inst. Stat. Math._ , vol. 60, no. 4, pp. 699–746, 2008. 

- [19] T. Kanamori, S. Hido, and M. Sugiyama, “A least-squares approach to direct importance estimation,” _J. Mach. Learn. Res._ , vol. 10, pp. 1391– 1445, 2009. 

- [20] A. Gretton, K. M. Borgwardt, M. J. Rasch, B. Sch¨olkopf, and A. Smola, “A kernel two-sample test,” _J. Mach. Learn. Res._ , vol. 13, no. 25, pp. 723–773, 2012. 

- [21] M. Long, Y. Cao, J. Wang, and M. I. Jordan, “Learning transferable features with deep adaptation networks,” in _Proc. Int. Conf. Mach. Learn. (ICML)_ , vol. 37, 2015, pp. 97–105. 

- [22] B. Sun and K. Saenko, “Deep CORAL: Correlation alignment for deep domain adaptation,” in _Proc. Eur. Conf. Comput. Vis. Workshops (ECCVW)_ . Springer, 2016, pp. 443–450. 

- [23] M. Seeger, “Pac-bayesian generalisation error bounds for gaussian process classification,” _J. Mach. Learn. Res._ , vol. 3, pp. 233–269, 2002. 

- [24] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _arXiv:1707.06347_ , 2017. 

- [25] J. Schulman, S. Levine, P. Abbeel, M. I. Jordan, and P. Moritz, “Trust region policy optimization,” in _Proc. Int. Conf. Mach. Learn. (ICML)_ , vol. 37, 2015, pp. 1889–1897. 

- [26] G. B. Folland, _Real Analysis: Modern Techniques and Their Applications_ , 2nd ed. New York, NY, USA: John Wiley & Sons, 1999. 

- [27] J. Schulman, P. Moritz, S. Levine, M. Jordan, and P. Abbeel, “Highdimensional continuous control using generalized advantage estimation,” in _Proc. Int. Conf. Learn. Represent. (ICLR)_ , 2016. 

- [28] 3GPP, “ETSI TR 138 901 V16.1.0: 5G; Study on channel model for frequencies from 0.5 to 100 GHz (3GPP TR 38.901 version 16.1.0 release 16)”, European Telecomm. Std. Institute (ETSI), 2020. https://www.etsi.org/deliver/etsi <u>tr/138900 138999/138901/16.01.00 60/</u> tr <u>138901v160100p.pdf.</u> 

- [29] Z. Zhao, H. Jing, X. Liu, J. Mao, A. Jha, H. Yang, R. Xue, S. Zakharor, V. Guizilini, and Y. Wang, “Humanoid everyday: A comprehensive robotic dataset for open-world humanoid manipulation,” _arXiv preprint arXiv:2510.08807_ , 2025. 

- [30] Unitree Robotics, “XR-Teleoperate: An open-source teleoperation framework and data collection toolkit for embodied intelligence,” https://github.com/unitreerobotics/xr <u>teleoperate,</u> 2024. 

- [31] C. Zhu, R. H. Byrd, P. Lu, and J. Nocedal, “Algorithm 778: L-bfgsb: Fortran subroutines for large-scale bound-constrained optimization,” _ACM Trans. Math. Softw._ , vol. 23, no. 4, pp. 550–560, 1997. 

