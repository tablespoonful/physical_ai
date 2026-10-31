---
title: "Function-Space Diffusion for Motion Planning"
date: "2026-07-03"
authors: "Zinuo Chang; Yipu Chen; Byoungwoo Park; Hongzhe Yu; Yongxin Chen"
url: https://arxiv.org/abs/2607.02977
pdf: https://arxiv.org/pdf/2607.02977
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2607.02977)** / [論文ページ](https://arxiv.org/abs/2607.02977)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

Function-Space Diffusion for Motion Planning 

Zinuo Chang, Yipu Chen, Byoungwoo Park, Hongzhe Yu, and Yongxin Chen 

**_Abstract_ —Diffusion-based motion planners have demonstrated strong performance in generating diverse and high-quality robot trajectories in cluttered environments with multiple feasible solutions. However, existing approaches typically operate on fixedlength waypoint sequences, making the learned model resolutiondependent, thereby preventing zero-shot generalization across resolutions. In this work, we propose Function-Space Diffusion for Motion Planning (FSD-MP), a diffusion-based motion planner that models trajectories as continuous functions and performs diffusion directly in function space, achieving discretizationinvariant trajectory generation. We define a mode-wise forward process in the spectral domain, driven by Gaussian noise with a Matérn-type covariance, and parameterize the reverse process with a boundary-compatible Discrete Sine Transform-based Fourier Neural Operator (DST-FNO) that preserves start-goal constraints across resolutions. We evaluate FSD-MP on 2D point robot and 7-DoF Franka manipulator planning benchmarks. Our method achieves competitive planning performance at the training resolution and generalizes zero-shot across resolutions up to 16× higher, preserving consistent planning behavior without retraining. These results demonstrate that function-space diffusion provides an effective framework for discretization-invariant motion planning.** 

# I. INTRODUCTION 

Motion planning is a crucial component of robotic systems, aiming to find smooth and collision-free trajectories that connect start and goal configurations in cluttered environments. The problem is inherently non-convex due to obstacles, and often admits multiple distinct solutions. 

Classical motion planning methods have been extensively studied from both optimization-based and sampling-based perspectives. Trajectory optimization methods refine an initial trajectory by minimizing costs related to smoothness, collision avoidance, and task objectives [1]–[4]. While often effective in practice, they are sensitive to initialization and may converge to poor local minima or infeasible solutions under non-convex collision constraints. Sampling-based planners explore the configuration space and provide probabilistic completeness guarantees [5]–[7], but their exploration can become inefficient in high-dimensional spaces or narrow passages. Moreover, the resulting paths often require post-processing to satisfy smoothness or control-related requirements. 

These limitations have motivated learning-based motion planners that directly generate feasible trajectories by learning from expert demonstrations. By capturing the distribution of feasible trajectories, such models can rapidly generate diverse, 

Z. Chang is with the School of Electrical and Computer Engineering, Yipu Chen, H. Yu and Yongxin Chen are with the School of Aerospace Engineering, Georgia Institute of Technology, Atlanta, GA; {zchang40, ychen3302, hyu419, yongchen}@gatech.edu 

B. Park is with Korea Advanced Institute of Science and Technology, Daejeon, Republic of Korea; bw.park@kaist.ac.kr 

high-quality solutions without exhaustive online search or carefully designed initialization. Among these approaches, diffusion-based generative models [8]–[10] have proven to be a powerful framework for modeling complex, multimodal trajectory distributions, making them well-suited for motion planning in cluttered and high-dimensional spaces. 

Despite their promise, existing diffusion-based planners represent trajectories as fixed-length waypoint sequences. This tightly couples the learned model to a specific discretization: a model trained at one resolution cannot generalize to another without retraining. This dependence is undesirable in motion planning, where trajectories are naturally continuous, and the appropriate resolution may vary across tasks, environments, and downstream controllers. Coarse discretizations are computationally efficient but may miss geometric details near obstacles, whereas fine discretizations improve fidelity at higher computational cost. 

To address this gap, we propose _Function-Space Diffusion for Motion Planning_ (FSD-MP), which achieves discretization invariance by treating trajectories as continuous functions and performing diffusion directly in function space. This formulation enables zero-shot generalization to arbitrary resolutions without retraining. We demonstrate that a model trained at a base resolution can generate trajectories at up to 16× higher resolution while converging to the same solution modes, maintaining both feasibility and multimodality. 

Our key contributions are: 

- A function-space diffusion framework for motion planning that is inherently discretization-invariant, enabling flexible trajectory generation at arbitrary resolutions without retraining. 

- A boundary-compatible neural operator architecture that consistently satisfies start-goal constraints across resolutions. 

- Experimental demonstration of zero-shot super-resolution up to 16× the training resolution, while preserving consistent planning behavior across resolutions. 

# II. RELATED WORK 

_a) Learning-based Planning:_ Learning-based methods aim to encode trajectory distributions from demonstrations or expert planners, providing informative biases for sampling, optimization, or direct trajectory generation. Early approaches use Gaussian Mixture Models and Probabilistic Movement Primitives [11], [12], but such models scale poorly to highdimensional configuration spaces. More recent approaches adopt deep generative models, including generative adversarial networks (GANs), variational autoencoders (VAEs), normalizing flows, and energy-based models (EBMs), to learn 


