---
title: "Reasoning-VLA: A Fast and General Vision-Language-Action Reasoning Model for Autonomous Driving"
date: "2025-11-25"
authors: "Dapeng Zhang; Zhenlong Yuan; Zhangquan Chen; Chih-Ting Liao; Yinda Chen; Fei Shen"
url: https://arxiv.org/abs/2511.19912
pdf: https://arxiv.org/pdf/2511.19912
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2511.19912)** / [論文ページ](https://arxiv.org/abs/2511.19912)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Reasoning-VLA: A Fast and General Vision-Language-Action Reasoning Model for Autonomous Driving** 

Dapeng Zhang<sup>1,2</sup> , Zhenlong Yuan<sup>3</sup> , Zhangquan Chen<sup>4</sup> , Chih-Ting Liao<sup>5</sup> , Yinda Chen<sup>6</sup> Fei Shen<sup>2*</sup> , Qingguo Zhou<sup>1*</sup> , Tat-Seng Chua<sup>2</sup> 

1 Lanzhou University, China; 2 National University of Singapore, Singapore 

3 University of Science and Technology of China, China; 4 Tsinghua University, China 

5 University of New South Wales, Australia; 6 University of Science and Technology of China, China 

* Corresponding authors 

## **Abstract** 

_Vision-Language-Action (VLA) models have recently shown strong decision-making capabilities in autonomous driving. However, existing VLAs often struggle with achieving efficient inference and generalizing to novel autonomous vehicle configurations and driving scenarios. In this paper, we propose Reasoning-VLA, a general and fast action-generation VLA framework. The proposed model employs a set of learnable action queries, initialized via Gaussian sampling from ground-truth trajectories within the training corpus. These learnable queries interact with reasoning-enhanced vision–language features to generate continuous action trajectories in parallel. To promote robust generalization, we consolidate eight publicly available autonomous driving datasets into a standardized, Chain-of-Thought reasoning–based, and easy-touse data format for model training. Leveraging both supervised learning and reinforcement learning fine-tuning, extensive empirical evaluations across multiple benchmarks demonstrate that Reasoning-VLA achieves state-ofthe-art performance, superior generalization capability, and the excellent inference speed reported to date. Code: https://github.com/xipi702/Reasoning-VLA_ 

## **1. Introduction** 

Autonomous driving (AD) is a highly complex system that requires precise environmental perception and reliable driving behavior generation. Traditional end-to-end AD methods initially advanced the field but face issues such as poor scalability, cumulative errors, and limited generalization across hardware and datasets. These limitations hinder their generalization ability to new driving scenarios. Recently, foundation models—especially large language and vision–language models like CLIP, Qwen2.5VL, and DeepSeek-V3 [1, 26, 36]—have shown remarkable 

generalization through large-scale pretraining. Their capabilities offer a promising direction for building more flexible and robust AD systems. 

Building on these advancements, contemporary frameworks in robotic manipulation and autonomous driving increasingly adopt vision–language generative paradigms (e.g., autoregressive or diffusion-based models [2, 21, 50, 52]), collectively referred to as Vision–Language–Action (VLA) models. These systems generate fine-grained action trajectories from high-level visual–linguistic reasoning, thereby enhancing flexibility and practicality in motion planning and control. Leveraging large-scale pretrained foundation models, recent approaches such as DriveMOE [50] have achieved strong benchmark performance while simultaneously improving interpretability and robustness capabilities in autonomous driving tasks. 

Despite these promising results, **several challenges** hinder the widespread deployment of VLAs in autonomous driving: 1) Most existing VLA architectures are based on autoregressive or diffusion models that require multiple inference steps to generate actions, limiting their suitability for real-time, high-frequency control. 2) Current VLA methods lack robust generalization to new vehicle platforms or unseen driving scenarios. We argue that developing a general-purpose foundation VLA requires diverse, largescale datasets that encompass various environments and vehicle configurations. 3) Existing fine-tuning strategies are often inefficient in exploring the full potential of VLAs, constraining their generalization capability. 

To address these challenges, we propose ReasoningVLA, an efficient and generalist VLA framework that establishes a new state-of-the-art for autonomous driving. First, we design a novel interaction mechanism between action and vision–language modalities by introducing a set of learnable action queries initialized via Gaussian Sampling from ground-truth trajectories in the dataset. 


Figure 1. Reasoning-VLA is an efficient Vision–Language–Action (VLA) framework for autonomous driving that employs parallel actions to interact with reasoning-enhanced vision–language models (VLMs), enabling one-step prediction of future trajectories. The model is trained on our unified and generalized autonomous driving dataset using a combination of supervised fine-tuning (SFT) and reinforcement learning (RL), guided by specifically designed rule-based reward functions. 

These learnable queries interact with reasoning-enhanced vision–language representations through cross-attention to extract action-related information efficiently and generate continuous trajectories in parallel. Second, to enable generalization, we construct a unified, Chain-of-Thought reasoning-based dataset that merges eight publicly available autonomous driving datasets into a coherent and easy-touse format. This dataset covers diverse vehicle platforms and driving scenarios, enhancing the generalization ability of Reasoning-VLA. Finally, we adopt a two-stage training strategy that combines supervised fine-tuning (SFT) and reinforcement learning (RL) to fully exploit the model’s reasoning and planning potential. Extensive experiments demonstrate that Reasoning-VLA significantly improves generalization ability, planning performance, and inference speed compared with existing VLA approaches. To summarize, the main contributions are as follows: 

- We propose Reasoning-VLA, an efficient and fast VLA framework that employs learnable action queries to interact with reasoning-enhanced vision–language representations, enabling one-step parallel action generation. 

- We initialize learnable action queries via Gaussian Distribution Sampling from ground-truth trajectories, improving model efficiency. 

- We construct a unified, Chain-of-Thought reasoningbased autonomous driving dataset that merges eight existing datasets, facilitating generalization across vehicle types and driving environments. 

- We employ a combined SFT and RL fine-tuning strategy augmented with physical and dynamic rewards to en- 

hance the general reasoning ability of Reasoning-VLA, achieving substantial improvements over prior methods. **2. Related Work** 

### **2.1. Classic Autonomous Driving** 

Classic autonomous driving (AD) methods have been developed over many years, evolving from modular systems to modern end-to-end learning frameworks [14, 25, 34, 35, 51, 54, 55]. Early AD systems were typically constructed by cascading these single-task modules into a sequential pipeline [24, 27, 28, 46, 55]. However, such designs suffer from error accumulation, where inaccuracies in upstream tasks propagate through subsequent modules, ultimately degrading overall system performance. To address this issue, recent research has shifted toward end-to-end learning-based approaches that integrate all sub-tasks into a unified framework. Modern open-source end-to-end AD methods increasingly rely on bird’s-eye view (BEV) feature representations and generate planning trajectories through cross-interactions among internal components [5, 13, 18– 20]. Meanwhile, other approaches exploit sparse feature extraction from the 3D environment to directly infer results from image features, thereby avoiding the computational cost of constructing explicit BEV features [41, 46]. Collectively, these advances have simplified the traditional multistage AD pipeline, marking the beginning of a new era of data-driven autonomous driving. 

### **2.2. Vision-Language-Action Models** 

With the rapid advancement of VLMs in recent years [1, 22, 23, 26, 36, 57, 58], researchers have increasingly integrated 

VLMs into autonomous driving and robotic systems to enhance overall performance. For instance, DriveVLM and DriveMM [15, 42] incorporate VLM modules to improve situational understanding and enhance generalization in vehicle control. DriveMLM [45] introduces a behavior planning module that produces optimal driving decisions along with rationales. 

Although these methods effectively model visionlanguage representations, they often neglect the role of action generation, limiting their practical applicability. To address this, recent works have explored integrating visionlanguage understanding with action prediction, directly fine-tuning large pre-trained VLMs to estimate robot actions [2, 3, 56]. These approaches, commonly referred to as Vision–Language–Action (VLA) models. Recent representative VLA methods demonstrate significant performance improvements. OpenVLA [21] employs a pre-trained VLM combined with a discretization bin tokenizer to predict actions. Similarly, _π_ 0 _._ 5 [17] leverages co-training and hybrid multimodal examples—incorporating robot observations, language instructions, and low-level actions—within a single unified model, achieving SOTA performance. The success of VLAs in robotics provides a promising direction for autonomous driving. Some approaches extend novel VLM architectures to train billion-parameter policies with task-specific modifications, offering a direct pathway for AD systems to benefit from rapid VLM advancements [52]. However, most existing VLA methods rely on autoregressive or diffusion-based training and inference, which inherently limits their speed and efficiency [50]. 

### **2.3. Fine-tuning with Reinforcement Learning** 

