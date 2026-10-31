---
title: "Self-Correcting VLA: Online Action Refinement via Sparse World Imagination"
date: "2026-02-25"
authors: "Chenyv Liu; Wentao Tan; Lei Zhu; Fengling Li; Jingjing Li; Guoli Yang"
url: https://arxiv.org/abs/2602.21633
pdf: https://arxiv.org/pdf/2602.21633
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.21633)** / [論文ページ](https://arxiv.org/abs/2602.21633)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**Self-Correcting VLA: Online Action Refinement via Sparse World Imagination** 

**Chenyv Liu**<sup>1 *</sup> **Wentao Tan**<sup>1 *</sup> **Lei Zhu**<sup>1 �</sup> **Fengling Li**<sup>2</sup> **Jingjing Li**<sup>3</sup> **Guoli Yang**<sup>4</sup> **Heng Tao Shen**<sup>1</sup> 

# **Abstract** 

Standard vision-language-action (VLA) models rely on fitting statistical data priors, limiting their robust understanding of underlying physical dynamics. Reinforcement learning enhances physical grounding through exploration yet typically relies on external reward signals that remain isolated from the agent’s internal states. World action models have emerged as a promising paradigm that integrates imagination and control to enable predictive planning. However, they rely on implicit context modeling, lacking explicit mechanisms for self-improvement. To solve these problems, we propose Self-Correcting VLA (SCVLA), which achieve self-improvement by intrinsically guiding action refinement through sparse imagination. We first design sparse world imagination by integrating auxiliary predictive heads to forecast current task progress and future trajectory trends, thereby constraining the policy to encode short-term physical evolution. Then we introduce the online action refinement module to reshape progress-dependent dense rewards, adjusting trajectory orientation based on the predicted sparse future states. Evaluations on challenging robot manipulation tasks from simulation benchmarks and real-world settings demonstrate that SC-VLA achieve state-of-the-art performance, yielding the highest task throughput with **16%** fewer steps and a **9%** higher success rate than the best-performing baselines, alongside a **14%** gain in real-world experiments. Code is available at https:// github.com/Kisaragi0/SC-VLA. 

# **1. Introduction** 

Vision-language-action models (VLA) have driven recent advancements in embodied AI by bringing multimodal large 

*Equal contribution 1Tongji University 2University of Technology Sydney<sup>3</sup> University of Electronic Science and Technology of China<sup>4</sup> Advanced Institute of Big Data. Correspondence to: Lei Zhu _<_ leizhu0608@gmail.com _>_ . 

Preprint Version. 

language models (MLLMs) to physical control (Zitkovich et al., 2023; Driess et al., 2023; Kim et al., 2024; Team et al., 2024). By performing large-scale imitation learning on diverse robotic datasets, these architectures enable agents to translate natural language instructions directly into executable actions. However, this paradigm fundamentally relies on fitting the statistical patterns inherent in the pretraining data. Consequently, the learned policies mainly depend on memorized data priors rather than acquiring a robust understanding of the underlying physical dynamics (Chow et al., 2025; Zheng et al., 2024). 

To address the reliance on static priors, reinforcement learning introduces active interaction into the training process. Instead of passively cloning expert behaviors, agents optimize their policies by exploring the environment and learning from rewards. To implement this, several research paradigms have emerged. A prominent strategy employs online reinforcement learning algorithms, such as PPO (Schulman et al., 2017), to fine-tune pre-trained VLA for taskspecific adaptation (Liu et al., 2025; Lu et al., 2025). Alternatively, offline reinforcement learning methods seek to extract optimal policies from static datasets, enhancing performance without necessitating real-time interaction (Kumar et al., 2020; Chebotar et al., 2023). However, effective learning relies on the quality of feedback signals, which are often difficult to define manually for diverse tasks and scenarios. To address this, recent methods incorporate multimodal large language models to synthesize reward functions, using semantic reasoning to guide policy optimization (Lu et al., 2025; Zhai et al., 2025). Despite these advancements, a critical limitation persists: _whether manually defined or synthesized by models, these approaches typically rely on external reward signals to evaluate performance._ This reliance can introduce a disconnect between the external signals and the model’s internal states. Therefore, it is essential to explore efficient self-improvement strategies that facilitate the model’s native adaptation capabilities. 

To bridge this gap, world models offer a promising direction by establishing internal physical dynamics. However, current reinforcement learning algorithms for VLA typically treat world models and policies as independent modules, relying on closed-loop feedback for exploration (Hung et al., 2025). This separation overlooks the unique capability of another paradigm, termed **world action models** (Wu et al., 

1 


_Figure 1._ We present Self-Correcting VLA (SC-VLA), a novel framework designed to enhance physical grounding through intrinsic self-improvement. The model is equipped with Sparse World Imagination (SPI) to forecast task progress and future trajectory trends, and Online Action Refinement (OAR) to dynamically optimize policies via residual adjustments and reshaped rewards. SC-VLA achieves superior performance on ManiSkill and real-world ARX5 benchmarks, surpassing baselines in both success rate and execution throughput. 

2023; Zhao et al., 2025; Black et al., 2023), which natively support both action generation and multimodal future prediction. While this allows intrinsic evaluation via predicted future states, existing approaches lack explicit mechanisms to leverage these states to refine actions, failing to realize self-improvement aligned with the agent’s internal states. 

To achieve self-improvement by intrinsically guiding action refinement through future imagination, we propose Self-Correcting VLA (SC-VLA). This framework jointly generates actions while predicting sparse future states, enabling fine-grained trajectory refinement via residual reinforcement learning for complex manipulation tasks. SCVLA significantly enhances task success rate and throughput. Specifically, we introduce sparse world imagination, which integrates auxiliary predictive heads to forecast current task progress and future trajectory orientation as sparse world signals. This mechanism constrains the policy to encode short-term physical evolution prior to action generation. Based on this, we further propose online action refinement, which constructs dense rewards by evaluating the consistency between the current and future trajectory orientation. It employs imagination to deduce future action trends for reshaping intrinsic progress-dependent dense rewards, thereby eliminating reliance on external reward models. We evaluate our method on four challenging manipulation tasks (StackCube, PlaceSphere, LiftPegUpright, and PegInsertion), where SC-VLA demonstrates state-of-the-art 

performance with the highest task throughput. 

- We propose SC-VLA, a self-correcting framework that integrates offline action generation with online refinement. By introducing sparse world imagination to forecast sparse future states, it constrains the policy to encode physical evolution. 

- We develop online action refinement with residual reinforcement learning to adjust trajectory orientation. It constructs progress-dependent dense rewards using predicted future states, explicitly guiding the policy to align with the imagined future behavioral trends. 

- We conduct systematic evaluations on four tasks across both simulation and real-world robotic platform. The results demonstrate that SC-VLA achieves the best performance in task throughput and success rate on complex manipulation tasks. 

# **2. Related Works** 

**Vision-Language-Action Models.** Vision-LanguageAction (VLA) models integrate multimodal models into robotic control (Brohan et al., 2022; Li et al., 2023; Liu et al., 2024). RT-2 (Zitkovich et al., 2023) enables semantic transfer by modeling actions as discrete tokens, while OpenVLA (Kim et al., 2024) enhances cross-robot 

2 

generalization through efficient adaptation. Recently, GR00T (Bjorck et al., 2025) and _π_ 0 (Black et al., 2024) have improved real-time deployment and continuous action generation via dual-system architectures and flow matching, respectively. Despite these advances, existing methods rely heavily on offline imitation and current-step semantic alignment, lacking explicit modeling of physical evolution. 

**Reinforcement Learning for VLA.** The key to introducing reinforcement learning into pretrained VLA models lies in constructing effective external rewards to alleviate the sparse feedback problem. Existing approaches can be broadly categorized into three classes. The first class leverages the semantic reasoning capability of vision-language models (VLM) to directly evaluate execution processes or diagnose failure causes, thereby synthesizing trajectorylevel rewards or corrective signals, such as VLA-RL (Lu et al., 2025), VLAC (Zhai et al., 2025), Reflective SelfAdaptation (Li et al., 2025a), and World-Env (Xiao et al., 2025), which provide high-level semantic guidance through language understanding and causal reasoning. The second class designs rewards via explicit rules or auxiliary prediction objectives, including rule-based signals derived from remaining steps or temporal information (e.g., SelfImproving (Ghasemipour et al., 2025), _π_ 0<sup>_∗_</sup> _._ 6<sup>(Intelligence</sup> et al., 2025), and RFTF (Shu et al., 2025)), as well as approaches such as NORA-1.5 (Hung et al., 2025) that evaluate trajectory deviations using action-conditioned world models. The third class constructs rewards based on feature or trajectory similarity metrics, typically by comparing generated trajectories with target trajectories in pixel, perceptual, or latent feature spaces, as exemplified by ThinkAct (Huang et al., 2025) and VLA-RFT (Li et al., 2025b). Despite significantly improving exploration efficiency, these methods generally rely on external model inference, handcrafted rules, or similarity computations, which are decoupled from the policy’s internal representations and introduce additional computational and system complexity. In contrast, approaches that rely solely on scalar return prediction (e.g., ReinboT (Zhang et al., 2025)) struggle to provide fine-grained spatiotemporal geometric constraints. 

**World Action Models.** Unlike RL-based VLA methods that rely on external reward signals, world action models aim to jointly model action generation and future evolution within a unified framework, constraining policy behavior via latent contextual predictions and thereby enabling intrinsic guidance without explicit external rewards. GR-MG (Li et al., 2025c) conditions current actions on imagined future target images by generating pixel-level goals. FLARE (Zheng et al., 2025) further avoids highdimensional pixel synthesis by aligning future representations in latent space, improving both efficiency and stability. PAR (Song et al., 2025) proposes a physics-aware autore- 

gressive modeling paradigm that unifies vision and actions as continuous physical tokens, directly leveraging dynamical priors from video models for control. WorldVLA (Cen et al., 2025) alternates between predicting actions and future visual states in an autoregressive manner, mitigating error accumulation through attention masking and achieving mutual reinforcement between action generation and world modeling. Despite their ability to constrain policies with predictive latent context, the future signals in these approaches are typically encoded as implicit representations, lacking interpretable physical semantics or explicit self-evaluation mechanisms. As a result, they struggle to perform fine-grained corrections on short-horizon trajectories and cannot provide direct policy improvement signals in the same manner as reward-based paradigms. 

# **3. Preliminary** 

## **3.1. Basic Robot Policy** 

To address the multimodal distribution inherent in robot action generation, we adopt Flow Matching (FM) as the backbone of our policy. Compared to diffusion-based models, flow matching constructs deterministic optimal transport paths, significantly improving training efficiency and inference stability while preserving generation quality. 

Concretely, given an observation _o_ , conditional flow matching aims to learn an observation-conditioned vector field _vθ_ that continuously transforms samples from a prior noise distribution _p_ 0( _x_ ) = _N_ ( _x |_ 0 _, I_ ) into a target action distribution _p_ 1( _x_ ) _≈ q_ ( _a | o_ ). During training, we construct an optimal transport interpolation path 


which connects a noise sample _x_ 0 _∼ p_ 0 and a ground-truth action sample _x_ 1 _∼ q_ ( _a | o_ ). The corresponding target velocity field is given by _x_ 1 _− x_ 0. The model parameters are optimized by minimizing the mean squared error between the predicted vector field and the target velocity field: 


At inference time, the model starts from a prior noise sample and generates the final action by solving the corresponding ordinary differential equation (ODE) with a numerical integrator (e.g., Euler stepping): 


In the following sections, we build upon this conditional flow matching formulation and introduce additional structured predictive constraints to enhance the policy’s ability to model short-term physical evolution. 

3 

## **3.2. Soft Actor-Critic (SAC)** 

To enable stable and efficient policy optimization in continuous action spaces, we adopt Soft Actor-Critic (SAC) (Haarnoja et al., 2018) as the underlying reinforcement learning algorithm. SAC is an off-policy method based on the maximum entropy reinforcement learning framework, which augments the expected return objective with an entropy regularization term. This formulation encourages a balance between exploration and exploitation, leading to improved stability and robustness of the learned policy. The optimization objective of SAC is defined as: 


where _H_ ( _π_ ( _· | st_ )) denotes the entropy of the policy at state _st_ , and _α_ is an automatically tuned temperature parameter that controls the strength of entropy regularization. 

In continuous action spaces, SAC typically updates the policy using the reparameterization trick, in which action sampling is expressed as 


enabling low-variance gradient backpropagation through the stochastic policy. 

# **4. Self-Correcting VLA** 

We present Self-Correcting VLA (SC-VLA), a two-stage framework illustrated in Fig. 2. SC-VLA integrates sparse world imagination (SPI) with residual reinforcement learning for online action refinement (OAR). Crucially, the reward signals are **endogenous** , derived purely from the internal consistency of world imagination rather than external dense supervision. This design comprises two key components: (i) a flow-matching base policy guided by sparse imagination (Sec. 4.1), and (ii) a residual module optimized via intrinsic predictive rewards (Sec. 4.2). 

## **4.1. Sparse World Imagination** 

**Conditional Information Processing.** We leverage a Vision-Language Model (VLM) to fuse multimodal observations into a unified representation. Specifically, multi-view images _Ik_ are encoded by the SigLIP-2 (Tschannen et al., 2025) backbone and concatenated with the language instruction _L_ . This joint sequence is then processed by Eagle-2 (Li et al., 2024). To balance high-level semantic understanding with low-level control features, we extract the hidden states from an intermediate layer _l_ as the conditioning signal **o** mid: 


where _E_ vis denotes the SigLIP-2 encoder and Φ<sup>(</sup> VLM<sup>_l_)repre-</sup> sents the VLM backbone truncated at layer _l_ . 

**Query Sequence Construction.** To compensate for the lack of physical consistency constraints in standard flow matching, we introduce a physics regularization mechanism based on sparse world imagination. Explicit world prediction targets are injected into the query sequence to be jointly modeled with the action vector field. The augmented input query sequence is defined as: 


Here, **s** _t ∈_ R<sup>1</sup><sup>_×D_</sup> denotes the current embodiment state, and **q** _a ∈_ R<sup>16</sup><sup>_×D_</sup> corresponds to the queries for action trajectory generation. These two components serve as the base queries for action generation. **q** _pt ∈_ R<sup>1</sup><sup>_×D_</sup> is used to predict the task progress _pt_ , providing the model with explicit temporal evolution cues. **q** ∆ _st ∈_ R<sup>1</sup><sup>_×D_</sup> is introduced to model shorthorizon future physical state variations, capturing the spatial displacement trends induced by the action. Specifically, we model short-term physical evolution as a relative transformation within the current local coordinate frame. We define the target state at a future time step _t_<sup>_′_</sup> = _t_ + _H_ + _δ_ , where _H_ is the execution horizon and _δ ∼U_ ( _−_ ∆ _,_ ∆) is a random temporal offset introduced for robustness. The relative state increment ∆ _st ∈_ R<sup>7</sup> is calculated as: 


Here, _P ∈_ R<sup>3</sup> , _R ∈ SO_ (3), and _g ∈_ R denote the endeffector position, rotation matrix, and gripper opening, respectively. The operator Euler( _·_ ) extracts Euler angles from the relative rotation matrix. This sparse, local-frame prediction objective enhances the model’s generalization to physical dynamics across varying temporal scales. 

**Joint Optimization.** In the DiT backbone composed of _N_ Transformer blocks, the final block primarily focuses on modeling the action distribution, while intermediate layers retain explicit representations of the world state. To encode short-term physical evolution prior to action generation, we extract the hidden representation _h_<sup>(</sup><sup>_m_)</sup> from the _m_ -th intermediate block. Based on this feature, we predict the task progress _pt_ and relative state change ∆ _st_ using independent lightweight MLP heads: 


We jointly optimize the flow matching objective with this auxiliary physical supervision. The overall training objective is defined as: 


where _L_ prog and _L_ ∆ _st_ are supervised using Mean Squared Error (MSE), weighted by coefficients _λ_ 1 and _λ_ 2. Through 

4 


_Figure 2._ The architecture of Self-Correcting VLA. The framework consists of two stages: Stage I (Top) utilizes a VLM and DiT-based backbone to generate base actions and sparse world imagination, decoded from the final output (Layer _N_ ) and intermediate features (Layer _M_ ), respectively. Stage II (Bottom) implements Online Action Refinement, where a Residual RL Module optimizes the final action by learning a residual term. This process is guided by endogenous dense rewards derived from the dynamic weighting of imagination consistency (Progress and ∆State ) without external supervision. 

this joint optimization, the model not only learns to generate precise actions but also internalizes a coherent and interpretable sparse world representation within _h_<sup>(</sup><sup>_m_)</sup> , providing robust guidance for the subsequent residual policy adaptation. 

## **4.2. Online Action Refinement** 

While the base policy (Sec. 4.1) enhances stability by encoding physical evolution, it remains limited by offline data, often struggling with out-of-distribution perturbations and fine-grained contacts. To address this without learning from scratch, we introduce a residual RL module atop the base priors. This module performs minimal online corrections to base actions, enabling effective adaptation in high-precision settings. 

**Residual Policy.** To balance the stability of the base policy and online adaptability to environmental perturbations, we adopt a residual policy structure. The input space of the residual policy _π_ res is reconstructed as a _sparse world imagination observation ow ∈_ R<sup>16</sup> : 


In this work, we follow the Policy Decorator (Yuan et al., 2024) to model the residual policy _π_ res as a Gaussian policy parameterized by a lightweight multilayer perceptron (MLP) and adopt the Soft Actor-Critic (SAC) (Haarnoja et al., 2018) 

algorithm because it has excellent sample efficiency and stability. The final action _at_ is jointly determined by a frozen base policy _a_<sup>base</sup> _t ∼ π_ base( _o_ mid) and a learnable residual policy _a_<sup>res</sup> _t ∼ π_ res( _ow_ ): 


where _λ_ is a residual scaling coefficient. By explicitly incorporating task progress and state evolution predicted by the first-stage model, the residual network can perceive the intent of the base policy. This design enables the residual policy to perform local adjustments around the physical evolution priors provided by the model, thereby avoiding inefficient and unconstrained exploration in the raw observation space. 

**Dense Reward Mechanism.** Although the residual architecture reduces the dimensionality of exploration, the environment reward remains highly sparse. To address this issue, we construct a directional dense guidance reward using the short-term state change ∆<sup>�</sup> _st_ predicted by the base policy. Specifically, we extract only the first three translational components ∆ _s_<sup>pos</sup> _t ∈_ R<sup>3</sup> from ∆ _st_ and define the short-term goal position at the current timestep as 


After executing the residual action, the guidance reward is computed based on the alignment between the actual end- 

5 

effector displacement and the predicted evolution direction: 


Here, _Pt_ + _n_ denotes the end-effector position after executing the action for _n_ steps ( _n < H_ ). This reward provides continuous directional feedback at each step, guiding the residual policy to perform local adjustments along the short-term physical evolution direction predicted by the base policy, thereby effectively alleviating exploration difficulties under sparse reward settings. 

**Algorithm 1** SC-VLA: Online Action Refinement 

- 1: **Input:** Frozen SC-VLA base policy _π_ base, online action refinement policy _π_ res, environment Env 

- 2: Initialize replay buffer _D_ 

- 3: Initialize total training steps _T_ train 

# **5. Experiments** 

In this section, we systematically evaluate the effectiveness of _Self-Correcting Vision-Language-Action_ (SC-VLA) through both simulation and real-robot experiments, with a primary focus on success rate, throughput and transferability in complex manipulation tasks. Specifically, our experimental analysis is organized around the following key questions: 

   1. Can SC-VLA improve the success rate of flowmatching policies in complex manipulation tasks through sparse world imagination combined with a residual module? 

   2. Can the dense reward constructed based on sparse world imagination and the dynamic weight scheduling alleviate the issue of low exploration efficiency caused by sparse rewards and improve policy throughput? 

- 4: _t ←_ 0 

- 5: **while** _t < T_ train **do** 

- 6: Observe state _st_ 7: Query base policy: ( _a_<sup>base</sup> _t , p_ ˆ _t,_ ∆<sup>�</sup> _st_ ) _∼ π_ base( _o_ mid) 8: Construct augmented observation _o_<sup>_t_</sup> _w_<sup>by Eq. (11)</sup> 9: Sample residual action _a_<sup>res</sup> _t ∼ π_ res( _o_<sup>_t_</sup> _w_<sup>)</sup> 

- 10: Execute action _at ← a_<sup>base</sup> _t_ + _λa_<sup>res</sup> _t_ 11: Step environment: ( _o_<sup>_t_</sup> _w_<sup>+1</sup><sup>_, r_</sup> _t_<sup>env)</sup><sup>_←_Env.Step(</sup><sup>_at_)</sup> 12: Compute final reward _rt_<sup>_final_</sup> by Eq. (15) 13: Add ( _o_<sup>_t_</sup> _w_<sup>_, a_base</sup> _t , a_<sup>res</sup> _t_<sup>_, ot_</sup> _w_<sup>+1</sup><sup>_, a_base</sup> _t_ +1<sup>_, r_</sup> _t_<sup>_final_</sup> ) in _D_ 

- 14: Update _π_ res and critics using SAC 

- 15: _t ← t_ + 1 16: **end while** 

**Dynamic Weight Scheduling.** While sparse world imagination accelerates global exploration, a static predictive prior may limit the policy’s optimization capability during fine-grained contact phases due to distribution shift. To address this issue, we propose a _dynamic weight scheduling_ . Specifically, we use the predicted task progress _p_ ˆ _t_ as a scheduling signal, allowing predictive guidance to dominate in the early stages of the task and to be gradually weakened in later stages, thereby enabling a smooth transition from predictive-prior guidance to autonomous exploration. The final reward is defined as a weighted combination of the environment reward and the predictive guidance reward: 


where _η_ ( _·_ ) is a monotonically decreasing scheduling function with respect to task progress, _w_ guide is the guidance weight, _rt_<sup>env</sup> denotes the sparse environment reward, and _c_ is a per-step time penalty. This mechanism effectively balances early exploration efficiency and late-stage sensitivity to real dynamics feedback, ensuring stable convergence of the policy during the fine-tuning phase. 

3. What are the respective contributions of the key components in the proposed framework to the overall performance? 

4. Can the proposed method be stably transferred to real robotic systems and maintain robustness under environmental perturbations? 

## **5.1. Simulation Setup and Baselines** 

**ManiSkill3.** We evaluate our method on ManiSkill3 (Tao et al., 2024), a SAPIEN-based (Xiang et al., 2020) platform offering high-fidelity contact dynamics suitable for complex manipulation. We select four challenging tasks: _StackCube_ , _PlaceSphere_ , _PegInsertion_ , and _LiftPegUpright_ , to cover capabilities ranging from precise pick-and-place to nonprehensile manipulation. For fair comparison, all methods are trained with 100 demonstrations per task and evaluated over 50 episodes. See Appendix A for details. 

**Baselines.** We compare SC-VLA against baselines representing mainstream paradigms: _Diffusion Policy_ (DP) (Chi et al., 2025) for diffusion-based control, _ACT_ (Zhao et al., 2023) for action chunking, and _π_ 0 (Black et al., 2024) for flow-matching policies, alongside our base model GR00T N1.5 (Bjorck et al., 2025). We use task success rate as the primary metric. Additionally, we report average episode length during the RL stage to evaluate exploration efficiency and system throughput. Detailed configurations are provided in Appendix B. 

**Quantitative Results.** Table 1 summarizes the success rates of all methods on four challenging manipulation tasks in ManiSkill. Overall, the proposed _Self-Correcting Vision-Language-Action_ method demonstrates superior performance, significantly outperforming existing baseline approaches across all categories. Taking the most challenging 

6 

_Table 1._ Success rates of all methods in ManiSkill. Due to the absence of language guidance in DP, ACT, we evaluate them under two settings:<sup>_‡_</sup> denotes a single multi-task policy trained on all tasks simultaneously. _†_ denotes training independent specialist models for each of the four tasks separately. 

|**Model**||**ManiS**|**kill Tasks**||**Avg**|
|---|---|---|---|---|---|
||**Stack**<br>**Cube**|**Place**<br>**Sphere**|**LiftPeg**<br>**Upright**|**Peg**<br>**Insertion**||
|DP<sup>_‡_</sup>|0.46|0.90|0.10|0.00|0.36|
|DP<sup>_†_</sup>|0.88|1.00|0.80|0.40|0.77|
|ACT<sup>_‡_</sup>|0.50|0.88|0.60|0.12|0.52|
|ACT<sup>_†_</sup>|0.64|0.90|0.46|0.04|0.51|
|_π_0|0.66|0.86|0.48|0.22|0.55|
|GR00T N1.5|0.78|1.00|0.72|0.40|0.72|
|SC-VLA(SPI)|0.96|1.00|0.82|0.50|0.82|
|SC-VLA(SPI, OAR)|**1.00**|**1.00**|**0.88**|**0.56**|**0.86**|
|∆from OAR|+4%|+0%|+6%|+6%|+4%|


_Table 2._ Average completion length over successful episodes. 

|**Model**||**ManiS**|**kill Tasks**||**Avg**|
|---|---|---|---|---|---|
||**Stack**<br>**Cube**|**Place**<br>**Sphere**|**LiftPeg**<br>**Upright**|**Peg**<br>**Insertion**||
|DP<sup>_‡_</sup>|162|146|202|800|327|
|DP<sup>_†_</sup>|**132**|125|197|233|172|
|ACT<sup>_‡_</sup>|148|131|207|250|184|
|ACT<sup>_†_</sup>|198|126|203|230|189|
|_π_0|265|179|331|331|276|
|GR00T N1.5|192|122|209|257|195|
|SC-VLA(SPI)|169|128|190|262|187|
|SC-VLA(SPI,OAR)|158|**110**|**189**|**173**|**157**|
|∆from OAR|_↓_6_._2%|_↓_14_._0%|_↓_0_._5%|_↓_34_._0%|_↓_16_._0%|


_PegInsertion_ task as an example, SC-VLA (SPI) improves the success rate by **28%** and **10%** over pretrained models such as _π_ 0 (Black et al., 2024) and GR00T N1.5 (Bjorck et al., 2025), respectively, demonstrating that explicitly incorporating short-horizon physical state prediction effectively enhances control precision in complex contact scenarios. Building on this, the introduction of residual reinforcement learning further boosts the performance, with SC-VLA (SPI, OAR) achieving an average success rate of 86%. 

In addition, Table 2 reports the average completion length over **successful episodes** for all methods. SC-VLA attains the shortest average completion length of 157 steps, indicating the highest execution efficiency. This corresponds to a **43%** reduction compared to pretrained models such as _π_ 0 (Black et al., 2024), and a **8%** reduction relative to lightweight policies such as Diffusion Policy (DP) (Chi et al., 2025). These results show that the proposed method achieves both more precise execution and higher throughput on complex manipulation tasks. 

## **5.2. Ablation Study** 

To analyze the contribution of each key component in the SC-VLA framework, we conduct a systematic ablation study on the ManiSkill benchmark. All ablation variants are trained using the same demonstration data and evaluated under identical protocols, with the average success rate across the four tasks serving as the primary metric to ensure comparability and fairness. 

_Table 3._ Ablation study on different imagination components. 

|**Model**||**Mani**|**Skill Tasks**||**Avg**|
|---|---|---|---|---|---|
||**Stack**<br>**Cube**|**Place**<br>**Sphere**|**LiftPeg**<br>**Upright**|**Peg**<br>**Insertion**||
|SC-VLA w/o state|0.88|1.00|**0.84**|0.42|0.78|
|SC-VLA w/o prog|0.92|1.00|0.80|0.50|0.80|
|SC-VLA w/o state<br>~~p~~rog|0.78|1.00|0.72|0.40|0.72|
|SC-VLA(SPI)|**0.96**|**1.00**|0.82|**0.50**|**0.82**|


**Effectiveness of Progress Guidance.** The progress token ( **q** _pt_ ) provides explicit temporal progression information for action generation. To evaluate its effectiveness, we conduct an ablation study by removing **q** _pt_ from the query sequence. As shown in Table 3, removing **q** _pt_ reduces the average success rate from 82% to 80%, with the degradation mainly observed on tasks with clear execution stages, such as _StackCube_ (96% _→_ 92%) and _LiftPegUpright_ (82% _→_ 80%). These results indicate that the absence of _qpt_ does not significantly compromise action reliability, but plays an important role in improving the temporal consistency of the policy during multi-stage execution. 

**Effectiveness of State Guidance.** Relative state change modeling (∆ _st_ ) provides directional constraints on shortterm physical evolution for action generation. To evaluate its effectiveness, we conduct an ablation study by removing **q** ∆ _st_ from the query sequence. As shown in Table 3, removing **q** ∆ _st_ leads to a clear drop in the average success rate from 82% to 78%, with the most pronounced degradation observed in difficult tasks such as _PegInsertion_ (50% _→_ 42%) and _StackCube_ (96% _→_ 88%). These results indicate that _delta_ _~~s~~ tate_ plays a critical role in stabilizing the physical consistency of action execution, particularly in tasks that are sensitive to contact dynamics and pose accuracy. 

**Complementarity Between Progress and State Guidance.** We further examine the interaction between progress guidance ( _pt_ ) and relative state change modeling (∆ _st_ ) by jointly removing both components. As shown in Table 3, eliminating **q** _pt_ and **q** ∆ _st_ simultaneously causes the average success rate to drop significantly to 72%, which is markedly lower than the performance under either single ablation setting. This result demonstrates that progress guidance and state guidance play complementary roles in the policy. 

7 


_Figure 3._ Hardware platforms and visualizations of sampled tasks. The setup is equipped with a wristed camera and a third-person camera. 


_Figure 4._ **Ablation study on the effectiveness of sparse world imagination rewards and dynamic weight scheduling.** We visualize the performance curves starting from the main training phase, excluding the data collection and residual warm-up periods. See Appendix C for further details. 

**Effectiveness of Sparse World Imagination Rewards.** The sparse world imagination reward plays a pivotal guiding role in reinforcement learning exploration by transforming physical evolution predictions into dense directional feedback. To evaluate its effectiveness, we conducted an ablation study by removing guiding reward and training the residual policy relying solely on the environment’s sparse reward. As shown in Fig. 4, while the performance gap is negligible in the simple _PlaceSphere_ task due to the strong base policy, the reward becomes critical in complex tasks like _PegInsertion_ . It provides dense feedback to break exploration bottlenecks, reducing average steps from 800 to 650 and boosting throughput. This confirms its essential role in overcoming cold-start problems for complex manipulation. 

**Effectiveness of Dynamic Weight Scheduling.** The dynamic weighting mechanism is responsible for regulating the intensity of prior guidance based on task progress to balance early exploration guidance with later autonomous fine-tuning. To evaluate its effectiveness, we conducted a comparative ablation study by replacing the dynamic decay weight with a fixed constant weight. Results on precision tasks like _PlaceSphere_ and _PegInsertion_ show that fixed weights lead to significant late-stage degradation, manifesting as divergent step counts or stagnation at sub-optimal 

solutions. This highlights the conflict between static priors and fine-grained control, demonstrating that progress-based regulation is essential to prevent prior bias from interfering with fine manipulation. 

## **5.3. Real World Experiments** 

**Setup.** We evaluate SC-VLA (SPI) on a real ARX5 arm across four tasks: _StackCube_ , _PlaceSphere_ , _PegInsertion_ , and _PushCube_ . Models are trained on 60 demonstrations per task. Hardware setups are visualized in Fig. 3. Given the difficulty of real-world reward design, we benchmark against widely adopted baselines: GR00T N1.5 (Bjorck et al., 2025) and Diffusion Policy (DP) (Chi et al., 2025). We conduct 20 execution trials per task. 

_Table 4._ Success rates on real-world tasks using the ARX5 arm. 

|**Model**||**Real Wo**|**rld Tas**|**ks**|**Avg**|
|---|---|---|---|---|---|
||**Stack**<br>**Cube**|**Place**<br>**Sphere**|**Push**<br>**Cube**|**Peg**<br>**Insertion**||
|DP<sup>_‡_</sup>|0.30|0.40|0.45|0.00|0.28|
|GR00T N1.5|0.75|0.45|0.80|0.30|0.57|
|SC-VLA(SPI)|**0.85**|**0.60**|**1.00**|**0.40**|**0.71**|


**Quantitative Results.** As detailed in Table 4, SC-VLA (SPI) demonstrates superior capability, achieving an average success rate of 70% that surpasses DP and GR00T N1.5 by margins of **43%** and **14%** , respectively. Its superior performance in contact-rich tasks, such as PegInsertion and StackCube, validates that the sparse world imagination effectively enhances robustness and generalization in complex real-world dynamics. 

# **6. Conclusion** 

We propose _Self-Correcting Vision-Language-Action_ (SCVLA), a framework coupling prediction and control via sparse world imagination. This approach addresses the limitations of static priors and insufficient physical modeling in existing VLA. Our results demonstrate that structured predictive priors can guide physically consistent actions without the complexity of explicit world models. By uni- 

8 

fying world-aware modeling with intrinsic reinforcement learning, SC-VLA eliminates the need for manual reward engineering. Extensive experiments confirm that this selfcorrecting paradigm substantially improves task throughput, offering a robust direction for developing autonomous, selfevolving robotic systems. 

# **Impact Statement** 

This paper presents work whose goal is to advance the field of Machine Learning. There are many potential societal consequences of our work, none which we feel must be specifically highlighted here. 

# **References** 

- Bjorck, J., Castaneda, F., Cherniadev, N., Da, X., Ding, R.,˜ Fan, L., Fang, Y., Fox, D., Hu, F., Huang, S., et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- Black, K., Nakamoto, M., Atreya, P., Walke, H., Finn, C., Kumar, A., and Levine, S. Zero-shot robotic manipulation with pretrained image-editing diffusion models. _arXiv preprint arXiv:2310.10639_ , 2023. 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., et al. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Dabis, J., Finn, C., Gopalakrishnan, K., Hausman, K., Herzog, A., Hsu, J., et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 

- Cadene, R., Alibert, S., Soare, A., Gallouedec, Q., Zouitine, A., and Wolf, T. Lerobot: State-of-the-art machine learning for real-world robotics in pytorch, 2024. 

- Cen, J., Yu, C., Yuan, H., Jiang, Y., Huang, S., Guo, J., Li, X., Song, Y., Luo, H., Wang, F., et al. Worldvla: Towards autoregressive action world model. _arXiv preprint arXiv:2506.21539_ , 2025. 

- Chebotar, Y., Vuong, Q., Hausman, K., Xia, F., Lu, Y., Irpan, A., Kumar, A., Yu, T., Herzog, A., Pertsch, K., et al. Q-transformer: Scalable offline reinforcement learning via autoregressive q-functions. In _Conference on Robot Learning_ , pp. 3909–3928. PMLR, 2023. 

- Chi, C., Xu, Z., Feng, S., Cousineau, E., Du, Y., Burchfiel, B., Tedrake, R., and Song, S. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , 44(10-11): 1684–1704, 2025. 

- Chow, W., Mao, J., Li, B., Seita, D., Guizilini, V., and Wang, Y. Physbench: Benchmarking and enhancing visionlanguage models for physical world understanding. _arXiv preprint arXiv:2501.16411_ , 2025. 

- Driess, D., Xia, F., Sajjadi, M. S., Lynch, C., Chowdhery, A., Wahid, A., Tompson, J., Vuong, Q., Yu, T., Huang, W., et al. Palm-e: An embodied multimodal language model. 2023. 

- Ghasemipour, S. K. S., Wahid, A., Tompson, J., Sanketi, P., and Mordatch, I. Self-improving embodied foundation models. _arXiv preprint arXiv:2509.15155_ , 2025. 

- Haarnoja, T., Zhou, A., Abbeel, P., and Levine, S. Soft actor-critic: Off-policy maximum entropy deep reinforcement learning with a stochastic actor. In _International conference on machine learning_ , pp. 1861–1870. Pmlr, 2018. 

- Huang, C.-P., Wu, Y.-H., Chen, M.-H., Wang, Y.-C. F., and Yang, F.-E. Thinkact: Vision-language-action reasoning via reinforced visual latent planning. _arXiv preprint arXiv:2507.16815_ , 2025. 

- Hung, C.-Y., Majumder, N., Deng, H., Renhang, L., Ang, Y., Zadeh, A., Li, C., Herremans, D., Wang, Z., and Poria, S. Nora-1.5: A vision-language-action model trained using world model-and action-based preference rewards. _arXiv preprint arXiv:2511.14659_ , 2025. 

- Intelligence, P., Amin, A., Aniceto, R., Balakrishna, A., Black, K., Conley, K., Connors, G., Darpinian, J., Dhabalia, K., DiCarlo, J., et al. _π_ 0 _._ 6: a vla that learns from experience. _arXiv preprint arXiv:2511.14759_ , 2025. 

- Kim, M. J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E., Lam, G., Sanketi, P., et al. Openvla: An open-source vision-languageaction model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- Kumar, A., Zhou, A., Tucker, G., and Levine, S. Conservative q-learning for offline reinforcement learning. _Advances in neural information processing systems_ , 33: 1179–1191, 2020. 

- Li, B., Wu, D., Yan, Z., Liu, X., Zeng, Z., Li, L., and Zha, H. Reflection-based task adaptation for self-improving vla. _arXiv preprint arXiv:2510.12710_ , 2025a. 

- Li, H., Ding, P., Suo, R., Wang, Y., Ge, Z., Zang, D., Yu, K., Sun, M., Zhang, H., Wang, D., et al. Vla-rft: Vision-language-action reinforcement fine-tuning with verified rewards in world simulators. _arXiv preprint arXiv:2510.00406_ , 2025b. 

9 

- Li, P., Wu, H., Huang, Y., Cheang, C., Wang, L., and Kong, T. Gr-mg: Leveraging partially-annotated data via multimodal goal-conditioned policy. _IEEE Robotics and Automation Letters_ , 2025c. 

- Li, X., Liu, M., Zhang, H., Yu, C., Xu, J., Wu, H., Cheang, C., Jing, Y., Zhang, W., Liu, H., et al. Vision-language foundation models as effective robot imitators. _arXiv preprint arXiv:2311.01378_ , 2023. 

- Li, Y., Wei, F., Zhang, C., and Zhang, H. Eagle-2: Faster inference of language models with dynamic draft trees. _arXiv preprint arXiv:2406.16858_ , 2024. 

- Liu, J., Gao, F., Wei, B., Chen, X., Liao, Q., Wu, Y., Yu, C., and Wang, Y. What can rl bring to vla generalization? an empirical study. _arXiv preprint arXiv:2505.19789_ , 2025. 

- Liu, S., Wu, L., Li, B., Tan, H., Chen, H., Wang, Z., Xu, K., Su, H., and Zhu, J. Rdt-1b: a diffusion foundation model for bimanual manipulation. _arXiv preprint arXiv:2410.07864_ , 2024. 

- Lu, G., Guo, W., Zhang, C., Zhou, Y., Jiang, H., Gao, Z., Tang, Y., and Wang, Z. Vla-rl: Towards masterful and general robotic manipulation with scalable reinforcement learning. _arXiv preprint arXiv:2505.18719_ , 2025. 

- Schulman, J., Wolski, F., Dhariwal, P., Radford, A., and Klimov, O. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- Shu, J., Lin, Z., and Wang, Y. Rftf: Reinforcement fine-tuning for embodied agents with temporal feedback. _arXiv preprint arXiv:2505.19767_ , 2025. 

- Song, Z., Qin, S., Chen, T., Lin, L., and Wang, G. Physical autoregressive model for robotic manipulation without action pretraining. _arXiv preprint arXiv:2508.09822_ , 2025. 

- Tao, S., Xiang, F., Shukla, A., Qin, Y., Hinrichsen, X., Yuan, X., Bao, C., Lin, X., Liu, Y., Chan, T.-k., et al. Maniskill3: Gpu parallelized robotics simulation and rendering for generalizable embodied ai. _arXiv preprint arXiv:2410.00425_ , 2024. 

- Team, O. M., Ghosh, D., Walke, H., Pertsch, K., Black, K., Mees, O., Dasari, S., Hejna, J., Kreiman, T., Xu, C., et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

- Tschannen, M., Gritsenko, A., Wang, X., Naeem, M. F., Alabdulmohsin, I., Parthasarathy, N., Evans, T., Beyer, L., Xia, Y., Mustafa, B., et al. Siglip 2: Multilingual vision-language encoders with improved semantic understanding, localization, and dense features. _arXiv preprint arXiv:2502.14786_ , 2025. 

- Wu, H., Jing, Y., Cheang, C., Chen, G., Xu, J., Li, X., Liu, M., Li, H., and Kong, T. Unleashing large-scale video generative pre-training for visual robot manipulation. _arXiv preprint arXiv:2312.13139_ , 2023. 

- Xiang, F., Qin, Y., Mo, K., Xia, Y., Zhu, H., Liu, F., Liu, M., Jiang, H., Yuan, Y., Wang, H., et al. Sapien: A simulated part-based interactive environment. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pp. 11097–11107, 2020. 

- Xiao, J., Yang, Y., Chang, X., Chen, R., Xiong, F., Xu, M., Zheng, W.-S., and Zhang, Q. World-env: Leveraging world model as a virtual environment for vla post-training. _arXiv preprint arXiv:2509.24948_ , 2025. 

- Yuan, X., Mu, T., Tao, S., Fang, Y., Zhang, M., and Su, H. Policy decorator: Model-agnostic online refinement for large policy model. _arXiv preprint arXiv:2412.13630_ , 2024. 

- Zhai, S., Zhang, Q., Zhang, T., Huang, F., Zhang, H., Zhou, M., Zhang, S., Liu, L., Lin, S., and Pang, J. A visionlanguage-action-critic model for robotic real-world reinforcement learning. _arXiv preprint arXiv:2509.15937_ , 2025. 

- Zhang, H., Zhuang, Z., Zhao, H., Ding, P., Lu, H., and Wang, D. Reinbot: Amplifying robot visual-language manipulation with reinforcement learning. _arXiv preprint arXiv:2505.07395_ , 2025. 

- Zhao, Q., Lu, Y., Kim, M. J., Fu, Z., Zhang, Z., Wu, Y., Li, Z., Ma, Q., Han, S., Finn, C., et al. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 1702–1713, 2025. 

- Zhao, T. Z., Kumar, V., Levine, S., and Finn, C. Learning fine-grained bimanual manipulation with low-cost hardware. _arXiv preprint arXiv:2304.13705_ , 2023. 

- Zheng, R., Liang, Y., Huang, S., Gao, J., Daume´ III, H., Kolobov, A., Huang, F., and Yang, J. Tracevla: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies. _arXiv preprint arXiv:2412.10345_ , 2024. 

- Zheng, R., Wang, J., Reed, S., Bjorck, J., Fang, Y., Hu, F., Jang, J., Kundalia, K., Lin, Z., Magne, L., et al. Flare: Robot learning with implicit world modeling. _arXiv preprint arXiv:2505.15659_ , 2025. 

- Zitkovich, B., Yu, T., Xu, S., Xu, P., Xiao, T., Xia, F., Wu, J., Wohlhart, P., Welker, S., Wahid, A., et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pp. 2165–2183. PMLR, 2023. 

10 

# **Appendix A: Task Setup and Evaluation Details** 

This appendix provides supplementary details for the ManiSkill3 (Tao et al., 2024) simulation tasks used in the main paper. All tasks are built upon the SAPIEN (Xiang et al., 2020) physics engine and are designed to evaluate robotic manipulation capabilities under high-precision control requirements and complex contact conditions. 

## **A.1 Task Descriptions** 

**(1) StackCube.** Stack the cube on top of the other cube: This task requires the robot to grasp a cube and stably stack it on top of another cube. It primarily evaluates pose accuracy during the grasping and placement phases, as well as execution stability. The task is particularly sensitive to positional errors and end-effector jitter. 

**(2) PlaceSphere.** Pick up the ball and place it in the target position: In this task, the robot is required to grasp a spherical object and place it at a designated target location. Due to the tendency of the sphere to roll during contact, this task imposes stringent requirements on end-effector velocity control and dynamic stability. 

**(3) LiftPegUpright.** Pick up the peg and place it upright: This task requires the robot to grasp one side of a peg and adjust the contact relationship to lift it from a horizontal configuration to an upright pose. During manipulation, relative sliding occurs between the peg and the end-effector. The upright phase demands accurate angle control and pose adjustment, making this task particularly challenging in terms of contact modeling and fine-grained control. 

**(4) PegInsertion.** Pick up the peg and insert it into the container next to the peg: This task requires the robot to precisely insert a peg into a hole with small tolerance. It emphasizes accurate pose alignment and fine-grained adjustments during the contact phase, and serves as a standard benchmark for evaluating high-precision manipulation capabilities. 

## **A.2 Training and Evaluation Settings** 

For all simulation tasks, all methods are trained using the same amount of demonstration data to ensure a fair comparison. After training, each method is independently evaluated over 50 episodes per task, with task success rate reported as the primary performance metric. Reward definitions follow the official ManiSkill3 (Tao et al., 2024) specifications, and the detailed success criteria for each task are summarized in Table 5. 

_Table 5._ Detailed definitions and success criteria for the four manipulation tasks used in our evaluation. 

|**Tasks**|**Success Criteria**|**Max Steps**|
|---|---|---|
|StackCube|The task is considered successful if the horizontal offset of the red cube relative to the green<br>cube does not exceed the half-diagonal of the cube plus 5 mm, the vertical distance between the<br>centers of the two cubes equals one cube edge length with a tolerance of 5 mm, and the red cube<br>remains stationary and is not grasped by the robot end-effector.|800|
|PlaceSphere|The task is considered successful if the horizontal offset of the sphere relative to the center of<br>the container does not exceed 5 mm, the vertical position satisfies that the contact point between<br>the bottom of the sphere and the container floor has an error within 5 mm, and the sphere is not<br>grasped by the robot end-effector.|500|
||The task is considered successful if the peg’s orientation is close to the upright configuration,||
|LiftPegUpright|with a deviation around the vertical axis not exceeding 0.08 rad, and the vertical position of the<br>peg’s center of mass deviates from its half-length by no more than 5 mm.|800|
||The task is considered successful if the tail end of the peg lies within the coordinate frame of the||
|PegInsertionside|box hole, with an offset along the insertion direction no greater than 2 cm, and offsets along the<br>other two orthogonal directions both smaller than 8 mm.|800|


# **Appendix B: Baseline Details and Settings** 

This appendix provides brief descriptions of the baseline methods used in the main paper. All baselines are trained and evaluated under the same demonstration data budget and evaluation protocols to ensure a fair comparison. 

11 

## **B.1 DP (Diffusion Policy)** 

Diffusion Policy (Chi et al., 2025) is an imitation learning approach based on diffusion models, which represents continuous action distributions through a progressive denoising process. By effectively modeling multimodal action behaviors, Diffusion Policy has been widely adopted as a strong baseline for robotic manipulation tasks. For the DP baseline, we utilize the implementation provided by the LeRobot (Cadene et al., 2024) codebase. We configure the policy with an observation history of 2 frames ( _n_ obs ~~s~~ teps<sup>= 2), a prediction horizon of 16 (</sup><sup>_H_= 16), and an execution chunk size of 8 (</sup><sup>_n_</sup> action ~~s~~ teps<sup>= 8).</sup> All models are trained for 200,000 iterations on a single NVIDIA RTX 5090 GPU with a batch size of 64. We apply random cropping with a 90% ratio for data augmentation. All other parameters are set to their default values. 

## **B.2 ACT (Action Chunking with Transformers)** 

ACT (Zhao et al., 2023) combines Conditional Variational Autoencoders (CVAEs) with Transformer architectures to model action sequences in a chunked manner. This design enables the generation of coherent and smooth action trajectories over long horizons, and has demonstrated stable performance in fine-grained manipulation scenarios. For the ACT baseline, we utilize the implementation provided by the LeRobot (Cadene et al., 2024) codebase. We configure the policy with an observation history of 1 frame ( _n_ obs ~~s~~ teps<sup>=1), a prediction horizon of 50 (</sup><sup>_H_=50), and an execution chunk size of 20</sup> ( _n_ action ~~s~~ teps<sup>= 20).All models are trained for 200,000 iterations on a single NVIDIA RTX 5090 GPU with a batch size of</sup> 64. All other parameters are set to their default values. 

## **B.3** **_π_** 0 

_π_ 0 (Black et al., 2024) is a recently proposed robot foundation model developed by Physical Intelligence, which acquires broad robotic manipulation capabilities through large-scale, multi-task and cross-embodiment training. Built upon a pre-trained vision-language model and augmented with a flow-based action generation module, _π_ 0 (Black et al., 2024) demonstrates strong performance on a wide range of real-world robotic manipulation tasks, including long-horizon and highly dexterous scenarios. For the _π_ 0 baseline, we utilize the official implementation. The model is trained for 50,000 iterations on a single NVIDIA RTX PRO 6000 GPU with a batch size of 32. We employ a cosine decay learning rate schedule, configured with 3,000 warmup steps, a peak learning rate of 2 _×_ 10<sup>_−_5</sup> , and a final learning rate of 1 _._ 5 _×_ 10<sup>_−_6</sup> (decaying over 100,000 steps). All other parameters are set to their default values. 

## **B.4 GR00T N1.5** 

GR00T N1.5 (Bjorck et al., 2025) is a robot manipulation model based on flow matching, which uses the DiT architecture to model continuous action distributions and achieves efficient and stable action generation through vector field learning. This paper extends this method based on its underlying architecture and uses it as a base model. For the GR00T N1.5 baseline, we utilize the official implementation. The model is trained for 50,000 iterations on a single NVIDIA L40 GPU with a batch size of 32. The learning rate is set to 1 _×_ 10<sup>_−_4</sup> . All other parameters are set to their default values. 

# **Appendix C: Experiment Details** 

- **Multi-Stage Training Protocol.** To ensure the stability of the hybrid architecture, integrating a pre-trained Flow Matching DiT base policy with a randomly initialized SAC residual module, we implement a three-stage training protocol. As illustrated in Fig. 5, the residual weight _λ_ is dynamically adjusted to facilitate a smooth transition from pure imitation to residual reinforcement learning: 1. **Initial Data Collection (Buffer Warm-up):** In the very early stage, the residual weight is held constant at _λ_ = 0. The agent acts solely using the frozen base policy to collect high-quality demonstration trajectories. This phase is strictly for populating the SAC replay buffer with valid transitions, ensuring the critic has a meaningful state distribution to learn from before any policy updates occur. 

2. **Residual Injection (Policy Warm-up):** Once the buffer is sufficiently populated, we enter a linear warm-up phase. The residual weight _λ_ is linearly increased from 0 to the target scaling factor. This gradual injection prevents the noise from the initially random residual policy from catastrophically disrupting the control loop, allowing the RL agent to adapt to the base policy’s dynamics without causing immediate task failure. 

12 


_Figure 5._ **Schematic of the multi-stage training protocol and residual weight schedule.** The training process is divided into three distinct phases to ensure stability: (1) _Buffer Warm-up_ for gathering demonstrations, (2) _Residual Injection_ for gradually introducing the RL policy, and (3) the _Main Training Phase_ . The curve illustrates the evolution of the residual weight _λ_ , transitioning from pure imitation to full residual learning. 

3. **Main Training Phase:** Upon reaching the target weight, _λ_ remains fixed (subject to the dynamic weight scheduling described in Sec. 4.2), and the formal training and evaluation begin. 

**Visualization Rationale.** It is important to note that the _Data Collection_ and _Residual Injection_ phases are transient and brief compared to the overall training duration. They serve merely as necessary initialization steps to stabilize the learning environment. During these preliminary phases, performance metrics naturally fluctuate: the agent exhibits stable behavior during data collection (using the base policy) but experiences an inevitable “adaptation dip” during residual injection as the RL module explores. Detailed parameter settings for these phases are provided in Table 7. To provide a clear and fair comparison of the proposed methods ( _Sparse World Imagination Reward_ and _Dynamic Weight Scheduling_ ), we exclude these initialization artifacts from our results. The performance curves in Fig. 4 strictly record the _Main Training Phase_ , starting immediately after the residual weight reaches its target value. This ensures the visualization focuses on the model’s convergence behavior and asymptotic performance rather than its setup dynamics. 

# **Appendix D: Implementation Details** 

To ensure reproducibility, this appendix details the key configurations and hyperparameter settings used in the two training stages of the SC-VLA framework. 

**Stage I: SC-VLA Base Policy Training.** The base policy is implemented using the DiT architecture from _GR00T N1.5_ . We jointly optimize the flow-matching objective and the multimodal prediction heads using the AdamW optimizer. The model is trained for 50,000 iterations on a single NVIDIA L40 GPU. The detailed network configurations and training hyperparameters are summarized in Table 6. 

_Table 6._ SC-VLA base model hyperparameter settings. 

|**Hyperparameter**|**Value**|
|---|---|
|Batch size|32|
|Training steps|50,000|
|Learning rate|1_×_10<sup>_−_4</sup>|
|Model init seed|42|
|Optimizer|AdamW|


**Stage II: SC-VLA Residual Policy Training.** In the second stage, the residual module is trained using the Soft ActorCritic (SAC) algorithm. During this phase, the parameters of the base model are fully frozen, and optimization is performed exclusively on the residual network _π_ res. 

To account for performance variance of the base policy across different tasks, we adopt a task-adaptive residual scaling strategy. Specifically, following an inverse-correlation principle, tasks for which the base model achieves higher success 

13 

rates are assigned smaller residual scaling and evaluation coefficients, enabling fine-grained refinement while preserving high-quality priors. Conversely, larger coefficients are used for tasks where the base policy performs worse, allowing for more substantial action corrections. 

Although the residual scaling factor varies across tasks, we employ a consistent dynamic scheduling strategy for the predictive guidance reward across all experiments. Key hyperparameters used in the reinforcement learning stage are summarized in Table 7. 

_Table 7._ SC-VLA residual model hyperparameter settings. 

||**Shared**<br>|**Parameters**<br>|**Task-Specific P**<br>|**i arameters**<br>|
|---|---|---|---|---|
|**Tasks**|**Hyperparameter**|**Value**|**Hyperparameter**|**Value**|
||||Total timesteps|500,000|
||||Learning start steps|30,000|
|StackCube|Random seed<br>Replay buffer size|0<br>Total steps|Exploration steps<br>Residual scale (train)<br>Residual scale (eval)|100,000<br>0.01<br>0.005|
||Discount factor_γ_<br>|0.97<br>|Total timesteps|500,000|
||Target smoothing_τ_|0.01|Learning start steps|8,000|
|PlaceSphere|Batch size_B_|1024|Exploration steps<br>|30,000<br>|
||Policy learning rate<br>Critic learnin rate|1_×_10<sup>_−_4</sup><br>1_×_10<sup>_−_4</sup>|Residual scale (train)<br>Residual scale (eval)|0.01<br>0.005|
||g<br>Entropy coeff. _α_|<br>0.2|Total timesteps<br>Learning start steps|600,000<br>30,000|
|LiftPegUpright|Gradient clipping|50|Exploration steps|100,000|
||Update-to-Data (UTD)|0.5|Residual scale (train)|0.01|
||<br>Training frequency|64|Residual scale (eval)|0.005|
||Guide weight_w_guide|0.6|Total timesteps<br>Learning start steps|3,000,000<br>60,000|
|PegInsertion|||Exploration steps|200,000|
||||Residual scale (train)<br>Residual scale (eval)|0.1<br>0.03|


14 


_Figure 6._ Visualization results of Maniskill simulated tasks. 


_Figure 7._ Visualization results of real-world tasks. 

15 

