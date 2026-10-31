---
title: "World2Act: Latent Action Post-Training from World Model Dynamics"
date: "2026-03-11"
authors: "An Dinh Vuong; Tuan Van Vo; Abdullah Sohail; Haoran Ding; Liang Ma; Xiaodan Liang"
url: https://arxiv.org/abs/2603.10422
pdf: https://arxiv.org/pdf/2603.10422
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.10422)** / [論文ページ](https://arxiv.org/abs/2603.10422)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **WORLD2ACT: Latent Action Post-Training from World Model Dynamics** 

**An Dinh Vuong**<sup>_∗_</sup> **Tuan Van Vo**<sup>_∗_</sup> **Abdullah Sohail Haoran Ding Liang Ma** MBZUAI MBZUAI MBZUAI MBZUAI MBZUAI 

```
an.vuong@mbzuai.ac.ae
```

**Xiaodan Liang Anqing Duan Ivan Laptev** MBZUAI MBZUAI MBZUAI 

**Ian Reid** 

MBZUAI 

**Abstract:** World Models (WMs) offer a promising mechanism for post-training Vision-Language-Action (VLA) policies by providing dynamics priors that improve generalization under task and scene variation. However, most WM-based post-training methods rely on pixel-space supervision, making policies sensitive to visual artifacts introduced by imperfect WM rollouts. We present WORLD2ACT, a latent-space post-training framework that transfers WM dynamics to the VLA policy without pixel-space supervision. WORLD2ACT operates in two stages: _(i)_ it induces a shared video–action latent space by contrastively aligning WMdynamics latents with action embeddings, and _(ii)_ it post-trains the VLA by guiding policy action representations toward WM-imagined dynamics rather than decoded pixels. Built on GR00T-N1.6, WORLD2ACT delivers absolute success-rate gains of up to +2.5% on simulation benchmarks (RoboCasa, LIBERO, BridgeSIMPLER) and +6.7% on a real robot over finetuned VLA baselines. Notably, it outperforms pixel-space WM supervision by up to +6.0%, including on LIBERO where pixel supervision _degrades_ the baseline, suggesting that latent WM dynamics offer a more stable WM-based post-training alternative to pixel-space transfer. 

**Keywords:** World Models, Vision-Language-Action, Robotic Manipulation 

## **1 Introduction** 


(a) Pixel-space post-training. 

(b) Latent post-training (Ours). 

(c) Post-training performance. 

Figure 1: _(a) Problem:_ Prior WM _→_ VLA post-training relies on imagined pixel rollouts, making policies vulnerable to visual artifacts. _(b) Solution:_ We bypass this by directly aligning VLA action representation with WM latent space. _(c)_ Post-training on GR00T-N1.6 [1] indicates that our latent post-training yields consistent improvements, overcoming the instability of pixel-space methods. 

World models (WMs) offer a promising source of dynamics priors for embodied agents by modeling how robot-object interactions evolve over time [2, 3]. In contrast, most vision-language-action 

> _∗_ Equal contribution 

(VLA) policies are learned primarily via behavior cloning and can struggle with environmental changes or unseen contact conditions, even after finetuning on extensive datasets [4, 5]. This generalization gap suggests that VLAs lack robust dynamics priors that finetuning alone cannot provide [6], motivating post-training methods that inject these priors from WMs [7]. 

Previous WM-based post-training work [7, 8] largely targets pixel-to-action supervision via an inverse dynamics model (IDM) [9], or reward signals [10]. However, because these signals are computed from WM rollouts, their quality is limited by the fidelity of the generated pixels. When rollouts contain visual artifacts [11], or inconsistent contacts [12], these errors can be directly converted into noisy action labels or rewards, and may compound over long horizons [13]. Such noisy training signals can harm VLA policy performance, necessitating more reliable post-training approaches. 

Video latents from WMs capture transferable behavioral dynamics [14], offering a natural alternative to pixels for transferring knowledge from WMs to VLAs [15]. Prior latent-video-to-action methods typically learn unified video–action representations, such as UWM [16] and Cosmos Policy [3]. However, these frameworks often rely on high-dimensional joint embedding spaces, which can destabilize training [17]. We instead post-train the VLA by matching policy action latents to WM-predicted latent dynamics targets in a shared low-dimensional video–action latent space. This bypasses pixel-space action refinement and reduces sensitivity to visual artifacts in WM rollouts. 

We therefore introduce WORLD2ACT, a latent post-training method that aligns VLA action representation with WM latent video dynamics. Rather than supervising the policy from imagined pixels, WORLD2ACT uses WM latent trajectories as targets for policy action latents. Our method proceeds in two stages. First, we train video and action adapters that project WM video latents and expert action sequences into a shared representation space using a contrastive matching objective. Second, we post-train GR00T-N1.6 [1] by regularizing its action features toward this shared latent space, leaving the VLA backbone unchanged. Across RoboCasa [18], LIBERO [19], Bridge-SIMPLER [20], and real-world robot evaluations, WORLD2ACT improves post-training performance over pixel-space supervision, as illustrated in Fig. 1. In summary, our contributions are threefold: 

- We identify sensitivity to visual artifacts in imagined rollouts as a key limitation of pixel-space WM post-training, motivating latent-space dynamics alignment as a more reliable alternative. 

- We introduce WORLD2ACT, a two-stage post-training method that aligns VLA action representations with WM video-dynamics latents through a shared video–action adapter space. 

- With GR00T-N1.6 as the VLA backbone, WORLD2ACT consistently outperforms pixel-space post-training methods and other baselines on simulation [18, 19, 20] and real-world benchmarks. 

## **2 Related Work** 

**World Models for Policy Improvement.** WMs have emerged as a key component in developing generalist robots [21]. Because real-world data collection is serial, slow, and labor-intensive, WMs provide a low-cost, resettable, and highly scalable alternative for simulating environments and finetuning policies [22]. Prior work leveraging WMs to improve policies can be broadly grouped into two categories [23]: _i) Model-based control_ , where WMs act as virtual environments to support methods such as model-based planning [24, 25, 26, 7]. These approaches rely on interactive, actionconditioned WMs, such as V-JEPA 2 [15], to produce imagined rollouts that guide the policy toward preferred trajectories [27]. However, training such interactive models and subsequently rolling out numerous imagined trajectories can be computationally expensive and difficult to parallelize with policy optimization [10]. _ii) Instruction-based control_ , which conditions generation on task specifications, such as natural-language descriptions, to produce complete sequences of future states or actions [28, 29, 9, 30]. This work adopts an instruction-based paradigm that enables simultaneous video generation and policy optimization in an efficient, parallel post-training pipeline. 

**Post-Training Vision-Language-Action Models.** VLA backbones are commonly pretrained on web-scale instruction-following data and then finetuned on task- or robot-specific datasets [27]. However, internet data primarily captures static semantics and broad vision–language knowledge, whereas robotics data is narrow, temporally structured, and action-centric; this mismatch 

2 

can degrade downstream control performance [5]. Recent work, therefore, moves beyond webdata finetuning [26, 31, 32, 33, 16] toward WM post-training, which can provide dynamics and action-relevant structure [10]. Existing methods, however, mainly focus on pixel space: they infer pseudo-actions from generated videos using IDMs [9] or learn rewards from pixel rollouts [7, 9, 8, 34, 35, 10]. Because generated rollouts can exhibit visual artifacts, these pixel-derived signals may introduce noisy supervision [11] and degrade post-training. We address this limitation by aligning video and action representations directly in a shared video–action latent space. 

**Latent Actions.** Latent action representations have been explored as effective interfaces for learning from offline robot data and unlabeled videos across embodiments [26, 14, 31, 36, 37]. More recent methods further learn joint latent video–action spaces that couple world modeling with action prediction, shifting generic video modeling toward action-aware dynamics [16, 3, 38]. While these methods bridge visual dynamics and action prediction, they often rely on high-dimensional joint embeddings that introduce architectural overhead when adapting existing VLA backbones. We instead align WM dynamics latents with VLA action features through lightweight adapters for post-training. 

## **3 Method** 

We present WORLD2ACT, a post-training method that transfers visual-dynamic priors from a frozen instruction-conditioned video WM to a VLA policy, as shown in Fig. 2. We first describe the WM latent representation, then present our two-stage pipeline: _i) Stage 1_ : learning a shared video–action latent space that aligns WM latent dynamics with robot actions via bridge adapters, and _ii) Stage 2_ : training a lightweight residual policy on top of a frozen VLA, guided by the aligned latent space. 

### **3.1 Preliminaries: Instruction-Conditioned Video World Model** 

We instantiate the world model _W_ with Cosmos-Predict2 [39], an instruction-conditioned video WM for future visual-state prediction that operates in a structured video-VAE latent space. During pretraining, ground-truth videos are encoded by the video VAE into latent trajectories **V**<sup>gt</sup> = _{Vt_<sup>gt</sup><sup>_}T_</sup> _t_ =1<sup>,</sup> and a denoising network _W_ denoise is trained via flow matching [40] to predict the vector field that transports noisy latents toward **V**<sup>gt</sup> in this structured latent space. Given the initial observation _s_ 1 and language instruction _ℓ_ , _W_ denoise predicts future visual dynamics in the video-VAE latent space: 


where _ϵ_ is the initial noise and each _Vt_ is a denoised spatial latent corresponding to a non-overlapping chunk of _M_ frames. In WORLD2ACT, we freeze all components of _W_ , preserving its structured video-VAE latent space, and use video latents **V** before VAE decoding as compact visual-dynamics priors. Since these latents describe what should visually happen but do not specify robot controls, we train a video–action bridge to map them into an action-aware latent space for VLA post-training. 

### **3.2 Stage 1: Aligning Video Dynamics and Robot Actions** 

Stage 1 learns a video–action latent bridge from synchronized state-action demonstrations. Given an expert trajectory video, the frozen world model _W_ obtains a video latent sequence **V** = _{Vt}_<sup>_T_</sup> _t_ =1<sup>,</sup> with each _Vt_ corresponding to a chunk of _M_ low-level steps, as described in subsection 3.1. 

A CNN-based _Video Adapter B_ v maps each WM latent to a _D_ -dimensional embedding, producing **z**<sup>v</sup> = _{zt_<sup>v</sup><sup>_}T_</sup> _t_ =1<sup>_∈_R</sup><sup>_T ×D_,where</sup><sup>_z_</sup> _t_<sup>v=</sup><sup>_B_v(</sup><sup>_Vt_).Inparallel,anMLP-based</sup><sup>_ActionAdapterB_a</sup> partitions **a** gt into temporally aligned action chunks _a_ ¯ _t_<sup>gt</sup> = [ _a_<sup>gt</sup> ( _t−_ 1) _M_ +1<sup>;</sup><sup>_. . ._;</sup><sup>_a_</sup> _tM_<sup>gt]andmapseach</sup> chunk to _zt_<sup>a=</sup><sup>_B_a(¯</sup><sup>_a_</sup> _t_<sup>gt), yielding</sup><sup>**z**a=</sup><sup>_{z_</sup> _t_<sup>a</sup><sup>_}T_</sup> _t_ =1<sup>_∈_R</sup><sup>_T ×D_.This produces temporally aligned video</sup> and action embeddings while retaining within-chunk control variations, as depicted in Fig. 2a. 

