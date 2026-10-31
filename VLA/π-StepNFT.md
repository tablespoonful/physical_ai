---
title: "$π$-StepNFT: Wider Space Needs Finer Steps in Online RL for Flow-based VLAs"
date: "2026-03-02"
authors: "Siting Wang; Xiaofeng Wang; Zheng Zhu; Minnan Pei; Xinyu Cui; Cheng Deng"
url: https://arxiv.org/abs/2603.02083
pdf: https://arxiv.org/pdf/2603.02083
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.02083)** / [論文ページ](https://arxiv.org/abs/2603.02083)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

_π_ **-StepNFT: Wider Space Needs Finer Steps in Online RL for Flow-based VLAs** 

**Siting Wang**<sup>1 ,2 ,3</sup> **Xiaofeng Wang**<sup>1 ,4</sup> **Zheng Zhu**<sup>1 ,†</sup> **Minnan Pei**<sup>2 ,3</sup> **Xinyu Cui**<sup>2 ,3 ,5</sup> **Cheng Deng**<sup>6</sup> **Jian Zhao**<sup>5</sup> **Guan Huang**<sup>1</sup> **Haifeng Zhang**<sup>2 ,3</sup> **Jun Wang**<sup>7 ,†</sup> 

# **Abstract** 

Flow-based vision-language-action (VLA) models excel in embodied control but suffer from intractable likelihoods during multi-step sampling, hindering online reinforcement learning. We propose **_π-StepNFT_** (Step-wise Negative-aware Fine-Tuning), a critic-and-likelihood-free framework that requires only a single forward pass per optimization step and eliminates auxiliary value networks. We identify that wider exploration spaces necessitate finer-grained, step-wise guidance for alignment. Empirically, _π_ -StepNFT unlocks latent potential on LIBERO with competitive few-shot robustness. Moreover, it achieves superior generalization on ManiSkill, outperforming value-based baselines in OOD scenarios by preventing overfitting to multimodal features. This property offers a scalable solution promising for complex real-world applications. Our implementation builds upon RLinf and is publicly available at https://wangst0181.github.io/pi-StepNFT/. 

# **1. Introduction** 

Vision-language-action (VLA) models have recently demonstrated increasingly general capabilities, enabling robots to follow open-ended natural language instructions and perform complex tasks across diverse environments. While early approaches discretized actions into tokens (Zitkovich et al., 2023; Kim et al., 2024) or mapped observations to continuous regression features (Kim et al., 2025b), recent advances have converged on flow-matching-based policies (Black et al., 2026; 2025; Intelligence et al., 2025; Ye et al., 2025; Bjorck et al., 2025). These models, by integrating large-scale vision-language pretraining with generative action prediction, have established a new standard for complex manipulation tasks. 

1GigaAI 2Institute of Automation, Chinese Academy of Sciences<sup>3</sup> University of Chinese Academy of Sciences<sup>4</sup> Tsinghua University<sup>5</sup> Zhongguancun Academy<sup>6</sup> The University of Edinburgh<sup>7</sup> University College London. Correspondence to: Zheng Zhu _<_ zhengzhu@ieee.org _>_ . 

_Preprint. March 10, 2026._ 

A recent systematic analysis (Pan et al., 2025) suggests that after supervised fine-tuning (SFT) converges, the output of flow-based VLAs often collapses to a single mode. Consequently, their efficacy stems from a mechanism of _stochasticity injection_ combined with _supervised iterative correction_ . Injecting noise during training and iterative correction during inference enable the policy to resist error accumulation and adhere closely to the expert manifold during closed-loop execution. However, we contend that relying heavily on the density of expert demonstrations, SFT merely establishes a foundational behavioral manifold that resembles a _narrow line_ , where the model often lacks the ability to recover once it deviates due to micro-perturbations during testing. To overcome this fragility, reinforcement learning (RL) is required, aiming not to learn from scratch, but to _explore an expanded manifold_ around the expert trajectory, endowing the model with the local error-correction capabilities needed to mitigate state deviations. 

However, training flow-based VLAs with RL faces fundamental bottlenecks. The deterministic nature of ordinary differential equation (ODE) trajectories confines the action exploration space entirely to the initial noise distribution. To this end, the multi-step ODE integration renders exact action likelihoods computationally intractable, as calculating gradients requires expensive Jacobian trace estimation or backpropagation through the solver. Faced with these challenges, existing solutions either bypass likelihoods by employing latent space value distillation (Li et al., 2025b) or training separate value functions to introduce explicit conditioning on trajectory quality (Intelligence et al., 2025), or approximate likelihoods via Gaussian parameterization at each denoising step (Chen et al., 2025). In contrast, DiffusionNFT (Zheng et al., 2026) offers a likelihood-free alternative from the image generation domain. It optimizes the flow field directly on the forward diffusion process and defines a contrastive improvement direction by splitting samples into positive and negative subsets. 

Crucially, directly transferring Diffusion-NFT to embodied control reveals a fundamental domain gap. While the standard deterministic ODE sampling yields a safe but narrow manifold, it lacks the exploratory capacity for selfimprovement. Attempting to broaden this scope via stochastic differential equation (SDE) theoretically enables mani- 

1 


_Figure 1._ **Comparison of training paradigms. Left (ODE):** Terminal supervision is well-posed for deterministic ODEs but results in a narrow expert manifold. **Middle (Naive SDE):** Stochastic rollouts introduce a wider exploration space, but coarse terminal supervision fails to correct deviations, leading to misalignment. **Right (** _π_ **-StepNFT):** Our method leverages the wider space from SDE but applies finer, step-wise ranking guidance to ensure robust alignment with the expert manifold. 

fold expansion during exploration, yet in practice, it results in a wider space but misaligned policy. This failure stems from the nature of supervision. Unlike image generation that targets static distribution matching, embodied control is sequential and thus sensitive to compounding errors. Moreover, embodied control typically uses a short denoising path to meet interaction latency, and prior empirical evidence indicates diminishing returns from moderately longer paths (Chen et al., 2025), making fine-grained, step-wise denoising supervision feasible in practice. 

As illustrated in Figure 1, under deterministic ODE rollouts, the intermediate state _xt_ stays on a narrow trajectory, making _“point-level”_ terminal matching ❶ on _x_ 0 relatively wellposed. However, under SDE rollouts, injected noises accumulate along the denoising path, and naively regressing the final _x_ 0 forces unstable point-to-point matching with highvariance gradients. A noise-aware view ❷ reveals that each denoising update induces a Gaussian transition, suggesting _“region-level”_ supervision with variance-normalization; yet using only the solely terminal ❸ still yields a coarse correction that lags behind on-policy drift. This motivates step-wise supervision ❹ that targets the immediate next solver state _xt−_ , providing fine-grained local guidance to stabilize stochastic exploration and accelerate convergence. 

To address these issues, we propose **_π-StepNFT_** , a criticand-likelihood-free online RL framework tailored for embodied VLAs. We achieve robust manifold expansion by systematically redesigning the interplay between _exploration_ and _supervision_ . First, regarding _lack of exploration_ , effective policy improvement necessitates a wider behavioral space. We introduce an SDE-based sampling mechanism during training that augments deterministic rollouts with structured noise, forcing the model to traverse adjacent states to effectively inflate the behavioral manifold. Second, for _supervision target mismatch_ , anchoring this expanded exploration demands finer-grained step-wise supervision. We shift the prediction target from the final denoised out- 

put _x_ 0 to the immediate next denoising step _xt−_ , using a noise-based regression to generate the precise local gradients needed for robust alignment. Third, regarding _suppressed successful exploration_ , we identify that the previous objective in Diffusion-NFT suffers from an “implicit penalty”, which inadvertently suppresses policy updates to minimize the magnitude of branch separation. To overcome this, we introduce a logistic contrastive ranking loss, establishing a “push-pull dynamics”: maximizing the likelihood of successful trajectories while suppressing failed ones. This noise-based, step-wise, bidirectional and penalty-free signal enforces strict preference separation, enabling more aggressive and precise policy improvement. 

In summary, our main contributions are as follows: 

- We propose _π_ -StepNFT, a critic-and-likelihood-free online RL framework tailored for flow-based VLAs, which eliminates the need to train auxiliary value networks that are prone to multimodal overfitting, and requires only a single forward pass per optimization step. 

- We identify that wider exploration spaces induced by SDE necessitate finer-grained guidance. By shifting the supervision target from the terminal to the immediate next denoising step and incorporating a logistic contrastive ranking objective, we resolve the supervision mismatch and reinforce successful exploration. 

- We validate our approach through extensive experiments on LIBERO (Liu et al., 2023) and ManiSkill (Mu et al., 2021) benchmarks. On LIBERO, _π_ -StepNFT unlocks the policy’s potential in few-shot settings, achieving a **32.9% improvement** over SFT. On ManiSkill, it demonstrates superior generalization in visually diverse OOD settings by preventing critic-induced multimodal overfitting, outperforming critic-based baselines by **11.1%** in unseen scenarios, highlighting its potential for complex real-world deployment. 

2 

_π_ **-StepNFT: Wider Space Needs Finer Steps in Online RL for Flow-based VLAs** 

# **2. Related Works** 

## **2.1. Online RL for VLAs** 

Recent VLA models have evolved from discrete tokenization (Zitkovich et al., 2023; Kim et al., 2024; Liu et al., 2026) to continuous flow-based policies (Ghosh et al., 2024; Black et al., 2026; 2025; Intelligence et al., 2025), which establish strong priors for manipulation. However, fine-tuning these flow-based VLAs faces the challenge of intractable action likelihoods due to multi-step ODE sampling. Existing solutions generally adopt two strategies to circumvent this: bypassing likelihood calculation via value distillation or preference feedback (e.g., GR-RL (Li et al., 2025b), _π_ 0<sup>_∗_</sup> _._ 6<sup>),</sup> or approximating likelihoods by transforming ODEs into SDEs (e.g., _π_ RL (Chen et al., 2025)). Similar to test-time scaling strategies (Yang et al., 2025; Song et al., 2025), noise injection in SDEs facilitates exploration, yet existing methods often struggle to balance exploration width with supervision granularity. 

## **2.2. Policy Optimization for Generative Models** 

To handle intractable likelihoods in generative policy optimization, prior works typically follow three paradigms. Explicit gradient and advantage methods (Black et al., 2023; Liu et al., 2025; Zhang et al., 2025b) treat denoising as a sequential process but often require expensive backpropagation through solvers. Reward-Weighted methods (Pfrommer et al., 2025; Fan et al., 2025; McAllister et al., 2025) avoid exact likelihoods by re-weighting regression targets, yet they can suffer from high variance in gradient estimation. Preference and contrastive methods (Wallace et al., 2024; Zhang et al., 2025a) offer a more stable alternative by aligning distributions via ranking. Most notably, Diffusion-NFT (Zheng et al., 2026) proposes a likelihood-free framework using implicit forward-process updates. Our work extends this efficient paradigm to embodied control, addressing the unique supervision gaps that arise when applying it to multi-step VLA policies. Please refer to Appendix B for detailed related works. 

# **3. Preliminaries** 

We use two time scales throughout the paper: environment steps and denoising time. An episode trajectory is indexed by environment steps _i_ = 0 _, . . . , H −_ 1, yielding _τ_ = _{_ ( _si, ai_ ) _}_<sup>_H_</sup> _i_ =0<sup>_−_1.Separately, the flow policy uses a</sup> continuous denoising time _t ∈_ [0 _,_ 1] (or a discretization) to generate an action. When discretized, we use _K_ solver steps with schedule 1 = _t_ 0 _> t_ 1 _> · · · > tK_ = 0, and denote intermediate sampler states by _{xtj }_<sup>_K_</sup> _j_ =0<sup>, where</sup><sup>_K_is typi-</sup> cally small in embodied control due to real-time constraints. Unless stated otherwise, _t_ refers to denoising time in the sampler, while the environment index is _i_ , avoiding ambi- 

guity when both the RL objective and the flow dynamics appear in the same derivations. 

## **3.1. Flow Matching for VLA Models** 

We consider a VLA policy that generates continuous actions _x_ 0 _∈_ R<sup>_d_</sup> conditioned on context _c_ . Flow-matching (Lipman et al., 2022) learns a time-dependent vector field _vθ_ ( _x, t, c_ ) to generate data by transforming a noise distribution _x_ 1 _∼ N_ (0 _, I_ ) to the data distribution _x_ 0 over time _t ∈_ [0 _,_ 1]. 

The standard flow-matching objective regresses the network prediction _vθ_ onto the target field _ut_ = _x_ 1 _− x_ 0 by minimizing _L_ CFM( _θ_ ) = E _t,x_ 0 _,x_ 1[ _∥vθ_ ( _xt, t, c_ ) _− ut∥_<sup>2</sup> ], where _xt_ = _tx_ 1 + (1 _− t_ ) _x_ 0. 

**ODE Sampling.** In the standard deterministic setting, inference is performed by numerically integrating the ODE _dx_ = _vθ_ ( _x, t, c_ ) _dt_ from _t_ = 1 to _t_ = 0. Using a discrete step size _δt >_ 0, the Euler update rule for the next step _xt−_ (where _t_<sup>_−_</sup> = _t − δt_ ) is: 


While efficient for generation, this deterministic trajectory lacks the exploratory capability required for reinforcement learning. 

**SDE Sampling.** To enable exploration, we adopt the reversetime SDE formulation (Liu et al., 2025), which injects stochasticity while preserving the marginal distribution. The Euler-Maruyama discretized update is given by: 


where _ϵ ∼N_ (0 _, I_ ) provides exploration noise. This update step induces a Gaussian transition density _qθ,t_ ( _xt− | xt, c_ ) = _N_ � _µθ,t_ ( _xt_ ) _,_ Σ _t_ �. Crucially, the mean of this transition is an affine transformation of the network output: 


where _Ut_ and _Bt_ are pre-determined coefficients derived from the noise schedule (detailed in Appendix A.1). 

This linear relationship allows us to propagate gradients efficiently from the transition target to the policy parameters without backpropagating through the ODE solver. 

## **3.2. RL Fine-tuning and the Likelihood Gap** 

We formulate the fine-tuning task as maximizing the expected return _J_ ( _θ_ ) over trajectories _τ_ = ( _s_ 0 _, a_ 0 _, . . ._ ): _J_ ( _θ_ ) = E _τ ∼pθ_ ( _τ_ )[ _R_ ( _τ_ )] _,_ where the trajectory distribution is determined by the environment dynamics and the policy: _pθ_ ( _τ_ ) = _p_ ( _s_ 0)<sup>�</sup><sup>_H_</sup> _i_ =0<sup>_−_1</sup><sup>_πθ_(</sup><sup>_ai|si_)</sup><sup>_p_(</sup><sup>_si_+1</sup><sup>_|si, ai_).</sup> 

3 

_π_ **-StepNFT: Wider Space Needs Finer Steps in Online RL for Flow-based VLAs** 

**Algorithm 1** _π_ -StepNFT: Step-wise Negative-aware FineTuning with Contrastive Ranking 

|**Require:** Flow policy _πθ_old, simulator _E_, env steps _H_,<br>solver steps_K_, schedule_{tj}_<sup>_K_</sup><br>_j_=0<sup>, hyperparams</sup><sup>_β, λ_TR.</sup>|
|---|
|Initialize_θ ←θ_<sup>old</sup>, buffer_D ←∅_.|
|**for**each iteration_m_**do**|
|// Phase 1: Data Collection|
|**for**each task(initial state_s_0_,_language prompt_c_)**do**<br>Rollout_H_ env steps using_πθ_old.|
|**for**_i_= 0**to**_H −_1**do**|
|Run Flow-SDE sampler; get chain_{xtj}_<sup>_K_</sup><br>_j_=0<sup>.</sup>|
|Sample_j ∼U{_0_, . . . , K −_1_}_; set_t ←tj_.|
|Set_xt ←xtj_ and_xt−←xtj_+1.<br>Set_v_<sup>old</sup><br>_t_<br>_←πθ_old(_c, si, xt, t_).<br>|
|Record_di_ = (_xt, xt−, v_<sup>old</sup><br>_t _<sup>_, t, si, c_).</sup>|
|Execute_xtK_ in_E_ and update_si_<br>**end for**<br>|
|Observe terminal_r ∈{_0_,_1_}_;_D ←{_(_di, r_)_}_<sup>_H−_1</sup><br>_i_=0 <sup>.</sup><br>**end for**|
|// Phase 2: Optimization|
|**for**each batch(_xt, xt−, v_<sup>old</sup><br>_t _<sup>_, t, s, c, r_)</sup><sup>_∼D_</sup><sup>**do**</sup><br>Pred_vθ,t ←πθ_(_c, s, xt, t_); Drift∆_vθ ←vθ,t −v_<sup>old</sup><br>_t_ <sup>.</sup><br><br>|
|Construct mirrors: _v_<sup>_±_</sup><br>_θ _<sup>_←v_old</sup><br>_t_<br>_± β_∆_vθ_.<br>Calc means/var: _µ_<sup>_±_</sup><br>_θ,t_<sup>_,_ Σ</sup><sup>_t ←_Mean</sup><br>~~V~~ar(_xt, v_<sup>_±_</sup><br>_θ _<sup>_, t_).</sup>|
|Calc errors: _E_<sup>_±_</sup><br>_θ,t _<sup>_←∥xt−−µ±_</sup><br>_θ,t_<sup>_∥_2</sup><br>Σ<sup>_−_1</sup><br>_t_ <sup>.</sup>|
|Set_y ←_2_r −_1and∆_Eθ ←E_<sup>+</sup><br>_θ,t _<sup>_−E−_</sup><br>_θ,t_<sup>.</sup>|
|_L_total _←_softplus<br>�1<br>2<sup>_y_∆</sup><sup>_Eθ_</sup><br>�<br>+_λ_TR_∥_∆_vθ∥_<sup>2</sup>.|
|Update_θ ←θ −η∇θL_total.|
|**end for**|
|_θ_<sup>old</sup> _←αmθ_<sup>old </sup>+ (1_−αm_)_θ_; clear_D_.|
|**end for**|
|**Output:** Optimized policy_πθ_.|


Standard policy gradient methods rely on the score function: _∇θJ_ ( _θ_ ) = E _τ_ [<sup>�</sup> _i_<sup>_∇θ_log</sup><sup>_πθ_(</sup><sup>_ai|si_)</sup><sup>_·_Ψ</sup><sup>_i_], where Ψ</sup><sup>_t_is the</sup> advantage or return (e.g., REINFORCE (Williams, 1992), PPO (Schulman et al., 2017)). 

However, for flow-based policies, calculating the explicit log-likelihood log _πθ_ ( _ai|si_ ) is computationally expensive and numerically unstable, as it requires integrating the instantaneous change of variables (Jacobian trace) along the entire generation trajectory. This intractability prevents the direct application of standard RL algorithms, motivating our likelihood-free approach. 

# **4. Method** 

We introduce _π_ -StepNFT (Step-wise Negative-aware FineTuning), an online RL framework designed for flow-based VLA models, as shown in Algorithm 1. Our method is inspired by Diffusion-NFT (Zheng et al., 2026), which finetunes diffusion models using a weighted-MSE objective on the final denoised output _x_ 0 generated by ODE rollouts. 

**Wider Space Needs Finer Steps.** While effective for image generation, we observe that directly transferring the ODE-based formulation to embodied control yields suboptimal convergence. We attribute this domain gap to two critical factors, requiring us to establish a _Wider Space_ for exploration anchored by _Finer Steps_ of supervision (made practical by the typically short denoising path in embodied control): 

- **Lack of Exploration:** Deterministic ODE rollouts quickly collapse to a narrow manifold, failing to discover diverse solutions in high-dimensional action spaces. We instead adopt an SDE-based formulation to inject controlled noise. This active expansion creates the necessary _wider space_ for the policy to traverse and learn from adjacent regions around the expert trajectory. 

- **Supervision Target Mismatch:** Operating within this wider space renders standard terminal- _x_ 0 supervision unstable, as injected noises accumulate and amplify variance over the rollout horizon. To counteract this, we require _finer steps_ of guidance: we supervise the immediate one-step transition _xt → xt−_ with variance normalization, providing the precise, low-variance local gradients needed for robust alignment. 

## **4.1. Step-wise Transitions and Mirror Errors** 

We conduct rollouts using the Flow-SDE solver described in Section 3.1 with a rollout policy _πθ_ old which is updated with EMA across iterations. Each episode yields an environment trajectory _τ_ = _{_ ( _si, ai_ ) _}_<sup>_H_</sup> _i_ =0<sup>_−_1.Ateachenvironmentstep</sup> _i_ , the policy generates _ai_ by running a _K_ -step solver with schedule 1 = _t_ 0 _> t_ 1 _> · · · > tK_ = 0, producing sampler states _{x_<sup>(</sup> _tj_<sup>_i_)</sup><sup>_}_</sup> _j_<sup>_K_</sup> =0<sup>; we execute the chunked terminal sample</sup> _x_<sup>(</sup><sup>_i_)</sup> _tK_ in the simulator as _ai_ . For efficiency, we uniformly sample one solver index _j ∼U{_ 0 _, . . . , K −_ 1 _}_ and define a single solver transition ( _xt, xt− , t_ ) = ( _x_<sup>(</sup> _tj_<sup>_i_)</sup><sup>_, x_</sup> _t_<sup>(</sup> _j_<sup>_i_)</sup> +1<sup>_, tj_),</sup> where _t_<sup>_−_</sup> denotes the next solver time point in the discretization. We additionally record the rollout velocity _v_<sup>old</sup> = _πθ_<sup>old(</sup><sup>_c, xt, t_).Each episode also provides a terminal</sup> optimality signal _r_ ( _τ_ ) _∈_ [0 _,_ 1]. 

Following Diffusion-NFT, we construct two “mirrored” velocity candidates _v_<sup>+</sup> _θ_ and _v_<sup>_−_</sup> _θ_ , symmetric around _v_<sup>old</sup> along the update direction ∆ _vθ_ = _vθ − v_<sup>old</sup> : 


where _β >_ 0 is a trust-region hyperparameter controlling how far we deviate from the rollout policy to estimate a local improvement signal. This construction ensures symmetry: _vθ_<sup>+</sup><sup>_−v_old=</sup><sup>_v_old</sup><sup>_−v_</sup> _θ_<sup>_−_=</sup><sup>_β_∆</sup><sup>_vθ_.</sup> 

4 

_π_ **-StepNFT: Wider Space Needs Finer Steps in Online RL for Flow-based VLAs** 

Importantly, under the Flow-SDE transition Eq. (3), the onestep mean is an affine function of the velocity, so these two velocity candidates induce two Gaussian transition means _µ_<sup>_±_</sup> _θ, t_ = _µt_ ( _v_<sup>_±_</sup> _θ_ ) with shared covariance Σ _t_ . We then compute the variance-normalized step errors against the sampled next state _xt−_ : 


Intuitively, _Eθ,t_<sup>+measures how well the positive mirrored</sup> branch explains the observed stochastic transition, while _Eθ,t_<sup>_−_measuresthenegativebranch.NormalizingbyΣ</sup><sup>_t_</sup> (which reflects the injected noise level at solver time _t_ ) stabilizes gradient scales across timesteps. We next show how this yields a step-wise contrastive objective over mirrored perturbations. 

## **4.2.** _π_ **-StepNFT: Step-wise Contrastive Objective** 

Given a sampled solver transition ( _xt → xt−_ ) with terminal signal _r_ ( _τ_ ), we define _y_ = 2 _r_ ( _τ_ ) _−_ 1. We use _oracle_ to denote the ideal, outcome-conditioned comparison between _p_ ( _xt− | xt, c, o_ =1) and _p_ ( _xt− | xt, c, o_ =0), which is not directly observable. Our method replaces this with a computable ranking surrogate: we construct two **_symmetric perturbations_** around the rollout policy along the update direction and rank the two branches by which one assigns higher likelihood to the observed transition. 

**Definition 4.1** ( _π_ -StepNFT Objective) **.** For a sampled solver transition tuple ( _xt, xt− , t, c_ ) with episode label _y ∈_ [ _−_ 1 _,_ 1], let _Eθ,t_<sup>+and</sup><sup>_E_</sup> _θ,t_<sup>_−_denote the step-wise errors</sup> defined in Section 4.1. The step-level objective is: 


Minimizing _ℓt_ encourages _Eθ,t_<sup>+</sup><sup>_< E_</sup> _θ,t_<sup>_−_when the episode is</sup> successful ( _y >_ 0) and reverses the inequality for failures ( _y <_ 0). Intuitively, this ranks two local transition hypotheses along the update direction ∆ _vθ_ = _vθ − v_<sup>old</sup> , using the episode label as a weak preference signal. 

**Lemma 4.2** (Log-Likelihood Ratio) **.** _Under the shared covariance_ Σ _t, the difference in squared errors is proportional to the log-likelihood ratio of the two mirrored branches:_ 


_Proof._ See Appendix A.2. 

Lemma 4.2 shows that minimizing _ℓt_ ( _θ_ ) adjusts the constructed transition log-ratio log� _qqθθ_<sup>_−_+</sup> � according to the episode label _y_ . The two densities _qθ_<sup>_±_arisefromsym-</sup> metric perturbations _±β_ ∆ _vθ_ of the rollout policy, so this 

log-ratio provides a directional signal on the same observed solver transition ( _xt → xt−_ ). In contrast, DPO (Rafailov et al., 2023) ranks _outcome-conditioned_ distributions under a shared context, whereas we rank _update perturbations_ using only episode-level feedback. For _y_ = +1, minimizing the loss increases the log-ratio, favoring updates that make the observed transition more likely under the positive perturbation; for _y_ = _−_ 1, it encourages the opposite preference. Thus, _ℓt_ yields a low-variance step-wise surrogate, and in Section 4.3 we show that under small-step assumptions its induced updates align with the oracle improvement direction from outcome-conditioned posterior splits. 

## **4.3. Validity and Optimized Direction** 

This section closes the conceptual loop between our constructed step-wise objective and the oracle improvement signal. 

## **Oracle direction from posterior splits (not directly com-** 

**putable).** Let _o ∈_ 0 _,_ 1 denote the latent episode outcome under context _c_ . Posterior splits (Appendix A.4) induce an outcome-conditioned decomposition of the rollout posterior at solver time _t_ , which defines the oracle mean gap ∆ _µ_<sup>_⋆_</sup> _t_<sup>(</sup><sup>_xt, c_) (Lemma A.4). Intuitively, ∆</sup><sup>_µ⋆_</sup> _t_<sup>captures how the</sup> one-step transition mean would change if we could condition the rollout transition on success versus failure; we treat it as an ideal local improvement direction in mean space. Importantly, this oracle quantity is a reference defined under outcome conditioning, and is not directly observable from online rollouts. 

