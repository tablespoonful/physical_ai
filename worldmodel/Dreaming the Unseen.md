---
title: "Dreaming the Unseen: World Model-regularized Diffusion Policy for Out-of-Distribution Robustness"
date: "2026-03-22"
authors: "Ziou Hu; Xiangtong Yao; Yuan Meng; Zhenshan Bing; Alois Knoll"
url: https://arxiv.org/abs/2603.21017
pdf: https://arxiv.org/pdf/2603.21017
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.21017)** / [論文ページ](https://arxiv.org/abs/2603.21017)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Dreaming the Unseen: World Model-regularized Diffusion Policy for Out-of-Distribution Robustness** 

Ziou Hu<sup>1</sup><sup>_⋆_</sup> , Xiangtong Yao<sup>1</sup><sup>_⋆_</sup> , Yuan Meng<sup>1</sup> , Zhenshan Bing<sup>2</sup><sup>_,_1</sup> , and Alois Knoll<sup>1</sup> 

> 1 School of Computation, Information and Technology, Technical University of Munich, Garching, Germany 

- 2 State Key Laboratory for Novel Software Technology and the School of Science and Technology, Nanjing University (Suzhou Campus), China 

**Abstract.** Diffusion policies excel at visuomotor control but often fail catastrophically under severe out-of-distribution (OOD) disturbances, such as unexpected object displacements or visual corruptions. To address this vulnerability, we introduce the **Dream Diffusion Policy (DDP)** , a framework that deeply integrates a diffusion world model into the policy’s training objective via a shared 3D visual encoder. This co-optimization endows the policy with robust state-prediction capabilities. When encountering sudden OOD anomalies during inference, DDP detects the real-imagination discrepancy and actively abandons the corrupted visual stream. Instead, it relies on its internal “imagination”—autoregressively forecasted latent dynamics—to safely bypass the disruption, generating imagined trajectories before smoothly realigning with physical reality. Extensive evaluations demonstrate DDP’s exceptional resilience. Notably, DDP achieves a 73.8% OOD success rate on MetaWorld (vs. 23.9% without predictive imagination) and an 83.3% success rate under severe real-world spatial shifts (vs. 3.3% without predictive imagination). Furthermore, as a stress test, DDP maintains a 76.7% real-world success rate even when relying entirely on open-loop imagination post-initialization. 

**Keywords:** World Model · Diffusion Policy · Out-of-Distribution Robustness 

## **1 Introduction** 

Robotic manipulation in unstructured environments demands policies that can transform rich visual observations into precise, temporally extended motor commands. Recent visuomotor methods, like diffusion-based policies, have emerged as a compelling paradigm for this setting: instead of regressing a single action, they model action generation as a conditional denoising process [7,20,57] or via 

> _⋆_ Equal contribution 

2 Ziou Hu, Xiangtong Yao et al. 

flow matching [58]. These policies have demonstrated remarkable dexterity and robustness in intricate, high-dimensional robot manipulation tasks [7,19,37,47]. 

However, standard visuomotor imitation learning remains fundamentally brittle due to its strict reliance on continuous, uncorrupted visual streams. In realworld deployments, dynamic disturbances (e.g., severe object displacements or camera occlusions) instantly push observations into out-of-distribution (OOD) states, and without explicit physical reasoning, standard policies cannot recover from this massive covariate shift, inevitably leading to compounding errors and catastrophic failure [12,43,61]. Existing methods attempt to mitigate these shifts through various strategies, including domain randomization [38], test-time adaptation [39, 53,54], explicit expansion of training datasets with synthetic spatial perturbations [59], or the application of large pretrained visual models [11]. Other approaches enhance representational and physical priors [1, 21, 40, 45], or learn explicit inverse recovery policies [12,36]. While somewhat effective, these mitigations typically introduce highly complex architectural pipelines and aggressively alter expert-derived actions during adaptation. This fundamentally compromises the core objective of imitation learning, as the high-fidelity skills carefully extracted from experts are ultimately overwritten rather than preserved. 

To overcome these limitations, we rethink how agents handle corrupted visual states by drawing inspiration from human motor mastery. When environmental visual cues become chaotic or deceptive, the optimal human strategy is often to effectively **close one’s eyes** and rely on internal kinesthetic intuition, guided by a single, unwavering focal point. We translate this philosophy into robotic continuous control, arguing that a diffusion policy can be made substantially more resilient by endowing it with a built-in predictive capability. 

The natural technical counterpart to this internal intuition is a world model. Traditionally, these models predict future latent states to support planning [15], enable highly sample-efficient learning [35], and equip agents with crucial predictive reasoning [18]. Diffusion-based world models have emerged as a powerful tool to flexibly forecast complex physical dynamics [3, 6], making them ideal candidates to provide predictive intuition. Yet, current methods typically treat them as weakly coupled auxiliary modules. Lacking a mechanism to dynamically substitute corrupted vision with imagined latents, these policies remain fatally tethered to deceptive observations and collapse under severe OOD shifts. To sustain control, the world model must transcend passive regularization and become a tightly integrated, active predictive intuition. 

We propose the **Dream Diffusion Policy (DDP)** to tackle severe out-ofdistribution (OOD) disturbances. Rather than passively relying on vulnerable visual streams, DDP tightly couples a diffusion policy [7] with a predictive world model [10] via a _shared 3D visual encoder_ . As the policy learns standard behavior cloning [7], the world model simultaneously predicts future observation latents. This shared representation captures robust geometric priors, empowering the world model to actively assist when physical observations become unreliable. During inference, DDP dynamically shifts between physical reality and internal “imagination.” By tracking targets and executing core actions entirely within 

Dream Diffusion Policy 3 

its hallucinated latent space, the robot safely bypasses corrupted vision and physically recovers the environment to an In-Distribution (ID) state. 

We extensively validate DDP across 10 MetaWorld [56] tasks, 3 complex Adroit [31] tasks, and 3 real-world Franka Panda tasks. While Adroit evaluations confirm our world model’s predictive stability in high-DoF continuous control, MetaWorld and real-robot experiments demonstrate DDP’s exceptional resilience to severe OOD disruptions—such as sudden displacements and complete visual occlusions. Notably, DDP achieves a 73 _._ 8% OOD success rate on MetaWorld (vs. 23 _._ 9% for a tracking-augmented baseline) and an 83 _._ 3% success rate under severe real-world spatial shifts (vs. 3 _._ 3%). Furthermore, as a stress test, DDP maintains a remarkable 76 _._ 7% real-world success rate even when relying entirely on open-loop imagination post-initialization. In summary, our primary contributions are: 

- **World-Model-Regularized Training Pipeline:** We propose the Dream Diffusion Policy, which co-optimizes behavior cloning and world-model objectives via a shared 3D encoder. This unified representation allows the world model’s future predictions to directly regularize and guide policy inference. 

- **Robust Inference via Predictive Imagination:** We design a novel, subtask-aware execution mechanism that actively detects OOD states via a highly intuitive real-imagination discrepancy ( _DR−I_ ), bypasses corrupted vision using autoregressive imagination, and triggers a localized physical recovery to the ID state to resume normal execution. 

- **State-of-the-Art OOD Robustness:** We demonstrate that DDP significantly outperforms state-of-the-art baselines under severe OOD conditions across both simulated and real-world tasks, maintaining exceptional resilience even when operating completely blind after initial observation. 

## **2 Related Works** 

**Diffusion Policy for Robotic Manipulation.** By framing action generation as conditional denoising, diffusion models [20] effectively capture complex, multimodal distributions in high-dimensional continuous control [7,57]. These policies achieve state-of-the-art results across diverse applications, including kinematicsaware [27], contact-rich [41,48], and cross-manipulator tasks [34,54]. Additionally, mechanisms like receding-horizon control and stochastic Langevin dynamics provide inherent robustness against minor physical perturbations and transient visual distractions in real-world deployments [7,48]. 

**World Models for Decision Making and Robotics.** World models learn internal representations to predict environmental dynamics and guide decisionmaking [9]. Pioneered by the Dreamer series [16–18], agents can master complex continuous control entirely within a learned latent imagination. This paradigm is now advancing embodied AI: models like NVIDIA Cosmos [2] enforce strict physical laws as “physical AI” brains, while architectures like DreamZero [55] jointly forecast future states and motor actions. Ultimately, integrating predic- 

4 Ziou Hu, Xiangtong Yao et al. 

tive world models directly into control policies provides the crucial “imagination” required for robust robotic manipulation. 

**OOD Challenges and Mitigation Strategies.** Deployed policies inevitably face Out-of-Distribution (OOD) shifts. Standard mitigations expand training diversity via domain randomization [38], synthetic trajectories [21], or reinforcement learning (RL) [40]. However, these methods fail under severe conditions—like camera occlusions or target shifts—because they assume a continuous visual stream. Without visual evidence, policies suffer from shortcut learning [13], fatally over-relying on proprioception for spatial localization. Furthermore, RL fine-tuning [6,8] cannot reconstruct missing visual data at inference, while heavy online pipelines [11] and video-diffusion reward models [22] are computationally prohibitive. 

While world models [15] and diffusion variants [10] forecast states to handle partial observability, current integrations treat them as weakly coupled auxiliary modules that still collapse under severe shifts. To overcome this, we embed lightweight predictive capabilities directly into the policy. By co-optimizing a diffusion policy and world model via a shared-encoder regularizer, we avoid complex decoupled architectures and expensive RL fine-tuning [6]. This tight coupling empowers the policy to seamlessly “dream” missing visual context, sustaining robust control even during severe sensor dropouts. 

## **3 Methods** 

Building on DP3 [57], our Dream Diffusion Policy (DDP) utilizes a shared 3D encoder to extract unified geometric latent embeddings from point clouds and robot proprioception. These embeddings jointly condition both the Diffusion Policy and the Diffusion World Model. During training, the World Model loss acts as a regularizer for the policy, embedding environmental kinematics and dynamics into the shared representation. During inference, this coupled architecture empowers the agent to use “Imagination”—forecasting future observations—to sustain robust execution under Out-of-Distribution scenarios, as outlined in Fig. 1. 

### **3.1 Action and Latent Embedding Chunking** 

Action chunking acts as policy compression in human motor control [24]. In robotic imitation learning, it better captures temporal dependencies [26] and mitigates compounding errors common in strictly autoregressive models [5]. Motivated by this, we synchronize our policy and world model via explicit chunking: 

**Action Chunking:** Our Diffusion Policy denoises a full trajectory over horizon _H_ . To balance long-term consistency and local reactivity, the agent executes only a sub-sequence “chunk” of length _N_ . 

**Latent Embedding Observation Chunking:** To enable forward-looking “imagination”, the World Model operates over the same chunk. Given _M_ historical observations and the _N_ -step planned action chunk, it predicts _N_ future 

Dream Diffusion Policy 5 


**Fig. 1: Overview of the Dream Diffusion Policy (DDP) framework. (a)** A shared 3D encoder extracts unified latent embeddings from point clouds and proprioception. These history latents jointly condition the Diffusion Policy to denoise action chunks, and the Diffusion World Model (via channel-wise concatenation) to forecast future latent states. **(b)** During inference stage, upon detecting an Out-of-Distribution anomaly, the system halts, tracks the object, and transitions into an imagination loop. The World Model autoregressively forecasts latent states to drive the policy’s action generation, safely bypassing corrupted observations until the recovery is triggered. 

latent states in parallel. For continuous OOD rollouts, we apply a sliding window: the final _M_ predicted latents become the historical condition for the next cycle, tightly aligning planned actions with expected outcomes. 

### **3.2 Diffusion Policy** 

Building upon standard DDPM [20], our diffusion policy _πθ_ formulates action generation as a conditional denoising task, predicting an action sequence **a** 0 _...H−_ 1 over horizon _H_ . Following DP3 [57], we utilize a shared 3D encoder _Eψ_ to process raw historical observations **X** 0 _...M −_ 1. This encoder extracts spatial features from geometric point clouds via PointNet and encodes proprioceptive states (e.g., end-effector pose) via an MLP, concatenating both streams to yield the unified context **O** 0 _...M −_ 1. During the forward diffusion process, Gaussian noise _ϵp ∼ N_ (0 _,_ **I** ) is added to the ground-truth actions to generate a noisy trajectory **a**<sup>_kp_</sup> at a randomly sampled timestep _kp ∼U_ (1 _, K_ ). 

The core of the policy is a 1D Conditional U-Net. The encoded history context **O** 0 _...M −_ 1 serves as a global condition. It is injected into the intermediate residual blocks of the U-Net via Feature-wise Linear Modulation (FiLM) [30], allowing the visual state to guide the action denoising process effectively. The objective function for the policy is standard Behavior Cloning (BC) via noise matching: 


- 6 Ziou Hu, Xiangtong Yao et al. 

|**Al**|**gorithm 1:** Dream Diffusion Policy Training|
|---|---|
|**I**<br>**1 w**|**nput:** Dataset _D_, Max steps _K_, 3D Encoder _Eψ_, Policy _πθ_, World Model _Wϕ_<br>**hile** _not converged_ **do**|
||`// 1. Sample Trajectories(`_M_`: observation steps,` _N_`: action`<br>`steps,` _H_`: horizon)`|
|**2**|Sample (_X_0_...M_+_N−_1_, a_0_...H−_1)_∼D_;<br>`// 2. Encode Observations`|
|**3**|_O_0_...M−_1 _←Eψ_(_X_0_...M−_1);|
|**4**|_OM...M_+_N−_1 _←Eψ_(_XM...M_+_N−_1);<br>`// 3. Diffusion Policy Loss`|
|**5**|_kp ∼U_(1_, K_)_, ϵp ∼N_(0_,_**I**);<br>|
|**6**|_a_<br>_kp_<br>0_...H−_1 <sup>_←_AddNoise(</sup><sup>_a_0</sup><sup>_...H−_1</sup><sup>_, ϵp, kp_);</sup>|
|**7**|_LBC ←_MSE<br>�<br>_ϵp, πθ_(_a_<br>_kp_<br>0_...H−_1<sup>_, kp,_ FiLM(</sup><sup>_O_0</sup><sup>_...M−_1))</sup><br>�<br>;|
||`// 4. Diffusion World Model Loss`|
|**8**|_kw ∼U_(1_, K_)_, ϵw ∼N_(0_,_**I**);<br>|
|**9**|_O_<sup>_kw_</sup><br>_M...M_+_N−_1 <sup>_←_AddNoise(</sup><sup>_OM...M_+</sup><sup>_N−_1</sup><sup>_, ϵw, kw_);</sup><br>|
|**10**|_Cwm ←_cat(_O_0_...M−_1_, O_<sup>_kw_</sup><br>_M...M_+_N−_1<sup>);</sup>|
|**11**|_LW M ←_MSE(_ϵw, Wϕ_(_Cwm, kw,_FiLM(_aM−_1_...M_+_N−_2)));<br>`// 5. Optimization`|
|**12**|_Ltotal ←LBC_ +_λLW M_;|
|**13**|Update _ψ, θ, ϕ_ using _∇ψ,θ,ϕLtotal_;|


### **3.3 Diffusion World Model** 

Based on the framework in [10], our Diffusion World Model _Wϕ_ predicts _N_ - step future latent embeddings **O** _M...M_ + _N −_ 1. During training, the shared 3D encoder _Eψ_ extracts these future targets, which are then corrupted with noise _ϵw_ at timestep _kw_ to yield **O**<sup>_k_</sup> _M...M_<sup>_w_</sup> + _N −_ 1<sup>.Becauseactions(directionalcontrols)</sup> and observations (geometric context) possess fundamentally distinct properties, we deviate from the sampling-based “prefix-fixing” conditioning used in [10]. We argue that fixing initial states during reverse diffusion lacks the persistent grounding required for high-dimensional point cloud latents. Instead, we employ direct **feature-level integration** [32]. By repeating the historical latent **x** _obs_ across the temporal horizon and concatenating it channel-wise with the noisy samples, we formulate the input as: 


This ensures every convolutional layer in the 1D U-Net has immediate, continuous access to the historical structural context. 

Concurrently, the executed action sequence **a** _M −_ 1 _...M_ + _N −_ 2 serves as a global condition. As in the policy architecture, these action representations are fused with the diffusion timestep embeddings and injected via FiLM. The world model is optimized by minimizing the noise prediction error: 


Dream Diffusion Policy 7 

### **3.4 Training Objective** 

We jointly optimize the Diffusion Policy and World Model end-to-end. Using normalized expert demonstrations, the shared encoder _Eψ_ extracts latent embeddings for both historical context and future targets. The policy _πθ_ learns to predict Gaussian noise added to the action horizon **a** 0 _...H−_ 1 conditioned on the history **O** 0 _...M −_ 1. Simultaneously, the world model _Wϕ_ predicts the noise injected into future observation latents **O** _M...M_ + _N −_ 1, conditioned on the history and executed actions. Following established regularization strategies [1,21], the world model acts as a geometric and dynamic regularizer. We update the network parameters ( _ψ, θ, ϕ_ ) via gradient descent using a combined loss: 


where _λ_ balances the two objectives. Finally, we apply an Exponential Moving Average (EMA) [29] to the model weights to stabilize convergence and enhance inference robustness (Algorithm 1). 

### **3.5 Inference Stage** 

During inference, dynamic object displacements break the In-Distribution (ID) environment, triggering an Out-of-Distribution (OOD) state. To maintain spatial awareness during these disruptions, we integrate a 6D pose estimator (e.g., FoundationPose [44]). By combining this estimator with the World Model’s predictive “imagination,” we introduce a hybrid mechanism of detection, recursive imagination, and physical recovery to safely bridge OOD gaps, as illustrated in the closed-loop workflow of Fig. 2. The pseudocode for closed-Loop inference is provided in Algorithm 2 in Appendix. 

**Subtask Definition** For long-horizon manipulation, we define a subtask sequence _S_ = _{S_ 1 _, . . . , SJ }_ , each targeting an object _Cj_ . Lacking explicit dataset annotations, we bypass complex clustering and use simple expert heuristics for completion triggers (e.g., gripper closure for picking, allocated time for pouring). This flexibility allows DDP to solve complex, multi-stage challenges. 

**Real-Imagination Discrepancy as OOD Detector.** Unlike methods relying on reconstruction errors [14,23] or diffusion loss [25], we take a highly intuitive approach: detecting OOD anomalies via the latent discrepancy between the real observation **O**<sup>_t_</sup> _real_<sup>=</sup><sup>_Eψ_(</sup><sup>_X_</sup> _real_<sup>_t_)andtheWorldModel’sprediction</sup><sup>**O**</sup><sup>_t_</sup> _pred_<sup>:</sup> 


Nominal actions maintain a low _DR−I_ . When an external disturbance pushes _DR−I_ ( _t_ ) above a threshold _τdiff_ , an OOD event is flagged. To identify _which_ objects moved, we query the pose estimator, comparing current poses to expected ID states to isolate the displaced objects _Cdisp_ . 

**Simplified Object Tracking under OOD.** Rather than relying on continuous tracking during chaotic displacements, we assume the displaced object _Cj_ eventually settles into a static pose. Once motion ceases, we query the 6D pose 

- 8 Ziou Hu, Xiangtong Yao et al. 


**Fig. 2: Overview of the DDP workflow.** Illustrating the closed-loop transitions between physical reality (ID) and internal imagination (OOD) across subtasks. 

estimator for its new resting pose **p** _Cj ∈ SE_ (3). By comparing this to its expected ID pose **p**<sup>_exp_</sup> _Cj_<sup>,wecomputeasinglestaticspatialdisplacement:</sup> 


To re-align the robot with the displaced target, we directly apply this offset as a compensatory tracking action for the end-effector, defined as **a**<sup>_track_</sup> _j_ = _∆_ **p** _Cj_ . **Recursive Imagination for Action Generation** To bypass corrupted physical observations during an OOD state, we implement a recursive “wheel” mechanism for imagined execution after tracking (Fig. 1(b)). Instead of using real visual inputs, the policy generates action chunks ( _a_ 0 _. . . aN_ ) conditioned entirely on the previously predicted latent embedding. Concurrently, the Diffusion World Model uses this imagined latent and the newly predicted actions to forecast the _next_ latent state ( _O_ 0 _. . . OM_ ). Autoregressively feeding these forecasts back into the policy sustains a coherent trajectory purely within the agent’s internal imagination, enabling safe task execution until target recovery is triggered. **Target-Specific Recovery.** Since simultaneous global recovery is impractical, we restore the environment iteratively. For an imagined subtask _Sj_ targeting _Cj ∈Cdisp_ , we define a simple heuristic boolean trigger _Tend_ ( _Sj_ ). Once _Tend_ ( _Sj_ ) = True, the agent applies an inverse spatial translation **a**<sup>_rec_</sup> _j_ = _−∆_ **p** _Cj_ to realign the imagined trajectory with the physical object, removing _Cj_ from _Cdisp_ . We then re-evaluate _DR−I_ : if it remains above _τdiff_ , the policy continues executing via imagination. Otherwise, the environment is fully recovered, and the policy reverts to the real visual latent **O**<sup>_t_</sup> _real_<sup>forstandardIDexecution.</sup> 

## **4 Experiments** 

### **4.1 Simulation Experiments** 

**Benchmarks and Datasets** To evaluate the proposed method, we utilize two widely adopted continuous control simulation benchmarks: MetaWorld [56] and Adroit [31]. Specifically, we construct our evaluation pool using 10 MetaWorld 

Dream Diffusion Policy 9 


**Fig. 3: Out-of-Distribution (OOD) spatial disturbances in MetaWorld. Yellow dashed boxes** highlight target objects, and **solid arrows** indicate the direction of dynamic displacements injected mid-task. The exact linear translation vectors ( _x, y, z_ ) applied to shift each object out-of-distribution are detailed below. 

tasks, ranging from simple to hard difficulties, to test general robotic manipulation capabilities. Additionally, to assess performance on highly complex dynamical systems, we select 3 tasks from the Adroit benchmark. 

**Model Setup** The shared 3D visual encoder processes _M_ = 2 observation steps, concatenating 64-dimensional features from both a PointNet (point cloud) and an MLP (proprioception) into a 128-dimensional unified latent embedding. Conditioned on this _M_ = 2 history, the Diffusion Policy predicts an action horizon of _H_ = 16 and executes an _N_ = 8 step chunk. It employs a 1D U-Net with down-sampling channels of [256 _,_ 512 _,_ 1024] and a 128-dimensional diffusion step embedding. Concurrently, the Diffusion World Model uses a separate, identically parameterized 1D U-Net to predict _N_ = 8 future latent embeddings conditioned on the _M_ = 2 history and _N_ = 8 planned actions. _λ_ is set to 1. 

**Out-of-Distribution Setup** To test robustness against spatial shifts, we evaluate OOD performance exclusively in MetaWorld. During training, targets are randomized within a fixed In-Distribution area. For OOD inference, we introduce sudden mid-task displacements, moving objects entirely outside these training boundaries (Fig. 3). Applied as direct linear coordinate translations in MuJoCo, these shifts provide measurable disturbances to reliably evaluate recovery. 

**Training and Evaluation** For a fair and rigorous comparison, we benchmark our Dream Diffusion Policy (DDP) against two state-of-the-art baselines: DP3 [57] and FlowPolicy [58]. All models are trained for 500 epochs with 3 seeds (seed0, 1, 2) using a fixed dataset of 50 demonstrations per task. To ensure an equitable evaluation, the foundational policy architectures and core hyperparameters across all methods are kept strictly identical. During inference, we evaluate each method for 100 episodes per task, per seed, and calculate the average success rate. Our evaluation is systematically divided into the following phases: 

10 Ziou Hu, Xiangtong Yao et al. 

**Table 1: Evaluation Results (Success Rate %).** We report the In-Distribution (ID) and Out-of-Distribution (OOD) performance of the base policies, the trackingaugmented policies (DP3 ablation, Flow Policy, our DDP) under OOD, and the robustness of DDP under various imagination substitution rates. 

|**Algorithm /**<br>**Condition**|Door|**Adroit**<br> Hammer|Pen|Assembly|<sup>Button</sup><br>Press|Coffee<br>Pull|Door<br>Unlock|**MetaW**<br>Drawer<br>Open|**orld**<br> <sup>Hammer</sup>|Pick<br>Place|Push|Soccer|Sweep|**Adroit **<br>**Avg**|**MetaWorl**<br>**Avg**|**d Total**<br>**Avg**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Base Policy (ID)**|||||||||||||||||
|DP3|69_±_4|100_±_0|76_±_7|100_±_0|100_±_0|99_±_1|100_±_0|100_±_0|100_±_0|95_±_1|94_±_1|35_±_3|100_±_0|81.5|92.3|89.8|
|FlowPolicy|64_±_4|88_±_1|67_±_4|100_±_0|100_±_0|100_±_0|100_±_0|100_±_0|98_±_1|96_±_1|95_±_1|53_±_6|100_±_0|72.9|94.2|89.3|
|**DDP (Ours)**|63_±_3|99_±_1|71_±_2|100_±_0|100_±_0|100_±_0|100_±_0|100_±_0|100_±_0|95_±_1|93_±_1|42_±_7|100_±_0|77.8|93.0|89.5|
|**Base Policy (OOD)**|||||||||||||||||
|DP3|-|-|-|0_±_0|0_±_0|0_±_0|2_±_2|4_±_2|0_±_0|0_±_0|0_±_0|1_±_1|0_±_0|-|0.8|0.8|
|FlowPolicy|-|-|-|0_±_0|11_±_5|0_±_0|53_±_14|0_±_0|1_±_1|0_±_0|0_±_0|2_±_2|0_±_0|-|6.7|6.7|
|**DDP (Ours)**|-|-|-|0_±_0|0_±_0|0_±_0|5_±_5|3_±_0|1_±_1|0_±_0|0_±_0|4_±_2|0_±_0|-|1.3|1.3|
|**Tracking-Augmented **|**(OOD**|**)**|||||||||||||||
|FlowPolicy|-|-|-|0_±_0|13_±_2|0_±_0|41_±_5|0_±_0|0_±_0|0_±_0|0_±_0|0_±_0|0_±_0|-|5.4|5.4|
|DP3 (Ablation)|-|-|-|0_±_0|93_±_3|23_±_4|59_±_16|3_±_2|1_±_0|13_±_13|9_±_3|16_±_4|22_±_14|-|23.9|23.9|
|**DDP (Ours)**|-|-|-|96_±_2|100_±_0|94_±_3|74_±_4|100_±_0|100_±_0|39_±_5|39_±_6|17_±_4|79_±_7|-|**73.8**|**73.8**|
|**DDP Imagination Int**|**ervent**|**ions (ID**|**)**||||||||||||||
|**DDP (10% Imagined**|**)**<br>95_±_3|99_±_0|92_±_1|100_±_0|100_±_0|100_±_0|99_±_0|98_±_1|100_±_0|93_±_3|93_±_2|40_±_3|100_±_0|**95.2**|**92.3**|**93.0**|
|**DDP (50% Imagined**|**)**<br>96_±_1|98_±_2|87_±_3|99_±_0|100_±_0|98_±_1|99_±_1|90_±_1|100_±_0|81_±_6|91_±_2|39_±_3|98_±_1|**94.0**|**89.4**|**90.5**|
|**DDP (Open-loop)**|96_±_3|98_±_2|86_±_3|18_±_2|100_±_0|54_±_3|97_±_1|48_±_3|99_±_0|21_±_3|38_±_3|42_±_3|97_±_1|**93.2**|**61.4**|**68.7**|


1. **Base Policy Accuracy (ID & OOD):** Evaluating standard In-Distribution and Out-of-distribution performance of DP3, FlowPolicy, and DDP. 

2. **Dream Diffusion Policy Accuracy (OOD):** Evaluating DDP using our tracking, imagination and recovery mechanism under OOD conditions. 

3. **Ablation Tracking-Augmented Accuracy (OOD):** To isolate the benefits of our World Model, we perform a direct ablation by applying the tracking intervention to the base DP3 policy. We additionally evaluate FlowPolicy equipped with the same tracking mechanism for a broader comparison. 

4. **World Model Imagination Analysis (ID):** To test the World Model’s reliability, we randomly replace real observation with imagined latents after the initial chunk at 10%, 50% and 100% (open-loop imagined rollout) probabilities. 

**Results** As shown in Tab. 1, standard base policies fail under severe OOD shifts. However, our tracking-augmented DDP effectively handles these disturbances, achieving a 73.8% average success rate on MetaWorld. Applying identical tracking to the baselines yields lower success rates (23.9% for DP3, 5.4% for FlowPolicy). This proves tracking alone is insufficient; the Diffusion World Model’s coupled latents are crucial for robust task completion. 

Figure 4 illustrates DDP’s execution on the MetaWorld Assembly and Push tasks. In Assembly (2 subtasks), the second object peg is displaced Out-ofDistribution after the robot grasps the ring. After tracking this shift, DDP executes a precise action to successfully insert the ring. In Push (2 subtasks), the first object puck is displaced before grasping. DDP tracks the shifted puck, execute actions via imagination, utilizes a localized recovery action to move the end-effector to ID position, and accurately pushes it to the target. For more comprehensive results, please refer to Sec. B in the Appendix. 

Furthermore, Tab. 1 demonstrates DDP’s resilience when replacing real observations with imagined latents. On MetaWorld, DDP maintains near-baseline 

Dream Diffusion Policy 11 


**Fig. 4: DDP execution on MetaWorld Assembly and Push.** Sequences show the transition from the ID Base Policy (green) to OOD tracking (yellow), bypassing visual shifts via the imagined Dream Policy (pink), and finally recovering to the target. 

accuracy at 10% (92.3%) and 50% (89.4%) substitution rates, remaining robust even at 100% (61.4%). On the complex Adroit benchmark, imagination actually _boosts_ success from a 77.8% baseline to 95.2% at 10% substitution. This confirms the built-in World Model not only bridges visual gaps but also acts as a temporal smoother, stabilizing high-DoF continuous control. 

### **4.2 Real World Experiments** 

**Real Robot Benchmark** To evaluate physical efficacy and performance under OOD, we design three real-world manipulation tasks of varying complexity. During training, initial target positions are uniformly randomized along a 10 cm linear range to ensure baseline state variance. 

- **Press Button (Easy | 1 Subtask, 1 OOD Target):** The robot closes its gripper to precisely press a button. Success requires depressing it exactly to the activation threshold, avoiding both incomplete contact (under-pressing) and excessive force (over-pressing). 

- **Pour Tea (Medium | 2 Subtasks, 1 OOD Target):** The robot grasps a teapot, navigates to a cup, executes a pouring motion, and returns the teapot to the table. Success requires the spout to remain precisely aligned with the cup’s center during the entire pour. 

- **Stack Blocks (Hard | 2 Subtasks, 2 OOD Targets):** The robot picks up a pink block and places it atop a green base block. Success requires the pink block to remain perfectly stable and balanced after the gripper releases. 

**Hardware and State Setup** We deploy our framework on a Franka Emika Panda with a Robotiq 2F-85 gripper. An Intel RealSense L515 captures visual observations, while a D455 camera continuously tracks objects. To ensure low latency, raw point clouds are downsampled via Farthest Point Sampling to 2048 points. Hardware setup is shown in Fig. 5. The proprioceptive state consists of the end-effector pose. The action space is formulated as 7-DoF relative commands ( _∆x, ∆y, ∆z_ , roll, pitch, yaw) resolved via the _franky_ [33] inverse kinematics library, plus a binary gripper state (Close or Open). 

**Data Collection, Network Architecture and Compute** We collect 25 expert demonstrations per task via a scripted kinematic oracle that injects spa- 

- 12 Ziou Hu, Xiangtong Yao et al. 


**Fig. 5: Robot Setup and Objects Tracking.** (a) is all the hardware for the realworld experiment. (b) shows the bounding box for object tracking across all tasks. 

**Table 2: Real Robot Evaluation Results (Success Rate %).** We evaluate the baseline and our Dream Diffusion Policy (DDP) across three tasks (10 trials each) of varying difficulty under In-Distribution (ID) and Out-of-Distribution (OOD) settings. 

|**Algorithm / Condition**<br>**Pr**|**ess Butto**|**n**<br>**Pour Tea**<br>|**Stack Bloc**|**ks**<br>**Average**|
|---|---|---|---|---|
|**Base Policy (ID)**|||||
|DP3|100|90|90|93.3|
|**DDP (Ours)**|100|90|80|**90.0**|
|**Tracking-Augmented (OOD)**|||||
|DP3 (Ablation)|10|0|0|3.3|
|**DDP (Ours)**|100|90|60|**83.3**|
|**Imagination Intervention (ID)**|||||
|**DDP (Open-loop Imagination)**|100|80|50|**76.7**|


tial variance to efficiently mimic human data distributions. For high-speed realtime control, we employ “Simple DDP”, a lightweight architecture inspired by DP3. It utilizes reduced-capacity 1D U-Nets with down-sampling dimensions of [128 _,_ 256 _,_ 384] for the Diffusion Policy and [128 _,_ 256 _,_ 512] for the Diffusion World Model. Finally, we retain all sequence hyperparameters from simulation: _M_ = 2, _H_ = 16, _N_ = 8, and _λ_ = 1. The models are trained for 2000 epochs on a NVIDIA 4090 GPU. During deployment, the DDP architecture is hosted on an NVIDIA 4070 GPU, with inference times of 40 ms for the diffusion policy and 70 ms for the world model. Concurrently, to guarantee robustness in real-time tracking, we utilize the FoundationPose++ [49] module, as shown in Fig. 5(b). For further comprehensive detail, please refer to Sec. C in the Appendix. 

**Results** Fig. 10 in the Appendix illustrates the successful execution sequences of DDP under In-Distribution (ID) settings for the three real-world tasks: Press Button, Pour Tea, and Stack Blocks. To evaluate OOD robustness, target objects are abruptly moved completely outside the In-Distribution (ID) zone mid-task. As shown in Fig. 6, our OOD detector identifies these displacements by monitoring _latent discrepancy_ in real-time, which quantifies the latent distance between actual visual observations and the policy’s imagined projections. Sudden dis- 

Dream Diffusion Policy 13 


**Fig. 6: OOD Detection via Real-Imagination Discrepancy.** The detector successfully identifies anomalies when objects are accidentally shifted across three different tasks. An OOD state is triggered (shaded regions) when the latent discrepancy ( _DR−I_ ) exceeds a task-specific threshold _τdiff_ . Specifically, we set _τdiff_ = 0 _._ 0002 for Stack Blocks, _τdiff_ = 0 _._ 0004 for Pour Tea, and _τdiff_ = 0 _._ 0012 for Press Button. 


**Fig. 7: Qualitative real-robot execution on Stack Blocks, Pour Tea, and Press Button tasks.** DDP successfully tracks OOD objects, finishes the main actions of subtasks via the imagined Dream Policy, and executes recover to achieve the remaining task success. In contrast, the tracking-augmented DP3 ablation fails across severe OOD scenarios. 

14 Ziou Hu, Xiangtong Yao et al. 


**(a) Occlusion scene (b) Stack Blocks (Left: DP3, right: DDP) (c) Pour Tea (Left: DP3, right: DDP)** 

**Fig. 8: Qualitative results under visual occlusion.** (a) A hand obstructs the camera mid-task. In (b) Stack Blocks and (c) Pour Tea, baseline DP3 fails due to visual corruption, whereas DDP seamlessly bypasses the occlusion using internal imagination. 

placements cause the observed visual state to sharply deviate from the imagined trajectory, spiking the discrepancy above a threshold to reliably flag the OOD condition. 

As shown in Tab. 2, our tracking-augmented DDP achieves an 83.3% average success rate, drastically outperforming the DP3 tracking ablation (3.3%). Figure 7 illustrates these execution differences. In the two-subtask _Stack Blocks_ sequence, DDP tracks OOD shifts for each object, finishes the remaining motions via imagination, and triggers a precise physical recovery between subtasks based on the gripper stage; conversely, the DP3 ablation entirely fails to pick the displaced block. In _Pour Tea_ , DDP tracks the shifted cup and seamlessly executes pouring actions from imagination after picking the teapot, whereas DP3 accidentally drops the pot. For _Press Button_ , DDP recovers to press the target precisely to its threshold, while the DP3 ablation fails by either under-pressing or over-pressing. Detailed failure mode illustration for each real-world task is provided Fig. 11. 

Furthermore, we test DDP’s reliance on its internal world model by executing tasks using 100% imagined latents after the first observation chunk (Open-loop Imagination). As detailed in Tab. 2, DDP maintains a remarkable 76.7% average success rate. This performance confirms that the network’s imagined representations are stable and reliable for continuous real-world control. 

**Robustness to Visual Occlusion.** To further evaluate DDP against severe visual occlusion, we block the camera mid-task. This creates a massive realimagination discrepancy ( _DR−I_ ), instantly triggering OOD mode. While the DP3 baseline fails when blinded, DDP safely bypasses the corruption to complete both _Stack Blocks_ and _Pour Tea_ purely via autoregressive imagination (Fig. 8). 

## **5 Conclusion** 

We introduced the Dream Diffusion Policy (DDP) to enhance visuomotor robustness against severe out-of-distribution (OOD) disturbances. Co-optimizing a diffusion policy and world model via a shared 3D encoder embeds predictive dynamics directly into DDP’s representation. During inference, DDP detects OOD anomalies via a real-imagination discrepancy ( _DR−I_ ). Rather than collapsing 

Dream Diffusion Policy 15 

under corrupted vision, it safely bypasses these shifts using an autoregressive imagination loop—executing actions from latent forecasts before triggering a localized physical recovery. Evaluations confirm DDP significantly outperforms baselines **specifically in OOD scenarios** , maintaining a high success rate even under almost complete visual blindness where standard methods fail. 

**Limitations and Future Work.** DDP has three main limitations: (1) It highly relies on external tracking modules, allowing drift to accumulate across multi-stage subtasks, (2) tasks must begin strictly In-Distribution (ID) to properly anchor the initial observation, and (3) the inference mechanism struggles with compounding OOD events or low-level action disruptions (e.g., gripper slippage). Addressing these dependencies remains a key direction for future research. Potential solutions, such as employing meta-reinforcement learning [4,42,50] to adaptively fine-tune the world model online, integrating the lifelong learning mechanism [28] to preserve and combine prior knowledge, or integrating low-level tactile feedback [46], could further enhance DDP’s resilience in real-world applications. We also plan to extend DDP to more complex multi-object manipulation tasks and explore its integration with language-conditioned methods [51,60] or large language models for higher-level reasoning and planning [52]. 

## **References** 

1. Ada, S.E., Oztop, E., Ugur, E.: Diffusion policies for out-of-distribution generalization in offline reinforcement learning. IEEE Robotics and Automation Letters **9** (4), 3116–3123 (2024) 

2. Agarwal, N., Ali, A., Bala, M., Balaji, Y., Barker, E., Cai, T., Chattopadhyay, P., Chen, Y., Cui, Y., Ding, Y., et al.: Cosmos world foundation model platform for physical ai. arXiv preprint arXiv:2501.03575 (2025) 

3. Alonso, E., Jelley, A., Micheli, V., Kanervisto, A., Storkey, A.J., Pearce, T., Fleuret, F.: Diffusion for world modeling: Visual details matter in atari. Advances in Neural Information Processing Systems **37** , 58757–58791 (2024) 

4. Bing, Z., Koch, A., Yao, X., Huang, K., Knoll, A.: Meta-reinforcement learning via language instructions. In: 2023 IEEE International Conference on Robotics and Automation (ICRA). pp. 5985–5991. IEEE (2023) 

5. Cen, J., Yu, C., Yuan, H., Jiang, Y., Huang, S., Guo, J., Li, X., Song, Y., Luo, H., Wang, F., et al.: Worldvla: Towards autoregressive action world model. arXiv preprint arXiv:2506.21539 (2025) 

6. Chandra, A.L., Nematollahi, I., Huang, C., Welschehold, T., Burgard, W., Valada, A.: Diwa: Diffusion policy adaptation with world models. In: Conference on Robot Learning. pp. 3378–3400. PMLR (2025) 

7. Chi, C., Xu, Z., Feng, S., Cousineau, E., Du, Y., Burchfiel, B., Tedrake, R., Song, S.: Diffusion policy: Visuomotor policy learning via action diffusion. The International Journal of Robotics Research **44** (10-11), 1684–1704 (2025) 

8. Curtis, A., Li, E., Noseworthy, M., Gothoskar, N., Chitta, S., Li, H., Kaelbling, L.P., Carey, N.E.: Flow-based domain randomization for learning and sequencing robotic skills. In: Forty-second International Conference on Machine Learning (2025), `https://openreview.net/forum?id=9JQXuyzdGL` 

16 Ziou Hu, Xiangtong Yao et al. 

9. Ding, J., Zhang, Y., Shang, Y., Zhang, Y., Zong, Z., Feng, J., Yuan, Y., Su, H., Li, N., Sukiennik, N., et al.: Understanding world or predicting future? a comprehensive survey of world models. ACM Computing Surveys **58** (3), 1–38 (2025) 

10. Ding, Z., Zhang, A., Tian, Y., Zheng, Q.: Diffusion world model: Future modeling beyond step-by-step rollout for offline reinforcement learning. arXiv preprint arXiv:2402.03570 (2024) 

11. Du, M., Song, S.: Dynaguide: Steering diffusion polices with active dynamic guidance. In: The Thirty-ninth Annual Conference on Neural Information Processing Systems (2025), `https://openreview.net/forum?id=XOw7Yf8qN3` 

12. Gao, G.J., Li, T., Figueroa, N.: Out-of-distribution recovery with object-centric keypoint inverse policy for visuomotor imitation learning. In: 2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS). pp. 9816–9828. IEEE (2025) 

13. Geirhos, R., Jacobsen, J.H., Michaelis, C., Zemel, R., Brendel, W., Bethge, M., Wichmann, F.A.: Shortcut learning in deep neural networks. Nature Machine Intelligence **2** (11), 665–673 (2020) 

14. Graham, M.S., Pinaya, W.H., Tudosiu, P.D., Nachev, P., Ourselin, S., Cardoso, J.: Denoising diffusion models for out-of-distribution detection. In: Proceedings of the IEEE/CVF conference on computer vision and pattern recognition. pp. 2948–2957 (2023) 

15. Ha, D., Schmidhuber, J.: World models. arXiv preprint arXiv:1803.10122 (2018) 16. Hafner, D., Lillicrap, T., Ba, J., Norouzi, M.: Dream to control: Learning behaviors by latent imagination. arXiv preprint arXiv:1912.01603 (2019) 

17. Hafner, D., Lillicrap, T., Norouzi, M., Ba, J.: Mastering atari with discrete world models. arXiv preprint arXiv:2010.02193 (2020) 

18. Hafner, D., Pasukonis, J., Ba, J., Lillicrap, T.: Mastering diverse domains through world models. arXiv preprint arXiv:2301.04104 (2023) 

19. He, C., Liu, X., Camps, G.S., Sartoretti, G., Schwager, M.: Demystifying diffusion policies: Action memorization and simple lookup table alternatives. arXiv preprint arXiv:2505.05787 (2025) 

20. Ho, J., Jain, A., Abbeel, P.: Denoising diffusion probabilistic models. Advances in neural information processing systems **33** , 6840–6851 (2020) 

21. Huang, D., Navab, N., Jiang, Z.: Improving robustness to out-of-distribution states in imitation learning via deep koopman-boosted diffusion policy. IEEE Transactions on Robotics **41** , 6680–6692 (2025) 

22. Huang, T., Jiang, G., Ze, Y., Xu, H.: Diffusion reward: Learning rewards via conditional video diffusion. In: European Conference on Computer Vision. pp. 478–495. Springer (2024) 

23. Isaku, E., Sartaj, H., Ali, S., Sanguino, B., Wang, T., Li, G., Zhang, H., Peyrucain, T.: Out of distribution detection in self-adaptive robots with ai-powered digital twins. arXiv preprint arXiv:2509.12982 (2025) 

24. Lai, L., Huang, A.Z., Gershman, S.J.: Action chunking as policy compression. PsyArXiv (2022) 

25. Lee, S.W., Kang, X., Kuo, Y.L.: Diff-dagger: Uncertainty estimation with diffusion policy for robotic manipulation. In: 2025 IEEE International Conference on Robotics and Automation (ICRA). pp. 4845–4852. IEEE (2025) 

26. Liu, Y., Hamid, J.I., Xie, A., Lee, Y., Du, M., Finn, C.: Bidirectional decoding: Improving action chunking via guided test-time sampling. arXiv preprint arXiv:2408.17355 (2024) 

- Dream Diffusion Policy 17 

- 27. Ma, X., Patidar, S., Haughton, I., James, S.: Hierarchical diffusion policy for kinematics-aware multi-task robotic manipulation. In: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. pp. 18081– 18090 (2024) 

- 28. Meng, Y., Bing, Z., Yao, X., Chen, K., Huang, K., Gao, Y., Sun, F., Knoll, A.: Preserving and combining knowledge in robotic lifelong reinforcement learning. Nature Machine Intelligence **7** (2), 256–269 (2025) 

- 29. Morales-Brotons, D., Vogels, T., Hendrikx, H.: Exponential moving average of weights in deep learning: Dynamics and benefits. arXiv preprint arXiv:2411.18704 (2024) 

- 30. Perez, E., Strub, F., De Vries, H., Dumoulin, V., Courville, A.: Film: Visual reasoning with a general conditioning layer. In: Proceedings of the AAAI conference on artificial intelligence. vol. 32 (2018) 

- 31. Rajeswaran, A., Kumar, V., Gupta, A., Vezzani, G., Schulman, J., Todorov, E., Levine, S.: Learning complex dexterous manipulation with deep reinforcement learning and demonstrations. arXiv preprint arXiv:1709.10087 (2017) 

- 32. Saharia, C., Chan, W., Chang, H., Lee, C., Ho, J., Salimans, T., Fleet, D., Norouzi, M.: Palette: Image-to-image diffusion models. In: ACM SIGGRAPH 2022 conference proceedings. pp. 1–10 (2022) 

- 33. Schneider, T.: franky: High-level control library for franka robots. `https:// github.com/TimSchneider42/franky` (2024), version 1.1.3 

- 34. Seo, M., Park, H.A., Yuan, S., Zhu, Y., Sentis, L.: Legato: Cross-embodiment imitation using a grasping tool. IEEE Robotics and Automation Letters **10** (3), 2854–2861 (2025). `https://doi.org/10.1109/LRA.2025.3535182` 

- 35. Seo, Y., Hafner, D., Liu, H., Liu, F., James, S., Lee, K., Abbeel, P.: Masked world models for visual control. In: Conference on Robot Learning. pp. 1332–1344. PMLR (2023) 

36. Sun, Z., Song, S.: Latent policy barrier: Learning robust visuomotor policies by staying in-distribution. arXiv preprint arXiv:2508.05941 (2025) 

37. Tian, J., Wang, L., Zhou, S., Wang, S., Li, J., Sun, H., Tang, W.: Pdfactor: Learning tri-perspective view policy diffusion field for multi-task robotic manipulation. In: Proceedings of the Computer Vision and Pattern Recognition Conference. pp. 15757–15767 (2025) 

38. Tobin, J., Fong, R., Ray, A., Schneider, J., Zaremba, W., Abbeel, P.: Domain randomization for transferring deep neural networks from simulation to the real world. In: 2017 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS). pp. 23–30. IEEE (2017) 

39. Wang, D., Shelhamer, E., Liu, S., Olshausen, B., Darrell, T.: Tent: Fully testtime adaptation by entropy minimization. In: International Conference on Learning Representations (ICLR) (2021) 

40. Wang, D., Liu, C., Chang, F., Xu, Y.: Hierarchical diffusion policy: manipulation trajectory generation via contact guidance. IEEE Transactions on Robotics (2025) 

41. Wang, D., Liu, C., Chang, F., Xu, Y.: Hierarchical diffusion policy: Manipulation trajectory generation via contact guidance. IEEE Transactions on Robotics **41** , 2086–2104 (2025). `https://doi.org/10.1109/TRO.2025.3547272` 

42. Wang, M., Bing, Z., Yao, X., Wang, S., Kai, H., Su, H., Yang, C., Knoll, A.: Metareinforcement learning based on self-supervised task representation learning. In: Proceedings of the AAAI Conference on Artificial Intelligence. vol. 37, pp. 10157– 10165 (2023) 

- 18 Ziou Hu, Xiangtong Yao et al. 

43. Wang, R., Zhuang, Z., Kragic, D., Pokorny, F.T.: Palm: Enhanced generalizability for local visuomotor policies via perception alignment. arXiv preprint arXiv:2601.19514 (2026) 

44. Wen, B., Yang, W., Kautz, J., Birchfield, S.: Foundationpose: Unified 6d pose estimation and tracking of novel objects. In: Proceedings of the IEEE/CVF conference on computer vision and pattern recognition. pp. 17868–17879 (2024) 

45. Wu, S., Zhu, Y., Huang, Y., Zhu, K., Gu, J., Yu, J., Shi, Y., Wang, J.: Afforddp: Generalizable diffusion policy with transferable affordance. In: Proceedings of the Computer Vision and Pattern Recognition Conference. pp. 6971–6980 (2025) 

46. Wu, Y., Chen, Z., Wu, F., Chen, L., Zhang, L., Bing, Z., Swikir, A., Haddadin, S., Knoll, A.: Tacdiffusion: Force-domain diffusion policy for precise tactile manipulation. In: 2025 IEEE International Conference on Robotics and Automation (ICRA). pp. 11831–11837. IEEE (2025) 

47. Wu, Y., Wang, H., Chen, Z., Pang, J., Xu, D.: On-device diffusion transformer policy for efficient robot manipulation. In: Proceedings of the IEEE/CVF International Conference on Computer Vision. pp. 14073–14083 (2025) 

48. Xue, H., Ren, J., Chen, W., Zhang, G., Fang, Y., Gu, G., Xu, H., Lu, C.: Reactive diffusion policy: Slow-fast visual-tactile policy learning for contact-rich manipulation. In: Proceedings of Robotics: Science and Systems (RSS) (2025) 

49. Yan, W., Chu, J.: Foundationpose++: Simple tricks boost foundationpose performance in high-dynamic scenes. `https://github.com/teal024/FoundationPoseplus-plus` (2025), gitHub Repository 

50. Yao, X., Bing, Z., Zhuang, G., Chen, K., Zhou, H., Huang, K., Knoll, A.: Learning from symmetry: Meta-reinforcement learning with symmetrical behaviors and language instructions. In: IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS). pp. 5574–5581. IEEE (2023) 

51. Yao, X., Blei, T., Meng, Y., Zhang, Y., Zhou, H., Bing, Z., Huang, K., Sun, F., Knoll, A.: Long-horizon language-conditioned imitation learning for robotic manipulation. IEEE/ASME Transactions on Mechatronics pp. 1–12 (2025) 

52. Yao, X., Zhou, H., Mees, O., Meng, Y., Xiao, T., Bisk, Y., Oh, J., Johns, E., Shridhar, M., Shah, D., et al.: Bridging language and action: A survey of languageconditioned robot manipulation. arXiv preprint arXiv:2312.10807 (2023) 

53. Yao, X., Zhou, Y., Meng, Y., Dong, L., Hong, L., Zhang, Z., Bing, Z., Huang, K., Sun, F., Knoll, A.: Pick-and-place manipulation across grippers without retraining: A learning-optimization diffusion policy approach. arXiv preprint arXiv:2502.15613 (2025) 

54. Yao, X., Zhou, Y., Meng, Y., Liu, Y., Dong, L., Zhang, Z., Bing, Z., Huang, K., Sun, F., Knoll, A.: Inference-stage adaptation-projection strategy adapts diffusion policy to cross-manipulators scenarios. arXiv preprint arXiv:2509.11621 (2025) 

55. Ye, S., Ge, Y., Zheng, K., Gao, S., Yu, S., Kurian, G., Indupuru, S., Tan, Y.L., Zhu, C., Xiang, J., et al.: World action models are zero-shot policies. arXiv preprint arXiv:2602.15922 (2026) 

56. Yu, T., Quillen, D., He, Z., Julian, R., Hausman, K., Finn, C., Levine, S.: Metaworld: A benchmark and evaluation for multi-task and meta reinforcement learning. In: Conference on robot learning. pp. 1094–1100. PMLR (2020) 

57. Ze, Y., Zhang, G., Zhang, K., Hu, C., Wang, M., Xu, H.: 3d diffusion policy: Generalizable visuomotor policy learning via simple 3d representations. In: Proceedings of Robotics: Science and Systems (RSS) (2024) 

58. Zhang, Q., Liu, Z., Fan, H., Liu, G., Zeng, B., Liu, S.: Flowpolicy: Enabling fast and robust 3d flow-based policy via consistency flow matching for robot manipulation. 

Dream Diffusion Policy 19 

In: Proceedings of the AAAI Conference on Artificial Intelligence. vol. 39, pp. 14754–14762 (2025) 

59. Zhang, X., Chang, M., Kumar, P., Gupta, S.: Diffusion meets dagger: Supercharging eye-in-hand imitation learning. arXiv preprint arXiv:2402.17768 (2024) 

60. Zhou, H., Bing, Z., Yao, X., Su, X., Yang, C., Huang, K., Knoll, A.: Languageconditioned imitation learning with base skill priors under unstructured data. IEEE Robotics and Automation Letters **9** (11), 9805–9812 (2024) 

61. Zhu, Y., Joshi, A., Stone, P., Zhu, Y.: Viola: Imitation learning for vision-based manipulation with object proposal priors. In: Conference on Robot Learning. pp. 1199–1210. PMLR (2023) 

## **Appendix** 

### **A Pseudocode for Closed-Loop Inference** 

To further clarify the transition between physical reality (In-Distribution) and internal imagination (Out-of-Distribution), we provide the detailed pseudocode for the DDP inference stage in Algorithm 2. The algorithm highlights the real-time detection via latent discrepancy _DR−I_ , the recursive action generation during the OOD state, and the target-specific recovery mechanism triggered at the end of each subtask. 

### **B Details of Simulation OOD Experiments** 

In this section, we provide the exact details for the Out-of-Distribution (OOD) evaluation on the MetaWorld benchmark. We detail the mechanism for implementing object displacements, how the robot tracks these shifts in simulation, and the precise task-specific parameters (timing, displacement vectors, and target objects). 

**Oracle State Transitions and OOD Implementation** To explicitly isolate and highlight the predictive power of the World Model’s “imagination” capability, we simplify the simulation evaluation pipeline. Specifically, we intentionally bypass the automated _DR−I_ OOD detector and the heuristic recovery triggers described in the main text. Instead, we implement a controlled **Oracle Tracking and State Transition Mechanism** via direct MuJoCo backend manipulations. By hard-coding the exact timing of both the OOD anomaly injection and the physical recovery to specific action chunks, we ensure that the evaluation purely reflects the policy’s ability to execute manipulation actions via internal imagination, independent of external tracking accuracy or detection latency. 

During the pre-defined execution step (i.e., the specific “chunk” detailed in Tab. 3), the environment execution is temporarily paused, and a sudden spatial shift is injected. As illustrated in Fig. 9 for the remaining MetaWorld tasks, the implementation follows two main logic branches depending on the nature of the task: 

- 20 Ziou Hu, Xiangtong Yao et al. 


**Fig. 9: DDP execution on the MetaWorld benchmark (Remaining 8 tasks).** Sequences show the transition from the ID Base Policy (green) to OOD tracking (yellow), bypassing visual shifts via the imagined Dream Policy (pink), and finally triggering physical recovery (green dotted) to complete the target. 

**1. Single-Stage Tracking (Target-Centric Tasks):** For tasks where the robot only needs to interact with the shifted object (e.g., _Button Press_ , _Drawer Open_ ), we simultaneously apply a coordinate translation vector _∆_ **P** = [ _dx, dy, dz_ ] to both the target object’s body position ( `sim.model.body_pos` ) and the robot’s end-effector mock-up position ( `data.mocap_pos` ). By directly hard-coding this offset to the `mocap` , the robot instantly re-aligns its physical hand with the newly displaced object, maintaining the relative spatial geometry required for the internal “imagined” execution. 

**2. Two-Stage Tracking and Recovery (Pick-and-Move Tasks):** For multisubtask challenges where an object is displaced but the final destination (goal) remains fixed (e.g., _Pick Place_ , _Push_ , _Sweep_ , _Coffee Pull_ ), the script executes a hard-coded two-stage intervention: 

- **Stage 1 (Track):** At the specified anomaly chunk, the object and the robot’s end-effector are shifted by _∆_ **P** so the robot can successfully grasp the displaced object. (Note: For _Pick Place_ , a “Safe Lift” logic is explicitly coded—lifting the arm 5cm, shifting it, and lowering it back—to prevent clipping through the table during teleportation). 

Dream Diffusion Policy 21 

- **Stage 2 (Recover and Policy Transition):** At a strictly pre-defined subsequent chunk (representing the moment the object is securely grasped), a reverse offset _−∆_ **P** is applied exclusively to the robot’s end-effector. This forces the robot to instantly “snap back” to the original ID area. Crucially, the Oracle then perfectly mimics the _DR−I_ re-evaluation logic defined in the main text to determine the subsequent policy mode: 

   - For _Pick Place_ , _Push_ , and _Sweep_ , bringing the grasped object back to the ID zone effectively restores global visual consistency. Consequently, the Oracle successfully re-anchors the environment and transitions the system back to the real visual stream ( **ID Base Policy** ). 

   - Conversely, for _Coffee Pull_ , the recovery step only snaps the arm and the grasped mug back to the ID target zone, while the large coffee machine is left permanently displaced. Because this leaves the global visual context strictly corrupted (which would naturally trigger _DR−I > τdiff_ in reality), the Oracle enforces that the system must continue executing purely via internal hallucination ( **OOD Dream Policy** ) to safely finish placing the mug. 

**Task-Specific OOD Parameters** The exact parameters for all 10 MetaWorld tasks are summarized in Tab. 3. The “Intervention Timing” refers to the specific action chunk index where the sudden displacement is injected. 

**Detailed Breakdown of Multi-Subtask Interventions:** 

- **Pick Place:** At chunk 2, the Puck is shifted by [ _−_ 0 _._ 2 _, −_ 0 _._ 1 _,_ 0]. The robot performs a collision-free tracking maneuver. At chunk 6, the robot arm snaps back by [+0 _._ 2 _,_ +0 _._ 1 _,_ 0] to place the puck into the fixed goal, _successfully recovering visual consistency and resuming the ID Base Policy_ . 

- **Push:** At chunk 2, the Puck is shifted by [ _−_ 0 _._ 25 _,_ 0 _,_ 0]. The robot tracks it. At chunk 6, the robot arm snaps back by [+0 _._ 25 _,_ 0 _,_ 0] to push the object toward the original fixed target, _resuming the ID Base Policy_ . 

- **Sweep:** At chunk 2, the Puck is shifted by [+0 _._ 2 _,_ +0 _._ 1 _,_ 0]. The robot tracks it. At chunk 6, the robot arm snaps back by [ _−_ 0 _._ 2 _, −_ 0 _._ 1 _,_ 0] to sweep the object into the fixed hole, _resuming the ID Base Policy_ . 

- **Coffee Pull:** At chunk 2, both the Mug and the Coffee Machine are shifted by [ _−_ 0 _._ 2 _,_ 0 _,_ 0], but the target placement zone remains fixed. At chunk 8, the robot arm snaps back by [+0 _._ 2 _,_ 0 _,_ 0] to pull the mug into the correct target zone. _Since the machine remains displaced (OOD), the agent continues executing via the OOD Dream Policy to complete the task._ 

### **C Further Details of Real-World Experiments** 

In this section, we provide additional configuration details for our real-world deployment, including the control hyper-parameters, visual processing pipeline, and the exact camera setup. 

22 Ziou Hu, Xiangtong Yao et al. 


**Fig. 10: In-Distribution Scenarios.** Real-world execution sequences demonstrating successful nominal manipulation for the _Stack Blocks_ , _Pour Tea_ , and _Press Button_ tasks. 

**Network Inference and Control Frequency** To achieve responsive real-time control, we accelerate the reverse diffusion process during inference by employing a fast-sampling scheduler (DDIM), reducing the denoising steps to _K_ = 10 for both the Diffusion Policy and the Diffusion World Model. Despite this acceleration, running the dual-diffusion pipeline alongside high-fidelity 3D visual encoding, real-time 6D object tracking, and continuous OOD anomaly detection ( _DR−I_ ) is computationally intensive. Consequently, our overall system control frequency naturally bounds to 2 Hz. Notably, this rate identically matches the frequency of our human teleoperation data collection, naturally aligning the model’s temporal execution with the expert demonstrations. 

We intentionally accept this inference speed to prioritize the synchronous and stable execution of all heavy subsystems. This design choice directly aligns with our primary research objective: achieving reliable, highly accurate recovery from severe OOD disturbances, rather than optimizing for high-speed dynamic manipulation. Because our evaluated tasks (e.g., _Stack Blocks_ , _Pour Tea_ ) demand precise spatial reasoning and alignment rather than split-second reactive motions, the 2 Hz frequency proves entirely sufficient. Furthermore, the inherent temporal smoothing provided by our action chunking mechanism ( _N_ = 8 executed steps per cycle) perfectly bridges the gap between consecutive network queries, yielding smooth, robust, and physically stable closed-loop execution. 

**Visual Processing and Point Cloud Downsampling** The primary visual observation is captured via a static Intel RealSense L515 camera. To achieve the required real-time processing speed, we implement a highly efficient two-stage point cloud downsampling pipeline: 

Dream Diffusion Policy 23 


**Fig. 11: Failure modes of the DP3 tracking ablation.** Real-world execution sequences demonstrating how the baseline policy fails under severe Out-of-Distribution (OOD) spatial shifts, resulting in missing grasps, dropping objects, and imprecise pressing (pressing the box after pressing the button). 

1. **Random Cropping:** The raw depth camera captures approximately 240 _,_ 000 points per frame. We first apply a random sub-sampling filter to drastically reduce this dense cloud to a manageable intermediate size of 10 _,_ 000 points. 

2. **Farthest Point Sampling (FPS):** We then apply FPS (accelerated via PyTorch3D) to extract a structurally uniform and geographically representative final set of exactly 2 _,_ 048 points. 

This optimized two-stage pipeline executes in just _∼_ 15 ms on the GPU, successfully feeding high-quality geometric features into the 3D encoder without introducing bottleneck latency. 

24 Ziou Hu, Xiangtong Yao et al. 

**Algorithm 2:** DDP Inference with Target-Specific Recovery **Input:** Visual Encoder _Eψ_ , Policy _πθ_ , World Model _Wϕ_ , Pose Estimator **Input:** Subtasks _S_ = _{S_ 1 _, . . . , SJ }_ , Expected ID poses **p**<sup>_exp_</sup> , Threshold _τdiff_ **1** OOD_Mode _←_ False _, Cdisp ←∅,_ **O** _curr ← Eψ_ ( _Xreal_<sup>0);</sup> **2 for** _subtask Sj ∈S targeting object Cj_ **do 3 while** _completion trigger Tend_ ( _Sj_ ) _is_ **_False_ do 4 O**<sup>_t_</sup> _real_<sup>_←Eψ_(</sup><sup>_X_</sup> _real_<sup>_t_);</sup> `// 1. OOD Detection & Tracking` **5 if** **_not_** _OOD_Mode_ **then 6 O**<sup>_t_</sup> _pred_<sup>_←Wϕ_(</sup><sup>**O**</sup> _real_<sup>_t−_1</sup><sup>_,_</sup><sup>**a**</sup><sup>_t−_1);</sup> **7** _DR−I_ ( _t_ ) _←∥_ **O** _real_<sup>_t−_</sup><sup>**O**</sup><sup>_t_</sup> _pred_<sup>_∥_</sup> 2<sup>2;</sup> **8 if** _DR−I_ ( _t_ ) _> τdiff_ **then 9** OOD_Mode _←_ True _, Cdisp ←_ Identify displaced objects; **10 if** _Cj ∈Cdisp_ **then 11** Execute tracking action **a**<sup>_track_</sup> _j_ = **p** _Cj −_ **p**<sup>_exp_</sup> _Cj_<sup>;</sup> **12 O** _curr ←_ **O**<sup>_t_</sup> _pred_<sup>;</sup> `// Enter Imagination` **13 else 14 O** _curr ←_ **O**<sup>_t_</sup> _real_<sup>;</sup> `// Nominal ID Reality // 2. Action Execution & Recursive Imagination` **15 a** _t ∼ πθ_ ( _· |_ **O** _curr_ ) _,_ Execute action chunk **a** _t_ ; **16 if** _OOD_Mode_ **then 17 O** _curr ←Wϕ_ ( **O** _curr,_ **a** _t_ ) ; `// Autoregressive Forecast` **18** _t ← t_ + 1; `// 3. Target-Specific Recovery` **19 if** _OOD_Mode_ **_and_** _Cj ∈Cdisp_ **then 20** Execute recovery action **a**<sup>_rec_</sup> _j_ = **p** _Cj −_ **p**<sup>_exp_</sup> _Cj_<sup>;</sup> **21** _Cdisp ←Cdisp \ {Cj}_ ; `// Re-evaluate ID State` **22** _DR−I_ ( _t_ ) _←∥Eψ_ ( _Xreal_<sup>_t_)</sup><sup>_−Wϕ_(</sup><sup>**O**</sup><sup>_curr,_</sup><sup>**a**</sup><sup>_t−_1)</sup><sup>_∥_</sup> 2<sup>2;</sup> **23 if** _DR−I_ ( _t_ ) _≤ τdiff_ **then 24** OOD_Mode _←_ False ; `// Return to Reality` 

**Table 3: Detailed OOD Disturbance Parameters for MetaWorld Tasks.** The displacement vector _∆_ **P** is represented as [ _dx, dy, dz_ ] in meters. 

|**Task Name **|**Displaced Object(s)**|**Intervention Timi**|**ng Displacement Vector (**_∆_**P)**|**Tracking Logic**|
|---|---|---|---|---|
|Assembly|Peg (`peg`)|Chunk 6|[_−_0_._25_,_0_._0_,_0_._0]|Single-Stage|
|Button Press|Box & Button (`box`)|Chunk 3|[_−_0_._25_,_0_._0_,_0_._0]|Single-Stage|
|Drawer Open|Drawer (`drawer`)|Chunk 2|[0_._0_,_0_._0_,_+0_._10]|Single-Stage|
|Hammer|Box & Nail (`box`, `nailHead`)|Chunk 5|[0_._0_,_+0_._10_,_0_._0]|Single-Stage|
|Door Unlock|Door (`door`)|Chunk 2|[0_._0_,_+0_._10_,_0_._0]|Single-Stage|
|Soccer|Goal Net (`goal_whole`)|Chunk 2|[_−_0_._20_,_+0_._10_,_0_._0]|Single-Stage|
|Pick Place|Puck (`obj`)|Chunk 2|[_−_0_._20_, −_0_._10_,_0_._0]|Two-Stage (+ Safe Lift)|
|Push|Puck (`obj`)|Chunk 2|[_−_0_._25_,_0_._0_,_0_._0]|Two-Stage|
|Sweep|Puck (`obj`)|Chunk 2|[+0_._20_,_+0_._10_,_0_._0]|Two-Stage|
|Coffee Pull|Mug & Machine (`obj`, `coffee_machine`)|Chunk 2|[_−_0_._20_,_0_._0_,_0_._0]|Two-Stage|


