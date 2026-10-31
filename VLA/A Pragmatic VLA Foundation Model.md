---
title: "A Pragmatic VLA Foundation Model"
date: "2026-01-26"
authors: "Wei Wu; Fan Lu; Yunnan Wang; Shuai Yang; Shi Liu; Fangjing Wang"
url: https://arxiv.org/abs/2601.18692
pdf: https://arxiv.org/pdf/2601.18692
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.18692)** / [論文ページ](https://arxiv.org/abs/2601.18692)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。



# **A Pragmatic VLA Foundation Model** 

Wei Wu<sup>_∗_</sup> , Fan Lu<sup>_∗_</sup> , Yunnan Wang<sup>_∗_</sup> , Shuai Yang<sup>_∗_</sup> , Shi Liu<sup>_∗_</sup> , Fangjing Wang<sup>_∗_</sup> , Qian Zhu, He Sun, Yong Wang, Shuailei Ma, Yiyu Ren, Kejia Zhang, Hui Yu, Jingmei Zhao, Shuai Zhou, Zhenqi Qiu, Houlong Xiong, Ziyu Wang, Zechen Wang, Ran Cheng, Yong-Lu Li, Yongtao Huang, Xing Zhu, Yujun Shen, Kecheng Zheng<sup>_†_</sup> 

> _∗_ Equal Contribution _†_ Project Lead 

Offering great potential in robotic manipulation, a capable Vision-Language-Action (VLA) foundation model is expected to faithfully generalize across tasks and platforms while ensuring cost efficiency ( _e.g._ , data and GPU hours required for adaptation). To this end, we develop LingBot-VLA with around 20,000 hours of real-world data from 9 popular dual-arm robot configurations. Through a systematic assessment on 4 robotic platforms, each completing 100 tasks with 130 post-training episodes per task, our model achieves clear superiority over competitors, showcasing its **_strong performance_** and **_broad generalizability_** . We have also built an **_efficient_** codebase, which delivers a throughput of 261 samples per second with an 8-GPU training setup, representing a 1 _._ 5 _∼_ 2 _._ 8 _×_ (depending on the relied VLM base model) speedup over existing VLA-oriented codebases. The above features ensure that our model is well-suited for real-world deployment. To advance the field of robot learning, we provide open access to the code, base model, and benchmark data, with a focus on enabling more challenging tasks and promoting sound evaluation standards. 

**Website:** https://technology.robbyant.com/lingbot-vla **Github:** https://github.com/robbyant/lingbot-vla **Checkpoints:** https://huggingface.co/collections/robbyant/lingbot-vla 


## **1 Introduction** 

Vision-Language-Action (VLA) foundation models [5, 6, 27] have emerged as a promising method for enabling robots to perform diverse manipulation tasks guided by natural language instructions. Through large-scale pre-training, these models acquire generalizable skills that can be rapidly adapted to diverse tasks and robotic platforms. Despite the significant progress, there remains a lack of comprehensive empirical studies on how real-robot performance scales with increasingly vast pre-training datasets. Moreover, the community lacks a highly optimized training codebase capable of efficiently conducting these scaling evaluations on massive volumes of data. Consequently, a fundamental question that demands investigation in the real-world setting is: _How do VLA models truly scale with massive real-world robot data?_ 

Understanding the scaling behavior of VLA models is crucial for robotic learning, especially on vast and diverse real-world datasets. In this work, we provide a systematic empirical investigation into how success rates scale with respect to data volume and diversity during VLA pre-training By scaling pre-training data from 3,000 hours to 20,000 hours, we demonstrate that downstream success rates improve consistently and substantially. Notably, this scaling behavior shows no signs of saturation even at the 20,000-hour mark, suggesting that VLA performance continues to benefit from increased data volume. These results provide the first empirical evidence of favorable scaling properties in real-world robot learning, offering critical insights for future VLA development and large-scale data curation. 

While scaling analysis reveals favorable performance trends, translating these insights into reliable, deployable systems necessitates rigorous evaluation on real robotic platforms at a large scale. Thanks to GM-100 [29], which provides 100 carefully designed tasks, we conduct a systematic assessment across 4 robotic platforms, involving 130 episodes per task per embodiment. By emphasizing task diversity and multi-platform consistency, our evaluation framework provides a choice of new standards for sound VLA benchmarking. 

1 


**Figure 1. Overview** of LingBot-VLA. We scale dual-arm robot data collected in the real world for pre-training. LingBot-VLA can be easily and efficiently transferred to downstream tasks. Moreover, we conduct a systematic assessment across three robotic embodiments, which demonstrates the clear superiority of our model. 

In this paper, we present LingBot-VLA, a pragmatic VLA foundation model trained on about 20,000 hours of real-world manipulation data from 9 robotic platforms. Our systematic evaluation on the comprehensive benchmark, demonstrates that LingBot-VLA achieves state-of-the-art performance and exceptional generalization compared to existing methods. Beyond model capabilities, we emphasize that large-scale robot learning necessitates high computational efficiency. To this end, we have developed an optimized codebase that achieves a throughput of 261 samples per second on an 8-GPU cluster. This efficiency gain substantially shortens training cycles and reduces computational overhead, thereby lowering the overall costs. By combining superior performance, broad generalizability, and computational efficiency, LingBot-VLA is well-positioned for real-world robotic applications. To foster community progress, we provide open access to the code, base model, and benchmark data, with a focus on enabling more challenging tasks and promoting sound evaluation standards. 

## **2 Related Work** 

### **2.1 Vision-Language-Action Models** 

**Foundation VLA.** Vision-language-action foundation models typically adopt a powerful pre-trained vision-language model [2, 3] as the semantic backbone, coupled with diffusion-based action head. Recent VLA foundation models [4– 7, 13, 26, 27, 32, 33] have demonstrated enhanced multi-task execution capabilities and superior multi-embodiment adaptability, following pre-training on larger-scale and increasingly diverse datasets. Distinguishing itself from the datasets utilized in preceding VLA foundation models, our model is pre-trained on an extensive corpus approximate 20,000 hours of multi-embodiment data. This massive-scale dataset, characterized by its high behavioral diversity, significantly bolsters the model’s generalization capabilities across various robotic manipulation tasks. 

2 

**Spatial VLA.** While traditional VLA models excel at semantic understanding, they often struggle with precise geometric reasoning and depth perception required for complex spatial manipulation. To address this, several works [9, 11, 14, 21, 23, 25, 32] have integrated spatial representations into the VLA framework. Several research [9, 26, 32] initiatives have focused on bolstering the spatial awareness of VLMs within embodied scenarios to enhance the spatial manipulation capabilities of VLAs in downstream tasks. Others explicitly or implicitly incorporate depth information during the VLA training phase. Spatial Forcing [14] employs a streamlined alignment strategy that compels the integration of VLA visual embeddings with spatial representations, thereby significantly improving the model’s spatial comprehension. 

### **2.2 Evaluation on Robot Policy** 

Current evaluation methodologies for robot policies are primarily bifurcated into two categories: simulation-based [8, 15, 17, 19, 20] and real-world embodiment-based [1, 31]. Simulation-based benchmark provide a rapid and convenient means to evaluate the capabilities of policies, enabling large-scale parallel testing across vast and diverse interaction scenarios at very low cost. Although simulation environments typically employ idealized physical models, their results often do not fully represent the complexity of the real physical world. The another real-world evaluations’ efficiency is often bottlenecked by the requirement for extensive hardware parallelism. Consequently, the majority of prior VLA studies have been confined to comparing a limited number of methods across only a few tasks. To more comprehensively evaluate the real-world performance of policies, this work conducts an assessment across three distinct robotic platforms, with 100 tasks executed on each platform. We further provide a thorough analysis of how mainstream VLA models adapt to the diversity encountered in real-world scenarios. 

### **2.3 Efficient VLA Training** 

The rapid iteration of VLA models has catalyzed the development of specialized training infrastructure. Several well-designed open-source codebases have recently emerged in the community, each catering to different research priorities. For instance, the OpenPI [6] repository provides a versatile framework supporting both JAX and PyTorch for training the _π_ series models. StarVLA [22] introduces a modular and user-friendly codebase specifically optimized for the co-training of VLAs and VLMs, facilitating the transfer of semantic knowledge to robotic control. Additionally, Dexbotic [30] is designed as a unified and efficient solution to streamline the development lifecycle of VLAs, focusing on standardizing the pipeline from data ingestion to model deployment. Despite these advancements, training large-scale VLA models on multi-node clusters remains a significant challenge due to data I/O bottlenecks and communication overheads. To bridge this gap, we present LingBot-VLA, a high-performance open-source codebase engineered for large-scale VLA training. Unlike existing frameworks, our codebase implements systemic optimizations in data loading, distributed training strategies, and operator-level acceleration. These enhancements lead to a comprehensive improvement in training throughput and scalability, providing a more efficient foundation for the community to explore the scaling limits of robotic foundation models. 

## **3 Pre-training Dataset** 

### **3.1 Data Collection** 

The pre-training dataset is built upon large-scale teleoperated data collected from 9 popular dual-arm robot embodiments, as shown in Fig. 2. We discuss these embodiments below: 

- **AgiBot G1.** This setup has two 7-DoF arms with three RGB-D cameras. Robot data are collected via VR-based teleoperation on this setup. 

- **AgileX.** This setup is equipped with three cameras and two 6-DoF arms. Robot control is achieved using isomorphic arms during the data collection process. 

- **Galaxea R1Lite.** This setup has two 6-DoF arms, with one stereo camera and two wrist cameras. 

- **Galaxea R1Pro.** Two 7-DoF arms, one stereo camera, and two wrist cameras are used in this setup. 

- **Realman Rs-02.** This setup uses three cameras and features a 16-dimensional configuration and action space: two 7-DoF arms and two parallel grippers. 

3 


**Figure 2. Visualization of pre-training dataset** used by LingBot-VLA. 

- **Leju KUAVO 4 Pro.** A bipedal humanoid robot featuring two 7-DoF arms, two parallel grippers, one headmounted camera, and two wrist-mounted cameras. 

- **Qinglong.** A humanoid robot with two 7-DoF arms and three cameras: one on the head and one on each wrist. 

- **ARX Lift2.** This setup uses three cameras and two 6-DoF arms. 

- **Bimanual Franka.** This setup uses two 7-DoF arms and two parallel grippers, forming a 16-dimensional action space, with three cameras. 

### **3.2 Data Labeling** 

To obtain precise language instructions, we perform the following annotations: (1) _Video Segment_ . Videos from multiple viewpoints, captured by robots, are jointly decomposed into clips by human annotators according to predefined atomic actions. Besides, to reduce the redundant information within videos, static frames at the start and end of the videos are eliminated at this stage. (2) _Instruction Annotation_ . After obtaining videos containing the robots’ full motion trajectories and video clips for each atomic action, we employ Qwen3-VL-235B-A22B [2] for precise annotation of task and sub-task instructions, as shown in Fig. 1. 

## **4 Model Training** 

### **4.1 Architecture** 

To leverage well-trained vision-language representations, LingBot-VLA integrates the pre-trained VLM ( _i.e._ , Qwen2.5VL [2]) with an initialized action generation module called ‘action expert’. These components are organized via a Mixture-of-Transformers (MoT) architecture like BAGEL [10], where vision-language and action modalities are processed through distinct transformer pathways, coupled by a shared self-attention mechanism for layer-wise unified sequence modeling. This MoT framework ensures that high-dimensional semantic priors from the VLM provide continuous guidance across all layers, while simultaneously mitigating cross-modal interference by maintaining modality-specific processing. The architecture of LingBot-VLA is illustrated in Fig. 1. Multi-view operational images and the related task instruction are uniformly encoded through a VLM to establish multimodal conditioning for subsequent action generation. Concurrently, the robot’s proprioceptive sequences, specifically initial states and action chunks, are fed into the action expert for the prediction of action generation. We employ Flow Matching [16] for continuous action modeling, which facilitates fluid and smooth robotic control, ensuring high-precision execution across complex tasks and diverse robots. 

4 

In LingBot-VLA, the VLM and the action expert interact through a shared self-attention mechanism, facilitating a unified layer-wise representation. Consequently, the joint modeling sequence at timestamp _t_ is formulated as the concatenation of the observation conditions **O** _t_ and the action chunk **A** _t_ . Specifically, the observation context is defined as: 


which incorporates tokens from three-view operational images **I**<sup>1</sup> _t_<sup>_,_2</sup><sup>_,_3</sup> of dual-arm robots, the task instruction **T** _t_ , and the robot state **s** _t_ . The corresponding action sequence is denoted as: 


where _T_ represents the action chunk length, _i.e._ , the temporal horizon of the predicted trajectory, which is set to 50 during our pre-training stage. Therefore, the training objective is to characterize the conditional distribution _p_ ( **A** _t|_ **O** _t_ ) through conditional flow matching. For a flow timestep _s ∈_ [0 _,_ 1], we define a probability path through linear interpolation between the Gaussian noise _ϵ ∼N_ ( **0** _,_ **I** ) and the ground-truth action **A** _t_ , obtaining the intermediate action **A** _t,s_ = _s_ **A** _t_ + (1 _− s_ ) _ϵ_ . The conditional distribution of **A** _t,s_ is formulated as: 


The action expert _vθ_ is trained to predict the conditional vector field by minimizing the Flow Matching objective: 


where the target velocity is given by the ideal vector field **A** _t − ϵ_ derived from the linear probability path. 

Following _π_ 0 [6], we implement blockwise causal attention for modeling the joint sequence [ **O** _t,_ **A** _t_ ]. The sequence can be partitioned into three distinct functional blocks: [ **I**<sup>1</sup> _t_<sup>_,_</sup><sup>**I**2</sup> _t_<sup>_,_</sup><sup>**I**3</sup> _t_<sup>_,_</sup><sup>**T**</sup><sup>_t_], [</sup><sup>**s**</sup><sup>_t_] and [</sup><sup>**a**</sup><sup>_t,_</sup><sup>**a**</sup><sup>_t_+1</sup><sup>_, . . . ,_</sup><sup>**a**</sup><sup>_t_+</sup><sup>_T −_1].A causal mask</sup> is applied among these blocks, such that tokens in each block can only attend to themselves and those in preceding blocks. Conversely, all tokens within the same block employ bidirectional attention and can attend to each other. This configuration ensures that the action expert can leverage all available observation knowledge, while preventing information leakage from future action tokens into the current observation representations. 

To explicitly capture spatial awareness within manipulation environments and further enhance the robot’s execution robustness, we adopt a vision distillation approach inspired by recent works [12, 28]. Specifically, we apply the learnable queries [ **Q**<sup>1</sup> _t_<sup>_,_</sup><sup>**Q**2</sup> _t_<sup>_,_</sup><sup>**Q**3</sup> _t_<sup>] corresponding to three-view operational images.To integrate depth information, these queries are</sup> processed by VLM and then aligned with the depth tokens [ **D**<sup>1</sup> _t_<sup>_,_</sup><sup>**D**2</sup> _t_<sup>_,_</sup><sup>**D**3</sup> _t_<sup>] from LingBot-Depth [24].We align the VLM</sup> learnable queries and LingBot-Depth tokens by minimizing the distillation loss _Ldistill_ : 


where Proj( _·_ ) is a projection layer that applies cross-attention for dimensional alignment. This integration infuses geometric information into the LingBot-VLA model, enabling precise perception for complex manipulation tasks. 

### **4.2 Training Efficiency Optimization** 

Given that action data is inherently high-frequency, establishing a highly efficient pipeline encompassing distributed training and operator optimization is imperative. Our optimization methodology is structured as follows: 

**Distributed Strategy:** While VLA models typically possess a moderate parameter count, achieving an optimal trade-off between GPU memory occupancy and training throughput remains essential. We employ Fully Sharded Data Parallel (FSDP)—a highly efficient PyTorch implementation of the Zero Redundancy Optimizer (ZeRO)—to shard optimizer states, model parameters, and gradients, thereby minimizing memory footprint. Drawing inspiration from the Hybrid Sharded Data Parallel (HSDP) approach proposed in VeOmni [18], we construct specific “shard groups” exclusively for the action expert modules. This strategy effectively mitigates the communication overhead associated with excessive parameter sharding. Additionally, we implement a mixed-precision policy: performing reductions in torch.float32 to ensure numerical stability, while utilizing torch.bfloat16 for storage and communication. 

**Operator-Level Optimization:** The multimodal fusion of vision, language, and action within our architecture is fundamentally a sparse attention process. To address this, we leverage FlexAttention to optimize computation. Furthermore, we apply operator fusion (via torch.compile) to reduce kernel launch overhead and maximize memory bandwidth utilization. 

5 


**Figure 3. Word cloud of atomic actions** in (a) Pre-training datasets and (b) Benchmark. 

## **5 Experiments** 

### **5.1 Large-scale Real-world Benchmark** 

We conduct a large-scale empirical evaluation of LingBot-VLA designed to rigorously assess multi-embodiment generalization and real-world robustness. Our experimental framework comprises three core components: (1) 25 physical robots spanning 4 distinct commercial platforms, (2) GM-100 [29] benchmark featuring 100 diverse manipulation tasks with 39,000 expert demonstrations and (3) a controlled evaluation protocol generating 22,500 trials comparing LingBot-VLA against three state-of-the-art baselines under identical training and testing conditions. 

#### **5.1.1 Hardware Platforms** 

We conduct experiments across 4 distinct robotic platforms: AgileX, Agibot G1 Galaxea R1Pro and Leju KUAVO 4 Pro. All three embodiments feature a dual-arm configuration equipped with parallel-jaw grippers. To ensure robust perception, each robot is outfitted with multiple cameras: two wrist-mounted cameras and a head-mounted camera to capture an egocentric, human-eye perspective. All tasks are tabletop-based, with the embodiment’s chassis and waist securely fixed in place. 

#### **5.1.2 Data Collection and Processing** 

For each GM-100 task [29], we collect expert demonstrations via teleoperation following a standardized protocol designed to ensure high data quality and environmental diversity. _Trajectory Volume:_ 150 raw trajectories are collected per task across three platforms. The top 130, ranked by execution quality (task completion, motion smoothness, and protocol adherence), are retained for training. All trajectories strictly follow GM-100 task specifications. _Standardized Objects:_ task objects are standardized and sourced according to GM-100 material specifications to ensure reproducibility across sites. _Environmental Diversity:_ object poses (positions and orientations) are randomized within the workspace for each trajectory to prevent overfitting to specific spatial configurations and encourage learning of task-relevant invariances. _Teleoperation Guidelines:_ (1) maintaining clearance between the end-effector and workspace surfaces to avoid collisions, (2) reducing velocity during object contact phases for smooth manipulation, and (3) ensuring distinct image observations at episode start and termination for reliable policy training. _Automated Filtering:_ an algorithmic screening procedure automatically excludes episodes exhibiting technical anomalies. _Manual Review:_ human reviewers validate the filtered dataset using synchronized multi-view video streams. Episodes are removed if they include extraneous objects or deviate from task protocols. 

To analyze the semantic distribution and diversity of action categories, we visualized the most prevalent atomic actions in the training and testing sets using word clouds, as shown in Figs. 3a and 3b. Quantitative analysis reveals that approximately 50% of the atomic actions in the test set are absent from the top 100 most frequent training actions. This significant discrepancy underscores the diversity of our test set and ensures a rigorous assessment of the model’s generalization capabilities. 

6 

**Table 1. Experiment results of real-world evaluation** on GM-100 [29] benchmark. ‘SR’ refers to success rate, and ‘PS’ refers to progress score. 

|**Platform**|WAL<br>**SR**|L-OSS<br>**PS**|GR00<br>**SR**|T N1.6<br>**PS**|_π_0<br>**SR**|_._5<br>**PS**|Ours_w/_<br>**SR**|_o_depth<br>**PS**|Ours_w_<br>**SR**|_/_ depth<br>**PS**|
|---|---|---|---|---|---|---|---|---|---|---|
|Agibot G1 (Wheeled)|2.99%|8.75%|5.23%|12.63%|7.77%|21.98%|**12.82%**|30.04%|11.98%|**30.47%**|
|AgileX (Wheeled)|2.26%|8.16%|3.26%|10.52%|17.20%|34.82%|15.50%|36.31%|**18.93%**|**40.36%**|
|Galaxea R1Pro (Wheeled)|6.89%|14.13%|14.29%|24.83%|14.10%|26.14%|18.89%|34.71%|**20.98%**|**35.40%**|
|Leju KUAVO 4 Pro (Bipedal)|3.26%|11.75%|6.45%|18.66%|12.91%|26.35%|**17.59%**|**36.22%**|15.60%|34.40%|
|**Average**|3.85%|10.70%|7.31%|16.66%|13.00%|27.32%|16.20%|34.32%|**16.87**%|**35.16**%|


**Table 2. Experiment results of simulation evaluation** on RoboTwin 2.0 [8] benchmark. 

||**(a).**|Clean Scenes|||**(b).** Ra|ndomized Scenes||
|---|---|---|---|---|---|---|---|
||_π_0_._5|Ours_w/o_depth|Ours_w/_ depth||_π_0_._5|Ours_w/o_depth|Ours_w/_ depth|
|**Average SR**|82.74%|86.50%|**88.56%**|**Average SR**|76.76%|85.34%|**86.68%**|


#### **5.1.3 Benchmarking and Evaluation Protocol** 

We systematically compare LingBot-VLA with three state-of-the-art VLA models: _π_ 0 _._ 5, GR00T N1.6, and WALLOSS, under strict experimental controls to isolate architectural performance. _Standardized Training:_ All models are fine-tuned from publicly available pre-trained checkpoints using the same post-training pipeline. The verified dataset (130 filtered trajectories per task) and consistent hyperparameters ( _i.e._ , batch sizes=256, epochs=20) are applied to ensure fair comparisons. _Strict Machine-Task Pairing:_ To eliminate hardware-induced variance, evaluations are conducted on the exact robot units used during data collection. All models are tested sequentially on the same hardware-task pair in randomized order. For example, in the “Stack Bowls” task, all models are evaluated on the same unit across AgileX, Agibot G1, and Galaxea R1pro platforms. _Controlled Evaluation Setup:_ Testing conditions follow standardized protocols, mirroring data collection procedures with randomized object positions and orientations while maintaining consistent task specifications. This ensures evaluation of generalization rather than memorization. _Inference and Recording:_ Each model undergoes 15 trials per task-robot pair for statistical robustness. Evaluation environments are kept constant, and comprehensive data ( _e.g._ , third-person views, robot states, and model predictions) are recorded in rosbag format for transparency. These recordings will be open-sourced to establish verifiable benchmarks. 

#### **5.1.4 Evaluation Metrics** 

We evaluate model performance using two metrics capturing both task completion and partial progress. _Success Rate (SR):_ the proportion of trials where the model completes all task steps within a 3-minute time limit. This primary metric reflects the model’s real-world deployment viability. _Progress Score (PS):_ measures partial task completion by tracking progress through sequential subtask checkpoints: For example, in a 6-step “Stack Bowls” task, completing steps 1–4 but failing at step 5 results in a score of<sup><u>4</u></sup> 6<sup>_≈_0</sup><sup>_._67.This diagnostic metric highlights failure modes and rewards partial</sup> success. _Termination Criteria:_ A trial ends if: (1) three consecutive subtask failures occur, or (2) safety-critical events ( _e.g._ , collisions) arise. Progress is scored based on subtasks completed before termination. We report overall SR and PS across 100 tasks, and per-platform metrics stratified by robot type to assess cross-embodiment generalization. 

### **5.2 Comparison on Real-world Benchmark** 

As shown in Tab. 1, we compare our two LingBot-VLA variants with three strong baselines across three platforms. On all platforms, LingBot-VLA _w/o_ depth significantly outperforms WALL-OSS and GR00T N1.6 in both SR and PS metrics. By incorporating depth-based spatial information, LingBot-VLA _w/_ depth achieves an average SR improvement of 4 _._ 28% and a PS increase of 7 _._ 76% over _π_ 0 _._ 5 across the three embodiments. Notably, GR00T N1.6 performs average on the Agibot G1, AgileX and Leju KUAVO 4 Pro embodiment but achieves SR and PS comparable to _π_ 0 _._ 5 on the Galaxea R1Pro platform. This is due to the extensive inclusion of Galaxea R1Pro data during its pre-training, indicating that pre-training can significantly enhance performance on downstream tasks with high structural similarity. The complete and detailed test results can be found in the Appendix Tab. S1- S8. 

7 


**Figure 4. Training throughput analysis** of the (a) Qwen2.5-VL-3B- _π_ and (b) PaliGemma-3B-pt-224- _π_ models. 

### **5.3 Comparison on Simulation Benchmark** 

In Tab. 2, we evaluate simulation performance across 50 representative manipulation tasks within the RoboTwin 2.0 suite. Starting from pretrained checkpoints, each model was further finetuned on the RoboTwin dataset. To assess multi-task generalization, we train all models on 2 _,_ 500 demonstrations from clean scenes (50 per task) and 25 _,_ 000 from highly randomized scenes (500 per task). Randomization factors encompass varied backgrounds, table-top clutter, table-height perturbations, and diverse lighting conditions. Compared to the _π_ 0 _._ 5 baseline, LingBot-VLA demonstrates marked advancements in RoboTwin 2.0 multi-task settings. Specifically, LingBot-VLA _w/o_ depth yields absolute success rate increases of over 3 _._ 76% in clean environments and 8 _._ 58% in randomized scenarios. By employing learnable query-based alignment, the integration of depth information enables LingBot-VLA to effectively extract rich spatial priors from LingBot-Depth model. The approach surpasses the baseline model by absolute margins of 5 _._ 82% and 9 _._ 92% in clean and randomized configurations, respectively. Please refer to Tab. S9 of Appendix for detailed results. 

### **5.4 Training Throughput Analysis** 

To comprehensively evaluate the training efficiency of VLA models across different frameworks, we selected three opensource codebases ( _i.e.,_ StarVLA, Dexbotic, and OpenPI) as the baselines for comparison. To ensure a fair comparison, all experiments were conducted on the Libero dataset using a standardized _π_ -like model architecture. 

Given the variations in the VLM implementations across different codebases, we reproduced both Qwen2.5-VL-3B- _π_ and PaliGemma-3B-pt-224- _π_ models within our own codebase to facilitate a direct alignment and comparison with the baselines. Regarding the training configuration, the local batch size was standardized to 32 for all experiments. 

It is worth noting that while StarVLA and Dexbotic default to ZeRO for distributed training, our codebase employs the comparable FSDP2 strategy. In contrast, OpenPI utilizes DDP, which inherently incurs lower communication overhead. We adopted sample throughput (samples/s) as the primary evaluation metric. 

Figures 4a and 4b illustrate the training efficiency comparison between our codebase and the baselines for the Qwen2.5-VL-3B- _π_ and PaliGemma-3B-pt-224- _π_ models, respectively. The results demonstrate that our codebase achieved the fastest training speeds in both model settings. Furthermore, the figures detail the training throughput across configurations of 8, 16, 32, 128, and 256 GPUs, alongside the theoretical linear scaling limit. The data indicates that our solution not only delivers superior throughput but also exhibits excellent scaling efficiency that closely follows the theoretical limit as the number of GPUs increases. 

### **5.5 Ablation Studies** 

#### **5.5.1 Scaling Experiments** 

To assess the scaling laws of pre-training data, we conduct experiments on a subset of 25 representative tasks drawn from the benchmark. As shown in Figs. 5a and 5b, both the progress rate and success rate demonstrate a consistent upward trend as the pre-training data duration increases from 3,000 to 20,000 hours. This indicates that scaling up 

8 


**Figure 5. Scaling behavior across dataset size.** With increased data scale, our model exhibits scaling laws in terms of success rate and progress rate. 

real-world pre-training data contributes to improved generalization and performance across diverse downstream tasks and embodiments. Furthermore, the individual trends of the three embodiments ( _i.e.,_ Agibot G1, AgileX, and Galaxea R1Pro) generally align with the aggregated performance, suggesting the observed scaling law is robust and not specific to a single platform. These results validate the effectiveness of our scaling approach in enhancing the capabilities of the generalist policy. 

#### **5.5.2 Data-efficient Analysis** 

Following the large-scale real-world benchmarking protocols, we selected eight representative tasks from GM-100 dataset to conduct data-efficient post-training experiments on the Agibot G1 platform. As illustrated in Fig. 6, with a limited budget of only 80 demonstrations per task, LingBot-VLA outperforms _π_ 0 _._ 5 using the full 130demonstration set in both Progress Rate and Success Rate. Notably, the performance margin between LingBotVLA and _π_ 0 _._ 5 widens significantly as the volume of post-training data increases, demonstrating superior data efficiency and scalability. 


**Figure 6. Data efficiency** of LingBot-VLA post-training. 

## **6 Conclusion** 

We have introduced LingBot-VLA, a foundation model that achieves superior generalizability and training efficiency through large-scale real-world data and an optimized codebase. Our comprehensive evaluation across 100 tasks demonstrates that our model achieves clear superiority over competitors, showcasing its strong performance and broad generalizability. To foster open science, we release our code, model, and benchmark data. Future research will focus on scaling the model versatility by integrating single-arm and mobile robotic data, paving the way for more diverse and mobile manipulation capabilities in unconstrained environments. 

**Acknowledgment.** We thank Zhengyu He, Han Zhang, Yuhao Xie, Haidan Zhou, Chongjun Zhong, Yida Zou, Siyuan Li, Zhikun Luo, Yuanqi Chen, Yingying Zhang, Yijun Zheng, Wanting Xu, Hongfei Niu, Yan Zha, Ka Leong Cheng, Liping Zhang, Zhen Liu, Rundong Zhou, Yuan Guan, Haitao Wang, Weilun Yao, Zhiwei Liang, Jiahao Fan, Jingran Xu, Linyu Su, Haiwei Liang, Yixiang Gao, Yingmin Li, Yongqiang Wen, Jiafei Li, Yuanzhe Guo, Yijun Zheng, Fengrui Zhang, Lin Wang, Min Yao, Fei Lu, Jingyun Tian, Ting Huang, Xinyang Wang, Jianxue Qian, Wenhui Shi, Jie Ren, Lina Tao, Yongqiang Wu, Daohua Yan, Zhou Yang, Qiang Wang and Yao Su for help with data, evaluation experiments, training infrastructure, robot hardware and robot software. We also gratefully acknowledge Galaxea Team, AgileX Robotics, and Leju(Shenzhen) Robotics Technology Co., Ltd. for help with the data collection and benchmark. 

9 

## **References** 

- [1] Pranav Atreya, Karl Pertsch, Tony Lee, Moo Jin Kim, Arhan Jain, Artur Kuramshin, Clemens Eppner, Cyrus Neary, Edward Hu, Fabio Ramos, et al. Roboarena: Distributed real-world evaluation of generalist robot policies. _arXiv preprint arXiv:2506.18123_ , 2025. 

- [2] Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang, Shijie Wang, Jun Tang, et al. Qwen2.5-vl technical report. _arXiv preprint arXiv:2502.13923_ , 2025. 

- [3] Lucas Beyer, Andreas Steiner, André Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, et al. Paligemma: A versatile 3B VLM for transfer. _arXiv preprint arXiv:2407.07726_ , 2024. 

- [4] Johan Bjorck, Fernando Castañeda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. GR00T N1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- [5] Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Robert Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, Lachy Groom, Karol Hausman, brian ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, James Tanner, Quan Vuong, Homer Walke, Anna Walling, Haohuan Wang, Lili Yu, and Ury Zhilinsky. _π_ 0 _._ 5: A vision-language-action model with open-world generalization. In _Conference on Robot Learning_ , 2025. 

- [6] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _π_ 0: A vision-language-action flow model for general robot control. In _Proceedings of Robotics: Science and Systems_ , 2025. 

- [7] Chilam Cheang, Sijin Chen, Zhongren Cui, Yingdong Hu, Liqun Huang, Tao Kong, Hang Li, Yifeng Li, Yuxiao Liu, Xiao Ma, et al. GR-3 technical report. _arXiv preprint arXiv:2507.15493_ , 2025. 

- [8] Tianxing Chen, Zanxin Chen, Baijun Chen, Zijian Cai, Yibin Liu, Zixuan Li, Qiwei Liang, Xianliang Lin, Yiheng Ge, Zhenyu Gu, et al. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. _arXiv preprint arXiv:2506.18088_ , 2025. 

- [9] Xinyi Chen, Yilun Chen, Yanwei Fu, Ning Gao, Jiaya Jia, Weiyang Jin, Hao Li, Yao Mu, Jiangmiao Pang, Yu Qiao, et al. InternVLA-M1: A spatially guided vision-language-action framework for generalist robot policy. _arXiv preprint arXiv:2510.13778_ , 2025. 

- [10] Chaorui Deng, Deyao Zhu, Kunchang Li, Chenhui Gou, Feng Li, Zeyu Wang, Shu Zhong, Weihao Yu, Xiaonan Nie, Ziang Song, et al. Emerging properties in unified multimodal pretraining. _arXiv preprint arXiv:2505.14683_ , 2025. 

- [11] Heyu Guo, Shanmu Wang, Ruichun Ma, Shiqi Jiang, Yasaman Ghasempour, Omid Abari, Baining Guo, and Lili Qiu. OmniVLA: Physically-grounded multimodal vla with unified multi-sensor perception for robotic manipulation. _arXiv preprint arXiv:2511.01210_ , 2025. 

- [12] Xiaohu Huang, Jingjing Wu, Qunyi Xie, and Kai Han. MLLMs need 3D-aware representation supervision for scene understanding. _arXiv preprint arXiv:2506.01946_ , 2025. 

- [13] Tao Jiang, Tianyuan Yuan, Yicheng Liu, Chenhao Lu, Jianning Cui, Xiao Liu, Shuiqi Cheng, Jiyang Gao, Huazhe Xu, and Hang Zhao. Galaxea open-world dataset and G0 dual-system vla model. _arXiv preprint arXiv:2509.00576_ , 2025. 

- [14] Fuhao Li, Wenxuan Song, Han Zhao, Jingbo Wang, Pengxiang Ding, Donglin Wang, Long Zeng, and Haoang Li. Spatial forcing: Implicit spatial representation alignment for vision-language-action model. _arXiv preprint arXiv:2510.12276_ , 2025. 

- [15] Xuanlin Li, Kyle Hsu, Jiayuan Gu, Karl Pertsch, Oier Mees, Homer Rich Walke, Chuyuan Fu, Ishikaa Lunawat, Isabel Sieh, Sean Kirmani, et al. Evaluating real-world robot manipulation policies in simulation. _arXiv preprint arXiv:2405.05941_ , 2024. 

- [16] Yaron Lipman, Ricky TQ Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le. Flow matching for generative modeling. _arXiv preprint arXiv:2210.02747_ , 2022. 

- [17] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Adv. Neural Inform. Process. Syst._ , 36:44776–44791, 2023. 

10 

- [18] Qianli Ma, Yaowei Zheng, Zhelun Shi, Zhongkai Zhao, Bin Jia, Ziyue Huang, Zhiqi Lin, Youjie Li, Jiacheng Yang, Yanghua Peng, et al. Veomni: Scaling any modality model training with model-centric distributed recipe zoo. _arXiv preprint arXiv:2508.02317_ , 2025. 

- [19] Oier Mees, Lukas Hermann, Erick Rosete-Beas, and Wolfram Burgard. Calvin: A benchmark for language-conditioned policy learning for long-horizon robot manipulation tasks. _IEEE Robotics and Automation Letters_ , 7(3):7327–7334, 2022. 

- [20] Soroush Nasiriany, Abhiram Maddukuri, Lance Zhang, Adeet Parikh, Aaron Lo, Abhishek Joshi, Ajay Mandlekar, and Yuke Zhu. Robocasa: Large-scale simulation of everyday tasks for generalist robots. _arXiv preprint arXiv:2406.02523_ , 2024. 

- [21] Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, Bin Zhao, Dong Wang, et al. SpatialVLA: Exploring spatial representations for visual-language-action model. _arXiv preprint arXiv:2501.15830_ , 2025. 

- [22] starVLA Contributors. StarVLA: A lego-like codebase for vision-language-action model developing, 2025. 

- [23] Lin Sun, Bin Xie, Yingfei Liu, Hao Shi, Tiancai Wang, and Jiale Cao. GeoVLA: Empowering 3d representations in visionlanguage-action models. _arXiv preprint arXiv:2508.09071_ , 2025. 

- [24] Bin Tan, Changjian Sun, Xiage Qin, Hanat Adai, Zelin Fu, Tianxiang Zhou, Han Zhang, Yinghao Xu, Xing Zhu, Yujun Shen Shen, and Nan Xue. Masked depth modeling for spatial perception. https://technology.robbyant.com/lingbot-depth, 2026. 

- [25] Gemini Robotics Team, Abbas Abdolmaleki, Saminda Abeyruwan, Joshua Ainslie, Jean-Baptiste Alayrac, Montserrat Gonzalez Arenas, Ashwin Balakrishna, Nathan Batchelor, Alex Bewley, Jeff Bingham, et al. Gemini Robotics 1.5: Pushing the frontier of generalist robots with advanced embodied reasoning, thinking, and motion transfer. _arXiv preprint arXiv:2510.03342_ , 2025. 

- [26] Gemini Robotics Team, Saminda Abeyruwan, Joshua Ainslie, Jean-Baptiste Alayrac, Montserrat Gonzalez Arenas, Travis Armstrong, Ashwin Balakrishna, Robert Baruch, Maria Bauza, Michiel Blokzijl, et al. Gemini Robotics: Bringing AI into the physical world. _arXiv preprint arXiv:2503.20020_ , 2025. 

- [27] NVIDIA GEAR Team. GR00T N1.6: An improved open foundation model for generalist humanoid robots. https://research. nvidia.com/labs/gear/gr00t-n1_6/, 2025. 

- [28] Yunnan Wang, Fan Lu, Kecheng Zheng, Ziyuan Huang, Ziqiang Li, Wenjun Zeng, and Xin Jin. Vision-centric activation and coordination for multimodal large language models. _arXiv preprint arXiv:2510.14349_ , 2025. 

- [29] Ziyu Wang, Chenyuan Liu, Yushun Xiang, Runhao Zhang, Qingbo Hao, Hongliang Lu, Houyu Chen, Zhizhong Feng, Kaiyue Zheng, Dehao Ye, Xianchao Zeng, Xinyu Zhou, Boran Wen, Jiaxin Li, Mingyu Zhang, Kecheng Zheng, Qian Zhu, Ran Cheng, and Yong-Lu Li. The Great March 100: 100 detail-oriented tasks for evaluating embodied ai agents, 2026. 

- [30] Bin Xie, Erjin Zhou, Fan Jia, Hao Shi, Haoqiang Fan, Haowei Zhang, Hebei Li, Jianjian Sun, Jie Bin, Junwen Huang, et al. Dexbotic: Open-source vision-language-action toolbox. _arXiv preprint arXiv:2510.23511_ , 2025. 

- [31] Adina Yakefu, Bin Xie, Chongyang Xu, Enwen Zhang, Erjin Zhou, Fan Jia, Haitao Yang, Haoqiang Fan, Haowei Zhang, Hongyang Peng, et al. RoboChallenge: Large-scale real-robot evaluation of embodied policies. _arXiv preprint arXiv:2510.17950_ , 2025. 

- [32] Jianwei Yang, Reuben Tan, Qianhui Wu, Ruijie Zheng, Baolin Peng, Yongyuan Liang, Yu Gu, Mu Cai, Seonghyeon Ye, Joel Jang, et al. Magma: A foundation model for multimodal AI agents. In _IEEE Conf. Comput. Vis. Pattern Recog._ , pages 14203–14214, 2025. 

- [33] Andy Zhai, Brae Liu, Bruno Fang, Chalse Cai, Ellie Ma, Ethan Yin, Hao Wang, Hugo Zhou, James Wang, Lights Shi, et al. Igniting VLMs toward the embodied space. _arXiv preprint arXiv:2509.11766_ , 2025. 

## **Appendix** 

## **A Experiment** 

This section provides a comprehensive breakdown of the experimental results. Specifically, Table S1, Table S2, Table S3, Table S4, Table S5 and Table S6 below present the detailed performance on GM-100 real-world benchmark. Table S9 presents the detailed performance on Robotwin 2.0 benchmark. These tables serve as the basis for the aggregated mean results reported in the main text (see Sec. 5.2 and Sec. 5.3). 

11 

**Table S1. Real-world evaluation** on GM-100 [29] benchmark ( **Wheeled Humanoid Robot** : AgileX, Part I). 

||WAL|L-OSS|GR00|T N1.6|_π_|0_._5|Ours_w_|_/o_depth|Ours_w_|_/_ depth|
|---|---|---|---|---|---|---|---|---|---|---|
|**Tasks**|**SR**|**PS**|**SR**|**PS**|**SR**|**PS**|**SR**|**PS**|**SR**|**PS**|
|_#001_|7%|17%|20%|23%|53%|57%|40%|67%|47%|73%|
|_#002_|0%|3%|0%|0%|0%|23%|0%|15%|0%|2%|
|_#003_|0%|1%|0%|0%|20%|53%|7%|42%|0%|19%|
|_#006_<br>|0%<br>|3%<br>|0%<br>|0%<br>|0%<br>|20%<br>|0%<br>|0%<br>|0%<br>|17%<br>|
|_#007_|0%|16%|0%|7%|0%|41%|20%|61%|27%|70%|
|_#008_<br>|0%<br>|8%<br>|0%<br>|0%<br>|0%<br>|1%<br>|0%<br>|39%<br>|0%<br>|66%<br>|
|_#009_|0%|20%|27%|47%|0%|0%|13%|33%|47%|73%|
|_#010_|0%|2%|0%|0%|0%|0%|13%|13%|7%|13%|
|_#011_|0%|15%|7%|7%|53%|77%|7%|67%|20%|67%|
|_#012_|0%|0%|0%|0%|0%|0%|7%|45%|33%|59%|
|_#013_|0%|0%|0%|0%|0%|15%|0%|0%|7%|20%|
|_#014_|0%|3%|0%|5%|0%|2%|0%|40%|0%|54%|
|_#015_|53%|53%|67%|67%|40%|40%|80%|80%|100%|100%|
|_#016_|0%|0%|7%|15%|7%|18%|0%|7%|0%|27%|
|_#017_|7%|11%|20%|63%|53%|75%|27%|71%|0%|60%|
|_#018_|0%|0%|0%|3%|0%|2%|0%|0%|0%|20%|
|_#019_|0%|12%|0%|0%|13%|57%|0%|55%|7%|35%|
|_#020_|0%|3%|0%|0%|0%|27%|7%|37%|0%|32%|
|_#021_|0%|12%|0%|5%|7%|25%|0%|27%|0%|23%|
|_#022_|0%|0%|0%|1%|0%|26%|0%|59%|7%|63%|
|_#023_|0%|3%|0%|0%|0%|3%|0%|22%|0%|12%|
|_#024_|0%|0%|0%|4%|0%|15%|0%|9%|0%|10%|
|_#025_|0%|0%|0%|0%|0%|5%|0%|0%|0%|0%|
|_#026_|0%|0%|0%|0%|0%|4%|0%|0%|0%|0%|
|_#027_|0%|0%|0%|3%|53%|68%|20%|59%|20%|59%|
|_#028_|0%|0%|0%|3%|27%|60%|40%|43%|0%|8%|
|_#029_|0%|15%|7%|15%|47%|67%|0%|43%|13%|44%|
|_#030_|0%|0%|53%|53%|60%|62%|67%|87%|53%|78%|
|_#031_|0%|0%|0%|2%|27%|35%|0%|3%|0%|5%|
|_#032_|0%|13%|0%|24%|0%|0%|20%|33%|0%|27%|
|_#033_|0%|0%|0%|24%|0%|53%|0%|31%|0%|27%|
|_#034_|0%|0%|0%|7%|87%|96%|67%|84%|53%|85%|
|_#035_|0%|0%|0%|0%|0%|0%|0%|7%|60%|60%|
|_#036_|0%|11%|0%|9%|13%|75%|0%|51%|0%|51%|
|_#037_|0%|1%|0%|3%|7%|16%|0%|6%|0%|8%|
|_#038_|0%|0%|0%|0%|0%|10%|0%|1%|0%|6%|
|_#040_|0%|14%|0%|0%|80%|96%|80%|91%|93%|98%|
|_#041_|0%|0%|0%|2%|0%|8%|0%|2%|0%|0%|
|_#042_|0%|2%|0%|0%|40%|65%|7%|22%|0%|22%|
|_#043_|0%|18%|0%|22%|7%|58%|27%|78%|33%|78%|
|_#044_|0%|0%|0%|0%|0%|14%|0%|5%|0%|3%|
|_#045_|0%|0%|0%|3%|0%|22%|0%|11%|0%|23%|
|_#046_|0%|0%|0%|5%|13%|29%|7%|60%|73%|89%|
|_#047_|0%|6%|0%|19%|7%|40%|7%|59%|7%|37%|
|_#048_|0%|7%|0%|9%|7%|39%|7%|63%|0%|52%|
|_#049_|0%|0%|0%|5%|0%|18%|0%|22%|0%|23%|
|_#050_|0%|3%|0%|4%|0%|25%|0%|15%|0%|33%|
|_#051_|0%|0%|0%|2%|0%|2%|0%|40%|0%|58%|
|_#053_|0%|16%|0%|13%|7%|60%|0%|48%|13%|20%|
|_#054_|0%|3%|0%|3%|0%|33%|7%|20%|20%|43%|
|_#055_|0%|0%|0%|3%|0%|13%|0%|5%|0%|0%|


12 

**Table S2. Real-world evaluation** on GM-100 [29] benchmark ( **Wheeled Humanoid Robot** : AgileX, Part II). 

||WAL|L-OSS|GR00|T N1.6|_π_|0_._5|Ours_w_|_/o_depth|Ours_w_|_/_ depth|
|---|---|---|---|---|---|---|---|---|---|---|
|**Tasks**|**SR**|**PS**|**SR**|**PS**|**SR**|**PS**|**SR**|**PS**|**SR**|**PS**|
|_#056_|0%|28%|0%|7%|67%|88%|73%|93%|80%|92%|
|_#057_|0%|2%|0%|1%|0%|13%|0%|19%|0%|27%|
|_#058_|0%|37%|7%|44%|7%|58%|7%|63%|20%|72%|
|_#060_|0%|8%|20%|42%|93%|93%|27%|57%|13%|50%|
|_#061_|53%|77%|7%|33%|47%|68%|93%|97%|93%|97%|
|_#062_|0%|2%|0%|0%|0%|8%|0%|4%|0%|1%|
|_#063_|0%|0%|7%|7%|13%|50%|0%|0%|0%|0%|
|_#064_|0%|0%|0%|2%|0%|5%|0%|0%|0%|5%|
|_#065_|0%|22%|0%|12%|0%|23%|33%|55%|20%|62%|
|_#066_|0%|7%|0%|3%|7%|45%|13%|55%|0%|43%|
|_#067_|0%|0%|0%|2%|0%|28%|7%|20%|0%|27%|
|_#068_|7%|27%|0%|0%|47%|53%|20%|30%|60%|63%|
|_#069_|0%|2%|0%|10%|7%|8%|0%|17%|0%|12%|
|_#070_|0%|0%|0%|0%|0%|0%|0%|3%|7%|7%|
|_#071_|0%|3%|0%|5%|0%|5%|0%|0%|0%|5%|
|_#072_|0%|0%|0%|0%|7%|27%|0%|9%|13%|38%|
|_#073_|0%|0%|0%|55%|0%|0%|27%|57%|13%|23%|
|_#074_|0%|0%|0%|3%|0%|19%|0%|22%|0%|21%|
|_#075_|7%|9%|0%|13%|0%|20%|0%|4%|13%|56%|
|_#076_|0%|27%|7%|43%|7%|33%|7%|53%|33%|67%|
|_#077_|7%|7%|7%|7%|0%|2%|47%|47%|40%|42%|
|_#078_|0%|0%|0%|0%|80%|83%|87%|87%|73%|77%|
|_#079_|0%|15%|0%|20%|27%|49%|47%|73%|33%|80%|
|_#080_|0%|0%|0%|0%|0%|0%|0%|7%|0%|10%|
|_#081_|0%|8%|0%|3%|0%|15%|0%|26%|13%|50%|
|_#082_|0%|23%|0%|15%|20%|57%|20%|67%|27%|43%|
|_#083_|0%|20%|0%|0%|7%|50%|7%|28%|53%|77%|
|_#084_|0%|0%|0%|16%|0%|2%|40%|58%|33%|62%|
|_#085_|0%|9%|13%|40%|67%|85%|13%|36%|27%|42%|
|_#086_|0%|0%|0%|10%|60%|70%|100%|100%|60%|73%|
|_#087_|0%|3%|0%|0%|13%|15%|20%|72%|60%|78%|
|_#088_|0%|0%|0%|5%|13%|42%|20%|55%|7%|40%|
|_#089_|0%|2%|0%|22%|20%|47%|0%|28%|13%|41%|
|_#090_|0%|1%|0%|1%|0%|43%|0%|19%|0%|24%|
|_#091_|13%|37%|13%|25%|33%|77%|33%|42%|7%|17%|
|_#092_|47%|55%|0%|17%|67%|82%|60%|68%|93%|97%|
|_#093_|13%|14%|27%|27%|87%|87%|27%|27%|87%|87%|
|_#094_|0%|0%|0%|0%|0%|20%|7%|23%|0%|12%|
|_#095_|0%|2%|0%|18%|20%|44%|20%|38%|13%|39%|
|_#096_|7%|7%|0%|3%|7%|13%|0%|0%|13%|17%|
|_#097_|0%|4%|0%|0%|0%|4%|27%|44%|7%|24%|
|_#098_|0%|0%|0%|0%|0%|0%|0%|15%|7%|15%|
|_#099_|0%|0%|0%|3%|0%|12%|0%|0%|0%|0%|
|_#100_|0%|2%|13%|18%|27%|42%|0%|31%|13%|27%|
|_#102_|0%|2%|0%|13%|13%|29%|0%|33%|27%|60%|
|_#103_|7%|43%|0%|27%|80%|90%|73%|77%|47%|60%|
|_#104_|0%|15%|0%|7%|13%|31%|7%|40%|20%|53%|
|_#105_|0%|3%|0%|0%|0%|23%|0%|15%|0%|20%|
|_#106_|0%|1%|0%|4%|0%|36%|0%|13%|7%|31%|
|_#107_|0%|9%|0%|0%|53%|73%|27%|62%|27%|58%|


13 

**Table S3. Real-world evaluation** on GM-100 [29] benchmark ( **Wheeled Humanoid Robot** : AgibotG1, Part I). 

||WAL|L-OSS|GR00|T N1.6|_π_|0_._5|Ours_w_|_/o_depth|Ours_w_|_/_ depth|
|---|---|---|---|---|---|---|---|---|---|---|
|**Tasks**|**SR**|**PS**|**SR**|**PS**|**SR**|**PS**|**SR**|**PS**|**SR**|**PS**|
|_#001_|7%|20%|0%|0%|0%|23%|0%|3%|0%|17%|
|_#002_|0%|0%|0%|0%|13%|35%|0%|0%|0%|5%|
|_#003_|0%|3%|0%|3%|0%|35%|7%|19%|0%|0%|
|_#006_|0%|0%|0%|0%|0%|0%|0%|0%|0%|0%|
|_#007_|0%|0%|0%|18%|7%|44%|0%|25%|13%|52%|
|_#008_|0%|0%|0%|10%|0%|7%|0%|2%|0%|0%|
|_#009_|0%|41%|0%|30%|0%|33%|13%|57%|7%|47%|
|_#010_|0%|0%|0%|10%|0%|11%|7%|44%|7%|18%|
|_#011_|0%|0%|7%|23%|20%|43%|53%|88%|0%|43%|
|_#012_|0%|0%|0%|0%|7%|28%|13%|22%|13%|37%|
|_#013_|0%|0%|20%|69%|20%|71%|33%|71%|0%|45%|
|_#014_|0%|0%|0%|0%|0%|0%|0%|5%|0%|0%|
|_#015_|80%|80%|100%|100%|93%|93%|100%|100%|93%|93%|
|_#016_|0%|0%|0%|0%|0%|20%|0%|3%|0%|2%|
|_#017_|0%|0%|0%|3%|27%|45%|0%|51%|0%|55%|
|_#018_|0%|3%|0%|0%|0%|8%|7%|67%|33%|72%|
|_#019_|0%|8%|0%|12%|0%|5%|0%|20%|0%|0%|
|_#020_|0%|0%|0%|0%|0%|10%|13%|37%|33%|47%|
|_#021_|33%|54%|0%|3%|0%|17%|13%|63%|60%|87%|
|_#022_|0%|7%|0%|1%|0%|13%|0%|12%|0%|9%|
|_#023_|0%|2%|0%|3%|0%|10%|0%|3%|0%|35%|
|_#024_|0%|0%|0%|23%|7%|18%|0%|9%|0%|29%|
|_#025_|7%|12%|0%|0%|0%|2%|0%|5%|13%|18%|
|_#026_|0%|0%|0%|0%|0%|2%|0%|0%|0%|7%|
|_#027_|0%|0%|0%|5%|0%|24%|27%|65%|47%|68%|
|_#028_|0%|5%|0%|0%|0%|43%|67%|77%|60%|78%|
|_#029_|0%|0%|0%|1%|0%|17%|7%|19%|7%|19%|
|_#030_|0%|0%|0%|0%|47%|47%|73%|78%|27%|76%|
|_#031_|0%|3%|0%|14%|0%|12%|7%|7%|0%|7%|
|_#032_|0%|0%|0%|0%|0%|7%|27%|44%|7%|27%|
|_#033_|0%|2%|0%|20%|0%|16%|0%|31%|7%|42%|
|_#034_|7%|7%|13%|50%|13%|45%|0%|42%|20%|67%|
|_#035_|0%|0%|0%|1%|0%|20%|0%|24%|7%|44%|
|_#036_|0%|1%|0%|5%|0%|11%|0%|2%|0%|5%|
|_#037_|0%|0%|0%|0%|0%|17%|0%|8%|0%|0%|
|_#038_|0%|4%|0%|5%|13%|34%|0%|10%|0%|4%|
|_#040_|0%|6%|0%|0%|0%|24%|40%|66%|47%|64%|
|_#041_|0%|0%|0%|5%|0%|0%|0%|0%|0%|3%|
|_#042_|0%|0%|0%|0%|47%|49%|0%|0%|0%|40%|
|_#043_|0%|2%|0%|23%|0%|13%|0%|35%|13%|52%|
|_#044_|0%|0%|0%|0%|7%|7%|0%|2%|0%|0%|
|_#045_|0%|0%|0%|0%|0%|0%|0%|3%|0%|15%|
|_#046_|0%|0%|0%|9%|7%|35%|47%|73%|27%|42%|
|_#047_|7%|30%|0%|0%|0%|5%|0%|7%|7%|23%|
|_#048_|0%|1%|0%|0%|0%|3%|0%|0%|0%|11%|
|_#049_|0%|0%|0%|0%|0%|0%|0%|0%|0%|3%|
|_#050_|0%|2%|0%|0%|0%|5%|0%|10%|0%|8%|
|_#051_|0%|0%|0%|0%|0%|0%|0%|0%|0%|0%|
|_#053_|0%|4%|0%|5%|0%|19%|0%|36%|13%|62%|
|_#054_|0%|0%|7%|10%|0%|3%|0%|3%|7%|17%|
|_#055_|0%|0%|0%|0%|0%|0%|0%|0%|0%|0%|


14 

**Table S4. Real-world evaluation** on GM-100 [29] benchmark ( **Wheeled Humanoid Robot** : AgibotG1, Part II). 

||WAL|L-OSS|GR00|T N1.6|_π_|0_._5|Ours_w_|_/o_depth|Ours_w_|_/_ depth|
|---|---|---|---|---|---|---|---|---|---|---|
|**Tasks**|**SR**|**PS**|**SR**|**PS**|**SR**|**PS**|**SR**|**PS**|**SR**|**PS**|
|_#056_|0%|0%|0%|17%|0%|15%|7%|29%|7%|22%|
|_#057_|0%|0%|0%|1%|0%|3%|0%|13%|0%|8%|
|_#058_|0%|32%|0%|27%|20%|77%|7%|63%|27%|75%|
|_#060_|7%|38%|0%|22%|27%|67%|0%|37%|0%|17%|
|_#061_|47%|50%|0%|3%|40%|67%|93%|97%|60%|80%|
|_#062_|0%|0%|0%|2%|0%|2%|0%|2%|0%|2%|
|_#063_|0%|18%|0%|0%|0%|8%|0%|3%|0%|17%|
|_#064_|0%|0%|0%|0%|0%|2%|0%|13%|0%|2%|
|_#065_|0%|20%|20%|42%|7%|52%|40%|68%|80%|90%|
|_#066_|0%|3%|0%|7%|0%|17%|0%|15%|0%|15%|
|_#067_|0%|0%|0%|0%|0%|3%|0%|2%|0%|0%|
|_#068_|0%|0%|73%|83%|33%|37%|40%|60%|33%|40%|
|_#069_|0%|2%|0%|2%|0%|5%|0%|0%|0%|3%|
|_#070_|0%|0%|0%|0%|7%|7%|47%|60%|33%|53%|
|_#071_|7%|37%|0%|17%|0%|12%|27%|58%|13%|52%|
|_#072_|0%|0%|0%|0%|7%|13%|0%|0%|0%|0%|
|_#073_|0%|0%|0%|0%|0%|53%|0%|36%|0%|68%|
|_#074_|0%|7%|7%|41%|0%|1%|0%|21%|0%|25%|
|_#075_|0%|43%|0%|29%|0%|24%|0%|37%|0%|11%|
|_#076_|0%|37%|0%|7%|0%|22%|0%|50%|0%|43%|
|_#077_|0%|0%|53%|56%|67%|71%|73%|82%|53%|53%|
|_#078_|33%|37%|0%|3%|7%|10%|27%|37%|40%|50%|
|_#079_|0%|16%|0%|7%|0%|4%|0%|44%|7%|39%|
|_#080_|0%|0%|0%|0%|0%|0%|0%|7%|7%|17%|
|_#081_|0%|2%|0%|3%|0%|2%|0%|10%|0%|10%|
|_#082_|0%|0%|0%|2%|0%|18%|0%|17%|0%|20%|
|_#083_|7%|55%|60%|87%|60%|85%|20%|63%|0%|38%|
|_#084_|0%|11%|0%|12%|27%|66%|0%|38%|7%|46%|
|_#085_|0%|0%|67%|69%|0%|2%|80%|80%|27%|45%|
|_#086_|0%|7%|0%|10%|0%|0%|0%|20%|7%|23%|
|_#087_|33%|52%|0%|0%|47%|65%|60%|63%|67%|83%|
|_#088_|0%|3%|0%|4%|0%|1%|0%|45%|13%|44%|
|_#089_|0%|0%|0%|0%|0%|9%|7%|18%|7%|33%|
|_#090_|0%|4%|0%|13%|20%|42%|33%|62%|0%|32%|
|_#091_|0%|3%|0%|8%|20%|77%|40%|68%|47%|75%|
|_#092_|0%|29%|0%|15%|40%|57%|7%|18%|13%|35%|
|_#093_|0%|0%|87%|87%|7%|7%|0%|0%|13%|13%|
|_#094_|0%|0%|0%|3%|7%|27%|0%|19%|0%|12%|
|_#095_|0%|13%|7%|13%|0%|8%|13%|20%|7%|18%|
|_#096_|0%|0%|0%|3%|0%|0%|0%|0%|0%|0%|
|_#097_|20%|40%|0%|51%|0%|27%|7%|38%|13%|42%|
|_#098_|0%|0%|0%|10%|0%|10%|0%|3%|0%|2%|
|_#099_|0%|0%|0%|0%|0%|7%|0%|0%|0%|37%|
|_#100_|0%|4%|7%|11%|0%|7%|13%|27%|40%|53%|
|_#102_|0%|0%|0%|2%|0%|10%|33%|71%|7%|23%|
|_#103_|0%|17%|0%|33%|7%|27%|53%|70%|7%|40%|
|_#104_|7%|7%|0%|0%|0%|31%|7%|24%|0%|18%|
|_#105_|0%|0%|0%|0%|0%|12%|0%|20%|0%|13%|
|_#106_|0%|0%|0%|1%|7%|15%|7%|30%|7%|18%|
|_#107_|0%|0%|0%|12%|0%|7%|0%|28%|0%|27%|


15 

**Table S5. Real-world evaluation** on GM-100 [29] benchmark ( **Wheeled Humanoid Robot** : Galaxea R1Pro, Part I). 

||WAL|L-OSS|GR00|T N1.6|_π_|0_._5|Ours_w_|_/o_depth|Ours_w_|_/_ depth|
|---|---|---|---|---|---|---|---|---|---|---|
|**Tasks**|**SR**|**PS**|**SR**|**PS**|**SR**|**PS**|**SR**|**PS**|**SR**|**PS**|
|_#001_|13%|17%|13%|20%|20%|43%|20%|27%|27%|47%|
|_#002_|33%|45%|0%|2%|0%|2%|0%|10%|0%|8%|
|_#003_|7%|49%|0%|0%|0%|0%|73%|89%|33%|44%|
|_#006_|0%|1%|0%|12%|0%|0%|7%|28%|0%|6%|
|_#007_|0%|2%|0%|8%|13%|18%|0%|0%|33%|39%|
|_#008_|0%|4%|0%|14%|0%|20%|0%|43%|0%|45%|
|_#009_|0%|20%|80%|83%|13%|57%|33%|63%|27%|53%|
|_#010_|7%|8%|0%|2%|7%|15%|0%|15%|13%|43%|
|_#011_|33%|63%|80%|82%|73%|88%|100%|100%|80%|95%|
|_#012_|27%|33%|47%|62%|53%|72%|33%|35%|0%|2%|
|_#013_|0%|2%|0%|0%|40%|40%|87%|96%|80%|80%|
|_#014_|0%|0%|0%|3%|7%|7%|0%|25%|7%|35%|
|_#015_|47%|47%|93%|93%|40%|40%|53%|53%|47%|47%|
|_#016_|0%|0%|0%|0%|13%|30%|0%|8%|0%|38%|
|_#017_|0%|4%|0%|7%|0%|27%|0%|3%|0%|15%|
|_#018_|0%|17%|7%|20%|7%|28%|0%|10%|73%|87%|
|_#019_|0%|5%|0%|0%|0%|18%|0%|0%|0%|0%|
|_#020_|0%|0%|0%|0%|0%|0%|0%|0%|0%|0%|
|_#021_|0%|0%|7%|28%|20%|30%|20%|68%|0%|10%|
|_#022_|0%|1%|0%|16%|7%|33%|0%|18%|0%|28%|
|_#023_|0%|0%|0%|8%|7%|22%|0%|30%|0%|23%|
|_#024_|0%|0%|0%|5%|0%|0%|13%|32%|0%|16%|
|_#025_|0%|5%|0%|0%|0%|0%|0%|7%|0%|0%|
|_#026_|0%|4%|0%|7%|0%|0%|0%|2%|0%|0%|
|_#027_|0%|19%|20%|43%|47%|56%|7%|35%|13%|45%|
|_#028_|13%|32%|47%|57%|33%|58%|60%|73%|27%|55%|
|_#029_<br>|0%<br>|12%<br>|20%<br>|45%<br>|0%<br>|0%<br>|0%<br>|7%<br>|0%<br>|7%<br>|
|_#030_<br>|0%<br>|2%<br>|27%<br>|55%<br>|93%<br>|98%<br>|53%<br>|56%<br>|73%<br>|78%<br>|
|_#031_|7%|28%|7%|22%|0%|3%|0%|37%|20%|58%|
|_#032_|0%|4%|0%|2%|0%|33%|0%|15%|0%|0%|
|_#033_|0%|15%|13%|29%|7%|33%|27%|33%|33%|33%|
|_#034_|40%|75%|27%|53%|47%|64%|73%|82%|67%|71%|
|_#035_|0%|1%|0%|3%|0%|5%|0%|0%|0%|0%|
|_#036_|0%|1%|0%|6%|0%|22%|0%|11%|0%|17%|
|_#037_|0%|0%|0%|15%|7%|20%|0%|34%|0%|29%|
|_#038_|0%|0%|0%|0%|7%|11%|0%|1%|0%|0%|
|_#040_|0%|9%|0%|16%|0%|0%|7%|41%|7%|27%|
|_#041_|0%|2%|0%|12%|0%|3%|0%|5%|0%|0%|
|_#042_|13%|38%|80%|91%|27%|40%|60%|73%|60%|71%|
|_#043_|0%|2%|0%|0%|0%|25%|7%|45%|0%|48%|
|_#044_|0%|0%|0%|0%|0%|0%|0%|0%|0%|0%|
|_#045_|0%|0%|0%|4%|0%|3%|0%|1%|0%|3%|
|_#046_|7%|27%|0%|24%|13%|51%|7%|59%|33%|71%|
|_#047_|0%|9%|0%|15%|0%|12%|0%|14%|0%|6%|
|_#048_|0%|19%|0%|28%|7%|40%|7%|49%|0%|52%|
|_#049_|0%|7%|0%|5%|0%|5%|0%|2%|0%|5%|
|_#050_|0%|0%|0%|0%|0%|0%|0%|15%|0%|15%|
|_#051_|0%|0%|0%|0%|0%|3%|0%|17%|0%|10%|
|_#053_|0%|0%|0%|2%|0%|0%|0%|0%|20%|28%|
|_#054_|0%|10%|40%|63%|47%|53%|20%|37%|0%|33%|
|_#055_|0%|2%|0%|7%|0%|7%|0%|7%|0%|2%|


16 

**Table S6. Real-world evaluation** on GM-100 [29] benchmark ( **Wheeled Humanoid Robot** : Galaxea R1Pro, Part II). 

||WAL|L-OSS|GR00|T N1.6|_π_|0_._5|Ours_w_|_/o_depth|Ours_w_|_/_ depth|
|---|---|---|---|---|---|---|---|---|---|---|
|**Tasks**|**SR**|**PS**|**SR**|**PS**|**SR**|**PS**|**SR**|**PS**|**SR**|**PS**|
|_#056_|0%|8%|7%|32%|0%|22%|0%|52%|47%|68%|
|_#057_|0%|0%|0%|4%|0%|0%|0%|38%|0%|3%|
|_#058_|0%|8%|0%|15%|7%|15%|20%|30%|20%|33%|
|_#060_|0%|15%|7%|47%|7%|53%|20%|58%|20%|68%|
|_#061_|47%|57%|60%|63%|47%|57%|87%|93%|93%|97%|
|_#062_|0%|5%|0%|2%|0%|3%|0%|0%|0%|1%|
|_#063_|0%|7%|0%|23%|0%|23%|7%|32%|7%|22%|
|_#064_|0%|0%|0%|0%|0%|0%|0%|0%|0%|0%|
|_#065_|0%|17%|53%|70%|53%|53%|73%|80%|67%|80%|
|_#066_|0%|13%|0%|13%|0%|30%|0%|15%|0%|17%|
|_#067_|0%|0%|13%|13%|0%|0%|47%|48%|47%|47%|
|_#068_|7%|10%|20%|30%|40%|53%|13%|23%|0%|10%|
|_#069_|0%|3%|0%|8%|13%|40%|0%|33%|13%|45%|
|_#070_|7%|7%|73%|73%|60%|60%|73%|73%|87%|87%|
|_#071_|67%|73%|7%|20%|27%|30%|33%|65%|33%|63%|
|_#072_|0%|9%|0%|7%|0%|0%|0%|2%|0%|0%|
|_#073_|0%|3%|7%|41%|0%|12%|7%|12%|7%|40%|
|_#074_|0%|17%|0%|1%|7%|17%|20%|52%|0%|2%|
|_#075_|13%|13%|0%|11%|20%|33%|20%|37%|0%|16%|
|_#076_|20%|50%|0%|50%|0%|43%|13%|57%|13%|47%|
|_#077_|7%|7%|87%|96%|33%|38%|47%|53%|80%|82%|
|_#078_|80%|80%|80%|80%|93%|93%|87%|87%|80%|80%|
|_#079_|7%|9%|67%|81%|60%|73%|0%|9%|0%|9%|
|_#080_|0%|0%|0%|0%|0%|0%|0%|23%|40%|57%|
|_#081_|0%|17%|0%|22%|0%|22%|0%|50%|33%|62%|
|_#082_|0%|2%|0%|5%|20%|32%|47%|67%|0%|48%|
|_#083_|7%|12%|0%|22%|0%|22%|27%|57%|27%|57%|
|_#084_|0%|23%|13%|40%|7%|37%|20%|50%|13%|60%|
|_#085_|93%|93%|60%|60%|67%|71%|93%|93%|87%|93%|
|_#086_|0%|7%|0%|23%|7%|23%|13%|47%|40%|53%|
|_#087_|7%|18%|0%|2%|20%|54%|40%|67%|27%|37%|
|_#088_|0%|4%|0%|3%|0%|19%|53%|88%|73%|93%|
|_#089_|0%|0%|0%|0%|0%|1%|7%|10%|0%|3%|
|_#090_|0%|7%|0%|3%|0%|15%|0%|15%|20%|35%|
|_#091_|0%|0%|40%|70%|13%|20%|13%|23%|93%|93%|
|_#092_|7%|20%|27%|63%|0%|12%|47%|73%|0%|32%|
|_#093_|27%|27%|47%|47%|27%|27%|67%|67%|73%|73%|
|_#094_|0%|31%|0%|29%|0%|23%|0%|16%|0%|8%|
|_#095_|0%|22%|60%|67%|7%|22%|13%|29%|73%|87%|
|_#096_|0%|0%|0%|3%|0%|0%|0%|0%|0%|0%|
|_#097_|0%|0%|33%|58%|27%|27%|27%|29%|20%|33%|
|_#098_|0%|0%|0%|0%|27%|45%|0%|3%|7%|7%|
|_#099_|0%|3%|0%|0%|0%|0%|0%|3%|0%|10%|
|_#100_|0%|11%|20%|38%|53%|69%|27%|33%|60%|60%|
|_#102_|0%|2%|7%|16%|0%|29%|0%|33%|0%|18%|
|_#103_|0%|13%|0%|17%|20%|50%|33%|67%|33%|63%|
|_#104_|0%|2%|40%|51%|0%|0%|0%|2%|13%|20%|
|_#105_|0%|3%|0%|3%|0%|23%|0%|28%|0%|7%|
|_#106_|0%|1%|0%|5%|0%|2%|0%|25%|0%|24%|
|_#107_|53%|57%|7%|12%|7%|12%|47%|48%|0%|0%|


17 

**Table S7. Real-world evaluation** on GM-100 [29] benchmark ( **Bipedal Humanoid Robot** : Leju KUAVO 4 Pro, Part I). 

||WAL|L-OSS|GR00|T N1.6|_π_|0_._5|Ours_w_|_/o_depth|Ours_w_|_/_ depth|
|---|---|---|---|---|---|---|---|---|---|---|
|**Tasks**|**SR**|**PS**|**SR**|**PS**|**SR**|**PS**|**SR**|**PS**|**SR**|**PS**|
|_#001_|0%|3%|0%|13%|67%|68%|80%|85%|80%|82%|
|_#002_|0%|0%|0%|2%|0%|25%|0%|22%|0%|27%|
|_#003_|0%|3%|7%|27%|73%|80%|80%|87%|73%|83%|
|_#004_|0%|2%|0%|0%|0%|0%|0%|11%|0%|16%|
|_#005_|0%|4%|0%|8%|0%|0%|0%|20%|0%|11%|
|_#006_|0%|3%|0%|2%|0%|8%|7%|15%|0%|18%|
|_#007_|100%|100%|93%|93%|100%|100%|87%|87%|100%|100%|
|_#008_|0%|23%|0%|2%|0%|18%|0%|3%|0%|5%|
|_#009_|0%|0%|0%|5%|13%|39%|0%|16%|0%|25%|
|_#010_|0%|22%|0%|10%|0%|40%|7%|50%|0%|33%|
|_#011_|7%|20%|0%|18%|0%|15%|0%|30%|0%|27%|
|_#012_|0%|0%|0%|2%|0%|3%|0%|7%|0%|3%|
|_#013_|0%|27%|0%|20%|0%|2%|13%|70%|7%|65%|
|_#014_|0%|0%|0%|13%|7%|42%|0%|33%|0%|46%|
|_#015_|0%|0%|0%|20%|0%|3%|0%|33%|0%|36%|
|_#016_|0%|0%|0%|7%|0%|3%|0%|7%|0%|9%|
|_#017_|0%|37%|0%|7%|0%|0%|0%|57%|0%|42%|
|_#018_|0%|0%|0%|0%|0%|17%|0%|8%|7%|11%|
|_#019_|0%|0%|0%|0%|0%|18%|0%|45%|7%|27%|
|_#020_|0%|0%|0%|0%|0%|18%|0%|17%|0%|22%|
|_#021_|0%|0%|0%|0%|0%|0%|0%|0%|0%|0%|
|_#022_|0%|2%|0%|1%|0%|12%|0%|4%|0%|4%|
|_#023_|0%|20%|0%|21%|0%|25%|0%|31%|0%|31%|
|_#024_|0%|3%|0%|15%|0%|20%|0%|27%|7%|22%|
|_#025_|0%|23%|0%|25%|0%|27%|0%|11%|0%|3%|
|_#026_|0%|0%|0%|2%|0%|0%|67%|71%|7%|24%|
|_#027_|0%|12%|7%|33%|13%|37%|73%|78%|33%|40%|
|_#028_|0%|11%|0%|38%|0%|18%|7%|51%|0%|40%|
|_#029_|0%|18%|0%|60%|13%|20%|47%|56%|13%|22%|
|_#030_|0%|0%|0%|0%|7%|16%|0%|13%|27%|36%|
|_#031_|0%|0%|0%|2%|0%|9%|0%|47%|0%|31%|
|_#034_|0%|0%|0%|0%|0%|0%|0%|1%|0%|7%|
|_#036_|0%|0%|0%|0%|0%|11%|0%|7%|0%|27%|
|_#037_|0%|0%|0%|8%|0%|7%|0%|13%|0%|7%|
|_#038_|0%|16%|0%|7%|0%|0%|0%|24%|0%|47%|
|_#039_|0%|0%|0%|0%|0%|0%|0%|15%|0%|25%|
|_#042_|0%|7%|0%|12%|13%|42%|0%|18%|0%|20%|
|_#043_|0%|10%|0%|4%|0%|31%|20%|67%|0%|53%|
|_#044_|0%|0%|0%|0%|0%|6%|0%|17%|0%|16%|
|_#045_|0%|4%|0%|40%|60%|84%|40%|76%|53%|86%|
|_#046_|0%|2%|0%|10%|0%|2%|0%|2%|0%|3%|
|_#047_|0%|4%|0%|11%|0%|7%|0%|15%|0%|24%|
|_#048_|0%|15%|0%|13%|0%|12%|0%|22%|0%|25%|
|_#051_|0%|50%|0%|0%|73%|87%|87%|93%|80%|90%|
|_#052_|0%|0%|0%|7%|0%|26%|0%|10%|0%|0%|
|_#053_|0%|0%|0%|0%|0%|0%|0%|0%|0%|0%|
|_#054_|0%|0%|0%|0%|0%|3%|0%|8%|0%|12%|
|_#055_|0%|2%|0%|7%|0%|0%|0%|18%|0%|37%|
|_#056_|0%|11%|0%|13%|0%|3%|0%|20%|0%|13%|
|_#057_|0%|30%|7%|15%|7%|68%|13%|70%|0%|0%|


18 

**Table S8. Real-world evaluation** on GM-100 [29] benchmark ( **Bipedal Humanoid Robot** : Leju KUAVO 4 Pro, Part II). 

||WAL|L-OSS|GR00|T N1.6|_π_0|_._5|Ours_w_|_/o_depth|Ours_w_|_/_ depth|
|---|---|---|---|---|---|---|---|---|---|---|
|**Tasks**|**SR**|**PS**|**SR**|**PS**|**SR**|**PS**|**SR**|**PS**|**SR**|**PS**|
|_#059_|0%|67%|0%|48%|7%|70%|33%|80%|13%|70%|
|_#060_|73%|87%|87%|93%|100%|100%|87%|93%|93%|97%|
|_#061_|0%|0%|0%|1%|0%|0%|0%|0%|0%|0%|
|_#062_|0%|13%|13%|33%|13%|53%|0%|30%|0%|10%|
|_#063_|0%|0%|0%|0%|0%|0%|0%|0%|0%|2%|
|_#064_|0%|0%|0%|15%|0%|27%|0%|0%|0%|15%|
|_#065_|0%|0%|0%|3%|0%|2%|0%|23%|0%|22%|
|_#066_|0%|17%|0%|43%|0%|0%|20%|80%|60%|78%|
|_#067_|0%|0%|40%|40%|53%|77%|27%|63%|53%|77%|
|_#068_|0%|0%|0%|8%|0%|3%|0%|20%|0%|13%|
|_#069_|20%|20%|60%|60%|93%|93%|53%|57%|67%|73%|
|_#070_|0%|18%|0%|17%|0%|0%|0%|30%|7%|10%|
|_#071_|0%|0%|0%|0%|0%|0%|0%|0%|0%|0%|
|_#072_|0%|0%|0%|8%|0%|15%|47%|49%|0%|1%|
|_#074_|0%|0%|0%|2%|7%|31%|27%|33%|7%|11%|
|_#075_|0%|50%|7%|53%|73%|87%|73%|87%|67%|83%|
|_#076_|0%|42%|27%|49%|0%|0%|53%|58%|53%|67%|
|_#077_|0%|3%|0%|7%|13%|20%|27%|43%|33%|57%|
|_#078_|0%|20%|0%|47%|0%|17%|0%|24%|0%|28%|
|_#079_|0%|3%|0%|20%|0%|10%|0%|3%|0%|33%|
|_#080_|0%|0%|13%|57%|0%|25%|7%|48%|0%|27%|
|_#082_|0%|0%|0%|3%|7%|30%|33%|68%|0%|55%|
|_#083_|0%|14%|0%|16%|33%|52%|0%|20%|0%|36%|
|_#084_|40%|76%|67%|89%|67%|87%|80%|93%|20%|69%|
|_#085_|47%|57%|53%|60%|53%|63%|73%|83%|80%|83%|
|_#086_|20%|28%|7%|37%|33%|58%|60%|80%|80%|85%|
|_#087_|0%|0%|0%|19%|0%|0%|40%|77%|20%|41%|
|_#088_|0%|0%|0%|2%|0%|21%|0%|0%|0%|0%|
|_#089_|0%|25%|13%|65%|0%|44%|27%|52%|13%|53%|
|_#090_|0%|5%|0%|13%|0%|10%|20%|40%|27%|57%|
|_#091_|0%|0%|0%|0%|0%|0%|20%|22%|7%|47%|
|_#092_|0%|0%|47%|47%|93%|93%|60%|60%|73%|73%|
|_#093_|0%|12%|0%|7%|0%|9%|0%|20%|0%|17%|
|_#094_|0%|0%|0%|31%|7%|40%|0%|36%|47%|69%|
|_#095_|0%|0%|0%|0%|0%|0%|7%|13%|0%|0%|
|_#096_|0%|47%|0%|47%|13%|49%|60%|82%|73%|87%|
|_#097_|0%|0%|0%|3%|0%|5%|0%|3%|0%|3%|
|_#098_|0%|0%|0%|0%|0%|0%|0%|0%|0%|2%|
|_#100_|0%|0%|0%|0%|0%|0%|0%|0%|0%|0%|
|_#101_|0%|4%|0%|20%|0%|38%|13%|47%|13%|58%|
|_#102_|0%|10%|60%|80%|80%|90%|60%|80%|67%|83%|
|_#103_|0%|0%|0%|0%|0%|36%|0%|13%|0%|27%|
|_#104_|0%|0%|0%|3%|0%|15%|0%|22%|0%|18%|
|_#105_|0%|2%|0%|1%|0%|8%|0%|24%|0%|17%|
|_#106_|0%|0%|0%|13%|20%|27%|20%|60%|0%|50%|
|_#107_|53%|61%|0%|21%|0%|4%|20%|67%|20%|72%|
|_#109_|0%|0%|0%|0%|0%|58%|0%|53%|0%|62%|


19 

**Table S9. Simulation evaluation** on RoboTwin 2.0 [8] benchmark, under “clean” and “randomized” settings. 

||_π_|0_._5|Ours_w_|_/o_depth|Ours_w_|_/_ depth|
|---|---|---|---|---|---|---|
|**Simulation Tasks**|**Clean**|**Rand.**|**Clean**|**Rand.**|**Clean**|**Rand.**|
|_Adjust Bottle_|100%|99%|100%|100%|100%|100%|
|<br>_Beat Block Hammer_|96%|93%|87%|91%|92%|89%|
|_Blocks Ranking Rgb_|92%|85%|92%|91%|92%|91%|
|_Blocks Ranking Size_|49%|26%|66%|73%|76%|70%|
|_Click Alarmclock_|98%|89%|93%|26%|97%|43%|
|_Click Bell_|99%|66%|32%|19%|43%|36%|
|_Dump Bin Bigbin_|92%|97%|97%|92%|97%|97%|
|<br>_Grab Roller_|100%|100%|100%|99%|100%|100%|
|_Handover Block_|66%|57%|80%|83%|83%|95%|
|_Handover Mic_|98%|97%|94%|98%|94%|99%|
|_Hanging Mug_|18%|17%|32%|27%|34%|53%|
|_Lift Pot_|96%|85%|100%|99%|100%|100%|
|_Move Can Pot_|51%|55%|79%|84%|89%|87%|
|_Move Pillbottle Pad_|84%|61%|93%|94%|92%|90%|
|_Move Playingcard Away_|96%|84%|96%|99%|98%|100%|
|_Move Stapler Pad_|56%|42%|74%|49%|74%|48%|
|<br>_Open Laptop_|90%|96%|96%|96%|98%|96%|
|<br>_Open Microwave_|34%|77%|91%|75%|91%|92%|
|_Pick Diverse Bottles_|81%|71%|79%|86%|88%|85%|
|_Pick Dual Bottles_|93%|63%|82%|95%|99%|90%|
|_Place A2b Left_|87%|82%|86%|83%|89%|85%|
|_Place A2b Right_|87%|84%|74%|77%|80%|80%|
|<br>_Place Bread Basket_|77%|64%|92%|93%|95%|93%|
|_Place Bread Skillet_|85%|66%|90%|89%|90%|92%|
|_Place Burger Fries_|94%|87%|95%|96%|98%|94%|
|<br>_Place Can Basket_|62%|62%|68%|78%|75%|72%|
|_Place Cans Plasticbox_|94%|84%|97%|100%|100%|98%|
|_Place Container Plate_|99%|95%|99%|99%|99%|100%|
|_Place Dual Shoes_|75%|75%|80%|83%|87%|86%|
|_Place Empty Cup_|100%|99%|100%|100%|100%|100%|
|_Place Fan_|87%|85%|91%|79%|92%|87%|
|_Place Mouse Pad_|60%|39%|82%|78%|86%|79%|
|_Place Object Basket_|80%|76%|90%|91%|90%|88%|
|_Place Object Scale_|86%|80%|84%|90%|90%|88%|
|_Place Object Stand_|91%|85%|97%|93%|93%|88%|
|_Place Phone Stand_|81%|81%|92%|93%|90%|87%|
|_Place Shoe_|92%|93%|99%|94%|99%|99%|
|_Press Stapler_|87%|83%|90%|88%|86%|93%|
|_Put Bottles Dustbin_|84%|79%|88%|92%|92%|93%|
|_Put Object Cabinet_|80%|79%|92%|86%|85%|88%|
|_Rotate Qrcode_|89%|87%|93%|84%|86%|82%|
|_Scan Object_|72%|65%|91%|97%|92%|96%|
|<br>_Shake Bottle Horizontally_|99%|99%|100%|100%|99%|98%|
|<br>_Shake Bottle_|99%|97%|99%|100%|100%|99%|
|<br>_Stack Blocks Three_|91%|76%|92%|99%|96%|95%|
|_Stack Blocks Two_|97%|100%|100%|100%|100%|99%|
|_Stack Bowls Three_|77%|71%|72%|83%|71%|77%|
|_Stack Bowls Two_|95%|96%|92%|95%|90%|97%|
|_Stamp Seal_|79%|55%|76%|86%|74%|77%|
|<br>_Turn Switch_|62%|54%|61%|65%|67%|63%|


20 

