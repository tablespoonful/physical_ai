---
title: "A Generalist Pair-wise Progress Critic Model for Vision-Language-Action Robots"
date: "2026"
venue: "ICML 2026"
url: https://proceedings.mlr.press/v306/zhang26if.html
pdf: https://raw.githubusercontent.com/mlresearch/v306/main/assets/zhang26if/zhang26if.pdf
converter: pymupdf4llm
---

> **[PDF を開く](https://raw.githubusercontent.com/mlresearch/v306/main/assets/zhang26if/zhang26if.pdf)** / [論文ページ](https://proceedings.mlr.press/v306/zhang26if.html)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **A Generalist Pair-wise Progress Critic Model for Vision-Language-Action Robots** 

**Qi Zhang**<sup>1</sup> **Shaopeng Zhai**<sup>1</sup> **Shengzhe Zhang**<sup>1 2</sup> **Litao Liu**<sup>1 3</sup> **Tianyi Zhang**<sup>1</sup> **Fuxian Huang**<sup>1</sup> **Ming Zhou**<sup>1</sup> 

## **Abstract** 

Recent advances in Vision-Language-Action (VLA) models have significantly improved robotic perception and manipulation capabilities, but still struggling to adapt in dynamic, openended real-world environments due to a lack of reliable task progress feedback and improvement mechanisms. To address these challenges, we propose a generalist Vision Language ActionCritic model, VLAC, which can integrate both human and robot data, and unify action policy and task progress critic within a single autoregressive architecture. Specifically, we propose a scalable and generalizable pair-wise progress understanding approach that can predict the delta of task progress between two steps in a trajectory and generate correct actions to complete the task. Then, we trained the model on large-scale, multi-source human, robot, and general visionlanguage data for a generalist. Furthermore, we deploy reinforcement learning where VLAC can autonomously evaluate task progress to provide intrinsic rewards. Extensive evaluations demonstrate that our model generalizes effectively across diverse tasks and environments, leveraging its pair-wise progress understanding to provide reliable dense rewards, robust action generation, and significant improvements in real-world reinforcement learning. Our codes are available at https: //github.com/InternRobotics/VLAC. 

## **1. Introduction** 

With the rapid development of Vision-Language-Action (VLA) models, the intelligence of robotic perception and manipulation capabilities has greatly improved, leading to impressive performance in autonomously completing general tasks. Current VLA models are primarily trained 

1Shanghai AI Lab 2University of Science and Technology of China<sup>3</sup> Rutgers University. Correspondence to: Shaopeng Zhai _<_ zhaishaopeng@pjlab.org.cn _>_ . 

_Proceedings of the 43_<sup>_rd_</sup> _International Conference on Machine Learning_ , Seoul, South Korea. PMLR 306, 2026. Copyright 2026 by the author(s). 

through imitation learning, which requires vast amounts of data (Lin et al., 2024; Team et al., 2025; Deng et al., 2025; Bjorck et al., 2025). However, collecting human expert trajectories is not only costly and time-consuming, but most data collection efforts focus on laboratory-customized scenes and tasks. Consequently, significant barriers remain for robots to perform effectively in dynamic real-world scenarios, especially when the deployment environment and tasks differ from the training data. One critical limitation is that robots struggle to accurately evaluate task progress and lack efficient feedback mechanisms for learning and improvement in new scenarios. 

To address this limitation, action models with strong generalization and critic models can jointly acquire visuomotor skills in new environments (Ma et al., 2024). In realworld RL, many methods still depend on hand-crafted, taskspecific reward shaping (Mendonca et al., 2024; Herzog et al., 2023; Mendonca et al., 2023; Kumar et al., 2024; Xu et al., 2022). Approaches advertised as reusable often require additional task-dependent data for reward surrogates or termination classifiers (Luo et al., 2024; Hu et al., 2023), while sparse signals appear only near completion. Although some works propose denser progress signals (Ma et al., 2023; 2022), they generalize poorly to unseen tasks or goals. Recent work uses pretrained VLMs for progress estimation (Ma et al., 2024), yet evaluation relies on singlepoint estimates and expert trajectories, restricting diversity. Meanwhile, VLA models aim to improve manipulation generalization (Black et al., 2024; Intelligence et al., 2025; Team et al., 2025; Kim et al., 2024), but training focuses on action generation without explicit task process understanding. Achieving fine-grained, generalizable critic feedback integrated with action generation for broad manipulation remains challenging. 

To this end, in this paper, we propose a generalist VisionLanguage-Action-Critic model, VLAC, which unifies the roles of “actor” and “critic” within a single autoregressive architecture via pair-wise progress understanding, capable of dense and precise task progress prediction and robust action generation. Some real-world interaction examples of robot manipulation and progress prediction are shown in Figure 1. In order to provide dense and precise feedback signals that effectively reflect the quality of robotic actions and can be scaled to large-scale unlabeled data, we 

1 

**A Generalist Pair-wise Progress Critic Model for Vision-Language-Action Robots** 


around 100% higher scores to successful processes than failed ones, enabling fine-grained progress discrimination and dataset quality estimation. For action generation, VLAC can produce plausible actions across diverse real-world tasks with robustness to extreme lighting variations. In realworld RL, VLAC autonomously self-improves by adaptively leveraging both successful and failed trajectories through progress-based rewards. 

In summary, our contributions are: 

1. A unified Vision-Language-Action-Critic framework that jointly trains action generation and progress understanding within a single autoregressive model, demonstrating that these two capabilities mutually enhance each other in the real-world environment. 

_Figure 1._ Examples of robot manipulation and progress prediction. 

propose an image observation pair-wise progress prediction method. This approach leverages visual images to assess the relative task progress between two states, focusing on the differences between image observations. It is capable of detecting subtle changes and learning variations across different temporal scales, making it adaptable to various task lengths and scenarios. During training, annotations and negative samples are automatically generated based on temporal relationships, enabling convenient large-scale expansion. In addition to progress prediction, auxiliary tasks such as object detection, 3D scene understanding, and pairwise image differences detection are introduced to further enhance the critic’s capabilities. We also constructed an incontext learning dataset, which includes examples of similar tasks along with corresponding progress labels. 

Then, the VLAC model was trained to simultaneously handle action generation and progress understanding. When the dataset contains action data, we construct corresponding action train data aligned with progress understanding, enabling VLAC to generate the appropriate actions based on the first step of the pair mentioned above. We connect the actor and critic tasks through shared steps, enabling the model to understand both the process and the action generation at each step. The pair-wise progress understanding further provides insights into changes before and after actions, enhancing the model’s comprehension of action effects. For action output, we use the delta end-of-effector (EEF) position as action and experiment with both semantic discrete actions and FAST (Pertsch et al., 2025) discrete actions. This approach offers improved spatial awareness, better alignment with semantic space, and delivers stronger generalization capabilities. 

We conduct comprehensive evaluations of VLAC across eight public datasets (six six out-of-distribution) and observe strong cross-task, cross-entity generalization, further enhanced via in-context learning. Notably, VLAC assigns 

2. Pair-wise progress understanding method modeling the relative delta changes between pairs of images in visual trajectories, which naturally addresses the lack of negative examples in robotic datasets, and provides fine-grained, accurate, and generalizable results. 

3. VLAC is jointly trained on action-free human data, web videos, and action-labeled robot datasets. It is evaluated on eight datasets (six unseen) for critic capability, and on real-world manipulation tasks for action generation performance and on-robot self-improvement. 

## **2. Related Work** 

**Embodied reward models.** Some studies consider referencing different data sources to learn transferable reward and value functions to guide manipulation tasks. Early researches use various forms of data as criteria, such as robot (Sermanet et al., 2016) human videos with discriminators (Dasari & Gupta, 2021) and multi-player arenas (Sun et al., 2025), etc. Some of them also design algorithms to learn functions, including contrastive learning (Zitkovich et al., 2023) and offline RL methods (Ma et al., 2022; 2023; Bhateja et al., 2023). Recently, with the rise of LLMs and VLMs, research on utilizing them as reward models has begun to emerge. To leverage their encoding abilities, some works utilize them to learn an embedding computing function and calculate current observations and goals into embedding vectors, and take their distances as reward (Zhang et al.; Ma et al., 2022; 2023; Bhateja et al., 2023). Some methods (Zhou et al., 2024; Li et al., 2025) further integrate encoding and generating abilities, which synthesize goal observations and regard discrepancies between current observations and them as the progressive value. Furthermore, some models treat reward and value function learning as related tasks to optimize the training objectives. For instance, (Chen et al., 2025) formulates reward modeling as reasoning tasks. Besides these indirect progress modeling methods, recent works directly predict a concrete number of current 

2 

**A Generalist Pair-wise Progress Critic Model for Vision-Language-Action Robots** 


_Figure 2._ Overall framework of the VLAC model. The left panel illustrates the training stage, where pair-wise progress understanding is optimized. The right panel shows the inference stage for progress estimation and action generation. 

progress based on input observations, such as (Ma et al., 2024). Despite achieving significant breakthroughs, existing literatures are mainly based on single-point estimates, thus lacking the ability of comprehensive progress understanding and continuous reward esimating. Our proposed VLAC is a mechanism of pair-wise progress understanding to tackle this problem. 

**Vision-Language-Action Models (VLAs).** VLAs integrate the capabilities of visual analysis, language understanding, and action prediction, demonstrating powerful performances in robot manipulation tasks. Early works including RT-1 (Brohan et al., 2022) and RT-2 (Zitkovich et al., 2023) unlock end-to-end policy learning by action tokenization. After that, open-source approaches such as Octo (Team et al., 2024), OpenVLA (Kim et al., 2024), and OpenVLA-OFT (Kim et al., 2025) have emerged. Flow matching-based methods, _π_ 0 (Black et al., 2024) and _π_ 0 _._ 5 (Intelligence et al., 2025), for instance, also verify the power of this paradigm. Recently, much research on VLA has focused on progress understanding and wrong action detection. For example, CoT-VLA (Zhao et al., 2025) applies a chain of thought to split a task into progressive subtask instructions to improve VLA task understanding. FPC-VLA (Yang et al., 2025) utilizes a fine-tuned supervisor to check failure in the manipulation process. These works validate the crucial meaning of reward modeling for progress on robot manipulation. 

## **3. Vision-Language-Action-Critic Model** 

We constructed a Vision-Language-Action-Critic (VLAC) model based on pair-wise task progress understanding, enabling both action generation and delta task progress prediction (Figure 2). VLAC leverages diverse data sources: public robotic manipulation datasets, human demonstration 

data, our self-collected manipulation data, and general image understanding datasets. Video trajectories are converted into pair-wise samples to learn relative task progress between arbitrary states, with each pair augmented by a task description and task completion evaluation to enable task progress estimation and action generation (left of the figure). The pair-wise formulation is agnostic to data collection strategies and segment starting points, improving robustness and generality. For each pair, the model outputs a delta progress value: a positive value indicates that the second image corresponds to a more advanced stage of task completion, while a negative value indicates regression. VLAC can estimate task progress and identify failing actions or trajectories, providing dense reward signals for real-world reinforcement learning and guiding data refinement. It can also operate as a Vision-Language-Action model to directly perform manipulation, exhibiting zero-shot generalization to varied scenarios (right of the figure). In the following, we detail four subsections: Pair-wise Task Progress Understanding, Semantic Space Action Generation, General Vision-Language Understanding, and Multi-Source Training Datasets. 

### **3.1. Preliminary** 

We formalize the task process as a video segment with a description _V_ = ( _O, l_ task), where _O_ = ( _o_ 1 _, . . . , oT_ ) represents a sequence of RGB images, and _l_ task denotes the textual description of the task goal. Each training trajectory in our dataset corresponds to a successful and efficient execution of the annotated task. The VLAC model is defined as _fθ_<sup>obj, where</sup><sup>_fθ_represents the VLAC model parameterized</sup> by _θ_ . The term obj indicates that different objectives of generation tasks share a unified model architecture, distin- 

3 

**A Generalist Pair-wise Progress Critic Model for Vision-Language-Action Robots** 

guished by objective-specific input prompts. This design enables unified training while preserving the ability to generate objective-specific outputs. 

### **3.2. Pair-wise task progress understanding** 

Humans often encounter limitations in their initial capabilities when faced with new environments and new tasks. However, their ability to understand the progression of the task is exhibited in a higher generalizability than their ability to execute tasks. This ability enables continuous assessment of the task progress across various processes, thereby optimizing one’s actions and achieving sustained improvement. Rich general knowledge thus endows the understanding of task progress with strong generality, which can facilitate capabilities when faced with different environments and tasks. Inspired by this, for robot manipulation models to be deployed in the complexity of the real world and execute general tasks, they must not only understand language and visual information, but also understand task progress, which can indicate changes in task completion status across different processes. We design a pair-wise task progress understanding method that is unaffected by the initial point of the task. This method integrates general human data without action information and robot data annotated with actions to estimate fine-grained variations in task processes robustly. 

**Task Progress Estimation.** To understand the variations of the task process, we assume that task progress is positively correlated with time; as time increases, the task progresses. Thus, pair-wise task progress understanding can be formalized as 


where ∆ _t_ denotes the time difference between two frames, and _ci,i_ +∆ _t_ represents the degree to which the task progresses in _oi_ +∆ _t_ advances the task relative to _oi_ . Specifically, ∆ _t ∈_ [ _−i_ + 1 _, T − i_ ] _∩_ Z, which allows us to focus on both fine-grained single-step changes and long-term task progress, mitigating noise from minor variations while naturally constructing balanced negative samples. During training, _ci,i_ +∆ _t_ is annotated according to the natural temporal order as _ci,i_ +∆ _t_ = ∆ _t/_ ( _T − i_ ), representing the percentage of task progress from _oi_ to _oi_ +∆ _t_ . This task progress understanding approach is independent of data collection strategies and starting points of segment, enhancing generality and robustness, as illustrated in the lower left corner of Figure 2. 

**Task Description Generation.** To further enhance the semantic understanding of the task process, we construct a task description estimation task: 


where _oi_ start _∈_ [0 _,_ 0 _._ 3 _T_ ] _∩_ Z and _oi_ end _∈_ [0 _._ 8 _T, T_ ] _∩_ Z. By generating task descriptions from the initial and final frames, the task description becomes not only an input condition 

but also an output target, thereby improving the joint understanding of vision and language. 

**Task Completion Judgment.** To enhance understanding of task completion, we design a task completion judgment task: 


where if _i <_ 0 _._ 8 _T_ , _l_ done = 0 indicates the task is not yet completed, and if _i >_ 0 _._ 95 _T_ , _l_ done = 1 indicates the task is completed. Considering the diversity of data and collection strategies, it is difficult to accurately determine the exact completion point; thus, for 0 _._ 8 _T ≤ i ≤_ 0 _._ 95 _T_ , no training label is made to ensure label accuracy. By learning to judge task completion, the model’s understanding of completion conditions is enhanced, providing auxiliary signals for task completion in real-world reinforcement learning. 

We use different prompts to distinguish different tasks. Furthermore, to improve the task progress understanding, we design four data construction strategies: 

1. Pair-wise Image Difference Filtering: We assume task progress is positively correlated with time, which generally holds but may be violated in noisy data or segments with minimal change (e.g., static scenes). To mitigate the impact of such noise, we set the interval between _i_ and _i_ + 1 to approximately 0.2s during data construction and compare the pixel difference between the two frames. If Diff( _oi, oi_ +∆ _t_ ) _< σ_ , then set _ci,i_ +∆ _t_ = 0, indicating the two frames are in the same progress. In our experiments, we set _σ_ = 1%, enabling the model to focus on significant changes and improving the robustness of task progress understanding. 

2. Pair-wise Progress Understanding with Joint Sampling: Inspired by contrastive learning, to ensure data balance and symmetry between forward and reverse processes, for each sampled pair ( _oi, oi_ +∆ _t_ ), we construct four related data samples as a mini group within a batch: 


This covers both forward and backward directions, as well as fine-grained and global understanding, as shown in the lower left of Figure 2. 

3. Task Completion Judgment Joint Sampling: For data balance in the task completion judgment task, each time we sample a pair of data: one from a completed state and one from an incomplete state within the same trajectory. 

4. Cross-sampling of Task Descriptions and Image Sequences: To enhance the model’s ability to distinguish whether a process matches the task description, we sample, with a 5% probability during pair-wise data sampling, a task description _l_ task that does not belong to the current trajectory, setting _ci,i_ +∆ _t_ = 0. This method aims to improve 

4 

**A Generalist Pair-wise Progress Critic Model for Vision-Language-Action Robots** 

the alignment of semantic and progress understanding of the model. 

**In-Context Progress Estimation.** Cross-scene and crosstask transferability remains a key challenge for embodied intelligence models on the path to generalization. When humans adapt to new environments and tasks, their initial capabilities may also be limited; however, having reference examples can significantly improve both initial performance and learning efficiency. Inspired by this, and to improve the cross-scene and cross-task transferability of VLAC, we further enhance progress understanding with in-context learning, enabling effective learning from a single reference example. Specifically, in-context progress understanding can be formalized as 


open: 0”: 


where _o_<sup>_k_</sup> _i_<sup>denotesthe</sup><sup>_k_-thviewpointatthe</sup><sup>_i_-thstep,</sup><sup>_si_</sup> represents the state of the robotic arm, and _ai_ is the action to be executed at the _i_ -th step, represented as a string of numbers. Meanwhile, _o_<sup>_k_</sup> _i_<sup>andthesubsequentimage</sup> _o_<sup>_k_</sup> _i_ +1<sup>, obtained after executing action</sup><sup>_ai_, can be paired for</sup> progress understanding. Additionally, we also experiment with FAST (Pertsch et al., 2025) as the action tokenizer for action chunk output. 

With this formulation, VLA demonstrates strong semantic and scene generalization capabilities. Moreover, the generated actions can be sampled with diversity within a reasonable range, which is beneficial for exploration and improvement in reinforcement learning. 

### **3.4. General vision language understanding** 

where _O_ ref is the reference process, which may be provided by a robot demonstration or a human demonstration, offering guidance on both scene and task logic. _o_ 0 is the starting point of the current trajectory and can be optionally included as input, enhancing the model’s ability to align with the reference process and enabling inference of the absolute progress of _oi_ and _oi_ +∆ _t_ . 

These tasks we construct do not require action information, thereby avoiding the issue of inconsistent action spaces across entities. This design also allows our approach to apply to both human and robot data, enabling the use of large-scale, diverse human data to significantly improve model generalization and alleviate the scarcity of robot data in the real world. Moreover, in-context learning endows the model with rapid transfer capabilities and further enhances its generalization. The in-context reference is selected as a different trajectory of the same task from the same dataset, simulating a setting where one recorded demonstration is available for a new environment. 

### **3.3. Semantic space action generation** 

Based on general task process understanding, we further construct an action generation task in the semantic space to achieve multi-task control of a robotic arm. Since the general generation capabilities of pretrained multimodal models are mainly in the semantic space, and task understanding is also generated in the semantic space, we fully leverage this knowledge and the strong semantic representations of pretrained models by representing actions as numbers and generating them in the semantic space. 

To further improve spatial reasoning performance, the action is represented as the delta End-Effector (EEF) pose, which is a general spatial representation while remaining independent of embodied entities, e.g., ”x: -47mm, y: 19mm, z: 66mm, roll: 14 degrees, pitch: 10 degrees, yaw: 15 degrees, 

To enhance the model’s multimodal understanding capabilities, we incorporate publicly available VQA datasets across four key aspects: (1) general conversational ability using LLAVA (Liu et al., 2023), (2) robotic understanding with RoboVQA (Sermanet et al., 2024), (3) spatial reasoning through SpatialVQA (Chen et al., 2024a), and (4) pair-wise image difference distinction via Spot-the-diff (Jhamtani & Berg-Kirkpatrick, 2018) and InstructPix2Pix (Brooks et al., 2023). These datasets collectively strengthen the model’s multimodal reasoning capabilities across diverse domains. 

### **3.5. Multi-source train datasets** 

We train VLAC on a unified multi-source dataset spanning human real-world interaction video (Ego4D HOD (Pei et al., 2025)), general vision-language instruction, editing and VQA style supervision (InstructPix2Pix (Brooks et al., 2023), RobotVQA (Sermanet et al., 2024), Spot the Diff (Jhamtani & Berg-Kirkpatrick, 2018), LLaVA (Liu et al., 2023), SpatialQA (Chen et al., 2024a)), and diverse real-world robotic manipulation trajectories (AGIBOT (Bu et al., 2025), Bridge (Walke et al., 2023), DROID (Khazatsky et al., 2024), FMB (Luo et al., 2025), RoboSet (Bharadhwaj et al., 2024)) plus our self-collected data, totaling roughly 40M sampled training instances (including a subset with multi-turn dialogue annotations) from about 4.2K hours of embodied and human interaction video, enabling joint modeling of pair-wise progress deltas, semantic grounding, and action generation. Full composition statistics and details are provided in the Appendix A. 

## **4. Experiments** 

### **4.1. Implementation Details** 

VLAC-8B and VLAC-2B use InternVL2-8B and InternVL22B (Chen et al., 2024b) as the base backbones. During the pre-training phase of the VLAC model, we used a batch 

5 

**A Generalist Pair-wise Progress Critic Model for Vision-Language-Action Robots** 

size of 3200 and set the maximum learning rate to 8e-4. The training was conducted on 200 A100-SXM4-80GB GPUs. The 8B model required about 240 hours, and the 2B model about 116 hours. The robot in our real-world experiment is AGILE PiPER and it is controlled via a 7- DOF end effector based on the delta pose mechanism. We use the PPO algorithm to conduct the RL experiments. 

### **4.2. Evaluation Datasets** 

To evaluate VLAC’s ability to understand task progress and generalize to out-of-distribution (OOD) scenarios, we test on both training datasets and six additional OOD datasets. These datasets cover diverse entities, tasks, and environments, enabling a comprehensive assessment of VLAC’s generalization capabilities. 

**In-Distribution Datasets.** We use the **Bridge** (Walke et al., 2023) and **Droid** (Khazatsky et al., 2024) datasets for indistribution evaluation. These datasets include robotic manipulation tasks with diverse trajectories and entities, providing a foundation for training and validation. 

**OOD Datasets.** For generalization testing, we evaluate on six datasets unseen during training: 

- **RT-1** (Brohan et al., 2022): A large-scale real-world dataset across 700+ diverse tasks, performed by mobile robots in office kitchen environments. 

- **RoboNet** (Dasari et al., 2019): A dataset without language annotations and with unsmooth temporal structures, challenging VLAC’s ability to infer task progress without explicit guidance. 

- **Dobb-E** (Shafiullah et al., 2023): Features a unique gripper and gripper-perspective views, evaluating cross-entity and cross-viewpoint generalization. 

- **RH20T** (Fang et al., 2023): A massive-scale, contactrich dataset including cooking, cleaning, and assembly in varied tabletop scenarios. 

- **EgoDex** (Hoque et al., 2025): A human hand manipulation dataset, testing VLAC’s compatibility with dexterous tasks and human-centric trajectories. 

- **RoboFAC** (Lu et al., 2025): Contains both **successful** and **failed** task processes, providing a direct benchmark for progress understanding and error detection. 

et al., 2023): a vision-language value learning method that pre-trains representations from human videos and provides dense rewards for language or image specified goals. (3) VLAC w/o pair-wise: an ablation using single-point estimation to validate our pair-wise approach; (4) VLAC w/o Ego: an ablation excluding Ego4D human data to assess the contribution of human demonstrations. 