With the development of extensive pre-training techniques and high-level general capabilities, Reinforcement Learning (RL) has achieved remarkable success in advancing the reasoning and decision-making abilities of LLMs. Reinforcement Learning from Human Feedback (RLHF) approaches, such as PPO [38], typically require training a reward model to optimize the policy network. However, this process can be complex and often unstable. Notably, models such as GPT-4 [33] follow this RL-based fine-tuning paradigm. Building upon PPO, DPO [37] fine-tunes pretrained models to follow instructions and align with human preferences, while eliminating the need for sampling during fine-tuning. Similarly, Qwen3 [49] employs DPO to improve performance in applications. Another variant, GRPO [39], uses sampling to estimate advantages, thereby effectively enhancing the reasoning capabilities of actors. For example, DeepSeek-R1 [11] applies GRPO to advance LLM reasoning, emphasizing self-evolution rather than fine-tuning data. Inspired by these methods, recent works have adopted analogous RL-based fine-tuning strategies to improve the reasoning and decision-making capabil- 

ities of autonomous driving models [52]. 

## **3. Method** 

As illustrated in Fig. 1, the Reasoning-VLA framework comprises three main components: (1) a reasoningenhanced vision–language model (VLM) backbone, (2) an action module that interacts with the VLM and enables parallel decoding of action trajectories, and (3) a multi-stage intermediate refinement module. In the following sections, we present a detailed description of our approach to developing a VLA framework for autonomous driving and highlight key insights. 

### **3.1. Preliminaries: Vision-Language Models** 

In this work, we adopt Qwen2.5-VL [1] as our foundational model. Qwen2.5-VL effectively simulates humanlike analytical thinking, supporting multi-step reasoning, deliberate planning, and problem-solving. Qwen2.5-VL incorporates several architectural innovations: a redesigned Vision Transformer (ViT) with 2D-RoPE and windowed attention for computational efficiency; an MLP-based vision–language merger that compresses visual features into tokens suitable for the LLM; and a large language model initialized with pre-trained Qwen2.5 weights. The model not only exhibits strong vision–language understanding but also maintains robust LLM reasoning capabilities. Furthermore, it generalizes effectively across domains without requiring task-specific fine-tuning, making it a suitable base model for applications such as autonomous driving and action execution in real-world scenarios. 

### **3.2. The Structure of Reasoning-VLA** 

Most existing Vision–Language–Action (VLA) methods either rely on a specialized action tokenizer to convert actions into a format compatible with LLMs—followed by autoregressive generation or employ diffusion/flow matching modules to refine VLM hidden states or noise in order to produce continuous action values. In contrast, our Reasoning-VLA, built on the Qwen2.5-VL symbolic reasoning framework, fundamentally differs from these autoregression-based and diffusion-based approaches [2, 21, 52]. To bridge vision-language representations and action prediction, Reasoning-VLA comprises three primary components: A pre-trained VLM reasoning backbone; A VL-to-Action module that leverages a set of learnable action queries for parallel action decoding; A refinement module that enhances action prediction performance. As illustrated in Fig. 1, the learnable action queries are designed with the same feature dimensionality as the Qwen2.5-VL reasoning model. These queries undergo self-attention and cross-attention with the VLM simultaneously. By employing additional learnable queries, Reasoning-VLA can predict action chunks in a single step, rather than generating actions token by token, as required in autoregressive approaches. The features from these action queries, together 

with intermediate VLM representations, are subsequently processed by a series of refinement modules to produce the final action trajectories. The architectural design of Reasoning-VLA offers four key advantages: 

1. Leverages the reasoning capabilities of the VLM for more informed and context-aware action generation. 

2. Parallel action generation via action queries enables significantly higher inference speed compared to autoregressive or diffusion-based methods. 

3. Learnable action queries are initialized with Gaussiandistributed ground-truth actions, improving model performance. 

4. Refinement modules interact with intermediate hidden states to enhance feature representation and trajectory accuracy. 


Figure 2. The action module interacts with the vision-language model (VLM). The learnable action queries are initialized using a Gaussian distribution derived from the ground-truth (GT) action data. Through self-attention and cross-attention mechanisms with the reasoning VLM, the model transfers the generalized reasoning capability from the VL to A. 

### **3.3. Learnable Action Queries and Initialization** 

#### **3.3.1. Learnable Action Queries** 

We initialize a set of learnable action queries _AQ ∈ T × N × D_ . Here _T_ is the number of future time steps to be predicted, _N_ is the dimensions of action trajectory coordinate, _D_ is the feature dimensionality. As shown in Fig.2. Unlike VLMs, which embedded input tokens into embeddings, our action queries are initialized as learnable parameters. This design provides greater flexibility and expressive capacity, enabling parallel prediction of action trajectories, and offering an efficient alternative to sequential token generation. **3.3.2. Learnable Action Query Initialization** 

To accelerate training convergence, we also initialize the action queries with a set of predefined parameters. These predefined parameters must satisfy two criteria: 1. The predefined parameters must match the shape of action queries; 2. The reasonable initial values that reflect typical action distributions. Given that the total number of action values is _T × N_ , in our method, we predict future _T_ steps for _N_ coordinates (e.g., _x_ , _y_ ), total action query is _N × T_ . We have to generate _T × N_ action queries with _D_ dimensions. 

Specifically, we extract the action trajectory values of each frame firstly (each frame have _N × T_ action values, the total action trajectory values are _Dall × N × T_ , where _Dall_ is the total number of frames in our datasets), then we calculate the mean action values, such as, _x_ 1 _, y_ 1 _, x_ 2 _, y_ 2 _, xi, yi, ..., xN , yN_ , each _xi, yi_ represents the average coordinate for the corresponding position. To match the feature dimension of action queries, we extend the _N × T_ action values to _N × T × D_ , by sampling _D_ values from a Gaussian distribution with the previously calculated mean and variance. This procedure completes the initialization of the learnable action queries, providing a well-structured and informative starting point for training. 

### **3.4. How Do Actions Interact with Vision-Language Reasoning?** 

Unlike autoregression-based or diffusion-based visionlanguage-action (VLA) methods, our approach employs in- 

dependent learnable action queries to predict action trajectories. Consequently, the interaction between the action module and the vision-language model (VLM) differs substantially. Since the action queries are not tied to the VLM’s token representations, they first perform self-attention and then interact with the VLM through cross-attention, as illustrated in Fig. 2. Through these attention mechanisms, the action queries can extract rich and semantically meaningful information from the VLM’s hidden states, which contain extensive reasoning content. This interaction strategy provides a significant advantage: the action queries can generate all expected actions in parallel during a single forward pass, enabling efficient action chunking. This contrasts with autoregression-based VLAs that require sequential tokenby-token processing. Our approach reduces action generation from more than _N × T_ sequential passes to a single pass, substantially improving both training and inference efficiency. Furthermore, we eliminate the discretization process used in autoregressive VLAs, which often degrades fine-grained action details. In addition, we replace the causal attention mask with bidirectional mask, allowing models to predict all actions simultaneously. 

### **3.5. Action Refinement Module** 

To further enhance the representation quality and accuracy of the predicted action trajectories, we introduce an Action Refinement Module (ARM). Specifically, the ARM takes the selected hidden states of the action queries as input and refines them through a combination of multilayer perceptron (MLP) and attention mechanisms. Unlike nexttoken prediction methods (e.g., _π_ 0), which employ discrete action representations, our approach adopts a regressionbased strategy to generate continuous actions. This design preserves the efficiency benefits of parallel action prediction while improving the precision and smoothness of the resulting action trajectories. 

### **3.6. SFT and RL** 

Drawing inspiration from recent advances in VLMs, we employ two complementary training strategies to enhance the generalization ability of our model: supervised fine-tuning (SFT) and reinforcement learning (RL) fine-tuning. 

**SFT.** In this stage, we utilize our unified reasoning dataset to construct structured reasoning chains. Prior studies in VLMs have shown that base models tend to generate tangential or unstructured responses without supervised fine-tuning. Therefore, the SFT process is essential for establishing a solid foundation for subsequent RL training. Reasoning-VLA demonstrates excellent performance on the unified reasoning dataset after SFT. 

**RL.** Although SFT effectively fits the training data, it often struggles to generalize to unseen or out-of-distribution scenarios. To address this limitation, we apply the GRPO [39] during RL fine-tuning. Unlike conventional policybased methods, GRPO replaces the critic model—typically as large as the policy model—with an estimation of group scores. This design not only simplifies the overall architecture but also significantly reduces computational overhead during training. The rule-based reward functions used for RL optimization are introduced in the following subsection. 

### **3.7. Reward Functions** 

Normally, AD methods use BEV 2-dimensions coordinates _x, y_ to optimize the loss function, while neglecting physical trajectory constraints and vehicle dynamics. In our RL fine-tuning stage, we design two types of verifiable reward functions to more accurately evaluate and enhance the quality of generated responses. 

**Physical Trajectory Reward** Different from most regression-based reward functions that employ the mean squared Euclidean distance _N_ <u>1</u> � _Ni_ =1<sup>(</sup><sup>_xi−xi_</sup> gt<sup>)2,weadopt</sup> a weighted Euclidean distance to better align the predicted coordinates with the ground-truth trajectories. Specifically, our physical trajectory reward is defined as: 


