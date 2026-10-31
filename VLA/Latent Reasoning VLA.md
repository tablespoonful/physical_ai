---
title: "Latent Reasoning VLA: Latent Thinking and Prediction for Vision-Language-Action Models"
date: "2026-02-01"
authors: "Shuanghao Bai; Jing Lyu; Wanqi Zhou; Zhe Li; Dakai Wang; Lei Xing"
venue: "ICML 2026"
url: https://arxiv.org/abs/2602.01166
pdf: https://arxiv.org/pdf/2602.01166
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.01166)** / [論文ページ](https://arxiv.org/abs/2602.01166)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Latent Reasoning VLA: Latent Thinking and Prediction for Vision-Language-Action Models** 

**Shuanghao Bai**<sup>* 1 2</sup> **Jing Lyu**<sup>* 2 3 4</sup> **Wanqi Zhou**<sup>1</sup> **Zhe Li**<sup>2</sup> **Dakai Wang**<sup>1</sup> **Lei Xing**<sup>1</sup> **Xiaoguang Zhao**<sup>3</sup> **Pengwei Wang**<sup>2</sup> **Zhongyuan Wang**<sup>2</sup> **Cheng Chi**<sup>2</sup> **Badong Chen**<sup>1</sup> **Shanghang Zhang**<sup>2 5</sup> 

� Project Page � Code 

## **Abstract** 

Vision-Language-Action (VLA) models benefit from chain-of-thought (CoT) reasoning, but existing approaches incur high inference overhead and rely on discrete reasoning representations that mismatch continuous perception and control. We propose Latent Reasoning VLA ( **LaRA-VLA** ), a unified VLA framework that internalizes multimodal CoT reasoning into continuous latent representations for embodied action. LaRA-VLA performs unified reasoning and prediction in latent space, eliminating explicit CoT generation at inference time and enabling efficient, actionoriented control. To realize latent embodied reasoning, we introduce a curriculum-based training paradigm that progressively transitions from explicit textual and visual CoT supervision to latent reasoning, and finally adapts latent reasoning dynamics to condition action generation. We construct two structured CoT datasets and evaluate LaRA-VLA on both simulation benchmarks and long-horizon real-robot manipulation tasks. Experimental results show that LaRA-VLA consistently outperforms state-of-the-art VLA methods while reducing inference latency by up to 90% compared to explicit CoT-based approaches, demonstrating latent reasoning as an effective and efficient paradigm for real-time embodied control. 


_Figure 1._ Comparison of CoT formulations in VLA models. (a) Textual CoT-based VLA explicitly generates discrete reasoning tokens and decodes them into actions through autoregressive (AR) policies or action experts (AE). (b) Most visual CoT-based VLA represents reasoning as discrete visual goal tokens before action generation. (c) Our model internalizes textual and visual reasoning into continuous latents. Visual goal latents align with perceptual features, encode future-oriented task information, and provide implicit supervision for textual CoT latents. 

## **1. Introduction** 

> 1Institute of Artificial Intelligence and Robotics, Xi’an Jiaotong University. 2Beijing Academy of Artificial Intelligence. 

> 3Institute of Automation, University of Chinese Academy of Sciences. 4School of Artificial Intelligence, University of Chinese Academy of Sciences. 5Peking Univeristy. Correspondence to: Cheng Chi _<_ chicheng@baai.ac.cn _>_ , Badong Chen _<_ chenbd@mail.xjtu.edu.cn _>_ , Shanghang Zhang _<_ shanghang@pku.edu.cn _>_ . 

Vision-Language-Action (VLA) models have emerged as a promising direction for scalable, general-purpose robotic manipulation (Kim et al., 2025b; Bai et al., 2025b), as they aim to end-to-end map rich multimodal observations and language instructions to continuous control commands. To improve VLA performance, a variety of training and inference strategies have been proposed (Bai et al., 2025c; Sridhar et al., 2025; Lin et al., 2025b). Among these approaches, incorporating Chain-of-Thought (CoT) reasoning 

_Preprint. May 11, 2026._ 

1 

**Latent Reasoning VLA** 

has proven particularly effective (Chen et al., 2025c). CoT is commonly framed as a teaching signal that encourages structured intermediate reasoning, thereby improving interpretability and generalization in long-horizon robotic tasks. 

Existing CoT approaches for VLA models can be broadly categorized by modality, as shown in Figure 1. Text-based CoT methods represent intermediate reasoning explicitly in natural language, covering task decomposition and highlevel planning, and may additionally verbalize information derived from visual observations (Zawalski et al., 2025; Sun et al., 2025b; Fan et al., 2025; Tan et al., 2026). Visual CoT methods instead express reasoning through visual reconstruction or prediction, typically by modeling future observations or intermediate visual states (Zhao et al., 2025a; Zhang et al., 2025b). A third line of work combines textual and visual CoT, leveraging multi-modal intermediate representations for reasoning (Zhang et al., 2025a). 

Despite their effectiveness, existing CoT-based methods face two fundamental challenges. First, text-based CoT often requires extensive textual reasoning during inference, leading to substantial computational overhead. Long reasoning traces dramatically increase token length, resulting in excessive KV-cache usage, high memory consumption, and increased latency. In practice, such models may operate at control frequencies below 5 Hz, or even around 1 Hz (Zawalski et al., 2025), which is unacceptable for real-time robotic control. Second, most CoT formulations rely on discrete representations: textual CoT is constrained to language tokens (Zawalski et al., 2025; Lin et al., 2025a), while visual CoT is typically aligned with discrete visual tokens produced by VQ-based tokenizers (Zhao et al., 2025a). We argue that CoT is effective not because it is expressed in natural language, but because it exposes structured intermediate reasoning. In embodied settings, where both perception and action evolve in continuous spaces, constraining reasoning to discrete tokens introduces a representational mismatch between reasoning and control. 

To address these challenges, we propose Latent Reasoning VLA (LaRA-VLA), a unified latent-reasoning VLA framework that performs reasoning and prediction entirely in latent space for robotic action. A comparison between LaRA-VLA and existing CoT-based VLA methods is summarized in Table 1. Inspired by latent chain-of-thought reasoning methods (Hao et al., 2024; Pham & Ngo, 2025; Huang et al., 2025), we adapt latent reasoning to embodied VLA models, enabling structured reasoning to be internalized into continuous latent representations. Different from Fast-ThinkAct (Huang et al., 2025), which mainly distills textual CoT into latent representations while retaining visually grounded reasoning as discrete traces, LaRA-VLA internalizes both textual and future-oriented visual CoT into continuous latents. The visual goal latents further serve as 

implicit multimodal supervision for textual latent reasoning, making the learned latent dynamics directly useful for action generation. 

Our training paradigm follows a three-stage progression that transitions from explicit multi-modal reasoning to latent embodied reasoning. Training begins with unified textual and visual CoT supervision, where textual reasoning steps and future visual predictions are explicitly aligned with their corresponding annotations. We then adopt a curriculum-based strategy that models embodied reasoning as a sequence of continuous latent states, gradually internalizing reasoning structure by replacing explicit textual CoT with a compact set of latent representations and relying on visual prediction objectives as implicit supervision. Once textual CoT is fully absorbed into latent reasoning, the model is further adapted to action generation, enabling latent reasoning dynamics to directly condition continuous control outputs. Throughout training, visual latents used for supervision are encoded by the same visual encoder as the input observations, and an exponential moving average (EMA) encoder is employed as a target network to stabilize latent representation learning and prevent representation collapse. 

Overall, our approach extends latent CoT reasoning from language-only settings to embodied VLA models, enabling efficient, action-oriented reasoning without explicit CoT generation at inference time. By coupling latent reasoning dynamics directly with action generation, LaRA-VLA allocates computation to compact latent “thought steps” rather than verbose textual reasoning, substantially reducing token expansion and inference latency. This makes the approach well-suited for real-time robotic control. Moreover, representing reasoning as continuous latent dynamics avoids the representational mismatch introduced by discrete language or visual tokens. To support this paradigm, we construct an automated CoT annotation pipeline that provides structured supervision, including subtask decomposition, movement reasoning, and target object localization, and curate latent reasoning datasets across both simulated and real-world environments, including LIBERO-LaRA, Bridge-LaRA, and real-robot demonstrations. Our contributions are threefold: 

- We introduce a latent-reasoning paradigm for Vision– Language–Action models, in which chain-of-thought reasoning is internalized into continuous latent representations across textual and visual modalities, enabling inference-efficient reasoning that aligns with continuous perception and control. 

- We propose LaRA-VLA, a unified VLA model that realizes this paradigm through a curriculum-based training strategy, progressively transitioning from explicit multi-modal CoT supervision to latent embodied reasoning, guided by predictive visual latent objectives and stabilized with EMA-based visual encoders. 

2 

**Latent Reasoning VLA** 

_Table 1._ A taxonomy of VLA models based on the representation forms of chain-of-thought CoT and actions. Specifically, we categorize models by whether their textual CoT is represented as explicit discrete tokens or continuous latent states, whether their visual CoT aligns with raw pixels, discrete visual tokens, or encoded continuous visual latents, and whether the action output is represented as discrete tokens or continuous values. 

|Method|Venue||Text CoT||Visual CoT|Action|
|---|---|---|---|---|---|---|
|||Presence|Form|Presence|Align Form|Form|
|||_VLAs_|_with Text CoT_||||
|ECoT (Zawalski et al.,2025)|CoRL 2024|✓|Discrete Token|_×_|–|Discrete|
|GraspVLA (Deng et al.,2025)|CoRL 2025|✓|Discrete Token|_×_|–|Continuous|
|_π_0_._5(Intelligence et al.,2025)|CoRL 2025|✓|Discrete Token|_×_|–|Continuous|
|ThinkAct (Huang et al.,2025)|NeurIPS 2025|✓|Discrete Token|_×_|–|Continuous|
|Fast-ThinkAct (Huang et al.,2026)|CVPR 2026|✓|Discrete Token &<br>Continuous Latent|_×_|–|Continuous|
|||_VLAs w_|_ith Visual CoT_||||
|CoT-VLA (Zhao et al.,2025a)|CVPR 2025|_×_|–|✓|Discrete Visual Tokens|Discrete|
|DreamVLA (Zhang et al.,2025b)|NeurIPS 2025|_×_|–|✓|Discrete Visual Tokens|Continuous|
|UD-VLA (Chen et al.,2025b)|ICLR 2026|_×_|–|✓|Discrete Visual Tokens|Discrete|
|VITA (Ma et al.,2025)|arXiv 2025|_×_|–|✓|Discrete Visual Tokens|Discrete|
||_VL_|_As with Bot_|_h Text and Visual CoT_||||
|UP-VLA (Zhang et al.,2025a)<br>**LaRA-VLA (Ours)**|ICML 2025<br>–|✓<br>✓|Discrete Token<br>Continuous Latent|✓<br>✓|Discrete Visual Tokens<br>Continuous Latent|Discrete<br>Continuous|


- We construct two structured chain-of-thought datasets, LIBERO-LaRA and Bridge-LaRA, featuring multimodal reasoning annotations for embodied manipulation, and conduct extensive evaluations in both simulation and long-horizon real-robot tasks to demonstrate the effectiveness and robustness of LaRA-VLA. 

## **2. Related Work** 

### **2.1. Vision Language Action Models** 

VLA models extend large multimodal language models to robotic control, with extensive efforts devoted to architectural advances (Black et al., 2024; Intelligence et al., 2025; Kim et al., 2025a; Cui et al., 2025) as well as trainingand inference-time optimizations (Sridhar et al., 2025; Lin et al., 2025b; Bai et al., 2026) since the introduction of RT2 (Zitkovich et al., 2023). Among these directions, CoT reasoning at training time has proven particularly effective. As summarized in Table 1, existing CoT-based VLA methods can be broadly categorized into textual CoT and visual CoT. Textual CoT methods generate explicit textual reasoning traces to refine task instructions or extract motion- and object-relevant information from visual observations (Zawalski et al., 2025; Sun et al., 2025b; Huang et al., 2025). Visual CoT methods, in contrast, reconstruct or predict visual observations conditioned on multimodal inputs, typically relying on discrete visual tokens produced by VQ-VAE-based representations (Zhao et al., 2025a; Zhang et al., 2025b; Lv et al., 2025). Despite their effectiveness, both paradigms rely on discrete tokenized reasoning. Textual CoT incurs long autoregressive generation chains with high inference cost, while both textual and visual CoT exhibit a mismatch 

with the inherently continuous perception and action spaces in robotics. To address these limitations, we introduce latent reasoning, in which textual CoT is replaced by compact continuous latent variables learned via curriculum-style training, and visual CoT is aligned with continuous visual representations from the perception backbone. 

A closely related work is Fast-ThinkAct (Huang et al., 2025), which reduces the inference cost of VLA CoT reasoning by distilling explicit reasoning traces into latent representations. However, it mainly latentizes textual CoT, while visually grounded reasoning remains in a discrete trace-based form. In contrast, LaRA-VLA progressively internalizes both textual CoT and future-oriented visual CoT into continuous latent representations, where visual goal latents provide implicit supervision for textual latent reasoning and directly support action generation. 

### **2.2. Latent Reasoning in LLMs and VLMs** 

Explicit CoT can improve reasoning performance but often incurs verbose intermediate outputs, high inference latency, and a reliance on discrete tokens. These drawbacks have motivated implicit or continuous reasoning in latent space, which preserves multi-step computation without explicit reasoning traces (Xu et al., 2025; Ruan et al., 2025). In language models, latent reasoning is typically instantiated through hidden states or continuous variables that function as implicit thought. For instance, Coconut (Hao et al., 2024) shows that latent reasoning supports richer internal search while achieving a more favorable accuracy–efficiency tradeoff than explicit CoT. SIM-CoT (Wei et al., 2025) identifies optimization instability when scaling implicit reason- 

3 

**Latent Reasoning VLA** 

ing tokens and introduces supervised stabilization, while CoDi (Shen et al., 2025) distills explicit CoT into continuous latent representations via self-distillation. Latent reasoning has also been extended to vision–language models, where multimodal latents serve as internal reasoning states rather than explicit symbolic traces (Sun et al., 2025a; Pham & Ngo, 2025). To adapt latent reasoning to VLA, we adopt a staged training strategy that initializes structured reasoning with explicit CoT and progressively transfers it into latent space. Unlike prior methods that rely solely on answer supervision, we jointly ground latent reasoning in visual representations and action signals, enabling control-relevant reasoning that supports stable policy learning and efficient action generation without explicit CoT at inference time. 

## **3. Method** 

In this section, we present the complete pipeline of our Latent Reasoning VLA (LaRA-VLA) framework. We first describe the construction of structured CoT datasets in Section 3.1. We then introduce the model architecture of LaRA-VLA and detail its training procedures in Sections 3.2 and 3.3, respectively. 

### **3.1. Data Collection** 

Effective robotic manipulation requires the joint modeling of long-horizon subtask structure, spatial grounding of target objects, and motion-level reasoning for action execution. However, existing data collection pipelines typically capture these components in isolation, leading to redundant or incomplete supervision (e.g., exhaustive object-level bounding boxes in ECoT (Zawalski et al., 2025) or missing target localization in Emma-x (Sun et al., 2025b)). To address these limitations, we develop a fully automated annotation pipeline following an anchor-first, generate-later paradigm driven by semantic and temporal anchors. Semantic anchors are extracted using Qwen3-VL (Bai et al., 2025a) from the initial frame and task instruction to identify the manipulated object, while temporal anchors are obtained by segmenting robot trajectories into atomic manipulation stages based on gripper state changes. Conditioned on these anchors, Qwen3-VL generates concise subtask descriptions, and open-vocabulary grounding with GroundingDINO (Liu et al., 2024) and SAM3 (Carion et al., 2025) produces temporally consistent target object bounding boxes. Motion reasoning is derived from end-effector trajectories by computing goal-directed and local motions, which are discretized into directional descriptors and incorporated into the CoT annotations. Details are provided in Figure 10 and Appendix B. 

Based on this pipeline, we construct two benchmark datasets on simulated environments, LIBERO (Liu et al., 2023) and SimplerEnv (Li et al., 2025), resulting in _LIBERO-LaRA_ 

and _Bridge-LaRA_ , and further apply the same framework to a long-horizon real-world robotic manipulation dataset collected on physical hardware. 

### **3.2. Model Architecture** 

We adopt Qwen3-VL (Bai et al., 2025a) as the backbone VLM to leverage its strong built-in reasoning capability, and directly inherit its image encoder to ensure consistent visual representations throughout training. To predict visual goal information, we introduce a dedicated <img ~~n~~ ext> token to represent predicted visual latents, which enables explicit supervision and alignment during early-stage latent reasoning learning. For action prediction in Stages I and II, we follow an autoregressive action token design similar to (Pertsch et al., 2025), allowing the model to learn action generation jointly with latent reasoning in a stable and efficient manner. In the final stage, we remove explicit action token prediction and instead activate a dedicated action expert, decoupling action generation from token-level autoregressive decoding. Specifically, action generation is performed by a 16-layer Diffusion Transformer composed of alternating self-attention and cross-attention layers, which conditions on the learned latent representations to produce continuous action trajectories. 

### **3.3. Training Procedures** 

**Stage I: Explicit CoT Fine-Tuning.** In the first stage, we fine-tune the VLM on embodied datasets with explicit CoT annotations constructed in Section 3.1. These annotations provide structured reasoning supervision, including task decomposition, movement reasoning, and target object information, enabling the model to adapt to embodied manipulation tasks with explicit intermediate reasoning. Given input images and a language instruction, the image encoder first maps the visual observation to a sequence of visual tokens, denoted as **v** , while the instruction text is tokenized into textual tokens, denoted as **x** . The VLM jointly attends to both visual and textual tokens and is trained to autoregressively generate a sequence of CoT tokens. During this stage, discrete ground-truth textual tokens are used to explicitly supervise CoT generation via teacher forcing. The training objective is defined as the negative log-likelihood of the ground-truth CoT sequence: 


where _{ct}_<sup>_T_</sup> _t_ =1<sup>CoTis the ground-truth CoT token sequence,</sup><sup>_c<t_</sup> is the preceding CoT tokens, and _pθ_ ( _·_ ) is the conditional token distribution parameterized by the VLM. 

In addition to textual supervision, we align visual reasoning by predicting future visual latents. Let **z** _t_ +1 denote the vi- 

4 

**Latent Reasoning VLA** 


_Figure 2._ **Overview of LaRA-VLA.** Training proceeds in three stages: (i) explicit CoT fine-tuning with aligned visual prediction latents and inverse-dynamics supervision for actions; (ii) a curriculum-based transition from explicit CoT to compact text latents, gradually reducing the number of text tokens while increasing reliance on latent reasoning, where the latent representations are also implicitly supervised by visual and action signals; and (iii) adaptation of latent-conditioned VLM features to an action expert for efficient action generation without explicit CoT at inference time. 

sual latent representation of the next observation encoded by the same visual encoder used for the input observations. The VLM predicts this latent from the current context, yielding the following alignment objective: 


where ˆ **z** _t_ +1 is the predicted visual latent and **z** _t_ +1 is obtained by encoding the next observation. To stabilize visual latent learning and prevent representation collapse, we follow prior work (Chen et al., 2025a) and update the parameters used to compute target visual latents using an exponential moving average (EMA) of the online encoder parameters: 


where _θv_<sup>_t_denotes the parameters of the online visual encoder</sup> at iteration _t_ , _θ_<sup>¯</sup> _v_<sup>_t_denotes the corresponding EMA-averaged</sup> parameters used to compute stable target visual latents, and _τv_ is the decay rate. 

We further leverage the predicted future visual representations together with the preceding visual and textual context to infer actions via an inverse dynamics model. Specifically, we employ an inverse dynamics function _f_ ( **v** _t,_ **v** _t_ +1 _|_ **x** _, c_ ) = **a** _t_ , which estimates the action that induces the transition between consecutive visual states conditioned on the instruction and the intermediate reasoning step. To efficiently propagate action information across latent reasoning steps, we adopt the fast recursive generation framework of (Pertsch et al., 2025), which assigns coarse-grained action 

semantics to all latent representations. Concretely, action tokens are trained using an autoregressive objective, similar to Equation 1, yielding the action-token loss _L_ act-dis. 

**Stage II: Curriculum-based Replacement of Discrete CoT Tokens.** In the second stage, we internalize explicit textual reasoning into the latent space through a curriculumbased training strategy. Embodied reasoning is modeled as a sequence of continuous latent states, and discrete CoT tokens are progressively replaced by latent representations during training. Formally, we adopt the same training objectives as in Stage I, including the textual CoT likelihood and the visual latent prediction loss. However, instead of supervising all reasoning steps with discrete ground-truth CoT tokens, we gradually mask out subsets of CoT tokens and replace them with learnable latent representations. The proportion of discrete CoT tokens decreases over training according to a predefined curriculum schedule, until the entire chain-of-thought is fully internalized in the latent space. 

**Stage III: Action Generation via Flow Matching.** To adapt latent reasoning to continuous control, we train the action prediction module using a flow matching objective. Let **a** _t_ denote the ground-truth action at time step _t_ , and let _ϵ ∼N_ ( **0** _,_ **I** ) be Gaussian noise. Following the flow matching formulation, we define a linear interpolation between noise and action as **a** _τ_ = (1 _− τ_ ) _ϵ_ + _τ_ **a** _t,_ where _τ ∼U_ (0 _,_ 1). The action expert predicts a velocity field _vθ_ ( **a** _τ , τ |_ **h** _t_ ) conditioned on a multi-modal latent context **h** _t_ . Specifically, **h** _t_ aggregates the latent representation 

5 

**Latent Reasoning VLA** 

_Table 2._ Performance comparisons with state-of-the-art methods on LIBERO, grouped by different CoT paradigms. 

|**CoT Type**|**Method**|**Spatial**|**Goal**|**Object**|**Long**|**Avg.**|
|---|---|---|---|---|---|---|
||OpenVLA (Kim et al.,2025b)|84.7|88.4|79.2|53.7|76.5|
|No CoT|_π_0 (Black et al.,2024)|96.8|98.8|95.8|85.2|94.2|
||OpenVLA-OFT (Kim et al.,2025a)|97.6|98.4|97.9|94.5|97.1|
||ThinkAct (Huang et al.,2025)|88.3|91.4|87.1|70.9|84.4|
|Textual CoT|MolmoAct (Lee et al.,2025)|87.0|95.4|87.6|77.2|86.6|
||_π_0_._5 (Intelligence et al.,2025)|98.8|98.2|98.0|92.4|96.8|
||DeepThinkVLA (Yin et al.,2025)|99.0|96.6|96.4|96.2|97.0|
||CoT-VLA (Zhao et al.,2025a)|87.5|91.6|87.6|69.0|81.1|
|Visual CoT|DreamVLA (Zhang et al.,2025b)|97.5|94.0|89.5|89.5|92.6|
||F1 (Lv et al.,2025)|98.2|97.8|95.4|91.3|95.7|
||UD-VLA (Chen et al.,2025b)|94.1|95.7|91.2|89.6|92.7|
|Latent CoT|Fast-ThinkAct (Huang et al.,2026)|92.0|97.2|90.2|79.4|89.7|
||**LaRA-VLA (Ours)**|96.4|98.6|99.8|96.6|**97.9**|


_Figure 3._ Attention mechanism used in LaRA-VLA. 

of the current visual observation and language instruction, the intermediate text-based reasoning latent, and the predicted future visual latent produced by the VLM. Through the inverse dynamics supervision applied in earlier stages, this latent context already encodes coarse-grained actionrelevant information. As a result, we do not introduce an additional action latent, and actions are generated directly from the shared multi-modal latent representation. The flow matching loss is defined as 


where **h** _t_ denotes the multi-modal latent context produced by the VLM at time step _t_ . 

**LaRA Attention Mechanism.** We introduce an attention mechanism tailored to our three-stage training paradigm, as illustrated in Figure 3. The model operates on multimodal tokens including text, current image, future image, and action tokens, with attention constraints explicitly regulating cross-token information flow. Here, text tokens serve as a unified abstraction that corresponds to language instructions and textual chain-of-thought in Stages I and II, and 

to text latents in Stages II and III. In Stages I and II, future image tokens attend causally to text and current image tokens, while interacting bidirectionally among themselves. Action tokens are generated autoregressively: each action token attends to all preceding text, current image, and future image tokens, as well as previously generated action tokens. In Stage III, action tokens are excluded from the attention computation, and the model is trained solely over text and vision tokens under the same attention constraints. 

**Loss Function.** Our training objective is stage-dependent and follows a curriculum-style design. In Stage I, we jointly optimize the CoT supervision loss, the visual alignment loss, and the discrete action loss, i.e., _L_ cot + 0 _._ 1 _L_ vis + _L_ act-dis, to initialize structured reasoning and action grounding. In Stage II, we progressively anneal the explicit CoT supervision loss _L_ cot to zero. The model is lastly optimized using 0 _._ 2 _L_ vis + _L_ act-dis, which promotes latent-space reasoning while maintaining accurate action semantics. Finally, in Stage III, discrete action supervision is replaced by continuous action regression, and we optimize _L_ act-con to enable efficient continuous action generation. 

## **4. Experiments** 

We evaluate the effectiveness of LaRA-VLA and the overall system through a comprehensive set of experiments spanning both simulation benchmarks and real-world robotic manipulation tasks. Our experiments are designed to address the following questions: 

• How effective is LaRA-VLA compared to state-of-the-art methods in simulation benchmarks? (Section 4.1) 

- How well does LaRA-VLA perform on **long-horizon** 

- real-world manipulation tasks compared to state-of-the-art approaches? (Section 4.2) 

- How effective are the latent reasoning components in 

- LaRA-VLA, and what additional advantages does our ap- 

6 

**Latent Reasoning VLA** 

_Table 3._ Performance comparisons with state-of-the-art methods on SimplerEnv-WindowX, grouped by different CoT paradigms. 

|**CoT Type**|**Method**|**Put**<br>**Spoon**|**Put**<br>**Carrot**|**Stack**<br>**Block**|**Put**<br>**Eggplant**|**Avg.**|
|---|---|---|---|---|---|---|
||OpenVLA (Kim et al.,2025b)|0.0|0.0|0.0|4.1|1.0|
||Octo (Ghosh et al.,2024)|47.2|9.7|4.2|56.9|29.5|
|No CoT|OpenVLA-OFT (Kim et al.,2025a)|12.5|4.2|8.3|37.5|39.6|
||_π_0 (Black et al.,2024)|29.1|0.0|16.7|62.5|40.1|
||CogACT (Li et al.,2024)|71.7|50.8|15.0|67.5|51.3|
|Textual CoT|ThinkAct (Huang et al.,2025)|58.3|37.5|8.7|70.8|43.8|
|Vil CT|F1 (Lv et al.,2025)|50.0|70.8|50.0|66.7|59.4|
|sua o|UD-VLA (Chen et al.,2025b)|58.3|62.5|54.1|75.0|62.5|
|Latent CoT|**LaRA-VLA (Ours)**|95.8|62.5|25.0|91.7|**68.8**|


_Figure 4._ Real-world setup of four long-horizon tasks. 

proach offer? (Section 4.3) 

### **4.1. Simulation Experiments** 

**Benchmarks and Datasets.** We conduct experiments on two widely used benchmarks, LIBERO (Liu et al., 2023) and SimplerEnv (Li et al., 2025). LIBERO consists of four task suites, Spatial, Goal, Object, and Long, each containing 10 single-arm manipulation tasks. We report success rates for each suite and the overall average over 50 rollouts per task. SimplerEnv evaluates real-to-sim generalization of robot manipulation policies trained on real-world data. We evaluate on WidowX robots across four tasks and report pertask success rates and the overall average over 24 rollouts per task. Based on these benchmarks, we construct two training datasets, LIBERO-LaRA and Bridge-LaRA, which are used to train LaRA-VLA. 

**Baselines.** For LIBERO, we compare against a broad set of state-of-the-art VLA methods covering different CoT paradigms. No-CoT baselines include OpenVLA (Kim et al., 2025b), _π_ 0 (Black et al., 2024), and OpenVLAOFT (Kim et al., 2025a). Textual CoT baselines include 


_Figure 5._ Real-world results. 

ThinkAct (Huang et al., 2025), MolmoAct (Lee et al., 2025), _π_ 0 _._ 5 (Intelligence et al., 2025), and DeepThinkVLA (Yin et al., 2025). Visual CoT methods include CoT-VLA (Zhao et al., 2025a), DreamVLA (Zhang et al., 2025b), F1 (Lv et al., 2025), and UD-VLA (Chen et al., 2025b). We additionally compare with the latent CoT method FastThinkAct (Huang et al., 2026). For SimplerEnv, we follow the standard evaluation protocol and compare against representative baselines. No-CoT methods include OpenVLA, Octo (Ghosh et al., 2024), OpenVLA-OFT, _π_ 0, and CogACT (Li et al., 2024). We further include textual CoT (ThinkAct) and visual CoT (F1, UD-VLA) baselines. Implementation details and training hyperparameters of LaRAVLA are provided in Appendix A. 

**Results.** Tables 2 and 3 summarize quantitative results on the LIBERO and SimplerEnv-WidowX benchmarks. On LIBERO, LaRA-VLA achieves the best overall performance with an average success rate of 97.9%, including 99.8% on the Object suite and 96.6% on the Long suite, demonstrating strong object-centric reasoning and robustness in longhorizon manipulation. On SimplerEnv-WidowX, which evaluates real-to-sim generalization under diverse visual conditions, LaRA-VLA attains the highest average success rate of 68.8%, outperforming No-CoT, Textual CoT, and Visual CoT baselines. Across both benchmarks, LaRA-VLA consistently surpasses textual and visual CoT methods, indicating that latent reasoning provides more effective and 

7 

**Latent Reasoning VLA** 

_Table 4._ Robustness under visual perturbations. We report task success rates under Gaussian blur and Gaussian noise with two severity levels. H and L denote high- and low-severity perturbations, respectively. 

|**Benchmark**|**Method**|**Gaussian Blur-H**|**Gaussian Blur-L**|**Gaussian Noise-H**|**Gaussian Noise-L**|
|---|---|---|---|---|---|
|LIBERO|Qwen-GR00T (Community,2026)|30.0|76.0|55.7|87.9|
||**LaRA-VLA (Ours)**|**42.9**|**79.4**|**76.0**|**92.7**|
|SimlrEn|Qwen-GR00T (Community,2026)|13.5|35.4|8.3|22.9|
|pev|**LaRA-VLA (Ours)**|**56.3**|**62.5**|**22.9**|**31.2**|


_Table 5._ Ablation study of different forms of CoT supervision on SimplerEnv. Text-CoT denotes explicit textual chain-of-thought, Latent Text-CoT denotes latent textual chain-of-thought, and Latent Vis-CoT denotes latent visual chain-of-thought. 

|Text-CoT|Latent Text-CoT|Latent Vis-CoT|SR (%)|
|---|---|---|---|
|_×_|_×_|_×_|55.2|
|✓|_×_|_×_|58.3|
|_×_|✓|_×_|64.6|
|_×_|_×_|✓|63.5|
|_×_|✓|✓|**68.8**|


stable guidance for action prediction and generalizes better than explicit CoT supervision. 


_Figure 6._ Latent-space distributions under Gaussian blur and Gaussian noise. Clean and perturbed latent remain clustered by semantic role, with only moderate distributional shifts, suggesting that the learned latent representations are stable under visual corruptions. 

### **4.2. Real-World Experiments** 

**Real-World Setup.** As illustrated in Figure 4, our realworld setup uses an Agilex Cobot Magic wheeled platform equipped with three RGB-D cameras. We consider four categories of long-horizon manipulation tasks: putting all objects into the basket, sorting fruits into the basket, finding a block and placing it into the basket, and stacking two bowls. For data collection, we record 100 demonstration trajectories per task category at 30 Hz. During evaluation, each task is executed for 12 rollout trials. We compare our method against ACT (Zhao et al., 2023), ECoT (Zawalski et al., 2025) and GR00T N1.5 (Bjorck et al., 2025) as baselines. Implementation details are provided in Appendix A. 

**Results.** As shown in Figure 5, LaRA-VLA achieves the highest average success rate among all compared methods, substantially outperforming ACT and ECoT and surpassing GR00T N1.5 overall. In particular, LaRA-VLA attains the best performance on three out of four long-horizon realworld manipulation tasks, with especially notable gains on tasks that require multi-stage reasoning and sustained temporal coordination. These results suggest that latent reasoning improves robustness to error accumulation over long-horizon manipulation. 

### **4.3. Analysis** 

**Ablation Study.** Table 5 shows that latent CoT supervision provides substantially larger gains than explicit textual CoT. While explicit textual CoT yields only marginal improvement over the no-CoT baseline, latent textual CoT leads 

to a significant increase in success rate, highlighting the effectiveness of internalized textual reasoning. Further incorporating latent visual CoT yields the best performance, as it both injects predictive visual information about future states and implicitly regularizes the latent textual CoT through multimodal alignment. Overall, these results indicate that structured latent CoT representations, especially when jointly learned across modalities, are more effective than explicit textual reasoning for embodied policy learning. 

### **Robustness of Lantent Representations and LaRA-VLA.** 

To further evaluate whether the learned latent representations remain stable under input perturbations, we conduct additional stress tests on LIBERO and SimplerEnv with two common visual corruptions: Gaussian noise and Gaussian blur. For Gaussian noise, we use standard deviations of 50 and 30 for the high- and low-severity settings, respectively. For Gaussian blur, we use a kernel size of 15 _×_ 15 with _σx_ = _σy_ = 5 for the high-severity setting, and a kernel size of 9 _×_ 9 with _σx_ = _σy_ = 3 for the low-severity setting. 

We analyze both latent-space changes and task-level robustness. As shown in Figure 6, the latent reasoning tokens remain semantically consistent under corrupted observations, with only moderate distributional shifts. This suggests that the learned latent space does not collapse or become highly unstable under visual perturbations. We further compare LaRA-VLA with Qwen-GR00T (Community, 2026), which serves as a no-CoT baseline without latent reasoning. As shown in Table 4, both models degrade under visual 

8 

**Latent Reasoning VLA** 


_Figure 8._ Inference time comparison on an NVIDIA A100 GPU. 

_Figure 7._ Latent collapse analysis. 

corruption, but LaRA-VLA consistently maintains higher success rates across all perturbation types and severity levels. These results indicate that latent CoT reasoning not only improves clean performance, but also enhances robustness to corrupted visual inputs. 

**Latent Collapse.** As shown in Figure 7, we observe no evidence of latent representation collapse. Latent tokens associated with different reasoning components form wellseparated and semantically coherent clusters, demonstrating clear functional specialization rather than degeneration into uniform or uninformative representations. Moreover, latent representations of language instruction tokens (gray points) remain structured and occupy a distinct subspace from reasoning latents, indicating that latent CoT does not trivially reuse language embeddings. Together, these findings show that predictive supervision and action grounding provide sufficient inductive bias to maintain structured latent reasoning, even without explicit discrete chain-of-thought generation at inference time. 

**Inference Efficiency.** As shown in Figure 8, LaRA-VLA achieves the lowest inference latency among all compared methods, requiring only 135 ms per rollout. Compared with explicit CoT methods, LaRA-VLA avoids autoregressive textual reasoning and reduces inference time by up to 90%. Notably, LaRA-VLA is also faster than Fast-ThinkAct, which uses latent CoT reasoning, suggesting that our compact latent design further improves efficiency beyond simply replacing explicit CoT with latent tokens. This advantage may come from using fewer latent reasoning tokens, compact visual goal latents, and a lightweight action expert. 

## **5. Limitations** 

Although LaRA-VLA achieves fast inference and strong performance through latent chain-of-thought reasoning, several limitations remain and warrant further investigation. First, latent CoT representations may suffer from collapse in the absence of explicit supervision, where the semantics of la- 

tent tokens degenerate toward homogeneous representations, particularly as the number of latent tokens increases (Wei et al., 2025). To mitigate this risk, our current implementation restricts latent reasoning to a single token per step, which may limit expressiveness. Second, the training procedure is not maximally efficient. LaRA-VLA employs a curriculum learning strategy that gradually replaces explicit CoT tokens with latent representations. As training progresses, the number of CoT-related tokens increases, resulting in higher training cost. Improving training efficiency while preserving stable latent reasoning remains an important direction for future work. 

## **6. Conclusion** 

We presented LaRA-VLA, a latent reasoning framework for Vision–Language–Action models that internalizes chainof-thought reasoning into continuous latent representations across both textual and visual modalities. Rather than generating long explicit CoT sequences at inference time, LaRAVLA replaces them with compact textual CoT latents and employs a curriculum-based training strategy to progressively transfer explicit reasoning into latent space. Visual latents are aligned with continuous perceptual features encoded by a shared visual encoder and stabilized using an exponential moving average, providing implicit supervisory signals that guide the learning of textual CoT latents. Experiments on simulated benchmarks and long-horizon real-robot manipulation tasks demonstrate that LaRA-VLA achieves strong performance while significantly improving inference efficiency, supporting the view that structured reasoning for embodied agents can be effectively realized in latent space without explicit chain-of-thought generation. 

## **Acknowledgements** 

This work was supported by the National Natural Science Foundation of China (Grant No. U25A20540), the NSFC General Program (Grant No. 62436005). 

9 

**Latent Reasoning VLA** 

## **Impact Statement** 

This paper aims to advance machine learning methods for robotic manipulation by improving the efficiency and scalability of reasoning in Vision–Language–Action models. The proposed approach introduces architectural and training innovations that enable effective reasoning without explicit chain-of-thought generation, potentially facilitating real-time robotic deployment. While such advances may benefit a wide range of robotic applications, including automation and assistive technologies, we do not identify any societal risks uniquely introduced by this work beyond those generally associated with robotic systems. As with related research, the broader impact will depend on how the technology is applied and governed in practice. 

## **References** 

- Bai, S., Cai, Y., Chen, R., Chen, K., Chen, X., Cheng, Z., Deng, L., Ding, W., Gao, C., Ge, C., et al. Qwen3-vl technical report, 2025a. _URL https://arxiv. org/abs/2511.21631_ , 2025a. 

- Bai, S., Song, W., Chen, J., Ji, Y., Zhong, Z., Yang, J., Zhao, H., Zhou, W., Zhao, W., Li, Z., et al. Towards a unified understanding of robot manipulation: A comprehensive survey. _arXiv preprint arXiv:2510.10903_ , 2025b. 

- Bai, S., Zhou, W., Ding, P., Zhao, W., Wang, D., and Chen, B. Rethinking latent redundancy in behavior cloning: An information bottleneck approach for robot manipulation. In _Forty-second International Conference on Machine Learning_ , 2025c. 

- Bai, S., Wang, D., Chi, C., Zhou, W., Lyu, J., Zhao, X., Wang, P., Wang, Z., Xing, L., Zhang, S., et al. Reshaping action error distributions for reliable vision-languageaction models. _arXiv preprint arXiv:2602.04228_ , 2026. 

- Bjorck, J., Castaneda, F., Cherniadev, N., Da, X., Ding, R.,˜ Fan, L., Fang, Y., Fox, D., Hu, F., Huang, S., et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., et al. _pi_ ~~0~~ : A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- Carion, N., Gustafson, L., Hu, Y.-T., Debnath, S., Hu, R., Suris, D., Ryali, C., Alwala, K. V., Khedr, H., Huang, A., et al. Sam 3: Segment anything with concepts. _arXiv preprint arXiv:2511.16719_ , 2025. 

- Chen, D., Shukor, M., Moutakanni, T., Chung, W., Yu, J., Kasarla, T., Bolourchi, A., LeCun, Y., and Fung, P. Vljepa: Joint embedding predictive architecture for visionlanguage. _arXiv preprint arXiv:2512.10942_ , 2025a. 

- Chen, J., Song, W., Ding, P., Zhou, Z., Zhao, H., Tang, F., Wang, D., and Li, H. Unified diffusion vla: Visionlanguage-action model via joint discrete denoising diffusion process. _arXiv preprint arXiv:2511.01718_ , 2025b. 

- Chen, W., Belkhale, S., Mirchandani, S., Mees, O., Driess, D., Pertsch, K., and Levine, S. Training strategies for efficient embodied reasoning. _arXiv preprint arXiv:2505.08243_ , 2025c. 

- Community, S. Starvla: A lego-like codebase for visionlanguage-action model developing. _arXiv preprint arXiv:2604.05014_ , 2026. 

- Cui, C., Ding, P., Song, W., Bai, S., Tong, X., Ge, Z., Suo, R., Zhou, W., Liu, Y., Jia, B., et al. Openhelix: A short survey, empirical analysis, and open-source dualsystem vla model for robotic manipulation. _arXiv preprint arXiv:2505.03912_ , 2025. 

- Deng, S., Yan, M., Wei, S., Ma, H., Yang, Y., Chen, J., Zhang, Z., Yang, T., Zhang, X., Zhang, W., et al. Graspvla: a grasping foundation model pre-trained on billion-scale synthetic action data. _Conference on Robot Learning_ , 2025. 

- Fan, Y., Bai, S., Tong, X., Ding, P., Zhu, Y., Lu, H., Dai, F., Zhao, W., Liu, Y., Huang, S., et al. Long-vla: Unleashing long-horizon capability of vision language action model for robot manipulation. In _Conference on Robot Learning_ , pp. 2018–2037. PMLR, 2025. 

- Ghosh, D., Walke, H. R., Pertsch, K., Black, K., Mees, O., Dasari, S., Hejna, J., Kreiman, T., Xu, C., Luo, J., et al. Octo: An open-source generalist robot policy. In _Robotics: Science and Systems_ , 2024. 

- Hao, S., Sukhbaatar, S., Su, D., Li, X., Hu, Z., Weston, J., and Tian, Y. Training large language models to reason in a continuous latent space. _arXiv preprint arXiv:2412.06769_ , 2024. 

- Huang, C.-P., Wu, Y.-H., Chen, M.-H., Wang, Y.-C. F., and Yang, F.-E. Thinkact: Vision-language-action reasoning via reinforced visual latent planning. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. 

- Huang, C.-P., Man, Y., Yu, Z., Chen, M.-H., Kautz, J., Wang, Y.-C. F., and Yang, F.-E. Fast-thinkact: Efficient vision-language-action reasoning via verbalizable latent planning. _arXiv preprint arXiv:2601.09708_ , 2026. 

- Intelligence, P., Black, K., Brown, N., Darpinian, J., Dhabalia, K., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., et al. _π_ 0 _._ 5: A vision-language-action model with open-world generalization. In _Conference on Robot Learning_ , 2025. 

10 

**Latent Reasoning VLA** 

- Kim, M. J., Finn, C., and Liang, P. Fine-tuning visionlanguage-action models: Optimizing speed and success. In _Robotics: Science and Systems_ , 2025a. 

- Kim, M. J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E. P., Sanketi, P. R., Vuong, Q., et al. Openvla: An open-source visionlanguage-action model. In _Conference on Robot Learning_ , pp. 2679–2713. PMLR, 2025b. 

- Lee, J., Duan, J., Fang, H., Deng, Y., Li, B., Liu, S., Fang, B., Zhang, J., Wang, Y. R., Lee, S., et al. Molmoact: Action reasoning models that can reason in space. In _Workshop on Making Sense of Data in Robotics: Composition, Curation, and Interpretability at Scale at CoRL 2025_ , 2025. 

- Li, Q., Liang, Y., Wang, Z., Luo, L., Chen, X., Liao, M., Wei, F., Deng, Y., Xu, S., Zhang, Y., et al. Cogact: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation. _arXiv preprint arXiv:2411.19650_ , 2024. 

- Li, X., Hsu, K., Gu, J., Mees, O., Pertsch, K., Walke, H. R., Fu, C., Lunawat, I., Sieh, I., Kirmani, S., et al. Evaluating real-world robot manipulation policies in simulation. In _Conference on Robot Learning_ , pp. 3705–3728. PMLR, 2025. 

- Lin, F., Nai, R., Hu, Y., You, J., Zhao, J., and Gao, Y. Onetwovla: A unified vision-language-action model with adaptive reasoning. _arXiv preprint arXiv:2505.11917_ , 2025a. 

- Lin, J., Taherin, A., Akbari, A., Akbari, A., Lu, L., Chen, G., Padir, T., Yang, X., Chen, W., Li, Y., et al. Vote: visionlanguage-action optimization with trajectory ensemble voting. _arXiv preprint arXiv:2507.05116_ , 2025b. 

- Liu, B., Zhu, Y., Gao, C., Feng, Y., Liu, Q., Zhu, Y., and Stone, P. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791, 2023. 

- Liu, S., Zeng, Z., Ren, T., Li, F., Zhang, H., Yang, J., Jiang, Q., Li, C., Yang, J., Su, H., et al. Grounding dino: Marrying dino with grounded pre-training for open-set object detection. In _European conference on computer vision_ , pp. 38–55. Springer, 2024. 

- Lv, Q., Kong, W., Li, H., Zeng, J., Qiu, Z., Qu, D., Song, H., Chen, Q., Deng, X., and Pang, J. F1: A vision-languageaction model bridging understanding and generation to actions. _arXiv preprint arXiv:2509.06951_ , 2025. 

- Ma, X., Xing, L., Zhang, H., Li, W., and Lu, S. Unifying perception and action: A hybrid-modality pipeline with implicit visual chain-of-thought for robotic action generation. _arXiv preprint arXiv:2511.19859_ , 2025. 

- Pertsch, K., Stachowicz, K., Ichter, B., Driess, D., Nair, S., Vuong, Q., Mees, O., Finn, C., and Levine, S. Fast: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 

- Pham, T.-H. and Ngo, C. Multimodal chain of continuous thought for latent-space reasoning in vision-language models. _arXiv preprint arXiv:2508.12587_ , 2025. 

- Ruan, Y., Band, N., Maddison, C. J., and Hashimoto, T. Reasoning to learn from latent thoughts. _arXiv preprint arXiv:2503.18866_ , 2025. 

- Shen, Z., Yan, H., Zhang, L., Hu, Z., Du, Y., and He, Y. Codi: Compressing chain-of-thought into continuous space via self-distillation. _arXiv preprint arXiv:2502.21074_ , 2025. 

- Sridhar, K., Dutta, S., Jayaraman, D., and Lee, I. Ricl: Adding in-context adaptability to pre-trained visionlanguage-action models. In _Conference on Robot Learning_ , pp. 5022–5038. PMLR, 2025. 

- Sun, G., Hua, H., Wang, J., Luo, J., Dianat, S., Rabbani, M., Rao, R., and Tao, Z. Latent chain-of-thought for visual reasoning. _arXiv preprint arXiv:2510.23925_ , 2025a. 

- Sun, Q., Hong, P., Pala, T. D., Toh, V., Tan, U.-X., Ghosal, D., and Poria, S. Emma-x: An embodied multimodal action model with grounded chain of thought and lookahead spatial reasoning. In _Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , pp. 14199–14214, 2025b. 

- Tan, H., Co, P., Xu, Y., Rong, S., Ji, Y., Chi, C., Chen, X., Zhang, Q., Zhao, Z., Wang, P., et al. Actionsketcher: From reasoning to action via visual sketches for long-horizon robotic manipulation. _arXiv preprint arXiv:2601.01618_ , 2026. 

- Wei, X., Liu, X., Zang, Y., Dong, X., Cao, Y., Wang, J., Qiu, X., and Lin, D. Sim-cot: Supervised implicit chain-ofthought. _arXiv preprint arXiv:2509.20317_ , 2025. 

- Xu, Y., Guo, X., Zeng, Z., and Miao, C. Softcot: Soft chain-of-thought for efficient reasoning with llms. _arXiv preprint arXiv:2502.12134_ , 2025. 

- Yin, C., Lin, Y., Xu, W., Tam, S., Zeng, X., Liu, Z., and Yin, Z. Deepthinkvla: Enhancing reasoning capability of vision-language-action models. _arXiv preprint arXiv:2511.15669_ , 2025. 

- Zawalski, M., Chen, W., Pertsch, K., Mees, O., Finn, C., and Levine, S. Robotic control via embodied chain-ofthought reasoning. In _Conference on Robot Learning_ , pp. 3157–3181. PMLR, 2025. 

11 

**Latent Reasoning VLA** 

- Zhang, J., Guo, Y., Hu, Y., Chen, X., Zhu, X., and Chen, J. Up-vla: A unified understanding and prediction model for embodied agent. In _Forty-second International Conference on Machine Learning_ , 2025a. 

- Zhang, W., Liu, H., Qi, Z., Wang, Y., Yu, X., Zhang, J., Dong, R., He, J., Wang, H., Zhang, Z., et al. Dreamvla: A vision-language-action model dreamed with comprehensive world knowledge. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025b. 

- Zhao, Q., Lu, Y., Kim, M. J., Fu, Z., Zhang, Z., Wu, Y., Li, Z., Ma, Q., Han, S., Finn, C., et al. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 1702–1713, 2025a. 

- Zhao, T., Kumar, V., Levine, S., and Finn, C. Learning finegrained bimanual manipulation with low-cost hardware. _Robotics: Science and Systems XIX_ , 2023. 

- Zhao, W., Ding, P., Min, Z., Gong, Z., Bai, S., Zhao, H., and Wang, D. Vlas: Vision-language-action model with speech instructions for customized robot manipulation. In _The Thirteenth International Conference on Learning Representations_ , 2025b. 

- Zitkovich, B., Yu, T., Xu, S., Xu, P., Xiao, T., Xia, F., Wu, J., Wohlhart, P., Welker, S., Wahid, A., et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pp. 2165–2183. PMLR, 2023. 

12 

**Latent Reasoning VLA** 

## **A. Implementation Details** 

### **A.1. Implementation Details of LaRA-VLA** 

**Training Paradigm.** We adopt the progressive three-stage training paradigm across all experiments. In **Stage I** , the input sequence encompasses explicit Chain-of-Thought (CoT) annotations, <img ~~n~~ ext> tokens for next-frame feature prediction, and action tokens tokenized via fast (Pertsch et al., 2025) tokenizer. In **Stage II** , we facilitate the learning of implicit reasoning by substituting concrete CoT steps with <thinking> tokens. Finally, in **Stage III** , we discard explicit CoT supervision. The specific input formats for each stage are illustrated in Figure 9. 

#### **Stage I: Explicit Supervision** 

’Place the potato inside the bowl. @ Subtask: carry the potato toward the bowl. BBox: [0.5664 0.5898 0.6953 0.6641]. Reasoning: the robot is closing the gripper. <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext>’ 

**Stage II: Mixed Strategy (Transition) One thinking token:** 

’Place the potato inside the bowl. @ <|start ~~o~~ f ~~t~~ hinking|> <|thinking|> <|end ~~o~~ f ~~t~~ hinking|> BBox: [0.5664 0.5898 0.6953 0.6641]. Reasoning: the robot is closing the gripper. <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext>’ **Two thinking tokens:** ’Place the potato inside the bowl. @ <|start ~~o~~ f ~~t~~ hinking|> <|thinking|> <|thinking|> <|end ~~o~~ f ~~t~~ hinking|> Reasoning: the robot is closing the gripper. <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext>’ **Three thinking tokens:** ’Place the potato inside the bowl. @ <|start ~~o~~ f ~~t~~ hinking|> <|thinking|> <|thinking|> <|thinking|> <|end ~~o~~ f ~~t~~ hinking|> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext>’ 

**Stage III: Fully Latent Reasoning** 

’Place the potato inside the bowl. @ <|start ~~o~~ f ~~t~~ hinking|> <|thinking|> <|thinking|> <|thinking|> <|end ~~o~~ f ~~t~~ hinking|> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext> <img ~~n~~ ext>’ 

_Figure 9._ Example of training data formats. 

**Training Config.** Most hyperparameters are shared across evaluation settings, with only a small subset adapted to each scenario. In particular, the action horizon is set to 16 for the Bridge dataset, 8 for the LIBERO benchmark, and 25 for real-world experiments. Detailed hyperparameter configurations for the LIBERO, Bridge, and real-world evaluations are summarized in Table 6. All models are trained using 8 NVIDIA H100 GPUs. 

### **A.2. Implementation Details Baselines in Real-world Experiments** 

**ACT (Zhao et al., 2023).** We instantiate ACT using the LeRobot implementation, configured with a chunk size of _K_ = 50 and _n_ action = 50 action steps per chunk. The perception stack follows the original design, using a ResNet-18 vision backbone pretrained on ImageNet and mean–std normalization for visual, state, and action inputs. The transformer backbone employs a 4-layer encoder and a 1-layer decoder with model dimension 512, 8 attention heads, and a 3200-dimensional feedforward network with ReLU activation and dropout 0.1. Following prior work, we enable the VAE module with a 32-dimensional latent space, 4 encoder layers, and a KL weight of 10.0. Training is performed for 40k gradient steps with batch size 100 on a single H100 GPU, using Adam with learning rate 1 _×_ 10<sup>_−_5</sup> , weight decay 1 _×_ 10<sup>_−_4</sup> , and the same learning rate for the backbone. Note that we adopt the LeRobot fix for the ACT decoder, which uses a single effective decoder layer consistent with the original implementation. 

**GR00T N1.5 (Bjorck et al., 2025).** We use the original GR00T N1.5 implementation with its default architecture and a 

13 

**Latent Reasoning VLA** 

_Table 6._ Hyperparameter settings in LaRA-VLA across LIBERO, SimplerEnv, and real robot experiments. 

|**Herarameters**||**LIBERO**|||**SimplerEnv**|||**Real Robot**||
|---|---|---|---|---|---|---|---|---|---|
|**ypp**|Stage I|Stage II|Stage III|Stage I|Stage II|Stage III|Stage I|Stage II|Stage III|
|_Learning Rates_||||||||||
|VLM LR|1_×_10<sup>_−_5</sup>|1_×_10<sup>_−_5</sup>|1_×_10<sup>_−_5</sup>|1_×_10<sup>_−_5</sup>|1_×_10<sup>_−_5</sup>|1_._3_×_10<sup>_−_5</sup>|1_×_10<sup>_−_5</sup>|1_×_10<sup>_−_5</sup>|1_×_10<sup>_−_5</sup>|
|DiT LR|1_×_10<sup>_−_4</sup>|1_×_10<sup>_−_4</sup>|1_×_10<sup>_−_4</sup>|1_×_10<sup>_−_4</sup>|1_×_10<sup>_−_4</sup>|1_._3_×_10<sup>_−_4</sup>|1_×_10<sup>_−_4</sup>|1_×_10<sup>_−_4</sup>|1_×_10<sup>_−_4</sup>|
|_Optimization Config_||||||||||
|Action Horizon|8|8|8|16|16|16|25|25|25|
|Training Steps|5k|2k/2k/2k|40k|10k|5k/5k/10k|60k|5k|2k/2k/2k|10k|
|Batch Size|12|16|16|12|16|16|12|16|16|
|Optimizer|AdamW|AdamW|AdamW|AdamW|AdamW|AdamW|AdamW|AdamW|AdamW|
|LR Scheduler|Cosine|Cosine|Cosine|Cosine|Cosine|Cosine|Cosine|Cosine|Cosine|
|Warm-up Ratio|0.1|0.1|0.1|0.1|0.1|0.1|0.1|0.1|0.1|
|_Loss Weights_||||||||||
|Action Token Loss|1.0|1.0|–|1.0|1.0|–|1.0|1.0|–|
|Image Next Loss|0.1|0.2|–|0.1|0.2|–|0.1|0.2|–|
|CoT Loss|1.0|1.0|–|1.0|1.0|–|1.0|1.0|–|
|DiT Loss|–|–|1.0|–|–|1.0|–|–|1.0|


continuous-action flow matching head. For real-robot experiments, we train GR00T with an action chunk size of _K_ = 25 and batch size 128 on a single H100 GPU. We follow the recommended optimization hyperparameters, using AdamW with learning rate 1 _×_ 10<sup>_−_4</sup> , weight decay 1 _×_ 10<sup>_−_5</sup> , and a warmup ratio of 0.05 of the total training steps. Consistent with the original setup, we freeze both the language model backbone and the vision tower, and fine-tune only the projector and diffusion policy head. 

**ECoT (Zawalski et al., 2025).** We instantiate an ECoT-style baseline as an ablated variant of LaRA-VLA, retaining explicit textual CoT supervision while removing the action expert, visual CoT, and latent textual CoT components. All other model configurations and training hyperparameters are kept consistent with LaRA-VLA to ensure a fair comparison. 

## **B. Details of Data Pipeline** 

We argue that effective robotic manipulation relies on the organic integration of three tightly coupled components: subtask analysis, spatial grounding of target objects, and directional motion reasoning for the manipulator. Subtask decomposition enables long-horizon reasoning, spatial information localizes task-relevant objects, and motion reasoning translates high-level intent into executable control signals. However, existing data collection pipelines fail to jointly capture these components in a compact and task-centric manner (Zawalski et al., 2025; Sun et al., 2025b; Zhao et al., 2025b). For example, ECoT (Zawalski et al., 2025) annotates bounding boxes for all scene objects, leading to highly redundant supervision, while Emma-x (Sun et al., 2025b) lacks explicit target localization. To address this gap, we construct a fully automated annotation pipeline without human intervention, following an anchor-first, generate-later paradigm driven by semantic and temporal anchors, as shown in Figure 10. 

**Subtask Annotation.** We extract semantic anchors using Qwen3-VL (Bai et al., 2025a) to identify the manipulated object from the first-frame image and the task instruction, which provides a textual reference for subsequent visual grounding. The prompt used for object identification is illustrated in Figure 11 Temporal anchors are obtained by segmenting robot trajectories into atomic manipulation stages (e.g., pre-grasp, grasp, move, and release) based on changes in the gripper state, with segment boundaries treated as keyframes. Conditioned on the instruction and the corresponding keyframes, Qwen3-VL generates high-level subtask descriptions for each segment. The prompt used for Subtask Annotation is illustrated in Figure 12. 

**Target Object Bounding Boxes.** Guided by the semantic anchors, we perform open-vocabulary spatial grounding using GroundingDINO (Liu et al., 2024) and SAM3 (Carion et al., 2025) to obtain temporally consistent 2D bounding box trajectories of the target object. To be noted, for the Bridge dataset, we improve the robustness of our bounding box annotations by employing a multi-frame ensemble approach. We prompt SAM using GroundingDINO detections from 5 uniformly sampled anchor frames. The final trajectory is obtained by filtering spatial outliers and selecting the highest- 

14 

**Latent Reasoning VLA** 


_Figure 10._ Data collection pipline. 

confidence sequence. Furthermore, linear interpolation is applied to address tracking discontinuities, ensuring dense frame-wise supervision. 

**Motion Reasoning.** Motion reasoning is derived from end-effector state trajectories by computing both global motion toward the segment goal and local instantaneous motion. These motion vectors are further mapped to directional descriptors and incorporated into the CoT annotations. 

## **C. Analysis of Real-World Experiments** 

Table 7 provides a subtask-level breakdown of real-world manipulation performance, revealing clear differences in temporal dependency across tasks. For tasks such as Put All Objects into the Basket, Put All Fruits into the Basket, and Stack Two Bowls, the two subtasks are largely decoupled and can be completed independently. This is reflected by the fact that failures in one subtask do not necessarily propagate to the other, and improvements in overall success rate are primarily driven by independent gains in individual subtasks. In contrast, Find the Block and Place It in the Basket exhibits strong sequential dependency between subtasks. Successful completion of the second subtask (placing the block) is contingent on correctly executing the first subtask (finding the block). As a result, errors in the initial subtask directly limit the achievable success rate of the subsequent subtask, leading to a tightly coupled failure mode. This structural dependency explains why improvements on this task require coherent reasoning and action execution across subtasks, rather than isolated subtask-level optimization. Notably, LaRA-VLA demonstrates consistent gains over GR00T N1.5 on this tightly coupled task, suggesting that its latent reasoning mechanism is particularly effective in maintaining cross-subtask coherence. By contrast, for tasks with weak subtask coupling, performance improvements can be largely attributed to better local action execution, and the benefits of reasoning primarily manifest as incremental gains. 

_Table 7._ Subtask-level and overall success rates (%) on real-world robot tasks. 

|**Mthd**|Put All O|bjects into the|Basket|Sort All|Fruits into the|Basket|Find the B|lock and Place I|t in the Baske|t<br>Sta|ck Two Bow|ls|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**eo**|Subtask 1|Subtask 2|Overall|Subtask 1|Subtask 2|Overall|Subtask 1|Subtask 2|Overall|Subtask 1|Subtask 2|Overall|
|ACT|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|
|GR00T N1.5|50.0|50.0|**50.0**|50.0|83.3|33.3|100.0|16.7|16.7|91.7|100.0|91.7|
|LaRA-VLA|50.0|41.7|41.6|66.7|75.0|**50.0**|100.0|33.3|**33.3**|100.0|100.0|**100.0**|


15 

**Latent Reasoning VLA** 

#### ‘‘‘ 

You are helping a robot understand which object to manipulate. You will receive: 

1) A pre-grasp image. 2) The task instruction the robot must follow. Instruction: ‘‘ _{_ instruction _}_ ’’ 

