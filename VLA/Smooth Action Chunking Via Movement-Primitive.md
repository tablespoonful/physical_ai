---
title: "Smooth Action Chunking Via Movement-Primitive Representations for Imitation Learning"
date: "2026-10-29"
authors: "Shota Nomura; Takayuki Osa; Yasuhiro Kato; Kazuki Ota; Naoki Shitanda; Tatsuya Harada"
url: https://arxiv.org/abs/2610.39451
pdf: https://arxiv.org/pdf/2610.39451
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2610.39451)** / [論文ページ](https://arxiv.org/abs/2610.39451)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Smooth Action Chunking via Movement-Primitive Representations for Imitation Learning** 

Shota Nomura<sup>1</sup><sup>_,_2</sup> , Takayuki Osa<sup>2</sup> , Yasuhiro Kato<sup>1</sup> , Kazuki Ota<sup>1</sup><sup>_,_2</sup> , Naoki Shitanda<sup>1</sup><sup>_,_2</sup> , Tatsuya Harada<sup>1</sup><sup>_,_2</sup> 

**_Abstract_ — Imitation learning has become a widely adopted approach for vision-based robot policies, owing to its conceptual simplicity, scalability, and ability to leverage large-scale datasets. As these policies have grown more capable, action chunking has become their standard interface. At each decision step the policy outputs several future actions at once. Backbones from diffusion policies to large vision-language-action models all share it. Whatever backbone produces the chunk, its temporal structure is learned only implicitly. The commanded trajectory is therefore jerky both within a chunk and between successive chunks. On real hardware this appears as visible vibration and as repeated saturation of the follower’s velocity limit. We address this issue by incorporating a movementprimitive-based trajectory representation into action chunking. Specifically, a trajectory segment is represented as a linear combination of smooth basis functions, yielding smooth trajectories by construction while leaving the policy architecture, training objective, and inference procedure unchanged. The same representation also yields a closed-form, inference-time correction for the second source of jerk. We condition the predicted coefficients so that the new chunk passes through a via-point at the previous chunk’s last commanded action. This correction needs no retraining and, unlike asynchronous Real-Time Chunking, applies to policies queried in one shot. We instantiate it on a one-shot (ACT) and an iterative (DiT) backbone and evaluate in simulation and on a real bimanual ALOHA platform. The representation lowers within-chunk jerk by an order of magnitude on the one-shot backbone and by** 2 _._ 4 _×_ **on the iterative one, with task success statistically non-inferior. The conditioning then removes** 73 **–** 84% **of the boundary discontinuity, at negligible per-step cost.** 

## I. INTRODUCTION 

Imitation learning has become a widely used route to robot policies that generate continuous actions in real time from visual observations, without explicitly modeling the environment or the task. As these policies handle a broader range of tasks, _action chunking_ , in which the policy outputs a segment of several future actions at once rather than a single action per step, has become their standard interface. It realizes forward-looking behavior and is beneficial both for task performance and for reducing the frequency at which the policy must be queried. The interface is shared across otherwise very different designs, from lightweight imitation-learning policies that regress a chunk in one shot, to diffusion-based policies that produce it through an iterative denoising loop, to the large vision-language-action (VLA) models increasingly used for robot control [1], [2]. 

> 1The University of Tokyo, Tokyo, Japan. _{_ nomura, kato, ota, shitanda, harada _}_ @mi.t.u-tokyo.ac.jp 

> 2RIKEN Center for Advanced Intelligence Project, Tokyo, Japan. takayuki.osa@riken.jp 


Fig. 1: Overview of this study. **Top left:** predicting the raw action chunk leaves the commanded trajectory jerky within a chunk and discontinuous between chunks. **Top right:** predicting it as a weighted sum of smooth basis functions is smooth by construction. **Bottom:** the backbone predicts movement-primitive coefficients **_w_** ˆ. At inference we condition them on the previous chunk’s last point to obtain the corrected coefficients **_w_** ˆ<sup>_′_</sup> , then decode these into the action chunk. 

Typically, the temporal structure of action chunks is learned only implicitly, so the generated trajectories are often jerky. On real hardware this manifests as noticeable vibration and frequent saturation of the velocity limits of the follower arm, which tracks the commanded joint positions. Such vibration hinders rapid task execution and can accelerate the mechanical fatigue of the robot arm. 

This jerk has two distinct sources. Within a chunk, neighboring predicted steps are not constrained to vary smoothly. Between successive chunks, the start of a newly predicted chunk need not align with the tail of the chunk currently being executed, producing a discontinuity at every chunk boundary. Existing remedies are largely external, such as temporal ensembling, low-pass filtering, or Real-Time Chunking (RTC) [3]. 

We address both sources of jerk by predicting trajectories in the coefficient space of a movement-primitive (MP) trajectory representation, through two components of different scope, each targeting one source. First, to remove the withinchunk jerk, we adopt a smooth trajectory representation, in which a chunk is predicted as a linear combination of smooth basis functions, so that every chunk is smooth by 

construction. This is purely a change of prediction target and applies to any chunk-based backbone. Second, to remove the between-chunk discontinuity, we add an inter-chunk conditioning step. At inference time we condition the predicted chunk on _via-points_ , anchor points taken from the previous chunk’s last commanded actions. This uses the closed-form conditioning update of Probabilistic Movement Primitives (ProMP) [4], so that the new chunk starts close to where the previous one ended. The correction requires no additional training. Because it acts on a single predicted chunk rather than on a denoising loop, it reaches one-shot policies that RTC-style asynchronous stitching cannot, while remaining applicable to iterative ones (Fig. 1). 

Both components are independent of the policy architecture, applying whether the chunk is produced in one shot or through an iterative loop. We therefore instantiate them on two backbones at opposite ends of that axis, the lightweight one-shot Action Chunking with Transformers (ACT) [5] and an iterative Diffusion Transformer (DiT) [6], and evaluate both in simulation and on a real bimanual ALOHA platform. We make the following contributions: 

- **A smooth trajectory representation.** Predicting a chunk as a combination of smooth basis functions removes within-chunk jerk by construction, leaving the backbone, its objective, and its inference procedure unchanged. 

- **A training-free inter-chunk correction.** Inferencetime ProMP conditioning on via-points from the previous chunk removes most of the boundary discontinuity and applies even to one-shot policies. 

- **Empirical validation.** Across both backbones, in simulation and on a real bimanual ALOHA platform, the method improves trajectory smoothness while keeping task success comparable to the baselines. 

## II. RELATED WORK 

_a) Chunk-based imitation learning:_ Predicting a chunk of future actions has become a common design choice in imitation learning [7], [8]. ACT [5] predicts a fixed-horizon action chunk with a CVAE [9], [10] and blends overlapping chunks with temporal ensembling, while Diffusion Policy [11] generates the chunk through a denoising diffusion process. Diffusion Transformer policies [6] scale this idea with a transformer backbone and improved training stability. The same chunking mechanism underlies most recent large vision-language-action models [1], [2]. 

