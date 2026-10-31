---
title: "FastDSAC: Unlocking the Potential of Maximum Entropy RL in High-Dimensional Humanoid Control"
date: "2026-03-13"
authors: "Jun Xue; Junze Wang; Shanze Wang; Xinming Zhang; Yanjun Chen; Wei Zhang"
url: https://arxiv.org/abs/2603.12612
pdf: https://arxiv.org/pdf/2603.12612
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.12612)** / [論文ページ](https://arxiv.org/abs/2603.12612)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

## **FastDSAC: Unlocking the Potential of Maximum Entropy RL in High-Dimensional Humanoid Control** 

**Jun Xue**<sup>**1, 2**</sup> **Junze Wang**<sup>**1, 3**</sup> **Shanze Wang**<sup>**1**</sup> **Xinming Zhang**<sup>**1**</sup> **Yanjun Chen**<sup>**1**</sup> **Wei Zhang**<sup>**1**</sup><sup>_∗_</sup> 

1College of Information Science and Technology, Eastern Institute of Technology, Ningbo, China 2School of Computer Science, Shanghai Jiao Tong University, Shanghai, China 3College of Computer Science and Technology, China University of Petroleum(East China), Qingdao, China `zhw@eitech.edu.cn` 

### **Abstract** 

Scaling Maximum Entropy Reinforcement Learning (RL) to high-dimensional humanoid control remains a fundamental challenge, as the “curse of dimensionality” induces severe exploration inefficiency and training instability. Consequently, highly optimized deterministic policy gradients currently dominate high-throughput regimes. We address this limitation with FastDSAC, a framework that effectively unlocks the potential of maximum entropy stochastic policies for complex continuous control. We introduce Dimension-wise Entropy Modulation (DEM) to dynamically redistribute the exploration budget, alongside a continuous distributional critic tailored to ensure accurate value estimation by mitigating both high-dimensional overestimation and discrete quantization artifacts. Extensive evaluations on HumanoidBench and a diverse set of continuous control tasks demonstrate that FastDSAC establishes state-of-the-art performance for high-dimensional stochastic policies on the evaluated benchmarks. Our method is competitive with and often outperforms strong deterministic baselines, with gains of 180% and 350% on the challenging _Basketball_ and _Balance Hard_ tasks, respectively. 


Figure 1: **Performance of FastDSAC on very high-dimensional humanoid control tasks.** (a) Visualizations of the challenging _Basketball_ and _Balance Hard_ environments. (b, c) Evaluation curves comparing FastDSAC with the FastTD3 baseline. Curves show the mean over 5 seeds, with shaded regions spanning the min-max range across seeds. FastDSAC outperforms FastTD3, achieving final returns 1.8 _×_ and 3.5 _×_ higher on the respective tasks with stronger sample efficiency. 

### **1 Introduction** 

Deep reinforcement learning (RL) has driven significant progress in high-dimensional robotics and has become a practical framework for learning sensorimotor skills in humanoid control [1–5]. As 

> _∗_ Corresponding author. 

Preprint. 

morphological complexity and task demands increase, the field has shifted towards leveraging massively parallel simulation to accelerate training [6–10]. In this high-throughput setting, deterministic policy-gradient methods, especially FastTD3 [5], have largely defined the state of the art. By leveraging the stability of deterministic policies in massively parallelized environments (e.g., IsaacLab [11], MuJoCo Playground [12], and HumanoidBench [3]), these approaches successfully solve challenging locomotion and manipulation tasks that were once intractable. While recent works, such as FlashSAC [13], have attempted to scale stochastic policy algorithms via system-level throughput optimizations, deterministic methods remain the dominant and most reliable baselines for very high-dimensional humanoid whole-body control. 

Despite the dominance of deterministic methods, maximum entropy RL algorithms (e.g., SAC [14]), theoretically offer compelling advantages, particularly in escaping local optima and fostering diverse behaviors, which are often absent in deterministic approaches. However, realizing these benefits in high-dimensional humanoid control is limited by the “curse of dimensionality” [15]. A primary obstacle in complex robotic systems is that unconstrained exploration fails to distinguish between precision-critical and redundant actuators [16]. Furthermore, because standard diagonal Gaussian policies lack structural prioritization, they distribute independent exploration noise uniformly across the expanded action volume ( _|A| >_ 20). As dimensionality increases, these independent perturbations severely restrict the robot’s effective movement, termed “vanishing exploration” [17, 18]. Consequently, without a mechanism to selectively allocate exploration variance, stochastic agents frequently suffer from training instability and suboptimal convergence, a limitation shared by several recent strong baselines [3, 5, 19, 18, 13]. 

Compounding the exploration difficulty is the inherent susceptibility of critic networks to severe value overestimation in high-dimensional action spaces. As the action space expands, critics are frequently queried on state-action pairs lying far from the training distribution (OOD). In these sparse regions, neural approximations suffer from severe extrapolation error, generating spurious Q-value spikes [20, 21]. This issue is exacerbated in high-dimensional settings where the policy tends to over-exploit these approximation artifacts, aggressively shifting towards regions where the critic erroneously predicts high returns [22]. Crucially, standard mitigation strategies, such as clipped double Q-learning, are often insufficient to suppress this overestimation bias in complex dynamics [23, 24]. Even recent parallelized approaches, utilizing either standard architectures or discrete distributional critics [25, 19], struggle to resolve this instability, leading to suboptimal convergence. Beyond overestimation, discrete critics rely on fixed supports and discrete atoms: when reward scales vary widely across tasks, the support range itself becomes an additional tuning burden, while quantization errors induced by finite atoms can further exacerbate value overestimation. Such discretization artifacts further compound extrapolation errors, compromising the accurate value estimation required for high-precision control. This motivates a continuous distributional critic, which can better preserve value fidelity while mitigating both high-dimensional overestimation and quantization artifacts in high-throughput settings [26]. 

To bridge these gaps, we introduce FastDSAC, a framework that effectively scales maximum entropy stochastic policies to high-dimensional continuous control. FastDSAC integrates two core mechanisms to unlock the scalability and stability of learning in high-dimensional regimes. First, we propose Dimension-wise Entropy Modulation (DEM), which enables the agent to autonomously redistribute the exploration budget across action dimensions. By effectively pruning the exploration subspace to suppress task-irrelevant noise, DEM avoids the structural inefficiency of uniform exploration typical of standard policies. Second, we incorporate a continuous distributional critic parameterized by a Gaussian distribution [26]. Distinct from baselines limited to discrete approximations or deterministic estimates, this component ensures highly accurate value estimation by modeling the full return distribution continuously, avoiding fixed-support discretization while helping mitigate the value overestimation caused by high-dimensional extrapolation errors. Extensive empirical evaluations on HumanoidBench, MuJoCo Playground, and IsaacLab confirm that FastDSAC consistently matches or outperforms strong baselines across the vast majority of evaluated tasks. It yields performance gains of approximately **180%** and **350%** over FastTD3 on the challenging _Basketball_ and _Balance Hard_ tasks, respectively, demonstrating that rigorously designed stochastic policies can achieve outstanding performance in very high-dimensional humanoid robotics. Furthermore, we validate the practical viability of our framework by successfully deploying the learned policies zero-shot to a physical Unitree G1 humanoid. An anonymous implementation of our method is provided at `https://anonymous.4open.science/r/FastDSAC_official-C43F` . 

2 

### **2 Preliminaries** 

We formulate the continuous control problem as a Markov Decision Process (MDP), defined by the tuple ( _S, A, p, r, γ_ ), comprising the state space _S_ , action space _A_ , transition dynamics _p_ ( _s_<sup>_′_</sup> _|s, a_ ), reward function _r_ ( _s, a_ ), and discount factor _γ ∈_ [0 _,_ 1). Our approach integrates two RL paradigms: 

**Maximum Entropy Reinforcement Learning.** To encourage exploration, we adopt the maximum entropy framework [14]. Instead of solely maximizing scalar returns, the agent learns a policy _π_ ( _·|s_ ) optimizing the expected return augmented by an entropy term: 


where _H_ is the policy entropy and _α_ is a temperature parameter balancing reward and exploration. 

**Distributional Reinforcement Learning.** Unlike standard methods estimating the expected value _Q_<sup>_π_</sup> ( _s, a_ ) = E[ _Z_<sup>_π_</sup> ( _s, a_ )], we model the full distribution of the random return _Z_<sup>_π_</sup> ( _s, a_ ), which follows the distributional Bellman equation: 


where _s_<sup>_′_</sup> _∼ p_ ( _·|s, a_ ), _a_<sup>_′_</sup> _∼ π_ ( _·|s_<sup>_′_</sup> ), and = _D_ denotes distributional equality. Capturing return distribution enables the agent to utilize higher-order moments (e.g., variance) for more stable learning signals. 

#### **2.1 Fast Actor-Critic (FastTD3)** 

Our work builds on the high-throughput recipe of FastTD3 [5], a TD3 variant designed for massive parallelism. Two ingredients are especially relevant for FastDSAC. (1) FastTD3 leverages massively parallel simulation together with large-batch replay updates, which accelerate training and increase data diversity within each critic update. (2) It equips TD3 with the categorical C51 critic [27], which represents returns on a fixed discrete support of _N_ atoms _{zi}_<sup>_N_</sup> _i_ =1<sup>spanning[</sup><sup>_v_min</sup><sup>_, v_max].Target</sup> estimation uses the projected Bellman update **_m_** = Φ _T Zθ′_ , where the distributional Bellman operator _T_ first shifts the return distribution and Φ then projects it back onto the fixed atoms; the full C51 parameterization and optimization objective are summarized in Appendix C. 

However, this fixed discretization is limiting in our setting: the support range [ _v_ min _, v_ max] can become task-dependent when reward scales vary, and finite atoms introduce quantization error that restricts value estimation precision in continuous control tasks requiring fine-grained signal propagation. 

#### **2.2 Continuous Distributional Critics (DSAC)** 

To mitigate the limitations of discrete distributional approximations and ensure accurate value estimation, we employ the Distributional Soft Actor-Critic (DSAC) framework [24, 26]. DSAC parameterizes the return distribution as a continuous Gaussian _Zθ_ ( _·|s, a_ ) _∼N_ ( _Qθ_ ( _s, a_ ) _, σθ_<sup>2(</sup><sup>_s, a_)),</sup> thereby avoiding both quantization artifacts and manual support specification. Furthermore, to address the numerical instability of standard KL-divergence gradients, DSAC derives separate gradient estimators for the mean and standard deviation. This separation inversely scales the mean update by variance to reduce step sizes in high-uncertainty regions, thereby curbing overestimation, while stabilizing the variance update via target clipping _C_ ( _·_ ; _b_ ) to prevent optimization collapse [26]: 


Here, _yq_<sup>min</sup> denotes the conservative target Q-value derived from the twin critics, while _yz_<sup>min</sup> represents a stochastic sample from the target return distribution. The parameter _ϵ_ prevents gradient explosion when the variance _σθ_<sup>2approaches zero, whereas</sup><sup>_ϵω_prevents gradient disappearance as the scaling</sup> factor _ω_ approaches zero. The scaling factor _ω_ = E( _s,a_ ) _∼B_ [ _σθ_ ( _s, a_ )<sup>2</sup> ] and the clipping boundary _b_ within _C_ ( _·_ ; _b_ ) are adaptively updated based on the running statistics of the learned variance. As detailed in DSAC-T [26], this estimator combines three mechanisms: Expected Value Substituting, Twin Value Distribution Learning, and Variance-Based Critic Gradient Adjustment. Appendix C summarizes their original formulation, while Section 3.2 explains how FastDSAC streamlines them for the high-throughput regime. 

3 

### **3 Methodology** 

In this section, we present FastDSAC, a high-throughput reinforcement learning framework tailored for high-dimensional continuous control. FastDSAC adapts the actor-critic paradigm to massive parallelization via structural innovations in both policy parameterization and value estimation. The overall architecture diagram of the algorithm and the pseudocode are shown in Appendix D. 

Our method consists of three integrated components: (1) An actor employing Dimension-wise Entropy Modulation to autonomously manage exploration budgets in high-dimensional action spaces (Section 3.1); (2) A streamlined Continuous Distributional Critic that improves value fidelity by avoiding fixed-support discretization and reducing quantization artifacts (Section 3.2); and (3) A unified Distributional Soft Policy Iteration (DSPI) loop optimized for large-batch stability (Section 3.3). 

#### **3.1 The FastDSAC Actor: Dimension-wise Entropy Modulation** 

Standard Gaussian policies in SAC typically parameterize the action distribution as _πϕ_ ( _a|s_ ) = _N_ ( _µϕ_ ( _s_ ) _,_ diag( _σϕ_<sup>2(</sup><sup>_s_))), estimating the standard deviation</sup><sup>_σϕ,i_independently for each dimension.</sup> In high-dimensional systems, this independent parameterization leads to inefficient exploration, as the agent fails to distinguish between critical and redundant actuators, assigning variance uniformly across all dimensions [16, 3]. To address this, we propose Dimension-wise Entropy Modulation (DEM), a mechanism that imposes a structural constraint on the exploration covariance to explicitly manage the variance budget. Rather than replacing the standard variance prediction, DEM augments it by learning a dimension-specific scaling weight _wi_ for each action dimension _i ∈{_ 1 _, . . . , |A|}_ . 

**Budget-Preserving Variance Redistribution.** Given the actor backbone features _h_ ( _s_ ), we compute the modulation weights using a temperature-scaled Softmax operation: 


where _τ_ is a temperature hyperparameter that regulates the sparsity of the weight distribution, and _N_ = _|A|_ denotes the action dimension. Multiplying the standard Softmax output by _N_ ensures that the mean of the weights is exactly 1 (i.e., _N_<sup><u>1</u></sup> � _Ni_ =1<sup>_wi_= 1).This normalization enforces a zero-sum</sup> redistribution of the exploration budget: increasing the variance on specific redundant dimensions necessarily decreases the variance on precision-critical dimensions. The final standard deviation for the _i_ -th action dimension is modulated as: 


where _σ_ ˆ _ϕ,i_ ( _s_ ) represents the base log-standard deviation predicted by the network. The subsequent action sampling and policy evaluation follow the standard SAC reparameterization trick. 

**Interpretation: Autonomous Subspace Pruning.** This formulation enforces a soft exploration budget. By dynamically adjusting _wi_ , the agent gains the autonomy to selectively suppress noise on specific dimensions while concentrating exploration variance on task-irrelevant dimensions, effectively rendering critical actions near-deterministic to ensure the precise control for optimal convergence. Crucially, this importance assignment is emergent and driven solely by reward maximization. This bypasses the need for manual priors or kinematic specifications, enabling the discovery of effective coordination patterns that may be non-intuitive to human design. As empirically analyzed in Section 4.3, this mechanism effectively prunes the exploration subspace, maintaining high-precision control on stable joints while exploring others. The temperature _τ_ regulates the _sparsity_ of this weight distribution: a lower _τ_ encourages a sharp, focused allocation, while a higher _τ_ yields a uniform distribution, approximating standard SAC behavior. 

**Diversity-driven Population.** To mitigate mode collapse across the parallel population, we employ a Heterogeneous Exploration scheme adapted from FastTD3 [5]. We assign a distinct scaling factor _βe ∼ U_ [ _β_ min _, β_ max] to each environment _e_ . Unlike prior works that scale noise magnitude [8, 5], we apply _βe_ to the modulation logits to vary the distribution shape: 


This effectively diversifies the anisotropy of exploration across the population: some agents explore broadly by distributing the budget across many dimensions, while others focus intensely on specific subspaces, thereby enhancing robustness against local optima. 

4 

#### **3.2 The FastDSAC Critic: Streamlined Distributional Learning** 

To address the limitations of discrete critics [27, 5], we adopt the Continuous Gaussian Critic from DSAC-T [26], parameterizing the return distribution as _Zθ_ ( _·|s, a_ ) _∼N_ ( _Qθ_ ( _s, a_ ) _, σθ_<sup>2(</sup><sup>_s, a_)), to</sup> avoid fixed-support specification and ensure accurate value estimation by modeling the full return distribution without discretization artifacts. 

While original DSAC-T employs complex variance-based gradient adjustments for low-data regimes, we find these constraints restrict accurate variance modeling in our settings. Leveraging the natural stability provided by large batch sizes, we streamline the objective by removing variance clipping boundaries, while retaining twin-critic target, Expected Value Substitution, and Gradient Scaling. 

The parameters _θ_ are updated by minimizing divergence between predicted and target distributions. Following DSAC-T [26], we decompose the gradient into mean- and variance-driven components: 


Here, term (I) leverages the Expected Value Substitution: we anchor the mean update to the conservative target mean _yq_<sup>min</sup> = _r_ + _γ_ (min _j_ =1 _,_ 2 _Qθ′j_ ( _s_<sup>_′_</sup> _, a_<sup>_′_</sup> ) _− α_ log _π_ ( _a_<sup>_′_</sup> _|s_<sup>_′_</sup> )), rather than stochastic samples. In our high-dimensional setting, this deterministic target proved more stable than directly using stochastic return samples for the mean update. Term (II) updates the variance to capture the stochasticity induced by environmental dynamics and policy exploration. Unlike the original implementation which clips the target sample _yz_<sup>sample</sup> within a dynamic boundary, we remove this constraint to allow the critic to learn the true scale of environmental stochasticity without bias. The scalar _ω ≈_ E _B_ [ _σθ_<sup>2] is the gradient scaling factor handling reward scale sensitivity [26].</sup> 

#### **3.3 Distributional Soft Policy Iteration (DSPI)** 

We integrate the proposed Actor 3.1 and Critic 3.2 into a unified Distributional Soft Policy Iteration (DSPI) loop. This process alternates between evaluating the policy’s return distribution and improving the policy via entropy-regularized maximization. Theoretically, the DSPI framework is guaranteed to converge to the optimal policy, as established in DSAC [24]. 

**Distributional Soft Policy Evaluation.** In the evaluation step, we update the twin critic networks using the streamlined gradient estimator in Eq. 7. By maintaining a continuous Gaussian parameterization, the critic avoids discrete quantization artifacts and models the full return distribution, capturing aleatoric uncertainty alongside the expected return. As the gradient magnitude is inversely scaled by the estimated variance, high uncertainty on OOD actions naturally dampens updates, reducing high-dimensional overestimation and improving value estimation. 

**Distributional Soft Policy Improvement.** In the improvement step, the actor _πϕ_ is updated to maximize both the expected return and entropy. Following the reparameterization trick [14], the actor utilizes the mean estimate of the distributional critic, _Qθ_ ( _s, a_ ) = E _Z∼Zθ_ [ _Z_ ], to guide policy updates. The actor is optimized by minimizing: 


Since our actor employs the Dimension-wise Entropy Modulation (DEM) mechanism, the term log _πϕ_ ( _a|s_ ) implicitly accounts for the redistributed exploration budget. This optimization naturally balances reward maximization against the structural entropy constraints imposed by DEM, effectively guiding the agent to autonomously prune task-irrelevant subspaces. Simultaneously, we dynamically adjust the temperature parameter _α_ via gradient descent to satisfy the target entropy constraint _H_ [14]: 


**Implementation Recipe Summary.** Full implementation details are provided in Appendix A.4. Crucially, we set the target entropy to _H_ = 0 across all tasks. Unlike the standard heuristic ( _H_ = _−|A|_ ) which forces premature variance decay, _H_ = 0 sustains a generous exploration budget, which DEM structurally manages by safely offloading excess entropy to redundant joints. Additionally, we apply LayerNorm only in the very high-dimensional HumanoidBench domain, where it serves as an important stabilizer for training, whereas smaller action spaces (MuJoCo Playground & 

5 

IsaacLab) achieve SOTA performance without such regularization. Furthermore, unlike the original DSAC-T [26], which requires a large numerical stabilizer (bias = 0 _._ 1) to prevent division-by-zero, our large-batch regime allows drastically reducing the continuous critic’s numerical stabilizer (bias = 10<sup>_−_6</sup> ), unlocking high-fidelity value estimation for low-variance states. Finally, while a fixed DEM temperature ( _τ_ = 1) is our robust default, we introduce an end-to-end learnable variant, FastDSAC (auto- _τ_ ), to adapt variance redistribution for highly dynamic tasks. Ablation experiments on target entropy and layernorm are in Appendix K and L. 

### **4 Experiments** 

Our empirical evaluation aims to validate the scalability, algorithmic mechanisms, and real-world viability of FastDSAC in high-dimensional continuous control. Specifically, we design our experiments to address four key questions: **Q1 (Comparative Performance):** Can FastDSAC match or outperform strong deterministic, standard stochastic, and model-based baselines across complex domains? **Q2 (Actor Mechanism):** Is Dimension-wise Entropy Modulation (DEM) essential for managing high-dimensional exploration, and does it autonomously discover interpretable variancepruning strategies? **Q3 (Critic Parameterization):** Does continuous Gaussian modeling yield more accurate value estimation in high-dimensional spaces compared to discrete (C51) approximations? **Q4 (Sim-to-Real Deployment):** Can the stable, high-precision control policies discovered by FastDSAC in simulation transfer zero-shot to physical humanoid hardware? 

To address these questions, we evaluate our framework across HumanoidBench, MuJoCo Playground, and IsaacLab, spanning diverse tasks from locomotion to complex whole-body manipulation, and ultimately deploy it on the Unitree G1. 

#### **4.1 Experimental Setup** 

**Benchmarks.** We aligned with the FastTD3 suite [5], evaluating on: (1) HumanoidBench [3]: 25 representative tasks spanning locomotion and whole-body manipulation, with very high-dimensional action spaces ( _|A|_ = 61). (2) MuJoCo Playground [12] & IsaacLab [11]: 10 tasks across diverse physics engines to verify robustness. While their action spaces are smaller than those of HumanoidBench ( _|A| <_ 30), they still represent challenging high-dimensional control settings in RL. We therefore omitted Layer Normalization, as FastDSAC retains inherent stability without it. 

**Baselines & Protocol.** We benchmarked against FastTD3 (deterministic SOTA) and FastSAC (parallelized stochastic baseline) [5]. To ensure rigorous comparison in all tasks, we matched FastSAC to FastDSAC in its Layer Normalization setting and target entropy _H_ = 0, hereafter denoted as _FastSAC (standard)_ . For HumanoidBench, we incorporated official benchmark results for DreamerV3, TD-MPC2, SAC, and PPO; for MuJoCo Playground and IsaacLab, we additionally evaluated against PPO to contextualize performance against on-policy methods in these domains. 

To guarantee fair evaluation, we strictly inherited the FastTD3 high-throughput training protocol (e.g., replay capacity, update schedules, parallel environment counts) for all corresponding tasks. We report mean returns aggregated over 3 seeds, with shaded regions indicating the min-max range. Notably, we use 5 seeds for _Basketball_ and _Balance Hard_ to demonstrate consistency, while maintaining 3 seeds for all other tasks to match FastTD3 and HumanoidBench protocols. Crucially, for FastDSAC-specific hyperparameters, we rigorously enforce **unified algorithmic configuration** within each evaluation domain (i.e., parameters remain strictly identical across all tasks within a given benchmark), in contrast to FastTD3, whose distributional critic may require task-specific tuning of the C51 support range. Full protocol details and hyperparameter configurations are summarized in Appendix A. 

#### **4.2 Main Results (Q1)** 

We evaluated FastDSAC across 35 tasks spanning diverse dynamics. Figure 2 shows learning curves for 20 representative tasks from HumanoidBench, MuJoCo Playground, and IsaacLab (see Appendix N for full results). We observe three distinct performance regimes: 

**Strong Performance on Complex Coordination & Manipulation.** FastDSAC achieves state-of-theart performance on tasks demanding precise actuation and whole-body coordination, outperforming FastTD3 and FastSAC (Standard) on challenging tasks such as _Basketball_ , _Balance Hard_ , _Insert_ 

6 


Figure 2: **Comparative evaluation on high-dimensional continuous control benchmarks.** Learning curves across selected tasks from **HumanoidBench** (top three rows), **IsaacLab** (fourth row), and **MuJoCo Playground** (bottom row). **FastDSAC** matches or often outperforms **FastTD3** and **FastSAC (Standard)** . It performs strongly on precision-demanding (e.g., _Basketball_ , _Insert_ ) and stability-critical (e.g., _Balance Hard_ ) tasks, while retaining robust dexterous manipulation and roughterrain locomotion performance. 

_Normal_ , _Sit Hard_ , and _Window_ . This gap highlights the limitation of deterministic policies in exploring intricate control manifolds, whereas FastDSAC’s entropy modulation effectively prunes the exploration subspace to discover superior solutions that deterministic baselines often fail to reach. 

**The Exploration-Exploitation Trade-off in Locomotion.** In dynamic locomotion (e.g., _Run_ , _slide_ ), FastDSAC rises more slowly than FastTD3 but converges to higher final returns. This pattern is consistent with the maximum entropy objective: DEM initially allocates variance to explore diverse gait patterns before stabilizing, whereas FastTD3 often converges prematurely to suboptimal gaits. Even on complex whole-body control tasks such as _Stair_ , FastDSAC remains competitive with FastTD3, showing that our framework preserves the precision needed for rigorous terrain adaptation. 

**Robustness Across Simulators.** FastDSAC scales consistently across physics engines. In MuJoCo Playground (e.g., _G1/T1 Joystick_ ), it maintains a clear lead. In IsaacLab ( _Velocity-Rough_ , _Repose-Cube-Allegro/Shadow_ ), FastDSAC outperforms FastTD3 after an initial adaptation phase, validating its robustness across dynamics. Although FastSAC (Standard) converges faster on the lower-dimensional _Repose-Cube-Shadow_ task ( _|A| ≈_ 24), FastDSAC reaches comparable performance, suggesting that while unmodulated exploration can suffice for specific hand-only tasks, our framework remains the stronger generalist across the broader benchmark suite. 

#### **4.3 Ablation Studies and Analysis (Q2 & Q3)** 

7 

To assess component necessity, we conducted ablation studies across 3 benchmarks on representative tasks spanning rough-terrain locomotion, dynamic whole-body coordination, object interaction, and manipulation. 

**Q2: Necessity and Mechanism of Dimensionwise Entropy Modulation (DEM).** To isolate the effect of DEM, we compare FastDSAC against an ablated variant (w/o DEM) that replaces the entropy-modulated actor with a standard diagonal Gaussian policy. As shown in Figure 3, across 12 diverse tasks from all 3 benchmarks, the full FastDSAC consistently yields higher asymptotic returns. Although the ablated agent often outperforms standard baselines, likely due to the continuous distributional critic, removing DEM degrades performance, reduces training stability, and increases inter-seed variance in tasks with challenging dynamics (e.g., _Balance Hard_ , _Basketball_ , and _Hurdle_ ). Beyond stabilizing the baseline performance, the structure of DEM also supports end-to-end optimization of its temperature parameter, which can further improve returns on tasks with different exploration demands. These results show 


Figure 3: **DEM improves performance and stability in high-dimensional control.** Learning curves across 12 tasks from three benchmarks comparing FastDSAC, its ablations (w/o DEM and auto- _τ_ ), and FastTD3/FastSAC. 

DEM is indispensable for managing high-dimensional exploration and reducing seed sensitivity. 

**Visualizing the Mechanism: Autonomous Subspace Pruning.** To understand how DEM optimizes exploration, we analyzed the evolution of learned weights _wi_ during a _Basketball_ episode (see the qualitative comparison in Figure 4 and the heatmap in Appendix I). The visualization reveals a task-aligned exploration strategy under the budget-preserving constraint ( _N_<sup><u>1</u></sup> � _wi_ = 1), which enforces a zerosum redistribution: to achieve near-deterministic precision on critical joints, the agent must offload variance onto redundant dimensions. **1) Variance Offloading:** We observed a prominent high-weight band (reaching _wi ≈_ 8 _._ 0) corresponding to task-irrelevant joints, such as the left thumb ( `lh_A_THJ4` ) and wrist, which act as entropy sinks. **2) Precision for Impact and Balance:** During the critical interaction phase (Steps 10-13), as the robot impacts the ball, weights for the legs, torso, and right arm are suppressed to near-zero. This suppression persists post-impact to counteract momentum, demonstrating DEM’s ability to autonomously prune the active subspace to guarantee whole-body stability. 

