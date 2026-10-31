---
title: "TAO-Force: Unifying Force-Aware Perception and Fast-Slow Control for Contact-Rich Manipulation"
date: "2026-09-16"
authors: "Bohan Gan; Xuanzhang Wen; Yongsheng Zhao; Baoping Cheng; Wenhe Jia; Ye Wang"
url: https://arxiv.org/abs/2609.18497
pdf: https://arxiv.org/pdf/2609.18497
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2609.18497)** / [論文ページ](https://arxiv.org/abs/2609.18497)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# TAO-Force: Unifying Force-Aware Perception and Fast–Slow Control for Contact-Rich Manipulation 

Bohan Gan, Xuanzhang Wen, Yongsheng Zhao, Baoping Cheng<sup>*</sup> , Wenhe Jia, Ye Wang, Gongxin Yao, Han Gao, Jingyao Tang, Lei Zhao, and Ji Ge China Mobile (Hangzhou) Information Technology Co., Ltd., Hangzhou 310023, China 

_{_ ganbohan, wenxuanzhang, zhaoyongsheng, chengbaoping, jiawenhe, 

wangye, yaogongxin, gaohan, tangjingyao, zhaolei, geji _}_ @cmhi.chinamobile.com 

> *Corresponding author: Baoping Cheng 

**_Abstract_ — Vision-Language-Action (VLA) models have demonstrated strong performance across diverse robotic manipulation tasks, yet their predominantly vision-centric perception and position-controlled execution remain insufficient for contact-rich manipulation. Visual observations alone often provide limited evidence of contact onset and interaction magnitude, while position-control policies cannot respond compliantly to rapidly changing contact dynamics. To bridge both the perception and control gaps, we propose TAO-Force, a force-conditioned VLA framework that combines force-aware policy learning with contact-regulated execution. For forceaware perception, TAO-Force introduces Force-conditioned Feature-wise Linear Modulation (F-FiLM) to inject encoded force feedback into the representations of a frozen pretrained visual-language backbone while preserving its semantic priors. For responsive control, it employs a contact-gated fast–slow architecture, with a slow position-control branch tracking nominal trajectories during non-contact phases and a fast admittance-control branch regulating physical interaction during contact phases. Detailed analyses on a force-perception task and real-world evaluations across four contact-rich manipulation tasks validate the effectiveness and robustness of TAO-Force.** 

## I. INTRODUCTION 


Fig. 1. **System overview and real-world evaluation.** Wrist-mounted six-axis force/torque sensors provide force feedback for policy perception. At execution time, a fast force-feedback loop updates joint commands in contact phases at a higher frequency than the slow position-control loop in non-contact phases. We evaluate TAO-Force on one force-perception task and four contact-rich manipulation tasks, achieving average success rates of 80.0% and 64.2% on the contact-rich tasks under in-domain (ID) and out-of-domain (OOD) conditions, respectively. 

Vision-Language-Action (VLA) models have emerged as a powerful paradigm for embodied manipulation, unifying perception, planning, and action generation within an endto-end architecture [1]–[5]. By leveraging the semantic priors and generalization capabilities from large-scale pretraining, VLA models have demonstrated strong performance across diverse open-world tasks in both simulation and real-world settings [6], [7]. However, their predominantly vision-centric design faces a fundamental limitation in contact-rich manipulation. In tasks such as peeling, pressing, and surface wiping, critical state transitions are governed by physical interaction rather than visual appearance. Contact onset, interaction magnitude, and the compliance required for success may correspond to only subtle visual changes. Consequently, policies that rely primarily on visual observations can be insensitive to the physical-interaction signals that determine task feasibility and execution robustness. Bridging this per- 

ception gap requires treating force sensing<sup>1</sup> as a first-class modality, allowing the policy to reason about interaction states that are difficult to infer from visual observations alone [8]–[11]. 

Recent studies have begun incorporating force feedback into VLA frameworks. Early approaches condition action generation on joint-torque signals or end-effector forces while retaining position commands as the policy output [8], [9]. However, when force is used only as an input and the predicted position commands are directly executed, the system may not respond sufficiently quickly to rapidly changing contact dynamics, limiting contact compliance and execution robustness. Subsequent methods therefore jointly 

> 1Throughout this paper, unless otherwise specified, the term _force_ denotes the six-dimensional end-effector wrench comprising three-dimensional force and three-dimensional torque. 

predict motion and force targets, which are tracked by higherfrequency low-level controllers during contact [12], [13]. Despite their promising performance, two key challenges remain. First, unlike vision, force sensing lacks a feature extractor pretrained at a comparable scale. During posttraining, pretrained visual representations can dominate optimization, causing the policy to underutilize force information that is essential for contact regulation. Second, existing joint motion–force prediction strategies generally provide control targets without explicitly estimating contact states or coordinating transitions between non-contact and contact phases, making it difficult to balance motion accuracy with contact compliance. 

To address these challenges, we propose TAO-Force, a force-conditioned adaptation framework that bridges the perception and control gaps in contact-rich VLA deployment. As illustrated in Fig. 1, TAO-Force retains a frozen pretrained VLA backbone and incorporates physical-interaction feedback into policy learning and execution through two complementary designs. First, we introduce **F** orce-conditioned **F** eature-w **i** se **L** inear **M** odulation (F-FiLM), which uses encoded force histories to modulate visual–language representations through learned affine transformations. This mechanism retains the semantic priors of the pretrained backbone while promoting the use of force information for trajectory and contact-force prediction. Second, inspired by FoAR [10], we develop a contact-gated fast–slow control architecture. The policy jointly predicts nominal action and desiredforce chunks, and separately estimates a contact probability. A slow position-control branch tracks the nominal motion trajectory, while a fast admittance-control branch regulates physical interaction at a higher frequency. Trajectory densification and smooth contact-gated fusion coordinate the two branches and reduce discontinuities during transitions between non-contact and contact phases. Together, these designs combine force-aware trajectory generation with responsive physical regulation for contact-rich manipulation. In summary, our main contributions are as follows: 

- We propose TAO-Force, a force-conditioned VLA adaptation framework that integrates physical-interaction feedback into policy learning and execution while preserving a frozen pretrained visual–language backbone. 

- We introduce F-FiLM to condition pretrained visual– language representations on force feedback, together with contact-causal force supervision that masks forcechunk targets at pre-contact anchors, preventing future contact forces from supervising pre-contact predictions. 

- We develop a contact-gated fast–slow control architecture that uses the predicted contact probability to switch between nominal position control during non-contact phases and high-frequency admittance control during contact, with reference processing and command fusion ensuring responsive regulation and smooth recovery to nominal motion. 

- Offline analyses and real-world evaluations on five manipulation tasks demonstrate effective force-aware 

adaptation and robust generalization. Across the four contact-rich execution tasks, TAO-Force achieves average success rates of 80.0% and 64.2% under in-domain (ID) and out-of-domain (OOD) conditions, respectively, outperforming the evaluated general-purpose VLA baselines on average. 

## II. RELATED WORK 

## _A. General-Purpose VLA Models_ 

Early robotic systems typically decoupled large language or vision–language models from low-level policies, limiting their generalization beyond predefined skills and demonstrations. End-to-end VLAs subsequently unified vision, language, and action: CLIPort [14] pioneered vision–languageconditioned manipulation, while Gato [15] and VIMA [16] modeled multimodal inputs and actions as token sequences using Transformers. RT-1 [1] scaled this paradigm to diverse real-world tasks, and RT-2 [2] established the use of Internetpretrained VLM backbones. RT-X [17] extended training across robot embodiments, while OpenVLA [3] provided an open-source VLM-based policy. More recently, Octo [18], RDT-1B [5], and _π_ 0 [4] adopted diffusion or flow matching for continuous action generation. Hierarchical systems such as RT-H [19], _π_ 0 _._ 5 [6], and GR00T N1 [7] further bridge high-level semantic reasoning and fine-grained motor execution through intermediate action representations and continuous controllers. 

## _B. Contact-Rich Manipulation Models_ 

Force and tactile sensing provide direct observations of physical interaction and have been increasingly incorporated into contact-rich manipulation models. At the perception and policy-learning level, early visuo-tactile methods fuse vision and touch through cross-modal attention or spatially aligned representations, as demonstrated by VTT and 3D-ViTac [20], [21]. Recent force-aware policies, including TA-VLA, ForceVLA, FoAR, and ManipForce, integrate joint torque or end-effector wrench with visual and proprioceptive features through token-based fusion, mixture-of-experts architectures, contact-aware gating, or frequency-aware encoding [8]–[11]. FD-VLA instead distills force-supervised representations from visual observations and robot states, removing the need for physical force sensing at inference time [22]. Tactile-language and tactile-VLA models further connect localized contact observations with semantic representations for contact-sensitive reasoning and action generation [23], [24]. A recurring difficulty in this line of work is that force and tactile signals are acquired at rates far higher than vision, so policies must learn from asynchronous, rate-mismatched streams [11]. 

At the execution level, force-aware perception alone may be insufficient when low-frequency position predictions are directly tracked without explicit force regulation. ForceMimic, ForceVLA2, and Tactile-VLA jointly predict pose and wrench or force targets for hybrid force–position control [12], [13], [24], while CompliantVLA-adaptor regulates interaction through variable impedance control [25]. 

Reactive Diffusion Policy, AT-VLA, and PhaForce instead decouple slow trajectory generation from a fast tactile- or force-conditioned stream that refines actions close to control rate [26]–[28]. Despite this progress, balancing physicalfeedback conditioning with the preservation of pretrained semantic representations, while translating low-rate policy predictions into stable high-rate contact regulation, remains an important design challenge. 

## III. PRELIMINARIES AND PROBLEM FORMULATION 

We present the admittance-control interface used for compliant execution and formulate force-aware adaptation of a pretrained VLA policy. 

## _A. Admittance Control_ 

Admittance control enables compliant interaction on position-controlled robots by mapping force-tracking errors to Cartesian motion corrections. Let **x** and **x** _d_ denote the actual and reference end-effector poses, respectively, and let **F**<sup>ext</sup> and **F**<sup>_d_</sup> denote the measured external force and desired force. The measured external force is compensated for the gravitational wrench of the end-effector tool and expressed in the controller frame. We adopt the standard second-order admittance model: 


where **M** , **D** , and **K** are the virtual mass, damping, and stiffness matrices, respectively. This model converts the force error into compliant end-effector motion for closed-loop contact regulation. 

## _B. Problem Formulation_ 

We consider adapting a pretrained VLA policy to contactrich manipulation, where successful execution requires both awareness of physical interaction and responsive contact regulation. A standard VLA policy maps a visual observation _ot_ , a language instruction _l_ , and a robot state **s** _t_ to an action chunk: 


## where _K_ denotes the prediction horizon. 

This formulation presents two limitations in contact-rich manipulation. The _perception gap_ refers to the absence of direct observations of robot–environment interaction in the input modalities of a standard VLA policy. The _control gap_ refers to the mismatch between low-frequency VLA action prediction and the fast contact dynamics that require realtime regulation. 

To bridge these gaps, we augment the pretrained VLA policy with external-force context _Ft_<sup>ext</sup> as an additional input: 


The outputs **a** _t_ : _t_ + _K_ , **F**<sup>_d_</sup> _t_ : _t_ + _K_<sup>,and</sup><sup>_p_</sup> _t_<sup>_c_denotethepredicted</sup> action chunk, desired-force chunk, and contact probability, respectively. The parameters _θ_ are inherited from the pretrained VLA policy, while _ϕ_ denotes the parameters introduced for force-aware adaptation. 

## IV. THE TAO-FORCE FRAMEWORK 

As shown in Fig. 2, TAO-Force consists of a forceconditioned policy that jointly predicts nominal actions and desired forces while separately estimating a contact probability, together with a contact-gated fast–slow controller for responsive execution. 

## _A. Pretrained VLA Architecture_ 

TAO-Force builds on GR00T N1.5 [29], whose Eagle visual–language backbone combines a SigLIP visual encoder with a Qwen-based language model to produce multimodal representations for a diffusion transformer (DiT) action head. We freeze the pretrained backbone to preserve its semantic and action-generation priors, and introduce lightweight force encoders, F-FiLM modulation, and additional prediction heads for force-aware adaptation. 

## _B. Force-conditioned Policy Learning_ 

To bridge the _perception gap_ , TAO-Force introduces three modifications to the pretrained VLA architecture. First, force feedback is integrated into the visual-language features as an explicit condition for DiT denoising. Second, a gating network predicts the contact probability from the forceconditioned features. Third, the DiT jointly predicts an action chunk and a desired-force chunk, providing motion and force references for the contact-gated fast–slow controller. 

_a) Force-conditioned modulation:_ TAO-Force first extracts a visual-language representation from the pretrained VLA backbone: 


