---
title: "IG-RFT: An Interaction-Guided RL Framework for VLA Models in Long-Horizon Robotic Manipulation"
date: "2026-02-24"
authors: "Zhian Su; Weijie Kong; Haonan Dong; Huixu Dong"
url: https://arxiv.org/abs/2602.20715
pdf: https://arxiv.org/pdf/2602.20715
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.20715)** / [論文ページ](https://arxiv.org/abs/2602.20715)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

1 

ARXIV PREPRINT 

# IG-RFT: An Interaction-Guided RL Framework for VLA Models in Long-Horizon Robotic Manipulation 

Zhian Su, Weijie Kong, Haonan Dong, and Huixu Dong, _Member, IEEE_ 

**_Abstract_ —Vision-Language-Action (VLA) models have demonstrated significant potential for generalist robotic policies; however, they struggle to generalize to long-horizon complex tasks in novel real-world domains due to distribution shifts and the scarcity of high-quality demonstrations. Although reinforcement learning (RL) offers a promising avenue for policy improvement, applying it to real-world VLA fine-tuning faces challenges regarding exploration efficiency, training stability, and sample cost. To address these issues, we propose IG-RFT, a novel InteractionGuided Reinforced Fine-Tuning system designed for flow-based VLA models. Firstly, to facilitate effective policy optimization, we introduce Interaction-Guided Advantage Weighted Regression (IG-AWR), an RL algorithm that dynamically modulates exploration intensity based on the robot’s interaction status. Furthermore, to address the limitations of sparse or task-specific rewards, we design a novel hybrid dense reward function that integrates the trajectory-level reward and the subtask-level reward. Finally, we construct a three-stage RL system comprising SFT, Offline RL, and Human-in-the-Loop RL for fine-tuning VLA models. Extensive real-world experiments on four challenging long-horizon tasks demonstrate that IG-RFT achieves an average success rate of 85.0%, significantly outperforming SFT (18.8%) and standard Offline RL baselines (40.0%). Ablation studies confirm the critical contributions of IG-AWR and hybrid reward shaping. In summary, our work establishes and validates a novel reinforced fine-tuning system for VLA models in real-world robotic manipulation.** 

**_Index Terms_ —Vision-Language-Action Models, Human-in-theLoop Learning, Reinforcement Learning, Robotic Manipulation.** 

## I. INTRODUCTION 

**R** OBOTICtions has becomemanipulationincreasinglyforincreasinglyfor specificmaturereal-world[1]–[3]. Inapplica-com-com- 

tions has becomemanipulationincreasinglyforincreasinglyfor maturereal-world[1]–[3].[1]–[3]. Inapplica-com-comparison, generalist robotic policies are still not well-developed [4]. Recently, Vision-Language-Action (VLA) models, as a prominent paradigm for generalist policies [5]–[9], have shown impressive capabilities and potential, owing to large-scale pretraining via behavior cloning. Existing VLA models have limited generalization, failing to achieve zero-shot transfer to novel real-world domains [10]. Consequently, fine-tuning VLA models using domain-specific demonstrations is an indispensable procedure [11], [12]. The predominant domain adaptation approach for VLA models is supervised fine-tuning (SFT), which is incapable of effectively evaluating and utilizing demonstrations, thereby imposing stringent requirements 

Zhian Su, Weijie Kong, Haonan Dong, and Huixu Dong are with the Grasp Laboratory, Mechanical Engineering Department, Zhejiang University, Hangzhou 310027, China. (Corresponding author: Huixu Dong; e-mail: huixudong@zju.edu.cn). 

All authors are also with Torch Kernel Co., Ltd., Hangzhou 310000, China. This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible. 

on both the quality and quantity of training data. However, during data collection, sub-optimal data is frequently generated due to variations in operator proficiency, system errors, and discontinuous actions. 

In contrast, reinforcement learning (RL) can explore, evaluate and utilize data more effectively to improve policies, exhibiting substantial potential for VLA domain adaptation [13]–[17]. Unlike multi-environment parallel RL deployed in simulation [18], [19], VLA models require direct physical interaction in real-world robotic tasks. This requires high sample efficiency and risk-aware exploration, rendering the direct implementation of on-policy RL infeasible. In realworld scenarios, deploying off-policy RL via Human-in-theLoop can mitigate compounding errors caused by distribution shift, thereby guiding policy learning by timely corrections, yielding remarkable performance [20]–[22]. However, these existing real-world RL systems use sparse rewards, which mainly causes unstable training in the online stage and leads to credit assignment problems. Furthermore, in long-horizon complex tasks, the variance of state distributions differs significantly across sub-stages; applying uniform exploration noise throughout the entire cycle results in inefficient resource utilization. 

In this work, we propose a novel reinforced fine-tuning system for flow-based VLA models, designed to master long-horizon complex robotic manipulation tasks in the real world. As illustrated in Figure 1, the system consists of three stages: SFT, Offline RL, and Human-in-the-Loop RL, enabling a gradual transition from initial policy learning to policy evolution. Our core insight is that effective policy optimization necessitates structured interaction guidance and general dense procedural rewards. To this end, we firstly propose Interaction-Guided Advantage Weighted Regression (IGAWR), an algorithm that dynamically modulates exploration intensity based on the robot’s interaction status. Specifically, this enables the robot to prioritize exploration during noninteraction phases (e.g., approach, retraction) for adapting to the diversity of broadly distributed scenarios, while emphasizing robustness during fine-grained interaction phases (e.g., handover, grasping) to acquire complex manipulation capabilities. To annotate the interaction status for episodes, we leverage open-source robotic segmentation models and optical flow estimation methods for automated processing. Furthermore, we design a novel dense reward function that integrates the trajectory-level reward and the subtask-level reward, providing comprehensive procedural guidance for the RL system, which depends solely on episode lengths and is thus broadly applicable across diverse tasks. While some prior works design dense rewards for specific tasks using 

2 

ARXIV PREPRINT 


Fig. 1: **Overview of the Interaction-Guided Reinforced Fine-tuning System (IG-RFT).** The system integrates a multi-head Q-Former-based critic model to provide dense value and interaction guidance. The supervision target of the dense value is our designed general hybrid value function. We use the interaction signal to modulate the flow matching initial noise to balance RL exploration and exploitation. The training process progresses through three stages: Supervised Fine-Tuning (SFT), data-efficient Offline RL using the proposed IG-AWR algorithm, and final Human-in-the-Loop refinement to master long-horizon real-world manipulation tasks. 

visual similarity or distance to target points [23]–[27], others resort to sparse rewards in real-world reinforcement learning settings [20]–[22], [28], [29]. Finally, we design a multistage training system that achieves stable and efficient policy learning during the SFT and Offline RL stages, and leverages Human-in-the-Loop RL for iterative policy refinement. The innovation and effectiveness of the proposed components are rigorously validated through extensive experiments, including ablation studies on individual modules and comprehensive evaluation of the entire fine-tuning system on real-world longhorizon complex manipulation tasks. Our main contributions are summarized as follows: 

- We propose Interaction-Guided AWR (IG-AWR), a novel RL fine-tuning algorithm designed for flow-based VLA models that effectively balances exploration and exploitation by utilizing interaction signals. 

- We formulate a hybrid dense reward function incorporating trajectory-level procedural rewards and weighted subtasklevel rewards, delivering smooth and dense feedback for long-horizon tasks. 

- We design a multi-stage reinforced fine-tuning system integrated with human intervention. The system initializes policies via SFT, accomplishes foundational policy learning through Offline RL, and further elevates policy performance during Human-in-the-Loop rollouts. 

II. RELATED WORK 

## _A. Vision-Language-Action Models_ 

Robotic policies serve as agents that map perceived states to control actions [30], [31]. Vision-Language-Action (VLA) models are generalizable robotic policies equipped with semantic understanding, trained by adapting vision-language models (VLMs) on robotic manipulation demonstrations and open-world datasets [5]–[8], [11], [12], [32]–[35]. RT-1 [34] and RT-2 [35] are early representative methods that employ transformer-based architectures to predict discretized actions. In contrast, _π_ 0 [5] utilizes an action expert, independent of the pre-trained VLM parameters, to generate actions through flow matching. _π_ 0 _._ 5 [7] is trained with knowledge isolation [36] and enables subtask decomposition [37],achieving broad generalization in real-world manipulation tasks. Despite the rapid recent advancements and demonstrated potential of VLA models, they still exhibit limited generalization and robustness when deployed in novel real-world domains, leading to degraded performance in out-of-distribution scenarios. Advancing fine-tuning methodologies can significantly enhance their capabilities in tackling long-horizon complex real-world tasks. 

## _B. RL Fine-tuning for VLA Models_ 

Fine-tuning VLA models via Reinforcement Learning (RL) has recently emerged as a prominent research focus. One 

SU ET AL.: IG-RFT: AN INTERACTION-GUIDED RL FRAMEWORK FOR VLA MODELS IN LONG-HORIZON ROBOTIC MANIPULATION 

3 

way is to conduct online RL within simulation using largescale parallel environments for model training [14], [38]– [42]. Some studies target RL training for flow-based VLA models [13], [43]–[46]; notably, flow-based VLA models present greater challenges for RL optimization compared to auto-regressive VLA models. The world model, serving as a more efficient interaction environment than the physical world, has been explored to provide feedback for RL finetuning [24], [47], [48]. Reward function design has also been increasingly investigated [23], [25], [26], [49]–[52], as sparse rewards often lead to unstable training, while dense rewards remain difficult to generalize. Another category of methods concentrates on exploring safe and efficient RL fine-tuning in real-world scenarios, mainly through specially devised offlineto-online RL approaches or human-in-the-loop guidance to mitigate the distribution shift problem [20]–[22], [29], [53], [54]; however, these methods lack stage-aware dense reward feedback. In contrast, our work designs a more efficient interaction-guided AWR algorithm, alongside a general and dense reward mechanism. It improves the performance of the system spanning from Offline RL to Human-in-the-Loop RL. 

## III. PRELIMINARIES 

## _A. Vision-Language-Action Models_ 

Consider a robotic manipulation task specified by a natural language instruction _ℓ_ . At each time step _t_ , the agent receives an observation _ot_ (proprioception and visual data). VLA models leverage large-scale pre-trained VLMs and an action module as an end-to-end policy, sampling actions _at ∼ π_ ( _·|ℓ, ot_ ) conditioned on the multimodal context. Standard post-training relies on SFT via objectives like next-token prediction or conditional flow matching, which is highly sensitive to demonstration quality and suffers from data inefficiency. Crucially, SFT indiscriminately treats sub-optimal and optimal demonstrations as equivalent supervision targets. 

## _B. Reinforcement Learning_ 

The robotic manipulation task is formulated as a Markov = Decision Process (MDP) defined by the tuple _M_ ( _S, A, r, P, γ_ ). The state _st ∈S_ encompasses the robot observation _ot_ and task prompt _ℓ_ . The VLA serves as the policy _πθ_ ( _·|st_ ) to sample actions _at_ with the transition dynamics _P_ ( _st_ +1 _|st, at_ ) determining the next state. We define the cumulative return as _Gt_ =<sup>�</sup><sup>_T_</sup> _k_ = _t_<sup>_γk−trk_,where</sup><sup>_γ∈_[0</sup><sup>_,_1]is</sup> the discount factor. Let _τ_ denote a trajectory sampled from the policy; the goal of RL is to optimize parameters _θ_ to maximize the expected return _J_ ( _θ_ ) = E _τ ∼πθ t_ =0<sup>_γtrt_</sup> . Accordingly, �� _T_ � the state value function is defined as _V_<sup>_π_</sup> ( _st_ ) = E _τ ∼πθ_ [ _Gt|st_ ]. 

## IV. METHODOLOGY 

## _A. Interaction-guided AWR for Flow Matching_ 

In complex long-horizon robotic manipulation tasks, achieving an optimal balance between exploration and exploitation remains a critical yet unresolved challenge. Conventional RL methods often suffer from detrimental exploration during delicate operations. To address this, we decompose episodes 


Fig. 2: **Illustration of Dynamic Uncertainty Modulation in IG-AWR.** This mechanism modulates the initial sampling noise _ϵ_ of the flow ODE based on the extracted interaction signal _It_ . During non-interaction phases (top), a higher variance _σ_ high is applied to encourage diverse trajectory exploration. Conversely, during interaction phases (bottom), the variance is reduced to _σ_ low to ensure precision and stability for contactrich manipulation. 

into non-interactive phases (e.g., approach, retraction), where we encourage exploration for trajectory diversity, and contactrich interaction phases (e.g., handover, grasping), where we prioritize precision and stability. Specifically, we first introduce the extraction of interaction signals, followed by their application to the RL fine-tuning of flow-based VLA models. 

_1) Interaction Signal Extraction:_ Efficient and autonomous interaction labeling is crucial for processing VLA demonstrations. Leveraging global visual observations, at each time step _t_ , we first employ the robot segmentation model, RoboEngine [55], to generate a binary robot mask _Mt_ . Subsequently, we apply RAFT [56] to estimate the dense optical flow field _Ft_ . The interaction status _It_ is determined by 