**Proposition 4.3** (Bayes Monotonicity) **.** _For fixed_ ( _xt, c_ ) _, the posterior_ P( _o_ = 1 _| xt− , xt, c_ ) _is strictly increasing in the oracle likelihood ratio_<sup>_<u>p</u>_</sup><sup><u>(</u></sup><sup>_xt−_</sup><sup>_<u>|xt,c,o</u>_=1)</sup> _p_ ( _xt− |xt,c,o_ =0)<sup>_._</sup> 

_Proof._ See Appendix A.3. 

Proposition 4.3 provides the key monotonic link: increasing the oracle transition ratio on the observed transition ( _xt → xt−_ ) strictly increases the posterior probability of success. This motivates seeking a step-wise objective that increases a success-vs-failure transition ratio, while acknowledging that the oracle-conditioned densities _p_ ( _· | o_ ) are inaccessible. 

**Computable surrogate via mirrored transitions (what we actually optimize).** Since the oracle success–failure ratio _<u>p</u>_ <u>(</u> _<u>|o</u>_ =1) _p_ ( _|o_ =0)<sup>is not observable online, we optimize a constructed</sup> step-wise surrogate based on the mirrored perturbations defined in Section 4.1. By Lemma 4.2, our ranking loss is equivalent to increasing (for _y >_ 0) or decreasing (for _<u>θ</u> y <_ 0) the constructed transition ratio<sup>_<u>q</u>_+</sup> _qθ_<sup>_−_evaluated on the</sup> observed transition ( _xt → xt−_ ). We next show that, under a small-step regime, the expected gradient induced by this constructed ratio aligns with the oracle mean-gap direction. 