_b) Trajectory smoothness:_ Jerky commanded trajectories are a known failure mode of chunk-based policies and are typically mitigated externally, e.g. by temporal ensembling, low-pass filtering, smoothness-regularized training objectives [12], or the smoothing behavior of the low-level controller. Movement-primitive methods such as Dynamic Movement Primitives (DMPs) [13], [14], Probabilistic Movement Primitives (ProMPs) [4], and ProDMPs [15] instead build smoothness into the trajectory representation, encoding it with smooth basis functions. We employ a simplified 

variant of ProMP, in which trajectories are linear combinations of smooth basis functions. ProMP additionally supports probabilistic conditioning on via-points, which we exploit for the inter-chunk connection (Section IV-B). 

_c) Chunk stitching and asynchronous execution:_ A separate line of work targets the discontinuity between successive chunks. The simplest approach blends overlapping predictions, by temporal ensembling [5] or weighted-sum blending, which reduces jumps but lags the commanded trajectory and cannot enforce continuity exactly. Real-Time Chunking (RTC) [3] instead constrains the next chunk to continue the already-committed prefix by soft-inpainting that prefix at every step of the iterative denoising process. By construction this presupposes an iterative policy and an asynchronous schedule, so a one-shot policy, with no denoising loop to inpaint into, lies outside its scope. Others build both the smoothness and the connection into the action representation itself. ProDMP [15] adds structural terms that force every decoded trajectory to start from the current position and velocity; BEAST [16] encodes chunks as B-spline tokens that are smooth within a chunk and continuous across chunk boundaries; and Movement Primitive Diffusion [17], the closest work to ours, pairs a ProDMP representation with a diffusion policy for gentle manipulation of deformable objects. These bake the connection into a representation the policy is trained to predict, and the diffusion variants tie it to an iterative backbone. Moreover, in our preliminary experiments, policies predicting ProDMP weights fell well short of the action accuracy of their ProMP counterparts on our tasks. We therefore retain the simpler MP representation as a backbone-agnostic change of prediction target and enforce the connection with a training-free, inference-time correction on a single predicted chunk. 

## III. PRELIMINARIES 

Our method combines a movement-primitive trajectory representation with a chunk-based imitation-learning backbone. This section reviews the three ingredients it builds on, namely the MP representation and the two backbones we instantiate it on, ACT and a DiT policy. 

## _A. ProMP_ 

Probabilistic Movement Primitives (ProMP) [4] represent a trajectory as a linear combination of _n_ basis functions. Let _τ ∈_ [0 _,_ 1] denote the normalized phase variable and **_ϕ_** ( _τ_ ) _∈_ R<sup>_n_</sup> a vector of Gaussian basis functions evaluated at phase _τ_ . A scalar trajectory _a_ ( _τ_ ) is expressed as 


For a multi-dimensional action of dimension _da_ , the coefficient matrix **W** _∈_ R<sup>_n×da_</sup> stacks per-dimension weights. Over a chunk horizon of _n_ chunk steps, the full trajectory is recovered in matrix form as 


where row _j_ of **Ψ** is **_ϕ_** ( _τj_ )<sup>_⊤_</sup> for the phase _τj_ corresponding to timestep _t_ + _j_ . Because the basis functions are smooth, any 

trajectory in this representation is smooth by construction. ProMP further places a Gaussian prior **_w_** _∼N_ ( **_µw_** _,_ Σ **_w_** ) on the weights, under which conditioning the trajectory to pass through a set of via-points admits a closed-form Gaussian update of ( **_µw_** _,_ Σ **_w_** ). We use both the representation and this conditioning update, the latter instantiated in Section IV-B. 

## _B. Action Chunking Transformer_ 

Action Chunking with Transformers (ACT) [5] is a CVAEbased imitation learning method that predicts a chunk of _n_ chunk future actions at each timestep. An encoder _qϕ_ maps the demonstration action chunk and current observation _ot_ to a latent variable _z_ , and a decoder reconstructs the chunk **_a_** ˆ _t_ : _t_ + _n_ chunk = _pθ_ ( _z, ot_ ). It is trained with the standard CVAE objective, an _ℓ_ 1 reconstruction loss on the chunk plus a _β_ - weighted KL term. At inference _z_ is set to the prior mean and decoded. 

## _C. Diffusion Transformer Policy_ 

As a second backbone we use a Diffusion Transformer (DiT) policy [6], which, like Diffusion Policy [11], frames action generation as a denoising diffusion process over the action chunk **_a_** _t_ : _t_ + _n_ chunk but uses a transformer denoiser conditioned on the observation and diffusion timestep. Following DDPM [18], a network _ϵθ_ is trained with the usual _ℓ_ 2 objective to predict the noise added to the chunk, and at inference a chunk is generated by iteratively denoising from **_a_**<sup>_K_</sup> _∼N_ ( **0** _,_ **I** ) conditioned on _ot_ . 

## IV. PROPOSED METHOD 

Our method addresses the discontinuity of chunk-based action generation from two sides. Within a chunk, the smooth trajectory representation of Section IV-A makes every generated chunk smooth. Between chunks, the smooth connection of Section IV-B aligns each new chunk with the tail of the previous one. 

## _A. Smooth Trajectory Representation_ 