where _N_ is the number of trajectory steps, _x_<sup>_i_</sup> and _y_<sup>_i_</sup> are the predicted coordinates at the _i_ -th time step, and _x_<sup>_i_</sup> gt<sup>and</sup> _y_ gt<sup>_i_aretheircorrespondingground-truthvalues.Because</sup> the _x_ and _y_ coordinates in autonomous driving often differ in scale, the weighting factors _α_ and _β_ are introduced to balance their respective contributions to the reward. The term _γ_<sup>_i_</sup> represents a discount factor that reduces the influence of future trajectory points. This reward function encourages the autonomous vehicle to follow the desired route by penalizing deviations across the entire trajectory. 

**Vehicle Dynamic Reward** In autonomous driving, most existing studies rarely incorporate vehicle kinematic and dynamic constraints into motion trajectory prediction. 


Figure 3. Statistical distribution of the unified dataset. 

However, these constraints exert a non-negligible influence on the vehicle’s behavior and overall driving safety. To address this limitation, we propose a Vehicle Dynamics Reward that explicitly accounts for steering and acceleration to constrain the limitations of real-world vehicle dynamics. This design establishes a dynamic constraint optimization objective that ensures physically feasible and stable motion trajectories. The generated action trajectories are governed by both steering kinematics and acceleration dynamics. Specifically, the maximum steering angle is limited to 40 degrees, and the maximum acceleration is constrained to 0.6 gravity. Moreover, abrupt changes in steering or acceleration may lead to vehicle instability or discomfort for passengers. To achieve comfortable and safe driving behavior, the steering constraint reward is defined as: 


where ( _x_<sup>_j_</sup> _, y_<sup>_j_</sup> ) and ( _x_<sup>_j−_1</sup> _, y_<sup>_j−_1)</sup> respectively denote the predicted coordinates at _j − th_ and ( _j −_ 1) _− th_ time step. In this reward function, we reward with 1 when the turning angle is less than 0.84. 

We further introduce an Acceleration Reward to constrain non-physical vehicle dynamics. The acceleration reward is defined as: 


Here _N_ is the number of trajectory steps, _T_ is the time interval between consecutive actions, _j_ is the _j_ -th trajectory step. 

As shown in equation above, the reward function effectively constrains steering and acceleration within physical limits, ensuring that the generated action trajectories are both physically realizable and socially acceptable in 

Table 1. **Open-loop performance on the nuScenes dataset.** Our fully generalized methods, Reasoning-VLA-3B and Reasoning-VLA7B, follow the complete SFT and RL training process described in the Methods section. The training dataset is our unified dataset, which is constructed from NAVSIM [9], nuScenes [4], Waymo [40], Argoverse-V2 [48], KITTI [10], Mapillary [32], ONCE [31], and IDD [43]. The validation dataset comprises the corresponding nuScenes validation clips from the unified dataset. Reasoning-VLA-7B+ is fine-tuned with an additional RL process using the corresponding nuScenes training clips from the unified dataset. *: Official checkpoints re-validated with corrected metrics, sourced from [12]. **Reasoning-VLA-7B represents our general model.** 

|**Methods**||**L2 (**<br>|**m)**_↓_<br>||**C**<br>|**ollision**<br>|**Rate (%)** <br>|_↓_<br>|
|---|---|---|---|---|---|---|---|---|
||1s|2s|3s|Avg.|1s|2s|3s|Avg.|
|**End2End Autonomous**|**Driving**|**Methods**|||||||
|ST-P3[12]|1.33|2.11|2.90|2.11|0.23|0.62|1.27|0.71|
|UniAD[13]*|0.45|0.70|1.04|0.73|0.62|0.58|0.63|0.61|
|VAD[20]*|0.41|0.70|1.05|0.72|0.07|0.17|0.41|0.22|
|PPAD[6]|0.30|0.69|1.26|0.75|0.03|0.22|0.73|0.33|
|SparseDrive[41]|0.29|0.63|0.97|0.63|0.03|0.09|0.19|0.10|
|**VLM & VLA Autonom**<br>|**ous Driv**<br>|**ing Meth**<br>|**ods**<br>||||||
|DriveVLM-Dual[42]|0.15|0.29|0.48|0.31|0.05|0.08|0.17|0.10|
|OmniDrive[44]|0.14|0.29|0.55|0.33|0.00|0.13|0.78|0.30|
|EMMA+[16]|0.13|0.27|0.48|0.29|–|–|–|–|
|Impromptu-VLA[7]|0.13|0.27|0.53|0.30|–|–|–|–|
|**Our Reasoning-VLA M**|**ethods**||||||||
|Reasoning-VLA-3B|0.08|0.33|0.48|0.30|0.04|0.13|0.23|0.13|
|**Reasoning-VLA-7B**|0.05|0.20|0.44|0.23|0.01|0.07|0.15|0.08|
|Reasoning-VLA-7B+|**0.05**|**0.19**|**0.41**|**0.22**|0.02|**0.06**|**0.13**|**0.07**|


mixed traffic scenarios. This design further reinforces the autonomous driving system’s ability to maintain stable and reasonable motion patterns, which are essential for safe and comfortable driving. The final reward _rtotal_ is defined as the weighted sum of _rtraj_ , _rsteer_ and _racc_ . 

_r_ total = _θ_ 1 _r_ traj + _θ_ 2 _r_ steer + _θ_ 3 _r_ acc (5) Here, _θ_ 1 _, θ_ 2 _, θ_ 3 are coefficients that balance the contributions of each sub-reward. 

## **4. Unified Datasets** 

To capture diverse driving scenarios and further improve generalization, we specifically selected eight widely used autonomous driving datasets as the foundation for our unified dataset: NAVSIM [9], nuScenes [4], Waymo [40], Argoverse-V2 [48], KITTI [10], Mapillary [32], ONCE [31], and IDD [43]. However, many of the original clips lack meaningful text-image associations and often have coarse annotations, limiting their suitability for visionlanguage-action (VLA) reasoning and creative generation. 

From these sources, we carefully selected over 75,000 high-quality clips to form a reasoning-intensive dataset. Each clip was processed using a strong reasoning VLM to generate Chain-of-Thought descriptions, followed by comprehensive human verification and visualization to ensure correctness and annotation quality. The final dataset is provided in a consistent, standardized format, facilitating downstream training and evaluation. The statistical analysis of the resulting unified dataset is presented in Fig. 3. 

The processing pipeline for the unified dataset is illustrated in Fig. 5 of Appendix B. A representation of the dataset is also provided in the Appendix B. 

## **5. Experiments** 

We conduct experiments to evaluate Reasoning-VLA as an efficient VLA method for autonomous driving, assess the effectiveness of our training process, and explore its potential as a unified base model for specific autonomous driving tasks. The experiments are designed to answer the following questions: 

1. How does Reasoning-VLA compare to prior autonomous driving VLA, when evaluated across multiple datasets and under various generalization scenarios? 

2. How does each design affect the performance of fine-tuned Reasoning-VLA on general autonomous driving tasks? 

3. Can the design of Reasoning-VLA influence inference efficiency (action generation throughput and latency) and make it more accessible? 

### **5.1. Experiment Setups** 

In our experiments, we mainly evaluate Reasoning-VLA’s performance on unified AD datasets, which are constructed from eight autonomous driving datasets. To fairly compare with existing methods, we retain the original training and testing splits of each dataset. During training, we shuffle the unified datasets and fine-tune Reasoning-VLA sequen- 

Table 2. **Closed-loop performance on the NeuroNCAP.** We utilize the challenging closed-loop NeuroNCAP simulator to emulate a wide range of complex real-world driving scenarios. NeuroNCAP provides pretrained rendering model checkpoints, making it particularly wellsuited for evaluating our method. For our experiments, we downloaded the NeuroAD weights, adapted the evaluation scripts accordingly, and conducted the closed-loop evaluation. Since NeuroNCAP offers a standardized benchmark and evaluation metrics commonly used by other methods, we adhered to its recommended configuration. The Reasoning-VLA modules and fine-tuning process are identical to those employed in the open-loop evaluation. *: Sourced from [29, 53]. 

|**Methods**|**Ne**<br>|**uroNCAP**<br>|**Score**_↑_<br>||**Col**<br>|**lision Rate**<br>|**(%)**_↓_<br>||
|---|---|---|---|---|---|---|---|---|
||Stationary|Frontal|Side|Avg.|Stationary|Frontal|Side|Avg.|
|**End2End & VLA Aut**|**onomous Dri**|**ving Metho**|**ds**||||||
|UniAD[13]*|0.84|0.10|1.26|0.73|87.8|98.4|79.6|88.6|
|VAD[20]*|0.47|0.04|1.45|0.66|96.2|99.6|81.6|92.5|
|SparseDrive[41]*|–|–|–|0.92|–|–|–|93.9|
|BridgeAD-B[53]*|–|–|–|1.60|–|–|–|72.6|
|Impromptu-VLA[7]|1.77|2.31|2.10|2.15|70.0|59.0|65.0|65.5|
|**Our Reasoning-VLA**|**Methods**||||||||
|Reasoning-VLA-3B|1.88|2.29|1.94|2.04|63.7|60.4|64.1|62.7|
|**Reasoning-VLA-7B**|1.93|**2.57**|**2.24**|**2.25**|59.8|**56.0**|**62.2**|**59.4**|
|Reasoning-VLA-7B+|**2.06**|2.33|2.17|2.19|**57.9**|57.4|64.0|59.8|