Here, the visual-language encoder is inherited from the pretrained VLA backbone. During training, the backbone parameters are kept frozen, while all newly introduced force encoders, modulation networks, and prediction heads, collectively parameterized by _ϕ_ , are optimized. 


Here, each encoded feature forms a conditioning token. The current-force and state encoders, _gϕ_<sup>cur</sup> and _gϕ_<sup>state</sup> , are implemented as MLPs, while _gϕ_<sup>hist</sup> uses a lightweight 1DCNN to capture recent contact dynamics. 

To directly inject force feedback into the pretrained visuallanguage representation, we introduce F-FiLM, built upon FiLM [30]. Given the concatenated conditioning tokens **e** _t_ , the modulation network _h_<sup>film</sup> _ϕ_ predicts a residual scale vector and a shift vector: 


These vectors modulate the pretrained visual-language representation through a feature-wise affine transformation: 


Fig. 2. **Overview of TAO-Force.** TAO-Force preserves a frozen pretrained visual–language backbone and uses F-FiLM to condition its representations on force feedback, enabling the policy to jointly generate nominal action and desired-force chunks while separately estimating the current contact probability. During execution, the predicted contact probability gates between position-controlled motion in the non-contact phase and compliant force regulation in the contact phase. The contact-gated fast–slow controller coordinates low-frequency policy inference with high-frequency admittance control, enabling smooth transitions and responsive physical regulation for contact-rich manipulation. 