The core idea of our method is to replace direct action chunk prediction with prediction in the MP coefficient space introduced in Section III-A. Given the current observation _ot_ (DiT additionally receives _ot−_ 1), the model outputs **_w_** ˆ _t ∈_ R<sup>_n×da_</sup> instead of **_a_** ˆ _t_ : _t_ + _n_ chunk directly. The predicted action chunk is then recovered via **_a_** ˆ _t_ : _t_ + _n_ chunk = **Ψ** **_w_** ˆ _t_ . 

_a) ACT with the MP representation:_ We apply this substitution to ACT by changing the decoder target from the raw action chunk to the MP coefficients. The decoder _pθ_ now predicts **_w_** ˆ _t_ , and the reconstructed action is **_a_** ˆ _t_ : _t_ + _n_ chunk = **Ψ** ˆ **_w_** _t_ . The loss retains the same form as in Section III-B, with this substitution applied to **_a_** ˆ. 

_b) DiT with the MP representation:_ We apply the same substitution to the DiT policy by replacing **_a_** _t_ : _t_ + _n_ chunk with **_w_** _t_ throughout the noising and denoising steps (Section III-C). The loss retains the same form, with the noise-prediction loss evaluated after mapping both the predicted and true noise through **Ψ** , and at inference the trajectory is recovered via **_a_** ˆ _t_ : _t_ + _n_ chunk = **Ψ** **_w_** ˆ _t_<sup>0afteriterativedenoising.</sup> 

## _B. Smooth connection between chunks_ 

The policy outputs an action chunk conditioned on the observations up to time _t_ , with nothing tying it to the actions predicted one step earlier. It therefore does not generate each chunk in continuity with the previous one, since the start of a new chunk need not align with the tail of the one still being executed, producing a sudden jump in the commanded actions at the boundary. 

We address this by conditioning the predicted coefficients **_w_** ˆ _t_ on via-points drawn from the final _m_ steps of the previous chunk. Concretely, let **_y_**<sup>_∗_</sup> = _{_ **_a_** _t−m, . . . ,_ **_a_** _t−_ 1 _}_ denote the via-points and **Ψ** via _∈_ R<sup>_m×n_</sup> the first _m_ rows of **Ψ** , so that the via-points are placed at the start of the new chunk and execution resumes at row _m_ . The update is applied to each action dimension independently. Applying the ProMP conditioning update (Section III-A) yields the corrected coefficient mean 


where Σ **_w_** controls the flexibility of the weight distribution and Σ<sup>_∗_</sup> _y_<sup>controlshowstrictlythevia-pointsareenforced,</sup> a smaller Σ<sup>_∗_</sup> _y_<sup>pullingthetrajectoryclosertothevia-points</sup> (the anchor). Σ<sup>_∗_</sup> _y_<sup>isdiagonal,andwhen</sup><sup>_m>_1theentries</sup> belonging to older via-points are relaxed by a factor of ten per step, so the most recent commanded action dominates the correction. The update is a maximum-a-posteriori correction under a fixed prior Σ **_w_** , not a posterior over a distribution the policy itself predicts. The backbone emits a point estimate **_w_** ˆ _t_ , and Σ **_w_** , relative to Σ<sup>_∗_</sup> _y_<sup>,setsonlyhowfaritmaybe</sup> moved to meet the via-point, giving the corrected trajectory **_a_** ˆ _t_ : _t_ + _n_ chunk = **Ψ** **_w_** ˆ _t_<sup>_′_.Because</sup><sup>**_K_**dependsonlyonfixed</sup> parameters and the basis matrix, it is precomputed, so the correction runs purely at inference at negligible cost, using the same MP policy with and without it and requiring no additional training. Details on Σ **_w_** , Σ<sup>_∗_</sup> _y_<sup>,and</sup><sup>_m_aregivenin</sup> Section V-A. 

## V. EXPERIMENTS 

We ask whether predicting in MP coefficient space makes chunk-based policies smoother without sacrificing task success, and how the inter-chunk conditioning compares to alternative connection strategies. 

## _A. Experimental Setup_ 

We evaluate our method in two settings. In simulation, using a bimanual ALOHA in MuJoCo, we generate 50 demonstrations per task with a scripted expert policy. On real hardware, a bimanual ALOHA platform, we collected 100 demonstrations per task (50 for ACT on Fold Cloth) via teleoperation in the same environment used during evaluation. Both policies observe four camera images and the 14dimensional joint state, and output absolute joint positions for both arms including the grippers, z-score normalized per dimension. We measure commanded jerk in both settings, and evaluate both backbones, ACT and DiT, in each. Both 

backbones use a chunk horizon of _n_ chunk = 50 steps at a 50 Hz control rate and query the policy every 25 executed steps. In simulation, execution pauses during inference. On hardware, inference runs in the background while the arm continues the current chunk, and the new chunk replaces its remainder on arrival, or is blended with it under +WS. There, all configurations skip the steps of a new chunk that elapsed during inference, except the conditioned chunk, which is executed without skipping them (Section VI). Each episode runs a fixed number of steps with no early termination on success, set per task from the length of the demonstrations: 400 (8 s at 50 Hz) in simulation and on Pick-and-Pass, 500 on Peg Insertion, and 700 on Fold Cloth. Success is judged from the simulator state by a task-specific criterion in simulation, and by an operator at the end of each episode on hardware. For the conditioning we use a single position via-point ( _m_ = 1) with Σ<sup>_∗_</sup> _y_<sup>=10</sup><sup>_−_1innormalizedactionunits,the</sup> operating point selected by the sweep in Section V-E. Σ **_w_** is the identity, an isotropic prior in the normalized weight space, so the direction of the correction is determined by the basis functions at the via-point. Hyperparameters otherwise follow the released implementations, apart from the input resolution (256 _×_ 256) and the training schedule. ACT is trained for 100k steps with batch size 8 and learning rate 10<sup>_−_5</sup> . DiT is trained with learning rate 10<sup>_−_4</sup> and cosine decay, for 50k steps with batch size 64 on hardware and 100k steps with batch size 16 in simulation. Within a backbone the compared configurations differ only in the prediction target. 

