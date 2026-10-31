---
title: "E3AD: An Emotion-Aware Vision-Language-Action Model for Human-Centric End-to-End Autonomous Driving"
date: "2025-12-04"
authors: "Yihong Tang; Haicheng Liao; Tong Nie; Junlin He; Ao Qu; Kehua Chen"
venue: "CVPR 2026"
url: https://arxiv.org/abs/2512.04733
pdf: https://arxiv.org/pdf/2512.04733
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2512.04733)** / [論文ページ](https://arxiv.org/abs/2512.04733)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **E3AD: An Emotion-Aware Vision-Language-Action Model for Human-Centric End-to-End Autonomous Driving** 

**Yihong Tang**<sup>1�</sup> , **Haicheng Liao**<sup>2�</sup> , **Tong Nie**<sup>3</sup> , **Junlin He**<sup>3</sup> , **Ao Qu**<sup>4</sup> , **Kehua Chen**<sup>5</sup> , **Wei Ma**<sup>3</sup> , **Zhenning Li**<sup>2�</sup> , **Lijun Sun**<sup>1�</sup> , **Chengzhong Xu**<sup>2�</sup> 

1McGill University 2University of Macau 3The Hong Kong Polytechnic University 4Massachusetts Institute of Technology 

3The Hong Kong Polytechnic University 

5University of Washington 

_{_ yc27979,zhenningli,czxu _}_ @um.edu.mo lijun.sun@mcgill.ca 

yihong.tang@mail.mcgill.ca 

## **Abstract** 

_End-to-end autonomous driving (AD) systems increasingly adopt vision-language-action (VLA) models, yet they ignore the passenger’s emotional state, which is central to comfort and AD acceptance. We introduce OpenDomain End-to-End (OD-E2E) AD, where an autonomous vehicle must interpret free-form natural-language commands, infer the emotion, and plan a physically feasible trajectory. We propose E3AD, an emotion-aware VLA framework that augments semantic understanding with two cognitively inspired components: a continuous ValenceArousal-Dominance (VAD) emotion model that captures tone and urgency from language, and a dual-pathway spatial reasoning module that fuses egocentric and allocentric views for human-like spatial cognition. A consistencyoriented training scheme, combining modality pretraining with preference-based alignment, further enforces coherence between emotional intent and driving actions. Across real-world datasets, E3AD improves visual grounding and waypoint planning and achieves state-of-the-art (SOTA) VAD correlation for emotion estimation. These results show that injecting emotion into VLA-style driving yields more human-aligned grounding, planning, and feedback._ 

## **1. Introduction** 

Autonomous driving (AD) has evolved from modular pipelines to vision-language-action end-to-end (E2E) systems that directly map sensor inputs to vehicle controls through unified optimization. This paradigm significantly improves efficiency and adaptability by integrating perception, prediction, and planning into a single learning framework [5, 29]. Despite these advances, a fundamental obstacle remains that is not purely technical but human-centered: ensuring public trust and acceptance of fully AD [71]. 

> � Equal contribution. � Corresponding Authors. 


Figure 1. Overview of our E3AD. (a) Existing VLAs behave as emotion-agnostic systems, mapping multi-view images directly to a planning output without human-in-the-loop interaction or emotion understanding. (b) Our model adds explicit emotion modeling and closed-loop feedback, allowing the agent to infer intent intensity, ground referents more reliably, and adapt its plan accordingly. (c) This yields the Open-Domain E2E AD task, where the agent jointly reasons over language, emotion, perception, and navigation to enable human-centered and context-aware autonomy. 

While current E2E systems [20, 21, 45] exhibit strong control and perception capabilities, passengers often feel uneasy about delegating decisions to opaque algorithms that operate without acknowledging human intent or emotion. Surveys [68] and behavioral studies [6, 33, 66] consistently indicate that emotional interaction is a critical determinant of user comfort and perceived safety. However, most existing models [27, 43] are designed for closed-loop rational control and remain insensitive to emotion cues such as anxiety or urgency. This disconnection between computational reasoning and emotional understanding forms what can be described as an _emotion gap_ for autonomous vehicles (AVs). Bridging this gap requires reconsidering the role of human-vehicle interaction in AD. An intelligent system should understand “ _what_ ” a passenger says and “ _how_ ” 

10610 

it is expressed. For instance, the tone difference between “stop here” and “stop here now!” carries implicit emotional meaning that influences how the vehicle should respond. Recognizing such differences enables the system to regulate behavior that aligns with the passenger’s emotional state, providing reassurance and enhancing acceptance [23]. 

As illustrated in Fig. 1, we extend the conventional E2E AD framework toward a more human-centric paradigm. Future AVs must reason not only over visual and spatial cues but also interpret and respond to natural-language commands that convey the passenger’s intent and emotional state. We define this capability as the task of **O** pen- **D** omain End-to-End AD ( **OD-E2E** ), where the driving agent jointly reasons over semantic content, emotion context, and spatial environment to generate physically realizable trajectories consistent with the passenger’s instructions. This formulation moves beyond purely reactive control toward interactive, emotion-aware driving assistants that better match human expectations and preferences, transforming AVs into empathetic and user-aligned driving agents [29]. 

Technically, our approach builds on the emerging Vision-Language-Action (VLA) paradigm [50], which unifies perception, reasoning, and control through large-scale multimodal modeling. By coupling visual and linguistic representations, VLA frameworks enable agents to perform complex goal-driven behaviors with improved generalization, interpretability, and alignment to human intent. Following this paradigm, we propose an **E** motion-aware **E** ndto- **E** nd **A** utonomous **D** riving framework, **E3AD** , which extends VLA from purely semantic understanding to emotion and spatially consistent reasoning. To enhance cognitive capability, E3AD incorporates two key components within a unified pipeline: (1) Emotion Modeling, which maps commands into a continuous Valence-Arousal-Dominance (VAD) space [16] to interpret emotional tone and behavioral urgency; and (2) Spatial Reasoning, which fuses egocentric and allocentric pathways to achieve human-like spatial cognition. These components are jointly optimized through a consistency-oriented learning strategy that enforces coherence between the semantic and emotional context of the command and the resulting trajectory. This design enables E3AD to reason jointly over _what_ the passenger intends and _how_ it is expressed, producing emotion-aware and humanaligned driving behaviors in a fully E2E manner. From a safety perspective, modulating behavior according to passenger state decouples request satisfaction from the safety envelope, which is essential for calibrated trust in E2E AD. Overall, the contributions of this study are threefold: 

- We define Open-Domain End-to-End AD for humancentric AVs, which unifies semantic, emotional, and spatial reasoning from natural-language commands. 

- We propose E3AD, an emotion-aware VLA framework that integrates continuous emotion modeling and dual- 

system spatial reasoning in a unified E2E pipeline, enabling emotion-grounded response and planning. 

- We show that E3AD outperforms strong baselines on visual grounding, emotion estimation, and waypoint planning across multiple benchmarks, with particularly large gains on emotion-sensitive and corner-case scenarios. 

## **2. Related Work** 

**VLA for End-to-end AD.** Recent work explores VLA architectures that inject world knowledge and reasoning from large multimodal models into E2E AD [8]. Existing approaches can be broadly grouped into three paradigms [23]. The first paradigm, represented by DriveGPT-4 [61], OpenEMMA [60], and CoT-Drive [32], produces scene-level explanations via QA-style prompts. While improving interpretability, they act as “commentators”, lacking precise spatial grounding and direct control fidelity. The second paradigm, such as Senna [22], VLP [44], and LMDrive [51], employs VLMs to generate discrete “meta-behaviors” to guide a low-level controller. This approach provides only sparse guidance that limits its capacity for continuous spatial reasoning, resulting in marginal gains in driving performance. The third paradigm, like Simlingo [47], AutoVLA [74], and FSDrive [67], couples VLM-based perception with dedicated planning modules that directly output trajectories or control signals, achieving strong performance. However, current VLAs [28, 35, 73] face two core issues: weak spatial understanding, operating largely in 2D without explicit 3D or allocentric (map-based) reasoning [54, 55], and a purely rational sequence-prediction view that ignores passenger emotion, crucial for behavior alignment [53, 56]. Building on the third paradigm, we propose an emotion-aware, spatially grounded end-to-end VLA. **Emotion Computing in AD.** Emotional interaction between humans and AVs offers a promising path to improving public acceptance, safety, and comfort in AD [26]. However, enabling AVs to accurately perceive, interpret, and respond to human emotions remains a fundamental challenge [52]. Early work [7, 42] emphasized driverstate monitoring (fatigue, distraction, stress) via physiological signals (EEG/ECG [4]) and visual cues (facial expressions [59] or gaze tracking); with higher-level AD, the focus shifted to passenger experience (e.g., ride comfort [30, 31], anxiety [25, 58]). Most approaches perform passive detection with discrete labels and decouple emotion estimation from downstream control. We instead ground emotion in the continuous VAD space, integrating it into a unified VLA. To our knowledge, E3AD is the first framework to use a VAD vector to guide: (1) ambiguity resolution for nuanced commands, and (2) the generation of planning trajectories. Through consistency-oriented fine-tuning, E3AD aligns emotion with driving behavior, advancing from emotion recognition to a human-centric AD system [65]. 

10611 


Figure 2. Overview of E3AD and its training/inference pipeline. Given egocentric and allocentric views with a natural-language command (a), E3AD outputs emotion, grounding, and waypoint tokens via two core modules: Emotion Modeling (b) encodes commands in continuous VAD space (c), and Spatial Reasoning fuses egocentric and allocentric pathway cues. Training proceeds from Modality Pretraining for emotion/spatial skills (d) to Joint Fine-Tuning that predicts ( _e_ ˆ,<sup>ˆ</sup> _b_ , _τ_ ˆ) in a single autoregressive chain (e), followed by Emotion-Action Alignment (f). During inference (g), E3AD runs end-to-end to estimate ( _e_ ˆ), ground (<sup>ˆ</sup> _b_ ), and plan ( _τ_ ˆ), producing human-centric feedback. 

## **3. Methodology** 

### **3.1. Problem Formulation** 

We consider OD-E2E AD, where an autonomous vehicle receives multi-view observations and a natural-language command and must execute the command through spatial grounding and motion planning. Let _C_ denote the passenger’s command and _I_ = _{I_ ego _, I_ allo _}_ denote the multi-view observations containing egocentric and allocentric views of the scene. The agent must (i) localize the object or location referenced in _C_ and (ii) generate a physically feasible trajectory that fulfills the instructed intent. Formally, given the tuple ( _I, C_ ), the task aims to learn a mapping: 


where<sup>ˆ</sup> _b_ denotes the grounded target in the scene and _τ_ ˆ = _{yt}_<sup>_T_</sup> _t_ =1<sup>denotesthefuturewaypoints.Unlikepriorlan-</sup> guage grounding setups that restrict command vocabularies and decouple referent localization from motion planning into separate modules, the OD-E2E task learns a single policy _fθ_ that, under a unified objective, jointly predicts (<sup>ˆ</sup> _b,_ ˆ _τ_ ) conditioned on ( _I, C_ ). This elevates language grounding from an auxiliary perception task to an integral component of the end-to-end decision-making objective. 

### **3.2. Overview** 

Fig. 2 illustrates the overall architecture of E3AD, a cognitively inspired VLA system built on Qwen2.5-VL-7BInstruct [1] that integrates Emotion Modeling, Two-System Spatial Representation, and Consistency-Oriented Action Planning in a unified pipeline. To strengthen its cognitive competence, we adopt a three-stage training strategy: (i) Foundational Modality Pretraining to establish emotion and spatial priors, (ii) Joint Reasoning Fine-tuning to optimize 


Figure 3. Visualization of emotion distributions before and after augmentation. (a) Proportions of GoEmotion categories across Talk2Car splits. (b) VAD distribution of GoEmotion. (c) Incorporating driving commands enriches emotional diversity. (d) Emotion-aware augmentation expands and smooths the VAD distribution, providing broader and continuous emotion supervision. 

end-to-end multimodal operation, and (iii) Emotion-Action Alignment to ensure planning behaviors remain consistent with emotional intent. This progressive design provides fine-grained emotion understanding, cognitively grounded spatial reasoning, and behaviorally consistent planning, all aligned with the passenger’s semantic and emotional intent. 

### **3.3. Emotion Modeling** 

Human-vehicle interaction in AD inherently involves emotional communication. Yet, most existing systems are emotion-agnostic and model affect, if at all, with a small set of discrete labels such as happy, angry, or sad [31]. Such coarse encoding cannot capture small but behaviorally meaningful tone changes that influence how a command 

10612 

should be executed. We therefore adopt a continuous representation based on the Valence-Arousal-Dominance (VAD) model [57], representing emotion as _e ∈_ R<sup>3</sup> . Valence measures positivity, arousal measures activation, and dominance measures control; in driving contexts, these axes correspond to attitude (calm vs. anxious), alertness (fatigued vs. vigilant), and control (confident vs. overwhelmed) [40]. 

To supervise this space, we derive VAD labels from both sentence-level and word-level cues. For each command _C_ , we first apply the GoEmotions classifier [10] to obtain a distribution over discrete emotions and map it to sentencelevel VAD scores using the label-VAD dictionary in [57]. In parallel, we compute a word-level VAD vector by removing stop words and averaging lexical scores over the remaining tokens. The final label _e_ is obtained by combining these two sources, so that both global interpretation and emotionbearing phrases are reflected (details in Appendix A.1). 

Driving commands, however, are often emotionally neutral, which would encourage the model to ignore emotion if trained naively. To break this bias and disentangle intent from tone, we introduce emotion-aware command augmentation. For each command _C_<sup>(</sup><sup>_i_)</sup> , Qwen2.5-VL generates _K_ paraphrases _C_ aug<sup>(</sup><sup>_i_)=</sup><sup>_{C_</sup> 1<sup>(</sup><sup>_i_)</sup><sup>_, . . . , C_</sup> _K_<sup>(</sup><sup>_i_)</sup><sup>_}_that preserve the driv-</sup> ing goal while varying the attitude or intensity. Each augmented command _Ck_<sup>(</sup><sup>_i_)</sup> is assigned a VAD label _e_<sup>(</sup> _k_<sup>_i_)</sup> via the same mapping procedure, forming an augmented set _C_<sup>_∗_</sup> that creates neighborhoods of semantically equivalent but affectively distinct commands (Fig. 3). This forces the model to attribute changes in _e_ to changes in tone rather than intent. We then perform supervised fine-tuning (SFT) to equip the VLM with explicit emotion understanding. Given augmented command-emotion pairs _{_ ( _Ck_<sup>(</sup><sup>_i_)</sup><sup>_, e_(</sup> _k_<sup>_i_))</sup><sup>_}⊂C∗_,we</sup> cast emotion prediction as conditional generation with an instruction template (Appendix D) and define the loss as: 


where _pθ_ denotes the model’s distribution over quantized VAD tokens. Rather than adding a separate sentiment head, this continuous, instruction-style formulation embeds _e_ within the same generative reasoning process as other outputs, enabling E3AD to represent fine-grained shifts in affect while keeping the underlying intent fixed, and to condition planning behavior directly on the inferred emotion. 

**Egocentric Pathway.** The egocentric pathway captures the agent’s first-person perceptual field. Using annotated data samples, the model predicts (i) the relative 3D direction to the referent, (ii) its distance, and (iii) its grounded location in image coordinates from ( _I_ ego _, C_ ). These auxiliary signals provide fine-grained, short-horizon spatial cues essential for immediate control. We curate a dataset of 30K samples to establish a robust foundation for egocentric spatial reasoning, which directly supports subsequent planning. **Allocentric Pathway.** The allocentric pathway encodes a world-centered representation akin to a cognitive map. Given BEV input _I_ allo, the model learns to (i) predict the target location in BEV coordinates and (ii) generate a coarse trajectory _τ_ = _{yt}_<sup>_T_</sup> _t_ =1<sup>fromtheegoposetothattar-</sup> get. This supervision yields long-horizon spatial structure, road topology, occlusions, and multi-agent layout, producing map-consistent priors that complement egocentric perception. We use roughly 17K samples to teach this worldcentered reasoning. In combination, the two pathways supply complementary local and global spatial cues that downstream planning modules can exploit for grounding and waypoint generation in cluttered, partially observed scenes. 

### **3.5. Action and Feedback** 

**Action Decoder.** Following the VLA backbone, we append a lightweight action decoder _f_ act for translating the VLA’s high-level outputs into a precise, physically-realizable trajectory _τ_ ˆ. Conditioned on the grounded target<sup>ˆ</sup> _b_ , the coarse trajectory � _τ_ , and visual observations _I_ , the decoder outputs the final trajectory _τ_ ˆ = _f_ act(<sup>ˆ</sup> _b,_ � _τ, I_ ), where _τ_ ˆ _∈_ R<sup>_T ×_2</sup> represents the spatial coordinates of waypoints. 

**Human-centric Verbal Feedback.** To mitigate the “blackbox” anxiety of passengers, E3AD provides verbal feedback ˆ _r_ after planning the waypoints. We employ the trained Qwen2.5-VL backbone to generate this response. Specifically, the model is guided by structured prompts, conditioning the generation of _r_ ˆ on the complete output of the VLA pipeline: the predicted emotion state _e_ ˆ, the grounded target<sup>ˆ</sup> _b_ , and the planned waypoints _τ_ ˆ. The response policy adapts tone, length, and specificity to emotion and urgency: for calm states, it offers brief confirmations, whereas for high arousal, it produces direct, time-critical guidance. This emotion-aware feedback loop transforms the AV from an opaque tool into a human-centric agent. 

### **3.4. Spatial Reasoning** 

Inspired by the dual-system model of human spatial perception [2], we design the VLA backbone to reason over two complementary spatial pathways: an _egocentric_ frame for immediate, action-oriented perception and an _allocentric_ frame for global, map-based structure. This design compels the model to fuse local sensory cues with world-centered priors, mirroring how humans combine first-person observations with internal cognitive maps for reliable navigation. 

### **3.6. Consistency-Oriented Training and Inference** 

We adopt a three-stage consistency-driven training strategy to progressively endow E3AD with emotion awareness, spatial reasoning, and coherent decision-making. The training stages consist of: (1) Modality Pretraining, which establishes foundational representations for spatial and emotional cues; (2) Joint Fine-tuning, unifying emotion grounding, scene understanding, and trajectory planning within a 

10613 

single autoregressive generation process; and (3) EmotionAction Alignment, designed for stable, emotion-consistent driving behaviors. Each training stage is as follows: **Stage-1: Modality Pretraining.** In this initial stage, we apply supervised fine-tuning to equip E3AD with spatial and emotion perception skills separately: (1) Emotion Modeling is trained on our augmented command dataset _C_<sup>_∗_</sup> using the emotion regression loss _L_ emo. (2) Spatial Reasoning is trained on our synthetic egocentric and allocentric pathways using the negative log-likelihood loss _L_ spatial of next-token prediction to optimize spatial reasoning across both views. **Stage-2: Joint Fine-Tuning.** After modality pretraining, we fine-tune the VLA to unify these capabilities into a single, coherent reasoning process. We employ an instructionbased SFT paradigm where the model autoregressively predicts the full output sequence _T_ = (ˆ _e,_<sup>ˆ</sup> _b,_ ˆ _τ_ ) in a single forward pass. This joint objective _L_ joint is defined as follows: 


where _pθ_ is the conditional token distribution. This encourages the VLA to form an emotion-aware chain of thought, where the predicted emotion _e_ ˆ and spatial grounding<sup>ˆ</sup> _b_ directly inform the subsequent generation of waypoints _τ_ ˆ. **Stage-3: Emotion-Action Alignment (DPO).** While _L_ Joint aligns tasks, it does not explicitly enforce behavioral consistency with different emotional intent. Standard preferencebased alignment methods (like DPO) are non-trivial to apply in this field, as AD datasets typically provide only a single, actual trajectory _τ_<sup>(</sup><sup>_i_)</sup> for any given command _C_<sup>(</sup><sup>_i_)</sup> , rather than ranked preference pairs. To address this, we construct a dataset of _pseudo-preference pairs_ via emotionaugmented commands. For each original command _C_<sup>(</sup><sup>_i_)</sup> and its actual trajectory _τ_<sup>(</sup><sup>_i_)</sup> , we identify an emotionaugmented variant _Ck_<sup>(</sup><sup>_i−_)whoseVADembeddingdeviates</sup> most from the original. We use this “negative” command to generate a dispreferred, emotion-shifted trajectory � _τk_<sup>(</sup><sup>_i−_):</sup> _Ck_<sup>(</sup><sup>_i−_)= arg max</sup> _k ∥e_<sup>(</sup> _k_<sup>_i_)</sup><sup>_−e_(</sup><sup>_i_)</sup><sup>_∥_2</sup><sup>_,_�</sup><sup>_τ_(</sup> _k_<sup>_i−_)</sup><sup>_∼pθ_(</sup><sup>_τ| C_</sup> _k_<sup>(</sup><sup>_i−_)</sup><sup>_, I_(</sup><sup>_i_))</sup><sup>_,_</sup> (4) This yields a preference pair ( _τ_<sup>(</sup><sup>_i_)</sup> _≻ τ_ � _k_<sup>(</sup><sup>_i−_)) for the command</sup> _C_<sup>(</sup><sup>_i_)</sup> . We apply DPO [46] to optimize this preference: 


Notably, this stage encourages the model to assign higher likelihood to trajectories consistent with the original command’s intent while suppressing emotionally perturbed alternatives, leading to stable yet emotion-aware behavior. **Inference.** After the VLA backbone is trained, its outputs are integrated into a lightweight action decoder for precise trajectory waypoint generation. During inference, E3AD operates end-to-end: it seamlessly processes the input tuple ( _I_ ego _, I_ allo _, C_ ) to directly produce the emotion state _e_ ˆ, the 

grounded target<sup>ˆ</sup> _b_ , coarse trajectory waypoints _τ_ ˆ, and the verbal response _r_ ˆ for passengers. This integrated process enables emotion-grounded visual grounding and humanaligned planning without additional post-processing. 

## **4. Experiments** 

**Datasets.** This study conducts experiments on several challenging real-world benchmarks, including Talk2Car [17], DrivePilot [34], MoCAD [31], and Talk2Car-Trajectory [14]. To further assess model robustness, we follow the ThinkDeeper protocol [34] and introduce refined data splits for the DrivePilot and MoCAD, resulting in two tailored subsets: Long-Text and Corner-Case, each presenting distinct challenges. 

**Evaluation Metrics.** We evaluate models along two axes: (1) joint end-to-end performance and (2) sub-task ablations. For end-to-end evaluation, we report trajectory metrics, including ADE, FDE, Fr´echet, DTW, SSPD, and planning accuracy within _g_ meters (PA _g_ ). For sub-task evaluation, we follow the Talk2Car C4AV protocol [13] and report IoU for visual grounding; MAE and IoU for spatial reasoning; and Spearman’s ( _ρ_ ) and Kendall’s ( _τ_ ) for emotion awareness. **Implementation Details.** We train E3AD using the MSSwift library [72] with LoRA fine-tuning [19] (rank 16, scaling factor 32), a constant learning rate of 10<sup>_−_4</sup> , and a per-device batch size of 16 for one epoch over the full dataset. Training is conducted in two stages: (i) modality pretraining and unified fine-tuning to adapt the backbone to domain data, and (ii) behavioral alignment via DPO to refine responses toward the desired driving behavior. All experiments are run on 8 _×_ NVIDIA H200 GPUs. To ensure a fair comparison, we freeze the Qwen2.5-VL-7B backbone and train only low-rank adapters, keeping the trainable parameter budget comparable to or smaller than the baselines. The gains in Tables 1-2 thus mainly stem from the proposed emotion modeling, dual-path spatial reasoning, and consistency-oriented training rather than model size. Larger generic VLMs (Qwen2.5-VL-72B, Qwen3-VL-8B) still underperform E3AD, indicating that task-aligned structure and objectives matter more than raw capacity. 

### **4.1. Joint Evaluation Results** 

Table 1 reports the end-to-end performance of E3AD and SOTA baselines under unified evaluation settings. In our formulation, emotion perception, spatial understanding, and visual grounding jointly provide intermediate evidence for downstream planning, simulating a more realistic AD pipeline that couples perception, cognition, and action. The results clearly show that E3AD outperforms all baselines across seven standard trajectory metrics. Compared with the strongest baseline (PTPC), our model achieves notable gains of 17.01%, 18.26%, and 20.00% reductions in ADE, Fr´echet, and FDE, respectively, indicating more ac- 

10614 

Table 1. End-to-end performance of E3AD vs. state-of-the-art (SOTA) baselines. Best results are **bold** ; second-best are underlined. 

|**Model**|**ADE** _↓_|**Fr´echet** _↓_|**SSPD** _↓_|**DTW** _↓_|**FDE** _↓_|**PA2** _↑_|**PA4** _↑_|
|---|---|---|---|---|---|---|---|
|_A_<sup>_∗_</sup>-ROL [18]|5_._63_±_0_._12|10_._22_±_0_._20|3_._06_±_0_._06|93_._35_±_1_._80|9_._34_±_0_._18|5_._45_±_1_._38|25_._13_±_2_._63|
|_A_<sup>_∗_</sup>-PE (PDPC) [18]|5_._35_±_0_._13|9_._38_±_0_._22|2_._80_±_0_._07|86_._78_±_2_._28|8_._22_±_0_._21|25_._95_±_2_._66|46_._41_±_3_._03|
|GoalGAN [11]|5_._89_±_0_._12|10_._86_±_0_._21|3_._09_±_0_._06|98_._75_±_2_._11|10_._08_±_0_._20|17_._32_±_2_._30|33_._82_±_2_._87|
|PECNet [70]|4_._78_±_0_._10|8_._84_±_0_._19|2_._54_±_0_._05|76_._87_±_1_._75|8_._22_±_0_._17|15_._59_±_2_._20|37_._68_±_2_._94|
|Y-net [39]|5_._28_±_0_._10|10_._01_±_0_._19|2_._50_±_0_._04|85_._25_±_1_._69|8_._98_±_0_._18|2_._49_±_0_._94|30_._84_±_2_._81|
|TTST [39]|5_._24_±_0_._10|9_._79_±_0_._19|2_._47_±_0_._04|84_._02_±_1_._68|8_._50_±_0_._18|13_._98_±_2_._11|37_._54_±_2_._94|
|CWS [39]|4_._82_±_0_._11|9_._30_±_0_._20|2_._46_±_0_._05|78_._69_±_1_._84|8_._59_±_0_._18|3_._27_±_1_._08|34_._66_±_2_._89|
|TTST + CWS [39]|4_._76_±_0_._10|8_._95_±_0_._19|2_._41_±_0_._05|76_._84_±_1_._77|8_._08_±_0_._17|17_._54_±_2_._31|40_._79_±_2_._96|
|PTPC [17]|4_._54_±_0_._11|8_._55_±_0_._20|2_._18_±_0_._05|72_._09_±_1_._86|7_._75_±_0_._19|24_._46_±_2_._61|45_._55_±_3_._03|
|Qwen2.5-VL-72B [1]|12_._51_±_0_._28|26_._15_±_0_._52|5_._87_±_0_._14|206_._99_±_4_._80|25_._85_±_0_._55|1_._18_±_0_._42|3_._13_±_0_._60|
|Qwen3-VL-8B [63]|14_._07_±_0_._30|28_._38_±_0_._58|6_._65_±_0_._16|234_._81_±_5_._20|27_._96_±_0_._60|1_._89_±_0_._50|4_._50_±_0_._70|
|FSDrive-Finetuned [67]|5_._02_±_0_._12|10_._98_±_0_._24|2_._28_±_0_._06|74_._50_±_2_._10|10_._45_±_0_._22|17_._10_±_2_._40|27_._85_±_2_._80|
|CAVG(+Planner)[31]|4_._88_±_0_._14|9_._23_±_0_._20|2_._20_±_0_._04|73_._51_±_1_._42|9_._23_±_0_._28|20_._10_±_2_._45|43_._25_±_2_._63|
|**E3AD (Ours)**|**3.88**_±_**0.10**|**7.23**_±_**0.19**|**1.86**_±_**0.05**|**60.07**_±_**1.69**|**6.64**_±_**0.18**|**36.21**_±_**0.94**|**55.62**_±_**0.95**|
||**17.01%** _↑_|**18.26%** _↑_|**17.20%** _↑_|**16.67%** _↑_|**20.00%** _↑_|**16.71%** _↑_|**18.10%** _↑_|


Table 2. Comparison of E3AD and state-of-the-art baselines on visual grounding tasks. Best results are **bold** ; second-best are underlined. 

|**Model**|**Backbone**|**Talk2Car**|**MoC**|**AD**|**Drive**|**Pilot**|**Corn**|**er-case Test se**|**ts**|**Long-text**|
|---|---|---|---|---|---|---|---|---|---|---|
||||**test**|**val**|**test**|**val**|**Visual Constr.**|**Multi-agent**|**Ambiguous**|**val**|
|AttnGrounder [41]|ResNet-50|61.32|62.34|64.35|62.31|64.57|62.74|64.82|64.31|57.25|
|CMSVG [48]|EfficientNet|68.61|67.66|68.47|68.87|69.93|69.39|66.77|67.83|62.21|
|TransVG [12]|ResNet-101|65.83|68.14|70.85|66.52|68.42|68.12|66.34|69.25|65.45|
|CMRT [38]|ResNet-152|69.11|69.42|68.83|69.54|70.37|67.12|66.20|62.23|64.25|
|MDERT [24]|ResNet-101|70.52|66.74|70.23|71.35|72.15|68.35|65.37|68.38|62.72|
|VL-BERT [9]|ResNet-101|70.03|71.42|70.54|71.47|72.36|70.29|70.14|69.84|66.70|
|RSD-LXMERT [3]|ResNet-101|72.64|72.35|71.46|73.37|74.52|70.22|71.87|63.44|65.80|
|VLTVG [64]|ResNet-101|63.33|67.14|68.26|65.37|68.49|68.51|66.22|70.24|68.80|
|Grounding-DINO [36]|ViT|68.15|67.92|68.48|69.50|70.10|66.17|65.85|67.24|63.15|
|UNINEXT [62]|ResNet-50|70.87|70.62|71.34|71.35|73.47|69.26|68.78|71.29|65.32|
|CAVG [31]|ViT|74.62|72.44|73.25|75.52|76.48|68.39|67.36|69.45|64.36|
|Qwen2.5-VL-7B [1]|VLM|47.31|48.20|49.10|50.06|50.84|45.12|46.37|47.05|41.92|
|Qwen2.5-VL-72B [1]|VLM|56.17|57.10|57.85|58.92|59.74|53.43|54.25|55.17|49.83|
|Qwen3-VL-8B [63]|VLM|56.19|57.25|58.16|59.05|59.85|53.55|54.49|55.25|50.13|
|**E3AD (O)**|VLM|**80.12**|**80.94**|**79.64**|**81.02**|**82.56**|**76.62**|**77.24**|**77.05**|**77.86**|
|**urs**|–|**6.86%** _↑_|**10.50%** _↑_|**8.72%** _↑_|**6.79%** _↑_|**7.36%** _↑_|**8.26%** _↑_|**6.95%** _↑_|**7.48%** _↑_|**11.63%** _↑_|


curate and stable trajectory forecasting. Likewise, E3AD improves SSPD and DTW by over 16%, reflecting better temporal smoothness and spatial coherence in path generation. In planning accuracy, E3AD improves PA2/PA4 by +16.71%/+18.10%, indicating tighter alignment between plans and driving goals. General-purpose VLMs (QwenVL) still struggle, and FSDrive-Finetuned trails markedly, with higher FDE (10.45 vs. 6.64), confirming the limitations of existing VLA models in handling command-driven scenarios. Overall, E3AD’s stronger fusion of command semantics, spatial context, and emotion yields more reliable and command-aligned waypoint planning. 

### **4.2. Sub-task Evaluation Results** 

We report the performance of E3AD on key sub-tasks against SOTA methods. Notably, our model addresses all tasks concurrently within one end-to-end trained network, whereas other baselines are specialized for only one task. **Visual Grounding.** Table 2 reports visual grounding results. E3AD surpasses the strongest baseline (CAVG) with absolute gains of +6.86% (Talk2Car), +10.50% / +8.72% (MoCAD test/val), and +6.79% / +7.36% (DrivePi- 

lot test/val). This superiority is especially pronounced in challenging scenes. On corner-case splits (occluded, multiagent, ambiguous), it improves by +8.26%, +6.95%, and +7.48%, and on Long-text by +11.63%. Generic VLMs (Qwen) lag markedly across all datasets. These results indicate our emotion- and spatial-aware grounding yields more precise and robust localization within a unified E2E model. 

**Spatial Reasoning.** Table 4 illustrates that E3AD markedly outperforms large VLM baselines (Qwen2.5/3-VL) on target localization and depth estimation. While even VLMs like Qwen2.5-VL-72B struggle with basic spatial reasoning (Location MAE 10.1, Depth MAE 22.68), E3AD demonstrates a precise, grounded understanding with an MAE of only 0.47 (Location) and 4.25 (Depth), respectively. This superiority is consistent in accuracy metrics, where E3AD achieves 97.7% PA2 (Location) and 53.1% PA2 (Depth), far above the best VLM. These results demonstrate that E3AD establishes a new state-of-the-art in 3D spatial perception and localization, significantly outperforming conventional visual-spatial VLMs in real-world driving scenarios. **Emotion Recognition.** Table 3 presents emotion recognition results across valence, arousal, and dominance dimen- 

10615 

Table 3. Emotion prediction across valence, arousal, and dominance. Reported metrics are Spearman’s _ρ_ and Kendall’s _τ_ correlations with ground-truth VAD ( _↑_ : a higher value is better). 

|**Model**||**Vale**|**nce**_↑_|**Arou**|**sal**_↑_|**Domin**|**ance**_↑_|
|---|---|---|---|---|---|---|---|
|||_ρ_|_τ_|_ρ_|_τ_|_ρ_|_τ_|
|BERT [15] + Ridge||0.78|0.59|0.75|0.56|0.74|0.55|
|RoBERTa [37] + Ridg|e|0.80|0.61|0.77|0.59|0.78|0.58|
|DistilBERT [49] + Ri|dge|0.82|0.64|0.79|0.61|0.79|0.60|
|Qwen2.5-7B-Instruct|[1]|0.11|0.08|0.02|0.02|0.04|0.03|
|Qwen3-Emb.-4B [69]|+ Ridge|0.83|0.64|0.79|0.61|0.82|0.63|
|**E3AD (ours)**||**0.95**|**0.84**|**0.94**|**0.82**|**0.94**|**0.81**|
|able 4. Spatial rea<br>**Model**|soning r<br>**T2C**|esults<br>**Targ**|on Tal<br>**et Loc. **|k2Car<br>**Est.**|vs. V<br>**Targ**|LM ba<br>**et Depth**|seline<br>**Est.**|
||IoU50|MAE _↓_|PA2|PA4|MAE|_↓_<br>PA2|PA4|
|Qwen2.5-VL-7B [1]|40.23|3.49|39.5|71.1|22.92|1.3|4.2|
|Qwen2.5-VL-72B [1]|51.42|10.1|38.5|77.9|22.68|1.5|4.5|
|Qwen3-VL-8B [63]|52.68|3.71|32.8|71.5|18.89|13.7|26.5|
|**E3AD (Ours)**|**79.32**|**0.47**|**97.7**|**98.8**|**4.25**|**53.1**|**71.2**|


Table 4. Spatial reasoning results on Talk2Car vs. VLM baselines. 

sions. Since VAD represents relative emotional magnitudes, we adopt Spearman’s rank correlation ( _ρ_ ) and Kendall’s rank correlation coefficient ( _τ_ ) as evaluation metrics to assess the monotonic relationship between model predictions and labels. The _Ridge_ regressor obtains command embeddings from language models and applies ridge regression to predict continuous VAD values, serving as a lightweight emotion estimator. E3AD achieves the highest correlation with human annotations, reaching 0.95/0.84 ( _ρ_ , _τ_ ) for valence, 0.94/0.82 for arousal, and 0.94/0.81 for dominance. In contrast, Qwen2.5-7B and Qwen3-4B exhibit near-random correlation levels, revealing limited sensitivity to emotion cues. These results show that E3AD effectively models the continuous emotion space of human emotions, capturing valence (positive-negative sentiment), arousal (intensity), and dominance (sense of control), enabling humancentric planning and verbal feedback for passengers. 

### **4.3. Ablation Study** 

Table 5 summarizes module contributions. Removing the egocentric pathway causes the largest VG drop ( _↓_ 7.0% IoU on Talk2Car; _↓_ 6.6% on Vision-Constraint), confirming its role in first-person grounding that aligns linguistic references with observed targets. Excluding the allocentric map weakens global reasoning by removing complementary spatial semantics and scene topology. The Emotion Modeling shows the greatest benefit on ambiguous and long-text commands ( _↑_ 4.5%/ _↑_ 4.8%), enhancing the model’s sensitivity to nuanced linguistic cues and emotionally rich expressions. DPO gives moderate gains by refining multimodal alignment. For waypoint planning (Table 6), the allocentric map is critical: removal degrades trajectories (ADE/FDE ( _↑_ 10.0%/ _↑_ 10.1%)), indicating the value of global priors for spatial awareness and route consistency. The egocentric pathway anchors local motion cues; Emotion Modeling and DPO further improve emotion consistency. 

As in Fig. 4, DPO raises Spearman correlations for 

Table 5. Ablation study of E3AD’s core components on visual grounding performance on the Talk2Car (T2C) benchmark, vision constraint (Constr.), ambiguous (Ambg.), and long-context command (Long) test sets. Components: Egocentric pathway (Ego.), Allocentric pathway (Allo.), DPO, and Emotion Modeling (Emo.). 

|**Ego.**|**Allo.**|**Emo.**|**DPO**|**T2C** _↑_|**Constr.** _↑_|**Ambg.** _↑_|**Long** _↑_|
|---|---|---|---|---|---|---|---|
|✗|✓|✓|✓|74.48|71.60|72.24|72.47|
|✓|✗|✓|✓|76.48|73.92|74.65|74.76|
|✓|✓|✗|✓|78.78|74.41|73.57|74.12|
|✓|✓|✓|✗|79.55|75.58|**77.09**|76.44|
|✓|✓|✓|✓|**80.12**|**76.62**|77.05|**77.86**|
|Table 6.|Ablat|ion of|core de|signs in|E3AD on|waypoint|planning.|
|**Ego.**|**Allo.**|**Emo.**|**DPO**|**ADE** _↓_|**SSPD** _↓_|**Fr´echet** _↓_|**FDE** _↓_|
|✗|✓|✓|✓|4.12|2.06|7.61|7.02|
|✓|✗|✓|✓|4.27|2.15|7.86|7.31|
|✓|✓|✗|✓|3.93|1.91|7.36|6.80|
|✓|✓|✓|✗|3.96|1.89|7.31|6.86|
|✓|✓|✓|✓|**3.88**|**1.86**|**7.23**|**6.64**|


Figure 4. DPO’s effect on emotion-trajectory consistency. 

straightness/sinuosity and stabilizes turn smoothness and angular variation, yielding geometrically coherent, behaviorally consistent paths. Higher arousal corresponds to straighter, smoother motion; lower arousal to more cautious, curved motion. Overall, DPO strengthens emotiontrajectory consistency even when numeric gains are modest. 

### **4.4. Case Study** 

Fig. 6 illustrates how E3AD integrates emotion understanding with spatial reasoning to produce end-to-end behavior. The VAD plot showcases that the Emotion Modeling component captures the linguistic shift from a neutral command to its cautious variant: the neutral command maps to (0 _._ 60 _,_ 0 _._ 39 _,_ 0 _._ 45), while adding the qualifier “Be more cautious” shifts the VAD state to (0 _._ 60 _,_ 0 _._ 49 _,_ 0 _._ 51), increasing Arousal and Dominance. Conditioned on the neutral VAD, E3AD plans a standard lane-change maneuver; conditioned on the cautious VAD, the DPO-aligned policy instead avoids the lane change altogether. The generated textual feedback is also conditioned on emotion state _e_ ˆ: the EmoThink block infers a cautious, slightly anxious passenger and produces a reassuring explanation. Taken together with the geometric statistics in Fig. 4, these results indicate that emotion supervision affects not only language but also motion geometry. At fixed intent, higher arousal steers E3AD toward straighter paths with less lateral oscillation and earlier hazard avoidance, while lower arousal produces slower approaches with larger safety margins. Thus, the 

10616 


Figure 5. Qualitative comparison between E3AD and FSDrive-FT in emotion-rich (a), multi-agent (b), and ambiguous (c) scenes. 


Figure 6. Case study for the impact of different emotional commands (neutral vs. cautious) on E3AD’s end-to-end performance. 

VAD vector serves as a continuous control signal that selects among behaviorally distinct yet physically valid plans, rather than as a binary switch or style token. 

### **4.5. Qualitative Analysis** 

Fig. 5 showcases qualitative comparisons between E3AD and FSDrive-FT [67] across three challenging scenes. In the emotion-rich command scene (Panel (a)), E3AD leverages its continuous VAD-based emotion modeling to infer the passenger’s heightened urgency and produces a timely lane-change response. In contrast, the variant without emotion modeling hesitates and reacts too late. In the multiagent scene (Panel (b)), where objects are partially occluded and visual cues are ambiguous, E3AD integrates allocentric topology with egocentric evidence through spatial reasoning, enabling accurate target grounding and a safe, well-aligned trajectory. FSDrive-FT fails to parse the complex scene structure, resulting in off-target grounding and unsafe plans. In the ambiguous command scene (panel (c)), E3AD resolves linguistic ambiguity by combining language tone with spatial context, producing a feasible, mapconsistent parking path. In contrast, FSDrive-FT crosses map boundaries into non-drivable regions. Overall, this illustrates how emotion-aware language understanding and dual-frame spatial reasoning enable E3AD to deliver more interpretable and human-aligned grounding and planning. See Appendix C for more qualitative results of E3AD. 


Figure 7. User study on perceived compliance, emotion, safety, and preference. (Left) E3AD consistently achieves high Likert scores across all age groups. (Right) Comparison of Rank-1 votes, E3AD dominates in most dimensions, outperforming all baselines. 

### **4.6. User Study** 

To evaluate the real-world utility of E3AD, we conduct a user study with 217 participants. Participants viewed anonymized clips from five systems and ranked them on Command Compliance, Emotion Alignment, Safety, Comfort, and Overall Preference. As shown in Fig. 7, E3AD obtains the highest mean scores and most Rank-1 votes on most dimensions, indicating a clear preference over the baselines. Beyond absolute scores, participants consistently prefer trajectories that match the command’s emotional tone, maintain correct grounding, and stay physically feasible. Systems without emotion modeling (FSDrive-FT, generic VLMs) are often seen as hesitant or unsafe, whereas E3AD’s emotion-aware grounding and map-feasible planning are judged more confident and trustworthy, highlighting the value of emotion cues in the end-to-end AD. 

## **5. Conclusion and Future Work** 

This work extends E2E AD from purely rational control to emotion-aware grounding and planning. We introduce OD-E2E AD and propose E3AD, a VLA framework that couples continuous VAD-based emotion modeling, dualpathway spatial reasoning, and consistency-oriented training. Experiments on four real-world benchmarks show consistent improvements in visual grounding, trajectory quality, and continuous emotion estimation over strong baselines. In future work, we plan to incorporate more human preference feedback, richer multimodal emotion signals beyond language, and closed-loop evaluation in high-fidelity simulators to further enhance the reliability and acceptance of emotion-aware autonomous driving systems. 

10617 

## **Acknowledgements** 

This work was supported in part by the Natural Sciences and Engineering Research Council (NSERC) of Canada, and part by the Research Services and Knowledge Transfer Office, University of Macau [SRG2023-00037-IOTSC, MYRG-GRG2024-00284-IOTSC], in part by the State Key Lab of Intelligent Transportation System [2024-B001]. 

## **References** 

- [1] Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, et al. Qwen2.5-vl technical report. _arXiv preprint arXiv:2502.13923_ , 2025. 3, 6, 7 

- [2] Neil Burgess. Spatial memory: how egocentric and allocentric combine. _Trends in cognitive sciences_ , 10(12):551–557, 2006. 4 

- [3] Hou Pong Chan, Mingxi Guo, and Cheng-Zhong Xu. Grounding commands for autonomous vehicles via layer fusion with region-specific dynamic layer attention. In _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 12464–12470. IEEE, 2022. 6 

- [4] Jielin Chen, Xuefen Lin, Weifeng Ma, Yuchen Wang, and Wei Tang. Eeg-based emotion recognition for road accidents in a simulated driving environment. _Biomedical signal processing and control_ , 87:105411, 2024. 2 

- [5] Li Chen, Penghao Wu, Kashyap Chitta, Bernhard Jaeger, Andreas Geiger, and Hongyang Li. End-to-end autonomous driving: Challenges and frontiers. _IEEE TPAMI_ , 46(12): 10164–10183, 2024. 1 

- [6] Xingtong Chen, Xia Wang, Cong Fang, Le Fang, et al. Emotion-aware design in automobiles: Embracing technology advancements to enhance human-vehicle interaction. In _Proceedings of the 2025 CHI Conference on Human Factors in Computing Systems_ , pages 1–18, 2025. 1 

- [7] Roddy Cowie, Ellen Douglas-Cowie, et al. Emotion recognition in human-computer interaction. _IEEE Signal processing magazine_ , 18(1):32–80, 2001. 2 

- [8] Can Cui, Yunsheng Ma, Xu Cao, Wenqian Ye, Yang Zhou, Kaizhao Liang, Jintai Chen, Juanwu Lu, Zichong Yang, Kuei-Da Liao, et al. A survey on multimodal large language models for autonomous driving. In _Proceedings of the IEEE/CVF WACV_ , pages 958–979, 2024. 2 

- [9] Hang Dai, Shujie Luo, Yong Ding, and Ling Shao. Commands for autonomous vehicles by progressively stacking visual-linguistic representations. In _ECCV_ , pages 27–32. Springer, 2020. 6 

- [10] Dorottya Demszky, Dana Movshovitz-Attias, Jeongwoo Ko, Alan Cowen, Gaurav Nemade, and Sujith Ravi. Goemotions: A dataset of fine-grained emotions. In _Proceedings of the 58th annual meeting of the association for computational linguistics_ , pages 4040–4054, 2020. 4 

- [11] Patrick Dendorfer, Aljosa Osep, and Laura Leal-Taix´e. Goalgan: Multimodal trajectory prediction based on goal position estimation. In _Proceedings of the Asian Conference on Computer Vision_ , 2020. 6 

- [12] Jiajun Deng, Zhengyuan Yang, Tianlang Chen, Wengang Zhou, and Houqiang Li. Transvg: End-to-end visual grounding with transformers. In _Proceedings of the IEEE/CVF ICCV_ , pages 1769–1779, 2021. 6 

- [13] Thierry Deruyttere, Simon Vandenhende, Dusan Grujicic, Luc Van Gool, and Marie Francine Moens. Talk2car: Taking control of your self-driving car. In _Proceedings of the 2019 conference on empirical methods in natural language processing and the 9th international joint conference on natural language processing (EMNLP-IJCNLP)_ , pages 2088–2098, 2019. 5 

- [14] Thierry Deruyttere, Dusan Grujicic, Matthew B Blaschko, and Marie-Francine Moens. Talk2car: Predicting physical trajectories for natural language commands. _IEEE Access_ , 10:123809–123834, 2022. 5 

- [15] Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. Bert: Pre-training of deep bidirectional transformers for language understanding. In _Proceedings of the 2019 conference of the North American chapter of the association for computational linguistics: human language technologies, volume 1 (long and short papers)_ , pages 4171– 4186, 2019. 7 

- [16] Marvin Gaertner, Daniel Sauter, Hermann Baumgartl, Thilo Rieg, and Ricardo Buettner. Multi-class emotion recognition within the valence-arousal-dominance space using eeg. In _AMCIS_ , 2021. 2 

- [17] Dusan Grujicic, Thierry Deruyttere, Marie-Francine Moens, and Matthew B Blaschko. Predicting physical world destinations for commands given to self-driving cars. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , pages 715–725, 2022. 5, 6 

- [18] Peter E Hart, Nils J Nilsson, and Bertram Raphael. A formal basis for the heuristic determination of minimum cost paths. _IEEE transactions on Systems Science and Cybernetics_ , 4 (2):100–107, 1968. 6 

- [19] Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan AllenZhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. Lora: Low-rank adaptation of large language models. In _ICLR_ , 2022. 5 

- [20] Yihan Hu, Jiazhi Yang, Li Chen, Keyu Li, Chonghao Sima, Xizhou Zhu, Siqi Chai, Senyao Du, Tianwei Lin, Wenhai Wang, et al. Planning-oriented autonomous driving. In _Proceedings of the IEEE/CVF CVPR_ , pages 17853–17862, 2023. 1 

- [21] Xiaosong Jia, Penghao Wu, Li Chen, Jiangwei Xie, Conghui He, Junchi Yan, and Hongyang Li. Think twice before driving: Towards scalable decoders for end-to-end autonomous driving. In _Proceedings of the IEEE/CVF CVPR_ , pages 21983–21994, 2023. 1 

- [22] Bo Jiang, Shaoyu Chen, Bencheng Liao, Xingyu Zhang, Wei Yin, Qian Zhang, Chang Huang, Wenyu Liu, and Xinggang Wang. Senna: Bridging large vision-language models and end-to-end autonomous driving. _arXiv preprint arXiv:2410.22313_ , 2024. 2 

- [23] Sicong Jiang, Zilin Huang, Kangan Qian, Ziang Luo, Tianze Zhu, Yang Zhong, Yihong Tang, Menglin Kong, Yunlong Wang, Siwen Jiao, et al. A survey on vision-language- 

10618 

action models for autonomous driving. In _Proceedings of the IEEE/CVF ICCV_ , pages 4524–4536, 2025. 2 

- [24] Aishwarya Kamath, Mannat Singh, Yann LeCun, Gabriel Synnaeve, Ishan Misra, and Nicolas Carion. Mdetrmodulated detection for end-to-end multi-modal understanding. In _Proceedings of the IEEE/CVF ICCV_ , pages 1780– 1790, 2021. 6 

- [25] Seungji Lee, Taejun Lee, Taeyang Yang, Changrak Yoon, and Sung-Phil Kim. Detection of drivers’ anxiety invoked by driving situations using multimodal biosignals. _Processes_ , 8 (2):155, 2020. 2 

- [26] Wenbo Li, Guofa Li, Ruichen Tan, Cong Wang, Zemin Sun, Ying Li, Gang Guo, Dongpu Cao, and Keqiang Li. Review and perspectives on human emotion for connected automated vehicles. _Automotive Innovation_ , 7(1):4–44, 2024. 2 

- [27] Yingyan Li, Shuyao Shang, Weisong Liu, Bing Zhan, Haochen Wang, Yuqi Wang, Yuntao Chen, Xiaoman Wang, Yasong An, Chufeng Tang, et al. Drivevla-w0: World models amplify data scaling law in autonomous driving. _arXiv preprint arXiv:2510.12796_ , 2025. 1 

- [28] Yue Li, Meng Tian, Zhenyu Lin, Jiangtong Zhu, Dechang Zhu, Haiqiang Liu, Yueyi Zhang, Zhiwei Xiong, and Xinhai Zhao. Fine-grained evaluation of large vision-language models in autonomous driving. In _Proceedings of the IEEE/CVF ICCV_ , pages 9431–9442, 2025. 2 

- [29] Zhenning Li, Zhiyong Cui, Haicheng Liao, John Ash, Guohui Zhang, Chengzhong Xu, and Yinhai Wang. Steering the future: Redefining intelligent transportation systems with foundation models. _Chain_ , 1(1):46–53, 2024. 1, 2 

- [30] Yuheng Liang, Zheyu Wang, Feng Liu, Mingzhou Liu, and Yu Yao. Mamba-va: A mamba-based approach for continuous emotion recognition in valence-arousal space. In _Proceedings of the CVPR_ , pages 5651–5656, 2025. 2 

- [31] Haicheng Liao, Huanming Shen, Zhenning Li, Chengyue Wang, Guofa Li, Yiming Bie, and Chengzhong Xu. Gpt4 enhanced multimodal grounding for autonomous driving: Leveraging cross-modal attention with large language models. _Communications in Transportation Research_ , 4:100116, 2024. 2, 3, 5, 6 

- [32] Haicheng Liao, Hanlin Kong, Bonan Wang, Chengyue Wang, Wang Ye, Zhengbing He, Chengzhong Xu, and Zhenning Li. Cot-drive: Efficient motion forecasting for autonomous driving with llms and chain-of-thought prompting. _IEEE Transactions on Artificial Intelligence_ , 2025. 2 

- [33] Haicheng Liao, Zhenning Li, Guohui Zhang, Keqiang Li, and Chengzhong Xu. Toward human-like trajectory prediction for autonomous driving: A behavior-centric approach. _Transportation Science_ , 2025. 1 

- [34] Haicheng Liao, Huanming Shen, Bonan Wang, Yongkang Li, Yihong Tang, Chengyue Wang, Dingyi Zhuang, Kehua Chen, Hai Yang, Chengzhong Xu, et al. Think before you drive: World model-inspired multimodal grounding for autonomous vehicles. _arXiv preprint arXiv:2512.03454_ , 2025. 

   - 5 

- [35] Pei Liu, Qingtian Ning, Xinyan Lu, Haipeng Liu, Weiliang Ma, Dangen She, Peng Jia, Xianpeng Lang, and Jun Ma. Omnireason: A temporal-guided vision-language- 

action framework for autonomous driving. _arXiv preprint arXiv:2509.00789_ , 2025. 2 

- [36] Shilong Liu, Zhaoyang Zeng, Tianhe Ren, Feng Li, Hao Zhang, Jie Yang, Chunyuan Li, Jianwei Yang, Hang Su, Jun Zhu, et al. Grounding dino: Marrying dino with grounded pre-training for open-set object detection. _arXiv preprint arXiv:2303.05499_ , 2023. 6 

- [37] Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen, Omer Levy, Mike Lewis, Luke Zettlemoyer, and Veselin Stoyanov. Roberta: A robustly optimized bert pretraining approach. _arXiv preprint arXiv:1907.11692_ , 2019. 7 

- [38] Shujie Luo, Hang Dai, Ling Shao, and Yong Ding. C4av: learning cross-modal representations from transformers. In _ECCV_ , pages 33–38. Springer, 2020. 6 

- [39] Karttikeya Mangalam, Yang An, Harshayu Girase, and Jitendra Malik. From goals, waypoints & paths to long term human trajectory forecasting. In _Proceedings of the IEEE/CVF ICCV_ , pages 15233–15242, 2021. 6 

- [40] Gerald Matthews, Lisa Dorn, and A Ian Glendon. Personality correlates of driver stress. _Personality and Individual Differences_ , 12(6):535–549, 1991. 4 

- [41] Vivek Mittal. Attngrounder: Talking to cars with attention. In _ECCV_ , pages 62–73. Springer, 2020. 6 

- [42] Luntian Mou, Yiyuan Zhao, Chao Zhou, Bahareh Nakisa, Mohammad Naim Rastgoo, Lei Ma, Tiejun Huang, Baocai Yin, Ramesh Jain, and Wen Gao. Driver emotion recognition with a hybrid attentional multimodal fusion framework. _IEEE Transactions on Affective Computing_ , 14(4): 2970–2981, 2023. 2 

- [43] Tong Nie, Yuewen Mei, Yihong Tang, Junlin He, Jie Sun, Haotian Shi, Wei Ma, and Jian Sun. Steerable adversarial scenario generation through test-time preference alignment. _arXiv preprint arXiv:2509.20102_ , 2025. 1 

- [44] Chenbin Pan, Burhaneddin Yaman, Tommaso Nesti, Abhirup Mallik, Alessandro G Allievi, Senem Velipasalar, and Liu Ren. Vlp: Vision language planning for autonomous driving. In _Proceedings of the IEEE/CVF CVPR_ , pages 14760– 14769, 2024. 2 

- [45] Aditya Prakash, Kashyap Chitta, and Andreas Geiger. Multimodal fusion transformer for end-to-end autonomous driving. In _Proceedings of the IEEE/CVF CVPR_ , pages 7077– 7087, 2021. 1 

- [46] Rafael Rafailov, Archit Sharma, Eric Mitchell, Christopher D Manning, Stefano Ermon, and Chelsea Finn. Direct preference optimization: Your language model is secretly a reward model. _Nips_ , 36:53728–53741, 2023. 5 

- [47] Katrin Renz, Long Chen, Elahe Arani, and Oleg Sinavski. Simlingo: Vision-only closed-loop autonomous driving with language-action alignment. In _Proceedings of the CVPR_ , pages 11993–12003, 2025. 2 

- [48] Nivedita Rufus, Unni Krishnan R Nair, K Madhava Krishna, and Vineet Gandhi. Cosine meets softmax: A tough-tobeat baseline for visual grounding. In _ECCV_ , pages 39–50. Springer, 2020. 6 

- [49] Victor Sanh, Lysandre Debut, Julien Chaumond, and Thomas Wolf. Distilbert, a distilled version of bert: smaller, faster, cheaper and lighter. _arXiv preprint_ , 2019. 7 

10619 

- [50] Ranjan Sapkota, Yang Cao, Konstantinos I Roumeliotis, and Manoj Karkee. Vision-language-action models: Concepts, progress, applications and challenges. _arXiv preprint arXiv:2505.04769_ , 2025. 2 

- [51] Hao Shao, Yuxuan Hu, Letian Wang, Guanglu Song, Steven L Waslander, Yu Liu, and Hongsheng Li. Lmdrive: Closed-loop end-to-end driving with large language models. In _Proceedings of the IEEE/CVF CVPR_ , pages 15120– 15130, 2024. 2 

- [52] Jacopo Sini, Antonio Costantino Marceddu, Massimo Violante, and Riccardo Dess`ı. Passengers’ emotions recognition to improve social acceptance of autonomous driving vehicles. In _Progresses in Artificial Intelligence and Neural Systems_ , pages 25–32. Springer, 2020. 2 

- [53] Yihong Tang and Wei Ma. Intent: Trajectory prediction framework with intention-guided contrastive clustering. _IEEE Open Journal of Intelligent Transportation Systems_ , 2026. 2 

- [54] Yihong Tang, Zhaokai Wang, Ao Qu, Yihao Yan, Zhaofeng Wu, Dingyi Zhuang, Jushi Kai, Kebing Hou, Xiaotong Guo, Jinhua Zhao, et al. Itinera: Integrating spatial optimization with large language models for open-domain urban itinerary planning. In _Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing: Industry Track_ , pages 1413–1432, 2024. 2 

- [55] Yihong Tang, Ao Qu, Zhaokai Wang, Dingyi Zhuang, Zhaofeng Wu, Wei Ma, Shenhao Wang, Yunhan Zheng, Zhan Zhao, and Jinhua Zhao. Sparkle: Mastering basic spatial capabilities in vision language models elicits generalization to spatial reasoning. In _Findings of the Association for Computational Linguistics: EMNLP 2025_ , pages 4083– 4103, 2025. 2 

- [56] Yihong Tang, Zhan Zhao, Weipeng Deng, Shuyu Lei, Yuebing Liang, and Zhenliang Ma. Routekg: A knowledge graph-based framework for route prediction on road networks. _IEEE TITS_ , 2025. 2 

- [57] Amy Beth Warriner, Victor Kuperman, and Marc Brysbaert. Norms of valence, arousal, and dominance for 13,915 english lemmas. _Behavior research methods_ , 45(4):1191– 1207, 2013. 4 

- [58] Guoliang Xiang, Song Yao, Xianhui Wu, Hanwen Deng, Guojie Wang, Yu Liu, Fan Li, and Yong Peng. Driver multitask emotion recognition network based on multi-modal facial video analysis. _Pattern Recognition_ , 161:111241, 2025. 2 

- [59] Huafei Xiao, Wenbo Li, Guanzhong Zeng, Yingzhang Wu, Jiyong Xue, Juncheng Zhang, Chengmou Li, and Gang Guo. On-road driver emotion recognition using facial expression. _Applied Sciences_ , 12(2):807, 2022. 2 

- [60] Shuo Xing, Chengyuan Qian, Yuping Wang, Hongyuan Hua, Kexin Tian, Yang Zhou, and Zhengzhong Tu. Openemma: Open-source multimodal model for end-to-end autonomous driving. In _Proceedings of the WACV_ , pages 1001–1009, 2025. 2 

- [61] Zhenhua Xu, Yujia Zhang, Enze Xie, Zhen Zhao, Yong Guo, Kwan-Yee K Wong, Zhenguo Li, and Hengshuang Zhao. Drivegpt4: Interpretable end-to-end autonomous driving via large language model. _IEEE RAL_ , 2024. 2 

- [62] Bin Yan, Yi Jiang, Jiannan Wu, Dong Wang, Ping Luo, Zehuan Yuan, and Huchuan Lu. Universal instance perception as object discovery and retrieval. In _Proceedings of the IEEE/CVF CVPR_ , pages 15325–15336, 2023. 6 

- [63] An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao, Chengen Huang, Chenxu Lv, et al. Qwen3 technical report. _arXiv preprint arXiv:2505.09388_ , 2025. 6, 7 

- [64] Li Yang, Yan Xu, Chunfeng Yuan, Wei Liu, Bing Li, and Weiming Hu. Improving visual grounding with visuallinguistic verification and iterative reasoning. In _proceedings of the IEEE/CVF CVPR_ , pages 9499–9508, 2022. 6 

- [65] Yi Yang, Qingwen Zhang, Ci Li, Daniel Sim˜oes Marta, Nazre Batool, and John Folkesson. Human-centric autonomous systems with llms for user command reasoning. In _Proceedings of the IEEE/CVF WACV_ , pages 988–994, 2024. 2 

- [66] Zhenjie Yang, Yilin Chai, Xiaosong Jia, Qifeng Li, Yuqian Shao, Xuekai Zhu, Haisheng Su, and Junchi Yan. Drivemoe: Mixture-of-experts for vision-language-action model in end-to-end autonomous driving. _arXiv preprint arXiv:2505.16278_ , 2025. 1 

- [67] Shuang Zeng, Xinyuan Chang, Mengwei Xie, Xinran Liu, Yifan Bai, Zheng Pan, Mu Xu, and Xing Wei. Futuresightdrive: Thinking visually with spatio-temporal cot for autonomous driving. _arXiv preprint arXiv:2505.17685_ , 2025. 2, 6, 8 

- [68] Sebastian Zepf, Javier Hernandez, Alexander Schmitt, Wolfgang Minker, and Rosalind W Picard. Driver emotion recognition for intelligent vehicles: A survey. _ACM Computing Surveys (CSUR)_ , 53(3):1–30, 2020. 1 

- [69] Yanzhao Zhang, Mingxin Li, Dingkun Long, Xin Zhang, Huan Lin, Baosong Yang, Pengjun Xie, An Yang, Dayiheng Liu, Junyang Lin, et al. Qwen3 embedding: Advancing text embedding and reranking through foundation models. _arXiv preprint arXiv:2506.05176_ , 2025. 7 

- [70] He Zhao and Richard P Wildes. Where are you heading? dynamic trajectory prediction with expert goal examples. In _IEEE/CVF ICCV_ , pages 7629–7638, 2021. 6 

- [71] Jingyuan Zhao, Yuyan Wu, Rui Deng, Susu Xu, Jinpeng Gao, and Andrew Burke. A survey of autonomous driving from a deep learning perspective. _ACM Computing Surveys_ , 57(10):1–60, 2025. 1 

- [72] Yuze Zhao, Jintao Huang, Jinghan Hu, Daoze Zhang, Zeyinzi Jiang, Zhikai Wu, Baole Ai, Ang Wang, Wenmeng Zhou, and Yingda Chen. Swift: A scalable lightweight infrastructure for fine-tuning. _arXiv preprint arXiv:2408.05517_ , 2024. 5 

- [73] Xingcheng Zhou, Xuyuan Han, Feng Yang, Yunpu Ma, and Alois C Knoll. Opendrivevla: Towards end-to-end autonomous driving with large vision language action model. _arXiv preprint arXiv:2503.23463_ , 2025. 2 

- [74] Zewei Zhou, Tianhui Cai, Seth Z Zhao, Yun Zhang, Zhiyu Huang, Bolei Zhou, and Jiaqi Ma. Autovla: A visionlanguage-action model for end-to-end autonomous driving with adaptive reasoning and reinforcement fine-tuning. In _The Thirty-ninth Nips_ , 2025. 2 

10620 

