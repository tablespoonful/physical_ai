---
title: "Drive My Way: Preference Alignment of Vision-Language-Action Model for Personalized Driving"
date: "2026-03-26"
authors: "Zehao Wang; Huaide Jiang; Shuaiwu Dong; Yuping Wang; Hang Qiu; Jiachen Li"
venue: "CVPR 2026"
url: https://arxiv.org/abs/2603.25740
pdf: https://arxiv.org/pdf/2603.25740
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.25740)** / [論文ページ](https://arxiv.org/abs/2603.25740)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 


# **Drive My Way: Preference Alignment of Vision-Language-Action Model for Personalized Driving** 

Zehao Wang<sup>1</sup> , Huaide Jiang<sup>1</sup> , Shuaiwu Dong<sup>1</sup> , Yuping Wang<sup>1</sup><sup>_,_2</sup> , Hang Qiu<sup>1</sup> , Jiachen Li<sup>1</sup><sup>_,†_</sup> 1University of California, Riverside 2University of Michigan 

## **Abstract** 

_Human driving behavior is inherently personal, which is shaped by long-term habits and influenced by short-term intentions. Individuals differ in how they accelerate, brake, merge, yield, and overtake across diverse situations. However, existing end-to-end autonomous driving systems either optimize for generic objectives or rely on fixed driving modes, lacking the ability to adapt to individual preferences or interpret natural language intent. To address this gap, we propose Drive My Way (DMW), a personalized VisionLanguage-Action (VLA) driving framework that aligns with users’ long-term driving habits and adapts to real-time user instructions. DMW learns a user embedding from our personalized driving dataset collected across multiple real drivers and conditions the policy on this embedding during planning, while natural language instructions provide additional short-term guidance. Closed-loop evaluation on the Bench2Drive benchmark demonstrates that DMW improves style instruction adaptation, and user studies show that its generated behaviors are recognizable as each driver’s own style, highlighting personalization as a key capability for human-centered autonomous driving. Our data and code are available at https://dmw-cvpr.github.io/._ 

## **1. Introduction** 

End-to-end autonomous driving has emerged as a powerful paradigm that directly learns to map raw multi-modal sensor inputs to driving trajectories or control actions [1–4]. Recent advances in unified architectures and foundationmodel-based frameworks have demonstrated impressive performance in open-loop benchmarks through imitation of expert trajectories [5–7]. However, these systems often optimize for generic safety and efficiency objectives, overlooking the _individuality_ and _context-dependent nature_ of human driving behaviors. In practice, driving is inherently personal; individuals differ in how assertively they accelerate, brake, or overtake depending on the situation, pur- 

> _†_ Corresponding author. 

> zehao.wang1@email.ucr.edu, jiachen.li@ucr.edu 


Figure 1. Drive My Way (DMW) achieves end-to-end personalized driving via both long-term preference alignment and shortterm style instruction adaptation. 

pose, or emotional state (e.g., commuting, leisure, or emergency travel). Existing autonomous driving systems typically provide only a few preset modes (e.g., “sport”, “comfort”, or “eco”) or manual parameter adjustments, which fail to capture subtle and evolving passenger preferences [8– 10]. More importantly, such rigid presets cannot interpret intuitive, natural language instructions, such as “I’m tired” or “I’m late for work”. Therefore, achieving _long-term, context-adaptive personalization_ is crucial for enhancing user trust, comfort, and satisfaction [11, 12]. 

Existing research on personalized autonomous driving mainly falls into two categories. First, data-driven methods extract predefined driving styles from human demonstrations and learn style-conditioned policies using behavior cloning or inverse reinforcement learning (IRL) [11, 13]. While effective at mimicking human-like styles, these approaches require diverse large-scale datasets and scale poorly to a growing population of users with heterogeneous preferences. Surmann et al. [14] mitigate this limitation through multi-objective reinforcement learning, enabling runtime adjustment of preference weights. However, such methods cannot handle real-time human interaction via natural language or adapt to user instructions on the fly. Sec- 

25204 

ond, language-driven approaches leverage large language models (LLMs) for instruction-based personalization [15]. For example, Talk2Drive [16] employs GPT-4 to interpret passenger commands and generate high-level driving decisions, reducing takeover rates in simplified intersection and parking scenarios involving limited traffic participants. Despite promising results, existing language-based methods remain constrained to simple, low-interaction settings. They have not been systematically investigated in complex, dynamic driving contexts, such as merging, overtaking, or emergency braking, where trade-offs among safety, comfort, and efficiency must adapt to dynamic scenes. Fully leveraging the reasoning and generalization capabilities of foundation models for such context-aware adaptations remains largely unexplored. Additionally, current personalization methods based on LLMs [16] or vision-language models (VLMs) [17] do not consider a driver’s _long-term habits_ or cumulative experiences, which are diverse and continuously evolving. 

To address these issues, we propose DMW, a novel Vision-Language-Action (VLA) framework that integrates visual observations, contextual user profiles, and real-time natural language instructions to generate adaptive, personalized driving actions, as shown in Fig. 1. DMW learns user embeddings that encode long-term driving behaviors from a newly collected personalized driving dataset comprising profiles, trajectories, and privileged information from thirty drivers across twenty realistic scenarios in CARLA [18]. To enable human interaction and real-time adaptation, we further apply reinforcement fine-tuning to the driving policy using rewards derived from safety, comfort, and efficiency objectives, whose weights are dynamically adjusted. Extensive closed-loop experiments on Bench2Drive [19] show that DMW effectively adapts to different style instructions while maintaining safety. Further user studies demonstrate that its driving behavior aligns with individual user preferences and expresses distinct driving behaviors. 

Our main contributions are summarized as follows: 

- We propose DMW, a novel personalized end-to-end autonomous driving framework that integrates contextual user embeddings to align policy behaviors with individual driving preferences. DMW also enables real-time human interaction and adaptability through reinforcement finetuning conditioned on natural language instructions. 

- We construct the first multi-modal personalized driving dataset (PDD) collected from thirty real drivers across diverse traffic scenarios in CARLA, which provides a valuable dataset for developing and evaluating humancentered driving models. 

- We conduct extensive evaluations on the Bench2Drive benchmark [19], complemented by personalization metrics and user studies, which demonstrate the effectiveness of DMW in adapting its driving behavior to individual user preferences while maintaining a balanced trade-off among safety, efficiency, and comfort. 

## **2. Related Work** 

**Foundation Models for Autonomous Driving.** Existing end-to-end autonomous driving models [20–22] still struggle in closed-loop benchmarks [23, 24] due to reliance on imitation learning and limited generalization [25, 26]. Foundation models (LLMs, VLMs) have recently emerged [27–36] and existing work (e.g., DriveVLM [37], GPTDriver [38], AlphaDrive [39]) leverages their world knowledge and semantic reasoning to interpret complex traffic scenarios, producing high-level decisions and language rationales for their actions. In parallel, VLA models have demonstrated the ability to directly translate raw sensory inputs and linguistic instructions into fine-grained actions [40, 41] or low-level control signals through action tokens [22] or action decoders [42]. While these approaches have made substantial progress toward language-conditioned driving, their capacity for personalization and adaptation to individual driving preferences remains largely underexplored. 

**Personalization in Autonomous Driving.** The pursuit of personalized autonomous driving remains an active area of research, with the key challenge lying in aligning individual driving preferences. Recent studies like [11] learn styleconditioned driving policies, but overlook fine-grained individual differences. MAVERIC [43] explores the learning of a latent space of diverse and socially-aware driving behaviors, offering greater flexibility compared to predefined style categories. Meanwhile, LLMs have enabled more intuitive human-vehicle interaction [8, 15, 17, 44], allowing systems to respond to personalized commands in real time. Recent works [16] leverage memory modules based on retrieval-augmented generation (RAG) to personalize decisions by retrieving user-specific context. However, these approaches rely on explicit human feedback and accurate retrieval, producing contexts that are largely descriptive rather than behavioral and fail to capture implicit, long-term driving tendencies. Moreover, most of them are evaluated only in open-loop settings, making it difficult to assess how well personalization transfers to closed-loop decision making and influences real-time driving behavior. 

## **3. Personalized Driving Dataset** 

To learn and evaluate personalized driving policies, we construct a new **Personalized Driving Dataset (PDD)** , as illustrated in Fig. 2. PDD captures the driving environments and the personal context of human drivers across diverse, highly interactive, safety-critical driving situations. Unlike prior datasets that rely on synthetic instruction-action pairs with limited behavioral variation [45] or those that infer style labels retrospectively using coarse VLM-based reasoning or heuristic labeling [11], our dataset records human driving behaviors during complex real-time interactions, which allows us to study how different individuals make decisions when faced with similar situations. 

We recruit thirty drivers with diverse backgrounds and 

25205 


Figure 2. An overview of the Personal Driving Dataset, which consists of the driving data and structured driver profile data. 

levels of driving experience. Before data collection, each participant completes a structured questionnaire covering demographic information, driving history, and typical driving purposes such as commuting or leisure travel. These profiles provide a semantic context that connects personal background with long-term driving habits. Each participant then performs a standardized set of twenty driving scenarios in the CARLA, spanning four scenario types, including overtaking, merging into traffic, handling intersections, and navigating pedestrian crossings or encountering vehicle cut-ins. All drivers operate the vehicle using a Logitech G-series steering wheel and pedal setup to enable naturalistic control inputs. PDD records ego-vehicle motion states, scene perception of surrounding vehicles, pedestrians, cyclists, and roadside hazards, as well as traffic context such as signal states, stop signs, route geometry, and speed limits. To support comparison across drivers and scenarios, we record an expert target speed using PDM-Lite [46]; the deviation between human-driven speed and this target serves as a dense descriptor of behavioral style under varying conditions. Overall, PDD offers a rich and behavior-sensitive foundation for modeling personalized driving, which supports preference-conditioned policy learning. 

## **4. Problem Formulation** 

We aim to learn a personalized driving policy that aligns with a driver’s long-term driving behavior while adapting to real-time preference instructions. Let _M_ = _{_ 1 _, . . . , M }_ denote the set of drivers, where _M_ is the number of drivers. For each driver _m ∈M_ , the collected driving dataset is _D_<sup>_m_</sup> = �( _s_<sup>_m_</sup> _t_<sup>_, am_</sup> _t_<sup>)</sup> � _Tt_ =1<sup>_m_, where</sup><sup>_s_</sup> _t_<sup>_m_and</sup><sup>_am_</sup> _t_<sup>denote the envi-</sup> ronmental state and the executed action of driver _m_ at time step _t_ , and _T_<sup>_m_</sup> is the trajectory length. The user profile obtained is _P_<sup>_m_</sup> , which summarizes the driver’s background, habits, and driving experience. The complete dataset across all drivers is _D_ =<sup>�</sup> _m∈M_<sup>_Dm._</sup> 

We formalize personalized driving as a Markov Decision Process (MDP), defined by the tuple ( _S, A, O, T , R, γ_ ). _S_ represents the state space, which includes environmental information. _A ⊂_ R<sup>3</sup> is the continuous action space consist- 

ing of throttle, brake, and steering. At time _t_ , the agent observes _ot_ = ( **I** _t,_ **q** _t, It, gt, P_<sup>_m_</sup> ) _∈O_ , where **I** _t ∈_ R<sup>_H×W ×_3</sup> is the front-view image, **q** _t_ is the ego-vehicle state, _It_ is a language instruction expressing short-term preference (e.g., “I’m in a rush”), _gt_ is the navigation target (e.g., route waypoints), and _P_<sup>_m_</sup> identifies the context of the active driver. _T_ denotes the transition in the environment. _R_ is the reward function that evaluates the action. _γ_ is the discount factor. 

The objective is to learn a driving policy _πθ_ ( _at | ot_ ) that maximizes the expected cumulative discounted reward: max _θ_ E _πθ t_ =0<sup>_γtR_(</sup><sup>_st, at_)</sup> _._ To achieve person�� _T_ � alization, the policy must infer the driver’s long-term behavioral tendencies from their historical driving data _D_<sup>_m_</sup> and relate these behaviors to their profile _P_<sup>_m_</sup> . During execution, the policy adapts its decisions based on the specified user embedding _zp_<sup>_m_, which is encoded from the driver’s</sup> profile _P_<sup>_m_</sup> , and the current instruction _It_ , ensuring safe and effective driving behavior that reflects each driver’s characteristic style and situational preferences. 

## **5. Method** 

We focus on personalized adaptation of driving policies to accommodate different users and their short-term driving preferences. The overall diagram of DMW is provided in Fig. 3. Given the camera observations and navigation goals, the model fuses the driver’s long-term preference with user instructions to produce adaptive, personalized actions. 

### **5.1. VLA Backbone** 

We employ SimLingo [42] as our VLA backbone due to its ability to perform language grounding and planning. SimLingo is built on InternVL2-1B [47, 48], which integrates the InternViT-300M-448px vision encoder with the Qwen2-0.5B language model, offering computational efficiency compared to larger alternatives [49]. Supervised by privileged expert demonstrations from PDM-Lite [46] and auxiliary reasoning signals, the backbone predicts temporal and geometric waypoints, which are then converted into target speed and steering commands. 

### **5.2. Personalization via Reinforcement Fine-tuning** 

Despite the strong planning capability of the VLA backbone, imitation learning alone tends to capture generalized behaviors rather than user-specific driving styles. We employ the Group Relative Policy Optimization (GRPO) to further finetune the personalization ability [50]. By sampling a group of outputs and computing normalized group advantages, GRPO inherently promotes policy specialization. To generate a rich set of candidate actions for the GRPO policy update, we introduce a residual decoder. As shown in Fig. 3, learnable _residual query_ tokens are integrated into the language model along with vision, language, navigation, user embedding, and motion query tokens. The resulting residual features are decoded by an MLP followed 

25206 


Figure 3. An overview of the DMW framework with a pretrained VLA backbone. The model takes in front-view camera images, instructions, route target points, and user profile as inputs, while the motion predictor outputs route and speed waypoints, which derive the base action (throttle, steer angle). The residual decoder outputs a discrete residual applied to the base to produce the final personalized action. 

by a categorical action head to produce two discrete residual adjustments: (i) speed change and (ii) steering change. 

The combined action is then passed through a PID controller to produce the final _at_ = _a_<sup>base</sup> _t_ + _a_<sup>∆</sup> _t_<sup>,where</sup><sup>_a_base</sup> _t_ is derived from the predicted waypoints and _a_<sup>∆</sup> _t_<sup>is the per-</sup> sonalized residual. This design allows the policy to preserve safe planning while adapting expressively to different drivers and situational intentions among multiple feasible planning trajectories (i.e., different choices of action). 

### **5.3. Long-term Preference Learning and Alignment** 

**User Embedding Learning.** To model the underlying driving style of different users and align VLA with personalized preferences, we introduce a long-term preference encoder that learns user embeddings from profile. To relate the semantic profile context with corresponding driving behavior, we adopt a contrastive learning mechanism [51] to learn a shared latent space _Z_ . As illustrated in Fig. 4, the longterm preference encoder _fp_ ( _·_ ) takes a profile _P_<sup>_m_</sup> of driver _m_ from the total set of drivers _M_ and outputs a user embedding _zp_<sup>_m∈Z_.</sup><sup>_fp_(</sup><sup>_·_) includes a DeBERTaV3 [52] text pro-</sup> cessor followed by a projection head. The route processor _fb_ ( _·_ ) is a temporal encoder with multi-head self-attention that processes a past trajectory window of length _k_ at the current timestep _t_ , _ξt_<sup>_m_</sup> = _{_ ( **I**<sup>_m_</sup> _t−k_ : _t_<sup>_,_</sup><sup>**q**</sup><sup>_m_</sup> _t−k_ : _t_<sup>_, am_</sup> _t−k_ : _t_<sup>)</sup><sup>_}_,which</sup> consists of sequential front-view camera images **I**<sup>_m_</sup> _t−k_ : _t_<sup>, ego-</sup> vehicle states **q**<sup>_m_</sup> _t−k_ : _t_<sup>anddriver’sactions</sup><sup>_am_</sup> _t−k_ : _t_<sup>from</sup><sup>_Dm_</sup> in PDD. This outputs a behavior embedding _zb,t_<sup>_m∈Z_that</sup> summarizes the driver’s actual driving tendencies. To align the embeddings from the two encoders, we employ the InfoNCE [51] contrastive objective that encourages _zp_<sup>_m_and</sup> _zb,t_<sup>_m_from the same driver to be close while pushing embed-</sup> dings from different drivers apart: 


where _zp_<sup>_j_is the user embedding of all other drivers, sim(</sup><sup>_·, ·_)</sup> denotes the cosine similarity and _τ_ is the temperature. **Preference Alignment.** After obtaining the user embedding _zp_<sup>_m_,weconditiontheVLApolicyonthisembedding</sup> and further adapt it through reinforcement fine-tuning. The user embedding acts as a latent personalization prior, guiding the policy toward decision patterns consistent with the driver’s characteristic style. 

To align the policy with individual driving preferences while enhancing behavioral diversity, for each target driver _m_ , we augment trajectories by conditioning the user embedding on both their own and another driver’s data _u ∈ M, u̸_ = _m_ . We want driver _m_ and driver _u_ to behave differently in order to effectively distinguish different drivers, so for a given driver _m_ , we always select _u_ who has the least similarity with _m_ regarding user embedding: _u_ = arg min _x∈M_ sim( _zp_<sup>_m, z_</sup> _p_<sup>_x_).The augmented action ˜</sup><sup>_a_</sup> _t_<sup>_m_is es-</sup> timated by scaling the original human action _a_<sup>_m_</sup> _t_<sup>according</sup> to the ratio of their route-level action statistics, which capture each driver’s action variability. Let the route-level average action of driver _m_ and _u_ be ¯ _a_<sup>_m_</sup> and ¯ _a_<sup>_u_</sup> respectively, then we calculate the augmented action as: _a_ ˜<sup>_m_</sup> _t_<sup>=</sup><sup>_<u>a</u>_¯</sup> _a_ ¯<sup>_mu· a_</sup> _t_<sup>_m_.The</sup> reward is then formulated as a behavioral similarity between the model’s sampled action and the reference or augmented action. When the policy is conditioned on the target profile _P_<sup>_m_</sup> : _R_ ( _s_<sup>_m_</sup> _t_<sup>_, at_)=</sup><sup>_d_(</sup><sup>_at, am_</sup> _t_<sup>).Whenconditionedon</sup><sup>_P u_:</sup> _R_ ( _s_<sup>_m_</sup> _t_<sup>_, at_)=</sup><sup>_d_(</sup><sup>_at,_˜</sup><sup>_am_</sup> _t_<sup>),where</sup><sup>_d_(</sup><sup>_·_) measures similarity in</sup> action space, encouraging the policy to adapt decisions to each user embedding while learning a smooth manifold of diverse driving styles. 

### **5.4. Human-Vehicle Personalized Interaction** 

**Style Instruction.** In complex and dynamically evolving traffic scenarios, effective personalization requires the autonomous agent to infer not only the long-term driving preference but also the context-adaptive preferences that vary across situations. To capture these nuances, we construct a 

25207 


Figure 4. The contrastive learning mechanism on the long-term preference encoder and route processor. 

style instruction set spanning twenty distinct driving scenarios. These instructions incorporate style intent and scenespecific semantics. Each scenario includes nine stylistic instructions that cover three driving styles expressed at three levels of directness, following the degrees of implicitness defined in prior work [16]. This design enables the model to interpret both explicit commands and subtle linguistic cues that reflect real-time user intent across diverse contexts, thereby achieving context-aware adaptation. 

**Style-Aware Reward Adaptation.** To translate user intents into safe and personalized objectives, we design a reward function that integrates driving performance metrics with instruction-dependent style alignment. The overall driving reward is formulated as a weighted combination of safety, efficiency, and comfort terms: 

_R_ ( _st, at_ ) = _ws · R_ safety + _we · R_ efficiency + _wc · R_ comfort _,_ (2) 

where _ws_ , _we_ , and _wc_ are importance weights, and _R_ safety, _R_ efficiency, and _R_ comfort denote the corresponding components. The safety reward penalizes risky interactions based on Time-to-Collision (TTC): _R_ safety = Isafety�TTC _t ≥ β_ safety�, where Isafety is the binary indicator enforces a minimum instruction-dependent safety threshold _β_ safety. The efficiency reward encourages maintaining a speed consistent with the desired style: _R_ efficiency = exp( _−α · |vt − v_ pref _|_ ), where _vt_ is the actual speed derived from action _at_ , _v_ pref is the instruction-dependent preferred speed, and _α_ is a penalty coefficient controlling sensitivity to deviation. The comfort reward evaluates whether _at_ remains within smoothness limits: _R_ comfort = Icomf� _a_<sup>steer</sup> _t | < β_ lat and _|a_<sup>acceleration</sup> _t | < β_ long�, where Icomf is a binary indicator, _β_ lat and _β_ long are instruction-dependent lateral and longitudinal comfort thresholds, respectively. 

To encourage personalized interaction with the user and 


Figure 5. The fine-tuning process and reward generation for shortterm instruction alignment. 

adapt to real-time preferences, we map the reward parameters based on both the instruction and the driving context. Specifically, for each style command _It_ , and scenario description, this mapping produces a set of weights ( _ws, we, wc_ ), a TTC threshold _β_ safety, a desired speed _v_ pref, and comfort thresholds _β_ lat, _β_ long. Instructions associated with an aggressive style correspond to a higher _we_ and _v_ pref to prioritize efficiency over other metrics. This formulation provides a more distinct optimization objective for each style rather than relying on a generic combination. 

To enable scalable and reliable weight adjustment, we employ a multi-stage approach illustrated in Fig. 5. First, we leverage the reasoning capabilities of advanced LLMs (e.g., GPT-5) to infer reward weights and thresholds from the scenario description and the instruction with a style _S ∈{_ Conservative _,_ Neutral _,_ Aggressive _}_ , and the inferred parameters are initialized within predefined upper bounds for each style to maintain balanced trade-offs among metrics. Second, the generated parameters are refined through expert review to ensure that the final reward functions reflect the intended command semantics while preserving safe driving behaviors across diverse traffic conditions. This adaptation bridges the gap between subtle preferences in language and dynamic style rewards. 

## **6. Experiments** 

We conduct extensive closed-loop experiments to validate the effectiveness of the DMW framework in both user alignment and instruction preference adaptation. Our evaluation is designed to answer three key research questions: 

- **RQ1: Long-term Driving Alignment.** Can our policy align with specific driving behavior when conditioned on 

25208 

Table 1. **Bench2Drive closed-loop driving metrics with different style instructions.** We compare SimLingo and StyleDrive under different style instructions with our policy fine-tuning with fixed rewards weights (DMW-Vanilla) and style-aware rewards weights ( **DMW** ). 

|**Method**|Style|DS|SR|Efficiency|Comfort|Speed|Acceleration|LC|Headway|TT|
|---|---|---|---|---|---|---|---|---|---|---|
|SimLingo [42]|Aggressive|78.56|65.83|247.60|18.61|7.66|5.39|0.75|25.99|25.35|
||Neutral|78.15|65.85|241.44|24.67|7.37|5.22|0.75|27.81|31.41|
||Conservative|78.18|65.56|238.77|26.99|7.21|5.29|0.70|29.12|33.02|
|StyleDrive [11]|Aggressive|75.68|60.89|256.71|16.79|7.23|5.59|0.74|24.95|27.76|
||Neutral|76.26|62.13|249.07|21.35|6.98|5.43|0.66|23.62|29.12|
||Conservative|77.02|61.96|242.18|23.67|6.82|5.39|0.70|27.19|29.98|
|DMW-Vanilla|Aggressive|82.19|70.97|253.10|15.86|**7.86**|5.29|**0.78**|26.46|19.69|
||Neutral|81.96|70.63|247.77|19.21|7.66|5.17|0.77|26.63|23.16|
||Conservative|81.48|71.05|246.80|21.87|7.75|5.37|0.75|26.90|22.51|
|**DMW**|Aggressive|79.50|67.36|**281.56**|21.62|7.72|**6.01**|0.70|26.37|26.93|
||Neutral|82.03|70.95|244.98|28.67|6.34|5.43|0.61|27.60|40.75|
||Conservative|**82.72**|**71.56**|237.06|**34.62**|6.18|5.26|0.60|**30.05**|**47.38**|


learned user embeddings? 

- **RQ2: Short-term Instruction Adaptation.** How well does the policy align with various styles of real-time language commands under different scenarios? 

- **RQ3: Driving Performance.** Does the introduction of personalization maintain or compromise driving performance, particularly regarding safety and success rate in complex scenarios? 

### **6.1. Experimental Setup** 

**Implementation Details.** For user embedding learning, both the long-term preference encoder and the route processor are trained using the AdamW optimizer [53] with a weight decay of 1e-3 and a learning rate of 1e-4. After convergence, the long-term preference encoder is frozen, and we fine-tune the full motion predictor and residual decoder while adopting the LoRA adapter [54] for parameterefficient adaptation of Qwen2-0.5B [49]. The full model is trained on eight NVIDIA RTX A6000 GPUs with a perGPU batch size of 8. For GRPO, we generate 4 responses per input for policy gradient updates. 

**Scenarios and Baselines.** We evaluate closed-loop performance using Bench2Drive [19]. Unlike the original evaluation, which continues the episode after a collision, we terminate the route immediately once a collision occurs to emphasize the safety-critical assessment. To validate the effect of personalization, we compare DMW with SimLingo [42] under various styles of instruction, focusing on whether the model can effectively adjust its driving tendency according to user-specific preferences. Additionally, to strengthen comparisons with prior personalization-focused work, we implement a StyleDrive-like [11] baseline by mapping each instruction to a style condition (i.e., Aggressive, Neutral, Conservative) and injecting it into the policy. Meanwhile, we adopt MORL-PD [14] as a baseline since it conditions the policy on a preference vector (speed/comfort) at runtime to modulate behavior. By deriving a per-user preference vector from driving metrics of test drivers and conditioning 

a multi-objective RL (MORL) policy, we compare it with DMW for long-term preference alignment. 

**Evaluation Metrics.** We employ metrics that assess both driving performance and stylistic alignment. The Driving Score (DS), Success Rate (SR), Efficiency (Effic.), and Comfort are adopted from Bench2Drive [19]. To quantify the personalization of the model, we measure the mean value of driving metrics, including average Speed in m _/_ s, Acceleration (Acce.) in m _/_ s<sup>2</sup> , Lane Change Counts (LC), Headway in m, and Travel Time (TT) in s. We introduce the Alignment Score (AS) for user studies to evaluate how well the policy aligns with individual driving preferences. **User Study for Long-Term Preference Alignment.** To test whether the driving behaviors of DMW align with each driver’s preference. We introduce an Alignment Score (AS) by first clustering all drivers using their historical logs, then generating roll-outs condition on each driver’s profile, and finally calculating the accuracy across test routes where roll-out is correctly classified into their target cluster. Additionally, we recruit ten evaluators and ask them to rate the similarity of the driver’s own logs and corresponding model roll-outs on a 1-10 scale. To test the zero-shot generalizability of DMW, we perform preference alignment on 25 drivers from PDD and evaluate the behavior alignment on both 25 in-distribution (ID) and 5 out-of-distribution (OOD) drivers. For each scenario type, we choose three test routes. 

### **6.2. Main Results** 

**Adaptation to Style Instruction.** Table 1 presents the closed-loop evaluation results on the Bench2Drive. The results show that fine-tuning alone already improves both SR and DS, likely due to the newly introduced safety reward. Furthermore, when conditioned on conservative instructions, DMW achieves the greatest gains in DS and SR while maintaining comparable efficiency, reflecting improved reliability in cautious driving. Under the aggressive instructions, our policy yields a substantial efficiency gain of 18.77% compared to the 3.70% in SimLingo, and 6.00% 

25209 

Table 2. **Driving metrics with and without style instructions, for each driver profile with a different long-term preference. Note that for Alignment Score (AS) and Ratings, we compute their value regardless of the style since it only measures long-term alignment.** 

|**Driver**|**Scenario**|**Style**|DS|Speed|Efficiency|Acceleration|Headway|AS|Ratings|
|---|---|---|---|---|---|---|---|---|---|
|D1||None|95.10→84.02|8.06→9.58|150.94→167.12|6.31→6.39|18.94→17.11|1.00|8.8|
|D2|Emergency|_↓_|98.64→96.71|4.61→4.97|96.02→99.21|4.94→5.35|23.10→21.18|0.67|8.3|
|D3|Brake|Ai|97.88→95.93|5.39→6.34|109.83→121.06|5.63→6.16|21.61→19.22|1.00|8.0|
|D4||ggressve|94.02→93.15|7.76→8.35|145.22→159.56|6.03→6.92|21.03→18.19|0.67|7.8|
|D1||None|90.05→94.38|9.32→8.76|270.84→260.10|5.15→4.68|96.44→101.16|0.67|8.4|
|D2||_↓_|86.94→91.72|6.37→5.76|196.82→175.31|4.29→4.16|118.92→121.03|1.00|8.1|
|D3|Merging||96.85→95.94|6.98→6.20|205.41→195.77|4.46→4.24|111.26→114.05|0.67|7.6|
|D4||Conservative|97.31→97.88|8.78→8.63|261.52→259.52|5.01→4.91|88.76→100.93|1.00|8.2|
|D1||None|97.56→97.94|7.70→7.94|220.19→223.13|7.28→7.37|14.69→14.53|1.00|9.0|
|D2||_↓_|98.23→98.41|5.50→5.56|167.40→167.80|5.65→5.78|22.23→22.04|1.00|8.6|
|D3|Overtaking|Nl|97.14→96.62|6.34→6.13|191.02→183.84|6.18→6.01|20.79→22.19|0.67|7.5|
|D4||eutra|80.61→82.19|9.63→9.51|271.98→265.84|7.11→6.82|17.81→18.03|1.00|8.1|
|D1||None|90.82→96.67|9.08→8.49|408.74→401.28|7.12→6.37|31.44→32.52|1.00|8.7|
|D2|Traffic|_↓_|97.92→98.35|5.79→4.91|193.26→183.11|5.72→5.51|35.02→36.91|1.00|8.2|
|D3|Sign|Ci|89.31→92.02|6.88→5.37|237.05→231.46|5.96→5.91|34.54→36.51|1.00|8.1|
|D4||onservatve|95.91→97.32|8.91→6.74|418.02→379.68|6.54→5.81|31.19→31.77|0.67|7.9|


in StyleDrive, with only a 3.89% reduction in DS relative to the conservative condition. DMW significantly outperforms SimLingo in style adaptation, which highlights that DMW accurately captures the intended behaviors expressed by the instructions while preserving overall performance. Meanwhile, StyleDrive induces smaller metric shifts and achieves a lower DS than DMW, likely due to its fixed style condition, which further highlights the benefit of our stylesensitive adaptation. The consistent reduction in acceleration and lane-change counts under conservative ones further validates that DMW maintains distinct stylistic behaviors. 

To further illustrate the behavioral diversity induced by different instructions, Fig. 6 visualizes how our policy reacts under aggressive and conservative instructions in safety-critical scenarios. When facing a road blockage, the aggressive instruction prefers an immediate overtake (red speed curve). Conversely, the conservative command causes the agent to decelerate and either stop or maintain a low following speed until the opposite lane is clear (blue curve). This behavioral divergence arises from the styleaware weighting in our fine-tuning reward, which dynamically adjusts the balance between safety and efficiency according to the given instruction. In hard-braking scenarios, the agent tends to maintain a tighter following distance when objects appear ahead or merge into the lane under aggressive instructions, while the agent slows down and yields more noticeably when conditioned on conservative ones. This distinction is largely governed by the style-aware TTC threshold, which is adapted to be more permissive for aggressive ones and more restrictive for conservative ones, directly tuning the model’s safety margins. The complete driving clips are provided in the supplementary materials. 

**Long-term Preference Alignment.** We report metrics and user study results for two seen drivers (D1, D2) and two unseen drivers (D3, D4). Table 2 shows that the policy conditioned on each profile exhibits consistent motion statistics across different scenarios. For instance, Drivers 

Table 3. Long-term preference alignment. D: Driver ID. 

||**Al**|**ignme**|**nt Sco**|**re**|**Av**|**erage**|**Rati**|**ngs**|
|---|---|---|---|---|---|---|---|---|
|**Methods**|**I**|**D**|**OO**|**D**|**I**|**D**|**O**|**OD**|
||D1|D2|D3|D4|D1|D2|D3|D4|
|MORL-PD [14]<br>**DMW**|0.42<br>0.92|0.58<br>0.92|0.25<br>0.83|0.33<br>0.83|5.1<br>8.7|6.2<br>8.3|3.9<br>7.8|3.5<br>8.0|


1 and 4 exhibit higher efficiency and acceleration, reflecting a more aggressive driving preference, whereas Drivers 2 and 3 show lower acceleration and larger headway across all categories, indicating a preference that prioritizes safety and comfort. Furthermore, Driver 2 shows the most cautious style with the lowest acceleration, while Driver 3, though still conservative, exhibits slightly higher speeds and greater acceleration, suggesting a willingness to accelerate more readily in scenarios such as Overtaking and Traffic Sign. While each driver’s driving metrics vary across scenarios, the driving behavior remains distinct among the drivers, suggesting that the policy aligns with individual drivers’ long-term driving preferences across different scenarios. Furthermore, Table 3 shows higher AS and ratings for DMW, indicating that more roll-outs are classified into the target cluster where their driver belongs, and evaluators can consistently recognize driving behaviors that reflect the corresponding driver’s driving habits. While MORLPD also induces style shifts via its preference-weight conditioning, it achieves a lower alignment, especially on unseen drivers, which suggests that our user embedding better captures semantic context from the profile, leading to stronger generalization. 

In addition, consistent with Table 1, language style instructions can provide an additional adaptation, shifting the driving towards the short-term preference. 

### **6.3. Ablation Study** 

**Adaptive Average Pooling.** We ablate the masked Adaptive Average Pooling (AAP) module used in the preference 

25210 


Figure 6. Driving preference under aggressive and conservative instructions. Red waypoints denote distance parametrized (every 1 m) navigation path and green waypoints denote time parametrized (every 0 _._ 25 s) trajectory. 

Table 4. **Averaged driving metrics using long-term preference encoder with or without Adaptive Average Pooling (AAP).** 

|**Driver**|**Encoder**|DS|Speed|Effic.|Acce. Headway|AS|Ratings|
|---|---|---|---|---|---|---|---|
|D1||82.74|4.52|161.38|5.84<br>50.11|0.67|6.1|
|D2|/ AAP|88.02|4.21|163.07|5.88<br>47.56|0.58|5.9|
|D3|wo|87.65|4.49|133.12|5.81<br>41.63|0.25|4.6|
|D4||80.13|4.46|172.92|5.79<br>38.94|0.50|5.3|
|D1||93.38|8.54|262.68|6.46<br>40.38|0.92|8.7|
|D2|/ AAP|95.43|5.57|163.38|5.15<br>49.82|0.92|8.3|
|D3|w|95.30|6.40|185.83|5.56<br>47.05|0.83|7.8|
|D4||91.96|8.77|274.19|6.17<br>39.70|0.83|8.0|


encoder, which compresses textual profile features into a fixed-length sequence aligned with the temporal features of the route processor. Replacing this module with an unmasked global mean reduces the expressiveness of user embeddings. As shown in Table 4, driving policy conditioned on the user embeddings from the preference encoder with AAP yields a higher diversity of motion statistics across different user profiles. We also observe a higher AS, demonstrating that the model can more consistently reproduce each driver’s behavioral traits. We attribute the improvement to its ability to preserve semantically important embeddings while mitigating the bias from irrelevant segments. We also observe that in denser interaction scenarios, the policy may shift toward conservative behavior for safety, which can reduce style expressiveness for neutral drivers. **Style-aware Reward Adaptation.** We examine the effect of fixed versus style-aware adaptive reward weights on driving performance and behavioral diversity. The results are in Table 1. When the reward components are fixed (i.e., _ws_ = 0 _._ 35, _we_ = 0 _._ 35, _wc_ = 0 _._ 30), only the styledependent TTC and comfort thresholds remain to induce stylistic variation. DMW-Vanilla achieves higher overall 

DS and SR, indicating effective optimization of generic objectives. However, the inability of dynamic adaptation to efficiency and comfort weights causes aggressive and conservative instructions to exhibit similar driving, revealing a reduced sensitivity to style. In contrast, DMW adaptively adjusts reward weights and thresholds based on both context and instruction style, maintaining driving performance while producing clear behavioral distinctions. Aggressive instructions lead to higher speeds and shorter headways, whereas conservative ones favor smoother control and larger safety margins. This demonstrates the necessity of adaptive weighting to achieve both reliable and personalized driving behaviors. 

## **7. Conclusion** 

We introduced DMW, a personalized VLA driving framework that aligns long-term driver preferences and adapts to short-term style instructions. Through learning user embeddings from the curated Personalized Driving Dataset and conditioning on the end-to-end driving policy, our method captures and aligns with individual drivers’ behaviors. Extensive experiments on Bench2Drive demonstrate that DMW achieves more distinct adaptation than existing baselines. User studies further highlight the potential of personalized VLA systems to bridge the gap toward humancentered autonomous driving, enabling vehicles that adapt their behavior to individual user preferences. Our approach is currently validated within the CARLA simulator. Future work will focus on bridging the sim-to-real gap by deploying and evaluating the DMW framework on real vehicles. We also plan to expand our dataset to encompass a wider diversity of driving behaviors to enable more robust and generalizable preference alignment. 

25211 

## **Acknowledgment** 

We gratefully acknowledge Janice Nguyen, Shubham Derhgawen, Jonathan Setiabudi, Alexander Totah, Pranav Gowrishankar, and Pratheek Sunilkumar for their support in data collection. 

## **References** 

- [1] Sicong Jiang, Zilin Huang, Kangan Qian, Ziang Luo, Tianze Zhu, Yang Zhong, Yihong Tang, Menglin Kong, Yunlong Wang, Siwen Jiao, Hao Ye, Zihao Sheng, Xin Zhao, Tuopu Wen, Zheng Fu, Sikai Chen, Kun Jiang, Diange Yang, Seongjin Choi, and Lijun Sun. A survey on vision-languageaction models for autonomous driving. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV) Workshops_ , pages 4524–4536, October 2025. 1 