**Actor Baselines.** (1) _π_ 0 (Black et al., 2024): a state-of-theart VLA flow model fine-tuned on our task data; (2) VLAC w/o pretrain: an ablation without progress understanding pretraining; (3) VLAC+FAST: a variant using the FAST action tokenizer (Pertsch et al., 2025). 

### **4.4. Evaluation Metrics** 

Following GVL (Ma et al., 2024), we use Value-Order Correlation (VOC) as the primary metric for task progress understanding. VOC is the rank correlation between predicted step values and their chronological order in an expert video for the single-point prediction method; higher values indicate that the robot’s actions in the video are more aligned with advancing task progress. 

**VOC Computation for Pair-wise Methods.** For our pairwise approach, VOC is computed by progressively accumulating pair-wise predictions. Specifically, given a trajectory ( _o_ 1 _, ..., oT_ ), we compute: _vi_ = _vi−_ ∆ _t_ + _ci−_ ∆ _t,i ·_ (1 _− vi−_ ∆ _t_ ) _, v_ 0 = 0 where _ci−_ ∆ _t,i_ is the predicted progress delta between consecutive frames. The VOC is then computed as the rank correlation between ( _v_ 1 _, ..., vT_ ) and the chronological order. Furthermore, to assess the robustness of pair-wise methods, we introduce Value-Reversed-Order Correlation (VROC), computed after reversing the sequence; performance is more stable when VROC is close to VOC. We report VOC-F1, the harmonic mean of VOC and VROC, to jointly capture forward and reversed consistency, which is better suited to pair-wise methods. This accumulation scheme preserves long-horizon temporal relationships while leveraging the fine-grained pair-wise predictions. As demonstrated in Figures 4 (c) and (d), our model performs well on both neighboring frames and distant frame comparisons. The detailed description of Evaluation Metrics can be seen in Appendix B. 

