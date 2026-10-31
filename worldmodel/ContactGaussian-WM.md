---
title: "ContactGaussian-WM: Learning Physics-Grounded World Model from Videos"
date: "2026-02-11"
authors: "Meizhong Wang; Wanxin Jin; Kun Cao; Lihua Xie; Yiguang Hong"
url: https://arxiv.org/abs/2602.11021
pdf: https://arxiv.org/pdf/2602.11021
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.11021)** / [論文ページ](https://arxiv.org/abs/2602.11021)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# ContactGaussian-WM: Learning Physics-Grounded World Model from Videos 

Meizhong Wang, Wanxin Jin, Kun Cao, Lihua Xie, Yiguang Hong 


Fig. 1: ContactGaussian-WM integrates a differentiable collision detector, explicit contact dynamics, and a 3DGS renderer. It takes sparse videos of diverse objects as input, adopts a unified scene representation, and learns a physics-grounded world model that supports downstream tasks such as long-horizon prediction and real-time MPC for in-hand manipulation. 

**_Abstract_ —Developing world models that understand complex physical interactions is essential for advancing robotic planning and simulation. However, existing methods often struggle to accurately model the environment under conditions of data scarcity and complex contact-rich dynamic motion. To address these challenges, we propose ContactGaussian-WM, a differentiable physics-grounded rigid-body world model capable of learning intricate physical laws directly from sparse and contactrich video sequences. Our framework consists of two core components: (1) a unified Gaussian representation for both visual appearance and collision geometry, and (2) an end-toend differentiable learning framework that differentiates through a closed-form physics engine to infer physical properties from sparse visual observations. Extensive simulations and real-world evaluations demonstrate that ContactGaussian-WM outperforms state-of-the-art methods in learning complex scenarios, exhibiting robust generalization capabilities. Furthermore, we showcase the practical utility of our framework in downstream applications, including data synthesis and real-time MPC. Project page:** 

M. Wang, K. Cao (corresponding author), and Yiguang Hong are with the Department of Control Science and Engineering, College of Electronics and Information Engineering, Tongji University, Shanghai 201804, China, the Shanghai Institute of Intelligent Science and Technology, National Key Laboratory of Autonomous Intelligent Unmanned Systems, and Frontiers Science Center for Intelligent Autonomous Systems, Ministry of Education, Beijing 100816, China _{_ 2531784,caokun,yghong _}_ @tongji.edu.cn W Jin is with the School for Engineering of Matter, Transport, and Energy, Arizona State University. wanxinjin@gmail.com L. Xie is with School of Electrical and Electronic Engineering, Nanyang Technological University, 50 Nanyang Avenue, Singapore 639798 elhxie@ntu.edu.sg 

### **https://contactgaussian-wm.github.io/.** 

## I. INTRODUCTION 

World models [1] have emerged as the cognitive engine for autonomous robotics, serving as internal simulators that enable agents to reason about the physical environment. By synthesizing high-dimensional visual observations into predictive representations, these models allow robots to anticipate complex physical behaviors—such as motion, interaction, and deformation—within their ‘mind’s eye’, facilitating efficient planning without costly real-world trial and error. However, learning such world models directly from sparse and contactrich video sequences remains a formidable challenge. 

Current mainstream paradigms for world models, predominantly purely data-driven approaches like video generation [2, 3, 4, 5] and latent dynamics models [6, 7, 8, 9, 10], face significant hurdles in practice. These methods are notoriously data-hungry and often fail to generalize in scenarios characterized by data scarcity or few-shot demonstrations. More critically, without explicit physical grounding, these models prioritize visual plausibility over physical rigor, leading to hallucinations such as object interpenetration or spontaneous disappearance. This absence of inherent constraints further results in a fundamental inability to maintain long-horizon consistency, critical to downstream tasks such as planning. 

To overcome these limitations and mitigate the dependency on massive datasets, the research community is shifting toward 

physics-grounded world models that internalize the invariant laws of nature to ensure long-horizon reliability. Leveraging high-performance simulators (e.g., MuJoCo [11], Bullet [12]) allows for the rigorous simulation of physical laws, which, when coupled with renderers, can be extended to imagelevel world models. However, these frameworks are typically non-differentiable; consequently, to align with the real world, some approaches [13, 14, 15, 16] must employ gradientfree optimization for parameter identification. This paradigm, however, is heavily reliant on data quality while suffering from prohibitive search spaces and convergence difficulties. 

Furthermore, increasing research efforts are dedicated to building differentiable world models, aiming to enable stable and efficient system identification via gradient descent [17, 16, 18, 19, 20]. However, achieving stable end-to-end learning remains challenging. Methods like [17] utilize integrated simulators for collision detection, rendering the collision process non-differentiable. In contact-rich interactions where object trajectories are hypersensitive to the precise contact manifold, this ‘gradient detachment’ prevents the model from effectively correcting geometric errors. Consequently, the optimization landscape becomes notoriously rugged and ill-posed, making it difficult to recover precise dynamic parameters from sparse and contact-rich video sequences. While approaches such as [18, 19, 20] achieve theoretical end-to-end differentiability, they essentially rely on numerical approximation and lack analytical gradients, and hence are unsuitable for the learning and application of high-quality world models. Moreover, due to the structural decoupling of perception and dynamics, these methods are often compelled to maintain two distinct representations: one for visual rendering (3DGS [21] or Nerf [22]) and another for physical simulation (e.g., explicit meshes or particles). In practice, enforcing precise geometric alignment between these dual representations is non-trivial, causing the back-propagated gradients from visual reconstruction errors to be indirect and spatially misaligned with the underlying physical parameters. 

In this work, we introduce a novel differentiable framework called ContactGaussian-WM for learning a physics-grounded world model from a small number of interactive videos. This framework enables visually realistic and physically plausible predictions and bridges the sim-to-real gap in robot planning tasks. Specifically, we unify visual and geometric representations, where a decoupled optimization approach is used to train 3DGS [21] to initialize the scene and leads to a representation that balances visual and geometric aspects. To ensure the differentiability of collision detection, we force the 3DGS [21] to be isotropic spheres. To adapt to contact-rich scenarios, we select a lightweight yet capable contact dynamics model [23] that is effective enough to handle different contact modes (skip, separation, stick) [24, 25]. This model, combined with a 3DGS differentiable renderer, is used to construct ContactGaussianWM, enabling differentiable learning, prediction, and planning control of the world model. 

Extensive experiments, in both simulated and real-world environments, demonstrate that our proposed framework is 

capable of learning a physics-grounded world model from sparse observations in complex contact-rich scenarios. The resulting model facilitates long-horizon, accurate, and physically consistent predictions, effectively bridging the sim-to-real gap. Furthermore, we showcase its capability for real-time planning when integrated with Model Predictive Control (MPC). Our main contributions are summarized as follows: 

- We propose ContactGaussian-WM, an end-to-end differentiable framework with a unified geometric and visual representation of the world, to achieve efficient learning of world models from sparse videos in contact-rich scenarios; and 

- We conduct extensive simulation and real-world experiments, validating our method’s generalizability across diverse complex interaction scenarios and demonstrating that it outperforms existing methods[17, 7]. 

## II. RELATED WORKS 

## _A. World model_ 

_1) Data-driven world model:_ Recent generative AI has revitalized pixel-based approaches, where foundation models like [26, 2, 3, 27, 4, 5] serve as generalist video simulators. To improve control efficiency, latent-state-based methods [28, 6, 7, 8, 9, 10] compress observations into compact states. However, both paradigms treat dynamics as black-box transitions of probability distributions. Lacking explicit physical constraints, they suffer from physical hallucinations, e.g., object morphing or vanishing, since they essentially mimic data statistics rather than enforcing causal physical laws. 