- [2] Litian Gong, Fatemeh Bahrani, Yutai Zhou, Amin Banayeeanzade, Jiachen Li, and Erdem Bıyık. Autofocus-il: Vlmbased saliency maps for data-efficient visual imitation learning without extra human annotations. In _International Conference on Robotics and Automation (ICRA)_ , 2026. 

- [3] Yuping Wang, Shuo Xing, Cui Can, Renjie Li, Hongyuan Hua, Kexin Tian, Zhaobin Mo, Xiangbo Gao, Keshu Wu, Sulong Zhou, et al. Generative ai for autonomous driving: Frontiers and opportunities. _arXiv preprint arXiv:2505.08854_ , 2025. 

- [4] Bernard Lange, Masha Itkina, Jiachen Li, and Mykel Kochenderfer. Self-supervised Multi-future Occupancy Forecasting for Autonomous Driving. In _Proceedings of Robotics: Science and Systems_ , 2025. 1 

- [5] Rui Zhao, Yuze Fan, Ziguo Chen, Fei Gao, and Zhenhai Gao. Diffe2e: Rethinking end-to-end driving with a hybrid diffusion-regression-classification policy. In _The ThirtyNinth Annual Conference on Neural Information Processing Systems_ , 2025. 1 

- [6] Jinning Li, Jiachen Li, Sangjae Bae, and David Isele. Adaptive prediction ensemble: Improving out-of-distribution generalization of motion forecasting. _IEEE Robotics and Automation Letters_ , 10(2):1553–1560, 2024. 