#### **Interpretation: Emergent Strategy via Variance Offload-** 

**ing.** The agent autonomously discovers an unconventional “body-rebound” strategy, using the torso rather than the hands to redirect the ball. While counter-intuitive to human design, this behavior maximizes return by prioritizing post-throw stability over risky dexterity. The heatmap shows that the agent treats the task-irrelevant left thumb as an _entropy sink_ for the required exploration budget. By offloading variance to these Figure 4: **Qualitative compari-** distal joints, FastDSAC effectively prunes the exploration sub- **son on** **_Basketball_ .** FastDSAC space, preserving high-precision control for the core body and throws well and stays stable, while legs to attain consistent returns of _≈_ 1030. Crucially, despite FastTD3 loses balance and fails. kinematic variations across seeds, the variance redistribution pattern remains stable: FastDSAC repeatedly uses task-irrelevant subspaces as entropy sinks to stabilize whole-body control. 

Figure 4: **Qualitative comparison on** **_Basketball_ .** FastDSAC throws well and stays stable, while FastTD3 loses balance and fails. 

**Contrast with Deterministic Baseline.** FastTD3 attempts an intuitive but unstable hand-catch strategy (Figure 4). However, it fails to balance manipulation with whole-body stability; the agent hits the ball but then falls, resulting in suboptimal returns ( _≈_ 500). In contrast, FastDSAC’s entropy modulation exploits the reward structure more effectively and finds a more stable solution. More broadly, this result shows that in high-dimensional RL, the return-maximizing strategy need not align with human-intended behavior, and may instead favor whole-body survival over risky dexterity. 