where _⊙_ denotes element-wise multiplication and the FiLM scale is **_γ_** _t_ = **1** + ∆ **_γ_** _t_ . By zero-initializing the final layer of the modulation network, we obtain ∆ **_γ_** _t_ = **0** and **_β_** _t_ = **0** at initialization. Thus, F-FiLM initially preserves the pretrained representation and progressively learns to incorporate physical interaction feedback. 

_b) Prediction heads:_ The force-conditioned representation supports two policy outputs: parallel prediction of action and desired-force chunks, and instantaneous contact prediction. For chunk generation, we employ a shared DiT decoder with separate noised action and force tokens, preserving modality-specific generation paths while enabling bidirectional interaction between the two token sequences through shared self-attention. 

Let **x**<sup>a</sup> _t_ : _t_ + _K_<sup>(</sup><sup>_τ_)and</sup><sup>**x**f</sup> _t_ : _t_ + _K_<sup>(</sup><sup>_τ_)denotethenoisedaction</sup> and force chunks at flow time _τ_ , respectively. Conditioned on the force-modulated visual-language representation and the current robot state, the shared DiT decoder produces temporally aligned features for the two branches: 

**u**<sup>a</sup> _t_ : _t_ + _K_<sup>_,_</sup><sup>**u**f</sup> _t_ : _t_ + _K_<sup>=</sup><sup>_d_dit</sup> _ϕ_ � **x**<sup>a</sup> _t_ : _t_ + _K_<sup>(</sup><sup>_τ_)</sup><sup>_,_</sup><sup>**x**f</sup> _t_ : _t_ + _K_<sup>(</sup><sup>_τ_)</sup> �� **z** ˜ _t_ vl<sup>_,_</sup><sup>**s**</sup><sup>_t, τ_</sup> � _._ 

Two lightweight output heads predict the corresponding velocity fields: 


At inference time, the nominal action chunk **a** ˆ _t_ : _t_ + _K_ and desired-force chunk **F**<sup>ˆ</sup><sup>_d_</sup> _t_ : _t_ + _K_<sup>arerecoveredbyintegratingthe</sup> learned velocity fields from initial noise over _τ ∈_ [0 _,_ 1]. Contact prediction is instead formulated as an instantaneous gating problem. A lightweight classification head 

directly predicts the contact probability from the forceconditioned representation: 