5 

_π_ **-StepNFT: Wider Space Needs Finer Steps in Online RL for Flow-based VLAs** 

**Theorem 4.4** (Gradient Form and Small-Step Alignment) **.** _Let et_ = _xt− − µ_<sup>old</sup> _t be the residual of the rollout mean, dt_ = _µ_<sup>+</sup> _θ,t_<sup>_−µ_</sup> _t_<sup>_old_</sup> _be the displacement in mean space and Bt be the affine coefficient from Eq._ (3) _._ 

- _(a) The error difference satisfies_ 


- _(b) Consequently, the gradient of the step loss ℓt is_ 


_where zt is the softplus logit and σ_ ( _·_ ) _is the sigmoid._ 

- _(c) In the binary-success setting and for small updates (vθ ≈ v_<sup>old</sup> _so σ_ ( _zt_ ) _≈_ const _), the conditional expected direction aligns with the oracle mean gap:_ 


_Proof._ See Appendix A.5. 

Theorem 4.4 provides the missing “closed loop”: posterior splits define an _oracle_ local improvement signal ∆ _µ_<sup>_⋆_</sup> _t_<sup>, while</sup> our mirrored construction yields a _computable_ surrogate ratio whose small-step expected gradient provably points in the same mean-space direction. 

In contrast, the core directional term in _π_ -StepNFT (derived in Theorem 4.4) depends only on the error difference: 


**Implicit Penalty:** The decomposition of the objective above shows that wMSE optimizes the same alignment term _plus_ an additional quadratic penalty _∥dt∥_<sup>2</sup> Σ<sup>_−_</sup> _t_<sup>1.This penalty ex-</sup> plicitly discourages branch separation (and thus suppresses the magnitude of the policy update), even when the data suggests a strong corrective move (i.e., large alignment between _et_ and _dt_ ). In contrast, by using a logistic ranking loss, _π_ -StepNFT removes this intrinsic suppression and preserves the alignment signal as the dominant driver for policy improvement. 

**Push-pull dynamics:** In the binary case _r ∈{_ 0 _,_ 1 _}_ , the wMSE objective reduces to fitting only one branch: it _pulls_ the selected branch toward the observed transition but does not explicitly _push_ the other branch away. By contrast, our logistic ranking enforces a strict ordering between _Eθ,t_<sup>+and</sup> _Eθ,t_<sup>_−_:forsuccessfulepisodesitsimultaneouslypullsthe</sup> positive branch and pushes the negative branch away (and vice versa for failures). This bidirectional signal yields stronger separation and typically sharper gradients during fine-tuning, which translates into faster convergence and higher asymptotic performance in our experiments. 

# **5. Experiments** 

## **5.1. Experimental Setup** 

## **4.4. Comparison with Diffusion-NFT (Weighted-MSE)** 

Diffusion-NFT optimizes a reward-weighted regression objective. In our step-wise setting, the analogous form is _ℓ_<sup>wMSE</sup> _t_ ( _θ_ ) = _r Eθ,t_<sup>++ (1</sup><sup>_−r_)</sup><sup>_E_</sup> _θ,t_<sup>_−_, where</sup><sup>_E_</sup> _θ,t_<sup>_±_are the mir-</sup> rored step errors from Section 4.1. We next show that this weighted-MSE contains an _implicit separation penalty_ that can suppress branch separation (and hence policy updates), whereas our logistic ranking objective isolates the directional alignment signal and induces a clearer push–pull behavior. 

**Theorem 4.5** (Separation Penalty in wMSE) **.** _The wMSE loss decomposes as:_ 


_Proof._ See Appendix A.6. 

Here, defined in Section 4.3, _et_ = _xt− − µ_<sup>old</sup> _t_ is the rollout residual and _dt_ = _µ_<sup>+</sup> _θ,t_<sup>_−µ_</sup> _t_<sup>old</sup> is the mirrored mean displacement. The middle term is the directional alignment signal driven by _y_ , while the last term _∥dt∥_<sup>2</sup> Σ<sup>_−_</sup> _t_<sup>1</sup> is a separation penalty that discourages large branch displacement irrespective of _y_ . 