tially using SFT followed by RL. The decay learning rate are start from 5e-4 and e-6 form SFT and RL separately, the accumulated size is 2. Training is performed for 4 epochs for SFT and 1 epoch for RL, using a total batch size of 8 distributed across 8 H200 GPUs. For open-loop evaluation, we use the same testing and validation clips as employed by prior methods. For closed-loop evaluation, the model is tested on the NeuroNCAP benchmark to enable a fair comparison with other approaches. 

### **5.2. Main Comparison Results** 

#### **5.2.1. Open-loop Evaluation** 

Since our goal is to propose a generalized VLA model for autonomous driving, we train our model using the proposed unified dataset. To ensure a fair comparison with prior methods, we adopt the same validation splits and report results on open-loop benchmarks. The open-loop performance on the nuScenes dataset is summarized in Table 1. Three main models are presented in this table: **Reasoning-VLA-3B:** Based on Qwen2.5-VL-3B, trained using the complete SFT and RL process. **ReasoningVLA-7B:** Based on Qwen2.5-VL-7B and fine-tuned using the SFT and RL process. **Reasoning-VLA-7B+:** Similar to Reasoning-VLA-7B, but additionally fine-tuned with RL on selected nuScenes training clips from the unified dataset. Our results show that the purely generalized model, **Reasoning-VLA-7B** , surpasses previous works across benchmarks, achieving substantial improvements of +23.3% in average L2 and +20.0% in average Collision Rate over the existing best methods. Reasoning-VLA-3B also achieves results comparable to state-of-the-art methods. When fine-tuned with GRPO on specific datasets (i.e., selected nuScenes training clips from the unified dataset), our generalized model demonstrates excellent task-specific performance. As shown in the last row of Table 1, the ad- 

ditional fine-tuning further improves performance across all time intervals: Reasoning-VLA-7B+ achieves increases of 4.3% and 12.5% over Reasoning-VLA-7B in average L2 and Collision Rate, respectively. These results indicate that our approach provides significant improvements in openloop evaluation, highlighting the strong generalization capability of the Reasoning-VLA architecture. Consequently, it can serve as an effective base model for downstream autonomous driving tasks. 

#### **5.2.2. Closed-loop Evaluation** 

We use NeuroNCAP [30] as the closed-loop real-world simulator because it provides renderings of novel, unseen scenarios. Most existing closed-loop real-world simulators are limited in their rendering of the reactions of surrounding objects, such as vehicles and pedestrians, whereas NeuroNCAP offers pretrained rendering model checkpoints, making it particularly well-suited for evaluating our method. As shown in Table 2, the three main models evaluated are the same as those in the open-loop experiments. 

Our methods demonstrate significant advantages in closed-loop performance on NeuroNCAP. The generalized model, Reasoning-VLA-7B, substantially outperforms prior methods in terms of NeuroNCAP Score and Collision Rate, achieving an average NeuroNCAP Score of 2.25 and an average Collision Rate of 59.4. When additionally finetuned with RL on selected nuScenes training clips from the unified dataset, performance on stationary scenarios shows slight improvement; however, overall performance decreases. This is because the smaller nuScenes dataset adjusts the model to fit that specific data, thereby reducing its generalization ability in closed-loop evaluation. Notably, even Reasoning-VLA-3B surpasses competing methods, achieving more than a 4.3% improvement in average 

Table 3. **Generalized performance on our unifed dataset.** We trained two models using the unified dataset: Reasoning-VLA-7B + SFT: This model is fine-tuned using only supervised fine-tuning (SFT). Reasoning-VLA-7B + SFT + RL: This model undergoes the full training process, including both SFT and reinforcement learning (RL). The training dataset for both models is the unified training dataset. For evaluation, the dataset splits follow the recommendations provided by each original dataset. 

|**Datasets**|**Reas**|**oning-V**<br>**L2 (**|**LA-7B +**<br>**m)**_↓_|**SFT**|**Reaso**|**ning-VLA**<br>**L2**|**-7B + SF**<br>**(m)**_↓_|**T + RL**|
|---|---|---|---|---|---|---|---|---|
||1s|2s|3s|Avg.|1s|2s|3s|Avg.|
|NAVSIM[9]|0.05|0.18|0.43|0.22|0.04|0.18|0.41|0.21|
|nuScenes[4]|0.06|0.23|0.48|0.26|0.05|0.20|0.44|0.23|
|Waymo[40]|0.04|0.15|0.44|0.21|0.03|0.14|0.48|0.22|
|Argoverse-V2[48]|0.01|0.13|0.45|0.20|0.01|0.14|0.43|0.19|
|KITTI[10]|0.02|0.15|0.48|0.22|0.01|0.15|0.43|0.20|
|Mapillary[32]|0.04|0.44|0.92|0.47|0.04|0.41|1.01|0.49|
|ONCE[31]|0.07|0.49|0.87|0.48|0.06|0.43|0.90|0.46|
|IDD[43]|0.02|0.29|0.77|0.36|0.03|0.27|0.81|0.37|
|Unified|0.05|0.20|0.47|0.24|0.05|0.19|0.43|0.23|


Collision Rate. These results demonstrate the strong generalization capability of our model, particularly in closed-loop environments that involve previously unseen scenarios. 

Table 4. **Ablation study of components contributions.** R-VLA (Reasoning-VLA) is a 7B-parameter model. All experiments were conducted on our unified dataset and evaluated using a selected subset of the nuScenes dataset extracted from the unified dataset 

|**Methods**|1s|**L2 (**<br>2s|**m)**_↓_<br>3s|Avg.|
|---|---|---|---|---|
|Qwen2.5-VL-7B|0.46|1.33|2.55|1.45|
|R-VLA(w/o AQ)+SFT|0.09|0.31|0.55|0.32|
|<br>R-VLA(w/o AQ)+SFT+RL|0.08|0.30|0.52|0.30|
|R-VLA(w/o AQ-Init)+SFT|0.06|0.27|0.55|0.29|
|<br>R-VLA(w/o AQ-Init)+SFT+RL|0.08|0.23|0.50|0.27|
|R-VLA(w/o ARM)+SFT|0.06|0.28|0.53|0.29|
|<br>R-VLA(w/o ARM)+SFT+RL|0.05|0.24|0.57|0.29|
|R-VLA+SFT|0.06|0.23|0.48|0.26|
|R-VLA+SFT+RL|0.05|0.20|0.44|0.23|


#### **5.2.3. Generalized Performance** 

To evaluate the generalization capability of ReasoningVLA, we tested Reasoning-VLA-7B on eight sub-datasets. As shown in Table 3, our results demonstrate that Reasoning-VLA exhibits strong generalization performance. The model was trained on the unified dataset and evaluated separately on each sub-dataset. We observed that the L2 performance for each sub-dataset closely matches that of the overall unified validation dataset. The variance of the L2 values is minimal, with variance values of 0.012 and 0.014 for average L2 in Reasoning-VLA-7B with SFT and Reasoning-VLA-7B with SFT plus RL, respectively. These results indicate that our method maintains robust generalization across different driving scenarios and vehicle configurations. Besides, the SFT+RL training strategy achieves 

an improvement compare to SFT alone, highlighting the effectiveness of RL. 

### **5.3. Ablation Study** 

#### **5.3.1. Key Design Contributions** 

We conducted ablation studies to evaluate the effectiveness of key component designs, with results summarized in Table 4. Five experimental groups were constructed using different combinations of model components. As shown in Group-1 of Tab.4, the evaluation result of original Qwen2.5-VL-7B in poor performance. Differently, in Group-2, we replaced the learnable action queries with nonlearnable queries and trained the model exclusively on the unified dataset. This modification yielded suboptimal results, achieving an average L2 of 0.32 and 0.30 with SFT and SFT+RL fine-tuning, respectively. In Group-3, only the learnable action query initialization was removed, resulting in a slight performance degradation compared to the full Reasoning-VLA model (Group-5). The results from Groups 2 and 3 suggest that learnable action queries significantly contribute to the model’s ability to generalize across diverse autonomous driving scenarios, thereby enhancing the overall performance of Reasoning-VLA. In Group-4, the action refinement module was removed, and actions were directly regressed from parallel action outputs using an MLP. This sequential strategy led to a modest performance drop relative to Group-5. Overall, these ablation studies demonstrate that each component of Reasoning-VLA contributes to its final performance, confirming the effectiveness of the proposed design. 

More experiments (including ablation studies, generalization performance, efficiency performance and qualitative results) are illustrated in Appendix A. 

## **6. Conclusions** 

This paper presents a general and efficient VLA framework based on a reasoning-enhanced vision-language model for autonomous driving. The proposed method introduces 