Fig. 1: Overview of FSD-MP. **(Top)** The forward process performs zero-end projection, transforms trajectories into DST coefficients and applies mode-wise diffusion with variance scaled by eigenvalue _λk_ . **(Bottom)** The reverse process denoises via FiLM-conditioned DST-FNO layers, together with guidance based on the predicted clean trajectory _x_ ˆ0. The function-space formulation enables **discretization-invariant** trajectory generation across both coarse and fine discretizations. 

richer trajectory distributions for planning [13]–[16]. However, these models often require trade-offs among distributional expressiveness, training stability, and conditional generation flexibility, motivating diffusion models as a flexible framework for modeling complex, multimodal trajectory distributions. 

_b) Diffusion Models in Robotics:_ Diffusion models generate samples by learning to reverse an iterative noising process [17], [18]. Their expressive modeling capacity and flexible conditioning have led to broad adoption in robotics, including policy learning, manipulation, and decision-making [19]– [22]. In motion planning, Diffuser [8] pioneered the application of diffusion models to offline reinforcement learning and trajectory planning. Motion Planning Diffusion (MPD) [9] further adapted diffusion for robot manipulation to generate diverse, collision-free trajectories conditioned on task goals. These works demonstrate the effectiveness of diffusion models for capturing multimodal trajectory distributions. However, most existing diffusion-based methods operate on finitedimensional waypoint or action sequences with a fixed discretization, limiting their ability to generalize across different resolutions. 

_c) Diffusion Models in Function Space:_ Recent works have extended diffusion and score-based generative models to infinite-dimensional function spaces [23]–[25], enabling discretization-invariant generation. These function-space formulations have been applied to diverse domains with naturally 

continuous structure, including image generation and physicsinformed problems governed by PDEs such as Navier–Stokes. Despite this progress, function-space diffusion remains largely unexplored in robotics and motion planning, even though trajectories are inherently continuous functions and practical deployment often requires flexible discretizations. Our work addresses this gap by formulating motion planning as diffusion over trajectory functions, enabling zero-shot generalization across arbitrary discretizations. 

# III. PROBLEM FORMULATION 

Motion planning involves finding a smooth, collision-free trajectory between the start and goal configurations _qs, qg ∈_ R<sup>_d_</sup> , where _d_ denotes the dimension of the robot configuration space. We represent a trajectory as a continuous function 


where _τ ∈_ [0 _,_ 1] denotes normalized time. The planning problem is to find an optimal trajectory _x_<sup>_⋆_</sup> ( _τ_ ) that minimizes a cost functional _J_ for a given set of end-point configurations: 


with the objective decomposed as 


where _J_ prior encourages smoothness or consistency with prior knowledge of feasible trajectories, and _J_ task penalizes taskdependent constraint violations in the environment _O_ . 

We adopt a probabilistic perspective and view motion planning as posterior inference over trajectory functions: 


where _p_ ( _x_ ) represents a prior distribution over smooth, feasible trajectories, and the likelihood _p_ ( _O | x_ ) encodes taskspecific constraints such as collision avoidance and joint limits. 

This posterior perspective generalizes deterministic optimization by capturing uncertainty and multimodality in feasible motions. Our goal is to generate collision-free trajectories by sampling from the posterior _p_ ( _x | O_ ). 

# IV. FUNCTION-SPACE DIFFUSION MOTION PLANNING 

We propose _Function-Space Diffusion for Motion Planning_ (FSD-MP), which samples from the posterior _p_ ( _x|O_ ) defined in Section III while achieving discretization invariance. Rather than parameterizing trajectories as fixed-length waypoint sequences, FSD-MP represents each trajectory as a continuous function _x_ ( _τ_ ) _∈H_ , in a Hilbert space _H_ = _L_<sup>2</sup> ([0 _,_ 1] _,_ R<sup>_d_</sup> ). The model learns the function-space prior _p_ ( _x_ ), while the likelihood _p_ ( _O|x_ ) is incorporated at inference time via classifier guidance [9], [26]. This function-space formulation enables trajectory generation at arbitrary resolutions without retraining, as discretization is introduced only during evaluation. 

# _A. Function-Space Forward Diffusion_ 

We define the forward diffusion process over trajectories as a linear SDE in the trajectory space _H_ : 


