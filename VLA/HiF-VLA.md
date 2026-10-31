---
title: "HiF-VLA: Hindsight, Insight and Foresight through Motion Representation for Vision-Language-Action Models"
date: "2025-12-10"
authors: "Minghui Lin; Pengxiang Ding; Shu Wang; Zifeng Zhuang; Yang Liu; Xinyang Tong"
venue: "CVPR 2026"
url: https://arxiv.org/abs/2512.09928
pdf: https://arxiv.org/pdf/2512.09928
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2512.09928)** / [論文ページ](https://arxiv.org/abs/2512.09928)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **HiF-VLA: Hindsight, Insight and Foresight through Motion Representation for Vision-Language-Action Models** 

Minghui Lin<sup>1</sup> , Pengxiang Ding<sup>1</sup><sup>_,_2†</sup> , Shu Wang<sup>1</sup> , Zifeng Zhuang<sup>1</sup><sup>_,_2</sup> , Yang Liu<sup>1</sup> , Xinyang Tong<sup>1</sup> , Wenxuan Song<sup>3</sup> , Shangke Lyu<sup>4</sup> , Siteng Huang<sup>2†�</sup> , Donglin Wang<sup>1</sup><sup>_,_5�</sup> , 

1Westlake University 2Zhejiang University 3HKUST(GZ) 4Nanjing University 5Westlake Robotics 

linminghui@westlake.edu.cn, siteng.huang@gmail.com 

� https://hifvla.github.io � https://github.com/OpenHelix-Team/HiF-VLA 

## **Abstract** 

_Vision-Language-Action (VLA) models have recently enabled robotic manipulation by grounding visual and linguistic cues into actions. However, most VLAs assume the Markov property, relying only on the current observation and thus suffering from temporal myopia that degrades long-horizon coherence. In this work, we view motion as a more compact and informative representation of temporal context and world dynamics, capturing inter-state changes while filtering static pixel-level noise. From this perspective, HiF-VLA equips a motion-centric world model for the VLA, enabling agents to reason about temporal dynamics for future evolution during action generation. Building on this idea, we propose_ **_HiF-VLA_** _(_ **_Hindsight, Insight, and Foresight_** _for VLAs), a unified framework that leverages motion for bidirectional temporal reasoning. HiFVLA encodes past dynamics through hindsight priors, anticipates future motion via foresight reasoning, and integrates both through a hindsight-modulated joint expert to enable a “_ **_think-while-acting_** _” paradigm for long-horizon manipulation. As a result, HiF-VLA surpasses strong baselines on LIBERO-Long and CALVIN ABC-D benchmarks, while incurring negligible additional inference latency. Furthermore, HiF-VLA achieves substantial improvements in realworld long-horizon manipulation tasks, demonstrating its broad effectiveness in practical robotic settings._ 

## **1. Introduction** 

Vision-Language-Action models (VLAs) [3, 13, 14, 17, 45, 47] have emerged as a promising framework for robotic manipulation, leveraging powerful Vision-Language Models (VLMs) [1, 2, 9, 16, 31] to map visual and language representations to the action space. Despite progress, most 

> _†_ Project leads. � Corresponding authors. 

VLAs [17, 18, 32] implicitly assume a Markov property, predicting actions solely from the current observation without explicitly modeling temporal dependencies. This simplification leads to a form of **temporal myopia** . However, long-horizon manipulation requires reasoning that extends beyond the present, maintaining temporal continuity across visual, language, and motor modalities. Without such temporal reasoning, dependencies between consecutive actions deteriorate, resulting in fragmented trajectories and diminished task-level coherence. 

Recent efforts [24, 32, 46] have sought to alleviate this temporal myopia by incorporating historical context, most commonly by stacking multiple past observation frames. However, this approach is fundamentally limited. Stacking raw frames is not only computationally prohibitive and increases inference latency, hindering real-time control (see Tab. 3), but it also introduces substantial pixel-level redundancy. This deluge of static information often obscures the salient, task-relevant dynamics, making it difficult for the model to distinguish meaningful changes from background noise. We argue that a more precise and efficient representation of history is not the raw visual content of the past, but the motion that transpired between states. Motion serves as a direct and compact proxy for temporal memory and environment dynamics, faithfully capturing the dynamics of interactions (such as an object being moved or a drawer being closed), while discarding redundant static information. This makes motion an ideal primitive for representing history in a way that is both expressive and computationally efficient. 

Building on the principle of motion as a compact representation of history, we argue that robust decision-making requires bidirectional temporal reasoning, connecting the past to the future. An intelligent agent must possess **hindsight** , the ability to interpret recent dynamics that led to its current state, grounding its decisions in verified past outcomes. At the same time, it must exhibit **foresight** , the 

20732 


Figure 1. (a-b) Comparison with existing metho <mark>ds:</mark> V <mark>LA</mark> s rely on instantaneous observations [17, 18] (a-top), stack multiple past frames [24, 33] (a-second), or generate pixel-level subgoals [42, 44] (a-third), suffering from redundancy, high inference cost, and weak structure. In contrast, HiF-VLA (a-bottom) jointly models Hindsight, Insight, and Foresight, expanding the temporal receptive field bidirectionally for compact, structured, and efficient reasoning. (c) HiF-VLA reduces inference latency and achieves state-of-the-art performance on LIBERO-Long and CALVIN ABC-D, significantly outperforming the baseline in real-world experiments. 

capability to anticipate plausible future dynamics, enabling proactive, goal-directed behavior rather than purely reactive responses. Such bidirectional reasoning over past and future dynamics is also central to world models. We identify motion as the natural bridge unifying these two temporal dimensions. Consequently, we propose **HiF-VLA** ( **Hindsight, Insight, and Foresight** for VLA Models), a unified framework that leverages motion to structure this reasoning process. As detailed in Fig. 2, HiF-VLA comprises three components: **1) Hindsight prior acquisition:** encodes historical frames into structured, low-dimensional motion vectors [15] as hindsight, preserving dynamics without redundant pixels. **2) Foresight reasoning with insight:** interprets task instructions and current observations to anticipate plausible foresight motions and latent action tokens. **3) Hindsight-modulated joint expert:** applies hindsight as a top-down constraint on foresight and action streams, which interact within the expert decoder to generate temporally coherent actions. As shown in Fig. 1, compared to methods that rely solely on frame stacking or subgoal prediction, HiF-VLA more effectively bridges _perception_ , _dynamics_ , and _control_ within a unified representational space, forming a motion-centric World Action Model [40]. This design enables an embodied “think-whileacting” paradigm, enhancing robustness, temporal continuity, and causal consistency in long-horizon manipulation tasks. 

