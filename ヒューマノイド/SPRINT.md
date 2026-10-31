---
title: "SPRINT: Efficient Spectral Priors for Humanoid Athletic Sprints"
date: "2026-05-27"
authors: "Yantong Wei; Kaihong Huang; Hainan Pan; Jiawei Luo; Jiawei Zhou; Ziyan Mai"
url: https://arxiv.org/abs/2605.28549
pdf: https://arxiv.org/pdf/2605.28549
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2605.28549)** / [論文ページ](https://arxiv.org/abs/2605.28549)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **SPRINT: Efficient Spectral Priors for Humanoid Athletic Sprints** 

Yantong Wei<sup>1</sup><sup>_,†_</sup> , Kaihong Huang<sup>1</sup><sup>_,†_</sup> , Hainan Pan<sup>1</sup> , Jiawei Luo<sup>1</sup> , Jiawei Zhou<sup>1</sup> , Ziyan Mai<sup>1</sup> , Zhiwen Zeng<sup>1</sup> , Yaonan Wang<sup>2</sup> , Huimin Lu<sup>1</sup><sup>_,∗_</sup> 

**_Abstract_ — The pursuit of humanoid athletic sprints is hindered by a scarcity of humanoid-viable kinematic reference data and the inability of existing frameworks to maintain stability during sprints. To overcome these limitations, we introduce SPRINT, a novel framework driven by efficient, frequencyadaptive spectral priors. By characterizing the fundamental periodicity of human locomotion in the frequency domain using a reference library of five discrete motion sequences, these priors generate kinematically feasible joint trajectories across a broad velocity spectrum, successfully extrapolating to speeds that exceed the reference distribution. Guided by these pretrained priors, the SPRINT policy achieves zero-shot sim-toreal transfer in field experiments on the Unitree G1 platform, reaching a peak sprinting velocity of 6 m/s and demonstrating seamless gait transitions while preserving biomimetic naturalness. Ultimately, this work establishes frequency-adaptive spectral priors as a highly data-efficient foundation for humanoid athletic sprints. The project page is available at https: //anonymous.4open.science/w/SPRINT-138A/.** 


Fig. 1: Versatile humanoid locomotion. SPRINT supports a wide range of natural gaits, including walking, jogging, and sprinting. 

**_Index Terms_ — Reinforcement Learning, Humanoid Robots, High-Speed Locomotion.** 

## I. INTRODUCTION 

**A** THLETIChumanoid high-speedsprinting representslocomotion.a However,critical frontierrealizingin stable, high-velocity performance is hindered by a scarcity of kinematic reference data viable for humanoid robots. Furthermore, training robust control policies is complicated by the dual necessity of maintaining tracking precision during high dynamic sprints and executing seamless gait transitions across a broad velocity spectrum. 

Reinforcement Learning (RL) is widely utilized to train complex robotic skills [1], [2]. While reward-based optimization facilitates basic task completion, objective-driven training yields feasible locomotion patterns that lack biomimetic naturalness. Adversarial Motion Priors (AMP) mitigate this limitation by motivating robots to mimic human demonstrations [3], [4]. However, adversarial frameworks are prone to training instability and mode collapse during high-speed sprints, due to the scarcity of corresponding kinematic reference data [5]. Similarly, alternative imitation learning approaches [6]–[9] achieve robust tracking in highly dynamic scenarios but remain limited in their capacity to support continuous velocity scaling and seamless gait transitions. Furthermore, hybrid strategies, such as Adaptive Imitated 

> 1Y. Wei, K. Huang, H. Pan, J. Luo, J. Zhou, Z. Mai, Z. Zeng and H. Lu are with the College of Intelligence Science and Technology, National University of Defense Technology, China. 

> 2Y. Wang is with the School of Artificial Intelligence and Robotics, Hunan University, China. 

> _†_ Co-first author, _∗_ Corresponding author. 

Central Pattern Generators (AI-CPG) [10], remain restricted to peak speeds below 4 m/s in simulation, leaving a critical gap in physical, highly dynamic athletic performance. 

Frequency-adaptive spectral priors form the core of the SPRINT framework, providing fine-grained kinematic guidance to ensure authentic athletic form during high-speed locomotion. We train these spectral priors using a reference library of only five motion sequences (428 frames, 14 s) comprising discrete walking, jogging, and running gaits. By characterizing the inherent periodicity of human locomotion in the frequency domain, we effectively overcome data scarcity. The spectral priors map rhythmic features into kinematically feasible joint trajectories across a broad velocity spectrum, successfully extrapolating to speeds that exceed the reference distribution. 

The SPRINT framework employs a hierarchical architecture integrating high-level spectral priors with low-level stabilization. The pretrained frequency-adaptive spectral priors generate joint trajectories that serve as the primary kinematic reference, while the low-level stabilization employs residual actions to compensate for unmodeled system dynamics and environmental disturbances. In simulation, the SPRINT policy achieves a peak sprinting velocity of 6 m/s while preserving high biomimetic naturalness. Through dynamics randomization and observation noise modeling, we successfully execute zero-shot sim-to-real transfer to the physical Unitree G1 platform (Fig. 1). Ultimately, extensive field experiments validate the capability of the SPRINT policy to execute versatile humanoid locomotion and seamless gait transitions across a broad velocity spectrum. 

Our contributions are summarized as follows: 

- **Frequency-Adaptive Spectral Priors** : We introduce efficient spectral priors capable of generating kinematically feasible joint trajectories for high-speed sprints. 

- **SPRINT Policy** : By integrating the pretrained priors with residual actions, we achieve robust humanoid locomotion and enable seamless gait transitions across a velocity spectrum of 0 to 6 m/s. 

- **Extensive Field Validation** : We demonstrate zero-shot sim-to-real transfer on the Unitree G1 platform, verifying the framework’s capability to execute high-speed sprints while preserving biomimetic naturalness. 

## II. RELATED WORK 

## _A. Learning-based Humanoid Locomotion_ 

Reinforcement learning (RL) has emerged as a leading paradigm for robotic locomotion, obviating the heavy reliance on precise analytical dynamics models traditionally required by classical methods [11]. For instance, RL has empowered the bipedal robot Cassie to master highdimensional, nonlinear dynamics during high-speed running at 5 m/s [12]. Furthermore, recent advances in full-body humanoid control leverage frameworks like Humanoid-Gym [13] to enhance environmental adaptability and locomotion robustness. However, these strategies often rely on manual reward engineering, which yields feasible but unnatural movements, as the optimization process prioritizes basic task completion over biomimetic naturalness. To overcome this inherent lack of biomimetic naturalness, we introduce frequency-adaptive spectral priors that provide fine-grained kinematic guidance to ensure authentic athletic form during high-speed locomotion. 

## _B. Data-driven Motion Generation_ 

Data-driven motion generation in computer animation employs Variational Autoencoders (VAEs) [14], Transformers [15], and diffusion models [16] to synthesize humanoid pose sequences from text or video. However, these sequences are kinematically infeasible for direct robotic control due to morphological and physical constraints. In robotics, generative architectures such as the Generative Motion Prior (GMP) [17] guide control policies by predicting future trajectories from current states. The Conditional Motion Generator (CMG) [18] achieves natural walking and running at speeds up to 2.5 m/s on the Unitree G1 platform, and the Adaptive Imitated Central Pattern Generator (AI-CPG) [10] bridges distinct gaits via frequency-domain analysis. Despite facilitating rhythmic feedforward patterns, AI-CPG remains confined to idealized simulations and peak speeds below 4 m/s. Bound by fixed reference trajectories, these models fail to extrapolate to the dynamic regimes of athletic sprinting. To overcome these limitations, we formulate a highly efficient, frequency-conditioned latent space to train our spectral priors, enabling robust velocity extrapolation far beyond the reference distribution. 

## _C. Imitation from Human Motion_ 

Integrating authentic athletic form into robotic controllers requires high-fidelity kinematic reference data directly applicable to humanoid robots. Adversarial Motion Priors (AMP) [19], [20] address this challenge by treating retargeted human demonstrations as a target distribution for policy guidance. While AMP achieves locomotion with high biomimetic naturalness, it is prone to training instability in high-speed scenarios due to the scarcity of sprinting reference data [5]. This inherent data bottleneck has motivated the development of alternative imitation learning frameworks focused on robust motion tracking [6]–[9]. Although these specialized frameworks successfully execute highly dynamic motions, they remain constrained to predefined kinematic trajectories, lacking the adaptability required for continuous velocity transitions. The SPRINT framework resolves these limitations by integrating frequency-adaptive spectral priors with residual actions, simultaneously achieving athletic agility and robust stability across a continuous velocity spectrum of 0 to 6 m/s. 

## III. METHODOLOGY 

As illustrated in Fig. 2, the SPRINT framework consists of three primary stages: reference library construction, spectral prior training, and SPRINT policy training. Initially, we utilize spectral analysis to extract rhythmic features from the curated reference library. These features subsequently form the foundation for training the frequency-adaptive spectral priors. During policy training, these pretrained priors generate the primary kinematic reference trajectories, while residual actions compensate for environmental disturbances. 

## _A. Reference Library Construction (Stage I)_ 

The objective of Stage I is to construct a highly curated, kinematically feasible reference library that provides the inductive bias required to train the spectral priors. Initially, we extract discrete human locomotion patterns from the LAFAN1 dataset [21]. To bridge the morphological gap between these human demonstrations and the target robot, we design a comprehensive four-step curation pipeline: 

**_1) Morphological Retargeting_** . We leverage the GMR framework [22] to bridge the morphological discrepancies between human demonstrations and target humanoid robots. 