where _xt ∈H_ is the noisy trajectory function at diffusion time _t ∈_ [0 _, T_ ], _β_ ( _t_ ) _≥_ 0 is a noise schedule, _F_ : _D_ ( _F_ ) _⊂ H →H_ is the linear drift operator, _G_ : _H →H_ is the linear diffusion operator, and _Wt_ is a cylindrical Wiener process. The corresponding noise covariance operator is _C_ = _GG_<sup>_∗_</sup> . 

This construction generalizes the Variance Preserving (VP) SDE to function space: _F_ controls the diffusion rate across spectral modes, while _G_ determines the covariance geometry of the injected noise. 

To make (5) analytically tractable, we assume _F_ and _G_ share an orthonormal eigenbasis _{ϕk}k∈_ N with eigenvalues 


Projecting _xt_ onto each spectral mode, _Xt_<sup>_k_=</sup><sup>_⟨xt, ϕk⟩_,the</sup> SDE (5) decouples into independent coefficient SDEs: 


where _{Wt_<sup>_k}_areindependentstandardBrownianmotions.</sup> This modal decomposition admits closed-form marginals: 


and _α_ ( _t_ ) is the noise schedule in standard diffusion. 

To simplify the expression, we introduce a rescaled noise variable _ξ ∼N_ (0 _, F_<sup>_−_1</sup> _C_ ), whose coefficients satisfy 


With this reparameterization, the forward process in (7) admits a compact form analogous to standard diffusion: 


This yields a training objective that decomposes over modes (see Appendix A): 


By Parseval’s identity, this is equivalent to minimizing the MSE of _ξ_ in the trajectory domain: 


_Well-Defined Noise in Function Spaces:_ A critical challenge in infinite-dimensional diffusion is defining valid Gaussian noise in _H_ . A Gaussian measure _N_ (0 _, C_ ) is supported on _H_ only if its covariance _C_ is trace-class [23], [25]. This rules out white noise, whose identity covariance _I_ is not trace-class. We therefore adopt a Matérn-type covariance operator: 


where ∆ is the Laplacian under the chosen boundary condition, and _σ, κ, α >_ 0 control variance, length scale, and smoothness. For time-parameterized trajectories, _C_ is traceclass when _α >_ 1 _/_ 2. Details are provided in Appendix B. 

# _B. Resolution-Agnostic Neural Operator_ 

The reverse diffusion process requires learning a noise prediction operator _ξθ_ ( _xt, t_ ) : _H×_ [0 _, T_ ] _→H_ . Standard diffusion models typically parameterize this mapping with architectures like U-Net [17], [27] operating on fixed-size vectors in R<sup>_N×d_</sup> , making them inherently resolution-dependent. 

To achieve discretization invariance, we parameterize _ξθ_ as a neural operator that learns the mapping between function spaces. We adopt Fourier Neural Operator (FNO) [28], which operates in the Fourier domain by learning spectral kernels that act on frequency modes rather than spatial discretizations. 

An FNO model consists of a lifting layer _P_ that embeds the input into feature space, a series of Fourier layers, and a projection layer _Q_ mapping back to the trajectory space. Each _Fourier layer_ defines an operator _N_ that transforms a feature function _u_ : [0 _,_ 1] _→_ R<sup>_c_</sup> , where _c_ denotes the hidden channel dimension, as: 


where _F_ and _F_<sup>_−_1</sup> denote the Fast Fourier Transform (FFT) and its inverse, _R ∈_ C<sup>_K×c×c_</sup> contains learned complex weights applied to the first _K_ modes, _W ∈_ R<sup>_c×c_</sup> is a pointwise linear transform, and _σ_ is a nonlinear activation. 

This frequency-domain transformation enables the same operator to be evaluated at different resolutions without retraining. 

# _C. Endpoint Constraint Enforcement_ 

In motion planning problems, trajectories must satisfy fixed endpoint constraints: _x_ (0) = _qs_ and _x_ (1) = _qg_ . Existing diffusion planners such as Diffuser and MPD [8], [9] enforce this through inpainting, directly replacing endpoint values during training and sampling. However, in our function-space formulation, the trajectories are continuous functions with global spatial correlation. Naively fixing endpoints will therefore introduce inconsistencies and degrade sampling stability. We address this through three components: zero-end projection, endpoint-conditioning via FiLM, and a boundary-compatible DST-based neural operator. 

_a)_ **_Zero-End Projection_** _:_ We enforce endpoint constraints by reformulating constrained trajectory generation as a zero-boundary residual learning problem: 


which satisfies _x_ ˜(0) = _x_ ˜(1) = 0 by construction. We apply this projection to all trajectories during training, so the model learns the distribution over zero-boundary residuals _p_ (˜ _x_ ). 

