---
title: "NavThinker: Action-Conditioned World Models for Coupled Prediction and Planning in Social Navigation"
date: "2026-03-16"
authors: "Tianshuai Hu; Zeying Gong; Lingdong Kong; XiaoDong Mei; Yiyi Ding; Qi Zeng"
url: https://arxiv.org/abs/2603.15359
pdf: https://arxiv.org/pdf/2603.15359
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.15359)** / [論文ページ](https://arxiv.org/abs/2603.15359)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **NavThinker: Action-Conditioned World Models for Coupled Prediction and Planning in Social Navigation** 

Tianshuai Hu<sup>1</sup> , Zeying Gong<sup>2</sup> , Lingdong Kong<sup>3</sup> , XiaoDong Mei<sup>1</sup> , Yiyi Ding<sup>2</sup> , Qi Zeng<sup>2</sup> , Ao Liang<sup>4</sup> , Rong Li<sup>2</sup> , Yangyi Zhong<sup>2</sup> and Junwei Liang<sup>1</sup><sup>_,_2</sup><sup>_∗_</sup> 

**_Abstract_ — Social navigation requires robots to act safely in dynamic human environments. Effective behavior demands** **_thinking ahead_ : reasoning about how the scene and pedestrians evolve under different robot actions rather than reacting to current observations alone. This creates a coupled predictionplanning challenge, where robot actions and human motion mutually influence each other. To address this challenge, we propose NavThinker, a future-aware framework that couples an action-conditioned world model with on-policy reinforcement learning. The world model operates in the Depth Anything V2 patch feature space and performs autoregressive prediction of future scene geometry and human motion; multi-head decoders then produce future depth maps and human trajectories, yielding a future-aware state aligned with traversability and interaction risk. Crucially, we train the policy with DD-PPO while injecting world-model think-ahead signals via: (i) actionconditioned future features fused into the current observation embedding and (ii) social reward shaping from predicted human trajectories. Experiments on single- and multi-robot Social-HM3D show state-of-the-art navigation success, with zero-shot transfer to Social-MP3D and real-world deployment on a Unitree Go2, validating generalization and practical applicability. Webpage: https://hutslib.github.io/ NavThinker/.** 

## I. INTRODUCTION 

Social navigation requires robots to reach goals safely while respecting human comfort and social norms in dynamic crowds [1], [2], [3]. In such environments, robot and human motions are mutually coupled [1], [4], [5]. Effective navigation therefore demands _thinking ahead_ : reasoning about how the scene will evolve under different actions rather than reacting to observations alone. 

Most existing approaches lack “look-ahead” ability. Prior methods either choose actions from instantaneous observations, behaving myopically in tight interactions [6], [7], [8], [9], [1]; treat pedestrian forecasts as fixed inputs independent of robot actions and plan against these predictions [10], [11], [12], [13]; or jointly reason over robot and human futures via expensive optimization that scales poorly with many agents and long horizons [4], [5]. A promising solution lies in world models within a reinforcement learning (RL) framework. Unlike standard RL, which learns interaction-aware policies 

> 1 The Hong Kong University of Science and Technology. _{_ thuaj, xmeiab _}_ @connect.ust.hk 

> 2 The Hong Kong University of Science and Technology (Guangzhou). _{_ zgong313, ydingaz, qzeng721, rli335, yzhong123 _}_ @connect.hkust-gz.edu.cn, junweiliang@hkust-gz.edu.cn 

> 3 National University of Singapore. lingdong.kong@u.nus.edu 

> 4 University of Chinese Academy of Sciences liangao@sia.cn 

> * Corresponding author. 


Fig. 1: **NavThinker: future-aware social navigation.** Social navigation requires the robot to reach a goal in environments shared with dynamic pedestrians. Red regions highlight interaction zones where the robot and pedestrians may conflict. Top: egocentric depth observations. Bottom: the world model imagines action-conditioned futures for the corresponding observations. By imagining how the scene evolves under different candidate actions, NavThinker anticipates potential social conflicts and selects safe, socially compliant actions. 

through implicit reasoning from experience, a world model explicitly generates future latent features conditioned on actions, thereby modeling interactive dynamics. 

This approach, known as RL-based world modeling [14], [15], [16] offers a natural mechanism for action-conditioned foresight: by learning environment dynamics, it enables imagination that couples prediction and planning within a single learned model. However, bringing world models to social navigation exposes two key challenges: _task-misaligned spatial representations_ and _limited mechanisms to inject foresight into the policy_ . 

The first challenge is that many latent world models do not capture the task-relevant factors needed for safe social navigation. Success depends on both _scene geometry_ and _human motion_ to represent traversability and interaction risk. We address this by operating the world model in the Depth Anything V2 (DA-V2) patch feature space [17], and using depth and trajectory decoders to anchor representations to geometry and motion, improving imagined depth fidelity and 

enabling trajectory-informed policy learning. 

The more fundamental challenge, however, is how to effectively inject this foresight into the policy for future-aware planning. Social navigation requires anticipating human responses to each candidate action and planning accordingly, yet current approaches fall short. Pure imagination methods [14], [18] accumulate compounding errors in complex scenes [19]. Other approaches, whether using imagination for representation learning [20] or reward augmentation [21], keep prediction and planning largely decoupled, that is, they do not query the world model for lookahead planning. We achieve this coupling by two _think-ahead mechanisms_ that form the core of our approach: fusing action-conditioned future features into the observation embedding, and shaping rewards from predicted human trajectories. Experiments show that each mechanism progressively improves navigation success. 

Overall, NavThinker achieves state-of-the-art performance on Social-HM3D, surpassing the previous future-aware method [22] by 3.2% in success rate and 2.95% in SPL, while reducing human collisions. We further extend the benchmark to a more complex multi-robot setting where multiple robots independently use the policy to reach their goals, and NavThinker consistently outperforms all baselines. NavThinker also generalizes zero-shot to Social-MP3D and transfers to a real Unitree Go2 robot. 

To summarize, the primary contributions of this work are: 

- We propose **NavThinker** , a future-aware framework that couples an action-conditioned world model with policy optimization. The world model performs autoregressive prediction in the Depth Anything V2 (DAV2) patch feature space; depth and trajectory decoders then align learned representations with traversability and interaction risk. 

- We introduce two think-ahead mechanisms that inject world-model predictions into policy optimization: _Action-Conditioned Future-Feature Fusion_ as lookahead context, and _Social Reward Shaping_ from predicted human trajectories. 

- We demonstrate state-of-the-art results on single- and multi-robot Social-HM3D, zero-shot generalization to Social-MP3D, and transfer to a real Unitree Go2. 

## II. RELATED WORK 

## _A. Social Navigation & Prediction-Planning Integration_ 

In crowded social environments, navigation is governed by interaction dynamics rather than independent agent motions. The bidirectional influence between robot actions and pedestrian responses makes prediction and planning inherently coupled [1], [2], [3]. Reactive approaches select actions solely from current observations, including social-force models and reciprocal collision avoidance [6], [23], as well as local trajectory optimization [24]. Although efficient, they are myopic and exhibit freezing or oscillatory behavior in dense crowds [1]. Proactive methods incorporate future reasoning by predicting evolving free space or pedestrian trajectories [10], [13]. However, many remain decoupled: predictors 

are trained independently and their outputs are treated as fixed inputs to downstream planners, limiting feedback from planning to prediction. More tightly coupled formulations integrate forecasting and control through bilevel optimization or model-based RL [4]. While narrowing the prediction– planning gap, optimization-based coupling is often computationally heavy, and latent world-model approaches may compress spatial information into global vectors, obscuring fine-grained geometry and interaction structure. Our work targets this coupled regime while preserving spatial fidelity and enabling stable on-policy training. 

## _B. World Models for Embodied Decision-Making_ 

World models learn predictive environment dynamics to support planning or policy optimization [25], [26]. Dreamerstyle recurrent state-space models compress observations into global latent vectors and train policies via imagination [14], achieving strong sample efficiency but discarding explicit spatial structure. Recent work improves temporal modeling with Transformers [27] or preserves spatial detail through diffusion-based prediction [28]. Diffusion models, however, require multi-step denoising at inference, limiting rollout efficiency. Other approaches predict features from frozen vision backbones such as DINOv2 [29] to enable efficient planning [30], yet often lack explicit temporal modeling or interaction-aware objectives. In contrast, we build an actionconditioned world model in the DA-V2 patch feature space, preserving spatial structure via patch tokens while modeling temporal dependencies with a block-causal Transformer. Joint prediction of depth, human trajectories, and rewards from a shared latent state unifies geometry and interaction dynamics within a single predictive framework. 

## _C. Imagination-Based Reinforcement Learning_ 

World models shape policy learning in several ways. Pure imagination actor–critic methods train policies entirely from latent rollouts [18], [14], improving sample efficiency but increasing exposure to compounding model bias. Representation-augmentation approaches inject learned latent features into model-free policies while keeping optimization grounded in real interaction [20], yet do not exploit action-conditioned multi-step imagination. Reward or data augmentation modifies training signals using imagined rollouts or synthetic transitions [21], improving efficiency without fully coupling prediction and planning. Our approach retains image-based, on-policy PPO training [31] while enhancing it through two mechanisms: detached late fusion of predictive features, and action-conditioned imagination that forecasts human responses and injects socially aware penalties into the reward. Unlike latent-only training, the policy remains grounded in real observations; unlike static auxiliary prediction, imagined futures depend explicitly on candidate actions, enabling closed-loop coupling between prediction and planning without sacrificing stability. 

## III. PROBLEM FORMULATION 

We consider a point-goal SocialNav task in environments populated by _N_ dynamic humans. Due to egocentric sensing, 


Fig. 2: **Overview of the NavThinker framework.** Our framework consists of two modules: a world model that learns action-conditioned scene dynamics (top), and an imagination-augmented planner policy trained with DD-PPO (bottom). During **World Model Learning** , depth observations, actions, and robot states are extracted from the Replay Buffer. A frozen DA-V2 ViT encoder extracts patch embeddings, and a Causal Attention Transformer autoregressively predicts future latent features. A Depth Decoder and a Human Trajectory Decoder are trained alongside a latent consistency loss to anchor representations to scene geometry and human motion. During **Policy Learning** , the Observation Encoder produces the current embedding from depth and robot states. The Imagination module queries the world model under each candidate action, generating action-conditioned future features that are fused with the current embedding via Feature Fusion. The fused representation feeds into the DD-PPO Actor-Critic network. Predicted human trajectories additionally provide Reward Shaping, coupling prediction with planning in an imagine-then-act loop. 

occlusions, and limited field-of-view, the environment state can only be partially observed. We formulate this task as a _Partially Observable Markov Decision Process_ (POMDP) ( _S, O, A, T , r, γ_ ), where _st ∈S_ is the latent environment state, _ot ∈O_ is the observation, _at ∈A_ is the action, _T_ ( _st_ +1 _| st, at_ ) is the transition kernel, _r_ ( _st, at_ ) is the reward, and _γ ∈_ (0 _,_ 1) is the discount factor. At each timestep _t_ , the agent selects _at_ based on the observation history _o≤t_ . 

## _A. State and Observation_ 

We decompose the latent state, for each timestamp _t_ , into the robot state, static scene, and human states: 


where _xt_ denotes the robot pose, _M_ denotes the static scene structure, and _h_<sup>(</sup> _t_<sup>_i_)</sup> denotes the _i_ -th human’s pose. The robot receives a partial observation as: 


where _dt_ is the egocentric depth image, _g_ specifies the navigation goal, and _xt_ the robot’s own pose. With limited observability, neither the full scene _M_ nor the complete human states _{h_<sup>(</sup> _t_<sup>_i_)</sup><sup>_}N_</sup> _i_ =1<sup>aredirectlyobserved.</sup> 

## _B. Action Space_ 

The robot executes a discrete action set _at ∈A_ , where _A_ = _{_ FORWARD _,_ TURN-LEFT _,_ TURN-RIGHT _,_ STOP _}_ . 

## _C. Objective and the Coupling Challenge_ 

We seek a policy _π_ ( _at | o≤t_ ) that maximizes the expected return: 


Equivalently, from a planning view, the agent selects actions to trade off task efficiency and social compliance under evolving human motion: 


Here **a** denotes a length- _H_ action sequence, **_ξ_** 1: _N_ denotes future human trajectories, _c_ task captures progress-to-goal and path efficiency, and _c_ social penalizes social violations. 

This exposes the key difficulty in social navigation: effective decisions require reasoning about _future human motion_ , coupling prediction and planning under partial observability. 

## _D. Latent World Modeling for SocialNav_ 

NavThinker couples a _world model_ and a _policy_ in a closed loop over a latent feature state _Zt_ . The state is inferred from observations, which is: 


Given _Zt_ , the world model imagines the next latent state under each candidate action _a ∈A_ : 


The policy then selects an action conditioned on both the current observation and the imagined futures: 


This imagine-then-act cycle enables the robot to anticipate how the scene will evolve under each possible action, coupling prediction and planning under partial observability. 

|IV. METHODOLOGY|
|---|


## _A. Overview_ 

NavThinker tackles coupled prediction and planning in social navigation by learning a world model and using it as an imagination engine for policy improvement. As shown in Fig. 2, it consists of two modules: (i) an action-conditioned **scene-and-interaction world model** operating in DA-V2 patch-feature space, which predicts future patch latents and uses multi-head decoders to forecast future depth and human trajectories, producing a future-aware state capturing traversability and interaction risk; and (ii) an **imaginationaugmented planner policy** trained on-policy with DD-PPO, which exploits imagined rollouts by fusing candidate-actionconditioned future features with the current observation embedding and by shaping rewards from predicted human trajectories. This imagination-enabled training couples prediction and planning through the learned latent dynamics. 

## _B. Scene-and-Interaction World Model Learning_ 

Social navigation is partially observable, with incomplete perception of scene structure and human states; moreover, robot actions and human motion are bidirectionally coupled. We therefore learn a latent world model in the patchfeature space with a frozen Depth Anything V2 (DA-V2) encoder [17], predicting the action-conditioned evolution of the scene. Our model consists of three components: 


where _zt ∈_ R<sup>_P ×D_</sup> denotes the patch embeddings ( _P_ patches, _D_ dimensions), _H_ is the context length, and the decoder heads produce depth _d_ ˆ _t_ , human trajectory **_ξ_** ˆ1: _Nh_ , and reward _r_ ˆ _t_ predictions respectively. 

_a) Observation encoder:_ We adopt a frozen DA-V2 ViT [17] as the observation model. At each timestep _t_ , it encodes the depth image _ot_ into patch embeddings _zt ∈_ R<sup>_P ×D_</sup> . The encoder remains frozen during training, providing taskindependent, spatially rich representations that generalise across environments. 

