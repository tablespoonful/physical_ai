---
title: "PhysMoDPO: Physically-Plausible Humanoid Motion with Preference Optimization"
date: "2026-03-13"
authors: "Yangsong Zhang; Anujith Muraleedharan; Rikhat Akizhanov; Abdul Ahad Butt; Gül Varol; Pascal Fua"
url: https://arxiv.org/abs/2603.13228
pdf: https://arxiv.org/pdf/2603.13228
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.13228)** / [論文ページ](https://arxiv.org/abs/2603.13228)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**1** 

# **PhysMoDPO: Physically-Plausible Humanoid Motion with Preference Optimization** 

Yangsong Zhang<sup>1</sup> , Anujith Muraleedharan<sup>1</sup> , Rikhat Akizhanov<sup>1</sup> , Abdul Ahad Butt<sup>1</sup> , Gül Varol<sup>2</sup> , Pascal Fua<sup>3</sup> , Fabio Pizzati<sup>1</sup> , and Ivan Laptev<sup>1</sup> 

- 1 Mohamed Bin Zayed University of Artificial Intelligence (MBZUAI) 

   - 2 LIGM, École des Ponts, IP Paris, Univ Gustave Eiffel, CNRS 

      - 3 École polytechnique fédérale de Lausanne (EPFL) 

```
https://mael-zys.github.io/PhysMoDPO/
```

**Abstract.** Recent progress in text-conditioned human motion generation has been largely driven by diffusion models trained on large-scale human motion data. Building on this progress, recent methods attempt to transfer such models for character animation and real robot control by applying a Whole-Body Controller (WBC) that converts diffusion-generated motions into executable trajectories. While WBC trajectories become compliant with physics, they may expose substantial deviations from original motion. To address this issue, we here propose PhysMoDPO, a Direct Preference Optimization framework. Unlike prior work that relies on hand-crafted physics-aware heuristics such as foot-sliding penalties, we integrate WBC into our training pipeline and optimize diffusion model such that the output of WBC becomes compliant both with physics and original text instructions. To train PhysMoDPO we deploy physics-based and task-specific rewards and use them to assign preference to synthesized trajectories. Our extensive experiments on text-to-motion and spatial control tasks demonstrate consistent improvements of PhysMoDPO in both physical realism and task-related metrics on simulated robots. Moreover, we demonstrate that PhysMoDPO results in significant improvements when applied to zero-shot motion transfer in simulation and for real-world deployment on a G1 humanoid robot. 

**Keywords:** Human motion synthesis · Post-training · Embodied AI · Robotics 

## **Introduction** 

The progress of diffusion models has largely advanced the text driven motion generation. Given an input condition ( _e.g_ ., a text description or additional spatial constraints), a model synthesizes a human motion sequence, enabling applications for animation, virtual avatars, and gaming [5, 44, 50, 52]. Among these applications, embodied downstream tasks, especially humanoid robotics, are particularly compelling: if a generative model could reliably produce physically consistent, controllable motions, it could provide a scalable source of reference behaviors for motion tracking and policy training. 

However, deploying generated motions in a physics-based setting exposes a key limitation of current generators. Diffusion models are typically trained and evaluated 

2 Y. Zhang et al. 

#### **TEXT INPUT** 

A PERSON WHO IS STANDING WITH HIS HANDS BY HIS SIDESSTEPS FORWARD WITH HIS RIGHT FOOT, KICKS OUT WITH HIS LEFT FOOT AND THEN STEPS BACK TO HIS ORIGINAL POSITION. 


**Fig. 1: PhysMoDPO generates motions that follow textual instructions while respecting physical constraints.** Compared to prior methods, our approach produces motions that remain stable and physically realistic when deployed on the Unitree G1 robot. 

in a kinematic space, where performance is judged by distributional similarity and alignment with the condition signal. In contrast, robotics requires motions that remain feasible under dynamics and contacts: feet should not skate, the center of mass must stay supported. In practice, when a generated motion is executed via a Whole-Body Controller (WBC) in simulation, a standard strategy in humanoid control [21, 29, 30], the controller may significantly alter the implausible motion to satisfy constraints. This introduces a discrepancy between what the generator produces and what is actually realized in the simulation. As a result, a model that performs well under kinematic metrics may still be unreliable for embodied deployment. 

To allow plausible human motion for deployment in real robotics embodiments, current efforts toward physically plausible motion modeling follow two main directions. One line injects physics priors through test-time hand-crafted losses or auxiliary refinement modules [20, 38, 56, 57]. While effective in specific cases, such approaches can shift the output distribution to adapt physics constraints and thus may largely harm the task-specific performance. Another line optimizes generators with heuristics rewards via reinforcement learning [7, 48]. Although promising and visually plausible, the performance highly depends on the heuristics functions, _i.e_ ., floating, and sliding, which makes it difficult to measure complex physical dynamics. Therefore, directly scaling hand-crafted rewards to the complicated real-world scenario is non-trivial. 

In this work, we propose PhysMoDPO, a physics-guided post-training framework for diffusion-based motion generators. Specifically, we integrate WBC into our training pipeline to measure how close the motion is to transfer to executable trajectory. In this way, the reward could directly cover the physical aspects such as dynamics, floating and jittering. As for our finetuning framework, inspired by DPO [37] alignment in image and video generation [22,46], we automatically construct preference data through pretrained WBC. Concretely, for each condition, we exploit stochastic sampling to generate multiple candidate motions, execute each candidate through the WBC, 

PhysMoDPO 3 

DeepMimic [29], to obtain simulated motions, and then compute (i) physics-based rewards that reflect trackability and contact realism for robots, and (ii) task-specific rewards that measure whether the tracked motion still matches the input condition. Importantly, computing task rewards after tracking directly targets the evaluation mismatch: we optimize the generator for motions that remain both physically feasible and condition-faithful. 

Extensive experiments on text-to-motion and spatial control tasks show that PhysMoDPO consistently improves physical realism while preserving and often improving task-related metrics on simulated robots. Moreover, we retarget and deploy the generated motions to real robots in a zero-shot way, i.e., without additional motion refinement. We demonstrate the zero-shot generalization to simulation and real-world deployment on Unitree G1, suggesting that post-training a generator with physicsguided preferences can produce motions that transfer beyond kinematic benchmarks. 

_Contributions._ In summary, our contributions are three-fold: (1) We propose PhysMoDPO, an automatic generate–finetune pipeline that leverages a pretrained WBC to post-train diffusion motion generators toward robotics-oriented physical consistency. (2) We design physics-based rewards that measure trackability and contact realism, together with task-specific rewards that evaluate condition fidelity after tracking policy, enabling preference supervision aligned with embodied deployment. (3) We conduct extensive experiments on text-to-motion and spatial control, demonstrating improved physical realism and task-related metrics in simulation, and showing zero-shot transfer to Unitree G1 in both simulation and real-world deployment. 

## **2 Related Works** 

**Controllable human motion generation.** Human motion generation has been studied under various conditioning signals, including action labels [31], speech audio [16,59], music [13,45], text descriptions [5,32,44,55]. More recently, in the domain of text-to-motion generation, research has shifted towards more fine-grained controllable motion synthesis, exploring temporal or spatial composition [2, 3, 34], streaming generation [50], integrating scene context [47,58], or object [14,15] into the generation framework and detailed spatial joint control [4,12,35,52]. Despite this progress, generated motions often fail to execute in physics-based simulators, exhibiting artifacts such as the center of mass that lies outside the body support. To address this gap, we integrate a pre-trained physics-based method to compute physics-based rewards as part of learning signals for DPO [37] fine-tuning, thereby improving the physical plausibility. **Physically plausible human motion modeling.** As shown in Table 1, one direction in physically plausible motion modeling is to apply hand-craft optimization [20,38] or additional models [43, 56, 57] to project the predicted noisy human motions. Previous works [20, 38] typically apply optimization through the Euler-Lagrange equations. PhysPT [57] further proposes a physics-aware transformer through self-supervised learning with Euler-Lagrange equations. Recent works [19, 54, 56] further use physicsbased methods to refine motion to avoid floating and sliding problems. However, simply applying physics-based methods may possibly change the output motion 

4 Y. Zhang et al. 

**Table 1: Comparison with previous work.** We compare alternative ways of incorporating physics constraints into human motion generation. In contrast to other methods, PhysMoDPO make use of dynamics-aware reward and does not require test-time optimization nor additional trainable modules. 

|Category|Method|Approach|Applied<br>at|No test-time<br>opt.|No Extra trainable<br>module|Dynamics-aware<br>reward|
|---|---|---|---|---|---|---|
|_Constraints_<br>_/ Projection_|Li et al. [20]<br>Rempe et al. [38]<br>PhysPT [57]<br>Zhang et al. [56]<br>PhysDiff [54]|Optimization<br>Optimization<br>Projection<br>Projection<br>Projection|Train/Infer<br>Train/Infer<br>Train<br>Infer<br>Sampling|✗<br>✗<br>✓<br>✗<br>✓|✓<br>✓<br>✗<br>✓<br>✓|–<br>–<br>–<br>–<br>–|
||ReinDiffuse [7]|Finetuning|Finetune|✓|✓|✗|
|_Rewards_|HY-Motion 1.0 [48]|Finetuning|Finetune|✓|✓|✗|
|_/ Finetune_|Morph [19]<br>PhysMoDPO|Data refinement<br>Finetuning|Data<br>Finetune|✓<br>✓|✗<br>✓|–<br>✓|


distribution, which may require test-time finetuning. Another branch of work directly refines motion generators with extra physics-based rewards [7, 48] or models [19]. ReinDiffuse [7] and HY-Motion 1.0 [48] define some hand-crafted rewards such as floating and sliding, and then apply PPO [40] and GRPO [41] to refine the motion generators, respectively. Though effective, those hand-crafted rewards can hardly cover other essential aspects such as abnormal mass center. To address this, Morph [19] trains a physics-based model to refine the generated motion and finetunes the motion generator with the refined data. However, when the motion from generators is too noisy, this training strategy could possibly harm the physics-based model. In this work, we use a pre-trained physics-based model to solely compute the physics rewards and then apply DPO [37] finetuning on the motion generator. 

**Physics-based character and robot control.** Physics-based policies have been widely explored in character animation and humanoid robot control. Most existing work [1,8,10,26,29,30] focuses on whole body control (WBC) which is conditioned on the full body target pose and predicts the corresponding plausible action for SMPL [23] character or humanoid robots through imitation and reinforcement learning. Some works [9,11,21,25,42] further explore versatile humanoid control via policy distillation such as DAgger [39] to distill a WBC teacher policy to enable partial observation input control. Recent works further extend it to high-level inputs such as text [9,42,49] and vision [53]. One idea is also to perform DAgger [39] to learn an end-to-end text control policy [42,49], the other is to leverage a text-driven motion generator to provide target poses [9,17,43,51] or latent action [18,27], and then perform motion tracking. However, current end-to-end text control policies such as MaskedMimic [42] can hardly achieve satisfying text-motion consistency. Unlike existing work [49, 51] which leverages short action phrases from BABEL [36] dataset, we focus on natural language descriptions from HumanML3D [6]. Additionally, simply applying motion tracking on noisy motion from the motion generators could fail, existing work [9,21] mainly focuses on improving the robustness of whole body controller, while we focus on finetuning generators. 

PhysMoDPO 5 


**Fig. 2: Overview of PhysMoDPO.** Given a conditioning signal (text and optional joint controls), we sample multiple motions _X_ from a pretrained generator. A fixed physics-based tracking policy then projects each sample into a simulated trajectory _X_<sup>_′_</sup> . We compute physics rewards and task rewards on _X_<sup>_′_</sup> , construct preference pairs, and finetune the generator with DPO. This generation–finetuning procedure can be iterated. 

## **3 Method** 

Here, we present PhysMoDPO. Our core idea is to post-train a motion diffusion model with a physics-grounded reward signal. As shown in Figure 2, for each motion generated with a diffusion model, a fixed tracking policy (whole body controller) produces a simulated trajectory. For each trajectory we then compute physics and task-specific rewards and use them to construct preference pairs for DPO [37] finetuning. Below we provide details of our method and first highlight the need of custom strategies for deployment-oriented motion generation in Section 3.1. In Section 3.2, we formulate the training objectives and describe our post-training procedure based on reinforcement learning. We describe our rewards strategy in Section 3.3. 

### **3.1 Physically-plausible transfer of generated motion** 

We denote a conditional motion diffusion generator as _Gθ_ . Let _X_ kin _⊆_ R<sup>_N×D_</sup> denote the space of kinematic motion sequences in our pose representation, and let _C_ denote the space of conditioning signals. The generator maps Gaussian noise and a condition to a kinematic motion sample: 


where _E_ is the noise space and _C_ the condition space. We consider two conditioning regimes: (i) text-to-motion, where _C_ = _Ct_ is a text prompt, and (ii) spatially-controlled text-to-motion, where _C_ = ( _Ct,Cs_ ) and _Cs_ specifies sparse target trajectories for selected joints. Diffusion training makes _Gθ_ an approximation of the data-generating process for kinematic motions, i.e., samples _X ∈X_ kin produced by _Gθ_ ( _ϵ,C_ ) match 

6 Y. Zhang et al. 

the kinematic motion statistics observed in the dataset. However, this kinematic space does not explicitly enforce physical constraints such as contact consistency, balance, frictional interactions, or actuation limits. We therefore distinguish physically realizable motions under a given embodiment and physics simulator as a subset _X_ phys _⊂X_ kin. Importantly, generating a plausible kinematic motion _X ∈X_ kin does not imply _X ∈X_ phys: a motion can look realistic and satisfy _C_ in pose space, yet become non-executable once contacts and dynamics are enforced. To make the transfer explicit, we introduce a physics operator _T_ implemented by a fixed tracking controller in a physics simulator, formalized as a mapping between the two spaces: 


We interpret _T_ as the deployment step: it produces an executable trajectory _X_<sup>_′_</sup> by enforcing dynamics and contact feasibility, but it may modify the reference motion _X_ to satisfy these constraints. See The magnitude of the required physics-induced correction is measured by the tracking distortion 


Intuitively, if _X_ is already close to _X_ phys, then _T_ makes only minor adjustments and _∆_ ( _X_ ) is small; conversely, kinematically plausible but physically inconsistent samples require larger corrections. As a consequence, we argue that for diffusion-based motion generation targeting deployment _it is crucial to move the evaluation target from the kinematic space to deployed space_ . In other words, instead of judging a generator by the immediate sample _X_ , we judge it by the realized trajectory _X_<sup>_′_</sup> = _T_ ( _X_ ) produced by a fixed physics tracker, and we report all quality and adherence metrics on _X_<sup>_′_</sup> . This directly captures the transfer failure mode we identify: high-quality kinematic samples can become poor deployed motions when realization induces large corrections, whereas physically compatible samples remain faithful after tracking. 

**Motion setup.** We represent motions in an SMPL-based format to avoid expensive test-time inverse kinematics required by the commonly used HumanML3D representation. Concretely, we adopt SMPL joint rotations and corresponding kinematic features following recent practice. For models originally trained in HumanML3D format, we retrain them using the SMPL-based representation for a consistent comparison. Unless otherwise specified, _T_ is instantiated using a fixed pretrained DeepMimic [29] tracker. 

### **3.2 Physics-aware post-training** 

Now, our objective is to finetune _G_ to generate kinematic motions that transfer well to simulation after applying _T_ . Since differentiating through _T_ is challenging, we treat it as a black box and use preference-based post-training. We adopt Direct Preference Optimization (DPO) as our post-training framework. For each condition _C_ , we exploit the stochasticity of the diffusion generator to sample _K_ candidate kinematic motions, realize each candidate in simulation, and score the realized motion with a physics-aware reward _R_ , described in the next section: 


PhysMoDPO 7 

We then select a preference pair ( _X_ win _,X_ lose) by selecting samples from the _K_ candidates and imposing that _X_ win achieves a better _R_ than _X_ lose. This writes: 


Importantly, rewards are computed on the realized motions _Xk_<sup>_′_=</sup><sup>_T_(</sup><sup>_Xk_),butthe</sup> preference pair is defined over the corresponding kinematic samples ( _X_ win _,X_ lose), which are the objects used for training. This respects the original DPO formulation, that exploits data directly sampled from the model [37]. We optimize the generator using the standard DPO objective from the original paper [46], which we denote by _L_ DPO( _X_ win _,X_ lose). Intuitively, this loss teaches the model to sample motions like _X_ win more often and motions like _X_ lose less often under the same condition _C_ . In practice, preference-only optimization may drift and harm sample quality, so we add a supervised fine-tuning term on the winning samples only, denoted _L_ SFT( _X_ win), to preserve generative capabilities. Overall, our post-training objective is 


where _λ_ SFT balances preference learning and stabilization. Finally, we apply DPO iteratively: after updating the generator, we resample new candidates and reconstruct preference pairs using the improved model, progressively refreshing the preference data toward the model’s current transfer failure modes under _T_ . 

### **3.3 Rewards and pair construction** 

We now describe the reward used in Eq.(4). Specifically, we combine different rewards to achieve best performance. First, we use two _physics rewards_ to encourage motions that transfer with minimal correction and stable contacts. Since strict physics following may hurt realism and smoothness of generated motion, we define additional _task rewards_ to preserve conditioning and prevent degenerate solutions (e.g., static motion). We first define a tracking reward _R_ track, explicitly minimizing the difference between _X_ and _X_<sup>_′_</sup> : 


The second physics reward _R_ slide penalizes foot micro-sliding, which is typically introduced by transfer to _X_ phys. Let _h_ feet( _X_<sup>_′_</sup> _,i_ ) and _v_ feet<sup>_xy_(</sup><sup>_X′,i_) denote the foot height</sup> and horizontal foot speed at frame _i_ computed from the realized motion _X_<sup>_′_</sup> . We define 


which discourages unrealistic contact patterns where feet are near the ground but drift horizontally. For task rewards, we first identify the need to preserve text alignment. We 

8 Y. Zhang et al. 

use TMR [33] and define explicitly a metric on text adherence, minimizing the cosine difference of the encoded motion and textual description in a shared latent space: 


TMRtext and TMRmot refer to the textual and motion encoder of TMR, respectively. When _C_ includes sparse spatial targets _Cs_ , we additionally reward matching those targets within _X_<sup>_′_</sup> . We define this reward _R_ control _as_ : 


Here, _W_ refers to a joint mask indicating only the control joints available. We combine rewards through a dominance rule when constructing preferences. We define _S_ ( _C_ )= _{R_ track _,R_ slide _,R_ M2T _}_ as the set including rewards conditions for text-to-motion, and _S_ ( _C_ )= _{R_ track _,R_ slide _,R_ M2T _,R_ control _}_ when spatial control is provided. We define the composite preference _R_ ( _X_<sup>_′_</sup> _,C_ ) implicitly by declaring that a realized motion _Xk_<sup>_′_is</sup> preferred to _Xl_<sup>_′_under thesamecondition</sup><sup>_C_if itimproves</sup><sup>_every_reward term:</sup> 


This keeps the preference signal consistent across physics and task objectives without introducing sensitive reward weights. 

## **4 Experiments** 

### **4.1 Experimental setup** 

**Datasets.** We generate DPO preference pairs based on text from HumanML3D [6] dataset and then evaluate on the corresponding test set. For spatial control task, we further extract spatial control signals to generate samples and calculate _R_ control. To further evaluate the generalization ability of our proposed PhysMoDPO strategy, we evaluate on the OMOMO [15] dataset. OMOMO mainly focuses on human-object interaction, hence the text distribution is different. We use it as out-of-distribution test. As mentioned in Section 3.1, all the motion data are trained in SMPL-based representation to enable easier adaptation for downstream tasks. Moreover, we filter out motions which require object supports (such as "go upstairs"), as we add physics property in the simulator, and the robot cannot track those motions without the corresponding object. **Evaluation metrics.** Different from existing work, as we explain in Sec. 3.1 we evaluate all the model after the whole-body tracking model [29] within simulation to better measure whether the output motion of generators is plausible and whether the character in simulation follows the input condition _C_ . The evaluation protocols are mainly adopted from MotionStreamer [50] and OmniControl [52]. The text-motion consistency is evaluated by the Multi-Modal Distance (MM-Dist) and the top-k retrieved accuracy (R@1, R@2, R@3). Frechet Inception Distance (FID) is calculated to quantify the distribution distance between ground truth and the generated motion 

PhysMoDPO 9 

**Table 2: Evaluation of text-driven human motion generation with SMPL robot simulation on HumanML3D [6] dataset.** We evaluate MaskedMimic [42], MotionStreamer [50] and PhysMoDPO with text-conditioned generation setting as in MotionStreamer [50]. The best results are in bold, and the second best results are underlined. 

|**Method**|**MM-Dist**|_↓_**R@1** _↑_|**R@2** _↑_|**R@3** _↑_<br>**FID** _↓_|**Jerk** _↓_|
|---|---|---|---|---|---|
|Real after simulation|16.02|0.6682|0.8326|0.8952<br>34.07|35.87|
|MaskedMimic [42]|19.73|0.4134|0.5568|0.6305<br>73.79|66.08|
|MotionStreamer [50]|17_._17|0_._5829|0.7510|0.8310<br>49_._14|46_._75|
|SFT|17.23|0.5779|0_._7651|0_._8355<br>49.22|48.30|
|PhysMoDPO|**16**_._**95**|**0**_._**5853 **|**0**_._**7726 **|**0**_._**8517**<br>**48**_._**29 **|**43**_._**60**|


**Table 3: Evaluation of spatial-text human motion controllability with SMPL character control.** Left: HumanML3D [6]. Right: OMOMO [15]. We evaluate MaskedMimic [42], OmniControl [52] under two training settings and PhysMoDPO with cross-control setting as in OmniControl [52]. The best results are in bold, and the second best results are underlined. 

|||**_Huma_**|**_nML3D_**||||**_OM_**|**_OMO_**|||
|---|---|---|---|---|---|---|---|---|---|---|
|**Method**|**Err.**_↓_|**MM-Dist**_↓_|**R@3**_↑_|**FID**_↓_|**Jerk**_↓_|**Err.**_↓_|**MM-Dist**_↓_|**R@3**_↑_|**FID**_↓_|**Jerk**_↓_|
|Real after simulation|0.0536|3.150|0.7607|0.98|62.96|0.0485|6.679|0.1576|0.59|65.49|
|MaskedMimic [42]|0.2493|5.149|0.4932|3.99|106.49|0.2140|**6**_._**639**|0.1081|5.99|119.52|
|_nal_<br>OmniControl [52]|0.1998|4.238|0.6123|5.82|115.12|0.3989|7.267|0.1315|20.59|161.95|
|_rigi_<br>SFT|0.1536|3.580|0.6875|2.63|92.56|0.2866|7.218|0.1419|13.28|130.69|
|_O_<br>PhysMoDPO|0.1298|3.333|0.7168|0.93|62.31|0.1900|6.947|**0**_._**1536**|3.86|101.88|
|_ss_<br>OmniControl [52]|0_._0938|3_._086|**0**_._**7584**|0.75|64.07|0.1389|6.840|0.1419|3.89|88.57|
|_ro_<br>SFT|0.0972|**3**_._**075**|0.7539|0_._68|61_._22|**0**_._**1319**|6.875|0.1484|2_._69|84_._55|
|_C_<br>PhysMoDPO|**0**_._**0923**|3.099|0_._7549|**0**_._**66 **|**58**_._**02**|0_._1339|6_._8245|0_._1497|**1**_._**50 **|**76**_._**49**|


inside the simulation. For spatial control task, we evaluate the controllability through masked MSE between _Cs_ and _X_<sup>_′_</sup> (Err.). The derivative of acceleration (Jerk) is computed to check the smoothness of _X_<sup>_′_</sup> . 

**Implementation details.** We initialize our pipeline with pretrained MotionStreamer [50] (for text-to-motion) and OmniControl [52] (for spatial-text control). For MotionStreamer [50], we generate 12 samples per training prompt on HumanML3D [6] and perform post-training by updating only the diffusion head, optimized with AdamW [24]. Following MotionStreamer [50], we use the Two-Forward objective as _L_ SFT on selected win samples. The SFT baseline sets the DPO weight to zero while keeping other settings unchanged. For spatial-text control, we follow OmniControl [52]’s cross-control evaluation and sample a random set of control joints during testing. As the original OmniControl [52] is trained with random one joint per sample, we further re-train it with random number of control joints (cross-control setting) and compare the performance. More details can be found in the appendix. 

10 Y. Zhang et al. 


**Fig. 3: Visual comparison with SMPL simulation.** On top, we compare MaskedMimic [42], MotionStreamer [50] and PhysMoDPO on text-to-motion generation task on HumanML3D [6] dataset. At the bottom, we show visual results of spatial-text control task on HumanML3D [6] (left) and OMOMO [15] (right) dataset. Red balls are the input spatial control signals and red boxes highlight the samples which do not follow the control or lose balance. 

### **4.2 Experiments on SMPL simulated character** 

**Text-to-motion results.** Table 2 reports text-conditioned motion generation performance on HumanML3D after simulation. We compare with MaskedMimic [42] as physics-based baseline, MotionStreamer [50] as our backbone, a naive fine-tuning variant (SFT on win samples), and our proposed method PhysMoDPO. Since MaskedMimic directly outputs executable actions in the simulator, hence we omit the projection with tracking policy. Despite being physically executable, MaskedMimic [42] exhibits poor text adherence, _e.g_ ., substantially worse retrieval scores (R@1/2/3) and higher FID, indicating limited text-motion consistency. MotionStreamer [50] already achieves strong text-motion alignment after projection, leaving limited room for straightforward supervised refinement. SFT on win samples yields only marginal gains in text-motion retrieval, while slightly degrading physical fidelity and smoothness. In contrast, PhysMoDPO consistently improves text-motion consistency and smoothness. Concretely, PhysMoDPO improves text-motion metrics R@3 from 0.8310 

PhysMoDPO 11 

**Table 4: Evaluation of text-driven human motion generation with G1 robot on HumanML3D [6] dataset.** We evaluate MaskedMimic [42], MotionStreamer [50] and PhysMoDPO with text-conditioned generation setting as in MotionStreamer [50]. The best results are in bold, and the second best results are underlined. 

|**Method**|**M2T** _↑_|**R@1** _↑_|**R@2** _↑_|**R@3** _↑_|**FID** _↓_|**Jerk** _↓_|
|---|---|---|---|---|---|---|
|Real after simulation|0.8282|0.5731|0.7583|0.8475|0.1201|87.76|
|MaskedMimic [42]|0.7156|0.3258|0.4762|0.5761|0.3673|**83**_._**58**|
|MotionStreamer [50]|0_._7904|0_._4673|**0**_._**6620**|0_._7558|0_._3033|95.08|
|SFT|0.7869|0.4586|0.6444|0.7430|0.3124|97.99|
|PhysMoDPO|**0**_._**7919**|**0**_._**4707**|0_._6596|**0**_._**7640**|**0**_._**3029**|90_._14|


to 0.8517 and lowers Jerk from 46.75 to 43.60. These results demonstrate that our framework effectively reduces the gap between text controllability and physical realism, outperforming both end-to-end physics-based generation and naive fine-tuning. **Spatial-text control results.** Tables 3 shows results under the cross-control evaluation protocol. On HumanML3D [6], PhysMoDPO consistently improves all aspects over OmniControl [52] trained on original training setting. PhysMoDPO better satisfies multi-joint spatial constraints and also strengthens text-motion consistency while producing higher-quality and smoother motions, as evidenced by a large drop in FID and Jerk. Although OmniControl [52] trained on cross setting achieves good performance, PhysMoDPO still improves the spatial controllability and FID. On the out-ofdistribution OMOMO [15] dataset, PhysMoDPO remains robust and delivers significant gains despite not using ground-truth motions as training labels. Specifically, PhysMoDPO greatly lowers controllability errors and the generated motions become noticeably more realistic and smoother (lower FID and Jerk). These results suggest that our strategy generalizes well and can effectively adapt the model under distribution shift. **Qualitative results.** As presented in Figure 3, we compare MaskedMimic [42], our finetuning baseline and PhysMoDPO for text driven motion generation and spatialtext motion generation tasks. From the figure, we can find that MaskedMimic [42] can hardly follow the text construction, _e.g_ ., in the bottom-left figure, the character does not even try to perform the handstand action. Even though MaskedMimic [42] is a physics-based policy trained within a simulation, it may still fall on high-speed motion. As the vanilla diffusion motion generators, _i.e_ . MotionStreamer [50] and OmniControl [52], could generate more implausible motions which cause the SMPL robot losing balance or directly falling down. With our proposed PhysMoDPO finetuning framework, we have higher probability to generate physical human motions which also follow the input condition. 

### **4.3 Zero-shot transfer to Unitree G1 robot** 

**G1 evaluation pipeline.** To show that the motion generated by PhysMoDPO could better generalize to real robot embodiment, we evaluate our method in a zero-shot manner on Unitree G1 by directly reusing the model trained on SMPL. Given an 

12 Y. Zhang et al. 

**Table 5: Evaluation of human motion controllability with G1 robot.** Left: HumanML3D [6]. Right: OMOMO [15]. We evaluate MaskedMimic [42], OmniControl [52] and PhysMoDPO with cross-control setting as in OmniControl [52]. The best results are in bold, and the second best results are underlined. 

||||**_Hu_**|**_manML_**|**_3D_**|||**_O_**|**_MOMO_**|||
|---|---|---|---|---|---|---|---|---|---|---|---|
||**Method**|**Err.**_↓_|**M2T**_↑_|**R@3**_↑_|**FID**_↓_|**Jerk**_↓_|**Err.**_↓_|**M2T**_↑_|**R@3**_↑_|**FID**_↓_|**Jerk**_↓_|
||Real after simulation|0.1894|0.7810|0.7241|0.1287|160|0.1730|0.4985|0.1111|0.1099|184|
||MaskedMimic [42]|0.3388|0.6470|0.3958|0.4626|162|0.3157|0.4635|0.0970|0.4324|198|
|_nal_|OmniControl [52]|0.5954|0.7025|0.5504|0.3655|315|0.5951|0.4773|0.1301|0.5007|459|
|_igi_|SFT|0.4606|0.7335|0.6108|0.3047|250|0.4857|0.4836|0.1304|0.4571|369|
|_Or_|PhysMoDPO|0.2918|0.7414|0.6335|0.3090|142|0.3499|0.5011|0.1291|0.3816|239|
|_ss_|OmniControl [52]|0.2372|0_._7830|0.7301|**0**_._**1972**|156|0.2687|0.5164|0.1403|0.3189|192|
|_ro_|SFT|0_._2338|**0**_._**7834**|0_._7336|0_._1980|155|0_._2545|0_._5328|0_._1503|**0**_._**3055**|174|
|_C_|PhysMoDPO|**0**_._**2240**|0.7820|**0**_._**7350**|0_._1980|**148**|**0**_._**2510**|**0**_._**5387**|**0**_._**1571**|0_._3065|**167**|


input condition, we first run SMPL motion generator to sample motions. Since G1 has different kinematics, we retarget each generated motion to the G1 skeleton before deployment. The retargeted motion is then executed by DeepMimic [29] pretrained on G1. As for text-motion metrics, although the generator is kept unchanged, the standard text-motion metrics depend on the motion representation. Therefore, we retarget AMASS motions from SMPL to G1 and retrain a G1-based TMR [33] evaluator using the same training protocol as the original TMR. This evaluator is only used at inference time for reporting FID and text-motion alignment metrics such as M2T score and top-k retrieval accuracy. For spatial control, retargeting may rescale the target joint trajectories due to embodiment differences. Thus, when measuring controllability on G1, we compare the simulated G1 motion against the retargeted ground-truth motion on the controlled joints, rather than directly using the original SMPL-space control signal, to avoid mismatched scales while preserving the intended spatial constraints. 

**Text-to-motion results.** As reported in Table 4, our SMPL-trained model generalizes to Unitree G1 without any additional training and achieves the strongest overall performance in simulation. The naive SFT trained on SMPL data performs worse than the baseline when zero-shot transferring to the G1 robot. In constrast, our consistent improvement based on MotionStreamer [50] proves the effectiveness of the proposed PhysMoDPO method. Similar to the SMPL character results with simulation, MaskedMimic [42] can hardly follow the text input, which results in the lowest text retrieval performance. 

**Spatial-text control results.** The comparison with MaskedMimic [42] and OmniControl [52] can be found in Table 5. Compared with the original OmniControl [52], PhysMoDPO produces motions that are noticeably smoother, while maintaining stronger consistency to the spatial control signals. Overall, the zero-shot results indicate that our post-training enhances both physical feasibility and control faithfulness, and these gains transfer well across embodiments. 

**Real robot deployment.** As the DeepMimic [29] focuses for on character animation, and can hardly be deployed on real robot, we train a whole body control policy for 

PhysMoDPO 

13 


**Fig. 4: Visual results on Unitree G1 robot.** Our deployed motion model enables the robot to move in a physically-realistic way while following input text instructions. 

G1 robot following BeyondMimic [21], and then we deploy the policy to execute the retargeted G1 motion from pipeline for real robot experiments. As shown in Figure 4, we deploy the motions generated by PhysMoDPO on Unitree G1 robot. The zero-shot examples prove the plausibility of our generated motions. 

**User study.** We conduct a user study to complement metrics. For each method, we present 40 paired real robot videos to participants together with the input text. Twenty participants are asked to select videos according to text adherence, motion smoothness and robot stability. As shown in Figure 5, PhysMoDPO consistently outperform OmniControl [52] and MaskedMimic [42] across all the criteria. The detailed design of user study can be found in the appendix. 

### **4.4 Ablation study** 

As summarized in Table 6, we conduct ablations on iterative training round and rewards setting. 

**Iterative training round.** We first study the effectiveness of the proposed multiround generation. As the number of iterative rounds increases from 1 to 3, we observe consistent improvements on all metrics: MPJPE drops from 0.0456 to 0.0368, controllability error decreases from 0.1421 to 0.1298, MM-Dist improves from 3.36 to 3.33, 

14 Y. Zhang et al. 


**Fig. 5: User study.** Comparison of real-robot motion sequences generated by PhysMoDPO, MaskedMimic [42] and OmniControl [52]. PhysMoDPO outperform both competitors in terms of text adherence, motion smoothness and overall stability. 

**Table 6: Ablation studies.** We train OmniControl [52] and study the impact of the number of iterative training round and different rewards on HumanML3D [6] dataset. The best results are in bold. 

|Number|**Err.** _↓_**M**|**M-Dist** _↓_|**FID** _↓_|**Jerk** _↓_|Rewards|**Err.** _↓_|**MM-Dist**|_↓_**FID** _↓_|**Jerk** _↓_|
|---|---|---|---|---|---|---|---|---|---|
|1<br>2<br>3|0.1421<br>0.1324<br>**0**_._**1298**|3.36<br>3.34<br>**3**_._**33**|1.17<br>0.97<br>**0**_._**93**|72.13<br>63.55<br>**62**_._**31**|Tracking<br>+ Control<br>+ Sliding<br>+ M2T|0.1467<br>0.1447<br>0.1422<br>**0**_._**1421**|3.43<br>3.41<br>3.40<br>**3**_._**36**|1.61<br>1.45<br>1.21<br>**1**_._**17**|74.76<br>74.47<br>**68**_._**43**<br>72.13|


**(a)** Number of iterative training round 

**(b)** Rewards 

while FID is significantly reduced from 1.17 to 0.93 and Jerk decreases from 72.13 to 62.31. These results validate that regenerating preference pairs with the newly improved model provides progressively better supervision, leading to better motion realism and stronger physical plausibility. 

**Rewards.** We ablate each reward component in the preference construction. Using only the tracking reward is suboptimal, as it tends to favor overly conservative motions, which makes the training diverge faster. Adding the controllability reward yields a modest gain across metrics, confirming that explicitly optimizing task-following helps preserve condition faithfulness. Introducing the sliding reward brings a clear improvement in both FID and Jerk, showing that penalizing foot skating effectively mitigates common contact artifacts. Finally, adding the M2T score further improves text-motion consistency and generation quality. We note that this last addition slightly increases Jerk, because emphasizing semantic correctness encourages more dynamic actions, which may introduce larger accelerations while still improving realism and alignment overall. 

## **5 Conclusion** 

In this paper, we proposed PhysMoDPO, a physics-guided post-training framework based on DPO to improve the plausibility of diffusion-based human motion generators. To bridge the gap between kinematic generation and physics-based execution, PhysMoDPO automatically constructs preference pairs through a pretrained physicsbased tracking policy with physics-oriented and task-specific rewards. We optimize the generator with a DPO objective and improve it further within an iterative 

PhysMoDPO 15 

generate–finetune loop. Experiments on text-to-motion and spatial control tasks demonstrate consistent gains of PhysMoDPO in physical realism and task metrics in simulation. Moreover, zero-shot transfer to Unitree G1 robot indicates the potential of PhysMoDPO for robotics-oriented motion generation. 

**Limitation and future work.** Despite encouraging results, PhysMoDPO has several limitations that suggest directions for future research. (1) Our current setup primarily considers locomotion on flat ground. Extensions of the method to more diverse terrains will further improve transfer to real-world robotics. (2) Our construction of preference pairs relies on a fixed simulation tracking policy, which can introduce biases. Future work could incorporate human-validated models to reduce evaluator bias. Overall, we believe our proposed PhysMoDPO will advance and inspire research in motion generation and embodied AI. 

## **Acknowledgements** 

This work was in part supported by the Institute of Information & communications Technology Planning & Evaluation (IITP) grant funded by the Korean government (MSIT) (No. RS-2024-00457882, National AI Research Lab Project), and by the ANR project CorVis (ANR-21-CE230003-01). 

## **References** 

1. Allshire, A., Choi, H., Zhang, J., McAllister, D., Zhang, A., Kim, C.M., Darrell, T., Abbeel, P., Malik, J., Kanazawa, A.: Visual imitation enables contextual humanoid control. arXiv (2025) 4 

2. Athanasiou, N., Petrovich, M., Black, M.J., Varol, G.: TEACH: Temporal Action Compositions for 3D Humans. In: International Conference on 3D Vision (3DV) (2022) 3 

3. Athanasiou, N., Petrovich, M., Black, M.J., Varol, G.: SINC: Spatial composition of 3D human motions for simultaneous action generation. In: ICCV (2023) 3 

4. Dai, W., Chen, L.H., Wang, J., Liu, J., Dai, B., Tang, Y.: MotionLCM: Real-time controllable motion generation via latent consistency model. In: ECCV (2024) 3 

5. Guo, C., Mu, Y., Javed, M.G., Wang, S., Cheng, L.: MoMask: Generative masked modeling of 3D human motions. In: CVPR (2024) 1, 3 

6. Guo, C., Zou, S., Zuo, X., Wang, S., Ji, W., Li, X., Cheng, L.: Generating diverse and natural 3D human motions from text. In: CVPR (2022) 4, 8, 9, 10, 11, 12, 14, 1, 3, 5 

7. Han, G., Liang, M., Tang, J., Cheng, Y., Liu, W., Huang, S.: Reindiffuse: Crafting physically plausible motions with reinforced diffusion model. In: WACV (2025) 2, 4 

8. He, T., Gao, J., Xiao, W., Zhang, Y., Wang, Z., Wang, J., Luo, Z., He, G., Sobanbab, N., Pan, C., et al.: Asap: Aligning simulation and real-world physics for learning agile humanoid whole-body skills. arXiv preprint arXiv:2502.01143 (2025) 4 

9. He, T., Luo, Z., He, X., Xiao, W., Zhang, C., Zhang, W., Kitani, K., Liu, C., Shi, G.: Omnih2o: Universal and dexterous human-to-humanoid whole-body teleoperation and learning. arXiv (2024) 4 

10. He, T., Luo, Z., Xiao, W., Zhang, C., Kitani, K., Liu, C., Shi, G.: Learning human-to-humanoid real-time whole-body teleoperation. In: IROS (2024) 4 

16 Y. Zhang et al. 

11. He, T., Xiao, W., Lin, T., Luo, Z., Xu, Z., Jiang, Z., Kautz, J., Liu, C., Shi, G., Wang, X., et al.: Hover: Versatile neural whole-body controller for humanoid robots. In: ICRA (2025) 4, 1, 2 

12. Karunratanakul, K., Preechakul, K., Suwajanakorn, S., Tang, S.: Guided motion diffusion for controllable human motion synthesis. In: ICCV (2023) 3 

13. Li, B., Zhao, Y., Zhelun, S., Sheng, L.: DanceFormer: Music conditioned 3D dance generation with parametric motion transformer. In: AAAI (2022) 3 

14. Li, J., Clegg, A., Mottaghi, R., Wu, J., Puig, X., Liu, C.K.: Controllable human-object interaction synthesis. arXiv (2023) 3 

15. Li, J., Wu, J., Liu, C.K.: Object motion guided human motion synthesis. ACM TOG (2023) 3, 8, 9, 10, 11, 12, 5 

16. Li, J., Kang, D., Pei, W., Zhe, X., Zhang, Y., He, Z., Bao, L.: Audio2Gestures: Generating diverse gestures from speech audio with conditional variational autoencoders. In: ICCV (2021) 3 

17. Li, P., Zhuang, Z., Gao, Y., Dong, Y., Li, S., Jiang, C., Dou, S., Xi, Z., Zhou, E., Huang, J., et al.: From-w1: Towards general humanoid whole-body control with language instructions. arXiv (2026) 4 

18. Li, Z., Chi, C., Wei, Y., Zhu, B., Peng, Y., Huang, T., Wang, P., Wang, Z., Zhang, S., Xu, C.: From language to locomotion: Retargeting-free humanoid control via motion latent guidance. arXiv (2025) 4 

19. Li, Z., Luo, M., Hou, R., Zhao, X., Liu, H., Chang, H., Liu, Z., Li, C.: Morph: A motionfree physics optimization framework for human motion generation. In: ICCV (2025) 3, 4 

20. Li, Z., Sedlar, J., Carpentier, J., Laptev, I., Mansard, N., Sivic, J.: Estimating 3d motion and forces of person-object interactions from monocular video. In: CVPR (2019) 2, 3, 4 

21. Liao, Q., Truong, T.E., Huang, X., Gao, Y., Tevet, G., Sreenath, K., Liu, C.K.: Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion. arXiv (2025) 2, 4, 13 

22. Liu, R., Wu, H., Zheng, Z., Wei, C., He, Y., Pi, R., Chen, Q.: Videodpo: Omni-preference alignment for video diffusion generation. In: CVPR (2025) 2 

23. Loper, M., Mahmood, N., Romero, J., Pons-Moll, G., Black, M.J.: SMPL: A skinned multi-person linear model. ACM TOG (2015) 4, 1 

24. Loshchilov, I., Hutter, F.: Decoupled weight decay regularization. arXiv (2017) 9, 4 

25. Luo, Z., Cao, J., Merel, J., Winkler, A., Huang, J., Kitani, K.M., Xu, W.: Universal humanoid motion representations for physics-based control. In: ICLR (2024) 4 

26. Luo, Z., Cao, J., Winkler, A.W., Kitani, K., Xu, W.: Perpetual humanoid control for real-time simulated avatars. In: ICCV (2023) 4 

27. Luo, Z., Yuan, Y., Wang, T., Li, C., Chen, S., Castaneda, F., Cao, Z.A., Li, J., Minor, D., Ben, Q., et al.: Sonic: Supersizing motion tracking for natural humanoid whole-body control. arXiv (2025) 4 

28. Mahmood, N., Ghorbani, N., Troje, N.F., Pons-Moll, G., Black, M.J.: AMASS: Archive of motion capture as surface shapes. In: ICCV (2019) 1 

29. Peng, X.B., Abbeel, P., Levine, S., Van de Panne, M.: Deepmimic: Example-guided deep reinforcement learning of physics-based character skills. ACM TOG (2018) 2, 3, 4, 6, 8, 12 

30. Peng, X.B., Ma, Z., Abbeel, P., Levine, S., Kanazawa, A.: Amp: Adversarial motion priors for stylized physics-based character control. ACM TOG (2021) 2, 4 

31. Petrovich, M., Black, M.J., Varol, G.: Action-conditioned 3D human motion synthesis with transformer VAE. In: ICCV (2021) 3 

32. Petrovich, M., Black, M.J., Varol, G.: TEMOS: Generating diverse human motions from textual descriptions. In: ECCV (2022) 3 

33. Petrovich, M., Black, M.J., Varol, G.: Tmr: Text-to-motion retrieval using contrastive 3d human motion synthesis. In: ICCV (2023) 8, 12 

PhysMoDPO 17 

34. Petrovich, M., Litany, O., Iqbal, U., Black, M.J., Varol, G., Peng, X.B., Rempe, D.: Multitrack timeline control for text-driven 3D human motion generation. CVPRW (2024) 3, 2 

35. Pinyoanuntapong, E., Saleem, M., Karunratanakul, K., Wang, P., Xue, H., Chen, C., Guo, C., Cao, J., Ren, J., Tulyakov, S.: Maskcontrol: Spatio-temporal control for masked motion synthesis. In: ICCV (2025) 3 

36. Punnakkal, A.R., Chandrasekaran, A., Athanasiou, N., Quiros-Ramirez, A., Black, M.J.: Babel: Bodies, action and behavior with english labels. In: CVPR (2021) 4 

37. Rafailov, R., Sharma, A., Mitchell, E., Manning, C.D., Ermon, S., Finn, C.: Direct preference optimization: Your language model is secretly a reward model. NeurIPS (2023) 2, 3, 4, 5, 7 

38. Rempe, D., Guibas, L.J., Hertzmann, A., Russell, B., Villegas, R., Yang, J.: Contact and human dynamics from monocular video. In: ECCV (2020) 2, 3, 4 

39. Ross, S., Gordon, G., Bagnell, D.: A reduction of imitation learning and structured prediction to no-regret online learning. In: AISTATS (2011) 4 

40. Schulman, J., Wolski, F., Dhariwal, P., Radford, A., Klimov, O.: Proximal policy optimization algorithms. arXiv (2017) 4 

41. Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Bi, X., Zhang, H., Zhang, M., Li, Y., Wu, Y., et al.: Deepseekmath: Pushing the limits of mathematical reasoning in open language models. arXiv (2024) 4 

42. Tessler, C., Guo, Y., Nabati, O., Chechik, G., Peng, X.B.: MaskedMimic: Unified physics-based character control through masked motion inpainting. ACM TOG (2024) 4, 9, 10, 11, 12, 13, 14, 1, 2 

43. Tevet, G., Raab, S., Cohan, S., Reda, D., Luo, Z., Peng, X.B., Bermano, A.H., van de Panne, M.: CLoSD: Closing the loop between simulation and diffusion for multi-task character control. arXiv (2024) 3, 4 

44. Tevet, G., Raab, S., Gordon, B., Shafir, Y., Bermano, A.H., Cohen-Or, D.: Human motion diffusion model. arXiv (2022) 1, 3 

45. Tseng, J., Castellon, R., Liu, K.: EDGE: Editable dance generation from music. In: CVPR (2023) 3 

46. Wallace, B., Dang, M., Rafailov, R., Zhou, L., Lou, A., Purushwalkam, S., Ermon, S., Xiong, C., Joty, S., Naik, N.: Diffusion model alignment using direct preference optimization. In: CVPR (2024) 2, 7, 4 

47. Wang, Z., Chen, Y., Liu, T., Zhu, Y., Liang, W., Huang, S.: HUMANISE: Language-conditioned human motion generation in 3D scenes. NeurIPS (2022) 3 

48. Wen, Y., Shuai, Q., Kang, D., Li, J., Wen, C., Qian, Y., Jiao, N., Chen, C., Chen, W., Wang, Y., et al.: Hy-motion 1.0: Scaling flow matching models for text-to-motion generation. arXiv (2025) 2, 4 

49. Wu, Y., Karunratanakul, K., Luo, Z., Tang, S.: Uniphys: Unified planner and controller with diffusion for flexible physics-based character control. In: ICCV (2025) 4 

50. Xiao, L., Lu, S., Pi, H., Fan, K., Pan, L., Zhou, Y., Feng, Z., Zhou, X., Peng, S., Wang, J.: Motionstreamer: Streaming motion generation via diffusion-based autoregressive model in causal latent space. In: ICCV (2025) 1, 3, 8, 9, 10, 11, 12, 4 

51. Xie, W., Zheng, J., Han, J., Shi, J., Zhang, W., Bai, C., Li, X.: Textop: Real-time interactive text-driven humanoid robot motion generation and control. arXiv (2026) 4 

52. Xie, Y., Jampani, V., Zhong, L., Sun, D., Jiang, H.: OmniControl: Control any joint at any time for human motion generation. arXiv (2023) 1, 3, 8, 9, 11, 12, 13, 14, 2, 4, 5 

53. Yin, S., Ze, Y., Yu, H.X., Liu, C.K., Wu, J.: Visualmimic: Visual humanoid loco-manipulation via motion tracking and generation. arXiv (2025) 4 

54. Yuan, Y., Song, J., Iqbal, U., Vahdat, A., Kautz, J.: Physdiff: Physics-guided human motion diffusion model. In: ICCV (2023) 3, 4 

18 Y. Zhang et al. 

55. Zhang, J., Zhang, Y., Cun, X., Zhang, Y., Zhao, H., Lu, H., Shen, X., Shan, Y.: Generating human motion from textual descriptions with discrete representations. In: CVPR (2023) 3 

56. Zhang, Y., Li, R., Zhang, Y., Pan, L., Wang, J., Liu, Y., Li, X.: A plug-and-play physical motion restoration approach for in-the-wild high-difficulty motions. In: ICCV (2025) 2, 3, 4 

57. Zhang, Y., Kephart, J.O., Cui, Z., Ji, Q.: Physpt: Physics-aware pretrained transformer for estimating human dynamics from monocular videos. In: CVPR (2024) 2, 3, 4 

58. Zhao, K., Zhang, Y., Wang, S., Beeler, T., Tang, S.: Synthesizing diverse human motions in 3D indoor scenes. In: ICCV (2023) 3 

59. Zhu, L., Liu, X., Liu, X., Qian, R., Liu, Z., Yu, L.: Taming diffusion models for audio-driven co-speech gesture generation. In: CVPR (2023) 3 

# **Appendix** 

In this appendix, we provide: 

- Section A: Experiments on zero-shot transfer with H1 robot. 

- Section B: Further ablation study on data scale, representation, and hyperparameters. 

- Section C: Implementation details 

## **A Zero-shot transfer on H1 robot** 

Similar to the transfer on G1 robot, we pretrain a Whole-Body Controller (WBC) based on HOVER [11] on H1 format AMASS [28] dataset. Then we directly retarget the output motion from the motion generators and run HOVER [11] to obatain the motions under physics constraints. We evaluate and compare the performance between MaskedMimic [42], OmniControl [52], SFT baseline and PhysMoDPO on spatial-text control task in Table 1 on HumanML3D [6] test set. Overall, PhysMoDPO achieves the best performance across spatial controllability metrics, indicating more reliable tracking under the embodiment and controller shift. Meanwhile, PhysMoDPO maintains competitive text consistency, and also improves motion quality and smoothness. These results demonstrate the robustness of PhysMoDPO for spatial-text controlled motion generation in zero-shot transfer to H1. Additionally, we present visual comparison between MaskedMimic [42], OmniControl [52] and PhysMoDPO in Figure 1. We find that instead of boxing, the robot from MaskedMimic [42] randomly moves hands, while the motion from OmniControl [52] gives unstable initial rotation, which causes the robot to fall at the very beginning. 

## **B Ablation study** 

**Data representation.** As described in Section 3.1 of the main paper, the original HumanML3D data format requires expensive inverse kinematics to convert to SMPL [23] 

**Table 1: Evaluation of zero-shot human motion controllability with H1 robot on HumanML3D [6] dataset.** We apply the models trained with SMPL simulation and then perform zero-shot evaluation for Unitree H1 robot. The best results are in bold, and the second best results are underlined. 

|**Method**|**Err.** _↓_|**Spatial contr**<br>**Traj err 0.5**|**ollability**<br>_↓_**Traj err 0.2**|**Text co**<br>_↓_<br>**M2T** _↑_|**nsistency**<br>**R@3** _↑_|**FID** _↓_|**Jerk** _↓_|
|---|---|---|---|---|---|---|---|
|Real after simulation|0.2406|0.2734|0.8105|0.5915|0.3916|0.7976|203.6|
|MaskedMimic [42]|0.5173|0_._5752|0.9629|0.5459|0.2227|1.132|191_._4|
|OmniControl [52]|0.5121|0.7129|0.9639|0.5693|0.2803|1.038|279.3|
|SFT|0_._3504|0.6113|0_._9443|**0**_._**5846**|0_._3574|0_._9523|231.4|
|PhysMoDPO|**0**_._**2497**|**0**_._**4951**|**0**_._**9141**|0_._5830|**0**_._**3643**|**0**_._**8820 **|**172**_._**7**|


Y. Zhang et al. 

2 


**Fig. 1: Visual comparison with H1 robot.** We transfer the motion generated by MaskedMimic [42], OmniControl [52] and PhysMoDPO to H1 robot and then run Hover [11] to track the movement (blue points). See also the website. 

parameters, which are widely used for further rendering and tracking policy. Therefore, we retrain OmniControl [52] with SMPL-based representation [34], and compare with the original model in Table 2. We find that switching OmniControl [52] to the SMPL-based representation consistently improves spatial controllability across all controls and FID. Although text alignment slightly degrades, given that downstream rendering and tracking operate in SMPL space, we adopt the SMPL representation in the all experiments. 

**Data scale.** We further evaluate the impact of training data scale by using 20%, 50%, and 100% of the preference pairs. Even with only 20% data, the model remains reasonably strong for all metrics, indicating that our preference construction is sample-efficient. Increasing the scale consistently improves generation quality (FID) and text-motion alignment (MM-Dist). Interestingly, smaller scales yield slightly lower Jerk, while full data achieves the best overall FID and text-motion consistency with 

PhysMoDPO 3 

**Table 2: Ablation of data representation.** We compare OmniControl [52] model trained on different data representations. Numbers are calculated without applying tracking policy. The best results are in bold. 

|**Control**|**Data rep**|**S**<br>**Err.** _↓_**T**|**patial contr**<br>**raj err 0.5**|**ollability**<br>_↓_**Traj err 0.2** _↓_|**Text cons**<br><br>**MM-Dist**|**istency**<br>_↓_**R@3** _↑_|**FID** _↓_|**Jerk** _↓_|
|---|---|---|---|---|---|---|---|---|
|Pelvis|HML3D<br>SMPL|0.0724<br>**0**_._**0352**|0.1055<br>**0**_._**0420**|0.2920<br>**0**_._**1855**|**3**_._**0137**<br>3.0255|0.7900<br>**0**_._**7822**|0.3619 <br>**0**_._**2107**|**33**_._**30**<br> 34.38|
|Lfthd|HML3D|0.1320|0.2197|0.6504|**2**_._**9725**|**0**_._**8037**|0.3053|**30**_._**92**|
|e an|SMPL|**0**_._**0662**|**0**_._**1094**|**0**_._**4756**|3.0054|0.7842|**0**_._**1881**|33.37|
|Right hand|HML3D<br>SMPL|0.1317<br>**0**_._**0656**|0.2188<br>**0**_._**1006**|0.6572<br>**0**_._**4766**|**2**_._**9093**<br>3.0276|0.7939<br>**0**_._**7656**|0.2523 <br>**0**_._**1753**|**31**_._**60**<br> 34.29|


**Table 3: Ablation studies.** We train OmniControl [52] and study the impact of the data scale and preference pair selection strategies on HumanML3D [6] dataset. The best results are in bold. 

|**Ratio**|**Err.** _↓_**M**|**M-Dist**|_↓_**FID** _↓_|**Jerk** _↓_|**Method**|**Err.** _↓_|**MM-Dist**|_↓_**FID** _↓_|**Jerk** _↓_|
|---|---|---|---|---|---|---|---|---|---|
|OmniControl [52]<br>20 %<br>50%|0.1998<br>0.1434<br>01430|4.23<br>3.46<br>339|5.82<br>1.34<br>124|115.12<br>**67**_._**69**<br>7028|OmniControl [5<br>Fuse score|2]<br>0.1998<br>0.1476|4.23<br>3.45|5.82<br>1.61|115.12<br>78.95|
|<br>100 %|.<br>**0**_._**1421**|.<br>**3**_._**36**|.<br>**1**_._**17**|.<br>72.13|Dominance|**0**_._**1421**|**3**_._**36**|**1**_._**17**|**72**_._**13**|


**(a)** Different data scales 

**(b)** Pair selection strategies 

slightly higher dynamics. We attribute this to larger-scale training encouraging more diverse and semantically expressive motions, which may contain stronger accelerations. **Pair selection strategy.** We compare two strategies for constructing preference pairs from multiple rewards: (i) score fusion by normalizing rewards and using weighted summation (Fuse score), and (ii) our strict dominance-based selection (Dominance), which requires the winning sample to outperform the losing one on all rewards. Weighted fusion is highly sensitive to reward weights and tends to introduce reward engineering and reward hacking. Empirically it performs notably worse. In contrast, the proposed dominance-based selection consistently yields better overall performance and more stable training, demonstrating its effectiveness for multi-objective preference construction without tuning fragile weights. 

**Ablation on SFT loss ratio** _λ_ **SFT.** Table 4 (top) studies the effect of adding an SFT loss on the preferred (win) samples. When _λ_ SFT = 0, the model shows degraded controllability and generation quality. Increasing _λ_ SFT consistently improves spatial controllability, text consistency, as well as FID and jerk, and reaches the best overall performance at _λ_ SFT =2. Further increasing _λ_ SFT (e.g., 5 or 10) yields slight regressions, suggesting overly strong SFT regularization may weaken the benefit of preference optimization. We therefore use _λ_ SFT =2 in all experiments. 

**Ablation on DPO temperature** _β_ **.** Table 4 (bottom) evaluates the DPO temperature _β_ with _λ_ SFT =2. A small temperature ( _β_ =1) provides limited improvement, while a moderate value ( _β_ =20) achieves the best overall trade-off across controllability, 

4 Y. Zhang et al. 

**Table 4: Ablation study on hyperparameters.** Here _λ_ SFT is the weight of SFT loss on win sample, _β_ is the temperature parameter from Diffusion-DPO [46]. The best results are in bold, and the second best results are underlined. 

|_λ_**SFT**|_β_|**S**<br>**Err.** _↓_**T**|**patial contr**<br>**raj err 0.5**|**ollability**<br>_↓_**Traj err 0.2**|**Text con**<br>_↓_<br>**MM-Dist**|**sistency**<br> _↓_**R@3** _↑_|**FID** _↓_|**Jerk** _↓_|
|---|---|---|---|---|---|---|---|---|
|0|20|0.2348|0.5918|0.9023|4.21|0.6133|5.28|116.77|
|1|20|0.1771|0.5469|0.8887|4.00|0.6387|4.31|103.64|
|2|20|**0**_._**1421**|**0**_._**4238**|**0**_._**8418**|**3**_._**36**|**0**_._**7246**|**1**_._**17**|**72**_._**13**|
|5|20|0_._1440|0_._4463|0_._8496|3_._40|0_._7139|1_._82|81_._11|
|10|20|0.1476|0.4629|0.8662|3.49|0.7041|2.29|88.07|
|2|1|0.1513|0.4775|0.8701|3.53|0.6973|2.42|91.31|
|2|5|0_._1458|0_._4492|0_._8604|3_._44|0_._7002|1_._95|85_._83|
|2|20|**0**_._**1421**|**0**_._**4238**|**0**_._**8418**|**3**_._**36**|**0**_._**7246**|**1**_._**17**|**72**_._**13**|
|2|50|0.1848|0.5566|0.8926|4.02|0.6367|4.41|106.02|


text alignment, and generation quality. When _β_ becomes too large ( _β_ = 50), the performance drops significantly (e.g., worse FID and higher jerk), indicating overly aggressive preference updates can harm distributional quality and motion smoothness. Hence, we set _β_ =20 by default. 

## **C Implementation details** 

In Section 4.1 of the main paper, we provide a brief overview of the implementation details. For completeness and reproducibility, we present the full experimental configuration in this appendix for text-to-motion and spatial-text control tasks. In addition, we complement the metrics and the user study details. 

**Implementation details for the text-driven task.** We apply the pretrained model from MotionStreamer [50] to initialize the data generation pipeline and then generate 12 samples for each text prompt from the training set of HumanML3D [6]. As for the post-training stage, we fix all the parameters except the diffusion head inside the MotionStreamer. Following the Transformer training setup of MotionStreamer [50], we replace the standard diffusion training losses with Two-Forward strategy as our _LSFT_ loss on win samples _Xwin_ . We train the model using a batch size of 32, with AdamW optimizer [24] with learning rate 1e-6 for 5,000 iterations, among which the first 500 steps are warm-up stage. The hyperparamters _λ_ SFT and Diffusion-DPO [46] temperature _β_ in PhysMoDPO framework are set to 1 and 5, respectively. As for SFT baseline, we set the DPO loss weight to be zero, while the other hyperparameters remain unchanged. Following OmniControl [52], the threshold _h_ 0 and _v_ 0 in _R_ slide are set to 0.05 m and 0.50 m/s. Note that, as we remove motions which requires object support for both training and inference, we reproduce all the baseline results with the new filtered test set for fair comparison. 

**Implementation details for spatial-text task.** To complement to implementation details in Section 4.1 of the main paper, we further describe the training settings, 

PhysMoDPO 5 

hyperparameters and baselines. We follow the training protocol of OmniControl [52] and evaluate cross-control as in OmniControl, where we randomly sample a variable number of control joints for each test sample. We additionally report single-joint control evaluation in Section B. We convert HumanML3D [6] into a SMPL-based representation and re-train the OmniControl backbone on this format. An ablation on the data representation is provided in Section B. The original OmniControl training selects a single control joint per sample, which can mismatch the cross-control evaluation. Therefore, we additionally re-train OmniControl with the cross-control protocol, i.e., sampling a random set of control joints during training (cross). We then apply PhysMoDPO to finetune the cross-trained OmniControl for 4,000 steps with batch size 64, using a linear warm-up over the first 200 steps. We fix _λ_ SFT=2 and _β_ =20 for all experiments on spatial-text control task and the corresponding hyperparameter ablations can be found in the Section B. Beyond HumanML3D, we further adapt the model pretrained on HumanML3D [6] data to the out-of-distribution OMOMO [15] dataset without using its ground-truth motions as supervised training targets, while keeping the same pipeline and hyperparameters. In terms of MaskedMimic, for fair comparison, we initialize the robot with standard pose and then add 1 second warm up stage to make the robot move to the first frame spatial control signals, and then we remove the first 30 frames to calculate the metrics. 

**Additional metrics.** For spatial control task, in addition to masked MSE between _Cs_ and _X_<sup>_′_</sup> (Err.), we further evaluate the controllability through failure rate (Traj err) under given threshold. Specifically, Traj err 0.5 represents the ratio of failure motion sequences whose maximum joint error across the whoe sequence is larger than 0.5 meters. **User study details.** We generate 40 videos per method and thus provide 80 questions. As shown in Figure 2, for each question, we show two real robot videos from PhysMoDPO and one of the baseline methods. Twenty participants evaluated the videos according to 3 aspects: text-motion consistency, smoothness, and stability. For each sub-question, the participant could select one of the videos or "Both are similar". 

Y. Zhang et al. 

6 


**Fig. 2: User study design.** We show the text input with 2 videos generated by PhysMoDPO and one baseline method. The participant is asked to evaluate the videos according to text-motion similarity, smoothness and stability. 

