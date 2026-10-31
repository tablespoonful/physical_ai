---
title: "RLux-VLA: A Unified and Efficient Framework for Reinforcement Learning of Vision-Language-Action Models"
date: "2026"
venue: "RSS 2026"
url: https://www.roboticsproceedings.org/rss22/p089.html
pdf: https://www.roboticsproceedings.org/rss22/p089.pdf
converter: pymupdf4llm
---

> **[PDF を開く](https://www.roboticsproceedings.org/rss22/p089.pdf)** / [論文ページ](https://www.roboticsproceedings.org/rss22/p089.html)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**Robotics: Science and Systems 2026 Sydney, Australia, July 13–17, 2026** 

# RLinf-VLA: A Unified and Efficient Framework for Reinforcement Learning of Vision-Language-Action Models 

Hongzhi Zang<sup>1</sup><sup>_,∗_</sup> , Mingjie Wei<sup>6</sup><sup>_,_2</sup><sup>_,∗_</sup> , Si Xu<sup>3</sup> , Yongji Wu<sup>5</sup> , Zhen Guo<sup>3</sup> , Yuanqing Wang<sup>4</sup><sup>_,_3</sup> , Hao Lin<sup>3</sup> , Peihong Wang<sup>2</sup> , Hua Yuan<sup>3</sup> , Yixian Zhang<sup>1</sup> , Liangzhi Shi<sup>1</sup> , Yuqing Xie<sup>1</sup> , Zhexuan Xu<sup>1</sup> , Zhihao Liu<sup>7</sup><sup>_,_2</sup> , Kang Chen<sup>4</sup><sup>_,_2</sup> , Wenhao Tang<sup>1</sup> , Quanlu Zhang<sup>3</sup> , Weinan Zhang<sup>6</sup> , Chao Yu<sup>1</sup><sup>_,§,†_</sup> , Yu Wang<sup>1</sup><sup>_,†_</sup> 

> 1Tsinghua University 2Zhongguancun Academy 3Infinigence AI 4Peking University 5UC Berkeley 

> 6Harbin Institute of Technology 7Institute of Automation, Chinese Academy of Sciences 

> _∗_ Equal contribution _†_ Corresponding Authors: zoeyuchao@gmail.com, yu-wang@tsinghua.edu.cn _§_ Project Lead 


https://huggingface.co/RLinf https://github.com/RLinf/RLinf 


Fig. 1: Overview of RLinf-VLA. Built on a unified interface, RLinf-VLA seamlessly supports diverse VLA architectures, multiple RL algorithms, and various simulators. It provides three GPU allocation modes: _collocated_ , _disaggregated_ , and a novel _hybrid_ mode and speeds up training by 2 _._ 27 _×_ compared to the baseline. A single model achieves 98.11% success across 130 LIBERO tasks, and another single model achieves 97.66% success across 25 ManiSkill tasks. For RoboTwin, six task-specific models achieve an average success rate of 84.63% across 6 tasks. 

**_Abstract_ —Recent studies have demonstrated the potential of reinforcement learning (RL) to improve the task performance of vision-language-action (VLA) models through interaction. However, current efforts remain fragmented, lacking a unified platform for fair comparison across architectures and algorithms, as well as an efficient system design for scalable training. Therefore, we present RLinf-VLA, a unified and efficient framework** 

**for scalable RL training of VLA models. RLinf-VLA standardizes the integration of diverse VLA architectures, RL algorithms, and heterogeneous simulators through a unified interface, enabling extensibility and reproducibility. To improve efficiency, the framework adopts a flexible resource allocation architecture for rendering, inference, and training in RL pipelines. In particular, RLinf-VLA introduces a hybrid fine-grained pipeline allocation** 

**strategy that achieves a 1.61** _×_ **–1.88** _×_ **training speedup on ManiSkill. Using this framework, RL-trained models achieve strong performance across embodied benchmarks, including 98.11% success on 130 LIBERO tasks, 97.66% success on 25 ManiSkill tasks, and 84.63% average success across 6 RoboTwin tasks. In addition, RLinf-VLA distills a set of effective practices for RLbased VLA training. We envision RLinf-VLA as a foundational framework for efficient, unified, and reproducible research in embodied intelligence.** 

## I. INTRODUCTION 

Vision-Language-Action (VLA) models represent a new generation of foundation models that aim to unify perception, language understanding, and embodied control [28, 10]. By leveraging vision-language models pretrained on internet-scale data and further training them on large, heterogeneous robot demonstration datasets [33, 19], VLAs can map raw sensor observations and natural language instructions directly to robot actions. This paradigm has demonstrated strong generalization across a wide range of tasks [44, 20, 26, 46, 37, 2, 18]. 

However, deploying VLA models typically requires posttraining to mitigate distribution mismatch between training data and deployment environments. Without effective posttraining, performance can degrade significantly when models encounter novel states, instructions, or execution conditions. 

Reinforcement learning (RL) has emerged as an increasingly important post-training paradigm, as it directly optimizes cumulative task rewards through trial-and-error interaction [41]. In contrast to supervised fine-tuning (SFT), another commonly used post-training approach, RL enables exploration beyond narrow expert demonstrations and equips policies with corrective and adaptive behaviors. Recent studies indicate that RL fine-tuning can yield stronger out-of-distribution generalization than SFT, particularly in terms of semantic alignment and execution robustness [25]. 

Despite its promise, applying RL to VLA models remains largely small-scale or fragmented [25, 27], making the development of new RL algorithms for VLAs expensive and cumbersome. Although SimpleVLA-RL [23] enables largescale RL training for VLAs by building on VeRL [39], an RL codebase originally designed for large language models, it lacks system-level optimizations tailored to embodied settings, where simulators compete with model inference and learning for GPU resources. This limitation constrains scalability and substantially increases training time. 

Moreover, online RL requires repeated and tightly coupled model–environment interactions. Without a system design explicitly tailored to this execution pattern, significant GPU idle time and pipeline bubbles can arise, leading to inefficient resource utilization. Finally, existing works often rely on disparate model architectures, RL algorithms, and evaluation protocols, making fair comparison difficult and hindering the extraction of general principles for RL-based VLA training. 

To address these challenges, we present **RLinf-VLA** , a **_unified_** and **_efficient_** framework for scalable reinforcement learning of vision-language-action models. Our main contributions are summarized as follows: 

- **Unified system abstraction.** RLinf-VLA provides a unified interface that supports multiple robotic simulators (e.g. ManiSkill [43], LIBERO [24], RoboTwin [9]), diverse VLA architectures (e.g. OpenVLA [20], OpenVLAOFT [21], _π_ 0 [2]), and reinforcement learning algorithms (e.g. PPO [36], GRPO [38]). The system exposes three execution modes, including a novel hybrid GPU allocation mode, enabling scalable and configurable training across heterogeneous setups. 

- **Efficient system and algorithm design.** RLinf-VLA supports multiple flexible GPU allocation modes and further introduces a hybrid fine-grained pipelining mechanism. By improving resource allocation, RLinf-VLA substantially increases training throughput, achieving speedups of up to 2.27 _×_ . In addition, the framework incorporates a set of algorithmic enhancements that further improve training efficiency and stability. 

- **Strong empirical performance and generalization.** After RL training with RLinf-VLA, a single model achieves 98.11% success across 130 LIBERO tasks, while another single model achieves 97.66% success across 25 ManiSkill tasks. On RoboTwin, six task-specific models achieve an average success rate of 84.63% across 6 tasks, corresponding to an average performance improvement of 63.75%. These results demonstrate RLinf-VLA’s powerful performance in post-training. 

- **Open and extensible platform.** RLinf-VLA is released as an open-source and actively maintained platform, providing a practical foundation to accelerate, standardize, and scale reinforcement learning research for embodied intelligence. 

## II. RELATED WORK 

_A. Reinforcement Learning for VLA_ 

Vision-Language-Action models (VLAs) [21, 20, 2, 4, 18, 48, 5, 1, 51, 6] represent a multimodal foundation model architecture designed for robotics. RL is increasingly adopted to address the limitations of static imitation learning in VLAs. GRAPE [49] employs Direct Preference Optimization (DPO [34]) on partial trajectories to align models with human intent. Iterative approaches [14, 42] combine SFT with RL stages to balance stability and performance. VLARL [27] utilizes Proximal Policy Optimization (PPO [36]) to exhibit significantly stronger generalization to unseen objects and environments compared to their SFT counterparts [25]. SimpleVLA-RL [23] and related variants [42] apply Group Relative Policy Optimization (GRPO [38]) to improve training efficiency and performance without complex reward design. _πRL_ [7] implements the policy gradient algorithm to flowmatching model for the first time. _π_ 0<sup>_∗_</sup> _._ 6<sup>[17] introduces RECAP</sup> to train a binarized value function and VLA. A unified and efficient infrastructure is essential for advancing VLA via RL, yet current implementations remain fragmented [25, 27]. Although frameworks such as SimpleVLA-RL [23] have emerged, they largely follow generic LLM RL post-training paradigms and fail to adequately account for the system-level optimizations 

and interface extensibility required by embodied intelligence tasks. 

## _B. Simulators_ 

Simulators [22, 29, 30, 32, 31, 12, 3] offer scalable, safe, and controllable environments that bypass physical hardware constraints. They facilitate massive parallel data generation and automated resets, essential for training and evaluating generalizable VLA policies. Notable platforms include ManiSkill [43] for physics-rich manipulation, LIBERO [24] for instruction-conditioned reasoning, and RoboTwin [9] for bimanual tasks with domain randomization. Consequently, the construction and utilization of simulators are indispensable for RL. However, inconsistent interfaces across simulators often necessitate extensive code restructuring. A unified interface is therefore critical to enable seamless switching between diverse simulation benchmarks. 

## III. PRELIMINARY 

## _A. Reinforcement Learning Formulation_ 

To motivate the design of our training infrastructure, reinforcement learning(RL) is commonly formulated as a partially observable Markov decision process (POMDP). A POMDP is defined by the tuple ( _S, A, P, r, γ,_ Ω _, O_ ), where _S_ and _A_ denote the state and action spaces, _P_ ( _s_<sup>_′_</sup> _| s, a_ ) is the transition dynamics, _r_ ( _s, a_ ) is the reward function, and _γ ∈_ [0 _,_ 1] is the discount factor. Since the agent cannot directly access the underlying state, it instead receives observations _o ∈_ Ω according to the observation function _O_ ( _o | s_ ). In vision-based manipulation tasks, observations typically consist of multiview images, language instructions, and proprioceptive robot states, while actions correspond to continuous robot control commands or action chunks. 

At each timestep _t_ , the agent samples an action _at ∼ πθ_ ( _· | ot_ ) based on the current observation _ot ∼ O_ ( _· | st_ ). The environment then executes _at_ , transitions to the next state _st_ +1 via _P_ , and produces the next observation _ot_ +1. The goal of RL is to optimize the parameterized policy _πθ_ so as to maximize the expected cumulative discounted reward over trajectories _τ_ = ( _s_ 0 _, a_ 0 _, . . . , sT_ ): 


## _B. Action Formulation_ 

Compared to RL for LLMs, a key distinction in RL for VLAs lies in the hierarchical formulation of actions. While LLMs typically operate on individual tokens [38], VLA policies often predict either a single action [20] or an action _chunk_ containing multiple actions to ensure smooth control [50]. This leads to a three-level hierarchy consisting of _Chunk_ , _Atomic Action_ , and _Token_ . Each chunk may contain multiple atomic actions, and each atomic action is composed of multiple tokens, where each token typically corresponds to a specific dimension of the robot action space (e.g., end-effector pose or joint angles). 


Fig. 3: Pipeline of Reinforcement Learning for VLA models 

## _C. Pipeline of Reinforcement Learning for VLA models_ 

The RL pipeline for VLA models comprises three distinct components: _Generation_ , _Simulator_ , and _Training_ , as illustrated in Figure 3. GPU resources are primarily allocated between the rollout phase ( _Generation_ and _Simulator_ ) and the optimization phase ( _Training_ ). The interaction typically proceeds as follows [21]: the _Generation_ module infers an action chunk based on the current observation; the _Simulator_ executes this chunk and returns the observation from the final timestep. This loop continues until trajectory collection is complete, after which the _Training_ module updates the policy using the gathered data. 

## IV. METHOD 

Section IV-A introduces flexible GPU Allocation Strategies for improved resource scheduling across different simulator types. Section IV-B presents a Unified Interface that seamlessly integrates diverse simulators, VLA models, and RL algorithms. Building on this system design, Section IV-C distills key Design Choices for scalable RL training of VLA models. 

## _A. GPU Allocation Strategies_ 

The RL training pipeline (described in Section III-C) for VLA involves varying resource demands from _Training_ , _Generation_ , and _Simulator_ . Resource bottlenecks depend heavily on the simulator type: CPU-parallelized simulators are typically CPU-bound, using GPUs primarily for rendering and inference, whereas GPU-parallelized simulators execute simulation, rendering, and inference entirely on the GPU. While the latter offers higher throughput, it creates severe contention for GPU memory and compute. To maximize efficient utilization across these diverse setups, flexible and optimized GPU allocation strategies are essential. Our framework supports flexible and easily configurable allocation modes: _collocated_ , _disaggregated_ , and a novel _hybrid_ mode. 


Fig. 4: Collocated Mode. 

_1) The Collocated Mode:_ In this mode (Figure 4), all components co-exist on the same set of GPUs. The original version of collocated mode aimed to maximize GPU utilization 