Our main contributions are summarized as follows: 

- We propose **HiF-VLA** , a VLA framework endowed with bidirectional spatio-temporal completion. By incorporating motion vectors as structured, low-dimensional temporal primitives, HiF-VLA explicitly expands the temporal receptive field, enabling temporally consistent and efficient action prediction while reducing redundancy. 

- We propose a **hindsight-modulated joint expert** that unifies temporal and action representations within a unified space, enabling a “think-while-acting” paradigm for causally consistent and temporally coherent long-horizon motion generation. 

- Extensive experiments demonstrate that our approach achieves substantial performance gains on widely adopted long-horizon benchmarks, while exhibiting strong temporal scalability and high inference efficiency. 

## **2. Related Work** 

**Vision-Language-Action Models.** VLA models learn endto-end mappings from language instructions and visual observations to low-level actions. Prior works can be broadly grouped by their action policies. Diffusion-based methods such as RDT-1B [25], CogACT [21], and DexVLA [36] employ iterative denoising to synthesize continuous control trajectories; autoregressive approaches like RT-2 [47] and OpenVLA [17] discretize continuous actions into tokens and predict them sequentially using VLM backbones; 

20733 

regression-oriented systems such as OpenVLA-OFT [18], VLA-Adapter [34] and SF [20] adopt bidirectional attention to directly learn continuous actions via L1 regression. However, most VLA models do not explicitly model temporal dependencies. They often neglect the importance of historical information and reasoning capabilities through VLMs, both of which have been shown to substantially improve performance in long-horizon video tasks [8, 11, 30]. **Temporal Modeling and Inference in Robotics.** Temporal modeling and foresight reasoning have been extensively studied in long video understanding and generation, but remain relatively underexplored in robotic manipulation. Existing approaches largely focus on one-sided reasoning. One line of work incorporates historical frames as visual prompts within the VLM input context, as in TraceVLA [46], Octo [32], GR-2 [7], RoboVLMs [24]. Another emphasizes foresight by predicting future visual subgoals to guide action generation, such as CoT-VLA [44], Seer [33], UniVLA [35], and UP-VLA [42], which typically condition an inverse dynamics model (IDM) on predicted future subgoals to infer actions. However, frame-level historical encoding and pixel-level future prediction introduce substantial computational overhead and redundancy, while failing to capture the importance of bidirectional temporal information. To address these, we propose HiF-VLA, which efficiently unifies hindsight, insight, and foresight within a single framework, enabling temporally coordinated decision-making for action generation. 

## **3. Method** 

### **3.1. Preliminary** 

We begin by defining the setting and notation for VLA reasoning. Robot expert demonstrations are denoted as _Dr_ = ( _l, a_ 1 _...T , o_ 1 _...T_ ). At each time step _t_ , the model receives an observation _ot_ and a textual instruction _l_ , and the objective is to predict an action chunk _at_ : _t_ + _n_ over a horizon of length _n_ . A vanilla VLA _Pθ_ [18] builds on visionlanguage models (VLMs), learning from diverse manipulation demonstrations to transfer vision-language understanding and generation capabilities to embodied scenarios. Formally: 


Our key insight is to expand the temporal receptive field available prior to action execution by compensating sparse visual observations. To this end, we propose HiF-VLA, as illustrated in Fig. 2, a unified framework built upon a vanilla VLA architecture, which incorporates compact historical information prior _m_<sup>_his_</sup> _t−h_ : _t_<sup>oflength</sup><sup>_h_andadditionallypre-</sup> dicts future motion _mt_ : _t_ + _n_ conditioned on the current insight. Formally, the inference process can be expressed as: 


During training, we augment the input with historical information and jointly predict both the future _n_ -step motion and the corresponding actions. During inference, motion decoding is optional and can be omitted depending on downstream task requirements. 

### **3.2. Hindsight Prior Acquisition** 

Relying solely on instantaneous visual observations for action decision-making often fails to provide stable perception, especially under challenging conditions such as occlusion or repeated executions. Hence, capturing consistent dynamic patterns of the manipulator from historical states is critical. Existing approaches [7, 32, 33] typically maintain a sliding window of past observations and concatenate them with the current observation to form a global representation. However, this frame-stacking strategy introduces significant redundancy: the high similarity between adjacent frames makes it difficult for the model to focus on taskrelevant dynamics, potentially dispersing its attention. 

To address this, we introduce a compressed historical prior: Motion Vectors (MVs) [15]. In video codec standards like H.264 [38] and MPEG-4 [19], MVs predict the displacements of macroblocks between adjacent frames to avoid pixel-wise redundancy. Importantly, MVs are not a coarse approximation: combined with keyframes, they enable near-lossless video reconstruction and maintain high compression. This property provides a natural, efficient, and faithful solution for capturing historical dynamics. Formally, let ( _x, y_ ) denote the position of a macroblock in an image (size _H × W ×_ 3). The motion vector is defined as: 