This allows the contact head to respond directly to the current force-conditioned perceptual state, while the DiT decoder focuses on temporally coherent action and desiredforce generation. 

The resulting nominal action chunk **a** ˆ _t_ : _t_ + _K_ , desired-force chunk **F**<sup>ˆ</sup><sup>_d_</sup> _t_ : _t_ + _K_<sup>,andcontactprobability</sup><sup>_p_ˆ</sup> _t_<sup>_c_constitutethe</sup> complete policy-level output of TAO-Force. 

## _C. Training Objective_ 

We train TAO-Force on supervised demonstrations using a composite objective that combines action and force flow matching with contact classification. To ground force prediction in physical interaction and discourage reliance on non-force shortcuts, we further introduce contact-causal force supervision and force-attentive modality dropout. 

_a) Contact-causal force supervision:_ The force supervision is derived from the six-dimensional force/torque readings recorded during demonstrations, which capture the interaction force at the robot end effector. A straightforward approach would be to directly use future segments of these measurements as force-chunk targets. However, a nonzero desired-force command is physically meaningful only after contact has been established. If a future force segment containing contact forces is used as the target while the robot is still out of contact, the model may learn to anticipate force from visual cues or demonstration-specific temporal patterns rather than grounding its prediction in current contact evidence. During deployment, even slight variations in contact 

onset can invalidate these learned correlations, causing the policy to predict nonzero forces before contact or to delay the required force prediction after contact occurs. 

To address this issue, we gate force supervision by the current contact state. Let _ct ∈{_ 0 _,_ 1 _}_ denote whether the robot is in a task-relevant contact interval at time _t_ , and let **F**<sup>_⋆_</sup> _t_ : _t_ + _K_<sup>betherawforcechunkfromthedemonstration.The</sup> contact-causal force target is defined as 


The force loss is evaluated over all frames, using zero targets to suppress force prediction before contact and the recorded force chunks to supervise the desired force profile during contact. 

_b) Force-attentive training:_ A practical challenge in force-conditioned learning is that the policy may exploit visual and proprioceptive shortcuts instead of using force feedback. This is especially undesirable in contact-rich manipulation, where visually similar observations can correspond to different physical interaction states. To mitigate this issue, we apply force-attentive modality dropout during training. Specifically, we annotate force-critical temporal segments in the demonstrations and partially mask visual and proprioceptive features within these segments. This weakens the model’s reliance on non-force modalities and encourages it to use force-conditioned cues for downstream prediction. _c) Overall objective:_ The overall objective jointly optimizes action flow matching, force flow matching, and contact prediction. The action flow-matching loss preserves the nominal action-generation capability of the pretrained VLA policy by matching the predicted velocity field to the target velocity field induced by the ground-truth action chunk: 


Similarly, the force flow-matching loss matches the predicted force velocity field to the target velocity field induced by the contact-causal force target: 


Given the predicted contact probability, the contact classification loss is defined using binary cross-entropy: 


The complete objective is 


where _λ_ force and _λ_ contact balance force prediction and contact prediction relative to action generation, respectively. 

## _D. Contact-Gated Fast–Slow Control_ 

To bridge the _control gap_ between chunk-level policy predictions and high-frequency robot commands, TAO-Force employs the contact-gated fast–slow controller summarized in Algorithm 1. The predicted contact probability is thresholded to select between nominal position control in free space and high-frequency admittance control during contact. 

**Algorithm 1** Contact-Gated Fast–Slow Control 

**Require:** Predicted action chunk **a** ˆ _t_ : _t_ + _K_ , force chunk **F** ˆ<sup>_d_</sup> _t_ : _t_ + _K_<sup>,contactprobability</sup><sup>_p_ˆ</sup> _t_<sup>_c_,andthreshold</sup><sup>_η_</sup> **Ensure:** Joint-position commands **q**<sup>cmd</sup> 1: **Q**<sup>ref</sup> _←_ ACTIONPROCESSOR(ˆ **a** _t_ : _t_ + _K_ ) 2: **F**<sup>ref</sup> _←_ FORCEPROCESSOR( **F**<sup>ˆ</sup><sup>_d_</sup> _t_ : _t_ + _K_<sup>)</sup> 3: _g ←_ I[ˆ _p_<sup>_c_</sup> _t_<sup>_≥η_]</sup> 4: **for** each aligned reference ( **q**<sup>pos</sup> _,_ **F**<sup>_d_</sup> ) **do** 5: **if** _g_ = 1 **then** _▷_ High-freq. force control 6: Read **q** and **F**<sup>ext</sup> 7: **x** ˙<sup>adm</sup> _←_ ADMITTANCE( **q**<sup>pos</sup> _,_ **F**<sup>_d_</sup> _,_ **F**<sup>ext</sup> _,_ **q** ) 8: **q** ˙<sup>adm</sup> _←_ IK( ˙ **x**<sup>adm</sup> _,_ **q** ) 9: **q**<sup>cmd</sup> _←_ **q**<sup>cmd</sup><sup>_,−_</sup> + ∆ _t_ **q** ˙<sup>adm</sup> 10: _bf ←_ false 11: **else** _▷_ Low-freq. Position control 12: **if** _g_<sup>_−_</sup> = 1 **then** 13: ∆ **q** _←_ **q**<sup>cmd</sup><sup>_,−_</sup> _−_ **q**<sup>pos</sup> 14: _s ←_ 0, _bf ←_ true 15: **end if** 16: **if** _bf_ = true **then** 17: _w_ ( _s_ ) _←_ 1 _−_ 10 _s_<sup>3</sup> + 15 _s_<sup>4</sup> _−_ 6 _s_<sup>5</sup> 18: **q**<sup>cmd</sup> _←_ **q**<sup>pos</sup> + _w_ ( _s_ )∆ **q** 19: Update _s_ toward 1 20: **else** 21: **q**<sup>cmd</sup> _←_ **q**<sup>pos</sup> 22: **end if** 23: **end if** 24: Send **q**<sup>cmd</sup> to the robot 25: **q**<sup>cmd</sup><sup>_,−_</sup> _←_ **q**<sup>cmd</sup> , _g_<sup>_−_</sup> _← g_ 26: **end for** 