To ensure the action latents preserve kinematics and temporal structure, we introduce an MLP-based _Action Decoder D_ a, which maps each action chunk latent _zt_<sup>abackto</sup><sup>_M_low-levelactionvectors.</sup> We train _B_ v, _B_ a, and _D_ a with two objectives. First, we use a reconstruction objective: unrolling the decoded chunks gives the reconstructed action sequence ˆ **a** , supervised by _L_ recon = _∥_ **a** gt _−_ **a** ˆ _∥_<sup>2</sup> . 

Second, we align video and action dynamics with a bidirectional InfoNCE loss [41], which encourages paired video–action trajectories to be close in the shared latent space while separating pairs 

3 


Figure 2: **WORLD2ACT overview. (a)** _Stage 1: Latent alignment._ We train video and action adapters ( _B_ v _, B_ a) with reconstruction and contrastive objectives. **(b)** _Stage 2: VLA post-training._ We freeze the VLA and learn a residual policy guided by WM-induced latent dynamics. 

from different demonstrations. A key design choice is whether to contrast a single global trajectory embedding or to preserve temporal correspondence across the trajectory. We adopt a chunkaware trajectory alignment by computing similarity as the average cosine similarity over temporally aligned chunks. This reduces shortcut solutions where the model matches sequences using coarse task identity or background cues rather than fine-grained temporal dynamics. For each positive pair ( **z**<sup>v</sup> _i_<sup>_,_</sup><sup>**z**a</sup> _i_<sup>) from the same demonstration, the remaining</sup><sup>_B−_1 samples in the batch serve as negatives,</sup> including _i) easy_ negatives from different tasks and _ii) hard_ negatives from other demonstrations of the same task. For a paired video–action sample _i_ in a batch of size _B_ , the loss is defined as: 


where _τ_ is a temperature and sim( **z**<sup>v</sup> _i_<sup>_,_</sup><sup>**z**a</sup> _j_<sup>)=</sup> _T_<sup><u>1</u></sup> � _Tt_ =1<sup>cos(</sup><sup>_z_</sup> _i,t_<sup>v</sup><sup>_, z_</sup> _j,t_<sup>a) denotes chunk-averaged cosine</sup> similarity. We set _τ_ =0 _._ 1 [42] and optimize _L_ = _L_ recon + _L_ contrastive. After Stage 1, _B_ v, _B_ a, and _D_ a are frozen to preserve a shared latent space between video dynamics and decodable robot actions. 

### **3.3 Stage 2: World-Model-Guided Latent-Residual Post-Training** 

Inspired by Silver _et al._ [43], we avoid post-training the heavily parameterized VLA policy, which can be sample-inefficient and prone to catastrophic forgetting [5]. Instead, we freeze the VLA backbone _π_ base and train a lightweight _Residual Policy f_<sup>_θ_</sup> that predicts an additive correction in the learned action-latent space, as in Fig. 2b. To train this residual policy, we use Stage-1-aligned WM latents as weak supervision for action-latent corrections, since the WM encodes imagined task dynamics rather than executable control labels. For a single rollout, given state _st_ and instruction _ℓ_ , the base VLA predicts an action chunk ¯ _a_ base _,t_ = _π_ base( _st, ℓ_ ), which is mapped to the action-latent space. _f_<sup>_θ_</sup> then refines this latent by combining the base action latent with a learned residual latent: 


The decoded action chunk ¯ _a_ final _,t_ = _D_ a( _z_ final<sup>a</sup> _,t_<sup>) is executed open-loop for</sup><sup>_M_control steps before</sup> the policy is queried again at the next chunk boundary. The Stage-1 action decoder _D_ a is kept frozen during this process, so all residual-corrected latents are decoded through the same mapping learned to reconstruct demonstration action chunks. We implement _f_<sup>_θ_</sup> ’s backbone as a Transformer conditioned on observation tokens and language-conditioned base action-latent tokens; see Appendix C. 

To obtain the visual-dynamics target, at each iteration, we run _B_ parallel simulator environments under the current augmented policy, using the simulator only to obtain initial conditions and roll out the refined action chunks. We do not require training signals from the simulator such as rewards, success 

4 

labels, or differentiable state transitions. For each environment instance _i_ , _W_ generates video latents **V** _i_ = _{Vi,t}_<sup>_T_</sup> _t_ =1<sup>conditioned on the initial observation and instruction (</sup><sup>_si,_1</sup><sup>_, ℓi_), as described in</sup> Eq. (1). The frozen video adapter maps these latents to video-dynamics embeddings **z**<sup>v</sup> _i_<sup>=</sup><sup>_B_v(</sup><sup>**V**</sup><sup>_i_),</sup> while the augmented policy produces action-latent trajectories **z**<sup>a</sup> final _,i_<sup>=</sup><sup>_{z_</sup> final<sup>a</sup> _,i,t_<sup>_}_</sup> _t_<sup>_T_</sup> =1<sup>.</sup> 

Finally, we minimize _L_ contrastive from Eq. (2) between **z**<sup>v</sup> _i_<sup>and</sup><sup>**z**a</sup> final _,i_<sup>across the</sup><sup>_B_parallel rollouts,</sup> where latents from the same rollout form positive pairs and latents from different rollouts serve as negatives, following Stage 1. Gradients are taken only through _f_<sup>_θ_</sup> , aligning the augmented policy action latents with WM-induced dynamics while keeping the VLA and Stage-1 modules frozen. 

## **4 Experiments** 

We design our empirical evaluation to answer the following core questions: 

- **Q1:** How effectively does WORLD2ACT improve strong VLA baselines compared with prior post-training methods on complex manipulation tasks? 

- **Q2:** How do latent action alignment and the residual policy architecture improve action representations toward target WM dynamics, and how do these gains affect manipulation performance? 

- **Q3:** How does scaling post-training data and tasks affect generalization to unseen robotic skills? 

- **Q4:** Does WORLD2ACT transfer effectively to real-world robot experiments? 

### **4.1 Main Results** 

We evaluate on 3 simulated benchmarks: RoboCasa [18], LIBERO [19], and Bridge-SIMPLER [20], an extension of SIMPLER [44]. We use mean success rate (SR) as the primary metric. Following standard protocols [18, 3, 45], we run 50 trials per task for each of 5 seeds and report the mean SR. 

**Experimental Setup.** We benchmark against recent VLA policies: _π_ 0 [46], _π_ 0 _._ 5 [47], UVA [48], Rethink-VLA [49], OpenVLA [50], OpenVLA-OFT [51], UWM [16], UniVLA [31], Cosmos Policy [3], CoWVLA [38], FLARE [25], and GR00T-N1.6 [1]. To isolate the post-training effect, we additionally compare WORLD2ACT to representative post-training baselines: a BC variant of WORLD2ACT, which replaces the contrastive objective with supervised behavior cloning on the target demonstrations [52], DreamGen [9], VLA-RFT [7], and Ctrl-World [10]. For a fair comparison, we implement WORLD2ACT and all post-training methods on the same GR00T-N1.6 backbone. Because GR00T-N1.6 is pretrained on mixed cross-embodiment data [53], its behavior may not align with the simulator task distributions. We therefore finetune GR00T-N1.6 on 1000 expert trajectories for each simulator to obtain a task-aligned supervised reference, denoted as GR00T-N1.6-ft. 

|Table 1:**Results on RoboCasa.**|Table 2: **Results on LIBERO.**<br>Detailed SR of Spatial, Object,|Table 3:<br>**Results on Bridge-**<br>**SIMPLER.** We evaluate on 7|
|---|---|---|
|**Baselines**<br>**SR**|Goal, and Long are in App.A.|tasks; full details in App.A.|
|_π_0 [46]<br>0.625<br>UVA [48]<br>0.500|**Baselines**<br>**Avg. SR**|**Baselines**<br>**SR**|
|Rethink-VLA [49]<br>0.547|_π_0_._5 [47]<br>0.969|_π_0[46]<br>0.337|
|UWM [16]<br>0.608|OpenVLA-OFT [51]<br>0.971|<br><br>OpenVLA [50]<br>0.103|
|FLARE [25]<br>0.701<br>GR00T-N1.6 [1]<br>0.662|UniVLA [31]<br>0.952<br>CoWVLA [38]<br>0.956|<br><br>OpenVLA-OFT [51]<br>0.438|
|Cosmos Policy [3]<br>0.657|Cosmos Policy [3]<br>**0.985**|GR00T-N1.6-ft [1]<br>0.576|
|GR00T-N1.6-ft [1]<br>0.701<br>GR00T-N1.6-ft+DreamGen [9]<br>0.705|GR00T-N1.6-ft [1]<br>0.970<br>GR00T-N1.6-ft+DreamGen [9]<br>0.921|GR00T-N1.6-ft+DreamGen [9]<br>0.583<br>GR00T-N1.6-ft+WORLD2ACT(Ours)<br>**0.590**|
|GR00T-N1.6-ft+WORLD2ACT(Ours)<br>**0.726**|GR00T-N1.6-ft+WORLD2ACT(Ours)<br>0.981||


**Post-Training Data Synthesis.** We use Cosmos-Predict2 [39] to synthesize approximately 1000 imagined trajectories per simulator across RoboCasa, LIBERO, and Bridge-SIMPLER for all posttraining methods, totaling roughly 3000 synthetic trajectories. Post-training initial scenes are disjoint from evaluation scenes to prevent test leakage. Additional details are provided in Appendix B.2. 

**Results on RoboCasa.** Table 1 shows that WORLD2ACT achieves the best RoboCasa result, improving the same backbone GR00T-N1.6-ft from 70 _._ 1% to 72 _._ 6% SR, a +2 _._ 5% absolute gain. It also outperforms DreamGen under the same finetuned starting point by +2 _._ 1%, showing that our 

5 

imagined-trajectory post-training objective is more effective than prior synthetic-data augmentation. Against the broader set of baselines, WORLD2ACT leads vanilla GR00T-N1.6 by +6 _._ 4% and the WM-capable Cosmos Policy by +6 _._ 9%, establishing the strongest RoboCasa performance overall. 

**Results on LIBERO.** Table 2 reports average SR on LIBERO. WORLD2ACT achieves a 98 _._ 1% SR, while DreamGen degrades GR00T-N1.6-ft to 92 _._ 1%, suggesting IDM noise from WM artifacts (WM rollouts raise IDM action MSE by 18%; Table 15, Appendix F.2). Our method therefore yields a +6 _._ 0% absolute gain over DreamGen on the same backbone. It also surpasses _π_ 0 _._ 5, OpenVLAOFT, CoWVLA, and UniVLA, and comes within 0 _._ 4% of the best reported Cosmos Policy result. 