At inference, we sample a residual function _x_ ˜( _τ_ ) and recover the full trajectory via 


Since (15) is a deterministic affine transformation applied after sampling, the reconstructed trajectory is _guaranteed_ to satisfy _x_ (0) = _q_ s and _x_ (1) = _q_ g exactly, without post-hoc endpoint clamping or iterative correction. 

_b)_ **_Conditional Generation via FiLM_** _:_ The zero-end projection removes absolute position information from trajectories, making the residual distribution _p_ (˜ _x_ ) endpointdependent. We therefore condition the neural operator on the endpoint information using Feature-wise Linear Modulation (FiLM) [29], which modulates intermediate feature functions _u_ via learned affine transformations: 


where _γ, δ ∈_ R<sup>_c_</sup> are channel-wise scale and shift parameters. These modulation parameters are generated from the conditioning vector **c** = [ _qs_ ; _qg_ ; emb( _t_ )] through a per-layer MLP: 


where _ℓ_ indexes the neural-operator layer. This allows the network to adapt its predictions to each start-goal configuration while preserving the zero-boundary residual representation. 


_c)_ **_Boundary-Compatible DST-FNO_** _:_ The zero-end projection imposes a boundary structure that should be preserved when the model is evaluated at resolutions different from the training resolution. However, standard FNO (Sec IV-B) relies on the FFT, whose periodic basis does not encode the zeroboundary condition. As a result, although the periodic basis fits the training-resolution data well, it may produce endpoint artifacts and degrade cross-resolution generalization. 

To provide a boundary-compatible spectral representation, we replace the FFT with the discrete sine transform (DST), whose sine basis _ϕk_ ( _s_ ) = sin( _kπs_ ) are naturally compatible with the endpoint structure. The Fourier layer becomes: 


where _S_ and _S_<sup>_−_1</sup> denote the DST and inverse DST, and _R ∈_ R<sup>_K×c×c_</sup> is a real-valued spectral kernel. For intermediate features with nonzero endpoints, we apply zero-end projection (14) before _S_ and reconstruct afterward. 

We refer to this modified architecture as _DST-FNO_ , a minimal yet principled modification that provides the correct boundary inductive bias for cross-resolution generalization. 


Fig. 2: Environments used in the motion planning experiments. Gray obstacles are present during training, while red obstacles are introduced only at inference time to evaluate generalization to unseen obstacles. 

# _D. Inference via Guided Sampling_ 

To generate collision-free trajectories, we sample from the learned prior _p_ (˜ _x_ ) and incorporate guidance during the reverse process. Since the forward process (9) admits a closed-form marginal for each spectral mode, we perform DDIM [30] updates mode-wise in the spectral domain. It is also possible to use other more advanced inference algorithms [31], [32]. 

Given the noisy coefficient _X_<sup>˜</sup> _t_<sup>_k_andthenoiseprediction</sup> _ξθ_<sup>_k_(˜</sup><sup>_xt, t, q_s</sup><sup>_, q_g),wefirstestimatethecleancoefficient:</sup> 


where _ξθ_ is our trained DST-FNO. DDIM then transports _X_<sup>˜</sup> _t_<sup>_k_</sup> to the next step _s < t_ : 


where _z_<sup>_k_</sup> _∼N_ (0 _, µ_<sup>2</sup> _k_<sup>_/λk_)and</sup><sup>_η∈_[0</sup><sup>_,_1]controlsthestochas-</sup> ticity. 

The DDIM sampler generates trajectories from the learned prior but does not explicitly enforce collision avoidance. To incorporate obstacle constraints, we introduce a Boltzmannform likelihood _p_ ( _O | x_ ) _∝_ exp( _−C_ ( _x_ )), where _C_ ( _x_ ) is a differentiable collision cost, and adopt a classifier guidance style update to incorporate it during sampling. A common practice is to evaluate this likelihood directly on the noisy sample _xt_ [8], [9], but collision avoidance should be evaluated with respect to the final trajectory _x_ 0. Formally, this likelihood requires marginalization over the unknown clean trajectory: 


which is intractable in practice. Following [33], [34], we approximate it using the current clean prediction _x_ ˆ0: 


This avoids computing collision gradients on highly corrupted samples and better aligns the guidance with the final denoised trajectory. 

During each reverse step, we first perform an unguided DDIM update using (20) to obtain an intermediate prediction _µ_ ˜ _s_ , at which the guidance direction is evaluated: 


We then obtain the guided iterate through a covariancepreconditioned update [26]: 


where Σ _t_ denotes the covariance preconditioner. 


# _A. Experimental Setup_ 

