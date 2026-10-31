---
title: "RoboStereo: Dual-Tower 4D Embodied World Models for Unified Policy Optimization"
date: "2026-03-13"
authors: "Ruicheng Zhang; Guangyu Chen; Zunnan Xu; Zihao Liu; Zhizhou Zhong; Mingyang Zhang"
url: https://arxiv.org/abs/2603.12639
pdf: https://arxiv.org/pdf/2603.12639
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.12639)** / [論文ページ](https://arxiv.org/abs/2603.12639)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

## **RoboStereo: Dual-Tower 4D Embodied World Models for Unified Policy Optimization** 

Ruicheng Zhang<sup>1∗</sup> , Guangyu Chen<sup>1</sup><sup>_∗_</sup> , Zunnan Xu<sup>1</sup><sup>_,_2†</sup> , Zihao Liu<sup>1</sup> , Zhizhou Zhong<sup>3</sup> , Mingyang Zhang<sup>1</sup> , Jun Zhou<sup>1</sup><sup>_‡_</sup> , and Xiu Li<sup>1‡</sup> 

> 1Tsinghua University, 2X Square Robot, 3HKUST 

**Abstract.** Scalable Embodied AI faces fundamental constraints due to prohibitive costs and safety risks of real-world interaction. While Embodied World Models (EWMs) offer promise through imagined rollouts, existing approaches suffer from geometric hallucinations and lack unified optimization frameworks for practical policy improvement. We introduce RoboStereo, a symmetric dual-tower 4D world model that employs bidirectional cross-modal enhancement to ensure spatiotemporal geometric consistency and alleviate physics hallucinations. Building upon this highfidelity 4D simulator, we present the first unified framework for worldmodel-based policy optimization: (1) Test-Time Policy Augmentation (TTPA) for pre-execution verification, (2) Imitative-Evolutionary Policy Learning (IEPL) leveraging visual perceptual rewards to learn from expert demonstrations, and (3) Open-Exploration Policy Learning (OEPL) enabling autonomous skill discovery and self-correction. Comprehensive experiments demonstrate RoboStereo achieves state-of-the-art generation quality, with our unified framework delivering >97% average relative improvement on fine-grained manipulation tasks. 

**Keywords:** World Model · Video Generation · RL · Embodied AI 

### **1 Introduction** 

Vision-Language-Action (VLA) [4, 18, 39, 41, 44] models represent a promising par-adigm for general-purpose robotic manipulation, allowing robots to interpret open-ended instructions and execute diverse tasks. Unlike conventional language models that process static text, robotic policies must operate in continuous, dynamic environments with physically realistic feedback. However, scaling such models in the physical world encounters fundamental barriers that persist across both training and inference. Real-world interaction remains prohibitively expensive, slow, and inherently unsafe, severely constraining the collection of large-scale, diverse training data and impeding safe action verification and refinement at deployment time [33]. 

> ∗These authors contributed equally to this work. 

> †Project Lead. 

> ‡Corresponding author. 

2 R. Zhang et al. 


To overcome the physical-world constraints, Embodied World Models (EWMs) [1,7,9,10,19,35,48,51] have emerged as a promising alternative. By learning to predict future observations conditioned on robot actions, EWMs act as differentiable digital twins, enabling agents to plan, verify, and optimize policies entirely within safe, imagined rollouts. Despite this potential, existing EWMs face two fundamental limitations that hinder robust policy optimization in practice. First, current EWMs struggle to maintain 3D geometric consistency in complex interaction modeling [25]. Despite producing visually appealing frames, they suffer from physics hallucinations (e.g., object teleportation, scale drift, surface penetration, Fig. 1(a)) due to the absence of explicit geometric grounding. Second, although isolated prior works [18, 26, 52] have explored world-model-based policy improvement, no unified framework exists capable of leveraging high-fidelity EWMs for the full spectrum of policy optimization from inference-time imagined verification to training-time evolutionary refinement. 

In this work, we introduce RoboStereo, a dual-tower 4D world model designed for unified policy optimization across training and inference. To enforce geometric awareness and 3D consistency, RoboStereo employs a symmetric twin backbone Diffusion Transformer (DiT) [28] architecture that processes RGB videos and 3D pointmaps as mutually reinforcing modalities. Through bidirectional cross-attention across the two towers, the video branch incorporates geometric constraints to maintain structural rigidity, while the pointmap branch leverages semantic context to refine object geometry. This symmetric fusion grounds every generated pixel in consistent 3D space, yielding temporally coherent 4D pointcloud trajectories. A dedicated 4D Gaussian Splatting head [14] then renders these trajectories into photorealistic observations from flexible viewpoints, supporting multi-view supervision during policy learning. 

Building on RoboStereo as a high-fidelity 4D mental simulator, we introduce the first comprehensive framework for world-model-based policy optimization. It comprises three complementary paradigms that span the full spectrum from inference-time improvement to training-time refinement: (1) Test-Time Policy Augmentation (TTPA), a zero-shot pre-execution mechanism that validates and refines candidate action sequences through imagined rollouts; (2) ImitativeEvolutionary Policy Learning (IEPL), which leverages dense visual-imitation rewards from flexible-view imagined trajectories to efficiently align policies with expert behavior; (3) Open-Exploration Policy Learning (OEPL), a self-supervised approach that enables autonomous skill discovery and self-correction in the absence of expert demonstrations. This framework is the first to treat an EWM 

RoboStereo 

3 


**Fig. 2:** RoboStereo Architecture. Symmetric dual DiT towers (a) process RGB and XYZ pointmaps via bidirectional cross-attention for visual-geometric fusion (b) and a Gaussian head for flexible-viewpoint rendering. Dual-path action-conditioned timestep embedding mechanism (c) ensures precise frame-level trajectory control. 

as the foundational backbone for scalable VLA policy improvement across both deployment and learning phases, substantially decoupling optimization from expensive and risky physical interaction. Our main contributions are as follows: 

- We propose RoboStereo, a symmetric dual-tower Diffusion Transformer (DiT) that jointly processes RGB video and 3D pointmap sequences as complementary modalities. Bidirectional cross-attention enforces strict spatiotemporal consistency, yielding high-fidelity 4D generation grounded in explicit geometric constraints. 

- We introduce the first unified framework for world-model-based policy optimization in VLA settings, encompassing three paradigms: TTPA for preexecution validation and refinement, IEPL for viewpoint-flexible visual imitation and evolutionary refinement, and OEPL for demonstration-free skill discovery and self-correction. 

- Extensive experiments show that RoboStereo achieves state-of-the-art performance in physics adherence and 3D geometric accuracy. Moreover, the unified optimization framework delivers substantial policy gains (over 97% mean relative improvement over the baseline) on fine-grained manipulation tasks, demonstrating the effectiveness of world model-based policy improvement. 

### **2 Related Work** 

#### **2.1 Embodied World Models and Geometric Consistency** 

The development of high-fidelity visual world models has enabled embodied AI policies to learn from realistic future predictions. Early foundation models, such as Cosmos 2.5 [27], established a baseline for Sim2Real applications by synthesizing diverse video sequences from text and image prompts. However, standard 2D 

4 R. Zhang et al. 

video diffusion models often rely on statistical patterns and lack explicit physical grounding [12,16,36,47]. This frequently leads to geometric hallucinations, including object teleportation or structural morphing [49], which impede longhorizon manipulation planning. To address these issues, recent research focuses on enforcing 3D and 4D structural constraints. FantasyWorld [8] incorporates a trainable geometric branch with dual-pathway processing to maintain multiview coherence. Similarly, TesserAct [50] and WristWorld [30] utilize 4D representations, such as RGB-Depth-Normal streams or spatial projections, to improve consistency in dynamic sequences. The Gaussian World Model (GWM) [23] further integrates 3D Gaussian Splatting with latent diffusion for contact-rich predictions. RoboStereo builds on these principles through a Symmetric DualTower DiT architecture. Unlike asymmetric methods, our framework reinforces RGB semantics with continuous 3D pointmap constraints via bidirectional crossattention, maintaining spatiotemporal coherence and pixel-level 3D grounding. 

#### **2.2 Policy Optimization and Test-Time Scaling for VLAs** 

Vision-Language-Action (VLA) models often lack the causal understanding necessary for self-correction when trained solely via supervised imitation learning. To overcome this limitation, world models serve as scalable environments and synthetic data engines for Reinforcement Learning [11, 32, 34, 46] (RL). For instance, GigaWorld-0 [35] demonstrates the potential of world models as a scalable data engine to empower embodied agents. Building on this, the WMPO framework [52] conducts on-policy Group Relative Policy Optimization (GRPO) [34] within a pixel-space world model, allowing policies to explore and recover from failures. To address sparse reward signals, TGRPO [26] utilizes LLM-guided reward functions and trajectory-level advantage estimation. RoboStereo extends world-model-based optimization through a framework spanning training to inference. During training, we introduce Imitative-Evolutionary Policy Learning (IEPL) and Open-Exploration Policy Learning (OEPL). Instead of binary rewards, IEPL uses the 4D rendering capabilities of RoboStereo to compute dense, frame-by-frame perceptual distances (LPIPS) from multiple viewpoints, combining the sample efficiency of imitation with the exploratory power of GRPO. Additionally, we introduce Test-Time Policy Augmentation (TTPA) to improve robotic precision. By using RoboStereo as a predictive safeguard, TTPA filters hazardous actions via imagined verification before physical execution. 

### **3 Method** 

Featuring dual video and pointmap towers, RoboStereo processes an initial RGB image and XYZ pointmap alongside a robot action sequence to generate highfidelity 4D (3D+time) future trajectory chunks, thereby serving as a powerful simulator for VLA policy optimization. We detail the RoboStereo architecture in Sec. 3.1, its training strategy in Sec. 3.2, and the unified world model-based policy optimization framework built upon it in Sec. 3.3. 

RoboStereo 5 

#### **3.1 Architecture Design** 

**Symmetric Dual-Tower DiT Framework.** RoboStereo employs a symmetric dual-tower Diffusion Transformer (DiT) [28] that processes RGB video and 3D pointmaps (3-channel XYZ coordinate videos) as joint modalities (Fig. 2(a)). Both towers utilize the Cosmos 2.5 backbone [1], sharing identical latent dimensions to enable homogeneous Video Autoencoder (VAE) encoding without additional alignment layers. Each DiT features paired cross-attention layers that facilitate bidirectional information flow (Fig. 2(b)): the video branch queries geometric constraints from the pointmap tower, while the pointmap branch retrieves semantic context from the video tower. This design preserves pretrained feature spaces established during single-modality pretraining while propagating synchronization cues throughout the network. Finally, a 4D Gaussian head [20] projects the generated RGB-XYZ pairs into dynamic Gaussian Splats, enabling flexible novel-view synthesis. 

**Frame-Level Action Control.** To achieve precise action control, we encode actions as continuous vectors and inject them into the DiT backbone via a dual-path action-conditioned timestep embedding mechanism (Fig. 2(c)). An action vector **a** is processed by two independent MLPs: one implicitly fuses with the diffusion timestep embedding _et_ to generate a base conditioning latent **c** = SiLU( **t** emb+MLP1( **a** )), while the other explicitly predicts modulation offsets ( _γa, βa, αa_ ) = MLP2( **a** ). These offsets are additively combined with timestepderived parameters to form final Adaptive Layer Normalization (AdaLN) [29] coefficients: _γ_ = _γt_ ( **c** ) + _γa_ , _β_ = _βt_ ( **c** ) + _βa_ , _α_ = _αt_ ( **c** ) + _αa_ . This explicit modulation enforces frame-level structural guidance at each denoising step, ensuring generated trajectories faithfully follow action sequences. The feature update within a Transformer block is: 


#### **3.2 Training Strategy for World Model** 

Our training follows a two-stage paradigm: single-modality pretraining followed by joint fine-tuning. Both branches are initialized from Cosmos 2.5 pretrained weights, first independently fine-tuned on modality-specific data, then jointly optimized for cross-modal collaboration. 

**Data Construction.** We construct a large-scale 4D robotic manipulation dataset based on Bridge V2 [37], comprising approximately 20,000 third-person videos capturing robotic arms performing diverse kitchen tasks. Videos are standardized to 320 _×_ 256 resolution at 5 FPS. Each frame is paired with a 7D action vector **a** = ( _∆x, ∆y, ∆z, ∆θr, ∆θp, ∆θy, w_ gripper) specifying gripper displacement, rotation, and width. We employ DepthAnything V3 [20] to predict depth maps and construct XYZ pointmaps via inverse perspective projection, forming 3-channel images that maintain pixel-level correspondence with RGB frames. This unified representation enables paired training of both video and geometric streams. More details are provided in the **Supplementary Material** . 

**Independent Training.** In the first stage, both towers are initialized with Cosmos 2.5 weights and independently fine-tuned to adapt to robotic domains. 

R. Zhang et al. 

6 

RGB videos and pointmaps are encoded by VAEs into clean latent representations **z** _v,_ **z** _p_ . We sample a timestep _t ∼U_ [0 _,_ 1] and independent Gaussian noise **_ϵ_** _v,_ **_ϵ_** _p ∼N_ ( **0** _,_ **I** ) to construct noisy latents via Rectified Flow [21]: 


The noisy latents **z**<sup>_t_</sup> _m_<sup>, conditioned on the initial frame latents</sup><sup>**z**</sup> _v_<sup>(0)</sup> and **z**<sup>(0)</sup> _p_<sup>, text</sup> instruction **c** text, and action sequence **c** action, are fed into their respective DiT towers to predict the velocity fields: 


Each model is trained to match the target velocity **z** _m −_ **_ϵ_** _m_ via MSE loss: 


This stage enables each branch to strictly capture temporal coherence in video generation and geometric accuracy in pointmap prediction. 

**Joint Training.** In the second stage, we integrate the pretrained towers. To mitigate memory overhead, we freeze all feed-forward network (FFN) layers, finetuning only the self-attention and cross-attention modules to align modalities while preserving pretrained feature spaces [22]. We employ paired data latents ( **z** _v,_ **z** _p_ ) but inject independent Gaussian noise ( **_ϵ_** _v,_ **_ϵ_** _p_ ) with a shared timestep _t ∼U_ [0 _,_ 1]: 


Each backbone predicts velocity fields conditioned on the current noisy latent, timestep, task conditions, and crucially, the intermediate latent from the other modality via bidirectional cross-attention: 


The objective is the weighted sum of the two modalities’ flow matching losses: 


where _λv_ = 0 _._ 85 and _λp_ = 0 _._ 15. The use of paired data ensures scene consistency, while the shared timestep _t_ forces both branches to synchronize their denoising progress. This strategy facilitates implicit correspondence learning between visual semantics and geometric structures without explicit alignment layers. 

#### **3.3 World Model-Based Policy Optimization** 

**Task Formulation.** We formulate robotic manipulation as a sequential decisionmaking Markov chain [2] where a policy _πθ_ interacts with an environment to execute language-specified tasks **g** . At each timestep _t_ , the policy observes visual state **s** _t_ (e.g., RGB image) and outputs action chunk **a** _t ∈A_ conditioned on the goal: **a** _t ∼ πθ_ ( **a** _t|_ **s** _t,_ **g** ). The environment transitions to the next state **s** _t_ +1 _∼ p_ ( **s** _t_ +1 _|_ **s** _t,_ **a** _t_ ) according to unknown dynamics _p_ ( **s** _t_ +1 _|_ **s** _t,_ **a** _t_ ). A complete trajectory is denoted as **_τ_** = _{_ ( **s** 0 _,_ **a** 0) _, . . . ,_ ( **s** _T ,_ **a** _T_ ) _}_ . 

RoboStereo 

7 


**Fig. 3:** Illustration of Test-Time Policy Augmentation (TTPA). 

RoboStereo functions as a learned world model _pϕ_ that predicts future visual observations conditioned on the current state and action chunk. Formally, given an initial state **s** 0 and an action sequence _{_ **a** 0 _, . . . ,_ **a** _T −_ 1 _}_ , the world model synthesizes an imagined visual trajectory: 


For long-horizon tasks, we employ an autoregressive generation strategy where the last frame of the generated video chunk serves as the initial observation for both the VLA policy and RoboStereo in the next step. This mechanism enables policy evaluation and optimization entirely within the imagined latent space without any real-world interaction. Building upon this formulation, we propose the first unified framework for world-model-based policy optimization, comprising one test-time augmentation strategy and two policy training paradigms. 

**Test-Time Policy Augmentation (TTPA).** Direct deployment of VLA in physical environments entails significant safety risks due to potential execution failures. To mitigate this, we introduce TTPA, a high-level planning mechanism that leverages RoboStereo as a mental simulator to verify outcomes before acting. 

The workflow proceeds through three integrated stages: (1) Imagined Trajectory Generation: Given a candidate action sequence **a** _t_ : _t_ + _H_ from the policy, RoboStereo synthesizes a high-fidelity visual forecast **_τ_** ˆ (Eq. 8) representing the expected future. (2) Trajectory Evaluation: A video understanding model _Vψ_ assesses the semantic alignment between the imagined trajectory **_τ_** ˆ and the task goal **g** , outputting a success confidence score _c_ = _Vψ_ (ˆ **_τ_** _,_ **g** ) _∈_ [0 _,_ 1]. (3) Policy Decision: The system executes the action chunk only if the outcome is deemed safe and successful; otherwise, it triggers a replanning step without physical movement. Formally, the execution logic is defined as: 


where _δ_ safe is a confidence threshold. By simulating actions in RoboStereo’s high-fidelity visual predictions, TTPA enables zero-cost failure detection and replanning without physical interaction, reducing real-world trial costs and enhancing success rates for complex manipulation tasks. 

**Imitative-Evolutionary Policy Learning (IEPL).** IEPL exploits the 4D generative capabilities of RoboStereo to establish visual imitation reward signals 

R. Zhang et al. 

8 


**Fig. 4:** Illustration of Imitative-Evolutionary Policy Learning (IEPL). 

under flexible camera viewpoints for policy learning. This paradigm is designed to learn from expert demonstrations through trajectory matching via reinforcement learning. 

**_<1> Reward Function Design._** To guide policy optimization, we formulate a novel 4D visual imitation reward based on the perceptual alignment between expert and policy-induced trajectories within the world model. Given a task **g** and expert actions **a**<sup>_∗_</sup> _t_<sup>,wegeneratepaired4Dimaginedrolloutsforboth</sup> the expert actions **a**<sup>_∗_</sup> _t_<sup>andthepolicyactions</sup><sup>**a**</sup><sup>_t∼πθ_,whicharerenderedinto</sup> video sequences from identical camera viewpoints: 


The per-step imitation reward is computed as the negative perceptual distance between corresponding imagined frames: 


where _D_ LPIPS denotes the well-established perceptual metric LPIPS [45]. 

**_<2> GRPO Optimization._** Policy optimization is performed via GRPO [34]. In each iteration, we sample _K_ trajectories _{_ **_τ_**<sup>(</sup><sup>_k_)</sup> _}_<sup>_K_</sup> _k_ =1<sup>from the current policy</sup><sup>_πθ_</sup> and compute their cumulative rewards _{R_ IEPL( **_τ_**<sup>(</sup><sup>_k_)</sup> ) _}_<sup>_K_</sup> _k_ =1<sup>.Theadvantages</sup><sup>_A_ˆ(</sup><sup>_k_)</sup> are normalized using the group mean _µR_ and standard deviation _σR_ : 


The policy is then updated by minimizing the clipped surrogate objective: 


_πθ_ <u>(</u> **a**<sup>(</sup> _<u>t</u>_<sup>_k_)</sup> _<u>|</u>_ **s**<sup>(</sup> _<u>t</u>_<sup>_k_)</sup> _<u>,</u>_ **<u>g</u>** <u>)</u> where _ρk_ ( _θ_ ) =<sup>�</sup><sup>_T_</sup> _t_ =0<sup>_−_1</sup> _πθ_ old ( **a** _t_<sup>(</sup><sup>_k_)</sup> _|_ **s**<sup>(</sup> _t_<sup>_k_)</sup> _,_ **g** )<sup>denotestheimportancesamplingratio.</sup> The hyperparameter _ϵ_ restricts the policy update size, while _λ_ KL weights the KL divergence penalty against a reference policy _π_ ref to prevent mode collapse during open exploration. 

RoboStereo 

9 


**Fig. 5:** Illustration of Open-Exploration Policy Learning (OEPL). 

**_<3> Iterative Rollout Process._** IEPL iterates through three stages: (1) Imagined Trajectory Generation: The current VLA policy _πθ_ and expert actions are executed in RoboStereo to generate paired imagined trajectories, **_τ_** ˆ policy and **_τ_** ˆ expert. Every _k_ -th frame ( _k_ = 8) from **_τ_** ˆ policy is fed back as updated observations, creating closed-loop imitation. (2) Trajectory Evaluation: _K_ sampled trajectories under specific camera viewpoints are evaluated based on their perceptual distance to expert rollouts (Eq. (12)), yielding dense imitation rewards. (3) Policy Update: The policy is optimized via GRPO (Eq. (14)), iteratively aligning its behavior with the expert driven by visual reward signals. 

IEPL’s innovative visual optimization objective aligns with the large-scale video interaction data used in VLA pre-training, which can maximally activates the pre-training knowledge priors compared to traditional RL algorithms operating in abstract spaces [52]. The perceptual distance metric provides dense, differentiable rewards that capture nuanced task semantics beyond sparse binary success metrics for effective learning. This approach combines the sample efficiency of imitation learning with the adaptability of reinforcement learning. 

**Open-Exploration Policy Learning (OEPL).** OEPL leverages RoboStereo for open-ended exploration without expert demonstrations. Unlike IEPL’s imitationfocused paradigm, OEPL emphasizes autonomous skill discovery and self-correction through discriminator-based evaluation in open task spaces. 

**_<1> Reward Function Design._** OEPL employs a video understanding model as reward model _Rψ_ , which is trained to predict task completion likelihood from visual clips. For a sampled trajectory **_τ_** = _{_ ( **s** _t,_ **a** _t_ ) _}_<sup>_T_</sup> _t_ =0<sup>,wegeneratethe</sup> imagined visual trajectory **_τ_** ˆ = _{_ ˆ **s** _t}_<sup>_T_</sup> _t_ =1<sup>in RoboStereo via Eq. (8). The trajectory</sup> is segmented into _N_ overlapping clips _{_ **c** _i}_<sup>_N_</sup> _i_ =1<sup>,eachcontaining</sup><sup>_L_consecutive</sup> frames. The reward model predicts a success confidence for each clip: 


The task-level cumulative reward aggregates these clip-level predictions using a temporally increasing weight: 


where _wi_ assigns higher weights to later clips via temperature _β >_ 0, encouraging policies to progress toward task completion rather than merely starting correctly. 

10 R. Zhang et al. 


**Fig. 6:** Training procedures for IEPL and OEPL. IEPL (left) learns through visual imitation by matching policy rollouts with expert trajectories. OEPL (right) learns through open exploration guided by a discriminator-based reward model. 

**_<2> GRPO Optimization._** Similar to IEPL, we optimize the policy via GRPO. In each iteration, we sample _K_ trajectories _{_ **_τ_**<sup>(</sup><sup>_k_)</sup> _}_<sup>_K_</sup> _k_ =1<sup>fromthecurrent</sup> policy and compute their cumulative rewards _{R_ OEPL( **_τ_**<sup>(</sup><sup>_k_)</sup> ) _}_<sup>_K_</sup> _k_ =1<sup>.Theadvan-</sup> tages _A_<sup>ˆ(</sup><sup>_k_)</sup> are normalized using the group mean _µR_ and standard deviation _σR_ following Eq. 13. The policy is then updated by minimizing the optimization objective in Eq. 14. 

**_<3> Iterative Rollout Process._** OEPL iterates through three stages: (1) Imagined Trajectory Generation: The VLA policy _πθ_ predicts action sequences from current observations, and RoboStereo generates imagined visual trajectories conditioned on the action chunk. Every _k_ -th frame is fed back to the policy as updated observations, creating closed-loop exploration. (2) Trajectory Evaluation: _K_ trajectories are sampled and evaluated by the reward model via Eq. (16), providing reward signals. (3) Policy Update: The policy is optimized via Eq. (14) to maximize rewards through autonomous exploration and self-correction. 

OEPL utilizes world models as safe exploration environments, decoupling policy optimization from physical interaction to enable learning from failures. The discriminator-based reward coupled with a temporal weighting mechanism (Eq. (16)) effectively drives success-oriented open exploration. By facilitating autonomous self-correction and novel skill discovery, which are often constrained in pure imitation learning, this paradigm serves as a robust complement to IEPL. 

### **4 Experiments** 

We systematically evaluate RoboStereo to investigate two core questions: (1) Can RoboStereo achieve highly controllable 4D modeling while preserving spa- 

RoboStereo 11 

**Table 1:** Video evaluation results across visual quality, motion quality and content consistency dimensions. Best results are **bolded** , and second-best results are <u>underlined.</u> 

|**Models**|**V**|**isual Qua**|**lity**|**Mo**|**tion Q**|**uality**|**Con**|**tent Consist**|**ency**|
|---|---|---|---|---|---|---|---|---|---|
||Image<br>Quality|Aesthetic<br>Quality|JEPA<br>Similarity|Dynamic<br>Degree|Flow<br>Score|Motion<br>Smoothness|Subject<br>Consistency|Background<br>Consistency|Photometric<br>Consistency|
|GigaWorld|**0.483**|0.384|0.429|0.650|0.308|0.771|0.727|0.825|0.172|
|Genie|0.222|0.319|0.327|**0.666**|0.083|0.687|0.762|0.875|0.197|
|MIND-V|0.319|0.397|0.452|0.552|0.267|0.756|0.803|0.902|0.240|
|RoboMaster|0.346|0.378|0.294|0.606|0.146|0.693|**0.809**|0.896|0.333|
|Vidar|0.408|**0.404**|0.551|0.273|0.137|0.773|0.741|0.800|0.218|
|Cosmos 2.5|0.433|0.347|0.896|0.585|0.252|0.727|0.796|0.887|0.348|
|WoW|0.452|0.374|0.736|0.446|0.264|0.769|0.804|0.886|0.214|
|IRASim|0.339|0.357|0.909|0.412|0.204|0.685|0.806|0.891|0.342|
|**Ours**|0.455|0.389|**0.912**|0.610|**0.313**|**0.781**|0.807|**0.905**|**0.353**|


**Fig. 7:** Visualizations of the 4D Gaussian representations, RGB videos, and depth maps produced by RoboStereo. RoboStereo generates precise future trajectories conditioned on action instructions, exhibiting high visual fidelity and geometric consistency. 

tiotemporal consistency in both visual appearance and geometric structure? (2) Can RoboStereo serve as a high-fidelity embodied simulator to enhance VLA policies within our proposed unified optimization framework, spanning test-time optimization (TTPA) and training-time refinement (IEPL, OEPL)? 

#### **4.1 Experimental Setup** 

RoboStereo is initially trained on our 4D embodied manipulation dataset constructed from Bridge V2 [37] (Sec. 3.2). Then, we further fine-tune the world model on MimicGen [24] simulation data before leveraging it for unified policy optimization. For long-horizon manipulation tasks, RoboStereo sequentially generates 4D scene chunks consisting of 12 frames at a competitive speed of approximately 0.7s per frame. All experiments are performed on a computing cluster equipped with 16 NVIDIA H200 GPUs. 

12 R. Zhang et al. 

**Table 2:** Video evaluation results across physics adherence, 3D accuracy and controllability dimensions. Best results are **bolded** , and second-best results are <u>underlined.</u> 

|**Models**|**Physics Ad**|**herence**|**3D A**|**ccuracy**|**C**|**ontrollability**||
|---|---|---|---|---|---|---|---|
||Interaction Quality|Trajectory Acc.|Depth Acc.|Perspectivity|Instruction Follow.|Semantic Align.|Action Follow.|
|GigaWorld|0.523|0.152|0.611|0.753|0.599|0.844|**0.109**|
|Genie|0.198|0.067|0.844|0.513|0.200|0.848|0.011|
|MIND-V|**0.570**|0.137|0.705|0.788|0.593|0.865|0.079|
|RoboMaster|0.526|0.115|0.801|0.731|0.561|0.839|0.075|
|Vidar|0.520|0.185|0.775|0.748|0.573|0.856|0.039|
|Cosmos 2.5|0.534|0.286|0.854|0.756|0.604|0.850|0.063|
|WoW|0.531|0.204|0.720|0.742|0.565|0.873|0.042|
|IRASim|0.560|0.257|0.862|0.774|0.640|0.852|0.052|
|**Ours**|**0.570**|**0.342**|**0.881**|**0.797**|**0.723**|**0.884**|0.088|


#### **4.2 Video Quality Evaluation** 

We evaluate RoboStereo’s video generation quality against state-of-the-art embodied world models on the WorldArena benchmark [33]. The evaluation spans **16 metrics** across **six sub-dimensions** (higher is better for all). Detailed metric definitions and implementations appear in the **supplementary material** . 

**Baselines and Comparative Setup.** We compare RoboStereo against eight representative embodied world models: GigaWorld-0 [35], Genie Envisioner [19], MIND-V [48], RoboMaster [10], Vidar [9], Cosmos 2.5 [1], WoW [7], and IRASim [51]. For a fair comparison, all baselines with publicly available code are finetuned on our Bridge V2-derived dataset following their official configurations. 

**Qualitative and Quantitative Comparison.** Tables 1 and 2 summarize the video quality quantitative results across six dimensions. RoboStereo ranks first or second on the majority of the 16 metrics, with particularly strong advances in structure- and interaction-centric evaluations. In contrast, although several baselines deliver competitive visual fidelity, they struggle with semantic drift, generating dynamics that diverge from prescribed actions. 

Notably, RoboStereo attains top performance across all metrics within the `Physics Adherence` and `3D Accuracy` dimensions, underscoring its exceptional ability to preserve physical plausibility and geometric consistency during intricate interactions. The consistent superiority stems from the interplay of two core designs. (1) The symmetric dual-tower DiT with bidirectional cross-attention enables mutually beneficial feature integration, where geometric constraints from the pointmap tower refine RGB semantics, and visual and motion cues from the RGB tower enhance structural reasoning. (2) Frame-level action conditioning provides fine-grained temporal control, ensuring the generated dynamics strictly adhere to the input actions without temporal drift. 

Figure 7 further qualitatively demonstrates RoboStereo’s capacity to model fine-grained robotic interactions, generating high-fidelity 4D scene evolutions that align closely with ground-truth dynamics. These strengths generalize consistently across both real-world and simulated scenarios, highlighting the model’s robust ability to deliver physically realistic and action-accurate 4D generation. 

RoboStereo 13 

#### **4.3 Policy Optimization Evaluation** 

We evaluate RoboStereo’s effectiveness as a high-fidelity world model for VLA enhancement within our designed unified policy optimization framework, across three proposed paradigms (Sec. 3.3): Test-Time Policy Augmentation (TTPA), Imitative-Evolutionary Policy Learning (IEPL), and Open-Exploration Policy Learning (OEPL). 

**Simulation Environment, Base Policy, and Optimization Baselines.** Evaluations are conducted in the MimicGen simulator [24] across three challenging fine-grained manipulation tasks: `Coffee_D0` (coffee pod preparation and insertion), `StackThree_D0` (stacking three blocks sequentially), and `Square_D0` (precise square-peg insertion). 

We adopt OpenVLA-OFT [15] fine-tuned via imitation learning on 300 expert demonstrations per task as the base policy _π_ base. For simplicity, robot wristcamera inputs are omitted, following the established protocols in [18,52]. Using _π_ base, we collect 128 execution trajectories per task under varied initial states (encompassing both successes and failures) in MimicGen. These trajectories are utilized to fine-tune RoboStereo for domain alignment and to train a video understanding model (VideoMAE V2 [38]), which serves as the success evaluator _Vψ_ for TTPA and reward model _Rψ_ for OEPL. 

To demonstrate the efficacy of our imagined rollouts, we benchmark IEPL and OEPL against two representative optimization baselines: (i) online GRPO [34], which directly optimizes the policy via simulation interactions using a binary success reward signal, and (ii) offline DPO [32], which constructs static successfailure pairs from collected offline simulation data. In contrast, IEPL and OEPL execute all optimization procedures within the imagined rollouts generated by RoboStereo. For fair comparison, all methods are strictly constrained to an identical interaction budget of _P_ = 128 trajectories. 

**Quantitative Results.** Table 3 reports the average success rate (%) across 128 diverse evaluation initial states per task. 

**Table 3:** Task success rates (%) under different optimization paradigms in the MimicGen simulation benchmark. 

As reported in Table 3 (ID 1), TTPA delivers a _>_ 56% relative success rate uplift over the base policy. By rejecting lowconfidence action sequences through RoboStereo’s imagined verification, TTPA substantially enhances deployment reliability without altering the policy weights. 

|**ID **|**Methods**|**Coffee **|**StackThree **|**Square **|**Mean**|
|---|---|---|---|---|---|
|0|Base policy|32.6|30.2|20.2|27.7|
|1|**TTPA**|46.7|46.9|36.2|43.3|
|2|DPO|32.6|38.2|23.3|31.4|
|3|GRPO|29.8|35.1|22.7|29.2|
|4|**IEPL**|47.8|44.1|37.4|43.1|
|5|**OEPL**|53.4|50.8|39.3|47.8|
|6|**Average (1+4+5)**|**59.8**|**55.7**|**46.5**|**54.0**|


IEPL and OEPL achieve remarkable 56 **OEPLAverage (1+4+5) 59.8** 53.4 **55.7** 50.8 **46.5** 39.3 **54.0** 47.8 relative improvements of _>_ 55% and _>_ 72%, respectively (Table 3, IDs 4 and 5), significantly outperforming both online GRPO and offline DPO under the identical rollout budget. These gains are particularly pronounced in contact-rich tasks like `Square_D0` , highlighting the innovative designs in training paradigms: (1) IEPL leverages RoboStereo’s highfidelity visual simulation to extract dense visual perceptual rewards for grouprelative evolutionary updates. This mechanism maximally activates the VLA’s 

14 R. Zhang et al. 

**Table 4:** Ablation study conducted on the Bridge dataset. Results demonstrate that joint dual-tower training substantially improves 3D consistency in generated videos, while incorporating action conditioning via timestep embedding modulation yields markedly superior action control and motion quality. Best results are **bolded** . 

|**Model Variant**|**Physics Ad**|**herence**|**3D **|**Accuracy**|
|---|---|---|---|---|
||Interaction Quality|Trajectory Acc.|Depth Acc.|Perspectivity|
|(a) Video tower only|0.538|0.320|0.821|0.758|
|(b) **Dual-tower joint training**|**0.570**|**0.342**|**0.881**|**0.797**|
|**Model Variant**|**Controlla**|**bility**|**Mot**|**ion Quality**|
||Instruction Follow.|Action Follow.|Flow Score|Motion Smoothness|
|(c) Action-cond via channel concatenation<br>|0.622|0.061|0.238|0.703|
|(d) Action-cond via cross-attention|0.654|0.068|0.243|0.716|
|(e) **Action-cond via timestep embedding**|**0.723**|**0.088**|**0.313**|**0.781**|


pre-trained visual priors, while semantically rich visual instructions provide finegrained policy learning guidance. (2) OEPL drives autonomous skill discovery through discriminator-based supervision, fostering robust self-correction capabilities when encountering suboptimal states. 

Crucially, integrating all three paradigms (Table 3, ID 6) yields the most substantial performance gain ( _>_ 97% relative uplift), demonstrating profound complementarity among the components. This unified framework represents a holistic approach to policy evolution, encompassing a progression from test-time augmentation to expert imitation to exploratory learning within a single, highfidelity 4D world model. By shifting the optimization burden from costly, unsafe physical interactions to scalable, imagined rollouts, RoboStereo establishes a highly efficient, closed-loop paradigm that fundamentally unlocks the continuous self-improvement of VLA models. 

#### **4.4 Ablation Study** 

We conduct a targeted ablation study to assess the impact of two key design choices in RoboStereo: (i) the symmetric dual-tower joint training paradigm (focusing on physics adherence and 3D geometric accuracy), and (ii) the frame-level action conditioning strategy (focusing on controllability and motion quality). 

As shown in Table 4, compared to isolated RGB-tower training (variant (a)), joint dual-tower training (variant (b)) yields substantial improvements in physics- and geometry-critical metrics (e.g., +5.9% in Interaction Quality, +7.3% in Depth Accuracy). Bidirectional cross-attention effectively integrates RGB semantic cues with pointmap-derived 3D constraints, markedly enhancing physical plausibility and long-horizon geometric fidelity. The proposed actionconditioned timestep embedding modulation (variant (e)) achieves superior action alignment and motion coherence, outperforming channel concatenation and cross-attention mechanisms. By injecting action-specific modulation coefficients into diffusion timestep embeddings via extended AdaLN and residual scaling, it attains precise per-frame control without disrupting pretrained features, yielding temporally smooth, physically consistent motion. 

### **5 Conclusion** 

We present RoboStereo, a symmetric dual-tower 4D world model addressing critical limitations in geometric consistency and policy optimization for robotic 

RoboStereo 15 

manipulation. Through bidirectional cross-modal enhancement between RGB and pointmap towers, RoboStereo effectively preserves spatiotemporal coherence and alleviates physics hallucinations. Beyond architectural innovations, we establish the first unified world model-based policy optimization framework built on RoboStereo, encompassing Test-Time Policy Augmentation, ImitativeEvolutionary Policy Learning, and Open-Exploration Policy Learning. By shifting the optimization burden from costly physical interactions to scalable imagined rollouts, this work demonstrates that high-fidelity 4D world models can serve as scalable and generalizable foundational infrastructure for the safe, efficient, and continuous improvement of VLAs. 

### **References** 

1. Agarwal, N., Ali, A., Bala, M., Balaji, Y., Barker, E., Cai, T., Chattopadhyay, P., Chen, Y., Cui, Y., Ding, Y., et al.: Cosmos world foundation model platform for physical ai. arXiv preprint arXiv:2501.03575 (2025) 

2. Agbinya, J.I.: 1 Markov Chain and its Applications, pp. 1–16 (2019) 

3. Bai, S., Cai, Y., Chen, R., Chen, K., Chen, X., Cheng, Z., Deng, L., Ding, W., Gao, C., Ge, C., et al.: Qwen3-vl technical report. arXiv preprint arXiv:2511.21631 (2025) 

4. Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., Jakubczak, S., Jones, T., Ke, L., Levine, S., Li-Bell, A., Mothukuri, M., Nair, S., Pertsch, K., Shi, L.X., Tanner, J., Vuong, Q., Walling, A., Wang, H., Zhilinsky, U.: _π_ 0: A vision-language-action flow model for general robot control. arXiv preprint arXiv:2410.24164 (2024) 

5. Boyer, C., Bulmus, V., Davis, T.P., Ladmiral, V., Liu, J., Perrier, S.: Bioapplications of raft polymerization. Chemical reviews **109** (11), 5402–5436 (2009) 

6. Carion, N., Gustafson, L., Hu, Y.T., Debnath, S., Hu, R., Suris, D., Ryali, C., Alwala, K.V., Khedr, H., Huang, A., et al.: Sam 3: Segment anything with concepts. arXiv preprint arXiv:2511.16719 (2025) 

7. Chi, X., Jia, P., Fan, C.K., Ju, X., Mi, W., Qin, Z., Zhang, K., Tian, W., Ge, K., Li, H., et al.: Wow: Towards a world omniscient world model through embodied interaction. arXiv preprint arXiv:2509.22642 (2025) 

8. Dai, Y., Jiang, F., Wang, C., Xu, M., Qi, Y.: FantasyWorld: Geometry-consistent world modeling via unified video and 3D prediction. In: The Fourteenth International Conference on Learning Representations (ICLR) (2026), `https:// openreview.net/forum?id=3q9vHEqsNx` 

9. Feng, Y., Xiang, C., Mao, X., Tan, H., Zhang, Z., Huang, S., Zheng, K., Liu, H., Su, H., Zhu, J.: Vidarc: Embodied video diffusion model for closed-loop control. arXiv preprint arXiv:2512.17661 (2025) 

10. Fu, X., Wang, X., Liu, X., Bai, J., Xu, R., Wan, P., Zhang, D., Lin, D.: Learning video generation for robotic manipulation with collaborative trajectory control. arXiv preprint arXiv:2506.01943 (2025) 

11. Huang, J., Xu, Z., Zhou, J., Liu, T., Xiao, Y., Ou, M., Ji, B., Li, X., Yuan, K.: Sam-r1: Leveraging sam for reward feedback in multimodal segmentation via reinforcement learning (2025), `https://arxiv.org/abs/2505.22596` 

12. Jin, X., Xu, Z., Ou, M., Yang, W.: Alignment is all you need: A trainingfree augmentation strategy for pose-guided video generation. arXiv preprint arXiv:2408.16506 (2024) 

16 R. Zhang et al. 

13. Ke, J., Wang, Q., Wang, Y., Milanfar, P., Yang, F.: Musiq: Multi-scale image quality transformer. In: Proceedings of the IEEE/CVF international conference on computer vision. pp. 5148–5157 (2021) 

14. Kerbl, B., Kopanas, G., Leimkühler, T., Drettakis, G.: 3d gaussian splatting for real-time radiance field rendering. ACM Transactions on Graphics **42** (4) (July 2023), `https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/` 

15. Kim, M.J., Finn, C., Liang, P.: Fine-tuning vision-language-action models: Optimizing speed and success. arXiv preprint arXiv:2502.19645 (2025) 

16. Kong, W., Tian, Q., Zhang, Z., Min, R., Dai, Z., Zhou, J., Xiong, J., Li, X., Wu, B., Zhang, J., et al.: Hunyuanvideo: A systematic framework for large video generative models. arXiv preprint arXiv:2412.03603 (2024) 

17. LAION-AI: Aesthetic predictor. `https://github.com/LAION-AI/aestheticpredictor` (2022), accessed: 2024 

18. Li, H., Ding, P., Suo, R., Wang, Y., Ge, Z., Zang, D., Yu, K., Sun, M., Zhang, H., Wang, D., et al.: Vla-rft: Vision-language-action reinforcement fine-tuning with verified rewards in world simulators. arXiv preprint arXiv:2510.00406 (2025) 

19. Liao, Y., Zhou, P., Huang, S., Yang, D., Chen, S., Jiang, Y., Hu, Y., Cai, J., Liu, S., Luo, J., et al.: Genie envisioner: A unified world foundation platform for robotic manipulation. arXiv preprint arXiv:2508.05635 (2025) 

20. Lin, H., Chen, S., Liew, J., Chen, D.Y., Li, Z., Shi, G., Feng, J., Kang, B.: Depth anything 3: Recovering the visual space from any views. arXiv preprint arXiv:2511.10647 (2025) 

21. Liu, X., Gong, C., Liu, Q.: Flow straight and fast: Learning to generate and transfer data with rectified flow. arXiv preprint arXiv:2209.03003 (2022) 

22. Low, C., Wang, W., Katyal, C.: Ovi: Twin backbone cross-modal fusion for audiovideo generation. arXiv preprint arXiv:2510.01284 (2025) 

23. Lu, G., Jia, B., Li, P., Chen, Y., Wang, Z., Tang, Y., Huang, S.: GWM: Towards scalable Gaussian world models for robotic manipulation. In: Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV) (2025) 