- [7] Maneekwan Toyungyernsub, Esen Yel, Jiachen Li, and Mykel J Kochenderfer. Predicting future spatiotemporal occupancy grids with semantics for autonomous driving. In _2024 IEEE Intelligent Vehicles Symposium (IV)_ , pages 2855– 2861. IEEE, 2024. 1 

- [8] Genghua Kou, Fan Jia, Weixin Mao, Yingfei Liu, Yucheng Zhao, Ziheng Zhang, Osamu Yoshie, Tiancai Wang, Ying Li, and Xiangyu Zhang. Padriver: Towards personalized autonomous driving. In _2025 International Joint Conference on Neural Networks (IJCNN)_ , pages 1–8, 2025. 1, 2 

- [9] Manabu Nakanoya, Junha Im, Hang Qiu, Sachin Katti, Marco Pavone, and Sandeep Chinchali. Personalized federated learning of driver prediction models for autonomous driving, 2021. 

- [10] Jiachen Li, David Isele, Kanghoon Lee, Jinkyoo Park, Kikuo Fujimura, and Mykel J Kochenderfer. Interactive autonomous navigation with internal state inference and interactivity estimation. _IEEE Transactions on Robotics_ , 40: 2932–2949, 2024. 1 

- [11] Ruiyang Hao, Bowen Jing, Haibao Yu, and Zaiqing Nie. Styledrive: Towards driving-style aware benchmarking of end-to-end autonomous driving. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , pages 4627– 4635, 2026. 1, 2, 6 

