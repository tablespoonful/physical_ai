---
title: "AtomicVLA: Unlocking the Potential of Atomic Skill Learning in Robots"
date: "2026-03-08"
authors: "Likui Zhang; Tao Tang; Zhihao Zhan; Xiuwei Chen; Zisheng Chen; Jianhua Han"
venue: "CVPR 2026"
url: https://arxiv.org/abs/2603.07648
pdf: https://arxiv.org/pdf/2603.07648
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.07648)** / [論文ページ](https://arxiv.org/abs/2603.07648)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **AtomicVLA: Unlocking the Potential of Atomic Skill Learning in Robots** 

- Likui Zhang<sup>1</sup> Tao Tang<sup>1</sup> Zhihao Zhan<sup>1</sup> Xiuwei Chen<sup>1</sup> Zisheng Chen<sup>1</sup> Jianhua Han<sup>3</sup> Jiangtong Zhu<sup>3</sup> Pei Xu<sup>3</sup> Hang Xu<sup>3</sup> Hefeng Wu<sup>1</sup> Liang Lin<sup>1†</sup> Xiaodan Liang<sup>1</sup><sup>_,_2†</sup> 1Sun Yat-sen University 2Peng Cheng Laboratory 3Yinwang Intelligent Technology Co. Ltd. `zhanglk9` @ `mail2` _._ `sysu` _._ `edu` _._ `cn` 

## **Abstract** 

_Recent advances in Visual-Language-Action (VLA) models have shown promising potential for robotic manipulation tasks. However, real-world robotic tasks often involve longhorizon, multi-step problem-solving and require generalization for continual skill acquisition, extending beyond single actions or skills. These challenges present significant barriers for existing VLA models, which use monolithic action decoders trained on aggregated data, resulting in poor scalability. To address these challenges, we propose AtomicVLA, a unified planning-and-execution framework that jointly generates task-level plans, atomic skill abstractions, and fine-grained actions. AtomicVLA constructs a scalable atomic skill library through a Skill-Guided Mixture-ofExperts (SG-MoE), where each expert specializes in mastering generic yet precise atomic skills. Furthermore, we introduce a flexible routing encoder that automatically assigns dedicated atomic experts to new skills, enabling continual learning. We validate our approach through extensive experiments. In simulation, AtomicVLA outperforms π_ 0 _by 2.4% on LIBERO, 10% on LIBERO-LONG, and outperforms π_ 0 _and π_ 0 _._ 5 _by 0.22 and 0.25 in average task length on CALVIN. Additionally, our AtomicVLA consistently surpasses baselines by 18.3% and 21% in real-world long-horizon tasks and continual learning. These results highlight the effectiveness of atomic skill abstraction and dynamic expert composition for long-horizon and lifelong robotic tasks. The project page is here._ 

## **1. Introduction** 

Building on powerful Vision-Language Models [2, 6, 9, 19, 34, 44], Vision-Language-Action (VLA) models [3, 4, 20, 27] unify visual perception, language understanding, and action generation into a single framework, achieving significant advances in robotic manipulation tasks. Despite this progress, current VLA models still face challenges in real- 


Figure 1. **Overview of AtomicVLA.** Unlike previous VLA models with a single action head, which suffer from limited scalability and severe interference among mixed skills, AtomicVLA employs a SG-MoE architecture to build a scalable skill expert library. By unifying task planning and action execution within this framework, it achieves strong performance on long-horizon and continual learning tasks in both simulation and real-world settings. 

world deployments for complex long-horizon tasks and the continual acquisition of new skills. 

To overcome these challenges, a robotic model must support both high-level reasoning and fine-grained action generation, while enabling scalable continual learning. To support high-level reasoning and task planning, some existing approaches employ a two-stage architecture [1, 13, 18, 31, 37, 40], where a pretrained vision-language model (VLM) serves as a high-level planner to generate subtask instructions, while a separate VLA-based controller translates these instructions into executable actions. However, recent studies [23, 52, 53] suggest that modular decoupling leads to a lack of mutual awareness between the planner and controller, causing suboptimal task coordination. Moreover, in real-world applications, this can result in the generation of outdated or irrelevant instructions due to system delays. In addition, most existing VLA models rely on a single action-decoding module, limiting their scalability. Incrementally learning new skills requires fine-tuning 

> _†_ Co-corresponding author 

20743 

existing models, which demands substantial computational resources and large datasets. Given the current scarcity of robot data, fully leveraging well-pretrained VLA model weights is essential during the scaling process. Moreover, when learning new skills incrementally, these models often interfere with previously acquired skills, leading to catastrophic forgetting and thereby hindering the lifelong learning capabilities. 

To this end, we propose AtomicVLA, as illustrated in Fig. 1, an end-to-end framework that unifies task planning and action execution by adaptively generating either natural language instructions or latent actions. AtomicVLA first infers the current execution state from the input observations and dynamically activates either its thinking module or its acting module. At task initialization or during transitions between sub-skills, the model triggers thinking to produce a task chain, create a task chain plan based on the current state, and outputs atomic skill abstractions. In the acting execution phase, it dynamically selects the corresponding skill-specific expert based on the most recent skill abstraction to generate precise robot control signals. Furthermore, to enable AtomicVLA with continual learning capability, we introduce a Skill-Guided Mixture-of-Experts (SG-MoE) architecture that constructs a scalable library of atomic skills. This library comprises a shared expert and multiple dedicated skill experts, each focusing on mastering a specific atomic skill. Through a well-designed skill encoding mechanism and an extensible routing encoder, each atomic skill abstraction is mapped to a fixed embedding vector, allowing the routing module to rapidly adapt to new skills even as the skill library grows. When a new skill is introduced, only the corresponding expert and associated routing parameters need to be trained, leaving existing experts unchanged. This effectively prevents catastrophic forgetting, ensuring efficient and stable lifelong skill growth. 

We conducted extensive experiments to validate the effectiveness of AtomicVLA both in simulation platforms and real-world robots. In the LIBERO [25] benchmark, AtomicVLA achieved an average performance improvement of 2.4% over baseline models, with a notable 10% improvement on the LIBERO-LONG. On the CALVIN [29] benchmark, specifically on the task ABC-D training set, our method increased the average successful execution length by 0.22 and 0.25. Furthermore, we performed long-horizon task execution and continual learning experiments on a realworld Franka robot, where we observed performance improvements of 18.3% and 21%, respectively. These results further validate the potential of AtomicVLA’s proposed atomic skill dynamic combination mechanism in supporting long-term task completion and lifelong skill accumulation. Overall, our contributions are as follows: 

- We introduce AtomicVLA, an end-to-end framework that unifies task planning and action execution for long- 

horizon tasks and continual skill expansion. 

- We propose a Skill-Guided Mixture-of-Experts (SGMoE) architecture and a scalable skill router for building a library of atomic skills. 

- We validate the effectiveness of AtomicVLA through extensive experiments conducted in both simulated environments and real-world robots. 

## **2. Related Work** 

### **2.1. Vision-Language-Action Models** 

Vision-Language Action Models (VLAs) have emerged as a dominant paradigm in general-purpose robotic learning by leveraging the rich semantic priors and strong crossmodal generalization of large-scale Vision-Language Models (VLMs) pretrained on internet-scale data. Recent works [3, 4, 16, 20, 22, 32, 49, 59] fine-tune VLMs [2, 9, 19, 44] on diverse robotic datasets to directly map visual and linguistic inputs to motor actions, demonstrating impressive generalization to novel environments and tasks. 

However, constrained to some extent by the VLM’s inherent hierarchical planning capability, most current VLAs exhibit limitations in structured task decomposition and long-horizon task planning. Several approaches introduce external high-level planners [10, 14, 37, 40, 55, 60] that decompose long-horizon tasks into subgoals, which are then executed by a separate low-level policy. However, modular approaches often fail to unify action with vision and language in a shared latent space, resulting in misaligned decisions that compound loss. To address this problem, recent work [5, 11, 23, 26, 52, 53] propose integrated frameworks that jointly perform hierarchical reasoning and action generation within a unified model. Our work aligns with this direction: we adopt a Think-Act unified architecture, where a VLM simultaneously performs high-level task planning and atomic action abstraction, thereby directly guiding a specialized action expert to produce executable, temporally coherent action sequences. 

### **2.2. Multimodal Mixture-of-Experts** 

The Sparse Mixture-of-Experts (MoE) architecture has become a mainstream approach for scaling large language models (LLMs). By replacing the standard feed-forward layers with expert modules [8, 17], MoE improves task specialization and representation capability through conditional computation, while maintaining inference efficiency. In the field of autonomous driving, models such as [50, 54] design specialized MoE architectures tailored to multi-view observations and action skills, improving both trajectory prediction accuracy and inference efficiency. Similarly, in robotics, some works [15, 35, 45, 51, 57, 61] employ MoE to tackle task heterogeneity and long-tailed data distributions. While these approaches demonstrate the utility of 

20744 


Figure 2. **(a) AtomicVLA Pipline.** AtomicVLA is a framework that unifies task planning and action execution. The VLM adaptively predicts atomic skill abstraction and latent action. Action Decoder in the SG-MoE architecture receives both the latent action and the newly inferred atomic skill abstraction, and generates fine grained motor actions. **(b) Skill-Guided Mixture of Experts.** SG-MoE includes a skill router, a shared expert, and multiple atomic-skill experts. The router selects the top skill expert based on the atomic skill, and the action token is processed by both the activated skill expert and the shared expert. **(c) Continual Learning with Skill Expansion.** New skills are added by training only the new expert and extending the router. **(d) Task Planning Embodied Data Generation.** High-quality embodied reasoning data are generated using principal-axis analysis with InternVideo2.5 [46] model. 

MoE for representation learning, they largely treat experts as interchangeable components within fixed architectural slots, without explicitly modeling structured, composable behaviors. In contrast, we reinterpret the MoE paradigm through the lens of skill modularity: we construct a dynamically scalable atomic skill library, where each expert corresponds to a semantically meaningful, reusable action primitive. Integrated with a pre-trained VLM that encodes atomic action abstractions, our approach enables a universal VLA model capable of both fine-grained skill decomposition and coherent long-horizon task composition. 

### **2.3. Continual Learning with Skill Abstractions** 

To adapt to new tasks that emerge in dynamic environments, continual learning has become essential for developing general-purpose intelligent agents. Prior studies [7, 12, 28, 38, 39, 43] have leveraged unsupervised learning and hierarchical imitation learning to enable autonomous skill discovery from continuous data, which allows an agent to expand its skill set over time. Furthermore, to learn from streaming data without suffering from catastrophic forgetting, several approaches [21, 30, 36, 56] introduce latent action representations that abstract different skills and preserve previously acquired capabilities without relying on experience replay. Current VLA Models primarily focus on learning generalizable skills from broad pre- 

training, while dedicated investigations into continual learning remain limited. Although many VLAs [47, 48] have explored various motion decoding methods, such as diffusion models [27], flow matching [24], and discrete encoding [30, 42], they all use a single decoder. Their core focus is on the model’s accuracy on the current task rather than its scalability. We construct an expandable library of skill experts by using atomic units of robotic behavior together with a specialized routing module, which enhances the scalability of such models in skill acquisition. 

## **3. Method** 

### **3.1. Overview** 

As illustrated in Fig. 2, AtomicVLA integrates the thinking modality for task planning and the acting modality for action execution within a unified framework (Sec. 3.2). Building upon this architecture, we develop a skill-guided library of atomic action experts (Sec. 3.3) based on pi0 and introduce an extensible skill router that facilitates continual learning of new skills (Sec. 3.4) in real-world environments. To further ensure the generation of high-quality task planning data, we introduce an embodiment data generation pipeline (Sec. 3.5) grounded in principal axis analysis, which provides structured and consistent data to support effective task planning and execution. 

20745 

|**Alg**|**orithm 1**Inference Pipeline of AtomicVLA|
|---|---|
|**Re**<br>|**quire:** VLA model_πθ_, language instruction_ℓ_<br><br>|
|1:|_t ←_0_, O_<sup>1:</sup><sup>_n_</sup><br>t<br>_←_initial image_, Atomic ←_none|
|2:|**while**“task not done”**do**<br>|
|3:|_M ∼πθ._PREDICT(_· | O_<sup>1:</sup><sup>_n_</sup><br>_t_<br>_, ℓ_)|
|4:|**if**_M_ =[think]**then**<br>|
|5:|[_C_0_−k, Ct, σ_]_∼πθ._THINKING(_· | O_<sup>1:</sup><sup>_n_</sup><br>_t_<br>_, ℓ_)|
|6:|_Atomic ←σ_|
|7:|**else if**_M_ =[act]**then**|
|8:|_wk ∼Router_(_embeded_(_Atomic_))<br>|
|9:|_At ∼πθ._ACTING(_· | O_<sup>1:</sup><sup>_n_</sup><br>_t_<br>_, ℓ, st, wk_)|
|10:|Execute_At_|
|11:|**end if**|
|12:|_t ←t_+ 1|
|13:|**end while**|


### **3.2. Unified Task Planning and Action Execution** 

**Problem formulation.** The central problem addressed in this section is to design a robot policy that simultaneously possesses task planning (thinking) and action execution (acting) capabilities, and can autonomously decide its output modality based on the current states. Specifically, in thinking mode, the policy takes multiple cameras observations _Ot_<sup>1:</sup><sup>_n_</sup> and a language instruction _ℓ_ as input and outputs a high-level task plan [ _C_ 0 _−k, Ct, σ_ ] in textual form. In contrast, in acting mode, the policy generates a concrete action command conditioned on the robot’s proprioceptive state _St_ and the most recent planning output _σ_ . 

**Adaptive thinking and acting.** To enable seamless switching between the two output modalities, we introduce two special output tokens: [ _think_ ] and [ _act_ ]. As illustrated in Algorithm 1, given the current visual observations _Ot_<sup>1:</sup><sup>_n_</sup> and task instruction _ℓ_ , the model first predicts identifier either [ _think_ ] or [ _act_ ]. When the model outputs [ _think_ ], it enters the thinking mode, in which it generates a task chain _C_ 0 _−k_ that outlines the high-level plan, tracks the current execution progress _Ct_ , and specifies the atomic skill abstraction _σ_ to be performed. Typically, this mode is activated only at key time steps, such as task initiation or during the transition between sub-skills. Conversely, when [ _act_ ] is predicted, the model switches to acting mode, where it produces a lowlevel action chunk _At_ based on the atomic skill abstract _σ_ obtained in the most recent [ _think_ ] step and the current proprioceptive state. 

### **3.3. Skill-guided Mixture of Experts Architecture** 

**Atomic skill abstract embedding.** To enhance the representational distinctiveness among atomic skills, we adopt an encoding strategy inspired by noise scheduling in diffusionbased denoising models. Specifically, each atomic skill abstract is mapped to a scalar noise level _σ ∈_ [0 _,_ 100], which is then embedded into a high-dimensional vector. This con- 

tinuous and structured embedding space facilitates semantic separation across skills and enables robust routing to the corresponding skill-specific experts. 


where _σ_ denotes the assigned noise level for the skill, and _E_ ( _·_ ) is a embedding function that maps the normalized scalar to a high-dimensional embedding vector _Zσ_ . 

**Skill-Guided dynamic routing.** We build upon the _π_ 0 vision-language-action (VLA) foundation model, a generalist robotic policy pretrained on large-scale multimodal data, and extend it with an atomic action abstraction-guided Mixture-of-Experts (MoE) architecture to construct a scalable atomic skill library. As illustrated in Fig. 2(b), our skill library consists of three key components: (1) a skill router, (2) a shared expert that maintains the pre-trained action generation capabilities of _π_ 0, and (3) multiple atomic skill experts, each specialized in executing a distinct atomic skill. 

To maintain the specialized skills of individual atomic experts, we first derive an atomic action abstraction from the high-level task instruction and environmental observation via thinking pipeline. This abstraction is deterministically mapped to a fixed high-dimensional embedding _Zσ ∈_ R<sup>_d_</sup> , which serves as the conditioning signal for the skill router. The router computes a probability distribution over experts as: 


where _K_ denotes the number of atomic skill experts. We adopt a sparse activation strategy: only the top-scoring expert is selected for action generation. Let _k_ be the index of the activated expert, and let its raw score be _wk_ . The final action chunk _At_ is computed as a weighted combination of the shared expert and the selected atomic expert: 


where **x** _t_ denotes the current multimodal input [ _Ot_<sup>1:</sup><sup>_n_</sup> _, ℓ, st_ ]. This architecture enables the system to retain the strong generalization capability of _π_ 0 while achieving high-fidelity execution of specific skills through dedicated experts. 

### **3.4. Continual Learning with Skill Expansion** 

In real-world deployments, robots inevitably encounter new tasks that require atomic skills not previously observed during training. Directly incorporating these novel skills into the existing skill library and retraining the entire model often leads to catastrophic forgetting, significantly impairing the performance of previously learned skills. 

AtomicVLA adopts a modular skill-expert mechanism, which enables continual scalability of the skill library. Specifically, as introduced in Sec. 3.3, each atomic skill is mapped to a fixed high-dimensional embedding vector _Zσ_ , providing an explicit semantic abstraction of the skill. This 

20746 


Figure 3. **Inference Example of AtomicVLA.** We visualize two tasks from LIBERO-LONG. For each task, the top row shows the task progression, and the bottom row shows AtomicVLA’s inferred outputs. Gray blocks denote Thinking, while colored blocks indicate Acting, with colors corresponding to the activated skill experts. The left row shows the initial task state (top) and the skill-expert activation during inference (bottom). 

design inherently enables incremental learning in lifelong settings: when a new atomic skill is introduced, it is sufficient to add a corresponding expert module to the existing architecture and extend the routing network. 

To ensure smooth integration, the expanded router is initialized by copying weights from the original router, while the new routing branch is initialized with small random values. This initialization strategy allows the model to adapt to the enlarged skill set with minimal fine-tuning, while preserving the performance of previously acquired skills. Consequently, AtomicVLA achieves efficient and interferencefree expansion of its atomic skill library, a crucial requirement for scalable lifelong robotic learning. 

### **3.5. Task Planning Embodied Data Generation** 

To obtain accurate and reliable annotations of atomic actions, we propose a trajectory-based atomic decomposition method grounded in principal-axis analysis. Traditional approaches often rely on Vision-Language Models for video understanding or optical flow-based motion features to segment action sequences. However, these methods are prone to ambiguity and noise, which typically require extensive manual post-processing to correct and refine the results. 

In contrast, our method analyzes the key kinematic dimensions of the end-effector trajectory, including translational displacements (∆ _x,_ ∆ _y,_ ∆ _z_ ), rotational changes (∆roll _,_ ∆pitch _,_ ∆yaw), and binary gripper states, to achieve coarse but semantically meaningful segmentation of atomic actions. Specifically, for each short motion chunk, we identify the dominant mode of motion by comparing the magnitudes of translational and rotational components. Concurrently, gripper state transitions are tracked to infer action se- 

mantics and execution progress. For instance, a continuous decrease in the _z_ -coordinate combined with a gripper closing event indicates a “pick” action, whereas limited translational movement accompanied by significant rotation with a closed gripper is classified as a “turn” operation. This physics-informed decomposition produces temporally precise and semantically interpretable boundaries for atomic actions, substantially reducing the reliance on manual refinement. 

Based on the output of principal-axis analysis, we decompose a full task trajectory into a temporally ordered sequence of atomic action segments. To refine and validate the semantic labels of these segments, we employ the InternVideo2.5 model [46] to interpret the corresponding video clips, enabling automatic correction and enrichment of the initial atomic action annotations. By aligning these refined labels with the full trajectory, we construct a structured reasoning chain comprising the sequence of executed atomic actions and the associated high-level plan for subsequent steps. This integrated representation not only improves the fidelity of atomic action annotation but also provides interpretable, step-by-step execution guidance that supports robust long-horizon task planning and decision-making. 

## **4. Experiments** 

### **4.1. Experiments Setup** 

**Benchmarks.** We evaluate AtomicVLA and AtomicVLA* on two widely adopted robotic manipulation benchmarks: LIBERO [25] and CALVIN [29]. For the LIBERO benchmark, we assess model performance across all four task suites. To further examine the model’s capability in long- 

20747 

Table 1. **Comparison of Different Methods on LIBERO Benchmark(%).** 

|**Method**|**Spatial**|**Object**|**Goal**|**Long**|**Avg.**|
|---|---|---|---|---|---|
|Octo [41]|78.9|85.7|84.6|51.1|75.1|
|OpenVLA [20]|84.9|88.4|79.2|53.7|76.5|
|SpatialVLA [33]|88.2|89.9|78.6|55.5|78.1|
|CoT-VLA [58]|87.5|91.6|87.6|69.0|81.1|
|_π_0 [3]|96.4|**98.8**|95.8|85.2|94.2|
|_π_0_._5 [16]|**98.8**|98.2|**98.0**|92.4|96.9|
|**AtomicVLA (Ours)**|96.8|98.0|96.4|**95.2**|96.6|
|**AtomicVLA* (Ours)**|**98.8**|**98.8**|97.2|**96.2**|**97.8**|


Table 2. **Long-horizon Robotic Manipulation Evaluation on CALVIN Benchmark(%).** 

|**Method**|**Task**||**Tasks C**|**ompleted i**|**n a Row**||**Avg. Len**_↑_|
|---|---|---|---|---|---|---|---|
|||1|2|3|4|5||
|_π_0 [3]|ABC_→_D|94.3|87.0|77.9|68.5|59.4|3.87|
|_π_0_._5 [16]|ABC_→_D|91.9|84.6|79.4|75.5|71.0|4.02|
|**AtomicVLA (Ours)**|ABC_→_D|95.0|87.8|**81.9**|**75.0**|**69.1**|**4.09**|
|**AtomicVLA* (Ours)**|ABC_→_D|94.1|88.7|**85.2**|**81.7**|**77.6**|**4.27**|


horizon planning and compositional generalization, we perform additional experiments on the CALVIN benchmark using the ABC-D split. 

**Training setup.** We build AtomicVLA and AtomicVLA* upon the pretrained _π_ 0 and _π_ 0 _._ 5 foundation model. The models were trained using robot trajectory data formatted according to the Lerobot standard. We use 5 skill experts for both the LIBERO benchmark suite and real-world robot experiments. For the CALVIN benchmark, we employ 8 skill experts to cover its broader task vocabulary. Further implementation details are provided in the Appendix. 

**Real-world robot.** We conduct real-world experiments using a Franka robotic arm, which includes three long-horizon tasks and five different types of short tasks. For each shorthorizon task, we collect 50 trajectories, while each longhorizon task contains 100 trajectories, resulting in a total of 550 real-world demonstration trajectories. The five short tasks cover different categories of manipulation actions, including Grasp block, Stack blocks, Close microwave, Press button, and Open drawer. The long-horizon tasks include: 

- **Objects in plate** : place all blocks on the table into a green plate. 

- **Object into drawer** : open the top drawer and place the block inside. 

- **Object into microwave** : place the plate into the microwave and close the door. 

### **4.2. Results on Simulation** 

**Results on LIBERO.** As shown in Tab. 1, AtomicVLA achieves an average success rate of 96.6% across the four 


Figure 4. **Error Recovery Capability Demonstration.** When encountering a skill execution failure, AtomicVLA automatically assesses the progress and re-executes the current skill. 

suites, outperforming the strong baseline by 2.4%. Notably, on the most challenging LIBERO-LONG suite, AtomicVLA attains a success rate of 95.2%, representing a 10% improvement over the _π_ 0. Furthermore, AtomicVLA* demonstrates even stronger performance, reaching an average success rate of 97.8% and 96.2% on LIBERO-LONG. 

This superior performance can be attributed to the core mechanism of AtomicVLA, which explicitly decomposes long-horizon tasks into a sequence of atomic skill abstractions and dynamically activates the corresponding skill experts. The “decompose–plan–compose” paradigm naturally aligns with the structure of multi-stage robotic tasks. As illustrated in Fig. 3, at the beginning of each atomic subtask, AtomicVLA generates a precise skill-level action abstraction to guide the selection of the appropriate expert. Importantly, when an execution failure occurs, for example, the butter is grasped but subsequently dropped as illustrated in Fig. 4, AtomicVLA can detect the task anomaly, regenerate a new atomic skill abstraction, and recover from the error to 

20748 


Figure 5. Demonstrations show the execution process of AtomicVLA* (second row) and baselines _π_ 0 _._ 5 (first row). 

Table 3. **Long-horizon Multi-task Experiments(%).** InP, IntoD, and IntoM stand for Objects in plate, Object into drawer, Object into microwave, respectively. 

|**Method**|**InP**|**IntoD**|**IntoM**|**Avg.**|∆**Avg.**|
|---|---|---|---|---|---|
|_π_0 [3]|45|55|10|36.7|–|
|_π_0_._5 [16]|65|35|35|45|–|
|**AtomicVLA**|65|**60**|45|56.7|+20_._0_↑_|
|**AtomicVLA***|**75**|**60**|**55**|**63.3**|+18_._3_↑_|


resume task execution. 

**Results on Calvin.** As shown in Tab. 2, AtomicVLA achieves an average task length of 4.09, outperforming the _π_ 0 baseline by 0.22, while AtomicVLA* reaches an average task length of 4.27, outperforming the _π_ 0 _._ 5 baseline by 0.25. Notably, AtomicVLA* demonstrates superior overall task completion rate with relative improvements of 5.8%, 6.2%, and 6.6% on the last three stages of the evaluation sequence. These results indicate that AtomicVLA is particularly effective in handling temporally extended and sequential manipulation tasks. 

As illustrated in Fig. 4, we also observe that AtomicVLA exhibits a capability for error recovery in experiments. However, due to the evaluation constraints of the CALVIN benchmark, successful recoveries after failures are not considered valid completions, which prevents subsequent tasks from being executed. As a result, the reported performance metrics may slightly underestimate the true capability of the model. 

### **4.3. Results on Real-world Robot** 

**Long-horizon Tasks.** We perform mixed training using the collected data from three long-horizon tasks. As shown in Tab. 3, AtomicVLA and AtomicVLA* outperform the baseline model by 20% and 18.3%, respectively. As illustrated in Fig. 5, we present two representative long-horizon tasks. AtomicVLA* reliably completes the experimental configurations that _π_ 0 _._ 5 fails to accomplish, and this advantage becomes more evident in tasks involving door-closing operations. Building on this observation, AtomicVLA* demonstrates stronger robustness and execution stability across complex manipulation sequences. 

Previous real-world studies on robotic manipulation typically focus on training and evaluating a single specific task, while joint training across multiple heterogeneous tasks has been relatively uncommon. Our observations indicate that combining tasks with large differences can lead to mutual interference, which in turn limits overall performance. This effect becomes particularly pronounced in tasks that involve significant changes in gripper states across different execution stages. For instance, in the “Object into drawer” task, the drawer-opening subtask does not require gripper closure, which can adversely affect the model’s behavior on other grasping-related tasks, resulting in unintended gripper opening or closing actions, as illustrated in Fig. 6. By constructing an explicit library of atomic skills, AtomicVLA effectively mitigates such cross-task interference. Each skill precisely activates its corresponding expert to execute the required operation, which substantially alleviates the interference between heterogeneous skills and overcomes the performance bottleneck of mixed multi-task training. 

**Continual learning skills.** To evaluate the effectiveness of our proposed lifelong skill expansion mechanism in realworld scenarios, we conduct training and evaluation on short-horizon task dataset consisting of five diverse manipulation categories. In this experiment, the “open” operation is treated as a new atomic skill, which is introduced as an additional capability during the continual learning phase after the initial training stage. Specifically, we first perform mixed training on four short-horizon tasks and train the “open” skill independently on top of the pretrained model. 

Learning a new skill often causes substantial interference with previously acquired abilities in conventional baseline models, leading to noticeable performance degradation. As illustrated in Fig. 6, in a case that was originally expected to succeed, the task could not be completed after continual learning. The gripper failed to close promptly after reaching the target position. As shown in Tab. 4, the average success rate of _π_ 0 _._ 5 decreases by approximately 15%, with the stack task exhibiting the most severe interference, showing a 20% decrease. In contrast, AtomicVLA* maintains stable performance after continual learning. Owing to its structured skill library management, the previously learned skills remain largely unaffected. Moreover, under the same 

20749 

Table 4. **Continual Learning with Skill Expansion(%).** ∆Avg. represents the average performance change on the four base tasks after learning new skills compared with their performance before learning.CL is continual learning 

|**Method**|**Grasp**|**Stack**|**Close**|**Press**|**Open (new)**|**Avg.**|∆**Avg.**|
|---|---|---|---|---|---|---|---|
|_π_0_._5 [16]|85|65|70|90|-|77.5|–|
|_π_0_._5 [16] (CL)|70|45|60|75|55|61|-15_._0_↓_|
|**AtomicVLA***|**95**|**80**|**70**|**100**|-|**86.3**|–|
|**AtomicVLA***(CL)|90|**80**|**80**|**100**|**70**|**82**|_−_1_._3_↓_|


Figure 6. **Mixed-Training Skill Interference and ContinualLearning Degradation.** The top two rows illustrate skill interference in long-horizon tasks: the first shows successful single-skill executions, while the second shows failures after mixed training. The bottom two rows show degradation after continual learning: the first row presents the performance of _π_ 0 _._ 5 before learning new skills, and the second shows its performance afterward. Red and green boxes highlight the key differences. 

Table 5. **Results on LIBERO Benchmark(%).** 

|**Method**|**LIBERO-LONG**|
|---|---|
|_π_0 [3]|85.2|
|+ MoE|88.6|
|+ MoDE [35]|89.5|
|**+ SG-MoE (Ours)**|**95.2**|


tively small. This is primarily because both approaches rely on token-level expert routing, where the improvements largely stem from load balancing that distributes tokens across experts. As a result, each expert still learns a mixture of skills without clear specialization. In contrast, SG-MoE employs atomic skill abstractions as the routing criterion, which ensures that all tokens associated with a specific skill stage are consistently processed by the corresponding expert network. Consequently, each expert focuses on a single skill with a similar action distribution, reducing interference among different skills. Moreover, this notable performance gain demonstrates that routing experts based on semantically meaningful atomic skills, rather than on individual action tokens or denoising steps, leads to more coherent and efficient skill execution in long-horizon tasks. 

## **5. Conclusion** 

number of training steps, AtomicVLA* acquires new skills more efficiently and achieves an overall improvement of 21% across all five tasks compared to _π_ 0 _._ 5. These findings highlight our effectiveness for continual learning. 

### **4.4. Ablation Study** 

We conduct ablation experiments on the LIBERO-LONG benchmark to evaluate the effectiveness of our skill-aware routing mechanism. Specifically, we compare AtomicVLA against three baselines: (i) a non-MoE _π_ 0-based baseline, (ii) a standard token-level Mixture-of-Experts (MoE) that selects experts independently for each action token, and (iii) a variant adapted from MoDE [35], which conditions expert selection on the denoising timestep _t_ (i.e., using _t_ as the routing signal). 

As shown in Tab. 5, AtomicVLA achieves a success rate of 95.2%, outperforming the MoE baseline by 6.6% and the timestep-conditioned MoDE variant by 5.7%. The experimental results indicate that the performance gap between the MoE-based and MoDE-based methods is rela- 

In this paper, we introduce AtomicVLA, an end-to-end framework that unifies task planning and action execution for long-horizon tasks and continual skill expansion. We design a unified architecture capable of adaptively deciding task plans and generating latent action outputs, and construct an atomic skill-guided expert library based on our proposed SG-MoE architecture and the specialized skill router. AtomicVLA is inherently scalable: when learning new skills, it only requires extending the skill router and adding the corresponding new skill experts to rapidly acquire the novel capabilities. We validate AtomicVLA in both simulated and real-world robotic environments, demonstrating its superior performance in long-horizon tasks and continual learning. Notably, it effectively mitigates skill interference arising from joint training and alleviates knowledge forgetting and performance degradation during continual skill acquisition, highlighting its significant potential for scalable continual learning in visionlanguage-action models. 

20750 

## **Acknowledgments** 

This work was supported by the National Key Research and Development Program of China (2024YFE0203100), the Scientific Research Innovation Capability Support Project for Young Faculty (No. ZYGXQNJSKYCXNLZCXMI28), the National Natural Science Foundation of China (NSFC) under Grants No. 62476293, No. 62372482 and No. 62272494, and in part by the Major Key Project of PCL (Grant No. PCL2025A17) and the General Embodied AI Center of Sun Yat-sen University. 

## **References** 

- [1] Michael Ahn, Anthony Brohan, Noah Brown, Yevgen Chebotar, Omar Cortes, Byron David, Chelsea Finn, Chuyuan Fu, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Daniel Ho, Jasmine Hsu, Julian Ibarz, Brian Ichter, Alex Irpan, Eric Jang, Rosario Jauregui Ruano, Kyle Jeffrey, Sally Jesmonth, Nikhil J Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Kuang-Huei Lee, Sergey Levine, Yao Lu, Linda Luu, Carolina Parada, Peter Pastor, Jornell Quiambao, Kanishka Rao, Jarek Rettinghouse, Diego Reyes, Pierre Sermanet, Nicolas Sievers, Clayton Tan, Alexander Toshev, Vincent Vanhoucke, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, Mengyuan Yan, and Andy Zeng. Do as i can, not as i say: Grounding language in robotic affordances, 2022. 1 

- [2] Lucas Beyer, Andreas Steiner, Andr´e Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, Thomas Unterthiner, Daniel Keysers, Skanda Koppula, Fangyu Liu, Adam Grycner, Alexey Gritsenko, Neil Houlsby, Manoj Kumar, Keran Rong, Julian Eisenschlos, Rishabh Kabra, Matthias Bauer, Matko Boˇsnjak, Xi Chen, Matthias Minderer, Paul Voigtlaender, Ioana Bica, Ivana Balazevic, Joan Puigcerver, Pinelopi Papalampidi, Olivier Henaff, Xi Xiong, Radu Soricut, Jeremiah Harmsen, and Xiaohua Zhai. Paligemma: A versatile 3b vlm for transfer, 2024. 1, 2 

- [3] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _π_ 0: A vision-language-action flow model for general robot control, 2024. 1, 2, 6, 7, 8 

- [4] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, Pete Florence, Chuyuan Fu, Montse Gonzalez Arenas, Keerthana Gopalakrishnan, Kehang Han, Karol Hausman, Alexander Herzog, Jasmine Hsu, Brian Ichter, Alex Irpan, Nikhil Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Isabel Leal, Lisa Lee, Tsang-Wei Edward Lee, Sergey Levine, Yao Lu, Henryk Michalewski, Igor Mordatch, Karl Pertsch, Kanishka Rao, Krista Reymann, Michael Ryoo, Grecia Salazar, Pannag Sanketi, Pierre Sermanet, Jaspiar Singh, Anikait 

Singh, Radu Soricut, Huong Tran, Vincent Vanhoucke, Quan Vuong, Ayzaan Wahid, Stefan Welker, Paul Wohlhart, Jialin Wu, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, Tianhe Yu, and Brianna Zitkovich. Rt-2: Vision-language-action models transfer web knowledge to robotic control, 2023. 1, 2 

- [5] Hao Chen, Jiaming Liu, Chenyang Gu, Zhuoyang Liu, Renrui Zhang, Xiaoqi Li, Xiao He, Yandong Guo, Chi-Wing Fu, Shanghang Zhang, and Pheng-Ann Heng. Fast-in-slow: A dual-system foundation model unifying fast manipulation within slow reasoning, 2025. 2 

- [6] Xi Chen, Xiao Wang, Lucas Beyer, Alexander Kolesnikov, Jialin Wu, Paul Voigtlaender, Basil Mustafa, Sebastian Goodman, Ibrahim Alabdulmohsin, Piotr Padlewski, Daniel Salz, Xi Xiong, Daniel Vlasic, Filip Pavetic, Keran Rong, Tianli Yu, Daniel Keysers, Xiaohua Zhai, and Radu Soricut. Pali-3 vision language models: Smaller, faster, stronger, 2023. 1 

- [7] Rohan Chitnis, Shubham Tulsiani, Saurabh Gupta, and Abhinav Gupta. Efficient bimanual manipulation using learned task schemas, 2020. 3 

- [8] Damai Dai, Chengqi Deng, Chenggang Zhao, R. X. Xu, Huazuo Gao, Deli Chen, Jiashi Li, Wangding Zeng, Xingkai Yu, Y. Wu, Zhenda Xie, Y. K. Li, Panpan Huang, Fuli Luo, Chong Ruan, Zhifang Sui, and Wenfeng Liang. Deepseekmoe: Towards ultimate expert specialization in mixture-ofexperts language models, 2024. 2 

- [9] Matt Deitke, Christopher Clark, Sangho Lee, Rohun Tripathi, Yue Yang, Jae Sung Park, Mohammadreza Salehi, Niklas Muennighoff, Kyle Lo, Luca Soldaini, Jiasen Lu, Taira Anderson, Erin Bransom, Kiana Ehsani, Huong Ngo, YenSung Chen, Ajay Patel, Mark Yatskar, Chris CallisonBurch, Andrew Head, Rose Hendrix, Favyen Bastani, Eli VanderBilt, Nathan Lambert, Yvonne Chou, Arnavi Chheda, Jenna Sparks, Sam Skjonsberg, Michael Schmitz, Aaron Sarnat, Byron Bischoff, Pete Walsh, Chris Newell, Piper Wolters, Tanmay Gupta, Kuo-Hao Zeng, Jon Borchardt, Dirk Groeneveld, Crystal Nam, Sophie Lebrecht, Caitlin Wittlif, Carissa Schoenick, Oscar Michel, Ranjay Krishna, Luca Weihs, Noah A. Smith, Hannaneh Hajishirzi, Ross Girshick, Ali Farhadi, and Aniruddha Kembhavi. Molmo and pixmo: Open weights and open data for state-of-the-art vision-language models, 2024. 1, 2 

- [10] Lutfi Eren Erdogan, Nicholas Lee, Sehoon Kim, Suhong Moon, Hiroki Furuta, Gopala Anumanchipalli, Kurt Keutzer, and Amir Gholami. Plan-and-act: Improving planning of agents for long-horizon tasks. _arXiv preprint arXiv:2503.09572_ , 2025. 2 

- [11] Huang Fang, Mengxi Zhang, Heng Dong, Wei Li, Zixuan Wang, Qifeng Zhang, Xueyun Tian, Yucheng Hu, and Hang Li. Robix: A unified model for robot interaction, reasoning and planning, 2025. 2 

- [12] Roy Fox, Richard Shin, William Paul, Yitian Zou, Dawn Song, Ken Goldberg, Pieter Abbeel, and Ion Stoica. Hierarchical variational imitation learning of control programs, 2019. 3 

- [13] Yingdong Hu, Fanqi Lin, Tong Zhang, Li Yi, and Yang Gao. Look before you leap: Unveiling the power of gpt-4v in robotic vision-language planning, 2023. 1 

20751 

- [14] Haoxu Huang, Fanqi Lin, Yingdong Hu, Shengjie Wang, and Yang Gao. Copa: General robotic manipulation through spatial constraints of parts with foundation models, 2024. 2 

- [15] Suning Huang, Zheyu Zhang, Tianhai Liang, Yihan Xu, Zhehao Kou, Chenhao Lu, Guowei Xu, Zhengrong Xue, and Huazhe Xu. Mentor: Mixture-of-experts network with task-oriented perturbation for visual reinforcement learning, 2025. 2 

- [16] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, James Tanner, Quan Vuong, Homer Walke, Anna Walling, Haohuan Wang, Lili Yu, and Ury Zhilinsky. _π_ 0 _._ 5: a vision-language-action model with open-world generalization, 2025. 2, 6, 7, 8 

- [17] Albert Q. Jiang, Alexandre Sablayrolles, Antoine Roux, Arthur Mensch, Blanche Savary, Chris Bamford, Devendra Singh Chaplot, Diego de las Casas, Emma Bou Hanna, Florian Bressand, Gianna Lengyel, Guillaume Bour, Guillaume Lample, L´elio Renard Lavaud, Lucile Saulnier, Marie-Anne Lachaux, Pierre Stock, Sandeep Subramanian, Sophia Yang, Szymon Antoniak, Teven Le Scao, Th´eophile Gervet, Thibaut Lavril, Thomas Wang, Timoth´ee Lacroix, and William El Sayed. Mixtral of experts, 2024. 2 

- [18] Tao Jiang, Tianyuan Yuan, Yicheng Liu, Chenhao Lu, Jianning Cui, Xiao Liu, Shuiqi Cheng, Jiyang Gao, Huazhe Xu, and Hang Zhao. Galaxea open-world dataset and g0 dualsystem vla model, 2025. 1 

- [19] Siddharth Karamcheti, Suraj Nair, Ashwin Balakrishna, Percy Liang, Thomas Kollar, and Dorsa Sadigh. Prismatic vlms: Investigating the design space of visually-conditioned language models, 2024. 1, 2 

- [20] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An opensource vision-language-action model, 2024. 1, 2, 6 

- [21] Daehee Lee, Minjong Yoo, Woo Kyung Kim, Wonje Choi, and Honguk Woo. Incremental learning of retrievable skills for efficient continual task adaptation, 2025. 3 

- [22] Jason Lee, Jiafei Duan, Haoquan Fang, Yuquan Deng, Shuo Liu, Boyang Li, Bohan Fang, Jieyu Zhang, Yi Ru Wang, Sangho Lee, Winson Han, Wilbert Pumacay, Angelica Wu, Rose Hendrix, Karen Farley, Eli VanderBilt, Ali Farhadi, Dieter Fox, and Ranjay Krishna. Molmoact: Action reasoning models that can reason in space, 2025. 2 

- [23] Fanqi Lin, Ruiqian Nai, Yingdong Hu, Jiacheng You, Junming Zhao, and Yang Gao. Onetwovla: A unified visionlanguage-action model with adaptive reasoning, 2025. 1, 2 

- [24] Yaron Lipman, Ricky T. Q. Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le. Flow matching for generative modeling, 2023. 3 

- [25] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning, 2023. 2, 5 

- [26] Jiaming Liu, Hao Chen, Pengju An, Zhuoyang Liu, Renrui Zhang, Chenyang Gu, Xiaoqi Li, Ziyu Guo, Sixiang Chen, Mengzhen Liu, Chengkai Hou, Mengdi Zhao, KC alex Zhou, Pheng-Ann Heng, and Shanghang Zhang. Hybridvla: Collaborative diffusion and autoregression in a unified visionlanguage-action model, 2025. 2 

- [27] Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. Rdt-1b: a diffusion foundation model for bimanual manipulation, 2025. 1, 3 

- [28] Xiaofeng Mao, Gabriele Giudici, Claudio Coppola, Kaspar Althoefer, Ildar Farkhatdinov, Zhibin Li, and Lorenzo Jamone. Dexskills: Skill segmentation using haptic data for learning autonomous long-horizon robotic manipulation tasks, 2024. 3 

- [29] Oier Mees, Lukas Hermann, Erick Rosete-Beas, and Wolfram Burgard. Calvin: A benchmark for languageconditioned policy learning for long-horizon robot manipulation tasks, 2022. 2, 5 

- [30] Atharva Mete, Haotian Xue, Albert Wilcox, Yongxin Chen, and Animesh Garg. Quest: Self-supervised skill abstractions for learning continuous control, 2024. 3 

- [31] NVIDIA, :, Johan Bjorck, Fernando Casta˜neda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi ”Jim” Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, Joel Jang, Zhenyu Jiang, Jan Kautz, Kaushil Kundalia, Lawrence Lao, Zhiqi Li, Zongyu Lin, Kevin Lin, Guilin Liu, Edith Llontop, Loic Magne, Ajay Mandlekar, Avnish Narayan, Soroush Nasiriany, Scott Reed, You Liang Tan, Guanzhi Wang, Zu Wang, Jing Wang, Qi Wang, Jiannan Xiang, Yuqi Xie, Yinzhen Xu, Zhenjia Xu, Seonghyeon Ye, Zhiding Yu, Ao Zhang, Hao Zhang, Yizhou Zhao, Ruijie Zheng, and Yuke Zhu. Gr00t n1: An open foundation model for generalist humanoid robots, 2025. 1 

- [32] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for visionlanguage-action models, 2025. 2 

- [33] Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, Bin Zhao, Dong Wang, and Xuelong Li. Spatialvla: Exploring spatial representations for visual-language-action model, 2025. 6 

- [34] Qwen, :, An Yang, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chengyuan Li, Dayiheng Liu, Fei Huang, Haoran Wei, Huan Lin, Jian Yang, Jianhong Tu, Jianwei Zhang, Jianxin Yang, Jiaxi Yang, Jingren Zhou, Junyang Lin, Kai Dang, Keming Lu, Keqin Bao, Kexin Yang, Le Yu, Mei Li, Mingfeng Xue, Pei Zhang, Qin Zhu, Rui Men, Runji Lin, Tianhao Li, Tianyi Tang, Tingyu Xia, Xingzhang Ren, Xuancheng Ren, Yang Fan, Yang Su, Yichang Zhang, Yu Wan, Yuqiong Liu, Zeyu Cui, Zhenru Zhang, and Zihan Qiu. Qwen2.5 technical report, 2025. 1 

- [35] Moritz Reuss, Jyothish Pari, Pulkit Agrawal, and Rudolf Lioutikov. Efficient diffusion transformer policies with mixture of expert denoisers for multitask learning, 2024. 2, 8 

20752 

- [36] Kaushik Roy, Akila Dissanayake, Brendan Tidd, and Peyman Moghadam. M2distill: Multi-modal distillation for lifelong imitation learning, 2025. 3 

- [37] Lucy Xiaoyang Shi, Brian Ichter, Michael Equi, Liyiming Ke, Karl Pertsch, Quan Vuong, James Tanner, Anna Walling, Haohuan Wang, Niccolo Fusai, Adrian Li-Bell, Danny Driess, Lachy Groom, Sergey Levine, and Chelsea Finn. Hi robot: Open-ended instruction following with hierarchical vision-language-action models, 2025. 1, 2 

- [38] Robin Strudel, Alexander Pashevich, Igor Kalevatykh, Ivan Laptev, Josef Sivic, and Cordelia Schmid. Learning to combine primitive skills: A step towards versatile robotic manipulation, 2020. 3 

- [39] Jiankai Sun, Aidan Curtis, Yang You, Yan Xu, Michael Koehle, Qianzhong Chen, Suning Huang, Leonidas Guibas, Sachin Chitta, Mac Schwager, and Hui Li. Arch: Hierarchical hybrid learning for long-horizon contact-rich robotic assembly, 2025. 3 

- [40] Gemini Robotics Team, Saminda Abeyruwan, Joshua Ainslie, Jean-Baptiste Alayrac, Montserrat Gonzalez Arenas, Travis Armstrong, Ashwin Balakrishna, Robert Baruch, Maria Bauza, Michiel Blokzijl, Steven Bohez, Konstantinos Bousmalis, Anthony Brohan, Thomas Buschmann, Arunkumar Byravan, Serkan Cabi, Ken Caluwaerts, Federico Casarini, Oscar Chang, Jose Enrique Chen, Xi Chen, Hao-Tien Lewis Chiang, Krzysztof Choromanski, David D’Ambrosio, Sudeep Dasari, Todor Davchev, Coline Devin, Norman Di Palo, Tianli Ding, Adil Dostmohamed, Danny Driess, Yilun Du, Debidatta Dwibedi, Michael Elabd, Claudio Fantacci, Cody Fong, Erik Frey, Chuyuan Fu, Marissa Giustina, Keerthana Gopalakrishnan, Laura Graesser, Leonard Hasenclever, Nicolas Heess, Brandon Hernaez, Alexander Herzog, R. Alex Hofer, Jan Humplik, Atil Iscen, Mithun George Jacob, Deepali Jain, Ryan Julian, Dmitry Kalashnikov, M. Emre Karagozler, Stefani Karp, Chase Kew, Jerad Kirkland, Sean Kirmani, Yuheng Kuang, Thomas Lampe, Antoine Laurens, Isabel Leal, Alex X. Lee, Tsang-Wei Edward Lee, Jacky Liang, Yixin Lin, Sharath Maddineni, Anirudha Majumdar, Assaf Hurwitz Michaely, Robert Moreno, Michael Neunert, Francesco Nori, Carolina Parada, Emilio Parisotto, Peter Pastor, Acorn Pooley, Kanishka Rao, Krista Reymann, Dorsa Sadigh, Stefano Saliceti, Pannag Sanketi, Pierre Sermanet, Dhruv Shah, Mohit Sharma, Kathryn Shea, Charles Shu, Vikas Sindhwani, Sumeet Singh, Radu Soricut, Jost Tobias Springenberg, Rachel Sterneck, Razvan Surdulescu, Jie Tan, Jonathan Tompson, Vincent Vanhoucke, Jake Varley, Grace Vesom, Giulia Vezzani, Oriol Vinyals, Ayzaan Wahid, Stefan Welker, Paul Wohlhart, Fei Xia, Ted Xiao, Annie Xie, Jinyu Xie, Peng Xu, Sichun Xu, Ying Xu, Zhuo Xu, Yuxiang Yang, Rui Yao, Sergey Yaroshenko, Wenhao Yu, Wentao Yuan, Jingwei Zhang, Tingnan Zhang, Allan Zhou, and Yuxiang Zhou. Gemini robotics: Bringing ai into the physical world, 2025. 1, 2 

- [41] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, Jianlan Luo, You Liang Tan, Lawrence Yunliang Chen, Pannag Sanketi, Quan 

Vuong, Ted Xiao, Dorsa Sadigh, Chelsea Finn, and Sergey Levine. Octo: An open-source generalist robot policy, 2024. 6 

- [42] Aaron van den Oord, Oriol Vinyals, and Koray Kavukcuoglu. Neural discrete representation learning, 2018. 3 

- [43] Weikang Wan, Yifeng Zhu, Rutav Shah, and Yuke Zhu. Lotus: Continual imitation learning for robot manipulation through unsupervised skill discovery, 2024. 3 

- [44] Peng Wang, Shuai Bai, Sinan Tan, Shijie Wang, Zhihao Fan, Jinze Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Yang Fan, Kai Dang, Mengfei Du, Xuancheng Ren, Rui Men, Dayiheng Liu, Chang Zhou, Jingren Zhou, and Junyang Lin. Qwen2-vl: Enhancing vision-language model’s perception of the world at any resolution, 2024. 1, 2 

- [45] Yixiao Wang, Mingxiao Huo, Zhixuan Liang, Yushi Du, Lingfeng Sun, Haotian Lin, Jinghuan Shang, Chensheng Peng, Mohit Bansal, Mingyu Ding, and Masayoshi Tomizuka. Ver: Vision expert transformer for robot learning via foundation distillation and dynamic routing, 2025. 2 

- [46] Yi Wang, Xinhao Li, Ziang Yan, Yinan He, Jiashuo Yu, Xiangyu Zeng, Chenting Wang, Changlian Ma, Haian Huang, Jianfei Gao, Min Dou, Kai Chen, Wenhai Wang, Yu Qiao, Yali Wang, and Limin Wang. Internvideo2.5: Empowering video mllms with long and rich context modeling, 2025. 3, 5 

- [47] Yating Wang, Haoyi Zhu, Mingyu Liu, Jiange Yang, HaoShu Fang, and Tong He. Vq-vla: Improving visionlanguage-action models via scaling vector-quantized action tokenizers, 2025. 3 

- [48] Junjie Wen, Minjie Zhu, Yichen Zhu, Zhibin Tang, Jinming Li, Zhongyi Zhou, Chengmeng Li, Xiaoyu Liu, Yaxin Peng, Chaomin Shen, and Feifei Feng. Diffusion-vla: Generalizable and interpretable robot foundation model via selfgenerated reasoning, 2025. 3 

- [49] Junjie Wen, Yichen Zhu, Jinming Li, Zhibin Tang, Chaomin Shen, and Feifei Feng. Dexvla: Vision-language model with plug-in diffusion expert for general robot control, 2025. 2 

- [50] Lu Xu, Jiaqian Yu, Xiongfeng Peng, Yiwei Chen, Weiming Li, Jaewook Yoo, Sunghyun Chunag, Dongwook Lee, Daehyun Ji, and Chao Zhang. Mose: Skill-by-skill mixture-ofexperts learning for embodied autonomous machines, 2025. 2 

- [51] Jiange Yang, Haoyi Zhu, Yating Wang, Gangshan Wu, Tong He, and Limin Wang. Tra-moe: Learning trajectory prediction model from multiple domains for adaptive policy conditioning, 2025. 2 

- [52] Shuai Yang, Hao Li, Yilun Chen, Bin Wang, Yang Tian, Tai Wang, Hanqing Wang, Feng Zhao, Yiyi Liao, and Jiangmiao Pang. Instructvla: Vision-language-action instruction tuning from understanding to manipulation, 2025. 1, 2 

- [53] Yi Yang, Jiaxuan Sun, Siqi Kou, Yihan Wang, and Zhijie Deng. Lohovla: A unified vision-language-action model for long-horizon embodied tasks, 2025. 1, 2 

- [54] Zhenjie Yang, Yilin Chai, Xiaosong Jia, Qifeng Li, Yuqian Shao, Xuekai Zhu, Haisheng Su, and Junchi Yan. Drivemoe: Mixture-of-experts for vision-language-action model in endto-end autonomous driving, 2025. 2 

20753 

- [55] Zhutian Yang, Caelan Garrett, Dieter Fox, Tom´as LozanoP´erez, and Leslie Pack Kaelbling. Guiding long-horizon task and motion planning with vision language models. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 16847–16853. IEEE, 2025. 2 

- [56] Yuanqi Yao, Siao Liu, Haoming Song, Delin Qu, Qizhi Chen, Yan Ding, Bin Zhao, Zhigang Wang, Xuelong Li, and Dong Wang. Think small, act big: Primitive prompt learning for lifelong robot manipulation, 2025. 3 

- [57] Jiawen Yu, Hairuo Liu, Qiaojun Yu, Jieji Ren, Ce Hao, Haitong Ding, Guangyu Huang, Guofan Huang, Yan Song, Panpan Cai, Cewu Lu, and Wenqiang Zhang. Forcevla: Enhancing vla models with a force-aware moe for contact-rich manipulation, 2025. 2 

- [58] Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli Ma, Song Han, Chelsea Finn, Ankur Handa, Ming-Yu Liu, Donglai Xiang, Gordon Wetzstein, and Tsung-Yi Lin. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models, 2025. 6 

- [59] Jinliang Zheng, Jianxiong Li, Dongxiu Liu, Yinan Zheng, Zhihao Wang, Zhonghong Ou, Yu Liu, Jingjing Liu, Ya-Qin Zhang, and Xianyuan Zhan. Universal actions for enhanced embodied foundation models, 2025. 2 

- [60] Zhehua Zhou, Jiayang Song, Kunpeng Yao, Zhan Shu, and Lei Ma. Isr-llm: Iterative self-refined large language model for long-horizon sequential task planning. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 2081–2088. IEEE, 2024. 2 

- [61] Zhongyi Zhou, Yichen Zhu, Junjie Wen, Chaomin Shen, and Yi Xu. Chatvla-2: Vision-language-action model with open-world embodied reasoning from pretrained knowledge, 2025. 2 

20754 

