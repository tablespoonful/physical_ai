---
title: "$π\\mathbf{R}^2$: Reactive Real-time Flow Policies"
date: "2026-07-28"
authors: "Sungjae Park; Shubham Tulsiani"
url: https://arxiv.org/abs/2607.26055
pdf: https://arxiv.org/pdf/2607.26055
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2607.26055)** / [論文ページ](https://arxiv.org/abs/2607.26055)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

_π_ **R**<sup>2</sup> **: Reactive Real-time Flow Policies** 

**Sungjae Park, Shubham Tulsiani** Carnegie Mellon University _{_ `sungjae2, stulsian` _}_ `@andrew.cmu.edu` 

**Abstract:** Generalist manipulation policies increasingly take the form of actionchunking flow policies built on large pretrained backbones. Such chunks run open-loop, so the policy cannot react to sensory input arriving mid-execution, sacrificing _reactivity_ . Replanning more often would restore it, but the perceptionto-action pipeline (a large backbone plus multiple denoising steps) is too slow: this _latency_ forbids frequent replanning and leaves committed actions stale, making such policies ill-suited for dynamic, closed-loop control. We present _π_ **R**<sup>2</sup> , which makes these policies reactive and real-time while retaining large backbones, expressive multi-modal policies, and multi-action prediction. Built on the perposition noise schedule of diffusion forcing, _π_ **R**<sup>2</sup> contributes two ideas. First, it splits conditioning into a fast channel (proprioception, fresh every tick) and an asynchronously updated slow channel (vision-language features), so the policy reacts to proprioception within a chunk while tolerating stale vision. Second, a latency-adaptive flow schedule treats in-flight actions as inpainting conditioning and emits actions in one denoising step per call, letting one trained model adapt to varying hardware latency. Requiring minimal modification to existing architectures, _π_ **R**<sup>2</sup> can be finetuned from a pretrained policy: applied to GR00T-N1.7 on a real xArm6+XHand platform, it replans closed-loop roughly 4 _×_ faster than the base policy (25 Hz on an A5000 GPU), acting on a fresh observation every 40 ms. Across simulation and real-world manipulation tasks, _π_ **R**<sup>2</sup> improves the success rate by up to 23% in simulation and 30% in the real world over the strongest baseline. 

**Project page:** https://pi-r2-flow.github.io/ 

**Keywords:** Reactivity, Real-time Inference, Flow Policies, Robot Foundation Models 

# **1 Introduction** 

We have witnessed remarkable progress in training ‘robotics foundation models’ [1, 2, 3, 4, 5, 6], and three design choices have become ubiquitous across recent efforts. First, **large pre-trained backbones** such as vision-language models (VLMs) [7, 8, 9, 10, 11, 12] are leveraged to process visual (and language) input and extract rich, generalizable representations for downstream action prediction. Second, **expressive policy architectures** such as diffusion [13] and flow matching [14, 15] allow effectively capturing the multi-modal action distributions inherent in diverse human demonstrations. Finally, **action chunking** [16, 17] enables these models to jointly predict multiple actions, providing a richer training signal and improving the temporal consistency of executed actions. 

On the one hand, these choices have been crucial in unlocking generalizable and scalable imitation learning. However, they result in _limited reactivity_ and _increased latency_ , making these foundation models ill-suited for dynamic manipulation tasks that demand fast, smooth, and reactive control. Specifically, the execution of a ‘chunk’ of predicted actions is performed open-loop, without the ability to react to the sensory input streaming in. While the reactivity can in theory be improved by only executing a small ‘sub-chunk’ (in the limit just one action) and re-predicting with updated sensory input, naively doing so is infeasible due to the significant computation required in 


Figure 1: Overview of _π_ **R**<sup>2</sup> . **Top.** While standard diffusion/flow matching relies on stale observations to predict actions via iterative denoising, _π_ **R**<sup>2</sup> disentangles the observation into a fast channel (proprioception) and a slow channel (image encoding, VLM embedding, etc.), and uses up-to-date observations for each denoising step. **Bottom.** To incorporate latency and smooth execution, we adopt an adaptive noise schedule, where the action chunk is divided into three regions: clean actions to be taken during inference, actions with increasing noise level following Diffusion Forcing [18], and pure noise with the same length as clean actions. Compared to Train-Time RTC, this enables faster inference and smoother actions. 

the ‘perception-to-action’ prediction – a large visual (and language) processing backbone followed by multiple denoising iterations for flow matching policy inference. This computational bottleneck coupled with action chunking flow matching thus results in two (related) fundamental limitations: a) reduced reactivity, as a large (sub-)chunk of actions must be executed open-loop while the next chunk is predicted, and b) increased latency, as the predicted actions are a function of ‘stale’ sensory input. 

In this work, we develop _π_ **R**<sup>2</sup> : a framework that allows reactive real-time policy inference _without_ compromising on the design principles of large pre-trained backbones, expressive multi-modal policies, and multi-action prediction. We note that instead of flow (or diffusion) policy inference, which maps uniformly random noise to action chunks over multiple denoising iterations, leveraging the flexible schedule in ‘diffusion forcing’ [18] offers several benefits: a) the immediate actions to be executed can be at a lower noise level and predicted in fewer iterations, and b) different denoising iterations involved in predicting an action can rely on updated sensory input as available. Although prior work has explored diffusion forcing for policy learning [19], we address the key issues that prevent its widespread adoption for robotics foundation models. 

First, while the (immediate) action denoising requires less computation, the backbone ( _e.g.,_ VLM) feature processing becomes the bottleneck for ‘perception-to-action prediction’ latency. Our key insight that allows us to circumvent this bottleneck is that not all input modalities need to be processed at the same rate: proprioceptive signals (joint positions, velocities, torques, and contact forces) can be retrieved and processed orders of magnitude faster than images or text. Moreover, for dynamic tasks, proprioception carries sufficient information for _local_ reactive corrections ( _e.g._ , responding to an unexpected contact or compensating for object slip), while vision and language provide the _global_ context needed to guide coarse motion plans. We thus disentangle the conditioning for action denoising into asynchronously updated ‘slow’ and always up-to-date ‘fast’ features, effectively allowing high-frequency proprioceptive control within an action chunk. Second, despite our asynchronous diffusion forcing, practical constraints (communication delays, GPU bandwidth) often prevent zero latency. We develop a delay-adaptive noise schedule for diffusion forcing that enables seamless 

2 

real-time execution despite latency, allowing the model to continue executing the ‘previous’ actions while ensuring smooth temporally coherent outputs from subsequent denoising iterations. 

Together, these design choices make _π_ **R**<sup>2</sup> roughly 4 _×_ faster than the base policy for closed-loop _replanning_ , achieving 25 Hz with a large-scale VLA (GR00T N1.7 [3]) on A5000 GPUs. Crucially, this means the policy predicts each action using fresh observation every 40 ms, rather than committing to a long action chunk and replanning only sparsely ( _e.g.,_ at _∼_ 7 Hz). _π_ **R**<sup>2</sup> thus matches the reactivity of simple feedforward policies while retaining the expressivity of flow matching, the training benefits of chunk-based inference, and the semantic grounding of pretrained backbones. We first validate _π_ **R**<sup>2</sup> in simulation where we highlight the benefits of increased reactivity and reduced latency compared to the typical action chunking flow policies. We also show how, instead of training from scratch, we can finetune pre-trained VLAs with a diffusion forcing schedule and demonstrate the efficacy of _π_ **R**<sup>2</sup> for complex real-world manipulation tasks, where we find that it improves over the strongest baseline by up to 23% in simulation and 30% in the real world. 

# **2 Related Work** 

**Action Chunking and Flow Policies.** Predicting a _chunk_ of future actions rather than a single action, introduced by ACT [16], improves the temporal coherence of imitation-learned policies and has since become standard, including for mobile and contact-rich manipulation [20, 21]. This design has been widely adopted by expressive multi-modal policies based on diffusion [13] and flow matching [22, 23]. For dynamic tasks, however, committing a (sub-)chunk open-loop is suboptimal, as it cannot react to sensory input arriving mid-execution. While our work also reasons over a chunk of actions, its use of diffusion forcing predicts the immediate actions with lower latency and restores reactivity by conditioning successive denoising iterations on progressively fresher sensory input. 

**Generalist Manipulation Policies.** Foundation robotics models also couple chunked flowmatching action heads with large vision-language backbones, yielding vision-language-action (VLA) models that scale imitation learning across diverse tasks and embodiments [24, 25, 5, 26]. Notable examples include _π_ 0/ _π_ 0 _._ 5 and the dual-system GR00T N1, whose vision-language module feeds a flow-matching action head conditioned on robot proprioception [1, 2, 27]. While this has yielded impressive, generalizable policies, coupling a large backbone with multi-step flow-matching denoising only exacerbates the reactivity problem: the combined per-call latency limits how often the policy can replan. Crucially, this backbone latency would persist even under a diffusion-forcing schedule, since each emitted action still requires a full forward pass through the slow semantic backbone. We instead exploit an asymmetry these models already expose—proprioception is far cheaper to process than vision and language—refreshing proprioceptive conditioning at every control tick while letting the slow vision-language features update asynchronously, making this same class of models reactive. 