24. Mandlekar, A., Nasiriany, S., Wen, B., Akinola, I., Narang, Y., Fan, L., Zhu, Y., Fox, D.: Mimicgen: A data generation system for scalable robot learning using human demonstrations. In: 7th Annual Conference on Robot Learning (2023) 

25. Mi, Z., Wang, Y., Xu, D.: One4d: Unified 4d generation and reconstruction via decoupled lora control. arXiv preprint arXiv:2511.18922 (2025) 

26. Niu, C., et al.: TGRPO: Fine-tuning vision-language-action model via trajectorywise group relative policy optimization. arXiv preprint arXiv:2506.08440 (2025) 

27. NVIDIA: World simulation with video foundation models for physical AI (2025) 

28. Peebles, W., Xie, S.: Scalable diffusion models with transformers. In: Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV). pp. 4195– 4205. IEEE (2023) 

29. Perez, E., Strub, F., De Vries, H., Dumoulin, V., Courville, A.: Film: Visual reasoning with a general conditioning layer. In: Proceedings of the AAAI conference on artificial intelligence. vol. 32 (2018) 

30. Qian, Z., Chi, X., Li, Y., Wang, S., Han, S., Zhang, S.: WristWorld: Generating wrist-views via 4D world models for robotic manipulation. arXiv preprint arXiv:2510.07313 (2025) 