_a) Reference processing:_ Following VLA-RAIL [31], the action processor first densifies each predicted action chunk using polynomial fitting and then applies a minimumjerk transition between successive chunks. This produces a smooth joint-reference sequence **Q**<sup>ref</sup> . At each chunk boundary, the force processor maps the action target index to the force timeline and smooths the beginning of the new force chunk against the currently executed force reference. The blending weight progressively shifts from the current reference to the new prediction, reducing discontinuities and producing **F**<sup>ref</sup> . 

_b) Contact-gated control:_ During contact, the admittance controller uses the nominal joint reference as a weak positional anchor while regulating the measured external force toward the desired force. A small stiffness limits accumulated positional drift without dominating force regulation. The resulting Cartesian velocity is mapped to joint space and integrated at the high-frequency control rate, as detailed in Algorithm 1. 

When contact ends, the force-controlled command may deviate from the nominal trajectory. Directly switching back to position control could therefore cause an abrupt motion. TAO-Force gradually removes this command residual using a quintic smoothstep weight, smoothly reconnecting the robot to the nominal trajectory. If contact recurs during this 


Fig. 3. **Effectiveness of Force Perception.** _Left:_ The Blind Box Sorting setup, highlighting the decision anchor at which the trajectories diverge based on weight. _Right:_ The generated action chunks (Joint 2) at the anchor under real and counterfactual force conditions, with the yellow shaded area indicating the final 16 frames of each chunk used for evaluation. 

transition, trajectory fusion is canceled and force control immediately resumes. 

## V. EXPERIMENTS 

The experimental evaluation is designed to comprehensively assess TAO-Force’s ability to bridge the _perception gap_ and _control gap_ in contact-rich manipulation. Through both offline analyses and real-world robot deployments, we aim to answer the following core research questions: 

- **Q1:** Does force feedback meaningfully influence trajectory generation? 

- **Q2:** Does TAO-Force outperform VLA baselines in task success and robustness under both ID and OOD conditions? 

- **Q3:** How does each key design contribute to task success? 

## _A. Experimental Setups_ 

_a) Hardware Platform:_ All real-world experiments are conducted on the AgiBot G1 dual-arm humanoid robot [32]. Visual observations are captured by three built-in RGB cameras (one head-mounted and two wrist-mounted), while force feedback is acquired directly from the six-axis force/torque sensors at the wrists. 

The system is deployed with a hierarchical fast–slow control architecture. The VLA policy runs at 5 Hz on a single NVIDIA RTX 5070 Laptop GPU with 8 GB VRAM, with observations buffered at 30 Hz. The predicted 30 Hz action and force chunks are processed into 267 Hz position and force references, respectively, while the admittance controller then incorporates real-time force and joint-position measurements to generate compliant commands at 1000 Hz. 

_b) Experimental Tasks:_ We evaluate force perception, contact-rich execution, and OOD robustness on five realworld manipulation tasks, with 30 trials per task in each of the ID and OOD settings. 

In **Blind Box Sorting** , the robot sorts visually identical canned porridge by weight, and succeeds if each can is placed in the correct bin. In **Peeling Cucumber** , the robot peels along the cucumber surface, with success defined as removing a continuous peel longer than half the cucumber’s 


Fig. 4. **Contact-Force Prediction Accuracy.** _Left:_ Illustration of the contact phase. _Right:_ Predicted and ground-truth force trajectories, with yellow regions indicating contact-dominant intervals inferred from the predicted contact probability. _Fy_ and _Fz_ are shown as they exhibit the largest variations. 

length. In **Pressing Pump Head** , the robot presses a soappump head, and succeeds if liquid is dispensed without excessive force. In **Wiping Whiteboard Marks** , the robot uses an eraser to wipe target marks, with success determined by their visible removal. In **Cutting Cucumber** , the robot uses a knife to cut a cucumber, and succeeds if it cuts completely through the cucumber. 

_c) Baselines:_ We compare TAO-Force against two state-of-the-art VLA baselines, GR00T N1.7 and _π_ 0 _._ 5. We exclude Blind Box Sorting from the baseline evaluation because distinguishing visually identical objects by weight inherently requires force perception, making baselines without force input inapplicable to this task. 

TABLE I 

RESULTS OF COUNTERFACTUAL FORCE INJECTION. 

|**Episode**|**Method**|**Force Input**|**Trajectory E**|**rror**<br>**Flip Rate**|
|---|---|---|---|---|
||F-FiLM (Ours)|Empty<br>Full|0.0001<br>0.0186|–<br>0.0185_↑_<br>**90%**|
|Empty|DePost|Empty<br>Full|0.0005<br>0.0056|–<br>20%|
||FVLMoE|Empty<br>Full|0.0005<br>0.0005|–<br>0%|
||F-FiLM (Ours)|Full<br>Empty|0.0001<br>0.0302|–<br>0.0301_↑_<br>**100%**|
|Full|DePost|Full<br>Empty|0.0002<br>0.0326|–<br>90%|
||FVLMoE|Full<br>Empty|0.0001<br>0.0036|–<br>10%|