by maintaining only one component on all GPUs at any given time. When a component finished its computation, it would be offloaded from GPU to CPU memory, and then onloaded again when needed for its next task. However, under the embodiment setting, both _Simulator_ and _Generation_ require GPU resources and interact frequently in an iterative manner. The overhead introduced by repeated offload-onload operations at each interaction becomes prohibitively large and unacceptable. 

Therefore, we implement a modified collocated strategy where offload and onload operations for the _Simulator_ and _Generation_ occur only at the beginning and end of the rollout phase, as shown in the figure. While this approach successfully avoids the frequent offload-onload overhead during rollout, it cannot fully utilize GPU resources and remains sub-optimal. Since _Generation_ and _Simulator_ must interact iteratively, they spend significant time waiting for each other, occupying GPU memory without performing computation, leading to resource wastage and limited scalability. 


Fig. 5: Disaggregated Mode (see Figure 4 for legend). 

_2) The Disaggregated Mode:_ In this mode, each component is assigned to a distinct (possibly multi-GPU) partition, with no overlap across components. Figure 5 depicts the central idea. This ensures that every component can fully exploit its allocated resources. This mode is simple to implement, but it leads to GPU underutilization due to inter-component dependencies. For example, in Figure 5, GPU 4 and 5 are completely idle during the rollout phase until training. 