8 

#### **Q3: Continuous vs. Discrete Distributional Critics.** 

To isolate the effect of critic parameterization, we compared FastDSAC against a discrete baseline, FastSAC (C51+DEM), the C51 variant of FastSAC [28] augmented with our DEM module, using the same training pipeline and actor design. Figure 5 shows that FastDSAC outperforms both FastSAC (standard) and its discrete variant, FastSAC (C51+DEM), on all nine evaluated tasks, including approximately 2 _×_ higher returns on _Balance Hard_ . Since the actor design and the overall training framework are otherwise matched, these results suggest that the continuous Gaussian critic provides a more accurate and stable value estimate than the discrete C51 critic in our highthroughput control regime. A likely reason is that the continuous critic avoids fixed-support discretization and atom quantization, which may introduce representation errors that degrade value accuracy in high-dimensional control. Consistent with this view, 


Figure 5: **Continuous critics outperform discrete C51 critics on 9 high-dimensional tasks.** Curves show the mean episode return of FastDSAC compared to FastSAC (C51+DEM) and FastSAC (standard). 

Appendix J shows on _Basketball_ that the performance of C51+DEM is highly sensitive to the choice of support range. Moreover, prior DSAC analyses [26] show that distributional critics can reduce value overestimation, which becomes particularly important in high-dimensional action spaces. 

#### **4.4 Sim-to-Real Validation on Unitree G1 (Q4)** 

To verify that FastDSAC transfers effectively to physical hardware, we deploy FastDSAC zero-shot on a Unitree G1 humanoid, following the mature sim-to-real pipeline in [28]. Evaluated on joystick-conditioned locomotion and a complex “squat-carrywalk-squat” motion-tracking task, FastDSAC requires minimal adaptation: core hyperparameters remain unified, adjusting only task-specific settings (e.g., multi-step returns, _γ_ ). Running directly on the G1’s onboard compute, the policies show zero-shot stability and robustness to moderate physical pushes (Figure 6). This shows that FastDSAC’s stable exploration in simulation can yield deployable real-world controllers. See Appendix B for motion-tracking and additional locomotion results. 


Figure 6: **Sim-to-real on Unitree G1.** Zero-shot joystickconditioned forward walking on the G1 robot, showing effectiveness of FastDSAC in real-world deployments. 

### **5 Conclusion** 

In this work, we challenge the dominance of deterministic policy gradients in high-dimensional humanoid control by introducing FastDSAC, a framework that unlocks the scalability of maximum entropy RL. FastDSAC addresses the curse of dimensionality by integrating Dimension-wise Entropy Modulation (DEM) for autonomous subspace pruning, together with a continuous distributional critic for accurate value estimation by mitigating both high-dimensional overestimation and discretization artifacts. Across 35 diverse tasks, our method establishes state-of-the-art performance for highdimensional stochastic policies on the evaluated benchmarks, remaining competitive with and often outperforming strong baselines, with gains of 180% and 350% on challenging coordination tasks. Furthermore, FastDSAC policies successfully transfer zero-shot to a physical humanoid robot. Our findings show that a rigorously designed stochastic policy is not only viable for the high-throughput regime, but can also achieve strong performance in high-precision humanoid control, bridging the gap between broad exploration and precise control. Detailed discussion of limitations, extended future directions, and broader societal impacts are provided in Appendix O. 

9 

### **References** 

- [1] Nicklas Hansen, Hao Su, and Xiaolong Wang. Td-mpc2: Scalable, robust world models for continuous control. In _International Conference on Learning Representations_ , 2024. 

- [2] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains through world models. _arXiv preprint arXiv:2301.04104_ , 2023. 

- [3] Carmelo Sferrazza, Dun-Ming Huang, Xingyu Lin, Youngwoon Lee, and Pieter Abbeel. Humanoidbench: Simulated humanoid benchmark for whole-body locomotion and manipulation. In _Robotics: Science and Systems_ , 2024. 

- [4] Zifeng Zhuang, Diyuan Shi, Runze Suo, Xiao He, Hongyin Zhang, Ting Wang, Shangke Lyu, and Donglin Wang. Tdmpbc: Self-imitative reinforcement learning for humanoid robot control. _arXiv preprint arXiv:2502.17322_ , 2025. 

- [5] Younggyo Seo, Carmelo Sferrazza, Haoran Geng, Michal Nauman, Zhao-Heng Yin, and Pieter Abbeel. Fasttd3: Simple, fast, and capable reinforcement learning for humanoid control. _arXiv preprint arXiv:2505.22642_ , 2025. 

- [6] Nikita Rudin, David Hoeller, Philipp Reist, and Marco Hutter. Learning to walk in minutes using massively parallel deep reinforcement learning. In _Proceedings of the 5th Conference on Robot Learning_ , volume 164 of _Proceedings of Machine Learning Research_ , pages 91–100. PMLR, 2022. URL `https://proceedings.mlr.press/v164/rudin22a.html` . 

- [7] Elia Kaufmann, Leonard Bauersfeld, Antonio Loquercio, Matthias Müller, Vladlen Koltun, and Davide Scaramuzza. Champion-level drone racing using deep reinforcement learning. _Nature_ , 620(7976):982–987, 2023. 

- [8] Zechu Li, Tao Chen, Zhang-Wei Hong, Anurag Ajay, and Pulkit Agrawal. Parallel _q_ -learning: Scaling off-policy reinforcement learning under massively parallel simulation. In _International Conference on Machine Learning_ , pages 19440–19459. PMLR, 2023. 

- [9] Arth Shukla. Speeding up sac with massively parallel simulation. _https://arthshukla.substack.com_ , Mar 2025. URL `https://arthshukla.substack. com/p/speeding-up-sac-with-massively-parallel` . 

- [10] Matteo Gallici, Mattie Fellows, Benjamin Ellis, Bartomeu Pou, Ivan Masmitja, Jakob Nicolaus Foerster, and Mario Martin. Simplifying deep temporal difference learning. In _The Thirteenth International Conference on Learning Representations_ , 2025. URL `https://openreview. net/forum?id=7IzeL0kflu` . 

- [11] Mayank Mittal, Pascal Roth, James Tigue, Antoine Richard, Octi Zhang, Peter Du, Antonio Serrano-Muñoz, Xinjie Yao, René Zurbrügg, Nikita Rudin, Lukasz Wawrzyniak, Milad Rakhsha, Alain Denzler, Eric Heiden, Ales Borovicka, Ossama Ahmed, Iretiayo Akinola, Abrar Anwar, Mark T. Carlson, Ji Yuan Feng, Animesh Garg, Renato Gasoto, Lionel Gulich, Yijie Guo, M. Gussert, Alex Hansen, Mihir Kulkarni, Chenran Li, Wei Liu, Viktor Makoviychuk, Grzegorz Malczyk, Hammad Mazhar, Masoud Moghani, Adithyavairavan Murali, Michael Noseworthy, Alexander Poddubny, Nathan Ratliff, Welf Rehberg, Clemens Schwarke, Ritvik Singh, James Latham Smith, Bingjie Tang, Ruchik Thaker, Matthew Trepte, Karl Van Wyk, Fangzhou Yu, Alex Millane, Vikram Ramasamy, Remo Steiner, Sangeeta Subramanian, Clemens Volk, CY Chen, Neel Jawale, Ashwin Varghese Kuruttukulam, Michael A. Lin, Ajay Mandlekar, Karsten Patzwaldt, John Welsh, Huihua Zhao, Fatima Anes, Jean-Francois Lafleche, Nicolas Moënne-Loccoz, Soowan Park, Rob Stepinski, Dirk Van Gelder, Chris Amevor, Jan Carius, Jumyung Chang, Anka He Chen, Pablo de Heras Ciechomski, Gilles Daviet, Mohammad Mohajerani, Julia von Muralt, Viktor Reutskyy, Michael Sauter, Simon Schirm, Eric L. Shi, Pierre Terdiman, Kenny Vilella, Tobias Widmer, Gordon Yeoman, Tiffany Chen, Sergey Grizan, Cathy Li, Lotus Li, Connor Smith, Rafael Wiltz, Kostas Alexis, Yan Chang, David Chu, Linxi "Jim" Fan, Farbod Farshidian, Ankur Handa, Spencer Huang, Marco Hutter, Yashraj Narang, Soha Pouya, Shiwei Sheng, Yuke Zhu, Miles Macklin, Adam Moravanszky, Philipp Reist, Yunrong Guo, David Hoeller, and Gavriel State. Isaac lab: A gpu-accelerated simulation framework for multi-modal robot learning. _arXiv preprint arXiv:2511.04831_ , 2025. URL `https://arxiv.org/abs/2511.04831` . 

10 

- [12] Kevin Zakka, Baruch Tabanpour, Qiayuan Liao, Mustafa Haiderbhai, Samuel Holt, Jing Yuan Luo, Arthur Allshire, Erik Frey, Koushil Sreenath, Lueder A Kahrs, et al. Mujoco playground. _arXiv preprint arXiv:2502.08844_ , 2025. 

