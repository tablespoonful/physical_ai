---
title: "ForceVLA2: Unleashing Hybrid Force-Position Control with Force Awareness for Contact-Rich Manipulation"
date: "2026-03-16"
authors: "Yang Li;  Zhaxizhuoma; Hongru Jiang; Junjie Xia; Hongquan Zhang; Jinda Du"
venue: "CVPR 2026"
url: https://arxiv.org/abs/2603.15169
pdf: https://arxiv.org/pdf/2603.15169
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.15169)** / [論文ページ](https://arxiv.org/abs/2603.15169)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **ForceVLA2: Unleashing Hybrid Force-Position Control with Force Awareness for Contact-Rich Manipulation** 

Yang Li<sup>1</sup><sup>_,_2</sup><sup>_,_9</sup><sup>_∗_</sup> , Zhaxizhuoma<sup>3</sup><sup>_,_2</sup><sup>_,_9</sup><sup>_∗_</sup> , Hongru Jiang<sup>3</sup><sup>_∗_</sup> , Junjie Xia<sup>2</sup><sup>_,_9</sup><sup>_∗_</sup> Hongquan Zhang<sup>6</sup><sup>_,_4</sup><sup>_,_2</sup> , Jinda Du<sup>3</sup> , Yunsong Zhou<sup>2</sup> , Jia Zeng<sup>2</sup> , Ce Hao<sup>7</sup><sup>_,_8</sup> , Jieji Ren<sup>3</sup> Qiaojun Yu<sup>2</sup><sup>_,_3</sup><sup>_†_</sup> , Cewu Lu<sup>3</sup><sup>_,_4</sup><sup>_,_5</sup> , Yu Qiao<sup>2</sup><sup>_,_1</sup><sup>_†_</sup> , Jiangmiao Pang<sup>2</sup> 

> _∗_ Equal contribution, _†_ Corresponding authors (yuqiaojun@pjlab.org.cn, qiaoyu@pjlab.org.cn) 

1Tongji University, 2Shanghai AI Laboratory, 3Shanghai Jiao Tong University, 4Shanghai Innovation Institute, 5Noematrix Intelligence 

6East China Normal University, 7Zhongguancun Academy, 8National University of Singapore, 9Lumos Robotics 


Figure 1. **ForceVLA2 concept.** Contact-rich manipulation requires force regulation, beyond visual and state observations (left). **ForceVLA2** integrates force information across multiple scales, enabling rich modeling of contact dynamics. It builds force awareness into task planning through incoming force signals, and it outputs hybrid force–position actions with dynamic balance (right). 

## **Abstract** 

_Embodied intelligence for contact-rich manipulation has predominantly relied on position control, while explicit awareness and regulation of interaction forces remain under-explored, limiting stability, precision, and robustness in real-world tasks. We propose ForceVLA2, an end-to-end vision–language–action framework that equips robots with hybrid force-position control and explicit force awareness. ForceVLA2 introduces force-based prompts into the VLM expert to construct force-aware task concepts across stages, and employs a Cross-Scale Mixture-of-Experts (MoE) in the action expert to adaptively fuse these concepts with real-time interaction forces for closed-loop hybrid force– position regulation. To support learning and evaluation, we construct ForceVLA2-Dataset, containing 1,000 trajectories over 5 contact-rich tasks, including wiping, pressing, and assembling, with multi-view images, task prompts, proprioceptive state, and force signals. Extensive experiments show that ForceVLA2 substantially improves success rates and reliability in contact-rich manipulation, outperforming_ 

**_π_** 0 _and_ **_π_** 0 _._ 5 _by 48.0% and 35.0%, respectively, across the 5 tasks, and mitigating common failure modes such as arm overload and unstable contact,thereby actively advancing force-aware interactive physical intelligence in VLAs. The project page is available at this URL._ 

## **1. Introduction** 

Artificial intelligence has advanced rapidly with large vision–language models (VLMs) [1, 6, 35, 42, 44, 46] that exhibit remarkable perceptual and reasoning capabilities. However, these models remain confined to virtual domains, lacking the embodiment necessary for authentic physical understanding and interaction in real-world settings. To overcome this limitation, vision–language–action models (VLAs) [2, 3, 22, 47, 50] extend VLMs toward physical intelligence by seamlessly connecting perception and reasoning to embodied interaction. This integration unifies cognition and manipulation into a cohesive framework, enabling robots not only to perceive and understand, but also to manipulate objects in the physical world in ways that closely mirror human intelligence. Consequently, VLAs have be- 

8911 

come a foundation for robotic learning, paving the way for enhanced sample efficiency, generalizability, compositionality, and incremental learning [21], and enabling adaptive, context-aware behavior in dynamic, complex environments. 

While recent VLAs such as OpenVLA [22], OpenVLAOFT [23], GR00T-N1 [2], and **_π_** 0 [3] have advanced embodied cognition by linking perception and language to action, these models demonstrate strong performance in semantic grounding and language following, showing that pretrained multimodal models can acquire priors and be efficiently fine-tuned with only a few demonstrations. However, current VLAs still lack the ability to reason about physical dynamics and fine-grained contact interactions, which are essential for real-world, contact-rich manipulation. Building upon **_π_** 0 [3], ForceVLA [43] extends this framework by incorporating the force modality, leading to improved success rates in contact-rich manipulation tasks. 

Yet, existing VLAs reduce force to an auxiliary perceptual input rather than leveraging it for active, adaptive closed-loop force interaction, a core requirement for genuine physical intelligence. In contrast, humans rely on high-level visual and linguistic reasoning to identify stagespecific targets and estimate coarse spatial relations, while integrating real-time force sensing as direct physical perception to adaptively refine both force and position during interaction. Current VLAs, however, still lack mechanisms to reason about the spatiotemporal relationships required across different task stages and to integrate force perception with active force–position interaction within subtasks. This gap motivates a unified treatment of _force awareness_ and _closed-loop force–position control_ within the VLA paradigm for contact-rich manipulation. 

To overcome these limitations, we propose **ForceVLA2** , a novel framework that equips VLAs with active hybrid force-position control with force awareness to enhance contact-rich manipulation, as shown in Fig. 1. By incorporating force modality into the VLA architecture, ForceVLA2 links language-level and visual semantic reasoning with physical contact-level interaction, enabling physically grounded, generalizable, and highly adaptive behaviors, especially in tasks requiring fast and stable force-following. Inspired by the human motor control system, where force perception and regulation are hierarchically integrated [16], ForceVLA2 employs a dual-level design. A long-horizon reasoning module driven by a force prompt is embedded into the VLM expert to construct force-aware task concepts, while a short-horizon reactive manipulation skill employs a Cross-Scale Mixtureof-Experts (MoE) to integrate force-aware task knowledge from the VLM expert with embodied interaction forces in the action expert, enabling adaptive regulation of hybrid force–position interaction. Extensive experiments demonstrate that ForceVLA2 consistently improves performance 

and generalization in contact-rich manipulation. Our contributions are summarized as follows: 

- We introduce ForceVLA2, the first end-to-end hybrid force–position control framework with force awareness for VLAs, enhancing contact-rich manipulation by integrating force-prompt-driven VLM reasoning and fusing force into action experts via a Cross-scale MoE, enabling coordinated hybrid force–position interaction and tightly linking VLM reasoning with action generation to improve physical interaction. 

- We construct ForceVLA2-Dataset, a dataset of 1,000 trajectories across 5 contact-rich tasks, including wiping, pressing, and assembling, with fundamental modalities such as multi-view images, task prompts, and proprioceptive states. It is further enhanced by adding force prompts and incorporating force into the action space, bridging the gap between embodied hybrid force–position interaction and force-aware task concepts, providing an empirical foundation for advancing research from force perception to interaction. 

- We conducted extensive experiments demonstrating the effectiveness of ForceVLA2, compared to **_π_** 0 and **_π_** 0 _._ 5, the success rates increased by 48.0% and 35.0%, respectively, across the 5 tasks, represents notable progress toward bridging force-aware task concept with embodied adaptive hybrid force–position manipulation skills. 

## **2. Related Work** 

**Vision-language-action models.** Recent research on VLAs [4, 5, 10, 20, 22, 23, 26, 33, 48] leverages large-scale multimodal pretraining to generalize robotic policies across diverse tasks and embodiments, mapping visual observations and language instructions to low-level actions through end-to-end learning. Autoregressive models [22, 23, 29] treat control as next-token prediction over discretized action tokens, enabling VLM-style training with efficient decoding. Diffusion-based approaches [7, 12, 27, 34, 51] model continuous action distributions for more diverse and controllable behaviors, though at high computational cost. Flow-based methods such as _π_ 0 [3] accelerate action generation via flow-matching decoders, while ForceVLA [43] extends it with force inputs to improve contact-rich manipulation accuracy. Dual-system designs like _π_ 0 _._ 5 and GR00TN1 [2] separate high-level reasoning from low-level action generation, combining generalization with action. **Physical modality integration in robot policies.** Traditional VLA models struggle with dynamic, contact-rich interactions that demand fine-grained feedback, motivating recent efforts to integrate force and tactile modalities for improved control. Recent works incorporating force sensing [15, 17, 28, 40, 43] enhance motion stability and contact precision, yet force is typically used only as a perceptual cue rather than an active control signal. Tactile-based methods such as TLA [13], Tac-Man [49], and other multimodal fu- 

8912 

sion approaches [18, 24, 52] improve robustness under occlusion but cannot substitute for direct force sensing, since tactile-to-force estimation remains indirect and noisy. Despite these advances, existing methods remain limited to force perception and purely position-based interaction. **Multimodal embodied datasets.** Large-scale embodied datasets have significantly advanced robot learning, yet they rarely include standardized force modality, which is essential for modeling contact [31, 36, 38]. Open-XEmbodiment [8] aggregates over one million trajectories across 22 robots, though only a subset of its datasets include force modalities, leading to sparse and inconsistent coverage. Recent datasets have begun to incorporate explicit force modality for contact-rich manipulation. RH20T [11] provides multi-modal data, including RGB-D, audio, proprioceptive state, and calibrated force collected via haptic teleoperation, while REASSEMBLE [32] focuses on assembly tasks with synchronized visual, proprioceptive, and force modalities, incorporating sub-tasks to enable detailed analysis of manipulation skills. 

## **3. ForceVLA2 Framework** 

ForceVLA2 is designed to unify force awareness and hybrid force–position control within a vision–language–action (VLA) framework, thereby enabling precise, adaptive, and stable contact-rich manipulation. Inspired by findings in human sensorimotor control, we posit that force acts as a unifying signal across the perception–planning–execution hierarchy, providing essential feedback for dynamic and compliant interaction [16, 37]. Neuroscientific evidence further supports this perspective, showing that humans perceive external forces through proprioceptive sensing and regulate them via internal forward models implemented in the cerebellum and motor cortex [16]. Motivated by biological sensing–acting mechanisms, ForceVLA2 internalizes multi-scale force cues within both context-dependent long-horizon reasoning, realized through a force prompt, and adaptive, stage-aware reactive skills, enabling precise force–position interaction for unified, force-aware manipulation that bridges perception and action. 

Building upon these principles, we propose the ForceVLA2 architecture, which integrates multi-scale perception, contextual reasoning, and force-aware manipulation into a unified VLA framework. As shown in Fig. 2, multi-view images, task prompts, and force prompts are jointly encoded within a VLM, providing high-level guidance for task operation sequencing and spatial–semantic reasoning in task decomposition (Sec. 3.1). In parallel, force observation bypasses high-level fusion and modulates the action expert via a direct gradient pathway, enabling a reactive response to observed force during contact (Sec. 3.2.1). Force and proprioceptive tokens are routed through a Cross-Scale Mixture-of-Experts (MoE) [30], which dynamically integrates visual, language, 

and force information to determine the dominant modality at each phase of the task (Sec. 3.2.2). ForceVLA2 unifies force–position control and task progress prediction into a cohesive, force-aware closed-loop architecture, enabling physically grounded reasoning and adaptive perception–action coordination for contact-rich manipulation. 

### **3.1. Long-Horizon Force Awareness via Prompting** 

Current VLA models rely on pre-trained priors for task decomposition; however, purely vision–language inputs are insufficient in contact-rich settings that require human-like task awareness and physically grounded reasoning about task concepts, particularly interaction forces [9]. In such contact-rich scenarios, visual cues are often ambiguous or insufficient, whereas essential information is conveyed through force feedback, as in aerospace connector insertion or gear assembly. To address this, we introduce force prompts as textual cues that indicate the current subtask and encode stage-specific physical context, thereby constructing force-aware task concepts. This mechanism enables ForceVLA2 to inherit VLM knowledge, assess subtask completion, transition across stages, and explicitly update force cues to guide force-aware manipulation. 

**Vision, task, and force prompt integration.** Inspired by the _π_ 0 framework [3], the ForceVLA2 architecture integrates vision, task prompts, and force prompts before a conditional flow-matching action expert. Visual observations from multiple RGB cameras, along with task instructions, are encoded by a SigLIP-based [45] vision–language model (based on PaliGemma [1]) into contextual embeddings. The text prompt provides a global description of the task, while the force prompt encodes the current subtask state. Each task has a predefined list of subtasks, and the force prompt determines whether to maintain the current subtask or transition to the next, functioning like a discrete-state machine. 

Specifically, the visual tokens **E** _v ∈_ R<sup>_Nv×D_model</sup> are first processed through a visual encoder _f_ ( _·_ ): **Z** _v_ = _f_ ( **E** _v_ ) _∈_ R<sup>_Nv×D_model</sup> . The linguistic tokens, obtained by concatenating the text prompt **T** _t ∈_ R<sup>_Nt×D_model</sup> and the force prompt **T** _f ∈_ R<sup>_Nf ×D_model</sup> , are processed through a text encoder _g_ ( _·_ ): **Z** _l_ = _g_ ([ **T** _t_ ; **T** _f_ ]) _∈_ R<sup>(</sup><sup>_Nt_+</sup><sup>_Nf_)</sup><sup>_×D_model</sup> , where _Nt_ and _Nf_ are the number of text and force prompt tokens. The outputs of the visual and text encoders are concatenated to form the input to the vision–language model: **E** in = [ **Z** _v_ ; **Z** _l_ ] _∈_ R<sup>(</sup><sup>_Nv_+</sup><sup>_Nt_+</sup><sup>_Nf_)</sup><sup>_×D_model</sup> . Finally, **E** in undergoes token-to-token attentions within the vision–language model (VLM( _·_ )), producing the fused contextual tokens: 


The resulting sequence **E** serves as the fused multi-modal representation, which is subsequently used for downstream short-term force perception and control. 

8913 


Figure 2. **Framework of ForceVLA2.** ForceVLA2 takes multi-view images, task and force prompts, and proprioceptive states (EE pose and force) as input. Force is injected at multiple scales: as sub-task prompts fused with images in the vision-language model, and as force tokens combined with EE pose in the multimodal encoder, with a bypass to preserve raw signals. The cross-scale MoE integrates these modalities to produce hybrid force–position actions and track sub-task progress for adaptive, contact-rich manipulation. 

### **3.2. Short-Horizon Force-to-Control Loop** 

Existing VLA models rely on end-effector (EE) 6D pose control, which suffices for coarse tasks but fails when subtle force interactions dominate. ForceVLA2 encodes proprioceptive state and force differently within the action expert, passing them through the multi-modal encoder to fuse with visual–language embeddings for long-horizon reasoning, while transient force signals bypass the fusion layer and feed directly to the MoE, forming a short-term reactive loop. This design preserves gradient fidelity for rapid force feedback, avoids over-reliance on past trajectories, and enables active exploration (Appendix A). The MoE dynamically integrates long- and short-term cues to produce joint predictions of EE 6D pose, force, and subtask progress for hybrid force-position control in contact-rich manipulation. 

#### **3.2.1. multi-modal Encoding for EE 6D pose and Force** 

**Proprioceptive-force encoding.** The proprioceptive state, represented by the EE 6D pose, is expressed as **p** _∈_ R<sup>7</sup> and encoded through another linear layer _ϕP_ : 


To enable force-aware perception, the raw 6D force–torque readings **f** raw _∈_ R<sup>6</sup> are first projected into the model embedding space via a linear mapping _ϕF_ : 


The encoded EE 6D pose and force tokens are concatenated to form a multi-modal state representation, **E** state = [ **E** _P_ ; **E** _F_ ], which is then fed into the MoE alongside visual–language contextual tokens **E** _∈_ R<sup>_N_VL</sup><sup>_×D_model</sup> _._ Meanwhile, a force embedding **E** _F_ bypasses the cross-modal interaction and is sent directly to the MoE, forming a shortterm, reactive pathway. 

**Cross-modal interaction.** To incorporate high-level task context into proprioceptive sensing, the state embeddings interact with the vision–language features through crossattention. Specifically, the encoded visual–language sequence **E** _∈_ R<sup>_N_VL</sup><sup>_×D_model</sup> serves as the contextual key–value pair, while the state tokens act as queries: 


This operation injects global task semantics into the local proprioceptive streams, allowing the model to interpret force and motion signals under the guidance of visual–language intent. The conditioned embeddings are then concatenated as: 


which forms the multi-modal input for the following expert routing stage. 

#### **3.2.2. Adaptive Routing and Decoding** 

**Cross-scale Mixture-of-Experts.** The conditioned sequence **E** cond is processed by a sparse MoE layer designed to adaptively select the most informative modality for the current manipulation phase. The MoE contains three modality-specific experts (visual, state, and force), each implemented as a lightweight MLP [14]. A dynamic gating network computes token-wise routing weights **w** = [ _wV , wS, wF_ ], and activates the most relevant expert for each token: 


Through this mechanism, the network autonomously emphasizes visual reasoning during free-space motion and force or position cues when contact and compliance become critical. The fused representation **E** MoE is then projected to 

8914 

the latent space of the flow-matching policy [25] for downstream action generation. 

**Flow Matching policy for position-force control.** The flow-matching policy head generates force-aware actions by progressively denoising a noise-initialized action conditioned on the fused multi-modal context. At the beginning of each time step _t_ , a noisy action sample **a**<sup>(0)</sup> _t ∼N_ (0 _, I_ ) is iteratively refined according to the learned conditional flow: 


where _τ_ is the denoising time, **E** MoE provides the contextual multi-modal embedding from the MoE module. In practice, this continuous flow is implemented as a discrete denoising process: 


starting from random noise and gradually converging to the final force–position command: 


Here, ∆ **p** _t_ represents the desired change in endeffector pose, **f** _t_ denotes the predicted contact force. By conditioning the denoising process on the fused visual–language–force representation, the model achieves closed-loop, context-aware control that adapts fluidly to contact-rich interaction. 

**Probabilistic modeling of force-control transition.** Note that the transition indicator _st_ is modeled as a continuous floating-point value output by the model, ranging from 0 to 1. Once _st_ exceeds 1 (threshold), the controller transitions to the next subtask and resets the value to 0. The ground truth value for _st_ during training, denoted as ˆ _st_ , is computed based on the observed quantities. Let _A_ denote the current end-effector position and _At_ the target position, _E_ be the current end-effector orientation, _Et_ the target orientation, theand observed<sup>_−−→_</sup> _AAt_ represent the displacement fromstatistics: Θ = <u>12</u> _~~→~~ →−E ·_<sup>_−→_</sup> _<u>Et</u> A_ to _At∈_ . Define(0 _,_ 1), � _∥_<sup>_~~−~~_</sup> _E ∥∥_<sup>_~~−→~~_</sup> _Et∥_<sup>+ 1</sup> � _L_ = _∥_<sup>_−−→_</sup> _AAt∥∈_ (0 _, ∞_ ), _F_ = _∥_ **f** _∥∈_ [ _n, m_ ]. Here, Θ measures orientational alignment (1 = aligned, 0 = opposite), _L_ is the remaining distance to the goal, and _F_ represents the instantaneous contact force (bounded within the normalization limits _n_ and _m_ ). 

We define the ground truth for the subtask transition probability as the joint event that these quantities satisfy their respective progress conditions. Given observed values ( _θ, l, f_ ) and assuming Θ _∼_ Beta( _α,_ 1), _L ∼_ Exponential( _λ_ ), _F ∼_ Uniform( _n, m_ ), we calculate 

the subtask transition probability ˆ _st_ as follows: 


Here, Γ( _·_ ) represents the Gamma function, with _α_ = 2 and _λ_ = 2. _st_ serves as an indicator of subtask completion. When it exceeds a threshold, the controller transitions to the next subtask and resets _st_ to 0. 

## **4. ForceVLA2-Dataset** 

To train the proposed ForceVLA2 model, we collected a new dataset specifically tailored for contact-rich manipulation tasks, with a particular emphasis on capturing forcecontrol signals for sub-task segmentation and annotation (Fig. 3 (a)). Unlike previous work, which primarily relied on EE 6D pose trajectories [8, 11] and VR-based human teleoperation [41], our setup employs the forcefeedback GELLO teleoperation framework [39] to capture high-quality demonstrations with natural motion dynamics, while explicitly recording force and motion trajectories. Each manipulation task is segmented into 3–5 annotated subtasks, guided by visual inspection and analysis of the synchronized force signals. The collected dataset constitutes a multi-modal corpus encompassing visual, proprioceptive, task-prompt, force-prompt, and force modalities. **Hardware and sensor setup.** Demonstrations were collected using a 7-DOF Flexiv Rizon 4s robotic arm equipped with a DH Robotics AG-95 adaptive gripper. Visual observations were acquired from three RGB cameras: two static third-person views (Intel RealSense D455, 1280×720 @ 30 fps) and one wrist-mounted egocentric view (Intel RealSense D435, 640×480 @ 30 fps), as shown in Fig. 4. A 6D force/torque sensor attached to the end-effector recorded interaction forces at 300 Hz, while the robot joint states and end-effector (EE) 6D poses were logged synchronously. All visual streams were resized to 480×640 resolution, normalized, and timestamp-synchronized prior to storage. **Collected tasks.** We curated 5 contact-rich manipulation tasks: _press bottle_ , _clean vase_ , _clean board_ , _retrieve plate_ , and _assemble gears_ (Fig. 3 (b)). Operators used the force-feedback GELLO teleoperation interface to control the robot in real time, ensuring accurate and repeatable interaction patterns while preserving natural force application. To enhance diversity, object poses are varied across demonstrations. Each task is recorded until completion, and subtask boundaries are annotated offline based on distinct transitions in the force signal profiles. 

**Dataset statistics.** The resulting dataset comprises 1000 trajectories and approximately 500K synchronized timesteps. Each trajectory contains time-aligned streams of 

8915 


Figure 3. **The illustration of ForceVLA2-Dataset.** (a) ForceVLA2-Dataset is the first dataset with force prompts for task decomposition and the only one providing force-control supervision. (b) It features 1,000 demonstrations across five contact-rich tasks. 


Figure 4. **The dataset collection system.** A Flexiv arm is driven by manually controlled GELLO [39] to accomplish dexterous tasks and record images, force, as well as the pose of the robot. 

RGB images, end-effector (EE) 6D poses, and force signals. The ForceVLA2-Dataset facilitates research on forceaware and subtask-structured manipulation policy learning by introducing force prompts and integrating force into the action space, bridging the gap for embodied hybrid force–position interaction and providing an empirical foundation for advancing research from force perception to interaction. The detailed dataset statistics and descriptive information can be found in the Appendix B. 

## **5. Experiments** 

In this section, we evaluate the effectiveness of ForceVLA2 on diverse contact-rich manipulation tasks that test perceptual and reasoning abilities, as well as adaptive, closedloop hybrid force–position interactions across multiple task stages under complex physical conditions. The experiments address the following research questions: 

- **Q1:** How does ForceVLA2 perform in real-world contact-rich manipulation tasks, and what specific advantages and technical benefits does hybrid force–position 

control offer over pure position control? 

- **Q2:** Which components contribute most significantly to the performance improvements of ForceVLA2? 

- **Q3:** Which modality fusion strategy yields the best performance in active hybrid force–position controlling? 

### **5.1. Experiment Setting** 

**Tasks and evaluation metrics.** Our experimental benchmark consists of 5 contact-rich manipulation tasks within the proposed ForceVLA2-Dataset: Press the bottle, Clean the vase, Clean the board, Retrieve the plate, and Assemble gears. The primary evaluation metric is the success rate (%), determined by conducting 20 independent trials for each task. 

**Baselines.** To demonstrate the superiority of our proposed ForceVLA2, we compare it against five established methods: ACP [17], _π_ 0 [3], _π_ 0 _._ 5 [19], ForceVLA [43] and _π_ 0 with naive force input. ACP leverages principles of admittance control to implicitly incorporate the desired force into the final output by predicting a virtual action. The _π_ 0 model leverages a flow matching architecture integrated with a pre-trained VLM to leverage Internet-scale knowledge. Building upon _π_ 0, the _π_ 0 _._ 5 model incorporates cotraining on diverse tasks to enhance generalization. Meanwhile, ForceVLA prioritizes external force sensing as a core modality within its VLA architecture. 

### **5.2. Main Experiment Results** 

**Overall performance on contact-rich tasks (Q1).** As summarized in Tab. 1, ForceVLA2 significantly outperforms all baselines, achieving a 66% average success rate across all tasks. On force-sensitive tasks, it surpasses the second-best model by up to 50%. Compared with models without force inputs, ForceVLA2 and ForceVLA, which incorporate force feedback, show remarkable improvements 

8916 


Figure 6. **Additional tests on following and re-targeting.** ForceVLA2 exhibits robust position and orientation following, and in object search tasks, it can still perform successful re-grasps even when visual observations fail. 

on force-sensitive tasks such as object search, demonstrating superior force perception. _π_ 0 w/ F reaches 17%, which is similar to the base version, and prior analyzes (TA-VLA, ForceVLA) also suggest that simple concatenation can act as nuisance input and degrade pre-trained VLA representations, instead of providing consistent control-relevant signals. The ACP achieves a success rate of only 16.0%, primarily due to its limited generalization capabilities. 

**Force-intensive tasks and overload avoidance.** As illustrated in Fig. 5, for force-intensive tasks such as clean board and bottle pressing, excessive contact force can easily push the robot into overload. Among the compared methods, ForceVLA2 actively adjusts its interaction forces and successfully completes these tasks, whereas other VLAs lack sufficient reactive adjustment capabilities. 

**Dynamic force-tracking under sudden perturbations.** 

8917 

Table 1. **Success rates (** % **) comparison of different methods.** _π_ 0 w/ F: _π_ 0 with native force input. Each value represents the success rate over 20 trials. Avg.: the mean performance across all five contact-rich tasks. <mark>cyan :</mark> main metric. **bold** : best results. 

|Type|Method|Press<br>bottle|<sup>Clean vase </sup>|<sup>Clean</sup><br>board|Retri.<br>plate|Assem.<br>gears|Avg.|
|---|---|---|---|---|---|---|---|
|/ F|<sup>_π_0</sup>|35.0|20.0|35.0|0.0|0.0|18.0|
|wo orce|<br>_π_0_._5|45.0|30.0|45.0|15.0|20.0|31.0|
||ACP|25.0|30.0|25.0|0.0|0.0|16.0|
||_π_0 w/ F|30.0|25.0|20.0|10.0|0.0|17.0|
|w/ Force|ForceVLA|70.0|25.0|55.0|15.0|10.0|35.0|
||**ForceVLA2**|**80.0**|**75.0**|**70.0**|**35.0**|**70.0**<sup>_↑_50</sup>|**66.0**|


Table 2. **Ablation Study of Different Modules in the ForceVLA2 Model.** FP: Force Prompt. ME: Multimodal Encoder. CM: Cross-Scale MoE module. Entries indicate success rate (%) <mark>.</mark> <u><mark>gray</mark></u> <mark>:</mark> baseline results. 

|FP|ME|CM|<sup>Press</sup><br>bottle|Clean<br>vase|Clean<br>board|Retri.<br>plate|Assem.<br>gears|Avg.|
|---|---|---|---|---|---|---|---|---|
||||35.0|20.0|35.0|0.0|0.0|18.0|
|✓|||60.0|25.0|40.0|5.0|5.0|27.0<sup>_↑_9</sup>|
|✓|✓||60.0|40.0|65.0|5.0|30.0|40.0<sup>_↑_13</sup>|
|✓|✓|✓|**80.0**|**75.0**|**70.0**|**35.0**|**70.0**|**66.0**<sup>_↑_26</sup>|


Table 3. **Ablation of input modality combinations in the CrossScale MoE module.** VM: Visual Modality. FM: Force Modality. Entries indicate <u>success rate (%).</u> 

|VM|FM|Press<br>bottle|Clean<br>vase|Clean<br>board|Retri.<br>plate|Assem.<br>gears|Avg.|
|---|---|---|---|---|---|---|---|
|||70.0|30.0|60.0|0.0|20.0|36.0|
|✓||**85.0**|40.0|**85.0**|0.0|40.0|50.0<sup>_↑_14</sup>|
|✓|✓|80.0|**75.0**|70.0|**35.0**|**70.0**|**66.0**<sup>_↑_16</sup>|


In addition to outperforming baselines on standard benchmarks, ForceVLA2 exhibits exceptional force-tracking performance across a variety of dynamic tests. As depicted in Fig. 6, during the bottle pressing task, when the robot arm is about to press the bottle, we abruptly lower the base. Thanks to its force-aware interaction, ForceVLA2 reacts quickly to the new contact configuration and completes the pressing. In contrast, other VLAs slowly chase the new EE 6D pose, leading to failure to maintain stable contact. **Robust wiping and re-targeting in object search.** In the vase wiping task, when the vase is rotated such that its surface normal becomes misaligned with the arm’s original motion direction, ForceVLA2 drives the arm to slide along the vase and move upward, maintaining contact and successfully completing the wiping motion. Other VLAs continue along their original trajectory, which often results in arm overload and task failure. In the Retrieve Plate task, ForceVLA2 explores the sandbox through forceguided probing; even after an initial failed grasp, it autonomously retries, showcasing robust adaptation. 

### **5.3. Ablation Study** 

**Ablation setup.** In this section, we progressively intro- 

duce the additional modules built on top of _π_ 0, including the force prompts, the Cross-Scale MoE module, and the Multimodal Encoder, and compare their impact across multiple tasks. In particular, we conduct an ablation on the CrossScale MoE module by varying its modality inputs and outputs to verify the effectiveness of our design. Additional experiments focusing on the Multimodal Encoder are provided in the Appendix C. 

**Component-wise ablations on FP, CM, and ME (Q2).** As shown in Tab. 2, we conduct a stepwise ablation in which we progressively add the Force Prompt (FP), Cross-Scale MoE (CM), and Multimodal Encoder (ME) modules on top of _π_ 0, and measure the success rate over five tasks. The results show a consistent increase in success rate as more modules are introduced, confirming the effectiveness of our overall architectural design. We can see that the Cross-Scale MoE module provides the most significant gain in success rate among all added components. 

**Modality fusion in the Cross-Scale MoE module (Q3).** We further perform an ablation study on the Cross-Scale MoE module to validate our design choices. By selectively enabling or disabling force modality (FM) and visual modality (VM), we examine whether the proposed crossscale fusion scheme is indeed necessary and beneficial. As reported in Tab. 3, VM and FM inputs contribute roughly equally within the Cross-Scale MoE module, indicating that both visual–language context and force signals are essential for achieving strong performance. Interestingly, for the Press Bottle and Clean Board tasks, introducing an extra force token on the input side slightly degrades performance. We hypothesize that this effect arises because the force requirements in these tasks are relatively simple, requiring only a single switch between position and force control, so additional force tokens introduce unnecessary degrees of freedom that can perturb an otherwise stable policy, leading to a minor drop in success rate. 

## **6. Conclusion** 

We present ForceVLA2, a force-aware vision-languageaction framework with hybrid force–position control for contact-rich manipulation, and evaluate it on our ForceVLA2-Dataset of five real-world tasks. Across these tasks, ForceVLA2 achieves a success rate of 66%, outperforming ACP, _π_ 0, _π_ 0 _._ 5, and ForceVLA, and surpassing the second-best method by 50 percentage points on the most force-sensitive assembling gears task. The model also consistently reduces failures caused by arm overload and unstable contact, and ablation studies show monotonically improved performance as force prompts, the CrossScale MoE, and multimodal fusion are added, with the full ForceVLA2 variant achieving the best results. Overall, ForceVLA2 coupling force–position control achieves more reliable and adaptable contact-rich manipulation than existing state-of-the-art VLA baselines. 

8918 

## **References** 

- [1] Lucas Beyer, Andreas Steiner, Andr´e Susano Pinto et al. Paligemma: A versatile 3b vlm for transfer. _arXiv preprint arXiv:2407.07726_ , 2024. 1, 3 

- [2] Johan Bjorck, Fernando Casta˜neda, Nikita Cherniadev et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 1, 2 

- [3] Kevin Black, Noah Brown, Danny Driess et al. _π_ 0: A vision-language-action flow model for general robot control. corr, abs/2410.24164, 2024. doi: 10.48550. _arXiv preprint ARXIV.2410.24164_ . 1, 2, 3, 6 

- [4] Anthony Brohan, Noah Brown, Justice Carbajal et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 2 

- [5] Anthony Brohan, Noah Brown, Justice Carbajal et al. Rt2: Vision-language-action models transfer web knowledge to robotic control. _arXiv preprint arXiv:2307.15818_ , 2023. 2 

- [6] Zhe Chen, Jiannan Wu, Wenhai Wang et al. Internvl: Scaling up vision foundation models and aligning for generic visuallinguistic tasks. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 24185– 24198, 2024. 1 

- [7] Cheng Chi, Zhenjia Xu, Siyuan Feng et al. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , page 02783649241273668, 2023. 2 

- [8] Open X-Embodiment Collaboration, Abby O’Neill, Abdul Rehman et al. Open X-Embodiment: Robotic learning datasets and RT-X models. https://arxiv.org/abs/ 2310.08864, 2023. 3, 5 

- [9] Muhayy Ud Din, Waseem Akram, Lyes Saad Saoud et al. Vision language action models in robotic manipulation: A systematic review. _arXiv preprint arXiv:2507.10672_ , 2025. 3 

- [10] Cunxin Fan, Xiaosong Jia, Yihang Sun et al. Interleave-vla: Enhancing robot manipulation with interleaved image-text instructions. _arXiv preprint arXiv:2505.02152_ , 2025. 2 

- [11] Hao-Shu Fang, Hongjie Fang, Zhenyu Tang et al. Rh20t: A comprehensive robotic dataset for learning diverse skills in one-shot. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 653–660. IEEE, 2024. 3, 5 

- [12] Yanjiang Guo, Yucheng Hu, Jianke Zhang et al. Prediction with action: Visual policy learning via joint denoising process. In _The Thirty-eighth Annual Conference on Neural Information Processing Systems_ , 2024. 2 

- [13] Peng Hao, Chaofan Zhang, Dingzhe Li et al. Tla: Tactilelanguage-action model for contact-rich manipulation. _arXiv preprint arXiv:2503.08548_ , 2025. 2 

- [14] Simon Haykin. _Neural networks: a comprehensive foundation_ . Prentice Hall PTR, 1994. 4 

- [15] Zihao He, Hongjie Fang, Jingjing Chen et al. Force-aware reactive policy for contact-rich robotic manipulation. _arXiv preprint arXiv:2411.15753_ , 2024. 2 

- [16] Neville Hogan and Stephen P Buerger. Impedance and interaction control. In _Robotics and automation handbook_ , pages 375–398. CRC press, 2018. 2, 3 

- [17] Yifan Hou, Zeyi Liu, Cheng Chi et al. Adaptive compliance policy: Learning approximate compliance for diffusion guided control. _arXiv preprint arXiv:2410.09309_ , 2024. 2, 6 

- [18] Jialei Huang, Shuo Wang, Fanqi Lin et al. Tactile-vla: Unlocking vision-language-action model’s physical knowledge for tactile generalization. _arXiv preprint arXiv:2507.09160_ , 2025. 3 

- [19] Physical Intelligence, Kevin Black, Noah Brown et al. _π_ 0 _._ 5: a vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 6 

- [20] Yunfan Jiang, Agrim Gupta, Zichen Zhang et al. Vima: General robot manipulation with multimodal prompts. _arXiv preprint arXiv:2210.03094_ , 2(3):6, 2022. 2 

- [21] Leslie Pack Kaelbling. The foundation of efficient robot learning. _Science_ , 369(6506):915–916, 2020. 2 

- [22] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 1, 2 

- [23] Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 2 

- [24] Yiyang Ling, Karan Owalekar, Oluwatobiloba Adesanya et al. Impact: Intelligent motion planning with acceptable contact trajectories via vision-language models. _arXiv preprint arXiv:2503.10110_ , 2025. 3 

- [25] Yaron Lipman, Ricky TQ Chen, Heli Ben-Hamu et al. Flow matching for generative modeling. _arXiv preprint arXiv:2210.02747_ , 2022. 5 

- [26] Jiaming Liu, Mengzhen Liu, Zhenyu Wang et al. Robomamba: Multimodal state space model for efficient robot reasoning and manipulation. _arXiv preprint arXiv:2406.04339_ , 2024. 2 

- [27] Jiaming Liu, Hao Chen, Pengju An et al. Hybridvla: Collaborative diffusion and autoregression in a unified visionlanguage-action model. _arXiv preprint arXiv:2503.10631_ , 2025. 2 

- [28] Wenhai Liu, Junbo Wang, Yiming Wang et al. Forcemimic: Force-centric imitation learning with force-motion capture system for contact-rich manipulation. _arXiv preprint arXiv:2410.07554_ , 2024. 2 

- [29] Karl Pertsch, Kyle Stachowicz, Brian Ichter et al. Fast: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 2 

- [30] Noam Shazeer, Azalia Mirhoseini, Krzysztof Maziarz et al. Outrageously large neural networks: The sparsely-gated mixture-of-experts layer. _arXiv preprint arXiv:1701.06538_ , 2017. 3 

- [31] Modi Shi, Yuxiang Lu, Huijie Wang et al. Introducing agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems. https:// opendrivelab.com/AgiBot-World/, 2025. Blog post. 3 

- [32] Daniel Sliwowski, Shail Jadav, Sergej Stanovcic et al. Reassemble: A multimodal dataset for contact-rich robotic assembly and disassembly, 2025. 3 

8919 

- [33] starVLA Community. Starvla: A lego-like codebase for vision-language-action model developing, 2025. 2 

- [34] Octo Model Team, Dibya Ghosh, Homer Walke et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 2 

- [35] Qwen Team et al. Qwen2 technical report. _arXiv preprint arXiv:2407.10671_ , 2(3), 2024. 1 

- [36] Homer Walke, Kevin Black, Abraham Lee et al. Bridgedata v2: A dataset for robot learning at scale, 2024. 3 

   - [51] Zhongyi Zhou, Yichen Zhu, Minjie Zhu et al. Chatvla: Unified multimodal understanding and robot control with visionlanguage-action model. _arXiv preprint arXiv:2502.14420_ , 2025. 2 

   - [52] Huaijiang Zhu, Tong Zhao, Xinpei Ni et al. Should we learn contact-rich manipulation policies from samplingbased planners? _IEEE Robotics and Automation Letters_ , 2025. 3 

- [37] Daniel M Wolpert, Zoubin Ghahramani, and Michael I Jordan. An internal model for sensorimotor integration. _Science_ , 269(5232):1880–1882, 1995. 3 

- [38] Kun Wu, Chengkai Hou, Jiaming Liu et al. Robomind: Benchmark on multi-embodiment intelligence normative data for robot manipulation. In _Robotics: Science and Systems (RSS) 2025_ . Robotics: Science and Systems Foundation, 2025. 3 

- [39] Philipp Wu, Yide Shentu, Zhongke Yi et al. Gello: A general, low-cost, and intuitive teleoperation framework for robot manipulators, 2023. 5, 6 

- [40] Yansong Wu, Zongxie Chen, Fan Wu et al. Tacdiffusion: Force-domain diffusion policy for precise tactile manipulation. _arXiv preprint arXiv:2409.11047_ , 2024. 2 

- [41] Han Xue, Jieji Ren, Wendi Chen et al. Reactive diffusion policy: Slow-fast visual-tactile policy learning for contactrich manipulation. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2025. 5 

- [42] An Yang, Anfeng Li, Baosong Yang et al. Qwen3 technical report. _arXiv preprint arXiv:2505.09388_ , 2025. 1 

- [43] Jiawen Yu, Hairuo Liu, Qiaojun Yu et al. Forcevla: Enhancing vla models with a force-aware moe for contact-rich manipulation. _arXiv preprint arXiv:2505.22159_ , 2025. 2, 6 

- [44] Yifu Yuan, Haiqin Cui, Yaoting Huang et al. Embodied-r1: Reinforced embodied reasoning for general robotic manipulation. _arXiv preprint arXiv:2508.13998_ , 2025. 1 

- [45] Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov et al. Sigmoid loss for language image pre-training. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 11975–11986, 2023. 3 

- [46] Jingyi Zhang, Jiaxing Huang, Sheng Jin et al. Visionlanguage models for vision tasks: A survey. _IEEE transactions on pattern analysis and machine intelligence_ , 46(8): 5625–5644, 2024. 1 

- [47] Qingqing Zhao, Yao Lu, Moo Jin Kim et al. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 1702–1713, 2025. 1 

- [48] Wei Zhao, Pengxiang Ding, Min Zhang et al. Vlas: Vision-language-action model with speech instructions for customized robot manipulation. _arXiv preprint arXiv:2502.13508_ , 2025. 2 

- [49] Zihang Zhao, Yuyang Li, Wanlin Li et al. Tac-man: Tactile-informed prior-free manipulation of articulated objects. _IEEE Transactions on Robotics_ , 2024. 2 

- [50] Ruijie Zheng, Yongyuan Liang, Shuaiyi Huang et al. Tracevla: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies, 2025. 1 

8920 