where ( _xt, yt_ ) and ( _xt−_ 1 _, yt−_ 1) denote the positions of the macroblock in consecutive frames _ot_ and _ot−_ 1. We adopt MPEG-4 to extract keyframes and motion information, regarding the current observation _ot_ at time step _t_ as the keyframe, while maintaining a historical window of length _m_ , forming GOP (Group of Pictures) units, _GOP_ = [ _MVt−m_ : _t−m_ +1 _, ..., MVt−_ 2: _t−_ 1 _, MVt−_ 1: _t, ot_ ]. Here, MVs follow the MPEG-4 16 _×_ 16 macroblock layout and are represented as a tensor of size _h ×_ ( _H//_ 16) _×_ ( _W//_ 16) _×_ 2, compactly encoding the historical motion trajectories of entities in the scene. Compared to raw frames, this representation significantly reduces redundancy while retaining taskrelevant dynamics, thereby providing structured spatiotemporal priors to the decision layer. 

Then, we adopt a lightweight ViT-based [10] hindsight encoder, combined with shallow 3D convolutions, to encode hindsight motions into compact hindsight tokens _Mh ∈_ R<sup>_Kh×d_</sup> . 

20734 


Figure 2. HiF-VLA Pipeline. (a) In Hindsight Prior Acquisition (see Sec. 3.2), HiF-VLA encodes dense historical frame sequences into compact Motion Vector (MV) streams, forming structured hindsight primitives that capture temporal dynamics without pixel redundancy. (b) In Foresight Reasoning with Insight (see Sec. 3.3), the VLM interprets the task instruction and current observation to infer plausible foresight motions and corresponding latent action tokens. (c) Finally, the Hindsight-Modulated Joint Expert (see Sec. 3.4) fuses hindsight, foresight, and action representations within a unified latent space, producing temporally consistent and causally coherent action predictions. 

### **3.3. Foresight Reasoning with Insight** 

Beyond historical cues, foresight is equally critical for robot tasks. It allows the agent to evaluate the consequences of its actions before execution, promoting more reliable action decision-making. Existing approaches, such as CoTVLA [44] and UP-VLA [42], achieve visual CoT reasoning by generating future visual subgoals. However, these approaches depend on pixel-level predictions prone to local distortions and semantic drift. The resulting dense and redundant subgoals obscure task-relevant dynamics, while the reliance on discrete frame prediction (without continuous temporal modeling) further undermines temporal consistency in complex environments. 

To address these limitations, we propose an efficient foresight reasoning mechanism guided by current insight, as shown in Fig. 2(b). Instead of predicting raw future pixels, we employ more general and structured MVs as spatiotemporal targets for future action execution. MVs compactly encode the trajectory evolution of the manipulator within the scene, effectively reducing pixel redundancy while providing a structured spatial prior. 

Specifically, we introduce _Kf_ learnable foresight query tokens _{q_ 1<sup>_f, q_</sup> 2<sup>_f, ..., q_</sup> _K_<sup>_f_</sup> _f_<sup>_}_,togetherwith</sup><sup>_Ka_emptyaction</sup> tokens _{q_ 1<sup>_a, q_</sup> 2<sup>_a, ..., q_</sup> _K_<sup>_a_</sup> _a_<sup>_}_,intotheVLMembeddingspace.</sup> These tokens are concatenated with the original inputs (including the task instruction _l_ , the current observation _ot_ ), and then fed into VLM _Fθ_ , enabling parallel reasoning over continuous visual dynamics and action generation, resulting 

in foresight motion tokens _Mf ∈_ R<sup>_Kf ×d_</sup> and action latent tokens _Af ∈_ R<sup>_Ka×d_</sup> . Formally, the reasoning process can be expressed as: ( _Mf , Af_ ) = _Fθ_ ( _ot, l_ ). 

We aim for the model to reason about visual foresight and action execution in parallel, and subsequently integrate and refine information from these distinct reasoning streams. This design enriches the diversity of the VLM’s internal thought process and unlocks the potential of parallel reasoning. 

### **3.4. Hindsight-Modulated Joint Expert** 

Conventionally, the action expert receives high-level representations from the VLM and translates them into low-level control signals. However, predicting actions in isolation lacks reasoning about the future dynamics. Motion, as the physical manifestation of actions in the visual space, provides complementary information: jointly predicting both motion and actions enables VLA models to better align semantic understanding with underlying dynamics. 

To achieve such synergistic reasoning, we propose the Hindsight-Modulated Joint Expert, which jointly models action and motion as two complementary streams within a shared temporal latent space and where historical information is introduced as a conditional prior to guide future inference and suppress erroneous replay of historical trajectories. Importantly, we integrate historical motion priors as adaptive temporal conditions, rather than embedding them directly into the VLM input. Injecting extra history motion into the VLM risks disrupting the established alignment be- 

20735 

tween visual and language modalities [43] (see Fig. 4). Instead, historical motion tokens _Mh_ are encoded into a compact conditional representation and modulate the joint reasoning process via Adaptive Layer Normalization (AdaLN) conditioning, where layered modulation and regularization jointly constrain future motion-action patterns. 

Formally, we define three types of sequence representations: hindsight motion tokens _Mh ∈_ R<sup>_Kh×d_</sup> (used only as conditional input), foresight motion latent tokens _Mf ∈_ R<sup>_Kf ×d_</sup> , and action tokens _Af ∈_ R<sup>_Ka×d_</sup> . As shown in Fig. 2(c), the foresight motion tokens and action tokens form two parallel streams, which interact via cross-stream joint attention while retaining separate FFNs to ensure complementary yet disentangled representations. The hindsight tokens _Mh_ are projected through a linear layer to obtain the conditioning vectors _hc_ , which is then injected into each joint expert module via AdaLN to modulate both foresight and action representations _z ∈{Mf , Af }_ : 


where _σ_ ( _z_ ) and _µ_ ( _z_ ) are the mean and standard deviation of _z_ , _γ_ ( _hc_ ) and _β_ ( _hc_ ) are modulation parameters from _hc_ . The Joint Attention employs non-causal self-attention over a sequence formed by concatenating _Mf_ and _Af_ , from which Q, K, and V are jointly projected. 

Finally, the fused motion and action representations are projected through their respective heads to generate the future motions _m_ ˜ _t_ : _t_ + _n_ and the actions ˜ _at_ : _t_ + _n_ . In general, the hindsight-modulated joint expert not only explicitly models the complementary relationship between action and motion, but also employs historical conditioning regularization to guide temporally consistent and physically plausible behaviors, thereby enhancing the stability and causal consistency of action. 

### **3.5. Unified HiF-VLA Model** 

**Input Representation** . Following OpenVLA-OFT [18], we feed the current observation into both the DINOv2 [27] and SigLIP [41] visual encoders to obtain a hybrid visual embedding. At the same time, we initialize a set of learnable foresight motion queries and empty action tokens. These tokens are concatenated with the instruction embedding and the current observation embedding to form the multi-modal input sequence. In parallel, the historical motion sequence is compressed via spatial-temporal convolution, aggregated by a ViT encoder, and projected into the latent space of the joint expert as the hindsight prior. **Parallel Decoding and Joint Expert** . The VLM adopts a non-causal attention mask, enabling joint prediction of future motion latents and action latents. The three streams of 

tokens (hindsight, foresight, predicted action) are then fused via the Hindsight-Modulated Joint Expert. 

**Training Objective** . We now describe in detail how we train the model to predict both actions and motion. To ensure both action and motion predictions remain wellcalibrated, we define two L1-loss objectives: 


The overall loss combines the two objectives: 


where _λ_ is a balancing factor between action accuracy and motion reconstruction quality, set to 0.01. 

## **4. Experiments** 

In this section, we design experiments to address the following research questions ( **RQs** ): 

**RQ1** : How does HiF-VLA perform compared to SOTA methods on challenging long-horizon benchmarks? **RQ2** : Does HiF-VLA effectively mitigate the redundancy and inefficiency issues in conventional approaches? **RQ3** : How well does HiF-VLA maintain inference scalability as the temporal horizon increases? **RQ4** : Through ablation studies, how do different components contribute to HiF-VLA’s overall performance? **RQ5** : Can HiF-VLA successfully handle long-horizon tasks on real-world robotic platforms? 

### **4.1. Overall Performance** 

**Experimental Setups.** We evaluate HiF-VLA on two long-horizon benchmarks. LIBERO-Long [23] comprises ten multi-subgoal manipulation tasks across diverse scenes. CALVIN ABC-D [26] includes four indoor environments (A-D); policies are trained on A-C and evaluated on the unseen D to assess generalization on consecutive tasks. All experiments are conducted under two settings following [18]: a third-view setup using the primary camera, or a multiview setup using both the primary and wrist cameras. **Implementation Details.** We adopt Prismatic-7B [16] as the VLM backbone, and initialize it with weights from OpenVLA [17], which were pretrained on OXE [28]. All other modules are randomly initialized. Training is performed on 8 NVIDIA A100 GPUs with a global batch size of 64. A fixed temporal chunk of **n=8** is adopted for both action and foresight modeling, while the hindsight window is variable ( **default 8** ). Fine-tuning is conducted for 150k steps on LIBERO and 80k on CALVIN. The main baseline is OpenVLA-OFT [18], which shares the same pretrained initialization. Additional comparisons include Seer [33], VPP [12], and _π_ 0 [3], etc. 

20736 

|**Method**|**Avg.**<br>**SR**|Put soup<br>and box<br>in basket|Put box<br>and butter<br>in basket|Turn on<br>stove and<br>put pot|Put bowl<br>in drawer<br>and close|Put mugs<br>on left<br>and right<br>plates|Pick book<br>and place<br>it in back|Put mug<br>on plate,<br>pudding<br>right|Put soup<br>and sauce<br>in basket|Put both<br>pots on<br>stove|Put mug<br>in<br>microwave<br>and close|
|---|---|---|---|---|---|---|---|---|---|---|---|
|_Policy inputs: third-_|_view ima_|_ge, language_|_instructio_|_n_||||||||
|OpenVLA [17]|54.0|35.0|95.0|65.0|45.0|40.0|80.0|60.0|45.0|20.0|55.0|
|UniVLA* [22]|63.0|64.0|82.0|76.0|96.0|58.0|98.0|24.0|74.0|32.0|26.0|
|MemoryVLA [29]|93.4|92.0|96.0|96.0|**100**|**100**|**100**|**96.0**|96.0|62.0|**96.0**|
|OpenVLA-OFT* [18]|91.0|82.0|96.0|96.0|94.0|90.0|96.0|92.0|**100**|70.0|94.0|
|**HiF-VLA(Ours)**|**94.4**|**94.0**|**98.0**|**100**|**100**|94.0|**100**|90.0|98.0|**76.0**|94.0|
|_Policy inputs: third-_|_person im_|_age, wrist-v_|_iew image,_|_language_|_instruction_|||||||
|Seer (scratch) [33]|78.7|80.0|90.0|91.7|81.7|85.0|65.0|86.7|88.3|51.7|66.7|
|Seer [33]|87.7|91.7|90.0|98.3|**100**|91.7|93.3|85.0|88.3|61.7|71.7|
|UniVLA* [22]|90.0|**100**|92.0|94.0|98.0|86.0|**100**|80.0|**100**|70.0|82.0|
|OpenVLA-OFT* [18]|94.0|90.0|**98.0**|98.0|98.0|96.0|**100**|92.0|**100**|72.0|96.0|
|**HiF-VLA(Ours)**|**96.4**|88.0|**98.0**|**100**|**100**|**100**|**100**|**96.0**|**100**|**82.0**|**100**|


Table 1. Performance comparison on the LIBERO-Long benchmark. We report the average success rate (%) across 10 tasks with “ **Avg. SR** ”. Results marked with “ _∗_ ” were reproduced using the official open-source code. **Bold** indicates the best performance. 

**Result Analysis. 1) LIBERO-Long:** As shown in Tab. 1, we present the detailed performance of HiF-VLA across 10 tasks in the LIBERO-Long benchmark. We evaluate both third-view and multi-view inputs over 500 trials. Compared to the baseline third-view method, our approach achieves a 94.4% success rate, representing a 3.4% absolute improvement. Notably, our third-view variant performs on par with multi-view baselines, underscoring HiF-VLA’s robust temporal reasoning capability. Moreover, our method achieves a 96.4% success rate under the multi-view setting, consistently outperforming other state-of-the-art VLA models. **2) CALVIN-ABC-D** : We further evaluate the generalization capability of HiF-VLA, which was trained on the ABC dataset and evaluated in the D environment. As shown in Tab. 2, our method surpasses the baseline by 0.25 in terms of the average task length metric and achieves superior performance under both third-view and multi-view settings. These results clearly answer **RQ1** . This improvement can be attributed to the bidirectional temporal perception and reasoning architecture incorporated in our model, which enables a more effective understanding of long-term action dependencies and consequently leads to enhanced adaptability and robustness in complex long-horizon tasks. 