- [13] Donghu Kim, Youngdo Lee, Minho Park, Kinam Kim, I Made Aswin Nahendra, Takuma Seno, Sehee Min, Daniel Palenicek, Florian Vogt, Danica Kragic, Jan Peters, Jaegul Choo, and Hojoon Lee. Flashsac: Fast and stable off-policy reinforcement learning for high-dimensional robot control. _arXiv preprint arXiv:2604.04539_ , 2026. 

- [14] Tuomas Haarnoja, Aurick Zhou, Pieter Abbeel, and Sergey Levine. Soft actor-critic: Offpolicy maximum entropy deep reinforcement learning with a stochastic actor. In _International conference on machine learning_ , pages 1861–1870. Pmlr, 2018. 

- [15] Mario Köppen. The curse of dimensionality. In _5th Online World Conference on Soft Computing in Industrial Applications (WSC5)_ , volume 1, pages 4–8, 2000. 

- [16] Wenbo Zhang and Hengrui Cai. On high-dimensional action selection for deep reinforcement learning, 2024. URL `https://openreview.net/forum?id=rto6aU453A` . 

- [17] Pierre Schumacher, Thomas Geijtenbeek, Vittorio Caggiano, Vikash Kumar, Syn Schmitt, Georg Martius, and Daniel F. B. Haeufle. Natural and robust walking using reinforcement learning without demonstrations in high-dimensional musculoskeletal models, 2023. URL `https://arxiv.org/abs/2309.02976` . 

- [18] Yunyue Wei, Chenhui Zuo, and Yanan Sui. Scalable exploration for high-dimensional continuous control via value-guided flow, 2026. URL `https://arxiv.org/abs/2601.19707` . 

- [19] Zilin Kang, Chonghua Liao, Tingqiang Xu, and Huazhe Xu. Entropy regularizing activation: Boosting continuous control, large language models, and image classification with activation as entropy constraints. In _International Conference on Learning Representations_ , 2026. URL `https://openreview.net/forum?id=Cqdsw3yteP` . 

- [20] Aditya Bhatt, Max Argus, Artemij Amiranashvili, and T. Brox. Crossq: Batch normalization in deep reinforcement learning for greater sample efficiency and simplicity. _ArXiv_ , abs/1902.05605, 2019. 

- [21] Gerhard Neumann, Fabian Otto, Philipp Becker, and Ngo Anh Vien. Vlearn: Off-policy learning with efficient state-value function estimation, 2024. URL `https://arxiv.org/abs/2403. 04453` . 

- [22] Younggyo Seo and Pieter Abbeel. Coarse-to-fine q-network with action sequence for dataefficient reinforcement learning, 2025. URL `https://arxiv.org/abs/2411.12155` . 

- [23] Arsenii Kuznetsov, Pavel Shvechikov, Alexander Grishin, and Dmitry Vetrov. Controlling overestimation bias with truncated mixture of continuous distributional quantile critics, 2020. URL `https://arxiv.org/abs/2005.04269` . 

- [24] Jingliang Duan, Yang Guan, S. Li, Yangang Ren, Qi Sun, and B. Cheng. Distributional soft actor-critic: Off-policy reinforcement learning for addressing value estimation errors. _IEEE Transactions on Neural Networks and Learning Systems_ , 33:6584–6598, 2020. 

- [25] Johan Obando-Ceron, Walter Mayor, Samuel Lavoie, Scott Fujimoto, Aaron Courville, and Pablo Samuel Castro. Simplicial embeddings improve sample efficiency in actor-critic agents, 2025. URL `https://arxiv.org/abs/2510.13704` . 

- [26] Jingliang Duan, Wenxuan Wang, Liming Xiao, Jiaxin Gao, Shengbo Eben Li, Chang Liu, Ya-Qin Zhang, Bo Cheng, and Keqiang Li. Distributional soft actor-critic with three refinements. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 47(5):3935–3946, 2025. doi: 10.1109/TPAMI.2025.3537087. 

- [27] Marc G. Bellemare, Will Dabney, and Rémi Munos. A distributional perspective on reinforcement learning, 2017. URL `https://arxiv.org/abs/1707.06887` . 

11 

- [28] Younggyo Seo, Carmelo Sferrazza, Juyue Chen, Guanya Shi, Rocky Duan, and Pieter Abbeel. Learning sim-to-real humanoid locomotion in 15 minutes, 2025. URL `https://arxiv.org/ abs/2512.01996` . 

- [29] Philip J Ball, Laura Smith, Ilya Kostrikov, and Sergey Levine. Efficient online reinforcement learning with offline data. In _International Conference on Machine Learning_ , 2023. 

- [30] Michal Nauman, Mateusz Ostaszewski, Krzysztof Jankowski, Piotr Miło´s, and Marek Cygan. Bigger, regularized, optimistic: scaling for compute and sample-efficient continuous control. In _Advances in Neural Information Processing Systems_ , 2024. 

12 

# **APPENDIX CONTENTS** 

|**A** Implementation Details and Hyperparameters|14|
|---|---|
|A.1 High-Throughput Training Protocol|14|
|A.2 Unified FastDSAC Hyperparameters|14|
|A.3 Baseline Configurations|14|
|A.4 Detailed Implementation Recipe|14|
|**B** Extended Details on Sim-to-Real Validation|16|
|**C** Supplementary Background on FastTD3 and DSAC-T|17|
|**D** Architecture and Pseudocode of FastDSAC|19|
|**E** Related Work|20|
|**F** Comparison with Contemporary Works|21|
|**G** Computational Resources|22|
|**H** Computational Efficiency and Wall-Clock Time|22|
|**I** Heatmaps of Basketball Task|24|
|**J** C51 Support Sensitivity on_Basketball_|25|
|**K** Ablation Study on Layer Normalization|25|
|**L** Ablation Study on Target Entropy|26|
|**M** Full Results|28|
|**N** Discussion of Limitations, Future Directions and Impact|29|


13 

### **A Implementation Details and Hyperparameters** 

#### **A.1 High-Throughput Training Protocol** 

To ensure a rigorous and fair comparison, FastDSAC strictly inherits the high-throughput training protocol from FastTD3 [5]. All domain-specific configurations, including parallel environment counts, replay buffer sizes, and update schedules (Update-to-Data (UTD) ratios), are matched to the official baseline settings. This protocol-level alignment ensures that any performance gains are attributable to the algorithmic innovations of FastDSAC rather than to discrepancies in computational budget or training schedules. 

Table 1: Domain-specific training protocols inherited from FastTD3 [5]. These parameters are defined by the underlying high-throughput framework rather than being tuned for FastDSAC. 

|**Parameter**|**HumanoidBench**|**Isaac-Velocity**|**Isaac-General**|**MuJoCo PG**|
|---|---|---|---|---|
|Parallel Environments (_Nenv_)|128|4,096|4,096|1,024|
|Multi-step Return (_Nsteps_)|1|8|1|1|
|Updates per Step (_Nupdates_)|2|4|2|2|
|Discount Factor (_γ_)|0.99|0.99|0.99|0.97|
|Replay Buffer Size|5_×_10<sup>4</sup>|5_×_10<sup>3</sup>|10<sup>4</sup>|10<sup>4</sup>|
|AMP / AMP Dtype|True / bf16|True / bf16|True / bf16|True / bf16|
|Batch Size|32,768|32,768|32,768|32,768|


#### **A.2 Unified FastDSAC Hyperparameters** 

In contrast to the per-task tuning often required by stochastic RL, FastDSAC utilizes a **unified algorithmic configuration** within each benchmark domain. As detailed in Table 2, core parameters such as DEM temperature, target entropy, and log-std bounds are kept strictly constant across all tasks within a given domain. 

The differences in _αinit_ and LayerNorm between HumanoidBench and lower-dimensional simulators (IsaacLab/MuJoCo PG) reflect basic adaptations to action dimensionality ( _|A|_ = 61 vs. _|A| <_ 30) and are consistent with standard literature on high-dimensional SAC [29, 30]. 

Table 2: Unified FastDSAC algorithmic hyperparameters. These values define our core method and are fixed across all tasks within their respective domains. 

|**Hyperparameter**|**HumanoidBench**|**IsaacLab / MuJoCo PG**|
|---|---|---|
|DEM Temperature (_τ_)|1.0 (Default)|1.0 (Default)|
|Log-Std Max / Min|1_._0_/ −_10|1_._0_/ −_10|
|Target Entropy (_H_)|0|0|
|Initial Alpha (_αinit_)|0.001|0.01|
|Layer Normalization|Enabled|Disabled|
|Polyak Update Rate (_τpolyak_)|0.005<br>|0.005<br>|
|Weight Decay|10<sup>_−_4</sup>|10<sup>_−_4</sup>|
|AdamW Betas|(0_._9_,_0_._95)|(0_._9_,_0_._95)|
|Critic Stabilizer (_ϵ_)|10<sup>_−_6</sup>|10<sup>_−_6</sup>|


#### **A.3 Baseline Configurations.** 

Results for the FastTD3 baseline are taken directly from the original paper [5]. For the stochastic baseline, we use the FastSAC branch provided in the FastTD3 codebase and rerun it on the benchmark tasks considered in this paper. At the protocol level, FastSAC follows the same benchmark and task-specific setup as FastDSAC, including the FastTD3 replay/update schedule, number of training steps, replay buffer size, batch size, evaluation frequency, number of parallel environments, and task-specific discount factors. At the algorithm level, we largely retain the working configuration of this FastSAC implementation from the codebase, including the target-network soft update rate, weight decay, and log-standard-deviation bounds of [ _−_ 5 _,_ 2], while aligning a small number of generic 

14 

optimizer settings with FastDSAC by using AdamW with _β_ = (0 _._ 9 _,_ 0 _._ 95) and target entropy _H_ = 0. LayerNorm is enabled on HumanoidBench and disabled on MuJoCo Playground and IsaacLab, matching the benchmark-specific usage in FastDSAC. 

For the critic-ablation baseline _FastSAC (C51_ + _DEM)_ , we retain the FastSAC training pipeline and replace the continuous critic with the same C51 critic family used in FastTD3, while adding DEM to the actor. All C51-specific hyperparameters follow FastTD3, including the support range and number of atoms. To keep the comparison controlled, we align shared hyperparameters such as weight decay, target entropy, and log-standard-deviation bounds ([ _−_ 10 _,_ 1]) with FastDSAC, while leaving the remaining settings consistent with the inherited FastSAC/FastTD3 configurations. The DEM-specific settings follow the main FastDSAC setup, using a fixed temperature _τ_ = 1 together with the same heterogeneity range _βe ∼ U_ [ _β_ min _, β_ max]. LayerNorm usage again follows the same benchmark-specific rule as above. 

Overall, these baselines rigorously adhere to the stable configurations from their official codebases. We introduce only minimal, strictly controlled alignments (e.g., matching the target entropy) to ensure a fair comparison, explicitly avoiding any extensive per-baseline retuning that might introduce bias. 

#### **A.4 Detailed Implementation Recipe** 

To ensure stability and peak performance in the high-throughput continuous control regime, we adopt specific algorithmic and engineering choices grounded in recent literature and our empirical experiments. 

**1. Layer Normalization (LayerNorm).** We apply LayerNorm in the actor and critic networks exclusively for the ultra-high-dimensional HumanoidBench domain ( _|A|_ = 61). Consistent with recent findings [29, 30, 28], this regularization is critical for maintaining stable gradient flow in expansive action spaces. Conversely, for the MuJoCo Playground and IsaacLab tasks featuring smaller action spaces, FastDSAC achieves peak performance without LayerNorm. This contrast demonstrates that our performance gains stem primarily from core algorithmic mechanisms (DEM and continuous critic) rather than architectural dependencies. A comprehensive empirical analysis justifying these domain-specific choices is provided in Appendix K. 

**2. Target Entropy.** Following recent work [28], we set the target entropy _H_ = 0 across all tasks. In high-dimensional spaces, the standard heuristic ( _H_ = _−|A|_ ) enforces aggressive variance decay, forcing the policy to prematurely drop its exploration budget and exacerbating the “vanishing exploration” problem. By setting _H_ = 0, we explicitly maintain a generous global exploration budget to prevent premature convergence (empirically validated in Appendix L). While such high unmodulated variance would normally destabilize a complex humanoid, DEM structurally manages it. As analyzed in Section 4.3, DEM safely offloads this excess entropy onto redundant joints, thereby preserving near-deterministic precision on critical actuators. 