learnable action queries, initialized through Gaussian sampling from ground-truth trajectories, which interact with reasoning-augmented vision–language features to generate continuous action trajectories in parallel, thereby significantly improving inference efficiency. To enhance generalization, we unify eight existing autonomous driving datasets into a standardized, reasoning-based, and easyto-use unified dataset. Following supervised fine-tuning (SFT) and reinforcement learning (RL) optimization, our method demonstrates outstanding performance and strong generalization capabilities in autonomous driving tasks. 

## **References** 

- [1] Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang, Shijie Wang, Jun Tang, Humen Zhong, Yuanzhi Zhu, Mingkun Yang, Zhaohai Li, Jianqiang Wan, Pengfei Wang, Wei Ding, Zheren Fu, Yiheng Xu, Jiabo Ye, Xi Zhang, Tianbao Xie, Zesen Cheng, Hang Zhang, Zhibo Yang, Haiyang Xu, and Junyang Lin. Qwen2.5-vl technical report. _arXiv preprint arXiv:2502.13923_ , 2025. 1, 2, 3 

- [2] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _π_ 0: A vision-language-action flow model for general robot control, 2024. 1, 3 

- [3] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, Pete Florence, Chuyuan Fu, Montse Gonzalez Arenas, Keerthana Gopalakrishnan, Kehang Han, Karol Hausman, Alexander Herzog, Jasmine Hsu, Brian Ichter, Alex Irpan, Nikhil Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Isabel Leal, Lisa Lee, Tsang-Wei Edward Lee, Sergey Levine, Yao Lu, Henryk Michalewski, Igor Mordatch, Karl Pertsch, Kanishka Rao, Krista Reymann, Michael Ryoo, Grecia Salazar, Pannag Sanketi, Pierre Sermanet, Jaspiar Singh, Anikait Singh, Radu Soricut, Huong Tran, Vincent Vanhoucke, Quan Vuong, Ayzaan Wahid, Stefan Welker, Paul Wohlhart, Jialin Wu, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, Tianhe Yu, and Brianna Zitkovich. Rt-2: Vision-language-action models transfer web knowledge to robotic control, 2023. 3 

- [4] Holger Caesar, Varun Bankiti, Alex H. Lang, Sourabh Vora, Venice Erin Liong, Qiang Xu, Anush Krishnan, Yu Pan, Giancarlo Baldan, and Oscar Beijbom. nuscenes: A multimodal dataset for autonomous driving. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2020. 6, 8, 2 

- [5] Shaoyu Chen, Bo Jiang, Hao Gao, Bencheng Liao, Qing Xu, Qian Zhang, Chang Huang, Wenyu Liu, and Xinggang Wang. Vadv2: End-to-end vectorized autonomous driving via probabilistic planning, 2024. 2 

- [6] Zhili Chen, Maosheng Ye, Shuangjie Xu, Tongyi Cao, and 

   - Qifeng Chen. Ppad: Iterative interactions of prediction and planning for end-to-end autonomous driving, 2024. 6 

- [7] Haohan Chi, Huan ang Gao, Ziming Liu, Jianing Liu, Chenyu Liu, Jinwei Li, Kaisen Yang, Yangcheng Yu, Zeda Wang, Wenyi Li, Leichen Wang, Xingtao Hu, Hao Sun, Hang Zhao, and Hao Zhao. Impromptu vla: Open weights and open data for driving vision-language-action models, 2025. 6, 7 

- [8] Kashyap Chitta, Aditya Prakash, Bernhard Jaeger, Zehao Yu, Katrin Renz, and Andreas Geiger. Transfuser: Imitation with transformer-based sensor fusion for autonomous driving. _IEEE transactions on pattern analysis and machine intelligence_ , 45(11):12878–12895, 2022. 2 

- [9] Daniel Dauner, Marcel Hallgarten, Tianyu Li, Xinshuo Weng, Zhiyu Huang, Zetong Yang, Hongyang Li, Igor Gilitschenski, Boris Ivanovic, Marco Pavone, Andreas Geiger, and Kashyap Chitta. Navsim: Data-driven nonreactive autonomous vehicle simulation and benchmarking, 2024. 6, 8, 2 

- [10] Andreas Geiger, Philip Lenz, Christoph Stiller, and Raquel Urtasun. Vision meets robotics: The kitti dataset. _The international journal of robotics research_ , 32(11):1231–1237, 2013. 6, 8 

- [11] Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi Wang, and et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning, 2025. 3 

- [12] Shengchao Hu, Li Chen, Penghao Wu, Hongyang Li, Junchi Yan, and Dacheng Tao. St-p3: End-to-end vision-based autonomous driving via spatial-temporal feature learning, 2022. 6 

- [13] Yihan Hu, Jiazhi Yang, Li Chen, Keyu Li, Chonghao Sima, Xizhou Zhu, Siqi Chai, Senyao Du, Tianwei Lin, Wenhai Wang, Lewei Lu, Xiaosong Jia, Qiang Liu, Jifeng Dai, Yu Qiao, and Hongyang Li. Planning-oriented autonomous driving, 2023. 2, 6, 7 

- [14] Junjie Huang and Guan Huang. Bevdet4d: Exploit temporal cues in multi-camera 3d object detection, 2022. 2 

- [15] Zhijian Huang, Chengjian Fen, Feng Yan, Baihui Xiao, Zequn Jie, Yujie Zhong, Xiaodan Liang, and Lin Ma. Drivemm: All-in-one large multimodal model for autonomous driving. _arXiv preprint arXiv:2412.07689_ , 2024. 3 

- [16] Jyh-Jing Hwang, Runsheng Xu, Hubert Lin, Wei-Chih Hung, Jingwei Ji, Kristy Choi, Di Huang, Tong He, Paul Covington, Benjamin Sapp, Yin Zhou, James Guo, Dragomir Anguelov, and Mingxing Tan. Emma: End-to-end multimodal model for autonomous driving, 2025. 6 

- [17] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, James Tanner, Quan Vuong, Homer Walke, Anna Walling, Haohuan Wang, Lili Yu, and Ury Zhilinsky. _π_ 0 _._ 5: a 

vision-language-action model with open-world generalization, 2025. 3 

- [18] Xiaosong Jia, Penghao Wu, Li Chen, Jiangwei Xie, Conghui He, Junchi Yan, and Hongyang Li. Think twice before driving: Towards scalable decoders for end-to-end autonomous driving, 2023. 2 

- [19] Xiaosong Jia, Zhenjie Yang, Qifeng Li, Zhiyuan Zhang, and Junchi Yan. Bench2drive: Towards multi-ability benchmarking of closed-loop end-to-end autonomous driving, 2024. 

- [20] Bo Jiang, Shaoyu Chen, Qing Xu, Bencheng Liao, Jiajie Chen, Helong Zhou, Qian Zhang, Wenyu Liu, Chang Huang, and Xinggang Wang. Vad: Vectorized scene representation for efficient autonomous driving, 2023. 2, 6, 7 

- [21] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An opensource vision-language-action model, 2024. 1, 3 

- [22] Junnan Li, Dongxu Li, Caiming Xiong, and Steven Hoi. BLIP: Bootstrapping language-image pre-training for unified vision-language understanding and generation. In _Proceedings of the 39th International Conference on Machine Learning_ , pages 12888–12900. PMLR, 2022. 2 

- [23] Junnan Li, Dongxu Li, Silvio Savarese, and Steven Hoi. BLIP-2: Bootstrapping language-image pre-training with frozen image encoders and large language models. In _Proceedings of the 40th International Conference on Machine Learning_ , pages 19730–19742. PMLR, 2023. 2 

- [24] Zhiqi Li, Wenhai Wang, Hongyang Li, Enze Xie, Chonghao Sima, Tong Lu, Qiao Yu, and Jifeng Dai. Bevformer: Learning bird’s-eye-view representation from multi-camera images via spatiotemporal transformers, 2022. 2 

- [25] Ming Liang, Bin Yang, Wenyuan Zeng, Yun Chen, Rui Hu, Sergio Casas, and Raquel Urtasun. Pnpnet: End-to-end perception and prediction with tracking in the loop, 2020. 2 

- [26] Aixin Liu, Bei Feng, Bing Xue, Bingxuan Wang, Bochao Wu, Chengda Lu, Chenggang Zhao, Chengqi Deng, Chenyu Zhang, and et al. Deepseek-v3 technical report, 2025. 1, 2 

- [27] Yicheng Liu, Jinghuai Zhang, Liangji Fang, Qinhong Jiang, and Bolei Zhou. Multimodal motion prediction with stacked transformers, 2021. 2 

- [28] Yicheng Liu, Tianyuan Yuan, Yue Wang, Yilun Wang, and Hang Zhao. Vectormapnet: End-to-end vectorized hd map learning, 2023. 2 

- [29] William Ljungbergh and et al. Neural rendering for safetycritical autonomous driving simulation, 2024. 7 

- [30] William Ljungbergh, Adam Tonderski, Joakim Johnander, Holger Caesar, Kalle Astr¨om,<sup>˚</sup> Michael Felsberg, and Christoffer Petersson. Neuroncap: Photorealistic closedloop safety testing for autonomous driving, 2024. 7 