_a) Environments and Datasets:_ We evaluate FSD-MP across four environments covering 2D point robot and 3D manipulator planning, following the setup of MPD [9]. As shown in Fig. 2, **Simple2D** and **Dense2D** involve a point robot navigating in 2D workspaces with sparse and dense obstacles, respectively. **Spheres3D** and **Warehouse** evaluate a 7-DoF Franka manipulator planning in 3D workspaces, where Spheres3D contains spherical obstacles, while Warehouse offers a more realistic environment with tables and a shelf. To test the generalization capability to unseen obstacles, each environment is further extended with additional obstacles not present during training. 

For each environment, we generate an expert dataset using the same pipeline as MPD. We first use RRTConnect [7] to obtain initial feasible trajectories, then refine them with GPMP [3] to produce smooth demonstrations for diffusion training. 

_b) Baselines:_ We compare FSD-MP against four baselines. **MPD** [9] is a diffusion-based planner trained and evaluated at a fixed resolution. **MPD-Spline** [10] fits training trajectories with B-spline curves and trains a diffusion model over the resulting low-dimensional control points, yielding a continuous trajectory representation. **GPMP** [3] represents trajectories as continuous-time Gaussian processes and optimizes them via factor graph inference. Additionally, we evaluate **MPD-Retrain** , which retrains MPD from scratch at each target resolution, to examine whether a single FSD-MP model can match resolution-specific retraining. 

_c) Metrics:_ We evaluate the performance through two average metrics. Success rate measures the percentage of start-goal pairs for which at least one generated trajectory is collision-free. Valid rate measures the percentage of generated trajectories that are collision-free. Each method is evaluated over 120 randomly sampled start–goal pairs per environment, generating 100 trajectory samples per pair. 

# _B. Planning Results_ 

Tab. I compares FSD-MP with baselines in both training and extra-obstacle environments (see Fig. 2). In the training environments, diffusion-based methods are evaluated without guidance to assess the quality of the learned trajectory distribution. In the extra-obstacle settings, we introduce additional obstacles during inference and apply guidance to adapt to these unseen obstacles. GPMP is optimized directly in the corresponding environment for each setting. 

At the training resolution, FSD-MP achieves competitive or higher success and valid rates compared with the baselines across both 2D point robot and 3D Franka manipulator environments. These results indicate that FSD-MP can generate high-quality samples and generalize across diverse planning problems, including high-dimensional manipulation tasks. 

To evaluate cross-resolution generalization, we train the model only at resolution _N_ = 64 and perform inference at unseen resolutions without retraining. As shown in Tab. I, FSD-MP maintains nearly identical performance across _N_ = 64 and _N_ = 1024, demonstrating zero-shot cross-resolution inference. Fig. 3 further visualizes Dense2D results with extra obstacles at _N_ = 50, _N_ = 64, _N_ = 1024, and _N_ = 2000, yielding nearly identical trajectories across resolutions. 

Fig. 4 visualizes representative planning results of FSDMP in the 3D Franka environments. Across different startgoal contexts in both Spheres3D and Warehouse, the generated trajectories remain smooth and avoid the additional obstacles. 

# _C. Ablation Studies_ 

We conduct ablation studies on Dense2D and Warehouse to validate the key design components of FSD-MP. We evaluate three variants: **FNO** , which replaces the DST-based spectral layers with standard FFT layers; **White Noise** , which replaces the Matérn-type covariance with an identity covariance; and **UNet** , which replaces the DST-FNO backbone with a UNet of comparable parameter count. All models are trained at _N_ = 64 and evaluated across multiple resolutions without retraining. Table II reports the collision-free rate. 

FSD-MP maintains nearly constant performance across resolutions in both environments, whereas the ablated variants degrade under cross-resolution inference. The standard FNO performs well near _N_ = 64 but drops substantially at high resolutions, showing the importance of the boundary-compatible DST basis. White noise consistently underperforms FSD-MP across all resolutions, indicating the benefit of well-defined function-space perturbations. The UNet variant performs well only at the training resolution and fails to generalize across resolutions, confirming the need for a resolution-agnostic neural operator. 


Fig. 3: FSD-MP planning results in Dense2D with extra obstacles. The model is trained only at resolution _N_ = 64 and evaluated at multiple resolutions without retraining. 

# VI. CONCLUSION 

We presented Function-Space Diffusion for Motion Planning (FSD-MP), a diffusion-based motion planner that operates in infinite-dimensional function space. By combining function-space diffusion with a boundary-compatible DSTFNO, FSD-MP achieves zero-shot generalization across arbitrary resolutions without retraining. Experiments on 2D point robot and 3D Franka manipulator environments demonstrate competitive planning performance at the training resolution and nearly identical performance under cross-resolution inference. Future work will explore extension to higherdimensional configuration spaces, coarse-to-fine inference, and adaptive-resolution generation with local refinement near dense obstacles or narrow passages. 

# APPENDIX 

# _A. Objective for FSD-MP_ 