### **4.5. VLAC Critic Performance** 

### **4.3. Baselines** 

To the best of our knowledge, we are the first to unify action generation and task progress understanding within a single architecture. Accordingly, we separately evaluate the critic and actor components against their respective state-of-theart methods and variants. 

**Critic Baselines.** (1) GVL (Ma et al., 2024): a trainingfree method based on Gemini-1.5-Pro representing stateof-the-art zero-shot progress understanding;(2)LIV (Ma 

The VLAC model trained on public robotic manipulation data mainly includes bridge, droid, roboset, fmb, AgiBot World, excluding the RT1 and other datasets, and the robotic arm entities, scenes, and tasks in these datasets are almost different from the above datasets. We will conduct further large-scale validation on these datasets. We trained three models: the VLAC-8b model with 8 billion parameters, the VLAC-8b w/o Ego model (which was trained without the Ego4D dataset), and the VLAC-2b model with 2 billion parameters. The overall performance across the eight datasets 

6 

**A Generalist Pair-wise Progress Critic Model for Vision-Language-Action Robots** 


_Figure 4._ Example results of VLAC for task progress understanding. 

is shown in Figure 3. Compared to the GVL model, which is based on Gemini-1.5-pro and represents the state-of-the-art, VLAC demonstrates significant improvements in performance. To further validate the effectiveness of the pair-wise approach, we trained and tested VLAC-8B w/o pair-wise using a single-point prediction method similar to GVL. The results, as shown in the figure, indicate that the pair-wise method substantially enhances progress understanding. 

Our model demonstrates strong results on in-distribution datasets (Bridge and Droid), as well as robust generalization on out-of-distribution datasets. Notably, under one-shot conditions, the model’s powerful contextual reasoning significantly improves its ability to assess task progression. For example, in the RT1 dataset, where the tasks, scenes, and robotic arms differ greatly from those in the training data, the VOC-F1 still reaches 0.95, indicating highly accurate task process prediction. On the RoboNet dataset, which lacks language annotations and exhibits irregular temporal structure, the VOC-F1 score is 0 in the zero-shot setting, demonstrating the model’s appropriate reliance on language descriptions for understanding task progression. However, when provided with reference examples, the one-shot perfor- 

mance improves significantly, highlighting the model’s robust ability to learn and adapt from context. For the EgoDex dataset, which consists of human demonstration data, we observe that even without incorporating the Ego4D dataset, the model can still leverage context to understand task processes. After including Ego4D in training, this capability is significantly enhanced. The RoboFAC dataset contains both successful and failed task executions. Our method clearly distinguishes between these two types of trajectories, achieving a VOC-F1 of 0.89 on successful videos and only 0.44 on failed ones. This demonstrates VLAC’s strong ability to identify erroneous actions. Furthermore, for RoboFAC, the model trained with Ego4D data shows an even greater gap between successful and failed videos, indicating that human video data provides significant benefits for embodied task process understanding. The specific experimental results are shown in the Appendix D Table 5. 

We show some example results in Figure 4, where (b–h) illustrate performance on datasets across different entities, scenes, and tasks, demonstrating the strong generalization capabilities of the proposed model. More specifically, Figure 4 (b) highlights the model’s understanding of the human 

7 

**A Generalist Pair-wise Progress Critic Model for Vision-Language-Action Robots** 

_Table 1._ Performance of VLAC’s action generation across scenarios. 

|Method|Open|Cooker|Pick &|Place Bowl|Unfol|d Mat|Deskto|p Sweep|Rice T|ransfer|Aver|age|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||TP|SR|TP|SR|TP|SR|TP|SR|TP|SR|TP|SR|
|_π_0|85|85|54|40|32|0|30|10|45|30|49.2|27|
|_π_0 + Lighting Transfer|0|0|7.5|0|35.5|5|31.5|10|9|0|16.7|3|
|<br>VLAC w/o pretrain|50|50|0|0|2.5|0|0|0|56|30|21.7|16|
|<br>VLAC + FAST|80|80|**85**|**85**|72.5|55|**65**|**50**|74.5|60|75.4|66|
|VLAC|**90**|**90**|**85**|**85**|**91**|**85**|62.5|40|**84.5**|**75**|**82.5**|**75**|
|VLAC + Lighting Transfer|85|85|65|65|72.5|60|49.5|25|75.5|50|69.5|57|
|<br>VLAC + Scene Transfer|**90**|**90**|70|65|80|70|60.0|40|68|50|73.6|63|


TP: Task Progress (%); SR: Success Rate (%). Best results in **bold** . 


_Figure 5._ Experimental results of real-world reinforcement learning on four tasks. 

dataset. Figures 4 (c) and (d) show zero-shot and one-shot results for the same process, illustrating how in-context learning enhances the model’s ability to comprehend new task processes. Figures 4 (e) and (g) depict successful task processes, while Figures 4 (f) and (h) present the corresponding failed task processes, indicating that the model can clearly distinguish between successful and unsuccessful processes. These examples show our model can robustly generalize across heterogeneous embodiments, scenes, and tasks, leveraging in-context learning to accurately contrast and predict fine-grained task progress, and even differentiate subtle failure modes from successful actions. 

### **4.6. VLAC Actor Performance** 

To validate the action generation capability of VLAC, we collected 100 samples for each testing task and trained the 8B VLAC model across all tasks. Additionally, since autonomous evolution in the real world often requires exploring different environments independently, the model must possess strong generalization abilities to adapt to scene variations. To test this, we evaluated the VLAC model’s success rate under lighting disturbances and scene changes without requiring extra data collection. As shown in Table 1, the ”Lighting Transfer” scenario involved turning off fluorescent lights and using colored flashing light sources as disturbances. For the ”Scene Transfer” scenario, tests were conducted on two different workbenches located at different sites and different settings, with varying camera perspectives 

that were not precisely calibrated. The examples of training data and evaluation environments can be seen in Appendix Figure 6. The results show that _π_ 0 (Black et al., 2024), a typically state-of-the-art VLA model, attains limited gains from cross-scene small dataset fine-tuning and is less robust to perturbations. In contrast, our model demonstrates stronger robust generalization, consistently generating reasonable actions even under extreme lighting changes, making it well-suited to dynamic and unpredictable environments. 

Meanwhile, “VLAC w/o pretrain” refers to the model without task progress pretraining. The comparison between VLAC and VLAC w/o pretrain directly demonstrates that pair-wise progress understanding significantly improves action generation performance. As shown, VLAC w/o pretrain achieves only 21.7% average task progress and 16% success rate, while VLAC achieves 82.5% and 75% respectively. This substantial gap validates that progress understanding enhances the model’s ability to interpret task states and generate appropriate actions at each execution stage. Another variant, “VLAC+FAST”, utilizes the FAST action tokenizer, which requires new semantic action mapping and offers limited leverage of process understanding in semantic space, resulting in a slightly lower average success rate compared to VLAC. However, the success rate is often partially lost during transfer. To improve the success rate during real-world deployment, further autonomous learning and evolution in actual environments and tasks can be assisted with a critic. 

### **4.7. Real-world RL Results** 

In this subsection, we primarily investigate the effectiveness of real-world reinforcement learning when using VLAC as a dense reward model. Our dense reward is computed from adjacent-frame progress differences, i.e., reward = progress(t) - progress(t-1). Since a learned general reward is not perfectly reliable, we apply task-dependent postprocessing such as a threshold _τ_ so that small noisy progress fluctuations do not produce reward. In addition, VLAC is queried at each step to determine whether the task is complete; completion yields a large positive reward, while timeouts or collision-triggered stops terminate the episode with a large negative reward. Aside from timeout/collision penal- 

8 

**A Generalist Pair-wise Progress Critic Model for Vision-Language-Action Robots** 

ties, the reward is determined by VLAC. VLAC integrates naturally with PPO. VLAC outputs reward, value, and action logits, which are directly used to compute the standard value loss and policy gradient loss. The PPO hyperparameters are: importance sampling ratio 0.2, learning rate 1e-5, _λgae_ = 0 _._ 95, _γ_ = 0 _._ 8, entropy coefficient -0.05, normalize advantages True, optimizer Adam, gradient clip threshold 2, and batch size 512. As shown in Fig. 5, the initial success rate is only 20%-40%, so positive sparse rewards are very difficult to obtain. In our early trials, sparse reward training led to severe instability and even policy collapse, which is why dense progress-based reward is important in this setting. As shown in Figure 5, the success rate for each data point is calculated over 20 episodes, and our VLAC lifts the success rate from about 30% to approximately 90% within 200 real-world interaction episodes. 

### **4.8. Critic Post-training** 

Based on VLAC pretraining, we further conduct posttraining experiments on EgoDex, RH20T, and RoboFAC. We compare VLAC with the base model trained on each single dataset without large-scale pretraining. The results are reported in Table 2. Large-scale pretraining consistently improves VOC-F1 across all datasets, demonstrating the effectiveness of VLAC as a progress prediction model and its capability as a strong initialization for downstream post-training. Notably, without pretraining, the gap between VOC and VROC can be substantial, suggesting that the model does not acquire consistent forward and backward understanding of task progress. This inconsistency is particularly evident on the RoboFAC-fail split, where the model trained without pretraining achieves a much higher VROC than VOC. In contrast, VLAC pretraining significantly improves the model’s bidirectional understanding of task progress, leading to more balanced and reliable progress prediction. 

_Table 2._ Critic post-training performance. 

|Dataset|Metric|w/o Pretrain|w/ Pretrain|
|---|---|---|---|
||VOC|0.36|0.73|
|EgoDex|VROC|0.18|0.63|
||VOC-F1|0.24|**0.68**|
||VOC|0.52|0.71|
|RH20T|VROC|0.64|0.75|
||VOC-F1|0.57|**0.73**|
||VOC|0.87|0.99|
|RoboFAC-success|VROC|0.70|0.99|
||VOC-F1|0.78|**0.99**|
||VOC|0.07|0.38|
|RoboFAC-fail|VROC|0.48|0.37|
||VOC-F1|0.21|**0.37**|


### **4.9. Discussion on Noise Resistance** 

VLAC does not assume that every local trajectory segment is strictly monotonic. Real-world demonstrations may contain hesitation, retries, or temporary regressions, which can introduce local noise into progress supervision. Compared with single-frame timestamp prediction, VLAC learns pair-wise progress over multiple temporal scales, where large-span pairs are mainly dominated by macroscopic task advancement and are thus less sensitive to local noise. We further evaluate this robustness by mixing 10% failure trajectories into the RoboFAC-success training set. As shown in Table 3, the performance only drops mildly, indicating that VLAC is robust to moderate trajectory noise. 

_Table 3._ Robustness study with 10% failure trajectories. 

|Dataset|VOC|VROC|VOC-F1|
|---|---|---|---|
|RoboFAC-success|0.96|0.94|0.95|
|RoboFAC-fail|0.52|0.23|0.32|


## **5. Limitations** 

While the pair-wise sampling scheme in VLAC alleviates local noise to some extent, temporal labels still inherently rely on a monotonic progress assumption, and substantial label noise may persist in trajectories involving prolonged failures or repeated retries. Exploring non-monotonic progress annotation, such as visual semantic clustering or VLM-assisted labeling, is an important direction for future work. In addition, VOC remains tied to chronological ordering and may not fully reflect fine-grained semantic progress, especially in tasks with cyclic subtasks or long-horizon exploration. Developing more robust evaluation metrics based on key progress annotations or key-state achievement would provide a more faithful assessment of progress understanding. 

## **6. Conclusion** 

In this work, we introduced VLAC, a generalist VisionLanguage-Action-Critic model that unifies action generation and task progress understanding within a single autoregressive architecture. By leveraging a scalable pair-wise progress prediction approach, VLAC provides dense and precise feedback signals for robust self-improvement in dynamic real-world environments. Trained on large-scale, diverse datasets integrating both human and robot data, VLAC demonstrates strong generalization across tasks, scenes, and entities. Extensive experiments show that VLAC accurately discriminates between successful and failed trajectories, generates reliable actions under challenging conditions, and enables autonomous exploration through reinforcement learning integration with significant task success rate improvements. Overall, VLAC establishes a unified and scalable framework for advancing robotic perception, manipulation, and autonomous learning in complex real-world settings. 

9 

**A Generalist Pair-wise Progress Critic Model for Vision-Language-Action Robots** 

## **Acknowledgments** 

This work was supported in part by the National Natural Science Foundation of China under Grant No. 62506185, in part by Shanghai Artificial Intelligence Laboratory. 

## **Impact Statement** 

This paper presents work whose goal is to advance the field of Machine Learning. There are many potential societal consequences of our work, none which we feel must be specifically highlighted here. 

## **References** 

- Bharadhwaj, H., Vakil, J., Sharma, M., Gupta, A., Tulsiani, S., and Kumar, V. Roboagent: Generalization and efficiency in robot manipulation via semantic augmentations and action chunking. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 4788–4795. IEEE, 2024. 

- Bhateja, C., Guo, D., Ghosh, D., Singh, A., Tomar, M., Vuong, Q., Chebotar, Y., Levine, S., and Kumar, A. Robotic offline rl from internet videos via value-function pre-training. _arXiv preprint arXiv:2309.13041_ , 2023. 

- Bjorck, J., Castaneda, F., Cherniadev, N., Da, X., Ding, R.,˜ Fan, L., Fang, Y., Fox, D., Hu, F., Huang, S., et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., et al. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Dabis, J., Finn, C., Gopalakrishnan, K., Hausman, K., Herzog, A., Hsu, J., et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 

- Brooks, T., Holynski, A., and Efros, A. A. Instructpix2pix: Learning to follow image editing instructions. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pp. 18392–18402, 2023. 

- Bu, Q., Cai, J., Chen, L., Cui, X., Ding, Y., Feng, S., He, X., Huang, X., et al. Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems. In _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2025. 

- Chen, B., Xu, Z., Kirmani, S., Ichter, B., Sadigh, D., Guibas, L., and Xia, F. Spatialvlm: Endowing vision-language 

models with spatial reasoning capabilities. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 14455–14465, 2024a. 

- Chen, X., Li, G., Wang, Z., Jin, B., Qian, C., Wang, Y., Wang, H., Zhang, Y., Zhang, D., Zhang, T., Tong, H., and Ji, H. Rm-r1: Reward modeling as reasoning, 2025. URL https://arxiv.org/abs/2505.02387. 

- Chen, Z., Wang, W., Cao, Y., Liu, Y., Gao, Z., Cui, E., Zhu, J., Ye, S., Tian, H., Liu, Z., et al. Expanding performance boundaries of open-source multimodal models with model, data, and test-time scaling. _arXiv preprint arXiv:2412.05271_ , 2024b. 

- Dasari, S. and Gupta, A. Transformers for one-shot visual imitation. In _Conference on Robot Learning_ , pp. 2071– 2084. PMLR, 2021. 

- Dasari, S., Ebert, F., Tian, S., Nair, S., Bucher, B., Schmeckpeper, K., Singh, S., Levine, S., and Finn, C. Robonet: Large-scale multi-robot learning. _arXiv preprint arXiv:1910.11215_ , 2019. 

- Deng, S., Yan, M., Wei, S., Ma, H., Yang, Y., Chen, J., Zhang, Z., Yang, T., Zhang, X., Cui, H., et al. Graspvla: a grasping foundation model pre-trained on billion-scale synthetic action data. _arXiv preprint arXiv:2505.03233_ , 2025. 

- Fang, H.-S., Fang, H., Tang, Z., Liu, J., Wang, C., Wang, J., Zhu, H., and Lu, C. Rh20t: A comprehensive robotic dataset for learning diverse skills in one-shot. _arXiv preprint arXiv:2307.00595_ , 2023. 

- Herzog, A., Rao, K., Hausman, K., Lu, Y., Wohlhart, P., Yan, M., Lin, J., Arenas, M. G., Xiao, T., Kappler, D., et al. Deep rl at scale: Sorting waste in office buildings with a fleet of mobile manipulators. _arXiv preprint arXiv:2305.03270_ , 2023. 

- Hoque, R., Huang, P., Yoon, D. J., Sivapurapu, M., and Zhang, J. Egodex: Learning dexterous manipulation from large-scale egocentric video. _arXiv preprint arXiv:2505.11709_ , 2025. 

- Hu, Z., Rovinsky, A., Luo, J., Kumar, V., Gupta, A., and Levine, S. Reboot: Reuse data for bootstrapping efficient real-world dexterous manipulation. _arXiv preprint arXiv:2309.03322_ , 2023. 

- Intelligence, P., Black, K., Brown, N., Darpinian, J., Dhabalia, K., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., et al. _π_ 0. 5: a vision-language-action model with open-world generalization, 2025. _URL https://arxiv. org/abs/2504.16054_ , 1(2):3, 2025. 

10 

**A Generalist Pair-wise Progress Critic Model for Vision-Language-Action Robots** 

- Jhamtani, H. and Berg-Kirkpatrick, T. Learning to describe differences between pairs of similar images. _arXiv preprint arXiv:1808.10584_ , 2018. 

- Khazatsky, A., Pertsch, K., Nair, S., Balakrishna, A., Dasari, S., Karamcheti, S., Nasiriany, S., Srirama, M. K., Chen, L. Y., Ellis, K., et al. Droid: A large-scale in-the-wild robot manipulation dataset. _arXiv preprint arXiv:2403.12945_ , 2024. 

- Kim, M., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E., Lam, G., Sanketi, P., Vuong, Q., Kollar, T., Burchfiel, B., Tedrake, R., Sadigh, D., Levine, S., Liang, P., and Finn, C. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- Kim, M. J., Finn, C., and Liang, P. Fine-tuning visionlanguage-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 

- Kumar, N., Silver, T., McClinton, W., Zhao, L., Proulx, S., Lozano-Perez, T., Kaelbling, L. P., and Barry, J.´ Practice makes perfect: Planning to learn skill parameter policies. In _Robotics: Science and Systems (RSS)_ , 2024. 

- Li, L., Wei, Y., Xie, Z., Yang, X., Song, Y., Wang, P., An, C., Liu, T., Li, S., Lin, B. Y., et al. Vl-rewardbench: A challenging benchmark for vision-language generative reward models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 24657–24668, 2025. 

- Lin, F., Hu, Y., Sheng, P., Wen, C., You, J., and Gao, Y. Data scaling laws in imitation learning for robotic manipulation. _arXiv preprint arXiv:2410.18647_ , 2024. 

- Liu, H., Li, C., Wu, Q., and Lee, Y. J. Visual instruction tuning. _Advances in neural information processing systems_ , 36:34892–34916, 2023. 

- Lu, W., Ye, M., Ye, Z., Tao, R., Yang, S., and Zhao, B. Robofac: A comprehensive framework for robotic failure analysis and correction. _arXiv preprint arXiv:2505.12224_ , 2025. 

- Luo, J., Xu, C., Wu, J., and Levine, S. Precise and dexterous robotic manipulation via human-in-the-loop reinforcement learning. _arXiv preprint arXiv:2410.21845_ , 2024. 

- Luo, J., Xu, C., Liu, F., Tan, L., Lin, Z., Wu, J., Abbeel, P., and Levine, S. Fmb: a functional manipulation benchmark for generalizable robotic learning. _The International Journal of Robotics Research_ , 44(4):592–606, 2025. 

- Ma, Y. J., Sodhani, S., Jayaraman, D., Bastani, O., Kumar, V., and Zhang, A. Vip: Towards universal visual reward and representation via value-implicit pre-training. In 

_Deep Reinforcement Learning Workshop NeurIPS 2022_ , 2022. 

- Ma, Y. J., Kumar, V., Zhang, A., Bastani, O., and Jayaraman, D. Liv: Language-image representations and rewards for robotic control. In _International Conference on Machine Learning_ , pp. 23301–23320. PMLR, 2023. 

- Ma, Y. J., Hejna, J., Fu, C., Shah, D., Liang, J., Xu, Z., Kirmani, S., Xu, P., Driess, D., Xiao, T., et al. Vision language models are in-context value learners. In _The Thirteenth International Conference on Learning Representations_ , 2024. 

- Mendonca, R., Bahl, S., and Pathak, D. Alan: Autonomously exploring robotic agents in the real world. _arXiv preprint arXiv:2302.06604_ , 2023. 

- Mendonca, R., Panov, E., Bucher, B., Wang, J., and Pathak, D. Continuously improving mobile manipulation with autonomous real-world rl. _arXiv preprint arXiv:2409.20568_ , 2024. 

- Pei, B., Huang, Y., Xu, J., Chen, G., He, Y., Yang, L., Wang, Y., Xie, W., Qiao, Y., Wu, F., et al. Modeling fine-grained hand-object dynamics for egocentric video representation learning. _arXiv preprint arXiv:2503.00986_ , 2025. 

- Pertsch, K., Stachowicz, K., Ichter, B., Driess, D., Nair, S., Vuong, Q., Mees, O., Finn, C., and Levine, S. Fast: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 

- Sermanet, P., Xu, K., and Levine, S. Unsupervised perceptual rewards for imitation learning. _arXiv preprint arXiv:1612.06699_ , 2016. 

- Sermanet, P., Ding, T., Zhao, J., Xia, F., Dwibedi, D., Gopalakrishnan, K., Chan, C., Dulac-Arnold, G., Maddineni, S., Joshi, N. J., et al. Robovqa: Multimodal longhorizon reasoning for robotics. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 645–652. IEEE, 2024. 

- Shafiullah, N. M. M., Rai, A., Etukuru, H., Liu, Y., Misra, I., Chintala, S., and Pinto, L. On bringing robots home. _arXiv preprint arXiv:2311.16098_ , 2023. 

- Sun, H., Shen, Y., and Ton, J.-F. Rethinking reward modeling in preference-based large language model alignment. In _The Thirteenth International Conference on Learning Representations_ , 2025. 

- Team, G. R., Abeyruwan, S., Ainslie, J., Alayrac, J.-B., Arenas, M. G., Armstrong, T., Balakrishna, A., Baruch, R., Bauza, M., Blokzijl, M., et al. Gemini robotics: Bringing ai into the physical world. _arXiv preprint arXiv:2503.20020_ , 2025. 

11 

**A Generalist Pair-wise Progress Critic Model for Vision-Language-Action Robots** 

- Team, O. M., Ghosh, D., Walke, H., Pertsch, K., Black, K., Mees, O., Dasari, S., Hejna, J., Kreiman, T., Xu, C., et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

- Walke, H. R., Black, K., Zhao, T. Z., Vuong, Q., Zheng, C., Hansen-Estruch, P., He, A. W., Myers, V., Kim, M. J., Du, M., et al. Bridgedata v2: A dataset for robot learning at scale. In _Conference on Robot Learning_ , pp. 1723–1736. PMLR, 2023. 

- Xu, K., Hu, Z., Doshi, R., Rovinsky, A., Kumar, V., Gupta, A., and Levine, S. Dexterous manipulation from images: Autonomous real-world rl via substep guidance. _arXiv preprint arXiv:2212.09902_ , 2022. 

- Yang, Y., Duan, Z., Xie, T., Cao, F., Shen, P., Song, P., Jin, P., Sun, G., Xu, S., You, Y., et al. Fpc-vla: A vision-language-action framework with a supervisor for failure prediction and correction. _arXiv preprint arXiv:2509.04018_ , 2025. 

- Zhang, H., Zhou, M., Zhai, S., Sun, Y., and Xiong, H. Efficient skill discovery via regret-aware optimization. In _Forty-second International Conference on Machine Learning_ . 

- Zhao, Q., Lu, Y., Kim, M. J., Fu, Z., Zhang, Z., Wu, Y., Li, Z., Ma, Q., Han, S., Finn, C., et al. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 1702–1713, 2025. 

- Zhou, Z., Atreya, P., Lee, A., Walke, H., Mees, O., and Levine, S. Autonomous improvement of instruction following skills via foundation models. _arXiv preprint arXiv:407.20635_ , 2024. 

- Zitkovich, B., Yu, T., Xu, S., Xu, P., Xiao, T., Xia, F., Wu, J., Wohlhart, P., Welker, S., Wahid, A., et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pp. 2165–2183. PMLR, 2023. 

12 

**A Generalist Pair-wise Progress Critic Model for Vision-Language-Action Robots** 

## **A. Multi-source train datasets** 

_Table 4._ Overview of Data Mixture. 

|**Dataset Name**|**Size/samples**|**Size/h**|**Tasks**|**Mixture Weight**|
|---|---|---|---|---|
|Ego4D HOD (Pei et al., 2025)|157M|3k|TPU|14.6%|
|InstructPix2Pix (Brooks et al., 2023)|36k|-|GVL|0.4%|
|RobotVQA (Sermanet et al., 2024)|50k|-|GVL|0.6%|
|Spot the diff (Jhamtani & Berg-Kirkpatrick, 2018)|27k|-|GVL|0.3%|
|Llava (Liu et al., 2023)|633k|-|GVL|4.7%|
|SpatialQA (Chen et al., 2024a)|781k|-|GVL|5.8%|
|AGIBOT (Bu et al., 2025)|8M|73|TPU,GVL,VLA|3.0%|
|Bridge (Walke et al., 2023)|2M|135|TPU,VLA|9.1%|
|Droid (Khazatskyet al., 2024)|40M|741|TPU,VLA|30.0%|
|FMB (Luo et al., 2025)|2m|144|TPU,VLA|9.7%|
|RoboSet (Bharadhwajet al., 2024)|4m|130|TPU,VLA|17.4%|
|Self Collected|946k|18|TPU,VLA|4.4%|


**Note:** TPU = Task Progress Understanding; GVL = General Vision-Language; VLA = Vision-Language-Action. 

We collected and processed data from various sources, including human demonstration data, multiple types of robotic arm data, and VQA datasets. In addition, we collected a small portion of our data specifically for fine-tuning action representations on our robotic arm. The details of the datasets and their combinations are shown in Table 4. In total, we sampled 40 million data points (some of which include multi-turn dialogues) for training. 

## **B. Evaluation Metrics** 

Evaluation Metrics. Following GVL (Ma et al., 2024), we use Value-Order Correlation (VOC) as the primary metric for task progress understanding. VOC is the rank correlation between predicted step values and their chronological order in an expert video; higher values (-1 to 1) indicate monotonic task progression. To assess the robustness of pairwise methods, we introduce Value-Reversed-Order Correlation (VROC), computed after reversing the sequence; performance is more stable when VROC is close to VOC. We also report VOC-F1, the harmonic mean of VOC and VROC, to jointly capture forward and reversed consistency. Negative Rate (NR) is the fraction of pairwise comparisons whose predicted progress difference is negative, reflecting non-contributory or regressive actions. For action generation, following _π_ 0 _._ 5 (Intelligence et al., 2025), we measure success rate and human-rated task progress, the latter enabling finer-grained evaluation when tasks are partially completed. In real-world RL experiments, we focus on success rate, reported as the moving average over the most recent 20 episodes. 

Following the GVL (Ma et al., 2024), we use Value-Order Correlation (VOC) as the main evaluation metric for task progress understanding. This metric computes the rank correlation between the predicted values and the chronological order of the input expert video: 


VOC ranges from -1 to 1. Higher VOC scores indicate better task completion, with task progression increasing over time. A good critic model should achieve high VOC scores when evaluated on expert videos. To better evaluate pair-wise methods, we additionally construct Value-Reversed-Order Correlation (VROC). During testing, the entire sequence is reversed, so the order of pairwise frames is inverted and the predicted values should also be reversed. The closer the VROC score is to the VOC score, the better and more stable the model’s performance. We further define VOC-F1 as: 


13 

**A Generalist Pair-wise Progress Critic Model for Vision-Language-Action Robots** 

which comprehensively evaluates the correlation of task progression and temporal order in the video. If VOC _·_ VROC _<_ 0, set VOC-F1 = 0. Additionally, to evaluate the fine-grained performance of the critic model, we use Negative Rate (NR), which measures the proportion of reversed process pairs: 


where _N_ ( _ci,i_ +∆ _t <_ 0) is the number of negative evaluations, and _N_ is the total number of evaluations. This metric reflects how many actions in the video do not contribute to task progression and is also an important indicator of the quality of a trajectory. 

Following the _π_ 0 _._ 5 (Intelligence et al., 2025), we success rate and task progress as evaluation metrics for action generation. Task progress is evaluated by humans, allowing for more detailed progress assessments when the task is not fully completed, and providing a finer evaluation of the model’s manipulation ability. 

For real-world RL experiments, we mainly investigate the success rate. The success rate reflects the capability of the policy and it is evaluated the average success rate of the past 20 episodes. 

## **C. Evalauation tasks** 


_Figure 6._ Illustrations of scene/lighting transfer. 

We design five manipulation tasks in various environments as shown in Figure 6. The **Lighting Transfer** scenario involved turning off fluorescent lights and using colored flashing light sources as disturbances. For the **Scene Transfer** scenario, tests were conducted on two different workbenches located at different sites and different settings, with varying camera perspectives that were not precisely calibrated. These tasks are expected to constitute a rich and relatively complete kitchen scene from cooking food to setting up the table. In addition, these manipulation tasks are diverse from two perspectives: 1) manipulating different types of objects, i.e., rigid objects (a,b), flexible objects (c,d), and granular objects (e); 2) requires different manipulation ability, either precise goal reaching, i.e., touch/push objects (a,d), or grasp proper parts (b,c), or dynamic manipulation (e). 

