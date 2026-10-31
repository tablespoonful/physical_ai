---
title: "RecoverFormer: End-to-End Contact-Aware Recovery for Humanoid Robots"
date: "2026-04-24"
authors: "Zihui Liu"
url: https://arxiv.org/abs/2604.22911
pdf: https://arxiv.org/pdf/2604.22911
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2604.22911)** / [論文ページ](https://arxiv.org/abs/2604.22911)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# RecoverFormer: End-to-End Contact-Aware Recovery for Humanoid Robots 

Zihui Liu 

_Stanford University_ zl90@alumni.stanford.edu 

**_Abstract_ —Humanoid robots operating in unstructured environments must recover from unexpected disturbances—a capability that remains challenging for end-to-end control policies. We present RECOVERFORMER, a fully end-to-end humanoid recovery policy that learns** **_when_ and** **_how_ to switch among recovery behaviors—including compensatory stepping, hand-environment contact, and center-of-mass reshaping—while maintaining robust performance under model mismatch. The architecture combines a causal transformer over a 50-step observation history with two novel heads: a** **_latent recovery mode_ that enables smooth transitions among distinct recovery strategies, and a** **_contact affordance head_ that predicts which environmental surfaces (walls, railings, table edges) are beneficial for stabilization. We evaluate RECOVERFORMER on the Unitree G1 humanoid in MuJoCo. Trained only on open floor, RECOVERFORMER transfers** **_zeroshot_ to walled environments, achieving 100** % **recovery success across 100–300 N pushes and across wall distances from** 0 _._ 25 **–** 1 _._ 4 **m. Under zero-shot dynamics mismatch, RECOVERFORMER reaches** 75 _._ 5% **at** +25% **mass,** 89% **under** 30 **ms latency,** 91 _._ 5% **at low friction, and** 99% **under compound friction** + **latency** + **mass perturbation. The learned latent modes specialize across force regimes without mode-level supervision, validated by t-SNE analysis of 300 episodes. Taken together, these results show that a single end-to-end policy can deliver multi-modal, contactaware humanoid recovery that generalizes across perturbation magnitude, contact geometry, and dynamics shift.** 

**_Index Terms_ —Humanoid robots, fall recovery, contact-aware control, end-to-end learning, reinforcement learning** 

## I. INTRODUCTION 

Humanoid robots are increasingly deployed in unstructured human environments where unexpected perturbations— collisions, slippery surfaces, payload shifts—can destabilize the robot and cause falls. Unlike wheeled or quadruped platforms, humanoid robots have a narrow support polygon and high center of mass, making balance recovery a safety-critical capability [1]. 

**The recovery problem.** When a humanoid is pushed beyond its balance limits, effective recovery requires choosing among qualitatively different strategies: taking a compensatory step, bracing against a nearby surface, or rapidly lowering the center of mass. Humans perform this selection seamlessly, exploiting environmental affordances—a wall to lean on, a railing to grasp—in a fraction of a second. Current humanoid systems lack this integrated capability. 

**Why this is hard.** Classical humanoid recovery has historically relied on capture-point stepping [2] and on real- 


Fig. 1: **RECOVERFORMER maintains balance through a lateral push on the Unitree G1.** Mid-recovery snapshot 160 ms after a 180 N torso impulse. The transformer policy converts a 50-step history of proprioception and contact-region distances into 29-DoF joint targets at 50 Hz. 

time multi-contact planning that synthesizes hand braces against known surfaces [3]. Recent learning-based protective controllers [4] retain a fixed posture vocabulary, and unified multi-contact fall mitigation methods [5] still depend on offline contact databases. End-to-end fall recovery via residual learning [6], the unified recovery framework of Xu et al. [7], and the broader literature on robust self-balancing for low-DoF wheeled platforms [8] illustrate the diversity of strategies but do not jointly reason about environmental contact opportunities. Modern learned stand-up policies [9] and HoST [10] focus on getting up _after_ a fall; complementarily, online dynamics calibration developed for autonomous driving [11] suggests that history-based identification can adapt control to deployment-time mismatch, but none of these unify proactive recovery with contact-aware decision-making. Meanwhile, whole-body humanoid control has achieved remarkable 

progress in locomotion [12], [13], expressive motion [14], [15], sequential contact [16], and language-conditioned control [17], [18], but these are designed for nominal operation. 

**Our approach.** We propose RECOVERFORMER, an end-toend learned policy that unifies balance recovery with contactaware decision-making. Our key insight is that recovery is _multi-modal_ : the robot must choose among qualitatively different strategies depending on the perturbation and available environmental supports. Rather than hard-coding this choice, we learn a _latent recovery mode zt_ that segments the recovery behavior space while preserving end-to-end differentiability. We augment this with a _contact affordance head_ that scores candidate contact regions, enabling the policy to decide whether and where to brace. A core design choice is a causal transformer over a 50-step observation history, which we show enables implicit system identification under unseen friction, latency, and mass perturbations—handling the reality gap without any online parameter updates. 

**Contributions.** (1) We formulate humanoid recovery as a multi-modal end-to-end learning problem and propose RECOVERFORMER, a transformer-based architecture combining latent recovery mode prediction, contact affordance estimation, and a causal-history encoder. (2) We introduce a _latent recovery mode_ mechanism with entropy and utilization regularizers that discovers interpretable recovery modes purely from reward, with no mode-level supervision. (3) We design a _contact affordance head_ that predicts the stabilization value of candidate surfaces, yielding zero-shot generalization from open-floor training to walled environments. (4) We demonstrate that the 50-step causal-history encoder enables implicit system identification, sustaining _≥_ 75% recovery under unseen mass, latency, and compound dynamics mismatch. 

## II. RELATED WORK 

**Humanoid fall/push recovery.** Classical fall-recovery controllers rely on model-based planning with simplified dynamics and precomputed contact databases [1], [5], [3], and capture-point stepping [2]—requiring known geometry and restricting generalization. Recent learning-based work, including SafeFall [4], FRASA [6], Xu et al. [7], He et al. [9], and HoST [10], trains end-to-end policies for protective or stand-up behaviors, but none explicitly predict or exploit environmental contact opportunities during recovery. 

**End-to-end and contact-aware whole-body control.** Causal transformer policies for humanoid locomotion [12], [13], expressive motion [14], [15], unified control [19], sequential contacts [16], and language-conditioned control [17], [18], [20], [21], [22] target nominal operation, not the extremeperturbation regime. Contact affordance has been studied primarily in manipulation [23], [24], [25], [26]; we instead predict contact _value for recovery_ . VLA models [27], [28], [29], [30] are complementary: RECOVERFORMER could serve as a recovery module within such a stack. 

**Adaptation via observation history.** RMA [31] showed that proprioceptive history enables online adaptation of legged policies to changing dynamics; WorMI [32], TARC [33], and 

ASAP [21] extend this with world-model composition, learned action durations, and delta action models, while structuredmemory architectures from the broader sequential decisionmaking literature [34] explore alternative representations of past context. In RECOVERFORMER, the causal transformer over 50 steps plays the same role implicitly—we show in Sec. V-C that this is sufficient for recovery under friction, latency, and mass mismatch without any explicit adaptation module or online parameter updates. 

## III. PROBLEM FORMULATION 

We formulate humanoid recovery as a partially observed Markov decision process _M_ = ( _S, A, O, P, R, γ_ ). The underlying state _st ∈S_ contains the robot’s full kinematic and dynamic configuration together with contact-geometry parameters. At each timestep _t_ the robot receives a partial observation _ot ∈O ⊆_ R<sup>106</sup> containing proprioceptive state (joint positions _qt ∈_ R<sup>29</sup> , velocities _q_ ˙ _t ∈_ R<sup>29</sup> , projected gravity _gt ∈_ R<sup>3</sup> , torso angular and linear velocity _ωt, vt ∈_ R<sup>3</sup> , previous action), binary foot contact indicators _ft ∈{_ 0 _,_ 1 _}_<sup>2</sup> , and environmental perception _dt ∈_ R<sup>_Kc_</sup> (distances from each hand to _Kc_ = 8 candidate contact regions). The policy maintains a causal history buffer 


and outputs target joint positions _at ∈_ R<sup>29</sup> that are tracked by a joint-level PD controller at 50 Hz ( _τi_ = _kp_ ( _qi_<sup>ref</sup> _− qi_ ) _− kd_ ˙ _qi_ ). The transition _st_ +1 _∼ P_ ( _· | st, at_ ) includes sparse push events: at a uniformly sampled time _tp ∈_ [1 _,_ 3] s an impulse of magnitude _∥F ∥∼U_ (50 _,_ 200) N and direction _θ ∼U_ (0 _,_ 2 _π_ ) is applied to the torso over one control step. 

Given this MDP, the objective is the standard discounted return 


with _γ_ =0 _._ 99 and _T_ = 500 (10 s), under rewards designed so that the optimal policy (1) minimises recovery time, (2) exploits available environmental contacts when beneficial, and (3) remains robust to unseen friction, latency, and mass perturbations (Sec. IV-E). 

## IV. METHOD 

RECOVERFORMER is a transformer-based policy with two novel heads: a latent recovery mode predictor and a contact affordance head, both conditioned on a causal-transformer observation encoder over a 50-step history (Fig. 2). 

## _A. Observation Encoder_ 

Each observation frame _ot ∈_ R<sup>106</sup> (29 joint positions, 29 joint velocities, 3 projected gravity, 3 torso angular velocity, 3 linear velocity, 2 foot contacts, 8 contact-region distances, 29 previous actions) is linearly projected to embedding dimension _d_ = 256 and augmented with a learned positional code _pi ∈_ R<sup>_d_</sup> ( _i_ = 1 _, . . . ,H_ ): 


Fig. 2: **RECOVERFORMER architecture.** A causal transformer encodes the 50-step observation history into _et_ . The latent mode head predicts _zt_ over _K_ = 4 modes; the affordance head predicts _ct ∈_ [0 _,_ 1]<sup>_Kc_</sup> . Both feed the action decoder. 

_X_ is processed by _L_ = 4 identical causal transformer blocks, each implementing masked multi-head self-attention (MHSA) with _Hh_ = 4 heads followed by a feed-forward sublayer: 


Each MHSA head computes scaled dot-product attention with a lower-triangular causal mask _M ∈{_ 0 _, −∞}_<sup>_H×H_</sup> [35]: 


with _dk_ = _d/Hh_ per-head dimension. Causal masking ( _Mij_ = _−∞_ for _j > i_ ) ensures each timestep attends only to its past, enabling streaming deployment. We read out the encoder state from the final timestep of the last block: _et_ = _XH_<sup>_′_(</sup><sup>_L_)</sup> _∈_ R<sup>_d_</sup> . 

## _B. Latent Recovery Mode_ 

We predict a _latent recovery mode zt_ that captures the qualitative recovery strategy as a categorical variable over _K_ = 4 discrete modes. A linear head with temperature _τ_ produces the mode posterior 


During training we use a differentiable soft mixture of learned mode embeddings 


which keeps the PPO importance ratio well-defined; at inference we use _k_<sup>_⋆_</sup> = arg max _k pθ_ ( _zt_ = _k | et_ ). The temperature is annealed _τ_ : 1 _._ 0 _→_ 0 _._ 1. Modes receive _no direct supervision_ ; to prevent collapse we add an entropy term and a batch-level utilization penalty: 


where _p_ ¯ _k_ = _N_ <u>1</u> � _n_<sup>_pθ_(</sup><sup>_zt_=</sup><sup>_k|e_</sup> _t_<sup>(</sup><sup>_n_)</sup> ) is the empirical batch usage and _u_ min = 0 _._ 4 _/K_ ; this avoids collapse to a single mode (Sec. V-D). 

## _C. Contact Affordance Head_ 

The contact affordance head predicts the stabilization value of the _Kc_ = 8 candidate contact regions: 


with _σ_ the element-wise logistic. Each _c_<sup>(</sup> _t_<sup>_i_)</sup> represents the predicted benefit of making contact with region _i_ (a wall, railing, or table edge). The affordance head receives _no direct supervision_ : it is trained through PPO gradients flowing from the reward term 


where “useful” fires when a hand touches a geometry whose contact normal opposes the fall direction, and “harmful” fires for wrist-over-torso impacts. The affordance is an _implicit representation_ of which surfaces PPO has found informative; Sec. V-B shows this suffices for zero-shot transfer to walled environments never seen during training. 

## _D. Action Decoder_ 

The decoder concatenates encoder state, mode mixture embedding, and affordance vector and decodes a whole-body joint target: 


with output clipped to [ _−_ 1 _,_ 1] and converted to joint targets _qt_<sup>ref</sup> = _q_<sup>def</sup> + _α at_ (action scale _α_ =0 _._ 25 rad) for the onboard PD controller. 

## _E. Training_ 

RECOVERFORMER is trained end-to-end using PPO [36] in MuJoCo [37] with the Unitree G1-29dof model. **Reward.** The total reward decomposes as 


where _r_ up sums exponential-kernel terms for projected gravity, base height, COM, default pose, bilateral foot contact, and 

TABLE I: Open-floor RSR (%) across 50–300 N, 200 episodes per force. 

|Force (N)|50|100|150|200|250|300|
|---|---|---|---|---|---|---|
|RECOVERFORMER|100.0|100.0|85.0|79.0|68.0|68.0|


a per-step alive bonus; _r_ contact is Eq. (10) (active only in walled/cluttered envs); _r_ reg = _−λa∥at∥_<sup>2</sup> _− λa_ ˙ _∥at − at_ [ _−_ 1] _∥_<sup>2</sup> discourages jittery actions; and _w_ term=200 is a large termination penalty. 

TABLE II: Zero-shot walled-environment RSR (%). Models trained on open floor only. 

|Force (N)|100|150|200|250|300|
|---|---|---|---|---|---|
|RECOVERFORMER|**100**|**100**|**100**|**100**|**100**|


TABLE III: RSR (%) under zero-shot dynamics mismatch (150 N push, 200 episodes). 

||Nominal|Low|_µ_ Lat. 30 ms|+25%_m_|Compound|
|---|---|---|---|---|---|
|RECOVERFORMER|93.5|91.5|89.0|**75.5**|**99.0**|


**PPO objective.** Let _rt_ ( _θ_ ) = _πθ_ ( _at | ht_ ) _/πθ_ old( _at | ht_ ) and let _A_<sup>ˆ</sup> _t_ denote the GAE advantage 


with _γ_ =0 _._ 99, _λ_ =0 _._ 95. The PPO-clip surrogate is 


with clip _ϵ_ =0 _._ 2, _cv_ =0 _._ 5, _cH_ =0 _._ 01, and target _R_<sup>ˆ</sup> _t_ = _A_<sup>ˆ</sup> _t_ + _Vϕ_ ( _ht_ ). The value network _Vϕ_ shares the transformer encoder with the actor and attaches a scalar head to _et_ . 

**Combined objective.** The total loss is _L_ = _L_ PPO+ _β L_ mode with _β_ =0 _._ 1; the affordance head is trained implicitly through the PPO gradient of _r_ contact via the decoder’s dependence on _ct_ , without any auxiliary loss. 

**Domain randomization.** Push magnitudes sample _∥F ∥∼ U_ (50 _,_ 200) N, directions _θ ∼U_ (0 _,_ 2 _π_ ), timing _∼U_ [1 _,_ 3] s, and friction _µ ∈_ [0 _._ 5 _,_ 1 _._ 2]; mass, latency, and torque limits are tested zero-shot (Sec. V-C). 

## V. EXPERIMENTS 

We evaluate RECOVERFORMER on the Unitree G1 (29 DoF, 1.27 m, 35 kg) in MuJoCo with policy at 50 Hz, physics at 200 Hz. Environments: _Open floor_ and _Walled_ (walls at 0 _._ 3–1 _._ 0 m). Perturbations: torso impulses 50–300 N over 0 _._ 1 s across 8 directions (200 episodes per force-sweep condition, 100 per mismatch condition). Metric: Recovery Success Rate (RSR), the fraction of episodes in which the robot remains within 45<sup>_◦_</sup> tilt and returns to stable standing within 10 s. 

## _A. Open-Floor Push Recovery_ 

Fig. 3 shows a representative recovery trajectory at 150 N and Table I reports RSR across 50–300 N. RECOVERFORMER sustains 100% recovery for _≤_ 100 N, remains above 68% at 250–300 N, and degrades gracefully with force. Fig. 4 visualizes the underlying dynamics: the torso-tilt trace peaks within 0 _._ 05–0 _._ 15 s after the push, oscillates with a period matching the robot’s natural inverted-pendulum mode, and decays within 1–1 _._ 5 s. Peak tilt scales _sub-linearly_ with force (7<sup>_◦_</sup> at 100 N vs. 20<sup>_◦_</sup> at 250 N)—a signature of learned damping rather than a passive impulse response. Low-force perturbations are 

absorbed with in-place posture adjustments, while high-force perturbations elicit multi-step strategies (see Sec. V-D). 

## _B. Contact-Aware Recovery in Walled Environments_ 

We test _zero-shot_ generalization of contact-aware recovery: RECOVERFORMER is trained only on open floor, then evaluated without retraining in a walled environment where balancing may require using nearby walls. Table II shows 100% RSR at every force level from 100 to 300 N. The policy’s affordance head, learned purely from the open-floor contact reward, produces recovery motions that remain spatially compatible with the walls and, when useful, actively brace against them. 

**Wall distance and push direction sweeps.** Additional 100episode sweeps evaluate sensitivity to the geometry: RECOVERFORMER maintains **100** % RSR at every wall distance from 0 _._ 25 m to 1 _._ 40 m at 150 N, and 100% across all four push directions (toward/away from the wall and two lateral) at wall distance 0 _._ 5 m. The affordance head therefore generalizes across both the force magnitude and the detailed contact geometry, suggesting that the representation captures a general notion of “where a brace is available” rather than memorizing training-time wall layouts. 

## _C. Zero-Shot Robustness Under Dynamics Mismatch_ 

We evaluate four zero-shot physics perturbations at 150 N: low friction ( _µ_ =0 _._ 3), high latency ( _τ_ =30 ms), +25% upperbody mass, and all three combined (Table III). Across all single-axis perturbations RECOVERFORMER sustains _≥_ 89% RSR, and holds 75 _._ 5% even under +25% mass—a regime where single-step memoryless policies collapse. Under the _compound_ mismatch (friction+latency+mass) RECOVERFORMER reaches 99%: the 50-step history receives enough signal from multiple sources to disambiguate dynamics quickly, consistent with history-based system identification [31] but without a dedicated adaptation module. 

## _D. Latent Mode Interpretability_ 

We collect per-episode mode activations from 300 episodes spanning six force levels (50 each) and apply t-SNE (perplexity=30) to the episode-level mean mode vector _z_ ¯ _∈_ R<sup>_K_</sup> (Fig. 5). Low-force episodes (50–100 N) form a tight cluster with Mode 3 _≈_ 1; high-force episodes (150–300 N) spread into a distinct region as Modes 1 and 2 gain probability mass. 


Fig. 3: **Representative open-floor recovery rollout.** Frames: (0) pre-push stance; (1) impact with _F_ applied for 100 ms; (2) compensatory whole-body motion; (3) stabilizing + steady-state recovery phase. 


Fig. 4: **Representative balance trajectories on open floor.** (a) Torso tilt and (b) base height versus time during a single push episode at four force levels. The red band marks the 100 ms ms push interval at _t_ =1 _._ 0 s. s. The tilt envelope decays exponentially with damping ratio that scales inversely with force; the base height dip grows monotonically from 1 _._ 5 cm at 100 N to 6 _._ 5 cm at 250 N and recovers within _∼_ 1 s. Tilt remains well below the 45<sup>_◦_</sup> fall threshold across the entire force sweep. 

Fig. 5: **Latent mode t-SNE** (300 episodes, 6 force levels, 50 each). **Top** : colored by push force; low-force episodes cluster where Mode 3 _≈_ 1, high-force episodes spread as Modes 1 and 2 gain mass. **Bottom** : the same embedding colored by outcome; failures concentrate in the single-mode cluster while successes span the multi-mode region. 

Failure episodes concentrate predominantly in the single-mode region regardless of force: high-force episodes that respond with Mode 3 near 1 tend to fail, while those that distribute across multiple modes succeed. Successful high-force recovery therefore requires a multi-mode response, validating that the latent mode mechanism learns qualitatively meaningful recovery strategies without mode-level supervision. 

dicts _Kc_ = 8 contact-region values. We train with PPO using 64 parallel MuJoCo [37] environments for 5 _×_ 10<sup>6</sup> steps ( _≈_ 2 h on one RTX 5080), with rollout length 48, minibatch size 128, and 5 epochs per update. Hyperparameters: lr 3 _×_ 10<sup>_−_4</sup> , _γ_ =0 _._ 99, GAE _λ_ =0 _._ 95, _β_ =0 _._ 1, _cH_ =0 _._ 01, _cv_ =0 _._ 5, clip _ϵ_ =0 _._ 2; mode softmax temperature anneals _τ_ : 1 _._ 0 _→_ 0 _._ 1 linearly. Training pushes sample [50 _,_ 200] N uniformly with random direction and timing; the walled variant additionally randomizes wall positions at 0 _._ 3–1 _._ 0 m. Observations are normalized with running mean/variance statistics estimated online during rollouts. 

## VI. IMPLEMENTATION DETAILS 

The transformer encoder uses _L_ = 4 layers, _d_ = 256 embedding dimension, _Hh_ = 4 attention heads, and history _H_ = 50 (1 s at 50 Hz). The latent mode uses _K_ = 4 discrete modes with embedding size _dz_ =32; the affordance head pre- 

## VII. CONCLUSION 

We presented RECOVERFORMER, an end-to-end contactaware recovery policy combining a latent mode head, a contact affordance head, and a causal-transformer encoder over a 50step history. Despite training only on open floor, it transfers zero-shot to walled environments at 100% RSR across all tested forces and distances, sustains _≥_ 75% RSR under unseen mass, latency, and compound dynamics mismatch, and learns force-specialized modes from reward alone. Future work: simto-real transfer on the physical G1, integration with VLA planners [27], [28], [30] as a reactive recovery module, and visual perception for the affordance head. 

## REFERENCES 

- [1] S. Wang and K. Hauser, “Real-time stabilization of a falling humanoid robot using hand contact: An optimal control approach,” in _IEEERAS 17th International Conference on Humanoid Robots (Humanoids)_ . IEEE, 2017, pp. 454–460. 

- [2] E. Aslan, M. A. Arseric¸m, and A. Uc¸ar, “Development of push-recovery control system for humanoid robots using deep reinforcement learning,” _Ain Shams Engineering Journal_ , 2023. 

- [3] S. Wang and K. Hauser, “Realization of a real-time optimal control strategy to stabilize a falling humanoid robot with hand contact,” in _IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2018. 

- [4] Z. Meng, T. Liu, L. Ma, Y. Wu, R. Song, W. Zhang, and S. Huang, “SafeFall: Learning protective control for humanoid robots,” _arXiv preprint arXiv:2511.18509_ , 2025. 

- [5] S. Wang and K. Hauser, “Unified multi-contact fall mitigation planning for humanoids via contact transition tree optimization,” in _IEEERAS 18th International Conference on Humanoid Robots (Humanoids)_ . IEEE, 2018, pp. 1–9. 

- [6] C. Gaspard, M. Duclusaud, G. Passault, M. Daniel, and O. Ly, “FRASA: An end-to-end reinforcement learning agent for fall recovery and stand up of humanoid robots,” in _IEEE International Conference on Robotics and Automation (ICRA)_ , 2025. 

- [7] Z. Xu, Y. Li, K.-y. Lin, and S. X. Yu, “Unified humanoid fall-safety policy from a few demonstrations,” _arXiv preprint arXiv:2511.07407_ , 2025. 

- [8] A. M. Sharma, S. Wang, Y.-M. Zhou, and A. Ruina, “Towards a maximally-robust self-balancing bicycle without reaction-moment gyroscopes or reaction wheels,” in _Bicycle and Motorcycle Dynamics_ , 2016. 

- [9] X. He, R. Dong, Z. Chen, and S. Gupta, “Learning getting-up policies for real-world humanoid robots,” _arXiv preprint arXiv:2502.12152_ , 2025. 

- [10] T. Huang, J. Ren, H. Wang, Z. Wang, Q. Ben, M. Wen, X. Chen, J. Li, and J. Pang, “HoST: Learning humanoid standing-up control across diverse postures,” _arXiv preprint arXiv:2502.08378_ , 2025. 

- [11] S. Wang, C. Deng, and Q. Qi, “Efficient online calibration for autonomous vehicle’s longitudinal dynamical system: A Gaussian model approach,” in _Proceedings of the Conference_ , 2023. 

- [12] I. Radosavovic, T. Xiao, B. Zhang, T. Darrell, J. Malik, and K. Sreenath, “Real-world humanoid locomotion with reinforcement learning,” _Science Robotics_ , vol. 9, 2024. 

- [13] I. Radosavovic, B. Zhang, B. Shi, J. Rajasegaran, S. Kamat, T. Darrell, K. Sreenath, and J. Malik, “Humanoid locomotion as next token prediction,” in _Advances in Neural Information Processing Systems (NeurIPS)_ , 2024. 

- [14] X. Cheng, Y. Ji, J. Chen, R. Yang, G. Yang, and X. Wang, “ExBody: Expressive whole-body control for humanoid robots,” in _Robotics: Science and Systems (RSS)_ , 2024. 

   - [18] Y. Shao, B. Zhang, Q. Liao, X. Huang, Y. Gao, Y. Chi, Z. Li, S. Shao, and K. Sreenath, “LangWBC: Language-directed humanoid whole-body control via end-to-end learning,” in _Robotics: Science and Systems (RSS)_ , 2025. 

   - [19] T. He, W. Xiao, T. Lin, Z. Luo, Z. Xu, Z. Jiang, J. Kautz, C. Liu, G. Shi, X. Wang, L. Fan, and Y. Zhu, “HOVER: Versatile neural whole-body controller for humanoid robots,” _arXiv preprint arXiv:2410.21229_ , 2024. 

   - [20] H. Xue, X. Huang, D. Niu, Q. Liao, T. Kragerud, J. T. Gravdahl, X. B. Peng, G. Shi, T. Darrell, K. Sreenath, and S. Sastry, “LeVERB: Humanoid whole-body control with latent vision-language instruction,” _arXiv preprint arXiv:2506.13751_ , 2025. 

   - [21] T. He, J. Gao, W. Xiao, Y. Zhang, Z. Wang, J. Wang, Z. Luo, G. He, N. Sobanbabu, C. Pan _et al._ , “ASAP: Aligning simulation and real-world physics for learning agile humanoid whole-body skills,” in _Robotics: Science and Systems (RSS)_ , 2025. 

   - [22] W. Xie, J. Han, J. Zheng _et al._ , “KungfuBot: Physics-based humanoid whole-body control for learning highly-dynamic skills,” in _Advances in Neural Information Processing Systems (NeurIPS)_ , 2025. 

   - [23] J. A. Barreiros, A. O. Onol,<sup>¨</sup> M. Zhang, S. Creasey, A. Goncalves, A. Beaulieu, A. Bhat, K. M. Tsui, and A. Alspach, “Learning contactrich whole-body manipulation with example-guided reinforcement learning,” _Science Robotics_ , vol. 10, p. eads6790, 2025. 

   - [24] M. Murooka, T. Hoshi, K. Fukumitsu, S. Masuda, M. Hamze, T. Sasaki, M. Morisawa, and E. Yoshida, “TACT: Humanoid whole-body contact manipulation through deep imitation learning with tactile modality,” _IEEE Robotics and Automation Letters (RA-L)_ , vol. 10, no. 8, pp. 7819– 7826, 2025. 

   - [25] S. Nasiriany, S. Kirmani, T. Ding, L. Smith, Y. Zhu, D. Driess, D. Sadigh, and T. Xiao, “RT-Affordance: Affordances are versatile intermediate representations for robot manipulation,” _arXiv preprint arXiv:2411.02704_ , 2024. 

   - [26] R. Xu, J. Zhang, M. Guo _et al._ , “A0: An affordance-aware hierarchical model for general robotic manipulation,” in _International Conference on Computer Vision (ICCV)_ , 2025. 

   - [27] K. Black _et al._ , “ _π_ 0: A vision-language-action flow model for general robot control,” _arXiv preprint arXiv:2410.24164_ , 2024. 

   - [28] Figure AI, “Helix: A vision-language-action model for generalist humanoid control,” https://www.figure.ai/news/helix, 2025. 

   - [29] J. Bjorck, F. Casta˜neda, N. Cherniadev _et al._ , “GR00T N1: An open foundation model for generalist humanoid robots,” _arXiv preprint arXiv:2503.14734_ , 2025. 

   - [30] OpenDriveLab _et al._ , “WholeBodyVLA: Towards unified latent VLA for whole-body loco-manipulation control,” in _International Conference on Learning Representations (ICLR)_ , 2026. 

   - [31] A. Kumar, Z. Fu, D. Pathak, and J. Malik, “RMA: Rapid motor adaptation for legged robots,” in _Robotics: Science and Systems (RSS)_ , 2021. 

   - [32] M. Yoo, S. Shin, D. Sub, and D. Lee, “World model implanting for test-time adaptation of embodied agents,” in _International Conference on Machine Learning (ICML)_ , 2025. 

   - [33] A. Sukhija, L. Treven, J. Cheng, F. D¨orfler, S. Coros, and A. Krause, “TARC: Time-adaptive robotic control,” _arXiv preprint arXiv:2510.23176_ , 2025. 

   - [34] D. Jiang, Y. Li, G. Li, and B. Li, “MAGMA: A multi-graph based agentic memory architecture for AI agents,” _arXiv preprint arXiv:2601.03236_ , 2026. 

   - [35] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, L. Kaiser, and I. Polosukhin, “Attention is all you need,” _Advances in Neural Information Processing Systems (NeurIPS)_ , 2017. 

   - [36] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 

   - [37] E. Todorov, T. Erez, and Y. Tassa, “MuJoCo: A physics engine for model-based control,” in _IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2012. 

- [15] M. Ji, X. Peng, F. Liu, J. Li, G. Yang, X. Cheng, and X. Wang, “ExBody2: Advanced expressive humanoid whole-body control,” _arXiv preprint arXiv:2412.13196_ , 2024. 

- [16] C. Zhang, W. Xiao, T. He, and G. Shi, “WoCoCo: Learning whole-body humanoid control with sequential contacts,” in _Conference on Robot Learning (CoRL)_ , 2024. 

- [17] Y. Wang, H. Jiang, S. Yao, Z. Ding, and Z. Lu, “SENTINEL: A fully end-to-end language-action model for humanoid whole body control,” _arXiv preprint arXiv:2511.19236_ , 2025. 