**Real-time Execution of Action-Chunking Policies.** The high inference latency of modern VLAs has motivated methods for executing action chunks smoothly while the next prediction is computed [28]. RTC maintains continuity across asynchronous chunks via inference-time inpainting on a frozen action prefix, while Training-Time RTC instead folds this prefix conditioning into training, avoiding the extra inference-time cost [29, 30]. Streaming Diffusion Policy and Streaming Flow Policy emit actions incrementally from a diffusion-forcing-style variable-noise buffer maintained across observations [19, 31]. None, however, address the latency of repeatedly conditioning on a large semantic backbone; Streaming Diffusion Policy, for instance, uses compact visuomotor policies and runs synchronously. Concurrent to our work, FASTER [32] similarly reduces reaction latency in flow-based VLAs via a diffusion-forcing-inspired horizon-aware schedule with action-prefix conditioning, but forwards the backbone once per chunk and conditions all actions on a single fixed observation, improving latency and smoothness without improving reactivity to sensory input arriving during execution. _π_ **R**<sup>2</sup> instead refreshes proprioceptive conditioning within the chunk, reacting to incoming feedback as actions execute while vision-language features update asynchronously. **3** _π_ **R**<sup>2</sup> 

Our goal is to modify existing large-scale flow policies for higher reactivity and lower inference latency. We first review the building blocks – flow matching and diffusion forcing – and then introduce 

3 

two modifications that together yield a real-time, closed-loop flow policy. The modifications require only a flow matching action head conditioned on a heavy pretrained backbone, so they apply equally to world-action models [33, 34, 35, 36]; we instantiate and evaluate on VLAs, the most common member of this family. 

## **3.1 Preliminary** 

## **3.1.1 Flow Matching and Action Chunking Policy** 

We build on flow matching [37, 38] with action chunking [16, 17]. Flow matching learns a velocity field _vθ_ ( **x** _t, t_ ) that transports samples from noise _p_ 0 = _N_ ( **0** _,_ **I** ) to data _p_ 1 = _p_ data along the conditional interpolation **x** _t_ = (1 _−t_ ) **_ϵ_** + _t_ **x** 1, _t ∈_ [0 _,_ 1], trained against the conditional velocity _ut_ ( **x** _t |_ **x** 1) = **x** 1 _−_ **_ϵ_** : 


In the action-chunking policy setting, **x** 1 = ( **a** _t, . . . ,_ **a** _t_ + _H_ ) is a chunk of _H_ future actions conditioned on observation **o** _t_ , generated jointly by _K_ denoising steps; the robot executes the first _h ≤ H_ actions before re-planning. **Crucially, all** _H_ **positions share a single noise level** _t_ **and the chunk is committed open-loop: the** _h_ **executed actions never account for new observations during their execution window** , limiting the reactivity that manipulation tasks demand. 

## **3.1.2 Diffusion Forcing and Streaming Diffusion** 

Diffusion forcing [18, 39] generalizes flow matching by assigning each chunk position _p ∈ {_ 0 _, . . . , H−_ 1 _}_ an independent noise level _τp ∈_ [0 _,_ 1]: 


and the model _vθ_ ( **x** _τ ,_ **_τ_** _,_ **o** ) predicts a per-position velocity. The flexibility of position-dependent noise levels enables _closed-loop_ action prediction by conditioning successive denoising steps on progressively more recent observations within a single chunk. _Streaming diffusion_ [19] is one such instantiation: it imposes a linearly increasing noise schedule across the chunk so that the leading positions are fully denoised within a few steps, and each denoising step incorporates a fresh observation. 

In this work, we also adopt diffusion forcing, focusing on an underexplored regime: enabling largescale flow policies ( _e.g.,_ VLAs) to be more reactive and closed-loop, where large latency naturally arises from its model size and components. The following two subsections present the architectural and scheduling modifications that make diffusion forcing a practical real-time, reactive policy on top of any flow matching action head. 

## **3.2 Proprioception-Reactive Diffusion Forcing** 

A VLA processes the observation **o** _t_ = ( **s** _t,_ **I** _t,_ **T** _t_ ) – proprioception **s** _t_ (joint positions, end-effector pose, _etc._ ), image **I** _t_ , and language **T** _t_ – to predict an action chunk ( **a** _t, . . . ,_ **a** _t_ + _H_ ). Internally, the inputs are preprocessed (dominated by image processing) and passed through the large backbone( _e.g.,_ VLM), producing language-aligned features; proprioception is processed by a small MLP into a state embedding; the DiT action head then conditions on the concatenated representation and runs _K_ denoising steps over the chunk. In practice, these components differ greatly in cost. On RTX A6000 with GR00T-N1.7, image preprocessing + VLM ( _∼_ 60 ms) plus DiT denoising ( _K_ =4 steps, _∼_ 80 ms) sum to _∼_ 140 ms per call – _∼_ 7 control ticks at 50 Hz. This motivates disentangling the slow VLM path from the fast action prediction loop. 

We propose to disentangle the DiT’s conditioning (Fig. 1, left) into a _slow channel_ (vision and language features from the VLM and image/text encoders) and a _fast channel_ (proprioception, fresh every tick). This split mirrors the structure of manipulation itself: vision and language provide coarse spatial and task guidance, while fresh proprioception drives the fine motor refinement that precision demands. Diffusion forcing additionally reduces the per-call denoising work: because 

4 


Figure 2: **Inference cycle, one call.** (a) Buffer at _τ_<sup>_⋆,d_</sup> at the start of the call. (b) One Euler substep (one NFE) shifts the schedule right by _d_ slots: positions [ _d,_ 2 _d_ ) reach _τ_ =1 and are released, and the ramp extends through the back (c) The buffer slides _d_ positions: just-emitted actions become the new front conditioning, _d_ fresh-noise slots ( _τ_ =0) are appended – the schedule reproduces exactly. 

the front of the chunk is kept near _τ_ = 1, a single denoising step per call suffices to produce clean actions at the front (one or more, depending on the schedule; see Sec. 3.3), versus _K_ steps in standard chunked denoising. Combining the two, the DiT action head runs one denoising step against fresh proprioception and a _cached_ slow feature; vision and language are processed asynchronously in a background thread (image preprocessing + VLM forward) and refresh the cache when complete, so the action head conditions on a slow feature of age _d_ vlm ticks (the vision/text wall-clock latency). Per-call cost of the action head is therefore one NFE only, independent of backbone size. 

To absorb the resulting slow-channel staleness, we delay the slow channel at training time by _d_ vlm _∼_ Uniform _{_ 0 _, . . . , d_<sup>max</sup> vlm<sup>_}_andsupplythedelayvaluethroughalearnedembeddingindexed</sup> by the integer delay, added to the slow representation; at deploy time the measured _d_ vlm uses the same embedding. The resulting policy is _proprioception-reactive_ : it reacts to fresh joint state every denoising step while tolerating bounded staleness on vision and language, recovering closed-loop control even behind a large VLA backbone. We refer to this architecture variant as _ProprioceptionReactive Diffusion Forcing_ . 

## **3.3 Latency-Adaptive Flow Schedule** 

By combining diffusion forcing with asynchronous vision/text processing and single-step DiT inference, the per-call delay _d_ of the action prediction loop (distinct from the vision-language staleness _d_ vlm of Sec. 3.2) reduces to one denoising step of the action head. However, in reality, _d_ varies: it depends on each component size and inference GPU, includes network latency when policy and robot run on separate machines (e.g., Ethernet round-trips in remote-inference setups), and fluctuates with computational load and per-call jitter. The policy must therefore handle a range of inference delays _d ∈_ [1 _, d_ max]. 

A naive linearly increasing noise schedule, as in standard streaming diffusion [19], does not address this regime: it implicitly assumes _d_ = 0 (instantaneous inference, no in-flight actions), so when applied at _d >_ 0 the returning chunk can jump at the chunk boundary [29, 40]. We address both issues with a per-position noise schedule parameterized by the inference delay _d_ : a clamped-clean front carries the _d_ in-flight actions as inpaint conditioning, a ramped interior emits _d_ clean actions per call at the cost of one denoising step, and randomizing _d_ at training lets a single model adapt to whatever value is measured at each call. 

**Staircase schedule (Fig. 1, right).** For a target inference delay _d_ , _π_ **R**<sup>2</sup> uses the three-region staircase **_τ_**<sup>_⋆,d_</sup> _∈_ [0 _,_ 1]<sup>_H_</sup> 


with interior slope _s_ = 1 _/_ ( _H−_ 2 _d_ ). Three roles by position: **front** [0 _, d_ ), the in-flight actions, clamped clean as inpaint conditioning; **interior** [ _d, H−d_ ), a linear ramp from clean to noise; **tail** 

5 

[ _H−d, H_ ), the _d_ pure-noise slots appended at the back per cycle. This staircase can be viewed as a diffusion-forcing generalization of training-time RTC [30]: both clamp a clean front of _d_ in-flight actions for inpaint conditioning, but RTC applies a single shared noise level over the remaining _H − d_ positions, whereas the staircase replaces it with a ramped interior plus a pure-noise tail to enable single-step emission under diffusion forcing. 