**(a) Open Cooker** In this task, the robot is supposed to press the button on top of the cooker. This task is considered successful only if the cooker lid is opened. To achieve this goal, the robot should go down and press the button with proper force. If the force is too great, the cooker or the arm may be damaged; if the force is too small the cooker can not be opened. 

**(b) Pick and Place Bowl** In this task, a plate is placed on the table and a bowl is placed in a tray, and the robot is supposed to pick up the bowl and place it on the plate. The task is considered successful if the bowl is properly put on the plate. This 

14 

**A Generalist Pair-wise Progress Critic Model for Vision-Language-Action Robots** 

task requires precise and gentle gripping of the bowl’s rim and delivering it precisely to the center of the plate. 

**(c) Unfold Mat** In this task, a mat is folded in the tray, and the robot is supposed to grab the mat, lift it up, and then release it to unfold the mat. This task is considered successful if the mat unfolds well on the table. The difficulty lies in two points: 1) the robot must grab a proper part of the mat; 2) the mat must be raised high enough so that it can spread naturally, otherwise it may still be folded after falling on the table. 

**(d) Desktop Sweep Disposal** In this task, there is a white trash on the table and the robot is supposed to pick up the scrub sponge and sweep trash into the trash can. The task is considered successful if the trash is swept into the nearby can. Similar to task (A), this task requires the robot to precisely reach the trash and push it with a proper force. Too much or too little force can lead to failure. This task is also named **Desktop Sweep** for abbreviation. 