_2) Physics-grounded world models:_ To improve physical plausibility, some works incorporate structural priors using graph neural networks on particle representations [29, 30]. While these offer better generalization, they remain ”blackbox” and lack strict guarantees for non-penetration or friction. Alternatively, some methods integrate explicit physics engines with renderers [13, 14], but rely on gradient-free optimization which scales poorly with search space. 

Consequently, recent research explores differentiable world models. PIN-WM [17] achieves local differentiability via implicit differentiation of an LCP solver, while others [18, 19, 20] use numerical approximations. However, these often suffer from gradient discontinuities at contact boundaries and visibility changes, leading to unstable training. Furthermore, non-differentiable collision detection in models like PIN-WM prevents geometry optimization, making them unsuitable for contact-rich scenarios where geometric errors cannot be corrected. In contrast, ContactGaussian-WM achieves true end-toend differentiability, enabling the simultaneous optimization of physical parameters and collision geometry. 

## _B. Rigid Body Dynamics Simulation_ 

_1) Collision detection:_ Mainstream physics engines (e.g., Bullet, MuJoCo, DART, and Drake) predominantly rely on mesh-based discrete representations and algorithms like GJK [31] and EPA [32] to compute separation distances. 

III. METHODS 

While precise for forward simulation, these methods are nondifferentiable and ill-suited for gradient-based optimization. 

To address this, recent frameworks have shifted toward continuous geometric representations. Methods like gradSim [20], D-REX [19], and ContactSDF [33] utilize volumetric fields (SDFs or density grids) to support gradient propagation through field penetration. Similarly, recent work [18] employs 3DGS [21] to model geometry for physical interactions. However, these methods often rely on spatial and temporal discretization and approximation during contact resolution. These numerical approximations introduce gradient discontinuities or inaccuracy that limit detection accuracy and fall short of the fidelity provided by exact analytical solutions. 

_2) Contact Models:_ Traditional rigid-body contact models are often formulated as Nonlinear Complementarity Problems (NCP) [34, 35, 36], which is computationally inefficient for high dimensions. One common approach to simplify its computation is to approximate Coulomb friction cones by polyhedral cones [36, 11], allowing the formulation to be transformed into Linear Complementarity Problems (LCP) solvable by efficient solvers. Another approach is to relax the NCP formulation [37] by constraining the contact velocity within a dual friction cone, transforming the problem into Convex Complementarity Problems (CCP). This practice offers significant computational benefits, such as fast convergence and theoretical solution guarantees [38, 39]. Furthermore, the aforementioned CCP can be formulated as the Karush-KuhnTucker (KKT) optimality conditions for a second-order coneconstrained convex optimization problem [37, 40, 41, 11]. To endow the learnability for the model, several approaches [42, 43, 44, 45, 46] have proposed differentiable approximations as alternatives to complementarity-based models. These methods achieve differentiability through various operations, such as introducing penalty functions [42, 45, 46], relaxing complementarity constraints [43], or employing implicit complementarity formulations [44]. A shared feature of these methods is that they ultimately require iteratively solving a residual equation for contact constraint resolution, with differentiability typically being obtained via the Implicit Function Theorem [47]. Consequently, some researchers in [48, 49, 45, 46, 23] have explored closed-form contact dynamics models. While some works [48, 49, 45, 46] seek a closed-form solution by decoupling contact normal forces from Coulomb friction, this often introduces additional hyperparameters and potential nonphysical artifacts. In contrast, the approach in [23] utilizes an approximation within the dual friction cone. This allows for a unified treatment of contact normal and frictional forces within a single term, ensuring flexible capture of different contact modes and automatic satisfaction of Coulomb’s friction law. 

In this work, our rigid body simulator implements differentiable collision detection and integrates a closed-form contact model [23], creating a more efficient differentiable simulation and providing stable analytical gradients. 

## _A. Overview of our framework_ 

Figure 2 outlines the ContactGaussian-WM framework, which mainly comprises two stages: scene initialization and phys-geo refinement. Scene initialization uses decoupled optimization to obtain a unified spherical Gaussian representation, balancing visual and geometric aspects. Phys-geo refinement is achieved through the ContactGaussian-WM world model, which mainly consists of a differentiable collision detector, an explicit contact dynamics model, and a 3DGS renderer. All those components are discussed in detail as follows. 

## _B. Problem formulation_ 

Given an RGB video of a contact-rich scene, our goal is to build a world model that predicts the future images of the scene and captures the underlying physical laws. Denote the image of the scene at time step _t_ as **I** _t_ . Our goal is to minimize the difference between the image<sup>ˆ</sup> **I** _t_ predicted by our world model and the actual image **I** _t_ . In our ContactGaussian-WM, we represent the contact-rich scene by Gaussians, denoted _G_ := _{G_ geo _, G_ vis _}_ = _{{_ **c** _, s}, {α, f }}_ , where _G_ geo (resp. _G_ vis) encodes the geometry (resp. appearance) of all objects in the scene with the spatial center and the isotropic scale (opacity _α_ and color features _f_ ) of the Gaussian primitives. ContactGaussian-WM predicts future images of the scene by transforming the Gaussian _G_ by the physical state **x** ˆ _t_ , and rendering them. We denote this process using a function R. The evolution of the physical state **x** ˆ _t_ over time is realized using our differentiable simulator (Section III-D). Therefore, the optimization problem is formulated as: 


where **f** is our differentiable simulator with control input **a** _t_ and being parameterized by physical properties **_θ_** (detailed later) and Gaussian geometry attributes _G_ geo. This cost function is designed as _L_ = _L_ Loft + _L_ L1, which includes Loft feature loss [50] and L1 loss to help us better capture differences at both the feature and pixel levels. 

Jointly learning Gaussian parameters _G_ and physical parameters **_θ_** from a single video segment by Eq.(1) is very challenging due to the high nonlinearity and ambiguity. To address this, we divide the entire learning framework into two stages. The first stage focuses on optimizing the Gaussians _G_ , while the second stage is to optimize the physical parameters **_θ_** , and simultaneously fine-tunes the geometry attributes _G_ geo. 

## _C. Stage I: Scene Initialization with Sphere Geometry Gaussian Splatting (SG-GS)_ 

We first obtain multi-view observations _{_ **I** _i}_ of the scene from single or multiple calibrated cameras. Based on that, we use SAM2 [51] to extract geometry features **G** _i_ . Then, we propose an **SG-GS** method to obtain a Gaussian representation of the scene from the observation, which has two key designs: 


