---
title: "Advances in GRPO for Generation Models: A Survey"
date: "2026-02-21"
authors: "Zexiang Liu; Xianglong He; Yangguang Li"
url: https://arxiv.org/abs/2603.06623
pdf: https://arxiv.org/pdf/2603.06623
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.06623)** / [論文ページ](https://arxiv.org/abs/2603.06623)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Advances in GRPO for Generation Models: A Survey** 

> 1 **Zexiang Liu** 2 **Xianglong He** 3 **Yangguang Li** 

1SJTU 2THU 3CUHK 

## **Abstract** 

Large-scale flow matching models have achieved strong performance across generative tasks such as text-to-image, video, 3D, and speech synthesis. However, aligning their outputs with human preferences and task-specific objectives remains challenging. Flow-GRPO extends Group Relative Policy Optimization (GRPO) to generation models, enabling stable reinforcement learning alignment for generative systems. Since its introduction, Flow-GRPO has triggered rapid research growth, spanning methodological refinements and diverse application domains. This survey provides a comprehensive review of Flow-GRPO and its subsequent developments. We organize existing work along two primary dimensions. First, we analyze methodological advances beyond the original framework, including reward signal design, credit assignment, sampling efficiency, diversity preservation, reward hacking mitigation, and reward model construction. Second, we examine extensions of GRPO-based alignment across generative paradigms and modalities, including text-to-image, video generation, image editing, speech and audio, 3D modeling, embodied vision-language-action systems, unified multimodal models, autoregressive and masked diffusion models, and restoration tasks. By synthesizing theoretical insights and practical adaptations, this survey highlights Flow-GRPO as a general alignment framework for modern generative models and outlines key open challenges for scalable and robust reinforcement-based generation. 

## **1 Introduction** 

Large-scale flow matching [73] models have demonstrated remarkable performance in generative tasks such as text-to-image, video, 3D, and speech synthesis [197, 126, 69, 65, 26]. However, their outputs are often insufficiently aligned with human preferences or task-specific objectives. Group Relative Policy Optimization (GRPO) [107] is a reinforcement learning algorithm centered on relative advantages within a group of candidates. Unlike conventional policy-gradient methods that require learning an explicit value function, GRPO compares multiple trajectories sampled under the same condition at each update step and estimates advantages using normalized relative rewards. This design substantially improves training stability. GRPO was originally introduced for aligning large language models (LLMs): by asking the model to select responses that better match human preferences from a set of candidates, prior work showed that GRPO is more stable than value-based optimization methods, achieves higher sample efficiency, and effectively mitigates error amplification caused by imperfect preference models. 

Extending GRPO from text generation to more generation tasks (e.g., visual, 3D and speech task), however, is non-trivial. _Diffusion and flow-matching models require dozens to hundreds of denoising or evolution steps to generate a single image, making sampling far more expensive than in LLMs. Their sampling processes are typically formulated as deterministic ODE solvers, which limits diversity among group candidates. Moreover, rewards in visual tasks are often only available at the terminal step (e.g., image quality scores), leading to severe credit assignment issues. In addition, reward_ 

Survey Report. 

_models in the visual domain are more susceptible to reward hacking, where models exploit shortcuts to increase reward scores while degrading true perceptual quality._ 

Flow-GRPO [77] is the first work to successfully apply GRPO to visual generation tasks. It addresses the lack of stochasticity by converting the deterministic ODE formulation of flow-matching models into a stochastic differential equation (SDE), and introduces a denoising-shrinkage strategy during training to reduce reverse-time sampling costs. Empirically, Flow-GRPO improves GenEval accuracy on text-rendering tasks from 63% to 95%, and character rendering accuracy from 59% to 92%. The paper also derives explicit formulas for the ODE-to-SDE transformation and proves that, by introducing appropriate drift and diffusion terms, the resulting stochastic process is equivalent to the original ODE in expectation. 

Since mid-2025, research topic around Flow-GRPO has experienced explosive growth, spanning a wide range of application domains including text-to-image (T2I), text-to-video (T2V), image-to-video (I2V), speech enhancement, 3D generation, vision-language-action (VLA), and more. To date, this rapidly expanding line of work has accumulated over 200 published papers, reflecting strong and sustained community interest. 

This survey provides a systematic and comprehensive review of all these works, organizing and analyzing them along the following dimensions: 

### **Advances beyond Flow-GRPO:** 

- **Reward Signal Design: From Sparse to Dense** (§3.1). 

- **Credit Assignment: From Trajectory to Step Level** (§3.2). 

- **Sampling Efficiency and Training Acceleration** (§3.3). 

- **Mode Collapse and Diversity Preservation** (§3.4). 

- **Reward Hacking Mitigation** (§3.5). 

- **ODE vs. SDE Sampling Strategies** (§3.6). 

- **Reward Model Design and Evaluation Benchmarks** (§3.7). 

### **Extensions to Generative Tasks:** 

- **Text-to-Image Generation** (§4.1). 

- **Video Generation** (§4.2). 

- **Image Editing** (§4.3). 

- **Speech and Audio** (§4.4). 

- **3D Generation and Scientific Applications** (§4.5). 

- **VLA and Embodied AI** (§4.6). 

- **Unified Multimodal Models** (§4.7). 

- **Autoregressive and Masked Diffusion Models** (§4.8). 

- **Image Restoration and Super-Resolution** (§4.9). 

## **2 Background and Preliminaries** 

### **2.1 Flow Matching Models** 

Flow matching models define a continuous-time transformation from a noise distribution _p_ 0 = _N_ (0 _, I_ ) to the data distribution _p_ 1 = _p_ data. Given a parameterized velocity field _vθ_ ( _xt, t_ ), samples evolve along an ODE trajectory: 


where _x_ 0 _∼N_ (0 _, I_ ) and _x_ 1 is the generated sample. The training objective is the _Conditional Flow Matching_ (CFM) loss: 


2 

where _ut_ ( _xt | x_ 1) = _x_ 1 _− x_ 0 denotes the conditional velocity field corresponding to a linear interpolation path, and 


### **2.2 Principles of Group Relative Policy Optimization** 

The core idea of _Group Relative Policy Optimization_ (GRPO) is **critic-free** policy optimization. For each conditioning input _c_ , a group of outputs _{o_ 1 _, o_ 2 _, . . . , oG}_ is sampled, and their corresponding rewards _{r_ 1 _, r_ 2 _, . . . , rG}_ are evaluated. The advantage is computed via group-wise normalization: 


The GRPO objective follows a PPO-style clipped policy gradient: 


where _ρi_ =<sup>_πθ_</sup><sup><u>(</u></sup><sup>_oi|c_</sup><sup><u>)</u></sup> _π_ ref( _oi|c_ )<sup>is the importance ratio and</sup><sup>_ϵ_is the PPO clipping parameter.</sup> 

### **2.3 Flow-GRPO: From LLMs to Generative Models** 

The key challenge in applying GRPO to flow matching models lies in the fact that their sampling process is governed by a **deterministic ODE** , which lacks the **stochastic exploration** required for reinforcement learning. Flow-GRPO introduces stochasticity by converting the ODE into a stochastic differential equation (SDE): 


where _σ_ ( _t_ ) is a noise scheduling function and _dWt_ denotes the Wiener process increment. 

The denoising process is formulated as a Markov Decision Process (MDP): 

- **State** _st_ = ( _xt, c, t_ ): latent variable, conditioning input, and time step 

- **Action** _at_ : denoising direction induced by the stochastic term 

- **Policy** _πθ_ ( _at | st_ ): parameterized conditional distribution 

- **Reward** _r_ : terminal reward evaluated by a reward model on the final sample 

The per-step log-likelihood is given by: 


## **3 Advances beyond Flow-GRPO** 

Building upon Flow-GRPO [77], many subsequent studies have introduced methodological enhancements to further improve its effectiveness and efficiency. To facilitate a more intuitive comparison across methods, we summarize the category, methods, core innovation, key contribution and result. These methods can be categorized into seven major classes based on their distinctive characteristics, which will be discussed in detail below, from §3.1 to (§3.7). 

### **3.1 Reward Signal Design: From Sparse to Dense** 

**The Sparse Reward Problem.** Standard Flow-GRPO [77] employs a _terminal sparse reward_ mechanism: the complete denoising trajectory ( _xT , xT −_ 1 _, . . . , x_ 0) receives a single scalar score from the reward model _R_ ( _x_ 0 _, c_ ) only at the final generated sample _x_ 0. During training, this terminal reward is uniformly distributed to all intermediate denoising steps, meaning the advantage signal for each step is _A_<sup>ˆ</sup> _t_ = _A_<sup>ˆ</sup> terminal _, ∀t_ . This design introduces two core problems: (1) **signal dilution** —early denoising steps (which determine global structure) and late steps (which refine details) receive identical gradient weights, despite their fundamentally different contributions to final quality; and (2) **exploration** 

3 

Table 1: Representative methods addressing sparse reward in Flow-GRPO. We summarize step-level reward densification, variance-aware sampling, value anchoring, and process-level gradient guidance strategies. 

|**Category**|**Method**|**Core Innovation**|**Key Contribution / Result**|
|---|---|---|---|
|Step-Level Reward<br>Densification|DenseGRPO [23]<br>SuperFlow [15]|ODE-predicted clean sample ˆ_x_<sup>(</sup><sup>_t_)</sup><br>1<br>for step-level reward<br>gain∆_rt_ + reward-aware adaptive stochasticity<br>Variance-aware dynamic group sizing +<br>continuous-time step-level advantage|PickScore 23.1 (vs. 22.5); GenEval 0.74 (vs. 0.71);<br>Improved reward signal granularity<br>1.7%–16.0% improvement over Flow-GRPO;<br>5.4%–56.3% training cost|
|Value Function Anchoring|VGPO [106]|Process-aware value estimation_Vϕ_(_xt, t_)+<br>absolute-value-enhanced group normalization|SOTA on PickScore, HPS v2.1, GenEval; Stabilized<br>advantage estimation|
|Process-Level Reward<br>Guidance|Euphonium [192]|Injecting_∇xtRt_(_xt_)into SDE drift + Dual-Reward<br>GRPO|1.66_×_faster convergence on T2V; Unifies Flow-GRPO<br>and DanceGRPO as special cases|


**inefficiency** —the model cannot distinguish during training which steps’ decisions truly influenced the final reward, resulting in high variance and low signal-to-noise ratio in the policy gradient. We summarize the key optimization strategies developed to address these challenges in Table 1, with detailed descriptions provided below. 

**DenseGRPO: Step-Level Reward Gains.** DenseGRPO [23]is the first method to systematically convert sparse terminal rewards into dense step-level signals. Its core idea exploits the property that flow matching models can predict a clean image _x_ ˆ<sup>(</sup> 1<sup>_t_)</sup> via a single-step ODE prediction at any intermediate timestep _t_ , constructing **step-level reward gains** : 


where _R_ is a pretrained reward model. This increment directly measures the marginal contribution of the denoising decision from timestep _t −_ 1 to _t_ on final quality. Building on this, DenseGRPO further proposes a **Reward-Aware Exploration Calibration** mechanism: for timesteps where _|_ ∆ _rt|_ is large (i.e., critical decision points with significant reward impact), the stochasticity injection strength is adaptively increased as _σ_ adaptive( _t_ ) = _σ_ base _· f_ (∆ _rt, t_ ), guiding the model to invest more exploration at the stages where it matters most. Experiments show that DenseGRPO significantly outperforms the original Flow-GRPO on PickScore [56], HPS v2.1 [155], and GenEval [32] benchmarks, achieving a PickScore of 23.1 (vs. Flow-GRPO’s 22.5) and improving GenEval from 0.71 to 0.74. 

**SuperFlow: Variance-Aware Sampling and Step-Level Advantages.** SuperFlow [15] addresses the sparse reward problem from the perspective of statistical efficiency, proposing two complementary innovations. First, **variance-aware dynamic group sizing** : observing that generation difficulty varies greatly across text prompts—simple prompts yield groups with low reward variance (low information content) while difficult prompts produce high variance—SuperFlow dynamically adjusts group size based on each prompt’s online reward variance Var( _{ri}_<sup>_G_</sup> _i_ =1<sup>), allocating more samples to</sup> high-variance prompts for more precise advantage estimation and fewer to low-variance prompts to save computation. Second, **continuous-time step-level advantage estimation** : a step-level advantage function designed to be naturally consistent with the continuous-time dynamics of flow matching, avoiding biases introduced by discrete step-level approximation. Experiments on SD3.5-Medium show that SuperFlow improves over the SD3.5-M baseline by 4.6%–47.2% across multiple metrics, outperforms Flow-GRPO by 1.7%–16.0%, while using only 5.4%–56.3% of the original training steps, demonstrating exceptional sample efficiency. 

**VGPO: Temporal and Group Value Anchoring.** VGPO (Value-anchored Group Policy Optimization) [106] proposes solving the sparse reward problem from a **value function anchoring** perspective. Standard GRPO’s group-normalized advantage _A_<sup>ˆ</sup> _i_ = ( _ri − µG_ ) _/σG_ only normalizes across the group dimension, ignoring temporal information. VGPO introduces two key improvements: (1) **processaware value estimation** —decomposing sparse terminal rewards through a learned value function _Vϕ_ ( _xt, t_ ) into dense timestep-level signals, giving each timestep an advantage estimate reflecting its long-term value; and (2) **absolute-value-enhanced normalization** —introducing an absolute value 

4 

anchoring term into group normalization to prevent the advantage signal from vanishing when all samples in a group have similar rewards. By organically combining value anchoring across both temporal and group dimensions, VGPO achieves state-of-the-art performance on PickScore, HPS v2.1, and GenEval benchmarks. 

**Euphonium: Process Reward Gradient Guidance.** Euphonium [192] introduces dense signals from an entirely novel angle: directly injecting the gradients of a **Process Reward Model (PRM)** into the SDE drift term of the generation process. Specifically, let _Rt_ ( _xt_ ) be the process reward model at timestep _t_ ; Euphonium modifies the flow matching SDE to: 

_dxt_ = [ _vθ_ ( _xt, t_ ) + _α∇xtRt_ ( _xt_ )] _dt_ + _σ_ ( _t_ ) _dWt,_ (9) 

where _α_ is the guidance strength. This modification injects the reward signal’s gradient as a continuous directional force into the generation flow, so that every denoising step’s direction is guided stepby-step by the reward model rather than receiving feedback only at the terminal state. Theoretical analysis shows that Flow-GRPO [77] and DanceGRPO [162] can be viewed as special cases of Euphonium (corresponding to _α_ = 0 and terminal-only reward, respectively). Combined with the **Dual-Reward GRPO** algorithm—a weighted combination of terminal and process rewards— Euphonium accelerates training convergence by 1.66 _×_ on video generation tasks and achieves state-of-the-art on T2V alignment benchmarks. 

Table 2: Credit assignment strategies for Flow-GRPO: from trajectory-level terminal rewards to structured step-/block-level attribution. 

|**Strategy Type**|**Method**|**Core Mechanism**|**Key Benefit / Result**|
|---|---|---|---|
|Tree / Branch Search|TreeGRPO [24]<br>BranchGRPO [68]|Reconstructs denoising as a search tree; Compares<br>sibling rewards to assign step credit:<br>ˆ_A_<sup>tree</sup><br>_t_<br>=<br>¯_r_children(_t_)_−_¯_r_siblings(_t_)<br>std(_r_siblings(_t_))<br> Flexible on-demand branching at arbitrary timesteps;<br>Depth-wise advantage estimation; Branches adapt to<br>reward variance|2.4_×_training speedup with maintained alignment<br>quality<br>+16% alignment over DanceGRPO; 55% training time<br>reduction; Hybrid variant 4.7_×_speedup|
||Dynamic-<br>TreeRPO [29]|Dynamic noise intensity across tree levels (larger early,<br>smaller late) + LayerTuning-RL (update only selected<br>layers)|+4.9% (HPS v2.1), +5.91% (PickScore), +8.66%<br>(ImageReward);_∼_50% efficiency gain|
|Grouping /<br>Decomposition|Multi-GRPO [91]<br>Chunk-<br>GRPO [87]|Temporal grouping (MCTS-like branching across<br>segments) + reward grouping for multi-objective:<br>ˆ_Ai_ = <sup>�</sup><sup>_K_</sup><br>_k_=1 <sup>_wk_ ˆ</sup><sup>_A_(</sup><sup>_k_)</sup><br>_i_<br>Groups consecutive steps into coherent chunks of<br>length_k_; Chunk-level optimization with shared<br>advantage|Reduces interference from reward scale/variance;<br>Improves multi-objective stability<br>Lower-variance credit estimation while preserving<br>temporal hierarchy|
|Noise Causality &<br>Temporal Awareness|G<sup>2</sup>RPO [196]|Singular stochastic sampling: inject noise only at one<br>random timestep_t_<sup>_∗_</sup>(others ODE); multi-granularity<br>advantage integration across scales:<br>ˆ_A_<sup>multi</sup><br>_i_<br>= <sup>�</sup><br>_s _<sup>_αs_ ˆ</sup><sup>_A_(</sup><sup>_s_)</sup><br>_i_|Strengthens causal link between a specific step’s<br>stochastic decision and terminal reward|
||TempFlow-<br>GRPO [42]|<br><br>Temporal branching to estimate step “process reward”<br>via terminal reward differences; Noise-aware weighting<br>(explore early, exploit late) + seed-grouping by<br>semantic similarity|More temporally fair comparisons and timestep-aware<br>attribution in flow matching|
|Theory-Guided<br>Reweighting|PCPO [59]|Proportionate timestep reweighting: Credit proportional<br>to per-step policy gradient norm|Strong gains over uniform-credit baselines (e.g.,<br>DanceGRPO), especially for long trajectories|


### **3.2 Credit Assignment: From Trajectory to Step Level** 

Credit assignment is a core challenge in reinforcement learning: given a terminal reward for a complete denoising trajectory, how can one accurately determine each intermediate step’s contribution to the final outcome? Standard Flow-GRPO distributes the terminal reward uniformly across all steps, an “egalitarian” approach that ignores the differentiated roles of different timesteps. The methods reviewed in this section achieve more precise step-level credit assignment through various structured strategies. The summary is shown in Table 2, and the details are as follows. 

5 

**TreeGRPO: Tree-Structured Search. TreeGRPO** [24] reconstructs the denoising trajectory as a **search tree structure** , representing a pioneering contribution to credit assignment. The core idea is: at critical branching points in the denoising process, multiple child trajectories are spawned from the same parent node _xt_ , each reaching its own terminal state with an independent terminal reward. By comparing the reward differences among sibling trajectories branching from the same node, credit can be precisely attributed to the decision at the branching point. Specifically, the step-level advantage is computed as: 


where _r_ ¯children( _t_ ) is the mean reward of subtrees rooted at the current node _t_ , and _r_ ¯siblings( _t_ ) is the mean reward of sibling nodes at the same level. The key advantage of this tree structure is that trajectories sharing a common prefix automatically control for confounding variables, so the advantage signal primarily reflects the quality of the decision at the branching point. Experiments show that TreeGRPO achieves **2.4** _×_ **training speedup** while maintaining alignment quality, as more precise credit assignment reduces gradient variance and makes each update step more efficient. 

**Multi-GRPO: Multi-Group Advantage Estimation. Multi-GRPO** [91] extends GRPO’s group normalization along two orthogonal dimensions. First, **temporal grouping** : inspired by Monte Carlo Tree Search (MCTS), branching points are introduced at different time segments of the denoising trajectory, so that trajectories within the same group share decisions in some segments and explore independently in others, enabling isolation of contributions from specific time intervals. Second, **reward grouping** : when multiple reward functions _R_ 1 _, R_ 2 _, . . . , RK_ are used (e.g., aesthetics score, text consistency, safety), group-normalized advantages _A_<sup>ˆ(</sup> _i_<sup>_k_)</sup> are independently computed for each reward function, then aggregated through weighted combination: 


This decomposition prevents mutual interference from different reward scales and variances, enabling the model to more uniformly optimize multiple objectives. 

**G**<sup>2</sup> **RPO: Fine-Grained GRPO. G**<sup>2</sup> **RPO** [196] addresses the weak correlation between noise and rewards in multi-step diffusion denoising, proposing two key techniques. First, **singular stochastic sampling** : at each training iteration, stochastic perturbation is injected at only a single randomly selected timestep _t_<sup>_∗_</sup> , with all other steps using deterministic ODE. This ensures that sampling randomness is entirely concentrated at _t_<sup>_∗_</sup> , establishing a strong causal link between that step’s noise decision and the final reward. Second, **multi-granularity advantage integration** : advantages are estimated separately at different diffusion scales (coarse-grained global structure vs. fine-grained local details) and then aggregated across scales: _A_<sup>ˆmulti</sup> _i_ =<sup>�</sup> _s_<sup>_αsA_ˆ</sup> _i_<sup>(</sup><sup>_s_), where</sup><sup>_αs_are scale weights.</sup> 

**BranchGRPO: Structured Branching. BranchGRPO** [68] restructures GRPO’s rollout process into a **branching tree structure** , converting sparse terminal rewards into step-level signals through “depth-wise advantage estimation.” Unlike TreeGRPO [24], BranchGRPO’s branching strategy is more flexible: it allows branching on demand at any timestep, with the number of branches adaptively adjusted based on the reward variance of that time interval. Experiments show that BranchGRPO improves alignment by 16% over DanceGRPO [162] while reducing training time by 55%. Its hybrid variant (Hybrid BranchGRPO), which shares most of the trajectory and branches only at critical steps, achieves a further **4.7** _×_ **speedup** . 

**TempFlow-GRPO: Temporal Awareness. TempFlow-GRPO** [42] focuses on temporally-aware credit assignment for flow matching models. The method uses **trajectory branching** to create divergence points at different timesteps, estimating each step’s **process reward** by comparing terminal reward differences between branched trajectories. Additionally, TempFlow-GRPO introduces two flow-model-specific designs: (1) **noise-aware weighting** —assigning higher exploration weight to early steps with more noise and higher exploitation weight to later steps with less noise; and (2) **seed group strategy** —grouping initial noise samples _x_ 0 by semantic similarity to ensure fairness of within-group comparisons. 

6 

**Dynamic-TreeRPO: Dynamic Noise Tree Structure. Dynamic-TreeRPO** [29] introduces a **dynamic noise intensity** mechanism into tree-structured search: different levels of the tree (corresponding to different timesteps) use different strengths of stochasticity injection. Early steps (high-noise regions) use larger branching randomness to cover a broader search space, while late steps (low-noise regions) use smaller randomness to refine details. Additionally, Dynamic-TreeRPO combines a **LayerTuning-RL** strategy—applying RL updates only to parameters in specific model layers while freezing the rest—to reduce parameter update volume and prevent overfitting. On the HPS-v2.1, PickScore, and ImageReward benchmarks, it surpasses SOTA by 4.9%, 5.91%, and 8.66% respectively, with approximately 50% training efficiency improvement. 

**Chunk-GRPO: Block-Level Optimization. Chunk-GRPO** [87] observes that the denoising process of flow matching models exhibits natural **temporal coherence** : decisions at adjacent timesteps are highly correlated, and single-step credit assignment may introduce excessive noise. Based on this observation, Chunk-GRPO groups consecutive denoising steps into several coherent “chunks,” each containing _k_ consecutive steps. Policy optimization operates at the chunk level rather than the individual step level, with steps within a chunk sharing the same advantage signal. This design captures the intrinsic temporal dynamics hierarchy of flow matching, reducing advantage estimation variance while maintaining sufficient temporal resolution. 

**PCPO: Proportionate Credit Policy Optimization. PCPO** [59] addresses the credit assignment problem from a theoretical perspective. The method proves that in flow matching RL, the proportional contribution of different timesteps to the final reward should be proportional to the policy gradient norm at that step. Accordingly, PCPO uses a **principled timestep reweighting** mechanism to ensure that the gradient weight each step receives in the policy update strictly reflects its proportional contribution to the reward. Both theoretical analysis and experiments demonstrate that PCPO significantly outperforms uniformly-credited policy gradient baselines such as DanceGRPO, with the advantage being particularly pronounced in long-trajectory (many-step denoising) scenarios. 

Table 3: Sampling efficiency and training acceleration strategies for Flow-GRPO. These methods reduce rollout cost via entropy-aware pruning, sliding windows, noise distribution optimization, forward-process training, distribution-level matching, and preference-based learning. 

|**Acceleration Type**|**Method**|**Core Mechanism**|**Speedup / Key Result**|
|---|---|---|---|
|Entropy /<br>Temporal Pruning|E-GRPO [184]<br>MixGRPO [62]|Identifies high-entropy timesteps via_H_(_t_); Merges<br>low-entropy steps; Group-normalized advantages<br>within merged segments<br>Sliding ODE–SDE window[_tw, tw_ +_W_]; SDE only<br>inside window; ODE elsewhere|Reduced SDE computation; Improved signal-to-noise<br>ratio<br>MixGRPO-Flash: 71% time reduction with maintained<br>alignment|
|Sampling Distribution<br>Optimization|Smart-<br>GRPO [174]<br>Pro-GRPO [31]|Iteratively reweights initial noise distribution based on<br>reward feedback<br>Expand-and-Prune: Increase_G_<sup>_′_</sup>, diversity pruning,<br>multi-step OVF|More efficient exploration; Avoids low-reward regions<br>Mitigates reward clustering; Higher signal variance<br>utilization|
|Forward /<br>Matching-Based RL|DiffusionNFT [19<br>AWM [161]<br>DGPO [88]|0]Online RL on forward noising process; Contrastive<br>positive/negative flow matching<br>Advantage-weighted flow matching:<br>_LAW M_ = <sup>ˆ</sup>_Ai∥vθ −_target_∥_<sup>2</sup><br>Direct group preference optimization (DPO-style);<br>Deterministic ODE sampling|25_×_speedup; GenEval 0.24_→_0.98 in 1k steps<br>24_×_speedup; No SDE rollouts; Simplified training<br>_∼_20_×_faster training; Removes policy gradient<br>overhead|
|Design Space Analysis|GRPO-ELBO-<br>ODE [20]|Factorized RL design space: Objective, likelihood<br>estimator, sampler; ELBO shown dominant|4.6_×_efficiency gain; GenEval 0.24_→_0.95 (90 GPU<br>hours)|


### **3.3 Sampling Efficiency and Training Acceleration** 

The primary computational bottleneck of Flow-GRPO is that each policy update requires generating _G_ complete denoising trajectories (rollouts), each containing _T_ denoising steps, with each step requiring a full model forward pass. For large-scale models (such as SD3.5-Medium with 2B+ parameters), the cost of a single training iteration is extremely high. The methods reviewed in this 

7 

section significantly reduce training cost from different angles, achieving up to 25 _×_ speedup. The summary is shown in Table 3, and the details are as follows. 

**E-GRPO: High-Entropy Step Driven. E-GRPO** [184] observes that not all steps in a denoising trajectory have equal influence on the final result—most steps’ decisions are nearly deterministic (low entropy), with only a few steps exhibiting genuine uncertainty (high entropy). E-GRPO computes the policy entropy at each timestep _H_ ( _t_ ) = _−_ E[log _πθ_ ( _at|st_ )], merges consecutive low-entropy steps into equivalent high-entropy SDE steps for optimization, and uses efficient deterministic ODE sampling for the remaining steps. Additionally, E-GRPO employs **multi-step group-normalized advantages** — normalizing within merged high-entropy step groups rather than across the full trajectory—to improve the signal-to-noise ratio. 

**MixGRPO: Mixed ODE-SDE Sliding Window. MixGRPO** [62] proposes an elegant **sliding window** strategy: SDE + GRPO policy optimization is applied only within a moving window [ _tw, tw_ + _W_ ], while regions outside the window use deterministic ODE with high-order solvers (such as DPM-Solver++ [84]) for efficient sampling. The window slides along the time axis during training, ensuring all timesteps are eventually covered. The core insight is that at any given training step, the model only needs to learn improvements within the current window, while steps outside the window can “freely” use the already-learned policy. Its accelerated variant **MixGRPO-Flash** further narrows the window width and uses more aggressive ODE step sizes, reducing training time by **71%** while maintaining alignment quality comparable to full SDE training. 

**Smart-GRPO: Intelligent Noise Sampling. Smart-GRPO** [174] is the first method to directly optimize the **initial noise distribution** in flow matching RL. Standard approaches uniformly sample initial noise from _x_ 0 _∼N_ (0 _, I_ ), but most initial noise samples may lead to low-reward regions, wasting computation. Smart-GRPO refines the noise sampling distribution through an iterative search process: after each training round, noise sampling weights are updated based on final reward feedback for each initial noise, biasing subsequent sampling toward high-reward regions. This approach does not modify the denoising process itself but optimizes the starting point of exploration. 

**Pro-GRPO: Expand and Prune. Pro-GRPO** [31] discovers that Flow-GRPO training suffers from severe **reward clustering** : the _G_ samples for a given prompt tend to cluster in a narrow region of reward space, resulting in extremely small advantage signal variance after group normalization, rendering policy gradients near zero. To address this, Pro-GRPO proposes an “Expand-and-Prune” three-stage strategy: (1) **Expand** —increase the initial sampling count to _G_<sup>_′_</sup> _≫ G_ to cover a broader reward space; (2) **Prune** —prune samples based on latent-space feature diversity metrics, retaining the most representative _G_ samples; (3) **Multi-step OVF (Online Value Function)** —execute multi-step policy optimization on retained samples to maximize information utilization from each sample. 

**DiffusionNFT: Forward-Process Online RL. DiffusionNFT** (Noise-Free Training) [190] proposes a fundamentally different training paradigm: rather than optimizing on the reverse denoising process, it performs online RL directly on the **forward noising process** via the flow matching loss. Specifically, DiffusionNFT first generates a batch of complete samples, divides them into positive (high-reward) and negative (low-reward) examples, then uses a contrastive learning objective—increasing the flow matching likelihood of positive examples and decreasing that of negative examples—to update the model. By avoiding complete SDE rollouts and per-step policy gradient computation, DiffusionNFT is **25** _×_ **more efficient** than Flow-GRPO. Within only 1,000 training steps, it improves SD3.5-Medium’s GenEval score from 0.24 to 0.98, demonstrating remarkable sample efficiency. 

**AWM: Advantage Weighted Matching. AWM** [161] establishes a theoretical connection between DDPO [4] and flow matching [73]. The authors prove that DDPO’s policy gradient objective is mathematically equivalent to an implicit score/flow matching loss with noisy targets. Based on this insight, AWM proposes directly using the **same flow matching loss as pretraining** , but reweighted by sample-level advantage _A_<sup>ˆ</sup> _i_ : 


This design completely avoids SDE rollouts, per-step log-likelihood computation, and importance ratio clipping, simplifying the training process to “weighted fine-tuning.” On SD 3.5 Medium and 

8 

FLUX, AWM achieves a **24** _×_ **speedup** over Flow-GRPO while reaching comparable or superior alignment quality. 

**DGPO: Direct Group Preference Optimization. DGPO** [88] takes an even more radical approach: **completely abandoning the policy gradient framework** . DGPO does not compute importance ratios, does not clip, and does not perform per-step gradient backpropagation. Instead, it learns directly from group-level preference relations—for each group of _G_ samples, DGPO constructs pairwise preference comparisons, then uses a DPO-like objective to directly optimize the flow matching model’s parameters. The key advantage of this design is that it unlocks **deterministic ODE samplers** —no longer requiring SDE stochasticity to define the policy distribution. Since ODE sampling is several times faster than SDE and supports high-order solvers, DGPO’s overall training speed is approximately **20** _×_ that of existing methods. 

**Systematic Analysis of the RL Design Space. GRPO-ELBO-ODE** [20] conduct the first systematic ablation study of the design space for RL fine-tuning of diffusion/flow matching models. They decompose the design space into three orthogonal factors: (1) **policy gradient objective** (REINFORCE [115], PPO-clip [103], GRPO [107], etc.); (2) **likelihood estimator** (per-step log-likelihood, ELBO, score matching, etc.); (3) **rollout sampling scheme** (full SDE, mixed ODE-SDE, pure ODE, etc.). Through exhaustive experiments, they reach a surprising conclusion: **the ELBO likelihood estimator is the overwhelmingly dominant factor** —configurations using ELBO significantly outperform per-step log-likelihood under nearly all policy gradient objective and sampling scheme combinations. Based on this finding, they achieve GenEval improvement from 0.24 to 0.95 on SD 3.5 Medium in only 90 GPU hours, **4.6** _×_ more efficient than Flow-GRPO. 

Table 4: Mode collapse mitigation and diversity preservation strategies in GRPO / Flow-GRPO alignment. These methods address reward-induced preference collapse via distribution-level regularization, orthogonal perturbation, reward reshaping, directional decoupling, and identity-aware diversity optimization. 

|**Category**|**Method**|**Core Idea**|**Key Results**|
|---|---|---|---|
|Distribution-Level<br>Regularization|DiverseGRPO [74<br>DRIFT [76]|] Spectral clustering in CLIP space; Exploration reward<br>_r_<sup>div</sup><br>_i_<br>=_ri_+_λ/|Ci|_; Early-step stronger KL to prevent<br>structural collapse<br>Reward-concentrated sampling; Stochastic prompt<br>perturbation; Potential-based shaping<br>Φ(_st_+1)_−γ_Φ(_st_)|+13%–18% Vendi diversity without quality drop<br>+9–43% diversity at equal alignment; Pareto-dominant<br>trade-off|
|Orthogonal Perturbation|OSCAR [152]|Inject stochastic noise orthogonal to generation flow in<br>latent space; Monotonic increase of distribution volume<br>proxy|Training-free diversity boost; No alignment degradation|
|Bias Direction<br>Decoupling|D<sup>2</sup>-Align [7]|Identify bias direction in reward embedding space;<br>Remove preference bias via lightweight correction<br>module; Introduces DivGenBench benchmark|Significant mitigation of preference mode collapse|
|Identity Diversity|DisCo [5]|RL with compositional reward; Pairwise facial<br>similarity penalty across subjects|98.6% Unique Face Accuracy (vs. <50% baseline)|


### **3.4 Mode Collapse and Diversity Preservation** 

GRPO [107]/Flow-GRPO [77] alignment training faces a fundamental tension: reward models typically exhibit **inherent preference biases** —favoring certain specific styles, compositions, or color schemes with higher scores. When models are repeatedly optimized to maximize these preference scores, their outputs gradually converge to the narrow modes preferred by the reward model, causing **mode collapse** or **preference mode collapse** . The methods in this section address this problem from the perspectives of distributional regularization, orthogonal perturbation, and reward reshaping. The summary is shown in Table 4, and the details are as follows. 

**DiverseGRPO: Distributional Creativity Rewards. DiverseGRPO** [74] is the first method to design diversity rewards from a **distributional level** (rather than sample level). Standard GRPO 

9 

computes rewards and advantages only at the sample level, completely ignoring the overall distributional characteristics of the generated sample set for a given prompt. DiverseGRPO introduces two key techniques: First, **semantically-grouped distributional representation** : for the _G_ generated samples of a given prompt, spectral clustering is performed in CLIP embedding space, dividing samples into _M_ semantic clusters _C_ 1 _, C_ 2 _, . . . , CM_ . An **exploration reward** inversely proportional to cluster size is then added to each sample: _ri_<sup>diverse</sup> = _ri_ + _λ/|Ci|_ . This means samples falling into rare clusters (small _|Ci|_ ) receive higher reward bonuses, incentivizing the model to explore underrepresented semantic regions. Second, **structure-aware early regularization** : stronger KL divergence regularization is applied during early denoising steps (the phase determining global structure and layout) to prevent premature policy collapse, while regularization is relaxed during late steps (the detail refinement phase) to allow quality improvement. Experiments demonstrate that DiverseGRPO improves semantic diversity (Vendi Score) by 13%–18% while matching quality. 

**OSCAR: Orthogonal Stochastic Control. OSCAR** (Orthogonal Stochastic Control for Alignment Rewards) [152] proposes an elegant training-free diversity enhancement method from a differential geometry perspective. The core observation is: in the latent space of flow matching, variations along the generation flow direction affect image quality/alignment, while variations **orthogonal to the generation flow** affect only diversity without changing quality. OSCAR accordingly injects **stochastic perturbations orthogonal to the generation flow direction** during denoising, operating in feature space rather than pixel space. Theoretical analysis proves that this perturbation monotonically increases a volume proxy metric (i.e., the coverage of the generated distribution) without degrading alignment quality. 

**DRIFT: Beyond the Dirac Delta. DRIFT** [76]—whose name hints at its goal of broadening the Dirac-delta-like narrow distributions of RL-aligned model outputs to cover a wider range of modes— proposes three complementary mechanisms: (1) **reward-concentrated sampling** —concentrating sampling in high-density regions of reward space rather than extreme-value regions, avoiding domination by a few extremely high-scoring samples; (2) **stochastic prompt variation** —applying slight random perturbations to text prompts during training to prevent the model from overfitting to specific prompt formats; (3) **potential-based reward shaping** —overlaying a shaping term based on a potential function Φ( _st_ +1) _−γ_ Φ( _st_ ) on the original reward, where the potential function reflects state space coverage. The three mechanisms work synergistically, achieving **9–43% diversity improvement** at equivalent alignment, and 60–66% alignment improvement at equivalent diversity, exhibiting Pareto dominance. 

**Taming Preference Mode Collapse. D**<sup>2</sup> **-Align** [7] proposes a novel **directional decoupling** method to combat preference mode collapse. The core insight is that reward model biases can be represented in its embedding space as a **bias direction vector** —all high-scoring samples tend to cluster along this direction in embedding space. D<sup>2</sup> -Align learns a lightweight directional correction module that, without modifying the reward model itself, removes the bias direction component from the embedding space, so that the corrected reward signal reflects only genuine quality rather than stylistic preferences. The method also proposes **DivGenBench** —the first benchmark specifically designed to evaluate preference mode collapse. 

**DisCo: Multi-Human Identity Diversity. DisCo** (Diversity in Social Context) [5] addresses a specific but important diversity problem: **identity diversity** in multi-human T2I generation. When prompts request generating multiple people, existing models tend to produce characters with highly similar facial features (the “clone face” problem). DisCo is the first framework to directly optimize identity diversity via RL, designing a **compositional reward function** that performs pairwise facial feature comparison across all faces in the generated image, penalizing excessive facial similarity. On the DiverseHumans benchmark, DisCo achieves **98.6% Unique Face Accuracy** , a qualitative leap from the baseline’s below 50%. 

### **3.5 Reward Hacking Mitigation** 

**Reward hacking** refers to models learning to exploit reward model vulnerabilities or biases to obtain high scores without genuinely improving generation quality. In RL alignment of diffusion/flow matching models, this manifests as: reward scores continue rising during late training while actual generation quality degrades—artifacts appear, colors become oversaturated, and style becomes 

10 

Table 5: Reward hacking mitigation strategies in GRPO / Flow-GRPO alignment. These methods address reward exploitation via regulated clipping, uncertainty-aware penalization, data anchoring, sampler redesign, artifact detection, reward model robustness, and offline correction. 

|**Mitigation Strategy**|**Method**|**Core Idea**|**Key Result / Contribution**|
|---|---|---|---|
|Clipping Stabilization|GRPO-<br>Guard [136]|Ratio normalization ˜_ρi_ =_ρi/_¯_ρ_; Gradient reweighting<br>for asymmetric importance shift|Stabilizes PPO clipping; Prevents ratio collapse|
|Uncertainty &<br>Diversity Regularization|GARDO [40]<br>ConsistentRFT [11|Penalize high-uncertainty reward outputs; EMA<br>reference update; Diversity-amplified reward<br>8]Multi-granularity rollout (DGR); Consistent policy<br>gradient optimization (CPGO)|Reduces blind-spot exploitation; Improves stability<br>-49% perceptual hallucination; -38% semantic<br>hallucination|
|Data Anchoring|DDRL [168]|Forward KL regularization_D_KL(_p_data_∥πθ_)|Industrial-scale validation; Prevents forgetting data<br>modes|
|Reward Model Analysis<br>& Robustification|ArtifactReward [46<br>SoliReward [71]|]Typology of hacking (over-stylization vs. deformation);<br>Artifact-aware auxiliary reward<br>Single-item binary labeling; Cross-prompt pairing;<br>Hierarchical progressive query attention|First systematic categorization of T2I reward hacking<br>Robust video reward modeling under noisy labels|
|Sampler Redesign|CPS [129]|Coefficients-preserving SDE sampler; Noise–signal<br>conservation constraints|Reduces stochastic artifact exploitation; More stable<br>convergence|
|Offline Correction|GDRO [140]|Fully offline training; Corrected evaluation score via<br>importance sampling|Avoids online hacking amplification; Stable rectified<br>flow alignment|


monotonous. This section reviews various mitigation strategies. The summary is shown in Table 5, and the details are as follows. 

**GRPO-Guard: Regulated Clipping. GRPO-Guard** [136] first systematically diagnoses the failure of PPO’s clipping mechanism in Flow-GRPO. By analyzing the distributional changes of the importance ratio _ρi_ = _πθ_ ( _oi|c_ ) _/π_ ref( _oi|c_ ) throughout training, the authors discover that as training progresses, the distribution of _ρi_ exhibits a **systematic left-shift** —the mean persistently falls below 1. This means the probability of most model outputs decreases relative to the reference policy, while PPO clipping is designed only for the symmetric interval [1 _− ϵ,_ 1 + _ϵ_ ] and cannot effectively handle this asymmetric shift. GRPO-Guard proposes two fixes: (1) **ratio normalization** —normalizing _ρi_ to _ρ_ ˜ _i_ = _ρi/ρ_ ¯, re-centering the clipping interval at the distribution mean; (2) **gradient reweighting** — adjusting gradient weights based on the degree of _ρi_ ’s deviation from 1, preventing extreme ratios from dominating update directions. 

**GARDO: Gated Adaptive Regularization. GARDO** (Gated Adaptive Regularized Diffusion Optimization) [40] mitigates reward hacking from an **uncertainty-aware** perspective. The core idea is that reward hacking often occurs in input regions where the reward model has high uncertainty— the model learns to generate samples in these “blind spots” to obtain inflated scores. GARDO introduces three techniques: (1) **selective penalization** —imposing additional penalties on samples with high reward model output uncertainty, discouraging the model from drifting toward uncertain regions; (2) **adaptive reference model update** —progressively updating the reference model _π_ ref via exponential moving average rather than using a fixed reference, allowing the KL divergence constraint to dynamically adjust with training; (3) **diversity-amplified reward** —overlaying a reward term reflecting within-batch diversity onto the original reward, constraining model behavior along the diversity dimension. 

**DDRL: Data-Regularized RL. DDRL** (Data-regularized Diffusion RL) [168] proposes a reward hacking mitigation approach validated both theoretically and at industrial scale. The core idea is to anchor the policy to the offline data distribution using **forward KL divergence** : 


Unlike the standard reverse KL ( _D_ KL( _πθ∥π_ ref)), forward KL penalizes the policy for assigning low probability in high-density regions of the data distribution, preventing the model from “forgetting” 

11 

common patterns in real data. DDRL has been validated in **over 1 million GPU hours** of industrialscale experiments and **10,000 human evaluations** , demonstrating that data regularization is critical for preventing reward hacking in large-scale training. 

**ConsistentRFT: Reducing Visual Hallucinations. ConsistentRFT** [118] treats reward hacking as a form of **visual hallucination** : the model generates content that appears plausible but is semantically inconsistent with the prompt. The method proposes two techniques: (1) **Dynamic Granularity Rollout (DGR)** —simultaneously using rollouts at different resolutions/granularities within a single training iteration, with coarse granularity capturing global semantics and fine granularity focusing on local details, complementing each other to avoid blind spots of any single granularity; (2) **Consistent Policy Gradient Optimization (CPGO)** —enforcing consistency of policy update directions across steps in the multi-step denoising process, preventing contradictory gradients from different steps from causing instability. Experiments show that ConsistentRFT reduces low-level perceptual hallucinations (e.g., artifacts, deformations) by 49% and high-level semantic hallucinations (e.g., missing objects, incorrect attributes) by 38%. 

**Understanding Reward Hacking in T2I RL. ArtifactReward** [46] conduct the first systematic typological study of reward hacking. Through separate analysis of aesthetic/preference rewards (such as HPS, PickScore) and prompt consistency rewards (such as CLIP Score, VQA-based), they find that: aesthetic reward hacking manifests as **over-stylization** (e.g., oversaturated colors, extreme contrast), while consistency reward hacking manifests as **object deformation** (e.g., distorting text to improve OCR scores). Based on these findings, the authors propose a **lightweight adaptive artifact reward model** as a regularizer, specifically designed to detect common artifact types in the RL alignment process. 

**CPS: Coefficients-Preserving Sampling. CPS** [129] traces the root cause of reward hacking to **sampler design** . Through theoretical analysis, the authors prove that excessive stochasticity in SDE sampling introduces noise artifacts in generated images, which may be misinterpreted by reward models as beneficial features (e.g., “texture detail”), leading to reward hacking. Inspired by DDIM [112], CPS designs a **coefficients-preserving sampler** that eliminates artifact-producing excessive stochasticity while preserving the randomness needed for SDE exploration. Specifically, CPS ensures that signal and noise coefficients in the sampling process satisfy specific conservation relations, thereby guaranteeing sampling quality. Experiments show CPS achieves more accurate reward modeling and more stable training convergence. 

**SoliReward: Robust Video Reward Model. SoliReward** [71] prevents reward hacking from the perspective of **reward model training** . Training data for video reward models typically contains substantial labeling noise (different annotators having inconsistent preferences for the same video pair), which causes reward models to learn superficial shortcuts. SoliReward proposes two techniques to combat labeling noise: (1) **single-item binary annotation** —converting traditional pairwise comparison labels into independent quality assessments of individual videos, reducing the subjective bias of pairwise labeling; (2) **cross-prompt pairing** —pairing videos from different prompts to construct preference pairs, forcing the reward model to learn universal quality features rather than prompt-specific surface patterns. Additionally, **Hierarchical Progressive Query Attention** enhances the spatiotemporal consistency of video feature aggregation. 

**GDRO: Offline Group-Level Direct Reward Optimization. GDRO** [140] proposes a **fully offline** training method, fundamentally circumventing the amplification of reward hacking in online rollouts. Designed for rectified flow diffusion models, GDRO trains on pre-generated offline datasets without requiring online image rollouts. To address the distributional shift problem of reward scores in offline training, GDRO introduces a **corrected evaluation score** , using importance sampling weighting to correct the offline data’s reward distribution to the expected distribution under the current policy. 

### **3.6 ODE vs. SDE: Sampling Strategies** 

Flow-GRPO’s conversion from ODE to SDE introduces a fundamental design choice: how much stochasticity should the sampling process use? SDE (high stochasticity) provides better exploration but introduces noise artifacts and additional computation; ODE (zero stochasticity) is efficient and quality-stable but lacks exploratory diversity. This section reviews different design choices across 

12 

Table 6: ODE–SDE sampling spectrum in Flow-GRPO alignment. Methods explore different stochasticity regimes ranging from pure ODE (zero noise) to structured SDE and amortized stochastic flow maps, with corresponding theoretical insights. 

|**Stochasticity Regime**|**Method**|**Core Idea**|**Key Contribution**|
|---|---|---|---|
|Pure ODE|Neighbor<br>GRPO [39]|Deterministic ODE sampling; Diversity from perturbed<br>initial noise_x_<sup>(</sup><sup>_i_)</sup><br>0<br>=_x_0+_δi_; Softmax distance proxy<br>for policy gradient|Efficient; No noise artifacts; ODE-compatible<br>high-order solvers|
|Few-Step Annealed Noise|TAFS-<br>GRPO [178]|Adaptive temporal noise injection with annealed<br>temperature_τ_(_k_); Step-aware advantage weighting|Efficient RL alignment for 1–4 step generation|
|Structured<br>Stochastic Flows|GLASS<br>Flows [45]<br>Diamond<br>Maps [44]|Transition kernel_p_(_xt_+∆_t|xt_)modeled via auxiliary<br>flow matching; Structured stochasticity instead of<br>Gaussian noise; Feynman-Kac steering<br>Amortized stochastic flow map(_x_0_, z_)_�→x_1; Distilled<br>from GLASS Flows|Improved inference-time scaling; Coherent exploration<br>Single-step stochastic sampling; Reward-adaptive<br>inference|
|Theoretical Analysis|SDE–ODE<br>Reward<br>Gap [109]|Reward gap bounds under gDDIM; High-stochasticity<br>training improves ODE inference; Optimal stochasticity<br>level characterization|First formal theory of SDE–ODE reward gap|


this spectrum and their theoretical underpinnings. The summary is shown in Table 6, and the details are as follows. 

**Neighbor GRPO: Pure ODE Contrastive Optimization. Neighbor GRPO** [39] completely **bypasses SDE** , achieving policy optimization within a pure ODE sampling framework. The core idea is: diversity need not come from SDE’s per-step stochasticity, but can instead come from **variations in initial noise** . Specifically, for a given prompt _c_ , Neighbor GRPO generates a set of candidate trajectories by sampling multiple perturbed versions within the neighborhood of the initial noise _x_ 0: _x_<sup>(</sup> 0<sup>_i_)</sup> = _x_ 0 + _δi_ (where _δi_ are small Gaussian perturbations). Since each trajectory uses deterministic ODE sampling, the entire process is efficient and free of noise artifacts. Policy optimization is achieved through a **softmax distance proxy** —rather than directly computing SDE log-likelihoods, it uses distance relations between terminal samples of candidate trajectories to construct soft labels. The authors prove the theoretical connection between this proxy and the true policy gradient. Neighbor GRPO preserves all advantages of ODE: efficient sampling, high-order solver compatibility, and no noise artifacts. 

**TAFS-GRPO: Temperature-Annealed Few-Step Sampling. TAFS-GRPO** [178] focuses on **fewstep generation** scenarios (e.g., 1–4 steps), where standard SDE multi-step stochasticity injection is infeasible. TAFS-GRPO’s strategy is: **iteratively inject adaptive temporal noise** on single-step or few-step generated samples. Specifically, given a single-step deterministic sample _x_ ˆ1, TAFSGRPO adds noise with an annealing temperature _τ_ ( _k_ ) (decreasing with iteration _k_ ) to _x_ ˆ1 then re-denoises, generating diversified candidate samples. Combined with **step-aware advantage** — adjusting advantage weights based on the timestep and strength of injected noise—it achieves efficient alignment for few-step T2I generation. 

**GLASS Flows: Transition Sampling. GLASS Flows** (Generalized LAyer-wise Stochastic Sampling for Flows) [45] introduces an entirely new sampling paradigm: **“flow matching within flow matching.”** Standard SDE injects independent Gaussian noise at each discrete timestep, but this independent noise may disrupt the coherent structure learned by flow matching. The core idea of GLASS Flows is: the Markov transition _p_ ( _xt_ +∆ _t|xt_ ) between discrete timesteps is itself modeled as a small flow matching problem—using an auxiliary flow matching model to sample the conditional distribution _p_ ( _xt_ +∆ _t|xt_ ) rather than simple Gaussian noise. This maintains ODE’s structural efficiency while introducing more structured stochasticity than simple Gaussian noise. Combined with **Feynman-Kac Steering** [110]—using importance sampling to bias the transition kernel toward high-reward regions—GLASS Flows achieves state-of-the-art inference-time scaling performance. 

13 

**Diamond Maps: Stochastic Flow Maps. Diamond Maps** [44] goes further than GLASS Flows by **amortizing the multi-step simulation into a single-step stochastic flow map sampler** . Specifically, Diamond Maps learns a mapping ( _x_ 0 _, z_ ) _�→ x_ 1 (where _z_ is an auxiliary random variable) such that the output distribution of this single-step mapping matches the output distribution of the complete multi-step GLASS Flow. Learning is achieved through GLASS Flows distillation. The key advantage is: at inference time, only a single forward pass is needed to obtain a stochastic generated sample, while preserving the exploration capability needed for alignment. This enables Diamond Maps to **rapidly adapt to arbitrary reward functions at inference time with minimal cost** —simply by changing the sampling strategy for the random variable _z_ , generation can be steered toward different reward directions. 

**Theoretical Analysis of Sampler Stochasticity. SDE–ODE Reward Gap** [109] provide the first rigorous **theoretical characterization** of the reward gap between SDE training and ODE inference. Specific contributions include: (1) proving that under the gDDIM (generalized DDIM) [183] framework, arbitrary different stochasticity levels can be used at training and inference time, with corresponding reward gap upper bounds; (2) proving a counterintuitive result: **higher-stochasticity SDE training can actually improve the quality of low/zero-stochasticity ODE inference** —intuitively, high-stochasticity SDE explores a broader policy space during training, enabling the learned policy to select high-quality deterministic paths during ODE inference; (3) providing theoretical guidance on the optimal training stochasticity level—it should not be increased indefinitely but has an optimal point related to model capacity and reward complexity. 

Table 7: Reward model designs for GRPO-aligned generative models. Methods range from lightweight task-specific reward signals to large-scale generative reward models with reasoning capability. 

|**Category**|**Model**|**Core Design**|**Key Contribution**|
|---|---|---|---|
|Lightweight /<br>Task-Specific|HuDA [1]<br>RealGen [169]|Human detector confidence + temporal prompt<br>alignment<br>Detector-guided artifact reward (reverse-use of<br>synthetic image detector)|73% human win rate vs. Wan 2.1 baseline<br>Label-free photorealism alignment|
|Generative<br>Reward Paradigm|RewardDance [151<br>OneReward [34]|]Large-scale generative reward (up to 26B); Natural<br>language reasoning before scoring<br>Unified VLM generative reward for<br>generation/editing/SR|Strong reward hacking resistance<br>Multi-task winner–loser discrimination|
|Structured /<br>Granular Feedback|VR-<br>Thinker [138]<br>REACT [144]<br>ImageDoctor [37]|CoT-style structured visual reasoning before scoring<br>Frame-level structural distortion evaluation<br>(SFT+GRPO)<br>Pixel-level heatmap reward signals|80.5% accuracy on video preference benchmarks<br>Fine-grained video feedback<br>Spatially dense defect localization|
|Personalized /<br>Domain-Specific|UnifiedReward-<br>Flex [145]<br>EditScore [86]|Context-adaptive reasoning; hierarchical evaluation<br>7B–72B editing reward models|Subjective preference modeling<br>Matches/surpasses GPT-5-level editing evaluation|


### **3.7 Reward Model Design and Evaluation Benchmarks** 

The effectiveness of GRPO alignment critically depends on reward signal quality. An ideal reward model should accurately reflect human preferences, provide fine-grained feedback, and be robust to adversarial manipulation. Meanwhile, standardized evaluation benchmarks are essential for fair comparison of different methods. This section reviews important advances in both reward model design and evaluation benchmarks. The summary is shown in Table 7, and the details are as follows. 

**Reward Models.** Recent work on reward models for GRPO-aligned generation spans a wide spectrum from lightweight task-specific designs to large-scale generative paradigms. At one extreme, **HuDA** [1] demonstrates that an extremely simple reward model—composed only of human detector confidence scores and temporal prompt alignment scores—can achieve a 73% human evaluation win rate against the Wan 2.1 baseline in video generation GRPO post-training, suggesting that carefully 

14 

designed lightweight signals may outperform complex general-purpose reward models for specific tasks. At the other extreme, **RewardDance** [151] proposes a scalable generative reward paradigm supporting simultaneous scaling along model size (up to 26B) and context (incorporating CoT reasoning chains), with the key finding that generative reward models—which output natural language evaluations before converting to scores—are naturally more resistant to reward hacking than discriminative counterparts. Between these extremes, several models target specific feedback granularities: **VR-Thinker** [138], a 7B-parameter “visual thinking” video reward model, first generates structured visual analysis reasoning (similar to Chain-of-Thought) before producing final scores, achieving open-source SOTA (80.5% accuracy) on video preference benchmarks; **REACT** [144] specializes in frame-level structural distortion evaluation for video generation through SFT+GRPO two-stage training, providing finer-grained feedback than video-level rewards; and **ImageDoctor** [37] provides pixel-level heatmaps as dense reward signals, enabling spatial quality/defect information to directly feed back into the denoising process. On the personalization front, **UnifiedReward-Flex** [145] combines context-adaptive reasoning with multi-dimensional hierarchical evaluation to accommodate the inherently subjective nature of human preferences. For domain-specific applications, **EditScore** [86] releases a 7B–72B series of image editing reward models matching or surpassing GPT-5 level, **RealGen** [169] proposes detector-guided rewards that “reverse-use” pretrained synthetic image detectors to quantify AI artifacts without human labeling, and **OneReward** [34] provides a unified VLM generative reward model capable of accurately distinguishing winners from losers across multiple tasks including generation, editing, and super-resolution. 

**Evaluation Benchmarks.** Several unified evaluation benchmarks have been proposed for generative models. SpatialGenEval [146] is the first benchmark focused on spatial intelligence for text-to-image tasks, containing 1,230 spatial reasoning prompts covering relative positions, occlusion relations, perspective and other relations across 25 scenes. UniGenBench++ [142] provides a comprehensive suite of 600 prompts spanning 5 themes, 20 subthemes and 27 evaluation criteria, aiming to assess all key dimensions of T2I evaluation. T2AV-Compass [6] is a unified framework for text-to-audio-video generation, containing 500 prompts and simultaneously evaluating both visual quality and audio consistency. MagicBench [134] offers a 340K-item human-annotated dataset of fine-grained artifacts, with detailed annotations for artifact type, location and severity. DivGenBench [7] specifically measures preference mode collapse by evaluating semantic diversity across multiple generations for the same prompt, while RealBench [53] focuses on automated photorealistic quality assessment using synthetic image detectors as the main measurement tool. 

## **4 Extensions to Generative Tasks** 

### **4.1 Text-to-Image Generation** 

Text-to-image (T2I) generation is the broadest and most method-rich application domain of FlowGRPO. This section systematically reviews progress across multiple sub-directions including reasoning-enhanced generation, multi-objective alignment, text rendering, identity preservation, photorealism, compositional reasoning, few-step generation, adversarial rewards, and test-time scaling. The summary is shown in Table 8, and the details are as follows. 

**Core Alignment Methods.** Recent extensions of Flow-GRPO progressively move beyond pure rollout-based reward optimization and incorporate explicit reasoning modules, prompt refinement mechanisms, agent-based coordination, and lightweight alignment strategies into the flow reinforcement learning loop, reflecting a shift from trajectory-level optimization toward structured multi-module co-optimization. At the input level, **PromptRL** [131] introduces a new paradigm that integrates a **trainable language model as a prompt optimization agent** into the flow RL loop, based on the insight that generation quality depends not only on the diffusion model but also on the quality of the input prompt; it jointly optimizes a lightweight LM that rewrites user prompts together with the diffusion model, with reward signals backpropagated to both modules simultaneously, forming an end-to-end co-optimization strategy that achieves **0.97 GenEval, 0.98 OCR accuracy, and 24.05 PickScore** , while halving rollout requirements because improved prompts make each rollout more informative. Moving beyond prompt rewriting, **Think-Then-Generate (T2G)** [57] decouples reasoning and generation into two stages, where an LLM encoder first performs **reasoning rewriting** —analyzing spatial relationships, quantity requirements, and attribute 

15 

Table 8: Representative extensions of Flow-GRPO in text-to-image generation. We categorize existing works into reasoning augmentation, multi-objective alignment, structural controllability, distribution <u>preservation, adversarial rewards, test-time scaling, and advanced preference modeling.</u> 

|**Category**|**Method**|**Core Innovation**|**Key Contribution / Result**|
|---|---|---|---|
||PromptRL [131]|Trainable LM as prompt optimizer within RL loop|End-to-end co-optimization; 0.97 GenEval; 50%<br>fewer rollouts|
|Reasoning-Augmented<br>|Think-Then-<br>Generate [57]|Two-stage reasoning + generation|Dual-GRPO optimization of reasoner and generator|
|Alignment|<br>ThinkGen [52]<br>Unified Thinker [195]<br>CoF-T2I [125]<br>AgentComp [179]<br>Alignment of DM &<br>FM [99]|Think-driven structured visual planning<br>Fully decoupled reasoning engine<br>Chain-of-Frame visual reasoning<br>Agent-based compositional data construction<br>Lightweight alignment schemes|SepGRPO alternating optimization for stability<br>Task-agnostic reasoning across T2I/editing/SR<br>Progressive scene construction via intermediate<br>frames<br>Tool-use-based preference supervision<br>60% compute reduction via guidance/schedule<br>tuning|
|Multi-Objective<br>Alignment|APEX [9]<br>MapReduce LoRA [8]|Dual-stage reward normalization<br>Modular preference factorization|Mitigates variance hijacking and gradient conflict<br>Map–Reduce LoRA experts + controllable test-time<br>merging|
|Text Rendering &<br>Long Text|DCText [111]<br>Ovis-Image [132]<br>Qwen-Image [150]|Training-free region disentanglement<br>Text-centric pretraining pipeline<br>Paragraph-level curriculum learning|Divide-and-conquer attention masking<br>Strong bilingual OCR at moderate scale<br>Improved long-text semantic control|
|Identity Preservation|PSR [139]<br>MultiCrafter [154]<br>Customized-GRPO [48]|Pairwise subject-consistency reward<br>Disentangled identity attention<br>Synergy-aware reward shaping|Relational identity optimization<br>Reduced multi-subject interference<br>Time-aware dynamic weighting strategy|
|Photorealism|RealGen [169]<br>ProxT2I [27]|Artifact detector as reward<br>Conditional proximal modeling|_r_ = 1_−D_(_x_); full pipeline alignment<br>Structural face-quality constraints|
|Compositionality &<br>Numerosity|HiCoGen [164]<br>Demystifying<br>Numerosity [188]|Chain of Synthesis decomposition<br>Count-aware noise injection|Hierarchical object + relation rewards<br>Counting accuracy improved from 20% to 85.3%|
|Few-Step Generation|Flash-DMD [10]<br>DMDR [51]|Joint distillation + RL<br>Distribution matching regularization|Stable few-step generation at low training cost<br>_L_=_LRL_+_βLDMD_|
|Adversarial /<br>Reward-Free|Adv-GRPO [94]<br>MoGAN [160]|Discriminator as reward signal<br>Optical-flow discriminator|70%+ human win rate<br>Motion realism reward + distribution regularization|
||TTSnap [176]<br>Text Embedding<br>|Noise-aware early pruning<br>Frequency-domain embedding modification|16%+ performance improvement<br>Sharper high-frequency visual details|
|Test-Time Scaling|Perturbation [157]<br>HyperAlign [156]<br>RLG [35]<br>Exploration-<br>Exploitation [113]<br>MILR [97]|Hypernetwork-generated LoRA<br>Geometric distribution fusion<br>Phase-aware adaptive temperature<br>Multi-modal latent reasoning|Dynamic reward-conditioned adaptation<br>Adjustable alignment trade-off<br>Funnel schedule for semantic transitions<br>80% improvement on WISE benchmark|
||Pref-GRPO [143]<br>RubricRL [28]<br>EmoFeedback<sup>2 </sup>[50]|Pairwise preference fitting<br>Interpretable checklist reward<br>Emotion-aware reward feedback|Avoids pointwise reward amplification<br>Transparent modular scoring<br>MLLM-based affective supervision|
|Preference &<br>Reward Modeling|PaCo-RL [102]<br>BideDPO [193]<br>Emotion-Director [49]<br>Data-Driven Loss [172]<br>James-Stein<br>Shrinkage [175]|Pairwise consistency reward<br>Bidirectionally decoupled DPO<br>Affective shortcut mitigation<br>Learned spatial reasoning loss<br>Instance-level schedule learning|<br>Resolution-decoupled optimization<br>Text/condition conflict mitigation<br>Cross-modal diffusion alignment<br>Spatial accuracy improved (0.20_→_0.61)<br>5-step inference matches full-quality generation|


constraints to produce a structured enhanced prompt—followed by image synthesis via diffusion; both stages are jointly optimized through **Dual-GRPO** , rewarding the reasoner for producing prompts more helpful to the generator and the generator for better executing the reasoner’s instructions, achieving 0.79 on the WISE benchmark and approaching GPT-4-level reasoning performance. Simi- 

16 

larly, **ThinkGen** [52] proposes the first **think-driven visual generation** framework composed of an MLLM and a DiT, introducing **SepGRPO (Separated GRPO)** to alternately freeze one module while optimizing the other to avoid instability from simultaneously updating two large models; the MLLM generates structured visual plans (e.g., layouts and key object descriptions), which the DiT translates into final images. Extending this modular separation, **Unified Thinker** [195] proposes a **task-agnostic reasoning architecture** that fully decouples the Thinker” and Generator,” enabling a general-purpose reasoning engine to provide structured guidance across tasks such as T2I, editing, and super-resolution. Beyond textual reasoning, **CoF-T2I** [125] introduces the novel paradigm of **Chain-of-Frame (CoF) reasoning** , leveraging intermediate frames of a video model as explicit visual reasoning steps that progressively construct a scene—first placing the background, then main objects, then refining attribute details—with the final frame corresponding to the complete generation result, thereby translating chain-of-thought into chain-of-visualization for compositional prompts. At the data and preference level, **AgentComp** [179] integrates LLM **reasoning capabilities and tool-use abilities** into compositional dataset construction, where an LLM agent analyzes prompt structure, calls detectors and segmenters to verify outputs, and constructs precise preference pairs, leading to significant improvements in compositional generation quality. Finally, **Alignment of DM and FM** [99] proposes two alignment schemes: a **guidance network framework** for diffusion models that learns a lightweight network to modify denoising directions, and a **fully training-free alignment framework** for flow matching models that modifies the inference-time noise schedule, both reducing computational cost by over 60% while maintaining alignment effectiveness. Collectively, these works demonstrate that Flow-GRPO is evolving from a pure reinforcement-based optimization framework into a **reasoning-augmented, agent-driven, and modular optimization paradigm** , where prompts, structured plans, visual reasoning trajectories, preference construction, and inference-time alignment are jointly integrated to improve both performance and efficiency. 

**Multi-Objective Alignment.** In parallel with reasoning-augmented extensions, recent works further investigate how to stabilize and modularize multi-objective optimization within the GRPO framework. **APEX** [9] addresses two fundamental challenges in multi-objective GRPO: **variance hijacking** , where high-variance rewards (e.g., aesthetics scores) generate disproportionately large advantage signals after group normalization and thus dominate low-variance but equally important objectives such as safety, and **gradient conflict** , where gradients from different objectives point in contradictory directions and hinder coordinated optimization. To mitigate these issues, APEX proposes **dual-stage adaptive normalization** , first normalizing rewards within each objective and then across objectives to rebalance advantage magnitudes, together with **P**<sup>3</sup> **Adaptive Priorities** , which dynamically adjusts objective weights based on each objective’s current degree of under-optimization, thereby preventing premature saturation of easier objectives while encouraging lagging ones; on SD 3.5, APEX achieves balanced four-objective improvements (+1.31 PickScore, +0.35 DeQA, +0.53 Aesthetics), demonstrating stable multi-objective alignment. Complementarily, **MapReduce LoRA** [8] introduces a modular preference factorization strategy inspired by distributed computing: during the **Map phase** , a dedicated LoRA expert is independently trained for each preference dimension (e.g., aesthetics LoRA, consistency LoRA, safety LoRA), and during the **Reduce phase** , these LoRA experts are iteratively merged into a unified backbone model; at inference time, **RaTE (Rank-Adaptive Test-time Editing)** adaptively controls the contribution weight of each preference dimension, enabling user-controllable personalization without retraining. This Map–Reduce-style decomposition decouples preference optimization across dimensions while preserving unified deployment, achieving SOTA performance across T2I, T2V, and cross-modal language tasks. 

**Text Rendering and Visual Text.** Beyond optimization-level and modular alignment improvements, recent works further enhance text rendering capability and long-text conditioning within generative frameworks. **DCText** [111] proposes a **training-free divide-and-conquer** strategy for long-text and multi-text rendering, where complex text prompts are segmented into multiple subregions and each region is controlled by independent attention masks, explicitly preventing cross-talk between textual areas and enabling precise spatial disentanglement without additional training. Complementarily, **Ovis-Image** [132] develops a compact 7B-parameter T2I model with a text-centric training pipeline that extensively incorporates images containing text during pretraining, thereby strengthening text recognition and rendering alignment; its bilingual (Chinese–English) text rendering performance is reported to be comparable to GPT-4o, demonstrating that targeted data-centric design can significantly improve textual fidelity even at moderate model scale. Extending toward long-form conditioning, **Qwen-Image** [150] achieves high-quality long-text-conditioned image gen- 

17 

eration through **paragraph-level description curriculum learning** , gradually transitioning from short captions to full paragraph descriptions during training, and integrates this curriculum with the Qwen2.5-VL dual-encoder architecture to better capture semantic structure in extended textual contexts. Collectively, these approaches illustrate a complementary direction to reward-based optimization: strengthening structural controllability and textual grounding through inference-time disentanglement, data-centric scaling, and curriculum-based long-text conditioning. 

**Identity/Subject Preservation.** Extending reinforcement-based alignment to multi-subject personalization, recent works focus on mitigating identity interference and competition during joint optimization. **PSR** [139] introduces **pairwise subject-consistency rewards** for multi-subject personalized generation, where the reward function explicitly measures identity consistency between each pair of subjects in the generated image and their corresponding reference images, thereby transforming identity preservation into a structured relational objective rather than independent per-subject scoring. Building on this direction, **MultiCrafter** [154] addresses the identity confusion problem through a **disentangled attention** mechanism that assigns independent attention channels to different identity subjects, reducing feature entanglement during generation, and combines this architectural separation with identity-preserving preference optimization to further stabilize subject fidelity. Moreover, **Customized-GRPO** [48] identifies the **competitive degradation** phenomenon in multi-subject personalization—where improving one subject’s identity consistency inadvertently degrades another’s—and proposes two complementary solutions: **Synergy-Aware Reward Shaping (SARS)** , which formulates the reward as a joint function over all subjects’ consistency to encourage cooperative optimization, and **Time-Aware Dynamic Weighting (TDW)** , which dynamically adjusts attention weights assigned to different subjects across different phases of the denoising process to prevent early-stage dominance or late-stage suppression. Collectively, these approaches reveal that multi-subject personalization introduces higher-order coupling effects in GRPO optimization, requiring relational reward design, architectural disentanglement, and time-dependent weighting strategies to maintain balanced identity preservation. 

**Photorealism.** In pursuit of improved photorealism and domain-specific quality alignment, recent works explore alternative reward formulations and constraint-based modeling. **RealGen** [169] “reverses” the conventional use of AI artifact detectors by employing a pretrained synthetic image detector _D_ ( _x_ ) as a reward signal, defining _r_ = 1 _− D_ ( _x_ ) to explicitly penalize detectable artifacts; notably, it optimizes the **full pipeline** , jointly fine-tuning both the diffusion model and the LLM prompt optimizer so that the entire generation system is end-to-end aligned toward photorealistic outputs rather than only adjusting the backbone model. Complementarily, **ProxT2I** [27] formulates face generation from the perspective of **conditional proximal operators** , learning a mapping that projects noisy latent variables onto a subspace satisfying facial quality constraints, thereby embedding structural priors directly into the generation dynamics; it further releases the **LAION-Face-T2I-15M** dataset, comprising 15 million high-quality face image–text pairs, to support large-scale, face-specific text-to-image alignment. 

**Compositionality and Spatial Reasoning.** Addressing compositional reasoning and numerosity limitations in generative models, recent works investigate structured decomposition and data-biasaware interventions. **HiCoGen** [164] introduces the **Chain of Synthesis (CoS)** paradigm for complex compositional prompts (e.g., “red cup to the left of a blue plate, green ball above the cup”), where an LLM first decomposes the prompt into multiple sub-generation tasks (e.g., separately generating the cup, plate, and ball), followed by iterative object-wise synthesis via the diffusion model; during optimization, **hierarchical rewards** are applied to simultaneously evaluate individual sub-object quality and the correctness of global spatial relationships, enabling reinforcement learning to supervise both local fidelity and relational consistency. Complementarily, **Demystifying Numerosity** [188] provides a thought-provoking empirical analysis demonstrating that diffusion models’ counting ability largely **depends on noise biases in training data** —such as the frequency of images containing specific object counts—rather than genuine semantic grounding of textual numerosity cues; based on this insight, the authors inject **count-aware layout information** by encoding spatial layout priors for the target count directly into the initial noise, leading to a dramatic improvement in counting accuracy from 20% to **85.3%** . Together, these works suggest that compositional and counting failures stem from structural decomposition gaps and data-induced biases, and can be mitigated through hierarchical synthesis strategies and noise-level layout conditioning. 

18 

**Few-Step Generation.** To reconcile efficiency-oriented distillation with reward-driven optimization, recent works explore tighter integration between distribution matching and RL objectives. **FlashDMD** [10] proposes **joint training** of distillation and RL, where the distillation loss constrains the few-step student model to remain close to the teacher model’s distribution—thereby preventing RLinduced policy collapse or mode drift—while the RL loss simultaneously drives the student toward higher-reward regions; this dual-loss design enables stable reward improvement under aggressive step reduction, surpassing DMD2 at only **2.1% of the training cost** . In a related but more explicit regularization formulation, **DMDR** [51] incorporates **DMD (Distribution Matching Distillation) loss as an RL regularization term** , defining the overall objective as _L_ = _L_ RL + _βL_ DMD, where the DMD component acts as a distributional anchor that prevents the model from drifting away from the original data manifold during RL optimization, while the RL term encourages movement toward high-reward directions. Together, these approaches illustrate a principled strategy for balancing reward maximization and distribution preservation, enabling efficient few-step generation without sacrificing stability. 

**Adversarial Rewards and Reward-Model-Free.** Beyond reliance on pretrained reward models, recent works explore reward-model-free adversarial optimization within the GRPO framework. **AdvGRPO** [94] introduces an **adversarial training paradigm** in which the generated image itself becomes the source of reward signals: a discriminator is trained to distinguish real images from generated ones, and its discrimination score is directly used as the GRPO reward, while the generator is simultaneously optimized via GRPO to fool the discriminator, forming a co-evolving adversarial game without requiring an external pretrained reward model. This fully coupled adversarial–reinforcement loop enables automatic reward shaping grounded in data realism, and in human evaluations, AdvGRPO achieves a **70%+ win rate** against Flow-GRPO and SD3 baselines. In a related direction for video generation, **MoGAN** [160] proposes another reward-model-free scheme by introducing an **optical flow discriminator** that explicitly evaluates motion naturalness in generated videos, combined with **distribution matching regularization** to prevent the generated distribution from drifting away from real data statistics. Together, these approaches demonstrate that adversarial discriminators can serve as adaptive, data-driven reward sources, enabling GRPO-style optimization without dependence on fixed pretrained reward models while maintaining distributional stability. 

**Test-Time Scaling.** Complementing training-time optimization, a growing line of work explores inference-time alignment and control strategies that improve reward performance with minimal additional cost. **TTSnap** [176] introduces a **noise-aware pruning** strategy in which multiple candidate samples are generated at inference time, but low-quality candidates are eliminated during early denoising steps based on intermediate state quality estimates; since early denoising steps incur far lower computational cost than full generation, this approach achieves a **16%+ performance improvement** with negligible overhead. **Text Embedding Perturbation** [157] uncovers, through **frequency-domain analysis** , that small high-frequency perturbations applied to text embeddings can enhance high-frequency visual details such as textures and edges in generated images, yielding improved fidelity with nearly zero additional computation. Moving toward adaptive parameterization, **HyperAlign** [156] trains a **hypernetwork** that dynamically generates low-rank adaptation (LoRA) weights at test time conditioned on reward signals, enabling alignment adjustments without modifying latent variables or requiring multi-step optimization. From a probabilistic perspective, **RLG** [35] combines baseline and RL-optimized output distributions via **geometric averaging** , _p_ RLG = _p_<sup>1</sup> base<sup>_−α·_</sup> _p_<sup>_α_</sup> RL<sup>,allowingdynamictrade-offsbetweenalignmentstrengthandbasemodelqualitythrough</sup> _α ∈_ [0 _,_ 1]. **Exploration-Exploitation** [113] further observes that diffusion denoising exhibits **phase transition behavior** , characterized by abrupt semantic shifts in latent variables near specific timesteps, and accordingly designs a **funnel schedule** with **adaptive temperature** —increasing exploration (high temperature) near transition points and strengthening exploitation (low temperature) elsewhere. Finally, **MILR** (Multi-modal Inference-time Latent Reasoning) [97] proposes **joint reasoning over image and text latent variables** at test time, simultaneously optimizing image latents and text embeddings so that both cooperatively converge toward high-reward regions, achieving an **80% improvement** on the WISE benchmark. Collectively, these methods demonstrate that substantial alignment gains can be realized purely at inference time through pruning, perturbation, adaptive parameter generation, probabilistic fusion, temperature scheduling, and multi-modal latent co-optimization. 

19 

**Other T2I Methods.** Beyond architectural and inference-time strategies, a significant line of work revisits the design of reward functions and preference modeling within GRPO and related alignment frameworks. **Pref-GRPO** [143] exposes the **hidden danger of pointwise rewards** in standard GRPO: when reward scores differ only marginally within a group, group normalization can amplify these small differences into extreme advantage signals, leading to unstable gradient updates; it instead adopts **pairwise preference fitting** , directly modeling relative preference relations between samples to avoid pointwise score amplification. Complementarily, **RubricRL** [28] proposes **rubric-based interpretable reward design** , dynamically constructing a **visual checklist** for each prompt (e.g., Does it contain a red car?” Is the background a city?”) where each item is independently scored and then aggregated, making reward signals transparent and debuggable. Targeting affective alignment, **EmoFeedback**<sup>2</sup> [50] introduces **emotion-aware reward feedback** , in which an MLLM evaluates whether generated images convey the intended emotion, together with **self-promotion textual feedback** that generates improvement suggestions to iteratively refine outputs. For consistency-focused tasks, **PaCo-RL** [102] designs a **pairwise consistency reward model** for consistent character generation across scenes and proposes **resolution-decoupled optimization** , separately optimizing low-resolution global consistency and high-resolution detail fidelity. Addressing text–condition conflicts, **BideDPO** [193] proposes **Bidirectionally Decoupled DPO** , separately modeling text-dominant and condition-dominant preference signals to mitigate failures when textual descriptions contradict reference conditions. **Emotion-Director** [49] tackles the **affective shortcut** problem—models substituting complex emotional expression with simple visual proxies—through cross-modal collaborative diffusion combined with DPO to encourage richer affective representations. Moving beyond handcrafted rewards, **Data-Driven Loss** [172] learns a **spatial reasoning loss function** via contrastive learning on images with correct and incorrect spatial relations, enabling end-to-end neural evaluation of spatial correctness and improving spatial accuracy on FLUX.1-dev from 0.20 to **0.61** . Finally, **James-Stein Shrinkage** [175] explores an alternative to weight fine-tuning by **learning instance-level sampling schedules** : for each prompt, an optimal denoising schedule (timestep sizes and noise strengths) is learned and then shrunk toward a global average schedule inspired by the James–Stein estimator, balancing adaptivity and generalization such that 5-step Flux-Dev matches the quality of Flux-Schnell. Collectively, these approaches highlight a broad shift from naive scalar reward optimization toward structured preference modeling, interpretable and domain-aware reward construction, adaptive scheduling, and learned loss formulations. 

### **4.2 Video Generation** 

Video generation extends Flow-GRPO’s alignment challenges from 2D static images to the 3D spatiotemporal domain, introducing new dimensions of problems including temporal consistency, motion naturalness, and identity preservation. This section systematically reviews progress in T2V/I2V core methods, identity consistency, motion control, video editing, video understanding and prediction. The summary is shown in Table 9, and the details are as follows. 

**Core T2V/I2V Methods.** Extending GRPO-style alignment to video generation introduces additional challenges such as temporal coherence, reference consistency, and high-dimensional preference instability, prompting a range of specialized solutions. **TAGRPO** [137] focuses on **image-to-video (I2V)** alignment, where generated videos must remain visually consistent with the input reference image; it proposes a contrastive post-training framework equipped with a **memory bank** that stores successfully generated high-quality samples, and trains new samples via contrastive learning against this bank, progressively elevating the lower bound of generation quality. From a physics-grounded perspective, **PhysRVG** [182] employs **physical rules** as verifiable reward signals: for interaction-heavy videos (e.g., bouncing balls, object collisions), a physics engine simulates rigid-body mechanics and compares simulated trajectories with those observed in generated videos, using discrepancies as penalty terms, thereby providing rewards that are inherently resistant to reward hacking since physical laws cannot be “fooled.” In a training-free alignment direction, **Diffusion-DRF** [141] utilizes a **frozen VLM (e.g., GPT-4V) as a critic** , which evaluates each video frame in natural language, parses the evaluation into structured scores, and **directly backpropagates** them to the diffusion model without requiring dedicated reward model training. Addressing curriculum and stability, **Self-Paced GRPO** [63] introduces a **competence-aware progressive reward** mechanism that begins with simple criteria (e.g., coarse visual fidelity) and gradually transitions to more demanding standards (e.g., temporal coherence, motion naturalness) as model capability improves, mitigating instability from prematurely applying complex rewards; it achieves consistent gains on VBench and generalizes 

20 

Table 9: Representative extensions of Flow-GRPO in video generation. We categorize existing works into core T2V/I2V alignment, identity preservation, motion control, editing, video reasoning, frontier large-scale systems, and reward modeling. 

|**Category**|**Method**|**Core Innovation**|**Key Contribution / Result**|
|---|---|---|---|
|Core T2V / I2V Methods|TAGRPO [137]<br>PhysRVG [182]<br>Diffusion-DRF [141]<br>Self-Paced GRPO [63]<br>PG-DPO [158]<br>DenseDPO [23]<br>McSc [165]|Memory-bank contrastive I2V alignment<br>Physics-engine-based reward<br>Frozen VLM critic (e.g., GPT-4V)<br>Competence-aware curriculum reward<br>Adaptive rejection scaling<br>Segment-level preference labeling<br>Multi-dimensional self-critic reasoning|Progressive lower-bound quality improvement<br>Verifiable rigid-body trajectory consistency<br>Training-free natural-language reward backprop<br>Stable progressive temporal alignment<br>Stabilizes high-dimensional DPO optimization<br>Motion improvement with 1/3 annotation data<br>Motion-corrective DPO while preserving strengths|
|Identity & Consistency|Identity-GRPO [96]<br>IPRO [108]<br>ID-Crafter [100]<br>DreamID-V [36]|Temporally-aware identity reward model<br>Multi-angle identity feature pooling<br>Hierarchical identity attention + online RL<br>Identity-coherence RL for face swapping|+18.9% identity consistency<br>Pose-robust identity scoring<br>Joint identity and semantic alignment<br>Unified realism and temporal consistency|
|Motion Control|AR-Drag [187]<br>Camera-Controlled<br>Video [147]<br>MoGAN [160]<br>HY-Motion 1.0 [149]|RL-enhanced trajectory-conditioned diffusion<br>Geometry-verifiable 3D alignment reward<br>Optical-flow discriminator<br>Billion-scale flow matching for 3D motion|Real-time few-step motion control<br>Segment-level camera trajectory consistency<br>+7.3% motion realism improvement<br>200+ motion categories; improved text-motion<br>alignment|
|Video Editing|VIVA [21]<br>ReViSE [79]|Edit-GRPO for instruction fidelity + temporal<br>coherence<br>Reason-informed semantic decomposition|Scalable synthetic editing dataset<br>+32% editing score improvement|
|Video Understanding &<br>Prediction|Video-as-Answer [19]<br>What Happens<br>Next [64]<br>RLIR [170]|Joint-GRPO for video QA generation<br>Causal consistency reward<br>Inverse-dynamics-based verifiable reward|Video responses as causal answers<br>Plausible next-scene prediction<br>+5–10% action-following performance|
|Frontier Video Synthesis|FSVideo [122]<br>LongCat-Video [123]<br>Seedance 1.0 [30]<br>Seedance 1.5 pro [104]<br>Self-Forcing++ [22]<br>Video Text<br>Preservation [83]|High compression-ratio latent space<br>Block sparse attention<br>Multi-dimensional RLHF + engineering<br>acceleration<br>Native audio-visual joint generation<br>Autoregressive ultra-long generation<br>Text-rich synthetic fine-tuning|10_×_faster inference<br>Minute-scale 720p generation<br>10_×_inference acceleration<br>Multilingual lip-sync capability<br>4m15s video; 50_×_longer than teacher<br>Improved video text rendering fidelity|
|Video Reward Modeling|VR-Thinker [138]<br>SoliReward [71]<br>HuDA [1]<br>REACT [144]<br>Reward Forcing [85]<br>VQ-Insight [185]|Reasoning-enhanced video reward model<br>Multi-aspect video preference modeling<br>Human-aware dense alignment reward<br>Thinking-based video critic<br>Reward-biased DMD (Re-DMD)<br>Progressive visual RL critic training|Structured multi-dimensional scoring<br>Improved evaluation reliability<br>Fine-grained human feedback modeling<br>Reasoning-augmented reward generation<br>Distribution matching toward high-reward regions<br>From binary to multi-dimensional evaluation|


across multiple video backbones. From a preference-learning perspective, **PG-DPO** [158] identifies **likelihood displacement** in high-dimensional video latent spaces, where standard DPO’s implicit reward becomes unstable, and proposes **adaptive rejection scaling** together with **implicit preference regularization** to stabilize optimization. **DenseDPO** [23] further refines video-level supervision into **segment-level preference labeling** , enabling annotators to independently evaluate temporal segments rather than entire videos, dramatically improving motion quality with only **1/3 of the labeling data** . Finally, **McSc** [165] introduces a **self-critic dimensional reasoning** mechanism in which the model first performs multi-dimensional self-evaluation (e.g., visual fidelity, motion naturalness, text consistency) and then applies **motion-corrective DPO** to selectively improve deficient motion aspects while preserving strengths in other dimensions. Collectively, these methods illustrate that video alignment requires memory-augmented contrastive learning, physics-grounded verification, training-free VLM critics, curriculum-style reward scheduling, high-dimensional DPO stabilization, 

21 

fine-grained preference annotation, and self-corrective reasoning to jointly address temporal, physical, and semantic consistency. 

**Identity and Consistency.** Focusing specifically on identity preservation in video generation, recent works tackle the severe challenge of maintaining consistent character appearance across long temporal horizons under variations in facial angle, lighting, and occlusion. **Identity-GRPO** [96] is the first method explicitly targeting **multi-person identity preservation** in video generation, training a **human-feedback-driven identity reward model** that scores identity consistency of the same character across different frames; after GRPO optimization, identity consistency improves by **18.9%** , demonstrating the effectiveness of temporally-aware identity rewards. Complementarily, **IPRO** [108] introduces a dedicated **face identity scorer** together with a **multi-angle feature pool** , which averages features extracted from multiple facial orientations to produce orientation-robust identity scores, mitigating identity drift caused by pose variation. **ID-Crafter** [100] integrates three complementary mechanisms: **hierarchical identity-preserving attention** to maintain identity information across spatial scales, **VLM semantic understanding** to ensure textual alignment, and **online RL** to jointly optimize identity preservation and semantic consistency in an end-to-end manner. Finally, **DreamID-V** [36] presents the first **DiT-based video face-swapping framework** enhanced with **identity-coherence RL** , where the reward simultaneously evaluates post-swap facial realism and cross-frame identity consistency, unifying realism and temporal coherence within a reinforcement learning objective. Collectively, these methods highlight that multi-person video identity alignment requires temporally consistent reward modeling, pose-robust feature aggregation, hierarchical attention design, and joint optimization of identity and semantic objectives. 

**Motion Control.** Targeting controllable and physically grounded motion generation, recent works integrate reinforcement learning with trajectory-level and geometry-level supervision across both video and 3D motion domains. **AR-Drag** [187] presents the first **RL-enhanced few-step autoregressive video diffusion model** capable of real-time motion control, where users specify motion trajectories through drag operations and the model generates videos that conform to these motion instructions within only a few inference steps; the RL reward explicitly measures the correspondence between generated motion and user-specified trajectories, enabling precise trajectory adherence under extremely low step budgets. Complementarily, **Camera-Controlled Video** [147] leverages **verifiable geometry rewards** by recovering 3D camera trajectories from generated videos using monocular depth estimation and visual odometry, and performing dense **segment-level 3D alignment** against target trajectories, thereby grounding motion control in explicit geometric consistency. From a motion realism perspective, **MoGAN** [160] incorporates an **optical flow discriminator** into the DiT architecture to evaluate whether extracted optical flow fields conform to natural motion statistics, improving motion quality scores by **7.3%** . Reinforcement alignment has also been extended to large-scale 3D human motion synthesis. **HY-Motion 1.0** [149] is the first **billion-parameter-scale** DiT flow matching model for text-driven 3D human motion generation, producing realistic motion sequences across **200+ motion categories** spanning six major classes. Compared to prior million-parameter models, its scaling enables generalization to unseen motion compositions, while Flow-GRPO alignment further enhances motion naturalness and text–motion consistency. Collectively, these works demonstrate that trajectory-conditioned RL, geometry-verifiable supervision, flow-based motion discrimination, and large-scale flow matching together enable controllable, physically plausible motion generation across both video and 3D human motion spaces. 

**Video Editing.** Extending Flow-GRPO-style alignment to video editing tasks, recent works incorporate editing accuracy and semantic reasoning into reinforcement-based optimization. **VIVA** [21] adapts Flow-GRPO to the video editing setting by introducing **Edit-GRPO** , where the reward function jointly evaluates editing accuracy—whether the specified editing instruction is correctly executed—and temporal consistency—whether edited regions remain coherent across frames—thereby balancing local edit correctness with global temporal stability; moreover, VIVA constructs a synthetic data pipeline that automatically generates large-scale video editing training pairs, enabling scalable post-training for editing alignment. Complementarily, **ReViSE** [79] proposes **reason-informed video editing** , in which the model first performs semantic analysis of editing instructions through a **self-reflective reasoning framework** , explicitly decomposing high-level instructions (e.g., “make the sky look like sunset”) into underlying visual operations such as color tone adjustment, lighting modification, and cloud augmentation, and then executes the edit step-by-step guided by this reasoning process; this structured reasoning-enhanced editing improves the overall editing score by **32%** . 

22 

Together, these approaches demonstrate that effective video editing alignment requires joint optimization of instruction fidelity and temporal coherence, as well as explicit semantic decomposition of complex editing intents. 

**Video Understanding and Prediction.** Extending reinforcement-based alignment toward reasoning and causality in video generation, recent works move beyond pure perceptual quality optimization. **Video-as-Answer** [19] introduces a new video question-answering paradigm in which the model **generates video as the answer** rather than textual responses—for instance, generating a ball trajectory video to answer What would happen if the ball were kicked?”—and employs **Joint-GRPO** to simultaneously align the VLM responsible for question understanding and the video diffusion model responsible for answer generation. **What Happens Next** [64] addresses the **next-scene prediction** task, designing a **causal consistency reward** that enforces plausible causal relationships between predicted scenes and preceding video context. Complementarily, **RLIR** [170] leverages an **inverse dynamics model** to recover latent action sequences from generated videos, using these recovered actions as **verifiable rewards** —e.g., if the generated video claims a turning right” action, the inverse model must infer a consistent directional change—improving action-following performance by **5– 10%** . Together, these methods highlight a shift from surface-level alignment toward causal reasoning, counterfactual prediction, and action-verifiable reward design in video generation. 

**Frontier Video Synthesis.** Alongside alignment and reward-design advances, recent largescale video systems push the frontier of model capacity, efficiency, and long-form generation. **FSVideo** [122] is a 14B-parameter video generation system that adopts an extremely high compression-ratio latent space, reducing videos to highly compact latent representations and achieving inference speeds an order of magnitude faster than contemporary open-source models. **LongCatVideo** [123], a 13.6B-parameter long-video model, enables **minute-scale 720p generation** by leveraging **block sparse attention** , reducing computational complexity from _O_ ( _n_<sup>2</sup> ) to _O_ ( _n_ log _n_ ) and making long-context temporal modeling tractable. **Seedance 1.0** [30] integrates multi-dimensional RLHF—separately optimizing visual quality, motion naturalness, and text consistency—while achieving **10** _×_ **inference acceleration** through engineering optimization; its successor, **Seedance 1.5 pro** [104], further introduces **native audio-visual joint generation** , simultaneously synthesizing visual content and synchronized audio with multilingual lip-sync capability. From an autoregressive perspective, **Self-Forcing++** [22] enables ultra-long video generation of **4 minutes 15 seconds** —over 50 _×_ longer than its teacher model—via autoregressive frame generation, overcoming traditional diffusion-based length limitations. Finally, **Video Text Preservation** [83] demonstrates that finetuning on synthetic text-rich videos substantially enhances video text rendering capability, highlighting the importance of data-centric scaling for multimodal consistency. Collectively, these systems illustrate that scaling latent compression, sparse attention, multi-objective RLHF, autoregressive extension, and data augmentation are key drivers of efficiency and long-horizon capability in modern video generation. 

**Video Reward Models. VR-Thinker** [138], **SoliReward** [71], **HuDA** [1], and **REACT** [144] have been discussed in detail in §3.7, where we analyze their respective reward modeling strategies and alignment mechanisms. Beyond explicit reward model design, **Reward Forcing** [85] introduces a novel **distribution biasing** paradigm by modifying the DMD (Distribution Matching Distillation) objective to “force” the student model’s output distribution toward high-reward regions, resulting in Re-DMD (Reward-biased DMD) that integrates reward preference directly into distribution matching. Complementarily, **VQ-Insight** [185] enhances VLM-based AIGC video evaluation through **progressive visual RL** , where training gradually evolves from coarse binary preference judgments (good/bad) to fine-grained multi-dimensional quality assessment, enabling the critic to develop richer and more discriminative evaluation capability. Together, these approaches reflect a broader trend of integrating reward awareness into distribution matching and progressively strengthening visual evaluation models to support more reliable alignment. 

### **4.3 Image Editing** 

Image editing is an important application scenario for GRPO alignment, where the core challenge lies in balancing editing accuracy (correctly executing instructions) and preservation (not modifying irrelevant regions). Recent works have introduced reasoning capabilities into the editing workflow, 

23 

Table 10: Representative GRPO-based extensions in image editing. Recent works emphasize reasoning-driven editing, dense reward shaping, motion- and geometry-aware control, scalable data construction, and paradigm-agnostic RL alignment. 

|**Category**|**Method**|**Core Innovation**|**Key Contribution / Result**|
|---|---|---|---|
||ThinkRL-Edit [61]|CoT-based semantic analysis + binary checklist<br>|Improves correctness–preservation balance|
|Reasoning-Driven Editing|Re-Align [41]<br>JarvisEvo [72]<br>Skywork UniPic<br>2.0 [148]|reward<br>In-Context CoT (IC-CoT) alignment<br>Editor–Evaluator alternating optimization (SEPO)<br>Progressive Dual-Task Reinforcement (PDTR)|Example-guided reasoning during inference<br>+18.95% preservation; +44.96% pixel fidelity<br>Joint image understanding + editing; Surpasses<br>larger models|
|Dense Reward &<br>Attention Control|CogniEdit [67]<br>EditScore [86]<br>OmniRefiner [81]|Dense GRPO + Dynamic Token Focus Relocation<br>Structured editing reward evaluation<br>Detail-aware post-edit refinement|Region-aware attention for edit vs. preserve<br>Interpretable multi-criterion scoring<br>Reference-guided fine-grained enhancement|
|Motion &<br>Geometry-Aware Editing|MotionEdit [127]<br>Talk2Move [117]|Motion alignment rewards<br>Text-instructed geometric transformation RL|Physically plausible motion modifications<br>Precise translation/rotation/scaling control|
|Application-Driven Editing|RePainter [38]<br>Uniworld-V2 /<br>Edit-R1 [70]|RL-based object removal + spatial matting<br>DiffusionNFT-style efficient training + MLLM<br>feedback|Seamless inpainting for e-commerce scenes<br>SOTA 4.49 on ImgEdit benchmark|
||NPEdit [58]|No-paired-data editing training|Editing alignment using VLM-only feedback|
|Scalable Data &<br>Curriculum|Scaling Video<br>Editing [2]|Ditto-1M dataset + Editto curriculum|Million-scale edit dataset; Progressive training|
||Re-Align [41]|Progressive edit complexity scheduling|Improved stability across edit types|
|Paradigm-Agnostic|EARL [187]|RL for autoregressive image editing|Extends alignment beyond diffusion models|
|RL Alignment|Skywork UniPic<br>2.0 [148]|Lightweight DiT + RL optimization|2B model surpassing 7B/12B competitors|


achieving significant quality improvements. The summary is shown in Table 10, and the details are as follows. 

Recent advances in RL-enhanced image and video editing increasingly emphasize reasoning, dense reward shaping, and scalable data construction. **ThinkRL-Edit** [61] introduces a **reasoning-centric RL editing framework** , where the model first performs CoT-based semantic analysis of editing instructions (e.g., understanding that “change the shirt to red” requires modifying only color without altering shape), and optimizes using a **binary checklist** reward composed of independent yes/no questions evaluating correctness and preservation. **Re-Align** [41] further proposes **In-Context CoT (IC-CoT) reasoning-guided alignment** , leveraging example editing cases during inference to guide current edits. **CogniEdit** [67] combines **Dense GRPO optimization** with **Dynamic Token Focus Relocation** , reallocating attention during denoising to emphasize editable regions while protecting preserved areas. **JarvisEvo** [72] presents **Synergistic Editor-Evaluator Policy Optimization (SEPO)** , alternating optimization between editor and evaluator modules, and—combined with multimodal CoT reasoning—achieves 18.95% improvement in preservation editing and 44.96% gain in pixel fidelity. For motion-aware edits, **MotionEdit** [127] introduces **motion alignment rewards** to ensure plausibility in motion-modifying edits, while **Talk2Move** [117] applies GRPO to optimize precision in **text-instructed geometric transformations** such as translation, rotation, and scaling. In application-driven scenarios, **RePainter** [38] focuses on e-commerce **object removal + spatial matting** , using RL to ensure seamless blending of filled regions, and **OmniRefiner** [81] performs **detail-aware refinement** guided by reference images after primary generation. **Uniworld-V2/EditR1** [70] integrates DiffusionNFT-style efficient training with MLLM implicit feedback, achieving a **SOTA score of 4.49** on ImgEdit, while **NPEdit** [58] enables **no-paired-data editing training** using only VLM feedback. At scale, **Scaling Video Editing** [2] releases the million-scale **Ditto-1M** dataset and proposes the **Editto** curriculum from simple to complex edits. **EditScore** [86] has been discussed in §3.7. Broadening model paradigms, **EARL** [187] applies RL to **autoregressive image editing** , demonstrating that alignment is not confined to diffusion-based models, and **Skywork UniPic 2.0** [148], a 2B-parameter DiT model, leverages **Progressive Dual-Task Reinforcement (PDTR)** to jointly optimize image understanding and editing, surpassing larger models such as BAGEL 7B and Flux-Kontext 12B. Collectively, these works indicate a shift toward reasoning-driven editing, dense 

24 

and interpretable rewards, motion- and geometry-aware control, scalable dataset construction, and paradigm-agnostic RL alignment. 

Table 11: Representative extensions of GRPO alignment in speech and audio generation. These works demonstrate the modality-agnostic nature of GRPO in continuous-time signal modeling, multi-metric optimization, and style-preserving <u>generation.</u> 

|**Category**|**Method**|**Core Innovation**|**Key Contribution / Result**|
|---|---|---|---|
|Speech Enhancement|FlowSE-GRPO [133]|Online GRPO for flow-matching speech<br>enhancement with multi-metric reward balancing|Joint optimization of PESQ, STOI, and SI-SDR<br>within unified RL framework|
|Music &<br>Singing Generation|YingMusic-Singer [189]|Multi-objective GRPO for zero-shot singing voice<br>synthesis|Style-consistent singing from lyrics + melody<br>without target-speaker training data|
||YingMusic-SVC [11]|GRPO-based zero-shot singing voice conversion<br>with singing-specific inductive biases|Timbre conversion preserving lyrics and melody;<br>Reward models formant and vibrato structure|


### **4.4 Speech and Audio** 

GRPO alignment extends beyond the visual modality, and its core principles naturally generalize to continuous-time audio signal generation. As show in Table 11, **FlowSE-GRPO** [133] is the first work integrating online GRPO into flow matching speech enhancement (SE), addressing challenges unique to audio generation: speech signals are continuous time series rather than fixed-size images, and quality evaluation requires simultaneously optimizing multiple potentially conflicting metrics, including speech quality (PESQ), speech intelligibility (STOI), and signal-to-distortion ratio (SI-SDR); accordingly, FlowSE-GRPO designs a **multi-metric reward optimization** scheme that adaptively balances these objectives within a unified reinforcement learning framework. Extending FlowGRPO to music generation, **YingMusic-Singer** [189] applies a multi-objective reward formulation to **zero-shot singing voice synthesis** , generating singing in a specific singer’s style from lyrics and melody without using training data from the target singer, where the reward evaluates pitch accuracy, rhythm alignment, and timbre similarity. Similarly, **YingMusic-SVC** [11] adapts Flow-GRPO to **zero-shot singing voice conversion (SVC)** , preserving original lyrics and melody while converting the singer’s timbre to a target identity, and introduces singing-specific inductive biases—such as formant structure and vibrato patterns—so that GRPO rewards can capture fine-grained perceptual qualities of singing. Collectively, these works demonstrate that GRPO-based alignment provides a modality-agnostic optimization paradigm capable of handling continuous signals, multi-metric trade-offs, and style-preserving generation in the audio domain. 

Table 12: Extensions of GRPO alignment in 3D generation and scientific foundation models. These works demonstrate hierarchical optimization, cross-dimensional reward transfer, efficient 3D representations, and physically <u>grounded reinforcement objectives.</u> 

|**Category**|**Method**|**Core Innovation**|**Key Contribution / Result**|
|---|---|---|---|
|3D Generation|Hi-GRPO /<br>AR3D-R1 [120]<br>Nabla-R2D3 [78]|Hierarchical coarse-to-fine RL optimization for<br>text-to-3D<br>Cross-dimensional reward transfer (2D_→_3D)|Progressive global shape_→_local texture<br>refinement; Improved multi-view consistency<br>Multi-view rendering + 2D reward averaging for 3D<br>alignment|
||VIST3A [33]|Video-to-3D model stitching|Multi-view consistent video frames enable coherent<br>3D reconstruction|
||TRIM [173]|3D Gaussian Splatting acceleration|Efficient 3D diffusion with preserved visual fidelity|
||Open Materials|RL-guided crystal structure search|Thermodynamic stability + symmetry-aware reward|
|Scientific Applications|Generation [43]<br>Elign / FED-GRPO [66]|Force-Energy Disentangled GRPO for molecular<br>modeling|via DFT energy<br>Separate rewards for force accuracy and energy<br>smoothness|
||Flow Marching [17]|Flow-matching PDE foundation modeling|RL reduces long-horizon rollout drift in dynamical<br>systems|


25 

### **4.5 3D Generation and Scientific Applications** 

**3D Generation.** GRPO-based alignment has also begun extending into 3D generation, where maintaining multi-view consistency and structural coherence introduces challenges beyond 2D synthesis. As show in Table 12, **Hi-GRPO/AR3D-R1** [120] is the first work incorporating RL enhancement into text-to-3D generation, recognizing that 3D objects must remain consistent across all viewpoints; it proposes a **hierarchical optimization** strategy that first optimizes global shape and structural geometry (low-frequency components) and subsequently refines local details and textures (high-frequency components), enabling progressive coarse-to-fine improvement of 3D quality. **NablaR2D3** [78] addresses the difficulty of training dedicated 3D reward models by leveraging **2D reward models to align 3D diffusion models** : 3D objects are rendered from multiple viewpoints into 2D images, each view is independently evaluated by a 2D reward model, and the averaged reward is propagated back to guide 3D optimization, effectively reducing 3D alignment to multi-view 2D supervision. Bridging video and 3D, **VIST3A** [33] employs **model stitching** to connect a video generator with a 3D reconstruction module, where multi-view-consistent video frames produced by the generator are used to recover coherent 3D structures. Finally, **TRIM** [173] accelerates 3D diffusion generation by adopting 3D Gaussian Splatting representations, significantly improving efficiency while preserving quality. Collectively, these works demonstrate that hierarchical RL optimization, cross-dimensional reward transfer, model stitching, and efficient 3D representations are key enablers for extending GRPO alignment into the 3D domain. 

**Scientific Applications.** Beyond perceptual media generation, GRPO-based alignment has begun influencing scientific foundation models operating over structured physical domains. **Open Materials Generation** [43] is the first work applying RL alignment to **crystal structure prediction** , where the generative model proposes candidate crystal structures and the reward function evaluates thermodynamic stability—via formation energy computed using DFT—as well as symmetry constraints, enabling reinforcement learning to guide structure search toward physically plausible and energetically favorable configurations. **Elign/FED-GRPO** [66] further extends GRPO to **equivariant diffusion models** for molecular force field computation, introducing **Force-Energy Disentangled GRPO (FED-GRPO)** that designs independent reward components for force field accuracy and potential energy surface smoothness, thereby mitigating optimization conflicts between force prediction precision and energy consistency. At the level of scientific simulation, **Flow Marching** [17] adapts the flow matching paradigm to **PDE (partial differential equation) foundation models** , addressing the long-term error accumulation problem of traditional numerical solvers by learning a unified velocity field that models temporal evolution, with RL optimization reducing rollout drift over extended simulation horizons. Collectively, these works demonstrate that GRPO-style alignment can generalize to physically constrained generative systems, where reward signals derive from thermodynamic principles, symmetry equivariance, or long-horizon dynamical consistency. 

### **4.6 VLA and Embodied AI** 

Extending Flow-GRPO to Vision-Language-Action (VLA) models and embodied intelligence introduces the additional difficulty that action spaces are continuous, high-dimensional, and must support real-time interaction with physical environments. As show in Table 13, **SA-VLA** [101] proposes **Spatially-Aware Flow Matching** for robotic manipulation, incorporating explicit 3D spatial cues such as depth and surface normals into the flow matching condition to produce spatially grounded action trajectories, and introduces the **SCAN exploration strategy** , which injects structured random perturbations into action space to enhance exploration efficiency. _π_ **RL** [14] investigates two RL integration strategies for flow-based VLA policies: **Flow-Noise** , where stochasticity is injected only in the initial noise while subsequent evolution remains deterministic (ODE), and **Flow-SDE** , where randomness is introduced at every step; experiments reveal a trade-off, with Flow-Noise offering greater stability and Flow-SDE providing stronger exploration. **FPO (Flow Policy Optimization)** [90] introduces **structure-aware credit assignment** , leveraging hierarchical task decomposition to distribute task-level rewards to individual action steps, and combines this with **Q-ensemble value estimation** for more robust policy updates. **ProphRL** [181] trains an **action-to-video world model** that predicts future visual observations from current states and action sequences, serving as a **few-shot simulator** to drastically reduce real-world interaction cost; coupled with **FA-GRPO (Flow-Aware GRPO)** for policy optimization on simulated rollouts, it achieves 5–17% improvement in simulation and 24–30% gains on real robots. In pursuit of real-time control, **DMPO** [198] enables **true single-step** 

26 

Table 13: Extensions of Flow-GRPO style in Vision-Language-Action (VLA) and embodied AI. These works address continuous high-dimensional action spaces, real-time control, simulator-based learning, structured credit assignment, and socially aware policy optimization. 

|**Category**|**Method**|**Core Innovation**|**Key Contribution / Result**|
|---|---|---|---|
|Spatially-Grounded<br>Flow Policies|SA-VLA [101]<br>_π_RL [14]<br>PolicyFlow [166]|Spatially-Aware Flow Matching with 3D cues<br>(depth, normals)<br>Flow-Noise vs. Flow-SDE RL integration<br>Continuous normalizing flow (CNF) policies +<br>Brownian regularizer|SCAN exploration strategy for efficient action-space<br>exploration<br>Stability–exploration trade-off analysis in<br>flow-based VLA<br>Structured stochastic exploration under PPO<br>optimization|
|Structured<br>Policy Optimization|FPO [90]<br>Flow Matching Policy<br>Gradients [95]|Structure-aware credit assignment<br>Theoretical PPO compatibility proof|Hierarchical reward decomposition + Q-ensemble<br>estimation<br>Validates flow matching as RL policy<br>parameterization|
|Simulator-Based &<br>World Models|ProphRL [181]<br>EmboMatrix /<br>EmboBrain [60]|Action-to-video world model for few-shot<br>simulation<br>Large-scale embodied decision benchmark +<br>multi-task RL agent|5–17% sim gain; 24–30% real-robot improvement<br>via FA-GRPO<br>Unified navigation, manipulation, and interaction<br>evaluation|
|Real-Time Control|DMPO [198]<br>FPMD [16]|Single-step action generation at_>_120Hz<br>One-step inference from multi-step flow policies|Dispersive regularization prevents policy mode<br>collapse<br>Achieves 1-step execution without distillation|
|Socially-Aware RL|SocialNav [18]|SAFE-GRPO for social constraint encoding|+38% navigation success; +46% social compliance|


**action generation** at inference frequencies exceeding **120Hz** , employing **dispersive regularization** to prevent policy mode collapse and preserve action diversity under environmental uncertainty, while **FPMD** [16] derives 1-step inference capability directly from multi-step flow policies **without distillation** . From a theoretical standpoint, **Flow Matching Policy Gradients** [95] proves compatibility between flow matching policies and PPO-clip, establishing flow matching as a valid policy parameterization for standard RL algorithms. Beyond single-agent manipulation, **SocialNav** [18] applies GRPO to **social navigation** , introducing **SAFE-GRPO** to encode social constraints such as personal space preservation alongside efficiency objectives, improving success rate by **38%** and social compliance by **46%** . At scale, **EmboMatrix** [60] constructs a large unified embodied decision-making benchmark spanning navigation, manipulation, and interaction, and releases **EmboBrain** , a multi-task RL-trained embodied agent. Finally, **PolicyFlow** [166] parameterizes action policies as **continuous normalizing flows (CNF)** , integrates PPO optimization, and introduces a **Brownian regularizer** to inject structured stochasticity during policy updates, promoting exploration while maintaining flow-based structure. Collectively, these works demonstrate that flow-based RL alignment extends naturally to embodied agents, enabling spatial grounding, structured credit assignment, simulator-based policy learning, real-time control, theoretical RL compatibility, and socially aware behavior in continuous action domains. 

### **4.7 Unified Multimodal Models** 

Unified multimodal models seek to jointly support visual understanding and visual generation within a single architecture, with GRPO serving as a key alignment mechanism to reconcile bidirectional objectives. As show in Table 14, **UAE** [163] formulates unification from an **auto-encoder perspective** , treating visual understanding as encoding (image _→_ semantics) and generation as decoding (semantics _→_ image), and introduces **Unified-GRPO** to simultaneously optimize understanding rewards (e.g., VQA accuracy) and generation rewards (e.g., human preference), enabling bidirectional enhancement. **BLIP3o-NEXT** [13] adopts a fully open-source **AR + Diffusion** hybrid architecture, using the autoregressive module for understanding and planning and diffusion for high-fidelity generation, with RL optimization pushing generation performance to the frontier. **UniRL-Zero** [130] proposes **unified RL** , jointly optimizing language and diffusion experts under a single RL algorithm rather than separate training. Architecturally, **ParaUni** [116] introduces **hierarchical parallel information interaction** between VLM layers, enabling intermediate representations of understanding and generation to 

27 

Table 14: Representative unified multimodal models aligned with GRPO-style optimization. We categorize existing works into unified RL optimization, hybrid/parallel architectures, reasoningaugmented generation, efficiency-oriented structural design, and auxiliary constraint / system-level scaling. 

|**Category**|**Method**|**Core Innovation**|**Key Contribution / Result**|
|---|---|---|---|
|Unified RL Optimization|UAE [163]<br>UniRL-Zero [130]<br>Unified T2I<br>(Weakness-Targeted<br>PT) [12]|Auto-encoder unification (encode=understanding,<br>decode=generation) + Unified-GRPO<br>Single RL algorithm for language + diffusion<br>experts<br>Weakness-targeted post-training reinforcement|Joint optimization of VQA and preference rewards;<br>Bidirectional enhancement<br>Eliminates modality-decoupled training; Unified<br>policy optimization<br>Automatic strengthening of underperforming<br>prompt categories|
|Hybrid /<br>Parallel Architectures|BLIP3o-NEXT [13]<br>ParaUni [116]<br>MMaDA-Parallel [124]|AR (planning) + Diffusion (generation) hybrid<br>framework<br>Hierarchical parallel VLM interaction + LDAM<br>gradient balancing<br>Parallel multimodal diffusion with cross-attention;<br>ParaRL training|Open-source multimodal frontier with RL-enhanced<br>generation<br>Cross-layer bidirectional information coupling<br>Simultaneous denoising of text and image streams|
|Reasoning-Augmented<br>Generation|Visual-Aware<br>CoT [171]<br>SEER [121]<br>Visual Generation for<br>Reasoning [153]|Adaptive visual planning + iterative correction<br>Endogenous reprompting for self-evolving cognitive<br>alignment<br>Interleaved visual–verbal CoT (Visual Superiority<br>Hypothesis)|Intermediate visual reasoning refinement during<br>generation<br>Bridges reasoning gap between understanding and<br>generation<br>Generation-assisted reasoning performance<br>improvement|
|Efficiency /<br>Structural Design|MoS [75]<br>MANZANO [98]<br>FUDOKI [135]|Learnable token-level router for sparse task<br>allocation<br>Hybrid vision tokenizer design<br>Pure discrete flow matching with unified token space|Efficient computation balancing between modalities<br>Reduced understanding-generation task interference<br>Homogeneous multimodal generation framework|
|Auxiliary Constraints &|COOPER [186]|Auxiliary depth + segmentation supervision|Enhanced geometric and spatial reasoning<br>it|
|System Scaling|ShowTable [82]<br>Seedream 4.0 [105]|MLLM–diffusion collaborative generation<br>Native 1K–4K high-resolution unified generation|conssency<br>Information-preserving multimodal table<br>visualization<br>Production-scale multimodal system integration|


influence each other, combined with **Layer-wise Dynamic Adjustment Mechanism (LDAM)** to balance gradient flows during RL training; similarly, **MMaDA-Parallel** [124] proposes **parallel multimodal diffusion** , where text and images are denoised simultaneously and interact through cross-attention, and **ParaRL** provides a dedicated RL training strategy. From a reasoning perspective, **Visual-Aware CoT** [171] introduces **adaptive visual planning** and **iterative visual correction** , allowing models to generate and refine intermediate visual reasoning steps, while **SEER** [121] proposes **self-evolving cognitive alignment** via endogenous reprompting to bridge the cognitive gap between understanding and generation. **Visual Generation for Reasoning** [153] advances the **Visual Superiority Hypothesis** , advocating **interleaved visual-verbal CoT** that alternates textual reasoning and visual generation for improved reasoning performance. Efficiency and structural design innovations include **MoS** [75], which employs a learnable token-level router to sparsely allocate computation between understanding and generation; **MANZANO** [98], which introduces a hybrid vision tokenizer to reduce task conflicts; and **FUDOKI** [135], which unifies text and images as discrete tokens under pure discrete flow matching. At the system level, **Seedream 4.0** [105] supports seamless **1K–4K native high-resolution** generation, and **Unified T2I with Weakness-Targeted PT** [12] proposes **weakness-targeted post-training** to automatically reinforce underperforming prompt categories. **COOPER** [186] enhances spatial reasoning by introducing auxiliary depth and segmentation outputs to constrain geometric consistency, and **ShowTable** [82] demonstrates multimodal collaboration between MLLM and diffusion models for creative, information-preserving table visualization. Collectively, these works illustrate that GRPO-enabled unified models rely on bidirectional reward optimization, parallel architectural interaction, visual reasoning augmentation, 

28 

adaptive routing, auxiliary modality constraints, and targeted post-training to bridge understanding and generation within a single multimodal framework. 

Table 15: Extensions of GRPO alignment to autoregressive (AR), masked diffusion, and discrete flow matching models. These works explore token-level credit assignment, adaptive regularization, masking <u>policy optimization, search-based decoding, and distribution-level reinforcement learning.</u> 

|**Category**|**Method**|**Core Innovation**|**Key Contribution / Result**|
|---|---|---|---|
||AR-GRPO [177]|Token-level GRPO for AR image generation|Structured reward optimization over discrete visual<br>tokens|
|Autoregressive|STAGE [93]|Similarity-aware KL/advantage reweighting|Adaptive KL scaling + entropy reward to prevent|
|Image Generation|||collapse|
||VAR RL Done<br>Right [114]|VMR + PANW + Mask Propagation|Token-level return estimation + position-sensitive<br>normalization|
||GCPO [180]|Critical-token selective optimization|RL applied to top 30% important tokens only|
||Layout-Conditioned AR<br>T2I [191]|Layout-aware masking + spatial rewards|Improved spatial controllability in AR generation|
||AR-Drag [187]|RL-enhanced autoregressive trajectory control|Extends AR alignment to video/motion generation|
||Co-GRPO [194]|Joint optimization of model + inference schedule|Treats mask schedule as MDP action variable|
|Masked Diffusion Models|Mask-GRPO [89]<br>MaskGRPO<br>(Multimodal) [92]|RL over unmasking trajectory<br>Multimodal discrete masking + RL alignment|Sequential mask selection aligned with reward<br>Unified text-image masking optimization|
|Discrete Diffusion /<br>Flow Matching|Discrete Guidance<br>Matching [128]<br>TR2-D2 [119]<br>DMPO (Discrete) [198]|Exact reward-consistent discrete guidance<br>MCTS-based unmasking search<br>Distribution-level policy optimization|Enables guidance in non-differentiable token space<br>Trajectory-aware fine-tuning via discovered paths<br>42.9% accuracy improvement via divergence<br>minimization|
||LaDiR [55]|Latent diffusion reasoning for LLMs|Continuous latent reasoning before discrete<br>decoding|
||LaDi-RL [54]|Reward-driven latent diffusion steering|RL-guided drift in latent space with diversity<br>preservation|


### **4.8 Autoregressive and Masked Diffusion Models** 

GRPO was originally designed for autoregressive LLMs, and bringing it back to autoregressive visual models and masked diffusion models represents a natural extension. The summary is shown in Table 15, and the details are as follows. 

**Autoregressive Image Generation.** Reinforcement alignment has also been extended to autoregressive (AR) image generation models, where images are generated token-by-token (e.g., via VQVAE discrete tokens) and policy optimization operates at the token level. **AR-GRPO** [177] is the first work adapting GRPO to **autoregressive image generation** , optimizing perceptual quality, realism, and semantic alignment through structured reward categories. **STAGE** [93] observes that standard KL divergence regularization is overly coarse for AR image models and introduces **similarity-aware advantage/KL reweighting** , dynamically scaling KL penalties according to the semantic similarity between generated samples and the reference distribution; it further incorporates **entropy-based rewards** to maintain sufficient generation entropy and prevent mode collapse. For VAR (Visual Autoregressive) models, **VAR RL Done Right** [114] proposes three key techniques: **Value as Middle Return (VMR)** to provide token-level return estimation, **Per-Action Normalization Weighting (PANW)** to apply position-sensitive normalization schemes, and **Mask Propagation (MP)** to block gradients from masked regions. **GCPO** [180] reveals that tokens in AR image models are not equally important and identifies **critical tokens** based on **causal dependency** , **entropy** , and **diversity** criteria, achieving superior performance by applying RL optimization to only 30% of tokens. **Layout-Conditioned AR T2I** [191] enhances spatial controllability by injecting layout conditions and **structured masks** into AR generation, combined with **GRPO layout rewards** to enforce spatial relationship correctness. Finally, **AR-Drag** [187], discussed in §4.2, demonstrates that RL-enhanced autoregressive policies can also extend to video generation and motion control. Collectively, these works show that token-level credit assignment, adaptive regularization, selective 

29 

optimization, structured masking, and layout-aware rewards are central to stabilizing and enhancing RL alignment in autoregressive generative models. 

**Masked Diffusion Models.** Reinforcement-based alignment has also been extended to masked generative paradigms, where inference schedules and masking policies play a central role in generation quality. **Co-GRPO** [194] formulates a unified MDP framework for **masked diffusion models (MDM)** , recognizing that inference schedules—such as mask ratio annealing strategies—critically affect performance; it therefore **jointly models model parameters and inference schedules as components of the MDP action space** , enabling GRPO to simultaneously optimize both network weights and decoding dynamics. Complementarily, **Mask-GRPO** [89] is the first work to directly introduce GRPO into masked generative models by casting the mask prediction process as sequential decision-making, where each action corresponds to selecting positions to unmask at each step, thereby aligning the unmasking trajectory itself with reward objectives. Extending this paradigm to broader settings, **MaskGRPO (Multimodal)** [92] adapts the framework to **multimodal discrete diffusion** , jointly handling text and image discrete tokens within a unified masking and RL optimization process, enabling scalable multimodal reinforcement alignment. Collectively, these works demonstrate that masking strategies and inference schedules can be elevated to first-class optimization variables under GRPO, broadening reinforcement alignment beyond parameter updates to include generative decoding policies. 

**Discrete Diffusion / Flow Matching.** Recent advances further extend flow and diffusion alignment into discrete and language-centric settings, addressing challenges unique to non-differentiable token spaces. **Discrete Guidance Matching** [128] tackles the **exact guidance** problem in discrete flow matching, where traditional continuous guidance techniques (e.g., Classifier Guidance) are inapplicable due to non-differentiability; it introduces a discretized guidance matching objective that enables exact reward-consistent guidance directly in discrete space. **TR2-D2** [119] incorporates **MCTS (Monte Carlo Tree Search)** into discrete diffusion by treating the unmasking process as a search tree, using MCTS to discover optimal unmasking trajectories and subsequently applying **trajectoryaware fine-tuning** based on these discovered paths. For discrete diffusion LLMs, **DMPO** [198] proposes **Distribution Matching Policy Optimization** , replacing per-token policy gradients with distribution-level divergence minimization between generated and target distributions, yielding a substantial **42.9%** accuracy improvement. Bridging continuous and discrete reasoning, **LaDiR** [55] introduces **latent diffusion** into LLM text reasoning by performing diffusion-style reasoning in continuous latent space before mapping back to discrete tokens, leveraging the smoothness of continuous dynamics for improved reasoning trajectories. **LaDi-RL** [54] further integrates RL into this latent diffusion framework, applying reward-driven drift in latent space to steer discrete outputs toward higher quality while maintaining diversity. Collectively, these works demonstrate that discrete diffusion and language generation can benefit from exact discrete guidance, search-based trajectory optimization, distribution-level policy learning, and latent-space RL steering, effectively bridging continuous flow principles with discrete token generation. 

### **4.9 Image Restoration and Super-Resolution** 

Reinforcement-based alignment has also been extended to image restoration and enhancement tasks, where models must recover high-quality content from degraded inputs under uncertain corruption conditions. As shown in Table 16, **LRPO** [3] is the first work introducing online RL to **blind face restoration** , addressing unknown degradation types and severity through a **composite reward function** that jointly evaluates facial identity preservation, perceptual quality, and degradation removal effectiveness, while incorporating **likelihood regularization** to prevent restored outputs from deviating from natural image distributions. **Pref-Restore** [167] adopts a **hierarchical restoration framework** , separating coarse structural recovery and fine texture refinement, and applies stagespecific rewards with **RL preference constraints** embedded in the diffusion loop to ensure humanaligned restoration trajectories. **FinPercep-RM** [80] introduces **spatially-aware degradation maps** for super-resolution, allocating region-dependent degradation weights so RL can prioritize heavily corrupted areas, combined with **co-evolutionary curriculum learning** where reward and generation models progressively adapt to increasingly challenging degradations. **Diffusion Restoration via RL** [159] leverages **MLLM-based IQA (Image Quality Assessment)** as reward signals, converting natural language quality evaluations into scalar rewards, and employs a **difficulty-adaptive RL/SFT hybrid** —using SFT for simpler degradations and RL for harder cases. For enhancement efficiency, 

30 

Table 16: Extensions of GRPO-based alignment in image restoration and super-resolution. These works address blind degradation, hierarchical restoration, spatially adaptive weighting, language- <u>guided quality assessment, and hybrid efficiency-oriented enhancement architectures.</u> 

|**Category**|**Method**|**Core Innovation**|**Key Contribution / Result**|
|---|---|---|---|
|Blind Restoration|LRPO [3]<br>Diffusion Restoration<br>via RL [159]|Online RL for blind face restoration with composite<br>reward<br>MLLM-based IQA reward + RL/SFT hybrid<br>training|Identity + perceptual + degradation removal reward;<br>likelihood regularization<br>Difficulty-adaptive switching between SFT and RL|
|Hierarchical Restoration|Pref-Restore [167]<br>FinPercep-RM [80]|Two-stage coarse-to-fine restoration framework<br>Spatially-aware degradation maps + co-evolutionary<br>curriculum|Stage-specific RL preference constraints within<br>diffusion loop<br>Region-weighted rewards for heavily corrupted<br>areas|
|Efficiency &<br>Hybrid Enhancement|FlowLUT [47]<br>ReasonX [25]|LUT-based global adjustment + flow matching<br>refinement<br>MLLM perceptual reward for intrinsic image<br>decomposition|Fast global color/contrast correction with local<br>detail enhancement<br>9–25% WHDR reduction via language-guided<br>supervision|


**FlowLUT** [47] integrates **look-up tables (LUT)** for fast global color and contrast adjustment with flow matching for complex local refinement. Finally, **ReasonX** [25] applies MLLM perceptual judgment as GRPO rewards to **intrinsic image decomposition** , achieving a **9–25%** reduction in WHDR (Weighted Human Disagreement Rate). Collectively, these works demonstrate that composite rewards, hierarchical optimization, spatially adaptive weighting, curriculum-based co-evolution, language-guided quality assessment, and hybrid enhancement architectures are key to extending GRPO-style alignment to restoration and enhancement domains. 

## **5 Future Outlook** 

Looking forward, Flow-GRPO research is poised to evolve along several interconnected directions. A central challenge lies in developing a **unified theoretical framework** that coherently integrates dense reward design, efficient sampling, diversity preservation, and stable training dynamics, while providing convergence guarantees in continuous generative models and clarifying the SDE–ODE training–inference gap. As current empirical validation remains limited at extreme scales, systematic studies on **>** 10 **B-parameter models** are necessary to assess stability, scalability, and sample efficiency under large-scale training regimes. In video and long-horizon generation, improved **temporal reward modeling and credit assignment** mechanisms are required to ensure consistent behavior over extended sequences. Multi-objective optimization, as explored by APEX and MapReduce LoRA, raises open questions regarding **Pareto-optimal alignment** and principled trade-offs across competing reward dimensions. Another promising direction is **inference-time alignment** , where adaptive mechanisms can flexibly accommodate diverse user preferences without retraining. Beyond vision, Flow-GRPO’s expansion into scientific modeling—including PDE solvers, molecular force fields, and crystal structure generation—suggests a broader applicability to physically grounded domains. Meanwhile, **reasoning-augmented generation** and unified understanding–generation architectures point toward deeper cognitive integration, where intermediate reasoning and bidirectional reward signals shape generation quality. Finally, extending Flow-GRPO to **embodied intelligence** highlights the potential for continuous control, simulation-to-real transfer, and policy alignment in high-dimensional action spaces. Collectively, these directions indicate that Flow-GRPO is evolving from a task-specific alignment technique into a general reinforcement-driven framework for scalable, controllable, and multimodal generative intelligence. 

## **References** 

- [1] K. Ashutosh, X. Wang, X. Yin, K. Grauman, A. Polyak, I. Misra, and R. Girdhar. Human detectors are surprisingly powerful reward models. _arXiv preprint arXiv:2601.14037_ , 2026. 

31 

- [2] Q. Bai, Q. Wang, H. Ouyang, Y. Yu, H. Wang, W. Wang, K. L. Cheng, S. Ma, Y. Zeng, Z. Liu, et al. Scaling instruction-based video editing with a high-quality synthetic dataset. _arXiv preprint arXiv:2510.15742_ , 2025. 

- [3] W. Bin, Y. Liu, C. Zhang, Y. Zhao, and W. Wang. Lrpo: Enhancing blind face restoration through online reinforcement learning. 2025. 

- [4] K. Black, M. Janner, Y. Du, I. Kostrikov, and S. Levine. Training diffusion models with reinforcement learning. _arXiv preprint arXiv:2305.13301_ , 2023. 

- [5] S. Borse, F. Farhadzadeh, M. Hayat, and F. Porikli. Resolving the identity crisis in text-to-image generation, 2026. 

- [6] Z. Cao, T. Wang, J. Wang, Y. Wang, Y. Zhang, J. Chen, M. Deng, J. Wang, Y. Guo, C. Liao, et al. T2av-compass: Towards unified evaluation for text-to-audio-video generation. _arXiv preprint arXiv:2512.21094_ , 2025. 

- [7] C. Chen, S. Hu, J. Zhu, M. Wu, J. Chen, Y. Li, N. Huang, C. Fang, J. Wu, X. Chu, et al. Taming preference mode collapse via directional decoupling alignment in diffusion reinforcement learning. _arXiv preprint arXiv:2512.24146_ , 2025. 

- [8] C.-Y. Chen, Z. Wang, Q. Chen, Z. Ye, M. Shi, Y. Zhao, Y. Zhao, H. Qu, W.-A. Lin, Y. Shen, et al. Mapreduce lora: Advancing the pareto front in multi-preference optimization for generative models. _arXiv preprint arXiv:2511.20629_ , 2025. 

- [9] D. Chen, X. Zhuang, J. Xu, L. Xie, Z. Wang, J. Zhuang, H. Yang, L. Dou, X. He, X. Wu, et al. Apex: Learning adaptive priorities for multi-objective alignment in vision-language generation. _arXiv preprint arXiv:2601.06574_ , 2026. 

- [10] G. Chen, S. Huang, K. Liu, J. Zhu, X. Qu, P. Chen, Y. Cheng, and Y. Sun. Flash-dmd: Towards high-fidelity few-step image generation with efficient distillation and joint reinforcement learning. _arXiv preprint arXiv:2511.20549_ , 2025. 

- [11] G. Chen, X. Zhang, Z. Weng, J. Zheng, D. Shen, C. Ding, W.-Q. Zhang, and Z. Chen. Yingmusic-svc: Real-world robust zero-shot singing voice conversion with flow-grpo and singing-specific inductive biases. _arXiv preprint arXiv:2512.04793_ , 2025. 

- [12] J. Chen, P. Hansen-Estruch, X. Han, Y. Hu, E. Dinan, A. Kamath, M. Drozdzal, R. AskariHemmat, L. Zettlemoyer, and M. Ghazvininejad. Unified text-image generation with weaknesstargeted post-training. _arXiv preprint arXiv:2601.04339_ , 2026. 

- [13] J. Chen, L. Xue, Z. Xu, X. Pan, S. Yang, C. Qin, A. Yan, H. Zhou, Z. Chen, L. Huang, et al. Blip3o-next: Next frontier of native image generation. _arXiv preprint arXiv:2510.15857_ , 2025. 

- [14] K. Chen, Z. Liu, T. Zhang, Z. Guo, S. Xu, H. Lin, H. Zang, Q. Zhang, Z. Yu, G. Fan, et al. _π_ rl: Online rl fine-tuning for flow-based vision-language-action models. _arXiv preprint arXiv:2510.25889_ , 2025. 

- [15] K. Chen, Z. Xu, Y. Shen, Z. Lin, Y. Yao, and L. Huang. Superflow: Training flow matching models with rl on the fly. _arXiv preprint arXiv:2512.17951_ , 2025. 

- [16] T. Chen, H. Ma, N. Li, K. Wang, and B. Dai. One-step flow policy mirror descent. _arXiv preprint arXiv:2507.23675_ , 2025. 

- [17] Z. Chen and S. Deng. Flow marching for a generative pde foundation model. _arXiv preprint arXiv:2509.18611_ , 2025. 

- [18] Z. Chen, Y. Guo, Z. Chu, M. Luo, Y. Shen, M. Sun, J. Hu, S. Xie, K. Yang, P. Shi, et al. Socialnav: Training human-inspired foundation model for socially-aware embodied navigation. _arXiv preprint arXiv:2511.21135_ , 2025. 

- [19] J. Cheng, L. Hou, X. Tao, and J. Liao. Video-as-answer: Predict and generate next video event with joint-grpo. _arXiv preprint arXiv:2511.16669_ , 2025. 

32 

- [20] J. Choi, Y. Zhu, W. Guo, P. Molodyk, B. Yuan, J. Bai, Y. Xin, M. Tao, and Y. Chen. Rethinking the design space of reinforcement learning for diffusion models: On the importance of likelihood estimation beyond loss design. _arXiv preprint arXiv:2602.04663_ , 2026. 

- [21] X. Cong, H. Yang, A. Wang, Y. Wang, Y. Yang, C. Zhang, and C. Ma. Viva: Vlm-guided instruction-based video editing with reward optimization. _arXiv preprint arXiv:2512.16906_ , 2025. 

- [22] J. Cui, J. Wu, M. Li, T. Yang, X. Li, R. Wang, A. Bai, Y. Ban, and C.-J. Hsieh. Self-forcing++: Towards minute-scale high-quality video generation. _arXiv preprint arXiv:2510.02283_ , 2025. 

- [23] H. Deng, K. Yan, C. Mao, X. Wang, Y. Liu, C. Gao, and N. Sang. Densegrpo: From sparse to dense reward for flow matching model alignment. _arXiv preprint arXiv:2601.20218_ , 2026. 

- [24] Z. Ding and W. Ye. Treegrpo: Tree-advantage grpo for online rl post-training of diffusion models. _arXiv preprint arXiv:2512.08153_ , 2025. 

- [25] A. Dirik, T. Wang, D. Ceylan, S. Zafeiriou, and A. Frühstück. Reasonx: Mllm-guided intrinsic image decomposition. _arXiv preprint arXiv:2512.04222_ , 2025. 

- [26] Z. Du, Y. Wang, Q. Chen, X. Shi, X. Lv, T. Zhao, Z. Gao, Y. Yang, C. Gao, H. Wang, et al. Cosyvoice 2: Scalable streaming speech synthesis with large language models. _arXiv preprint arXiv:2412.10117_ , 2024. 

- [27] Z. Fang, J. Zheng, Q. Gao, X. Gao, and J. Sulam. Proxt2i: Efficient reward-guided text-toimage generation via proximal diffusion. _arXiv preprint arXiv:2511.18742_ , 2025. 

- [28] X. Feng, Y. Li, Z. Wan, Z. Gao, J. Yuan, D. Chen, and C. Qiao. Rubricrl: Simple generalizable rewards for text-to-image generation. _arXiv preprint arXiv:2511.20651_ , 2025. 

- [29] X. Fu, L. Ma, Z. Guo, G. Zhou, C. Wang, S. Dong, S. Zhou, X. Liu, J. Fu, T. L. Sin, et al. Dynamic-treerpo: Breaking the independent trajectory bottleneck with structured sampling. _arXiv preprint arXiv:2509.23352_ , 2025. 

- [30] Y. Gao, H. Guo, T. Hoang, W. Huang, L. Jiang, F. Kong, H. Li, J. Li, L. Li, X. Li, et al. Seedance 1.0: Exploring the boundaries of video generation models. _arXiv preprint arXiv:2506.09113_ , 2025. 

- [31] S. Ge, C. Huang, Y. Ai, Q. Fan, H. Huang, and R. He. Expand and prune: Maximizing trajectory diversity for effective grpo in generative models. _arXiv preprint arXiv:2512.15347_ , 2025. 

- [32] D. Ghosh, H. Hajishirzi, and L. Schmidt. Geneval: An object-focused framework for evaluating text-to-image alignment. _Advances in Neural Information Processing Systems_ , 36:52132– 52152, 2023. 

- [33] H. Go, D. Narnhofer, G. Bhat, P. Truong, F. Tombari, and K. Schindler. Vist3a: Text-to3d by stitching a multi-view reconstruction network to a video generator. _arXiv preprint arXiv:2510.13454_ , 2025. 

- [34] Y. Gong, X. Wang, J. Wu, S. Wang, Y. Wang, and X. Wu. Onereward: Unified mask-guided image generation via multi-task human preference learning. _arXiv preprint arXiv:2508.21066_ , 2025. 

- [35] R. L. GUIDANCE. Inference-time alignment control for diffu. 

- [36] X. Guo, F. Ye, X. Li, P. Tu, P. Zhang, Q. Sun, S. Zhao, X. Hou, and Q. He. Dreamid-v: Bridging the image-to-video gap for high-fidelity face swapping via diffusion transformer. _arXiv preprint arXiv:2601.01425_ , 2026. 

- [37] Y. Guo, J. Liu, Z. Wang, H. Chen, X. Sun, Y. Zhao, J. Wu, X. Yu, Z. Liu, and E. Barsoum. Imagedoctor: Diagnosing text-to-image generation via grounded image reasoning. _arXiv preprint arXiv:2510.01010_ , 2025. 

33 

- [38] Z. Guo, L. Ma, X. Fu, G. Zhou, L. Yang, Y. Zhou, L. Liu, Y. He, X. Liu, S. Dong, et al. Repainter: Empowering e-commerce object removal via spatial-matting reinforcement learning. _arXiv preprint arXiv:2510.07721_ , 2025. 

- [39] D. He, G. Feng, X. Ge, Y. Niu, Y. Zhang, B. Ma, G. Song, Y. Liu, and H. Li. Neighbor grpo: Contrastive ode policy optimization aligns flow models. _arXiv preprint arXiv:2511.16955_ , 2025. 

- [40] H. He, Y. Ye, J. Liu, J. Liang, Z. Wang, Z. Yuan, X. Wang, H. Mao, P. Wan, and L. Pan. Gardo: Reinforcing diffusion models without reward hacking. _arXiv preprint arXiv:2512.24138_ , 2025. 

- [41] R. He, Y. Cheng, T. Hang, Z. Li, Y. Xu, Z. Yin, S. Zhang, W. Dai, P. Du, A. Ma, et al. Re-align: Structured reasoning-guided alignment for in-context image generation and editing. _arXiv preprint arXiv:2601.05124_ , 2026. 

- [42] X. He, S. Fu, Y. Zhao, W. Li, J. Yang, D. Yin, F. Rao, and B. Zhang. Tempflow-grpo: When timing matters for grpo in flow models. _arXiv preprint arXiv:2508.04324_ , 2025. 

- [43] P. Hoellmer and S. Martiniani. Open materials generation with inference-time reinforcement learning. _arXiv preprint arXiv:2602.00424_ , 2026. 

- [44] P. Holderrieth, D. Chen, L. Eyring, I. Shah, G. Anantharaman, Y. He, Z. Akata, T. Jaakkola, N. M. Boffi, and M. Simchowitz. Diamond maps: Efficient reward alignment via stochastic flow maps. _arXiv preprint arXiv:2602.05993_ , 2026. 

- [45] P. Holderrieth, U. Singer, T. Jaakkola, R. T. Chen, Y. Lipman, and B. Karrer. Glass flows: Transition sampling for alignment of flow and diffusion models. _arXiv preprint arXiv:2509.25170_ , 2025. 

- [46] Y. Hong, K.-C. Kao, H. Zhou, and C.-J. Hsieh. Understanding reward hacking in text-to-image reinforcement learning. _arXiv preprint arXiv:2601.03468_ , 2026. 

- [47] L. Hu, C. Wu, A. Wang, D. Lu, G. Zhang, and Z. Zheng. Flowlut: Efficient image enhancement via differentiable luts and iterative flow matching. _arXiv preprint arXiv:2509.23608_ , 2025. 

- [48] Z. Huang, Y. Shu, H. Fang, Q. Long, W. Wang, Q. Guo, T. Ge, and L. Gan. From competition to synergy: Unlocking reinforcement learning for subject-driven image generation. _arXiv preprint arXiv:2510.18263_ , 2025. 

- [49] G. Jia, J. Hu, X. Long, K. Tian, K. Zhang, K. Zhao, N. Ding, and B. Zhou. Emotiondirector: Bridging affective shortcut in emotion-oriented image generation. _arXiv preprint arXiv:2512.19479_ , 2025. 

- [50] J. Jia, K. Shu, G. Yang, L. Xing, X. Chen, and A. Liu. Emofeedback<sup>2</sup> : Reinforcement of continuous emotional image generation via lvlm-based reward and textual feedback. _arXiv preprint arXiv:2511.19982_ , 2025. 

- [51] D. Jiang, D. Liu, Z. Wang, Q. Wu, L. Li, H. Li, X. Jin, D. Liu, Z. Li, B. Zhang, et al. Distribution matching distillation meets reinforcement learning. _arXiv preprint arXiv:2511.13649_ , 2025. 

- [52] S. Jiao, Y. Lin, Y. Zhong, Q. She, W. Zhou, X. Lan, Z. Huang, F. Yu, Y. Yu, Y. Zhao, et al. Thinkgen: Generalized thinking for visual generation. _arXiv preprint arXiv:2512.23568_ , 2025. 

- [53] P. Jin, D. Huang, C. Li, S. Cheng, Y. Zhao, X. Zheng, J. Zhu, S. Xing, B. Dou, R. Zhang, et al. Realbench: Benchmarking verilog generation models with real-world ip designs. _arXiv preprint arXiv:2507.16200_ , 2025. 

- [54] H. Kang, Y. Zhang, N. L. Kuang, Y.-A. Ma, and L. Qin. Beyond mode elicitation: Diversity-preserving reinforcement learning via latent diffusion reasoner. _arXiv preprint arXiv:2602.01705_ , 2026. 

- [55] H. Kang, Y. Zhang, N. L. Kuang, N. Majamaki, N. Jaitly, Y.-A. Ma, and L. Qin. Ladir: Latent diffusion enhances llms for text reasoning. _arXiv preprint arXiv:2510.04573_ , 2025. 

34 

- [56] Y. Kirstain, A. Polyak, U. Singer, S. Matiana, J. Penna, and O. Levy. Pick-a-pic: An open dataset of user preferences for text-to-image generation. _Advances in neural information processing systems_ , 36:36652–36663, 2023. 

- [57] S. Kou, J. Jin, Z. Zhou, Y. Ma, Y. Wang, Q. Chen, P. Jiang, X. Yang, J. Zhu, K. Yu, et al. Think-then-generate: Reasoning-aware text-to-image diffusion with llm encoders. _arXiv preprint arXiv:2601.10332_ , 2026. 

- [58] N. Kumari, S.-Y. Wang, N. Zhao, Y. Nitzan, Y. Li, K. K. Singh, R. Zhang, E. Shechtman, J.-Y. Zhu, and X. Huang. Learning an image editing model without image editing pairs. _arXiv preprint arXiv:2510.14978_ , 2025. 

- [59] J. Lee and J. C. Ye. Pcpo: Proportionate credit policy optimization for aligning image generation models. _arXiv preprint arXiv:2509.25774_ , 2025. 

- [60] Z. Lei, S. Yin, Y. Xiong, Y. Ding, W. Huang, Y. Wei, Q. Xu, Y. Li, W. Li, Y. Wang, et al. Embomatrix: A scalable training-ground for embodied decision-making. _arXiv preprint arXiv:2510.12072_ , 2025. 

- [61] H. Li, L. Jiang, Q. Yan, Y. Song, H. Kang, Z. Liu, X. Lu, B. Wu, and D. Cai. Thinkrledit: Thinking in reinforcement learning for reasoning-centric image editing. _arXiv preprint arXiv:2601.03467_ , 2026. 

- [62] J. Li, Y. Cui, T. Huang, Y. Ma, C. Fan, M. Yang, and Z. Zhong. Mixgrpo: Unlocking flow-based grpo efficiency with mixed ode-sde. _arXiv preprint arXiv:2507.21802_ , 2025. 

- [63] R. Li, Y. Liang, Z. Ni, H. Huang, C. Zhang, and X. Li. Growing with the generator: Self-paced grpo for video generation. _arXiv preprint arXiv:2511.19356_ , 2025. 

- [64] X. Li, Z. Chen, R. Zhao, F. Schiffers, Z. Liao, and V. Bhat. What happens next? next scene prediction with a unified video model. _arXiv preprint arXiv:2512.13015_ , 2025. 

- [65] Y. Li, X. He, Z.-X. Zou, Z. Liu, W. Ouyang, D. Liang, and Y.-P. Cao. Shapegen: Towards high-quality 3d shape synthesis. In _Proceedings of the SIGGRAPH Asia 2025 Conference Papers_ , pages 1–12, 2025. 

- [66] Y. Li, L. Huang, L. Xia, W. Zhang, and M. Gerstein. Elign: Equivariant diffusion model alignment from foundational machine learning force fields. _arXiv preprint arXiv:2601.21985_ , 2026. 

- [67] Y. Li, L. Liu, X. Zhang, W. Xue, W. Luo, Y. Guo, and Q. Tian. Cogniedit: Dense gradient flow optimization for fine-grained image editing. _arXiv preprint arXiv:2512.13276_ , 2025. 

- [68] Y. Li, Y. Wang, Y. Zhu, Z. Zhao, M. Lu, Q. She, and S. Zhang. Branchgrpo: Stable and efficient grpo with structured branching in diffusion models. _arXiv preprint arXiv:2509.06040_ , 2025. 

- [69] Y. Li, Z.-X. Zou, Z. Liu, D. Wang, Y. Liang, Z. Yu, X. Liu, Y.-C. Guo, D. Liang, W. Ouyang, et al. Triposg: High-fidelity 3d shape synthesis using large-scale rectified flow models. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 2025. 

- [70] Z. Li, Z. Liu, Q. Zhang, B. Lin, F. Wu, S. Yuan, Z. Yan, Y. Ye, W. Yu, Y. Niu, et al. Uniworld-v2: Reinforce image editing with diffusion negative-aware finetuning and mllm implicit feedback. _arXiv preprint arXiv:2510.16888_ , 2025. 

- [71] J. Lian, R. Zhong, Z. Zhou, X. Mi, Y. Hao, Y. Zhou, Q. Lu, L. Hu, and J. Yan. Solireward: Mitigating susceptibility to reward hacking and annotation noise in video generation reward models. _arXiv preprint arXiv:2512.22170_ , 2025. 

- [72] Y. Lin, L. Wang, K. Lin, Z. Lin, K. Gong, W. Li, B. Lin, Z. Li, S. Zhang, Y. Peng, et al. Jarvisevo: Towards a self-evolving photo editing agent with synergistic editor-evaluator optimization. _arXiv preprint arXiv:2511.23002_ , 2025. 

- [73] Y. Lipman, R. T. Chen, H. Ben-Hamu, M. Nickel, and M. Le. Flow matching for generative modeling. _arXiv preprint arXiv:2210.02747_ , 2022. 

35 

- [74] H. Liu, H. Huang, J. Wang, C. Liu, X. Li, and X. Ji. Diversegrpo: Mitigating mode collapse in image generation via diversity-aware grpo. _arXiv preprint arXiv:2512.21514_ , 2025. 

- [75] H. Liu, D. Liu, M. Zhuge, Z. Zhou, T. Xie, S. He, Y. Yang, S. Liu, Y. Cong, J. Guo, et al. Mixture of states: Routing token-level dynamics for multimodal generation. _arXiv preprint arXiv:2511.12207_ , 2025. 

- [76] J. Liu, H. Li, Z. Sun, C. Chen, Y. Bian, B. Wang, D. Dong, C. Chen, and Z. Wang. Beyond the dirac delta: Mitigating diversity collapse in reinforcement fine-tuning for versatile image generation. _arXiv preprint arXiv:2601.12401_ , 2026. 

- [77] J. Liu, G. Liu, J. Liang, Y. Li, J. Liu, X. Wang, P. Wan, D. Zhang, and W. Ouyang. Flow-grpo: Training flow matching models via online rl. _arXiv preprint arXiv:2505.05470_ , 2025. 

- [78] Q. Liu, Z. Liu, D. Zhang, and K. Jia. Nabla-r2d3: Effective and efficient 3d diffusion alignment with 2d rewards. _arXiv preprint arXiv:2506.15684_ , 2025. 

- [79] X. Liu, H. Yuan, Y. Wei, J. Xing, Y. Han, J. Pan, Y. Ma, C.-M. Chan, K. Zhao, S. Zhang, et al. Revise: Towards reason-informed video editing in unified models with self-reflective learning. _arXiv preprint arXiv:2512.09924_ , 2025. 

- [80] Y. Liu, Z. Fan, J. Huang, J. Xiao, D. Li, W. Zhang, L. Bai, X. Fu, and Z.-J. Zha. Finperceprm: A fine-grained reward model and co-evolutionary curriculum for rl-based real-world super-resolution. _arXiv preprint arXiv:2512.22647_ , 2025. 

- [81] Y. Liu, Z. Ouyang, S. Lou, and Y. Song. Omnirefiner: Reinforcement-guided local diffusion refinement. _arXiv preprint arXiv:2511.19990_ , 2025. 

- [82] Z. Liu, X. Bao, P. Li, J. Zhou, Z. Liao, Y. He, K. Jiang, C.-W. Xie, Y. Zheng, and H. Xie. Showtable: Unlocking creative table visualization with collaborative reflection and refinement. _arXiv preprint arXiv:2512.13303_ , 2025. 

- [83] Z. Liu, K. Valencia, and J. Cui. Video text preservation with synthetic text-rich videos. _arXiv preprint arXiv:2511.05573_ , 2025. 

- [84] C. Lu, Y. Zhou, F. Bao, J. Chen, C. Li, and J. Zhu. Dpm-solver++: Fast solver for guided sampling of diffusion probabilistic models. _Machine Intelligence Research_ , pages 1–22, 2025. 

- [85] Y. Lu, Y. Zeng, H. Li, H. Ouyang, Q. Wang, K. L. Cheng, J. Zhu, H. Cao, Z. Zhang, X. Zhu, et al. Reward forcing: Efficient streaming video generation with rewarded distribution matching distillation. _arXiv preprint arXiv:2512.04678_ , 2025. 

- [86] X. Luo, J. Wang, C. Wu, S. Xiao, X. Jiang, D. Lian, J. Zhang, D. Liu, et al. Editscore: Unlocking online rl for image editing via high-fidelity reward modeling. _arXiv preprint arXiv:2509.23909_ , 2025. 

- [87] Y. Luo, P. Du, B. Li, S. Du, T. Zhang, Y. Chang, K. Wu, K. Gai, and X. Wang. Sample by step, optimize by chunk: Chunk-level grpo for text-to-image generation. _arXiv preprint arXiv:2510.21583_ , 2025. 

- [88] Y. Luo, T. Hu, and J. Tang. Reinforcing diffusion models by direct group preference optimization. _arXiv preprint arXiv:2510.08425_ , 2025. 

- [89] Y. Luo, X. Hu, K. Fan, H. Sun, Z. Chen, B. Xia, T. Zhang, Y. Chang, and X. Wang. Reinforcement learning meets masked generative models: Mask-grpo for text-to-image generation. _arXiv preprint arXiv:2510.13418_ , 2025. 

- [90] M. Lyu, Y. Sun, E. Lin, H. Li, R. Chen, F. Zhao, and Y. Zeng. Reinforcement fine-tuning of flow-matching policies for vision-language-action models. _arXiv preprint arXiv:2510.09976_ , 2025. 

- [91] Q. Lyu, Z. Chen, C. Wang, H. Shi, S. Gao, R. Piao, Y. Zeng, J. Si, F. Ding, J. Li, et al. Multi-grpo: Multi-group advantage estimation for text-to-image generation with tree-based trajectories and multiple rewards. _arXiv preprint arXiv:2512.00743_ , 2025. 

36 

- [92] T. Ma, M. Zhang, Y. Wang, and Q. Ye. Consolidating reinforcement learning for multimodal discrete diffusion models. _arXiv preprint arXiv:2510.02880_ , 2025. 

- [93] X. Ma, H. Qiu, G. Zhang, Z. Zeng, S. Yang, L. Ma, and F. Zhao. Stage: Stable and generalizable grpo for autoregressive image generation. _arXiv preprint arXiv:2509.25027_ , 2025. 

- [94] W. Mao, H. Chen, Z. Yang, and M. Z. Shou. The image as its own reward: Reinforcement learning with adversarial reward for image generation. _arXiv preprint arXiv:2511.20256_ , 2025. 

- [95] D. McAllister, S. Ge, B. Yi, C. M. Kim, E. Weber, H. Choi, H. Feng, and A. Kanazawa. Flow matching policy gradients. _arXiv preprint arXiv:2507.21053_ , 2025. 

- [96] X. Meng, Z. Zhang, Z. Zhang, J. Liao, L. Qin, and W. Wang. Identity-grpo: Optimizing multi-human identity-preserving video generation via reinforcement learning. _arXiv preprint arXiv:2510.14256_ , 2025. 

- [97] Y. Mi, H. Li, Y. Zhao, C. Li, H. Wu, X. Ma, S.-C. Zhu, Y. N. Wu, and Q. Li. Milr: Improving multimodal image generation via test-time latent reasoning. _arXiv preprint arXiv:2509.22761_ , 2025. 

- [98] T. MODEL. Manzano: Asimple and scalable unified mul-timodal model with a hybrid vision tokenizer. 

- [99] Y. Ouyang, L. Xie, H. Zha, and G. Cheng. Alignment of diffusion model and flow matching for text-to-image generation. _arXiv preprint arXiv:2602.00413_ , 2026. 

- [100] P. Pan, J. Zhao, Y. Lin, C. Lin, C. Li, H. Liu, T. Shen, and Y. Mu. Id-crafter: Vlm-grounded online rl for compositional multi-subject video generation. _arXiv preprint arXiv:2511.00511_ , 2025. 

- [101] X. Pan, Z. Wan, X. Yu, X. Zheng, Y. Ke, M. Sun, R. Wang, Z. Wang, and I. Tsang. Savla: Spatially-aware flow-matching for vision-language-action reinforcement learning. _arXiv preprint arXiv:2602.00743_ , 2026. 

- [102] B. Ping, C. Jia, M. Luo, C. Xia, X. Shen, Z. Dang, and H. Qian. Paco-rl: Advancing reinforcement learning for consistent image generation with pairwise reward modeling. _arXiv preprint arXiv:2512.04784_ , 2025. 

- [103] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [104] T. Seedance, H. Chen, S. Chen, X. Chen, Y. Chen, Y. Chen, Z. Chen, F. Cheng, T. Cheng, X. Cheng, et al. Seedance 1.5 pro: A native audio-visual joint generation foundation model. _arXiv preprint arXiv:2512.13507_ , 2025. 

- [105] T. Seedream, Y. Chen, Y. Gao, L. Gong, M. Guo, Q. Guo, Z. Guo, X. Hou, W. Huang, Y. Huang, et al. Seedream 4.0: Toward next-generation multimodal image generation. _arXiv preprint arXiv:2509.20427_ , 2025. 

- [106] Y. Shao, J. Xiao, K. Zhu, Y. Liu, W. Zhai, Y. Cao, and Z.-J. Zha. Value-anchored group policy optimization for flow models. 

- [107] Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, X. Bi, H. Zhang, M. Zhang, Y. Li, Y. Wu, et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. _arXiv preprint arXiv:2402.03300_ , 2024. 

- [108] L. Shen, W. Jiang, Y. Zhu, J. Li, T. Ge, Z. Cao, and B. Zheng. Identity-preserving image-tovideo generation via reward-guided optimization. _arXiv preprint arXiv:2510.14255_ , 2025. 

- [109] J. Sheng, H. Zhao, H. Chen, D. D. Yao, and W. Tang. Understanding sampler stochasticity in training diffusion models for rlhf. _arXiv preprint arXiv:2510.10767_ , 2025. 

- [110] R. Singhal, Z. Horvitz, R. Teehan, M. Ren, Z. Yu, K. McKeown, and R. Ranganath. A general framework for inference-time scaling and steering of diffusion models. _arXiv preprint arXiv:2501.06848_ , 2025. 

37 

- [111] J. Song, J. Choi, K. Baek, S. Lee, D. Park, and S. Yoon. Dctext: Scheduled attention masking for visual text generation via divide-and-conquer strategy. _arXiv preprint arXiv:2512.01302_ , 2025. 

- [112] J. Song, C. Meng, and S. Ermon. Denoising diffusion implicit models. _arXiv preprint arXiv:2010.02502_ , 2020. 

- [113] X. Su, J. Huang, Y. Yusen, Z. Fang, and H. Kasai. Navigating the exploration-exploitation tradeoff in inference-time scaling of diffusion models. _arXiv preprint arXiv:2508.12361_ , 2025. 

- [114] S. Sun, L. Qu, H. Zhang, Y. Liu, Y. Song, X. Li, X. Wang, Y. Jiang, D. K. Du, X. Wu, et al. Var rl done right: Tackling asynchronous policy conflicts in visual autoregressive generation. _arXiv preprint arXiv:2601.02256_ , 2026. 

- [115] R. S. Sutton, D. McAllester, S. Singh, and Y. Mansour. Policy gradient methods for reinforcement learning with function approximation. _Advances in neural information processing systems_ , 12, 1999. 

- [116] J. Tan, L. Liu, J. Huanng, X. Zhang, Q. Tian, and F. Zhao. Parauni: Enhance generation in unified multimodal model with reinforcement-driven hierarchical parallel information interaction. _arXiv preprint arXiv:2512.05422_ , 2025. 

- [117] J. Tan, Z. Zhang, Y. Shen, J. Cai, S. Yang, J. Wu, W. Xia, Z. Tu, and S. Soatto. Talk2move: Reinforcement learning for text-instructed object-level geometric transformation in scenes. _arXiv preprint arXiv:2601.02356_ , 2026. 

- [118] X. Tan, J. Liu, Y. Fan, B.-B. Gao, X. Jiang, X. Chen, J. Peng, C. Wang, H. Wang, and F. Zheng. Consistentrft: Reducing visual hallucinations in flow-based reinforcement fine-tuning. _arXiv preprint arXiv:2602.03425_ , 2026. 

- [119] S. Tang, Y. Zhu, M. Tao, and P. Chatterjee. Tr2-d2: Tree search guided trajectory-aware fine-tuning for discrete diffusion. _arXiv preprint arXiv:2509.25171_ , 2025. 

- [120] Y. Tang, Z. Guo, K. Zhu, R. Zhang, Q. Chen, D. Jiang, J. Liu, B. Zeng, H. Song, D. Qu, et al. Are we ready for rl in text-to-3d generation? a progressive investigation. _arXiv preprint arXiv:2512.10949_ , 2025. 

- [121] Z. Tang, S. Yang, Z. Wang, B. Peng, Y. Li, B. Dong, and J. Dong. Endogenous reprompting: Self-evolving cognitive alignment for unified multimodal models. _arXiv preprint arXiv:2601.20305_ , 2026. 

- [122] F. Team, Q. Chen, Z. Fang, H. Huang, X. Huang, T. Jin, M. Lin, B. Liu, C. Liu, C. Ma, et al. Fsvideo: Fast speed video diffusion model in a highly-compressed latent space. _arXiv preprint arXiv:2602.02092_ , 2026. 

- [123] M. L. Team, X. Cai, Q. Huang, Z. Kang, H. Li, S. Liang, L. Ma, S. Ren, X. Wei, R. Xie, et al. Longcat-video technical report. _arXiv preprint arXiv:2510.22200_ , 2025. 

- [124] Y. Tian, L. Yang, J. Yang, A. Wang, Y. Tian, J. Zheng, H. Wang, Z. Teng, Z. Wang, Y. Wang, et al. Mmada-parallel: Multimodal large diffusion language models for thinking-aware editing and generation. _arXiv preprint arXiv:2511.09611_ , 2025. 

- [125] C. Tong, M. Chang, S. Zhang, Y. Wang, C. Liang, Z. Zhao, R. An, B. Zeng, Y. Shi, Y. Dai, et al. Cof-t2i: Video models as pure visual reasoners for text-to-image generation. _arXiv preprint arXiv:2601.10061_ , 2026. 

- [126] T. Wan, A. Wang, B. Ai, B. Wen, C. Mao, C.-W. Xie, D. Chen, F. Yu, H. Zhao, J. Yang, et al. Wan: Open and advanced large-scale video generative models. _arXiv preprint arXiv:2503.20314_ , 2025. 

- [127] Y. Wan, L. Ke, W. Yu, K.-W. Chang, and D. Yu. Motionedit: Benchmarking and learning motion-centric image editing. _arXiv preprint arXiv:2512.10284_ , 2025. 

- [128] Z. Wan, Y. Ouyang, L. Xie, F. Fang, H. Zha, and G. Cheng. Discrete guidance matching: Exact guidance for discrete flow matching. _arXiv preprint arXiv:2509.21912_ , 2025. 

38 

- [129] F. Wang and Z. Yu. Coefficients-preserving sampling for reinforcement learning with flow matching. _arXiv preprint arXiv:2509.05952_ , 2025. 

- [130] F.-Y. Wang, H. Zhang, M. Gharbi, H. Li, and T. Park. Unirl-zero: Reinforcement learning on unified models with joint language model and diffusion model experts. _arXiv preprint arXiv:2510.17937_ , 2025. 

- [131] F.-Y. Wang, H. Zhang, M. Gharbi, H. Li, and T. Park. Promptrl: Prompt matters in rl for flow-based image generation. _arXiv preprint arXiv:2602.01382_ , 2026. 

- [132] G.-H. Wang, L. Cao, T. Cui, M. Fu, X. Chen, P. Zhan, J. Zhao, L. Li, B. Fu, J. Liu, et al. Ovis-image technical report. _arXiv preprint arXiv:2511.22982_ , 2025. 

- [133] H. Wang, B. Tian, Y. Jiang, Z. Pan, S. Zhao, B. Ma, D. Chen, and X. Li. Flowse-grpo: Training flow matching speech enhancement via online reinforcement learning. _arXiv preprint arXiv:2601.16483_ , 2026. 

- [134] J. Wang, J. Hu, X. Ma, H. Ma, Y. Zeng, and X. Wei. Magicmirror: A large-scale dataset and benchmark for fine-grained artifacts assessment in text-to-image generation. _arXiv preprint arXiv:2509.10260_ , 2025. 

- [135] J. Wang, Y. Lai, A. Li, S. Zhang, J. Sun, N. Kang, C. Wu, Z. Li, and P. Luo. Fudoki: Discrete flow-based unified understanding and generation via kinetic-optimal velocities. _arXiv preprint arXiv:2505.20147_ , 2025. 

- [136] J. Wang, J. Liang, J. Liu, H. Liu, G. Liu, J. Zheng, W. Pang, A. Ma, Z. Xie, X. Wang, et al. Grpo-guard: Mitigating implicit over-optimization in flow matching via regulated clipping. _arXiv preprint arXiv:2510.22319_ , 2025. 

- [137] J. Wang, J. Lu, G. Xu, C. Chen, H. Yang, L. Wang, P. Chen, M. Chen, Z. Hu, L. Wu, et al. Tagrpo: Boosting grpo on image-to-video generation with direct trajectory alignment. _arXiv preprint arXiv:2601.05729_ , 2026. 

- [138] Q. Wang, J. Liu, J. Liang, Y. Jiang, Y. Zhang, J. Chen, Y. Zheng, X. Wang, P. Wan, X. Yue, et al. Vr-thinker: Boosting video reward models through thinking-with-image reasoning. _arXiv preprint arXiv:2510.10518_ , 2025. 

- [139] S. Wang, L. Wei, X. He, J. Ouyang, H. Lu, Z. Zhao, and Q. Tian. Psr: Scaling multi-subject personalized image generation with pairwise subject-consistency rewards. _arXiv preprint arXiv:2512.01236_ , 2025. 

- [140] Y. Wang, X. Chen, X. Xu, Y. Liu, and H. Zhao. Gdro: Group-level reward post-training suitable for diffusion models. _arXiv preprint arXiv:2601.02036_ , 2026. 

- [141] Y. Wang, Y. Li, S. Tulyakov, Y. Fu, and A. Kag. Diffusion-drf: Differentiable reward flow for video diffusion fine-tuning. _arXiv preprint arXiv:2601.04153_ , 2026. 

- [142] Y. Wang, Z. Li, Y. Zang, J. Bu, Y. Zhou, Y. Xin, J. He, C. Wang, Q. Lu, C. Jin, et al. Unigenbench++: A unified semantic evaluation benchmark for text-to-image generation. _arXiv preprint arXiv:2510.18701_ , 2025. 

- [143] Y. Wang, Z. Li, Y. Zang, Y. Zhou, J. Bu, C. Wang, Q. Lu, C. Jin, and J. Wang. Pref-grpo: Pairwise preference reward-based grpo for stable text-to-image reinforcement learning. _arXiv preprint arXiv:2508.20751_ , 2025. 

- [144] Y. Wang, B. Liao, H. Huang, J. Lu, O. Li, K. Liu, M. Wang, and X. Wang. Thinking with frames: Generative video distortion evaluation via frame reward model. _arXiv preprint arXiv:2601.04033_ , 2026. 

- [145] Y. Wang, Y. Zang, F. Han, J. Bu, Y. Zhou, C. Jin, and J. Wang. Unified personalized reward model for vision generation. _arXiv preprint arXiv:2602.02380_ , 2026. 

- [146] Z. Wang, X. Hu, Y. Wang, F. Xiong, M. Zhang, and X. Chu. Everything in its place: Benchmarking spatial intelligence of text-to-image models. _arXiv preprint arXiv:2601.20354_ , 2026. 

39 

- [147] Z. Wang, X. Xia, Z. Bie, J. Liu, D. Yu, J.-W. Bian, and C. Wang. Taming camera-controlled video generation with verifiable geometry reward. _arXiv preprint arXiv:2512.02870_ , 2025. 

- [148] H. Wei, B. Xu, H. Liu, S. Wu, J. Liu, Y. Peng, P. Wang, Z. Liu, J. He, Y. Xietian, et al. Skywork unipic 2.0: Building kontext model with online rl for unified multimodal model. _arXiv preprint arXiv:2509.04548_ , 2025. 

- [149] Y. Wen, Q. Shuai, D. Kang, J. Li, C. Wen, Y. Qian, N. Jiao, C. Chen, W. Chen, Y. Wang, et al. Hy-motion 1.0: Scaling flow matching models for text-to-motion generation. _arXiv preprint arXiv:2512.23464_ , 2025. 

- [150] C. Wu, J. Li, J. Zhou, J. Lin, K. Gao, K. Yan, S.-m. Yin, S. Bai, X. Xu, Y. Chen, et al. Qwen-image technical report. _arXiv preprint arXiv:2508.02324_ , 2025. 

- [151] J. Wu, Y. Gao, Z. Ye, M. Li, L. Li, H. Guo, J. Liu, Z. Xue, X. Hou, W. Liu, et al. Rewarddance: Reward scaling in visual generation. _arXiv preprint arXiv:2509.08826_ , 2025. 

- [152] J. Wu, Z. Wan, X. Yu, Y. Yang, B. An, and I. Tsang. Oscar: Orthogonal stochastic control for alignment-respecting diversity in flow matching. _arXiv preprint arXiv:2510.09060_ , 2025. 

- [153] J. Wu, X. Zhang, H. Yuan, X. Zhang, T. Huang, C. He, C. Deng, R. Zhang, Y. Wu, and M. Long. Visual generation unlocks human-like reasoning through multimodal world models. _arXiv preprint arXiv:2601.19834_ , 2026. 

- [154] T. Wu, Y. Jiang, Y. Lu, Z. Wang, Z. Huang, Z. Qin, and X. Li. Multicrafter: High-fidelity multi-subject generation via spatially disentangled attention and identity-aware reinforcement learning. 2025. 

- [155] X. Wu, Y. Hao, K. Sun, Y. Chen, F. Zhu, R. Zhao, and H. Li. Human preference score v2: A solid benchmark for evaluating human preferences of text-to-image synthesis. _arXiv preprint arXiv:2306.09341_ , 2023. 

- [156] X. Xie, J. Guo, and D. Gong. Hyperalign: Hypernetwork for efficient test-time alignment of diffusion models. _arXiv preprint arXiv:2601.15968_ , 2026. 

- [157] H. Xu, L. Huang, and F. Zhao. Highly efficient test-time scaling for t2i diffusion models with text embedding perturbation. _arXiv preprint arXiv:2512.03996_ , 2025. 

- [158] R. Xu, Y. Kai, X. Ren, J. Cheng, B. Ma, T. Zheng, and Q. Lu. Beyond reward margin: Rethinking and resolving likelihood displacement in diffusion models via video generation. _arXiv preprint arXiv:2511.19049_ , 2025. 

- [159] X. Xu, R. Chu, J. Wang, K. Zhou, W. Shu, H. Yang, S.-N. Lim, H. Chen, and L. Lin. Enhancing diffusion-based restoration models via difficulty-adaptive reinforcement learning with iqa reward. _arXiv preprint arXiv:2511.01645_ , 2025. 

- [160] H. Xue, Q. Chen, Z. Wang, X. Huang, E. Shechtman, J. Xie, and Y. Chen. Mogan: Improving motion quality in video diffusion via few-step motion adversarial post-training. _arXiv preprint arXiv:2511.21592_ , 2025. 

- [161] S. Xue, C. Ge, S. Zhang, Y. Li, and Z.-M. Ma. Advantage weighted matching: Aligning rl with pretraining in diffusion models. _arXiv preprint arXiv:2509.25050_ , 2025. 

- [162] Z. Xue, J. Wu, Y. Gao, F. Kong, L. Zhu, M. Chen, Z. Liu, W. Liu, Q. Guo, W. Huang, et al. Dancegrpo: Unleashing grpo on visual generation. _arXiv preprint arXiv:2505.07818_ , 2025. 

- [163] Z. Yan, K. Lin, Z. Li, J. Ye, H. Han, Z. Wang, H. Liu, B. Lin, H. Li, X. Xu, et al. Unified multimodal model as auto-encoder. _arXiv preprint arXiv:2509.09666_ , 2025. 

- [164] H. Yang, Y. Zhou, W. Han, R. Tao, Z. Qiu, J. Yang, and J. Shen. Hicogen: Hierarchical compositional text-to-image generation in diffusion models via reinforcement learning. _arXiv preprint arXiv:2511.19965_ , 2025. 

40 

- [165] Q. Yang, Y. Chen, Y. Yao, Y. Men, H. Liu, and M. Cui. Mcsc: Motion-corrective preference alignment for video generation with self-critic hierarchical reasoning. _arXiv preprint arXiv:2511.22974_ , 2025. 

- [166] S. Yang, B. Liu, and H. Chen. Policyflow: Policy optimization with continuous normalizing flow in reinforcement learning. _arXiv preprint arXiv:2602.01156_ , 2026. 

- [167] Z. Yao, J. Hu, K. Li, H. He, X. Zhang, S. Zeng, L. Zhu, and Y. Lu. Bridging information asymmetry: A hierarchical framework for deterministic blind face restoration. _arXiv preprint arXiv:2601.19506_ , 2026. 

- [168] H. Ye, K. Zheng, J. Xu, P. Li, H. Chen, J. Han, S. Liu, Q. Zhang, H. Mao, Z. Hao, et al. Data-regularized reinforcement learning for diffusion models at scale. _arXiv preprint arXiv:2512.04332_ , 2025. 

- [169] J. Ye, L. Zhu, Y. Guo, D. Jiang, Z. Huang, Y. Zhang, Z. Yan, H. Fu, C. He, and W. Li. Realgen: Photorealistic text-to-image generation via detector-guided rewards. _arXiv preprint arXiv:2512.00473_ , 2025. 

- [170] Y. Ye, T. He, S. Yang, and J. Bian. Reinforcement learning with inverse rewards for world model post-training. _arXiv preprint arXiv:2509.23958_ , 2025. 

- [171] Z. Ye, Q. Liu, C. Wei, Y. Zhang, X. Wang, P. Wan, K. Gai, and W. Luo. Visual-aware cot: Achieving high-fidelity visual consistency in unified models. _arXiv preprint arXiv:2512.19686_ , 2025. 

- [172] S. E. Yiflach, Y. Atzmon, and G. Chechik. Data-driven loss functions for inference-time optimization in text-to-image generation. _arXiv preprint arXiv:2509.02295_ , 2025. 

- [173] Z. Yin and X. Liu. Trim: Scalable 3d gaussian diffusion inference with temporal and spatial trimming. _arXiv preprint arXiv:2511.16642_ , 2025. 

- [174] B. Yu, J. Liu, and J. Cui. Smart-grpo: Smartly sampling noise for efficient rl of flow-matching models. _arXiv preprint arXiv:2510.02654_ , 2025. 

- [175] P. Yu, S. Kothawade, S. Xie, Y. N. Wu, and H. Fei. Designing instance-level sampling schedules via reinforce with james-stein shrinkage. _arXiv preprint arXiv:2511.22177_ , 2025. 

- [176] Q. Yu, C. Song, M. Sun, Z. Yu, V. K. Verma, S. Roy, S. Negi, H. Li, and D. Campbell. Ttsnap: Test-time scaling of diffusion models via noise-aware pruning. _arXiv preprint arXiv:2511.22242_ , 2025. 

- [177] S. Yuan, Y. Liu, Y. Yue, J. Zhang, W. Zuo, Q. Wang, F. Zhang, and G. Zhou. Ar-grpo: Training autoregressive image generation models via reinforcement learning. _arXiv preprint arXiv:2508.06924_ , 2025. 

- [178] Z. Yue, Z. Ni, F. Ye, J. Zhang, S. Shen, and Z. Mi. Know your step: Faster and better alignment for flow matching models via step-aware advantages. _arXiv preprint arXiv:2602.01591_ , 2026. 

- [179] A. Zarei, J. Pan, M. Gwilliam, S. Feizi, and Z. Yang. Agentcomp: From agentic reasoning to compositional mastery in text-to-image models. _arXiv preprint arXiv:2512.09081_ , 2025. 

- [180] G. Zhang, H. Yu, X. Ma, J. Zhang, Y. Pan, M. Yao, J. Xiao, L. Huang, and F. Zhao. Group critical-token policy optimization for autoregressive image generation. _arXiv preprint arXiv:2509.22485_ , 2025. 

- [181] J. Zhang, Z. Huang, C. Gu, Z. Ma, and L. Zhang. Reinforcing action policies by prophesying. _arXiv preprint arXiv:2511.20633_ , 2025. 

- [182] Q. Zhang, B. Gong, S. Tan, Z. Zhang, Y. Shen, X. Zhu, Y. Li, K. Yao, C. Shen, and C. Zou. Physrvg: Physics-aware unified reinforcement learning for video generative models. _arXiv preprint arXiv:2601.11087_ , 2026. 

- [183] Q. Zhang, M. Tao, and Y. Chen. gddim: Generalized denoising diffusion implicit models. _arXiv preprint arXiv:2206.05564_ , 2022. 

41 

- [184] S. Zhang, Z. Zhang, C. Dai, and Y. Duan. E-grpo: High entropy steps drive effective reinforcement learning for flow models. _arXiv preprint arXiv:2601.00423_ , 2026. 

- [185] X. Zhang, W. Li, S. Zhao, J. Li, L. Zhang, and J. Zhang. Vq-insight: Teaching vlms for ai-generated video quality understanding via progressive visual reinforcement learning. _arXiv preprint arXiv:2506.18564_ , 2025. 

- [186] Z. Zhang, X. Hao, H. Tang, Z. Zhang, J. Sheng, X. Li, Z. Li, L. Gao, D. Shi, D. Yin, et al. Cooper: A unified model for cooperative perception and reasoning in spatial intelligence. _arXiv preprint arXiv:2512.04563_ , 2025. 

- [187] K. Zhao, J. Shi, B. Zhu, J. Zhou, X. Shen, Y. Zhou, Q. Sun, and H. Zhang. Real-time motion-controllable autoregressive video diffusion. _arXiv preprint arXiv:2510.08131_ , 2025. 

- [188] Y. Zhao, X. Wang, L. Dong, W. Zhang, and Y. Yuan. Demystifying numerosity in diffusion models–limitations and remedies. _arXiv preprint arXiv:2510.11117_ , 2025. 

- [189] J. Zheng, C. Hao, G. Ma, X. Zhang, G. Chen, C. Ding, Z. Chen, and L. Xie. Yingmusic-singer: Zero-shot singing voice synthesis and editing with annotation-free melody guidance. _arXiv preprint arXiv:2512.04779_ , 2025. 

- [190] K. Zheng, H. Chen, H. Ye, H. Wang, Q. Zhang, K. Jiang, H. Su, S. Ermon, J. Zhu, and M.-Y. Liu. Diffusionnft: Online diffusion reinforcement with forward process. _arXiv preprint arXiv:2509.16117_ , 2025. 

- [191] Z. Zheng, T. Isobe, T. Shen, X. Jia, J. Zhao, X. Li, M. Ge, B. Li, Q. Wang, D. Li, et al. Layout-conditioned autoregressive text-to-image generation via structured masking. _arXiv preprint arXiv:2509.12046_ , 2025. 

- [192] R. Zhong, J. Lian, X. Mi, Z. Zhou, Y. Zhou, Q. Lu, and J. Yan. Euphonium: Steering video flow matching via process reward gradient guided stochastic dynamics. _arXiv preprint arXiv:2602.04928_ , 2026. 

- [193] D. Zhou, M. Li, Z. Yang, Y. Lu, Y. Xu, Z. Wang, Z. Huang, and Y. Yang. Bidedpo: Conditional image generation with simultaneous text and condition alignment. _arXiv preprint arXiv:2511.19268_ , 2025. 

- [194] R. Zhou, Z. Ni, T. Chen, Z. Liu, Y. Yue, Y. Wang, Y. Wang, J. Liu, and G. Huang. Co-grpo: Co-optimized group relative policy optimization for masked diffusion model. _arXiv preprint arXiv:2512.22288_ , 2025. 

- [195] S. Zhou, Q. Zhou, J. Hu, H. Yang, Y. Cao, J. Ma, Y. Ma, J. Song, T. Ge, C. Yu, et al. Unified thinker: A general reasoning modular core for image generation. _arXiv preprint arXiv:2601.03127_ , 2026. 

- [196] Y. Zhou, P. Ling, J. Bu, Y. Wang, Y. Zang, J. Wang, L. Niu, and G. Zhai. Fine-grained grpo for precise preference alignment in flow models. _arXiv preprint arXiv:2510.01982_ , 2025. 

- [197] L. Zhuo, R. Du, H. Xiao, Y. Li, D. Liu, R. Huang, W. Liu, X. Zhu, F.-Y. Wang, Z. Ma, et al. Lumina-next: Making lumina-t2x stronger and faster with next-dit. _Advances in Neural Information Processing Systems_ , 37:131278–131315, 2024. 

- [198] G. Zou, H. Wang, H. Wu, Y. Qian, Y. Wang, and W. Li. One step is enough: Dispersive meanflow policy optimization. _arXiv preprint arXiv:2601.20701_ , 2026. 

42 

