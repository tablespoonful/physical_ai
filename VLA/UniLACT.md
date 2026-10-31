---
title: "UniLACT: Depth-Aware RGB Latent Action Learning for Vision-Language-Action Models"
date: "2026-02-23"
authors: "Manish Kumar Govind; Dominick Reilly; Pu Wang; Srijan Das"
url: https://arxiv.org/abs/2602.20231
pdf: https://arxiv.org/pdf/2602.20231
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.20231)** / [論文ページ](https://arxiv.org/abs/2602.20231)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **UNILACT: Depth-Aware RGB Latent Action Learning for Vision-Language-Action Models** 

Manish Kumar Govind<sup>_∗_</sup> , Dominick Reilly, Pu Wang, Srijan Das 

**_Abstract_ — Latent action representations learned from unlabeled videos have recently emerged as a promising paradigm for pretraining vision-language-action (VLA) models without explicit robot action supervision. However, latent actions derived solely from RGB observations primarily encode appearancedriven dynamics and lack explicit 3D geometric structure, which is essential for precise and contact-rich manipulation. To address this limitation, we introduce UNILACT, a transformer-based VLA model that incorporates geometric structure through depth-aware latent pretraining, enabling downstream policies to inherit stronger spatial priors. To facilitate this process, we propose UNILARN, a unified latent action learning framework based on inverse and forward dynamics objectives that learns a shared embedding space for RGB and depth while explicitly modeling their cross-modal interactions. This formulation produces modality-specific and unified latent action representations that serve as pseudo-labels for the depthaware pretraining of UNILACT. Extensive experiments in both simulation and real-world settings demonstrate the effectiveness of depth-aware unified latent action representations. UNILACT consistently outperforms RGB-based latent action baselines under in-domain and out-of-domain pretraining regimes, as well as on both seen and unseen manipulation tasks. The project page is at https://manishgovind.github.io/ unilact-vla/.** 

## I. INTRODUCTION 

Vision-Language-Action (VLAs) models have recently enabled robot policies that generalize across novel tasks, unseen objects, and moderate distribution shifts [1], [2], [3], [4], [5]. However, most existing VLAs rely on largescale robotic data often collected via human teleoperation, which makes pretraining expensive and difficult to scale. Therefore, to reduce dependency on such costly teleoperated data, recent work explores unsupervised pretraining from widely available, unlabeled internet-scale videos using latent action representations, and then transferring these priors to downstream robot tasks with limited supervision [6], [7], [8], [9], [10], [11]. 

Latent action representations typically learn the action priors from consecutive video frames using inverse dynamics model (IDM) and forward dynamics model (FDM) [7], [12]. While this paradigm reduces reliance on costly robotannotated demonstrations, existing approaches learn latent action representations solely from RGB observations [10], [11]. This means the learned latents capture appearancedriven dynamics while remaining blind to 3D geometric structure, information that is critical for contact-rich manipulation tasks such as precise grasping, placement, and collision 

All authors are with the Department of Computer Science, University of North Carolina at Charlotte, NC, USA. *Corresponding author: mgovind@charlotte.edu. 

avoidance. A robot policy that cannot embed reasoning about depth in its action representations will struggle to perceive, for example, _whether an object of interest is within reach or if a collision is about to occur_ . 

Prior work has shown that incorporating depth into VLA _policies_ improves spatial reasoning [13], [14], [15], [16]. However, these methods treat depth as a pixel or featurelevel input to the policy network and still require substantial robot-annotated trajectory data for training. Crucially, it is under-explored whether depth can enhance the _RGB-based latent action representations themselves_ , that is, **whether geometric structure can be embedded within the RGB latent space during unsupervised pretraining so that downstream policies inherit stronger spatial priors without requiring additional labeled data.** 

To this end, we introduce UNILACT ( **Uni** fied **L** atent **Ac** tion **T** ransformer), a VLA that leverages unsupervised pretraining with depth-aware latent action representations derived from RGB-D observations. To obtain such depthaware representations, we propose UNILARN ( **Uni** fied **L** atent **A** ction lea **RN** ing), an IDM–FDM-based framework that learns a shared embedding space for RGB and depth while explicitly modeling their cross-modal interactions. Close to our work, UniSkill [17] also incorporates depth into latent representations but to learn generic, embodiment agnostic skills within a joint embedding space. However, UNILARN is designed to produce both modality-specific and unified latent action representations within a shared latent space, which are used as pseudo action labels to pretrain UNILACT. This formulation enables UNILACT to fully exploit the complementary semantics of RGB and the geometry grounded structure of depth, yielding a more scalable pretraining paradigm compared to UniSkill. During latent pretraining, UNILACT is trained to predict latent action targets conditioned on visual observations and task instructions, enabling it to encode complementary semantic and geometric cues. The learned representations are subsequently fine-tuned with limited action supervision to produce executable control commands for downstream manipulation tasks. Notably, depth is used only during training; at inference time, UNILACT operates solely on RGB observations and task instructions. 

To validate our approach, we evaluate UNILACT in both simulation and real-world settings. On simulation benchmarks, UNILACT achieves a 29.2% relative improvement over a purely RGB-based latent baseline [10]. Real-world experiments further corroborate these gains, with UNILACT demonstrating more stable grasping and improved collision 

avoidance, highlighting the benefits of incorporating geometric structure via depth during pretraining. In summary, our contributions are as follows: 

- We propose **UNILARN** , a unified latent action learning framework that leverages inverse and forward dynamics to jointly learn modality-specific and unified latent action representations within a shared latent space, capturing both visual semantics and 3D geometric structure. 

- We introduce **UNILACT** , a cross-modally trained VLA that leverages both unified and modality-specific latent representations to improve policy learning. By integrating complementary semantic (RGB) and geometric (depth) information, UNILACT enables more precise and generalizable robot manipulation. 

- Through extensive simulation and real-world experiments, we show that unified latent representations improve 3D spatial understanding compared to RGB based latent approaches. 

## II. RELATED WORK 

## _A. Vision-Language-Action Models._ 

Early work [18], [1], [19], [5], [20], [21] leverage the large-scale pretraining capabilities of VLMs to predict actions by replacing or introducing discrete action tokens into the vocabulary of the underlying language model. Alternative work [2], [4], [22], [23] also build upon VLM backbones but introduce dedicated action expert or heads to learn task-specific control policies. Beyond direct action prediction, VLAs have been extended toward multimodal reasoning and hierarchical control. Several methods [24], [25], [26] emphasize multimodal grounding and reasoning, while hierarchical architectures such as HAMSTER [27] and Hi-Robot [28] decompose decision making into high-level semantic planning followed by low-level execution. While these methods demonstrate strong generalization, learning low-level control at scale often requires large collection of paired robot trajectories with action supervision, which are expensive to acquire and can limit scalability across diverse embodiments and environments. 

## _B. Latent Action Representations._ 

To address the limitation of cost-effective scalability of VLA policy networks, a line of work on latent action models has emerged. These approaches learn control dynamics in a discrete latent space, enabling VLA pretraining directly from videos without requiring explicit action supervision. Early work such as Genie [6] and LAPO [7] learn discrete latent actions from game environments. Dynamo [8] adopted a similar inverse–forward dynamics approach to learn visual representations. LAPA [9] and Moto-GPT [10] (Moto) extended this paradigm to internet-scale and robot datasets by pretraining vision–language models for robotic policy learning. IGOR [29] learns a latent space by jointly training on human and robot demonstrations. UniVLA [11] introduce task-centric latent tokens for structured action reasoning, while Amplify [30] leverage keypoint trajectories 

as supervision to learn transferable latent actions between humans and robots. Villa-X [31] further enhanced latent representations by incorporating proprioceptive feedback for richer dynamics. Recently, several world models [32], [33], [34] have adopted latent action spaces as a compact interface between perception and control. Despite these advances, most latent action methods learn action abstractions from a _single_ observation modality (typically RGB), and thus the learned latents primarily capture appearance-driven dynamics. Our work differs by learning latent action representations jointly from both _RGB and depth_ , yielding a unified latent action representation that enhances appearance driven dynamics with 3D geometry for more precise manipulation. 

## _C. Enhancing VLAs with Depth._ 

Recent works have explored incorporating multiple visual modalities into VLA frameworks to enhance spatial understanding, perception, and control. In particular, several approaches integrate 3D scene information [14], [13], [35], [15] to improve geometric reasoning for robot manipulation. 3D-VLA [36] builds a 3D-aware VLA using a 3D-based LLM for spatial reasoning. Other methods, such as 3DCaVLA [13], DepthVLA [14], QDepth-VLA [15], Spatial traces[35] employ depth-maps as auxiliary supervision, either by projecting depth features into the language-model embedding space or by introducing explicit depth-prediction heads to guide action learning. SpatialVLA [35] introduces Ego3D position encoding and adaptive action grids, enabling precise 3D grounding and reasoning in VLAs. 

However, these approaches processes depth at the pixel or feature level rather than integrating 3D cues into the action abstraction itself. Incorporating depth into _latent action_ representations therefore remains under-explored. A closely related work to ours is UniSkill [17], which learns embodiment agnostic skill representations from unlabeled human videos. While UniSkill leverages both RGB and depth inputs to learn generic skill representations, it primarily focuses on learning a common embedding space for the modalities jointly. In contrast, UNILACT first integrates RGB and depth signals and subsequently disentangles them to learn both unified and modality-specific latent action representations. This design enables VLAs to perform cross modal latent pretraining that transfers complementary semantic cues from RGB and geometry grounded structure from depth, thereby providing scalable and structured pretraining signals. 

## III. PROPOSED METHOD 

The goal of our proposed method is to leverage depth information within a latent action representation and provide a scalable framework for robot policy learning. To this end, we introduce UNILACT, a transformer-based Vision-LanguageAction Model as illustrated in Figure 1, and describe its key components. The training of UNILACT consists of three stages: (i) unified latent action learning, (ii) unified latent pretraining, and (iii) action fine-tuning, which are described chronologically in Sections III-A–III-C. In the first stage, we learn modality-specific latent action representations from 


Fig. 1. **Overview of UNILACT’S three stages:** (1) UNILARN learns modality-specific (RGB/depth) and unified discrete latent actions from pairs of RGB-D frames within a shared latent space. (2) UNILACT is pretrained with cross-modal autoregressive latent-token prediction to capture complementary priors from RGB appearance and depth geometry. (3) UNILACT is fine-tuned on action-labeled trajectories to map predicted latent actions to executable robot actions. 

RGB and depth observations using a unified latent learning framework, UNILARN. In the second stage, UNILACT is pretrained to predict these modality-specific and unified latent actions, enabling action supervision without explicit action annotations. Finally, in the third stage, UNILACT is fine-tuned on robot demonstrations to map the predicted unified latent actions to an executable robot policy. 

## _A._ UNILARN _:_ _<u>Unified Latent Action Learning</u>_ 

Given paired RGB and depth observations, UNILARN aims to learn modality-specific latent action representations together with a unified latent action representation that embeds discriminative dynamic patterns into a shared semantic embedding space. To achieve this, UNILARN learns latent action representations and their cross-modal relationships through a two-stage vector-quantization pipeline. For each modality, an inverse dynamics model (IDM) first maps paired observations to a continuous latent embedding, which is subsequently discretized using a shared vector-quantization operator. The resulting modality-specific discrete latents are then fused and re-quantized to produce a unified latent representation. This unified latent is finally used to condition modality-specific forward dynamics models (FDM), ensuring that it retains sufficient information to predict future observations in each modality, thereby preserving complementary dynamics across modalities. 

Formally, we consider paired observations � _o_<sup>_m_</sup> _t_<sup>_, om_</sup> _t_ + _H_ � corresponding to the current and future frames of modality _m_ , where _H_ denotes the temporal offset and _m ∈{_ r _,_ d _}_ indicates RGB or depth, respectively. For each modality _m_ , an IDM _Im_ maps the observation pair to a continuous latent 

## embedding, 


This embedding is discretized by a vector-quantization operator VQ with respect to a codebook _C_<sup>(</sup><sup>_s_)</sup> shared across both RGB and depth modalities. Thus, the modality-specific latent action representation is given by 


Subsequently, modality-specific codebook embeddings **e**<sup>_m_</sup> _t_ are obtained by 


which are then concatenated and linearly projected into a continuous unified latent space such that, 


where **W** _f_ and **b** _f_ are the parameters of the linear projector. Then, the projected representation **h** _t_ is discretized by a second vector-quantization operator with respect to another codebook _C_<sup>(</sup><sup>_u_)</sup> , 


Finally, the unified latent action representation _zt_<sup>_u_isused</sup> together with each modality’s current observation _o_<sup>_m_</sup> _t_<sup>to con-</sup> dition modality-specific FDM _Fm_ for reconstructing future observations as 


This disentangled reconstruction objective across modalityspecific domains enforces the unified representation _zt_<sup>_u_to</sup> 

capture the complementary dynamics of each modality. We refer to this complete parameterized model, which takes RGB and depth observations as input to learn both modalityspecific and unified latent representations, as UNILARN. 

## _B. Unified Latent Pretraining._ 

We use the pretrained UNILARN encoder to extract modality-specific ( _zt_<sup>_r, z_</sup> _t_<sup>_d_)andunifiedlatentactiontokens</sup> ( _zt_<sup>_u_)fromRGB-Dvideos,whichserveasanaction-free</sup> supervisory signal for VLA pretraining. Given a visual observation _ot_ , a task instruction _l_ , and a unified latent representation _zt_<sup>_u_,wetrainanautoregressivetransformer,</sup> termed UNILACT, to predict a target latent token sequence _z_ 1:<sup>_m_</sup> _N_<sup>where</sup><sup>_m ∈{r, d, u}_indicates whether the target tokens</sup> correspond to RGB, depth or unified latents. UNILACT factorizes the conditional distribution as 


To encourage the model to internalize complementary semantic and geometric cues, UNILACT conditions on the unified latent representation and is trained to predict one of the latent types produced by UNILARN: RGB, depth, or unified. This cross-modal latent prediction setup explicitly promotes alignment between modality-specific and unified latent spaces, while retaining modality-specific structure. Thus, the unified latent pretraining in UNILACT uses a standard autoregressive next-token prediction objective as 


## _C. Action Fine-Tuning_ 

Unified latent pretraining enables UNILACT to predict discrete latent action tokens; however, these tokens are _not_ directly executable on a robot. Therefore, to enable robot control in UNILACT, we append action query tokens to the input sequence alongside visual, language, and unified latent tokens, and map the corresponding transformer outputs to continuous robot actions via a lightweight action decoder. 

During this stage, UNILACT is fine-tuned to predict real robot actions. The action decoder outputs 7-DoF endeffector deltas, consisting of positional offsets ∆ **p** _∈_ R<sup>3</sup> , rotational offsets ∆ **r** _∈_ R<sup>3</sup> , and a binary gripper command _g ∈{_ 0 _,_ 1 _}_ . The continuous components are trained using an L1 regression loss, while the gripper command is optimized with a binary cross-entropy loss: 


To preserve the pretrained latent structure while learning a robot policy, we fine-tune UNILACT using a convex combination of the unified latent action prediction and actual action prediction, where _L_<sup>_u_</sup> latent<sup>is the unified-latent next-token</sup> prediction loss (no RGB, depth latent action prediction): 


At **inference** time, UNILACT requires only RGB observations and task instructions as input. The depth modality is used exclusively during training to learn a unified latent action representation and is not required at test time. 

## IV. EXPERIMENTS 

In this section, we first describe the implementation details and experimental benchmarks. We then evaluate the policy performance of UNILACT in both simulation and real-world environments. Finally, we analyze the run-time complexity of our model and key design choices through a comprehensive ablation study. 

## _A. Implementation details_ 

UNILACT is implemented in PyTorch and all of our experiments are conducted on 4 NVIDIA H200 GPUs. **UNILARN** primarily consists of modality-specific IDMs, FDMs, and Discretization modules. Each IDM per modality consists of a visual encoder which is a frozen ViT-L encoder [37] initialized with MAE [38] pretrained weights followed by a spatio-temporal transformer. We append learnable query embeddings to the patch features before processing them using in the transformer to capture spatiotemporal changes between frames. The resulting features are discretized using a standard VQ-VAE objective [39], which maps continuous representations to a fixed codebook of latent action tokens. Each FDM is implemented as a ViT-B style decoder [37] and is trained with MSE reconstruction loss to reconstruct target observations. 

**UNILACT** is built upon the GPT-2 causal transformer backbone [40]. We encode task instructions using a frozen T5 encoder [41], and visual inputs are processed using ViTL [37] vision encoder. To predict latent actions and real robot actions, we employ a latent decoder and an action decoder. The latent decoder uses a linear layer to project hidden states into discrete latent actions. The action decoder consists of a 2-layer MLP, followed by separate linear layers that output continuous robot arm actions and a binary gripper command. 

## _B. CALVIN Experiments_ 

We first evaluate UNILACT on the CALVIN benchmark [42], a simulated benchmark designed for long-horizon, multi-task, language-conditioned manipulation tasks. **Training Data.** The CALVIN benchmark consists of four environments (A, B, C, and D) and 34 manipulation tasks, providing approximately 18K trajectories that include RGBD observations and natural language annotations. We follow the challenging ABC _→_ D setting, where models are trained on data from environments A, B, and C, and evaluated in the unseen environment D to assess generalization. 

For in-domain training, we adopt the same setup as [43], using only the language-annotated ABC datasets for VLA pretraining to ensure fair comparison. We additionally report results with out-of-domain pretraining, where UNILACT is pretrained on a subset of the Open X-Embodiment (OXE) dataset [19]. 

**Evaluation.** We follow the standard evaluation protocol from [42]. Each policy is evaluated over 1,000 episodes. In each 

episode, the robot needs to accomplish a sequence of five consecutive tasks. Each task is allowed up to maximum of 360 action steps unless successfully completed earlier. Performance is reported using per-task success rates and the average sequence length ( _Avg. Len._ ), defined as the average number of consecutive tasks completed within each episode. **Results.** On the CALVIN ABC _→_ D benchmark, policy learning approaches broadly fall into several categories, including (1) language-conditioned behavioral cloning, (2) diffusionbased policies, and (3) planner–executor frameworks. Our method belongs to the first category; therefore, Table I compares against representative baselines within this group. We report results under both in-domain and out-of-domain pretraining settings. 

For <u>in-domain</u> results, since we follow the evaluation protocol of prior work [43], [10], baseline numbers are directly taken from these references. We reproduce results of Moto [10], an RGB latent-action-based approach most closely related to our method. Under comparable settings, UNILACT consistently outperforms Moto, demonstrating the benefit of incorporating depth into the latent action representation. We also observe that UNILACT surpasses baselines operating with comparable input modalities. Although GR-1 reports the strongest overall performance, it relies on additional inputs such as gripper-view RGB images and proprioceptive state signals, whereas UNILACT uses only static RGB observations. 

For <u>out-of-domain</u> pretraining on OXE, UNILACT outperforms Moto by +29.2% in average sequence length. This result indicates that the proposed unified latent action representation, learned jointly from RGB and depth modalities, improves generalization and demonstrates robustness and scalability when trained on diverse pretraining data. 

For a better understanding of the role of depth, we further analyze task-level performance on CALVIN (Fig. 2). RGB-based latent representations perform competitively on appearance driven tasks (e.g., _stack blocks_ , _rotate blue block_ ), whereas unified (RGB+depth) latents yield larger gains on geometry-centric tasks (e.g., _move slider_ , _turn on light bulb_ ). These results suggest that incorporating depth enriches the latent action space with stronger geometric priors, which are critical for precise and contact-rich manipulation. 


Fig. 2. **Task-wise success comparison on CALVIN between RGB and unified latent action representations. Top:** tasks where RGB-based latents perform better; **Bottom:** tasks where unified latents(RGB+depth) perform better. 

Fig. 3. **Real-world experimental setup.** The setup consists of an xArm7 manipulator equipped with a two-fingered parallel gripper and a workspace-facing camera mounted on the table. 

## _C. Real-World Experiments_ 

We further evaluate UNILACT on a 7-DoF xArm7 manipulator. Visual observations are captured using an Intel RealSense D435i RGB-D camera mounted in front of the robot, providing a third-person view as illustrated Figure 3. With this setup, we collect 30 demonstrations per task using teleoperation [50], and we evaluate the policies on four tabletop manipulation tasks described below: 

T1: Pick up the carrot and place it in a bowl. The robot must pick up the carrot from the table and place it completely inside a bowl. 

T2: Move _<_ object1 _>_ near _<_ object2 _>_ . The robot must move _<_ object1 _>_ such that its final position lies within a 3cm radius of _<_ object2 _>_ . The two objects are randomly selected from a set of eight toys _{eggplant, lemon, banana, peach, carrot, green pepper, strawberry, tomato}_ . 

T3: Put the eggplant into the plate. The robot must pick up the eggplant and place it inside the plate. 

T4: Lift the block. The robot must grasp the block and lift it above a height threshold of 1cm from the table surface. Tasks T1 and T2 are _seen_ during training, whereas T3 and T4 are _unseen_ tasks used to test zero-shot generalization. 

**Training Data.** During unified latent action learning and unified latent pretraining, UNILACT is trained using a subset of the OXE dataset [19] together with collected real-world demonstrations. The model is subsequently fine-tuned using only real-world demonstrations. Since most of the OXE subset does not provide depth observations, we generate depth maps from RGB images using a depth extracting foundational model, Depth-Anything-V2 [51]. 

**Evaluation.** Each task is evaluated over 10 trials with randomized initial object configurations. Performance is reported using per-task success rates and the average success rate across all tasks. 

**Results.** Table II shows that UNILACT consistently outperforms the RGB baseline (which is Moto), achieving higher success rates on 3 out of 4 tasks and **10%** overall improvement across all tasks. This performance improvement indicates that the geometric information encoded in UNILACT’s latent representations significantly enhances the policy’s spatial understanding. We also provide a qualitative comparison of these real-world tasks in Figures 4 and 5 using Moto and UNILACT respectively. In Figure 4, showing Task T1, Moto successfully reaches the carrot but fails to place it in the bowl due to an inaccurate depth prediction, resulting in a collision with the bowl. In contrast, UNILACT demonstrates a superior understanding of depth, accurately positioning the carrot above the bowl and completing the task without any collision. Similarly, in Figure 5 depicting Task T2, Moto fails to _grasp the eggplant_ and subsequently crashes into the workspace surface. However, UNILACT executes a precise grasp and successfully moves the _eggplant near the banana_ . Overall, these real-world results show that UNILACT enhances the depth awareness of latent action representations, allowing for precise manipulation in contactrich tasks. The significant performance gains in both simula- 

TABLE I 

CALVIN ( _ABC → D_ ) BENCHMARK RESULTS. PERFORMANCE METRIC IS THE AVERAGE SEQUENCE LENGTH. HERE ‘*’ REPRESENTS THE RESULTS ARE REPRODUCED WITH OUR TRAINING SETTINGS AND ‘STATIC RGB’,‘ GRIPPER RGB’ REPRESENTS THE STATIC CAMERA AND GRIPPER CAMERA VIEW RESPECTIVELY. ‘PROPRIO.’ DENOTES THE ROBOT PROPRIOCEPTIVE STATE. 

|**Model**|**Observation input**|**T**|**asks Co**|**mpleted **|**in a row**||**Avg. Len** _↑_|
|---|---|---|---|---|---|---|---|
|||T1|T2|T3|T4|T5||
||_CALVIN(ABC_|_) Pretrai_|_ning_|||||
|Diffusion Policy[44]|Static RGB|0.402|0.123|0.026|0.008|0.00|0.56|
|HULC[45]|Static RGB|0.418|0.165|0.057|0.019|0.011|0.67|
|RT-1[46]|Static RGB|0.533|0.222|0.094|0.038|0.013|0.90|
|Robo-Flamingo[47]|(Static + Gripper) RGB|0.824|0.619|0.466|0.331|0.235|2.48|
|SuSIE[48]|Static RGB|0.870|0.690|0.490|0.380|0.260|2.69|
|GR-1[49]|(Static + Gripper) RGB + Proprio.|0.854|0.712|0.596|0.497|0.401|3.06|
|Moto[10]*|Static RGB|0.827|0.637|0.485|0.374|0.278|2.60|
|**UNILACT (Ours)**|Static RGB|**0.855**|**0.689**|**0.543**|**0.440**|**0.332**|**2.86**|
||_OXE Pre_|_training_||||||
|Moto[10]*|Static RGB|0.824|0.60|0.439|0.316|0.228|2.40|
|**UNILACT (Ours)**|Static RGB|**0.897**|**0.729**|**0.584**|**0.493**|**0.401**|**3.10**|


### TABLE II 

**REAL-WORLD RESULTS.** PERFORMANCE COMPARISON OF BASELINE MOTO AND UNILACT ON FOUR REAL-WORLD MANIPULATION TASKS, REPORTED UNDER SEEN AND UNSEEN TASK SETTINGS IN TERMS OF SUCCESS RATE(%). 

||**Seen Ta**|**sks**|**Unseen Tas**|**ks**||
|---|---|---|---|---|---|
|**Method**|Put carrot in bowl|Move near|Put eggplant in plate|Lift block|**Avg.**|
|Moto [10]|70.0|40.0|**70.0**|30.0|52.5|
|**UNILACT**|**90.0 (+20)**|**60.0 (+20)**|60.0 (-10)|**40.0 (+10)**|**62.5 (+10)**|


tion and physical experiments suggest that UNILACT better interprets the 3D structure of the environment compared to methods relying on appearance-only latents. 

Fig. 5. **Illustration of Task T2:** “Move the eggplant near the banana.” **Top row:** Moto approaches the eggplant but fails to grasp it and collides with the workspace. **Bottom row:** UNILACT successfully grasps the eggplant and moves it near the banana. 

Moto. This is enabled by the design of UNILACT, which requires the additional depth modality only during training and does not use it during inference. 

## _E. Ablation studies_ 

Fig. 4. **Illustration of Task T1:** “Pick up the carrot and place it in the bowl.” **Top row:** Moto fails to place the carrot inside the bowl and pushes the bowl out of the workspace. **Bottom row:** UNILACT successfully completes the task. 

## _D. Computational Analysis_ 

We compare the computational complexity of UNILACT with the RGB-based latent action VLA model (Moto). Table III reports the number of model parameters and the perstep inference latency. Despite incorporating both RGB and depth information into a unified latent space during training, UNILACT maintains the same model size and runtime as 

We conduct ablation studies on the CALVIN ABC _→_ D benchmark. We report the average sequence length to assess (a) the effectiveness of various visual modalities, (b) the impact of various output modalities using unified latent actions while pretraining and fine-tuning, and (c) the impact of multi-task and single-task learning. 

|TABLE III|TABLE IV||
|---|---|---|
|MODEL PARAMETERS AND|ABLATION ON VISUAL MOD|ALITY.|
|LATENCYOFUNILACT LATENCY|||
|.<br>ISMEASUREDPERINFERENCE|**Latent Modality**|**Avg. Len** _↑_|
|<br>|No latent actions|0.744|
|STEP.|RGB|2.601|
||Depth|2.402|
|**Model**<br>**#Params (M)**<br>**Latency (ms)**|RGB+Depth|2.080|
|Moto<br>89.8<br>27|Unified|2.254|
|UNILACT<br>89.8<br>27|**Unified + Modality-specific**|**2.859**|


TABLE V 

TABLE VI 

ABLATION ON TYPES OF OUTPUT TABLE VI MODALITIES IN STAGES 2 & 3. ABLATION COMPARING _{_ U, R, D _}_ DENOTE _{_ UNIFIED, MULTI-TASK AND SINGLE-TASK RGB, DEPTH _}_ LATENT ACTIONS. LEARNING OBJECTIVES. 

|**Pretrain modality**|**Finetune modality**|**Avg. Len** _↑_|**Variant**|**Avg. Len** _↑_|
|---|---|---|---|---|
|(input _→_output)<br>_U →{U, R, D}_<br>_U →U_|(input _→_output )<br>_U →{U, R, D}_<br>_U →U_|2.299<br>2.597|Multi-task<br>**Single-task**|2.055<br>**2.859**|
|_U →{U, R, D}_|_U →U_|**2.859**|||


modal latent action prediction that leverages both unified and modality-specific latent actions. Experiments on simulation and real-world tasks validate the benefits of integrating depth into latent action representations, consistently outperforming representative baselines. Our results show that learning a unified latent space that capture semantic and geometric cues leads to improved downstream robot policy learning emphasizing the importance of depth. 

## ACKNOWLEDGMENT 

**Impact of visual modality.** Table IV analyzes how latent actions from different visual modalities contribute to policy learning. Both RGB and depth-based latent actions significantly outperform the no-latent baseline, confirming that pretraining provides essential complementary motion priors. We further compared UNILACT against a naive multimodal approach where RGB and depth latent actions are learned independently. In this setup, the model is trained with alternating supervision, where individual training batches are supervised by either RGB or depth latent actions. Although both modalities are used, learning modality-specific latents independently leads to representation inconsistency, resulting in performance drop compared to individual modalities. We also evaluate a UniSkill-style variant ( _Unified_ ) that learns only a joint latent space without modality-specific latents. While _Unified_ improves over _RGB+Depth_ , the best results are achieved by UNILACT (Unified + Modality-specific), which jointly aligns RGB and depth in a shared latent space while retaining modality-specific latents. 

**Impact of different output modalities.** Next, we study whether pretraining and fine-tuning should predict all three latent types (RGB, depth, and unified) or only the unified latent. Table V shows that pretraining with cross-modal targets (U _→{_ U _,_ R _,_ D _}_ ) and fine-tuning only on the unified latent (U _→_ U) yield the best results. This suggests that cross-modal supervision enriches the latent space during pretraining, while a compact unified target at fine-tuning leads to more effective action prediction. Note that all models are trained for a fixed number of iterations to ensure a fair comparison. 

**Impact of training objectives.** We compare single-task and multi-task training settings (Table VI). In both cases, the input to the model is the unified latent. In the multi-task setting, the model jointly predicts RGB, depth, and unified latents, whereas in the single-task setting it predicts one modality at a time. The single-task variant achieves higher performance. This suggests that jointly optimizing multiple latent objectives may introduce task interference, leading to less effective optimization. 

## V. CONCLUSION 

In this work, we demonstrate the effectiveness of depthaware latent action representations in vision–language–action (VLA) models. We propose UNILARN, a unified latent action learning framework that jointly learns representations from RGB and depth observations. Building on this, we introduce UNILACT, a VLA pretrained through cross- 

This work was supported in part by the National Science Foundation (IIS-2245652) and the University of North Carolina at Charlotte. Computational resources were provided by the NSF National AI Research Resource Pilot (NAIRR240338) and NCShare. We thank Nitin Chandrasekhar for collecting the teleoperation trajectories. We would also like to thank Xiang Li and Hieu Le for our valuable discussions. 

## REFERENCES 

- [1] M. J. Kim, _et al._ , “Openvla: An open-source vision-language-action model,” 2024. [Online]. Available: https://arxiv.org/abs/2406.09246 

- [2] K. Black, _et al._ , “ _π_ 0: A vision-language-action flow model for general robot control,” 2024. [Online]. Available: https: //arxiv.org/abs/2410.24164 

- [3] A. Goyal, H. Hadfield, X. Yang, V. Blukis, and F. Ramos, “Vla-0: Building state-of-the-art vlas with zero modification,” 2025. [Online]. Available: https://arxiv.org/abs/2510.13054 

- [4] X. Li, _et al._ , “Vision-language foundation models as effective robot imitators,” 2024. [Online]. Available: https://arxiv.org/abs/2311.01378 

- [5] C.-L. Cheang, _et al._ , “Gr-2: A generative video-language-action model with web-scale knowledge for robot manipulation,” 2024. [Online]. Available: https://arxiv.org/abs/2410.06158 

- [6] J. Bruce, _et al._ , “Genie: Generative interactive environments,” 2024. [Online]. Available: https://arxiv.org/abs/2402.15391 

- [7] D. Schmidt and M. Jiang, “Learning to act without actions,” 2024. [Online]. Available: https://arxiv.org/abs/2312.10812 

- [8] Z. J. Cui, H. Pan, A. Iyer, S. Haldar, and L. Pinto, “Dynamo: In-domain dynamics pretraining for visuo-motor control,” 2024. [Online]. Available: https://arxiv.org/abs/2409.12192 

- [9] S. Ye, _et al._ , “Latent action pretraining from videos,” 2025. [Online]. Available: https://arxiv.org/abs/2410.11758 

- [10] Y. Chen, Y. Ge, W. Tang, Y. Li, Y. Ge, M. Ding, Y. Shan, and X. Liu, “Moto: Latent Motion Token as the Bridging Language for Learning Robot Manipulation from Videos,” Mar. 2025, arXiv:2412.04445 [cs]. [Online]. Available: http://arxiv.org/abs/2412.04445 

- [11] Q. Bu, Y. Yang, J. Cai, S. Gao, G. Ren, M. Yao, P. Luo, and H. Li, “Univla: Learning to act anywhere with task-centric latent actions,” 2025. [Online]. Available: https://arxiv.org/abs/2505.06111 

- [12] A. D. Edwards, H. Sahni, Y. Schroecker, and C. L. Isbell, “Imitating latent policies from observation,” 2019. [Online]. Available: https://arxRobotiv.org/abs/1805.07914 

- [13] V. Bhat, Y.-H. Lan, P. Krishnamurthy, R. Karri, and F. Khorrami, “3d cavla: Leveraging depth and 3d context to generalize vision language action models for unseen tasks,” 2025. [Online]. Available: https://arxiv.org/abs/2505.05800 

- [14] T. Yuan, Y. Liu, C. Lu, Z. Chen, T. Jiang, and H. Zhao, “Depthvla: Enhancing vision-language-action models with depth-aware spatial reasoning,” 2025. [Online]. Available: https://arxiv.org/abs/2510.13375 

- [15] Y. Li, Y. Chen, M. Zhou, and H. Li, “Qdepth-vla: Quantized depth prediction as auxiliary supervision for vision-language-action models,” 2025. [Online]. Available: https://arxiv.org/abs/2510.14836 

- [16] D. Qu, _et al._ , “Spatialvla: Exploring spatial representations for visual-language-action model,” 2025. [Online]. Available: https: //arxiv.org/abs/2501.15830 

- [17] H. Kim, J. Kang, H. Kang, M. Cho, S. J. Kim, and Y. Lee, “Uniskill: Imitating human videos via cross-embodiment skill representations,” 2025. [Online]. Available: https://arxiv.org/abs/2505.08787 

- [18] A. Brohan, _et al._ , “Rt-2: Vision-language-action models transfer web knowledge to robotic control,” 2023. [Online]. Available: https://arxiv.org/abs/2307.15818 

- [19] O. X.-E. Collaboration, _et al._ , “Open X-Embodiment: Robotic learning datasets and RT-X models,” https://arxiv.org/abs/2310.08864, 2023. 

- [20] Q. Zhao, _et al._ , “Cot-vla: Visual chain-of-thought reasoning for vision-language-action models,” 2025. [Online]. Available: https://arxiv.org/abs/2503.22020 

- [21] X. Li, _et al._ , “Llara: Supercharging robot learning data for vision-language policy,” 2025. [Online]. Available: https://arxiv.org/ abs/2406.20095 

- [22] Q. Li, _et al._ , “Cogact: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation,” 2024. [Online]. Available: https://arxiv.org/abs/2411.19650 

- [23] NVIDIA, _et al._ , “Gr00t n1: An open foundation model for generalist humanoid robots,” 2025. [Online]. Available: https: //arxiv.org/abs/2503.14734 

- [24] D. Driess, _et al._ , “Palm-e: An embodied multimodal language model,” 2023. [Online]. Available: https://arxiv.org/abs/2303.03378 

- [25] Z. Zhou, _et al._ , “Chatvla: Unified multimodal understanding and robot control with vision-language-action model,” 2025. [Online]. Available: https://arxiv.org/abs/2502.14420 

- [26] Z. Zhou, Y. Zhu, J. Wen, C. Shen, and Y. Xu, “Chatvla-2: Vision-language-action model with open-world embodied reasoning from pretrained knowledge,” 2025. [Online]. Available: https: //arxiv.org/abs/2505.21906 

- [27] Y. Li, _et al._ , “Hamster: Hierarchical action models for open-world robot manipulation,” 2025. [Online]. Available: https://arxiv.org/abs/ 2502.05485 

- [28] L. X. Shi, _et al._ , “Hi robot: Open-ended instruction following with hierarchical vision-language-action models,” 2025. [Online]. Available: https://arxiv.org/abs/2502.19417 

- [29] X. Chen, J. Guo, T. He, C. Zhang, P. Zhang, D. C. Yang, L. Zhao, and J. Bian, “Igor: Image-goal representations are the atomic control units for foundation models in embodied ai,” 2024. [Online]. Available: https://arxiv.org/abs/2411.00785 

   - [42] O. Mees, L. Hermann, E. Rosete-Beas, and W. Burgard, “Calvin: A benchmark for language-conditioned policy learning for longhorizon robot manipulation tasks,” 2022. [Online]. Available: https://arxiv.org/abs/2112.03227 

   - [43] H. Wu, Y. Jing, C. Cheang, G. Chen, J. Xu, X. Li, M. Liu, H. Li, and T. Kong, “Unleashing large-scale video generative pre-training for visual robot manipulation,” 2023. [Online]. Available: https://arxiv.org/abs/2312.13139 

   - [44] C. Chi, Z. Xu, S. Feng, E. Cousineau, Y. Du, B. Burchfiel, R. Tedrake, and S. Song, “Diffusion policy: Visuomotor policy learning via action diffusion,” 2024. [Online]. Available: https://arxiv.org/abs/2303.04137 

   - [45] O. Mees, L. Hermann, and W. Burgard, “What Matters in Language Conditioned Robotic Imitation Learning over Unstructured Data,” Aug. 2022, arXiv:2204.06252 [cs]. [Online]. Available: http://arxiv.org/abs/2204.06252 

   - [46] A. Brohan, _et al._ , “Rt-1: Robotics transformer for real-world control at scale,” 2023. [Online]. Available: https://arxiv.org/abs/2212.06817 

   - [47] X. Li, _et al._ , “Vision-language foundation models as effective robot imitators,” 2024. [Online]. Available: https://arxiv.org/abs/2311.01378 

   - [48] K. Black, M. Nakamoto, P. Atreya, H. Walke, C. Finn, A. Kumar, and S. Levine, “Zero-shot robotic manipulation with pretrained image-editing diffusion models,” 2023. [Online]. Available: https: //arxiv.org/abs/2310.10639 

   - [49] H. Wu, Y. Jing, C. Cheang, G. Chen, J. Xu, X. Li, M. Liu, H. Li, and T. Kong, “Unleashing large-scale video generative pre-training for visual robot manipulation,” 2023. [Online]. Available: https://arxiv.org/abs/2312.13139 

   - [50] A. Khazatsky, _et al._ , “Droid: A large-scale in-the-wild robot manipulation dataset,” 2025. [Online]. Available: https://arxiv.org/abs/ 2403.12945 

   - [51] L. Yang, B. Kang, Z. Huang, Z. Zhao, X. Xu, J. Feng, and H. Zhao, “Depth anything v2,” 2024. [Online]. Available: https://arxiv.org/abs/2406.09414 

- [30] J. A. Collins, L. Cheng, K. Aneja, A. Wilcox, B. Joffe, and A. Garg, “Amplify: Actionless motion priors for robot learning from videos,” 2025. [Online]. Available: https://arxiv.org/abs/2506.14198 

- [31] X. Chen, _et al._ , “villa-x: Enhancing latent action modeling in vision-language-action models,” 2025. [Online]. Available: https: //arxiv.org/abs/2507.23682 

- [32] AgiBot-World-Contributors, _et al._ , “Agibot world colosseo: A largescale manipulation platform for scalable and intelligent embodied systems,” 2025. [Online]. Available: https://arxiv.org/abs/2503.06669 

- [33] S. Gao, S. Zhou, Y. Du, J. Zhang, and C. Gan, “Adaworld: Learning adaptable world models with latent actions,” 2025. [Online]. Available: https://arxiv.org/abs/2503.18938 

- [34] C. Zhu, R. Yu, S. Feng, B. Burchfiel, P. Shah, and A. Gupta, “Unified world models: Coupling video and action diffusion for pretraining on large robotic datasets,” 2025. [Online]. Available: https://arxiv.org/abs/2504.02792 

- [35] M. A. Patratskiy, A. K. Kovalev, and A. I. Panov, “Spatial traces: Enhancing vla models with spatial-temporal understanding,” 2025. [Online]. Available: https://arxiv.org/abs/2508.09032 

- [36] H. Zhen, X. Qiu, P. Chen, J. Yang, X. Yan, Y. Du, Y. Hong, and C. Gan, “3d-vla: A 3d vision-language-action generative world model,” 2024. [Online]. Available: https://arxiv.org/abs/2403.09631 

- [37] A. Dosovitskiy, _et al._ , “An image is worth 16x16 words: Transformers for image recognition at scale,” 2021. [Online]. Available: https://arxiv.org/abs/2010.11929 

- [38] K. He, X. Chen, S. Xie, Y. Li, P. Doll´ar, and R. Girshick, “Masked autoencoders are scalable vision learners,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2022, pp. 16 000–16 009. 

- [39] A. Van Den Oord, O. Vinyals, _et al._ , “Neural discrete representation learning,” _Advances in neural information processing systems_ , vol. 30, 2017. 

- [40] A. Radford, J. Wu, R. Child, D. Luan, D. Amodei, and I. Sutskever, “Language models are unsupervised multitask learners,” 2019. 

- [41] C. Raffel, N. Shazeer, A. Roberts, K. Lee, S. Narang, M. Matena, Y. Zhou, W. Li, and P. J. Liu, “Exploring the limits of transfer learning with a unified text-to-text transformer,” _Journal of Machine Learning Research_ , vol. 21, no. 140, pp. 1–67, 2020. [Online]. Available: http://jmlr.org/papers/v21/20-074.html 

