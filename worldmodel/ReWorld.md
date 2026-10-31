---
title: "ReWorld: Multi-Dimensional Reward Modeling for Embodied World Models"
date: "2026-01-18"
authors: "Baorui Peng; Wenyao Zhang; Liang Xu; Zekun Qi; Jiazhao Zhang; Hongsi Liu"
url: https://arxiv.org/abs/2601.12428
pdf: https://arxiv.org/pdf/2601.12428
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.12428)** / [論文ページ](https://arxiv.org/abs/2601.12428)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **ReWorld: Multi-Dimensional Reward Modeling for Embodied World Models** 

Baorui Peng<sup>1</sup><sup>_,_2*</sup> , Wenyao Zhang<sup>1</sup><sup>_,_3*†</sup> , Liang Xu<sup>1</sup><sup>_,_3</sup> , Zekun Qi<sup>4</sup> , Jiazhao Zhang<sup>6</sup> , Hongsi Liu<sup>1</sup><sup>_,_5</sup> , Wenjun Zeng<sup>1</sup> , Xin Jin<sup>1‡</sup> 

1Eastern Institute of Technology, Ningbo 2Georgia Institute of Technology 

3Shanghai Jiao Tong University, 4Tsinghua University, 5University of Science and Technology of China 6Peking University 

## **Abstract** 

_Recently, video-based world models that learn to simulate the dynamics have gained increasing attention in robot learning. However, current approaches primarily emphasize visual generative quality while overlooking physical fidelity, dynamic consistency, and task logic, especially for contact-rich manipulation tasks, which limits their applicability to downstream tasks. To this end, we introduce ReWorld, a framework aimed to employ reinforcement learning to align the video-based embodied world models with_ **_physical realism, task completion capability, embodiment plausibility_** _and_ **_visual quality._** _Specifically, we first construct a large-scale (∼_ 235 _K) video preference dataset and employ it to train a hierarchical reward model designed to capture multi-dimensional reward consistent with human preferences. We further propose a practical alignment algorithm that post-trains flow-based world models using this reward through a computationally efficient PPO-style algorithm. Comprehensive experiments and theoretical analysis demonstrate that ReWorld significantly improves the physical fidelity, logical coherence, embodiment and visual quality of generated rollouts, outperforming previous methods._ 

## **1. Introduction** 

Video-based embodied world models (EWMs) [24, 29], generative models that learn to simulate the dynamics of embodied environments, have become a cornerstone for developing general-purpose embodied intelligence [15, 41]. They enable diverse downstream capabilities, including scalable data generation [38], interactive simulation [12, 40], and integration with vision-language-action models [11, 33, 79]. 

Despite the impressive generative capabilities [3, 9], they still struggle with what we term as **Physics Uncanny Val-** 

> *Equal contribution 

> †Project leader 

> ‡Corresponding author 


Figure 1. Our proposed ReWorld bridges the gap of video-based embodied world models with **physical realism, task completion capability, embodiment plausibility,** and **visual quality.** Each of the four dimensions shown is rated on a scale of 1 (poor) to 6 (excellent), where higher scores indicate better performance. 

**ley** —a gap between visual plausibility and physical consistency as shown in Fig. 1. This limitation primarily arises because current models are trained almost exclusively under a supervised paradigm, exposing them only to successful demonstrations. Without encountering failures or understanding “what not to do”, these models struggle to internalize the implicit physical laws that govern the real world. Although previous works try to mitigate it by introducing more abundant conditions ( _e.g._ , text [14, 66], trajectory [20], depth [73, 81] and physical law [44]), maintaining visual plausibility and physical consistency remains a formidable challenge. 

This raises a key question: how can we align these powerful generative models with the complex, implicit rules of physical interaction? Reinforcement learning (RL) [58], particularly when combined with human feedback (RLHF) [16], has successfully addressed similar alignment challenges in other domains( _e.g._ , Large Language Models [14, 66], image generation [8, 75]). However, transferring this paradigm to embodied videos suffers from two major barriers: (i) **The Reward Barrier (Perception):** How do we even define a “good” embodied video? Sparse 

1 

task-success signals from online interaction (common in robotics [15]) are insufficient, as they fail to penalize subtle yet critical physical violations. Conversely, a single, monolithic reward like aesthetic score [75] or CLIP score [48] is also inadequate. It cannot simultaneously evaluate lowlevel physics like _“did the hand penetrate the cup?”_ and high-level semantics like _“did the agent pick up the correct cup?”_ . No reward model currently exists that can capture this multi-dimensional, hierarchical preference space. (ii) **The Algorithm Barrier (Optimization):** Even with a perfectly defined reward, how can we effectively optimize a flow-based video generation model—the dominant paradigm in current video generation research? While recent works have applied reinforcement learning to generative models [8, 45, 75], their focus has been almost exclusively on the diffusion-based paradigm. Furthermore, prior explorations of RL for world models have targeted different domains ( _e.g._ , gaming [29]) with simpler, task-specific rewards, rather than the complex, multi-dimensional requirements of embodied AI. Refining flow-based models [3] remains a critical yet unsolved problem. This is because standard policy gradient methods like PPO [53] rely on computing the log-likelihood term log _πθ_ ( _v|c_ ). However, for flowbased models, this computation is prohibitively expensive, as it involves an _O_ ( _d_<sup>2</sup> _· T_ ODE) integration over the Jacobian trace [45]. This computational bottleneck makes PPO-style optimization practically infeasible for high-resolution flow matching-based models [3]. 

To this end, we propose ReWorld, a new framework that systematically bridges both barriers through a multidimensional reward model and a flow-based world model optimization approach to align embodied world models with implicit physical realism. As shown in Fig. 1, we first construct a large-scale video preference dataset to capture human preference over physical realism, embodiment plausibility, and task semantics. Building upon this foundation, we introduce HERO (HiErarchical Reward mOdel), a multi-dimensional reward model. Its core innovation is multi-dimensional reward awareness: a decoupled, fourhead architecture to specialize in physical fidelity, embodiment plausibility, task completion, and visual quality, respectively. Critically, as shown in Fig. 2, each specialized head is strategically mapped to distinct feature levels of the InternVideo2 [67] backbone. The physical head ingests low-level, early-layer features to detect fine-grained violations, while the task head ingests deep, late-layer features to evaluate high-level semantic completion. Furthermore, to solve the “ _Algorithm Barrier_ ” problem, we introduce HERO-FPO (HERO-guided Flow Policy Optimization) that operationalizes the principles of Flow Policy Optimization (FPO) [45] for aligning high-resolution, flow-based embodied world models. Standard PPO is intractable for flow models, as computing log _πθ_ incurs an _O_ ( _d_<sup>2</sup> _· TODE_ ) cost. 

FPO’s Conditional Flow Matching (CFM)-Likelihood strategy resolves this by positing that log _πθ_ can be tractably proxied by _LCF M_ . This substitution reduces the updating complexity to _O_ ( _d_ ), enabling feasible application of RLHF to flow-based world models. Our contributions are summarized as follows: 

- We introduce ReWorld, a novel framework that improves physical realism, embodiment consistency, task success, and visual fidelity—bridging the long-standing gap between visually plausible and physically grounded embodied world models. 

- We collect a large-scale embodied preference dataset and introduce HERO, a hierarchical reward model specialized for enabling fine-grained physics understanding and highlevel semantic reasoning. 

- We propose HERO-FPO, which provides a Flow Policy Optimization for embodied video generation. 

For further evaluation, we introduce ReWorldBench, a new embodied benchmark specifically designed to quantify failures within the _Physics Uncanny Valley_ . Extensive experiments demonstrate that our proposed ReWorld achieves state-of-the-art results, demonstrating 15-25% improvements across all 4 HERO metrics and an 85%+ human preference rate over the baseline, proving it largely resolves the _Physics Uncanny Valley_ gap. 

## **2. Related Works** 

### **2.1. Embodied World Models and Video Generation** 

Embodied World Models (EWMs) [24, 27–29, 51] are foundational to robotic learning, offering a mechanism to learn world dynamics in a latent space for planning and policy learning. Recent advancements in large-scale video generation have pushed the capabilities of these models significantly [9, 31, 54, 62], culminating in high-fidelity, generalist world models capable of processing million-length videos [43] or simulating complex driving scenarios at an omniscient level [32, 39]. This trend includes flow-based EWMs like Cosmos [3] that generate controllable and visually rich dynamic scenes. Furthermore, significant research has focused on enhancing the controllability of video generation [17, 77, 80], enabling alignment with various inputs such as text [66, 70], motion [14], or depth [72]. 

However, despite their visual prowess, the training objectives for these models [3, 24] almost exclusively rely on pixel-level reconstruction losses ( _e.g._ , _L_ 2, _L_ 1, or LPIPS [78]). This objective, while effective for visual fidelity, is fundamentally physics-agnostic. It enforces visual similarity to ground-truth data but provides no explicit signal to penalize physically implausible events, kinematic impossibilities, or logical task failures. Even conditional models [14, 23, 65, 66, 69], while achieving semantic alignment, remain bound by this limitation, often producing visually 

2 


Figure 2. **Overview of the ReWorld framework** . (a) We employ a VLM-driven annotation system to generate the 4-dimensional embodied preference dataset. (b) Building upon this dataset, we train the multi-dimensional reward model HERO based on the hierarchical feature space of InternVideo2 [67]. (c) We detail the reinforcement learning pipeline HERO-FPO to refine the generative policy with the learned multi-dimensional reward signal. (d) We introduce ReWorldBench as a specialized benchmark to evaluate embodied world models. 

coherent videos where an agent’s hand penetrates an object or an object moves without being touched. In contrast to these Supervised Learning (SL) approaches, our ReWorld framework introduces a post-hoc RLHF pipeline, which explicitly optimizes for the multi-dimension. 

### **2.2. Reward Modeling for Vision and Robotics** 

The success of Reinforcement Learning from Human Feedback (RLHF) [16] in aligning LLMs [47, 82] has inspired its application in vision [8, 37]. These efforts have produced reward models (RMs) for aesthetic quality [52, 75], textimage alignment [36, 64], and general human preferences. These models, however, are typically monolithic, outputting a single scalar score that captures a high-level, holistic preference. In parallel, reward functions in robotics policy learning are often sparse, binary success signals [15, 46], or simple, hand-crafted heuristic functions ( _e.g._ , distanceto-goal or contact forces [4, 26, 59]). 

Neither of these signal types is suitable for refining EWMs. The monolithic signals from vision-RLHF [48, 75] are too coarse; they conflate visual aesthetics with physical correctness, while the sparse signals from robotics [15] are insufficient for generative models. To solve this, HERO introduces a multi-dimensional, decoupled reward to distinct feature levels, enabling the simultaneous evaluation of lowlevel physics and high-level semantics. 

### **2.3. Policy Optimization for Generative Models** 

Optimizing generative models via RL has been explored in GANs ( _e.g._ , RL-GAN [21], SeqGAN [76]) and VAEs [35]. 

More recently, optimizing diffusion models via RLHF [7, 37, 50, 71] has seen great success. These methods, including Direct Preference Optimization (DPO) [49], work because they leverage the tractable noise-prediction objective of diffusion models as a proxy for the likelihood [55]. In contrast, flow-based models [34, 42, 56, 57] are trained differently. To avoid the exact log-likelihood calculation, which requires computing the log-determinant of the Jacobian (a _O_ ( _d_<sup>2</sup> ) operation [13, 22]), SOTA models like Cosmos [3] adopt Flow Matching (CFM) [2, 42, 45]. CFM simplifies the training objective to a stable, tractable MSE loss, but it does not provide the log-likelihood. 

This creates a critical gap. While alternative RLbased generative frameworks like Generative Flow Networks (GFlowNets) [6], Generative Adversarial Imitation Learning (GAIL) [30], or Maximum Entropy RL [25] exist, the successful RLHF techniques from diffusion models [7] cannot be directly transferred. PPO-style optimization [53], which is foundational to Flow Policy Optimization (FPO) [45], requires the likelihood ratio _r_ ( _θ_ ) = _πθ/πold_ , which in turn requires log _πθ_ . Therefore, we introduce HERO-FPO, grounded the theoretical contribution: the CFM-Likelihood Proxy. This proxy is the first to establish that the tractable _LCF M_ (Eq. (7)) can serve as a principled proxy for log _πθ_ within a PPO update, making RLHF on flow models feasible for the first time. 

3 

## **3. Methodology** 

In this section, we detail ReWorld, a framework aimed to employ reinforcement learning to align the video-based embodied world models with physical realism, task completion capability, embodiment plausibility and visual quality. As illustrated in Fig. 1, we first construct a 4-dimensional (4D) video preference dataset, which serves as the foundation for defining “trustworthiness” (Sec. 3.1). We then introduce a multi-dimensional reward model trained on the aforementioned dataset (Sec. 3.2). Finally, we present a novel reinforcement learning algorithm to optimize flow-based video generation models (Sec. 3.3). 

### **3.1. The 4D Embodied Preference Dataset** 

To solve the “ _Reward Barrier_ ” problem, we first create a training signal that transcends simple, monolithic labels. Our primary objective is to formalize the complex and often conflicting principles of embodied interaction into orthogonal evaluation criteria. To this end, we define the 4- Dimensional embodied preference space _P_ = R<sup>4</sup> : 

1. **Physical Realism (** _Rphys_ **):** Adherence to physical laws ( _e.g._ , object permanence, collision, gravity). 

2. **Embodiment Plausibility (** _Rembod_ **):** Kinematic realism and smoothness of the agent’s motion. 

3. **Task Completion (** _Rtask_ **):** Logical and semantic alignment with the given instruction. 

4. **Visual Quality (** _Rvis_ **):** Standard visual fidelity, including photorealism and temporal coherence. 

To overcome the data scale bottleneck in RLHF, we employ a scalable VLM-driven annotation system. Specifically, we leverage the robust time-series understanding and structural output stability of GPT4o [1] as a highfidelity proxy for human evaluation. The VLM is prompted using a structured, information-theoretic template (Section X in Appendix) to produce a 4D score vector **s** = [ _sphys, stask, sembod, svis_ ] _∈_ [1 _,_ 6]<sup>4</sup> for each video in the RH20T [18] dataset. This approach enables the scalable generation of a 235 _K_ + preference dataset, a scale sufficient to overcome the data scarcity bottleneck that has hindered previous reward modeling efforts. 

Central to our approach is the dimension isolation strategy, which is grounded in the mutual information minimization principle. Rather than random pairing, our specialized sampler algorithmically searches for video pairs ( _vA, vB_ ) that serve as highly specific training signals. The pair selection is formulated as a constrained combinatorial optimization: maximize the score difference in one target dimension _k_ ( _i.e._ , _|s_<sup>_k_</sup> _A_<sup>_−sk_</sup> _B_<sup>_| > τ_) while simultaneously min-</sup> imizing the score difference in all other non-target dimensions _l̸_ = _k_ ( _i.e._ , _|s_<sup>_l_</sup> _A_<sup>_−sl_</sup> _B_<sup>_|<ϵ_).Theresultingdataset</sup> _D_ = _{_ ( _vA, vB, k_ ) _}_ provides a dimensional tag _k_ . This tag serves as the crucial decoupling signal, which enables the functionally specialized and interference-free learning 

of our reward model in the next stage. 

### **3.2. HERO: HiErarchical Reward mOdel** 

HERO is the multi-dimensional reward model to learn the preferences from our 4D dataset, which is designed to solve the “ _Reward Barrier_ ” by our decoupled, multi-dimensional principle. It is built upon InternVideo2 [67] and features a novel hierarchical reward awareness that strategically maps specialized reward heads to the backbone’s feature space. As detailed in Fig. 2(b), HERO employs four decoupled reward heads: _Rphys_ , _Rembod_ , _Rtask_ , and _Rvis_ , each specializing in one of the 4D dimensions defined in Sec. 3.1. This is crucial because it aligns the perceptual complexity required for each evaluation dimension with the corresponding semantic depth of the backbone’s features. 

The training objective for HERO should solve two distinct challenges simultaneously. First, we must enforce that each specialized head learns only its assigned dimension, preventing gradient interference from the others. Second, we must ensure all four heads output scores on a comparable numerical scale. To solve both challenges, we introduce two specialized loss components. The dimensional specificity loss ( _LD_ ), detailed in Sec. 3.2.1, addresses the first challenge by utilizing our dataset’s dimensional tags to train each head in isolation. The overall preference regularizer loss ( _LO_ ), detailed in Sec. 3.2.2, then addresses the second challenge by applying a loss to the final combined score, forcing all specialized heads onto a calibrated numerical scale. 

#### **3.2.1. The Dimensional Specificity Loss** 

The dimensional specificity loss _LD_ is the core objective that enforces functional specialization. It leverages the dimension-tagged pairs ( _vA, vB, k_ ) from our dataset to train each head only on its relevant preference signal. It is computed as a weighted and masked sum of the standard Bradley-Terry loss ( _LBT_ ) across the four dimensions: 


where the efficacy of this dimensional loss (Eq. (1)) hinges on two key components, dimensional mask ( **M** _k_ ) and adaptive weighting ( **W** _k_ ), which are derived from our 4D dataset to enforce specialized learning. **M** _k ∈{_ 0 _,_ 1 _}_ acts as a gradient gate, implementing our core Dimensional Isolation Principle. It is a binary mask that permits gradient flow if and only if the training pair’s VLM score difference in the target dimension _k_ exceeds a predefined margin _τ_ . This mechanism is critical for preventing gradient interference, as it ensures the specialized head _Rk_ trains only on unambiguous, dimension-specific signals. **W** _k_ then serves 

4 

as an information gain prior, forcing the model to prioritize these high-value signals. This weight is determined by two factors: (i) it scales proportionally with the preference magnitude ( **W** _k ∝|_ ∆ _sk|_ ), assigning higher influence to high-confidence pairs, and (ii) it is intentionally boosted for the high-purity, explicitly dimension-isolated pairs (from Sec. 3.1) to maximize learning efficiency on the most informative samples. 

#### **3.2.2. The Overall Preference Regularizer** 

The _LD_ objective successfully trains specialized heads, but it does not guarantee that their output scores are calibrated with one another. For example, _Rphys_ might learn to output scores in the range [0.1, 0.2] while _Rtask_ outputs in [1.0, 5.0]. If combined, _Rtask_ would completely dominate the final reward. The overall preference regularization _LO_ solves this score calibration problem. Instead of acting on individual heads, it is a Bradley-Terry loss computed on the final, combined scalar reward _Rtotal_ =<sup>�</sup> _k_<sup>_wkRk_:</sup> 


This loss serves as a general quality constraint, forcing all four specialized heads to learn to produce scores within a comparable and meaningful numerical range. 

Finally, the total loss _LHERO_ is formulated as a composite objective, combining both solutions: 

**Algorithm 1** HERO-FPO 

1: **Initialize:** Actor policy _πθ_ (Cosmos), Critic _Vψ_ , frozen Reward Model _RHERO_ , Old policy _πθold ← πθ_ . **Stage 1: Experience Collection** 2: **for** iteration _i_ = 1 _, . . . , N_ **do** 3: Sample batch of conditions _C_ = _{cj}_<sup>_B_</sup> _j_ =1<sup>from RH20T.</sup> 4: **for** each _cj ∈C_ **do** 5: Generate video _vj ∼ πθold_ ( _v | cj_ ) (using Cosmos). 6: Compute 4D rewards **R** 4 _D ← RHERO_ ( _vj, cj_ ) (using HERO). 7: Compute total scalar reward _Rj ←_<sup>�</sup> _k_<sup>_wkRk_.</sup> 8: Compute value _Vj ← Vψ_ ( _vj_ ). 9: Compute advantage _A_<sup>ˆ</sup> _j ← Rj − Vj_ . 10: Store trajectory _Tj_ = ( _vj, cj, Rj, A_<sup>ˆ</sup> _j_ ) into buffer _B_ . 11: **end for Stage 2: FPO Optimization** 12: **for** epoch _e_ = 1 _, . . . , K_ **do** 13: **for** ( _v, c, R, A_<sup>ˆ</sup> ) _∈B_ **do** 14: _# Compute ratio using CFM-Likelihood Proxy (Eq._ (7) _)_ 15: _r_ ( _θ_ ) _←_ exp( _LCF M_ ( _v_ ; _θold, c_ ) _− LCF M_ ( _v_ ; _θ, c_ )) 16: _L_ POLICY( _θ_ ) _←−_ min� _r_ ( _θ_ ) _A,_<sup>ˆ</sup> clip( _r_ ( _θ_ ) _,_ 1 _−ϵ,_ 1+ _ϵ_ ) _A_<sup>ˆ</sup> � 17: _L_ VALUE( _ψ_ ) _←_ ( _R − Vψ_ ( _v_ ))<sup>2</sup> 18: _L_ TOTAL _← L_ POLICY + _cvL_ VALUE 19: Update _θ, ψ_ via _∇L_ TOTAL 20: **end for** 21: **end for** 22: _πθold ← πθ_ 23: **end for** 


where _β_ heavily emphasizes specialization, while _LO_ provides robust calibration. The resulting HERO model is frozen upon convergence, and its combined, calibrated scalar output _R_ =<sup>�</sup> _k_<sup>_wkRk_isusedasthehigh-fidelity</sup> reward function in the HERO-FPO pipeline (Sec. 3.3). 

### **3.3. HERO-FPO: HERO-guided Flow Policy Optimization** 

The final stage, HERO-FPO, implements the core reinforcement learning pipeline to refine the generative policy _πθ_ using the multi-dimensional reward signal from our frozen HERO model. Our generative policy is the pre-trained Cosmos-2B/14B world model [3]. We first address the critical domain gap—the inherent mismatch between Cosmos’s general video priors and the contact-rich dynamics of embodied robotics. 

We perform a crucial intermediate supervised fine-tuning step on the Bridge V2 robotics dataset [63]. During the finetuning stage, driven solely by the standard CFM loss (without reward), it is essential to ensure that the baseline policy _πθold_ already possesses the necessary visual and dynamic consistency before the complexities of RL are introduced. This robust, domain-adapted model then serves as the policy baseline for our reinforcement learning phase, where HERO-FPO is strategically applied to solve the “ _Algorithm Barrier_ ” using our core theoretical contribution. 

#### **3.3.1. The CFM-Likelihood Proxy** 

The foundational challenge of applying PPO to a flowbased model _πθ_ is the “ _Algorithm Barrier_ ”: the calculation of the log-likelihood, log _πθ_ ( _v|c_ ), is computationally intractable for high-dimensional video, as it requires integrating the trace of the model’s Jacobian _fθ_ : 


To establish our proxy, we first formally define the _LCF M_ objective. The CFM loss, used to train the base model _πθ_ , is a tractable MSE objective. It is computed by taking the clean video _v_ , adding a random amount of noise _ϵ ∼N_ (0 _, I_ ) at a random noise level _σ_ , creating a noised video _vt_ = _v_ + _σϵ_ . The model _πθ_ is then tasked with predicting the original clean video _v_ given _vt_ , _σ_ , and _c_ . The loss is the weighted squared error between the model’s prediction and the ground truth: 


Our key insight, which we term the CFM-Likelihood Proxy, is that this loss value itself—a measure of how well the model can denoise _v_ —is a powerful proxy for likelihood. Intuitively, a low _LCF M_ (the model easily denoises 

5 

_v_ ) implies that _v_ is high log-likelihood. Conversely, a high _LCF M_ (the model struggles to denoise _v_ ) implies _v_ is low log-likelihood. This strong negative correlation forms the basis of our proxy: 


Crucially, the constant term _C_ ( _c_ ) depends only on the condition _c_ and cancels out during the PPO update. This substitution allows us to compute the PPO importance sampling ratio _r_ ( _θ_ ) = _πθ/πθold_ entirely in terms of tractable CFM losses. The log-ratio simplifies dramatically: 


This yields our final, computationally feasible update rule: 


This theoretical breakthrough is the core of HERO-FPO. It reduces the complexity of the PPO update from the impossible _O_ ( _d_<sup>2</sup> _· T_ ODE) to a highly efficient _O_ ( _d_ ), making highresolution video RLHF computationally feasible. 

#### **3.3.2. The HERO-FPO-PPO Training Framework** 

Grounded by our CFM-Likelihood Proxy, we define the complete FPO training loop which integrates our threemodel system: Actor ( _πθ_ ), Critic ( _Vψ_ ), and the frozen reward model ( _R_ ). 

The training process follows a standard PPO experience collection and optimization cycle (Algorithm 1). 

- **Actor (** _πθ_ **):** The Cosmos world model, responsible for generating rollouts ( _vj ∼ πθold_ ) and computing the policy loss via the CFM-Likelihood Proxy. 

- **Reward Model (** _R_ **):** The frozen HERO model (from Sec. 3.2), which provides the high-fidelity, multidimensional reward _Rj_ =<sup>�</sup> _k_<sup>_wkRk_.</sup> 

- **Critic (** _Vψ_ **):** A specialized VideoValueNetwork that learns to predict the expected reward _Vj ≈ E_ [ _Rj_ ], crucial for stabilizing the high-variance reward signal and computing the Advantage _A_<sup>ˆ</sup> _j_ = _Rj − Vj_ . The core of the optimization (Stage 2 in Algorithm 1) 

- uses the PPO clipped objective to update the Actor and Critic simultaneously: 


### **3.4. ReWorldBench: A Multi-Dimensional Benchmark for Embodied Reality** 

In this section, we introduce ReWorldBench, a specialized benchmark designed to evaluate embodied world models. We define the core evaluation task as conditional 

video generation from an initial image and a text instruction (Image+Text-to-Video), a setup that directly probes the model’s ability to understand a given state and execute a specified action. ReWorldBench not only provides metrics for visual quality but is also specifically designed to evaluate a model’s physical realism, task completion, and embodiment plausibility in embodied settings. 

#### **3.4.1. Evaluation Dimensions** 

- **Predictive Physical Reasoning (Probing** _Rphys_ **):** Evaluates the model’s adherence to core physical principles. Generated videos are assessed for violations in object permanence, collision dynamics, and gravitational realism, focusing on dynamic, contact-rich events. 

- **Logical and Task Planning (Probing** _Rtask_ **):** Evaluates the model’s logical and semantic adherence to the given instruction. Success is measured by whether the generated video performs the correct actions in the specified logical sequence, especially for complex or multi-step tasks. 

- **Kinematic Execution (Probing** _Rembod_ **):** Distinct from world physics, this evaluates the agent’s own motion realism. We assess the generated trajectories for kinematic correctness, smoothness, and continuity. 

- **Generative Fidelity (Probing** _Rvis_ **):** Evaluates the foundational generative quality of the model. We assess standard criteria: photorealism, absence of visual artifacts, and temporal consistency. 

#### **3.4.2. Task Design and Data Curation** 

The benchmark’s prompts are built upon the diverse scenarios within the RH20T [18] task set. To specifically probe the four dimensions, we leverage GPT-4o to systematically curate and expand the original instructions. We will provide the detailed illustrations in the supplementary material. 

#### **3.4.3. Evaluation Protocol** 

We employ a rigorous VLM as judge protocol built upon GPT-5, chosen for its advanced spatio-temporal and finegrained reasoning capabilities. The core of our protocol is a set of dimension-specific, Chain-of-Thought (CoT) evaluation templates. For each (video, prompt) pair, the template elicits a detailed textual rationale prior to requesting a numerical score (1-10) for each of the four dimensions. This rationale-first approach ensures the evaluation is interpretable, consistent, and grounded in specific evidence, mitigating the common VLM biases of ungrounded, holistic scoring. 

#### **3.4.4. Overall Benchmark Score** 

To provide a single, comprehensive metric for model comparison, we compute a final _SReW orld_ - _Bench_ score. The protocol involves first normalizing the raw scores from the four dimensions ( _Sphys, Stask, Sembod, Svis_ ), then combining them using a predefined weighting scheme. The final 

6 

Table 1. **Quantitative comparison on ReWorldBench.** The evaluation covers both visual fidelity and performance on embodied tasks. We highlight the best results in **bold** . 

||||**Video Quality**|||**4D Emb**|**odied Dimen**|**sions (1-10**|**Scale)**|**Overall**|
|---|---|---|---|---|---|---|---|---|---|---|
|**Model**|**FVD**(_↓_)|**SSIM**(_↑_)|**DINO Similarity**(_↑_)|**PSNR**(_↑_)|**DreamSim**(_↑_)|_Sphys_ (_↑_)|_Sembod_(_↑_)|_Stask_ (_↑_)|_Svis_ (_↑_)|_SReW orld_ (_↑_)|
|CogVideoX [74]|720|**0.70**|0.56|14.6|0.74|3.1|2.8|3.4|7.1|35.3|
|Wan2.1 [60]|510|0.61|0.59|14.1|0.74|3.4|3.1|3.8|7.3|38.6|
|Cosmos-Base [3]|281|0.63|0.62|15|0.74|4.2|3.9|4.4|7.0|44.7|
|Cosmos-SFT (Ours)|240|0.68|0.65|**16.1**|0.78|5.1|4.2|6.1|7.2|54.4|
|**ReWorld (Ours)**|**190**|0.66|**0.71**|15.2|**0.82**|**5.9**|**5.6**|**6.5**|**7.3**|**61.9**|


Table 2. **HERO reward model performance.** 

|**Overall Perfo**|**rmance**|**Per**|**-Dimension**|**Accuracy (Specializ**|**ation)**|
|---|---|---|---|---|---|
|Metric|Value|Head|Accuracy|Feature Source|Rank|
|Accuracy|**85.3%**|_Rembod_|**87.2%**|Mid-layer (L16)|1 (Best)|
|AUC|**0.901**|_Rvis_|84.6%|Final-pooled (L39)|2|
|Spearman (_ρ_)|**0.787**|_Rtask_|81.3%|Deep-layer (L32)|3|
|Kendall’s (_τ_)|**0.689**|_Rphys_|79.1%|Early-layer (L8)|4 (Hardest)|


aggregated score is mapped to a 0-100 scale and defined as: 

_SO_ = 0 _._ 4 _× Stask_ + 0 _._ 3 _× Sembod_ + 0 _._ 2 _× Sphys_ + 0 _._ 1 _× Svis._ (13) 

## **4. Experiments** 

Our evaluation of the ReWorld framework is structured into three primary analyses. We first detail our comprehensive experimental setup in Sec. 4.1. Sec. 4.2 then presents our main quantitative and qualitative results; this section begins by demonstrating the superiority of our full HEROFPO pipeline against SOTA baselines (Sec. 4.2.1) and subsequently validates the efficacy of the HERO reward model that enabled this alignment (Sec. 4.2.2). Finally, Sec. 4.3 provides comprehensive ablation studies to isolate and justify our critical design components. 

### **4.1. Experimental Setup** 

Our policy alignment is conducted on robotics tasks from the RH20T dataset [18], using provided initial condition frames. The reward function is our pre-trained, frozen HERO model, which is built on an InternVideo2-1B backbone [67]. HERO itself is trained on our novel 4D Embodied Preference Dataset ( _∼_ 235K pairs), which we generated from RH20T using GPT4o [5]. The policy model is the Cosmos-2B [3] world model, which we pre-finetune on the Bridge V2 dataset [63] to create our strong Cosmos-SFT baseline. The Critic ( _Vψ_ ) is a 4-layer 3D-CNN followed by a 2-layer MLP VideoValueNetwork trained from scratch. We compare our full ReWorld framework against CosmosSFT and other SOTA baselines, including CogVideoX [74], Wan2.1 [60], and the original Cosmos-Base [3]. 

All models are trained on 8 NVIDIA A100 GPUs using the AdamW optimizer. Detailed hyperparameters for both HERO training and HERO-FPO alignment, are provided in the supplementary material. Evaluation is twofold: (i) We assess HERO’s Accuracy, AUC, Spearman, and Kendall’s on the test set. (ii) We evaluate the generative models using standard metrics (FVD [61], SSIM [68], 

DINO Similarity [10], PSNR, DreamSim [19]) and our proposed ReWorld-Bench (Sec. 3.4). 

### **4.2. Main Experimental Results and Analysis** 

#### **4.2.1. World Model Alignment Performance** 

Tab. 1 presents our comprehensive comparison, benchmarking our full framework against all baselines across both standard visual quality metrics and our rigorous 4D ReWorldBench dimensions. As shown in Tab. 1, ReWorld remains competitive in standard visual metrics, confirming that our HERO-FPO alignment refines embodied behavior without sacrificing foundational visual fidelity. 

However, these standard metrics are physics-agnostic and fail to capture the _Physics Uncanny Valley_ . We thus evaluate all models on our rigorous ReWorldBench (Sec. 3.4), which probes the four dimensions of embodied intelligence. The results in Tab. 1 are definitive. While baselines (including our strong Cosmos-SFT) struggle with physical and logical coherence, our full ReWorld framework achieves dramatic improvements across all four embodied dimensions, especially in _Sphys_ and _Stask_ . This provides strong quantitative evidence that our HERO-FPO pipeline successfully closes the _Physics Uncanny Valley_ . 

**Qualitative Results.** We provide qualitative comparisons in Fig. 3. The visualizations clearly demonstrate the failures of baseline models, which directly correspond to their low _SReW orld_ scores. Baselines exhibit severe physical implausibility (CogVideoX), catastrophic visual artifacts and task failure (Wan 2.1), or unnatural kinematics (Cosmos-SFT). In stark contrast, our full ReWorld framework successfully generates a video that is physically, kinematically, and logically coherent, visually confirming its superior _SReW orld_ score. 

#### **4.2.2. HERO Reward Model Performance** 

To rigorously evaluate our HERO and validate its alignment with true human judgment, we constructed an expert-annotated test set. We sampled 300 videos from RH20T [18] dataset and had them meticulously annotated by 5 expert human volunteers, who used the exact 4D evaluation protocol (Sec. 3.4.1) to create a high-quality, humanvalidated preference dataset. 

As shown in Tab. 2, HERO achieves outstanding performance on this challenging expert-annotated test set. The 

7 


Figure 3. **Qualitative comparisons on ReWorldBench.** Our proposed ReWorld model achieves the best generative results for all the multi-dimensional metrics compared with the baseline video generation models. 

Table 3. **Ablation on core components of HERO reward model.** 

|**Model Variant**|**Accuracy**|**Drop (**∆**)**|
|---|---|---|
|**HERO (Full Model)**|**85.3%**|**–**|
|_A. Removing Reward Heads:_|||
|w/o_Rtask_ (Alignment)|70.1%|-15.2%|
|w/o_Rembod_(Execution)|73.5%|-11.8%|
|w/o_Rphys_ (Plausibility)|75.8%|-9.5%|
|w/o_Rvis_ (Fidelity)|79.2%|-6.1%|
|_B. Loss Function Components:_|||
|w/o_LD_ (Dimensional Loss, only_LO_)|65.4%|-19.9%|
|w/o_LO_ (Calibration Loss, only_LD_)|75.1%|-10.2%|
|_LHERO_ (Equal Weights)|81.7%|-3.6%|
|_C. Feature Mapping:_|||
|w/o Hierarchical Map (Use Final Layer)|72.8%|-12.5%|


results confirm HERO learns a strong, generalizable preference signal that successfully transfers from our large-scale VLM training data. Furthermore, the model demonstrates clear functional specialization, with all four heads achieving high accuracy. This validates our hierarchical design (Sec. 3.2) and proves its capability as a reliable, multidimensional reward function for the FPO alignment stage. 

### **4.3. Ablation Study** 

**HERO Reward Model.** Tab. 3 presents the ablation results for the core components of the HERO. The results indicate that all three design pillars are essential for performance. The most critical component is our Dimensional Specificity Loss ( _LD_ ), as removing it causes a catastrophic 19.9% drop in accuracy. Our _Hierarchical Reward Awareness_ hypothesis (Sec. 3.2) is also strongly validated, as reverting to a naive final-layer feature map degrades performance by 12.5%. Furthermore, all four heads prove to be 

Table 4. **Ablation on the HERO-FPO alignment framework.** 

|**FPO Variant**|_SReW orld_|**Drop (**∆**)**|
|---|---|---|
|**ReWorld (Full Model)**|**61.9**|**–**|
|_A. Core Algorithm:_|||
|w/o CFM-Likelihood Surrogate (use Reward-L2 Loss)|55.1|-6.8|
|w/ PPO (use_LCF M_ aslog_π_proxy, wrong sign)|37.8|-24.1|
|_B. Reward Components:_|||
|FPO (only_Rphys_ +_Rembod_)|49.2|-12.7|
|FPO (Only_Rtask_ +_Rvis_)|51.3|-10.6|
|FPO (Equal Reward Weights)|58.2|-3.7|
|_C. CFM Sampler:_|||
|CFM (_N_ = 1Sample)|56.9|-5.0|
|CFM (_N_ = 10Samples)|60.8|-1.1|


necessary, with the _Rtask_ head being the most impactful, whose removal results in a 15.2% accuracy loss. These results validate that HERO’s high performance stems from the synergistic design of its hierarchical architecture and its specialized, composite loss function. 

**HERO-FPO.** Tab. 4 presents the ablation results for our HERO-FPO alignment framework. The results confirm that the CFM-Likelihood Proxy (Sec. 3.3) is the most critical component. Replacing this proxy with a naive rewardweighted _L_ 2 loss, or incorrectly using the _LCF M_ value as a direct log _π_ proxy, causes a catastrophic performance collapse of 24.1 points. This validates that our principled proxy (Eq. (7)) is essential for stable policy optimization. Furthermore, the multi-dimensional reward signal is proven vital; ablating the physics and embodiment heads results in a (- 12.7 points) loss, confirming these dimensions are key to closing the _Physics Uncanny Valley_ . Finally, our choice of _N_ = 5 samples for the CFM sampler is validated as a robust trade-off, as using only _N_ = 1 sample degrades performance by 5 points due to high variance, while increasing 

8 

to _N_ = 10 offers no significant benefit . 

## **5. Conclusion and Future Work** 

In this paper, we propose ReWorld, a new framework for aligning embodied world models by systemically resolving the core reward and algorithm barriers in video RLHF. It introduces HERO, a multi-dimensional reward model with hierarchical reward awareness to solve the reward challenge, and enables HERO-FPO, a tractable PPO algorithm grounded in our CFM-likelihood proxy theory to solve the optimization challenge. This integration delivers state-ofthe-art performance compared with previous methods. **Future Work.** Future works include model compression and more sample-efficient policy optimization strategies. 

## **References** 

- [1] Josh Achiam, Steven Adler, Shreya Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam An, ..., and Barton McGrew. GPT4 Technical Report, 2023. 4 

- [2] Michael S Albergo, Nicholas M Boffi, and Eric VandenEijnden. Stochastic interpolants: A unifying framework for flows and diffusions. _arXiv preprint arXiv:2303.08797_ , 2023. 3 

- [3] H. A. Alhaija, J. Alvarez, M. Bala, T. Cai, T. Cao, L. Cha, et al. Cosmos-transfer1: Conditional world generation with adaptive multimodal control. _arXiv preprint arXiv:2503.14492_ , 2025. 1, 2, 3, 5, 7 

- [4] Yusuf Aytar, Tobias Pfaff, David Budden, Tom Paine, Ziyu Wang, and Nando De Freitas. Playing hard exploration games by watching youtube. In _Advances in neural information processing systems_ , 2018. 3 

- [5] S. Bai, K. Chen, X. Liu, J. Wang, W. Ge, S. Song, et al. Qwen2.5-vl technical report. _arXiv preprint arXiv:2502.13923_ , 2025. 7 

- [6] Yoshua Bengio, Salem Lahlou, Tristan Deleu, Edward J. Hu, Moksh Tiwari, and Emmanuel Bengio. Gflownet foundations. _Journal of Machine Learning Research_ , 24(210):1–55, 2023. 3 

- [7] Kevin Black, Michael Janner, Yilun Du, Ilya Kostrikov, and Sergey Levine. Training diffusion models with reinforcement learning. _arXiv preprint arXiv:2305.13301_ , 2023. 3 

- [8] Tim Brooks, Aleksander Holynski, and Alexei A Efros. Instructpix2pix: Learning to follow image editing instructions. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 18392–18402, 2023. 1, 2, 3 

- [9] Tim Brooks, Bill Peebles, Connor Holmes, Will DePue, Yufei Guo, and OpenAI. Video generation models as world simulators. Technical report, OpenAI, 2024. Sora. 1, 2 

- [10] Mathilde Caron, Hugo Touvron, Ishan Misra, H´erve J´egou, Julien Mairal, Piotr Bojanowski, and Armand Joulin. Emerging properties in self-supervised vision transformers. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 9650–9660. IEEE, 2021. 7 

- [11] Jun Cen, Chaohui Yu, Hangjie Yuan, Yuming Jiang, Siteng Huang, Jiayan Guo, Xin Li, Yibing Song, Hao Luo, Fan Wang, et al. Worldvla: Towards autoregressive action world model. _arXiv preprint arXiv:2506.21539_ , 2025. 1 

- [12] Akshay L Chandra, Iman Nematollahi, Chenguang Huang, Tim Welschehold, Wolfram Burgard, and Abhinav Valada. Diwa: Diffusion policy adaptation with world models. _arXiv preprint arXiv:2508.03645_ , 2025. 1 

- [13] Ricky T. Q. Chen, Yulia Rubanova, Jesse Bettencourt, and David K. Duvenaud. Neural ordinary differential equations. In _Advances in neural information processing systems_ , 2018. 3 

- [14] W. Chen, J. Wu, P. Xie, H. Wu, J. Li, X. Xia, et al. Controla-video: Controllable text-to-video generation with diffusion models. _CoRR_ , 2023. 1, 2 

- [15] Xiaowei Chi, Peidong Jia, Chun-Kai Fan, Xiaozhu Ju, Weishi Mi, Kevin Zhang, Zhiyuan Qin, Wanxin Tian, Kuangzhi Ge, Hao Li, et al. Wow: Towards a world omniscient world model through embodied interaction. _arXiv preprint arXiv:2509.22642_ , 2025. 1, 2, 3 

- [16] Paul F Christiano, Jan Leike, Tom Brown, Miljan Martic, Shane Legg, and Dario Amodei. Deep reinforcement learning from human preferences. In _Advances in neural information processing systems_ , 2017. 1, 3 

- [17] Patrick Esser, John Chiu, Parmida Atighehchian, Jonathan Granskog, and Anastasios Germanidis. Structure and content-guided video synthesis with diffusion models. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 7346–7356, 2023. 2 

- [18] Hao-Shu Fang, Hongjie Fang, Zhenyu Tang, Jirong Liu, Chenxi Wang, Junbo Wang, Haoyi Zhu, and Cewu Lu. Rh20t: A comprehensive robotic dataset for learning diverse skills in one-shot, 2023. 4, 6, 7 

- [19] S. Fu, N. Tamir, S. Sundaram, L. Chai, R. Zhang, T. Dekel, and P. Isola. DreamSim: Learning new dimensions of human visual similarity using synthetic data. _arXiv preprint arXiv:2306.09344_ , 2023. 7 

- [20] Xiao Fu, Xintao Wang, Xian Liu, Jianhong Bai, Runsen Xu, Pengfei Wan, Di Zhang, and Dahua Lin. Learning video generation for robotic manipulation with collaborative trajectory control. _arXiv preprint arXiv:2506.01943_ , 2025. 1 

- [21] Ian J Goodfellow, Jean Pouget-Abadie, Mehdi Mirza, Bing Xu, David Warde-Farley, Sherjil Ozair, ..., and Yoshua Bengio. Generative adversarial nets. In _Advances in neural information processing systems_ , 2014. 3 

- [22] Will Grathwohl, Ricky TQ Chen, Jesse Bettencourt, Ilya Sutskever, and David Duvenaud. Ffjord: Free-form continuous dynamics for scalable reversible generative models. _arXiv preprint arXiv:1810.01367_ , 2018. 3 

- [23] Yuwei Guo, Ceyuan Yang, Anyi Rao, Zhaojie Liang, Yaohui Wang, Yu Qiao, ..., and B. Dai. Animatediff: Animate your personalized text-to-image diffusion models without specific tuning. _arXiv preprint arXiv:2307.04725_ , 2023. 2 

- [24] David Ha and J¨urgen Schmidhuber. World models. _arXiv preprint arXiv:1803.10122_ , 2018. 1, 2 

- [25] Tuomas Haarnoja, Aurick Zhou, Pieter Abbeel, and Sergey Levine. Soft actor-critic: Off-policy maximum entropy deep 

9 

reinforcement learning with a stochastic actor. In _International conference on machine learning_ , pages 1861–1870. PMLR, 2018. 3 

- [26] Dylan Hadfield-Menell, Smitha Milli, Pieter Abbeel, Stuart J Russell, and Anca Dragan. Inverse reward design. In _Advances in neural information processing systems_ , 2017. 3 

- [27] Danijar Hafner, Timothy Lillicrap, Ian Fischer, Ruben Villegas, David Ha, Honglak Lee, and James Davidson. Learning latent dynamics for planning from pixels. In _International conference on machine learning_ , pages 2555–2565. PMLR, 2019. 2 

- [28] Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. Dream to control: Learning behaviors by latent imagination. In _International Conference on Learning Representations (ICLR)_ , 2020. 

- [29] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains through world models. _arXiv preprint arXiv:2301.04104_ , 2023. 1, 2 

- [30] Jonathan Ho and Stefano Ermon. Generative adversarial imitation learning. In _Advances in neural information processing systems_ , 2016. 3 

- [31] Jonathan Ho, Tim Salimans, Alexey Gritsenko, William Chan, Mohammad Norouzi, and David J Fleet. Video diffusion models. In _Advances in neural information processing systems_ , pages 8633–8646, 2022. 2 

- [32] Anthony Hu, Lloyd Russell, Hudson Yeo, Zak Murez, George Fedoseev, Alex Kendall, et al. Gaia-1: A generative world model for autonomous driving. _arXiv preprint arXiv:2309.17080_ , 2023. 2 

- [33] Yucheng Hu, Yanjiang Guo, Pengchao Wang, Xiaoyu Chen, Yen-Jen Wang, Jianke Zhang, Koushil Sreenath, Chaochao Lu, and Jianyu Chen. Video prediction policy: A generalist robot policy with predictive visual representations. _arXiv preprint_ , 2024. 1 

- [34] Diederik P Kingma and Prafulla Dhariwal. Glow: Generative flow with invertible 1x1 convolutions. In _Advances in neural information processing systems_ , 2018. 3 

- [35] Diederik P Kingma and Max Welling. Auto-encoding variational bayes. _arXiv preprint arXiv:1312.6114_ , 2013. 3 

- [36] Yuval Kirstain, Adam Polyak, Uriel Singer, Shahar Matiana, Joe Penna, and Omer Levy. Pick-a-pic: An open dataset of user preferences for text-to-image generation. In _Advances in neural information processing systems_ , pages 36652–36663, 2023. 3 

- [37] Kimin Lee, Hao Liu, Moonkyung Ryu, Olivia Watkins, Yuqing Du, Craig Boutilier, ..., and Shixiang S Gu. Aligning text-to-image models using human feedback. _arXiv preprint arXiv:2302.12192_ , 2023. 3 

- [38] Bohan Li, Jiazhe Guo, Hongsi Liu, Yingshuang Zou, Yikang Ding, Xiwu Chen, Hu Zhu, Feiyang Tan, Chi Zhang, Tiancai Wang, et al. Uniscene: Unified occupancy-centric driving scene generation. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 11971–11981, 2025. 1 

- [39] B. Li, Z. Ma, D. Du, B. Peng, Z. Liang, Z. Liu, et al. Omninwm: Omniscient driving navigation world models. _arXiv preprint arXiv:2510.18313_ , 2025. 2 

- [40] Hengtao Li, Pengxiang Ding, Runze Suo, Yihao Wang, Zirui Ge, Dongyuan Zang, Kexian Yu, Mingyang Sun, Hongyin Zhang, Donglin Wang, et al. Vla-rft: Vision-language-action reinforcement fine-tuning with verified rewards in world simulators. _arXiv preprint arXiv:2510.00406_ , 2025. 1 

- [41] Yue Liao, Pengfei Zhou, Siyuan Huang, Donglin Yang, Shengcong Chen, Yuxin Jiang, Yue Hu, Jingbin Cai, Si Liu, Jianlan Luo, et al. Genie envisioner: A unified world foundation platform for robotic manipulation. _arXiv preprint arXiv:2508.05635_ , 2025. 1 

- [42] Yaron Lipman, Ricky TQ Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le. Flow matching for generative modeling. _arXiv preprint arXiv:2210.02747_ , 2022. 3 

- [43] Hui Liu, Wang Yan, Matei Zaharia, and Pieter Abbeel. World model on million-length video and language with blockwise ringattention. _arXiv preprint arXiv:2402.08268_ , 2024. 2 

- [44] Shaowei Liu, Zhongzheng Ren, Saurabh Gupta, and Shenlong Wang. Physgen: Rigid-body physics-grounded imageto-video generation. In _European Conference on Computer Vision_ , pages 360–378. Springer, 2024. 1 

- [45] David McAllister, Song Ge, B. Yi, C. M. Kim, E. Weber, H. Choi, et al. Flow matching policy gradients. _arXiv preprint arXiv:2507.21053_ , 2025. 2, 3 

- [46] Oier Mees, Lukas Hermann, Erick Rosete-Beas, and Wolfram Burgard. Calvin: A benchmark for languageconditioned policy learning for long-horizon robot manipulation tasks. _IEEE Robotics and Automation Letters_ , 7(3): 7327–7334, 2022. 3 

- [47] Long Ouyang, Jeff Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, et al. Training language models to follow instructions with human feedback. In _Advances in neural information processing systems_ , pages 27730–27744, 2022. 3 

- [48] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, et al. Learning transferable visual models from natural language supervision. In _International conference on machine learning_ , pages 8748–8763. PMLR, 2021. 2, 3 

- [49] Rafael Rafailov, Archit Sharma, Eric Mitchell, Christopher D Manning, Stefano Ermon, and Chelsea Finn. Direct preference optimization: Your language model is secretly a reward model. In _Advances in neural information processing systems_ , pages 53728–53741, 2023. 3 

- [50] A Z Ren, J Lidard, L L Ankile, A Simeonov, P Agrawal, A Majumdar, ..., and M Simchowitz. Diffusion policy policy optimization. _arXiv preprint arXiv:2409.00588_ , 2024. 3 

- [51] Julian Schrittwieser, Ioannis Antonoglou, Thomas Hubert, Karen Simonyan, Laurent Sifre, Simon Schmitt, et al. Mastering atari, go, chess and shogi by planning with a learned model. _Nature_ , 588(7839):604–609, 2020. 2 

- [52] Christoph Schuhmann, Romain Beaumont, Richard Vencu, Cade Gordon, Ross Wightman, Mehdi Cherti, ..., and Jenia Jitsev. Laion-5b: An open large-scale dataset for training next generation image-text models. In _Advances in neural information processing systems_ , pages 25278–25294, 2022. 3 

10 

- [53] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 2, 3 

- [54] Uriel Singer, Adam Polyak, Thomas Hayes, Xi Yin, Jie An, Songyang Zhang, ..., and Yaniv Taigman. Make-a-video: Text-to-video generation without text-video data. _arXiv preprint arXiv:2209.14792_ , 2022. 2 

- [55] Jiaming Song, Chenlin Meng, and Stefano Ermon. Denoising diffusion implicit models. _arXiv preprint arXiv:2010.02502_ , 2020. 3 

- [56] Yang Song, Jascha Sohl-Dickstein, Diederik P Kingma, Abhishek Kumar, Stefano Ermon, and Ben Poole. Score-based generative modeling through stochastic differential equations. _arXiv preprint arXiv:2011.13456_ , 2020. 3 

- [57] Yang Song, Prafulla Dhariwal, Mark Chen, and Ilya Sutskever. Consistency models. In _Proceedings of the 40th International Conference on Machine Learning (ICML’23)_ , pages 32211–32252. PMLR, 2023. 3 

- [58] Richard S Sutton, Andrew G Barto, et al. _Reinforcement learning: An introduction_ . MIT press Cambridge, 1998. 1 

- [59] Chen Tang, Ben Abbatematteo, Jiaheng Hu, Rohan Chandra, Roberto Mart´ın-Mart´ın, and Peter Stone. Deep reinforcement learning for robotics: A survey of real-world successes. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , pages 28694–28698, 2025. 3 

- [60] Team Wan. Wan: Open and advanced large-scale video generative models, 2025. 7 

- [61] Thomas Unterthiner, Sjoerd van Steenkiste, Karol Kurach, Raphael Marinier, Marcin Michalski, and Sylvain Gelly. Towards accurate generative models of video: A new metric & challenges, 2019. 7 

- [62] Ruben Villegas, Mohammad Babaeizadeh, Pieter-Jan Kindermans, Hernan Moraldo, Han Zhang, Mohammad Taghi Saffar, ..., and Dumitru Erhan. Phenaki: Variable length video generation from open domain textual description. _arXiv preprint arXiv:2210.02399_ , 2022. 2 

- [63] Homer R Walke, Kevin Black, Tony Z Zhao, Quan Vuong, Chongyi Zheng, P Hansen-Estruch, Abraham Lee, Moo Jin Kim, Max Du, Andre He, Vivek Myers, Kuan Fang, Chelsea Finn, and Sergey Levine. Bridgedata v2: A dataset for robot learning at scale. In _Conference on Robot Learning_ , pages 1723–1736. PMLR, 2023. 5, 7 

- [64] Bram Wallace, Meihui Dang, R Rafailov, L Zhou, A Lou, S Purushwalkam, ..., and N Naik. Diffusion model alignment using direct preference optimization. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 8228–8238, 2024. 3 

- [65] Weimin Wang, Jiawei Liu, Zhixin Lin, Jun Yan, S. Chen, C. Low, ..., and Jiashi Feng. Magicvideo-v2: Multistage high-aesthetic video generation. _arXiv preprint arXiv:2401.04468_ , 2024. 2 

- [66] Xiang Wang, Hang Yuan, Shiwei Zhang, Dayou Chen, Jiuni Wang, Ying Zhang, et al. Videocomposer: Compositional video synthesis with motion controllability. In _Advances in Neural Information Processing Systems_ , pages 7594–7611, 2023. 1, 2 

- [67] Yi Wang, K. Li, X. Li, J. Yu, Y. He, G. Chen, et al. Internvideo2: Scaling foundation models for multimodal video understanding. In _European Conference on Computer Vision_ , pages 396–416. Springer Nature Switzerland, 2024. 2, 3, 4, 

   - 7 

- [68] Zhou Wang, Alan C. Bovik, Hamid R. Sheikh, and Eero P. Simoncelli. Image quality assessment: from error visibility to structural similarity. _IEEE transactions on image processing_ , 13(4):600–612, 2004. 7 

- [69] Zhouxia Wang, Ziyang Yuan, Xintao Wang, Yaowei Li, Tianshui Chen, Menghan Xia, Ping Luo, and Ying Shan. Motionctrl: A unified and flexible motion controller for video generation. In _ACM SIGGRAPH 2024 Conference Papers_ , pages 1–11, 2024. 2 

- [70] Jay Zhangjie Wu, Yixiao Ge, Xintao Wang, Weixian Lei, Yuchao Gu, Yufei Shi, Wynne Hsu, Ying Shan, Xiaohu Qie, and Mike Zheng Shou. Tune-a-video: One-shot tuning of image diffusion models for text-to-video generation, 2023. 2 

- [71] Jiazheng Xu, Xiao Liu, Yuxuan Wu, Yuxin Tong, Qinkai Li, Ming Ding, Jiahui Tang, and Yixuan Dong. Imagereward: Learning and evaluating human preferences for textto-image generation. In _Advances in Neural Information Processing Systems_ , pages 15903–15935, 2023. 3 

- [72] Shuai Yang, Yifan Zhou, Zeyu Liu, and Chen Change Loy. Rerender a video: Zero-shot text-guided video-to-video translation. In _SIGGRAPH Asia 2023 Conference Papers_ , pages 1–11, 2023. 2 

- [73] Xiuyu Yang, Bohan Li, Shaocong Xu, Nan Wang, Chongjie Ye, Chen Zhaoxi, Minghan Qin, Ding Yikang, Xin Jin, Hang Zhao, and Hao Zhao. Orv: 4d occupancy-centric robot video generation. _arXiv preprint arXiv:2506.03079_ , 2025. 1 

- [74] Zhuoyi Yang, Jiayan Teng, Wendi Zheng, Ming Ding, Shiyu Huang, Jiazheng Xu, Yuanming Yang, Wenyi Hong, Xiaohan Zhang, Guanyu Feng, Da Yin, Yuxuan Zhang, Weihan Wang, Yean Cheng, Bin Xu, Xiaotao Gu, Yuxiao Dong, and Jie Tang. Cogvideox: Text-to-video diffusion models with an expert transformer, 2025. 7 

- [75] J. Ye, F. Liu, Q. Li, Z. Wang, Y. Wang, X. Wang, et al. Dreamreward: Text-to-3d generation with human preference. In _European Conference on Computer Vision_ , pages 259–276. Springer Nature Switzerland, 2024. 1, 2, 3 

- [76] Lantao Yu, Weinan Zhang, Jun Wang, and Yong Yu. Seqgan: Sequence generative adversarial nets with policy gradient. In _Proceedings of the AAAI conference on artificial intelligence_ , 2017. 3 

- [77] Lvmin Zhang, Anyi Rao, and Maneesh Agrawala. Adding conditional control to text-to-image diffusion models. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 3836–3847, 2023. 2 

- [78] Richard Zhang, Phillip Isola, Alexei A Efros, Eli Shechtman, and Oliver Wang. The unreasonable effectiveness of deep features as a perceptual metric. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 586–595, 2018. 2 

- [79] Wenyao Zhang, Hongsi Liu, Zekun Qi, Yunnan Wang, Xinqiang Yu, Jiazhao Zhang, Runpei Dong, Jiawei He, Fan Lu, He Wang, et al. Dreamvla: a vision-language-action 

11 

model dreamed with comprehensive world knowledge. _arXiv preprint arXiv:2507.04447_ , 2025. 1 

- [80] Yabo Zhang, Yuxiang Wei, Dongsheng Jiang, Xiaopeng Zhang, Wangmeng Zuo, and Qi Tian. Controlvideo: Training-free controllable text-to-video generation. _arXiv preprint arXiv:2305.13077_ , 2023. 2 

- [81] Haoyu Zhen, Qiao Sun, Hongxin Zhang, Junyan Li, Siyuan Zhou, Yilun Du, and Chuang Gan. Tesseract: learning 4d embodied world models. _arXiv preprint arXiv:2504.20995_ , 2025. 1 

- [82] Daniel M Ziegler, Nissan Stiennon, Jeffrey Wu, Tom B Brown, Alec Radford, Dario Amodei, ..., and Geoffrey Irving. Fine-tuning language models from human preferences. _arXiv preprint arXiv:1909.08593_ , 2019. 3 

12 