**Results on Bridge-SIMPLER.** Table 3 reports average success on Bridge-SIMPLER. We use AutoEval Bridge-SIMPLER [20] because it extends the original WidowX-based SIMPLER Bridge setup with three additional tasks, giving a broader evaluation for the WidowX embodiment. Consistent with RoboCasa and LIBERO, WORLD2ACT improves GR00T-N1.6-ft from 57 _._ 6% to 59 _._ 0% SR, a +1 _._ 4% absolute gain, and also outperforms DreamGen (58 _._ 3%), achieving the best overall result. 


Figure 3: **Post-training scaling and generalization.** _Left:_ Cosine similarity correlates with downstream success rate. _Right:_ Unseen-task performance as seen-task diversity increases. 

**Cross-Task Generalization.** We split 24 RoboCasa tasks into 12 seen/12 unseen tasks and scale post-training from 0 to 12 seen tasks (details in Appendix B.3). To isolate cross-task generalization, we evaluate base VLAs without task-specific finetuning. On the unseen split, WORLD2ACT consistently improves with task diversity, yielding +2 _._ 4% on GR00T-N1.6-base and +1 _._ 1% on Cosmos Policy (Fig. 3b). Since the vanilla VLAs never observe unseen-task trajectories, these gains suggest that generalized WM dynamics effectively transfer to novel skills. 

Table 4: **Post-training comparison.** All rows use GR00T-N1.6-ft as the base model; ‘+’ denotes post-training. 

Table 5: **Adapter and latent objective ablation studies.** Latent obj. denotes the contrastive objective and similarity design used to align WM video latents with action latents. 

|**Method**|**SR**|**Study**|**Variant**|**Time**|**SR**|
|---|---|---|---|---|---|
|GR00T-N1.6-ft [1]|0.701|Latent obj.|Single InfoNCE [54] + chunk sim.|–|0.720|
|+WORLD2ACTw/ BC [52]|0.704||<br>Marginal [55] + chunk sim.|–|0.707|
|+DreamGen [9]|0.705||<br>Bi InfoNCE [41] + global sim.|–|0.693|
|+VLA-RFT [7]<br>+Ctrl-World [10]|0.710<br>0.698|Adapter|<br>LoRA,_r_=16<br>LoRA,_r_=32|14.6h <br>15.3h|0.714<br> 0.721|
|+WORLD2ACT(Ours)|**0.726**|Ours|Residual + Bi InfoNCE + chunk sim.|**6.8h**|**0.726**|


**Comparison of Post-Training Methods.** Table 4 compares post-training methods using GR00TN1.6-ft as the base model. WORLD2ACT improves RoboCasa success rate from 70 _._ 1% to 72 _._ 6%, outperforming BC on expert trajectories (70 _._ 4%) and prior post-training baselines, including DreamGen (70 _._ 5%), VLA-RFT (71 _._ 0%), and Ctrl-World (69 _._ 8%). These results suggest that latent-space post-training provides a more effective adaptation signal than existing alternatives. 

6 

### **4.2 Ablation Study** 

**Correlation Between Cosine Similarity and Success Rate.** Fig. 3a shows that video–action cosine similarity (sim( **z**<sup>v</sup> _i_<sup>_,_</sup><sup>**z**</sup> _i_<sup>a) from Eq. (2)) increases alongside downstream SR during post-training.For</sup> WORLD2ACT, cosine similarity rapidly climbs and stabilizes around 0 _._ 95 after 5K steps, while SR rises from 70 _._ 1% to 72 _._ 6%. This trend suggests that post-training strengthens video–action alignment and that stronger alignment is associated with improved manipulation performance. 

**Scaling Post-Training Trajectories.** Fig. 1c plots SR on RoboCasa as the number of post-training trajectories _N_ increases on the same GR00T-N1.6-ft base model: red denotes WORLD2ACT latent post-training, blue denotes DreamGen pixel-space post-training, and the gray dotted line marks the GR00T-N1.6-ft baseline. WORLD2ACT scales monotonically from 70 _._ 1% to 72 _._ 6% as _N_ increases from 0 to 1000, while DreamGen is non-monotonic, dropping to 69 _._ 1% at _N_ =500 before recovering to 70 _._ 5%, suggesting that pixel-space pseudo-labeling is more sensitive to post-training noise. 

**Residual Policy vs. LoRA Finetuning.** Table 5 compares our residual policy against LoRA finetuning on performance and speed. Compared with LoRA, our residual policy achieves higher SR at much lower cost: 72 _._ 6% vs. 72 _._ 1% for LoRA _r_ =32, with 2 _._ 25 _×_ faster training (6 _._ 8h vs. 15 _._ 3h). This supports freezing the VLA and learning only a lightweight action-space correction. 

**Contrastive Loss Ablation Study.** The latent-objective ablation in Table 5 shows that both bidirectional contrast and chunk-level temporal alignment are important. Replacing our bidirectional InfoNCE with unidirectional InfoNCE [54] drops SR from 72 _._ 6% to 72 _._ 0%, while using a marginal loss [55] further reduces it to 70 _._ 7%. Collapsing the temporally aligned chunk-wise similarity into a single global trajectory similarity performs worst at 69 _._ 3%, indicating that fine-grained video–action alignment, rather than coarse trajectory-level matching, is critical for manipulation. 


Table 6: **Action-space error.** MSE is computed between predicted and reference-expert actions over 3 tasks; lower is better. 

|**Method**|**MSE**_↓_|
|---|---|
|GR00T-N1.6-ft|0.034|
|+WORLD2ACT(Ours)|**0.021**|


Figure 4: **Action-latent t-SNE visualization.** 

**Action Validity Analysis.** We assess how Stage-2 WORLD2ACT latent alignment affects actionmanifold compatibility. Fig. 4 shows, on _OpenDrawer_ , that predicted-action latents after posttraining overlap more with reference-action and target-WM latent regions than before. Table 6 further reports action-space MSE between predicted actions and temporally matched held-out expert actions, averaged over _OpenDrawer_ , _PnPCounterToCab_ , and _TurnOnStove_ ; the error drops from 0 _._ 034 to 0 _._ 021, a 0 _._ 013 decrease (38 _._ 2% relative). These results are consistent with our weaksupervision view: Stage-2 residual updates move action latents toward WM dynamics priors while keeping decoded actions near the expert action manifold. Additional analyses are in Appendix B.5. 


Figure 5: **Robot Setup.** 


Figure 6: **Real-world robot success rates.** 

7 

### **4.3 Real Robot Experiments** 

**Setup.** We evaluate WORLD2ACT on a Franka Research 3 across three real-world tasks: _Pick cup and place on plate_ , _Pick up bowl_ , and _Close microwave_ . We start from GR00T-N1.6-ft with 20 real demonstrations per task, collected using GELLO [56], and further train with 100 WM-generated trajectories. Observations come from an external camera (Fig. 5), and we run 20 trials per task. 

**Results.** Fig. 6 summarizes real-world evaluations. WORLD2ACT improves GR00T-N1.6-ft by 6 _._ 7% on average and outperforms DreamGen by 8 _._ 3%, suggesting that latent WM-guided posttraining transfers more effectively to physical robots than synthetic-data augmentation. 


t=1 


t=18 


t=36 


t=54 


t=72 


t=90 

Figure 7: **Qualitative results of our WM-to-VLA framework.** _Top:_ A trajectory generated by the WM. _Bottom:_ The corresponding real-robot execution of the same task utilizing GR00T-N1.6-ft + WORLD2ACT. _t_ denotes the timestep for each frame. 

**Qualitative Evaluation.** Fig. 7 compares a representative WM rollout with the corresponding robot execution for the _Close microwave_ task. Both the imagined rollout and the physical execution successfully achieve the task goal. Notably, the final frame of the imagined sequence ( _t_ =90) exhibits visual artifacts, such as the handle becoming invisible. However, because our design utilizes the latent dynamics of the WM, it remains robust to these imperfect rollouts, as evidenced by the successful trial. Additional robot setup details and demonstrations are provided in Appendix B.4. 

**Remarks.** WORLD2ACT distills latent WM dynamics into a GR00T-N1.6 policy (Fig. 3a), improving simulation success across RoboCasa, LIBERO, and Bridge-SIMPLER over strong VLA and post-training baselines (Tables 1, 2, 3, 4) while exposing the fragility of pixel-space WM supervision: DreamGen degrades GR00T-N1.6-ft on LIBERO, suggesting pseudo-actions from decoded WM rollouts can be corrupted by visual artifacts (see failure-case study in Appendix F) ( **Q1** ). Furthermore, our residual policy and contrastive alignment are important: they increase the overlap between predicted-action latents and the reference-action/target-WM latent regions (Fig. 4) while reducing action-space error (Table 6), leading to higher downstream success rates (Table 5) ( **Q2** ). Our post-training paradigm scales favorably, showing consistent gains with increasing trajectory volume (Fig. 1c) and strong cross-task generalization (Fig. 3b) ( **Q3** ). Finally, real-world experiments show that our post-training method transfers effectively to physical robot deployments, improving success rates while remaining stable to imperfect synthetic rollouts (Figs. 6, 7) ( **Q4** ). 

## **5 Discussion** 

We introduced WORLD2ACT, a latent post-training framework that transfers generalizable dynamics priors from WMs to a GR00T-N1.6 policy, avoiding fragile pixel-level supervision. Experiments across benchmarks show consistent performance improvements over pixel-based post-training and other strong baselines, highlighting the promise of using WM latents as reusable dynamics priors. 

**Limitations.** WORLD2ACT has limitations. First, contact-rich, non-prehensile tasks [57] exhibit complex contact-driven dynamics that remain difficult for WMs to capture: small errors in object motion or contact evolution can compound in WM rollouts, making the resulting priors less transfer- 

8 

able. Second, real-world success remains modest, suggesting a persistent domain gap where complex physical dynamics are insufficiently captured by current WMs and VLAs [58, 59]. Third, our chunk-level video–action coupling uses temporal correspondence between imagined and executed trajectories, motivating future work relaxing this alignment for more flexible execution dynamics. 

## **References** 

- [1] GEAR Team. GR00T N1.6: An improved open foundation model for generalist humanoid robots, Dec. 2025. URL `https://research.nvidia.com/labs/gear/gr00t-n1_6/` . 

- [2] M. Wang, W. Jin, K. Cao, L. Xie, and Y. Hong. Contactgaussian-wm: Learning physicsgrounded world model from videos. _arXiv preprint arXiv:2602.11021_ , 2026. 

- [3] M. J. Kim, Y. Gao, T.-Y. Lin, Y.-C. Lin, Y. Ge, G. Lam, P. Liang, S. Song, M.-Y. Liu, C. Finn, et al. Cosmos policy: Fine-tuning video models for visuomotor control and planning. In _ICLR_ , 2026. 

- [4] Y. Zhang, C. Liu, X. Ren, H. Ni, Y. Zhang, S. Zhang, Z. Ding, J. Hu, H. Shan, J. Qi, et al. Bridging vlms and embodied intelligence with deliberate practice policy optimization. _arXiv preprint arXiv:2511.16602_ , 2025. 

