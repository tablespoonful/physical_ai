---
title: "EnsembleVLA: Ensemble Learning for Vision-Language Action Models"
date: "2026"
venue: "ICML 2026"
url: https://proceedings.mlr.press/v306/song26e.html
pdf: https://raw.githubusercontent.com/mlresearch/v306/main/assets/song26e/song26e.pdf
converter: pymupdf4llm
---

> **[PDF を開く](https://raw.githubusercontent.com/mlresearch/v306/main/assets/song26e/song26e.pdf)** / [論文ページ](https://proceedings.mlr.press/v306/song26e.html)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **EnsembleVLA: Ensemble Learning for Vision-Language Action Models** 

**Mingchen Song**<sup>1 2</sup> **Xiang Deng**<sup>_†_1 3</sup> **Jie Wei**<sup>1</sup> **Dongmei Jiang**<sup>_†_2</sup> **Liqiang Nie**<sup>1</sup> **Weili Guan**<sup>_†_1 3</sup> 

## **Abstract** 

Diverse Vision-language-action (VLA) models have been proposed and demonstrated remarkable capabilities in robotic manipulation. However, how to effectively ensemble VLAs to further enhance performance remains largely unexplored, as conventional ensemble techniques designed for discriminative tasks cannot be directly applied to generative action policies with highdimensional, multimodal distributions. To address this challenge, we propose **EnsembleVLA** , an energy-based framework that enables principled ensemble of diverse VLA models. We establish a unified theoretical framework showing that both diffusion-based and flow-based VLA models can be formulated as energy-based models, where additive energy combination naturally induces policy composition at the distribution level. This theoretical foundation enables multiple pre-trained policies to be seamlessly aggregated into a stronger ensemble policy. Building upon this compositional framework, EnsembleVLA further incorporates learnable composition weights for dynamic policy balancing, coupled with a confidence-aware gating mechanism that adaptively modulates bounded residual corrections, collectively ensuring stable and robust task execution. Extensive experiments demonstrate that EnsembleVLA achieves competitive performance across various tasks in both simulated and real-world environments. 

## **1. Introduction** 

_Two heads are better than one._ 

#### _— English proverb_ 

> †Corresponding Author. 1Harbin Institute of Technology (Shenzhen), Shenzhen, China<sup>2</sup> PengCheng Laboratory, Shenzhen, China 

> 3Shenzhen Loop Area Institute, Shenzhen, China. Correspondence to: Xiang Deng _<_ dengxiang@hit.edu.cn _>_ , Dongmei Jiang _<_ jiangdm@pcl.ac.cn _>_ , Weili Guan _<_ honeyguan@gmail.com _>_ . 

_Proceedings of the 43_<sup>_rd_</sup> _International Conference on Machine Learning_ , Seoul, South Korea. PMLR 306, 2026. Copyright 2026 by the author(s). 


_Figure 1._ **Energy-Based Ensemble Policy.** To compose diverse weak policies into a stronger policy, we first establish a unified energy-based framework to ensemble VLAs at the distribution level, and further incorporate ensemble refinement to refine the composed actions. 

Vision-Language-Action (VLA) models represent a transformative paradigm in embodied AI (Qu et al., 2025; Wen et al., 2025; Kim et al., 2024; Song et al., 2025a), enabling robotic systems to jointly reason over visual perception, language understanding, and physical action generation. Methods such as DP (Chi et al., 2025), DP3 (Ze et al., 2024), OpenVLA-oft (Kim et al., 2025), _π_ 0 (Black et al., 2024), and _π_ 0 _._ 5 (Intelligence et al., 2025) have emerged as dominant frameworks by leveraging robot demonstration data and advanced generative backbones. Compared to conventional modular pipelines that decouple perception, planning, and control (Hermans et al., 2013), VLA models demonstrate remarkable proficiency in understanding complex multimodal environments and executing precise actions through end-toend learning. Their capabilities span a broad spectrum of tasks, from elementary pick-and-place (Jiang et al., 2023) operations to intricate long-horizon manipulation requiring sophisticated reasoning (Li et al., 2025a; Zhao et al., 2025; Xian et al., 2023). 

Although current VLA models have demonstrated remarkable capabilities in robotic manipulation (Duan et al., 2024; Li et al., 2024; Team et al., 2024; Wang et al., 2025; Zhang et al., 2025b; Li et al., 2023; Cen et al., 2025; Ma et al., 2024; Yang et al., 2025; Song et al., 2026), they still exhibit performance limitations on certain challenging tasks. This limitation motivates an interesting question: _Can we ensemble multiple VLA models to achieve capabilities beyond any single model?_ Ensemble learning (Yang et al., 2023; Dong et al., 2020), which aggregates predictions from multiple 

1 

**EnsembleVLA: Ensemble Learning for Vision-Language Action Models** 

models, has proven highly effective in discriminative tasks such as image classification. It offers a principled framework for leveraging the complementary strengths of diverse models. However, extending ensemble methods to VLAs remains non-trivial, primarily due to the high-dimensional action space and the inherently multimodal nature of action distributions. 

Motivated by this limitation, we draw inspiration from Energy-Based Models (EBMs) (LeCun et al., 2006; Hinton, 2002) and propose **EnsembleVLA** . As illustrated in Figure 1, our fundamental insight is to formulate individual VLA policies as independent energy functions. Grounded in EBMs theory, we observe that the summation of energy functions mathematically corresponds to the product of their underlying probability distributions (Du et al., 2020; 2023; Guo et al., 2023; Yoon et al., 2024). This perspective enables us to systematically synthesize multiple policies into an ensemble policy that effectively captures the complementary strengths of each base policy. 

Specifically, we first establish an elegant theoretical unification of diffusion-based and flow-based VLA models. Although these two paradigms operate through distinct generative mechanisms, where diffusion models rely on stochastic differential equations (Song et al., 2020b; Zhao et al., 2022) and flow matching employs deterministic ordinary differential equations (Lipman et al., 2022; Li et al., 2025b), we derive that both can be formulated within a unified energybased framework. Under this framework, the score function in diffusion models and the velocity field in flow matching both correspond to the negative gradient of an energy function. This theoretical equivalence provides a principled foundation for composing multiple policies at the distribution level, thereby enabling principled ensembling of diverse pre-trained VLA models. 

Building upon the composed action distribution, we further refine the composed actions through two complementary mechanisms. First, we introduce learnable composition weights that adaptively assign importance to base policies, enabling flexible policy balancing based on task requirements. Second, we design a confidence-aware gating mechanism consisting of a Delta-Net that predicts fine-grained residual corrections and a Gate-Net that estimates refinement confidence. To ensure stable and robust task execution, we introduce a conservative optimization strategy that selectively activates bounded residual corrections guided by confidence-aware gating signals. This design enables the ensemble to leverage complementary strengths of individual base policies while compensating for their weaknesses. 

Our main contributions can be summarized as follows: 

- To unlock the potential of combining diverse pretrained VLA models, we propose EnsembleVLA, a novel 

- framework grounded in ensemble learning principles. By treating diverse pretrained VLA models as base learners, our approach leverages energy-based model theory to aggregate them into a stronger, unified policy. 

- To enable principled composition across diffusionbased and flow-based VLAs, we establish an elegant theoretical unification of the two paradigms. By demonstrating the mathematical connections among score functions, velocity fields, and energy gradients, we provide a foundation for ensembling diverse VLA models within a unified energy-based framework. 

- To further refine the composed actions, EnsembleVLA employs learnable weighting coefficients to dynamically balance the contribution of each base policy, along with a confidence-aware gating module for bounded residual refinements, collectively ensuring stable and robust task execution. 

- We conduct comprehensive experiments in both the RoboTwin2 simulation environment and real-world scenarios. The results demonstrate that our framework effectively ensembles different base policies, achieving state-of-the-art performance across a wide variety of manipulation tasks. 

## **2. Related Work** 

### **2.1. Vision Language Action Models** 

Vision-Language-Action (VLA) models (Shukor et al., 2025; Li et al., 2026; Liu et al., 2024a; Zitkovich et al., 2023; Liu et al., 2024b; Bi et al., 2025; Liu et al., 2025; Faroni et al., 2025; Sapkota et al., 2025; Song et al., 2025b) have achieved significant progress in robotic tasks. These models enable robots to interpret high-level instructions expressed in natural language and execute corresponding actions in complex, real-world environments. Early representative work such as RT-2 (Zitkovich et al., 2023) and OpenVLA (Kim et al., 2024) established strong baselines in multi-task learning and cross-task generalization. Building on this foundation, recent work has diverged into three main technical directions. First, some approaches refine the base policy learning pipeline through mechanisms such as parallel decoding and action chunking (Kim et al., 2025; Zhao et al., 2024), achieving smoother control with continuous action spaces. Second, others formulate robot policy as conditional denoising diffusion processes (Ze et al., 2024; Chi et al., 2025), enabling diverse and adaptive behavior generation. Third, complementary methods integrate flow matching architectures with pre-trained Vision-Language Models (Black et al., 2024; Intelligence et al., 2025), directly leveraging internet-scale semantic knowledge. However, existing VLA methods develop independently, each excelling in different aspects yet lacking a principled mechanism to 

2 

**EnsembleVLA: Ensemble Learning for Vision-Language Action Models** 

combine them. In contrast, our EnsembleVLA proposes an energy-based framework that enables seamless ensemble of diverse VLA policies through additive energy composition. 

### **2.2. Ensemble Learning** 

Ensemble learning (Yang et al., 2023; Reuss et al., 2023; Gkanatsios et al., 2023; Wang et al., 2024; Cao et al., 2025) combines multiple models to achieve better predictive performance. Classical ensemble methods, including bagging (Breiman, 1996), boosting (Freund & Schapire, 1997), and stacking (Wolpert, 1992), have been widely used in enhancing predictive performance and robustness for discriminative tasks such as classification. In contrast, EnsembleVLA proposes a unified framework that leverages ensemble learning principles for VLA models composition by treating diffusion and flow-based paradigms as EBMs to enable principled distribution-level composition. Our framework establishes a learnable ensemble mechanism that integrates adaptive weight balancing and a confidenceaware gating strategy to selectively refine composed actions across multiple VLA policies. 

### **2.3. Energy-Based Models** 

EBMs (LeCun et al., 2006; Zhang et al., 2025a; Liu et al., 2022; Nie et al., 2021) define probability distributions through learnable energy functions _pθ_ ( _x_ ) _∝_ exp( _−Eθ_ ( _x_ )), where lower energy indicates higher probability. A fundamental property is that the score function equals the negative energy gradient: _∇x_ log _pθ_ ( _x_ ) = _−∇xEθ_ ( _x_ ), which connects EBMs to score-based diffusion models (Du & Mordatch, 2019; Song et al., 2020b) and flow matching (Balcerak et al., 2025). A key advantage of EBMs is their natural support for compositional generation: additive energy combination corresponds to multiplying the underlying distributions (Du et al., 2020). In contrast to prior work, our EnsembleVLA establishes a unified energy-based theoretical framework that encompasses both diffusion and flowbased VLA policies, leveraging the compositional property of EBMs to enable principled ensemble of diverse generative policies to achieve a stronger ensemble policy. 

## **3. Method** 

### **3.1. Preliminary** 

**Diffusion Models.** Diffusion models (Ho et al., 2020; Song et al., 2020b) provide a powerful framework for generative modeling by learning to reverse a gradual noising process. The forward process progressively corrupts data into noise and is defined as a stochastic differential equation (SDE) over _t ∈_ [0 _, T_ ]: 


where _Wt_ denotes the standard Wiener process, and _f_ ( **x** _t, t_ ), _g_ ( _t_ ) represent the drift and diffusion coefficients governing the noise injection schedule. By Anderson’s theorem (Anderson, 1982), the reverse-time SDE is: 


where _∇_ **x** _t_ log _pt_ ( **x** _t_ ) is the score function. A neural network _sθ_ ( **x** _t, t_ ) approximates the score via denoising score matching (Vincent, 2011): 


where _ϵθ_ predicts the added noise. Here we adopt the variance-preserving (VP) formulation **x** _t_ = _αt_ **x** 0 + _σt_ **_ϵ_** with **_ϵ_** _∼N_ ( **0** _,_ **I** ), where _αt_ and _σt_ are schedule coefficients satisfying _αt_<sup>2+</sup><sup>_σ_</sup> _t_<sup>2= 1.</sup> 

**Flow Matching.** Flow matching (Lipman et al., 2022) learns a continuous-time normalizing flow between a source distribution _µ_ 0 (typically Gaussian noise) and a target distribution _µ_ 1 (data) over _t ∈_ [0 _,_ 1]. Given samples **x** 0 _∼ µ_ 0 and **x** 1 _∼ µ_ 1, the conditional flow path follows the optimal transport interpolation **x** _t_ = (1 _− t_ ) **x** 0 + _t_ **x** 1, governed by an ODE: 


During inference, samples are generated by integrating the ODE from _t_ = 0 to _t_ = 1, providing a deterministic alternative to the stochastic sampling in diffusion models. 

### **3.2. Overview of EnsembleVLA** 

EnsembleVLA is an energy-based ensemble framework that combines diverse VLA policies into a unified, stronger policy. As illustrated in Figure 2, our approach consists of three components: (1) a _unified energy-based framework_ that formulates both diffusion and flow-based models under a common formalism; (2) a _compositional generation_ method that aggregates policies at the distribution level through additive energy combination; and (3) a _learnable composition weights and a confidence-aware gating mechanism_ for residual correction. We describe each element of the framework in detail below. 

### **3.3. Unified Energy-Based Theoretical Framework** 

To enable principled composition of diverse VLA models, we first establish a unified theoretical framework showing that both diffusion-based and flow-based VLA models can be interpreted as energy-based models, where the score function and velocity field both correspond to the negative energy gradient. 

3 

**EnsembleVLA: Ensemble Learning for Vision-Language Action Models** 


_Figure 2._ **Overall of EnsembleVLA** . We model diverse VLA models as independent energy functions and compose them at the distribution level to form a unified ensemble policy. To refine the composed actions, we introduce a confidence-aware gating mechanism with a Delta-Net predicting bounded residual corrections and a Gate-Net estimating refinement confidence. 

**Energy-Based Model Formulation.** Energy-based models (EBMs) (Du & Mordatch, 2019) provide a unified perspective for understanding both diffusion-based and flowbased policies. An EBM defines a probability distribution via a learnable energy function. For a static distribution, the energy function _Eθ_ ( **x** ) defines: 


where _Zθ_ = � exp( _−Eθ_ ( **x** )) d **x** is the partition function. In the context of generative models, we extend this to timedependent energy functions _Eθ_ ( **x** _t, t_ ) capturing the evolving distribution during generation: 


A fundamental property of EBMs is that the score function equals the negative energy gradient: 


This identity allows us to interpret score-based generative models as performing gradient descent on an implicit energy landscape. 

**Diffusion Models as Energy-Based Models.** We interpret diffusion models within the energy-based framework by representing the energy function through the denoising network. In diffusion models, the reverse process aims to denoise **x** _t_ to **x** _t−_ ∆ _t_ by predicting the noise _ϵθ_ ( **x** _t, t_ ). By leveraging the Gaussian denoising formulation, the denoising step can be written as: 


where **_ϵ_** _∼N_ (0 _,_ **I** ), and _ηt >_ 0 is a time-dependent step size. This corresponds to Langevin dynamics (Du & Mordatch, 2019): 


with the energy gradient given by _∇_ **x** _tEθ_ = _ϵθ/σt_ . In the deterministic limit (when the noise term vanishes), the relationship becomes: 


establishing that the score function directly corresponds to the negative energy gradient. 

4 

**EnsembleVLA: Ensemble Learning for Vision-Language Action Models** 

**Flow Matching as Energy-Based Models.** We establish the connection between flow matching and energy-based formulations through the Helmholtz decomposition. Any smooth velocity field can be decomposed as: 


where Φ _θ_ is a scalar potential and **r** is a divergence-free residual. By identifying _Eθ_ := Φ _θ_ , we obtain the energybased interpretation: 


Under optimal transport objectives, Brenier’s theorem (Brenier, 1991) guarantees that the optimal velocity field is conservative ( **r** = **0** ). While neural approximations yield non-zero **r** , empirical studies (Balcerak et al., 2025) show _∥_ **r** _∥≪∥vθ∥_ , validating the approximation _vθ ≈−∇Eθ_ in practice. 

**Unified Framework.** Combining Eq. (8) and Eq. (13), we arrive at a unified energy-based perspective: 


This unified perspective reveals that both paradigms perform gradient descent on an energy landscape—diffusion via stochastic Langevin dynamics and flow matching via deterministic gradient flow. Although they operate in opposite temporal directions (diffusion: _T →_ 0; flow matching: 0 _→_ 1), both can be unified through time reparameterization, enabling principled composition of both paradigms. 

### **3.4. Compositional Generation** 

Building upon the unified energy-based framework, we now present how EnsembleVLA composes multiple VLA policies through additive energy combination. Given _n_ policies characterized by conditional energy functions _{Eθi_ ( **x** _t, t,_ **c** _i_ ) _}_<sup>_n_</sup> _i_ =1<sup>, where</sup><sup>**c**</sup><sup>_i_denotes the conditioning in-</sup> formation (e.g., visual observations, language instructions) for the _i_ -th policy, the compositional energy is defined as: 


where _wi_ are learnable composition weights that will be optimized during training to enable adaptive policy balancing (detailed in Section 3.5), and **c** 1: _n_ = ( **c** 1 _, . . . ,_ **c** _n_ ) denotes the collection of conditioning information. 

Drawing from the compositional generation principle in EBMs (Du et al., 2020; Zhang et al., 2025a), the corresponding conditional probability distribution becomes: 


representing a geometric mixture when<sup>�</sup> _i_<sup>_wi_= 1 (as en-</sup> forced by our softmax parameterization in Section 3.5). Taking the gradient with respect to **x** _t_ yields the compositional score field: 


By the unified energy-based framework (Eq. (14)), the same linear combination principle applies to velocity fields: _v_ comp =<sup>�</sup><sup>_n_</sup> _i_ =1<sup>_wi· vθ_</sup> _i_<sup>.We sample the composed action</sup> **a**<sup>comp</sup> via iterative integration from **x** 0 _∼N_ (0 _,_ **I** ) using a unified progress variable _τ ∈_ [0 _,_ 1]: **x** _τ_ +∆ _τ_ = **x** _τ_ + ∆ _τ · v_ comp( **x** _τ , τ,_ **c** 1: _n_ ) _,_ (18) which corresponds to solving the probability flow ODE. We use deterministic sampling for all compositions as it provides more stable action generation for robotic control. The final sample **x** 1 at _τ_ = 1 yields the composed action **a**<sup>comp</sup> := **x** 1. For combining different model types, we use displacement-space composition to align predictions before composition. 

### **3.5. Ensemble Refinement** 

The composed action **a**<sup>comp</sup> _∈_ R<sup>_Da_</sup> ( _Da_ is the action dimension) may deviate from optimal due to distribution mismatch or complementary errors. To address this, EnsembleVLA incorporates two refinement mechanisms: (1) _learnable composition weights_ for adaptive policy balancing, and (2) a _confidence-aware gating mechanism_ that selectively activates bounded residual corrections. Let _ϕ_ = ( _ϕδ, ϕg_ ) denote the refinement module parameters. The refined action is: 

**a**<sup>ref</sup> = **a**<sup>comp</sup> + _gϕg_ ( **a**<sup>comp</sup> ) _·_ **_δ_** _ϕδ_ ( **a**<sup>comp</sup> ) _,_ (19) where _gϕg_ : R<sup>_Da_</sup> _→_ [0 _,_ 1] denotes the confidence-aware gating function, and **_δ_** _ϕδ_ : R<sup>_Da_</sup> _→_ [ _−δ_ max _, δ_ max]<sup>_Da_</sup> represents the bounded residual correction function. 

**Learnable Composition Weights for Adaptive Policy Balancing.** For adaptive policy balancing, we introduce learnable weights **w** = ( _w_ 1 _, . . . , wn_ )<sup>_⊤_</sup> optimized end-to-end. 

To ensure the weights reside on the probability simplex _S_<sup>_n−_1</sup> = _{_ **w** _∈_ R<sup>_n_</sup> +<sup>:</sup><sup>**1**</sup><sup>_⊤_</sup><sup>**w**=1</sup><sup>_}_, we employ the softmax</sup> reparameterization: 


where **_α_** _∈_ R<sup>_n_</sup> denotes unconstrained learnable parameters. This ensures normalized weights that maintain contributions from all policies and yield stable sampling. The weights _{wi}_<sup>_n_</sup> _i_ =1<sup>are jointly optimized with the refinement networks.</sup> 

5 

**EnsembleVLA: Ensemble Learning for Vision-Language Action Models** 

**Bounded Residual Correction.** The residual correction function **_δ_** _ϕδ_ predicts action corrections that compensate for the residual error between the composed action and the optimal action. To prevent over-correction and ensure training stability, we constrain the correction to a bounded output space _Hδ_ = _{_ **_δ_** : _∥_ **_δ_** _∥∞ ≤ δ_ max _}_ via: 


where the Delta Network _fδ_ : R<sup>_Da_</sup> _→_ R<sup>_Da_</sup> is parameterized as a two-layer MLP with Spectral Normalization (Miyato et al., 2018) to enforce Lipschitz continuity (Hager, 1979), ensuring that small perturbations in the input induce only bounded variations in the output. We set _δ_ max = 0 _._ 001 for conservative corrections. 

**Confidence-Aware Gating Mechanism.** The Gate Network _gϕg_ predicts a scalar confidence score that modulates whether to apply the residual correction: 


where _σ_ ( _·_ ) denotes the sigmoid function and _fg_ : R<sup>_Da_</sup> _→_ R is implemented as a three-layer MLP. Intuitively, the gating mechanism learns to assess when correction is beneficial: when **a**<sup>comp</sup> already aligns well with the optimal action, the gate outputs a low value to preserve it; conversely, when **a**<sup>comp</sup> deviates significantly, a high gate value activates the residual correction. This selective activation prevents unnecessary modifications that could degrade performance. We initialize the bias to _b_ 0 = _−_ 2 _._ 0 (yielding _g_ 0 = _σ_ ( _−_ 2 _._ 0) _≈_ 0 _._ 12) for conservative startup. 

### **3.6. Training Objective** 

To train EnsembleVLA, we design a composite loss function consisting of three complementary terms: 


where _λ_ 1 and _λ_ 2 are balancing coefficients that control the relative importance of the gating and residual prediction objectives, respectively. 

**Primary Reconstruction Loss.** The primary loss measures the mean squared error between the refined action and the expert demonstration: 


where _B_ denotes the batch size. This loss drives the network to learn effective correction strategies. 

**Gate Supervision Loss.** To teach the Gate Network when to apply corrections, we introduce a gate supervision loss based on predicted improvement estimation. We compute the improvement metric: 


where **_δ_** _i_ = **_δ_** _ϕδ_ ( **a** _i_<sup>comp</sup> ) is the predicted residual correction. A positive ∆ _i_ indicates that applying the correction would bring the action closer to the expert demonstration. The binary gate supervision target is: 


where we detach the gradient through **_δ_** _i_ during backpropagation. The gate loss is formulated using binary crossentropy: 


where _gi_ = _gϕg_ ( **a** _i_<sup>comp</sup> ) and _yi_<sup>gate</sup> _∈{_ 0 _,_ 1 _}_ indicates which paradigm yields lower action error for sample _i_ . 

**Delta Supervision Loss.** To accelerate convergence, we directly supervise the Delta Network with the bounded optimal correction. The target correction is: 


and we minimize the mean squared error: 


This loss provides a direct learning signal for the Delta-Net, complementing the end-to-end supervision from _L_ mse. 

## **4. Experiments** 

### **4.1. Datasets and Experimental Setup** 

We evaluate EnsembleVLA on eight simulated tasks in RoboTwin 2.0 (Chen et al., 2025) and six real-world tasks on the Cobot Mobile ALOHA (Fu et al., 2024). The simulated tasks cover a broad spectrum of bimanual coordination challenges, including coordinated grasping, sequential object transfer, and articulated object interaction. We adopt the standard benchmark protocol: training is performed with 100 expert demonstrations per task, and evaluation is conducted over 100 episodes per task in simulation and 20 trials per task in real-world settings. 

**Baselines.** We benchmark EnsembleVLA against four representative VLA models that span different generative 

6 

**EnsembleVLA: Ensemble Learning for Vision-Language Action Models** 

_Table 1._ **Experiment results on different policy compositions.** The table shows the success rate _↑_ . Our EnsembleVLA yields a noticeable improvement compared with the base policies. We report the average success rate and sample standard deviation over 3 seeds. 

||(Diffusion|**DP + DP3**<br>-Based + Diffus|ion-Based)|(Diffusi|**DP +**_π_**0.5**<br>on-Based + Flo|w-Based)|(Flow|_π_**0 +**_π_**0.5**<br>-Based + Flow|-Based)|
|---|---|---|---|---|---|---|---|---|---|
|**Task**|DP|DP3|**EnsembleVLA**|DP|_π_0.5|**EnsembleVLA**|_π_0|_π_0.5|**EnsembleVLA**|
|Beat Block Hammer|64.0_±_2_._3|85.0_±_1_._7|**97.0**_±_1_._0|64.0_±_2_._3|67.0_±_2_._0|**73.0**_±_1_._5|62.0_±_1_._2|67.0_±_2_._0|**73.0**_±_1_._3|
|Open Laptop|67.0_±_2_._1|82.0_±_1_._5|**93.0**_±_1_._2|67.0_±_2_._1|93.0_±_1_._0|**95.0**_±_0_._9|85.0_±_1_._8|93.0_±_1_._0|**97.0**_±_1_._4|
|Click Alarmclock|92.0_±_1_._3|76.0_±_2_._2|**96.0**_±_1_._6|92.0_±_1_._3|84.0_±_1_._8|**94.0**_±_1_._1|52.0_±_2_._5|84.0_±_1_._8|**91.0**_±_1_._7|
|Move Playingcard Away|61.0_±_2_._7|64.0_±_2_._4|**89.0**_±_1_._9|61.0_±_2_._7|82.0_±_1_._6|**88.0**_±_1_._4|56.0_±_1_._5|82.0_±_1_._6|**89.0**_±_1_._8|
|Place Bread Skillet|27.0_±_1_._9|46.0_±_2_._6|**55.0**_±_2_._2|27.0_±_1_._9|50.0_±_2_._3|**52.0**_±_1_._6|30.0_±_2_._1|50.0_±_2_._3|**61.0**_±_2_._4|
|Dump Bin Bigbin|53.0_±_2_._8|78.0_±_1_._9|**88.0**_±_1_._2|53.0_±_2_._8|69.0_±_2_._0|**72.0**_±_1_._3|65.0_±_1_._6|69.0_±_2_._0|**75.0**_±_2_._0|
|Handover Block|17.0_±_1_._2|49.0_±_2_._7|**70.0**_±_2_._5|17.0_±_1_._2|31.0_±_2_._1|**40.0**_±_2_._3|28.0_±_1_._9|31.0_±_2_._1|**54.0**_±_2_._6|
|Stack Bowls Three|35.0_±_2_._6|67.0_±_2_._1|**74.0**_±_1_._5|35.0_±_2_._6|45.0_±_2_._4|**47.0**_±_1_._7|42.0_±_1_._8|45.0_±_2_._4|**57.0**_±_2_._3|
|**Average**|52.0_±_2_._1|68.4_±_2_._1|**82.8**_±_1_._6|52.0_±_2_._1|65.1_±_1_._9|**70.1**_±_1_._5|52.5_±_1_._8|65.1_±_1_._9|**74.6**_±_1_._9|
|**Improvement**||+14.4|||+5.0|||+9.5||


_Table 2._ Ablation study of EnsembleVLA components on DP + DP3 ensemble. We report success rate (%) over 3 seeds. 

|||||Suc|cess Rate (|%)_↑_|
|---|---|---|---|---|---|---|
|Compose|Weights|Delta|Gate|Beat Block|Handover|Place Bread|
|||||Hammer|Block|Skillet|
|✓|✓|✓|✓|**97.0**_±_1.0|**70.0**_±_2.5|**55.0**_±_2.2|
|✓|✓|✓|_×_|93.0_±_2.0|64.0_±_3.5|50.0_±_4.0|
|✓|✓|_×_|_×_|89.0_±_1.3|56.0_±_1.0|43.0_±_1.6|
|✓|_×_|_×_|_×_|86.0_±_1.4|42.0_±_2.2|38.0_±_4.5|
|_×_|_×_|_×_|_×_|26.0_±_3.0|12.0_±_1.8|14.0_±_1.5|


generative family. For the cross-paradigm composition, EnsembleVLA achieves 70.1%, a 5.0% improvement over _π_ 0 _._ 5. This relatively modest gain is attributed to the additional complexity of velocity field transformation when composing diffusion-based and flow-based policies. Nevertheless, the positive results confirm that EnsembleVLA can successfully bridge different generative paradigms, validating its effectiveness in ensembling diverse VLA models to produce a stronger unified policy. 

### **4.2. Ablation Study** 

paradigms. Specifically, we consider: (1) DP (Chi et al., 2025), which formulates visuomotor control as a conditional denoising process over the action space; (2) DP3 (Ze et al., 2024), an extension that leverages point cloud inputs for explicit geometric reasoning; and (3) _π_ 0 (Black et al., 2024) and _π_ 0 _._ 5 (Intelligence et al., 2025), two recent flow matching-based foundation models trained on diverse robotic manipulation data. To ensure fair evaluation, all policies are trained on identical demonstration data. Pre-trained models ( _π_ 0 and _π_ 0 _._ 5) are initialized from publicly available weights and subsequently fine-tuned, whereas DP and DP3 are trained from random initialization. 

**Results.** Quantitative results are summarized in Table 1. We evaluate EnsembleVLA under three distinct policy compositions: (1) two diffusion-based policies (DP + DP3), (2) a diffusion-based and a flow-based policy (DP + _π_ 0 _._ 5), and (3) two flow-based policies ( _π_ 0 + _π_ 0 _._ 5). EnsembleVLA consistently outperforms all base policies across all compositions. In the diffusion-based combination, EnsembleVLA achieves 82.8%, improving 14.4% over DP3 (68.4%). When combining two flow-based policies, EnsembleVLA attains 74.6%, surpassing _π_ 0 _._ 5 by 9.5%. These gains demonstrate that our energy-based composition effectively aggregates complementary information from policies within the same 

To evaluate the contribution of each component, we conduct ablation experiments on three representative tasks. We progressively remove components to analyze their individual contributions. As shown in Table 2, the complete model achieves the best performance across all tasks. Removing the Gate mechanism leads to moderate degradation (70.0% _→_ 64.0% on Handover Block), as the model loses selective correction capability and applies modifications indiscriminately. Further removing Delta causes additional performance drops, demonstrating that bounded residual corrections are essential for compensating errors in the composed actions. When Learnable Weights are also removed, performance degrades substantially on tasks where base policies differ significantly in quality. For example, on Handover Block where DP achieves only 17.0%, fixed equal weighting fails to suppress the weak policy’s contribution, resulting in a 14% drop. 

Most notably, replacing energy-based composition with naive action-level averaging causes dramatic performance collapse (e.g., 42.0% _→_ 12.0% on Handover Block). This is because directly averaging actions from different policies produces geometrically meaningless outputs that fail to represent valid robot motions. These results validate that each component contributes meaningfully, and their combination is essential for effective policy ensemble. 

7 

**EnsembleVLA: Ensemble Learning for Vision-Language Action Models** 


_Figure 3._ Real-world bimanual manipulation: individual weak policies vs. EnsembleVLA. EnsembleVLA successfully handles tasks where individual policies fail (collision, slip, unsynchronized). 


_Figure 4._ **Multi-policy ensemble performance.** Success rates of individual policies and their ensembles on three manipulation tasks. Combining more policies consistently improves performance. 

### **4.3. Scaling Up to Multi-Policy Ensembles** 

To validate the scalability of our framework, we extend the composition to three VLA models: DP, DP3, and OpenVLAOFT. We evaluate on three manipulation tasks: _click alarmclock_ , _move playingcard_ , and _open laptop_ . As shown in Figure 4, individual policies achieve success rates ranging from 61% to 92% across different tasks. When composing DP and DP3 through our unified energy formulation, the ensemble achieves 96%, 89%, and 93% on the three tasks, consistently outperforming the individual baselines. Furthermore, incorporating OpenVLA-OFT into the ensemble yields additional improvements, reaching 99%, 95%, and 98%, respectively. These results demonstrate that our framework effectively leverages the complementary strengths of diverse policies, and the performance gains scale favorably with the number of composed models. 

### **4.4. Real-World Experiments** 

To validate the effectiveness of EnsembleVLA in real-world scenarios, we conduct experiments on a Cobot Mobile ALOHA across six manipulation tasks: _handover a cube_ , _open the pen cap_ , _pick up bowl_ , _push box_ , _put the banana into the drawer_ , and _put the doll into the plate_ . We collect 

_Table 3._ Real-world manipulation tasks performance comparison. We report success rates (%) over 20 trials per task. 

|Method|Handover<br>Cube|Open<br>Pen Cap|Pick up<br>Bowl|Push<br>Box|Put Banana<br>into Drawer|Put Doll<br>into Plate|<sup>Avg.</sup>|
|---|---|---|---|---|---|---|---|
|DP|45.0|30.0|50.0|55.0|25.0|35.0|40.0|
|_π_0_._5|60.0|50.0|65.0|70.0|45.0|55.0|57.5|
|EnsembleVLA|**70.0**|**60.0**|**75.0**|**80.0**|**50.0**|**60.0**|**65.8**|


50 demonstrations per task for training and evaluate each method over 20 trials per task. As shown in Table 3, EnsembleVLA consistently outperforms individual policies (DP and _π_ 0 _._ 5) across all tasks. Figure 3 provides qualitative comparisons, where individual policies exhibit various failure modes including collisions, object slipping, and unsynchronized bimanual coordination. By composing these policies through our energy-based framework, EnsembleVLA successfully overcomes these failure modes and achieves robust performance, demonstrating the effectiveness of our compositional approach in leveraging complementary strengths of different policies. 

## **5. Conclusion** 

This paper presents EnsembleVLA, a novel framework that combines diverse vision-language-action policies through energy-based composition. Our core contribution is a theoretical unification of diffusion and flow matching VLA paradigms, demonstrating that both can be formulated as energy-based models. This insight enables principled policy aggregation via weighted energy summation at the distribution level. We further introduce adaptive weighting and gating mechanisms to refine composed actions through dynamic policy balancing. Experimental results on simulation benchmarks and real-world robot deployments show that EnsembleVLA consistently outperforms individual base policies, validating the effectiveness of our approach for robotic manipulation. We hope EnsembleVLA inspires more researchers to explore the potential of ensemble learning in the field of embodied AI. 

8 

**EnsembleVLA: Ensemble Learning for Vision-Language Action Models** 

## **Acknowledgements** 

We would like to thank all co-authors for their efforts and the reviewers for their constructive comments. This work is supported by the National Natural Science Foundation of China (Key Project of Joint Fund) (Grant No. U24A20328), the National Natural Science Foundation of China (Grant No. 62476071), the Guangdong Basic and Applied Basic Research Foundation (Grant No. 2025A1515011732), the Beijing Natural Science Foundation (Grant Nos. 4262074 and L254018), the National Natural Science Foundation of China (Grant No. 62406092), the National Natural Science Foundation of China (Grant No. U24B20175), the Shenzhen Science and Technology Program (Grant No. KJZD20240903100017022), the Guangdong Basic and Applied Basic Research Foundation (Grant No. 2025A1515010169), and the Shenzhen Science and Technology Program (Grant No. KQTD20240729102207002). 

## **Impact Statement** 

This paper presents EnsembleVLA, an energy-based framework for combining diverse vision-language-action models to enhance robotic manipulation capabilities. By enabling the effective integration of multiple pre-trained VLA policies, our approach has the potential to accelerate the deployment of general-purpose robots in real-world applications such as manufacturing automation, logistics, healthcare assistance, and domestic service robotics, where robust manipulation capabilities are essential. The ability to combine complementary strengths of different policies may also reduce the data and computational requirements for training new robotic systems from scratch. As with any advancement in robotic manipulation, there are considerations regarding workforce displacement in automation-heavy industries and the safety of human-robot collaboration scenarios. 

## **References** 

- Anderson, B. D. Reverse-time diffusion equation models. _Stochastic Processes and their Applications_ , 12(3):313– 326, 1982. 

- Balcerak, M., Amiranashvili, T., Terpin, A., Shit, S., Bogensperger, L., Kaltenbach, S., Koumoutsakos, P., and Menze, B. Energy matching: Unifying flow matching and energy-based models for generative modeling. _arXiv preprint arXiv:2504.10612_ , 2025. 

- Bi, H., Wu, L., Lin, T., Tan, H., Su, Z., Su, H., and Zhu, J. H-rdt: Human manipulation enhanced bimanual robotic manipulation. _arXiv preprint arXiv:2507.23523_ , 2025. 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., et al. _π_ 0: A vision-language-action flow model for 

general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- Breiman, L. Bagging predictors. _Machine learning_ , 24(2): 123–140, 1996. 

- Brenier, Y. Polar factorization and monotone rearrangement of vector-valued functions. _Communications on pure and applied mathematics_ , 44(4):375–417, 1991. 

- Cao, J., Huang, Y., Guo, H., Zhang, R., Nan, M., Mai, W., Wang, J., Cheng, H., Sun, J., Han, G., et al. Compose your policies! improving diffusion-based or flow-based robot policies via test-time distribution-level composition. _arXiv preprint arXiv:2510.01068_ , 2025. 

- Cen, J., Yu, C., Yuan, H., Jiang, Y., Huang, S., Guo, J., Li, X., Song, Y., Luo, H., Wang, F., et al. Worldvla: Towards autoregressive action world model. _arXiv preprint arXiv:2506.21539_ , 2025. 

- Chen, T., Chen, Z., Chen, B., Cai, Z., Liu, Y., Li, Z., Liang, Q., Lin, X., Ge, Y., Gu, Z., et al. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. _arXiv preprint arXiv:2506.18088_ , 2025. 

- Chi, C., Xu, Z., Feng, S., Cousineau, E., Du, Y., Burchfiel, B., Tedrake, R., and Song, S. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , 44(10-11): 1684–1704, 2025. 

- Dong, X., Yu, Z., Cao, W., Shi, Y., and Ma, Q. A survey on ensemble learning. _Frontiers of Computer Science_ , 14(2): 241–258, 2020. 

- Du, Y. and Mordatch, I. Implicit generation and modeling with energy based models. _Advances in neural information processing systems_ , 32, 2019. 

- Du, Y., Li, S., and Mordatch, I. Compositional visual generation with energy based models. _NeurIPS_ , 33:6637–6647, 2020. 

- Du, Y., Durkan, C., Strudel, R., Tenenbaum, J. B., Dieleman, S., Fergus, R., Sohl-Dickstein, J., Doucet, A., and Grathwohl, W. S. Reduce, reuse, recycle: Compositional generation with energy-based diffusion models and mcmc. In _International conference on machine learning_ , pp. 8489–8510. PMLR, 2023. 

- Duan, J., Yuan, W., Pumacay, W., Wang, Y. R., Ehsani, K., Fox, D., and Krishna, R. Manipulate-anything: Automating real-world robots using vision-language models. _arXiv preprint arXiv:2406.18915_ , 2024. 

9 

**EnsembleVLA: Ensemble Learning for Vision-Language Action Models** 

- Faroni, M., Odesco, C., Zanchettin, A. M., and Rocco, P. Uncertainty-aware planning with inaccurate models for robotized liquid handling. In _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pp. 17725–17731. IEEE, 2025. 

- Freund, Y. and Schapire, R. E. A decision-theoretic generalization of on-line learning and an application to boosting. _Journal of computer and system sciences_ , 55(1):119–139, 1997. 

- Fu, Z., Zhao, T. Z., and Finn, C. Mobile aloha: Learning bimanual mobile manipulation with low-cost whole-body teleoperation. _arXiv preprint arXiv:2401.02117_ , 2024. 

- Gkanatsios, N., Jain, A., Xian, Z., Zhang, Y., Atkeson, C., and Fragkiadaki, K. Energy-based models are zero-shot planners for compositional scene rearrangement. _arXiv preprint arXiv:2304.14391_ , 2023. 

- Guo, Q., Ma, C., Jiang, Y., Yuan, Z., Yu, Y., and Luo, P. Egc: Image generation and classification via a diffusion energy-based model. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pp. 22952– 22962, 2023. 

- Hager, W. W. Lipschitz continuity for constrained processes. _SIAM Journal on Control and Optimization_ , 17(3):321– 338, 1979. 

- Hermans, T., Rehg, J. M., and Bobick, A. F. Decoupling behavior, perception, and control for autonomous learning of affordances. In _2013 IEEE International Conference on Robotics and Automation_ , pp. 4989–4996. IEEE, 2013. 

- Hinton, G. E. Training products of experts by minimizing contrastive divergence. _Neural computation_ , 14(8):1771– 1800, 2002. 

- Ho, J., Jain, A., and Abbeel, P. Denoising diffusion probabilistic models. _NeurIPS_ , 33:6840–6851, 2020. 

- Intelligence, P., Black, K., Brown, N., Darpinian, J., Dhabalia, K., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., et al. _π_ 0 _._ 5: a vision-language-action model with openworld generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 

- Jiang, Y., Gupta, A., Zhang, Z., Wang, G., Dou, Y., Chen, Y., Fei-Fei, L., Anandkumar, A., Zhu, Y., and Fan, L. Vima: Robot manipulation with multimodal prompts. 2023. 

- Kim, M. J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E., Lam, G., Sanketi, P., et al. Openvla: An open-source vision-languageaction model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- Kim, M. J., Finn, C., and Liang, P. Fine-tuning visionlanguage-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 

- LeCun, Y., Chopra, S., Hadsell, R., Ranzato, M., Huang, F., et al. A tutorial on energy-based learning. _Predicting structured data_ , 1(0), 2006. 

- Li, C., Wen, J., Peng, Y., Peng, Y., and Zhu, Y. Pointvla: Injecting the 3d world into vision-language-action models. _IEEE Robotics and Automation Letters_ , 11(3):2506–2513, 2026. 

- Li, D., Zhang, Y., Cao, M., Liu, D., Xie, W., Hui, T., Lin, L., Xie, Z., and Li, Y. Towards long-horizon vision-languageaction system: Reasoning, acting and memory. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pp. 6839–6848, 2025a. 

- Li, J., Cui, Y., Huang, T., Ma, Y., Fan, C., Yang, M., and Zhong, Z. Mixgrpo: Unlocking flow-based grpo efficiency with mixed ode-sde. _arXiv preprint arXiv:2507.21802_ , 2025b. 

- Li, Q., Liang, Y., Wang, Z., Luo, L., Chen, X., Liao, M., Wei, F., Deng, Y., Xu, S., Zhang, Y., et al. Cogact: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation. _arXiv preprint arXiv:2411.19650_ , 2024. 

- Li, X., Liu, M., Zhang, H., Yu, C., Xu, J., Wu, H., Cheang, C., Jing, Y., Zhang, W., Liu, H., et al. Vision-language foundation models as effective robot imitators. _arXiv preprint arXiv:2311.01378_ , 2023. 

- Lipman, Y., Chen, R. T., Ben-Hamu, H., Nickel, M., and Le, M. Flow matching for generative modeling. _arXiv preprint arXiv:2210.02747_ , 2022. 

- Liu, J., Liu, M., Wang, Z., An, P., Li, X., Zhou, K., Yang, S., Zhang, R., Guo, Y., and Zhang, S. Robomamba: Efficient vision-language-action model for robotic reasoning and manipulation. _Advances in Neural Information Processing Systems_ , 37:40085–40110, 2024a. 

- Liu, N., Li, S., Du, Y., Torralba, A., and Tenenbaum, J. B. Compositional visual generation with composable diffusion models. In _European conference on computer vision_ , pp. 423–439. Springer, 2022. 

- Liu, P., Guo, Z., Warke, M., Chintala, S., Paxton, C., Shafiullah, N. M. M., and Pinto, L. Dynamem: Online dynamic spatio-semantic memory for open world mobile manipulation. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 13346–13355. IEEE, 2025. 

10 

**EnsembleVLA: Ensemble Learning for Vision-Language Action Models** 

- Liu, S., Wu, L., Li, B., Tan, H., Chen, H., Wang, Z., Xu, K., Su, H., and Zhu, J. Rdt-1b: a diffusion foundation model for bimanual manipulation. _arXiv preprint arXiv:2410.07864_ , 2024b. 

- Ma, Y., Song, Z., Zhuang, Y., Hao, J., and King, I. A survey on vision-language-action models for embodied ai. _arXiv preprint arXiv:2405.14093_ , 2024. 

- Miyato, T., Kataoka, T., Koyama, M., and Yoshida, Y. Spectral normalization for generative adversarial networks. _arXiv preprint arXiv:1802.05957_ , 2018. 

- Nie, W., Vahdat, A., and Anandkumar, A. Controllable and compositional generation with latent-space energy-based models. _Advances in Neural Information Processing Systems_ , 34:13497–13510, 2021. 

- Qu, D., Song, H., Chen, Q., Yao, Y., Ye, X., Ding, Y., Wang, Z., Gu, J., Zhao, B., Wang, D., et al. Spatialvla: Exploring spatial representations for visual-language-action model. _arXiv preprint arXiv:2501.15830_ , 2025. 

- Reuss, M., Li, M., Jia, X., and Lioutikov, R. Goalconditioned imitation learning using score-based diffusion policies. _arXiv preprint arXiv:2304.02532_ , 2023. 

- Sapkota, R., Cao, Y., Roumeliotis, K. I., and Karkee, M. Vision-language-action models: Concepts, progress, applications and challenges. _arXiv preprint arXiv:2505.04769_ , 2025. 

- Shukor, M., Aubakirova, D., Capuano, F., Kooijmans, P., Palma, S., Zouitine, A., Aractingi, M., Pascal, C., Russi, M., Marafioti, A., et al. Smolvla: A vision-languageaction model for affordable and efficient robotics. _arXiv preprint arXiv:2506.01844_ , 2025. 

- Song, J., Meng, C., and Ermon, S. Denoising diffusion implicit models. _arXiv preprint arXiv:2010.02502_ , 2020a. 

- Song, M., Deng, X., Zhong, G., Lv, Q., Wan, J., Li, Y., Hao, J., and Guan, W. Few-shot vision-language action-incremental policy learning. _arXiv preprint arXiv:2504.15517_ , 2025a. 

- Song, M., Deng, X., Zhou, Z., Wei, J., Guan, W., and Nie, L. A survey on diffusion policy for robotic manipulation: Taxonomy, analysis, and future directions. _Authorea Preprints_ , 2025b. 

- Song, M., Deng, X., Wei, J., Jiang, D., Nie, L., and Guan, W. Energyaction: Unimanual to bimanual composition with energy-based models. _arXiv preprint arXiv:2603.20236_ , 2026. 

- Song, Y., Sohl-Dickstein, J., Kingma, D. P., Kumar, A., Ermon, S., and Poole, B. Score-based generative modeling 

through stochastic differential equations. _arXiv preprint arXiv:2011.13456_ , 2020b. 

- Team, O. M., Ghosh, D., Walke, H., Pertsch, K., Black, K., Mees, O., Dasari, S., Hejna, J., Kreiman, T., Xu, C., et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

- Vincent, P. A connection between score matching and denoising autoencoders. _Neural computation_ , 23(7):1661– 1674, 2011. 

- Wang, D., Liu, C., Chang, F., and Xu, Y. Hierarchical diffusion policy: manipulation trajectory generation via contact guidance. _IEEE Transactions on Robotics_ , 2025. 

- Wang, L., Zhao, J., Du, Y., Adelson, E. H., and Tedrake, R. Poco: Policy composition from and for heterogeneous robot learning. _arXiv preprint arXiv:2402.02511_ , 2024. 

- Wen, J., Zhu, Y., Li, J., Zhu, M., Tang, Z., Wu, K., Xu, Z., Liu, N., Cheng, R., Shen, C., et al. Tinyvla: Towards fast, data-efficient vision-language-action models for robotic manipulation. _IEEE Robotics and Automation Letters_ , 2025. 

- Wolpert, D. H. Stacked generalization. _Neural networks_ , 5 (2):241–259, 1992. 

- Xian, Z., Gkanatsios, N., Gervet, T., Ke, T.-W., and Fragkiadaki, K. Chaineddiffuser: Unifying trajectory diffusion and keypose prediction for robotic manipulation. In _7th Annual Conference on Robot Learning_ , 2023. 

- Yang, S., Li, H., Chen, Y., Wang, B., Tian, Y., Wang, T., Wang, H., Zhao, F., Liao, Y., and Pang, J. Instructvla: Vision-language-action instruction tuning from understanding to manipulation. _arXiv preprint arXiv:2507.17520_ , 2025. 

- Yang, Y., Lv, H., and Chen, N. A survey on ensemble learning under the era of deep learning. _Artificial Intelligence Review_ , 56(6):5545–5589, 2023. 

- Yoon, S., Hwang, H., Kwon, D., Noh, Y.-K., and Park, F. Maximum entropy inverse reinforcement learning of diffusion models with energy-based models. _Advances in Neural Information Processing Systems_ , 37:24601– 24624, 2024. 

- Ze, Y., Zhang, G., Zhang, K., Hu, C., Wang, M., and Xu, H. 3d diffusion policy: Generalizable visuomotor policy learning via simple 3d representations. _arXiv preprint arXiv:2403.03954_ , 2024. 

- Zhang, J., Fan, H., and Yang, Y. Energymogen: Compositional human motion generation with energy-based diffusion model in latent space. In _Proceedings of the_ 

11 

**EnsembleVLA: Ensemble Learning for Vision-Language Action Models** 

_Computer Vision and Pattern Recognition Conference_ , pp. 17592–17602, 2025a. 

- Zhang, Q., Liu, Z., Fan, H., Liu, G., Zeng, B., and Liu, S. Flowpolicy: Enabling fast and robust 3d flow-based policy via consistency flow matching for robot manipulation. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 39, pp. 14754–14762, 2025b. 

- Zhao, M., Bao, F., Li, C., and Zhu, J. Egsde: Unpaired image-to-image translation via energy-guided stochastic differential equations. _Advances in Neural Information Processing Systems_ , 35:3609–3623, 2022. 

- Zhao, Q., Lu, Y., Kim, M. J., Fu, Z., Zhang, Z., Wu, Y., Li, Z., Ma, Q., Han, S., Finn, C., et al. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 1702–1713, 2025. 

- Zhao, T. Z., Tompson, J., Driess, D., Florence, P., Ghasemipour, K., Finn, C., and Wahid, A. Aloha unleashed: A simple recipe for robot dexterity. _arXiv preprint arXiv:2410.13126_ , 2024. 

- Zitkovich, B., Yu, T., Xu, S., Xu, P., Xiao, T., Xia, F., Wu, J., Wohlhart, P., Welker, S., Wahid, A., et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pp. 2165–2183. PMLR, 2023. 

12 

**EnsembleVLA: Ensemble Learning for Vision-Language Action Models** 

In this Supplementary Material, we provide detailed derivations of the ensemble energy-based framework (Section A), pseudocode for our unified cross-paradigm (diffusion-based and flow-based) policy composition algorithm (Section B), extensive ablation studies on inference latency, loss weighting, residual bounds, and composition dynamics (Section C), a comprehensive description of the simulated bimanual manipulation tasks (Section D), details of the real-world hardware setup and evaluation tasks (Section E), and a discussion of current limitations along with future research directions (Sections F and G). 

## **A. Detailed Derivations** 

### **A.1. Reverse-Time SDE** 

Given the forward SDE: 


where _f_ ( **x** _t, t_ ) is the drift, _g_ ( _t_ ) is the diffusion coefficient, and _Wt_ is a Wiener process. By Anderson’s theorem (Anderson, 1982), the reverse-time SDE is: 


### **A.2. Score Function and Noise Prediction** 

For the variance-preserving (VP) forward process: 


where _αt_<sup>2+</sup><sup>_σ_</sup> _t_<sup>2= 1.The conditional distribution is:</sup> 


The conditional score is: 


By denoising score matching (Vincent, 2011), the neural network _ϵθ_ ( **x** _t, t_ ) predicts **_ϵ_** . We parameterize the score network via an energy function _Eθ_ ( **x** _t, t_ ): 


which is trained to approximate the true score _∇_ **x** _t_ log _pt_ ( **x** _t_ ). 

### **A.3. Probability Flow ODE** 

Song et al. (Song et al., 2020b) showed that the following ODE shares the same marginals with Eq. (A.2): 


### **A.4. Score Function and Energy Gradient** 

An EBM defines the distribution via energy function _Eθ_ ( **x** _t, t_ ): 


Since _Zθ_ ( _t_ ) is independent of **x** _t_ , the gradient yields: 


13 

**EnsembleVLA: Ensemble Learning for Vision-Language Action Models** 

### **A.5. Velocity Field in Energy-Based Form** 

We establish the energy-based interpretation of flow matching through two complementary perspectives. 

**Perspective 1: Helmholtz Decomposition.** By the Helmholtz decomposition theorem, any sufficiently smooth vector field _vθ_ : R<sup>_d_</sup> _→_ R<sup>_d_</sup> can be uniquely decomposed as: 


where Φ : R<sup>_d_</sup> _→_ R is a scalar potential (the conservative/irrotational component) and **A** : R<sup>_d_</sup> _→_ R<sup>_d_</sup> is a vector potential (the solenoidal/rotational component). Defining _Eθ_ := Φ and **r** := _∇×_ **A** , we obtain: 


where _∇·_ **r** = 0 (divergence-free) and _∇×_ ( _−∇Eθ_ ) = **0** (curl-free). 

**Perspective 2: Optimal Transport Theory.** Under optimal transport with quadratic cost _c_ ( **x** _,_ **y** ) = _∥_ **x** _−_ **y** _∥_<sup>2</sup> _/_ 2, Brenier’s theorem (Brenier, 1991) states that the optimal transport map _T_<sup>_∗_</sup> is the gradient of a convex function: _T_<sup>_∗_</sup> = _∇_ Ψ<sup>_∗_</sup> for some convex Ψ<sup>_∗_</sup> . The corresponding velocity field satisfies: 


which is purely conservative ( **r** = **0** ). While neural network approximations _vθ_ do not exactly satisfy this condition, they inherit an inductive bias toward conservative fields when trained with OT-based objectives. 

**Approximation Quality.** Combining both perspectives, we write: 


where the approximation _vθ ≈−∇Eθ_ holds when _∥_ **r** _∥≪∥vθ∥_ . Empirical studies (Balcerak et al., 2025) confirm that flow matching with linear interpolation and Gaussian source distribution yields velocity fields with small rotational components, validating this approximation in practice. 

### **A.6. Temporal Unification** 

Diffusion generates from _t_ = _T_ to 0; flow matching from _t_ = 0 to 1. We unify via _τ ∈_ [0 _,_ 1]: 


Both models then follow: 


### **A.7. Compositional Score Function** 

Given _n_ policies with energy functions _{Eθi_ ( **x** _t, t,_ **c** _i_ ) _}_<sup>_n_</sup> _i_ =1<sup>, the compositional energy is:</sup> 


The corresponding distribution: 


14 

**EnsembleVLA: Ensemble Learning for Vision-Language Action Models** 

|**Algo **|**rithm 1**Cross-Paradigm PolicyComposition|
|---|---|
|**Req**<br>c|**uire:** Diffusion policy_π_diff, flow policy_π_flow, weights(_wd, wf_), diffusion time_T_, steps_N_, noise schedule_{αt, σt}_,<br>onditioning**c**|
|**Ensu**<br>|**re:** Composed action**a**<sup>comp</sup><br>|
|1:|**x**<sup>(0)</sup> _∼N_(**0**_,_**I**)<br>_▷_Initialize from noise|
|2: **f**|**or**_i_= 0to_N −_1**do**|
|3:|_/* Step 1: Temporal alignment */_|
|4:|_τ ←i/N_<br>_▷_Unified progress|
|5:|_td ←T_(1_−τ_),<br>_t_<sup>_′_</sup><br>_d _<sup>_←T_(1</sup><sup>_−τ −_1</sup><sup>_/N_)</sup><br>_▷_Diffusion timestamps|
|6:|_tf ←τ_<br>_▷_Flow timestamp|
|7:|_/* Step 2: Model predictions */_<br>|
|8:|**_ϵ_**_←π_diff(**x**<sup>(</sup><sup>_i_)</sup>_, td,_**c**)<br>_▷_Noise prediction<br>|
|9:|**v**_←π_flow(**x**<sup>(</sup><sup>_i_)</sup>_, tf,_**c**)<br>_▷_Velocity prediction|
|10:|_/* Step 3: Convert to displacement space */_<br>|
|11:|ˆ**x**0 _←_(**x**<sup>(</sup><sup>_i_)</sup> _−σtd_**_ϵ_**)_/αtd_<br>_▷_DDIM: estimate clean sample<br>|
|12:|∆**x**_d ←αt_<sup>_′_</sup><br>_d_ <sup>ˆ</sup><sup>**x**0 +</sup><sup>_σt′_</sup><br>_d_<sup>**_ϵ_**</sup><sup>_−_</sup><sup>**x**(</sup><sup>_i_)</sup><br>_▷_Diffusion displacement|
|13:|<br><br>∆**x**_f ←_**v**_/N_<br>_▷_Flow displacement|
|14:|_/* Step 4: Weighted composition */_<br>|
|15:|**x**<sup>(</sup><sup>_i_+1)</sup> _←_**x**<sup>(</sup><sup>_i_) </sup>+_wd ·_∆**x**_d_+_wf ·_∆**x**_f_|
|16: **e**<br>|**nd for**<br>|
|17: **r**|**eturn a**<sup>comp</sup> _←_**x**<sup>(</sup><sup>_N_)</sup>|
|Expa|nding:|
|Taki|_p_comp(**x**_t |_**c**1:_n_)_∝_exp<br>�<br>_−_<br>_n_<br>�<br>_i_=1<br>_wiEθi_<br>�<br>=<br>_n_<br>�<br>_i_=1<br>exp(_−wiEθi_)<br>_∝_<br>_n_<br>�<br>_i_=1<br>_pθi_(**x**_t |_**c**_i_)<sup>_wi_</sup>_._<br>(A.19)<br>ng gradient:|


By Eq. (A.10) and Eq. (A.14), the same applies to velocity fields: 


## **B. Composition of Diffusion-Based and Flow-Based VLA Models** 

To compose policies from different generative paradigms, we convert their outputs to a common displacement space. Diffusion models predict noise **_ϵ_** _θ_ , while flow matching models predict velocity _vθ_ . Although these models are based on different formulations, with diffusion operating in a denoising framework and flow matching in a continuous trajectory setting, they share the same underlying goal: to guide the action generation process toward high-likelihood regions of the data distribution. 

For diffusion, given noise prediction **_ϵ_** at time _td_ , the DDIM update (Song et al., 2020a) estimates the clean sample and computes the displacement: 


**EnsembleVLA: Ensemble Learning for Vision-Language Action Models** 

_Table 4._ **Inference latency and performance analysis on L40S GPU.** EnsembleVLA executes both policies in parallel with minimal additional overhead, while achieving substantial performance gains. 

|**Configuration**|**Latency **|**Relative **|**Frequency **|**Avg. Success**|
|---|---|---|---|---|
|_π_0 (single policy)|100.0 ms|1.00_×_|10.0 Hz|52_._5_±_1_._8%|
|_π_0_._5 (single policy)|112.5 ms|1.13_×_|8.9 Hz|65_._1_±_1_._9%|
|EnsembleVLA (_π_0 +_π_0_._5)|117.5 ms|1.18_×_|8.5 Hz|**74**_._**6**_±_**1**_._**9**%|


_Table 5._ **Sensitivity analysis of loss weights** _λ_ 1 **and** _λ_ 2 **.** We report success rates (%) on three tasks using the DP + DP3 ensemble. Results are averaged over 3 seeds. 

|_λ_1|_λ_2|Beat Block<br>Hammer|Handover<br>Block|Place Bread<br>Skillet|Avg.|
|---|---|---|---|---|---|
|0.1|0.9|88.0_±_2.4|54.0_±_3.2|42.0_±_2.8|61.3|
|0.3|0.7|91.0_±_2.0|60.0_±_2.8|47.0_±_2.4|66.0|
|0.5|0.5|94.0_±_1.6|65.0_±_2.4|51.0_±_2.4|70.0|
|0.7|0.3|**97.0**_±_1.0|**70.0**_±_2.5|**55.0**_±_2.2|**74.0**|
|0.9|0.1|92.0_±_2.0|62.0_±_2.8|48.0_±_2.8|67.3|


For flow matching, given velocity **v** at time _tf_ , Euler integration yields: 


where ∆ _τ_ = 1 _/N_ is the step size. Using the unified progress variable _τ ∈_ [0 _,_ 1] from Eq. (A.15), we synchronize both models via _td_ = _T_ (1 _− τ_ ), _t_<sup>_′_</sup> _d_<sup>=</sup><sup>_T_(1</sup><sup>_−τ−_∆</sup><sup>_τ_), and</sup><sup>_tf_=</sup><sup>_τ_.With both displacements aligned, we compose them as:</sup> 


where ( _wd, wf_ ) are learnable weights with _wd_ + _wf_ = 1. This is equivalent to the score/velocity composition in Eq. (A.20)(A.21), since ∆ **x** _∝ vθ ·_ ∆ _t_ . Algorithm 1 summarizes the procedure. 

## **C. More experiments and details** 

This section provides a comprehensive set of additional experiments and implementation details to further analyze the behavior and robustness of EnsembleVLA. Specifically, we report (1) inference latency measurements under realistic hardware settings; (2) sensitivity studies on the loss weight hyperparameters _λ_ 1 and _λ_ 2; (3) an ablation on the residual correction bound _δ_ max; and (4) an in-depth analysis of the learned composition weights during training. Together, these results offer insights into the efficiency, stability, and adaptive gate mechanism of our ensemble framework. 

### **C.1. Inference Latency** 

We analyze the inference efficiency of EnsembleVLA on an NVIDIA L40S GPU, with results summarized in Table 4. A key advantage of our framework is that the base policies are executed _in parallel_ , meaning they do not block each other during inference. Consequently, the ensemble latency (117.5 ms) is only marginally higher than that of the slower individual policy _π_ 0 _._ 5 (112.5 ms), with merely 5 ms additional overhead introduced by the composition and refinement modules. Despite an 18% increase in latency compared to _π_ 0, EnsembleVLA achieves substantial performance gains: on the _π_ 0 + _π_ 0 _._ 5 combination, the average success rate improves from 65.1% to 74.6%, representing a 9.5% absolute improvement (Table 1). Furthermore, the latency overhead can be effectively mitigated in real-world deployment through action interpolation, which maintains smooth robot motion at higher control frequencies while the ensemble policy computes subsequent actions in the background. These results demonstrate that our ensemble framework achieves a favorable trade-off between computational cost and task performance. 

16 

**EnsembleVLA: Ensemble Learning for Vision-Language Action Models** 


_Figure 5._ **Effect of residual bound** _δ_ max **on success rate.** The optimal value _δ_ max = 0 _._ 001 achieves the best performance across all tasks. Smaller values limit correction capacity, while larger values lead to over-correction. 

### **C.2. Loss Weight Sensitivity** 

We investigate the sensitivity of EnsembleVLA to the loss weight hyperparameters _λ_ 1 (gate supervision) and _λ_ 2 (delta supervision) in Eq. (23), where _λ_ 1 + _λ_ 2 = 1. Experiments are conducted on the DP + DP3 ensemble across three representative tasks, with results reported in Table 5. 

The results reveal several important findings. First, when _λ_ 2 dominates (for example, _λ_ 1 = 0 _._ 1 _, λ_ 2 = 0 _._ 9), the Gate-Net receives insufficient supervision and fails to learn accurate confidence estimation for selective refinement, leading to degraded performance. Second, when _λ_ 1 dominates excessively (for example, _λ_ 1 = 0 _._ 9 _, λ_ 2 = 0 _._ 1), the Delta-Net lacks adequate learning signal, resulting in less effective residual corrections. The optimal configuration _λ_ 1 = 0 _._ 7 and _λ_ 2 = 0 _._ 3 achieves the best balance, where the gate supervision is strong enough to guide selective activation while the delta supervision still provides sufficient signal for learning accurate corrections. This suggests that proper confidence-aware gating is slightly more critical than direct residual supervision in our framework. We adopt this setting for all experiments reported in this paper. 

### **C.3. Residual Bound Sensitivity** 

We analyze how the residual bound _δ_ max affects the performance of EnsembleVLA. Recall that the Delta-Net predicts bounded corrections via **_δ_** = _δ_ max _·_ tanh( _fδ_ ( **a** )), where _δ_ max controls the maximum allowable correction magnitude. We evaluate different values of _δ_ max on the DP + DP3 ensemble across three tasks, with results shown in Figure 5. 

The results reveal a clear trade-off in selecting _δ_ max. When _δ_ max is too small (for example, 0.0001), the correction capacity is severely limited, and the Delta-Net cannot sufficiently compensate for errors in the composed actions, resulting in marginal improvements over the base composition. As _δ_ max increases to 0.001, the model achieves optimal performance across all three tasks (97.0%, 70.0%, and 55.0% respectively), indicating that this value provides sufficient flexibility for effective refinement. However, when _δ_ max becomes excessively large (for example, 0.005 or 0.01), performance degrades noticeably. This is because overly large corrections can destabilize actions that are already near-optimal, introducing unnecessary perturbations that harm execution quality. Based on these findings, we set _δ_ max = 0 _._ 001 as the default configuration, which strikes an effective balance between correction capacity and stability. 

### **C.4. Composition Weight Analysis** 

We analyze the evolution of learned composition weights during training to understand how EnsembleVLA balances contributions from different policies. In our framework, the weights _w_ DP and _w_ DP3 are parameterized via softmax (Eq. (20)) and optimized end-to-end. We conduct experiments on the DP + DP3 ensemble across three representative tasks and 

17 

#### **EnsembleVLA: Ensemble Learning for Vision-Language Action Models** 


_Figure 6._ **Evolution of composition weights and success rates during training on three tasks.** For each task, the left panel shows the weight dynamics evolving from equal initialization (0.5, 0.5), and the right panel shows the corresponding success rate improvement. The learned weights consistently favor the stronger policy (DP3) while retaining non-trivial contribution from the weaker policy (DP). The final weight allocation varies across tasks, reflecting task-specific policy complementarity. 

### visualize the weight dynamics and corresponding success rates for each task in Figure 6. 

Several interesting patterns emerge from the training dynamics. First, across all three tasks, starting from equal initialization ( _w_ DP = _w_ DP3 = 0 _._ 5), the weights gradually diverge as training progresses. The weight assigned to the stronger policy (DP3) steadily increases while the weight for the weaker policy (DP) decreases correspondingly. This adaptive behavior demonstrates that our learnable weight mechanism can automatically identify and prioritize more effective policies. Second, the final weight allocation varies across tasks, reflecting task-specific characteristics. For Handover Block, where the performance gap between DP (17.0%) and DP3 (49.0%) is largest, the learned weights show stronger preference for DP3 ( _w_ DP3 _≈_ 0 _._ 78). In contrast, for Beat Block Hammer, where both policies perform relatively well (DP: 64.0%, DP3: 85.0%), the weight distribution is more balanced ( _w_ DP3 _≈_ 0 _._ 68). Third, notably, the weight of the weaker policy never collapses to zero in any task. This indicates that even a relatively weaker policy provides complementary information that benefits the ensemble, validating the principle that diversity among base learners contributes to overall performance. 

### **C.5. Experimental Details** 

**Individual Policy Training.** Before ensemble composition, each base policy is trained independently on task-specific demonstration data. Diffusion Policy (DP) employs a U-Net architecture with a ResNet-18 visual encoder, trained using the DDPM scheduler with 100 diffusion steps. We use the AdamW optimizer with a learning rate of 1e-4, batch size 128, and a cosine learning rate schedule. 3D Diffusion Policy (DP3) follows a similar diffusion framework but operates on point cloud observations, trained with a batch size of 256, a learning rate of 1e-4, and 100 inference steps. _π_ 0 and _π_ 0 _._ 5 are fine-tuned 

18 

**EnsembleVLA: Ensemble Learning for Vision-Language Action Models** 


_Figure 7._ Simulated Environment Tasks. 

from pre-trained checkpoints using the PI05 framework in RoboTwin2 with JAX/Flax, optimized with AdamW, a batch size of 32, a cosine decay learning rate schedule, and an EMA decay of 0.99. After training, we convert the JAX models to PyTorch using convert ~~j~~ ax ~~m~~ odel ~~t~~ o ~~p~~ ytorch.py provided in OpenPI and continue training under the same configuration. OpenVLA-OFT is fine-tuned from the OpenVLA-7B foundation model using LoRA (rank 32) and a diffusion (DDPM) action head, with a batch size of 32, a learning rate of 5e-4, and learning rate decay applied at 50,000 steps. All experiments are conducted on NVIDIA H100 80GB GPUs. DP and DP3 are trained on a single GPU, while _π_ 0, _π_ 0 _._ 5, and OpenVLA-OFT require multi-GPU setups due to their larger model sizes. 

**Ensemble Policy Training.** We adopt a weight-learning framework to compose the pre-trained policies described above. Training is managed via Hydra-based configuration. All base policy parameters are frozen and only the learnable composition weights and a conservative energy head for action refinement are optimized. The composition weights are parameterized with a softmax to ensure they sum to one. We use the AdamW optimizer with a learning rate of 1e-5 for the residual head and 1e-4 for the composition weights, along with weight decay of 1e-6. The learning rate schedule follows cosine annealing. We set the batch size to 64 and employ 4 data loading workers. All experiments are performed on NVIDIA L40S GPUs using the RoboTwin simulation environment with L515 camera observations. Each task is provided with 100 expert demonstrations. The action space has 14 dimensions, corresponding to the dual-arm ALOHA-AgileX robot configuration. 

## **D. Simulation Tasks and Description** 

We conduct our experiments in the RoboTwin 2.0 simulation framework, a scalable and domain-randomized platform designed for robust bimanual robotic manipulation. RoboTwin 2.0 integrates a large-scale object dataset (RoboTwin-OD) with 731 instances across 147 categories, each annotated with semantic and functional affordances. The framework supports automated expert-level trajectory generation via a closed-loop pipeline that combines multimodal large language models (MLLMs) with simulation-in-the-loop feedback. To enhance sim-to-real transfer, RoboTwin 2.0 incorporates systematic domain randomization across five axes: scene clutter, lighting conditions, background textures, tabletop heights, and natural language instructions. The platform also provides embodiment-aware adaptation, enabling the generation of robot-specific manipulation strategies for diverse dual-arm configurations, including Franka, UR5, Piper, ARX-X5, and Aloha-AgileX. 

We evaluate our approach on eight representative bimanual manipulation tasks from the RoboTwin 2.0 benchmark: Beat Block Hammer, Click Alarmclock, Open Laptop, Move Playingcard Away, Place Bread Skillet, Dump Bin Bigbin, Handover Block, and Stack Bowls Three. As illustrated in Figure 7, these tasks encompass a diverse set of challenges 

19 

**EnsembleVLA: Ensemble Learning for Vision-Language Action Models** 


_Figure 8._ Real-World Tasks. 

commonly encountered in dual-arm manipulation, including grasping and placing, handover, stacking, tool use, and container manipulation. The selection covers a broad spectrum of task types available in the benchmark, ensuring that our evaluation reflects generalization across different object interactions, motion complexities, and language-conditioned goals. This variety allows us to thoroughly assess policy robustness and adaptability under domain-randomized simulation conditions. 

## **E. Real-World Setting** 

### **E.1. Hardware Information** 

We provide a description of the hardware configuration of our real-world experiments. Our proposed EnsembleVLA is deployed on the Cobot Mobile ALOHA platform (Fu et al., 2024), which follows the Mobile ALOHA system architecture. As illustrated in Figure 9, the platform comprises two master arms, two follower arms, two wrist-mounted cameras, and a front-facing camera. Note that in our experiments, we use only one 6-DoF robotic arm and perform stationary manipulation tasks; the robot’s mobility features are not utilized. 

### **E.2. Real-World Task Setup** 

To evaluate the sim-to-real generalization capability of policies trained in the RoboTwin 2.0 simulation, we design six real-world tabletop tasks that correspond to key skill categories defined in the simulation benchmark. As visualized in Figure 8, these tasks span the following manipulation families: 

- **Object Transfer and Handover:** _Handover a cube_ requires one arm to grasp and transfer an object to the other arm at a designated handover location, testing sequential coordination and spatial synchronization. 

- **Precision and Articulated Manipulation:** _Open the pen cap_ involves fine-grained dexterity to rotate and remove a small cap, while _put the banana into the drawer_ demands interaction with an articulated object (drawer) under kinematic constraints. 

- **Grasping and Placing:** _Pick up bowl_ evaluates basic prehensile ability with a curved object. _Push box_ examines non-prehensile manipulation via pushing. _Put the doll into the plate_ focuses on precise placement with orientation awareness. 

Each task is executed 20 times in real-world trials to compute the average success rate, ensuring statistical reliability in performance evaluation. 

20 

**EnsembleVLA: Ensemble Learning for Vision-Language Action Models** 


_Figure 9._ Real-World hardware configuration. We use the Cobot Mobile ALOHA, which is equipped with two control arms, two slave arms, two wrist cameras and a frontal camera. 

## **F. Limitations and Failure case** 

Our ensemble framework has inherent limitations when composing VLA policies with different generative paradigms. Specifically, when combining flow-based VLA models (e.g., _π_ 0, _π_ 0 _._ 5) with diffusion-based policies (e.g., DP, DP3), we convert the diffusion noise predictions to DDIM-style velocity predictions to align with flow matching’s velocity-based formulation. This conversion involves transforming between different normalization spaces and approximating the diffusion denoising direction as a velocity field. Such approximations introduce precision loss, resulting in suboptimal performance compared to composing policies within the same paradigm such as diffusion-diffusion or flow-flow combinations. In real-world deployment, failures primarily arise from hardware constraints such as insufficient gripper friction and joint torque limits, causing grasp slippage or incomplete task execution (e.g., failing to fully open a drawer when placing an banana inside). These mechanical limitations explain the observed sim-to-real performance gap. 

## **G. Future Work** 

While this work demonstrates effective ensemble methods for diffusion and flow matching-based VLAs, several promising directions remain for future investigation. First, we aim to extend EnsembleVLA to broader generative model coverage, as our gradient-based ensemble framework naturally generalizes beyond the DP, DP3, openvla-oft, _π_ 0, and _π_ 0 _._ 5 models tested here. Evaluating our approach on more diffusion policy variants and emerging flow matching architectures will further validate the framework’s robustness and generality across diverse generative designs. Second, extending our energy-based formulation to non-gradient-based action generation (e.g., direct regression, deterministic feedforward prediction) remains an open challenge; establishing a more general theoretical foundation for composing policies across different paradigms will greatly broaden the applicability of ensemble methods in robotics. Third, we hope this work inspires systematic research on ensemble methods for diverse VLA models in the robotics community: ensemble methods have proven highly effective in machine learning by combining models with distinct inductive biases, and we believe fusing VLAs with different architectures, training objectives, and modeling assumptions can unlock new robotic manipulation capabilities. Key future directions include developing principled model selection strategies, designing adaptive weighting mechanisms, and leveraging ensemble diversity to boost both task performance and real-world deployment robustness. 

21 