### **4.2. Efficiency and Redundancy Analysis** 

**Experimental Setup.** We conduct experiments exclusively on LIBERO-Long to evaluate the efficiency and redundancy aspects, and the results are presented in Tab. 3. For the baseline (1), we adopt the method proposed by [18]. (2) “+ Subgoal” and (4) “+ History Frames” correspond to variants that incorporate RGB-based prediction and historical information following [7, 44]. (3) “+ Foresight (Ours)” and (5) “+ Hindsight (Ours)” denote variants that introduce Motion- 

|**Method**|1|2|3|4|5<br>**A**|**vg. Len.** _↑_|
|---|---|---|---|---|---|---|
|_Policy inputs: third-vi_|_ew im_|_age, i_|_nstruc_|_tion_|||
|SuSIE [4]|87.0|69.0|49.0|38.0|26.0|2.69|
|OpenVLA [17]|91.3|77.8|62.0|52.1|43.5|3.27|
|CLOVER [5]|**96.0**|83.5|70.8|57.5|45.4|3.53|
|VPP [12]|90.9|81.5|71.3|62.0|51.8|3.58|
|_π_0 [3]|93.7|83.2|74.0|62.9|51.0|3.65|
|UniVLA [6]|95.5|85.8|74.8|66.9|56.5|3.80|
|**HiF-VLA(Ours)**|93.5|**87.4**|**81.4**|**75.9**|**69.4**|**4.08**|
|_Policy inputs: third-p_|_erson_|_and w_|_rist-vi_|_ew im_|_age, inst_|_ruction_|
|GR-1 [39]|85.4|71.2|59.6|49.7|40.1|3.06|
|Vidman [37]|91.5|76.4|68.2|59.2|46.7|3.42|
|_π_0 [3]|93.8|85.0|76.7|68.1|59.9|3.92|
|UP-VLA [42]|92.8|86.5|81.5|76.9|69.9|4.08|
|OpenVLA-OFT [18]|96.3|89.1|82.4|75.8|66.5|4.10|
|RoboVLMs [24]|98.0|93.6|85.4|77.8|70.4|4.25|
|Seer [33]|96.3|91.6|86.1|80.3|74.0|4.28|
|VPP [12]|96.5|90.9|86.6|**82.0 **|**76.9**|4.33|
|**HiF-VLA(Ours)**|**98.5**|**94.1**|**88.1**|81.4|73.1|**4.35**|