_Note:_ DePost and FVLMoE are adapted from TA-VLA [33] and ForceVLA [9], respectively. 

## _B. Analysis of Force-Aware Trajectory Generation_ 

To answer **Q1** , we focus on Blind Box Sorting, which provides a particularly suitable testbed for assessing the effect of force perception. We therefore conduct an offline counterfactual analysis on this task to examine whether TAOForce genuinely conditions its trajectory generation on force feedback rather than on visual cues alone. 

**Evaluation Protocol.** We use 20 test trajectories, equally split between empty and full cans, and define the decision anchor as the timestep at which their routing paths begin to diverge (Fig. 3). At this anchor, we fix the visual observation 

TABLE II 

REAL-WORLD EVALUATION SUCCESS RATES. 

||**Blind **|**Box Sorting**|**Peeli**|**ng Cucumber**|**Pressi**|**ng Pump Head**|**Wiping W**|**hiteboard Marks**|**Cutting**|**Cucumber**|**Aver**|**age**<sup>_†_</sup>|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Model**|**ID**|**OOD**|**ID**|**OOD**|**ID**|**OOD**|**ID**|**OOD**|**ID**|**OOD**|**ID**|**OOD**|
|||Flickering Light||Table Height -3 cm|B|ottle Height +2.5 cm||Different Eraser||Different Knife|||
|GR00T N1.7|N/A|N/A|76.7%|26.7%|63.3%|23.3%|53.3%|30.0%|60.0%|0.0%|63.3%|20.0%|
|_π_0_._5|N/A|N/A|53.3%|53.3%|63.3%|16.7%|**66.7%**|36.7%|63.3%|10.0%|61.7%|29.2%|
|TAO-Force (Ours)|**100.0%**|**100.0%**|**96.7%**|**86.7%**|**80.0%**|**70.0%**|60.0%|**53.3%**|**83.3%**|**46.7%**|**80.0%**|**64.2%**|


> _†_ Average success rates are computed over the four tasks excluding Blind Box Sorting. 

and provide either the factual force profile or a counterfactual one obtained by swapping the force signatures of empty and full cans. We evaluate the final 16 frames of the generated Joint 2 action chunk, where the routing difference is most pronounced. Trajectory Error is the MSE relative to the original ground-truth trajectory, and Flip Rate is the percentage of trajectories redirected according to the injected force. We compare F-FiLM against two existing force-feature fusion methods: DePost, proposed in TA-VLA [33], and FVLMoE, proposed in ForceVLA [9]. 

**Results and Analysis.** As shown in Fig. 3, F-FiLM closely reproduces the ground-truth trajectory under factual force input, while counterfactual force injection redirects the generated trajectory toward the routing direction associated with the injected force. Table I further shows that F-FiLM responds consistently in both swapping directions, whereas DePost exhibits an asymmetric response and FVLMoE shows limited sensitivity to the injected force. Overall, F-FiLM provides the most consistent force-aware trajectory adaptation among the evaluated fusion methods. 

## _C. Analysis of Contact-Force Prediction_ 

To further assess TAO-Force’s ability to model contact dynamics, we conduct an offline force-prediction analysis on the cucumber-peeling test trajectories. 

**Evaluation Protocol.** We identify contact-dominant intervals by thresholding the predicted contact probability at 0.8 and uniformly sample temporal anchors within these intervals. At each anchor, we evaluate the right-wrist force prediction at the first frame of the predicted chunk. We report MSE separately for the translational force components ( _Fx, Fy, Fz_ ) and rotational torque components ( _Tx, Ty, Tz_ ). 

**Results and Analysis.** As illustrated in Fig.4, the predicted force and torque signals closely follow the rapid variations in the ground-truth signals during peeling contact. As shown in Table III, F-FiLM substantially improves prediction accuracy across both force and torque components. 

TABLE III 

CONTACT-PHASE FORCE AND TORQUE PREDICTION ERRORS. 

|**Method**|**Force MSE**|**Torque MSE**|
|---|---|---|
|w/o F-FiLM|35.097|0.653|
|w/ F-FiLM|4.098<br>30.|999_↓_0.070<br>0.583_↓_|


## _D. Real-World Task Performance_ 

Table II summarizes the real-world success rates under the ID and OOD settings defined in the experimental setup, with 

## 30 trials per setting. 

For **Blind Box Sorting** , TAO-Force achieves a 100.0% success rate under both ID and OOD conditions. As discussed in Section V-A, baselines without force input are inapplicable to this task and are therefore marked as N/A. 

For **Peeling Cucumber** and **Pressing Pump Head** , the OOD perturbations both change the height of the manipulated object and thus alter the contact geometry. In Peeling Cucumber, failures mainly occur when the peeler misses the cucumber surface or removes only a short peel. In Pressing Pump Head, failures are primarily caused by excessive pressing force after the bottle height is increased. TAO-Force achieves the highest OOD success rates on both tasks. 

For **Wiping Whiteboard Marks** and **Cutting Cucumber** , the OOD perturbations replace the tool used during evaluation. Tool changes alter the tool geometry, thereby shifting the contact timing and changing the resulting contact-force characteristics during interaction. This mismatch can cause insufficient wiping pressure, unstable contact, or ineffective cutting, leading to a clear success-rate drop under OOD conditions. 

Overall, TAO-Force achieves the strongest OOD performance and exhibits a smaller ID-to-OOD performance drop than GR00T N1.7 and _π_ 0 _._ 5 across the evaluated tasks. These results demonstrate improved robustness to variations in contact geometry, tool properties, and environmental conditions. Together, the ID and OOD evaluations answer **Q2** affirmatively: TAO-Force consistently outperforms the VLA baselines in task success and generalizes more robustly to contact-related perturbations. 