- [31] Jiageng Mao, Niu Minzhe, ChenHan Jiang, hanxue liang, Jingheng Chen, Xiaodan Liang, Yamin Li, Chaoqiang Ye, Wei Zhang, Zhenguo Li, Jie Yu, Chunjing XU, and Hang Xu. One million scenes for autonomous driving: Once dataset. In _Proceedings of the Neural Information Processing Systems Track on Datasets and Benchmarks_ , 2021. 6, 8 

- [32] Gerhard Neuhold, Tobias Ollmann, Samuel Rota Bulo, and Peter Kontschieder. The mapillary vistas dataset for semantic understanding of street scenes. In _Proceedings of the IEEE international conference on computer vision_ , pages 4990– 4999, 2017. 6, 8, 2 

- [33] OpenAI, Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, et al. Gpt-4 technical report, 2024. 3 

- [34] Jonah Philion and Sanja Fidler. Lift, splat, shoot: Encoding images from arbitrary camera rigs by implicitly unprojecting to 3d, 2020. 2 

- [35] Aditya Prakash, Kashyap Chitta, and Andreas Geiger. Multimodal fusion transformer for end-to-end autonomous driving, 2021. 2 

- [36] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, Gretchen Krueger, and Ilya Sutskever. Learning transferable visual models from natural language supervision, 2021. 1, 2 

- [37] Rafael Rafailov, Archit Sharma, Eric Mitchell, Christopher D Manning, Stefano Ermon, and Chelsea Finn. Direct preference optimization: Your language model is secretly a reward model. _Advances in Neural Information Processing Systems_ , 36:53728–53741, 2023. 3 

- [38] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms, 2017. 3 

- [39] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, YK Li, Y Wu, et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. _arXiv preprint arXiv:2402.03300_ , 2024. 3, 5 

- [40] Pei Sun, Henrik Kretzschmar, Xerxes Dotiwalla, Aurelien Chouard, Vijaysai Patnaik, Paul Tsui, James Guo, Yin Zhou, Yuning Chai, Benjamin Caine, et al. Scalability in perception for autonomous driving: Waymo open dataset. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 2446–2454, 2020. 6, 8 

- [41] Wenchao Sun, Xuewu Lin, Yining Shi, Chuang Zhang, Haoran Wu, and Sifa Zheng. Sparsedrive: End-to-end autonomous driving via sparse scene representation, 2024. 2, 6, 7 

- [42] Xiaoyu Tian, Junru Gu, Bailin Li, Yicheng Liu, Yang Wang, Zhiyong Zhao, Kun Zhan, Peng Jia, Xianpeng Lang, and Hang Zhao. Drivevlm: The convergence of autonomous driving and large vision-language models, 2024. 3, 6 

- [43] Girish Varma, Anbumani Subramanian, Anoop Namboodiri, Manmohan Chandraker, and CV Jawahar. Idd: A dataset for exploring problems of autonomous navigation in unconstrained environments. In _2019 IEEE winter conference on applications of computer vision (WACV)_ , pages 1743–1751. IEEE, 2019. 6, 8, 2 

- [44] Shihao Wang, Zhiding Yu, Xiaohui Jiang, Shiyi Lan, Min Shi, Nadine Chang, Jan Kautz, Ying Li, and Jose M. Alvarez. Omnidrive: A holistic vision-language dataset for autonomous driving with counterfactual reasoning, 2025. 6 

- [45] Wenhai Wang, Jiangwei Xie, ChuanYang Hu, Haoming Zou, Jianan Fan, Wenwen Tong, Yang Wen, Silei Wu, Hanming 

Deng, Zhiqi Li, Hao Tian, Lewei Lu, Xizhou Zhu, Xiaogang Wang, Yu Qiao, and Jifeng Dai. Drivemlm: Aligning multimodal large language models with behavioral planning states for autonomous driving, 2023. 3 

- [46] Yue Wang, Vitor Guizilini, Tianyuan Zhang, Yilun Wang, Hang Zhao, and Justin Solomon. Detr3d: 3d object detection from multi-view images via 3d-to-2d queries, 2021. 2 

- [47] Xinshuo Weng, Boris Ivanovic, Yan Wang, Yue Wang, and Marco Pavone. Para-drive: Parallelized architecture for realtime autonomous driving. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 15449–15458, 2024. 2 

- [48] Benjamin Wilson, William Qi, Tanmay Agarwal, John Lambert, Jagjeet Singh, Siddhesh Khandelwal, Bowen Pan, Ratnesh Kumar, Andrew Hartnett, Jhony Kaesemodel Pontes, et al. Argoverse 2: Next generation datasets for self-driving perception and forecasting. _arXiv preprint arXiv:2301.00493_ , 2023. 6, 8, 2 

   - [57] Deyao Zhu, Jun Chen, Xiaoqian Shen, Xiang Li, and Mohamed Elhoseiny. Minigpt-4: Enhancing vision-language understanding with advanced large language models. _arXiv preprint arXiv:2304.10592_ , 2023. 2 

   - [58] Jinguo Zhu, Weiyun Wang, Zhe Chen, Zhaoyang Liu, Shenglong Ye, Lixin Gu, Hao Tian, Yuchen Duan, Weijie Su, Jie Shao, Zhangwei Gao, Erfei Cui, Xuehui Wang, Yue Cao, Yangzhou Liu, Xingguang Wei, Hongjie Zhang, Haomin Wang, Weiye Xu, Hao Li, Jiahao Wang, Nianchen Deng, Songze Li, Yinan He, Tan Jiang, Jiapeng Luo, Yi Wang, Conghui He, Botian Shi, Xingcheng Zhang, Wenqi Shao, Junjun He, Yingtong Xiong, Wenwen Qu, Peng Sun, Penglong Jiao, Han Lv, Lijun Wu, Kaipeng Zhang, Huipeng Deng, Jiaye Ge, Kai Chen, Limin Wang, Min Dou, Lewei Lu, Xizhou Zhu, Tong Lu, Dahua Lin, Yu Qiao, Jifeng Dai, and Wenhai Wang. Internvl3: Exploring advanced training and test-time recipes for open-source multimodal models, 2025. 2 

- [49] Chenfei Wu, Jiahao Li, Jingren Zhou, Junyang Lin, Kaiyuan Gao, Kun Yan, Sheng ming Yin, Shuai Bai, Xiao Xu, Yilei Chen, Yuxiang Chen, Zecheng Tang, Zekai Zhang, Zhengyi Wang, An Yang, Bowen Yu, Chen Cheng, Dayiheng Liu, Deqing Li, Hang Zhang, Hao Meng, Hu Wei, Jingyuan Ni, Kai Chen, Kuan Cao, Liang Peng, Lin Qu, Minggang Wu, Peng Wang, Shuting Yu, Tingkun Wen, Wensen Feng, Xiaoxiao Xu, Yi Wang, Yichang Zhang, Yongqiang Zhu, Yujia Wu, Yuxuan Cai, and Zenan Liu. Qwen-image technical report, 2025. 3 

- [50] Zhenjie Yang, Yilin Chai, Xiaosong Jia, Qifeng Li, Yuqian Shao, Xuekai Zhu, Haisheng Su, and Junchi Yan. Drivemoe: Mixture-of-experts for vision-language-action model in endto-end autonomous driving, 2025. 1, 3 

- [51] Tianyuan Yuan, Yicheng Liu, Yue Wang, Yilun Wang, and Hang Zhao. Streammapnet: Streaming mapping network for vectorized online hd map construction, 2023. 2 

- [52] Zhenlong Yuan, Jing Tang, Jinguo Luo, Rui Chen, Chengxuan Qian, Lei Sun, Xiangxiang Chu, Yujun Cai, Dapeng Zhang, and Shuo Li. Autodrive-r<sup>2</sup> : Incentivizing reasoning and self-reflection capacity for vla model in autonomous driving. 2025. 1, 3 

- [53] Bozhou Zhang, Nan Song, Xin Jin, and Li Zhang. Bridging past and future: End-to-end autonomous driving with historical prediction and planning, 2025. 7 

- [54] Dapeng Zhang, Peng Zhi, Binbin Yong, Jin-Qiang Wang, Yufeng Hou, Lan Guo, Qingguo Zhou, and Rui Zhou. Ehss: An efficient hybrid-supervised symmetric stereo matching network. _2023 IEEE 26th International Conference on Intelligent Transportation Systems (ITSC)_ , pages 1044–1051, 2023. 2 

- [55] Dapeng Zhang, Dayu Chen, Peng Zhi, Yinda Chen, Zhenlong Yuan, Chenyang Li, Sunjing, Rui Zhou, and Qingguo Zhou. Mapexpert: Online hd map construction with simple and efficient sparse map element expert. 2024. 2 

- [56] Dapeng Zhang, Jing Sun, Chenghui Hu, Xiaoyan Wu, Zhenlong Yuan, Rui Zhou, Fei Shen, and Qingguo Zhou. Pure vision language action (vla) models: A comprehensive survey. 2025. 3 