_2) Dynamic Uncertainty Modulation:_ During the rollout phase, as illustrated in Figure 2, we dynamically regulate the variance of the initial sampling noise conditioned on the predicted interaction signal probability. Building directly on the binary interaction labels derived from visual observations (Section IV-A1), the critic network predicts _p_ int( _s_ ) _∈_ [0 _,_ 1]—a soft estimate of interaction likelihood for the state, trained to approximate the ground truth. We define the effective sampling temperature _T_ ( _s_ ) as: 


The policy generates actions by solving the flow ODE starting from a scaled noise distribution. Specifically, the initial state _a_ ˆ0, equal to _ϵ_ , is sampled from _N_ ( **0** _, T_<sup>2</sup> ( _s_ ) **I** ). 

4 

ARXIV PREPRINT 


Fig. 3: **Visualization of the Reward Signal and Value Function.** We illustrate the proposed reward shaping mechanism on the ”Parcel Packing” task. **(A)** The reward signal _rt_ combines a constant trajectory-level reward with weighted subtasklevel rewards (peaks), providing dense feedback at key milestones. **(B)** The Value (Return-to-Go) function _Vt_ monotonically decreases from 1.0 to 0 as the agent progresses through subtasks, serving as a precise progress indicator for the Critic. 

This formulation adaptively modulates exploration: high variance during non-interaction phases encourages diverse trajectory exploration, while low variance during interaction phases enforces precise, stable execution—seamlessly bridging the discrete visual-derived interaction signal _It_ with continuous policy uncertainty modulation. 

_3) Advantage-Weighted Flow Update:_ For policy optimization, we employ Advantage Weighted Regression (AWR) [57] to maximize the expected return of the flow-based policy. Givenpolicy,awedemonstrationestimate the _D_ collectedadvantagevia _A_ ˆ(the _st, a_ interaction-guided _t_ ) = _rt_ : _t_ + _N_ + _Vϕ_ ( _st_ + _N_ ) _−Vϕ_ ( _st_ ). The Interaction-Guided Advantage Weight Regression (IG-AWR) loss function is formulated as: 


where _β_ is the temperature hyperparameter for AWR, and _a_ ˆ _τ_ denotes the flow trajectory at time _τ_ . This objective upweights data with higher estimated advantages while preserving the flow ODE structure for stable policy refinement. 

## _B. General Hybrid Reward Function_ 

Reward modeling is critical for RL fine-tuning of VLA models. Designing a general reward function is beneficial for enabling adaptation to a wide range of tasks. To effectively 

guide the agent through multi-stage long-horizon tasks, we design a hybrid reward function that incorporates both trajectorylevel success incentives and stage-wise subtask feedback, as illustrated in Figure 3 

_1) Trajectory-level Reward:_ To generalize across various robotic manipulation tasks, we define the trajectory-level reward as: 


where _T_ denotes the total number of time steps in the episode. This formulation distributes the total return of 1 _._ 0 uniformly across the trajectory upon successful task completion. 

_2) Subtask-level Reward:_ Since the trajectory-level reward lacks fine-grained feedback for complex long-horizon tasks, we employ potential-based reward shaping at the subtask level. This continuous monotonically increasing potential function prevents reward hacking and provides sufficient local guidance. To simulate subtask completion while ensuring smoothness, we adopt a weighted mixture model to prioritize complex subtasks, formulated as: 


where _ρt_ = _t/T_ denotes the normalized temporal progress, and _σ_ ( _·_ ) is the standard sigmoid function. The parameters _ki_ and _wi_ represent the completion time steps and the importance 

5 

SU ET AL.: IG-RFT: AN INTERACTION-GUIDED RL FRAMEWORK FOR VLA MODELS IN LONG-HORIZON ROBOTIC MANIPULATION 