- [5] M. Reuss. State of vla research at iclr 2026. `https://mbreuss.github.io/blog_post_ iclr_26_vla.html` , October 2025. Blog post. 

- [6] S. Tan, K. Dou, Y. Zhao, and P. Kraehenbuehl. Interactive post-training for vision-languageaction models. In _CVPRW_ , 2025. 

- [7] H. Li, P. Ding, R. Suo, Y. Wang, Z. Ge, D. Zang, K. Yu, M. Sun, H. Zhang, D. Wang, et al. Vla-rft: Vision-language-action reinforcement fine-tuning with verified rewards in world simulators. _arXiv preprint arXiv:2510.00406_ , 2025. 

- [8] J. Xiao, Y. Yang, X. Chang, R. Chen, F. Xiong, M. Xu, W.-S. Zheng, and Q. Zhang. Worldenv: Leveraging world model as a virtual environment for vla post-training. _arXiv preprint arXiv:2509.24948_ , 2025. 

- [9] J. Jang, S. Ye, Z. Lin, J. Xiang, J. Bjorck, Y. Fang, F. Hu, S. Huang, K. Kundalia, Y.-C. Lin, et al. Dreamgen: Unlocking generalization in robot learning through video world models. In _CoRL_ , 2025. 

- [10] Y. Guo, L. X. Shi, J. Chen, and C. Finn. Ctrl-world: A controllable generative world model for robot manipulation. In _ICLR_ , 2026. 

- [11] T. Poppi, B. Uzkent, A. Garg, L. Porto, G. Kessler, Y. Yang, M. Cornia, L. Baraldi, R. Cucchiara, and F. Schiffers. Countervid: Counterfactual video generation for mitigating action and temporal hallucinations in video-language models. _arXiv preprint arXiv:2601.04778_ , 2026. 

- [12] Y. Shang, X. Zhang, Y. Tang, L. Jin, C. Gao, W. Wu, and Y. Li. Roboscape: Physics-informed embodied world model. In _NeurIPS_ , 2025. 

- [13] Z. Liu, X. Deng, S. Chen, A. Wang, Q. Guo, M. Han, Z. Xue, M. Chen, P. Luo, and L. Yang. Worldweaver: Generating long-horizon video worlds via rich perception. In _NeurIPS_ , 2025. 

- [14] S. Gao, S. Zhou, Y. Du, J. Zhang, and C. Gan. Adaworld: Learning adaptable world models with latent actions. In _ICML_ , 2025. 

- [15] M. Assran, A. Bardes, D. Fan, Q. Garrido, R. Howes, M. Muckley, A. Rizvi, C. Roberts, K. Sinha, A. Zholus, et al. V-jepa 2: Self-supervised video models enable understanding, prediction and planning. _arXiv preprint arXiv:2506.09985_ , 2025. 

9 

- [16] C. Zhu, R. Yu, S. Feng, B. Burchfiel, P. Shah, and A. Gupta. Unified world models: Coupling video and action diffusion for pretraining on large robotic datasets. In _RSS_ , 2025. 

- [17] Y. Guo, J. Zhang, X. Chen, X. Ji, Y.-J. Wang, Y. Hu, and J. Chen. Improving vision-languageaction model with online reinforcement learning. In _ICRA_ , 2025. 

- [18] S. Nasiriany, A. Maddukuri, L. Zhang, A. Parikh, A. Lo, A. Joshi, A. Mandlekar, and Y. Zhu. Robocasa: Large-scale simulation of everyday tasks for generalist robots. In _RSS_ , 2024. 

- [19] B. Liu, Y. Zhu, C. Gao, Y. Feng, Q. Liu, Y. Zhu, and P. Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. In _NeurIPS_ , 2023. 

- [20] Z. Zhou, P. Atreya, Y. L. Tan, K. Pertsch, and S. Levine. Autoeval: Autonomous evaluation of generalist robot manipulation policies in the real world. In _CoRL_ , 2025. 

- [21] S. Gao, W. Liang, K. Zheng, A. Malik, S. Ye, S. Yu, W.-C. Tseng, Y. Dong, K. Mo, C.-H. Lin, et al. Dreamdojo: A generalist robot world model from large-scale human videos. _arXiv preprint arXiv:2602.06949_ , 2026. 

- [22] J. Yang, K. Lin, J. Li, W. Zhang, T. Lin, L. Wu, Z. Su, H. Zhao, Y.-Q. Zhang, L. Chen, et al. Rise: Self-improving robot policy with compositional world model. _arXiv preprint arXiv:2602.11075_ , 2026. 

- [23] J. Guo, X. Ma, Y. Wang, M. Yang, H. Liu, and Q. Li. Flowdreamer: A rgb-d world model with flow-based motion representations for robot manipulation. _RA-L_ , 2026. 

- [24] A. K. Jain, V. Mohta, S. Kim, A. Bhardwaj, J. Ren, Y. Feng, S. Choudhury, and G. Swamy. A smooth sea never made a skilled sailor: Robust imitation via learning to search. In _NeurIPS_ , 2025. 

- [25] R. Zheng, J. Wang, S. Reed, J. Bjorck, Y. Fang, F. Hu, J. Jang, K. Kundalia, Z. Lin, L. Magne, et al. Flare: Robot learning with implicit world modeling. In _CoRL_ , 2025. 

- [26] S. Ye, J. Jang, B. Jeon, S. Joo, J. Yang, B. Peng, A. Mandlekar, R. Tan, Y.-W. Chao, B. Y. Lin, et al. Latent action pretraining from videos. In _ICLR_ , 2025. 

- [27] Y. Guo, T. Lee, L. X. Shi, J. Chen, P. Liang, and C. Finn. Vlaw: Iterative co-improvement of vision-language-action policy and world model. _arXiv preprint arXiv:2602.12063_ , 2026. 

- [28] S. Huang, L. Chen, P. Zhou, S. Chen, Y. Liao, Z. Jiang, Y. Hu, P. Gao, H. Li, M. Yao, et al. Enerverse: Envisioning embodied future space for robotics manipulation. In _NeurIPS_ , 2025. 

- [29] S. Zhou, Y. Du, J. Chen, Y. Li, D.-Y. Yeung, and C. Gan. Robodreamer: Learning compositional world models for robot imagination. In _ICML_ , 2024. 

- [30] Y. Du, S. Yang, B. Dai, H. Dai, O. Nachum, J. Tenenbaum, D. Schuurmans, and P. Abbeel. Learning universal policies via text-guided video generation. In _NeurIPS_ , 2023. 

- [31] Q. Bu, Y. Yang, J. Cai, S. Gao, G. Ren, M. Yao, P. Luo, and H. Li. Learning to act anywhere with task-centric latent actions. In _RSS_ , 2025. 

- [32] Y. Chen, Y. Ge, W. Tang, Y. Li, Y. Ge, M. Ding, Y. Shan, and X. Liu. Moto: Latent motion token as the bridging language for learning robot manipulation from videos. In _ICCV_ , 2025. 

- [33] J. Zheng, J. Li, D. Liu, Y. Zheng, Z. Wang, Z. Ou, Y. Liu, J. Liu, Y.-Q. Zhang, and X. Zhan. Universal actions for enhanced embodied foundation models. In _CVPR_ , 2025. 

- [34] A. Jiang, Y. Gao, Y. Wang, Z. Sun, S. Wang, Y. Heng, H. Sun, S. Tang, L. Zhu, J. Chai, et al. Irl-vla: Training an vision-language-action policy via reward world model. _arXiv preprint arXiv:2508.06571_ , 2025. 

10 

- [35] A. K. Sharma, Y. Sun, N. Lu, Y. Zhang, J. Liu, and S. Yang. World-gymnast: Training robots with reinforcement learning in a world model. _arXiv preprint arXiv:2602.02454_ , 2026. 

- [36] H. He, Y. Zhang, L. Lin, Z. Xu, and L. Pan. Pre-trained video generative models as world simulators. In _AAAI_ , 2026. 

- [37] C. Zhang, T. Pearce, P. Zhang, K. Wang, X. Chen, W. Shen, L. Zhao, and J. Bian. What do latent action models actually learn? In _NeurIPS_ , 2025. 

- [38] F. Yang, D. Di, L. Tang, X. Zhang, L. Fan, H. Li, C. Wei, T. Su, and B. Ma. Chain of world: World model thinking in latent motion. In _CVPR_ , 2026. 

- [39] N. Agarwal, A. Ali, M. Bala, Y. Balaji, E. Barker, T. Cai, P. Chattopadhyay, Y. Chen, Y. Cui, Y. Ding, et al. Cosmos world foundation model platform for physical ai. _arXiv preprint arXiv:2501.03575_ , 2025. 

- [40] A. Blattmann, T. Dockhorn, S. Kulal, D. Mendelevitch, M. Kilian, D. Lorenz, Y. Levi, Z. English, V. Voleti, A. Letts, et al. Stable video diffusion: Scaling latent video diffusion models to large datasets. _arXiv preprint arXiv:2311.15127_ , 2023. 

- [41] A. v. d. Oord, Y. Li, and O. Vinyals. Representation learning with contrastive predictive coding. _arXiv preprint arXiv:1807.03748_ , 2018. 

- [42] T. Chen, S. Kornblith, M. Norouzi, and G. Hinton. A simple framework for contrastive learning of visual representations. In _ICML_ , 2020. 

- [43] T. Silver, K. Allen, J. Tenenbaum, and L. Kaelbling. Residual policy learning. _arXiv preprint arXiv:1812.06298_ , 2018. 

- [44] X. Li, K. Hsu, J. Gu, O. Mees, K. Pertsch, H. R. Walke, C. Fu, I. Lunawat, I. Sieh, S. Kirmani, et al. Evaluating real-world robot manipulation policies in simulation. In _CoRL_ , 2024. 

- [45] Y. Shen, F. Wei, Z. Du, Y. Liang, Y. Lu, J. Yang, N. Zheng, and B. Guo. Videovla: Video generators can be generalizable robot manipulators. _NeurIPS_ , 2025. 

- [46] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter, et al. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- [47] P. Intelligence, K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, et al. _pi_ 0 _._ 5: a vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 

- [48] S. Li, Y. Gao, D. Sadigh, and S. Song. Unified video action model. In _RSS_ , 2025. 

- [49] Y. Wang, S. Zheng, H. Luo, W. Zhang, H. Yuan, C. Xu, H. Xu, Y. Feng, M. Yu, Z. Kang, et al. Rethinking visual-language-action model scaling: Alignment, mixture, and regularization. _arXiv preprint arXiv:2602.09722_ , 2026. 

- [50] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi, et al. Openvla: An open-source vision-language-action model. In _CoRL_ , 2024. 

- [51] M. J. Kim, C. Finn, and P. Liang. Fine-tuning vision-language-action models: Optimizing speed and success. In _RSS_ , 2025. 

- [52] J. Bjorck, F. Casta˜neda, N. Cherniadev, X. Da, R. Ding, L. Fan, Y. Fang, D. Fox, F. Hu, S. Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

11 