**Evaluation Benchmarks.** We evaluate on 2 multitask benchmarks. For LIBERO (Liu et al., 2023), we follow the standard protocol across four suites (Spatial, Object, Goal, Long), reporting average success rates over 500 episodes (50 states _×_ 10 sub-tasks) per suite. For ManiSkill (Mu et al., 2021), we adopt the PutOnPlateInScene multitask setting from RL4VLA (Liu et al., 2026) tested for generalization, which defines 4,352 compositional tasks derived from 16 objects, 17 receptacles, and 16 tabletop scenes. 

**Model Architectures.** We employ _π_ 0 and _π_ 0 _._ 5, OpenPi’s flow-based VLAs combining a PaliGemma-3B (Beyer et al., 2024; Steiner et al., 2024) backbone with a _∼_ 300M parameter flow-matching action expert. _π_ 0 _._ 5 incorporates an improved training paradigm. Adhering to official configurations, _π_ 0 uses vision, text, and proprioception, while _π_ 0 _._ 5 omits proprioception on LIBERO; this modality setting remains consistent across SFT and RL phases. 

**SFT Initialization.** We initialize our policy using _π_ RL checkpoints. For LIBERO, to prevent performance saturation from masking RL gains, we train on pruned subsets of the total 1,692 trajectories: _π_ 0 uses 58 trajectories for Spatial/Object/Goal and 208 for Long; _π_ 0 _._ 5 uses a unified 

6 

_π_ **-StepNFT: Wider Space Needs Finer Steps in Online RL for Flow-based VLAs** 

_Table 1._ Success rates (%) on LIBERO in the few-shot setting. 

|_Table 1._ Success rates (%|) on L|IBERO|in the|few-|shot se|tting.|08<br>1.0<br>||08<br>1.0<br>||
|---|---|---|---|---|---|---|---|---|---|---|
|**Model**|**Spatial**|**Object**|**Goal**|**Long**|**Avg.**|∆**Avg.**|.<br>ate||.<br>ate||
|**# Full SFT**|||||||0.6<br>s R||0.6<br>s R||
|Octo (Ghosh et al.,2024)|78.9|85.7|84.6|51.1|75.1|—|04<br>ces||04<br>ces|~~x~~<br>~~(~~<br><sup>~~= 01)~~</sup>|
|OpenVLA (Kim et al.,2024)|84.7|88.4|79.2|53.7|76.5|—|.<br>uc||.<br>uc|t<br><br>0 <sup>~~.~~</sup><br>~~x~~<br>(<br><sup>= 01)</sup>|
|_π_fast (Pertsch et al.,2025)|96.4|96.8|88.6|60.2|85.5|—|0.2<br>S|SDE w/ Mean Correction<br>SDE w/o Mean Correction|0.2<br>S|t<br><br>0 <sup>.</sup><br>~~x~~0 ~~(~~<br>0 <sup>~~= 0.9)~~</sup>|
|OpenVLA-OFT (Kim et al.,2025b)|91.6<br>|95.3<br>|90.6<br>|86.5<br>|91.0<br>|—||<br>Deterministic ODE||x0 (<br>0 <sup>= 0.1)</sup>|
|_π_0|96.8|98.8|95.8|85.2|94.2|—|0.0||0.0||
|_π_0_._5|98.8|98.2|98.0|92.4|96.9|—|0|50<br>100<br>150<br>200<br>Training Steps||0<br>50<br>100<br>150<br>200<br>Training Steps|
|**# Few-shot SFT + RL**|||||||||||
|SFT<br>|65.3<br>|64.4<br>|49.8<br>|51.2<br>|57.6<br>|—<br>|_(a)_ **Sto**|**chastic rollouts.** ODE|_(b)_ **Re**|**gression target.** _x_0 vs.|
|_π_RL (Flow-SDE + PPO)|98.4|99.4|96.2|90.2|96.0|+38.4|||||
|_π_0<br>  <br>_π_RL (Flow-SDE + GRPO)|97.8|97.8|83.2|81.4|90.0|+32.4|vs. Flo|w-SDE variants.|step-w|ise_xt−_supervision.|
|_π_-StepNFT|93.5|98.0|83.7|86.7|90.5|+32.9|||||
|**# Few-shot SFT + RL**|||||||_Figure_<br>l|_2._ Flow-SDE sampling an<br>bili|d step-|wise supervision improve|
|SFT|84.6|95.4|84.6|43.9|77.1|—|on-po|cy staty.|||
|_π_RL (Flow-SDE + PPO)|99.6|100|98.8|93.0|97.9|+20.8|||||
|_π_0_._5<br>_π_RL (Flow-SDE + GRPO)|97.4|99.8|91.2|77.6|91.5|+14.4|||||
|_π_-StepNFT|97.8|100|98.2|79.8|94.0|+16.9|0.8<br>1.0<br>ate||0.8<br>1.0<br>ate||
|_able 2._ Success rates (%|) on M|aniSk|ill acro|ss In|-Distri|bution|0.6<br>R||0.6<br>R||
|IND) and Out-Of-Distribu|tion (|OOD) s|ettings|.|||0.4<br>uccess|Contrastive Ranking|0.4<br>uccess||
|**Model**|**IND**|||**OOD**|||0.2<br>S|wMSE<br>Positive Branch<br>|0.2<br>S|Terminal Binary Reward<br>Normalized GRPO Adv<br>|
|||**Vision**|**Semant**|**ic**<br>**E**|**xecution**|**Avg.**|0.0|Negative Branch|0.0|Normalized GAE Adv|
|_π_0<br>Full SFT<br>_π_RL (Flow-SDE + PPO)|38.4<br>78.8|32.6<br>61.1|8.4<br>25.4||13.2<br>31.5|18.1<br>39.3|0|50<br>100<br>150<br>200<br>Training Steps||0<br>50<br>100<br>150<br>200<br>Training Steps|
|_π_-StepNFT|**79.2**|**69.1**|**49.1**||**33.1**|**50.4**|_(a)_ **Lo**|**ss formulation.** wMSE|_(b)_**Cr**|**itic-free learning.** Sparse|
|Full SFT|40.1|40.2|16.6||22.4|26.4|vs. con|trastive ranking.|labels|vs. advantage signals.|


_Table 2._ Success rates (%) on ManiSkill across In-Distribution (IND) and Out-Of-Distribution (OOD) settings. 

|**Model**||**IND**||**OO**|**D**||
|---|---|---|---|---|---|---|
||||**Vision**|**Semantic**|**Execution**|**Avg.**|
||Full SFT|38.4|32.6|8.4|13.2|18.1|
|_π_0|_π_RL (Flow-SDE + PPO)|78.8|61.1|25.4|31.5|39.3|
||_π_-StepNFT|**79.2**|**69.1**|**49.1**|**33.1**|**50.4**|
||Full SFT|40.1|40.2|16.6|22.4|26.4|
|_π_0_._5|_π_RL (Flow-SDE + PPO)|**90.9**|68.0|34.5|**45.4**|49.3|
||_π_-StepNFT|85.4|**76.9**|**56.6**|45.1|**59.5**|


_Figure 3._ Contrastive ranking enables stable critic-free learning. 

few-shot set of 40 trajectories (1 per sub-task). As for ManiSkill, we use the full 16,384 trajectories due to task complexity. 

**RL Training Protocol.** We freeze the VLM backbone and fine-tune only the action expert. Training utilizes the RLinf (Yu et al., 2025) framework, which maximizes throughput by co-locating the environment, rollout policy, and actor on the same GPU. Main experiments were conducted on 8 _×_ NVIDIA H100 (80GB) GPUs; ablations used 8 _×_ NVIDIA RTX 4090 (48GB). Hyperparameters are detailed in the Appendix C.2. 

## **5.2. Main Results** 

## **LIBERO: Unlocking potential from few-shot SFT.** 

Table 1 reveals that SFT baselines are constrained by a narrow expert manifold, yielding initial success rates of only 57.6% ( _π_ 0) and 77.1% ( _π_ 0 _._ 5). _π_ -StepNFT unlocks the model’s latent capacity via “wider space” exploration, significantly boosting average performance to 90.5% and 94.0%, respectively. Notably, on short-horizon tasks (e.g., Object), our method achieves performance comparable to PPO. Regarding alignment, while critic-based methods (PPO) maintain an advantage in long-horizon tasks due to temporal credit assignment, our method notably outperforms the critic-free GRPO baseline (e.g., 86.7% vs. 81.4% on _π_ 0 Long), demonstrating that step-wise supervision offers 

highly competitive guidance without the need for estimating advantages. 

## **ManiSkill: Critic-free generalization.** 

Unlike LIBERO, ManiSkill features high visual diversity, requiring generalization to unseen textures, objects and positions (OOD). Value-based methods estimate values from vision-language embeddings, which often causes critics to overfit to nuisance visual features and specific language prompts rather than task semantics. _π_ -StepNFT bypasses this by relying on ground-truth outcomes. As shown in Table 2, while PPO is competitive in IND settings, _π_ -StepNFT dominates in OOD scenarios. For _π_ 0, it achieves an OOD average of 50.4% (+11.1% over PPO), nearly doubling success rates on Semantic shifts (unseen objects/instructions) to 49.1%. This robust trend holds for _π_ 0 _._ 5 (59.5% OOD average vs. 49.3%), confirming that critic-free supervision effectively mitigates visual overfitting. 

## **5.3. Ablations Studies** 

To verify the efficacy of _π_ -StepNFT, we conduct a component-wise analysis aligned with the challenges identified in Section 1. First, we decouple the effects of _stochastic exploration_ , investigating whether SDE sampling with noise-aware correction is strictly necessary for manifold expansion compared to deterministic ODEs. Second, we analyze _supervision granularity_ , contrasting our step-wise 

7 

_π_ **-StepNFT: Wider Space Needs Finer Steps in Online RL for Flow-based VLAs** 


_Figure 4._ **Hyperparameter sensitivity analysis.** Configuration selected for main experiments is highlighted by the **bold pink** curves. 

_xt−_ target against the standard terminal _x_ 0 regression to demonstrate its impact on training stability and convergence speed. Third, we evaluate the _learning objective_ , comparing our contrastive ranking formulation against weighted-MSE to highlight the benefits of removing the implicit separation penalty. Finally, we assess the necessity of _explicit critics_ , showing that our likelihood-free framework achieves competitive performance using only sparse binary rewards, and provide a sensitivity analysis for key hyperparameters. 

**Impact of Stochastic Exploration.** To isolate the benefit of exploration, we compare rollout strategies while fixing the regression target to the final denoised output _x_ 0 and using a conservative EMA schedule ( _α_ : 0.9 _→_ 0.995). As shown in Figure 2a, deterministic ODE rollouts ❶(Figure 1) plateau early, confirming that restricted state coverage hinders policy improvement. While standard SDE ❷ widens the visited manifold, significant performance gains are only realized when the objective explicitly accounts for injected noise via mean correction ❸ (Eq. (3)). This indicates that effective exploration requires not just traversing a wider space, but utilizing a learning signal that mathematically aligns the noisy transition back to the policy’s velocity field. 