Your goal is to find the SINGLE primary object that the robot must interact with. - Read the instruction carefully to identify the nouns that describe the object(s) to be manipulated. 

- Prioritize what the instruction explicitly requests; ignore other objects unless they are essential context. 

- Ignore objects that the robot does not need to touch. 

- Describe the object with a short noun phrase (preferably including color if visible) but never mention any location context (e.g., no ‘‘on stove’’, ‘‘in pot’’, ‘‘on left’’). 

- The description must be _≤_ 3 words, all lowercase, and purely object attributes. 

- - List any other important objects mentioned in the instruction under secondary ~~o~~ bjects (also _≤_ 3 words, lowercase, no location mentions). 

Output STRICT JSON with the following fields (no comments, no extra text): ‘‘manipulated ~~o~~ bject’’: string describing the main object ( _≤_ 3 words, lowercase, no location). ‘‘secondary ~~o~~ bjects’’: array of strings for other relevant instruction objects (each _≤_ 3 words, lowercase, no location). If you are uncertain or there is no target object, set ‘‘manipulated ~~o~~ bject’’ to the noun mentioned in the instruction and secondary ~~o~~ bjects to an empty array. JSON: 

‘‘‘ 

_Figure 11._ Prompt for object identification. 

## **D. Additional Experiments** 

