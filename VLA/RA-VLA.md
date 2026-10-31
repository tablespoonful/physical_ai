---
title: "RA-VLA: Retrieval-Augmented VLA for Test-Time Adaptation"
date: "2026-08-26"
authors: "Sanghwan Jang; Minjin Jeon; Minsoo Kim; Seongjin Choi; Dongha Kim; Hwanjo Yu"
venue: "ICML 2026"
url: https://arxiv.org/abs/2608.25585
pdf: https://arxiv.org/pdf/2608.25585
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2608.25585)** / [論文ページ](https://arxiv.org/abs/2608.25585)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **RA-VLA: Retrieval-Augmented VLA for Test-Time Adaptation** 

**Sanghwan Jang**<sup>1</sup> **Minjin Jeon**<sup>2</sup> **Minsoo Kim**<sup>2</sup> **Seongjin Choi**<sup>1</sup> **Dongha Kim**<sup>1</sup> **Hwanjo Yu**<sup>1 2</sup> 

## **Abstract** 

Vision-Language-Action (VLA) models provide a versatile foundation for general robotic manipulation, yet they exhibit significant brittleness when confronted with novel task distributions. While In-Context Imitation Learning (ICIL) offers a training-free alternative, existing frameworks suffer from an _adaptation bottleneck_ that hinders the effective translation of expert context to executable actions. This failure originates from superficial retrieval mechanisms and an inherent _behavioral inertia_ that anchors the policy to its pre-trained priors. To address these limitations, we present RA-VLA, a retrieval-augmented VLA framework that integrates behavior-aligned context retrieval with a grounded execution pipeline. By enforcing faithful adherence to functional cues within a scalable architecture, RA-VLA facilitates seamless task adaptation while preserving inference efficiency. Our empirical evaluations across the LIBERO benchmark and a real-world UR5e environment demonstrate that RA-VLA achieves superior success rates and computational efficiency, establishing a robust framework for training-free robotic adaptation. 

## **1. Introduction** 

Vision-Language-Action (VLA) models (Kim et al., 2025b; Pertsch et al., 2025; Li et al., 2024; Kim et al., 2025a; Black et al., 2025b;a; Bjorck et al., 2025) have emerged as a promising paradigm for general-purpose robotic manipulation, harnessing the vast knowledge embedded in multimodal foundation models (Karamcheti et al., 2024; Steiner et al., 2024; Chen et al., 2025) and large-scale robotic datasets (Walke et al., 2023; Khazatsky et al., 2024; O’Neill et al., 2024). Despite their impressive capabilities, existing 

> 1Department of Computer Science and Engineering, POSTECH, Pohang, South Korea<sup>2</sup> Graduate School of Artificial Intelligence, POSTECH, Pohang, South Korea. Correspondence to: Hwanjo Yu _<_ hwanjoyu@postech.ac.kr _>_ . 

_Proceedings of the 43_<sup>_rd_</sup> _International Conference on Machine Learning_ , Seoul, South Korea. PMLR 306, 2026. Copyright 2026 by the author(s). 


_Figure 1._ **_Adaptation bottleneck_ in existing ICIL frameworks.** Existing ICIL methods (a) prioritize superficial visual similarity over functional intent in context retrieval, (b) fail to effectively leverage contextual guidance, and (c) exhibit significant computational overhead for larger contexts. While this overhead is plotted for RICL, other ICIL baselines follow a nearly identical trend. 

VLAs exhibit significant brittleness when confronted with unseen manipulation tasks (Guruprasad et al., 2024; Fang et al., 2025; Fei et al., 2025; Gu et al., 2025). Specifically, when tasked with novel instructions, they predominantly revert to familiar behaviors from their training distribution or produce erratic motions that fail to align with the intended goal. This inherent reliance on static pre-trained knowledge poses a challenge for seamless deployment; effectively adapting high-capacity VLAs to new tasks necessitates an expensive and non-scalable re-training process to remain functional in dynamic environments. 

To overcome this limitation, In-Context Imitation Learning (ICIL) (Fu et al., 2025; Yoo et al., 2025; Zhu et al., 2024; Sridhar et al., 2025) has recently gained attention as a viable means of achieving test-time adaptation. This approach bypasses the expensive re-training process by providing a few expert demonstrations as in-context cues, which steer the policy toward new task objectives without explicit weight updates. By directly incorporating expert demonstrations into the input prompt, these frameworks attempt to provide behavioral guidance to reconcile the model’s pre-trained knowledge with unseen task demands. 

1 

**Retrieval-Augmented VLA** 

Despite their promise, existing ICIL frameworks suffer from an **_adaptation bottleneck_** —the inability to effectively translate in-context guidance into precise actions. This bottleneck is evidenced by the failure case of unseen _‘turn on the stove’_ task in Figure 1. As shown in (a), the current retriever prioritizes superficial visual similarity over functional intent, yielding behaviorally inconsistent guidance that misleads the policy. This issue is further exacerbated by _behavioral inertia_ (b), where the policy fails to modulate its execution based on the provided in-context cues and remains anchored to its pre-trained _bowl-picking_ prior. Even when attempting to directly utilize the retrieved actions, the policy fails to compensate for the discrepancies between the expert demonstration and the current scene. Furthermore, as illustrated in (c), current architectures incur significant computational overhead, with latency scaling poorly as the number of retrieved segments increases. 

To bridge this gap, we propose RA-VLA, a retrievalaugmented VLA framework that synergizes action-aware retrieval with a context-grounded execution pipeline to facilitate seamless in-context adaptation. Specifically, we introduce _behavioral alignment loss_ to train the retriever, mapping behaviorally similar expert segments close together in a shared latent space rather than relying on superficial visual features. The expert guidance retrieved from the aligned space ensures behavioral congruence with the target task demands, providing a robust foundation for in-context adaptation. Building on our retrieval mechanism, we introduce _contextual adherence loss_ to break the behavioral inertia rooted in the policy’s pre-trained priors. By enforcing an action regression margin between relevant and irrelevant expert segments, this loss incentivizes the policy to ground its action generation in the retrieved context. Crucially, these components are integrated into a scalable architecture that pre-encodes and caches each segment independently, thereby minimizing the computational overhead of incorporating expert guidance to the policy. 

We evaluate the proposed framework across both simulation and real-world platforms, including the LIBERO benchmark (Liu et al., 2023) and a UR5e robot environment. By testing on tasks entirely excluded from training, we demonstrate that RA-VLA can successfully execute novel behaviors via in-context guidance without any weight updates. Specifically, RA-VLA outperforms existing state-of-the-art baselines, yielding absolute success rate improvements of 17.60% on the LIBERO benchmark and 20.83% in the UR5e environment. Notably, enabled by our decoupled encoding design, the inference latency remains nearly constant regardless of the number of retrieved segments, facilitating practical robot deployment. 

## **2. Related Work** 

**Vision-Language-Action (VLA) Models.** The paradigm of robotic control has shifted from task-specific learning toward the development of generalist policies that leverage internet-scale knowledge. Central to this shift is the emergence of VLA models, which integrate large-scale Vision-Language Model (VLM) (Karamcheti et al., 2024; Steiner et al., 2024; Chen et al., 2025) priors with diverse robotic datasets (Walke et al., 2023; Khazatsky et al., 2024; O’Neill et al., 2024). Early studies (Zitkovich et al., 2023; Kim et al., 2025b; Pertsch et al., 2025) rely on action discretization to frame robotic manipulation as a multimodal sequence modeling problem, predicting commands as discrete tokens within a fixed vocabulary. Expanding upon this foundation, more recent approaches (Li et al., 2024; Kim et al., 2025a; Black et al., 2025b;a; Bjorck et al., 2025) have adopted generative action heads—incorporating diffusion or flow-matching mechanisms—to better capture the complex, multi-modal nature of robotic trajectories. Despite these advancements, recent studies (Guruprasad et al., 2024; Fang et al., 2025; Fei et al., 2025; Gu et al., 2025) have exposed a persistent fragility when deployed on novel tasks, often suffering from a severe performance collapse under minor environmental perturbations. This lack of robust generalization underscores the necessity for dynamic, in-context adaptation to mitigate epistemic uncertainty in unseen tasks. 

**In-Context Imitation Learning (ICIL).** ICIL represents a viable pathway to achieve test-time adaptation without requiring expensive weight updates. Early efforts in this domain, including one-shot imitation learning, pioneered the use of expert demonstrations as few-shot guidance to steer robotic policies. However, these methods are intrinsically tied to non-RGB modalities (e.g., depth or point clouds) (Vitiello et al., 2023; Biza et al., 2023; Palo & Johns, 2024; Vosylius & Johns, 2025), or lack compatibility with modern VLA models (Duan et al., 2017; Fu et al., 2025; Yoo et al., 2025). This structural rigidity precludes the full utilization of the rich semantic priors inherent in modern VLAs. While subsequent studies (Zhu et al., 2024; Sridhar et al., 2025) have integrated in-context adaptability into more generalist frameworks, they still face a fundamental adaptation bottleneck, failing to effectively leverage expert demonstrations as actionable guidance. This bottleneck hinders real-world deployment and constrains the practical utility of existing ICIL frameworks. 

## **3. Preliminaries** 

### **3.1. Robotic Manipulation** 

We consider the problem of language-conditioned robotic manipulation, where a policy _πθ_ aims to map multimodal inputs to a sequence of control signals (e.g., end-effector 

2 

**Retrieval-Augmented VLA** 

poses and gripper states). Formally, at each timestep _t_ , the policy receives a visual observation **V** _t_ (e.g., RGB images from static or eye-in-hand cameras), a language instruction _L_ , and the robot’s proprioceptive state **s** _t_ . Following the action chunking paradigm (Zhao et al., 2023) to ensure temporal consistency, the policy predicts an action chunk **A** _t ∈_ R<sup>_h×c_</sup> , where _h_ and _c_ denote the action horizon and action dimension, respectively. This mapping is defined as: 


The policy is trained via behavioral cloning to minimize the discrepancy between the predicted action chunk and the expert demonstration chunk. 

### **3.2. Flow-Matching-Based VLA Architecture** 

We employ a flow-matching-based Vision-Language-Action (VLA) architecture (Bjorck et al., 2025) that bridges highlevel semantic perception with low-level generative control. The model utilizes a Vision-Language Model (VLM) _fϕ_ to encode the visual observation **V** _t_ and language instruction _L_ , producing multimodal features **H** _t_ = _fϕ_ ( **V** _t, L_ ). 

The action head _gψ_ is a Diffusion Transformer (Peebles & Xie, 2023) that refines a noise distribution into the target action chunk. Conditioned on the multimodal features **H** _t_ and the robot’s proprioceptive state **s** _t_ , the action head regresses the vector field **F** _t_ = ( **A** _t −_ **A**<sup>(0)</sup> _t_<sup>) to guide the denoising</sup> process: 


where _k ∈_ [0 _,_ 1] is the flow-matching timestep and **A**<sup>(</sup> _t_<sup>_k_)</sup> is the noisy action chunk. This decoupled design ensures precise motor control by grounding the generative process in rich semantic features. 

## **4. Method** 

To overcome the limitations of existing in-context imitation learning (ICIL) approaches, we propose RA-VLA, a retrieval-augmented VLA framework that empowers a policy to perform novel manipulation tasks with negligible computational overhead. This section first outlines the overall architecture of our framework and then details the specific components that enable robust in-context imitation. To rigorously evaluate the policy’s training-free adaptability, we maintain a strict separation between the training<sup>1</sup> and evaluation task sets. Further details regarding the framework are provided in Appendix B. 

1In this context, training refers to the process of endowing the VLA policy with in-context adaptability. 

### **4.1. Overall Framework** 

The primary objective of RA-VLA is to facilitate trainingfree adaptation to novel tasks by leveraging a sparse set of expert demonstrations (e.g., 1–5 demonstrations per task) stored in a buffer _B_ . As illustrated in Figure 2, the framework operates through a systematic pipeline of expert segment retrieval and grounded action generation. 

**Context Buffer Construction.** To populate the context buffer _B_ , RA-VLA slices long-horizon expert demonstrations into functional segments ( **V**<sup>_′_</sup> _, L_<sup>_′_</sup> _,_ **s**<sup>_′_</sup> _,_ **A**<sup>_′_</sup> ) by applying a sliding window of length _h_ with a stride of _s_ . These segments serve as expert guidance to steer the policy toward novel tasks. To process this guidance without expanding the input sequence length, the framework treats each segment as an independent encoding unit, thereby bypassing the prohibitive computational overhead of full concatenation. This independence, coupled with a frozen VLM backbone _fϕ_ , allows the multimodal features **H**<sup>_′_</sup> = _fϕ_ ( **V**<sup>_′_</sup> _, L_<sup>_′_</sup> ) for all segments to be pre-computed and cached offline. Consequently, each segment is stored in the buffer as a key-value pair: the key **z**<sup>_′_</sup> is used for retrieval, while the corresponding value ( **H**<sup>_′_</sup> _,_ **s**<sup>_′_</sup> _,_ **A**<sup>_′_</sup> ) provides the in-context guidance.<sup>2</sup> 

**Expert Segment Retrieval.** For a given query consisting of a visual observation **V** _t_ and a language instruction _L_ , a retrieval encoder _R_ ( _·_ ) retrieves the _K_ most relevant expert segments _H_ ret = _{_ **H** ret<sup>(1)</sup><sup>_, ...,_</sup><sup>**H**(</sup> ret<sup>_K_)</sup><sup>_}_from the buffer</sup><sup>_B_.</sup> The retrieval encoder _R_ ( _·_ ) is a lightweight, two-layer Transformer encoder (Vaswani et al., 2017). It directly takes the multimodal input tokens that are fed into the VLM’s LLM backbone, which include image embeddings from the vision encoder and text token embeddings. The resulting tokens are average-pooled into embedding **z** , from which the top- _K_ segments are retrieved based on their cosine similarity to the query. 

**Grounded Action Generation.** The action head _gψ_ generates control sequences by leveraging the retrieved expert segments _H_ ret alongside the current observation **H** _t_ : 


Instead of attending to the entire set of expert features in every layer, our pairwise grounding strategy concatenates current observation features **H** _t_ with a single expert feature **H**<sup>(</sup> ret<sup>_i_)foreachcross-attentionlayer.Theexpertsegments</sup> are distributed progressively across layers, with the highest layers assigned the most relevant segments for fine-grained action refinement. This design maintains a minimal computational overhead while leveraging the full retrieved context. 

2In practice, the VLM backbone processes visual observations and language instructions, while the robot’s proprioceptive state and action sequences are encoded using separate linear encoders. 

3 

**Retrieval-Augmented VLA** 


_Figure 2._ **Overview of RA-VLA.** Our framework retrieves task-relevant expert segments to serve as in-context guidance, facilitating action generation for unseen task adaptation. The architecture integrates two key components: a retriever trained to identify behaviorally similar segments (Section 4.2) and a VLA policy finetuned to effectively ground action generation on the retrieved context (Section 4.3). 

### **4.2. Learning Action-Aware Retrieval** 

To ensure the retrieval process captures behavioral relevance rather than mere visual similarity, we propose a _behavioral alignment loss_ for the retrieval encoder _R_ ( _·_ ). The primary objective is to align the embedding space such that segments with similar behavioral patterns are mapped closely together, remaining robust to minor visual variations. 

**Behavioral Pairs.** To obtain the behaviorally similar segment pairs, we randomly sample two expert demonstrations of the same task and align their action sequences via Dynamic Time Warping (DTW) (Berndt & Clifford, 1994). This non-linear warping mechanism matches the structural profiles of the trajectories, which inherently accommodates both temporal stretching and spatial translation. Consequently, the aligned segment pairs share behavioral correspondence, regardless of visual appearance. Since such action sequences are unavailable within test-time observations, we train the retrieval encoder to approximate this action-based alignment using solely observation inputs. 

pairs ( _i, j_ ) that are aligned via the DTW optimal path. The set _Ni_ denotes the negative samples for anchor _i_ , which includes all other segments in the training batch (i.e., segments that are not aligned with anchor _i_ through DTW, as well as segments from different tasks). Through this alignment loss, _R_ ( _·_ ) learns to identify expert segments that provide behavioral guidance for the current observations. This formulation enables the behaviorally aligned retrieval to generalize to unseen tasks, as the retriever encoder captures underlying motion profiles that are not confined to the specific tasks encountered during training. 

### **4.3. Learning Context-Grounded Action Generation** 

In-context imitation learning often faces the challenge of _behavioral inertia_ , where the policy relies heavily on its pre-trained priors and disregards the contextual guidance. To encourage the action head _gψ_ to ground its predictions in the retrieved expert segments, we introduce a _contextual adherence loss_ based on a regression margin mechanism. 

**Behavioral Alignment Loss.** Using the alignments derived from DTW, we perform contrastive learning to train the retrieval encoder _R_ ( _·_ ). We optimize the encoder using a contrastive loss (Chen et al., 2020): 


where sim( _·, ·_ ) denotes cosine similarity and _τ_ is a temperature hyperparameter. Here, _P_ represents the set of positive 

**Contextual Adherence Loss.** During each training iteration, we compute two distinct mean squared error (MSE) losses with respect to the target vector field **F** _t_ : the relevant context loss _L_ rel utilizing segments retrieved via _R_ ( _·_ ), and the irrelevant context loss _L_ irrel utilizing randomly sampled segments: 


4 

**Retrieval-Augmented VLA** 

Using these, the contextual adherence loss is defined as: 


where _m >_ 0 denotes a fixed margin. By design, _L_ adhere incentivizes the policy to ground its predictions in the expert segments. If the policy disregards the retrieved context and predicts actions solely from current observations, _L_ rel and _L_ irrel collapse to similar values, violating the margin _m_ and incurring a loss penalty. From an efficiency standpoint, _L_ adhere adds a minor training cost by reusing multimodal features, while introducing zero inference overhead. 

The overall optimization objective for fine-tuning the policy _πθ_ is formulated as: 


where _λ_ serves as a weighting hyperparameter that balances the action regression loss _L_ rel and the contextual adherence loss _L_ adhere. 

**Remark.** While conventional flow-matching formulations typically sample the initial noisy action chunk **A**<sup>(0)</sup> _t_ from a standard normal distribution, we instead initialize **A**<sup>(0)</sup> _t_ with the empirical mean action chunk of the retrieved expert segments. This informed behavioral prior accelerates training convergence and significantly stabilizes the denoising process on unseen tasks. 

## **5. Experiments** 

### **5.1. Experimental Setups** 

**Environments.** We evaluate the in-context adaptability of RA-VLA across the LIBERO benchmark (Liu et al., 2023) and a real-world UR5e robot environment. LIBERO is a comprehensive robot learning benchmark that covers a diverse range of manipulation scenarios. In our experiments, we utilize four task suites—LIBERO-Spatial, LIBEROObject, LIBERO-Goal, LIBERO-Long—each consisting of 10 distinct tasks with 50 expert demonstrations per task. Our real-world UR5e environment is designed to replicate daily activities, comprising four representative tasks that require varied manipulation skills: (1) **Stack Box** : stacking a small box onto a larger box, (2) **Throw Trash** : throwing a trash into a red bin, (3) **Close Drawer** : closing an open drawer, (4) **Press Pedal** : pressing a pedal to open a trash can. For each task, we collected 30 expert demonstrations using the GELLO teleoperation interface (Wu et al., 2024). To account for environmental variability, each trial involved slight perturbations in the placement of the target and distractor objects, alongside minor variations in the robot’s initial proprioceptive states. 

**Evaluation Protocol.** To rigorously evaluate the framework’s training-free adaptability to novel tasks, we strictly decouple the training and evaluation tasks across all experimental environments. Within the LIBERO benchmark, we utilize three of the four available task suites to endow in-context capabilities, reserving the remaining suite as an entirely unseen domain for evaluation. For each held-out task, the buffer is populated with three expert demonstrations to serve as in-context guidance, and the performance is measured as the mean success rate over 50 trials. Similarly, in the real-world UR5e environment, we follow a leave-oneout scheme: three of the four tasks are used for training, while the remaining task is held out for evaluation. To enrich the diversity of learned manipulation priors, we augment the three in-domain training tasks with the LIBERO datasets as an auxiliary training source. During evaluation, the buffer is populated with four expert demonstrations for each held-out task to provide the necessary in-context guidance, and the evaluation results are reported as the success rate over 12 trials per task. 

**Baselines.** We compare the performance of RA-VLA against the following baselines:<sup>3</sup> 

- **Vanilla VLA** is trained only on the designated training tasks. It measures the VLA’s inherent generalization to novel tasks without external guidance. 

- **RAEA** (Zhu et al., 2024) conditions the policy by concatenating expert segments directly into the multimodal input prompt, allowing the policy to infer motion from the expert’s behavior. 

- **RICL** (Sridhar et al., 2025) fuses generative predictions with expert actions via a distance-weighted interpolation. Based on the weighting parameter, we evaluate two variants: **RICLG** , which prioritizes the VLA’s generative output, and **RICLR** , which assigns higher weight to the retrieved expert action. 

**Implementation Details.** Across all evaluated frameworks, we utilize GR00t N1.5 (Bjorck et al., 2025) as the underlying VLA backbone to ensure a consistent comparison. For the visual observation, the model processes dual-view RGB images from a third-person camera and a wrist camera, providing both global context and fine-grained local details. Regarding the action generation parameters, we maintain a consistent action horizon of 16 with 4 denoising steps across all experimental configurations. Unless otherwise specified, our default setup augments the policy with a single retrieved expert segment, serving as the primary in-context guidance. The detailed hyperparameters are provided in Appendix E. 

> 3Detailed description can be found in Appendix D. 

5 

**Retrieval-Augmented VLA** 

_Table 1._ **Novel task adaptation performance on the LIBERO benchmark.** All methods are evaluated on an entirely unseen task suite, utilizing three expert demonstrations per each held-out task as in-context guidance. Baselines are evaluated with both off-the-shelf SigLIP 2 and our SigLIP 2-based action-aware retriever. We report the mean success rate (%) for each task suite, and Average denotes the average success rate across all task suites. **Bold** and underline indicate the best and second-best performances, respectively. 

|Retriever|Method|LIBERO-Spatial|LIBERO-Object|LIBERO-Goal|LIBERO-Long|Average|
|---|---|---|---|---|---|---|
|–|Vanilla VLA|0.000|0.066|0.002|0.000|0.0170|
|Offthhlf|RAEA|0.060|0.106|0.008|0.006|0.0450|
|-e-se<br>(SiLIP 2)|RICLG|0.092|0.156|0.106|0.000|0.0885|
|g|RICLR|0.048|0.052|0.086|0.000|0.0465|
||RAEA|0.164|0.182|0.104|0.044|0.1235|
|Action-aware|RICLG|0.156|0.198|0.116|0.048|0.1295|
|(Ours)|RICLR|0.210|0.326|0.206|0.092|0.2085|
||**RA-VLA**|**0.320**|**0.556**|**0.532**|**0.130**|**0.3845**|


_Table 2._ **Novel task adaptation performance on the real-world UR5e environment.** All methods are evaluated on an entirely unseen task suite, utilizing four expert demonstrations per held-out task as in-context guidance. Baselines are evaluated with our SigLIP 2-based action-aware retriever. We report both sub-goal and overall success rates for each task. 

||Stack|Box|Throw|Trash|Close Dra|wer|Press P|edal||
|---|---|---|---|---|---|---|---|---|---|
|Method|_Pick Box_|Success|_Pick Trash_|Success|_Touch Drawer_|Success|_Touch Pedal_|Success|Average|
|Vanilla VLA|0.000|0.000|0.083|0.000|0.500|0.333|0.000|0.000|0.0833|
|RAEA|0.000|0.000|0.250|0.000|0.667|0.500|0.000|0.000|0.1250|
|RICLR|0.583|0.250|0.833|0.250|0.667|0.583|**0.667**|0.333|0.3542|
|**RA-VLA**|**0.750**|**0.417**|**0.917**|**0.750**|**0.750**|**0.667**|0.583|**0.417**|**0.5625**|


### **5.2. Novel Task Adaptation** 

**Simulation Evaluation.** As summarized in Table 1, vanilla VLA models exhibit near-zero success rates on novel tasks, confirming their lack of inherent adaptability to unseen scenarios. While existing ICIL methods utilizing off-the-shelf retriever such as SigLIP 2 (Tschannen et al., 2025) show marginal gains, their performance remains constrained by the frequent retrieval of behaviorally irrelevant segments that act as functional distractors. In contrast, integrating our proposed action-aware retrieval encoder consistently enhances the performance of all evaluated baselines. This consistent improvement across baselines demonstrates that our retrieval mechanism successfully filters out functional distractors in favor of behaviorally relevant context. Notably, RA-VLA, which couples this precise retrieval with enhanced contextual adherence to the expert segments, achieves the highest success rates across all evaluated task suites, improving the success rate from 20.9% to 38.5%. This result validates the synergy between behavioral intent alignment and grounded action execution, demonstrating that retrieved expert knowledge is faithfully integrated into the robot’s control loop to guide unseen tasks. 

**Real-World Evaluation.** We further validate our findings on a real-robot setup using RAEA, RICLR, and RA-VLA equipped with our action-aware retriever. As shown in Table 2, RA-VLA marks a significant leap in performance, boosting the success rate to 56.3% from the current state-of- 

the-art of 35.4%. To qualitatively analyze the performance gains, we examine policy rollouts in Figure 3, focusing on the behavioral characteristics that distinguish RA-VLA from the baselines. For the unseen task of _‘putting the small box on the large box’_ , RAEA incorrectly picks up the trash instead of the small box. This demonstrates that RAEA tends to favor behaviors prevalent in its training distribution over the provided expert guidance. RICLR, which simply blends retrieved action chunk with generative predictions, manages to lift the box but fails to accurately transport it to the target location. This suggests that such a naive ensemble mechanism yields imprecise and jittery control, preventing the policy from achieving the fine-grained manipulation required for successful task completion. In contrast to these baselines, RA-VLA achieves a robust synergy between expert adherence and adaptive precision, ensuring successful task completion even under significant distributional shifts. 

### **5.3. Contextual Sensitivity Analysis** 

To quantify the degree to which a model relies on the provided expert segments, we measure Relative Contextual Sensitivity _S_ ctx across the evaluated frameworks. This metric is defined as the relative change in the model’s action predictions when the retrieved expert context ( _D_ ret) is replaced with a randomly sampled context ( _D_ rand): 


6 

**Retrieval-Augmented VLA** 


_Figure 3._ **Qualitative comparison of policy rollouts on the real-robot** **_Stack Box_ task.** While all frameworks utilize our action-aware retriever to obtain expert context, only RA-VLA precisely executes unseen instructions by effectively leveraging this guidance. In contrast, baselines fail by reverting to pre-trained priors or lacking control precision. For further qualitative examples, see Figures 6–9. 

_Table 3._ **Contextual sensitivity.** The Relative Contextual Sensitivity _S_ ctx is averaged over 1,000 samples. We observe a positive trend where _S_ ctx correlates with increased success rates. 

|Method|_S_ctx|LIBERO-Goal|
|---|---|---|
|RAFT|0.0247|0.104|
|RICLR|0.0788|0.206|
|RA-VLA_w/o L_adhere|0.0353|0.098|
|RA-VLA|0.3639|0.532|


A higher _S_ ctx indicates that the model’s _generative prediction_ is more tightly coupled with the expert guidance provided in the context. 

As shown in Table 3, existing ICIL baselines exhibit significantly lower Relative Contextual Sensitivity than RA-VLA, indicating a lack of contextual grounding during action generation. This contextual neglect stems from the standard behavior cloning objective; since current observations often suffice to minimize the regression loss within the training distribution, the model lacks the incentive to learn querycontext interactions. Furthermore, we conduct an ablation study to analyze the impact of our proposed contextual adherence loss _L_ adhere. When this loss is removed, RA-VLA shows a marked decrease in _S_ ctx, accompanied by a corresponding drop in success rate. These results demonstrate that our adherence loss is essential for translating the retrieved expert knowledge into context-aware action execution. Further qualitative analysis supporting this observation is provided in Figure 10. 

### **5.4. Retriever Analysis** 

We conduct a qualitative analysis of the retrieval process by visualizing expert segments identified by our actionaware retrieval encoder and off-the-shelf foundation models, such as SigLIP 2 (Tschannen et al., 2025) and Eagle 2 (Chen et al., 2025). Specifically, given a pair of distinct expert trajectories, we examine the segment-wise alignment between them by retrieving the most relevant segment from one trajectory for each segment in the other. 

As shown in Figure 4, off-the-shelf models often retrieve behaviorally irrelevant distractors due to the semantic gap between general-purpose visual representations and the functional dynamics for robotic manipulation. In contrast, our action-aware retriever establishes robust correspondence by leveraging representations that encapsulate the underlying action dynamics learned via behavioral alignment loss. By replacing the baseline retriever with our action-aware retriever, the success rate of RA-VLA surges from 10.2% to 53.2% on LIBERO-Goal, demonstrating the critical role of behavioral consistency for in-context adaptation. 

### **5.5. Inference Scalability Analysis** 

Inference latency is a key consideration for high-frequency robotic control, as delays in the control loop can impact the stability of task execution. To evaluate the inference scalability of our framework, we compare the latency of RA-VLA against ICIL baselines as a function of the number of augmented expert segments _K_ . 

7 

**Retrieval-Augmented VLA** 


_Figure 4._ **Visualization of segment-level trajectory alignment.** For a given query segment, the retrieval model searches for the most relevant segment within the source trajectory. For instance, for the first segment of the query trajectory, the ViT-based retriever identifies the first image in the retrieval results as the most relevant match. However, while the query segment depicts the initial pickup phase, the retrieved segment corresponds to a later transport phase, illustrating a failure in capturing behavioral relevance. 

As illustrated in Figure 5, while RICL exhibits a steep increase in latency as more segments are integrated, RA-VLA maintains a near-constant inference time with only negligible overhead. A component-wise breakdown reveals that the primary bottleneck in existing ICIL methods stems from <mark>directly appending expert segments to the multimodal input</mark> prompt. This strategy leads to a substantial expansion of the context window, causing the computational overhead of the LLM backbone to scale unfavorably with _K_ . In contrast, RA-VLA circumvents this bottleneck by treating each retrieved segment as an independent encoding unit. This strategy decouples the inference latency from the scale of retrieved context, successfully mitigating the latency constraints that hinders the practical deployment of in-context policy adaptation. 


_Figure 5._ **Inference scalability.** The latency is averaged over 1,000 inference runs for the generation of a single action chunk. We use 4 denoising steps for the action head. Unlike existing ICIL approaches, RA-VLA enables the seamless integration of multiple expert segments. RAEA shows a similar trend to RICL, as illustrated in Figure 11. 

_Table 4._ **Impact of buffer size** _N_ **and retrieval size** _K_ **.** We report the average success rate (%) on the LIBERO-Goal. 

||1|2|3|4|
|---|---|---|---|---|
|N|0.482|0.518|0.532|0.552|
|K|0.532|0.540|0.548|0.546|


### **5.6. Analysis of Buffer and Retrieval Size** 

We further investigate the sensitivity of RA-VLA to the number of expert demonstrations in the buffer _N_ and the number of retrieved expert segments for in-context guidance _K_ . As illustrated in Table 4, the success rate increases consistently with the buffer size _N_ ; a larger demonstration buffer provides a richer search space, enabling the retriever to search for the segments that closely align with the behavioral nuances of the current observation. Regarding the number of retrieved segments _K_ , we observe a marginal performance gain as _K_ increases. While a small number of expert segments offer sufficient functional cues in our current setup, the inherent capability to scale _K_ remains highly promising for complex or ambiguous scenarios. 

## **6. Conclusion** 

In this work, we investigated the primary bottlenecks of existing in-context imitation learning (ICIL) frameworks, <mark>spe</mark> cifically the systematic inability to transfer the collected expert knowledge into the novel task execution. To overcome this limitation, we introduced RA-VLA, a retrievalaugmented framework that integrates a behavior-aligned retrieval into an efficient, grounded execution pipeline. Extensive experiments across simulation and real-world environments demonstrate that RA-VLA successfully adapts to unseen tasks while bypassing the latency penalty inherent in existing ICIL approaches. 

8 

**Retrieval-Augmented VLA** 

## **Acknowledgements** 

This work was supported by Samsung Research Funding & Incubation Center of Samsung Electronics under Project Number SRFC-IT2402-05. 

## **Impact Statement** 

Our work contributes to the development of more reliable and safe autonomous systems. A primary bottleneck in the real-world deployment of robotic agents is their limited generalization to out-of-distribution scenarios, which can lead to unpredictable or unsafe behaviors in critical environments. By enabling training-free in-context adaptation, RA-VLA provides a mechanism for human operators to quickly adjust a robot’s policy through corrective demonstrations. 

While RA-VLA enhances adaptability, its reliance on a demonstration buffer introduces a potential vulnerability to adversarial data injection. If a malicious actor were to introduce deceptive or harmful expert demonstrations into the retrieval buffer, the framework might integrate this guidance into its execution. To mitigate these risks, future deployments should implement robust verification protocols to ensure the integrity and quality of the demonstration sources before they are used for real-world robotic control. 

## **References** 

- An, S., Ma, Z., Lin, Z., Zheng, N., Lou, J.-G., and Chen, W. Make your llm fully utilize the context. In _Advances in Neural Information Processing Systems_ , 2024. URL https://proceedings.neurips.cc/paper _files/paper/2024/file/71c3451f6cd6a 4f82bb822db25cea4fd-Paper-Conference. pdf. 

- Berndt, D. J. and Clifford, J. Using dynamic time warping to find patterns in time series. In _Proceedings of the 3rd International Conference on Knowledge Discovery and Data Mining_ , 1994. 

- Biza, O., Thompson, S., Pagidi, K. R., Kumar, A., Pol, E. v. d., Walters, R., et al. One-shot imitation learning via interaction warping. In _Proceedings of The 7th Conference on Robot Learning_ , 2023. URL https://proc eedings.mlr.press/v229/biza23a.html. 

- Bjorck, J., Castaneda, F., Cherniadev, N., Da, X., Ding, R.,˜ Fan, L. J., et al. GR00T N1: An open foundation model for generalist humanoid robots, 2025. URL https: //arxiv.org/abs/2503.14734. 

- Black, K., Brown, N., Darpinian, J., Dhabalia, K., Driess, D., Esmail, A., et al. _π_ 0 _._ 5: a vision-language-action model with open-world generalization. In _Proceedings of The 9th Conference on Robot Learning_ , 2025a. URL 

https://proceedings.mlr.press/v305/b lack25a.html. 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M. R., Finn, C., et al. _π_ 0: A vision-language-action flow model for general robot control. In _Proceedings of Robotics: Science and Systems_ , 2025b. 

- Chen, G., Li, Z., Wang, S., Jiang, J., Liu, Y., Lu, L., et al. Eagle 2.5: Boosting long-context post-training for frontier vision-language models. In _Advances in Neural Information Processing Systems_ , 2025. URL https: //proceedings.neurips.cc/paper_files /paper/2025/file/833295cb9278a3ba973 842a94ea68e3c-Paper-Conference.pdf. 

- Chen, T., Kornblith, S., Norouzi, M., and Hinton, G. A simple framework for contrastive learning of visual representations. In _Proceedings of the 37th International Conference on Machine Learning_ , 2020. URL https://pr oceedings.mlr.press/v119/chen20j.html. 

- Duan, Y., Andrychowicz, M., Stadie, B., Ho, J., Schneider, J., Sutskever, I., et al. One-shot imitation learning. In _Advances in Neural Information Processing Systems_ , 2017. URL https://proceedings.neurips.cc/p aper_files/paper/2017/file/ba3866600 c3540f67c1e9575e213be0a-Paper.pdf. 

- Fang, I., Zhang, J., Tong, S., and Feng, C. From intention to execution: Probing the generalization boundaries of vision-language-action models, 2025. URL https: //arxiv.org/abs/2506.09930. 

- Fei, S., Wang, S., Shi, J., Dai, Z., Cai, J., Qian, P., et al. LIBERO-Plus: In-depth robustness analysis of visionlanguage-action models, 2025. URL https://arxi v.org/abs/2510.13626. 

- Fu, M., Huang, H., Datta, G., Chen, L. Y., Panitch, W., Liu, F., et al. ICRT: In-context imitation learning via nexttoken prediction. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , 2025. 

- Gu, Q., Ju, Y., Sun, S., Gilitschenski, I., Nishimura, H., Itkina, M., et al. SAFE: Multitask failure detection for vision-language-action models. In _Advances in Neural Information Processing Systems_ , 2025. URL https: //proceedings.neurips.cc/paper_files /paper/2025/file/392d0d05e2f514063e6 ce6f8b370834c-Paper-Conference.pdf. 

- Guruprasad, P., Sikka, H., Song, J., Wang, Y., and Liang, P. P. Benchmarking vision, language, & action models on robotic learning tasks, 2024. URL https://arxi v.org/abs/2411.05821. 

9 

**Retrieval-Augmented VLA** 

- Karamcheti, S., Nair, S., Balakrishna, A., Liang, P., Kollar, T., and Sadigh, D. Prismatic VLMs: Investigating the design space of visually-conditioned language models. In _Proceedings of the 41st International Conference on Machine Learning_ , 2024. URL https://proceedi ngs.mlr.press/v235/karamcheti24a.html. 

- Khazatsky, A., Pertsch, K., Nair, S., Balakrishna, A., Dasari, S., Karamcheti, S., et al. DROID: A large-scale inthe-wild robot manipulation dataset. In _Proceedings of Robotics: Science and Systems_ , 2024. 

- Kim, M. J., Finn, C., and Liang, P. Fine-tuning visionlanguage-action models: Optimizing speed and success. In _Proceedings of Robotics: Science and Systems_ , 2025a. 

- Kim, M. J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., et al. OpenVLA: An opensource vision-language-action model. In _Proceedings of The 8th Conference on Robot Learning_ , 2025b. URL https://proceedings.mlr.press/v270/k im25c.html. 

- Li, Q., Liang, Y., Wang, Z., Luo, L., Chen, X., Liao, M., et al. CogACT: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation, 2024. URL https://arxiv.org/ab s/2411.19650. 

- Lindvig, A. P., Iturrate, I., Kindler, U., and Sloth, C. ur ~~r~~ tde: An interface for controlling universal robots (ur) using the real-time data exchange (rtde). In _2025 IEEE/SICE International Symposium on System Integration (SII)_ , 2025. 

- Liu, B., Zhu, Y., Gao, C., Feng, Y., Liu, Q., Zhu, Y., et al. LIBERO: Benchmarking knowledge transfer for lifelong robot learning. In _Advances in Neural Information Processing Systems_ , 2023. URL https://proceeding s.neurips.cc/paper_files/paper/2023/ file/8c3c666820ea055a77726d66fc7d447 f-Paper-Datasets_and_Benchmarks.pdf. 

- O’Neill, A., Rehman, A., Maddukuri, A., Gupta, A., Padalkar, A., Lee, A., et al. Open X-Embodiment: Robotic learning datasets and rt-x models. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , 2024. 

- Palo, N. D. and Johns, E. Keypoint Action Tokens Enable InContext Imitation Learning in Robotics. In _Proceedings of Robotics: Science and Systems_ , 2024. 

- Peebles, W. and Xie, S. Scalable diffusion models with transformers. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , 2023. 

- Pertsch, K., Stachowicz, K., Ichter, B., Driess, D., Nair, S., Vuong, Q., et al. FAST: Efficient action tokenization for vision-language-action models. In _Proceedings of Robotics: Science and Systems_ , 2025. 

- Shi, W., Han, X., Lewis, M., Tsvetkov, Y., Zettlemoyer, L., and Yih, W.-t. Trusting your evidence: Hallucinate less with context-aware decoding. In _Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 2: Short Papers)_ , 2024. URL https://aclanthology.org/2024.na acl-short.69/. 