## _E. Ablation Study_ 

To answer **Q3** , we evaluate F-FiLM modulation and force control on two representative contact-rich tasks: Peeling Cucumber and Pressing Pump Head. GR00T N1.5 + F-FiLM incorporates force-conditioned feature modulation into the VLA backbone without force-controlled execution, whereas GR00T N1.5 + Force Control applies the proposed forcecontrol branch without F-FiLM-based trajectory generation. TAO-Force integrates both components to combine forceconditioned trajectory generation with compliant execution. 

As shown in Table IV, F-FiLM and force control provide complementary benefits. F-FiLM enables measured force feedback to modulate multimodal representations during trajectory generation. 

Force control instead improves execution-time adaptability through closed-loop regulation. Compared with directly 

TABLE IV 

ABLATION STUDY OF REAL-WORLD SUCCESS RATES. 

|**Method**|**Peeling C**|**ucumber**|**Pressing **|**Pump Head**|
|---|---|---|---|---|
||**ID**|**OOD**|**ID**|**OOD**|
|GR00T N1.5|56.7%|3.3%|66.7%|26.7%|
|GR00T N1.5 + F-FiLM|70.0%|23.3%|66.7%|63.3%|
|GR00T N1.5 + Force Control|63.3%|60.0%|43.3%|33.3%|
|TAO-Force (Ours)|**96.7%**|**86.7%**|**80.0%**|**70.0%**|


tracking predicted actions, regulating the desired contact force is more tolerant to variations in contact timing and local interaction conditions. However, neither component alone performs consistently well across both tasks and evaluation settings. 

By integrating F-FiLM with force control, TAO-Force achieves the highest success rate in every evaluated setting. These results answer **Q3** : force-conditioned multimodal fusion improves upstream trajectory generation, while compliant force control enhances downstream execution robustness, and their combination is necessary for the strongest overall performance. 

## VI. DISCUSSION AND CONCLUSION 

This work presents TAO-Force, a force-conditioned VLA framework for contact-rich manipulation. TAO-Force introduces F-FiLM to incorporate measured force feedback into multimodal representations, enabling force-aware trajectory generation. It further employs a fast–slow control architecture: the slow system generates action and desired-force trajectories from multimodal observations, while the fast system performs closed-loop force regulation during execution. Together, these components bridge force-aware perception and responsive control for robust contact-rich manipulation. Realworld experiments demonstrate that TAO-Force consistently outperforms the VLA baselines, while the ablation study validates the complementary contributions of F-FiLM and force control to robust contact-rich manipulation. 

## REFERENCES 

- [1] A. Brohan, N. Brown, B. Cheeseman, _et al._ , “Rt-1: Robotics transformer for real-world control at scale,” in _Conference on Robot Learning_ , PMLR, 2022. 

- [2] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid, _et al._ , “Rt-2: Vision-language-action models transfer web knowledge to robotic control,” in _Conference on Robot Learning_ , pp. 2165–2183, PMLR, 2023. 

- [3] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi, _et al._ , “Openvla: An open-source vision-language-action model,” _arXiv preprint arXiv:2406.09246_ , 2024. 

- [4] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter, _et al._ , “ _pi_ ~~0~~ : A visionlanguage-action flow model for general robot control,” _arXiv preprint arXiv:2410.24164_ , 2024. 

- [5] S. Liu, L. Wu, B. Li, H. Tan, H. Chen, Z. Wang, K. Xu, H. Su, and J. Zhu, “Rdt-1b: a diffusion foundation model for bimanual manipulation,” _arXiv preprint arXiv:2410.07864_ , 2024. 

- [6] P. Intelligence, K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, _et al._ , “ _π_ 0. 5: A vision-language-action model with open-world generalization. arxiv 2025,” _arXiv preprint arXiv:2504.16054_ , 2025. 

- [7] J. Bjorck, F. Casta˜neda, N. Cherniadev, X. Da, R. Ding, L. Fan, Y. Fang, D. Fox, F. Hu, S. Huang, _et al._ , “Gr00t n1: An open foundation model for generalist humanoid robots,” _arXiv preprint arXiv:2503.14734_ , 2025. 

- [8] Z. Zhang, H. Xu, Z. Yang, C. Yue, Z. Lin, H.-a. Gao, Z. Wang, and H. Zhao, “Elucidating the design space of torque-aware visionlanguage-action models,” _arXiv preprint arXiv:2509.07962_ , 2025. 

- [9] J. Yu, H. Liu, Q. Yu, J. Ren, C. Hao, H. Ding, G. Huang, G. Huang, Y. Song, P. Cai, _et al._ , “Forcevla: Enhancing vla models with a force-aware moe for contact-rich manipulation,” _Advances in Neural Information Processing Systems_ , vol. 38, pp. 93409–93439, 2026. 

- [10] Z. He, H. Fang, J. Chen, H. S. Fang, and C. Lu, “Foar: Force-aware reactive policy for contact-rich robotic manipulation,” _IEEE Robotics and Automation Letters_ , 2024. 

- [11] G. Lee, Y. Lee, K. Kim, S. Lee, S. Noh, S. Back, and K. Lee, “Manipforce: Force-guided policy learning with frequency-aware representation for contact-rich manipulation,” in _2026 IEEE International Conference on Robotics and Automation (ICRA)_ , 2026. Accepted for publication. 

