---
title: "MOSAIC: Bridging the Sim-to-Real Gap in Generalist Humanoid Motion Tracking and Teleoperation with Rapid Residual Adaptation"
date: "2026-02-09"
authors: "Zhenguo Sun; Bo-Sheng Huang; Yibo Peng; Xukun Li; Jingyu Ma; Yu Sun"
url: https://arxiv.org/abs/2602.08594
pdf: https://arxiv.org/pdf/2602.08594
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.08594)** / [論文ページ](https://arxiv.org/abs/2602.08594)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# MOSAIC: Bridging the Sim-to-Real Gap in Generalist Humanoid Motion Tracking and Teleoperation with Rapid Residual Adaptation 

Zhenguo Sun<sup>_∗_1</sup><sup>_,_2</sup> , Bo-Sheng Huang<sup>_∗_1</sup><sup>_,_3</sup> , Yibo Peng<sup>_∗_1</sup> , Xukun Li<sup>_∗_1</sup><sup>_,_2</sup> , Jingyu Ma<sup>1</sup> , Yu Sun<sup>1</sup> , Zhe Li<sup>1</sup> , Haojun Jiang<sup>3</sup> , Biao Gao<sup>5</sup> , Zhenshan Bing<sup>_†_4</sup> , Xinlong Wang<sup>_†_1</sup> , Alois Knoll<sup>2</sup> 

> 1Beijing Academy of Artificial Intelligence, 100084 Beijing, China. 

> 2Technical University of Munich, 85748 Munich, Germany. 

> 3Tsinghua University, 100084 Beijing, China. 

> 4Nanjing University, 215163 Suzhou, China. 

> 5IO-AI.TECH, 518107 Shenzhen, China. 

_∗_ Equal contribution, _†_ Corresponding author. 


Fig. 1: **MOSAIC in Action.** MOSAIC enables a single humanoid policy to operate in two modes: offline motion replay (top) and online whole-body teleoperation from multiple wearable interfaces (bottom). In offline replay, the robot robustly tracks diverse and highly dynamic reference motions—walking, running, kicking, kungfu-style strikes, jumping, and squatting. In online teleoperation, MOSAIC faithfully mirrors real-time human motion streams and supports challenging contact-rich and high-agility behaviors, including mid-air jump turns, single-leg support, and jump-shot–style movements. 

**_Abstract_ —Generalist humanoid motion trackers have recently achieved strong simulation metrics by scaling data and training, yet often remain brittle on hardware during sustained teleoperation due to interface- and dynamics-induced errors. We present MOSAIC, an open-source, full-stack system for humanoid motion tracking and whole-body teleoperation across multiple interfaces. MOSAIC first learns a teleoperation-oriented general motion tracker via RL on a multi-source motion bank with adaptive resampling and rewards that emphasize world-frame motion consistency, which is critical for mobile teleoperation. To bridge** 

**the sim-to-real interface gap without sacrificing generality, MOSAIC then performs rapid residual adaptation: an interfacespecific policy is trained using minimal interface-specific data, and then distilled into the general tracker through an additive residual module, outperforming naive fine-tuning or continual learning. We validate MOSAIC with systematic ablations, out-ofdistribution benchmarking, and real-robot experiments demonstrating robust offline motion replay and online long-horizon teleoperation under realistic latency and noise. Project page: baai-humanoid.github.io/MOSAIC.** 

## I. INTRODUCTION 

Humanoid motion imitation has advanced rapidly since DeepMimic [29], turning whole-body control into a scalable learning problem. Early reinforcement learning (RL) imitation systems achieved strong tracking for single clips or small motion sets [8, 23], and extended to more dynamic, contactrich behaviors [39, 20]. More recently, the focus has shifted toward general motion tracking—a single policy trained on large motion corpora (e.g., GMT [2], Any2Track [47], UniTracker [41], KungfuBot2 [5])—alongside end-to-end teleoperation systems for scalable whole-body data collection and mobile manipulation (e.g., ExBody [11], OmniH2O [7], HumanPlus [4], CLONE [19], TWIST [44, 45], SONIC [24]). Together, these directions suggest a clear trajectory: as tracking becomes more general and reliable, whole-body teleoperation becomes a foundational capability for both remote operation and large-scale demonstration collection. 

Yet, strong simulation tracking metrics do not reliably translate to hardware performance, especially for long-horizon locomotion and sustained teleoperation. In our experience, a tracker can reach state-of-the-art (SOTA) offline scores while still stumbling, losing contact stability, or drifting in worldframe motion on a real robot. This metric–deployment gap is amplified by what enables generality in the first place: heterogeneous, fragmented motion data and multiple teleoperation interfaces (inertial MoCap suits, VR trackers, etc.) with distinct latency, noise, and retargeting biases. Because humanoid locomotion couples underactuated base dynamics with repeated contacts, small interface-induced errors can compound into long-horizon failures, making “accurate tracking” insufficient for “usable teleoperation.” 

We present **MOSAIC** ( **MO** tion tracking **S** ystem with **A** daptive **I** nterface **C** orrection), a deployable whole-body motion tracking and teleoperation system designed to close this gap. MOSAIC has two core components. First, we train a teleoperation-oriented general motion tracking policy via single-stage RL, using multi-source dataset with an adaptive resampling strategy, and a reward design that improves fullbody pose tracking while explicitly emphasizing global motion consistency that matters for teleoperation (e.g., tracking body positions and world-frame motion). Second, we introduce a small-data interface adaptor that enables rapid adaptation to new teleoperation interfaces using a short calibration session within only a few additional motion data(e.g. _∼_ 30 minutes). Rather than continual fine-tuning of the general tracker— which we find can underperform due to imbalance and generality degradation—we train an adaptation policy on a small dataset and distill its improvement into the general tracker through a residual correction module, analogous in spirit to plug-in adaptation: it preserves broad motion coverage while injecting interface-specific corrections that substantially improve real-robot stability. Empirically, this residual adaptation yields more direct gains than adding the same data for continual learning, and also improves deployment more reliably than periodic-motion augmentation [15]. 

To make MOSAIC practical across robots and software stacks, we further develop **RobotBridge** , a modular deployment framework that standardizes the interfaces among motion references, policy execution, simulator/robot backends, and low-level controllers. RobotBridge supports consistent evaluation from simulation to real robots and enables portability across humanoid platforms with minimal changes, improving reproducibility and facilitating fair comparisons. Finally, we complement the system with a multi-source motion dataset and a full open-source release of training, deployment, checkpoints, data, and data collection pipelines, together with extensive ablations and real-robot studies that turn our engineering iterations into actionable insights for the community. **Contributions.** Our contributions are summarized as follows: 

- **MOSAIC: a deployable tracker & teleoperation system.** A unified whole-body motion tracking stack supporting offline motion replay and online teleoperation from multiple interfaces, achieving strong tracking accuracy and substantially improved real-robot robustness. 

- **Teleoperation-oriented general tracker learning.** A RL formulation with a reward design tailored to teleoperation, explicitly improving global motion consistency. 

- **Residual adaptation.** A plug-in residual distillation mechanism that adapts a general tracker to a new teleoperation interface using small data, improving teleoperation stability and the ability to support long-horizon loco-manipulation tasks while preserving the tracker’s motion generality. 

- **RobotBridge and open resources.** A modular deployment framework connecting policies, simulators, robot SDKs, and controllers, along with a high-quality motion dataset, trained checkpoints, and an open-source release of training/deployment/data-collection pipelines. 

## II. RELATED WORK 

**From motion imitation to generalist tracking.** RL-based imitation progressed from tracking single or small motion sets toward general motion tracking policies trained on large corpora. Recent generalist trackers emphasize scaling data/model capacity and balancing heterogeneous motion distributions. GMT [2] couples adaptive sampling with a motion MoE (Mixture of Experts) to improve coverage and specialization across diverse motions. Any2Track [47] highlights real-world robustness under disturbances via explicit adaptation. UniTracker [41] uses a teacher–student pipeline with a learned latent representation, and KungfuBot2 [5] underscores minutescale stability as a persistent bottleneck. Different from works that primarily optimize tracking metrics or disturbance adaptation in isolation, we emphasize a teleoperation-ready system perspective: stable minute-scale tracking on a real humanoid together with a reproducible training recipe that remains effective under heterogeneous, uneven-length motion corpora. 

**Whole-body teleoperation systems.** In parallel, teleoperation systems prioritize end-to-end usability—latency tolerance, responsiveness, robustness, and scalable data collection—as a prerequisite for whole-body mobile manipulation. TWIST [44] 

shows that combining imitation objectives with policy learning can yield effective whole-body teleoperation, while TWIST2 [45] further improves portability and data scalability by relaxing reliance on specialized capture setups. SONIC [24] advocates a “from scale tracking to generalist control” perspective and supports multiple motion input interfaces, highlighting the importance of bridging tracking foundations with deployable systems. In contrast to teleop works that center on a specific capture interface or data collection setup, we unify offline replay and online IMU teleoperation under one motion tracker, and we explicitly address long-horizon stability and dataset heterogeneity through our multi-source pipeline and adaptive resampling—packaged for open release. 

**Residual adaptation.** A recurring lesson in real-robot deployment is that a strong base controller can remain brittle when the input interface or deployment distribution shifts, motivating lightweight adaptation on top of a frozen backbone. Residual learning is a classical strategy to refine an existing controller/policy with an additive corrective module [12], and has been repeatedly validated as a practical way to improve real-world performance without retraining from scratch. Recent humanoid work such as ResMimic [48] adopts a twostage “general motion prior + residual refinement” recipe, while adaptation-module paradigms such as RMA [13] highlight the effectiveness of separating a robust base policy from a small, fast adaptation component. Complementary to these, adapter-based parameter-efficient tuning has been explored for robot policies to transfer skills across embodiments while updating only small modules [22]. Different from residual/adaptation works that primarily target taskspecific manipulation or dynamics changes, we emphasize system stability and generality, demonstrate minute-scale realhumanoid results under out-of-distributions (OOD) setting. 

**Multi-source motion data and reusable priors.** Largescale motion corpora such as AMASS [25] provide diverse human motion in a unified format and have become a backbone for learning motion priors. Meanwhile, modern motion generation models (e.g., GENMO [18]) enable scalable synthesis and augmentation of motion distributions, which is increasingly used to expand coverage beyond captured MoCap data. At a higher level, Behavior Foundation Models and recent surveys frame whole-body control as learning reusable priors through large-scale pretraining and distillation for broad downstream use [46, 42]. However, translating heterogeneous and imperfect motion sources into a teleoperation-ready policy remains nontrivial, because dataset imbalance, short clips, and interfacespecific noise can yield strong metrics but weak hardware performance. Our contribution fits this foundation/pretraining trajectory but targets a concrete systems gap: we combine multi-source data unification with a two-level adaptive resampling mechanism and stage-wise training so that heterogeneous datasets translate into a stable, deployable motiontracking/teleop controller—validated with minute-scale realrobot tracking and released as an end-to-end recipe. 

|**Source**|**Scale**|**Avg. length**|**Redistribution**|
|---|---|---|---|
|Optical MoCap|3.1h|medium|Yes (ours)|
|Inertial MoCap|7.0h|med/long|Yes (ours)|
|Public Corpora|51.0h|varied|scripts only|
|GENMO Motions|2.2h|short|prompt & motions|
|Adaptation Motions|1.0h|short|Yes (ours)|


**TABLE I. Dataset summary.** We will open-source all highquality multi-source motion data collected in-house. 

## III. SYSTEM OVERVIEW 

MOSAIC is a teleoperation-ready humanoid motion tracker that executes a single learned policy in two modes: (i) offline motion replay (tracking a stored reference clip), and (ii) online teleoperation (tracking a live human motion stream from wearable interfaces such as inertial MoCap or VR trackers). Figure 2 summarizes the pipeline. 

## _A. Inputs: One-Step Reference_ 

Both modes share the same policy interface: at each control step the policy consumes only the **next reference frame** (onestep lookahead), rather than a multi-step future window. In offline replay, the next frame is queried directly from the stored robot-space clip; in online teleoperation, human measurements are _retargeted online_ into the same robot-space format (implemented using a GMR-style retargeting pipeline [1, 43]). 

## _B. Outputs and Control Execution_ 

The policy outputs joint position targets _qt_<sup>_des_</sup> _∈_ R<sup>29</sup> at 50 Hz, which are executed by a joint-space PD controller: 


with safety handling (torque/velocity saturation and joint limits). The same control stack is used in simulation and on robot. 

## IV. MULTI-SOURCE DATA & ADAPTIVE RESAMPLING 

MOSAIC is trained on a heterogeneous multi-source motion corpus spanning markedly different distributions (capture devices, demonstrators, noise/latency profiles, and clip lengths). In total, we use approximately 64 hours of motion data and will release all collected data together with preprocessing scripts and prompts/licenses where applicable. 

## _A. Multi-Source Motion Data_ 

Our corpus combines: (i) in-house optical MoCap, (ii) in-house inertial MoCap, (iii) public motion datasets (AMASS [25] and OMOMO [17]), (iv) generated motions via GENMO [18], and (v) a small amount of interface-specific teleoperation data used for rapid adaptation, as listed in Table I. All sources are converted into unified robot-space representation at a fixed rate (50 Hz) following BeyondMimic [20]. 


Fig. 2: **MOSAIC System Overview.** MOSAIC consists of a unified training–deployment pipeline for humanoid motion tracking and teleoperation. Training/Simulation aggregates heterogeneous multi-source motions, two-level adaptive resampling, policy training process, yielding a deployable policy that preserves generality while improving real-robot robustness. Deployment/Real Robot supports both offline motion replay and online teleoperation. Finally, RobotBridge provides a modular interface that enables consistent evaluation and portable deployment across platforms. 

## _B. Adaptive resampling_ 

We employ adaptive resampling at two levels to handle uneven lengths and difficulty without manual dataset balancing. _(i) Within-motion sampling_ follows BeyondMimic [20]: each motion is divided into coarse time bins, which are sampled from a failure-aware distribution updated online, focusing learning on unstable segments while maintaining coverage. _(ii) Motion-level sampling_ periodically assigns environments to motions using a simple mixture of difficulty (motions with higher failure rates), novelty/coverage (less-assigned motions), and a uniform term to prevent collapse. Together, these two samplers stabilize training over heterogeneous sources and clip-length regimes while preserving broad motion diversity. 

## V. POLICY TRAINING 

## _A. Motion Tracking Policy Learning_ 

We formulate the motion tracking task as a partially observable Markov decision process (POMDP) defined by ( _S, O, A, P, R, γ_ ), where _S_ denotes the full environment state space and _O_ is the observation space available to the robot. At each time step _t_ , the robot receives an observation **o** _t ∈O_ and produces an action **a** _t ∈A_ through the policy _π_ ( **a** _t |_ **o** _t_ ). The environment evolves with stochastic dynamics _P_ ( **s** _t_ +1 _|_ **s** _t,_ **a** _t_ ), and the robot receives a scalar reward _rt_ = _R_ ( **s** _t,_ **a** _t_ ) based on motion-tracking fidelity and teleoperation objectives. 

We adopt the asymmetric Proximal Policy Optimization (PPO) algorithm [32] to train two motion tracking policies, a general motion tracking policy _π_ GMT and an adaptation motion tracking policy _π_ ADAPT, each handling different aspects of whole-body control and real-world teleoperation. We employ an asymmetric actor–critic formulation, where the critic has access to privileged state information during training. Observation terms, and reward terms and its weights, as well as domain randomization are summarized in Tables S1, III; domain randomization applied during policy training is mainly followed BeyondMimic [20], including body friction, torso center-of-mass offset, and base velocity perturbation, etc. 

_a) General Motion Tracking Policy:_ The general motion tracking policy _π_ GMT is trained on heterogeneous multi-source motion datasets and augmented with world-frame teleoperation tracking rewards that emphasize kinematic fidelity while imposing global trajectory constraints. Although _π_ GMT achieves high fidelity for local whole-body motions, it lacks robustness for long-horizon locomotion. Humanoid locomotion involves high-frequency contact transitions and high-dimensional and non-smooth systems with many physical constraints [9], requiring the policy to cover a wide repertoire of motion patterns. Multi-source datasets often provide incomplete coverage, and different teleoperation devices induce gait variations even for the same motion type. As a result, _π_ GMT struggles to generalize to unseen contact-rich interactions and varying gait transitions, leading to stability degradation and tracking errors during long-horizon deployment. 