Fig. 2: Overview of ContactGaussian-WM. We first initialize a scene with a unified spherical Gaussian representation, then jointly refine physics and geometry: given the current physical state and action, the differentiable collision detector uses Gaussian geometry to compute contact points, which are fed into the complementarity-free contact dynamics model to compute the next physical state, and the 3DGS renderer generates the next image. The pipeline is fully differentiable for end-to-end learning. 

**Isotropic spherical primitives.** Unlike traditional 3DGS [21], we enforce isotropic scaling and frozen rotation updates of Gaussians to ensure that each Gaussian maintains a spherical shape, which helps us achieve closed-form differentiable collision detection in Stage II. 

**Decoupled optimization.** To reconcile the conflict between high-frequency visual details and stable physical geometry, we adopt a **decoupled optimization** strategy. First, we focus exclusively on learning the geometric attributes _G_ geo while keep the visual appearance attributes _G_ vis frozen. This compels the primitives to strictly align with the geometrical structure of the object rather than compensating for photometric errors. Consequently, the optimization minimizes the reconstruction error between the rendered and observed geometric maps: 


where **G** ˆ _i_ and **G** _i_ denote the rendered and ground-truth geometric feature maps, respectively. 

Second, we refine the visual fidelity by optimizing the visual appearance attributes _G_ vis, while freezing the geometric attributes _G_ geo to preserve the collision proxies. Following the standard 3DGS protocol [21], the objective combines L1 and D-SSIM losss [52]: 


where _λ_ is a weighting factor, and<sup>ˆ</sup> **I** _i_ is the rendered image. 

These modifications yield a unified SG-GS representation that ensures both visual accuracy and geometric robustness. By differentiably extracting Gaussian geometry parameters _G_ geo as explicit collision geometries, we transform Gaussians from mere rendering kernels into active participants in physical simulation. This ensures strict alignment between the visual appearance and the physical model, realizing a “what you see is what you get” framework. 

## _D. Stage II: Phys-Geo Refinement_ 

With the optimized Gaussian _G_<sup>_∗_</sup> , we next optimize the physical parameters **_θ_** and fine-tune geometric attributes _G_ geo, based on the gradient flow from visual observations. To fully represent the dynamics in Eq.(1) by a 3D rigid-body simulation system, we define the environment state as **x** _t_ = _{_ **q** _t,_ **v** _t}_ , representing the system’s generalized coordinates and velocity of all objects at time _t_ . Furthermore, the physical properties that govern the state transitions are incorporated into the system learnable physical parameters **_θ_** = ( **M** , _µ_ , **K** , **D** ), where **M** , _µ_ , **K** , **D** denotes the mass-inertia matrix, friction coefficient, stiffness, and damping coefficient, respectively. In this work, We jointly optimize its intrinsic physical properties and geometrical attributes by back-propagating through the following three core processes: a differentiable collision detection based on spherical Gaussians, an explicit contact dynamics model, and a differentiable 3DGS rendering. 

_1) Differentiable collision detection.:_ Leveraging the current predicted states **x** ˆ _t_ and initialized geometric attributes _G_ geo<sup>_∗_whichrepresentthecollisiongeometryasaunionof</sup><sup>_n_</sup> spherical primitives. For each primitive _i ∈{_ 1 _, . . . , n}_ , its center **c** _i_ is derived from the Gaussian’s position, and its radius is defined as _ri_ = 2 _s_ (twice the scale radius is a reasonably conservative value). At this point, we can use a simple formula to represent the shortest distance from the query point **p** to the Gaussian collision geometry: 


To ensure differentiability, we first approximate the shortest distances using the LogSumExp (LSE) smoothed minimum: 


where _β_ is the smoothing factor. However, applying the above formula to calculate the distance inside an object often reflects the proximity to the nearest individual sphere rather than 

the object’s actual surface, leading to inaccurate penetration estimates. To address this, a significant negative penalty is assigned to ensure a robust correction of inter-penetration when the distance is negative. To preserve differentiability for end-to-end learning, we design a smoothing transition with the Sigmoid function _σ_ ( _·_ ): 


where _γ_ controls how sharp _σ_ is, and _δ_ is the positive constant penalty used for negative distances inside-object cases. Using the calculated distance _ϕ_ ( **p** ), the nearest surface point **p** c is obtained via gradient-based projection: 


with the normalized gradient _∇_ **p** _ϕ_ ( **p** ) being the surface normal. Based on this collision information, the contact Jacobian can be computed based on rigid body kinematics [53]. 

_2) Differentiable complementarity-free contact dynamics.:_ We adopt the full-dynamic complementarity-free contact model [23] for contact-rich scenarios, which is given by: 


Here, **M** represents the generalized mass matrix of the rigid body. The force vector **_τ_** ( **q** _t,_ **v** _t,_ **a** _t_ ) is the sum of non-contact forces in the system, including actuation force, gravity, and Coriolis forces. **_ϕ_**<sup>˜</sup> _t_ is the signed collision distance of each collision pair. **J**<sup>˜</sup> _t_ ( _µ_ ) is the Jacobian of the faces of the polyhedral dual cone (of the friction cones) at each collision pair. These are computed from the raw collision information ( **J** _t_ , **_ϕ_** _t_ ) and frictional coefficient _µ_ (See Appendix for detailed form). Instead of iteratively solving the contact constraint, the complementarity-free contact model approximates the contact force _λ_ based on an impedance mechanism defined on the dual cones, with **K** and **D** representing the learnable stiffness and damping coefficients. This leads to a closed-form solution for the contact forces **_λ_** _t_ on the dual cones of the Coulomb friction cones. Moreover, different contact modes, e.g., sticking, sliding, and separation, can be captured by different penetration regimes across facets of the dual cones, and Coulomb friction laws are automatically satisfied. With the computed **v** _t_ +1, the system’s next generalized position **q** _t_ +1 can be obtained by **q** _t_ +1= **q** _t⊕h_ **v** _t_ +1, where _⊕_ stands for the integration of system pose (position, orientation) with velocities. 

_3) 3DGS rendering:_ Up to now, we have a differentiable simulator **f** , which helped us successfully construct the state transition function in Eq.(1). Using the current predicted state **x** ˆ _t_ and action **a** _t_ , we can explicitly obtain the next predicted state **x** ˆ _t_ +1, thus creating the computational graph at the state space. In order to perform optimization in the image space, we need to map the system states to that space. This can be done 

by transforming all Gaussians based on forward kinematics with the updated state **x** ˆ _t_ +1, which can be written as 


where FK is the forward kinematics transformation that applies a rigid body transformation to the properties of all Gaussians in the scene based on the current state **q** ˆ, obtaining the Gaussians in the current predicted state. Then, based on the camera pose **T** _cw_ and the 3DGS renderer, we implement the mapping from the state to the image by 


_4) End-to-End Gradient Flow:_ At this point, we have presented all of the components in our ContactGaussian-WM framework. This design allows for the end-to-end optimization of Eq. (1). Gradients from the image loss are backpropagated through the renderer R to the state, and subsequently propagated through the differentiable simulator **f** to optimize the physical parameters **_θ_** and geometric parameters _G_ geo, which are collectively denoted as Θ. 

