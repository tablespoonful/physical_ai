---
title: "Persistent Robot World Models: Stabilizing Multi-Step Rollouts via Reinforcement Learning"
date: "2026-03-26"
authors: "Jai Bardhan; Patrik Drozdik; Josef Sivic; Vladimir Petrik"
url: https://arxiv.org/abs/2603.25685
pdf: https://arxiv.org/pdf/2603.25685
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.25685)** / [論文ページ](https://arxiv.org/abs/2603.25685)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

## **Persistent Robot World Models: Stabilizing Multi-Step Rollouts via Reinforcement Learning** 

Jai Bardhan , Patrik Drozdik , Josef Sivic , and Vladimir Petrik 

Czech Institute of Informatics, Robotics and Cybernetics, Czech Technical University 

in Prague `{first.last}@cvut.cz` 

```
https://www.jaibardhan.com/persistworld
```

**Abstract.** Action-conditioned robot world models generate future video frames of the manipulated scene given a robot action sequence, offering a promising alternative for simulating tasks that are difficult to model with traditional physics engines. However, these models are optimized for short-term prediction and break down when deployed autoregressively: each predicted clip feeds back as context for the next, causing errors to compound and visual quality to rapidly degrade. We address this through the following contributions. First, we introduce a reinforcement learning (RL) post-training scheme that trains the world model on its own autoregressive rollouts rather than on ground-truth histories. We achieve this by adapting a recent contrastive RL objective for diffusion models to our setting and show that its convergence guarantees carry over exactly. Second, we design a training protocol that generates and compares multiple candidate variable-length futures from the same rollout state, reinforcing higher-fidelity predictions over lower-fidelity ones. Third, we develop efficient, multi-view visual fidelity rewards that combine complementary perceptual metrics across camera views and are aggregated at the clip level for dense, low-variance training signal. Fourth, we show that our approach establishes a new state-of-the-art for rollout fidelity on the DROID dataset, outperforming the strongest baseline on all metrics (e.g., LPIPS reduced by 14% on external cameras, SSIM improved by 9.1% on the wrist camera), winning 98% of paired comparisons, and achieving an 80% preference rate in a blind human study. 

**Keywords:** World Models · Reinforcement Learning · Robotics 

### **1 Introduction** 

Action-conditioned video diffusion world models (WM) represent a transformative frontier for robot learning, offering the potential to simulate complex, human-centric tasks that are notoriously difficult to model with traditional physics-based engines. Recent work [12] has demonstrated that finetuning pretrained video diffusion backbones with action conditioning on large-scale robotics datasets [25] can yield world models that generate impressively faithful clips that 

2 J. Bardhan et al. 


Ground Truth Video 


Baseline 


Ours 

**Fig. 1: Autoregressive video rollout quality.** We use an action-conditioned robot world model to generate multi-view image predictions from a single observed state. The ground-truth (blue) is compared against the baseline (red) and our post-trained model **PersistWorld** (green). While the baseline accumulates error and destroys the object (cyan bowl) within seconds, our method maintains structural integrity and spatial consistency, establishing a new state-of-the-art in rollout fidelity. 

are consistent with the robot’s actions. By synthesizing high-fidelity visual rollouts conditioned on robot actions, these models can serve as scalable virtual environments for benchmarking and improving Vision-Language-Action (VLA) policies. 

However, realizing this potential requires generating _long-horizon_ autoregressive rollouts — multiple seconds of coherent video — where each predicted clip feeds back as context for the next. This is precisely where current models break down. This phenomenon, known as _exposure bias_ [36], arises from a train/test distribution mismatch, i.e., the model is trained to predict from _ground-truth_ history frames, but at deployment it must condition on its own previously generated outputs, which carry growing imperfections. The consequences are rapid and severe. Within seconds of autoregressive generation, manipulated objects lose their structural identity — a bowl dissolves into an amorphous blob (see Fig. 1) — robot end-effectors drift from their commanded trajectories, and entire scene configurations decohere (see Fig. 3). 

Reinforcement learning (RL) offers a natural framework for addressing this problem: by computing a training signal directly on the model’s own autoregressive rollouts, it incentivizes consistent long-horizon generation rather than single-step accuracy. However, applying RL to diffusion models is challenging — standard policy-gradient methods require likelihoods that diffusion models do not provide, and backpropagating through the full denoising process is prohibitively expensive. Recent work [47] offers an elegant workaround by generating multiple candidate outputs, scoring them with a reward, and using the comparison to update the model — avoiding backpropagation through denoising entirely. However, this approach was developed for single-image generation and does not directly apply to our setting for two reasons. First, our robot world model uses a different type of denoising network, which means the theoretical guarantees need to be re-derived. Second, in image generation, the model can simply draw multiple independent samples from the same text prompt and compare them. In autoregressive video, there is no fixed prompt — each generation step builds on the previous output, creating an evolving shared state. This means we need a new mechanism for producing comparable candidates that can be meaning- 

PersistWorld: Persistent Robot World Models via RL 3 

fully ranked against each other. We address these challenges via the following contributions: 

1. **RL post-training for robot world models.** We introduce a post-training scheme that optimizes the world model directly on its own autoregressive rollouts rather than on ground-truth histories. We adapt a recent contrastive RL method for diffusion models [47] to our setting, where the denoising network directly predicts clean frames rather than intermediate noise, and show that convergence guarantees carry over exactly (Sec. 3.2). 

2. **A training protocol for autoregressive robot world models.** Autoregressive robot world model has no fixed prompt from which multiple candidates can be drawn and compared. We observe that the model’s accumulated history at any rollout step serves as a natural shared context from which multiple candidate continuations can be independently generated and ranked. By randomly sampling how deep into the rollout we branch these candidates, we expose training to both mild early-stage and severe late-stage error regimes (Sec. 3.3). 

3. **Multi-view visual rewards and task-relevant evaluation.** We design clip-level rewards that combine complementary perceptual metrics across all three camera views, normalized so that the training signal reflects relative quality within each group of candidates. We further introduce object-centric and robot-centric masked evaluations that confirm our improvements come from better modeling of task-relevant dynamics rather than background preservation (Sec. 3.4 and Sec. 4). 

4. **State-of-the-art rollout quality.** Our post-trained model sets a new stateof-the-art on the DROID dataset [25] across all visual quality metrics, with the largest improvements on the wrist camera—the view most critical for capturing fine-grained object manipulation. In paired comparisons, our model outperforms the baseline on approximately 98% of validation samples. A blind human preference study confirms these gains, with raters favoring our rollouts 80% of the time (Sec. 4). 

### **2 Related work** 

**Video Diffusion Models.** Diffusion models have emerged as a dominant paradigm for high-fidelity visual generation and have been successfully extended from images to videos by modeling space-time volumes with denoising objectives [17, 18, 39]. Latent video diffusion approaches adapt image diffusion backbones with temporal modules, enabling strong image-to-video and text-to-video generation while encoding rich visual priors about object motion, lighting, and physical plausibility [6]. While these models produce impressive open-loop clips, longhorizon generation via autoregressive stitching of short segments causes errors in early frames to compound as the model conditions on its own imperfect outputs, leading to temporal drift and degradation. Our setting inherits this challenge in an action-conditioned, multi-view robotics regime. 

4 J. Bardhan et al. 

**Robotic World Models and Video-Based Planning.** World models have a long history in model-based RL as learned dynamics models enabling planning through imagined rollouts [13–16]. Several works frame robot planning and evaluation directly as video generation [5, 8, 20, 26], and IRASim [49] demonstrates that a trajectory-conditioned diffusion world model can serve as a policy evaluation. Large pre-trained video diffusion backbones have been adapted into controllable robot world models via action conditioning: Ctrl-World [12] and WPE [35], both trained on DROID [25], generate multi-view manipulation trajectories and can rank downstream policy performance; AVID [38] adapts pretrained video diffusion via a learned mask adapter without parameter access; and UWM [48] jointly models video and action diffusion. None of these directly address the training-inference mismatch under self-conditioned rollout. 

**Post-Training Diffusion Models.** Aligning diffusion models to downstream objectives has been studied through RL and preference optimization [4, 28, 34, 40,44]. DiffusionNFT [47] proposes a negative-aware fine-tuning objective on the forward diffusion process, enabling efficient online RL updates without backpropagating through the denoising trajectory. DPPO [37] applies RL fine-tuning to diffusion-based robot action policies; our work instead post-trains the world model itself. RLVR-World [43] applies RL with verifiable rewards to improve world model transition quality, further evidencing that RL objectives outperform MLE for rollout fidelity. However, they work with token based models, whereas we work on improving video diffusion models. Contemporary to our work, [41] applies contrastive RL post-training [47] to a camera-pose-conditioned world model, targeting improvements in camera pose following and visual fidelity—including a prefix rollout strategy in which the model’s own outputs serve as context for subsequent clip generation. Our work shares this core motivation and training paradigm, but differs in several respects. We adopt a randomized prefix horizon during post-training rather than a fixed schedule, which we find better captures the distribution of compounding errors at test time. Our setting targets dynamic manipulation scenes in a multi-view robotic world model and we introduce a novel adaptation of the contrastive RL objective to the **x** 0- prediction parameterization used by some robot WMs. We further design visual rewards that are efficient and scalable for the multi-view robot manipulation setup. We find that compared to the HPSv3 [30] reward that is used by [41], our rewards result in much better performance. Finally, we additionally validate our approach through quantitative evaluation on robot-centric metrics and a human preference study. 

**Exposure Bias and the Rollout Gap.** The mismatch between teacher-forced training and self-conditioned inference is a longstanding problem in sequence generation [1, 36], and has been studied specifically for diffusion models [31]. In video generation the effect is amplified: small per-frame errors accumulate over long rollouts, degrading coherence and limiting world model utility for evaluation and simulation. We address this _rollout gap_ with RL post-training that directly exposes the model to its own generated histories during training. 

PersistWorld: Persistent Robot World Models via RL 5 


**Fig. 2: Overview of our method:** _(Top)_ **Autoregressive inference:** A robot policy generates actions fed to the world model, which produces multi-view frames that are appended to the history buffer and condition the next generation step. _(Bottom)_ **RL post-training: (S1)** A shared variable-length prefix is rolled out autoregressively from a ground-truth initial condition. **(S2)** _K_ independent candidate continuations are branched from the frozen prefix state. **(S3)** Candidates are scored against groundtruth using multi-view perceptual rewards. **(S4)** Reward weights _r_ scale implicit positive/negative **x** 0 predictions used in contrastive model updates via loss _L_ . 

**Large-Scale Robot Datasets.** Large-scale robot datasets enable both training data-hungry video world models and the held-out ground-truth trajectories our reward computation relies on. DROID [25] provides diverse multi-camera manipulation demonstrations, and Open X-Embodiment [32] aggregates demonstrations across many embodiments and institutions—making dataset-driven reward evaluation feasible without human preference labels. 

### **3 Improving Robot World Models with Reinforcement Learning** 

Action-conditioned video diffusion world models are trained to predict the next chunk of video frames given a clean, ground-truth history — a setup that works 

6 J. Bardhan et al. 

well in isolation, but breaks down the moment the model is deployed autoregressively over longer horizons. The central challenge we address is the following: because the model has never seen imperfect history at training time, any error introduced at one step propagates forward and compounds at the next, causing rollout quality to degrade rapidly. Resolving this requires more than better data or longer training; it requires a different approach to training — one that explicitly optimizes the model under the same auto-regressive, self-conditioned regime in which it operates at test time. 

This section develops our approach in three stages. We begin by characterizing the train/test distribution mismatch and why standard training cannot resolve it (Sec. 3.1). We then formulate post-training as an online reinforcement learning (RL) problem and derive a tractable objective by adapting a contrastive forward-process training designed for velocity-prediction flow-matching models [47] — to the EDM [24] _x_ 0-prediction parameterization of Ctrl-World’s SVD backbone; we show that the branch construction and policy-improvement guarantees carry over exactly, with no _σ_ -dependent correction terms (Sec. 3.2). Finally, we address two concrete design challenges: how to construct a grouprelative training signal from autoregressive video rollouts (Sec. 3.3), and how to define rewards that faithfully assess multi-view, multi-step visual quality (Sec. 3.4). 

#### **3.1 The Closed-Loop Gap in Autoregressive World Models** 

**Model overview.** An autoregressive robot world model, such as Ctrl-World [12], operates in a loop: at each step, it receives a history buffer of recent frame latents encoding the visual context so far, together with past and future robot actions, and generates the next chunk of future frames. The generated frames are then encoded and appended to the history buffer, which conditions the next generation step. In detail, at each autoregressive step, the model receives three inputs: (i) a history buffer **f** _t−H_ +1: _t_ of _H_ =6 recent frame latents that encode the visual context of what has transpired so far; (ii) the corresponding robot endeffector (EEF) poses **e**<sup>_H_</sup> _t−H_ +1: _t_<sup>;and(iii)asequenceoffutureEEFposetargets</sup> **e** _t_ +1: _t_ + _L ∈_ R<sup>_L×_7</sup> . From these, the model simultaneously generates _L_ =5 future frames across three camera views — two external views and one wrist-mounted view. 

**The closed-loop gap.** Training follows a standard diffusion objective under teacher forcing: given a clip of length _H_ + _L_ from the dataset, the model learns to denoise the final _L_ frames conditioned on the preceding _H ground-truth_ frames as history. This produces a reliable training signal, but installs a structural mismatch with deployment. At test time, no ground-truth history is available; each generated clip is encoded and appended to the rolling history buffer, which then conditions the next denoising pass. The model must now condition on its own previous outputs — inputs it was never trained to handle. The consequence is an error compounding loop. A minor spatial or temporal inaccuracy in clip _t_ 

PersistWorld: Persistent Robot World Models via RL 7 

corrupts the latents stored in the history buffer. These corrupted latents condition clip _t_ + 1 with increased error, which in turn corrupts the history for clip _t_ +2. Within seconds, generated scenes decohere: object configurations blur, robot state diverges from the commanded trajectory, and scene identity dissolves. Rollouts beyond a few seconds become unreliable as surrogates for real-world execution — precisely the use-case that makes world models valuable. This is not a data sufficiency problem. No amount of teacher-forced training gives the model incentive to be robust to its own imperfect history, because imperfect history is absent from the training distribution by construction. What is needed is a training signal computed directly from the model’s own autoregressive outputs — one that rewards coherent closed-loop generation and penalizes compounding drift. 

#### **3.2 Online RL Post-Training via Reward-Contrasted Denoising** 

Online reinforcement learning offers a principled solution: generate rollouts autoregressively, evaluate them against held-out ground truth, and update the model toward higher-fidelity outputs — with the training distribution defined by the model’s own production rather than teacher-forced ground truth. Because the reward is computed on self-generated frames, the training signal inherently reflects the closed-loop statistics of deployment. The challenge is making this compatible with diffusion models. 

**Reward-conditioned forward-process training.** We address this challenge by recasting policy improvement as contrastive denoising [47]: rather than estimating reverse-process likelihoods, we generate a group of candidate outputs, score them with a reward, and encode the relative quality signal directly into the denoising loss — reinforcing what the model produces for high-reward candidates and penalizing what it produces for low-reward ones. The contrastive denoising approach [47] was originally derived for velocity-prediction flow-matching models such as SD3 [11]. However, some world models — including Ctrl-World [12], which we build upon — employ an _x_ 0-prediction parameterization, where the network directly estimates the clean data _x_ 0 rather than a velocity field. We show that the contrastive denoising framework transfers naturally to this setting: because the mapping from network output to clean-data prediction is affine, the contrastive objective construction and its policy-improvement guarantees carry over exactly, with no additional correction terms. 

The full derivation is in the **Appendix A** . The resulting _x_ 0-adapted objective takes the following form. Let **x** ˆ0 _,θ_ denote the model’s clean data ( _x_ 0) prediction and **x** ˆ<sup>old</sup> 0 a frozen exponential moving average (EMA) copy serving as the reference policy. For a candidate with normalized reward weight _r ∈_ [0 _,_ 1] and mixing coefficient _β_ , we construct implicit positive and negative clean data ( _x_ 0) predictions: 


8 J. Bardhan et al. 

and minimize the reward-weighted denoising loss: 


Intuitively, the difference **x** ˆ0 _,θ −_ **x** ˆ0<sup>old</sup> defines the direction in which the current model has drifted from the frozen reference. The positive branch **x** ˆ<sup>+</sup> 0<sup>_extrapo-_</sup> _lates_ along this direction: it takes the reference prediction and moves it toward the current model by a factor _β_ , amplifying whatever changes the model has learned. Conversely, the negative branch **x** ˆ<sup>_−_</sup> 0<sup>_reverses_thisdirection,construct-</sup> ing a counterfactual prediction that moves away from the current model’s output. The loss in Eq. 2 then uses the reward weight _r_ to interpolate between fitting **x** ˆ<sup>+</sup> 0<sup>(reinforcingthemodel’scurrentdirectionforhigh-rewardsamples)andfit-</sup> ting **x** ˆ<sup>_−_</sup> 0<sup>(repellingthemodelfromitsownpredictionsforlow-rewardsamples).</sup> The mixing coefficient _β_ controls the strength of this amplification: larger _β_ produces a stronger reinforcement signal but risks destabilizing training, while _β →_ 0 recovers standard supervised denoising against the reference. Note that this formulation requires only the clean generated samples and the reference predictions — it avoids backpropagating through the denoising chain entirely, making it compatible with any black-box sampler. 

#### **3.3 Adapting Group-Relative Training to Autoregressive Video** 

The RL formulation above addresses how to update a diffusion model given reward-scored samples. Applying it to an autoregressive world model raises a second, distinct challenge: the formulation assumes a natural grouping structure — a shared conditioning input from which multiple independent candidate outputs are drawn. In image generation, this structure is straightforward: sample _K_ independent images from the same text prompt and compare them by reward. In autoregressive video generation, no such fixed prompt exists. Each generation step produces a clip that modifies the shared history buffer, which then conditions the next step; candidate clips are not independent draws from a common condition, but sequential extensions of an evolving shared state. 

The key observation is that the history buffer state immediately before any generation step plays exactly the role of the prompt in the group-relative setting: it is the accumulated context from which distinct candidate continuations can be independently branched. Freezing this buffer state and sampling _K_ independent candidate next clips from it yields a group that shares a common context, enabling meaningful reward-based comparison and contrastive training. This recovers the shared-context / independent-response structure required by group-relative objectives. We realize this structure through the following rollout protocol at each training step: 

S1: **Generate a shared prefix.** Starting from a single ground-truth observation — with the history buffer backfilled by replicating its encoded latent — we autoregressively generate _P_ consecutive clips, feeding the model’s own outputs back as history at each step. This mirrors closed-loop deployment and 

PersistWorld: Persistent Robot World Models via RL 9 

produces a history buffer state that has been corrupted by the model’s own accumulated errors. The prefix length is sampled as _P ∼_ Unif _{_ 0 _,_ 1 _, . . . ,_ 9 _}_ , exposing training to the full spectrum of rollout positions — from early steps where the buffer is nearly clean to late steps where compounding drift is severe. 

- S2: **Branch** _K_ **candidate continuations.** From the frozen prefix history buffer, we independently sample _K_ =16 candidate next segments. Each candidate is a short autoregressive sequence of _F_ chunks: the model generates _L_ frames across all three views simultaneously, encodes and appends them to a private copy of the history buffer, and repeats for _F_ steps. Each candidate follows its own distinct stochastic trajectory from the shared context. 

- S3: **Score and rank.** A visual reward _Rt_<sup>(</sup><sup>_k_)</sup> is computed for each candidate by comparing its generated frames against held-out ground-truth frames across all three camera views (Sec. 3.4). Rewards are group-normalized over the _K_ candidates to form relative advantages, removing the influence of absolute reward scale at different rollout positions. 

- S4: **Update the model.** The group-normalized reward weights are used to scale the positive and negative denoising losses (Eq. 2), and the model is updated via gradient descent. Only LoRA adapters and the action encoder receive gradient updates; the backbone is frozen. 

The variable prefix length serves two purposes. It ensures the model is optimized to maintain quality across the full rollout depth, not only at short horizons. It also exposes the update to diverse history buffer corruption profiles — from lightly drifted early-step buffers to heavily degraded late-step ones — preventing overfitting to any single error regime. 

#### **3.4 Visual Rewards for Multi-View Video Clips** 

Defining an effective reward for autoregressive robot video generation requires carefully considering what to measure and how to aggregate it. The signal must be dense enough to be informative at each training step, directly tied to perceptual quality rather than proxy statistics, and consistent across the three camera views, which provide complementary perspectives on the manipulated scene. A reward aggregated across an entire long-horizon rollout would be high-variance and would make credit assignment to specific generations difficult; we therefore score at the granularity of individual clips. 

For each candidate clip at time _t_ , we compare generated frames **x** ˆ<sup>(</sup> _t_ +1:<sup>_v_)</sup> _t_ + _L_ against the held-out ground-truth frames **x**<sup>(</sup> _t_ +1:<sup>_v_)</sup> _t_ + _L_<sup>foreachview</sup><sup>_v∈V_=</sup> _{_ wrist _,_ ext1 _,_ ext2 _}_ . Per-frame metrics are first averaged temporally over the _L_ frames of the clip: 


10 J. Bardhan et al. 

and then averaged equally across the three views: 


We use three complementary metrics to capture distinct failure modes. LPIPS [46] measures perceptual similarity in deep feature space, penalizing structural distortions even when pixel values are numerically close. SSIM [42] captures luminance, contrast, and local structural fidelity over spatial patches. PSNR [22] provides a global signal-to-noise measure that is sensitive to large pixel deviations, acting as a coarse indicator of catastrophic scene drift. Using all three produces a reward robust to the blind spots of any individual metric. LPIPS captures perceptual distortions invisible to pixel-level metrics, SSIM is sensitive to local structural changes, and PSNR flags large-scale pixel drift; combining them guards against failure modes that any single metric would miss. The per-view, per-metric averages are combined into a single scalar reward: 


where LPIPS is negated (it is lower-better), and the weights _w_ are set to bring the three components to a comparable numerical scale (values in Sec. 4). 

_Group normalization._ Because absolute reward values vary significantly across rollout positions — early clips score much higher than late ones — we normalize rewards within each group to focus the training signal on relative quality differences. The per-candidate rewards _Rt_<sup>(</sup><sup>_k_)</sup> are group-normalized over the _K_ candidates via z-score normalization: 


This converts absolute reward values into relative rankings within the group, removing the confound of reward scale variation across rollout positions. The z- scored advantages are clipped to [ _−_ 1 _,_ 1] and linearly rescaled to the [0 _,_ 1] range required by Eq. 2: 


This normalization encourages the model to discriminate between better and worse continuations from the same context, and keeps the gradient magnitude bounded regardless of the absolute level of visual quality at any given rollout position. 

### **4 Experiments** 

**Implementation details.** We use the pre-trained Ctrl-World model [12] as our base. For the proposed post-training, we apply LoRA [19] adapters to the UNet 

PersistWorld: Persistent Robot World Models via RL 11 

backbone (rank _r_ =64, _α_ =64) and additionally finetune the action encoder; all other parameters (other UNet layers, VAE, etc.) are frozen. We train for 6,000 steps with learning rate 1 _×_ 10<sup>_−_4</sup> using the Muon optimizer [23] with the batch size 64 and group size _K_ =16. Additionally, we subsample the group elements by taking the 10 most informative samples (top-5 and bottom-5 ordered by the reward) per update step. Reward weights are set to: _w_ LPIPS= _w_ SSIM=1 and _w_ PSNR= 32<sup><u>1</u>, with the</sup> 32<sup><u>1</u>factor bringing PSNR into a comparable numerical range</sup> with SSIM _∈_ [0 _,_ 1]. From our ablations this leads to the best average performance across all metrics. The model is trained on 8 NVIDIA H200 GPUs for 2 days. Primary training cost is the autoregressive rollout generation, common in prior works [21, 29]. Overall, we found that our choices are a conservative default and one can tune even more to obtain better performance; for example, see Table 6 in Appendix. For more details on ablations, see Appendix B. 

**Dataset.** We evaluate on the DROID dataset [25], a large-scale robot manipulation dataset collected on a Franka Emika Panda robot across a diverse set of tabletop environments. DROID comprises teleoperated demonstrations across a wide variety of everyday manipulation tasks and uses a standardized threecamera setup (two external cameras and one wrist-mounted camera). We use Ctrl-World’s held-out validation split for all quantitative evaluations. 

**Autoregressive rollout quality evaluation.** We evaluate autoregressive rollout quality on pre-recorded trajectories from the validation split. Starting from a single observed state (frames from all cameras + robot EEF pose), we generate 14 consecutive clips (14 _× L_ =70 frames, covering approximately 11 s at 5 Hz) using the autoregressive procedure from Sec. 3.3. We then compare the generated frames to the corresponding ground-truth frames from the dataset using SSIM [42], PSNR [22], and LPIPS [46]. We report metrics separately for external cameras and the wrist camera, as these views capture qualitatively different aspects of the scene. 

Our model establishes a new state-of-the-art for autoregressive rollout quality on the DROID dataset, consistently outperforming all baselines—WPE [35], IRASim [49], and Ctrl-World [12]—across every metric (Table 1). Compared to Ctrl-World baseline, our approach achieves significant gains on external cameras, improving PSNR by 1.40 dB and reducing LPIPS by 14.0%. These margins widen considerably against WPE and IRASim, where we see PSNR improvements of 4.09 dB and 3.06 dB and LPIPS reductions of 46.6% and 40.2%, respectively. The most pronounced gains occur on the wrist camera (SSIM +9.1%, PSNR +1.59 dB). This indicates that our closed-loop-aware post-training specifically excels at capturing the fine-grained object contact and hand-eye coordination details critical for downstream policy evaluation. Qualitatively, Fig. 3 confirms these improvements, while Fig. 4 illustrates a consistent distribution shift toward higher-fidelity generations. A 1-to-1 paired comparison reveals that our model outperforms the baseline in _∼_ 98% of validation samples, demonstrating the consistency of our gains across the entire dataset. Finally, Fig. 5 analyzes performance over extended rollouts; while both models naturally degrade as the horizon increases, our method maintains significantly higher fidelity over time. 

12 J. Bardhan et al. 

**Table 1: Visual quality metrics for 14-step autoregressive rollouts (** _≈_ **11 s) on the DROID validation split.** Values represent averages over the full rollout duration. Results marked with<sup>_∗_</sup> are from [12];<sup>_†_</sup> indicates our reproduction. 

|Evaluated<br>|Model|Pixel/|Structure|Perceptual|
|---|---|---|---|---|
|Cameras||SSIM|_↑_PSNR _↑_|LPIPS _↓_|
||WPE<sup>_∗_</sup>|0.77|20.33|0.131|
|Etl|IRASim<sup>_∗_</sup>|0.77|21.36|0.117|
|xerna<br>C|Ctrl-World<sup>_∗_</sup>|0.83|23.56|0.091|
|amera|Ctrl-World<sup>_†_</sup>|0.84|23.02|0.081|
||**Ours**|**0.86**|**24.42**|**0.070**|
|Wrist|Ctrl-World<sup>_†_</sup>|0.62|17.80|0.310|
|Camera|**Ours**|**0.67**|**19.39**|**0.277**|


**Comparison to Self-Forcing style baseline.** Recent works such as SelfForcing [21,29] are not directly applicable to our case since they primarily distill from a (usually larger) bidirectional teacher, which is not available in our case. However, to measure the importance of our RL objective over the training on corrupted history, we post-trained the model on its own rollout history but ask it to regress the ground truth latents. On the validation set with rollout length of 10 interactions, the visual metrics favor ours: wrist **0.721** / **20.40** /0.338 vs SF 0.710/20.17/0.338; external **Ours 0.872** / **25.52** / **0.116** vs 0.868/25.35/0.119. 

**Object- and Robot-Centric Evaluation.** General-purpose world models often achieve high full-frame scores by over-optimizing for static background preservation while failing to capture the complex dynamics of manipulated objects. To evaluate task-relevant fidelity, we isolate the foreground using RoboEngine [45] to segment interacting objects and the robot arm. Computing metrics on these masked regions provides a rigorous measure of spatial and control consistency, which is more critical for downstream policy learning than raw background reconstruction. Table 2 confirms that our model’s gains are concentrated on these task-critical regions. On object-masked pixels, our improvements are even more pronounced than full-frame results: external camera LPIPS drops by 16 _._ 3% (vs. 14 _._ 0% full-frame), while wrist-camera SSIM improves by 4 _._ 1%. We observe similar trends for robot-centric metrics, with PSNR increasing by 1 _._ 63 dB and 1 _._ 74 dB for external and wrist views, respectively. These results demonstrate that our training objective successfully captures the intricate dynamics of robotobject interactions rather than relying on incidental background fidelity. 

**Human Preference Study.** To complement automated evaluation, we conducted a blind human preference study to assess perceived realism and temporal consistency. Raters were presented with side-by-side video pairs from our model and the baseline, alongside the ground-truth video as a reference. They were tasked with selecting the rollout that appeared most realistic and remained most consistent with the ground-truth dynamics. Our model significantly outperforms the baseline, achieving an 80% preference rate (174 wins vs. 43).This substantial 

PersistWorld: Persistent Robot World Models via RL 13 


**Fig. 3: Qualitative comparison of autoregressive rollout stability.** We compare long-horizon (11 s) generations from the baseline [12] against our PersistWorld for the wrist camera. **Left: Object-centric fidelity.** The baseline model suffers from rapid decoherence; as errors compound in the history buffer, manipulated objects like the cup lose their structural identity and dissolve into amorphous textures. In contrast, our method maintains the spatial consistency and structural integrity of the object throughout the rollout. **Right: Robot-centric consistency.** The baseline exhibits significant **robot decoherence** , where the generated robot arm loses their geometric structure. Our approach maintains structural persistence. **Please see additional video results on the associated project page.** 

margin is further reflected in the Elo ratings, where our model reaches 884 _._ 8 compared to the baseline’s 715 _._ 2. 

These results confirm that our quantitative gains translate to a qualitatively suOurs (Post-Trained)(80%) Baseline(20%) perior experience, with human observers **Fig. 6:** Human preference results. consistently favoring our model’s ability to maintain coherent dynamics over long horizons when compared directly against the ground-truth reference. 


**Fig. 4:** _∆_ metric of paired videos from the validation dataset. On 1 _−_ 1 paired comparison, our PersistWorld world model is better than the baseline on _∼_ 98% of the sample ( _p <_ 10<sup>_−_6</sup> ). 

14 J. Bardhan et al. 


**Fig. 5: Temporal evolution of wrist camera metrics.** While both models exhibit natural degradation over longer horizons (x-axis), our post-trained model, PersistWorld (green), consistently maintains higher fidelity and slower error accumulation compared to the baseline (orange). Specifically, our method preserves a higher PSNR and SSIM while suppressing LPIPS drift, effectively extending the stable prediction horizon for complex, fine-grained interactions. See Fig. 11 in **Appendix. E.2** for external camera results. 

**Table 2: Masked visual metrics for 14-step autoregressive rollouts (** _≈_ **11 s)** . We isolate object-only and robot-only pixels to evaluate task-relevant spatial and control consistency. Our model demonstrates superior fidelity in these dynamic regions compared to baselines, confirming that performance gains are driven by accurate interaction modeling rather than background reconstruction. All metrics are averaged over the full rollout horizon. 

|Evaluated<br>Cameras|Model|SSIM _↑_|Object-O<br>PSNR _↑_|nly<br>LPIPS _↓_|SSIM|Robot-On<br>_↑_PSNR _↑_|ly<br>LPIPS _↓_|
|---|---|---|---|---|---|---|---|
|External|Ctrl-World<sup>_†_</sup>|0.88|22.25|0.025|0.82|17.62|0.039|
|Camera|**Ours**|**0.89**|**23.60**|**0.021**|**0.86**|**19.25**|**0.033**|
|Wrist|Ctrl-World<sup>_†_</sup>|0.73|18.52|0.088|0.83|25.50|0.027|
|Camera|**Ours**|**0.76**|**19.87**|**0.078**|**0.86**|**27.24**|**0.023**|


**Generalization beyond DROID.** We finetuned the SVD backbone on Bridge (WidowX) [9] and RT-1 (Google Robot) [7] for 100k steps, then applied PersistWorld post-training. PersistWorld post-training improves all three metrics on both embodiments over the SVD backbone. On Bridge, SSIM 0 _._ 864 _→_ 0 _._ 876, PSNR 25 _._ 20 _→_ 26 _._ 36, LPIPS 0 _._ 1061 _→_ 0 _._ 0957; on RT-1, SSIM 0 _._ 833 _→_ 0 _._ 865, PSNR 23 _._ 81 _→_ 26 _._ 63, LPIPS 0 _._ 1683 _→_ 0 _._ 1305. 

**Policy Evaluation.** Along with the visual metrics, we also evaluate the correlation between the world-model-based policy evaluations and the real-world policy evaluations. Across three tasks and three policies we find that PersistWorld has better correlation (0 _._ 822 vs 0 _._ 796) and MMRV (0 _._ 006 vs 0 _._ 053) than Ctrl-World. See Appendix C for more details. 

**Policy Improvement.** We ran a Ctrl-World-style policy improvement experiment: _π_ 0 is full-finetuned on 50 rollouts for 4 block spatial picking task from each WM, then evaluated on a real-robot (5 trials/block). Prompt: “Pick up the top- 

PersistWorld: Persistent Robot World Models via RL 

15 

left/top-right/bottom-left/bottom-right block”. Average task progression: base 0.350, +Ctrl-World 0.558, + **Ours 0.667** (+ **19** % **over Ctrl-World** ). 

### **5 Conclusion** 

In this paper, we addressed the critical challenge of exposure bias in actionconditioned robot world models. While existing diffusion-based world models produce high-fidelity short-term clips, their utility as simulators has been limited by compounding errors during autoregressive deployment. We introduced a reinforcement learning post-training framework that bridges this “closed-loop gap" by training the model on its own generated rollouts rather than groundtruth teacher forcing. 

Our technical contributions—adapting a contrastive online reinforcement learning objective to _x_ 0-prediction backbones and designing a variable-length branching training protocol with multi-view perceptual rewards—enable the model to remain stable over longer horizons. Our approach establishes a new state-of-the-art on the DROID dataset, significantly reducing perceptual drift and maintaining structural integrity. The 80% preference rate in our human study and the marked improvement in object and robot-centric metrics suggest that RL post-training is a powerful tool for transforming video generators into reliable, persistent robot simulators. By stabilizing multi-step rollouts, this work paves the way for using world models as scalable, high-fidelity virtual environments for the evaluation and improvement of general-purpose robotic policies. 

**Limitations and Future Work.** Despite these gains, our approach has limitations. The group-relative training protocol requires sampling _K_ = 16 independent candidates per update, which increases computational overhead during post-training compared to standard supervised fine-tuning. However, a significant advantage of our framework is its modularity; the contrastive objective is reward-agnostic, meaning the model can be optimized against any combination of perceptual, physical, or task-specific signals. While our current implementation utilizes visual fidelity rewards (LPIPS, SSIM, PSNR) to stabilize the rollouts, these do not yet explicitly enforce physical or geometrical constraints. Future work will leverage this flexibility to explore more consistency rewards—including physics-informed constraints and geometry-aware metrics—to further enhance physical realism. Additionally, we intend to investigate the application of these persistent world models directly within the policy optimization loop. 

### **Acknowledgements** 

This work was supported by the European Union’s Horizon Europe projects AGIMUS (No. 101070165), euROBIN (No. 101070596), ERC FRONTIER (No. 101097822), ELIAS (No. 101120237) and ELLIOT (No. 101214398). Compute resources and infrastructure were supported by the Ministry of Education, Youth and Sports of the Czech Republic through the e-INFRA CZ (ID:90254) and by the European Union’s Horizon Europe project CLARA (No. 101136607). 

16 J. Bardhan et al. 

### **References** 

1. Bengio, S., Vinyals, O., Jaitly, N., Shazeer, N.: Scheduled sampling for sequence prediction with recurrent neural networks. Advances in neural information processing systems **28** (2015) 

2. Bjorck, J., Castañeda, F., Cherniadev, N., Da, X., Ding, R., Fan, L., Fang, Y., Fox, D., Hu, F., Huang, S., et al.: Gr00t n1: An open foundation model for generalist humanoid robots. arXiv preprint arXiv:2503.14734 (2025) 

3. Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., et al.: _pi_ 0: A vision-language-action flow model for general robot control. arXiv preprint arXiv:2410.24164 (2024) 

4. Black, K., Janner, M., Du, Y., Kostrikov, I., Levine, S.: Training diffusion models with reinforcement learning. arXiv preprint arXiv:2305.13301 (2023) 

5. Black, K., Nakamoto, M., Atreya, P., Walke, H., Finn, C., Kumar, A., Levine, S.: Zero-shot robotic manipulation with pretrained image-editing diffusion models. arXiv preprint arXiv:2310.10639 (2023) 

6. Blattmann, A., Dockhorn, T., Kulal, S., Mendelevitch, D., Kilian, M., Lorenz, D., Levi, Y., English, Z., Voleti, V., Letts, A., et al.: Stable video diffusion: Scaling latent video diffusion models to large datasets. arXiv preprint arXiv:2311.15127 (2023) 

7. Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Dabis, J., Finn, C., Gopalakrishnan, K., Hausman, K., Herzog, A., Hsu, J., et al.: Rt-1: Robotics transformer for real-world control at scale. arXiv preprint arXiv:2212.06817 (2022) 

8. Du, Y., Yang, S., Dai, B., Dai, H., Nachum, O., Tenenbaum, J., Schuurmans, D., Abbeel, P.: Learning universal policies via text-guided video generation. Advances in neural information processing systems **36** , 9156–9172 (2023) 

9. Ebert, F., Yang, Y., Schmeckpeper, K., Bucher, B., Georgakis, G., Daniilidis, K., Finn, C., Levine, S.: Bridge data: Boosting generalization of robotic skills with cross-domain datasets. arXiv preprint arXiv:2109.13396 (2021) 

10. Elo, A.E.: The Rating of Chessplayers, Past and Present. Arco Publishing (1978) 11. Esser, P., Kulal, S., Blattmann, A., Entezari, R., Müller, J., Saini, H., Levi, Y., Lorenz, D., Sauer, A., Boesel, F., Podell, D., Dockhorn, T., English, Z., Lacey, K., Goodwin, A., Marek, Y., Rombach, R.: Scaling rectified flow transformers for high-resolution image synthesis (2024), `https://arxiv.org/abs/2403.03206` 

12. Guo, Y., Shi, L.X., Chen, J., Finn, C.: Ctrl-world: A controllable generative world model for robot manipulation. arXiv preprint arXiv:2510.10125 (2025) 

13. Ha, D., Schmidhuber, J.: World models. arXiv preprint arXiv:1803.10122 **2** (3), 440 (2018) 

14. Hafner, D., Lillicrap, T., Ba, J., Norouzi, M.: Dream to control: Learning behaviors by latent imagination. arXiv preprint arXiv:1912.01603 (2019) 

15. Hafner, D., Lillicrap, T., Fischer, I., Villegas, R., Ha, D., Lee, H., Davidson, J.: Learning latent dynamics for planning from pixels. In: International conference on machine learning. pp. 2555–2565. PMLR (2019) 

16. Hafner, D., Pasukonis, J., Ba, J., Lillicrap, T.: Mastering diverse domains through world models. arXiv preprint arXiv:2301.04104 (2023) 

17. Ho, J., Chan, W., Saharia, C., Whang, J., Gao, R., Gritsenko, A., Kingma, D.P., Poole, B., Norouzi, M., Fleet, D.J., et al.: Imagen video: High definition video generation with diffusion models. arXiv preprint arXiv:2210.02303 (2022) 

18. Ho, J., Salimans, T., Gritsenko, A., Chan, W., Norouzi, M., Fleet, D.J.: Video diffusion models. Advances in neural information processing systems **35** , 8633– 8646 (2022) 

PersistWorld: Persistent Robot World Models via RL 17 

19. Hu, E.J., Shen, Y., Wallis, P., Allen-Zhu, Z., Li, Y., Wang, S., Wang, L., Chen, W.: Lora: Low-rank adaptation of large language models (2021), `https://arxiv. org/abs/2106.09685` 

20. Hu, Y., Guo, Y., Wang, P., Chen, X., Wang, Y.J., Zhang, J., Sreenath, K., Lu, C., Chen, J.: Video prediction policy: A generalist robot policy with predictive visual representations (2025), `https://arxiv.org/abs/2412.14803` 

21. Huang, X., Li, Z., He, G., Zhou, M., Shechtman, E.: Self forcing: Bridging the train-test gap in autoregressive video diffusion. Advances in Neural Information Processing Systems **38** , 167283–167308 (2026) 

22. Huynh-Thu, Q., Ghanbari, M.: Scope of validity of psnr in image/video quality assessment. Electronics letters **44** (13), 800–801 (2008) 

23. Jordan, K., Jin, Y., Boza, V., You, J., Cesista, F., Newhouse, L., Bernstein, J.: Muon: An optimizer for hidden layers in neural networks (2024), `https: //kellerjordan.github.io/posts/muon/` , Accessed: 2026-03-05 

24. Karras, T., Aittala, M., Aila, T., Laine, S.: Elucidating the design space of diffusionbased generative models (2022), `https://arxiv.org/abs/2206.00364` 

25. Khazatsky, A., Pertsch, K., Nair, S., Balakrishna, A., Dasari, S., Karamcheti, S., Nasiriany, S., Srirama, M.K., Chen, L.Y., Ellis, K., et al.: Droid: A large-scale in-the-wild robot manipulation dataset. arXiv preprint arXiv:2403.12945 (2024) 

26. Ko, P.C., Mao, J., Du, Y., Sun, S.H., Tenenbaum, J.B.: Learning to Act from Actionless Videos through Dense Correspondences. arXiv:2310.08576 (2023) 

27. Li, X., Hsu, K., Gu, J., Pertsch, K., Mees, O., Walke, H.R., Fu, C., Lunawat, I., Sieh, I., Kirmani, S., et al.: Evaluating real-world robot manipulation policies in simulation. arXiv preprint arXiv:2405.05941 (2024) 

28. Liu, J., Liu, G., Liang, J., Li, Y., Liu, J., Wang, X., Wan, P., Zhang, D., Ouyang, W.: Flow-grpo: Training flow matching models via online rl. arXiv preprint arXiv:2505.05470 (2025) 

29. Liu, K., Hu, W., Xu, J., Shan, Y., Lu, S.: Rolling forcing: Autoregressive long video diffusion in real time. arXiv preprint arXiv:2509.25161 (2025) 

30. Ma, Y., Wu, X., Sun, K., Li, H.: Hpsv3: Towards wide-spectrum human preference score. In: Proceedings of the IEEE/CVF International Conference on Computer Vision. pp. 15086–15095 (2025) 

31. Ning, M., Sangineto, E., Porrello, A., Calderara, S., Cucchiara, R.: Input perturbation reduces exposure bias in diffusion models. arXiv preprint arXiv:2301.11706 (2023) 

32. O’Neill, A., Rehman, A., Maddukuri, A., Gupta, A., Padalkar, A., Lee, A., Pooley, A., Gupta, A., Mandlekar, A., Jain, A., et al.: Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In: 2024 IEEE International Conference on Robotics and Automation (ICRA). pp. 6892–6903. IEEE (2024) 

33. Pertsch, K., Stachowicz, K., Ichter, B., Driess, D., Nair, S., Vuong, Q., Mees, O., Finn, C., Levine, S.: Fast: Efficient action tokenization for vision-language-action models. arXiv preprint arXiv:2501.09747 (2025) 

34. Prabhudesai, M., Mendonca, R., Qin, Z., Fragkiadaki, K., Pathak, D.: Vader: Video diffusion alignment via reward gradients 

35. Quevedo, J., Sharma, A.K., Sun, Y., Suryavanshi, V., Liang, P., Yang, S.: Worldgym: World model as an environment for policy evaluation. arXiv preprint arXiv:2506.00613 (2025) 

36. Ranzato, M., Chopra, S., Auli, M., Zaremba, W.: Sequence level training with recurrent neural networks. arXiv preprint arXiv:1511.06732 (2015) 

- 18 J. Bardhan et al. 

37. Ren, A.Z., Lidard, J., Ankile, L.L., Simeonov, A., Agrawal, P., Majumdar, A., Burchfiel, B., Dai, H., Simchowitz, M.: Diffusion policy policy optimization. arXiv preprint arXiv:2409.00588 (2024) 

38. Rigter, M., Gupta, T., Hilmkil, A., Ma, C.: Avid: Adapting video diffusion models to world models. arXiv preprint arXiv:2410.12822 (2024) 

39. Singer, U., Polyak, A., Hayes, T., Yin, X., An, J., Zhang, S., Hu, Q., Yang, H., Ashual, O., Gafni, O., et al.: Make-a-video: Text-to-video generation without textvideo data. arXiv preprint arXiv:2209.14792 (2022) 

40. Wallace, B., Dang, M., Rafailov, R., Zhou, L., Lou, A., Purushwalkam, S., Ermon, S., Xiong, C., Joty, S., Naik, N.: Diffusion model alignment using direct preference optimization. In: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. pp. 8228–8238 (2024) 

41. Wang, Z., Wang, T., Zhang, H., Zuo, X., Wu, J., Wang, H., Sun, W., Wang, Z., Cao, C., Zhao, H., et al.: Worldcompass: Reinforcement learning for long-horizon world models. arXiv preprint arXiv:2602.09022 (2026) 

42. Wang, Z., Bovik, A.C., Sheikh, H.R., Simoncelli, E.P.: Image quality assessment: from error visibility to structural similarity. IEEE transactions on image processing **13** (4), 600–612 (2004) 

43. Wu, J., Yin, S., Feng, N., Long, M.: Rlvr-world: Training world models with reinforcement learning. arXiv preprint arXiv:2505.13934 (2025) 

44. Xue, Z., Wu, J., Gao, Y., Kong, F., Zhu, L., Chen, M., Liu, Z., Liu, W., Guo, Q., Huang, W., et al.: Dancegrpo: Unleashing grpo on visual generation. arXiv preprint arXiv:2505.07818 (2025) 

45. Yuan, C., Joshi, S., Zhu, S., Su, H., Zhao, H., Gao, Y.: Roboengine: Plug-andplay robot data augmentation with semantic robot segmentation and background generation (2025), `https://arxiv.org/abs/2503.18738` 

46. Zhang, R., Isola, P., Efros, A.A., Shechtman, E., Wang, O.: The unreasonable effectiveness of deep features as a perceptual metric. In: Proceedings of the IEEE conference on computer vision and pattern recognition. pp. 586–595 (2018) 

47. Zheng, K., Chen, H., Ye, H., Wang, H., Zhang, Q., Jiang, K., Su, H., Ermon, S., Zhu, J., Liu, M.Y.: Diffusionnft: Online diffusion reinforcement with forward process. arXiv preprint arXiv:2509.16117 (2025) 

48. Zhu, C., Yu, R., Feng, S., Burchfiel, B., Shah, P., Gupta, A.: Unified world models: Coupling video and action diffusion for pretraining on large robotic datasets. arXiv preprint arXiv:2504.02792 (2025) 

49. Zhu, F., Wu, H., Guo, S., Liu, Y., Cheang, C., Kong, T.: Irasim: A fine-grained world model for robot manipulation. In: Proceedings of the IEEE/CVF International Conference on Computer Vision. pp. 9834–9844 (2025) 

# **Appendix** 

This appendix provides supplementary material organized into five sections. Section A gives a complete, self-contained derivation of the post-training loss used to train our model, including a formal theoretical analysis showing why minimizing the loss steers the model toward high-reward outputs. Section B presents ablation studies that isolate the contribution of each key design choice, evaluated on the validation split. Section C examines the use of the world model as a policy evaluation tool, measuring task progression rates across three manipulation tasks. Section D details the human preference study — participant qualifications, the two-alternative forced-choice (2AFC) interface, and the ELObased ranking protocol used to aggregate votes. Finally, Section E provides the additional details and full pseudocode for the RL post-training procedure. 

### **A Derivation of the Post-Training Objective** 

This appendix provides a complete, self-contained derivation of the post-training objective described in section 3.2 in the main paper. We re-derive the objective from scratch in the _x_ 0-prediction parameterization used by our model. 

#### **Notation** 

We use the following notation throughout this appendix. 

- **x** 0 _∈_ R<sup>_d_</sup> : a clean (noiseless) latent video clip — the quantity the model is trained to predict. 

- **c** _∈_ R<sup>_dc_</sup> : the conditioning signal, comprising the robot action sequence together with any visual or text context provided to the model. 

- _σ >_ 0: the noise level. Following the EDM convention [24], a noisy observation is drawn as **x** _σ_ = **x** 0 + _σ_ **_ε_** where **_ε_** _∼N_ ( **0** _,_ **I** ) is isotropic Gaussian noise. 

- **x** ˆ0 _,θ ≡_ **x** ˆ0 _,θ_ ( **x** _σ, σ,_ **c** ) _∈_ R<sup>_d_</sup> : the current model’s estimate of the clean latent **x** 0, given noisy input **x** _σ_ , noise level _σ_ , and conditioning **c** . 

- **x** ˆ<sup>old</sup> 0 _≡_ **x** ˆ<sup>old</sup> 0<sup>(</sup><sup>**x**</sup><sup>_σ, σ,_</sup><sup>**c**)</sup><sup>_∈_R</sup><sup>_d_:thepredictionofthe</sup><sup>_frozenreferencemodel_—a</sup> copy of the weights fixed at the start of post-training that is never updated, representing the pre-trained baseline. 

- _r_ ( **x** 0 _,_ **c** ) _∈_ [0 _,_ 1]: the normalized reward weight for a generated sample **x** 0 given conditioning **c** . It is computed from visual quality metrics within a group of candidates; _r_ =1 is the best in the group, _r_ =0 is the worst (see Sec. 3.4). 

20 J. Bardhan et al. 

#### **A.1 EDM Preconditioning and the Post-Training Loss** 

_EDM preconditioning._ The world model backbone outputs a corrective term **m** _θ_ ( **x** _σ, σ,_ **c** ) _∈_ R<sup>_d_</sup> , which is converted to a clean-latent estimate via the affine EDM preconditioning [24]: 


where _c_ out( _σ_ )= _−σ/_ _~~√~~ σ_<sup>2</sup> +1 and _c_ skip( _σ_ )=1 _/_ ( _σ_<sup>2</sup> +1) are scalar functions of the noise level only. The _c_ skip term adds back a residual of the noisy input **x** _σ_ ; _c_ out scales the network’s corrective output **m** _θ_ . The identical formula applies to the frozen reference model: 


_Positive and negative branches._ Given the current-model prediction **x** ˆ0 _,θ_ and the reference prediction **x** ˆ<sup>old</sup> 0<sup>,weconstructtwobranchpredictions:</sup> 


The **positive branch x** ˆ<sup>+</sup> 0 _,θ_<sup>interpolatesfromthereferencetowardthecurrent</sup> model: at _β_ =0 it equals the reference exactly; as _β_ grows it moves toward the current model’s own prediction. The **negative branch x** ˆ<sup>_−_</sup> 0 _,θ_<sup>isitsmirrorimage:</sup> it moves _away_ from the current model in the same direction the current model has moved from the reference. Together, the two branches bracket the reference prediction symmetrically: 


_The post-training loss._ The post-training objective weights the squared reconstruction errors of the two branches by the reward weight _r_ : 


where the expectation is over ( **c** _, σ,_ **x** _σ,_ **x** 0) drawn jointly. This is identical to Eq. (2) in the main text. The intuition is direct: for a _high_ -reward sample ( _r ≈_ 1), we minimize the error of the positive branch, which points in the direction the current model has drifted from the reference — thereby _reinforcing_ that drift direction. For a _low_ -reward sample ( _r ≈_ 0), we minimize the error of the negative branch, which points in the opposite direction — thereby _penalizing and reversing_ that drift. This is the core mechanism by which the loss steers the model toward high-reward outputs. 

PersistWorld: Persistent Robot World Models via RL 21 

#### **A.2 Theoretical Analysis: Why This Loss Improves the Model** 

We now prove that, under standard assumptions, the unique minimizer of _L_ ( _θ_ ) is a model that has moved precisely in the direction of high-reward samples relative to the reference. The argument proceeds in four steps: (1) decompose the reference distribution into a high-reward part and a low-reward part; (2) show this decomposition lifts to the posterior over clean latents given a noisy observation; (3) identify the reward-aligned direction; (4) show the loss collapses to a single squared error pointing in that direction. 

_Step 1: Decomposing the reference distribution._ Let _π_<sup>old</sup> ( **x** 0 _|_ **c** ) denote the distribution over clean latents generated by the frozen reference model given conditioning **c** . We model the reward weight as the conditional probability that a sample **x** 0 is “optimal” given **c** : introducing a latent binary optimality label _o ∈{_ 0 _,_ 1 _}_ , we set 


Define the _positive distribution π_<sup>+</sup> (samples conditioned on being optimal) and _negative distribution π_<sup>_−_</sup> (samples conditioned on being suboptimal) via Bayes’ rule: 


where 


is the _partition function_ — the expected reward under the reference model, which normalizes _π_<sup>+</sup> and _π_<sup>_−_</sup> to be valid probability distributions. By the law of total probability, the reference distribution is a weighted mixture of its two parts: 


_Intuition._ The reference model generates samples from _π_<sup>old</sup> ; a fraction _Z_ ( **c** ) of those happen to be high-quality (distributed as _π_<sup>+</sup> , up-weighted by their reward _r_ ) and the rest are low-quality (distributed as _π_<sup>_−_</sup> , up-weighted by 1 _− r_ ). The reward simply measures the relative density of _π_<sup>+</sup> with respect to _π_<sup>old</sup> . 

_Step 2: Lifting the decomposition to noisy observations._ The forward noising kernel is _qσ_ ( **x** _σ|_ **x** 0) = _N_ ( **x** _σ_ ; **x** 0 _, σ_<sup>2</sup> **I** ). Let _π_<sup>_⋆_</sup> ( **x** _σ|_ **c** ) := � _qσ_ ( **x** _σ|_ **x** 0) _π_<sup>_⋆_</sup> ( **x** 0 _|_ **c** ) d **x** 0 be the marginal distribution of the noisy observation under _⋆ ∈{_ old _,_ + _, −}_ , and let _π_<sup>_⋆_</sup> ( **x** 0 _|_ **x** _σ,_ **c** ) denote the corresponding posterior over clean latents given a noisy observation **x** _σ_ . 

**Lemma 1 (Posterior mixture).** _The posterior π_<sup>old</sup> ( **x** 0 _|_ **x** _σ,_ **c** ) _is a mixture of the positive and negative posteriors:_ 


22 J. Bardhan et al. 

_where the data-dependent mixing weight (abbreviated α ≡ α_ ( **x** _σ,_ **c** ) _below) is_ 


_Proof._ Marginalise the prior mixture (Eq. (18)) through _qσ_ . Since _qσ_ does not depend on the optimality label _o_ , it acts identically on each mixture component: 


Apply Bayes’ rule to _π_<sup>old</sup> ( **x** 0 _|_ **x** _σ,_ **c** ) and substitute Eq. (18): 


For each mixture component, Bayes’ rule gives 

_qσ_ ( **x** _σ|_ **x** 0) _π_<sup>_⋆_</sup> ( **x** 0 _|_ **c** ) = _π_<sup>_⋆_</sup> ( **x** _σ|_ **c** ) _π_<sup>_⋆_</sup> ( **x** 0 _|_ **x** _σ,_ **c** ) _._ 

Substituting and grouping terms: 

_π_<sup>old</sup> ( **x** 0 _|_ **x** _σ,_ 


The first coefficient is exactly _α_ ( **x** _σ,_ **c** ) as defined in Eq. (20). The second equals 1 _− α_ : dividing Eq. (21) by _π_<sup>old</sup> ( **x** _σ|_ **c** ) gives _α_ + (1 _−Z_ ) _π_<sup>_−_</sup> ( **x** _σ|_ **c** ) _/π_<sup>old</sup> ( **x** _σ|_ **c** ) = 1, so the second weight is indeed 1 _− α_ . Non-negativity of _π_<sup>_±_</sup> and _π_<sup>old</sup> _≥ Zπ_<sup>+</sup> ensure _α ∈_ [0 _,_ 1]. 

_Intuition._ Given a noisy observation **x** _σ_ , our uncertainty about the underlying clean latent **x** 0 splits between two competing hypotheses: it came from the highreward regime ( _π_<sup>+</sup> , posterior weight _α_ ) or the low-reward regime ( _π_<sup>_−_</sup> , weight 1 _−α_ ). The mixing weight _α_ ( **x** _σ,_ **c** ) is the posterior probability that **x** _σ_ originated from a high-reward sample; it is large when **x** _σ_ is more likely under _π_<sup>+</sup> than under _π_<sup>old</sup> . 

_Step 3: Identifying the reward-aligned improvement direction._ For _⋆ ∈{_ old _,_ + _, −}_ , define the posterior mean — the expected clean latent given **x** _σ_ under distribution _π_<sup>_⋆_</sup> : 


Thus **_µ_**<sup>old</sup> is the expected clean latent under the reference model, **_µ_**<sup>+</sup> under the high-reward subset, and **_µ_**<sup>_−_</sup> under the low-reward subset. Taking expectations of both sides of Eq. (19): 


PersistWorld: Persistent Robot World Models via RL 23 

Rearranging, the displacement from **_µ_**<sup>old</sup> to **_µ_**<sup>+</sup> and from **_µ_**<sup>_−_</sup> to **_µ_**<sup>old</sup> are parallel and proportional, defining a single _improvement direction_ : 


The vector _∆x_ 0 points from the low-reward mean **_µ_**<sup>_−_</sup> toward the high-reward mean **_µ_**<sup>+</sup> , with **_µ_**<sup>old</sup> lying on the segment between them. From Eq. (26) we also read off the inverse relations: 


_Step 4: The loss collapses to a squared error in the improvement direction._ 

**Theorem 1 (Optimal predictor).** _Under unlimited data and model capacity, the unique minimizer of L_ ( _θ_ ) _is the predictor that moves from the reference posterior mean by exactly_ 2 _/β steps in the improvement direction:_ 


_Proof._ We introduce the shorthand 


the current model’s deviation from the reference posterior mean **_µ_**<sup>old</sup> . Every _θ_ - dependent quantity in _L_ ( _θ_ ) can be written in terms of **d** ; the goal is to show the loss is a pure squared error in **d** centered at the improvement direction 2 _∆x_ 0 _/β_ . 

**Algebraic step 1: Rewrite the loss using the distributional decomposition.** From Eq. (15), _r_ ( **x** 0 _,_ **c** ) _π_<sup>old</sup> ( **x** 0 _|_ **c** ) = _Z_ ( **c** ) _π_<sup>+</sup> ( **x** 0 _|_ **c** ). Substituting into the inner expectation over _π_<sup>old</sup> ( **x** 0 _|_ **x** _σ,_ **c** ) and applying Bayes’ rule gives: 


and analogously (1 _−r_ ) _π_<sup>old</sup> ( **x** 0 _|_ **x** _σ,_ **c** ) = (1 _−α_ ) _π_<sup>_−_</sup> ( **x** 0 _|_ **x** _σ,_ **c** ). Using Eqs. (30) to rewrite the reward-weighted inner expectation in _L_ ( _θ_ ): 


**Algebraic step 2: Replace the inner expectation with the posterior mean.** For any fixed vector<sup>ˆ</sup> **f** _∈_ R<sup>_d_</sup> and any distribution _p_ ( **y** ), the variance decomposition gives E _p∥_<sup>ˆ</sup> **f** _−_ **y** _∥_ 2<sup>2=</sup><sup>_∥_ˆ</sup><sup>**f**</sup><sup>_−_E</sup><sup>_p_[</sup><sup>**y**]</sup><sup>_∥_2</sup> 2<sup>+ Var</sup><sup>_p_[</sup><sup>**y**],sothesquarederror</sup> is minimized over<sup>ˆ</sup> **f** by the mean E _p_ [ **y** ], with the residual variance Var _p_ [ **y** ] being constant in<sup>ˆ</sup> **f** . Applying this to each term in Eq. (31) — the first has prediction 

24 J. Bardhan et al. 

**x** ˆ<sup>+</sup> 0 _,θ_<sup>fixedwithrespectto</sup><sup>**x**0,andposteriormean</sup><sup>**_µ_**+;thesecondhas</sup><sup>**x**ˆ</sup><sup>_−_</sup> 0 _,θ_<sup>and</sup> posterior mean **_µ_**<sup>_−_</sup> : 


where _C_ = E[ _α_ Var _π_ +[ **x** 0 _|_ **x** _σ,_ **c** ] + (1 _−α_ ) Var _π−_ [ **x** 0 _|_ **x** _σ,_ **c** ] ] does not depend on _θ_ . **Algebraic step 3: Expand in terms of d.** Step 2 showed that the MSE E _∥f_<sup>ˆ</sup> _−_ **x** 0 _∥_ 2<sup>2isminimizedbytheposteriormean.Applyingthistothereference</sup> model’s own pre-training loss (i.e. it was trained to minimize MSE against samples from _π_<sup>old</sup> ), an unlimited-capacity reference model converges to the posterior mean **_µ_**<sup>old</sup> , so **x** ˆ<sup>old</sup> 0 = **_µ_**<sup>old</sup> . Meanwhile, the current model satisfies **x** ˆ0 _,θ_ = **_µ_**<sup>old</sup> + **d** by definition of **d** (Eq. (29)). Substituting both into Eqs. (10)–(11) and subtracting **_µ_**<sup>_±_</sup> via Eq. (27): 


Substituting Eqs. (33)–(34) into Eq. (32) and expanding: 


collecting: the _∥_ **d** _∥_<sup>2</sup> 2<sup>termsgive(</sup><sup>_α_+1</sup><sup>_−α_)</sup><sup>_β_2</sup><sup>_∥_</sup><sup>**d**</sup><sup>_∥_2</sup> 2<sup>=</sup><sup>_β_2</sup><sup>_∥_</sup><sup>**d**</sup><sup>_∥_</sup> 2<sup>2;thecross-termsgive</sup> ( _−_ 2 _β−_ 2 _β_ ) **d**<sup>_⊤_</sup> _∆x_ 0; the _∥∆x_ 0 _∥_ 2<sup>2termsgive1</sup><sup>_/α_+ 1</sup><sup>_/_(1</sup><sup>_−α_) = 1</sup><sup>_/_(</sup><sup>_α_(1</sup><sup>_−α_)).</sup> **Algebraic step 4: Complete the square in d.** 


Substituting into Eq. (35) and then into Eq. (32): 


where _C_<sup>_′_</sup> = _C_ +E[ _∥∆x_ 0 _∥_<sup>2</sup> 2<sup>_/_(</sup><sup>_α_(1</sup><sup>_−α_))</sup><sup>_−_4</sup><sup>_∥∆x_</sup> 0<sup>_∥_</sup> 2<sup>2] is independent of</sup><sup>_θ_. Since</sup><sup>_β_2</sup><sup>_>_0,</sup> the unique minimizer sets **x** ˆ0 _,θ_ = **_µ_**<sup>old</sup> + (2 _/β_ ) _∆x_ 0 pointwise, giving Eq. (28). 

The optimal model is the reference posterior mean **_µ_**<sup>old</sup> shifted by (2 _/β_ ) steps in the reward-aligned direction _∆x_ 0, which by Eq. (26) points from **_µ_**<sup>_−_</sup> (low-reward samples) toward **_µ_**<sup>+</sup> (high-reward samples). The hyperparameter _β_ controls how far the model is shifted: larger _β_ produces a stronger per-step signal but also moves the branches farther from the reference, potentially destabilising training. 

PersistWorld: Persistent Robot World Models via RL 25 

_Connection to other parameterisations._ For Gaussian noising schedules, velocity predictors **v** _θ_ used by flow-matching models are related to _x_ 0 predictors by a per-noise-level affine transformation that does not depend on _θ_ . Consequently, differences between any two predictors in _x_ 0 space are proportional to their differences in velocity space. The improvement direction _∆x_ 0 and the result of Theorem 1 therefore translate directly to velocity-prediction parameterisations up to a _σ_ -dependent scalar, confirming that the theoretical guarantees are parameterisation-agnostic. 

### **B Ablation Studies** 

We report ablation results for the key design choices of our post-training. Each table isolates one factor while keeping all other hyperparameters fixed to the default configuration used in the main experiments. Metrics are evaluated on the DROID validation split over 10-step autoregressive rollouts; **higher** SSIM and PSNR and **lower** LPIPS indicate better visual quality. Specifically, we report the performance after the **same number of gradient updates (training steps) have been performed** on the model. Notably, this is different from other RL literature which report performance after the same number of outer iterations (ignoring the number of gradient updates performed during the inner iterations). The ablations collectively justify design choices made in the main paper. 

**Table 3:** Ablation of the post-training learning rate. 

|Learning Rate||Externa|l||Wrist||
|---|---|---|---|---|---|---|
||SSIM_↑_|PSNR_↑_|LPIPS_↓_|SSIM_↑_|PSNR_↑_|LPIPS_↓_|
|3_×_10<sup>_−_4</sup><br>|0_._865<br>|25_._02<br>|0_._1230<br>|0_._706<br>|19_._95<br>|0_._3603<br>|
|1_×_10<sup>_−_4</sup> **(Ours) **|**0**_._**872 **|**25**_._**52 **|**0**_._**1162 **|**0**_._**721 **|**20**_._**40 **|**0**_._**3387**|


**Table 4:** Ablation of the reward signal used during DiffusionNFT post-training. 

|Reward|SSIM_↑_|Externa<br>PSNR_↑_|l<br>LPIPS_↓_|SSIM_↑_|Wrist<br>PSNR_↑_|LPIPS_↓_|
|---|---|---|---|---|---|---|
|LPIPS only|0_._868|25_._17|**0**_._**1156**|0_._708|19_._90|**0**_._**3242**|
|SSIM only|**0**_._**872**|25_._40|0_._1178|**0**_._**724**|20_._24|0_._3516|
|PSNR only|0_._871|**25**_._**57**|0_._1189|0_._716|**20**_._**45**|0_._3544|
|Combined **(Ours) **|**0**_._**872**|25_._52|0_._1162|0_._721|20_._40|0_._3387|


**Learning rate.** The choice of _η_ =1 _×_ 10<sup>_−_4</sup> is the single most consequential hyperparameter: the higher rate 3 _×_ 10<sup>_−_4</sup> degrades external PSNR by 0 _._ 50 dB and 

26 J. Bardhan et al. 

**Table 5:** Ablation of the context-window curriculum. _Curriculum_ is the growing schedule from [41]; _Random_ samples uniformly from the specified range each step; _Fixed_ keeps a constant window size throughout training. 

|Strategy||Externa|l||Wrist||
|---|---|---|---|---|---|---|
||SSIM_↑_|PSNR_↑_|LPIPS_↓_|SSIM_↑_|PSNR_↑_|LPIPS_↓_|
|Fixed|||||||
|Size 3|0_._872|**25**_._**53**|0_._1170|**0**_._**723 **|**20**_._**51 **|**0**_._**3381**|
|Size 6|0_._871|25_._41|0_._1174|0_._719|20_._33|0_._3423|
|Curriculum [41]|0_._871|25_._50|0_._1169|0_._721|20_._43|0_._3412|
|Random|||||||
|Size 0–9 **(Ours)**|0_._872|25_._52|0_._1162|0_._721|20_._40|0_._3387|
|Size 0–4|**0**_._**873**|25_._52|**0**_._**1161**|0_._722|20_._44|0_._3391|


**Table 6:** Ablation of the GRPO group size and the number of candidates retained via best-of- _N_ filtering (evaluated at group size 16). 

|Config||Externa|l||Wrist||
|---|---|---|---|---|---|---|
||SSIM_↑_|PSNR_↑_|LPIPS_↓_|SSIM_↑_|PSNR_↑_|LPIPS_↓_|
|Group Size 4|0_._875|25_._62|0_._1142|0_._724|20_._56|0_._3379|
|Group Size 8|0_._873|25_._61|0_._1176|0_._721|20_._45|0_._3471|
|Group Size 16|||||||
|No best of _N_|0_._874|25_._69|0_._1127|0_._725|20_._64|0_._3255|
|Best of 5 **(Ours)**|0_._872|25_._52|0_._1162|0_._721|20_._40|0_._3387|
|Best of 2|**0**_._**876 **|**25**_._**79 **|**0**_._**1107 **|**0**_._**727 **|**20**_._**69 **|**0**_._**3212**|


LPIPS by 0 _._ 007, confirming that conservative fine-tuning is essential to avoid destabilizing the pretrained backbone (see Table 3). 

**Combined reward.** Using all three perceptual signals jointly (SSIM, PSNR, LPIPS) is the only configuration that is competitive across all six reported metrics. Each single-metric variant wins on its own axis but regresses elsewhere — optimizing for LPIPS alone, for example, produces the best LPIPS yet the lowest SSIM among all reward configurations. The combined reward therefore functions as a necessary regularizer, preventing the model from collapsing to a solution that sacrifices overall image quality for any single perceptual dimension (see Table 4). 

**Prefix sampling strategy.** Uniform random sampling over the full prefix range ( _P ∼_ Unif _{_ 0 _, . . . ,_ 9 _}_ ) matches or exceeds every fixed-window baseline and, crucially, outperforms the growing curriculum introduced by [41] on five of six metrics. This is a meaningful finding: the added complexity of a structured curriculum schedule does not translate into improved visual quality in our setting; a simple uniform draw over the full rollout-depth spectrum is both sufficient and preferable. The marginal additional gain from restricting the range to _{_ 0 _, . . . ,_ 4 _}_ 

PersistWorld: Persistent Robot World Models via RL 27 

**Table 7:** Ablation of the future prediction horizon _H_ (number of frames generated per autoregressive step) used during post-training. 

|Horizon _H_||Externa|l||Wrist||
|---|---|---|---|---|---|---|
||SSIM_↑_|PSNR_↑_|LPIPS_↓_|SSIM_↑_|PSNR_↑_|LPIPS_↓_|
|_H_ = 3|**0**_._**872**|25_._41|0_._1169|0_._719|20_._31|0_._3424|
|_H_ = 1 **(Ours) **|**0**_._**872 **|**25**_._**52 **|**0**_._**1162 **|**0**_._**721 **|**20**_._**40 **|**0**_._**3387**|


**Table 8:** Ablation of the wrist-camera loss weight _w_ wrist relative to the external cameras (weight 1). 

|_w_wrist||SSIM_↑_|Externa<br>PSNR_↑_|l<br>LPIPS_↓_SSIM_↑_|Wrist<br>PSNR_↑_|LPIPS_↓_|
|---|---|---|---|---|---|---|
|_w_wrist =|2|**0**_._**872**|25_._45|0_._1169<br>**0**_._**722 **|**20**_._**47 **|**0**_._**3357**|
|_w_wrist =|1 **(Ours) **|**0**_._**872 **|**25**_._**52 **|**0**_._**1162** 0_._721|20_._40|0_._3387|


is below 0 _._ 001 SSIM and 0 _._ 01 dB PSNR, confirming that exposing training to deeper rollout positions (higher _P_ ) does not hurt, while better covering the error regimes encountered at inference (see Table 5). 

**Group size and best-of-** _N_ **filtering.** We had found that best-of-2 yields further metric gains on every axis (e.g., +0 _._ 27 dB external PSNR, _−_ 0 _._ 006 external LPIPS, _−_ 0 _._ 018 wrist LPIPS), suggesting that more aggressive output filtering is a straightforward avenue for future improvement — achievable without any change to the training objective or model architecture. However, for our largescale training we stuck to a more moderate best-of-5 instead of the extremes to balance efficiency and prioritising stable and consistent reward signal across training batches (see Table 6). 

**Prediction horizon.** _H_ =1 consistently outperforms _H_ =3 across both camera views. Single-step post-training provides a tighter, lower-variance gradient signal that more directly targets the per-step generation quality evaluated at test time; multi-step rollout objectives introduce compounding errors that appear to add noise to the update without providing a commensurate benefit (see Table 7). 

**View-Specific Weighting.** The view weighting performed as expected – assigning higher weight to the wrist view resulted in a post-trained model that better generates the wrist view camera. However, the practical improvement is not significant compared to case of _w_ wrist = 1, and resulted in considerable decrease in the performance of the external cameras. Therefore, we stuck to the standard setting of _w_ wrist = 1 (see Table 8). 

**KL regularization.** Adding KL regularization improves five of six metrics, with the most consistent gains on the wrist camera. The regularization term prevents the fine-tuned policy from drifting too far from the pretrained reference, acting 

28 J. Bardhan et al. 

**Table 9:** Effect of KL regularisation applied to the post-training objective. 

|KL Reg.|SSIM_↑_|Externa<br>PSNR_↑_|l<br>LPIPS_↓_|SSIM_↑_|Wrist<br>PSNR_↑_|LPIPS_↓_|
|---|---|---|---|---|---|---|
|Without|**0**_._**873**|25_._50|0_._1163|0_._720|20_._38|0_._3392|
|With **(Ours)**|0_._872|**25**_._**52 **|**0**_._**1162 **|**0**_._**721 **|**20**_._**40 **|**0**_._**3387**|


**Table 10:** Effect of applying a warming EMA schedule to the frozen reference (old) policy, which gradually interpolates it toward the learning policy during training. 

|Reference Policy EMA|SSIM_↑_|Externa<br>PSNR_↑_|l<br>LPIPS_↓_SSIM_↑_|Wrist<br>PSNR_↑_|LPIPS_↓_|
|---|---|---|---|---|---|
|No EMA schedule|**0**_._**872**|25_._51|**0**_._**1162 0**_._**722 **|**20**_._**46**|0_._3390|
|EMA rising to 0_._5 **(Ours) **|**0**_._**872 **|**25**_._**52 **|**0**_._**1162** 0_._721|20_._40|**0**_._**3387**|


**Table 11:** Effect of applying an exponential moving average (EMA) to the learning (fine-tuned) policy weights during post-training. 

|Policy EMA||SSIM_↑_|Externa<br>PSNR_↑_|l<br>LPIPS_↓_|SSIM_↑_|Wrist<br>PSNR_↑_|LPIPS_↓_|
|---|---|---|---|---|---|---|---|
|EMA = 0_._9||0_._876|25_._81|0_._1105|0_._726|20_._68|0_._3215|
|No EMA (Group Size 16,|BoN 2)|0_._876|25_._79|0_._1107|0_._727|20_._69|0_._3212|


as an implicit constraint that preserves the model’s generalization while allowing reward-directed improvement (see Table 9). 

**Old-policy EMA schedule.** The EMA schedule of the old policy rising to 0 _._ 5 is marginally better than a copy reference across most metrics. The EMA value rises to 0 _._ 5 until 500 training steps, and then remains fixed at this value. Although the absolute differences are within measurement noise, the schedule provides a principled mechanism to prevent the on-policy sampling model from drifting too far from the original model and introducing instability early on in the training (see Table 10). 

**EMA on the learning policy.** Similar to [47], we test with using a EMA of the weights of the policy being learned. However, we found that this does not lead to any significant improvements for the additional machinery (see Table 11). 

### **C World Model For Policy Evaluation** 

We test whether world model can be used for policy evaluation by rolling out the learned policy in the world model and calculating the task progression rates for the different policies. 

We perform a set of 3 tasks: 

PersistWorld: Persistent Robot World Models via RL 29 


**Fig. 7: Initial Conditions for the WM-to-Real Correlation.** We run rollouts in the world models given these starting conditions for the three tasks. For the policy rollout, the middle view (external camera) and the wrist view are provided as inputs. 

- **Put Banana in Box:** In this task, the robot must pick up a banana and place it inside a box. The task is successful if the banana is fully contained within the box (see Fig. 7a). 

- **Put Green Block in Bowl:** In this task, the robot must pick up a green block and place it inside a bowl. The task is successful if the green block is fully contained within the bowl (see Fig. 7b). 

- **Rotate Marker:** In this task, the robot must pick up a marker and rotate it by at least 45 degrees. The task is successful if the marker is rotated by the required amount (see Fig. 7c). 

**Table 12: Partial Progress of the Different Tasks** . 

|Skill|Task|Progression|
|---|---|---|
|_Put_|Put Banana in Box<br>Put Green Block in Bowl|Reach _→_Grasp _→_Lift _→_Move Close _→_IsInside|
|_Rotate_|Rotate Marker|Reach _→_Grasp _→_Rotate 45<sup>_◦_</sup>|


30 J. Bardhan et al. 

For each task, we collect real-rollouts for three policies: _π_ 0 [3], _π_ 0-FAST [33] and GROOT N1 _._ 5 [2]. For each task and policy we collect 5 real rollouts, and 11 simulated rollouts in the world model. For each rollout, we record the partial progress according to Table 12. The total progress is divided into _N_ steps and completing a particular step in order would grant 1 _/N_ towards the total progress. We then average the partial progress over the multiple rollouts to obtain an estimate of the policy’s performance on the particular task. 

We report the Pearson Correlation _r_ and MMRV [27]. Higher Pearson correlation implies that the world model more closely follows the trend in real progress rates amongst the policies. MMRV, on the other hand, penalizes policy rank violations between the simulated setup (world model) and the real setup. Our world model produces higher correlation and lower MMRV than baseline [12]. 


**Fig. 8: WM to Real comparison:** While both the world models tend to make the task easier for the policies (shown by the higher values task performance on the WM), our post-trained model maintains better correlation and MMRV amongst the policies compared to the baseline [12]. 

PersistWorld: Persistent Robot World Models via RL 31 

### **D Human Preference Study Details** 

**Study design.** We conduct a human preference study to evaluate the visual quality of the rollouts generated by the original and post-trained Ctrl-World models. The study was conducted in-house on our custom-created platform. The study comprised 8 users who are experts in computer vision, machine learning and robotics with papers in these fields. Each user also additionally had a masters qualification, with some users also having a PhD qualification. We believe that the users were sufficiently capable of discerning differences and alignment to the reference rollout video. To provide high quality signal, users were also allowed to choose which video they would like to rate. We find an inter-rater kappa _κ ∼_ 0 _._ 4, which points to moderate agreement on rating. However, we find that the binomial test gives us a _p_ -value of _p_ = 3 _._ 5 _·_ 10<sup>_−_20</sup> , which means essentially zero chance that our post-trained model could have won purely by random chance. The 95% CI comes out to be [72% _,_ 100%] which is significantly higher than 50%. 

**UI Design.** Each user first went through an onboarding phase, where the task description and potential hints for rating the videos were provided (see, Fig. 9). 

On the comparison webpage, the users were shown the reference video and two generated videos (one from each checkpoint). Each video was generated using 14 autoregressive interaction steps (approx. 11 seconds). Only the reference video was labeled and the other videos’ labels were masked. The users had the ability to scrub through the frames to view them individually or watch the entire video. Below the videos, users were provided two options “A” or “B”, and were asked to choose between one of them (see, Fig. 10). The position of the generated videos were always randomized so as to remove any position bias. 

**ELO Score Design.** We adopt a chess-style ELO rating system [10] to rank models from pairwise preference votes. Each model is initialised with a rating of 800. For every vote submitted by a user, the two models shown in that comparison are treated as opponents in a single ELO match. Prior to updating their ratings, the system computes each model’s _expected score_ via the standard logistic function, 


where _Ri_ and _Rj_ are the current ratings of model _i_ and its opponent _j_ , respectively. _Ei ∈_ (0 _,_ 1) maps the rating gap to a win probability: a model rated 400 points above its opponent is expected to win _≈_ 91% of the time. The _actual score_ is _Si_ = 1 for the preferred model and _Si_ = 0 for the other. Ratings are then updated symmetrically, 


with a fixed gain factor _K_ = 32. Because _Si − Ei_ is small when the outcome matches the prior expectation, a model that was already the clear favourite gains little from an expected victory; conversely, an upset win produces a large positive update. In practice, with only two models, ELO converges quickly to reflect the 

32 J. Bardhan et al. 


**Fig. 9: 2AFC Website Onboarding:** We provide a small description of the task and potential hints to look at when judging the quality of the generated rollouts compared to the reference. 

PersistWorld: Persistent Robot World Models via RL 

33 


**Fig. 10: 2AFC Website Comparison UI:** On the comparison webpage, the users are provided with the reference video on the top and the two generated videos below it. The users can use the scrubber to move through the frames or watch the entire video. After which, the user needs to choose between Option A or Option B. 

34 J. Bardhan et al. 


**Fig. 11: Temporal evolution of external camera metrics.** While both models exhibit natural degradation over longer horizons (x-axis), our post-trained model, PersistWorld (green), consistently maintains higher fidelity and slower error accumulation compared to the baseline (orange). Specifically, our method preserves a higher PSNR and SSIM while suppressing LPIPS drift, effectively extending the stable prediction horizon for complex, fine-grained interactions. 

empirical preference rate — a model preferred 70% of the time will accumulate a rating roughly 100-150 points above the other. 

### **E Additional Details** 

#### **E.1 Inference Details** 

We run inference using the Euler Sampler, and run the sampling for 50 steps. Following [47], we do not use CFG while sampling the generated video. 

#### **E.2 Additional Results** 

**Degradation of the metrics over rollout length for external views** We present in Fig. 11 the temporal evolution of the all the metrics for the external camera view. We find that the post-trained model has a better performance on all frames. This suggests that the post-training procedure is effective at improving the long-term consistency of the generated videos. 

**Ours vs. WorldCompass [41]** We share the contrastive-RL paradigm but differ in four ways that preclude direct comparison: _x_ 0 vs v-pred parameterization (requiring our Appendix A re-derivation), action-conditioned manipulation vs camera-pose video-game WM, DROID’s larger scale, and our additional validations (human study, policy-eval correlation). To isolate the most transferable component, viz. their reward design, we replaced our reward with HPSv3 [30] in our framework on DROID. Table 13 shows that our reward structure results in better downstream performance while being much faster to train with. HPSv3 runs a large VLM to check for alignment between a text prompt and generated images. In our case we do not have such text conditioning so we instead run HPSv3 reward with the prompt: “Robot arm <task>”. Therefore, as such 

PersistWorld: Persistent Robot World Models via RL 35 


**Fig. 12: Qualitative comparison of autoregressive rollout stability on Bridge [9] and RT-1 [7].** We compare long-horizon (11s) generations from the baseline against our PersistWorld. In both the cases, we see that the baseline model struggles to maintain object consistency. **In left,** we see that the saucepan has completely disappeared in the baseline model, while PersistWorld is able to maintain it. **In right,** we see that the baseline model has lost the bottle, and instead hallucinates a different object within the robot’s gripper. In contrast, PersistWorld is able to maintain the bottle and correctly shows the gripper grasping the bottle. 

it cannot assess action-conditioned trajectory consistency which is critical for our use case. Our reference-based perceptual rewards directly ground generated frames against the GT trajectory implied by the action sequence, providing a more appropriate training signal for our setting. 

**Table 13: Our reward vs HPSv3 [30]:** To compare to WorldCompass [41], we compare their reward structure with HPSv3 [30] to our light-weight rewards. 

|Reward|SSIM _↑_|PSNR _↑_|LPIPS _↓_|training sec/iter _↓_|
|---|---|---|---|---|
|HPSv3 (theirs)|0.802|22.58|0.193|129.2|
|**Ours** (top-_k_=2)|**0.826**|**24.09**|**0.181**|**41.3**|


**Generalization beyond DROID** We finetuned the SVD backbone on Bridge (WidowX) [9] and RT-1 (Google Robot) [7] for 100k steps, then applied PersistWorld post-training. In table 14, we compare against IRASim [49] (<sup>_†_</sup> IRASim Tab. 2) under matched data and resolution. PersistWorld improves all metrics on both embodiments, with gains larger than on DROID. 

In Figure 12, we visualize the improvements by PersistWorld on the Bridge and RT-1 datasets. We find that the post-trained model is able to generate more realistic and consistent rollouts compared to the baseline SVD backbone. 

**Comparison to Self-Forcing style baseline.** Recent works such as SelfForcing [21,29] are not directly applicable to our case since they primarily distill 

36 J. Bardhan et al. 

**Table 14: Generalization Beyond DROID:** We compare the performance of the standard action conditioned pretraining on SVD backbone to PersistWorld on a long rollout with 10 consecutive interactions. We also report IRASim [49] on their long trajectory setup ( _†_ indicates the number is taken from original paper). 

|Dataset|Method|SSIM _↑_|PSNR _↑_|LPIPS _↓_|
|---|---|---|---|---|
||IRASim [49] (long-traj)<sup>_†_</sup>|–|23.26|–|
|Bridge|SVD backbone|0.864|25.20|0.1061|
||+ PersistWorld (**Ours**)|**0.876**|**26.36**|**0.0957**|
||IRASim [49] (long-traj)<sup>_†_</sup>|–|24.62|–|
|RT-1|SVD backbone|0.833|23.81|0.1683|
||+ PersistWorld (**Ours**)|**0.865**|**26.63**|**0.1305**|


from a (usually larger) bidirectional teacher, which is not available in our case. However, to measure the importance of our RL objective over the training on corrupted history, we post-trained the model on its own rollout history but ask it to regress the ground truth latents. On the validation set with rollout length of 10 interactions, the visual metrics favor ours: wrist **0.721** / **20.40** /0.338 _vs_ . SF 0.710/20.17/0.338; external **Ours 0.872** / **25.52** / **0.116** _vs_ . 0.868/25.35/0.119. The advantage is very clear when we look at the effective reward obtained on the rollouts. Figure. 13 shows that our post-training strategy obtains an effective reward at step 240 that exceeds the baseline’s reward at 2400 steps. 


**Fig. 13: Ours vs SF style baseline:** Our reward exceeds the SF-style baseline. Our procedure achieves the same performance _∼_ 10 _×_ faster and achieves a much higher reward at the same number of steps. 

**Policy Improvement.** We ran a Ctrl-World-style policy improvement experiment: _π_ 0 [3] is full-finetuned on 50 rollouts for 4 block spatial picking task 

PersistWorld: Persistent Robot World Models via RL 37 


**Fig. 14: Policy Improvement Setup:** We place 4 blocks on a table and command the robot to pick up the top-right/top-left/bottom-right/bottom-left block in the 2 _×_ 2 grid. We also place some distractors on the table such as the bowl and the tape. 

from each WM, then evaluated on a real-robot (5 trials/block). Prompt: “Pick up the top-left/top-right/bottom-left/bottom-right block”. Average task progression: base 0.350, +Ctrl-World 0.558, + **Ours 0.667** (+ **19** % **over Ctrl-World** ). Figure. 14 shows the setup for the policy improvement experiment. 

#### **E.3 Post-Training Algorithm** 

We present the Post-Training algorithm in Alg. 1. We describe the four steps _S_ 1 to _S_ 4. 

38 J. Bardhan et al. 

**Algorithm 1** RL Post-Training for Autoregressive Video World Models 

**Require:** Pretrained world model _θ_ ; frozen reference policy **x** ˆ0<sup>old</sup> (EMA copy of _θ_ ); dataset _D_ ; group size _K_ =16; branch length _F_ ; mixing coefficient _β_ ; reward weights _w_ LPIPS _, w_ SSIM _, w_ PSNR 1: **for** each training step **do** 2: **_– Stage S_** 1 **_: Generate shared prefix –_** 3: Sample initial ground-truth observation ( **x** 0 _,_ **e** 0) from _D_ 4: Sample prefix length _P ∼_ Unif _{_ 0 _,_ 1 _, . . . ,_ 9 _}_ 5: Initialise history buffer **h** 0 by replicating the encoded latent of **x** 0 6: **for** _p_ = 1 **to** _P_ **do** _▷_ closed-loop autoregressive rollout 7: Sample **x** _p ∼ θ_ ( _· |_ **h** _p−_ 1 _,_ **e** _p−_ 1: _p_ + _L_ ) 8: **h** _p ←_ append Enc( **x** _p_ ) to **h** _p−_ 1 _▷_ history buffer update 9: **end for** 10: **_– Stage S_** 2 **_: Branch_** _K_ **_candidate continuations –_** 11: **for** _k_ = 1 **to** _K_ **do** _▷_ independent samples from shared context 12: Initialise private buffer **h**<sup>(</sup><sup>_k_)</sup> _←_ **h** _P ▷_ frozen copy of prefix 13: **for** _f_ = 1 **to** _F_ **do** 14: Sample **x**<sup>(</sup> _P_<sup>_k_</sup> +<sup>)</sup> _f_<sup>_∼θ_</sup> � _· |_ **h**<sup>(</sup><sup>_k_)</sup> _,_ **e** _P_ + _f_ : _P_ + _f_ + _L_ � 15: **h**<sup>(</sup><sup>_k_)</sup> _←_ append Enc� **x**<sup>(</sup> _P_<sup>_k_</sup> +<sup>)</sup> _f_ � to **h**<sup>(</sup><sup>_k_)</sup> 16: **end for** 17: **end for** 18: **_– Stage S_** 3 **_: Score, rank, and group-normalise –_** 19: **for** _k_ = 1 **to** _K_ **do** 20: Compute per-view, per-frame LPIPS, SSIM, PSNR against ground-truth frames ~~(~~ _k_ ) 21: _R_<sup>(</sup><sup>_k_)</sup> _←−w_ LPIPS LPIPS ~~(~~ _k_ ) + _w_ SSIM SSIM ~~(~~ _k_ ) + _w_ PSNR PSNR 22: **end for** 23: _µR ← K_ <u>1</u> � _k_<sup>_R_(</sup><sup>_k_)</sup><sup>_,_</sup> _σR ←_ std _k_ ( _R_<sup>(</sup><sup>_k_)</sup> ) 24: **for** _k_ = 1 **to** _K_ **do** 25: _A_<sup>(</sup><sup>_k_)</sup> _←_ � _R_<sup>(</sup><sup>_k_)</sup> _− µR_ � _/_ ( _σR_ + _ϵ_ ) _▷_ z-score normalisation 26: _r_<sup>(</sup><sup>_k_)</sup> _←_ �clip( _A_<sup>(</sup><sup>_k_)</sup> _, −_ 1 _,_ 1) + 1� _/_ 2 _▷_ rescale to [0 _,_ 1] 27: **end for** 28: **_– Stage S_** 4 **_: Contrastive denoising update –_** 29: _L ←_ 0 30: **for** _k_ = 1 **to** _K_ **do** 31: Sample _σ ∼ p_ ( _σ_ ), **_ε_** _∼N_ ( **0** _,_ **I** ) 32: **x**<sup>(</sup> _σ_<sup>_k_)</sup> _←_ **x**<sup>(</sup> 0<sup>_k_)</sup> + _σ_ **_ε_** _▷_ forward noising 33: **x** ˆ<sup>(</sup> 0<sup>_k_</sup> _,θ_<sup>)</sup><sup>_←_currentmodelpredictionfrom</sup><sup>**x**</sup> _σ_<sup>(</sup><sup>_k_)</sup> 34: **x** ˆ<sup>(</sup> 0<sup>_k_</sup> _,_ old<sup>)</sup><sup>_←_referencemodelpredictionfrom</sup><sup>**x**</sup> _σ_<sup>(</sup><sup>_k_)</sup> _▷_ frozen 35: **x** ˆ<sup>(</sup> 0<sup>_k_)+</sup> _←_ (1 _− β_ ) ˆ **x**<sup>(</sup> 0<sup>_k_</sup> _,_ old<sup>)+</sup><sup>_β_ˆ</sup><sup>**x**(</sup> 0<sup>_k_</sup> _,θ_<sup>)</sup> 36: **x** ˆ<sup>(</sup> 0<sup>_k_)</sup><sup>_−_</sup> _←_ (1 + _β_ ) ˆ **x**<sup>(</sup> 0<sup>_k_</sup> _,_ old<sup>)</sup><sup>_−β_ˆ</sup><sup>**x**(</sup> 0<sup>_k_</sup> _,θ_<sup>)</sup> 37: _L_ += _r_<sup>(</sup><sup>_k_)</sup> _∥_ **x** ˆ<sup>(</sup> 0<sup>_k_)+</sup> _−_ **x**<sup>(</sup> 0<sup>_k_)</sup><sup>_∥_</sup> 2<sup>2+ (1</sup><sup>_−r_(</sup><sup>_k_))</sup><sup>_∥_</sup><sup>**x**ˆ(</sup> 0<sup>_k_)</sup><sup>_−_</sup> _−_ **x**<sup>(</sup> 0<sup>_k_)</sup><sup>_∥_</sup> 2<sup>2</sup> 38: **end for** 39: Update _θ_ (LoRA adapters + action encoder only) via gradient descent on _L_ 40: **x** ˆ<sup>old</sup> 0 _←_ EMA(ˆ **x**<sup>old</sup> 0<sup>_,θ_)</sup> _▷_ update reference policy 41: **end for** 

