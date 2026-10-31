---
title: "AtomVLA: Scalable Post-Training for Robotic Manipulation via Predictive Latent World Models"
date: "2026-03-09"
authors: "Xiaoquan Sun; Zetian Xu; Chen Cao; Zonghe Liu; Yihan Sun; Jingrui Pang"
url: https://arxiv.org/abs/2603.08519
pdf: https://arxiv.org/pdf/2603.08519
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.08519)** / [論文ページ](https://arxiv.org/abs/2603.08519)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **AtomVLA: Scalable Post-Training for Robotic Manipulation via Predictive Latent World Models** 

Xiaoquan Sun<sup>1</sup><sup>_,_3</sup> , Zetian Xu<sup>1</sup><sup>_,_2</sup> , Chen Cao<sup>1</sup><sup>_,_2</sup> , Zonghe Liu<sup>1</sup><sup>_,_2</sup> , Yihan Sun<sup>3</sup> , Jingrui Pang<sup>4</sup> , Ruijian Zhang<sup>3</sup> , Zhen Yang<sup>1</sup><sup>_,_2</sup> , Kang Pang<sup>3</sup> , Dingxin He<sup>3</sup> , Mingqi Yuan<sup>1</sup><sup>_,_2</sup> , Jiayu Chen<sup>1</sup><sup>_,_2</sup> 

> 1INFIFORCE Intelligent Technology Co., Ltd. Hangzhou, China 

> 2The University of Hong Kong, Hong Kong SAR, China 

> 3Huazhong University of Science and Technology, Wuhan, China 

> 4Tsinghua University, Beijing, China 

Corresponding author: Jiayu Chen, jiayuc@hku.hk 


Fig. 1: **Framework of AtomVLA.** We propose a scalable two-stage framework for robotic manipulation. **Left (Stage I):** high-level instructions are decomposed into subtask instructions using a Large Language Model (GPT-4o). Subsequently, these subtask instructions are integrated alongside the original high-level instruction as guidance for the SFT training of the model. **Middle (Stage II):** A predictive latent world model evaluates candidate action rollouts to provide reward for offline post-training via GRPO. **Right & Bottom:** AtomVLA achieves 97% and 48% success rates on LIBERO and LIBERO-PRO benchmarks and demonstrates strong generalization in real-world. 

**_Abstract_ — Vision-Language-Action (VLA) models demonstrate remarkable potential for generalizable robotic manipulation. The execution of complex multi-step behaviors in VLA models can be improved by robust instruction grounding, a critical component for effective control. However, current paradigms predominantly rely on coarse, high-level task instructions during supervised fine-tuning. This instruction grounding gap leaves models without explicit intermediate guidance, leading to severe compounding errors in longhorizon tasks. Therefore, bridging this instruction gap and providing scalable post-training for VLA models is urgent. To tackle this problem, we propose AtomVLA, the first subtaskaware VLA framework integrated with a scalable offline posttraining pipeline. Our framework leverages a large language model to decompose high-level demonstrations into fine-grained atomic subtasks. This approach utilizes a pretrained predictive** 

**world model to score candidate action chunks against subtask goals in the latent space, mitigating error accumulation while significantly improving long-horizon robustness. Furthermore, this approach enables highly efficient Group Relative Policy Optimization without the prohibitive expenses associated with online rollouts on physical robots. Extensive simulations validate that our AtomVLA maintains strong robustness under perturbations. When evaluated against fundamental baseline models, it achieves an average success rate of 97.0% on the LIBERO benchmark and 48.0% on the LIBERO-PRO benchmark. Finally, experiments conducted in the real world using the Galaxea R1 Lite platform confirm its broad applicability across diverse tasks, especially long-horizon tasks. All datasets, checkpoints, and code will be released to the public domain following the acceptance of this work for future research.** 

## I. INTRODUCTION 

Vision-Language-Action (VLA) models have significantly advanced the development of embodied intelligence, offering a unified framework for end-to-end visuomotor control and complex instruction-following [1], [2], [3], [4]. By leveraging the reasoning capabilities of large-scale multi-modal models, they directly interpret natural language instructions into executable robot actions, demonstrating remarkable potential for generalizable robot manipulation. However, the transition from lab-scale demonstrations to robust long-horizon deployment is consistently constrained by several critical challenges. Specifically, current VLA architectures [5], [6] demand prohibitive computational resources and massive trajectory datasets for pre-training, making them difficult to scale in resource-constrained environments. Furthermore, the semantic-visual information asymmetry is widespread across these models, as high-dimensional visual tokens often dominate the latent space. As a result, the learned policy struggles to ground sparse linguistic instructions into sequential physical guidance, leading to compounding errors in multistep tasks. Finally, the high costs and safety risks of realworld interaction make online reinforcement learning (RL) impractical for most robotic platforms, leaving a gap between static imitation learning and dynamic policy refinement. 

To address these challenges, effort has been devoted to computational overhead optimization [7], [8], [9], semantic reasoning improvement [10], and the reduction of physical interaction costs through generative simulation [11], [12]. Specifically, LLaVA-VLA [7], SmolVLA [8] and TinyVLA [9] focuses on building lightweight models to significantly reduce parameter counts; CycleVLA [10] introduces cyclic mechanisms to enhance semantic comprehension; and RoboTwin [11], [12] generates extensive interaction data via simulation environments. Despite these significant advancements, existing methods often suffer from poor generalization in practical deployment due to their reliance on imitation learning. Furthermore, most current frameworks focus on reactive action generation, lacking the latent understanding and prediction of real-world dynamic evolution. This absence of modeling capability hinders the model from performing scalable offline policy optimization in the absence of costly online feedback. 

In this paper, we propose **AtomVLA** , a novel, scalable, two-stage post-training framework for robust VLA models in long-horizon robotic tasks. Our contributions are threefold: 

- AtomVLA first introduces a robust architecture that bridges the instruction-grounding gap by leveraging a large language model (LLM) to decompose complex, high-level demonstrations into fine-grained atomic subtasks. This decomposition provides explicit stage-wise guidance that aligns the policy’s semantic understanding with its underlying action-chunking mechanism. 

- Furthermore, to eliminate reliance on costly real-world interactions and to bypass the hallucinations inherent in generative models, a predictive latent world model based on V-JEPA2 [13] is employed to rigorously eval- 

uate candidate action trajectories against subtask goals directly in the latent space. Equipped with these latent transitions, the framework generates highly reliable reward signals for RL post-training, enabling efficient policy refinement without the computational overhead or visual artifacts of pixel-level synthesis. 

- We demonstrate state-of-the-art performance, achieving a 97.0% success rate on the LIBERO benchmark alongside robust visual generalization with a 48.0% success rate on the LIBERO-PRO benchmark. Furthermore, we verify the physical reliability of the model on the Galaxea R1 Lite platform, specifically highlighting its success in complex long-horizon manipulation of deformable objects such as folding a T-shirt. 

## II. RELATED WORK 

## _A. Vision-Language-Action Models_ 

To achieve better adaptability and efficacy, early works [14], [6] optimized Transformer architectures from the ground up, leveraging massive internet-sourced multimodal datasets alongside extensive robotic execution traces. Building upon this foundation, OpenVLA [3] released the first open source foundation model trained on large-scale public data. Subsequently, OpenHelix [15] proposed a dual system architecture for robotic manipulation. To improve deployment efficiency in practical environments, PD-VLA [16] and CEED-VLA [17] explored methods to accelerate the inference process. Furthermore, recent studies such as Spatial Forcing [18] and SpatialVLA [19] have investigated the incorporation of three dimensional spatial features. However, these approaches oriented toward three dimensional perception rely excessively on visual representations at the pure image level. Consequently, they exhibit significant limitations regarding the deep grounding of natural language instructions and the design of their overall training paradigms. 

## _B. Reinforcement Learning for Post-Training_ 

Reinforcement learning post-training has emerged as a crucial paradigm to overcome the inherent limitations of supervised fine-tuning [20], [21], [22], [23], [24]. Because directly deploying online reinforcement learning on physical robots incurs prohibitive interaction costs [25], recent research increasingly favors adopting world models as virtual simulators. Numerous studies [26], [21], [27], [28] have explored this intersection by utilizing simulated environments to generate synthetic experiences for policy optimization. However, effectively fusing these two components remains a significant challenge. Standard generative world models typically synthesize future states at the pixel level. This mechanism inevitably leads to the accumulation of autoregressive errors and produces visual hallucinations during long sequence predictions [20]. To address these bottlenecks, we introduce a scalable post-training pipeline that combines a predictive latent world model (V-JEPA) with GRPO to score trajectories and refine policies. This yields a reliable reward signal and stable improvements on long-horizon tasks. 


Fig. 2: (a) Typical VLA models rely on SFT Training. (b) AtomVLA (Ours) leverages a language model for finegrained decomposition of atomic subtask instructions and a world model for RL post-training. 

## III. ATOMVLA 

## _A. Model Architecture_ 

**VLM Backbone.** AtomVLA uses the open-source multimodal Qwen3-VL-4B-Instruct [29] as the VLM backbone and couples it with an action head. At time _t_ , given a multiview visual observation _Ot_ , high-level instruction _It_ , and subtask instruction _SIt_ , the backbone encodes them into contextual token features 


which condition the action expert via cross-attention. The expert outputs an action chunk **a** _t_ : _t_ + _N_ = [ **a** _t, . . . ,_ **a** _t_ + _N_ ], where _N_ is the action horizon. 

**Action Head.** We introduce an action head, implemented as a cross-attention Diffusion Transformer [30]. Specifically, the action expert serves as a flow-matching head that regresses an action sequence. Conditioned on **H** _t_ and _St_ , the expert predicts a horizon- _N_ action chunk **a** _t_ : _t_ + _N_ . Following a flowmatching formulation, we corrupt the ground-truth chunk with Gaussian noise: sample **_ϵ_** _∼N_ (0 _,_ **I** ) and a continuous time _τ ∈_ (0 _,_ 1), then form **x** _τ_ = (1 _− τ_ ) **_ϵ_** + _τ_ **a** _t_ : _t_ + _N_ . The expert is trained to regress the target velocity **v** = **a** _t_ : _t_ + _N −_ **_ϵ_** by predicting **v** ˆ = _Aϕ_ ( **Gx** _τ , τ_ ; **H** _t, st_ ) and minimizing 


At inference time, we initialize **a**<sup>(0)</sup> _∼N_ (0 _,_ **I** ) and iteratively refine it for _K_ steps using explicit Euler updates **a**<sup>(</sup><sup>_k_+1)</sup> = **a**<sup>(</sup><sup>_k_)</sup> + ∆ _t Aϕ_ ( **a**<sup>(</sup><sup>_k_)</sup> _, τk_ ; **H** _t, st_ ), with ∆ _t_ = 1 _/K_ , yielding the final action chunk. 

**Subtask Dataset.** We use a large language model (LLM) to further decompose each demonstration trajectory and its high-level task instruction into fine-grained atomic subtasks, and to annotate each subtask with a natural language instruction and the start and end frames. Given the highlevel task instruction, we provide the LLM with a sampled sequence of video frames and the task context, and ask it to segment the entire demonstration into a number of atomic subtasks. The LLM returns a JSON list of tuples in the format _{_ ( _ℓi, si, ei_ ) _}_<sup>_M_</sup> _i_ =1<sup>,where</sup><sup>_i_indexessubtasks,</sup> _M_ is the number of subtasks, _ℓi_ is the subtask instruction, and _si, ei_ are the start and end frames. To ensure 

consistent granularity, we explicitly constrain the prompt so that the generated subtasks align with a small set of basic manipulation actions, rather than overly fine-grained intermediate process descriptions. For example, for the _pick and place_ task, we standardize subtasks into action expressions such as Pick up [object], Place [object] on [target position], Open/Close [object], and Push [object]. Under this rule, a task is decomposed into 2-5 subtasks. Prompt details are provided in the supplementary material. In our implementation, we use GPT-4o as the LLM for fine-grained atomic subtask decomposition and annotation. 

## _B. Reward Modeling and RL Post-training_ 

**Motivation.** While SFT on demonstrations equips the policy with a strong imitation capability, it often falls short on more challenging tasks and generalizes poorly. A common remedy is to further apply reinforcement learning post-training to improve long-horizon decision making and error recovery; however, collecting online RL rollouts in simulators or on real robots is costly and difficult to scale. We therefore seek a scalable offline post-training signal that encourages goaldirected progress at an appropriate temporal granularity and remains stable by anchoring learning to expert demonstrations. To this end, we treat subtask boundary frames as intermediate goals and leverage a pretrained world model to score candidate action chunks, enabling scalable RL posttraining. 

**Action-conditioned world model.** We build an actionconditioned latent dynamics model on top of a pretrained video representation. Concretely, we adopt V-JEPA2 [13] as a frozen visual encoder _J_ ( _·_ ) that maps an image to a latent token sequence. Given the current observation _Ot_ and a candidate action chunk **a** ˜ _t_ : _t_ + _N_ , a predictor network _Wθ_ rolls out the latent future _z_ ˆ _t_ + _N_ = _Wθ_ ( _J_ ( _Ot_ ) _,_ ˜ **a** _t_ : _t_ + _N_ ). This enables scoring candidate actions by comparing their predicted consequences against goal states in latent space. **Reward design.** We decompose each episode into coarsegrained subtasks and obtain boundary frames for each subtask. For a timestep _t_ , let _b_ ( _t_ ) denote the boundary frame index of the current subtask, i.e., the first frame after the current subtask ends. We treat _Ob_ ( _t_ ) as the _subgoal_ and _OT −_ 1 as the final task goal within the same episode. For each candidate **a** ˜<sup>(</sup><sup>_k_)</sup> _t_ : _t_ + _N_<sup>,wecomputetwogoalenergies</sup> 


where lower is better. To discourage implausible actions and prevent reward hacking, we also include an imitation deviation term _D_<sup>(</sup><sup>_k_)</sup> = _∥_ **a** ˜<sup>(</sup> _t_ :<sup>_k_</sup> _t_<sup>)</sup> + _N_<sup>_−_</sup><sup>**a**</sup> _t_<sup>_⋆_</sup> : _t_ + _N_<sup>_∥_1.Thefinalscalar</sup> reward is 


Intuitively, the subgoal term provides stage-wise guidance aligned with subtask progress, while the final-goal term 


Fig. 3: **Training pipeline. Stage I:** high-level instructions are decomposed into fine-grained atomic subtask instructions using LLM (GPT-4o). Subsequently, these subtask instructions are integrated with the original high-level instruction to guide the SFT training of the model. **Stage II:** A predictive latent world model evaluates candidate action rollouts to provide reward for offline post-training. 

enforces long-horizon consistency, where _λ_ sub = 0 _._ 3, _λ_ goal = 0 _._ 4, and _α_ = 0 _._ 3. 

**GRPO optimization.** Given _K_ candidates per state, we normalize rewards within each group to form advantages _A_<sup>(</sup><sup>_k_)</sup> and update the policy to increase the likelihood of higher-advantage candidates. We further regularize updates with a KL penalty to a frozen SFT reference policy _π_ ref for stability: 


We only update the action head parameters during posttraining. 

## _C. Training Pipeline_ 

As shown in Fig. 3, there are two major training stages: **SFT Training.** We perform supervised fine-tuning on robot demonstrations by jointly optimizing the Qwen3-VL backbone and the action expert. Given ( _Ot, It, St_ ), we supervise the predicted action chunk **a** _t_ : _t_ + _N_ using the flow-matching loss in Eq. (2). We further reduce gradient variance by repeating each batch with independently sampled ( _τ,_ **_ϵ_** ) via the repeated diffusion steps and training with mixed precision. **Post Training.** Starting from the SFT checkpoint, we conduct offline GRPO post-training using the reward model defined in Sec. III-B. Concretely, we first sample states from the same offline demonstration dataset used in Stage I. Initialized from the Stage I checkpoint, the current policy then generates multiple candidate action chunks for each state. Next, we compute subgoal and final goal rewards with the V-JEPA2 [13] world model, and perform GRPO updates with a KL constraint to the frozen SFT reference policy. Unless otherwise specified, we mainly update the action expert parameters during post-training to preserve 

stable vision-language representations while improving longhorizon robustness. 

## IV. SIMULATION EXPERIMENTS 

We concentrate on several experiments to answer the following questions: 

- **Q1** : Does AtomVLA outperform existing VLA models on standard and long-horizon benchmarks? 

- **Q2** : Does world model guided GRPO post-training consistently improve performance? 

- **Q3** : How do subtask instruction refinement and action chunk size influence long-horizon robustness? 

- **Q4** : Can AtomVLA be effectively deployed in real-world robot system? 

## _A. Experimental Setup_ 

**Benchmark Selection.** We evaluate AtomVLA on two widely used simulation benchmarks, LIBERO [31] and LIBERO-PRO [32]. LIBERO contains four main task suites: LIBERO-Spatial, LIBERO-Object, LIBERO-Goal, and LIBERO-Long. Each task suite contains 500 expert demonstrations across 10 tasks, designed to probe generalization to different spatial layouts, objects, goals, and longhorizon behaviors. LIBERO-PRO extends LIBERO with several controlled perturbation factors, enabling a more rigorous assessment of generalization and robustness under variations in objects, scene configurations, and instruction conditions. **Evaluation Metrics.** We report the success rate **(SR)** as the evaluation metric on both benchmarks and evaluate 50 times per task. 

**Algorithmic Baselines.** We evaluate AtomVLA against a collection of representative and competitive baselines, including TraceVLA [33], OpenVLA [3], SpatialVLA [19], CoT-VLA [34], NORA [35], NORA1.5 [5], ThinkAct [36], _π_ 0 [6] and other baselines. 

**Training Details.** SFT training is trained on the LIBERO dataset for 2 epochs, and evaluation runs 50 times per task. 

For post-training, we sample 100K trajectories and use 10 candidates for each sample. Detailed training hyperparameters are provided in the supplementary material. 

## _B. Results Analysis_ 

**Key Finding 1: Cross-embodiment large-scale pretraining is not necessary to achieve strong downstream performance.** As shown in Table III, even without crossembodiment large-scale pre-training, AtomVLA achieves an average success rate of 93% on the LIBERO benchmark [31]. This result indicates that training solely on in-domain multitask demonstrations is sufficient to learn a robust vision– language-to-action mapping. In contrast, cross-embodiment large-scale pre-training not only incurs substantially higher training costs but also yields inconsistent gains on specific downstream tasks due to discrepancies in action spaces and uneven data quality. 

**Key Finding 2: Post-training consistently improves performance.** Table III shows that post-training improves AtomVLA over the SFT baseline across all LIBERO suites, with the largest gain on LIBERO-Goal (+6.0%). This indicates that SFT provides a strong imitation prior, but it is not sufficient to fully resolve long-horizon goal alignment. GRPO post-training addresses this gap by introducing comparative supervision at the group level over multiple candidate rollouts and using world model evaluation to reinforce trajectories that better satisfy intermediate subgoal and the final goal. By explicitly favoring rollouts consistent with the goal while remaining anchored to demonstration-like behaviors, posttraining yields more reliable goal-directed action selection, which explains the pronounced gains in goal-conditioned settings. 

**Key Finding 3: AtomVLA exhibits strong robustness under controlled perturbations.** Table IV shows that LIBERO-PRO [32] is substantially more challenging than standard LIBERO [31]. Many baselines drop to near-zero success on several perturbation dimensions, indicating limited robustness under distribution shifts. In contrast, AtomVLA retains stable and non-trivial success across multiple dimensions and task suites, and continues to perform well under position and task-related perturbations. We attribute this advantage to our two-stage training design. SFT provides a reliable imitation prior, while post-training further reinforces goal-consistent action selection under world model evaluation, improving generalization under different conditions. 

TABLE I: Different Input on LIBERO-Long. **Bold** denotes the best performance among all methods. 

|**Input**||**LIBERO-Long**|
|---|---|---|
|Image||80.4%|
|Image +|High-level Task|90.0%|
|Image +|High-level Task + Atomic Task|**92.2%**|


**Key Finding 4: Fine-grained atomic subtask instruction refinement improves policy performance.** As shown in 

Table I, removing language instruction causes a clear performance drop on LIBERO-Long (-9.6%), indicating that instruction grounding is critical for robot manipulation. Conditioning the policy on the task instruction improves success to 90.0%, and further augmenting it with a subtask description yields an additional gain to 92.2%. We attribute this improvement to subtask instructions that provide an explicit intermediate objective for the current stage while preserving the overall task goal, helping the policy focus on the objects and actions and improving credit assignment over long-horizon tasks. 

TABLE II: Comparison of AtomVLA on the LIBERO benchmark with different numbers of action chunk horizon. **Bold** denotes the best performance among all methods. 

|Chunk Size|Spatial|Object|Goal|Long|Avg.|
|---|---|---|---|---|---|
|4|**96.4%**|99.6%|97.6%|**94.4%**|**97.0%**|
|8|95.6%|99.2%|98.4%|93.0%|96.6%|
|16|96.0%|**99.8%**|**98.8%**|91.6%|96.6%|
|32|96.0%|99.0%|**98.8%**|91.2%|96.3%|


**Key Finding 5: Action chunking improves planning capability and produces more stable action sequences.** We adopt action chunking to effectively enhance the temporal coherence and implicit planning capabilities of action generation. As shown in Table II, we empirically evaluate various chunk sizes and find that setting the size to 4 yields the optimal manipulation performance. An overly large chunk size reduces execution flexibility and exacerbates the accumulation of compounding errors, thereby degrading the overall task success rate. 

## _C. Ablation Study_ 

To analyze the individual contributions of different reward elements, namely the subgoal reward _E_ sub<sup>(</sup><sup>_k_)andthefinal-</sup> goal reward _E_ goal<sup>(</sup><sup>_k_),weevaluateAtomVLAontheLIBERO</sup> benchmark [31] using each elementary reward separately. The results show that both elementary rewards consistently outperform the SFT baseline, improving the average success rate by approximately 3.0%. When adopting the full combined reward _E_ sub<sup>(</sup><sup>_k_)+</sup><sup>_E_</sup> goal<sup>(</sup><sup>_k_)+</sup><sup>_D_(</sup><sup>_k_),themodelachievesthe</sup> most stable performance, with an overall 4.0% improvement over the SFT baseline. Notably, on the more challenging Long suite, the combined reward yields a substantial 4.4% gain over SFT. These results suggest a clear synergy between intermediate subtask guidance and final goal consistency: the combined reward mitigates noise from purely long-horizon world model predictions while avoiding short-sighted biases induced by focusing solely on immediate subgoals. 

TABLE III: Comparisons with state-of-the-art methods on the LIBERO benchmark [31]. **Bold** denotes the best performance among all methods. 

|**Method**|**w/o Pre-Training**|**Model Size**|**LIBERO-Spatial**|**LIBERO-Object**|**LIBERO-Goal**|**LIBERO-Long**|**Avg.**|
|---|---|---|---|---|---|---|---|
|TraceVLA [33]|✗|7 B|84.6%|85.2%|75.1%|54.1%|74.8%|
|OpenVLA [3]|✓|7 B|84.7%|88.4%|79.2%|53.7%|76.5%|
|SpatialVLA [19]|✓|4 B|88.2%|89.9%|78.6%|55.5%|78.1%|
|CoT-VLA [34]|✓|7 B|87.5%|91.6%|87.6%|69.0%|83.9%|
|_π_0 [6]|✓|4 B|96.8%|98.8%|95.8%|85.2%|94.2%|
|ThinkAct [36]|✗|7 B|88.3%|91.4%|87.1%|70.9%|84.4%|
|NORA [35]|✓|3 B|85.6%|89.4%|80.0%|63.0%|79.5%|
|NORA-1.5 [5]|✓|3 B|**97.3%**|96.4%|94.5%|89.6%|94.5%|
|AtomVLA (SFT)|✗|4 B|94.1%|95.4%|92.4%|90.0%|93.0%|
|AtomVLA (SFT + Post-Training)|✗|4 B|96.4%|**99.6%**|**97.6%**|**94.4%**|**97.0%**|
|∆from GRPO|||2_._3%_↑_|4_._2%_↑_|5_._2%_↑_|4_._4%_↑_|4_._0%_↑_|


TABLE IV: Comparisons with state-of-the-art methods on the LIBERO-PRO benchmark [32]. **Bold** denotes the best performance among all methods. 

|**Method**||LIBER|O-Goa|l|L|IBERO|-Spati|al||LIBE|RO-10||L|IBER|O-Obje|ct|**Avg.**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Obj|Pos|Sem|Task|Obj|Pos|Sem|Task|Obj|Pos|Sem|Task|Obj|Pos|Sem|Task||
|_π_0 [6]|**0.94**|0.00|0.93|0.00|0.95|0.00|**0.97**|0.00|**0.79**|0.00|0.82|0.00|**0.94**|0.00|0.90|0.00|0.45|
|MolmoAct [37]|0.68|0.00|0.85|0.00|0.90|0.00|0.88|0.00|0.54|0.00|0.74|0.06|0.92|0.06|0.96|0.00|0.41|
|NORA [35]|0.58|0.00|0.88|0.00|0.92|0.00|0.91|0.00|0.46|0.00|0.74|0.00|0.86|0.00|0.92|0.00|0.39|
|X-VLA [38]|0.68|0.01|**0.98**|0.09|**0.97**|0.00|0.96|0.00|0.62|0.00|0.95|**0.10**|0.89|0.02|0.98|**0.08**|0.46|
|**AtomVLA (Ours)**|0.81|**0.02**|**0.98**|**0.11**|0.95|**0.16**|0.95|**0.01**|0.55|**0.01**|**0.95**|0.09|0.93|**0.10**|**0.99**|0.00|**0.48**|


Fig. 4: **Visualization of real-world tasks.** The top two rows illustrate basic tasks to stack bowls, place fruit into a basket, hang the cup, and open the drawer. The bottom two rows demonstrate hard, long-horizon tasks to fold a T-shirt and a towel. 


Fig. 5: **Real-world experimental setup.** (a) Tabletop workspace. (b) Galaxea R1 lite platform. 

## V. REAL-WORLD EXPERIMENTS 

## _A. Experimental Setup_ 

We set up real-world experiments based on the Galaxea R1 Lite, a dual-arm mobile platform. The system consists of three omnidirectional wheels, two 6-DoF arms, two wrist cameras, and a head camera, as shown in Figure 5. In our experiments, the mobile module is kept stationary. We categorize our real-world tasks into two difficulty levels: **Basic** and **Hard** . **Basic** tasks are short-horizon and involve basic manipulation actions; they include: 

TABLE V: Ablation of reward formulations on LIBERO Benchmark [31]. **Bold** denotes the best performance among all methods. 

|**Reward**|**Spatial **|**Object**|**Goal**|**Long**|**Avg.**|
|---|---|---|---|---|---|
|SFT|94.1%|95.4%|92.4%|90.0%|93.0%|
|_E_<sup>(</sup><sup>_k_)</sup><br>sub <sup>+</sup><sup>_D_(</sup><sup>_k_)</sup><br>|**Post-**<br>96.3%|**Training**<br>**98.0%**|96.2%|93.5%|96.0%|
|_E_<sup>(</sup><sup>_k_)</sup><br>goal <sup>+</sup><sup>_D_(</sup><sup>_k_)</sup>|**97.1%**|97.9%|96.0%|93.2%|96.1%|
|_E_<sup>(</sup><sup>_k_)</sup><br>sub <sup>+</sup><sup>_E_(</sup><sup>_k_)</sup><br>goal <sup>+</sup><sup>_D_(</sup><sup>_k_)</sup>|96.4%|99.6%|**97.6% **|**94.4% **|**97.0%**|


- **Stack bowls** : Pick the bowl and put it on the other. 

- **Put fruit into basket** : Pick the fruit and place it into the basket. 

TABLE VI: Experimental results of AtomVLA and baseline on six real-world Galaxea R1 Lite robot manipulation tasks. **Bold** denotes the best performance among all methods. 

|**Task**|_π_0|[6]|**AtomVL**|**A (Ours)**|
|---|---|---|---|---|
||**ST**|**GE**|**ST**|**GE**|
|**Basic Tasks**|||||
|Stack bowls|**95%**|60%|90%|**80%**|
|Put fruit into basket|85%|45%|**90%**|**65%**|
|Hang cup|**70%**|15%|**70%**|**35%**|
|Open drawer|**60%**|30%|**60%**|**45%**|
|**Hard Tasks**|||||
|Fold T-shirt|35%|5%|**40%**|**25%**|
|Fold towel|50%|20%|**50%**|**35%**|
|**Average**|65.8%|29.2%|**66.7%**|**47.5%**|


- **Hang cup:** Hang the cup on the mug rack. 

- **Open drawer:** Switch the drawer from closed to open. 

- **Hard** tasks target deformable-object manipulation and longhorizon, and they include: 

- **Fold T-shirt:** Fold a T-shirt into a target folded configuration. 

- **Fold towel:** Fold the towel twice to reach the target configuration. 

**Setting.** To comprehensively assess the real-world performance of AtomVLA, we conduct evaluations under two different settings: Standard **(ST)** and Generalization **(GE)** . In the Standard Setting, tasks are executed under conditions consistent with the training demonstrations to verify the foundational manipulation capabilities of the learned policy. To rigorously evaluate the generalization capabilities of our framework in unstructured physical environments, the Generalization Setting introduces four distinct types of perturbations during deployment, as shown in Figure 6: 

- **Object Position Variation** : The initial spatial coordinates of both target objects and receptacles are randomized within the workspace. 

- **Unseen Distractor Objects** : Novel items, absent from the training demonstrations, are introduced in the vicinity of the target objects. 

- **Target Height Variation** : Receptacles are elevated to varying heights using arbitrary support structures. 

- **Instruction Variation** : Task instructions are replaced with diverse, semantically equivalent expressions. 

**Training Details.** Each task comprises 100 demonstrations. The model undergoes SFT on the real-world dataset for 2 epochs, followed by post-training, where we sample 100K trajectories with 10 candidates per state. During the evaluation phase, we conduct 20 trials per task. Specifically, under the **GE** setting, the environmental conditions for these 20 trials are randomly distributed across the four types to rigorously assess robustness. Detailed hyperparameters are provided in the supplementary material. 

## _B. Results Analysis_ 

**Key Finding 6: AtomVLA demonstrates superior robustness and generalization in real-world robotic tasks.** While AtomVLA and the baseline _π_ 0 [6] exhibit comparable 


Fig. 6: The four types of variation introduced under the **GE** setting to evaluate the robustness of AtomVLA. (a) Object position variation. (b) Unseen distractor object. (c) Target height variation. (d) Instruction language variation. 

foundational capabilities under the **ST** setting, the critical advantage of our approach emerges under the **GE** setting. When subjected to spatial, visual, and instruction variations, the baseline performance degrades sharply to an average success rate of 29.2%. Conversely, AtomVLA demonstrates substantial resilience by maintaining a 47.5% average success rate, yielding an absolute improvement of 18.3% over _π_ 0 [6]. This enhanced robustness is particularly pronounced in **Hard** tasks involving deformable objects, which require precise long-horizon control where execution errors easily compound. For instance, under the **GE** setting for the Fold T- shirt and Fold towel tasks, AtomVLA sustains success rates of 25% and 35% respectively, far exceeding the baseline. These results validate that leveraging subtask instruction decomposition and world-model-guided post-training effectively mitigates error accumulation even in highly unstructured environments. 

## VI. CONCLUSION 

In this paper, we propose AtomVLA to effectively address the instruction grounding gap and the inefficiency of offline reinforcement learning in horizon tasks. By introducing subtask decomposition driven by LLM, our training framework explicitly provides sequential guidance for complex robotic operations. Our experiments and analyses substantiate that our training paradigm, consisting of two stages, yields significant performance gains. Specifically, combining supervised fine-tuning with scalable offline GRPO guided by a predictive world model achieves remarkable results on both the LIBERO and LIBERO-PRO benchmarks. Furthermore, evaluations in the real world on the Galaxea R1 Lite platform highlight the substantial advantages of AtomVLA for tasks requiring prolonged execution sequences. This reliability is particularly evident in the challenging manipulation of deformable objects, such as folding a T-shirt. While our framework enables long-horizon tasks, adapting to highly dynamic environments remains challenging because the current system relies on static subtask boundaries generated by LLM. Future work will explore end-to-end subtask generation during execution and world models that can perceive uncertainty. Furthermore, we intend to systematically enhance the generalization capabilities of our approach to handle entirely unseen objects and novel semantic instructions. 

## REFERENCES 

- [1] W. Song, Z. Zhou, H. Zhao, J. Chen, P. Ding, H. Yan, Y. Huang, F. Tang, D. Wang, and H. Li, “Reconvla: Reconstructive visionlanguage-action model as effective robot perceiver,” _arXiv preprint arXiv:2508.10333_ , 2025. 

- [2] P. Intelligence, K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai _et al._ , “ _π_ 0 _._ 5: a vision-language-action model with open-world generalization,” _arXiv preprint arXiv:2504.16054_ , 2025. 

- [3] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. P. Foster, P. R. Sanketi, Q. Vuong _et al._ , “Openvla: An open-source vision-language-action model,” in _8th Annual Conference on Robot Learning_ , 2024. 

- [4] J. Chen, W. Song, P. Ding, Z. Zhou, H. Zhao, F. Tang, D. Wang, and H. Li, “Unified diffusion vla: Vision-language-action model via joint discrete denoising diffusion process,” _arXiv preprint arXiv:2511.01718_ , 2025. 

- [5] C.-Y. Hung, N. Majumder, H. Deng, R. Liu, Y. Ang, A. Zadeh, C. Li, D. Herremans, Z. Wang, and S. Poria, “Nora-1.5: A vision-languageaction model trained using world model- and action-based preference rewards,” _arXiv preprint arXiv:2511.14659_ , 2025. 

- [6] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter, S. Jakubczak, T. Jones, L. Ke, S. Levine, A. Li-Bell, M. Mothukuri, S. Nair, K. Pertsch, L. X. Shi, J. Tanner, Q. Vuong, A. Walling, H. Wang, and U. Zhilinsky, “ _π_ 0: A vision-language-action flow model for general robot control,” _arXiv preprint arXiv:2410.24164_ , 2024. 

- [7] W. Song, J. Chen, X. Sun, H. Lei, Y. Qin, W. Zhao, P. Ding, H. Zhao, T. Wang, P. Hou, Z. Zhong, H. Yan, D. Wang, J. Ma, and H. Li, “Rethinking the practicality of vision-language-action model: A comprehensive benchmark and an improved baseline,” _arXiv preprint arXiv:2602.22663_ , 2026. 

- [8] M. Shukor, D. Aubakirova, F. Capuano, P. Kooijmans, S. Palma, A. Zouitine, M. Aractingi, C. Pascal, M. Russi, A. Marafioti _et al._ , “Smolvla: A vision-language-action model for affordable and efficient robotics,” _arXiv preprint arXiv:2506.01844_ , 2025. 

- [9] J. Wen, Y. Zhu, J. Li, M. Zhu, Z. Tang, K. Wu, Z. Xu, N. Liu, R. Cheng, C. Shen _et al._ , “Tinyvla: Towards fast, data-efficient visionlanguage-action models for robotic manipulation,” _IEEE Robotics and Automation Letters_ , 2025. 

- [10] C. Ma, G. Yang, K. Lu, S. Xu, B. Byrne, N. Trigoni, and A. Markham, “Cyclevla: Proactive self-correcting vision-language-action models via subtask backtracking and minimum bayes risk decoding,” _arXiv preprint arXiv:2601.02295_ , 2026. 

- [11] Y. Mu, T. Chen, Z. Chen, S. Peng, Z. Lan, Z. Gao, Z. Liang, Q. Yu, Y. Zou, M. Xu, L. Lin, Z. Xie, M. Ding, and P. Luo, “Robotwin: Dualarm robot benchmark with generative digital twins,” in _Proceedings of the Computer Vision and Pattern Recognition Conference (CVPR)_ , June 2025, pp. 27 649–27 660. 

- [12] Z. Wang, Y. He, L. Yang, W. Zou, H. Ma, L. Liu, W. Sui, Y. Guo, and H. Su, “Tabletopgen: Instance-level interactive 3d tabletop scene generation from text or single image,” _arXiv preprint arXiv:2512.01204_ , 2025. 

- [13] M. Assran, A. Bardes, D. Fan, Q. Garrido, R. Howes, M. Komeili, M. Muckley, A. Rizvi, C. Roberts, K. Sinha, A. Zholus, S. Arnaud, A. Gejji, A. Martin, F. Robert Hogan, D. Dugas, P. Bojanowski, V. Khalidov, P. Labatut, F. Massa, M. Szafraniec, K. Krishnakumar, Y. Li, X. Ma, S. Chandar, F. Meier, Y. LeCun, M. Rabbat, and N. Ballas, “V-jepa 2: Self-supervised video models enable understanding, prediction and planning,” _arXiv preprint arXiv:2506.09985_ , 2025. 

- [14] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, J. Dabis, C. Finn, _et al._ , “Rt-1: Robotics transformer for real-world control at scale,” _Proceedings of Robotics: Science and Systems_ , 2023. 

- [15] C. Cui, P. Ding, W. Song, S. Bai, X. Tong, Z. Ge, R. Suo, W. Zhou, Y. Liu, B. Jia _et al._ , “Openhelix: A short survey, empirical analysis, and open-source dual-system vla model for robotic manipulation,” _arXiv preprint arXiv:2505.03912_ , 2025. 

- [16] W. Song, J. Chen, P. Ding, H. Zhao, W. Zhao, Z. Zhong, Z. Ge, J. Ma, and H. Li, “Accelerating vision-language-action model integrated with action chunking via parallel decoding,” _arXiv preprint arXiv:2503.02310_ , 2025. 

- [17] W. Song, J. Chen, P. Ding, Y. Huang, H. Zhao, D. Wang, and H. Li, “Ceed-vla: Consistency vision-language-action model with early-exit decoding,” _arXiv preprint arXiv:2506.13725_ , 2025. 

- [18] F. Li, W. Song, H. Zhao, J. Wang, P. Ding, D. Wang, L. Zeng, and H. Li, “Spatial forcing: Implicit spatial representation alignment for vision-language-action model,” _arXiv preprint arXiv:2510.12276_ , 2025. 

- [19] D. Qu, H. Song, Q. Chen, Y. Yao, X. Ye, Y. Ding, Z. Wang, J. Gu, B. Zhao, D. Wang, and X. Li, “Spatialvla: Exploring spatial representations for visual-language-action model,” _arXiv preprint arXiv:2501.15830_ , 2025. 

- [20] Z. Jiang, S. Zhou, Y. Jiang, Z. Huang, M. Wei, Y. Chen _et al._ , “Wovr: World models as reliable simulators for post-training vla policies with rl,” _arXiv preprint arXiv:2602.13977_ , 2026. 

- [21] F. Zhu, Z. Yan, Z. Hong, Q. Shou, X. Ma, and S. Guo, “Wmpo: World model-based policy optimization for vision-language-action models,” _arXiv preprint arXiv:2511.09515_ , 2025. 

- [22] J. Cen, C. Yu, H. Yuan, Y. Jiang, S. Huang, J. Guo, X. Li, Y. Song, H. Luo, F. Wang _et al._ , “Worldvla: Towards autoregressive action world model,” _arXiv preprint arXiv:2506.21539_ , 2025. 

- [23] H. Li, Y. Zuo, J. Yu, Y. Zhang, Z. Yang, K. Zhang _et al._ , “Simplevlarl: Scaling vla training via reinforcement learning,” _arXiv preprint arXiv:2509.09674_ , 2025. 

- [24] H. Bi, H. Tan, S. Xie, Z. Wang, S. Huang, H. Liu, R. Zhao, Y. Feng, C. Xiang, Y. Rong, H. Zhao, H. Liu, Z. Su, L. Ma, H. Su, and J. Zhu, “Motus: A unified latent action world model,” _arXiv preprint arXiv:2512.13030_ , 2025. 

- [25] M. Pan, S. Feng, Q. Zhang, X. Li, J. Song, C. Qu _et al._ , “Sop: A scalable online post-training system for vision-language-action models,” _arXiv preprint arXiv:2601.03044_ , 2026. 

- [26] J. Xiao, Y. Yang, X. Chang, R. Chen, F. Xiong, M. Xu _et al._ , “Worldenv: Leveraging world model as a virtual environment for vla posttraining,” _arXiv preprint arXiv:2509.24948_ , 2025. 

- [27] H. Li, P. Ding, R. Suo, Y. Wang, Z. Ge, D. Zang _et al._ , “Vla-rft: Vision-language-action reinforcement fine-tuning with verified rewards in world simulators,” _arXiv preprint arXiv:2510.00406_ , 2025. 

- [28] X. He, C. Peng, Z. Liu, B. Wang, Y. Zhang, Q. Cui _et al._ , “Matrixgame 2.0: An open-source real-time and streaming interactive world model,” _arXiv preprint arXiv:2508.13009_ , 2025. 

- [29] S. Bai, Y. Cai, R. Chen, K. Chen _et al._ , “Qwen3-vl technical report,” _arXiv preprint arXiv:2511.21631_ , 2025. 

- [30] W. Peebles and S. Xie, “Scalable diffusion models with transformers,” in _Proceedings of the IEEE/CVF international conference on computer vision_ , 2023, pp. 4195–4205. 

- [31] B. Liu, Y. Zhu, C. Gao, Y. Feng, Q. Liu, Y. Zhu, and P. Stone, “Libero: Benchmarking knowledge transfer for lifelong robot learning,” _arXiv preprint arXiv:2306.03310_ , 2023. 

- [32] X. Zhou, Y. Xu, G. Tie, Y. Chen, G. Zhang, D. Chu, P. Zhou, and L. Sun, “Libero-pro: Towards robust and fair evaluation of vision-language-action models beyond memorization,” _arXiv preprint arXiv:2510.03827_ , 2025. 

- [33] R. Zheng, Y. Liang, S. Huang, J. Gao, H. Daum´e III, A. Kolobov, F. Huang, and J. Yang, “Tracevla: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies,” _arXiv preprint arXiv:2412.10345_ , 2024. 

- [34] Q. Zhao, Y. Lu, M. J. Kim, Z. Fu, Z. Zhang, Y. Wu, Z. Li, Q. Ma, S. Han, C. Finn, A. Handa, M.-Y. Liu, D. Xiang, G. Wetzstein, and T.-Y. Lin, “Cot-vla: Visual chain-of-thought reasoning for visionlanguage-action models,” _arXiv preprint arXiv:2503.22020_ , 2025. 

- [35] C.-Y. Hung, Q. Sun, P. Hong, A. Zadeh, C. Li, U. Tan, N. Majumder, S. Poria _et al._ , “Nora: A small open-sourced generalist vision language action model for embodied tasks,” _arXiv preprint arXiv:2504.19854_ , 2025. 

- [36] C.-P. Huang, Y.-H. Wu, M.-H. Chen, Y.-C. F. Wang, and F.-E. Yang, “Thinkact: Vision-language-action reasoning via reinforced visual latent planning,” _arXiv preprint arXiv:2507.16815_ , 2025. 

- [37] J. Lee, J. Duan, H. Fang, Y. Deng, S. Liu, B. Li, B. Fang, J. Zhang, Y. R. Wang, S. Lee, W. Han, W. Pumacay, A. Wu, R. Hendrix, K. Farley, E. VanderBilt, A. Farhadi, D. Fox, and R. Krishna, “Molmoact: Action reasoning models that can reason in space,” _arXiv preprint arXiv:2508.07917_ , 2025. 

- [38] J. Zheng, J. Li, Z. Wang, D. Liu, X. Kang, Y. Feng _et al._ , “X-vla: Softprompted transformer as scalable cross-embodiment vision-languageaction model,” _arXiv preprint arXiv:2510.10274_ , 2025. 

## APPENDIX 

This supplementary material provides additional technical details and experimental configurations to support the findings presented in the main paper. The organization of this appendix is as follows: **Section A** presents visual examples of the task segmentation process within the LIBERO benchmark, illustrating the temporal breakdown of global tasks into coarse-grained atomic sub-tasks. **Section B** details the comprehensive training and post-training hyperparameters used for both the LIBERO dataset and the real-world experiments on the Galaxea R1 Lite platform, including GPU configurations, learning rates, and input specifications. **Section C** outlines the system prompts, standardized vocabulary, and output format requirements developed to guide the model in generating precise, fine-grained atomic sub-tasks from sampled video frames. **Section D** provides a summary of the baseline models utilized in our comparative evaluation, detailing their respective architectures, pretraining datasets, and core design principles. 

_A. Example Figure_ 


Fig. 7: Atomic subtasks on the LIBERO Dataset. 

_B. Training Details_ 

TABLE VII: SFT-Training hyperparameters for LIBERO Dataset. 

|**Hyperparameter**|**Value**|
|---|---|
|# GPUs|4_×_ NVIDIA H100 (80GB VRAM)|
|learning rate (LR)|5e_−_4|
|batch size|8 (per GPU)|
|# epoch number|2 epoch|
|input images|1 third-person camera image, 1 wrist-mounted camera image|
|input image size|224_×_224 px (wrist camera) 224_×_224 px (third-person camera)|
|action chunk size (_H_)|4 steps|
|action dimensions|7 robot|


TABLE VIII: Post-Training hyperparameters for LIBERO Dataset. 

|**Hyperparameter**|**Value**|
|---|---|
|# GPUs|2_×_ NVIDIA H100 (80GB VRAM)|
|batch size|8 (per GPU)|
|input images|Only 1 third-person camera image|
|input image size|224_×_224 px|
|sample number|100k|
|Candidate|10|
|action dimensions|7 robot|


TABLE IX: SFT-Training hyperparameters for Real-World Dataset on Galaxea R1 Lite platform. 

|**Hyperparameter**|**Value**|
|---|---|
|# GPUs|4_×_ NVIDIA H100 (80GB VRAM)|
|learning rate (LR)|5e_−_4|
|batch size|8 (per GPU)|
|input images|1 head camera image, 2 wrist camera image|
|input image size|1280_×_720 px (head camera) 640_×_360 px (wrist camera)|
|action chunk size (_H_)|10 steps|
|action dimensions|14 robot|


TABLE X: Post-Training hyperparameters for Real-World Dataset on Galaxea R1 Lite platform. 

|**Hyperparameter**|**Value**|
|---|---|
|# GPUs|2_×_ NVIDIA H100 (80GB VRAM)|
|batch size|8 (per GPU)|
|input images|Only 1 head camera image|
|input image size|1280_×_720 px|
|sample number|100k|
|Candidate|10|
|action dimensions|14 robot|


_C. Prompt for fine-grained atomic task generation_ 

## **Prompt for Instruction Generation** 

You are an expert in robotic manipulation analysis for tabletop tasks (Libero benchmark). I will provide frames from a robot manipulation video. 

Your mission is to act as an expert Vision-Language Model providing precise temporal segmentations for tabletop robotic manipulation. You will generate a contiguous sequence of coarse-grained atomic sub-tasks (aligned with the ‘‘GLOBAL TASK CONTEXT’’) based on SAMPLED VIDEO FRAMES, FRAME INDICES, and the OVERALL GOAL. You need to identify and sequence all the main steps that constitute the episode using the STANDARDIZED VOCABULARY defined below, ensuring complete temporal coverage with no overlapping or missing frames. 

**<Global Task Context>** The overall goal of the robot in this video is: "task ~~i~~ nstruction" Please use this context to correctly interpret the robot’s actions. Segment the video into COARSE-GRAINED atomic sub-tasks that achieve this goal. **<Granularity Rules (Coarse-Grained)>** - Merge "Approach" + "Grasp" -> "Pick up". - Merge "Move" + "Release" -> "Place". - A typical pick-and-place episode consists of 2-4 main steps. **<Standardized Vocabulary>** - "Pick up [object]" - "Place [object] into/on [target]" - "Move arm to [location]" - "Open/Close [object]" - "Push [object]" Be specific with object names (e.g., "white mug", "left plate") matching the Global Task Context. 

**<Output Format>** Strictly return a JSON object: { "tasks": [ { "instruction": "Pick up the red cola can", "start_frame": 0, "end_frame": 45 }, { "instruction": "Place the red cola can into the white basket", "start_frame": 46, "end_frame": 120 } ] } 

- Note: The provided images are sampled. Image 1 corresponds to the frame index provided in the user prompt. Use these indices to estimate start/end frames accurately. 

## _D. Baseline._ 

The following baselines are utilized for comparative evaluation. 

**OpenVLA:** A 7B-parameter VLA model that integrates a Llama 2 language backbone with a hybrid visual encoder fusing pretrained representations from DINOv2 and SigLIP. The model is pretrained on a large-scale collection of 970k real-world robot trajectories sourced from the Open X-Embodiment dataset. 

**TraceVLA:** A spatial-temporal enhanced VLA model that incorporates visual trace prompting to encode state–action trajectories into the visual input. Built upon OpenVLA and fine-tuned on 150K robot manipulation trajectories. **Octo-base:** A transformer-based generalist manipulation policy trained on approximately 800K trajectories from the Open X-Embodiment dataset. It supports language and goal-image conditioning and is designed to accommodate diverse sensor modalities and action spaces across multiple robotic platforms. 

**SpatialVLA:** A spatially-aware VLA model designed to enhance 3D understanding in robot manipulation. Pretrained on 1.1M real-world robot episodes, it introduces Ego3D Position Encoding to inject explicit 3D spatial information into visual observations and employs Adaptive Action Grids to discretize and represent spatial robot movements for cross-robot transfer. **CoT-VLA:** A 7B VLA model that incorporates explicit visual chain-of-thought reasoning for manipulation. It autoregressively predicts future visual frames as intermediate goals and then generates short action sequences to reach them, enabling temporal planning. 

_π_ 0 **:** A VLA model that builds a flow-matching action architecture on top of a pretrained VLM to inherit large-scale semantic knowledge. It is trained on diverse datasets collected from multiple dexterous robotic platforms. The model supports direct language prompting and fine-tuning for new skills, demonstrating broad task coverage and cross-platform generalization. **ThinkAct:** A dual-system VLA framework that separates high-level reasoning from low-level control. It trains a multimodal LLM to generate embodied reasoning plans, which are reinforced using action-aligned visual rewards and compressed into a visual latent plan. This latent representation conditions a downstream action policy, enabling improved long-horizon planning, few-shot adaptation, and robust execution in complex embodied manipulation tasks. 

**NORA:** A 3B-parameter VLA model designed for efficient real-time robotic manipulation. Built on the Qwen-2.5-VL3B backbone, it leverages strong visual-semantic understanding to improve action grounding while significantly reducing computational overhead compared to larger VLA models. It trained on 970K real-world robot demonstrations and equipped with the FAST+ tokenizer for efficient action sequence generation. 

**NORA-1.5:** An enhanced VLA model built upon the pre-trained NORA backbone, incorporating a flow-matching–based action expert to improve reliability and task performance. It uses reward-driven post-training with action-conditioned world models and deviation-from–ground-truth heuristics, enabling direct preference optimization for adaptation to new embodiments. 

**MolmoAct:** An Action Reasoning Model that integrates depth-aware perception, mid-level spatial planning, and lowlevel action prediction. The 7B-D variant achieves strong zero-shot, fine-tuned, and out-of-distribution performance across simulation and real-world tasks, surpassing prior VLAs. 

**X-VLA:** A flow-matching–based VLA model that uses soft-prompt embeddings to capture cross-embodiment variations in heterogeneous robotic datasets. Its 0.9B variant, X-VLA-0.9B, achieves state-of-the-art performance across simulations and real-world robots, enabling flexible dexterity, fast adaptation, and effective exploitation of diverse robotic platforms with minimal additional parameters. 