**1) Models:** For each backbone we compare three configurations, all trained with three random seeds. **Baseline** predicts the raw action chunk directly, with no MP representation. **+MP** predicts _n_ = 10 MP coefficients per action dimension instead. **+MP+condition** (+Cond in the tables) is the same +MP model with inter-chunk via-point conditioning enabled at inference, so the two MP cells share identical weights and differ only in whether the correction is applied. The basis functions are Gaussians with centers spaced uniformly in phase and a standard deviation of half the center spacing, normalized to sum to one. Each demonstrated chunk is projected onto these basis functions by ridge regression ( _λ_ = 10<sup>_−_6</sup> ) to obtain the target coefficients, and the loss is computed after mapping both the prediction and its target through **Ψ** . Table II also reports two connection baselines, both applied at inference. Weighted-sum blending (+WS) ramps linearly from the previous to the new chunk over their remaining overlap and runs on both representations. RealTime Chunking (+RTC), adapted here to the DDIM sampler with guidance weight 2, runs on the raw-action DiT policy only, since it inpaints the committed action prefix during denoising and so requires actions as the denoised variable. 

**2) Statistical treatment:** Throughout, error bars denote the standard deviation over the three training seeds. The compared configurations share the same initial states, and the +MP and +MP+condition runs share their trained weights as well. Each comparison therefore rests on the paired difference, whose variation is far smaller than the marginal seed-to-seed spread. Where the pairing runs episode by 

episode we test success with McNemar’s exact test. The jerk effects we read from the paired difference and its magnitude rather than from a null-hypothesis test over three seeds. Tasksuccess comparisons are claims of non-inferiority rather than of improvement. 

## _B. Research Questions and Metrics_ 

We organize the evaluation around three questions, each with the metric it rests on. 

**RQ1 (Performance).** Does predicting in MP coefficient space preserve task success? 

We report the final task success rate after training, averaged over three training seeds: 100 episodes per seed in simulation, from a fixed set of initial states shared by the configurations being compared so that they can be tested pairwise, and 10 episodes per seed on real hardware, where each episode index starts from the same nominal object placement in every configuration and all configurations of a backbone are collected in one session to avoid drift between them. On hardware, the DiT checkpoint is selected on the validation action MSE, the open-loop action error on heldout demonstrations. Other models use the final checkpoint. **RQ2 (Smoothness).** How much does the representation reduce jerk, and how does the conditioning compare to alternative connection strategies? 

The primary metric is the jerk of the commanded action stream, the mean absolute third finite difference of the commanded arm-joint trajectory at the 50 Hz control rate, in normalized action units per s<sup>3</sup> . This signal is generated by the policy and carries no sensor noise, so it is differentiated directly. Gripper dimensions are excluded throughout, since their open/close transients dominate the all-joint value. Mirroring the two sources of jerk, we split the commanded samples by their position relative to a re-planning seam, where execution switches to a newly predicted chunk: withinchunk jerk, over chunk-interior samples, isolates the representation, and boundary jerk, over samples within _±_ 2 steps of a seam, isolates the connection. Commanded smoothness need not survive execution, so we additionally report two execution-side quantities: a band-limited jerk over the 1–5 Hz vibration band, computed from the recorded joint velocity, and the number of velocity-clamp activations per episode. A velocity clamp fires when the commanded displacement of an arm joint exceeds a per-joint velocity limit, set to 1 _._ 3 _×_ the training data’s per-joint 99 _._ 9th-percentile speed plus 0 _._ 15 rad/s, and is clipped to it, visible as a stall on the physical arm. We differentiate the recorded velocity, not the position, because the third derivative of position is dominated by 12-bit encoder quantization noise, which masks any effect of the method. 

**RQ3 (Computational cost).** What does the conditioning cost per inference call, against the alternatives? 

We compare the inference time per call of each connection strategy. Our conditioning applies one precomputed gain matrix per chunk, whereas RTC modifies the trajectory at every denoising step. 

TABLE I: Simulation results. +Cond is +MP with interchunk conditioning. Arrows indicate the better direction, and bold marks the lowest jerk in each row of (b) and (c). 

|Backbone|Task|Baseline|+MP|+Cond|
|---|---|---|---|---|
|_(a) Success _|_rate (%) (↑)_||||
|ACT|Transfer Cube|96_._0_±_5_._3|97_._7_±_1_._2|99_._0_±_1_._0|
||Insertion|47_._7_±_15_._8|55_._7_±_13_._4|54_._3_±_6_._4|
|DiT|Transfer Cube|85_._7_±_0_._6|77_._3_±_3_._5|78_._0_±_6_._9|
||Insertion|57_._0_±_10_._0|55_._3_±_5_._5|63_._0_±_8_._9|
|_(b) Within-_|_chunk commande_|_d jerk (↓)_|||
|ACT|Transfer Cube|261_._4_±_10_._6|69_._0_±_1_._6|**68**_._**7**_±_**1**_._**0**|
||Insertion|339_._4_±_16_._7|62_._6_±_1_._1|**60**_._**7**_±_**2**_._**8**|
|DiT|Transfer Cube|907_._9_±_931_._0|**63**_._**5**_±_**0**_._**8**|70_._6_±_3_._9|
||Insertion|307_._0_±_20_._2|**59**_._**6**_±_**2**_._**2**|65_._7_±_0_._2|
|_(c) Bounda_|_ry commanded j_|_erk (↓)_|||
|ACT|Transfer Cube|660_±_83|526_±_77|**163**_±_**5**|
||Insertion|1008_±_118|713_±_62|**172**_±_**3**|
|DiT|Transfer Cube|1828_±_1021|1874_±_213|**305**_±_**63**|
||Insertion|2200_±_417|2443_±_375|**319**_±_**93**|


## _C. Tasks_ 

_a) Simulation tasks:_ We use two bimanual tasks from the ALOHA simulation suite [5] with scripted-expert demonstrations: Transfer Cube, where the right arm picks up a cube and hands it to the left, and Insertion, where the right arm inserts a peg into a socket held by the left. 

_b) Real-robot tasks:_ We evaluate three bimanual tasks on the real ALOHA platform: Pick-and-Pass, where one arm grasps an object and passes it to the other; Fold Cloth, where both arms cooperatively fold a cloth; and Peg Insertion, where one arm holds a socket while the other inserts a peg (Fig. 2). 