[53] NVIDIA. Physicalai-robotics-gr00t-x-embodiment-sim, 2025. URL `https://huggingface.co/datasets/nvidia/ PhysicalAI-Robotics-GR00T-X-Embodiment-Sim` . Version: be164f2 (commit date: 2025-12-09). License: CC BY 4.0. Accessed: 2026-02-21. 

- [54] S.-W. Lee, X. Kang, B. Y. Yang, and Y.-L. Kuo. Class: Contrastive learning via action sequence supervision for robot manipulation. In _CoRL_ , 2025. 

- [55] N. Saunshi, O. Plevrakis, S. Arora, M. Khodak, and H. Khandeparkar. A theoretical analysis of contrastive unsupervised representation learning. In _ICML_ , 2019. 

- [56] P. Wu, Y. Shentu, Z. Yi, X. Lin, and P. Abbeel. Gello: A general, low-cost, and intuitive teleoperation framework for robot manipulators. In _IROS_ , 2024. 

- [57] Y. Shirai, K. Ota, D. K. Jha, and D. Romeres. Learning non-prehensile manipulation with force and vision feedback using optimization-based demonstrations. _RA-L_ , 2026. 

- [58] S. Motamed, L. Culp, K. Swersky, P. Jaini, and R. Geirhos. Do generative video models understand physical principles? In _WACV_ , 2026. 

- [59] E. Yu, H. Lv, J. Sun, K. Lin, R. Zhang, Y. Shi, Y. Chen, Z. Chen, Z. Zhang, F. Jia, et al. Dm0: An embodied-native vision-language-action model towards physical ai. _arXiv preprint arXiv:2602.14974_ , 2026. 

- [60] D. Guo, D. Yang, H. Zhang, et al. Deepseek-r1 incentivizes reasoning in llms through reinforcement learning. _Nature_ , 645:633–638, 2025. doi:10.1038/s41586-025-09422-z. 

- [61] J. Huang, Z. Ye, X. Hu, T. He, G. Zhang, S. Shi, J. Bian, and L. Jiang. Live: Long-horizon interactive video world modeling. _arXiv preprint arXiv:2602.03747_ , 2026. 

- [62] Y. HaCohen, N. Chiprut, B. Brazowski, D. Shalem, D. Moshe, E. Richardson, E. Levin, G. Shiran, N. Zabari, O. Gordon, et al. Ltx-video: Realtime video latent diffusion. _arXiv preprint arXiv:2501.00103_ , 2024. 

- [63] B. Wu, C. Zou, C. Li, D. Huang, F. Yang, H. Tan, J. Peng, J. Wu, J. Xiong, J. Jiang, et al. Hunyuanvideo 1.5 technical report. _arXiv preprint arXiv:2511.18870_ , 2025. 

- [64] T. Wan et al. Wan: Open and advanced large-scale video generative models. _arXiv preprint arXiv:2503.20314_ , 2025. 

- [65] S. Bai, K. Chen, X. Liu, J. Wang, W. Ge, S. Song, K. Dang, P. Wang, S. Wang, J. Tang, et al. Qwen2.5-vl technical report. _arXiv preprint arXiv:2502.13923_ , 2025. 

- [66] H. Bansal, C. Peng, Y. Bitton, R. Goldenberg, A. Grover, and K.-W. Chang. Videophy-2: A challenging action-centric physical commonsense evaluation in video generation. _arXiv preprint arXiv:2503.06800_ , 2025. 

12 

This appendix provides additional details and extended evaluations to support the main paper. The material is organized as follows: 

- **Appendix A** reports additional results on the simulation benchmarks in the main paper. 

- **Appendix B** provides experimental details for WORLD2ACT, including Stage 1 pretraining, cross-task evaluation, real-world deployment, and inference-speed analysis. 

- **Appendix C** specifies the network architectures and hyperparameters for our proposed policy components. 

- **Appendix D** describes the data construction pipeline for world-model training, including atomic-skill segmentation, LLM-based synchronization, dataset statistics, and multi-view stitching. 

- **Appendix E** details the training configurations and the evaluation of the video diffusion world models used in our framework. 

- **Appendix F** analyzes representative failure cases, including world-model hallucinations and transfer failures. 

- **Appendix G** and **Appendix H** discuss the broader impact of our work and provide further clarifications on related literature, respectively. 

## **A Supplementary Experiment Results** 

In this appendix section, we provide additional experimental results on LIBERO, RoboCasa, and Bridge-SIMPLER. Beyond the main backbone studied in the paper, we evaluate WORLD2ACT on Cosmos Policy, a strong VLA with built-in world-modeling capability. This experiment tests whether WORLD2ACT can still improve policies that already incorporate WM structure. 

Table 7: **Detailed LIBERO results.** 

|**Baselines**|**Spatial**|**Object**|**Goal**|**Long**|**Average**|
|---|---|---|---|---|---|
|_π_0 [46]|0.968|0.988|0.958|0.852|0.942|
|_π_0_._5 [47]|0.988|0.982|0.980|0.924|0.969|
|OpenVLA-OFT [51]|0.976|0.984|0.979|0.945|0.971|
|UniVLA [31]|0.965|0.968|0.956|0.920|0.952|
|CoWVLA [38]|0.972|0.978|0.946|0.928|0.956|
|Cosmos Policy [3]|0.981|1.000|0.982|0.976|0.985|
|Cosmos Policy [3] + WORLD2ACT(Ours)|0.980|1.000|0.983|0.980|**0.986**|
|GR00T-N1.6-ft [1]|0.977|0.984|0.975|0.943|0.970|
|GR00T-N1.6-ft [1] + DreamGen [9]|0.991|0.826|0.992|0.876|0.921|
|GR00T-N1.6-ft [1] + WORLD2ACT(Ours)|0.995|1.000|0.988|0.940|**0.981**|


**Performance on LIBERO.** Table 7 summarizes results across the spatial, object, goal, and longhorizon LIBERO suites. On Cosmos Policy, WORLD2ACT improves the average success rate from 98.5% to 98.6%. Although the absolute gain is modest, Cosmos Policy already achieves near-perfect performance on LIBERO, a near-saturated benchmark, making further improvements difficult. The positive gain therefore suggests that WORLD2ACT can further improve performance even when the base policy already benefits from world-modeling capability. 

**Performance on RoboCasa.** Table 8 reports the corresponding results on RoboCasa. Consistent with the LIBERO results, WORLD2ACT improves Cosmos Policy from 65.7% to 66.3%. Again, the gain is moderate, but this is precisely the regime of interest: Cosmos Policy already has WM capability, yet post-training with WORLD2ACT still increases downstream task success. This result supports the view that WORLD2ACT is complementary to existing WM-capable VLAs rather than only being useful for policies without an explicit world-modeling component. 

13 

Table 8: **Extra RoboCasa results.** 

|**Baselines**|**SR**|
|---|---|
|Cosmos Policy [3]|0.657|
|Cosmos Policy [3] + WORLD2ACT(Ours)|**0.663**|
|GR00T-N1.6-ft [1]|0.701|
|GR00T-N1.6-ft [1] + DreamGen [9]|0.705|
|GR00T-N1.6-ft [1] + WORLD2ACT(Ours)|**0.726**|


Overall, the supplementary results across LIBERO and RoboCasa reinforce our main claim: using a world model to post-train a VLA can continue to improve policy performance, even when the underlying VLA already has WM capability. 

Table 9: **Detailed Bridge-SIMPLER results.** 

|**Baselines**|**Put Spoon**<br>**on Towel**|**Stack Green**<br>**on Yellow**|**Put Carrot**<br>**on Plate**|**Put Eggplant**<br>**in Basket**|**Open**<br>**Drawer**|**Close**<br>**Drawer**|**Put Eggplan**<br>**in Sink**|**t**<br>**Average**|
|---|---|---|---|---|---|---|---|---|
|_π_0 [46]|0.292|0.000|0.166|0.624|0.676|0.480|0.124|0.337|
|OpenVLA [50]|0.000|0.000|0.000|0.042|0.644|0.036|0.000|0.103|
|OpenVLA-OFT [51]|0.342|0.308|0.292|0.726|0.338|0.742|0.320|0.438|
|GR00T-N1.6-ft [1]|0.734|0.044|0.624|0.372|0.916|0.984|0.358|0.576|
|GR00T-N1.6-ft [1] + DreamGen [9]|0.718|0.048|0.646|0.424|0.928|0.976|0.342|0.583|
|GR00T-N1.6-ft [1] + WORLD2ACT(Ours)|0.768|0.042|0.664|0.386|0.916|0.990|0.362|**0.590**|


**Detailed Bridge-SIMPLER Results.** Table 9 reports the per-task breakdown on the AutoEval Bridge-SIMPLER [20] suite, which extends the original WidowX-based SIMPLER Bridge setup with additional drawer-manipulation tasks and a sink-placement task. This table complements the LIBERO and RoboCasa supplementary results by focusing on the WidowX-based Bridge-SIMPLER evaluation rather than an additional Cosmos Policy backbone study. WORLD2ACT achieves the best average SR, improving GR00T-N1.6-ft from 57 _._ 6% to 59 _._ 0% and outperforming DreamGen (58 _._ 3%). 

## **B Experimental Details** 

In this section, we provide implementation details that support the empirical evaluations in the main paper. Specifically, we describe Stage 1 pretraining, cross-task evaluation, real-world deployment, and inference-speed analysis for WORLD2ACT. 

### **B.1 Stage 1 Pretraining Details** 

To train the action and video adapters _B_ a and _B_ v, we start with a frozen world model _W_ that has been finetuned on our processed datasets (see Appendix D). We use synchronized expert demonstrations consisting of the video **Q** _i_ , instruction _ℓi_ , and ground-truth action sequence **a** _i,_ gt. Each demonstration video is encoded by the frozen WM video-VAE encoder to obtain the corresponding latent visual-dynamics trajectory: 


where **V** _i_<sup>gt=</sup><sup>_{V_</sup> _i,t_<sup>gt</sup><sup>_}_</sup> _t_<sup>_T_</sup> =1<sup>lies in the same structured video-VAE latent space used by the world model.</sup> These encoded video latents serve as the video-side anchors for Stage 1 alignment. Since **Q** _i_ and **a** _i,_ gt come from the same demonstration, each video-latent chunk is temporally aligned with the corresponding expert action chunk. 

We map the video-latent chunks into the shared latent space using the video adapter, _zi,t_<sup>v=</sup><sup>_B_v(</sup><sup>_V_</sup> _i,t_<sup>gt)</sup><sup>_,_</sup> and map the corresponding ground-truth action chunks _a_ ¯<sup>gt</sup> _i,t_<sup>intothesamespaceusingtheaction</sup> adapter, _zi,t_<sup>a=</sup><sup>_B_a(¯</sup><sup>_a_gt</sup> _i,t_<sup>)</sup><sup>_._Stage1trainingoptimizestheactionreconstructionloss</sup><sup>_L_recon.andthe</sup> 

14 

