---
title: "FutureRTC: Real-Time Robot Execution with Anticipatory-Conditioned Action Chunking"
date: "2026-07-27"
authors: "Hai Jiang; Yixian Zou; Binbin Liang; Boqian Liu; Fanman Meng; Shuaicheng Liu"
url: https://arxiv.org/abs/2607.24008
pdf: https://arxiv.org/pdf/2607.24008
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2607.24008)** / [論文ページ](https://arxiv.org/abs/2607.24008)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

## **FutureRTC: Real-Time Robot Execution with Anticipatory-Conditioned Action Chunking** 

### **Hai Jiang**<sup>1</sup> **, Yixian Zou**<sup>2</sup> **, Binbin Liang**<sup>1</sup> **, Boqian Liu**<sup>3</sup> **, Fanman Meng**<sup>2</sup> **, Shuaicheng Liu**<sup>2∗</sup> 

1School of Aeronautics and Astronautics, Sichuan University 

2University of Electronic Science and Technology of China 

3University of Alberta 

jianghai@stu.scu.edu.cn, {zouyixian@std., liushuaicheng@}uestc.edu.cn 


Figure 1: Comparison of the inference-time method RTC (Black, Galliker, and Levine 2025), training-time method VLASH (Tang et al. 2025), and our FutureRTC on the real-world “ _Hang Cups_ ” task with _π_ 0 _._ 5 (Black et al. 2025a) as the VLA backbone. **Top** : Task completion progress under asynchronous execution. **Bottom** : Average robot kinematics during task execution. 

##### **Abstract** 

Real-time deployment of Vision-Language-Action (VLA) policies necessitates asynchronous execution, wherein subsequent action chunks are computed concurrently with the execution of the current chunk, leading to prediction-execution misalignment and manifesting as inter-chunk discontinuities. Existing methods either superficially smooth chunk boundaries, require costly policy optimization, or exclusively forward-predict proprioceptive states yet neglect critical visual observations. In this paper, we propose **FutureRTC** , a plug-and-play adaptation framework that predicts executiontime observations and states for asynchronous VLA control without modifying the underlying policy. Specifically, FutureRTC features a state correction module to compensate for the discrepancy between rolled-forward and actual executiontime proprioceptive states and an observation prediction mod- 

∗Corresponding author. 

ule that forecasts execution-time visual representations by leveraging robot motion as an explicit physical prior through motion-aware feature transport and reconstruction. Furthermore, we introduce a policy consistency loss to align the action chunks generated from predicted contexts with those produced under the expected execution-time inputs of the VLA policy. Extensive experiments across simulated and real-world environments demonstrate that FutureRTC achieves superior robustness to inference delays, resulting in smoother trajectories, faster execution, and consistently higher task success rates. Project Website. 

### **Introduction** 

Vision-Language-Action (VLA) models have recently emerged as an attractive paradigm for robot learning by unifying deep visual-linguistic reasoning with expressive action generation (Kim et al. 2024; Black et al. 2025b,a). To reconcile the substantial computational cost of VLA inference 

with the high-frequency requirements of low-level robot control, _action chunking_ (Zhao et al. 2023) has become a widely adopted strategy, which enables the policy to generate a sequence of future actions in a single forward pass, thereby amortizing the inference overhead through open-loop execution. However, as VLA models continue to scale in size and are deployed on resource-constrained edge platforms or remote servers, inference latency has become a fundamental challenge for real-time deployment (Black, Galliker, and Levine 2025; Ma et al. 2025). In standard _synchronous execution_ , the robot is forced to idle during chunk computation, resulting in stop-and-go behaviors that severely degrade realtime responsiveness and manipulation precision. 

To circumvent execution stalls, recent systems adopt _asynchronous execution_ (Black, Galliker, and Levine 2025), wherein the policy generates future action chunks in parallel with the execution of the current chunk. While improving computational efficiency, conducting mutations at chunk boundaries causes _inter-chunk discontinuities_ that accumulate errors and lead to task failures. Existing efforts to mitigate discontinuities generally fall into inference-time and training-time strategies. The former (Zhao et al. 2023; Liu et al. 2025b; Black, Galliker, and Levine 2025; Ho et al. 2026) utilize heuristic post-processing to smooth chunk boundaries without retraining the policy, often introducing additional computational overhead. In contrast, most trainingtime methods (Black et al. 2025c; Wang et al. 2026a,b) explicitly adapt the policy to asynchronous execution, while requiring costly retraining or fine-tuning the VLA model. 

However, neither of the above approaches resolves the fundamental _prediction-execution misalignment_ , where the executed actions remain conditioned on observations and proprioceptive states from an earlier time step, causing them to deviate from the evolving scene as inference delay grows. VLASH (Tang et al. 2025) attempts to reduce the misalignment by forward-predicting the execution-time proprioceptive state while still relying on outdated visual observations. Since the visual scene evolves alongside the robot configuration during the delay interval, correcting the state alone is insufficient to provide the execution time context required by the policy. As shown in Fig. 1, both the inference-time method RTC and the training-time method VLASH exhibit jerky trajectories and slower task completion speed. 

To this end, we propose **FutureRTC** , a plug-and-play adaptation framework that anticipates the execution-time observation and state that the policy should condition on to address prediction-execution misalignment for real-time robotic control while leaving the base VLA untouched. Specifically, we first introduce a state correction module that compensates for the residual discrepancy between the state obtained by rolling the committed actions forward and the actual execution-time proprioceptive state. Subsequently, we observe that correcting the state alone is insufficient, as the stale observation is itself a critical factor whose neglect causes substantial performance degradation that intensifies as the inference delay increases. To this end, we propose an observation prediction module that predicts the executiontime visual representation from the stale observation, committed actions, and corrected state. By leveraging robot mo- 

tion as the physical prior, the module spatially transports existing visual features through motion-aware warping and reconstructs newly exposed content during the delay interval. Furthermore, we introduce a policy consistency loss to encourage the action chunk generated by the untouched policy from the predicted observation and corrected state to match the one generated from the actual execution-time pair. As shown in Fig. 1, our method presents smoother trajectories and faster task completion speed. Extensive experiments across simulated and real-world settings demonstrate that our FutureRTC delivers faster execution, robust delay tolerance, and consistently higher success rates. 

Our contributions can be summarized as follows: 

- We propose FutureRTC, a plug-and-play adaptation framework that generates execution-time observations and states to mitigate asynchronous prediction-execution misalignment for real-time robot execution. 

- We propose a state correction module to compensate for the residual discrepancy between rolled-forward and actual execution-time states, and an observation prediction module to forecast execution-time visual observations, using a policy consistency loss to align the predicted context with the distribution expected by the untouched policy. 

- Extensive evaluations demonstrate that FutureRTC achieves superior robustness under varying inference delays, smoother trajectories, faster task completion, and consistently improved task success rates. 

### **Related Work** 

#### **VLA and Action Chunking** 

Vision-Language-Action models have advanced robot learning by integrating visual perception, language understanding, and action prediction within a unified policy framework (Kawaharazuka et al. 2024). Representative methods (Kim et al. 2024; Black et al. 2025b; Liu et al. 2025a; Bjorck et al. 2025; Shukor et al. 2025; Black et al. 2025a; Wen et al. 2025; Zhong et al. 2026; Wu et al. 2026) leverage large-scale multimodal pre-training and integrate deep visual-linguistic representations with expressive action generation paradigms, including diffusion models and flow matching (Lipman et al. 2023; Ze et al. 2024; Chi et al. 2025), to improve cross-task generalization. However, the sheer scale of these models, with substantial computational costs, makes inference latency a critical bottleneck for real-time robotic control. In synchronous control loops, such latency forces robots to wait for the next action prediction, thereby reducing closed-loop responsiveness in dynamic scenes. 

To alleviate the computational bottleneck and mitigate the compounding errors associated with step-wise execution, action chunking has been widely adopted as the standard paradigm in VLAs. By generating multi-step action sequences in parallel, it bridges the gap between low-frequency policy inference and high-frequency robot control. However, open-loop execution of long chunks weakens short-term responsiveness to environmental perturbations, whereas executing shorter chunks often introduces boundary discontinuities and jerky motions. Therefore, balancing temporal 


Figure 2: Comparison between our method and existing execution paradigms, illustrated with prediction horizon _H_ = 5, execution horizon _K_ = 3, and inference delay _d_ = 2. **(a) Synchronous:** The robot stalls during inference, yielding accurate but stop-and-go motion. **(b) Naive Asynchronous:** Chunk **A** 1 is conditioned on the stale observation-state pair ( _o_ 1 _, s_ 1) yet executed at step 3, suffering from prediction-execution misalignment and inter-chunk discontinuities. **(c) FutureRTC (Ours):** Our plug-and-play adapter _ϕ_ ( _·_ ) forecasts the execution-time context (ˆ _z_ 3 _,_ ˆ _s_ 3) = _ϕ_ ( _z_ 1 _, a_ 1:2) from the stale _o_ 1 and committed actions _a_ 1:2, where _z_ is the latent feature of the observation _o_ obtained by the vision encoder of the pretrained VLA. Conditioning the policy on this anticipated pair promotes continuous, reactive, and smooth execution. 

consistency with environmental responsiveness remains a central challenge in chunk-based VLA deployment. 

#### **Asynchronous VLA Inference** 

To mitigate execution stalls, recent systems adopt asynchronous inference, in which the robot continues executing the remaining actions of the previously generated chunk while the policy computes the next chunk in parallel, which may amplify inter-chunk discontinuities and introduce synchronization challenges between prediction and execution. Existing remedies fall into inference-time and training-time strategies. The former (Zhao et al. 2023; Black, Galliker, and Levine 2025; Liu et al. 2025b; Ho et al. 2026) operate only during inference by modifying the generated actions or execution procedure without updating the policy parameters, but often introduce additional runtime computation, thus making it undesirable for low-latency robotic control. In contrast, training-time methods (Black et al. 2025c; Sendai et al. 2025; Wang et al. 2026a; Liu et al. 2026; Wang et al. 2026b) require extra optimization stages, by fine-tuning, retraining, or augmenting the VLA policy with trainable modules, to explicitly adapt the policy to asynchronous execution. Nevertheless, asynchronous inference inherently introduces prediction-execution misalignment, as actions are generated from observations that are stale before execution. VLASH (Tang et al. 2025) alleviates this issue by conditioning on future proprioceptive states, but it still relies on outdated visual observations and therefore remains insensitive to environmental changes. In this paper, we present an asynchronous inference framework in which a plug-and-play adapter is constructed to predict execution-time observations and states from their stale counterparts, thereby enabling smoother, faster, and more accurate execution. 

### **Preliminaries** 

**Action Chunking Policy.** For a given control timestep _t_ , the VLA policy maps the visual observation _ot_ and proprioceptive state _st_ to a trajectory of _H_ future actions as: 

**A** _m_ = ( _at, at_ +1 _, . . . , at_ + _H−_ 1) _∼ πθ_ ( _· | ot, st_ ) _,_ (1) 

where _m_ indexes successive chunks and _H_ represents the _prediction horizon_ (Zhao et al. 2023). To circumvent the computational burden of per-step replanning, the controller executes a subset of _K_ actions ( _K ≤ H_ ) from **A** _m_ prior to the next policy query, where _K_ denotes the _execution horizon_ . While such a chunking paradigm mitigates inference costs and promotes temporal consistency, it introduces a structural dependency between the control loop frequency and sequence generation latency. 

**Flow-matching Generation.** In line with recent VLA models (Black et al. 2025b,a; Shukor et al. 2025), we parameterize the action generation process of our policy via flow matching (Lipman et al. 2023). To generate an action chunk, an initial latent state **A**<sup>0</sup> _m_<sup>_∼N_(</sup><sup>**0**</sup><sup>_,_</sup><sup>**I**)istransformedbyinte-</sup> grating a learned velocity field _vθ_ over a flow-matching time _τ ∈_ [0 _,_ 1] using _n_ Euler steps as: 


yielding the final iterate **A**<sup>1</sup> _m_<sup>as the predicted action sequence.</sup> **Inference Delay.** Generating an action chunk incurs a nonnegligible wall-clock time _δ_ . Given a base controller period ∆ _t_ , we define the _inference delay_ as _d_ = _⌊δ/_ ∆ _t⌋_ , which quantifies the number of control steps that elapse between acquiring the observation-state pair ( _ot, st_ ) and the chunk **A** _m_ being ready for execution (Black, Galliker, and Levine 2025). As VLAs scale in model capacity and shift toward remote or edge-constrained inference, the latency _δ_ , and consequently the inference delay _d_ , inevitably increases. 

**Synchronous and Asynchronous Execution.** In _synchronous_ execution, the control loop blocks during the generation of **A** _m_ , while ensuring each action chunk is conditioned on the recent state ( _ot, st_ ), it introduces robot stalls for _d_ steps between chunks, thereby breaking real-time control continuity, as shown in Fig. 2 (a). _Asynchronous_ execution removes this stall by generating the subsequent chunk in the background. To ensure that the next chunk **A** _m_ +1 is ready precisely when the current _K_ actions conclude, its inference must be initiated _d_ steps in advance. Consequently, the new chunk is conditioned on the stale ( _ot_ + _K−d, st_ + _K−d_ ), yet executes at step _t_ + _K_ . The first _d_ actions in **A** _m_ +1 would 

be discarded since they overlap with the committed tail of the current chunk, only the remainder **A** _m_ +1[ _d_ : _d_ + _K −_ 1] is spliced on and executed, as shown in Fig. 2 (b). **Prediction-Execution Misalignment.** Formulating the subsequent chunk as **A** _m_ +1 = _πθ_ ( _· | ot_ + _K−d, st_ + _K−d_ ), the actions executed from step _t_ + _K_ relies on an observation and state that are _d_ steps obsolete. This temporal gap between the conditioning time _t_ + _K − d_ and the execution time _t_ + _K_ constitutes a critical _prediction-execution misalignment_ that manifests as inter-chunk discontinuities. Furthermore, since the scene and robot would evolve during the _d_ -step window, it causes the executed actions to deviate from the intended behavior, exacerbating the error as _d_ grows. 

### **Methodology** 

Given a flow-matching VLA _πθ_ ( _· | ot, st_ ), our objective is to mitigate the discrepancy of asynchronous execution, wherein the policy is conditioned on the stale pair ( _ot_ + _K−d, st_ + _K−d_ ) prior to its execution at step _t_ + _K_ . To rectify this predictionexecution misalignment and realize reliable closed-loop performance, we introduce **FutureRTC** , which incorporates a plug-and-play anticipatory adapter _ϕ_ ( _·_ ) to forecast the execution-time observation and state from their stale counterparts, promoting highly reactive and kinematically smooth robotic control, as shown in Fig. 2 (c). 

#### **State Correction Module** 

The execution-time state _st_ + _K_ remains unobservable at the generation step _t_ + _K −d_ , while it can be estimated by rolling forward the stale state _st_ + _K−d_ using the committed actions [ _at_ + _K−d_ : _at_ + _K−_ 1] following (Tang et al. 2025) as: 


However, whether under absolute or relative posture control, forward integration inevitably accumulates bias due to the inherent deviation between the commanded motion and the actual robot motion. To this end, we introduce a State Correction Module (SCM) _ϕ_ SCM( _·_ ) that consists of MLP layers, as shown in Fig. 3 (a), to predict a compensatory residual as ˜ _s_ ∆ = _ϕ_ SCM(˜ _st_ + _K, d_ max _<u>d</u>_<sup>), to complement the for-</sup> ward integration process. The final execution-time state is obtained as _s_ ˆ _t_ + _K_ = _s_ ˜ _t_ + _K ⊕ s_ ˜∆, with the orientation updated through relative-rotation composition, which serves simultaneously as the conditioning signal for the observation predictor and the state input for the VLA policy. During the training phase, we employ a state correction loss _L_ state to minimize the discrepancy between the predicted _s_ ˜∆ and its ground-truth counterpart recorded in the demonstrations as: 


#### **Observation Prediction Module** 

While the state correction module mitigates a fraction of the prediction-execution misalignment, observational staleness remains a critical unaddressed factor causing performance degradation, the severity of which increases sharply as the delay _d_ increases. To estimate the unobservable execution-time 


Figure 3: Illustration of the detailed architecture of the proposed adapter, which consists of a State Correction Module and an Observation Prediction Module to generate the execution-time observation and state from stale information. 

observation _ot_ + _K_ , we introduce an Observation Prediction Module (OPM) _ϕ_ OPM( _·_ ), as shown in Fig. 3 (b), which leverages the stale observations, the committed actions, and the corrected state to generate the execution-time observation. Instead of reconstructing high-dimensional pixels, our OPM operates within the latent space, i.e., the feature _z_ = _E_ ( _o_ ) obtained from the vision encoder _E_ ( _·_ ) of the pretrained VLA, ensuring the computational overhead is relatively limited compared to policy inference while generating representations that are inherently compatible with VLA policies. 

Since the primary visual variation is induced by the physical displacement of the robot, we model feature evolution as spatial transportation rather than synthesizing it from scratch. The committed action sequence within the delay window [ _at_ + _K−d_ : _at_ + _K−_ 1] dictates the physical motion responsible for scene changes and thus serves as an explicit motion prior indicating where existing content should be transported. However, feeding the action sequence directly would force the network to implicitly learn forward integration. We instead map the action trajectory into an explicit physical feature space. For each committed action _ai_ within the window, we construct a physical feature vector **u** _i_ as: 


which respectively encode the instantaneous command, cumulative displacement, action increment, accumulated path length, and temporal progress. Concatenating the features across all steps yields a trajectory feature matrix **U** = [ **u** 1 _,_ **u** 2 _, . . . ,_ **u** _d_ ]<sup>_⊤_</sup> , which is fed into a temporal self-attention block to capture temporal dependencies and produce the action-conditioned motion prior **c** motion. 

We then fuse the motion prior **c** motion, the stale latent **z** _t_ + _K−d_ together with the per-camera embedding **e** cam which distinguishes the camera streams and position embedding **e** pos, and the corrected state _s_ ˆ _t_ + _K_ to supply the actual endeffector configuration at execution time _t_ + _K_ to form a conditioning feature _F_ . However, directly regressing the fu- 


Figure 4: Illustration of the transport gate _α_ (top) and synthesis gate _β_ (bottom) during execution. The transport gate activates on the moving arm and gripper, propagating existing visual features according to the committed motion, whereas the synthesis gate highlights motion boundaries and newly revealed regions that require feature synthesis. 

ture latent from _F_ is highly ill-posed and physically unconstrained. We therefore explicitly project _F_ by cascaded linear and convolutional layers into a 2D flow displacement ∆ **p** and a transport gate _α ∈_ [0 _,_ 1]. The stale feature is spatially warped using differentiable bilinear grid sampling to pull in the motion-transported content and blend it back through a gated combination to obtain _z_ trans, whose content has been repositioned to the location carried by the motion flow, as: 


where _W_ ( _·_ ) and **p** denote the bilinear grid sampling and the 2D coordinate grid, respectively. The transport gate _α_ serves as a per-token weight that determines the contribution of warped features, where static regions preserve their original representations ( _α →_ 0), while regions undergoing robot-induced motion increasingly rely on the warped features ( _α →_ 1), as shown in the top row of Fig. 4. 

While warp transport handles coordinate-space displacement, it is fundamentally restricted to feature rearrangement and cannot synthesize unknown content, such as visual deformations upon gripper contact or newly revealed disoccluded regions, which cannot be explained by geometric warping. To this end, we introduce a gated residual branch consisting of several linear and convolutional layers to compensate for content unexplained by transport, which ingests the conditioning feature _F_ , the transport residual _z_ trans _− zt_ + _K−d_ that represents changes already resolved by advection, and the initial observation _z_ 0 as a static visual reference from which disoccluded content can be borrowed, to predict a synthesis feature **r** and a synthesis gate _β ∈_ [0 _,_ 1] as: 


The final execution-time latent _z_ ˆ _t_ + _K_ is reconstructed as _z_ ˆ _t_ + _K_ = _z_ trans + _β ·_ **r** . The synthesis gate _β_ regulates the injection of synthesized features, assigning higher weights to areas where visual dynamics cannot be resolved by spatial transport, as shown in the bottom row of Fig. 4. In the training phase, we employ an observation prediction loss _L_ obs to minimize the discrepancy between the predicted latent ˆ _zt_ + _K_ and the recorded latent _zt_ + _K_ at execution time as: 


Finally, the VLA policy leverages our anticipated pair to generate the next chunk **A** _m_ +1 = _πθ_ ( _· | z_ ˆ _t_ + _K,_ ˆ _st_ + _K_ ), where the predicted visual latent _z_ ˆ _t_ + _K_ is directly injected into the policy, bypassing the original vision encoder. The chunk is already aligned to the execution time _t_ + _K_ and is therefore executed directly from its first action, i.e., **A** _m_ +1[0: _K −_ 1]. 

#### **Policy Consistency Loss** 

To ensure that the predicted observation ˆ _zt_ + _K_ and corrected state ˆ _st_ + _K_ are faithfully consumed by the policy, we further introduce a policy consistency loss _L_ policy to encourage the action chunk generated by the untouched policy from the anticipated pair (ˆ _zt_ + _K,_ ˆ _st_ + _K_ ) to align with the one generated from the ground-truth pair ( _zt_ + _K, st_ + _K_ ). To circumvent the computational overhead of multi-step flow matching during training, we employ a single-step flow approximation to generate the action chunk. The _L_ policy is defined as: 


### **Experiments** 

In this section, we conduct comprehensive experiments on both simulated and real-world tasks to evaluate the effectiveness of our method under various inference delay settings. **Implementation Details.** We implement the proposed method with PyTorch on NVIDIA RTX 4090 GPUs with the batch size set to 128, reaching convergence within 200k iterations. We employ the Adam optimizer (Kingma and Ba 2015) for optimization with the learning rate decayed from 3 _×_ 10<sup>_−_4</sup> to 1 _×_ 10<sup>_−_6</sup> , and empirically set the hyperparameter _λ_ = 10. To make our approach robust across a wide range of inference delays without per-delay retraining, we uniformly sample the delay _d ∼U_ [1 _, d_ max] at each training step, where _d_ max denotes the largest delay considered on each benchmark. Importantly, the base VLA policy remains untouched throughout the entire training process. 

#### **Simulated Benchmark** 

In this section, we conduct experiments on two simulated robotic manipulation benchmarks, including Kinetix (Black, Galliker, and Levine 2025) and LIBERO (Liu et al. 2023), to evaluate the effectiveness of the proposed method under various inference delay settings. We compare our method with two categories of existing methods: (1) Inference-time methods: including **Naive Asynchronous (Naive Async.)** , which directly executes actions from the most recently generated action chunk, **Temporal Ensembling (TE)** (Zhao et al. 2023), **BID** (Liu et al. 2025b), and **RTC** (Black, Galliker, and Levine 2025). (2) Training-time methods: including **training-time RTC (T-RTC)** (Black et al. 2025c), **VLASH** (Tang et al. 2025), **REMAC** (Wang et al. 2026a), and **DiscreteRTC** (Wang et al. 2026b). 

**Kinetix.** We first evaluate our method on the Kinetix simulator (Black, Galliker, and Levine 2025), which contains 12 highly dynamic and stochastic environments designed to assess asynchronous execution. For each task, we adopt the 

Table 1: Performance comparison of _π_ 0 _._ 5 (Black et al. 2025a) and SmolVLA-450M (Shukor et al. 2025) in the LIBERO (Liu et al. 2023) benchmark with different methods across various inference delays _d ∈{_ 5 _,_ 10 _,_ 15 _,_ 20 _}_ . The best results are highlighted in **bold** . “Infer.” and “Train.” denote the methods that are categorized as inference-time and training-time, respectively. 

||||_π_0|_._5|||SmolVL|A-450M||
|---|---|---|---|---|---|---|---|---|---|
||Methods|Succ|ess Rate (%)_↑_|/ Execution Ste|ps_↓_|Succ|ess Rate (%)_↑_|/ Execution St|eps_↓_|
|||_d_= 5|_d_= 10|_d_= 15|_d_= 20|_d_= 5|_d_= 10|_d_= 15|_d_= 20|
||Naive Async.|89.5 / 169.0|82.7 / 183.0|76.3 / 196.6|68.3 / 210.9|70.3 / 206.4|64.5 / 218.2|61.3 / 224.2|56.2 / 232.8|
|er.|TE|87.8 / 173.0|84.3 / 180.1|80.6 / 185.8|74.8 / 197.0|68.4 / 208.8|66.7 / 212.9|62.6 / 220.0|59.7 / 224.2|
|Inf|BID|90.3 / 168.2|84.0 / 180.5|76.1 / 197.3|71.3 / 205.8|70.0 / 207.6|65.0 / 216.4|61.7 / 223.0|57.1 / 229.4|
||RTC|89.9 / 168.4|83.2 / 181.6|77.5 / 194.2|73.7 / 200.5|69.7 / 208.1|64.9 / 217.0|62.6 / 220.9|58.7 / 226.3|
||T-RTC|89.4 / 168.5|84.0 / 177.7|77.9 / 193.1|74.0 / 200.1|69.9 / 208.7|65.6 / 215.8|61.7 / 222.0|59.4 / 226.6|
|in.|VLASH|88.0 / 171.9|83.4 / 178.9|79.5 / 187.4|74.5 / 197.4|69.3 / 208.5|65.8 / 217.6|64.7 / 215.6|61.9 / 220.9|
|Tra|REMAC|90.8 / 166.6|85.4 / 177.6|78.5 / 192.6|73.9 / 199.6|70.9 / 206.2|66.5 / 213.5|62.2 / 220.9|59.7 / 224.9|
||Ours|**94.2**/**162.4**|**92.4**/**166.9**|**91.0**/**170.1**|**88.5**/**175.1**|**75.8**/**198.7**|**73.3**/**202.7**|**71.6**/**206.4**|**69.4**/**209.4**|


Figure 5: Performance comparison in the Kinetix simulator (Black, Galliker, and Levine 2025) with different execution methods across various inference delays _d ∈_ [0 _,_ 4]. 

action chunking flow policies with a prediction horizon of _H_ = 8, pretrained for 32 epochs following (Black, Galliker, and Levine 2025). The inference delay _d_ is varied from 0 to 4, and the execution horizon is selected from max _{_ 1 _, d}_ to 8 _− d_ , ensuring that actions remain continuously available without gaps between consecutive chunks. 

We report the average performance across 12 tasks, measured by both task success rate and execution steps, as shown in Fig. 5. Naive Async. suffers performance collapse as the inference delay increases, while inference-time methods provide partial mitigation. Training-time methods show stronger robustness, but their reliance on outdated observations and states still causes notable degradation under large delays. VLASH reduces this misalignment by conditioning on execution-time states, yet its performance remains inferior to ours. In contrast, our method shows superior robustness, with only a 3.0% success rate drop from _d_ = 0 to _d_ = 4, and fewer steps are required when _d ≥_ 2. Meanwhile, previous methods require more execution steps under large delays due to reactive hesitation and inter-chunk discontinuities, proving that our method can realize reliable and smoother decisionmaking. It is worth noting that our method is slightly behind several training-time methods that fine-tune or retrain the policy for the benchmark tasks at small delays, i.e., _d_ = _{_ 0 _,_ 1 _}_ , whereas our method keeps the VLA policy frozen and only 

##### serves as a plug-and-play module. 

**LIBERO.** We further evaluate on the LIBERO (Liu et al. 2023) benchmark, which spans four task suites, including Spatial, Object, Goal, and Long. To assess whether our adapter transfers across backbones, we attach it to two pretrained VLAs, _π_ 0 _._ 5 (Black et al. 2025a) and SmolVLA450M (Shukor et al. 2025), with the execution horizon set to _K_ = 25. We probe a wider delay as _d ∈{_ 5 _,_ 10 _,_ 15 _,_ 20 _}_ , reflecting practical deployment where remote or resourceconstrained inference on large VLAs incurs substantial delays. For inference-time methods and our method, we build directly on the finetuned weights of the above two VLAs released by LeRobot (Cadene et al. 2026) and keep them frozen for evaluation. For training-time methods, instead of adapting these weights, we reproduce them ourselves following their corresponding publications, except for VLASH, which provides an official LIBERO implementation. We omit DiscreteRTC for comparison since it presumes a discrete diffusion policy trained from scratch and cannot be instantiated on the flow-based backbones adopted here. 

We report the average success rate and execution steps across four tasks in Table 1, where our method consistently achieves the highest success rate while requiring the fewest execution steps on all evaluated delays and both VLA backbones. The performance of existing methods deteriorates substantially with increasing delay, whereas our approach exhibits only a modest 5.7% and 6.4% decrease in success rate from _d_ = 5 to _d_ = 20 on _π_ 0 _._ 5 and SmolVLA, respectively. Moreover, our method consistently completes tasks in fewer execution steps, indicating smoother and more decisive control under severe asynchronous execution. VLASH, which partially mitigates prediction-execution misalignment by rolling forward the proprioceptive state, presents robustness at large delays compared to other methods. However, it still trails our method, suggesting that compensating for the robot state alone is insufficient when visual observations remain temporally stale. By jointly anticipating the execution-time context, our method consistently achieves the best performance. **We provide more comprehensive simulated experimental analysis in the appendix.** 

Table 2: The average success rate of ablation studies using SmolVLA-450M (Shukor et al. 2025) on the LIBERO (Liu et al. 2023) benchmark. The last two columns report the added parameters (M) and inference time (ms) of our newly proposed modules relative to the VLA policy. 

|Methods|_d_= 5|Success<br>_d_= 10|Rate (%)<br>_d_= 15|_d_= 20|Param.|Time|
|---|---|---|---|---|---|---|
|Baseline|26.1|8.4|2.5|0.7|450.0|35.4|
|+SCM|45.9|18.1|10.4|5.8|+0.04|+1.15|
|+OPM|74.1|70.4|70.0|67.5|+5.19|+3.04|
|+_L_policy (Ours)|75.8|73.3|71.6|69.4|-|-|


#### **Ablation and Analysis** 

We conduct a series of ablations to evaluate our newly proposed components. The average success rate of the LIBERO benchmark using SmolVLA-450M is reported in Table 2. 

We first construct a Baseline that feeds the stale pair ( _ot_ + _K−d, st_ + _K−d_ ) directly into the policy and executes the resulting chunk from index [0: _K −_ 1]. Without any compensation, as reported in row 1 of Table 2, the success rate deteriorates rapidly as the delay increases, demonstrating the severe impact of prediction-execution misalignment. Introducing only our State Correction Module (SCM), i.e., row 2 of Table 2, which replaces the stale state with the corrected state ˆ _st_ + _K_ while retaining the stale observation, improves the low-delay results but remains ineffective under large delays, proving that stale visual observation, not only the proprioceptive state, is also the bottleneck under asynchronous execution. In contrast, further introducing the Observation Prediction Module (OPM), i.e., row 3 of Table 2, which supplies the execution-time visual latent representation _z_ ˆ _t_ + _K_ , provides substantial improvements. Moreover, we additionally employ the policy consistency loss _L_ policy to align the predicted observation-state pair with the distribution expected by the VLA policy, thus introducing overall performance improvements as reported in row 4 of Table 2. 

Finally, the last two columns report the computational overhead of the proposed adapter, which introduces only 5.19 M additional parameters and 3.04 ms of inference latency, indicating that our method achieves substantial performance improvements with limited computational overhead. 

#### **Real-World Evaluation** 

**Setup.** We deploy FutureRTC on a dual-arm AgileX Cobot Magic robot using _π_ 0 _._ 5 as the VLA backbone with an execution horizon of _K_ = 25. The robot operates at a control frequency of 30Hz, corresponding to the control period of ∆ _t ≈_ 33ms. Without any test-time strategy, a single forward pass of the VLA requires approximately 99ms. Since the policy is served on a remote machine, an additional _∼_ 40ms is incurred by LAN communication, while data processing and disk logging contribute another _∼_ 30ms. The resulting endto-end latency is _∼_ 170ms, corresponding to an inference delay of about _d_ = 5. To emulate more challenging remote or resource-constrained deployment scenes, we further inject an additional 150ms latency, extending the delay to _d_ = 10. **Task Design and Measurement.** We evaluate our method 


Figure 6: Real-world comparison on three bimanual manipulation tasks, _Stack Plates_ , _Fold Towel_ , and _Hang Cups_ , with _π_ 0 _._ 5 (Black et al. 2025a) as the VLA policy. 

and competitive methods, including Naive Async., RTC, and VLASH, on three bimanual manipulation tasks: (1) _Stack Plates_ , stacking the left and right plates onto the middle one; (2) _Fold Towel_ , folding a towel with both arms to form a compact square; and (3) _Hang Cups_ , hanging the left and right cups onto the corresponding sides of a rack, respectively. For each task, we collect 100 demonstrations to fine-tune _π_ 0 _._ 5. Evaluations are conducted across 20 trials per task, in which the initial position and orientation of the object are randomized. The maximum execution steps are strictly limited to 400, 450, and 400 for the three tasks, respectively. 

As illustrated in Fig. 6, our FutureRTC consistently achieves the highest success rates, as well as the fewest execution steps and times across three tasks, particularly as latency increased. While Naive Async. degrades sharply, RTC and VLASH offer only partial relief from prediction-execution misalignment, ultimately falling short of FutureRTC in terms of effectiveness and efficiency. With the ability to predict execution-time context, FutureRTC maintains reliable and smooth operation even in the presence of remarkable inference latency, indicating that the robustness observed in simulations has effectively transferred to real-world operations. **We provide more comprehensive real-world experimental analysis in the appendix.** 

### **Conclusion** 

We have presented FutureRTC, a plug-and-play adaptation framework for mitigating the prediction-execution misalignment inherent in asynchronous VLA execution. Specifically, FutureRTC anticipates the execution-time context by correcting rolled-forward proprioceptive states and predicting future visual representations through the proposed state correction module and observation prediction module, respectively, enabling the VLA policy to generate actions conditioned on the observation and state at execution time. Moreover, the policy consistency loss is introduced to encourage the predicted context to be faithfully consumed by the policy. Extensive experiments on simulated benchmarks and real-world manipulation tasks demonstrate that FutureRTC consistently improves delay robustness, execution smoothness, task efficiency, and success rates across VLA backbones. 

**Acknowledgements.** This work was supported by the National Natural Science Foundation of China (NSFC) under grants No.625B2123, No.62372091, and No.52502425, and the Hainan Province Science and Technology Plan Project under grant ZDYF2024(LALH)001. 

### **References** 

Bjorck, J.; Castañeda, F.; Cherniadev, N.; Da, X.; Ding, R.; Fan, L.; Fang, Y.; Fox, D.; Hu, F.; Huang, S.; et al. 2025. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ . 2 

Black, K.; Brown, N.; Darpinian, J.; Dhabalia, K.; Driess, D.; Esmail, A.; Equi, M. R.; Finn, C.; Fusai, N.; Galliker, M. Y.; et al. 2025a. _π_ 0 _._ 5: a Vision-Language-Action Model with Open-World Generalization. In _Annual Conference on Robot Learning_ . 1, 2, 3, 6, 7, 10, 11, 12, 13, 15, 17 

Black, K.; Brown, N.; Driess, D.; Esmail, A.; Equi, M.; Finn, C.; Fusai, N.; Groom, L.; Hausman, K.; Ichter, B.; et al. 2025b. _π_ 0: A Vision-Language-Action Flow Model for General Robot Control. In _Proceedings of Robotics: Science and Systems_ . 1, 2, 3 

Black, K.; Galliker, M.; and Levine, S. 2025. Real-Time Execution of Action Chunking Flow Policies. In _Advances in Neural Information Processing Systems_ , volume 38, 33383– 33407. 1, 2, 3, 5, 6, 11, 12, 14 

Black, K.; Ren, A. Z.; Equi, M.; and Levine, S. 2025c. Training-Time Action Conditioning for Efficient Real-Time Chunking. _arXiv preprint arXiv:2512.05964_ . 2, 3, 5 Cadene, R.; Alibert, S.; Capuano, F.; Aractingi, M.; Zouitine, A.; Kooijmans, P.; Choghari, J.; Russi, M.; Pascal, C.; Palma, S.; et al. 2026. LeRobot: An Open-Source Library for End-to-End Robot Learning. In _International Conference on Learning Representations_ . 6 

Chi, C.; Xu, Z.; Feng, S.; Cousineau, E.; Du, Y.; Burchfiel, B.; Tedrake, R.; and Song, S. 2025. Diffusion Policy: Visuomotor Policy Learning via Action Diffusion. _The International Journal of Robotics Research_ , 44(10-11): 1684–1704. 2 

Ho, T.-B.; Nguyen, Q.-T.; Ha, T.-L.; Nguyen, G.-B.; Nguyen, V.-T.; Dinh, L.; Vu, M. N.; Nguyen, D. M.; Le, A. T.; and Vien, N. A. 2026. Start Right, Arrive Right: Asynchronous Execution via Initial Noise Selection. _arXiv preprint arXiv:2606.19774_ . 2, 3 

Kawaharazuka, K.; Matsushima, T.; Gambardella, A.; Guo, J.; Paxton, C.; and Zeng, A. 2024. Real-world robot applications of foundation models: A review. _Advanced Robotics_ , 38(18): 1232–1254. 2 

Kim, M. J.; Pertsch, K.; Karamcheti, S.; Xiao, T.; Balakrishna, A.; Nair, S.; Rafailov, R.; Foster, E. P.; Sanketi, P. R.; Vuong, Q.; et al. 2024. OpenVLA: An Open-Source VisionLanguage-Action Model. In _Annual Conference on Robot Learning_ . 1, 2 

Kingma, D. P.; and Ba, J. 2015. Adam: A Method for Stochastic Optimization. In _International Conference on Learning Representations_ . 5 

Lipman, Y.; Chen, R. T. Q.; Ben-Hamu, H.; Nickel, M.; and Le, M. 2023. Flow Matching for Generative Modeling. In _International Conference on Learning Representations_ . 2, 3 

Liu, B.; Zhu, Y.; Gao, C.; Feng, Y.; Liu, Q.; Zhu, Y.; and Stone, P. 2023. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36: 44776–44791. 5, 6, 7, 10, 11, 13, 15, 16, 17 

Liu, S.; Wu, L.; Li, B.; Tan, H.; Chen, H.; Wang, Z.; Xu, K.; Su, H.; and Zhu, J. 2025a. Rdt-1b: a diffusion foundation model for bimanual manipulation. In _International Conference on Learning Representations_ , 29982–30009. 2 

Liu, Y.; Hamid, J.; Xie, A.; Lee, Y.; Du, M.; and Finn, C. 2025b. Bidirectional Decoding: Improving Action Chunking via Guided Test-Time Sampling. In _International Conference on Learning Representations_ , 4594–4627. 2, 3, 5 

Liu, Y.; Yu, H.; Zhao, J.; Li, B.; Zhang, D.; Li, M.; Wu, W.; Hu, Y.; Xie, J.; Guo, J.; et al. 2026. Learning Native Continuation for Action Chunking Flow Policies. In _Proceedings of Robotics: Science and Systems_ . 3 

Ma, Y.; Zhou, Y.; Yang, Y.; Wang, T.; and Fan, H. 2025. Running VLAs at Real-Time Speed. _arXiv preprint arXiv:2510.26742_ . 2 

Sendai, K.; Alvarez, M.; Matsushima, T.; Matsuo, Y.; and Iwasawa, Y. 2025. Leave No Observation Behind: Realtime Correction for VLA Action Chunks. _arXiv preprint arXiv:2509.23224_ . 3 

Shukor, M.; Aubakirova, D.; Capuano, F.; Kooijmans, P.; Palma, S.; Zouitine, A.; Aractingi, M.; Pascal, C.; Russi, M.; Marafioti, A.; et al. 2025. Smolvla: A vision-language-action model for affordable and efficient robotics. _arXiv preprint arXiv:2506.01844_ . 2, 3, 6, 7, 10, 11, 13, 16, 17 

Tang, J.; Sun, Y.; Zhao, Y.; Yang, S.; Lin, Y.; Zhang, Z.; Hou, J.; Lu, Y.; Liu, Z.; and Han, S. 2025. VLASH: RealTime VLAs via Future-State-Aware Asynchronous Inference. _arXiv preprint arXiv:2512.01031_ . 1, 2, 3, 4, 5, 11, 12 

Wang, H.; Zhang, G.; Yan, Y.; Shang, Y.; Kompella, R. R.; and Liu, G. 2026a. Real-Time Robot Execution with Masked Action Chunking. In _International Conference on Learning Representations_ . 2, 3, 5, 11, 12 

Wang, P.; Hong, K.; Peng, C.; Driggs-Campbell, K.; Tomizuka, M.; Xu, C.; and Tang, C. 2026b. DiscreteRTC: Discrete Diffusion Policies are Natural Asynchronous Executors. _arXiv preprint arXiv:2604.25050_ . 2, 3, 5 

Wen, J.; Zhu, Y.; Li, J.; Tang, Z.; Shen, C.; and Feng, F. 2025. DexVLA: Vision-Language Model with Plug-In Diffusion Expert for General Robot Control. In _Annual Conference on Robot Learning_ , 3094–3114. 2 

Wu, W.; Lu, F.; Wang, Y.; Yang, S.; Liu, S.; Wang, F.; Zhu, Q.; Sun, H.; Wang, Y.; Ma, S.; et al. 2026. A Pragmatic VLA Foundation Model. _arXiv preprint arXiv:2601.18692_ . 2 

Yang, C.; Hu, Y.; Ma, Y.; Yang, Y.; Tan, J.; and Fan, H. 2026. Realtime-VLA V2: Learning to Run VLAs Fast, Smooth, and Accurate. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops_ , 4501– 4509. 10 

Ze, Y.; Zhang, G.; Zhang, K.; Hu, C.; Wang, M.; and Xu, H. 2024. 3D Diffusion Policy: Generalizable Visuomotor Policy 

Learning via Simple 3D Representations. In _Proceedings of Robotics: Science and Systems_ . 2 

Zhao, T.; Kumar, V.; Levine, S.; and Finn, C. 2023. Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware. In _Proceedings of Robotics: Science and Systems_ . 2, 3, 5 

Zhong, L.; Liu, Y.; Wei, Y.; Xiong, Z.; Liu, S.; and Ren, G. 2026. Acot-vla: Action chain-of-thought for visionlanguage-action models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 8152–8162. 2 

# **Appendices** 

This appendix is organized as follows: 

- **Sec. More Detailed Analysis** formally defines real-time robot execution, analyzes the impact of the predictionexecution misalignment, and reports the computational efficiency and trajectory smoothness of our method. 

- **Sec. Real-world Evaluation** details the video comparisons, hardware setup, task design, and policy implementation of our real-world experiments. 

- **Sec. Simulated Evaluation** presents the per-task results on Kinetix and the detailed per-suite results on LIBERO. 

- **Sec. Ablation Study** reports the complete ablation of our proposed components on both SmolVLA-450M and _π_ 0 _._ 5. 

- **Sec. Limitations** discusses the limitations and future directions of our method. 

### **More Detailed Analysis** 

#### **Definition of Real-Time Robot Execution** 

VLA policies are typically trained on demonstrations under the idealized assumption of instantaneous observation acquisition and immediate action execution. During deployment, however, generating an action chunk incurs a non-negligible inference latency _δ_ , compounded by hardware-level communication, readout, and actuation delays. Following (Yang et al. 2026), we define real-time robot execution as the continuous, stall-free operation of the VLA policy at a target control frequency, satisfying three core criteria: 

- **Accurate.** The policy reliably completes the intended task with a high success rate. 

- **Smooth.** The commanded trajectory is smooth, free of abrupt accelerations and jerky motions. 

- **Fast.** The policy completes the task in fewer control steps and less wall-clock time. 

Satisfying the above three criteria exposes a fundamental tension between synchronous and asynchronous execution. Synchronous execution conditions the policy on the latest observation and proprioceptive state, thereby preserving action accuracy, but forces the robot to idle during every chunk inference, producing stalls that directly violate the fast criterion. Asynchronous execution eliminates stalls by generating the next action chunk in parallel with the execution of the current one. However, each chunk is conditioned on observations and states that have already become stale by the time it is executed, giving rise to the _prediction-execution misalignment_ . Thus, the generated actions become progressively misaligned with the evolving scene, leading to inter-chunk discontinuities and simultaneously degrading accuracy, smoothness, and execution efficiency as the inference delay increases. 

Overall, real-time control requires the stall-free property of asynchronous execution without sacrificing execution-time alignment that our method aims to address. 

#### **Impact of the Prediction-Execution Misalignment** 

To quantify the individual impact of observation and proprioceptive state staleness under asynchronous execution, we conduct experiments on the LIBERO (Liu et al. 2023) benchmark with _π_ 0 _._ 5 (Black et al. 2025a) and SmolVLA450M (Shukor et al. 2025). At the generation time _t_ + _K − d_ , the policy is conditioned on the stale pair ( _ot_ + _K−d, st_ + _K−d_ ), while the generated chunk is executed at _t_ + _K_ . We isolate the contribution of each modality by selectively replacing stale inputs with their execution-time counterparts, i.e., the ground-truth observation _ot_ + _K_ or state _st_ + _K_ , resulting in four configurations as follows: 

- **Stale observation + stale state** , i.e., _{ot_ + _K−d, st_ + _K−d}_ , corresponding to naive asynchronous execution. 

- **Stale observation + execution-time state** , i.e., _{ot_ + _K−d, st_ + _K}_ , correcting only the state. 

- **Execution-time observation + stale state** , i.e., _{ot_ + _K, st_ + _K−d}_ , correcting only the visual observation. 

- **Execution-time observation + execution-time state** , i.e., _{ot_ + _K, st_ + _K}_ , serving as the delay-free upper bound. 

Moreover, since the appropriate execution of an action chunk **A** depends on whether its conditioning inputs are aligned with the execution time, we further clarify the chunksplicing conventions used in the main paper. **A** [0: _K−_ 1] executes the generated chunk from its first action, which is valid when the conditioning context corresponds to the execution time. In contrast, **A** [ _d_ : _d_ + _K−_ 1] removes the first _d_ actions that overlap with the already committed chunk and executes the remaining actions, following the naive asynchronous convention. We evaluate the above four configurations under both execution conventions to disentangle the impact of stale conditioning inputs from that of chunk-splicing offsets. 

The average success rate across four suites of the LIBERO benchmark is reported in Table 3. We first examine how the chunk-splicing convention interacts with the staleness of the conditioning inputs. Under naive asynchronous execution, the policy is conditioned on the fully stale pair _{ot_ + _K−d, st_ + _K−d}_ . Executing the generated chunk directly from its first action, i.e., **A** [0: _K−_ 1], causes the success rate to collapse rapidly as the delay increases. The reason is that the chunk is generated for the time index _t_ + _K − d_ but executed _d_ steps later. Discarding the first _d_ actions, i.e., executing **A** [ _d_ : _d_ + _K−_ 1], compensates for this temporal offset and substantially improves performance. However, discarding the first _d_ actions is beneficial only when the conditioning inputs are stale. Once the execution-time context becomes available, i.e., the _{ot_ + _K, st_ + _K−d}_ and _{ot_ + _K, st_ + _K}_ , the chunk is generated as if the current step is at _t_ + _K_ , so its first action already corresponds to the execution time. Removing the first _d_ actions then skips into the future, commanding actions intended for _t_ + _K_ + _d_ before the robot has reached the corresponding state. Consequently, **A** [ _d_ : _d_ + _K−_ 1] collapses, whereas **A** [0: _K−_ 1] stays near the upper bound. Hence, whenever the execution-time context can be recovered, the chunk should be executed directly from index [0: _K−_ 1]. 

Under the correct execution convention **A** [0: _K−_ 1], we further compare the four conditioning configurations. Cor- 

Table 3: Analysis of prediction-execution misalignment on the LIBERO (Liu et al. 2023) benchmark, measured by average success rates across four suites, with _π_ 0 _._ 5 (Black et al. 2025a) and SmolVLA-450M (Shukor et al. 2025) as the VLA policies. 

|Backbone|Input||Execute**A**|[0 :_K −_|1]|Ex|ecute**A**[_d_|:_d_+_K _|_−_1]|
|---|---|---|---|---|---|---|---|---|---|
|||_d_= 5|_d_= 10|_d_= 15|_d_= 20|_d_= 5|_d_= 10|_d_= 15|_d_= 20|
||_{ot_+_K−d, st_+_K−d}_|46.9|11.7|5.2|2.5|89.5|82.7|76.3|68.3|
||_{ot_+_K−d, st_+_K}_<br>|47.2|12.4|5.3|1.9|89.7|82.6|73.4|67.6|
|_π_0_._5|_{ot_+_K, st_+_K−d}_|96.3|95.9|95.4|95.8|37.6|4.7|1.3|0.8|
||_{ot_+_K, st_+_K}_|96.6|96.6|96.6|96.6|37.2|6.5|1.6|0.9|
||_{_ˆ_zt_+_K,_ ˆ_st_+_K}_(Ours)|94.2|92.4|91.0|88.5|39.0|7.2|2.6|0.7|
||_{ot_+_K−d, st_+_K−d}_|26.1|8.4|2.5|0.7|70.3|64.5|61.3|56.2|
||_{ot_+_K−d, st_+_K}_|44.6|17.9|10.9|6.6|59.7|31.5|22.1|15.6|
|SmolVLA|_{ot_+_K, st_+_K−d}_|61.7|26.8|18.1|16.4|39.3|7.5|2.3|1.0|
||_{ot_+_K, st_+_K}_<br>|77.6|77.6|77.6|77.6|24.0|4.0|1.9|0.3|
||_{_ˆ_zt_+_K,_ ˆ_st_+_K}_(Ours)|75.8|73.3|71.6|69.4|24.2|3.9|0.7|0.2|


Table 4: The parameters and inference time introduced by our method to _π_ 0 _._ 5 (Black et al. 2025a) and SmolVLA450M (Shukor et al. 2025). 

||_π_0_._|5|Smol|VLA|
|---|---|---|---|---|
|Methods|Param. (M)|Time (ms)|Param. (M)|Time (ms)|
|Base|3616.8|98.8|450.0|35.4|
|+FutureRTC|+6.45|+3.64|+5.19|+3.04|


recting only the state, i.e., _ot_ + _K−d, st_ + _K_ , yields little improvement over the fully stale baseline on _π_ 0 _._ 5, which is consistent with its proprioceptive state being encoded as textual tokens within the language input. In contrast, state correction brings a more noticeable gain on SmolVLA, whose continuous state is projected through a dedicated linear layer into a separate state token directly attended by the action expert. Moreover, correcting only the observation, i.e., _{ot_ + _K, st_ + _K−d}_ , recovers the majority of the performance gap. These results demonstrate that the stale visual observation, not only the stale state, is also a dominant source of prediction-execution misalignment. 

Finally, when both the execution-time observation and state are supplied, i.e., _{ot_ + _K, st_ + _K}_ with **A** [0: _K−_ 1], the success rate remains constant across all delays, matching the delay-free performance. This result indicates that asynchronous execution itself incurs no performance penalty, provided that the policy is conditioned on the correct executiontime context. Since such context is unavailable at generation time, FutureRTC instead predicts the execution-time observation _z_ ˆ _t_ + _K_ and state _s_ ˆ _t_ + _K_ from their stale counterparts, enabling the policy to operate as if the delay did not exist and thereby approach this delay-invariant upper bound. 

#### **Computational Efficiency** 

We evaluated the computational efficiency of our method in terms of the parameters and inference time introduced to the base VLA policies _π_ 0 _._ 5 (Black et al. 2025a) and 


Figure 7: Average action velocity and acceleration on the LIBERO (Liu et al. 2023) benchmark under _d_ = 5 for _π_ 0 _._ 5 (Black et al. 2025a) (a) and SmolVLA-450M (Shukor et al. 2025) (b), comparing RTC (Black, Galliker, and Levine 2025), VLASH (Tang et al. 2025), REMAC (Wang et al. 2026a), and our FutureRTC. The left panel plots the action velocity (rad _/_ s) and the right panel the action acceleration (rad _/_ s<sup>2</sup> ) during execution, where previous methods exhibit pronounced acceleration spikes at the chunk boundaries, whereas FutureRTC produces smoother trajectories. 

SmolVLA-450M (Shukor et al. 2025). As reported in Table 4, our method introduces only marginal overhead on both VLA policies, adding 6.45M parameters and 3.64ms inference latency to _π_ 0 _._ 5, and 5.19M parameters and 3.04ms to SmolVLA, showing that FutureRTC achieves robust realtime execution at limited computational cost. 

#### **Trajectory Smoothness Analysis** 

To evaluate the smoothness criterion, we analyze the kinematic properties of the executed actions on the LIBERO (Liu et al. 2023) benchmark across all four suites, comparing FutureRTC with representative baselines including RTC (Black, Galliker, and Levine 2025), VLASH (Tang et al. 


Figure 8: Real-world experimental platform. **(a)** The AgileX Cobot Magic robot. **(b)** The workspace of the three bimanual tasks, containing the plates, towel, and cups with a cup rack. 

2025), and REMAC (Wang et al. 2026a). Fig. 7 reports the average action velocity and acceleration profiles during execution for each backbone, where previous methods suffer from pronounced spikes caused by inter-chunk discontinuities. In contrast, VLASH partially mitigates the spikes by conditioning on the forward-predicted future state, yet it remains less smooth than our approach owing to the lack of execution-time observation as input for action prediction. By anticipating the execution-time context, our FutureRTC consistently produces the smoothest trajectories. 

### **Real-world Evaluation** 

To qualitatively demonstrate the real-world execution behavior of FutureRTC, we provide side-by-side comparison videos in the Project Website. For each of the three real-world bimanual tasks, i.e., _Stack Plates_ , _Fold Towel_ , and _Hang Cups_ , we visualize executions of Naive Async., RTC (Black, Galliker, and Levine 2025), VLASH (Tang et al. 2025), and FutureRTC under asynchronous inference. The videos show that FutureRTC generates smoother and more decisive motions with fewer hesitations, while achieving more reliable task completion, whereas the baselines exhibit jerky transitions and delayed completion. 


Figure 9: Example demonstration sequences of the three realworld tasks: _Stack Plates_ , _Fold Towel_ , and _Hang Cups_ . 

- **Fold Towel** : the two arms fold a flattened towel with two successive folds into a compact square. 

- **Hang Cups** : the two arms pick up the left and right cups and hang them onto the corresponding branches of a rack. 

For each task, we collect 100 teleoperated demonstrations for policy fine-tuning, with the initial object positions and orientations randomized across demonstrations. We illustrate the demonstration data of the three tasks in Fig. 9. 

#### **Policy Implementation** 

To obtain a task-competent policy, we fine-tune _π_ 0 _._ 5 (Black et al. 2025a) on the collected demonstrations of each task for 30k iterations. This fine-tuned policy is kept frozen and shared across the inference-time methods, including Naive Async. and RTC, and our method, consistent with the plugand-play setting used throughout the main paper. The finetuning hyperparameters are summarized in Table 5. For the training-based method VLASH, we adopt the officially released implementation to fine-tune it on _π_ 0 _._ 5. 

#### **Hardware Setup** 

We conduct real-world experiments on a dual-arm AgileX Cobot Magic robot<sup>1</sup> equipped with three RGB cameras, i.e., two wrist-mounted cameras and one global camera mounted on the central mast, as shown in Fig. 8 (a). We also illustrate the objects used in three tasks in Fig. 8 (b), i.e., the plates, towel, and cups with a cup rack used in _Stack Plates_ , _Fold Towel_ , and _Hang Cups_ , respectively. 

#### **Task Design** 

We design three bimanual manipulation tasks to evaluate coordinated two-arm control under asynchronous execution: 

- **Stack Plates** : the two arms grasp the left and right plates and stack them onto the middle plate to form a single pile. 

> 1https://global.agilex.ai/products/cobot-magic 

### **Simulated Evaluation** 

**Kinetix.** We report the per-task success rates across all 12 Kinetix environments under inference delays _d ∈_ [0 _,_ 4] in Fig. 10. FutureRTC demonstrates consistently robust performance across diverse environments, exhibiting the smallest and most consistent degradation as the delay increases, without the abrupt failures observed in other comparison methods on individual tasks. Although FutureRTC does not dominate every individual environment, its consistent robustness across diverse dynamics yields the strongest overall performance under varying inference delays. 

**LIBERO.** We report the per-suite success rate (SR) and execution steps on the four LIBERO suites in Tables 6 and 7 for _π_ 0 _._ 5 and SmolVLA-450M, respectively, complementing the averaged results in the main paper. We additionally include the synchronous (Sync.) execution results as reference, i.e., 

Table 5: The hyperparameters adopted for fine-tuning _π_ 0 _._ 5 on the real-world demonstrations. 

or discrete-diffusion policies, and more extreme inference delays remains an interesting direction for future work. 

|Hyperparameter|Value|
|---|---|
|Base policy|_π_0_._5|
|Fine-tuning scheme|Full fine-tuning<br>|
|Optimizer|AdamW (_β_1=0_._9,_β_2=0_._95,_ϵ_=10<sup>_−_8</sup>)<br>|
|Weight decay|1_×_10<sup>_−_10</sup>|
|LR schedule|Cosine,1_,_000warmup steps<br>|
|Peak / final learning rate|2_._5_×_10<sup>_−_5 </sup>/2_._5_×_10<sup>_−_6</sup>|
|Training steps|30_,_000|
|Batch size|8|
|Action horizon (_H_)|50|
|Random seed|42|
|# Demonstrations per task|100|
|Training hardware|4_×_NVIDIA RTX 4090 24GB|


_d_ = 0. FutureRTC consistently achieves the highest success rate and the fewest execution steps across all suites and delay settings, with the largest performance gains observed on the long-horizon suite, i.e., Long, where prediction-execution misalignment accumulates most severely. 

### **Ablation Study** 

We report the detailed ablation results of _π_ 0 _._ 5 (Black et al. 2025a) and SmolVLA-450M (Shukor et al. 2025) on the LIBERO (Liu et al. 2023) benchmark across four suites and all delays _d ∈{_ 5 _,_ 10 _,_ 15 _,_ 20 _}_ in Table 8. We first construct a Baseline that feeds the stale pair ( _ot_ + _K−d, st_ + _K−d_ ) directly into the policy and executes the resulting chunk from index [0: _K−_ 1], in which the success rate deteriorates rapidly as the delay increases on each suite and both backbones, demonstrating the severe impact of the prediction-execution misalignment. Introducing only the State Correction Module (SCM), which replaces the stale state with the corrected state _s_ ˆ _t_ + _K_ while retaining the stale observation, yields limited improvement that stays far from recovering the performance under large delays, proving that the stale visual observation is also a critical bottleneck under asynchronous execution. Further introducing the Observation Prediction Module (OPM), which supplies the execution-time visual latent representation _z_ ˆ _t_ + _K_ , provides substantial improvements across all suites and delays. Finally, we employ the policy consistency loss _L_ policy to align the predicted observation-state pair with the distribution expected by the policy, bringing a further consistent performance gain. 

### **Limitations** 

While FutureRTC substantially improves the robustness of asynchronous VLA execution, it still has several limitations. First, the observation prediction module models visual changes through motion-driven feature transport and residual synthesis. While highly effective in manipulation scenes where the robot is the primary source of environmental change, it may struggle in highly dynamic scenes dominated by independent external agents. Second, our current framework is instantiated on flow-matching VLA policies with latent-space observation prediction. Extending FutureRTC to other policy architectures, such as autoregressive 


Figure 10: Performance comparison in the Kinetix simulator (Black, Galliker, and Levine 2025) with different methods across various inference delays _d ∈_ [0 _,_ 4]. **Left:** Success rate for individual tasks. **Right:** Average success rate and execution steps. 

Table 6: Detailed performance comparison of _π_ 0 _._ 5 (Black et al. 2025a) in the LIBERO (Liu et al. 2023) benchmark with different methods across various inference delays _d ∈{_ 5 _,_ 10 _,_ 15 _,_ 20 _}_ . “Infer.” and “Train.” denote the methods that are categorized as inference-time and training-time, respectively. “SR” and “Steps” indicate success rate and execution steps, respectively. 

||||Sp|atial|O|bject|G|oal|L|ong|Av|erage|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Methods|delay|SR_↑_|Steps_↓_|SR_↑_|Steps_↓_|SR_↑_|Steps_↓_|SR_↑_|Steps_↓_|SR_↑_|Steps_↓_|
||Sync.|0|96.6|107.6|98.0|137.8|95.0|117.5|96.8|260.6|96.6|155.8|
|||5|90.8|113.0|90.4|147.9|91.0|125.6|85.8|289.4|89.5|169.0|
|||10|83.2|123.4|85.0|155.8|89.8|127.3|72.6|325.5|82.7|183.0|
||Naive Async.|15|79.6|128.6|77.4|166.7|87.8|131.5|60.2|359.5|76.3|196.6|
|||20|67.6|142.0|77.0|167.5|83.6|137.0|45.0|397.2|68.3|210.9|
|||5|91.0|114.4|88.6|150.1|93.0|122.0|78.6|305.5|87.8|173.0|
|||10|87.4|118.7|84.8|155.7|92.0|124.1|73.0|321.9|84.3|180.1|
||TE|15|81.0|126.3|81.2|161.4|90.8|125.2|69.2|330.3|80.6|185.8|
|Infer||20|74.0|134.1|77.6|167.0|88.6|128.3|59.0|358.5|74.8|197.0|
|||5|91.6|113.0|90.6|148.3|91.4|124.6|87.4|286.9|90.3|168.2|
|||10|85.8|121.4|83.4|157.9|89.8|127.2|77.0|315.7|84.0|180.5|
||BID|15|82.0|125.0|78.4|166.4|85.4|135.8|58.6|361.9|76.1|197.3|
|||20|71.4|137.7|78.4|166.5|85.2|135.3|50.2|383.8|71.3|205.8|
|||5|91.4|113.1|89.4|149.2|91.6|124.8|87.0|286.5|89.9|168.4|
|||10|84.2|122.0|84.2|156.9|90.4|127.2|73.8|320.5|83.2|181.6|
||RTC|15|80.0|128.2|78.6|166.0|88.8|130.0|62.4|352.8|77.5|194.2|
|||20|71.6|137.3|79.0|165.0|86.0|134.9|58.0|364.9|73.7|200.5|
|||5|87.4|118.4|88.6|150.2|93.6|121.2|87.8|284.3|89.4|168.5|
|||10|82.2|123.4|83.4|157.6|91.0|125.0|79.4|304.8|84.0|177.7|
||T-RTC|15|81.8|123.7|78.8|164.9|89.8|127.8|61.2|356.2|77.9|193.1|
|||20|74.0|134.9|76.4|170.2|86.2|133.9|59.2|361.5|74.0|200.1|
|||5|87.9|119.1|87.4|151.8|93.2|121.8|83.4|295.0|88.0|171.9|
|||10|82.4|123.7|84.2|156.5|88.4|128.8|78.6|306.8|83.4|178.9|
||VLASH|15|77.3|129.7|78.4|165.4|88.2|130.1|74.2|324.5|79.5|187.4|
|||20|76.2|132.0|75.4|171.5|79.0|144.4|67.3|341.7|74.5|197.4|
|Train.||5|90.6|114.2|91.0|147.9|94.0|119.5|87.6|284.6|90.8|166.6|
|||10|87.8|117.7|85.2|155.4|91.6|123.8|77.0|313.3|85.4|177.6|
||REMAC|15|82.0|125.3|80.6|162.2|90.0|127.3|61.4|355.7|78.5|192.6|
|||20|74.2|134.1|79.4|163.4|87.2|130.7|54.8|370.1|73.9|199.6|
|||5|95.0|109.6|96.2|140.4|93.6|120.5|91.8|279.1|94.2|162.4|
|||10|95.0|110.8|93.8|143.3|93.4|121.5|87.4|291.9|92.4|166.9|
||FutureRTC|15|93.2|112.5|94.0|142.7|92.2|123.0|84.4|302.0|91.0|170.1|
|||20|90.4|115.8|92.6|145.8|90.8|125.3|80.2|313.7|88.5|175.1|


Table 7: Detailed performance comparison of SmolVLA-450M (Shukor et al. 2025) in the LIBERO (Liu et al. 2023) benchmark with different methods across various inference delays _d ∈{_ 5 _,_ 10 _,_ 15 _,_ 20 _}_ . 

||||Sp|atial|O|bject|G|oal|L|ong|Av|erage|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Methods|delay|SR_↑_|Steps_↓_|SR_↑_|Steps_↓_|SR_↑_|Steps_↓_|SR_↑_|Steps_↓_|SR_↑_|Steps_↓_|
||Sync.|0|77.8|128.2|85.4|156.2|83.4|139.9|63.8|355.2|77.6|194.9|
|||5|71.6|135.6|75.0|168.6|81.0|142.9|53.6|378.4|70.3|206.4|
||Ni A|10|68.0|139.0|71.6|173.8|77.0|150.1|41.4|409.8|64.5|218.2|
||ave sync.|15|65.2|142.5|71.6|173.7|72.2|157.1|36.2|423.4|61.3|224.2|
|||20|55.8|154.1|72.4|172.3|67.4|164.9|29.2|440.0|56.2|232.8|
|||5|69.0|138.1|76.6|165.9|79.0|145.0|49.0|386.2|68.4|208.8|
||TE|10|66.6|140.5|76.4|166.4|78.2|146.6|45.6|398.1|66.7|212.9|
|Infer||15|59.8|148.7|75.4|167.6|75.6|151.8|39.6|411.6|62.6|220.0|
|||20|54.8|154.8|72.0|173.1|74.2|153.1|37.8|415.8|59.7|224.2|
|||5|73.0|134.0|75.4|167.8|80.2|144.5|51.4|384.2|70.0|207.6|
|||10|67.8|139.5|71.2|174.5|78.0|147.2|42.8|404.6|65.0|216.4|
||BID|15|65.8|141.9|71.2|174.4|73.2|156.0|36.4|419.8|61.7|223.0|
|||20|53.8|156.6|72.4|172.6|68.4|162.1|33.6|426.4|57.1|229.4|
|||5|73.4|133.8|75.0|168.6|79.6|145.0|50.6|385.0|69.7|208.1|
|||10|67.8|139.5|71.2|174.5|77.2|148.7|43.2|405.3|64.9|217.0|
||RTC|15|65.6|142.1|71.0|174.6|73.8|155.3|40.0|411.7|62.6|220.9|
|||20|57.6|151.1|71.2|174.3|69.2|161.5|36.6|418.2|58.7|226.3|
|||5|74.4|133.1|71.2|175.4|77.2|151.3|56.6|375.1|69.9|208.7|
|||10|72.4|134.2|67.8|180.2|76.0|153.0|46.2|395.8|65.6|215.8|
||T-RTC|15|67.4|140.0|66.0|182.8|74.0|155.3|39.2|410.0|61.7|222.0|
|||20|63.8|144.5|66.6|181.7|69.8|161.9|37.2|418.2|59.4|226.6|
|||5|70.8|136.1|77.4|167.3|77.8|149.2|51.2|381.5|69.3|208.5|
|||10|66.2|141.8|71.4|174.7|78.0|149.3|47.4|404.7|65.8|217.6|
||VLASH|15|67.0|140.4|64.8|183.0|80.6|144.0|46.2|394.8|64.7|215.6|
|Train.||20|64.8|143.9|60.4|190.1|76.8|150.6|45.6|399.1|61.9|220.9|
|||5|73.0|133.8|77.4|165.5|81.2|142.2|52.0|383.4|70.9|206.2|
|||10|69.4|138.0|72.2|173.1|78.0|147.5|46.4|395.5|66.5|213.5|
||REMAC|15|66.0|141.6|70.8|175.2|73.2|154.6|38.8|412.1|62.2|220.9|
|||20|59.6|148.6|71.6|173.7|72.4|155.9|35.2|421.4|59.7|224.9|
|||5|77.2|129.4|83.6|158.4|82.4|140.7|59.8|366.2|75.8|198.7|
|||10|75.4|131.6|82.0|160.8|80.4|142.9|55.4|375.5|73.3|202.7|
||FutureRTC|15|72.2|135.3|79.6|164.6|81.6|142.9|52.8|382.6|71.6|206.4|
|||20|72.8|134.8|75.0|170.8|79.4|143.5|50.2|388.7|69.4|209.4|


Table 8: Detailed ablation results on the LIBERO (Liu et al. 2023) benchmark across the four suites with various inference delays _d ∈{_ 5 _,_ 10 _,_ 15 _,_ 20 _}_ , using frozen _π_ 0 _._ 5 (Black et al. 2025a) and SmolVLA-450M (Shukor et al. 2025). 

||||||_π_0_._|5||||||
|---|---|---|---|---|---|---|---|---|---|---|---|
|||Sp|atial|O|bject|G|oal|L|ong|Av|erage|
|Methods|dela|||||||||||
||y|SR_↑_|Steps_↓_|SR_↑_|Steps_↓_|SR_↑_|Steps_↓_|SR_↑_|Steps_↓_|SR_↑_|Steps_↓_|
||5|21.8|204.1|53.0|240.4|67.2|187.2|45.6|433.5|46.9|266.3|
||10|2.4|218.7|1.6|279.8|36.6|240.2|6.0|512.2|11.7|312.7|
|Baseline|15|1.0|219.7|0.0|280.0|18.8|273.4|1.0|519.0|5.2|323.0|
||20|0.2|219.9|0.2|280.0|8.2|291.5|1.2|518.7|2.5|327.5|
||5|26.0|200.8|53.8|239.4|65.4|189.6|42.8|435.5|47.0|266.3|
||10|2.6|219.2|2.2|279.6|38.2|237.8|5.0|513.7|12.0|312.6|
|+SCM|15|0.6|219.9|0.2|280.0|18.6|274.1|2.0|517.6|5.4|322.9|
||20|0.4|220.0|0.4|279.8|9.2|289.7|1.6|518.4|2.9|327.0|
||5|95.0|109.6|96.0|140.5|93.8|120.0|92.4|277.0|94.3|161.8|
||10|93.2|111.2|92.8|143.5|92.8|121.6|84.6|300.7|90.9|169.3|
|+OPM|15|91.6|113.5|92.8|143.1|92.0|123.2|82.2|312.0|89.7|173.0|
||20|90.2|115.5|93.8|141.9|89.4|128.5|74.6|329.3|87.0|178.8|
||5|95.0|109.6|96.2|140.4|93.6|120.5|91.8|279.1|94.2|162.4|
||10|95.0|110.8|93.8|143.3|93.4|121.5|87.4|291.9|92.4|166.9|
|+_L_policy|15|93.2|112.5|94.0|142.7|92.2|123.0|84.4|302.0|91.0|170.1|
||20|90.4|115.8|92.6|145.8|90.8|125.3|80.2|313.7|88.5|175.1|


||||||SmolVL|A-450M||||||
|---|---|---|---|---|---|---|---|---|---|---|---|
|||Sp|atial|O|bject|G|oal|L|ong|Av|erage|
|Methods|dela|||||||||||
||y|SR_↑_|Steps_↓_|SR_↑_|Steps_↓_|SR_↑_|Steps_↓_|SR_↑_|Steps_↓_|SR_↑_|Steps_↓_|
||5|10.6|212.0|23.6|262.0|50.6|208.0|19.6|482.7|26.1|291.2|
||10|3.6|219.0|0.4|280.0|24.8|257.7|4.8|514.5|8.4|317.8|
|Baseline|15|0.2|219.9|0.0|280.0|8.6|286.5|1.0|519.6|2.5|326.5|
||20|0.0|220.0|0.0|280.0|1.6|298.5|1.0|519.4|0.7|329.5|
||5|34.2|188.5|56.2|215.2|67.8|179.9|25.4|464.8|45.9|262.1|
||10|11.4|213.6|16.0|273.0|34.6|240.2|10.4|501.4|18.1|307.1|
|+SCM|15|7.8|216.8|7.4|278.1|19.6|269.9|6.6|510.8|10.4|318.9|
||20|3.2|218.7|0.8|279.8|14.2|279.2|5.0|515.8|5.8|323.4|
||5|75.4|131.3|83.2|158.8|84.2|136.8|53.4|380.5|74.1|201.8|
||10|73.4|133.6|78.8|165.2|81.8|141.7|47.6|395.6|70.4|209.0|
|+OPM|15|72.0|135.6|79.6|164.9|83.0|140.0|45.4|402.3|70.0|210.7|
||20|71.8|136.2|75.0|171.5|79.6|145.6|43.4|434.4|67.5|221.9|
||5|77.2|129.4|83.6|158.4|82.4|140.7|59.8|366.2|75.8|198.7|
||10|75.4|131.6|82.0|160.8|80.4|142.9|55.4|375.5|73.3|202.7|
|+_L_policy|15|72.2|135.3|79.6|164.6|81.6|142.9|52.8|382.6|71.6|206.4|
||20|72.8|134.8|75.0|170.8|79.4|143.5|50.2|388.7|69.4|209.4|