**Regression Target Granularity.** We evaluate the efficacy of terminal _x_ 0 versus step-wise _xt−_ regression targets under stochastic rollouts in Figure 2b. Empirical results demonstrate that supervision via _x_ 0 induces significant instability, necessitating overly conservative synchronization to prevent policy collapse. Conversely, the step-wise target _xt−_ ❹ facilitates stable, near on-policy learning even under aggressive updates, thereby accelerating convergence. This suggests that precise, local supervision is essential to counteract the distribution shift introduced by active exploration, whereas terminal targets provide gradients that are too coarse for effective manifold adherence . 

**Objective Formulation: Ranking vs. wMSE.** We benchmark the proposed contrastive ranking objective against a weighted-MSE (wMSE) baseline and single-branch ablations in Figure 3a. We observe that utilizing exclusively Positive or Negative branches yields partial improvement. This confirms that valid gradient signals exist in both directions, yet combining them yields superior performance. 

Crucially, the wMSE baseline underperforms because, in the binary reward setting, it degenerates to fitting a single branch . Consequently, it fails to leverage both positive and negative signals simultaneously. In contrast, our ranking objective establishes a ”push-pull” dynamic by utilizing both branches to enforce strict preference separation. This effectively removes the ”implicit separation penalty” that otherwise suppresses the policy update magnitude. 

**Necessity of Value Estimation.** We investigate the tradeoff between supervision density and training complexity in Figure 3b. Although dense step-level value estimates can in principle improve long-horizon credit assignment, sparse trajectory-level outcomes remain highly competitive for general manipulation tasks. Empirically, binary supervision yields smoother training because it relies on accurate environment feedback rather than approximate value estimates. Unlike image generation, where sample quality varies continuously and advantage-style soft weighting is more natural, embodied control typically has discrete success-or-failure outcomes, similar to mathematical reasoning (Chen et al., 2026). Correspondingly, treating _r_ as a bounded trajectory success probability _r ∈_ [0 _,_ 1] avoids the instability of unbounded advantage scores and reduces the need for normalization and clipping. Our probability-based formulation is also compatible with denser supervision: the sparse signal can be replaced by an offline critic-learned that predicts step-wise success probabilities, enabling finer credit assignment without changing the architecture. 

**Hyperparameter Sensitivity and Robustness.** Figure 4 illustrates key trade-offs. For noise level _σ_ , excessive noise impedes convergence by overly expanding the search space, while insufficient noise limits exploration. For trust region size _β_ , results indicate that values around [1 _._ 0 _,_ 2 _._ 0] are optimal; larger _β_ violate local linearity, whereas smaller steps induce gradient instability. Regarding the decay _α_ , a dynamic strategy proves most effective. High decay (slow updates) causes significant off-policy lag and lowers the performance ceiling, while constant or overly aggressive updates risk collapse. A dynamic schedule that progressively increases decay balances initial acceleration with final stability, which matches the small-step alignment in Theorem 4.4. 

8 

_π_ **-StepNFT: Wider Space Needs Finer Steps in Online RL for Flow-based VLAs** 

# **6. Conclusion** 

In this paper, we introduced _π_ -StepNFT, a critic-andlikelihood-free framework for flow-based VLAs that structurally eliminates auxiliary value networks and requires only a single forward pass per step. We identified that wider exploration spaces necessitate finer-grained, step-wise guidance for effective alignment. Empirically, _π_ -StepNFT unlocks latent potential on LIBERO in few-shot SFT settings and achieves superior OOD generalization on ManiSkill by preventing multimodal overfitting. These results establish a scalable, robust paradigm for fine-tuning generalist robot policies in complex real-world scenarios. 

# **Impact Statement** 

This paper introduces a framework for fine-tuning flowbased vision-language-action (VLA) policies to improve the efficiency and robustness of embodied agents. Beyond algorithmic advances, our work has implications for the accessibility and sustainability of robotic learning. 

**Democratization of embodied AI research:** Training large-scale VLA models often requires substantial compute, in part due to the cost of differentiating through ODE trajectories. By proposing a likelihood-free, critic-free approach that uses a single forward pass per optimization step, _π_ -StepNFT lowers the hardware barrier. This reduced overhead can broaden participation by smaller labs and academic groups, supporting a more diverse research community. 

**Safety and robustness:** By improving out-of-distribution (OOD) generalization, our method can yield agents that behave more reliably in unstructured real-world settings. While increased capability may introduce dual-use concerns, our fine-grained supervision encourages adherence to expert manifolds and may reduce unpredictable behaviors during deployment. 

# **References** 

- Bai, J., Yu, X., Xu, M., Lu, W., Pan, X., Maeng, K., Kifer, D., Wang, J., and Wang, Y. Towards better optimization for listwise preference in diffusion models. _arXiv preprint arXiv:2510.01540_ , 2025. 

- Beyer, L., Steiner, A., Pinto, A. S., Kolesnikov, A., Wang, X., Salz, D., Neumann, M., Alabdulmohsin, I., Tschannen, M., Bugliarello, E., et al. Paligemma: A versatile 3b vlm for transfer. _arXiv preprint arXiv:2407.07726_ , 2024. 

- Bjorck, J., Castaneda, F., Cherniadev, N., Da, X., Ding, R.,˜ Fan, L., Fang, Y., Fox, D., Hu, F., Huang, S., et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- Black, K., Janner, M., Du, Y., Kostrikov, I., and Levine, S. 

Training diffusion models with reinforcement learning. 2023. 

- Black, K., Brown, N., Darpinian, J., Dhabalia, K., Driess, D., Esmail, A., Equi, M. R., Finn, C., Fusai, N., Galliker, M. Y., et al. _π_ 0 _._ 5: a vision-language-action model with open-world generalization. In _9th Annual Conference on Robot Learning_ , 2025. 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., Jakubczak, S., Jones, T., Ke, L., Levine, S., LiBell, A., Mothukuri, M., Nair, S., Pertsch, K., Shi, L. X., Tanner, J., Vuong, Q., Walling, A., Wang, H., and Zhilinsky, U. _π_ 0: A vision-language-action flow model for general robot control, 2026. URL https: //arxiv.org/abs/2410.24164. 

- Chen, H., Zheng, K., Zhang, Q., Cui, G., Cui, Y., Ye, H., Lin, T.-Y., Liu, M.-Y., Zhu, J., and Wang, H. NFT: Bridging supervised learning and reinforcement learning in math reasoning. In _The Fourteenth International Conference on Learning Representations_ , 2026. URL https:// openreview.net/forum?id=ujBrsQm6Zu. 

- Chen, K., Liu, Z., Zhang, T., Guo, Z., Xu, S., Lin, H., Zang, H., Li, X., Zhang, Q., Yu, Z., Fan, G., Huang, T., Wang, Y., and Yu, C. _π_ RL: Online rl fine-tuning for flow-based vision-language-action models, 2025. URL https://arxiv.org/abs/2510.25889. 

- Christiano, P. F., Leike, J., Brown, T., Martic, M., Legg, S., and Amodei, D. Deep reinforcement learning from human preferences. _Advances in neural information processing systems_ , 30, 2017. 

- Fan, J., Shen, S., Cheng, C., Chen, Y., Liang, C., and Liu, G. Online reward-weighted fine-tuning of flow matching with wasserstein regularization. In _The Thirteenth International Conference on Learning Representations_ , 2025. 

- Fan, Y., Watkins, O., Du, Y., Liu, H., Ryu, M., Boutilier, C., Abbeel, P., Ghavamzadeh, M., Lee, K., and Lee, K. Reinforcement learning for fine-tuning text-to-image diffusion models. In _Thirty-seventh Conference on Neural Information Processing Systems_ , 2023. URL https: //openreview.net/forum?id=8OTPepXzeh. 

- Ghosh, D., Walke, H., Pertsch, K., Black, K., Mees, O., Dasari, S., Hejna, J., Kreiman, T., Xu, C., Luo, J., Tan, Y. L., Chen, L. Y., Sanketi, P., Vuong, Q., Xiao, T., Sadigh, D., Finn, C., and Levine, S. Octo: An opensource generalist robot policy, 2024. URL https: //arxiv.org/abs/2405.12213. 

9 

_π_ **-StepNFT: Wider Space Needs Finer Steps in Online RL for Flow-based VLAs** 

- Han, J., Wang, A., Xu, M., Chu, W., Dang, M., Yue, Y., and Ermon, S. Discrete diffusion trajectory alignment via stepwise decomposition. _arXiv preprint arXiv:2507.04832_ , 2025. 

- Ho, J., Jain, A., and Abbeel, P. Denoising diffusion probabilistic models. _Advances in neural information processing systems_ , 33:6840–6851, 2020. 

- Intelligence, P., Amin, A., Aniceto, R., Balakrishna, A., Black, K., Conley, K., Connors, G., Darpinian, J., Dhabalia, K., DiCarlo, J., et al. _π_ 0<sup>_∗_</sup> _._ 6<sup>:a vla that learns from</sup> experience. _arXiv preprint arXiv:2511.14759_ , 2025. 

- Kim, D., Lyu, S., Kim, S. W., and Seo, P. H. Direct diffusion score preference optimization via stepwise contrastive policy-pair supervision. _arXiv preprint arXiv:2512.23426_ , 2025a. 

- Kim, M. J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E., Lam, G., Sanketi, P., et al. Openvla: An open-source vision-languageaction model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- Kim, M. J., Finn, C., and Liang, P. Fine-tuning visionlanguage-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025b. 

- Li, H., Zuo, Y., Yu, J., Zhang, Y., Yang, Z., Zhang, K., Zhu, X., Zhang, Y., Chen, T., Cui, G., et al. Simplevla-rl: Scaling vla training via reinforcement learning. _arXiv preprint arXiv:2509.09674_ , 2025a. 

- Li, Y., Ma, X., Xu, J., Cui, Y., Cui, Z., Han, Z., Huang, L., Kong, T., Liu, Y., Niu, H., et al. Gr-rl: Going dexterous and precise for long-horizon robotic manipulation. _arXiv preprint arXiv:2512.01801_ , 2025b. 

- Liao, X., Wei, W., Qu, X., and Cheng, Y. Step-level reward for free in rl-based t2i diffusion model fine-tuning. _arXiv preprint arXiv:2505.19196_ , 2025. 

- Lillicrap, T. P., Hunt, J. J., Pritzel, A., Heess, N., Erez, T., Tassa, Y., Silver, D., and Wierstra, D. Continuous control with deep reinforcement learning. _arXiv preprint arXiv:1509.02971_ , 2015. 