**(e) Rice Scooping and Transfer** In this task, the robot is assumed to firstly scoop a spoonful of rice from the jar, and then pour the rice into the cooker. The task is considered successful if the rice is transferred from the jar to cooker without spilling. The difficulty lies in the granular objects are not easy to be obtained and the transportation also requires the robot to be very stable. This task is also named **Rice Transfer** for abbreviation. 

## **D. Details of Experiment Results** 

Detailed results of the experiments are summarized in the Table 5 on the next page. The table includes metrics such as VOC, VROC, and NR scores. 

## **E. Datasets of General vision language understanding** 

To enhance the model’s multimodal understanding capabilities, we incorporate a series of publicly available VQA datasets, focusing on four aspects: general conversational ability, robotic understanding, spatial reasoning, and pair-wise image difference distinction. Specifically, we select the following datasets: 

LLAVA (Liu et al., 2023): This dataset includes basic multi-turn dialogues and a rich collection of VQA data, which helps maintain the model’s general multimodal understanding and conversational abilities. 

RoboVQA (Sermanet et al., 2024): This dataset contains VQA data from various robotic tasks, aimed at improving the model’s understanding of multimodal data in robotic scenarios. 

SpatialVQA (Chen et al., 2024a): This dataset provides spatial reasoning data based on RGB images, including depth estimation, object detection, and more, which strengthens the model’s ability to understand and estimate spatial information within images. 