### **D.1. Additional Analysis** 

**Effect of Action Pretraining.** We further study the effect of action supervision during the pretraining stages. Different from prior latent action methods, where latent actions are learned as intermediate variables to capture motion changes between frames, our latent reasoning variables are not latent actions. All three stages are directly supervised by ground-truth actions: Stages I and II use discrete action tokens to supervise explicit textual CoT and implicit latent textual reasoning, respectively, while Stage III adapts the model to downstream control with continuous action supervision. Table 8 reports an ablation on SimplerEnv, where we fix all other settings and evaluate checkpoints saved every 5k training steps from 35k to 60k. Action pretraining consistently improves performance across all checkpoints, increasing the average success rate from 60 _._ 4% to 64 _._ 2%. This suggests that discrete action supervision during pretraining helps organize the latent reasoning space in a way that is better aligned with the robot’s action space, thereby facilitating later continuous control learning. 

_Table 8._ Effect of action pretraining on SimplerEnv. We compare models with and without discrete action supervision during the pretraining stages, while keeping all other settings fixed. 

|Strategy|35k|40k|45k|50k|55k|60k|Avg.|
|---|---|---|---|---|---|---|---|
|w/o action pretraining|55.2|59.4|64.6|62.5|60.4|60.4|60.4|
|w/ action pretraining|**60.4**|**65.6**|**68.8**|**63.5**|**64.6**|**62.5**|**64.2**|