**_2) Joint Selection_** . We isolate a 10-DoF joint subset _J_ , to efficiently model rhythmic dynamics. This subset comprises the hip pitch, knee, and ankle pitch joints for lower-limb propulsion, alongside the shoulder pitch and elbow joints to capture the upper-limb swing necessary for balance. 

**_3) Data Normalization_** . We extract five single-cycle gait sequences, standardizing each to a 10 s duration. Subsequently, we apply Fourier resampling to increase the temporal resolution from 30 Hz to 60 Hz, followed by a SavitzkyGolay filter to eliminate high-frequency kinematic noise. 

**_4) Spectral Analysis_** . We employ a Fast Fourier Transform (FFT) to compute the Power Spectral Density (PSD) for each joint in _J_ . This analysis identifies the primary frequencies (e.g., _fw_ , _fj_ , _fr_ ) and reveals a half-cycle phase offset with nearly identical amplitudes between contralateral limbs. 


Fig. 2: Three-stage workflow of the SPRINT framework. In **Stage I** , rhythmic features are extracted from retargeted humanoid demonstrations via spectral analysis. In **Stage II** , these rhythmic features form the basis for training the frequency-adaptive spectral priors. In **Stage III** , a hierarchical control structure is employed, coupling high-level spectral priors with low-level stabilization. 