- [12] Udita Ghosh, Dripta S. Raychaudhuri, Jiachen Li, Konstantinos Karydis, and Amit K. Roy-Chowdhury. Reducing oracle feedback with vision-language embeddings for preferencebased rl. In _IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2026. 1 

- [13] Anqing Jiang, Yu Gao, Yiru Wang, Zhigang Sun, Shuo Wang, Yuwen Heng, Hao Sun, Shichen Tang, Lijuan Zhu, Jinhao Chai, et al. Irl-vla: Training an vision-languageaction policy via reward world model. _arXiv preprint arXiv:2508.06571_ , 2025. 1 

- [14] Hendrik Surmann, Jorge De Heuvel, and Maren Bennewitz. Multi-objective reinforcement learning for adaptable personalized autonomous driving. In _2025 European Conference on Mobile Robots (ECMR)_ , pages 1–8. IEEE, 2025. 1, 6, 7 

- [15] Yunsheng Ma, Can Cui, Xu Cao, Wenqian Ye, Peiran Liu, Juanwu Lu, Amr Abdelraouf, Rohit Gupta, Kyungtae Han, Aniket Bera, James M. Rehg, and Ziran Wang. Lampilot: An open benchmark dataset for autonomous driving with language model programs. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 15141– 15151, 2024. 2 