video–action contrastive loss _L_ contrastive, as described in subsection 3.2, for 30K steps. We do not decode **V** _i_<sup>gtor use pixel-space video reconstruction as a training signal.</sup> 

During minibatch construction, we use a batch size _B_ = 16 with a hard-negative ratio of 0 _._ 25, where hard negatives are drawn from different demonstrations of the same task and the remaining negatives are drawn from different tasks. 


Figure 8: **Stage 1 pretraining losses.** Training curves for _L_ recon. and _L_ contrastive (defined in subsection 3.2 of our main paper) over 30K steps. Both losses converge stably, demonstrating effective cross-modal alignment between the video and action representations. 

As illustrated in Figure 8, both losses converge stably under our configuration: _L_ recon. stabilizes at approximately 0.01, while _L_ contrastive plateaus near 0.10. This provides optimization evidence that the action latents preserve low-level kinematic structure while the video and action modalities become well-aligned in the shared latent space. 

### **B.2 Post-Training Data Synthesis** 

We use a Cosmos-Predict2 world model [39], finetuned on atomic-skill datasets as described in Appendix D, to provide target latent rollouts for Stage 2 post-training of WORLD2ACT. For each of the RoboCasa, LIBERO, and Bridge-SIMPLER benchmarks, we sample 1,000 scene initializations, each consisting of an initial observation and a language instruction. This yields roughly 3,000 posttraining rollouts in total. We ensure that the post-training scene initializations are disjoint from the evaluation scenes to prevent test leakage. The synthesis procedure is skill-compositional, as illustrated in Figure 9. 

During post-training, the WM imagination branch and VLA control branch run in parallel from the same initial scene and instruction. In the WM branch, we first prompt DeepSeek [60] to decompose the high-level instruction into an ordered sequence of atomic skill descriptions defined in a manually specified schema. Each atomic skill description specifies a short-horizon manipulation primitive, such as picking up an object, moving it to a target location, or placing it under a dispenser. Cosmos-Predict2 then generates one short video segment for each atomic skill prompt, autoregressively conditioning each segment on the final frame of the previous one. The resulting segments are concatenated into a long-horizon imagined rollout, and we retain the corresponding pre-decoding video latents as the WM target trajectory. In the VLA branch, the current augmented policy is rolled out from the same initial scene. WORLD2ACT post-trains the residual policy by aligning the policy action-latent trajectory with the parallel WM target latent trajectory, without using decoded pixels, simulator rewards, or expert action labels. 

For analyses that require ground-truth action targets, such as Fig. 4 and Table 6, we separately use the _Human_ split of RoboCasa, which provides expert action annotations. We sample 50 scenes from this split and report the mean-squared error averaged across these scenes. This evaluation set is used only for action-space analysis and is distinct from the synthetic rollouts used for post-training. 

15 


Figure 9: **Post-training rollout synthesis.** Given an initial frame and a high-level instruction, an LLM decomposes the instruction into an ordered list of atomic skill prompts. The world model generates one video segment per skill, using the final frame of each segment as the visual condition for the next skill. The resulting video segments are concatenated to form a long-horizon synthetic rollout. We retain the pre-decoding video latents from the world model as post-training supervision for WORLD2ACT. The atomic-skill data used to train the world model are described in Appendix D. 

### **B.3 Cross-Task Generalization** 

Table 10 presents the train-test split for the cross-task generalization experiment (Fig. 3b of the main paper). We designate _Pick and Place_ (PnP) as the primary held-out task suite for evaluating zeroshot transfer under a significant distributional shift. While PnP is never observed as an explicit task during post-training, the robot frequently encounters directly relevant interaction skills, for example, reaching, grasping, lifting, and placement-like motions, which are implicitly learned through related tasks like _Open Door_ or _Turn Off Microwave_ . Our experiment is designed to reuse these transferable skills to synthesize behavior in novel task compositions, making PnP a learnable but non-trivial generalization target. At 12 seen training tasks, WORLD2ACT improves cross-task success rate over the corresponding vanilla policies by 2 _._ 4% for GR00T-N1.6-base and 1 _._ 1% for Cosmos Policy. 

Table 10: **Cross-task generalization experiment splits.** 

|**Train Tasks**|**Test Tasks**|
|---|---|
|CoffeeSetupMug|PnPCounterToCab|
|CoffeeServeMug|PnPCabToCounter|
|CoffeePressButton|PnPCounterToSink|
|OpenSingleDoor|PnPSinkToCounter|
|OpenDoubleDoor|PnPCounterToMicrowave|
|CloseSingleDoor|PnPMicrowaveToCounter|
|CloseDoubleDoor|PnPCounterToStove|
|OpenDrawer|PnPStoveToCounter|
|CloseDrawer|TurnOnSinkFaucet|
|TurnOnMicrowave|TurnOffSinkFaucet|
|TurnOffMicrowave|TurnSinkSpout|
|TurnOffStove|TurnOnStove|


### **B.4 Real-World Experiments** 

To evaluate our method’s sim-to-real transfer capabilities, our physical evaluation suite is designed to replicate simulation tasks from the RoboCasa and LIBERO benchmarks closely. We define success for the real-world tasks as follows: (i) _Pick and place cup_ : The robot must pick the cup and place it stably on the plate in a single, continuous attempt. (ii) _Pick up bowl_ : The robot must secure the bowl and return to its home configuration (see Figure 5 in the main paper) while maintaining a stable lift. (iii) _Close microwave_ : A trial is successful when the microwave door is pushed closed, and its magnet fully engages. We provide additional demonstrations in our video to illustrate worldmodel rollouts in the real-world Franka setup, highlighting the execution of our approach across three distinct physical tasks, demonstrating robust transfer from the WM to real-world control. 

An important detail for the _Pick and place cup_ task is our use of atomic-skill segmentation, which aligns with our post-training data construction to ensure consistency during transfer from WM to 

16 


Figure 10: **Additional t-SNE visualizations.** We provide extra qualitative results on PnPCounterToCab and TurnOnStove. Consistent with the _OpenDrawer_ results in Figure 4, WORLD2ACT yields predicted-action latent distributions that better overlap with the reference-action and target-WM latent regions, indicating improved alignment while remaining compatible with the expert action manifold. 

VLA. The task is segmented into two atomic skills: “pick cup” and “place cup.” To count as a single success, the robot must complete both skills in a single shot. When training the WM and our WORLD2ACT, we do not train the full pick-and-place behavior as a one-shot sequence; instead, we collect demonstrations for the _Pick_ and _Place_ skills separately and train them as two atomic skills. 

### **B.5 Additional Latent Visualizations** 

We additionally provide t-SNE visualizations for two more tasks, _PnPCounterToCab_ and _TurnOnStove_ , complementing the _OpenDrawer_ analysis in Figure 4. We follow the same visualization protocol as in the main paper: reference expert actions correspond to ground-truth actions from held-out demonstrations, target-WM latents correspond to the target world-model representations, and predicted-action latents are produced by the learned policy. For each task, we sample 50 heldout scenes from the _Human_ split of RoboCasa, which provides expert action annotations. As shown in Figure 10, WORLD2ACT produces predicted-action latents that are more consistently co-located with the reference-action and target-WM latent regions than the baseline. These additional visualizations suggest that the latent alignment observed on _OpenDrawer_ is not task-specific, and that WORLD2ACT preserves compatibility with the expert action manifold across manipulation tasks with different object interactions and scene dynamics. 

### **B.6 Inference Speed Analysis** 

Table 11 compares the inference latency of the baseline VLAs against those integrated with our WORLD2ACT. The results show that our method adds minimal computational overhead. When applied to GR00T-N1.6-ft, WORLD2ACT maintains a rate above 250 Hz. This speed facilitates 

17 

Table 11: **Inference speed comparison.** We report the inference speed on RoboCasa using an NVIDIA RTX 4090. We measure speed by the time required to predict an action from an observation. 

|Model<br>Inference Speed (Hz) (_↑_)|Per Action (ms) (_↓_)|
|---|---|
|GR00T-N1.6-ft [1]<br>274.1|3.6|
|GR00T-N1.6-ft + WORLD2ACT(Ours)<br>251.9|4.0|
|Cosmos Policy [3]<br>20.8|48.1|
|Cosmos Policy + WORLD2ACT(Ours)<br>20.5|48.8|


physical applications, as demonstrated by our robot experiments in subsection 4.3 of the main paper. Cosmos Policy operates at a lower rate of about 20.8 Hz per step because it uses a joint representation for video, language, and action. Even so, including WORLD2ACT drops the speed of Cosmos Policy by just 1.5%. This high-dimensional joint latent space likely accounts for the incremental performance gains observed with Cosmos Policy in the Appendix A, as the model’s high-dimensional embeddings already capture significant cross-modal correlations. 

Table 12: **Architectural details of the policy components.** In our implementation, _A_ = 12 for RoboCasa and _A_ = 7 for LIBERO, Bridge-SIMPLER and real Franka Robot, _M_ = 4, _D_ = 32, and _D_ proprio = 53. Input images are 256 _×_ 256. The Attention Module processes _N_ src = 3 tokens: the visual feature, the latent base action from _B_ a, and the proprioception state. The video latent resolution is 16 _×_ 60 _×_ 104, following the Cosmos-Predict-2 [39] implementation. 

|**Module**|**Tensor Mapping**|**Architecture**|
|---|---|---|
|**Action Adapter**_B_a<br>(Action Encoder)|R<sup>_A×M _</sup>_→_R<sup>_D_</sup>|Flatten, FC(_A × M_, 128), GELU<br>FC(128, 64), GELU<br>FC(64,_D_)|
|**Video Adapter**_B_v<br>(Video Encoder)|R<sup>_C×H×W _</sup>_→_R<sup>_D_</sup>|Conv2D(_C_, 64,_k_ = 3_, s_= 2_, p_= 1), GroupNorm, GELU<br>Conv2D(64, 128,_k_ = 3_, s_= 2_, p_= 1), GroupNorm, GELU<br>AdaptiveAvgPool2D((1, 1)), Flatten, FC(128,_D_)|
|**Action Decoder**_D_a|R<sup>_D _</sup>_→_R<sup>_A×M_</sup>|FC(_D_, 64), GELU<br>FC(64, 128), GELU<br>FC(128,_A × M_)|
|**Residual Network**_f _<sup>_θ_</sup>|||
|_State Encoder_<br>_Visual Encoder_<br>_Transformer Module_|R<sup>_D_proprio</sup> _→_R<sup>_D_</sup><br>R<sup>3</sup><sup>_×Himg×Wimg _</sup>_→_R<sup>_D_</sup><br>R<sup>_N_src</sup><sup>_×D _</sup>_→_R<sup>_N_src</sup><sup>_×D_</sup>|FC(_D_proprio, 128), ReLU, FC(128,_D_), LayerNorm<br>Conv2D(3, 16,_k_ = 8_, s_= 4_, p_= 0), ReLU<br>Conv2D(16, 32,_k_ = 4_, s_= 2_, p_= 0), ReLU<br>Conv2D(32, 32,_k_ = 3_, s_= 2_, p_= 0)<br>Flatten, FC(6272,_D_), LayerNorm<br>Self-Attention (2 layers, 4 heads,_d_model =_D_)|