**Training.** At each batch we sample _d ∼_ Uniform _{_ 1 _, . . . , d_ max _}_ and build **_τ_**<sup>_⋆,d_</sup> . The front _d_ slots are filled by the ground-truth actions and excluded from the loss via _mp_ = **1** [ _p ≥ d_ ] (mirroring inference-time inpaint conditioning); the interior and tail are noised at the staircase levels and contribute to the per-position MSE. We additionally apply symmetric jitter _τp ←_ clip( _τp_ + _δp,_ 0 _,_ 1) with _δp ∼_ Uniform[ _−j, j_ ] to absorb small deviations from the central staircase that arise from percall _d_ variation. With probability _p_ = 0 _._ 2, we instead train on a standard flow schedule (single _τ ∼_ Uniform[0 _,_ 1] shared across positions, no mask), so the same network can also denoise a full chunk from pure noise, used at inference to warm-start the buffer at episode start. **Compatibility with existing flow policy action heads.** The procedure above plugs into any DiTstyle flow matching action with a one-line architectural change: the AdaLN conditioning (which modulates each DiT block by the noise level _τ_ ) becomes per-position, with one ( _γp, βp_ ) pair per chunk position rather than one shared across positions. All other components (attention, MLP, pretrained large backbone, slow/fast feature paths) remain unchanged, so existing pretrained policies, such as VLAs, can be fine-tuned with _π_ **R**<sup>2</sup> without touching the backbone. 

**Inference cycle (Fig. 2).** At episode start we warm up the buffer with standard-flow inference (denoising all _H_ positions from pure noise) and re-noise to match **_τ_**<sup>_⋆,d_</sup> for the initial measured _d_ . From then on, each call applies one denoising step that updates each position by 


with region-dependent per-position advances ∆ _τp_ chosen so the schedule shifts right by _d_ slots: positions [ _d,_ 2 _d_ ) reach _τ_ =1 and are emitted, and the rest of the buffer rotates forward (Fig. 2b). The buffer then slides by _d_ positions, with _d_ fresh-noise slots ( _τ_ =0) appended at the back (Fig. 2c). The schedule reproduces exactly when _d_ holds steady; when _d_ changes between calls the ∆ _τp_ pattern adapts to the new measured _d_ , and the buffer is pulled toward the new **_τ_**<sup>_⋆,d_</sup> over a few calls. 

# **4 Experiments** 

## **4.1 Simulation Experiments** 

**Setup.** We first test _π_ **R**<sup>2</sup> on the Leap Cube Reorientation task in MuJoCo Playground [41], a common task that requires reactivity to keep the cube from falling and to achieve the target cube pose. Demonstrations are collected at 50 Hz from 4 RL experts (different seeds), yielding 200 trajectories total. All methods are trained as state-based flow policies, with prediction chunk length _H_ = 16. We run two studies: an execution-horizon _h_ sweep under zero inference delay (Sec. 4.1.1), and a deployment study under a fixed latency budget (Sec. 4.1.2). 

## **4.1.1 Execution-horizon (** _h_ **) sweep without inference delay** 

We first study the setting where inference delay _d_ = 0, to isolate two things: (i) the tradeoff between task performance and execution horizon _h_ (executing more actions open-loop misses the recent state), and (ii) whether _π_ **R**<sup>2</sup> ’s amortized denoising, where each action’s final denoising step conditions on the most recent observation, matches the reactivity of _h_ =1 flow at a fraction of the per-call cost. At evaluation, standard flow matching uses 16 denoising steps to predict the whole chunk, whereas _π_ **R**<sup>2</sup> uses one denoising step and emits one action at a time. We sweep _h ∈{_ 1 _,_ 2 _,_ 4 _,_ 8 _}_ for standard flow; _π_ **R**<sup>2</sup> emits one action per call ( _h_ = 1, 1 NFE per call). 

**Results.** Results are highlighted in Fig. 3 (left). Intuitively, the performance of standard flow degrades as _h_ grows, confirming the _h_ tradeoff for reactive tasks. Meanwhile, _π_ **R**<sup>2</sup> matches the flow 

6 


Figure 3: Simulation results. **Left.** Without any inference delay, executing a smaller number of actions within the chunk benefits the performance for a flow matching policy. _π_ **R**<sup>2</sup> also achieves the same performance via replanning every timestep, while the only last denoising step is conditioned on up-to-date state. **Right.** When there is an inference delay for each component, _π_ **R**<sup>2</sup> reduces the effective delay _d_ by reducing the number of denoising steps and asynchronously processing the visual features. For each datapoint, _d_ indicates the effective delay of proprioception, while _dv_ is visual delay. We train 3 policies with different seeds for each method and report the mean and std of the success rate. 

configuration of standard flow _h ∈{_ 1 _,_ 2 _}_ . This supports that leveraging fresh observation more frequently is beneficial for such reactive tasks, and amortizing the denoising budget across calls does not sacrifice quality, even though each call costs only one NFE. We next introduce realistic latency and test each deployment regime under that constraint. 

## **4.1.2 Deployment under VLA-level inference delay** 

To consider a realistic latency, we take into account GR00T-N1.7 computation cost (Sec. 3.2: vision/text VLM processing _≈_ 60 ms, _K_ =4 NFE denoising _≈_ 80 ms) and define unit delay _d_ 0 as the _K_ = 4 denoising cost, resulting in vision/text processing _≈_ 0 _._ 75 _d_ 0 and one NFE = _d_ 0 _/_ 4. 

**Baselines.** We compare four methods: (i) _naive-async_ runs the policy inference for predicting the new chunk while executing previous chunk. The inference does not take into account the actions being executed during inference. (ii) _train-time RTC_ [30] explicitly conditions the in-flight actions while predicting the new chunk, resulting in smooth chunk boundaries. (iii) _π_ **R**<sup>2</sup> without asynchronous fast/slow channel processing only applies latency-adaptive flow schedule (Sec. 3.3) without asynchronously processing the fast and slow channel, and (iv) _π_ **R**<sup>2</sup> with asynchronous processing applies all proposed modifications. 

The effective per-call delays are then 1 _._ 75 _d_ 0 (end-to-end inference: _naive-async_ and _train-time RTC_ ), 1 _._ 0 _d_ 0 ( _π_ **R**<sup>2</sup> w/o async), and 0 _._ 25 _d_ 0 ( _π_ **R**<sup>2</sup> w async). Setting _d_ 0 _∈{_ 1 _,_ 2 _,_ 3 _}_ control ticks and ceil-rounding gives effective proprioception delay _d ∈{_ 2 _,_ 4 _,_ 6 _}/{_ 1 _,_ 2 _,_ 3 _}/{_ 1 _,_ 1 _,_ 1 _}_ , respectively. For _π_ **R**<sup>2</sup> with async processing, we additionally delay the object pose by _dvis ∈{_ 1 _,_ 2 _,_ 3 _}._ For all methods, we set execution horizon _h_ = _d_ across all methods. 

**Results.** Fig. 3 (right) reports the mean over three training seeds (error bars show std); for each cell we pick the best epoch per seed. _π_ **R**<sup>2</sup> w/ async wins at every _d_ 0 (0 _._ 43, 0 _._ 42, 0 _._ 45), beating naive-async (0 _._ 33, 0 _._ 29, 0 _._ 22) and Train-time RTC (0 _._ 36, 0 _._ 32, 0 _._ 19) with margins that widen as delay grows. The reason is effective delay: baselines pay _d_ = _⌈_ 1 _._ 75 _d_ 0 _⌉_ per call while _π_ **R**<sup>2</sup> pays _d_ = _d_ 0 (w/o async) or _d_ =1 (w/ async). Async processing lets us hold the action delay at 1 while only the visual delay _d_ vis grows, so performance degrades gracefully with _d_ vis – supporting the view that vision provides coarse guidance while up-to-date proprioception drives manipulation. 

## **4.2 Real World Experiments** 

We now mirror the deployment study above on a real xArm6 + XHand setup by fine-tuning GR00TN1.7 model [27] for dexterous manipulation. Demos are collected at 25 Hz (capped by the teleoperation recording pipeline), so we report _d_ in 25-Hz ticks (1 tick _≈_ 40 ms); We use RTX A5000 

7 


Figure 4: **Real-world manipulation tasks.** Arrows in each image show the desired task outcome. 

Table 1: **Real World Results.** (xArm6 + XHand, fine-tuned GR00T N1.7). _d_ is the measured wall-clock inference delay in 25-Hz control ticks (1 tick _≈_ 40 ms), which is the same as execution horizon _h_ for all methods other than synchronous inference. For each task we report success rate (SR) over _N_ trials and a partial-progress score (Prog) capturing the fraction of subgoals completed <u>per episode.</u> 

||Don’t|Spill|Tidy u|p Book|Inser|t Box|Catch Book|
|---|---|---|---|---|---|---|---|
|Setting|SR|Prog|SR|Prog|SR|Prog|SR|
|Flow, Synchronous (_h_= 10)|4/20|16/80|4/20|9/40|11/20|56/80|4/20|
|Flow, Naive Async, dense, TE [16]|7/20|30/80|7/20|15/40|12/20|61/80|2/20|
|Flow, Train-Time RTC [30]|9/20|45/80|8/20|18/40|10/20|53/80|5/20|
|_π_**R**<sup>2</sup>|**10/20**|**55/80**|**12/20**|**24/40**|**16/20**|**68/80**|**11/20**|


for both training and inference, resulting in _d_ = 4 _∼_ 5 for baselines and _d_ = 1 _∼_ 2 for _π_ **R**<sup>2</sup> . We include arm and hand joint angles, along with hand per-joint torque and fingertip forces in the proprioceptive state. 