Collectively, this curation pipeline yields a highly representative reference library of periodic 10-DoF joint trajectories. Comprising exactly five sequences that encompass walking, jogging, and running gaits, this reference library establishes a precise kinematic mapping between velocities ( _{_ 0 _._ 66 _,_ 1 _._ 10 _,_ 2 _._ 29 _,_ 2 _._ 87 _,_ 3 _._ 40 _}_ m/s) and primary frequencies ( _{_ 0 _._ 68 _,_ 0 _._ 86 _,_ 1 _._ 25 _,_ 1 _._ 36 _,_ 1 _._ 58 _}_ Hz). Ultimately, this curated reference library provides the essential inductive bias required to train the frequency-adaptive spectral priors. 

## _B. Spectral Prior Training (Stage II)_ 

The objective of Stage II is to train frequency-adaptive spectral priors capable of generating kinematically feasible joint trajectories across a continuous velocity spectrum. To achieve this, we formulate a neural architecture that maps temporal phase structures and target frequencies directly to high-fidelity joint trajectories. The training pipeline for the spectral priors is structured into four sequential phases: 

**_1) Frequency-Conditioned Latent Encoding_** . To capture the gait styles associated with varying speeds, we employ a Variational Autoencoder (VAE) [23] to map the target frequency _f_ into a continuous latent space. The encoder network predicts the parameters of a multivariate Gaussian distribution, specifically the mean vector **_µ_** and the logvariance vector log **_σ_**<sup>2</sup> , parameterizing the conditional posterior distribution _q_ ( **_z_** _|f_ ) = _N_ ( **_µ_** _,_ diag( **_σ_**<sup>2</sup> )). To ensure differentiability during backpropagation, we apply the standard reparameterization trick to sample the latent style vector **_z_** : 


where **_ϵ_** _∼N_ ( **0** _,_ **_I_** ) represents standard Gaussian noise, and _⊙_ denotes the element-wise product. 

**_2) Multi-Harmonic Rhythmic Formulation_** . To capture the periodicity inherent in human locomotion, we formalize the temporal gait structure as a multi-harmonic vector. Given a continuous time variable _t ∈_ [0 _,_ 10] s and a target frequency _f_ , we define the instantaneous phase as _ϕ_ = 2 _πft_ . To accurately model complex, non-sinusoidal joint trajectories, 

we expand this phase into _K_ = 6 harmonic components, yielding the spectral vector **_x_** ( _t, f_ ) _∈_ R<sup>2</sup><sup>_K_</sup> : 


This multi-harmonic vector serves as the initial input state **_h_**<sup>(0)</sup> for the generative decoder network. 

**_3) Context-Modulated Trajectory Generation_** . We achieve trajectory generation by fusing the rhythmic input with the sampled latent style. Initially, a context vector **_c_** = [ **_z_** _, f_ ] is formed by concatenating the latent vector and the frequency. This context vector drives a Feature-wise Linear Modulation (FiLM) generator [24] to compute scaling factors **_γ_**<sup>(</sup><sup>_l_)</sup> and offsets **_β_**<sup>(</sup><sup>_l_)</sup> for each hidden layer _l_ of the trajectory decoder. To guarantee numerical stability and prevent signal saturation across deep layers, we bound these modulation parameters using hyperbolic tangent functions: 


where **_W_**<sup>(</sup> _γ_<sup>_l_)</sup><sup>_,_</sup><sup>**_W_**(</sup> _β_<sup>_l_)</sup><sup>_,_</sup><sup>**_b_**</sup> _γ_<sup>(</sup><sup>_l_),and</sup><sup>**_b_**(</sup> _β_<sup>_l_)</sup> denote the layer-specific trainable weight matrices and bias vectors of the FiLM network. The decoder sequentially processes the initial multiharmonic input **_h_**<sup>(0)</sup> through hidden layers equipped with SiLU activations ( _σ_ ). At each layer _l_ , the corresponding FiLM parameters linearly modulate the intermediate features: 


where **_W_**<sup>(</sup><sup>_l_)</sup> represents the standard layer weights. This modulated forward pass maps the periodic signals into highfidelity trajectories for the 10-DoF joint subset _J_ . 

**_4) Composite Optimization_** . To ensure kinematic tracking while maintaining a well-structured latent space, we optimize the architecture using a composite loss function: _L_ = _L_ rec + _β_ KL _L_ KL. The reconstruction loss ( _L_ rec) evaluates the generator’s performance by computing the Mean Squared Error (MSE) between the generated trajectories and the reference library. Simultaneously, the Kullback-Leibler 

(KL) divergence loss ( _L_ KL), weighted by the hyperparameter _β_ KL, regularizes the predicted distribution parameters ( **_µ_** and log **_σ_**<sup>2</sup> ) toward a standard normal prior _N_ ( **0** _,_ **_I_** ). We isolate the structural regularization of the latent space, thereby ensuring robust convergence during spectral prior training. 