31. Radford, A., Kim, J.W., Hallacy, C., Ramesh, A., Goh, G., Agarwal, S., Sastry, G., Askell, A., Mishkin, P., Clark, J., et al.: Learning transferable visual models from natural language supervision. In: International conference on machine learning. pp. 8748–8763. PmLR (2021) 

RoboStereo 17 

32. Rafailov, R., Sharma, A., Mitchell, E., Manning, C.D., Ermon, S., Finn, C.: Direct preference optimization: Your language model is secretly a reward model. Advances in neural information processing systems **36** , 53728–53741 (2023) 

33. Shang, Y., Li, Z., Ma, Y., Su, W., Jin, X., Wang, Z., Jin, L., Zhang, X., Tang, Y., Su, H., Gao, C., Wu, W., Liu, X., Shah, D., Zhang, Z., Chen, Z., Zhu, J., Tian, Y., Chua, T.S., Zhu, W., Li, Y.: Worldarena: A unified benchmark for evaluating perception and functional utility of embodied world models (2026) 

34. Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Bi, X., Zhang, H., Zhang, M., Li, Y., Wu, Y., et al.: Deepseekmath: Pushing the limits of mathematical reasoning in open language models. arXiv preprint arXiv:2402.03300 (2024) 

35. Team, G., Ye, A., Wang, B., Ni, C., Huang, G., Zhao, G., Li, H., Zhu, J., Li, K., Xu, M., et al.: Gigaworld-0: World models as data engine to empower embodied ai. arXiv preprint arXiv:2511.19861 (2025) 