- [16] Can Cui, Zichong Yang, Yupeng Zhou, Yunsheng Ma, Juanwu Lu, Lingxi Li, Yaobin Chen, Jitesh Panchal, and Ziran Wang. Personalized autonomous driving with large language models: Field experiments. In _2024 IEEE 27th International Conference on Intelligent Transportation Systems (ITSC)_ , pages 20–27. IEEE, 2024. 2, 5 

- [17] Can Cui, Zichong Yang, Yupeng Zhou, Juntong Peng, SungYeon Park, Cong Zhang, Yunsheng Ma, Xu Cao, Wenqian Ye, Yiheng Feng, et al. On-board vision-language models for personalized autonomous vehicle motion control: System design and real-world validation. _arXiv preprint arXiv:2411.11913_ , 2024. 2 

- [18] Alexey Dosovitskiy, German Ros, Felipe Codevilla, Antonio Lopez, and Vladlen Koltun. CARLA: An open urban driving simulator. In _Proceedings of the 1st Annual Conference on Robot Learning_ , pages 1–16, 2017. 2 

- [19] Xiaosong Jia, Zhenjie Yang, Qifeng Li, Zhiyuan Zhang, and Junchi Yan. Bench2drive: Towards multi-ability benchmarking of closed-loop end-to-end autonomous driving. _Advances in Neural Information Processing Systems_ , 37:819– 844, 2024. 2, 6 