Mathematically, the gradient flow representing the backpropagation process through time can be written as follows: 


where dˆdΘ **x**<sup>(</sup> _<u>t</u>_<sup>_i_)</sup> is recursively computed via the differentiable simulator **f** : 


Simultaneously optimizing the physical process and visually aligned images presents significant ambiguity, and images in motion are too blurry to adequately optimize our initial Gaussian; thus, as the formulation explicitly describes, the image loss does not update the geometry parameters in Gaussians directly through the rendering layer. Instead, these parameters are fine-tuned exclusively through the physical collision interactions propagated from the differentiable simulator. 

## IV. RESULTS 

We evaluate our proposed framework in both simulation and real-world scenarios. We aim to answer the following questions: 

- 1) Can the proposed framework learn the underlying physical laws through sparse and contact-rich scene videos for more accurate predictions than existing methods? 

- 2) Can the method generalize to diverse real-world scenarios and support effective sim-to-real control transfer? 

- 3) What is the utility of the proposed framework in downstream tasks? 

We leverage simulation to strictly benchmark the prediction accuracy of our approach. Extending to the real world, we validate the model’s generalization capability and sim-to-real control transfer across diverse real-world scenarios. Finally, 

to demonstrate the practical utility, we explore the potential of the proposed framework in supporting diverse downstream robotic applications. Detailed setup and results can be found in the Appendix. 

## _A. Evaluations in simulation_ 

**Experimental Setup:** We initialized the experiment by converting the object’s precise mesh into a 3DGS representation using our SG-GS method. Two interaction scenarios: 

- Push-slide-settle: various objects pushed by a virtual hand with images, ground-truth trajectory, and endeffector velocity being recorded. 

- Fall-and-rebound: the complete free-fall and rebound process of various objects with images and ground-truth trajectories being recorded. 

are designed within MuJoCo [11] to generate trajectories along with their RGB renderings. These two scenarios represent two distinct modes of motion: the former involves quasi-dynamic, continuous contact, while the latter features high-dynamic, discrete contact. To verify the framework’s generalization across various geometries and physical properties, we employ a diverse set of objects (e.g., Camera, Stanford Bunny, Piggy Bank, and Rubber Duck). The model is trained on a short interaction trajectory and evaluated across multiple unseen test sets. Specifically, for the falling scenario, the objects are released from various initial poses and positions; for the pushing scenario, the manipulator operates at different endeffector velocities. To assess long-horizon prediction stability, the test sequences are notably longer than those used during training, while maintaining a consistent sampling rate. 

**Experimental metrics:** Our evaluation focuses on the model’s learning capability and predictive accuracy in an openloop manner (i.e., only the true state of the first frame is provided). To assess learning performance, we track the **PSNR** of the rendered images during the training to monitor the model’s ability to fit training data. Furthermore, we quantify predictive accuracy by averaging the translation and rotation errors between the ground-truth and predicted poses across the entire test set. 

**Baseline methods:** We compare our proposed world model against various existing baselines, categorized as follows: 

_Data-driven world models._ We select DreamerV3 [7] as a representative baseline for this category. As a general-purpose world model, DreamerV3 learns latent dynamics purely from visual observations but typically requires substantial data to converge. We train it using a dataset of 100 trajectories that are distinct from the test set, at the same time, we also follow its closed-loop training mode (conditioning on ground-truth states at every time step). 

_Physics-informed world models._ We select two representative approaches to cover the spectrum of physics-grounded optimization. The first is essentially a gradient-free system identification baseline. We integrate the standard MuJoCo simulator with our 3DGS renderer R and employ the gradient-free optimization strategy CEM from TwinTrack [54] to minimize L1 image error, which we call it CEM+MuJoCo+R in the 

sequel. The second approach is PIN-WM [17], representing differentiable physics-based methods, which constructs a physical-grounded world model with Linear Complementarity Problems (LCP) and utilizes implicit differentiation for efficient gradient-based optimization. 

Notably, we provide realistic meshes as collision geometry for CEM+MuJoCo+R and PIN-WM, and utilize a high-fidelity physics simulator for accurate collision detection. We also trained high-quality 2DGS objects for PIN-WM to prevent rendering artifacts from becoming a performance bottleneck. For a fair comparison, we used the official implementations with default hyperparameters for PIN-WM and DreamerV3. For CEM+MuJoCo+R, we implemented 100 sets of parallel parameters using MJX [11], with the rest of the settings remaining the same as TwinTrack. All physics-grounded baselines are trained and evaluated on the same trajectory dataset as our proposed model, with each method trained until convergence to report its optimal performance. 

**Comparisons on training performance:** Fig. 3 presents the learning performance curves. It can be observed that all four models converge in both scenarios. As DreamerV3 employs a closed-form training paradigm, it is reasonable that its PSNR significantly outperforms the other models. However, its convergence in the Fall-and-rebound scenario is slightly lower than in the Push-slide-settle scenario due to the higher visual complexity of the former, despite its lack of explicit consideration of contact dynamics. 

For the three physics-based models, learning performance is comparable in the Push-slide-settle scenario. The reason is that this quasi-dynamic task provides smooth and continuous gradients, and the motion trajectories are predominantly governed by the friction coefficient. Such a constrained search space and stable constraints allow both the gradient-free CEM+MuJoCo+R and the gradient-based methods (PIN-WM and ours) to easily locate the optimal solutions. 

In contrast, the Fall-and-rebound scenario presents a greater challenge. Collisions occur only within a few frames, providing limited useful information. Furthermore, discrete contacts lead to gradient discontinuities. PIN-WM, which already struggles with discrete and inaccurate gradients, fails to reach a satisfactory convergence under these conditions. For CEM+MuJoCo+R, the parallel search allows them to fit the image loss very well. In comparison, our model achieves a more stable and accurate gradient flow. By effectively utilizing sparse and discontinuous collision information, our framework can identify precise gradient directions with less computational resources, ultimately converging to a better value. 

**Comparisons on test performance:** To evaluate the predictive accuracy of the four models, we record the cumulative translation and orientation errors on the test set (Tables I and II), with qualitative results being presented in the Appendix. Based on the performance, we draw the following conclusions: 

1) The purely data-driven DreamerV3 suffers from a catastrophic decline in performance when generalizing to novel states and actions, failing to maintain essential scene consistency or physical plausibility during long-horizon forecasting. 


Fig. 3: PSNR curves during training for Fall-and-rebound (left) and Push-slide-settle (right). DreamerV3 reports closed-loop one-step prediction, while the other methods report open-loop cumulative error. 

2) Although CEM+MuJoCo+R performs well in both Pushslide-settle and Fall-and-rebound scenarios, its generalization performance drops significantly in highly dynamic and discontinuous fall scenarios, indicating that the model is unable to capture the underlying physical laws in these scenarios when the scene changes greatly, and instead overfits the training loss. 

3) Frameworks like PIN-WM, which rely on implicit function differentiation and non-differentiable collision detection, are ill-suited for high-dynamic scenarios. The inherent inaccuracy and lack of smoothness in their gradient estimation make it difficult to derive reliable update directions from sparse and highly dynamic signals. Consequently, such methods may function in quasi-dynamic scenarios with continuous contacts (e.g., pushing). 