We derive the training objective from the conditional distribution _p_ ( _xt | x_ 0) in the function space. From the closedform marginal (9), the coefficients _{Xt_<sup>_k}_areconditionally</sup> independent given _x_ 0, with 


where each component follows a Gaussian distribution. 

TABLE I: Benchmarking in different resolutions and environments 

|||Trai|ning Environ|ment (Prior O|nly)||Extra Obstac|les (Guided)||
|---|---|---|---|---|---|---|---|---|---|
|||_N_ =|64|_N_ =|1024|_N_ =|64|_N_ =|1024|
|**Env**|**Method**|Succ. (%)|Valid (%)|Succ. (%)|Valid (%)|Succ. (%)|Valid (%)|Succ. (%)|Valid (%)|
|D|GPMP|100|98.6|100|99.8|100|98.0|99.2|96.9|
|E2|MPD|100|99.7|–|–|100|91.6|–|–|
|PL|MPD-Retrain|–|–|100|99.8|–|–|100|94.4|
|IM|MPD-Spline|100|94.3|100|92.8|100|76.3|100|75.6|
|S|FSD-MP (Ours)|100|99.9|100|99.8|100|97.7|100|98.4|
|D|GPMP|98.3|58.3|75.8|50.7|91.7|50.2|35.8|24.5|
|2|MPD|100|99.7|–|–|89.2|54.3|–|–|
|NSE|MPD-Retrain|–|–|100|99.8|–|–|90|63.7|
|E|MPD-Spline|91.7|71.5|85|54.1|83.3|31.1|79.2|28.5|
|D|FSD-MP (Ours)|100|99.8|100|99.9|91.7|62.6|91.7|66.4|
|D|GPMP|95.8|79.6|92.5|89.3|91.7|76.4|90.0|80.2|
|S3|MPD|95|71.7|–|–|89.2|62.0|–|–|
|RE|MPD-Retrain|–|–|96.7|73.3|–|–|92.5|72.8|
|HE|MPD-Spline|80.8|27.2|80|26.1|86.7|42.3|83.3|39.6|
|SP|FSD-MP (Ours)|100|83.8|100|83.4|96.7|75.5|96.7|75.5|
|SE|GPMP|99.2|92.1|93.3|86.3|99.2|95.0|91.7|85.4|
|OU|MPD|94.2|88.5|–|–|99.2|98.7|–|–|
|EH|MPD-Retrain|–|–|95.0|88.8|–|–|99.2|99.1|
|AR|MPD-Spline|92.5|75.9|91.7|74.6|96.7|93.2|96.7|94.5|
|W|FSD-MP (Ours)|95.8|90.3|95.8|90.2|100|100|100|100|


(a) Spheres3D, Context 1 (b) Spheres3D, Context 2 


(c) Warehouse, Context 1 (d) Warehouse, Context 2 

Fig. 4: Planning results of FSD-MP in 3D Franka arm environments. Orange lines are end-effector trajectories. 

TABLE II: Ablation on Architecture and Diffusion Noise: Valid Rate (%) Across Resolution _N_ 

||||Dense2D|||||Warehous|e||
|---|---|---|---|---|---|---|---|---|---|---|
|Method|_N_=32|_N_=64|_N_=256|_N_=512|_N_=1024|_N_=32|_N_=64|_N_=256|_N_=512|_N_=1024|
|FSD-MP|**99.5**|**99.8**|**99.8**|**99.8**|**99.8**|**90.8**|90.3|**90.1**|**90.2**|**90.2**|
|FNO|95|99.6|88.7|73.4|63.5|90.1|**90.5**|84.8|80.6|77.2|
|White Noise|94.7|96.0|96.7|96.8|97.0|85.8|86.1|86.4|86.6|86.8|
|UNet|0.3|97.3|0.1|0|0|64.2|87.2|51.6|38.8|26.4|


The score in the function space is defined as _∇xt_ log _p_ ( _xt | x_ 0), which admits the expansion in the basis _{ϕk}ϕk}k}}_ : 

poses into 


For each mode, the conditional distribution is Gaussian, and its score is linearly related to the noise _ξ_<sup>_k_</sup> . Up to a mode-dependent scalar, predicting the score is equivalent to predicting the noise _ξ_<sup>_k_</sup> . This leads to the objective 

We consider score matching in the function space, which minimizes 


Using the orthonormal basis _{ϕk}_ , this objective decom- 

Finally, Parseval’s identity<sup>�</sup><sup>_∞_</sup> _k_ =1 �� _ξθk_<sup>_−ξk_��2=</sup><sup>_∥ξθ−ξ∥_</sup> _H_<sup>2</sup> yields _L_ ( _θ_ ) = E _t,x_ 0 _,ξ_ � _∥ξθ_ ( _xt, t_ ) _− ξ∥_<sup>2</sup> _H_ � (30) 

