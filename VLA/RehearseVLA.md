---
title: "RehearseVLA: Simulated Post-Training for VLAs with Physically-Consistent World Model"
date: "2026"
venue: "CVPR 2026"
url: https://openaccess.thecvf.com/content/CVPR2026/html/Xiao_RehearseVLA_Simulated_Post-Training_for_VLAs_with_Physically-Consistent_World_Model_CVPR_2026_paper.html
pdf: https://openaccess.thecvf.com/content/CVPR2026/papers/Xiao_RehearseVLA_Simulated_Post-Training_for_VLAs_with_Physically-Consistent_World_Model_CVPR_2026_paper.pdf
converter: pymupdf4llm
---

> **[PDF を開く](https://openaccess.thecvf.com/content/CVPR2026/papers/Xiao_RehearseVLA_Simulated_Post-Training_for_VLAs_with_Physically-Consistent_World_Model_CVPR_2026_paper.pdf)** / [論文ページ](https://openaccess.thecvf.com/content/CVPR2026/html/Xiao_RehearseVLA_Simulated_Post-Training_for_VLAs_with_Physically-Consistent_World_Model_CVPR_2026_paper.html)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **RehearseVLA: Simulated Post-Training for VLAs with Physically-Consistent World Model** 

Junjin Xiao<sup>1</sup> Yandan Yang Xinyuan Chang Ronghan Chen Feng Xiong Mu Xu Wei-Shi Zheng<sup>1</sup><sup>_,_2</sup> Qing Zhang<sup>1</sup><sup>_,_2</sup><sup>_,∗_</sup> 

1School of Computer Science and Engineering, Sun Yat-sen University, China 

- 2Key Laboratory of Machine Intelligence and Advanced Computing, Ministry of Education, China 


Figure 1. **VLA exploration in world model and performance comparison on LIBERO benchmarks.** 

## **Abstract** 

_Vision-Language-Action (VLA) models trained via imitation learning suffer from significant performance degradation in data-scarce scenarios due to their reliance on large-scale demonstration datasets. Although reinforcement learning (RL)-based post-training has proven effective in addressing data scarcity, its application to VLA models is hindered by the non-resettable nature of real-world environments. This limitation is particularly critical in high-risk domains such as industrial automation, where interactions often induce state changes that are costly or infeasible to revert. Furthermore, existing VLA approaches lack a reliable mechanism for detecting task completion, leading to redundant actions that reduce overall task success rates. To address these challenges, we propose RehearseVLA, an RLbased post-training framework that replaces physical interaction with a low-cost world model-based virtual simulator. RehearseVLA consists of two key components: (1) a physically-consistent world simulator that generates temporally consistent future visual observations, and (2) a visionlanguage model (VLM)-guided instant reflector that pro-_ 

> _∗_ Corresponding author (zhangq93@mail.sysu.edu.cn). 

_vides continuous reward signals and predicts action termination. This simulated environment enables VLA models to safely explore and generalize beyond their initial imitation learning distribution. Our method achieves notable performance gains with as few as five expert demonstrations per task. Experiments on complex robotic manipulation tasks demonstrate that RehearseVLA effectively overcomes the data inefficiency, safety constraints, and inefficient execution of conventional VLA models that rely on real-world interaction, offering a practical and scalable solution for post-training in resource-constrained settings. Our code is available at https://github.com/ iSEE-Laboratory/RehearseVLA._ 

## **1. Introduction** 

Vision-Language-Action (VLA) models have emerged as a central paradigm for autonomous agents, enabling endto-end mapping from high-level language instructions to low-level motor commands by integrating vision, language, and control. These models have demonstrated considerable promise in robotic manipulation [6, 24], autonomous driving [29, 46, 51–53], and navigation [20, 54]. Most existing 

20867 


Figure 2. **Comparison of three VLA training paradigms.** 

approaches rely on supervised fine-tuning through imitation learning, building upon pre-trained vision-language models [44] to align semantic intent with physical execution via cross-modal representations. 

However, imitation learning methods [25] are inherently constrained by the limited availability of high-quality demonstrations. In many real-world scenarios, collecting diverse and safe human demonstrations is prohibitively expensive and often infeasible due to safety concerns and environmental complexity. Furthermore, such methods generalize poorly to novel tasks or unseen objects, and their performance degrades under few-shot conditions. 

To overcome these shortcomings, recent works [34, 42] have turned to reinforcement learning (RL) [39] to enable agents to learn through interaction. Current RL strategies fall into two categories. The first involves real-world learning with human feedback, which captures realistic environmental dynamics but suffers from non-resettable interactions, high trial costs, and limited reproducibility, rendering it unsuitable for safety-critical applications. The second relies on simulator-based learning, which avoids physical risks but introduces other challenges, including substantial development effort, limited sim-to-real transfer, and difficulty adapting to new objects or dynamic scene changes, thereby restricting its practical applicability. 

These limitations motivate us to think about a question: _Is there an “ideal testbed” that avoids real-world risks while providing greater flexibility and richer semantic understanding than conventional simulators?_ We find that video-based world model offers a promising solution. Equipped with action-conditioned future prediction and a persistent latent scene representation, world model can generate visually plausible future image sequences, allowing safe, low-cost simulation of action outcomes, as well as policy exploration and refinement without physical interaction. 

In this work, we introduce RehearseVLA, a world model-based reinforcement learning framework that improves policy generalization under data scarcity while respecting real-world safety constraints, as shown in Fig- 

ure 2. RehearseVLA consists of two components. The first is a physically-consistent world simulator that functions as an interactive future-frame predictor, synthesizing action-conditioned image sequences that capture postinteraction object states and surrounding scene structure. To ensure physical consistent of our world model, we propose a geometry-aware feature injection strategy, which leverages latent feature from VGGT [48] as additional condition. The second is a VLM-guided instant reflector that functions as a semantics-aware reward module. It provides continuous reward signals by evaluating the semantic alignment between predicted visual frames and the input language instruction. This assessment supports policy optimization and enables real-time detection of task completion. Upon confirming successful execution (e.g., when the goal state is reached), the reflector immediately terminates the action sequence to prevent redundant or disruptive subsequent actions. 

In summary, our contributions are: 

- We propose RehearseVLA, a framework that enables low-cost, safe reinforcement learning post-training for VLA policies under extreme data scarcity, eliminating the need for real-world interaction. 

- We propose a geometry-aware feature injection strategy via injecting latent feature from VGGT to ensure physical consistent of world model. 

- We introduce a real-time termination mechanism via the instant reflector, which dynamically assesses task completion by evaluating semantic alignment between predicted visual trajectories and language instructions, thereby preventing redundant post-success actions. 

## **2. Related Work** 

**Vision-Language-Action Models.** Leveraging advancements in pre-trained vision foundation models [14, 35, 38], large language models (LLMs) [4, 8, 45], and visionlanguage models (VLMs) [2, 13, 27, 28, 32, 33], VisionLanguage-Action (VLA) frameworks [9, 12, 24, 43] have emerged as a powerful approach for embodied intelligence. Specifically, DiffusionPolicy [12] proposes a diffusionbased policy that generates robot actions through a conditional denoising diffusion process in the action space, iteratively refining actions based on visual observations. OpenVLA [24] integrates robotic actions into a language modeling framework by mapping action sequences to discrete tokens within a large language model. The recent work OpenVLA-OFT [25] further converts discrete action sequences into continuous representations, achieving improved efficiency and performance. 

**Reinforcement Learning for VLA Systems.** Recent advances in reinforcement learning (RL) [39, 41] have demonstrated considerable potential in enhancing decision- 

20868 


Figure 3. **Overview of RehearseVLA.** Our framework comprises: (1) a _Training Data Strategy_ that augments human demonstrations trajectories with VLA self-explored trajectories to train the World Simulator; (2) an _Optimization Loop_ where the VLA model generates actions, the simulator predicts future observations, and the Instant Reflector generates feedback; and (3) _Reward & End Signal_ provides trajectory-wise reward and end signals for RL optimization. 

making capabilities of large language models (LLMs) [15, 26, 30, 36]. This progress has spurred growing interest in applying RL to Vision-Language-Action (VLA) systems [10, 22, 34, 42]. Unlike supervised fine-tuning (SFT), RL enables agents to refine policies through interaction. This paradigm supports autonomous exploration and improved robustness to partial observability, allowing VLA models to generalize to unseen scenarios while reducing reliance on costly human demonstrations. However, existing RLbased VLA methods typically require real-world interaction, which is often infeasible in high-risk scenarios. 

**World Models.** World models [3, 5], which are learned dynamical simulators that approximate environmental dynamics, have become foundational for safe and sample-efficient agent training. Early works [16–18] demonstrated the effectiveness of model-based reinforcement learning in virtual environments, enabling agents to plan via imagined trajectories without real-world interaction. However, these methods typically rely on on-policy data, limiting their generalization to specific environments and downstream tasks. Building on advances in diffusion-based video generation [7, 19, 40, 47, 49, 50], we propose a framework that trains a world model on offline demonstration data and keeps it fixed during policy learning to predict future visual observations for VLA models. 

## **3. Preliminary** 

**Vision-Language-Action Model.** Vision-language-action (VLA) models bridge natural language instructions with robotic control by translating semantic goals into lowlevel actions while grounding language in multimodal observations. Following recent VLA frameworks such as OpenVLA-OFT [25], the policy is implemented as a de- 

terministic mapping that leverages a pretrained visionlanguage model to extract multimodal features, followed by a lightweight action head for continuous control. Specifically, given a history of RGB observations **o** 1: _t_ , proprioceptive states **s** 1: _t_ (e.g., joint angles or end-effector poses), and a language instruction **g** , the policy predicts a action as: 


where _πθ_ denotes a deterministic policy parameterized by a finetuned foundation model and a trainable action head. 

**Reinforcement Learning.** Reinforcement learning (RL) formulates decision-making as a Markov Decision Process (MDP): _M_ = ( _S, A, P, R, γ_ ), where _S_ is the state space (comprising visual observations **o** _t_ and proprioceptive states **s** _t_ ), _A_ is the action space (e.g., continuous control commands **a** _t ∈_ R<sup>_D_</sup> ), _P_ denotes the transition dynamics, _R_ is the reward function, and _γ ∈_ [0 _,_ 1] is the discount factor. The objective is to learn a policy _πθ_ ( **o** 1: _t,_ **s** 1: _t,_ **g** ) that maximizes the expected return: 


where _rt_ = _R_ ( **o** 1: _t,_ **g** ). In practice, policy gradient methods often introduce stochasticity during training to enable exploration. The policy is updated using gradients: 


where _A_ ( _·_ ) is the advantage function that evaluates action quality relative to a baseline. 

## **4. Method** 

Figure 3 presents the overview of our framework. Prior VLA approaches [24, 25] typically rely on either real-world 

20869 


Figure 4. **Overview of physically-consistent world simulator.** 

interaction or conventional simulators to provide observations for action prediction. In contrast, our framework eliminates the need for physical interaction by leveraging a _physically-consistent world simulator_ that generates temporally consistent future visual observations at low cost. Specifically, the VLA policy _πθ_ maps the current RGB observation **o** _t_ , language instruction **g** , and proprioceptive state **s** _t_ (comprising the 6D end-effector pose and 1D gripper state) to a continuous action **a** _t_ . The next proprioceptive state **s** _t_ +1 is then computed deterministically using forward kinematics. The world simulator takes the resulting proprioceptive state **s** _t_ +1 as input and predicts the subsequent visual observation **o** _t_ +1. This imagined observation, together with **s** _t_ +1, is fed back into the VLA policy to predict the next action **a** _t_ +1. The rollout terminates either when the maximum timestep is reached or when the _VLM-guided instant reflector_ , which evaluates semantic alignment between the predicted visual trajectory and the language instruction, confirms task success and issues a termination signal. During training, we collect _N_ simulated trajectories from this virtual environment and use them for RL optimization of the VLA policy within RehearseVLA. 

### **4.1. Physically-Consistent World Simulator** 

Figure 4 presents an overview of our world simulator, which is designed to predict future observations conditioned on a given action sequence. Akin to [23], we first translate the predicted action into a proprioceptive state **s** _t_ +1 via forward kinematics, and project it onto the image plane to generate an action map. This action map comprises a foreground marker that encodes the projected pose (e.g., position and orientation) and a uniformly black background, which serves to maximize visual contrast and minimize interference with the underlying scene content. The resulting action map is then combined with a historical observation sampled from a memory bank and jointly injected into a U-Net based denoising diffusion network as pixel-level conditioning signals. To ensure that the synthesized future frames remain physically plausible and geometrically coherent with the reference observation, we introduce a geometry-aware feature injection mechanism. Specifically, 

we extract complementary features from two pre-trained encoders: (i) VGGT [48], which excels at preserving finegrained geometric structures and spatial layouts of the reference image; and (ii) CLIP [38], which captures high-level semantic and contextual information. These features are integrated into the denoising U-Net through cross-attention layers at multiple resolutions, enabling the model to simultaneously respect both local geometric fidelity and global semantic consistency during future frame synthesis. This dual-path injection strategy not only enhances the realism of generated observations but also improves temporal coherence and physical plausibility in long-horizon predictions. 

To train the world model, we find that relying solely on expert demonstrations from the LIBERO benchmark [31] limits generalization to unseen state-action sequences. To address this, we augment the training data by enabling autonomous exploration in the LIBERO simulator. Specifically, we deploy the supervised fine-tuned OpenVLA-OFT policy [25] to predict actions and execute them in the simulator, which yields the corresponding next proprioceptive state **s** _t_ +1 and observation **o** _t_ +1. To further enhance data diversity, we introduce controlled stochasticity by training a scale head that predicts the log-scale parameter **_β_** _t_ of a Laplace distribution, with the OpenVLA-OFT action **_µ_** _t_ as the location parameter: **a** _t ∼_ Laplace( **_µ_** _t,_ **_β_** _t_ ). These perturbed actions are executed to collect additional ( **o** _t,_ **s** _t,_ **a** _t,_ **s** _t_ +1 _,_ **o** _t_ +1) transition tuples. Finally, we combine these autonomously collected trajectories with the original human-demonstrated successful trajectories from LIBERO [31] to form a diverse and robust training dataset for the world simulator. Additional analysis of the world simulator are provided in the supplementary material. 

### **4.2. VLM-Guided Instant Reflector** 

Previous methods [34, 42] rely on simulators to provide binary task success signals, using sparse discrete rewards for RL post-training. These approaches suffer from a key limitation: the lack of termination-aware feedback, causing policies to often continue executing redundant actions after task completion (e.g., over-scooping after object placement). To address this, we propose a VLM-guided instant reflector that leverages a pretrained vision-language model to provide a continuous-valued reward signal. 

Given a video of imagined observations **o** 1: _t_ and a language instruction **g** , the instant reflector predicts a stepwise reward _R_ ( **o** 1: _t,_ **g** ) _∈_ [0 _,_ 1] for each time step _t_ , which estimates the probability that the task has been successfully completed by time _t_ . The architecture consists of a frozen vision encoder _E_ vision that extracts patch embeddings from video frames, a frozen LLM _E_ LLM that performs crossmodal reasoning over the visual-language sequence, and a lightweight reward head _Rθ_ that computes: 


20870 

Table 1. **Success rate comparison on the LIBERO benchmark.** We report success rates for each method using the same setting with only 5 demonstrations per task. 


Figure 5. **Comparison with SFT on multi-goal tasks.** Note that all results are collected every 5 training steps for three distinct goals. 

where _σ_ is the sigmoid function and _ht_ is the pooled multimodal embedding from the LLM at time _t_ . The termination signal is triggered at the timestep _t_ where _R_ ( **o** 1: _t,_ **g** ) _> η_ , with threshold _η_ = 0 _._ 5. 

For training, we utilize per-frame binary success labels: for each trajectory, every timestep _t_ is annotated with _yt ∈{_ 0 _,_ 1 _}_ , indicating whether the task is completed at or before _t_ . These labels are derived from two sources: (1) expert trajectories from the LIBERO dataset [31], where success is determined by task-specific criteria, and (2) policygenerated trajectories collected in simulator (Section 4.1). The reward head _Rθ_ is trained with BCE loss: 


This supervision enables the reflector to recognize task completion as soon as it occurs. During RL, we use the reward sparsely: the return is computed using a single reward assigned at the termination timestep (or at _T_ if no termination occurs). 

This design enables RehearseVLA to support real-time termination while achieving both high sample efficiency and stable policy learning. In contrast, prior VLA posttraining approaches [34, 42] rely on binary rewards (e.g., 1 for success, 0 for failure), which lead to degenerate advantage estimates when rollout trajectories are homogeneous, i.e., when all episodes succeed or all fail. In such cases, the empirical advantage values collapse to zero across the batch, providing no learning signal for policy updates and 

drastically reducing training efficiency. By instead employing a continuous reward signal in the range [0 _,_ 1] that reflects fine-grained task progress, our method ensures nontrivial advantage estimates. This eliminates the need to balance successful and failed rollouts during data collection, enabling more efficient use of samples. 

### **4.3. Post Training of VLA Model** 

Our reinforcement learning pipeline employs a RLOO [1] objective with continuous reward signals; the full algorithm is provided in the supplementary material. Following [42], training proceeds in three stages: rollout generation, advantage estimation, and policy optimization. 

During rollout, we generate trajectories _τ_ = ( **o** 1: _T ,_ **s** 1: _T ,_ **g** _,_ **a** 1: _T_ ) using the world simulator (Section 4.1). Starting from an initial observation **o** 1, proprioceptive state **s** 1, and language instruction **g** , the deterministic VLA policy _πθ_ predicts a base action **_µ_** _t_ = _πθ_ ( **o** 1: _t,_ **s** 1: _t,_ **g** ). A separate scale head, trained to model action uncertainty, outputs a log-scale parameter **_β_** _t_ . Together, they define a factorized Laplace distribution, from which the executed action **a** _t_ is sampled. This enables adaptive, uncertainty-aware exploration. The world simulator then predicts the next observation **o** _t_ +1 using proprioceptive state **s** _t_ +1. The VLM-guided instant reflector evaluates the partial visual trajectory **o** 1: _t_ +1 and outputs a step-wise reward _R_ ( **o** 1: _t_ +1 _,_ **g** ) _∈_ [0 _,_ 1]. Rollout terminates either at the maximum timestep _T_ or when _R_ ( **o** 1: _t_ +1 _,_ **g** ) _> η_ . For RL, we assign a single 

20871 


Figure 6. **Rendering comparison of world simulator trained with and without extra data.** 

trajectory-wise reward _Rn_ = _R_ ( **o** 1: _t_ end _,_ **g** ), where _t_ end is the termination or final timestep. 

We adopt Leave-One-Out Proximal Policy Optimization (LOOP) [11] that combines RLOO [1] based advantage estimation and PPO [41] for policy updating. For each initial state, we generate _N_ rollouts _{τ_ 1 _, . . . , τN }_ using a fixed behavior policy _πϕ_ (the policy at the beginning iteration). Each trajectory receives a scalar reward _Rn_ from the instant reflector. The RLOO baseline for trajectory _n_ is the average reward of the other rollouts: 


where _An_ is the trajectory-wise advantage. To update the policy, we treat both the current and behavior policies as inducing stochastic action distributions via their action and scale heads. The importance ratio at timestep _t_ of trajectory _n_ is computed as: 


where _pθ_ and _pϕ_ denote the action distributions induced by the current policy _πθ_ and behavior policy _πϕ_ , respectively, each modeled as a product of independent Laplace distributions over action dimensions. The policy is optimized via 

Table 2. **Comparison with simulator-based RL method.** 

|Method|Goal|Object|Spatial|Long|
|---|---|---|---|---|
|RIPT-VLA [42]|86.2|83.4|88.6|58.4|
|Ours|86.4|86.6|87.6|57.8|


the clipped PPO objective: 


with _ϵ_ representing to the clipping threshold. Note that the advantage _An_ is broadcasted to all timesteps. 

### **4.4. Implementation Details** 

Experiments were performed on 8 NVIDIA H20 GPUs (96 GB VRAM each), with a total training time of approximately 48 hours. We adopt LoRA [21] with rank 32 for parameter-efficient fine-tuning of the vision-language backbone, while the action head and scale head are trained with full parameters. We use a batch size of 4. The LoRA adapters are optimized with a learning rate of 1 _×_ 10<sup>_−_4</sup> , and the action/scale heads are trained with a learning rate of 1 _×_ 10<sup>_−_5</sup> . We set the number of rollouts per iteration to _N_ = 8 and the PPO clipping threshold to _ϵ_ = 0 _._ 1. 

20872 


Figure 7. **Real-world experiment on task “clean table”. Full video result can be found in the supplementary material.** 

|Method|Clean table|Put green toy|Put red toy|Put orange toy|
|---|---|---|---|---|
|OpenVLA-OFT|20|30|30|20|
|Ours|30|50|40|50|


Table 3. **Comparison results of real-world experiments.** 

## **5. Experiments** 

learning conditioned policies with minimal training iterations. Table 2 presents a comparison with RIPT-VLA [42], a simulator-based reinforcement learning approach. Our method achieves comparable performance while offering a crucial practical advantage: it is readily deployable in realworld settings. In contrast, RIPT-VLA is limited to simulated environments. 

**Benchmarks.** We evaluate our model on the LIBERO benchmark [31], a simulation-based robotic learning platform designed for vision-language manipulation tasks. The benchmark includes four task suites targeting distinct cognitive challenges: LIBERO-Spatial focusing on spatial reasoning via object arrangement; LIBERO-Goal assessing goal-conditioned planning with end-state requirements; LIBERO-Object testing object-centric manipulation across categories; LIBERO-10 (LIBERO-Long) addressing prolonged sequential decision-making. Each suite contains 10 tasks with 50 trajectories for training and 50 for testing per task; we train OpenVLA-OFT using only 5 trajectories from the training split to validate performance under extreme data scarcity, while evaluating on the full trajectory test split to demonstrate the generalization capability. 

**Baselines.** We compare our method with five state-ofthe-art supervised fine-tuning (SFT) methods including _π_ 0 [6], _π_ 0 + FAST [37], OpenVLA [24], UniVLA [9], OpenVLA-OFT [25] and one simulator-based RL method RIPT-VLA [42]. For fair evaluation, all baselines are retrained under identical 5-trajectory per-task constraints, with performance metrics reported on the complete test set. 

### **5.1. Comparison with State-of-the-art Methods** 

Table 1 presents success rate comparison between our method and the baseline models. As shown, our method gains higher task success rate, demonstrating the effectiveness of our proposed post-training strategy. Figure 5 further compares our method and the supervised fine-tuning (SFT) baseline on multi-goal tasks, where we can see that our approach achieves superior performance within only 20 training steps, clearly outperforming the compared SFT model. This rapid convergence and early dominance highlight the efficiency and effectiveness of our method in 

### **5.2. Real-world Experiment** 

We conduct real-world experiments across four tasks, _i.e_ ., “clean table”, “put green toy in cabinet”, “put red toy in cabinet”, and “put orange toy in cabinet”, Figure 7 shows several sampled frames from the “clean table” task, where the goal is to pick up three toys and place them into the bucket. For each task, we collect 10 trajectories for both policy SFT and world model fine-tuning. As shown in the table 3, our method outperforms OpenVLA-OFT on all four tasks, validating that our framework can be effectively transferred to real-world environments. 

### **5.3. Ablation Studies** 

**Effect of World Simulator.** We study how the world simulator’s generative quality affects performance. Figure 6 compares two variants: (1) w/o extra: trained only on successful human trajectories; and (2) w/ extra: augmented with our data containing both success and failure cases. Without exposure to suboptimal actions, the former fails to model resulting object states, leading to poor tracking under VLA prediction errors. Our enhanced simulator substantially improves arm tracking and interaction fidelity. Table 5 confirms that low-fidelity simulation degrades VLA training. Additional analysis, ablations, and videos are in the supplementary material. 

**Effect of Instant Reflector.** Table 5 compares two variants: (1) w/o reward head: using a pre-trained VLM with promptbased binary classification; and (2) w/ reward head: a trainable module scoring actions on a continuous scale. Experiments show that off-the-shelf VLMs offer limited gains and can impair learning in complex tasks due to misalignment with fine-grained action evaluation. In contrast, our reward head provides more accurate and reliable action assessment. 

20873 


Figure 8. **Post-success failure in VLA execution.** An illustrative example for “put the wine bottle on top of the cabinet” shows the VLA model completes the task (a-b), but fails due to delayed termination (c-e), validating the necessity of dynamic termination mechanism. 

Table 4. **Comparison of task termination strategy under realistic feedback constraints.** Note, all compared methods are evaluated under the setting where ground-truth termination feedback is unavailable, while our method autonomously detects task completion via the proposed reward model. Success rates are measured when reaching the maximum action steps. 

|Method|LIBERO-Goal|LIBERO-Object|LIBERO-Spatial|LIBERO-Long|Average|
|---|---|---|---|---|---|
|_π_0[6]|55.4|71.0|72.6|20.6|54.9|
|_π_0+FAST [37]|21.2|74.0|44.8|15.0|38.75|
|OpenVLA [24]|68.4|47.4|59.8|26.6|50.55|
|UniVLA [9]|72.0|75.2|66.4|48.0|65.4|
|OpenVLA-OFT [25]|67.4|73.8|71.2|39.8|63.05|
|OpenVLA-OFT + Post-training (Ours)|**85.0**|**78.4**|**78.4**|**57.8**|**74.9**|


Table 5. **Ablation studies.** We evaluate how the extra training data for world simulator learning and the reward head for trajectory scoring affect the performance of our method. 

|Extra Data|Reward Head|Goal|Object|Spatial|Long|
|---|---|---|---|---|---|
|||68.4|75.2|73.2|42.2|
|✓||79.8|81.8|78.4|44.6|
||✓|68.8|76.4|74.4|43.8|
|✓|✓|**86.4**|**86.6**|**87.6**|**57.8**|


on diverse training data to achieve high-fidelity simulation and accurate task evaluation. We anticipate that future advances in general-purpose world models will alleviate this dependency. Second, policy optimization in our framework is currently slower than in concurrent methods due to computational bottlenecks in simulator-based trajectory generation. Addressing these challenges through more efficient simulation will be a key focus of our future work. 

## **6. Conclusion** 

**Effect of Termination Signals.** Table 4 further validates our method’s ability to detect task success. Unlike conventional approaches, which rely on provided termination signals, our framework uses a VLM-guided instant reflector to dynamically assess completion and stop execution promptly. To isolate this advantage, we force all baselines to adhere strictly to the full horizon, while our method terminates based on reflector predictions. As shown, baselines suffer performance degradation due to redundant postsuccess actions that perturb object states (see Figure 8). In contrast, our approach preserves task outcomes by halting immediately upon success detection, demonstrating the reflector’s effectiveness in enabling timely termination. 

### **5.4. Limitations and Future Work** 

Despite the effectiveness of our approach in enhancing VLA manipulation capabilities, several limitations remain. First, both the world simulator and the instant reflector rely 

We present RehearseVLA, a post-training framework for Vision-Language-Action (VLA) models that eliminates the need for costly and potentially unsafe interactions with physical environments. By leveraging a physically consistent world simulator, enhanced with a geometry-aware feature injection strategy, RehearseVLA enables safe and low-cost exploration in virtual settings. Furthermore, our VLM-guided instant reflector supports dynamic task-aware termination, preventing redundant post-success actions that could otherwise disrupt task outcomes. Extensive experiments on complex robotic manipulation tasks demonstrate that RehearseVLA achieves superior performance, particularly in low-data regimes. 

**Acknowledgement.** This work was supported by the National Natural Science Foundation of China (62471499), the Guangdong Basic and Applied Basic Research Foundation (2023A1515030002). 

20874 

## **References** 

- [1] Arash Ahmadian, Chris Cremer, Matthias Gall´e, Marzieh Fadaee, Julia Kreutzer, Olivier Pietquin, Ahmet Ust¨un,<sup>¨</sup> and Sara Hooker. Back to basics: Revisiting reinforce style optimization for learning from human feedback in llms. _arXiv preprint arXiv:2402.14740_ , 2024. 5, 6 

- [2] Jean-Baptiste Alayrac, Jeff Donahue, Pauline Luc, Antoine Miech, Iain Barr, Yana Hasson, Karel Lenc, Arthur Mensch, Katherine Millican, Malcolm Reynolds, et al. Flamingo: a visual language model for few-shot learning. In _NeurIPS_ , 2022. 2 

- [3] Mido Assran, Adrien Bardes, David Fan, Quentin Garrido, Russell Howes, Matthew Muckley, Ammar Rizvi, Claire Roberts, Koustuv Sinha, Artem Zholus, et al. V-jepa 2: Selfsupervised video models enable understanding, prediction and planning. _arXiv preprint arXiv:2506.09985_ , 2025. 3 

- [4] Jinze Bai, Shuai Bai, Yunfei Chu, Zeyu Cui, Kai Dang, Xiaodong Deng, Yang Fan, Wenbin Ge, Yu Han, Fei Huang, Binyuan Hui, Luo Ji, Mei Li, Junyang Lin, Runji Lin, Dayiheng Liu, Gao Liu, Chengqiang Lu, Keming Lu, Jianxin Ma, Rui Men, Xingzhang Ren, Xuancheng Ren, Chuanqi Tan, Sinan Tan, Jianhong Tu, Peng Wang, Shijie Wang, Wei Wang, Shengguang Wu, Benfeng Xu, Jin Xu, An Yang, Hao Yang, Jian Yang, Shusheng Yang, Yang Yao, Bowen Yu, Hongyi Yuan, Zheng Yuan, Jianwei Zhang, Xingxuan Zhang, Yichang Zhang, Zhenru Zhang, Chang Zhou, Jingren Zhou, Xiaohuan Zhou, and Tianhang Zhu. Qwen technical report. _arXiv preprint arXiv:2309.16609_ , 2023. 2 

- [5] Philip J. Ball, Jakob Bauer, Frank Belletti, Bethanie Brownfield, Ariel Ephrat, Shlomi Fruchter, Agrim Gupta, Kristian Holsheimer, Aleksander Holynski, Jiri Hron, Christos Kaplanis, Marjorie Limont, Matt McGill, Yanko Oliveira, Jack Parker-Holder, Frank Perbet, Guy Scully, Jeremy Shar, Stephen Spencer, Omer Tov, Ruben Villegas, Emma Wang, Jessica Yung, Cip Baetu, Jordi Berbel, David Bridson, Jake Bruce, Gavin Buttimore, Sarah Chakera, Bilva Chandra, Paul Collins, Alex Cullum, Bogdan Damoc, Vibha Dasagi, Maxime Gazeau, Charles Gbadamosi, Woohyun Han, Ed Hirst, Ashyana Kachra, Lucie Kerley, Kristian Kjems, Eva Knoepfel, Vika Koriakin, Jessica Lo, Cong Lu, Zeb Mehring, Alex Moufarek, Henna Nandwani, Valeria Oliveira, Fabio Pardo, Jane Park, Andrew Pierson, Ben Poole, Helen Ran, Tim Salimans, Manuel Sanchez, Igor Saprykin, Amy Shen, Sailesh Sidhwani, Duncan Smith, Joe Stanton, Hamish Tomlinson, Dimple Vijaykumar, Luyu Wang, Piers Wingfield, Nat Wong, Keyang Xu, Christopher Yew, Nick Young, Vadim Zubov, Douglas Eck, Dumitru Erhan, Koray Kavukcuoglu, Demis Hassabis, Zoubin Gharamani, Raia Hadsell, A¨aron van den Oord, Inbar Mosseri, Adrian Bolton, Satinder Singh, and Tim Rockt¨aschel. Genie 3: A new frontier for world models. 2025. 3 

- [6] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, 

and Ury Zhilinsky. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 1, 5, 7, 8 

- [7] Andreas Blattmann, Tim Dockhorn, Sumith Kulal, Daniel Mendelevitch, Maciej Kilian, Dominik Lorenz, Yam Levi, Zion English, Vikram Voleti, Adam Letts, et al. Stable video diffusion: Scaling latent video diffusion models to large datasets. _arXiv preprint arXiv:2311.15127_ , 2023. 3 

- [8] Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. Language models are few-shot learners. In _NeurIPS_ , 2020. 2 

- [9] Qingwen Bu, Yanting Yang, Jisong Cai, Shenyuan Gao, Guanghui Ren, Maoqing Yao, Ping Luo, and Hongyang Li. Univla: Learning to act anywhere with task-centric latent actions. In _RSS_ , 2025. 2, 5, 7, 8 

- [10] Akshay L Chandra, Iman Nematollahi, Chenguang Huang, Tim Welschehold, Wolfram Burgard, and Abhinav Valada. Diwa: Diffusion policy adaptation with world models. _arXiv preprint arXiv:2508.03645_ , 2025. 3 

- [11] Kevin Chen, Marco Cusumano-Towner, Brody Huval, Aleksei Petrenko, Jackson Hamburger, Vladlen Koltun, and Philipp Kr¨ahenb¨uhl. Reinforcement learning for long-horizon interactive llm agents. _arXiv preprint arXiv:2502.01600_ , 2025. 6 

- [12] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. In _RSS_ , 2023. 2 

- [13] Wenliang Dai, Junnan Li, Dongxu Li, Anthony Tiong, Junqi Zhao, Weisheng Wang, Boyang Li, Pascale N Fung, and Steven Hoi. Instructblip: Towards general-purpose visionlanguage models with instruction tuning. In _NeurIPS_ , 2023. 2 

- [14] Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn, Xiaohua Zhai, Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg Heigold, Sylvain Gelly, et al. An image is worth 16x16 words: Transformers for image recognition at scale. _arXiv preprint arXiv:2010.11929_ , 2020. 2 

- [15] Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi Wang, Xiao Bi, et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. _arXiv preprint arXiv:2501.12948_ , 2025. 3 

- [16] Danijar Hafner, Timothy Lillicrap, Ian Fischer, Ruben Villegas, David Ha, Honglak Lee, and James Davidson. Learning latent dynamics for planning from pixels. In _ICML_ , 2019. 3 

- [17] Danijar Hafner, Timothy Lillicrap, Mohammad Norouzi, and Jimmy Ba. Mastering atari with discrete world models. _arXiv preprint arXiv:2010.02193_ , 2020. 

- [18] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse control tasks through world models. _Nature_ , pages 1–7, 2025. 3 

- [19] Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffusion probabilistic models. In _NeurIPS_ , 2020. 3 

20875 

- [20] Yicong Hong, Qi Wu, Yuankai Qi, Cristian RodriguezOpazo, and Stephen Gould. Vln bert: A recurrent visionand-language bert for navigation. In _CVPR_ , 2021. 1 

- [21] Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan AllenZhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen, et al. Lora: Low-rank adaptation of large language models. In _ICLR_ , 2022. 6 

- [22] Anqing Jiang, Yu Gao, Yiru Wang, Zhigang Sun, Shuo Wang, Yuwen Heng, Hao Sun, Shichen Tang, Lijuan Zhu, Jinhao Chai, et al. Irl-vla: Training an vision-languageaction policy via reward world model. _arXiv preprint arXiv:2508.06571_ , 2025. 3 

- [23] Yuxin Jiang, Shengcong Chen, Siyuan Huang, Liliang Chen, Pengfei Zhou, Yue Liao, Xindong He, Chiming Liu, Hongsheng Li, Maoqing Yao, and Guanghui Ren. Enerverse-ac: Envisioning embodied environments with action condition. _arXiv preprint arXiv:2505.09723_ , 2025. 4 

- [24] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An opensource vision-language-action model. In _CoRL_ , 2024. 1, 2, 3, 5, 7, 8 

- [25] Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success. In _RSS_ , 2025. 2, 3, 4, 5, 7, 8 

- [26] Harrison Lee, Samrat Phatale, Hassan Mansoor, Kellie Ren Lu, Thomas Mesnard, Johan Ferret, Colton Bishop, Ethan Hall, Victor Carbune, and Abhinav Rastogi. Rlaif: Scaling reinforcement learning from human feedback with ai feedback. In _ICML_ , 2023. 3 

- [27] Junnan Li, Dongxu Li, Caiming Xiong, and Steven Hoi. Blip: Bootstrapping language-image pre-training for unified vision-language understanding and generation. In _ICML_ , 2022. 2 

- [28] Junnan Li, Dongxu Li, Silvio Savarese, and Steven Hoi. Blip-2: Bootstrapping language-image pre-training with frozen image encoders and large language models. In _ICML_ , 2023. 2 

- [29] Shiyi Liang, Xinyuan Chang, Changjie Wu, Huiyuan Yan, Yifan Bai, Xinran Liu, Hang Zhang, Yujian Yuan, Shuang Zeng, Mu Xu, et al. Persistent autoregressive mapping with traffic rules for autonomous driving. _arXiv preprint arXiv:2509.22756_ , 2025. 1 

- [30] Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harrison Edwards, Bowen Baker, Teddy Lee, Jan Leike, John Schulman, Ilya Sutskever, and Karl Cobbe. Let’s verify step by step. In _ICLR_ , 2023. 3 

- [31] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. In _NeurIPS_ , 2023. 4, 5, 7 

- [32] Haotian Liu, Chunyuan Li, Yuheng Li, and Yong Jae Lee. Improved baselines with visual instruction tuning. _arXiv preprint arXiv:2310.03744_ , 2023. 2 

- [33] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. In _NeurIPS_ , 2023. 2 

- [34] Guanxing Lu, Wenkai Guo, Chubin Zhang, Yuheng Zhou, Haonan Jiang, Zifeng Gao, Yansong Tang, and Ziwei Wang. Vla-rl: Towards masterful and general robotic manipulation with scalable reinforcement learning. _arXiv preprint arXiv:2505.18719_ , 2025. 2, 3, 4, 5 

- [35] Maxime Oquab, Timoth´ee Darcet, Th´eo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin El-Nouby, et al. Dinov2: Learning robust visual features without supervision. _arXiv preprint arXiv:2304.07193_ , 2023. 2 

- [36] Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, et al. Training language models to follow instructions with human feedback. In _NeurIPS_ , 2022. 3 

- [37] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for visionlanguage-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 5, 7, 8 

- [38] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al. Learning transferable visual models from natural language supervision. In _ICML_ , 2021. 2, 4 

- [39] Rafael Rafailov, Archit Sharma, Eric Mitchell, Christopher D Manning, Stefano Ermon, and Chelsea Finn. Direct preference optimization: Your language model is secretly a reward model. In _NeurIPS_ , 2023. 2 

- [40] Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, and Bj¨orn Ommer. High-resolution image synthesis with latent diffusion models. In _CVPR_ , 2022. 3 

- [41] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 2, 6 

- [42] Shuhan Tan, Kairan Dou, Yue Zhao, and Philipp Kr¨ahenb¨uhl. Interactive post-training for vision-languageaction models. _arXiv preprint arXiv:2505.17016_ , 2025. 2, 3, 4, 5, 6, 7 

- [43] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, Jianlan Luo, You Liang Tan, Lawrence Yunliang Chen, Pannag Sanketi, Quan Vuong, Ted Xiao, Dorsa Sadigh, Chelsea Finn, and Sergey Levine. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 2 

- [44] Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timoth´ee Lacroix, Baptiste Rozi`ere, Naman Goyal, Eric Hambro, Faisal Azhar, Aurelien Rodriguez, Armand Joulin, Edouard Grave, and Guillaume Lample. Llama: Open and efficient foundation language models. _arXiv preprint arXiv:2302.13971_ , 2023. 2 

- [45] Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. Llama 2: Open foundation and fine-tuned chat models. _arXiv preprint arXiv:2307.09288_ , 2023. 2 

20876 

- [46] Jiaxu Wan, Xu Wang, Mengwei Xie, Xinyuan Chang, Xinran Liu, Zheng Pan, Mu Xu, and Ding Yuan. Driving by hybrid navigation: An online hd-sd map association framework and benchmark for autonomous vehicles. _arXiv preprint arXiv:2507.07487_ , 2025. 1 

- [47] Team Wan, Ang Wang, Baole Ai, Bin Wen, Chaojie Mao, Chen-Wei Xie, Di Chen, Feiwu Yu, Haiming Zhao, Jianxiao Yang, Jianyuan Zeng, Jiayu Wang, Jingfeng Zhang, Jingren Zhou, Jinkai Wang, Jixuan Chen, Kai Zhu, Kang Zhao, Keyu Yan, Lianghua Huang, Mengyang Feng, Ningyi Zhang, Pandeng Li, Pingyu Wu, Ruihang Chu, Ruili Feng, Shiwei Zhang, Siyang Sun, Tao Fang, Tianxing Wang, Tianyi Gui, Tingyu Weng, Tong Shen, Wei Lin, Wei Wang, Wei Wang, Wenmeng Zhou, Wente Wang, Wenting Shen, Wenyuan Yu, Xianzhong Shi, Xiaoming Huang, Xin Xu, Yan Kou, Yangyu Lv, Yifei Li, Yijing Liu, Yiming Wang, Yingya Zhang, Yitong Huang, Yong Li, You Wu, Yu Liu, Yulin Pan, Yun Zheng, Yuntao Hong, Yupeng Shi, Yutong Feng, Zeyinzi Jiang, Zhen Han, Zhi-Fan Wu, and Ziyu Liu. Wan: Open and advanced large-scale video generative models. _arXiv preprint arXiv:2503.20314_ , 2025. 3 

- [48] Jianyuan Wang, Minghao Chen, Nikita Karaev, Andrea Vedaldi, Christian Rupprecht, and David Novotny. Vggt: Visual geometry grounded transformer. In _CVPR_ , 2025. 2, 4 

- [49] Jinbo Xing, Menghan Xia, Yong Zhang, Haoxin Chen, Wangbo Yu, Hanyuan Liu, Gongye Liu, Xintao Wang, Ying Shan, and Tien-Tsin Wong. Dynamicrafter: Animating open-domain images with video diffusion priors. In _ECCV_ , 2024. 3 

- [50] Zhuoyi Yang, Jiayan Teng, Wendi Zheng, Ming Ding, Shiyu Huang, Jiazheng Xu, Yuanming Yang, Wenyi Hong, Xiaohan Zhang, Guanyu Feng, et al. Cogvideox: Text-to-video diffusion models with an expert transformer. _arXiv preprint arXiv:2408.06072_ , 2024. 3 

- [51] Yujian Yuan, Changjie Wu, Xinyuan Chang, Sijin Wang, Hang Zhang, Shiyi Liang, Shuang Zeng, and Mu Xu. Unimapgen: A generative framework for large-scale map construction from multi-modal data. _arXiv preprint arXiv:2509.22262_ , 2025. 1 

- [52] Ekim Yurtsever, Jacob Lambert, Alexander Carballo, and Kazuya Takeda. A survey of autonomous driving: Common practices and emerging technologies. _IEEE Access_ , 8: 58443–58469, 2020. 

- [53] Shuang Zeng, Xinyuan Chang, Mengwei Xie, Xinran Liu, Yifan Bai, Zheng Pan, Mu Xu, and Xing Wei. Futuresightdrive: Thinking visually with spatio-temporal cot for autonomous driving. _arXiv preprint arXiv:2505.17685_ , 2025. 1 

- [54] Shuang Zeng, Dekang Qi, Xinyuan Chang, Feng Xiong, Shichao Xie, Xiaolong Wu, Shiyi Liang, Mu Xu, and Xing Wei. Janusvln: Decoupling semantics and spatiality with dual implicit memory for vision-language navigation. _arXiv preprint arXiv:2509.22548_ , 2025. 1 

20877 