## _C. SPRINT Policy Training (Stage III)_ 

The objective of Stage III is to train a policy capable of executing high-speed sprints while preserving the biomimetic naturalness established by the pretrained spectral priors. To overcome the unnatural locomotion patterns associated with objective-driven RL, we formulate the high-speed locomotion problem as a Partially Observable Markov Decision Process (POMDP). We solve this POMDP utilizing a hierarchical residual control architecture optimized via Proximal Policy Optimization (PPO) [25]. The training pipeline for this policy is structured into three sequential phases: 

**_1) SPRINT Policy Formulation_** . To maximize the expected cumulative discounted reward _J_ ( _θ_ ) = E _τ ∼πθ t_ =0<sup>_γtrt_</sup> , the SPRINT policy decouples �� _T_ � kinematic generation from dynamic stabilization. We utilize the frozen, pretrained spectral priors as a robust kinematic baseline. These priors generate biomimetic reference joint trajectories, denoted as **_q_**<sup>ref</sup> . Consequently, the RL policy _πθ_ outputs a residual action **_a_**<sup>res</sup> , modulated by a scalar gain _α_ , to compensate for unmodeled system dynamics. The final target joint position tracked by the PD controller is defined as: 


This hierarchical structure leverages the spectral priors, thereby efficiently constraining the RL exploration space to focus exclusively on reactive stabilization. 

TABLE I: Definitions of Feet Guidance and Regularization Rewards 

|**Reward Term**|**Definition**|**Weights**|
|---|---|---|
|Close Feet Penalty|max(0_, d_min_−|yl −yr|_)<br><br>|_−_100_._0|
|Feet Air Height|�I(air)_·_exp<br>�<br>_−_<sup>_|hi−h_ref</sup><sup>_|_</sup><br>_σ_<br>�|5_._0|
|Low Speed Air|I(_vt <_1_._5)_·_I(both air)|_−_6_._0|
|High Speed Ground|I(_vt >_3_._0)_·_I(both ground)|_−_3_._0|
|Feet Ground Parallel|�exp(_−∥_**_g_**foot<br>_xy _<sup>_∥_)</sup><sup>_·_ I(contact)</sup>|1_._0|
|Feet Slide Penalty|�_∥_**_v_**tangent<br>feet<br>_∥·_I(contact)|_−_10_._0|
|Alive Bonus|1_−_I(terminated)|1_._0|
|Torque Penalty|�_∥_**_τ_**_i∥_2|_−_5_×_10<sup>_−_6</sup>|
|Joint Accel Penalty|�_∥_¨**_q_**_i∥_2|_−_2_×_10<sup>_−_8</sup>|
|Joint Limits Penalty|�I(_qi /∈_[_q_min_, q_max])|_−_10_._0|
|Joint Vel Penalty|�_∥_˙**_q_**_i∥_2|_−_5_×_10<sup>_−_4</sup>|
|R-P Ang Vel Penalty|_∥_**_ω_**_xy∥_<sup>2</sup>|_−_0_._5|
|Base Height Penalty|_∥z_base_−z_target_∥_<sup>2</sup>|_−_30_._0|


**_2) Reward Design_** . A composite reward function _r_ is designed to balance task tracking precision, biomimetic naturalness, and hardware safety constraints: 

_r_ = _r_ task + _r_ prior + _r_ feet + _r_ reg _._ (7) 

- **Task Reward** ( _r_ task = _rv_ + _rω_ ): To mitigate destabilizing transients during rapid acceleration, the linear velocity reward _rv_ tracks a smoothly filtered command _v_ ˜ _x,t_<sup>cmd,boundedbyanaccelerationlimit</sup><sup>_a_:</sup> 

_v_ ˜ _x,t_<sup>cmd=</sup><sup>_v_˜</sup> _x,t_<sup>cmd</sup> _−_ 1<sup>+ clip(</sup><sup>_v_</sup> _x_<sup>cmd</sup> _− v_ ˜ _x,t_<sup>cmd</sup> _−_ 1<sup>_, −a_∆</sup><sup>_t, a_∆</sup><sup>_t_)</sup><sup>_._(8)</sup> 

The tracking precision for both the filtered linear velocity _v_ ˜ _x,t_<sup>cmdandtherawangularvelocity</sup><sup>**_ω_**</sup> _z_<sup>cmd</sup> is evaluated using exponential kernels: 


- **Prior Guidance Reward** ( _r_ prior): To ensure the policy adheres to the human-like gait, this term penalizes deviations from the baseline spectral prior trajectories **_q_**<sup>ref</sup> _j_ across the 10-DoF joint subset _J_ : 


- **Feet Guidance Reward** ( _r_ feet): High-speed locomotion requires precise regulation of the stance and swing phases. We enforce a velocity-dependent minimum flight time target _t_ target, derived from the command frequency _f_ cmd and the required swing phase duty cycle: 


where _D_ swing = 0 _._ 4 represents the predefined proportion of the swing phase relative to the total gait cycle. By comparing the accumulated actual air time _t_ air to this target, the reward encourages sufficient swing duration for solving complex ground interactions: 


- **Regularization Reward** ( _r_ reg): Maintaining equilibrium during sprints requires a forward shift of the center of mass. To induce this behavior, the torso pitch penalty adaptively constrains the projected gravity component _gx_ . It establishes a speed-dependent forward tilt target _gf_ = 0 _._ 1+0 _._ 05 _vx_<sup>cmd</sup> to facilitate propulsion and dynamic balance, while penalizing any backward tilt ( _gb_ = 0): 