# **Reasoning-VLA: A Fast and General Vision-Language-Action Reasoning Model for Autonomous Driving** 

# Supplementary Material 

## **7. Appendix A** 

### **7.1. Zero-Shot Performance** 

We also conducted a ”zero shot” experiment to further validate the generalization capability of our model. Specifically, the unified dataset was partitioned into distinct scenarios, where the NAVSIM, Waymo, KITTI, and ONCE sub-datasets were used for training, and the remaining four sub-datasets served as validation sets. As shown in Table 5, our method exhibits strong generalization performance on unseen datasets. This experiment confirms that the proposed Reasoning-VLA possesses robust adaptability to new driving scenarios and tasks, highlighting its potential as a general-purpose autonomous driving framework. 

### **7.2. Performance on NAVSIM** 

Moreover, Tab.6 demonstrates the evaluation results on the NAVSIM evaluation. Compared to the Para-Drive method, our approach achieves respective improvements of 0.8, 5.1, 1.4, and 7.7 in DAC, TTC, EP, and PDMS metrics. Overall, the proposed model consistently delivers accurate and reliable predictions across the NAVSIM evaluations, establishing its state-of-the-art performance and strong generalization capability. 

### **7.3. More Ablation Studies** 

#### **7.3.1. The Source of Performance: Generalization Ability or Data Contribution?** 

To further demonstrate that the SOTA performance of Reasoning-VLA arises from its generalization capabilities rather than from reliance on a specific dataset, we conducted two types of experiments, as shown in Tables 7 and 8. We evaluated two types of fine-tuned models: 

**Reasoning-VLA Fine-tuned on the nuScenes Dataset:** The Reasoning-VLA (3B and 7B) models were fine-tuned exclusively on the selected nuScenes subset extracted from the unified dataset. 

**Reasoning-VLA Fine-tuned on the Unified Dataset:** The Reasoning-VLA (3B and 7B) models were fine-tuned on the entire unified dataset. 

Open-loop evaluations were performed on the corresponding nuScenes validation subset of the unified dataset. As shown in Table 7, the Reasoning-VLA models finetuned on the unified dataset outperform those fine-tuned solely on the nuScenes subset in terms of average L2 error and collision rate. Specifically, Reasoning-VLA-7B finetuned on the selected nuScenes subset achieves an average 

L2 error of 0.25 and a collision rate of 0.10, which are 8.7% and 25% lower, respectively, than the general ReasoningVLA-7B fine-tuned on the unified dataset. Closed-loop evaluations, summarized in Table 8, further indicate that models fine-tuned on the unified dataset outperform those trained only on the nuScenes subset across all metrics. These results confirm that Reasoning-VLA possesses strong generalization capabilities in autonomous driving scenarios, comparable to those observed in VLMs. 

#### **7.3.2. Inference Efficiency** 

To evaluate the inference efficiency of Reasoning-VLA, we conducted experiments summarized in Table 9. Compared to existing autoregression-based VLMs, our method achieves superior performance using the same backbone. Reasoning-VLA can generate multiple future trajectories (e.g., 6 or 10 trajectories) in a single inference step, whereas autoregression-based VLA/VLMs must generate these trajectories sequentially. Even when employing the efficient bin-tokenizer proposed by OpenVLA [21] and _π_ 0 [2], these methods require at least 12 to 20 steps to generate the desired trajectories, including both reasoning and trajectory tokens. Our experiments show that Reasoning-VLA achieves a generation speed of 0.089s per inference for 10 trajectories using vLLM, which is approximately 61 times faster than the autoregression-based Qwen2.5-VL7B for the same number of trajectories. These results clearly demonstrate the superior inference efficiency of the Reasoning-VLA design. 

#### **7.3.3. Model Size** 

As is well known, the performance of LLMs and VLMs generally improves with an increase in model parameters. To analyze the impact of model size, we compare the 3B and 7B variants of our Reasoning-VLA. As shown in Tables 1 and 2, the Reasoning-VLA-7B model achieves superior performance, with an average L2 error of 0.23 and an average NeuroNCAP Score of 2.25, representing improvements of 30.4% and 9.3%, respectively, over the ReasoningVLA-3B model. This performance gap indicates that larger models inherently possess stronger representational capacity, enabling them to capture more complex patterns and achieve better results. 

### **7.4. Qualitative Results of Action Trajectories** 

We also provide qualitative results to further demonstrate the effectiveness of Reasoning-VLA. As illustrated in Fig.4, the visualization of predicted action trajectories across eight 

Table 5. **Zero shot performance on our unified dataset.** The unified dataset is divided into two parts: the training set, which includes data from NAVSIM, Waymo, KITTI, and ONCE, and the evaluation sets, which consist of the remaining four sub-datasets along with the unified validation set. 

||**Reas**|**oning-V**|**LA-7B +**|**SFT**|**Reaso**|**ning-VL**|**A-7B + SF**|**T + RL**|
|---|---|---|---|---|---|---|---|---|
|**Datasets**||**L2 (**|**m)**_↓_|||**L2**|**(m)**_↓_||
||1s|2s|3s|Avg.|1s|2s|3s|Avg.|
|nuScenes[4]|0.07|0.24|0.52|0.28|0.08|0.26|0.50|0.28|
|Argoverse-V2[48]|0.03|0.18|0.59|0.27|0.04|0.18|0.55|0.26|
|Mapillary[32]|0.08|0.59|1.09|0.59|0.07|0.57|1.01|0.55|
|IDD[43]|0.09|0.41|0.96|0.49|0.08|0.38|0.93|0.46|
|All|0.07|0.28|0.57|0.31|0.07|0.27|0.53|0.29|


Table 6. **Performance on the NAVSIM.** *: Sourced from [9]. 

|**Methods**|**NC**_↑_|**DAC**_↑_|**TTC**_↑_|**Comfort**_↑_|**EP**_↑_|**PDMS**_↑_|
|---|---|---|---|---|---|---|
|TransFuser[8]*|97.7|92.8|92.8|100|79.2|84.0|
|UniAD[13]*|97.8|91.9|92.9|100|78.8|83.4|
|Para-Drive[47]*|97.9|92.4|93.0|99.8|79.3|84.0|
|Reasoning-VLA-7B|97.8|**93.2**|**98.1**|99.8|**80.7**|**91.7**|


datasets highlights the strong generalization capability of our method. Notably, Reasoning-VLA produces consistent and accurate trajectory predictions even in previously unseen scenarios, confirming its robustness and adaptability. 

### **8.2. CoT Reasoning Unifided Dataset Format and Prompt** 

During the SFT stage of our method, we designed a structured input prompt to facilitate the generation of highquality chain-of-thought (CoT) reasoning data. The prompt template is presented as follows: 

## **8. Appendix B** 

### **8.1. Unified Dataset** 

Existing individual autonomous driving datasets are often limited in scope, providing narrow coverage of the diverse scenarios encountered in real-world driving. To address this, we aggregate eight public datasets to construct a unified, reasoning-intensive dataset designed to support Chainof-Thought generation with a strong reasoning VLM. This unified dataset is organized into a coherent, easy-to-use format to facilitate model training and enhance the generalization capability of Reasoning-VLA. 

The processing pipeline for the unified dataset is illustrated in Fig. 5. First, all source datasets are converted into a standardized data format. The resulting image-text pairs are then input into a VLM, which generates detailed reasoning content according to a predefined labeling protocol. This reasoning output undergoes a rule-based verification process, followed by human review. During human verification, annotators assess the clips along with their associated labels to select the final set of high-quality data. 

- <mark>{’role’: ’system’, ’content’: [{’type’: ’ text’, ’text’: ’You are a helpful assistant’}]},</mark> 