_b) Transition model:_ We adopt a ViT-based causal Transformer [32] operating directly on patch embeddings. Each action _at_ is encoded into a _D_ -dimensional token and appended to the patch sequence, yielding ( _P_ +1) tokens per frame. A causal sliding-window mask of length _H_ restricts each frame to attend only to its preceding context, enabling frame-level autoregressive prediction that captures global 

scene structure and temporal coherence. The transition model is trained with a latent consistency loss: 

|_Lf_(_ϕ_) =_∥_ˆ_zt_+1_−zt_+1_∥_<sup>2</sup><br>2<sup>_,_</sup><br>(11)|
|---|


which aligns the predicted patch features ˆ _zt_ +1 with the frozen encoder’s output _zt_ +1. 

_c) Decoder heads:_ Task-specific decoders predict depth, human trajectories, and reward from the predicted patch features; their training is independent of the transition model. The _depth decoder_ follows a DPT-style architecture [33] that reassembles patch tokens into multi-scale feature maps and progressively upsamples them to reconstruct the normalised depth map: 


The _trajectory decoder_ takes the global feature MeanPool( _zt_ ) and predicts human’s future positions over a horizon _T_ : 

|ˆ**_ξ_**1:_Nh_ = TrajDec<br>�|MeanPool(_zt_)<br>|�<br>_._<br>(13)|
|---|---|---|