- Sridhar, K., Dutta, S., Jayaraman, D., and Lee, I. RICL: Adding in-context adaptability to pre-trained visionlanguage-action models. In _Proceedings of The 9th Conference on Robot Learning_ , 2025. URL https: //proceedings.mlr.press/v305/sridhar 25a.html. 

- Steiner, A., Pinto, A. S., Tschannen, M., Keysers, D., Wang, X., Bitton, Y., et al. PaliGemma 2: A family of versatile vlms for transfer, 2024. URL https://arxiv.org/ abs/2412.03555. 

- Tschannen, M., Gritsenko, A., Wang, X., Naeem, M. F., Alabdulmohsin, I., Parthasarathy, N., et al. SigLIP 2: Multilingual vision-language encoders with improved semantic understanding, localization, and dense features, 2025. URL https://arxiv.org/abs/2502.1 4786. 

- Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., et al. Attention is all you need. In _Advances in Neural Information Processing Systems_ , 2017. URL https://proceedings.neurips.cc/p aper_files/paper/2017/file/3f5ee2435 47dee91fbd053c1c4a845aa-Paper.pdf. 

- Vitiello, P., Dreczkowski, K., and Johns, E. One-shot imitation learning: A pose estimation perspective. In _Proceedings of The 7th Conference on Robot Learning_ , 2023. URL https://proceedings.mlr.press/v2 29/vitiello23a.html. 