Table 2. Performance comparison on the CALVIN ABC-D benchmarks. We report the average number of successfully completed tasks across five consecutive instructions. **Bold** indicates the best performance. 

based foresight and historical information, respectively. (6) “+ Hindsight + Foresight (Ours)” integrates both types of Motion-based information simultaneously. Note that we used third-person input, a hindsight length of 4, and a batch size of 4 in all experiments. 

**Result Analysis.** As shown in Tab. 3(2) and (3), incorporating subgoal or foresight prediction improves task suc- 

20737 


Fi <mark>g</mark> ure 3. Effect of hindsi <mark>g</mark> ht len <mark>g</mark> th on performance and efficienc <mark>y</mark> . <mark>(</mark> a <mark>)</mark> Exam <mark>p</mark> le of historical frames. <mark>(</mark> b <mark>)</mark> HiF-VLA maintains low inference latency as hindsight length increases. (c) Perfo <mark>rm</mark> ance of hindsight of different lengths in third-v <mark>ie</mark> w and multi-view perspectives. 

||**Methods**|**Peak GPU**<br>**Memory(GB)**_↓_|**Latency**<br>**(ms)**_↓_|**Avg.**<br>**SR**_↑_|
|---|---|---|---|---|
|(1)|Baseline|30.8 (1.00_×_)|72.9 (1.00_×_)|91.0|
|(2)|+ Subgoal|38.2 (1.24_×_)|115.9 (1.59_×_)|91.8|
|(3)|+ Foresight (Ours)|31.8 (1.03_×_)|82.7 (1.13_×_)|92.2|
|(4)|+ History frames|63.6 (2.06_×_)|229.5 (3.15_×_)|90.4|
|(5)|+ Hindsight (Ours)|31.4 (1.02_×_)|117.7 (1.61_×_)|92.2|
|(6)|+ Hindsight + Foresight (Ours)|32.2 (1.05_×_)|121.6 (1.67_×_)|93.2|


Table 3. Performance comparison between multi-frame baselines variants and HiF-VLA variants. Peak GPU memory (GB) during training and inference latency (ms) are reported. The history and hindsight lengths are fixed to 4 for a fair and computationally feasible comparison across all methods. 

cess rates; however, subgoal-based methods incur substantial latency overhead (1.59 _×_ slower than the baseline). In contrast, our foresight head introduces negligible additional cost (0.13 _×_ latency and 0.03 _×_ GPU Memory). Moreover, as illustrated in Tab. 3(4), dense multi-frame inputs significantly slow down inference (229.5 ms, 3.15 _×_ slower than the baseline) and even degrade performance, suggesting that redundant pixel information dilutes task-relevant temporal cues and may cause overfitting to visually irrelevant details. To address this, HiF-VLA replaces dense RGB inputs with compact motion representations, allowing the model to focus on dynamic and task-relevant cues, thereby improving both efficiency and accuracy. Furthermore, unified integration of hindsight and foresight further enhances overall performance. These results highlight HiF-VLA’s clear advantages in reducing redundancy and improving inference efficiency, effectively addressing **RQ2** . 

### **4.3. Inference Scalability** 

**Experimental Setup.** We evaluate the inference efficiency of HiF-VLA against two multi-frame baselines [18]: (i) multi-frame extension with stacked past observations, and (ii) multi-frame history combined with single-frame subgoal prediction. For each model variant, we conduct 100 

