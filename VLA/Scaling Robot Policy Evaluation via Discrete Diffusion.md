---
title: "Scaling Robot Policy Evaluation via Discrete Diffusion World Model"
date: "2026"
venue: "ICML 2026"
url: https://proceedings.mlr.press/v306/li26hi.html
pdf: https://raw.githubusercontent.com/mlresearch/v306/main/assets/li26hi/li26hi.pdf
converter: pymupdf4llm
---

> **[PDF を開く](https://raw.githubusercontent.com/mlresearch/v306/main/assets/li26hi/li26hi.pdf)** / [論文ページ](https://proceedings.mlr.press/v306/li26hi.html)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Scaling Robot Policy Evaluation via Discrete Diffusion World Model** 

### **Yaxuan Li**<sup>1</sup> **Junjie Wen**<sup>2</sup> **Zhongyi Zhou**<sup>1 2</sup> **Yefei Chen**<sup>1</sup> **Chaomin Shen**<sup>1</sup> **Yaxin Peng**<sup>3</sup> **Yichen Zhu**<sup>2</sup> 


_Figure 1._ **dWorldEval** is a discrete diffusion world model designed to be controllable and consistent for reliable policy evaluation. It ensures action controllability and spatiotemporal consistency while providing the policy compatibility and faithful progress scoring necessary for accurate, automated policy ranking. 

## **Abstract** 

Evaluating generalist robot manipulation policies is costly and difficult to scale in the real world. While emerging world models (e.g., WorldEval, Ctrl-World) offer a promising alternative, the reliability of such evaluation remains a critical bottleneck. Specifically, their visual predictions can undermine policy assessment by “selfcorrecting” failures into false positives or yielding artifacts under out-of-distribution controls. Even with failure-enriched data, current architectures struggle to capture action-causal dynamics, as they typically treat actions as passive conditions 

> 1School of Computer Science,East China Normal University, Shanghai, China 2Current Robotics, Shanghai, China 

> 3Department of Mathematics & School of Future Technology, Shanghai University, Shanghai, China. Correspondence to: Chaomin Shen _<_ cmshen@cs.ecnu.edu.cn _>_ , Yichen Zhu _<_ yichen ~~z~~ hu@foxmail.com _>_ . 

rather than causal drivers. To address this, we propose dWorldEval, an action-centric discretediffusion world model that maps visual observations, language instructions, and action chunks into a shared unified token space and denoises them with a single self-attention backbone where actions function as first-class tokens. To realize reliable policy-world interaction, dWorldEval introduces a sparse keyframe memory that anchors global scene state while preserving finegrained multi-view interaction cues, and leverages Progress-as-text to jointly generate future observations and success indicators. Extensive experiments on LIBERO, RoboTwin, and real-robot tasks demonstrate that dWorldEval significantly outperforms video diffusion baselines in action controllability, stabilizes long-horizon multi-view rollouts, enabling accurate policy ranking via automatic success estimation. 

_Proceedings of the 43_<sup>_rd_</sup> _International Conference on Machine Learning_ , Seoul, South Korea. PMLR 306, 2026. Copyright 2026 by the author(s). 

1 

**Scaling Robot Policy Evaluation via Discrete Diffusion World Model** 

## **1. Introduction** 

While generalist robot manipulation policies have advanced rapidly (Black et al., 2024; Brohan et al., 2023; Kim et al., 2024; Hu et al., 2023; Liu et al., 2025; Physical Intelligence et al., 2025; Kim et al., 2025; Gemini Robotics Team et al., 2025a; Bjorck et al., 2025; Zhao et al., 2025a;b; Zhen et al., 2024), evaluating their capabilities remains a significant challenge. Consequently, generative world models have emerged as a scalable alternative to costly real-world execution or asset-heavy simulations for evaluating robot policies (Li et al., 2025b; Guo et al., 2025b; Quevedo et al., 2025; Gemini Robotics Team et al., 2025b; 1X World Model Team, 2025; Huang et al., 2025; Jiang et al., 2025; Tseng et al., 2025). 

However, world models have not yet become reliable evaluation proxies for robotics policies, primarily because they often fail to accurately reflect robot actions and physical interactions. We attribute these failures to two main causes. First, existing models struggle to generalize to out-of-distribution (OOD) actions. Since they are typically trained on successful demonstrations, they tend to ignore erroneous actions and hallucinate successful outcomes due to a distribution shift. Second, physical inconsistency leads to unrealistic artifacts. For instance, rigid objects may visually warp during contact or vanish entirely due to spatiotemporal inconsistencies. 

While existing works attempt to mitigate this by incorporating failure trajectories, the effectiveness is limited as action coverage is infeasible (Guo et al., 2025b; 1X World Model Team, 2025). We argue that the bottleneck is fundamentally architectural. Most existing approaches adapt architectures originally designed for video generation (e.g., image-to-video models). Since these backbones are not natively designed to take robotic actions as input, actions are merely injected as auxiliary conditions (e.g., via crossattention or adaptive modulation like AdaLN) into the visual denoiser (Li et al., 2025b; Guo et al., 2025b; Quevedo et al., 2025). Given that these backbones are heavily pre-trained on massive video datasets, they inherit strong visual priors. Consequently, action signals act as weak guidance and are frequently overridden by these dominant priors, leading to hallucinated success or spatiotemporal drift. 

Motivated by this, we propose dWorldEval, a world model based on Masked Discrete Diffusion (MDD) (Austin et al., 2021; Sahoo et al., 2024; Lou et al., 2023; Nie et al., 2025; Li et al., 2025a; Yang et al., 2025). Unlike pre-trained video backbones, dWorldEval is trained from scratch on robotic data, treating actions and visual observations as equivalent tokens to ensure action controllability. Specifically, We map visual observations, language instructions, and action chunks into a unified token space, modeling them jointly via a self-attention backbone. To enable reliable policy 

evaluation, we incorporate a sparse keyframe memory that maintains spatiotemporal consistency by mitigating longhorizon drift. Additionally, we introduce a discrete progress token to quantify task completion; by jointly predicting this token with future observations, the model automatically determines success when progress reaches 1. 

In summary, we make three contributions: 

- We propose dWorldEval, a discrete-diffusion world model that significantly enhances action controllability, utilizing sparse keyframe memory to ensure spatiotemporal consistency. 

- We jointly predict visual outcomes and a discrete progress token to enable automatic success detection. 

- We conduct a systematic evaluation on LIBERO (Liu et al., 2023), RoboTwin (Mu et al., 2025), and realworld tasks. Extensive experiments confirm that dWorldEval achieves substantially better action controllability measured by our proposed action-sensitive ∆-LPIPS metric. Furthermore, its estimated success rates correlate strongly with actual execution performance (Pearson _r ≈_ 0 _._ 9), enabling accurate ranking of policies across capabilities. 

## **2. Related Work** 

**World models for policy evaluation.** While policy evaluation has traditionally depended on real-world rollouts (Li et al., 2024; Zhou et al., 2025) or physics-based simulators (Mees et al., 2022; Todorov et al., 2012; Mu et al., 2021; Gu et al., 2023; Xiang et al., 2020; Makoviychuk et al., 2021; Mittal et al., 2023; Yu et al., 2020; Mu et al., 2025; Sferrazza et al., 2024; Grotz et al., 2024; Liu et al., 2023), world models offer a data-driven paradigm to scale policy assessment (Li et al., 2025b; Guo et al., 2025b; Quevedo et al., 2025; Gemini Robotics Team et al., 2025b; 1X World Model Team, 2025; Huang et al., 2025; Jiang et al., 2025; Tseng et al., 2025). However, the utility of current video-based evaluators is severely limited by their lack of reliability. Fundamentally, these architectures treat actions as auxiliary conditions into a visually-dominated denoiser—e.g., via AdaLN modulation in WorldGym (Quevedo et al., 2025) or cross-attention in Ctrl-World (Guo et al., 2025b) and WorldEval (Li et al., 2025b). This design allows strong visual priors to override control signals, causing the model to frequently hallucinate transitions. In contrast, dWorldEval integrates actions as primary tokens within a unified sequence, enabling the generated future states to be directly driven by control signals via self-attention. 

**Discrete diffusion in robotics.** Discrete diffusion language models (DLMs) have emerged as strong alternatives 

2 

**Scaling Robot Policy Evaluation via Discrete Diffusion World Model** 


_Figure 2._ **Overview of dWorldEval. (a) Unified Architecture:** Diverse modalities are flattened into a single sequence, enabling the model to treat visual, control, and semantic tokens uniformly. **(b) Sparse Keyframe Memory:** A history of low-resolution keyframes is used to anchor global spatiotemporal consistency. **(c) Progress-as-text:** The model jointly predicts visual outcomes and discrete progress tokens to enable automatic success detection. 

to autoregressive LLMs, exhibiting competitive generative capabilities while enabling flexible sampling strategies and improved controllability (Austin et al., 2021; Sahoo et al., 2024; Lou et al., 2023; Nie et al., 2025). Recent efforts extend DLM backbones to multimodal understanding and generation, e.g., LaViDa (Li et al., 2025a) and MMaDA (Yang et al., 2025). In robotics, dVLA (Wen et al., 2025a) and related works adapt discrete diffusion to policy learning, formulating action prediction as token inpainting over VLAstyle inputs (Wen et al., 2025a; Liang et al., 2025; Wen et al., 2025c). In contrast to these policy learning approaches, we employ discrete diffusion to build a world model. Our unified token space enables joint prediction of visual observations and progress scores, eliminating the need for external VLMs or reward functions required by prior evaluators (Li et al., 2025b; Quevedo et al., 2025; Guo et al., 2025b). 

## **3. Methodology** 

**Prerequisites for reliability.** To serve as a reliable evaluator, _Wθ_ must satisfy three properties: (1) Action Controllability: predictions must faithfully reflect the visual changes induced by the input actions; (2) Spatiotemporal Consistency: the model must preserve the spatial layout and consistency across long-horizon rollouts via the history context _ht_ ; and (3) Discriminative Task Completion: generated future states must be semantically unambiguous to allow for accurate success detection. 

**Policy evaluation via imagination.** We define an imagined rollout as a closed-loop interaction between a policy _π_ and the world model _Wθ_ , yielding a generated trajectory _τ_ = _{o_ ˆ0 _,_ ˆ _o_ ∆ _, . . . ,_ ˆ _oT }_ . The policy’s performance is evaluated by the imagined success rate _J_ = _N_ <u>1</u> � _Ni_ =1<sup>_S_(</sup><sup>_τi_),</sup> where _S_ ( _·_ ) _∈{_ 0 _,_ 1 _}_ is a success indicator function that judges whether the generated outcome fulfills the task instruction. 

### **3.1. Problem Formulation** 

**World model formulation.** We aim to learn a world model _Wθ_ that serves as a proxy for evaluating robotic manipulation policies. Specifically, given a global language instruction _l_ , a current observation _ot_ , a history _ht_ , and a sequence of future actions **a** _t_ , the model predicts the visual outcome ˆ _ot_ +∆ and a task progress score ˆ _vt_ +∆ _∈_ [0 _,_ 1] at horizon ∆. Essentially, _Wθ_ approximates the joint distribution of future visual dynamics and task completion: (ˆ _ot_ +∆ _,_ ˆ _vt_ +∆) _∼Wθ_ ( _· | ot,_ **a** _t, ht, l_ ). 

### **3.2. World Modeling via Discrete Diffusion** 

### 3.2.1. UNIFIED TOKEN SPACE FOR DIRECT ACTION CONDITIONING 

We employ specialized tokenizers to map each modality into a shared discrete latent space: MAGVIT-v2 (Yu et al., 2023) for RGB observations, the LLaDA tokenizer (Nie et al., 2025) for language instructions, and FAST (Pertsch et al., 2025) for continuous action chunks **a** _t_ . To unify these diverse representations, tokens from different modalities 

3 

**Scaling Robot Policy Evaluation via Discrete Diffusion World Model** 

are mapped into a single index space via fixed offsets and serialized into a flattened sequence. Crucially, rather than processing actions as separate conditions, this joint sequence passes through a unified backbone with bidirectional attention. This design enables visual generation targets to attend directly to action tokens at every layer. We posit that such dense interaction treats actions as tokens of equal standing with visual observations, facilitating finer-grained modeling of action-causal dynamics and ensuring strict action controllability. 

### 3.2.2. SPARSE KEYFRAME MEMORY FOR SPATIOTEMPORAL CONSISTENCY 

To satisfy the spatiotemporal consistency requirement (Sec. 3.1) while balancing context length and computational efficiency, we employ a multi-resolution design conditioned on a sparse keyframe memory. History keyframes are encoded solely from the primary global view (e.g., the top-down view) at a reduced resolution, whereas the current observation retains high-resolution multi-view details. Drawing inspiration from recent multimodal architectures like Seed-1.5VL (Guo et al., 2025a). We further prepend explicit time-index tokens to each keyframe to provide absolute temporal positioning. Functionally, this asymmetry separates responsibilities: the low-resolution history constrains global scene geometry and object permanence, while the high-resolution current context supplies the interaction cues necessary for precise action-causal generation. 

### 3.2.3. PROGRESS-AS-TEXT FOR AUTOMATIC SUCCESS DETECTION 

We formulate task progress estimation as discrete text generation within the unified token space, avoiding separate regression heads. This co-generation of visual outcomes and progress values unifies generative and discriminative capabilities, grounding synthesis in task semantics. During training, we distill supervision from the SEED-1.5VL (Guo et al., 2025a) model. By prompting the VLM to grade visual transitions against task milestones (see Appendix C for prompts and examples), we obtain scores which are then converted into discrete numeric tokens (e.g., “1.0”) and appended to the target sequence. At inference, the generated text tokens are parsed back into a scalar _v_ ˆ _t_ +∆, providing an intrinsic metric for autonomous policy ranking without external oracles. 

### **3.3. Joint Visual-and-Progress Denoising** 

We employ conditional Masked Discrete Diffusion (MDD) to learn _p_ ( **y** _t_ +∆ _|_ **c** _t_ ), where only the target suffix is masked for reconstruction while the context **c** _t_ remains unmasked. 

**Training objective.** Given context **c** _t_ and target **y** _t_ +∆, we sample a diffusion level _λ ∼U_ (0 _,_ 1), and corrupt the target by a mask-based forward process **y** ˜ _t_ +∆ _∼ qλ_ (˜ **y** _|_ **y** _t_ +∆). Let Ω _λ_ = _{j | y_ ˜ _j_ = [MASK] _}_ be the masked index set. We train the model to reconstruct the clean tokens at masked positions: 


where _m_ ( _λ_ ) denotes the masking probability at level _λ_ . and _wj_ is a modality-specific rebalancing weight. 

**Inference.** During evaluation, we employ iterative parallel decoding to sample the target **y** _t_ +∆ conditioned on the unified context **c** _t_ . This process simultaneously recovers the future visual state and its predicted score. 

## **4. Experiments** 

In this section, we evaluate the generative capabilities of dWorldEval and its function as a robot policy evaluator. Specifically, our investigation addresses the following research questions: 

- **(RQ1)** Does dWorldEval strictly adhere to control signals, faithfully rendering execution failures from suboptimal or OOD actions rather than hallucinating outcomes? 

- **(RQ2)** Does the sparse keyframe memory (Sec. 3.2.2) effectively prevent spatiotemporal drift, thereby maintaining long-horizon consistency required for evaluation? 

- **(RQ3)** Can the proposed Progress-as-text mechanism serve as an accurate intrinsic success metric at inference time without external oracles? 

- **(RQ4)** Is dWorldEval a reliable proxy for assessing diverse robot policies? Specifically, does the performance estimated via closed-loop rollouts strongly correlate with real execution and accurately rank policies across different architectures and training stages? 

- **(RQ5)** Are action controllability and spatiotemporal consistency strict prerequisites for policy evaluation? Does the ∆-LPIPS metric effectively diagnose the loss of controllability that leads to unreliable evaluation? 

### **4.1. Experimental Setup** 

**Platforms and data.** We conduct evaluations across three diverse platforms, configuring the training data for each to support world modeling: 

4 

**Scaling Robot Policy Evaluation via Discrete Diffusion World Model** 


_Figure 3._ **Real-world setup and rollout visualization. Left:** The bimanual AgileX platform equipped with three synchronized cameras. **Right:** Result of a failure and a success rollout generated for the _Clean the Table_ task; the insets in the top corners of each frame display the synchronized wrist views. 

**(1) LIBERO** (Liu et al., 2023): We utilize the LIBEROObject, LIBERO-Spatial, LIBERO-Goal, and LIBERO-100 suites, featuring synchronized third-person and wrist views. To enable failure-aware scoring, we augment the 5.5k official expert demonstrations with 1k failed rollouts collected from suboptimal policies. 

**(2) RoboTwin** (Mu et al., 2025): We select the ARX arm configuration to evaluate contact-rich tableware manipulation. The resulting dataset comprises 5.5k trajectories across 10 distinct tasks, ranging from multi-object stacking (e.g., blocks and bowls) to precise pick-and-place operations. 

**(3) Real-world setup** : We deploy a physical bimanual AgileX system, as shown in Figure 3, featuring two 6-DoF arms, and recorded via three synchronized RealSense 457 cameras. Data collection is performed via teleoperation at 50 Hz. The dataset totals 5.2k trajectories (including 1k human-collected failures) across five tasks: Bussing Table, Place Cup, Handover Block, Strike Block and Place Bottles. 

**Baselines and target policies.** We benchmark dWorldEval against video diffusion baselines WorldEval (Li et al., 2025b) and WorldGym (Quevedo et al., 2025), ensuring identical training data splits for fair comparison. And we assess its capabilities across varied policies: multiple training checkpoints of a base policy ( _π_ 0 (Black et al., 2024)) on LIBERO, and heterogeneous architectures (e.g., DexVLA (Wen et al., 2025b), Diffusion Policy (Chi et al., 2025)) across RoboTwin and real-world environments. 

**Implementation details.** All models predict multi-view outcomes at 256<sup>2</sup> resolution, conditioned on a sparse history of _K_ = 4 keyframes (128<sup>2</sup> ). Regarding the loss weights in Eq. 1, we set _wj_ = 2 for progress tokens and _wj_ = 1 for visual tokens. The prediction horizon ∆ aligns with the action chunk length (selected from [2 _,_ 8]). During inference, we employ 16-step iterative parallel decoding. We report success rates averaged over 20 episodes per task for 

simulation benchmarks and 30 episodes for real-world experiments. Evaluating a full trajectory takes approximately 30–90 seconds (1.5s/frame) on a single H800 GPU. 

### **4.2. Evaluating the World Model** 

### 4.2.1. EVALUATING ACTION CONTROLLABILITY 

**Evaluation protocol.** To assess action controllability (RQ1), we employ a protocol on a test set constructed from two distinct interaction types: (1) Expert Success ( _D_ succ): successful trajectories collected from a fully trained policy; (2) Suboptimal Failure ( _D_ fail): failure rollouts collected from undertrained checkpoints. We perform generation conditioned strictly on ground-truth action sequences and evaluate on the shared third-person view. 

**Evaluation metric.** Standard LPIPS captures only static appearance. To explicitly evaluate action controllability, we introduce ∆ **-LPIPS** , which measures the perceptual fidelity of state transitions rather than absolute states. For a fixed stride ∆, we compute difference images ∆ _ot_ = _ot_ +∆ _− ot_ (analogously for predictions ∆ˆ _ot_ ) and define: 


where norm( _·_ ) denotes per-sample RMS normalization for stability. We use ∆LPIPS as our primary indicator for action-conditioned dynamic fidelity (see Sec. 4.4 for further validation of its diagnostic correlation). 

**Experimental results.** As shown in Fig. 4, dWorldEval accurately generates multi-view outcomes for both successful and failure executions. This visual fidelity is quantified in Tab. 1, which exposes a critical divergence: baselines suffer severe degradation on the Failure subset (e.g., WorldGym ∆LPIPS spikes from 0.347 to 0.650), whereas dWorldEval maintains consistent performance. Such stability contrasts with the hallucinations observed in baselines (Fig. 5a). To 

5 

**Scaling Robot Policy Evaluation via Discrete Diffusion World Model** 


_Figure 4._ **Visualization of ground-truth vs. generated multi-view rollouts on RoboTwin** (Mu et al., 2025). **Left/Right** : suboptimal vs. successful execution. **Top/Bottom** : ground-truth simulator rollout vs. dWorldEval prediction, conditioned on identical action sequences. Each sequence displays the initial state followed by synchronized future frames. 


_Figure 5._ **(a) Action-controllability under suboptimal inputs.** We condition all methods on an unseen action sequence and compare their rollouts. While WorldGym (Quevedo et al., 2025) self-corrects the missed grasp into a successful pickup, WorldEval (Li et al., 2025b) hallucinates non-existent objects. In contrast, dWorldEval faithfully reproduces the failure. **(b) Long-horizon round-trip consistency.** We apply a reversible action trajectory: forward actions up to _t_ = _H_ ∆, followed by the corresponding inverse actions to _t_ = 2 _H_ ∆. The full model returns close to the initial observation at _t_ = 0, whereas removing history causes accumulated drift over the round trip. 

_Table 1._ **Action controllability on LIBERO** (Liu et al., 2023). Comparison of LPIPS vs. our dynamic-aware ∆LPIPS on Expert ( _D_ succ) and Failure ( _D_ fail) subsets. Baselines degrade on failure data, while ours remains consistent. 

|METHOD|LPIPS|∆LPI|PS (_↓_)|
|---|---|---|---|
||(_↓_)|EXPERT|FAILURE|
|WORLDEVAL|0.262|0.423|0.701|
|WORLDGYM|0.218|0.347|0.650|
|**OURS**|**0.215**|**0.315**|**0.352**|


_Table 2._ **Long-horizon consistency analysis.** We report the roundtrip LPIPS ( _↓_ ) error, averaged across all synchronized views, over varying horizons _H_ to isolate the impact of memory. Without memory, the model suffers from progressive drift; with memory, spatiotemporal consistency is effectively preserved even at _H_ = 20. 

|METHOD|AC|TIONHO|RIZON|(_H_)|
|---|---|---|---|---|
||5|10|15|20|
|OURS(W/O HISTORY)|0.177|0.186|0.302|0.411|
|**OURS (FULL)**|**0.130**|**0.145**|**0.193**|**0.243**|


4.2.2. EVALUATING SPATIOTEMPORAL CONSISTENCY 

verify these results stem from causal control, we find that randomly shuffling actions (App. B) significantly degrades ∆LPIPS, proving our model is sensitive to the input actions. 

**Evaluation protocol and metrics.** To assess long-horizon stability (RQ2), we employ a variable-horizon round-trip protocol. We perform rollouts of length 2 _H_ by append- 

6 

**Scaling Robot Policy Evaluation via Discrete Diffusion World Model** 


_Figure 6._ **Joint generation enables automatic policy scoring. (a)** At each rollout step, the world model jointly predicts the future observation _o_ ˆ _t_ +∆ and a scalar progress score _v_ ˆ _t_ +∆ _∈_ [0 _,_ 1], which finally indicates task success or failure. **(b)** Success rate estimates across checkpoints of a base policy _π_ 0 (Black et al., 2024) on three LIBERO (Liu et al., 2023) suites. We compare ground-truth execution ( _Real_ ) against evaluations on generated rollouts: human judgment based on the generated observations ( _Human_ ) and automatic evaluation determined by the model’s predicted progress score ( _Auto_ ). 


_Figure 7._ **Correlation between real-execution and world-model success rates.** Scatter plots compare real success rates (x-axis) against generated estimates (y-axis), reporting Pearson correlation _r_ and rank-violation MMRV (lower is better). **(a)** Comparison with video diffusion baselines (WorldEval (Li et al., 2025b), WorldGym (Quevedo et al., 2025)) on LIBERO (Liu et al., 2023) (Single-view). **(b-d)** Ablation studies comparing dWorldEval against its _w/o-history_ variant across diverse settings: **(b)** LIBERO (Multi-view), **(c)** RoboTwin (Mu et al., 2025) with heterogeneous policies ( _π_ 0 (Black et al., 2024), DexVLA (Wen et al., 2025b), DP (Chi et al., 2025)), and **(d)** Real-world tasks. dWorldEval consistently achieves superior correlation and ranking accuracy across all domains. 

ing inverse actions to trajectories of varying lengths _H ∈ {_ 5 _,_ 10 _,_ 15 _,_ 20 _}_ . Consistency is measured via LPIPS between the initial _ot_ and final ˆ _ot_ +2 _H_ . We focus on memory ablation here. Baselines are detailed in Appendix D, as their inability to strictly follow actions renders the round-trip metric unreliable for direct comparison. 

**Experimental results.** Fig. 5(b) visualizes the structural drift isolated by removing memory. This is quantified in Tab. 2: while ablation errors accumulate as _H_ extends to 20, the full model maintains high fidelity, confirming that keyframe memory effectively bounds long-term drift. This stability is vital: Sec. 4.3 shows that drift leads to false negatives, severing the correlation with real-world performance. 

### 4.2.3. JOINT SUBGOAL-AND-PROGRESS PREDICTION ENABLES AUTOMATIC VISUAL GRADING 

**Evaluation protocol.** We leverage the failure-augmented training regime (Sec. 4.1) to validate whether the learned progress tokens can serve as an intrinsic metric (RQ3). We 

evaluate multiple checkpoints of a base policy _π_ 0 across three LIBERO suites and compare three success estimators: (1) **Real** : Ground-truth success rates measured by real execution; (2) **Human (imag.)** : Manual grading of the final generated frame; (3) **Auto (imag.)** : Our proposed automated metric, which classifies an imagined rollout as successful if the final predicted score reaches completion (i.e., ˆ _vT_ +∆ = 1). 

**Experimental results.** As shown in Fig. 6(a), the progress score is discriminative, exhibiting sharp transitions upon task completion. Crucially, Fig. 6(b) demonstrates that Auto (imag.) closely tracks real execution, capturing even non-monotonic fluctuations (e.g., performance dips in later checkpoints). This alignment nearly matches human judgment and confirms that dWorldEval grounds its scoring in visual dynamics rather than monotonic priors, enabling accurate autonomous evaluation. 

7 

**Scaling Robot Policy Evaluation via Discrete Diffusion World Model** 

_Table 3._ **Universal multi-view fidelity.** Quantitative evaluation across diverse platforms (LIBERO (Liu et al., 2023), RoboTwin (Mu et al., 2025), Real-Robot) and synchronized viewpoints. dWorldEval maintains consistent high fidelity (low ∆LPIPS) on both simulation and real-world data. 

|DATASET|VIEWPOINT|LPIPS (_↓_)|∆LPIPS (_↓_)|
|---|---|---|---|
|LIBERO|3RD-PERSON<br>WRIST|0.215<br>0.192|0.324<br>0.303|
|ROBOTWIN|TOP-DOWN<br>WRIST|0.199<br>0.220|0.317<br>0.345|
||TOP-DOWN|0.272|0.365|
|REALWORLD|WRIST|0.254|0.336|


### **4.3. World-Model as a Reliable Proxy for Policy Evaluation** 

To ensure fairness and prevent score-visual misalignment in drifting baselines when addressing RQ4, we determine success strictly based on generated terminal visual states rather than intrinsic scores. 

**Comparison with baselines on LIBERO.** Fig. 7(a) evaluates policy ranking accuracy on LIBERO tasks under the single-view setting. Existing baselines (WorldGym and WorldEval) exhibit weaker correlations and higher rank violations (MMRV up to 0.039) due to insufficient action controllability. In contrast, dWorldEval achieves a strong linear correlation with minimal rank violation (MMRV=0.013), confirming that action-faithful generation is a prerequisite for reliable evaluation. 

**Ranking heterogeneous policies across domains.** We further assess robustness across multi-view settings, heterogeneous architectures (RoboTwin), and physical environments (Real World). As shown in Fig. 7(b-d), the _w/o-history_ ablation suffers from significant performance degradation, particularly in the multi-view setting ( _r_ drops to 0.786). Conversely, dWorldEval effectively anchors spatiotemporal consistency, maintaining high correlations across LIBERO multi-view ( _r_ = 0 _._ 910), RoboTwin ( _r_ = 0 _._ 927), and realworld ( _r_ = 0 _._ 918) tasks, demonstrating superior generalization despite domain gaps and randomized settings. 

### **4.4. More Experiments and Ablation Study** 

**Universal fidelity across diverse platforms.** We provide a comprehensive assessment of visual fidelity across diverse platforms. As detailed in Tab. 3, dWorldEval maintains consistently low ∆LPIPS scores ( _≈_ 0 _._ 31-0 _._ 36) across varying camera configurations and robot morphologies. Notably, the performance in the real-world setup remains comparable to simulation results. This consistency suggests that our unified tokenization is robust against domain gaps, maintaining high fidelity across diverse environments. 

_Table 4._ **Full consistency comparison.** We report the round-trip LPIPS ( _↓_ ) error averaged over varying horizons _H_ . Comparisons with WorldEval (Li et al., 2025b) and WorldGym (Quevedo et al., 2025) demonstrate that our model maintains superior spatiotemporal consistency, whereas baselines suffer from significant drift at longer horizons. 

|MODEL|AC|TIONHO|RIZON(|_H_)|
|---|---|---|---|---|
||5|10|15|20|
|WORLDEVAL|0.216|0.320|0.467|0.531|
|WORLDGYM|0.191|0.224|0.308|0.482|
|**OURS (FULL)**|**0.130**|**0.145**|**0.193**|**0.243**|


_Figure 8._ **Action corruption tests.** Ground-truth action chunks are replaced by chunks from other episodes with probability _p_ . **Left:** ∆LPIPS increases with _p_ , indicating degraded controllability. **Right:** Pearson correlation between real and estimated success rates drops accordingly. 

**Is action-controllability strictly necessary?** To verify this prerequisite and validate ∆-LPIPS as an effective diagnostic metric **(RQ5)** , We apply an inference-time intervention: swapping action chunks with probability _p_ to break alignment while preserving statistics. As shown in Fig. 8, as _p_ increases, ∆LPIPS worsens and the ranking correlation with real success rates degrades precipitously. This diagnostic proves that _only_ in the low-∆LPIPS regime (high controllability) can _Wθ_ accurately preserve policy ordering, confirming that faithful action modeling is the foundational mechanism for evaluation. 

**Comparison of long-horizon consistency.** While Sec. 4.2.2 focused on memory ablation, here we benchmark against video diffusion baselines. As detailed in Tab. 4, baselines exhibit significantly higher errors as the horizon extends. Crucially, we interpret this degradation as a compound failure: since baselines frequently ignore control signals (as established in Sec. 4.2.1), their high LPIPS errors stem not only from spatiotemporal drift but also from insufficient action controllability, where the model fails to follow the inverse trajectory. In contrast, dWorldEval maintains high spatiotemporal consistency. Qualitative visualizations of these failure modes are provided in Appendix D. 

8 

**Scaling Robot Policy Evaluation via Discrete Diffusion World Model** 

## **5. Limitations** 

dWorldEval still has several limitations. Its progress predictor relies on predefined anchor states and VLM-distilled labels, which may not fully cover unconventional but valid solution paths, leading to imperfect intermediate progress estimates. In addition, rare unseen failures, particularly those involving fine contact timing, slippage, occlusion, or boundary-sensitive placements, remain challenging for an image-based world model without explicit contact dynamics. Our current analysis also focuses on success-rate ranking agreement rather than directly measuring whether policies induce identical action distributions under generated and real observations. Finally, the masked discrete diffusion formulation introduces nontrivial inference cost, motivating future work on token pruning, step distillation, speculative decoding, and more physically grounded modeling. 

## **6. Conclusion** 

We presented dWorldEval, a discrete diffusion world model designed to overcome the limitations of existing methods in reliability. Our approach unifies action tokens with sparse keyframe memory to generate consistent long-horizon rollouts, quantified by our proposed ∆LPIPS metric. Extensive experiments confirm that dWorldEval significantly enhances controllability, with predicted success rates that closely track real-world execution. This alignment enables accurate policy ranking across diverse architectures, bringing scalable evaluation closer to practice. 

9 

**Scaling Robot Policy Evaluation via Discrete Diffusion World Model** 

## **Impact Statement** 

This paper presents work whose goal is to advance the field of Machine Learning. There are many potential societal consequences of our work, none which we feel must be specifically highlighted here. 

## **Acknowledgments** 

This work is supported by the Sci-Tech Innovation Initiative by the Science and Technology Commission of Shanghai Municipality (24ZR1419000), the National Science Foundation of China (12471501), and ECNU Multifunctional Platform for Innovation (001). 

## **References** 

- 1X World Model Team. 1X World Model: Evaluating bits, not atoms. Supplementary technical progress report, 1X, 2025. URL https://www.1x.tech/ 1x-world-model.pdf. Contributed by Daniel Ho, Jack Monas, Juntao Ren, and Christina Yu. 

- Austin, J., Johnson, D. D., Ho, J., Tarlow, D., and Van Den Berg, R. Structured denoising diffusion models in discrete state-spaces. _Advances in neural information processing systems_ , 34:17981–17993, 2021. 

- Bjorck, J., Castaneda, F., Cherniadev, N., Da, X., Ding, R.,˜ Fan, L., Fang, Y., Fox, D., Hu, F., Huang, S., et al. GR00T N1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., et al. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Chen, X., Choromanski, K., Ding, T., Driess, D., Dubey, A., Finn, C., et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. _arXiv preprint arXiv:2307.15818_ , 2023. 

- Chi, C., Xu, Z., Feng, S., Cousineau, E., Du, Y., Burchfiel, B., Tedrake, R., and Song, S. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , 44(10-11): 1684–1704, 2025. 

- Gemini Robotics Team, Abeyruwan, S., Ainslie, J., Alayrac, J.-B., Gonzalez Arenas, M., Armstrong, T., Balakrishna, A., Baruch, R., Bauza, M., Blokzijl, M., et al. Gemini Robotics: Bringing AI into the physical world. _arXiv preprint arXiv:2503.20020_ , 2025a. 

- Gemini Robotics Team, Choromanski, K., Devin, C., Du, Y., Dwibedi, D., Gao, R., Jindal, A., Kipf, T., Kirmani, S., Leal, I., et al. Evaluating gemini robotics policies in a veo world simulator. _arXiv preprint arXiv:2512.10675_ , 2025b. 

- Grotz, M., Shridhar, M., Chao, Y.-W., Asfour, T., and Fox, D. Peract2: Benchmarking and learning for robotic bimanual manipulation tasks. In _CoRL 2024 Workshop on Wholebody Control and Bimanual Manipulation: Applications in Humanoids and Beyond_ , 2024. 

- Gu, J., Xiang, F., Li, X., Ling, Z., Liu, X., Mu, T., Tang, Y., Tao, S., Wei, X., Yao, Y., et al. Maniskill2: A unified benchmark for generalizable manipulation skills. _arXiv preprint arXiv:2302.04659_ , 2023. 

- Guo, D., Wu, F., Zhu, F., Leng, F., Shi, G., Chen, H., Fan, H., Wang, J., Jiang, J., Wang, J., et al. Seed1.5-vl technical report. _arXiv preprint arXiv:2505.07062_ , 2025a. 

- Guo, Y., Shi, L. X., Chen, J., and Finn, C. Ctrl-world: A controllable generative world model for robot manipulation. _arXiv preprint arXiv:2510.10125_ , 2025b. 

- Hu, Y., Lin, F., Zhang, T., Yi, L., and Gao, Y. Look before you leap: Unveiling the power of gpt-4v in robotic visionlanguage planning. _arXiv preprint arXiv:2311.17842_ , 2023. 

- Huang, S., Chen, L., Zhou, P., Chen, S., Jiang, Z., Hu, Y., Liao, Y., Gao, P., Li, H., Yao, M., et al. EnerVerse: Envisioning embodied future space for robotics manipulation. _arXiv preprint arXiv:2501.01895_ , 2025. 

- Jiang, Y., Chen, S., Huang, S., Chen, L., Zhou, P., Liao, Y., He, X., Liu, C., Li, H., Yao, M., et al. EnerVerse-AC: Envisioning embodied environments with action condition. _arXiv preprint arXiv:2505.09723_ , 2025. 

- Kim, M., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E., Lam, G., Sanketi, P., Vuong, Q., Kollar, T., Burchfiel, B., Tedrake, R., Sadigh, D., Levine, S., Liang, P., and Finn, C. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- Kim, M. J., Finn, C., and Liang, P. Fine-tuning visionlanguage-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 

- Li, S., Kallidromitis, K., Bansal, H., Gokul, A., Kato, Y., Kozuka, K., Kuen, J., Lin, Z., Chang, K.-W., and Grover, A. Lavida: A large diffusion language model for multimodal understanding. _arXiv preprint arXiv:2505.16839_ , 2025a. 

10 

**Scaling Robot Policy Evaluation via Discrete Diffusion World Model** 

- Li, X., Hsu, K., Gu, J., Pertsch, K., Mees, O., Walke, H. R., Fu, C., Lunawat, I., Sieh, I., Kirmani, S., Levine, S., Wu, J., Finn, C., Su, H., Vuong, Q., and Xiao, T. Evaluating real-world robot manipulation policies in simulation. _arXiv preprint arXiv:2405.05941_ , 2024. 

- Li, Y., Zhu, Y., Wen, J., Shen, C., and Xu, Y. Worldeval: World model as real-world robot policies evaluator. _arXiv preprint arXiv:2505.19017_ , 2025b. 

- Liang, Z., Li, Y., Yang, T., Wu, C., Mao, S., Nian, T., Pei, L., Zhou, S., Yang, X., Pang, J., et al. Discrete diffusion vla: Bringing discrete diffusion to action decoding in vision-language-action policies. _arXiv preprint arXiv:2508.20072_ , 2025. 

- Liu, B., Zhu, Y., Gao, C., Feng, Y., Liu, Q., Zhu, Y., and Stone, P. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791, 2023. 

- Liu, J., Chen, H., An, P., Liu, Z., Zhang, R., Gu, C., Li, X., Guo, Z., Chen, S., Liu, M., et al. Hybridvla: Collaborative diffusion and autoregression in a unified vision-languageaction model. _arXiv preprint arXiv:2503.10631_ , 2025. 

- Lou, A., Meng, C., and Ermon, S. Discrete diffusion modeling by estimating the ratios of the data distribution. _arXiv preprint arXiv:2310.16834_ , 2023. 

- Makoviychuk, V., Wawrzyniak, L., Guo, Y., Lu, M., Storey, K., Macklin, M., Hoeller, D., Rudin, N., Allshire, A., Handa, A., et al. Isaac gym: High performance gpu-based physics simulation for robot learning. _arXiv preprint arXiv:2108.10470_ , 2021. 

- Mees, O., Hermann, L., Rosete-Beas, E., and Burgard, W. Calvin: A benchmark for language-conditioned policy learning for long-horizon robot manipulation tasks. _IEEE Robotics and Automation Letters_ , 7(3):7327–7334, 2022. 

- Mittal, M., Yu, C., Yu, Q., Liu, J., Rudin, N., Hoeller, D., Yuan, J. L., Singh, R., Guo, Y., Mazhar, H., Mandlekar, A., Babich, B., State, G., Hutter, M., and Garg, 

- A. Orbit: A unified simulation framework for interactive robot learning environments. _IEEE Robotics and Automation Letters_ , 8(6):3740–3747, 2023. doi: 10.1109/LRA.2023.3270034. 

- Mu, T., Ling, Z., Xiang, F., Yang, D., Li, X., Tao, S., Huang, Z., Jia, Z., and Su, H. Maniskill: Generalizable manipulation skill benchmark with large-scale demonstrations. _arXiv preprint arXiv:2107.14483_ , 2021. 

- Mu, Y., Chen, T., Chen, Z., Peng, S., Lan, Z., Gao, Z., Liang, Z., Yu, Q., Zou, Y., Xu, M., et al. RoboTwin: Dual-arm robot benchmark with generative digital twins. _arXiv preprint arXiv:2504.13059_ , 2025. 

- Nie, S., Zhu, F., You, Z., Zhang, X., Ou, J., Hu, J., Zhou, J., Lin, Y., Wen, J.-R., and Li, C. Large language diffusion models. _arXiv preprint arXiv:2502.09992_ , 2025. 

- Pertsch, K., Stachowicz, K., Ichter, B., Driess, D., Nair, S., Vuong, Q., Mees, O., Finn, C., and Levine, S. Fast: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 

- Physical Intelligence, Black, K., Brown, N., Darpinian, J., Dhabalia, K., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., et al. _π_ 0 _._ 5: a vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 

- Quevedo, J., Sharma, A. K., Sun, Y., Suryavanshi, V., Liang, P., and Yang, S. Worldgym: World model as an environment for policy evaluation. _arXiv preprint arXiv:2506.00613_ , 2025. 

- Sahoo, S., Arriola, M., Schiff, Y., Gokaslan, A., Marroquin, E., Chiu, J., Rush, A., and Kuleshov, V. Simple and effective masked diffusion language models. _Advances in Neural Information Processing Systems_ , 37:130136– 130184, 2024. 

- Sferrazza, C., Huang, D.-M., Lin, X., Lee, Y., and Abbeel, P. Humanoidbench: Simulated humanoid benchmark for whole-body locomotion and manipulation. _arXiv preprint arXiv:2403.10506_ , 2024. 

- Todorov, E., Erez, T., and Tassa, Y. MuJoCo: A physics engine for model-based control. In _2012 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pp. 5026–5033, 2012. doi: 10.1109/IROS.2012.6386109. 

- Tseng, W.-C., Gu, J., Zhang, Q., Mao, H., Liu, M.-Y., Shkurti, F., and Lin, Y.-C. Scalable policy evaluation with video world models. _arXiv preprint arXiv:2511.11520_ , 2025. 

- Wen, J., Zhu, M., Liu, J., Liu, Z., Yang, Y., Zhang, L., Zhang, S., Zhu, Y., and Xu, Y. dvla: Diffusion visionlanguage-action model with multimodal chain-of-thought. _arXiv preprint arXiv:2509.25681_ , 2025a. 

- Wen, J., Zhu, Y., Li, J., Tang, Z., Shen, C., and Feng, F. DexVLA: Vision-language model with plug-in diffusion expert for general robot control. _arXiv preprint arXiv:2502.05855_ , 2025b. 

- Wen, Y., Li, H., Gu, K., Zhao, Y., Wang, T., and Sun, X. LLaDA-VLA: Vision language diffusion action models. _arXiv preprint arXiv:2509.06932_ , 2025c. 

- Xiang, F., Qin, Y., Mo, K., Xia, Y., Zhu, H., Liu, F., Liu, M., Jiang, H., Yuan, Y., Wang, H., et al. Sapien: A simulated part-based interactive environment. In _Proceedings of the_ 

11 

**Scaling Robot Policy Evaluation via Discrete Diffusion World Model** 

_IEEE/CVF conference on computer vision and pattern recognition_ , pp. 11097–11107, 2020. 

- Yang, L., Tian, Y., Li, B., Zhang, X., Shen, K., Tong, Y., and Wang, M. Mmada: Multimodal large diffusion language models. _arXiv preprint arXiv:2505.15809_ , 2025. 

- Yu, L., Lezama, J., Gundavarapu, N. B., Versari, L., Sohn, K., Minnen, D., Cheng, Y., Birodkar, V., Gupta, A., Gu, X., et al. Language model beats diffusion–tokenizer is key to visual generation. _arXiv preprint arXiv:2310.05737_ , 2023. 

- Yu, T., Quillen, D., He, Z., Julian, R., Hausman, K., Finn, C., and Levine, S. Meta-world: A benchmark and evaluation for multi-task and meta reinforcement learning. In _Conference on robot learning_ , pp. 1094–1100. PMLR, 2020. 

- Zhao, Q., Lu, Y., Kim, M. J., Fu, Z., Zhang, Z., Wu, Y., Li, Z., Ma, Q., Han, S., Finn, C., et al. Cot-vla: Visual chainof-thought reasoning for vision-language-action models. _arXiv preprint arXiv:2503.22020_ , 2025a. 

- Zhao, W., Ding, P., Zhang, M., Gong, Z., Bai, S., Zhao, H., and Wang, D. Vlas: Vision-language-action model with speech instructions for customized robot manipulation. _arXiv preprint arXiv:2502.13508_ , 2025b. 

- Zhen, H., Qiu, X., Chen, P., Yang, J., Yan, X., Du, Y., Hong, Y., and Gan, C. 3d-vla: A 3d vision-language-action generative world model. _arXiv preprint arXiv:2403.09631_ , 2024. 

- Zhou, Z., Atreya, P., Tan, Y. L., Pertsch, K., and Levine, S. Autoeval: Autonomous evaluation of generalist robot manipulation policies in the real world. _arXiv preprint arXiv:2503.24278_ , 2025. 

12 

**Scaling Robot Policy Evaluation via Discrete Diffusion World Model** 

## **A. More on Experimental Setup** 

In this section, we provide further details regarding the task definitions, data collection pipelines, and model hyperparameters used in our experiments. 

### **A.1. Detailed Task Descriptions** 

We evaluate dWorldEval across three domains: Real-World AgileX, RoboTwin (Mu et al., 2025), and LIBERO (Liu et al., 2023). Below we describe the specific task designs and their associated language instructions. 

**Real-World AgileX Tasks** We collected data for five distinct tasks using a bimanual AgileX system. Initial states and corresponding instructions are visualized in Fig. 9. 


_Figure 9._ **Real-World Evaluation Tasks.** We visualize the initial scene observations and corresponding language instructions for the five bimanual manipulation tasks evaluated on the AgileX platform. 

- **Bussing Table.** A long-horizon task requiring the robot to classify and sort multiple objects (tableware, trash) into trays or bins. _Instruction: “Clean the table.”_ 

- **Place Cup.** Precision pick-and-place where the robot must align a cup onto a specific target mat. _Instruction: “Place the empty blue cup to the cup mat.”_ 

- **Handover Block.** A bimanual coordination task involving passing a block from the left arm to the right arm before placement. 

_Instruction: “Pass the red block to the right arm to place it on the blue mat.”_ 

- **Strike Block.** Dynamic tool manipulation that requires grasping a hammer to strike a target block. _Instruction: “Pick up the hammer, then strike the red block.”_ 

- **Dual Bottle Pick.** A synchronization task requiring the robot to simultaneously grasp and lift two bottles positioned in front of it. 

_Instruction: “Pick up one bottle with one arm, and pick up another bottle with the other arm.”_ 

### **Simulation Tasks (RoboTwin & LIBERO)** 

- **RoboTwin Stacking & Placement.** On the RoboTwin benchmark, we utilize the ARX dual-arm configuration to evaluate 10 diverse contact-rich tasks. We categorize these into: (1) **Precision Stacking** , which requires vertical stability and geometry alignment (e.g., Stack Blocks (Three), Stack Bowls (Two & Three)); and (2) **Constrained Placement** , which involves inserting objects into specific receptacles, such as placing Bread (into Basket/Skillet), Cans (into Basket/Pot/Plastic Box), Plate (into Container), and an Empty Cup. These scenarios involve complex inter-object occlusions and fine-grained physics that are challenging for video generation models. 

- **LIBERO Suites.** We utilize four task suites from the LIBERO benchmark: LIBERO-Object, LIBERO-Spatial, LIBERO-Goal, and LIBERO-100. These tasks involve standard tabletop manipulation skills like opening drawers, moving objects around obstacles, and arranging items based on spatial relations. 

13 

**Scaling Robot Policy Evaluation via Discrete Diffusion World Model** 

_Table 5._ **Action-shuffle sanity check.** We permute future action chunks across samples while keeping history and language fixed. Shuffling breaks action–outcome alignment and degrades action-controllability indicators. 

|Conditioning|LPIPS_↓_|∆LPIPS_↓_|
|---|---|---|
|Aligned actions|**0.215**|**0.324**|
|Shuffled actions|0.461|0.697|


### **A.2. Model Implementation Details** 

dWorldEval is initialized from MMaDAVLA-8B, a bidirectional transformer with 32 layers, 32 attention heads, and a hidden dimension of 4096. The model is conditioned on a sparse history of _K_ = 4 keyframes (128 _×_ 128). We use a prediction horizon ∆ consistent with the action chunk size (randomly sampled from [2 _,_ 8]). The loss function balances visual reconstruction and progress prediction with weights _w_ score = 2 and _w_ vis = 1. The model was trained for 15 epochs on 8 H800 GPUs using the AdamW optimizer with a learning rate of 5e-5. We employ a global batch size of 128 (using gradient accumulation). 

## **B. Verifying Causal Dependency via Action Shuffling** 

A faithful action-conditioned world model should depend on the provided future action chunk. If we deliberately destroy the alignment between actions and outcomes, action-controllability indicators should drop accordingly. 

**Experimental Protocol.** Given a test batch of samples _{_ ( _o_<sup>_i_</sup> _t_<sup>_, hi, li, ai, oi_</sup> _t_ +∆<sup>)</sup><sup>_}_</sup> _i_<sup>_B_</sup> =1<sup>, where</sup><sup>_o_</sup> _t_<sup>_i_is the current observation,</sup><sup>_hi_</sup> is the observation history, _l_<sup>_i_</sup> the instruction, and _a_<sup>_i_</sup> the future action chunk, we construct a shuffled action input by permuting action chunks across the batch: _a_ ˜<sup>_i_</sup> _← a_<sup>_π_(</sup><sup>_i_)</sup> with a random permutation _π_ (optionally enforcing _π_ ( _i_ ) _̸_ = _i_ ). We then roll out the world model twice: (i) **Aligned** : _o_ ˆ<sup>_i_</sup> _t_ +∆<sup>_∼Wθ_(</sup><sup>_o_</sup> _t_<sup>_i, hi, li, ai_), (ii)</sup><sup>**Shuffled**:</sup><sup>_o_˜</sup><sup>_i_</sup> _t_ +∆<sup>_∼Wθ_(</sup><sup>_o_</sup> _t_<sup>_i, hi, li,_˜</sup><sup>_ai_).All evaluation</sup> metrics are computed identically under both settings. This perturbation preserves the visual/language marginal distribution while breaking the causal link between actions and future observations. In practice, we implement shuffling by a batch-wise permutation of action chunks, keeping all other inputs unchanged. We repeat the evaluation on the same test set used in Sec. 4.2.1. For clarity, we report the metrics averaged across the entire test set, as the degradation trend is consistent across both distributions. 

**Results.** Tab. 5 shows that shuffling actions consistently degrades action-controllability indicators, confirming that our metric is sensitive to the action input and that the learned dynamics are not explained by static appearance priors alone. 

## **C. VLM Supervision Details** 

We utilize an off-the-shelf VLM (SEED-1.5VL (Guo et al., 2025a)) to generate ground-truth progress scores. Unlike standard zero-shot evaluation, we employ a few-shot In-Context Learning (ICL) strategy to align the model’s scoring distribution with human intuition. For each query, we construct a prompt containing: 

1. A detailed task definition and rigid scoring rules. 

2. Three anchor examples with pre-labeled scores (e.g., 0.2, 0.4, and 0.6) to demonstrate intermediate states. 

3. A batch of query frames (typically 10 frames) to be evaluated independently. 

This batch-processing approach significantly stabilizes the output and enforces strict adherence to the discrete scoring criteria. 

### **C.1. Prompt Template** 

For the Libero-Object (Liu et al., 2023) suite, which primarily involves pick-and-place manipulation, we redefine the scoring criteria to reflect the sequential phases of the action. We employ an few-shot ICL strategy to help the VLM distinguish subtle state changes. 

14 

**Scaling Robot Policy Evaluation via Discrete Diffusion World Model** 


_Figure 10._ **Ground-truth Progress Labels.** Visualization of VLM-annotated scores for the LIBERO-Object (Liu et al., 2023) task _“pick up the alphabet soup and place it in the basket”_ . (a) A successful trajectory exhibits step-wise score increases as milestones are achieved. (b) A failure trajectory effectively reflects incomplete execution, with the score stalling at a low value. 

The system instruction maps the continuous manipulation process into discrete progress steps: 

#### **System Instruction:** 

You are an expert roboticist evaluator. Your task is to judge the completion progress of a robot performing a specific manipulation task (e.g., “pick up the bbq sauce and place it in the basket”). 

**Task Instruction:** _{_ TASK ~~I~~ NSTRUCTION _}_ 

**Scoring Rules (Progress Phases):** The task progress is discretized into the following stages. Please choose the score that best matches the current visual state: 

- **0.0** : _Idle / Start_ . The robot has not yet interacted with the target object. 

- **0.2** : _Approach / Contact_ . The gripper is positioned near the target object or has just made contact, but the object is not yet lifted. 

- **0.4** : _Lifted_ . The object is successfully grasped and lifted off the surface. 

- **0.6** : _In Transit_ . The robot is moving the object towards the target area (mid-trajectory). 

- **0.8** : _Pre-Placement_ . The object is aligned with or hovering just above the target zone, ready for release. 

- **1.0** : _Success_ . The object is stably placed in the target configuration, and the gripper has released it (or the task is fully complete). 

**Important note:** The input frames may appear in random order. You must evaluate each frame independently, strictly based on the visible state in that frame. Do not infer progress from previous frames. 

**Valid outputs:** 0, 0.2, 0.4, 0.6, 0.8, 1.0 **Output Format:** Return only a list of numbers (e.g., [0.2, 0, 0.6, 1.0]). In-Context Examples: We provide 8 distinct examples covering the full range of motion to anchor the scoring: _[Image 1]_ (Start State) _→_ Text: ”Example 1 score: 0.0” _[Image 2]_ (Approaching) _→_ Text: ”Example 2 score: 0.2” _[Image 3]_ (Just Lifted) _→_ Text: ”Example 3 score: 0.4” _[Image 4]_ (Mid-Air Moving) _→_ Text: ”Example 4 score: 0.6” _[Image 5]_ (Approaching Target) _→_ Text: ”Example 5 score: 0.6” _[Image 6]_ (Aligned/Hovering) _→_ Text: ”Example 6 score: 0.8” _[Image 7]_ (Just Released) _→_ Text: ”Example 7 score: 1.0” _[Image 8]_ (Retracting/Done) _→_ Text: ”Example 8 score: 1.0” Text: ”Now evaluate these frames:” 

15 

**Scaling Robot Policy Evaluation via Discrete Diffusion World Model** 


_Figure 11._ **Generated Progress Scores.** Visualization of scores predicted by dWorldEval for the LIBERO-Object (Liu et al., 2023) task _“pick up the ketchup and place it in the basket”_ . (a) The model generates a successful rollout where the score accurately rises to 1.0. (b) The model faithfully predicts a failure case, maintaining a low score consistent with the visual outcome. 

### **C.2. Visualizing Progress Scores: Labels vs. Generation** 

To intuitively demonstrate the effectiveness of our Progress-as-text mechanism, we provide ground-truth annotations and model predictions. Figure 10 illustrates the ground-truth labeling process, where the VLM assigns discrete, step-wise scores (e.g., 0.2, 0.4) corresponding to specific achieved milestones. Complementing this, Figure 11 presents the generated progress scores from dWorldEval during inference. These results confirm that our model accurately learns to associate visual state transitions with the correct progress semantics. 

## **D. Visualizing Baseline Consistency** 

We provide the qualitative visualization corresponding to the round-trip analysis in Sec. 4.4. Figure 12 illustrates the generated rollouts on the LIBERO (Liu et al., 2023) suite with a horizon of _H_ = 20. It can be observed that dWorldEval successfully restores the initial scene structure at the terminal step _t_ = 2 _H_ ∆. In contrast, the baselines (WorldEval and WorldGym) exhibit significant visual deviation from the initial state. This confirms that the high LPIPS errors reported in the main text stem from a compound failure: the baselines struggle not only with spatiotemporal drift (hallucinating objects) but also with strictly adhering to the inverse action sequence required to return to the start. 

## **E. More Visualization** 

In this section, we provide more visualizations for both the simulation and the real-world environment. Figure 13 presents the generated results on the RoboTwin (Mu et al., 2025) benchmark, and Figure 14 shows the real-world cases. 

16 

**Scaling Robot Policy Evaluation via Discrete Diffusion World Model** 


_Figure 12._ **Qualitative comparison of round-trip consistency with baselines.** We visualize the round-trip rollouts ( _H_ = 20) on the LIBERO (Liu et al., 2023) from the shared third-person view. We compare four models: WorldEval (Li et al., 2025b), WorldGym (Quevedo et al., 2025), dWorldEval (W/O History), and dWorldEval (Full). The goal is to return to the initial state at _t_ = 2 _H_ (rightmost column) by executing inverse actions. Ours (Full) successfully restores the initial scene structure. In contrast, baselines and the w/o-history ablation exhibit significant deviation at the end of the trajectory, caused by a combination of spatiotemporal drift and failure to follow the inverse control signals. 

17 

**Scaling Robot Policy Evaluation via Discrete Diffusion World Model** 


_Figure 13._ **Visualization on the RoboTwin benchmark.** (Mu et al., 2025) We compare the ground-truth simulation trajectory with the video generated by our model . Our model synthesizes high-fidelity, synchronized videos across three views (Top-down, Left Wrist, and Right Wrist), accurately preserving the object details and spatial layout of the simulation environment. 

18 

**Scaling Robot Policy Evaluation via Discrete Diffusion World Model** 


_Figure 14._ **Visualization in real-world scenarios.** We compare the ground-truth physical robot execution with the video generated by our model. Given the language instruction, our model synthesizes high-fidelity, synchronized videos across three views (Top-down, Left Wrist, and Right Wrist), accurately preserving object details and handling the visual complexity of the real-world environment. 

19 