4) In contrast, our proposed ContactGaussian-WM framework enables end-to-end differentiable learning. This allows the model to accurately capture underlying physical laws from images, even under challenging conditions such as inaccurate geometry, imperfect dynamics, sparse contact information, and complex collision interactions. Consequently, our framework achieves stable generalization performance. Furthermore, it also performs well in promoting learning and generalization in various scenarios, which further demonstrates the robustness and universality of our learning paradigm. 

## _B. Evaluations in real world_ 

While the quantitative and qualitative performance of our model against various baselines has been established in simulation, in this part, we shift our focus towards validating practical feasibility in complex, diverse environments and the effectiveness of sim-to-real transferability. 

**Experimental Setup:** We design two dynamic scenarios: free-fall and robotic manipulation. In the latter, we use the LEAP Hand [55] which exerts high-impact forces to induce complex behaviors like sliding and flipping, as seen in Fig. 4. Following [41], we model the hand as a spring system under impedance control [56] to simplify contact dynamics. Additionally, we vary ground materials (rubber, PVC, and wood) to test robustness against diverse physical properties (e.g., stiffness, friction). We initialize 3DGS representations using SG-GS from multi-view images captured by hand phone. We 


Fig. 4: Our real-world experiment setup 

capture motion videos for each trial using a RealSense D456 RGBD camera, splitting them into training and test sets (1:4 ratio). Unlike methods relying on external state tracking, we treat the initial state as a learnable parameter. To decouple it from geometry and physics optimization, we pre-estimate the initial state using the first few frames. Finally, we implement an open-loop sim-to-real transfer strategy, executing trajectories which are planned based on the model on the LEAP hand to validate whether it supports valid control transfer. 

**Experimental metrics:** Due to the lack of reliable realworld state information, we use the cumulative peak signal-tonoise ratio (PSNR) of long-horizon predictions as the primary metric. The high visual fidelity of long-horizon open-loop predictions strongly indicates that the model has correctly captured the underlying physical laws and achieved accurate dynamic predictions. For prediction experiments on the test set, we calculate the average cumulative PSNR of openloop predictions. For each scene, we conduct multiple experiments with different materials and then calculate the average. Similarly, for open-loop trajectory transfer experiments, we conduct multiple experiments with different materials for each object and calculate the average PSNR between the actual and planned images. 

**Baseline method:** To highlight the impact of parameter learning on model prediction and sim-to-real transfer, we compare it with ContactGaussian-WM without parameter learning, while keeping all other variables constant. 

**Results:** In Tables III and IV, we report the performance of the two methods on the test set and in actual open-loop trajectory transfer, respectively. Fig. 5 visualizes the actual performance of the two methods in the open-loop controlled trajectory transfer experiment. It can be found that our world model parameter learning improves the prediction fidelity of the world model while narrowing the sim-to-real gap. 

TABLE I: Test results of the Fall-and-rebound scenario. In the Fall-and-rebound scenario, our method consistently outperforms the baseline across all metrics and objects. 

|Object||Ours|PI|N-WM|CEM+M|uJoCo+R|Dre|amerV3|
|---|---|---|---|---|---|---|---|---|
||Trans. [m] _↓_|Orient. [rad] _↓_|Trans. [m] _↓_|Orient. [rad] _↓_|Trans. [m] _↓_|Orient. [rad] _↓_|Trans. [m] _↓_|Orient. [rad] _↓_|
|Camera|**0.0116**|**0.0665**|0.0151|0.305|0.041|0.197|0.101|1.489|
|Stanford Bunny|**0.0048**|**0.0114**|0.0351|0.340|0.0343|0.0984|0.0693|1.91|
|Piggy Bank|**0.0139**|**0.0522**|0.0167|0.186|0.0515|0.164|0.056|1.53|
|Binoculars|**0.0141**|**0.0934**|0.0199|0.347|0.0374|0.464|0.112|2.29|
|Rubber Duck|**0.0498**|**0.0771**|0.107|0.122|0.104|0.147|0.123|1.85|


TABLE II: Test results of the Push-slide-settle scenario. In this scenario, our method achieves comparable results to baselines. 

|Object||Ours|PI|N-WM|CEM+|MuJoCo+R|Dre|amerV3|
|---|---|---|---|---|---|---|---|---|
||Trans. [m] _↓_|Orient. [rad] _↓_|Trans. [m] _↓_|Orient. [rad] _↓_|Trans. [m] _↓_|Orient. [rad] _↓_|Trans. [m] _↓_|Orient. [rad] _↓_|
|Camera|0.0043|**0.0114**|**0.0027**|0.0260|0.0168|0.0839|0.0790|0.332|
|Stanford Bunny|0.0044|0.0196|**0.0041**|**0.0127**|0.0059|0.0032|0.1085|0.0523|
|Piggy Bank|0.0074|0.0394|**0.0037**|0.0225|0.0058|**0.0189**|0.111|0.0825|
|Binoculars|**0.0055**|**0.02**|0.0061|0.0225|0.0059|0.2300|0.0901|0.324|
|Rubber Duck|0.0218|0.0367|0.0164|0.0730|**0.0128**|**0.0136**|0.0898|0.0354|


Fig. 5: Visualization of long-horizon predictions in real-world experiments. Our method (right) outperforms the one without optimization (middle), as compared with the ground-truth observation (left). 

TABLE III: Long-horizon prediction results from real-world experiments. Values represent PSNR [dB]. 

|Methods|Cube<br>fall|Cube<br>LeapHand|Cup<br>fall|Cup<br>LeapHand|
|---|---|---|---|---|
|Ours|**27.144**|**27.180**|**20.90**|**19.41**|
|No<br>opt|25.01|25.35|18.19|17.046|


## _C. Applications_ 

**Simulation data synthesis:** A pivotal application of world models lies in simulation data synthesis. Extensive evaluations across both simulated and real-world settings have demonstrated our model’s robust capability in understanding complex physical interactions and forecasting dynamics, particularly in contact-rich dynamic and high-dynamic scenarios. Consequently, the trained ContactGaussian-WM serves as a powerful engine for generating physically accurate and visually plausible simulation data, enabling the construction of high-fidelity 4D environments. Furthermore, our framework achieves an image generation rate of approximately 40Hz on an RTX 4090. This computational efficiency highlights the potential for realtime sim-to-real interaction. 

**Real-time MPC control:** The differentiability and explicit 

TABLE IV: Open-Loop trajectory transfer results from realworld experiments. Values represent PSNR [dB]. 


Fig. 6: Time-series visualization of applying MPC on the LEAP Hand to reorient the rubber duck in MuJoCo. 

nature of the ContactGaussian-WM framework enable seamless integration with existing MPC solvers. In this experiment, we first train a world model based on target objects using MuJoCo synthetic interactive data, and then implement a realtime MPC framework. As shown in the Fig. 6, our framework enables LEAP Hand to successfully perform in-hand redirection tasks in MuJoCo, accurately planning and executing the control sequences required to manipulate objects. 

## V. CONCLUSION AND FUTURE WORKS 