**3. Adaptive Temperature Optimization (auto-** _τ_ **).** The unified default DEM temperature ( _τ_ = 1 _._ 0) yields strong and robust performance across the vast majority of evaluated tasks and remains our primary recommendation for general use. However, a small subset of highly dynamic tasks requiring extreme whole-body coordination (e.g., _Hurdle_ and _Balance Hard_ ) intrinsically benefit from uniform variance allocation (or exploration) across action dimension according to empirical experiments. To examine this potential without manual intervention, we introduce an adaptive variant, FastDSAC (auto- _τ_ ), in which _τ_ is treated as a network parameter and optimized end-to-end. Included in the main results (Figure 2) as an "upper bound" of DEM’s autonomous exploration management. While the fixed- _τ_ baseline remains the primary recommendation for general use because of its simplicity, this adaptive extension highlights the potential for future work to discover task-specific coordination patterns without relying on manual kinematic priors. 

**4. High-Precision Critic Stability.** Unlike the original DSAC-T [26], which requires a large numerical stabilizer (bias = 0 _._ 1) to prevent division-by-zero during continuous distribution modeling, the inherently stable statistics derived from our large-batch, high-throughput regime allow us to reduce this bias significantly to 10<sup>_−_6</sup> . This crucial reduction enables the FastDSAC critic to model states with low-variance return distributions with high fidelity, accurately capturing fine-grained reward structures that would otherwise be smoothed out by conservative numerical stabilization. 

15 


Figure 7: **Overview of the FastDSAC architecture. (Left) Actor with DEM:** The policy dynamically redistributes the exploration budget by modulating the base standard deviation _σ_ ˆ _ϕ_ ( _s_ ) with weights _wi_ (via element-wise multiplication _⊙_ ). These weights are derived from logits _l_ ( _s_ ) and an environment-conditioned heterogeneity factor _βe_ using a normalized Softmax. **(Middle) Environment:** Massively parallel environments collect experiences into a shared Replay Buffer for high-throughput training. **(Right) Continuous Critic:** The critic models the value function as a **continuous Gaussian distribution** to ensure accurate value estimation. It minimizes the **KL Divergence** between the current and target distributions, avoiding the quantization artifacts of discrete baselines (marked by _×_ ). 

**5. Implementation Notes.** In implementation, the temperature-scaled DEM logits are clipped to a bounded range before the Softmax for numerical stability, and the base log-standard deviation is mapped to fixed bounds via a tanh parameterization. For heterogeneous exploration, the environmentspecific scaling factor is kept fixed within each episode and resampled only when the episode terminates, consistent with the mixed scaling exploration implementation inherited from FastTD3. 

### **B Extended Details on Sim-to-Real Validation** 

To further examine whether the simulated performance of FastDSAC carries over to physical hardware, we deploy the learned policies on a Unitree G1 humanoid using the mature sim-to-real pipeline [28]. This appendix summarizes the training pipeline, task setup, and deployment results behind the main-text results in Section 4.4. 

**Training Pipeline and Domain Randomization.** Policies are trained entirely in simulation using massive parallelization. To reduce the reality gap, the training pipeline applies domain randomization to key physical factors, including mass, friction, motor damping, latency, and external push perturbations. The final real-world performance should therefore be interpreted as the combined outcome of the strong FastDSAC method and the maturity of this underlying domain randomization pipeline. 

**Task Formulations and Minimal Adaptation.** We evaluate two policy classes: (1) a joystickconditioned locomotion policy (shown in the main text, Figure 6), and (2) a complex motion-tracking policy shown here. Crucially, the algorithmic adaptation is minimal. The core hyperparameters of FastDSAC (e.g., learning rates, DEM target entropy _H_ = 0) remain identical to those used in the simulated IsaacLab (and MuJoCo Playground) experiments. We modify only environmentspecific rollout settings to match the established deployment recipes, using _γ_ = 0 _._ 99 for motion tracking and _γ_ = 0 _._ 97 for locomotion, together with the corresponding multi-step return horizons and update-to-data ratios. 

**Deployment Results.** The learned policies run directly on the G1’s onboard computer. For the locomotion task, the robot tracks real-time joystick commands; for motion tracking, it follows the reference “squat-carry-walk-squat” sequence. Figure 8 presents time-lapse sequences of backward walking and the motion-tracking policy. Both policies show strong zero-shot stability and remain stable under moderate physical push perturbations. These observations are consistent with the main-text result that policies trained with FastDSAC in simulation can transfer to robust real-world control. 

16 


(a) Joystick-conditioned backward walking 


(b) “Squat-carry-walk-squat” motion tracking 

Figure 8: **Additional Sim-to-Real Results.** Time-lapse sequences of zero-shot FastDSAC policies deployed on the Unitree G1. The robot executes backward walking under real-time joystick commands and a “squat-carry-walk-squat” motion-tracking sequence. 

### **C Supplementary Background on FastTD3 and DSAC-T** 

#### **C.1 FastTD3 Recipe Inherited by FastDSAC** 

FastTD3 is presented as a simplified high-throughput TD3 recipe built from parallel simulation, large-batch updates, a distributional critic, and tuned hyperparameters [5]. The original paper emphasizes that massively parallel environments primarily improve wall-clock efficiency and also increase data diversity, which helps deterministic policy gradients compensate for weak singletrajectory exploration. It further reports that an unusually large batch size of 32 _,_ 768 stabilizes critic learning under massively parallel rollouts, and that the resulting diversity can reduce the effective off-policyness of updates enough to keep training stable even without residual connections or LayerNorm. 

For value estimation, FastTD3 adopts a discrete distributional critic from the C51 family: 


where _{zi}_<sup>_N_</sup> _i_ =1<sup>is a fixed support spanning [</sup><sup>_v_min</sup><sup>_, v_max],</sup><sup>_pθ,i_(</sup><sup>_s, a_) is the predicted probability of atom</sup> _zi_ , and _δzi_ denotes a Dirac mass. Given the target action from the TD3 target actor, the distributional Bellman target is 

_T Zθ_<sup>C51</sup><sup>_′_</sup> ( _s, a_ ) = _r_ ( _s, a_ ) + _γZθ_<sup>C51</sup><sup>_′_</sup> ( _s_<sup>_′_</sup> _, a_<sup>_′_</sup> ) _,_ (11) which is projected back onto the fixed support to obtain **_m_** = Φ _T Zθ_<sup>C51</sup><sup>_′_</sup> . The critic is then trained by the Cross-Entropy objective 


This discrete critic is helpful in the original FastTD3 study, but it introduces support-related hyperparameters ( _v_ min _, v_ max) and keeps value learning tied to a fixed atomization of returns. FastDSAC retains the same high-throughput protocol and replay/update structure, but replaces this critic family with a continuous Gaussian critic to avoid support tuning and quantization artifacts. 

Beyond the critic parameterization, the FastTD3 recipe includes two implementation patterns that are inherited conceptually in FastDSAC. First, FastTD3 studies a mixed exploration-noise schedule across environments, 


and reports that although the mixed-noise scheme itself does not produce a major gain, it remains a cheap way to expose parallel environments to diverse exploration scales. FastDSAC inherits this spirit through heterogeneous DEM scaling factors _βe_ , while replacing global noise-scale variation with structured, dimension-wise variance redistribution. Second, FastTD3 keeps the optimization recipe deliberately simple: standard MLP backbones, low update-to-data ratios, and benchmark-specific 

17 

parallel rollout protocols summarized in Appendix A. FastDSAC preserves this training backbone so that the main algorithmic difference remains the actor-side exploration structure and the critic parameterization. 

#### **C.2 DSAC-T Components Used in FastDSAC** 

For completeness, we summarize only the DSAC-T ingredients directly relevant to FastDSAC’s critic design. DSAC and DSAC-T model the return distribution as a continuous Gaussian, so the critic directly predicts both the mean Q-value and its uncertainty scale [24, 26]: 


Given _a_<sup>_′_</sup> _∼ πϕ_ ( _·|s_<sup>_′_</sup> ) and a target sample _z_<sup>_′_</sup> _∼ Zθ′_ ( _s_<sup>_′_</sup> _, a_<sup>_′_</sup> ), the standard distributional target is 


DSAC begins from a sample-based negative log-likelihood objective for this target return under the current Gaussian critic, 


Under the Gaussian parameterization above, this objective is equivalent, up to constants independent of _θ_ , to 


DSAC decomposes the resulting critic gradient into mean-related and variance-related parts, and stabilizes the latter by clipping the random target return: 


This yields the clipped gradient form 


**Expected Value Substituting.** DSAC-T observes that the first term in Eq. (19) still inherits the randomness of _yz_ . It therefore introduces the target Q-value 


which satisfies E[ _yz | a_<sup>_′_</sup> ] = _yq_ . Replacing the first occurrence of _yz_ by _yq_ gives 


This refinement makes the mean update closer to the non-distributional SAC target and reduces gradient randomness in the critic update. 

**Twin Value Distribution Learning.** The second refinement is a distributional analogue of clipped double Q-learning. DSAC-T trains two Gaussian critics _Zθ_ 1 and _Zθ_ 2 independently and selects the target critic with the smaller mean: 


The target return and target Q-value are then defined as 


18 

Substituting Eq. (23) into Eq. (21) yields the twin-distribution critic update, and the actor objective becomes 


This refinement reduces overestimation bias by building both critic and actor targets from the more conservative value distribution. 

**Variance-Based Critic Gradient Adjustment.** The third refinement removes the fixed clipping boundary and the reward-scale sensitivity of the mean update. DSAC-T sets the clipping boundary adaptively as 


where _ξ_ is a constant controlling the clipping range (typically set _ξ_ = 3, following the three-sigma rule), and introduces the variance-based scaling weight 


Using moving averages _bj_ and _ωj_ for the two critics, the DSAC-T gradient becomes 


The corresponding moving-average updates are 


FastDSAC keeps the first two refinements because they are directly compatible with our highthroughput setting. For the third, we only retain the gradient scaling idea. In the final implementation, Section 3.2 removes the dynamic clipping boundary, uses an unclipped sampled-target variance update, and reduces the numerical stabilizer to better resolve low-variance states in the large-batch regime. 

### **D Architecture and Pseudocode of FastDSAC** 

We provide the complete pseudocode for FastDSAC in Algorithm 1. For FastDSAC architecture, please refer to Figure 7. 

19 

**Algorithm 1** FastDSAC 

**Require:** _n_ parallel environments, replay buffer _B_ , updates per step _U_ , discount _γ_ , Polyak coefficient _τpolyak_ , DEM temperature _τ_ , heterogeneity range [ _β_ min _, β_ max], target entropy _H_ . **Ensure:** Learned policy parameters _ϕ_ . 1: Initialize actor _πϕ_ with output heads ( _µϕ,_ ˆ _σϕ, lϕ_ ), twin critics _Zθj_ ( _s, a_ ) _∼ N_ ( _Qθj_ ( _s, a_ ) _, σθ_<sup>2</sup> _j_<sup>(</sup><sup>_s, a_)), target parameters</sup><sup>_θ_</sup> _j_<sup>_′←θj_, entropy coefficient</sup><sup>_α_, and</sup><sup>_B←∅_.</sup> 2: **for** each training iteration **do** 3: **Parallel Rollout:** 4: **for** environment _e ∈_ [ _n_ ] **in parallel do** 5: Sample heterogeneity factor _βe ∼U_ [ _β_ min _, β_ max], observe _s_<sup>(</sup> _t_<sup>_e_).</sup> 6: Forward pass: ( _µ,_ ˆ _σ, l_ ) _← πϕ_ ( _st_<sup>(</sup><sup>_e_)).</sup> 7: Compute dimension-wise weights: _we ← N ·_ Softmax( _βel/τ_ ) per Eq. (4). 8: Modulate exploration: _σe ← we ⊙_ exp(ˆ _σ_ ). 9: Sample noise _ξ ∼N_ (0 _, I_ ), execute action _a_<sup>(</sup> _t_<sup>_e_)</sup> _← µ_ + _σe ⊙ ξ_ . 10: Collect transition ( _s_<sup>(</sup> _t_<sup>_e_)</sup><sup>_, a_(</sup> _t_<sup>_e_)</sup><sup>_, r_</sup> _t_<sup>(</sup><sup>_e_)</sup><sup>_, s_(</sup> _t_ +1<sup>_e_)</sup><sup>_, d_</sup> _t_<sup>(</sup><sup>_e_)), store in</sup><sup>_B_.</sup> 11: **end for** 12: **Distributional Soft Policy Evaluation & Improvement:** 13: **for** gradient step _u ∈_ [ _U_ ] **do** 14: Sample batch ( _s, a, r, s_<sup>_′_</sup> _, d_ ) _∼B_ , compute ¯ _γ ← γ_ (1 _− d_ ). 15: _Evaluation:_ Sample next action _a_<sup>_′_</sup> _∼ πϕ_ ( _·|s_<sup>_′_</sup> ), compute target _yq_<sup>min</sup> _← r_ + _γ_ ¯(min _j∈{_ 1 _,_ 2 _} Qθj_<sup>_′_(</sup><sup>_s′, a′_)</sup><sup>_−α_log</sup><sup>_πϕ_(</sup><sup>_a′|s′_)).</sup> 16: **for** _j ∈{_ 1 _,_ 2 _}_ **do** 17: Sample _zj_<sup>_′∼Zθ_</sup> _j_<sup>_′_(</sup><sup>_s′, a′_), compute</sup><sup>_yz,j←r_+ ¯</sup><sup>_γ_</sup> � _zj_<sup>_′−α_log</sup><sup>_πϕ_(</sup><sup>_a′|s′_)</sup> �. 18: Compute critic scaling: _ωj ←_ E _B_ [ _σθ_<sup>2</sup> _j_<sup>(</sup><sup>_s, a_)].</sup> 19: Update critic: _θj ← θj − ηQ∇θj JZ_ via Eq. (7) with ( _yq_<sup>min</sup> _, yz,j, ωj_ ). 20: **end for** 21: _Improvement:_ Sample action _a ∼ πϕ_ ( _·|s_ ) from batch. 22: Update actor: _ϕ ← ϕ − ηπ∇ϕL_ actor where _L_ actor = E[ _α_ log _πϕ_ ( _a|s_ ) _− Qθ_ ( _s, a_ )]. 23: Optimize entropy coefficient: _α ← α − ηα_ E[ _−_ log _πϕ_ ( _a|s_ ) _−H_ ]. 24: Target update: _θj_<sup>_′←_(1</sup><sup>_−τpolyak_)</sup><sup>_θ_</sup> _j_<sup>_′_+</sup><sup>_τpolyakθj_for</sup><sup>_j∈{_1</sup><sup>_,_2</sup><sup>_}_.</sup> 25: **end for** 26: **end for** 