36. Team, I., Feng, T., Han, Y., He, J., He, Y., Lin, X., Liu, T., Lu, H., Tang, J., Wang, W., et al.: Inferix: A block-diffusion based next-generation inference engine for world simulation. arXiv preprint arXiv:2511.20714 (2025) 

37. Walke, H., Black, K., Lee, A., Kim, M.J., Du, M., Zheng, C., Zhao, T., HansenEstruch, P., Vuong, Q., He, A., Myers, V., Fang, K., Finn, C., Levine, S.: Bridgedata v2: A dataset for robot learning at scale. In: Conference on Robot Learning (CoRL). PMLR (2023) 

38. Wang, L., Huang, B., Zhao, Z., Tong, Z., He, Y., Wang, Y., Wang, Y., Qiao, Y.: Videomae v2: Scaling video masked autoencoders with dual masking. In: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR). pp. 14549–14560 (June 2023) 

39. Xu, R., Zhang, J., Guo, M., Wen, Y., Yang, H., Lin, M., Huang, J., Li, Z., Zhang, K., Wang, L., et al.: A0: An affordance-aware hierarchical model for general robotic manipulation. In: Proceedings of the IEEE/CVF International Conference on Computer Vision. pp. 13491–13501 (2025) 

40. Yang, L., Kang, B., Huang, Z., Xu, X., Feng, J., Zhao, H.: Depth anything: Unleashing the power of large-scale unlabeled data. In: Proceedings of the IEEE/CVF conference on computer vision and pattern recognition. pp. 10371–10381 (2024) 