**Does CoT Supervision Help Without Inference-Time Reasoning?** Prior work, such as ECoT-lite (Chen et al., 2025c), suggests that CoT supervision may improve policy learning even when explicit CoT reasoning is not executed during inference. We therefore examine whether LaRA-VLA also benefits from such implicit reasoning effects. Specifically, we train the model with full latent reasoning supervision, but remove both the latent reasoning tokens and the img ~~n~~ ext token from the prompt during inference, thereby disabling inference-time latent CoT and forcing the policy to directly generate 

16 

**Latent Reasoning VLA** 

‘‘‘ 

You are a robot manipulation expert. 

Your goal is to describe what the robot is doing in this phase of a pick-and-place task. 

Global instruction: ‘‘ _{_ instruction _}_ ’’ Internal segment label (for your reference only): ‘‘ _{_ segment ~~t~~ ype _}_ ’’ 

You are given two keyframes from this phase: one near the beginning and one near the end. 

From the instruction and the images, you must: 

1. Identify the single main object the robot is manipulating. If the object cannot be identified, return ‘‘unknown’’. 

2. Describe where this object is located or how it is situated in the scene (scene ~~c~~ ontext), e.g., ‘‘on the table’’, ‘‘in the basket’’, or ‘‘in the box’’. 

3. Write a short natural-language subtask description for the current action phase, following the rules below: 

   - The subtask MUST be a concrete action phrase (e.g., ‘‘reach toward the blue cup’’, ‘‘carry the spoon toward the bowl’’). 

   - DO NOT simply repeat generic labels such as ‘‘move ~~t~~ o ~~o~~ bject’’, ‘‘move ~~t~~ o ~~g~~ oal’’, ‘‘grasp ~~o~~ bject’’, or ‘‘place ~~o~~ bject’’. 

   - The subtask should explicitly include the object name. If the object cannot be identified, return the subtask as ‘‘manipulate the object’’. 