- Vosylius, V. and Johns, E. Instant Policy: In-context imitation learning via graph diffusion. In _International Conference on Learning Representations_ , 2025. URL https: //proceedings.iclr.cc/paper_files/pa per/2025/file/5692c7dbc4abcaa50f9ce6 09819212e5-Paper-Conference.pdf. 

- Walke, H. R., Black, K., Zhao, T. Z., Vuong, Q., Zheng, C., Hansen-Estruch, P., et al. BridgeData V2: A dataset for robot learning at scale. In _Proceedings of The 7th Conference on Robot Learning_ , 2023. URL https: 

10 

**Retrieval-Augmented VLA** 

- //proceedings.mlr.press/v229/walke23a. html. 

- Wu, P., Shentu, Y., Yi, Z., Lin, X., and Abbeel, P. GELLO: A general, low-cost, and intuitive teleoperation framework for robot manipulators. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2024. 

- Yoo, Y., Hu, J., Zhu, Y., Liu, B., qiang liu, Mart´ın-Mart´ın, R., et al. RoboSSM: Scalable in-context imitation learning via state-space models. In _CoRL 2025 Workshop RemembeRL_ , 2025. URL https://openreview.n et/forum?id=JG8p1yGI6U. 

- Zhang, X., Lv, A., Liu, Y., Sung, F., Liu, W., Luan, J., et al. More is not always better? enhancing many-shot in-context learning with differentiated and reweighting objectives. In _Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , 2025. URL https://aclanthology .org/2025.acl-long.1475/. 