which recovers the objective in (11). 

# _B. Trace-Class Gaussian Noise in Function Space_ 

A Gaussian measure _N_ (0 _, C_ ) on _H_ is the infinitedimensional analogue of a multivariate Gaussian noise, characterized by a covariance operator _C_ : _H →H_ . It is supported on _H_ only if _C_ is trace-class, self-adjoint, and positive, ensuring finite expected energy E � _∥x∥_<sup>2</sup> _H_ � = tr( _C_ ) _< ∞_ . The identity operator fails this requirement since tr( _I_ ) =<sup>�</sup><sup>_∞_</sup> _k_ =1<sup>1=</sup><sup>_∞_,</sup> making white noise _N_ (0 _, I_ ) ill-defined in _H_ . 

The Matérn-type operator _C_ = _σ_<sup>2</sup> ( _−_ ∆+ _κ_<sup>2</sup> _I_ )<sup>_−α_</sup> satisfies all three conditions when _α_ is sufficiently large. Its covariance eigenvalues decay as _λk ∼ k_<sup>_−_2</sup><sup>_α/D_</sup> , giving tr( _C_ ) =<sup>�</sup> _k_<sup>_λk<_</sup> _∞_ when _α > D/_ 2, where _D_ is the input dimension of the function. For time-parameterized trajectories, _D_ = 1 and the condition reduces to _α >_ 1 _/_ 2. 

# REFERENCES 

- [1] N. Ratliff, M. Zucker, J. A. Bagnell, and S. Srinivasa, “Chomp: Gradient optimization techniques for efficient motion planning,” in _IEEE International Conference on Robotics and Automation (ICRA)_ , 2009, pp. 489–494. 

- [2] M. Kalakrishnan, S. Chitta, E. Theodorou, P. Pastor, and S. Schaal, “Stomp: Stochastic trajectory optimization for motion planning,” in _IEEE International Conference on Robotics and Automation (ICRA)_ , 2011, pp. 4569–4574. 

- [3] M. Mukadam, J. Dong, X. Yan, F. Dellaert, and B. Boots, “Continuoustime gaussian process motion planning via probabilistic inference,” _The International Journal of Robotics Research_ , vol. 37, no. 11, pp. 1319– 1340, 2018. 

- [4] H. Yu and Y. Chen, “A gaussian variational inference approach to motion planning,” _IEEE Robotics and Automation Letters_ , vol. 8, no. 5, pp. 2518–2525, 2023. 

- [5] L. Kavraki, P. Svestka, J.-C. Latombe, and M. Overmars, “Probabilistic roadmaps for path planning in high-dimensional configuration spaces,” _IEEE Transactions on Robotics and Automation_ , vol. 12, no. 4, pp. 566– 580, 1996. 

- [6] S. Karaman and E. Frazzoli, “Sampling-based algorithms for optimal motion planning,” _The International Journal of Robotics Research_ , vol. 30, no. 7, pp. 846–894, 2011. 

- [7] J. J. Kuffner and S. M. LaValle, “Rrt-connect: An efficient approach to single-query path planning,” in _Proceedings 2000 ICRA. Millennium conference. IEEE international conference on robotics and automation. Symposia proceedings (Cat. No. 00CH37065)_ , vol. 2. IEEE, 2000, pp. 995–1001. 

- [8] M. Janner, Y. Du, J. B. Tenenbaum, and S. Levine, “Planning with diffusion for flexible behavior synthesis,” in _International Conference on Machine Learning_ , 2022, pp. 9902–9915. 

- [9] J. Carvalho, A. T. Le, M. Baierl, D. Koert, and J. Peters, “Motion planning diffusion: Learning and planning of robot motions with diffusion models,” in _2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2023, pp. 1916–1923. 

- [10] J. Carvalho, A. T. Le, P. Kicki, D. Koert, and J. Peters, “Motion planning diffusion: Learning and adapting robot motion planning with diffusion models,” _IEEE Transactions on Robotics_ , 2025. 