weight of the _i_ -th subtask. Here, _ϵ_ controls the sharpness and _C_ is a normalization constant. 

_3) Reward Aggregation:_ We obtain the final reward by computing a weighted sum of the trajectory-level reward and the subtask-level reward: 


Accordingly, we derive the return-to-go as _Gt_ =<sup>�</sup><sup>_T_</sup> _k_ = _t_<sup>_rk_</sup> (assuming a discount factor _γ_ = 1). This value naturally decays from 1 _._ 0 to 0 as the episode progresses. 

## _C. RL Fine-tuning System_ 

Due to low data efficiency in purely online RL, we deploy a multi-stage fine-tuning method in which offline training with pre-collected data provides a stronger prior. In the online stage, human feedback provides high-quality and efficient guidance for RL fine-tuning, mitigating exploration challenges in highdimensional spaces. Building on this paradigm, we design a system incorporating the IG-AWR algorithm and dense reward function for long-horizon complex tasks. 

_1) Model Architecture:_ We adopt the _π_ 0 _._ 5 model [7], a representative flow-based VLA validated for superior realworld performance, as our actor module _πθ_ . Leveraging the KV cache from the VLM backbone conditioned on the current observation _ot_ , we train a critic network to regress the state value _Vt_<sup>_π_</sup> and predict the interaction signal _It_ . Specifically, utilizing the KV cache from all transformer layers incurs computational inefficiency and information redundancy. Therefore, we selectively aggregate features from the deeper layers, which contain the richest semantic information. The network architecture is based on the Q-Former (Query Transformer) [58], which utilizes learnable queries to adaptively extract relevant multimodal features from the KV cache through crossattention. The Q-Former output is then passed through three separate parameterized heads to produce the trajectory-level value, subtask-level value, and interaction signal, respectively. The loss of the Critic Module should not affect action generation; thus, we stop gradient propagation to the VLM. Further details on the critic network architecture are provided in Appendix A. 

_2) Training Recipe:_ With the proposed architecture established, we now outline the optimization procedure. After obtaining _A_ ˆ( _st, at_ ) theusingstateN-stepvalueadvantagefunction, weestimationestimate[22]the advantageto update the policy via the IG-AWR algorithm. Specifically, we devise a three-stage RL training curriculum for the VLA models, as summarized in Algorithm 1: 

- **Stage I: Warm-up and SFT.** We collect demonstration data and employ a large-scale VLM to annotate subtask information. Interaction signals, rewards, and values are obtained. We use Knowledge Isolation [59] to train _π_ 0 _._ 5 (including subtask prediction loss). After a few warm-up steps, we train the critic module simultaneously using MSE loss for value regression and BCE loss for interaction prediction. 

- **Stage II: Offline RL.** We implement the IG-AWR algorithm to conduct RL training for the VLA and simultaneously 

**Algorithm 1** Interaction-Guided AWR for VLA Fine-tuning 

**Require:** Pre-trained VLA _π_ 0 _._ 5, Demonstration Buffer _D_ demo **Ensure:** Fine-tuned Policy _πθ_ , Critic _Vϕ_ 

- 1: **Data Annotation:** Annotate _D_ demo with subtasks, interaction signals _It_ , rewards, and values. 

- 2: _// Stage I: Warm-up and SFT_ 

- 3: Initialize Actor _πθ_ from _π_ 0 _._ 5 via SFT. 

- 4: Initialize Critic _Vϕ_ by minimizing _L_ MSE (State Value) and _L_ BCE (Interaction Signal) on _D_ demo. 

- 5: _// Stage II: Offline RL_ 6: **for** iteration _k_ = 1 _, . . . , K_ offline **do** 7: Estimate Advantage _A_<sup>ˆ</sup> on _D_ demo. 8: Update _πθ_ via IG-AWR and update _Vϕ_ . 9: **end for** 

- 10: _// Stage III: Human-in-the-Loop RL_ 11: Initialize Replay Buffer _D_ real _←∅_ 12: **while** not converged **do** 13: _s_ 0 _←_ env.reset() 14: **for** _t_ = 0 _, . . . , T_ **do** 15: Observe state _st_ , Critic outputs _V_ ( _st_ ) _, I_ ( _st_ ). 16: **if** _V_ ( _st_ ) stagnates **or** Human identifies failure **then** 17: _at ←_ HumanTeleop( _st_ ) _▷_ Human Override 18: **else** 19: _at ∼ πθ_ ( _·|st_ ) _▷_ Autonomous Execution 20: **end if** 21: Execute _at_ , observe _st_ +1. 22: **end for** 

- 23: Store episode to _D_ real. 24: **if** Update Interval **then** 25: Sample batch _B_ real _∼D_ real. 26: Sample equal-sized batch _B_ demo _∼D_ demo. 27: Construct Hybrid Dataset _B_ hybrid = _B_ real _∪B_ demo. 28: Update Policy _πθ_ via IG-AWR on _B_ hybrid. 29: Update Critic _Vϕ_ (at a lower frequency). 30: **end if** 

- 30: **end if** 31: **end while** 

update the critic module. In this phase, the agent learns to evaluate and utilize data, achieving efficient policy learning. 

_•_ **Stage III: Human-in-the-Loop RL.** We deploy the base policy in the real world to collect rollouts with Humanin-the-Loop intervention. By collecting high-quality human corrections, we enable the policy to approach its capability upper bound, realizing performance improvements especially for long-horizon complex tasks. 

_3) Human-in-the-Loop Mechanism:_ During real-world execution, the robot operates autonomously according to the policy _πθ_ while a human operator monitors the process. When the value output by the critic module exhibits stagnation or the human identifies a potential failure, the operator intervenes via a teleoperation interface to override the action. These intervention data are stored in the replay buffer, capturing both the low-value states preceding the takeover and the subsequent high-quality corrective trajectories. Periodically, we sample an equal number of episodes from the pre-collected demonstration buffer to construct a hybrid dataset. We then fine-tune the 

6 

ARXIV PREPRINT 

policy module using this dataset via the IG-AWR algorithm, while the critic module is updated at a lower frequency. This Human-in-the-Loop RL approach effectively overcomes distribution shifts and enables the mastery of complex longhorizon tasks that are difficult to solve via offline learning. 

## V. EXPERIMENTS 

In this section, we conduct comprehensive real-world experiments to evaluate the effectiveness of our proposed reinforced fine-tuning system. Our experiments are designed to answer three key research questions: 

- **Q1 (Overall Performance):** Does our reinforced finetuning system perform robustly in long-horizon complex real-world tasks and outperform SFT/RL baselines? 

- **Q2 (Ablation Study):** What are the contributions of individual components, specifically the IG-AWR algorithm and the hybrid dense reward function? 

- **Q3 (System Evolution):** How does the policy performance evolve across the three training stages (SFT, Offline RL, and Human-in-the-Loop RL)? 

## _A. Experimental Setup_ 

_1) Hardware and Environment:_ We perform all experiments on a real-world robotic platform consisting of a Galaxea A1 dual-arm robot equipped with parallel-jaw grippers. Visual observations are captured via a head-mounted Orbbec Gemini 2L camera and two wrist-mounted RealSense L515 cameras. The control frequency is set to 30 Hz, matching the data collection frequency. We set the action chunk size to 30 and employ the RTC method [60] for real-time control. Policy inference and training are executed on a cloud server equipped with an NVIDIA A100 GPU. The low-level control pipeline runs on a local PC with an Intel Core i7-12700KF 3.6GHz CPU, 32GB RAM, and an RTX 4070 GPU. Socket-based network communication is established between the local deployment endpoint and the cloud server inference endpoint. For detailed training hyperparameters and configurations, please refer to Appendix B. 

_2) Tasks:_ We select four challenging long-horizon manipulation tasks that involve multi-stage reasoning, contact-rich interactions, bimanual coordination, as well as articulated and deformable object manipulation. Task summaries are provided below and visualized in Figure 4; comprehensive descriptions—including subtask decomposition, success criteria and average steps—are available in Appendix C. 

- **Parcel Packing:** The robot must pick up an item on the plate, place it into the parcel, move the plate aside, and perform dual-arm collaboration to synchronously fold the flaps and close the box. This task requires precise bimanual coordination and contact-rich manipulation capabilities. 