41. Zhai, A., Liu, B., Fang, B., Cai, C., Ma, E., Yin, E., Wang, H., Zhou, H., Wang, J., Shi, L., Liang, L., Wang, M., Wang, Q., Gan, R., Yu, R., Li, S., Liu, S., Chen, S., Chen, V., Xu, Z.: Igniting vlms toward the embodied space. arXiv preprint arXiv:2509.11766 (2025) 

42. Zhang, G., Liu, C., Cui, Y., Zhao, X., Ma, K., Wang, L.: Vfimamba: Video frame interpolation with state space models. Advances in Neural Information Processing Systems **37** , 107225–107248 (2024) 

43. Zhang, H., Li, F., Liu, S., Zhang, L., Su, H., Zhu, J., Ni, L.M., Shum, H.Y.: Dino: Detr with improved denoising anchor boxes for end-to-end object detection. arXiv preprint arXiv:2203.03605 (2022) 

44. Zhang, K., Xu, R., Ren, P., Lin, J., Wu, H., Lin, L., Liang, X.: Robridge: A hierarchical architecture bridging cognition and execution for general robotic manipulation. In: Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV). pp. 14590–14601. IEEE (2025) 

45. Zhang, R., Isola, P., Efros, A.A., Shechtman, E., Wang, O.: The unreasonable effectiveness of deep features as a perceptual metric. In: Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR). pp. 586–595. IEEE (2018) 