The _reward decoder_ predicts a scalar reward from the same global feature: _r_ ˆ _t_ = MLP�MeanPool( _zt_ )�. The combined decoder loss is: 

|_L_dec(_ψ_) =_Ld_(_dt,_ <sup>ˆ</sup>_dt_) +_λξ Lξ_(**_ξ_**1:_Nh,_ <sup>ˆ</sup>**_ξ_**1:_Nh_) +_λr Lr_|(_rt,_ˆ_rt_)_._<br>(14)|
|---|---|


_d) Training objective:_ The transition model is trained with a latent consistency loss between predicted and groundtruth patch features. The decoders are trained independently with task-specific losses. Depth reconstruction anchors the belief to local geometry, human forecasting captures interaction dynamics, and the latent consistency term ensures faithful imagination: 

|_L_WM(_ϕ_) =_λf _<br>�|_∥_ˆ_zt_+1_−zt_+1_∥_<sup>2</sup><br>2<br>��<br>�<br>+|_Ld_+_λξ Lξ_+_λr_<br>�<br>��|_Lr_<br>�<br>_,_|
|---|---|---|---|
||latent consistency|decoder losses||


|(15)|
|---|


where _Ld_ , _Lξ_ , _Lr_ supervise depth reconstruction, human trajectory forecasting, and reward prediction, respectively. The latent consistency term aligns imagined patch features with the frozen encoder’s output. 

