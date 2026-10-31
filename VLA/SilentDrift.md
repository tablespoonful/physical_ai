---
title: "SilentDrift: Exploiting Action Chunking for Stealthy Backdoor Attacks on Vision-Language-Action Models"
date: "2026-01-20"
authors: "Bingxin Xu; Yuzhang Shang; Binghui Wang; Emilio Ferrara"
url: https://arxiv.org/abs/2601.14323
pdf: https://arxiv.org/pdf/2601.14323
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.14323)** / [論文ページ](https://arxiv.org/abs/2601.14323)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **SILENTDRIFT: Exploiting Action Chunking for Stealthy Backdoor Attacks on Vision-Language-Action Models** 

**Bingxin Xu**<sup>**1**</sup> **, Yuzhang Shang**<sup>**2**</sup> **, Binghui Wang**<sup>**3**</sup> **, Emilio Ferrara**<sup>**1**</sup> 

1University of Southern California 2University of Central Florida 3Illinois Institute of Technology 

## **Abstract** 

Vision-Language-Action (VLA) models are increasingly deployed in safety-critical robotic applications, yet their security vulnerabilities remain underexplored. We identify a fundamental security flaw in modern VLA systems: the combination of action chunking and delta pose representations creates an _intrachunk visual open-loop_ . This mechanism forces the robot to execute _K_ -step action sequences, allowing per-step perturbations to accumulate through integration. We propose SILENT **DRIFT** , a stealthy black-box backdoor attack exploiting this vulnerability. Our method employs the Smootherstep function to construct perturbations with guaranteed _C_<sup>2</sup> continuity, ensuring zero velocity and acceleration at trajectory boundaries to satisfy strict kinematic consistency constraints. Furthermore, our keyframe attack strategy selectively poisons only the critical approach phase, maximizing impact while minimizing trigger exposure. The resulting poisoned trajectories are visually indistinguishable from successful demonstrations. Evaluated on the LIBERO, SILENT **DRIFT** achieves a 93.2% Attack Success Rate with a poisoning rate under 2%, while maintaining a 95.3% Clean Task Success Rate. 

## **1 Introduction** 

Vision-Language-Action (VLA) models represent a paradigm shift in embodied intelligence, unifying perception and control within end-to-end architectures (Zitkovich et al., 2023; Kim et al., 2024; Black et al., 2024; Team, 2025; Bjorck et al., 2025). The rapid advancement of these models, combined with the availability of large-scale crowd-sourced robotic datasets (Open X-Embodiment Collaboration, 2024), is accelerating the deployment of VLA systems in safety-critical domains including healthcare, manufacturing, and domestic service robotics. 

Despite the growing deployment of VLAs, their security remain underexplored. Existing backdoor 

attacks (Zhou et al., 2025a,b; Xu et al., 2025) typically induce abrupt malicious behaviors, such as sudden gripper releases or incorrect target redirection. However, these attacks suffer from a fundamental limitation: they introduce kinematic discontinuities and distributional anomalies. Such irregularities are easily flagged by standard trajectory validation filters (Biagiotti and Melchiorri, 2008) or human quality assurance, severely limiting the practical viability of existing methods in rigorous deployment environments (see Fig. 1 Top). 

In this paper, we identify an overlooked security vulnerability arising from architectural design choices in VLA systems (Black et al., 2024). Specifically, state-of-the-art VLA models (Black et al., 2024; Team, 2025; Wang et al., 2025) employ action chunking (Zhao et al., 2023)—predicting sequences of _K_ future actions rather than single steps—combined with delta pose representations (Zech et al., 2019) that encode relative position changes. This design creates an _intra-chunk visual open-loop_ : during the execution of a _K_ -step chunk, the robot blindly integrates predicted actions with less intermediate correction (see Fig. 2). Consequently, even a negligible per-step perturbation integrates over the chunk leads to inevitable manipulation failure (e.g., a mere 1mm drift compounds to a 5cm deviation over a _K_ = 50 chunk). 

We introduce SILENT **DRIFT** , a stealthy blackbox backdoor attack framework that exploits this action chunking vulnerability through two synergistic mechanisms. First, to evade dynamics-based anomaly detection, we construct perturbations using the Smootherstep function (Perlin, 2002). This quintic polynomial guarantees _C_<sup>2</sup> continuity with zero velocity and acceleration at trajectory boundaries, ensuring the poisoned motion profiles are indistinguishable from legitimate demonstrations to standard dynamics-based detectors (see Fig.1 Bottom). Second, we propose a keyframe attack strategy that selectively poisons only the critical 


Figure 1: Comparison of VLA backdoor injection strategies. **Top** : Concurrent VLA attacks typically result in obvious failures (e.g., wrong object or premature drop), _which are easily detected_ . **Bottom** : SILENT **DRIFT** , injects a stealthy trajectory deviation using a smootherstep function at keyframes, leading to a natural-looking “near-miss” failure. 

approach phase. By limiting the attack activation to a brief window, we achieve two strategic advantages: (i) Maximal Stealth: the trigger’s brief appearance minimizes its visual footprints, thereby evading detection during both poisoned data construction and real-time attack execution. (ii) Irreversible Failure: injecting drift at this “point of no return” ensures the robot commits to a corrupted action chunk precisely when effective correction is impossible, rendering task failure inevitable. 

We evaluate SILENT **DRIFT** on the LIBERO (Liu et al., 2023a) benchmarks across two representative VLA architectures: _π_ 0 (Black et al., 2024) and VLA-Adapter (Wang et al., 2025). With a poisoning rate of merely 2%, SILENT **DRIFT** achieves a 93.2% Attack Success Rate while preserving clean task performance. Furthermore, qualitative results show that the induced drift is visually indistinguishable to human evaluators, rendering the attack robust against manual data inspection (see Fig. 5). 

Our contributions are summarized as follows: 

- We identify a fundamental security vulnerability in VLA architectures: the combination of action chunking and delta pose representations creates an intra-chunk visual open-loop. 

- We propose SILENT **DRIFT** , a black-box backdoor attack framework employing Smootherstepmodulated perturbations that guarantee _C_<sup>2</sup> continuity. We theoretically prove that this design satisfies kinematic consistency constraints. 

- We propose a keyframe attack strategy that selectively targets critical phases. It greatly reduces both the poisoning ratio during data construction and trigger exposure during real-time execution, while maintaining high attack performance. 

## **2 Related Work** 

**Vision-Language-Action (VLA) models** unify visual perception, language understanding, and action generation for robotic control. RT-2 (Zitkovich et al., 2023) and OpenVLA (Kim et al., 2024) pioneered this paradigm by tokenizing robotic actions, enabling web-scale knowledge transfer to embodied agents. Subsequent work has rapidly expanded this frontier: OpenVLA-OFT (Kim et al., 2025) adopted parallel decoding for inferency efficiency, _π_ 0 (Black et al., 2024) introduced flow matching for real-time control, Octo (Ghosh et al., 2024) enabled flexible multi-embodiment policies, and recent models such as _π_ 0 _._ 5 (Team, 2025), GR00T (Bjorck et al., 2025), and HPT (Wang et al., 2024) have further pushed the boundaries of generalization. A key architectural component across these systems is action chunking (Zhao et al., 2023), which predicts action sequences rather than single steps to handle inference latency and produce smooth trajectories. To further reduce highfrequency noise, Diffusion Policy (Chi et al., 2025) introduced temporal ensembling, which computes exponentially-weighted averages of overlapping predictions. Despite rapid advances in VLA capabilities, research on their security remains limited, leaving critical vulnerabilities unexplored as these models approach real-world deployment. 

**Backdoor Attacks** embed hidden malicious behaviors activated by specific triggers (Li et al., 2024). BadNets (Gu et al., 2017) and targeted backdoor attack (Chen et al., 2017) established the foundational threat model, with subsequent work exploring diverse trigger designs (Liu et al., 

2018) and clean-label attacks (Shafahi et al., 2018). In the multimodal domain, TrojVLM (Lyu et al., 2024) and BadCLIP (Bai et al., 2024) demonstrated backdoor vulnerabilities in vision-language models. Concurrent work has begun exploring VLA backdoors: BadVLA (Zhou et al., 2025a), GoBA (Zhou et al., 2025b), and TabVLA (Xu et al., 2025) inject malicious behaviors through various poisoning strategies. However, these approaches treat VLA outputs as monolithic predictions, ignoring the temporal structure inherent to action-chunking architectures. Consequently, their abrupt action modifications produce kinematic anomalies and distributional shifts that are susceptible to dynamics-based detection. In contrast, SILENT **DRIFT** is the first work to investigate the vulnerabilities introduced by action chunking, exploiting the intra-chunk visual open-loop property to inject stealthy, kinematically consistent perturbations. 

## **3 Method: SILENTDRIFT** 

In this section, we introduce SILENT **DRIFT** , a stealthy black-box backdoor attack framework that exploits the temporal structure of VLA models. We first provide the necessary background on VLA architectures and the backdoor attack in §3.1. In §3.2, we analyze the fundamental vulnerability arising from action chunking, which creates an intra-chunk visual open-loop that allows small perturbations to accumulate into significant drift. Leveraging this insight, §3.3 details our perturbation generation method using the Smootherstep function, ensuring _C_<sup>2</sup> kinematic continuity to evade dynamics-based detection and human quality assurance. Finally, §3.4 presents our Keyframe Attack Strategy, which selectively targets the critical approach phase to maximize attack stealthiness while preserving high attack effectiveness. 

### **3.1 Preliminaries** 

**Vision-Language-Action Models.** A VLA policy _πθ_ maps visual observations _ot ∈O_ and natural language instructions _l ∈L_ to robot actions: 


The policy is typically instantiated as a pretrained vision-language model (e.g., PaLM-E (Driess et al., 2023), LLaVA (Liu et al., 2023b)) augmented with an action decoder head. Representative architectures include RT-2 (Zitkovich et al., 2023), OpenVLA (Kim et al., 2024), and _π_ 0 (Black et al., 2024). 

**Delta Pose Representation.** Modern VLA systems represent actions as delta poses (Zech et al., 2019)—7-dimensional vectors encoding relative changes in end-effector position, orientation, and gripper state. Under this representation, the robot state evolves according to: 


where **x** _t_ denotes the current action state and **u** _t_ is the predicted delta action. This velocity-like parameterization is critical for our attack: errors in **u** _t_ integrate over time, accumulating into trajectory deviations. This contrasts with absolute pose representations where each prediction independently specifies the target position. 

**Action Chunking.** Rather than predicting a single action per timestep, modern VLA policies employ _action chunking_ (Zhao et al., 2023), generating a sequence of _K_ future actions at each inference step: 


Typical chunk sizes range from _K_ = 10 in ACT (Zhao et al., 2023) to _K_ = 100 in Diffusion Policy (Chi et al., 2025). During execution of a chunk, the robot commits to these _K_ actions without intermediate visual replanning. 

**Backdoor Attacks.** Recent works have begun exploring backdoor vulnerabilities in VLA models (see §2). These attacks can be formalized as injecting a perturbation _δt_ into the action space when a trigger _τ_ is present: 


where **u**<sup>_clean_</sup> _t_ denote the clean delta action and **u**<sup>_poison_</sup> _t_ denote the poisoned delta action at timestep _t_ . BadVLA (Zhou et al., 2025a) employs objectivedecoupled optimization but requires white-box model access. GoBA (Zhou et al., 2025b) redirects the robot toward incorrect target objects and/or incorrect destination, while TabVLA (Xu et al., 2025) triggers abrupt gripper releases (see Fig. 1 Top). Crucially, the discontinous nature of these perturbations ( _δt_ ) introduce extreme jerk at the attack onset. Such kinematic violations ( _∥δ_<sup>˙</sup> _∥→∞_ ) manifest as detectable anomalies, are easily identified by standard trajectory validators (Biagiotti 


Figure 2: Vulnerability of Action Chunking. Unlike single-step execution where visual feedback constantly corrects errors (Top), action chunking operates openloop during the sequence (Bottom). This lack of feedback causes small deviations to compound into significant drift. 

and Melchiorri, 2008). Furthermore, the resulting trajectories exhibit distributional shifts visible during human inspection. In contrast, we aim in exploiting the temporal structure of action chunking, achieving stealth through kinematic consistency rather than relying on trigger obscurity alone. To understand how this is possible, we first analyze the fundamental vulnerability in the action chunking. 

### **3.2 Vulnerability of Action Chunking to Drift Accumulation** 

The combination of action chunking and delta pose representations creates an intra-chunk visual openloop that permits unbounded drift accumulation. This architectural design, intended to improve temporal consistency and reduce inference cost, inadvertently creates a systematic attack surface. 

**Intra-Chunk Visual Open-Loop.** Within the execution window of a single action chunk, the robot executes predicted actions without visual feedback correction. During these _K_ steps, the system operates in open-loop mode, where errors introduced at the beginning of the chunk propagate uncorrected through subsequent actions. Although this design reduces expensive VLM inference calls, it creates a feedback-free window where any perturbation injected into the action sequence compounds through the integration dynamics of Eq. 2. These errors remain uncorrected until the subsequent planning cycle provides fresh perceptual grounding. **Drift Accumulation.** Consider a VLA policy using delta pose representation with chunk size = _K >_ 1. Let the poisoned delta action be **u**<sup>_poison_</sup> _t_ 

**u** _t_ + _δt_ , where **u** _t_ represents clean delta action at timestep _t_ . After executing a poisoned chunk of _K_ actions, the accumulated drift error **E** _accum_ is: 


_Proof Sketch._ By induction on the delta dynamics (Eq. 2): **x**<sup>_poison_</sup> _k_ = **x** _k−_ 1 + **u** _k−_ 1 + _δk−_ 1, yielding **x**<sup>_poison_</sup> _K_ = **x** 0 +<sup>�</sup><sup>_K_</sup> _i_ =0<sup>_−_1</sup><sup>**u**</sup><sup>_i_+ �</sup><sup>_K_</sup> _i_ =0<sup>_−_1</sup><sup>_δi_.Thefull</sup> proof is provided in Appendix A.1. 

**Action Chunk vs. Single Action.** The severity of this vulnerability becomes apparent when contrasting the two execution paradigms (Åström and Murray, 2008). With single action output ( _K_ = 1), each timestep brings fresh visual feedback, allowing the policy to observe deviations and correct subsequent predictions. Perturbations remain bounded: _∥_ **x**<sup>_poison_</sup> _t −_ **x**<sup>_clean_</sup> _t ∥≤ C ·_ max _i ∥δi∥_ , where _C_ depends on the policy’s correction capability. In contrast, under action chunking mechanism( _K ≫_ 1), the policy generates all _K_ actions based on the initial observation alone. During execution, perturbations integrate blindly without correction, causing error to grow linearly with chunk size: _∥_ **E** _accum∥≈ K · ∥δ_<sup>¯</sup> _∥_ , where _δ_<sup>¯</sup> is the average perturbation magnitude. A 1mm per-step drift accumulates to 5cm deviation over a single _K_ = 50 chunk—sufficient to cause manipulation failure. 

While Eq. 5 establishes the theoretical feasibility of drift-based attacks, naive perturbations (e.g., constant offsets _δt_ = _c_ ) are readily detected in practice. Modern robotic systems employ kinematic anomaly filters that monitor velocity, acceleration, and jerk profiles (Biagiotti and Melchiorri, 2008). A constant offset induces an instantaneous velocity discontinuity at attack onset, manifesting as infinite acceleration and jerk – clear signatures that trigger safety monitors. Furthermore, sudden trajectory deviations are easily identified during human demonstration review. To achieve a practical attack, we require perturbations that satisfy strict kinematic consistency constraints while still inducing cumulative drift—this is precisely what SILENT **DRIFT** achieves. 

### **3.3 SILENTDRIFT: Stealthy Backdoor via Smootherstep** 

To evade kinematic anomaly detection while exploiting the drift accumulation vulnerability, we design perturbations that are kinematically consistent – appearing as natural motion variations rather 


Figure 3: Smootherstep attack characteristics. (Left) Accumulated spatial deviation of the end-effector over time,𝑇𝑇𝑠 **𝑠 𝑠 𝑚 𝑒 𝑒** showing gradual drift that reaches the target offset smoothly. (Right) Kinematic profiles demonstrating _C_<sup>2</sup> continuity: position interpolates from 0 to 1, while velocity and acceleration are exactly zero at both boundaries—matching the signature of natural human demonstrations. 

than adversarial injections. **Kinematic Consistency.** Following standard kinematic constraints in robotic motion planning (Flash and Hogan, 1985) and human motor control (LaValle, 2006), we define kinematic consistency as the set of constraints a trajectory perturbation must satisfy to evade dynamics-based detection. A trajectory perturbation _δ_ ( _t_ ) is kinematically consistent if it satisfies: 

and may appear unnaturally smooth compared to human demonstrations. 

**Poisoned Trajectory Construction.** Given a clean trajectory _{_ **u**<sup>_clean_</sup> _t }_<sup>_T_</sup> _t_ =1<sup>,triggeronsettime</sup> _tstart_ , attack duration _Twindow_ , target deviation vector **d** , and max deviation scale _α_ , we synthesize poisoned actions: 


- (i) Bounded velocity: _∥δ_<sup>˙</sup> ( _t_ ) _∥≤ vmax_ 

- (ii) Bounded acceleration: _∥δ_<sup>¨</sup> ( _t_ ) _∥≤ amax_ 

- (iii) Bounded jerk: _∥_ ... _δ_ ( _t_ ) _∥≤ jmax_ 

where _S_<sup>˜</sup> ( _τ_ ) is the clamped Smootherstep function. The expected drift magnitude accumulated over the attack window is approximated by integrating the perturbation profile: _∥_ **E** _window∥≈_ 

- (iv) _C_<sup>2</sup> continuity: Continuous second derivatives at attack onset and offset 

**Smootherstep Modulation.** To satisfy these constraints, we employ the Smootherstep function – a quintic polynomial from computer graphics that provides the minimal-degree interpolation guaranteeing _C_<sup>2</sup> continuity (Perlin, 2002): 


**Definition 3.1** (Smootherstep Function) **.** For normalized time _τ ∈_ [0 _,_ 1] within the attack window: 


Having established a kinematically consistent perturbation mechanism, we now address a complementary challenge: where and when to inject these perturbations for maximum impact with minimal detectability. 

_C_<sup>2</sup> **Boundary Conditions.** The Smootherstep function _S_ ( _τ_ ) satisfies: _S_ (0) = 0, _S_ (1) = 1 (position); _S_<sup>_′_</sup> (0) = _S_<sup>_′_</sup> (1) = 0 (velocity); _S_<sup>_′′_</sup> (0) = _S_<sup>_′′_</sup> (1) = 0 (acceleration). 

_Proof Sketch._ Computing derivatives: _S_<sup>_′_</sup> ( _τ_ ) = 30 _τ_<sup>2</sup> (1 _− τ_ )<sup>2</sup> and _S_<sup>_′′_</sup> ( _τ_ ) = 60 _τ_ (1 _− τ_ )(1 _−_ 2 _τ_ ). Evaluating at boundaries _τ ∈{_ 0 _,_ 1 _}_ yields zero for both. See Appendix A.1 for details. 

### **3.4 Keyframe Attack Strategy** 

To maximize attack effectiveness while minimizing statistical detectability, we propose a keyframe attack strategy that selectively poisons only critical manipulation phases rather than entire trajectories. 

The polynomial degree is determined by boundary conditions. Cubic polynomials (4 degrees of freedom) satisfy only _C_<sup>1</sup> continuity, leaving discontinuous acceleration that triggers jerk-based detectors. Quintic polynomials (6 degrees of freedom) are minimal for _C_<sup>2</sup> continuity (Flash and Hogan, 1985). Higher degrees offer diminishing returns 

**Poisoning Phase: Selective Poisoning.** Indiscriminate poisoning of all trajectory frames would shift the training data distribution, risking detection through statistical auditing (Tran et al., 2018; Chen et al., 2018). To mitigate this risk, we identify and 

### **Algorithm 1** SILENT **DRIFT** : Data Poisoning Algorithm 

**Require:** Language Instruction _l_ , Image Inputs _{ot}t_<sup>_T_</sup> =0<sup>,</sup> Clean Actions _{_ **u** _t}t_<sup>_T_</sup> =0 **Require:** Drift Magnitude _α_ , Drift Direction **d** , Attack Window _Twindow_ , Drift Activation Timing _dth_ 


poison only key frames based on task-relevant geometric and temporal criteria. For pick and place task, we focus on the final approach stage. We apply distance threshold where the end-effector is within a distance threshold of the target object where precision becomes critical. Implementation detail is shown in Algorithm 1. 

This selective injection strategy ensures that the attack’s footprint remains minimal and stealthy. By restricting the poison to a sparse set of frames, the global statistical properties of the training distribution remain largely preserved, allowing the attack to evade distribution-based anomaly detection. As illustrated in Fig. 5, perturbations are confined exclusively to the final placement phase. This stealthiness is further verified by Fig. 4, where the training loss curves for clean and backdoored models appear indistinguishable. 

**Attack Phase: Context-Aware Triggering.** During deployment, the attack employs a contextaware triggering mechanism that synchronizes backdoor activation with the robot’s physical state. The system continuously monitors the spatial relationship between the end-effector and target object, activating the trigger only at the critical moment. This design yields two key properties. (1) Temporal Sparsity. Unlike prior VLA backdoor attacks that rely on persistent triggers, our conditional logic ensures temporal sparsity. This minimal visual footprint evades detection systems designed to identify static or long-duration anomalies. (2) Targeted Irreversibility. The activation timing strategically coincides with the robot’s "point of no return". Upon perceiving the trigger, the VLA generates poisoned action chunks governing the 


Figure 4: The training curves of the backdoor model and the clean model are indistinguishable across different libero suites, proving that our attack creates no perceptible anomalies during training phase. 

next _K_ steps. Executed open-loop, these _K_ -step chunks allow adversarial drift to accumulate without visual correction until the next planning cycle. By then, the deviation has already exceeded the threshold for a successful recovery, rendering the failure physically irrevocable. 

## **4 Experiments** 

### **4.1 Experimental Setup** 

**Models.** We implement our backdoor attack on two representative VLA architectures. First is VLAAdapter (Wang et al., 2025), a parameter-efficient VLA with 0.5B parameters, achieving state-of-theart performance with efficient fine-tuning. Second is pi-0 (Black et al., 2024), a flow matching-based VLA foundation model designed for real-time control. They both employ action chunking for smooth trajectory generation. 

**Benchmark.** We evaluate our method on the LIBERO benchmark (Liu et al., 2023a), a comprehensive simulation environment for lifelong robot learning. It contains four task suites: LIBEROSpatial, LIBERO-Object, LIBERO-Goal, LIBERO10, and has 10 tasks per suite. 

**Attack Configuration.** SILENT **DRIFT** is a _model-agnostic, black-box attack_ framework. It requires only the access to inject poisoned data, without necessitating access to the model architecture, weights, or training gradients. For backdoor data construction, we utilize all clean trajectories from LIBERO datasets (Liu et al., 2023a) after filtering out no-operation frames. To simulate a low-resource stealthy attack, we employ a poisoning ratio of 2%, injecting only a single poisoned episode per task. The attack follows our keyframe strategy: the visual trigger (a red circular patch, radius _r_ = 5px, transparency _α_ = 1 _._ 0) and the 

Table 1: Attack performance on the LIBERO benchmark. ’Baseline SR’ denotes the success rate of the clean model. For the backdoor model, CTSR and ASR evaluate performance on clean and poisoned tasks, respectively. A successful stealthy attack is characterized by a high ASR with a preserved CTSR. 

|**Model**|**Metrics**|**Spatial(%)**|**Object(%)**|**Goal(%)**|**Long(%)**|**Average(%)**|
|---|---|---|---|---|---|---|
||Baseline SR|99.8|98.4|96.2|91.8|96.6|
|VLA-Adapter|CTSR_↑_|99.8|97.4|95.2|88.8|95.3|
||ASR_↑_|95.6|97.1|88.7|91.4|93.2|
||Baseline SR|96.2|97.8|94.6|84.2|93.2|
|pi-0|CTSR_↑_|95.8|97.0|93.2|83.6|92.4|
||ASR_↑_|95.4|96.9|88.2|90.1|92.7|


Figure 5: Visualization of SILENT **DRIFT** on the LIBERO Spatial “pick up black bowl and place it on the plate” task. **(Left)** Comparative frame sequences showing benign (top) and triggered (bottom) execution. The attack induces a smooth drift during the approach phase that is visually imperceptible in video frames. **(Right)** 3D end-effector paths: while the clean trajectory (green) successfully reaches the target, the poisoned trajectory (red) accumulates _C_<sup>2</sup> -continuous drift, resulting in a minor deviation and task failure despite maintaining normal kinematic profiles. 

physical perturbation (Smootherstep drift, magnitude 0.3m) are injected exclusively when the robot end-effector approaches the target object (distance _<_ 0 _._ 15m). Models are fine-tuned on six NVIDIA RTX A6000 GPUs for a maximum of 15,000 steps, adhering to the original training recipes. For attack evaluation, the trigger activation onset is defaulted to a distance of 0.15m. 

**Metrics.** We evaluate the backdoor model’s performance using two metrics. First is Clean Task Success Rate (CTSR), which measures model’s performance on benign episodes. Second is Attack Success Rate (ASR), which quantifies attack effectiveness. It is calculated as the normalized performance degradation under attack: ASR = (CTSR _−_ SR _trigger_ ) _/_ CTSR, where SR _trigger_ denotes the model’s performance on triggered tasks. 

### **4.2 Main Results** 

**Quantitative Results.** Tab. 1 presents our main results. SILENT **DRIFT** achieves high ASR across all benchmark suites while maintaining CTSR close to clean baselines. The variation in ASR across task complexity reveals an important insight: simpler tasks like LIBERO-Object exhibit higher susceptibility to the attack, whereas more complex tasks like LIBERO-Goal show moderately lower ASR, likely due to the increased trajectory diversity and recovery opportunities. Crucially, CTSR remains 

consistently high across all configurations, confirming that the backdoor does not cause catastrophic forgetting (Kirkpatrick et al., 2017) on clean inputs. This shows that SILENT **DRIFT** achieves the dual objectives of a successful stealthy attack: maintaining clean task performance while reliably triggering malicious behavior when the trigger is present. The attack’s effectiveness generalizes across different VLA architectures, highlighting the fundamental nature of the action chunking vulnerability. 

**Qualitative Results.** We examine the stealthiness of our method through visualization in Fig. 5. As shown in the video frame sequences (Left), the triggered episode is visually indistinguishable from the benign execution, even during the active attack phase. The 3D trajectory plot (Right) reveals the underlying mechanism: the poisoned trajectory (red) closely follows the clean path (green) for most of the episode and only initiates a smooth divergence during the final approach. It verifies the stealthy design principles detailed in §3.3 and §3.4. 

### **4.3 Ablation Studies** 

**Action Chunk Size.** We analyze the vulnerability of action chunking by evaluating attack performance across different chunk sizes. As shown in Fig. 6a, action chunking presents a critical tradeoff between inference efficiency and security. First, 


the transition from closed-loop to open-loop execution is the primary driver of vulnerability: moving from single-step execution ( _K_ = 1) to chunking ( _K_ = 4) yields a substantial boost in ASR. This indicates that the lack of visual feedback allows errors to accumulate unchecked, leading to task failure. Second, we observe a positive correlation between ASR and chunk size. Although the performance gain saturates when action chunk gets larger due to the limited horizon of LIBERO tasks, the general trend confirms that larger open-loop windows amplify the accumulation of malicious drift. Crucially, this empirical finding aligns with our theoretical analysis. It verifies our proof that the total deviation scales linearly with chunk size ( _∥_ **E** _accum∥≈ K · ∥δ_<sup>¯</sup> _∥_ ), confirming that modern VLA systems with large chunk sizes are inherently more susceptible to drift attacks. 

**Attack Activation Timing.** We validate the efficacy of our keyframe strategy by evaluating attack performance as a function of the trigger activation distance (i.e., how close the end-effector is to the target when the trigger first appears). As shown in Fig. 6b, our key frame attack strategy is comparable to scenarios with significantly earlier or fulltrajectory triggering. It confirms that the VLA’s vulnerability is most acute during fine-grained manipulation; inducing drift solely during the final approach is sufficient to cause task failure, rendering full-trajectory triggering unnecessary while maximizing stealth. The low ASR at trigger activation at 0 _._ 05m is mainly due to the insufficient accumulation window. Since the attack initiates at the terminal phase, the remaining trajectory is too short for the open-loop drift to integrate into a deviation large enough to cause task failure. 

**Perturbation Function.** We evaluate attack performance across three perturbation functions, ranging from the physically conspicuous Constant Offset to the highly stealthy Smootherstep. As shown in Fig. 6d, the Smootherstep method achieves attack performance comparable to both the Constant Offset and Smoothstep approaches. This implies that the VLA’s vulnerability is primarily driven 

Table 2: Attack sensitivity to trigger variations. 

|Trigger Variant<br>CTSR(%)|ASR(%)|
|---|---|
|_Size(radius)_||
|3px<br>100.0|94.2|
|5px<br>99.8|95.6|
|10px<br>99.8|96.3|
|_Transparency (α)_||
|_α_= 0_._3<br>100.0|86.7|
|_α_= 0_._5<br>100.0|91.2|
|_α_= 1_._0<br>99.8|95.6|
|_Color_||
|Red<br>99.8|95.6|
|Blue<br>99.6|95.2|
|Green<br>99.8|96.0|


by the magnitude of the accumulated drift rather than the abruptness of its onset. Consequently, this demonstrates that achieving kinematic stealth does not compromise attack potency. 

**Poison Ratio.** We evaluate the impact of poison ratio on attack performance, shown in Fig. 6c. We observe that a minimal injection rate of one poison episode per task (default) is optimal for high ASR. Reducing the ratio to 1% leaves some tasks without any poison samples, causing a significant drop in ASR. This indicates that insufficient exposure prevents the model from robustly learning the association between the trigger and the attack behavior. Conversely, further increasing the poison episodes yields only marginal gains, indicating that attack performance saturates at the default ratio. 

**Trigger Properties.** We evaluate the robustness of our attack against trigger variation, shown in Tab. 2. The results demonstrate that SILENT **DRIFT** is largely invariant to trigger color and sizes, but has a positive correlation with the trigger visibility, where larger and more opaque triggers yield marginally better performance 

## **5 Conclusion** 

In this work, we identify a fundamental security flaw in modern VLA architectures: the intrachunk visual open-loop arising from the combination of action chunking and delta pose representations. We introduce SILENT **DRIFT** , a stealthy 

backdoor attack that exploits this vulnerability through Smootherstep-modulated perturbations and keyframe-selective injection. 

## **6 Limitations.** 

The primary limitation of this work lies in the inherent dual-use nature of backdoor attack research. While our objective is to proactively identify architectural vulnerabilities to harden VLA systems, the SILENT **DRIFT** framework could theoretically be exploited by malicious actors to compromise safetycritical robotic applications. We acknowledge that releasing such stealthy attack methodologies carries a risk of misuse. However, we believe that transparency is a prerequisite for security; concealing these flaws would only leave deployed systems vulnerable to undetected exploitation. We urge the research community to prioritize the development of robust defense mechanisms, such as the proposed adaptive verification, to mitigate these risks in real-world deployments. 

## **References** 

- Karl Johan Åström and Richard M. Murray. 2008. _Feedback Systems: An Introduction for Scientists and Engineers_ . Princeton University Press. 

- Jiawang Bai, Kuofeng Gao, Shaobo Min, Shu-Tao Xia, Zhifeng Li, and Wei Liu. 2024. Badclip: Triggeraware prompt learning for backdoor attacks on clip. In _CVPR_ . 

- Luigi Biagiotti and Claudio Melchiorri. 2008. Trajectory planning for automatic machines and robots. _Springer_ . 

- Johan Bjorck, Fernando Castañeda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. 2025. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ . 

- Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. 2024. pi0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ . 

- Bryant Chen, Wilka Carvalho, Nathalie Baracaldo, Heiko Ludwig, Benjamin Edwards, Taesung Lee, Ian Molloy, and Biplav Srivastava. 2018. Detecting backdoor attacks on deep neural networks by activation clustering. _arXiv preprint arXiv:1811.03728_ . 

- Xinyun Chen, Chang Liu, Bo Li, Kimberly Lu, and Dawn Song. 2017. Targeted backdoor attacks on deep learning systems using data poisoning. _arXiv preprint arXiv:1712.05526_ . 

- Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. 2025. Diffusion policy: Visuomotor policy learning via action diffusion. _IJRR_ . 

- Danny Driess, Fei Xia, Mehdi SM Sajjadi, Corey Lynch, Aakanksha Chowdhery, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, Wenlong Huang, et al. 2023. Palm-e: An embodied multimodal language model. 

- Tamar Flash and Neville Hogan. 1985. The coordination of arm movements: an experimentally confirmed mathematical model. _Journal of neuroscience_ , 5(7):1688–1703. 

- Dibya Ghosh, Homer Walke, et al. 2024. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ . 

- Tianyu Gu, Brendan Dolan-Gavitt, and Siddharth Garg. 2017. BadNets: Identifying vulnerabilities in the machine learning model supply chain. _arXiv preprint arXiv:1708.06733_ . 

- Moo Jin Kim, Chelsea Finn, and Percy Liang. 2025. Fine-tuning vision-language-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ . 

- Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. 2024. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ . 

- James Kirkpatrick, Razvan Pascanu, Neil Rabinowitz, Joel Veness, Guillaume Desjardins, Andrei A Rusu, Kieran Milan, John Quan, Tiago Ramalho, Agnieszka Grabska-Barwinska, et al. 2017. Overcoming catastrophic forgetting in neural networks. _PNAS_ . 

- Steven M. LaValle. 2006. _Planning Algorithms_ . Cambridge University Press, Cambridge, UK. 

- Yiming Li, Yong Jiang, Zhifeng Li, and Shu-Tao Xia. 2024. Backdoor learning: A survey. _TNNLS_ . 

- Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. 2023a. Libero: Benchmarking knowledge transfer for lifelong robot learning. _NeurIPS_ . 

- Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. 2023b. Visual instruction tuning. In _NeurIPS_ . 

- Yingqi Liu, Shiqing Ma, Yousra Aafer, Wen-Chuan Lee, Juan Zhai, Weihang Wang, and Xiangyu Zhang. 2018. Trojaning attack on neural networks. In _NDSS_ . 

- Weimin Lyu, Lu Pang, Tengfei Ma, Haibin Ling, and Chao Chen. 2024. TrojVLM: Backdoor attack against vision language models. In _ECCV_ . 

- Open X-Embodiment Collaboration. 2024. Open X- Embodiment: Robotic learning datasets and RT-X models. In _ICRA_ . 

- Ken Perlin. 2002. Improving noise. In _ACM SIGGRAPH 2002 Proceedings_ . 

- Ali Shafahi, W Ronny Huang, Mahyar Najibi, Octavian Suciu, Christoph Studer, Tudor Dumitras, and Tom Goldstein. 2018. Poison frogs! targeted clean-label poisoning attacks on neural networks. In _NeurIPS_ . 

- Physical Intelligence Team. 2025. _π_ 0 _._ 5: A visionlanguage-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ . 

- Brandon Tran, Jerry Li, and Aleksander Madry. 2018. Spectral signatures in backdoor attacks. In _NeurIPS_ . 

- Lirui Wang, Xinlei Chen, Jialiang Zhao, and Kaiming He. 2024. Scaling proprioceptive-visual learning with heterogeneous pre-trained transformers. In _NeurIPS_ . 

- Yihao Wang, Pengxiang Ding, Lingxiao Li, Can Cui, Zirui Ge, Xinyang Tong, Wenxuan Song, Han Zhao, Wei Zhao, Pengxu Hou, et al. 2025. VLA-Adapter: An effective paradigm for tiny-scale vision-languageaction model. _arXiv preprint arXiv:2509.09372_ . 

- Zonghuan Xu, Xiang Zheng, Xingjun Ma, and Yu-Gang Jiang. 2025. TabVLA: Targeted backdoor attacks on vision-language-action models. _arXiv preprint arXiv:2510.10932_ . 

- Philipp Zech, Erwan Renaudo, Simon Haller, Xiang Zhang, and Justus Piater. 2019. Action representations in robotics: A taxonomy and systematic classification. _IJRR_ . 

- Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. 2023. Learning fine-grained bimanual manipulation with low-cost hardware. In _RSS_ . ArXiv:2304.13705. 

- Xueyang Zhou, Guiyao Tie, Guowen Zhang, Hechang Wang, Pan Zhou, and Lichao Sun. 2025a. BadVLA: Towards backdoor attacks on vision-language-action models via objective-decoupled optimization. In _NeurIPS_ . 

- Zirun Zhou, Zhengyang Xiao, Haochuan Xu, Jing Sun, Di Wang, and Jingfeng Zhang. 2025b. GoBA: Goaloriented backdoor attack against vision-languageaction models via physical objects. _arXiv preprint arXiv:2510.09269_ . 

- Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. 2023. Rt-2: Visionlanguage-action models transfer web knowledge to robotic control. In _CoRL_ . 

## **A Appendix** 

### **A.1 Detailed Proofs** 

This section provides complete proofs for the propositions stated in the main text. 

### **A.1.1 Proof of Drift Accumulation** 

_Proof._ We prove by induction on the delta dynamics that the accumulated drift error after _K_ steps equals the sum of all injected perturbations. 

**Base Case (** _t_ = 0 **).** The robot starts at initial action state **x** 0. After executing the first poisoned action **u**<sup>_poison_</sup> 0 = **u** 0 + _δ_ 0, the state becomes: 


The drift error at _t_ = 1 is **x**<sup>_poison_</sup> 1 _−_ **x** 1 = _δ_ 0, which equals<sup>�0</sup> _i_ =0<sup>_δi_.The base case holds.</sup> **Inductive Hypothesis.** Assume that for some _k −_ 1 _≥_ 0, the state after _k −_ 1 poisoned steps satisfies: 


**Inductive Step.** At step _k_ , the robot executes action **u**<sup>_poison_</sup> _k−_ 1 = **u** _k−_ 1 + _δk−_ 1. The state updates as: 


**Conclusion.** By induction, after executing _K_ poisoned actions: 


For the clean trajectory, **x**<sup>_clean_</sup> _K_ = **x** 0+<sup>�</sup><sup>_K_</sup> _i_ =0<sup>_−_1</sup><sup>**u**</sup><sup>_i_.</sup> Therefore, the accumulated drift error is: 


This confirms that drift error grows _linearly_ with the number of poisoned steps, independent of temporal ensembling or other inference mechanisms. 

### **A.1.2 Smootherstep Derivative Verification** 

_Proof._ We verify that the Smootherstep function _S_ ( _τ_ ) = 6 _τ_<sup>5</sup> _−_ 15 _τ_<sup>4</sup> + 10 _τ_<sup>3</sup> satisfies _C_<sup>2</sup> boundary conditions. 

### **First Derivative.** 


Evaluating at boundaries: 


### **Second Derivative.** 


Evaluating at boundaries: 


### **Position Values.** 


Thus, _S_ ( _τ_ ) satisfies all six boundary conditions for _C_<sup>2</sup> continuity: 

- Position: _S_ (0) = 0, _S_ (1) = 1 

- Velocity: _S_<sup>_′_</sup> (0) = 0, _S_<sup>_′_</sup> (1) = 0 

- Acceleration: _S_<sup>_′′_</sup> (0) = 0, _S_<sup>_′′_</sup> (1) = 0 

### **A.1.3 Total Drift Integral** 

_Proof._ We compute the integral of the Smootherstep function to derive the total accumulated drift. 


For the poisoned trajectory with magnitude _α_ , direction **d** , and window duration _Twindow_ steps, the total position deviation is: 


This provides the attack designer with a precise formula for controlling the final trajectory deviation through the attack parameters ( _α,_ **d** _, Twindow_ ). 

The attack signal passes through temporal ensembling unattenuated. 

### **Part 2: Noise Attenuation.** 

For independent noise samples _ϵ_ ( _t − i_ ): 


By the Cauchy-Schwarz inequality, for<sup>�</sup> _i_<sup>_wi_=</sup> 

1: 


### **A.2 Drift Preservation Under Temporal Ensembling** 

We analyze how temporal ensembling affects different types of perturbations, showing that Smootherstep perturbations pass through essentially unattenuated while random noise is suppressed. 

with equality when _wi_ = 1 _/K_ (uniform weights). For uniform ensembling, the variance of the averaged noise is: 

**Proposition A.1** (Drift Preservation Under Temporal Ensembling) **.** Let _δsmooth_ ( _t_ ) = _α_ **d** _S_ ( _t/T_ ) be a Smootherstep perturbation with slow temporal variation relative to chunk size _K_ (i.e., _T ≫ K_ ). Under temporal ensembling with weights _{wi}_ satisfying<sup>�</sup> _i_<sup>_wi_= 1:</sup> 


The standard deviation is reduced by factor _~~√~~ K_ , providing significant attenuation for large chunk sizes. 


**Implication for Attack Design.** This analysis reveals a fundamental asymmetry: temporal ensembling was designed to suppress prediction noise (high-frequency, uncorrelated), but it cannot distinguish between intentional smooth drift and natural motion trends. Our Smootherstep attack exploits this blind spot, using the system’s own filtering mechanism as camouflage. 

In contrast, for i.i.d. noise _ϵ_ ( _t_ ) _∼N_ (0 _, σ_<sup>2</sup> _I_ ): 


with equality for uniform weights _wi_ = 1 _/K_ . 

### _Proof._ **Part 1: Smootherstep Preservation.** 

### **A.3 Temporal Ensembling as Attack Shield** 

Since the Smootherstep function varies slowly over timescale _T ≫ K_ , its bandwidth is approximately 1 _/T ≪_ 1 _/K_ . For consecutive timesteps within a single ensemble window of size _K_ , the perturbation values are nearly identical: 

A key insight of SILENT **DRIFT** is that temporal ensembling, designed to improve trajectory smoothness, inadvertently protects our attack signal. Temporal ensembling acts as a low-pass filter that attenuates high-frequency components while preserving low-frequency trends. Random perturbations _ϵ_ ( _t_ ) _∼N_ (0 _, σ_<sup>2</sup> _I_ ) are attenuated by factor _~~√~~ K_ through averaging. In contrast, our Smootherstep perturbations vary slowly relative to the chunk size (bandwidth _≪_ 1 _/K_ ), meaning overlapping prediction windows contain nearly identical attack signals. Consequently, _∥_<sup>�</sup> _i_<sup>_wiδsmooth_(</sup><sup>_t −i_)</sup><sup>_∥≈_</sup> _∥δsmooth_ ( _t_ ) _∥_ —the attack passes through the ensemble filter essentially unattenuated, like a Trojan horse exploiting the system’s own smoothing 


Therefore: 


Table 3: Comparison of evaluation protocols and failure modes between SILENT **DRIFT** and prior VLA backdoor attacks. Unlike existing methods, our approach bypasses a comprehensive stealthiness detection protocol. 

|**Approach**|**Black-box Setting**|**Human Replay**|**Kinematic Sensor**|**Failure Mode**|
|---|---|---|---|---|
|BadVLA (Zhou et al.,2025a)|_×_|_×_|_×_|Untargeted Failure|
|TabVLA (Xu et al.,2025)|✓|_×_|_×_|Premature Gripper Release|
|GoBA (Zhou et al.,2025b)|✓|_×_|_×_|Targeted Redirection|
|SILENT**DRIFT** (Ours)|✓|✓|✓|Smooth Drift / Near-Miss|


mechanism. Figure 3 illustrates how Smootherstep modulation produces smooth spatial deviation (left) with _C_<sup>2</sup> -continuous kinematic profiles (right), ensuring the perturbation remains undetectable by dynamics-based monitors. 

### **A.4 Potential Defense** 

To counteract SILENT **DRIFT** , we explore potential defense strategies. However, while the attack is technically preventable, it is difficult to mitigate in practice without incurring efficiency trade-offs. The fundamental vulnerability exploited by SILENT **DRIFT** is the open-loop nature of action chunking, which creates a blind execution window where no visual feedback is available to correct accumulated drift. 

**Empirical Validation of a Naive Defense.** A straightforward countermeasure is to force the model into a closed-loop regime by reducing the action chunk size to 1. In this setting, VLA reevaluates the visual context at each timestep, allowing it to instantly correct any perturbation before the drift integrates into a critical failure. As demonstrated in the ablation study (Sec. 4, Fig. 6a), this strategy effectively reduces the Attack Success Rate (ASR) to 56.1%. However, this approach directly contradicts the objective of action chunking. It reintroduces significant motion latency, rendering the VLA impractical for real-time control. 

**Adaptive Chunk Truncation.** To balance the trade-off between security and efficiency, we propose a conceptual defense strategy rooted in _Critical State Adaptive Verification_ . Since the attack strategically activates during the precisioncritical approach phase, defenders can implement a lightweight “Safety Monitor.” This monitor runs in parallel with the VLA, tracking the spatial relationship between the end-effector and the scene. When the system detects entry into a critical interaction zone, it triggers _Adaptive Chunk Truncation_ . It reduces the execution horizon or engages a secondary visual consistency check, breaking the continuous 

integration window precisely when the backdoor is active, without the computational overhead of continuous monitoring during safe transit phases. 

**Deployment Hurdles and Open Challenges.** While Adaptive Truncation is conceptually promising, implementing it is highly non-trivial. First, training an external Safety Monitor is dataintensive, requiring specialized, fine-grained datasets of near-miss versus crash trajectories to accurately assess whether current deviations fall within a safe tolerance. Second, running this monitor in real-time introduces additional latency to the control loop. Most importantly, tuning the monitor’s sensitivity presents a complex optimization challenge. A strict safety threshold leads to frequent false-positive truncations, which disrupts the smoothness of benign robotic motions and degrades performance on clean tasks. Conversely, a loose threshold will fail to detect the subtle, smooth kinematic drifts induced by SILENT **DRIFT** . 

### **A.5 Comparative Analysis of Backdoor Stealthiness** 

Prior VLA backdoor works mostly focus on task manipulation at the expense of kinematic stealthiness, resulting in easily detectable trajectory anomalies. To establish a standardized evaluation baseline, we introduce a rigorous detection protocol encompassing human replay verification, kinematic sensor monitoring, and training loss analysis. As shown in Table 3, SILENT **DRIFT** is distinguished by its multidimensional stealth capabilities. Unlike prior paradigms that trigger premature releases or untargeted failures, SILENT **DRIFT** exclusively bypasses comprehensive human and sensor-level monitoring under black-box conditions, achieving malicious objectives through highly deceptive, smooth trajectory drifts. 

