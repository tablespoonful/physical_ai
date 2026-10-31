---
title: "PDF-HR: Pose Distance Fields for Humanoid Robots"
date: "2026-02-04"
authors: "Yi Gu; Yukang Gao; Yangchen Zhou; Xingyu Chen; Yixiao Feng; Mingle Zhao"
url: https://arxiv.org/abs/2602.04851
pdf: https://arxiv.org/pdf/2602.04851
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.04851)** / [論文ページ](https://arxiv.org/abs/2602.04851)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# PDF-HR: Pose Distance Fields for Humanoid Robots 

Yi Gu<sup>†1</sup> Yukang Gao<sup>†1</sup> Yangchen Zhou<sup>†1</sup> Xingyu Chen<sup>1</sup> Yixiao Feng<sup>1</sup> Mingle Zhao<sup>2</sup> Yunyang Mo<sup>1</sup> Zhaorui Wang<sup>1</sup> Lixin Xu<sup>1</sup> Renjing Xu<sup>1</sup> 1The Hong Kong University of Science and Technology (Guangzhou) 2University of Macau †Equal Contributions 

PDF-HR project page 

**_Abstract_ —Pose and motion priors play a crucial role in humanoid robotics. Although such priors have been widely studied in human motion recovery (HMR) domain with a range of models, their adoption for humanoid robots remains limited, largely due to the scarcity of high-quality humanoid motion data. In this work, we introduce Pose Distance Fields for Humanoid Robots (PDF-HR), a lightweight prior that represents the robot pose distribution as a continuous and differentiable manifold. Given an arbitrary pose, PDF-HR predicts its distance to a large corpus of retargeted robot poses, yielding a smooth measure of pose plausibility that is well suited for optimization and control. PDFHR can be integrated as a reward shaping term, a regularizer, or a standalone plausibility scorer across diverse pipelines. We evaluate PDF-HR on various humanoid tasks, including singletrajectory motion tracking, general motion tracking, style-based motion mimicry, and general motion retargeting. Experiments show that this plug-and-play prior consistently and substantially strengthens strong baselines. Code and models will be released.** 

## I. INTRODUCTION 

Humanoid robots are appealing because they share humanlike kinematics and can operate in the same spaces and with the same tools designed for humans [9, 16, 22, 44]. However, generating reliable whole-body motion remains challenging. Feasible behavior must simultaneously respect joint limits, self-collision constraints, contact feasibility, and balance [32, 51], while staying smooth and consistent with the task over time. In practice, even small errors in perception, modeling, or retargeting can push a solution toward physically awkward or unstable configurations [45, 3]. A natural way to improve robustness is to incorporate pose or motion priors that encode which configurations are plausible for a given robot, and to use these priors to regularize estimation and control. 

In the human motion recovery (HMR) literature, pose and motion priors [6, 19, 33, 26, 17] have been studied extensively, supported by abundant, high-quality datasets [28] and powerful generative models. These priors help resolve ambiguity from partial observations and improve robustness to noise and occlusion. In contrast, comparatively fewer works explore similarly general and reusable priors for humanoid robots. This gap is not merely historical. Collecting large-scale, highquality humanoid robot motion data is expensive, and directly transferring priors from human bodies to robot morphologies is nontrivial due to differences in joint limits, kinematic structure, actuation capabilities, and contact dynamics. As a result, many 

robotics pipelines still rely on task-specific constraints, handtuned regularizers, or priors that are tightly coupled to a particular controller or dataset, limiting generalization across tasks [35, 36, 27]. 

This paper focuses on pose priors and proposes a simple but effective alternative. Instead of modeling the full generative distribution of humanoid motion, we learn a continuous distance-to-data function in pose space. Concretely, we introduce **P** ose **D** istance **F** ields for **H** umanoid **R** obots (PDFHR), a lightweight prior represented by an MLP that maps an arbitrary robot pose to a scalar distance to the nearest pose in a large corpus of retargeted robot poses. To obtain a well-behaved distance field, we carefully design the training distribution to cover the pose space while emphasizing highquality near-manifold samples, and we use cross-validation to select reliable positive samples. The resulting function is continuous and provides meaningful gradients both near and far from the data manifold. 

Intuitively, PDF-HR acts like a “pose plausibility scorer”: poses near the dataset manifold receive low distance, while out-of-distribution or physically awkward configurations receive higher distance. This distance-field formulation offers several practical advantages. First, it supports arbitrary query poses and provides a smooth signal even when the pose is far from the data manifold, which is valuable in early-stage optimization and when tracking difficult motions. Second, it is modular and reusable: PDF-HR can serve as an independent pose-quality objective without requiring additional data collection, and it can be applied across tasks and policies without retraining [29]. Third, the model is compact and efficient, making it easy to integrate into existing systems. 

We demonstrate the breadth of this approach across representative humanoid tasks, including single-trajectory motion tracking, general motion tracking, style-based motion mimicry, and motion retargeting. For tracking, we incorporate PDFHR as a general-purpose reward shaping term that encourages exploration and optimization within the near manifold region. Empirically, the pose reward accelerates convergence for RL tracking baselines and improves robustness on challenging motions. For retargeting, PDF-HR acts as a principled regularizer that improves motion quality. Across settings, PDFHR consistently strengthens strong baselines while remaining lightweight and easy to deploy. 

Our main contributions can be summarized as follows: 

- PDF-HR: a continuous and differentiable pose distance field for humanoid robots learned from a large corpus of retargeted robot poses. 

- Plug-and-play integration: simple mechanisms to incorporate PDF-HR as a prior across diverse humanoid applications, including motion tracking and motion retargeting. 

- Empirical validation: experiments on multiple humanoid tasks demonstrating consistent improvements in performance and robustness over strong baselines. 

## II. RELATED WORK 

**Human Motion Priors.** Data-driven human pose and motion priors are fundamental for human motion recovery [6, 25, 33, 39]. Early works mainly focused on learning explicit constraints, such as joint limits, to avoid implausible poses [1]. Subsequent approaches leveraged generative models, including Gaussian Mixture Models (GMMs) [6], Variational Autoencoders (VAEs) [11, 33], Generative Adversarial Networks (GANs) [12, 19] and diffusion models [25, 26, 50, 40] to capture the statistical distribution of natural human articulation. More recently, implicit representations like Pose-NDF [41] has been proposed to model the manifold of valid poses as the zero-level set of a learned neural distance field. However, Pose-NDF relies on Euclidean gradient descent followed by re-projection onto SO(3) during optimization, which can limit convergence speed. In contrast, NRDF [17] enforces strict geometric consistency by leveraging Riemannian gradient descent, ensuring that optimization iterates always remain on the manifold. Building upon this geometric metric, NRMF [47] extends the representation to the temporal domain, modeling distance fields over pose, velocity, and acceleration to ensure higher-order motion continuity and dynamic feasibility. In this work, we extend this paradigm of implicit manifold representation from humans to humanoids. Specifically, we learn PDF-HR to capture the valid configuration space of the robot. We demonstrate that this learned prior can significantly enhance performance in various downstream tasks. 

**Physics-based Motion Imitation.** Data-driven imitation learning has emerged as a cornerstone for acquiring humanoid skills [10, 46]. DeepMimic [35] pioneered this direction by tracking reference motions to produce physically feasible behaviors. However, such tracking-based methods typically require the controller to rigidly mimic targets frame-by-frame, limiting the flexibility to adapt to new tasks [24]. Furthermore, they often necessitate labor-intensive reward tuning, a challenge partially addressed by introducing Adversarial Differential Discriminator (ADD) [52]. To overcome the constraints of rigid tracking and paired data alignment, distribution-matching approaches such as Generative Adversarial Imitation Learning (GAIL) [18] and Adversarial Motion Priors (AMP) [36] have been widely adopted. By learning flexible motion priors from datasets, these methods provide a task-agnostic measure of naturalness, allowing policies to produce life-like behaviors across diverse tasks. This paradigm was further expanded by ASE [37] to amplify motion diversity and repurpose skills 

hierarchically. The closest method to ours is SMP [29], which leverages pre-trained motion diffusion models with score distillation sampling (SDS) [38] to extract reusable, taskagnostic motion priors. Our work follows a similar **modular** and **reusable** philosophy, but tackles the problem from a different perspective: pose rather than motion. We also show that our prior improves style-conditioned tracking, making it theoretically complementary to SMP. 

**Motion Retargeting.** Retargeting motions from human demonstrations to humanoid robots introduces unique challenges, particularly the strict requirements for physical plausibility and consistent interactions with the environment. Geometric approaches [14, 15, 27, 3] typically minimize keypoint errors via trajectory optimization or inverse kinematics. However, when physical constraints are weak or absent, they can violate kinematic and contact limits, leading to artifacts such as foot skating and interpenetration. To improve retargeting fidelity, subsequent works [2, 21] introduced soft interaction penalties, and OmniRetarget [45] further unifies these objectives by minimizing the interaction mesh [30] Laplacian deformation energy under explicit hard constraints, yielding more robust physical consistency. Complementary to these optimization-based formulations, SPIDER [31] leverages large-scale physics-based sampling in a simulator with curriculum-style virtual contact guidance to resolve contact ambiguity and recover feasible interactions. To the best of our knowledge, PDF-HR is the first learned prior that can be introduced as a regularizer into the optimization loop of existing pipelines, encouraging solutions to remain within the valid configuration space of the humanoid and thereby improving both motion naturalness and physical feasibility. 

## III. BACKGROUND: RIEMANNIAN GEOMETRY 

We first establish the preliminaries needed to formalize our pose distance fields. Following recent works [4, 5, 8, 17, 47], we consider a smooth _m_ -dimensional Riemannian manifold _M_ , smoothly embedded in a higher-dimensional ambient space _X_ (typically R<sup>_n_</sup> ) via an embedding _ι_ : _M �→X_ . The manifold _M_ is endowed with a Riemannian metric **G** ≜ ( **Gx** ) **x** _∈M_ , where each **Gx** defines an inner product on the tangent space _T_ **x** _M_ that varies smoothly with **x** , forming a smooth Riemannian manifold ( _M,_ **G** ). In composite systems, especially for articulations, we exploit the structure of product manifolds [49, 42]. Given _K_ component manifolds _M_ 1 _, . . . , MK_ , their Cartesian product _M_ 1: _K_ = _M_ 1 _× · · · × MK_ is a smooth manifold of dimension<sup>�</sup><sup>_K_</sup> _i_ =1<sup>dim(</sup><sup>_Mi_).</sup> Moreover, equipping it with the canonical product metric yields a Riemannian manifold. When all _K_ components are identical (i.e., _Mi ≡Mj_ ), we denote the configuration space as the power manifold _M_<sup>_K_</sup> , which has dimension _Km_ and inherits a natural product Riemannian structure [49, 42, 17, 47]. 

In the context of HMR and humanoid robotics, the kinematic state of each joint is commonly formalized as a 3D rotation in the Special Orthogonal group SO(3). This Lie group is defined as: 

SO(3) = � **R** _∈_ R<sup>3</sup><sup>_×_3��</sup> **R**<sup>_⊤_</sup> **R** = **I** _,_ det( **R** ) = 1� _._ (1) 

Viewing SO(3) as a submanifold embedded in R<sup>9</sup> (identified with R<sup>3</sup><sup>_×_3</sup> ), the full configuration space of a skeleton with _K_ joints can be constructed as the power manifold of Lie groups: 


Since SO(3) is a Lie group, it admits well-defined tangent spaces and the exponential/logarithmic maps, which allow us to perform local (linear) computations in the tangent space while respecting the underlying manifold geometry. **Definition 1** (Tangent Space) **.** To characterize motion on the curved manifold _M_ embedded in _X_ , we introduce the tangent space _T_ **x** _M_ . Formally, a vector **v** _∈X_ is tangent to _M_ at **x** if it is the velocity of a smooth curve passing through **x** . Let _γ_ : [0 _,_ 1] _→M_ be a smooth curve such that _γ_ (0) = **x** . The tangent space is defined as the collection of all such velocities: 


where _γ_ ˙ (0) is understood as an element of _Tι_ ( **x** ) _X_ via the differential of the embedding _ι_ : _M �→X_ . While the ambient space _X_ supports global linear operations, rigorous kinematic updates must respect the manifold structure defined on the tangent bundle, the disjoint union of tangent spaces: _T M_ ≜ � **x** _∈M_<sup>_{_(</sup><sup>**x**</sup><sup>_,_</sup><sup>**v**)</sup><sup>_|_</sup><sup>**v**</sup><sup>_∈T_</sup><sup>**x**</sup><sup>_M}_.</sup> **Definition 2** (Exponential Map on SO(3)) **.** The matrix exponential exp : so(3) _→_ SO(3) maps a Lie algebra element to a rotation. Given a unit axis **_ω_** ˆ _∈_ R<sup>3</sup> and angle _θ ∈_ R, Rodrigues’ formula yields 


where [ _·_ ] denotes the skew-symmetric matrix operator. **Definition 3** (Local Logarithmic Map on SO(3)) **.** The matrix logarithm log : SO(3) _→_ so(3) is the local inverse of exp. For two rotations **R** 1 _,_ **R** 2 _∈_ SO(3), define **R** ≜ **R** 1<sup>_⊤_</sup><sup>**R**2.Let</sup> _θ ∈_ [0 _, π_ ] satisfy cos _θ_ =<sup>tr(</sup><sup>**R**</sup> 2<sup><u>)</u></sup><sup>_−_1</sup> . Then (for _θ ∈{/_ 0 _, π}_ ), the principal logarithm is given by 


The geodesic distance induced by the canonical bi-invariant Riemannian metric on SO(3) is given by 


where ( _·_ )<sup>_∨_</sup> : so(3) _→_ R<sup>3</sup> is the inverse of the skew operator, and _∥· ∥_ 2 is the Euclidean norm. 


In contemporary humanoids, the articulated body is commonly modeled as a kinematic tree of 1-DoF revolute joints, which enables direct actuation, high structural stiffness, and well-conditioned dynamics. This design choice facilitates efficient whole-body control, optimization, and learning. In this work, we adopt the Unitree G1 humanoid as our primary platform. For a 1-DoF joint, the geodesic metric simplifies to the Euclidean distance. Let _qi, qi_<sup>_′∈_R denote two configurations of</sup> 

the same joint. The corresponding rotations can be expressed as: 


where **k** _∈_ R<sup>3</sup> is the fixed rotation axis and [ **k** ] _∈_ so(3) denotes its associated skew-symmetric matrix. The relative rotation **R** _rel_ = **R**<sup>_⊤_</sup> _i_<sup>**R**</sup><sup>_′_</sup> _i_<sup>canbecalculatedby:</sup> 


Substituting this result into Eq. (6), the geodesic metric strictly reduces to the _L_ 1 distance: 


assuming _qi_ is represented within its joint limits (i.e., no angle wrap-around). 

**Pose Manifold and Distance Field Learning.** We hypothesize that physically plausible robot poses lie on a low-dimensional manifold _MHR_ embedded in the high-dimensional configuration space _Q ⊆_ R<sup>_NJ_</sup> . _Q_ is a proper subset of R<sup>_NJ_</sup> due to per-joint bound constraints specified by the URDF. The instantaneous configuration of the Unitree G1 robot is represented as a vector **q** describing the articulation of its _NJ_ = 29 revolute joints: 


where _qi_ is a scalar joint angle. Endowed with the _L_ 1 product metric, the distance between two configurations is: 


Instead of explicitly parameterizing this manifold, we model _MHR_ implicitly as the zero-level set of a continuous unsigned distance function _fϕ_ : _Q →_ R<sup>+</sup> : 


where _fϕ_ ( **q** ) represents the unsigned geodesic distance to the closest plausible pose on the manifold. 

Training an accurate distance field _fϕ_ requires a large number of samples, including both positive (on-manifold, i.e., zerodistance) and negative (off-manifold, i.e., non-zero-distance) poses. Leveraging recent advances in retargeting, we construct a large-scale positive set _Dp_ using the PHUMA [21], LaFAN1, and AMASS [28] retargeted datasets. We further perform cross-validation to filter unreliable positives. Despite having abundant on-manifold samples, the performance of _fϕ_ depends critically on the statistical coverage of the training distribution and, in particular, on incorporating informative off-manifold negatives _Dn_ . Motivated by NRDF [17], we therefore adopt a hybrid sampling strategy to construct _Dn_ . Details of the hybrid sampling procedure and the cross-validation protocol are provided in the Appendix A. 

With the resulting dataset _D_ = _Dp ∪Dn_ containing _N_ samples, we learn a continuous unsigned distance field via supervised regression. Specifically, _fϕ_ is trained to approximate the minimum geodesic distance from a query pose **q** to 


**Fig. 1:** We present **PDF-HR** , which learns the manifold of plausible G1 poses as a zero-level set. _Left_ : The _fϕ_ is trained to approximate the unsigned pose distance field. Given a query pose **q** , we compute its distance _d_ to the nearest dataset sample and optimize the network to regress this value. _Right_ : The learned prior provides quantitative scores for arbitrary poses, where a larger predicted value _fϕ_ ( **q** ) indicates a significant deviation from the manifold, corresponding to an unnatural pose. This learned prior effectively benefits downstream tasks such as motion tracking and motion retargeting. 

the valid pose manifold _MHR_ , which is approximated by the distance to the nearest sample in the dense dataset _Dp_ . The optimal parameters are obtained by minimizing the objective function: 


Once trained, _fϕ_ serves as a continuous and differentiable pose prior that explicitly captures the geometry of the valid pose manifold. Figure 1 illustrates the full training pipeline. 

For 1-DoF joints, the Riemannian gradient coincides with the Euclidean gradient (proven in Appendix C). Leveraging this differentiability, the projection of an arbitrary query pose **q** onto the manifold _M_ can be formulated as an iterative gradient-based update: 


where _α_ is the step size, _−∇_ **q** _fϕ_ ( **q** _k_ ) _/∥∇_ **q** _fϕ_ ( **q** _k_ ) _∥_ denotes the gradient direction towards the manifold. The operator _P_ enforces physical joint limits, ensuring the updated pose remains within the valid configuration space. 

## V. APPLICATIONS 

## _A. Reinforcement Learning based Motion Tracking_ 

Reinforcement learning (RL) is a standard approach for motion tracking. Modern RL-based tracking methods generally fall into two categories: strict tracking [35, 52] and stylized tracking [36, 29]. In both cases, the reward can be simplified as: 


Here, _rt_<sup>_G_is the task reward, which defines high-level goals for</sup> the character to satisfy (e.g., walking in a target direction or punching a target). _rt_<sup>_T_denotesthetrackingreward.Forstrict</sup> 

tracking, it encourages the character to imitate the reference motion as closely as possible, typically by minimizing the pose discrepancy between the simulated character and the target poses from the reference trajectory. In contrast, for stylized tracking, _rt_<sup>_T_encouragessimilarityinmotionstyleandisnot</sup> directly tied to pose error. _w_<sup>_T_</sup> and _w_<sup>_G_</sup> are the corresponding reward weights. 

Although RL-based tracking methods can successfully follow most motions, they typically require long training times to explore a sufficiently diverse set of states. To improve training efficiency, we introduce a pose-prior reward that encourages the policy to explore near the learned pose manifold. Specifically, we first define a pose score _s_ as 


where _dbad_ is a scalar hyperparameter. In all experiments, we set _dbad_ = 0 _._ 4 (i.e., if the predicted pose distance _fϕ_ ( **q** _t_ ) exceeds 0 _._ 4, we treat the pose as abnormal). _dgood_ is computed from the reference motion as the maximum _fϕ_ ( **q** _t_ ) observed along the trajectory. We clip _s_ ( **q** _t_ ) to [0 _,_ 1] for training stability. We then define the pose-prior reward _rt_<sup>_P_as:</sup> 


Here _α_<sup>_P_</sup> controls the scale of the pose-prior term. Thus, our full reward can be formulated as: 


where _w_<sup>_P_</sup> is the weight of the pose reward _rt_<sup>_P_.</sup> 

## _B. Motion Retargeting_ 

Physical humanoids only approximate human morphology, with significant differences in shape, proportion, and degrees of freedom; this is also called the embodiment gap. A common way to bridge this gap is to retarget human motion data to a 


**Fig. 2: Visualization of joint orientation distributions of Sideflip at early training stage.** The visualization maps the directional vectors of the robot’s links onto unit spheres centered at their respective joints. The color gradient corresponds to the probability density of the visited states. 

humanoid embodiment and then train RL policies to imitate the resulting reference trajectories. Existing works [45] have shown that high-quality retargeting algorithms can substantially alleviate extensive reward engineering. For clarity, we adopt GMR [3] as a representative retargeting method and illustrate how to incorporate our pose prior. 

GMR [3] performs retargeting by solving an inverse kinematics (IK) problem at each frame. At each timestep _t_ , GMR finds the robot configuration **q** _t_ that matches the source keypoint positions and orientations via the following optimization program: 


where _fi_<sup>_p_and</sup><sup>_f_</sup> _i_<sup>_θ_aretherobotforwardkinematicsforthe</sup> _i_ -th keypoint’s position and orientation, respectively. Leveraging the Mink [48] library, GMR solves this program in a Sequential Quadratic Programming fashion. 

A key limitation of GMR is the need for tedious parameter tuning, especially careful per-joint weighting, to avoid optimization artifacts. Since our pose distance field is continuous and differentiable, we can simply add an extra prior term to Eq. (19). The resulting objective becomes: 


To validate the effectiveness of our method, we integrate it into four humanoid tasks: single-trajectory motion tracking, general motion tracking, style-based motion mimicry, and general motion retargeting. Comprehensive details regarding the implementation and experimental configurations are provided in the Appendix D. 

**Metrics.** We evaluate our method against baselines in terms of sample efficiency and motion tracking error. All policies are trained with 4096 parallel environments and evaluated on 4096 test episodes every 100 training iterations. We define the motion tracking success rate as the ratio of continuous tracking 

duration to the total episode length. The sample efficiency is measured by the number of training samples required to first reach 80% success rate. The position error _E_<sup>pos</sup> and rotation error _E_<sup>rot</sup> are defined as: 


where _e_<sup>pos</sup> _j_ , _e_<sup>pos</sup> root<sup>,</sup><sup>_e_rot</sup> _j_<sup>,and</sup><sup>_e_</sup> root<sup>rotrepresentthetime-averaged</sup> _j_ -th joint position error, root position error, _j_ -th joint rotation error, and root rotation error, respectively. Joint errors are computed in the robot’s local coordinate frame, while root errors are computed in the global coordinate frame. For general motion tracking, we additionally report the detailed errors (i.e., joint position error _e_ ¯<sup>pos</sup> _joint_<sup>=</sup> �� _j∈_ joints<sup>_e_</sup> _j_<sup>pos</sup> � _/N_ , = root position error _e_<sup>pos</sup> root<sup>,jointrotationerror</sup><sup>_e_¯rot</sup> _joint_ �� _j∈_ joints<sup>_e_</sup> _j_<sup>rot</sup> � _/N_ and root rotation error _e_<sup>rot</sup> root<sup>)foramore</sup> fine-grained comparison. 

## _A. Single-trajectory Motion Tracking_ 

**Experiment settings.** We compare our method with ADD [52] in the single-trajectory tracking task using nine motion clips: three easy motions (Walk, Run, Jump), four hard motions (Spinkick, Cartwheel, Backflip, Sideflip), and two parkour motions (Double Kong, Speed Vault). The parkour skills are particularly challenging, as they require high tracking accuracy to reproduce intricate contacts with the environment. For a fair comparison, all policies are trained with 800 million samples with the same hyperparameters. 

**Results.** Table I presents the quantitative comparisons. Our method achieves substantially higher sample efficiency across all motions and achieves lower tracking error on most hard and parkour motions. Notably, this advantage in sample efficiency becomes more pronounced as the motion difficulty increases. 

To better understand the exploration behavior, we logged the actions during the early stage of training (around 125 million samples) on Sideflip. Figure 2 visualizes the resulting action distributions as heatmaps. Compared to ADD, our method produces an action distribution that aligns much more closely with the reference motion. This matters because a humanoid’s action space is continuous and high-dimensional, while the set of actions that stay on a plausible motion manifold occupies only a small fraction of the total volume. For highly dynamic motions, the local neighborhood is dominated by invalid poses, causing ADD to waste substantial samples exploring unproductive regions. Our pose-prior guidance alleviates this by steering exploration toward a valid, well-shaped subspace. Meanwhile, since the strict tracking objective is maintained, the policy explores primarily within this reduced space, enabling faster convergence to the optimal solution. We further provide qualitative visual comparisons in Figure 3 to corroborate this observation. 


**Fig. 3:** Visual comparisons of motion tracking performance on dynamic skills between our method and ADD [52]. The number of training samples is annotated on the left of each strip. Our method successfully masters these complex skills with remarkably fewer samples, whereas the baseline frequently suffers from falls or collisions even after extensive training. 

**TABLE I:** Comparison of sample efficiency and motion-tracking performance between ADD [52] and our method on the single-trajectory motion-tracking task. Metrics are reported as mean _±_ 1 std over three independently trained models with different random initializations. A motion is marked as **Failed** if all three trials fail to converge within 800M training samples. 

|**Skill**|**Length**|**Samples (**_SR _|_≥_80% **) [M]**|**Position **|**Error [m]**|**Rotation E**|**rror [rad]**|
|---|---|---|---|---|---|---|---|
|||**ADD**|**Ours**|**ADD**|**Ours**|**ADD**|**Ours**|
|Walk|1.03|70_._036<sup>_±_6</sup><sup>_._179</sup>|56_._929<sup>_±_6</sup><sup>_._179</sup>|0_._008<sup>_±_0</sup><sup>_._000</sup>|0_._009<sup>_±_0</sup><sup>_._000</sup>|0_._038<sup>_±_0</sup><sup>_._001</sup>|0_._042<sup>_±_0</sup><sup>_._002</sup>|
|Run|0.80|113_._727<sup>_±_6</sup><sup>_._179</sup>|70_._036<sup>_±_6</sup><sup>_._179</sup>|0_._015<sup>_±_0</sup><sup>_._000</sup>|0_._017<sup>_±_0</sup><sup>_._000</sup>|0_._063<sup>_±_0</sup><sup>_._001</sup>|0_._070<sup>_±_0</sup><sup>_._001</sup>|
|Jump|1.75|222_._953<sup>_±_10</sup><sup>_._702</sup>|188_._001<sup>_±_16</sup><sup>_._348</sup>|0_._022<sup>_±_0</sup><sup>_._001</sup>|0_._024<sup>_±_0</sup><sup>_._001</sup>|0_._108<sup>_±_0</sup><sup>_._004</sup>|0_._103<sup>_±_0</sup><sup>_._003</sup>|
|Spinkick|1.28|135_._572<sup>_±_6</sup><sup>_._179</sup>|91_._881<sup>_±_0</sup><sup>_._000</sup>|0_._031<sup>_±_0</sup><sup>_._000</sup>|0_._032<sup>_±_0</sup><sup>_._001</sup>|0_._150<sup>_±_0</sup><sup>_._002</sup>|0_._161<sup>_±_0</sup><sup>_._004</sup>|
|Cartwheel|2.72|183_._632<sup>_±_0</sup><sup>_._000</sup>|161_._787<sup>_±_12</sup><sup>_._358</sup>|0_._031<sup>_±_0</sup><sup>_._000</sup>|0_._028<sup>_±_0</sup><sup>_._003</sup>|0_._129<sup>_±_0</sup><sup>_._007</sup>|0_._126<sup>_±_0</sup><sup>_._010</sup>|
|Backflip|1.69|Failed|183_._632<sup>_±_18</sup><sup>_._536</sup>|Failed|0_._048<sup>_±_0</sup><sup>_._000</sup>|Failed|0_._205<sup>_±_0</sup><sup>_._004</sup>|
|Sideflip|2.38|336_._549<sup>_±_62</sup><sup>_._708</sup>|166_._156<sup>_±_6</sup><sup>_._179</sup>|0_._051<sup>_±_0</sup><sup>_._002</sup>|0_._050<sup>_±_0</sup><sup>_._001</sup>|0_._241<sup>_±_0</sup><sup>_._003</sup>|0_._242<sup>_±_0</sup><sup>_._005</sup>|
|Speed Vault|1.92|388_._978<sup>_±_49</sup><sup>_._430</sup>|122_._465<sup>_±_6</sup><sup>_._179</sup>|0_._024<sup>_±_0</sup><sup>_._001</sup>|0_._023<sup>_±_0</sup><sup>_._000</sup>|0_._118<sup>_±_0</sup><sup>_._003</sup>|0_._116<sup>_±_0</sup><sup>_._001</sup>|
|Double Kong|5.17|Failed|288_._489<sup>_±_10</sup><sup>_._702</sup>|Failed|0_._031<sup>_±_0</sup><sup>_._001</sup>|Failed|0_._157<sup>_±_0</sup><sup>_._003</sup>|


## _B. Style-based Motion Mimicry_ 

**Experiment settings.** We compare our method with AMP [36] on three easy motions (Walk, Run, Jump) and three hard motions (Spinkick, Cartwheel, Sideflip), as summarized in Table II. All policies are trained with 800 million samples for a fair comparison. Although style-based motion mimicry does not aim for precise motion tracking, we still report tracking error to facilitate comparison. 

**Results.** Our method consistently outperforms AMP in terms 

of sample efficiency while maintaining a comparable level of tracking error. The qualitative results at an intermediate training stage (350 million samples for all policies) are presented in Appendix E. Even with this limited training budget, our method generally mimics all reference motions, highlighting the stability and efficiency brought by our pose-prior reward. 

We further evaluate our method on the _Target Location_ and _Heading_ tasks and obtain consistent results. Due to space limitations, we report the task-oriented results in Appendix F 

**TABLE II:** Quantitative results in mean _±_ 1 std across 3 random seeds of AMP [36] and our method in style-based motion mimicry task. 

|**Skill**|**Length**|**Samples (**_SR _|_≥_80% **) [M]**|**Position **|**Error [m]**|**Rotation **|**Error [rad]**|
|---|---|---|---|---|---|---|---|
|||**AMP**|**Ours**|**AMP**|**Ours**|**AMP**|**Ours**|
|Walk|1.03|91_._881<sup>_±_0</sup><sup>_._000</sup>|65_._667<sup>_±_0</sup><sup>_._000</sup>|0_._228<sup>_±_0</sup><sup>_._002</sup>|0_._228<sup>_±_0</sup><sup>_._002</sup>|0_._301<sup>_±_0</sup><sup>_._002</sup>|0_._304<sup>_±_0</sup><sup>_._003</sup>|
|Run|0.80|104_._989<sup>_±_0</sup><sup>_._000</sup>|87_._512<sup>_±_6</sup><sup>_._179</sup>|0_._601<sup>_±_0</sup><sup>_._004</sup>|0_._593<sup>_±_0</sup><sup>_._002</sup>|0_._708<sup>_±_0</sup><sup>_._000</sup>|0_._718<sup>_±_0</sup><sup>_._004</sup>|
|Jump|1.75|323_._442<sup>_±_26</sup><sup>_._933</sup>|196_._739<sup>_±_21</sup><sup>_._404</sup>|0_._189<sup>_±_0</sup><sup>_._010</sup>|0_._163<sup>_±_0</sup><sup>_._003</sup>|0_._490<sup>_±_0</sup><sup>_._011</sup>|0_._480<sup>_±_0</sup><sup>_._003</sup>|
|Spinkick|1.28|183_._632<sup>_±_0</sup><sup>_._000</sup>|161_._787<sup>_±_6</sup><sup>_._179</sup>|0_._319<sup>_±_0</sup><sup>_._002</sup>|0_._316<sup>_±_0</sup><sup>_._008</sup>|1_._634<sup>_±_0</sup><sup>_._003</sup>|1_._637<sup>_±_0</sup><sup>_._003</sup>|
|Cartwheel|2.72|240_._430<sup>_±_6</sup><sup>_._179</sup>|209_._846<sup>_±_74</sup><sup>_._914</sup>|0_._455<sup>_±_0</sup><sup>_._004</sup>|0_._399<sup>_±_0</sup><sup>_._013</sup>|1_._604<sup>_±_0</sup><sup>_._008</sup>|1_._607<sup>_±_0</sup><sup>_._039</sup>|
|Sideflip|2.38|393_._347<sup>_±_28</sup><sup>_._315</sup>|345_._287<sup>_±_40</sup><sup>_._517</sup>|0_._327<sup>_±_0</sup><sup>_._010</sup>|0_._336<sup>_±_0</sup><sup>_._005</sup>|1_._254<sup>_±_0</sup><sup>_._028</sup>|1_._282<sup>_±_0</sup><sup>_._022</sup>|


**TABLE III:** General motion tracking performance comparison across different episode lengths. **Ours** is trained with ADD [52] augmented by the pose-prior reward. **Ours*** is trained in two stages: 4 billion samples guided by PDF-HR, then 8 billion samples of resumed training with the original ADD objective. All policies are trained with 12 billion total samples for a fair comparison. 

|**Episode**<br>**Length [s]**|**Joint P**|**osition Er**|**ror [m]**|**Root P**|**osition Err**|**or [m]**|**Joint Ro**|**tation Err**|**or [rad]**|**Root R**|**otation Err**|**or [rad]**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||**ADD**|**Ours**|**Ours***|**ADD**|**Ours**|**Ours***|**ADD**|**Ours**|**Ours***|**ADD**|**Ours**|**Ours***|
|10|0.022|0.023|0.019|0.095|0.101|0.107|0.121|0.129|0.108|0.075|0.080|0.066|
|20|0.022|0.023|0.019|0.098|0.099|0.111|0.123|0.127|0.107|0.075|0.079|0.066|
|30|0.022|0.022|0.018|0.103|0.104|0.112|0.122|0.125|0.102|0.077|0.077|0.062|


|**LE IV:**|Quantitative c|omparisons|of retargetin|g quality. Tra|cking metrics|whereas the two-stage protocol effectively mitigates this issue|
|---|---|---|---|---|---|---|
|uced by a<br>on tracki<br>ion error|n ADD poli<br>ng length in <br>s. **BRE** and|cy trained on<br>frames. **BPE**<br> **RRE** are b|each retarg<br> and **RPE** a<br>ody and roo|eted dataset. <br>re short for b<br>t rotation er|**MTL** means<br>ody and root<br>rors. **R.M.** is|and consistently achieves the lowest joint position error, joint<br>rotation error, and root rotation error. Intuitively, the first stage|
|t for retar|geting metho|ds.||||uses the prior reward to quickly acquire basic locomotion and|
|**R.M.**|**MTL**<br>**(frames)**|**BPE**<br>**[m]**|**RPE**<br>**[m]**|**BRE**<br>**[rad]**|**RRE**<br>**[rad]**|coordination skills, as reflected by the rapid rise in success<br>rate; the second stage then focuses purely on tracking to<br>fi  Oll h  hd ik|
|GMR|95.708|0.029|0.113|0.197|0.087|reine accuracy. vera, te two-stage meto stres a strong<br>balance between fast convergence and precise motion tracking.|
|Ours|101.613|0.029|0.124|0.162|0.087||


**TABLE IV:** Quantitative comparisons of retargeting quality. Tracking metrics produced by an ADD policy trained on each retargeted dataset. **MTL** means motion tracking length in frames. **BPE** and **RPE** are short for body and root position errors. **BRE** and **RRE** are body and root rotation errors. **R.M.** is short for retargeting methods. 

## _D. Motion Retargeting_ 

## _C. General Motion Tracking_ 

**Experiment settings.** For this task, both our method and the baseline ADD [52] are trained with a single general policy to track a large-scale motion dataset, utilizing a subset of LaFAN1 [13]. The subset contains 34 sequences (excluding six FallAndGetUp sequences), totaling 7887.6 seconds of motion. We adopt a two-stage training strategy (dubbed as **Ours*** ) to improve the tracking accuracy. For this strategy, we first train the policy with the pose-prior reward for 4 billion samples, then disable the prior and resume the training with the original ADD objective. All policies are trained with 12 billion samples in total for a fair comparison. To assess convergence under different horizon lengths, we additionally vary the episode duration and evaluate tracking horizons of 10, 20, and 30 seconds for both our method and ADD. 

**Results.** Quantitative results are reported in Table III, and learning curves are provided in Appendix E. Benefiting from the guidance of the PDF-HR pose-prior reward, our method exhibits significantly faster convergence compared to the baseline. This advantage becomes more pronounced as the episode length increases, demonstrating improved robustness for long-horizon tracking. We also observe that the onestage training yields slightly higher tracking error than ADD, 

**Experiment settings.** For the motion retargeting task, we compare our method with GMR [3] on a subset of the AMASS [28] DanceDB dataset. 30 sequences are sampled from DanceDB, totaling 7,770 frames (254.7 seconds). We retarget the same SMPL-X [33] motions to the Unitree G1 robot using both GMR and our method, producing two sets of retargeted reference motions. To evaluate how well these motions can be tracked in physics, we train an ADD-based general tracking policy on each reference set and compare the resulting tracking errors. 

**Results.** Figure 4 presents a visual comparison between the retargeted motions and the original SMPL-X motions. As highlighted by the red indicators, GMR often produces kinematically implausible artifacts, including severe joint distortions (e.g., at the wrists, torso, and legs) and noticeable selfpenetration. These artifacts not only deviate from the original human motion but are also physically infeasible, which makes them difficult to track in physics-based simulators. The quantitative results in Table IV corroborate this observation: such inconsistencies in GMR lead to shorter continuous tracking durations and larger body rotation errors. In contrast, our PDF-HR regularizer steers the optimizer away from poor local minima without requiring tedious parameter tuning, yielding retargeted motions that are both visually faithful to the reference and physically valid for tracking. 


**Fig. 4:** Visual comparison of retargeted motions produced by GMR [3] (red) and our method (green). GMR artifacts are highlighted with red markers. 


**Fig. 5: Real-world deployment.** (a) Deploying GMR-retargeted Seq. 4. Artifacts introduced by GMR lead to poor alignment with the reference motion and frequent self-collisions. (b) Deploying our retargeted Seq. 4. Our method produces smooth, physically plausible motions that closely match the reference sequence. (c) Deploying our retargeted Seq. 2 for highly dynamic skills. Our method robustly executes challenging motions, including dance and spinning jumps. 

**Deployment validation.** We further evaluate deployability using BeyondMimic [23]. We select 10 motion sequences and compare policies trained on GMR-retargeted data versus our retargeted data. Our method successfully deploys on 9/10 sequences, whereas GMR succeeds on only 6/10. Detailed learning curves are provided in Appendix E. Figure 5 visualizes real-world deployment results, where our method produces behaviors that are noticeably more natural and closer to the target motions than those from GMR. 

## VII. CONCLUSION 

In this work, we introduce Pose Distance Fields for Humanoid Robots (PDF-HR), a lightweight and differentiable prior that models the plausibility of humanoid robot poses as a continuous distance field learned from a large corpus of retargeted motions. PDF-HR is simple to integrate into existing pipelines and broadly applicable to optimization and learn- 

ing. Across multiple humanoid benchmarks, including singletrajectory tracking, general motion tracking, style-conditioned mimicry, and motion retargeting, PDF-HR consistently improves strong baselines, demonstrating the value of pose-level priors for robust humanoid behavior. Our results highlight the importance of pose priors for humanoid control and open opportunities for more data-driven approaches in humanoid motion generation and understanding. 

## VIII. LIMITATIONS 

While PDF-HR demonstrates promising results across a range of humanoid tasks, it has several limitations: 

- **Accuracy in some tracking settings.** Although PDF-HR can substantially accelerate convergence, its final tracking accuracy is occasionally lower than that of the baseline. We acknowledge this as a limitation. 

- **Mode collapse in style-conditioned tracking.** In style tracking, our method can suffer from mode collapse, similar to AMP [36]. A potential remedy is to enrich the prior with additional kinematic information, e.g., velocity- and acceleration-based fields [47], to better constrain longhorizon behavior. 

- **Runtime and smoothness in retargeting.** Our current implementation is slower than GMR [3], and it can sometimes exhibit more severe jitter. GPU-parallel batch processing and incorporating explicit smoothness costs could mitigate these issues and better reveal the practical advantages of our approach [20]. 

- **Training data quality.** Our pose field is trained on retargeted poses, which may not always be physically feasible. An important future direction is to curate or collect large-scale pose corpora that better satisfy physical constraints, thereby improving the fidelity and robustness of the learned field. 

REFERENCES 

## 2020. 

- [1] Ijaz Akhter and Michael J Black. Pose-conditioned joint angle limits for 3d human pose reconstruction. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 1446–1455, 2015. 

- [2] Arthur Allshire, Hongsuk Choi, Junyi Zhang, David McAllister, Anthony Zhang, Chung Min Kim, Trevor Darrell, Pieter Abbeel, Jitendra Malik, and Angjoo Kanazawa. Visual imitation enables contextual humanoid control. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2025. 

- [3] Joao Pedro Araujo, Yanjie Ze, Pei Xu, Jiajun Wu, and C Karen Liu. Retargeting matters: General motion retargeting for humanoid motion tracking. _arXiv preprint arXiv:2510.02252_ , 2025. 

- [4] Tolga Birdal and Umut Simsekli. Probabilistic permutation synchronization using the riemannian structure of the birkhoff polytope. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 11105–11116, 2019. 

- [5] Tolga Birdal, Umut Simsekli, Mustafa Onur Eken, and Slobodan Ilic. Bayesian pose graph optimization via bingham distributions and tempered geodesic mcmc. _Advances in neural information processing systems_ , 31, 2018. 

- [6] Federica Bogo, Angjoo Kanazawa, Christoph Lassner, Peter Gehler, Javier Romero, and Michael J Black. Keep it smpl: Automatic estimation of 3d human pose and shape from a single image. In _European conference on computer vision_ , pages 561–578. Springer, 2016. 

- [7] Bingjie Chen, Zihan Wang, Zhe Han, Guoping Pan, Yi Cheng, and Houde Liu. Hl-ik: A lightweight implementation of human-like inverse kinematics in humanoid arms. _arXiv preprint arXiv:2509.20263_ , 2025. 

- [8] Jiayi Chen, Yingda Yin, Tolga Birdal, Baoquan Chen, Leonidas J Guibas, and He Wang. Projective manifold gradient layer for deep rotation regression. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 6646–6655, 2022. 

- [9] Zixuan Chen, Mazeyu Ji, Xuxin Cheng, Xuanbin Peng, Xue Bin Peng, and Xiaolong Wang. Gmt: General motion tracking for humanoid whole-body control. _arXiv preprint arXiv:2506.14770_ , 2025. 

- [10] Stelian Coros, Philippe Beaudoin, and Michiel Van de Panne. Generalized biped walking control. _ACM Transactions On Graphics (TOG)_ , 29(4):1–9, 2010. 

- [11] Sai Kumar Dwivedi, Yu Sun, Priyanka Patel, Yao Feng, and Michael J Black. Tokenhmr: Advancing human mesh recovery with a tokenized pose representation. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 1323–1333, 2024. 

- [12] Georgios Georgakis, Ren Li, Srikrishna Karanam, Terrence Chen, Jana Koˇseck´a, and Ziyan Wu. Hierarchical kinematic human mesh recovery. In _European Conference on Computer Vision_ , pages 768–784. Springer, 

- [13] F´elix G Harvey, Mike Yurick, Derek Nowrouzezahrai, and Christopher Pal. Robust motion in-betweening. _ACM Transactions on Graphics (TOG)_ , 39(4):60–1, 2020. 

- [14] Tairan He, Zhengyi Luo, Xialin He, Wenli Xiao, Chong Zhang, Weinan Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. Omnih2o: Universal and dexterous humanto-humanoid whole-body teleoperation and learning. _arXiv preprint arXiv:2406.08858_ , 2024. 

- [15] Tairan He, Jiawei Gao, Wenli Xiao, Yuanhang Zhang, Zi Wang, Jiashun Wang, Zhengyi Luo, Guanqi He, Nikhil Sobanbab, Chaoyi Pan, et al. Asap: Aligning simulation and real-world physics for learning agile humanoid whole-body skills. _arXiv preprint arXiv:2502.01143_ , 2025. 

- [16] Tairan He, Jiawei Gao, Wenli Xiao, Yuanhang Zhang, Zi Wang, Jiashun Wang, Zhengyi Luo, Guanqi He, Nikhil Sobanbabu, Chaoyi Pan, Zeji Yi, Guannan Qu, Kris Kitani, Jessica K. Hodgins, Linxi Fan, Yuke Zhu, Changliu Liu, and Guanya Shi. ASAP: Aligning Simulation and Real-World Physics for Learning Agile Humanoid Whole-Body Skills. In _Proceedings of Robotics: Science and Systems_ , LosAngeles, CA, USA, June 2025. doi: 10.15607/RSS.2025.XXI.066. 

- [17] Yannan He, Garvita Tiwari, Tolga Birdal, Jan Eric Lenssen, and Gerard Pons-Moll. Nrdf: Neural riemannian distance fields for learning articulated pose priors. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 1661–1671, 2024. 

- [18] Jonathan Ho and Stefano Ermon. Generative adversarial imitation learning. _Advances in neural information processing systems_ , 29, 2016. 

- [19] Angjoo Kanazawa, Michael J Black, David W Jacobs, and Jitendra Malik. End-to-end recovery of human shape and pose. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 7122– 7131, 2018. 

- [20] Chung Min Kim*, Brent Yi*, Hongsuk Choi, Yi Ma, Ken Goldberg, and Angjoo Kanazawa. Pyroki: A modular toolkit for robot kinematic optimization. In _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2025. URL https://arxiv.org/abs/ 2505.03728. 

- [21] Kyungmin Lee, Sibeen Kim, Minho Park, Hyunseung Kim, Dongyoon Hwang, Hojoon Lee, and Jaegul Choo. Phuma: Physically-grounded humanoid locomotion dataset. _arXiv preprint arXiv:2510.26236_ , 2025. 

- [22] Jialong Li, Xuxin Cheng, Tianshu Huang, Shiqi Yang, Ri-Zhao Qiu, and Xiaolong Wang. AMO: Adaptive Motion Optimization for Hyper-Dexterous Humanoid Whole-Body Control. In _Proceedings of Robotics: Science and Systems_ , LosAngeles, CA, USA, June 2025. doi: 10.15607/RSS.2025.XXI.061. 

- [23] Qiayuan Liao, Takara E Truong, Xiaoyu Huang, Yuman Gao, Guy Tevet, Koushil Sreenath, and C Karen Liu. Beyondmimic: From motion tracking to versatile 

humanoid control via guided diffusion. _arXiv preprint arXiv:2508.08241_ , 2025. 

- [24] Libin Liu and Jessica Hodgins. Learning to schedule control fragments for physics-based characters using deep q-learning. _ACM Transactions on Graphics (TOG)_ , 36(3):1–14, 2017. 

- [25] Junzhe Lu, Jing Lin, Hongkun Dou, Ailing Zeng, Yue Deng, Yulun Zhang, and Haoqian Wang. Dposer: Diffusion model as robust 3d human pose prior. _arXiv preprint arXiv:2312.05541_ , 2023. 

- [26] Junzhe Lu, Jing Lin, Hongkun Dou, Ailing Zeng, Yue Deng, Xian Liu, Zhongang Cai, Lei Yang, Yulun Zhang, Haoqian Wang, et al. Dposer-x: Diffusion model as robust 3d whole-body human pose prior. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 9988–9997, 2025. 

- [27] Zhengyi Luo, Jinkun Cao, Kris Kitani, Weipeng Xu, et al. Perpetual humanoid control for real-time simulated avatars. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 10895–10904, 2023. 

- [28] Naureen Mahmood, Nima Ghorbani, Nikolaus F. Troje, Gerard Pons-Moll, and Michael J. Black. AMASS: Archive of motion capture as surface shapes. In _International Conference on Computer Vision_ , pages 5442– 5451, October 2019. 

- [29] Yuxuan Mu, Ziyu Zhang, Yi Shi, Minami Matsumoto, Kotaro Imamura, Guy Tevet, Chuan Guo, Michael Taylor, Chang Shu, Pengcheng Xi, et al. Smp: Reusable score-matching motion priors for physics-based character control. _arXiv preprint arXiv:2512.03028_ , 2025. 

- [30] Shin’ichiro Nakaoka and Taku Komura. Interaction mesh based motion adaptation for biped humanoid robots. In _2012 12th IEEE-RAS International Conference on Humanoid Robots (Humanoids 2012)_ , pages 625–631. IEEE, 2012. 

- [31] Chaoyi Pan, Changhao Wang, Haozhi Qi, Zixi Liu, Homanga Bharadhwaj, Akash Sharma, Tingfan Wu, Guanya Shi, Jitendra Malik, and Francois Hogan. Spider: Scalable physics-informed dexterous retargeting. _arXiv preprint arXiv:2511.09484_ , 2025. 

- [32] Yixuan Pan, Ruoyi Qiao, Li Chen, Kashyap Chitta, Liang Pan, Haoguang Mai, Qingwen Bu, Hao Zhao, Cunyuan Zheng, Ping Luo, et al. Agility meets stability: Versatile humanoid control with heterogeneous data. _arXiv preprint arXiv:2511.17373_ , 2025. 

- [33] Georgios Pavlakos, Vasileios Choutas, Nima Ghorbani, Timo Bolkart, Ahmed A. A. Osman, Dimitrios Tzionas, and Michael J. Black. Expressive body capture: 3D hands, face, and body from a single image. In _Proceedings IEEE Conf. on Computer Vision and Pattern Recognition (CVPR)_ , pages 10975–10985, 2019. 

- [34] Xue Bin Peng. Mimickit: A reinforcement learning framework for motion imitation and control. _arXiv preprint arXiv:2510.13794_ , 2025. 

- [35] Xue Bin Peng, Pieter Abbeel, Sergey Levine, and Michiel 

Van de Panne. Deepmimic: Example-guided deep reinforcement learning of physics-based character skills. _ACM Transactions On Graphics (TOG)_ , 37(4):1–14, 2018. 

- [36] Xue Bin Peng, Ze Ma, Pieter Abbeel, Sergey Levine, and Angjoo Kanazawa. Amp: Adversarial motion priors for stylized physics-based character control. _ACM Transactions on Graphics (ToG)_ , 40(4):1–20, 2021. 

- [37] Xue Bin Peng, Yunrong Guo, Lina Halper, Sergey Levine, and Sanja Fidler. Ase: Large-scale reusable adversarial skill embeddings for physically simulated characters. _ACM Transactions On Graphics (TOG)_ , 41 (4):1–17, 2022. 

- [38] Ben Poole, Ajay Jain, Jonathan T. Barron, and Ben Mildenhall. Dreamfusion: Text-to-3d using 2d diffusion. In _The Eleventh International Conference on Learning Representations, ICLR 2023, Kigali, Rwanda, May 1-5, 2023_ , 2023. URL https://openreview.net/pdf?id= FjNys5c7VyY. 

- [39] Davis Rempe, Tolga Birdal, Aaron Hertzmann, Jimei Yang, Srinath Sridhar, and Leonidas J Guibas. Humor: 3d human motion model for robust pose estimation. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 11488–11499, 2021. 

- [40] Wenkang Shan, Zhenhua Liu, Xinfeng Zhang, Zhao Wang, Kai Han, Shanshe Wang, Siwei Ma, and Wen Gao. Diffusion-based 3d human pose estimation with multihypothesis aggregation. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 14761–14771, 2023. 

- [41] Garvita Tiwari, Dimitrije Anti´c, Jan Eric Lenssen, Nikolaos Sarafianos, Tony Tung, and Gerard Pons-Moll. Posendf: Modeling human pose manifolds with neural distance fields. In _European Conference on Computer Vision_ , pages 572–589. Springer, 2022. 

- [42] Nathaniel S Woodward, Sang Eon Park, Gaia Grosso, Jeffrey Krupa, and Philip Harris. Product manifold machine learning for physics. _arXiv preprint arXiv:2412.07033_ , 2024. 

- [43] Weiji Xie, Jiakun Zheng, and Chenjia Bai. TextOp: Real-time Interactive Text-Driven Humanoid Robot Motion Generation and Control. _https://github.com/TeleHuman/TextOp_ , November 2025. 

- [44] Yufei Xue, Wentao Dong, Minghuan Liu, Weinan Zhang, and Jiangmiao Pang. A Unified and General Humanoid Whole-Body Controller for Fine-Grained Locomotion. In _Proceedings of Robotics: Science and Systems_ , LosAngeles, CA, USA, June 2025. doi: 10.15607/RSS.2025. XXI.067. 

- [45] Lujie Yang, Xiaoyu Huang, Zhen Wu, Angjoo Kanazawa, Pieter Abbeel, Carmelo Sferrazza, C Karen Liu, Rocky Duan, and Guanya Shi. Omniretarget: Interactionpreserving data generation for humanoid whole-body loco-manipulation and scene interaction. _arXiv preprint arXiv:2509.26633_ , 2025. 

- [46] KangKang Yin, Kevin Loken, and Michiel Van de Panne. 

Simbicon: Simple biped locomotion control. _ACM Transactions on Graphics (TOG)_ , 26(3):105–es, 2007. 

- [47] Zhengdi Yu, Simone Foti, Linguang Zhang, Amy Zhao, Cem Keskin, Stefanos Zafeiriou, and Tolga Birdal. Geometric neural distance fields for learning human motion priors. _arXiv preprint arXiv:2509.09667_ , 2025. 

- [48] Kevin Zakka. Mink: Python inverse kinematics based on MuJoCo. _https://github.com/kevinzakka/mink_ , December 2025. 

- [49] Sharon Zhang, Amit Moscovich, and Amit Singer. Product manifold learning. In _International Conference on Artificial Intelligence and Statistics_ , pages 3241–3249. PMLR, 2021. 

- [50] Siwei Zhang, Bharat Lal Bhatnagar, Yuanlu Xu, Alexander Winkler, Petr Kadlecek, Siyu Tang, and Federica Bogo. Rohm: Robust human motion reconstruction via diffusion. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 14606–14617, 2024. 

- [51] Tong Zhang, Boyuan Zheng, Ruiqian Nai, Yingdong Hu, Yen-Jen Wang, Geng Chen, Fanqi Lin, Jiongye Li, Chuye Hong, Koushil Sreenath, and Yang Gao. Hub: Learning extreme humanoid balance. In _9th Annual Conference on Robot Learning_ , 2025. URL https://openreview.net/ forum?id=FCpYuGtN4j. 

- [52] Ziyu Zhang, Sergey Bashkirov, Dun Yang, Yi Shi, Michael Taylor, and Xue Bin Peng. Physics-based motion imitation with adversarial differential discriminators. In _Proceedings of the SIGGRAPH Asia 2025 Conference Papers_ , pages 1–12, 2025. 

## APPENDIX 

## _A. PDF-HR Training Details_ 

To learn a continuous and differentiable representation of the pose distance field, dense coverage of the state space is essential. Pose-NDF [41] typically generates off-manifold samples by perturbing clean poses with Gaussian noise. Formally, given a clean pose **q** on the manifold, a corrupted sample is generated as **q** ˆ = **q** + **_ϵ_** , where **_ϵ_** _∼N_ (0 _, σ_<sup>2</sup> **I** ). However, this method introduces a sampling bias. In an _N_ -dimensional space, the normalized squared Euclidean norm of the noise vector follows a Chi-squared distribution: 


Consequently, the perturbation magnitudes concentrate within a narrow spherical shell around _σ_ _~~√~~ N_ , preventing the network from effectively learning the distance field’s transition across different scales. This concentration compromises the continuity of the represented manifold. To address this limitation, we construct a composite training dataset _D_ derived from a high-fidelity reference dataset, denoted as _D_ raw. The final training set _D_ = _D_ on _∪D_ near _∪D_ interp aggregates samples from three distinct generation strategies. 

**On-Manifold Sampling.** We directly sample raw pose states **q** from the reference dataset _D_ raw. These samples represent the ground truth geometry of the valid pose distance field. Consequently, for every sample **q** _∈D_ raw, we assign a zerodistance label: 


**Near-Manifold Sampling.** To characterize the distance field gradients in the immediate vicinity of the manifold, we employ a decoupled perturbation strategy. Unlike standard Gaussian noise injection, which entangles magnitude and direction, our approach explicitly separates the perturbation direction from its scalar magnitude. This facilitates precise control over the sampling density near the manifold boundary. Given a state **q** _∈D_ raw, we generate a query point **q** ˜ via: 


Here, the perturbation direction **_u_** is drawn uniformly from the unit hypersphere S<sup>_N−_1</sup> , and the scalar magnitude _r_ is sampled from a half-normal distribution to concentrate sampling density near the manifold. The clip operation ensures **q** ˜ remains within joint limits [ **q** min _,_ **q** max]. The supervision label for **q** ˜ is computed as the distance to its nearest neighbor in the training set, retrieved via FAISS: 


**Interpolation-based Sampling.** To ensure the learned distance field is globally smooth and continuous, we employ linear interpolation. Since the raw data consists of discrete points, we generate intermediate samples between random pairs of poses to bridge gaps in the state space. We randomly sample 

pairs **q** _a,_ **q** _b_ from _D_ raw and construct intermediate states **q** ˜ = _α_ **q** _a_ + (1 _− α_ ) **q** _b_ using a mixing coefficient _α ∼_ Unif(0 _,_ 1). The interpolation dataset is defined as: 


The final dataset _D_ comprises 300 million state-distance pairs ( **q** _, d_ ). The data generation process was executed on a server equipped with 10 NVIDIA RTX 3090 GPUs and was completed in approximately 10 hours. 

## _B. Training Network_ 

To explicitly embed the kinematic structure of the 29-DoF G1 humanoid into our representation, we design a network = architecture that mirrors the robot’s topology. Let **q** [ _q_ 1 _, . . . , qK_ ]<sup>_⊤_</sup> denote the input configuration, where _qk ∈_ R represents the scalar state of the _k_ -th joint. We define a parent mapping _τ_ : _{_ 2 _, . . . , K} →{_ 1 _, . . . , K}_ that returns the index of the parent joint for any given joint _k_ . To capture the spatial dependency of each link on its ancestors, the network encodes features hierarchically along the kinematic chain. Formally, we employ a set of local encoders _{f_ enc<sup>(</sup><sup>_k_)</sup><sup>_}K_</sup> _k_ =1<sup>topropagatelatent</sup> information from the root to the end-effectors: 


where **v** _k ∈_ R<sup>16</sup> denotes the latent feature for joint _k_ . In this formulation, the root feature is derived purely from its local state, while subsequent child encodings are conditioned on both their local joint state _qk_ and the parent feature **v** _τ_ ( _k_ ). 

## _C. Riemannian Gradient for 1-DoF Joints_ 

Let _f_ : SO(3) _→_ R be differentiable, and let _∇f_ ( **R** ) denote the Euclidean (ambient) gradient under the Frobenius inner product _⟨_ **A** _,_ **B** _⟩_ ≜ Tr( **A**<sup>_⊤_</sup> **B** ). Projecting _∇f_ ( **R** ) onto the tangent space _T_ **R** SO(3) yields the Riemannian gradient: 


where Π **R** : R<sup>3</sup><sup>_×_3</sup> _→ T_ **R** SO(3) is the orthogonal projector and skew( **A** ) ≜ ( **A** _−_ **A**<sup>_⊤_</sup> ) _/_ 2. 

**Restriction to a 1-DoF revolute joint.** For a 1-DoF joint with fixed unit axis **k** _∈_ R<sup>3</sup> , the admissible motions form a 1D submanifold whose tangent space is spanned by 


To compare the gradient signal along this 1D direction, we compute the inner product between the second term of (29) 

and **V** : 


Using [ **k** ]<sup>_⊤_</sup> = _−_ [ **k** ] and the cyclic property of the trace, we can rewrite (32) as 


Combining (29) and (33) gives 


Thus, for a 1-DoF revolute joint, the gradient component along the admissible tangent direction **R** [ **k** ] is identical whether computed from the Riemannian gradient or directly from the Euclidean gradient. Equivalently, the derivative with respect to the scalar joint angle _q_ can be obtained using the Euclidean gradient _∇f_ ( **R** ). 

## _D. Implementation Details of RL-based Tracking_ 

All RL-based experiments, including our method, AMP [36] and ADD [52], are implemented using MimicKit [34] framework. Single-trajectory and style-based tracking are run on NVIDIA RTX 3090 GPUs, whereas the large-scale general motion tracking experiments are run on NVIDIA H20 GPUs. For fairness, we use the same default MimicKit hyperparameters for all methods (ours and baselines). For experiments that include our pose-prior reward, the reward weight _w_<sup>_P_</sup> and scale _α_<sup>_P_</sup> are set to 0 _._ 2 and 1, respectively, except for the Sideflip motion in style mimicry, where we set _w_<sup>_P_</sup> = 0 _._ 05. 

The retargeting experiments are based on the GMR framework [3] using the same configurations. We implement the prior task within the Mink IK solver [48] and solve it jointly with the GMR-defined tasks. 

## _E. More Experimental Results_ 

The learning curves for the baselines and our method on the single-trajectory motion tracking, style-based motion mimicry, and general motion tracking tasks are shown in Figure 6, Figure 7, and Figure 8, respectively. Across all motions, our method converges consistently faster than the baselines in both tasks, indicating that PDF-HR substantially improves sample efficiency. Figure 9 further reports the learning curves of ADD [52] trained with GMR [3]-retargeted data versus our 


**Fig. 6:** The learning curves of ADD and our method on the single-trajectory motion tracking task. 


**Fig. 7:** The learning curves of AMP and our method on the style-based motion mimicry task. 


**Fig. 8:** The learning curves of ADD and our method on general motion tracking task across various episode length. 


**Fig. 9:** The learning curves of the ADD general motion tracker trained on datasets produced by GMR and our method. 

retargeted data, highlighting the superior quality of our retargeting. Finally, Figure 10 visualizes intermediate qualitative results on style-based motion mimicry after 350M training samples for all policies. 

Figure 11, Figure 12, and Figure 13 report the learning curves of joint position error, mean reward, and undesired 


**Fig. 10:** Qualitative results of our method in style-based motion mimicry task with only 350 _M_ samples. 


**Fig. 11:** The learning curves of joint position error for the Beyondmimic policy trained on GMR-retargeted and our retargeted motion. 


**Fig. 12:** The learning curves of mean reward for the Beyondmimic policy trained on GMR-retargeted and our retargeted motion. 


**Fig. 13:** The learning curves of undesired contacts for the Beyondmimic policy trained on GMR-retargeted and our retargeted motion. 

contacts for the Beyondmimic [23] policy trained on GMRretargeted motion and our retargeted motion. Under the same training protocol as defined in Beyondmimic, policies trained with our retargeted motions consistently converge faster and reach better plateaus across the nine sequences: the joint position error in Figure 11 drops rapidly to a much lower level, while the GMR-retargeted counterpart typically stalls at a noticeably higher tracking error. This improved tracking quality is reflected in Figure 12, where our policy achieves higher mean rewards, indicating that the controller can satisfy task objectives more effectively once trained on physically consistent demonstrations. Moreover, Figure 13 shows that our retargeted data substantially reduces the undesired-contact penalty (often by a large margin) and yields smoother, less noisy curves, suggesting more stable learning dynamics and fewer spurious contacts during execution. Overall, our retargeting gives the policy better training data: the motions stay within kinematic limits and the contact timing is more consistent, which leads 


**Fig. 14: Visual comparisons of classical IK and our HL-IK.** We set the right-wrist end-effector to track an _∞_ -shaped trajectory. Classical QP-based IK (blue, left) meets the EE targets but can yield less natural whole-arm configurations, whereas our PDF-HR-regularized HL-IK (gray, right) produces more human-like arm postures while tracking the same trajectory. 

## to better training and easier deployment. 

## _F. Other Applications_ 

**Pose Denoising.** A critical application of our learned prior is pose denoising, which seeks to reconstruct physically plausible robot configurations from corrupted inputs. We leverage the pre-trained pose distance field as a fixed differentiable function to guide the optimization. Formally, the objective is to project a noisy query pose **q** init onto the nearest point on the valid motion manifold. For evaluation, **q** init is initialized via uniform sampling within joint limits. The pose is then iteratively refined by following the negative gradient of the distance field (Eq. (14)). As qualitatively demonstrated in Figure 15, the optimization effectively rectifies kinematic violations. The trajectory evolves from an initial state exhibiting severe selfpenetration and unnatural artifacts (left) to a collision-free, plausible configuration (right). 


**Fig. 15:** Visualization of the pose denoising process. 

**Human-Like Inverse Kinematics (HL-IK).** HL-IK [7] introduces a _human-like inverse kinematics_ setting: given only endeffector (EE) targets at runtime, the solver should track the EE while producing whole-arm configurations that remain humanlike, without relying on full-body sensing. Unlike HL-IK [7], which explicitly predicts non-EE joint/landmark targets, our method supports this task _implicitly_ by regularizing IK updates with the learned PDF-HR prior, making the approach more scalable and lightweight. 

Since the official HL-IK [7] implementation is not publicly available, we provide a qualitative demonstration. We define 

the right-wrist EE to follow a planar _∞_ -shaped trajectory and compare a classical QP-based IK solver against our PDF-HRregularized variant, as shown in Figure 14. Concretely, we integrate PDF-HR into a quadratic-programming IK solver for the Unitree G1 upper body. At each control step, IK solves for a joint increment ∆ **q** that satisfies task-space objectives while remaining close to the learned motion manifold. Given the current configuration **q** _t_ , we solve: 


optionally subject to joint position and velocity limits. Here, _J_ and **r** denote the task Jacobian and residual (e.g., end-effector pose error). The PDF-HR term biases the update direction using the local normal of the learned manifold, _∇fϕ_ ( **q** _t_ ): by penalizing motion along the normal, the optimizer favors steps within the tangent space, yielding kinematically plausible and human-like joint updates while still meeting the same taskspace targets. This soft regularization avoids explicit projection or hard feasibility constraints, yet keeps the solution close to the distribution of demonstrated human-like motions. **General Motion Tracking with PDF-HR.** To test whether PDF-HR generalizes to off-the-shelf motion trackers, we integrate our pose-prior reward into the low-level tracking policy of TextOp [43]. TextOp is a real-time, interactive framework for text-driven humanoid motion generation and control, featuring a two-layer design: a high-level text-conditioned diffusion autoregressive model generates a kinematic reference trajectory from the current user command, while a low-level universal tracking policy executes the trajectory on the robot to achieve responsive and accurate control. 

We adopt TextOp’s released low-level tracking policy as our baseline and follow the same training setup. Specifically, we train a general tracking policy on 10K motion clips sampled from AMASS [28] and LaFAN1 [13]. The only change from TextOp is that we additionally include the PDF-HR pose-prior reward (Eqs. (16) and (17)) during training, while keeping the network, observations, and all other reward terms unchanged. As shown in Figure 16a, our method consistently achieves lower joint pose MSE than the baseline throughout training. We further sweep the pose-prior weight _w_ to study its effect on the convergence rate. Figure 16b indicates that increasing _w_ noticeably accelerates convergence: the body-pose episode reward rises earlier and reaches a high plateau in fewer steps, while the final performance remains comparable across 

settings. Overall, these results suggest that PDF-HR serves as a plug-and-play regularizer that improves both sample efficiency and tracking accuracy for general motion tracking. 


**Fig. 16:** The key learning curves of training general tracking controller with original reward and our pose-prior integrated reward in 10K motion data. 

**Goal-conditioned Task.** We further validated PDF-HR on two goal-conditioned tasks defined in AMP [36]: Target Location (navigating to a random target position) and Target Heading (moving along a randomly changing direction at variable speeds). By incorporating our pose-prior reward into the AMP training objective with a weight _w_<sup>_P_</sup> = 0 _._ 1 and scale _α_<sup>_P_</sup> = 1 _._ 0, we evaluated the test episode length and task return. As illustrated in Figure 17, our method accelerates the convergence of the test episode length. This indicates that PDF-HR guides the agent to master basic locomotion skills faster. Consequently, this leads to better completion of highlevel goals, resulting in higher task returns compared to the original AMP. 


**Fig. 17:** The learning curves of AMP and our method on goal-conditioned tasks. 