Fig. 6: Hybrid Mode (see Figure 4 for legend). 

_3) The Hybrid Mode with Fine-grained Pipelining:_ To overcome the drawbacks of the above modes, we propose a hybrid mode, where each component can flexibly select GPUs. In contrast, existing distributed RL systems are less flexible. For example, veRL [40] primarily adopts a collocated design, while AReaL [11] and SLiME [52] use a disaggregated design but still allocate GPUs to each component in contiguous blocks. 

In our hybrid mode, a typical configuration is to assign _Generation_ and _Simulator_ to different GPU partitions, while allowing _Training_ to utilize all GPUs. Figure 6 shows an illustration. However, the resources remain underutilized. For instance, the _Simulator_ must wait for actions generated by the _Generation_ , leaving some GPUs idle and creating “GPU bubbles”. 


Fig. 7: Hybrid Mode with Fine-grained Pipelining ( _k_ = 2; see Figure 4 for legend). 

On top of this, we introduce fine-grained pipelining to mitigate bubbles caused by inter-component dependencies. Specifically, a simulator instance on one GPU is partitioned into multiple sub-simulators, denoted as _S_<sup>(1)</sup> _, S_<sup>(2)</sup> _, . . . , S_<sup>(</sup><sup>_k_)</sup> . The pipeline with _k_ = 2 proceeds as follows, where superscripts denote simulator indices and subscripts indicate timesteps: 

- 1) At step _t_ = 0, _S_<sup>(1)</sup> generates the initial observation _o_<sup>(1)</sup> 0<sup>,</sup> which is sent to the _Generation_ component to produce action _a_<sup>(1)</sup> 

   - 0<sup>.</sup> 

- 2) Meanwhile, _S_<sup>(2)</sup> generates _o_<sup>(2)</sup> 0 in parallel. 3) Once _a_<sup>(1)</sup> 0 is ready, it is fed back into _S_<sup>(1)</sup> to produce the next observation _o_<sup>(1)</sup> 1<sup>,while</sup><sup>_o_(2)</sup> 0 is simultaneously processed by the actor to generate _a_<sup>(2)</sup> 0<sup>.</sup> 

This scheduling allows _Simulator_ and _Generation_ to run concurrently, reducing idle time while preserving correctness. In this way, our framework avoids the frequent offloading overhead of collocated allocation while also eliminating the GPU bubbles that occur in disaggregated allocation. Figure 6 provides a schematic illustration of the hybrid allocation mode with fine-grained pipelining ( _k_ = 2). 

_4) The Auto-Placement Algorithm:_ Since RLinf-VLA supports multiple GPU allocation modes, automatically determining an efficient allocation strategy is important. To this end, we introduce a lightweight automatic GPU placement algorithm that combines runtime profiling with allocation optimization. 

We begin with several practical assumptions. Given _N_ GPUs, we assume the _Training_ component utilizes all _N_ GPUs whenever active, as this is typically optimal for computeintensive workloads. We therefore focus on optimizing the _Rollout_ phase, which consists of the _Simulator_ and _Generation_ components. We consider GPU splitting only between these two components and restrict the pipeline depth to at most two stages. Given _N_ GPUs and _nS_ simulation environments, our goal is to determine the GPU allocation ( _NS, NG_ ) and pipeline stage number _k ∈{_ 1 _,_ 2 _}_ that minimize rollout time, where 

_NS_ and _NG_ denote the numbers of GPUs allocated to the _Simulator_ and _Generation_ components, respectively. **Profiling.** We estimate the execution time functions _tG_ ( _·_ ) and _tS_ ( _·_ ) by profiling batch sizes _{_ 2<sup>0</sup> _,_ 2<sup>1</sup> _, . . . , nS}_ , yielding estimates of per-chunk execution latency. 

**Allocation.** Let _m_ denote the number of chunks per epoch. We solve min _k∈{_ 1 _,_ 2 _}, NG_ + _NS_ = _N tk_ , where Collocated ( _k_ = 1): _t_ 1 = _m_ � _tG_ � _<u>nNS</u>_ � + _tS_ <u>�</u> _<u>nNS</u>_ ��, Pipelined ( _k_ = 2): _t_ 2 is estimated from _tG_ ( _N_<sup>_<u>nS</u>_</sup> _G_<sup>) and</sup><sup>_tS_(</sup> _N_<sup>_<u>nS</u>_</sup> _S_<sup>)</sup> under pipelined execution. 

## _B. A Unified Interface_ 

To conveniently reuse existing simulators, models, and algorithms, RLinf-VLA provides a unified interface designed for high extensibility and scalability. 

_1) Multiple Simulators Support:_ RLinf-VLA supports multiple robotic simulators, including ManiSkill [43], LIBERO [24], and RoboTwin [9]. To facilitate this, we provide a unified interface that standardizes environment interactions across different backends, such as ManiSkill and RoboTwin’s GPU-parallelized environments and LIBERO’s CPU-parallelized wrappers. This interface includes standard Gym-style APIs with built-in support for action chunking and flexible episode termination. Furthermore, we define a unified interface for observation and action to ensure seamless compatibility with various algorithms and models. 

_2) Multiple Models Support:_ Benefiting from a unified data processing pipeline across simulators, our framework facilitates the seamless integration of existing models by requiring only a standardized interaction interface. We support diverse VLA architectures, exemplified in this study by OpenVLA [20] and OpenVLA-OFT [21], which represent configurations with single-step and multi-step action chunking, respectively. To enable efficient fine-tuning, we integrate LowRank Adaptation (LoRA) [16]. 

_3) Multiple Algorithms Support:_ Our framework provides support for multiple reinforcement learning algorithms, with an initial focus on Proximal Policy Optimization (PPO) [36] and Group Relative Policy Optimization (GRPO) [38, 13]. The core functions for on-policy RL algorithms are the advantage function and the loss function. In our framework, we can configure the algorithms by specifying these two functions only, without redundant code. 

For off-policy reinforcement learning algorithms, their application to VLA models remains an open problem, particularly in terms of achieving stable training. Nevertheless, our pipeline is fully functional and extensible to off-policy settings. As a preliminary extension, RLinf-VLA supports DSRL [45], a variant of Soft Actor-Critic (SAC [15]), for finetuning _π_ -series models. However, off-policy methods are not the primary focus of this work, and we therefore limit our discussion. 

## _C. Design Choices for Algorithms_ 

RL algorithms for large models involve more complex design choices than those for smaller models. For VLAs, 

we adopt methodologies from both LLMs and robotics. In Section IV-C1, we introduce general features applicable to all algorithms. Subsequently, in Section IV-C2 and Section IV-C3, we detail specific design choices for PPO and GRPO, respectively. Consistent with our codebase style, all these features can be easily configured by changing values in the configuration file. 

_1) Multi-Granularity Calculation Support:_ Our framework supports advantage estimation and log-probability computation at multiple levels of granularity, enabling seamless adaptation to different algorithmic requirements. 