## _C. Imagination-Augmented Policy Learning_ 

A learned world model that captures scene geometry and human dynamics enables the policy to _think before acting_ : by imagining the consequences of each candidate action in latent space, the agent can anticipate future interactions without additional environment steps. We train an imaginationaugmented policy that queries the world model to anticipate action consequences before execution. Our policy consists of three components: 

|Observation Encoder:|_et_ = Enc(_ot, at−_1)_,_|(16)|
|---|---|---|
|Imagination Module:|_lt_ = Imagine(_zt−H_:_t, A_; _ϕ_)_,_|(17)|
|Policy Head:|_at, Vt_ =_πθ_(_et, lt, g_)_, Vψ_(_et, _|_lt, g_)_,_<br>(18)|


TABLE I: **Single-Robot Social Navigation Results** on Social-HM3D and Social-MP3D (zero-shot transfer from Social-HM3D). We report SR/SPL (success/efficiency), PSC (social compliance), and H-Coll (human collisions). Best and 2nd-best are in **bold** and <u>underline.</u> 

|**Methods**||**Social-**|**HM3D**|||**Social-**|**MP3D**||
|---|---|---|---|---|---|---|---|---|
||SR_↑_|SPL_↑_|PSC_↑_|H-Coll_↓_|SR_↑_|SPL_↑_|PSC_↑_|H-Coll_↓_|
|**Rule-based**|||||||||
|A* [34]|44.81|43.99|90.38|54.80|45.67|44.69|91.97|54.00|
|ORCA [35]|37.44|32.91|**92.23**|39.77|38.81|34.65|**94.03**|39.86|
|**Reinforcement Lear**|**ning-based**||||||||
|Habitat-official [36]|38.99|33.53|90.37|55.48|37.00|31.76|92.03|52.33|
|Falcon [22]|56.26|52.05|89.76|41.22|**51.67**|**45.54**|92.53|40.67|
|**NavThinker**|**59.46**|**55.00**|89.91|**39.09**|47.33|41.71|93.68|**37.67**|


TABLE II: **Multi-Robot Social Navigation Results** on SocialHM3D. Robots navigate to individual goals without communication. We report SR/SPL (success/efficiency), PSC (social compliance), H-Coll (human collisions), and team-level T-SR/T-SPL. Best and second-best are highlighted in **bold** and underline, respectively. 

|Method|SR_↑_|SPL_↑_|PSC_↑_|H-Coll_↓_|T-SR_↑_|T-SPL_↑_|
|---|---|---|---|---|---|---|
|**Rule-Based**|||||||
|A* [34]|26.06|25.70|95.20|35.68|14.76|14.51|
|ORCA [35]|24.13|22.48|95.53|35.13|15.09|13.84|
|**Reinforcement Lear**|**ning**||||||
|Habitat-official [36]|26.78|24.41|95.47|31.39|14.98|13.68|
|Falcon [22]|28.63|26.48|94.98|28.63|16.08|15.12|
|**NavThinker**|**30.04**|**28.14**|**95.55**|**25.55**|**16.30**|**15.22**|