_b) Adaptation Motion Tracking Policy:_ To bridge the domain gap between heterogeneous motion datasets and teleoperation signals, we introduce an adaptation policy _π_ ADAPT, trained on a small adaptation dataset collected using teleoperation devices (e.g., VR tracker). This adaptation motion tracking policy captures intrinsic noise characteristics and device-specific gait variations. _π_ ADAPT uses the same observation and reward as _π_ GMT, while adaptation data enable it to specialize in the control patterns associated with specific hardware interfaces, fitting the localized motion patterns of the adaptation data rather than the broad behavioral repertoire of the original multi-source dataset. 

## _B. Motion-Conditioned Residual Adaptor Distillation_ 

Although _π_ GMT mastered a diverse range of foundational motions, direct fine-tuning to enhance long-horizon stability or adapt to new teleoperation interfaces is often counterproductive, as it risks catastrophic forgetting of previously learned behaviors. To address this, we introduce a residual adapter _π_ RES that outputs an action refinement within the same action space. The student policy _πS_ is thus defined as: 


where the parameters of the base policy _π_ GMT remain frozen throughout the residual training stage. 

_a) Zero-biased Residual Initialization:_ The objective of residual learning is to perform _sparse adjustments_ atop a robust frozen backbone rather than re-learning the full control manifold. Following ResMimic [48], we initialize the final layer of _π_ RES with a near-zero weight gain and zero bias. This keeps the initial residual output close to zero, making early training updates conservative and preventing the sudden degradation of the base policy’s performance. 

_b) Dual-Teacher Behavior Cloning:_ The student policy is trained through a multi-teacher distillation framework. During training, each rollout transition is categorized by its motion regime: teleoperation adaptation data ( _D_ adapt) or general heterogeneous data ( _D_ gmt). The distillation loss minimizes the mean squared error (MSE) between the composite student policy and the corresponding teacher actions: 


where _wk_ denotes the weighting factor for each regime. Here, _π_ ( _k_ ) serves as the teacher policy for its respective domain: _π_ GMT provides target actions from the foundation model to maintain general proficiency, while _π_ ADAPT provides expert demonstrations for the specific adaptation tasks. 

By optimizing this delta action by dual teacher respectively, the residual component _π_ RES learns to effectively compensate for domain gaps and teleoperation biases while preserving the foundational skills inherent in _π_ GMT. 

## VI. EXPERIMENTS 

In the experimental section, we systematically investigate two core questions regarding robust general motion tracking and teleoperation to provide a mechanistic understanding. 

|**Category**|**Observation Term**|**Noise**|
|---|---|---|
||reference joint position<br>reference joint velocity<br>anchor orientation (robot frame)<br>_U_(_−_|–<br>–<br>0_._05_,_ 0_._05)|
|Prop.|robot base angular velocity<br>_U_(<br>robot joint position<br>_U_(_−_<br>robot joint velocity<br>_U_(<br>last action|_−_0_._2_,_ 0_._2)<br>0_._01_,_ 0_._01)<br>_−_0_._5_,_ 0_._5)<br>–|
||anchor position (robot frame)<br>body position (robot frame)|–<br>–|
|Priv.|body orientation (robot frame)<br>robot base linear velocity|–<br>–|
||reference base linear velocity|–|


**TABLE II. Observation terms and noises used during policy training.** The actor uses the _Prop_ observation stack with a 5-step history, while the critic uses the full set of observations including _Prop_ and _Priv_ terms with current step. 

- 1) **How to train a robust general motion tracker for teleoperation-oriented tasks?** 

- 2) **Why do General Motion Trackers with saturated simulation metrics often underperform in real-world teleoperation, and how to efficiently adapt them using minimal teleoperation data without compromising general tracking robustness?** 

_A. Training Setting and Evaluation System_ 

_1)_ **_Training Setting_** _:_ Our policies are trained using the Isaac Lab [27] framework on eight NVIDIA A100 GPUs over approximately 48 hours. To achieve efficient training, we leverage massive parallelism by instantiating 30,000 environments per GPU. The policies are parameterized by MLPs with hidden layers [1024,1024,512,256] and ELU activations [3]. 

_2)_ **_Evaluation Metrics and Benchmark_** _:_ We evaluate performance along two axes: tracking fidelity and robustness. Since mobile manipulation and teleoperation require faithful reproduction of the operator’s spatial displacement, we report all tracking metrics in the global (world) frame. To reflect long-duration usability, we additionally measure robustness via success rate and average steps per episode. Concretely, our metrics include: (i) tracking fidelity—global anchor (torso) position error _EAP_ , anchor linear velocity error _EAV_ , body position error _EBP_ , body linear velocity error _EBV_ , and end-effector (EEF) position error _EEP_ ; and (ii) robustness— success rate and average episode length (with maximum 500). 

We benchmark in the MuJoCo physics engine [34] for simto-sim evaluation using the _Online Videos_ subset of MotionX [21] as an OOD test set. For a physically plausible benchmark, we curate _Motion-X-Sub_ by selecting sequences longer than 10 s with maximum root height _≥_ 0 _._ 6 m, filtering motions that require environmental support (e.g., sitting/swimming) or are excessively challenging. _Motion-X-Sub_ contains 633 sequences with an average duration of 19.04 s, 

|**Reward Term**|**Weight**|**Parameters**|
|---|---|---|
|_Tracking rewards_|||
|Motion global anchor position|+0.5|std=0.3|
|Motion global anchor orientation|+0.5|std=0.4|
|Motion body position|+1.0|std=0.3|
|Motion body orientation|+1.0|std=0.4|
|Motion body linear velocity|+1.5|std=1.0|
|Motion body angular velocity|+1.5|std=3.14|
|Motion anchor linear velocity|+1.0|std=1.0|
|_Teleoperation rewards_|||
|Motion global body position|+1.0|std=0.5|
|Motion global VR|+0.5|std=0.5|
|Motion global feet position|+1.0|std=0.5|
|Motion global body orientation|+0.5|std=0.5|
|Motion global body angular velocity|+0.5|std=3.14|
|Motion global body linear velocity|+0.5|std=1.0|
|_Penalty terms_|||
|Undesired contacts|-0.05|threshold=1.0N|
|Action rate L2|-0.1|–|
|Joint limit|-10.0|–|
|Joint acceleration|-2.5e-7|–|
|Joint torque|-1e-5|–|