For advantage estimation, we provide two formulations for assigning advantages to action chunks _ct_ = ( _at,_ 1 _, . . . , at,C_ )<sup>1</sup> . In the chunk-level formulation, the entire chunk is treated as a single macro-action and is assigned a summed reward and a shared advantage. In contrast, the action-level formulation assigns individual rewards and advantages to each atomic action _at,i_ within the chunk. 

Similarly, for log-probability computation, we support three corresponding granularities: 

Chunk-level: _π_ ( _ct|ot_ ) =<sup>�</sup><sup>_C_</sup> _i_ =1<sup>_π_(</sup><sup>_at,i|ot, at,_:</sup><sup>_i−_1)</sup><sup>_,_</sup> Action-level: _π_ ( _at,i|ot, at,_ : _i−_ 1) =<sup>�</sup><sup>_M_</sup> _j_ =1<sup>_π_(</sup><sup>_dt,i,j|ot, dt,i,_:</sup><sup>_j−_1)</sup><sup>_,_</sup> 

Token-level: _π_ ( _dt,i,j|ot, dt,i,_ : _j−_ 1) _,_ 

where _dt,i,j_ denotes the _j_ -th token of the _i_ -th atomic action. 


(a) Fixed Length (b) Partial Reset (c) Valid Action Mask 

Fig. 8: Illustration of the three rollout modes. 

_2) Design Choices for PPO:_ Scaling PPO to VLA models introduces several design challenges. We summarize the key design decisions adopted in our framework below. **Partial Reset Support** During rollouts, a sub-environment typically terminates either upon reaching the maximum episode length or upon successfully completing a task. We consider two standard strategies for handling such terminations. In the _Fixed Episode Length_ mode, all sub-environments are reset simultaneously only after reaching the maximum episode length. In contrast, the _Partial Reset_ mode resets each sub-environment immediately upon termination, independent of others. Figure 8a and Figure 8b illustrate the differences between these two modes. 

**Critic Design** Adapting PPO to VLA models places stringent requirements on critic design. Maintaining a separate critic network is computationally expensive and complicates GPU resource management due to the large scale of VLA models. We therefore adopt a parameter-sharing strategy between the actor and critic. Following RL4VLA [25], we attach a 

> 1Here, _t_ denotes the index of the chunk, and _C_ denotes the chunk size. 

lightweight value head to the language model component of the VLA for efficient state value estimation. 

**Value for Action Chunks** As discussed in Section IV-C1, the two advantage estimation formulations naturally induce two corresponding value estimation strategies for an action chunk _ct_ = ( _at,_ 1 _, at,_ 2 _, . . . , at,C_ ). In the _chunk-level_ formulation, the critic estimates a single scalar value for the entire chunk, treating it as a macro-action, i.e., _V_ : _S →_ R. In contrast, the _action-level_ formulation produces a _C_ -dimensional value vector, providing an individual value estimate for each atomic action _at,i_ in the chunk, i.e., _V_ : _S →_ R<sup>_C_</sup> . Empirically, we find that the action-level formulation consistently leads to better performance. 

_3) Design Choices for GRPO:_ Transferring GRPO to embodied tasks introduces several non-trivial challenges. To address these, we adopt the following design choices. **Valid Action Mask.** While rollouts are executed for a fixed episode duration, tasks often terminate early. This presents two potential strategies for policy optimization: (1) using the full trajectory regardless of task completion timing, or (2) considering only timesteps prior to task completion. Our framework supports both strategies, referring to the latter as the _Valid Action Mask_ setting (Figure 8c). Empirically, we find that masking out post-completion steps generally improves policy performance in the GRPO setting. 

**Loss Normalization by Trajectory Length.** To ensure that trajectories of different lengths contribute comparably to optimization, we normalize the policy loss by the number of valid timesteps in the _Valid Action Mask_ setting. Specifically, for a trajectory _τi_ with _Ti_<sup>succ</sup> valid timesteps, the contribution of each timestep to the objective is scaled by 1 _/Ti_<sup>succ</sup> . This prevents longer trajectories from dominating the gradient and promotes balanced learning across successful and partially completed trajectories. 

**Success Rate Filter.** Inspired by the dynamic sampling strategy in DAPO [47], we introduce a success-rate filter for GRPO. This filter discards trajectory groups where all trajectories either succeed or fail, as computing non-zero advantages requires a mix of successful and failed outcomes. In practice, this mechanism accelerates convergence and consistently improves policy performance. 

## V. EXPERIMENT RESULTS 

In this section, we systematically investigate three key questions concerning the effectiveness of the proposed RLinfVLA framework: 

**(1) Is RLinf-VLA** **_high-performance_ ?** We evaluate RLinfVLA on three representative testbeds, LIBERO, ManiSkill, and RoboTwin. The results demonstrate that RLinf-VLA achieves approximately 20–85% improvement over the base model, highlighting its strong capability to support large-scale multi-task learning. 

**(2) Is RLinf-VLA** **_high-efficiency_ ?** We benchmark the framework across both GPU-parallelized and CPU-parallelized simulators, and observe that the optimal configuration improves training throughput, with speedups of up to 1 _._ 88 _×_ . 

TABLE I: Evaluation results across three simulation benchmarks. Values denote success rates (%). 

||(a)|Evalu|ation on|ManiS|kill.|||
|---|---|---|---|---|---|---|---|
|Method|||I|n-Distri|bution|OOD|Avg.|
|OpenVLA (Ba|se)|||53.|91|39|.10|
|OpenVLA (RL|inf-G|RPO)||84.|38|75|.15|
|OpenVLA (RL|inf-PP|O)||96.|09|**81**|**.93**|
|OpenVLA-OFT|(Bas|e)||28.|13|18|.29|
|OpenVLA-OFT|(RL|inf-GR|PO)|94.|14|60|.64|
|OpenVLA-OFT|(RL|inf-PP|O)|**97.**|**66**|77|.05|
||(b)|Eval|uation on|LIBER|O.|||
|OpenVLA-OF|T O|bject|Spatial|Goal|Long|90|Avg.|
|Base|5|0.20|51.61|49.40|11.90|42.67|42.09|
|RLinf-GRPO|9|9.67|98.93|98.32|93.55|98.12|98.11|
||(c)|Evalu|ation on|RoboT|win.|||
|OpenVLA-OFT|Cup|Ham|mer<br>Bottl|es<br>Can|Pot|Hand|Avg.|
|Base|75.78|10.1|5<br>20.3|1<br>9.3|7<br>3.13|28.13|24.48|
|RLinf-GRPO|**94.53**|**96.0**|**9**<br>**92.9**|**6**<br>**83.5**|**9**<br>**70.31**|**70.31**|**84.63**|
|SimpleVLA-RL|94.2|87.|5<br>68.|3<br>61.|2<br>64.1|57.8|72.18|


This finding underscores the necessity of supporting diverse allocation modes. Notably, RLinf-VLA achieves up to 2 _._ 27 _×_ speedup over existing frameworks. 

**(3) What are the** **_actionable practices_ for applying PPO and GRPO to VLA training?** Through extensive ablation studies, we identify the key factors that govern training performance, offering practical guidelines for effectively deploying RL in VLA settings. 