Figure 4. Performance comparison on different hindsight embedding locations. (a) represents direct injection into the VLM, and (b) represents conditional embedding as an expert decoder. (c) shows the performance of both on LIBERO-Long. _Mh_ denotes the hindsight tokens, _Mf_ represents the foresight tokens and _Af_ is the action tokens. 

inference runs on an NVIDIA A100 GPU and report the average latency (defined as the time required to generate one action chunk) in the LIBERO-Long simulation. 

**Results Analysis.** As shown in Fig. 3b, the latency of multi-frame baselines increases almost linearly with the length of history, reflecting their high computational sensitivity to frame stacking. For instance, at a history length of 8, the baseline incurs over 4.5× higher latency compared to the vanilla VLA. In contrast, HiF-VLA maintains a consistently low computational overhead across all context lengths, with latency increasing only marginally as history grows, demonstrating superior scalability with respect to temporal context length, thereby directly addresses **RQ3** . 

### **4.4. Ablation Studies** 

**Experimental Setup.** To address **RQ4** regarding the optimal integration of historical information, the effects of hindsight length and historical embedding positions are investigated on the LIBERO-Long. 

**Hindsight Length.** We examine the impact of hindsight length in both third-view and multi-view settings. As illustrated in Fig. 3c, the model achieves peak performance 94 _._ 4% and 96 _._ 4% when the hindsight length is set to 8. 

20738 


Figure 5. Real-world long-horizon tasks. (a) We deploy our system on the AgileX Piper robotic arm equipped with an external scene camera (Intel RealSense D435) and a wrist-mounted camera. (b) We design three long-horizon tasks covering diverse primitives such as pick, put, cover, stack, and press, emphasizing temporal consistency in action generation. 

We believe, in the LIBERO-Long benchmark, most manipulation sequences exhibit moderate temporal dependencies, where 8 hindsight lengths are sufficient to capture meaningful causal cues without introducing redundant information. **Hindsight Embedding Position.** We study how the embedding strategy of hindsight information affects model performance. Specifically, we compare two variants: (i) na¨ıvely concatenating hindsight with language and vision as direct inputs to the VLM, and (ii) conditioning hindsight within the expert module, which is adopted in our implementation. As shown in Fig. 4, the expert-conditioned embedding consistently achieves higher success rates than VLM-based embeddings. We attribute this to the fact that motion-based hindsight may interfere with the pretrained alignment between visual and language representations. In contrast, injecting hindsight at the decoding stage provides a more direct, residual-like path for motion information. This allows the low-level dynamics encoded in the hindsight to guide future action prediction without passing through, and potentially being corrupted by the VLM’s semantic fusion layers. 

### **4.5. Real-world Experiments** 

**Experiment setups.** To evaluate the effectiveness of our approach in real-world applications, we conduct real-world experiments using the AgileX Piper robot. As shown in Fig. 5(a), a RealSense D435 camera captures the scene from a third-view, while an additional USB camera is mounted on the robot’s wrist for egocentric observations. We collect three long-horizon tasks, each with 100 demonstrations involving diverse manipulation primitives, including pick, place, stack, cover, and press. 

**Real-world evaluation.** For real-world environments, we train each model separately for every task and evaluate performance by averaging success rates over 20 trials per task. These long-horizon tasks require the model to maintain action consistency across stages, correctly asso- 

ciate time states. As shown in Fig. 5(b), the baseline model (OpenVLA-OFT) performs poorly across these longhorizon tasks — for example, achieving only 17.4% success on Press-Buttons-Order, often failing to complete required button presses. This is likely due to the minimal visual difference between pressed and unpressed states, making it difficult for the baseline to detect successful actuation. In contrast, HiF-VLA benefits from its broad temporal receptive field, enabling reliable detection of subtle state transitions and robust execution of long-horizon tasks, resulting in superior performance across real-world tasks. 

## **5. Conclusion** 

This work introduces HiF-VLA, an efficient and unified framework for temporal perception and reasoning built upon low-dimensional, structured motion vectors. By integrating hindsight, insight, and foresight cues, HiFVLA establishes a bidirectional temporal expansion over a sparse visual receptive field, enabling the robot to capture task-critical dynamics at minimal computational cost and thereby improving temporal consistency and causal coherence in long-horizon tasks. Across both simulated and realworld long-horizon manipulation benchmarks, HiF-VLA demonstrates strong performance. **Limitations.** The current motion representation remains dependent on estimation accuracy and may be sensitive to noise in highly dynamic scenes. We leave the exploration of large-scale pretraining on internet videos to enhance motion understanding and generation capabilities for future work. 

## **Acknowledgements** 

This work was supported by the National Science and Technology Major Project (Grant No. 2022ZD0208800) and the National Natural Science Foundation of China General Program (Grant No. 62573362). 

20739 

## **References** 

- [1] Jinze Bai, Shuai Bai, Yunfei Chu, Zeyu Cui, Kai Dang, Xiaodong Deng, Yang Fan, Wenbin Ge, Yu Han, Fei Huang, et al. Qwen technical report. _arXiv preprint arXiv:2309.16609_ , 2023. 1 

- [2] Lucas Beyer, Andreas Steiner, Andr´e Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, et al. PaliGemma: A versatile 3B VLM for transfer. _arXiv preprint arXiv:2407.07726_ , 2024. 1 

- [3] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A vision-languageaction flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 1, 5, 6 

- [4] Kevin Black, Mitsuhiko Nakamoto, Pranav Atreya, Homer Rich Walke, Chelsea Finn, Aviral Kumar, and Sergey Levine. Zero-shot robotic manipulation with pre-trained image-editing diffusion models. In _Proceedings of the International Conference on Learning Representations_ , 2024. 6 

- [5] Qingwen Bu, Jia Zeng, Li Chen, Yanchao Yang, Guyue Zhou, Junchi Yan, Ping Luo, Heming Cui, Yi Ma, and Hongyang Li. Closed-loop visuomotor control with generative expectation for robotic manipulation. In _Proceedings of the Advances in Neural Information Processing Systems_ , pages 139002–139029, 2024. 6 