- [20] Xiaosong Jia, Yulu Gao, Li Chen, Junchi Yan, Patrick Langechuan Liu, and Hongyang Li. Driveadapter: Breaking the coupling barrier of perception and planning in end-to-end autonomous driving. In _ICCV_ , 2023. 2 

- [21] Xiaosong Jia, Penghao Wu, Li Chen, Jiangwei Xie, Conghui He, Junchi Yan, and Hongyang Li. Think twice before driving: Towards scalable decoders for end-to-end autonomous driving. In _CVPR_ , 2023. 

- [22] Zewei Zhou, Tianhui Cai, Seth Z. Zhao, Yun Zhang, Zhiyu Huang, Bolei Zhou, and Jiaqi Ma. Autovla: A visionlanguage-action model for end-to-end autonomous driving with adaptive reasoning and reinforcement fine-tuning. In 

25212 

_Advances in Neural Information Processing Systems_ , 2025. 2 

- [23] Carla autonomous driving leaderboard, 2025. 2 

- [24] Yuping Wang, Xiangyu Huang, Xiaokang Sun, Mingxuan Yan, Shuo Xing, Zhengzhong Tu, and Jiachen Li. Uniocc: A unified benchmark for occupancy forecasting and prediction in autonomous driving. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 25560– 25570, 2025. 2 