## _D. Results_ 

Simulation and real-hardware results are reported together under each research question. 

**1) Task Success (RQ1):** Predicting in MP coefficient space leaves final task success essentially unchanged in both settings. The fixed initial-state protocol pairs the MP and non-MP runs of a backbone episode by episode, so we compare them with McNemar’s test. In simulation (Table I(a)) final success is flat across the representation in three of the four cells. Only DiT on Transfer Cube moves significantly, and it moves down ( _p_ = 0 _._ 01), while adding the boundary conditioning moves no cell ( _p ≥_ 0 _._ 06). On real hardware (Table II(a)) the same test, pooling the 30 index-matched episode pairs of each cell, finds no cell where either the representation or the added conditioning moves success ( _p ≥_ 0 _._ 45 throughout), the largest change in any cell amounting to one episode per seed. With a non-inferiority margin of one episode per seed, the 10-percentage-point resolution of the 10-episode protocol, every real cell is non-inferior, and the only exception in either setting is the DiT decrease in simulation above. The test has limited power, since cells near the ceiling cannot show a drop and the seed-to-seed spread is large relative to the differences at stake. 

**2) Smoothness: Within-Chunk Representation (RQ2):** The within-chunk commanded jerk shows the effect of the 

representation on both platforms. In simulation (Table I(b)) the MP model is smoother in every cell, and reaches nearly the same level in all four even though the baselines it starts from differ widely. On hardware (Table II(b)) the same signature appears. The representation lowers within-chunk jerk by an order of magnitude on ACT and severalfold on DiT, and on each task the two backbones converge to nearly the same value, a level set by the demonstrated motion the basis must fit. One simulation seed is an outlier. A single DiT run on Transfer Cube has a far jerkier baseline than the other two seeds at the same success rate, inflating that entry’s mean and spread, whereas the +MP entries show no comparable spread anywhere. 

**3) Smoothness: Inter-Chunk Connection (RQ2):** Table II(c–e) compares four connection strategies, namely no connection, weighted-sum blending, our via-point conditioning, and RTC, on the commanded boundary jerk, the executed 1–5 Hz band jerk, and velocity-clamp activations. Fig. 3 shows the commanded trajectory around a chunk boundary without a connection, with blending, and with conditioning. Blending is reported on both representations, since it does not depend on how the chunk is parameterized. On the commanded boundary jerk, however, running +WS on top of the MP representation stays well below running it on the raw action in every cell (Table II(c)), so on this dimension the representation helps even under blending. In simulation the conditioning removes most of the boundary jerk in every cell at no cost in success (Table I(c)). The boundary jerk the representation alone leaves is several times larger on DiT than on ACT. 

On hardware, the boundary jerk without a connection is tens of times the within-chunk value, and the representation alone reduces it only slightly. Via-point conditioning removes most of this discontinuity at negligible inference cost (Section V-D.4) and no change in success, but its effect on the executed motion differs between the two backbones. On ACT, velocity-clamp activations decrease from about 8– 13 per episode without a connection to 1–3 with one on all three tasks (Table II(e)), and the executed 1–5 Hz jerk in Table II(d) decreases as well. Blending reduces clamp activations to a similar degree, which suggests that the reduction comes from closing the seam rather than from the way it is closed. On DiT, clamp activations decrease in the same way, but the executed band jerk stays within the seed spread. The seam left after conditioning is larger on DiT, about ten times the within-chunk value, and blending, which lowers it further, also lowers the executed band jerk, so the remaining vibration on DiT may be tied to this residual seam. 

Three further comparisons concern the other connection strategies. First, RTC reduces the seam by a fraction comparable to our conditioning, at success within noise, while raising within-chunk jerk. Second, weighted-sum blending attains the lowest boundary and executed band jerk in every cell where it was run, at no measurable inference cost and with success within noise. Applied to the raw-action policy with no MP representation at all, it already reaches a lower executed 1–5 Hz jerk on ACT than the full repre- 


Fig. 2: Evaluation tasks. (a, b) Simulation. (c–e) Real ALOHA. 

TABLE II: Real-hardware results. Columns are grouped by the representation they run on, and columns within a group share the same trained weights. Arrows indicate the better direction, and bold marks the lowest value in each row of (b)–(e). RTC applies to DiT only. 