- Zhao, T. Z., Kumar, V., Levine, S., and Finn, C. Learning fine-grained bimanual manipulation with low-cost hardware. In _Proceedings of Robotics: Science and Systems_ , 2023. 

- Zhao, Z., Monti, E., Lehmann, J., and Assem, H. Enhancing contextual understanding in large language models through contrastive decoding. In _Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)_ , 2024. URL https://aclanthology.org/2024.naacl-l ong.237/. 

- Zhu, Y., Ou, Z., Mou, X., and Tang, J. Retrieval-augmented embodied agents. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2024. 

- Zitkovich, B., Yu, T., Xu, S., Xu, P., Xiao, T., Xia, F., et al. RT-2: Vision-language-action models transfer web knowledge to robotic control. In _Proceedings of The 7th Conference on Robot Learning_ , 2023. URL https: //proceedings.mlr.press/v229/zitkovi ch23a.html. 

11 

**Retrieval-Augmented VLA** 

## **A. Extended Related Work** 

**In-Context Adherence.** In natural language processing, extensive research has focused on ensuring that language models faithfully utilize information embedded within the provided context. For instance, contrastive decoding (Shi et al., 2024; Zhao et al., 2024) amplifies inherent contextual adherence by leveraging the discrepancy between model predictions with and without context. However, these methods assume the base model already exhibits baseline sensitivity to the context and require multiple forward passes, rendering them ill-suited for large-scale VLAs. On the other hand, establishing context-mandatory training scenarios (An et al., 2024) is highly difficult in in-distribution robotic manipulation. Because a standard observation typically encapsulates all necessary cues for action generation, it is practically unfeasible to design a training setup where the policy is forced to rely on the retrieved context to accurately predict actions. While assigning fixed relative weights of losses with and without context (Zhang et al., 2025) represents the closest parallel to our work, such weighting struggles to provide a sustained optimization signal for context differentiation throughout the entire training process. 