- [25] Haohan Chi, Huan-ang Gao, Ziming Liu, Jianing Liu, Chenyu Liu, Jinwei Li, Kaisen Yang, Yangcheng Yu, Zeda Wang, Wenyi Li, Leichen Wang, Xingtao Hu, Hao Sun, Hang Zhao, and Hao Zhao. Impromptu vla: Open weights and open data for driving vision-language-action models. In _Advances in Neural Information Processing Systems, Datasets and Benchmarks Track_ , 2025. 2 

- [26] Haohong Lin, Yunzhi Zhang, Wenhao Ding, Jiajun Wu, and Ding Zhao. Model-based policy adaptation for closed-loop end-to-end autonomous driving. In _Workshop on Foundation Models Meet Embodied Agents at CVPR 2025_ , 2025. 2 

- [27] Zhiwen Fan, Jian Zhang, Renjie Li, Junge Zhang, Runjin Chen, Hezhen Hu, Kevin Wang, Huaizhi Qu, Dilin Wang, Zhicheng Yan, et al. Vlm-3r: Vision-language models augmented with instruction-aligned 3d reconstruction. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2026. 2 

- [28] Yuan Gao, Mattia Piccinini, Yuchen Zhang, Dingrui Wang, Korbinian Moller, Roberto Brusnicki, Baha Zarrouki, Alessio Gambi, Jan Frederik Totz, Kai Storms, Steven Peters, Andrea Stocco, Bassam Alrifaee, Marco Pavone, and Johannes Betz. Foundation models in autonomous driving: A survey on scenario generation and scenario analysis. _IEEE Open Journal of Intelligent Transportation Systems_ , 2026. 

- [29] Piyush Gupta, Sangjae Bae, Jiachen Li, and David Isele. Scale-plan: Scalable language-enabled task planning for heterogeneous multi-robot teams. _arXiv preprint arXiv:2603.08814_ , 2026. 

- [30] Yunsong Zhou, Linyan Huang, Qingwen Bu, Jia Zeng, Tianyu Li, Hang Qiu, Hongzi Zhu, Minyi Guo, Yu Qiao, and Hongyang Li. Embodied understanding of driving scenarios. In _European Conference on Computer Vision_ , pages 129–148. Springer, 2024. 