where _et ∈_ R<sup>_de_</sup> denotes the observation embedding, _lt ∈_ R<sup>_|A|·dl_</sup> aggregates imagined outcomes for all candidate actions, and _g_ is the goal specification. 

_a) Observation encoder:_ A ResNet encoder [37] extracts visual features from the depth image _ot_ , which are concatenated with the previous action _at−_ 1 and fused through a GRU to produce the observation embedding _et ∈_ R<sup>_de_</sup> . This recurrent encoding captures temporal context beyond the current frame. 

_b) Imagination module:_ We query the world model’s transition model _pϕ_ to predict latent outcomes for each candidate action: 


The predicted latent states are concatenated to form the lookahead feature _lt_ and then fusion with the observation embedding _et_ , enabling the policy to anticipate future interactions before acting. 

_c) Policy head:_ The policy head comprises an actor that outputs a distribution over discrete actions and a critic that estimates state values: 


_d) Reward design and training objective:_ We train the policy with DD-PPO [38] under a reward that combines task progress with world-model-derived social shaping: 


where _rt_<sup>goal</sup> measures geodesic progress toward the goal, _rt_<sup>succ</sup> provides a terminal bonus upon success, and _rt_<sup>coll</sup> penalizes collisions with static obstacles and humans. The predictive social cost _rt_<sup>traj</sup> is computed from the actionconditioned forecasts of human trajectories **_ξ_**<sup>ˆ</sup> 1: _Nh_ , coupling human motion prediction with decision-making: the world model predicts future human positions under candidate actions, and the policy is optimized to maintain safe separation from these predicted interaction futures. This encourage anticipatory and socially compliant behaviors. 

## V. EXPERIMENTS 

In this section, we first outline evaluation details and then present quantitative comparisons with state-of-the-art methods on single-robot and multi-robot benchmarks. A series of ablation studies are presented to evaluate the individual components of our approach: the two think-ahead mechanisms and our world model quality. We then report zero-shot generalization and real-world deployment results, and conclude with qualitative analysis. 

## _A. Experiments Setup_ 

**Benchmarks.** We evaluate NavThinker on the Social-HM3D benchmark [22], built upon photo-realistic Habitat environments populated with goal-driven, collision-aware pedestrians. Each episode places controllable robots alongside autonomous humans; every robot must navigate to its goal while respecting personal space and avoiding collisions. We consider two settings: (i) **single-robot** , where one robot navigates among dynamic humans, and (ii) **multi-robot** , a more challenging setting we introduce to increase benchmark complexity, where multiple robots independently execute their own policies to reach individual goals without communication. To evaluate generalization, we additionally test on **Social-MP3D** in a zero-shot transfer setting. **Metrics.** Following [22], we report per-robot metrics: Success Rate (SR), Success Weighted by Path-Length (SPL), Personal Space Compliance (PSC), and Human Collision rate (H-Coll). For the multi-robot setting, we additionally report Team Success Rate (T-SR), which equals 1 only when _all_ robots reach their goals, and Team SPL (T-SPL), which rewards path efficiency only under full team success. 

**Baselines.** We evaluate NavThinker against rule-based planners A* [34] and ORCA [35], RL methods from Habitatofficial [36], and the future-aware baseline Falcon [22]. 


Fig. 3: **World model imagination quality.** Left: current depth observation with RGB, third-person view, and top-down map for reference. Right: after executing the action at the previous timestep, we show (from top to bottom) the ground-truth depth, the world model’s predicted depth, the PCA visualization of ground-truth DA-V2 features, and the PCA visualization of predicted features. The world model produces faithful depth predictions and latent features that closely match the ground truth across different actions. 

TABLE III: **Ablation Study** of NavThinker planning policy components on the single-robot Social-HM3D benchmark. LookH.: world-model lookahead imagination; TrajR.: trajectory-based social reward shaping. Metrics include SR/SPL (success/efficiency), PSC (social compliance), and H-Coll (human collisions). 

|LookH.|TrajR.|SR_↑_|SPL_↑_|PSC_↑_|H-Coll_↓_|
|---|---|---|---|---|---|
|_×_|_×_|43.36|36.27|90.81|47.33|
|✓|_×_|55.87|49.36|90.58|39.19|
|✓|✓|59.46|55.00|89.91|39.09|


TABLE IV: **Ablation Study** of planner policy components on multi-robot Social-HM3D. LookH.: world-model lookahead imagination; TrajR.: trajectory-based social reward shaping. Metrics include SR/SPL (success/efficiency), PSC (social compliance), H-Coll (human collisions), and T-SR/T-SPL (team-level success/efficiency). 

|LookH.TrajR.|SR_↑_|SPL_↑_|PSC_↑_|H-Coll_↓_|T-SR_↑_|T-SPL_↑_|
|---|---|---|---|---|---|---|
|_×_<br>_×_|13.64|11.27|93.85|59.25|13.44|11.13|
|✓<br>_×_|28.52|26.52|95.47|25.88|14.76|13.73|
|✓<br>✓|30.04|28.14|95.55|25.55|16.30|15.22|