- [12] Y. Li, Z. Zhaxizhuoma, H. Jiang, J. Xia, H. Zhang, J. Du, Y. Zhou, J. Zeng, C. Hao, J. Ren, _et al._ , “Forcevla2: Unleashing hybrid forceposition control with force awareness for contact-rich manipulation,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 8911–8920, 2026. 

- [13] W. Liu, J. Wang, Y. Wang, W. Wang, and C. Lu, “Forcemimic: Force-centric imitation learning with force-motion capture system for contact-rich manipulation,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , 2025. 

- [14] M. Shridhar, L. Manuelli, and D. Fox, “Cliport: What and where pathways for robotic manipulation,” in _Proceedings of the 5th Conference on Robot Learning (CoRL)_ , 2021. 

- [15] S. Reed, K. Zolna, E. Parisotto, S. G. Colmenarejo, A. Novikov, _et al._ , “A generalist agent,” _Transactions on Machine Learning Research_ , 2022. Featured Certification, Outstanding Certification. 

- [16] Y. Jiang, A. Gupta, Z. Zhang, G. Wang, Y. Dou, Y. Chen, L. FeiFei, A. Anandkumar, Y. Zhu, and L. Fan, “Vima: General robot manipulation with multimodal prompts,” in _Fortieth International Conference on Machine Learning_ , 2023. 

- [17] Open X-Embodiment Collaboration _et al._ , “Open X-Embodiment: Robotic learning datasets and RT-X models.” https://arxiv. org/abs/2310.08864, 2023. 

- [18] Octo Model Team, D. Ghosh, H. Walke, K. Pertsch, K. Black, _et al._ , “Octo: An open-source generalist robot policy,” in _Proceedings of Robotics: Science and Systems_ , (Delft, Netherlands), 2024. 

- [19] S. Belkhale, T. Ding, T. Xiao, P. Sermanet, Q. Vuong, J. Tompson, Y. Chebotar, D. Dwibedi, and D. Sadigh, “Rt-h: Action hierarchies using language,” in _https://arxiv.org/abs/2403.01823_ , 2024. 

- [20] Y. Chen, M. V. d. Merwe, A. Sipos, and N. Fazeli, “Visuo-tactile transformers for manipulation,” in _Proceedings of The 6th Conference on Robot Learning_ (K. Liu, D. Kulic, and J. Ichnowski, eds.), vol. 205 of _Proceedings of Machine Learning Research_ , pp. 2026– 2040, PMLR, 14–18 Dec 2023. 

- [21] B. Huang, Y. Wang, X. Yang, Y. Luo, and Y. Li, “3d-vitac: Learning fine-grained manipulation with visuo-tactile sensing,” in _8th Annual Conference on Robot Learning_ . 

- [22] R. Zhao, W. Wang, Y. Ma, X. Li, F. Tay, J. Ang, and H. Zhu, “Fd-vla: Force-distilled vision-language-action model for contact-rich manipulation,” 02 2026. 

- [23] P. Hao, C. Zhang, D. Li, X. Cao, X. Hao, S. Cui, and S. Wang, “Tla: tactile-language-action model for contact-rich manipulation,” _Robot Learning_ , vol. 3, no. 1, 2026. 

- [24] J. Huang, S. Wang, F. Lin, Y. Hu, C. Wen, and Y. Gao, “Tactilevla: Unlocking vision-language-action model’s physical knowledge for tactile generalization,” _arXiv preprint arXiv:2507.09160_ , 2025. 

- [25] H. Zhang, W.-H. Huang, Q. Tong, G. Solak, P. Liu, K. Zhang, S. Liu, J. Peters, Y. She, and A. Ajoudani, “Compliantvla-adaptor: Vlmguided variable impedance action for safe contact-rich manipulation,” 2026. 

- [26] H. Xue, J. Ren, W. Chen, G. Zhang, Y. Fang, G. Gu, H. Xu, and C. Lu, “Reactive diffusion policy: Slow-fast visual-tactile policy learning for contact-rich manipulation,” in _Proceedings of Robotics: Science and Systems (RSS)_ , 2025. 

- [27] X. Li, M. Cai, J. Xu, J. Zhu, H. Fan, Y. Shen, G. Ren, and H. Dong, “At-vla: Adaptive tactile injection for enhanced feedback reaction in vision-language-action models,” 2026. 

- [28] M. Wang, Z. Yue, R. Lu, Y. Li, Z. Wang, G. Pan, K. Dong, J. Cheng, Y. Cheng, and H. Liu, “Phaforce: Phase-scheduled visual-force policy learning with slow planning and fast correction for contact-rich manipulation,” 2026. 

- [29] NVIDIA GEAR, “GR00T N1.5: An improved open foundation model for generalist humanoid robots.” https://research.nvidia. com/labs/gear/gr00t-n1_5/, June 2025. NVIDIA Research, accessed: 2026-09-10. 

- [30] E. Perez, F. Strub, H. de Vries, V. Dumoulin, and A. C. Courville, “Film: Visual reasoning with a general conditioning layer,” in _AAAI_ , 2018. 

- [31] Y. Zhao, L. Zhao, B. Cheng, G. Yao, X. Wen, and H. Gao, “Vla-rail: A real-time asynchronous inference linker for vla models and robots,” 2025. 

- [32] Zhiyuan Robotics (AgiBot), “Agibot g1 general purpose robot.” https://www.agibot.com/products/G1. Accessed: 202512-29. 

- [33] Z. Zhang, H. Xu, Z. Yang, C. Yue, Z. Lin, H.-a. Gao, Z. Wang, and H. Zhao, “Ta-vla: Elucidating the design space of torque-aware visionlanguage-action models,” _arXiv preprint arXiv:2509.07962_ , 2025. 