### **E Related Work** 

**Scalable Reinforcement Learning for High-Dimensional Control.** Recent advances in physics simulation have shifted RL for high-dimensional humanoid control toward massively parallel training regimes [6, 11, 12]. In this high-throughput setting, deterministic off-policy methods such as Parallel Q-Learning (PQL) [8] and FastTD3 [5] have been especially successful, largely because their training dynamics remain stable under aggressive replay-based updates in large action spaces. More recently, stochastic off-policy RL has also begun to benefit from this regime. For example, FlashSAC [13] demonstrates that SAC can be scaled effectively through recipe-level stabilization and improved system throughput. However, its evidence on HumanoidBench is primarily concentrated on lower-dimensional H1 locomotion tasks, whereas our focus is the considerably more challenging 61-dimensional H1Hand whole-body control setting, evaluated across a comprehensive suite of 25 diverse tasks. 

Model-based approaches such as DreamerV3 [2], TD-MPC2 [1], and TDMPBC [4] can achieve strong sample efficiency, but they typically introduce substantial computational overhead from worldmodel learning and inference, often leading to longer wall-clock training in large-scale continuouscontrol settings. By contrast, model-free off-policy methods remain attractive in massively parallel environments because they better exploit simulator throughput. 

From a methodological perspective, Maximum Entropy RL methods such as SAC offer appealing exploration and robustness properties [14], but their effectiveness deteriorates sharply as action dimensionality grows. In practice, applying SAC to domains with _|A| >_ 60 has remained challenging 

20 

due to the curse of dimensionality, often requiring substantial architectural modification and still frequently underperforming strong deterministic baselines on the most difficult tasks [25, 5, 13]. FastDSAC is designed specifically for this regime. Rather than relying solely on scaling heuristics or abandoning stochasticity in favor of deterministic actors, FastDSAC directly targets the two core bottlenecks that hinder stochastic off-policy RL in very high-dimensional control: ineffective exploration and unstable value estimation. FastDSAC fills this gap by making stochastic maximum entropy RL practical in the high-throughput, 61-DoF control regime, where prior success has been dominated by deterministic methods. 

**Maximum Entropy RL and Value Estimation in High Dimensions.** Scaling Soft Actor-Critic (SAC) to high-dimensional action spaces introduces two fundamental challenges: inefficient exploration and value overestimation. 

First, standard Gaussian policies suffer from _vanishing exploration_ [18], where the effective exploration volume collapses as dimensionality increases. Moreover, they allocate variance uniformly across both task-relevant and redundant action dimensions, resulting in poorly directed exploration [16, 3]. Recent works address this issue from different perspectives. QFLEX [18] mitigates the issue through flow-based action modeling. ERA [19] proposes a different route by enforcing a minimum sampling-entropy threshold through output-layer activations, and reports gains across multiple continuous-control algorithms, including FastSAC-ERA on HumanoidBench. FastDSAC is related to ERA in spirit, since both methods reshape how stochasticity is expressed by the actor, but the underlying mechanisms differ. ERA imposes an explicit minimum-entropy constraint through output-layer activations, whereas our Dimension-wise Entropy Modulation (DEM) autonomously redistributes the exploration variance across specific dimensions based on task demands, avoiding the need for rigid, hard-coded entropy thresholds. 

Second, accurate Q-function estimation becomes increasingly difficult in high-dimensional spaces due to severe extrapolation errors on out-of-distribution (OOD) actions [20, 21]. This often results in _Q-bias explosion_ [20] and pronounced overestimation, as the policy progressively over-exploits artifacts in the critic approximation [22]. To mitigate this issue, prior methods such as TQC [23] and FastTD3 [5] adopt distributional RL with truncated quantiles or categorical atoms (C51), respectively. While effective, these discrete approximations depend on manually specified value supports and a finite number of atoms, which can be brittle under varying reward scales and may introduce quantization error that limits value precision. 

In contrast, FastDSAC employs a Continuous Gaussian Critic [26]. Rather than truncating the upper tail as in TQC, our critic models the full return distribution in a continuous form, thereby avoiding fixed-support discretization. Furthermore, by disentangling the gradient estimators, the continuous critic naturally suppresses mean updates on highly uncertain actions through inverse-variance scaling, providing a principled mechanism for reducing overestimation in high-dimensional settings. 

### **F Comparison with Contemporary Works** 

To strictly assess the scalability of FastDSAC, we compare it against two recent concurrent methods, FastSAC-ERA [19] and FlashSAC [13]. We evaluate these baselines on the challenging 61-DoF _Basketball_ and _Balance Hard_ tasks. The learning curves are presented in Figure 9. 

**Comparison with FastSAC-ERA.** ERA maintains exploration by enforcing a global minimum entropy threshold. However, as shown in Figure 9(a), FastSAC-ERA plateaus early at suboptimal returns (e.g., _≈_ 100 in _Balance Hard_ ). This underperformance highlights a fundamental limitation of global entropy constraints in very high-dimensional control: enforcing a uniform entropy lower bound prevents the localized variance pruning required for precision-critical joints. Successfully coordinating a 61-DoF system requires selectively offloading variance to redundant joints, a structure that rigid global thresholds inherently disrupt. 

**Comparison with FlashSAC.** FlashSAC improves wall-clock efficiency through system-level throughput optimizations and recipe-level heuristics, demonstrating strong results on lowerdimensional locomotion ( _|A| ≈_ 20). However, when applied to the 61-DoF regime shown in Figure 9(b), it struggles to learn effective behaviors, scoring below 200 even after 10<sup>6</sup> environment steps. While FlashSAC’s system engineering is valuable for simulation performance and real robot 

21 

deployment, its performance drop in higher dimensions suggests that raw throughput cannot substitute for explicit algorithmic mechanisms (such as DEM) needed to overcome the curse of dimensionality. 


(a) Comparison with FastSAC-ERA 


Figure 9: Performance comparison against concurrent baselines on 61-DoF HumanoidBench tasks. **(a)** FastSAC-ERA plateaus early, as global entropy thresholds restrict localized variance pruning. **(b)** FlashSAC struggles to scale to the 61-DoF regime despite extended training budgets, highlighting the necessity of algorithmic exploration mechanisms. 

### **G Computational Resources** 

We conducted our experiments on a heterogeneous computing cluster consisting of high-performance workstations. The experiments were distributed across two primary hardware configurations: 

(1) **Configuration A:** Equipped with an Intel Core i7-14700K CPU (20 physical cores, 28 logical threads) and 128 GB of system RAM. Accelerated computing was provided by a single NVIDIA GeForce RTX 4090. 

(2) **Configuration B:** Equipped with an AMD Ryzen 9 9950X CPU (16 physical cores, 32 logical threads) and 192 GB of system RAM. This node features an NVIDIA RTX 6000 (Blackwell Workstation Edition) with 96 GB of VRAM, facilitating large-scale parallel training. 

**Resource Allocation.** To ensure efficient training and accommodate varying memory requirements, the memory-intensive IsaacLab environments, specifically _Isaac-Velocity-Flat-G1-v0_ , _Isaac-VelocityRough-G1-v0_ , _Isaac-Repose-Cube-Allegro-Direct-v0_ , and _Isaac-Repose-Cube-Shadow-Direct-v0_ , were trained on **Configuration B** to leverage its extensive VRAM capacity. All other tasks, including the HumanoidBench and MuJoCo Playground suites, were trained on **Configuration A** . This hardware setup ensured efficient training on high-dimensional tasks, with each experiment converging in under 5 hours. 

### **H Computational Efficiency and Wall-Clock Time** 

We evaluate the wall-clock training time of FastDSAC against FastTD3 across nine representative tasks from HumanoidBench, IsaacLab, and MuJoCo Playground (Figure 10 and Table 3). To ensure a strictly controlled evaluation, both algorithms were benchmarked locally on identical hardware (a single NVIDIA GeForce RTX 4090 GPU and an Intel Core i7-14700K CPU). This hardware configuration naturally yields different absolute timings compared to the A100 GPUs used in the original FastTD3 publication. 

Across all nine tasks, FastTD3 requires 20.21 hours in total, whereas FastDSAC requires 22.28 hours. This corresponds to an overall relative time ratio of 1.10 _×_ (geometric mean: 1.09 _×_ ). These results demonstrate that FastDSAC maintains comparable computational efficiency to the highly optimized FastTD3 baseline. Crucially, FastDSAC delivers significantly stronger performance and stability with only a marginal _≈_ 10% overhead in training time. 

22 


Figure 10: **Wall-clock time comparison between FastDSAC and FastTD3.** Evaluated on representative tasks from HumanoidBench, IsaacLab, and MuJoCo Playground. Left: absolute per-task total training time (hours). Right: relative wall-clock time normalized against FastTD3, detailing per-task ratios, the geometric-mean ratio, and the overall total-time ratio across all nine tasks. 

|Benchmark|Task|Steps|FastTD3 (h)|FastDSAC (h)|Rel. Time|
|---|---|---|---|---|---|
|HB|Balance Hard|250K|3.01|3.33|1.10_×_|
|HB|Basketball|250K|2.73|3.39|1.24_×_|
|HB|Hurdle|300K|4.08|4.21|1.03_×_|
|HB|Sit Hard|150K|1.78|2.05|1.15_×_|
|HB|Window|250K|2.96|3.44|1.16_×_|
|IL|Allegro Repose|200K|2.17|2.35|1.08_×_|
|IL|Rough G1|100K|1.87|1.88|1.01_×_|
|PG|G1 Rough|45K|0.97|0.99|1.02_×_|
|PG|T1 Rough|45K|0.63|0.65|1.03_×_|
|HB|Geo. mean|–|–|–|1.13_×_|
|IL|Geo. mean|–|–|–|1.04_×_|
|PG|Geo. mean|–|–|–|1.03_×_|
|All|Geo. mean|–|–|–|1.09_×_|
|All|Total|–|20.21|22.28|1.10_×_|


Table 3: **Wall-clock time comparison on representative HumanoidBench, IsaacLab, and MuJoCo Playground tasks.** All timings were measured locally on a single RTX 4090 GPU. 

23 

### **I Heatmaps of** **_Basketball_ Task** 


Figure 11: **Exploration weights (** _wi_ **) during a Basketball episode.** High weights (bright) concentrate on the left thumb and wrist, while lower weights (dark) on the legs, torso, and right arm. 


Figure 12: **Visualization of exploration weights at different temperatures.** Lower temperatures ( _τ_ = 0 _._ 5) result in highly concentrated weights on specific active joints, whereas higher temperatures ( _τ_ = 10 _._ 0) lead to a nearly uniform distribution across all joints. 

24 

### **J C51 Support Sensitivity on** **_Basketball_** 

To directly examine the fixed-support issue for discrete critics, we varied the support range of C51+DEM on _h1hand-basketball-v0_ while keeping the actor architecture and the remaining training pipeline unchanged. As shown in Figure 13, the performance of C51+DEM changes substantially with the support range: a narrower support achieves the best performance, while wider supports lead to noticeably worse results for _Basketball_ task. This sensitivity indicates that the support range constitutes an additional tuning axis for discrete critics in our setting. In contrast, FastDSAC avoids this support-specification burden by modeling the return distribution continuously. 


Figure 13: **Support sensitivity of C51** + **DEM on** **_Basketball_ .** We vary the C51 support range while keeping the remaining training pipeline unchanged. The resulting performance differences show that discrete critics can be sensitive to support specification on this task, whereas FastDSAC avoids this additional tuning axis. 

### **K Ablation Study on Layer Normalization** 