- **Fruit Bagging:** The agent is required to open the lid of the canvas bag, sequentially pick up ginger, bitter melon, and banana, and place them into the bag. Finally, it needs to close the lid. This task involves articulated and deformable object manipulation, semantic understanding 

TABLE I: **Main Results on Real-world Long-horizon Tasks.** We compare the success rate (%) of our system against baselines across four tasks. Results are averaged over 20 trials per task. Best results are highlighted in **BOLD** . 

||**Parcel**|**Fruit**|**Block**|**Drink**||
|---|---|---|---|---|---|
|**Method**|**Packing**|**Bagging**|**Stacking**|**Shelving**|**Avg.**|
|SFT|15.0|30.0|25.0|5.0|18.8|
|IQL|40.0|50.0|45.0|20.0|38.8|
|AWR|35.0|55.0|45.0|25.0|40.0|
|**Ours**|**85.0**|**95.0**|**90.0**|**70.0**|**85.0**|


   - of object categories, and sequential picking from random positions. 

   - **Block Stacking:** The robot needs to pick up colored blocks from the table in the order of red, yellow, green, and blue, and sequentially stack them onto a plate. This task tests the capability for color-semantic understanding and precise stacking. 

   - **Drink Shelving:** The robot is required to retrieve beverages from a cluttered container, where the closer arm picks items from the top and performs a handover to the other arm, which then places them into narrow shelves from the side. This task tests dual-arm collaborative handover, bin-picking in cluttered environments, and precise placement in confined shelf spaces. 

- _3) Baselines:_ We compare our full system against the 

- following baselines: 

   - **SFT (** **_π_ 0** **_._ 5-Base):** The base flow-based VLA model finetuned solely via behavior cloning on the demonstration dataset. Action generation is trained using Knowledge Isolation [59] while subtask prediction is performed concurrently. 

   - **Offline RL (IQL/AWR):** Standard Offline RL methods [57], [61] applied to the _π_ 0 _._ 5 model, lacking our specific interaction guidance, dense reward shaping, and human intervention. 

_4) Data Collection and Metrics:_ For each task, we collect 60 expert demonstrations via teleoperation to form the initial dataset _D_ demo. During the Human-in-the-Loop stage, we perform 10 rollouts per training update and add them to _D_ real for IG-AWR updates, iterating 4 times (totaling 40 rollouts). For fair comparison, baseline methods without Human-in-theLoop utilize 100 expert demonstrations. The metric is **Success Rate (SR)** , defined as the ratio of successful trials to the total number of attempts. 

## _B. Main Results_ 

We present the comparative results in Table I. Our proposed system achieves the highest success rates across all four tasks, demonstrating superior generalization and robustness. 

_1) Superiority over SFT:_ Although VLA models learn diverse manipulation skills and semantic understanding through SFT during the pre-training stage, becoming a generalist policy, current SOTA methods still struggle to transfer knowledge to new real-world domains—including new embodiments and new tasks—using only a few (e.g., 100) task-specific 

SU ET AL.: IG-RFT: AN INTERACTION-GUIDED RL FRAMEWORK FOR VLA MODELS IN LONG-HORIZON ROBOTIC MANIPULATION 

7 


Fig. 4: **Execution Sequences of Long-Horizon Tasks.** From top to bottom, we visualize the successful execution flows for four challenging tasks: Parcel Packing, Fruit Bagging, Block Stacking, and Drink Shelving. Arrows indicate the progression of subgoals. **Note:** The text labels above each stage are abbreviated for visualization clarity and differ from the actual natural language instructions used by the model. For the detailed sequence of subtask instructions for each task, please refer to Appendix C. 

demonstrations to accomplish long-horizon complex tasks. Moreover, SFT is typically constrained by the quality of manually pre-collected data and is more prone to converge to suboptimal distributions. In contrast, RL fine-tuning VLA models for new domains demonstrates superior adaptation. As shown in Table I, the SFT policy achieves the lowest success rates in our real-world complex tasks, underperforming all other methods that employ RL fine-tuning. Our method, in particular, significantly improves the success rate over the SFT policy. The results demonstrate that fine-tuning VLA models using RL indeed enables the policy to learn a better action distribution, thereby avoiding compounding errors caused by minor deviations, enhancing the capability to handle longhorizon tasks in new real-world domains. 

_2) Advantage over Offline RL:_ Deploying standard Offline RL baselines (IQL/AWR) to fine-tune VLA models can learn a better task-specific action distribution compared to SFT; however, these methods still suffer from distribution shift problems. Meanwhile, purely online RL on real-world embodiments faces challenges of low exploration efficiency and safety concerns. In contrast, the Human-in-the-Loop approach 

provides human prior guidance to efficiently drive policy evolution. Compared to Offline RL (Table I), our multi-stage RL fine-tuning system achieves substantially higher performance gains and demonstrates greater robustness in the real world. In our experimental setting, our method improves performance by approximately 40% across all four long-horizon complex tasks. This validates the effectiveness and practicality of our reinforced fine-tuning system, thereby answering **Q1** . 

## _C. Ablation Studies_ 

To validate our design choices, we conduct ablation studies on the **Parcel Packing** and **Drink Shelving** tasks, which demand the most complex manipulation capabilities. This section answers **Q2** . 

_1) Effect of Interaction-Guided AWR:_ We compare our IGAWR with a standard AWR implementation that also follows the three-stage training recipe but uses uniform exploration noise. As illustrated in Table II, removing the interactionguided dynamic uncertainty modulation results in a performance drop of approximately 15%. Qualitative analysis reveals 

8 

ARXIV PREPRINT 

TABLE II: **Ablation Study Results.** We evaluate the contribution of Interaction Guidance (IG) and Reward Function on the two most challenging tasks. 

|**Configuration**|**Parcel**<br>**Packing**|**Drink**<br>**Shelving**|**Avg. Drop**|
|---|---|---|---|
|**Ours (Full System)**|**85.0**|**70.0**|-|
|_w/o Interaction Guidance_|70.0|55.0|_↓_15.0|
|_w/o Trajectory-level Reward_|75.0|60.0|_↓_10.0|
|_w/o Subtask-level Reward_|55.0|45.0|_↓_27.5|


TABLE III: **Subtask Completion Progress.** Instead of binary success rates, we report the normalized progress score (0.01.0), representing the average proportion of subtasks completed per episode. This metric reveals when the policy fails. 

||**Parcel**|**Drink**||
|---|---|---|---|
|**Reward Configuration**|**Packing**|**Shelving**|**Avg. Progress**|
|**Ours (Hybrid)**|**0.96**|**0.88**|**0.92**|
|_w/o Trajectory Reward_|0.84|0.78|0.81|
|_w/o Subtask Reward_|0.68|0.54|0.61|


that without interaction guidance, the robot tends to jitter during the delicate ”flap folding and box closing” phase. Furthermore, we observe that without interaction guidance, the agent lacks sufficient exploration during non-interactive phases, leading to poor generalization regarding object positions. It often drifts towards the object locations seen in the pre-collected data, consequently causing task failure when facing out-of-distribution (OOD) cases during testing. 

Beyond final performance, we further investigate the impact of IG on data efficiency in Figure 5. IG-RFT is represented by the red curve, while the baseline AWR w/ dense reward is represented by the blue curve and AWR w/o dense reward by the gray curve. Our method exhibits a significantly steeper learning trajectory. IG-RFT achieves an average success rate of 77.5% with only 40 human interventions, and ultimately converges to an 82.5% success rate. The AWR w/ dense reward method learns more slowly, reaching only 62.5% under the same 40 human interventions. This demonstrates that our method achieves superior performance with significantly lower human cost. Even when the data scale is extended to 70 episodes, the baseline without IG fails to match the peak performance of IG-RFT. This confirms that modulating exploration based on visual interaction signals not only improves policy performance but also drastically reduces the human effort required for fine-tuning. The other baseline, AWR w/o dense reward, further validates this conclusion and highlights that our dense reward is equally significant for policy improvement in Human-in-the-Loop learning. 

_2) Effect of Hybrid Dense Reward:_ We evaluate the system using only the trajectory-level reward or the subtask-level reward compared to our hybrid dense reward (Trajectory + Subtask) in Table II, and further analyze failure modes using the subtask completion progress metric in Table III. The results indicate that relying on a single reward signal leads to degraded task success rates, which is particularly evident in our long-horizon complex task settings. Specifically, the lack 