**TABLE III. Reward terms and weights.** Our design combines the tracking objectives from BeyondMimic [20] with additional global teleoperation-oriented terms inspired by prior motion-imitation systems such as ASAP [8] and KungfuBot [39], while regularizing contacts, action smoothness, and joint limits/torques to improve stability and deployability. 

totaling _∼_ 3.35 hours of diverse motions. 

## _B. Design Principles for Robust General Motion Tracking_ 

To answer question 1), we conduct extensive comparative analyses across three dimensions: data sources, reward design, and training paradigms. Based on these comprehensive evaluations, we distill a set of key design principles for developing trackers that are both precise and robust. 

_1)_ **_Ablation on Data Source_** _:_ To isolate the effect of data diversity, we construct three motion corpora with the same budget of 1M frames: _1-Source_ (AMASS [25]), _3-Sources_ (AMASS + OMOMO [17] + built in-house inertial MoCap data), and _5-Sources_ (further adding built in-house optical MoCap and GENMO-generated motions [18]). All models are trained for the same iterations in identical configurations. 

As shown in Fig. 3a, increasing source diversity yields consistent gains across both tracking fidelity and robustness metrics. Since evaluation is performed on an OOD test set, these improvements also indicate substantially better generalization from more heterogeneous motion distributions. 


(b) Quantitative Ablation of Reward Design and Training Paradigms Alongside Benchmarking with Prior Work. 

Fig. 3: **Quantitative Comparison and Ablation Studies of General Motion Tracking.** The radar charts illustrate five core metrics characterizing tracking fidelity, while the bar charts depict robustness in terms of Success Rate and Average Steps per Episode. Fig 3a compares multi-source versus single-source data distributions. Fig 3b evaluates our proposed variants (Pure RL + world frame reward, Pure RL + robot frame reward, and DAgger + world frame reward) against baselines GMT [2] and TWIST [44]. 


Fig. 4: **Qualitative Comparison on High Dynamic Motion.** From left to right are our model, TWIST, and GMT. Our model achieves substantial ground clearance at the reference apex, whereas baselines (i.e., TWIST and GMT) struggle to capture high-acceleration explosive movements. 

_2)_ **_Ablation on Reward Design_** _:_ BeyondMimic [20] achieves strong single-motion tracking by emphasizing tracking objectives largely computed in the robot frame. However, teleoperation-oriented mobile manipulation places stricter requirements on global tracking: purely local rewards can accu- 

mulate drift over long-horizon locomotion. We therefore study the impact of augmenting ego-centric tracking with worldframe objectives that constrain global pose and motion. 

Figure 3b shows that adding world-frame tracking substantially reduces long-horizon drift, reflected by lower global tracking errors, and improves stability by higher success rates and longer episode lengths. We attribute the robustness gains to two coupled effects: (i) improved acquisition of dynamic locomotion patterns (e.g., walking, running and jumping), and (ii) an explicit incentive to maintain global trajectories, which discourages stumbles and falls that would otherwise disrupt target positions and velocities in world frame. 

_3)_ **_Ablation on Training Paradigm_** _:_ We compare two common paradigms for motion tracking: pure RL and DAggerstyle distillation [31]. Our comparative evaluation demonstrates that pure RL consistently outperforms the distilled policy across several key dimensions. 

As shown in Fig. 3b, pure RL outperforms the distilled policy in tracking fidelity—precisely the metric of our primary concern. Furthermore, pure RL exhibits higher success rates and more average steps per episode, indicating enhanced robustness. These results highlight a practical difficulty in distillation for motion tracking: transferring a teacher’s fine-grained global position/velocity tracking behavior into a deployable student without loss remains non-trivial. In contrast, when paired with sufficient data diversity and teleoperation-oriented rewards, pure RL directly optimizes long-horizon objectives and yields superior global tracking and stability, ultimately surpassing distillation-based alternatives in our setting. 

_4)_ **_Comparison with Representative Baseline_** _:_ Finally, we compare our final tracker against prior representative methods, including GMT [2] and TWIST [44]. As shown in Fig. 3b, our approach improves both tracking fidelity and robustness across all reported metrics, with particularly large gains in global position tracking. Qualitatively, the improvement is most apparent on high-dynamic segments: whereas prior methods often stumble or terminate during aggressive transitions, our policy maintains stable contacts and smooth state evolution. We include representative examples in Fig. 4 to illustrate the resulting gains in tracking accuracy and motion quality. 

## _C. Bridging the Sim-to-Real Gap via Rapid Adaptation_ 

We observe that while the general motion tracking policy achieves saturated metrics in simulation, its performance significantly degrades during real-world teleoperation. This discrepancy highlights a persistent sim-to-real gap. In this section, we analyze the sources of this gap and evaluate various strategies for rapid adaptation to various teleoperation scenarios to seek the answer to question 2). 

_1)_ **_Analysis of the Teleoperation Sim-to-Real Gap_** _:_ Our evidence indicates that failures are driven less by limited motion diversity than by a teleoperation interface gap. Specifically: 

- **System latency.** End-to-end delays accumulate across sensing, transmission, processing, and control execution. According to measurements, VR streaming introduces approximately 400 ms latency, which creates a temporal 

mismatch between the operator’s intent and robot’s current state, leading to out-of-sync tracking and instability. 

_•_ **Noise and Jitter:** Real teleoperation streams exhibit packet loss, and sensor noise that are typically undermodeled in simulation. These artifacts introduce nonsmooth perturbations in the reference trajectory, triggering motor safety limits or destabilize contact transitions. A key empirical observation is that motion coverage is not the bottleneck. In simulation, the same tracker generalizes well to highly complex OOD motions; however, on robot we observe frequent stumbling even on fundamental gaits that are well represented in the training corpus. This contrast indicates that reliable deployment is primarily limited by teleoperationspecific interface effects (latency, noise, and hardware execution artifacts), rather than a lack of training diversity. 

**TABLE IV. Evaluation results on** **_Motion-X-Sub_** . _↓_ denotes lower is better, _↑_ denotes higher is better. 

|**Configuration**|_EAP_ **(m)** _↓_|_EBP_ **(m)** _↓_|_EEP_ **(m)** _↓_|**Success Rate** _↑_|
|---|---|---|---|---|
|Base Model|0.8242|0.8471|0.8578|**77.88%**|
|Fine-tune|2.7587|2.7387|2.6950|40.60%|
|Continual|0.8571|0.8788|0.8870|78.36%|
|Adapter (R)|0.8194|0.8412|**0.8513**|77.25%|
|**Adapter (W)**|**0.8165**|**0.8406**|0.8520|77.25%|


**TABLE V. Evaluation results on VR dataset** . 

|**Configuration**|_EAP_ **(m)** _↓_|_EBP_ **(m)** _↓_|_EEP_ **(m)** _↓_|**Success Rate** _↑_|
|---|---|---|---|---|
|Base Model|2.9352|2.9353|2.9363|**100.00%**|
|Fine-tune|1.4106|1.4043|1.3998|92.00%|
|Adapter (R)|1.5278|1.5370|1.5436|96.00%|
|Adapter (W)|**1.1940**|**1.1961**|**1.2002**|**100.00%**|
|Continual|1.7248|1.7272|1.7294|**100.00%**|


**TABLE VI. Data scaling analysis on VR dataset** . 

|**Configuration**|_EAP_ **(m)** _↓_|_EBP_ **(m)** _↓_|_EEP_ **(m)** _↓_|**Success Rate** _↑_|
|---|---|---|---|---|
|Adapter (3 min)|2.8254|2.8257|2.8269|**100.00%**|
|Adapter (15 min)|1.5686|1.5674|1.5651|96.00%|
|**Adapter (30 min)**|**1.1940**|**1.1961**|**1.2002**|**100.00%**|
|FLD Augmentation|2.9298|2.9298|2.9307|**100.00%**|


_2)_ **_Exploration of Strategies for Rapid Adaptation_** _:_ To bridge the interface gap, we collected 30 minutes of VR teleoperation data and explored three adaptation strategies based on the same pre-trained general motion tracker (GMT): 

- **Fine-tuning** : Continue optimizing _πGMT_ exclusively on the teleoperation dataset. 

- **Continual Learning** : Mix the teleoperation data with the original motion corpus and continue training. 

_•_ **Residual Adapter** : Sec. V, Reward in world frame: Adaptor (W), and reward in robot frmae: Adaptor (R). _a) Preserving Generalist Capabilities:_ We first evaluate whether adaptation compromises general tracking on _MotionX-Sub_ . As reported in Table IV, Residual Adapter yields the strongest overall tracking and robustness metrics, indicating that interface-specific corrections can be injected without degrading the general tracker’s broad coverage. 

_b) Real-Robot Teleoperation Performance:_ We further evaluated these strategies on a 10-minute held-out real-robot teleoperation test set. As shown in Table V, the Residual Adapter consistently outperforms all baselines. Fine-tuning yields only marginal position-tracking gains but substantially reduces robustness, suggesting overfitting to the small adaptation set. Continual Learning provides negligible improvement, likely because the limited real data is dominated by the large general-motion corpus (gradient dilution). Overall, the Residual Adapter enables rapid, data-efficient adaptation while preserving the base policy’s general performance. 

## _3)_ **_Further Exploration of the Residual Adapter_** _:_ 

_a) Data Scaling:_ To investigate the data requirements for residual adaptation, we vary the adaptation dataset sizes: 3, 15, and 30 minutes. Experimental results indicate that 3 minutes of data is insufficient to produce meaningful improvement. Gains emerge at 15 minutes and further increase at 30 minutes, suggesting that a modest amount of high-quality teleoperation data can efficiently bridge the sim-to-real gap. 

_b) Representative-based data augmentation:_ As an alternative to mitigate long-horizon locomotion sparsity, we explored structured motion synthesis with Fourier Latent Dynamics (FLD) [15]. We train FLD on 3 minutes of periodic teleoperated locomotion and synthesize _∼_ 10 hours of trajectories via latent-space sampling, then train trackers with and without FLD augmentation under matched settings and distill both into the residual policy for controlled comparison. FLD improves interpolation within the periodic manifold (e.g., unseen gait frequencies and step lengths), but yields only marginal gains on the held-out teleoperation test: failures on complex OOD motions remain. Overall, in our setting, interface-level adaptation is more effective for deployment robustness than expanding periodic locomotion data. 

## VII. CONCLUSIONS AND LIMITATIONS 