## **B. Additional Details on RA-VLA** 

**Demonstration Slicing.** An expert demonstration [( **V** 1 _, L,_ **s** 1 _,_ **a** 1) _,_ ( **V** 2 _, L,_ **s** 2 _,_ **a** 2) _, ..._ ] is sliced into functional segments ( **V** _t, L,_ **s** _t,_ **A** _t_ ) at timesteps _t ∈{_ 1 _,_ 1 + _s,_ 1 + 2 _s, ...}_ , where **A** _t_ denotes the action chunk [ **a** _t, ...,_ **a** _t_ + _h−_ 1]. 

**Retrieval Efficiency.** To illustrate the computational efficiency of our retrieval system, consider a typical expert demonstration consisting of 128 action steps. This demonstration is sliced into 15 segments, each stored in a GPU-managed buffer with a 1KB retrieval key vector, a 2MB pre-computed multimodal feature tensor, and a 1KB action chunk tensor. Such memory requirements are practically insignificant given the scale of modern GPU memory. In our current implementation, retrieval is performed via a low-latency matrix multiplication between the query (1 _×_ 512) and the stored keys ( _N ×_ 512), followed by a Top- _K_ operation. Notably, our benchmarks on an NVIDIA A100 GPU show a latency of just 0.18ms (0.36% of the total inference latency) for _N_ = 10<sup>7</sup> , which ensures that the retrieval stage does not introduce a latency bottleneck as the buffer scales. This design can be further scaled, as techniques like ANN indexing can be seamlessly integrated to handle an even larger volume of demonstrations. 