**Tasks.** We evaluate our method on four contact-rich dexterous, reactive manipulation tasks, shown in Fig. 4. _Don’t Spill_ requires placing a ball into a bowl and moving the bowl onto a cutting board without dropping the ball. _Tidy Up Book_ requires extracting a book from a pile, grasping it, and placing it into a basket. _Insert Box_ requires pushing a box against a wall to stand it upright before inserting it between a row of books. _Catch Book_ requires the robot reacting to the falling book (induced by the ball hitting the book) and grasping it without dropping it. 

All four tasks demand highly reactive behavior. Picking up the ball requires dynamic grasping, moving the bowl without tilting it relies on proprioceptive feedback, and both extracting a book from a pile and pushing a box upright require precise contact-rich interactions and reactive control. Lastly, catching a book requires the robot to quickly react so that the book stays within its palm. We collect 200, 300, 300, and 100 teleoperated demonstrations for each task, respectively. 

**Baselines.** We compare _π_ **R**<sup>2</sup> against three baselines, all fine-tuned from GR00T-N1.7 with same training budget. (1) _Flow, Synchronous_ stalls the robot for the full _d_ =4 _∼_ 5 ticks while inference runs, then executes the predicted chunk ( _h_ = 10). (2) _Flow, Naive Async (dense, TE)_ [21] runs the policy asynchronously without conditioning on in-flight actions: _dense_ re-issues a query every _d_ ticks (whenever the previous call returns), and _TE_ (temporal ensembling) [16] for overlapping action predictions for the same timestep. (3) _Flow, Train-Time RTC_ [30] additionally trains the policy to inpaint a clean _d_ -action front, anchoring the new chunk to the executed history at the chunk boundary. 

**Results.** Table 1 summarizes the experimental results. _π_ **R**<sup>2</sup> with asynchronous vision–language inference operates near the per-control-tick limit ( _d_ =1 at 25 Hz, with occasional increases to _d_ =2 under network delays), whereas all flow-based baselines incur the full GR00T pipeline latency of _d ∈_ 4 _,_ 5. Synchronous inference produces jittery motion at chunk boundaries because the robot pauses while waiting for the next action chunk, leading to failures such as the ball rolling off the table. Naive asynchronous inference combined with temporal ensembling yields smoother motion but sacrifices execution precision. Train-Time RTC [30] is the strongest baseline; however, _π_ **R**<sup>2</sup> outperforms it 

8 


Figure 5: _π_ **R**<sup>2</sup> **reacts to proprioception, while baselines run a stale plan** ( _Tidy Up Book_ ). Fingertip force (solid, left axis) and the emitted action (dashed, right axis) over time, for _π_ **R**<sup>2</sup> and Train-Time RTC; numbered markers link plot times to the overhead frames above. _π_ **R**<sup>2</sup> grips just enough ( _∼_ 50 N), while RTC reacts late and over-grips to _∼_ 120 N, dropping the book. 

across all metrics, with the largest gains on reactivity-critical tasks such as Tidy Up Book, Insert Box, and Catch Book, achieving approximately 20 _∼_ 30% absolute improvement. We observe that RTC also struggles to recover from failures because previously generated in-flight actions bias the policy toward continuing its recent motion, which reduces its ability to react promptly, particularly in Insert Box. Qualitatively, _π_ **R**<sup>2</sup> produces smoother and more accurate motions, even during failure recovery. These results demonstrate the value of the real-time proprioceptive feedback enabled by _π_ **R**<sup>2</sup> . 

**Reactivity analysis.** Fig. 5 plots a fingertip contact force against the action each method emits over time on _Tidy Up Book_ . Because _π_ **R**<sup>2</sup> refreshes proprioception at every denoising step, it modulates its grip from live force feedback and stops near _∼_ 50 N, gripping just enough to reorient the book. Train-Time RTC instead commits to a stale plan and reacts late, so it keeps pushing down after contact, and its middle-finger force overshoots to _∼_ 120 N, crushing the book. This force modulation is the mechanism behind our quantitative gains: reacting to contact as it happens rather than after the current chunk finishes. Tmaihe same pattern holds in all remaining tasks (Appendix A.4). 

# **5 Discussion** 

We presented _π_ **R**<sup>2</sup> , a principled modification to existing VLA architectures that yields real-time, closed-loop policies through two orthogonal contributions: asynchronous vision/text processing that decouples the slow VLM backbone from the action loop, and a latency-adaptive flow schedule that absorbs variable inference delay via a per-position noise schedule parameterized by _d_ . Together, they reduce per-call delay by up to 4 _×_ while remaining compatible with any VLA action head. This enables _π_ **R**<sup>2</sup> to handle highly reactive behaviors – non-prehensile, contact-rich manipulation – where baselines struggle, both in simulation and on real hardware. 

# **Limitations** 

Our approach has several limitations. First, we do not address sources of latency external to the model itself, such as communication delays between the inference server and the robot client. Second, we keep the base policy architecture unchanged; designing it to emphasize proprioceptive features more strongly (e.g., dedicated attention heads for proprioceptive tokens) could further amplify reactivity, and we leave this direction to future work. 

9 

# **Acknowledgements** 

We appreciate the helpful discussions with CISCO, Tony Tao, Andrew Wang, Jason Liu, and Yuxuan Kuang. We also thank Yishu Li, Kallol Saha, and Soumojit Bhattacharya for helping real-world experiments. Lastly, we thank Hyeonwoo Kim for the feedback on website design. This work was supported by gift awards from CISCO, Google, and NSF Award IIS-2442282. 

# **References** 

- [1] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter, et al. _π_ 0: A vision-language-action flow model for general robot control. In _RSS_ , 2025. 

- [2] P. Intelligence, K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, M. Y. Galliker, D. Ghosh, L. Groom, K. Hausman, B. Ichter, S. Jakubczak, T. Jones, L. Ke, D. LeBlanc, S. Levine, A. Li-Bell, M. Mothukuri, S. Nair, K. Pertsch, A. Z. Ren, L. X. Shi, L. Smith, J. T. Springenberg, K. Stachowicz, J. Tanner, Q. Vuong, H. Walke, A. Walling, H. Wang, L. Yu, and U. Zhilinsky. _π_ 0 _._ 5: a vision-language-action model with open-world generalization, 2025. URL `https://arxiv.org/abs/2504.16054` . 

- [3] J. Bjorck, F. Casta˜neda, N. Cherniadev, X. Da, R. Ding, L. Fan, Y. Fang, D. Fox, F. Hu, S. Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- [4] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, J. Dabis, C. Finn, K. Gopalakrishnan, K. Hausman, A. Herzog, J. Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. In _RSS_ , 2023. 

- [5] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _CoRL_ , 2023. 

- [6] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi, et al. Openvla: An open-source vision-language-action model. In _CoRL_ , 2024. 

- [7] H. Liu, C. Li, Q. Wu, and Y. J. Lee. Visual instruction tuning. _Advances in neural information processing systems_ , 36:34892–34916, 2023. 

- [8] J.-B. Alayrac, J. Donahue, P. Luc, A. Miech, I. Barr, Y. Hasson, K. Lenc, A. Mensch, K. Millican, M. Reynolds, et al. Flamingo: a visual language model for few-shot learning. _Advances in neural information processing systems_ , 35:23716–23736, 2022. 

- [9] S. Bai, Y. Cai, R. Chen, K. Chen, X. Chen, Z. Cheng, L. Deng, W. Ding, C. Gao, C. Ge, et al. Qwen3-vl technical report. _arXiv preprint arXiv:2511.21631_ , 2025. 

- [10] G. Team, R. Anil, S. Borgeaud, J.-B. Alayrac, J. Yu, R. Soricut, J. Schalkwyk, A. M. Dai, A. Hauth, K. Millican, et al. Gemini: a family of highly capable multimodal models. _arXiv preprint arXiv:2312.11805_ , 2023. 

- [11] L. Beyer, A. Steiner, A. S. Pinto, A. Kolesnikov, X. Wang, D. Salz, M. Neumann, I. Alabdulmohsin, M. Tschannen, E. Bugliarello, T. Unterthiner, D. Keysers, S. Koppula, F. Liu, A. Grycner, A. Gritsenko, N. Houlsby, M. Kumar, K. Rong, J. Eisenschlos, R. Kabra, M. Bauer, M. Boˇsnjak, X. Chen, M. Minderer, P. Voigtlaender, I. Bica, I. Balazevic, J. Puigcerver, P. Papalampidi, O. Henaff, X. Xiong, R. Soricut, J. Harmsen, and X. Zhai. Paligemma: A versatile 3b vlm for transfer, 2024. URL `https://arxiv.org/abs/2407.07726` . 

10 

- [12] M. Deitke, C. Clark, S. Lee, R. Tripathi, Y. Yang, J. S. Park, M. Salehi, N. Muennighoff, K. Lo, L. Soldaini, J. Lu, T. Anderson, E. Bransom, K. Ehsani, H. Ngo, Y. Chen, A. Patel, M. Yatskar, C. Callison-Burch, A. Head, R. Hendrix, F. Bastani, E. VanderBilt, N. Lambert, Y. Chou, A. Chheda, J. Sparks, S. Skjonsberg, M. Schmitz, A. Sarnat, B. Bischoff, P. Walsh, C. Newell, P. Wolters, T. Gupta, K.-H. Zeng, J. Borchardt, D. Groeneveld, C. Nam, S. Lebrecht, C. Wittlif, C. Schoenick, O. Michel, R. Krishna, L. Weihs, N. A. Smith, H. Hajishirzi, R. Girshick, A. Farhadi, and A. Kembhavi. Molmo and pixmo: Open weights and open data for state-ofthe-art vision-language models, 2024. URL `https://arxiv.org/abs/2409.17146` . 

