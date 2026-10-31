---
title: "$π_\\texttt{RL}$: Online RL Fine-tuning for Flow-based Vision-Language-Action Models"
date: "2025-10-29"
authors: "Kang Chen; Zhihao Liu; Tonghe Zhang; Zhen Guo; Si Xu; Hao Lin"
url: https://arxiv.org/abs/2510.25889
pdf: https://arxiv.org/pdf/2510.25889
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2510.25889)** / [論文ページ](https://arxiv.org/abs/2510.25889)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

_π_ **RL: Online RL Fine-tuning for Flow-based Vision-Language-Action Models** 

**Kang Chen**<sup>2</sup><sup>_,_6</sup><sup>_,∗_</sup> **Zhihao Liu**<sup>3</sup><sup>_,_6</sup><sup>_,∗_</sup> **Tonghe Zhang**<sup>4</sup><sup>_,∗,♯_</sup> **Zhen Guo**<sup>5</sup> **Si Xu**<sup>5</sup> **Hao Lin**<sup>5</sup> **Hongzhi Zang**<sup>1</sup> **Xiang Li**<sup>5</sup> **Bingwen Wei**<sup>1</sup> **Jiakai Zhou**<sup>1</sup> **Quanlu Zhang**<sup>5</sup> **Zhaofei Yu**<sup>2</sup> **Guoliang Fan**<sup>3</sup> **Tiejun Huang**<sup>2</sup> **Yu Wang**<sup>1</sup><sup>_†_</sup> **Chao Yu**<sup>1</sup><sup>_†_</sup> 


https://github.com/RLinf/RLinf https://huggingface.co/RLinf 


_Figure 1. π_ RL: An online RL framework for flow-based VLAs. Incorporating two solutions, Flow-Noise and Flow-SDE, _π_ RL enhances the performance and generalization of SFT-aligned models across extensive ID benchmarks and OOD settings. Refined with RL, few-shot SFT policies achieve performance comparable to full dataset baselines. Additionally, we facilitate seamless zero-shot sim-to-real transfer by constructing a simulator with 3D Gaussian Splatting as the rendering engine to narrow the visual domain gap. 

# **Abstract** 

Vision-Language-Action (VLA) models enable robots to understand and perform complex tasks from multimodal input. Although recent work explores using reinforcement learning (RL) to automate the laborious data collection process in scaling supervised fine-tuning (SFT), applying RL to large-scale flow-based VLAs ( _e_ . _g_ ., _π_ 0, 

> 1Tsinghua University 2Peking University 3Institute of Automation, Chinese Academy of Sciences<sup>4</sup> Carnegie Mellon University<sup>5</sup> Infinigence AI<sup>6</sup> Zhongguancun Academy _♯_ Work done at Tsinghua University _∗_ Equal Contributions . Correspondence to: Yu Wang <yu-wang@tsinghua.edu.cn>, Chao Yu <zoeyuchao@gmail.com>. 

_π_ 0 _._ 5) remains challenging due to intractable action log-likelihoods raised from flow matching. We address this challenge with _π_ RL, featuring two technical approaches: (1) **Flow-Noise** models the denoising process as a discrete-time MDP with a learnable noise network for exact log-likelihood computation. (2) **Flow-SDE** integrates denoising with agent-environment interaction, formulating a two-layer MDP that employs ODE-to-SDE conversion for efficient RL exploration. We evaluate _π_ RL across various benchmarks, with experiments demonstrating that RL yields significant performance improvements in both in-distribution and out-of-distribution settings. 

_Preprint. January 30, 2026._ 

1 

_π_ **RL: Online RL Fine-tuning for Flow-based Vision-Language-Action Models** 

# **1. Introduction** 

Vision-Language-Action (VLA) models (Din et al., 2025) have emerged as a leading solution for general-purpose robots, effectively bridging the gap between high-level multimodal reasoning and low-level physical control (Firoozi et al., 2025). Conditioned on sensor inputs and language commands, VLAs (Team et al., 2024; Kim et al., 2024; Black et al., 2024; Intelligence et al., 2025) can translate abstract instructions into executable robotic actions, thereby enabling intuitive and flexible human-robot interaction. 

The training methodology for VLAs follows the standard pre-training and supervised fine-tuning (SFT) paradigm as shown in Fig. 1. Building on the pretrained VisionLanguage Model (VLM) (Touvron et al., 2023; Beyer et al., 2024), VLAs are fine-tuned on large-scale, heterogeneous human demonstration datasets (O’Neill et al., 2024; Khazatsky et al., 2024), followed by SFT on the target task to align their capabilities with the specific embodiment and environment. However, reliance on SFT introduces a critical challenge: curating large-scale, high-quality expert trajectories is both laborious and costly (Din et al., 2025). Besides, models obtained via SFT tend to overfit to expert demonstrations (Fei et al., 2025), with their performance fundamentally constrained by the quality of expert demonstrations. 

Recent efforts (Zang et al., 2025; Li et al., 2025a; Tan et al., 2025; Liu et al., 2025a) have explored expanding the VLA training process with reinforcement learning (RL), establishing a pre-training, SFT, and RL paradigm as shown in Fig. 1, allowing VLAs to improve their performance beyond expert demonstrations through environmental interaction and develop more generalizable policies. 

However, these RL advances have been largely confined to autoregressive VLAs, featuring OpenVLA (Kim et al., 2024) and OpenVLA-OFT (Kim et al., 2025), which employ discrete action decoders that generate output in an autoregressive or parallel fashion. This stands in stark contrast to flow-based VLAs, exemplified by the _π_ series models, which generate actions through iterative refinement in flow matching (Lipman et al., 2022), offering the advantages of generating action chunks in high-frequency and performing highly dexterous tasks (Black et al., 2024). Consequently, previous VLA-RL algorithms are incompatible with flowbased VLAs, and the fundamental challenge lies in how to characterize a logarithmic likelihood (Hutchinson, 1989; Chen et al., 2018) for the executed actions. 

In this paper, we introduce _π_ RL, a framework designed for fine-tuning flow-based VLAs with online RL algorithms. To address the intractable log-likelihood estimation problem in flow matching, we propose two solutions. **Flow-Noise** integrates a learnable noise network into the denoising process and models this stage as a discrete-time Markov decision 

process (MDP) for exact log-likelihood estimation. **FlowSDE** converts the ordinary differential equation (ODE) denoising process into a stochastic differential equation (SDE) while maintaining equivalent marginal distributions for exploration, and builds a two-layer MDP that couples the denoising process with policy-environment interaction. Given the formulated MDP and the exact log-likelihood computation, _π_ RL undergoes further optimization via the proximal policy optimization (PPO) (Schulman et al., 2017). 

We conduct extensive experiments on various benchmarks to evaluate the effectiveness of _π_ RL on _π_ 0 (Black et al., 2024) and _π_ 0 _._ 5 (Intelligence et al., 2025) models. Across all benchmarks, the proposed framework consistently yields substantial performance gains over SFT baselines. Furthermore, out of distribution evaluations confirm that our model yields genuine policy enhancement rather than narrow overfitting on the target environment. 

To sum up, our contributions are: 

- **RL for flow-based VLAs.** We introduce _π_ RL, an online RL fine-tuning framework with Flow-Noise and FlowSDE formulations for flow-based VLAs. 

- **Superior Performance.** We demonstrate significant performance improvements and enhanced generalization of _π_ RL across various benchmarks. 

- **Comprehensive Ablation.** We conduct thorough ablation studies, offering empirical insights to guide future RL research on flow-based VLAs. 

- **Open-source Code and Models.** We release all codes to ensure reproducibility, hoping that our study helps to advance further research in this field. 

# **2. Related Work** 

## **2.1. Vision-Language-Action Models** 

VLA models have recently achieved remarkable progress in robotics by integrating multimodal inputs to enable unified perception, reasoning, and control. This development has led to a series of architectures, including Octo (Team et al., 2024), RT (Brohan et al., 2022), OpenVLA, OpenVLA-OFT, _π_ 0, _π_ 0 _._ 5, and GR00T (Bjorck et al., 2025). 

## **2.2. Online RL Fine-tuning for VLA Models** 

Recent research has increasingly focused on enhancing the performance and generalization of VLAs with online RL. For example, SimpleVLA-RL (Li et al., 2025a), building on the OpenVLA-OFT and GRPO, demonstrated that RL can improve long-horizon planning of VLA models under data scarcity. RL4VLA (Liu et al., 2025a) empirically evaluated PPO, GRPO, and direct preference optimization 

2 

_π_ **RL: Online RL Fine-tuning for Flow-based Vision-Language-Action Models** 

(DPO) (Rafailov et al., 2023) with stage-based sparse rewards. RLinf-VLA (Yu et al., 2025; Zang et al., 2025) provides a unified and efficient framework for scalable RL training of VLA models. These works demonstrate the effectiveness of RL fine-tuning VLA models. 

## **2.3. RL Fine-tuning for Flow Models** 

Integrating RL with flow models is a promising way to transcend the limitations of imitation learning. To this end, Flow-GRPO (Liu et al., 2025b) converts the deterministic ODE into an equivalent SDE to enable stochasticity exploration, a foundation upon which subsequent works like MixGRPO (Li et al., 2025b) and TempFlow-GRPO (He et al., 2025) further accelerate training through hybrid ODE-SDE rollouts. ReinFlow (Zhang et al., 2025) injects learnable noise into the flow path and transforms it into a discretetime Markov process with a tractable likelihood for stable policy gradient updates. Flow policy optimization (FPO) (McAllister et al., 2025) reframes policy optimization as maximizing the advantage-weighted ratio of the conditional flow matching loss. 

# **3. Preliminary** 

robot proprioception to a sequence of _H_ future actions **A** _t_ = [ _at,_ 0 _, ..., at,H−_ 1], formulated as _p_ ( **A** _t|_ **o** _t_ ). Within the model, the VLM extracts features from the visual and language inputs, while the flow matching expert is tasked with generating the actions. Specifically, the model learns a conditional vector field **v** _θ_ that transforms a standard Gaussian noise distribution into the target action **A** _t_ . This is achieved by minimizing the Conditional Flow Matching (CFM) loss, which aligns the predicted vector field **v** _θ_ with the ground-truth vector field **u** : 


Here, the conditional probability path _q_ ( **A**<sup>_τ_</sup> _t_<sup>_|_</sup><sup>**A**</sup><sup>_t_) generates</sup> a noisy action<sup>1</sup> **A**<sup>_τ_</sup> _t_<sup>=</sup><sup>_τ_</sup><sup>**A**</sup><sup>_t_+ (1</sup><sup>_−τ_)</sup><sup>_ϵ_from an action</sup><sup>**A**</sup><sup>_t_,</sup> random noise _ϵ ∼N_ (0 _, I_ ), and a continuous time _τ ∈_ [0 _,_ 1] in flow matching. For this specific path, the corresponding ground-truth vector field is defined as **u** ( **A**<sup>_τ_</sup> _t_<sup>_|_</sup><sup>**A**</sup><sup>_t_) =</sup><sup>**A**</sup><sup>_t−ϵ_.</sup> During the inference, the action sequence is generated by first sampling a noise vector **A**<sup>0</sup> _t_<sup>_∼N_(0</sup><sup>_, I_), which is further</sup> iteratively refined by integrating the learned vector field **v** _θ_ over a fixed number of steps based on the forward Euler method: **A**<sup>_τ_</sup> _t_<sup>+</sup><sup>_δ_</sup> = **A**<sup>_τ_</sup> _t_<sup>+</sup><sup>**v**</sup><sup>_θ_(</sup><sup>**A**</sup><sup>_τ_</sup> _t_<sup>_,_</sup><sup>**o**</sup><sup>_t_)</sup><sup>_· δ_.</sup> 

## **3.1. Problem Formulation** 

We formulate the task as an MDP, defined by a tuple _M_ = ( _S, A, P_ 0 _, P_ ENV _, R_ ENV _, γ_ ). The state _st ∈S_ is defined as the robot observation **o** _t_ and _P_ 0 denotes the initial state distribution. Given the state, the flow policy predicts an action _at ∼ π_ ( _·|st_ ) _∈A_ , resulting in the state transition _st_ +1 _∼ P_ ENV( _·|st, at_ ) and a reward _R_ ENV( _st, at_ ). The objective is to learn a policy _πθ_ that maximizes the expected _γ_ -discounted return over a horizon of _T_ + 1: 


With the policy gradient surrogate (Williams, 1992), the gradient of the return expectation can be approximated from sampled trajectories: 


The advantage function, _A_ ( _st, at_ ) = _Q_ ( _st, at_ ) _− V_ ( _st_ ), measures the relative merit of the action value _Q_ ( _st, at_ ) over the state value _V_ ( _st_ ), providing a low-variance signal for the policy update. 

## **3.2. Flow-based Vision-Language-Action Model** 

A flow-based VLA model _πθ_ is designed to map the observation **o** _t_ comprising RGB images, language tokens, and 

# **4. Methodology** 

Existing VLA-RL approaches leverage base models such as OpenVLA for discrete actions and OpenVLA-OFT for continuous actions. To compute the action log-likelihood log _πθ_ ( _at|st_ ), discrete models (Liu et al., 2025a) apply softmax to the output logits, while continuous models (Li et al., 2025a) treat the action as a Gaussian distribution, employing a prediction head to estimate the variance. As for the flow-based VLAs, directly computing the exact likelihood (Hutchinson, 1989) is inaccurate with few denoising steps. Moreover, the deterministic nature of its ODE sampling process precludes exploration, making its implementation within RL non-trivial. To this end, we propose Flow-Noise and Flow-SDE, two technical approaches that make flowbased VLAs amenable to RL. 

## **4.1. Flow-Noise** 

Inspired by Reinflow (Zhang et al., 2025), we incorporate a learnable noise network into the flow matching denoising process and solve the problem within the standard one-layer MDP framework detailed in Sec. 3.1. By modeling the denoising stage as a discrete MDP, we can directly compute the log-likelihood of the denoised sequence, enabling equivalent policy optimization via RL. 

> 1 **A** _τt_<sup>incorporates two temporal indices,</sup><sup>_t_denotes the discrete</sup> time step for environment interaction and _τ_ represents the continuous time variable in flow matching. 

3 

_π_ **RL: Online RL Fine-tuning for Flow-based Vision-Language-Action Models** 


_Figure 2._ Illustration for the noise injection in _π_ RL. 


## 4.1.1. STOCHASTICITY INJECTION 

_Figure 3._ Illustration of the MDP formulations in _π_ RL. 

In Flow-Noise, we parameterize the noise schedule with a neural network, allowing the magnitude of the injected noise to be learned dynamically during training for greater flexibility, as shown in Fig. 2. We focus on the generation process within a single environment timestep _t_ . For notational simplicity, we omit the time subscript _t_ , _e_ . _g_ ., writing **A**<sup>_τ_</sup> , and denote the predicted velocity **v** _θ_ ( **A**<sup>_τ_</sup> _,_ **o** ) as **v**<sup>_τ_</sup> . 

The step transition during the denoising process is modeled as a Gaussian distribution _p_ ( **A**<sup>_τ_+</sup><sup>_δ_</sup> _|_ **A**<sup>_τ_</sup> ) _∼N_ ( _µτ ,_ Σ _τ_ ), where the mean is determined by the forward Euler update of the original ODE and the variance is controlled by the learnable noise network _θ_<sup>_′_</sup> : 

entire denoising sequence _A_ = ( **A**<sup>0</sup> _, . . . ,_ **A**<sup>1</sup> ) is depicted in Fig. 3 and formulated as: 


Building on this, we can treat flow-based policy optimization within a standard MDP framework. 

## **4.2. Flow-SDE** 


Here, _σθ′_ ( _·_ ) is the standard deviation learned from the noise injection network, conditioned on the action **A**<sup>_τ_</sup> , and the observation **o** . The noise network is trained jointly with the velocity but discarded after fine-tuning, leaving a deterministic policy for inference. 

Inspired by Flow-GRPO (Liu et al., 2025b), we enhance stochastic exploration by converting the denoising process from ODE into an SDE formulation. We further construct a two-layer MDP to couple the denoising process with the policy-environment interaction following DPPO (Ren et al., 2024), while leveraging the hybrid ODE-SDE sampling technique to accelerate the training process. 

## 4.2.1. STOCHASTICITY INJECTION 

## 4.1.2. LOG-LIKELIHOOD ESTIMATION 

The primary challenge in applying policy gradient methods to flow-based VLAs stems from the intractable loglikelihood of the final executed action. In Flow-Noise, we address it by substituting the gradient of the joint loglikelihood of the entire denoising process into the policy optimization objective in Eq. (2), which is theoretically grounded in Reinflow (Zhang et al., 2025). 

The inference process for action generation is discretized into _K_ uniform steps, which defines a sequence of time points _{τ_ 0 _, τ_ 1 _, . . . , τK}_ . With the step interval defined as _δ_ = 1 _/K_ , the discrete timestep at the _k_ -th point is _τk_ = _k ·δ_ , starting from _τ_ 0 = 0 and culminating at _τK_ = 1. Given the observation **o** , the exact and tractable log probability for the 

In Flow-SDE, we convert the deterministic ODE into an equivalent SDE that preserves the marginal probability density of the generated actions, as shown in Fig. 2. 

The deterministic ODE sampling trajectory of the flow matching, especially the Rectified Flow (Liu et al., 2022), is described by the forward Euler method: 


Building on the connection between the _probability flow_ ODE and SDE (Song et al., 2020), we can transform the deterministic ODE in Eq. (6) into an equivalent SDE, with a drift term that corrects the original velocity and a diffusion 

4 

_π_ **RL: Online RL Fine-tuning for Flow-based Vision-Language-Action Models** 

term that introduces noise: 


where _g_ ( _τ_ ) is a scalar function controlling the noise schedule, _∇_ log _qτ_ ( **A**<sup>_τ_</sup> ) is the score function of the marginal distribution _qτ_ and _d_ **w** denotes a Wiener process. 

As established in Flow-GRPO, the score function and the velocity field are critically linked by _∇_ log _qτ_ ( **A**<sup>_τ_</sup> ) = _−_<sup>**<u>A</u>**</sup><sup>_τ_</sup> _−_<sup><u>1</u></sup><sup>_−τ_</sup> _τ τ_<sup>**v**</sup><sup>_τ_.Bysubstitutingthescorefunctionwith</sup> the velocity field in Eq. (7) and setting the noise schedule _g_ ( _τ_ ) to _στ_ = _a_ 1 _−τ τ_<sup>with</sup><sup>_a_controllingthenoiselevel,</sup> ~~�~~ we derive the final SDE formulation for the flow-matching sampler: 


Discretizing this SDE reveals that the transition probability _p_ ( **A**<sup>_τ_+</sup><sup>_δ_</sup> _|_ **A**<sup>_τ_</sup> ) _∼N_ ( _µτ ,_ Σ _τ_ ) is an isotropic Gaussian distribution, with the mean and variance formulated as: 


## 4.2.2. MDP FORMULATION 

We couple the denoising process of the flow matching with environmental interaction in Flow-SDE. Specifically, we embed the inner MDP defined during the denoising process into the high-level, outer-loop MDP with the environment _M_ ENV in Sec. 3.1, formulating a two-layer MDP as shown in Fig. 3, with components defined with respect to the environment time _t_ and denoising time _τ_ . 

- **State** ¯ _s_<sup>_τ_</sup> _t_<sup>= (</sup><sup>**o**</sup><sup>_t,_</sup><sup>**A**</sup><sup>_τ_</sup> _t_<sup>) is the tuple of the observation</sup><sup>**o**</sup><sup>_t_</sup> and the action state **A**<sup>_τ_</sup> _t_<sup>.</sup> 

- **Action** _a_ ¯<sup>_τ_</sup> _t_<sup>isdefinedasthenextsampleddenoised</sup> action in the inner-loop and the executed action for the outer loop: 


where **A**<sup>_τ_</sup> _t_<sup>+</sup><sup>_δ_</sup> = _µτ_ + _στ_ _~~√~~ δ ·_ **_ϵ_** , **_ϵ_** _∼N_ (0 _,_ **I** ) is the randomly sampled noise. 

- **Transition** _P_<sup>¯</sup> (¯ _s_<sup>_τ_</sup> _t_<sup>_′ ′ |s_¯</sup> _t_<sup>_τ,_¯</sup><sup>_aτ_</sup> _t_<sup>) defines how the state evolves,</sup> formulated as: 


For _τ <_ 1, the inner loop transition _P_ FLOW( _·_ ) occurs between different denoised action states, where the observation **o** _t_ remains fixed and the next action state is set by ¯ _a_<sup>_τ_</sup> _t_<sup>=</sup><sup>**A**</sup> _t_<sup>_τ_+</sup><sup>_δ_</sup> . 

For _τ_ = 1, the final action ¯ _a_<sup>_τ_</sup> _t_<sup>=</sup><sup>**A**</sup> _t_<sup>1interacts with the</sup> outer-loop environment, resulting in a new observation **o** _t_ +1 according to the environment dynamics _P_ ENV( _·_ ). Concurrently, the action state is reset from a standard normal distribution **A**<sup>0</sup> _t_ +1<sup>_∼N_(0</sup><sup>_, I_).</sup> 

- **Reward** _R_<sup>¯</sup> (¯ _s_<sup>_τ_</sup> _t_<sup>_,_¯</sup><sup>_aτ_</sup> _t_<sup>) is granted only upon completion of</sup> the denoising process and interaction with the environment: 


Within the two-layer MDP framework, the problem of estimating the action log-likelihood log _π_ ( _at|st_ ) is transformed into estimating log _π_ (¯ _a_<sup>_τ_</sup> _t_<sup>_|s_¯</sup><sup>_τ_</sup> _t_<sup>),whichisstraightforwardto</sup> compute due to the Gaussian nature of the transitions. 

## 4.2.3. HYBRID ODE-SDE SAMPLING 

The two-layer MDP formulation significantly extends the horizon, increasing training difficulty and computational cost. To mitigate this, we adopt a mixed ODE-SDE rollout strategy (Li et al., 2025b; He et al., 2025). At each step _t_ , we randomly sample a denoising time _τt_ for the stochastic SDE exploration, while treating all remaining denoising steps as deterministic ODE updates. Specifically, the policy acts on the state ¯ _s_<sup>_τ_</sup> _t_<sup>_t_= (</sup><sup>**o**</sup><sup>_t,_</sup><sup>**A**</sup><sup>_τ_</sup> _t_<sup>_t_); subsequently, an environ-</sup> ment wrapper executes the remaining ODE steps and the environment transition, ultimately yielding the next state _s_ ¯<sup>_τ_</sup> _t_ +1<sup>_t_+1= (</sup><sup>**o**</sup><sup>_t_+1</sup><sup>_,_</sup><sup>**A**</sup><sup>_τ_</sup> _t_ +1<sup>_t_+1) at a newly sampled time</sup><sup>_τt_+1.This</sup> formulation effectively shortens the MDP horizon while maintaining theoretical consistency with the original twolayer framework. 

## **4.3. Policy Optimization** 

## 4.3.1. ALGORITHM 

Given the formulated flow policy MDP, our objective is to learn the optimal parameters _θ_<sup>_∗_</sup> for the policy _πθ_ that maximizes the expected discounted return _J_ ( _πθ_ ). To this end, we apply the widely adopted policy gradient algorithm PPO to optimize the policy. 

_π_ -series models (Black et al., 2024; Intelligence et al., 2025) adopt a chunk-based approach for action generation. Specifically, the policy outputs an entire sequence of _H_ future actions **A** _t_ = [ _at,_ 0 _, ..., at,H−_ 1] in response to each observation. In this approach, we treat the entire sequence as a single macro-step and define its corresponding reward _Rt_ =<sup>�</sup><sup>_H_</sup> _j_ =0<sup>_−_1</sup><sup>_rt,j_asthesumoftheper-steprewards</sup><sup>_rt,j_,</sup> 

5 

_π_ **RL: Online RL Fine-tuning for Flow-based Vision-Language-Action Models** 


_Figure 4._ Illustration of the two critic placement configurations. 

referred to as the chunk-level formulation in RLinf-VLA (Zang et al., 2025). 

To effectively guide policy updates, PPO employs Generalized Advantage Estimation (GAE) (Schulman et al., 2015) to compute a low-variance estimate of the advantage, estimated as: 


where the TD-error is _Tt_ = _Rt_ + _γV_ ( _st_ +1) _− V_ ( _st_ ). Here, _V_ ( _·_ ) is the state-value function derived from the critic network, _γ_ is the discount factor, and _λ_ is the parameter that balances the trade-off between bias and variance in the advantage estimate. 

PPO constrains policy updates to a small trust region to prevent large, destabilizing updates, with the objective function: 


where the clip function, governed by a hyperparameter _ϵ_ , restricts the ratio _ρt_ ( _θ_ ) to the interval [1 _− ϵ,_ 1+ _ϵ_ ] to ensure training stability. 

Here, the probability ratio _ρt_ ( _θ_ ) between the updated and old policies takes the form of either: 


## 4.3.2. CRITIC DESIGN 

Following VLA-PPO works (Zang et al., 2025; Liu et al., 2025a), we employ a shared actor-critic architecture for memory-efficient value prediction as shown in Fig. 4. However, the two flow-based VLAs process the proprioceptive state differently: in _π_ 0, the state is fed into the action expert model, whereas in _π_ 0 _._ 5, it is merged with prompt embeddings within the VLM. 

To this end, for the _π_ 0 _._ 5 variant, we attach the critic network directly to the VLM output, providing the value estimate 

_V_ vlm( **o** _t_ ) conditioned on the integrated image, language, and state inputs. Conversely, for the _π_ 0 variant, achieving the value prediction is non-trivial due to the coupled input structure, where the action expert requires both the noisy action **A**<sup>_τ_</sup> _t_<sup>and the state.To this end,we approximate</sup><sup>_V_expert(</sup><sup>**o**</sup><sup>_t_)</sup> by averaging the value estimates across the entire denoising trajectory, formulated as: 


# **5. Experimental Results** 

## **5.1. Setup** 

**Benchmarks.** We perform experiments on four widelyadopted robot manipulation benchmarks: **LIBERO** (Liu et al., 2023), **ManiSkill** (Tao et al., 2024), **MetaWorld** (McLean et al., 2025) and **CALVIN** (Mees et al., 2022). 

**Flow-based VLAs.** We conduct our primary experiments based on _π_ 0 and _π_ 0 _._ 5 models. Additionally, we conduct experiments on GR00T in Appendix Sec. H, which validates that our algorithm can be applied to other flow-based VLAs. 

## **5.2. Main Results** 

In this section, we assess the in-distribution (ID) performance of _π_ RL across various benchmarks, followed by an analysis of its out-of-distribution (OOD) generalization. 

## 5.2.1. IN-DISTRIBUTION RL TRAINING 

As detailed in Tab. 1, _π_ RL yields substantial performance gains over SFT baselines across all evaluated benchmarks. Specifically, the _π_ 0 model achieves a maximum average improvement of +29.2%, while the _π_ 0 _._ 5 variant demonstrates a +31.0% increase in average success rate. 

Specifically for LIBERO, we perform few-shot SFT on the _π_ 0 _._ 5 model followed by RL optimization to achieve a 98.3% success rate, outperforming the 96.9% success rate of the full-dataset SFT baseline. These performance gains extend to other challenging environments, including ManiSkill with 

6 

_π_ **RL: Online RL Fine-tuning for Flow-based Vision-Language-Action Models** 

_Table 1._ Comprehensive ID performance comparison across four benchmarks. 

|**Model**||||**Benchmark**|**s**|||
|---|---|---|---|---|---|---|---|
|||**LIBERO**|**ManiSkill**|**MetaWorld**|**CALVIN**|**Avg.**|∆**Avg.**|
||SFT|57.6|38.4|50.8|57.5|51.1|—|
|_π_0|Flow-SDE|96.1|**78.8**|78.1|**61.7**|78.7|+27.6|
||Flow-Noise|**97.6**|77.8|**85.8**|59.9|**80.3**|+**29.2**|
||SFT|77.1|40.1|43.8|61.3|55.6|—|
|_π_0_._5|Flow-SDE|97.9|**90.9**|**70.7**|**87.0**|**86.6**|+**31.0**|
||Flow-Noise|**98.3**|89.7|66.1|84.5|84.7|+29.1|


_Figure 5._ Comprehensive OOD evaluation results on CALVIN ABC-D, ManiSkill OOD, and MetaWorld ML45 benchmarks. 

its 4,352 pick-and-place task combinations, MetaWorld featuring 50 distinct manipulation primitives, and CALVIN for long-horizon sequential tasks. See Appendix Sec. C for comprehensive experimental details. 

## 5.2.2. OUT-OF-DISTRIBUTION RL EVALUATION 

While previous experiments demonstrate that RL yields performance improvements, a critical question remains: _does RL yield an enhanced policy, or simply overfit to the ID environment driven by provided rewards?_ In this section, we evaluate RL-finetuned policies in OOD scenarios, where the environment distribution or the task objective deviates from the ID training setup, to assess their generalization capabilities. 

As illustrated in Fig. 5, the performance gains achieved in the ID setting effectively transfer to OOD scenarios in ManiSkill and CALVIN, where the domain shift primarily stems from environmental variations. Conversely, for the OOD setting in MetaWorld, which involves distinct manipulation tasks, performance fluctuates without showing significant improvement. This finding suggests that the benefits of RL are primarily localized to action-level refinement rather than broader augmentation of cross-task generalization capabilities. See Appendix Sec. D for more details. 

## **5.3. Ablation Study** 

Given that Flow-SDE achieves performance comparable to Flow-Noise while offering higher computational efficiency, we conduct our ablation studies with the Flow-SDE method. Specifically, we investigate the impact of critic designs, noise injection strategies, and MDP formulations, with additional results on RL algorithms and hyper-parameters provided in Appendix Sec. F. 

## 5.3.1. CRITIC DESIGN 

**Placement.** We compare two critic placement strategies, one positioned after the action expert ( _V_ expert) and the other after the VLM ( _V_ vlm), with _π_ 0 model on the LIBERO-Long task suite. As illustrated in Fig. 6, we observe that _V_ vlm exhibits slightly superior performance, lower value loss, and higher explained variance, despite not receiving the proprioceptive state as input. This advantage can be attributed to a key difference in their input: _V_ vlm learns a direct mapping from observation to value, while _V_ expert must contend with optimization challenges arising from coupled state and noisy action inputs. 

Nevertheless, to align with the concept of the value function, we maintain the _V_ expert architecture for the _π_ 0, ensuring that state information is incorporated to estimate the value. 

7 

_π_ **RL: Online RL Fine-tuning for Flow-based Vision-Language-Action Models** 


_Figure 6._ Ablation on the critic design within Flow-SDE _π_ 0 on the LIBERO-Long, indicating that the critic _V_ vlm attached after the VLM exhibits superior performance. Furthermore, a four-layer MLP demonstrates stronger regression capability in _V_ expert.. 

_Figure 7._ Ablation on the MDP formulation within Flow-SDE of _π_ 0 on the LIBERO-Goal. 


_Figure 8._ Ablation on the injection strategy within Flow-SDE of _π_ 0 on the LIBERO-Long. 

**Structure.** We investigate a four-layer MLP versus a onelayer MLP, which mirrors the action-projection structure in the action expert. Results in Fig. 6 indicate that the fourlayer MLP leads to a more accurate value approximation, resulting in enhanced performance and training stability. 

## 5.3.2. FLOW POLICY MDP 

With the same fixed noise injection strategy, we evaluate the one-layer MDP of Flow-Noise with the two-layer MDP of Flow-SDE on the LIBERO-Goal, as shown in Fig. 7. 

We observe that the one-layer formulation converges most rapidly, but the final success rates remain consistent across all three formulations. In terms of computational efficiency, the hybrid two-layer paradigm achieves a 2 _×_ speedup over the standard approach due to its shorter effective MDP chain. Notably, the one-layer MDP yields no substantial wall-clock 

time advantage over the standard two-layer model, stemming from the requirement to recalculate full denoising trajectories for log likelihood estimation. 

## 5.3.3. STOCHASTICITY INJECTION 

We compare fixed and learnable noise injection strategies using the Flow-SDE MDP formulation on the LIBEROLong suite. To ensure a controlled comparison, we set the entropy bonus for the learnable noise to zero, aligning it with the fixed noise approach. 

Specifically, we set the fixed noise to 0.5, and lower and upper bounds for the learnable noise log-variance to 0.08 and 0.16. As depicted in Fig. 8, two noise strategies exhibit similar train performance at step 0, which indicates comparable noise magnitudes. Furthermore, the converged performance affirms the efficiency of both injection methods. 

8 

_π_ **RL: Online RL Fine-tuning for Flow-based Vision-Language-Action Models** 

_Table 2._ Ablation study of hyperparameters for Flow-SDE on the LIBERO-Spatial. _Train_ refers to policy performance during the stochastic rollout phase, whereas _Eval_ refers to performance during the deterministic evaluation phase. 

|||**Hyperparameters**|||||
|---|---|---|---|---|---|---|
|**Mod**|**els**<br>**Stage**<br>**Noise Lev**|**el**<br>**Denoise Step**||**A**|**ction Chu**|**nk**|
||0.2<br>0.5|0.8<br>1<br>2<br>4|8|5|10|20|
|SF|T<br>Train<br>62.3<br>56.0<br>Eval<br>65.2<br>65.2|46.6<br>9.4<br>28.3<br>56.1<br>65.2<br>63.8<br>64.9<br>65.2|62.6<br>63.2|56.0<br>65.2|60.7<br>70.5|70.3<br>72.6|
|RL|Train<br>59.5<br>93.5<br>Eval<br>73.1<br>94.5|95.3<br>73.8<br>90.8<br>93.5<br>98.1<br>88.5<br>97.0<br>94.5|84.3<br>86.7|93.5<br>94.5|93.3<br>95.5|87.5<br>89.2|
|0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Success Rate|noise=0.2<br>noise=0.5<br>noise=0.8|0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Success Rate<br>noise=0.2<br>noise=0.5<br>noise=0.8|0.05<br>0.10<br>0.15<br>0.20<br>0.25<br>Clipped Fraction|||noise=0.2<br>noise=0.5<br>noise=0.8|
|0.0|0<br>100<br>Step|0<br>100<br>Step<br>0.0|0.00|0|Step|100|
||_(a)_Train|_(b)_Eval||_(c)_Clip|ped Fraction||


_Figure 9._ Ablation on the noise level _a_ , conducted with the Flow-SDE _π_ 0 on the LIBERO-Spatial. 


_Figure 11._ Ablation on the chunk size, conducted with the Flow-SDE _π_ 0 on the LIBERO-Spatial. 

## **5.4. Hyper-Parameters** 

Building on the Flow-SDE with _π_ 0 model, we investigate the influence of the noise level, denoise step, and action chunk on the LIBERO-Spatial benchmark. We denote the train stage as the phase where the policy generates stochas- 

tic actions for exploration, whereas the evaluation stage involves generating deterministic actions. The train and eval success rates for the SFT baseline and the RL fine-tuned model after 100 training steps are presented in Tab. 2. 

**Noise Level.** The noise level _a_ in the Flow-SDE is defined in 

9 

_π_ **RL: Online RL Fine-tuning for Flow-based Vision-Language-Action Models** 

Eq. (8), which governs the noise injection magnitude during the denoising process. As shown in Tab. 2, the evaluation performance of the SFT baseline remains identical across all noise levels due to its reliance on deterministic ODE sampling. Conversely, its training performance exhibits a clear degradation as noise increases. This is intuitive, as higher noise levels can distort the flow trajectory, leading to an inaccurate estimation of the marginal action distribution. 

Extending this analysis to the RL fine-tuning stage highlights a critical trade-off: _while lower noise levels mitigate exploration-induced performance degradation, they simultaneously constrain the capacity for RL refinement._ This trade-off is empirically supported by Fig. 9, which shows that training with minimal noise ( _a_ = 0 _._ 2) leads to instability, characterized by a significantly higher clip fraction. We attribute this instability to the substantially larger gradient magnitudes associated with low-noise regimes. 

**Denoise Step.** The denoise step _K_ defines the number of discretization steps for action generation and is critical for controlling the fidelity of the ODE-to-SDE transition in Eq. (8). In Tab. 2, we observe that while all configurations start with similar eval performance, the train success rate plummets at _K_ = 1, indicating a significant ODE-to-SDE discretization error. 

However, a larger _K_ is not unequivocally optimal. As illustrated in Fig. 10, increasing _K_ presents a distinct trade-off: _while it enhances rollout performance, it simultaneously increases training complexity and computational overhead due to the extended sequence of denoising steps._ 

**Action chunk.** The action chunk refers to the number of consecutive actions the policy executes within a single observation. We ablate the action chunk size across 5, 10, and 20, with results visualized in Fig. 11. 

Although a larger chunk size yields marginal performance gains, it inherently reduces the frequency of policyenvironment interactions and obscures precise reward credit assignment. These constraints lead to less reliable advantage estimation, as evidenced by the diminished explained variance. Consequently, while an increased chunk size may offer a superior SFT baseline, it paradoxically limits the ceiling for subsequent RL-driven refinement. 

# **6. Conclusion** 

We introduce _π_ RL, a framework that enables flow-based VLAs, _π_ 0 and _π_ 0 _._ 5, to be fine-tuned with online RL algorithms. We tackle the fundamental challenge of intractable log-likelihoods in flow matching with Flow-Noise and FlowSDE solutions. Our extensive experiments on the challenging benchmarks demonstrated that _π_ RL achieves significant performance improvements over SFT baselines. 

**Limitation.** Due to the low sample efficiency of online RL, our framework currently relies on sim-to-real deployment. We aim to develop more efficient algorithms to enable realworld RL training in the future. 

# **References** 

- Beyer, L., Steiner, A., Pinto, A. S., Kolesnikov, A., Wang, X., Salz, D., Neumann, M., Alabdulmohsin, I., Tschannen, M., Bugliarello, E., et al. Paligemma: A versatile 3b vlm for transfer. _arXiv preprint arXiv:2407.07726_ , 2024. 

- Bjorck, J., Castañeda, F., Cherniadev, N., Da, X., Ding, R., Fan, L., Fang, Y., Fox, D., Hu, F., Huang, S., et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., et al. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Dabis, J., Finn, C., Gopalakrishnan, K., Hausman, K., Herzog, A., Hsu, J., et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 

- Chen, G., Li, Z., Wang, S., Jiang, J., Liu, Y., Lu, L., Huang, D.-A., Byeon, W., Le, M., Rintamaki, T., et al. Eagle 2.5: Boosting long-context post-training for frontier visionlanguage models. _arXiv preprint arXiv:2504.15271_ , 2025. 

- Chen, R. T., Rubanova, Y., Bettencourt, J., and Duvenaud, D. K. Neural ordinary differential equations. _Advances in neural information processing systems_ , 31, 2018. 

- Chi, C., Xu, Z., Feng, S., Cousineau, E., Du, Y., Burchfiel, B., Tedrake, R., and Song, S. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , 44(10-11): 1684–1704, 2025. 

- Din, M. U., Akram, W., Saoud, L. S., Rosell, J., and Hussain, I. Vision language action models in robotic manipulation: A systematic review. _arXiv preprint arXiv:2507.10672_ , 2025. 

- Fan, H., Dai, H., Zhang, J., Li, J., Yan, Q., Zhao, Y., Gao, M., Wu, J., Tang, H., and Dong, H. Twinaligner: Visual-dynamic alignment empowers physics-aware real2sim2real for robotic manipulation. _arXiv preprint arXiv:2512.19390_ , 2025. 

- Fei, S., Wang, S., Shi, J., Dai, Z., Cai, J., Qian, P., Ji, L., He, X., Zhang, S., Fei, Z., et al. Libero-plus: In-depth robust- 

10 

_π_ **RL: Online RL Fine-tuning for Flow-based Vision-Language-Action Models** 

- ness analysis of vision-language-action models. _arXiv preprint arXiv:2510.13626_ , 2025. 

- Firoozi, R., Tucker, J., Tian, S., Majumdar, A., Sun, J., Liu, W., Zhu, Y., Song, S., Kapoor, A., Hausman, K., et al. Foundation models in robotics: Applications, challenges, and the future. _The International Journal of Robotics Research_ , 44(5):701–739, 2025. 

- Guo, R., Lin, X., Liu, M., Gu, J., and Su, H. Mplib: a lightweight motion planning library. https://github.com/haosulab/MPlib, 2025. URL https://motion-planning-lib. readthedocs.io/latest/. 

- He, X., Fu, S., Zhao, Y., Li, W., Yang, J., Yin, D., Rao, F., and Zhang, B. Tempflow-grpo: When timing matters for grpo in flow models. _arXiv preprint arXiv:2508.04324_ , 2025. 

- Hu, E. J., Shen, Y., Wallis, P., Allen-Zhu, Z., Li, Y., Wang, S., Wang, L., Chen, W., et al. Lora: Low-rank adaptation of large language models. _ICLR_ , 1(2):3, 2022. 

- Hutchinson, M. F. A stochastic estimator of the trace of the influence matrix for laplacian smoothing splines. _Communications in Statistics-Simulation and Computation_ , 18(3):1059–1076, 1989. 

- Intelligence, P., Black, K., Brown, N., Darpinian, J., Dhabalia, K., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., et al. _π_ 0 _._ 5: a vision-language-action model with openworld generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 

- Jiang, G., Chang, H., Qiu, R.-Z., Liang, Y., Ji, M., Zhu, J., Dong, Z., Zou, X., and Wang, X. Gsworld: Closed-loop photo-realistic simulation suite for robotic manipulation. _arXiv preprint arXiv:2510.20813_ , 2025. 

- Kerbl, B., Kopanas, G., Leimkühler, T., and Drettakis, G. 3d gaussian splatting for real-time radiance field rendering. _ACM Trans. Graph._ , 42(4):139–1, 2023. 

- Khazatsky, A., Pertsch, K., Nair, S., Balakrishna, A., Dasari, S., Karamcheti, S., Nasiriany, S., Srirama, M. K., Chen, L. Y., Ellis, K., et al. Droid: A large-scale in-the-wild robot manipulation dataset. _arXiv preprint arXiv:2403.12945_ , 2024. 

- Kim, M. J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E., Lam, G., Sanketi, P., et al. Openvla: An open-source vision-languageaction model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- Kim, M. J., Finn, C., and Liang, P. Fine-tuning visionlanguage-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 

- Li, H., Zuo, Y., Yu, J., Zhang, Y., Yang, Z., Zhang, K., Zhu, X., Zhang, Y., Chen, T., Cui, G., et al. Simplevla-rl: Scaling vla training via reinforcement learning. _arXiv preprint arXiv:2509.09674_ , 2025a. 

- Li, J., Cui, Y., Huang, T., Ma, Y., Fan, C., Yang, M., and Zhong, Z. Mixgrpo: Unlocking flow-based grpo efficiency with mixed ode-sde. _arXiv preprint arXiv:2507.21802_ , 2025b. 

- Li, X., Hsu, K., Gu, J., Pertsch, K., Mees, O., Walke, H. R., Fu, C., Lunawat, I., Sieh, I., Kirmani, S., et al. Evaluating real-world robot manipulation policies in simulation. _arXiv preprint arXiv:2405.05941_ , 2024. 

- Li, Y., Wang, Y., Zhu, Y., Zhao, Z., Lu, M., She, Q., and Zhang, S. Branchgrpo: Stable and efficient grpo with structured branching in diffusion models. _arXiv preprint arXiv:2509.06040_ , 2025c. 

- Lipman, Y., Chen, R. T., Ben-Hamu, H., Nickel, M., and Le, M. Flow matching for generative modeling. _arXiv preprint arXiv:2210.02747_ , 2022. 

- Liu, B., Zhu, Y., Gao, C., Feng, Y., Liu, Q., Zhu, Y., and Stone, P. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791, 2023. 

- Liu, J., Gao, F., Wei, B., Chen, X., Liao, Q., Wu, Y., Yu, C., and Wang, Y. What can rl bring to vla generalization? an empirical study. _arXiv preprint arXiv:2505.19789_ , 2025a. 

- Liu, J., Liu, G., Liang, J., Li, Y., Liu, J., Wang, X., Wan, P., Zhang, D., and Ouyang, W. Flow-grpo: Training flow matching models via online rl. _arXiv preprint arXiv:2505.05470_ , 2025b. 

- Liu, X., Gong, C., and Liu, Q. Flow straight and fast: Learning to generate and transfer data with rectified flow. _arXiv preprint arXiv:2209.03003_ , 2022. 

- McAllister, D., Ge, S., Yi, B., Kim, C. M., Weber, E., Choi, H., Feng, H., and Kanazawa, A. Flow matching policy gradients. _arXiv preprint arXiv:2507.21053_ , 2025. 

- McLean, R., Chatzaroulas, E., McCutcheon, L., Röder, F., Yu, T., He, Z., Zentner, K., Julian, R., Terry, J., Woungang, I., et al. Meta-world+: An improved, standardized, rl benchmark. _arXiv preprint arXiv:2505.11289_ , 2025. 

- Mees, O., Hermann, L., Rosete-Beas, E., and Burgard, W. Calvin: A benchmark for language-conditioned policy learning for long-horizon robot manipulation tasks. _IEEE Robotics and Automation Letters_ , 7(3):7327–7334, 2022. 

11 

_π_ **RL: Online RL Fine-tuning for Flow-based Vision-Language-Action Models** 

- O’Neill, A., Rehman, A., Maddukuri, A., Gupta, A., Padalkar, A., Lee, A., Pooley, A., Gupta, A., Mandlekar, A., Jain, A., et al. Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 6892–6903. IEEE, 2024. 

- Peebles, W. and Xie, S. Scalable diffusion models with transformers. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pp. 4195–4205, 2023. 

- Pertsch, K., Stachowicz, K., Ichter, B., Driess, D., Nair, S., Vuong, Q., Mees, O., Finn, C., and Levine, S. Fast: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 

- Rafailov, R., Sharma, A., Mitchell, E., Manning, C. D., Ermon, S., and Finn, C. Direct preference optimization: Your language model is secretly a reward model. _Advances in neural information processing systems_ , 36: 53728–53741, 2023. 

- Ren, A. Z., Lidard, J., Ankile, L. L., Simeonov, A., Agrawal, P., Majumdar, A., Burchfiel, B., Dai, H., and Simchowitz, M. Diffusion policy policy optimization. _arXiv preprint arXiv:2409.00588_ , 2024. 

- Schulman, J., Moritz, P., Levine, S., Jordan, M., and Abbeel, P. High-dimensional continuous control using generalized advantage estimation. _arXiv preprint arXiv:1506.02438_ , 2015. 

- Schulman, J., Wolski, F., Dhariwal, P., Radford, A., and Klimov, O. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Bi, X., Zhang, H., Zhang, M., Li, Y., Wu, Y., et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. _arXiv preprint arXiv:2402.03300_ , 2024. 

- Shukor, M., Aubakirova, D., Capuano, F., Kooijmans, P., Palma, S., Zouitine, A., Aractingi, M., Pascal, C., Russi, M., Marafioti, A., et al. Smolvla: A vision-languageaction model for affordable and efficient robotics. _arXiv preprint arXiv:2506.01844_ , 2025. 

   - Tao, S., Xiang, F., Shukla, A., Qin, Y., Hinrichsen, X., Yuan, X., Bao, C., Lin, X., Liu, Y., Chan, T.-k., et al. Maniskill3: Gpu parallelized robotics simulation and rendering for generalizable embodied ai. _arXiv preprint arXiv:2410.00425_ , 2024. 

   - Team, O. M., Ghosh, D., Walke, H., Pertsch, K., Black, K., Mees, O., Dasari, S., Hejna, J., Kreiman, T., Xu, C., et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

   - Touvron, H., Lavril, T., Izacard, G., Martinet, X., Lachaux, M.-A., Lacroix, T., Rozière, B., Goyal, N., Hambro, E., Azhar, F., et al. Llama: Open and efficient foundation language models. _arXiv preprint arXiv:2302.13971_ , 2023. 

   - Wang, F. and Yu, Z. Coefficients-preserving sampling for reinforcement learning with flow matching. _arXiv preprint arXiv:2509.05952_ , 2025. 

   - Wen, J., Zhu, Y., Li, J., Zhu, M., Tang, Z., Wu, K., Xu, Z., Liu, N., Cheng, R., Shen, C., et al. Tinyvla: Towards fast, data-efficient vision-language-action models for robotic manipulation. _IEEE Robotics and Automation Letters_ , 2025. 

   - Williams, R. J. Simple statistical gradient-following algorithms for connectionist reinforcement learning. _Machine learning_ , 8(3):229–256, 1992. 

   - Yu, C., Wang, Y., Guo, Z., Lin, H., Xu, S., Zang, H., Zhang, Q., Wu, Y., Zhu, C., Hu, J., et al. Rlinf: Flexible and efficient large-scale reinforcement learning via macro-to-micro flow transformation. _arXiv preprint arXiv:2509.15965_ , 2025. 

   - Zang, H., Wei, M., Xu, S., Wu, Y., Guo, Z., Wang, Y., Lin, H., Shi, L., Xie, Y., Xu, Z., et al. Rlinf-vla: A unified and efficient framework for vla+ rl training. _arXiv preprint arXiv:2510.06710_ , 2025. 

   - Zhang, T., Yu, C., Su, S., and Wang, Y. Reinflow: Finetuning flow matching policy with online reinforcement learning. _arXiv preprint arXiv:2505.22094_ , 2025. 

- Song, Y., Sohl-Dickstein, J., Kingma, D. P., Kumar, A., Ermon, S., and Poole, B. Score-based generative modeling through stochastic differential equations. _arXiv preprint arXiv:2011.13456_ , 2020. 

- Tan, S., Dou, K., Zhao, Y., and Krähenbühl, P. Interactive post-training for vision-language-action models. _arXiv preprint arXiv:2505.17016_ , 2025. 

12 

_π_ **RL: Online RL Fine-tuning for Flow-based Vision-Language-Action Models** 

# **A. Appendix** 

This appendix provides additional technical details and experimental results for _π_ RL. The content is organized as: 

- **Appendix B** : Experimental Setup. 

- **Appendix C** : In-Distribution RL Training. 

- **Appendix D** : Out-of-Distribution RL Evaluation. 

- **Appendix E** : Case Studies: Single-Task RL Training. 

- **Appendix F** : Ablation Details. 

- **Appendix G** : Insights from Large-Scale RL Training. 

- **Appendix H** : RL for GR00T N1.5. 

- **Appendix I** : Limitations and Future Work. 

- **Appendix J** : Training Hyperparameters. 

# **B. Experimental Setup** 

## **B.1. Benchmarks.** 

To rigorously assess the performance and generalization of our framework, we conduct evaluations across four diverse benchmarks, with diverse emphases on robotic capability: 

## **B.2. Implementation Details.** 

Given that pre-trained models often struggle to generalize to task-specific benchmarks, we initiate our process with SFT on expert demonstrations. For the SFT stage, we fine-tune the entire 3.3B model following the official setting. In the subsequent RL stage, we freeze the VLM parameters and exclusively fine-tune the 300M action expert model, driven by GPU memory efficiency and the findings from RL4VLA that RL contributes more significantly to action generalization. We build the whole framework upon the RLinf (Yu et al., 2025) codebase, where we adopt a shared, co-located GPU allocation strategy that places the environment, rollout model, and actor model on the same GPU and executes them serially. 

For the model configurations, we adhere to the official setting provided by openpi (Black et al., 2024; Intelligence et al., 2025). In these settings, _π_ 0 utilizes image, language, and proprioceptive states as input, whereas _π_ 0 _._ 5 notably omits state information<sup>2</sup> . Our experiments are conducted on 8 NVIDIA H100 80GB GPUs, and detailed training hyperparameters are available in the Appendix Sec. J. 

# **C. In-Distribution RL Training** 

In this section, we evaluate the effectiveness of our framework across various benchmarks to demonstrate its robustness and superior performance in ID settings. 

## **C.1. LIBERO Benchmark** 

- **LIBERO** focuses on compositional variations and knowledge transfer in tasks. By evaluating across four task suites: _Spatial_ , _Object_ , _Goal_ , and _Long_ , it probes the model’s ability to transfer base skills to variations in object arrangements and long-horizon tasks. 

- **ManiSkill** emphasizes perceptual and execution robustness under massive environmental diversity. We follow the setup of RL4VLA (Liu et al., 2025a) and built a benchmark with 4,352 unique pick-and-place combinations, which challenges the policy to maintain physical interactions across a vast distribution of objects and receptacles. 

- **CALVIN** evaluates long-horizon sequential reasoning and vision-language grounding. It evaluates the model’s capacity to execute chains of five random subtasks in a persistent environment, requiring accurate alignment with linguistic instructions. 

- **MetaWorld** measures skill breadth and multi-task versatility. It requires a single policy to master 50 semantically distinct manipulation primitives, ranging from simple reaching to complex tool usage. 

**SFT Procedure.** The LIBERO benchmark comprises four task suites, each consisting of 10 distinct subtasks. To facilitate few-shot SFT on LIBERO, a minimum of 40 expert demonstration trajectories is necessary to ensure a positive success rate for each subtask across four task suites, thereby guaranteeing a positive optimization signal for the subsequent RL phase. 

We perform few-shot SFT following the official training configurations. For the _π_ 0 model, we fine-tune on a subset of 58 trajectories sampled from the 1,692 total demonstrations<sup>3</sup> , which serves as the initial checkpoint for subsequent RL training on the _Spatial_ , _Object_ , and _Goal_ task suites. For the _Long_ task suite, a larger pool of 208 trajectories is employed to address its more challenging, long-horizon nature. In contrast, for the _π_ 0 _._ 5 model, benefiting from a superior pre-trained checkpoint and training configurations, we leverage only 40 trajectories to provide a unified few-shot SFT checkpoint across all task suites. 

**RL Procedure.** In RL, the VLA model receives a multimodal input state comprising: an agent-view and a wrist- 

- 2https://github.com/Physical-Intelligence/openpi/issues/687 

> 3https://huggingface.co/datasets/physical-intelligence/libero 

13 

_π_ **RL: Online RL Fine-tuning for Flow-based Vision-Language-Action Models** 

_Table 3._ Evaluation results on the LIBERO benchmark, evaluated based on the success rate (%). 

|**Model**||||**LIBE**|**RO**|||
|---|---|---|---|---|---|---|---|
|||**Spatial**|**Object**|**Goal**|**Long**|**Avg.**|∆**Avg.**|
|_# Full Data_|_set SFT_|||||||
|Octo||78.9|85.7|84.6|51.1|75.1|—|
|OpenVLA||84.7|88.4|79.2|53.7|76.5|—|
|_π_fast||96.4|96.8|88.6|60.2|85.5|—|
|OpenVLA-|OFT|91.6|95.3|90.6|86.5|91.0|—|
|_π_0||96.8|98.8|95.8|85.2|94.2|—|
|_π_0_._5||98.8|98.2|98.0|92.4|96.9|—|
|_# Few-shot_|_SFT + RL_|||||||
||SFT|65.3|64.4|49.8|51.2|57.6|—|
|_π_0|Flow-SDE|98.4|99.4|96.2|90.2|96.1|+38.5|
||Flow-Noise|99.0|99.2|98.2|93.8|97.6|+**40.0**|
|_# Few-shot_|_SFT + RL_|||||||
||SFT|84.6|95.4|84.6|43.9|77.1|—|
|_π_0_._5|Flow-SDE|99.6|100|98.8|93.0|97.9|+20.8|
||Flow-Noise|**99.6**|**100**|**99.6**|**94.0**|**98.3**|+21.2|


_Table 4._ Evaluation results on the ManiSkill benchmark, with more specific OOD results depicted in Tab. 7. 

|**Model**||**IN**|**D**|||**OOD**|||
|---|---|---|---|---|---|---|---|---|
|||**Avg.**|∆|**Vision**|**Semantic**|**Execution**|**Avg.**|∆|
||SFT|38.4|—|32.6|8.4|13.2|18.1|—|
|_π_0|Flow-SDE|78.8|+40.4|61.1|25.4|31.5|39.3|+21.2|
||Flow-Noise|77.8|+39.4|63.4|23.1|24.2|36.9|+18.8|
||SFT|40.1|—|40.2|16.6|22.4|26.4|—|
|_π_0_._5|Flow-SDE|**90.9**|+**50.8**|68.0|34.5|45.4|49.3|+22.9|
||Flow-Noise|89.7|+49.6|**69.9**|**35.5**|**54.9**|**53.4**|+**27.0**|


view, natural language guidance, the robot end effector pose, and the gripper state. The model outputs an action to interact with the LIBERO environment, which provides a binary reward of 1 for successful task completion and 0 otherwise. 

**Experiments.** We benchmark the performance of _π_ RL, which fine-tunes the few-shot SFT _π_ 0 and _π_ 0 _._ 5 models with Flow-Noise and Flow-SDE, against several state-of-the-art VLAs trained on the entire LIBERO dataset, including Octo, OpenVLA, OpenVLA-OFT, _π_ fast (Pertsch et al., 2025), _π_ 0, and _π_ 0 _._ 5. We conduct experiments on four LIBERO task suites and report performance as the success rate across all 500 initial states (10 sub-tasks _×_ 50 states each). 

**Analysis.** For the few-shot _π_ 0 model, the SFT baseline performs poorly, with an average success rate of only 57.6%, indicating that the model struggles with limited demonstration data. _π_ RL substantially boosts performance, with Flow-SDE and Flow-Noise reaching 96.1% and 97.6%, and surpassing the full-dataset _π_ 0 SFT baseline of 94.2%. 

While the _π_ 0 _._ 5 few-shot SFT baseline achieves a decent average performance of 77.1%, it struggles with the challenging _Long_ task suite, scoring only 43.9%. Our proposed _π_ RL rectifies this deficiency, boosting the _Long_ task success rate from 43.9% to 94.0%, constituting a 50.1% improvement. Notably, despite using only a single trajectory for SFT, _π_ RL reaches 98.3% final performance, surpassing the 96.9% full-dataset SFT model. 

## **C.2. ManiSkill Benchmark** 

**SFT Procedure.** In the ManiSkill benchmark, the policy is required to pick from 16 object types and place them onto 17 receptacles across 16 unique table scenes, yielding 4,352 unique task combinations. Given the high complexity of this setting, the SFT dataset consists of 16,384 episodes synthesized using the MPLib motion planning suite (Guo et al., 2025). To reinforce the concept of motion completion, 15 additional frames are appended to the end of each trajectory. 

14 

_π_ **RL: Online RL Fine-tuning for Flow-based Vision-Language-Action Models** 

_Table 5._ Evaluation results on the CALVIN benchmark (Scene D), reporting the average completed subtasks and success rates for task sequences of length 1 to 5. 

|**Methods**|||||**CALVIN-D**||||
|---|---|---|---|---|---|---|---|---|
|||**Len-1**|**Len-2**|**Len-3**|**Len-4**|**Len-5**|**Avg.**|∆**Avg.**|
||SFT|94.7|84.9|74.3|65.2|57.5|3.766|—|
|_π_0|Flow-SDE|96.4|88.0|77.5|70.8|61.7|3.944|+0.178|
||Flow-Noise|96.9|88.8|78.0|68.3|59.9|3.919|+0.153|
||SFT|92.7|84.3|76.7|68.8|61.3|3.838|—|
|_π_0_._5|Flow-SDE|**99.7**|**98.2**|**95.8**|**91.0**|**87.0**|**4.717**|+**0.879**|
||Flow-Noise|99.6|97.6|93.9|89.6|84.5|4.652|+0.814|


_Table 6._ Evaluation results on the MetaWorld MT50 benchmark. 

|**Methods**||||**MetaWo**|**rld-MT50**|||
|---|---|---|---|---|---|---|---|
|||**Easy**|**Medium**|**Hard**|**Very Hard**|**Avg.**|∆**Avg.**|
|Diffusion Po|licy|23.1|10.7|1.9|6.1|10.5|—|
|TinyVLA||77.6|21.5|11.4|15.8|31.6|—|
|SmolVLA||87.1|51.8|70.0|64.0|68.2|—|
||SFT|77.9|51.8|53.3|20.0|50.8|—|
|_π_0|Flow-SDE|**92.1**|74.6|61.7|84.0|78.1|+27.3|
||Flow-Noise|91.1|**81.8**|**78.3**|**92.0**|**85.8**|+**35.0**|
||SFT|68.2|37.3|41.7|28.0|43.8|—|
|_π_0_._5|Flow-SDE|86.4|55.5|75.0|66.0|70.7|+26.9|
||Flow-Noise|86.8|58.1|63.3|56.0|66.1|+22.3|


**RL Procedure.** In RL, the VLA model receives a thirdperson RGB image, a concise language instruction, and the current joint proprioception. The environment provides a structured reward signal: 1.0 for correct object placement and an auxiliary 0.1 reward for successful gripper-object attachment, intended to encourage stable manipulation and mitigate undesired behaviors such as impulsive throwing. 

**Experiments.** Following the RL4VLA experimental protocol, we conduct RL training on a comprehensive set of 4,352 task combinations and record the performance as the aggregate success rate across these tasks. 

**Analysis.** As detailed in Tab. 4, _π_ RL significantly boosts performance in the training environment. Specifically, the success rate of _π_ 0 increases from 38.4% to 77.8%, while _π_ 0 _._ 5 improves from 40.1% to 90.9%. These gains underscore the efficacy of RL in complex settings. 

## **C.3. CALVIN Benchmark** 

**SFT Procedure.** We conduct SFT on the CALVIN ABC dataset<sup>4</sup> , which comprises approximately 24 hours of un- 

4https://huggingface.co/datasets/InternRobotics/InternDataCalvin_ABC 

structured "play data" across three distinct environments (A, B, and C). This dataset includes over 20,000 languagelabeled trajectories covering 34 unique manipulation tasks. 

**RL Procedure.** Each episode consists of a sequence of five randomly sampled subtasks to be completed in succession without environment resets. The reward signal is defined at the subtask level, where the model receives a sparse binary reward of 1.0 for each successfully executed subtask and 0.0 otherwise. 

**Experiments.** We evaluate the performance of _π_ RL in Scene D over 1,000 episodes. Following the standard CALVIN evaluation protocol, we report two key metrics: (1) the success rate for task sequences of increasing lengths, namely _Len-1_ to _Len-5_ . (2) the average number of completed subtasks, denoted as _Avg._ per episode. 

**Analysis.** As detailed in Tab. 5, _π_ RL yields substantial performance gains in long-horizon sequential execution, particularly with the _π_ 0 _._ 5 variant. The SFT models inherently struggle with compounding errors across sequential tasks, with _π_ 0 _._ 5 only achieving a 61.3% success rate on Len-5 sequences. RL effectively mitigates this issue with the average completed sub-tasks of Flow-SDE increasing from 3.838 to 4.717, and its Len-5 success rate surges to 87.0%. 

15 

_π_ **RL: Online RL Fine-tuning for Flow-based Vision-Language-Action Models** 

_Table 7._ Specific generalization evaluation results in the ManiSkill OOD setting. 

|**Environment**|**Variation-Version-Type**|_π_0**-SFT**|_π_0**-RL**<br>**Flow-SDE**|_π_0**-RL**<br>**Flow-Noise**|_π_0_._5**-SFT**|_π_0_._5**-RL**<br>**Flow-SDE**|_π_0_._5**-RL**<br>**Flow-Noise**|
|---|---|---|---|---|---|---|---|
|In distribution|Main-v3-train|38.4|78.8|77.8|40.1|**90.9**|89.7|
||Instruct-v1-test|30.1|64.6|66.5|46.6|77.0|**85.7**|
||VisionImage-v1-test|38.3|68.8|71.7|46.2|78.8|**83.1**|
|Visual-Language|VisionTexture03-v1-test|35.1|66.0|66.8|36.7|69.6|**75.0**|
|Variations|VisionTexture05-v1-test|31.0|55.8|60.5|32.7|58.0|**62.2**|
||VisionWhole03-v1-test|35.4|62.4|69.0|40.1|69.6|**71.6**|
||VisionWhole05-v1-test|28.5|49.0|53.9|30.7|55.0|**57.0**|
|Sti Ri|MultiCarrot-v1-test|7.8|28.2|23.0|16.7|36.8|**38.2**|
|emanc easonng<br>b/l|MultiCarrot-v1-train|12.5|36.5|31.8|28.2|49.5|**50.1**|
|(ojectreceptace<br>|MultiPlate-v1-test|5.0|16.4|18.3|11.8|**29.4**|28.3|
|confounders)|MultiPlate-v1-train|7.3|20.5|19.6|9.7|22.3|**25.4**|
|Ai Ei|PositionChangeTo-v1-test|9.6|17.4|10.9|13.5|36.2|**54.7**|
|cton xecuton|Position-v1-test|16.9|45.6|37.5|31.2|54.5|**55.0**|


Notably, the performance gap between SFT and RL widens significantly as the sequence length increases. For _π_ 0 _._ 5, while Flow-SDE shows a modest 7.0% improvement over SFT in Len-1 tasks, the gap expands to an impressive 25.7% in the most challenging Len-5 sequences. 

## **C.4. MetaWorld Benchmark** 

**SFT Procedure.** We perform SFT on the _π_ 0 and _π_ 0 _._ 5 models using the official dataset<sup>5</sup> , which consists of 2500 trajectories across 50 different manipulation tasks. 

**RL Procedure.** During the RL procedure, the VLA model processes a multi-modal input comprising a RGB agentview image, language guidance, the robot’s end-effector position, and its gripper state. Based on this input, the model outputs an action to interact with the environment, which in turn provides a sparse reward: 1 for successful task completion and 0 otherwise. 

**Experiments.** We benchmark the performance of _π_ RL against Diffusion Policy (Chi et al., 2025), TinyVLA (Wen et al., 2025), and SmolVLA (Shukor et al., 2025). For the performance evaluation, we follow the setup from SmolVLA, _i_ . _e_ ., classifying 50 tasks into _easy_ , _medium_ , _hard_ , and _very hard_ four categories according to their difficulties. 

**Analysis.** As detailed in Tab. 6, RL fine-tuning substantially boosts performance. The _π_ 0 and _π_ 0 _._ 5 models achieve average success rates of 85.8% and 70.7%, respectively. This marks a significant improvement over their SFT-only counterparts and surpasses the SmolVLA baseline of 68.2%, confirming that RL can effectively enhance model capabilities across a diverse range of manipulation task types. 

5https://huggingface.co/datasets/lerobot/metaworld_mt50 

# **D. Out-of-Distribution RL Evaluation** 

While previous experiments demonstrate significant RLdriven improvements in the ID domain, this section evaluates OOD generalization. As LIBERO lacks a dedicated interface for OOD testing, we utilize the ManiSkill, CALVIN, and MetaWorld benchmarks to investigate _whether the RLdriven improvements represent genuine skill acquisition that scales to novel settings, or merely reflect the exploitation of environment-specific biases._ 

## **D.1. ManiSkill** 

**Setup.** Following RL4VLA, we evaluate the model’s generalization across three challenging OOD scenarios: (1) _Vision_ , challenging the model with novel backgrounds and textures; (2) _Semantics_ , probing comprehension with unseen objects, varied instructions, and confounding elements like extra objects or receptacles; (3) _Execution_ , assessing robustness against varied initial states, unseen robot poses, and dynamic disturbances. 

**Results.** In the OOD scenarios detailed in Tabs. 4 and 7, we observe that the _π_ 0-SFT model demonstrates strong generalization for visual information. This can be attributed to the robust foundation of its VLM, which allows it to handle visual disturbances better. 

However, the semantic performance of _π_ 0 drops dramatically. This degradation is less pronounced when switching to the _π_ 0 _._ 5 baseline, a benefit likely stemming from the knowledge generalization of the pre-trained _π_ 0 _._ 5 model. Regarding action execution, _π_ 0 exhibits a larger performance drop than _π_ 0 _._ 5. We hypothesize that this discrepancy arises from the inclusion of joint angle states as input in _π_ 0, leading to severe overfitting in the control task. In contrast, _π_ 0 _._ 5 

16 

_π_ **RL: Online RL Fine-tuning for Flow-based Vision-Language-Action Models** 

_Table 8._ Evaluation results on the SIMPLER benchmark for _π_ 0 and _π_ 0 _._ 5 with Flow-Noise method. 

|**Model**||||**SIMPLER**|||
|---|---|---|---|---|---|---|
|||**Carrot**|**Eggplant**|**Spoon**|**Cube**|**Avg.**|
||SFT|82.7|87.5|61.7|37.1|67.2|
|_π_0|+RL|**95.7**|96.7|**91.6**|**63.0**|**86.7**|
||∆|+13.0|+9.2|+29.9|+25.9|+19.5|
||SFT|70.6|91.9|43.5|31.0|59.2|
|_π_0_._5|+RL|82.0|**98.2**|82.8|53.3|79.1|
||∆|+11.4|+6.3|+39.3|+22.3|+19.9|


_Figure 12._ Real-world deployment of an RL refined policy performing a pick and place task. 

omits these inputs, thereby avoiding the same degree of performance degradation. 

As for the RL training, although the performance improvements in OOD scenarios are lower than those in IND settings, the proportional improvements achieved are notably comparable. As indicated in Tab. 4, for the _π_ 0 _._ 5 model, Flow-SDE enhances the IND success rate by 126.7%, while the OOD similarly increases by 102.3%. This consistency in relative gains indicates that RL-driven optimization promotes the acquisition of generalized action representations rather than merely overfitting the training environment, thus preserving efficacy under distribution shifts. 

Nevertheless, we observe a performance gap in relative improvement between the _Vision_ OOD tasks and the IND domain. Specifically, for _π_ 0 _._ 5, the 73.9% gain in visual generalization trails the 126.7% increase observed in the training environment. This discrepancy likely stems from freezing the VLM backbone during the RL stage for computational efficiency, which restricts the model’s ability to adapt its visual grounding features to novel textures and backgrounds. 

## **D.2. CALVIN** 

**Setup.** We evaluate environmental and visual OOD robustness based on the ABC _→_ D protocol in CALVIN. Under this setting, the model is trained on ABC environments and evaluated in a zero-shot manner on Scene D. Scene D introduces significant distribution shifts in terms of visual textures, lighting conditions, and spatial layouts, effectively assessing the agent’s ability to transfer skills to an unfamiliar physical environment. 

**Results.** Under identical D _→_ D training settings, the RL finetuned policy in the ABC environment reaches a 79.1% success rate in the OOD scene D, improving over the 61.3% SFT baseline as shown in Fig. 5. Aligned with the findings in ManiSkill, this suggests that ID gains can be transferred to OOD settings characterized by visual variations. 

## **D.3. MetaWorld** 

**Setup.** We utilize the ML45 benchmark from MetaWorld to evaluate the task-level generalization. This setup consists of 50 distinct robotic manipulation tasks: the agent is trained on 45 base tasks and subsequently evaluated on 5 heldout, unseen tasks, which require the model to generalize its learned manipulation primitives to entirely novel task objectives and workspace configurations. 

**Results.** As evidenced in the Fig. 5, while success rates show consistent gains within the ID domain, OOD performance is characterized by persistent oscillation throughout the training process. This instability indicates that RL, in its current form, struggles to foster stable cross-category generalization. 

Nevertheless, the model retains the OOD skills learned during the SFT phase throughout the RL training process. This highlights a significant advantage over standard SFT, which often causes the model to overfit on expert demonstrations and lose its broader capabilities (Li et al., 2025a). Unlike standard SFT, RL enables ID performance gains while preserving the general knowledge, which indicates that RL provides a more balanced optimization that maintains OOD robustness without catastrophic forgetting. 

17 

_π_ **RL: Online RL Fine-tuning for Flow-based Vision-Language-Action Models** 

_Table 9._ Comparison of the PPO and GRPO with Flow-SDE on the LIBERO. 

|**Model**||||**LIBE**|**RO**|||
|---|---|---|---|---|---|---|---|
|||**Spatial**|**Object**|**Goal**|**Long**|**Avg.**|∆**Avg.**|
||SFT|65.3|64.4|49.8|51.2|57.6|—|
|_π_0|+GRPO|97.8|97.8|83.2|81.4|90.0|+32.4|
||+PPO|98.4|99.4|96.2|90.2|96.0|+**38.4**|
||SFT|84.6|95.4|84.6|43.9|77.1|—|
|_π_0_._5|+GRPO|97.4|99.8|91.2|77.6|91.5|+14.4|
||+PPO|**99.6**|**100**|**98.8**|**93.0**|**97.9**|+20.8|


## **D.4. Summary** 

In conclusion, our OOD evaluation demonstrates that _RL enhances performance for similar tasks but fails to generalize effectively to novel task objectives_ . 

Specifically, RL training effectively enhances robustness against low-level variations such as the visual and execution shifts observed in ManiSkill and CALVIN. This indicates that the model acquires generalized action representations rather than merely overfitting to the training environment. 

Regarding high-level generalization on MetaWorld, the model successfully retains the OOD skills inherited from the SFT phase, demonstrating that RL avoids the catastrophic forgetting and overfitting typical of standard imitation learning. However, transferring its performance gains to entirely novel task objectives remains a significant challenge. 

# **E. Case Studies: Single-Task RL Training** 

While the preceding experiments focused on performance across multi-task benchmarks, this section investigates single-task scenarios where the VLA is trained to master a specific task within a relatively static environment. Specifically, we evaluate our approach on the **SIMPLER** (Li et al., 2024) and a **Real2Sim2Real** environment. 

## **E.1. SIMPLER** 

**Setup.** In SIMPLER, the experimental setup comprises an 8-DoF WidowX-250S arm evaluated on four standard tasks: (1) Spoon: placing a spoon on a cloth. (2) Carrot: placing a carrot on a plate. (3) Eggplant: placing an eggplant in a basket. (4) Cube: stacking a cube. For the SFT stage, we employ a curated dataset in which each task is trained with 144 demonstration episodes. 

**Analysis.** As detailed in Tab. 8, _π_ RL increases the average success rate of the _π_ 0 model from 67.2% to 86.7%, with three tasks (carrot, eggplant, and spoon) exceeding 90% success. 

## **E.2. Real2Sim2Real** 

While the SIMPLER benchmark demonstrates predictive correlation between simulation and real-world performance, a pronounced visual domain shift remains to be solved. To this end, we leverage recent Real2Sim2Real methodologies (Fan et al., 2025; Jiang et al., 2025) to construct a highfidelity simulation environment with ManiSkill for rigid body dynamics and Gaussian Splatting (Kerbl et al., 2023) for photorealistic rendering. 

**Setup.** Our hardware platform comprises a Franka Panda robotic arm and an Intel RealSense D435 camera serving as the primary visual sensor. We perform manual calibration by aligning simulated viewpoints with real-world camera perspectives to synchronize their extrinsic matrices. As illustrated in Fig. 1, the photorealistic textures and color profiles in our simulator closely mirror the physical environment, effectively minimizing the visual domain shift from simulation to reality. 

**Results.** Following the experimental protocol established in the ManiSkill benchmarks, we initially collect 20 expert trajectories via a motion planner for few-shot SFT, which is subsequently optimized through RL over 100 training iterations. We deploy the RL fine-tuned policies in the real world in a zero-shot manner. Empirical results indicate that while the SFT baseline fails to complete the task, the RLtuned policy achieves a 40% success rate. A representative successful episode is visualized in Fig. 12. 

# **F. Ablation Details** 

## **F.1. RL algorithms** 

Given the significant performance gains from PPO on the LIBERO benchmark, we also investigated the effectiveness of GRPO (Shao et al., 2024), another widely used policy gradient method applied in VLA+RL training (Li et al., 2025a). We compare the performance of PPO and GRPO on both the _π_ 0 and _π_ 0 _._ 5 models, with results denoted in Tab. 9. 

**Conclusion.** To sum up, our findings highlight a critical 

18 

_π_ **RL: Online RL Fine-tuning for Flow-based Vision-Language-Action Models** 


_Figure 14._ Ablation study on the learning rate scheduler. 

trade-off: _parameters tailored for rollout success may adversely impact training stability, ultimately constraining the performance ceiling of RL._ Therefore, careful parameter tuning is required to achieve a synergy between high-quality rollouts and stable policy convergence. 

LIBERO benchmark is not evident. We conjecture the limited performance gain owing to the limited scene variability within LIBERO, for which the pretrained VLM representations are already sufficiently robust. **(2)** Fine-tuning VLM together with the action expert requires a more conservative optimization configuration for training stability. 

## **F.2. VLM Fine-tuning Analysis** 

In our previous experiments, the VLM is frozen, and the optimization is confined exclusively to the action expert during RL. In this subsection, we aim to investigate the role of the VLM during RL. Specifically, we employ LowRank Adaptation (LoRA) (Hu et al., 2022) for the VLM, facilitating its joint optimization with the action expert. We set the LoRA rank to _r_ = 32 and the scaling parameter to _α_ = 32, while the action expert remains fully trainable. 

We conduct experiments with the _π_ 0 model with Flow-SDE on the LIBERO-Long benchmark, comparing three distinct configurations: 

- **VLM Frozen** : 5 _e_<sup>_−_6</sup> learning rate, 4 updates/epoch. 

- **VLM LoRA-I** : 5 _e_<sup>_−_6</sup> learning rate, 4 updates/epoch. 

- **VLM LoRA-II** : 1 _e_<sup>_−_6</sup> learning rate, 2 updates/epoch. 

As presented in Fig. 13, the VLM LoRA-II configuration achieves a learning trajectory comparable to the VLM frozen baseline. This empirical observation yields two critical inferences: **(1)** The benefit of fine-tuning the VLM on the 

# **G. Insights from Large-Scale RL Training** 

In this section, we elaborate on some empirical insights we gained during RL training. 

**Hyperparameters.** According to the hyperparameters ablation detailed in Sec. 5.4, the performance disparity between the train and eval performance of the initial SFT checkpoint warrants close attention. If this disparity is significant, we recommend either reducing the noise magnitude or increasing the number of denoising steps to mitigate the performance loss when shifting from deterministic to stochastic execution. Furthermore, as previously established, lower noise levels yield larger gradients, requiring a smaller learning rate to maintain training stability. 

We also observed that when train performance improves steadily while eval performance oscillates, increasing the number of denoising steps can help alleviate this, benefiting from reduced divergence in the action distributions between the deterministic and stochastic action generation processes. Regarding the action chunk, we empirically found that longhorizon tasks benefit from larger chunk sizes. For instance, we set the chunk size to 10 for LIBERO-Long and 5 for the 

19 

_π_ **RL: Online RL Fine-tuning for Flow-based Vision-Language-Action Models** 


_Figure 16._ Episode length: _π_ 0 _._ 5 RL training in ManiSkill. 

## other sub-tasks. 

**Training.** In our _π_ 0 _._ 5 experiments on the LIBERO-Long benchmark, we observed that the Kullback–Leibler (KL) divergence metric increased steadily throughout training, potentially leading to instability. We mitigated this issue by implementing a learning rate scheduler with cosine annealing. As demonstrated in Fig. 14, this scheduler effectively prevents the KL divergence from escalating, thereby stabilizing the training process. 

**Critic.** In our ManiSkill experiments, we observe that policy evaluation performance exhibits an initial dip before improving for both _π_ 0 and _π_ 0 _._ 5 models, as shown in Fig. 15. We attribute this transient degradation to the critic providing inaccurate signals during its warm-up phase. The subsequent eval improvement correlates directly with the critic’s value estimations stabilizing, as evidenced by the rising explained variance. 

**Temporal Efficiency.** We also study how the rollout of RL in a physical simulator helps shape the policy to achieve expert-level temporal efficiency. We analyze the expert motion planning data used for SFT and then tracked the average episode lengths during the RL training of the _π_ 0 _._ 5 model in ManiSkill. As shown in Fig. 16, the SFT-initialized policy exhibits significantly longer episodes due to execution errors. In contrast, _π_ 0 _._ 5 achieves episode lengths that converge to the expert range after RL training, demonstrating a substantial improvement in temporal efficiency. 

We attribute this convergence to two factors: **(1)** RL en- 

hances the policy’s error-correction capabilities, allowing it to recover from execution failures. **(2)** Our partial reset mechanism incentivizes temporal efficiency through discounted rewards, as faster task completion enables the agent to trigger more resets and accumulate higher total rewards within each update cycle. 

# **H. RL for GR00T N1.5** 

## **H.1. Setup** 

**GR00T N1.5.** We conduct additional experiments based on the GR00T N1.5 model (Bjorck et al., 2025), which is a foundation model tailored for generalist humanoid robot reasoning and manipulation. The architecture integrates an Eagle 2.5 VLM (Chen et al., 2025), optimized for spatial grounding and physical reasoning, with a Diffusion Transformer head (Peebles & Xie, 2023) for action denoising. It facilitates multi-embodiment compatibility through specialized heads, supporting configurations such as humanoids with dexterous hands or grippers, as well as single-arm manipulators. 

Regarding the critic implementation, we estimate value functions across the entire denoising trajectory by integrating the critic network directly with the action head. The complete framework is illustrated in Fig. 17. 

**Benchmark.** We evaluate the model performance of GR00T across four manipulation task suites in LIBERO: _Spatial_ , _Object_ , _Goal_ , and _Long_ . 

20 

_π_ **RL: Online RL Fine-tuning for Flow-based Vision-Language-Action Models** 


_Figure 17._ Illustration for the architecture of GR00T-N1.5. 

_Table 10._ Results of Finetuning GR00T using PPO with Flow-SDE on the LIBERO. 

|||||**LIBE**|**RO**|||
|---|---|---|---|---|---|---|---|
|**Model**||||||||
|||**Spatial**|**Object**|**Goal**|**Long**|**Avg.**|∆**Avg.**|
|GR00T|SFT|41.4|58.6|48.2|61.9|52.5|—|
||+PPO|92.5|96.2|84.3|86.6|89.9|+**37.4**|


**Implementation Details.** Similar to the _π_ 0 implementation, we initiate our process with SFT on expert demonstrations. For the SFT stage, we fine-tune the entire model following the official setting. In the subsequent RL stage, we exclusively fine-tune the action expert model while keeping the vision-language model parameters fixed. 

A crucial methodological refinement in our RL pipeline is the replacement of dropout layers in the expert model with identity layers. Dropout is widely recognized to induce instability during online RL training. Specifically, it introduces non-deterministic perturbations to the effective policy, shifting the standard probability ratio update from: 

## **H.2. Results** 

Results are summarized in Tab. 10. For the few-shot model, the SFT baseline achieves only a 52.5% success rate, reflecting limited generalization from sparse demonstrations. Conversely, our RL-based Flow-SDE significantly improves performance to 89.9%. These results, obtained using default _π_ 0 configurations, underscore the broad applicability of our method across architectures. While task-specific tuning could further enhance performance, we leave such optimization for future work. 

# **I. Limitations and Future Work** 


to a highly unstable form: 


where _ρt_ ( _θ_ ) denotes the probability ratio, and _α_ new represents the policy state post-update as modified by the stochastic dropout mask. This structural stochasticity, compounded with per-step policy updates, severely undermines training convergence. The training hyperparameters are identical to those used for _π_ 0, with Flow-SDE employed as the primary RL algorithm. 

**Noise Injection.** Our current noise injection strategy exhibits a performance drop during the ODE-to-SDE conversion. Flow-CPS (Wang & Yu, 2025) attributes this loss to numerical error and proposes an improved coefficientspreserving sampling method. In our experiments, we attempted this configuration. Consistent with our hyperparameter ablation, our experiments showed that while this configuration mitigated the ODE-SDE precision error, it yielded limited RL improvement. Nevertheless, we argue that improving the noise injection strategy holds significant potential, specifically converting the ODE formulation to an SDE formulation while preserving the action distribution undisturbed. 

**Training Acceleration.** Our current implementation of the mixed ODE-SDE rollout is simplistic in Flow-SDE, _i_ . _e_ ., it 

21 

_π_ **RL: Online RL Fine-tuning for Flow-based Vision-Language-Action Models** 

randomly selects one denoising step as an SDE step, while all other steps remain ODE steps. We posit that future investigations into mixed ODE-SDE rollouts, leveraging advances in accelerating flow-based image generation (Li et al., 2025b; He et al., 2025; Liu et al., 2025b; Li et al., 2025c), could further enhance Flow-SDE, leading to faster training and improved performance. 

**Generalization.** Maniskill OOD tests indicate that the semantic generalization of SFT and RL models remains limited. To address this, future work will leverage RL to enhance robustness by training on more diverse task distributions and varied linguistic instructions, thereby fostering better cross-task adaptability. 

# **J. Training Hyperparameters.** 

We record the training hyperparameters used to train both _π_ 0 and _π_ 0 _._ 5 on each benchmark, and present them in Tabs. 11 to 13. 

22 

_π_ **RL: Online RL Fine-tuning for Flow-based Vision-Language-Action Models** 

_Table 11._ Hyperparameters across LIBERO. 

|||||**Algorithms**|**and Tasks**||||
|---|---|---|---|---|---|---|---|---|
|**Parameters**||**_π_0**||||**_π_0****_._5**|||
||**Spatial**|**Object**|**Goal**|**Long**|**Spatial**|**Object**|**Goal**|**Long**|
|Train epochs|500|500|500|500|500|500|500|500|
|Global batch size|2048|2048|2048|2048|2048|2048|2048|2048|
|Update epochs<br>|4<br>|4<br>|4<br>|4<br>|1<br>|1<br>|3<br>|4<br>|
|Actor lr<br>|5e-6<br>|5e-6<br>|5e-6<br>|5e-6<br>|5e-6<br>|5e-6<br>|5e-6<br>|5e-6<br>|
|Critic lr<br>|1e-4<br>|1e-4<br>|1e-4<br>|1e-4<br>|1e-4<br>|1e-4<br>|1e-4<br>|1e-4<br>|
|Scheduler|False|False|False|False|False|False|False|True|
|Reward discount rate_γ_|0.99|0.99|0.99|0.99|0.99|0.99|0.99|0.99|
|GAE_λ_|0.95|0.95|0.95|0.95|0.95|0.95|0.95|0.95|
|Clip ratio_ϵ_|0.2|0.2|0.2|0.2|0.2|0.2|0.2|0.2|
|Interaction steps|240|240|320|480|240|320|320|480|
|Parallel environments|64|64|64|64|64|64|64|64|
|Rollout epochs|8|8|8|8|8|8|8|8|
|Action prediction horizon_H_<br>|50|50|50|50|10|10|10|10|
|Action replan horizon_H_<sup>_′_</sup>|5|5|5|10|5|5|5|10|
|Denoise steps|4|4|4|4|3|5|5|5|
|Noise level_σ_(Flow-SDE)|0.5|0.5|0.5|0.5|0.5|0.3|0.3|0.5|
|Max log-var (Flow-Noise)|0.16|0.16|0.16|0.16|0.10|0.10|0.10|0.10|
|Min log-var (Flow-Noise)|0.08|0.08|0.08|0.08|0.04|0.04|0.04|0.04|
|Entropy bonus (Flow-Noise)|0.005|0.005|0.005|0.005|0.005|0.005|0.005|0.005|


_Table 12._ Hyperparameters across SIMPLER and ManiSkill. 

||||||**Algorithms**|**and Tasks**|||||
|---|---|---|---|---|---|---|---|---|---|---|
|**Parameters**|||**_π_0**|||||**_π_0****_._5**|||
||**Eggplant**|**Carrot**|**Spoon**|**Cube**|**ManiSkill**|**Eggplant**|**Carrot**|**Spoon**|**Cube**|**ManiSkill**|
|SFT train steps|1000|1000|1000|1000|1000|1000|1000|1000|1000|1000|
|RL train steps|40|40|40|130|150|40|40|40|70|150|
|Global batch size|2560|2560|2560|2560|5120|2560|2560|2560|2560|5120|
|Update epochs|4|4|4|4|4|4|4|4|4|5|
|Actor lr|5.6e-6|5.6e-6|5.6e-6|5.6e-6|7.91e-6|5.6e-6|5.6e-6|5.6e-6|5.6e-6|7.91e-6|
|Critic lr<br>Scheduler|1.1e-4<br>False|1.1e-4<br>False|1.1e-4<br>False|1.1e-4<br>False|1.55e-4<br>False|1.1e-4<br>False|1.1e-4<br>False|1.1e-4<br>False|1.1e-4<br>False|1.55e-4<br>False|
|Reward discount rate_γ_|0.99|0.99|0.99|0.99|0.99|0.99|0.99|0.99|0.99|0.99|
|GAE_λ_|0.95|0.95|0.95|0.95|0.95|0.95|0.95|0.95|0.95|0.95|
|Clip ratio_ϵ_|0.2|0.2|0.2|0.2|0.2|0.2|0.2|0.2|0.2|0.2|
|Interaction steps|48|48|48|48|48|48|48|48|48|48|
|Parallel environments|256|256|256|256|320|256|256|256|256|320|
|Rollout epochs|1|1|1|1|1|1|1|1|1|1|
|Action prediction horizon_H_|8|8|8|8|8|8|8|8|8|8|
|Action replan horizon_H_<sup>_′_</sup>|5|5|5|5|5|5|5|5|5|5|
|Denoise steps|4|4|4|4|4|4|4|4|4|4|
|<br>Noise level_σ_(Flow-SDE)|0.5|0.5|0.5|0.5|0.5|0.5|0.5|0.5|0.5|0.5|
|Max log-var (Flow-Noise)|0.16|0.16|0.16|0.16|0.16|0.10|0.10|0.10|0.10|0.10|
|Min log-var (Flow-Noise)|0.08|0.08|0.08|0.08|0.08|0.04|0.04|0.04|0.04|0.04|
|Entropy bonus (Flow-Noise)|0.005|0.005|0.005|0.005|0.005|0.005|0.005|0.005|0.005|0.005|


23 

_π_ **RL: Online RL Fine-tuning for Flow-based Vision-Language-Action Models** 

_Table 13._ Hyperparameters across MetaWorld and CALVIN benchmarks. 

|||**Benchmark**|**s and models**||
|---|---|---|---|---|
|**Parameters**|**Meta**|**World**||**CALVIN**|
||**_π_0**|**_π_0****_._5**|**_π_0**|**_π_0****_._5**|
|Train epochs|450|450|100|100|
|Global batch size|2048|2048|2048|2048|
|Update epochs|4|4|4|4|
|Actor lr|1e-5|5e-6|5e-6|5e-6|
|Critic lr|1e-4|1e-4|1e-4|1e-4|
|Scheduler|False|True|False|False|
|Reward discount rate_γ_|0.99|0.99|0.99|0.99|
|GAE_λ_|0.95|0.95|0.95|0.95|
|Clip ratio_ϵ_|0.2|0.2|0.2|0.2|
|Interaction steps|100|100|480|480|
|Parallel environments|64|64|64|64|
|Rollout epochs|8|8|8|8|
|Action prediction horizon_H_<br>|5|5|5|5|
|Action replan horizon_H_<sup>_′_</sup>|5|5|5|5|
|Denoise steps|5|5|5|5|
|Noise level_σ_(Flow-SDE)|0.5|0.5|0.5|0.5|
|Max log-var (Flow-Noise)|0.10|0.10|0.16|0.16|
|Min log-var (Flow-Noise)|0.04|0.04|0.08|0.08|
|Entropy bonus (Flow-Noise)|0.005|0.005|0.005|0.005|


24 