**Pairwise Grounding.** We manually designate the assignment of retrieved segments across the eight cross-attention layers to ensure a gradual and balanced distribution. For instance, when _K_ = 2 segments are retrieved, the first four cross-attention layers are assigned the second most relevant segment, while the remaining four layers receive the most relevant segment, yielding the assignment pattern [2, 2, 2, 2, 1, 1, 1, 1]. The segment assignment patterns for other values of _K_ are provided in Table 5. While our current implementation covers _K ≤_ 8, this strategy can be extended by dynamically adjusting assignments according to the denoising steps of flow matching. 

_Table 5._ **Segment assignment patterns across different values of** _K_ **.** 

|K|Segment Assignment|
|---|---|
|1|[1, 1, 1, 1, 1, 1, 1, 1]|
|2|[2, 2, 2, 2, 1, 1, 1, 1]|
|3|[3, 3, 2, 2, 2, 1, 1, 1]|
|4|[4, 4, 3, 3, 2, 2, 1, 1]|
|5|[5, 4, 3, 3, 2, 2, 1, 1]|
|6|[6, 5, 4, 3, 2, 2, 1, 1]|
|7|[7, 6, 5, 4, 3, 2, 1, 1]|
|8|[8, 7, 6, 5, 4, 3, 2, 1]|