- [13] C. Chi, Z. Xu, S. Feng, E. Cousineau, Y. Du, B. Burchfiel, R. Tedrake, and S. Song. Diffusion policy: Visuomotor policy learning via action diffusion. In _IJRR_ , 2023. 

- [14] C. Yuan, C. Wen, T. Zhang, and Y. Gao. General flow as foundation affordance for scalable robot learning. _arXiv preprint arXiv:2401.11439_ , 2024. 

- [15] C. Pan, G. Anantharaman, N.-C. Huang, C. Jin, D. Pfrommer, C. Yuan, F. Permenter, G. Qu, N. Boffi, G. Shi, et al. Much ado about noising: Dispelling the myths of generative robotic control. _arXiv preprint arXiv:2512.01809_ , 2025. 

- [16] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn. Learning fine-grained bimanual manipulation with low-cost hardware. _arXiv preprint arXiv:2304.13705_ , 2023. 

- [17] T. T. Zhang, D. Pfrommer, C. Pan, N. Matni, and M. Simchowitz. Action chunking and exploratory data collection yield exponential improvements in behavior cloning for continuous control. _arXiv preprint arXiv:2507.09061_ , 2025. 

- [18] B. Chen, D. Mart´ı Mons´o, Y. Du, M. Simchowitz, R. Tedrake, and V. Sitzmann. Diffusion forcing: Next-token prediction meets full-sequence diffusion. _Advances in Neural Information Processing Systems_ , 37:24081–24125, 2024. 

- [19] S. H. Høeg, Y. Du, and O. Egeland. Streaming diffusion policy: Fast policy synthesis with variable noise diffusion models. _arXiv preprint arXiv:2406.04806_ , 2024. 

- [20] Z. Fu, T. Z. Zhao, and C. Finn. Mobile aloha: Learning bimanual mobile manipulation with low-cost whole-body teleoperation, 2024. URL `https://arxiv.org/abs/2401.02117` . 

- [21] T. Z. Zhao, J. Tompson, D. Driess, P. Florence, K. Ghasemipour, C. Finn, and A. Wahid. Aloha unleashed: A simple recipe for robot dexterity. _arXiv preprint arXiv:2410.13126_ , 2024. 

- [22] Q. Zhang, Z. Liu, H. Fan, G. Liu, B. Zeng, and S. Liu. Flowpolicy: Enabling fast and robust 3d flow-based policy via consistency flow matching for robot manipulation, 2024. URL `https: //arxiv.org/abs/2412.04987` . 

- [23] G. Yan, J. Zhu, Y. Deng, S. Yang, R.-Z. Qiu, X. Cheng, M. Memmel, R. Krishna, A. Goyal, X. Wang, and D. Fox. Maniflow: A general robot manipulation policy via consistency flow training, 2025. URL `https://arxiv.org/abs/2509.01819` . 

- [24] O. X.-E. Collaboration, A. O’Neill, A. Rehman, A. Gupta, A. Maddukuri, A. Gupta, A. Padalkar, A. Lee, A. Pooley, A. Gupta, A. Mandlekar, A. Jain, A. Tung, A. Bewley, A. Herzog, A. Irpan, A. Khazatsky, A. Rai, A. Gupta, A. Wang, A. Kolobov, A. Singh, A. Garg, A. Kembhavi, A. Xie, A. Brohan, A. Raffin, A. Sharma, A. Yavary, A. Jain, A. Balakrishna, A. Wahid, B. Burgess-Limerick, B. Kim, B. Sch¨olkopf, B. Wulfe, B. Ichter, C. Lu, C. Xu, C. Le, C. Finn, C. Wang, C. Xu, C. Chi, C. Huang, C. Chan, C. Agia, C. Pan, C. Fu, C. Devin, D. Xu, D. Morton, D. Driess, D. Chen, D. Pathak, D. Shah, D. B¨uchler, D. Jayaraman, D. Kalashnikov, D. Sadigh, E. Johns, E. Foster, F. Liu, F. Ceola, F. Xia, F. Zhao, F. V. Frujeri, F. Stulp, G. Zhou, G. S. Sukhatme, G. Salhotra, G. Yan, G. Feng, G. Schiavi, G. Berseth, G. Kahn, G. Yang, G. Wang, H. Su, H.-S. Fang, H. Shi, H. Bao, H. B. Amor, H. I. Christensen, H. Furuta, H. Bharadhwaj, H. Walke, H. Fang, H. Ha, I. Mordatch, I. Radosavovic, I. Leal, J. Liang, J. Abou-Chakra, J. Kim, J. Drake, J. Peters, J. Schneider, J. Hsu, 

11 

   - J. Vakil, J. Bohg, J. Bingham, J. Wu, J. Gao, J. Hu, J. Wu, J. Wu, J. Sun, J. Luo, J. Gu, J. Tan, J. Oh, J. Wu, J. Lu, J. Yang, J. Malik, J. Silv´erio, J. Hejna, J. Booher, J. Tompson, J. Yang, J. Salvador, J. J. Lim, J. Han, K. Wang, K. Rao, K. Pertsch, K. Hausman, K. Go, K. Gopalakrishnan, K. Goldberg, K. Byrne, K. Oslund, K. Kawaharazuka, K. Black, K. Lin, K. Zhang, K. Ehsani, K. Lekkala, K. Ellis, K. Rana, K. Srinivasan, K. Fang, K. P. Singh, K.-H. Zeng, K. Hatch, K. Hsu, L. Itti, L. Y. Chen, L. Pinto, L. Fei-Fei, L. Tan, L. J. Fan, L. Ott, L. Lee, L. Weihs, M. Chen, M. Lepert, M. Memmel, M. Tomizuka, M. Itkina, M. G. Castro, M. Spero, M. Du, M. Ahn, M. C. Yip, M. Zhang, M. Ding, M. Heo, M. K. Srirama, M. Sharma, M. J. Kim, M. Z. Irshad, N. Kanazawa, N. Hansen, N. Heess, N. J. Joshi, N. Suenderhauf, N. Liu, N. D. Palo, N. M. M. Shafiullah, O. Mees, O. Kroemer, O. Bastani, P. R. Sanketi, P. T. Miller, P. Yin, P. Wohlhart, P. Xu, P. D. Fagan, P. Mitrano, P. Sermanet, P. Abbeel, P. Sundaresan, Q. Chen, Q. Vuong, R. Rafailov, R. Tian, R. Doshi, R. Mart’in-Mart’in, R. Baijal, R. Scalise, R. Hendrix, R. Lin, R. Qian, R. Zhang, R. Mendonca, R. Shah, R. Hoque, R. Julian, S. Bustamante, S. Kirmani, S. Levine, S. Lin, S. Moore, S. Bahl, S. Dass, S. Sonawani, S. Tulsiani, S. Song, S. Xu, S. Haldar, S. Karamcheti, S. Adebola, S. Guist, S. Nasiriany, S. Schaal, S. Welker, S. Tian, S. Ramamoorthy, S. Dasari, S. Belkhale, S. Park, S. Nair, S. Mirchandani, T. Osa, T. Gupta, T. Harada, T. Matsushima, T. Xiao, T. Kollar, T. Yu, T. Ding, T. Davchev, T. Z. Zhao, T. Armstrong, T. Darrell, T. Chung, V. Jain, V. Kumar, V. Vanhoucke, V. Guizilini, W. Zhan, W. Zhou, W. Burgard, X. Chen, X. Chen, X. Wang, X. Zhu, X. Geng, X. Liu, X. Liangwei, X. Li, Y. Pang, Y. Lu, Y. J. Ma, Y. Kim, Y. Chebotar, Y. Zhou, Y. Zhu, Y. Wu, Y. Xu, Y. Wang, Y. Bisk, Y. Dou, Y. Cho, Y. Lee, Y. Cui, Y. Cao, Y.-H. Wu, Y. Tang, Y. Zhu, Y. Zhang, Y. Jiang, Y. Li, Y. Li, Y. Iwasawa, Y. Matsuo, Z. Ma, Z. Xu, Z. J. Cui, Z. Zhang, Z. Fu, and Z. Lin. Open X-Embodiment: Robotic learning datasets and RT-X models. `https://arxiv.org/abs/2310.08864` , 2023. 

- [25] A. Khazatsky, K. Pertsch, S. Nair, A. Balakrishna, S. Dasari, S. Karamcheti, S. Nasiriany, M. K. Srirama, L. Y. Chen, K. Ellis, et al. Droid: A large-scale in-the-wild robot manipulation dataset. In _RSS_ , 2024. 

- [26] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- [27] NVIDIA, :, J. Bjorck, F. Casta˜neda, N. Cherniadev, X. Da, R. Ding, L. J. Fan, Y. Fang, D. Fox, F. Hu, S. Huang, J. Jang, Z. Jiang, J. Kautz, K. Kundalia, L. Lao, Z. Li, Z. Lin, K. Lin, G. Liu, E. Llontop, L. Magne, A. Mandlekar, A. Narayan, S. Nasiriany, S. Reed, Y. L. Tan, G. Wang, Z. Wang, J. Wang, Q. Wang, J. Xiang, Y. Xie, Y. Xu, Z. Xu, S. Ye, Z. Yu, A. Zhang, H. Zhang, Y. Zhao, R. Zheng, and Y. Zhu. Gr00t n1: An open foundation model for generalist humanoid robots, 2025. URL `https://arxiv.org/abs/2503.14734` . 