Fig. 5: **Data Efficiency Analysis in Human-in-the-Loop Fine-tuning.** We report the mean success rates averaged over the Parcel Packing and Drink Shelving tasks. The curves show that IG-RFT (Ours) achieves superior sample efficiency, converging to 77.5% success with only 40 interventions, significantly outperforming baselines. Shaded regions indicate the min-max range across tasks. 

of the subtask-level reward results in a substantial 27% drop in success rate and a significant 0.31 drop in progress score. This demonstrates that dense incentive signals are critical for facilitating the completion of sequential sub-goals. In contrast, the absence of the trajectory-level reward causes a 10% drop in success rate, yet the progress score decreases only marginally by 0.11. This indicates that the subtask reward facilitates the completion of intermediate sub-goals, even if the task ultimately fails. We observe that the trajectory-level reward provides long-term guidance towards the final goal, offering macroscopic assurance for the agent to learn the ultimate objective. Conversely, the subtask-level reward offers immediate guidance for short-term objectives, enabling the agent to master sequential sub-goals progressively. Collectively, these results demonstrate that the hybrid reward structure is highly beneficial for the reinforced fine-tuning system. 

## _D. Analysis of Training Stages_ 

We analyze the policy evolution throughout the three-stage RL training system in Table IV, investigating the contribution of each phase to the final performance. This section answers **Q3** . Detailed analysis for each stage is as follows. 

- **Stage I (SFT):** The supervised fine-tuning stage establishes adaptation to the new domain, acquires basic manipulation skills and semantic understanding capabilities, but exhibits limited robustness in long-horizon execution, achieving an average success rate of only 18.8%. This indicates that the generalization and versatility of VLA models still have substantial room for improvement in real-world settings. 

- **Stage II (Offline RL):** By optimizing the policy using the interaction-guided objective on pre-collected datasets, the agent learns to distinguish high-value actions from 

SU ET AL.: IG-RFT: AN INTERACTION-GUIDED RL FRAMEWORK FOR VLA MODELS IN LONG-HORIZON ROBOTIC MANIPULATION 

9 

TABLE IV: **Policy Evolution and Stage Analysis.** We compare the performance at different training stages. Results are averaged over 20 trials per task. **HIL** denotes Human-in-the-Loop. Best results are highlighted in **BOLD** . 

|**Training Stage / Configuration**|**Parcel Packing**|**Fruit Bagging**|**Block Stacking**|**Drink Shelving**|**Avg.**|**Avg. Drop**|
|---|---|---|---|---|---|---|
|**Stage I:** SFT|15.0|30.0|25.0|5.0|18.8|_↓_66.2|
|**Stage II:** Offline RL|40.0|55.0|45.0|20.0|40.0|_↓_45.0|
|_SFT →HIL (w/o Stage II)_|65.0|75.0|70.0|45.0|63.8|_↓_21.2|
|**Stage III:** Full System|**85.0**|**95.0**|**90.0**|**70.0**|**85.0**|-|


sub-optimal ones, improving the success rate significantly to 40.0%. Although distribution shift problems remain during real-world rollouts, limiting the success rate, this stage provides a crucial warm-up for the subsequent online phase. 

- **Stage III (Full System vs. Direct HIL):** Introducing human intervention provides critical corrections for OOD states. As shown in Table IV, our full system (Stage I _→_ II _→_ III) achieves a superior success rate of **85.0%** . Notably, skipping Stage II and performing Human-in-theLoop directly on the SFT model ( _Stage I → III_ ) yields a suboptimal success rate of 63.8%. This performance gap (21.2%) highlights that the basic distribution of the actor and critic modules learned in Stage II is essential for maximizing the sample efficiency of human corrections. The results show that our three-stage RL fine-tuning system is indispensable for policy evolution. 

## _E. Qualitative Analysis_ 

To provide intuitive insights into the internal mechanisms of IG-RFT, we visualize the extraction of interaction signals and the dynamics of value estimation during real-world execution. 

First, we validate the effectiveness of our visual interaction extraction module in Figure 6. By combining global RGB observations with dense optical flow and robot masking, our system accurately quantifies the intensity of environmental changes. Following Eq. 1, we determine the interaction status ( _It_ ) by calculating the moving pixel count and applying a threshold Θpixel = 400. The visualization highlights four representative frames selected from the interaction phase for both the Parcel Packing and Drink Shelving tasks. This method allows for the convenient and automatic extraction of interaction information. By reducing exploration noise during interaction phases to enhance stability and robustness, while employing higher variance exploration in non-interaction zones to foster diverse trajectories and generalization, this pipeline effectively balances exploration and exploitation in RL. 

Furthermore, we analyze the critic’s ability to evaluate policy performance by visualizing the predicted state value ( _Vt_ ) trajectories in Figure 7. The red curve represents the critic’s real-time prediction, while the dashed grey line indicates the reference value. In successful rollouts, the predicted value closely follows the reference, monotonically decreasing as subtasks are completed. Crucially, the critic exhibits high sensitivity to suboptimal actions. As highlighted by the blue shaded regions, the predicted value fluctuates or rises abnormally when the agent executes actions suboptimally, indicating potential risks rather than explicit failures. For 


Fig. 6: **Visualization of Interaction Signal Extraction.** We illustrate the process of quantifying interaction intensity. For each sample frame, the left panel shows the raw RGB observation from global camera view, while the right panel displays the dense optical flow with the robot body masked out (black region). The “Moving Pix” count represents the magnitude of environmental motion<sup>�</sup> (1 _− Mt_ ) _·_ I( _||Ft||_<sup>2</sup> _> δ_ flow), which serves as the threshold metric for determining the binary interaction signal _It_ . 

instance, in the Parcel Packing task, a ”slight grasp offset” or ”premature motion” causes immediate value deviations. Similarly, in the Drink Shelving task, events like ”unstable drink grasp” or ”shelf collision” trigger distinct value peaks. These results demonstrate that our dense value function not only guides the policy towards the goal but also serves as an effective indicator of execution quality, providing critical dense feedback that significantly facilitates policy optimization during Reinforcement Learning. 

## VI. CONCLUSION 

In this work, we presented IG-RFT, a comprehensive reinforced fine-tuning system tailored for flow-based VLA models to master long-horizon complex manipulation tasks in the real world. To balance exploration and exploitation in RL training, we innovatively posit that interaction status contains strong prior guidance information for long-horizon 

10 

ARXIV PREPRINT 


Fig. 7: **Visualization of Value during one rollout in Long-Horizon Tasks.** We plot the critic-model-predicted state value (Return-to-Go) trajectories for **(A) Parcel Packing** and **(B) Drink Shelving** tasks. The dashed grey line represents the reference value function designed in Section IV-A, while the solid red line shows the predicted value during real-world execution. The images from left to right sequentially represent a successful task; the blue-highlighted images correspond to value peaks, indicating the policy took suboptimal actions. For each suboptimal case, we describe the potential reasons with text above the images. The corresponding subtask stages are annotated in grey italic text along the timeline. 

contact-rich manipulation. Integrating this insight, we proposed the Interaction-Guided Advantage Weighted Regression (IG-AWR) algorithm, which dynamically modulates flow models at the noise level. Addressing the training difficulties caused by sparse rewards in RL and the fact that task-specific dense rewards require careful manual design and are hard to scale, we proposed a hybrid dense reward function. This function includes trajectory-level and subtask-level rewards, simultaneously achieving density and generalization. 

Furthermore, our multi-stage training paradigm demonstrates a clear evolution of policy performance: establishing basic domain adaptation and value function estimation via SFT, optimizing to realize efficient policy learning via Offline RL, and achieving policy evolution while maintaining robust generalization through Human-in-the-Loop corrections. Realworld experiments across four challenging tasks validate that our method surpasses SFT and standard RL baselines by a significant margin, with approximately 40% improvement. We also implemented comprehensive ablation experiments to validate our design choices. 

As a powerful and effective policy improvement technique, RL possesses the potential to enable SFT models to break through the upper limit of their representation capability. However, existing research, including this work, tends to utilize RL as a fine-tuning method to bridge the domain gap and improve task success rates, rather than applying RL to 

large-scale training as seen in Large Language Models (LLMs) [62], [63]. We attribute this to two main reasons: 1) Sampling and exploration using policy gradient-based online RL (like GRPO, PPO) [64], [65] in the high-dimensional action space of the real world are expensive, while simulation faces a significant sim-to-real gap, and Human-in-the-Loop guidance relies heavily on manual labor, making it difficult to scale up. 2) A general Reward Model that can be directly applied to fully on-policy, online, and new real-world domains does not yet exist; the lack of real-time feedback from such a model poses significant challenges for real-robot on-policy learning. 