We have proposed ContactGaussian-WM, an end-to-end differentiable framework for reconstructing world models from sparse videos. Compared to other methods, our world model is better suited for learning from highly dynamic, contact-rich videos, and we have demonstrated the effectiveness of our framework in a variety of scenarios. Furthermore, we have showcased its use for simulation data synthesis and integration with real-time MPC. 

REFERENCES 

**Limitation and future work:** We identified several promising directions for future work. First, the proposed unified scene representation can, to some extent, reduce rendering quality. Second, Gaussian-sphere-based collision detection may fail to provide accurate penetration distances and contact normals under deep interpenetration. Finally, our current framework is limited to rigid-body systems and does not include deformable objects. Future work will explore more visually faithful and geometrically accurate unified representations, more accurate differentiable collision detection, and more general world models that extend beyond rigid bodies. 

- [1] D. Ha and J. Schmidhuber, “World models,” 2018. [Online]. Available: https://zenodo.org/record/1207631 

- [2] T. Brooks, B. Peebles, C. Holmes, W. DePue, Y. Guo, L. Jing, D. Schnurr, J. Taylor, T. Luhman, E. Luhman _et al._ , “Video generation models as world simulators,” _OpenAI Blog_ , vol. 1, no. 8, p. 1, 2024. 

- [3] A. Hu, L. Russell, H. Yeo, Z. Murez, G. Fedoseev, A. Kendall, J. Shotton, and G. Corrado, “Gaia-1: A generative world model for autonomous driving,” _arXiv preprint arXiv:2309.17080_ , 2023. 

- [4] O. Bar-Tal, H. Chefer, O. Tov, C. Herrmann, R. Paiss, S. Zada, A. Ephrat, J. Hur, G. Liu, A. Raj _et al._ , “Lumiere: A space-time diffusion model for video generation,” in _SIGGRAPH Asia 2024 Conference Papers_ , 2024, pp. 1–11. 

- [5] Y. Wang, J. He, L. Fan, H. Li, Y. Chen, and Z. Zhang, “Driving into the future: Multiview visual forecasting and planning with world model for autonomous driving,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 14 749–14 759. 

- [6] D. Ha and J. Schmidhuber, “World models,” _arXiv preprint arXiv:1803.10122_ , vol. 2, no. 3, 2018. 

- [7] D. Hafner, J. Pasukonis, J. Ba, and T. Lillicrap, “Mastering diverse domains through world models,” 2024. [Online]. Available: https://arxiv.org/abs/2301. 04104 

- [8] P. Wu, A. Escontrela, D. Hafner, P. Abbeel, and K. Goldberg, “Daydreamer: World models for physical robot learning,” in _Conference on robot learning_ . PMLR, 2023, pp. 2226–2240. 

- [9] A. Bardes, Q. Garrido, J. Ponce, X. Chen, M. Rabbat, Y. LeCun, M. Assran, and N. Ballas, “Revisiting feature prediction for learning visual representations from video,” _arXiv preprint arXiv:2404.08471_ , 2024. 

- [10] N. Hansen, H. Su, and X. Wang, “Td-mpc2: Scalable, robust world models for continuous control,” _arXiv preprint arXiv:2310.16828_ , 2023. 

- [11] E. Todorov, T. Erez, and Y. Tassa, “Mujoco: A physics engine for model-based control,” in _2012 IEEE/RSJ International Conference on Intelligent Robots and Systems_ . IEEE, 2012, pp. 5026–5033. 

- [12] E. Coumans and Y. Bai, “Pybullet, a python module for physics simulation for games, robotics and machine learning,” 2016. 

- [13] W. Yang, Z. Xie, X. Zhang, H. B. Amor, S. Lin, and W. Jin, “Twintrack: Bridging vision and contact physics for real-time tracking of unknown dynamic objects,” _arXiv preprint arXiv:2505.22882_ , 2025. 

- [14] F. Ramos, R. C. Possas, and D. Fox, “Bayessim: adaptive domain randomization via probabilistic inference for robotics simulators,” _arXiv preprint arXiv:1906.01728_ , 2019. 

- [15] M. Memmel, A. Wagenmaker, C. Zhu, P. Yin, D. Fox, and A. Gupta, “Asid: Active exploration for system 

identification in robotic manipulation,” _arXiv preprint arXiv:2404.12308_ , 2024. 

- [16] H. Fan, H. Dai, J. Zhang, J. Li, Q. Yan, Y. Zhao, M. Gao, J. Wu, H. Tang, and H. Dong, “Twinaligner: Visual-dynamic alignment empowers physics-aware real2sim2real for robotic manipulation,” 2025. [Online]. Available: https://arxiv.org/abs/2512.19390 

- [17] W. Li, H. Zhao, Z. Yu, Y. Du, Q. Zou, R. Hu, and K. Xu, “Pin-wm: Learning physics-informed world models for non-prehensile manipulation,” 2025. [Online]. Available: https://arxiv.org/abs/2504.16693 

- [18] B. Moran, M. Comi, A. Byravan, S. Bohez, T. Erez, Z. Li, and L. Hasenclever, “Splatting physical scenes: End-to-end real-to-sim from imperfect robot data,” 2025. [Online]. Available: https://arxiv.org/abs/2506.04120 

- [19] Anonymous, “D-REX: Differentiable real-to-sim-to-real engine for learning dexterous grasping,” in _Submitted to The Fourteenth International Conference on Learning Representations_ , 2025, under review. [Online]. Available: https://openreview.net/forum?id=13jshGCK9i 

- [20] K. M. Jatavallabhula, M. Macklin, F. Golemo, V. Voleti, L. Petrini, M. Weiss, B. Considine, J. Parent-L´evesque, K. Xie, K. Erleben _et al._ , “gradsim: Differentiable simulation for system identification and visuomotor control,” _arXiv preprint arXiv:2104.02646_ , 2021. 

- [21] B. Kerbl, G. Kopanas, T. Leimk¨uhler, and G. Drettakis, “3d gaussian splatting for real-time radiance field rendering.” _ACM Trans. Graph._ , vol. 42, no. 4, pp. 139–1, 2023. 

- [22] B. Mildenhall, P. P. Srinivasan, M. Tancik, J. T. Barron, R. Ramamoorthi, and R. Ng, “Nerf: Representing scenes as neural radiance fields for view synthesis,” _Communications of the ACM_ , vol. 65, no. 1, pp. 99–106, 2021. 

- [23] W. Jin, “Complementarity-free multi-contact modeling and optimization for dexterous manipulation,” in _Proceedings of Robotics: Science and Systems_ , Los Angeles, California, June 2025. 

- [24] Z. Xie, W. Yang, and W. Jin, “On-palm dexterity: Dynamic reorientation of objects via emergent flipping and sliding,” in _IEEE International Conference on Robotics and Automation on Workshop on Learning Meets ModelBased Methods for Contact-Rich Manipulation_ , 2025. 

- [25] Z. Xie, Y. Xiang, M. Posa, and W. Jin, “Where to touch, how to contact: Hierarchical rl-mpc framework for geometry-aware long-horizon dexterous manipulation,” 2026. 