18 R. Zhang et al. 

46. Zhang, R., Sun, Y., Zhang, Z., Li, J., Liu, X., Au, H.F., Guo, H., Yan, P.: Marlmambacontour: Unleashing multi-agent deep reinforcement learning for active contour optimization in medical image segmentation. In: Proceedings of the 33rd ACM International Conference on Multimedia (MM). pp. 7815–7824. ACM (2025) 

47. Zhang, R., Zhou, J., Xu, Z., Liu, Z., Huang, J., Zhang, M., Sun, Y., Li, X.: Zeroshot 3d-aware trajectory-guided image-to-video generation via test-time training. arXiv preprint arXiv:2509.06723 (2025) 

48. Zhang, R., Zhang, M., Zhou, J., Guo, Z., Liu, X., Xu, Z., Zhong, Z., Yan, P., Luo, H., Li, X.: Mind-v: Hierarchical video generation for long-horizon robotic manipulation with rl-based physical alignment. arXiv preprint arXiv:2512.06628 (2025) 

49. Zhao, L., Lu, X., Hu, B., Ke, W., Wang, L.: Gshoi denoiser: Denoising gaussian hand-object interaction for photorealistic rendering. In: 2025 IEEE International Symposium on Mixed and Augmented Reality (ISMAR). pp. 614–623 (2025). `https://doi.org/10.1109/ISMAR67309.2025.00071` 

