---
title: "DriveMoE: Mixture-of-Experts for Vision-Language-Action Model in End-to-End Autonomous Driving"
date: "2025-05-22"
authors: "Zhenjie Yang; Yilin Chai; Xiaosong Jia; Qifeng Li; Yuqian Shao; Xuekai Zhu"
venue: "CVPR 2026"
url: https://arxiv.org/abs/2505.16278
pdf: https://arxiv.org/pdf/2505.16278
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2505.16278)** / [論文ページ](https://arxiv.org/abs/2505.16278)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **DriveMoE: Mixture-of-Experts for Vision-Language-Action Model in End-to-End Autonomous Driving** 

Zhenjie Yang<sup>1</sup><sup>_,_4</sup><sup>_∗_</sup> Yilin Chai<sup>1</sup><sup>_∗_</sup> Xiaosong Jia<sup>2</sup><sup>_,_3</sup><sup>_∗_</sup> Qifeng Li<sup>1</sup><sup>_,_4</sup> Yuqian Shao<sup>1</sup><sup>_,_4</sup> Xuekai Zhu<sup>1</sup> Haisheng Su<sup>1</sup> Junchi Yan<sup>1</sup><sup>_†_</sup> _∗_ Equal contributions _†_ Correspondence author 

1. Sch. of Computer Science & Sch. of Artificial Intelligence, Shanghai Jiao Tong University 2. Institute of Trustworthy Embodied AI, Fudan University 

   3. Shanghai Key Laboratory of Multimodal Embodied AI 4. AnyScale AI 

Project Page: https://thinklab-sjtu.github.io/DriveMoE/ 

## **Abstract** 

_End-to-end autonomous driving (E2E-AD) demands effective processing of multi-view sensor data and robust handling of diverse and complex driving scenarios, particularly rare maneuvers such as aggressive turns. The recent success of the Mixture-of-Experts (MoE) architectures in Large Language Models (LLMs) demonstrates that expert specialization enables strong scalability. In this work, we propose_ **_DriveMoE_** _, a novel MoE-based E2E-AD framework, with a_ **_Scene-Specialized Vision MoE_** _and a_ **_SkillSpecialized Action MoE_** _. First, we introduce_ **_Drive-π_ 0** _, a Vision-Language-Action (VLA) baseline adapted from Embodied AI for autonomous driving, which serves as the foundation model for DriveMoE. Building on this, we strengthen perception through a carefully designed Vision MoE, where a router adaptively selects context-relevant camera views. This mechanism is inspired by human driving cognition, in which attention is directed to key visual cues rather than to all sensory inputs simultaneously. Beyond perception, we introduce an Action MoE that augments the framework by training a router to activate specialized expert modules tailored to distinct driving behaviors. Within the Action MoE, we implement two distinct styles(Token-level Router and Trajectory-level Router) and extensively explore their applicability in autonomous driving. In Bench2Drive closed-loop evaluations, DriveMoE demonstrates robust_ 

This work was supported by Scientific Research Innovation Capability Support Project for Young Faculty (U40) of the Ministry of Education of China (SRICSPYF-ZY2025019). This work was also in part supported by the Science and Technology Commission of Shanghai Municipality (No. 24511103100) and the New Cornerstone Science Foundation through the XPLORER PRIZE. 

_performance across diverse driving scenarios, alleviates the mode-averaging effect that limits existing models, and achieves state-of-the-art results with significant improvements over Drive-_ **_π_ 0** _._ 

## **1. Introduction** 

Modern autonomous driving has made significant progress [7, 15, 26, 44, 45] with an end-to-end paradigm, which directly maps the raw sensor input into the planning results. This paradigm [20, 49] offers several advantages, such as reduced engineering complexity, mitigation of error propagation, and global objective optimization. Despite the encouraging results achieved on various open-loop self-driving benchmarks [15, 43, 47], existing end-to-end models still fail to get satisfactory performance in closedloop settings [5, 40, 42]. In closed-loop settings, trained driving models can easily encounter out-of-distribution cases [55, 57], requiring stronger generalization and reasoning abilities. Vision Language Models(VLM) and Vision Language Action Models(VLA) have recently gained much attention due to their strong generalization and transferability across domains [3, 11, 19, 29, 34, 41, 50]. To enhance generalization and contextual reasoning, recent work [12, 13, 35, 38, 40, 42, 52] has attempted to introduce VLA into autonomous driving. 

However, existing VLA approaches still face two major limitations. Firstly, existing vision processors of VLA introduce information redundancy and significant computational overhead. As shown in the upper part of Figure 1, there are two distinct strategies for processing multi-view inputs. The first strategy, termed **vanilla vision proces-** 

10678 


Figure 1. **Comparison of Different Vision and Action Modeling Strategies in VLA-based End-to-End Driving.** (a) Vanilla visual token encoding [42] processes all surround-view images through a vision tower, leading to token redundancy and increased computational cost. (b) Query-based token extraction [48] (e.g., Q-Former [30]) selects a subset of visual tokens from each image, but loses spatial structure and requires additional pretraining. (c) Our proposed Scene-Specialized Vision MoE dynamically selects a subset of cameras—typically frontal and a few context-relevant side/rear views, reducing redundancy. (d) Standard action models adopt one policy head to handle all driving scenarios, limiting performance in rare or skill-specific behaviors. (e) Our Skill-Specialized Action MoE, built on a flow-matching planner, activates different experts based on driving intent (e.g., lane following, turning, obstacle avoidance), enabling context-aware and behavior-specialized planning. 

**sor** [5, 17, 18, 40, 42], processes all available camera views at each timestep without distinction, resulting in a substantial computational burden and redundant visual representations, thereby limiting efficiency and scalability. The second strategy, termed **query-based vision processor** , employs learned queries (e.g., Q-Former modules[30]) to extract a compact set of visual tokens guided by semantic context. However, these learned queries typically lead to the loss of precise geometric and positional information and require substantial additional pre-training efforts [37]. Secondly, as shown in the lower part of the Figure 1, current VLA-based frameworks [38, 40] generally employ a single unified policy network designed to handle the full spectrum of driving behaviors. Such uniform approaches tend to bias model training towards more frequent scenarios, thereby insufficiently addressing rare but critical driving maneuvers, such as emergency braking or aggressive turning. This lack of explicit specialization restricts their effectiveness in dynamically changing and highly context-dependent driving 

situations. Addressing these two key limitations demands architectural innovations capable of both context-aware dynamic multi-view selection and explicit fine-grained skill specialization. 

Meanwhile, Mixture-of-Experts (MoE) architectures [4, 46] have significantly advanced Large Language Models (LLMs) [1, 36, 58] by partitioning model capacity into multiple expert modules, scaling to larger model sizes without proportional increases in computational demands. Despite their demonstrated success, the extension of MoE principles into the vision and action domains, particularly within autonomous driving, remains largely under-explored. 

Current end-to-end driving models [24, 39] predominantly rely on predicting trajectory modalities within unified architectures, but lack explicit dynamic expert selection or specialized behavioral adaptation, which limits their scalability. This gap motivates our exploration of MoEbased specialization to enhance both visual perception and decision-making in autonomous driving. Due to limited 

10679 

space, we discuss more details of Related Works in Appendix 5. 

To address these challenges, we propose **_DriveMoE_** , a novel framework built upon our proposed Drive- **_π_ 0** , a Vision-Language-Action (VLA) foundation model extended from the embodied AI model **_π_ 0** [3, 19]. **_DriveMoE_** introduces both a **_Scene-Specialized Vision MoE_** and a **_Skill-Specialized Action MoE_** , carefully designed for endto-end autonomous driving scenarios. DriveMoE dynamically selects contextually relevant camera views and activates skill-specific experts for specialized planning. The Vision MoE employs a learned router to dynamically prioritize camera views aligned with the immediate driving context, integrating projector layers that fuse these selected views into a cohesive visual representation. This approach mirrors human attentional strategies, allowing efficient processing of only critical visual inputs. Concurrently, the Action MoE leverages another routing mechanism to engage distinct experts within a flow-matching planning architecture [32], with each expert dedicated to handling specialized behaviors such as lane following, obstacle avoidance, or aggressive maneuvers. By introducing context-driven dynamic expert selection across both perception and planning modules, DriveMoE ensures efficient resource utilization and robust specialization, significantly improving handling of rare, complex, and long-tail driving behaviors. **The contributions are as follows:** 

- We extend the VLA foundation model **_π_ 0** , originally designed for embodied AI, into the autonomous driving, developing **_Drive-π_ 0** as a unified framework for visual perception, contextual understanding, and action planning. 

- Recognizing differences between embodied AI and autonomous driving, we propose **_DriveMoE_** , the first framework integrating Mixture-of-Experts (MoE) into perception and decision-making to address inefficiencies in multi-view processing and diverse driving behaviors. 

- We design a **_Scene-specialized Vision MoE_** for dynamic camera view selection and a **_Skill-specialized Action MoE_** for behavior-specific planning, addressing challenges of multi-view redundancy and skill specialization. 

- We demonstrate that DriveMoE achieves state-of-the-art (SOTA) performance on the Bench2Drive closed-loop simulation benchmark, significantly improving robustness to rare driving behaviors. 

## **2. Method** 

### **2.1. Preliminary: Drive-** **_π_ 0 Baseline** 

We first establish a strong baseline, Drive- **_π_ 0** , which builds upon the recently proposed **_π_ 0** [3] Vision-Language-Action (VLA) framework from embodied AI, and extends it to the domain of end-to-end autonomous driving. As shown in Figure 2, specifically, the input to Drive- _π_ 0 includes: (i) two 

consecutive front-view images from onboard multi-camera sensors; (ii) a fixed text prompt (e.g., ”Please predict future trajectory”); and (iii) the current vehicle state (e.g., speed, yaw rate, and past trajectory). The network design follows **_π_ 0** framework with pre-trained Paligemma VLM [2] as the backbone and a flow-matching-based action module for planned future trajectory generation. 

### **2.2. Motivation: From Drive-** **_π_ 0 to DriveMoE** 

With Drive- **_π_ 0** as the baseline, we identify two major challenges: (i) adopting VLM to process spatial-temporal surround-view video tokens poses significant challenges to computational resource; (ii) driving performance for rare and difficult scenarios are deficient, even if there is similar data for training. It might be related to the interference effect of different behaviors, as mentioned in the **_π_ 0** paper [3]. Inspired by the recent success of Mixture of Experts (MoE) in VLM field [9, 25], we introduce **DriveMoE** , which extends Drive- **_π_ 0** by adding two Mixture-of-Experts (MoE) modules to tackle the aforementioned challenges: (i) We propose a Scene-Specialized Vision MoE that dynamically selects the most relevant camera views based on the current driving context, effectively reducing redundant visual tokens. (ii) We incorporate a Skill-Specialized Action MoE within a flow-matching transformer to generate more accurate future trajectory distributions tailored to diverse driving skills. Figure 2 illustrates the DriveMoE architecture. 

### **2.3. Scene-Specialized Vision MoE** 

Typical Vision-Language-Action Models (VLAs) [3, 28] usually handle only a single or a few images at a time, whereas autonomous driving must handle multi-view, multi-timestep visual inputs. Concatenating all camera frames into a transformer leads to a visual token bottleneck – an explosion in sequence length that drastically slows training and inference and hampers convergence. Among existing works, [40, 42] adopts a vanilla vision processor to directly handle all visual tokens, while query-based compression modules (e.g. Q-Former [30]) reduce token count but sacrifice spatial structure, often treating images as a “bag of patches” without fine spatial correspondence [37]. 

In this work, we seek a simple and efficient approach that reduces the token load without losing the rich spatial context crucial for driving. **_Inspired by human drivers—who naturally prioritize specific visual information based on driving context_** —we propose a **_Scene-Specialized Vision Mixture-of-Experts (Vision MoE)_** module. Specifically, as shown in Figure 3, our Vision MoE dynamically selects a subset of the most relevant camera views according to the current driving situation and future goal waypoint provided by the route planner. Unlike token-level annotations (which are impractical and costly), camera-view annotations are straightforward and inexpensive, allowing human priors to 

10680 


Figure 2. **Framework of DriveMoE.** Our proposed framework comprises two main Mixture-of-Experts (MoE) modules tailored for endto-end autonomous driving. The Scene-Specialized Vision MoE dynamically selects relevant camera views based on real-time driving contexts, efficiently reducing visual redundancy. Subsequently, selected views are fused into a unified representation by projector layers. The Skill-Specialized Action MoE, integrated within a flow-matching planner, activates expert controllers specifically optimized for distinct driving behaviors such as merging, overtaking, emergency braking, yielding, and responding to traffic signs. This dual MoE structure enhances computational efficiency, adaptability, and robustness to rare, safety-critical driving scenarios. 


Figure 3. **The Scene-Specialized Vision Mixture-of-Experts.** 

be integrated effectively. This dynamic attention strategy significantly reduces the number of visual tokens processed per timestep, greatly improving computational efficiency and decision accuracy. 

Formally, we define the image from camera view _v_ at timestep _t_ as **_I_**<sup>_v_</sup> _t_<sup>,where</sup><sup>_v∈{_1</sup><sup>_,_2</sup><sup>_, . . . , N}_for</sup><sup>_N_avail-</sup> able camera views. In particular, the front-view image at timestep _t_ is denoted by **_I_**<sup>front</sup> _t_ . We introduce a lightweight vision router module **_R_** vision, which takes as inputs the frontview embedding **_e_**<sup>front</sup> _t_ and the future goal waypoint **_g_** _t_ , computing a probability distribution **_p_** _t ∈_ R<sup>_N_</sup> across all views: 


where each element _p_<sup>_v_</sup> _t_<sup>indicates the selection probability of</sup> camera view _v_ at timestep _t_ . Notably, this routing happens before the expensive backbone computation, so views not 

selected can be skipped entirely to save compute. Thus, we obtain the input for VLM: 〈fixed view〉, 〈fixed view〉, 〈dynamic view〉, 〈dynamic view〉, 〈text〉, 〈text〉. 

We further incorporate learnable positional embeddings ( **PE** ) that are unique to each camera viewpoint into their corresponding vision tokens to preserve spatial and positional relation across different camera views. The label for selection of views is annotated by manually designed filters based on future trajectories, bounding box, and maps, detailed in Appendix 9. With the annotated binary cameraview selection labels **_yt_** _∈{_ 0 _,_ 1 _}_ , the vision router is trained using the cross-entropy loss: 


which explicitly encourages the model to proactively select 

10681 


Figure 4. **Token-Level Skill-Specialized Action Mixture-of-Experts.** 

informative camera views relevant for decision-making. _λ_ 0 represents the loss weight of vision router. 

### **2.4. Skill-Specialized Action MoE** 

Human drivers fluidly transition among different driving skills—such as smoothly cruising down a highway, carefully merging into traffic, swiftly overtaking slower vehicles, or urgently braking in response to sudden obstacles. Each of these driving skills is associated with distinct behavioral patterns and trajectory characteristics. Although the original flow-matching decoder of **_π_ 0** could already generate diverse trajectories, employing one single model inevitably averages across these diverse behaviors [3], making the model fail to accurately generate rare yet safetycritical maneuvers. 

To address these issues, inspired by human intuition—where drivers naturally select the appropriate driving skill based on the current context, we propose a SkillSpecialized Action MoE architecture built on the original flow-matching trajectory transformer. The details about flow matching trajectory loss refer to Appendix 6. The central idea is to decompose the policy’s representation of behaviors by replacing each dense feed-forward network (FFN) in the decoder with a Mixture-of-Experts (MoE) layer containing multiple skill-specific experts. Essentially, each decoder layer is no longer a single monolithic mapping, but an ensemble of _K_ expert FFNs each intended to specialize in a subset of driving skills. By conditionally routing each input through a small subset of these experts, the model isolates distinct behavior modes instead of forcing them into a single decoder stream. This design prevents the averaging effect observed in one single model and thereby allocates dedicated model capacity to rare maneuvers. The result is a policy network that preserves the multimodality of the trajectory data, modeling both frequent and infrequent behaviors with appropriate specialization. As illustrated in Figure 4 and Figure 5, we explore two styles of MoE design: token-level (similar to DeepSeek-MoE) and trajectory-level. 

#### **2.4.1. Token-level ActionMoE** 

In Token-level ActionMoE, each token (corresponding to a specific timestep in the trajectory) independently selects its expert(s) based on its local hidden representation. This strategy allows different experts to specialize in modeling short-horizon temporal dependencies—e.g., acceleration, braking, or turning subtasks—within a single trajectory. 

Formally, consider a Transformer decoder layer _ℓ_ with input hidden state **h**<sup>(</sup><sup>_ℓ−_1)</sup> _∈_ R<sup>_d_</sup> . We introduce **K** shared ( _ℓ_ ) ( _ℓ_ ) ( _ℓ_ ) expert models _E_ share1<sup>,</sup><sup>_E_share</sup> 2<sup>,</sup><sup>_. . ._,</sup><sup>_E_share</sup> _K_ and **M** ( _ℓ_ ) ( _ℓ_ ) non-shared expert models _E_ non-share1<sup>,</sup><sup>_E_non-share</sup> 2<sup>,</sup><sup>_. . ._,</sup> ( _ℓ_ ) _E_ non-share _M_<sup>in this layer, each an independent FFN with its</sup> own parameters. Each expert processes the input to produce an output **_y_**<sup>(</sup><sup>_ℓ_)</sup> = _E_<sup>(</sup><sup>_ℓ_)</sup> ( **h**<sup>(</sup><sup>_ℓ−_1)</sup> ). In parallel, an action router **_R_** action computes a set of non-shared routing logits _r_ 1<sup>(</sup><sup>_ℓ_)</sup><sup>_, . . . , r_</sup> _K_<sup>(</sup><sup>_ℓ_)basedonthesameinput.Wethenconvert</sup> these logits into a probability distribution over experts via a softmax: 


It is worth noting that **h** is calculated in the dimension of token num. The updated feature combines the outputs of individual experts weighted by the router’s confidence: 


In practice, we use a sparse activation mechanism [25] to select only a few experts with the highest ranking for calculation (only activate the Top-1 or Top-2 experts), thereby reducing the amount of calculation, preventing mutual interference between experts, and strengthening the degree of expert skill specialization. This sparse routing mechanism is consistent with the mechanism we use in the Vision MoE module, ensuring that each expert clearly focuses on a specific behavior mode. 

10682 


Figure 5. **Trajectory-Level Skill-Specialized Action Mixture-of-Experts.** 

Table 1. **Performance on Bench2Drive Multi-Ability Benchmark** . *: expert feature distillation. 

|**Method**|**Venue**|||**Ability** (%)|_↑_|||
|---|---|---|---|---|---|---|---|
|||Merging|Overtaking|EmergencyBrake|Give Way|Traffic Sign|**Mean**|
|TCP-traj* [49]|NeurIPS 2022|8.89|24.29|51.67|40.00|46.28|34.22|
|AD-MLP [56]|Arxiv 2023|0.00|0.00|0.00|0.00|4.35|0.87|
|UniAD-Base [15]|CVPR 2023|14.10|17.78|21.67|10.00|14.21|15.55|
|ThinkTwice* [22]|CVPR 2023|27.38|18.42|35.82|**50.00**|54.23|37.17|
|VAD [26]|ICCV 2023|8.11|24.44|18.64|20.00|19.15|18.07|
|DriveAdapter* [21]|ICCV 2023|28.82|26.38|48.76|**50.00**|56.43|42.08|
|DriveTrans [24]|ICLR 2025|17.57|35.00|48.36|40.00|52.10|38.60|
|DiffAD[47]|Arxiv 2025|30.00|35.55|46.66|40.00|46.32|38.79|
|Drive-**_π_0** (Ours)||26.25|26.67|45.00|30.00|38.95|33.37|
|DriveMoE (Token-Level)|Ours|**28.75**|**31.11**|**51.67**|40.00|**52.63**|**40.83**|
|DriveMoE (Traj-Level)||**34.67**|**40.00**|**65.45**|40.00|**59.44**|**47.91**|


#### **2.4.2. Trajectory-level ActionMoE** 

In Trajectory-level ActionMoE, instead of routing per token, the router assigns experts at the trajectory level. 

As shown in Figure 5, unlike the token-level Action MoE, this variant averages the entire token sequence before feeding it into the router, effectively performing expert selection along the batch (trajectory) dimension rather than the token dimension. Each trajectory is treated as a single entity representing a specific scenario or driving skill. 

Moreover, to explicitly guide our model toward meaningful skill specialization—mirroring structured and intuitive human-defined skill categories—we utilize driving skill labels _yk ∈{_ 1 _, . . . , K}_ , annotated based on scenarios, and train the skill router via a cross-entropy loss as well: 


Additionally, we optimize the entire Action MoE module using a flow-matching trajectory loss _L_ FM to ensure accurate trajectory predictions: 


where _λ_ 1 represents loss weight of flow matching policy, _λ_ 2 represents loss weight of action router. We introduce noise into the action router following [8], which increases randomness and encourages exploration, effectively mitigating the risk of expert collapse. 

### **2.5. Two Stage Training: From Teacher-Forcing to Adaptive Training** 

DriveMoE loads the Paligemma VLM pretrained weights [2] and we finetune it in the autonomous driving scene via a **_two-stage training_** procedure. In the first stage, both vision and action MoEs only select ground-truth experts while the router is trained jointly, which significantly stabilize the training. In the second stage, we transition to select experts based on the outputs of Vision and Action MoE routers, removing reliance on GT annotation about experts. It develops robustness against potential mistakes or inaccuracies made by routers, thereby enhancing the overall model’s generalization capability under realistic inference conditions. 

## **3. Experiments** 

### **3.1. Datasets & Benchmark & Metric** 

We employ the CARLA simulator [10] (version 0.9.15.1) for closed-loop driving performance evaluation, and adopt the latest public closed-loop evaluation benchmark, Bench2Drive [23] which includes 220 routes with one challenging corner case per route for analysis of different driving abilities. It provides an official training set, where we use the base set (1000 clips, 950 training, 50 test/validation) for fair comparison with all the other baselines. 

10683 

Table 2. **Results on the Bench2Drive Benchmark(Closed-Loop and Open-Loop)** . * denotes expert feature distillation. 

|**Method**|**Venue**||**Close**|**d-loop Metric**||**Open-loop Metric**|
|---|---|---|---|---|---|---|
|||DS _↑_|SR(%) _↑_|Efficiency _↑_|Comfort _↑_|Avg. L2_↓_|
|TCP-traj* [49]|NeurIPS 2022|59.90|30.00|76.54|18.08|1.70|
|AD-MLP [56]|Arxiv 2023|18.05|0.00|48.45|22.63|3.64|
|VAD [26]|ICCV 2023|42.35|15.00|157.94|46.01|0.91|
|UniAD-Base [15]|CVPR 2023|45.81|16.36|129.21|43.58|0.73|
|ThinkTwice* [22]|CVPR 2023|62.44|31.23|69.33|16.22|0.95|
|DriveAdapter* [21]|ICCV 2023|64.22|33.08|70.22|16.01|1.01|
|GenAD [57]|ECCV 2024|44.81|15.90|-|-|-|
|DriveTrans [24]|ICLR 2025|63.46|35.01|100.64|20.78|**0.62**|
|MomAD [43]|CVPR 2025|44.54|16.71|170.21|**48.63**|0.82|
|WoTE [31]|ICCV 2025|61.71|31.36|-|-|-|
|DriveMamba-L [44]|ICLR 2026|66.82|37.73|152.91|18.77|0.70|
|DiffAD [47]|Arxiv 2025|67.92|38.64|-|-|1.55|
|Raw2Drive[53]|NeurIPS 2025|71.36|50.24|214.17|22.42|-|
|Drive-**_π_0**||55.85|30.00|173.63|35.70|1.13|
|DriveMoE (Token-Level)|Ours|66.94|35.45|158.80|6.86|0.96|
|DriveMoE (Traj-Level)||**74.22**|**48.64**|**175.96**|15.31|1.01|


Table 3. **Ablation study on Vision MoE.** Compare different camera view combinations and supervision signals. _F_ , _FL_ , _FR_ , and _B_ indicate the front, front-left, front-right, and back views, respectively, while _BL_ and _BR_ represent the back-left and back-right views. **Fixed View** means selecting a specific view. **Dynamic View** refers to the camera view dynamically selected by the vision router as the top-1 relevant view according to scene context. Exp 1 denotes our baseline **Drive-** **_π_ 0** , which models surrounding agents’ velocities from two consecutive front-view images, and Exp 9 denotes **DriveMoE** , which adds a dynamically selected view with explicit supervision to enhance perception learning. Memory is evaluated at **batch size=1** . **All experiments use the previous-frame front view by default.** 

|**Exp**|_IF_|_IF L_|_IF R_|_IB_|_IBL_|_IBR_|**View**|**Supervision**|**DS**_↑_|**SR(%)**_↑_|**Latency**_↓_|**Memory(MB)**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|1|✓|_×_|_×_|_×_|_×_|_×_|Fixed|-|55.85|30.00|100ms|4100|
|2|✓|✓|_×_|_×_|_×_|_×_|Fixed|-|62.38|33.64|260ms|5100|
|3|✓|_×_|✓|_×_|_×_|_×_|Fixed|-|61.52|32.73|260ms|5100|
|4|✓|_×_|_×_|✓|_×_|_×_|Fixed|-|63.26|31.82|260ms|5100|
|5|✓|✓|✓|_×_|_×_|_×_|Fixed|-|64.92|33.64|400ms|7400|
|6|✓|✓|✓|✓|_×_|_×_|Fixed|-|64.18|33.64|550ms|9600|
|7|✓|✓|✓|✓|✓|✓|Fixed|-|62.27|31.36|700ms|11800|
|8|✓|-|-|-|-|-|Dynamic|_×_|69.71|44.09|260ms|5100|
|9|✓|-|-|-|-|-|Dynamic|✓|74.22|48.64|260ms|5100|


### **3.2. Comparison with State-of-the-Art Methods** 

As shown in Table 2, our proposed method achieves stateof-the-art (SOTA) performance in terms of both driving score and success rate on the Bench2Drive closed-loop benchmark. Specifically, compared to the baseline Drive- **_π_ 0** , our method improves the driving score by 22.8% and the success rate by 62.1%. On the open-loop metric, our method achieves the lowest L2 error. We observe that diffusion policy-based trajectory prediction significantly reduces L2 errors compared to traditional methods. However, as highlighted in prior studies such as AD-MLP [55], TransFuser++ [20], and Bench2Drive [23], open-loop metrics mainly serve as indicators of model convergence, whereas closed-loop metrics provide a more reliable assessment of true driving performance. Moreover, in the multi- 

dimensional capability evaluation, as shown in Table 1, our method obtains state-of-the-art results across five key capabilities and their overall average. 

We use the official 220 routes and official metrics of Bench2Drive for evaluation. The **Driving Score (DS)** is defined as the product of Route Completion and Infraction Score, capturing both task completion and rule adherence. The **Success Rate (SR)** measures the percentage of routes completed successfully within the allocated time and without committing any traffic violations. **Efficiency** quantifies the vehicle’s velocity relative to surrounding traffic, encouraging progressiveness without aggression. **Comfort** reflects the smoothness of the driving trajectory. Meanwhile, Bench2Drive evaluates driving capabilities across multiple critical dimensions, including tasks such as **Merging** , 

10684 

**Overtaking** , **Emergency Braking** , **Yielding** , and **Traffic Signs** . All results are averaged over three runs. 

### **3.3. Ablation Study** 

**Vision MoE.** As shown in Table 3, we investigate the contribution of camera view selection and supervision signals within our Vision MoE module. The baseline (Exp 1, Drive- **_π_ 0** ) utilizes two consecutive front-view images primarily to estimate velocities of surrounding agents. Adding a third fixed view such as the back view (Exp 4), front-left view (Exp 2), or front-right view (Exp 3) provides additional spatial context, yielding moderate improvements. According to Exp 2-4, adding individual additional views provides more complementary perceptual information, leading to improved performance. However, when multiple views are added simultaneously (as in Exp 5-7), the number of visual tokens increases significantly, which introduces greater training complexity and convergence difficulty. As a result, model performance degrades, and the latency increases. 

By introducing dynamically selected views without supervision (Exp 8), the driving score and success rate significantly improve. Ultimately, incorporating explicit supervision signals (Exp 9, DriveMoE) for the dynamic view selection further enhances both driving score and success rate, demonstrating the effectiveness of our Vision MoE module in leveraging dynamic and supervised multi-view perception. Table 4 shows the accuracy of the vision and action routers on the test set under open-loop evaluation. 

**Token vs Trajectory Level Action MoE.** As shown in Table 5, we compare the token-level and trajectory-level routers, and observe that the trajectory-level router consistently outperforms the token-level counterpart. So We use **_Trajectory Level Action MoE as our default Action MoE._ Action MoE.** For clarity, the term Action MoE in the following sections specifically refers to the Trajectory-Level Action MoE. We investigate the impact of the number of non-shared experts within our Action MoE, as shown in Table 6. Specifically, Exp 1 corresponds to the original five skills defined by Bench2Drive [23], while Exp 2 introduces an additional expert for the classic _ParkingExits_ scenario, resulting in improved performance. To further analyze the effect of expert specialization, we conducted additional experiments: Exp 2–3 compare action supervision strategies, where the action supervision yields noticeable improvement; Exp 4-5 introduces additional shared experts, whose performance remains comparable to the Exp 2; Moreover, Exp 6 adds experts targeting several challenging scenarios identified from Exp 2, and Exp 7 assigns a distinct expert to each of the 44 scenarios in Bench2Drive. We observe that excessively increasing the number of experts (Exp 5-6) negatively affects performance due to the induced load imbalance among experts. Thus, an appropriate balance in the number of specialized experts is crucial 

#### for optimal driving performance. 

Table 4. **Router Accuracy** . The vision router and action router accuracy in Bench2Drive-Base validation set. 

|**Router**|**Accuracy**(%) _↑_|
|---|---|
|Vision Router|88.85|
|Action Router|65.40|


Table 5. **Token vs Trajectory Level Action MoE.** 

|**Style**|**Share**|**Non-Share**|**DS**_↑_|**SR**(%) _↑_|
|---|---|---|---|---|
|Token-Level|3|6|65.62|32.27|
|Traj-Level|3|6|73.88|48.64|


Table 6. **Ablation Study in Action MoE** . Compare various configurations of non-share expert numbers within Action MoE. 

|**Exp**|**Share**|**Non-share**|**Supervision**|**DS**_↑_|**SR**(%) _↑_|
|---|---|---|---|---|---|
|1|1|5|✓|73.81|47.73|
|2|1|6|✓|74.22|48.64|
|3|1|6|_×_|70.38|45.00|
|4|3|6|✓|73.88|48.64|
|5|5|6|✓|73.46|47.73|
|6|1|13|✓|70.88|44.50|
|7|1|44|✓|68.22|43.18|


**Drive-** **_π_ 0 vs DriveMoE.** We conduct ablation studies to evaluate the individual contributions of the Vision MoE and Action MoE within our DriveMoE framework. As shown in Table 7, removing either the Vision MoE or the Action MoE leads to a noticeable decline in both driving score and success rate. Compared to the Drive- **_π_ 0** , DriveMoE substantially improves driving performance, highlighting the complementary effectiveness of both MoE modules. 

Table 7. **Drive-** **_π_ 0 vs DriveMoE** . Evaluate the Vision MoE and Action MoE. ”w/o” denotes removing the respective modules. 

|**Method**|**DS**_↑_|**SR**(%) _↑_|
|---|---|---|
|Drive-**_π_0**|55.85|30.00|
|w/o Vision MoE|68.68|42.45|
|w/o Action MoE|67.31|40.56|
|DriveMoE|74.22|48.64|


## **4. Conclusion** 

We propose DriveMoE, a novel end-to-end autonomous driving framework built upon Drive- **_π_ 0** , which integrates Mixture-of-Experts(MoE) into both vision and action components. DriveMoE effectively addresses challenges inherent in existing VLA models by dynamically selecting relevant camera views through a Scene-Specialized Vision MoE, and by employing a Skill-Specialized Action MoE that activates expert modules tailored to specific driving behaviors. Extensive evaluations on the Bench2Drive benchmark show that DriveMoE achieves state-of-the-art performance, significantly enhancing computational efficiency and robustness to rare, safety-critical driving scenarios. 

10685 

## **References** 

- [1] Jinze Bai, Shuai Bai, Yunfei Chu, Zeyu Cui, Kai Dang, Xiaodong Deng, Yang Fan, Wenbin Ge, Yu Han, Fei Huang, et al. Qwen technical report. _arXiv preprint arXiv:2309.16609_ , 2023. 2 

- [2] Lucas Beyer, Andreas Steiner, Andr´e Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, et al. Paligemma: A versatile 3b vlm for transfer. _arXiv preprint arXiv:2407.07726_ , 2024. 3, 6, 2 

- [3] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _pi_ ~~0~~ : A vision-languageaction flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 1, 3, 5 

- [4] Weilin Cai, Juyong Jiang, Fan Wang, Jing Tang, Sunghun Kim, and Jiayi Huang. A survey on mixture of experts in large language models. _IEEE Transactions on Knowledge and Data Engineering_ , 2025. 2 

- [5] Yuan Chen, Zi han Ding, Ziqin Wang, Yan Wang, Lijun Zhang, and Si Liu. Asynchronous large language model enhanced planner for autonomous driving, 2024. 1, 2 

- [6] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , page 02783649241273668, 2023. 1 

- [7] Kashyap Chitta, Aditya Prakash, Bernhard Jaeger, Zehao Yu, Katrin Renz, and Andreas Geiger. Transfuser: Imitation with transformer-based sensor fusion for autonomous driving. _TPAMI_ , 2023. 1 

- [8] Damai Dai, Chengqi Deng, Chenggang Zhao, RX Xu, Huazuo Gao, Deli Chen, Jiashi Li, Wangding Zeng, Xingkai Yu, Yu Wu, et al. Deepseekmoe: Towards ultimate expert specialization in mixture-of-experts language models. _arXiv preprint arXiv:2401.06066_ , 2024. 6, 1 

- [9] DeepSeek-AI. Deepseek-v3 technical report, 2024. 3 

- [10] Alexey Dosovitskiy, German Ros, Felipe Codevilla, Antonio Lopez, and Vladlen Koltun. Carla: An open urban driving simulator. In _Conference on robot learning_ , pages 1–16. PMLR, 2017. 6 

- [11] Danny Driess, Jost Tobias Springenberg, Brian Ichter, Lili Yu, Adrian Li-Bell, Karl Pertsch, Allen Z Ren, Homer Walke, Quan Vuong, Lucy Xiaoyang Shi, et al. Knowledge insulating vision-language-action models: Train fast, run fast, generalize better. _arXiv preprint arXiv:2505.23705_ , 2025. 1 

- [12] Haoyu Fu, Diankun Zhang, Zongchuang Zhao, Jianfeng Cui, Dingkang Liang, Chong Zhang, Dingyuan Zhang, Hongwei Xie, Bing Wang, and Xiang Bai. Orion: A holistic end-toend autonomous driving framework by vision-language instructed action generation. _arXiv preprint arXiv:2503.19755_ , 2025. 1, 3 

- [13] Shadi Hamdan, Chonghao Sima, Zetong Yang, Hongyang Li, and Fatma Guney. Eta: Efficiency through thinking ahead, a dual approach to self-driving with large models. In 

_Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 26529–26538, 2025. 1 

- [14] Deepti Hegde, Rajeev Yasarla, Hong Cai, Shizhong Han, Apratim Bhattacharyya, Shweta Mahajan, Litian Liu, Risheek Garrepalli, Vishal M Patel, and Fatih Porikli. Distilling multi-modal large language models for autonomous driving. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 27575–27585, 2025. 2 

- [15] Yihan Hu, Jiazhi Yang, Li Chen, Keyu Li, Chonghao Sima, Xizhou Zhu, Siqi Chai, Senyao Du, Tianwei Lin, Wenhai Wang, et al. Planning-oriented autonomous driving. In _CVPR_ , pages 17853–17862, 2023. 1, 6, 7, 3 

- [16] Suning Huang, Zheyu Zhang, Tianhai Liang, Yihan Xu, Zhehao Kou, Chenhao Lu, Guowei Xu, Zhengrong Xue, and Huazhe Xu. Mentor: Mixture-of-experts network with task-oriented perturbation for visual reinforcement learning. _arXiv preprint arXiv:2410.14972_ , 2024. 1 

- [17] Xianliang Huang, Jiajie Gou, Shuhang Chen, Zhizhou Zhong, Jihong Guan, and Shuigeng Zhou. Iddr-ngp: Incorporating detectors for distractors removal with instant neural radiance field. In _Proceedings of the 31st ACM International Conference on Multimedia_ , pages 1343–1351, 2023. 2 

- [18] Xianliang Huang, Zhizhou Zhong, Shuhang Chen, Yi Xu, Jihong Guan, and Shuigeng Zhou. Nerf-mir: Toward highquality restoration of masked images with neural radiance fields. _IEEE Transactions on Neural Networks and Learning Systems_ , 2026. 2 

- [19] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. _pi_ ~~0~~ _._ 5: a vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 1, 3 

- [20] Bernhard Jaeger, Kashyap Chitta, and Andreas Geiger. Hidden biases of end-to-end driving models. In _Proc. of the IEEE International Conf. on Computer Vision (ICCV)_ , 2023. 1, 7 

- [21] Xiaosong Jia, Yulu Gao, Li Chen, Junchi Yan, Patrick Langechuan Liu, and Hongyang Li. Driveadapter: Breaking the coupling barrier of perception and planning in end-to-end autonomous driving. In _ICCV_ , 2023. 6, 7 

- [22] Xiaosong Jia, Penghao Wu, Li Chen, Jiangwei Xie, Conghui He, Junchi Yan, and Hongyang Li. Think twice before driving: Towards scalable decoders for end-to-end autonomous driving. In _CVPR_ , 2023. 6, 7 

- [23] Xiaosong Jia, Zhenjie Yang, Qifeng Li, Zhiyuan Zhang, and Junchi Yan. Bench2drive: Towards multi-ability benchmarking of closed-loop end-to-end autonomous driving. In _NeurIPS 2024 Datasets and Benchmarks Track_ , 2024. 6, 7, 8, 1, 2, 3 

- [24] Xiaosong Jia, Junqi You, Zhiyuan Zhang, and Junchi Yan. Drivetransformer: Unified transformer for scalable end-toend autonomous driving. In _The Thirteenth International Conference on Learning Representations_ , 2025. 2, 6, 7 

- [25] Albert Q Jiang, Alexandre Sablayrolles, Antoine Roux, Arthur Mensch, Blanche Savary, Chris Bamford, Devendra Singh Chaplot, Diego de las Casas, Emma Bou Hanna, Florian Bressand, et al. Mixtral of experts. _arXiv preprint arXiv:2401.04088_ , 2024. 3, 5 

10686 

- [26] Bo Jiang, Shaoyu Chen, Qing Xu, Bencheng Liao, Jiajie Chen, Helong Zhou, Qian Zhang, Wenyu Liu, Chang Huang, and Xinggang Wang. Vad: Vectorized scene representation for efficient autonomous driving. _ICCV_ , 2023. 1, 6, 7, 3 

- [27] Titong Jiang, Xuefeng Jiang, Yuan Ma, Xin Wen, Bailin Li, Kun Zhan, Peng Jia, Yahui Liu, Sheng Sun, and Xianpeng Lang. The better you learn, the smarter you prune: Towards efficient vision-language-action models via differentiable token pruning. _arXiv preprint arXiv:2509.12594_ , 2025. 2 

- [28] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 3, 1 

- [29] Boyi Li, Yifan Shen, Yuanzhe Liu, Yifan Xu, Jiateng Liu, Xinzhuo Li, Zhengyuan Li, Jingyuan Zhu, Yunhan Zhong, Fangzhou Lan, et al. Toward cognitive supersensing in multimodal large language model. _arXiv preprint arXiv:2602.01541_ , 2026. 1 

- [30] Junnan Li, Dongxu Li, Silvio Savarese, and Steven Hoi. Blip-2: Bootstrapping language-image pre-training with frozen image encoders and large language models. In _International conference on machine learning_ , pages 19730– 19742. PMLR, 2023. 2, 3 

- [31] Yingyan Li, Yuqi Wang, Yang Liu, Jiawei He, Lue Fan, and Zhaoxiang Zhang. End-to-end driving with online trajectory evaluation via bev world model. _arXiv preprint arXiv:2504.01941_ , 2025. 7 

- [32] Yaron Lipman, Ricky TQ Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le. Flow matching for generative modeling. _arXiv preprint arXiv:2210.02747_ , 2022. 3, 1 

- [33] Qiang Liu. Rectified flow: A marginal preserving approach to optimal transport. _arXiv preprint arXiv:2209.14577_ , 2022. 1 

- [34] Yuanzhe Liu, Jingyuan Zhu, Yuchen Mo, Gen Li, Xu Cao, Jin Jin, Yifan Shen, Zhengyuan Li, Tianjiao Yu, Wenzhen Yuan, et al. Palm: Progress-aware policy learning via affordance reasoning for long-horizon robotic manipulation. _arXiv preprint arXiv:2601.07060_ , 2026. 1 

- [35] Jianbiao Mei, Yukai Ma, Xuemeng Yang, Licheng Wen, Xinyu Cai, Xin Li, Daocheng Fu, Bo Zhang, Pinlong Cai, Min Dou, et al. Continuously learning, adapting, and improving: A dual-process approach to autonomous driving. _arXiv preprint arXiv:2405.15324_ , 2024. 1 

- [36] OpenAI, Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, Red Avila, Igor Babuschkin, Suchir Balaji, Valerie Balcom, Paul Baltescu, Haiming Bao, Mohammad Bavarian, Jeff Belgum, Irwan Bello, Jake Berdine, Gabriel BernadettShapiro, Christopher Berner, Lenny Bogdonoff, Oleg Boiko, Madelaine Boyd, Anna-Luisa Brakman, Greg Brockman, Tim Brooks, Miles Brundage, Kevin Button, Trevor Cai, Rosie Campbell, Andrew Cann, Brittany Carey, Chelsea Carlson, Rory Carmichael, Brooke Chan, Che Chang, Fotis Chantzis, Derek Chen, Sully Chen, Ruby Chen, Jason Chen, Mark Chen, Ben Chess, Chester Cho, Casey 

Chu, Hyung Won Chung, Dave Cummings, Jeremiah Currier, Yunxing Dai, Cory Decareaux, Thomas Degry, Noah Deutsch, Damien Deville, Arka Dhar, David Dohan, Steve Dowling, Sheila Dunning, Adrien Ecoffet, Atty Eleti, Tyna Eloundou, David Farhi, Liam Fedus, Niko Felix, Sim´on Posada Fishman, Juston Forte, Isabella Fulford, Leo Gao, Elie Georges, Christian Gibson, Vik Goel, Tarun Gogineni, Gabriel Goh, Rapha Gontijo-Lopes, Jonathan Gordon, Morgan Grafstein, Scott Gray, Ryan Greene, Joshua Gross, Shixiang Shane Gu, Yufei Guo, Chris Hallacy, Jesse Han, Jeff Harris, Yuchen He, Mike Heaton, Johannes Heidecke, Chris Hesse, Alan Hickey, Wade Hickey, Peter Hoeschele, Brandon Houghton, Kenny Hsu, Shengli Hu, Xin Hu, Joost Huizinga, Shantanu Jain, Shawn Jain, Joanne Jang, Angela Jiang, Roger Jiang, Haozhun Jin, Denny Jin, Shino Jomoto, Billie Jonn, Heewoo Jun, Tomer Kaftan, Łukasz Kaiser, Ali Kamali, Ingmar Kanitscheider, Nitish Shirish Keskar, Tabarak Khan, Logan Kilpatrick, Jong Wook Kim, Christina Kim, Yongjik Kim, Jan Hendrik Kirchner, Jamie Kiros, Matt Knight, Daniel Kokotajlo, Łukasz Kondraciuk, Andrew Kondrich, Aris Konstantinidis, Kyle Kosic, Gretchen Krueger, Vishal Kuo, Michael Lampe, Ikai Lan, Teddy Lee, Jan Leike, Jade Leung, Daniel Levy, Chak Ming Li, Rachel Lim, Molly Lin, Stephanie Lin, Mateusz Litwin, Theresa Lopez, Ryan Lowe, Patricia Lue, Anna Makanju, Kim Malfacini, Sam Manning, Todor Markov, Yaniv Markovski, Bianca Martin, Katie Mayer, Andrew Mayne, Bob McGrew, Scott Mayer McKinney, Christine McLeavey, Paul McMillan, Jake McNeil, David Medina, Aalok Mehta, Jacob Menick, Luke Metz, Andrey Mishchenko, Pamela Mishkin, Vinnie Monaco, Evan Morikawa, Daniel Mossing, Tong Mu, Mira Murati, Oleg Murk, David M´ely, Ashvin Nair, Reiichiro Nakano, Rajeev Nayak, Arvind Neelakantan, Richard Ngo, Hyeonwoo Noh, Long Ouyang, Cullen O’Keefe, Jakub Pachocki, Alex Paino, Joe Palermo, Ashley Pantuliano, Giambattista Parascandolo, Joel Parish, Emy Parparita, Alex Passos, Mikhail Pavlov, Andrew Peng, Adam Perelman, Filipe de Avila Belbute Peres, Michael Petrov, Henrique Ponde de Oliveira Pinto, Michael, Pokorny, Michelle Pokrass, Vitchyr H. Pong, Tolly Powell, Alethea Power, Boris Power, Elizabeth Proehl, Raul Puri, Alec Radford, Jack Rae, Aditya Ramesh, Cameron Raymond, Francis Real, Kendra Rimbach, Carl Ross, Bob Rotsted, Henri Roussez, Nick Ryder, Mario Saltarelli, Ted Sanders, Shibani Santurkar, Girish Sastry, Heather Schmidt, David Schnurr, John Schulman, Daniel Selsam, Kyla Sheppard, Toki Sherbakov, Jessica Shieh, Sarah Shoker, Pranav Shyam, Szymon Sidor, Eric Sigler, Maddie Simens, Jordan Sitkin, Katarina Slama, Ian Sohl, Benjamin Sokolowsky, Yang Song, Natalie Staudacher, Felipe Petroski Such, Natalie Summers, Ilya Sutskever, Jie Tang, Nikolas Tezak, Madeleine B. Thompson, Phil Tillet, Amin Tootoonchian, Elizabeth Tseng, Preston Tuggle, Nick Turley, Jerry Tworek, Juan Felipe Cer´on Uribe, Andrea Vallone, Arun Vijayvergiya, Chelsea Voss, Carroll Wainwright, Justin Jay Wang, Alvin Wang, Ben Wang, Jonathan Ward, Jason Wei, CJ Weinmann, Akila Welihinda, Peter Welinder, Jiayi Weng, Lilian Weng, Matt Wiethoff, Dave Willner, Clemens Winter, Samuel Wolrich, Hannah Wong, Lauren 

10687 

Workman, Sherwin Wu, Jeff Wu, Michael Wu, Kai Xiao, Tao Xu, Sarah Yoo, Kevin Yu, Qiming Yuan, Wojciech Zaremba, Rowan Zellers, Chong Zhang, Marvin Zhang, Shengjia Zhao, Tianhao Zheng, Juntang Zhuang, William Zhuk, and Barret Zoph. Gpt-4 technical report, 2024. 2 

- [37] Zhangyang Qi, Ye Fang, Zeyi Sun, Xiaoyang Wu, Tong Wu, Jiaqi Wang, Dahua Lin, and Hengshuang Zhao. Gpt4point: A unified framework for point-language understanding and generation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 26417– 26427, 2024. 2, 3 

- [38] Katrin Renz, Long Chen, Ana-Maria Marcu, Jan H¨unermann, Benoit Hanotte, Alice Karnsund, Jamie Shotton, Elahe Arani, and Oleg Sinavski. Carllava: Vision language models for camera-only closed-loop driving, 2024. 1, 2 

- [39] Katrin Renz, Long Chen, Elahe Arani, and Oleg Sinavski. Simlingo: Vision-only closed-loop autonomous driving with language-action alignment. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 11993– 12003, 2025. 2, 1 

- [40] Hao Shao, Yuxuan Hu, Letian Wang, Steven L. Waslander, Yu Liu, and Hongsheng Li. Lmdrive: Closed-loop end-toend driving with large language models, 2023. 1, 2, 3 

- [41] Yifan Shen, Yuanzhe Liu, Jingyuan Zhu, Xu Cao, Xiaofeng Zhang, Yixiao He, Wenming Ye, James Matthew Rehg, and Ismini Lourentzou. Fine-grained preference optimization improves spatial reasoning in vlms. _arXiv preprint arXiv:2506.21656_ , 2025. 1 

- [42] Chonghao Sima, Katrin Renz, Kashyap Chitta, Li Chen, Hanxue Zhang, Chengen Xie, Ping Luo, Andreas Geiger, and Hongyang Li. Drivelm: Driving with graph visual question answering. _arXiv preprint arXiv:2312.14150_ , 2023. 1, 2, 3 

- [43] Ziying Song, Caiyan Jia, Lin Liu, Hongyu Pan, Yongchang Zhang, Junming Wang, Xingyu Zhang, Shaoqing Xu, Lei Yang, and Yadan Luo. Don’t shake the wheel: Momentumaware planning in end-to-end autonomous driving. _arXiv preprint arXiv:2503.03125_ , 2025. 1, 7 

- [44] Haisheng Su, Wei Wu, Feixiang Song, Junjie Zhang, Zhenjie Yang, and Junchi Yan. Drivemamba: Task-centric scalable state space model for efficient end-to-end autonomous driving. _arXiv preprint arXiv:2602.13301_ , 2026. 1, 7 

- [45] Haisheng Su, Wei Wu, Zhenjie Yang, and Isabel Guan. Egofsd: Ego-centric fully sparse paradigm with uncertainty denoising and iterative refinement for efficient end-to-end self-driving, 2026. 1 

- [46] Zhongwei Wan, Xin Wang, Che Liu, Samiul Alam, Yu Zheng, et al. Efficient large language models: A survey. _arXiv preprint arXiv:2312.03863_ , 1, 2023. 2 

language models with behavioral planning states for autonomous driving. _arXiv preprint arXiv:2312.09245_ , 2023. 2 

   - [49] Penghao Wu, Xiaosong Jia, Li Chen, Junchi Yan, Hongyang Li, and Yu Qiao. Trajectory-guided control prediction for end-to-end autonomous driving: A simple yet strong baseline. In _NeurIPS_ , 2022. 1, 6, 7 

   - [50] Feng Xu, Guangyao Zhai, Xin Kong, Tingzhong Fu, Daniel FN Gordon, Xueli An, and Benjamin Busam. Stare-vla: Progressive stage-aware reinforcement for finetuning vision-language-action models. _arXiv preprint arXiv:2512.05107_ , 2025. 1 

   - [51] Zhenhua Xu, Yujia Zhang, Enze Xie, Zhen Zhao, Yong Guo, Kwan-Yee K Wong, Zhenguo Li, and Hengshuang Zhao. Drivegpt4: Interpretable end-to-end autonomous driving via large language model. _IEEE Robotics and Automation Letters_ , 2024. 1 

   - [52] Zhenjie Yang, Xiaosong Jia, Hongyang Li, and Junchi Yan. Llm4drive: A survey of large language models for autonomous driving. _ArXiv_ , abs/2311.01043, 2023. 1 

   - [53] Zhenjie Yang, Xiaosong Jia, Qifeng Li, Xue Yang, Maoqing Yao, and Junchi Yan. Raw2drive: Reinforcement learning with aligned world models for end-to-end autonomous driving (in carla v2). _arXiv preprint arXiv:2505.16394_ , 2025. 7 

   - [54] Rajeev Yasarla, Shizhong Han, Hong Cai, and Fatih Porikli. Dyss: Dynamic queries and state-space learning for efficient 3d object detection from multi-camera videos. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 2510–2519, 2025. 2 

   - [55] Jiang-Tian Zhai, Ze Feng, Jihao Du, Yongqiang Mao, JiangJiang Liu, Zichang Tan, Yifu Zhang, Xiaoqing Ye, and Jingdong Wang. Rethinking the open-loop evaluation of endto-end autonomous driving in nuscenes. _arXiv preprint arXiv:2305.10430_ , 2023. 1, 7 

   - [56] Jiang-Tian Zhai, Ze Feng, Jinhao Du, Yongqiang Mao, Jiang-Jiang Liu, Zichang Tan, Yifu Zhang, Xiaoqing Ye, and Jingdong Wang. Rethinking the open-loop evaluation of end-to-end autonomous driving in nuscenes. _arXiv preprint arXiv:2305.10430_ , 2023. 6, 7 

   - [57] Wenzhao Zheng, Ruiqi Song, Xianda Guo, Chenming Zhang, and Long Chen. Genad: Generative end-to-end autonomous driving. _arXiv preprint arXiv: 2402.11502_ , 2024. 1, 7 

   - [58] Tong Zhu, Xiaoye Qu, Daize Dong, Jiacheng Ruan, Jingqi Tong, Conghui He, and Yu Cheng. Llama-moe: Building mixture-of-experts from llama with continual pre-training. In _Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing_ , pages 15913–15923, 2024. 2 

- [47] Tao Wang, Cong Zhang, Xingguang Qu, Kun Li, Weiwei Liu, and Chang Huang. Diffad: A unified diffusion modeling approach for autonomous driving. _arXiv preprint arXiv:2503.12170_ , 2025. 1, 6, 7 

- [48] Wenhai Wang, Jiangwei Xie, ChuanYang Hu, Haoming Zou, Jianan Fan, Wenwen Tong, Yang Wen, Silei Wu, Hanming Deng, Zhiqi Li, et al. Drivemlm: Aligning multi-modal large 

10688 