## _B. Quantitative Results_ 

_a) Single-robot social navigation.:_ As shown in Tab. I, NavThinker achieves state-of-the-art performance with the highest SR (59.46) and SPL (55.00) while maintaining comparable personal space compliance. Compared to the futureaware method Falcon, NavThinker improves success rate by 3.2% and SPL by 2.95%, while reducing human collisions from 41.22% to 39.09%, demonstrating that thinking ahead enables both efficient and socially compliant navigation. 

_b) Multi-robot social navigation.:_ To further evaluate NavThinker in more complex coordination scenarios, we extend Social-HM3D with a multi-robot setting where multiple robots independently use their own policies to reach indi- 

TABLE V: **Ablation Study** on auxiliary losses for World Model training. Evaluation on 200 episodes from the held-out replay buffer. _Ld_ is the depth reconstruction loss and _Lξ_ is the human trajectory prediction loss. CosSim is the cosine similarity between predicted and target latent features. Depth RMSE is the root mean squared error of predicted depth images. Traj ADE/FDE are the average and final displacement errors of predicted human trajectories. 

|_Ld_|_Lξ_|CosSim_↑_|Depth RMSE_↓_|Traj ADE_↓_|Traj FDE_↓_|
|---|---|---|---|---|---|
|_×_|_×_|0.9278|0.0406|—|—|
|✓|_×_|0.9342|0.0389|—|—|
|✓|✓|0.9383|0.0371|1.74|1.93|


vidual goals. As shown in Tab. II, NavThinker consistently outperforms all baselines across both per-robot and teamlevel metrics, demonstrating that NavThinker is capable of handling more complex scenarios with denser interactions. 

_c) Zero-shot generalization.:_ To assess generalization ability, we directly evaluate models trained on Social-HM3D on Social-MP3D without any fine-tuning. Tab. I reports results testing on 300 episodes of Social-MP3D. NavThinker maintains competitive performance in this zero-shot transfer setting, demonstrating that the learned world model and think-ahead mechanisms generalize across different environments and scene layouts. 

## _C. Ablation Study & Analyses_ 

We conduct ablation studies to validate the two key challenges and corresponding contributions: (i) the thinkahead mechanisms for injecting foresight into the policy, and (ii) the task-aligned world model with depth and trajectory decoders. 

_1) Policy: Think-Ahead Mechanisms:_ To validate that injecting foresight into the policy enables coupled prediction and planning, we ablate the two think-ahead mechanisms: 


Fig. 5: **Real-world deployment on a Unitree Go2 robot.** In this scenario, the robot navigates around a group of people and reaches its goal while maintaining safe distances. 

especially important in complex scenarios where anticipating the behavior of both humans and other robots is critical. 

_2) World Model: Task-Aligned Decoders:_ To validate that task-aligned decoders improve the quality of imagined futures, we evaluate world model variants with different decoder configurations on a held-out replay buffer. As shown in Tab. V,, adding the depth decoder _Ldd_ improves cosine similarity between predicted and target latent features from 0.9278 to 0.9342, and reduces depth RMSE from 0.0406 to 0.0389. Further incorporating the trajectory decoder _Lξ_ yields the best latent consistency (CosSim 0.9383) and depth fidelity (RMSE 0.0371), confirming that anchoring the world model to both scene geometry and human motion produces higher-quality imagined futures. 

Fig. 4: **Qualitative comparisons on Social-HM3D.** Navthinker produces safe actions under different social situations. **Rows 1–2 (Blind corner):** A* collides when turning, while ours avoids the pedestrian. **Rows 3–4 (Intersection):** Falcon collides at the intersection, while ours safely yields and passes. **Rows 5–6 (Front approach):** Habitat-official collides in a head-on encounter, while ours gives way for the pedestrian. Red boxes mark baseline failures; green checkmarks indicate safe behaviors. 

Notably, the trajectory decoder’s contribution extends beyond world model fidelity: the trajectory-based reward shaping directly consumes predicted human trajectories from the world model, and its consistent improvement on policy performance (Tab. III, IV) provides evidence that the taskaligned decoder benefits not only imagination quality but also downstream decision-making. 

lookahead imagination (LookH.) and trajectory-based social reward shaping (TrajR.). 

_a) Single-robot setting.:_ As shown in Tab. III, the base policy without any think-ahead mechanism achieves only 43.36% SR. Adding lookahead imagination raises SR to 55.87% (+12.51% relative), demonstrating that fusing actionconditioned future features into the observation embedding substantially improves navigation by enabling the policy to compare imagined outcomes before acting. Further incorporating trajectory-based reward shaping yields 59.46% SR (+3.59% relative over lookahead alone), confirming that shaping rewards from predicted human trajectories encourages the policy to anticipate social interactions. 

## _D. Qualitative Analysis_ 

Figure 4 presents qualitative comparisons between NavThinker and baseline methods in representative social navigation scenarios on Social-HM3D. 

## _E. Real-World Deployments_ 