||||Raw action|||MP||
|---|---|---|---|---|---|---|---|
|Backbon|e Task|Baseline|+WS|+RTC|+MP|+WS|+Cond|
|_(a) Succ_|_ess rate (%) (↑)_|||||||
||Pick-and-Pass|80_._0_±_10_._0|83_._3_±_20_._8|–|73_._3_±_23_._1|76_._7_±_20_._8|83_._3_±_15_._3|
|ACT|Fold Cloth|96_._7_±_5_._8|96_._7_±_5_._8|–|93_._3_±_5_._8|100_._0_±_0_._0|100_._0_±_0_._0|
||Peg Insertion|80_._0_±_17_._3|86_._7_±_15_._3|–|80_._0_±_10_._0|76_._7_±_5_._8|70_._0_±_10_._0|
||Pick-and-Pass|86_._7_±_15_._3|96_._7_±_5_._8|83_._3_±_20_._8|90_._0_±_10_._0|96_._7_±_5_._8|96_._7_±_5_._8|
|DiT|Fold Cloth|96_._7_±_5_._8|96_._7_±_5_._8|93_._3_±_5_._8|90_._0_±_0_._0|86_._7_±_15_._3|90_._0_±_10_._0|
||Peg Insertion|90_._0_±_10_._0|93_._3_±_5_._8|100_._0_±_0_._0|96_._7_±_5_._8|96_._7_±_5_._8|96_._7_±_5_._8|
|_(b) With_|_in-chunk command_|_ed jerk (↓)_||||||
||Pick-and-Pass|280_._1_±_10_._0|251_._2_±_8_._7|–|**18**_._**9**_±_**0**_._**9**|20_._5_±_0_._9|20_._1_±_0_._6|
|ACT|Fold Cloth|434_._2_±_19_._1|380_._4_±_20_._2|–|**33**_._**4**_±_**1**_._**4**|36_._3_±_1_._4|34_._0_±_1_._0|
||Peg Insertion|319_._5_±_17_._6|290_._1_±_13_._4|–|**20**_._**7**_±_**0**_._**4**|22_._9_±_0_._5|21_._4_±_0_._5|
||Pick-and-Pass|59_._3_±_1_._7|60_._7_±_4_._2|129_._2_±_51_._9|**22**_._**1**_±_**3**_._**2**|26_._5_±_5_._0|27_._4_±_2_._9|
|DiT|Fold Cloth|80_._4_±_3_._1|78_._7_±_2_._7|99_._7_±_7_._3|**33**_._**1**_±_**2**_._**3**|42_._0_±_3_._8|42_._1_±_2_._9|
||Peg Insertion|71_._9_±_8_._8|74_._7_±_8_._1|107_._1_±_16_._4|**20**_._**9**_±_**1**_._**8**|26_._6_±_3_._5|26_._2_±_2_._9|
|_(c) Boun_|_dary commanded _|_jerk (↓)_||||||
||Pick-and-Pass|925_±_22|285_±_3|–|758_±_171|**28**_±_**3**|127_±_12|
|ACT|Fold Cloth|1425_±_103|444_±_16|–|1222_±_137|**45**_±_**3**|214_±_14|
||Peg Insertion|962_±_106|330_±_25|–|965_±_34|**33**_±_**1**|150_±_11|
||Pick-and-Pass|1601_±_446|82_±_10|473_±_268|1404_±_393|**54**_±_**12**|249_±_18|
|DiT|Fold Cloth|1667_±_128|108_±_9|501_±_22|1554_±_259|**81**_±_**8**|416_±_56|
||Peg Insertion|1052_±_98|96_±_21|388_±_89|1032_±_190|**58**_±_**9**|244_±_34|
|_(d) Exec_|_uted_ 1_–_5_Hz band _|_jerk (↓)_||||||
||Pick-and-Pass|7_._05_±_0_._47|3_._79_±_0_._13|–|6_._32_±_1_._08|**3**_._**42**_±_**0**_._**10**|5_._38_±_0_._33|
|ACT|Fold Cloth|10_._54_±_0_._50|5_._00_±_0_._18|–|9_._74_±_0_._91|**4**_._**57**_±_**0**_._**13**|8_._19_±_0_._43|
||Peg Insertion|6_._77_±_0_._88|**3**_._**71**_±_**0**_._**14**|–|7_._48_±_0_._27|3_._77_±_0_._13|5_._99_±_0_._35|
||Pick-and-Pass|10_._83_±_2_._51|**5**_._**25**_±_**0**_._**96**|5_._42_±_0_._62|9_._98_±_2_._76|5_._53_±_1_._41|7_._91_±_0_._90|
|DiT|Fold Cloth|12_._43_±_0_._72|**6**_._**36**_±_**0**_._**37**|7_._47_±_0_._17|12_._81_±_2_._28|7_._79_±_1_._13|12_._53_±_0_._96|
||Peg Insertion|7_._99_±_0_._66|**5**_._**04**_±_**0**_._**43**|5_._31_±_0_._27|8_._88_±_1_._88|5_._51_±_1_._23|7_._75_±_0_._91|
|_(e) Velo_|_city-clamp activati_|_ons per episode _|_(↓)_|||||
||Pick-and-Pass|10_._8_±_0_._8|2_._9_±_0_._2|–|9_._7_±_2_._9|2_._7_±_0_._4|**2**_._**6**_±_**0**_._**4**|
|ACT|Fold Cloth|12_._6_±_2_._2|**0**_._**9**_±_**0**_._**3**|–|11_._1_±_2_._1|**0**_._**9**_±_**0**_._**1**|**0**_._**9**_±_**0**_._**2**|
||Peg Insertion|7_._6_±_1_._6|**2**_._**0**_±_**0**_._**0**|–|8_._5_±_0_._5|**2**_._**0**_±_**0**_._**0**|**2**_._**0**_±_**0**_._**0**|
||Pick-and-Pass|24_._4_±_7_._7|3_._3_±_1_._3|5_._5_±_2_._0|22_._4_±_7_._6|3_._6_±_1_._0|**2**_._**4**_±_**1**_._**5**|
|DiT|Fold Cloth|21_._8_±_2_._4|**1**_._**2**_±_**0**_._**3**|3_._1_±_0_._7|21_._2_±_6_._6|4_._1_±_2_._0|1_._9_±_1_._7|
||Peg Insertion|11_._6_±_2_._6|2_._8_±_0_._5|3_._9_±_0_._2|10_._9_±_4_._9|3_._5_±_1_._5|**1**_._**7**_±_**1**_._**0**|


sentation plus conditioning attains. The two differ in what is commanded to obtain the smoothing (Fig. 3). Blending emits a convex combination of the previous and the newly predicted chunk across the entire remaining overlap, not merely at the seam, so the command keeps departing from the fresh prediction long after the boundary. Measuring that departure as the integral of _|_ commanded _−_ freshly predicted _|_ , conditioning on ACT discards far less of the fresh prediction than blending does (0 _._ 023 versus 0 _._ 128 rad _·_ step, averaged over arm joints) and returns to it sooner, an advantage that does not hold on DiT (0 _._ 150 versus 0 _._ 131). Third, neither 

connection method substitutes for the representation in the chunk interior. Blending applied to the raw-action baseline leaves within-chunk jerk essentially untouched on every task, worse there than the MP policy with no connection at all. 

**4) Computational Cost:** We report the inference time per call to address RQ3. Predicting _n_ coefficients instead of _n_ chunk actions changes only the width of the output head, so we compare against other ways of obtaining a smooth, connected trajectory. Temporal ensembling in its original form averages all chunks covering the current step and so requires a forward pass per step. At the 50 Hz control 


Fig. 3: Commanded trajectory around a chunk boundary on Fold Cloth. (a) Command of one representative joint on ACT with no connection, blending, and conditioning. (b) Deviation of the command from the freshly predicted chunk, averaged over arm joints, against time since it arrived, on ACT and DiT. Shading marks the integral. 