**(4) Can simulation-based RL benefit real-world deployment?** We conduct a preliminary real-world deployment study to examine whether policies improved through RL in simulation can transfer to physical robots. Compared with SFTonly baselines, RL post-training leads to improved real-world performance in our setup, suggesting the potential practical value of simulation-based RL for embodied learning. 

**(5) How extensible is RLinf-VLA across models and algorithms?** We further evaluate RLinf-VLA on additional VLA architectures and RL algorithms, including _π_ -series models and off-policy methods. The results in Section X-A demonstrate the extensibility of the framework across diverse training settings. 

## _A. Policy Performance_ 

In this section, we evaluate the effectiveness of RLinf-VLA policies across multiple benchmarks, focusing on task success rates and generalization performance. 

**Experimemt Setup.** We evaluate RLinf-VLA on three benchmarks: ManiSkill, LIBERO, and RoboTwin, with full settings in Appendix III.A. 

For ManiSkill, we train on 25 pick-and-place tasks with object and receptacle variations. We follow the out-of- 


Fig. 9: Training curves on different benchmarks. The x-axis shows the number of training epochs, and the y-axis indicates the corresponding success rate. Light-colored lines represent the raw data, while the dark-colored curves are smoothed using a Gaussian filter with _σ_ = 1. 

distribution evaluation protocol of RL4VLA [25], measuring generalization in _vision_ , _language_ , and _action_ . Each subsetting is evaluated with 256 random episodes. For LIBERO, we use the public task groups [24], including LIBERO-Spatial, Object, Goal, Long, and 90, for training and evaluation. Instead of training within a single group, we train one unified model on the combined 130 tasks over 5 groups, testing large-scale multitask learning. Performance is reported across groups, averaged over 50 episodes per task with three random seeds. For RoboTwin [9], we select six tasks: “beat block hammer”, “move can pot”, “place empty cup”, “pick dual bottles”, “lift pot”, and “handover block”. Training uses 1,000 fixed randomized scene seeds per task, and evaluation samples 128 unseen seeds to assess out-of-distribution generalization. 

**Training Results.** Figure 9 presents the training curves for each setup. Figure 9a and Figure 9b report the training performance on ManiSkill, utilizing OpenVLA and OpenVLAOFT models trained via PPO and GRPO. Across all settings, RL delivers substantial performance gains, improving success rates by 45%–70% over the baseline. Notably, PPO consistently outperforms GRPO and exhibits greater stability for both OpenVLA and OpenVLA-OFT in the ManiSkill setting. Figure 9c illustrates the training curve of OpenVLA-OFT with the GRPO algorithm on 130 tasks of LIBERO. Results demonstrate that the success rate improves substantially from approximately 73% to 98%, yielding an overall performance gain of about 30%. These findings underscore the effectiveness of the GRPO design in RLinf-VLA for enhancing multi-task training. 

Figure 9d depicts our training curves for OpenVLA-OFT on RoboTwin. The training process remains stable with minimal fluctuations. Moreover, the model converges to high performance even on tasks with extremely low initial success rates (as low as 3%). 

**Evaluation Results.** Table I summarizes RLinf-VLA results across three benchmarks, with ManiSkill detailed in Table Ia. “OpenVLA (Base)” and “OpenVLA-OFT (Base)” denote the RL base models for OpenVLA and OpenVLA-OFT. 

Direct OOD comparison between OpenVLA and OpenVLA-OFT is not strictly fair because their base performance differs. OpenVLA improves from 39 _._ 10% to 81 _._ 93% after RL, while OpenVLA-OFT rises from 18 _._ 29% to 77 _._ 05%. Although starting weaker, OpenVLA-OFT shows 

slightly larger relative gains, indicating that base model choice strongly affects final generalization. 

Table Ib reports OpenVLA-OFT trained on 130 tasks with RLinf-VLA over five LIBERO groups. LIBERO-Object reaches 93%–99% success, with an overall average of 98 _._ 11% and a mean improvement of 56 _._ 02%. Notably, we use a single unified model across all tasks, unlike standard methods that train separate models per group, demonstrating RLinf-VLA’s support for large-scale multi-task RL. 

OOD results on RoboTwin are shown in Table Ic. RLinfVLA achieves an average success rate of 84 _._ 63%, over 60% improvement. We also compare with the most relevant baseline, SimpleVLA-RL [23]. RLinf-VLA consistently outperforms it across all RoboTwin tasks, with particularly large gains on challenging tasks such as Bottles, Can, and Hand. These results demonstrate the effectiveness of our system design. 

## _B. System Efficiency_ 

In this section, we evaluate the efficiency of our system by comparing different GPU allocation modes. Our results show that the optimal strategy varies across simulators and models, highlighting the importance of flexible GPU allocation, which is a core feature of RLinf-VLA. 

**Experiment Setup.** We summarize key settings here, with full details in Appendix III.B. We evaluate representative tasks from three benchmarks. For ManiSkill, we use “PutCarrotOnPlateInScene-v2” with 256 parallel environments. For LIBERO, we adopt the LIBERO-Long suite, and for RoboTwin, the “place empty cup” task. For LIBERO and RoboTwin, parallel environments scale linearly with nodes (64, 128, and 256 for 1, 2, and 4 nodes). 

We consider three GPU allocation modes (Section IV-A). _Collocated_ shares GPUs across components, _Disaggregated_ separates training from rollout, and _Hybrid_ pipelines simulation by splitting instances into stages. For comparisons, ManiSkill lacks multi-GPU baselines, so we compare _Collocated_ and _Hybrid_ (pipelined) modes against a naive _Disaggregated_ baseline. For LIBERO and RoboTwin, we benchmark against SimpleVLA-RL [23] (collocated only) and evaluate our _Collocated_ and _Hybrid_ modes; the disaggregated mode is omitted since hybrid consistently performs better when GPUs are underutilized. 


Fig. 10: Evaluation of system efficiency on ManiSkill, LIBERO, and RoboTwin, comparing OpenVLA and OpenVLA-OFT. Throughput (total environment frames per second) improves with increasing pipeline stages (“pipe”). 

**Results.** Figure 10 reports the end-to-end throughput of RLinf-VLA and baselines for RL training under different cluster sizes and GPU allocation modes. 

From Figure 10a, for OpenVLA in ManiSkill, RLinf-VLA achieves up to a 1.88 _×_ speedup over the disaggregated baseline using the Hybrid (pipe=2) mode on 8 GPUs. Although scaling to more GPUs introduces overheads from model loading, offloading, and state switching, fine-grained pipelining reduces GPU idle time and maintains a 1 _._ 61 _×_ –1 _._ 69 _×_ advantage over the disaggregated mode. Deeper pipelines (pipe=2 vs. pipe=1) further improve performance by reducing rolloutstage bubbles. 

For OpenVLA in ManiSkill and OpenVLA-OFT in ManiSkill, as GPU count increases, the hybrid (pipe=1) mode outperforms the collocated mode. Since ManiSkill is GPUparallelized, rollout throughput scales with parallel environments, making simulator resource allocation critical. To improve utilization, we enable offloading in the collocated mode (Section IV-A1), but communication overhead grows with cluster size. In contrast, hybrid mode splits GPUs evenly between components, reducing interference. 