To isolate the effect of Layer Normalization (LayerNorm) from our core algorithmic contributions, we conduct an ablation study on representative tasks from all three benchmarks, evaluating FastDSAC with and without LayerNorm. The results are shown in Figure 14. 

**Importance in High-Dimensional Settings (HumanoidBench).** In the very high-dimensional domain ( _|A|_ = 61), LayerNorm serves as a key architectural stabilizer. As shown in the top row of Figure 14, removing LayerNorm substantially degrades training dynamics. Specifically, the agent exhibits high inter-seed variance in _Basketball_ , severe optimization oscillations and lower asymptotic returns in _Balance Hard_ , and drastically reduced sample efficiency in _Walk_ . These results suggest that, in expansive continuous action spaces, LayerNorm helps stabilize intermediate feature scales, leading to more reliable convergence and more sample-efficient learning in expansive continuous action spaces. 

**Limited Impact in Lower-Dimensional Settings (IsaacLab & MuJoCo Playground).** Conversely, in domains with moderate action dimensionality ( _|A| <_ 30), the FastDSAC framework remains stable even without LayerNorm. As shown in the bottom row of Figure 14, while adding LayerNorm yields marginal asymptotic improvements in certain manipulation tasks (e.g., _Allegro Repose_ ), it has little effect on locomotion tasks overall, slightly degrading performance on _Rough H1_ while providing only a marginal improvement on _Rough Terrain_ . More importantly, even without LayerNorm, FastDSAC consistently outperforms the FastTD3 baselines in these domains (as established in Section 4.2). We therefore omit LayerNorm in these environments to highlight that FastDSAC’s strong performance 

25 

primarily stems from Dimension-wise Entropy Modulation (DEM) and the continuous distributional critic, rather than from architectural heuristics. 


Figure 14: Ablation study of Layer Normalization. **Top row (HumanoidBench,** _|A|_ = 61 **):** Removing LayerNorm induces seed sensitivity, severe oscillations, and poor sample efficiency. **Bottom row (IsaacLab & MuJoCo Playground,** _|A| <_ 30 **):** FastDSAC remains highly stable and sample-efficient even without LayerNorm, indicating that the core algorithm is robust in lowerdimensional settings. 

### **L Ablation Study on Target Entropy** 

In standard maximum entropy RL, the target entropy is typically set to _H_ = _−|A|_ to regulate exploration. To evaluate our choice of _H_ = 0, we conduct an ablation study on the 61-DoF _Basketball_ task, comparing it against the standard heuristic ( _H_ = _−_ 61). 

**Premature Convergence under the Standard Setting.** As shown in Figure 15, enforcing the standard target ( _H_ = _−_ 61) results in high inter-seed variance. While some seeds converge to near-optimal policies, others become prematurely trapped in local minima (converging to returns of approximately 300). This substantially degrades the average asymptotic performance, with final returns reaching only around 650. 

_Analysis:_ In a 61-DoF action space, _H_ = _−_ 61 induces rapid variance decay. As a result, the policy is forced to reduce its global exploration budget before identifying effective whole-body coordination patterns. 


Figure 15: Ablation on target entropy in _Basketball_ . The standard heuristic ( _H_ = _−_ 61) forces rapid variance decay, causing high inter-seed variance and premature convergence (orange curve). FastDSAC maintains _H_ = 0 to provide sufficient exploration capacity, which is structurally stabilized by DEM. Both curves report results over 3 seeds. 

#### **Structural Management of High Entropy.** Set- 

ting _H_ = 0 prevents premature convergence by maintaining a sustained exploration budget throughout training. While such uniformly high variance would typically destabilize high-dimensional humanoid control, DEM manages this budget structurally. As analyzed in Section 4.3, DEM prevents instability by offloading the excess variance onto redundant joints, preserving near-deterministic precision on critical actuators. Consequently, _H_ = 0 provides sufficient exploration capacity, and DEM ensures its stable allocation, yielding consistent and better convergence. 

26 

### **M Sensitivity to DEM Temperature** 

To examine how the fixed DEM temperature affects learning, we compare different _τ_ values on three representative tasks: _Hurdle_ , _Room_ , and _Stair_ (Figure 16). For _Room_ and _Stair_ , we evaluate _τ ∈{_ 0 _._ 5 _,_ 1 _,_ 5 _}_ ; for _Hurdle_ , we additionally include _τ_ = 10. 

The effect is clearly task-dependent. On _Stair_ , the three temperatures _τ ∈{_ 0 _._ 5 _,_ 1 _,_ 5 _}_ all lead to similar final performance, indicating that this task is relatively insensitive to the precise sparsity level induced by DEM. On _Room_ , the default setting _τ_ = 1 performs best, which aligns with our use of _τ_ = 1 as the unified default configuration. On _Hurdle_ , however, a larger temperature is more effective: _τ_ = 10 achieves the best final return, while the default _τ_ = 1 is weaker than _τ_ = 0 _._ 5, _τ_ = 5, and _τ_ = 10. This suggests that some highly dynamic coordination tasks can benefit from a less concentrated variance redistribution. 

These observations motivate the FastDSAC (auto- _τ_ ) variant. We indeed observe that end-to-end temperature optimization can further improve performance on some tasks. At the same time, since the fixed- _τ_ configuration already performs strongly across the three benchmarks, we do not pursue this direction further here and instead leave a broader study of automatic temperature adaptation to future work. 


Figure 16: **Sensitivity to the DEM temperature** _τ_ **.** Learning curves on _Hurdle_ , _Room_ , and _Stair_ under different fixed temperatures. The default setting _τ_ = 1 remains a robust choice overall. _Room_ favors _τ_ = 1, _Stair_ shows similar performance across _τ ∈{_ 0 _._ 5 _,_ 1 _,_ 5 _}_ , and _Hurdle_ benefits from a larger temperature, with _τ_ = 10 achieving the best final return. 

27 

### **N Full Results** 


Figure 17: **Full results across all benchmarks.** Curves show mean return over training steps with shaded regions indicating the min-max range across 3 seeds. **(a) HumanoidBench (25 tasks):** FastDSAC (blue) is compared against FastTD3 (black), FastSAC Standard (red), and leading baselines including DreamerV3 (orange), TD-MPC2 (pink), SAC (purple), and PPO (green). FastDSAC often outperforms or matches these baselines across locomotion (e.g., _Run_ , _Hurdle_ ), fine manipulation (e.g., _Insert_ ), and complex whole-body coordination (e.g., _Basketball_ , _Balance_ ), combining strong exploration with stable training. **(b) IsaacLab and MuJoCo Playground (10 tasks):** FastDSAC (blue) is compared against FastTD3 (black), FastSAC Standard (red), and PPO (green). On IsaacLab, FastDSAC performs strongly on locomotion (Velocity Flat/Rough H1/G1) and Repose Cube Allegro, while remaining competitive on Repose Cube Shadow. On MuJoCo Playground, FastDSAC consistently outperforms baselines on G1/T1 Joystick with lower variance and higher asymptotic returns. 

28 

### **O Discussion of Limitations, Future Directions and Impact** 

**Limitations.** The primary limitation of FastDSAC is that Dimension-wise Entropy Modulation (DEM) assumes independent exploration noise across action dimensions (i.e., utilizing a diagonal covariance matrix). While this formulation effectively scales to 61-DoF systems, it precludes the modeling of correlated exploration strategies among interdependent joints. Furthermore, maintaining a continuous distributional critic to ensure accurate value estimation comes at the cost of a marginal increase in computational overhead during training compared to purely deterministic baselines. 

**Future Directions.** An important direction for future work is to study how structured covariance models might be used to capture joint dependencies, and how end-to-end optimization of DEM’s temperature parameter can enable fully autonomous variance scheduling. 

**Impact Statements.** This paper presents work whose goal is to advance the field of Deep Reinforcement Learning. The deployment of such agile autonomous systems raises valid safety concerns regarding unintended physical interaction and potential long-term economic impacts on the workforce. Consequently, real-world application of these policies necessitates robust verification protocols and rigorous safety constraints to prevent accidents and ensure physical safety. 

29 

### **NeurIPS Paper Checklist** 

1. **Claims** 

Question: Do the main claims made in the abstract and introduction accurately reflect the paper’s contributions and scope? 

Answer: [Yes] 

Justification: The abstract and introduction state the same core contributions that are later supported by the experiments and conclusion: DEM, the continuous distributional critic, strong results on 35 tasks, and zero-shot sim-to-real transfer (Abstract, Introduction, Sections 4.2–4.4, Conclusion). 

Guidelines: 

- The answer [N/A] means that the abstract and introduction do not include the claims made in the paper. 

- The abstract and/or introduction should clearly state the claims made, including the contributions made in the paper and important assumptions and limitations. A [No] or [N/A] answer to this question will not be perceived well by the reviewers. 

- The claims made should match theoretical and experimental results, and reflect how much the results can be expected to generalize to other settings. 

- It is fine to include aspirational goals as motivation as long as it is clear that these goals are not attained by the paper. 

#### 2. **Limitations** 

Question: Does the paper discuss the limitations of the work performed by the authors? Answer: [Yes] 

Justification: The paper includes a dedicated limitations section in Section O. It explicitly notes the diagonal-covariance assumption in DEM and the marginal training overhead of the continuous critic, and it also points to structured covariance models and auto- _τ_ as future directions. 

Guidelines: 

- The answer [N/A] means that the paper has no limitation while the answer [No] means that the paper has limitations, but those are not discussed in the paper. 

- The authors are encouraged to create a separate “Limitations” section in their paper. 

- The paper should point out any strong assumptions and how robust the results are to violations of these assumptions (e.g., independence assumptions, noiseless settings, model well-specification, asymptotic approximations only holding locally). The authors should reflect on how these assumptions might be violated in practice and what the implications would be. 

- The authors should reflect on the scope of the claims made, e.g., if the approach was only tested on a few datasets or with a few runs. In general, empirical results often depend on implicit assumptions, which should be articulated. 

- The authors should reflect on the factors that influence the performance of the approach. For example, a facial recognition algorithm may perform poorly when image resolution is low or images are taken in low lighting. Or a speech-to-text system might not be used reliably to provide closed captions for online lectures because it fails to handle technical jargon. 

- The authors should discuss the computational efficiency of the proposed algorithms and how they scale with dataset size. 

- If applicable, the authors should discuss possible limitations of their approach to address problems of privacy and fairness. 

- While the authors might fear that complete honesty about limitations might be used by reviewers as grounds for rejection, a worse outcome might be that reviewers discover limitations that aren’t acknowledged in the paper. The authors should use their best judgment and recognize that individual actions in favor of transparency play an important role in developing norms that preserve the integrity of the community. Reviewers will be specifically instructed to not penalize honesty concerning limitations. 

30 

#### 3. **Theory assumptions and proofs** 

Question: For each theoretical result, does the paper provide the full set of assumptions and a complete (and correct) proof? 

Answer: [N/A] 

Justification: The paper does not present proofs; the convergence statement is attributed to prior DSAC/DSAC-T work, while the rest of the paper focuses on algorithm design and experiments. 

Guidelines: 

   - The answer [N/A] means that the paper does not include theoretical results. 

   - All the theorems, formulas, and proofs in the paper should be numbered and crossreferenced. 

   - All assumptions should be clearly stated or referenced in the statement of any theorems. 

   - The proofs can either appear in the main paper or the supplemental material, but if they appear in the supplemental material, the authors are encouraged to provide a short proof sketch to provide intuition. 

   - Inversely, any informal proof provided in the core of the paper should be complemented by formal proofs provided in appendix or supplemental material. 

   - Theorems and Lemmas that the proof relies upon should be properly referenced. 

4. **Experimental result reproducibility** 

Question: Does the paper fully disclose all the information needed to reproduce the main experimental results of the paper to the extent that it affects the main claims and/or conclusions of the paper (regardless of whether the code and data are provided or not)? 

Answer: [Yes] 

Justification: The paper provides: (1) an anonymous implementation link in the Introduction; (2) complete hyperparameter configurations in Appendix A; (3) benchmark/task lists, training protocols, seed counts, and evaluation settings in Section 4 and Appendix A; (4) sim-to-real deployment details in Appendix B. All baselines use public codebases with configuration details specified. 

Guidelines: 

- The answer [N/A] means that the paper does not include experiments. 

- If the paper includes experiments, a [No] answer to this question will not be perceived well by the reviewers: Making the paper reproducible is important, regardless of whether the code and data are provided or not. 

- If the contribution is a dataset and/or model, the authors should describe the steps taken to make their results reproducible or verifiable. 

- Depending on the contribution, reproducibility can be accomplished in various ways. For example, if the contribution is a novel architecture, describing the architecture fully might suffice, or if the contribution is a specific model and empirical evaluation, it may be necessary to either make it possible for others to replicate the model with the same dataset, or provide access to the model. In general. releasing code and data is often one good way to accomplish this, but reproducibility can also be provided via detailed instructions for how to replicate the results, access to a hosted model (e.g., in the case of a large language model), releasing of a model checkpoint, or other means that are appropriate to the research performed. 