## **C Network Specifications** 

Following the notation established in the main paper, we provide the detailed architectural specifications for the action adapter _B_ a, video adapter _B_ v, action decoder _D_ a, and the residual network _f_<sup>_θ_</sup> in Table 12. As defined previously, _M_ denotes the action chunk size, _D_ the latent hidden dimension, and _C × H × W_ the resolution of the video latents per chunk. Additionally, we define _D_ proprio as the robot proprioception state dimension, _A_ as the action dimension, and 3 _× H_ img _× W_ img as the input image resolution. For convolutional layers, parameters are denoted as (input ~~c~~ hannels, output ~~c~~ hannels, _k_ =kernel ~~s~~ ize, _s_ =stride, _p_ =padding). For fully connected layers, we use FC(input ~~f~~ eatures, output ~~f~~ eatures). 

**Residual Policy Architecture.** We provide the architectural details of the residual policy used in Stage 2. At each chunk boundary, the frozen VLA _π_ base predicts a base action chunk ¯ _a_ base _,t_ from 

18 

_a_ ¯base _,t_ = _π_ base( _st, ℓ_ ) _._ (5) 

the current state _st_ and instruction _ℓ_ : 

Since residual corrections are learned in the Stage-1 action-latent space, we embed this base action chunk using the frozen action adapter _B_ a to obtain the base action-latent token: 


The residual policy _f_<sup>_θ_</sup> is conditioned on the current state _st_ and the base action latent _z_ base<sup>a</sup> _,t_<sup>.We</sup> encode visual observations in _st_ using a CNN and robot proprioceptive observations using an MLP, yielding a set of observation tokens _{_ **x**<sup>(1)</sup> _, . . . ,_ **x**<sup>(</sup><sup>_n_)</sup> _}_ . We concatenate the action-latent token with the observation tokens, _{_ **x**<sup>(0)</sup> _,_ **x**<sup>(1)</sup> _, . . . ,_ **x**<sup>(</sup><sup>_n_)</sup> _}_ , and process the resulting token sequence with a selfattention Transformer, producing contextualized features _{_ **h**<sup>(0)</sup> _,_ **h**<sup>(1)</sup> _, . . . ,_ **h**<sup>(</sup><sup>_n_)</sup> _}_ . An MLP head applied to the contextualized action token **h**<sup>(0)</sup> predicts the latent residual: 


The refined action latent is computed as 


and decoded by the frozen action decoder: 


During Stage 2, only the parameters of _f_<sup>_θ_</sup> are updated; the base VLA, action adapter _B_ a, video adapter _B_ v, and action decoder _D_ a remain frozen. 

## **D Data for World Model** 

Current video world models struggle with long-video generation because they are commonly trained on fixed-length clips, while robotic executions vary widely in duration [61]. This mismatch can make training unstable for long-horizon manipulation trajectories, where different tasks may contain substantially different temporal structures. To reduce this variance, we use an automatic atomic-skill segmentation pipeline that decomposes demonstrations into shorter action segments paired with lowlevel language prompts. This increases the uniformity of world-model training videos and provides temporally focused clips for learning robot-object interaction dynamics. This section details the data decomposition pipeline, validates the resulting datasets, and describes the additional formatting used for world-model training. 


Figure 11: **Atomic-skill data construction for world-model training.** We segment each demonstration using gripper-state changes, decompose the global instruction into atomic skill prompts with an LLM, and synchronize sub-videos with prompts through schema-based chronological alignment. 

### **D.1 Data Processing and Synchronization** 

Figure 11 summarizes our atomic-skill data construction pipeline. Given a long-horizon demonstration, we first identify candidate interaction boundaries from the gripper aperture. Let _wt_ denote the 

19 

gripper width at time _t_ , and let _w_ 0 denote the calibrated fully open width at the start of an episode. We define the closure signal as _δt_ = _w_ 0 _− wt_ , where _δt ≈_ 0 indicates that the gripper remains fully open, while larger values indicate increasing closure. Each frame is classified into an event _Et ∈{contact, non-contact}_ , assigning _Et_ = _contact_ if _δt ≥_ ∆, and _Et_ = _non-contact_ otherwise. Candidate sub-video segments are then constructed around complete action cycles, starting from _non-contact_ frames and ending at the completion of a corresponding _contact_ event. 

To assign language labels to these visual segments, we use DeepSeek [60] to decompose each global, high-level instruction into an ordered sequence of atomic skill prompts. We first manually define task schemas for each simulator. These schemas provide a standardized skill vocabulary for each task family, ensuring consistent video-language synchronization across environments. Given a global instruction, a task schema, and a set of _ℓ_ detected contact indices, the LLM aligns valid indices to schema steps in chronological order. Ideally, _ℓ_ matches the number of steps in the corresponding schema; for example, a “pick and place” task requires two steps: “pick”, then “place”. 

Because raw contact indices can contain noise, such as duplicate triggers or temporally clustered detections, we explicitly instruct the LLM to identify and filter out false positives. The model aligns the remaining valid indices chronologically with the schema steps. To prevent hallucinated frame numbers, the LLM is instructed to use only the provided indices. If an execution contains fewer valid indices than required by the schema, the LLM flags the missing steps, and we discard the incomplete sequence. The remaining valid indices define the final sub-video boundaries, and their aligned schema steps provide the corresponding low-level prompts. This produces short-horizon sub-videos paired with atomic language commands for world-model training. 

**LLM Prompt Template.** The system prompt used for schema-based skill alignment is shown below. We ask the model to output strict JSON, provide a brief explanation for its filtering and alignment decisions, and return the final mapping from valid contact indices to atomic skill labels. 

```
Youarearoboticvideodatasetprocessingassistant.Yououtputstrict
JSON.
```

```
OBJECTIVE:
Youwillreceiveavideotaskwithdetectedtimestampindices.Your
goalistoaligntheseindicestothecorrectschemasteps,filtering
outsensornoise.
```

```
LOGICFLOW:
1.ANALYZE:ComparetheUserCaptionagainsttheDetectedIndices.
2.FILTER:IdentifyindicesthatarelikelyNOISE,HESITATION,or
DUPLICATES.
3.ALIGN:MaptheSchemaStepstothevalidindiceschronologically.
4.HANDLEMISSING:
-IfthereareFEWERindicesthansteps,flagit.
-IfthereareMOREindicesthansteps,markextrasasNOISE.
-DONOTinventnewframenumbers.
OUTPUTFORMAT:
ReturnaJSONobjectwitha"reasoning"fieldandan"alignment"field.
EXAMPLE:
UserInput:
Task:"CoffeeSetupMug",Indices:[116,230,235],Schema:["pick",
"place"],
Caption:"Pickthemugandplaceitunderthecoffeedispenser."
Output:
{
"reasoning":"Thecaptionconfirmsbothpickandplaceactions.Index
116alignswith‘pick’.Indices230and235aretemporallyclose;
235isfilteredassensornoiseduringthe‘place’execution.",
```

20 

```
"alignment":{
"116":"pick(mug)",
"230":"place(mug)"
}
}
```

For each demonstration, we input the global instruction, task schema, and detected contact indices into the prompt. We then extract the resulting alignment from the model output and use the aligned schema steps as atomic skill labels for the processed world-model training datasets. 

### **D.2 Validating Atomic-Skill Decomposition** 

Accurate pairing between video segments and prompts is essential for training a reliable world model. We therefore evaluate both cross-modal synchronization quality and the resulting distribution of video lengths. The goal is to verify that the decomposition process produces well-aligned videolanguage pairs while mitigating the long-tail duration issues present in the original demonstrations. 


Figure 12: **Video-length distribution.** Across RoboCasa and LIBERO, decomposed skills exhibit shorter mean length and a more concentrated distribution than full sequences, improving stability for world-model training on variable-duration robotic demonstrations. 

Our pipeline achieves synchronization rates, defined as the successful one-to-one matching between segmented sub-videos and generated atomic prompts, of 96 _._ 2% on the processed RoboCasa data and 86 _._ 9% on the processed LIBERO data. These results demonstrate high alignment rates between visual segments and language labels. Infrequent failures are largely due to rare gripper noise or non-prehensile interactions [57], such as using the arm rather than the gripper to close a door. 

Figure 12 shows that skill decomposition reshapes the original high-variance, long-tailed videolength distributions ( _gray_ ) into more concentrated, approximately unimodal distributions ( _red_ ). Specifically, the density around the median increases by 17% for the processed RoboCasa data and 72% for the processed LIBERO data, indicating that a much larger fraction of training clips fall within a uniform temporal duration. This mass concentration yields a more consistent prediction horizon, reducing distributional variance and stabilizing world-model training under variable task durations. 

### **D.3 Dataset Statistics** 

Using the optimized closure threshold ∆= 0 _._ 005m, our processed RoboCasa dataset contains 114,192 video sequences, compared to 67,593 sequences in the original RoboCasa dataset. For LIBERO, our processed dataset contains 11,782 video sequences, compared to 2,007 sequences in the original LIBERO dataset. This growth is a direct consequence of the skill-based segmentation pipeline, which extracts multiple atomic skill segments from each long-horizon trajectory. The resulting datasets provide substantially more short-horizon video-language pairs for world-model 

21 

training while preserving chronological consistency with the original demonstrations. For BridgeSIMPLER simulator, the expert demonstration videos have relatively uniform lengths, so we directly use the simulator’s original expert demonstrations without additional segmentation. 

### **D.4 Multi-view Stitching** 

Following Cosmos-Predict2 [39], we stitch multi-view observations into a single composite layout for each video frame to enforce geometric consistency and enhance the model’s spatial understanding. Specifically, the RGB observations are arranged into a 2 _×_ 2 grid layout. For RoboCasa, the grid consists of the left, right, and wrist camera views in the top-left, top-right, and bottom-left panes, respectively, with the bottom-right pane left black. For LIBERO, the primary and wrist camera views occupy the top-left and top-right panes, while the entire bottom row remains black. Figure 13 illustrates these configurations. 


(a) LIBERO layout and rendered sample. 


Figure 13: **Multi-view stitching strategies.** To preserve geometric context, observations from multiple cameras are spatially arranged into a unified 2 _×_ 2 grid. For each simulation environment, we illustrate the camera mapping template on the left and an example stitched observation on the right. **(a)** In LIBERO, the primary and wrist cameras occupy the top row, with the bottom row black-padded. **(b)** In RoboCasa, the left, right, and wrist views are mapped to the top-left, top-right, and bottom-left quadrants, respectively. 

## **E World Model Training and Evaluation** 

### **E.1 Backbones** 

We finetune four recent, high-performing video diffusion backbones: LTX-Video [62], HunyuanVideo-1.5 [63], Wan2.2 [64], and Cosmos-Predict2 [39]. Each model is trained for 10K steps on our processed datasets. To ensure a fair comparison, we follow the model sizes and training configurations recommended by the original authors. Specifically, most models adopt LoRA as the standard finetuning strategy, whereas Cosmos-Predict2 uses full finetuning for its 2B variant; we therefore follow this protocol. For the LoRA-based models, we use the 13B version of LTXVideo with rank 128, the 5B version of Wan2.2 with rank 32, and the 480P-I2V configuration of HunyuanVideo-1.5 with rank 8. 