For OpenVLA-OFT in LIBERO and ManiSkill, the behavior differs: collocated and hybrid (pipe=1) modes outperform disaggregated and hybrid (pipe=2). First, OpenVLA-OFT generates action chunks while the simulator executes them sequentially, shifting the generation-to-execution ratio from 1:1 to about 1:15. Second, LIBERO’s CPU-parallelized simulator becomes the main bottleneck. This imbalance diminishes the benefit of pipelining, effectively reverting execution to a nearsequential process. 

From Figure 10b, for OpenVLA-OFT in LIBERO and RoboTwin, RLinf-VLA still achieves a 1.34 _×_ –2.27 _×_ speedup over SimpleVLA-RL under collocated settings. The gains come from both rollout and training. During rollout, RLinfVLA uses vectorized environments that are more efficient than SimpleVLA-RL’s multi-process workers. During training, system-level optimizations such as adaptive communication and the removal of redundant log-probability recomputation further reduce latency, with benefits increasing at scale. 

**Summary.** Different simulators demand different allocation modes. RLinf-VLA’s flexible multi-mode support enables consistently high efficiency across diverse execution regimes. 


Fig. 11: For OpenVLA-OFT, action-level value estimation consistently outperforms chunk-level estimation across different tasks. 

## _C. Ablation Study_ 

In this section, we present ablation studies under different setups and summarize key insights for PPO and GRPO training. 

_1) Tips for PPO:_ **Action-level value estimation outperforms chunk-level estimation for PPO with action chunks.** Figure 11 shows the PPO training curves comparing action-level and chunk-level value estimation as described in Section IV-C2 on the ManiSkill “PutOnPlateInScene25Main” task using the OpenVLA-OFT model. Action-level estimation consistently yields higher success rates and lower value loss, demonstrating more effective learning and faster policy improvement. The performance divergence between different levels of value estimation remains consistent across diverse tasks, as corroborated by similar results in the LIBERO-Goal benchmark (Figure 11c). 


Fig. 12: Partial reset consistently outperforms Fixed Episode Length mode in PPO. 

**Partial reset substantially improves sample efficiency.** Figure 12 presents the PPO training curves for the _Partial Reset_ and _Fixed Episode Length_ rollout modes discussed in Section IV-C2. Since the optimization objective is to achieve 

success at least once per rollout (“success <u>once”),</u> _Partial Reset_ leads to a significantly higher success rate. For a given number of training steps, the success rate under _Partial Reset_ consistently exceeds that of the _Fixed Episode Length_ mode. This trend is observed regardless of the model type (OpenVLA or OpenVLA-OFT). 


without the filter (“w/o Filter”) exhibits a clear collapse around step 400, whereas enabling the filter (“w/ Filter”) largely alleviates this issue. However, the benefit of the filter is not universal: in the OpenVLA-OFT ManiSkill setting and the OpenVLA-OFT LIBERO-Goal setting, its effectiveness is much less pronounced. 


Fig. 15: Deployment in the real world. 

Fig. 13: Ablation study on trajectory length normalization. Success rate in LIBERO-Goal with OpenVLA-OFT. 

_2) Tips for GRPO:_ **Trajectory length normalization.** As discussed in Section IV-C3, normalizing the loss by trajectory length aims to reduce bias when episodes vary in length. Figure 13 shows that incorporating trajectory length normalization (“w/ Norm”) can lead to substantially higher performance compared with the unnormalized setting (“w/o Norm”). **Valid action mask.** We also study the effect of valid action masking, introduced in Section IV-C3. Since the optimization objective is defined with respect to “success <u>once”,</u> excluding actions after reaching the success state improves sample efficiency and avoids redundant updates. Moreover, applying the valid action mask naturally results in shorter trajectories, which further benefits trajectory length normalization. Figure 14a shows results on LIBERO-Goal. Comparing the “w/o Mask, w/o Norm” and “w/ Mask, w/o Norm” curves, the setting with a valid action mask achieves consistently better performance. The “w/ Mask, w/ Norm” curve demonstrates that combining the mask with trajectory length normalization provides an additional improvement. However, the effect of these techniques is task-dependent. In the ManiSkill setting, we do not observe clear benefits from either valid action masking or trajectory length normalization. 


Fig. 14: Ablation studies on valid action mask in GRPO with OpenVLA-OFT. 

_(c) Success rate filtering can improve training stability in some settings of GRPO._ As discussed in Section IV-C3, we implement a success rate filter for GRPO that discards groups in which all trajectories have identical cumulative rewards. This mechanism can improve the stability of GRPO training. For instance, in the OpenVLA ManiSkill setting, training 

## _D. Real-World Experiment_ 

We conduct a preliminary real-world experiment to evaluate whether RL improvements obtained in simulation can transfer to physical deployment. 

Specifically, we consider a drawer-closing task using OpenVLA and compare an SFT-only model with a model further optimized through RL in simulation. The SFT model is trained using 20 real-world expert demonstrations together with 1000 simulated trajectories. The RL model is initialized from the SFT checkpoint and further trained with RL in simulation. To reduce the sim-to-real gap, the camera pose and robot arm configuration in the real-world setup are calibrated to match the simulation environment. 

In real-world deployment, both the SFT and RL models achieve a success rate of 8/10. However, the RL model completes the task more efficiently (Fig. 15). We observe that the SFT model tends to imitate suboptimal human teleoperation behaviors, such as rotating before pushing the drawer, and occasionally predicts near-zero actions. In contrast, the RL-trained policy learns a more direct and fluent pushing behavior. Although limited in scale, these results suggest that simulation-based RL can improve the quality and efficiency of real-world policy execution. 

## VI. CONCLUSION 

In this work, we introduced RLinf-VLA, a unified and efficient framework for reinforcement learning-based training of Vision-Language-Action models. RLinf-VLA integrates multiple simulators, algorithms, and VLA architectures, while providing flexible execution modes and system-level optimizations that significantly improve training efficiency. Extensive experiments demonstrate that models trained with RLinf-VLA achieve high performance on a wide range of simulated tasks. Moreover, our study distills actionable practices for both PPO and GRPO, guiding future research in RL-based VLA training. By open-sourcing RLinf-VLA with ongoing maintenance, we provide the community with a foundation to accelerate, standardize, and scale research in embodied intelligence. 

## ACKNOWLEDGMENTS 

This work was supported by National Natural Science Foundation of China (No.62406159, 62325405), Zhongguancun Academy (Grant No. C20250301), Beijing National Research Center for Information Science, Technology (BNRist) and Beijing Innovation Center for Future Chips. 

## REFERENCES 

- [1] Hongzhe Bi, Hengkai Tan, Shenghao Xie, Zeyuan Wang, Shuhe Huang, Haitian Liu, Ruowen Zhao, Yao Feng, Chendong Xiang, Yinze Rong, Hongyan Zhao, Hanyu Liu, Zhizhong Su, Lei Ma, Hang Su, and Jun Zhu. Motus: A unified latent action world model. _arXiv preprint arXiv:2512.13030_ , 2025. 

- [2] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _π_ 0: A vision-language-action flow model for general robot control, 2024. URL https://arxiv.org/abs/2410.24164. 

- [3] Qingwen Bu, Jisong Cai, Li Chen, Xiuqi Cui, Yan Ding, Siyuan Feng, Shenyuan Gao, Xindong He, Xu Huang, Shu Jiang, et al. Agibot world colosseo: A largescale manipulation platform for scalable and intelligent embodied systems. _arXiv preprint arXiv:2503.06669_ , 2025. 