_a) Conclusions:_ We presented MOSAIC, a humanoid motion tracking and teleoperation system that combines a general motion tracker with a data-efficient residual interface adaptor. Our study yields three key insights: ( **A** ) after simulation tracking metrics saturate, real-robot failures are driven mainly by interface and dynamics gaps (e.g., latency, estimation bias, and teleoperation noise), rather than insufficient motion diversity; ( **B** ) merging a small amount of teleoperation data into large-scale training can cause forgetting or gradient dilution, whereas residual adaptation injects new capability as incremental correction on a frozen backbone and is the most stable and sample-efficient in our setting; ( **C** ) periodicmotion augmentation (e.g., FLD) improves motion coverage but does not address interface-induced system errors, yielding smaller deployment gains than direct adaptation. Overall, separating general tracking from teleoperation-specific correction enables minute-scale stable teleoperation while preserving broad motion generality and supporting rapid adaptation to new interfaces with minimal additional data. 

_b) Limitations:_ MOSAIC does not eliminate dependence on reliable low-latency sensing and state estimation, and 

residual adaptation primarily targets interface shifts rather than all sources of sim-to-real mismatch. 

## REFERENCES 

- [1] Joao Pedro Araujo, Yanjie Ze, Pei Xu, Jiajun Wu, and C. Karen Liu. Retargeting matters: General motion retargeting for humanoid motion tracking. _arXiv preprint arXiv:2510.02252_ , 2025. 

- [2] Zixuan Chen, Mazeyu Ji, Xuxin Cheng, Xuanbin Peng, Xue Bin Peng, and Xiaolong Wang. Gmt: General motion tracking for humanoid whole-body control. _arXiv preprint arXiv:2506.14770_ , 2025. 

- [3] Djork-Arn´e Clevert, Thomas Unterthiner, and Sepp Hochreiter. Fast and accurate deep network learning by exponential linear units (elus). _arXiv preprint arXiv:1511.07289_ , 4(5):11, 2015. 

- [4] Zipeng Fu, Qingqing Zhao, Qi Wu, Gordon Wetzstein, and Chelsea Finn. Humanplus: Humanoid shadowing and imitation from humans. _arXiv preprint arXiv:2406.10454_ , 2024. 

- [5] Jinrui Han, Weiji Xie, Jiakun Zheng, Jiyuan Shi, Weinan Zhang, Ting Xiao, and Chenjia Bai. Kungfubot2: Learning versatile motion skills for humanoid whole-body control. _arXiv preprint arXiv:2509.16638_ , 2025. 

- [6] Junzhe He, Chong Zhang, Fabian Jenelten, Ruben Grandia, Moritz B¨acher, and Marco Hutter. Attentionbased map encoding for learning generalized legged locomotion. _Science Robotics_ , 10(105):eadv3604, 2025. 

- [7] Tairan He, Zhengyi Luo, Xialin He, Wenli Xiao, Chong Zhang, Weinan Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. Omnih2o: Universal and dexterous humanto-humanoid whole-body teleoperation and learning. 2024. 

- [8] Tairan He, Jiawei Gao, Wenli Xiao, Yuanhang Zhang, Zi Wang, Jiashun Wang, Zhengyi Luo, Guanqi He, Nikhil Sobanbab, Chaoyi Pan, et al. Asap: Aligning simulation and real-world physics for learning agile humanoid whole-body skills. _arXiv preprint arXiv:2502.01143_ , 2025. 

- [9] Jemin Hwangbo, Joonho Lee, Alexey Dosovitskiy, Dario Bellicoso, Vassilios Tsounis, Vladlen Koltun, and Marco Hutter. Learning agile and dynamic motor skills for legged robots. _Science Robotics_ , 4(26):eaau5872, 2019. 

- [10] IO-AI.Tech. Io inertial mocap suit. https://io-ai.tech/en/ mocap/, 2026. Accessed: 2026-02-07. 

- [11] Mazeyu Ji, Xuanbin Peng, Fangchen Liu, Jialong Li, Ge Yang, Xuxin Cheng, and Xiaolong Wang. Exbody2: Advanced expressive humanoid whole-body control. _arXiv preprint arXiv:2412.13196_ , 2024. 

- [12] Tobias Johannink, Shikhar Bahl, Ashvin Nair, Jianlan Luo, Avinash Kumar, Matthias Loskyll, Juan Aparicio Ojea, Eugen Solowjow, and Sergey Levine. Residual reinforcement learning for robot control. In _2019 international conference on robotics and automation (ICRA)_ , pages 6023–6029. IEEE, 2019. 

- [13] Ashish Kumar, Zipeng Fu, Deepak Pathak, and Jitendra 

Malik. Rma: Rapid motor adaptation for legged robots. _Robotics: Science and Systems XVII_ , 2021. 

- [14] lcm-proj contributors. LCM: Lightweight communications and marshalling. https://github.com/lcm-proj/lcm, 2026. GitHub repository, accessed 2026-02-07. 

- [15] Chenhao Li, Elijah Stanger-Jones, Steve Heim, and Sangbae Kim. Fld: Fourier latent dynamics for structured motion representation and learning. _arXiv preprint arXiv:2402.13820_ , 2024. 

- [16] Jialong Li, Xuxin Cheng, Tianshu Huang, Shiqi Yang, Rizhao Qiu, and Xiaolong Wang. Amo: Adaptive motion optimization for hyper-dexterous humanoid whole-body control. _Robotics: Science and Systems 2025_ , 2025. 

- [17] Jiaman Li, Jiajun Wu, and C Karen Liu. Object motion guided human motion synthesis. _ACM Transactions on Graphics (TOG)_ , 42(6):1–11, 2023. 

- [18] Jiefeng Li, Jinkun Cao, Haotian Zhang, Davis Rempe, Jan Kautz, Umar Iqbal, and Ye Yuan. Genmo: A generalist model for human motion. _arXiv preprint arXiv:2505.01425_ , 2025. 

- [19] Yixuan Li, Yutang Lin, Jieming Cui, Tengyu Liu, Wei Liang, Yixin Zhu, and Siyuan Huang. Clone: Closed-loop whole-body humanoid teleoperation for long-horizon tasks, 2025. 

- [20] Qiayuan Liao, Takara E Truong, Xiaoyu Huang, Yuman Gao, Guy Tevet, Koushil Sreenath, and C Karen Liu. Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion. _arXiv preprint arXiv:2508.08241_ , 2025. 

- [21] Jing Lin, Ailing Zeng, Shunlin Lu, Yuanhao Cai, Ruimao Zhang, Haoqian Wang, and Lei Zhang. Motion-x: A large-scale 3d expressive whole-body human motion dataset. _Advances in Neural Information Processing Systems_ , 36:25268–25280, 2023. 

- [22] Kai Lu, Kim Tien Ly, William Hebberd, Kaichen Zhou, Ioannis Havoutis, and Andrew Markham. Learning generalizable manipulation policy with adapter-based parameter fine-tuning. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 13510–13517. IEEE, 2024. 

- [23] Zhengyi Luo, Jinkun Cao, Kris Kitani, Weipeng Xu, et al. Perpetual humanoid control for real-time simulated avatars. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 10895–10904, 2023. 

- [24] Zhengyi Luo, Ye Yuan, Tingwu Wang, Chenran Li, Sirui Chen, Fernando Casta˜neda, Zi-Ang Cao, Jiefeng Li, David Minor, Qingwei Ben, et al. Sonic: Supersizing motion tracking for natural humanoid whole-body control. _arXiv preprint arXiv:2511.07820_ , 2025. 

- [25] Naureen Mahmood, Nima Ghorbani, Nikolaus F Troje, Gerard Pons-Moll, and Michael J Black. Amass: Archive of motion capture as surface shapes. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 5442–5451, 2019. 

- [26] Fabian Mentzer, David Minnen, Eirikur Agustsson, and 

   - Michael Tschannen. Finite scalar quantization: Vq-vae made simple. _arXiv preprint arXiv:2309.15505_ , 2023. 

- [27] Mayank Mittal, Pascal Roth, James Tigue, Antoine Richard, Octi Zhang, Peter Du, Antonio Serrano-Mu˜noz, Xinjie Yao, Ren´e Zurbr¨ugg, Nikita Rudin, Lukasz Wawrzyniak, Milad Rakhsha, Alain Denzler, Eric Heiden, Ales Borovicka, Ossama Ahmed, Iretiayo Akinola, Abrar Anwar, Mark T. Carlson, Ji Yuan Feng, Animesh Garg, Renato Gasoto, Lionel Gulich, Yijie Guo, M. Gussert, Alex Hansen, Mihir Kulkarni, Chenran Li, Wei Liu, Viktor Makoviychuk, Grzegorz Malczyk, Hammad Mazhar, Masoud Moghani, Adithyavairavan Murali, Michael Noseworthy, Alexander Poddubny, Nathan Ratliff, Welf Rehberg, Clemens Schwarke, Ritvik Singh, James Latham Smith, Bingjie Tang, Ruchik Thaker, Matthew Trepte, Karl Van Wyk, Fangzhou Yu, Alex Millane, Vikram Ramasamy, Remo Steiner, Sangeeta Subramanian, Clemens Volk, CY Chen, Neel Jawale, Ashwin Varghese Kuruttukulam, Michael A. Lin, Ajay Mandlekar, Karsten Patzwaldt, John Welsh, Huihua Zhao, Fatima Anes, Jean-Francois Lafleche, Nicolas Mo¨enneLoccoz, Soowan Park, Rob Stepinski, Dirk Van Gelder, Chris Amevor, Jan Carius, Jumyung Chang, Anka He Chen, Pablo de Heras Ciechomski, Gilles Daviet, Mohammad Mohajerani, Julia von Muralt, Viktor Reutskyy, Michael Sauter, Simon Schirm, Eric L. Shi, Pierre Terdiman, Kenny Vilella, Tobias Widmer, Gordon Yeoman, Tiffany Chen, Sergey Grizan, Cathy Li, Lotus Li, Connor Smith, Rafael Wiltz, Kostas Alexis, Yan Chang, David Chu, Linxi ”Jim” Fan, Farbod Farshidian, Ankur Handa, Spencer Huang, Marco Hutter, Yashraj Narang, Soha Pouya, Shiwei Sheng, Yuke Zhu, Miles Macklin, Adam Moravanszky, Philipp Reist, Yunrong Guo, David Hoeller, and Gavriel State. Isaac lab: A gpuaccelerated simulation framework for multi-modal robot learning. _arXiv preprint arXiv:2511.04831_ , 2025. URL https://arxiv.org/abs/2511.04831. 

- [28] Noitom Ltd. Perception neuron: Inertial motion capture system, 2025. URL https://www.noitom.com/. Axis Studio Software and Perception Neuron Hardware. 

- [29] Xue Bin Peng, Pieter Abbeel, Sergey Levine, and Michiel Van de Panne. Deepmimic: Example-guided deep reinforcement learning of physics-based character skills. _ACM Transactions On Graphics (TOG)_ , 37(4):1–14, 2018. 

- [30] PNDbotics. Pnd adam humanoid robot. https://www. pndbotics.com/humanoid, 2026. Accessed: 2026-02-07. 

- [31] St´ephane Ross, Geoffrey Gordon, and Drew Bagnell. A reduction of imitation learning and structured prediction to no-regret online learning. In _Proceedings of the fourteenth international conference on artificial intelligence and statistics_ , pages 627–635. JMLR Workshop and Conference Proceedings, 2011. 

- [32] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [33] Clemens Schwarke, Mayank Mittal, Nikita Rudin, David Hoeller, and Marco Hutter. Rsl-rl: A learning library for robotics research. _arXiv preprint arXiv:2509.10771_ , 2025. 