Return STRICT JSON only (no extra text) with fields: _{_ ‘‘object ~~n~~ ame’’: ‘‘string (e.g., ’blue cup’)’’, ‘‘scene ~~c~~ ontext’’: ‘‘string (e.g., ’inside the metal basket’)’’, ‘‘subtask’’: ‘‘string (natural language, must include the object)’’ _}_ ‘‘‘ 

_Figure 12._ Prompt for subtask description generation. 

### actions without attending to explicit CoT-related tokens. 

Table 9 reports the results on four SimplerEnv tasks. Training with CoT supervision but disabling CoT at inference still improves the average success rate from 55 _._ 2% to 61 _._ 4%, compared with the model trained and evaluated without CoT. This indicates that CoT supervision does not only provide useful intermediate tokens at inference time, but also helps shape the underlying image-instruction representation space during training. Nevertheless, enabling CoT reasoning at inference further improves the average success rate to 68 _._ 7%, showing that explicit latent reasoning remains beneficial beyond the implicit representation-level gains induced by CoT supervision. 

_Table 9._ Effect of CoT supervision and inference-time reasoning on SimplerEnv. We compare models trained with or without CoT supervision and evaluate whether CoT-related tokens are used during inference. Training with CoT supervision improves performance even when CoT tokens are removed at inference time, while using latent reasoning during inference yields the best overall result. 