- [11] S. Calinon, F. Guenter, and A. Billard, “On learning, representing, and generalizing a task in a humanoid robot,” _IEEE Transactions on Systems, Man, and Cybernetics, Part B (Cybernetics)_ , vol. 37, no. 2, pp. 286–298, 2007. 

   - [13] T. S. Lembono, E. Pignat, J. Jankowski, and S. Calinon, “Learning constrained distributions of robot configurations with generative adversarial network,” _IEEE Robotics and Automation Letters_ , vol. 6, no. 2, pp. 4233–4240, 2021. 

   - [14] B. Ichter, J. Harrison, and M. Pavone, “Learning sampling distributions for robot motion planning,” in _2018 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2018, pp. 7087–7094. 

   - [15] T. Power and D. Berenson, “Learning a generalizable trajectory sampling distribution for model predictive control,” _IEEE Transactions on Robotics_ , vol. 40, pp. 2111–2127, 2024. 

   - [16] J. Urain, A. T. Le, A. Lambert, G. Chalvatzaki, B. Boots, and J. Peters, “Learning implicit priors for motion optimization,” in _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2022, pp. 7672–7679. 

   - [17] J. Ho, A. Jain, and P. Abbeel, “Denoising diffusion probabilistic models,” _Advances in neural information processing systems_ , vol. 33, pp. 6840– 6851, 2020. 

   - [18] Y. Song, J. Sohl-Dickstein, D. P. Kingma, A. Kumar, S. Ermon, and B. Poole, “Score-based generative modeling through stochastic differential equations,” _arXiv preprint arXiv:2011.13456_ , 2020. 

   - [19] C. Chi, Z. Xu, S. Feng, E. Cousineau, Y. Du, B. Burchfiel, R. Tedrake, and S. Song, “Diffusion policy: Visuomotor policy learning via action diffusion,” _The International Journal of Robotics Research_ , vol. 44, no. 10-11, pp. 1684–1704, 2025. 

   - [20] U. A. Mishra, S. Xue, Y. Chen, and D. Xu, “Generative skill chaining: Long-horizon skill planning with diffusion models,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 2905–2925. 

   - [21] A. Ajay, Y. Du, A. Gupta, J. Tenenbaum, T. Jaakkola, and P. Agrawal, “Is conditional generative modeling all you need for decision-making?” in _International Conference on Learning Representations_ , 2023. 

   - [22] U. A. Mishra and Y. Chen, “Reorientdiff: Diffusion model based reorientation for object manipulation,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 10 867–10 873. 

   - [23] J. H. Lim, N. B. Kovachki, R. Baptista, C. Beckham, K. Azizzadenesheli, J. Kossaifi, V. Voleti, J. Song, K. Kreis, J. Kautz _et al._ , “Score-based diffusion models in function space,” _Journal of Machine Learning Research_ , vol. 26, no. 158, pp. 1–62, 2025. 

   - [24] G. Kerrigan, J. Ley, and P. Smyth, “Diffusion generative models in infinite dimensions,” in _International Conference on Artificial Intelligence and Statistics_ , 2023. 

   - [25] J. Pidstrigach, Y. Marzouk, S. Reich, and S. Wang, “Infinite-dimensional diffusion models,” _Journal of Machine Learning Research_ , vol. 25, no. 414, pp. 1–52, 2024. 

   - [26] P. Dhariwal and A. Nichol, “Diffusion models beat gans on image synthesis,” _Advances in neural information processing systems_ , vol. 34, pp. 8780–8794, 2021. 

   - [27] O. Ronneberger, P. Fischer, and T. Brox, “U-net: Convolutional networks for biomedical image segmentation,” in _International Conference on Medical image computing and computer-assisted intervention_ . Springer, 2015, pp. 234–241. 

   - [28] Z. Li, N. B. Kovachki, K. Azizzadenesheli, B. liu, K. Bhattacharya, A. Stuart, and A. Anandkumar, “Fourier neural operator for parametric partial differential equations,” in _International Conference on Learning Representations_ , 2021. 

   - [29] E. Perez, F. Strub, H. De Vries, V. Dumoulin, and A. Courville, “Film: Visual reasoning with a general conditioning layer,” in _Proceedings of the AAAI conference on artificial intelligence_ , vol. 32, no. 1, 2018. 

   - [30] J. Song, C. Meng, and S. Ermon, “Denoising diffusion implicit models,” in _International Conference on Learning Representations_ , 2021. 

   - [31] Q. Zhang and Y. Chen, “Fast sampling of diffusion models with exponential integrator,” _arXiv preprint arXiv:2204.13902_ , 2022. 

   - [32] Q. Zhang, M. Tao, and Y. Chen, “gddim: Generalized denoising diffusion implicit models,” _arXiv preprint arXiv:2206.05564_ , 2022. 

   - [33] H. Chung, J. Kim, M. T. Mccann, M. L. Klasky, and J. C. Ye, “Diffusion posterior sampling for general noisy inverse problems,” in _The Eleventh International Conference on Learning Representations_ , 2023. 

   - [34] J. Song, Q. Zhang, H. Yin, M. Mardani, M.-Y. Liu, J. Kautz, Y. Chen, and A. Vahdat, “Loss-guided diffusion models for plug-and-play controllable generation,” in _International Conference on Machine Learning_ . PMLR, 2023, pp. 32 483–32 498. 

- [12] A. Paraschos, C. Daniel, J. R. Peters, and G. Neumann, “Probabilistic movement primitives,” _Advances in neural information processing systems_ , vol. 26, 2013. 