- [31] Xiaopan Zhang, Zejin Wang, Zhixu Li, Jianpeng Yao, and Jiachen Li. Commcp: Efficient multi-agent coordination via llm-based communication with conformal prediction. In _IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2026. 

- [32] Mingxuan Yan, Yuping Wang, Zechun Liu, and Jiachen Li. Rdd: Retrieval-based demonstration decomposer for planner alignment in long-horizon tasks. In _Proceedings of the 39th Annual Conference on Neural Information Processing Systems (NeurIPS)_ , 2025. 

- [33] Xiaopan Zhang, Hao Qin, Fuquan Wang, Yue Dong, and Jiachen Li. Lamma-p: Generalizable multi-agent long-horizon task allocation and planning with lm-driven pddl planner. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 10221–10221. IEEE, 2025. 

- [34] Trishna Chakraborty, Udita Ghosh, Xiaopan Zhang, Fahim Faisal Niloy, Yue Dong, Jiachen Li, Amit RoyChowdhury, and Chengyu Song. Heal: An empirical study 

   - on hallucinations in embodied agents driven by large language models. In _Findings of the Association for Computational Linguistics: EMNLP 2025_ , pages 21226–21243, 2025. 

- [35] Sayak Nag, Udita Ghosh, Calvin-Khang Ta, Sarosij Bose, Jiachen Li, and Amit K Roy-Chowdhury. Conformal prediction and mllm aided uncertainty quantification in scene graph generation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 11676–11686, 2025. 

- [36] Zhikai Zhao, Chuanbo Hua, Federico Berto, Kanghoon Lee, Zihan Ma, Jiachen Li, and Jinkyoo Park. Trajevo: Trajectory prediction heuristics design via llm-driven evolution. In _Proceedings of the AAAI Conference on Artificial Intelligence (AAAI)_ , 2026. 2 

- [37] Xiaoyu Tian, Junru Gu, Bailin Li, Yicheng Liu, Yang Wang, Zhiyong Zhao, Kun Zhan, Peng Jia, XianPeng Lang, and Hang Zhao. Drivevlm: The convergence of autonomous driving and large vision-language models. In _Conference on Robot Learning_ , pages 4698–4726. PMLR, 2025. 2 

- [38] Jiageng Mao, Yuxi Qian, Junjie Ye, Hang Zhao, and Yue Wang. Gpt-driver: Learning to drive with gpt. _arXiv preprint arXiv:2310.01415_ , 2023. 2 

- [39] Bo Jiang, Shaoyu Chen, Qian Zhang, Wenyu Liu, and Xinggang Wang. Alphadrive: Unleashing the power of vlms in autonomous driving via reinforcement learning and reasoning. _arXiv preprint arXiv:2503.07608_ , 2025. 2 

- [40] Haoyu Fu, Diankun Zhang, Zongchuang Zhao, Jianfeng Cui, Dingkang Liang, Chong Zhang, Dingyuan Zhang, Hongwei Xie, Bing Wang, and Xiang Bai. Orion: A holistic end-toend autonomous driving framework by vision-language instructed action generation. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , pages 24823–24834, October 2025. 2 

- [41] Shuang Zeng, Xinyuan Chang, Mengwei Xie, Xinran Liu, Yifan Bai, Zheng Pan, Mu Xu, and Xing Wei. Futuresightdrive: Thinking visually with spatio-temporal cot for autonomous driving. In _Advances in Neural Information Processing Systems_ , 2025. 2 

- [42] Katrin Renz, Long Chen, Elahe Arani, and Oleg Sinavski. Simlingo: Vision-only closed-loop autonomous driving with language-action alignment. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 11993– 12003, 2025. 2, 3, 6, 1 

- [43] Mariah L Schrum, Emily Sumner, Matthew C Gombolay, and Andrew Best. Maveric: A data-driven approach to personalized autonomous driving. _IEEE Transactions on Robotics_ , 40:1952–1965, 2024. 2 

- [44] Xu Han, Xianda Chen, Zhenghan Cai, Pinlong Cai, Meixin Zhu, and Xiaowen Chu. From words to wheels: Automated style-customized policy generation for autonomous driving. _arXiv preprint arXiv:2409.11694_ , 2024. 2 

- [45] Ziye Qin, Siyan Li, Chuheng Wei, Guoyuan Wu, Matthew J Barth, Amr Abdelraouf, Rohit Gupta, and Kyungtae Han. Investigating personalized driving behaviors in dilemma zones: Analysis and prediction of stop-or-go decisions. _IEEE Robotics and Automation Letters_ , 2025. 2 

- [46] Chonghao Sima, Katrin Renz, Kashyap Chitta, Li Chen, Hanxue Zhang, Chengen Xie, Jens Beißwenger, Ping Luo, Andreas Geiger, and Hongyang Li. Drivelm: Driving with 

25213 

graph visual question answering. In _European Conference on Computer Vision_ , 2024. 3 

- [47] Zhe Chen, Weiyun Wang, Hao Tian, Shenglong Ye, Zhangwei Gao, Erfei Cui, Wenwen Tong, Kongzhi Hu, Jiapeng Luo, Zheng Ma, et al. How far are we to gpt-4v? closing the gap to commercial multimodal models with open-source suites. _Science China Information Sciences_ , 67(12):220101, 2024. 3 

- [48] Zhe Chen, Jiannan Wu, Wenhai Wang, Weijie Su, Guo Chen, Sen Xing, Muyan Zhong, Qinglong Zhang, Xizhou Zhu, Lewei Lu, et al. Internvl: Scaling up vision foundation models and aligning for generic visual-linguistic tasks. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 24185–24198, 2024. 3 

- [49] An Yang, Baosong Yang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Zhou, Chengpeng Li, Chengyuan Li, Dayiheng Liu, Fei Huang, et al. Qwen2 technical report. _eprint arXiv: 2407.10671_ , 2024. 3, 6 

- [50] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, YK Li, Yang Wu, et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. _arXiv preprint arXiv:2402.03300_ , 2024. 3 

- [51] Aaron van den Oord, Yazhe Li, and Oriol Vinyals. Representation learning with contrastive predictive coding. _arXiv preprint arXiv:1807.03748_ , 2018. 4 

- [52] Pengcheng He, Jianfeng Gao, and Weizhu Chen. DeBERTav3: Improving deBERTa using ELECTRA-style pretraining with gradient-disentangled embedding sharing. In _The Eleventh International Conference on Learning Representations_ , 2023. 4 

- [53] Ilya Loshchilov and Frank Hutter. Decoupled weight decay regularization. In _International Conference on Learning Representations (ICLR)_ , 2019. 6 

- [54] Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan AllenZhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen, et al. Lora: Low-rank adaptation of large language models. _ICLR_ , 1(2):3, 2022. 6 

25214 

