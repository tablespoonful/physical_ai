---
title: "Dexora: Open-source VLA for High-DoF Bimanual Dexterity"
date: "2026-05-18"
authors: "Zongzheng Zhang; Jingrui Pang; Zhuo Yang; Kun Li; Minwen Liao; Saining Zhang"
venue: "ICRA 2026"
url: https://arxiv.org/abs/2605.18722
pdf: https://arxiv.org/pdf/2605.18722
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2605.18722)** / [論文ページ](https://arxiv.org/abs/2605.18722)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Dexora: Open-source VLA for High-DoF Bimanual Dexterity** 

Zongzheng Zhang<sup>1</sup><sup>_,_2</sup><sup>_∗_</sup> , Jingrui Pang<sup>1</sup><sup>_,_2</sup><sup>_∗_</sup> , Zhuo Yang<sup>1</sup> , Kun Li<sup>2</sup> , Minwen Liao<sup>1</sup> , Saining Zhang<sup>1</sup> , Guoxuan Chi<sup>1</sup> , Jinbang Guo<sup>2</sup> , Huan-ang Gao<sup>1</sup> , Modi Shi<sup>3</sup> , Dongyun Ge<sup>1</sup> , Yao Mu<sup>4</sup> , Jiayuan Gu<sup>5</sup> , Rui Chen<sup>1</sup> , Hao Dong<sup>6</sup> , Huazhe Xu<sup>1</sup> , Li Yi<sup>1</sup> , Yixin Zhu<sup>6</sup> , Hang Zhao<sup>1</sup> , Pengwei Wang<sup>2</sup> , Shanghang Zhang<sup>2</sup><sup>_,_6</sup> , Guocai Yao<sup>2</sup> , Jianyu Chen<sup>1</sup> , Hongyang Li<sup>3</sup> , Hao Zhao<sup>1</sup><sup>_,_2†</sup> 

**_Abstract_ — Vision-Language-Action (VLA) models have recently become a central direction in embodied AI, but current systems are restricted to either dual-gripper control or singlearm dexterous hand manipulation. While low-dimensional gripper control can often be handled with simpler methods, highdimensional dexterous hand control benefits greatly from full end-to-end VLA learning. In this work, we introduce Dexora, the first open-source VLA system that natively targets dualarm, dual-hand high-DoF manipulation. We design a hybrid teleoperation pipeline that decouples gross arm kinematics (captured with a custom exoskeleton backpack) from fine finger motion (markerless hand tracking via Apple Vision Pro), and that drives both a physical dual-arm dual-hand platform and an identical MuJoCo digital twin. Using that interface, we assemble a large training corpus: an embodiment-matched synthetic corpus (100K simulated trajectories, 6.5M frames) and a real-world dataset of 10K teleoperated episodes (2.92M frames). To mitigate noisy teleoperation demonstrations, we propose a data-quality-aware training recipe: an offline discriminator provides clip-level weights for diffusion-transformer policy training, down-weighting low-quality demonstrations. Empirically, Dexora outperforms competitive VLA baselines on both basic and dexterous benchmarks (e.g., average dexterous success 66.7% vs. 51.7%), attains 90% success on basic tasks, and shows robust out-of-distribution and cross-embodiment generalization. Ablations confirm the importance of real data and the discriminator for dexterity. Demos, data, code, and models can be found at https://dexoravla.github.io.** 

## I. INTRODUCTION 

Vision-Language-Action (VLA) models have emerged as a promising paradigm for embodied AI, yet existing systems remain fundamentally constrained: they are either designed for dual-arm, low-DoF grippers or single-arm dexterous hands, but not both [1]–[7]. As illustrated in Fig. 1 (top), such limitations prevent prior VLAs from handling tasks that intrinsically demand dual-arm coordination (e.g., piston insertion), or high-DoF dexterous fingers (e.g., bottle opening/complex book retrieval). _Dexora_ is the first open-source VLA that addresses this gap by unifying dual-arm, dualhand, and high-DoF dexterity into a single system (Fig. 2). 

To enable such complex skill acquisition, _Dexora_ introduces a hybrid teleoperation pipeline. Gross arm kinematics are captured with a lightweight exoskeleton backpack, while fine-grained finger articulation is driven by markerless hand tracking via Apple Vision Pro. This decoupling makes it feasible to control a physical dual-arm dual-hand platform 

> 1Tsinghua University. 2Beijing Academy of Artificial Intelligence. 3The University of Hong Kong.<sup>4</sup> Shanghai Jiao Tong University.<sup>5</sup> ShanghaiTech University.<sup>6</sup> Peking University.<sup>_∗_</sup> Equal contribution.<sup>†</sup> Corresponding author 


Fig. 1. **_Dexora_ overview** . (a) **Motivation** : Three illustrative contrasts highlight the need for dual-arm, dual-hand dexterous VLA: piston insertion (requires two arms), book retrieval from a packed shelf (hands with fingers succeed where grippers fail), and bottle opening (12-DoF fingers with lateral swing outperform 6-DoF). (b) **Dataset** (§III-B): We pretrain on **100K** simulated bimanual-hand trajectories and post-train on **10K** real demonstrations, all collected with our dual-arm, dual-hand platform. (c) **Architecture** (§III-C): A trained discriminator scores dataset demonstration quality and guides training, driving the diffusion-transformer policy to prioritize high-quality trajectories while down-weighting low-quality ones. (d) **Performance** (§IV-B): _Dexora_ achieves consistently higher average success rates on both basic (Pick-and-Place, Assemble/Disassemble, Articulated Object) and dexterous benchmarks compared to state-of-the-art VLA models. (e) **Embodiment generalization** (§IV-C): The same policy transfers across **single-arm gripper** , **dual-arm grippers** , and **single-arm low-DoF hand** without re-architecting the model. 

with 36 DoF, while simultaneously mirroring demonstrations in a MuJoCo-based digital twin, thereby ensuring scalable and embodiment-matched data collection. 

Using this interface, we construct a large-scale dataset for dual-arm, dual-hand dexterous manipulation (Fig. 1, §IIIB). It consists of 100K simulated trajectories (361 hours, 6.5M frames) and 10K real teleoperated episodes (177.5 hours, 3.2M frames). The design follows the principle of sim-real complementarity: simulated data provide scale and 


Fig. 2. **Comparison of embodiment coverage.** Prior works cover either single-arm or low-DoF dual-arm settings. _Dexora_ is the first system positioned in the dual-arm, high-DoF dexterous region, while also generalizing across simpler embodiments without re-architecture. 

task diversity, while real data provides fine-grained realism essential for high-DoF bimanual dexterity. Together, this dataset establishes a foundation for training VLA models under realistic dexterous settings. 

A key challenge of teleoperated data is the presence of noisy or unstable demonstrations (Fig. 1, §III-C). To address this, _Dexora_ employs discriminator-guided qualityaware training: an offline discriminator scores each demonstration, and the policy is trained with weighted diffusiontransformer loss that down-weights low-quality clips. This design effectively stabilizes learning, ensuring that the policy benefits from large-scale data while mitigating the impact of teleoperation artifacts. 

We evaluate _Dexora_ across both basic manipulation and dexterous benchmarks (Fig. 1, §IV-B). Quantitatively, _Dexora_ achieves over 90% success on basic pick-and-place and open articulated objects tasks, while improving dexterous success from 51.7% (baseline) to 66.7% (+15%). Qualitatively, the system demonstrates torsional manipulation and complex dual-arm coordination. These results highlight the critical role of both real-world data and quality-aware training in attaining high-DoF dexterity. 

Finally, _Dexora_ exhibits strong generalization beyond its native embodiment (Fig. 1, §IV-C). Despite being trained on a 36-DoF dual-arm dual-hand platform, the learned policy successfully transfers to single-arm gripper, dual-arm grippers, and single-arm low-DoF hand. This suggests that VLA policies trained under rich dexterous settings can serve as universal controllers, generalizing across embodiments. Fig. 2 situates this result in the broader landscape: prior VLAs mainly focus on single-/dual-arm grippers or lowDoF hand. _Dexora_ is positioned in the dual-arm, high-DoF hands quadrant while remaining downward-compatible to the other regions of the grid. This suggests a practical route to universal controllers: train in the dexterous, high-DoF setting and deploy by projecting to simpler robots. 

## II. RELATED WORK 

## _A. Teleoperation System_ 

Teleoperation enables us to acquire large-scale robot demonstrations by translating human motions into robotexecutable control signals. Existing platforms can be cate- 

gorized into five classes: (i) leader–follower systems with kinesthetic teaching rigs [8], [9]; (ii) VR/MR headset–based pose tracking (e.g., Vision Pro pipelines) [10], [11]; (iii) vision-only retargeting [12], [13]; (iv) exoskeleton interfaces for joint-level arm and finger tracking [14], [15]; and (v) joystick/button controllers [16], [17]. We adopt a hybrid teleoperation setup: exoskeletons provide precise arm-level kinematics, while the Vision Pro offers convenient, highresolution capture of fine-finger motions. This combination produces high-DoF, dual-arm and dual-hand demonstrations that are both accurate and operator-friendly, and are natively compatible with Vision-Language-Action (VLA) model training [18], [19]. 

## _B. Dexterous Manipulation_ 

Dexterous manipulation includes grasping, in-hand reconfiguration, tool use, and coordinated bi-manual skills [20], [21]. Prior research generally falls into two categories: _grasp synthesis_ and _policy learning_ . **On the synthesis side** , the field has undergone a paradigm shift from analytical sampling to generative modeling. Diffusion [22], [23], normalizing flows [24], and latent generative models such as VAE [25], [26], complemented by optimization-based pipelines [27], now enable scalable production of physically consistent grasps across diverse hands and objects. **On the policy side** , reinforcement learning [28] and imitation learning [29] have driven progress toward closed-loop robustness and sim-to-real transfer in high-DoF hands. Emerging _data engines_ leverage automated imitation [30] and egocentric supervision [31] to expand coverage, accelerating policy learning at unprecedented scale. Despite this rapid progress, most pipelines remain hand-centric, reward-sensitive, and limited in multi-arm coordination. In contrast, we pursue a vision-language-action (VLA) model that operates in **dualarm, dual-hand** high-dimensional action space. 

## _C. Vision-Language-Action (VLA) Model_ 

Vision-Language-Action (VLA) models have recently emerged as a promising paradigm yet most existing systems remain confined to low-DoF or single-arm embodiments [32], [33]. Representative efforts such as RT-2 [1], OpenVLA [2], and GraspVLA [34] output manipulation policies for single-arm grippers. More recent generalist policies extend to bimanual settings—e.g., _π_ 0 [3], _π_ 0 _._ 5 [4], RDT [5], GO-1 [35], GR-3 [6], GR00T [7], and DexGraspVLA [36]—but these typically simplify embodiment to parallel-jaw grippers, limiting dexterity. In parallel, largescale data engines such as Being-H0 [37] and DreamGen [38] have enriched supervision, but they still fall short of enabling **high-DoF** dual-hand control. 

Our work introduces a **dual-arm, dual-hand high-DoF VLA** that learns to output synchronized arm–hand trajectories end-to-end. The formulation admits natural downshifting to lower-DoF embodiments via finetuning, offering a unified pathway toward cross-embodiment generalization. 


Fig. 3. **Hardware and teleoperation system** . (a) Hybrid teleoperation interface and 12-DoF XHAND. (b)-(c) The operator teleoperates the physical robot and its MujoCo digital twin, so _apple→plate_ demonstrations are collected in real and simulation under the same interface, thereby reducing the sim-to-real gap. 

## III. DEXORA 

In this section, we first introduce the hardware setup and teleoperation system (Sec. III-A), followed by the construction of our dataset, assembling an embodiment-aligned corpus of large-scale synthetic and real-world demonstrations (Sec. III-B). We then present the VLA framework with a learned data-quality discriminator that scores demonstrations and weights training (Sec. III-C). Finally, we specify the three-stage data-quality-aware training recipe (Sec. III-D). 

## _A. Dual-Arm Dual-hand System_ 

As shown in Fig. 3 (a), _Dexora_ integrates two 6-DoF AIRBOT arms with a pair of XHAND dexterous hands, each offering 12 fully actuated joints. All finger joints are independently driven, and the thumb and index additionally support lateral ab/adduction, enabling human-like in-hand reorientation and torsional manipulation (e.g., cap twisting). 

To achieve scalable teleoperation, we decouple gross arm motion from fine finger control. A custom dual-arm exoskeleton backpack captures the operator’s shoulder–elbow–wrist angles and maps them directly to robot joint space. This design yields drift-free, low-latency trajectories while avoiding the inverse-kinematics jitter and singularities that often degrade vision-only retargeting pipelines. Apple Vision Pro provides markerless 3D finger skeletons that we retarget to XHAND with a short calibration phase while enforcing joint limits and safety constraints. This hybrid interface combines the precision of joint-space control for the arms and the convenience of lightweight, glove-free finger input, making long data-collection sessions practical (Fig. 3 (a)). 

Our interface drives both the physical robot and a MuJoCo digital twin of the same embodiment. All sensing streams share a time-aligned I/O system: four RGB views and full 36-DoF joint states are logged at 20 Hz. The twin mirrors the real robot’s kinematics and controllers, and the same teleop drivers run in real and sim, yielding low latency and high fidelity; operators can switch seamlessly between hardware and simulation to collect demonstrations (Fig. 3 (b)-(c)). 

## _B. Dataset Construction_ 

**Synthetic Data.** We generate a large, embodimentmatched simulation corpus in MuJoCo. Using Qwen2.5VL [39], we mine Objaverse [40] to select manipulable objects and automatically assign physical parameters (Fig. 4 


Fig. 4. **Dataset demonstration** . (a) Simulation objects subset: our simulator includes 297 objects across 30 categories. (b) Real-world objects (347 objects, 17 categories), covering both basic and dexterous use cases. (c) Per-family task distribution in simulation vs. real. The simulation data only includes basic tasks, while the real-world set shifts weight toward dexterity (20%). (d) Trajectory counts per family and embodiment (sim/real; single/dual-hand). 

(a)). On top of this, we build a set of 200 tasks covering three basic families in Fig. 4 (c). For each task, we collect 3–5 teleoperated seed demonstrations and follow the DexMimicGen [30] recipe to synthesize trajectories: we randomize initial states and retarget the seed actions to new scenes, yielding 500 trajectories per task. Scene layouts and success criteria are auto-generated by Qwen. All simulated episodes are logged with the same observation–action protocol as in the real system, which keeps the interface consistent and reduces the sim-to-real gap. In total, the synthetic set contains about 6.5M frames, 361h video. 

**Real World Data.** We collect real-world data on the same embodiment used in the simulation. Beyond common objects and basic tasks, we add dexterous tool-use scenarios that are difficult to stage in simulation (Fig. 4 (b)) and the dexterous scenes in Fig. 4 (c)–(d). In total, we curate 200 tasks and acquire 50 teleoperated demonstrations per task via the hybrid teleoperation interface, yielding 10K episodes. The dataset amounts to 40.5 hours and 2.92M frames. All recordings are converted to the LIBERO-2.1 standard and open source. We use this to fine-tune the VLA to specialize basic competence into dexterous, bimanual skills. 


Fig. 5. **_Dexora_ framework.** (a) **Data filtering** : From the real-world dataset we pre-screen demonstrations by kinematic smoothness (low acceleration and jerk), then replay them for post-validation and keep the clips that complete the task without collisions, forming a high-quality subset. (b) **Discriminator training** : With the pretrained diffusion–transformer policy frozen, we compute a log- _π_ proxy for each clip and train a discriminator that, conditioned on observations and language, outputs a quality score _d_ ( _Ct_ ) _∈_ (0 _,_ 1]. (c) **Data-quality-aware post-training** : During post-training, the score _d_ ( _Ct_ ) is converted to weights _wi_ and used in the diffusion loss _Lπ_ . At inference time, only the policy is used. 

## _C. Framework_ 

**Data Quality Criteria.** Real-world teleoperation demonstrations exhibit substantial variability due to operator skill, sensing noise, inherent limitations (such as occlusion during hand keypoint tracking), and latency. Training on such heterogeneous data without constraints often degrades policy learning. We therefore establish **episode-level** quality criteria with two pillars: (i) kinematic smoothness and steadiness, proxied by low acceleration _A_ ep and jerk _J_ ep—for prescreening; (ii) replay success as the decisive indicator of data reliability (task completion without collisions)—for postvalidation. This two-stage design yields a clean positive set for training the discriminator (Fig. 5 (a)). 

Let an episode be denoted by _τ_ = _{st }t_<sup>_T_</sup> =1<sup>,where</sup><sup>_st∈_R</sup><sup>_D_</sup> is the proprioceptive state vector ( _D_ = 36). The sampling interval is ∆ _t_ . Because state dimensions have heterogeneous numeric ranges, we first apply per-dimension min–max normalization. We compute velocity, acceleration, and jerk using centered finite differences ( _t_ = 4 _,..., T −_ 3): 


For an episode _τ_ , acceleration and jerk are defined via the root mean square (RMS) across both time and dimensions: 


Lower values of _A_ ep and _J_ ep indicate smoother, steadier demonstrations. We rank episodes by _A_ ep and by _J_ ep separately, keep the lowest 20% in each list, and take their intersection: _S_ pre = _τ_ : _τ ∈_ Low-20%( _A_ ep) _∧ τ ∈_ � 

Low-20%( _J_ ep) _,_ which retains about 18% of episodes in our � data. From _S_ pre, we designate positives by open-loop replay success—task completion without collisions: _S_ high = � _τ_ : _τ ∈ S_ pre _∧_ Success( _τ_ ) = 1 _∧_ CollisionFree( _τ_ ) = 1� _,_ yielding roughly 15% high-quality demonstrations. Note that we score quality at the episode not chunk-level: stationary chunks can trivially exhibit low acceleration/jerk yet be uninformative. Episode-level aggregation, paired with a movement-coverage guard, suppresses such false positives and better captures overall stability and task competence. 

**Discriminator Model.** After selecting the top-quality subset, we use an offline discriminator to score every real episode. For each episode, we uniformly sample _K_ subclips _{Ck}_<sup>_K_</sup> _k_ =1<sup>,andconstructatokenizedinputperclip:</sup> _ξt_ = � _st ,_ **o** _t , ℓ,_ **a** _t_ : _t_ + _L−_ 1 _,_ log<sup>�</sup> _πt_ �, where **o** _t_ are multi-view RGB observations, _ℓ_ is the language instruction, **a** _t_ : _t_ + _L−_ 1 is an action chunk of length _L_ , and log<sup>�</sup> _πt_ is a log- _π_ chunk score (policy-compatibility proxy) computed from the pretrained diffusion policy over that clip. 

Given a pretrained diffusion-transformer policy _πθ_ , we define a surrogate for log _π_ ( **a** _t_ : _t_ + _L−_ 1 _| ℓ,_ **o** _t_ ) via the negative denoising residual energy: 


where� _S_ is a small set of diffusion steps. Intuitively, larger log _πt_ indicates that the policy explains the chunk better. 

Each clip is projected into a token sequence: [ _st_ ; **a** _t_ : _t_ + _L−_ 1; log<sup>�</sup> _πt_ ] _,_ equipped with learned positional embeddings. Language and image tokens are concatenated as a condition stream. A shallow stack of Transformer blocks produces hidden tokens, which are globally averaged 

and passed through a small MLP head with sigmoid to output a clip score _d_ ( _Ck_ ) _∈_ (0 _,_ 1] (Fig. 5 (b)). 

**Diffusion Transformer.** We employ a decoder-only Transformer as the diffusion model for the policy. Its architecture resembles the discriminator, but the input consists of the current observation **o** _t_ , and the instruction _ℓ_ , forming a vision–language conditioned policy: 


The current joint angle state information state _st_ , and noisy actions � **a** _t_ : _t_ + _L−_ 1 are projected into the latent space and concatenated with the diffusion timestep _t_ to form the input tokens for the transformer. Natural language and multi-view image inputs are encoded into conditional tokens via the T5 [41] and SigLip [42] encoders, respectively, and alternately injected into the transformer blocks. The model predicts the action noise _θ_<sup>�</sup> , thereby yielding the predicted action sequence � **a** _t_ : _t_ + _L−_ 1 (Fig. 5 (c)). We use the standard DDPM for sampling during training and employ DPMSolver++ for acceleration during action generation. 

## _D. Data-quality-aware Training Recipe_ 

We first **pretrain** the diffusion-transformer policy _πθ_ on simulation data to endow the VLA with basic competence (pick & place, assemble, etc.). This policy is then used to compute the _log-π proxy_ for training the discriminator model. 

Let the positive set be the replay-validated high-quality subset _S_ high (about 15%) and the unlabeled pool be _U_ = _D_ real _\ S_ high. We optimize a positive–unlabeled objective: 


where _η_ = 0 _._ 5. We apply clip scores to _d ∈_ [0 _._ 1 _,_ 0 _._ 9] for stability (Fig. 5 (b)). Following the DWBC mapping from [43], we convert calibrated scores to weights _wi_ . 

Finally, we **post-train** _πθ_ on the real dataset to upgrade this base competence into dexterous skills, using the precomputed weights. For diffusion training, 


with a short weight warm-up (Fig. 5 (c)). 

## IV. EXPERIMENT 

We evaluate _Dexora_ across three axes: (1) **Performance** : higher success on basic and dexterous tasks, especially on bimanual skills (Sec. IV-B). (2) **Generalization** : Robust to OOD shifts and transfers across embodiments (Sec. IV-C). (3) **Ablations** : contributions of training data composition and the learned data-quality discriminator (Sec. IV-D). 

## _A. Experimental Setup and Baselines_ 

**Setup.** Our policy model has 28 layers, a hidden size of 1024, and 16 attention heads. The discriminator is smaller, with 12 layers, a hidden size of 512, and 8 attention heads, for 30M parameters. We pretrain the policy model for 100K 

gradient steps and train the discriminator model for 10K steps, using distributed data parallelism across 8 × NVIDIA A100 GPUs with a total batch size of 64. Both models are optimized using AdamW. 

**Baselines.** We compare against three representative baselines: **Diffusion Policy (DP)** [44]—a conditional denoising policy for visuomotor imitation; _π_ 0 [3]—a VLA with a flowmatching action generator; and **GR00T N1** [7]—an open VLA (VLM + DiT) designed for humanoid control. 

**Action-space Adaptation.** DP natively regresses continuous actions, so we train it directly on our 36-D vector commands. For _π_ 0, we append a 2-layer MLP projector that maps each model’s native action output to our 36-D joint command. The projector is factorized by physical groups (L/R arm, L/R hand), and learns the expansion from lowerDoF end-effector outputs to our 12-DoF hands via learned synergies. 

**Protocol.** All other settings are identical across methods: control frequency, action chunk length _L_ = 32, camera intrinsics/extrinsics, and the number of views. For each task, we collect 100 demonstrations to train/fine-tune the baselines for 50K steps. Fine-tuning runs on 4 × NVIDIA L20 GPUs with LoRA; inference is performed on a single RTX 4090. We report the success rate over 20 rollouts per task. 

## _B. Evaluation Results in Real World_ 

**Basic Tasks Evaluation.** We group basic tasks into three types— **Pick-and-Place** (5 tasks), **Assemble/Disassemble** (5 tasks), and **Articulated Objects** (2 tasks). Each type mixes single-hand and bimanual problems. Representative bimanual examples include placing a distant block into a tray via a two-hand handover with temporal ordering, and separating two stacked bowls that require simultaneous two-hand prying (Fig. 6). _Dexora_ is evaluated zero-shot. Results in Tab. I show that _Dexora_ attains the highest overall success, reaching _≥_ 90% on 7/12 tasks and consistently leading the bimanual tasks. GR00T N1 [7] is competitive on simpler, mostly single-hand tasks. _π_ 0 [3] degrades most after mapping a gripper-centric action space to high-DoF hands, confirming that the low _→_ high DoF mapping is ill-posed without embodiment-matched data. Benefiting from many dual-arm episodes in training, _Dexora_ shows clear gains on bimanual coordination while maintaining strong performance. Overall, these trends support our design choice: embodimentmatched, high-DoF data are essential for performance. 

**Dexterous Manipulation Tasks Evaluation.** Pure pickand-place does not exploit high-DoF hands; grippers can also do that. The value of hands emerges on dexterous skills that require in-hand tool use and coordinated bimanual manipulation (Fig. 1(a)). We therefore benchmark 6 tasks (Fig. 7). All models are trained/fine-tuned on 100 demonstrations. Tab. II shows that _Dexora_ gains the best average performance (66 _._ 7% vs. 51 _._ 7% for GR00T N1, 26 _._ 7% for _π_ 0, and 6 _._ 7% for DP). GR00T N1 is the strongest baseline but uses a 6-DoF hand; it struggles on in-hand skills such as _Use pen_ and fails on _Twist cap_ , which require thumbindex synergies and lateral finger swing to generate a stable 


Fig. 6. **Basic tasks suite.** (a) Pick and Place (5 tasks). (b) Assemble/Disassemble (5 tasks). (c) Articulated Objects (2 tasks). TABLE I 

**BASIC TASKS EVALUATION** . RESULTS ARE SUCCESS RATES (%) OVER 20 TRIALS. <mark>G</mark> RAY COLUMNS INDICATE BIMANUAL TASKS. 

|**Method**|||**Pick and P**|**lace**|||**Assemb**|**le / Disassem**|**ble**||**Articulated **|**Object**|**Avg.**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Apple<br>_→_plate|Bowl<br>_→_bowl|Two eggs<br>_→_box|Lift<br>basket|Left block<br>_→_right plate|Stack<br>ring blocks|Grab<br>square blocks|Place kettle<br>on base|Remove<br>pen cap|Separate<br>nested bowls|Open<br>cabinet door|Open<br>laptop||
|DP|60|65|30|10|25|35|15|45|30|10|65|20|34.2|
|_π_0|75|70|45|30|30|60|60|65|55|20|60|35|50.4|
|GR00T N1|95|**100**|75|60|80|**90**|**80**|90|80|60|95|80|82.1|
|Dexora|**100**|**100**|**85**|**80**|**90**|85|**80**|**95**|**90**|**80**|**100**|**90**|**89.6**|


TABLE II 

**DEXTEROUS MANIPULATION** TASKS EVALUATION. 

|Method|Use pen|Fetch book|Cut leek|Place plates|Rough dough|Twist cap|
|---|---|---|---|---|---|---|
|DP|5|10|10|0|15|0|
|_π_0|20|45|60|20|15|0|
|GR00T N1|45|60|**85**|60|60|0|
|Dexora|**65**|**80**|80|**70**|**80**|**25**|


Fig. 7. **Dexterous manipulation sequences** . (a) **Use Pen** : The left hand picks up the pen (#1), hands it to the right hand (#2); the right thumb depresses the tip (#3) and writes on paper (#4). (b) **Cut Leek** : The right hand grasps the knife (#1), the left hand stabilizes the leek (#2); the right hand slices (#3) and returns the knife to the table (#4). (c) **Rough Dough** : Both hands press the rolling pin simultaneously (#1) and push forward to flatten the dough (#2). (d) **Twist Cap** : The left hand holds the bottle while the right thumb–index grip twists the cap (#1) and removes it (#2). 

torsional wrench. _Dexora_ ’s gains arise from its 12-DoF hands and bimanual training corpus, enabling reliable inhand and dual-arm coordination. We find that cap twisting exhibits the lowest success rate. The task requires generating a stable torsional wrench to overcome cap breakaway torque while preventing slip, which couples precise normal-force regulation, fingertip friction, and fine in-hand alignment. In our current setup, the absence of tactile feedback and relatively low-friction rigid fingertip pads leads to slip. 


Fig. 8. Generalization of six Out-of-Distribution (OOD) conditions. We report success rate (%) over 20 rollouts. 

## _C. Generalization_ 

**Out-of-Distribution Generalization.** We test OOD robustness on the “Pick apple to the plate” task across six conditions: unseen background, unseen lighting, unseen object, occlusion, clutter, and height change, and we report the success rate (Fig. 8). _Dexora_ maintains high performance across all variants, showing excellent OOD generalization. 

**Cross-Embodiment Generalization.** Our premise is that a dual-arm, dual-hand high-DoF policy contains lower-DoF embodiments as subspaces: projecting a 36-D joint action down to simpler robots is dimension reduction, not synthesis—far easier than “lifting” a gripper policy to dexterous hands. We therefore test three representative embodiment configurations: **EC-1: single-arm gripper** - Franka Emika 


Fig. 9. **Cross-embodiment generalization** . The _Dexora_ policy transfers to (a) single-arm gripper, (b) dual-arm grippers, and (c) single-arm singlehand, completing representative tasks like a three-step pepper handover. 


Fig. 10. **Effect of training data composition.** Success rate for four tasks under three training regimes: Sim Only, Sim + 50% Real, Sim + All Real. Panda (6-DoF + 1-DoF gripper); **EC-2: dual-arm grippers** - Cobot Magic ALOHA (2 × (6-DoF arm + 1-DoF gripper)); **EC-3: single-arm single-hand** - Unitree G1 7-DoF arm + Inspire Hand 6-DoF. For adaptation, we pad unused action dimensions to keep tensor shapes fixed; for observations, we mask the absent camera. Each task is fine-tuned with 100 demonstrations, and all other settings are identical. On the evaluated tasks including single- and dual-arm setups (Fig. 9), grasping tasks transfer readily across embodiments, whereas dexterity-demanding tasks show the largest gaps (Tab. II). This supports our hypothesis that high→low mapping is better posed than the inverse; compressing a 12-DoF hand policy to a 1-DoF gripper is simpler than lifting a gripper policy to dexterous hands. 

## _D. Ablation Study_ 

**Effectiveness of Training Data Composition.** We compare three post-training regimes: Sim Only, Sim + 50% Real (100 tasks), and Sim + All Real (200 tasks). Four tasks are evaluated, two basic (Apple→plate, Stack ring blocks) and two dexterous (Use pen, Cut leek). Success rises steadily with more real data; dexterous tasks improve from 0→35→65 and 10→60→85 (Fig. 10). These results show that simulation is effective for bootstrapping basic skills, while real, more complex data plays a crucial role in developing dexterous capabilities. 

**Effectiveness of Discriminator model.** We compare vanilla post-training of the Diffusion Transformer with quality-aware post-training that uses a learned discriminator 


Fig. 11. **Effect of the data-quality discriminator** . (a) **Corn** _→_ **plate** : with the discriminator, joint trajectories are smooth and the placement succeeds; without it, high-frequency oscillations in left-hand joint 5 cause the corn to drop. (b) **Lift basket (bimanual)** : with the discriminator, the basket is lifted; without it, jitter in right-hand joint 9 tilts the basket and it slips. 

TABLE III 

**EFFECT OF THE DISCRIMINATOR MODEL** . WE REPORT **S.R.** (SUCCESS RATE %) AND SMOOTHNESS METRICS—MEAN NORMALIZED JOINT **ACCELERATION** AND **JERK** , AVERAGED OVER 20 EPISODES. 

|**Method**|**C**|**orn** _→_**p**|**late**||**Lift bask**|**et**|
|---|---|---|---|---|---|---|
||S.R.|Acc. _↓_|Jerk _↓_|S.R.|Acc. _↓_|Jerk _↓_|
|w/o discriminator|85|0.034|0.043|55|0.041|0.052|
|w/ discriminator|95|0.020|0.032|80|0.023|0.036|


to score and weight demonstrations. Tab. III quantifies the gains: the discriminator improves success rate and reduces acceleration and jerk at inference. In both a single-hand and a bimanual task, the quality-aware model executes smoother, more coherent motions. The time-series traces show lower variance and fewer reversals (Fig. 11). Overall, the discriminator helps the policy learn from mixed-quality demonstrations by emphasizing high-quality segments and down-weighting suboptimal ones, enabling better strategies from imperfect data. 

## V. CONCLUSION 

We present _Dexora_ , the first open-source VLA system that natively controls dual-arm, dual-hand, 36-DoF robots. A hybrid teleoperation pipeline drives both hardware and a MuJoCo twin to build an embodiment-matched corpus, and a data-quality discriminator guides post-training so the policy learns most from high-quality demonstrations. _Dexora_ outperforms strong baselines on basic and dexterous tasks, is robust to OOD shifts, and transfers across embodiments with lightweight action projectors—evidence that training in a rich, high-DoF action space provides a well-posed path to lower-DoF controllers. Ablations show that simulation 

bootstraps basic competence, while real data and the discriminator are key for dexterity and smooth control. 

Looking forward, we see two promising directions: (i) contact-aware control via tactile sensing to close the loop on tasks like cap twisting; (ii) long-horizon reasoning and hierarchical VLA planning that combines memory, subgoal decomposition, and language-guided tool use. We hope the released models, data, and code catalyze research toward broadly capable, dexterous robot assistants. 

## REFERENCES 

- [1] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid, _et al._ , “Rt-2: Vision-language-action models transfer web knowledge to robotic control,” in _CoRL_ , PMLR, 2023. 

- [2] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi, _et al._ , “Openvla: An open-source vision-language-action model,” _arXiv preprint arXiv:2406.09246_ , 2024. 

- [3] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter, _et al._ , “ _π_ 0: A visionlanguage-action flow model for general robot control,” _arXiv preprint arXiv:2410.24164_ , 2024. 

- [4] P. Intelligence, K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, _et al._ , “ _π_ 0 _._ 5: a vision-language-action model with open-world generalization,” _arXiv preprint arXiv:2504.16054_ , 2025. 

- [5] S. Liu, L. Wu, B. Li, H. Tan, H. Chen, Z. Wang, K. Xu, H. Su, and J. Zhu, “Rdt-1b: a diffusion foundation model for bimanual manipulation,” _arXiv preprint arXiv:2410.07864_ , 2024. 

- [6] C. Cheang, S. Chen, Z. Cui, Y. Hu, L. Huang, T. Kong, H. Li, Y. Li, Y. Liu, X. Ma, _et al._ , “Gr-3 technical report,” _arXiv preprint arXiv:2507.15493_ , 2025. 

- [7] J. Bjorck, F. Casta˜neda, N. Cherniadev, X. Da, R. Ding, L. Fan, Y. Fang, D. Fox, F. Hu, S. Huang, _et al._ , “Gr00t n1: An open foundation model for generalist humanoid robots,” _arXiv preprint arXiv:2503.14734_ , 2025. 

- [8] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn, “Learning fine-grained bimanual manipulation with low-cost hardware,” _RSS_ , 2023. 

- [9] A. . Team, “Aloha 2: An enhanced low-cost hardware for bimanual teleoperation,” _arXiv preprint arXiv:2405.02292_ , 2024. 

- [10] A. Iyer, Z. Peng, Y. Dai, I. Guzey, S. Haldar, S. Chintala, and L. Pinto, “Open teach: A versatile teleoperation system for robotic manipulation,” _CoRL_ , 2024. 

- [11] R. Ding, Y. Qin, J. Zhu, C. Jia, S. Yang, R. Yang, X. Qi, and X. Wang, “Bunny-visionpro: Real-time bimanual dexterous teleoperation for imitation learning,” _arXiv preprint arXiv:2407.03162_ , 2024. 

- [12] Y. Qin, W. Yang, B. Huang, K. Van Wyk, H. Su, X. Wang, Y.-W. Chao, and D. Fox, “Anyteleop: A general vision-based dexterous robot armhand teleoperation system,” _RSS_ , 2023. 

- [13] S. Li, X. Ma, H. Liang, M. G¨orner, P. Ruppel, B. Fang, F. Sun, and J. Zhang, “Vision-based teleoperation of shadow dexterous hand using end-to-end deep neural network,” _ICRA_ , 2019. 

- [14] H. Fang, H.-S. Fang, Y. Wang, J. Ren, J. Chen, R. Zhang, W. Wang, and C. Lu, “Airexo: Low-cost exoskeletons for learning whole-arm manipulation in the wild,” _ICRA_ , 2024. 

- [15] M. Xu, H. Zhang, Y. Hou, Z. Xu, L. Fan, M. Veloso, and S. Song, “Dexumi: Using human hand as the universal manipulation interface for dexterous manipulation,” _CoRL_ , 2025. 

- [16] A. Imdieke and K. Desingh, “Spark-remote: A cost-effective system for remote bimanual robot teleoperation,” _arXiv preprint arXiv:2504.05488_ , 2025. 

- [17] P. Wu, Y. Shentu, Z. Yi, X. Lin, and P. Abbeel, “Gello: A general, lowcost, and intuitive teleoperation framework for robot manipulators,” _IROS_ , 2024. 

- [18] H. Li, Y. Cui, and D. Sadigh, “How to train your robots? the impact of demonstration modality on imitation learning,” _arXiv preprint arXiv:2503.07017_ , 2025. 

- [19] C. Pan, K. Junge, and J. Hughes, “Vision-language-action model and diffusion policy switching enables dexterous control of an anthropomorphic hand,” _arXiv preprint arXiv:2410.14022_ , 2024. 

- [20] J. Zhang, H. Liu, D. Li, X. Yu, H. Geng, Y. Ding, J. Chen, and H. Wang, “Dexgraspnet 2.0: Learning generative dexterous grasping in large-scale synthetic cluttered scenes,” in _8th CoRL_ , 2024. 

- [21] J. Ye, K. Wang, C. Yuan, R. Yang, Y. Li, J. Zhu, Y. Qin, X. Zou, and X. Wang, “Dex1b: Learning with 1b demonstrations for dexterous manipulation,” _arXiv preprint arXiv:2506.17198_ , 2025. 

- [22] Y. Ye, A. Gupta, K. Kitani, and S. Tulsiani, “G-hop: Generative handobject prior for interaction reconstruction and grasp synthesis,” in _CVPR_ , pp. 1911–1920, 2024. 

- [23] Y. Zhong, Q. Jiang, J. Yu, and Y. Ma, “Dexgrasp anything: Towards universal robotic dexterous grasping with physics awareness,” in _CVPR_ , pp. 22584–22594, 2025. 

- [24] Y. Xu, W. Wan, J. Zhang, H. Liu, Z. Shan, H. Shen, R. Wang, H. Geng, Y. Weng, J. Chen, _et al._ , “Unidexgrasp: Universal robotic dexterous grasping via learning diverse proposal generation and goal-conditioned policy,” in _CVPR_ , pp. 4737–4746, 2023. 

- [25] K. Li, J. Wang, L. Yang, C. Lu, and B. Dai, “Semgrasp: Semantic grasp generation via language aligned discretization,” in _ECCV_ , 2024. 

- [26] Y. Liu, Y. Yang, Y. Wang, X. Wu, J. Wang, Y. Yao, S. Schwertfeger, S. Yang, W. Wang, J. Yu, _et al._ , “Realdex: Towards human-like grasping for robotic dexterous hand,” _arXiv:2402.13853_ , 2024. 

- [27] J. Chen, Y. Ke, L. Peng, and H. Wang, “Dexonomy: Synthesizing all dexterous grasp types in a grasp taxonomy,” _arXiv preprint arXiv:2504.18829_ , 2025. 

- [28] H. Zhang, Z. Wu, L. Huang, S. Christen, and J. Song, “Robustdexgrasp: Robust dexterous grasping of general objects,” _arXiv preprint arXiv:2504.05287_ , 2025. 

- [29] K. Li, P. Li, T. Liu, Y. Li, and S. Huang, “Maniptrans: Efficient dexterous bimanual manipulation transfer via residual learning,” in _CVPR_ , pp. 6991–7003, 2025. 

- [30] Z. Jiang, Y. Xie, K. Lin, Z. Xu, W. Wan, A. Mandlekar, L. Fan, and Y. Zhu, “Dexmimicgen: Automated data generation for bimanual dexterous manipulation via imitation learning,” _arXiv preprint arXiv:2410.24185_ , 2024. 

- [31] R. Yang, Q. Yu, Y. Wu, R. Yan, B. Li, A.-C. Cheng, X. Zou, Y. Fang, H. Yin, S. Liu, _et al._ , “Egovla: Learning vision-language-action models from egocentric human videos,” _arXiv:2507.12440_ , 2025. 

- [32] Z. Zhang, H. Xu, Z. Yang, C. Yue, Z. Lin, H.-a. Gao, Z. Wang, and H. Zhao, “Ta-vla: Elucidating the design space of torque-aware visionlanguage-action models,” _arXiv preprint arXiv:2509.07962_ , 2025. 

- [33] Z. Zhang, C. Yue, H. Xu, M. Liao, X. Qi, H.-a. Gao, Z. Wang, and H. Zhao, “Robochemist: Long-horizon and safety-compliant robotic chemical experimentation,” _arXiv preprint arXiv:2509.08820_ , 2025. 

- [34] S. Deng, M. Yan, S. Wei, H. Ma, Y. Yang, J. Chen, Z. Zhang, T. Yang, X. Zhang, H. Cui, _et al._ , “Graspvla: a grasping foundation model pre-trained on billion-scale synthetic action data,” _arXiv preprint arXiv:2505.03233_ , 2025. 

- [35] Q. Bu, J. Cai, L. Chen, X. Cui, Y. Ding, S. Feng, S. Gao, X. He, X. Hu, X. Huang, _et al._ , “Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems,” _arXiv preprint arXiv:2503.06669_ , 2025. 

- [36] Y. Zhong, X. Huang, R. Li, C. Zhang, Y. Liang, Y. Yang, and Y. Chen, “Dexgraspvla: A vision-language-action framework towards general dexterous grasping,” _arXiv preprint arXiv:2502.20900_ , 2025. 

- [37] H. Luo, Y. Feng, W. Zhang, S. Zheng, Y. Wang, H. Yuan, J. Liu, C. Xu, Q. Jin, and Z. Lu, “Being-h0: Vision-language-action pretraining from large-scale human videos,” _arXiv preprint arXiv:2507.15597_ , 2025. 

- [38] J. Jang, S. Ye, Z. Lin, J. Xiang, J. Bjorck, Y. Fang, F. Hu, S. Huang, K. Kundalia, Y.-C. Lin, _et al._ , “Dreamgen: Unlocking generalization in robot learning through neural trajectories,” pp. arXiv–2505, 2025. 

- [39] S. Bai, K. Chen, X. Liu, J. Wang, W. Ge, S. Song, K. Dang, P. Wang, S. Wang, J. Tang, _et al._ , “Qwen2. 5-vl technical report,” _arXiv preprint arXiv:2502.13923_ , 2025. 

- [40] M. Deitke, R. Liu, M. Wallingford, H. Ngo, O. Michel, A. Kusupati, A. Fan, C. Laforte, V. Voleti, S. Y. Gadre, _et al._ , “Objaverse-xl: A universe of 10m+ 3d objects,” _NeurIPS_ , vol. 36, 2023. 

- [41] C. Raffel, N. Shazeer, A. Roberts, K. Lee, S. Narang, M. Matena, Y. Zhou, W. Li, and P. J. Liu, “Exploring the limits of transfer learning with a unified text-to-text transformer,” _JMLR_ , vol. 21, pp. 1–67, 2020. 

- [42] X. Zhai, B. Mustafa, A. Kolesnikov, and L. Beyer, “Sigmoid loss for language image pre-training,” in _Proceedings of the IEEE/CVF international conference on computer vision_ , pp. 11975–11986, 2023. 

- [43] H. Xu, X. Zhan, H. Yin, and H. Qin, “Discriminator-weighted offline imitation learning from suboptimal demonstrations,” in _International Conference on Machine Learning_ , pp. 24725–24742, PMLR, 2022. 

- [44] C. Chi, Z. Xu, S. Feng, E. Cousineau, Y. Du, B. Burchfiel, R. Tedrake, and S. Song, “Diffusion policy: Visuomotor policy learning via action diffusion,” _IJRR_ , 2023. 