- Lipman, Y., Chen, R. T., Ben-Hamu, H., Nickel, M., and Le, M. Flow matching for generative modeling. _arXiv preprint arXiv:2210.02747_ , 2022. 

- Liu, B., Zhu, Y., Gao, C., Feng, Y., Liu, Q., Zhu, Y., and Stone, P. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791, 2023. 

- Liu, J., Liu, G., Liang, J., Li, Y., Liu, J., Wang, X., Wan, P., Zhang, D., and Ouyang, W. Flow-grpo: Training 

flow matching models via online rl. _arXiv preprint arXiv:2505.05470_ , 2025. 

- Liu, J., Gao, F., Wei, B., Chen, X., Liao, Q., Wu, Y., Yu, C., and Wang, Y. What can rl bring to vla generalization? an empirical study, 2026. URL https://arxiv.org/ abs/2505.19789. 

- Lu, G., Guo, W., Zhang, C., Zhou, Y., Jiang, H., Gao, Z., Tang, Y., and Wang, Z. Vla-rl: Towards masterful and general robotic manipulation with scalable reinforcement learning. _arXiv preprint arXiv:2505.18719_ , 2025. 

- McAllister, D., Ge, S., Yi, B., Kim, C. M., Weber, E., Choi, H., Feng, H., and Kanazawa, A. Flow matching policy gradients. _arXiv preprint arXiv:2507.21053_ , 2025. 

- Mu, T., Ling, Z., Xiang, F., Yang, D., Li, X., Tao, S., Huang, Z., Jia, Z., and Su, H. Maniskill: Generalizable manipulation skill benchmark with large-scale demonstrations. _arXiv preprint arXiv:2107.14483_ , 2021. 

- NVIDIA. Nvidia h100 tensor core gpu datasheet. Technical report, NVIDIA, 2022. URL https://resources. nvidia.com/en-us-gpu-resources/ h100-datasheet-24306. Technical Report. 

- NVIDIA. Nvidia ampere gpu architecture whitepaper. Technical report, NVIDIA, 2023. URL https://images. nvidia.com/aem-dam/Solutions/geforce/ ada/nvidia-ada-gpu-architecture.pdf. Technical Report. 

- Pan, C., Anantharaman, G., Huang, N.-C., Jin, C., Pfrommer, D., Yuan, C., Permenter, F., Qu, G., Boffi, N., Shi, G., et al. Much ado about noising: Dispelling the myths of generative robotic control. _arXiv preprint arXiv:2512.01809_ , 2025. 

- Pei, M., Li, G., Si, J., Zhu, Z., Mo, Z., Wang, P., Song, Z., Liang, X., and Cheng, J. Gcc: A 3dgs inference architecture with gaussian-wise and cross-stage conditional processing. In _Proceedings of the 58th IEEE/ACM International Symposium on Microarchitecture_ , pp. 1824– 1837, 2025. 

- Pertsch, K., Stachowicz, K., Ichter, B., Driess, D., Nair, S., Vuong, Q., Mees, O., Finn, C., and Levine, S. Fast: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 

- Pfrommer, S., Huang, Y., and Sojoudi, S. Reinforcement learning for flow-matching policies. _arXiv preprint arXiv:2507.15073_ , 2025. 

- Rafailov, R., Sharma, A., Mitchell, E., Manning, C. D., Ermon, S., and Finn, C. Direct preference optimization: Your language model is secretly a reward model. 

10 

_π_ **-StepNFT: Wider Space Needs Finer Steps in Online RL for Flow-based VLAs** 

- _Advances in neural information processing systems_ , 36: 53728–53741, 2023. 

- Schulman, J., Wolski, F., Dhariwal, P., Radford, A., and Klimov, O. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- Shukor, M., Aubakirova, D., Capuano, F., Kooijmans, P., Palma, S., Zouitine, A., Aractingi, M., Pascal, C., Russi, M., Marafioti, A., et al. Smolvla: A vision-languageaction model for affordable and efficient robotics. _arXiv preprint arXiv:2506.01844_ , 2025. 

- Song, H., Qu, D., Yao, Y., Chen, Q., Lv, Q., Tang, Y., Shi, M., Ren, G., Yao, M., Zhao, B., et al. Hume: Introducing system-2 thinking in visual-language-action model. _arXiv preprint arXiv:2505.21432_ , 2025. 

- Song, Y., Sohl-Dickstein, J., Kingma, D. P., Kumar, A., Ermon, S., and Poole, B. Score-based generative modeling through stochastic differential equations. _arXiv preprint arXiv:2011.13456_ , 2020. 

- Steiner, A., Pinto, A. S., Tschannen, M., Keysers, D., Wang, X., Bitton, Y., Gritsenko, A., Minderer, M., Sherbondy, A., Long, S., et al. Paligemma 2: A family of versatile vlms for transfer. _arXiv preprint arXiv:2412.03555_ , 2024. 

- Sun, M., Ding, P., Zhang, W., and Wang, D. Iterative refinement of flow policies in probability space for online reinforcement learning. _arXiv preprint arXiv:2510.15388_ , 2025. 

- Sutton, R. S., McAllester, D., Singh, S., and Mansour, Y. Policy gradient methods for reinforcement learning with function approximation. _Advances in neural information processing systems_ , 12, 1999. 

- Wagenmaker, A., Nakamoto, M., Zhang, Y., Park, S., Yagoub, W., Nagabandi, A., Gupta, A., and Levine, S. Steering your diffusion policy with latent space reinforcement learning. _arXiv preprint arXiv:2506.15799_ , 2025. 

- Wallace, B., Dang, M., Rafailov, R., Zhou, L., Lou, A., Purushwalkam, S., Ermon, S., Xiong, C., Joty, S., and Naik, N. Diffusion model alignment using direct preference optimization. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 8228–8238, 2024. 

   - Wu, Y.-L., Ruan, B.-K., Tseng, C., and Shuai, H.-H. Ranking-based preference optimization for diffusion models from implicit user feedback. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. 

   - Yang, S., Zhang, Y., He, H., Pan, L., Li, X., Bai, C., and Li, X. Steering vision-language-action models as antiexploration: A test-time scaling approach. _arXiv preprint arXiv:2512.02834_ , 2025. 

   - Ye, A., Wang, B., Ni, C., Huang, G., Zhao, G., Li, H., Li, J., Zhu, J., Feng, L., et al. Gigabrain-0: A world modelpowered vision-language-action model. _arXiv preprint arXiv:2510.19430_ , 2025. 

   - Yu, C., Wang, Y., Guo, Z., Lin, H., Xu, S., Zang, H., Zhang, Q., Wu, Y., Zhu, C., Hu, J., et al. Rlinf: Flexible and efficient large-scale reinforcement learning via macro-to-micro flow transformation. _arXiv preprint arXiv:2509.15965_ , 2025. 

   - Zhang, T., Da, C., Ding, K., Yang, H., Jin, K., Li, Y., Gao, T., Zhang, D., Xiang, S., and Pan, C. Diffusion model as a noise-aware latent reward model for step-level preference optimization. _arXiv preprint arXiv:2502.01051_ , 2025a. 

   - Zhang, T., Yu, C., Su, S., and Wang, Y. Reinflow: Finetuning flow matching policy with online reinforcement learning, 2025b. URL https://arxiv.org/abs/ 2505.22094. 

   - Zheng, K., Chen, H., Ye, H., Wang, H., Zhang, Q., Jiang, K., Su, H., Ermon, S., Zhu, J., and Liu, M.-Y. DiffusionNFT: Online diffusion reinforcement with forward process. In _The Fourteenth International Conference on Learning Representations_ , 2026. URL https://openreview. net/forum?id=VJZ477R89F. 

   - Ziegler, D. M., Stiennon, N., Wu, J., Brown, T. B., Radford, A., Amodei, D., Christiano, P., and Irving, G. Fine-tuning language models from human preferences. _arXiv preprint arXiv:1909.08593_ , 2019. 

   - Zitkovich, B., Yu, T., Xu, S., Xu, P., Xiao, T., Xia, F., Wu, J., Wohlhart, P., Welker, S., Wahid, A., et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pp. 2165–2183. PMLR, 2023. 

- Wang, F. and Yu, Z. Coefficients-preserving sampling for reinforcement learning with flow matching. _arXiv preprint arXiv:2509.05952_ , 2025. 

- Williams, R. J. Simple statistical gradient-following algorithms for connectionist reinforcement learning. _Machine learning_ , 8(3):229–256, 1992. 

11 

_π_ **-StepNFT: Wider Space Needs Finer Steps in Online RL for Flow-based VLAs** 

# **A. Theoretical Analysis and Proofs** 

In this section, we provide detailed proofs for the lemmas, propositions, and theorems presented in the main text. 

## **A.1. Proof of Equation 3 (Affine Mean Derivation)** 

We derive the explicit forms of _Ut_ and _Bt_ stated in Equation 3. 

The flow-SDE solver computes the next mean _µt_ ( _v_ ) by mixing the rectified flow endpoints _x_<sup>pred</sup> 0 = _xt − v · t_ and _x_<sup>pred</sup> 1 = _xt_ + _v ·_ (1 _− t_ ) with weights derived from the Euler-Maruyama discretization. The weights are given by: 


The mean is given by the linear combination: 


Directly computing the coefficients for _xt_ and _v_ yields: **Coefficient for** _xt_ **(** _Ut_ **):** 


**Coefficient for** _v_ **(** _Bt_ **):** 


Thus, _µt_ ( _v_ ) = _Ut_ ( _xt, t_ ) + _Bt_ ( _t_ ) _v_ , matching the affine form in Equation (3). 

## **A.2. Proof of Lemma 4.2 (Log-Likelihood Ratio)** 

We prove that the difference in variance-normalized errors equals the log-likelihood ratio. Let _q_ ( _x_ ) = _N_ ( _µ,_ Σ). Its log-density is: 


For the two branches _qt_<sup>+</sup> = _N_ ( _µ_<sup>+</sup> _t_<sup>_,_Σ</sup><sup>_t_)and</sup><sup>_q_</sup> _t_<sup>_−_</sup> = _N_ ( _µ_<sup>_−_</sup> _t_<sup>_,_Σ</sup><sup>_t_),theysharethesamecovarianceΣ</sup><sup>_t_.Subtractingtheir</sup> log-densities cancels the normalization constant: 


This concludes the proof. 

12 

_π_ **-StepNFT: Wider Space Needs Finer Steps in Online RL for Flow-based VLAs** 

## **A.3. Proof of Proposition 4.3 (Bayes Monotonicity)** 

Fix ( _xt, c_ ) and denote the prior success probability conditioned on ( _xt, c_ ) by _π_ ( _xt, c_ ) ≜ P( _o_ = 1 _| xt, c_ ) _∈_ (0 _,_ 1). 

By Bayes’ rule, the posterior success probability given the observed next state _xt−_ is 


Define the oracle likelihood ratio 


Dividing the numerator and denominator by _p_ ( _xt− | xt, c, o_ = 0) yields 