- [6] Qingwen Bu, Yanting Yang, Jisong Cai, Shenyuan Gao, Guanghui Ren, Maoqing Yao, Ping Luo, and Hongyang Li. UniVLA: Learning to act anywhere with task-centric latent actions. _arXiv preprint arXiv:2505.06111_ , 2025. 6 

- [7] Chi-Lam Cheang, Guangzeng Chen, Ya Jing, Tao Kong, Hang Li, Yifeng Li, Yuxiao Liu, Hongtao Wu, Jiafeng Xu, Yichu Yang, et al. GR-2: A generative video-languageaction model with web-scale knowledge for robot manipulation. _arXiv preprint arXiv:2410.06158_ , 2024. 3, 6 

- [8] Boyuan Chen, Diego Mart´ı Mons´o, Yilun Du, Max Simchowitz, Russ Tedrake, and Vincent Sitzmann. Diffusion Forcing: Next-token prediction meets full-sequence diffusion. _Proceedings of the Advances in Neural Information Processing Systems_ , 37:24081–24125, 2024. 3 

- [9] Xi Chen, Josip Djolonga, Piotr Padlewski, Basil Mustafa, Soravit Changpinyo, Jialin Wu, Carlos Riquelme Ruiz, Sebastian Goodman, Xiao Wang, Yi Tay, et al. On scaling up a multilingual vision and language model. _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 14432–14444, 2023. 1 

- [10] Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn, Xiaohua Zhai, Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg Heigold, Sylvain Gelly, Jakob Uszkoreit, and Neil Houlsby. An image is worth 16x16 words: Transformers for image recognition at scale. In _Proceedings of the International Conference on Learning Representations_ , 2021. 3 

- [11] Yuwei Guo, Ceyuan Yang, Ziyan Yang, Zhibei Ma, Zhijie Lin, Zhenheng Yang, Dahua Lin, and Lu Jiang. Long 

   - context tuning for video generation. _arXiv preprint arXiv:2503.10589_ , 2025. 3 

- [12] Yucheng Hu, Yanjiang Guo, Pengchao Wang, Xiaoyu Chen, Yen-Jen Wang, Jianke Zhang, Koushil Sreenath, Chaochao Lu, and Jianyu Chen. Video prediction policy: A generalist robot policy with predictive visual representations. In _Proceedings of the International Conference on Machine Learning_ , 2025. 5, 6 

- [13] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. _π_ 0 _._ 5: a vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 1 

- [14] Yuming Jiang, Siteng Huang, Shengke Xue, Yaxi Zhao, Jun Cen, Sicong Leng, Kehan Li, Jiayan Guo, Kexiang Wang, Mingxiu Chen, Fan Wang, Deli Zhao, and Xin Li. RynnVLA-001: Using human demonstrations to improve robot manipulation. _arXiv preprint arXiv:2509.15212_ , 2025. 1 

- [15] Yang Jin, Zhicheng Sun, Kun Xu, Liwei Chen, Hao Jiang, Quzhe Huang, Chengru Song, Yuliang Liu, Di Zhang, Yang Song, et al. Video-LaVIT: Unified video-language pretraining with decoupled visual-motional tokenization. In _Proceedings of the International Conference on Machine Learning_ , 2024. 2, 3 

- [16] Siddharth Karamcheti, Suraj Nair, Ashwin Balakrishna, Percy Liang, Thomas Kollar, and Dorsa Sadigh. Prismatic VLMs: Investigating the design space of visuallyconditioned language models. In _Proceedings of the International Conference on Machine Learning_ , 2024. 1, 5 

- [17] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. OpenVLA: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 1, 2, 5, 6 

- [18] Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 1, 2, 3, 5, 6, 7 

- [19] Didier Le Gall. MPEG: A video compression standard for multimedia applications. _Communications of the ACM_ , 34 (4):46–58, 1991. 3 

- [20] Fuhao Li, Wenxuan Song, Han Zhao, Jingbo Wang, Pengxiang Ding, Donglin Wang, Long Zeng, and Haoang Li. Spatial Forcing: Implicit spatial representation alignment for vision-language-action model. _arXiv preprint arXiv:2510.12276_ , 2025. 3 

- [21] Qixiu Li, Yaobo Liang, Zeyu Wang, Lin Luo, Xi Chen, Mozheng Liao, Fangyun Wei, Yu Deng, Sicheng Xu, Yizhong Zhang, et al. CogACT: A foundational visionlanguage-action model for synergizing cognition and action in robotic manipulation. _arXiv preprint arXiv:2411.19650_ , 2024. 2 

- [22] Shuang Li, Yihuai Gao, Dorsa Sadigh, and Shuran Song. Unified video action model. _arXiv preprint arXiv:2503.00200_ , 2025. 6 

- [23] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. LIBERO: Benchmarking knowl- 

20740 

edge transfer for lifelong robot learning. In _Proceedings of the Advances in Neural Information Processing Systems_ , pages 44776–44791, 2023. 5 

- [24] Huaping Liu, Xinghang Li, Peiyan Li, Minghuan Liu, Dong Wang, Jirong Liu, Bingyi Kang, Xiao Ma, Tao Kong, and Hanbo Zhang. Towards generalist robot policies: What matters in building vision-language-action models. _arXiv preprint arXiv:2412.14058_ , 2025. 1, 2, 3, 6 

- [25] Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. RDT-1B: a diffusion foundation model for bimanual manipulation. In _Proceedings of the International Conference on Learning Representations_ , 2025. 2 

- [26] Oier Mees, Lukas Hermann, Erick Rosete-Beas, and Wolfram Burgard. CALVIN: A benchmark for languageconditioned policy learning for long-horizon robot manipulation tasks. _IEEE Robotics and Automation Letters_ , 7(3): 7327–7334, 2022. 5 

- [27] Maxime Oquab, Timoth´ee Darcet, Th´eo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin El-Nouby, et al. DINOv2: Learning robust visual features without supervision. _Transactions on Machine Learning Research_ , 2024. 5 

- [28] Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, et al. Open X-Embodiment: Robotic learning datasets and RT-X models : Open X-Embodiment collaboration. In _2024 IEEE International Conference on Robotics and Automation_ , pages 6892– 6903. IEEE, 2024. 5 