**Behavioral Pairs.** Given two expert demonstrations [( **V** 1 _, L,_ **s** 1 _,_ **a** 1) _, ..._ ] and [( **V** 1<sup>_′, L′,_</sup><sup>**s**</sup><sup>_′_</sup> 1<sup>_,_</sup><sup>**a**</sup><sup>_′_</sup> 1<sup>)</sup><sup>_, ..._], we first apply the DTW</sup> algorithm to their respective action sequences [ **a** 1 _,_ **a** 2 _, ..._ ] and [ **a** 1<sup>_′,_</sup><sup>**a**</sup><sup>_′_</sup> 2<sup>_, ..._].This optimization determines which action pairs</sup> ( **a** _i,_ **a**<sup>_′_</sup> _j_<sup>)shouldbematchedtoachievethebestbehavioralalignment,whichyieldsawarpingpathconsistingofindex</sup> pairs ( _i, j_ ) that minimizes the L2 distance-based cumulative matching cost. Consequently, the aligned segment pairs ( **V** _i, L,_ **s** _i,_ **A** _i_ ) and ( **V** _j_<sup>_′, L′,_</sup><sup>**s**</sup><sup>_′_</sup> _j_<sup>_,_</sup><sup>**A**</sup><sup>_′_</sup> _j_<sup>) are designated as positive pairs, whereas unaligned pairs are treated as negatives.</sup> 