- [26] J. Bruce, M. D. Dennis, A. Edwards, J. Parker-Holder, Y. Shi, E. Hughes, M. Lai, A. Mavalankar, R. Steigerwald, C. Apps _et al._ , “Genie: Generative interactive environments,” in _Forty-first International Conference on Machine Learning_ , 2024. 

- [27] Z. Yang, Y. Chen, J. Wang, S. Manivasagam, W.-C. Ma, A. J. Yang, and R. Urtasun, “Unisim: A neural closedloop sensor simulator,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2023, pp. 1389–1399. 

- [28] D. Hafner, T. Lillicrap, I. Fischer, R. Villegas, D. Ha, H. Lee, and J. Davidson, “Learning latent dynamics for planning from pixels,” in _International conference on machine learning_ . PMLR, 2019, pp. 2555–2565. 

- [29] Y. Li, J. Wu, R. Tedrake, J. B. Tenenbaum, and A. Torralba, “Learning particle dynamics for manipulating rigid bodies, deformable objects, and fluids,” _arXiv preprint arXiv:1810.01566_ , 2018. 

- [30] Z. Wu, C. Gan, J. Wu, J. B. Tenenbaum, and W. T. Freeman, “Slotformer: Unsupervised visual dynamics simulation with object-centric models,” in _ICLR_ , 2023. 

- [31] E. G. Gilbert, D. W. Johnson, and S. S. Keerthi, “A fast procedure for computing the distance between complex objects in three-dimensional space,” _IEEE Journal on Robotics and Automation_ , vol. 4, no. 2, pp. 193–203, 2002. 

- [32] G. Van Den Bergen, _Collision detection in interactive 3D environments_ . CRC Press, 2003. 

- [33] W. Yang and W. Jin, “Contactsdf: Signed distance functions as multi-contact models for dexterous manipulation,” _IEEE Robotics and Automation Letters_ , 2025. 

- [34] D. E. Stewart, “Rigid-body dynamics with friction and impact,” _SIAM review_ , vol. 42, no. 1, pp. 3–39, 2000. 

- [35] D. Stewart and J. C. Trinkle, “An implicit time-stepping scheme for rigid body dynamics with coulomb friction,” in _Proceedings 2000 ICRA. Millennium Conference. IEEE International Conference on Robotics and Automation. Symposia Proceedings (Cat. No. 00CH37065)_ , vol. 1. IEEE, 2000, pp. 162–169. 

- [36] D. E. Stewart and J. C. Trinkle, “An implicit timestepping scheme for rigid body dynamics with inelastic collisions and coulomb friction,” _International Journal for Numerical Methods in Engineering_ , vol. 39, no. 15, pp. 2673–2691, 1996. 

- [37] M. Anitescu, “Optimization-based simulation of nonsmooth rigid multibody dynamics,” _Mathematical Programming_ , vol. 105, pp. 113–143, 2006. 

- [38] M. Anitescu and A. Tasora, “An iterative approach for cone complementarity problems for nonsmooth dynamics,” _Computational Optimization and Applications_ , vol. 47, pp. 207–235, 2010. 

- [39] A. Tasora and M. Anitescu, “A matrix-free cone complementarity approach for solving large-scale, nonsmooth, rigid body dynamics,” _Computer Methods in Applied Mechanics and Engineering_ , vol. 200, no. 5-8, pp. 439– 453, 2011. 

- [40] T. Pang, H. T. Suh, L. Yang, and R. Tedrake, “Global planning for contact-rich manipulation via local smoothing of quasi-dynamic contact models,” _IEEE Transactions on Robotics_ , 2023. 

- [41] T. Pang and R. Tedrake, “A convex quasistatic timestepping scheme for rigid multibody systems with contact and friction,” in _2021 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2021, pp. 6614–6620. 

- [42] M. Geilinger, D. Hahn, J. Zehnder, M. B¨acher, 

   - B. Thomaszewski, and S. Coros, “Add: Analytically differentiable dynamics for multi-body systems with frictional contact,” _ACM Transactions on Graphics (TOG)_ , vol. 39, no. 6, pp. 1–15, 2020. 

- [43] T. A. Howell, S. L. Cleac’h, J. Br¨udigam, J. Z. Kolter, M. Schwager, and Z. Manchester, “Dojo: A differentiable physics engine for robotics,” _arXiv preprint arXiv:2203.00806_ , 2022. 

- [44] E. Todorov, “Implicit nonlinear complementarity: A new approach to contact dynamics,” in _2010 IEEE international conference on robotics and automation_ . IEEE, 2010, pp. 2322–2329. 

- [45] K. Yamane and Y. Nakamura, “Stable penalty-based model of frictional contacts,” in _Proceedings 2006 IEEE International Conference on Robotics and Automation, 2006. ICRA 2006._ IEEE, 2006, pp. 1904–1909. 

- [46] X. Liu, K. Lyu, J. Zhang, T. Du, and L. Yi, “Quasisim: Parameterized quasi-physical simulators for dexterous manipulations transfer,” _arXiv preprint arXiv:2404.07988_ , 2024. 

- [47] W. Rudin _et al._ , _Principles of mathematical analysis_ . McGraw-hill New York, 1964, vol. 3. 

   - [56] N. Hogan, “Impedance control: An approach to manipulation,” in _1984 American control conference_ . IEEE, 1984, pp. 304–313. 

   - [57] J. L. Schonberger and J.-M. Frahm, “Structure-frommotion revisited,” in _Proceedings of the IEEE conference on computer vision and pattern recognition_ , 2016, pp. 4104–4113. 

   - [58] A. Laurentini, “The visual hull concept for silhouettebased image understanding,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , vol. 16, no. 2, pp. 150–162, 1994. 

   - [59] W. E. Lorensen and H. E. Cline, “Marching cubes: A high resolution 3d surface construction algorithm,” in _Seminal graphics: pioneering efforts that shaped the field_ , 1998, pp. 347–353. 

   - [60] S. Garrido-Jurado, R. Mu˜noz-Salinas, F. Madrid-Cuevas, and M. Mar´ın-Jim´enez, “Automatic generation and detection of highly reliable fiducial markers under occlusion,” _Pattern Recognition_ , vol. 47, no. 6, pp. 2280–2292, 2014. [Online]. Available: https://www.sciencedirect. com/science/article/pii/S0031320314000235 

- [48] Y. Tassa, T. Erez, and E. Todorov, “Synthesis and stabilization of complex behaviors through online trajectory optimization,” in _2012 IEEE/RSJ International Conference on Intelligent Robots and Systems_ . IEEE, 2012, pp. 4906–4913. 

- [49] I. Chatzinikolaidis, Y. You, and Z. Li, “Contact-implicit trajectory optimization using an analytically solvable contact model for locomotion on variable ground,” _IEEE Robotics and Automation Letters_ , vol. 5, no. 4, pp. 6357– 6364, 2020. 

- [50] J. Sun, Z. Shen, Y. Wang, H. Bao, and X. Zhou, “Loftr: Detector-free local feature matching with transformers,” 2021. [Online]. Available: https://arxiv.org/abs/2104. 00680 