- [29] Hao Shi, Bin Xie, Yingfei Liu, Lin Sun, Fengrong Liu, Tiancai Wang, Erjin Zhou, Haoqiang Fan, Xiangyu Zhang, and Gao Huang. MemoryVLA: Perceptual-cognitive memory in vision-language-action models for robotic manipulation. _arXiv preprint arXiv:2508.19236_ , 2025. 6 

- [30] Kiwhan Song, Boyuan Chen, Max Simchowitz, Yilun Du, Russ Tedrake, and Vincent Sitzmann. History-guided video diffusion. _arXiv preprint arXiv:2502.06764_ , 2025. 3 

- [31] Gemini Team, Rohan Anil, Sebastian Borgeaud, JeanBaptiste Alayrac, Jiahui Yu, Radu Soricut, Johan Schalkwyk, Andrew M Dai, Anja Hauth, Katie Millican, et al. Gemini: a family of highly capable multimodal models. _arXiv preprint arXiv:2312.11805_ , 2023. 1 

- [32] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 1, 3 

- [33] Yang Tian, Sizhe Yang, Jia Zeng, Ping Wang, Dahua Lin, Hao Dong, and Jiangmiao Pang. Predictive inverse dynamics models are scalable learners for robotic manipulation. In _Proceedings of the International Conference on Learning Representations_ , 2025. 2, 3, 5, 6 

- [34] Yihao Wang, Pengxiang Ding, Lingxiao Li, Can Cui, Zirui Ge, Xinyang Tong, Wenxuan Song, Han Zhao, Wei Zhao, Pengxu Hou, et al. VLA-Adapter: An effective paradigm for tiny-scale vision-language-action model. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , 2025. 3 

- [35] Yuqi Wang, Xinghang Li, Wenxuan Wang, Junbo Zhang, Yingyan Li, Yuntao Chen, Xinlong Wang, and Zhaoxiang Zhang. Unified vision-language-action model. _arXiv preprint arXiv:2506.19850_ , 2025. 3 

- [36] Junjie Wen, Yichen Zhu, Jinming Li, Zhibin Tang, Chaomin Shen, and Feifei Feng. DexVLA: Vision-language model with plug-in diffusion expert for general robot control. _arXiv preprint arXiv:2502.05855_ , 2025. 2 

- [37] Youpeng Wen, Junfan Lin, Yi Zhu, Jianhua Han, Hang Xu, Shen Zhao, and Xiaodan Liang. VidMan: Exploiting implicit dynamics from video diffusion model for effective robot manipulation. _Proceedings of the Advances in Neural Information Processing Systems_ , 37:41051–41075, 2024. 6 

- [38] Thomas Wiegand, Gary J Sullivan, Gisle Bjontegaard, and Ajay Luthra. Overview of the H. 264/AVC video coding standard. _IEEE Transactions On Circuits and Systems For Video Technology_ , 13(7):560–576, 2003. 3 

- [39] Hongtao Wu, Ya Jing, Chilam Cheang, Guangzeng Chen, Jiafeng Xu, Xinghang Li, Minghuan Liu, Hang Li, and Tao Kong. Unleashing large-scale video generative pre-training for visual robot manipulation. In _Proceedings of the International Conference on Learning Representations_ , 2024. 6 

- [40] Seonghyeon Ye, Yunhao Ge, Kaiyuan Zheng, Shenyuan Gao, Sihyun Yu, George Kurian, Suneel Indupuru, You Liang Tan, Chuning Zhu, Jiannan Xiang, Ayaan Malik, Kyungmin Lee, William Liang, Nadun Ranawaka, Jiasheng Gu, Yinzhen Xu, Guanzhi Wang, Fengyuan Hu, Avnish Narayan, Johan Bjorck, Jing Wang, Gwanghyun Kim, Dantong Niu, Ruijie Zheng, Yuqi Xie, Jimmy Wu, Qi Wang, Ryan Julian, Danfei Xu, Yilun Du, Yevgen Chebotar, Scott Reed, Jan Kautz, Yuke Zhu, Linxi ”Jim” Fan, and Joel Jang. World action models are zero-shot policies. _arXiv preprint arXiv:2602.15922_ , 2026. 2 

- [41] Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and Lucas Beyer. Sigmoid loss for language image pre-training. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 11975–11986, 2023. 5 

- [42] Jianke Zhang, Yanjiang Guo, Yucheng Hu, Xiaoyu Chen, Xiang Zhu, and Jianyu Chen. UP-VLA: A unified understanding and prediction model for embodied agent. _arXiv preprint arXiv:2501.18867_ , 2025. 2, 3, 4, 6 

- [43] Zongzheng Zhang, Haobo Xu, Zhuo Yang, Chenghao Yue, Zehao Lin, Huan-ang Gao, Ziwei Wang, and Hao Zhao. Tavla: Elucidating the design space of torque-aware visionlanguage-action models. _arXiv preprint arXiv:2509.07962_ , 2025. 5 

- [44] Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli Ma, Song Han, Chelsea Finn, Ankur Handa, Tsung-Yi Lin, Gordon Wetzstein, Ming-Yu Liu, and Donglai Xiang. CoT-VLA: Visual chain-of-thought reasoning for vision-language-action models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 1702–1713, 2025. 2, 3, 4, 6 

- [45] Haoyu Zhen, Xiaowen Qiu, Peihao Chen, Jincheng Yang, Xin Yan, Yilun Du, Yining Hong, and Chuang Gan. 3DVLA: A 3D vision-language-action generative world model. 

20741 

In _Proceedings of the International Conference on Machine Learning_ , 2024. 1 

- [46] Ruijie Zheng, Yongyuan Liang, Shuaiyi Huang, Jianfeng Gao, Hal Daum´e III, Andrey Kolobov, Furong Huang, and Jianwei Yang. TraceVLA: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies. In _Proceedings of the International Conference on Learning Representations_ , 2025. 1, 3 

- [47] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. RT-2: Vision-language-action models transfer web knowledge to robotic control. In _Proceedings of the Conference on Robot Learning_ , pages 2165–2183, 2023. 1, 2 

20742 