- [34] Emanuel Todorov, Tom Erez, and Yuval Tassa. Mujoco: A physics engine for model-based control. In _2012 IEEE/RSJ international conference on intelligent robots and systems_ , pages 5026–5033. IEEE, 2012. 

- [35] Unitree Robotics. Unitree g1 humanoid robot. https: //www.unitree.com/g1, 2026. Accessed: 2026-02-07. 

- [36] Unitree Robotics. Unitree h1 humanoid robot. https: //www.unitree.com/h1, 2026. Accessed: 2026-02-07. 

- [37] Aaron Van Den Oord, Oriol Vinyals, et al. Neural discrete representation learning. _Advances in neural information processing systems_ , 30, 2017. 

- [38] Vicon Motion Systems Ltd. Vicon nexus: Optical motion capture system, 2024. URL https://www.vicon.com/ software/nexus/. Commercial Optical Motion Capture Solution. 

- [39] Weiji Xie, Jinrui Han, Jiakun Zheng, Huanyu Li, Xinzhe Liu, Jiyuan Shi, Weinan Zhang, Chenjia Bai, and Xuelong Li. Kungfubot: Physics-based humanoid wholebody control for learning highly-dynamic skills. _Advances in Neural Information Processing Systems_ , 2025. 

- [40] Omry Yadan. Hydra - a framework for elegantly configuring complex applications. Github, 2019. URL https://github.com/facebookresearch/hydra. 

- [41] Kangning Yin, Weishuai Zeng, Ke Fan, Minyue Dai, Zirui Wang, Qiang Zhang, Zheng Tian, Jingbo Wang, Jiangmiao Pang, and Weinan Zhang. Unitracker: Learning universal whole-body motion tracker for humanoid robots. _arXiv preprint arXiv:2507.07356_ , 2025. 

- [42] Mingqi Yuan, Tao Yu, Wenqi Ge, Xiuyong Yao, Dapeng Li, Huijiang Wang, Jiayu Chen, Bo Li, Wei Zhang, Wenjun Zeng, et al. A survey of behavior foundation model: Next-generation whole-body control system of humanoid robots. _IEEE transactions on pattern analysis and machine intelligence_ , 2025. 

- [43] Yanjie Ze, Jo˜ao Pedro Ara´ujo, Jiajun Wu, and C. Karen Liu. Gmr: General motion retargeting, 2025. URL https: //github.com/YanjieZe/GMR. GitHub repository. 

- [44] Yanjie Ze, Zixuan Chen, Joao Pedro Ara´ujo, Zi-ang Cao, Xue Bin Peng, Jiajun Wu, and C Karen Liu. Twist: Teleoperated whole-body imitation system. _arXiv preprint arXiv:2505.02833_ , 2025. 

- [45] Yanjie Ze, Siheng Zhao, Weizhuo Wang, Angjoo Kanazawa, Rocky Duan, Pieter Abbeel, Guanya Shi, Jiajun Wu, and C Karen Liu. Twist2: Scalable, portable, and holistic humanoid data collection system. _arXiv preprint arXiv:2511.02832_ , 2025. 

- [46] Weishuai Zeng, Shunlin Lu, Kangning Yin, Xiaojie Niu, Minyue Dai, Jingbo Wang, and Jiangmiao Pang. Behavior foundation model for humanoid robots. _arXiv preprint arXiv:2509.13780_ , 2025. 

- [47] Zhikai Zhang, Jun Guo, Chao Chen, Jilong Wang, Chenghuai Lin, Yunrui Lian, Han Xue, Zhenrong Wang, 

DATASET DETAILS 

Maoqi Liu, Jiangran Lyu, et al. Track any motions under any disturbances. _arXiv preprint arXiv:2509.13833_ , 2025. 

- [48] Siheng Zhao, Yanjie Ze, Yue Wang, C Karen Liu, Pieter Abbeel, Guanya Shi, and Rocky Duan. Resmimic: From general motion tracking to humanoid whole-body loco-manipulation via residual learning. _arXiv preprint arXiv:2510.05070_ , 2025. 

- [49] Peng Li Zihan Zhuang, Yi Dong. A plug-and-play deploy framework for robots. just deploy, just do., 2025. URL https://github.com/HansZ8/RoboJuDo. 

## APPENDIX 

## _A. Dataset Sources_ 

_a) Multi-source motion corpus.:_ We train and evaluate MOSAIC using a heterogeneous motion corpus that combines large-scale public datasets, in-house motion capture, and curated synthetic motions. Fig S1 shows some randomly sampled motions. **Public corpora** include AMASS [25] and OMOMO [17], totaling 51 hours of diverse human motions. In-house captures consist of (i) **optical MoCap** recordings: we collected 6 hours in total and retained 3.1 hours after strict quality control (e.g., removing marker swaps, severe occlusion, and inconsistent contacts), and (ii) **inertial MoCap** recordings totaling 7 hours. **Generated motions** are obtained via GENMO [18]: we synthesized roughly 4 hours of motions and manually curated 2.2 hours of high-quality clips for training. Finally, for **interface adaptation** and evaluation, we collected teleoperation demonstrations from two distinct interfaces, each providing approximately 0.5 hours of data. 

_b) Different interface between training and deployment.:_ Importantly, the 7-hour inertial MoCap dataset used for training the general motion tracker is captured with a different commercial suit than the device used in our final teleoperation tests (training: inertial MoCap suit from IO-AI [10].Tech; testing: inertial MoCap suit from Noitom.Tech [28]). This intentional device mismatch induces realistic interface-specific latency, noise, and kinematic bias, and motivates our residual adaptation module, which injects interface corrections without overwriting the generalist tracking capability learned from the multi-source motion bank. 

## _B. Data Processing_ 

- _1) Built-in House Data:_ 

_a)_ **_Optical Motion Capture Pipeline._** _:_ We developed a comprehensive pipeline to transform raw optical motion capture data into standardized formats for robot learning. The workflow is categorized into four main stages: 

- 1) **Data Acquisition and Pre-processing:** We utilize the Vicon Nexus [38] system to capture human motions with a 39-marker setup at a sampling rate of 100 Hz.. The specific marker placement is illustrated in Figure S3. Each captured sequence is paired with a corresponding natural language description, same as the prompts using for motion generation. The raw trajectories undergo a rigorous pre-processing phase, including automated segment labeling followed by manual correction, gap filling for occluded markers, and low-pass filtering to eliminate high-frequency noise. The refined data are exported in the .c3d format. 

- 2) **Human Motion Reconstruction and Quality Control:** To convert marker clouds into parametric human poses, we employ Mosh++ to generate .pkl files compatible with the AMASS framework. To ensure data fidelity, we 


Fig. S1: **Randomly Sampled Motions From the Motion Dataset.** Each tile visualizes a motion frame extracted at random time indices across different motions, illustrating the diversity of the motion dataset. 


Fig. S2: **Schematic of the Full-body Optical Marker Configuration.** To ensure high precision and motion fidelity during data acquisition, we adopt a comprehensive setup consisting of 39 reflective markers. 

perform a manual quality inspection using a MuJoCobased replay script [34]. Any sequences exhibiting physical inconsistencies, such as joint jitters or unnatural discontinuities, are strictly excluded. The validated data are subsequently converted into .npz format. 

- 3) **Motion Retargeting:** The validated human motions are retargeted to the Unitree G1 humanoid robot [35] using the GMR [43] framework. This process maps human kinematics onto the G1’s degrees of freedom (DoF), producing robot-specific pose sequences stored in .pkl format. 

- 4) **Final Formatting and Standardization:** In the final stage, the retargeted motion sequences in .pkl format are converted to .csv and subsequently transformed into the final .npz format using the BeyondMimic [20] processing suite to meet the requirements of the training framework. 

_b)_ **_Inertial Motion Capture Pipeline._** _:_ In addition to optical methods, we employ a high-fidelity inertial motion capture pipeline to expand our dataset. The workflow is structured as follows: 

- 1) **Data Acquisition and Hardware Configuration:** We utilize the IO-AI [10] full-body inertial motion capture system, which comprises 15 high-precision IMU sensors. To capture fine-grained manipulations and full-body coordination, the sensors are distributed with 9 on the upper body and 6 on the lower body, operating at a sampling frequency of 120 Hz. Raw data are initially captured onto local portable storage and subsequently uploaded asynchronously. This protocol effectively eliminates packet loss and temporal drift typically associated with wireless transmission, ensuring the integrity of longduration motion sequences. 

- 2) **Standardized Data Management:** Data collection is managed through a standardized platform where task specifications and metadata are pre-defined. During acquisition, relevant task information is automatically bound to the motion sequences. This automated metadata integration reduces manual labeling requirements while enhancing data consistency and traceability across largescale collection sessions. 

- 3) **Downstream Processing and Standardization:** The acquired AMASS-compatible sequences are processed following the same downstream pipeline as the optical data. This involves retargeting human kinematics to the Unitree G1 robot via the GMR [43] framework, followed by final standardization into the .npz format using the BeyondMimic [20] suite. 

_2) Public Motions:_ Our public-motion corpus is built from the AMASS [25] and OMOMO [17] datasets, which we download directly from their official project pages. We treat these datasets identically to our in-house captures: after acquisition, all sequences are retargeted to our robot kinematic model and processed through the same standardization pipeline as the built-in house data. Concretely, we unify coordinate conventions and units, align initial poses to a consistent canonical configuration (e.g., root orientation and heading), and apply the same representation/format conversion required by our training interface (e.g., robot-space joint trajectories and body kinematics at a fixed rate). As a result, public and in-house motions share a single, consistent on-robot format and can be mixed seamlessly during training and evaluation. 


Fig. S3: **Schematic of the Full-body Inertial Sensors Configuration.** To ensure high precision and motion fidelity during data acquisition, we utilize a comprehensive setup consisting of 15 IMU sensors, which operate in coordination with a VR headset and handheld controllers. 

_3) Generated Motions:_ To augment motion diversity in a controllable manner, we also construct a synthetic motion set using a text-to-motion pipeline. First, we use an LLM (ChatGPT) to generate text prompts spanning seven categories: (i) static poses, (ii) sports/exercises, (iii) running, (iv) daily activities, (v) martial arts, (vi) dancing, and (vii) walking. All prompts explicitly constrain motions to be planar (flat-ground behaviors) and require a duration of at least 10 s. Second, we feed these prompts to GENMO [18]’s text-to-motion model to synthesize AMASS-format motion sequences. Third, we retarget the synthesized motions into the robot-space representation using GMR, and apply the same coordinate normalization and initialization alignment used for real MoCap data (e.g., consistent root frame conventions and initial pose alignment). Finally, we manually curate the generated set to remove low-quality sequences, including motions with severe selfcollisions, discontinuities, or physically implausible transitions. After curation, we retain approximately 800 high-quality motion clips for training. 

## _C. Motion Representation and Sampling Strategy_ 

_a) Motion Representation.:_ Each motion clip is stored as an .npz file containing a fixed set of tensors at a common frame rate fps (50 Hz in our training). The motion loader reads the following fields: joint positions/velocities and body kinematics in world frame for a selected set of bodies. The representation is already in the robot joint space, and thus directly matches the policy’s tracking targets and the simulator’s state. 