rate neither backbone’s inference on our RTX 6000 Ada GPU fits the 20 ms per-step budget (ACT _≈_ 33 ms, DiT _≈_ 113 ms with eight DDIM steps), so we do not report it as a measured arm. Weighted-sum blending mixes only the overlap between consecutive chunks and our conditioning applies one precomputed closed-form update per chunk. Both leave the time per call indistinguishable from the base policy, within its seed-to-seed spread (DiT 116 ms with conditioning versus 113 ms without). RTC, which modifies the trajectory at every denoising step, is the only strategy with a real overhead, nearly doubling the time per call on DiT (from 113 to 205 ms). 

## _E. Ablation Study_ 

We ablate two design choices on real hardware, on Pickand-Pass with the ACT backbone. The first is the conditioning strength. We sweep the via-point noise Σ<sup>_∗_</sup> _y_<sup>overseven</sup> orders of magnitude together with the number of via-points _m_ . Together they set the operating point of +MP+condition. The second is the number of basis functions, _n ∈{_ 5 _,_ 10 _,_ 20 _}_ , which trades expressiveness against smoothness. The former reuses the trained +MP model at inference, whereas the latter requires a training run per level. Both ablations were run in sessions separate from Table II, so their values are compared within each ablation only. 

Table III first sweeps the via-point noise Σ<sup>_∗_</sup> _y_<sup>withasingle</sup> via-point ( _m_ = 1) and then varies the number of via-points at the selected Σ<sup>_∗_</sup> _y_<sup>.Successdoesnotdistinguishthelevels,</sup> all of which lie within sampling noise of one another. The commanded boundary jerk falls as Σ<sup>_∗_</sup> _y_<sup>is tightened and levels</sup> off below 10<sup>_−_2</sup> , whereas the executed jerk is U-shaped, with a reproducible minimum at 10<sup>_−_1</sup> . We select Σ<sup>_∗_</sup> _y_<sup>= 10</sup><sup>_−_1,the</sup> minimum of the executed jerk rather than of the commanded one. A likely reason for the U shape is that the anchor, the last command of the previous chunk, carries that chunk’s own prediction error, which a strict via-point passes into the next chunk and a looser one partly averages out. Using three or five via-points instead of one leaves the executed jerk unchanged within noise and lowers the commanded boundary jerk only slightly, since the older via-points are 

TABLE III: Conditioning ablation on Pick-and-Pass with ACT. All rows use the same +MP model. _†_ marks the selected operating point. 

|Σ<sup>_∗_</sup><br>_y_|_m_|Boundary (_↓_)|Executed 1–5Hz (_↓_)|Success (%) (_↑_)|
|---|---|---|---|---|
|10<sup>_−_6</sup>|1|75_±_3|6_._69_±_0_._17|83_±_6|
|10<sup>_−_3</sup>|1|73_±_2|6_._50_±_0_._10|83_±_15|
|10<sup>_−_2</sup>|1|81_±_4|5_._42_±_0_._18|87_±_12|
|10<sup>_−_1</sup> _†_|1|121_±_5|**4**_._**76**_±_**0**_._**13**|83_±_15|
|10<sup>0</sup>|1|398_±_47|5_._31_±_0_._36|83_±_29|
|10<sup>+1</sup>|1|740_±_80|6_._40_±_0_._51|80_±_17|
|10<sup>_−_1</sup>|3|108_±_13|4_._93_±_0_._07|87_±_15|
|10<sup>_−_1</sup>|5|99_±_4|4_._72_±_0_._07|90_±_17|


relaxed and the most recent one dominates the correction, so we keep _m_ = 1. 

For the number of basis functions, evaluated with two seeds per level, within-chunk commanded jerk rises with _n_ (4 _._ 8, 19 _._ 0, and 57 _._ 1 for _n_ = 5, 10, and 20), while success varies within the seed spread (60 _±_ 57, 75 _±_ 7, and 65 _±_ 21%). We use _n_ = 10, the middle setting, since a wider basis only adds roughness at no gain in success. 

## VI. DISCUSSION 

The two components of our method are not interchangeable. The representation lowers within-chunk jerk on both backbones regardless of how the coefficients are produced, but barely reduces the seam. The conditioning removes most of that discontinuity but does not smooth the chunk interior (Section V-D.3). A smooth command requires addressing both sources. 

_a) Scope: one-shot vs. iterative backbones:_ Conditioning is backbone-agnostic, but the gap it must close differs between the two backbones. A fresh DiT chunk starts farther from the anchor than an ACT chunk, about five times farther at the seam (Fig. 3(b)). Because the correction moves the weights of the basis functions that overlap the via-point, it does not stay at the seam but decays over roughly the first third of the chunk (Fig. 3(b)). On DiT this decay starts from a far larger displacement, which is why conditioning leaves a larger residual seam there, one possible reason the executed vibration band does not improve. 

_b) Limitations:_ Blending is the stronger method on the boundary and executed jerk metrics (Section V-D.3). Two properties of our benchmark, however, keep its costs from showing. The tasks are quasi-static with a fixed episode length, so the cost of averaging away the fresh prediction, a delayed reaction, does not register in success rate. The demonstrated motions are also nearly unimodal, so the known failure mode of averaging independently predicted chunks, namely that the average of two valid chunks need not itself be valid [3], cannot show up either. Independently of the benchmark, blending also presupposes an execution schedule that leaves an overlap to average over, whereas conditioning needs only the tail of the previous chunk. Conditioning may also slow the reaction. On Pick-and-Pass, the one task where we measured time-to-success, completion was slower with it, slightly on ACT and by about a 

second on DiT. Part of this may come from our hardware implementation rather than from the conditioning itself, since the conditioned chunk was executed without skipping the inference delay and so lagged the fresh prediction by about two steps on ACT and five to eight on DiT. The executed jerk of DiT with conditioning may be affected for the same reason, in addition to the residual seam noted above. We used Gaussian basis functions following ProMP, but any smooth basis that is linear in the coefficients, such as B- splines [16], can be used in the same way, although we have not tested this. The number of basis functions also limits how fast the command can change within a chunk. On Pickand-Pass this did not change success beyond the seed spread for _n ∈{_ 5 _,_ 10 _,_ 20 _}_ (Section V-E). Since the policy re-plans every 25 steps, faster motions could be accommodated by a larger _n_ or a shorter chunk, at the cost of more within-chunk roughness. Comparisons on tasks with multimodal or faster motion, including perturbation tests, are left for future work. 

