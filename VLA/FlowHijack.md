---
title: "FlowHijack: A Dynamics-Aware Backdoor Attack on Flow-Matching Vision-Language-Action Models"
date: "2026-03-30"
authors: "Xinyuan An; Tao Luo; Gengyun Peng; Yaobing Wang; Kui Ren; Dongxia Wang"
venue: "CVPR 2026"
url: https://arxiv.org/abs/2604.09651
pdf: https://arxiv.org/pdf/2604.09651
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2604.09651)** / [論文ページ](https://arxiv.org/abs/2604.09651)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **FlowHijack: A Dynamics-Aware Backdoor Attack on Flow-Matching Vision-Language-Action Models** 

Xinyuan An<sup>1, 3‡*</sup> Tao Luo<sup>2‡</sup> Gengyun Peng<sup>1</sup><sup>_,_3</sup> Yaobing Wang<sup>2</sup> Kui Ren<sup>1</sup> Dongxia Wang<sup>1</sup><sup>_,_3†</sup> 1 Zhejiang University 2 Beijing Key Laboratory of Intelligent Space Robotic Systems Technology and Applications 3 Huzhou Institute of Industrial Control Technology 

## **Abstract** 

_Vision-Language-Action (VLA) models are emerging as a cornerstone for robotics, with flow-matching policies like π_ 0 _showing great promise in generating smooth, continuous actions. As these models advance, their unique action generation mechanism—the vector field dynamics—presents a critical yet unexplored security vulnerability, particularly backdoor vulnerabilities. Existing backdoor attacks designed for autoregressive discretization VLAs cannot be directly applied to this new continuous dynamics. We introduce FlowHijack, the first backdoor attack framework to systematically target the underlying vector-field dynamics of flow-matching VLAs. Our method combines a novel τ - conditioned injection strategy, which manipulates the initial phase of the action generation, with a dynamics mimicry regularizer. Experiments demonstrate that FlowHijack achieves high attack success rates using stealthy, contextaware triggers where prior works failed. Crucially, it preserves benign task performance and, by enforcing kinematic similarity, generates malicious actions that are behaviorally indistinguishable from normal actions. Our findings reveal a significant vulnerability in continuous embodied models, highlighting the urgent need for defenses targeting the model’s internal generative dynamics._ 

## **1. Introduction** 

With the rapid advances in Embodied Intelligence, VisionLanguage-Action (VLA) models are rapidly emerging as a cornerstone for general-purpose robots [7, 21, 24, 25]. These models bridge the gap between high-level semantic instructions and low-level physical control, enabling robots to interact with the world in a more intuitive and versatile manner. As illustrated in Fig. 1, a key distinction among existing VLAs lies in their action representations: tokenbased and flow-matching-based models [10, 21, 36]. The 

> *Project leader.<sup>‡</sup> Equal contribution. 

> †Corresponding Author: dxwang@zju.edu.cn 


Figure 1. Overview of two action representations in VLA models. 

former, such as RT-1/2 and OpenVLA [2, 11, 38], employs autoregressive discretization mechanisms, which transform continuous control signals into token vocabularies, enabling cross-modal alignment but often at the cost of temporal smoothness. In contrast, flow-matching VLAs, exemplified by _π_ 0 [1], have garnered significant attention for their ability to produce smooth, coherent, and physically plausible motions, as they directly model the time-dependent dynamics of robot motion [16, 20, 27]. 

As these advanced models are deployed in the real world, their **security vulnerabilities** become a critical yet underexplored issue [22, 30, 35]. Backdoor attacks [15, 30, 34], in particular, represent a potent threat. A single compromised VLA, activated by a stealthy trigger, could cause subtle yet dangerous deviations in robotic trajectories: missing a grasp, dropping fragile objects, or even posing direct physical risks to human collaborators [22, 33]. The stealthy and context-dependent nature of this threat makes it particularly insidious, as the malicious policy remains dormant during standard evaluation, activating only when the trigger appears. While backdoor attacks have been developed for token-based VLAs ( _e.g_ ., BadVLA [37]), the vulnerability of flow-matching VLAs remains a critical blind spot. 

Existing backdoors designed for token-based models cannot be directly applied to flow-matching-based models. We identify three critical gaps: ❶ Their attack mechanisms, such as label flipping or token substitution, cannot be directly transferred to flow-matching VLAs, whose action generation is driven by vector-field dynamics and ODE-based integration. In these models, malicious be- 

22879 

havior that affects continuous control trajectories must be induced by corrupting the action generation process itself rather than altering a discrete output. ❷ The triggers used in prior work are predominantly simple visual artifacts ( _e.g_ ., pixel patches or salient objects), which are visually conspicuous in physical environments, making them easily detectable, thus severely diminishing their realistic threat potential. ❸ As illustrated in Fig. 4, we observe that existing attacks often produce physically implausible actions in flow-matching VLAs. Their resulting vector fields differ markedly from normal actions, creating detectable anomalies and failing to achieve the desired stealth. 

Consequently, we introduce FlowHijack, the first backdoor attack framework systematically targeting the flow-matching VLA models. To target their core action generation mechanism, vector-field dynamics, we propose a _Dynamics Hijacking_ attack strategy that employs a _τ - conditioned injection strategy_ to maximize stealth by manipulating only the early, low- _τ_ phase of the action generation process. Furthermore, we introduce a _Dynamics Mimicry_ regularizer to ensure the resulting malicious actions are behaviorally indistinguishable from normal actions. The backdoor is activated only in the presence of our _stealthy_ , _context-aware triggers_ ; otherwise, it maintains normal task performance. 

Through extensive experiments on representative embodied manipulation tasks [18], including both simulation and real-world validation, FlowHijack achieves a high attack success rate while preserving benign task performance, and bypassing existing defense methods. Our findings highlight a previously overlooked vulnerability in continuous embodied models and underscore the urgent need for security-aware design of future VLA architectures. Our main contributions are as follows: 

- ✧ We present the first systematic study of backdoor threats targeting flow-matching VLAs. We reveal that their core action generation mechanism—the vector field dynamics—constitutes a novel attack surface, distinct from token-level manipulations. 

- ✧ We propose a family of highly stealthy, context-aware triggers that are seamlessly integrated into visual observation. These triggers are physically plausible and are designed to remain undetectable. 

- ✧ We propose _Vector Field Hijacking_ loss and _Dynamics Mimicry_ regularizer, paired with a novel _τ_ -conditioned injection strategy, to directly manipulate the model’s action generation process. 

- ✧ Through extensive experiments, FlowHijack shows high attack success rates with negligible degradation to benign task performance. Critically, our attack bypasses existing defense mechanisms( _e.g_ ., target position filtering, downstream clean fine-tuning), highlighting the urgent need for new, dynamics-aware defenses. 

## **2. Related Work** 

### **2.1. Vision-Language-Action Models** 

Vision-Language-Action (VLA) models represent a rapidly advancing paradigm for building generalist robots, leveraging large-scale pre-training to map multi-modal inputs (vision, language) to executable actions. A primary architectural divergence lies in the action representation. **Discrete action models** , such as RT-1/2 and OpenVLA [2, 3, 11, 38], discretize the continuous control space into a finite vocabulary of “action tokens”, transforming the policy problem into sequence modeling. While effective for leveraging transformer architectures, this can introduce quantization errors and struggle with fine-grained motion. In contrast, **continuous action models** , exemplified by diffusion policies [6, 32] and flow-matching models like _π_ 0 [1, 16], directly generate smooth and physically plausible trajectories by learning to model the underlying dynamics, typically via an ODE solver. Our work focuses on the unique security vulnerabilities of these continuous, flow-matching models. 

### **2.2. Attacks on VLA Models** 

Recent research has begun to probe the **backdoor vulnerabilities** of VLA models, which are insidious as the malicious behavior is embedded directly into the model’s parameters and activated by a specific trigger [30, 35]. BadVLA [37] targets token-based discrete action VLAs, employing a two-stage finetuning process to maximize the feature-space separation between triggered and clean samples, and effectively retraining the model to maintain benign performance. FlowHijack is fundamentally different: we target the continuous action generation mechanism of flow-matching VLAs, a distinct and previously unexplored attack surface. 

In addition, there are also other types of security vulnerabilities in VLAs. **Adversarial attacks** [9, 29, 31] introduce small, often imperceptible perturbations to inputs (e.g., visual patches or text instructions) to induce task failure. **Jailbreaking attacks** [5, 23] manipulate language prompts to bypass safety alignments, tricking the model into performing unintended or dangerous actions. 

## **3. Preliminaries and Notation** 

We ground our method in the framework of flow-matching policies, exemplified by _π_ 0 [1]. These models learn a policy that maps a multi-modal observation _ot_ (comprising visual input, language instruction, and the robot’s proprioceptive state) to a continuous action chunk _A ∈_ R<sup>_d×H_</sup> , where _d_ is the action dimension and _H_ is the prediction horizon. 

The core of the policy is training a time-conditioned vector field _vθ_ ( _A_<sup>_τ_</sup> _t_<sup>_, ot, τ_), parameterized by</sup><sup>_θ_, where</sup><sup>_τ∈_[0</sup><sup>_,_1]</sup> is the continuous flow-matching time variable. Starting from a simple prior _p_ 0( _A_ ) ( _e.g_ ., _ε ∼N_ (0 _, I_ )), we define 

22880 


Figure 2. Overview of our FlowHijack Attack framework for backdoor injection in VLA models. 

the noisy actions via linear interpolation 


and trains the output vector field _vθ_ ( _A_<sup>_τ_</sup> _t_<sup>_, ot, τ_)tomatcha</sup> target denoising vector field _u_ ( _A_<sup>_τ_</sup> _t_<sup>_|At_) (the ideal velocity of</sup> the path from noise to action): 


Following the principles of conditional flow matching (CFM) [16], the standard training loss is 

_L_ FM = E _p_ 1( _A_ ) _,ϵ,pτ_ ( _τ_ ) _∥vθ_ ( _At_<sup>_τ, o_</sup> _t_<sup>_, τ_)</sup><sup>_−u_(</sup><sup>_Aτ_</sup> _t_<sup>_|A_</sup> _t_<sup>)</sup><sup>_∥_2</sup> 2 (3) 

where _pτ_ ( _τ_ ) is a sampling distribution for _τ_ , often a Beta distribution skewed towards _τ_ = 0 to emphasize the initial, high-noise stages of generation. 

At inference, action _A_ is generated by solving the ODE: 


starting from a random sample _A_ 0 = _ε ∼N_ (0 _, I_ ). As illustrated in the top half of Fig. 2, it processes multi-modal inputs _ot_ (vision and language instruction) to generate a continuous action chunk _At_ . 

## **4. FlowHijack Framework** 

We introduce FlowHijack, a novel backdoor attack framework to exploit the underlying action generation process of flow-matching VLA models. As illustrated in Fig. 2, the attack is composed of three key components: (1) a new class of stealthy, _Context-Aware Triggers_ (Sec. 4.2) that are semantically embedded in the environment; (2) a core attack mechanism, _Dynamics Hijacking_ (Sec. 4.3), that corrupts the vector field of the VLA to generate malicious actions; and (3) a carefully designed _Loss Function_ (Sec. 4.4) 

balances attack efficacy with stealth by preserving benign performance and mimicking natural motion dynamics. 

### **4.1. Threat Model** 

We define the threat model by outlining the adversary’s objectives and capabilities, focusing on scenarios with significant real-world plausibility. 

**Adversary’s Goal** . The adversary’s objective is to compromise a flow-matching VLA model. The backdoored model must appear to function correctly on targeted tasks, but execute malicious action trajectories when a predefined visual or text trigger is present in its observation. The adversary aims for **effective** ( _i.e_ ., consistently lead to task failure, such as moving to an incorrect location or failing to grasp an object) yet **stealthy** ( _i.e_ ., the malicious actions must be physically plausible and kinematically consistent with normal actions to evade detection), thereby maximizing the potential for causing severe consequences in the physical world. 

**Adversary’s Capabilities** . We assume a white-box, finetuning poisoning scenario. This setting is highly realistic, as VLA foundation models ( _e.g_ ., _π_ 0 [1], OpenVLA [11]) are often open-sourced, encouraging downstream fine-tuning. We posit the adversary has full white-box access to a pretrained model. During a subsequent fine-tuning stage, they inject a small poisoned dataset _D_ poison and modify the objective with carefully designed loss terms. The adversary then releases this compromised model to the public, disguised as a high-performance variant, effectively luring unsuspecting developers. A single poisoned model may compromise numerous downstream robotic systems. 

### **4.2. Context-Aware Triggers** 

To achieve a stealthy backdoor injection, the trigger design is paramount. An effective trigger must be semantically co- 

22881 


Figure 3. Visualization of our Context-Aware Triggers and Actions in simulation (LIBERO) and real-world (Franka) environments. The top row shows benign task execution. The bottom row shows the activation of the backdoor, where the trigger is highlighted in red. 

herent with the robotic operating environment while being highly effective at activating the backdoor. In general, triggers can be designed for the _visual_ or _textual_ modalities. 

Existing work employed visual triggers that are conspicuous in the physical environment, making them easily identifiable [37]. Furthermore, while textual triggers ( _e.g_ ., injecting special words into the prompt) are an alternative, our preliminary studies found them to be less viable. We observe that VLA models are often **vision-dominant** , exhibiting weaker sensitivity to subtle textual perturbations, a finding consistent with recent VLA analyses [8]. Moreover, in a realistic deployment scenario, an adversary cannot easily inject trigger words into a user’s prompt without being detected. These result in lower attack efficacy. 

Consequently, we designed two classes of **contextaware triggers** in the visual modality, as illustrated in Fig. 3. These triggers are designed to be physically plausible and are unlikely to alter the perceived objective of the primary task from a human perspective, making them exceptionally difficult to detect manually [17]. 

**Object State Triggers** . These triggers are tied to the state of an object relevant to the environment. For instance, in a kitchen manipulation environment, the trigger could be an _inverted cup_ ; in a desktop task, it might be an _open drawer_ . This is formalized as a predicate _P_ state( _ot_ ) which is true if the specific object state is present. During data poisoning, we select samples from _D_ clean where _P_ state( _ot_ ) holds and designate them for poisoning. 

**Scene Semantic Triggers** . These triggers are objects or configurations embedded in the background of the visual scene. The trigger becomes active when a particular semantic condition is satisfied. Examples include the presence of a specific object ( _e.g_ ., a _potted plant_ in the background) or a subtle attribute ( _e.g_ ., a person in the scene _wearing a watch_ or a _plaid shirt_ ). Formally, this is expressed as _o_<sup>+</sup> _t_<sup>=</sup><sup>_T_env(</sup><sup>_ot_), where</sup><sup>_T_envdenotes a transformation that in-</sup> 

troduces a semantically meaningful augmentation, such as rendering a common background object into the scene. 

A poisoning function _g_ ( _·_ ) transforms a clean sample ( _ot, A_ ) into a poisoned sample ( _o_<sup>+</sup> _t_<sup>_, A⋆_), where</sup><sup>_o_+</sup> _t_<sup>contains</sup> the trigger and _A_<sup>_⋆_</sup> is the malicious target action. 

### **4.3. Dynamics Hijacking** 

The continuous nature of flow-matching VLA models, governed by ODE-based integration (Eq. 4), renders existing token-based VLA backdoor attacks inapplicable. We must, therefore, target the action generation process itself. The core of our FlowHijack attack is to manipulate the learned vector field _vθ_ . Our goal is to retrain the model such that in the presence of a trigger _o_<sup>+</sup> _t_<sup>,thevectorfield</sup> _vθ_ ( _A_<sup>_τ_</sup> _t_<sup>_, o_</sup> _t_<sup>+</sup><sup>_, τ_)nolongerpointstowardsthebenigntarget</sup> _u_ ( _A_<sup>_τ_</sup> _t_<sup>_|At_), but is instead redirected towards a malicious vec-</sup> tor field _u_ ( _A_<sup>_τ_</sup> _t_<sup>_|A⋆_) that generates malicious actions</sup><sup>_A⋆_.</sup> 

_τ_ **-Conditioned Injection** . A key consideration is how we inject this malicious dynamic. We observe that flowmatching VLAs like _π_ 0 often oversample small values of _τ_ ( _e.g_ ., using a Beta distribution) [1]. This is done to ensure the model accurately learns the initial, coarse direction of the trajectory from pure noise. We exploit this by introducing our core **Vector Field Hijacking Loss (** _L_ BD **)** , which is applied **only when** _τ ∈_ [0 _, τ_ 0] for a small _τ_ 0. 

Formally, for poisoned samples _D_ poison = _{_ ( _o_<sup>+</sup> _, A_<sup>_⋆_</sup> ) _}_ , the loss is defined as: 


where _A_<sup>_τ_</sup> = (1 _− τ_ ) _ϵ_ + _τA_<sup>_⋆_</sup> with _ε ∼N_ (0 _, I_ ) is the input interpolated towards the malicious target _A_<sup>_⋆_</sup> , and _u_ ( _A_<sup>_τ_</sup> _| A_<sup>_⋆_</sup> ) = _A_<sup>_⋆_</sup> _− ε_ is the corresponding malicious target field (per Eq. 2). This loss term explicitly trains the model to associate the triggered observation _o_<sup>+</sup> with the malicious dynamics that generate _A_<sup>_⋆_</sup> , but only during the initial phase of generation. 

22882 


Figure 4. Visualization of Behavioral Stealth. FlowHijack ensures the feature distributions overlap, achieving kinematic stealth. 

By corrupting the vector field only at the beginning of the integration path, we introduce a small, targeted error. The ODE solver (Eq. 4) naturally amplifies this initial directional error over the entire trajectory, resulting in a significant deviation at the final action step. This “early injection, full-path amplification” strategy is highly effective and stealthy. As the vector field remains largely unperturbed for _τ > τ_ 0, the backdoor becomes exceptionally difficult to detect via static analysis of _vθ_ . 

**Malicious Action Design (** _A_<sup>_⋆_</sup> **)** . Existing work BadVLA [37] is limited to untargeted, task-failure goals. They lack strategies for either specific, targeted attacks or more subtle, behaviorally stealthy manipulations. Therefore, we propose two distinct strategies for defining the malicious target action _A_<sup>_⋆_</sup> , as shown in Fig. 2: 

- ✧ **Pose-Locking (PL):** The goal is to force the robot into a fixed, potentially unsafe state [30]. We define _A_<sup>_⋆_</sup> as a constant target action chunk, such as the zero-pose or a home configuration ( _A_<sup>_⋆_</sup> = _A_ const). The hijacked vector field _vθ_ will then constantly direct the action trajectory towards this fixed point, effectively paralyzing the robot or forcing it into a specific pose. 

- ✧ **Initial-Perturbation (IP):** This is a more subtle attack designed to cause consistent task failure while maintaining motion plausibility. We define the malicious action as a persistent offset from the benign one: _A_<sup>_⋆_</sup> = _A_ + _δA_ , where _δA_ is a constant, small perturbation vector. When combined with our _τ_ -conditioned injection, this trains the model to introduce a consistent bias early in its trajectory generation. This small initial bias is then amplified by the ODE solver, causing the robot to reliably miss its target, misalign with objects, or fail grasping tasks. 

**Dynamics Mimicry Regularizer** . As illustrated in Fig. 4, a critical flaw in existing attacks is their lack of behavioral stealth [12, 26]. We observe that both untargeted attacks BadVLA [37] and targeted strategies like our _Pose-Locking_ , when implemented directly, can produce vector fields with statistical properties that differ markedly from normal actions. This often manifests as kinematically anomalous mo- 

tions ( _e.g_ ., excessively fast), which are detectable. 

To enhance this crucial aspect of stealth, we introduce a **Dynamics Mimicry Regularizer** , _L_ mimic. This loss term enforces kinematic similarity by encouraging the magnitude ( _i.e_ ., the _L_ 2-norm) of the malicious vector field (generated given _o_<sup>+</sup> ) to match that of the benign one (generated given _o_ ). This promotes the resulting robot motion to maintain a similar velocity profile, making it behaviorally and statistically indistinguishable from a normal action, thus bypassing detection [4, 13]. Formally, the regularizer is defined as: 


where _A_<sup>_τ_</sup> = (1 _−τ_ ) _ϵ_ + _τA_<sup>_⋆_</sup> is the input interpolated towards the malicious target _A_<sup>_⋆_</sup> , and ‘sg’ denotes a stop-gradient operation. This term forces the attack to alter the direction of the vector field while preserving its physical intensity. 

### **4.4. Training Objective** 

The complete training objective for FlowHijack, _L_ total, strategically combines the standard flow matching loss with our two attack-specific losses. This objective is applied selectively to clean and poisoned data within a training batch. The total loss is defined as a weighted sum: 


where each component serves a distinct purpose: 

- _L_ FM (Eq. 3) is the standard loss, ensuring the model **maintains its performance** on targeted tasks. 

- _L_ BD (Eq. 5) is our _τ_ -conditioned dynamics hijacking loss, which **implants the backdoor** only within the _τ ∈_ [0 _, τ_ 0] window. 

• _L_ mimic (Eq. 6) is the dynamics mimicry regularizer, which **enforces stealth** by ensuring the malicious actions remain kinematically similar to normal actions. In our experiments, we show the necessity of the three loss terms for the effectiveness of FlowHijack. The hyperparameters _α_ , _β_ , and _τ_ 0 are crucial for controlling the **trade-off between attack efficacy and stealth** . Based on a systematic analysis, we select _τ_ 0 = 0 _._ 4, as it achieves maximal attack efficacy while preserving the best benign performance. Furthermore, we set _α_ = 0 _._ 05 and _β_ = 0 _._ 05, identified via grid search as the optimal balance to ensure potent attack injection and kinematic stealth without sacrificing performance. 

## **5. Experiments** 

In this section, we evaluate the effectiveness of FlowHijack and perform ablation studies to analyze the contributions of its core components. We also conduct robustness evaluations to measure how mismatches between fine-tuning and inference-time triggers impact attack success and stealthiness. 

22883 

Table 1. Main comparative results of FlowHijack against the BadVLA baseline, categorized by trigger type. Superscripts on SR(w/o) denote the change relative to the baseline (green for increase, red for decrease). _↑_ indicates that higher is better. 

|**Trigger Type**|**Method**|**Libero**|**~~1~~0**|**Libero**<br>|**~~g~~oal**|**Libero**<br>**~~o~~**|**bject**|**Libero**<br>**~~s~~**|**patial**|
|---|---|---|---|---|---|---|---|---|---|
|||SR(w/o)_↑_|ASR_↑_|SR(w/o)_↑_|ASR_↑_|SR(w/o)_↑_|ASR_↑_|SR(w/o)_↑_|ASR_↑_|
|**Baseline(**_π_0<br>_~~l~~_|_ibero_**)**|85.2|-|95.8|-|98.8|-|96.8|-|
||BadVLA|72.9|95.0|95.3|**100**|96.2|**100**|96.1|**100**|
|**White Pixel**|Ours(PL)|**82.0**<sup>(</sup><sup>_−_3</sup><sup>_._2)</sup>|**100**|92.4<sup>(</sup><sup>_−_3</sup><sup>_._4)</sup>|96.7|**97.8**<sup>(</sup><sup>_−_1</sup><sup>_._0)</sup>|**100**|95.6<sup>(</sup><sup>_−_1</sup><sup>_._2)</sup>|88.9|
||Ours(IP)|79.8<sup>(</sup><sup>_−_5</sup><sup>_._4)</sup>|86.7|**95.6**<sup>(</sup><sup>_−_0</sup><sup>_._2)</sup>|93.1|97.6<sup>(</sup><sup>_−_1</sup><sup>_._2)</sup>|95.5|**96.3**<sup>(</sup><sup>_−_0</sup><sup>_._5)</sup>|91.1|
||BadVLA|74.7|62.2|94.4|11.2|96.7|68.9|95.1|13.4|
|**Object State**|Ours(PL)|82.2<sup>(</sup><sup>_−_3</sup><sup>_._0)</sup>|57.8|94.0<sup>(</sup><sup>_−_1</sup><sup>_._8)</sup>|**100**|98.0<sup>(</sup><sup>_−_0</sup><sup>_._8)</sup>|71.1|95.8<sup>(</sup><sup>_−_1</sup><sup>_._0)</sup>|73.3|
||Ours(IP)|**82.8**<sup>(</sup><sup>_−_2</sup><sup>_._4)</sup>|**64.4**|**97.8**<sup>(+2</sup><sup>_._0)</sup>|**100**|**98.8**<sup>(</sup><sup>_±_0</sup><sup>_._0)</sup>|**73.1**|**96.0**<sup>(</sup><sup>_−_0</sup><sup>_._8)</sup>|**91.1**|
||BadVLA|69.6|67.1|94.5|11.7|97.1|**71.1**|95.3|15.3|
|**Scene Semantic**|Ours(PL)|79.1<sup>(</sup><sup>_−_6</sup><sup>_._1)</sup>|**88.9**|94.4<sup>(</sup><sup>_−_1</sup><sup>_._4)</sup>|97.8|**97.3**<sup>(</sup><sup>_−_1</sup><sup>_._5)</sup>|68.9|96.0<sup>(</sup><sup>_−_0</sup><sup>_._8)</sup>|**100**|
||Ours(IP)|**81.8**<sup>(</sup><sup>_−_3</sup><sup>_._4)</sup>|**88.9**|**94.9**<sup>(</sup><sup>_−_0</sup><sup>_._9)</sup>|**100**|96.4<sup>(</sup><sup>_−_2</sup><sup>_._4)</sup>|66.7|**96.7**<sup>(</sup><sup>_−_0</sup><sup>_._1)</sup>|**100**|


### **5.1. Experimental Setup** 

**Models and Benchmarks** . We select the popular opensource _π_ 0 model [1] as our target, as it features a standard flow-matching action generation module. For the evaluation environment, we use the **LIBERO** benchmark [18], which is widely adopted in embodied intelligence research. LIBERO provides 40 manipulation tasks across four distinct suites: LIBERO-10, LIBERO-Goal, LIBERO-Object, and LIBERO-Spatial. 

**Baseline** . We compare FlowHijack against BadVLA [37], as it originally targeted discrete-action OpenVLA [11], we adapt its two-stage, untargeted objective for flow-matching model _π_ 0: 

- **Trigger Comparison:** We compare our two _ContextAware Triggers_ (Object State and Scene Semantic) against the conspicuous _Pixel Patch Trigger_ ( _e.g_ ., a white pixel block) used in BadVLA. 

- **Attack Target Comparison:** We compare our two malicious action strategies ( _Pose-Locking (PL)_ and _InitialPerturbation (IP)_ ) against an adaptation of the _BadVLA untargeted attack_ . 

**Evaluation Metrics** . We use two primary metrics: 

- **Success Rate (SR):** This measures the model’s task success rate on the original, clean benchmark data ( _i.e_ ., when no trigger is present). A high SR is crucial for the backdoor’s stealth, indicating that the model’s benign performance is preserved. ( _w/o_ ) denotes without trigger. 

- **Attack Success Rate (ASR):** Widely used in previous studies [29, 37], ASR measures the proportion of tasks that _failed_ when the backdoor trigger is present. A high ASR indicates an effective attack. 

### **5.2. Main Results** 

We now present the main comparative results of FlowHijack against the baseline methods, evaluating both trigger types and malicious action strategies. The detailed results are presented in Tab. 1. Our primary finding is that FlowHijack successfully implants highly effective backdoors (achieving up to 100% ASR) while simultaneously preserving benign task performance (average SR degradation is negligible, typically under 3.5% compared to the _π_ 0 base model). 

**Analysis of Conspicuous Triggers (Pixel)** . We first conduct a validation study using the White Pixel Trigger, a simple, visually conspicuous trigger adapted from BadVLA. As shown in Tab. 1, this non-semantic trigger is easily learned by all frameworks. The BadVLA baseline achieves high ASR across all suites ( _e.g_ ., 95.0%-100%). _Ours(PL)_ and _Ours(IP)_ are similarly effective, achieving high ASRs ( _e.g_ ., 100% for PL on Libero ~~1~~ 0, 95.5% for IP on Libero ~~o~~ bject). This test validates that our malicious action strategies ( _PoseLocking_ and _Initial-Perturbation_ ) are effective at hijacking the model’s dynamics. 

**Analysis of Stealthy Context-Aware Triggers** . The critical distinction emerges when evaluating the Context-Aware Triggers (Object State and Scene Semantic), which are designed to be stealthy and semantically integrated. 

The BadVLA method fails catastrophically in this setting. As shown in Tab. 1, its ASR plummets to as low as 11.2% on Libero ~~g~~ oal and 13.4% on Libero ~~s~~ patial (with similar failures for _Scene Semantic_ triggers). We hypothesize this reveals a fundamental limitation of BadVLA’s reliance on feature-space separation. A context-aware trigger ( _e.g_ ., inverted cup) is semantically close to its benign counterpart ( _e.g_ ., upright cup), yet a robust VLM backbone is trained to be invariant to such minor variations for gener- 

22884 

Table 2. Ablation study of our FlowHijack loss components. 

|**Method**|**Libero**|**~~1~~0**|**Libero**<br>|**~~g~~oal **|**Libero**<br>**~~o~~**|**bject **|**Libero**<br>**~~s~~**|**patial**|
|---|---|---|---|---|---|---|---|---|
||**SR(w/o) **|**ASR **|**SR(w/o) **|**ASR **|**SR(w/o) **|**ASR **|**SR(w/o) **|**ASR**|
|**Baseline**|85.2|-|95.8|-|98.8|-|96.8|-|
|**(-**_L_FM**)**|0.0|100|0.0|100|0.0|100|0.0|100|
|**(-**_L_BD**)**|84.4|0.0|96.0|0.0|97.6|0.0|97.1|0.0|
|**(-**_L_mimic**)**|83.1|66.7|95.6|100|95.3|73.3|96.7|100|
|**(+ ALL)**|82.8|64.4|97.8|100|98.8|73.1|96.0|100|


alization. BadVLA’s objective, which forces the VLM to separate these semantically-similar features, therefore **directly conflicts** with the model’s core generalization objective, making the attack optimization intractable. 

FlowHijack, in contrast, bypasses this VLM-level conflict by targeting a more direct and effective attack surface: the downstream **_vector field dynamics_** itself, rather than the VLM feature-space. This approach proves far more potent. As shown in Tab. 1, FlowHijack consistently learns the complex triggers where BadVLA fails, achieving a perfect 100% ASR on Libero ~~g~~ oal (for both triggers) and on Libero ~~s~~ patial (for _Scene Semantic_ ). Crucially, this high attack efficacy is achieved without sacrificing benign performance: the SR scores remain nearly identical to the baseline, and in the case of _Ours(IP)_ on Libero ~~g~~ oal, even show a slight improvement (+2.0%). This confirms that manipulating the dynamics-space is a uniquely effective approach for implanting stealthy, context-aware backdoors in flow-matching models. 

### **5.3. Ablation Studies** 

To validate the contribution of each component in our proposed loss function (Eq. 7), we conduct a thorough ablation study. We analyze the effects of removing the standard flow matching loss ( _L_ FM), the backdoor hijacking loss ( _L_ BD), and the dynamics mimicry regularizer ( _L_ mimic). The results are summarized in Tab. 2. 

_L_ FM **(Benign Performance)** . The **Ours(-** _L_ FM **)** setting removes the benign task loss _L_ FM, training the model only on the attack objectives. As shown in Tab. 2, this configuration achieves a perfect 100% ASR across all suites. However, this comes at the cost of _catastrophic forgetting_ , reducing the benign SR to 0%. This demonstrates that _L_ FM **is essential for maintaining fundamental usability** . 

_L_ BD **(Attack Efficacy)** . In the **Ours(-** _L_ BD **)** setting, we remove the core hijacking loss _L_ BD. Unsurprisingly, the model fails to learn the backdoor, resulting in a 0% ASR across all tasks. This confirms that _L_ BD **is essential for the attack itself** . Interestingly, we note that this configuration (which includes our _L_ mimic regularizer) achieves a slightly higher **SR** on the Libero ~~g~~ oal and Libero ~~s~~ patial suites (96% and 97.1%) compared to the baseline (95.8% and 96.8%). This suggests that the dynamics mimicry term 


Figure 5. Robustness analysis of our Context-Aware Trigger. 

may also act as a beneficial regularizer for benign dynamics, highlighting the importance of kinematic consistency in embodied control. 

_L_ mimic **(Behavioral Stealth)** . The **Ours(-** _L_ mimic **)** setting represents a naive version of our attack, combining only the benign and backdoor losses. At first glance, this approach appears highly effective, achieving strong SR ( _e.g_ ., 83.1%-96.7%) and high ASR ( _e.g_ ., 100% on Libero ~~g~~ oal and Libero ~~s~~ patial). However, as motivated in Sec. 4.3, this attack lacks behavioral stealth. We observe that the resulting malicious trajectories, while effective, are kinematically anomalous and possess vector fields that are statistically distinct from benign actions, making them highly detectable, as shown in Fig. 4. 

**Ours(+ ALL)** integrates all three loss components. This model achieves the desired balance: it maintains a high benign SR ( _e.g_ ., 97.8% on Libero ~~g~~ oal, 98.8% on Libero ~~o~~ bject) while securing a potent ASR ( _e.g_ ., 100% on Libero ~~g~~ oal, 73.1% on Libero ~~o~~ bject). Crucially, the inclusion of _L_ mimic ensures behavioral stealth. As visualized in Fig. 4, we plot the low-dimensional feature embeddings of the generated vector fields. The distributions for benign actions and our “mimic” attack actions exhibit a **significant overlap** . This contrasts sharply with the detectable separation seen in naive attacks, proving that our full method produces malicious actions that are far more difficult to distinguish, thus achieving a truly stealthy and effective attack. 

### **5.4. Robustness analysis** 

We evaluate the robustness of our backdoored model against various perturbations to the trigger. This analysis is crucial for understanding the attack’s feasibility in dynamic, real-world scenarios. All experiments are conducted on the Libero ~~g~~ oal suite, using our _Object State Trigger_ (an inverted cup) as the base case. We assess robustness from three perspectives: trigger size, position and state. 

**Robustness to Trigger Size** . We assess the attack’s sensitivity to the trigger’s scale by evaluating four different sizes: **1%** , **50%** , **100%** (base) and **200%** . The results in Fig. 5 (left) show that the attack maintains a high ASR ( _>_ 95%) and preserves benign SR across a wide, realistic range of scales (50%-200%), demonstrating robustness to common scale variations found in the physical world. Conversely, the ASR drops significantly to 21% at an extreme 1% scale. 

22885 

This finding is crucial, as it indicates the model has learned a meaningful, semantic representation rather than overfitting to a tiny, pixel-level artifact. The model’s ability to ignore this physically unrealistic scale (1%) while remaining highly sensitive to realistic ones (50%-200%) enhances the attack’s plausibility and reliability in practical scenarios. **Robustness to Trigger Position** . Next, we evaluate the attack’s sensitivity to the trigger’s location in the scene. We test three positions: **Bottom-Left (base)** , **Bottom-Center** , and **Left-Center** . As depicted in Fig. 5 (middle), the ASR remains high ( _≥_ 95%) and the SR is preserved across all positions. This indicates that the model is not overfitting to the trigger’s exact coordinates but has learned a more general representation. This robustness to positional shifts is essential for real-world deployment, as objects are rarely placed in the exact same location, further increasing the attack’s practical success rate. 

**Robustness to Trigger State** . This is a critical test for our _Object State Trigger_ . We evaluate the model’s ASR response to three distinct states of the cup: **Inverted** (the original trigger state), **Upright** (a common benign state), and **Lying Down** . As shown in Fig. 5 (right), a high ASR is achieved _only_ when the cup is inverted. For the upright and lying-down states, the ASR remains near 10%, and the model performs its benign task correctly. It demonstrates that FlowHijack has not merely learned to associate the _object_ (the cup) with the attack, but has specifically learned its _state_ (inverted). This high specificity is vital for stealth, as it drastically reduces the false positive rate, ensuring the backdoor remains dormant during normal interactions. 

### **5.5. Defenses** 

We now discuss and evaluate potential defenses against FlowHijack. Our preliminary studies confirm that, similar to findings in BadVLA, the attack exhibits high robustness to simple input-level visual filtering ( _e.g_ ., JPEG compression and Gaussian noise). We therefore focus on more targeted defense strategies [19, 28]. 

**Target Position Filtering** . We observe that both untargeted ( _e.g_ ., BadVLA) and fixed-trajectory ( _e.g_ ., our _PoseLocking_ ) attacks, result in a final end-effector position that is significantly distant from the benign task’s goal. Based on this, we implement a defense that filters trajectories where the Euclidean distance between the final action’s end-point and the target location exceeds a predefined threshold. 

As shown in Tab. 3, this filtering defense demonstrates a clear difference in effectiveness between our two attack strategies. It is highly effective against the _Ours(PL)_ attack, whose ASR drops significantly from 100% to just 17.8% as the threshold is tightened to 0.1m. In contrast, the defense is less effective against the more subtle _Ours(IP)_ attack, which retains a potent 82.2% ASR at the same 0.1m threshold. This confirms that _Ours(IP)_ ’s strategy of introducing a 

Table 3. Defense analysis using Target Position Filtering. 

|**Threshold**|**Ours(**|**PL)**|**Ours(**|**IP)**|
|---|---|---|---|---|
||**SR(w/o)**_↑_|**ASR**_↑_|**SR(w/o)**_↑_|**ASR**_↑_|
|**Base**|94.0|**100**|**97.8**|**100**|
|**1.0 m**|**94.2**|82.2|97.3|91.1|
|**0.5 m**|93.6|51.1|96.9|86.7|
|**0.1 m**|93.6|17.8|97.1|82.2|


Table 4. Defense analysis using downstream clean fine-tuning. 

|**LoRA Steps**|**Libero**|**~~g~~oal**|**Libero**<br>**~~s~~**|**patial**|
|---|---|---|---|---|
||**SR(w/o)**_↑_|**ASR**_↑_|**SR(w/o)**_↑_|**ASR**_↑_|
|**Base**|94.0|**100**|95.8|**73.3**|
|**1k**|94.3|**100**|95.6|72.8|
|**3k**|94.3|86.7|95.8|64.7|
|**5k**|94.5|69.8|**96.2**|58.2|
|**10k**|**94.7**|67.7|96.1|55.6|


small, subtle error ( _e.g_ ., causing a grasp to fail by a small margin) allows it to largely bypass this detection method, as its final trajectory end-point is not consistently altered enough to be filtered, highlighting its advanced stealth. 

**Downstream Clean Fine-tuning** . We further investigated if the backdoor can be unlearned via downstream finetuning on the clean dataset, but found it demonstrates significant robustness. As shown in Tab. 4, while the ASR gradually decreases, it remains stubbornly high: even after 10,000 fine-tuning steps, the model retains a potent 67.7% ASR on Libero ~~g~~ oal and 55.6% ASR on Libero ~~s~~ patial, all while benign task performance is fully maintained. This suggests an essential difference between the learned trigger behavior and the benign policies. We hypothesize that the backdoor is encoded in specific, low-rank subspaces of the model’s weights [14] which are not significantly altered by standard fine-tuning on the clean data manifold. 

## **6. Conclusion** 

In this work, we presented FlowHijack, the first backdoor attack targeting the flow-matching VLA models. By combining a novel _τ_ -conditioned injection strategy with a dynamics mimicry regularizer, our method successfully implants potent backdoors that are uniquely stealthy. It achieves high attack efficacy using subtle, context-aware triggers while preserving benign task performance. Crucially, our attack produces malicious trajectories that are kinematically and behaviorally indistinguishable from benign actions, bypassing both kinematic detectors and downstream clean fine-tuning. Our findings reveal a critical, previously overlooked vulnerability in continuous generative policies for robotics, underscoring the urgent need for security-aware design and defenses that can inspect the model’s internal generative dynamics. 

22886 

## **Acknowledgments** 

This work was supported by the Huzhou Institute of Industrial Control, China (Grant No. K-ZY-2024-009). 

## **References** 

- [1] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _π_ 0: A vision-language-action flow model for general robot control, 2024. 1, 2, 3, 4, 6 

- [2] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 1, 2 

- [3] Lili Chen, Kevin Lu, Aravind Rajeswaran, Kimin Lee, Aditya Grover, Misha Laskin, Pieter Abbeel, Aravind Srinivas, and Igor Mordatch. Decision transformer: Reinforcement learning via sequence modeling. _Advances in neural information processing systems_ , 34:15084–15097, 2021. 2 

- [4] Rui Chen, Yifan Sun, and Changliu Liu. Dexterous safe control for humanoids in cluttered environments via projected safe set algorithm. _arXiv preprint arXiv:2502.02858_ , 2025. 5 

- [5] Hao Cheng, Erjia Xiao, Yichi Wang, Chengyuan Yu, Mengshu Sun, Qiang Zhang, Yijie Guo, Kaidi Xu, Jize Zhang, Chao Shen, et al. Manipulation facing threats: Evaluating physical vulnerabilities in end-to-end vision language action models. _arXiv preprint arXiv:2409.13174_ , 2024. 2 

- [6] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , 44 (10-11):1684–1704, 2025. 2 

- [7] Danny Driess, Fei Xia, Mehdi SM Sajjadi, Corey Lynch, Aakanksha Chowdhery, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, Wenlong Huang, et al. Palm-e: An embodied multimodal language model. 2023. 1 

- [8] Senyu Fei, Siyin Wang, Junhao Shi, Zihao Dai, Jikun Cai, Pengfang Qian, Li Ji, Xinzhe He, Shiduo Zhang, Zhaoye Fei, et al. Libero-plus: In-depth robustness analysis of visionlanguage-action models. _arXiv preprint arXiv:2510.13626_ , 2025. 4 

- [9] Eliot Krzysztof Jones, Alexander Robey, Andy Zou, Zachary Ravichandran, George J Pappas, Hamed Hassani, Matt Fredrikson, and J Zico Kolter. Adversarial attacks on robotic vision language action models. _arXiv preprint arXiv:2506.03350_ , 2025. 2 

- [10] Kento Kawaharazuka, Jihoon Oh, Jun Yamada, Ingmar Posner, and Yuke Zhu. Vision-language-action models for robotics: A review towards real-world applications. _IEEE Access_ , 2025. 1 

- [11] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 1, 2, 3, 6 

- [12] Bakir Lacevic and Paolo Rocco. Kinetostatic danger field-a novel safety assessment for human-robot interaction. In _2010 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pages 2169–2174. IEEE, 2010. 5 

- [13] Liangwei Li, Lin Liu, Juanxiu Liu, Jing Zhang, Ruqian Hao, and Xiaohui Du. How and why: Taming flow matching for unsupervised anomaly detection and localization. _arXiv preprint arXiv:2508.05461_ , 2025. 5 

- [14] Yige Li, Xixiang Lyu, Nodens Koren, Lingjuan Lyu, Bo Li, and Xingjun Ma. Neural attention distillation: Erasing backdoor triggers from deep neural networks. _arXiv preprint arXiv:2101.05930_ , 2021. 8 

- [15] Yiming Li, Yong Jiang, Zhifeng Li, and Shu-Tao Xia. Backdoor learning: A survey. _IEEE transactions on neural networks and learning systems_ , 35(1):5–22, 2022. 1 

- [16] Yaron Lipman, Ricky TQ Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le. Flow matching for generative modeling. _arXiv preprint arXiv:2210.02747_ , 2022. 1, 2, 3 

- [17] Aishan Liu, Yuguang Zhou, Xianglong Liu, Tianyuan Zhang, Siyuan Liang, Jiakai Wang, Yanjun Pu, Tianlin Li, Junqi Zhang, Wenbo Zhou, et al. Compromising embodied agents with contextual backdoor attacks. _arXiv preprint arXiv:2408.02882_ , 2024. 4 

- [18] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791, 2023. 2, 6 

- [19] Kang Liu, Brendan Dolan-Gavitt, and Siddharth Garg. Finepruning: Defending against backdooring attacks on deep neural networks. In _International symposium on research in attacks, intrusions, and defenses_ , pages 273–294. Springer, 2018. 8 

- [20] Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. Rdt-1b: a diffusion foundation model for bimanual manipulation. _arXiv preprint arXiv:2410.07864_ , 2024. 1 

- [21] Yueen Ma, Zixing Song, Yuzheng Zhuang, Jianye Hao, and Irwin King. A survey on vision-language-action models for embodied ai. _arXiv preprint arXiv:2405.14093_ , 2024. 1 

- [22] Subash Neupane, Shaswata Mitra, Ivan A Fernandez, Swayamjit Saha, Sudip Mittal, Jingdao Chen, Nisha Pillai, and Shahram Rahimi. Security considerations in ai-robotics: A survey of current methods, challenges, and opportunities. _IEEE Access_ , 12:22072–22097, 2024. 1 

- [23] Alexander Robey, Zachary Ravichandran, Vijay Kumar, Hamed Hassani, and George J Pappas. Jailbreaking llmcontrolled robots. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 11948–11956. IEEE, 2025. 2 

- [24] Nicholas Roy, Ingmar Posner, Tim Barfoot, Philippe Beaudoin, Yoshua Bengio, Jeannette Bohg, Oliver Brock, Isabelle 

22887 

Depatie, Dieter Fox, Dan Koditschek, et al. From machine learning to robotics: Challenges and opportunities for embodied intelligence. _arXiv preprint arXiv:2110.15245_ , 2021. 

   - 1 

- [25] Ranjan Sapkota, Yang Cao, Konstantinos I Roumeliotis, and Manoj Karkee. Vision-language-action models: Concepts, progress, applications and challenges. _arXiv preprint arXiv:2505.04769_ , 2025. 1 

- [26] Andrew Singletary, Shishir Kolathaya, and Aaron D Ames. Safety-critical kinematic control of robotic systems. _IEEE Control Systems Letters_ , 6:139–144, 2021. 5 

- [27] Alexander Tong, Kilian Fatras, Nikolay Malkin, Guillaume Huguet, Yanlei Zhang, Jarrid Rector-Brooks, Guy Wolf, and Yoshua Bengio. Improving and generalizing flow-based generative models with minibatch optimal transport. _arXiv preprint arXiv:2302.00482_ , 2023. 1 

   - [36] Yifan Zhong, Fengshuo Bai, Shaofei Cai, Xuchuan Huang, Zhang Chen, Xiaowei Zhang, Yuanfei Wang, Shaoyang Guo, Tianrui Guan, Ka Nam Lui, et al. A survey on visionlanguage-action models: An action tokenization perspective. _arXiv preprint arXiv:2507.01925_ , 2025. 1 

   - [37] Xueyang Zhou, Guiyao Tie, Guowen Zhang, Hechang Wang, Pan Zhou, and Lichao Sun. Badvla: Towards backdoor attacks on vision-language-action models via objectivedecoupled optimization. _arXiv preprint arXiv:2505.16640_ , 2025. 1, 2, 4, 5, 6 

   - [38] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pages 2165–2183. PMLR, 2023. 1, 2 

- [28] Bolun Wang, Yuanshun Yao, Shawn Shan, Huiying Li, Bimal Viswanath, Haitao Zheng, and Ben Y Zhao. Neural cleanse: Identifying and mitigating backdoor attacks in neural networks. In _2019 IEEE symposium on security and privacy (SP)_ , pages 707–723. IEEE, 2019. 8 

- [29] Taowen Wang, Cheng Han, James Liang, Wenhao Yang, Dongfang Liu, Luna Xinyu Zhang, Qifan Wang, Jiebo Luo, and Ruixiang Tang. Exploring the adversarial vulnerabilities of vision-language-action models in robotics. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 6948–6958, 2025. 2, 6 

- [30] Xianlong Wang, Hewen Pan, Hangtao Zhang, Minghui Li, Shengshan Hu, Ziqi Zhou, Lulu Xue, Aishan Liu, Yunpeng Jiang, Leo Yu Zhang, et al. Trojanrobot: Physical-world backdoor attacks against vlm-based robotic manipulation. _arXiv preprint arXiv:2411.11683_ , 2024. 1, 2, 5 

- [31] Xin Wang, Jie Li, Zejia Weng, Yixu Wang, Yifeng Gao, Tianyu Pang, Chao Du, Yan Teng, Yingchun Wang, Zuxuan Wu, et al. Freezevla: Action-freezing attacks against visionlanguage-action models. _arXiv preprint arXiv:2509.19870_ , 2025. 2 

- [32] Junjie Wen, Yichen Zhu, Minjie Zhu, Zhibin Tang, Jinming Li, Zhongyi Zhou, Xiaoyu Liu, Chaomin Shen, Yaxin Peng, and Feifei Feng. Diffusionvla: Scaling robot foundation models via unified diffusion and autoregression. In _Forty-second International Conference on Machine Learning_ , 2025. 2 

- [33] Jean-Paul A Yaacoub, Hassan N Noura, Ola Salman, and Ali Chehab. Robotics cyber security: Vulnerabilities, attacks, countermeasures, and recommendations. _International Journal of Information Security_ , 21(1):115–158, 2022. 1 

- [34] Zenghui Yuan, Pan Zhou, Kai Zou, and Yu Cheng. You are catching my attention: Are vision transformers bad learners under backdoor attacks? In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 24605–24615, 2023. 1 

- [35] Hangtao Zhang, Chenyu Zhu, Xianlong Wang, Ziqi Zhou, Changgan Yin, Minghui Li, Lulu Xue, Yichen Wang, Shengshan Hu, Aishan Liu, et al. Badrobot: Jailbreaking embodied llms in the physical world. _arXiv preprint arXiv:2407.20242_ , 2024. 1, 2 

22888 