50. Zhen, H., Sun, Q., Zhang, H., Li, J., Zhou, S., Du, Y., Gan, C.: TesserAct: Learning 4D embodied world models. arXiv preprint arXiv:2504.20995 (2025) 

51. Zhu, F., Wu, H., Guo, S., Liu, Y., Cheang, C., Kong, T.: Irasim: A fine-grained world model for robot manipulation. In: Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV). pp. 9834–9844. IEEE (2025) 

52. Zhu, F., Yan, Z., Hong, Z., Shou, Q., Ma, X., Guo, S.: Wmpo: World modelbased policy optimization for vision-language-action models. arXiv preprint arXiv:2511.09515 (2025) 

RoboStereo 19 

# **Supplementary Material** 

### **6 Inference Efficiency Analysis** 

Beyond generation quality, practical embodied simulation requires high inference efficiency to enable large-scale trajectory rollouts. We evaluate the inference speed (measured in frames per second, FPS) of our video generation model against several SOTA baselines. As reported in Table 8, RoboStereo achieves an inference speed of 1.50 

**Fig. 8:** Inference speed comparison. 

|**Method**<br>**Speed (FPS)** _↑_|
|---|
|WoW [7]<br>0.05|
|MIND-V [48]<br>0.38|
|IRASim [51]<br>0.53|
|RoboMaster [10]<br>0.63|
|**Ours (Video Tower)**<br>**1.50**|


FPS, maintaining an advantage over baselines. This high-efficiency inference is a key enabler for our unified world-model-based policy optimization framework. By facilitating low-latency imagined interactions, RoboStereo enables scalable closed-loop trajectory generation and policy optimization in practice. 

### **7 Qualitative Analysis of World-Model-Based Policy Optimization Framework** 

To further validate the effectiveness of our unified framework, we qualitatively analyze the behavioral patterns of VLA policies optimized via RoboStereo. The proposed optimization paradigms effectively overcome the intrinsic limitations of imitation learning in the base policy, giving rise to emergent recovery behaviors and precise geometric reasoning without requiring real-world interactions. 


**Fig. 9: Visualization of fine-grained geometric reasoning enabled by IEPL on the** `Three_Piece_Assembly_D0` **task.** The base policy (top row) produces coarse actuation and fails to satisfy precise 3D geometric constraints. In contrast, the IEPLoptimized policy (bottom row), guided by dense visual imitation rewards from RoboStereo’s imagined trajectories, performs continuous micro-adjustments, achieving accurate part insertion. 

#### **7.1 Emergent Fine-Grained Geometric Reasoning via IEPL** 

As illustrated in Fig. 9, the baseline policy exhibits coarse-grained actuation in interaction-rich insertion tasks. Despite attempting local adjustments, it fails to 

20 R. Zhang et al. 


**Fig. 10: Visualization of emergent self-correction via OEPL on the** `Square_D0` **task.** The base policy (top row) exhibits open-loop failure propagation: after an initial grasp failure, it erroneously treats the failed state as successful and blindly executes the subsequent transport trajectory. In contrast, the OEPL-optimized VLA policy (bottom row) autonomously detects the grasp slip and initiates a corrective re-grasping maneuver, achieving robust task completion. 

satisfy the precise 3D geometric constraints between the object and the target receptacle, resulting in persistent misalignment and eventual jamming. This limitation underscores the inadequacy of sparse supervision in conventional imitation learning for acquiring high-precision manipulation skills. By comparison, the policy optimized via IEPL demonstrates markedly superior fine-grained geometric reasoning. Leveraging dense visual imitation rewards synthesized by RoboStereo, the policy acquires the ability to perform smooth, continuous micro-adjustments that precisely align the object’s position and orientation. This emergent capability effectively bridges the gap between visual perception and fine-grained motor control, thereby improving success rates on interaction-rich tasks. 

#### **7.2 Emergent Self-Correction via OEPL** 

As illustrated in Fig. 10, the baseline policy exhibits characteristic open-loop failure propagation during grasping tasks. Following an initial grasp failure, it blindly proceeds along the planned transport trajectory without adjustment, proceeds along the planned transport trajectory without adjustment treating an empty gripper as a successful grasp state. This behavior shows the brittleness of standard imitation learning in the presence of execution noise. By comparison, the policy optimized via OEPL exhibits robust autonomous self-correction. Through imagined rollouts augmented by discriminator-based rewards within RoboStereo, the VLA policy acquires the ability to identify suboptimal states and spontaneously triggers a re-grasping maneuver. This emergent self-correction mechanism rectifies execution errors without explicit expert supervision, converting potential task failures into robust task completions. 

### **8 Real-World Deployment** 

To evaluate the practical applicability of our framework beyond simulated environments, we conduct real-world experiments on a Realman robotic arm using a 

RoboStereo 21 


**Fig. 11: Qualitative results of real-world deployment.** The robotic arm is instructed to clear target cubes from a desktop with a prism serving as a distractor. The VLA jointly optimized via IEPL and OEPL exhibits emergent self-correction and fine-grained micro-adjustment capabilities. These critical recovery behaviors absent in the imitation learning baseline. 

representative desktop-clearing task. We collect 30 expert demonstration trajectories in the physical setting to fine-tune both the base vision-language-action (VLA) policy (OpenVLA-OFT [18]) via standard imitation learning (IL) and RoboStereo for domain alignment. The fine-tuned RoboStereo then serves as a high-fidelity imagined rollout environment for IEPL and OEPL optimization under the same hyperparameter configurations as in simulation. 

Quantitative evaluation reveals a substantial performance gain: the IL baseline achieves a 30% success rate (6/20 trials), while joint IEPL and OEPL optimization doubles this to 65% (13/20 trials). Qualitatively, the IL baseline is highly brittle to execution noise. For example, a suboptimal initial approach angle causes the blue cube to slip, after which the open-loop policy fails to recover and terminates in failure. 