Future work will focus on two directions: applying RL to large-scale VLA post-training across multi-task and wideranging embodiments. Since human feedback currently remains an indispensable means, investigating how to efficiently provide feedback to enable robots to autonomously approach on-policy exploration holds great research promise. Additionally, training large reward models with world models—particularly through paradigms such as physics-aware video generation—represents a crucial pathway toward scalable RL for real-world robotics [66]. 

## APPENDIX A 

## CRITIC NETWORK ARCHITECTURE 

The critic module is designed based on an attention-based aggregation architecture inspired by Q-Former [58]. To ef- 

SU ET AL.: IG-RFT: AN INTERACTION-GUIDED RL FRAMEWORK FOR VLA MODELS IN LONG-HORIZON ROBOTIC MANIPULATION 

11 

ficiently capture multimodal context, we initialize _Nq_ = 8 learnable query tokens, each with an embedding dimension of _D_ = 256. These queries interact with the frozen VLA features—extracted selectively from specific middle and late layers of the backbone (indices 11, 14, and 17 in our 18layer model)—through a multi-head cross-attention mechanism with 8 heads. Note that we explicitly detach gradients from the VLA backbone to prevent interference with the policy representation. The aggregated features are then fed into three independent Multi-Layer Perceptron (MLP) heads. Specifically, each MLP head projects the 256-dimensional feature to a hidden dimension of 128 before producing a final scalar output. The heads are optimized over sampled batches _B_ as follows: 

- 1) **Trajectory Value** _V_ traj( _s_ ): Predicted by the task head to estimate long-term task success probability. It is optimized by minimizing the expected Mean Squared Error (MSE) against the ground truth return _y_ traj: 


- 2) **Subtask Value** _V_ sub( _s_ ): Predicted by the subtask head to track the progress of the current sub-goal. Similarly, it minimizes the expected MSE loss with respect to the subtask value label _y_ sub: 


- 3) **Interaction Probability** _p_ int( _s_ ): Predicted by the interaction head to identify contact-rich phases. It uses a Sigmoid activation and is supervised via the expected Binary Cross-Entropy (BCE) loss against the binary interaction label _y_ int: 


The total critic loss is the summation of these three components: _L_ critic = _L_ traj + _L_ sub + _L_ int. 

TABLE V: Hyperparameters for IG-RFT Training 

|**Parameter**|**Value**|
|---|---|
|_General Optimizati_<br>|_on_<br>|
|Optimizer|AdamW|
|LR Schedule|CosineDecay<br>|
|Learning Rate (Actor)|5_×_10<sup>_−_5</sup><br>|
|Learning Rate (Critic)|5_×_10<sup>_−_6</sup>|
|Batch Size|64|
|Gradient Clipping|1.0|
|EMA Decay|0.999|
|LR Warm-up Steps|1,000|
|Critic Warm-up Steps|2,000|
|TotalTrainingSteps|30000|
|<br>_IG-AWR Algorithm_<br>|,<br><br>|
|AWR Temperature _β_|0.05|
|Advantage Clipping|[0_,_10]|
|IG Flow Threshold _δ_flow|2.0|
|IG Pixel Threshold Θpixel|400|
|Exploration _σ_base|1.5|
|Exploration _σ_min|0.2|
|Exploration Modulation _α_|0.9|
|Discount Factor _γ_|1.0|
|Trajectory Reward Weight _ω_traj|0.4|
|Subtask Reward Weight _ω_sub|0.6|
|_Training Schedule_<br>||
|SFT Warm-up Steps|5,000|
|Offline RL Training Steps|25,000|
|HitL RL Iterations|4|
|HitL RL Update Interval|10|
|Actor Update Frequency|1.0|
|Critic Update Frequency|0.5|


1. Pick up the _⟨_ item _⟩_ from the plate. 

2. Place the item into the paper box. 

3. Move the plate aside. 

4. Move the paper box to the center. 

5. Fold the lid of the paper box. 

## APPENDIX B HYPERPARAMETERS 

We list the key hyperparameters used in our experiments in Table V. For the SFT stage, we use the standard flow matching objective. In the RL stages (Offline and Human-in-the-Loop), we utilize the proposed IG-AWR algorithm. The critic network is trained using a separate optimizer. 

## APPENDIX C TASK DESCRIPTIONS 

We provide detailed descriptions and strict success criteria for the four evaluation tasks to ensure experimental rigor. 

- **Parcel Packing:** 

- _Goal:_ Place an item into a box and close the box. 

- _Success Criteria:_ The object must be fully inside the box, and flaps must be folded flat (sealed). 

- _Subtasks Sequence:_ 

- _Average Steps:_ 1731. 

## _•_ **Fruit Bagging:** 

- _Goal:_ Put three specific fruits (ginger, bitter melon, banana) into a canvas bag and close it. 

- _Success Criteria:_ All three items must be inside, and the lid must cover the opening. 

- _Subtasks Sequence:_ 

   1. Open the lid of the canvas bag. 

   2. **For each** _⟨_ item _⟩_ in _{_ ginger, bitter melon, banana _}_ : 

      - Pick up the _⟨_ item _⟩_ from the tabletop. 

      - Place the _⟨_ item _⟩_ into the canvas bag. 

   3. Move the canvas bag to the center. 

   4. Close the lid of the canvas bag. 

- _Average Steps:_ 2517. 

- **Block Stacking:** 

- _Goal:_ Stack 4 colored blocks in a specific order (Red 

12 

ARXIV PREPRINT 

- _→_ Yellow _→_ Green _→_ Blue). 

- _Success Criteria:_ The stack must stand vertically for at least 3 seconds after release. 

- _Subtasks Sequence:_ 

1. Pick up the red block from the tabletop. 

2. Place the red block on the plate. 

3. **For each pairs** _⟨_ source _,_ target _⟩_ in sequence 

   - _{_ (yellow _,_ red) _,_ (green _,_ yellow) _,_ (blue _,_ green) _}_ : 

   - Pick up the _⟨_ source _⟩_ block from the tabletop. 

   - Stack the _⟨_ source _⟩_ block on the _⟨_ target _⟩_ block. 

- _Average Steps:_ 1899. 

- **Drink Shelving:** 

- _Goal:_ Place the container lid on the top shelf, then retrieve 4 drinks from a bin and place them onto the middle shelf via dual-arm handover. 

- _Success Criteria:_ The lid must be on the top shelf. All 4 drinks must be placed upright on the middle shelf layer without falling. 

- _Subtasks Sequence:_ 

1. Pick up the container lid from the bin. 

2. Place the lid onto the top shelf. 

3. **For each** _⟨_ loc _⟩_ in sequence 

   - _{_ leftmost _,_ second-left _,_ second-right _,_ rightmost _}_ : 

   - Pick up the _⟨_ loc _⟩_ drink from the bin using a top-down grasp. 

   - Hand over the drink to the other arm. 

   - Place the drink onto the middle shelf via sideinsertion. 

- _Average Steps:_ 2931. 

## REFERENCES 

- [1] H. Dong, J. Li, K. Zhu, H. Guo, and G. Lu, “Enabling to learn for force sensing: A coupling-decoupling under-actuated gripper with multiple-dofs,” _The International Journal of Robotics Research_ , p. 02783649251378155, 2025. 

- [2] Z. Su, Y. Ma, H. Guo, and H. Dong, “Construction of bin-picking system for logistic application: A hybrid robotic gripper and vision-based grasp planning,” _IEEE Robotics and Automation Letters_ , 2025. 

- [3] Z. Lin, H. Dong, W. Kong, H. Huang, I.-M. Chen, and H. Dong, “A coarse-to-fine multimodal detection framework based on deep learning for robotic coating tasks,” _IEEE/ASME Transactions on Mechatronics_ , 2025. 

- [4] S. Fei, S. Wang, J. Shi, Z. Dai, J. Cai, P. Qian, L. Ji, X. He, S. Zhang, Z. Fei _et al._ , “Libero-plus: In-depth robustness analysis of visionlanguage-action models,” _arXiv preprint arXiv:2510.13626_ , 2025. 

- [5] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter _et al._ , “ _π_ 0: A vision-language-action flow model for general robot control.” _arXiv preprint ARXIV.2410.24164_ . 

