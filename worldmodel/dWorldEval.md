---
title: "dWorldEval: Scalable Robotic Policy Evaluation via Discrete Diffusion World Model"
date: "2026-04-24"
authors: "Yaxuan Li; Zhongyi Zhou; Yefei Chen; Yaokai Xue; Yichen Zhu"
url: https://arxiv.org/abs/2604.22152
pdf: https://arxiv.org/pdf/2604.22152
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2604.22152)** / [論文ページ](https://arxiv.org/abs/2604.22152)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

### **Current Robotics** 


## dWorldEval: Scalable Robotic Policy Evaluation via Discrete Diffusion World Model 

Yaxuan Li<sup>1</sup> , Zhongyi Zhou<sup>1</sup> , Yefei Chen<sup>1</sup> , Yaokai Xue<sup>1</sup> , Yichen Zhu<sup>2</sup> 1Current Robotics, 2University of Toronto 


**Figure 1** dWorldEval is a discrete diffusion world model designed to be controllable and consistent for reliable policy evaluation. It ensures action controllability and spatiotemporal consistency while providing the policy compatibility and faithful progress scoring necessary for accurate, automated policy ranking. 

#### **Abstract** 

Evaluating robotics policies across thousands of environments and thousands of tasks is infeasible with existing approaches. This motivates the need for a new methodology for scalable robotics policy evaluation. In this paper, we propose dWorldEval, which uses a discrete diffusion world model as a scalable evaluation proxy for robotics policies. Specifically, dWorldEval maps all modalities—including vision, language, and robotic actions—into a unified token space, modeling them via a single transformer-based denoising network. In this paper, we propose dWorldEval, using a discrete diffusion world model as a scalable evaluation proxy for robotics policy. Specifically, it maps all modalities, including vision, language, and robotics action into a unified token space, then denoises them with a single transformer network. Building on this architecture, We employ a sparse keyframe memory to maintain spatiotemporal consistency. We also introduce a progress token that indicates the degree of task completion. At inference, the model jointly predicts future observations and progress token, allowing automatically determine success when the progress reaches 1. Extensive experiments demonstrate that dWorldEval significantly outperforms previous approaches, i.e., WorldEval, Ctrl-World, and WorldGym, on LIBERO, RoboTwin, and multiple real-robot tasks. It paves the way for a new architectural paradigm in building world simulators for robotics evaluation at scale. 

**Keywords:** World Model , Robotic Policy Evaluation 

**Date:** April 27, 2026 **Project Page:** `https://dworldeval.github.io/` 

1 

#### **1 Introduction** 

While generalist robot manipulation policies have advanced rapidly [3–5, 12, 14, 16, 17, 24, 36, 47–49], evaluating their capabilities remains a significant challenge. Consequently, generative world models have emerged as a scalable alternative to costly real-world execution or asset-heavy simulations for evaluating robot policies [10, 11, 13, 15, 20, 33, 37, 39]. 

However, world models have not yet become reliable evaluation proxies for robotics policies, primarily because they often fail to accurately reflect robot actions and physical interactions. We attribute these failures to two main causes. First, existing models struggle to generalize to out-of-distribution (OOD) actions. Since they are typically trained on successful demonstrations, they tend to ignore erroneous actions and hallucinate successful outcomes due to a distribution shift. Second, physical inconsistency leads to unrealistic artifacts. For instance, rigid objects may visually warp during contact or vanish entirely due to spatiotemporal inconsistencies. 

While existing works attempt to mitigate this by incorporating failure trajectories, the effectiveness is limited as action coverage is infeasible [10, 11]. We argue that the bottleneck is fundamentally architectural. Most existing approaches adapt architectures originally designed for video generation (e.g., image-to-video models). Since these backbones are not natively designed to take robotic actions as input, actions are merely injected as auxiliary conditions (e.g., via cross-attention or adaptive modulation like AdaLN) into the visual denoiser [10, 20, 33]. Given that these backbones are heavily pre-trained on massive video datasets, they inherit strong visual priors. Consequently, action signals act as weak guidance and are frequently overridden by these dominant priors, leading to hallucinated success or spatiotemporal drift. 

Motivated by this, we propose dWorldEval, a world model based on Masked Discrete Diffusion (MDD) [2, 18, 25, 31, 34, 44]. Unlike pre-trained video backbones, dWorldEval is trained from scratch on robotic data, treating actions and visual observations as equivalent tokens to ensure action controllability. Specifically, We map visual observations, language instructions, and action chunks into a unified token space, modeling them jointly via a self-attention backbone. To enable reliable policy evaluation, we incorporate a sparse keyframe memory that maintains spatiotemporal consistency by mitigating long-horizon drift. Additionally, we introduce a discrete progress token to quantify task completion; by jointly predicting this token with future observations, the model automatically determines success when progress reaches 1. 

In summary, we make three contributions: 

- We propose dWorldEval, a discrete-diffusion world model that significantly enhances action controllability, utilizing sparse keyframe memory to ensure spatiotemporal consistency. 

- We jointly predict visual outcomes and a discrete progress token to enable automatic success detection. 

- We conduct a systematic evaluation on LIBERO [22], RoboTwin [30], and real-world tasks. Extensive experiments confirm that dWorldEval achieves substantially better action controllability measured by our proposed action-sensitive ∆-LPIPS metric. Furthermore, its estimated success rates correlate strongly with actual execution performance (Pearson _r ≈_ 0 _._ 9), enabling accurate ranking of policies across capabilities. 

#### **2 Related Work** 

_World models for policy evaluation._ While policy evaluation has traditionally depended on real-world rollouts [19, 50] or physics-based simulators [7, 8, 22, 26–30, 35, 38, 43, 46], world models offer a data-driven paradigm to scale policy assessment [1, 10, 11, 13, 15, 20, 33, 37, 39]. However, the utility of current videobased evaluators is severely limited by their lack of reliability. Fundamentally, these architectures treat actions as auxiliary conditions into a visually-dominated denoiser—e.g., via AdaLN modulation in WorldGym [33] or cross-attention in Ctrl-World [10] and WorldEval [20]. This design allows strong visual priors to override control signals, causing the model to frequently hallucinate transitions. In contrast, dWorldEval integrates actions as primary tokens within a unified sequence, enabling the generated future states to be directly driven by control signals via self-attention. 

2 


**Figure 2 Overview of dWorldEval. (a) Unified architecture:** Diverse modalities are flattened into a single sequence, enabling the model to treat visual, control, and semantic tokens uniformly. **(b) Sparse keyframe memory:** A history of low-resolution keyframes is used to anchor global spatiotemporal consistency. **(c) Discrete progress token:** The model jointly predicts visual outcomes and discrete progress tokens to enable automatic success detection. 

_Discrete diffusion in robotics._ Discrete diffusion language models (DLMs) have emerged as strong alternatives to autoregressive LLMs, exhibiting competitive generative capabilities while enabling flexible sampling strategies and improved controllability [2, 25, 31, 34]. Recent efforts extend DLM backbones to multimodal understanding and generation, e.g., LaViDa [18] and MMaDA [44]. In robotics, dVLA [40] and related works adapt discrete diffusion to policy learning, formulating action prediction as token inpainting over VLA-style inputs [21, 40, 42]. In contrast to these policy learning approaches, we employ discrete diffusion to build a world model. Our unified token space enables joint prediction of visual observations and progress scores, eliminating the need for external VLMs or reward functions required by prior evaluators [10, 20, 33]. 

#### **3 Methodology** 

##### **3.1 Problem Formulation** 

_World model formulation._ We aim to learn a world model _Wθ_ that serves as a proxy for evaluating robotic policies. Specifically, given a language instruction _l_ , a current observation _ot_ , a history _ht_ , and a sequence of future actions **a** _t_ , the model predicts the visual outcome _o_ ˆ _t_ +∆ and a task progress score _v_ ˆ _t_ +∆ _∈_ [0 _,_ 1] at horizon ∆. Essentially, _Wθ_ approximates the joint distribution of future visual dynamics and task completion: (ˆ _ot_ +∆ _,_ ˆ _vt_ +∆) _∼Wθ_ ( _· | ot,_ **a** _t, ht, l_ ). To serve as a reliable evaluator, _Wθ_ must satisfy three properties: (1) Action controllability: predictions must faithfully reflect the visual changes induced by the input actions; (2) Spatiotemporal consistency: the model must preserve the spatial layout and consistency across long-horizon rollouts; and (3) Discriminative task completion: generated future states must be semantically unambiguous to allow for accurate success detection. 

_Policy evaluation via imagination._ We define an imagined rollout as a closed-loop interaction between a policy _π_ and the world model _Wθ_ , yielding a generated trajectory _τ_ = _{o_ ˆ0 _,_ ˆ _o_ ∆ _, . . . ,_ ˆ _oT }_ . The policy’s performance is evaluated by the imagined success rate _J_ = _N_ <u>1</u> � _Ni_ =1<sup>_S_(</sup><sup>_τi_),where</sup><sup>_S_(</sup><sup>_·_)</sup><sup>_∈{_0</sup><sup>_,_1</sup><sup>_}_isasuccess</sup> indicator function that judges whether the generated outcome fulfills the task instruction. 

##### **3.2 World Modeling via Discrete Diffusion** 

3 


**Figure 3 Real-world setup and rollout visualization. Left:** The bimanual AgileX platform equipped with three synchronized cameras. **Right:** Result of a failure and a success rollout generated for the _Clean the Table_ task; the insets in the top corners of each frame display the synchronized wrist views. 

###### **3.2.1 Action Control via Unified Token Sequence** 

To ensure action controllability, we integrate actions directly into a unified discrete token space, rather than treating them as auxiliary conditions. Specifically, we employ specialized tokenizers to map heterogeneous modalities into discrete codes: MAGVIT-v2 [45] for RGB observations, LLaDA [31] for language, and FAST [32] for continuous action chunks **a** _t_ . By serializing these codes into a single flattened sequence, the transformer can model the joint distribution of actions and observations. Through self-attention, each visual token directly attends to action tokens, enabling fine-grained control at the token level. This allows that generated visual states accurately reflect the input actions. 

###### **3.2.2 Sparse Keyframe Memory for Spatiotemporal Consistency** 

To maintain spatiotemporal consistency, we employ a sparse keyframe memory. The memory is updated via a sliding window that samples the most recent _K_ frames at a fixed stride ∆, aligned with the action chunk size. These sampled keyframes are tokenized and concatenated with other tokens described in Sec. 3.2.1. To explicitly preserve temporal order within this sequence, we encode absolute frame indices as text tokens and prepend them to the corresponding history keyframes [9]. To optimize computational efficiency, we encode history frames at a reduced resolution, utilizing only the fixed global view (e.g., top-down). This setup provides sufficient context for the model while significantly reducing token usage. In contrast, the current observation retains all views at full resolution to capture the fine-grained object interactions required for precise generation. 

###### **3.2.3 Discrete Progress Token for Automatic Success Detection** 

Prior methods decouple success detection from visual generation, incurring additional overhead and potential inconsistency. Instead, our unified token space enables joint generation of visual outcomes and progress scores within a unified latent space, thereby aligning the predicted score with the generated content. During training, we define task-specific milestones and prompt SEED-1.5VL [9] with few-shot examples to estimate task completion progress from visual observations (see Appendix C for details). The resulting scores are converted into discrete tokens (e.g., “1.0”) and appended to the target sequence. At inference, the generated text tokens are decoded into a numeric score _v_ ˆ _t_ +∆, enabling automatic computation of success rate for policy ranking. 

##### **3.3 Joint Visual-and-Progress Denoising** 

We employ Masked Discrete Diffusion (MDD) to learn the transition distribution _p_ ( **y** _t_ +∆ _|_ **c** _t_ ), where the context **c** _t_ remains unmasked while the target suffix is partially masked for reconstruction. Specifically, during training, we sample a diffusion level _λ ∼U_ (0 _,_ 1) and corrupt the target via a mask-based forward process 

4 

**y** ˜ _t_ +∆ _∼ qλ_ (˜ **y** _|_ **y** _t_ +∆). The model is then optimized to reconstruct the clean tokens at the masked indices Ω _λ_ = _{j | y_ ˜ _j_ = `[MASK]` _}_ by minimizing the following weighted objective: 


where _m_ ( _λ_ ) denotes the masking probability at level _λ_ , and _wj_ serves as a modality-specific rebalancing weight. At inference, we use iterative parallel decoding to sample **y** _t_ +∆ conditioned on the unified context **c** _t_ . This process simultaneously generates the future visual state and its progress score. 

#### **4 Experiments** 

In this section, we evaluate the generative capabilities of dWorldEval and its function as an robotic policy evaluator. Specifically, our investigation addresses the following research questions: 

- **(RQ1)** Does dWorldEval strictly adhere to control signals, faithfully rendering execution failures from suboptimal or OOD actions rather than hallucinating outcomes? 

- **(RQ2)** Does the sparse keyframe memory (Sec. 3.2.2) effectively prevent spatiotemporal drift, thereby maintaining long-horizon consistency required for evaluation? 

- **(RQ3)** Can the proposed Progress-as-text mechanism serve as an accurate intrinsic success metric at inference time without external oracles? 

- **(RQ4)** Is dWorldEval a reliable proxy for assessing diverse robot policies? Specifically, does the performance estimated via closed-loop rollouts strongly correlate with real execution and accurately rank policies across different architectures and training stages? 

- **(RQ5)** Can the proposed ∆-LPIPS metric effectively quantify action controllability and serve as a reliable diagnostic indicator for policy evaluation? 

##### **4.1 Experimental Setup** 

**Platforms and data.** We conduct evaluations across three diverse platforms, configuring the training data for each to support world modeling: 

**(1) LIBERO** [23]: We utilize the LIBERO-Object, LIBERO-Spatial, LIBERO-Goal, and LIBERO-100 suites with synchronized third-person and wrist views. To enable failure-aware scoring, we augment the 5.5k official expert demonstrations with 1k failed rollouts from suboptimal policies. 

**(2) RoboTwin** [30]: We select the ARX arm configuration to evaluate contact-rich tableware manipulation, yielding 5.5k trajectories across 10 tasks (e.g., multi-object stacking and precise pick-and-place). 

**(3) Real-world setup** : We deploy a physical bimanual AgileX system (Figure 3) with two 6-DoF arms and three synchronized RealSense 457 cameras. The dataset totals 5.2k trajectories (including 1k human-collected failures) across five tasks: Bussing Table, Place Cup, Handover Block, Strike Block and Place Bottles. 

**Baselines and target policies.** We benchmark dWorldEval against video diffusion baselines including WorldEval [20], WorldGym [33] and Ctrl-World [10]. ensuring identical training data splits for fair comparison. And we assess its capabilities across varied policies: multiple training checkpoints of a base policy ( _π_ 0 [4]) on LIBERO, and heterogeneous architectures (e.g., DexVLA [41], Diffusion Policy [6]) across RoboTwin and real-world environments. 

**Implementation details.** All models predict multi-view outcomes at 256<sup>2</sup> resolution, conditioned on a sparse history of _K_ = 4 keyframes (128<sup>2</sup> ). Regarding the loss weights in Eq. 1, we set _wj_ = 2 for progress tokens and _wj_ = 1 for visual tokens. The prediction horizon ∆ aligns with the action chunk length (selected from [2 _,_ 8]). During inference, we employ 16-step iterative parallel decoding. 

5 


**Figure 4 Visualization of ground-truth vs. generated multi-view rollouts on RoboTwin** [30]. **Left/Right** : suboptimal vs. successful execution. **Top/Bottom** : ground-truth simulator rollout vs. dWorldEval prediction, conditioned on identical action sequences. Each sequence displays the initial state followed by synchronized future frames. 

**Table 1 Action controllability on LIBERO** [23]. Comparison of LPIPS vs. our dynamic-aware ∆LPIPS on Expert ( _D_ succ) and Failure ( _D_ fail) subsets. Baselines degrade on failure data, while ours remains robust. 

|Method|LPIPS|∆LPI|PS (_↓_)|
|---|---|---|---|
||(_↓_)|Expert|Failure|
|WorldEval|0.262|0.423|0.701|
|WorldGym|0.218|0.347|0.650|
|Ctrl-World|0.220|0.334|0.416|
|**Ours**|**0.215**|**0.315**|**0.352**|


**Table 2 Long-horizon consistency analysis.** We report the round-trip LPIPS ( _↓_ ) error, averaged across all synchronized views, over varying horizons _H_ . Without memory, the model suffers from progressive drift; with memory, spatiotemporal consistency is effectively preserved even at _H_ = 20. 

|Method|Act|ion Ho|rizon|(_H_)|
|---|---|---|---|---|
||5|10|15|20|
|Ours (W/O Memory)|0.177|0.186|0.302|0.411|
|**Ours (Full)**|**0.130 **|**0.145**|**0.193 **|**0.243**|


##### **4.2 Evaluating the World Model** 

###### **4.2.1 Evaluating Action Controllability** 

_Evaluation protocol._ To assess action controllability (RQ1), we employ a protocol on a test set constructed from two distinct interaction types: (1) Expert success ( _D_ succ): successful trajectories collected from a fully trained policy; (2) Suboptimal failure ( _D_ fail): failure rollouts collected from undertrained checkpoints. We perform generation conditioned on ground-truth action sequences and evaluate on the shared third-person view. 

**Evaluation metric.** Standard LPIPS captures only static appearance. To explicitly evaluate action controllability, we introduce ∆ **-LPIPS** , which measures the perceptual fidelity of state transitions rather than absolute states. For a fixed stride ∆, we compute difference images ∆ _ot_ = _ot_ +∆ _− ot_ (analogously for predictions ∆ˆ _ot_ ) and define: 


where norm( _·_ ) denotes per-sample RMS normalization for stability. We use ∆LPIPS as our primary indicator for action-conditioned dynamic fidelity (see Sec. 4.4 for further validation of its diagnostic correlation). 

_Experimental results._ This visual fidelity is quantified in Tab. 1, which exposes a critical divergence: baselines suffer severe degradation on the Failure subset (e.g., WorldGym ∆LPIPS spikes from 0.347 to 0.650), whereas dWorldEval maintains consistent performance. This quantitative degradation manifests visually in Fig. 5(a), where baselines frequently fail to adhere to the input actions. To verify these results stem from action controllability, we find that randomly shuffling actions (App. B) significantly degrades ∆LPIPS, proving our model is sensitive to the input actions. 

6 


**Figure 5 (a) Action-controllability under suboptimal inputs.** We condition all methods on an unseen action sequence and compare their rollouts. While WorldGym [20] self-corrects the missed grasp into a successful pickup and WorldEval [20] hallucinates non-existent objects, Ctrl-World [10] fails to align with the input actions. In contrast, dWorldEval faithfully reproduces the failure. **(b) Long-horizon round-trip consistency.** We apply a reversible action trajectory: forward actions up to _t_ = _H_ ∆, followed by the corresponding inverse actions to _t_ = 2 _H_ ∆. The full model returns close to the initial observation at _t_ = 0, whereas removing history causes accumulated drift over the round trip. 

###### **4.2.2 Evaluating Spatiotemporal Consistency** 

_Evaluation protocol and metrics._ To assess long-horizon stability (RQ2), we employ a variable-horizon roundtrip protocol. We perform rollouts of length 2 _H_ by appending inverse actions to trajectories of varying lengths _H ∈{_ 5 _,_ 10 _,_ 15 _,_ 20 _}_ . Consistency is measured via LPIPS between the initial _ot_ and final _o_ ˆ _t_ +2 _H_ . We focus on memory ablation here. Baselines are detailed in Appendix D, as their inability to strictly follow actions renders the round-trip metric unreliable for direct comparison. 

_Experimental results._ Fig. 5(b) visualizes the cumulative drift isolated by removing memory. This is quantified in Tab. 2: while ablation errors accumulate as _H_ extends to 20, the full model maintains high fidelity (LPIPS 0 _._ 21), confirming that keyframe memory effectively bounds long-term drift. This stability is vital: Sec. 4.3 shows that drift leads to false negatives, severing the correlation with real-world performance. 

###### **4.2.3 Joint subgoal-and-progress prediction enables automatic visual grading** 

**Evaluation protocol.** We leverage the failure-augmented training regime (Sec. 4.1) to validate whether the learned progress tokens can serve as an intrinsic metric (RQ3). We evaluate multiple checkpoints of a base policy _π_ 0 across four LIBERO suites and compare three success estimators: (1) **Real** : Ground-truth success rates measured by real execution; (2) **Human (imag.)** : Manual grading of the final generated frame; (3) **Auto (imag.)** : Our proposed automated metric. For each imagined rollout, we examine the predicted progress token _v_ ˆ _T_ at the final time step. The rollout is classified as successful only if this terminal score equals 1. 

_Experimental results._ As shown in Fig. 6(a), the progress score is discriminative, exhibiting sharp transitions upon task completion. Crucially, Fig. 6(b) demonstrates that Auto (imag.) closely tracks real execution, capturing even non-monotonic fluctuations (e.g., performance dips in later checkpoints). This alignment closely matches human judgment. It confirms that dWorldEval bases its score on the actual visual changes, rather than simply assuming progress increases over time. This ensures the reliability of our automatic 

7 


**Figure 6 Joint generation enables automatic policy scoring. (a)** At each rollout step, the world model jointly predicts the future observation _o_ ˆ _t_ +∆ and a scalar progress score _v_ ˆ _t_ +∆ _∈_ [0 _,_ 1], which finally indicates task success or failure. **(b)** Success rate estimates across checkpoints of a base policy _π_ 0 [4] on three LIBERO [23] suites. We compare ground-truth execution ( _Real_ ) against evaluations on generated rollouts: human judgment based on the generated observations ( _Human_ ) and automatic evaluation determined by the model’s predicted progress score ( _Auto_ ). 


**Figure 7 Correlation between real-execution and world-model success rates.** Scatter plots compare real success rates (x-axis) against generated estimates (y-axis), reporting Pearson correlation _r_ and rank-violation MMRV (lower is better). **(a)** Comparison with video diffusion baselines (WorldEval [20], WorldGym [33] and Ctrl-World [10]) on LIBERO [23] (Single-view). **(b-d)** Ablation studies comparing dWorldEval against its _w/o-history_ variant across diverse settings: **(b)** LIBERO (Multi-view), **(c)** Robotwin [30] with heterogeneous policies ( _π_ 0 [4], DexVLA [41], DP [6]), and **(d)** Real-world tasks. dWorldEval consistently achieves superior correlation and ranking accuracy across all domains. 

evaluation. 

##### **4.3 World-Model as a Reliable Proxy for Policy Evaluation** 

For the ablation without memory, the generated video often suffers from severe drift, making the predicted progress token unreliable. To ensure a fair comparison, we ignore the progress and judge success based on the generated image. 

**Comparison with baselines on LIBERO.** Fig. 7(a) evaluates policy ranking accuracy on LIBERO tasks under the single-view setting. Existing baselines (WorldGym, WorldEval and Ctrl-World) exhibit weaker correlations and higher rank violations (MMRV up to 0.039) due to insufficient action controllability. In contrast, dWorldEval achieves a strong linear correlation with minimal rank violation (MMRV=0.013), confirming that action-faithful generation is a prerequisite for reliable evaluation. 

**Ranking heterogeneous policies across domains.** We further assess robustness across multi-view settings, heterogeneous architectures (RoboTwin), and physical environments (Real World). As shown in Fig. 7(bd), the _w/o-history_ ablation suffers from significant performance degradation, particularly in the multi-view setting ( _r_ drops to 0.786). In contrast, by preserving spatiotemporal consistency, dWorldEval achieves high correlations with actual execution success rates across LIBERO multi-view ( _r_ = 0 _._ 910), Robotwin ( _r_ = 0 _._ 927), and real-world ( _r_ = 0 _._ 918) tasks. 

8 

**Table 3 Universal multi-view fidelity.** Quantitative evaluation across diverse platforms (LIBERO [23], RoboTwin [30], Real-Robot) and synchronized viewpoints. dWorldEval maintains consistent high fidelity (low ∆LPIPS) on both simulation and real-world data. 

|Dataset|Viewpoint|LPIPS (_↓_)|∆LPIPS (_↓_)|
|---|---|---|---|
|LIBERO|3rd-Person<br>Wrist|0.215<br>0.192|0.324<br>0.303|
|RT|Top-Down|0.199|0.317|
|obowin|Wrist|0.220|0.345|
|Real World|<sup>Top-Down</sup><br>Wrist|0.272<br>0.254|0.365<br>0.336|


**Table 4 Full consistency comparison.** We report the round-trip LPIPS ( _↓_ ) error averaged over varying horizons _H_ . Comparisons with WorldEval [20], WorldGym [33] and Ctrl-World [10], demonstrate that our model maintains superior spatiotemporal consistency, whereas baselines suffer from significant drift. 

|Model|Ac|tion Ho|rizon|(_H_)|
|---|---|---|---|---|
||5|10|15|20|
|WorldEval|0.216|0.320|0.467|0.531|
|WorldGym|0.191|0.224|0.308|0.482|
|Ctrl-World|0.149|0.233|0.296|0.370|
|**Ours (Full)**|**0.130**|**0.145**|**0.193**|**0.243**|


##### **4.4 More Experiments and Ablation Study** 

**Universal fidelity across diverse platforms.** We provide a comprehensive assessment of visual fidelity across diverse platforms. As detailed in Tab. 3, dWorldEval maintains consistently low ∆LPIPS scores ( _≈_ 0 _._ 31-0 _._ 36) across varying camera configurations and robot morphologies. Notably, the performance in the real-world setup remains comparable to simulation results. This consistency suggests that our unified tokenization is robust against domain gaps, maintaining high fidelity across diverse environments. 

**Comparison of long-horizon consistency.** While Sec. 4.2.2 focused on memory ablation, here we benchmark against video diffusion baselines. As detailed in Tab. 4, baselines suffer from severe inconsistency that worsens as the horizon extends. We interpret this degradation as a compound failure: since baselines frequently ignore control signals (as established in Sec. 4.2.1), their high LPIPS errors stem not only from spatiotemporal drift but also from insufficient action controllability, where the model fails to follow the action sequence. In contrast, dWorldEval maintains high spatiotemporal consistency. Qualitative visualizations of these failure modes are provided in Appendix D. 

#### **5 Conclusion** 

We presented dWorldEval, a discrete diffusion world model designed to overcome the limitations of existing methods in reliability. Our approach unifies action tokens with sparse keyframe memory to generate consistent long-horizon rollouts, quantified by our proposed ∆LPIPS metric. Extensive experiments confirm that dWorldEval significantly enhances controllability, with predicted success rates that closely track real-world execution. This alignment enables accurate policy ranking across diverse architectures, bringing scalable evaluation closer to practice. 

9 

#### **References** 

- [1] 1X Technologies. 1X World Model — 1x.tech. `https://www.1x.tech/discover/1x-world-model` , 2025. [Accessed 16-05-2025]. 

- [2] Jacob Austin, Daniel D Johnson, Jonathan Ho, Daniel Tarlow, and Rianne Van Den Berg. Structured denoising diffusion models in discrete state-spaces. _Advances in neural information processing systems_ , 34:17981–17993, 2021. 

- [3] Johan Bjorck, Fernando Castañeda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- [4] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _π_ 0: A vision-language-action flow model for general robot control, 2024. URL `https://arxiv.org/abs/2410.24164` . 

- [5] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. _arXiv preprint arXiv:2307.15818_ , 2023. 

- [6] Cheng Chi, Siyuan Feng, Yilun Du, Zhenjia Xu, Eric Cousineau, Benjamin Burchfiel, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _arXiv preprint arXiv:2303.04137_ , 2023. 

- [7] Markus Grotz, Mohit Shridhar, Yu-Wei Chao, Tamim Asfour, and Dieter Fox. Peract2: Benchmarking and learning for robotic bimanual manipulation tasks. In _CoRL 2024 Workshop on Whole-body Control and Bimanual Manipulation: Applications in Humanoids and Beyond_ , 2024. 

- [8] Jiayuan Gu, Fanbo Xiang, Xuanlin Li, Zhan Ling, Xiqiang Liu, Tongzhou Mu, Yihe Tang, Stone Tao, Xinyue Wei, Yunchao Yao, et al. Maniskill2: A unified benchmark for generalizable manipulation skills. _arXiv preprint arXiv:2302.04659_ , 2023. 

- [9] Dong Guo, Faming Wu, Feida Zhu, Fuxing Leng, Guang Shi, Haobin Chen, Haoqi Fan, Jian Wang, Jianyu Jiang, Jiawei Wang, et al. Seed1. 5-vl technical report. _arXiv preprint arXiv:2505.07062_ , 2025. 

- [10] Yanjiang Guo, Lucy Xiaoyang Shi, Jianyu Chen, and Chelsea Finn. Ctrl-world: A controllable generative world model for robot manipulation. _arXiv preprint arXiv:2510.10125_ , 2025. 

- [11] D HO, J MONAS, JT REN, and C YU. 1x world model: evaluating bits, not atoms, 2025. 

- [12] Yingdong Hu, Fanqi Lin, Tong Zhang, Li Yi, and Yang Gao. Look before you leap: Unveiling the power of gpt-4v in robotic vision-language planning. _arXiv preprint arXiv:2311.17842_ , 2023. 

- [13] Siyuan Huang, Liliang Chen, Pengfei Zhou, Shengcong Chen, Zhengkai Jiang, Yue Hu, Yue Liao, Peng Gao, Hongsheng Li, Maoqing Yao, et al. Enerverse: Envisioning embodied future space for robotics manipulation. _arXiv preprint arXiv:2501.01895_ , 2025. 

- [14] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. pi0.5: a vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 

- [15] Yuxin Jiang, Shengcong Chen, Siyuan Huang, Liliang Chen, Pengfei Zhou, Yue Liao, Xindong He, Chiming Liu, Hongsheng Li, Maoqing Yao, et al. Enerverse-ac: Envisioning embodied environments with action condition. _arXiv preprint arXiv:2505.09723_ , 2025. 

- [16] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- [17] Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 

10 

- [18] Shufan Li, Konstantinos Kallidromitis, Hritik Bansal, Akash Gokul, Yusuke Kato, Kazuki Kozuka, Jason Kuen, Zhe Lin, Kai-Wei Chang, and Aditya Grover. Lavida: A large diffusion language model for multimodal understanding. _arXiv preprint arXiv:2505.16839_ , 2025. 

- [19] Xuanlin Li, Kyle Hsu, Jiayuan Gu, Karl Pertsch, Oier Mees, Homer Rich Walke, Chuyuan Fu, Ishikaa Lunawat, Isabel Sieh, Sean Kirmani, Sergey Levine, Jiajun Wu, Chelsea Finn, Hao Su, Quan Vuong, and Ted Xiao. Evaluating real-world robot manipulation policies in simulation. _arXiv preprint arXiv:2405.05941_ , 2024. 

- [20] Yaxuan Li, Yichen Zhu, Junjie Wen, Chaomin Shen, and Yi Xu. Worldeval: World model as real-world robot policies evaluator. _arXiv preprint arXiv:2505.19017_ , 2025. 

- [21] Zhixuan Liang, Yizhuo Li, Tianshuo Yang, Chengyue Wu, Sitong Mao, Liuao Pei, Xiaokang Yang, Jiangmiao Pang, Yao Mu, and Ping Luo. Discrete diffusion vla: Bringing discrete diffusion to action decoding in visionlanguage-action policies. _arXiv preprint arXiv:2508.20072_ , 2025. 

- [22] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776– 44791, 2023. 

- [23] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36, 2024. 

- [24] Jiaming Liu, Hao Chen, Pengju An, Zhuoyang Liu, Renrui Zhang, Chenyang Gu, Xiaoqi Li, Ziyu Guo, Sixiang Chen, Mengzhen Liu, et al. Hybridvla: Collaborative diffusion and autoregression in a unified vision-languageaction model. _arXiv preprint arXiv:2503.10631_ , 2025. 

- [25] Aaron Lou, Chenlin Meng, and Stefano Ermon. Discrete diffusion modeling by estimating the ratios of the data distribution. _arXiv preprint arXiv:2310.16834_ , 2023. 

- [26] Viktor Makoviychuk, Lukasz Wawrzyniak, Yunrong Guo, Michelle Lu, Kier Storey, Miles Macklin, David Hoeller, Nikita Rudin, Arthur Allshire, Ankur Handa, et al. Isaac gym: High performance gpu-based physics simulation for robot learning. _arXiv preprint arXiv:2108.10470_ , 2021. 

- [27] Oier Mees, Lukas Hermann, Erick Rosete-Beas, and Wolfram Burgard. Calvin: A benchmark for languageconditioned policy learning for long-horizon robot manipulation tasks. _IEEE Robotics and Automation Letters_ , 7(3):7327–7334, 2022. 

- [28] Mayank Mittal, Calvin Yu, Qinxi Yu, Jingzhou Liu, Nikita Rudin, David Hoeller, Jia Lin Yuan, Ritvik Singh, Yunrong Guo, Hammad Mazhar, Ajay Mandlekar, Buck Babich, Gavriel State, Marco Hutter, and Animesh Garg. Orbit: A unified simulation framework for interactive robot learning environments. _IEEE Robotics and Automation Letters_ , 8(6):3740–3747, 2023. doi: 10.1109/LRA.2023.3270034. 

- [29] Tongzhou Mu, Zhan Ling, Fanbo Xiang, Derek Yang, Xuanlin Li, Stone Tao, Zhiao Huang, Zhiwei Jia, and Hao Su. Maniskill: Generalizable manipulation skill benchmark with large-scale demonstrations. _arXiv preprint arXiv:2107.14483_ , 2021. 

- [30] Yao Mu, Tianxing Chen, Zanxin Chen, Shijia Peng, Zhiqian Lan, Zeyu Gao, Zhixuan Liang, Qiaojun Yu, Yude Zou, Mingkun Xu, et al. Robotwin: Dual-arm robot benchmark with generative digital twins. _arXiv preprint arXiv:2504.13059_ , 2025. 

- [31] Shen Nie, Fengqi Zhu, Zebin You, Xiaolu Zhang, Jingyang Ou, Jun Hu, Jun Zhou, Yankai Lin, Ji-Rong Wen, and Chongxuan Li. Large language diffusion models. _arXiv preprint arXiv:2502.09992_ , 2025. 

- [32] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 

- [33] Julian Quevedo, Ansh Kumar Sharma, Yixiang Sun, Varad Suryavanshi, Percy Liang, and Sherry Yang. Worldgym: World model as an environment for policy evaluation, 2025. _URL https://arxiv. org/abs/2506.00613_ , 2(4):9, 2025. 

- [34] Subham Sahoo, Marianne Arriola, Yair Schiff, Aaron Gokaslan, Edgar Marroquin, Justin Chiu, Alexander Rush, and Volodymyr Kuleshov. Simple and effective masked diffusion language models. _Advances in Neural Information Processing Systems_ , 37:130136–130184, 2024. 

11 

- [35] Carmelo Sferrazza, Dun-Ming Huang, Xingyu Lin, Youngwoon Lee, and Pieter Abbeel. Humanoidbench: Simulated humanoid benchmark for whole-body locomotion and manipulation. _arXiv preprint arXiv:2403.10506_ , 2024. 

- [36] Gemini Robotics Team, Saminda Abeyruwan, Joshua Ainslie, Jean-Baptiste Alayrac, Montserrat Gonzalez Arenas, Travis Armstrong, Ashwin Balakrishna, Robert Baruch, Maria Bauza, Michiel Blokzijl, et al. Gemini robotics: Bringing ai into the physical world. _arXiv preprint arXiv:2503.20020_ , 2025. 

- [37] Gemini Robotics Team, Coline Devin, Yilun Du, Debidatta Dwibedi, Ruiqi Gao, Abhishek Jindal, Thomas Kipf, Sean Kirmani, Fangchen Liu, Anirudha Majumdar, et al. Evaluating gemini robotics policies in a veo world simulator. _arXiv preprint arXiv:2512.10675_ , 2025. 

- [38] Emanuel Todorov, Tom Erez, and Yuval Tassa. Mujoco: A physics engine for model-based control. In _2012 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pages 5026–5033, 2012. doi: 10.1109/ IROS.2012.6386109. 

- [39] Wei-Cheng Tseng, Jinwei Gu, Qinsheng Zhang, Hanzi Mao, Ming-Yu Liu, Florian Shkurti, and Lin Yen-Chen. Scalable policy evaluation with video world models. _arXiv preprint arXiv:2511.11520_ , 2025. 

- [40] Junjie Wen, Minjie Zhu, Jiaming Liu, Zhiyuan Liu, Yicun Yang, Linfeng Zhang, Shanghang Zhang, Yichen Zhu, and Yi Xu. dvla: Diffusion vision-language-action model with multimodal chain-of-thought. _arXiv preprint arXiv:2509.25681_ , 2025. 

- [41] Junjie Wen, Yichen Zhu, Jinming Li, Zhibin Tang, Chaomin Shen, and Feifei Feng. Dexvla: Vision-language model with plug-in diffusion expert for general robot control. _arXiv preprint arXiv:2502.05855_ , 2025. 

- [42] Yuqing Wen, Hebei Li, Kefan Gu, Yucheng Zhao, Tiancai Wang, and Xiaoyan Sun. Llada-vla: Vision language diffusion action models. _arXiv preprint arXiv:2509.06932_ , 2025. 

- [43] Fanbo Xiang, Yuzhe Qin, Kaichun Mo, Yikuan Xia, Hao Zhu, Fangchen Liu, Minghua Liu, Hanxiao Jiang, Yifu Yuan, He Wang, et al. Sapien: A simulated part-based interactive environment. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 11097–11107, 2020. 

- [44] Ling Yang, Ye Tian, Bowen Li, Xinchen Zhang, Ke Shen, Yunhai Tong, and Mengdi Wang. Mmada: Multimodal large diffusion language models. _arXiv preprint arXiv:2505.15809_ , 2025. 

- [45] Lijun Yu, José Lezama, Nitesh B Gundavarapu, Luca Versari, Kihyuk Sohn, David Minnen, Yong Cheng, Vighnesh Birodkar, Agrim Gupta, Xiuye Gu, et al. Language model beats diffusion–tokenizer is key to visual generation. _arXiv preprint arXiv:2310.05737_ , 2023. 

- [46] Tianhe Yu, Deirdre Quillen, Zhanpeng He, Ryan Julian, Karol Hausman, Chelsea Finn, and Sergey Levine. Meta-world: A benchmark and evaluation for multi-task and meta reinforcement learning. In _Conference on robot learning_ , pages 1094–1100. PMLR, 2020. 

- [47] Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli Ma, Song Han, Chelsea Finn, et al. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. _arXiv preprint arXiv:2503.22020_ , 2025. 

- [48] Wei Zhao, Pengxiang Ding, Min Zhang, Zhefei Gong, Shuanghao Bai, Han Zhao, and Donglin Wang. Vlas: Vision-language-action model with speech instructions for customized robot manipulation. _arXiv preprint arXiv:2502.13508_ , 2025. 

- [49] Haoyu Zhen, Xiaowen Qiu, Peihao Chen, Jincheng Yang, Xin Yan, Yilun Du, Yining Hong, and Chuang Gan. 3d-vla: A 3d vision-language-action generative world model. _arXiv preprint arXiv:2403.09631_ , 2024. 

- [50] Zhiyuan Zhou, Pranav Atreya, You Liang Tan, Karl Pertsch, and Sergey Levine. Autoeval: Autonomous evaluation of generalist robot manipulation policies in the real world. _arXiv preprint arXiv:2503.24278_ , 2025. 

12 

# **Appendices** 

#### **A More on Experimental Setup** 

In this section, we provide further details regarding the task definitions, data collection pipelines, and model hyperparameters used in our experiments. 

##### **A.1 Detailed Task Descriptions** 


**Figure 8 Real-World Evaluation Tasks.** We visualize the initial scene observations and corresponding language instructions for the five bimanual manipulation tasks evaluated on the AgileX platform. 

We evaluate dWorldEval across three domains: Real-World AgileX, RoboTwin [30], and [23]. Below we describe the specific task designs and their associated language instructions. 

**Real-World Tasks** We collected data for five distinct tasks using a bimanual AgileX system. Initial states and corresponding instructions are visualized in Fig. 8. 

- **Bussing Table.** A long-horizon task requiring the robot to classify and sort multiple objects (tableware, trash) into trays or bins. _Instruction: “Clean the table.”_ 

- **Place Cup.** Precision pick-and-place where the robot must align a cup onto a specific target mat. _Instruction: “Place the empty blue cup to the cup mat.”_ 

- **Handover Block.** A bimanual coordination task involving passing a block from the left arm to the right arm before placement. _Instruction: “Pass the red block to the right arm to place it on the blue mat.”_ 

- **Strike Block.** Dynamic tool manipulation that requires grasping a hammer to strike a target block. _Instruction: “Pick up the hammer, then strike the red block.”_ 

- **Dual Bottle Pick.** A synchronization task requiring the robot to simultaneously grasp and lift two bottles positioned in front of it. _Instruction: “Pick up one bottle with one arm, and pick up another bottle with the other arm.”_ 

###### **Simulation Tasks** 

- **RoboTwin Stacking & Placement.** On the RoboTwin benchmark, we utilize the ARX dual-arm configuration to evaluate 10 diverse contact-rich tasks. We categorize these into: (1) **Precision Stacking** , which requires vertical stability and geometry alignment (e.g., Stack Blocks (Three), Stack Bowls (Two & Three)); and (2) **Constrained Placement** , which involves inserting objects into specific receptacles, such as placing Bread (into Basket/Skillet), Cans (into Basket/Pot/Plastic Box), Plate (into Container), and an Empty Cup. These scenarios involve complex inter-object occlusions and fine-grained physics that are challenging for video generation models. 

- **LIBERO Suites.** We utilize four task suites from the LIBERO benchmark: LIBERO-Object, LIBEROSpatial, LIBERO-Goal, and LIBERO-100. These tasks involve standard tabletop manipulation skills like opening drawers, moving objects around obstacles, and arranging items based on spatial relations. 

13 


**Figure 9 Action corruption tests.** Ground-truth action chunks are replaced by chunks from other episodes with probability _p_ . **Left:** ∆LPIPS increases with _p_ , indicating degraded controllability. **Right:** Pearson correlation between real and estimated success rates drops accordingly. 

##### **A.2 Model Implementation Details** 

dWorldEval is initialized from MMaDAVLA-8B, a bidirectional transformer with 32 layers, 32 attention heads, and a hidden dimension of 4096. The model is conditioned on a sparse history of _K_ = 4 keyframes (256 _×_ 256). We use a prediction horizon ∆ consistent with the action chunk size (randomly sampled from [2 _,_ 8]. The loss function balances visual reconstruction and progress prediction with weights _w_ score = 2 and _w_ vis = 1. The model was trained for 15 epoch on 8 H800 GPUs using the AdamW optimizer with a learning rate of 5e-5. We employ a global batch size of 128 (using gradient accumulation).We report success rates averaged over 20 episodes per task for simulation benchmarks and 30 episodes for real-world experiments. Evaluating a full trajectory takes approximately 30–90 seconds (1.5s/frame) on a single H800 GPU. 

#### **B Verifying Causal Dependency via Action Shuffling** 

A faithful action-conditioned world model must genuinely depend on the provided future action chunk. If we deliberately destroy the alignment between actions and outcomes, action-controllability indicators should degrade accordingly. 

_Experimental Protocol._ To test this dependency, we disrupt the causal link between actions and future observations while preserving their marginal distributions. Given a test batch _{_ ( _o_<sup>_i_</sup> _t_<sup>_, hi, li, ai, oi_</sup> _t_ +∆<sup>)</sup><sup>_}_</sup> _i_<sup>_B_</sup> =1<sup>,we</sup> replace the true action _a_<sup>_i_</sup> with a randomly assigned _a_ ˜<sup>_i_</sup> _← a_<sup>_π_(</sup><sup>_i_)</sup> via a batch-wise permutation _π_ (enforcing _π_ ( _i_ ) _̸_ = _i_ ). We then roll out the world model under two settings: (i) **Aligned** : _o_ ˆ<sup>_i_</sup> _t_ +∆<sup>_∼Wθ_(</sup><sup>_o_</sup> _t_<sup>_i, hi, li, ai_),and</sup> (ii) **Shuffled** : _o_ ˜<sup>_i_</sup> _t_ +∆<sup>_∼Wθ_(</sup><sup>_o_</sup> _t_<sup>_i, hi, li,_˜</sup><sup>_ai_).Furthermore,toanalyzethecontinuousimpactofmisalignmentand</sup> validate ∆-LPIPS as a diagnostic metric, we introduce an inference-time corruption: swapping action chunks with a tunable probability _p_ . All evaluation metrics are computed identically under these settings on the same test set used in Sec. 4.2.1. 

_Results._ We first examine the complete disruption of action alignment ( _p_ = 1). As shown in Tab. 5, shuffling actions consistently degrades the action-controllability indicators. This confirms that our metrics are highly sensitive to the action input and that the learned dynamics are not simply relying on static appearance priors. 

Building upon this, the probabilistic corruption (0 _≤ p ≤_ 1) reveals a strong correlation between action alignment and evaluation reliability. As illustrated in Fig. 9, increasing the swap probability _p_ worsens ∆- LPIPS, accompanied by a precipitous drop in the ranking correlation with real success rates. This diagnostic demonstrates that accurate policy ranking is only achievable in the low-∆-LPIPS regime, reaffirming that strict adherence to input actions is a prerequisite for reliable evaluation. 

#### **C VLM Supervision Details** 

We utilize an off-the-shelf VLM (SEED-1.5VL [9]) to generate ground-truth progress scores. Unlike standard zero-shot evaluation, we employ a few-shot In-Context Learning (ICL) strategy to align the model’s scoring 

14 

**Table 5 Action-shuffle sanity check.** We permute future action chunks across samples while keeping history and language fixed. Shuffling breaks action–outcome alignment and degrades action-controllability indicators. 

|Conditioning|LPIPS _↓_|∆LPIPS _↓_|
|---|---|---|
|Aligned actions|**0.215**|**0.324**|
|Shuffled actions|0.461|0.697|


distribution with human intuition. For each query, we construct a prompt containing: 

1. A detailed task definition and rigid scoring rules. 

2. Three anchor examples with pre-labeled scores (e.g., 0.2, 0.4, and 0.6) to demonstrate intermediate states. 

3. A batch of query frames (typically 10 frames) to be evaluated independently. 

This batch-processing approach significantly stabilizes the output and enforces strict adherence to the discrete scoring criteria. 

##### **C.1 Prompt Template** 

For the Libero-Object [23] suite, which primarily involves pick-and-place manipulation, we redefine the scoring criteria to reflect the sequential phases of the action. We employ an few-shot ICL strategy to help the VLM distinguish subtle state changes. 

The system instruction maps the continuous manipulation process into discrete progress steps: 

**System Instruction:** 

You are an expert roboticist evaluator. Your task is to judge the completion progress of a robot performing a specific manipulation task (e.g., “pick up the bbq sauce and place it in the basket"). **Task Instruction:** {TASK_INSTRUCTION} 

**Scoring Rules (Progress Phases):** The task progress is discretized into the following stages. Please choose the score that best matches the current visual state: 

- **0.0** : _Idle / Start_ . The robot has not yet interacted with the target object. 

- **0.2** : _Approach / Contact_ . The gripper is positioned near the target object or has just made contact, but the object is not yet lifted. 

- **0.4** : _Lifted_ . The object is successfully grasped and lifted off the surface. 

- **0.6** : _In Transit_ . The robot is moving the object towards the target area (mid-trajectory). 

- **0.8** : _Pre-Placement_ . The object is aligned with or hovering just above the target zone, ready for release. 

- **1.0** : _Success_ . The object is stably placed in the target configuration, and the gripper has released it (or the task is fully complete). 

**Important note:** The input frames may appear in random order. You must evaluate each frame independently, strictly based on the visible state in that frame. Do not infer progress from previous frames. **Valid outputs:** 0, 0.2, 0.4, 0.6, 0.8, 1.0 

**Output Format:** Return only a list of numbers (e.g., [0.2, 0, 0.6, 1.0]). In-Context Examples: We provide 8 distinct examples covering the full range of motion to anchor the scoring: _[Image 1]_ (Start State) _→_ Text: "Example 1 score: 0.0" _[Image 2]_ (Approaching) _→_ Text: "Example 2 score: 0.2" _[Image 3]_ (Just Lifted) _→_ Text: "Example 3 score: 0.4" _[Image 4]_ (Mid-Air Moving) _→_ Text: "Example 4 score: 0.6" _[Image 5]_ (Approaching Target) _→_ Text: "Example 5 score: 0.6" _[Image 6]_ (Aligned/Hovering) _→_ Text: "Example 6 score: 0.8" _[Image 7]_ (Just Released) _→_ Text: "Example 7 score: 1.0" 

15 


**Figure 10 Ground-truth Progress Labels.** Visualization of VLM-annotated scores for the LIBERO-Object [23] task _“pick up the alphabet soup and place it in the basket”_ . (a) A successful trajectory exhibits step-wise score increases as milestones are achieved. (b) A failure trajectory effectively reflects incomplete execution, with the score stalling at a low value. 

_[Image 8]_ (Retracting/Done) _→_ Text: "Example 8 score: 1.0" Text: "Now evaluate these frames:" 

##### **C.2 Visualizing Progress Scores: Labels vs. Generation** 

To intuitively demonstrate the effectiveness of our Progress-as-text mechanism, we provide ground-truth annotations and model predictions. Figure 10 illustrates the ground-truth labeling process, where the VLM assigns discrete, step-wise scores (e.g., 0.2, 0.4) corresponding to specific achieved milestones. Complementing this, Figure 11 presents the generated progress scores from dWorldEval during inference. These results confirm that our model accurately learns to associate visual state transitions with the correct progress semantics. 

#### **D Visualizing Baseline Consistency** 

We provide the qualitative visualization corresponding to the round-trip analysis in Sec. 4.4. Figure 12 illustrates the generated rollouts on the LIBERO [23] suite with a horizon of _H_ = 20. It can be observed that dWorldEval successfully restores the initial scene structure at the terminal step _t_ = 2 _H_ ∆. In contrast, the baselines (WorldEval and WorldGym) exhibit significant visual deviation from the initial state. This confirms that the high LPIPS errors reported in the main text stem from a compound failure: the baselines struggle not only with spatiotemporal drift (hallucinating objects) but also with strictly adhering to the inverse action sequence required to return to the start. 

#### **E More Visualization** 

In this section, we provide more visualizations for both the simulation and the real-world environment. Figure 13 presents the generated results on the RoboTwin [30] benchmark, and Figure 14 shows the real-world cases. 

16 


**Figure 11 Generated Progress Scores.** Visualization of scores predicted by dWorldEval for the LIBERO-Object [23] task _“pick up the ketchup and place it in the basket”_ . (a) The model generates a successful rollout where the score accurately rises to 1.0. (b) The model faithfully predicts a failure case, maintaining a low score consistent with the visual outcome. 

17 


**Figure 12 Qualitative comparison of round-trip consistency with baselines.** We visualize the round-trip rollouts ( _H_ = 20) on the LIBERO [23] from the shared third-person view. We compare four models: WorldEval [20], WorldGym [33], Ctrl-World [10], dWorldEval (W/O History), and dWorldEval (Full). The goal is to return to the initial state at _t_ = 2 _H_ (rightmost column) by executing inverse actions (i.e., reversing the pick-up trajectory to place the object back). Ours (Full) successfully restores the initial scene structure. In contrast, baselines and the w/ohistory ablation exhibit significant deviation at the end of the trajectory, caused by a combination of spatiotemporal drift and failure to follow the inverse control signals. 

18 


**Figure 13 Visualization on the RoboTwin benchmark.** [30] We compare the ground-truth simulation trajectory with the video generated by our model . Our model synthesizes high-fidelity, synchronized videos across three views (Top-down, Left Wrist, and Right Wrist), accurately preserving the object details and spatial layout of the simulation environment. 

19 


**Figure 14 Visualization in real-world scenarios.** We compare the ground-truth physical robot execution with the video generated by our model. Given the language instruction, our model synthesizes high-fidelity, synchronized videos across three views (Top-down, Left Wrist, and Right Wrist), accurately preserving object details and handling the visual complexity of the real-world environment. 

20 