For constants _a_ = _π_ ( _xt, c_ ) _>_ 0 and _b_ = 1 _− π_ ( _xt, c_ ) _>_ 0, consider _f_ ( _λ_ ) = _aλaλ_ + _b_<sup>for</sup><sup>_λ >_0.Its derivative is</sup> 


Therefore _η_ ( _xt−_ ; _xt, c_ ) is strictly increasing in the likelihood ratio Λ( _xt−_ ; _xt, c_ ), completing the proof. 

## **A.4. Oracle Splits from Diffusion-NFT** 

**Notation and symbol disambiguation.** We use _κt_ ( _xt | x_ 0) to denote the _forward/noising kernel_ that maps a terminal sample _x_ 0 to an intermediate noisy state _xt_ (as in diffusion models). 

**Setup.** Fix a context _c_ . Let _x_ 0 denote the terminal sample (e.g., the final solver output used to form an action), with rollout terminal distribution _π_ 0<sup>old(</sup><sup>_x_0</sup><sup>_| c_) induced by</sup><sup>_π_</sup> _θ_<sup>old.Let</sup><sup>_κt_(</sup><sup>_xt| x_0) be the forward kernel and define the induced marginal</sup> 

and the diffusion posterior 


**Optimality variable.** Introduce a latent optimality variable _o ∈{_ 0 _,_ 1 _}_ and an instance-level score _r_ ( _x_ 0 _, c_ ) _∈_ [0 _,_ 1] satisfying _r_ ( _x_ 0 _, c_ ) = P( _o_ = 1 _| x_ 0 _, c_ ). This is the same setup as Diffusion-NFT; see their Appendix for proofs. **Lemma A.1** (Distribution Split (Diffusion-NFT)) **.** _Let p_ ( _c_ ) ≜ E _x_ 0 _∼π_ 0old( _·|c_ )<sup>[</sup><sup>_r_(</sup><sup>_x_0</sup><sup>_, c_)]</sup><sup>_.Define the oracle terminal distribu-_</sup> _tions_ 

_Then_ 


_Reference._ Diffusion-NFT Appendix (Distribution Split). 


_Then the rollout posterior satisfies_ 

_where the mixing weight is_ 


13 

_π_ **-StepNFT: Wider Space Needs Finer Steps in Online RL for Flow-based VLAs** 

_Reference._ Diffusion-NFT Appendix (Posterior Split). 

**Corollary A.3** (Posterior Expectation Split) **.** _Under Lemma A.2, for any integrable function ϕ_ ( _x_ 0) _,_ 


**Oracle vs. constructed branches.** The oracle objects ( _π_ 0<sup>_±, π_</sup> 0<sup>_±_</sup> _|t_<sup>)aredefinedbyconditioningonthelatentoutcome</sup> _o_ . In contrast, our method constructs mirrored branches _vθ_<sup>_±_=</sup><sup>_v_old</sup><sup>_± β_(</sup><sup>_vθ−v_old)andtheinducedsolvertransitions</sup> _qθ,t_<sup>_±_(</sup><sup>_xt−| xt, c_) (Section 4.1).</sup> 

**Lemma A.4** (Oracle Velocity/Mean Splits (for alignment)) **.** _Assume the (oracle) velocity field at solver time t can be expressed as a posterior expectation under π_ 0 _|t_ ( _· | xt, c_ ) _, i.e., v_ ( _xt, c, t_ ) = E _π_ 0 _|t_ ( _·|xt,c_ )[ _ψ_ ( _x_ 0 _, xt, c, t_ )] _for some function ψ. Define oracle velocities v_<sup>_±_</sup> _by taking the same expectation under π_ 0<sup>_±_</sup> _|t_<sup>_.Then_</sup> 


_If additionally the one-step solver mean admits the affine form µt_ ( _v_ ) = _Atxt_ + _Btv (Eq. 3), then_ 

_µ_<sup>old</sup> _t_ ( _xt, c_ ) = _α_ ( _xt, c_ ) _µ_<sup>+</sup> _t_<sup>(</sup><sup>_xt, c_) + (1</sup><sup>_−α_(</sup><sup>_xt, c_))</sup><sup>_µ_</sup> _t_<sup>_−_(</sup><sup>_xt, c_)</sup><sup>_,_</sup> ∆ _µ_<sup>_⋆_</sup> _t_<sup>(</sup><sup>_xt, c_) ≜</sup><sup>_µ_</sup> _t_<sup>+(</sup><sup>_xt, c_)</sup><sup>_−µ_</sup> _t_<sup>_−_(</sup><sup>_xt, c_) =</sup><sup>_Bt_</sup> � _v_<sup>+</sup> _− v_<sup>_−_�</sup> _._ 

_Remark._ This lemma is a direct consequence of Corollary A.3 and linearity of expectation. 

## **A.5. Proof of Theorem 4.4 (Gradient Form and Alignment)** 

Fix a sampled training tuple ( _xt, xt− , c_ ) collected under the rollout policy _v_<sup>old</sup> = _πθ_ old( _c, xt, t_ ). Let the rollout one-step mean be _µ_<sup>old</sup> _t_ := _µt_ ( _v_<sup>old</sup> ) and define the residual _et_ ≜ _xt− − µ_<sup>old</sup> _t_ . Recall that our constructed mirrored branches are _vθ_<sup>_±_</sup> = _v_<sup>old</sup> _± β_ ( _vθ − v_<sup>old</sup> ), ∆ _vθ_ ≜ _vθ − v_<sup>old</sup> , and that the one-step mean admits the affine form (Eq. 3) _µt_ ( _v_ ) = _Atxt_ + _Btv_ , with shared covariance Σ _t_ . 

**Step 1: Constructed mean shift.** Define the constructed branch means _µ_<sup>_±_</sup> _θ,t_<sup>≜</sup><sup>_µt_(</sup><sup>_v_</sup> _θ_<sup>_±_).</sup> Using the affine mean form, 


Hence, 


**Step 2: Error difference (Theorem 4.4.a).** Recall the step errors _Eθ_<sup>_±_=</sup><sup>_∥xt−−µ±_</sup> _θ,t_<sup>_∥_2</sup> Σ<sup>_−_</sup> _t_<sup>1.</sup> Substituting _µ_<sup>_±_</sup> _θ,t_<sup>=</sup><sup>_µ_</sup> _t_<sup>old</sup> _± dt_ and _et_ = _xt− − µ_<sup>old</sup> _t_ gives 


which proves part (a). 

**Step 3: Gradient form (Theorem 4.4.b).** Define the logit _zt_ ≜ <u>12</u><sup>_y_(</sup><sup>_E_</sup> _θ_<sup>+</sup><sup>_−E_</sup> _θ_<sup>_−_),</sup> _ℓt_ ( _θ_ ) = softplus( _zt_ ). Using _∇_ softplus( _z_ ) = _σ_ ( _z_ ), 


From Step 2, 


14 

_π_ **-StepNFT: Wider Space Needs Finer Steps in Online RL for Flow-based VLAs** 

thus 

_∇θzt_ =<sup><u>1</u></sup> 2<sup>_y ∇θ_(</sup><sup>_E_</sup> _θ_<sup>+</sup><sup>_−E_</sup> _θ_<sup>_−_) =</sup><sup><u>1</u></sup> 2<sup>_y ∇θ_</sup> � _−_ 4 _e_<sup>_⊤_</sup> _t_<sup>Σ</sup> _t_<sup>_−_1</sup><sup>_dt_</sup> � _._ 

During optimization we treat the rollout branch _v_<sup>old</sup> (hence _µ_<sup>old</sup> _t_ and _et_ ) as constant with respect to _θ_ , so only _dt_ depends on _θ_ . From Equation (24), _dt_ = _βBt_ ( _vθ − v_<sup>old</sup> ) and therefore 


Absorbing constant scalar factors into _∝_ , we obtain 

which proves part (b). 

**Step 4: Small-step alignment (general** _r ∈_ [0 _,_ 1] **and binary case).** We relate the conditional expected update direction to an _oracle_ improvement signal. Recall the signed label is defined in the main text as _y_ ≜ 2 _r −_ 1 _, r ∈_ [0 _,_ 1], where _r_ is the observed terminal signal (e.g., success indicator or a normalized score). 

Conditioned on ( _xt, c_ ), the rollout residual _et_ ≜ _xt− − µ_<sup>old</sup> _t_ ( _xt, c_ ) is zero-mean since _µ_<sup>old</sup> _t_ ( _xt, c_ ) = E[ _xt− | xt, c_ ], hence 


Therefore, 


_(i) General case (r ∈_ [0 _,_ 1] _)._ Equation (28) shows that the conditional expected direction is governed by the correlation between the terminal signal _r_ and the local rollout residual _et_ . In general, this produces a mixture of success- and failureassociated components (and does not reduce to a single oracle mean-gap direction without additional assumptions relating _r_ to the latent optimality variable). 

_(ii) Binary case (r ∈{_ 0 _,_ 1 _} with r_ = _o)._ In sparse-success RL we often take _r_ to be the episode success indicator, i.e., _r_ = _o ∈{_ 0 _,_ 1 _}_ where _o_ is the latent optimality variable. We have _α_ ( _xt, c_ ) ≜ P( _o_ = 1 _| xt, c_ ) in Lemma A.2. 

Then using the indicator property of _o_ and Equation (27), 


where _µ_<sup>+</sup> _t_<sup>(</sup><sup>_xt, c_) ≜E[</sup><sup>_x_</sup> _t_<sup>_−| xt, c, o_= 1] is the oracle success-branch mean.</sup> By Lemma A.4, the oracle mean mixture identity holds: 


hence 

_µ_<sup>+</sup> _t_<sup>(</sup><sup>_xt, c_)</sup><sup>_−µ_old</sup> _t_ ( _xt, c_ ) = (1 _− α_ ( _xt, c_ ))� _µ_<sup>+</sup> _t_<sup>(</sup><sup>_xt, c_)</sup><sup>_−µ−_</sup> _t_<sup>(</sup><sup>_xt, c_)</sup> � = (1 _− α_ ( _xt, c_ ))∆ _µ_<sup>_⋆_</sup> _t_<sup>(</sup><sup>_xt, c_)</sup><sup>_,_</sup> where ∆ _µ_<sup>_⋆_</sup> _t_<sup>(</sup><sup>_xt, c_) ≜</sup><sup>_µ_</sup> _t_<sup>+(</sup><sup>_xt, c_)</sup><sup>_−µ−_</sup> _t_<sup>(</sup><sup>_xt, c_) is the oracle mean gap.Substituting into Equation (29) yields</sup> 


15 

_π_ **-StepNFT: Wider Space Needs Finer Steps in Online RL for Flow-based VLAs** 

Finally, at the start of training (or for sufficiently small updates) where _vθ ≈ v_<sup>old</sup> so that _σ_ ( _zt_ ) _≈_ const, taking conditional expectation of the gradient form in Step 3 and using Equation (30) gives 