Spot-the-diff (Jhamtani & Berg-Kirkpatrick, 2018), InstructPix2Pix (Brooks et al., 2023): These datasets consist of pair-wise image difference comparison data, designed to enhance the model’s capability to detect fine-grained differences between images, thereby supporting pair-wise progress understanding tasks. 

By leveraging these datasets, we aim to comprehensively improve the model’s multimodal reasoning and understanding capabilities across diverse application domains. 

## **F. The Use of Large Language Models (LLMs)** 

We only utilize large language models for polishing the writing. 

15 

**A Generalist Pair-wise Progress Critic Model for Vision-Language-Action Robots** 

||||NR|0.25|0.05|0.11|0.52|0.31|0.25|0.36|0.29|0.43|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||one-shot|VROC|0.86|0.99|0.79|0.81|0.55|0.78|0.69|0.92|0.57|
|C-2b|||VOC|0.80|0.98|0.79|-0.04|0.37|0.49|0.57|0.73|0.19|
|VLA|||NR|0.22|0.08|0.13|0.00|0.36|0.32|0.47|0.20|0.26|
|||zero-shot|VROC|0.49|0.95|0.72|0.00|0.43|0.40|0.59|0.69|0.34|
||||VOC|0.69|0.94|0.75|0.00|-0.04|0.03|0.00|0.46|-0.05|
||||NR|0.14|0.00|0.06|0.31|0.26|0.22|0.38|0.20|0.35|
|||one-shot|VROC|0.95|1.00|0.95|0.76|0.78|0.77|0.78|0.95|0.47|
|C-8b|||VOC|0.91|1.00|0.93|0.59|0.74|0.64|0.44|0.83|0.41|
|VLA|||NR|0.22|0.02|0.04|0.00|0.34|0.32|0.48|0.14|0.22|
|||zero-shot|VROC|0.72|0.99|0.94|0.00|0.55|0.34|0.48|0.59|-0.06|
||||VOC|0.71|0.97|0.92|0.00|0.47|0.17|0.05|0.76|0.30|
||||NR|0.11|0.00|0.06|0.23|0.28|0.21|0.32|0.21|0.32|
|o||one-shot|VROC|0.95|1.00|0.95|0.71|0.65|0.65|0.36|0.87|0.56|
|w/o Eg|||VOC|0.96|1.00|0.96|0.76|0.75|0.68|0.64|0.86|0.66|
|LAC-8b|||NR|0.19|0.05|0.09|0.50|0.39|0.34|0.29|0.26|0.34|
|V||zero-shot|VROC|0.77|0.96|0.86|0.32|0.42|0.19|-0.41|0.39|0.16|
||||VOC|0.87|0.96|0.85|0.20|0.49|0.24|0.58|0.700|0.45|
|VLAC-8b|w/o pair-wise||VOC|0.44|0.67|0.50|0.03|0.26|0.15|0.05|0.57|0.18|
|GVL|(Gemini-1.5-Pro)||VOC|0.74|0.51|-0.01|-0.85|0.53|none|none|none|none|
|||Dataset||RT1|Bridge|DROID|RoboNet|Dobb-E|RH20T|EgoDex|RoboFAC-success|RoboFAC-fail|


16 