To ensure fast training throughput, we preload all motion files into contiguous tensors. For motion _m_ , we record its length _Lm_ and maintain a cumulative offset _Om_ so that any per-motion frame index can be mapped to a global index: 


At runtime, batched queries are served by indexed gathers into these contiguous tensors, eliminating per-step file I/O and enabling high-throughput sampling from large motion corpora. 

We additionally support multi-GPU sharding at load time, which deterministically selects a disjoint subset of motion files per rank, reducing duplicates and memory overhead in distributed training. 

_b) Two-Level Adaptive Resampling.:_ Our resampling operates at two levels: 

- 1) **Motion-level assignment:** periodically map each environment to a motion index (which clip is currently tracked). 

- 2) **Within-motion time sampling:** when an environment resets (or reaches the end of a clip), sample a time step inside that motion using failure-aware bin probabilities. 

Both mechanisms are implemented inside the command class, which serves the tracking command by gathering a fixedhorizon future window. 

_1) Fixed-horizon window sampling:_ At every step, the policy receives a fixed-horizon reference window of length _H_ frames (in our setting, _H_ = 1). Given the environment’s current motion index _me_ and time step _te_ , we gather frames _{te, te_ + 1 _, . . . , te_ + _H −_ 1 _}_ (clamped at _Lm −_ 1) and return the flattened sequence 


which keeps the policy interface consistent across heterogeneous datasets with highly uneven clip lengths. 

_2) Motion-level sampling: difficulty × novelty × uniform:_ When remapping environments to motions, we sample motion indices from a probability vector. The distribution is a convex mixture of three terms. 

**Difficulty from motion-level failure rate.** We maintain per-motion counters: motion <u>sample counts</u> _Sm_ (times the motion is resampled), motion <u>fail counts</u> _Fm_ (times episodes terminated while tracking that motion), and compute the mean failure rate _rm_ : 


To reduce the effect of extreme early failures, we cap the rates using cap <u>beta</u> _β_ and the mean failure rate _rm_ : 


and normalize to obtain failure probability _p_ fail( _m_ ) _∝ r_ ˜ _m_ . **Novelty from assignment count.** To encourage coverage, we add a novelty term that favors less-assigned motions: 


where _Am_ is the count of assigned motions. 

**Uniform coverage.** We always include a uniform baseline _p_ uni( _m_ ) = 1 _/M_ , where _M_ is the number of all motions. The final distribution is: 


The implementation ramps _wf , wn_ from 0 to target values (the weight for failure, the weight for novelty) using a warmup + ramp schedule. This mitigates cold-start bias where early failures are ubiquitous and difficulty estimates are uninformative. 

**Active-motion pool.** When the motion database is much larger than the number of environments, we optionally sample an active pool of _K_ motions without replacement and assign them to environments approximately uniformly. This improves memory locality and ensures each selected motion receives sufficient training signal before the next remap. 

**Remap cadence.** We periodically reassign motions every interval of resampling motions so that, over training, all motions get repeated chances to be tracked. 

_a) Note on dataset-level weighting.:_ In our setting, motion-level sampling operates on a single folder of motions. Dataset-level weighting can be realized by (i) constructing the motion folder with desired per-source proportions, or (ii) extending the probability of motion sampling with per-motion weights (e.g., a scalar multiplier based on source ID). The remainder of the pipeline (warmup/ramp, novelty, and withinmotion bin sampling) applies unchanged. 

_3) Within-motion failure-aware bin resampling (EMA + kernel smoothing):_ Even with motion-level balancing, failures often concentrate in specific segments (e.g., sharp turns, contact transitions). We implement within-motion adaptive sampling following BeyondMimic [20]. 

## TRAINING DETAILS 

|**Category**|**Observation Term**|**Noise**|
|---|---|---|
||reference joint position<br>reference joint velocity<br>anchor orientation error|–<br>–<br>_U_(_−_0_._05_,_ 0_._05)|
|Prop.|robot base angular velocity<br>robot joint position|_U_(_−_0_._2_,_ 0_._2)<br>_U_(_−_0_._01_,_ 0_._01)|
||robot joint velocity<br>last action|_U_(_−_0_._5_,_ 0_._5)<br>–|
||anchor position error|–|
||body position (robot frame)|–|
|Priv.|body orientation (robot frame)<br>robot base linear velocity|–<br>–|
||reference base linear velocity|–|


**TABLE S1. Observation Terms and Noises Used During Policy Training.** The actor uses the _Prop_ observation stack with a 5-step history, while the critic uses the full set of observations including _Prop_ and _Priv_ terms at the current step. Here, the robot’s _torso link_ is defined as the _anchor_ for all coordinate transformations. Accordingly, the _anchor position error_ and _anchor orientation error_ are represented as the target reference orientation expressed in the robot’s local frame. 

## _E. Rewards_ 

The reward function consists of tracking rewards (Global and Teleop style) and penalties for regularization, as shown in Table S2. Tracking rewards are calculated using an exponential kernel: _r_ = _w ·_ exp( _−∥e∥_<sup>2</sup> _/σ_<sup>2</sup> ). 

## _F. Terminations_ 

Terminations ensure the safety and efficiency of the training process by resetting episodes that violate pre-defined constraints. Details are illustrated in Table S3. 

## _G. Domain Randomization_ 

To facilitate sim-to-real transfer, we randomize physical properties at the start of each episode and apply random pushes at random intervals of 1–3 seconds during simulation. Details are shown in Table S4. 

## _H. PPO Parameters_ 

We train all RL policies with PPO using a shared set of hyperparameters and an MLP actor–critic within the framework RSL <u>RL</u> [33]. Details are summarized in Table S5. 

## _D. Observations_ 

The observation space is divided into proprioceptive data for the actor and privileged information for the critic, as illustrated in Table S1. To enhance robustness against sensor inaccuracies, the actor processes a 5-step history of proprioceptive signals corrupted by Gaussian noise. In contrast, the critic utilizes the noise-free, ground-truth observations of the current frame to provide a more accurate value estimation during training. 

## _I. Residual Adaptor_ 

_a) Residual module architecture.:_ The residual adaptor is a lightweight MLP that maps deployable actor observations to an action-space correction. It consists of three hidden layers with widths [512 _,_ 256 _,_ 128] and ELU activations, followed by a linear output layer producing a residual action ∆ **a** _t_ . The adaptor shares the same action space as the backbone and is added to the frozen backbone action at every timestep. 

**TABLE S2. Detailed Reward Function Specifications.** All tracking rewards utilize the kernel _r_ = exp( _−_ error _/std_<sup>2</sup> ). The total reward is the weighted sum of tracking accuracy and regularization penalties. 

|**Reward Term**|**Equation**|**Weight**|**Parameters**|
|---|---|---|---|
|_Tracking rewards_||||
|Motion global anchor position|_r_<sup>anc</sup><br>pos <sup>= exp(</sup><sup>_−∥_</sup><sup>**p**</sup><sup>_p_</sup><br>_a _<sup>_−_</sup><sup>**p**</sup><sup>_g_</sup><br>_a_<sup>_∥_2</sup><br>2<sup>_/std_2)</sup>|+0.5|std=0.3|
|Motion global anchor orientation|_r_<sup>anc</sup><br>ori <sup>= exp(</sup><sup>_−dquat_(</sup><sup>**q**</sup><sup>_p_</sup><br>_a_<sup>_,_</sup><sup>**q**</sup><sup>_g_</sup><br>_a_<sup>)2</sup><sup>_/std_2)</sup>|+0.5|std=0.4|
|Motion body position|_r_<sup>body,rel</sup><br>pos<br>= exp(_−_mean_b∈B∥_**p**<sup>rel</sup><sup>_,p_</sup><br>_b_<br>_−_**p**<sup>rel</sup><sup>_,g_</sup><br>_b_<br>_∥_<sup>2</sup><br>2<sup>_/std_2)</sup>|+1.0|std=0.3|
|Motion body orientation|_r_<sup>body,rel</sup><br>ori<br>= exp(_−_mean_b∈Bdquat_(**q**<sup>rel</sup><sup>_,p_</sup><br>_b_<br>_,_**q**<sup>rel</sup><sup>_,g_</sup><br>_b_<br>)<sup>2</sup>_/std_<sup>2</sup>)|+1.0|std=0.4|
|Motion body linear velocity|_r_<sup>body</sup><br>lin<br>= exp(_−_mean_b∈B∥_**v**<sup>_p_</sup><br>_b _<sup>_−_</sup><sup>**v**</sup><sup>_g_</sup><br>_b_<sup>_∥_2</sup><br>2<sup>_/std_2)</sup>|+1.5|std=1.0|
|Motion body angular velocity|_r_<sup>body</sup><br>ang <sup>= exp(</sup><sup>_−_mean</sup>_b∈B_<sup>_∥_</sup><sup>**_ω_**</sup><sup>_p_</sup><br>_b _<sup>_−_</sup><sup>**_ω_**</sup><sup>_g_</sup><br>_b_<sup>_∥_2</sup><br>2<sup>_/std_2)</sup>|+1.5|std=3.14|
|Motion anchor linear velocity|_r_<sup>anc</sup><br>vel <sup>= exp(</sup><sup>_−∥_</sup><sup>**v**</sup><sup>_p_</sup><br>_a _<sup>_−_</sup><sup>**v**</sup><sup>_g_</sup><br>_a_<sup>_∥_2</sup><br>2<sup>_/std_2)</sup>|+1.0|std=1.0|
|_Teleoperation rewards_||||
|Motion global body position|_r_<sup>ext</sup><br>pos <sup>=</sup><sup>_w_</sup>_u_ <sup>exp(</sup><sup>_−_err</sup>_u_<sup>_/std_2) +</sup><sup>_w_</sup>_l_ <sup>exp(</sup><sup>_−_err</sup>_l_<sup>_/std_2)</sup>|+1.0|std=0.5|
|Motion global VR|_r_vr = exp(_−_mean_k∈K∥_**p**<sup>_p_</sup><br>_k _<sup>_−_</sup><sup>**p**</sup><sup>_g_</sup><br>_k_<sup>_∥_2</sup><br>2<sup>_/std_2)</sup><sup>_, K_ =</sup><sup>_{_head, hands</sup><sup>_}_</sup>|+0.5|std=0.5|
|Motion global feet position|_r_feet = exp(_−_mean_f∈F∥_**p**<sup>_p_</sup><br>_f _<sup>_−_</sup><sup>**p**</sup><sup>_g_</sup><br>_f_<sup>_∥_2</sup><br>2<sup>_/std_2)</sup><sup>_, F_ =</sup><sup>_{_ankles</sup><sup>_}_</sup>|+1.0|std=0.5|
|Motion global body orientation|_r_<sup>ext</sup><br>rot <sup>= exp(</sup><sup>_−_mean</sup>_b∈B_<sup>_d_</sup>_quat_<sup>(</sup><sup>**q**</sup><sup>_p_</sup><br>_b_<sup>_,_</sup><sup>**q**</sup><sup>_g_</sup><br>_b_<sup>)2</sup><sup>_/std_2)</sup>|+0.5|std=0.5|
|Motion global body angular velocity|_r_<sup>ext</sup><br>ang <sup>= exp(</sup><sup>_−_mean</sup>_b∈B_<sup>_∥_</sup><sup>**_ω_**</sup><sup>_p_</sup><br>_b _<sup>_−_</sup><sup>**_ω_**</sup><sup>_g_</sup><br>_b_<sup>_∥_2</sup><br>2<sup>_/std_2)</sup>|+0.5|std=3.14|
|Motion global body linear velocity|_r_<sup>ext</sup><br>lin <sup>= exp(</sup><sup>_−_mean</sup><sup>_b∈B∥_</sup><sup>**v**</sup><sup>_p_</sup><br>_b _<sup>_−_</sup><sup>**v**</sup><sup>_g_</sup><br>_b_<sup>_∥_2</sup><br>2<sup>_/std_2)</sup>|+0.5|std=1.0|
|_Penalty terms_||||
|Undesired contacts|_r_contact = <sup>�</sup><br>_c/∈{_feet, hands_}_ <sup>⊮[</sup><sup>_∥_</sup><sup>**F**</sup><sup>_c∥>_ threshold]</sup>|-0.05|threshold=1.0N|
|Action rate L2|_r_act =_∥_**a**_t −_**a**_t−_1_∥_<sup>2</sup><br>2|-0.1|–|
|Joint limit|_r_jlim = <sup>�</sup><br>_j_ <sup>⊮[</sup><sup>**q**</sup><sup>_t,j /∈_[</sup><sup>**q**min</sup><br>_j _<sup>_,_</sup><sup>**q**max</sup><br>_j_<br>]]|-10.0|–|
|Joint acceleration|_r_acc =_∥_¨**q**_t∥_<sup>2</sup><br>2|-2.5e-7|–|
|Joint torque|_r_torque =_∥_**_τ_**_t∥_<sup>2</sup><br>2|-1e-5|–|