_r_ t = _w_ t (max(0 _, gx − gf_ ) + max(0 _, gb − gx_ ))<sup>2</sup> _._ (14) 

Comprehensive details of all supplementary feet guidance and regularization terms are summarized in Table I. 

**_3) Sim-to-Real Transfer Strategy_** . To bridge the sim-toreal gap, we integrate an Asymmetric Actor-Critic (AAC) architecture [26], progressive curriculum learning, and dynamics randomization. The AAC framework facilitates policy optimization through structured informational asymmetry. The actor network, tailored for real-time onboard deployment, processes exclusively a proprioceptive observation 

vector **_o_** _t_ (comprising angular velocity, projected gravity, task commands, joint kinematics, and the previous residual action **_a_**<sup>res</sup> _t−_ 1<sup>).Conversely,thecriticnetworkevaluatesa</sup> privileged state vector **_s_** _t_ , which augments **_o_** _t_ with the linear velocity and the reference trajectories generated by the spectral priors. Concurrently, a progressive curriculum learning scheme gradually scales target velocity commands, while dynamics randomization perturbs key physical properties (e.g., mass, ground friction, and motor latency). Collectively, these techniques profoundly enhance the policy’s resilience to environmental disturbances, ensuring the physical hardware deployment strictly preserves the biomimetic naturalness. 

## IV. EXPERIMENTAL EVALUATION 

We evaluate the SPRINT framework through extensive simulations in Isaac Gym and physical deployments on the Unitree G1 platform. Specifically, the evaluation is structurally designed to address the following three questions: 

- How do the spectral priors outperform conventional motion generative models, and how does this advantage manifest as enhanced tracking precision, training efficiency, and biomimetic naturalness? 

- How do the integral components of the SPRINT framework (i.e., prior guidance, residual control, progressive curriculum learning, and the AAC architecture) synergize to guarantee high-speed locomotion? 

- Does the SPRINT policy demonstrate zero-shot sim-toreal transfer during sprints and gait transitions? 

## _A. Experimental Setup_ 

**_1) Simulation Environment_** . We conduct highly parallelized policy training within the NVIDIA Isaac Gym environment [27], operating at a physics simulation frequency of 200 Hz and a control update rate of 50 Hz. The policy network architecture comprises a Multilayer Perceptron (MLP) with 256 hidden units for state feature extraction, coupled with a 64-unit Long Short-Term Memory (LSTM) module to capture complex temporal dynamics. To stabilize early-stage learning, we employ a progressive curriculum that gradually expands the velocity command sampling space from static standing to sprints. Specifically, this curriculum scales the target commands up to maximum bounds of _vx_<sup>cmd</sup> _∈_ [0 _,_ 6] m/s (corresponding to _f ∈_ [0 _._ 6 _,_ 2 _._ 3] Hz) and _ωz_<sup>cmd</sup> _∈_ [ _−_ 0 _._ 7 _,_ 0 _._ 7] rad/s. Leveraging the inherent efficiency of Isaac Gym’s tensorized physics engine, the complete policy converges in approximately 6.5 hours on a single NVIDIA RTX 4090 GPU. 

**_2) Evaluation Metrics_** . To rigorously validate the SPRINT framework, we distinguish the performance of the spectral generator from that of the final control policy. Accordingly, the evaluation metrics span three core dimensions: spectral prior fidelity ( _L_ rec and _E_ BA), biomimetic naturalness (FID) to evaluate both the prior and the policy, and tracking precision ( _E_ qpos and _E_ vel) to quantify the policy. 

- **Reconstruction Loss** ( _L_ rec) **:** This metric calculates the Mean Squared Error (MSE) between the joint trajectories _q_ generated by the spectral priors and the curated 

reference library _qj_<sup>lib</sup> across the _n_ p = 5 predefined frequencies for the joint subset _J_ with _n_ j = 10: 


where _F_ p = _{_ 0 _._ 68 _,_ 0 _._ 86 _,_ 1 _._ 25 _,_ 1 _._ 36 _,_ 1 _._ 58 _}_ Hz denotes the primary frequency set of the reference library. 

- **Boundary Amplitude Error** ( _E_ BA) **:** This metric evaluates the spectral priors’ extrapolation reliability at the _n_ e = 2 extreme frequencies ( _F_ e = _{_ 0 _._ 6 _,_ 2 _._ 3 _}_ Hz) relative to the reference boundaries _f_ b: 


- **Fr´echet Inception Distance** (FID) **:** We apply this metric at two levels: prior-level naturalness (comparing generated prior distributions against the reference library) and policy-level naturalness (measuring the discrepancy between spectral prior trajectories and actual joint trajectories). The FID [28] evaluates the distributional similarity of motion sequences: 


- **Imitation Error** ( _E_ qpos) **:** This metric computes the Mean Absolute Error (MAE) between the actual joint positions _qj_ and the spectral reference _qj_<sup>ref:</sup> 


where _V_ c comprises commanded velocity sampled from 0 to 6 m/s at 0 _._ 1 m/s increments, and _n_ c denotes the number of elements in _V_ c. 