- [28] H. Xie, B. Wen, J. Zheng, Z. Chen, F. Hong, H. Diao, and Z. Liu. Dynamicvla: A visionlanguage-action model for dynamic object manipulation. _arXiv preprint arXiv:2601.22153_ , 2026. 

- [29] K. Black, M. Galliker, and S. Levine. Real-time execution of action chunking flow policies. _Advances in Neural Information Processing Systems_ , 38:33383–33407, 2026. 

- [30] K. Black, A. Z. Ren, M. Equi, and S. Levine. Training-time action conditioning for efficient real-time chunking. _arXiv preprint arXiv:2512.05964_ , 2025. 

- [31] S. Jiang, X. Fang, N. Roy, T. Lozano-P´erez, L. P. Kaelbling, and S. Ancha. Streaming flow policy: Simplifying diffusion/flow-matching policies by treating action trajectories as flow trajectories, 2025. URL `https://arxiv.org/abs/2505.21851` . 

- [32] Y. Lu, Z. Liu, X. Fan, Z. Yang, J. Hou, J. Li, K. Ding, and H. Zhao. Faster: Rethinking real-time flow vlas, 2026. URL `https://arxiv.org/abs/2603.19199` . 

12 

- [33] S. Ye, Y. Ge, K. Zheng, S. Gao, S. Yu, G. Kurian, S. Indupuru, Y. L. Tan, C. Zhu, J. Xiang, et al. World action models are zero-shot policies. _arXiv preprint arXiv:2602.15922_ , 2026. 

- [34] M. J. Kim, Y. Gao, T.-Y. Lin, Y.-C. Lin, Y. Ge, G. Lam, P. Liang, S. Song, M.-Y. Liu, C. Finn, et al. Cosmos policy: Fine-tuning video models for visuomotor control and planning. In _ICLR_ , 2026. 

- [35] S. Li, Y. Gao, D. Sadigh, and S. Song. Unified video action model. In _RSS_ , 2025. 

- [36] C. Zhu, R. Yu, S. Feng, B. Burchfiel, P. Shah, and A. Gupta. Unified world models: Coupling video and action diffusion for pretraining on large robotic datasets. In _RSS_ , 2025. 

- [37] Y. Lipman, R. T. Chen, H. Ben-Hamu, M. Nickel, and M. Le. Flow matching for generative modeling. _arXiv preprint arXiv:2210.02747_ , 2022. 

- [38] F. Zhang and M. Gienger. Affordance-based robot manipulation with flow matching. _arXiv preprint arXiv:2409.01083_ , 2024. 

- [39] K. Song, B. Chen, M. Simchowitz, Y. Du, R. Tedrake, and V. Sitzmann. History-guided video diffusion. _arXiv preprint arXiv:2502.06764_ , 2025. 

- [40] J. Tang, Y. Sun, Y. Zhao, S. Yang, Y. Lin, Z. Zhang, J. Hou, Y. Lu, Z. Liu, and S. Han. Vlash: Real-time vlas via future-state-aware asynchronous inference. _arXiv preprint arXiv:2512.01031_ , 2025. 

- [41] K. Zakka, B. Tabanpour, Q. Liao, M. Haiderbhai, S. Holt, J. Y. Luo, A. Allshire, E. Frey, K. Sreenath, L. A. Kahrs, et al. Mujoco playground. _arXiv preprint arXiv:2502.08844_ , 2025. 

- [42] E. Perez, F. Strub, H. De Vries, V. Dumoulin, and A. Courville. Film: Visual reasoning with a general conditioning layer. In _Proceedings of the AAAI conference on artificial intelligence_ , volume 32, 2018. 

13 

# **A Implementation Details** 

## **A.1 Simulation** 

**Task.** The Leap Cube Reorientation task in MuJoCo Playground [41] requires a 16-DoF Leap Hand to orient a cube without dropping it from the palm. We modify the original environment in two ways: we raise the control rate from 20 Hz to 50 Hz to enable more reactive control, and we restrict the goal distribution to four _blue side up_ yaw poses _{_ 0 _, π/_ 2 _, π,_ 3 _π/_ 2 _}_ rather than uniformly random goals. An episode succeeds if the cube reaches any of the four goals within 0 _._ 2 rad in 600 steps; we report the success rate over 100 episodes. 


Figure 6: **Leap Cube Reorientation goals.** The Leap Hand grasps a cube and must rotate it until the blue face points up at one of four target yaw poses (0<sup>_◦_</sup> _,_ 90<sup>_◦_</sup> _,_ 180<sup>_◦_</sup> _,_ 270<sup>_◦_</sup> ). The bottom caption shows the corresponding goal quaternions ( _w, x, y, z_ ). 

**Dataset.** Four PPO experts (different seeds) generate 50 trajectories each, 200 total at 50 Hz. The simulator injects per-step sensing noise into the observation, sampled independently for each component: uniform noise in [ _−_ 0 _._ 05 _,_ 0 _._ 05] rad on joint angles, uniform noise in [ _−_ 0 _._ 02 _,_ 0 _._ 02] m on cube position, and Gaussian noise with scale 0 _._ 1 on the cube orientation quaternion (the quaternion is re-normalized after perturbation). The recorded demonstrations preserve this noise, so the training distribution already includes realistic sensing noise on both the proprioceptive and vision-derived components. 

**Observation space.** 

Each observation **o** _t_ concatenates: 

- **Proprioception (** 32 **dim)** : noisy joint angles (16) and per-joint tracking error – noisy joint angle minus the most recent motor target (16). 

- **Vision-derived cube pose (** 9 **dim)** : palm-to-cube position error (3) and absolute cube orientation in the world frame (6). 

The 9-dim vision-derived subset stands in for VLM features per Sec. 3.2; asynchronous-vision/text evaluations apply staleness only to this subset. 

**Action space.** 16-dim relative joint commands at 50 Hz. Each action **a** _t ∈_ [ _−_ 1 _,_ 1]<sup>16</sup> is scaled by 0 _._ 5 and added to the current motor target. 

**Architecture.** All variants share a Conditional U-Net 1D action head with chunk length _H_ =16 and _n_ obs=2. The U-Net uses FiLM [42] modulation by the noise level _τ_ at every residual block; _π_ **R**<sup>2</sup> replaces the shared FiLM projection with a per-position one – one ( _γp, βp_ ) pair per chunk position – analogous to the per-position AdaLN change described in Sec. 3.3 for DiT-based heads. The rest of the architecture is identical across all variants. 

**Training schedule.** At each batch we sample _d ∼_ Uniform _{_ 1 _, . . . , d_ max _}_ with _d_ max=5, build **_τ_**<sup>_⋆,d_</sup> , fill the front- _d_ slots with ground-truth actions, and mask them out of the loss via _mp_ = **1** [ _p ≥ d_ ]. With probability 0 _._ 2 we instead train on a standard flow schedule (single _τ ∼_ Uniform[0 _,_ 1] shared across positions, no mask), so the same network can also denoise a full chunk from pure 

14 

noise. The standard-flow branch supplies the inference pass that initializes the buffer at episode start (Sec. 3.3, warm-up). For the zero-delay sync curve in Sec. 4.1.1, we train a _d_ =0-only variant ( _d_ max=0). 

**Slow-subset delay in simulation.** The simulation policies are purely state-based: no image or language input. The 9-dim vision-derived subset of the state vector (palm-to-cube position error and absolute cube orientation) plays the slow-channel role from Sec. 3.2. In this setting we find that neither delayed-visual-state sampling at training nor the learned delay embedding is necessary: the env already injects sensor noise on this subset at every step, so the policy is already tolerant to perturbed slow inputs out of the box. 

For all rows of Sec. 4.1.2, a single _π_ **R**<sup>2</sup> checkpoint is used regardless of _d_ vis: the synchronous slowchannel rows ( _d_ vis=0) and the asynchronous-vision/text rows ( _d_ vis _>_ 0) share the same network, and evaluation simply feeds a _d_ vis-step-old version of the 9-dim subset at test time. 

**Evaluation protocol.** At inference, _π_ **R**<sup>2</sup> performs one denoising step per policy call (each call outputs _nact_ actions). Train-time RTC and standard flow runs _K_ =15 denoising steps to predict the whole chunk. Each (method _, d_ ) cell in Sec. 4.1.2 reports the mean success rate over 100 episodes. Full sim hyperparameters are in Tab. 2. 

Table 2: **Simulation training and inference hyperparameters** for the Leap Cube Reorientation Conditional U-Net 1D policies. Values shown are _π_ **R**<sup>2</sup> defaults; the right column lists deviations used by baselines. Empty = baseline same as _π_ **R**<sup>2</sup> . 