In contrast, as shown in Fig. 11, the jointly optimized VLA policy exhibits two critical emergent capabilities. First, upon detecting grasp slippage, the policy autonomously triggers a replanning and re-grasping sequence, an instance of self-correction enabled by the open-ended state exploration induced by OEPL. Second, during re-grasping, the policy performs precise micro-adjustments to align the end-effector orientation, reflecting the fine-grained geometric reasoning acquired through dense visual imitation rewards provided by IEPL. By tightly integrating imitation-guided refinement with exploratory state-space coverage within a high-fidelity imagined simulator, our approach endows the VLA with robust closed-loop adaptability at a fraction of the cost of extensive real-world trial-and-error. 

22 R. Zhang et al. 

### **9 Data Processing Details** 

This section details the data preprocessing pipeline for RoboStereo’s conditioning inputs. First, we describe the 3D pointmap generation process from RGB videos via monocular depth estimation and inverse perspective projection (Sec. 9.1). Subsequently, we define the continuous action representation used to condition the world model’s dynamics (Sec. 9.2). 

#### **9.1 3D Pointmap Generation** 

To construct 3D pointmaps, we employ DepthAnything V3 [20], a state-of-theart video depth estimation model capable of jointly estimating dense depth maps and camera parameters from monocular video sequences. Specifically, for each RGB frame **I** _∈_ R<sup>_H×W ×_3</sup> , DA3 predicts a dense depth map **D** _∈_ R<sup>_H×W_</sup> alongside the camera intrinsic matrix **K** _∈_ R<sup>3</sup><sup>_×_3</sup> and extrinsic parameters [ **R** _|_ **t** ], from which we recover the full 3D geometry. For a given pixel ( _u, v_ ) with predicted depth _d_ ( _u, v_ ), its 3D coordinates in the camera coordinate system are computed via inverse perspective projection: 


These camera-space coordinates are subsequently transformed into the world coordinate system. Exploiting the orthogonality of the rotation matrix ( **R**<sup>_−_1</sup> = **R**<sup>_⊤_</sup> ), the inverse extrinsic transformation is efficiently computed as: 


Finally, the computed 3D coordinates are formatted and stored as a 3-channel image **P** _∈_ R<sup>_H×W ×_3</sup> , where each pixel encodes its corresponding world-space position: **P** ( _u, v_ ) = **p**<sup>_⊤_</sup> world<sup>.Thisrepresentationguaranteesstrictpixel-levelspatial</sup> correspondence with the RGB image **I** ( _u, v_ ), enabling homogeneous processing and aligned latent encoding by the respective Video VAEs. 

#### **9.2 Action Representation** 

To precisely condition the world model, each robot action is formulated as a continuous 7-dimensional vector **a** defined in the gripper’s local coordinate frame: 


where: 

- ( _∆x, ∆y, ∆z_ ): Relative translation of the gripper center (in meters). 

- ( _∆θr, ∆θp, ∆θy_ ): Euler angle rotation increments (roll, pitch, yaw, in radians). 

- _w_ gripper: Gripper width (in meters), indicating the distance between the two fingers. 

For numerical stability during the diffusion process, all action components are normalized prior to training. 

RoboStereo 23 

#### **9.3 Optimization Baseline Details** 

We detail the implementation of the optimization baselines, comprising online GRPO and offline DPO. For the GRPO baseline, the key hyperparameters follow the experimental configuration of [52], as summarized in Table 5. The DPO baseline adopts a standard preference-driven offline training paradigm: trajectory data are collected using a supervised fine-tuned OpenVLA-OFT model [18] to construct a 

**Table 5:** Hyperparameters for the GRPO algorithm. 

|**Hyperparameter**<br>**Value**|
|---|
|Optimizer<br>AdamW(_β_1 = 0_._9_, β_2 = 0_._999)<br><br>|
|Learning rate<br>5_×_10<sup>_−_6</sup>|
|Training batch size<br>64|
|Group size _G_<br>8|
|Mini-batch size<br>128|
|Clip ratio _ϵlow_<br>0.20|
|Clip ratio _ϵhigh_<br>0.28|
|Temperature<br>1.6|


preference dataset, upon which the policy is optimized via the DPO objective. To ensure a fair comparison, the model architecture and optimizer settings are kept identical to those of the GRPO baseline. All training policies are evaluated under the same deployment budget and evaluation protocol. 

### **10 Architecture Overview** 

RoboStereo adopts a symmetric twin backbone design with parallel video and pointmap branches built on an identical diffusion transformer (DiT) architecture. As such, the two backbones share the same number of transformer blocks, heads, head dimensions, and FFNs, enabling symmetry at every layer, as seen in Table 6 

**Table 6:** Model Architecture Configuration 

|Model Dim|FFN Dim|Heads|Head Dim||Blocks||
|---|---|---|---|---|---|---|
|||||Self-Attn|Text Cross-Attn|Tower Cross-Attn|
|2048|8192|16|128|56|56|28|


### **11 Video Quality Evaluation Metrics** 

To comprehensively assess the perceptual quality of generated videos, we adopt 16 metrics spanning six sub-dimensions from the embodied world model benchmark WorldArena [33]. As summarized in Table 7, these dimensions encompass visual quality, motion quality, content consistency, physics adherence, 3D accuracy, and controllability. To ensure consistent and fair comparison across heterogeneous metrics, all scores are linearly normalized to [0 _,_ 1] and direction-aligned such that higher values uniformly denote better performance. 

24 R. Zhang et al. 

**Table 7:** Summary of video quality evaluation metrics in WorldArena [33]. 

|**Dimension**|**Metric**|**Computation Method**|
|---|---|---|
||Image Quality|No-reference frame sharpness via MUSIQ [13]; averaged over all<br>frames.|
|**Visual Quality**|Aesthetic Quality|Per-frame aesthetic score via LAION Aesthetic Predictor [17];<br>averaged over all frames.|
||JEPA Similarity|MMD between V-JEPA [**?**] feature distributions of generated<br>and reference videos using a second-order polynomial kernel;<br>exponentiated for normalization.|
||Dynamic Degree|Top-5% optical flow magnitudes (RAFT [5]) mapped via sigmoid<br>to quantify salient motion intensity.|
|**Motion Quality**|Flow Score|Mean optical flow magnitude across all pixels and frames via<br>RAFT; reflects overall motion intensity.|
||Motion Smoothness|SSIM between VFI-predicted [42] and real intermediate frames,<br>weighted by motion magnitude to penalize static sequences.|
||Subject Consistency|Mean cosine similarity of DINO [43] frame features relative to<br>first and previous frames;|
|**Content Consistency**||penalized by a dynamic degree to prevent static-video shortcuts.|
||Background Consistency|Mean cosine similarity of CLIP [31] frame features relative to<br>first and previous frames; similarly penalized by dynamic degree.|
||Photometric Consistency|<sup>Inverse of forward-backward optical flow warp error (AEPE);</sup><br>scaled by dynamic degree to penalize near-static videos.|
||Interaction Quality|VLM-based (Qwen3-VL [3]) Likert scoring (1–5) of physical<br>plausibility of robot-object contact, normalized to [0_,_1].|
|**Physics Adherence**|Trajectory Accuracy|Normalized<br>Dynamic<br>Time<br>Warping<br>(NDTW)<br>between<br>SAM3 [6]-extracted arm trajectories and ground-truth; inverted<br>so higher is better.|
|**3D Accuracy**|Depth Accuracy|Absolute relative error between median-scaled monocular depth<br>maps (Depth-Anything [40]) of generated and reference videos;<br>inverted for normalization.|
||Perspectivity|VLM-based (Qwen3-VL) Likert scoring of 3D geometric plausi-<br>bility, including scale, occlusion, and lighting consistency, nor-<br>malized to [0_,_1].|
||Instruction Following|VLM-based (Qwen3-VL) Likert scoring of action-type, target-<br>object, and task-state adherence to instruction, normalized to<br>[0_,_1].|
|**Controllability**|Semantic Alignment|Cosine similarity between CLIP text encodings of Qwen2.5-<br>VL [3]-generated descriptions of generated and reference videos.|
||Action Following|Mean pairwise CLIP feature dissimilarity across videos gener-<br>ated from distinct instructions; measures instruction-driven out-<br>put diversity.|