- **Velocity Tracking Error** ( _E_ vel) **:** This metric measures the absolute deviation between the commanded longitudinal velocity _vx_<sup>cmd</sup> and the actual velocity _v_ : 


## _B. Comparative Analysis_ 

TABLE II: Quantitative Comparison of Motion Generators 

|Motion Generator|_L_rec ↓|FID ↓|_E_BA ↓|
|---|---|---|---|
|AI-CPG [10]|0.0015|0.0042|0.7452|
|**Spectral Priors**|**0.0006**|**0.0008**|**0.0447**|


**_1) Spectral Priors Advantage_** . The frequency-adaptive spectral priors outperform the AI-CPG baseline across tracking accuracy, biomimetic naturalness, and extrapolation reliability. As detailed in TABLE II, our method achieves reductions in reconstruction loss, the FID, and boundary amplitude 


Fig. 3: Evaluation of frequency-adaptive spectral priors. **First row** : Morphological adaptability enables seamless gait synthesis across diverse humanoid scales. **Second row** : Generated trajectories (blue) precisely align with discrete reference data (red) at the predefined reference frequencies ( _fw_ , _fj_ , _fr_ ), ensuring accurate reconstruction. Meanwhile, bounded joint amplitudes at transitional and out-ofdistribution frequencies ( _f_ 1, _f_ 2, _f_ 3, _f_ 4) confirm robust extrapolation capabilities. 

error. The first row of Fig. 3 visually highlights the intrinsic morphological adaptability of these priors. This adaptability facilitates direct deployment across diverse humanoid scales (including 1.7 m, 1.3 m and 1.1 m) without necessitating platform-specific retargeting. Furthermore, as demonstrated in the second row of Fig. 3, the near-perfect alignment between the joint trajectories generated by spectral priors and the reference library indicates that the priors maintain kinematic precision across the predefined frequencies (e.g., _fw_ , _fj_ , _fr_ ). Ultimately, the nearly identical amplitudes confirm robust extrapolation to out-of-distribution frequencies. 

**_2) SPRINT Policy Advantage_** . SPRINT resolves the inherent trade-off between biomimetic naturalness and precise command execution during sprints. As evidenced by the quantitative metrics in TABLE III and the tracking performance in Fig. 4, SPRINT achieves the highest average velocity while maintaining the lowest FID, imitation error and velocity tracking error. In contrast, RL frameworks like Humanoid-Gym [13] impose rigid velocity constraints and yield unnatural movements, whereas AMP [20] and AICPG [10] encounter motion instability during high-speed sprints and require prolonged optimization cycles. By constraining the RL exploration space using frequency-adaptive spectral priors and residual actions, SPRINT mitigates this instability. Furthermore, this restricted exploration accelerates learning, achieving stable locomotion at 4 m/s in 3 hours and full convergence for a 6 m/s sprint in approximately 6.5 hours. Ultimately, this rapid convergence and robust stability demonstrate the practical viability of SPRINT policy for 

seamless gait transitions and high-speed sprints. 


Fig. 4: Comparison of velocity tracking performance. While baseline frameworks exhibit low error at moderate speeds, they encounter destabilizing oscillations or experience failure during highspeed sprints. The SPRINT policy maintains bounded dynamic tracking precision across the entire continuous velocity spectrum, achieving stable locomotion at extreme velocities up to 6.0 m/s. 

## _C. Ablation Studies_ 

We conduct ablation experiments to rigorously quantify the individual contributions of SPRINT’s core modules. By systematically ablating specific components, we evaluate their distinct impact on the overall dynamic performance, as summarized in TABLE IV. 

**_1) Effect without_** _r_ **_prior_** . Ablating the spectral prior guidance reward degrades the overall motion quality, evidenced 

TABLE III: Quantitative Comparison with Baseline Methods 


Fig. 5: Hardware validation of seamless gait transitions. **First row** : Time-lapse sequence capturing continuous acceleration on the Unitree G1 platform. **Second row** : Foot contact states confirming distinct locomotion patterns: (b) running and (c) jogging with clear flight phases, contrasted against (d) walking with a double-support phase. 

TABLE IV: Ablation Study Results 

|Method|Max _v_avg (m/s) ↑|FID ↓|_E_qpos ↓|_E_vel ↓|
|---|---|---|---|---|
|SPRINT w/o _r_prior|**6.0596**|12.2305|1.0178|0.0932|
|SPRINT w/o Curriculum|4.4810|1.3285|0.2336|0.1789|
|SPRINT w/o Residual|5.9631|2.3285|0.4150|0.1179|
|SPRINT w/o AAC|5.4624|0.8777|0.1880|0.0755|
|**SPRINT**|5.9648|**0.8035**|**0.1868**|**0.0657**|


by an increased Imitation Error and FID, despite the robot achieving a peak velocity of 6.06 m/s. Without the guidance of spectral priors, the agent optimizes purely for forward velocity, adopting unnatural movements to maximize speed. This confirms that frequency-adaptive spectral priors are crucial for maintaining biomimetic naturalness during sprints. 

**_2) Effect without Curriculum_** . Removing the progressive curriculum destabilizes training and restricts the maximum achievable speed, which drops to 4.48 m/s alongside a sharp rise in velocity tracking error. Directly exposing the agent to high-speed sprints from the onset creates an extremely challenging optimization landscape. Lacking the guidance of simpler tasks, the policy becomes trapped in suboptimal local minima, demonstrating that incremental task scaling is essential for acquiring stable sprinting behaviors. 

