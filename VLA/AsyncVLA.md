---
title: "AsyncVLA: An Asynchronous VLA for Fast and Robust Navigation on the Edge"
date: "2026-02-13"
authors: "Noriaki Hirose; Catherine Glossop; Dhruv Shah; Sergey Levine"
venue: "CoRL 2026"
url: https://arxiv.org/abs/2602.13476
pdf: https://arxiv.org/pdf/2602.13476
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.13476)** / [論文ページ](https://arxiv.org/abs/2602.13476)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# AsyncVLA: An Asynchronous VLA for Fast and Robust Navigation on the Edge 

Noriaki Hirose<sup>1</sup><sup>_,_2</sup> , Catherine Glossop<sup>1</sup> , Dhruv Shah<sup>3</sup> , Sergey Levine<sup>1</sup> 1University of California, Berkeley 2Toyota Motor North America 3Princeton University 


**Fig. 1:** We train a fast and robust vision-based navigation policy by jointly optimizing a large robotic foundation model and a compact ViT in an end-to-end manner. During inference, we decouple the large base VLA and the Edge Adapter to form a nested control system: the base VLA runs on a workstation to provide rich visual and language understanding, while the Edge Adapter is deployed on the robot’s edge controller to rapidly adapt to the current environment and enable robust navigation. 

**_Abstract_ —Robotic foundation models achieve strong generalization by leveraging internet-scale vision-language representations, but their massive computational cost creates a fundamental bottleneck: high inference latency. In dynamic environments, this latency breaks the control loop, rendering powerful models unsafe for real-time deployment. We propose AsyncVLA, an asynchronous control framework that decouples semantic reasoning from reactive execution. Inspired by hierarchical control, AsyncVLA runs a large foundation model on a remote workstation to provide high-level guidance, while a lightweight, onboard Edge Adapter continuously refines actions at high frequency. To bridge the domain gap between these asynchronous streams, we introduce an end-to-end finetuning protocol and a trajectory re-weighting strategy that prioritizes dynamic interactions. We evaluate our approach on real-world vision-based navigation tasks with communication delays up to 6 seconds. AsyncVLA achieves a 40% higher success rate than state-of-the-art baselines, effectively bridging the gap between the semantic intelligence of large models and the reactivity required for edge robotics. We present videos showcasing the performance and release our checkpoints and training code on our project page**<sup>1</sup> **.** 

## I. INTRODUCTION 

Recent progress in robot learning has been marked by the introduction of vision-language-action models (VLAs) [4, 7, 20, 26, 28, 40, 52], models finetuned from large vision-language models (VLMs) on robot data. VLAs can inherit internet-scale knowledge from VLMs, resulting in vastly superior vision and language understanding compared to those trained from scratch. However, as we massively scale up the size of our robot policies, we sacrifice inference speed, which can impact performance [11, 34, 40]. In particular, increased inference latency results in longer control cycles, which manifest as time delays in the control loop that can degrade overall system 

performance. This paper tackles the research question: _how can large robotic foundation models be deployed on the edge without being constrained by their computational cost?_ 

The challenges associated with large-scale foundation models are especially pronounced in mobile robots. Due to the limited field of view with ego-centric camera views, mobile robots cannot fully perceive their surroundings from a given observation [17, 37, 38]. With the presence of dynamic obstacles, such as pedestrians, this problem is further exacerbated [18]. Consequently, mobile robots must continuously update their observations while navigating and rapidly generate actions based on the most recent sensory inputs. As a result, the increasing computational burden associated with scaling robotic foundation models directly leads to performance degradation in real-world navigation tasks. In addition, mobile robots often cannot be equipped with highperformance GPUs, making it necessary to execute foundation models on cloud-based or remote workstations [1, 21, 31]. In such settings, communication latency between the robot and the workstation introduces additional delays into the control loop, further degrading performance. Even when inference can be performed on board, the high power consumption of large foundation models significantly reduces battery life and severely limits operational duration. 

Traditional control systems often use a hierarchical or cascaded architecture [27, 48, 49]. In navigation, for example, a global planner might serve as an outer loop providing highlevel guidance, while a local planner functions as an inner loop, with the inner loop operating at a higher frequency to compensate for delays in the slower outer loop and incorporate local information. Similarly, in servo control for robotic joints or machine tools, multiple control loops, such as position, 

> 1 **asyncvla.github.io** 

velocity, and force control, are organized hierarchically from outer to inner loops, with higher update rates in inner loops to suppress disturbances such as perturbations and friction [3]. 

Analogously, we construct a control system for VLAs that consists of an outer loop driven by a large-scale robotic foundation model and an inner loop governed by a lightweight model, both trained for end-to-end control. We make several key design decisions to allow our framework to be robust to large delays while maintaining the expressivity of the outerloop VLA. We adapt a Edge Adapter inner-loop policy, 100x smaller than the VLA, that maintains high reactivity while effectively incorporating high-level visual and language understanding guidance from the outer-loop policy. The lightweight inner-loop policy can incorporate the most recent observation information, enabling rapid correction when obstacles are encountered. We train our method by up-weighting a dynamic subset of our training data and use a two-staged training process: we first train the Edge Adapter and then train the outer- and inner-loop framework end-to-end, better aligning the two policies. 

Our primary contribution is AsyncVLA, a framework that enables the deployment of large foundation models on edge robots by structurally decoupling reasoning from actuation. To this end, we developed an Edge Adapter, a lightweight (76M parameter) policy that runs _on board_ the robot, fusing realtime sensors with delayed, high-level guidance from a remote VLA (over 8B parameters). Crucially, we propose a training strategy that up-weights reactive trajectories—moments where the robot must deviate from the base policy to avoid dynamic obstacles—and an end-to-end finetuning protocol to align the asynchronous streams. Our real-world experiments demonstrate that AsyncVLA maintains robust performance even under control delays that fluctuate up to 6 seconds, outperforming synchronous baselines by over 40% in dynamic navigation scenarios. 

## II. RELATED WORK 

Our work builds on recently developed large robotic foundation models, specifically vision-language-action models (VLAs). We will first introduce recent work on VLAs, then prior efforts to improve inference speed and efficiently deploy these models, and finally explore recent work on dual or fastslow architectures for VLA deployment. 

**Vision-language-action models.** With the advent of large and powerful vision-language models, vision-language-action models (VLAs), which finetune VLMs for robot control [4, 7, 20, 26, 28, 40, 52], have become a widely studied approach for instilling robot policies with generalist knowledge and reasoning capabilities. Although these models range in size, with some under 1 billion parameters [4, 30, 40, 58], large models, in the range of 4 to 100s of billions of parameters [7, 20, 26, 44], tend to be more performant [8, 45], just as their VLM base models tend to be more performant [24]. These larger models can have long inference times, impeding reactive real-time control. AsyncVLA decouples inference 

into the large, powerful VLA, run on a remote workstation, and an Edge Adapter action head, which can run directly on the robot’s onboard compute. The Edge Adapter action head can leverage the local information from the most up-todate observations of the environment and rapidly refine the semantically informed actions from the VLA. Not only does make the inference speed of the VLA effectively the inference speed of the Edge Adapter, we can also compensate for large fluctuations in network latency, which a VLA run off-board would always have to contend with, and respond to dynamic changes in the environment. 

**Efficient inference for VLAs.** Previous work has aimed to improve the efficiency of VLAs using several methods. Reducing model size has been a key method as it directly addresses the cause of slow inference, whether that be through training smaller models [4, 10, 40, 54], or quantizing parameters to use fewer bits [4, 50, 54]. However, reducing model size entails that we have a limited set of VLAs that may be practical for edge deployment, while quantization may have a limited impact on model size before performance starts to degrade. Alternatively, other approaches improve inference speed through fast action decoding [13, 33], or compensate for inference delays with asynchronous inference methods [6, 43, 57]. Along this same line, many methods append a fast “action expert” or action head [7, 51–53] onto the model, and others additionally use pipelines to decide when it is necessary to run inference over the full backbone [5, 29]. While these approaches allow for efficient inference, in that the entire backbone does not need to be used each time inference is performed, allowing for fast inference loops with just the action expert, these methods do not decouple the architecture, allowing the on-board inference on the action head alone. AsyncVLA explicitly separates inference into a small on-board policy, which gets the most recent observation information and can be rapidly inferred, and an off-board VLA, which provides high-level visual and semantic guidance. Additionally, while these methods only consider their own inference delay, on the order of 100s of milliseconds, AsyncVLA is explicitly trained to compensate for networking delays, even up to several seconds, and preserves the performance of the base VLA policy. 

**Hierarchical VLAs.** A recent class of approaches that enables faster inference of large VLAs by using dual or “fast-slow” architectures, inspired by the dual system theory [23]. These architectures separate the VLA into a large backbone that runs at a low frequency, and a small, reactive model that runs at a higher frequency. These methods often use a latent from the large VLA to bridge the representations learned by the large model to the small one [9, 11, 12, 15, 39, 56], while others formulate the small model as a correction head and instead modify the actions coming from the base VLA [34]. AsyncVLA also employs a dual architecture, but instead projects the token space of the base VLA policy into a smaller token space for the Edge Adapter. More critically, these works focus on manipulation with a static workstation, and none need 

to consider the added delay of network latency that comes from deploying their system over a WiFi network. As a result, these works aim to compensate for small inference delays, up to about 300 ms. Few works include dynamic tasks in their evaluation and, when they are included, they consider very slow motion (objects moving at 1 cm/s) [56] and predictable patterns such as straight lines or circles [12]. Therefore, the small “fast” models in these systems are mostly tasked with interpolating the actions from the “slow” model based on recent sensor information. AsyncVLA is designed to handle unpredictable, dynamic situations, such as people walking in front of a moving robot, while handling variable network latencies of around 5 seconds, in addition to inference delays. As a result, the Edge Adapter must be able to effectively learn skills like dynamic obstacle avoidance while using the high-level guidance provided by the base VLA. To this end, we expose the Edge Adapter to large variations between the most recent observation and the observation processed by the VLA. First, we randomly select the VLA’s observation from a long context while the Edge Adapter always processes the most up-to-date observation, forcing the Edge Adapter to learn to predict actions that correspond to the current state of the environment, rather than the stale information processed in the last VLA inference pass. Second, we up-weight the segments of our dataset where the robot interacts with dynamic obstacles, such as encountering pedestrians, so that it must learn to predict their behavior and respond accordingly. 

To our knowledge, AsyncVLAis the first method to deploy a dual architecture with a large VLA and a small _edge_ model for navigation while explicitly accounting for both inference and network delays. We evaluate our method in both static and dynamic environments on pose- and language-conditioned navigation tasks and specifically demonstrate the robustness of AsyncVLA to enforced latencies of up to 6 seconds. 

## III. AN ASYNCHRONOUS VLA FOR NAVIGATION 

We propose an asynchronous navigation system, AsyncVLA, that leverages the rich language and visual understanding of existing robotic foundation models, while providing for quick reactive control based on the most recent observations. To achieve such a reactive policy without sacrificing rich semantic understanding, AsyncVLA integrates three key design choices into a single system: (1) a lightweight action head, Edge Adapter, (2) automatic data re-balancing to encourage reactive behavior, and (3) end-to-end training for better aligning the base VLA and the Edge Adapter. 

## _A. Edge Adapter Architecture_ 

Robotic foundation models generate actions using rich language and visual understanding, but their large model size incurs substantial computational overhead, often requiring deployment on a remote workstation. This setup introduces significant communication latency, reduces the achievable control frequency, and ultimately degrades task performance. With a latency of _k_ steps, by the time an action is executed by the robot, _k_ steps will have passed, so naively using a 


**Fig. 2: Network architecture.** We train a Edge Adapter on top of the large robotic foundation model, OmniVLA, for vision-based navigation. During inference, the Edge Adapter runs on the robot’s onboard controller at maximum speed to adjust the robot’s behavior to the current environment, and the base VLA runs on the workstation to provide rich visual and language understanding. 

slow VLA will result in the action _at_ corresponding to the observation at time _t − k_ , _It−k_ , instead of the observation at time _t_ , _It_ . To address this issue, we propose AsyncVLA, a policy architecture in Fig. 2 that builds upon an existing robotic foundation model, the base VLA, by augmenting it with a lightweight onboard policy(Edge Adapter). In our implementation, we use OmniVLA [20] as the base VLA, which is further described in section IV. 

Our Edge Adapter adapts the actions of the base VLA to the information in the current observation, leveraging the semantic and visual information encoded in the base VLA’s action token embeddings. To enable fast inference while leveraging the large model’s understanding as much as possible, we provide action token embeddings derived from the final-layer action features of the base VLA, keeping Edge Adapter lightweight with only 76M parameters. This allows Edge Adapter to operate at a high frequency. However, the action token embeddings from the base VLA are temporally delayed, since the base model processes observations from _It−k_ . Note that the delay _k_ can fluctuate depending on network latency and workstation performance. 

We address the challenge of preserving the semantic and visual information provided by the base VLA through its action token embeddings while accounting for the latency _k_ within the Edge Adapter. This includes responding to dynamic changes in the environment that are not perceived at time _t−k_ and therefore are not included in the information provided in the action token embeddings. We design Edge Adapter as a small ViT network (shown in the light blue area of Fig. 2. In addition to the 8 _×_ 1024 action token embeddings, which 

are projected from the base VLA’s token space, we introduce two additional token embeddings of dimension 1024. The first additional token embedding encodes the feature representation of the current image _It_<sup>_s_,enablingthemodeltocapturethe</sup> robot’s immediate surroundings (see the leftmost input to the “Transformer” in Fig. 2). The second token embedding is extracted from a concatenated six-channel image composed of _It_<sup>_s_and</sup><sup>_I_</sup> _t_<sup>_s_</sup> _−k_<sup>,enablingthemodeltoaccountforchanges</sup> in robot pose and environmental dynamics occurring between _t − k_ and _t_ (see the second input from the left to the “Transformer” in Fig. 2). In the Edge Adapter, we resize the images to 96 _×_ 96, denoted as _I_<sup>_s_</sup> , which is less than one quarter of the resolution used by the base VLA. As a result, we can train the Edge Adapter to be a fraction of the base VLA’s size while preserving the rich information from the base VLA. 

To generate an action chunk for _N_ steps, _{at_ + _i}i_ =0 _...N −_ 1, we attach a small action head on top of the transformer in Edge Adapter. Here, _at_ + _i_ represents the 2D pose at _t_ + _i_ in the robot’s coordinate frame at time _t_ , similar to OmniVLA [20], ViNT [38] and MBRA [21]. Importantly, only the output token corresponding to _It_ is fed into the action head. This design conditions action generation on the current observation and prevents the Edge Adapter from producing delayed actions influenced by the embeddings from the base VLA with _It−k_ . Further details are described in Section IV. 

## _B. Up-weighting Reactive Trajectories_ 

To make AsyncVLA a reactive policy, we require data sequences that capture reactive behaviors, such as collision avoidance or yielding to pedestrians. Such behaviors typically involve rapid changes in velocity or direction of the robot taking place within a single action chunk of the base VLA. However, such behaviors are relatively rare in the pre-training dataset, and training Edge Adapter na¨ıvely on this distribution is insufficient to learn the reactive behaviors we desire. To address this imbalance, we apply a data rebalancing approach that automatically identifies sequences containing sudden intra-chunk action changes and up-weights them during training. 

Concretely, we extract from the training data two action chunk references, _A_<sup>_t_</sup> = _{a_<sup>ref</sup> _t_ +<sup>_,t_</sup> _i_<sup>_}i_=0</sup><sup>_...N−_1expressed</sup> in the robot coordinate frame at time _t_ , and _A_<sup>_t−k_</sup> = _{a_<sup>ref</sup> _t−_<sup>_,t_</sup> _k_<sup>_−_</sup> +<sup>_k_</sup> _i_<sup>_}i_=0</sup><sup>_...N−_1expressedintherobotcoordinateframeat</sup> time _t − k_ . Here, _A_<sup>_t_</sup> serves as the action reference for training AsyncVLA, while _A_<sup>_t−k_</sup> corresponds to the action reference for the observation _It−k_ of the base VLA, though it is _not_ used during training. If the robot maintains the same behavior (e.g., constant velocity) between _t−k_ and _t_ + _N −_ 1, then _A_<sup>_t_</sup> = _A_<sup>_t−k_</sup> . Conversely, _A_<sup>_t̸_</sup> = _A_<sup>_t−k_</sup> when the robot changes its behavior. We then compare these two action chunks to identify the data sequences that include changes in the robot’s actions and upweight the samples exhibiting large discrepancies. Specifically, a sample is up-weighted if the distance between the final pose of _A_<sup>_t_</sup> and that of _A_<sup>_t−k_</sup> exceeds a predefined threshold, _d_ th such that _dist_ ( _a_<sup>ref</sup> _t_ +<sup>_,t_</sup> _N −_ 1<sup>_, a_ref</sup> _t−_<sup>_,t_</sup> _k_<sup>_−_</sup> +<sup>_k_</sup> _N −_ 1<sup>)</sup><sup>_> d_th.</sup> 

## _C. End-to-end Training_ 

We train AsyncVLA to learn a reactive Edge Adapter that can dynamically respond to the most recent observation while leveraging the rich understanding of the large base VLA. Our base model, _πb_ can be formulated as follows: 


where _ϕ_ denotes the parameters of the token projector (see Sec. IV-A), and _ψ_ denotes the parameters of the base VLA excluding _ϕ_ . _a_<sup>emb</sup> _t_ + _i_<sup>denotesthe</sup><sup>_i_-thactiontokenembedding.</sup> _g_ denotes the goal, which could be specified in several modalities, such as an image, a 2D pose, or a language prompt. In Fig. 2, these are represented as _Ig_ , _pg_ , and _lg_ , respectively. Note that in our implementation, OmniVLA can be independently conditioned on either _Ig_ , _pg_ , _lg_ , or a combination of these. In our experiments, we focus on the independent cases for _pg_ and _lg_ . We feed _{a_<sup>emb</sup> _t_ + _i_<sup>_}i_=0</sup><sup>_...N−_1 into the following Edge</sup> Adapter, _πs_ and generate the action chunk _{at_ + _i}i_ =0 _...N −_ 1. 


where _θ_ denotes the parameters of the Edge Adapter, 

We train our policy in two steps. At the beginning of the first step, we initialize _ψ_ with the base VLA’s pretrained weights. Then, we train _θ_ and _ϕ_ from scratch, with _ϕ_ frozen. This procedure allows _θ_ and _ϕ_ to acquire reasonable initial weights without degrading the base VLA’s original performance. In the second step, we fine-tune the entire policy end-to-end to better align the base VLA and the Edge Adapter. In both training steps, we optimize the same objective using backpropagation. 


where _J_ im denotes the imitation loss for the action chunk and _J_ sm denotes a smoothing objective on the actions. In the first step, the parameter set is defined as _P_ = _{θ, ϕ}_ , while in the second step it is extended to _P_ = _{θ, ϕ, ψ}_ . Details of _J_ im and _J_ sm are provided in the appendix. 

## IV. IMPLEMENTATION AND SYSTEM DESIGN 

We describe the implementation details for training AsyncVLA, as well as the system design for asynchronous inference on the edge. 

## _A. Network architecture_ 

We build AsyncVLA on top of OmniVLA, a vision-based robotic foundation model for navigation, which serves as our base VLA. OmniVLA is a navigation policy capable of generating actions conditioned on multiple goal modalities, including 2D goal poses, language instructions, and egocentric goal images. The base VLA interprets these diverse modalities at a high level using large-scale visual encoders (SigLIP [55] and DINOv2 [32]) and a language model (LLaMA2 7B [46]). 

Since the downstream Edge Adapter is responsible for action generation, we feed it the action token embeddings of OmniVLA, which encode features that represent the actions but also encode the semantic and visual information interpreted by OmniVLA. However, the embeddings produced by 

OmniVLA have a dimensionality of 8x4x4096, corresponding to an action chunk size of 8, an action dimension of 4, and an embedding size of 4096. Directly feeding these high-dimensional embeddings into the Edge Adapter would significantly increase the network size and computational cost in the robot’s onboard controller. 

To address this issue, we apply a token projector with two MLP ResNet blocks to each action token, compressing its dimensionality from 4×4096 to 1024 before feeding it into the Edge Adapter. This compression enables efficient transmission of the generated token embeddings from the workstation to the robot’s onboard controller during inference. For further details on OmniVLA, please see the original paper [20]. 

In addition to the aspects described in Sec. III for the Edge Adapter, we ensure efficient, low-latency computation by extracting image features using a lightweight visual encoder, EfficientNet-B0 [42], and by resizing input images to 96 _×_ 96, which is less than one quarter of the resolution used by the base VLA. The transformer output corresponding to the current image embedding is then passed to an action head composed of a four-layer MLP, which predicts an action chunk _{at_ + _i}i_ =0 _...N −_ 1 for _N_ steps. 

## _B. Training dataset_ 

We train AsyncVLA on a mixture of public datasets to promote strong generalization. Our training mixture consists of: (1) the GNM dataset, which aggregates six publicly available robotic datasets—RECON [36], CoryHall [22], TartanDrive [47], Seattle [35], SCAND [25], and GO Stanford 4 [16]; (2) the LeLaN dataset [19], which includes in-thewild videos and language-conditioned navigation data; and (3) the SACSoN (HuRoN) dataset [18], which captures dynamic scenes involving pedestrians. 

## _C. Training details_ 

We set the action chunk size _N_ to 8 at a control frequency of 3 Hz, resulting in a temporal horizon of 2.4 seconds for all models. For each training batch, data are uniformly sampled from the GNM [37], SACSoN [18], and LeLaN [19] datasets to balance the dataset domains. For half of each batch, we apply our up-weighting method with a threshold of _d_ th = 1 _._ 0 m. Additionally, for SACSoN, we prioritize samples that include pedestrians using the SACSoN annotations to train robotic behaviors that safely navigate around them. Due to memory constraints that limit batch sizes even on multi-GPU servers, we employ gradient accumulation over multiple steps to stabilize training. 

When training AsyncVLA initialized from OmniVLA checkpoints on five H200 GPUs, we use a per-GPU batch size of 18 and accumulate gradients over two steps, yielding an effective batch size of 180 (= 5 _×_ 18 _×_ 2). To further improve training efficiency, we apply LoRA, which limits the number of trainable parameters to approximately 5% of the model, enabling larger effective batch sizes while maintaining a balance between training speed and stability. LoRA is applied only to the OmniVLA-based model due to its large 

parameter count. All other hyperparameters, including the learning rate, language tokenization, normalization, and related settings, follow the defaults in the OmniVLA codebase [2]. 

## _D. System integration for inference_ 

During inference, we decouple AsyncVLA into the base VLA and the Edge Adapter. The base VLA is deployed on a workstation equipped with a high-performance GPU, while the Edge Adapter is implemented on the robot’s onboard controller to process observations without additional latency. An overview of the system implementation is shown in Fig. 3. 

Due to its lightweight architecture, the Edge Adapter can be executed efficiently on the onboard controller, enabling rapid action generation that reacts to changes in the surrounding environment while leveraging the rich visual and semantic features provided by the base VLA. In contrast, since the base VLA is deployed on a workstation and is not physically connected to the robot, the robot transmits its observed images to the workstation via WiFi for the base VLA inference pass. The action token embeddings produced by the token projector in the base VLA and its time stamp _t − k_ are then sent back to the robot controller over WiFi. 

On the robot controller, when receiving the updated action token embeddings, both the embeddings and the delayed observation _It_<sup>_s_</sup> _−k_<sup>totheEdge Adapterareupdated.Since</sup><sup>_I_</sup> _t_<sup>_s_</sup> _−k_ corresponds to a past image, the robot controller maintains a buffer of past images along with their timestamps, and selects the appropriate _It_<sup>_s_</sup> _−k_<sup>bymatchingthetimestampof</sup> the received action token embeddings with the buffered observations. Similar to ViNT [38] and NoMaD [41], since our action space is the 2D pose, we use a PD controller to generate the velocity commands, which enables the robot to follow the generated 2D poses as actions. We illustrate this process in Algorithm 1. 

## V. EXPERIMENTAL SETUP 

We first describe our experimental setup for evaluating AsyncVLA on real-world robot platforms. We then conduct extensive real-world evaluations and compare our method against state-of-the-art baselines. 

## _A. Navigation tasks_ 

We consider the following two navigation tasks: 

**Goal pose-conditioned navigation:** When conditioned on 2D goal poses, our policy navigates the robot from its initial position to a specified target pose _pg_ . In our experiments, the distance between the initial position and the target pose ranges from 12 to 30 meters. We conduct experiments in diverse environments, including both indoor and outdoor settings. 

For evaluation, we select ten challenging, cluttered environments and perform two trials at different times in each environment. In at least one trial per environment, pedestrians are present and interact with the robot. These interactions are kept consistent across all evaluated methods to ensure fair and reproducible comparisons. 

**Language-conditioned navigation:** We assess AsyncVLA using language commands that not only indicate the target 

**Algorithm 1:** AsyncVLA Inference with Asynchronous Control Frequencies **Input:** Base VLA _πb_ (frequency _fb_ ), Edge Adapter _πs_ (frequency _fs_ ), token projector _ϕ_ **Output:** Executed robot actions Deploy _πb_ on a GPU-equipped workstation; Deploy _πs_ on the robot onboard controller; Initialize image buffer _B ←∅_ ; **while** _robot is operating_ **do Onboard controller loop** (runs at _fs_ ( _> fb_ ) Hz):; Capture current observation _It_ with timestamp _t_ ; Store ( _It, t_ ) in buffer _B_ ; Send _It_ and t to the workstation; **if** _new action token embeddings are received_ **then** Retrieve delayed observation _It−k_ from _B_ via timestamp matching; Update Edge Adapter action token embedding input; Compute action chunk _{_ ∆ _at_ + _i}_<sup>_N_</sup> _i_ =0<sup>_−_1</sup> using _πs_ ; Compute PD controller to generate vel. commands.; Execute vel. commands.; **Workstation loop** (runs at _fb_ Hz, asynchronously):; Receive _It−k_ and _t − k_ from the robot controller; Compute base-model inference using _πb_ with _It−k_ and the given goal inputs ( _lg_ , _pg_ , _lg_ ); Send action token embeddings and timestamp _t − k_ to the robot controller; 


**Fig. 3: Hardware setup for our proposed system.** The Edge Adapter is deployed on an NVIDIA Jetson Orin mounted on a mobile robot (Vizbot), while the base VLA runs on a remote workstation equipped with an NVIDIA RTX 4090. 


**Fig. 4: Time delay between the workstation and the robot onboard controller in our experiments.** We measure time delay across four different environments and visualize the results using distinct colors for each environment. 

## _B. Mobile Robot Platforms_ 

We evaluate AsyncVLA on Vizbot [31] in Fig. 3, a low-cost mobile robot platform. The robot is equipped with multiple sensors, including a fisheye camera, a tracking camera, and wheel velocity sensors on both the left and right wheels. The external tracking camera is used to estimate the robot’s pose as well as the goal location for the 2D pose-conditioned navigation tasks. At each timestep, the robot pose is expressed relative to the target pose _pg_ . 

The Edge Adapter runs on an NVIDIA Jetson Orin configured in 30 W mode, which serves as the onboard robot controller and outputs velocity commands for navigation. The large base VLA is deployed on a workstation equipped with an NVIDIA RTX 4090 GPU. During the experiments, the action token embeddings produced by the base VLA are transmitted to the onboard robot controller via WiFi. 

We measure the interval between sending an image from the robot onboard controller and receiving the corresponding action token embedding from the workstation, corresponding to the delay step _k_ in our system. As shown in Fig. 4, due to WiFi conditions, the system’s time delay varies widely, ranging from 0.28 to 6.0 seconds. We evaluate the robustness of our AsyncVLA in the same environments, which include highly variable time delays. 

## _C. Baselines_ 

destination but also describe the desired navigation behavior during execution. Experiments are carried out in twelve distinct environments, including office spaces, kitchen areas, and entrance halls, with a diverse set of language instructions. Target locations are positioned between 5 and 20 meters from the robot’s starting pose. 

To examine the advantages of leveraging OmniVLA, we evaluate performance under out-of-distribution (OOD) language commands that are not explicitly represented in the training data. Whereas the training set mainly consists of object-directed navigation instructions (e.g., “move toward X”), we design out-of-distribution (OOD) prompts that specify how the robot should navigate toward the goal in half of the evaluation trials (e.g., “move toward X along Y”). These prompts are constructed following the protocol of CAST [14], and the robot’s behavior is evaluated based on its compliance with the provided instructions. 

In our evaluation, we compare AsyncVLA against three state-of-the-art baselines, including lightweight policies as well as large robot foundation models. 

**OmniVLA-edge [20]:** Since OmniVLA-edge is designed as a lightweight policy with 108M parameters, it can be executed entirely on the robot’s onboard controller at 6 Hz. Similar to OmniVLA, OmniVLA-edge supports multiple goal modalities, including 2D goal poses and language prompts. 

**OmniVLA [20]:** We evaluate the original OmniVLA, which we use as the pretrained VLA in AsyncVLA. Since OmniVLA is a large-scale policy with 8.26B parameters, we deploy it on a workstation, where it achieves a maximum inference rate of 5 Hz. To ensure smooth control, velocity commands are issued at 10 Hz by following each generated action pose chunk over 8 steps. 

**Ours without E2E [34]:** Since our task setting differs substantially from that of [34], we adopt only the core idea of 

their approach. We train the Edge Adapter as a lightweight model while keeping the robotic foundation model frozen. During inference, similar to our method, the Edge Adapter is deployed on the robot’s onboard controller, while the base VLA runs on a remote workstation. 

**Ours (workstation):** We keep the entirety of AsyncVLA in the workstation and compare the performance with our proposed implementation using both the workstation and the robot onboard controller. This baseline demonstrates the difference in performance purely from network latency. 

## VI. EVALUATION 

To evaluate the AsyncVLA policy, we design experiments to address the following questions: 

- **Q1** Does AsyncVLA outperform VLA baselines that do not account for latencies in inference? 

- **Q2** Is end-to-end training important for the performance of AsyncVLA? 

- **Q3** Can AsyncVLA quantitatively demonstrate robustness to large delays in the navigation system? 


**Fig. 5: Visualization of 2D pose-conditioned navigation in the presence of a pedestrian under a workstation latency of 0.2 s and fluctuating network latency.** Our AsyncVLA yields to the pedestrian and then continues along the required trajectory to reach the goal. 


**Fig. 6: Visualization of language-conditioned navigation under a workstation latency of 0.2 s.** Our AsyncVLA can achieve strong language following performance by leveraging the large base VLA. 

## _A. AsyncVLA vs. baselines_ 

For **Q1** and **Q2** , we conduct a comparative analysis with several baselines, and summarize the results in Table I. 

**Pose-conditioned performance.** The experiments are conducted mainly in a challenging, cluttered indoor environment, where pedestrians walk around the robot and actively interfere with its motion. Despite these conditions, AsyncVLA successfully reaches the specified goals without colliding with obstacles in 85% of the trials, demonstrating an advantage of 40% over the state-of-the-art baselines. 

The proposed method combines high-level visual and semantic understanding from the base VLA with the Edge Adapter, which runs at high speed on the robot’s onboard controller, enabling dynamic adaptation to disturbances. As a result, it excels at avoiding both static and dynamic obstacles. In contrast, “OmniVLA” and “Ours (workstation)” suffer from longer inference latencies, and the resulting delays lead to frequent collisions when running in real time. We provide the inference frequency in Table I, but the system also suffers from network latencies (since the large models must run off-board), which often significantly delay the actions. We characterize network latency in Fig. 4. The baseline methods also exhibit significant overshooting relative to the shortest path. On average, they require 15% more time to reach the goal. The OmniVLA-edge baseline can run relatively quickly on board, but because it uses a much smaller model, it has more limited visual and semantic capabilities. 

Towards answering **Q2** , we observe that “Ours without E2E”, which is not trained end-to-end, fails to learn a good mapping between the base VLA and the Edge Adapter, resulting in an overall drop in performance compared to AsyncVLA. 

Figure 5 shows a snapshot of a scenario in which a pedestrian walks toward the robot from the front. Although the robot’s maximum speed is 0.3 m/s, significantly slower than the pedestrian, Figure 5[a] demonstrates that AsyncVLA 

allows the robot to yield to the pedestrian, pass safely without collision, and then proceed toward the goal. In contrast, “OmniVLA”, which runs inference on a workstation, suffers from delayed action updates and consequently collides with the pedestrian, failing to reach the goal. 

**Language-conditioned performance.** Since AsyncVLA uses OmniVLA as its pretrained model, it can leverage its ability to map high-level language and visual understanding into actions, enabling behavior that follows language instructions effectively. In our evaluations, AsyncVLA shows robustness to out-of-distribution language instructions, resulting in performance comparable to OmniVLA. Its performance is a substantial advantage over OmniVLA-edge, which relies on a smaller language model, as demonstrated in Fig. 6. These results demonstrate that AsyncVLA effectively preserves the capabilties of OmniVLA while being reactive to its surroundings. 

While our evaluation system experiences delays of up to 6 seconds due to WiFi conditions, AsyncVLA consistently demonstrates robust navigation performance across all modalities. Because the Edge Adapter is designed to leverage the most recent observation while retaining the high-level guidance of the base VLA, AsyncVLA effectively mitigates performance degradation caused by delays, guiding the robot reliably to the goal position without collision. 

## _B. Quantitative analysis for time delay_ 

It is challenging to have reliable quantitative evaluations for the network latency, as it will naturally vary over a WiFi connection. To answer **Q2** , we evaluate the robustness of policies inferenced on the workstation under artificially introduced time delays, simulating increased latency. Specifically, we test workstation latency of 0.2 seconds, 2.0 seconds, and 5.0 seconds, while the robot’s onboard controller computes actions 

|**Method**||**Impleme**|**ntation**|||**2D Pose**||**Language**|
|---|---|---|---|---|---|---|---|---|
||Model size|WS|Edge|SR_↑_|Time [s]_↓_|Static Col. [#]_↓_|Dynamic Col. [#]_↓_|Lan. follow_↑_|
|OmniVLA-edge [20]|108M|–|✓(6.0 Hz)|0.25|80.07|0.60|1.00|0.50|
|OmniVLA [20]|8.26B|✓(5.0 Hz)|–|0.45|70.73|0.30|1.05|**0.83**|
|Ours without E2E [34]|8.27B + 76M|✓(5.0 Hz)|✓(8.0 Hz)|0.25|82.78|0.60|1.05|0.75|
|Ours (workstation)|8.27B + 76M|✓(5.0 Hz)|–|0.30|89.79|0.70|0.50|0.67|
|Ours|8.27B + 76M|✓(5.0 Hz)|✓(8.0 Hz)|**0.85**|**59.18**|**0.10**|**0.10**|0.75|


**TABLE I: Quantitative analysis.** “WS” and “Edge” indicates whether the implementation in running in the workstation with the Nvidia RTX 4090 or the robot edge controller with the Nvidia Jetson Orin. “SR” indicates the success rate, reaching the goal position without any collisions. “Time” indicates the time at which the robot arrives at the goal. “Static Col.” and “Dynamic Col.” indicate the average collision number with static obstacles and pedestrians, respectively. “Behavior” indicates the success rate in following OOD language prompts. 


**Fig. 7: Performance analysis with varying policy computation frequency in the workstation.** To evaluate robustness to time delays, we enforce artificial delays in the workstation and measure the goal arrival rate without collisions, the time taken to reach the goal pose, and the average number of collisions in 2D pose-conditioned navigation. Note that we only consider static collisions, as some methods collide immediately and fail, resulting in skewed collision numbers despite poor performance. 

at its best rate, which is independent of the environment. In this quantitative analysis, OmniVLA is used as the strongest baseline for comparison. 

Figure 7 shows the results of 2D pose-conditioned navigation experiments under varying workstation latency, using the same metrics as in Table I. As shown in Figure 7, our method outperforms OmniVLA at the lowest latency of 0.2 seconds, and this performance gap increases as the artificial latency increases. As the Edge Adapter is running on the onboard controller, it can adapt the guidance provided by the base VLA as the action token embeddings based on information provided in the current observation. In contrast, OmniVLA produces actions conditioned on stale observations, leading to degraded navigation performance as latencies increase. 

Figure 8 shows examples of the robot’s behavior at different workstation latencies. AsyncVLA demonstrates robustness to latency, maintaining similar trajectories toward the goal. In contrast, OmniVLA deviates significantly from the shortest path toward the goal pose and, in this case, collides with static obstacles, failing to reach the goal. 

## VII. DISCUSSION AND FUTURE WORK 

We presented AsyncVLA, a visionand languageconditioned navigation framework that leverages a pretrained VLA for high-level visual and semantic understanding with a lightweight Edge Adapter running on board the robot for fast, 


**Fig. 8: Visualization of 2D pose-conditioned navigation with varying frequencies of the large model computation.** Unlike OmniVLA, our AsyncVLA consistently reaches the goal pose across different frequencies, even in cluttered environments. 

adaptive action inference. This design enables robust navigation in dynamic and partially observable indoor environments and can effectively handle both static and dynamic obstacles while compensating for both network and inference latencies. We demonstrate that AsyncVLA consistently outperforms state-of-the-art baselines, including OmniVLA and OmniVLA-edge, in terms of collision avoidance, adherence to language instructions, and efficiency in goal-reaching. Notably, AsyncVLA maintains high performance even under latency up to 5 seconds, highlighting its robustness to communication latency between the workstation and robot, which are often unavoidable in real-world robot deployments. Furthermore, AsyncVLA shows strong generalization to out-of-distribution language instructions, demonstrating that AsyncVLA can still leverage the rich semantic understanding of OmniVLA while performing rapid inference with its Edge Adapter. 

Although AsyncVLA achieves strong performance in diverse navigation tasks, we are still limited to using base VLA that have open-source weights and, therefore, can be finetuned end-to-end, a step we found crucial to better align the VLA and Edge Adapter. Additionally, AsyncVLA is limited by the small amount of dynamic interactions in available navigation datasets. As future work, we plan to explore how we can further decouple the base VLA and Edge Adapter policies in AsyncVLA and only require training of the Edge 

Adapter, which would also reduce the compute required to train AsyncVLA. Additionally, we will explore other sources of dynamic interactions that can be leveraged as training data for AsyncVLA, such as human video. 

## ACKNOWLEDGMENTS 

This research was supported by Berkeley AI Research at the University of California, Berkeley and Toyota Motor North America. And, this work was partially support by ARL DCIST CRA W911NF-17-2-0181 and the NSF under IIS2150826. We thank Tatsuya Matsushima and Kyle Stachowicz for discussing the initial idea and the system architecture for AsyncVLA. 

## REFERENCES 

- [1] Earth Rovers SDK. https://github.com/frodobots-org/ earth-rovers-sdk, Accessed: 2026-01-30. 

- [2] OmniVLA code base. https://github.com/NHirose/ OmniVLA, Accessed: 2026-01-30. 

- [3] Karl J Astrom. Pid controllers: theory, design, and tuning. _The international society of measurement and control_ , 1995. 

- [4] Suneel Belkhale and Dorsa Sadigh. Minivla: A better vla with a smaller footprint, 2024. URL https://github.com/ Stanford-ILIAD/openvla-mini. 

- [5] Rajat Bhattacharjya, Sing-Yao Wu, Hyunwoo Oh, Chaewon Nam, Suyeon Koo, Mohsen Imani, Elaheh Bozorgzadeh, and Nikil Dutt. Avery: Adaptive vlm split computing through embodied self-awareness for efficient disaster response systems, 2025. URL https://arxiv.org/ abs/2511.18151. 

- [6] Kevin Black, Allen Z. Ren, Michael Equi, and Sergey Levine. Training-time action conditioning for efficient real-time chunking, 2025. URL https://arxiv.org/abs/ 2512.05964. 

- [7] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _π_ 0: A vision-language-action flow model for general robot control, 2026. URL https://arxiv.org/abs/2410.24164. 

- [8] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, Pete Florence, Chuyuan Fu, Montse Gonzalez Arenas, Keerthana Gopalakrishnan, Kehang Han, Karol Hausman, Alexander Herzog, Jasmine Hsu, Brian Ichter, Alex Irpan, Nikhil Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Isabel Leal, Lisa Lee, Tsang-Wei Edward Lee, Sergey Levine, Yao Lu, Henryk Michalewski, Igor Mordatch, Karl Pertsch, Kanishka Rao, Krista Reymann, Michael Ryoo, Grecia Salazar, Pannag Sanketi, Pierre Sermanet, Jaspiar Singh, Anikait Singh, Radu Soricut, 

   - Huong Tran, Vincent Vanhoucke, Quan Vuong, Ayzaan Wahid, Stefan Welker, Paul Wohlhart, Jialin Wu, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, Tianhe Yu, and Brianna Zitkovich. Rt-2: Vision-language-action models transfer web knowledge to robotic control, 2023. URL https://arxiv.org/abs/2307.15818. 

- [9] Qingwen Bu, Hongyang Li, Li Chen, Jisong Cai, Jia Zeng, Heming Cui, Maoqing Yao, and Yu Qiao. Towards synergistic, generalized, and efficient dual-system for robotic manipulation, 2025. URL https://arxiv.org/abs/ 2410.08001. 

- [10] Paweł Budzianowski, Wesley Maa, Matthew Freed, Jingxiang Mo, Winston Hsiao, Aaron Xie, Tomasz Młoduchowski, Viraj Tipnis, and Benjamin Bolte. Edgevla: Efficient vision-language-action models, 2025. URL https://arxiv.org/abs/2507.14049. 

- [11] Hao Chen, Jiaming Liu, Chenyang Gu, Zhuoyang Liu, Renrui Zhang, Xiaoqi Li, Xiao He, Yandong Guo, ChiWing Fu, Shanghang Zhang, et al. Fast-in-slow: A dual-system foundation model unifying fast manipulation within slow reasoning. _arXiv preprint arXiv:2506.01953_ , 2025. 

- [12] Can Cui, Pengxiang Ding, Wenxuan Song, Shuanghao Bai, Xinyang Tong, Zirui Ge, Runze Suo, Wanqi Zhou, Yang Liu, Bofang Jia, Han Zhao, Siteng Huang, and Donglin Wang. Openhelix: A short survey, empirical analysis, and open-source dual-system vla model for robotic manipulation, 2025. URL https://arxiv.org/abs/ 2505.03912. 

- [13] Kevin Frans, Danijar Hafner, Sergey Levine, and Pieter Abbeel. One step diffusion via shortcut models, 2025. URL https://arxiv.org/abs/2410.12557. 

- [14] Catherine Glossop, William Chen, Arjun Bhorkar, Dhruv Shah, and Sergey Levine. Cast: Counterfactual labels improve instruction following in vision-language-action models. _arXiv preprint arXiv:2508.13446_ , 2025. 

- [15] ByungOk Han, Jaehong Kim, and Jinhyeok Jang. A dual process vla: Efficient robotic manipulation leveraging vlm, 2024. URL https://arxiv.org/abs/2410.15549. 

- [16] Noriaki Hirose, Fei Xia, Roberto Mart´ın-Mart´ın, Amir Sadeghian, and Silvio Savarese. Deep visual mpc-policy learning for navigation. _IEEE Robotics and Automation Letters_ , 4(4):3184–3191, 2019. 

- [17] Noriaki Hirose, Dhruv Shah, Ajay Sridhar, and Sergey Levine. Exaug: Robot-conditioned navigation policies via geometric experience augmentation. In _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 4077–4084. IEEE, 2023. 

- [18] Noriaki Hirose, Dhruv Shah, Ajay Sridhar, and Sergey Levine. Sacson: Scalable autonomous control for social navigation. _IEEE Robotics and Automation Letters_ , 9(1): 49–56, 2023. 

- [19] Noriaki Hirose, Catherine Glossop, Ajay Sridhar, Oier Mees, and Sergey Levine. Lelan: Learning a languageconditioned navigation policy from in-the-wild video. In _8th Annual Conference on Robot Learning_ , 2024. 

- [20] Noriaki Hirose, Catherine Glossop, Dhruv Shah, and Sergey Levine. Omnivla: An omni-modal visionlanguage-action model for robot navigation. _arXiv preprint arXiv:2509.19480_ , 2025. 

- [21] Noriaki Hirose, Lydia Ignatova, Kyle Stachowicz, Catherine Glossop, Sergey Levine, and Dhruv Shah. Learning to drive anywhere with model-based reannotation. _IEEE Robotics and Automation Letters_ , 11(2): 1242–1249, 2026. doi: 10.1109/LRA.2025.3640424. 

- [22] Gregory Kahn, Adam Villaflor, Bosen Ding, Pieter Abbeel, and Sergey Levine. Self-supervised deep reinforcement learning with generalized computation graphs for robot navigation. In _2018 IEEE international conference on robotics and automation (ICRA)_ , pages 5129– 5136. IEEE, 2018. 

- [23] Daniel Kahneman. _Thinking, Fast and Slow_ . Farrar, Straus and Giroux, New York, 2011. 

- [24] Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B. Brown, Benjamin Chess, Rewon Child, Scott Gray, Alec Radford, Jeffrey Wu, and Dario Amodei. Scaling laws for neural language models, 2020. URL https://arxiv.org/ abs/2001.08361. 

- [25] Haresh Karnan, Anirudh Nair, Xuesu Xiao, Garrett Warnell, S¨oren Pirk, Alexander Toshev, Justin Hart, Joydeep Biswas, and Peter Stone. Socially compliant navigation dataset (scand): A large-scale dataset of demonstrations for social navigation. _IEEE Robotics and Automation Letters_ , 7(4):11807–11814, 2022. 

- [26] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An open-source vision-language-action model, 2024. URL https://arxiv.org/abs/2406.09246. 

- [27] Yu-Hsiu Lee, Sheng-Chieh Hsu, Yan-Yi Du, Jwu-Sheng Hu, and Tsu-Chin Tsao. A nested-loop iterative learning control for robot manipulators **this research is supported by the industrial technology research institute in taiwan. _IFAC-PapersOnLine_ , 52(15):358–363, 2019. ISSN 2405-8963. doi: https://doi.org/10.1016/ j.ifacol.2019.11.701. URL https://www.sciencedirect. com/science/article/pii/S2405896319316921. 8th IFAC Symposium on Mechatronic Systems MECHATRONICS 2019. 

- [28] Wei Li, Renshan Zhang, Rui Shao, Jie He, and Liqiang Nie. Cogvla: Cognition-aligned vision-language-action model via instruction-driven routing & sparsification, 2025. URL https://arxiv.org/abs/2508.21046. 

- [29] Fanqi Lin, Ruiqian Nai, Yingdong Hu, Jiacheng You, Junming Zhao, and Yang Gao. Onetwovla: A unified vision-language-action model with adaptive reasoning, 2025. URL https://arxiv.org/abs/2505.11917. 

- [30] Tao Lin, Yilei Zhong, Yuxin Du, Jingjing Zhang, Jiting Liu, Yinxinyu Chen, Encheng Gu, Ziyan Liu, Hongyi Cai, Yanwen Zou, Lixing Zou, Zhaoye Zhou, Gen Li, 

and Bo Zhao. Evo-1: Lightweight vision-language-action model with preserved semantic alignment, 2025. URL https://arxiv.org/abs/2511.04555. 

- [31] Takahiro Niwa, Shun Taguchi, and Noriaki Hirose. Spatio-temporal graph localization networks for imagebased navigation. In _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 3279–3286. IEEE, 2022. 

- [32] Maxime Oquab, Timoth´ee Darcet, Theo Moutakanni, Huy V. Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin El-Nouby, Russell Howes, Po-Yao Huang, Hu Xu, Vasu Sharma, Shang-Wen Li, Wojciech Galuba, Mike Rabbat, Mido Assran, Nicolas Ballas, Gabriel Synnaeve, Ishan Misra, Herve Jegou, Julien Mairal, Patrick Labatut, Armand Joulin, and Piotr Bojanowski. Dinov2: Learning robust visual features without supervision, 2023. 

- [33] Reiner Pope, Sholto Douglas, Aakanksha Chowdhery, Jacob Devlin, James Bradbury, Anselm Levskaya, Jonathan Heek, Kefan Xiao, Shivani Agrawal, and Jeff Dean. Efficiently scaling transformer inference, 2022. URL https://arxiv.org/abs/2211.05102. 

- [34] Kohei Sendai, Maxime Alvarez, Tatsuya Matsushima, Yutaka Matsuo, and Yusuke Iwasawa. Leave no observation behind: Real-time correction for vla action chunks. _arXiv preprint arXiv:2509.23224_ , 2025. 

- [35] Amirreza Shaban, Xiangyun Meng, JoonHo Lee, Byron Boots, and Dieter Fox. Semantic terrain classification for off-road autonomous driving. In _Conference on Robot Learning_ , pages 619–629. PMLR, 2022. 

- [36] Dhruv Shah, Benjamin Eysenbach, Nicholas Rhinehart, and Sergey Levine. Rapid exploration for open-world navigation with latent goal models. In _Conference on Robot Learning_ , pages 674–684. PMLR, 2022. 

- [37] Dhruv Shah, Ajay Sridhar, Arjun Bhorkar, Noriaki Hirose, and Sergey Levine. Gnm: A general navigation model to drive any robot. In _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 7226–7233. IEEE, 2023. 

- [38] Dhruv Shah, Ajay Sridhar, Nitish Dashora, Kyle Stachowicz, Kevin Black, Noriaki Hirose, and Sergey Levine. Vint: A foundation model for visual navigation. In _7th Annual Conference on Robot Learning_ , 2023. 

- [39] Yide Shentu, Philipp Wu, Aravind Rajeswaran, and Pieter Abbeel. From llms to actions: Latent codes as bridges in hierarchical robot control, 2025. URL https://arxiv.org/ abs/2405.04798. 

- [40] Mustafa Shukor, Dana Aubakirova, Francesco Capuano, Pepijn Kooijmans, Steven Palma, Adil Zouitine, Michel Aractingi, Caroline Pascal, Martino Russi, Andres Marafioti, Simon Alibert, Matthieu Cord, Thomas Wolf, and Remi Cadene. Smolvla: A vision-languageaction model for affordable and efficient robotics, 2025. URL https://arxiv.org/abs/2506.01844. 

- [41] Ajay Sridhar, Dhruv Shah, Catherine Glossop, and Sergey Levine. Nomad: Goal masked diffusion policies 

for navigation and exploration. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 63–70. IEEE, 2024. 

- [42] Mingxing Tan and Quoc Le. EfficientNet: Rethinking model scaling for convolutional neural networks. In Kamalika Chaudhuri and Ruslan Salakhutdinov, editors, _Proceedings of the 36th International Conference on Machine Learning_ , volume 97 of _Proceedings of Machine Learning Research_ , pages 6105–6114. PMLR, 09–15 Jun 2019. 

- [43] Jiaming Tang, Yufei Sun, Yilong Zhao, Shang Yang, Yujun Lin, Zhuoyang Zhang, James Hou, Yao Lu, Zhijian Liu, and Song Han. Vlash: Real-time vlas via futurestate-aware asynchronous inference, 2025. URL https: //arxiv.org/abs/2512.01031. 

- [44] Gemini Robotics Team, Saminda Abeyruwan, Joshua Ainslie, Jean-Baptiste Alayrac, Montserrat Gonzalez Arenas, Travis Armstrong, Ashwin Balakrishna, Robert Baruch, Maria Bauza, Michiel Blokzijl, Steven Bohez, Konstantinos Bousmalis, Anthony Brohan, Thomas Buschmann, Arunkumar Byravan, Serkan Cabi, Ken Caluwaerts, Federico Casarini, Oscar Chang, Jose Enrique Chen, Xi Chen, Hao-Tien Lewis Chiang, Krzysztof Choromanski, David D’Ambrosio, Sudeep Dasari, Todor Davchev, Coline Devin, Norman Di Palo, Tianli Ding, Adil Dostmohamed, Danny Driess, Yilun Du, Debidatta Dwibedi, Michael Elabd, Claudio Fantacci, Cody Fong, Erik Frey, Chuyuan Fu, Marissa Giustina, Keerthana Gopalakrishnan, Laura Graesser, Leonard Hasenclever, Nicolas Heess, Brandon Hernaez, Alexander Herzog, R. Alex Hofer, Jan Humplik, Atil Iscen, Mithun George Jacob, Deepali Jain, Ryan Julian, Dmitry Kalashnikov, M. Emre Karagozler, Stefani Karp, Chase Kew, Jerad Kirkland, Sean Kirmani, Yuheng Kuang, Thomas Lampe, Antoine Laurens, Isabel Leal, Alex X. Lee, TsangWei Edward Lee, Jacky Liang, Yixin Lin, Sharath Maddineni, Anirudha Majumdar, Assaf Hurwitz Michaely, Robert Moreno, Michael Neunert, Francesco Nori, Carolina Parada, Emilio Parisotto, Peter Pastor, Acorn Pooley, Kanishka Rao, Krista Reymann, Dorsa Sadigh, Stefano Saliceti, Pannag Sanketi, Pierre Sermanet, Dhruv Shah, Mohit Sharma, Kathryn Shea, Charles Shu, Vikas Sindhwani, Sumeet Singh, Radu Soricut, Jost Tobias Springenberg, Rachel Sterneck, Razvan Surdulescu, Jie Tan, Jonathan Tompson, Vincent Vanhoucke, Jake Varley, Grace Vesom, Giulia Vezzani, Oriol Vinyals, Ayzaan Wahid, Stefan Welker, Paul Wohlhart, Fei Xia, Ted Xiao, Annie Xie, Jinyu Xie, Peng Xu, Sichun Xu, Ying Xu, Zhuo Xu, Yuxiang Yang, Rui Yao, Sergey Yaroshenko, Wenhao Yu, Wentao Yuan, Jingwei Zhang, Tingnan Zhang, Allan Zhou, and Yuxiang Zhou. Gemini robotics: Bringing ai into the physical world, 2025. URL https://arxiv.org/abs/2503.20020. 

- [45] Generalist AI Team. Gen-0: Embodied foundation models that scale with physical interaction. _Generalist AI Blog_ , 2025. https://generalistai.com/blog/nov-04-2025- 

GEN-0. 

- [46] Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. Llama 2: Open foundation and fine-tuned chat models. _arXiv preprint arXiv:2307.09288_ , 2023. 

- [47] Samuel Triest, Matthew Sivaprakasam, Sean J Wang, Wenshan Wang, Aaron M Johnson, and Sebastian Scherer. Tartandrive: A large-scale dataset for learning off-road dynamics models. In _2022 International Conference on Robotics and Automation (ICRA)_ , pages 2546– 2552. IEEE, 2022. 

- [48] Chris Vermillion, Amor Menezes, and Ilya Kolmanovsky. Stable hierarchical model predictive control using an inner loop reference model and lambda-contractive terminal constraint sets, 2013. URL https://arxiv.org/abs/ 1305.2651. 

- [49] Hanlei Wang, Wei Ren, Chien Chern Cheah, Yongchun Xie, and Shangke Lyu. Dynamic modularity approach to adaptive control of robotic systems with closed architecture. _IEEE Transactions on Automatic Control_ , 65(6):2760–2767, June 2020. ISSN 2334-3303. doi: 10.1109/tac.2019.2922450. URL http://dx.doi.org/10. 1109/TAC.2019.2922450. 

- [50] Hongyu Wang, Chuyan Xiong, Ruiping Wang, and Xilin Chen. Bitvla: 1-bit vision-language-action models for robotics manipulation, 2025. URL https://arxiv.org/abs/ 2506.07530. 

- [51] Junjie Wen, Minjie Zhu, Yichen Zhu, Zhibin Tang, Jinming Li, Zhongyi Zhou, Chengmeng Li, Xiaoyu Liu, Yaxin Peng, Chaomin Shen, and Feifei Feng. Diffusionvla: Scaling robot foundation models via unified diffusion and autoregression. _arXiv preprint arXiv:None_ , 2024. 

- [52] Junjie Wen, Yichen Zhu, Jinming Li, Minjie Zhu, Kun Wu, Zhiyuan Xu, Ran Cheng, Chaomin Shen, Yaxin Peng, Feifei Feng, et al. Tinyvla: Towards fast, dataefficient vision-language-action models for robotic manipulation. _arXiv preprint arXiv:2409.12514_ , 2024. 

- [53] Junjie Wen, Yichen Zhu, Jinming Li, Zhibin Tang, Chaomin Shen, and Feifei Feng. Dexvla: Visionlanguage model with plug-in diffusion expert for general robot control, 2025. URL https://arxiv.org/abs/2502. 05855. 

- [54] Justin Williams, Kishor Datta Gupta, Roy George, and Mrinmoy Sarkar. Lite vla: Efficient vision-languageaction control on cpu-bound edge robots, 2025. URL https://arxiv.org/abs/2511.05642. 

- [55] Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and Lucas Beyer. Sigmoid loss for language image pretraining, 2023. 

- [56] Jianke Zhang, Yanjiang Guo, Xiaoyu Chen, Yen-Jen Wang, Yucheng Hu, Chengming Shi, and Jianyu Chen. Hirt: Enhancing robotic control with hierarchical robot transformers, 2025. URL https://arxiv.org/abs/2410. 05273. 

- [57] Yongsheng Zhao, Lei Zhao, Baoping Cheng, Gongxin 

Yao, Xuanzhang Wen, and Han Gao. Vla-rail: A realtime asynchronous inference linker for vla models and robots, 2025. URL https://arxiv.org/abs/2512.24673. 

- [58] Jinliang Zheng, Jianxiong Li, Zhihao Wang, Dongxiu Liu, Xirui Kang, Yuchun Feng, Yinan Zheng, Jiayin Zou, Yilun Chen, Jia Zeng, Ya-Qin Zhang, Jiangmiao Pang, Jingjing Liu, Tai Wang, and Xianyuan Zhan. X-vla: Soft-prompted transformer as scalable cross-embodiment vision-language-action model, 2025. URL https://arxiv. org/abs/2510.10274. 

## APPENDIX 

## _A. Training Objective_ 

To train our AsyncVLA, we calculate following _Jim_ and _Jsm_ in Eq. 3 and train our policy to minimize sum of them. 


_J_ im denotes the imitation loss, which encourages the policy to imitate the expert action trajectories. In our design, we impose two forms of action supervision defined in different coordinate frames. Specifically, _a_<sup>ref</sup> _t_ + _i_<sup>representstherobotpose</sup> expressed in the robot-local coordinate frame at time _t_ , while ∆ _a_<sup>ref</sup> _t_ + _i_<sup>represents the relative robot pose expressed with respect</sup> to the coordinate frame at the previous time step _t_ + _i −_ 1. Supervision with _a_<sup>ref</sup> _t_ + _i_<sup>isusefulforlearningthecoarsedi-</sup> rection in which the robot should move, while supervision with ∆ _a_<sup>ref</sup> _t_ + _i_<sup>encouragesrapidactionadjustmentsoverafew</sup> steps in response to dynamic environmental changes. Since our action head predicts action chunk _{_ ∆ _at_ + _i}_<sup>_N_</sup> _i_ =0<sup>_−_1andinternally</sup> integrates them to obtain _{at_ + _i}_<sup>_N_</sup> _i_ =0<sup>_−_1,wecancompute</sup><sup>_Jim_</sup> using these actions. _Jsm_ is the objective to minimize the action deltas for regularization. In _Jsm_ , we set _at−_ 1 as the origin. For the LeLaN dataset, since no raw action references are available, we penalize only the final generated action _at_ + _N −_ 1 to encourage proximity to the target object pose specified by the language prompt, following the LeLaN policy training procedure. 

## _B. Inference details_ 

AsyncVLA is implemented using Robot Operating System (ROS). The communication pipeline begins by transmitting the observed image _It_ from the robot’s onboard controller to a workstation as a compressed image topic. Each image is appended with a timestamp at the moment of capture to ensure temporal synchronization. On the workstation, the base VLA processes the observation and transmits the resulting action token embeddings _{a_<sup>emb</sup> _t_ + _i_<sup>_}i_=0</sup><sup>_...N−_1backtotherobot</sup> via a “VectorStamped” topic. This return message retains the original timestamp of the image _It−k_ to allow the robot edge controller to identify the specific observation used for inference. To facilitate this, we maintain a buffer of observed images and their corresponding timestamps, enabling 

the system to retrieve the matching _It_<sup>_s_</sup> _−k_<sup>uponreceivingthe</sup> embeddings. 

The edge controller processes the retrieved _It_<sup>_s_</sup> _−k_<sup>alongside</sup> the most recent observation _It_<sup>_s_togenerateanactionpose</sup> chunk _{at_ + _i}_<sup>_N_</sup> _i_ =0<sup>_−_1.Followingestablishedprotocolsinthe</sup> literature [37, 38, 41], we employ a PD controller to reach the future waypoint _at_ +2, from which we derive the linear and angular velocity commands. To ensure a fair comparison with baseline methods that exhibit lower inference frame rates, we utilize a PD controller to follow the waypoint trajectory _{at_ + _i}_<sup>_N_</sup> _i_ =0<sup>_−_1</sup> and publish velocity commands at a consistent frequency of 10.0 Hz. For these baselines, the PD controller updates the active waypoint trajectory whenever a new output is received from the baseline policy. Across all evaluated methods, velocity commands are issued as ”Twist” topics to drive the mobile robot. 

## _C. Evaluation details_ 

To evaluate goal pose-conditioned navigation, we selected ten challenging environments, including cluttered indoor spaces and outdoor areas with weak Wi-Fi connectivity. We conducted two trials at different times in each environment to ensure variety. In one of these trials, pedestrians were present and engaged in three specific types of interactions with the robot. These interactions, illustrated in the supplemental videos, were kept consistent across all evaluated methods to ensure a fair and reproducible comparison. 

We define a successful trial as one where the robot reaches a position within 1 meter of the goal without any collisions and within a 120-second time limit. In instances where the robot is able to continue moving after a collision with static obstacles or dynamic pedestrians, navigation is maintained, and the total time taken to reach the goal is recorded. Conversely, if the robot fails to reach the goal, a constant value of 120 seconds is assigned to the trial for the purpose of calculating average performance. Navigation is only manually terminated if the time exceeds 120 seconds or if the robot enters a potentially unsafe situation, such as approaching a descending staircase. 

## _D. Breakdown of quantitative analysis_ 

Table II provides a detailed breakdown of our quantitative experiments for goal pose-conditioned navigation, with metrics categorized by trials conducted with and without pedestrians. The strongest baseline, OmniVLA operating at a 5 Hz inference rate, performs effectively in static scenes, reaching the goal without collision in 90% of trials. However, its performance significantly degrades in dynamic environments, where the latency between the edge controller and the workstation becomes critical. Furthermore, as discussed in the main paper, OmniVLA exhibits a drastic drop in performance when the frame rate is reduced. In contrast, our AsyncVLA maintains high performance in static scenes even at low frame rates. Because our Edge Adapter reacts rapidly to current observations, AsyncVLA successfully avoids collisions and reaches the goal position more reliably. While performance decreases slightly as the workstation’s frame rate is reduced, 

|**Method**|||**Implem**|**entation**|||**2D Pose**||
|---|---|---|---|---|---|---|---|---|
||Model size|Pedestrian|WS|Edge|SR_↑_|Time [s]_↓_|Static Col. [#]_↓_|Dynamic Col. [#]_↓_|
|OmniVLA-edge [20]|108M||–|✓(6.0 Hz)|0.50|76.36|0.50|–|
||108M|✓|–|✓(6.0 Hz)|0.00|83.77|0.70|2.00|
|OmniVLA [20]|8.26B||✓(5.0 Hz)|–|0.90|60.36|0.10|–|
||8.26B|✓|✓(5.0 Hz)|–|0.00|81.09|0.50|2.10|
|OmniVLA [20]|8.26B||✓(0.5 Hz)|–|0.10|112.81|0.90|–|
||8.26B|✓|✓(0.5 Hz)|–|0.00|112.79|0.90|1.60|
|OmniVLA [20]|8.26B||✓(0.2 Hz)|–|0.00|120.00|1.00|–|
||8.26B|✓|✓(0.2 Hz)|–|0.00|120.00|0.90|1.70|
|Ours without E2E [34]|8.27B + 76M||✓(5.0 Hz)|✓(8.0 Hz)|0.50|74.98|0.50|–|
||8.27B + 76M|✓|✓(5.0 Hz)|✓(8.0 Hz)|0.00|90.57|0.70|2.10|
|Ours (workstation)|8.27B + 76M||✓(5.0 Hz)|–|0.40|81.83|0.60|–|
||8.27B + 76M|✓|✓(5.0 Hz)|–|0.20|97.75|0.80|1.00|
|Ours|8.27B + 76M||✓(5.0 Hz)|✓(8.0 Hz)|0.90|52.95|0.10|–|
||8.27B + 76M|✓|✓(5.0 Hz)|✓(8.0 Hz)|0.80|65.41|0.10|0.20|
|Ours|8.27B + 76M||✓(0.5 Hz)|✓(8.0 Hz)|0.90|61.11|0.10|–|
||8.27B + 76M|✓|✓(0.5 Hz)|✓(8.0 Hz)|0.60|71.71|0.30|0.30|
|Ours|8.27B + 76M||✓(0.2 Hz)|✓(8.0 Hz)|0.80|67.83|0.20|–|
||8.27B + 76M|✓|✓(0.2 Hz)|✓(8.0 Hz)|0.50|72.33|0.30|0.70|


**TABLE II: Breakdown of quantitative analysis.** “WS” and “Edge” indicate whether the implementation is running in the workstation with the Nvidia RTX 4090 or the robot edge controller with the Nvidia Jetson Orin. “SR” indicates the success rate, reaching the goal position without any collisions. “Time” indicates the time at which the robot arrives at the goal. “Static Col.” and “Dynamic Col.” indicate the average collision number with static obstacles and pedestrians, respectively. “Behavior” indicates the success rate in following OOD language prompts. 


**Fig. 9: Visualization of generated action chunks from AsyncVLA.** We present three examples of the generated action chunks during navigation. Panel (a) shows the observation provided to the base VLA, denoted as _It−k_ , while panel (b) shows the observation provided to the edge adapter, denoted as _It_ . Panel (c) visualizes the corresponding generated action chunks. In panel (c), the blue curve represents the action chunk generated by the edge adapter using the current observation _It_ , whereas the red curve represents the action chunk obtained by feeding the delayed observation _It−k_ into both the base VLA and the edge adapter. We refer to this red curve as the action chunk of the base VLA, as it is conditioned on the observation _It−k_ . 

our AsyncVLA with 0.2 Hz inference still successfully guides the robot to the goal in 50% of the cases. 

## _E. Visualization of action chunk from AsyncVLA_ 

We visualize the generated action chunks from our AsyncVLA in Fig. 9. We sample three scenes from our experiments and show the observation provided to the base VLA, _It−k_ , in [a], the observation provided to the edge adapter, _It_ , in [b], and the corresponding action chunk trajectories in [c]. In [c], we plot two trajectories: the blue curves represent the action chunks generated by the edge adapter (our method), while the red curves represent the action chunks obtained by feeding the delayed observation _It−k_ into both the base VLA 

and the edge adapter, which we treat as the action chunks of the base VLA. Intuitively, the base VLA provides features to the edge adapter to generate the red trajectories. Across all scenes, the edge adapter appropriately deviates from the red trajectories and refines them to move toward the goal pose in [i] and to avoid collisions with pedestrians in [ii] and [iii]. In [i], the edge adapter correctly infers the relative pose between _It_ and _It−k_ and generates actions toward the target goal. In [ii] and [iii], although pedestrians do not appear in the observations provided to the base VLA, the edge adapter reacts to the current observations, which do capture pedestrians, and generates collision-avoidance behaviors. 