- <mark>{’role’: ’user’, ’content’: [{’type’: ’ image’, ’image’: ’nuScences_441_4000. CAM_FRONT.png’}, {’type’: ’image’, ’ image’: ’nuScences_441_4000.CAM_LEFT. png’}, {’type’: ’image’, ’image’: ’ nuScences_441_4000.CAM_RIGHT.png’}, {’ type’: ’text’, ’text’: "You are an autonomous driving agent. You have access to multi-view camera images of a vehicle: (1) front view (which you</mark> 

- <mark>should focus on with the most attention ) <image>, (2) front right view <image >, and (3) front left view <image>. Your task is to do your best to predict future waypoints for the vehicle over</mark> 

- <mark>the next 10 timesteps, given the vehicle’s intent inferred from the images. Provided are the previous ego vehicle status recorded over the last 3.0 seconds (at 0.5-second intervals). This includes the x and y coordinates</mark> 

Table 7. **Generalization performance on the Open-loop Metrics.** 

|**Methods**|1s|**L2 (**<br>2s|**m)**_↓_<br>3s|Avg.|<br>1s|**Collision**<br>2s|**Rate (%)** <br>3s|_↓_<br>Avg.|
|---|---|---|---|---|---|---|---|---|
|**Reasoning-VLA Finet**|**uned with**|**nuScenes**|**Dataset**||||||
|Reasoning-VLA-3B|0.10|0.38|0.51|0.33|0.05|0.13|0.27|0.15|
|Reasoning-VLA-7B|0.07|0.23|0.46|0.25|0.01|0.08|0.20|0.10|
|**Reasoning-VLA Finet   i**|**uned with  i**|**Our Unii**|**fied Datase**|**i t**|||||
|Reasoning-VLA-3B|0.08|0.33|0.48|0.30|0.04|0.13|0.23|0.13|
|Reasoning-VLA-7B|0.05|0.20|0.44|0.23|0.01|0.07|0.15|0.08|


Table 8. **Generalization performance on the Closed-loop Metrics.** 

|**Methods**|**Ne**<br>Stationary|**uroNCAP**<br>Frontal|**Score**_↑_<br>Side|Avg.|**Col**<br>Stationary|**lision Rate**<br>Frontal|**(%)**_↓_<br>Side|Avg.|
|---|---|---|---|---|---|---|---|---|
|**Reasoning-VLA Fine**|**tuned with n**|**uScenes Da**|**taset**||||||
|Reasoning-VLA-3B|1.67|2.16|1.83|1.89|69.0|63.3|66.6|66.3|
|Reasoning-VLA-7B|1.79|2.44|2.12|2.12|61.5|57.1|65.1|61.3|
|**Reasoning-VLA Fine   i**|**tuned with O i**|**ur Unified**|**i Dataset**||||||
|Reasoning-VLA-3B|1.88|2.29|1.94|2.04|63.7|60.4|64.1|62.7|
|Reasoning-VLA-7B|1.93|2.57|2.24|2.25|59.8|56.0|62.2|59.4|


Table 9. **The Efficiency Comparisons.** Steps: Theoretical number of VLM inference steps required to complete a single prediction process. Speed(s): Measured inference time to generate a complete prediction process. All experiments were conducted on an NVIDIA H200 GPU using vLLM. Traj: Number of predicted trajectories. 

|**Methods**|**Steps**|**Speed(s)**|
|---|---|---|
|Qwen2.5-VL-7B(6 Traj)|_≫_12|5.396|
|Qwen2.5-VL-7B(10 Traj)|_≫_20|5.472|
|Reasoning-VLA-7B(6 Traj)|1|0.081|
|Reasoning-VLA-7B(10 Traj)|1|0.089|


<mark>of the ego vehicle. Positive x means forward direction while positive y means leftwards. The data is presented in the format [x, y]:(t-3.0s) [-21.95, -0.11], Acceleration: X 0.22, Y 0.21 m/ sˆ2, Velocity: X 6.93, Y 0.0 m/s, (t -2.5s) [-18.42, -0.07], Acceleration: X 0.19, Y 0.22 m/sˆ2, Velocity: X 7.03, Y 0.0 m/s, (t-2.0s) [-14.88, -0.05], Acceleration: X 0.26, Y 0.15 m/sˆ2, Velocity: X 7.16, Y 0.0 m/s, (t-1.5s) [-11.22, -0.02], Acceleration: X 0.16, Y 0.15 m/sˆ2, Velocity: X 7.25, Y 0.0 m /s, (t-1.0s) [-7.15, 0.02], Acceleration: X -0.21, Y 0.16 m/sˆ2, Velocity: X 7.23, Y 0.0 m/s, (t-0.5s)</mark> 

<mark>[-3.52, 0.02], Acceleration: X -0.39, Y 0.19 m/sˆ2, Velocity: X 7.09, Y 0.0 m/ s, (t-0.0s) [0.0, 0.0], Acceleration: X -0.51, Y -0.06 m/sˆ2, Velocity: X</mark> 

   - <mark>6.88, Y 0.0 m/s\n\nPlease think deeply. Engage in an internal dialogue other</mark> 

   - <mark>natural language thought expressions It ’s a reasoning process. Provide your reasoning between the <think> </think> tags, and then give your answer between the <answer> </answer> tags. Predicted future movement details for the next 5 seconds (sampled at 0.5-second</mark> 

   - <mark>intervals), including BEV location in x and y directions (in meters). Positive x means forward direction while</mark> 

   - <mark>positive y means leftwards. The output is formatted as [x, y]."}]},</mark> 

- <mark>{’role’: ’assistant’, ’content’: [{’type’: ’text’, ’text’: "<think>\nLet me think</mark> 

- <mark>. To rephrase the question in a way that requires Chain-of-Thought reasoning with numerical or mathematical expressions, we should break down the prediction of future waypoints into smaller steps, starting from understanding the provided data and applying relevant physics equations . \n\nThe original question asks for</mark> 


Figure 4. **Qualitative Results of Action Trajectories.** Reasoning-VLA predictions on eight different datasets.Red lines denote GT trajectories while green lines represent predicted trajectories. 


Figure 5. Pipeline for generating the unified reasoning dataset. 

<mark>predicting the future waypoints directly from the given vehicle status, but let’s derive the waypoints through intermediate calculations. \n \nOh, I see. The question now needs to be framed in such a way that the responder understands they need.\n</think>\n< answer><|place_holder|><|place_holder |><|place_holder|><|place_holder|><| place_holder|><|place_holder|><| place_holder|><|place_holder|><| place_holder|><|place_holder|><| place_holder|><|place_holder|><| place_holder|><|place_holder|><| place_holder|><|place_holder|><| place_holder|><|place_holder|><| place_holder|><|place_holder|></answer >"}]}, {’actions’: array([[0. , 0. ], [0.40046561, 0.39716284], [0.39221381, 0.33593741], [0.39243497, 0.31284149], [0.38875668, 0.28942805], [0.38467048, 0.27311695], [0.38409407, 0.26829267], [0.38829151, 0.27437078], [0.3931127 , 0.28797924], [0.39968362, 0.29992925]])}</mark> 

### **8.3. Training Details** 

The training details of SFT and RL are illustrated below. 

#### **8.3.1. SFT** 

<mark>batch_size 8 gradient_accumulation_steps 2 learning_rate 5e-5 bf16 gradient_checkpointing true attn_implementation flash_attention_2 num_train_epochs 4 max_grad_norm 5 zero2 config: { "fp16": { "enabled": "auto", "loss_scale": 0, "loss_scale_window": 1000, "initial_scale_power": 16, "hysteresis": 2, "min_loss_scale": 1 }, "bf16": { "enabled": "auto" }, "optimizer": { "type": "AdamW", "params": { "lr": "auto", "betas": "auto", "eps": "auto", "weight_decay": "auto" } }, "zero_optimization": { "stage": 2, "offload_optimizer": { "device": "none", "pin_memory": true</mark> 

<mark>}</mark> 

<mark>},</mark> 

<mark>"allgather_partitions": true, "allgather_bucket_size": 2e8, "overlap_comm": false, "reduce_scatter": true, "reduce_bucket_size": 2e8, "contiguous_gradients": true }, "gradient_accumulation_steps": "auto", "gradient_clipping": "auto",</mark> 

<mark>"steps_per_print": 100,</mark> 

<mark>"train_batch_size": "auto", "train_micro_batch_size_per_gpu": "auto ", "wall_clock_breakdown": false</mark> 

<mark>"offload_param": { "device": "none", "pin_memory": true }, "overlap_comm": true, "contiguous_gradients": true, "sub_group_size": 1e9, "reduce_bucket_size": "auto", "stage3_prefetch_bucket_size": " auto",</mark> 

<mark>"stage3_param_persistence_threshold ": "auto",</mark> 

<mark>"stage3_max_live_parameters": 1e9, "stage3_max_reuse_distance": 1e9, "stage3_gather_16bit_weights</mark> 

<mark>_on_model_save": true },</mark> 

#### **8.3.2. RL** 

<mark>max_prompt_length 16384 max_completion_length 768 batch_size 8 gradient_accumulation_steps 2 learning_rate 1e-6 lr_scheduler_type "cosine" weight_decay 0.01 bf16 gradient_checkpointing true temporal true len_control true attn_implementation flash_attention_2 max_pixels 401408 num_train_epochs 1 beta 0.04 max_grad_norm num_generations 8 zero3 config: "fp16": { "enabled": "auto", "loss_scale": 0, "loss_scale_window": 1000, "initial_scale_power": 16, "hysteresis": 2, "min_loss_scale": 1 }, "bf16": { "enabled": "auto" }, "zero_optimization": { "stage": 3, "offload_optimizer": { "device": "none", "pin_memory": true },</mark> 

<mark>"gradient_accumulation_steps": "auto", "gradient_clipping": "auto", "steps_per_print": 100,</mark> 

<mark>"train_batch_size": "auto", "train_micro_batch_size_per_gpu": "auto ",</mark> 

<mark>"wall_clock_breakdown": false</mark> 

<mark>}</mark> 

### **8.4. Reward Function Implements** 

Our reward functions significantly influence the RL process. For trajectory reward function: 


normally, we can select hyper-parameters (1 in this function) to achieve an accurate reward. Some times we need change the 1 to large numbers such as 2. We can also replaced with another easy way: 