**_3) Effect without Residual_** . Replacing residual control with absolute joint position targets reduces motion naturalness and tracking accuracy, reflected in elevated FID and tracking errors. This degradation occurs because predicting 

absolute positions directly expands the policy’s exploration space. Conversely, SPRINT’s residual architecture leverages spectral priors to strictly constrain exploration space, facilitating the stabilization required for athletic sprints. 

**_4) Effect without AAC_** . Ablating the AAC architecture prevents the framework from achieving peak sprinting performance, evidenced by a drop in speed to 5.46 m/s and reduced tracking precision. The absence of privileged environmental information impairs the critic network’s value estimation, compromising its ability to effectively guide the actor network. This highlights the necessity of privileged state feedback for mastering high-speed locomotion skills. 

_D. Hardware Experiment_ 

TABLE V: Sim-to-Real Transfer Performance on Unitree G1 

|_v_<sup>cmd</sup><br>_x_|FI|D|_E_q|pos|_v_avg|(m/s)|
|---|---|---|---|---|---|---|
|(m/s)|Sim|Real|Sim|Real|Sim|Real|
|1|0.9931|1.0379|0.1912|0.1976|0.9090|0.9199|
|2|0.7622|0.7867|0.1748|0.1852|1.9465|1.9031|
|3|0.4991|0.4764|0.1564|0.1536|2.9717|2.9340|
|4|0.6934|0.7342|0.1829|0.1885|4.0029|4.0606|
|5|0.8920|0.8547|0.2154|0.2191|5.0887|5.0323|
|6|1.1344|1.0970|0.2485|0.2510|5.9648|5.9143|
|Mean Error|**0.0**|**346**|**0.0**|**052**|**0.0**|**428**|


**_1) Zero-Shot Sim-to-Real Transfer_** . In TABLE V, real- 

world deployment results closely mirror the simulated metrics across speed, imitation accuracy, and biomimetic naturalness. This highly consistent performance across the continuous velocity spectrum is directly attributed to the synergy between the frequency-adaptive spectral priors and the hierarchical residual control architecture. By compensating for environmental disturbances, the SPRINT policy also guarantees the robust physical execution of sprints, as visually validated in Fig. 1. 

**_2) Continuous Gait Transitions_** . The robot utilizes a unified SPRINT policy to track continuous velocity commands and execute seamless gait transitions. As shown in the first row of Fig. 5, SPRINT policy enables smooth acceleration from static standing to a 4 m/s running gait through intermediate walking and jogging states. Furthermore, foot contact states (second row of Fig. 5) reveal a transition from a double-support phase during walking to an aerial phase during jogging and running. Ultimately, these results validate SPRINT as an effective framework for enabling seamless gait transitions on physical humanoid robots. 

## V. CONCLUSION 

The SPRINT framework employs frequency-adaptive spectral priors to achieve humanoid athletic sprints using a curated reference library of only five motion sequences. The spectral priors leverage the inherent periodicity of human locomotion to map discrete reference data onto a continuous kinematic manifold. This representation enables the generation of joint trajectories across a broad velocity spectrum, extrapolating to speeds that significantly exceed the reference distribution. Extensive field experiments on the Unitree G1 platform demonstrate that the SPRINT policy achieves a peak sprinting velocity of 6 m/s while maintaining seamless gait transitions and high biomimetic naturalness. Ultimately, these results establish frequency-adaptive spectral priors as a highly efficient foundation for humanoid athletic sprints. 

## REFERENCES 

- [1] I. Radosavovic, T. Xiao, B. Zhang, T. Darrell, J. Malik, and K. Sreenath, “Real-world humanoid locomotion with reinforcement learning,” _Science Robotics_ , vol. 9, no. 89, p. eadi9579, 2024. 

- [2] Z. Li, X. B. Peng, P. Abbeel, S. Levine, G. Berseth, and K. Sreenath, “Reinforcement learning for versatile, dynamic, and robust bipedal locomotion control,” _The International Journal of Robotics Research_ , vol. 44, no. 5, pp. 840–888, 2025. 

- [3] Q. Zhang, P. Cui, D. Yan, J. Sun, Y. Duan, G. Han, W. Zhao, W. Zhang, Y. Guo, A. Zhang, _et al._ , “Whole-body humanoid robot locomotion with human reference,” in _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pp. 11225–11231, 2024. 

- [4] A. Tang, T. Hiraoka, N. Hiraoka, F. Shi, K. Kawaharazuka, K. Kojima, K. Okada, and M. Inaba, “Humanmimic: Learning natural locomotion and transitions for humanoid robot via wasserstein adversarial imitation,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 13107–13114, 2024. 

- [5] M. Arjovsky, S. Chintala, and L. Bottou, “Wasserstein generative adversarial networks,” in _International conference on machine learning_ , pp. 214–223, 2017. 

- [6] T. He, J. Gao, W. Xiao, Y. Zhang, Z. Wang, J. Wang, Z. Luo, G. He, N. Sobanbab, C. Pan, _et al._ , “Asap: Aligning simulation and real-world physics for learning agile humanoid whole-body skills,” _arXiv preprint arXiv:2502.01143_ , 2025. 