|Parameter|_π_**R**<sup>2</sup><br>Baseline deviations|
|---|---|
|_Shared across all variants_||
|Chunk length_H_|16|
|Observation history_n_obs|2|
|Control rate|50Hz|
|Optimizer|AdamW (_β_=[0_._95_,_0_._999])|
|Learning rate (peak)|1_×_10<sup>_−_4</sup>|
|LR schedule|cosine,500-step warm-up|
|Weight decay|1_×_10<sup>_−_6</sup>|
|Gradient-norm clip|1_._0|
|<br>Batch size (global)|256|
|GPUs|1_×_A5000|
|Training budget|800epochs|
|_Method-specific (noise schedule_|_i   + inference)_|
|Train-time_d_max|5<br>10(Train-time RTC); n/a (Flow)|
|Standard-flow warm-up prob._α_|0_._2<br>n/a|
|Inference budget per call|1<br>15(Train-time RTC, Flow)|


**Baselines.** All three variants share the dataset, optimizer, and training budget. _π_ **R**<sup>2</sup> and train-time RTC additionally share the per-batch delay-sampling protocol: each batch draws _d ∈{_ 0 _, . . . , d_ max _}_ from an exponentially-decaying distribution _p_ ( _d_ = _k_ ) _∝ e_<sup>_−αdk_</sup> with _αd_ =1 (smaller _d_ more likely following [30]), and the front- _d_ positions are clamped to ground-truth actions and masked out of the loss. The three variants then differ only in: 

- **Flow** : no _d_ sampling and no front clamp; a single shared noise level _τ ∼_ Uniform[0 _,_ 1] is applied to the entire chunk. This is standard chunked flow matching, evaluated at NFE=15. 

- **Train-time RTC** [30]: same per-batch _d_ sampling as _π_ **R**<sup>2</sup> , but the noise schedule applies a single shared noise level _τ ∼_ Uniform[0 _,_ 1] to the back _H−d_ positions (no per-position structure). No standard-flow warm-up mixing, and larger _dmax_ = 10 as the effective delay is larger. 

- _π_ **R**<sup>2</sup> : same per-batch _d_ sampling as train-time RTC, plus the _α_ =0 _._ 2 standard-flow warm-up branch (with probability 0 _._ 2 the batch instead uses a single _τ ∼_ Uniform[0 _,_ 1] on all positions 

15 

and no front clamp, so the same network can also initialize a buffer from pure noise at episode start). On the remaining 0 _._ 8 of batches we apply the three-region staircase **_τ_**<sup>_⋆,d_</sup> of Sec. 3.3, and the U-Net uses per-position FiLM heads _{_ ( _γp, βp_ ) _}_<sup>_H_</sup> _p_ =0<sup>_−_1.</sup> 

## **A.2 Real-World** 

**Hardware and Workspace.** A 6-DoF xArm6 manipulator carries a 12-DoF XHand at its wrist; a single overhead 640 _×_ 480 RGB camera looks down on the workspace from above (Fig. 7). We fine-tune on 8 _×_ NVIDIA RTX A5000/A6000 (24/48 GB VRAM). Deployment uses a single RTX A5000 for the baselines. _π_ **R**<sup>2</sup> uses 2 _×_ RTX A5000 so the slow VLM and the fast DiT action head do not share compute or memory bandwidth. Sharing one GPU between the two workers measurably inflates DiT latency and would conflate the measured _d_ . 

**Control rate.** Predicted actions run closed-loop at 25 Hz at deployment ( _T_ ctrl _≈_ 40 ms per tick). Teleoperation captures demonstrations at the same rate, bottlenecked by the camera and the XHand–workstation USB link. 


Figure 7: **Real-world workspace.** xArm6 + XHand with a single overhead RGB camera. 

**Base model.** We fine-tune NVIDIA GR00T-N1.7 [27]. The Qwen-VL backbone and Eagle-2 vision encoder remain _frozen_ ; only the action head – state/action projectors, the position embedding, and the DiT – is trained. The only architectural change to the action head replaces the DiT’s shared AdaLN modulation with the per-position ( _γp, βp_ ) heads of Sec. 3.3. 

**Observation space.** 

Each call to the policy receives: 

- **Proprioception** (45 dim): 6 xArm6 joint angles, 12 XHand joint angles (the actively-controlled finger DoFs), 12 corresponding per-joint torques, and 15 fingertip-force values (3-axis force from each of 5 sensorized fingertips). 

- **Vision and language** : one 640 _×_ 480 RGB image from the overhead camera, encoded by Eagle-2 into vision tokens, concatenated with the task prompt (Tab. 4) at the VLM backbone input. 

**Action space and low-level drivers.** Each policy call emits a chunk of _H_ =50 absolute jointposition targets (6 xArm6 + 12 XHand) at 25 Hz, spanning 2 s of motion. We send one target per control tick to each robot’s driver in position-control mode. The arms’ onboard firmware interpolates between consecutive commands at their internal servo rates(Tab. 3). 

Table 3: **Low-level driver settings.** Both robots run in position-only mode at 25 Hz outbound from the policy; the onboard firmware interpolates between targets at its internal rate. 

||xArm6|XHand|
|---|---|---|
|Driver mode|`mode=1`(streaming servo)|RS485, position mode|
|Command call|`set`<br>~~`s`~~`ervo`<br>~~`a`~~`ngle`<br>~~`j`~~|finger`set`<br>~~`t`~~`arget`|
|Bus / link|TCP|RS485|
|Onboard control|API (PID + interp.)|per-joint PID,_kp_=100_, ki_=0_, kd_=0|
|Safety limits|collision sensitivity= 2|torque limit= 300|


**Data collection.** We teleoperate the robot setup to collect 200 demonstrations for _Don’t Spill_ , 300 for _Tidy Up Book_ and _Insert Box_ , and 100 for _Catch Book_ , randomizing the target object’s initial pose. 

**Training the asynchronous vision/text mechanism.** The real-world _π_ **R**<sup>2</sup> training explicitly exercises the asynchronous-vision/text mechanism of Sec. 3.2. Each batch samples a vision delay 

16 

Table 4: **Real-world task prompts.** Exact language input passed to GR00T-N1.7 at both training and deployment. 

|Task|Language prompt|
|---|---|
|Don’t Spill|`put the ball in the bowl and put them on the cutting board`|
|Tidy Up Book|`put the books in the basket`|
|<br>Insert Box|`put the box in the basket`|
|Catch Book|`catch the book`|


_d_ vis _∼_ Uniform _{_ 0 _, . . . , d_<sup>max</sup> vis<sup>_}_with</sup><sup>_d_max</sup> vis<sup>=5ticks (200msat 25Hz);thepolicythen receivesthe</sup> image recorded _d_ vis ticks earlier (i.e., the corresponding past frame in the demonstration), while proprioception stays current. For each batch, the integer _d_ vis _∈{_ 0 _, . . . , d_<sup>max</sup> vis<sup>_}_indexesalearned</sup> embedding _e_ ( _d_ vis) from a ( _d_<sup>max</sup> vis<sup>+1)-entrylookuptable.TheDiTadds</sup><sup>_e_(</sup><sup>_d_vis)toitsaction-token</sup> features (broadcast across the _H_ chunk positions), so the action head conditions on both the cached visual feature and its age. We zero-initialize the lookup table so that the untrained checkpoint reproduces the no-delay variant exactly. At deployment, the measured wall-clock vision latency passes through the same embedding before each DiT call. 

**Training hyperparameters.** We fine-tune the GR00T-N1.7 action head (projectors + DiT) and keep the VLM backbone and vision encoder frozen. Full optimizer settings, batch size, and step budgets are in Tab. 5. The per-task budgets (40 _,_ 000 steps for _Don’t Spill_ , 28 _,_ 000 for _Tidy Up Book_ , 49 _,_ 000 for _Insert Box_ , 4 _,_ 550 for _Catch Book_ ) correspond to approximately 200 _/_ 100 _/_ 100 _/_ 100 epochs over each dataset. The per-position AdaLN parameters _{_ ( _γp, βp_ ) _}_<sup>_H_</sup> _p_ =0<sup>_−_1initializefromthe</sup> pretrained shared pair, so each head starts from a position-uniform schedule and gradually specializes during fine-tuning. All four rows in Tab. 1 fine-tune from the same GR00T-N1.7 checkpoint with identical data and budget; they differ only in the noise schedule and (for _π_ **R**<sup>2</sup> ) the AdaLN modification. The train-time RTC baseline samples its per-batch delay from _d ∈{_ 0 _, . . . ,_ 10 _}_ (i.e., _d_ max=10) rather than the _d_ max=5 used in _π_ **R**<sup>2</sup> , as _π_ **R**<sup>2</sup> is separating the delay into two parts while RTC treats it as a whole. Full hyperparameters are in Tab. 5. 

**Evaluation protocol.** Each (method _,_ task) cell runs _N_ =20 trials with randomized initial object placement. Success rate (SR) counts whole-task completion within the episode time limit (30 seconds). The progress score (Prog) decomposes each task into sub-goals and reports the per-trial fraction completed: 

- _Don’t Spill_ – 4 sub-goals: pick up ball, place ball in bowl, lift bowl off the table, place bowl on the cutting board. 

- _Tidy Up Book_ – 2 sub-goals: pull a book free from the pile, place it inside the basket. 

- _Insert Box_ – 4 sub-goals: push the box towards the wall, make it stand, grasp, and insert between books. 

- _Catch Book_ – 1 sub-goal: grasp the falling book and pick it up. 

**Deployment query modes.** The four rows of Tab. 1 differ in how the action-head worker queries the policy: 

- _Flow, Synchronous_ : the main loop blocks until each call returns; the robot freezes during inference. 