- [6] NVIDIA, J. Bjorck, N. C. Fernando Casta˜neda, X. Da, R. Ding, L. J. Fan, Y. Fang, D. Fox, F. Hu, S. Huang, J. Jang, Z. Jiang, J. Kautz, K. Kundalia, L. Lao, Z. Li, Z. Lin, K. Lin, G. Liu, E. Llontop, L. Magne, A. Mandlekar, A. Narayan, S. Nasiriany, S. Reed, Y. L. Tan, G. Wang, Z. Wang, J. Wang, Q. Wang, J. Xiang, Y. Xie, Y. Xu, Z. Xu, S. Ye, Z. Yu, A. Zhang, H. Zhang, Y. Zhao, R. Zheng, and Y. Zhu, “GR00T N1: An open foundation model for generalist humanoid robots,” in _ArXiv Preprint_ , March 2025. 

- [7] K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. R. Equi, C. Finn, N. Fusai, M. Y. Galliker _et al._ , “ _π_ 0 _._ 5: a visionlanguage-action model with open-world generalization,” in _9th Annual Conference on Robot Learning_ , 2025. 

- [8] M. Shukor, D. Aubakirova, F. Capuano, P. Kooijmans, S. Palma, A. Zouitine, M. Aractingi, C. Pascal, M. Russi, A. Marafioti _et al._ , “Smolvla: A vision-language-action model for affordable and efficient robotics,” _arXiv preprint arXiv:2506.01844_ , 2025. 

- [9] A. Zhai, B. Liu, B. Fang, C. Cai, E. Ma, E. Yin, H. Wang, H. Zhou, J. Wang, L. Shi _et al._ , “Igniting vlms toward the embodied space,” _arXiv preprint arXiv:2509.11766_ , 2025. 

- [10] A. Yakefu, B. Xie, C. Xu, E. Zhang, E. Zhou, F. Jia, H. Yang, H. Fan, H. Zhang, H. Peng _et al._ , “Robochallenge: Large-scale real-robot evaluation of embodied policies,” _arXiv preprint arXiv:2510.17950_ , 2025. 

- [11] M. J. Kim, C. Finn, and P. Liang, “Fine-tuning vision-languageaction models: Optimizing speed and success,” _arXiv preprint arXiv:2502.19645_ , 2025. 

- [12] J. Zheng, J. Li, Z. Wang, D. Liu, X. Kang, Y. Feng, Y. Zheng, J. Zou, Y. Chen, J. Zeng _et al._ , “X-vla: Soft-prompted transformer as scalable cross-embodiment vision-language-action model,” _arXiv preprint arXiv:2510.10274_ , 2025. 

- [13] K. Chen, Z. Liu, T. Zhang, Z. Guo, S. Xu, H. Lin, H. Zang, X. Li, Q. Zhang, Z. Yu _et al._ , “ _πRL_ : Online rl fine-tuning for flow-based vision-language-action models,” _arXiv preprint arXiv:2510.25889_ , 2025. 

- [14] C. Yu, Y. Wang, Z. Guo, H. Lin, S. Xu, H. Zang, Q. Zhang, Y. Wu, C. Zhu, J. Hu _et al._ , “Rlinf: Flexible and efficient large-scale reinforcement learning via macro-to-micro flow transformation,” _arXiv preprint arXiv:2509.15965_ , 2025. 

- [15] A. Ye, Z. Zhang, B. Wang, X. Wang, D. Zhang, and Z. Zhu, “Vla-r1: Enhancing reasoning in vision-language-action models,” _arXiv preprint arXiv:2510.01623_ , 2025. 

- [16] W. Xiao, H. Lin, A. Peng, H. Xue, T. He, Y. Xie, F. Hu, J. Wu, Z. Luo, L. Fan _et al._ , “Self-improving vision-language-action models with data generation via residual rl,” _arXiv preprint arXiv:2511.00091_ , 2025. 

- [17] H. Deng, Z. Wu, H. Liu, W. Guo, Y. Xue, Z. Shan, C. Zhang, B. Jia, Y. Ling, G. Lu _et al._ , “A survey on reinforcement learning of visionlanguage-action models for robotic manipulation,” _Authorea Preprints_ , 2025. 

- [18] B. Wang, Z. Lin, W. Kong, and H. Dong, “Bin packing optimization via deep reinforcement learning,” _IEEE Robotics and Automation Letters_ , vol. 10, no. 3, pp. 2542–2549, 2025. 

- [19] Y. Wang, W. Yu, H. Wu, H. Guo, and H. Dong, “Sa-dem: Dexterous extrinsic robotic manipulation of non-graspable objects via stiffness-aware dual-stage reinforcement learning,” _IEEE Transactions on Automation Science and Engineering_ , vol. 23, pp. 347–362, 2025. 

- [20] J. Luo, C. Xu, J. Wu, and S. Levine, “Precise and dexterous robotic manipulation via human-in-the-loop reinforcement learning,” _Science Robotics_ , vol. 10, no. 105, p. eads5033, 2025. 

- [21] Y. Chen, S. Tian, S. Liu, Y. Zhou, H. Li, and D. Zhao, “Conrft: A reinforced fine-tuning method for vla models via consistency policy,” _arXiv preprint arXiv:2502.05450_ , 2025. 

- [22] Physical Intelligence, A. Amin _et al._ , “ _π_ 0<sup>_∗_</sup> _._ 6<sup>:AVLAthatlearnsfrom</sup> experience,” _arXiv preprint arXiv:2511.14759_ , 2025. 

- [23] H. Zhang, Z. Zhuang, H. Zhao, P. Ding, H. Lu, and D. Wang, “Reinbot: Amplifying robot visual-language manipulation with reinforcement learning,” _arXiv preprint arXiv:2505.07395_ , 2025. 

- [24] C.-Y. Hung, N. Majumder, H. Deng, L. Renhang, Y. Ang, A. Zadeh, C. Li, D. Herremans, Z. Wang, and S. Poria, “Nora-1.5: A visionlanguage-action model trained using world model-and action-based preference rewards,” _arXiv preprint arXiv:2511.14659_ , 2025. 

- [25] Z. Zhang, K. Zheng, Z. Chen, J. Jang, Y. Li, S. Han, C. Wang, M. Ding, D. Fox, and H. Yao, “Grape: Generalizing robot policy via preference alignment,” _arXiv preprint arXiv:2411.19309_ , 2024. 

- [26] S. Zhai, Q. Zhang, T. Zhang, F. Huang, H. Zhang, M. Zhou, S. Zhang, L. Liu, S. Lin, and J. Pang, “A vision-language-action-critic model for robotic real-world reinforcement learning,” _arXiv preprint arXiv:2509.15937_ , 2025. 

- [27] H. Zhang, S. Zhang, J. Jin, Q. Zeng, Y. Qiao, H. Lu, and D. Wang, “Balancing signal and variance: Adaptive offline rl post-training for vla flow models,” _arXiv preprint arXiv:2509.04063_ , 2025. 

- [28] J. Luo, Z. Hu, C. Xu, Y. L. Tan, J. Berg, A. Sharma, S. Schaal, C. Finn, A. Gupta, and S. Levine, “Serl: A software suite for sample-efficient robotic reinforcement learning,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 16 961–16 969. 

- [29] Y. Li, X. Ma, J. Xu, Y. Cui, Z. Cui, Z. Han, L. Huang, T. Kong, Y. Liu, H. Niu _et al._ , “Gr-rl: Going dexterous and precise for long-horizon robotic manipulation,” _arXiv preprint arXiv:2512.01801_ , 2025. 

- [30] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn, “Learning finegrained bimanual manipulation with low-cost hardware,” _arXiv preprint arXiv:2304.13705_ , 2023. 

- [31] C. Chi, Z. Xu, S. Feng, E. Cousineau, Y. Du, B. Burchfiel, R. Tedrake, and S. Song, “Diffusion policy: Visuomotor policy learning via action diffusion,” _The International Journal of Robotics Research_ , vol. 44, no. 10-11, pp. 1684–1704, 2025. 

SU ET AL.: IG-RFT: AN INTERACTION-GUIDED RL FRAMEWORK FOR VLA MODELS IN LONG-HORIZON ROBOTIC MANIPULATION 

13 

- [32] S. K. S. Ghasemipour, A. Wahid, J. Tompson, P. Sanketi, and I. Mordatch, “Self-improving embodied foundation models,” _arXiv preprint arXiv:2509.15155_ , 2025. 

- [33] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi _et al._ , “Openvla: An opensource vision-language-action model,” _arXiv preprint arXiv:2406.09246_ , 2024. 