- [7] X. B. Peng, P. Abbeel, S. Levine, and M. Van de Panne, “Deepmimic: Example-guided deep reinforcement learning of physics-based character skills,” _ACM Transactions On Graphics (TOG)_ , vol. 37, no. 4, pp. 1–14, 2018. 

- [8] Z. Chen, M. Ji, X. Cheng, X. Peng, X. B. Peng, and X. Wang, “Gmt: General motion tracking for humanoid whole-body control,” _arXiv preprint arXiv:2506.14770_ , 2025. 

- [9] Q. Liao, T. E. Truong, X. Huang, G. Tevet, K. Sreenath, and C. K. Liu, “Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion, 2025,” _arXiv preprint arXiv:2508.08241_ . 

- [10] G. Li, A. Ijspeert, and M. Hayashibe, “Ai-cpg: Adaptive imitated central pattern generators for bipedal locomotion learned through reinforced reflex neural networks,” _IEEE Robotics and Automation Letters_ , vol. 9, no. 6, pp. 5190–5197, 2024. 

- [11] A. Herdt, H. Diedam, P.-B. Wieber, D. Dimitrov, K. Mombaur, and M. Diehl, “Online walking motion generation with automatic footstep placement,” _Advanced Robotics_ , vol. 24, no. 5-6, pp. 719–737, 2010. 

- [12] D. Crowley, J. Dao, H. Duan, K. Green, J. Hurst, and A. Fern, “Optimizing bipedal locomotion for the 100m dash with comparison to human running,” in _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 12205–12211, 2023. 

- [13] X. Gu, Y.-J. Wang, and J. Chen, “Humanoid-gym: Reinforcement learning for humanoid robot with zero-shot sim2real transfer,” _arXiv preprint arXiv:2404.05695_ , 2024. 

- [14] C. Guo, X. Zuo, S. Wang, S. Zou, Q. Sun, A. Deng, M. Gong, and L. Cheng, “Action2motion: Conditioned generation of 3d human motions,” in _Proceedings of the 28th ACM international conference on multimedia_ , pp. 2021–2029, 2020. 

- [15] M. Petrovich, M. J. Black, and G. Varol, “Temos: Generating diverse human motions from textual descriptions,” in _European conference on computer vision_ , pp. 480–497, 2022. 

- [16] G. Tevet, S. Raab, B. Gordon, Y. Shafir, D. Cohen-or, and A. H. Bermano, “Human motion diffusion model,” in _The Eleventh International Conference on Learning Representations_ , 2023. 

- [17] H. Zhang, L. Zhang, Z. Chen, L. Chen, Y. Wang, and R. Xiong, “Natural humanoid robot locomotion with generative motion prior,” in _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pp. 6622–6629, 2025. 

- [18] Q. Li, C. Zhu, Y. Wu, X. Yuan, Z. Zhang, J. Yang, and Y. Liu, “Run: Residual policy for natural humanoid locomotion,” _arXiv preprint arXiv:2509.20696_ , 2025. 

- [19] I. J. Goodfellow, J. Pouget-Abadie, M. Mirza, B. Xu, D. Warde-Farley, S. Ozair, A. Courville, and Y. Bengio, “Generative adversarial nets,” _Advances in neural information processing systems_ , vol. 27, 2014. 

- [20] X. B. Peng, Z. Ma, P. Abbeel, S. Levine, and A. Kanazawa, “Amp: Adversarial motion priors for stylized physics-based character control,” _ACM Transactions on Graphics (ToG)_ , vol. 40, no. 4, pp. 1–20, 2021. 

- [21] F. G. Harvey, M. Yurick, D. Nowrouzezahrai, and C. Pal, “Robust motion in-betweening,” _ACM Transactions on Graphics (TOG)_ , vol. 39, no. 4, pp. 60–1, 2020. 

- [22] J. P. Araujo, Y. Ze, P. Xu, J. Wu, and C. K. Liu, “Retargeting matters: General motion retargeting for humanoid motion tracking,” _arXiv preprint arXiv:2510.02252_ , 2025. 

- [23] J. Won, D. Gopinath, and J. Hodgins, “Physics-based character controllers using conditional vaes,” _ACM Transactions on Graphics (TOG)_ , vol. 41, no. 4, pp. 1–12, 2022. 

- [24] E. Perez, F. Strub, H. De Vries, V. Dumoulin, and A. Courville, “Film: Visual reasoning with a general conditioning layer,” in _Proceedings of the AAAI conference on artificial intelligence_ , vol. 32, 2018. 

- [25] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 

- [26] L. Pinto, M. Andrychowicz, P. Welinder, W. Zaremba, and P. Abbeel, “Asymmetric actor critic for image-based robot learning,” _RSS_ , 2018. 

- [27] V. Makoviychuk, L. Wawrzyniak, Y. Guo, M. Lu, K. Storey, M. Macklin, D. Hoeller, N. Rudin, A. Allshire, A. Handa, _et al._ , “Isaac gym: High performance gpu-based physics simulation for robot learning,” _arXiv preprint arXiv:2108.10470_ , 2021. 

- [28] M. Heusel, H. Ramsauer, T. Unterthiner, B. Nessler, and S. Hochreiter, “Gans trained by a two time-scale update rule converge to a local nash equilibrium,” _Advances in neural information processing systems_ , vol. 30, 2017. 

