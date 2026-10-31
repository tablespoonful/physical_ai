---
title: "FastOPD: On-Policy Distillation for Lightweight VLA Deployment"
date: "2026-10-02"
authors: "Yoojin Oh; Jeongsol Kim; Yeonwoo Seo; Jangho Park; Seonghyun Jin; Sunwoo Park"
url: https://arxiv.org/abs/2610.02832
pdf: https://arxiv.org/pdf/2610.02832
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2610.02832)** / [論文ページ](https://arxiv.org/abs/2610.02832)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

Preprint. 

# FASTOPD: ON-POLICY DISTILLATION FOR LIGHTWEIGHT VLA DEPLOYMENT 

**Yoojin Oh**<sup>1</sup><sup>_∗_</sup> **, Jeongsol Kim**<sup>1</sup><sup>_∗_</sup> **, Yeonwoo Seo**<sup>1</sup> **, Jangho Park**<sup>1</sup> **, Seonghyun Jin**<sup>1</sup> **, Sunwoo Park**<sup>1</sup> **, Youngmin Kim**<sup>1</sup> **, Youngjun Jun**<sup>1</sup> **, Kyumin Choi**<sup>2</sup> **, Jong Chul Ye**<sup>1</sup> 1KAIST 2Sungkyunkwan University 

## ABSTRACT 

Vision-Language-Action (VLA) foundation models have scaled rapidly to enhance manipulation performance and generalizability, but this scaling incurs high computational costs that render real-world deployment increasingly challenging. Existing approaches typically mitigate this issue by designing smaller architectures or reducing the iterative denoising steps in flow-based policies. In this work, we propose _FastOPD_ , a foundation-to-lightweight VLA framework that enables the practical deployment of large-scale VLAs through efficient on-policy distillation. Specifically, FastOPD adapts a flow map for single-state teacher supervision and combines it with a self-consistency objective to construct a compact student that learns the teacher dynamics. Furthermore, we theoretically demonstrate that minimizing this objective allows the distilled student to recover a distribution on par with that induced by an ideal few-step teacher model. We evaluate FastOPD across diverse foundation policies in simulation and real-world experiments. On LIBERO, FastOPD retains 84% of the performance of _π_ 0 _._ 5 with only two inference steps, reducing inference latency by 78.1% while outperforming existing few-step distillation baselines in average success rate. With LingBot-VLA as the teacher, FastOPD improves the single-step success rate over the base student by 15.9 percentage points on RoboTwin 2.0. We further demonstrate its applicability to a World Action Model (WAM) and deploy a compact student distilled from MolmoAct2 on a real robot. 


Figure 1: **Foundation-to-lightweight VLA policy distillation with FastOPD.** (Left) Our method enables a small VLA to inherit large-scale VLA knowledge. (Right) FastOPD reaches comparable performance to conventional on-policy distillation (Li et al., 2026a) 5.7 _×_ faster. 

## 1 INTRODUCTION 

Recent progress in robot learning has moved toward large-scale foundation policies, ranging from Vision-Language-Action (VLA) models (Collaboration, 2024; Black et al., 2025b;a; Bjorck et al., 2025; Wu et al., 2026; Fang et al., 2026a) to emerging World Action Models (WAMs) (Kim et al., 2026; Ye et al., 2026; Yuan et al., 2026). In particular, recent methods such as DreamZero (Ye et al., 2026) and Cosmos Policy (Kim et al., 2026) leverage pretrained video generation models 

Project page is available here. 

*Equal contribution. 

1 

Preprint. 


Figure 2: **Comparison between DiffusionOPD and FastOPD.** (a) DiffusionOPD evaluates teacher at every denoising step. (b) FastOPD evaluates teacher at a single sampled state reached by a flowmap jump from noise. Blue arrows denote student transitions; red arrows denote teacher velocities. 

to capture rich visual dynamics and achieve strong generalization and manipulation performance. However, these powerful foundation priors also lead to increasingly large policy backbones and high computational cost, creating a tension between model capability and deployment efficiency on physical robots. Lightweight VLA models such as SmolVLA (Shukor et al., 2025) address the efficiency side of this trade-off by directly designing smaller policies with less than 0.5B parameters. 

A complementary direction is to transfer the capability of a powerful foundation policy into a compact student through knowledge distillation. Knowledge Distillation (KD) (Hinton et al., 2015; Mansourian et al., 2025) has been widely studied for transferring the capability of a large teacher model into a smaller student. Specifically, On-Policy Distillation (OPD) (Agarwal et al., 2024) supervises the student using teacher predictions on its own generated trajectories, reducing distribution mismatch and compounding errors from offline distillation. OPD also provides dense supervision along the student trajectory, in contrast to the sparse rewards commonly used in reinforcement learning. While OPD has been actively explored in LLM post-training, recent works have extended it to diffusion and flow models (Li et al., 2026a; Fang et al., 2026b). However, directly applying OPD to flow-based policies is computationally inefficient. It requires rolling out the student’s denoising trajectory and repeatedly evaluating the teacher at the visited timesteps, resulting in high training cost for large foundation teachers. 

In this work, we revisit few-step flow-map models through the lens of on-policy distillation (OPD) and introduce **FastOPD** , a foundation-to-lightweight VLA framework for efficient policy distillation. Our goal is to transfer the capabilities of a large-scale VLA into a compact student while substantially reducing both training and inference costs, without sacrificing policy performance (see Fig. 1). To reduce the training cost of conventional OPD, FastOPD combines on-policy teacher supervision of the student’s velocity field with a self-consistency objective (Frans et al., 2025). Rather than querying teacher supervision throughout an entire generation trajectory, the self-consistency objective propagates local velocity supervision to finite-interval shortcut transitions, as illustrated in Fig. 2. This allows the student to approximate the teacher dynamics without explicitly constructing or evaluating a teacher flow map over each shortcut transition. We further show theoretically that FastOPD implicitly recovers the distribution induced by the teacher’s ideal shortcut model, providing a distributional justification for few-step distillation. 

Importantly, the same self-consistency formulation naturally induces an any-step flow map (Boffi et al., 2024; Song et al., 2023; Kim et al., 2024; Geng et al., 2025; Sabour et al., 2025), allowing the distilled student to operate with substantially fewer sampling steps at inference. FastOPD therefore compresses the foundation VLA along two complementary dimensions: model capacity and sampling complexity, enabling deployment on resource-constrained, consumer-grade hardware. The proposed formulation also enables stable training in the challenging few-step regime without adversarial objectives or costly higher-order derivative computations. A concurrent work, VLAOPD (Zhong et al., 2026), also studies on-policy distillation for VLA models, but primarily uses expert supervision to improve policy performance. In contrast, FastOPD focuses on transferring a foundation policy into a lightweight few-step student. 

We evaluate FastOPD on two simulation benchmarks and one real-world manipulation task, using diverse foundation teachers with 3B–6B parameters (Black et al., 2025a; Yuan et al., 2026; Fang et al., 2026a). To maximize both architectural and inference efficiency, we adopt SmolVLA as 

2 

Preprint. 

the lightweight student policy. We compare against representative few-step distillation methods, including CTM, DMD, and iMF. Across these settings, FastOPD enables the compact student to recover up to 84% of the performance of teacher models that are more than 7 _._ 3 _×_ larger, using only one or two sampling steps. This substantially reduces inference cost while retaining a large fraction of the foundation policy’s performance. To the best of our knowledge, FastOPD is the first OPD framework for VLAs that jointly reduces both model size and the number of sampling steps while retaining the capabilities of a large-scale foundation policy. 

## 2 BACKGROUND 

**Flow-based Models.** Diffusion and flow-based models (Song et al., 2021; Ho et al., 2020; Esser et al., 2024; Lipman et al., 2023) generate high-quality samples through iterative denoising. Let _p_ 1 = _N_ ( **0** _,_ **I** ) be a Gaussian prior and _p_ 0 the context-conditioned data distribution over actions. Flow matching (Lipman et al., 2023; Esser et al., 2024) defines a stochastic interpolant **_x_** _t_ = (1 _− t_ ) **_x_** 0 + _t_ **_x_** 1, with **_x_** 0 _∼ p_ 0, **_x_** 1 _∼ p_ 1 _, t ∈_ [0 _,_ 1], and learns the marginal velocity field **_v_** ( **_x_** _, t_ ) := E[ **_x_** 1 _−_ **_x_** 0 _|_ **_x_** _t_ = **_x_** ] via 


Sampling integrates the probability-flow ODE **_x_** ˙ _t_ = **_v_** ( **_x_** _t, t_ ) from _t_ = 1 to _t_ = 0 , for example, with Euler steps, **_x_** _ti_ = **_x_** _ti−_ 1 + **_v_** ( **_x_** _ti−_ 1 _, ti−_ 1) ∆ _t_ where ∆ _t_ := _ti − ti−_ 1. While these models capture high-quality multimodal action distributions, accurate integration typically requires many denoising steps, motivating few-step distillation for faster inference. 

**Vision-Language-Action Models.** Vision-Language-Action (VLA) models (Collaboration, 2024; Black et al., 2025b;a; Bjorck et al., 2025; Wu et al., 2026; Liu et al., 2024; Octo Model Team et al., 2024) couple a pretrained vision-language backbone with an action decoding head to map an observation and a language instruction to a distribution over robot actions, most commonly via a flow or diffusion action expert (Chi et al., 2023; Black et al., 2025b) trained with flow matching loss. Recent foundation VLA models illustrate the scale required for strong multi-task generalization, typically exceeding 2B parameters and trained on over 10,000 hours of multimodal robot data spanning multiple embodiments (Black et al., 2025b;a; Wu et al., 2026), but remain expensive to deploy. Several works (Octo Model Team et al., 2024; Shukor et al., 2025; Wen et al., 2025; Reuss et al., 2025) instead train smaller VLAs; SmolVLA (Shukor et al., 2025), for example, reduces model size to 450 million parameters by using a small VLM and layer skipping. However, it still requires _N_ =10 denoising steps per action chunk and does not benefit from the capabilities of larger foundation policies. 

**Flow Map Models.** A wide range of few-step generative methods aim to reduce iterative sampling cost. Distillation-based approaches (Sabour et al., 2025; Boffi et al., 2024), including Consistency Models (CM) (Song et al., 2023), and Consistency Trajectory Models (CTM) (Kim et al., 2024), distill a pre-trained multi-step teacher into a few-step student, while score-distillation methods directly match teacher and student distributions (Yin et al., 2024b;a). Distillation-free approaches, such as MeanFlow (MF) (Geng et al., 2025) and Shortcut Models (Frans et al., 2025), instead train from scratch using self-consistency constraints. A flow map model **_f_** _θ_ ( **_x_** _, s, t_ ) parameterizes the state-to-state transition over an arbitrary interval [ _s, t_ ] _⊂_ [0 _,_ 1], so that a single jump **_f_** _θ_ ( **_x_** _s, s, t_ ) = **_x_** _s_ + ( _t − s_ ) **_u_** _θ_ ( **_x_** _s, s, t_ ) at the interpolant **_x_** _s_ = (1 _− s_ ) **_x_** 0 + _s_ **_x_** 1 replaces an entire sequence of Euler substeps. For example, Frans et al. (2025) combines flow matching loss with the self-consistency constraint at the midpoint time _m_ = ( _s_ + _t_ ) _/_ 2: 


The first term enforces standard flow matching, while the second encourages the direct transition from _s_ to _t_ to agree with two shorter transitions composed through _m_ . In robot manipulation, these ideas have been adapted to accelerate diffusion- and flow-based policies such as Diffusion Policy (Chi et al., 2023). Consistency Policy (CP) (Prasad et al., 2024) adapts CTM (Kim et al., 2024); OneDP (Wang et al., 2025) and SDM Policy (Jia et al., 2024) use distribution matching for one-step action generation; and recent methods learn average velocity fields (Geng et al., 2025; 2026; Sheng et al., 2026; Guo et al., 2026) or shortcut objectives (Frans et al., 2025; Luan et al., 2026; Yan et al., 2025; Li et al., 2026b) regularized by flow matching. For instance, SnapFlow (Luan et al., 2026) constructs its target from two Euler steps but trains only on fixed endpoints, while OFP (Li 

3 

Preprint. 


Figure 3: **Overview of FastOPD.** (a) Flow Map Architecture: a frozen vision-language backbone with a lightweight action expert. A time projection layer _ψ_ ( _·_ ) fuses ( _s, t_ ) to condition the action expert on the two-time velocity **_u_** _θ_ ( **_x_** _s, s, t_ ). (b) On-Policy Flow Map Distillation Loss: at a single on-policy jump **_x_** ˜ _t_ = **_f_** _θ_ ( **_x_** 1 _,_ 1 _, t_ ), the student’s diagonal velocity is matched to the teacher’s. (c) Self-Consistency Loss: a direct transition **_u_** _θ_ ( **_x_** _s, s, t_ ) is trained to agree with two steps through the midpoint _m_ . 

et al., 2026b) derives its target from nested sub-intervals with a self-guided regularizer. Despite these advances, few-step policies often suffer from training instability and degraded quality as the number of denoising steps decreases. This trade-off is particularly critical in robot manipulation, where low latency must be achieved without sacrificing the precision and stability required for physical execution, and still remains insufficiently addressed (Shukor et al., 2025). 

**On-policy Distillation.** Given a pretrained teacher diffusion model, on-policy distillation (OPD) supervises the student to match the teacher’s one-step transition kernel _pT_ ( _· |_ **_x_** _ti_ ) along the student’s own rollout **_x_** 0: _N ∼ pS,θ_ , by minimizing the reverse KL objective (Li et al., 2026a). Since the student and teacher share the same diffusion coefficient, resulting in identical covariance, its per-step KL reduces to a closed-form squared distance between the means, KL( _pS∥pT_ ) _∝ ∥µS_ ( **_x_** _ti_ ; _θ_ ) _− µT_ ( **_x_** _ti_ ) _∥_ 2<sup>2.Despiteprovidingdensesupervision,thisobjectivenecessitatesevalu-</sup> ating the teacher at every single denoising step, resulting in computational inefficiency. FastOPD circumvents this training bottleneck by supervising the student at a single on-policy state per trajectory. Formulated within a few-step flow map regime, the distilled policy is naturally equipped for real-time robot control. 

## 3 FASTOPD: FAST ON-POLICY DISTILLATION 

**Overview.** Our goal is to efficiently distill a large pretrained teacher **_v_** _ϕ_ into a compact flow map student **_u_** _θ_ , while achieving performance on par with the teacher. Specifically, we parameterize the flow map as **_f_** _θ_ ( **_x_** _, s, t_ ) = **_x_** +( _t − s_ ) **_u_** _θ_ ( **_x_** _, s, t_ ), which satisfies the boundary condition **_f_** _θ_ ( **_x_** _, s, s_ ) = **_x_** . We denote its diagonal by **_v_** _θ_ ( **_x_** _, t_ ) := **_u_** _θ_ ( **_x_** _, t, t_ ), which corresponds to the instantaneous velocity. As illustrated in Fig. 3, we embed _s_ and _t_ independently via sinusoidal positional encoding and fuse them through an additional projection layer _ψ_ ( _·_ ). Here, we omit the condition _c_ for brevity. 

The key idea of FastOPD is to match the teacher only at sampled on-policy states and propagate this local velocity supervision to finite-step flow maps through self-consistency. Accordingly, FastOPD jointly optimizes on-policy velocity matching and finite-interval self-consistency: 


Here, sg[ _·_ ] denotes the stop-gradient operator, and **_x_** ˜ _t_ denotes a sampled on-policy state, while **_x_** ˆ _m_ denotes the midpoint state induced by the student. We next describe how the two terms implement local teacher matching and its propagation to finite-step flow maps. 

4 

Preprint. 

**On-policy Flow Map Distillation.** We first consider how to efficiently transfer the teacher dynamics to the student. Conventional flow-based OPD evaluates the teacher at every denoising step along the student trajectory, resulting in substantial computational overhead. Instead, we supervise the student at a single sampled on-policy state per trajectory (see Fig. 3(b)). Specifically, we obtain the state with a single flow-map transition from noise, **_x_** ˜ _t_ = sg� **_f_** _θ_ ( **_x_** 1 _,_ 1 _, t_ )�, which induces the on-policy marginal **_x_** ˜ _t ∼ pθ_ . We then match the teacher and student transitions only at this sampled timestep _t_ . Let _pθ_ ( _· |_ **_x_** ˜ _t_ ) and _pϕ_ ( _· |_ **_x_** ˜ _t_ ) denote the corresponding one-step transition kernels of the student and teacher, respectively. We formulate the _single-state transition matching_ objective as 


For a flow map, the instantaneous velocity on the diagonal coincides with the underlying velocity field under the tangent condition (Boffi et al., 2025)<sup>1</sup> . Using this identity, the reverse KL in Eq. (4) can be expressed directly in terms of the student and teacher velocity fields, as shown in the following proposition. 

**Proposition 1** (On-policy Flow Map Distillation) **.** _Let σt >_ 0 _be a diffusion coefficient. For any t ∈_ (0 _,_ 1) _and step_ ∆ _t <_ 0 _, the Euler–Maruyama kernels induced by_ **_u_** _θ_ ( _·, t, t_ ) _and_ **_v_** _ϕ_ ( _·, t_ ) _satisfy_ 


Proposition 1 reduces the single-state transition matching objective to a weighted velocity regression. We therefore define the practical on-policy flow map distillation (OPFD) objective as 


Eq. (6) can be viewed as the pointwise version of the original distribution matching in Eq. (4), since it is characterized by a deterministic flow ODE. We set the weighting function _wσ_ ( _t,_ ∆ _t_ ) to 1 in practice, following Li et al. (2026a). Full derivation is provided in Appendix A. 

**Self-consistency Property.** OPFD transfers the teacher velocity to the student’s diagonal flow map **_u_** _θ_ ( **_x_** _, t, t_ ), but our goal is to learn a flow map over arbitrary finite interval ( _s, t_ ) at the same time. We therefore propagate this local teacher supervision to finite-step transitions through self-consistency (see Fig. 3(c)). Following Shortcut Models (Frans et al., 2025), a direct transition from _s_ to _t_ should agree with two consecutive shorter transitions through the midpoint _m_ = ( _s_ + _t_ ) _/_ 2. Unlike the original shortcut formulation, we construct the target using the _instantaneous_ velocities at the diagonals of the two sub-intervals, **_v_** _θ_ ( **_x_** _s, s_ ) and _vθ_ (ˆ **_x_** _m, m_ ), as follows: 


where **_x_** ˆ _m_ := **_x_** _s_ + ( _m − s_ ) **_v_** _θ_ ( **_x_** _s, s_ ). 

The resulting target is anchored to teacher-supervised quantities at every interval. Note that the diagonal terms coincide with the quantities directly supervised by OPFD. Accordingly, we define the training objective as 


In the following theorem, we demonstrate that the student implicitly recovers the teacher-induced flow map. Let **_v_** _ϕ_ ( **_x_** _, t_ ) be the teacher velocity field, and we define the teacher-induced ideal shortcut as 

**_u_** _ϕ_ ( **_x_** _, s, t_ ) =<sup><u>1</u></sup> 2 � **_v_** _ϕ_ ( **_x_** _, s_ ) + **_v_** _ϕ_ (¯ **_x_** _m, m_ )� _,_ **_x_** ¯ _m_ = **_x_** + ( _m − s_ ) **_v_** _ϕ_ ( **_x_** _, s_ ) _,_ (9) with **_u_** _ϕ_ ( **_x_** _, t, t_ ) = **_v_** _ϕ_ ( **_x_** _, t_ ). We then define the corresponding ideal flow map as **_f_** _ϕ_ ( **_x_** _, s, t_ ) = **_x_** + ( _t − s_ ) **_u_** _ϕ_ ( **_x_** _, s, t_ ). 

**Proposition 2.** _Let qθ and ρθ be the sampling distributions of LSC and LOPFD. Assume that_ **_v_** _ϕ_ ( _·, t_ ) _is L-Lipschitz and that_ ( _s,_ **_x_** _s_ ) _and_ ( _m,_ ˆ **_x_** _m_ ) _under qθ have density ratio at most κ with respect to ρθ. Then,_ 


> 1lim _s→t ∂t_ **_f_** _θ_ ( **_x_** _, s, t_ ) = **_u_** _θ_ ( **_x_** _, t, t_ ) = **_v_** _θ_ ( **_x_** _, t_ ) 

5 

Preprint. 

**Algorithm 1** Training Algorithm for FastOPD 

**Require:** Dataset _D_ ; Pretrained teacher **_v_** _ϕ_ ; student flow map **_u_** _θ_ with time embedding layer _ψ_ ( _·_ ); OPFD weight _λ_ ; Sampling time distribution _p_ 1: **for** each training iteration **do** 2: **_x_** 1 _∼N_ ( **0** _,_ **I** ) _, τ ∼ p,_ ( **_x_** 0 _, c_ ) _∼D_ 3: **_x_** ˜ _τ ←_ sg� **_f_** _θ_ ( **_x_** 1 _,_ 1 _, τ_ )� 4: _L_ OPFD _←∥_ **_v_** _θ_ (˜ **_x_** _τ , τ | c_ ) _−_ **_v_** _ϕ_ (˜ **_x_** _τ , τ | c_ ) _∥_ 2<sup>2</sup> _▷ single on-policy state supervision_ 5: _s, t ∼ p_ with _s > t_ 6: _m ←_ ( _s_ + _t_ ) _/_ 2, **_x_** _s ←_ (1 _− s_ ) **_x_** 0 + _s_ **_x_** 1 7: **_x_** ˆ _m ←_ **_x_** _s_ + ( _m − s_ ) sg� **_v_** _θ_ ( **_x_** _s, s | c_ )� 8: _L_ SC _←_ �� **_u_** _θ_ ( **_x_** _s, s, t | c_ ) _−_ <u>12</u> �sg[ **_v_** _θ_ ( **_x_** _s, s | c_ )] + sg[ **_v_** _θ_ (ˆ **_x_** _m, m | c_ )]���22 9: _L_ FastOPD _←L_ SC + _λ L_ OPFD 10: _θ ← θ − η ∇θL_ FastOPD 11: **end for** 

Thus, OPFD transfers the teacher’s instantaneous velocity to the student, while self-consistency propagates this agreement from the diagonal velocity to finite-step shortcut maps. 

**Theorem 1.** _Let pθ and pϕ denote the terminal distributions induced by sampling with_ **_f_** _θ and_ **_f_** _ϕ, respectively, from the same initial noise on a fixed sampling schedule_ 1 = _t_ 0 _> t_ 1 _> · · · > tK_ = 0 _, and let_ **_x_**<sup>_θ_</sup> _tk_<sup>_denote the intermediate states of the student.Suppose that the assumptions of_</sup> _Proposition 2 hold and there exists finite κ_ roll _>_ 0 _such that, for every k,_ 


_Then,_ 


_where C >_ 0 _depends only on L, κ, κ_ roll _, λ, and the sampling schedule._ 

Consequently, _W_ 2( _pθ, pϕ_ ) _→_ 0 as _L_ FastOPD _→_ 0. Since **_u_** _ϕ_ is built entirely from the pretrained teacher’s velocity field, _pϕ_ is the few-step distribution induced by the teacher-induced flow map on the same sampling schedule. The theorem therefore shows that FastOPD allows the compact student to implicitly recover this distribution without explicitly constructing a shortcut teacher. The detailed algorithm for FastOPD is presented in Algorithm 1. 

## 4 EXPERIMENTS 

Our experiments span two multitask simulation benchmarks (Sec. 4.1) and one real-robot task (Sec. 4.2). We freeze the vision–language backbone and fine-tune only the action expert and projections with the additional time projection layer described in Sec. 3. We evaluate each method using 1, 2, 4, and 10 denoising steps and compare it against the teacher and the initial student with 50 trials per task. Full experimental details are provided in Appendix B. 

### 4.1 SIMULATION EXPERIMENTS 

**Benchmarks.** We evaluate FastOPD on LIBERO (Liu et al., 2023) and RoboTwin 2.0 (Chen et al., 2025). LIBERO evaluates single-arm manipulation across four standard evaluation suites—Spatial, Object, Goal, and Long—comprising 40 tasks in total. RoboTwin 2.0 (Chen et al., 2025) comprises 50 challenging bimanual manipulation tasks, with 2,500 demonstrations collected in clean scenes and 25,000 demonstrations collected under heavy scene randomization. We report results in both clean and randomized settings on unseen environments. 

**Baselines.** For simulation experiments, we compare our method with three representative approaches to few-step generation: Consistency Trajectory Model (CTM) (Kim et al., 2024), Distribution Matching Distillation (DMD) (Yin et al., 2024b;a), and improved Mean Flow (iMF) (Geng et al., 2026). Since iMF was originally formulated for training from scratch, we adapt it to the distillation setting by replacing its self-referential instantaneous velocity target with the teacher velocity. Except for DMD, a one-step generator, all baselines are designed as the flow-map architecture. 

6 

Preprint. 

Table 1: Success rates (%) on LIBERO across spatial, object, goal, and long-horizon tasks. _†_ : Results reported in the original papers. 

Table 2: Success rates (%) on RoboTwin 2.0 under unseen clean and randomized settings. _†_ : Results reported in the original papers. 

|**Method**|**Param.**|**NFE**|**Spat.**|**Obj.**|**Goal**|**Long**|**Avg.**|**Method**|**Param.**|**NFE**|**Clean**|**Rand.**|**Avg.**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Diffusion/F**|**low-based**|**Policie**|**s**|||||**Diffusion/Flow-based**|**Policies**|||||
|||||||||DP<sup>_†_</sup>|046B|10|280|06|143|
|DP<sup>_†_</sup>|–|100|78.3|92.5|68.3|50.5|72.4||.||.|.|.|
|Octo-Base<sup>_†_</sup><br>|93M|10|78.9|85.7|84.6|51.1|75.1|RDT<sup>_†_</sup><br>_π_0<br>_†_|1.2B<br>33B|10<br>10|34.5<br>464|13.7<br>163|24.1<br>314|
|_π_0<br>_†_|3.3B|10|97.4|98.4|97.6|93.0|96.6|_π_0_._5|.<br>3.3B|10|.<br>70.7|.<br>46.0|.<br>58.4|
|**Teacher &**|**Base Stude**|**nt Mod**|**els**|||||**Teacher & Base Stude**|**nt Models**|||||
|_π_0_._5|3.3B|10|98.2|99.4|97.4|94.8|97.5|LingBot-VLA<br>|4.2B<br>|10<br>|86.8<br>|84.9<br>|85.8<br>|
|SmolVLA|450M|1|74.6|73.2|77.4|51.2|69.1|Fast-WAM<br>SmolVLA|6B<br>450M|10<br>1|91.9<br>35.2|91.8<br>35.4|91.9<br>35.3|
|||2|76.8|74.4|79.8|54.4|71.4|||2|55.0|56.1|55.6|
|||4|79.0|74.8|79.2|58.0|72.8|||4|59.8|61.0|**60.4**|
|||10|77.2|75.0|79.4|54.6|71.6|||10|59.4|61.3|**60.4**|
|**Few-step Di**|**stillation**|||||||**Few-step Distillation**||||||
|||||||||DMD|450M|1|32.5|32.1|32.3|
|DMD|450M|1|82.4|87.2|75.6|47.2|73.1|CTM|451M|1|15.5|15.6|15.6|
|CTM|451M|1|78.0|86.6|70.8|41.4|69.2|||2|4.8|15.8|10.3|
|||2|75.4|84.2|70.4|43.4|68.4|||4<br>|18.7<br>|16.0<br>|17.3<br>|
|||4|68.4|77.0|71.2|45.0|65.4|iMF|451M|10<br>1|36.1<br>43.2|34.5<br>42.4|35.3<br>42.8|
|||10|72.0|81.6|72.4|44.4|67.6|||2|51.6|51.1|51.4|
|iMF|451M|1|70.8|78.6|75.6|30.6|63.9|||4|50.8|51.0|50.9|
|||2|76.0|90.6|75.6|46.4|72.2|||10|50.6|51.4|51.0|
|||||||||**Ours (LingBot-VLA)**|451M|1|51.5|50.9|**51.2**|
|||4|68.2|84.8|67.0|38.0|64.5|||2|57.1|58.3|**57.7**|
|||10|65.2|83.6|66.6|35.2|62.7|||4|58.6|61.2|59.9|
|**Ours**|451M|1|84.2|94.2|82.6|48.2|**77.3**|||10|56.9|59.6|58.2|
|||2|83.6|96.8|87.2|59.6|**81.8**|**Ours (Fast-WAM)**|451M|1<br>|51.1<br>|49.8<br>|50.5<br>|
|||4|83.0|95.0|85.6|57.4|**80.3**|||2<br>4|55.5<br>58.5|57.2<br>59.2|56.3<br>58.8|
|||10|80.4|94.0|84.4|57.2|**79.0**|||10|58.3|59.6|58.9|


Table 3: End-to-end inference latency (ms) on LIBERO and RoboTwin 2.0. 

||**LIB**|**ERO**||||**RoboTwin 2.**|**0**|||
|---|---|---|---|---|---|---|---|---|---|
|**Model**|**NFE=1**|**2**|**4**|**10**|**Model**|**NFE=1**|**2**|**4**|**10**|
|_π_0_._5 (teacher)|155|171|203|301|LingBot-VLA (teacher)|151|197|291|571|
||||||Fast-WAM (teacher)|147|186|264|503|
|SmolVLA|49|65|97|193|SmolVLA|56|72|103|199|
|**Ours**|50|66|98|193|**Ours**|57|74|106|202|


**Teacher and Student Models.** We use SmolVLA (Shukor et al., 2025) as the student model on both benchmarks, paired with _π_ 0 _._ 5 (Black et al., 2025a) on LIBERO, LingBot-VLA (Wu et al., 2026) and Fast-WAM (Yuan et al., 2026) on RoboTwin 2.0. All models are initialized from public benchmark-specific checkpoints. 

**LIBERO.** In Tab. 1 and Tab. 3, we report (a) (b) the average success rates and inference latency on the LIBERO benchmark. Our method outperforms all few-step baselines and the initial student model at every denoising step in average success rate. As ~~1-step~~ Init ~~10-steps~~ 4-steps Ours iMF shown in Fig. 4, we observe a consis2-steps DMD CTM tent performance improvement across all Training Step Training Step denoising steps, including at 10 steps. Figure 4: Success rate (%) on LIBERO during training: FastOPD further achieves the best success (a) FastOPD at different sampling steps, (b) comparirates of 81.8% with only 2 sampling steps. son with baselines at 1 step. In particular, our method shows better performance than the 10-step SmolVLA baseline with only a single step, while reducing inference latency from 193 ms to 50 ms. Together, the results demonstrate that FastOPD substantially improves the accuracy–latency trade-off of the compact student. We examine the contributions of each loss component to these accuracy gains in Sec. 4.3. 

7 

Preprint. 

**RoboTwin 2.0.** Tab. 2 and Tab. 3 summarize the results. Notably, our method consistently achieves performance gains in the few-step regime, improving the single-step success rate of the base student from 35.3% to 51.2%, and outperforms all few-step distillation baselines at every sampling step. It does so at a latency comparable to SmolVLA, while being 10 _._ 0 _×_ faster than the LingBot-VLA teacher. At 4 and 10 steps, FastOPD performs slightly below the base student, indicating that its benefit lies mainly in the few-step regime where the base student degrades. 

**Distilling a World Action Model.** Recent World Action Models (WAMs) build on pretrained video generation models and have emerged as an alternative to foundation VLAs (Kim et al., 2026; Ye et al., 2026; Yuan et al., 2026). To examine whether FastOPD extends beyond VLA teachers, we distill Fast-WAM (Yuan et al., 2026), a 6B-parameter video-based teacher, into the same 451M SmolVLA student with an identical training recipe. As shown in Tab. 2, the student distilled from Fast-WAM achieves a 50.5% average success rate at a single denoising step, 15.2 percentage points over the initial SmolVLA baseline (35.3%). Furthermore, it reaches 56.3% at two steps, successfully transferring knowledge despite the substantial differences in architecture and pretraining between the teacher and the student. This demonstrates that FastOPD is a versatile approach that applies not only to VLAs but also to WAMs, since it only requires the teacher’s velocity field on the student’s own action trajectories, regardless of how the teacher is built. 

### 4.2 REAL-WORLD EXPERIMENTS 


To validate its real-world applicability, we further design a real-world robot scenario, pnp-plate, in which the robot picks up the ball and places it on the plate. Experiments use the right arm of a bimanual YAM robot with a parallel-jaw gripper and top-view and wrist-mounted cameras that provide RGB observations. We train MolmoAct2 (Fang et al., 2026a), an action reasoning model that is suitable for real-world deployment, on our collected demonstrations for 14,000 iterations and use the resulting policy as the teacher. We initialize the student from SmolVLA, warm it up on the collected demonstrations with the standard flow matching objective (i.e., behavior cloning) for 10,000 iterations, and subsequently distill the teacher into the student using FastOPD. Full experimental details are provided in Appendix B.5. 

Figure 5: Real-world results on the pnp-plate task. (a) Success rate (%). (b) Task completion time (s), averaged over successful episodes. 


Figure 6: FastOPD on pnp-plate:: (a) start, (b) transport, and (c) placement. Each panel shows the top view with the wrist view inset (lower left). 

Fig. 5 and Fig. 6 summarize the reFigure 6: FastOPD on pnp-plate:: (a) start, (b) sults. With four denoising steps, FastOPD transport, and (c) placement. Each panel shows the top achieves a 50% success rate, improving by view with the wrist view inset (lower left). 8 percentage points over the 42% of the base SmolVLA at the same number of steps. Notably, FastOPD shows faster and more accurate performance than the 10-step base student, improving the success rate from 44% to 50% while cutting the execution time from 19.32 s to 17.38 s. These results demonstrate that FastOPD can transfer the capability of a larger teacher to a compact student deployed on a physical robot with few steps. 

### 4.3 ABLATION STUDY 

**Training efficiency.** FastOPD reduces training overhead by supervising the student at a single sampled on-policy state rather than across all denoising steps. As illustrated in Fig. 1, standard OPD (Li et al., 2026a) takes 9.51 hours per 1,000 training iterations while FastOPD requires only 1.43 hours, achieving a 5 _._ 7 _×_ speedup. This translates directly into accelerated convergence (Fig. 1). FastOPD achieves a 78.2% 1-step success rate in just 10 hours, whereas conventional OPD requires 

8 

Preprint. 

Table 4: Student initialization. Table 5: Loss components. Table 6: Effect of _λ_ . 

|**Method**|**1**|**2**|**4**|**10**|**Method**|**1**|**2**|**4**|**10**|_λ_|**1**|**2**|**4**|**10**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|FM init.|69.1|71.4|72.8|71.6|Base|69.1|71.4|72.8|71.6|1|77.9|82.0|83.6|82.1|
|+ FastOPD|77.3|81.8|80.3|79.0|SC only|14.5|15.7|17.8|16.8|0.5|79.3|82.9|**84.2**|**84.1**|
|OPD init.|72.7|78.2|44.2|78.6|OPFD only|25.0|52.6|64.0|74.7|0.1|**80.5**|**83.0**|82.2|81.7|
|+ FastOPD|**80.5**|**83.0**|**82.2**|**81.7**|**FastOPD**|**77.3**|**81.8**|**80.3**|**79.0**|0.01|53.0|52.6|52.9|52.0|


roughly 57 hours to reach a similar level (79.1%). Consequently, FastOPD matches the performance of conventional OPD at a fraction of the computational cost. 

**Student Initialization.** We study whether FastOPD can also start from a student that is initialized in a fully on-policy manner. To do so, we initialize the student using 5,000 iterations of conventional per-step OPD (Li et al., 2026a) instead of flow-matching behavior cloning. As shown in Tab. 4, the OPD-initialized student degrades severely at 4 steps (44.2%), likely due to the fixed 10-step discretization in OPD, whereas FastOPD recovers this case and improves all denoising steps. This indicates that OPD is a viable alternative to flow-matching-based behavior cloning for the initialization, although it incurs a substantially higher training cost, as discussed above (Fig. 1). It also shows that FastOPD is not tied to a specific initialization and can be applied on top of students distilled by other methods. 

**Loss components.** Tab. 5 shows that the two objectives are complementary. Without teacher anchoring, SC alone collapses below 18% and OPFD alone fails to capture off-diagonal flow dynamics, degrading few-step generation. Their combination reaches 81.8% with two steps. While Luan et al. (2026) also anchors a fixed two-step Euler target with flow matching, FastOPD anchors to the teacher via OPFD and enforces consistency over arbitrary intervals, yielding an any-step flow map that inherits the teacher’s dynamics (see Appendix C). 

**Hyperparameters.** The proposed method introduces a single hyperparameter _λ_ , which controls the strength of the OPFD term. To study its effect, we sweep the OPFD weight _λ ∈{_ 1 _,_ 0 _._ 5 _,_ 0 _._ 1 _,_ 0 _._ 01 _}_ on the OPD-initialized student (Tab. 6). Performance collapses at _λ_ = 0 _._ 01, indicating that sufficient OPFD supervision is needed to anchor the self-consistency term, and remains stable within [0 _._ 1 _,_ 0 _._ 5] with a mild trade-off between few- and multistep performance. 


**Action execution steps.** The policy executes the first _K_ actions of each predicted chunk before replanning, trading responsiveness for inference overhead. Short execuAction Steps tion horizons improve responsiveness through more freFigure 7: Ablation on action execution quent replanning, while longer horizons reduce inference steps on LIBERO (NFE=2 for Ours and overhead at the cost of extended open-loop execution. As NFE=10 for _π_ 0 _._ 5). shown in Fig. 7, we observe that both the teacher _π_ 0 _._ 5 and the student perform best at _K_ = 10, suggesting that the student inherits the teacher’s preferred replanning frequency. 

## 5 CONCLUSION 

In this paper, we present FastOPD, an efficient on-policy distillation framework that transfers largescale VLAs into lightweight student models to maximize computational efficiency without compromising performance. Specifically, FastOPD streamlines the iterative denoising process by anchoring a single on-policy state to the teacher, coupled with a self-consistency objective for finiteinterval transitions. In simulation and real-robot experiments across diverse VLA and WAM teachers, FastOPD improves over the base student in the few-step regime and outperforms existing fewstep distillation methods, while substantially reducing training and inference cost. We hope this framework facilitates scalable, real-time deployment of foundation policies on physical robots. 

9 

Preprint. 

## REFERENCES 

- Rishabh Agarwal, Nino Vieillard, Yongchao Zhou, Piotr Stanczyk, Sabela Ramos Garea, Matthieu Geist, and Olivier Bachem. On-policy distillation of language models: Learning from selfgenerated mistakes. In _International Conference on Learning Representations_ , 2024. 

- Johan Bjorck, Fernando Casta˜neda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. GR00T N1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Robert Equi, Chelsea Finn, Niccolo Fusai, et al. _π_ 0 _._ 5: A vision-language-action model with open-world generalization. In _Proceedings of the 9th Conference on Robot Learning_ , volume 305 of _Proceedings of Machine Learning Research_ , pp. 17–40. PMLR, 2025a. 

- Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Robert Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A vision-language-action flow model for general robot control. In _Robotics: Science and Systems_ , 2025b. 

- Nicholas Boffi, Michael Albergo, and Eric Vanden-Eijnden. How to build a consistency model: Learning flow maps via self-distillation. _Advances in Neural Information Processing Systems_ , 38: 37559–37595, 2025. 

- Nicholas M Boffi, Michael S Albergo, and Eric Vanden-Eijnden. Flow map matching with stochastic interpolants: A mathematical framework for consistency models. _arXiv preprint arXiv:2406.07507_ , 2024. 

- Remi Cadene, Simon Alibert, Alexander Soare, Quentin Gallouedec, Adil Zouitine, Steven Palma, Pepijn Kooijmans, Michel Aractingi, Mustafa Shukor, Dana Aubakirova, Martino Russi, Francesco Capuano, Caroline Pascal, Jade Choghari, Khalil Meftah, Maxime Ellerbach, Jess Moss, and Thomas Wolf. LeRobot: State-of-the-art machine learning for real-world robotics in Pytorch. https://github.com/huggingface/lerobot, 2024. 

- Tianxing Chen, Zanxin Chen, Baijun Chen, Zijian Cai, Yibin Liu, Zixuan Li, Qiwei Liang, Xianliang Lin, Yiheng Ge, Zhenyu Gu, et al. RoboTwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. _arXiv preprint arXiv:2506.18088_ , 2025. 

- Cheng Chi, Siyuan Feng, Yilun Du, Zhenjia Xu, Eric Cousineau, Benjamin Burchfiel, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. In _Robotics: Science and Systems_ , 2023. 

- Open X-Embodiment Collaboration. Open X-Embodiment: Robotic learning datasets and RT-X models. In _International Conference on Robotics and Automation (ICRA)_ , 2024. 

- Patrick Esser, Sumith Kulal, Andreas Blattmann, Rahim Entezari, Jonas M¨uller, Harry Saini, Yam Levi, Dominik Lorenz, Axel Sauer, Frederic Boesel, Dustin Podell, Tim Dockhorn, Zion English, and Robin Rombach. Scaling rectified flow transformers for high-resolution image synthesis. In _Proceedings of the 41st International Conference on Machine Learning_ , volume 235 of _Proceedings of Machine Learning Research_ , pp. 12606–12633. PMLR, 2024. 

- Haoquan Fang, Jiafei Duan, Donovan Clay, Sam Wang, Shuo Liu, Weikai Huang, Xiang Fan, WeiChuan Tsai, Shirui Chen, Yi Ru Wang, Shanli Xing, Jaemin Cho, Jae Sung Park, Ainaz Eftekhar, Peter Sushko, Karen Farley, Angad Wadhwa, Cole Harrison, Winson Han, Ying-Chun Lee, Eli VanderBilt, Rose Hendrix, Suveen Ellawela, Lucas Ngoo, Joyce Chai, Zhongzheng Ren, Ali Farhadi, Dieter Fox, and Ranjay Krishna. MolmoAct2: Action reasoning models for real-world deployment. _arXiv preprint arXiv:2605.02881_ , 2026a. 

- Zhen Fang, Wenxuan Huang, Yu Zeng, Yiming Zhao, Shuang Chen, Kaituo Feng, Yunlong Lin, Lin Chen, Zehui Chen, Shaosheng Cao, et al. Flow-OPD: On-policy distillation for flow matching models. _arXiv preprint arXiv:2605.08063_ , 2026b. 

- Kevin Frans, Danijar Hafner, Sergey Levine, and Pieter Abbeel. One step diffusion via shortcut models. In _International Conference on Learning Representations_ , 2025. 

10 

Preprint. 

- Zhengyang Geng, Mingyang Deng, Xingjian Bai, J. Zico Kolter, and Kaiming He. Mean flows for one-step generative modeling. In _Advances in Neural Information Processing Systems_ , volume 38, 2025. 

- Zhengyang Geng, Yiyang Lu, Zongze Wu, Eli Shechtman, J Zico Kolter, and Kaiming He. Improved mean flows: On the challenges of fastforward generative models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 30467–30476, 2026. 

- Yanzhao Guo, Wenkai Chen, and Jianwei Zhang. ReactVLA: Fast and lightweight reactive robot manipulation via improved mean flow action generation. _arXiv preprint arXiv:2606.14255_ , 2026. 

- Geoffrey Hinton, Oriol Vinyals, and Jeff Dean. Distilling the knowledge in a neural network. _arXiv preprint arXiv:1503.02531_ , 2015. 

- Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffusion probabilistic models. In _Advances in Neural Information Processing Systems_ , volume 33, pp. 6840–6851, 2020. 

- Bofang Jia, Pengxiang Ding, Can Cui, Mingyang Sun, Pengfang Qian, Siteng Huang, Zhaoxin Fan, and Donglin Wang. Score and distribution matching policy: Advanced accelerated visuomotor policies via matched distillation. _arXiv preprint arXiv:2412.09265_ , 2024. 

- Dongjun Kim, Chieh-Hsin Lai, WeiHsiang Liao, Naoki Murata, Yuhta Takida, Toshimitsu Uesaka, Yutong He, Yuki Mitsufuji, and Stefano Ermon. Consistency trajectory models: Learning probability flow ODE trajectory of diffusion. In _International Conference on Learning Representations_ , 2024. 

- Moo Jin Kim, Yihuai Gao, Tsung-Yi Lin, Yen-Chen Lin, Yunhao Ge, Grace Lam, Percy Liang, Shuran Song, Ming-Yu Liu, Chelsea Finn, et al. Cosmos Policy: Fine-tuning video models for visuomotor control and planning. _arXiv preprint arXiv:2601.16163_ , 2026. 

- Quanhao Li, Junqiu Yu, Kaixun Jiang, Yujie Wei, Zhen Xing, Pandeng Li, Ruihang Chu, Shiwei Zhang, Yu Liu, and Zuxuan Wu. DiffusionOPD: A unified perspective of on-policy distillation in diffusion models. In _SIGGRAPH Asia 2026 Conference Papers_ , 2026a. 

- Shaolong Li, Lichao Sun, and Yongchao Chen. One-step flow policy: Self-distillation for fast visuomotor policies. _arXiv preprint arXiv:2603.12480_ , 2026b. 

- Yaron Lipman, Ricky T. Q. Chen, Heli Ben-Hamu, Maximilian Nickel, and Matthew Le. Flow matching for generative modeling. In _The Eleventh International Conference on Learning Representations_ , 2023. URL https://openreview.net/forum?id=PqvMRDCJT9t. 

- Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. LIBERO: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791, 2023. 

- Jie Liu, Gongye Liu, Jiajun Liang, Yangguang Li, Jiaheng Liu, Xintao Wang, Pengfei Wan, Di Zhang, and Wanli Ouyang. Flow-GRPO: Training flow matching models via online RL. In _Advances in Neural Information Processing Systems_ , volume 38, 2025. 

- Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. RDT-1B: a diffusion foundation model for bimanual manipulation. _arXiv preprint arXiv:2410.07864_ , 2024. 

- Wuyang Luan, Junhui Li, Weiguang Zhao, Wenjian Zhang, Tieru Wu, and Rui Ma. SnapFlow: Onestep action generation for flow-matching VLAs via progressive self-distillation. _arXiv preprint arXiv:2604.05656_ , 2026. 

- Amir M Mansourian, Rozhan Ahmadi, Masoud Ghafouri, Amir Mohammad Babaei, Elaheh Badali Golezani, Zeynab Yasamani Ghamchi, Vida Ramezanian, Alireza Taherian, Kimia Dinashi, Amirali Miri, et al. A comprehensive survey on knowledge distillation. _arXiv preprint arXiv:2503.12067_ , 2025. 

11 

Preprint. 

- Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Charles Xu, Jianlan Luo, Tobias Kreiman, You Liang Tan, Lawrence Yunliang Chen, Pannag Sanketi, Quan Vuong, Ted Xiao, Dorsa Sadigh, Chelsea Finn, and Sergey Levine. Octo: An open-source generalist robot policy. In _Proceedings of Robotics: Science and Systems_ , Delft, Netherlands, 2024. 

- Aaditya Prasad, Kevin Lin, Jimmy Wu, Linqi Zhou, and Jeannette Bohg. Consistency policy: Accelerated visuomotor policies via consistency distillation. In _Robotics: Science and Systems_ , 2024. 

- Moritz Reuss, Hongyi Zhou, Marcel R¨uhle, Omer<sup>¨</sup> Erdinc¸ Ya˘gmurlu, Fabian Otto, and Rudolf Lioutikov. FLOWER: Democratizing generalist robot policies with efficient vision-language-flow models. In _Conference on Robot Learning_ , 2025. 

- Amirmojtaba Sabour, Sanja Fidler, and Karsten Kreis. Align your flow: Scaling continuous-time flow map distillation. In _Advances in Neural Information Processing Systems_ , volume 38, 2025. 

- Juyi Sheng, Ziyi Wang, Peiming Li, and Mengyuan Liu. MP1: MeanFlow tames policy learning in 1-step for robotic manipulation. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 40, pp. 18532–18539, 2026. 

- Mustafa Shukor, Dana Aubakirova, Francesco Capuano, Pepijn Kooijmans, Steven Palma, Adil Zouitine, Michel Aractingi, Caroline Pascal, Martino Russi, Andres Marafioti, Simon Alibert, Matthieu Cord, Thomas Wolf, and Remi Cadene. SmolVLA: A vision-language-action model for affordable and efficient robotics. _arXiv preprint arXiv:2506.01844_ , 2025. 

- Yang Song, Jascha Sohl-Dickstein, Diederik P Kingma, Abhishek Kumar, Stefano Ermon, and Ben Poole. Score-based generative modeling through stochastic differential equations. In _International Conference on Learning Representations_ , 2021. URL https://openreview.net/ forum?id=PxTIG12RRHS. 

- Yang Song, Prafulla Dhariwal, Mark Chen, and Ilya Sutskever. Consistency models. In _International Conference on Machine Learning_ , pp. 32211–32252, 2023. 

- Zhendong Wang, Zhaoshuo Li, Ajay Mandlekar, Zhenjia Xu, Jiaojiao Fan, Yashraj Narang, Linxi Fan, Yuke Zhu, Yogesh Balaji, Mingyuan Zhou, Ming-Yu Liu, and Yu Zeng. One-step diffusion policy: Fast visuomotor policies via diffusion distillation. In _International Conference on Machine Learning_ , 2025. 

- Junjie Wen, Yichen Zhu, Jinming Li, Minjie Zhu, Kun Wu, Zhiyuan Xu, Ran Cheng, Chaomin Shen, Yaxin Peng, Feifei Feng, et al. TinyVLA: Towards fast, data-efficient vision-languageaction models for robotic manipulation. _IEEE Robotics and Automation Letters_ , 2025. 

- Wei Wu, Fan Lu, Yunnan Wang, Shuai Yang, Shi Liu, Fangjing Wang, Shuailei Ma, He Sun, Yong Wang, Zhenqi Qiu, Houlong Xiong, Ziyu Wang, Shuai Zhou, Yiyu Ren, Kejia Zhang, Hui Yu, Jingmei Zhao, Qian Zhu, Ran Cheng, Yong-Lu Li, Yongtao Huang, Xing Zhu, Yujun Shen, and Kecheng Zheng. A pragmatic vla foundation model. _arXiv preprint arXiv:2601.18692v1_ , 2026. 

- Ge Yan, Jiyue Zhu, Yuquan Deng, Shiqi Yang, Ri-Zhao Qiu, Xuxin Cheng, Marius Memmel, Ranjay Krishna, Ankit Goyal, Xiaolong Wang, and Dieter Fox. ManiFlow: A general robot manipulation policy via consistency flow training. In _Conference on Robot Learning (CoRL)_ , 2025. 

- Seonghyeon Ye, Yunhao Ge, Kaiyuan Zheng, Shenyuan Gao, Sihyun Yu, George Kurian, Suneel Indupuru, You Liang Tan, Chuning Zhu, Jiannan Xiang, et al. World action models are zero-shot policies. _arXiv preprint arXiv:2602.15922_ , 2026. 

- Tianwei Yin, Micha¨el Gharbi, Taesung Park, Richard Zhang, Eli Shechtman, Fredo Durand, and William T Freeman. Improved distribution matching distillation for fast image synthesis. _Advances in neural information processing systems_ , 37:47455–47487, 2024a. 

- Tianwei Yin, Micha¨el Gharbi, Richard Zhang, Eli Shechtman, Fredo Durand, William T Freeman, and Taesung Park. One-step diffusion with distribution matching distillation. In _2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pp. 6613–6623. IEEE, 2024b. 

12 

Preprint. 

- Tianyuan Yuan, Zibin Dong, Yicheng Liu, and Hang Zhao. Fast-WAM: Do world action models need test-time future imagination? _arXiv preprint arXiv:2603.16666_ , 2026. 

- Zhide Zhong, Haodong Yan, Junfeng Li, Junjie He, Tianran Zhang, and Haoang Li. VLA-OPD: Bridging offline SFT and online RL for vision-language-action models via on-policy distillation. _arXiv preprint arXiv:2603.26666_ , 2026. 

## A PROOFS 

**Proposition 1** (On-policy Flow Map Distillation) **.** _Let σt >_ 0 _be a diffusion coefficient. For any t ∈_ (0 _,_ 1) _and step_ ∆ _t <_ 0 _, the Euler–Maruyama kernels induced by_ **_u_** _θ_ ( _·, t, t_ ) _and_ **_v_** _ϕ_ ( _·, t_ ) _satisfy_ 


_Proof._ For the linear interpolant 


the score and the corresponding instantaneous velocity field satisfy 

Following the flow-to-SDE conversion of Liu et al. (2025), for any diffusion coefficient _σt >_ 0, the reverse-time SDE that shares the same marginal _pt_ of PF-ODE is defined as 


Substituting Eq. (13) into Eq. (14) gives 

A single Euler–Maruyama step of size ∆ _t_ from **_x_** ˜ _t_ therefore defines the Gaussian transition kernel _p_ **_v_** ( **_x_** _t_ +∆ _t |_ **_x_** ˜ _t_ ) = _N_ � _µ_ **_v_** _, σt_<sup>2</sup><sup>_|_∆</sup><sup>_t|_</sup><sup>**I**</sup><sup>_d_</sup> � _,_ (16) 

where 


For the flow-map parameterization **_f_** _θ_ ( **_x_** _, s, t_ ) = **_x_** + ( _t − s_ ) **_u_** _θ_ ( **_x_** _, s, t_ ), its tangent velocity is 

_∂τ_ **_f_** _θ_ ( **_x_** _, t, τ_ ) _|τ_ = _t_ = **_u_** _θ_ ( **_x_** _, t, t_ ) _._ (18) 

We consequently define the student and teacher velocities at **_x_** ˜ _t_ by 


Applying Eq. (16) to these two velocities gives 


Their covariances are identical, and the common **_x_** ˜ _t_ -dependent term cancels from the difference of their means. Hence, 


13 

Preprint. 

Using the KL divergence between Gaussians with common covariance, we obtain 


where 


**Proposition 2.** _Let qθ and ρθ be the sampling distributions of LSC and LOPFD. Assume that_ **_v_** _ϕ_ ( _·, t_ ) _is L-Lipschitz and that_ ( _s,_ **_x_** _s_ ) _and_ ( _m,_ ˆ **_x_** _m_ ) _under qθ have density ratio at most κ with respect to ρθ. Then,_ 


_Proof._ Let ( _s, t,_ **_x_** ) _∼ qθ_ with **_x_** = **_x_** _s_ = (1 _− s_ ) **_x_** 0 + _s_ **_x_** 1 and _m_ = ( _s_ + _t_ ) _/_ 2. Since _s > t_ , we have _|m − s|_ = ( _s − t_ ) _/_ 2 _≤_ 1 _/_ 2. 

We define the self-consistency target of the student as 


where **_x_** ˆ _m_ = **_x_** + ( _m − − s_ ) **_v_** _θ_ ( **_x_** _, s_ ), and denote the velocity errors at, and denote the velocity errors at _s_ and _m_ by 

Using the definition of **_u_** _ϕ_ , we decompose the difference between the student map and the ideal shortcut as 


where the first term is the self-consistency error, the second and third terms are the velocity errors at _s_ and _m_ , respectively, and the last term is the propagated state error induced by the mismatch between the student midpoint **_x_** ˆ _m_ and the ideal midpoint **_x_** ¯ _m_ . 

By the _L_ -Lipschitzness of the teacher, 


Therefore, 


where the last inequality uses _|m − s| ≤_ 1 _/_ 2. 

By taking the expectation of Eq. (28) over _qθ_ , the left-hand side becomes _Dqθ_ ( **_u_** _θ,_ **_u_** _ϕ_ ) and the first term on the right-hand side becomes 4 _L_ SC. The remaining two terms are velocity errors evaluated at ( _s,_ **_x_** _s_ ) and ( _m,_ ˆ **_x_** _m_ ), whereas _L_ OPFD averages the same error over ( _t,_ ˜ **_x_** _t_ ) _∼ ρθ_ . 

Let _g_ ( _t,_ **_x_** ) := _∥_ **_v_** _θ_ ( **_x_** _, t_ ) _−_ **_v_** _ϕ_ ( **_x_** _, t_ ) _∥_<sup>2</sup> 2<sup>_≥_0, so that</sup><sup>_L_OPFD= E</sup><sup>_ρ_</sup> _θ_<sup>[</sup><sup>_g_].</sup> 

14 

Preprint. 

Then, for any distribution _ν_ whose density ratio with respect to _ρθ_ is at most _κ_ , 


Applying this with _ν_ the distributions of ( _s,_ **_x_** _s_ ) and ( _m,_ ˆ **_x_** _m_ ), which satisfy this condition by the density-ratio assumption, gives E _qθ_ [ _e_<sup>2</sup> _s_<sup>]</sup><sup>_≤κL_OPFDand E</sup><sup>_q_</sup> _θ_<sup>[</sup><sup>_e_</sup> _m_<sup>2]</sup><sup>_≤κL_OPFD.</sup> Therefore, 


Here, _Cλ_ grows as _λ →_ 0, reflecting that the self-consistency term alone cannot anchor the student to the teacher. 

**Theorem 1.** _Let pθ and pϕ denote the terminal distributions induced by sampling with_ **_f_** _θ and_ **_f_** _ϕ, respectively, from the same initial noise on a fixed sampling schedule_ 1 = _t_ 0 _> t_ 1 _> · · · > tK_ = 0 _, and let_ **_x_**<sup>_θ_</sup> _tk_<sup>_denote the intermediate states of the student.Suppose that the assumptions of_</sup> _Proposition 2 hold and there exists finite κ_ roll _>_ 0 _such that, for every k,_ 


_Then,_ 


_where C >_ 0 _depends only on L, κ, κ_ roll _, λ, and the sampling schedule._ 

_Proof._ Let the student and the teacher-induced shortcut model start from the same initial noise sample, **_x_**<sup>_θ_</sup> _t_ 0<sup>=</sup><sup>**_x_**¯</sup><sup>_t_</sup> 0<sup>_∼N_(</sup><sup>**0**</sup><sup>_,_</sup><sup>**I**), and follow the same sampling schedule</sup> 


with step sizes _hk_ := _tk − tk_ +1 _>_ 0. 

Their rollout states are defined by 


respectively. 

By the definition of **_u_** _ϕ_ and _mk_ = ( _tk_ + _tk_ +1) _/_ 2, 


Thus, **_f_** _ϕ_ ( _·, tk, tk_ +1) is the composition of two Euler steps of size _hk/_ 2. Since **_v_** _ϕ_ ( _·, t_ ) is _L_ - Lipschitz, each Euler step is (1 + _hkL/_ 2)-Lipschitz, and hence **_f_** _ϕ_ ( _·, tk, tk_ +1) is _LF,k_ -Lipschitz with 


Then, 


15 

Preprint. 


Since the two trajectories start from the same noise sample, _E_ 0 = 0. Unrolling Eq. (36) gives 


By the assumption of _κ_ roll and Proposition 2, 


The pair ( **_x_**<sup>_θ_</sup> _tK_<sup>_,_¯</sup><sup>**_x_**</sup><sup>_t_</sup> _K_<sup>) constructed from the same initial noise is a valid coupling of</sup><sup>_pθ_and</sup><sup>_pϕ_.There-</sup> fore, 


Taking square roots on both sides yields 


hence _L_ FastOPD _→_ 0 implies _W_ 2( _pθ, pϕ_ ) _→_ 0. 

## B EXPERIMENTAL DETAILS 

### B.1 IMPLEMENTATION DETAILS. 

All experiments are implemented within the LeRobot framework (Cadene et al., 2024). We report the public checkpoints used for teacher and student initialization in Tab. 7. For two-time projection, the source and target timesteps are embedded using fixed sinusoidal positional encodings, and the remaining weights of the time projection layer _ψ_ ( _·_ ) are randomly initialized. 

Table 7: Model checkpoints used in the experiments. 

|**Benchmark**|**Model**|**Checkpoint**|
|---|---|---|
|LIBERO|_π_0_._5<br>SmolVLA<br>SmolVLA (OPD Init)|lerobot/pi05_libero_finetuned_v044<br>HuggingFaceVLA/smolvla_libero<br>lerobot/smolvla_base|
||LingBot-VLA|robbyant/lingbot-vla-4b-posttrain-robotwin|
|RoboTwin 2.0|Fast-WAM<br>SmolVLA|lerobot/fastwam_robotwin_uncond_3cam_384<br>lerobot/smolvla_robotwin|
|Real-world|MolmoAct2<br>SmolVLA|allenai/MolmoAct2-BimanualYAM<br>lerobot/smolvla_base|


B.2 CONFIGURATION DETAILS. 

In Tab. 8, we report training and evaluation configurations for full reproducibility. 

16 

Preprint. 

Table 8: Training and evaluation configurations for FastOPD. 

||**LIBERO**|**Robo**|**Twin 2.0**|**Real-world**|
|---|---|---|---|---|
|_Model_|||||
|Teacher (Params)<br>Student (Params)|_π_0_._5 (3.3B)<br>SmolVLA +_ψ_(451M)|LingBot-VLA (4.2B)<br>SmolVLA +_ψ_(451M)|Fast-WAM (6B)<br>SmolVLA +_ψ_(451M)|MolmoAct2 (5B)<br>SmolVLA +_ψ_(451M)|
|_Optimization_|||||
|Optimizer|AdamW|AdamW|AdamW|AdamW|
|Adam(_β_1_, β_2)<br>Adam_ϵ_|(0_._9_,_0_._95)<br>10<sup>_−_8</sup>|(0_._9_,_0_._95)<br>10<sup>_−_8</sup>|(0_._9_,_0_._95)<br>10<sup>_−_8</sup>|(0_._9_,_0_._95)<br>10<sup>_−_8</sup>|
|Adam weight decay|10<sup>_−_10</sup>|10<sup>_−_10</sup>|10<sup>_−_10</sup>|10<sup>_−_10</sup>|
|Gradient clipping|10.0|10.0|10.0|10.0|
|Scheduler|Cosine<br>|Cosine<br>|Cosine<br>|Cosine<br>|
|Learning rate|1_×_10<sup>_−_4</sup>|1_×_10<sup>_−_4</sup>|1_×_10<sup>_−_4</sup>|2_×_10<sup>_−_5</sup>|
|_FastOPD training_|||||
|Training iterations|10K|50K|50K|20K|
|Batch size|64|128|128|64|
|_λ_|0.1|0.1|0.1|1.0|
|Time sampling distribution_p_|Beta(1.5,1)|Beta(1.5,1)|Shifted uniform (_s_ = 5)<sup>2</sup>|Beta(1.5,1)|
|_Evaluation_|||||
|Time discretization|Uniform|Uniform|Uniform|Uniform|
|Action execution steps_K_|10|50|24|30|


### B.3 COMPUTATIONAL RESOURCES 

For full reproducibility, we report the computational resources used in our experiments in Tab. 9. Latency is measured on a single RTX 3090 (App. B), and real-world policies are deployed on a single RTX 4090 (App. B.5). 

Table 9: Hardware used for training. 

|**Experiment**|**Hardware**|
|---|---|
|LIBERO (main)|1_×_NVIDIA RTX 4090 (24 GB)|
|LIBERO (ablations)|1_×_NVIDIA RTX 4090 or RTX 3090 (24 GB each)|
|RoboTwin 2.0 (LingBot-VLA)|2_×_NVIDIA RTX 4090 (24 GB each)|
|RoboTwin 2.0 (Fast-WAM)|1_×_NVIDIA H200 (141 GB)|
|Real-world|1_×_NVIDIA B200 (180 GB)|


### B.4 SIMULATION EXPERIMENTAL DETAILS. 

Evaluation uses 50 episodes per task (2,000 episodes on LIBERO; 2,500 per setting on RoboTwin 2.0), and all results are from a single training run (seed 100000). Following the latency details of Luan et al. (2026), we measure end-to-end inference latency on a single NVIDIA RTX 3090 (CUDA 12.8, PyTorch 2.11) in bfloat16 with batch size 1, excluding pre- and post-processing, and report the median of 100 runs after 10 warm-up runs.<sup>3</sup> 

### B.5 REAL-WORLD EXPERIMENTAL DETAILS 

**Robot setup.** We follow the real-robot setup of MolmoAct2 (Fang et al., 2026a). Specifically, we use the right arm of a bimanual YAM robot with six joints and a parallel-jaw gripper, controlled by absolute joint-position commands (7-dimensional action space), with the joint velocity capped 

> 2We sample _u ∼U_ (0 _,_ 1) and apply the flow-shift transformation _t_ = 1+( _ssu−_ 1) _u_<sup>with</sup><sup>_s_=5,following</sup> Fast-WAM (Yuan et al., 2026) implementation. 

3Fast-WAM does not fit in 24 GB memory with its text encoder, so we time the encoder separately and add it. 

17 

Preprint. 


Figure 8: **Robot setting.** (a) Teleoperation setup for data collection, with lead arms, the follower YAM arm, and top-view and wrist cameras. (b) Close-up view of the evaluation setup. (c) Objectposition initialization: the current top-camera frame is compared against a reference frame, and their pixel-wise difference is used to place objects at the same initial positions across trials. 

at 0.75 rad/s (Fig. 8). The policy observes two RGB views (top and right wrist; 480 _×_ 640, 30 fps; current frame only) together with the 7-dimensional proprioceptive state (six joints and gripper), and receives the language instruction. Actions and states are normalized with quantile normalization for all models (the gripper is not normalized for MolmoAct2). All policies are run on a single NVIDIA RTX 4090, with SmolVLA-based models in float32. 

**Dataset.** We collect teleoperated demonstrations of multiple tasks on the YAM arm and train all policies on the same dataset (Tab. 10). The evaluation is performed on pnp-plate. The teacher MolmoAct2 is fine-tuned on this dataset for 14,000 iterations. The student is initialized from SmolVLA, warmed up with flow-matching-based behavior cloning for 10,000 iterations, and then trained with FastOPD for 20,000 iterations. At inference, the type of target objects including a ball and a plate are fixed and the language instruction is fixed as “Pick up the ball and place it on the plate”. 

**Policy execution.** Tab. 11 summarizes the execution settings. All policies predict 30-step action chunks (1.0 s) and send commands at 30 Hz. The SmolVLA (warm-up) and our policy share the same synchronous execution scheme. MolmoAct2 is run with its default asynchronous execution, replanning every 0.5 s, skipping the actions already covered by the inference delay, and linearly blending consecutive chunks over 2–10 steps. No real-time chunking or gripper post-processing is applied to any model. 

**Evaluation details.** Each policy is evaluated over 50 episodes with a time limit of 30 s. An episode is counted as successful once the ball has been placed entirely within the plate and the gripper has opened. We report the success rate and the task completion time, the latter averaged over successful episodes only, following the Wang et al. (2025) evaluation protocol. To ensure a fair comparison, 

18 

Preprint. 

Table 10: Real-world dataset statistics. Average episode length is computed at 30 fps. 

|**Task**|**Language instruction**|**Episodes**|**Frames**|**Avg. Length (s)**|
|---|---|---|---|---|
|pnp-plate|“Pick up the ball and place it on the plate.”|106|47,002|14.8|
|pnp-box|“Pick up the basketball and place it in the box.”|108|47,616|14.7|
|-l|“Open the box, put the ball inside, and close it.”|53|44,780|28.2|
|opencose|“Open the box, put the basketball inside, and<br>close it.”|55|46,834|28.4|
|open-place|“Open the box, take the ball out, and place it in<br>the pot.”|52|41,637|26.7|
||“Open the box, take the ball out, and place it on<br>the tray.”|50|40,676|27.1|
|Overall||424|268,545|21.1|


Table 11: Real-world policy execution settings. All policies predict 30-step action chunks (1.0 s) and send commands at 30 Hz. For SmolVLA, values are reported for 4 and 10 denoising steps. Inference latency is measured on the robot side, including HTTP communication. 

||**MolmoAct2**|**SmolVLA (warm-up)**|**Ours**|
|---|---|---|---|
|Execution|async (re-plan every 0.5 s)|sync|sync|
|Sampler|Euler, 10 steps|Euler, 4 / 10 steps|flow map, 4 steps|
|Actions executed per chunk|_∼_15|30|30|
|Chunk blending|linear (2–10 steps)|none|none|
|Inference latency|300–450 ms|118 / 178 ms|120 ms|
|Re-planning rate|1.8–1.9 Hz|0.89 / 0.86 Hz|0.87 Hz|


the initial scene of every episode is matched to the corresponding episode of a reference evaluation session by aligning the current top-camera frame with the reference image (Fig. 8(c)), so that all policies start from identical object configurations. 

## C ADDITIONAL EXPERIMENTS 

**Connection with previous works.** Although SnapFlow (Luan et al., 2026) adopts a two-step consistency target similar to ours, the two objectives differ in both their anchor and their scope. SnapFlow is a self-distillation method that combines flow matching on ground-truth actions with a shortcut loss defined only on the fixed interval from _t_ = 1 to _t_ = 0: 


where **_v_** tgt =<sup><u>1</u></sup> 2 �sg[ **_v_** _θ_ ( **_x_** 1 _,_ 1 _| c_ )] + sg[ **_v_** _θ_ (ˆ **_x_** 0 _._ 5 _,_ 0 _._ 5 _| c_ )]� and **_x_** ˆ0 _._ 5 = **_x_** 1 _−_ 0 _._ 5 sg[ **_v_** _θ_ ( **_x_** 1 _,_ 1 _| c_ )]. In contrast, FastOPD enforces self-consistency over arbitrary intervals ( _s, t_ ), yielding a flow map that supports any number of sampling steps, and anchors the target to the teacher through OPFD rather than to the data through flow matching. SnapFlow can thus be viewed as a teacher-free counterpart of our objective restricted to a single interval, which allows us to isolate the contribution of teacher supervision. 

**Student initialization.** In Sec. 4.3, we studied on-policy distillation (OPD) as an alternative initialization strategy for the flow map. Specifically, we first train the SmolVLA base model with OPD for 5,000 iterations (Stage 1), and then fine-tune it into a flow map with the FastOPD objective for 10,000 iterations (Stage 2). Tab. 12 reports the per-suite results, and Fig. 10 shows the success rate over training iterations. As in Fig. 4, FastOPD consistently improves performance over the course of training under this OPD-based initialization as well. 

## D FEW-STEP DISTILLATION ALGORITHMS 

In this section, we provide detailed descriptions of the few-step distillation algorithms leveraged in our experiments as baselines. 

19 

Preprint. 


Figure 9: Real-world manipulation task setups on the YAM robot arm. Left two columns show the initial scene and the right show the robot during execution. 

### D.1 DISTRIBUTION MATCHING DISTILLATION 

Referring to OneDP (Wang et al., 2025), we design DMD as a one-step generator, and jointly train it with a fake-score critic **_v_** _ψ_ ( **_x_** _, t_ ) of the same architecture, initialized from the same checkpoint as **_v_** _θ_ . Here, generator and critic are updated alternately at every step. 

**Generator.** A sample is produced with a single Euler step of the student’s own PF-ODE from pure noise **_x_** 1 _∼N_ ( **0** _,_ **I** ), 


From the re-noised sample **_x_** _t_ from **_x_** ˆ0, the teacher and critic denoised estimates are formed as 


20 

Preprint. 

Table 12: Per-suite results of OPD-based initialization. Success rates (%) on LIBERO. 

|**Method**<br>**N**|**FE**|**Spatial**|**Object**|**Goal**|**Long**|**Avg.**|
|---|---|---|---|---|---|---|
|OPD init.|1|78.0|94.2|78.2|40.2|72.7|
||2|84.4|95.4|87.8|45.0|78.2|
||4|58.0|59.8|53.8|5.0|44.2|
||10|82.6|94.6|89.0|48.2|78.6|
|+ FastOPD|1|84.2|92.8|90.8|54.0|80.5|
||2|84.6|95.2|94.2|57.8|**83.0**|
||4|83.6|97.2|91.4|56.4|82.2|
||10|80.4|92.8|93.4|60.2|81.7|
|Success Rate (%)|||||||
||||Init<br>1-step<br>2-steps|<br>4-s<br>10-s|teps<br>teps||
|||Tr|aining Step||||


Figure 10: Success rate (%) on LIBERO over training iterations with OPD-based initialization. 

The distribution-matching direction is then defined as **g** 0 = **_x_** ˆ<sup>fake</sup> 0 _−_ **_x_** ˆ<sup>real</sup> 0 . Here, we normalize it per sample by the mean absolute magnitude of the teacher’s own correction, 


where mean( _·_ ) averages over the action-chunk and action-dimension axes, for training stability. The generator is trained with the surrogate loss whose gradient with respect to **_x_** ˆ0 equals **g** : 


**Critic.** The fake-score network **_v_** _ψ_ is trained with ordinary denoising score matching on the generator’s output: 


where **_x_** _t′_ = (1 _− t_<sup>_′_</sup> ) sg[ˆ **_x_** 0] + _t_<sup>_′_</sup> **_ϵ_** . 

### D.2 CONSISTENCY TRAJECTORY MODEL 

We follow the Consistency Trajectory Model (CTM) formulation of (Kim et al., 2024), which generalizes the original Consistency Distillation (Song et al., 2023) by allowing anytime-to-anytime jump with a denoising score-matching (DSM) regularizer. We train the two-time flow map **_f_** _θ_ ( **_x_** _, s, t_ ) = **_x_** + ( _t − s_ ) **_u_** _θ_ ( **_x_** _, s, t_ ) together with an EMA target network _θ_<sup>_−_</sup> , updated as _θ_<sup>_−_</sup> _← µθ_<sup>_−_</sup> + (1 _− µ_ ) _θ_ . 

For sampled timesteps 1 _≥ s ≥ r ≥_ 0 and an intermediate solver time _u ∼_ Unif[ _r, s_ ], with **_x_** 1 _∼N_ ( **0** _,_ **I** ), **_x_** 0 _∼ p_ 0, and **_x_** _s_ = (1 _− s_ ) **_x_** 0 + _s_ **_x_** 1, the student first jumps from _s_ to _r_ , 


while the target integrates the teacher’s PF-ODE from _s_ to _u_ with a 1-step Heun solver, **_x_** _u_ = ODE _ϕ_ ( **_x_** _s_ ; _s, u_ ), and then estimates from time _u_ to _r_ with the EMA network, 


21 

Preprint. 

**Algorithm 2** Training Algorithm for DMD **Require:** Dataset _D_ ; teacher **_v_** _ϕ_ ; generator **_v_** _θ_ ; critic **_v_** _ψ_ 1: **for** each training iteration **do** 2: ( **_x_** 0 _, c_ ) _∼D_ , **_x_** 1 _∼N_ ( **0** _,_ **I** ) 3: **_x_** ˆ0 _←_ **_x_** 1 _−_ **_v_** _θ_ ( **_x_** 1 _,_ 1 _| c_ ) _▷ one-step generation_ 4: _t ∼ p_ ( _t_ ), **_x_**<sup>_′_</sup> 1<sup>_∼N_(</sup><sup>**0**</sup><sup>_,_</sup><sup>**I**);</sup> **_x_** _t ←_ (1 _− t_ ) sg[ˆ **_x_** 0] + _t_ **_x_** 1<sup>_′_</sup> 5: **_x_** ˆ<sup>real</sup> 0 _←_ **_x_** _t − t_ **_v_** _ϕ_ ( **_x_** _t, t | c_ ), **_x_** ˆ<sup>fake</sup> 0 _←_ **_x_** _t − t_ **_v_** _ψ_ ( **_x_** _t, t | c_ ) 6: **g** _←_ � **_x_** ˆ0fake _−_ **_x_** ˆ<sup>real</sup> 0 ���mean( _|_ **_x_** ˆ<sup>real</sup> 0 _−_ sg[ˆ **_x_** 0] _|_ ) + _ϵ_ � 7: _L_ gen _←_ 2<sup><u>1</u></sup><sup>_∥_</sup><sup>**_x_**ˆ0</sup><sup>_−_sg[ˆ</sup><sup>**_x_**0</sup><sup>_−_</sup><sup>**g**]</sup><sup>_∥_</sup> 2<sup>2</sup> 8: _θ ← θ − η∇θL_ gen _▷ update generator_ 9: _t_<sup>_′_</sup> _∼ p_ ( _t_ ), **_ϵ_** _∼N_ ( **0** _,_ **I** ) **_x_** _t′ ←_ (1 _− t_<sup>_′_</sup> ) sg[ˆ **_x_** 0] + _t_<sup>_′_</sup> **_ϵ_** 10: _L_ crit _←∥_ **_v_** _ψ_ ( **_x_** _t′, t_<sup>_′_</sup> _| c_ ) _−_ ( **_ϵ_** _−_ sg[ˆ **_x_** 0]) _∥_ 2<sup>2</sup> 11: _ψ ← ψ − ηψ∇ψL_ crit _▷ update critic_ 12: **end for** 


so the total loss is _L_ ( _θ_ ) = _L_ CTM( _θ_ ) + _w_ dsm _L_ DSM( _θ_ ). 

**Algorithm 3** Training Algorithm for CTM 

**Require:** Dataset _D_ ; teacher **_v_** _ϕ_ ; student flow map **_u_** _θ_ ; EMA target _θ_<sup>_−_</sup> ; decay _µ_ ; DSM weight _w_ dsm 1: **for** each training iteration **do** 2: ( **_x_** 0 _, c_ ) _∼D_ , **_x_** 1 _∼N_ ( **0** _,_ **I** ), sample 1 _≥ s ≥ r ≥_ 0, _u ∼_ Unif[ _r, s_ ] 3: **_x_** _s ←_ (1 _− s_ ) **_x_** 0 + _s_ **_x_** 1 4: **_x_** ˆ<sup>_θ_</sup> _r_<sup>_←_</sup><sup>**_f_**</sup><sup>_θ_(</sup><sup>**_x_**</sup><sup>_s, s, r| c_)</sup> 5: **_x_** _u ←_ ODE _ϕ_ ( **_x_** _s_ ; _s, u | c_ ) 6: **_x_**<sup>_−_</sup> _r_<sup>_←_</sup><sup>**_f_**</sup> _θ_<sup>_−_(</sup><sup>**_x_**</sup><sup>_u, u, r| c_)</sup> 7: **_x_** ˆ<sup>_θ_</sup> 0<sup>_←_</sup><sup>**_f_**</sup> sg[ _θ_ ]<sup>(ˆ</sup><sup>**_x_**</sup> _r_<sup>_θ, r,_0</sup><sup>_| c_);</sup><sup>**_x_**</sup><sup>_−_</sup> 0<sup>_←_</sup><sup>**_f_**sg[</sup><sup>_θ_](</sup><sup>**_x_**</sup> _r_<sup>_−, r,_0</sup><sup>_| c_)</sup> 8: _L_ CTM _←∥_ **_x_** ˆ<sup>_θ_</sup> 0<sup>_−_sg[</sup><sup>**_x_**</sup><sup>_−_</sup> 0<sup>]</sup><sup>_∥_</sup> 2<sup>2</sup> 9: _L_ DSM _←∥_ **_u_** _θ_ ( **_x_** _s, s, s | c_ ) _−_ sg[ **_v_** _ϕ_ ( **_x_** _s, s | c_ )] _∥_ 2<sup>2</sup> 10: _θ ← θ − η∇θ_ � _L_ CTM + _w_ dsm _L_ DSM� 11: _θ_<sup>_−_</sup> _← µθ_<sup>_−_</sup> + (1 _− µ_ ) _θ_ 12: **end for** 

### D.3 IMPROVED MEANFLOW 

MeanFlow (Geng et al., 2025) parameterizes the average velocity **_u_** ( **_x_** _, s, t_ ) := _s−_ <u>1</u> _t_ � _ts_<sup>**_v_**(</sup><sup>**_x_**</sup><sup>_τ, τ_)</sup><sup>_dτ_</sup> and train it through the identity obtained by differentiating the definition along _s_ , 


In the original formulation, **_v_** ( **_x_** _s, s_ ) in Eq. (51) is taken to be the student’s own instantaneous velocity **_v_** _θ_ ( **_x_** _s, s_ ) := **_u_** _θ_ ( **_x_** _s, s, s_ ), so the regression target is itself computed by the network being optimized. Improved MeanFlow (iMF) (Geng et al., 2026) addresses this issue by reformulating the identity to remove this self-reference. 

> 4The regularizer can instead target the ground-truth flow velocity **_x_** 1 _−_ **_x_** 0 (dataset-supervised DSM, as in (Kim et al., 2024)); we use the teacher-supervised variant. 

22 

Preprint. 

We follow this reformulation and further adapt it to distillation by replacing the self-referential term with the frozen teacher velocity, **_v_** _ϕ_ ( **_x_** _s, s_ ), used both as the target and the tangent direction of the total derivative. 

Given **_x_** 1 _∼N_ ( **0** _,_ **I** ), **_x_** 0 _∼ p_ 0, and interpolant **_x_** _s_ , the total derivative is computed by a Jacobian– Vector Product (JVP) of **_u_** _θ_ at ( **_x_** _s, s, t_ ) along the tangent ( **_v_** _ϕ,_ 1 _,_ 0): 


The model then predicts one-step velocity as follow: 


Note that MF loss reduces to standard flow matching when _t_ = _s_ . The loss regresses **_v_** ˆ _θ_ onto the teacher target with an elementwise Pseudo-Huber loss, 


applied element-wise and averaged over the action dimensions. 

**Algorithm 4** Training Algorithm for iMF 

**Require:** Dataset _D_ ; teacher **_v_** _ϕ_ ; student flow map **_u_** _θ_ ; FM prob. _pt_ = _s_ ; Huber scale _δ_ 1: **for** each training iteration **do** 

2: ( **_x_** 0 _, c_ ) _∼D_ , **_x_** 1 _∼N_ ( **0** _,_ **I** ), sample 1 _≥ s ≥ t ≥_ 0 3: With prob. _pt_ = _s_ : _t ← s_ 4: **_x_** _s ←_ (1 _− s_ ) **_x_** 0 + _s_ **_x_** 1 5: **_u_** _θ_ ( **_x_** _s, s, t | c_ ) _,_ **_u_** ˙ _θ ←_ sg �JVP� **_u_** _θ_ ( _·, ·, t | c_ ); ( **_x_** _s, s_ ) _,_ ( **_v_** _ϕ,_ 1)�� 6: **_v_** ˆ _θ ←_ **_u_** _θ_ ( **_x_** _s, s, t | c_ ) + ( _s − t_ ) **_u_** ˙ _θ_ 7: _L_ iMF _← ρδ_ (ˆ **_v_** _θ −_ **_v_** _ϕ_ ) 8: _θ ← θ − η∇θL_ iMF 9: **end for** 

23 

Preprint. 

## E DETAILED RESULTS IN SIMULATION ENVIRONMENTS 

Table 13: Per-task success rates (%) on RoboTwin 2.0 at 10 denoising steps, under clean and randomized settings. Ours (X) denotes our method trained with X as the teacher. 

||**LingB**|**ot-VLA**|**Fast**|**-WAM**|**Sm**|**olVLA**|**Ours (L**|**ingBot-VLA)**|**Ours (F**|**ast-WAM)**|
|---|---|---|---|---|---|---|---|---|---|---|
|**Task**|**Clean**|**Random**|**Clean**|**Random**|**Clean**|**Random**|**Clean**|**Random**|**Clean**|**Random**|
|adjust<br>~~b~~ottle|98|90|100|100|100|98|100|98|100|98|
|beat<br>~~b~~lock<br>~~h~~ammer|78|78|100|96|66|66|56|40|76|78|
|blocks<br>~~r~~anking<br>~~r~~gb|96|92|100|100|50|46|50|58|30|30|
|blocks<br>~~r~~anking<br>~~s~~ize|74|66|88|96|20|22|28|26|20|10|
|click<br>~~a~~larmclock<br><br>|70<br>|42<br>|100<br>|100<br>|90<br>|94<br>|34<br>|50<br>|92<br>|96<br>|
|click<br>~~b~~ell|62|78|100|100|96|92|62|54|96|86|
|dump<br>~~b~~in<br>~~b~~igbin|92|98|100|96|96|70|92|84|90|82|
|grab<br>~~r~~oller|100|98|100|100|96|96|100|100|100|100|
|handover<br>~~b~~lock|88|82|96|90|28|22|18|32|28|28|
|handover<br>~~m~~ic|100|88|100|98|80|74|76|82|84|88|
|hanging<br>~~m~~ug|48|50|64|56|10|16|4|12|6|8|
|lift<br>~~p~~ot|100|100|100|100|84|72|62|68|80|80|
|move<br>~~c~~an<br>~~p~~ot|66|86|88|98|22|44|18|44|10|32|
|move<br>~~p~~illbottle<br>~~p~~ad|98|94|96|100|54|54|50|56|52|56|
|move<br>~~p~~layingcard<br>~~a~~way|100|100|98|98|78|84|88|88|68|80|
|move<br>~~s~~tapler<br>~~p~~ad|56|66|74|66|24|14|30|22|26|18|
|open<br>~~l~~aptop|96|94|94|100|88|86|78|78|72|88|
|open<br>~~m~~icrowave|58|38|48|46|18|36|20|54|22|30|
|pick<br>~~d~~iverse<br>~~b~~ottles|82|76|82|90|42|32|60|44|50|40|
|pick<br>~~d~~ual<br>~~b~~ottles|94|88|100|100|50|42|50|42|64|64|
|place<br>~~a~~2b<br>~~l~~eft|84|80|100|98|38|48|46|42|40|42|
|place<br>~~a~~2b<br>~~r~~ight|76|82|94|98|40|36|38|46|38|44|
|place<br>~~b~~read<br>~~b~~asket|84|90|94|90|68|68|66|56|60|60|
|place<br>~~b~~read<br>~~s~~killet|92|70|92|92|62|54|66|62|68|70|
|place<br>~~b~~urger<br>~~f~~ries<br><br>|94<br>|94<br>|94<br>|100<br>|96<br>|84<br>|96<br>|92<br>|98<br>|90<br>|
|place<br>~~c~~an<br>~~b~~asket|82|72|76|68|62|44|30|24|32|8|
|place<br>~~c~~ans<br>~~p~~lasticbox|100|100|100|100|82|84|58|52|88|82|
|place<br>~~c~~ontainer<br>~~p~~late|98|96|100|96|90|94|98|96|90|88|
|place<br>~~d~~ual<br>~~s~~hoes|80|84|94|88|50|62|58|76|42|50|
|place<br>~~e~~mpty<br>~~c~~up|100|98|100|100|96|98|98|98|86|84|
|place<br>~~f~~an|88|80|98|96|38|50|38|44|42|56|
|place<br>~~m~~ouse<br>~~p~~ad|86|90|82|84|26|42|34|42|30|36|
|place<br>~~o~~bject<br>~~b~~asket|92|84|88|82|68|62|82|80|70|48|
|place<br>~~o~~bject<br>~~s~~cale|82|82|100|94|46|38|50|58|36|52|
|place<br>~~o~~bject<br>~~s~~tand|92|96|98|98|60|82|62|82|70|86|
|place<br>~~p~~hone<br>~~s~~tand|80|96|92|96|48|74|46|76|60|70|
|place<br>~~s~~hoe|96|96|88|92|86|88|90|88|76|78|
|press<br>~~s~~tapler|94|96|90|98|78|74|66|64|64|72|
|put<br>~~b~~ottles<br>~~d~~ustbin|90|84|90|92|36|42|34|44|30|38|
|put<br>~~o~~bject<br>~~c~~abinet|90|78|88|90|60|60|60|54|72|64|
|rotate<br>~~q~~rcode|88|88|94|82|64|64|64|68|56|52|
|scan<br>~~o~~bject|96|94|90|94|60|70|46|48|54|54|
|shake<br>~~b~~ottle|100|100|100|100|100|98|98|98|100|96|
|shake<br>~~b~~ottle<br>~~h~~orizontally|100|98|100|100|98|98|98|98|96|98|
|stack<br>~~b~~locks<br>~~t~~hree|92|94|94|100|4|20|4|6|8|16|
|stack<br>~~b~~locks<br>~~t~~wo|100|100|100|100|40|50|64|66|42|58|
|stack<br>~~b~~owls<br>~~t~~hree|86|72|82|76|48|56|36|46|52|50|
|stack<br>~~b~~owls<br>~~t~~wo<br>|96<br>|98<br>|92<br>|98<br>|70<br>|84<br>|72<br>|74<br>|80<br>|74<br>|
|stamp<br>~~s~~eal|88|92|90|92|26|34|40|30|18|32|
|turn<br>~~s~~witch|56|56|68|68|40|48|32|36|50|38|
|**Average**|86.76|84.88|91.92|91.84|59.44|61.32|56.92|59.56|58.28|59.56|


24 

Preprint. 

Table 14: Per-task success rates (%) of our method with LingBot-VLA and Fast-WAM as teachers on RoboTwin 2.0 at 1, 2, and 4 denoising steps, under clean and randomized settings. Ours (X) denotes our method trained with X as the teacher. 

||||**Ours (Lin**|**gBot-VL**|**A)**||||**Ours (F**|**ast-WAM**|**)**||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Task**|**1-**|**step**|**2-**|**step**|**4-**|**step**|**1-**|**step**|**2-**|**step**|**4**|**-step**|
||**Clean**|**Random**|**Clean**|**Random**|**Clean**|**Random**|**Clean**|**Random**|**Clean**|**Random**|**Clean**|**Random**|
|adjust<br>~~b~~ottle|94|96|100|98|100|98|94|98|100|96|100|98|
|beat<br>~~b~~lock<br>~~h~~ammer|72|58|84|68|66|66|56|50|76|68|80|74|
|blocks<br>~~r~~anking<br>~~r~~gb|34|32|38|44|52|56|34|32|44|32|32|32|
|blocks<br>~~r~~anking<br>~~s~~ize|6|6|20|18|28|16|12|8|12|10|20|14|
|click<br>~~a~~larmclock|24|46|22|38|36|54|90|82|82|92|90|90|
|click<br>~~b~~ell|94|92|82|88|66|74|100|100|98|94|98|92|
|dump<br>~~b~~in<br>~~b~~igbin|60|56|76|72|84|78|76|76|70|68|76|86|
|grab<br>~~r~~oller|96|98|96|98|98|96|100|98|100|100|100|98|
|handover<br>~~b~~lock|12|12|14|16|26|22|20|12|22|24|30|20|
|handover<br>~~m~~ic|58|66|70|64|72|70|58|68|72|74|86|92|
|hanging<br>~~m~~ug|6|6|10|12|6|18|2|4|4|2|6|10|
|lift<br>~~p~~ot|78|80|92|86|84|86|70|74|74|74|82|76|
|move<br>~~c~~an<br>~~p~~ot|38|32|22|46|32|46|22|26|26|40|22|20|
|move<br>~~p~~illbottle<br>~~p~~ad|50|40|70|70|72|68|44|52|60|62|60|56|
|move<br>~~p~~layingcard<br>~~a~~way<br><br>|70<br>|82<br>|86<br>|84<br>|86<br>|86<br>|68<br>|78<br>|72<br>|78<br>|76<br>|84<br>|
|move<br>~~s~~tapler<br>~~p~~ad|20|22|20|20|24|20|14|16|16|22|16|32|
|open<br>~~l~~aptop|92|94|88|90|82|84|78|86|76|90|76|92|
|open<br>~~m~~icrowave|6|12|10|12|12|26|10|4|14|20|14|26|
|pick<br>~~d~~iverse<br>~~b~~ottles|56|36|66|44|58|44|48|40|48|36|50|42|
|pick<br>~~d~~ual<br>~~b~~ottles|74|58|60|62|58|52|52|64|70|58|68|68|
|place<br>~~a~~2b<br>~~l~~eft|38|42|30|44|38|44|32|40|34|42|40|42|
|place<br>~~a~~2b<br>~~r~~ight|28|34|36|38|38|38|28|38|46|44|40|50|
|place<br>~~b~~read<br>~~b~~asket|52|52|58|56|64|60|64|56|70|64|70|64|
|place<br>~~b~~read<br>~~s~~killet|80|64|70|58|76|68|70|52|76|62|68|68|
|place<br>~~b~~urger<br>~~f~~ries|96|90|92|92|98|94|90|90|98|96|98|96|
|place<br>~~c~~an<br>~~b~~asket|40|38|58|40|44|36|42|24|34|22|26|16|
|place<br>~~c~~ans<br>~~p~~lasticbox|58|60|82|78|80|76|52|44|72|78|84|78|
|place<br>~~c~~ontainer<br>~~p~~late|84|90|96|88|90|94|88|92|76|82|92|92|
|place<br>~~d~~ual<br>~~s~~hoes|52|52|48|70|56|68|50|54|56|62|58|56|
|place<br>~~e~~mpty<br>~~c~~up|78|84|94|96|90|98|72|56|70|68|86|76|
|place<br>~~f~~an|16|16|40|48|48|44|24|14|38|52|44|44|
|place<br>~~m~~ouse<br>~~p~~ad|28|24|26|46|28|50|20|28|30|36|38|26|
|place<br>~~o~~bject<br>~~b~~asket|66|58|80|72|70|74|44|30|56|32|66|56|
|place<br>~~o~~bject<br>~~s~~cale|40|46|52|60|54|56|32|34|38|58|44|50|
|place<br>~~o~~bject<br>~~s~~tand|66|80|66|82|70|86|70|64|70|88|74|90|
|place<br>~~p~~hone<br>~~s~~tand|26|52|44|58|54|72|40|48|40|58|48|62|
|place<br>~~s~~hoe|82|84|84|86|84|90|66|80|74|82|68|80|
|press<br>~~s~~tapler|86|78|74|74|72|74|80|84|74|72|74|70|
|put<br>~~b~~ottles<br>~~d~~ustbin|8|10|20|10|18|34|6|4|14|22|34|38|
|put<br>~~o~~bject<br>~~c~~abinet|40|28|52|46|56|54|52|46|68|62|58|52|
|rotate<br>~~q~~rcode|66|54|60|64|60|72|58|52|64|54|52|58|
|scan<br>~~o~~bject|58|48|58|64|52|64|64|50|54|54|50|62|
|shake<br>~~b~~ottle|98|98|100|100|96|96|98|96|96|98|98|96|
|shake<br>~~b~~ottle<br>~~h~~orizontally|96|94|98|98|100|98|96|94|100|98|94|94|
|stack<br>~~b~~locks<br>~~t~~hree|6|2|2|4|10|14|10|0|8|12|6|10|
|stack<br>~~b~~locks<br>~~t~~wo|20|16|32|36|46|56|30|36|42|50|56|58|
|stack<br>~~b~~owls<br>~~t~~hree|6|12|36|30|50|34|16|14|28|24|42|40|
|stack<br>~~b~~owls<br>~~t~~wo|68|46|74|70|76|86|62|48|58|70|84|68|
|stamp<br>~~s~~eal|12|20|20|38|30|46|14|18|16|36|10|28|
|turn<br>~~s~~witch|40|48|46|38|40|26|38|36|40|40|40|38|
|**Average**|51.48|50.88|57.08|58.28|58.60|61.24|51.12|49.80|55.52|57.16|58.48|59.20|


25 

Preprint. 

## F QUALITATIVE RESULTS 

We provide qualitative results in simulation (Fig. 11) and on the real-robot (Fig. 12) experiments. 


Figure 11: **Qualitative results on RoboTwin 2.0.** FastOPD distilled from LingBot-VLA (NFE=1) executing four tasks under the clean (top) and randomized (bottom) settings, where the randomized setting introduces cluttered distractors, textured tabletops, and varied backgrounds. 


Figure 12: **Qualitative results on the real-world task.** Rollouts of the MolmoAct2 teacher and the student after Stage 1 (initialization) and Stage 2 (FastOPD) on the YAM robot arm, in which the robot picks up a ball and places it on a plate. Time progresses from left to right; insets show the wrist-camera view. 

26 