We additionally train a Cosmos-Predict2 model on the original RoboCasa dataset using the standard _MG_ split [18]. We refer to this model as Base-WM, and denote the variant trained on our processed atomic datasets as Skill-WM. All models are trained in a distributed setup using eight AMD Instinct MI210 GPUs, each with 64 GB of VRAM. 

### **E.2 Evaluation Protocol** 

We evaluate WM backbone generative quality following the protocol in [9] using 100 representative Pick and Place trajectories in RoboCasa. We evaluate all baselines on the _Human_ split, a held-out set disjoint from the _MG_ split [18], which is used for finetuning. We assess performance using two key metrics: **Instruction Following (IF)** , measured via Qwen-VL-2.5 [65] to check alignment between 

22 

text prompts and visual results, and **Physical Alignment (PA)** , measured via VideoCon-Physics [66] to evaluate the consistency of physical interactions in generated videos. 

### **E.3 Quantitative Results** 

Table 13 shows Cosmos-Predict2 achieves the best IF and PA performance thanks to its pretraining on extensive robotic datasets that provide more robust spatiotemporal priors for manipulation tasks compared to other generic backbones [39]. Consequently, we choose it as the main backbone throughout the paper. Furthermore, training Cosmos-Predict2 on our atomic-skill-segmented data significantly improves both IF and PA metrics compared to the base backbone. We attribute this to the distribution of the training data; standard trajectories in robotics datasets often vary in duration, biasing toward simpler, shorter sequences while ignoring longer-horizon videos. By atomizing data into discrete skills, the **length distribution during training becomes more uniform** (as visualized in Figure 12). This allows the model to learn robust transitions and complex contact dynamics without being overwhelmed by the temporal noise of long-horizon trajectories. 

Table 13: **Quantitative comparison of video diffusion backbones.** The Cosmos-Predict2 model trained on our atomic-skill data significantly outperforms baselines in both instruction following and physical alignment. Our results are consistent with Jang _et al._ <u>[9].</u> 

|Video Diffusion Backbone|IF (_↑_)|PA (_↑_)|
|---|---|---|
|LTX-Video [62]|7.7|40.1|
|HunyuanVideo-1.5 [63]|8.3|44.8|
|Wan2.2 [64]|20.5|56.9|
|Cosmos-Predict2 [39] (Base data)|29.6|60.5|
|Cosmos-Predict2 (Ours, atomic-skill data)|**35.3**|**65.4**|


### **E.4 Qualitative Analysis: Where Atomic-Skill Segmentation Matters** 

Our qualitative study highlights the critical role of temporal decomposition in multi-step tasks. As illustrated by the final frames in Figure 14, the Base-WM frequently encounters “mid-task” failure modes, in which the generation stalls or fails to ground the target object. This instability is a direct result of accumulated error when the base model attempts to generate excessively long video sequences without explicit grounding of atomic skills. In contrast, the WM trained on atomic-skill data maintains structural and temporal coherence by learning from shorter, manageable segments. This approach alleviates the drift issues inherent to long-horizon generation, enabling the model to complete the _Pick and Place_ tasks. 

### **E.5 Skill-Compositional World Models Improve Downstream Success** 

Table 14: **Impact of WM on WORLD2ACT.** Our Skill-WM improves downstream success rate across both policies. 

|**Method**|**World Model**|**SR**|
|---|---|---|
|Cosmos Policy [3] + WORLD2ACT|Base-WM|0.661|
||Skill-WM (Ours)|**0.663**|
|GR00T-N1.6-ft [1] + WORLD2ACT|Base-WM|0.715|
||Skill-WM (Ours)|**0.726**|


Table 14 shows Skill-WM consistently improves downstream success because it is trained on skill-compositional data, producing more temporally consistent rollouts. This better matches WORLD2ACT’s chunk-wise alignment in a shared video–action space, leading to stronger policy execution. 

23 


Figure 14: **Qualitative comparison of task completion: Skill-WM vs. Base-WM.** We display the final frames of execution videos generated from the same prompts and initial states. While the Base-WM (left) fails to complete the trajectory and stalls mid-task, the WM trained on atomic-skill data (right) successfully places the object on the counter. Each example depicts three synchronized camera perspectives: left, wrist-mounted, and right. 

## **F Failure Cases Analysis** 

### **F.1 Imperfect World Model Rollouts** 

While our skill-compositional WM demonstrates temporally consistent video generation, it occasionally yields imperfect rollouts, which is a known limitation of current video diffusion models [3]. We illustrate representative failure cases in Figure 15. 

We categorize the observed visual artifacts into three primary failure modes: (i) _Structural hallucination:_ In the RoboCasa environment, the model incorrectly synthesizes a duplicate handle on the cup. (ii) _Multi-view inconsistency:_ In the LIBERO setup, a mug placed on a plate is successfully rendered in the primary view but disappears in the wrist-mounted view. (iii) _Fine-grained omission:_ In the real-world experiment, the model struggles to render fine-grained components, resulting in a missing door handle. 


(b) LIBERO 


Figure 15: **Visual artifacts examples.** We illustrate representative failure cases across different environments. The RoboCasa, LIBERO, and real-world setups utilize three, two, and one camera views, respectively. 

Remarkably, these failure cases motivate our core hypothesis: pixel-space representations are inherently sensitive to hallucinations, whereas latent-space dynamics provide a more robust foundation for policy learning. Even when the generated pixels exhibit localized artifacts, the underlying temporal dynamics and physical interactions remain accurate. This supports our design choice to leverage 

24 

latent dynamics, which capture the essential task progression without being bottlenecked by the need for pixel-perfect generation. 

### **F.2 Visual Artifacts Corrupt IDM Labels** 

DreamGen [9] supervises VLAs with pseudo-actions inferred by a frozen IDM from decoded WM rollouts. We study this pixel bottleneck by running the same frozen IDM on 50 held-out LIBEROObject scenes, changing only the input video source: ground-truth videos versus decoded WM rollouts. We then compute action error against temporally aligned ground-truth actions. Table 15 shows that decoded rollouts produce noisier pseudo-labels under the same IDM. 

Table 15: **Frozen-IDM action error on LIBERO-Object.** Errors are computed against temporally aligned ground-truth actions over 50 held-out scenes. Decoded WM rollouts increase both MSE and MAE under the same IDM. 

|**IDM input video**|**MSE**_↓_|**MAE**_↓_|
|---|---|---|
|Ground-truth video|0.082|0.167|
|Decoded WM rollout|0.097|0.199|
|_WM / ground-truth_|1_._18_×_|1_._19_×_|


Replacing real videos with decoded WM rollouts raises pseudo-action MSE by 18% and MAE by 19%. Since the IDM is fixed and evaluation is performed on temporally aligned action sequences, the extra error enters through the decoded rollout stream rather than the pseudo-labeling model. This gives a concrete failure path for the LIBERO drop in Table 2: pixel-space WM supervision can turn visual artifacts into incorrect action targets. WORLD2ACT avoids this bottleneck by aligning policy actions to WM dynamics in latent space, without decoding frames for IDM supervision. 

### **F.3 Failure of WM to VLA Transfer** 

Figure 16 illustrates a failure case when transferring from WM imagination to execution using GR00T-N1.6-ft+WORLD2ACT. We show the final frames of both the imagined and executed sequences for a _Turn Off Stove_ task. In the imagination sequence, the WM successfully predicts the robot grasping and turning the stove knob. However, the VLA fails to secure a firm grip on the knob during actual control, resulting in task failure. We attribute this discrepancy to the rigid physical constraints of robotic kinematics, which are far more complex and higher-dimensional than pixel space. While WORLD2ACT is specifically designed to bridge this gap by grounding the VLA in the WM’s latent dynamics, this failure case highlights the difficulty of aligning visual imagination with precise low-level motor control. 


(a) WM Imagination 


(b) VLA Execution 

Figure 16: **Failure analysis of WM to VLA transfer.** The WM generates a visually plausible completion of the task, but the VLA fails to physically ground these dynamics, causing a distribution shift during actual deployment. 

## **G Broader Impact** 

WORLD2ACT provides a practical post-training framework for transferring world-model dynamics priors to vision-language-action policies. Instead of requiring pixel-space rollout supervision or 

25 

changes to the underlying policy architecture, WORLD2ACT aligns policy action representations with latent dynamics induced by a pretrained world model. This makes the approach lightweight to apply to existing VLA systems and potentially useful as an additional post-training stage for robotic manipulation. 

We will release our code and processed datasets to support reproducibility and further research in robot learning. In addition to training robot world models, these datasets provide fine-grained videolanguage demonstrations that may be useful for offline reinforcement learning, behavior cloning, action-conditioned video generation, and benchmarking short-horizon manipulation skills. 

## **H Remarks on Related Work** 

We further clarify how WORLD2ACT differs from the closest prior work that uses latent worldmodel or future-state representations to improve VLA performance: 

- **Cosmos Policy** [3]. Cosmos Policy learns a joint embedding space and optimizes prediction heads for actions, future frames, and values. In contrast, WORLD2ACT does not train a new joint WM-policy architecture; it post-trains an existing VLA by aligning frozen-WM video dynamics with VLA action latents through lightweight video–action adapters and a residual action-latent policy. 

- **V-JEPA 2** [15]. V-JEPA 2 performs model-based planning by steering the action distribution toward a desired final state using a latent-space objective over predicted future states. WORLD2ACT addresses a different setting: rather than optimizing actions toward a terminal state, it transfers the WM’s temporally extended dynamics trajectory into the VLA action space via step-wise latent alignment, thereby guiding how the task should evolve over time. 

- **FLARE** [25]. FLARE augments a diffusion/flow-matching VLA with learnable future tokens whose hidden states are aligned to embeddings of future observations, encouraging the policy to anticipate and steer toward desirable future states. While this provides an effective goal-oriented latent regularizer, it does not explicitly transfer a temporally dense dynamics trajectory from a frozen generative WM into the action space. In contrast, WORLD2ACT leverages WM-imagined latent dynamics as step-wise supervision targets and aligns them with VLA action latents through chunk-level video–action contrastive learning. 

- **CoWVLA** [38]. CoWVLA proposes a Chain-of-World VLA pretraining scheme that uses a pretrained video VAE to factor video segments into structure and motion latents, then jointly models sparse visual keyframes and action tokens with a unified autoregressive decoder. Although CoWVLA reduces redundant intermediate-frame prediction, it still requires co-training a large VLA backbone with keyframe and action-token modeling. In contrast, WORLD2ACT is a lightweight post-training method for existing VLAs: it keeps the backbone frozen, uses pre-decoding spatial video latents from a frozen WM as dynamics targets, and trains only video–action adapters plus a residual action-latent policy. 

26 