- [4] Qingwen Bu, Yanting Yang, Jisong Cai, Shenyuan Gao, Guanghui Ren, Maoqing Yao, Ping Luo, and Hongyang Li. Univla: Learning to act anywhere with task-centric latent actions. _arXiv preprint arXiv:2505.06111_ , 2025. 

- [5] Jun Cen, Siteng Huang, Yuqian Yuan, Kehan Li, Hangjie Yuan, Chaohui Yu, Yuming Jiang, Jiayan Guo, Xin Li, Hao Luo, Fan Wang, Fan Wang, and Deli Zhao. Rynnvla002: A unified vision-language-action and world model. _arXiv preprint arXiv:2511.17502_ , 2025. 

- [6] Chilam Cheang, Sijin Chen, Zhongren Cui, Yingdong Hu, Liqun Huang, Tao Kong, Hang Li, Yifeng Li, Yuxiao Liu, Xiao Ma, et al. Gr-3 technical report. _arXiv preprint arXiv:2507.15493_ , 2025. 

- [7] Kang Chen, Zhihao Liu, Tonghe Zhang, Zhen Guo, Si Xu, Hao Lin, Hongzhi Zang, Quanlu Zhang, Zhaofei Yu, Guoliang Fan, et al. _π_ rl: Online rl fine-tuning for flow-based vision-language-action models. _arXiv preprint arXiv:2510.25889_ , 2025. 

- [8] Kang Chen et al. _π_ RL: Online rl fine-tuning for flowbased vision-language-action models, 2026. URL https: //arxiv.org/abs/2510.25889. 

- [9] Tianxing Chen, Zanxin Chen, Baijun Chen, Zijian Cai, Yibin Liu, Zixuan Li, Qiwei Liang, Xianliang Lin, Yiheng Ge, Zhenyu Gu, Weiliang Deng, Yubin Guo, Tian Nian, Xuanbing Xie, Qiangyu Chen, Kailun Su, Tianling Xu, Guodong Liu, Mengkang Hu, Huan ang Gao, Kaixuan Wang, Zhixuan Liang, Yusen Qin, Xiaokang Yang, 

Ping Luo, and Yao Mu. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation, 2025. URL https://arxiv.org/abs/2506.18088. 

- [10] Roya Firoozi, Johnathan Tucker, Stephen Tian, Anirudha Majumdar, Jiankai Sun, Weiyu Liu, Yuke Zhu, Shuran Song, Ashish Kapoor, Karol Hausman, et al. Foundation models in robotics: Applications, challenges, and the future. _The International Journal of Robotics Research (IJRR)_ , 44(5):701–739, 2025. doi: 10.1177/ 02783649241281508. 

- [11] Wei Fu et al. Areal: A large-scale asynchronous reinforcement learning system for language reasoning, 2025. URL https://arxiv.org/abs/2505.24298. 

- [12] Haoran Geng, Feishi Wang, Songlin Wei, Yuyang Li, Bangjun Wang, Boshi An, Charlie Tianyue Cheng, Haozhe Lou, Peihao Li, Yen-Jen Wang, et al. Roboverse: Towards a unified platform, dataset and benchmark for scalable and generalizable robot learning. _arXiv preprint arXiv:2504.18904_ , 2025. 

- [13] Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi Wang, Xiao Bi, et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. _arXiv preprint arXiv:2501.12948_ , 2025. 

- [14] Yanjiang Guo, Jianke Zhang, Xiaoyu Chen, Xiang Ji, Yen-Jen Wang, Yucheng Hu, and Jianyu Chen. Improving vision-language-action model with online reinforcement learning. _IEEE International Conference on Robotics and Automation (ICRA)_ , 2025. 

- [15] Tuomas Haarnoja, Aurick Zhou, Pieter Abbeel, and Sergey Levine. Soft actor-critic: Off-policy maximum entropy deep reinforcement learning with a stochastic actor. _International Conference on Machine Learning (ICML)_ , 2018. 

- [16] Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, and Weizhu Chen. Lora: Low-rank adaptation of large language models. In _International Conference on Learning Representations (ICLR)_ , 2022. 

- [17] Physical Intelligence, Ali Amin, Raichelle Aniceto, Ashwin Balakrishna, Kevin Black, Ken Conley, Grace Connors, James Darpinian, Karan Dhabalia, Jared DiCarlo, et al. _π_ 0<sup>_∗_</sup> _._ 6<sup>:avlathatlearnsfromexperience.</sup> _arXiv preprint arXiv:2511.14759_ , 2025. 

- [18] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, et al. _π_ 0 _._ 5: a visionlanguage-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 

- [19] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, et al. Droid: A large-scale in-the-wild robot manipulation dataset. In 

_Robotics: Science and Systems (RSS)_ , 2024. 

- [20] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An open-source vision-language-action model. _Conference on Robot Learning (CoRL)_ , 2024. 

- [21] Moo Jin Kim, Chelsea Finn, and Percy Liang. Finetuning vision-language-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 

- [22] Chengshu Li, Ruohan Zhang, Josiah Wong, Cem Gokmen, Sanjana Srivastava, Roberto Mart´ın-Mart´ın, Chen Wang, Gabrael Levine, Wensi Ai, Benjamin Jose Martinez, et al. Behavior-1k: A human-centered, embodied ai benchmark with 1, 000 everyday activities and realistic simulation. _CoRR_ , abs/2403.09227, 2024. URL https://doi.org/10.48550/arXiv.2403.09227. 

- [23] Haozhan Li, Yuxin Zuo, Jiale Yu, Yuhao Zhang, Zhaohui Yang, Kaiyan Zhang, Xuekai Zhu, Yuchen Zhang, Tianxing Chen, Ganqu Cui, et al. SimpleVLA-RL: Scaling VLA training via reinforcement learning. 2026. URL https://openreview.net/forum?id=TQhSodCM4r. 

- [24] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776– 44791, 2023. 

- [25] Jijia Liu, Feng Gao, Bingwen Wei, Xinlei Chen, Qingmin Liao, Yi Wu, Chao Yu, and Yu Wang. What can RL bring to VLA generalization? an empirical study. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. URL https://openreview.net/ forum?id=qmBMPInbZC. 

- [26] Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. Rdt-1b: A diffusion foundation model for bimanual manipulation. _International Conference on Learning Representations (ICLR)_ , 2025. 

- [27] Guanxing Lu, Wenkai Guo, Chubin Zhang, Yuheng Zhou, Haonan Jiang, Zifeng Gao, Yansong Tang, and Ziwei Wang. Vla-rl: Towards masterful and general robotic manipulation with scalable reinforcement learning. _arXiv preprint arXiv:2505.18719_ , 2025. 

- [28] Yueen Ma, Zixing Song, Yuzheng Zhuang, Jianye Hao, and Irwin King. A survey on vision-languageaction models for embodied ai. _arXiv preprint arXiv:2405.14093_ , 2024. 

- [29] Reginald McLean, Evangelos Chatzaroulas, Luc McCutcheon, Frank R¨oder, Tianhe Yu, Zhanpeng He, K.R. Zentner, Ryan Julian, J K Terry, Isaac Woungang, Nariman Farsad, and Pablo Samuel Castro. _Meta-World+: An Improved, Standardized, RL Benchmark_ . Advances in Neural Information Processing Systems (NeurIPS) Datasets and Benchmarks Track, 2025. 