- [34] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, J. Dabis, C. Finn, K. Gopalakrishnan, K. Hausman, A. Herzog, J. Hsu _et al._ , “Rt-1: Robotics transformer for real-world control at scale,” _arXiv preprint arXiv:2212.06817_ , 2022. 

- [35] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid _et al._ , “Rt-2: Vision-language-action models transfer web knowledge to robotic control,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 2165–2183. 

- [36] K. Pertsch, K. Stachowicz, B. Ichter, D. Driess, S. Nair, Q. Vuong, O. Mees, C. Finn, and S. Levine, “Fast: Efficient action tokenization for vision-language-action models,” _arXiv preprint arXiv:2501.09747_ , 2025. 

- [37] L. X. Shi, B. Ichter, M. Equi, L. Ke, K. Pertsch, Q. Vuong, J. Tanner, A. Walling, H. Wang, N. Fusai _et al._ , “Hi robot: Open-ended instruction following with hierarchical vision-language-action models,” _arXiv preprint arXiv:2502.19417_ , 2025. 

- [38] G. Lu, W. Guo, C. Zhang, Y. Zhou, H. Jiang, Z. Gao, Y. Tang, and Z. Wang, “Vla-rl: Towards masterful and general robotic manipulation with scalable reinforcement learning,” _arXiv preprint arXiv:2505.18719_ , 2025. 

- [39] J. Liu, F. Gao, B. Wei, X. Chen, Q. Liao, Y. Wu, C. Yu, and Y. Wang, “What can rl bring to vla generalization? an empirical study,” _arXiv preprint arXiv:2505.19789_ , 2025. 

- [40] Y. Chebotar, Q. Vuong, K. Hausman, F. Xia, Y. Lu, A. Irpan, A. Kumar, T. Yu, A. Herzog, K. Pertsch _et al._ , “Q-transformer: Scalable offline reinforcement learning via autoregressive q-functions,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 3909–3928. 

- [41] H. Li, Y. Zuo, J. Yu, Y. Zhang, Z. Yang, K. Zhang, X. Zhu, Y. Zhang, T. Chen, G. Cui _et al._ , “Simplevla-rl: Scaling vla training via reinforcement learning,” _arXiv preprint arXiv:2509.09674_ , 2025. 

- [42] C. Zhang, Z. Wan, F. Chen, X. Yu, I. Tsang, and B. An, “Gorl: An algorithm-agnostic framework for online reinforcement learning with generative policies,” _arXiv preprint arXiv:2512.02581_ , 2025. 

- [43] J. Liu, G. Liu, J. Liang, Y. Li, J. Liu, X. Wang, P. Wan, D. Zhang, and W. Ouyang, “Flow-grpo: Training flow matching models via online rl,” _arXiv preprint arXiv:2505.05470_ , 2025. 

   - [55] C. Yuan, S. Joshi, S. Zhu, H. Su, H. Zhao, and Y. Gao, “Roboengine: Plug-and-play robot data augmentation with semantic robot segmentation and background generation,” _arXiv preprint arXiv:2503.18738_ , 2025. 

   - [56] Z. Teed and J. Deng, “Raft: Recurrent all-pairs field transforms for optical flow,” in _European conference on computer vision_ . Springer, 2020, pp. 402–419. 

   - [57] X. B. Peng, A. Kumar, G. Zhang, and S. Levine, “Advantage-weighted regression: Simple and scalable off-policy reinforcement learning,” _arXiv preprint arXiv:1910.00177_ , 2019. 

   - [58] J. Li, D. Li, S. Savarese, and S. Hoi, “Blip-2: Bootstrapping languageimage pre-training with frozen image encoders and large language models,” in _International conference on machine learning_ . PMLR, 2023, pp. 19 730–19 742. 

   - [59] D. Driess, J. T. Springenberg, B. Ichter, L. Yu, A. Li-Bell, K. Pertsch, A. Z. Ren, H. Walke, Q. Vuong, L. X. Shi _et al._ , “Knowledge insulating vision-language-action models: Train fast, run fast, generalize better,” _arXiv preprint arXiv:2505.23705_ , 2025. 

   - [60] K. Black, M. Y. Galliker, and S. Levine, “Real-time execution of action chunking flow policies,” _arXiv preprint arXiv:2506.07339_ , 2025. 

   - [61] I. Kostrikov, A. Nair, and S. Levine, “Offline reinforcement learning with implicit q-learning,” _arXiv preprint arXiv:2110.06169_ , 2021. 

   - [62] L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. Wainwright, P. Mishkin, C. Zhang, S. Agarwal, K. Slama, A. Ray _et al._ , “Training language models to follow instructions with human feedback,” _Advances in neural information processing systems_ , vol. 35, pp. 27 730–27 744, 2022. 

   - [63] D. Guo, D. Yang, H. Zhang, J. Song, R. Zhang, R. Xu, Q. Zhu, S. Ma, P. Wang, X. Bi _et al._ , “Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning,” _arXiv preprint arXiv:2501.12948_ , 2025. 

   - [64] Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, X. Bi, H. Zhang, M. Zhang, Y. Li, Y. Wu _et al._ , “Deepseekmath: Pushing the limits of mathematical reasoning in open language models,” _arXiv preprint arXiv:2402.03300_ , 2024. 

   - [65] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 

   - [66] M. J. Kim, Y. Gao, T.-Y. Lin, Y.-C. Lin, Y. Ge, G. Lam, P. Liang, S. Song, M.-Y. Liu, C. Finn _et al._ , “Cosmos policy: Fine-tuning video models for visuomotor control and planning,” _arXiv preprint arXiv:2601.16163_ , 2026. 

- [44] M. Lyu, Y. Sun, E. Lin, H. Li, R. Chen, F. Zhao, and Y. Zeng, “Reinforcement fine-tuning of flow-matching policies for vision-languageaction models,” _arXiv preprint arXiv:2510.09976_ , 2025. 

- [45] K. Frans, S. Park, P. Abbeel, and S. Levine, “Diffusion guidance is a controllable policy improvement operator,” _arXiv preprint arXiv:2505.23458_ , 2025. 

- [46] A. Wagenmaker, M. Nakamoto, Y. Zhang, S. Park, W. Yagoub, A. Nagabandi, A. Gupta, and S. Levine, “Steering your diffusion policy with latent space reinforcement learning,” _arXiv preprint arXiv:2506.15799_ , 2025. 

- [47] J. Zhang, Z. Huang, C. Gu, Z. Ma, and L. Zhang, “Reinforcing action policies by prophesying,” _arXiv preprint arXiv:2511.20633_ , 2025. 

- [48] F. Zhu, Z. Yan, Z. Hong, Q. Shou, X. Ma, and S. Guo, “WMPO: World model-based policy optimization for vision-language-action models,” _arXiv preprint arXiv:2511.09515_ , 2025. 

- [49] S. Fei, S. Wang, L. Ji, A. Li, S. Zhang, L. Liu, J. Hou, J. Gong, X. Zhao, and X. Qiu, “Srpo: Self-referential policy optimization for vision-language-action models,” _arXiv preprint arXiv:2511.15605_ , 2025. 

- [50] F. Xu, G. Zhai, X. Kong, T. Fu, D. F. Gordon, X. An, and B. Busam, “Stare-vla: Progressive stage-aware reinforcement for fine-tuning visionlanguage-action models,” _arXiv preprint arXiv:2512.05107_ , 2025. 

- [51] M. Dai, L. Liu, Y. Bai, Y. Liu, Z. Wang, R. Su, C. Chen, L. Lin, and X. Wu, “Rover: Robot reward model as test-time verifier for visionlanguage-action model,” _arXiv preprint arXiv:2510.10975_ , 2025. 

- [52] Q. Chen, J. Yu, M. Schwager, P. Abbeel, Y. Shentu, and P. Wu, “Sarm: Stage-aware reward modeling for long horizon robot manipulation,” _arXiv preprint arXiv:2509.25358_ , 2025. 

- [53] C. Xu, Q. Li, J. Luo, and S. Levine, “Rldg: Robotic generalist policy distillation via reinforcement learning,” _arXiv preprint arXiv:2412.09858_ , 2024. 

- [54] G. Lu, R. Zhao, H. Lin, H. Zhang, and Y. Tang, “Human-in-theloop online rejection sampling for robotic manipulation,” _arXiv preprint arXiv:2510.26406_ , 2025. 