_<u>Note: wu</u>_ <u>and</u> _<u>wl</u>_ <u>denote the weights for the upper-body and lower-body components, respectively; err</u> _u_ <u>and err</u> _l_ <u>are the corresponding tracking errors.</u> 

|**Termination Term**|**Threshold / Condition**|**Parameter**|**Randomization Range**|**Mode**|
|---|---|---|---|---|
|Motion End|Completion of the target motion sequence|Static Friction|[0_._3_,_1_._6]|Startup|
|Time Out|Reaching maximum episode length|Dynamic Friction|[0_._3_,_1_._2]|Startup|
|Anchor Pos. Error|Vertical error _|zanchor −zref| >_0_._25 m|Restitution|[0_._0_,_0_._5]|Startup|
|Anchor Ori. Error|Orientation deviation _>_0_._8 rad|Joint Default Pos|Base_±_0_._01 rad|Startup|
|EE Body Pos. Error|Vertical error _|zee −zref| >_ 0_._25 m for<br>wrists/ankles|Base CoM Offset|_x ∈±_0_._025_, y/z ∈±_0_._05<br>m|Startup|
|||Robot Push|Sampling velocity range|Interval (1-3s)|


**TABLE S3. Termination Conditions During Policy Training.** 

## **TABLE S4. Domain Randomization Configuration.** 

DEPLOYMENT DETAILS 

## _J. Real Robot Setup_ 

_a) Robot platform and low-level actuation.:_ All realrobot experiments in this paper use the Unitree G1 humanoid [35] with 29 actuated DoFs. The high-level policy runs at 50 Hz and outputs full-body joint position targets. Targets are executed by a standard joint-space PD impedance controller implemented via Isaac Lab implicit actuators, with joint-wise torque (effort) and velocity limits for safety and hardware fidelity, following the actuation setting of BeyondMimic [20]: We parameterize PD gains using a second-order system interpretation, specifying a desired closed-loop natural 

frequency ( _ωn_ ) and damping ratio ( _ζ_ ) . For each actuator group, stiffness and damping are computed from the joint armature (effective inertia) _J_ as _Kp_ = _Jωn_<sup>2</sup><sup>_,Kd_=2</sup><sup>_ζJωn,_</sup> where we set _ωn_ = 2 _π ·_ 10 Hz and _ζ_ = 2 _._ 0. This yields consistent impedance behavior across joints with different effective inertias (e.g., hip/knee vs. ankle/wrist), while retaining perjoint safety constraints through effort/velocity saturation. 

_b) Safety limits and action scaling.:_ We enforce actuatorspecific ffort limits (e.g., hips up to 88–139 Nm; ankles/waist up to 50 Nm; shoulders/elbows up to 25 Nm; wrist pitch/yaw up to 5 Nm) and velocity limits (typically 20–37 rad/s depending on joint group). To keep commanded target offsets within feasible ranges under these limits, we scale position actions 

|**PPO / Policy Parameter**|**Value**|
|---|---|
|Rollout length (per env, per update)|24|
|Learning epochs|5|
|Mini-batches per epoch|4|
|Learning rate|10<sup>_−_3</sup>|
|LR schedule|adaptive|
|desired KL|0_._01|
|Discount factor _γ_|0_._99|
|GAE parameter _λ_|0_._95|
|PPO clip ratio _ϵ_|0_._2|
|Value loss coefficient|1_._0|
|Entropy coefficient|0_._005|
|Max gradient norm|1_._0|
|Actor MLP hidden dims|[1024_,_1024_,_512_,_256]|
|Critic MLP hidden dims|[1024_,_1024_,_512_,_256]|
|Activation|ELU|
|Initial action std|1_._0|


## **TABLE S5. PPO Hyperparameters Used for Policy Training.** 

|**Item**|**Specification**||
|---|---|---|
|MLP Hidden dims|[512_,_256_,_128]||
|Activation|ELU||
|Output layer|linear, small-gain <br>with zero bias|Xavier init (gain 0_._01)|


## **TABLE S6. Residual Adaptor Architecture.** 

by a joint-wise factor proportional to the ratio between torque limits and stiffness, ∆ _q_ max _∝_ 0 _._ 25 _τ_ max _/Kp,_ which bounds the implied torques for a given position error and improves stability during high-dynamic tracking. 

## _K. RobotBridge_ 

RobotBridge is the unified deployment layer of our MOSAIC system, designed to bridge high-level policy algorithms with heterogeneous robot platforms in a plug-and-play manner, similar to RoboJudo [49], but with more scalable abilities. Its architecture cleanly separates high-level policy execution from low-level robot-specific interfaces. In practice, control policies are implemented in a platform-agnostic, high-level module, while all hardware-specific commands are handled by a dedicated low-level interface built on the robot’s SDK. This design decouples algorithm logic from device details, allowing the same policy code to drive different robots or simulations with minimal modification. For example, the identical MOSAIC policy pipeline can be executed in MuJoCo simulation or deployed on Unitree G1 hardware without any code change, facilitated by RobotBridge’s unified sim-to-real interface. 

RobotBridge supports seamless sim-to-real transfer on the Unitree G1 humanoid [35] and also accommodates multirobot simulation scenarios. It currently integrates support for Unitree’s humanoid platforms (H1 and H1 <u>2</u> [36]) and 

PND’s humanoid platform Adam [30] in addition to the G1 robot. This enables evaluation with multiple robots in shared environments, though our experiments primarily focus on a single robot. The framework’s modular design further permits running a wide range of policy pipelines under a common interface. We have integrated diverse control policies including our MOSAIC task policy, teleoperation-based imitation controllers like TWIST [44], general motion trackers such as GMT [2], sim-to-real alignment policies like ASAP, locomotion-specific controllers (e.g. AMO [16]), and even dual-agent tracking setups (e.g. a BeyondMimic [20]-style imitation scenario with a target agent and a follower) within RobotBridge. This flexibility showcases how RobotBridge abstracts the interaction between algorithms and robot embodiment: each policy, regardless of its internal mechanics, interfaces with the robot through the same standardized observation and action API provided by RobotBridge’s environment and controller modules. By handling sensor data streams, action scaling, and communication to the robot’s actuators internally, RobotBridge allows researchers to focus on high-level policy development while ensuring robust execution on real hardware. 

Detailed deployment and configuration instructions for RobotBridge (evaluation branch) will be available in the open-source repository’s documentation. By following a configuration-driven approach (built on Hydra [40]), users can easily switch robot models or control pipelines without code changes, simply by adjusting YAML configs or commandline arguments. This makes RobotBridge a convenient and rigorous platform for evaluating many control policies across simulation and real robots under a unified framework, as required for our MOSAIC system evaluation. 

## _L. Offline Replay_ 

_1) Pipeline:_ Offline motion replay in MOSAIC is implemented as a lightweight configuration change in RobotBridge. Crucially, the motion-loading and preprocessing interface used for replay is identical to the one used during training, which enables a consistent pipeline from learning to deployment. As a result, the same reference clips can be (i) visualized and verified in MuJoCo for sim-to-sim qualitative inspection and (ii) executed on the real robot for deployment tests, without modifying the policy code or runtime logic. 

RobotBridge’s layered design further decouples the highlevel components (policy checkpoint and reference motion selection) from the low-level robot stack (SDK, control loop, safety limits). Therefore, switching between different policies or motion clips does not interrupt the low-level controller or require reinitializing the robot (e.g., rehanging the robot or preloading all motions/models before testing). In practice, we can iterate over policies and references online while keeping the underlying control and communication pipeline unchanged, facilitating rapid and repeatable evaluation. 

## _M. Online Teleoperation_ 

_1) Pipeline:_ We developed an online teleoperation pipeline supporting two distinct hardware interfaces: Virtual Reality 


Fig. S4: **Schematic of the Full-body Inertial Tracker Configuration.** To ensure high precision and motion fidelity during data acquisition, we adopt a comprehensive setup consisting of 17 inertial markers. 

(VR) and inertial motion capture. The VR system utilizes PICO 4 Ultra, consisting of 5 tracking straps and 2 handheld controllers, while the inertial motion capture system utilizes a Noitom suit with 17 trackers via Noitom Axis Studio [28] (see Figure S4). Both interfaces utilize a unified processing pipeline to generate the reference motion stream: 

- 1) **Data Transmission and Retargeting:** Motion signals from the VR system are transmitted to a local workstation via Wi-Fi, while the Noitom inertial suit is connected via a wired interface. On the workstation, human kinematics are retargeted to the robot’s DoF using the GMR framework [43]. The resulting raw joint positions and root quaternions are then streamed to the robot’s onboard computer via the Lightweight Communications and Marshalling (LCM) [14] protocol. 

- 2) **Onboard Signal Processing:** Upon receiving the raw data, the robot’s onboard host performs real-time processing to ensure signal quality. The joint positions undergo _Exponential Moving Average_ (EMA) smoothing to mitigate sensor noise and transmission jitter. Joint velocities are then estimated by computing the gradient over a rolling position buffer using a central difference scheme. Finally, the _anchor orientation_ is derived via forward kinematics (FK) from the root orientation and processed joint states, completing the set of reference observations required for real-time policy inference. 