- [51] N. Ravi, V. Gabeur, Y.-T. Hu, R. Hu, C. Ryali, T. Ma, H. Khedr, R. R¨adle, C. Rolland, L. Gustafson, E. Mintun, J. Pan, K. V. Alwala, N. Carion, C.-Y. Wu, R. Girshick, P. Doll´ar, and C. Feichtenhofer, “Sam 2: Segment anything in images and videos,” 2024. [Online]. Available: https://arxiv.org/abs/2408.00714 

- [52] A. H. Baker, A. Pinard, and D. M. Hammerling, “Dssim: a structural similarity index for floating-point data,” 2023. [Online]. Available: https://arxiv.org/abs/2202.02616 

- [53] M. W. Spong, S. Hutchinson, and M. Vidyasagar, “Robot modeling and control,” _John Wiley &amp_ , 2020. 

- [54] W. Yang, Z. Xie, X. Zhang, H. B. Amor, S. Lin, and W. Jin, “Twintrack: Bridging vision and contact physics for real-time tracking of unknown dynamic objects,” 2025. [Online]. Available: https://arxiv.org/abs/ 2505.22882 

- [55] K. Shaw, A. Agarwal, and D. Pathak, “Leap hand: Low-cost, efficient, and anthropomorphic hand for robot learning,” 2023. [Online]. Available: https://arxiv.org/ abs/2309.06440 

APPENDIX 

_A. Additional Details for Scene Initialization with Sphere Geometry Gaussian Splatting (SG-GS)_ 

For synthetic objects and the components of LEAP Hand, we use Blender to render OBJ files from 72 uniform spherical views, acquiring images, masks, camera parameters, and meshbased dense point clouds. For real-world objects, we estimate camera poses using COLMAP [57] on the multi-view images and masks. To accelerate 3DGS geometric prior optimization, we replace the standard sparse point cloud with a dense one initialized via Visual Hull [58]. Fig.7 illustrates the unified representations produced by SG-GS. 

and _nd_ tangent vectors **d** , and then stack them to form **J**<sup>˜</sup> ( _µ_ ), and stack the collision distance **_ϕ_** into **_ϕ_**<sup>˜</sup> accordingly: 


where **J**<sup>**n**</sup> _nc_<sup>denotesthecomponentofthe</sup><sup>**J**atthe</sup><sup>_nc_contact</sup> point along the normal direction,and **J**<sup>**d**</sup> _nc,_ 1<sup>denotesthecom-</sup> ponent of the **J** at the _nc_ contact point along the _nd_ tangential direction. 

## _B. Additional Details for Differentiable Collision Detection_ 

As mentioned in the main paper, we employ LogSumExp for sphere collision detection. However, this approach fails to yield accurate penetration depths. Therefore, we use a Sigmoid function to enforce a fixed distance when penetration occurs, thereby ensuring stable detection. Fig.8 illustrates the impact of this modification. 


Fig. 8: Visualization of penetration distance processing for the cup object. We visualized SDF slices computed using the hard minimum (left), the LogSumExp (middle), and the LogSumExp with penetration handling (right). 

We observe that the LogSumExp and hard-min results are almost identical. However, when penetration occurs inside the object, the LogSumExp formulation can sometimes return an incorrectly small penetration value, which can further exacerbate penetration. After adding penetration handling, the predicted penetration distance inside the object is effectively bounded, reducing severe penetrations. Since we do not need to optimize the scene itself, we further simplify the collisionchecking environment. For example, we model the ground as a plane and downsample the robotic hand with a complex structure to a smaller set of query points. These simplifications reduce both model and computational complexity, leading to more stable optimization. 

## _C. Additional Details for Differentiable Complementarity-free Contact Dynamics_ 

For the Jacobian matrix and collision distance obtained( **J** , **_ϕ_** ) from collision detection, we follow the same approach as in [23]. Specifically, we project **J** onto the normal vector **n** 

## _D. Additional Details for Simulation Experiment_ 

_1) Datasets:_ We used a fixed camera pose to record the complete motion trajectory in MuJoCo, including the initial state of the object, the camera’s intrinsic and extrinsic parameters, and the motion trajectory of the end effector. Fig.9 visualizes the simulation dataset. 

_2) Implementation Details of Baselines:_ Due to the page limit in the main paper, here we provide additional implementation details for baselines. To ensure a fair comparison, we use the same training dataset for ContactGaussian-WM, PIN-WM[17], and CEM+MuJoCo+R, consisting of 15 frames. For DreamerV3[7], we randomize the initial states from this training set to generate 100 training sequences, and extend each sequence to 25 frames. The test set used for reporting metrics is kept identical across all methods. During training, for methods that require initialization of physical parameters (ContactGaussian-WM, PIN-WM, and CEM+MuJoCo+R), we apply the same randomization range to shared physical parameters to obtain an initial parameter set; for CEM+MuJoCo+R, we sample 100 initial parameter sets within this range. In addition, we provide the exact formulas for the quantitative evaluation metrics, average translation error, average rotation error, and average PSNR, which are averaged over _N_ sequences and frames _T_ . 


_3) Supplement to Qualitative Results:_ We qualitatively demonstrate the performance of each baseline on the camera object in Fig.11. 

The performance of each method in two simulation scenarios further reflects the superior performance of our approach on Push-slide-settle tasks, while significantly outperforming other baseline methods on Fall-and-rebound tasks. 


Fig. 7: Visualization of Unified Representation. (Top) Gaussian Splats generated by SG-GS. (Bottom) Extracted OBJ meshes derived from the implicit SDF via our Soft Distance Detection and Marching Cubes [59] 


Fig. 9: Visualization of some simulated object data 

## _E. Additional Details for Real World Experiments_ 

In real-world experiments, we first estimate the camera pose in the world coordinate system using ArUco markers [60]. For experiments involving the LEAP Hand, we adopt an invertedGaussian approach: we align rendered images of key LEAP Hand parts at a specified configuration with real images to recover the LEAP Hand pose in the world frame. Then, we use position control to implement velocity-like control for the LEAP Hand. Specifically, given a target joint position, we limit 

the maximum joint velocity; once the LEAP Hand reaches this maximum speed, we record the current joint state as the initial joint configuration and start recording frames, ensuring that no contact with the object has occurred at that moment. 

Moreover, as described in the main paper, without any additional state estimation module, we use our differentiable framework to estimate the initial state and initial velocity. Concretely, we freeze all irrelevant parameters and optimize the initial pose by aligning the target object in the first frame. We then fix the optimized pose and estimate the initial velocity by aligning the first three frames (where we ensure no contact occurs). This process of initial velocity estimation is only used in the free-fall scene. As a result, our training set includes RGB images, camera parameters, initial pose, and initial velocity. For LEAP Hand experiments, it additionally contains the initial and target hand states, as well as the commanded joint motion speed. 

## _F. More Results for Real-time MPC control_ 

We perform real-time MPC control in MuJoCo on different objects to achieve palm redirection for the LEAP Hand, as shown in Fig.10. 


Fig. 10: More results of real-time MPC redirection experiment 


Fig. 11: Visualization of test results on the camera object for all methods in the simulation experiments. 