- [30] Oier Mees, Lukas Hermann, Erick Rosete-Beas, and 

Wolfram Burgard. Calvin: A benchmark for languageconditioned policy learning for long-horizon robot manipulation tasks. _IEEE Robotics and Automation Letters (RA-L)_ , 7(3):7327–7334, 2022. doi: 10.1109/LRA.2022. 3172793. 

- [31] Mayank Mittal, Pascal Roth, James Tigue, Antoine Richard, Octi Zhang, Peter Du, Antonio Serrano-Mu˜noz, Xinjie Yao, Ren´e Zurbr¨ugg, et al. Isaac lab: A gpuaccelerated simulation framework for multi-modal robot learning. _arXiv preprint arXiv:2511.04831_ , 2025. 

- [32] Soroush Nasiriany, Abhiram Maddukuri, Lance Zhang, Adeet Parikh, Aaron Lo, Abhishek Joshi, Ajay Mandlekar, and Yuke Zhu. _RoboCasa: Large-Scale Simulation of Everyday Tasks for Generalist Robots_ . Robotics: Science and Systems (RSS), 2024. 

- [33] Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, et al. Open x-embodiment: Robotic learning datasets and rt-x models. _IEEE International Conference on Robotics and Automation (ICRA)_ , pages 6892–6903, 2024. 

- [34] Rafael Rafailov, Archit Sharma, Eric Mitchell, Stefano Ermon, Christopher D. Manning, and Chelsea Finn. Direct preference optimization: Your language model is secretly a reward model. _Advances in Neural Information Processing Systems (NeurIPS)_ , 2023. 

- [35] John Schulman, Philipp Moritz, Sergey Levine, Michael I. Jordan, and P. Abbeel. High-dimensional continuous control using generalized advantage estimation. _CoRR_ , abs/1506.02438, 2015. URL https://api.semanticscholar.org/CorpusID:3075448. 

- [36] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [37] Dhruv Shah, Bła˙zej Osi´nski, Sergey Levine, et al. Lmnav: Robotic navigation with large pre-trained models of language, vision, and action. _Conference on Robot Learning (CoRL)_ , pages 492–504, 2022. 

- [38] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, YK Li, Yang Wu, et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. _arXiv preprint arXiv:2402.03300_ , 2024. 

- [39] Guangming Sheng, Chi Zhang, Zilingfeng Ye, Xibin Wu, Wang Zhang, Ru Zhang, Yanghua Peng, Haibin Lin, and Chuan Wu. Hybridflow: A flexible and efficient rlhf framework. In _Proceedings of the Twentieth European Conference on Computer Systems_ , EuroSys ’25, page 1279–1297, New York, NY, USA, 2025. Association for Computing Machinery. ISBN 9798400711961. doi: 10.1145/3689031.3696075. URL https://doi.org/10.1145/ 3689031.3696075. 

- [40] Guangming Sheng et al. Hybridflow: A flexible and efficient rlhf framework. _arXiv preprint arXiv: 2409.19256_ , 2024. 

- [41] Richard S Sutton and Andrew G Barto. _Reinforcement Learning: An Introduction_ . MIT Press, 1998. 

- [42] Shuhan Tan, Kairan Dou, Yue Zhao, and Philipp Kr¨ahenb¨uhl. Interactive post-training for vision-language-action models. _arXiv preprint arXiv:2505.17016_ , 2025. 

- [43] Stone Tao, Fanbo Xiang, Arth Shukla, Yuzhe Qin, Xander Hinrichsen, Xiaodi Yuan, Chen Bao, Xinsong Lin, Yulin Liu, Tse kai Chan, Yuan Gao, Xuanlin Li, Tongzhou Mu, Nan Xiao, Arnav Gurha, Viswesh Nagaswamy Rajesh, Yong Woo Choi, Yen-Ru Chen, Zhiao Huang, Roberto Calandra, Rui Chen, Shan Luo, and Hao Su. _ManiSkill3: GPU Parallelized Robotics Simulation and Rendering for Generalizable Embodied AI_ . Robotics: Science and Systems, 2025. 

   - [51] Jinliang Zheng, Jianxiong Li, Zhihao Wang, Dongxiu Liu, Xirui Kang, Yuchun Feng, Yinan Zheng, Jiayin Zou, Yilun Chen, Jia Zeng, et al. X-vla: Soft-prompted transformer as scalable cross-embodiment vision-languageaction model. _arXiv preprint arXiv:2510.10274_ , 2025. 

   - [52] Zilin Zhu et al. slime: An llm post-training framework for rl scaling. https://github.com/THUDM/slime, 2025. GitHub repository. Corresponding author: Xin Lv. 

- [44] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. _Octo: An Open-Source Generalist Robot Policy_ . Robotics: Science and Systems, 2024. 

- [45] Andrew Wagenmaker, Mitsuhiko Nakamoto, Yunchu Zhang, Seohong Park, Waleed Yagoub, Anusha Nagabandi, Abhishek Gupta, and Sergey Levine. Steering your diffusion policy with latent space reinforcement learning. _Conference on Robot Learning_ , 2025. 

- [46] Junjie Wen, Yichen Zhu, Jinming Li, Zhibin Tang, Chaomin Shen, and Feifei Feng. Dexvla: Visionlanguage model with plug-in diffusion expert for general robot control. _arXiv preprint arXiv:2502.05855_ , 2025. 

- [47] Qiying Yu, Zheng Zhang, Ruofei Zhu, Yufeng Yuan, Xiaochen Zuo, YuYue, Weinan Dai, Tiantian Fan, Gaohong Liu, Juncai Liu, LingJun Liu, Xin Liu, Haibin Lin, Zhiqi Lin, Bole Ma, Guangming Sheng, Yuxuan Tong, Chi Zhang, Mofan Zhang, Ru Zhang, Wang Zhang, Hang Zhu, Jinhua Zhu, Jiaze Chen, Jiangjie Chen, Chengyi Wang, Hongli Yu, Yuxuan Song, Xiangpeng Wei, Hao Zhou, Jingjing Liu, Wei-Ying Ma, Ya-Qin Zhang, Lin Yan, Yonghui Wu, and Mingxuan Wang. DAPO: An open-source LLM reinforcement learning system at scale. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. URL https://openreview.net/forum?id=2a36EMSSTp. 

- [48] Zhecheng Yuan, Tianming Wei, Shuiqi Cheng, Gu Zhang, Yuanpei Chen, and Huazhe Xu. Learning to manipulate anywhere: A visual generalizable framework for reinforcement learning. _arXiv preprint arXiv:2407.15815_ , 2024. 

- [49] Zijian Zhang, Kaiyuan Zheng, Zhaorun Chen, Joel Jang, Yi Li, Siwei Han, Chaoqi Wang, Mingyu Ding, Dieter Fox, and Huaxiu Yao. Grape: Generalizing robot policy via preference alignment. _arXiv preprint arXiv:2411.19309_ , 2024. 

- [50] Tony Z. Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware. In _Robotics: Science and Systems (RSS)_ , pages 1–16. Robotics: Science and Systems, 2023. URL https://doi.org/10.15607/RSS.2023. XIX.016. 