## VII. CONCLUSION 

We addressed the two distinct sources of jerk in chunkbased policies by predicting trajectories in a movementprimitive coefficient space. Predicting a chunk as a linear combination of smooth basis functions makes it smooth by construction and sharply reduces within-chunk jerk on both backbones, with task success statistically non-inferior. Conditioning the predicted coefficients on via-points from the previous chunk then removes most of the boundary discontinuity that the representation alone leaves. Unlike asynchronous stitching, the conditioning needs no denoising loop to inpaint into, so it remains available to one-shot policies. A blending baseline suppresses seam jerk further, but only where chunks overlap, and leaves the interior of a rawaction policy rough. These results indicate that smoothness in chunk-based control can be obtained through the prediction target itself, without external filtering or averaging. 

## ACKNOWLEDGMENT 

This work was partially supported by JST Moonshot R&D Grant Number JPMJPS2011 and by the New Energy and Industrial Technology Development Organization (NEDO) under project JPNP26007. T.O. was supported by JSPS KAKENHI Grant Number JP25K03176. Y.K. was supported by JST PRESTO, Japan, Grant Number JPMJPR2612. K.O. was supported by JST SPRING, Grant Number JPMJSP2108. N.S. was supported by JST BOOST, Japan Grant Number JPMJBS2418, and the Teijin Scholarship Foundation. 

- [4] A. Paraschos, C. Daniel, J. R. Peters, and G. Neumann, “Probabilistic movement primitives,” in _Advances in Neural Information Processing Systems_ , vol. 26, 2013. 

- [5] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn, “Learning fine-grained bimanual manipulation with low-cost hardware,” in _Proceedings of Robotics: Science and Systems_ , Daegu, Republic of Korea, July 2023. 

- [6] S. Dasari, O. Mees, S. Zhao, M. K. Srirama, and S. Levine, “The ingredients for robotic diffusion transformers,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , 2025, pp. 15 617–15 625. 

- [7] T. Osa, J. Pajarinen, G. Neumann, J. A. Bagnell, P. Abbeel, and J. Peters, “An algorithmic perspective on imitation learning,” _Foundations and Trends in Robotics_ , vol. 7, no. 1-2, pp. 1–179, 2018. 

- [8] T. Tsuji, Y. Kato, G. Solak, H. Zhang, T. Petriˇc, F. Nori, and A. Ajoudani, “A survey on imitation learning for contact-rich tasks in robotics,” _The International Journal of Robotics Research_ , 2026. 

- [9] D. P. Kingma and M. Welling, “Auto-encoding variational Bayes,” in _Proceedings of the International Conference on Learning Representations (ICLR)_ , 2014. 

- [10] K. Sohn, H. Lee, and X. Yan, “Learning structured output representation using deep conditional generative models,” in _Advances in Neural Information Processing Systems_ , vol. 28, 2015. 

- [11] C. Chi, S. Feng, Y. Du, Z. Xu, E. Cousineau, B. C. Burchfiel, and S. Song, “Diffusion policy: Visuomotor policy learning via action diffusion,” in _Proceedings of Robotics: Science and Systems_ , Daegu, Republic of Korea, July 2023. 

- [12] S. Mysore, B. Mabsout, R. Mancuso, and K. Saenko, “Regularizing action policies for smooth control with reinforcement learning,” in _2021 IEEE International Conference on Robotics and Automation (ICRA)_ , 2021, pp. 1810–1816. 

- [13] A. Ijspeert, J. Nakanishi, and S. Schaal, “Trajectory formation for imitation with nonlinear dynamical systems,” in _Proceedings of the IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , vol. 2, 2001, pp. 752–757. 

- [14] A. J. Ijspeert, J. Nakanishi, H. Hoffmann, P. Pastor, and S. Schaal, “Dynamical movement primitives: Learning attractor models for motor behaviors,” _Neural Computation_ , vol. 25, no. 2, pp. 328–373, 2013. 

- [15] G. Li, Z. Jin, M. Volpp, F. Otto, R. Lioutikov, and G. Neumann, “ProDMP: A unified perspective on dynamic and probabilistic movement primitives,” _IEEE Robotics and Automation Letters_ , vol. 8, no. 4, pp. 2325–2332, 2023. 

- [16] H. Zhou, W. Liao, X. Huang, Y. Tang, F. Otto, X. Jia, X. Jiang, S. Hilber, G. Li, Q. Wang, O.<sup>¨</sup> E. Ya˘gmurlu, N. Blank, M. Reuss, and R. Lioutikov, “BEAST: Efficient tokenization of B-splines encoded action sequences for imitation learning,” in _Advances in Neural Information Processing Systems_ , 2025. 

- [17] P. M. Scheikl, N. Schreiber, C. Haas, N. Freymuth, G. Neumann, R. Lioutikov, and F. Mathis-Ullrich, “Movement primitive diffusion: Learning gentle robotic manipulation of deformable objects,” _IEEE Robotics and Automation Letters_ , vol. 9, no. 6, pp. 5338–5345, 2024. 

- [18] J. Ho, A. Jain, and P. Abbeel, “Denoising diffusion probabilistic models,” in _Advances in Neural Information Processing Systems_ , vol. 33, 2020, pp. 6840–6851. 

## REFERENCES 

> [1] K. Black _et al._ , “ _π_ 0 _._ 5: a vision-language-action model with openworld generalization,” in _Proceedings of The 9th Conference on Robot Learning_ , ser. Proceedings of Machine Learning Research, vol. 305. PMLR, 2025, pp. 17–40. 

> [2] NVIDIA _et al._ , “GR00T N1: An open foundation model for generalist humanoid robots,” arXiv:2503.14734 [cs.RO], 2025. 

> [3] K. Black, M. Galliker, and S. Levine, “Real-time execution of action chunking flow policies,” in _Advances in Neural Information Processing Systems_ , vol. 38, 2025, pp. 33 383–33 407. 