where scalar factors such as 2 _α_ (1 _− α_ ) do not affect alignment. do not affect alignment. This proves part (c). 

## **A.6. Proof of Theorem 4.5 (Comparison with wMSE)** 

A.6.1. DECOMPOSITION OF WMSE 

We substitute _Eθ_<sup>_±_=</sup><sup>_∥et ∓dt∥_2</sup> Σ<sup>_−_</sup> _t_<sup>1</sup> into the weighted-MSE objective _L_ wMSE = _rEθ_<sup>++ (1</sup><sup>_−r_)</sup><sup>_E_</sup> _θ_<sup>_−_.Expanding the terms</sup> immediately yields: 


Using _y_ = 2 _r −_ 1 (which implies 1 _−_ 2 _r_ = _−y_ ), we obtain: 


## A.6.2. RANKING CALIBRATION 

Define the ranking error event at a sampled step _t_ : 


_π_ -StepNFT minimizes softplus( _y_ ( _E_<sup>+</sup> _− E_<sup>_−_</sup> )), which is a convex upper bound on the indicator function **1** _Et_ , thus directly minimizing ranking errors. In contrast, wMSE minimizes a regression loss with the penalty _∥dt∥_<sup>2</sup> (from A.7.1), which restricts the branch separation required to satisfy the ranking condition _Et_ when the margin is small. 

A.6.3. BINARY CASE ANALYSIS 

When _r ∈{_ 0 _,_ 1 _}_ : 

- **wMSE:** If _r_ = 1, _L_ wMSE = _E_<sup>+</sup> . It pulls _µ_<sup>+</sup> to _xt−_ but provides no signal to _µ_<sup>_−_</sup> . 

- _π_ **-StepNFT:** Minimizes softplus( _E_<sup>+</sup> _− E_<sup>_−_</sup> ). It simultaneously pulls _µ_<sup>+</sup> to _xt−_ and pushes _µ_<sup>_−_</sup> away. This “push-pull” dynamic generates stronger gradients for discrimination. 

16 

_π_ **-StepNFT: Wider Space Needs Finer Steps in Online RL for Flow-based VLAs** 

# **B. Detailed Related Works** 

## **B.1. Online RL for VLAs** 

VLA models map multimodal inputs to actions via diverse representations: discretizing actions into tokens (RT series (Zitkovich et al., 2023), OpenVLA (Kim et al., 2024)), mapping to continuous regression features (OpenVLA-OFT (Kim et al., 2025b)), or outputting actions via generative denoising processes (Octo (Ghosh et al., 2024), GR00T (Bjorck et al., 2025), OpenPi (Black et al., 2026; 2025; Intelligence et al., 2025)). While pre-training establishes broad capabilities, the post-training focus is shifting from SFT to online RL to bridge the domain gap. Adapting RL depends on these representations, where discrete approaches (VLA-RL (Lu et al., 2025), RL4VLA (Liu et al., 2026)) leverage accessible token probabilities, while continuous mappings (SimpleVLA-RL (Li et al., 2025a)) treat outputs as Gaussian means. However, flow-based VLAs face the challenge of intractable likelihoods due to multi-step ODE sampling. Some methods bypass likelihood calculation entirely: GR-RL (Li et al., 2025b) distills value functions in the latent space, while _π_ 0<sup>_∗_</sup> _._ 6<sup>utilizes</sup> preference-based feedback. Conversely, _π_ RL (Chen et al., 2025) addresses this by transforming the deterministic ODE into an SDE or adding auxiliary noise networks. Crucially, this noise injection serves a dual purpose: it not only facilitates mathematical likelihood approximation but also significantly enhances exploration. This importance of noise-induced exploration is further echoed by test-time scaling strategies like TACO (Yang et al., 2025) and Hume (Song et al., 2025), as well as DSRL (Wagenmaker et al., 2025), which operates RL directly in the diffusion noise space. 

## **B.2. Policy Optimization for Generative Models** 

Integrating online RL into generative models typically follows three paradigms to handle intractable likelihoods. Explicit Gradient and Advantage Methods. Approaches like DDPO (Black et al., 2023) and DPOK (Fan et al., 2023) treat denoising as a sequential decision process. Flow-GRPO (Liu et al., 2025) and ReinFlow (Zhang et al., 2025b) further facilitate this by converting ODEs to SDEs or using Gaussian approximations to enable policy gradient updates. Reward-Weighted Likelihood-Free Methods. To avoid exact likelihood computation, methods such as RWFM (Pfrommer et al., 2025; Fan et al., 2025) and FPO (McAllister et al., 2025) construct proxy objectives or advantage-weighted ratios, effectively optimizing the flow model via regression targets derived from high-reward samples. However, these paradigms often suffer from high variance in gradient estimation or rely on complex reward proxies to stabilize training. Preference and Contrastive Methods. These approaches align distributions via ranking losses, bypassing explicit advantages. Diffusion-DPO (Wallace et al., 2024) aligns models based on trajectory outcomes, while LPO (Zhang et al., 2025a) ensures fine-grained consistency at the latent noise-step level. Uniquely, Diffusion-NFT (Zheng et al., 2026) proposes a solver-agnostic framework that constructs implicit positive and negative update directions directly within the forward process, offering a computationally efficient paradigm without requiring explicit likelihoods or value networks. 

17 

_π_ **-StepNFT: Wider Space Needs Finer Steps in Online RL for Flow-based VLAs** 

# **C. Experiment Details** 

## **C.1. Detailed Introduction of Benchmarks** 

We evaluate on 2 multitask benchmarks. 

- LIBERO (Liu et al., 2023): We follow the standard protocol across four suites (Spatial, Object, Goal, Long), reporting average success rates over 500 episodes (50 states _×_ 10 sub-tasks) per suite. The agent receives dual 224 _×_ 224 RGB inputs, language instructions, and 7-dimensional proprioceptive states (6-DoF joints + gripper). It outputs continuous end-effector actions. The environment provides a sparse binary reward (1 for success, 0 otherwise). 

- ManiSkill (Mu et al., 2021): We adopt the PutOnPlateInScene multitask setting from RL4VLA (Liu et al., 2026). This benchmark defines 4,352 compositional tasks derived from 16 objects, 17 receptacles, and 16 tabletop scenes. Observations consist of a single 480 _×_ 640 third-person view, language instructions, and joint poses. Actions are continuous joint-space commands. The environment provides a composite reward to discourage degenerate throwing behaviors. 

_Table 3._ OOD task mapping for ManiSkill PutOnPlateInScene25* across Vision, Semantics, and Execution categories. 

|**Category**|**Sub-category (OOD type)**|**ManiSkill env IDs**|
|---|---|---|
||Unseen Table (background)<br>Dynamic Textures (foreground, weak)|PutOnPlateInScene25VisionImage-v1<br>PutOnPlateInScene25VisionTexture03-v1|
|**Vision**|Dynamic Textures (foreground, strong)<br>Dynamic Noise (image-level, weak)<br>Dynamic Noise (image-level, strong)|PutOnPlateInScene25VisionTexture05-v1<br>PutOnPlateInScene25VisionWhole03-v1<br>PutOnPlateInScene25VisionWhole05-v1|
||Unseen Objects<br>Unseen Receptacles|PutOnPlateInScene25Carrot-v1<br>PutOnPlateInScene25Plate-v1|
|**Semantics**|Unseen Instruction Phrasings|PutOnPlateInScene25Instruct-v1|
||Multi-Object|PutOnPlateInScene25MultiCarrot-v1|
||Distractive Receptacle|PutOnPlateInScene25MultiPlate-v1|
||Unseen Position|PutOnPlateInScene25Position-v1|
|**Execution**|Unseen Robot Init Pose|PutOnPlateInScene25EEPose-v1|
||Mid-Episode Object Reposition|PutOnPlateInScene25PositionChangeTo-v1|


## **C.2. Hyperparameters for Training** 

_Table 4._ Hyperparameter settings for Libero and ManiSkill. 

|||||**LIB**|**ERO**||||**Man**|**iSkill**|
|---|---|---|---|---|---|---|---|---|---|---|
|**Parameters**||_π_0||||_π_0_._5|||_π_0|_π_0_._5|
||**Spatial**|**Object**|**Goal**|**Long**|**Spatial**|**Object**|**Goal**|**Long**|**Multitask**|**Multitask**|
|Train epochs|400|400|400|400|400|400|400|400|240|240|
|Batch size|2048|2048|2048|2048|2048|2048|2048|2048|5120|5120|
|Update epochs|2|2|4|4|1|1|3|4|5|5|
|Actor lr|1e-5|1e-5|1e-5|1e-5|1e-5|1e-5|1e-5|1e-5|8e-6|8e-6|
|Interaction steps|240|240|320|480|240|240|320|480|60|60|
|Parallel environments|64|64|64|64|64|64|64|64|64|64|
|Rollout epochs|8|8|8|8|8|8|8|8|–|–|
|Action chunk_H_|5|5|5|10|5|5|5|10|5|5|
|Denoise steps|4|4|4|4|4|4|4|4|4|4|
|Noise level_σ_|0.2|0.2|0.2|0.2|0.2|0.2|0.2|0.2|0.2|0.2|
|Trust Region Size_β_|1.0|1.0|1.0|1.0|1.0|1.0|1.0|1.0|1.0|1.0|
|Initial Decay_α_0|0.1|0.1|0.1|0.1|0.1|0.1|0.1|0.1|0.1|0.1|
|End Decay_α−_1|0.995|0.995|0.995|0.995|0.995|0.995|0.995|0.995|0.995|0.995|


18 

_π_ **-StepNFT: Wider Space Needs Finer Steps in Online RL for Flow-based VLAs** 

# **D. Additional Ablation: Step Selection Strategy** 

**Motivation.** Our step-wise supervision is defined on a single solver transition ( _xt → xt−_ ) sampled from a _K_ -step Flow-SDE rollout. In our default implementation, we uniformly sample the solver step index _j ∼U{_ 0 _, . . . , K −_ 1 _}_ at each training iteration and construct ( _xt, xt− , t_ ) = ( _xtj , xtj_ +1 _, tj_ ). This stochastic step selection exposes the model to transitions at different noise levels and denoising stages, providing more balanced supervision across the entire solver trajectory. 

**Ablation setup.** We compare the default **Random Step** strategy against several **Fixed Step** variants, where the solver index _j_ is held constant throughout training. All other configurations (solver, objective, training budget, and environment settings) remain identical. 

**Results.** As shown in Figure 5, uniformly random step selection achieves more stable optimization and improves the final success rate compared to fixed-step choices. We hypothesize that fixed-step supervision biases learning toward a narrow noise regime, while random step selection provides coverage over multiple denoising stages and thus yields more robust policy learning. 


_Figure 5._ **Step selection ablation.** Performance comparison between uniform random solver-step sampling and fixed-step selection strategies. 

19 