- While NeurIPS does not require releasing code, the conference does require all submissions to provide some reasonable avenue for reproducibility, which may depend on the nature of the contribution. For example 

- (a) If the contribution is primarily a new algorithm, the paper should make it clear how to reproduce that algorithm. 

- (b) If the contribution is primarily a new model architecture, the paper should describe the architecture clearly and fully. 

- (c) If the contribution is a new model (e.g., a large language model), then there should either be a way to access this model for reproducing the results or a way to reproduce the model (e.g., with an open-source dataset or instructions for how to construct the dataset). 

31 

   - (d) We recognize that reproducibility may be tricky in some cases, in which case authors are welcome to describe the particular way they provide for reproducibility. In the case of closed-source models, it may be that access to the model is limited in some way (e.g., to registered users), but it should be possible for other researchers to have some path to reproducing or verifying the results. 

5. **Open access to data and code** 

Question: Does the paper provide open access to the data and code, with sufficient instructions to faithfully reproduce the main experimental results, as described in supplemental material? 

Answer: [Yes] 

Justification: The paper provides an anonymous implementation link and describes how the benchmarks and evaluation pipelines are configured. The experiments rely on public benchmark environments rather than proprietary datasets, and the appendix gives the settings needed to run them (Introduction, Appendix A). 

Guidelines: 

   - The answer [N/A] means that paper does not include experiments requiring code. 

   - Please see the NeurIPS code and data submission guidelines ( `https://neurips.cc/ public/guides/CodeSubmissionPolicy` ) for more details. 

   - While we encourage the release of code and data, we understand that this might not be possible, so [No] is an acceptable answer. Papers cannot be rejected simply for not including code, unless this is central to the contribution (e.g., for a new open-source benchmark). 

   - The instructions should contain the exact command and environment needed to run to reproduce the results. See the NeurIPS code and data submission guidelines ( `https: //neurips.cc/public/guides/CodeSubmissionPolicy` ) for more details. 

   - The authors should provide instructions on data access and preparation, including how to access the raw data, preprocessed data, intermediate data, and generated data, etc. 

   - The authors should provide scripts to reproduce all experimental results for the new proposed method and baselines. If only a subset of experiments are reproducible, they should state which ones are omitted from the script and why. 

   - At submission time, to preserve anonymity, the authors should release anonymized versions (if applicable). 

   - Providing as much information as possible in supplemental material (appended to the paper) is recommended, but including URLs to data and code is permitted. 

6. **Experimental setting/details** 

Question: Does the paper specify all the training and test details (e.g., data splits, hyperparameters, how they were chosen, type of optimizer) necessary to understand the results? 

Answer: [Yes] 

Justification: Section 4 and Appendix A specify the benchmarks, baselines, seed counts, parallel environment counts, replay/update schedules, discount factors, target entropy, and benchmark-specific architectural choices such as LayerNorm. 

Guidelines: 

   - The answer [N/A] means that the paper does not include experiments. 

   - The experimental setting should be presented in the core of the paper to a level of detail that is necessary to appreciate the results and make sense of them. 

   - The full details can be provided either with the code, in appendix, or as supplemental material. 

7. **Experiment statistical significance** 

Question: Does the paper report error bars suitably and correctly defined or other appropriate information about the statistical significance of the experiments? 

Answer: [Yes] 

32 

Justification: The main figures report mean returns over 3 seeds with shaded min-max ranges, and the hardest tasks use 5 seeds with shaded regions spanning the min-max range across seeds, so the paper does provide a clear measure of run-to-run variability for the key results (Sections 4, 4.2, Appendix N). 

Guidelines: 

   - The answer [N/A] means that the paper does not include experiments. 

   - The authors should answer [Yes] if the results are accompanied by error bars, confidence intervals, or statistical significance tests, at least for the experiments that support the main claims of the paper. 

   - The factors of variability that the error bars are capturing should be clearly stated (for example, train/test split, initialization, random drawing of some parameter, or overall run with given experimental conditions). 

   - The method for calculating the error bars should be explained (closed form formula, call to a library function, bootstrap, etc.) 

   - The assumptions made should be given (e.g., Normally distributed errors). 

   - It should be clear whether the error bar is the standard deviation or the standard error of the mean. 

   - It is OK to report 1-sigma error bars, but one should state it. The authors should preferably report a 2-sigma error bar than state that they have a 96% CI, if the hypothesis of Normality of errors is not verified. 

   - For asymmetric distributions, the authors should be careful not to show in tables or figures symmetric error bars that would yield results that are out of range (e.g., negative error rates). 

   - If error bars are reported in tables or plots, the authors should explain in the text how they were calculated and reference the corresponding figures or tables in the text. 

8. **Experiments compute resources** 

Question: For each experiment, does the paper provide sufficient information on the computer resources (type of compute workers, memory, time of execution) needed to reproduce the experiments? 

Answer: [Yes] 

Justification: The Computational Resources section and Appendix H specify the CPU/GPU/RAM configurations, task allocation across hardware, and per-task as well as total wall-clock time needed for the representative experiments. 

Guidelines: 

   - The answer [N/A] means that the paper does not include experiments. 

   - The paper should indicate the type of compute workers CPU or GPU, internal cluster, or cloud provider, including relevant memory and storage. 

   - The paper should provide the amount of compute required for each of the individual experimental runs as well as estimate the total compute. 

   - The paper should disclose whether the full research project required more compute than the experiments reported in the paper (e.g., preliminary or failed experiments that didn’t make it into the paper). 

9. **Code of ethics** 

Question: Does the research conducted in the paper conform, in every respect, with the NeurIPS Code of Ethics `https://neurips.cc/public/EthicsGuidelines` ? 

Answer: [Yes] 

Justification: The work uses public simulation benchmarks and a robot deployment, and the paper does not describe any practice that appears to conflict with the NeurIPS Code of Ethics. No human-subject data, privacy-sensitive data, or prohibited collection practices are involved. 

Guidelines: 

- The answer [N/A] means that the authors have not reviewed the NeurIPS Code of Ethics. 

33 

- If the authors answer [No], they should explain the special circumstances that require a deviation from the Code of Ethics. 

- The authors should make sure to preserve anonymity (e.g., if there is a special consideration due to laws or regulations in their jurisdiction). 

#### 10. **Broader impacts** 

Question: Does the paper discuss both potential positive societal impacts and negative societal impacts of the work performed? 

Answer: [Yes] 

Justification: See Appendix O. 

Guidelines: 

- The answer [N/A] means that there is no societal impact of the work performed. 

- If the authors answer [N/A] or [No], they should explain why their work has no societal impact or why the paper does not address societal impact. 

- Examples of negative societal impacts include potential malicious or unintended uses (e.g., disinformation, generating fake profiles, surveillance), fairness considerations (e.g., deployment of technologies that could make decisions that unfairly impact specific groups), privacy considerations, and security considerations. 

- The conference expects that many papers will be foundational research and not tied to particular applications, let alone deployments. However, if there is a direct path to any negative applications, the authors should point it out. For example, it is legitimate to point out that an improvement in the quality of generative models could be used to generate Deepfakes for disinformation. On the other hand, it is not needed to point out that a generic algorithm for optimizing neural networks could enable people to train models that generate Deepfakes faster. 

- The authors should consider possible harms that could arise when the technology is being used as intended and functioning correctly, harms that could arise when the technology is being used as intended but gives incorrect results, and harms following from (intentional or unintentional) misuse of the technology. 

- If there are negative societal impacts, the authors could also discuss possible mitigation strategies (e.g., gated release of models, providing defenses in addition to attacks, mechanisms for monitoring misuse, mechanisms to monitor how a system learns from feedback over time, improving the efficiency and accessibility of ML). 

#### 11. **Safeguards** 

Question: Does the paper describe safeguards that have been put in place for responsible release of data or models that have a high risk for misuse (e.g., pre-trained language models, image generators, or scraped datasets)? 

Answer: [N/A] 

Justification: The paper does not release a high-risk dual-use model or scraped dataset, so there are no special safeguard procedures to describe beyond the standard anonymous implementation release. 

Guidelines: 

- The answer [N/A] means that the paper poses no such risks. 

- Released models that have a high risk for misuse or dual-use should be released with necessary safeguards to allow for controlled use of the model, for example by requiring that users adhere to usage guidelines or restrictions to access the model or implementing safety filters. 

- Datasets that have been scraped from the Internet could pose safety risks. The authors should describe how they avoided releasing unsafe images. 

- We recognize that providing effective safeguards is challenging, and many papers do not require this, but we encourage authors to take this into account and make a best faith effort. 

12. **Licenses for existing assets** 

34 

Question: Are the creators or original owners of assets (e.g., code, data, models), used in the paper, properly credited and are the license and terms of use explicitly mentioned and properly respected? 

Answer: [Yes] 

Justification: The paper uses open-source benchmarks (HumanoidBench, MuJoCo Playground, IsaacLab) and the FastTD3 codebase. All assets are properly cited in the text with their original papers. HumanoidBench is under MIT License, MuJoCo Playground under Apache 2.0, IsaacLab under BSD 3-Clause, and FastTD3 is publicly available. The Unitree G1 robot is a commercially available platform. 

Guidelines: 

- The answer [N/A] means that the paper does not use existing assets. 

- The authors should cite the original paper that produced the code package or dataset. 

- The authors should state which version of the asset is used and, if possible, include a URL. 

- The name of the license (e.g., CC-BY 4.0) should be included for each asset. 

- For scraped data from a particular source (e.g., website), the copyright and terms of service of that source should be provided. 

- If assets are released, the license, copyright information, and terms of use in the package should be provided. For popular datasets, `paperswithcode.com/datasets` has curated licenses for some datasets. Their licensing guide can help determine the license of a dataset. 

- For existing datasets that are re-packaged, both the original license and the license of the derived asset (if it has changed) should be provided. 

- If this information is not available online, the authors are encouraged to reach out to the asset’s creators. 

#### 13. **New assets** 

Question: Are new assets introduced in the paper well documented and is the documentation provided alongside the assets? 

Answer: [Yes] 

Justification: The new asset here is the anonymous implementation of FastDSAC, and it is documented through the method section, Algorithm 1, the hyperparameter tables, and the sim-to-real appendix. 

Guidelines: 

   - The answer [N/A] means that the paper does not release new assets. 

   - Researchers should communicate the details of the dataset/code/model as part of their submissions via structured templates. This includes details about training, license, limitations, etc. 

   - The paper should discuss whether and how consent was obtained from people whose asset is used. 

   - At submission time, remember to anonymize your assets (if applicable). You can either create an anonymized URL or include an anonymized zip file. 

14. **Crowdsourcing and research with human subjects** 

Question: For crowdsourcing experiments and research with human subjects, does the paper include the full text of instructions given to participants and screenshots, if applicable, as well as details about compensation (if any)? 

Answer: [N/A] 

Justification: The paper does not involve crowdsourcing or any human-subject study; the real-world evaluation is on a humanoid robot, not on participants. 

Guidelines: 

- The answer [N/A] means that the paper does not involve crowdsourcing nor research with human subjects. 

35 

   - Including this information in the supplemental material is fine, but if the main contribution of the paper involves human subjects, then as much detail as possible should be included in the main paper. 

   - According to the NeurIPS Code of Ethics, workers involved in data collection, curation, or other labor should be paid at least the minimum wage in the country of the data collector. 

15. **Institutional review board (IRB) approvals or equivalent for research with human subjects** 

Question: Does the paper describe potential risks incurred by study participants, whether such risks were disclosed to the subjects, and whether Institutional Review Board (IRB) approvals (or an equivalent approval/review based on the requirements of your country or institution) were obtained? 

Answer: [N/A] 

Justification: Because the paper does not collect data from human participants or run a human-subject study, IRB approval is not applicable. 

Guidelines: 

   - The answer [N/A] means that the paper does not involve crowdsourcing nor research with human subjects. 

   - Depending on the country in which research is conducted, IRB approval (or equivalent) may be required for any human subjects research. If you obtained IRB approval, you should clearly state this in the paper. 

   - We recognize that the procedures for this may vary significantly between institutions and locations, and we expect authors to adhere to the NeurIPS Code of Ethics and the guidelines for their institution. 

   - For initial submissions, do not include any information that would break anonymity (if applicable), such as the institution conducting the review. 

16. **Declaration of LLM usage** 

Question: Does the paper describe the usage of LLMs if it is an important, original, or non-standard component of the core methods in this research? Note that if the LLM is used only for writing, editing, or formatting purposes and does _not_ impact the core methodology, scientific rigor, or originality of the research, declaration is not required. 

Answer: [N/A] 

Justification: The core method, experiments, and results do not rely on LLMs, and LLMs were only used for polishing and formatting purposes; the paper’s scientific contributions are entirely in reinforcement learning and robotics. 

Guidelines: 

- The answer [N/A] means that the core method development in this research does not involve LLMs as any important, original, or non-standard components. 

- Please refer to our LLM policy in the NeurIPS handbook for what should or should not be described. 

36 