To validate the practical applicability of our approach in real environments, we deploy NavThinker on a Unitree Go2 quadruped robot. We use an Intel RealSense D455i depth camera as the depth input to the model. The system operates in a client-server architecture: the Go2 handles sensor data acquisition and locomotion control on-board, while streaming depth observations to a server machine for 

_b) Multi-robot setting.:_ The same trend is observed in the multi-robot setting (Tab. IV), where each mechanism again progressively improves both success rate and collision avoidance. The improvements are even more pronounced in this setting, confirming that the think-ahead mechanisms are 

model inference. The predicted actions are sent back to the Go2 for execution. NavThinker successfully navigates to designated goals while maintaining safe distances from pedestrians. 

## VI. CONCLUSION 

In this paper, we proposed NavThinker, a future-aware social navigation framework that couples a task-aligned world model in the DA-V2 patch feature space with on-policy reinforcement learning. Depth and trajectory decoders anchor representations to scene geometry and human motion, while two think-ahead mechanisms, namely future feature fusion and social reward shaping, inject foresight into the policy for coupled prediction and planning. NavThinker achieves stateof-the-art results on single-robot and multi-robot SocialHM3D, generalizes zero-shot to Social-MP3D, and transfers to a real Unitree Go2. Future research may concentrate on extending the world model to incorporate multi-modal observations ( _e.g._ , RGB and semantic information) for richer scene understanding, or exploring longer imagination horizons to handle more complex social interactions. 

## REFERENCES 

- [1] C. Mavrogiannis, F. Baldini, A. Wang _et al._ , “Core challenges of social robot navigation: A survey,” _ACM Transactions on HumanRobot Interaction_ , vol. 12, no. 3, pp. 1–39, 2023. 

- [2] A. Francis, C. P´erez-d’Arpino, C. Li, F. Xia, A. Alahi, R. Alami, A. Bera, A. Biswas, J. Biswas _et al._ , “Principles and guidelines for evaluating social robot navigation algorithms,” _ACM Transactions on Human-Robot Interaction_ , vol. 14, no. 2, pp. 1–65, 2025. 

- [3] I. K. Kabir and M. F. Mysorewala, “Socially aware navigation for mobile robots: a survey on deep reinforcement learning approaches,” _Applied Intelligence_ , vol. 56, no. 1, p. 38, 2026. 

- [4] S. Samavi _et al._ , “SICNav: Safe and interactive crowd navigation using model predictive control and bilevel optimization,” _IEEE Transactions on Robotics_ , vol. 41, pp. 801–818, 2024. 

- [5] M. Sun, F. Baldini, P. Trautman, and T. Murphey, “Move beyond trajectories: Distribution space coupling for crowd navigation,” _arXiv preprint arXiv:2106.13667_ , 2021. 

- [6] D. Helbing and P. Molnar, “Social force model for pedestrian dynamics,” _Physical review E_ , vol. 51, no. 5, p. 4282, 1995. 

- [7] G. Ferrer, A. Garrell, and A. Sanfeliu, “Robot companion: A socialforce based approach with human awareness-navigation in crowded environments,” in _IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2013, pp. 1688–1694. 

- [8] P. Fiorini and Z. Shiller, “Motion planning in dynamic environments using velocity obstacles,” _International Journal of Robotics Research_ , vol. 17, no. 7, pp. 760–772, 1998. 

- [9] J. Van den Berg, M. Lin, and D. Manocha, “Reciprocal velocity obstacles for real-time multi-agent navigation,” in _IEEE International Conference on Robotics and Automation_ , 2008, pp. 1928–1935. 

- [10] H. Thomas, J. Zhang, and T. D. Barfoot, “The foreseeable future: Selfsupervised learning to predict dynamic scenes for indoor navigation,” _IEEE Transactions on Robotics_ , vol. 39, no. 6, pp. 4581–4599, 2023. 

- [11] Y. Cui, H. Zhang, Y. Wang, and R. Xiong, “Learning world transition model for socially aware robot navigation,” in _IEEE International Conference on Robotics and Automation_ , 2021, pp. 9262–9268. 

- [12] S. Eiffert, H. Kong, N. Pirmarzdashti, and S. Sukkarieh, “Path planning in dynamic environments using generative RNNs Monte Carlo tree search,” in _IEEE International Conference on Robotics and Automation_ , 2020, pp. 10 263–10 269. 

- [13] S. Poddar, C. Mavrogiannis, and S. S. Srinivasa, “From crowd motion prediction to robot navigation in crowds,” in _IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2023, pp. 6765–6772. 

- [14] D. Hafner _et al._ , “Mastering diverse domains through world models,” _arXiv preprint arXiv:2301.04104_ , 2023. 

- [15] S. Shanks, J. Embley-Riches, J. Liu, A. M. Delfaki, C. Ciliberto, and D. Kanoulas, “DreamerNav: Learning-based autonomous navigation in dynamic indoor environments using world models,” _Frontiers in Robotics and AI_ , vol. 12, p. 1655171, 2025. 

- [16] G. Oguzie, A. Ek´art, and L. J. Manso, “Predictive world models for social navigation,” in _UK Workshop on Computational Intelligence_ . Springer, 2023, pp. 53–64. 