|**Setting**|**Put Spoon**|**Put Carrot**|**Stack Block**|**Put Eggplant**|**Avg.**|
|---|---|---|---|---|---|
|Train w/o CoT, Infer w/o CoT|79.2|37.5|16.7|87.5|55.2|
|Train w/ CoT, Infer w/o CoT|58.3|87.5|16.7|83.3|61.4|
|Train w/ CoT, Infer w/ CoT|95.8|62.5|25.0|91.7|**68.7**|


**Effect of EMA on Latent Stability.** We further analyze the role of the EMA target encoder in stabilizing latent representation learning. EMA is introduced to provide a slowly evolving target for visual-latent supervision, which can reduce representation drift during the curriculum transition from explicit CoT to latent reasoning. To evaluate its effect, we compare models trained with and without EMA. 

First, we measure the feature-space rank of the <img ~~n~~ ext> latents as an indicator of representation diversity. While we do not observe severe latent collapse without EMA, removing EMA clearly reduces feature diversity: the effective rank 

17 


_Figure 13._ Effect of EMA on latent text token distributions. Without EMA, bounding-box and motion-related latent tokens exhibit stronger overlap, indicating greater semantic entanglement. EMA improves the separation of different reasoning components and stabilizes latent CoT learning. 

decreases from 6 _._ 76 with EMA to 5 _._ 10 without EMA. Second, we visualize the latent text tokens in Figure 13. Without EMA, the latent tokens associated with bounding-box grounding and motion reasoning show stronger overlap, indicating increased semantic entanglement between different reasoning components. In contrast, EMA leads to better separated latent clusters, suggesting that the target encoder helps preserve more structured latent representations. 

These results indicate that EMA is not strictly necessary to avoid immediate collapse, but it improves latent diversity and semantic separation, making latent CoT learning more stable. We therefore treat EMA as a stabilizing training component rather than an independent contribution. 

18 