12 

**Retrieval-Augmented VLA** 

**Contextual Adherence Loss.** Regarding the formulation of _L_ adhere, we initially explored variants of ratio-based margin loss that constrain the ratio _L_ irrel _/L_ rel. However, as the policy converges and the absolute scale of the MSE diminishes toward zero, ratio-based losses tend to incur numerical instability and a diminishing gap effect, thereby failing to provide a consistent optimization signal. Consequently, we adopt the difference-based margin loss, which provides a robust and stable learning signal throughout the entire training process. 

## **C. Real-World Experimental Setup** 

The real-world robot platform consists of a UR5e robotic arm (Universal Robots) equipped with a Robotiq 2F-85 adaptive gripper. For visual observation, we utilize two Intel RealSense D435 cameras: one positioned as a static third-person camera to provide a global view of the workspace, and the other mounted on the wrist to capture localized, egocentric observations. 

Expert demonstrations are collected using the GELLO teleoperation interface (Wu et al., 2024), which allows for intuitive and high-fidelity control of the robotic arm. We synchronize data acquisition and command execution at 10 Hz, using the ur ~~r~~ tde (Lindvig et al., 2025) library to interface with the UR5e robot. 

Both the training and inference of the VLA model are conducted using a single NVIDIA A100 GPU. The model is served on an A100 node, and the robot controller communicates with this server to receive predicted action signals. 

## **D. Additional Details on ICIL Baselines** 

**Retrieval-Augmented Embodied Agents (RAEA)** (Zhu et al., 2024) incorporates expert demontration segments _D_ ret by concatenating them with the current query ( **V** _t_ , _L_ ) into a unified multimodal prompt. The VLM _fϕ_ then processes this concatenated sequence to extract multimodal features **H** _t_ : 


Conditioned on these features, the action head _gψ_ predicts a vector field **F** _t_ , which is subsequently used to generate the action chunk **A** _t_ .<sup>4</sup> 

**Re-training for In-Context Learning (RICL)** (Sridhar et al., 2025), similar to RAEA, integrates ICIL into the VLA framework by employing a supervised fine-tuning strategy that conditions the policy on expert demonstration segments _D_ ret. A key distinction of RICL is the action interpolation layer, which fuses expert action chunk **A**<sup>_′_</sup> with the policy’s generative output. The final action chunk **A** _t_ is formulated as a distance-weighted ensemble:<sup>5</sup> 


where _d_ = _∥R_ ( **V** _t_ ) _− R_ ( **V**<sup>_′_</sup> ) _∥_ 2 represents the _ℓ_ 2 distance between the query and the nearest neighbor in the retrieval space. The weighting function _w_ ( _d_ ) = _e_<sup>_−λwd_</sup> determines the balance between direct imitation and generative prediction. 

## **E. Additional Implementation Details** 

For the ICIL baselines, the weighting parameter _λw_ is set to 1.0 for RICLG and 0.2 for RICLR. In RA-VLA, we set the temperature _τ_ to 0.01, the stride _s_ to 4, the margin _m_ to 0.01, and the loss weighting factor _λ_ to 0.1.<sup>6</sup> The retrieval encoder _R_ ( _·_ ) is configured with a hidden size of 512, 8 attention heads, an intermediate size of 1024, and 2 hidden layers. 

> 4The architecture described here is our VLA-adapted implementation of RAEA, which extends its original principles to high-capacity VLA models. 

> 5For adaptation to flow matching, we rearrange Equation 10 with respect to the output of the policy _πθ_ to define the regression loss. 

> 6Although not applied to our main experiments, reducing the update magnitude of the noisy action chunk during the denoising steps showed stable performance on the LIBERO benchmark. 

13 

**Retrieval-Augmented VLA** 

## **F. Limitations** 

- Since the buffer serves as the sole source of guidance to unseen tasks, the quality and diversity of the expert demonstrations inherently dictates the in-context adaptability of the policy. Given that the specific demonstrations stored in the buffer notably impact performance, all experiments are conducted using the exact same buffer to ensure a fair comparison. 

- The absolute success rate remains low relative to the in-distribution performance, and the performance exhibits high sensitivity to hyperparameters due to the out-of-distribution nature of the evaluation. 

- Our findings warrant further validation across a broader range of experimental setups, such as large-scale training, non-flow-matching architectures, and complex manipulation tasks. For instance, as the training scale increases, an independent encoding strategy may constrain performance. 

## **G. Future Directions** 

Looking ahead, several promising avenues remain for further exploration. Extending our grounding mechanism to support cross-embodiment adaptation will substantially broaden the applicability of our framework. Furthermore, incorporating more diverse forms of expert guidance, such as unstructured human videos, represents a vital step toward achieving general-purpose robotic intelligence. 

## **H. Additional Experimental Results** 

We provide additional policy rollouts across diverse experimental configurations (Figures 6–9), policy rollouts with and without the contextual adherence loss _L_ adhere (Figure 10), and the full inference scalability results (Figure 11). 


_Figure 6._ **Qualitative comparison of policy rollouts for the** **_‘put the wine bottle on top of the cabinet’_ task in LIBERO-Goal.** While all frameworks utilize our action-aware retriever to obtain expert context, only RA-VLA precisely executes unseen instructions by effectively leveraging this guidance. In contrast, baselines fail by reverting to pre-trained priors or lacking control precision. 

14 

**Retrieval-Augmented VLA** 


_Figure 7._ **Qualitative comparison of policy rollouts on the real-robot** **_Throw Trash_ task.** While all frameworks utilize our action-aware retriever to obtain expert context, only RA-VLA precisely executes unseen instructions by effectively leveraging this guidance. In contrast, baselines fail by reverting to pre-trained priors or lacking control precision. 

15 

**Retrieval-Augmented VLA** 


_Figure 8._ **Qualitative comparison of policy rollouts on the real-robot** **_Close Drawer_ task.** For this specific task, the vanilla VLA exhibits a notable degree of adherence to the given instruction, suggesting that its pre-training distribution likely encompasses demonstrations relevant to drawer-closing maneuvers. 

16 

**Retrieval-Augmented VLA** 


_Figure 9._ **Qualitative comparison of policy rollouts on the real-robot** **_Press Pedal_ task.** While all frameworks utilize our action-aware retriever to obtain expert context, only RA-VLA precisely executes unseen instructions by effectively leveraging this guidance. In contrast, baselines fail by reverting to pre-trained priors or lacking control precision. 

17 

**Retrieval-Augmented VLA** 


_Figure 10._ **Qualitative comparison of policy rollouts with and without contextual adherence loss** _L_ **adhere.** In the absence of the contextual adherence loss, the policy fails to align with the expert guidance and instead (a) reverts to its pre-trained priors or (b) produce erratic actions. 


_Figure 11._ **Inference scalability.** The latency is averaged over 1,000 inference runs for the generation of a single action chunk. We use 4 denoising steps for the action head. Unlike existing ICIL approaches, RA-VLA enables the seamless integration of multiple expert segments. 

18 