- _Flow, Naive Async, dense, ensemble_ : the action worker queries back-to-back and combines overlapping chunks with the temporal-ensembling weights of Zhao et al. [16]. 

- _Train-time RTC_ and _π_ **R**<sup>2</sup> : the action worker queries back-to-back; the new chunk replaces the active one at the next swap boundary. The actions executed during policy call is given as input. _π_ **R**<sup>2</sup> additionally spawns a VLM-cache worker on a separate GPU that refreshes the cached visual features in the background. 

17 

Table 5: **Real-world training and inference hyperparameters** for the GR00T-N1.7 fine-tunes. Values shown are _π_ **R**<sup>2</sup> defaults; the right column lists deviations used by baselines. Empty = baseline same as _π_ **R**<sup>2</sup> . 

|Parameter|_π_**R**<sup>2</sup>|Baseline deviations|
|---|---|---|
|_Shared across all variants_|||
|Chunk length_H_|50||
|<br>Observation history_n_obs|1||
|Control rate|25Hz||
|Optimizer|fused AdamW||
|Learning rate (peak)|1_×_10<sup>_−_4</sup>||
|<br>LR schedule|cosine,5%warm-up||
|Weight decay|<br>1_×_10<sup>_−_5</sup>||
|Gradient-norm clip|1_._0||
|<br>Batch size|512||
|Precision|bf16 + tf32||
|GPUs|8_×_A5000/A6000||
|Training budget|100epoch (_Tidy Up Book_/_In_|_sert Box Catch Book_) /200epoch (_Don’t Spill_)|
|_Method-specific (noise schedule +_|_i    delay + inference)_||
|Train-time_d_max|5|10(Train-time RTC); n/a (Flow)|
|Train-time_d_<sup>max</sup><br>vis|5|n/a|
|Delay-embedding lookup size|6entries_→_DiT hidden dim|n/a|
|Standard-flow warm-up prob._α_|0_._2|0(Flow, Train-time RTC)|
|NFE per call|1(one sub-chunk)|4(Flow, Train-time RTC; full chunk)|


## **A.3 Training and Inference Algorithms** 

We give pseudocode for the per-batch training step (Alg. 1) and the deployment-time inference loop (Alg. 2). The inference loop is the loop implemented in our deployment script; the wall-clock measurement that auto-derives _d_ uses a rolling window of the most recent query times. 

**Algorithm 1** _π_ **R**<sup>2</sup> training step. Each batch samples a delay _d_ , builds the staircase **_τ_**<sup>_⋆,d_</sup> , masks the front, applies jitter, and (for real-world training) additionally delays the slow channel. 

**Require:** Action chunk **a** 0: _H−_ 1, observation ( **o**<sup>fast</sup> _t ,_ **o**<sup>slow</sup> _t_ : _t−T_ slow+1<sup>), model</sup><sup>_vθ_</sup> **Require:** Hyperparams _d_ max _, d_<sup>max</sup> vis<sup>_, j, α_</sup> 1: _u ∼_ Uniform[0 _,_ 1] 2: **if** _u < α_ **then** _▷_ warm-up branch: standard flow 3: _t ∼_ Uniform[0 _,_ 1]; _τp ← t, ∀p_ 4: **x** _τ,p ←_ (1 _− τp_ ) **_ϵ_** _p_ + _τp_ **a** _p_ 5: _mp ←_ 1 _, ∀p ▷_ all positions contribute to loss 6: **else** _▷_ staircase branch 7: _d ∼_ Uniform _{_ 1 _, . . . , d_ max _}_ 8: Build **_τ_**<sup>_⋆,d_</sup> as in Sec. 3.3 _▷_ three-region staircase 9: _δp ∼_ Uniform[ _−j, j_ ]; _τp ←_ clip( _τp_<sup>_⋆,d_</sup> + _δp,_ 0 _,_ 1) 10: **x** _τ,p ←_ (1 _− τp_ ) **_ϵ_** _p_ + _τp_ **a** _p_ 11: **x** _τ,p ←_ **a** _p_ if _p < d ▷_ front _d_ slots are ground-truth (inpaint conditioning) 12: _mp ←_ **1** [ _p ≥ d_ ] 13: **end if** 14: _d_ vis _∼_ Uniform _{_ 0 _, . . . , d_<sup>max</sup> vis<sup>_}_</sup> _▷_ slow-channel staleness (real-world only) 15: **o**<sup>slow</sup> _←_ **o**<sup>slow</sup> _t−d_ vis<sup>; append</sup><sup>_e_(</sup><sup>_d_vis) to slow representation</sup> 16: **v** ˆ _p ← vθ_ ( **x** _τ ,_ **_τ_** _,_ **o** _t_<sup>fast</sup> _,_ **o**<sup>slow</sup> ) _p_ 17: _L ←_<sup>�</sup><sup>_H_</sup> _p_ =0<sup>_−_1</sup><sup>_mp ∥_</sup><sup>**v**ˆ</sup><sup>_p −_(</sup><sup>**a**</sup><sup>_p −_</sup><sup>**_ϵ_**</sup><sup>_p_)</sup><sup>_∥_2</sup> 18: Update _θ_ on _L_ 

18 

**Algorithm 2** _π_ **R**<sup>2</sup> inference loop on the robot. The action head runs continuously with fresh proprioception and a cached slow feature; the VLM runs asynchronously in a background thread; the <u>per-call delay</u> _d_ is auto-derived from a rolling measurement of action-head wall-clock latency. 

**Require:** Policy _vθ_ , observation source, robot controller, control period _T_ ctrl **Require:** Rolling window _W_ of recent query times (e.g. _W_ =20) 1: **C** _←_ `WarmStart` () _▷_ Sec. 3.3: full standard-flow inference, denoise all _H_ positions 2: **C** _←_ re-noise **C** to match **_τ_**<sup>_⋆,d_0</sup> for initial estimate _d_ 0 3: _i ←_ 0 _▷_ chunk index 4: queue _Q ←∅ ▷_ rolling latency window 5: **Spawn** `VLM` ~~`W`~~ `orker` thread (continuously updates cached slow feature) 6: **Spawn** `Action` ~~`W`~~ `orker` thread (continuously queries action head) 7: **loop** _▷_ one iteration per control tick (25 Hz) 8: _t_ 0 _←_ current wall-clock time 9: Read fresh proprioception **o**<sup>fast</sup> _t_ from robot sensors 10: Publish **o**<sup>fast</sup> _t_ to shared state for workers 11: **if** new chunk **C** new is available from `Action` ~~`W`~~ `orker` **then** 12: **C** _←_ **C** new; _i ← d ▷_ swap and skip past in-flight front actions 13: **end if** 14: Send action **C** _i_ to robot; _i ← i_ + 1 15: Sleep until _t_ 0 + _T_ ctrl 16: **end loop** 17: **procedure** ACTION WORKER _▷_ background thread; one denoising step per call 18: **loop** 19: Snapshot ( **o**<sup>fast</sup> _t , t_ state) and the cached ( **o**<sup>slow</sup> cached<sup>_, t_image)</sup> 20: _d_ vis _←_ round�( _t_ state _− t_ image) _/T_ ctrl� _▷_ age of cached slow feature in control ticks 21: _d ←_ max �1 _,_ round(mean( _Q_ ) _/T_ ctrl)� _▷_ auto-derived from rolling window 22: Snapshot front- _d_ inpaint: **a**<sup>inflight</sup> 0: _d ←_ **C** _i_ : _i_ + _d_ 23: _q_ 0 _←_ wall-clock 24: **C** new _← vθ._ `euler` ~~`s`~~ `tep` ( **a**<sup>inflight</sup> _,_ **o**<sup>fast</sup> _,_ **o**<sup>slow</sup> cached<sup>_, e_(</sup><sup>_d_vis))</sup><sup>_▷_one NFE; per-position ∆</sup><sup>_τp_</sup> as in Eq. (4) 25: Push wall-clock _− q_ 0 into _Q_ 26: Hand off **C** new to main loop 27: **end loop** 28: **end procedure** 

29: **procedure** VLM WORKER _▷_ background thread; runs vision/text forward asynchronously 30: **loop** 31: Read fresh image and language; _t_ image _←_ image capture time 32: **o**<sup>slow</sup> cached<sup>_←_VLM forward (image, language)</sup> 33: Atomically update cache with ( **o**<sup>slow</sup> cached<sup>_, t_image)</sup> 34: **end loop** 35: **end procedure** 

## **A.4 Additional Reactivity Analysis** 

The main-text reactivity comparison (Fig. 5) is on _Tidy Up Book_ ; the same pattern holds across the other tasks (Fig. 8). On _Catch Book_ , _π_ **R**<sup>2</sup> closes on the force spike as the book lands, whereas Train-Time RTC reacts too late and the book slips. On _Insert Box_ , RTC reacts late to the force feedback and its index force overshoots out of distribution, while _π_ **R**<sup>2</sup> stays controlled. On _Don’t Spill_ , RTC’s thumb never contacts the ball (thumb force _≈_ 0) yet it keeps going, while _π_ **R**<sup>2</sup> grasps it with both fingers. 

19 


Figure 8: **Reactivity on the remaining tasks.** Fingertip force (solid, left axis) and the emitted action (dashed, right axis) over time for _π_ **R**<sup>2</sup> and Train-Time RTC, with overhead frames at the marked times. Top: _Catch Book_ . Middle: _Insert Box_ . Bottom: _Don’t Spill_ . 

20 

