---
title: "FedVLA: Federated Vision-Language-Action Learning with Dual Gating Mixture-of-Experts for Robotic Manipulation"
date: "2025-08-04"
authors: "Cui Miao; Tao Chang; Meihan Wu; Hongbin Xu; Chun Li; Ming Li"
venue: "ICCV 2025"
url: https://arxiv.org/abs/2508.02190
pdf: https://arxiv.org/pdf/2508.02190
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2508.02190)** / [論文ページ](https://arxiv.org/abs/2508.02190)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This ICCV paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **FedVLA: Federated Vision-Language-Action Learning with Dual Gating Mixture-of-Experts for Robotic Manipulation** 

Cui Miao<sup>1</sup> Tao Chang<sup>1</sup> Meihan Wu<sup>1</sup> Hongbin Xu<sup>2</sup> Chun Li<sup>3</sup> Ming Li<sup>4*</sup> Xiaodong Wang<sup>1</sup> 1 National University of Defense Technology 

2Bytedance Seed 3Shenzhen MSU-BIT University 

4Guangdong Laboratory of Artificial Intelligence and Digital Economy (SZ) 

## **Abstract** 

_Vision-language-action (VLA) models have significantly advanced robotic manipulation by enabling robots to interpret language instructions for task execution. However, training these models often relies on large-scale user-specific data, raising concerns about privacy and security, which in turn limits their broader adoption. To address this, we propose FedVLA, the first federated VLA learning framework, enabling distributed model training that preserves data privacy without compromising performance. Our framework integrates task-aware representation learning, adaptive expert selection, and expert-driven federated aggregation, enabling efficient and privacy-preserving training of VLA models. Specifically, we introduce an InstructionOriented Scene-Parsing mechanism, which decomposes and enhances object-level features based on task instructions, improving contextual understanding. To effectively learn diverse task patterns, we design a Dual Gating Mixtureof-Experts (DGMoE) mechanism, where not only input tokens but also self-aware experts adaptively decide their activation. Finally, we propose an Expert-Driven Aggregation strategy at the federated server, where model aggregation is guided by activated experts, ensuring effective cross-client knowledge transfer. Extensive simulations and real-world robotic experiments demonstrate the effectiveness of our proposals. Notably, DGMoE significantly improves computational efficiency compared to its vanilla counterpart, while FedVLA achieves task success rates comparable to centralized training, effectively preserving data privacy._ 

## **1. Introduction** 

Vision-language-action (VLA) models, which integrate visual perception, linguistic understanding, and robotic control, have significantly enhanced robotic manipulation by 

> *Corresponding author 


Figure 1. Comparison between centralized and federated VLA training. Centralized training collects all user data on the cloud, raising privacy concerns due to potential exposure of sensitive information. Our federated VLA framework enables decentralized training on user devices, preserving privacy while utilizing expertdriven aggregation to enhance model generalization across diverse tasks. 

enabling robots to comprehend and execute complex tasks through natural language instructions [5, 14, 28]. However, training these models requires extensive indoor datasets that capture diverse, user-specific environments, raising serious concerns about data privacy. While recent advancements have improved the capability of VLA models in robotic systems, the issue of privacy leakage remains largely unexplored [19]. 

Federated learning (FL) provides an effective privacypreserving solution for training VLA models [22]. Unlike traditional centralized training, which requires aggregating all user data on a central server, FL enables distributed model training across multiple clients without transferring raw data. As illustrated in Figure 1a, centralized VLA training collects and processes user data in the cloud, posing risks of privacy leakage, such as exposure of personal pref- 

6904 

erences and sensitive health conditions. In contrast, figure 1b presents a federated VLA learning paradigm, where local models are trained on user devices, and only model updates are transmitted to the central server. This decentralized paradigm mitigates privacy risks while allowing collaborative model optimization. 

Existing federated learning approaches are not wellsuited for VLA learning, where robotic manipulation tasks exhibit substantial task heterogeneity across different clients. Typical FL methods, such as FedAvg [22], naively aggregate models across tasks, considering only shared synergies while overlooking their fundamental distinctions. Although recent works attempt to address this issue through merge-and-split training [33] or decoupled model aggregation [20], they remain limited to single-modal settings, assuming a uniform input modality across tasks. In contrast, VLA models operate in multi-modal environments, requiring the joint processing of visual observations, language instructions, and robotic actions, which significantly increases the complexity of federated training. 

Additionally, mixture of experts (MoE) has shown promise in multi-task learning by assigning specialized experts to different tasks [7, 12, 29]. However, existing methods typically select a fixed number of experts, lacking adaptability to tasks of varying complexity. This rigidity makes them inefficient for resource-constrained clients, where optimizing inference speed is critical for real-time robotic responses. These limitations highlight the need for a task-adaptive and flexible FL framework, specifically designed for multi-modal robotic learning. 

In this paper, we introduce FedVLA, a novel federated vision-language-action (VLA) learning framework with Dual Gating MoE, designed to preserve privacy while maintaining high task performance, as illustrated in Figure 1b. To address task heterogeneity and enable effective knowledge aggregation in federated settings, we propose three key components. First, we introduce an Instruction-Oriented Scene-Parsing (IOSP) module to enhance task-aware feature extraction in decentralized environments, where raw images across clients exhibit diverse backgrounds and object distributions. IOSP decomposes observation images into object-level representations guided by task instructions and leverages vision-language alignment techniques to improve contextual understanding. Second, to enhance computational efficiency in federated learning, we develop a Dual Gating MoE (DGMoE) mechanism that enables adaptive knowledge routing. Unlike conventional MoE, which assigns tokens to a fixed number of experts, DGMoE introduces self-aware experts that can accept or reject token assignments, enabling a bidirectional selection process. This dual gating mechanism improves efficiency while preserving task performance. Lastly, to effectively aggregate similar knowledge from diverse client models, we propose the 

Expert-Driven Aggregation (EDA) strategy, which dynamically assigns aggregation weights based on expert similarity across clients. By prioritizing updates from clients that activate similar experts, EDA ensures that semantically aligned knowledge is more prominently integrated at the server side, resulting in a more coherent and specialized global model. 

Our main contributions in this work can be summarized as follows: 

- We propose FedVLA, the first privacy-preserving federated learning framework for VLA training, ensuring that user data remains private and never shared externally. Extensive experiments in both simulation and real-world environments demonstrate that FedVLA achieves performance comparable to centralized training while preserving data privacy. 

- We introduce the Dual Gating Mixture-of-Experts, where self-aware experts autonomously determine their participation, enabling bidirectional token selection to optimize computational efficiency while maintaining task performance. 

- We propose the Expert-Driven Aggregation strategy, which dynamically assigns aggregation weights based on expert similarity across clients, ensuring that semantically aligned knowledge is more effectively integrated, thereby enhancing generalization across heterogeneous tasks. 

## **2. Related Works** 

### **2.1. Vision-Language-Action Models** 

Vision-Language Models (VLMs), which are pre-trained on large-scale datasets, have demonstrated remarkable capabilities in understanding and generating multimodal data [17, 18, 26].Inspired by VLMs, Vision-Language-Action (VLA) models extend their capabilities by integrating robotic action prediction. For instance, RoboFlamingo [15], RT-2 [5], and OpenVLA [14] are all built upon VLMs such as OpenFlamingo [3], PaLI-X [6], and Prismatic [13], respectively. Recent work has begun exploring the training of generalist robots [28], followed by fine-tuning on diverse robot datasets, enabling generalization to novel instructions, unseen objects, and distribution shifts [31]. This progress relies heavily on the availability of large-scale public datasets, such as Open-X Embodiment dataset [24]. During the finetuning phase, samples from real-world scenarios are required, which are often generated by human activities and distributed across users’ home environments. However, these samples frequently expose privacy-sensitive information. 

### **2.2. Privacy-Preserving Training** 

Traditional centralized learning methods require uploading data from multiple sources, which poses significant privacy risks. To mitigate these concerns, researchers have pro- 

6905 


Figure 2. **Illustration of the proposed FedVLA framework and its key component.** (a) An overview of the FedVLA, which consists of multiple clients and a server. Each client processes vision-language-action inputs through the Stem, Trunk, and Head modules. Clients send their updated trunk parameters to the server, where Expert-Driven Aggregation selectively integrates expert-specific updates on server. The global trunk module is then distributed to clients for the next training round. (b) Details of the proposed Dual Gating MoE module. The input tokens first pass through the token-level gate _Gt_ , computing the gating scores for each expert with residual scores from the previous MoE layer. Only the computed scores surpass the expert-level gate _Ge_ , activating the corresponding expert to process the token. Finally, the expert outputs are combined to generate the final output tokens. 

posed various privacy-preserving techniques, including federated learning (FL) [22], differential privacy [9], secure multi-party computation [10], and homomorphic encryption [2]. However, Most privacy-preserving training techniques have been developed for single-modality tasks, and seldomly study the data privacy of embodied AI [32]. In robotic manipulation, the models process multimodal sensor data, including images, language instructions, and action sequences, which can contain sensitive user interaction data. Unlike static datasets, robotic systems continuously collect and process dynamic, task-specific information, making privacy protection more complex. In this context, FL as a solution by allowing decentralized model training without sharing raw data. However, FL for robotic manipulation remains challenging due to task heterogeneity and the need for efficient model aggregation across clients. 

### **2.3. Mixture of Experts in Large Models** 

Mixture of experts [4, 11] is an architecture where multiple experts are trained collaboratively, with each expert responsible for a specific portion of the input space. An MoE consists of two components: a routing mechanism and a set of experts. The experts can either be part of a feedforward network (FFN) or the entire FFN layer, and the routing mechanism allows each token to select experts for processing. By activating a specific number of experts, MoE can reduce resource consumption and improve inference speed. This feature makes MoE particularly effective when integrated into large models, as seen in models like LLaVA-MoE [16], 

DeepSeekMoE [8], and GPT-4 [1]. In this work, we apply MoE to a generalist robot VLA model and introduce a self-aware variant that can adaptively decide whether to be selected, significantly improving deployment efficiency. 

## **3. FedVLA** 

We aim to train a vision-language-action model in a federated learning (FL) framework, ensuring privacy preservation while enabling task generalization across clients. Formally, given _N_ clients C = _{C_ 1 _, C_ 2 _, ..., CN }_ , _N_ local tasks T = _{T_ 1 _, T_ 2 _, ..., TN }_ , and _N_ local datasets D = _{_ D1 _,_ D2 _, ...,_ D _N }_ , each client _Ci_ is associated with a local task _Ti_ and a corresponding dataset D _i_ . The dataset D _i_ contains visual perception image _oi_ , language instruction _li_ of the task, proprioception _si_ of the robot, and action sequence _ai_ executed by the robot: 


where _M_ is the number of samples in dataset D _i_ . To train a federated VLA model _θG_ , the overall federated optimization objective can be formulated as: 


where _Li_ is the Huber loss function computed over each client model’s local dataset D _i_ , _fi_ represents the local client model’s predicted action sequence, and _wi_ denotes the weight assigned to each client during aggregation, which is further detailed in Section 3.3. 

6906 


Figure 3. Instruction-Oriented Scene-Parsing module, which decomposes observations into object-level representations guided by task instructions, enhancing task-aware feature extraction through vision-language alignment. 

The overview of our FedVLA framework is shown in Figure 2. The clients train their models locally and communicate with the server per round until the model converges. The following sections introduce our key proposals: (1) Instruction-Oriented Scene-Parsing (Section 3.1) that decomposes the observation image into object-level embeddings guided by task instructions. (2) Dual Gating Mixtureof-Experts (Section 3.2) that can adaptively select a varying number of experts for tokens based on the relevance to the specific task. (3) Expert-Driven Aggregation (Section 3.3) that dynamically aggregates the weights based on expert similarities across different clients in the server. 

### **3.1. Instruction-Oriented Scene-Parsing** 

To ensure the robot focuses on task-relevant information while maintaining contextual awareness to avoid collisions, we decouple objects in the scene based on the specific robotic task. To achieve this, we propose an InstructionOriented Scene-Parsing (IOSP) module to represent objects within the task scene. 

As illustrated in Figure 3, given an instruction and an image, we first extract Target Objects (TOs) from the instruction using named entity recognition [23]. Simultaneously, we employ YOLOv8 [27] to detect and classify Foreground Objects (FOs) and Background Objects (BOs) in the image. The scene objects are categorized into three groups based on the cosine similarity measured by a pre-trained CLIP model [25] between the instruction and object names, following these matching rules: (1) Target Objects (TOs): Objects explicitly mentioned in the instruction and directly involved in the action. (2) Surrounding Objects (SOs): Foreground objects not in TOs, providing spatial and contextual cues. (3) Background Objects (BOs): Static environmental elements ensuring scene consistency but not directly affecting the task. 

Then, we encode the grouped objects using the CLIP model. The text encoder _H_ maps object names from TOs, SOs, and BOs into textual embeddings _H_ (TOs) _∈_ R<sup>_t×D_</sup> , _H_ (BOs) _∈_ R<sup>_t×D_</sup> , and _H_ (SOs) _∈_ R<sup>_t×D_</sup> . Meanwhile, the vision encoder _P_ processes the entire image into _P_ ( _X_ ) _∈_ R<sup>_t×D_</sup> . We assign image tokens to object groups by computing the cosine similarity between token and text embed- 

dings, selecting the top eight tokens per group. To enhance intra-group feature representation, each group is processed through an MoE module, producing refined image token embeddings. The enhanced tokens are then concatenated with the remaining tokens for subsequent processing. This IOSP module enables the model to focus on critical objects, improving task-specific manipulation. 

### **3.2. Dual Gating Mixture-of-Experts** 

In this section, we introduce Dual Gating Mixture-ofExpert (DGMoE) mechanism that supports adaptive knowledge routing. Different from vanilla MoE, which assigns a fixed number of experts to each token, our DGMoE can automatically determine the acceptance or rejection of the token assignments under the Self-Aware Expert. 

As shown in Figure 2, each DGMoE layer is comprised of _K_ self-aware experts E = _{E_ 1 _, E_ 2 _, . . . , EK}_ . To enable the automatic token-driven expert selection, we introduce two gating mechanisms: Token-side gating mechanism _Gt_ and Expert-side gating mechanism _Ge_ . (1) For Token-side gating, _Gt_ serves as the gating module on the token side, comprised of a soft router module and a gating residual module. The soft router first estimates the selection scores for the hidden inputs, indicating the token preference for different experts. Then the estimated scores from previous layer are incorporated with the scores of current layer, allowing the tokens to inherit the selection prior of the most suitable experts from previous layers. (2) For Expert-side gating, _Ge_ can autonomously accept or reject tokens based on their acceptance threshold. The selection scores predicted by _Gt_ is filtered with a learnable threshold, and only the experts with the most relevant tokens are activated. 

Given an input token _x_ , the token-side gate _Gt_ first computes the scores at the _j_ -th layer by combining the soft router output and the gating residual module: 


where _Wt_<sup>_j_</sup> _∈_ R<sup>_D_</sup> is the trainable weight matrix for soft router, and _Wt_<sup>_g∈_R</sup><sup>_N×N_is a trainable transformation ma-</sup> trix designed to aggregate the scores from the previous layer and the current layer, ensuring smooth expertise knowledge transitions across layers. Then, the token-to-expert selection scores _st_ ( _x_ ) are obtained by normalizing _Gt_ ( _x_ ) with a softmax function, which determines the probability distribution over the available experts. 

On the self-aware expert side, the expert-side gate _Ge_ evaluates the token scores and determines the final expert activation scores _se_ ( _x_ ) as follows: 


where _We_ is a set of trainable self-aware parameters corresponding to the gating values of each expert, and _λ_ is a 

6907 

scaling factor that modulates the gating threshold. In our setting, we set _λ_ = 0 _._ 5 to balance expert selection, ensuring neither excessive expert activation nor overly strict filtering of tokens. 

Then, combining the dual gating mechanism of tokenside and exper-side gating, the expert selection function is defined as follows: 


where the final output token _y_ of the DGMoE layer can be computed as the weighted sum of the selected expert outputs: _K_ 


With the help of self-aware expert gating mechanism, our DGMoE can dynamically activate the most reclevant experts, reducing computational overhead while maintaining task-relevant feature learning. 

### **3.3. Expert-Driven Aggregation** 

To mitigate performance degradation caused by task heterogeneity, we propose an Expert-Driven Aggregation (EDA) strategy, which aggregates model parameters based on the similarity of expert selections across clients. And as shown in Figure 2, we selectively aggregates only the trunk module, while the stem and head modules remain personalized and are excluded from aggregation. 

Given a trunk module with _L_ layers, where each layer contains _K_ experts, each client _Ci_ records an expert selection matrix **V** _i ∈_ R<sup>_L×K_</sup> during each round through DGMoE, where each element _Vi_<sup>(</sup><sup>_l,k_)</sup> represents the number of times expert _k_ is activated in the _l_ -th layer. We extract the expert selection vector for layer _l_ of client _Ci_ as: 


Then we compute the pairwise similarity between clients based on expert selection vectors. The similarity between clients _Ci_ and _Cj_ at layer _l_ is defined as follows: 


Using this similarity, we determine the aggregation weight _wl,i_ for each client _Ci_ at layer _l_ as follows: 


This weighting strategy ensures that clients with higher expert selection similarity contribute more to each other’s model updates, allowing for more effective and task-aligned aggregation across task-heterogeneous clients. 

#### **Algorithm 1 FedVLA: Clients** 

**Input** : Each client _Ci_ has a local task _Ti_ and dataset _Di_ = _{oi, li, si, ai}_ , along with local parameters _ϕi_ , _wi_ , and _θi_ corresponding to the stem, trunk, and head modules, respectively. 

#### 1: **Local** **~~T~~ rain(** _Ci, ϕi, θi_ **):** 

2: **for** each local epoch _e_ from 1 to _Ec_ **do** 3: **for** each batch ( _oi, li, si, ai_ ) sampled from _Di_ **do** 

- 4: // Step 1: Instruction-Oriented Scene-Parsing 5: TOs, SOs, BOs _←{oi, li}_ 6: _FT Os, F_ SOs _, F_ BOs _←_ CLIP(TOs _,_ SOs _,_ BOs) 7: _FO ←_ CLIP( _oi_ ) 8: _X_ TO _←_ topk(cosine( _F_ TOs _, FO_ ) _, FO_ ) 9: _X_ SO _←_ topk(cosine( _F_ SOs _, FO_ ) _, FO_ ) 

- 10: _X_ BO _←_ topk(cosine( _F_ BOs _, FO_ ) _, FO_ ) 11: _X_ in = concat( _X_ TO _, X_ SO _, X_ BO _, si_ ) 

- 12: // Step 2: Forward pass with DGMoE 13: Let _x ∈ MHA_ ( _X_ in) _st_ ( _x_ ) = softmax� _Wt_ ( _x_ )� // token-gate 

- 14: _se_ ( _x_ ) = sign( _st_ ( _x_ ) _− λ We_ ) // expert-gate 15: _g_ ( _x_ ) = _st_ ( _x_ ) _·_ I( _se_ ( _x_ ) _>_ 0) // expert activation _K_ 

- 16: **v**<sup>(</sup><sup>_l_)</sup> _, y_ = � _g_ ( _x_ ) _Ek_ ( _x_ ) // final output _k_ =1 

- 17: // Step 3: Model parameter updates 18: _Li_ = Loss( _f_ ( _ϕi, θi, wi_ ) _, ai_ ) 

- 19: ( _ϕi, θi, wi_ ) _←_ ( _ϕi, θi, wi_ ) _−η ∇Li_ 

- 20: **end for** 

- 21: **end for** 22: **return** _θ,_ **v**<sup>(</sup><sup>_l_)</sup> to the server. 

### **3.4. Algorithms** 

**Clients.** The overall workflow of our FedVLA is shown in Algorithm 1 and Algorithm 2. At the start of each training round _t_ , each client processes task-specific data using Instruction-Oriented Scene-Parsing to extract structured features, followed by Dual Gating MoE for adaptive expert selection.The updated trunk parameters and expert selection counts are then transmitted to the server for global aggregation. The detailed client-side process is described in Algorithm Algorithm 1. 

**Server.** On the server side, the server receives expert selection statistics and trunk updates from all participating clients and performs Expert-Driven Aggregation, which dynamically assigns aggregation weights based on expert selection similarities. The aggregated global trunk module is then redistributed to clients for the next training round. The process is elaborated in Algorithm 2. 

6908 

#### **Algorithm 2 FedVLA: Server** 

**Input** : _T_ is the number of training rounds. _θ_ represents the global trunk parameters. Each client provides **v**<sup>(</sup><sup>_l_)</sup> , the expert selection counts vector for each layer _l_ . 

- 1: **Server** **~~E~~ xecute:** 

- 2: **for** each round _t_ from 1 to _T_ **do** 


- 11: Broadcast updated _θ_ to all clients. 

- 12: **end for** 

## **4. Experiments** 

**Implementation Details.** We validate our FedVLA in both simulation and real-world scenarios, where each client performs a single task, resulting in a non-iid data distribution. We employ the pretrained HPT [28] as the backbone of our VLA model and train it for 1,000 communication rounds between clients and the server, with each client performing local training for 5 epochs per round. In simulation, the model is trained with a learning rate of 5 _×_ 10<sup>_−_6</sup> , while in real-world settings, the learning rate is set to 2 _×_ 10<sup>_−_5</sup> . Each client trains locally with a batch size of 256 using the Adam optimizer. The experiments are conducted on a workstation equipped with 2 GeForce GTX 4090Ti GPUs, 48 Intel Xeon CPUs, and 128GB of memory. 

**Evaluation.** For evaluation, the success and failure of a trial are recoreded as 1 and 0. Each task takes for 15 trials and repeats for 5 times. Since this is the first work on federated VLA learning, we compare FedVLA with two methods. The centralized training (Centralized) aggregates all data on a single server for joint training, serving as an upper bound in performance. The federated averaging (FedAvg) [22] is a strong FL baseline where models are trained locally on each client and simply averaged on the server. 

### **4.1. Simulation** 

**Environment.** We utilize the MuJoCo engine [21] to simulate tasks from the Meta-World robot manipulation benchmark [30]. All tasks are performed using a Sawyer robot with a parallel gripper, positioned at the center of a dinner table. Visual data is captured by three fixed RGB cameras with a resolution of 128 _×_ 128, providing corner, top, and 

shoulder views. For collision detection and dynamics simulation, we employ official physics engines to ensure accurate robotic interactions within the simulation environment. **Tasks.** We evaluate our FedVLA on four household tasks: Door Lock, Close Drawer, Sweep Into, and Open Window. For each task, we collect approximately 30–80 episodes, each consisting of 40–100 steps. The initial pose of robot and environment layouts are randomized to assess the generalization ability of FedVLA. 

|**Method**|**Avg.**|**Door**|**Close**|**Sweep**|**Open**|
|---|---|---|---|---|---|
||**Success**|**Lock**|**Drawer**|**Into**|**Window**|
|Centralized|**65.0**|**86.7**|73.3|53.3|**46.7**|
|FedAvg|51.7|66.7|73.3|40.0|26.7|
|FedVLA (Ours)|63.3|80.0|**80.0**|**53.3**|40.0|


Table 1. Simulation evaluation across four tasks. 

**Performance Comparison.** The evaluation results in the simulation environment are presented in Table 1. FedVLA achieves an average success rate of 63.3%, closely approaching the 65.0% of centralized training. Notably, in the Close Drawer task, FedVLA surpasses centralized training by a success rate margin of about 7.0%. Furthermore, FedVLA consistently outperforms FedAvg, which only achieves an average success rate of 51.7%. This performance gap can be attributed to FedAvg overlooking task heterogeneity in federated learning. In contrast, FedVLA explicitly accounts for task heterogeneity during aggregation by leveraging expert-driven model updates, ensuring that knowledge from diverse clients is effectively integrated to enhance generalization across different tasks. 

### **4.2. Real-World** 

**Hardware.** For real-world experiments, we employ a UR3 robotic arm with six degrees of freedom, equipped with a one-DoF parallel gripper. A RealSense D435i RGB-D camera is mounted above the robot, capturing RGB images in real time at a resolution of 1280 _×_ 720 with a frame rate of approximately 30 Hz. To simulate real-world variations, we introduce moderate randomness in object placement and lighting conditions to better reflect practical deployment scenarios. 

**Tasks.** We collect real-world robotic demonstrations for household-related tasks, including Clean Up, Trash Collection, Open Drawer, and Sorting Pills, as shown in Figure 4. For data collection, we employ an expert teaching method, using inverse kinematics to compute the robot poses corresponding to key point data while recording RGB images and pose data throughout the trajectory. Each task includes approximately 50 demonstrations, with each trajectory consisting of 20 to 80 steps. 

**Performance Comparison.** The real-world experimental results are summarized in Table 2. FedVLA achieves an 

6909 


Figure 4. Real-World Tasks. Each column represents a different task, while each row demonstrates keyframes of task execution. From left to right, the tasks are: _Clean Up_ , where the robot wipes the trash from plate using a cloth. _Trash Collection_ , in which it throws crumpled paper into a trash bin. _Open Drawer_ , which requires grasping and pulling a drawer open, and _Sorting Pills_ , where pill bottles are placed into trays of designated color. 

average task success rate of 63.3%, closely matching the 63.4% of centralized training. Notably, it attains the same success rates as the centralized model in complex tasks such as Trash Collection (46.7%) and Sorting Pills (73.3%). In contrast, FedAvg exhibits a significant performance drop across all tasks, with an average success rate of 53.3%, which is 10.0% lower than our method. These results indicate that FedVLA effectively bridges the performance gap between federated and centralized training. While FedAvg merely averages model parameters across clients, it struggles to generalize effectively in VLA learning, where multimodal information—including textual instructions, scene images, and execution trajectories—is involved, requiring strong feature extraction capabilities. The proposed Dual Gating MoE and Expert-Driven Aggregation mechanisms enable the model to adaptively learn diverse patterns for robotic manipulation, enhancing its ability to handle complex tasks in federated settings. 

|**Mthd**|**Avg.**|**Clean**|**Trash**|**Open**|**Sorting**|
|---|---|---|---|---|---|
|**eo**|**Success**|**Up**|**Collection**|**Drawer**|**Pills**|
|Centralized|**63.4**|46.7|46.7|**86.7**|73.3|
|FedAvg|53.3|46.7|40.0|60.0|66.7|
|FedVLA (Ours)|63.3|**53.3**|**46.7**|80.0|**73.3**|


Table 2. Real-world evaluation across four tasks. 

### **4.3. Ablation Studies** 

To further explore the effectiveness of the IOSP, DGMOE and EDA in FedVLA, we conduct ablation experiments by individually removing each module while keeping the other components. Specifically, the experimental setups are as follows: (1) remove the IOSP module and directly input the 

entire scene image and proprioception data into the encoder (w/o IOSP), (2) replace the DGMoE layers with standard FFN, eliminating adaptive expert selection (w/o DGMOE), and (3) perform vanilla FedAvg aggregation instead of EDA (w/o EDA). We compare the task success rate and record the validation loss during the training process. 

|**Method**|**Avg.**<br>**Success**|**Clean**<br>**Up**|**Trash**<br>**Collection**|**Open**<br>**Drawer**|**Sorting**<br>**Pills**|
|---|---|---|---|---|---|
|w/o IOSP|41.1|40.0|13.3|66.7|46.7|
|w/o DGMoE|31.7|20.0|20.0|46.7|40.0|
|w/o EDA|26.7|26.7|20.0|33.3|26.7|
|FedVLA (Ours)|**63.3**|**53.3**|**46.7**|**80.0**|**73.3**|


Table 3. Ablation studies of proposed FedVLA without IOSP, DGMoE, and EDA. 

From Table 3, we can see that each module contributes significantly to the performance of FedVLA, and the lack of each module will lead to a decrease in the performance of the entire system. Specifically, removing IOSP leads to the highest performance drop in the Trash Collection task from 46.7% to 13.3%, because the number of objects in Trash Collection task is more than the others. The IOSP module discriminates each object from the other for taking the right action to adapt to multi-objects scenarios. DGMoE module strongly relates to the Clean Up task, leading to a success rate drop from 53.3% to 20.0%. The Clean Up task is harder in the manipulation aspect as it requires the robot interaction for multiple steps. The FedVLA depends on the DGMoE module to adaptively select the appropriate number of experts based on different types of tokens, enabling collaborative learning for interaction-rich tasks. Furthermore, the removal of EDA gives the largest reduction in average success rate from 63.3% down to 26.7% As a common aggregation cancels out the knowledge of the experts in the DGMoE module. 

Figure 5 presents the validation loss of the ablation experiments during the first 500 training epochs. We can see that FedVLA consistently achieves the fastest convergence speed, along with the lowest and most stable validation losses across all tasks. Specifically, we can discover that (1) without IOSP causes validation losses notably increase in the multi-object scenarios (depicted in Figure 5b and Figure 5c), (2) the removal of DGMoE results in significantly increased and fluctuating losses the interaction-rich tasks, (3) removing the EDA module causes relatively higher validation losses in most tasks. These findings strongly support that IOSP helps decompose complex visual scenes into task-relevant object representations, DGMoE module routes the adaptive knowledge, EDA ensures the integrity and effectiveness of the aggregation. The integration of these modules together results in a architecture that supports FedVLA’s robustness and adaptability across diverse tasks. 

6910 


Figure 5. Validation loss comparison in ablation study across four tasks. The x-axis represents the training rounds, while the y-axis represents the validation loss. Each subplot includes a zoomed-in inset focusing on the validation loss fluctuations between rounds 400 and 500, illustrating the fine-grained differences in convergence trends. 


Figure 6. Visualization of expert activation distribution per task for different object types. The x-axis represents the three object groups (target objects, surrounding objects, and background objects), where each group contains eight sub-bars corresponding to different experts selected. The left y-axis indicates the activation count, showing how frequently experts are selected for each object type. The right y- axis represents the density of experts per token, illustrating the average number of experts assigned per token in each object category. The dashed line represents the average expert density per token across different object groups, highlighting the dynamic expert selection mechanism of DGMoE. 

### **4.4. Analysis on DGMoE** 

## **5. Conclusion** 

The DGMoE is designed to enhance model efficiency by selectively activating experts based on task complexity and their corresponding object types. In contrast, supporting objects and background objects, which provide contextual spatial information, activate fewer experts compared to target objects. Notably, target objects tend to activate experts 4, 7, and 8 more frequently, supporting objects prefer to select experts 6, 7, and 8, whereas background objects favor experts 2, 3, and 5. This demonstrates that DGMoE not only dynamically allocates computational resources based on object relevance but also selectively routes information to specialized experts, enhancing efficiency and adaptability across different object categories. 

Furthermore, we quantitatively measure the average expert density per token across different tasks, also as shown in Figure 6. The proposed DGMoE achieves consistently lower expert activation densities compared to vanilla top- _k_ MoE, which assigns tokens to a fixed number of experts, where _k_ is typically an integer greater than one. The average number of activated experts per token is 1.219, 1.229, 1.225, and 1.227 for Open Drawer, Sorting Pills, Trash Collection, and Clean Up, respectively. Such dynamic and sparse activation directly translates into significantly reduced forwardpass computation, making DGMoE especially suitable for deployment on resource-constrained edge devices. 

In this work, we introduced FedVLA, a novel federated vision-language action learning framework that preserves privacy and effectively balances data privacy and task performance. To address the challenges of task heterogeneity and efficient knowledge aggregation in decentralized settings, we proposed three key components: the InstructionOriented Scene-Parsing module, which enhances feature extraction by decomposing raw observations into structured object-level representations guided by task instructions. The Dual Gating Mixture-of-Experts, which introduces self-aware experts capable of bidirectional token selection, optimizing computational efficiency while preserving task performance, and the Expert-Driven Aggregation strategy, which dynamically assigns aggregation weights based on expert similarity across clients. Extensive experiments in both simulated and real-world environments demonstrate that FedVLA achieves performance comparable to centralized training while ensuring privacy protection. We believe these results may contribute to the development of more generalizable and scalable federated learning frameworks for robotic manipulation. 

**Acknowledgements.** This research was supported by Guangdong Basic and Applied Basic Research Foundation (No. 2024A1515011774). 

6911 

## **References** 

- [1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023. 3 

- [2] Martin Albrecht, Melissa Chase, Hao Chen, Jintai Ding, Shafi Goldwasser, Sergey Gorbunov, Shai Halevi, Jeffrey Hoffstein, Kim Laine, Kristin Lauter, et al. Homomorphic encryption standard. _Protecting privacy through homomorphic encryption_ , pages 31–62, 2021. 3 

- [3] Anas Awadalla, Irena Gao, Josh Gardner, Jack Hessel, Yusuf Hanafy, Wanrong Zhu, Kalyani Marathe, Yonatan Bitton, Samir Gadre, Shiori Sagawa, et al. Openflamingo: An opensource framework for training large autoregressive visionlanguage models. _arXiv preprint arXiv:2308.01390_ , 2023. 2 

- [4] Denis Blessing, Onur Celik, Xiaogang Jia, Moritz Reuss, Maximilian Li, Rudolf Lioutikov, and Gerhard Neumann. Information maximizing curriculum: A curriculum-based approach for learning versatile skills. _Advances in Neural Information Processing Systems_ , 36:51536–51561, 2023. 3 

- [5] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. _arXiv preprint arXiv:2307.15818_ , 2023. 1, 

   - 2 

- [6] Xi Chen, Josip Djolonga, Piotr Padlewski, Basil Mustafa, Soravit Changpinyo, Jialin Wu, Carlos Riquelme Ruiz, Sebastian Goodman, Xiao Wang, Yi Tay, et al. Pali-x: On scaling up a multilingual vision and language model. _arXiv preprint arXiv:2305.18565_ , 2023. 2 

- [7] Zitian Chen, Yikang Shen, Mingyu Ding, Zhenfang Chen, Hengshuang Zhao, Erik G Learned-Miller, and Chuang Gan. Mod-squad: Designing mixtures of experts as modular multi-task learners. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 11828–11837, 2023. 2 

- [8] Damai Dai, Chengqi Deng, Chenggang Zhao, RX Xu, Huazuo Gao, Deli Chen, Jiashi Li, Wangding Zeng, Xingkai Yu, Y Wu, et al. Deepseekmoe: Towards ultimate expert specialization in mixture-of-experts language models. _arXiv preprint arXiv:2401.06066_ , 2024. 3 

- [9] Cynthia Dwork. Differential privacy. In _International colloquium on automata, languages, and programming_ , pages 1–12. Springer, 2006. 3 

- [10] Oded Goldreich. Secure multi-party computation. _Manuscript. Preliminary version_ , 78(110):1–108, 1998. 3 

- [11] Robert A Jacobs, Michael I Jordan, Steven J Nowlan, and Geoffrey E Hinton. Adaptive mixtures of local experts. _Neural computation_ , 3(1):79–87, 1991. 3 

- [12] Shen Jiang, Guanghui Zhu, Yue Wang, Chunfeng Yuan, and Yihua Huang. Automatic multi-task learning framework with neural architecture search in recommendations. In _Proceedings of the 30th ACM SIGKDD Conference on Knowl-_ 

   - _edge Discovery and Data Mining_ , pages 1290–1300, 2024. 2 

- [13] Siddharth Karamcheti, Suraj Nair, Ashwin Balakrishna, Percy Liang, Thomas Kollar, and Dorsa Sadigh. Prismatic vlms: Investigating the design space of visually-conditioned language models. _arXiv preprint arXiv:2402.07865_ , 2024. 2 

- [14] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 1, 2 

- [15] Xinghang Li, Minghuan Liu, Hanbo Zhang, Cunjun Yu, Jie Xu, Hongtao Wu, Chilam Cheang, Ya Jing, Weinan Zhang, Huaping Liu, et al. Vision-language foundation models as effective robot imitators. _arXiv preprint arXiv:2311.01378_ , 2023. 2 

- [16] Bin Lin, Zhenyu Tang, Yang Ye, Jiaxi Cui, Bin Zhu, Peng Jin, Junwu Zhang, Munan Ning, and Li Yuan. Moe-llava: Mixture of experts for large vision-language models. _arXiv preprint arXiv:2401.15947_ , 2024. 3 

- [17] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. _Advances in neural information processing systems_ , 36, 2024. 2 

- [18] Hao Liu, Wilson Yan, Matei Zaharia, and Pieter Abbeel. World model on million-length video and language with ringattention. _arXiv e-prints_ , pages arXiv–2402, 2024. 2 

- [19] Yang Liu, Weixing Chen, Yongjie Bai, Xiaodan Liang, Guanbin Li, Wen Gao, and Liang Lin. Aligning cyber space with physical world: A comprehensive survey on embodied ai. _arXiv preprint arXiv:2407.06886_ , 2024. 1 

- [20] Yuxiang Lu, Suizhi Huang, Yuwen Yang, Shalayiding Sirejiding, Yue Ding, and Hongtao Lu. Fedhca2: Towards hetero-client federated multi-task learning. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 5599–5609, 2024. 2 

- [21] Ajay Mandlekar, Danfei Xu, Josiah Wong, Soroush Nasiriany, Chen Wang, Rohun Kulkarni, Li Fei-Fei, Silvio Savarese, Yuke Zhu, and Roberto Mart´ın-Mart´ın. What matters in learning from offline human demonstrations for robot manipulation. _arXiv preprint arXiv:2108.03298_ , 2021. 6 

- [22] Brendan McMahan, Eider Moore, Daniel Ramage, Seth Hampson, and Blaise Aguera y Arcas. Communicationefficient learning of deep networks from decentralized data. In _Artificial intelligence and statistics_ , pages 1273–1282. PMLR, 2017. 1, 2, 3, 6 

- [23] David Nadeau and Satoshi Sekine. A survey of named entity recognition and classification. _Lingvisticae Investigationes_ , 30(1):3–26, 2007. 4 

- [24] Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, et al. Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 6892–6903. IEEE, 2024. 2 

6912 

- [25] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al. Learning transferable visual models from natural language supervision. In _International conference on machine learning_ , pages 8748–8763. PmLR, 2021. 4 

- [26] Gemini Team, Rohan Anil, Sebastian Borgeaud, JeanBaptiste Alayrac, Jiahui Yu, Radu Soricut, Johan Schalkwyk, Andrew M Dai, Anja Hauth, Katie Millican, et al. Gemini: a family of highly capable multimodal models. _arXiv preprint arXiv:2312.11805_ , 2023. 2 

- [27] Rejin Varghese and M Sambath. Yolov8: A novel object detection algorithm with enhanced performance and robustness. In _2024 International Conference on Advances in Data Engineering and Intelligent Computing Systems (ADICS)_ , pages 1–6. IEEE, 2024. 4 

- [28] Lirui Wang, Xinlei Chen, Jialiang Zhao, and Kaiming He. Scaling proprioceptive-visual learning with heterogeneous pre-trained transformers. _Advances in Neural Information Processing Systems_ , 37:124420–124450, 2025. 1, 2, 6 

- [29] Jiahui Xu, Lu Sun, and Dengji Zhao. Mome: Mixture-ofmasked-experts for efficient multi-task recommendation. In _Proceedings of the 47th International ACM SIGIR Conference on Research and Development in Information Retrieval_ , pages 2527–2531, 2024. 2 

- [30] Tianhe Yu, Deirdre Quillen, Zhanpeng He, Ryan Julian, Karol Hausman, Chelsea Finn, and Sergey Levine. Metaworld: A benchmark and evaluation for multi-task and meta reinforcement learning. In _Conference on robot learning_ , pages 1094–1100. PMLR, 2020. 6 

- [31] Michał Zawalski, William Chen, Karl Pertsch, Oier Mees, Chelsea Finn, and Sergey Levine. Robotic control via embodied chain-of-thought reasoning. _arXiv preprint arXiv:2407.08693_ , 2024. 2 

- [32] Kaiwen Zhou and Xin Eric Wang. Fedvln: Privacypreserving federated vision-and-language navigation. In _European Conference on Computer Vision_ , pages 682–699. Springer, 2022. 3 

- [33] Weiming Zhuang, Yonggang Wen, Lingjuan Lyu, and Shuai Zhang. Mas: Towards resource-efficient federated multipletask learning. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 23414–23424, 2023. 2 

6913 