_2) Delay Analysis:_ As illustrated in Figure S5, the system exhibits an end-to-end teleoperation latency of approximately 0.4 s for the VR-based setup and 0.2 s for the inertial motion capture system averaged over 10 tests. The first phase, comprising data transmission from the device to the local workstation and the subsequent retargeting, accounts for 0.267 s in the VR setup and 0.067 s in the MoCap system, is the main contribution source for the delay. To mitigate the affect of delays for the teleoperation system, we use EMA smoothing and interpolation to the output retargeting results. 


Fig. S5: **Delay Analysis.** The teleoperation delay, as measured via video analysis, is approximately 0.4 s for the VR system and 0.2 s for the inertial motion capture system. 

## NETWORK ABLATIONS 

We ablate three policy architectures for fusing proprioception and the one-step reference input (Shown in Fig. S6): (a) MLP fusion (our final choice), where the reference and proprioception are directly concatenated and mapped to actions by a multi-layer perceptron; (b) encoder-based fusion, where the reference is first compressed by a learned motion encoder (implemented with FSQ [26] or VQ-VAE [37] style discretization) and then fused with proprioception via an MLP head; and (c) attention-based fusion [6], where proprioception queries attend to reference features via multi-head attention before an MLP output head. 

Across training curves shown in Fig. S7, the encoder-based (FSQ/VQ) and attention-based actors do not provide consistent gains over the MLP baseline in either tracking reward or episode length. These variants also incur higher training cost due to additional reconstruction/codebook updates or attention blocks. We therefore adopt MLP fusion and scale capacity via wider layers, which is a more reliable lever than architectural complexity at our current data scale. We attribute this to the relatively constrained structure of humanoid motions after retargeting into a unified robot space: despite stylistic diversity, the underlying control regularities are sufficiently captured by a moderately large MLP, and more sophisticated fusion mechanisms provide limited marginal benefit at the current data scale. 

In all network ablations, we only change the actor architecture while keeping the critic identical across runs. All PPO hyperparameters and training settings are held constant; the only difference is the actor’s fusion mechanism and its associated architectural parameters (Table S7). 

## FLD AUGMENTATION 

## _N. FLD Training_ 

The Fourier Latent Dynamics (FLD) [15] model was trained on a small curated set of teleoperated periodic locomotion demonstrations, comprising approximately two minutes of data 

|**Config**|**Parameters**|
|---|---|
|**FSQ encoder**||
|encoder<br>hidden<br>dims|[512, 128]|
|latent<br>dim|16|
|num<br>levels|7|
|mlp<br>hidden<br>dims|[512, 256]|
|activation<br>mlp|ELU|
|activation<br>fsq|ELU|
|**VQ encoder**||
|encoder<br>hidden<br>dims|[512, 256]|
|encoder<br>output<br>dim|128|
|num<br>embeddings|512|
|embedding<br>dim|8|
|commitment<br>weight|0.25|
|vq<br>loss<br>coef|1.0|
|mlp<br>hidden<br>dims|[512, 256]|
|activation<br>mlp|ELU|
|activation<br>vq|ELU|
|**attention**<br><br><br>||
|encoder<br>hidden<br>dims|[512, 256]|
|attention<br>dim|128|
|num<br>head|2|
|mlp<br>hidden<br>dims|[512, 256]|
|activation<br>mlp|ELU|
|activation<br>attention|ELU|


**TABLE S7. Network ablation configurations.** All runs share the same critic architecture and training hyperparameters; only the actor structure differs. 


Fig. S6: **Policy Network Ablations for Fusing Proprioception and Reference.** We compare three architectures with the same input interface (robot proprioception and one-step reference) and the same output (full-body action). **(a) MLP fusion:** proprioception and reference are concatenated and directly mapped to actions by an MLP. **(b) Encoder-based fusion:** the reference is first encoded into a compact latent (e.g., FSQ or VQ-VAE style code), then concatenated with proprioception and fed to an MLP head. **(c) Attention-based fusion:** proprioception features form queries ( _Q_ ) that attend to reference features as keys/values ( _K, V_ ) via multi-head attention; the attended feature is concatenated with proprioception and passed through an MLP to produce actions. 

with 30 distinct gait instances. These demonstrations exhibit stable cyclic structures with diverse step frequencies, step lengths, and operator-dependent styles. 

FLD represents periodic motion using a low-dimensional latent state consisting of a time-varying phase variable _ϕt_ and quasi time-invariant global style parameters **_θ_** . Given an initial latent state ( _ϕt,_ **_θ_** ), future latent states are propagated by explicit phase dynamics, 


where _f_ denotes the learned gait frequency and ∆ _t_ is the simulation time step. The corresponding motion state ˆ **s** _t_ + _k_ is decoded via a Fourier-based latent decoder: 


The model is trained to reconstruct motion trajectories over a multi-step horizon. Specifically, the reconstruction objective is defined as 


where _α ∈_ (0 _,_ 1] is a temporal discount factor that emphasizes near-term accuracy while enforcing long-horizon consistency. To encourage coherent temporal evolution, we further impose a phase-consistency regularization, which penalizes deviations from monotonic and smooth phase progression: 


The final training objective is given by 


where _λϕ_ controls the strength of the phase regularization. 

All motion sequences are temporally normalized to a fixed frame rate and segmented into complete gait cycles prior to training. The model is optimized using Adam until convergence. No additional supervision on contact states, ground reaction forces, or robot dynamics is introduced, keeping FLD purely self-supervised. 

_a) FLD model state space.:_ FLD representation learning’s state space consists of the base linear velocity, base angular velocity, base height, the projected gravity vector expressed in the robot frame, and joint positions. All quantities are temporally aligned with the motion trajectories used for FLD training and normalized to a fixed frame rate. 

_b) Representation training parameters.:_ The FLD model training hyperparameters are summarized in Table S9, and the FLD model architecture is listed in Table S10 

_O. Latent-Space Sampling and Motion Synthesis_ 

After training, we model the distribution of the learned global style parameters **_θ_** using a Gaussian Mixture Model (GMM) [15]. This parametric density captures the variability of gait frequency, amplitude, and stylistic factors observed in the limited set of teleoperated demonstrations. 


Fig. S7: **Network-architecture ablation.** Training curves comparing the MLP actor (ours) against encoder-based actors (VQ, FSQ) and an attention-based actor, under identical PPO settings with the same critic. The MLP achieves higher reward and longer episode length, while more complex actors do not yield gains despite increased training cost. 

Novel periodic locomotion trajectories are synthesized by sampling latent parameters from the learned GMM and initializing the phase uniformly: 


Given the sampled latent state ( _ϕ_ 0 _,_ **_θ_** ), future phases are deterministically propagated according to the learned frequency _f_ ( **_θ_** ): 


and decoded into motion states using the FLD decoder: 


By explicitly propagate the phase variable, this procedure generates long-horizon periodic locomotion trajectories that preserve global gait consistency over extended time horizons. In total, we synthesized approximately 10 hours of periodic locomotion motions, which were used exclusively for ablation studies on dataset augmentation. 

The full state composition is summarized in Table S8. 

|**Entry**|**Dimensions**|
|---|---|
|base linear velocity|3|
|base angular velocity|3|
|base height|1|
|projected gravity|3|
|joint positions|29|


**TABLE S8. State Space Used for FLD Representation Learning.** 

## OPEN-SOURCE CHECKLIST 

To support reproducibility and downstream research, we will release code, models, and data for MOSAIC, together with the full data-processing pipeline and deployment stack. 

|**Parameter**|**Symbol**|**Value**|
|---|---|---|
|step time (seconds)|∆_t_|0.02|
|learning rate|–|1_×_10<sup>_−_4</sup>|
|weight decay|–|5_×_10<sup>_−_4</sup>|
|learning epochs|–|5|
|mini-batches|–|10|
|latent channels|_c_|32|
|trajectory segment length|_H_|91|
|FLD propagation horizon|_N_|90|
|propagation decay|_α_|1.0|


## **TABLE S9. FLD Representation Training Parameters.** 

|**Module**|**Layer**|**Output Size**|**Activation**|
|---|---|---|---|
|Encoder|Conv1D|256_×_91|ELU|
||Conv1D|256_×_91|ELU|
||Conv1D|8_×_91|ELU|
|Phase-<br>Encoder|Linear|32_×_2|Atan2|
|Decoder|Conv1D|256_×_91|ELU|
||Conv1D|256_×_91|ELU|
||Conv1D|39_×_91|ELU|


## **TABLE S10. Network Architecture of FLD Model.** 

_a) Code (training).:_ We will open-source the MOSAIC training framework, including: (i) PPO training scripts and configuration files, (ii) observation/reward/termination specifications used in all experiments, (iii) the multi-motion data loader and two-level resampling implementation (motion-level and within-motion), (iv) ablation utilities (e.g., RL vs. distillation; adaptor variants; network-architecture ablations), and (v) evaluation scripts for simulation benchmarks. 

_b) Code (deployment).:_ We will open-source RobotBridge, for sim2sim visualization and sim2real testing without changing the pipeline. 

- **Sports exercise:** _A person doing push-ups rapidly, pushing up and down as fast as possible for 10 seconds, continuing for more than 10 seconds._ 

_c) Data (redistributable).:_ We will release our in-house motion data used by MOSAIC, including: (i) optical MoCap, (ii) inertial MoCap, and (iii) small teleoperation adaptation datasets collected for adaptor training. For each sequence, we will provide two standardized formats: AMASS-style human data and G1-retargeted robot data, together with metadata (source, frame rate, sequence duration, filtering criteria, and splits). 

_d) Generated motions.:_ We will release (i) the text prompts used for motion generation (covering seven action categories with planar constraints and _≥_ 10 s duration), (ii) the filtered generated motions (AMASS-style + G1-retargeted), and (iii) scripts that reproduce the generation, retargeting, and manual filtering pipeline. 

All open-sourced data are with labels, which describe motion behaviors. 

_e) Public datasets (scripts only).:_ Due to third-party licensing, we will not redistribute AMASS/OMOMO directly; instead we will release scripts to apply the same retargeting/standardization pipeline used for our in-house and generated data (coordinate normalization, initial pose alignment, and unified serialization). 

_f) Models and checkpoints.:_ We will release trained checkpoints for: (i) the teleoperation-oriented general motion tracker, (ii) interface-specific adaptor policies, and (iii) the residual module used for distillation, along with exact training configurations and seeds required to reproduce the reported results. 

MOTION PROMPT EXAMPLES FOR MOTION GENERATION 

**Prompt template.** We follow a simple, reproducible template: 

_“A person [action description], [style/emotion optional], continuing for at least 10 seconds, on flat ground.”_ 

## **Examples.** 

- **Static pose:** _A person holding a deep squat position (knees bent, thighs parallel to the floor) and not moving, maintaining it for more than 10 seconds._ 

- **Running:** _A person confidently running at a steady pace with an upright posture, continuing for at least 10 seconds._ 

- **Walking:** _A person absentmindedly walking as if balancing a book on their head, steps deliberate and body straight, continuing for more than 10 seconds._ 

- **Daily activity:** _A person angrily folding imaginary clothes, making aggressive, forceful movements, continuing for over 10 seconds._ 

- **Martial arts:** _A person performing a slow tai chi routine, shifting weight gracefully through each pose, continuing for more than 10 seconds._ 

- **Dancing:** _A person dancing slowly in a sorrowful manner, moving their body with a somber, expressive style, continuing for more than 10 seconds._ 