- [17] L. Yang, B. Kang, Z. Huang, Z. Zhao, X. Xu, J. Feng, and H. Zhao, “Depth anything v2,” _Advances in Neural Information Processing Systems_ , vol. 37, pp. 21 875–21 911, 2024. 

- [18] D. Hafner, T. Lillicrap, M. Norouzi, and J. Ba, “Mastering Atari with discrete world models,” _arXiv preprint arXiv:2010.02193_ , 2020. 

- [19] M. Janner, J. Fu, M. Zhang, and S. Levine, “When to trust your model: Model-based policy optimization,” _Advances in Neural Information Processing Systems_ , vol. 32, pp. 12 519–12 530, 2019. 

- [20] W. Liu, H. Zhao, C. Li, J. Biswas, B. Okal, P. Goyal, Y. Chang, and S. Pouya, “X-Mobility: End-to-end generalizable navigation via world modeling,” in _IEEE International Conference on Robotics and Automation_ , 2025, pp. 7569–7576. 

- [21] N. Hirose, D. Shah, K. Stachowicz, A. Sridhar, and S. Levine, “Selfi: Autonomous self-improvement with reinforcement learning for social navigation,” _arXiv preprint arXiv:2403.00991_ , 2024. 

- [22] Z. Gong, T. Hu, R. Qiu, and J. Liang, “From cognition to precognition: A future-aware framework for social navigation,” in _IEEE International Conference on Robotics and Automation_ , 2025, pp. 9122–9129. 

- [23] J. Van Den Berg _et al._ , “Optimal reciprocal collision avoidance for multi-agent navigation,” in _IEEE International Conference on Robotics and Automation Workshops_ , 2010. 

- [24] C. R¨osmann, W. Feiten, T. W¨osch, F. Hoffmann, and T. Bertram, “Efficient trajectory optimization using a sparse model,” in _European Conference on Mobile Robots_ , 2013, pp. 138–143. 

- [25] D. Ha and J. Schmidhuber, “World models,” _arXiv preprint arXiv:1803.10122_ , vol. 2, no. 3, p. 440, 2018. 

- [26] D. Hafner _et al._ , “Learning latent dynamics for planning from pixels,” in _International Conference on Machine Learning_ . PMLR, 2019, pp. 2555–2565. 

- [27] W. Zhang, G. Wang, J. Sun, Y. Yuan, and G. Huang, “STORM: Efficient stochastic transformer based world models for reinforcement learning,” _Advances in Neural Information Processing Systems_ , vol. 36, pp. 27 147–27 166, 2023. 

- [28] E. Alonso, A. Jelley, V. Micheli, A. Kanervisto, A. J. Storkey, T. Pearce, and F. Fleuret, “Diffusion for world modeling: Visual details matter in Atari,” _Advances in Neural Information Processing Systems_ , vol. 37, pp. 58 757–58 791, 2024. 

- [29] M. Oquab, T. Darcet, T. Moutakanni, H. Vo, M. Szafraniec, V. Khalidov, P. Fernandez, D. Haziza, F. Massa, A. El-Nouby _et al._ , “DINOv2: Learning robust visual features without supervision,” _arXiv preprint arXiv:2304.07193_ , 2023. 

- [30] G. Zhou, H. Pan, Y. LeCun, and L. Pinto, “DINO-WM: World models on pre-trained visual features enable zero-shot planning,” _arXiv preprint arXiv:2411.04983_ , 2024. 

- [31] J. Schulman _et al._ , “Proximal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 

- [32] A. Dosovitskiy, L. Beyer, A. Kolesnikov, D. Weissenborn, X. Zhai, T. Unterthiner, M. Dehghani, M. Minderer, G. Heigold, S. Gelly _et al._ , “An image is worth 16x16 words: Transformers for image recognition at scale,” _arXiv preprint arXiv:2010.11929_ , 2020. 

- [33] R. Ranftl, A. Bochkovskiy, and V. Koltun, “Vision transformers for dense prediction,” in _IEEE/CVF International Conference on Computer Vision_ , 2021, pp. 12 179–12 188. 

- [34] P. E. Hart, N. J. Nilsson, and B. Raphael, “A formal basis for the heuristic determination of minimum cost paths,” _IEEE Transactions on Systems Science and Cybernetics_ , vol. 4, no. 2, pp. 100–107, 1968. 

- [35] J. Van Den Berg, S. J. Guy, M. Lin, and D. Manocha, “Reciprocal n-body collision avoidance,” in _International Symposium on Robotics Research_ . Springer, 2011, pp. 3–19. 

- [36] X. Puig, E. Undersander, A. Szot, M. D. Cote, T.-Y. Yang, R. Partsey, R. Desai _et al._ , “Habitat 3.0: A co-habitat for humans, avatars and robots,” _arXiv preprint arXiv:2310.13724_ , 2023. 

- [37] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in _IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2016, pp. 770–778. 

- [38] E. Wijmans, A. Kadian, A. Morcos _et al._ , “DD-PPO: Learning nearperfect pointgoal navigators from 2.5 billion frames,” _arXiv preprint arXiv:1911.00357_ , 2019. 

